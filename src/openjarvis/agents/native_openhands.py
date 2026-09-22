"""NativeOpenHandsAgent -- code-execution-centric agent.

Renamed from ``OpenHandsAgent`` to clarify this is OpenJarvis's native
CodeAct-style implementation.  The ``OpenHandsAgent`` name is now used
for the real openhands-sdk integration in ``openhands.py``.
"""

from __future__ import annotations

import json as _json
import re
from typing import Any, List, Optional

from openjarvis.agents._stubs import AgentContext, AgentResult, ToolUsingAgent
from openjarvis.agents.prompt_loader import (
    load_few_shot_exemplars,
    load_system_prompt_override,
)
from openjarvis.core.events import EventBus
from openjarvis.core.registry import AgentRegistry
from openjarvis.core.types import Message, Role, ToolCall, ToolResult
from openjarvis.engine._stubs import InferenceEngine
from openjarvis.tools._stubs import BaseTool, build_tool_descriptions

OPENHANDS_SYSTEM_PROMPT = (  # noqa: E501
    "You are an AI assistant with access to tools. "
    "You MUST use tools when they would help answer "
    "the user's question.\n\n"
    "## How to use tools\n\n"
    "To call a tool, write on its own lines:\n\n"
    "Action: <tool_name>\n"
    "Action Input: <json_arguments>\n\n"
    "You will receive the result, then continue your "
    "response.\n\n"
    "## Available tools\n\n"
    "{tool_descriptions}\n\n"
    "## Important rules\n\n"
    "- When the user asks you to look up, search, fetch, "
    "or summarize a URL or topic, you MUST use web_search. "
    "Do NOT say you cannot browse the web.\n"
    "- When the user provides a URL, pass the FULL URL "
    "(including https://) as the query to web_search. "
    "Do NOT rewrite URLs into search keywords.\n"
    "- When the user asks a math question, use calculator.\n"
    "- When the user asks to read a file, use file_read.\n"
    "- You CAN write Python code in ```python blocks and "
    "it will be executed. Use this for computation, data "
    "processing, or when no specific tool fits.\n"
    "- If no tool or code is needed, respond directly "
    "with your answer.\n"
    "- Do NOT include <think> tags or internal reasoning "
    "in your response. Respond directly."
)


