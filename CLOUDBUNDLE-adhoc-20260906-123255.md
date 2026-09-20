# OPENJARVIS CODE REVIEW BUNDLE

- marker: `openjarvis-cloudbundle-v1`
- set: `adhoc` - ad hoc bundle
- generated: 2026-09-06T12:32:55
- repo root: `C:\Users\Admin\OpenJarvis`
- files in bundle: 3

You are reviewing complete source files. Every file is included in full, with authoritative 1-based line numbers in the left gutter. Nothing has been elided.

---

# THE QUESTION

SYSTEM PROMPT ASSEMBLY AUDIT. In native_openhands.py the SYSTEM message is built at :324-330: build_tool_descriptions(self._tools) is formatted into (load_system_prompt_override('native_openhands') or OPENHANDS_SYSTEM_PROMPT). Few-shot exemplars are then inserted at :376-380 via messages.insert(-1,...) as alternating Role.USER/Role.ASSISTANT pairs. A downstream guard _truncate_if_needed (:113-138) sums characters across ALL messages and compares chars//4 against a hardcoded 3000 token budget, so every component below directly determines whether that guard fires. Q1: load_system_prompt_override at prompt_loader.py:30 - what exact path or paths on disk does it look for, what filename convention for agent_name='native_openhands', and what does it return if the file is absent, empty, or unreadable? State whether a silent fallback to OPENHANDS_SYSTEM_PROMPT is distinguishable from an override that loaded successfully. Q2: load_few_shot_exemplars at prompt_loader.py:53 - where does it read from, how many exemplars does it return by default, is there any cap on count or size, and what is the realistic total character volume it contributes? Q3: build_tool_descriptions at tools/_stubs.py:480 - what exactly does it render per tool, and for a registry of 12 tools estimate the total character count and token count of its output. Q4: given Q1-Q3, give a component-by-component character and token budget for the assembled SYSTEM message plus exemplars, before any user input. State the total and compare it against a 3000 token budget and against num_ctx 16384. Q5: is there ANY code path where the exemplars or the override are logged, counted, or otherwise observable at runtime, or is the assembled prompt size invisible? Answer each separately and cite file:line. Do not estimate where you can count.

---

# SOURCE

---

## FILE: `src/openjarvis/agents/prompt_loader.py`

- bytes: 2669
- lines: 83
- sha256: `A48EE0C8627FBD4B31EF39922CB08363456747EF525A637503920DABB8ABCF5A`
- line terminator: LF

Line numbers below are 1-based and authoritative. Cite them.

```python
 1 | """Load system prompt and few-shot overrides from $OPENJARVIS_HOME.
 2 | 
 3 | LLM-guided spec search (M1) proposes edits that get written to disk by appliers.
 4 | This module lets agents pick those overrides up at runtime:
 5 | 
 6 | - System prompts: ``$OPENJARVIS_HOME/agents/{name}/system_prompt.md``
 7 | - Few-shot exemplars: ``$OPENJARVIS_HOME/agents/{name}/few_shot.json``
 8 | 
 9 | Override files are templates — they may contain ``{tool_descriptions}`` and
10 | other format placeholders that the agent fills in via ``.format()``, exactly
11 | like the hardcoded constants.
12 | """
13 | 
14 | from __future__ import annotations
15 | 
16 | import json
17 | import logging
18 | import os
19 | from pathlib import Path
20 | from typing import Any
21 | 
22 | logger = logging.getLogger(__name__)
23 | 
24 | 
25 | def _openjarvis_home() -> Path:
26 |     """Resolve $OPENJARVIS_HOME, defaulting to ~/.openjarvis."""
27 |     return Path(os.environ.get("OPENJARVIS_HOME", "~/.openjarvis")).expanduser()
28 | 
29 | 
30 | def load_system_prompt_override(agent_name: str) -> str | None:
31 |     """Return the override prompt for *agent_name*, or ``None``.
32 | 
33 |     Looks for ``$OPENJARVIS_HOME/agents/<agent_name>/system_prompt.md``.
34 |     ``OPENJARVIS_HOME`` defaults to ``~/.openjarvis`` when unset.
35 |     """
36 |     home = _openjarvis_home()
37 |     prompt_path = home / "agents" / agent_name / "system_prompt.md"
38 |     if not prompt_path.exists():
39 |         return None
40 |     try:
41 |         content = prompt_path.read_text(encoding="utf-8")
42 |         logger.info(
43 |             "Loaded system prompt override for %s from %s", agent_name, prompt_path
44 |         )
45 |         return content
46 |     except Exception:
47 |         logger.warning(
48 |             "Failed to read system prompt override at %s", prompt_path, exc_info=True
49 |         )
50 |         return None
51 | 
52 | 
53 | def load_few_shot_exemplars(
54 |     agent_name: str,
55 | ) -> list[dict[str, Any]]:
56 |     """Return few-shot exemplars for *agent_name*, or empty list.
57 | 
58 |     Looks for ``$OPENJARVIS_HOME/agents/<agent_name>/few_shot.json``.
59 |     Expected format: ``[{"input": "Q", "output": "A"}, ...]``.
60 |     """
61 |     home = _openjarvis_home()
62 |     fs_path = home / "agents" / agent_name / "few_shot.json"
63 |     if not fs_path.exists():
64 |         return []
65 |     try:
66 |         data = json.loads(fs_path.read_text(encoding="utf-8"))
67 |         if not isinstance(data, list):
68 |             logger.warning("few_shot.json for %s is not a list", agent_name)
69 |             return []
70 |         logger.info(
71 |             "Loaded %d few-shot exemplars for %s from %s",
72 |             len(data),
73 |             agent_name,
74 |             fs_path,
75 |         )
76 |         return data
77 |     except Exception:
78 |         logger.warning(
79 |             "Failed to read few-shot exemplars at %s",
80 |             fs_path,
81 |             exc_info=True,
82 |         )
83 |         return []
```

---

## FILE: `src/openjarvis/tools/_stubs.py`

- bytes: 21068
- lines: 547
- sha256: `08B90B18308A4FB6B345921641A50CEFEEC015A3388BAD2202A27D4F150BF089`
- line terminator: CRLF

Line numbers below are 1-based and authoritative. Cite them.

