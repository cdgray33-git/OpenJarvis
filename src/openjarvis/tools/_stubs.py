"""ABC for tool implementations and the ToolExecutor dispatch engine.

Follows the same registry pattern as ``engine/_stubs.py`` and ``memory/_stubs.py``.
Each tool is registered via ``@ToolRegistry.register("name")`` and implements
``BaseTool`` with a ``spec`` property and ``execute()`` method.
"""

from __future__ import annotations

import concurrent.futures
import contextvars
import json
import logging
import logging.handlers
import os
import threading
import time
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional

from openjarvis.core.events import EventBus, EventType
from openjarvis.core.types import ToolCall, ToolResult

# ---------------------------------------------------------------------------
# ToolSpec — metadata describing a tool's interface
# ---------------------------------------------------------------------------


@dataclass(slots=True)
class ToolSpec:
    """Declarative description of a tool's interface and characteristics."""

    name: str
    description: str
    parameters: Dict[str, Any] = field(default_factory=dict)
    category: str = ""
    cost_estimate: float = 0.0
    latency_estimate: float = 0.0
    requires_confirmation: bool = False
    timeout_seconds: float = 30.0
    required_capabilities: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


# ---------------------------------------------------------------------------
# BaseTool ABC
# ---------------------------------------------------------------------------


class BaseTool(ABC):
    """Base class for all tool implementations.

    Subclasses must be registered via
    ``@ToolRegistry.register("name")`` to become discoverable.
    """

    tool_id: str
    is_local: bool = True

    @property
    @abstractmethod
    def spec(self) -> ToolSpec:
        """Return the tool specification."""

    @abstractmethod
    def execute(self, **params: Any) -> ToolResult:
        """Execute the tool with the given parameters."""

    def to_openai_function(self) -> Dict[str, Any]:
        """Convert to OpenAI function-calling format."""
        from openjarvis.tools.description_loader import (
            get_tool_description_override,
        )

        s = self.spec
        desc = get_tool_description_override(s.name) or s.description
        return {
            "type": "function",
            "function": {
                "name": s.name,
                "description": desc,
                "parameters": s.parameters,
            },
        }


# ---------------------------------------------------------------------------
# ToolExecutor — dispatch engine for tool calls
# ---------------------------------------------------------------------------



# --- openjarvis-dispatch-log-v1 ---------------------------------------------------
# Tool-boundary dispatch record in its own rotating file, so a turn that
# dispatched NOTHING is distinguishable from one never instrumented.
CURRENT_TURN_ID: contextvars.ContextVar = contextvars.ContextVar(
    "openjarvis_turn_id", default="-"
)

# openjarvis-confirm-emit-v1 - lets a Callable[[str], bool] confirm callback learn
# which confirm_id it is being asked about, without widening its signature.
CURRENT_CONFIRM_ID = contextvars.ContextVar("openjarvis_confirm_id", default="")
_dispatch_logger = None


def _get_dispatch_logger():
    global _dispatch_logger
    if _dispatch_logger is not None:
        return _dispatch_logger
    lg = logging.getLogger("openjarvis.dispatch")
    if not lg.handlers:
        log_dir = os.path.join(
            os.environ.get("LOCALAPPDATA", os.path.expanduser("~")),
            "OpenJarvis", "logs",
        )
        try:
            os.makedirs(log_dir, exist_ok=True)
            h = logging.handlers.RotatingFileHandler(
                os.path.join(log_dir, "dispatch.log"),
                maxBytes=2 * 1024 * 1024, backupCount=4, encoding="utf-8",
            )
            h.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
            lg.addHandler(h)
        except Exception:
            lg.addHandler(logging.NullHandler())
    lg.setLevel(logging.INFO)
    lg.propagate = False
    _dispatch_logger = lg
    return lg


def _args_digest(rawargs, limit: int = 400) -> str:
    try:
        s = rawargs if isinstance(rawargs, str) else json.dumps(rawargs, default=str)
    except Exception:
        s = str(rawargs)
    s = " ".join(s.split())
    return s[:limit] + ("...TRUNC" if len(s) > limit else "")