@AgentRegistry.register("native_openhands")
class NativeOpenHandsAgent(ToolUsingAgent):
    """Native CodeAct agent -- generates and executes Python code."""

    agent_id = "native_openhands"
    _default_temperature = 0.7
    _default_max_tokens = 2048
    _default_max_turns = 3

    def __init__(
        self,
        engine: InferenceEngine,
        model: str,
        *,
        tools: Optional[List[BaseTool]] = None,
        bus: Optional[EventBus] = None,
        max_turns: Optional[int] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        interactive: bool = False,
        confirm_callback=None,
    ) -> None:
        super().__init__(
            engine,
            model,
            tools=tools,
            bus=bus,
            max_turns=max_turns,
            temperature=temperature,
            max_tokens=max_tokens,
            interactive=interactive,
            confirm_callback=confirm_callback,
        )

    @staticmethod
    def _expand_urls(text: str) -> tuple[str, bool]:
        """If the user message contains a URL, fetch it and inline the content.

        Returns (possibly_expanded_text, was_expanded).
        """
        import re as _re

        url_match = _re.search(r"https?://[^\s,;\"'<>]+", text)
        if not url_match:
            return text, False
        url = url_match.group(0).rstrip(".,;)")
        try:
            from openjarvis.tools.web_search import WebSearchTool

            content = WebSearchTool._fetch_url(url, max_chars=4000)
            header = f"\n\n--- Content from {url} ---\n"
            footer = "\n--- End of content ---\n"
            expanded = text.replace(url, f"{header}{content}{footer}")
            return expanded, True
        except Exception:
            return text, False

    def _truncate_if_needed(
        self,
        messages: list[Message],
        max_prompt_tokens: int = 3000,
    ) -> list[Message]:
        """Truncate messages if estimated token count exceeds limit."""
        total_chars = sum(len(m.content) for m in messages)
        estimated_tokens = total_chars // 4
        if estimated_tokens <= max_prompt_tokens:
            return messages
        # Find the last user message and truncate its content
        for i in range(len(messages) - 1, -1, -1):
            if messages[i].role == Role.USER:
                excess_tokens = estimated_tokens - max_prompt_tokens
                excess_chars = excess_tokens * 4
                original = messages[i].content
                if len(original) > excess_chars + 200:
                    truncated = original[: len(original) - excess_chars]
                    messages[i] = Message(
                        role=Role.USER,
                        content=(
                            truncated + "\n\n[Input truncated to fit context window]"
                        ),
                    )
                break
        return messages

    @staticmethod
    def _strip_tool_call_text(text: str) -> str:
        """Remove raw tool call artifacts from final output."""
        # Remove Action: ... Action Input: ... blocks
        text = re.sub(
            r"Action:\s*.+?(?:Action Input:\s*.+?)?(?=\n\n|\Z)",
            "",
            text,
            flags=re.DOTALL | re.IGNORECASE,
        )
        # Remove <tool_call>...</tool_call> or </tool_name> blocks
        text = re.sub(r"<tool_call>.*?</\w+>", "", text, flags=re.DOTALL)
        return text.strip()

    def _extract_code(self, text: str) -> str | None:
        """Extract Python code from markdown code blocks."""
        match = re.search(r"```python\n(.*?)```", text, re.DOTALL)
        if match:
            return match.group(1).strip()
        return None



    def run(
        self,
        input: str,
        context: Optional[AgentContext] = None,
        **kwargs: Any,
    ) -> AgentResult:
        self._emit_turn_start(input)
        _oj_run_id = _oj_run_start(self, context, input)

        tool_descriptions = build_tool_descriptions(self._tools)
        prompt_template = (
            load_system_prompt_override("native_openhands") or OPENHANDS_SYSTEM_PROMPT
        )
        system_prompt = prompt_template.format(
            tool_descriptions=tool_descriptions,
        )

        # Pre-fetch any URLs in the input so the LLM gets the content directly
        input, url_expanded = self._expand_urls(input)

        # If URL content was inlined, skip the tool loop -- just summarize directly
        if url_expanded:
            direct_messages: list[Message] = [
                Message(
                    role=Role.SYSTEM,
                    content=(
                        "You are a helpful assistant. "
                        "Respond directly to the user's "
                        "request using the provided content."
                        " Do NOT include <think> tags."
                    ),
                ),
                Message(role=Role.USER, content=input),
            ]
            direct_messages = self._truncate_if_needed(direct_messages)
            try:
                result = self._generate(direct_messages)
            except Exception:
                # Propagate to the eval runner / server bridge so the failure
                # is recorded as an error instead of a fake "input too long"
                # answer that silently scores as 0%. Telemetry boundary is
                # still emitted before re-raising.
                self._emit_turn_end(turns=1, error=True)
                raise
            content = self._strip_think_tags(result.get("content", ""))
            usage = result.get("usage", {})
            _oj_run_end(_oj_run_id, "urldirect", 1, [], content)
            self._emit_turn_end(turns=1)
            return AgentResult(
                content=content,
                tool_results=[],
                turns=1,
                metadata={
                    "prompt_tokens": usage.get("prompt_tokens", 0),
                    "completion_tokens": usage.get("completion_tokens", 0),
                    "total_tokens": usage.get("total_tokens", 0),
                },
            )

        messages = self._build_messages(input, context, system_prompt=system_prompt)

        # Inject few-shot exemplars before the user input
        for ex in load_few_shot_exemplars("native_openhands"):
            if ex.get("input") and ex.get("output"):
                messages.insert(-1, Message(role=Role.USER, content=ex["input"]))
                messages.insert(-1, Message(role=Role.ASSISTANT, content=ex["output"]))

        messages = self._truncate_if_needed(messages)

        all_tool_results: list[ToolResult] = []
        turns = 0
        last_content = ""
        total_usage = {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0}

        # Build OpenAI-format tool schemas for native function calling
        openai_tools = self._executor.get_openai_tools() if self._tools else []
        # Side dict for Gemini thought_signatures (ToolCall uses slots)
        _thought_sigs: dict[str, bytes] = {}

        for _turn in range(self._max_turns):
            turns += 1
            _oj_turn_id = _oj_set_turn(_oj_run_id, turns)
            # Truncate before every generate call -- tool results may have
            # expanded the context beyond what the model supports.
            messages = self._truncate_if_needed(messages)

            gen_kwargs: dict[str, Any] = {}
            if openai_tools:
                gen_kwargs["tools"] = openai_tools

            try:
                result = self._generate(messages, **gen_kwargs)
            except Exception:
                # Propagate so the eval runner records a real error rather
                # than a fake "input too long" string that silently scores 0.
                self._emit_turn_end(turns=turns, error=True)
                raise

            # Accumulate usage from this generate call
            usage = result.get("usage", {})
            for k in total_usage:
                total_usage[k] += usage.get(k, 0)

            content = result.get("content", "")
            _oj_raw = content
            # Strip think tags so they don't interfere with parsing
            content = self._strip_think_tags(content)
            last_content = content

            # --- Native function-calling path (OpenAI, Anthropic, etc.) ---
            raw_tool_calls = result.get("tool_calls", [])
            _oj_raw_gen(_oj_run_id, _oj_turn_id, _oj_raw, content, len(raw_tool_calls))
            if raw_tool_calls:
                native_calls = []
                for i, tc in enumerate(raw_tool_calls):
                    call = ToolCall(
                        id=tc.get("id", f"call_{turns}_{i}"),
                        name=tc.get("name", ""),
                        arguments=tc.get("arguments", "{}"),
                    )
                    # Preserve thought_signature for Gemini reasoning
                    sig = tc.get("thought_signature")
                    if sig is not None:
                        _thought_sigs[call.id] = sig
                    native_calls.append(call)
                messages.append(
                    Message(
                        role=Role.ASSISTANT,
                        content=content,
                        tool_calls=native_calls,
                    )
                )
                for tc in native_calls:
                    tool_result = self._executor.execute(tc)
                    all_tool_results.append(tool_result)
                    obs_text = tool_result.content
                    if len(obs_text) > 4000:
                        obs_text = obs_text[:4000] + "\n\n[Output truncated]"
                    messages.append(
                        Message(
                            role=Role.TOOL,
                            content=obs_text,
                            tool_call_id=tc.id,
                            name=tc.name,
                        )
                    )
                continue

            # --- Text-based fallback (CodeAct / Action-Input format) ---

            # Try to extract code
            code = self._extract_code(content)
            if code:
                messages.append(Message(role=Role.ASSISTANT, content=content))

                # Execute via code_interpreter tool if available
                tool_call = ToolCall(
                    id=f"code_{turns}",
                    name="code_interpreter",
                    arguments=_json.dumps({"code": code}),
                )
                tool_result = self._executor.execute(tool_call)
                all_tool_results.append(tool_result)

                obs_text = tool_result.content
                if len(obs_text) > 4000:
                    obs_text = obs_text[:4000] + "\n\n[Output truncated]"
                observation = f"Output:\n{obs_text}"
                messages.append(Message(role=Role.USER, content=observation))
                continue

            # Try tool call
            tool_info = self._extract_text_tool_call(content)  # openjarvis-w77-dedupe-v1 (base ToolUsingAgent)
            if tool_info:
                action, action_input = tool_info
                messages.append(Message(role=Role.ASSISTANT, content=content))

                tool_call = ToolCall(
                    id=f"tool_{turns}", name=action, arguments=action_input
                )
                tool_result = self._executor.execute(tool_call)
                all_tool_results.append(tool_result)

                obs_text = tool_result.content
                if len(obs_text) > 4000:
                    obs_text = obs_text[:4000] + "\n\n[Output truncated]"
                observation = f"Result: {obs_text}"
                messages.append(Message(role=Role.USER, content=observation))
                continue

            # No code or tool call -- this is the final answer
            content = self._strip_think_tags(content)
            content = self._strip_tool_call_text(content)
            _oj_run_end(_oj_run_id, "final", turns, all_tool_results, content)
            self._emit_turn_end(turns=turns)
            return AgentResult(
                content=content,
                tool_results=all_tool_results,
                turns=turns,
                metadata=total_usage,
            )

        # Max turns
        final = self._strip_think_tags(last_content) or "Maximum turns reached."
        final = self._strip_tool_call_text(final)
        _oj_run_end(_oj_run_id, "maxturns", turns, all_tool_results, final)
        result = self._max_turns_result(all_tool_results, turns, content=final)
        result.metadata.update(total_usage)
        return result