```python
  1 | """ABC for tool implementations and the ToolExecutor dispatch engine.
  2 | 
  3 | Follows the same registry pattern as ``engine/_stubs.py`` and ``memory/_stubs.py``.
  4 | Each tool is registered via ``@ToolRegistry.register("name")`` and implements
  5 | ``BaseTool`` with a ``spec`` property and ``execute()`` method.
  6 | """
  7 | 
  8 | from __future__ import annotations
  9 | 
 10 | import concurrent.futures
 11 | import contextvars
 12 | import json
 13 | import logging
 14 | import logging.handlers
 15 | import os
 16 | import threading
 17 | import time
 18 | from abc import ABC, abstractmethod
 19 | from dataclasses import dataclass, field
 20 | from typing import Any, Callable, Dict, List, Optional
 21 | 
 22 | from openjarvis.core.events import EventBus, EventType
 23 | from openjarvis.core.types import ToolCall, ToolResult
 24 | 
 25 | # ---------------------------------------------------------------------------
 26 | # ToolSpec — metadata describing a tool's interface
 27 | # ---------------------------------------------------------------------------
 28 | 
 29 | 
 30 | @dataclass(slots=True)
 31 | class ToolSpec:
 32 |     """Declarative description of a tool's interface and characteristics."""
 33 | 
 34 |     name: str
 35 |     description: str
 36 |     parameters: Dict[str, Any] = field(default_factory=dict)
 37 |     category: str = ""
 38 |     cost_estimate: float = 0.0
 39 |     latency_estimate: float = 0.0
 40 |     requires_confirmation: bool = False
 41 |     timeout_seconds: float = 30.0
 42 |     required_capabilities: List[str] = field(default_factory=list)
 43 |     metadata: Dict[str, Any] = field(default_factory=dict)
 44 | 
 45 | 
 46 | # ---------------------------------------------------------------------------
 47 | # BaseTool ABC
 48 | # ---------------------------------------------------------------------------
 49 | 
 50 | 
 51 | class BaseTool(ABC):
 52 |     """Base class for all tool implementations.
 53 | 
 54 |     Subclasses must be registered via
 55 |     ``@ToolRegistry.register("name")`` to become discoverable.
 56 |     """
 57 | 
 58 |     tool_id: str
 59 |     is_local: bool = True
 60 | 
 61 |     @property
 62 |     @abstractmethod
 63 |     def spec(self) -> ToolSpec:
 64 |         """Return the tool specification."""
 65 | 
 66 |     @abstractmethod
 67 |     def execute(self, **params: Any) -> ToolResult:
 68 |         """Execute the tool with the given parameters."""
 69 | 
 70 |     def to_openai_function(self) -> Dict[str, Any]:
 71 |         """Convert to OpenAI function-calling format."""
 72 |         from openjarvis.tools.description_loader import (
 73 |             get_tool_description_override,
 74 |         )
 75 | 
 76 |         s = self.spec
 77 |         desc = get_tool_description_override(s.name) or s.description
 78 |         return {
 79 |             "type": "function",
 80 |             "function": {
 81 |                 "name": s.name,
 82 |                 "description": desc,
 83 |                 "parameters": s.parameters,
 84 |             },
 85 |         }
 86 | 
 87 | 
 88 | # ---------------------------------------------------------------------------
 89 | # ToolExecutor — dispatch engine for tool calls
 90 | # ---------------------------------------------------------------------------
 91 | 
 92 | 
 93 | 
 94 | # --- openjarvis-dispatch-log-v1 ---------------------------------------------------
 95 | # Tool-boundary dispatch record in its own rotating file, so a turn that
 96 | # dispatched NOTHING is distinguishable from one never instrumented.
 97 | CURRENT_TURN_ID: contextvars.ContextVar = contextvars.ContextVar(
 98 |     "openjarvis_turn_id", default="-"
 99 | )
100 | 
101 | # openjarvis-confirm-emit-v1 - lets a Callable[[str], bool] confirm callback learn
102 | # which confirm_id it is being asked about, without widening its signature.
103 | CURRENT_CONFIRM_ID = contextvars.ContextVar("openjarvis_confirm_id", default="")
104 | _dispatch_logger = None
105 | 
106 | 
107 | def _get_dispatch_logger():
108 |     global _dispatch_logger
109 |     if _dispatch_logger is not None:
110 |         return _dispatch_logger
111 |     lg = logging.getLogger("openjarvis.dispatch")
112 |     if not lg.handlers:
113 |         log_dir = os.path.join(
114 |             os.environ.get("LOCALAPPDATA", os.path.expanduser("~")),
115 |             "OpenJarvis", "logs",
116 |         )
117 |         try:
118 |             os.makedirs(log_dir, exist_ok=True)
119 |             h = logging.handlers.RotatingFileHandler(
120 |                 os.path.join(log_dir, "dispatch.log"),
121 |                 maxBytes=2 * 1024 * 1024, backupCount=4, encoding="utf-8",
122 |             )
123 |             h.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
124 |             lg.addHandler(h)
125 |         except Exception:
126 |             lg.addHandler(logging.NullHandler())
127 |     lg.setLevel(logging.INFO)
128 |     lg.propagate = False
129 |     _dispatch_logger = lg
130 |     return lg
131 | 
132 | 
133 | def _args_digest(rawargs, limit: int = 400) -> str:
134 |     try:
135 |         s = rawargs if isinstance(rawargs, str) else json.dumps(rawargs, default=str)
136 |     except Exception:
137 |         s = str(rawargs)
138 |     s = " ".join(s.split())
139 |     return s[:limit] + ("...TRUNC" if len(s) > limit else "")
140 | 
141 | 
142 | class ToolExecutor:
143 |     """Dispatch tool calls to registered tools with event bus integration.
144 | 
145 |     Parameters
146 |     ----------
147 |     tools:
148 |         List of tool instances to make available.
149 |     bus:
150 |         Optional event bus for publishing ``TOOL_CALL_START``/``TOOL_CALL_END``.
151 |     """
152 | 
153 |     def __init__(
154 |         self,
155 |         tools: List[BaseTool],
156 |         bus: Optional[EventBus] = None,
157 |         *,
158 |         interactive: bool = False,
159 |         confirm_callback: Optional[Callable[[str], bool]] = None,
160 |         default_timeout: float = 30.0,
161 |         capability_policy: Optional[Any] = None,
162 |         agent_id: str = "",
163 |         boundary_guard: Optional[Any] = None,
164 |     ) -> None:
165 |         self._tools: Dict[str, BaseTool] = {t.spec.name: t for t in tools}
166 |         self._bus = bus
167 |         self._interactive = interactive
168 |         self._confirm_callback = confirm_callback
169 |         self._default_timeout = default_timeout
170 |         self._capability_policy = capability_policy
171 |         self._agent_id = agent_id
172 |         self._boundary_guard = boundary_guard
173 | 
174 |     def execute(self, tool_call: ToolCall) -> ToolResult:
175 |         """Parse arguments, dispatch to tool, measure latency, emit events."""
176 |         _get_dispatch_logger().info(
177 |             "ATTEMPT turn=%s tool=%s args=%s thread=%s",
178 |             CURRENT_TURN_ID.get(), tool_call.name,
179 |             _args_digest(tool_call.arguments),
180 |             threading.current_thread().name,
181 |         )
182 |         tool = self._tools.get(tool_call.name)
183 |         if tool is None:
184 |             return ToolResult(
185 |                 tool_name=tool_call.name,
186 |                 content=f"Unknown tool: {tool_call.name}",
187 |                 success=False,
188 |             )
189 | 
190 |         # Parse arguments
191 |         try:
192 |             params = json.loads(tool_call.arguments) if tool_call.arguments else {}
193 |         except json.JSONDecodeError as exc:
194 |             return ToolResult(
195 |                 tool_name=tool_call.name,
196 |                 content=f"Invalid arguments JSON: {exc}",
197 |                 success=False,
198 |             )
199 | 
200 |         # Boundary guard: scan external tool arguments
201 |         if self._boundary_guard is not None and not getattr(tool, "is_local", True):
202 |             try:
203 |                 tool_call = self._boundary_guard.check_outbound(tool_call)
204 |                 # Re-parse arguments after potential redaction
205 |                 params = json.loads(tool_call.arguments) if tool_call.arguments else {}
206 |             except Exception as exc:
207 |                 return ToolResult(
208 |                     tool_name=tool_call.name,
209 |                     content=f"Security block: {exc}",
210 |                     success=False,
211 |                 )
212 | 
213 |         # RBAC capability check
214 |         if self._capability_policy and tool.spec.required_capabilities:
215 |             for cap in tool.spec.required_capabilities:
216 |                 if not self._capability_policy.check(
217 |                     self._agent_id,
218 |                     cap,
219 |                     tool_call.name,
220 |                 ):
221 |                     if self._bus:
222 |                         self._bus.publish(
223 |                             EventType.CAPABILITY_DENIED,
224 |                             {
225 |                                 "agent_id": self._agent_id,
226 |                                 "capability": cap,
227 |                                 "tool": tool_call.name,
228 |                             },
229 |                         )
230 |                     return ToolResult(
231 |                         tool_name=tool_call.name,
232 |                         content=(
233 |                             f"Capability '{cap}' denied for"
234 |                             f" agent '{self._agent_id}'"
235 |                             f" on tool '{tool_call.name}'."
236 |                         ),
237 |                         success=False,
238 |                     )
239 | 
240 |         # Taint checking (sink policy)
241 |         taint_set = params.get("_taint") if isinstance(params, dict) else None
242 |         if taint_set is not None:
243 |             try:
244 |                 from openjarvis.security.taint import TaintSet, check_taint
245 | 
246 |                 if isinstance(taint_set, TaintSet):
247 |                     violation = check_taint(tool_call.name, taint_set)
248 |                     if violation:
249 |                         if self._bus:
250 |                             self._bus.publish(
251 |                                 EventType.TAINT_VIOLATION,
252 |                                 {
253 |                                     "tool": tool_call.name,
254 |                                     "violation": violation,
255 |                                 },
256 |                             )
257 |                         return ToolResult(
258 |                             tool_name=tool_call.name,
259 |                             content=f"Taint violation: {violation}",
260 |                             success=False,
261 |                         )
262 |             except ImportError:
263 |                 pass
264 |             # Remove internal taint key before passing to tool
265 |             if isinstance(params, dict):
266 |                 params.pop("_taint", None)
267 | 
268 |         # Confirmation check for sensitive tools
269 |         if tool.spec.requires_confirmation:
270 |             if not self._interactive or self._confirm_callback is None:
271 |                 return ToolResult(
272 |                     tool_name=tool_call.name,
273 |                     content=(
274 |                         f"Tool '{tool_call.name}' requires"
275 |                         " confirmation but no confirmation"
276 |                         " callback is available."
277 |                     ),
278 |                     success=False,
279 |                 )
280 |             # openjarvis-confirm-emit-v1 - Defect 6 / 6c step 3
281 |             from openjarvis.core import confirm_registry as _cr
282 | 
283 |             _digest = _args_digest(tool_call.arguments)
284 |             prompt = (
285 |                 f"Allow execution of tool '{tool_call.name}' "
286 |                 f"with args {_digest}?"
287 |             )
288 |             _cid = _cr.register(
289 |                 tool=tool_call.name,
290 |                 agent_id=self._agent_id,
291 |                 turn_id=CURRENT_TURN_ID.get(),
292 |             )
293 |             _entry = _cr.get(_cid) or {}
294 |             if self._bus:
295 |                 self._bus.publish(
296 |                     EventType.TOOL_CONFIRM_REQUEST,
297 |                     {
298 |                         "confirm_id": _cid,
299 |                         "agent_id": self._agent_id,
300 |                         "turn_id": CURRENT_TURN_ID.get(),
301 |                         "tool": tool_call.name,
302 |                         "args_digest": _digest,
303 |                         "prompt": prompt,
304 |                         "expires_at": _entry.get("expires_at"),
305 |                     },
306 |                 )
307 |             _token = CURRENT_CONFIRM_ID.set(_cid)
308 |             try:
309 |                 _approved = self._confirm_callback(prompt)
310 |             finally:
311 |                 CURRENT_CONFIRM_ID.reset(_token)
312 |             # openjarvis-confirm-resolved-v1
313 |             _resolved = _cr.get(_cid) or {}
314 |             _decision = _resolved.get("decision") or (
315 |                 _cr.APPROVED if _approved else _cr.TIMEOUT
316 |             )
317 |             if self._bus:
318 |                 self._bus.publish(
319 |                     EventType.TOOL_CONFIRM_RESOLVED,
320 |                     {
321 |                         "confirm_id": _cid,
322 |                         "agent_id": self._agent_id,
323 |                         "turn_id": CURRENT_TURN_ID.get(),
324 |                         "tool": tool_call.name,
325 |                         "decision": _decision,
326 |                         "state": _resolved.get("state"),
327 |                         "created_at": _resolved.get("created_at"),
328 |                         "expires_at": _resolved.get("expires_at"),
329 |                         "reaped": not _resolved,
330 |                     },
331 |                 )
332 |             if not _approved:
333 |                 _final = (_cr.get(_cid) or {}).get("decision")
334 |                 if _final == _cr.DENIED:
335 |                     _content = (
336 |                         f"Tool '{tool_call.name}' execution denied by user."
337 |                     )
338 |                 elif _final == _cr.APPROVED:
339 |                     _content = (
340 |                         f"Tool '{tool_call.name}' was approved but the "
341 |                         "confirmation callback returned False. The tool did "
342 |                         "NOT run. Report this as an internal error, not as a "
343 |                         "refusal."
344 |                     )
345 |                 else:
346 |                     _content = (
347 |                         f"Tool '{tool_call.name}' was NOT executed because no "
348 |                         "confirmation answer arrived before the request "
349 |                         "expired. This is a TIMEOUT, not a refusal - the user "
350 |                         "did not deny it. Ask the user again rather than "
351 |                         "reporting that permission was refused."
352 |                     )
353 |                 return ToolResult(
354 |                     tool_name=tool_call.name,
355 |                     content=_content,
356 |                     success=False,
357 |                 )
358 | 
359 |         # Emit start event
360 |         if self._bus:
361 |             self._bus.publish(
362 |                 EventType.TOOL_CALL_START,
363 |                 {"tool": tool_call.name, "arguments": params},
364 |             )
365 | 
366 |         # Execute with timeout
367 |         timeout = tool.spec.timeout_seconds or self._default_timeout
368 |         t0 = time.time()
369 |         try:
370 |             with concurrent.futures.ThreadPoolExecutor(max_workers=1) as pool:
371 |                 future = pool.submit(tool.execute, **params)
372 |                 result = future.result(timeout=timeout)
373 |         except concurrent.futures.TimeoutError:
374 |             if self._bus:
375 |                 self._bus.publish(
376 |                     EventType.TOOL_TIMEOUT,
377 |                     {"tool": tool_call.name, "timeout": timeout},
378 |                 )
379 |             # openjarvis-tool-timeout-v1
380 |             result = ToolResult(
381 |                 tool_name=tool_call.name,
382 |                 content=(
383 |                     f"Tool '{tool_call.name}' exceeded its {timeout:.0f}s wait. "
384 |                     "OUTCOME UNKNOWN: the operation was NOT cancelled and may have "
385 |                     "completed successfully. Do NOT retry it and do NOT report it "
386 |                     "as failed. Verify the current state with a read-only check "
387 |                     "first, then report what the verification found."
388 |                 ),
389 |                 success=False,
390 |             )
391 |             result.metadata["timed_out"] = True
392 |             result.metadata["outcome_verified"] = False
393 |         except Exception as exc:
394 |             result = ToolResult(
395 |                 tool_name=tool_call.name,
396 |                 content=f"Tool execution error: {exc}",
397 |                 success=False,
398 |             )
399 |         latency = time.time() - t0
400 |         result.latency_seconds = latency
401 |         result.metadata["arguments"] = params
402 | 
403 |         # Auto-detect taints in results
404 |         if result.success:
405 |             try:
406 |                 from openjarvis.security.taint import auto_detect_taint
407 | 
408 |                 detected = auto_detect_taint(result.content)
409 |                 if detected and detected.labels:
410 |                     result.metadata["_taint"] = detected
411 |             except ImportError:
412 |                 pass
413 | 
414 |         # Emit end event
415 |         if self._bus:
416 |             result_text = str(result.content)[:10240] if result.content else ""
417 |             # Pass through ToolResult.metadata so downstream consumers
418 |             # (TraceCollector → TraceStep.metadata → SkillOptimizer) can
419 |             # see skill-tagged invocations.  Filter to JSON-serializable
420 |             # values only — internal objects like TaintSet (added by the
421 |             # taint auto-detect above) must not leak to event subscribers
422 |             # since the trace store will JSON-serialize them later.
423 |             event_metadata = self._json_safe_metadata(result.metadata)
424 |             self._bus.publish(
425 |                 EventType.TOOL_CALL_END,
426 |                 {
427 |                     "tool": tool_call.name,
428 |                     "success": result.success,
429 |                     "latency": latency,
430 |                     "result": result_text,
431 |                     "metadata": event_metadata,
432 |                 },
433 |             )
434 | 
435 |         _get_dispatch_logger().info(
436 |             "OUTCOME turn=%s tool=%s success=%s latency=%.3f timed_out=%s",
437 |             CURRENT_TURN_ID.get(), tool_call.name, result.success,
438 |             latency, bool(result.metadata.get("timed_out")),
439 |         )
440 |         return result
441 | 
442 |     @staticmethod
443 |     def _json_safe_metadata(metadata: Optional[Dict[str, Any]]) -> Dict[str, Any]:
444 |         """Return a copy of *metadata* containing only JSON-serializable values.
445 | 
446 |         ``ToolExecutor`` annotates ``ToolResult.metadata`` with internal
447 |         objects (currently ``_taint: TaintSet``).  Those are useful for
448 |         in-process security checks but cannot be serialized when the
449 |         ``TraceCollector`` writes ``TraceStep.metadata`` to JSON in the
450 |         SQLite trace store.  This helper drops any keys whose value is
451 |         not JSON-safe — silently, since the missing data is not
452 |         load-bearing for downstream consumers.
453 |         """
454 |         if not metadata:
455 |             return {}
456 | 
457 |         import json
458 | 
459 |         safe: Dict[str, Any] = {}
460 |         for key, value in metadata.items():
461 |             if not isinstance(key, str):
462 |                 continue
463 |             try:
464 |                 json.dumps(value)
465 |             except (TypeError, ValueError):
466 |                 # Skip non-serializable values (e.g. TaintSet)
467 |                 continue
468 |             safe[key] = value
469 |         return safe
470 | 
471 |     def available_tools(self) -> List[ToolSpec]:
472 |         """Return specs for all available tools."""
473 |         return [t.spec for t in self._tools.values()]
474 | 
475 |     def get_openai_tools(self) -> List[Dict[str, Any]]:
476 |         """Return tools in OpenAI function-calling format."""
477 |         return [t.to_openai_function() for t in self._tools.values()]
478 | 
479 | 
480 | def build_tool_descriptions(
481 |     tools: List[BaseTool],
482 |     *,
483 |     include_category: bool = True,
484 |     include_cost: bool = False,
485 | ) -> str:
486 |     """Build rich text descriptions from a list of tools.
487 | 
488 |     This is the single source of truth for all text-based agents that need
489 |     to describe available tools in their system prompts.
490 | 
491 |     Parameters
492 |     ----------
493 |     tools:
494 |         List of tool instances.
495 |     include_category:
496 |         Whether to include the ``Category:`` line.
497 |     include_cost:
498 |         Whether to include ``Cost estimate:`` and ``Latency estimate:`` lines.
499 | 
500 |     Returns
501 |     -------
502 |     str
503 |         Formatted multi-tool description, or ``"No tools available."`` if
504 |         *tools* is empty.
505 |     """
506 |     if not tools:
507 |         return "No tools available."
508 | 
509 |     from openjarvis.tools.description_loader import (
510 |         get_tool_description_override,
511 |     )
512 | 
513 |     sections: list[str] = []
514 |     for t in tools:
515 |         s = t.spec
516 |         desc = get_tool_description_override(s.name) or s.description
517 |         lines = [f"### {s.name}", desc]
518 | 
519 |         if include_category and s.category:
520 |             lines.append(f"Category: {s.category}")
521 | 
522 |         if include_cost:
523 |             if s.cost_estimate:
524 |                 lines.append(f"Cost estimate: ${s.cost_estimate:.4f}")
525 |             if s.latency_estimate:
526 |                 lines.append(f"Latency estimate: {s.latency_estimate:.1f}s")
527 | 
528 |         # Parameter descriptions
529 |         props = s.parameters.get("properties", {})
530 |         required = set(s.parameters.get("required", []))
531 |         if props:
532 |             lines.append("Parameters:")
533 |             for pname, pinfo in props.items():
534 |                 ptype = pinfo.get("type", "any")
535 |                 req_mark = ", required" if pname in required else ""
536 |                 desc = pinfo.get("description", "")
537 |                 if desc:
538 |                     lines.append(f"  - {pname} ({ptype}{req_mark}): {desc}")
539 |                 else:
540 |                     lines.append(f"  - {pname} ({ptype}{req_mark})")
541 | 
542 |         sections.append("\n".join(lines))
543 | 
544 |     return "\n\n".join(sections)
545 | 
546 | 
547 | __all__ = ["BaseTool", "ToolExecutor", "ToolSpec", "build_tool_descriptions"]
```