class ToolExecutor:
    """Dispatch tool calls to registered tools with event bus integration.

    Parameters
    ----------
    tools:
        List of tool instances to make available.
    bus:
        Optional event bus for publishing ``TOOL_CALL_START``/``TOOL_CALL_END``.
    """

    def __init__(
        self,
        tools: List[BaseTool],
        bus: Optional[EventBus] = None,
        *,
        interactive: bool = False,
        confirm_callback: Optional[Callable[[str], bool]] = None,
        default_timeout: float = 30.0,
        capability_policy: Optional[Any] = None,
        agent_id: str = "",
        boundary_guard: Optional[Any] = None,
    ) -> None:
        self._tools: Dict[str, BaseTool] = {t.spec.name: t for t in tools}
        self._bus = bus
        self._interactive = interactive
        self._confirm_callback = confirm_callback
        self._default_timeout = default_timeout
        self._capability_policy = capability_policy
        self._agent_id = agent_id
        self._boundary_guard = boundary_guard

    def execute(self, tool_call: ToolCall) -> ToolResult:
        """Parse arguments, dispatch to tool, measure latency, emit events."""
        _get_dispatch_logger().info(
            "ATTEMPT turn=%s tool=%s args=%s thread=%s",
            CURRENT_TURN_ID.get(), tool_call.name,
            _args_digest(tool_call.arguments),
            threading.current_thread().name,
        )
        tool = self._tools.get(tool_call.name)
        if tool is None:
            return ToolResult(
                tool_name=tool_call.name,
                content=f"Unknown tool: {tool_call.name}",
                success=False,
            )

        # Parse arguments
        try:
            params = json.loads(tool_call.arguments) if tool_call.arguments else {}
        except json.JSONDecodeError as exc:
            return ToolResult(
                tool_name=tool_call.name,
                content=f"Invalid arguments JSON: {exc}",
                success=False,
            )

        # Boundary guard: scan external tool arguments
        if self._boundary_guard is not None and not getattr(tool, "is_local", True):
            try:
                tool_call = self._boundary_guard.check_outbound(tool_call)
                # Re-parse arguments after potential redaction
                params = json.loads(tool_call.arguments) if tool_call.arguments else {}
            except Exception as exc:
                return ToolResult(
                    tool_name=tool_call.name,
                    content=f"Security block: {exc}",
                    success=False,
                )

        # RBAC capability check
        if self._capability_policy and tool.spec.required_capabilities:
            for cap in tool.spec.required_capabilities:
                if not self._capability_policy.check(
                    self._agent_id,
                    cap,
                    tool_call.name,
                ):
                    if self._bus:
                        self._bus.publish(
                            EventType.CAPABILITY_DENIED,
                            {
                                "agent_id": self._agent_id,
                                "capability": cap,
                                "tool": tool_call.name,
                            },
                        )
                    return ToolResult(
                        tool_name=tool_call.name,
                        content=(
                            f"Capability '{cap}' denied for"
                            f" agent '{self._agent_id}'"
                            f" on tool '{tool_call.name}'."
                        ),
                        success=False,
                    )

        # Taint checking (sink policy)
        taint_set = params.get("_taint") if isinstance(params, dict) else None
        if taint_set is not None:
            try:
                from openjarvis.security.taint import TaintSet, check_taint

                if isinstance(taint_set, TaintSet):
                    violation = check_taint(tool_call.name, taint_set)
                    if violation:
                        if self._bus:
                            self._bus.publish(
                                EventType.TAINT_VIOLATION,
                                {
                                    "tool": tool_call.name,
                                    "violation": violation,
                                },
                            )
                        return ToolResult(
                            tool_name=tool_call.name,
                            content=f"Taint violation: {violation}",
                            success=False,
                        )
            except ImportError:
                pass
            # Remove internal taint key before passing to tool
            if isinstance(params, dict):
                params.pop("_taint", None)

        # Confirmation check for sensitive tools
        if tool.spec.requires_confirmation:
            if not self._interactive or self._confirm_callback is None:
                return ToolResult(
                    tool_name=tool_call.name,
                    content=(
                        f"Tool '{tool_call.name}' requires"
                        " confirmation but no confirmation"
                        " callback is available."
                    ),
                    success=False,
                )
            # openjarvis-confirm-emit-v1 - Defect 6 / 6c step 3
            from openjarvis.core import confirm_registry as _cr

            _digest = _args_digest(tool_call.arguments)
            prompt = (
                f"Allow execution of tool '{tool_call.name}' "
                f"with args {_digest}?"
            )
            _cid = _cr.register(
                tool=tool_call.name,
                agent_id=self._agent_id,
                turn_id=CURRENT_TURN_ID.get(),
            )
            _entry = _cr.get(_cid) or {}
            if self._bus:
                self._bus.publish(
                    EventType.TOOL_CONFIRM_REQUEST,
                    {
                        "confirm_id": _cid,
                        "agent_id": self._agent_id,
                        "turn_id": CURRENT_TURN_ID.get(),
                        "tool": tool_call.name,
                        "args_digest": _digest,
                        "prompt": prompt,
                        "expires_at": _entry.get("expires_at"),
                    },
                )
            _token = CURRENT_CONFIRM_ID.set(_cid)
            try:
                _approved = self._confirm_callback(prompt)
            finally:
                CURRENT_CONFIRM_ID.reset(_token)
            # openjarvis-confirm-resolved-v1
            _resolved = _cr.get(_cid) or {}
            _decision = _resolved.get("decision") or (
                _cr.APPROVED if _approved else _cr.TIMEOUT
            )
            if self._bus:
                self._bus.publish(
                    EventType.TOOL_CONFIRM_RESOLVED,
                    {
                        "confirm_id": _cid,
                        "agent_id": self._agent_id,
                        "turn_id": CURRENT_TURN_ID.get(),
                        "tool": tool_call.name,
                        "decision": _decision,
                        "state": _resolved.get("state"),
                        "created_at": _resolved.get("created_at"),
                        "expires_at": _resolved.get("expires_at"),
                        "reaped": not _resolved,
                    },
                )
            if not _approved:
                _final = (_cr.get(_cid) or {}).get("decision")
                if _final == _cr.DENIED:
                    _content = (
                        f"Tool '{tool_call.name}' execution denied by user."
                    )
                elif _final == _cr.APPROVED:
                    _content = (
                        f"Tool '{tool_call.name}' was approved but the "
                        "confirmation callback returned False. The tool did "
                        "NOT run. Report this as an internal error, not as a "
                        "refusal."
                    )
                else:
                    _content = (
                        f"Tool '{tool_call.name}' was NOT executed because no "
                        "confirmation answer arrived before the request "
                        "expired. This is a TIMEOUT, not a refusal - the user "
                        "did not deny it. Ask the user again rather than "
                        "reporting that permission was refused."
                    )
                return ToolResult(
                    tool_name=tool_call.name,
                    content=_content,
                    success=False,
                )

        # Emit start event
        if self._bus:
            self._bus.publish(
                EventType.TOOL_CALL_START,
                {"tool": tool_call.name, "arguments": params},
            )

        # Execute with timeout
        timeout = tool.spec.timeout_seconds or self._default_timeout
        t0 = time.time()
        try:
            with concurrent.futures.ThreadPoolExecutor(max_workers=1) as pool:
                future = pool.submit(tool.execute, **params)
                result = future.result(timeout=timeout)
        except concurrent.futures.TimeoutError:
            if self._bus:
                self._bus.publish(
                    EventType.TOOL_TIMEOUT,
                    {"tool": tool_call.name, "timeout": timeout},
                )
            # openjarvis-tool-timeout-v1
            result = ToolResult(
                tool_name=tool_call.name,
                content=(
                    f"Tool '{tool_call.name}' exceeded its {timeout:.0f}s wait. "
                    "OUTCOME UNKNOWN: the operation was NOT cancelled and may have "
                    "completed successfully. Do NOT retry it and do NOT report it "
                    "as failed. Verify the current state with a read-only check "
                    "first, then report what the verification found."
                ),
                success=False,
            )
            result.metadata["timed_out"] = True
            result.metadata["outcome_verified"] = False
        except Exception as exc:
            result = ToolResult(
                tool_name=tool_call.name,
                content=f"Tool execution error: {exc}",
                success=False,
            )
        latency = time.time() - t0
        result.latency_seconds = latency
        result.metadata["arguments"] = params

        # Auto-detect taints in results
        if result.success:
            try:
                from openjarvis.security.taint import auto_detect_taint

                detected = auto_detect_taint(result.content)
                if detected and detected.labels:
                    result.metadata["_taint"] = detected
            except ImportError:
                pass

        # Emit end event
        if self._bus:
            result_text = str(result.content)[:10240] if result.content else ""
            # Pass through ToolResult.metadata so downstream consumers
            # (TraceCollector → TraceStep.metadata → SkillOptimizer) can
            # see skill-tagged invocations.  Filter to JSON-serializable
            # values only — internal objects like TaintSet (added by the
            # taint auto-detect above) must not leak to event subscribers
            # since the trace store will JSON-serialize them later.
            event_metadata = self._json_safe_metadata(result.metadata)
            self._bus.publish(
                EventType.TOOL_CALL_END,
                {
                    "tool": tool_call.name,
                    "success": result.success,
                    "latency": latency,
                    "result": result_text,
                    "metadata": event_metadata,
                },
            )

        _get_dispatch_logger().info(
            "OUTCOME turn=%s tool=%s success=%s latency=%.3f timed_out=%s",
            CURRENT_TURN_ID.get(), tool_call.name, result.success,
            latency, bool(result.metadata.get("timed_out")),
        )
        return result

    @staticmethod
    def _json_safe_metadata(metadata: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """Return a copy of *metadata* containing only JSON-serializable values.

        ``ToolExecutor`` annotates ``ToolResult.metadata`` with internal
        objects (currently ``_taint: TaintSet``).  Those are useful for
        in-process security checks but cannot be serialized when the
        ``TraceCollector`` writes ``TraceStep.metadata`` to JSON in the
        SQLite trace store.  This helper drops any keys whose value is
        not JSON-safe — silently, since the missing data is not
        load-bearing for downstream consumers.
        """
        if not metadata:
            return {}

        import json

        safe: Dict[str, Any] = {}
        for key, value in metadata.items():
            if not isinstance(key, str):
                continue
            try:
                json.dumps(value)
            except (TypeError, ValueError):
                # Skip non-serializable values (e.g. TaintSet)
                continue
            safe[key] = value
        return safe

    def available_tools(self) -> List[ToolSpec]:
        """Return specs for all available tools."""
        return [t.spec for t in self._tools.values()]

    def get_openai_tools(self) -> List[Dict[str, Any]]:
        """Return tools in OpenAI function-calling format."""
        return [t.to_openai_function() for t in self._tools.values()]


def build_tool_descriptions(
    tools: List[BaseTool],
    *,
    include_category: bool = True,
    include_cost: bool = False,
) -> str:
    """Build rich text descriptions from a list of tools.

    This is the single source of truth for all text-based agents that need
    to describe available tools in their system prompts.

    Parameters
    ----------
    tools:
        List of tool instances.
    include_category:
        Whether to include the ``Category:`` line.
    include_cost:
        Whether to include ``Cost estimate:`` and ``Latency estimate:`` lines.

    Returns
    -------
    str
        Formatted multi-tool description, or ``"No tools available."`` if
        *tools* is empty.
    """
    if not tools:
        return "No tools available."

    from openjarvis.tools.description_loader import (
        get_tool_description_override,
    )

    sections: list[str] = []
    for t in tools:
        s = t.spec
        desc = get_tool_description_override(s.name) or s.description
        lines = [f"### {s.name}", desc]

        if include_category and s.category:
            lines.append(f"Category: {s.category}")

        if include_cost:
            if s.cost_estimate:
                lines.append(f"Cost estimate: ${s.cost_estimate:.4f}")
            if s.latency_estimate:
                lines.append(f"Latency estimate: {s.latency_estimate:.1f}s")

        # Parameter descriptions
        props = s.parameters.get("properties", {})
        required = set(s.parameters.get("required", []))
        if props:
            lines.append("Parameters:")
            for pname, pinfo in props.items():
                ptype = pinfo.get("type", "any")
                req_mark = ", required" if pname in required else ""
                desc = pinfo.get("description", "")
                if desc:
                    lines.append(f"  - {pname} ({ptype}{req_mark}): {desc}")
                else:
                    lines.append(f"  - {pname} ({ptype}{req_mark})")

        sections.append("\n".join(lines))

    return "\n\n".join(sections)


__all__ = ["BaseTool", "ToolExecutor", "ToolSpec", "build_tool_descriptions"]