# --- openjarvis-agent-log-v1 -------------------------------------------------
# Turn-boundary record in its own rotating file, so an agent turn that
# dispatched NOTHING is distinguishable from one that was never instrumented.
# Also sets tools._stubs.CURRENT_TURN_ID (a ContextVar) so dispatch.log lines
# carry a real turn id.  Every call site is exception-swallowing on purpose:
# instrumentation must never be able to break a run.
_oj_agent_logger = None


def _oj_get_agent_logger():
    global _oj_agent_logger
    if _oj_agent_logger is not None:
        return _oj_agent_logger
    import logging as _lgm
    import logging.handlers as _lgh
    import os as _os

    lg = _lgm.getLogger("openjarvis.agent")
    if not lg.handlers:
        log_dir = _os.path.join(
            _os.environ.get("LOCALAPPDATA", _os.path.expanduser("~")),
            "OpenJarvis", "logs",
        )
        try:
            _os.makedirs(log_dir, exist_ok=True)
            h = _lgh.RotatingFileHandler(
                _os.path.join(log_dir, "agent.log"),
                maxBytes=2621440, backupCount=4, encoding="utf-8",
            )
            h.setFormatter(_lgm.Formatter("%(asctime)s %(levelname)s %(message)s"))
            lg.addHandler(h)
        except Exception:
            lg.addHandler(_lgm.NullHandler())
    lg.setLevel(_lgm.INFO)
    lg.propagate = False
    _oj_agent_logger = lg
    return lg