---

## FILE: `src/openjarvis/agents/native_openhands.py`

- bytes: 25611
- lines: 660
- sha256: `ECA4D84D79CD834E54B5A79FA2FE6784ED1AE1397BC8B93B14AACACE386E304E`
- line terminator: LF

Line numbers below are 1-based and authoritative. Cite them.

```python
  1 | """NativeOpenHandsAgent -- code-execution-centric agent.
  2 | 
  3 | Renamed from ``OpenHandsAgent`` to clarify this is OpenJarvis's native
  4 | CodeAct-style implementation.  The ``OpenHandsAgent`` name is now used
  5 | for the real openhands-sdk integration in ``openhands.py``.
  6 | """
  7 | 
  8 | from __future__ import annotations
  9 | 
 10 | import json as _json
 11 | import re
 12 | from typing import Any, List, Optional
 13 | 
 14 | from openjarvis.agents._stubs import AgentContext, AgentResult, ToolUsingAgent
 15 | from openjarvis.agents.prompt_loader import (
 16 |     load_few_shot_exemplars,
 17 |     load_system_prompt_override,
 18 | )
 19 | from openjarvis.core.events import EventBus
 20 | from openjarvis.core.registry import AgentRegistry
 21 | from openjarvis.core.types import Message, Role, ToolCall, ToolResult
 22 | from openjarvis.engine._stubs import InferenceEngine
 23 | from openjarvis.tools._stubs import BaseTool, build_tool_descriptions
 24 | 
 25 | OPENHANDS_SYSTEM_PROMPT = (  # noqa: E501
 26 |     "You are an AI assistant with access to tools. "
 27 |     "You MUST use tools when they would help answer "
 28 |     "the user's question.\n\n"
 29 |     "## How to use tools\n\n"
 30 |     "To call a tool, write on its own lines:\n\n"
 31 |     "Action: <tool_name>\n"
 32 |     "Action Input: <json_arguments>\n\n"
 33 |     "You will receive the result, then continue your "
 34 |     "response.\n\n"
 35 |     "## Available tools\n\n"
 36 |     "{tool_descriptions}\n\n"
 37 |     "## Important rules\n\n"
 38 |     "- When the user asks you to look up, search, fetch, "
 39 |     "or summarize a URL or topic, you MUST use web_search. "
 40 |     "Do NOT say you cannot browse the web.\n"
 41 |     "- When the user provides a URL, pass the FULL URL "
 42 |     "(including https://) as the query to web_search. "
 43 |     "Do NOT rewrite URLs into search keywords.\n"
 44 |     "- When the user asks a math question, use calculator.\n"
 45 |     "- When the user asks to read a file, use file_read.\n"
 46 |     "- You CAN write Python code in ```python blocks and "
 47 |     "it will be executed. Use this for computation, data "
 48 |     "processing, or when no specific tool fits.\n"
 49 |     "- If no tool or code is needed, respond directly "
 50 |     "with your answer.\n"
 51 |     "- Do NOT include <think> tags or internal reasoning "
 52 |     "in your response. Respond directly."
 53 | )
 54 | 
 55 | 
 56 | @AgentRegistry.register("native_openhands")
 57 | class NativeOpenHandsAgent(ToolUsingAgent):
 58 |     """Native CodeAct agent -- generates and executes Python code."""
 59 | 
 60 |     agent_id = "native_openhands"
 61 |     _default_temperature = 0.7
 62 |     _default_max_tokens = 2048
 63 |     _default_max_turns = 3
 64 | 
 65 |     def __init__(
 66 |         self,
 67 |         engine: InferenceEngine,
 68 |         model: str,
 69 |         *,
 70 |         tools: Optional[List[BaseTool]] = None,
 71 |         bus: Optional[EventBus] = None,
 72 |         max_turns: Optional[int] = None,
 73 |         temperature: Optional[float] = None,
 74 |         max_tokens: Optional[int] = None,
 75 |         interactive: bool = False,
 76 |         confirm_callback=None,
 77 |     ) -> None:
 78 |         super().__init__(
 79 |             engine,
 80 |             model,
 81 |             tools=tools,
 82 |             bus=bus,
 83 |             max_turns=max_turns,
 84 |             temperature=temperature,
 85 |             max_tokens=max_tokens,
 86 |             interactive=interactive,
 87 |             confirm_callback=confirm_callback,
 88 |         )
 89 | 
 90 |     @staticmethod
 91 |     def _expand_urls(text: str) -> tuple[str, bool]:
 92 |         """If the user message contains a URL, fetch it and inline the content.
 93 | 
 94 |         Returns (possibly_expanded_text, was_expanded).
 95 |         """
 96 |         import re as _re
 97 | 
 98 |         url_match = _re.search(r"https?://[^\s,;\"'<>]+", text)
 99 |         if not url_match:
100 |             return text, False
101 |         url = url_match.group(0).rstrip(".,;)")
102 |         try:
103 |             from openjarvis.tools.web_search import WebSearchTool
104 | 
105 |             content = WebSearchTool._fetch_url(url, max_chars=4000)
106 |             header = f"\n\n--- Content from {url} ---\n"
107 |             footer = "\n--- End of content ---\n"
108 |             expanded = text.replace(url, f"{header}{content}{footer}")
109 |             return expanded, True
110 |         except Exception:
111 |             return text, False
112 | 
113 |     def _truncate_if_needed(
114 |         self,
115 |         messages: list[Message],
116 |         max_prompt_tokens: int = 3000,
117 |     ) -> list[Message]:
118 |         """Truncate messages if estimated token count exceeds limit."""
119 |         total_chars = sum(len(m.content) for m in messages)
120 |         estimated_tokens = total_chars // 4
121 |         if estimated_tokens <= max_prompt_tokens:
122 |             return messages
123 |         # Find the last user message and truncate its content
124 |         for i in range(len(messages) - 1, -1, -1):
125 |             if messages[i].role == Role.USER:
126 |                 excess_tokens = estimated_tokens - max_prompt_tokens
127 |                 excess_chars = excess_tokens * 4
128 |                 original = messages[i].content
129 |                 if len(original) > excess_chars + 200:
130 |                     truncated = original[: len(original) - excess_chars]
131 |                     messages[i] = Message(
132 |                         role=Role.USER,
133 |                         content=(
134 |                             truncated + "\n\n[Input truncated to fit context window]"
135 |                         ),
136 |                     )
137 |                 break
138 |         return messages
139 | 
140 |     @staticmethod
141 |     def _strip_tool_call_text(text: str) -> str:
142 |         """Remove raw tool call artifacts from final output."""
143 |         # Remove Action: ... Action Input: ... blocks
144 |         text = re.sub(
145 |             r"Action:\s*.+?(?:Action Input:\s*.+?)?(?=\n\n|\Z)",
146 |             "",
147 |             text,
148 |             flags=re.DOTALL | re.IGNORECASE,
149 |         )
150 |         # Remove <tool_call>...</tool_call> or </tool_name> blocks
151 |         text = re.sub(r"<tool_call>.*?</\w+>", "", text, flags=re.DOTALL)
152 |         return text.strip()
153 | 
154 |     def _extract_code(self, text: str) -> str | None:
155 |         """Extract Python code from markdown code blocks."""
156 |         match = re.search(r"```python\n(.*?)```", text, re.DOTALL)
157 |         if match:
158 |             return match.group(1).strip()
159 |         return None
160 | 
161 |     def _extract_tool_call(self, text: str) -> tuple[str, str] | None:
162 |         """Extract tool call from structured output.
163 | 
164 |         Supports two formats:
165 |         1. Action: tool_name / Action Input: {"key": "value"}
166 |         2. <tool_call>tool_name\\n$key=value</tool_call> (XML-style)
167 |         """
168 |         # Format 1: Action / Action Input
169 |         action_match = re.search(r"Action:\s*(.+)", text, re.IGNORECASE)
170 |         input_match = re.search(
171 |             r"Action Input:\s*(.+?)(?=\n\n|\Z)", text, re.DOTALL | re.IGNORECASE
172 |         )
173 |         if action_match:
174 |             return (
175 |                 action_match.group(1).strip(),
176 |                 input_match.group(1).strip() if input_match else "{}",
177 |             )
178 | 
179 |         # Format 2: <tool_call>tool_name ... </tool_call> or </tool_name>
180 |         xml_match = re.search(
181 |             r"<tool_call>\s*(\w+)\s*(.*?)</\w+>",
182 |             text,
183 |             re.DOTALL,
184 |         )
185 |         if xml_match:
186 |             tool_name = xml_match.group(1).strip()
187 |             raw_params = xml_match.group(2).strip()
188 |             # Parse $key=value or <key>value</key> params into JSON
189 |             params: dict[str, Any] = {}
190 |             # $key=value format
191 |             pat = r"\$(\w+)=(.+?)(?=\$|\n<|</|$)"
192 |             for m in re.finditer(pat, raw_params, re.DOTALL):
193 |                 params[m.group(1)] = m.group(2).strip().rstrip("</>\n")
194 |             # <key>value</key> format
195 |             for m in re.finditer(r"<(\w+)>(.*?)</\1>", raw_params, re.DOTALL):
196 |                 key, val = m.group(1), m.group(2).strip()
197 |                 # Try to parse as int
198 |                 try:
199 |                     params[key] = int(val)
200 |                 except ValueError:
201 |                     params[key] = val
202 |             # key: value format (common in GLM models)
203 |             if not params:
204 |                 for m in re.finditer(
205 |                     r"(\w+)\s*:\s*(.+?)(?=\n\w+\s*:|$)", raw_params, re.DOTALL
206 |                 ):
207 |                     key, val = m.group(1), m.group(2).strip().strip("\"'")
208 |                     try:
209 |                         params[key] = int(val)
210 |                     except ValueError:
211 |                         params[key] = val
212 |             if params:
213 |                 return (tool_name, _json.dumps(params))
214 |             return (tool_name, "{}")
215 | 
216 |         # Format 4: OpenHands XML tool call
217 |         # <function=NAME><parameter=KEY>value</parameter></function>
218 |         # Emitted as content by qwen3-coder when native tool_calls do not fire.
219 |         # \s*=\s* and the \Z fallbacks tolerate the malformed spacing and
220 |         # missing closing tags observed in the wild, so the call executes
221 |         # instead of leaking backend syntax into the chat.
222 |         fn_match = re.search(
223 |             r"<function\s*=\s*[\"\']?([\w.\-]+)[\"\']?\s*>(.*?)(?:</function>|\Z)",
224 |             text,
225 |             re.DOTALL,
226 |         )
227 |         if fn_match:
228 |             fn_name = fn_match.group(1).strip()
229 |             fn_params: dict[str, Any] = {}
230 |             for _pm in re.finditer(
231 |                 r"<parameter\s*=\s*[\"\']?([\w.\-]+)[\"\']?\s*>(.*?)(?:</parameter>|\Z)",
232 |                 fn_match.group(2),
233 |                 re.DOTALL,
234 |             ):
235 |                 _val = _pm.group(2).strip()
236 |                 try:
237 |                     fn_params[_pm.group(1)] = int(_val)
238 |                 except ValueError:
239 |                     fn_params[_pm.group(1)] = _val
240 |             return (fn_name, _json.dumps(fn_params))
241 | 
242 |         # Format 3: bare JSON tool call {"name": "...", "arguments": {...}}
243 |         # Some Ollama models (notably qwen2.5-coder) emit tool calls as JSON
244 |         # in content instead of the structured tool_calls field. Catch it here
245 |         # so the call executes instead of leaking raw JSON into the chat.
246 |         json_call = self._extract_json_tool_call(text)
247 |         if json_call is not None:
248 |             return json_call
249 | 
250 |         return None
251 | 
252 |     def _extract_json_tool_call(self, text):
253 |         """Extract a bare JSON tool call: {"name": "...", "arguments": {...}}.
254 | 
255 |         Fires only on a real tool-call shape (a string ``name``/``tool`` plus an
256 |         ``arguments``/``parameters``/``input`` key), so ordinary JSON in a normal
257 |         answer is left untouched. Scans for the first balanced, string-aware
258 |         JSON object in the text.
259 |         """
260 |         known = set()
261 |         for _t in (self._tools or []):
262 |             _n = getattr(_t, "name", None) or getattr(_t, "tool_id", None)
263 |             if _n:
264 |                 known.add(str(_n))
265 |         start = text.find("{")
266 |         while start != -1:
267 |             depth = 0
268 |             in_str = False
269 |             esc = False
270 |             for j in range(start, len(text)):
271 |                 ch = text[j]
272 |                 if in_str:
273 |                     if esc:
274 |                         esc = False
275 |                     elif ch == chr(92):  # backslash
276 |                         esc = True
277 |                     elif ch == '"':
278 |                         in_str = False
279 |                     continue
280 |                 if ch == '"':
281 |                     in_str = True
282 |                 elif ch == "{":
283 |                     depth += 1
284 |                 elif ch == "}":
285 |                     depth -= 1
286 |                     if depth == 0:
287 |                         candidate = text[start:j + 1]
288 |                         try:
289 |                             obj = _json.loads(candidate)
290 |                         except Exception:
291 |                             obj = None
292 |                         if isinstance(obj, dict):
293 |                             name = obj.get("name") or obj.get("tool")
294 |                             has_args = (
295 |                                 "arguments" in obj
296 |                                 or "parameters" in obj
297 |                                 or "input" in obj
298 |                             )
299 |                             if isinstance(name, str) and name and (has_args or name in known):
300 |                                 if "arguments" in obj:
301 |                                     args = obj.get("arguments")
302 |                                 elif "parameters" in obj:
303 |                                     args = obj.get("parameters")
304 |                                 else:
305 |                                     args = obj.get("input", {})
306 |                                 if isinstance(args, str):
307 |                                     args_json = args
308 |                                 else:
309 |                                     args_json = _json.dumps(args or {})
310 |                                 return (name, args_json)
311 |                         break
312 |             start = text.find("{", start + 1)
313 |         return None
314 | 
315 |     def run(
316 |         self,
317 |         input: str,
318 |         context: Optional[AgentContext] = None,
319 |         **kwargs: Any,
320 |     ) -> AgentResult:
321 |         self._emit_turn_start(input)
322 |         _oj_run_id = _oj_run_start(self, context, input)
323 | 
324 |         tool_descriptions = build_tool_descriptions(self._tools)
325 |         prompt_template = (
326 |             load_system_prompt_override("native_openhands") or OPENHANDS_SYSTEM_PROMPT
327 |         )
328 |         system_prompt = prompt_template.format(
329 |             tool_descriptions=tool_descriptions,
330 |         )
331 | 
332 |         # Pre-fetch any URLs in the input so the LLM gets the content directly
333 |         input, url_expanded = self._expand_urls(input)
334 | 
335 |         # If URL content was inlined, skip the tool loop -- just summarize directly
336 |         if url_expanded:
337 |             direct_messages: list[Message] = [
338 |                 Message(
339 |                     role=Role.SYSTEM,
340 |                     content=(
341 |                         "You are a helpful assistant. "
342 |                         "Respond directly to the user's "
343 |                         "request using the provided content."
344 |                         " Do NOT include <think> tags."
345 |                     ),
346 |                 ),
347 |                 Message(role=Role.USER, content=input),
348 |             ]
349 |             direct_messages = self._truncate_if_needed(direct_messages)
350 |             try:
351 |                 result = self._generate(direct_messages)
352 |             except Exception:
353 |                 # Propagate to the eval runner / server bridge so the failure
354 |                 # is recorded as an error instead of a fake "input too long"
355 |                 # answer that silently scores as 0%. Telemetry boundary is
356 |                 # still emitted before re-raising.
357 |                 self._emit_turn_end(turns=1, error=True)
358 |                 raise
359 |             content = self._strip_think_tags(result.get("content", ""))
360 |             usage = result.get("usage", {})
361 |             _oj_run_end(_oj_run_id, "urldirect", 1, [], content)
362 |             self._emit_turn_end(turns=1)
363 |             return AgentResult(
364 |                 content=content,
365 |                 tool_results=[],
366 |                 turns=1,
367 |                 metadata={
368 |                     "prompt_tokens": usage.get("prompt_tokens", 0),
369 |                     "completion_tokens": usage.get("completion_tokens", 0),
370 |                     "total_tokens": usage.get("total_tokens", 0),
371 |                 },
372 |             )
373 | 
374 |         messages = self._build_messages(input, context, system_prompt=system_prompt)
375 | 
376 |         # Inject few-shot exemplars before the user input
377 |         for ex in load_few_shot_exemplars("native_openhands"):
378 |             if ex.get("input") and ex.get("output"):
379 |                 messages.insert(-1, Message(role=Role.USER, content=ex["input"]))
380 |                 messages.insert(-1, Message(role=Role.ASSISTANT, content=ex["output"]))
381 | 
382 |         messages = self._truncate_if_needed(messages)
383 | 
384 |         all_tool_results: list[ToolResult] = []
385 |         turns = 0
386 |         last_content = ""
387 |         total_usage = {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0}
388 | 
389 |         # Build OpenAI-format tool schemas for native function calling
390 |         openai_tools = self._executor.get_openai_tools() if self._tools else []
391 |         # Side dict for Gemini thought_signatures (ToolCall uses slots)
392 |         _thought_sigs: dict[str, bytes] = {}
393 | 
394 |         for _turn in range(self._max_turns):
395 |             turns += 1
396 |             _oj_turn_id = _oj_set_turn(_oj_run_id, turns)
397 |             # Truncate before every generate call -- tool results may have
398 |             # expanded the context beyond what the model supports.
399 |             messages = self._truncate_if_needed(messages)
400 | 
401 |             gen_kwargs: dict[str, Any] = {}
402 |             if openai_tools:
403 |                 gen_kwargs["tools"] = openai_tools
404 | 
405 |             try:
406 |                 result = self._generate(messages, **gen_kwargs)
407 |             except Exception:
408 |                 # Propagate so the eval runner records a real error rather
409 |                 # than a fake "input too long" string that silently scores 0.
410 |                 self._emit_turn_end(turns=turns, error=True)
411 |                 raise
412 | 
413 |             # Accumulate usage from this generate call
414 |             usage = result.get("usage", {})
415 |             for k in total_usage:
416 |                 total_usage[k] += usage.get(k, 0)
417 | 
418 |             content = result.get("content", "")
419 |             _oj_raw = content
420 |             # Strip think tags so they don't interfere with parsing
421 |             content = self._strip_think_tags(content)
422 |             last_content = content
423 | 
424 |             # --- Native function-calling path (OpenAI, Anthropic, etc.) ---
425 |             raw_tool_calls = result.get("tool_calls", [])
426 |             _oj_raw_gen(_oj_run_id, _oj_turn_id, _oj_raw, content, len(raw_tool_calls))
427 |             if raw_tool_calls:
428 |                 native_calls = []
429 |                 for i, tc in enumerate(raw_tool_calls):
430 |                     call = ToolCall(
431 |                         id=tc.get("id", f"call_{turns}_{i}"),
432 |                         name=tc.get("name", ""),
433 |                         arguments=tc.get("arguments", "{}"),
434 |                     )
435 |                     # Preserve thought_signature for Gemini reasoning
436 |                     sig = tc.get("thought_signature")
437 |                     if sig is not None:
438 |                         _thought_sigs[call.id] = sig
439 |                     native_calls.append(call)
440 |                 messages.append(
441 |                     Message(
442 |                         role=Role.ASSISTANT,
443 |                         content=content,
444 |                         tool_calls=native_calls,
445 |                     )
446 |                 )
447 |                 for tc in native_calls:
448 |                     tool_result = self._executor.execute(tc)
449 |                     all_tool_results.append(tool_result)
450 |                     obs_text = tool_result.content
451 |                     if len(obs_text) > 4000:
452 |                         obs_text = obs_text[:4000] + "\n\n[Output truncated]"
453 |                     messages.append(
454 |                         Message(
455 |                             role=Role.TOOL,
456 |                             content=obs_text,
457 |                             tool_call_id=tc.id,
458 |                             name=tc.name,
459 |                         )
460 |                     )
461 |                 continue
462 | 
463 |             # --- Text-based fallback (CodeAct / Action-Input format) ---
464 | 
465 |             # Try to extract code
466 |             code = self._extract_code(content)
467 |             if code:
468 |                 messages.append(Message(role=Role.ASSISTANT, content=content))
469 | 
470 |                 # Execute via code_interpreter tool if available
471 |                 tool_call = ToolCall(
472 |                     id=f"code_{turns}",
473 |                     name="code_interpreter",
474 |                     arguments=_json.dumps({"code": code}),
475 |                 )
476 |                 tool_result = self._executor.execute(tool_call)
477 |                 all_tool_results.append(tool_result)
478 | 
479 |                 obs_text = tool_result.content
480 |                 if len(obs_text) > 4000:
481 |                     obs_text = obs_text[:4000] + "\n\n[Output truncated]"
482 |                 observation = f"Output:\n{obs_text}"
483 |                 messages.append(Message(role=Role.USER, content=observation))
484 |                 continue
485 | 
486 |             # Try tool call
487 |             tool_info = self._extract_tool_call(content)
488 |             if tool_info:
489 |                 action, action_input = tool_info
490 |                 messages.append(Message(role=Role.ASSISTANT, content=content))
491 | 
492 |                 tool_call = ToolCall(
493 |                     id=f"tool_{turns}", name=action, arguments=action_input
494 |                 )
495 |                 tool_result = self._executor.execute(tool_call)
496 |                 all_tool_results.append(tool_result)
497 | 
498 |                 obs_text = tool_result.content
499 |                 if len(obs_text) > 4000:
500 |                     obs_text = obs_text[:4000] + "\n\n[Output truncated]"
501 |                 observation = f"Result: {obs_text}"
502 |                 messages.append(Message(role=Role.USER, content=observation))
503 |                 continue
504 | 
505 |             # No code or tool call -- this is the final answer
506 |             content = self._strip_think_tags(content)
507 |             content = self._strip_tool_call_text(content)
508 |             _oj_run_end(_oj_run_id, "final", turns, all_tool_results, content)
509 |             self._emit_turn_end(turns=turns)
510 |             return AgentResult(
511 |                 content=content,
512 |                 tool_results=all_tool_results,
513 |                 turns=turns,
514 |                 metadata=total_usage,
515 |             )
516 | 
517 |         # Max turns
518 |         final = self._strip_think_tags(last_content) or "Maximum turns reached."
519 |         final = self._strip_tool_call_text(final)
520 |         _oj_run_end(_oj_run_id, "maxturns", turns, all_tool_results, final)
521 |         result = self._max_turns_result(all_tool_results, turns, content=final)
522 |         result.metadata.update(total_usage)
523 |         return result
524 | 
525 | 
526 | 
527 | # --- openjarvis-agent-log-v1 -------------------------------------------------
528 | # Turn-boundary record in its own rotating file, so an agent turn that
529 | # dispatched NOTHING is distinguishable from one that was never instrumented.
530 | # Also sets tools._stubs.CURRENT_TURN_ID (a ContextVar) so dispatch.log lines
531 | # carry a real turn id.  Every call site is exception-swallowing on purpose:
532 | # instrumentation must never be able to break a run.
533 | _oj_agent_logger = None
534 | 
535 | 
536 | def _oj_get_agent_logger():
537 |     global _oj_agent_logger
538 |     if _oj_agent_logger is not None:
539 |         return _oj_agent_logger
540 |     import logging as _lgm
541 |     import logging.handlers as _lgh
542 |     import os as _os
543 | 
544 |     lg = _lgm.getLogger("openjarvis.agent")
545 |     if not lg.handlers:
546 |         log_dir = _os.path.join(
547 |             _os.environ.get("LOCALAPPDATA", _os.path.expanduser("~")),
548 |             "OpenJarvis", "logs",
549 |         )
550 |         try:
551 |             _os.makedirs(log_dir, exist_ok=True)
552 |             h = _lgh.RotatingFileHandler(
553 |                 _os.path.join(log_dir, "agent.log"),
554 |                 maxBytes=2621440, backupCount=4, encoding="utf-8",
555 |             )
556 |             h.setFormatter(_lgm.Formatter("%(asctime)s %(levelname)s %(message)s"))
557 |             lg.addHandler(h)
558 |         except Exception:
559 |             lg.addHandler(_lgm.NullHandler())
560 |     lg.setLevel(_lgm.INFO)
561 |     lg.propagate = False
562 |     _oj_agent_logger = lg
563 |     return lg
564 | 
565 | 
566 | def _oj_conv_id(context):
567 |     for attr in ("conversation_id", "session_id", "thread_id", "id"):
568 |         v = getattr(context, attr, None)
569 |         if v:
570 |             return str(v)
571 |     meta = getattr(context, "metadata", None)
572 |     if isinstance(meta, dict):
573 |         for k in ("conversation_id", "session_id", "thread_id"):
574 |             if meta.get(k):
575 |                 return str(meta[k])
576 |     return "-"
577 | 
578 | 
579 | def _oj_model_name(agent):
580 |     for attr in ("_model", "model", "_model_name"):
581 |         v = getattr(agent, attr, None)
582 |         if isinstance(v, str) and v:
583 |             return v
584 |     llm = getattr(agent, "_llm", None) or getattr(agent, "llm", None)
585 |     for attr in ("model", "model_name", "_model"):
586 |         v = getattr(llm, attr, None)
587 |         if isinstance(v, str) and v:
588 |             return v
589 |     return "-"
590 | 
591 | 
592 | def _oj_run_start(agent, context, input_text):
593 |     import uuid as _uuid
594 | 
595 |     run_id = _uuid.uuid4().hex[:8]
596 |     try:
597 |         _oj_get_agent_logger().info(
598 |             "RUNSTART run=%s agent=%s model=%s conv=%s tools=%d maxturns=%s chars=%d",
599 |             run_id,
600 |             type(agent).__name__,
601 |             _oj_model_name(agent),
602 |             _oj_conv_id(context),
603 |             len(getattr(agent, "_tools", []) or []),
604 |             getattr(agent, "_max_turns", "-"),
605 |             len(input_text or ""),
606 |         )
607 |     except Exception:
608 |         pass
609 |     return run_id
610 | 
611 | 
612 | def _oj_set_turn(run_id, turns):
613 |     turn_id = "%s-t%d" % (run_id, turns)
614 |     try:
615 |         from openjarvis.tools._stubs import CURRENT_TURN_ID as _cti
616 | 
617 |         _cti.set(turn_id)
618 |     except Exception:
619 |         pass
620 |     try:
621 |         _oj_get_agent_logger().info(
622 |             "TURN run=%s turn=%s n=%d", run_id, turn_id, turns
623 |         )
624 |     except Exception:
625 |         pass
626 |     return turn_id
627 | 
628 | 
629 | def _oj_run_end(run_id, kind, turns, tool_results, content):
630 |     try:
631 |         head = (content or "")[:160].replace("\n", " ").replace("\r", " ")
632 |         _oj_get_agent_logger().info(
633 |             "RUNEND run=%s exit=%s turns=%s dispatched=%d chars=%d head=%s",
634 |             run_id, kind, turns,
635 |             len(tool_results or []),
636 |             len(content or ""),
637 |             head,
638 |         )
639 |     except Exception:
640 |         pass
641 | 
642 | 
643 | # --- end openjarvis-agent-log-v1 ---------------------------------------------
644 | 
645 | 
646 | 
647 | 
648 | def _oj_raw_gen(run_id, turn_id, raw, stripped, n_tool_calls):
649 |     """openjarvis-raw-gen-v1 - log the pre-strip generation for one turn."""
650 |     try:
651 |         raw = raw or ""
652 |         stripped = stripped or ""
653 |         _oj_get_agent_logger().info(
654 |             "RAWGEN run=%s turn=%s rawlen=%d striplen=%d changed=%s ntc=%d raw=%s",
655 |             run_id, turn_id, len(raw), len(stripped),
656 |             (raw != stripped), n_tool_calls, repr(raw[:1500]),
657 |         )
658 |     except Exception:
659 |         pass
660 | __all__ = ["NativeOpenHandsAgent"]
```

---

# MANIFEST

| file | found | bytes | lines | sha256 |
|---|---|---|---|---|
| `src/openjarvis/agents/prompt_loader.py` | yes | 2669 | 83 | `A48EE0C8627FBD4B...` |
| `src/openjarvis/tools/_stubs.py` | yes | 21068 | 547 | `08B90B18308A4FB6...` |
| `src/openjarvis/agents/native_openhands.py` | yes | 25611 | 660 | `ECA4D84D79CD834E...` |

These hashes pin the exact bytes you reviewed. If a later patch is built against different bytes, the mismatch is detectable.