def _oj_conv_id(context):
    for attr in ("conversation_id", "session_id", "thread_id", "id"):
        v = getattr(context, attr, None)
        if v:
            return str(v)
    meta = getattr(context, "metadata", None)
    if isinstance(meta, dict):
        for k in ("conversation_id", "session_id", "thread_id"):
            if meta.get(k):
                return str(meta[k])
    return "-"


def _oj_model_name(agent):
    for attr in ("_model", "model", "_model_name"):
        v = getattr(agent, attr, None)
        if isinstance(v, str) and v:
            return v
    llm = getattr(agent, "_llm", None) or getattr(agent, "llm", None)
    for attr in ("model", "model_name", "_model"):
        v = getattr(llm, attr, None)
        if isinstance(v, str) and v:
            return v
    return "-"


def _oj_run_start(agent, context, input_text):
    import uuid as _uuid

    run_id = _uuid.uuid4().hex[:8]
    try:
        _oj_get_agent_logger().info(
            "RUNSTART run=%s agent=%s model=%s conv=%s tools=%d maxturns=%s chars=%d",
            run_id,
            type(agent).__name__,
            _oj_model_name(agent),
            _oj_conv_id(context),
            len(getattr(agent, "_tools", []) or []),
            getattr(agent, "_max_turns", "-"),
            len(input_text or ""),
        )
    except Exception:
        pass
    return run_id


def _oj_set_turn(run_id, turns):
    turn_id = "%s-t%d" % (run_id, turns)
    try:
        from openjarvis.tools._stubs import CURRENT_TURN_ID as _cti

        _cti.set(turn_id)
    except Exception:
        pass
    try:
        _oj_get_agent_logger().info(
            "TURN run=%s turn=%s n=%d", run_id, turn_id, turns
        )
    except Exception:
        pass
    return turn_id


def _oj_run_end(run_id, kind, turns, tool_results, content):
    try:
        head = (content or "")[:160].replace("\n", " ").replace("\r", " ")
        _oj_get_agent_logger().info(
            "RUNEND run=%s exit=%s turns=%s dispatched=%d chars=%d head=%s",
            run_id, kind, turns,
            len(tool_results or []),
            len(content or ""),
            head,
        )
    except Exception:
        pass


# --- end openjarvis-agent-log-v1 ---------------------------------------------




def _oj_raw_gen(run_id, turn_id, raw, stripped, n_tool_calls):
    """openjarvis-raw-gen-v1 - log the pre-strip generation for one turn."""
    try:
        raw = raw or ""
        stripped = stripped or ""
        _oj_get_agent_logger().info(
            "RAWGEN run=%s turn=%s rawlen=%d striplen=%d changed=%s ntc=%d raw=%s",
            run_id, turn_id, len(raw), len(stripped),
            (raw != stripped), n_tool_calls, repr(raw[:1500]),
        )
    except Exception:
        pass
__all__ = ["NativeOpenHandsAgent"]
