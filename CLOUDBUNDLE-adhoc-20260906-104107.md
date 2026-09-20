# OPENJARVIS CODE REVIEW BUNDLE

- marker: `openjarvis-cloudbundle-v1`
- set: `adhoc` - ad hoc bundle
- generated: 2026-09-06T10:41:07
- repo root: `C:\Users\Admin\OpenJarvis`
- files in bundle: 6

You are reviewing complete source files. Every file is included in full, with authoritative 1-based line numbers in the left gutter. Nothing has been elided.

---

# THE QUESTION

TRUNCATION CHAIN AUDIT. In native_openhands.py, _truncate_if_needed (:113-138) is called on the production path at :382 and :399, once before the turn loop and once per turn. It sums total_chars across ALL messages including SYSTEM, compares estimated_tokens (chars//4) against a hardcoded max_prompt_tokens=3000, then scans BACKWARD for the last Role.USER message and cuts characters off the TAIL of its content. Tool results are appended as Role.TOOL (:455) and assistant turns as Role.ASSISTANT (:442,:468) - nothing appended inside the loop is Role.USER. Production SYSTEM prompt overhead is ~3980 tokens and num_ctx is 16384. Q1: trace exactly what _truncate_if_needed does on turn 3 of a real run where SYSTEM is ~3980 tokens, the user ask is ~200 chars, few-shot exemplars were inserted at :379-380 as Role.USER, and two Role.TOOL results of ~4000 chars each have accumulated. State whether the guard at :129 passes or fails, and whether the function modifies anything at all. Q2: the comment at :397-398 says truncation is needed because tool results expand context. Given the backward scan only matches Role.USER, can this function ever reduce Role.TOOL content? Q3: core/compression.py:47 handles Role.TOOL against TOOL_OUTPUT_MAX. Is that compressor reachable from native_openhands.py on any path, and if not, what calls it? Q4: if messages exceed num_ctx after _truncate_if_needed no-ops, where does the actual truncation happen - engine, ollama server, or nowhere - and does the SYSTEM message survive it? Q5: where does the 3000 constant come from, is it referenced or configurable anywhere else, and what was it presumably sized against? Answer each separately and cite file:line.

---

# SOURCE

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

## FILE: `src/openjarvis/agents/_stubs.py`

- bytes: 12689
- lines: 358
- sha256: `C9D7C461B96EE8682FD27D72AE1B8A4798480A9623E89688ABD29C67EF938505`
- line terminator: LF

Line numbers below are 1-based and authoritative. Cite them.

```python
  1 | """ABC for agent implementations.
  2 | 
  3 | Adapted from IPW's ``BaseAgent`` at ``src/agents/base.py``.
  4 | Provides ``BaseAgent`` with concrete helper methods for event emission,
  5 | message building, and generation, plus ``ToolUsingAgent`` intermediate
  6 | base for agents that accept tools.
  7 | """
  8 | 
  9 | from __future__ import annotations
 10 | 
 11 | import re
 12 | from abc import ABC, abstractmethod
 13 | from dataclasses import dataclass, field
 14 | from typing import Any, Dict, List, Optional
 15 | 
 16 | from openjarvis.core.config import load_config
 17 | from openjarvis.core.events import EventBus, EventType
 18 | from openjarvis.core.types import Conversation, Message, Role, ToolResult
 19 | from openjarvis.engine._stubs import InferenceEngine
 20 | 
 21 | 
 22 | @dataclass(slots=True)
 23 | class AgentContext:
 24 |     """Runtime context handed to an agent on each invocation."""
 25 | 
 26 |     conversation: Conversation = field(default_factory=Conversation)
 27 |     tools: List[str] = field(default_factory=list)
 28 |     memory_results: List[Any] = field(default_factory=list)
 29 |     metadata: Dict[str, Any] = field(default_factory=dict)
 30 | 
 31 | 
 32 | @dataclass(slots=True)
 33 | class AgentResult:
 34 |     """Result returned after an agent completes a run."""
 35 | 
 36 |     content: str
 37 |     tool_results: List[ToolResult] = field(default_factory=list)
 38 |     turns: int = 0
 39 |     metadata: Dict[str, Any] = field(default_factory=dict)
 40 | 
 41 | 
 42 | class BaseAgent(ABC):
 43 |     """Base class for all agent implementations.
 44 | 
 45 |     Subclasses must be registered via
 46 |     ``@AgentRegistry.register("name")`` to become discoverable.
 47 | 
 48 |     Provides concrete helper methods that eliminate boilerplate in
 49 |     subclasses:
 50 | 
 51 |     - :meth:`_emit_turn_start` / :meth:`_emit_turn_end` -- event bus
 52 |     - :meth:`_build_messages` -- conversation + system prompt assembly
 53 |     - :meth:`_generate` -- delegates to engine with stored defaults
 54 |     - :meth:`_max_turns_result` -- standard max-turns-exceeded result
 55 |     - :meth:`_strip_think_tags` -- remove ``<think>`` blocks
 56 |     """
 57 | 
 58 |     agent_id: str
 59 |     accepts_tools: bool = False
 60 | 
 61 |     def __init__(
 62 |         self,
 63 |         engine: InferenceEngine,
 64 |         model: str,
 65 |         *,
 66 |         bus: Optional[EventBus] = None,
 67 |         temperature: Optional[float] = None,
 68 |         max_tokens: Optional[int] = None,
 69 |         prompt_builder: Optional[Any] = None,
 70 |     ) -> None:
 71 |         self._engine = engine
 72 |         self._model = model
 73 |         self._bus = bus
 74 |         self._prompt_builder = prompt_builder
 75 | 
 76 |         # Three-tier resolution: explicit arg > config > class default > hardcoded
 77 |         if temperature is not None and max_tokens is not None:
 78 |             self._temperature = temperature
 79 |             self._max_tokens = max_tokens
 80 |         else:
 81 |             try:
 82 |                 cfg = load_config()
 83 |                 self._temperature = (
 84 |                     temperature
 85 |                     if temperature is not None
 86 |                     else cfg.intelligence.temperature
 87 |                 )
 88 |                 self._max_tokens = (
 89 |                     max_tokens
 90 |                     if max_tokens is not None
 91 |                     else cfg.intelligence.max_tokens
 92 |                 )
 93 |             except Exception:
 94 |                 self._temperature = (
 95 |                     temperature
 96 |                     if temperature is not None
 97 |                     else getattr(self, "_default_temperature", 0.7)
 98 |                 )
 99 |                 self._max_tokens = (
100 |                     max_tokens
101 |                     if max_tokens is not None
102 |                     else getattr(self, "_default_max_tokens", 1024)
103 |                 )
104 | 
105 |     # ------------------------------------------------------------------
106 |     # Concrete helpers
107 |     # ------------------------------------------------------------------
108 | 
109 |     def _emit_turn_start(self, input: str) -> None:
110 |         """Publish ``AGENT_TURN_START`` if an event bus is available."""
111 |         if self._bus:
112 |             self._bus.publish(
113 |                 EventType.AGENT_TURN_START,
114 |                 {"agent": self.agent_id, "input": input},
115 |             )
116 | 
117 |     def _emit_turn_end(self, **data: Any) -> None:
118 |         """Publish ``AGENT_TURN_END`` if an event bus is available."""
119 |         if self._bus:
120 |             payload: Dict[str, Any] = {"agent": self.agent_id}
121 |             payload.update(data)
122 |             self._bus.publish(EventType.AGENT_TURN_END, payload)
123 | 
124 |     def _build_messages(
125 |         self,
126 |         input: str,
127 |         context: Optional[AgentContext] = None,
128 |         *,
129 |         system_prompt: Optional[str] = None,
130 |     ) -> list[Message]:
131 |         """Assemble the message list for a generate call.
132 | 
133 |         Optionally prepends a system prompt, then appends any context
134 |         conversation messages, and finally the user input.
135 |         """
136 |         messages: list[Message] = []
137 |         # Check if the context already supplies a system message
138 |         _context_has_system = (
139 |             context
140 |             and context.conversation.messages
141 |             and any(m.role == Role.SYSTEM for m in context.conversation.messages)
142 |         )
143 | 
144 |         if self._prompt_builder is not None:
145 |             effective_system_prompt = self._prompt_builder.build()
146 |         elif system_prompt:
147 |             effective_system_prompt = system_prompt
148 |         elif _context_has_system:
149 |             effective_system_prompt = None
150 |         else:
151 |             # Fall back to the config-level default (grounds local models)
152 |             try:
153 |                 cfg = load_config()
154 |                 effective_system_prompt = cfg.agent.default_system_prompt or None
155 |             except Exception:
156 |                 effective_system_prompt = None
157 |         if effective_system_prompt:
158 |             messages.append(Message(role=Role.SYSTEM, content=effective_system_prompt))
159 |         if context and context.conversation.messages:
160 |             messages.extend(context.conversation.messages)
161 |         messages.append(Message(role=Role.USER, content=input))
162 |         return messages
163 | 
164 |     def _generate(self, messages: list[Message], **extra_kwargs: Any) -> dict:
165 |         """Call ``engine.generate()`` with stored defaults.
166 | 
167 |         Extra kwargs (e.g. ``tools``) are forwarded to the engine.
168 |         Publishes INFERENCE_START/END events on the bus when the engine
169 |         does not publish its own (i.e. non-instrumented engines).
170 |         """
171 |         if self._bus and not getattr(self._engine, "_publishes_events", False):
172 |             engine_id = getattr(self._engine, "engine_id", "")
173 |             self._bus.publish(
174 |                 EventType.INFERENCE_START,
175 |                 {"model": self._model, "engine": engine_id},
176 |             )
177 | 
178 |         result = self._engine.generate(
179 |             messages,
180 |             model=self._model,
181 |             temperature=self._temperature,
182 |             max_tokens=self._max_tokens,
183 |             **extra_kwargs,
184 |         )
185 | 
186 |         if self._bus and not getattr(self._engine, "_publishes_events", False):
187 |             usage = result.get("usage", {})
188 |             self._bus.publish(
189 |                 EventType.INFERENCE_END,
190 |                 {
191 |                     "model": self._model,
192 |                     "usage": usage,
193 |                     "content": result.get("content", ""),
194 |                     "tool_calls": result.get("tool_calls", []),
195 |                     "finish_reason": result.get("finish_reason", ""),
196 |                 },
197 |             )
198 | 
199 |         return result
200 | 
201 |     def _max_turns_result(
202 |         self,
203 |         tool_results: list[ToolResult],
204 |         turns: int,
205 |         content: str = "",
206 |         *,
207 |         metadata: Optional[Dict[str, Any]] = None,
208 |     ) -> AgentResult:
209 |         """Build the standard result for when ``max_turns`` is exceeded."""
210 |         self._emit_turn_end(turns=turns, max_turns_exceeded=True)
211 |         md: Dict[str, Any] = {"max_turns_exceeded": True}
212 |         if metadata:
213 |             md.update(metadata)
214 |         return AgentResult(
215 |             content=content or "Maximum turns reached without a final answer.",
216 |             tool_results=tool_results,
217 |             turns=turns,
218 |             metadata=md,
219 |         )
220 | 
221 |     def _check_continuation(
222 |         self,
223 |         result: dict,
224 |         messages: list,
225 |         *,
226 |         max_continuations: int = 2,
227 |     ) -> str:
228 |         """Re-prompt on ``finish_reason == "length"`` to get complete output.
229 | 
230 |         Returns the concatenated content after up to *max_continuations*
231 |         follow-up generate calls.
232 |         """
233 |         content = result.get("content", "")
234 |         finish_reason = result.get("finish_reason", "")
235 | 
236 |         for _ in range(max_continuations):
237 |             if finish_reason != "length":
238 |                 break
239 |             # Append what we have so far and ask the model to continue
240 |             from openjarvis.core.types import Message, Role
241 | 
242 |             messages.append(Message(role=Role.ASSISTANT, content=content))
243 |             messages.append(
244 |                 Message(
245 |                     role=Role.USER,
246 |                     content="Continue from where you left off.",
247 |                 ),
248 |             )
249 |             cont = self._generate(messages)
250 |             continuation = cont.get("content", "")
251 |             content += continuation
252 |             finish_reason = cont.get("finish_reason", "")
253 | 
254 |         return content
255 | 
256 |     @staticmethod
257 |     def _strip_think_tags(text: str) -> str:
258 |         """Remove ``<think>...</think>`` blocks from model output.
259 | 
260 |         Handles both ``<think>...</think>`` and the common distilled-model
261 |         pattern where the opening ``<think>`` is absent and the response
262 |         begins directly with reasoning text followed by ``</think>``.
263 |         """
264 |         # Full <think>...</think> blocks
265 |         text = re.sub(
266 |             r"<think>.*?</think>\s*",
267 |             "",
268 |             text,
269 |             flags=re.DOTALL | re.IGNORECASE,
270 |         )
271 |         # Leading content before a bare </think> (no opening tag)
272 |         text = re.sub(r"^.*?</think>\s*", "", text, flags=re.DOTALL | re.IGNORECASE)
273 |         return text.strip()
274 | 
275 |     @abstractmethod
276 |     def run(
277 |         self,
278 |         input: str,
279 |         context: Optional[AgentContext] = None,
280 |         **kwargs: Any,
281 |     ) -> AgentResult:
282 |         """Execute the agent on *input* and return an ``AgentResult``."""
283 | 
284 | 
285 | class ToolUsingAgent(BaseAgent):
286 |     """Intermediate base for agents that accept and use tools.
287 | 
288 |     Sets ``accepts_tools = True`` for CLI/SDK introspection, and
289 |     initialises a :class:`ToolExecutor` from the provided tools.
290 |     """
291 | 
292 |     accepts_tools: bool = True
293 | 
294 |     def __init__(
295 |         self,
296 |         engine: InferenceEngine,
297 |         model: str,
298 |         *,
299 |         tools: Optional[List["BaseTool"]] = None,  # noqa: F821
300 |         bus: Optional[EventBus] = None,
301 |         max_turns: Optional[int] = None,
302 |         temperature: Optional[float] = None,
303 |         max_tokens: Optional[int] = None,
304 |         loop_guard_config: Optional[Any] = None,
305 |         capability_policy: Optional[Any] = None,
306 |         agent_id: Optional[str] = None,
307 |         interactive: bool = False,
308 |         confirm_callback: Optional[Any] = None,
309 |         skill_few_shot_examples: Optional[List[str]] = None,
310 |     ) -> None:
311 |         super().__init__(
312 |             engine,
313 |             model,
314 |             bus=bus,
315 |             temperature=temperature,
316 |             max_tokens=max_tokens,
317 |         )
318 |         from openjarvis.tools._stubs import ToolExecutor
319 | 
320 |         self._tools = tools or []
321 |         # Plan 2B I3: store optimized few-shot examples for agents to inject
322 |         # into their own system prompt templates as appropriate.
323 |         self._skill_few_shot_examples = list(skill_few_shot_examples or [])
324 |         _aid = agent_id or getattr(self, "agent_id", "")
325 |         self._executor = ToolExecutor(
326 |             self._tools,
327 |             bus=bus,
328 |             capability_policy=capability_policy,
329 |             agent_id=_aid,
330 |             interactive=interactive,
331 |             confirm_callback=confirm_callback,
332 |         )
333 |         # Resolve max_turns: explicit arg > config > class default > 10
334 |         if max_turns is not None:
335 |             self._max_turns = max_turns
336 |         else:
337 |             try:
338 |                 cfg = load_config()
339 |                 self._max_turns = cfg.agent.max_turns
340 |             except Exception:
341 |                 self._max_turns = getattr(self, "_default_max_turns", 10)
342 | 
343 |         # Loop guard
344 |         self._loop_guard = None
345 |         try:
346 |             from openjarvis.agents.loop_guard import LoopGuard, LoopGuardConfig
347 | 
348 |             if loop_guard_config is None:
349 |                 loop_guard_config = LoopGuardConfig()
350 |             elif isinstance(loop_guard_config, dict):
351 |                 loop_guard_config = LoopGuardConfig(**loop_guard_config)
352 |             if loop_guard_config.enabled:
353 |                 self._loop_guard = LoopGuard(loop_guard_config, bus=bus)
354 |         except ImportError:
355 |             pass
356 | 
357 | 
358 | __all__ = ["AgentContext", "AgentResult", "BaseAgent", "ToolUsingAgent"]
```

---

## FILE: `src/openjarvis/core/compression.py`

**NOT FOUND ON DISK.**

Files with this basename elsewhere in the tree:

- `src/openjarvis/sessions/compression.py`

Do not guess at this file's contents. Note its absence in your answer and work from what is present.

---

## FILE: `src/openjarvis/core/types.py`

- bytes: 8109
- lines: 278
- sha256: `4FBB732AE4DAAE5B117ECB37CC1F270CC67A614E51A1E5D37B7FBCBAABD66011`
- line terminator: LF

Line numbers below are 1-based and authoritative. Cite them.

```python
  1 | """Canonical data types shared across all OpenJarvis primitives."""
  2 | 
  3 | from __future__ import annotations
  4 | 
  5 | import uuid
  6 | from dataclasses import dataclass, field
  7 | from enum import Enum
  8 | from typing import Any, Dict, List, Optional, Sequence  # noqa: I001
  9 | 
 10 | # ---------------------------------------------------------------------------
 11 | # Enums
 12 | # ---------------------------------------------------------------------------
 13 | 
 14 | 
 15 | class Role(str, Enum):
 16 |     """Chat message roles (OpenAI-compatible)."""
 17 | 
 18 |     SYSTEM = "system"
 19 |     USER = "user"
 20 |     ASSISTANT = "assistant"
 21 |     TOOL = "tool"
 22 | 
 23 | 
 24 | class Quantization(str, Enum):
 25 |     """Model quantization formats."""
 26 | 
 27 |     NONE = "none"
 28 |     FP8 = "fp8"
 29 |     FP4 = "fp4"
 30 |     INT8 = "int8"
 31 |     INT4 = "int4"
 32 |     GGUF = "gguf"
 33 |     GGUF_Q4 = "gguf_q4"
 34 |     GGUF_Q8 = "gguf_q8"
 35 | 
 36 | 
 37 | class StepType(str, Enum):
 38 |     """Types of steps within an agent trace."""
 39 | 
 40 |     ROUTE = "route"
 41 |     RETRIEVE = "retrieve"
 42 |     GENERATE = "generate"
 43 |     TOOL_CALL = "tool_call"
 44 |     RESPOND = "respond"
 45 | 
 46 | 
 47 | # ---------------------------------------------------------------------------
 48 | # Message types
 49 | # ---------------------------------------------------------------------------
 50 | 
 51 | 
 52 | @dataclass(slots=True)
 53 | class ToolCall:
 54 |     """A single tool invocation request embedded in an assistant message."""
 55 | 
 56 |     id: str
 57 |     name: str
 58 |     arguments: str  # JSON string
 59 | 
 60 | 
 61 | @dataclass(slots=True)
 62 | class Message:
 63 |     """A single chat message (OpenAI-compatible structure)."""
 64 | 
 65 |     role: Role
 66 |     content: str = ""
 67 |     name: Optional[str] = None
 68 |     tool_calls: Optional[List[ToolCall]] = None
 69 |     tool_call_id: Optional[str] = None
 70 |     metadata: Dict[str, Any] = field(default_factory=dict)
 71 | 
 72 | 
 73 | @dataclass(slots=True)
 74 | class Conversation:
 75 |     """Ordered list of messages with an optional sliding-window cap."""
 76 | 
 77 |     messages: List[Message] = field(default_factory=list)
 78 |     max_messages: Optional[int] = None
 79 | 
 80 |     def add(self, message: Message) -> None:
 81 |         """Append a message, trimming oldest if *max_messages* is set."""
 82 |         self.messages.append(message)
 83 |         if self.max_messages is not None and len(self.messages) > self.max_messages:
 84 |             self.messages = self.messages[-self.max_messages :]
 85 | 
 86 |     def window(self, n: int) -> List[Message]:
 87 |         """Return the last *n* messages."""
 88 |         if n <= 0:
 89 |             return []
 90 |         return self.messages[-n:]
 91 | 
 92 | 
 93 | # ---------------------------------------------------------------------------
 94 | # Model / tool / telemetry records
 95 | # ---------------------------------------------------------------------------
 96 | 
 97 | 
 98 | @dataclass(slots=True)
 99 | class ModelSpec:
100 |     """Metadata describing a language model."""
101 | 
102 |     model_id: str
103 |     name: str
104 |     parameter_count_b: float
105 |     context_length: int
106 |     active_parameter_count_b: Optional[float] = None  # MoE active params
107 |     quantization: Quantization = Quantization.NONE
108 |     min_vram_gb: float = 0.0
109 |     supported_engines: Sequence[str] = ()
110 |     provider: str = ""
111 |     requires_api_key: bool = False
112 |     metadata: Dict[str, Any] = field(default_factory=dict)
113 | 
114 | 
115 | @dataclass(slots=True)
116 | class ToolResult:
117 |     """Result returned by a tool invocation."""
118 | 
119 |     tool_name: str
120 |     content: str
121 |     success: bool = True
122 |     usage: Dict[str, Any] = field(default_factory=dict)
123 |     cost_usd: float = 0.0
124 |     latency_seconds: float = 0.0
125 |     metadata: Dict[str, Any] = field(default_factory=dict)
126 | 
127 | 
128 | @dataclass(slots=True)
129 | class TelemetryRecord:
130 |     """Single telemetry observation recorded after an inference call."""
131 | 
132 |     timestamp: float
133 |     model_id: str
134 |     prompt_tokens: int = 0
135 |     prompt_tokens_evaluated: int = 0  # KV-cache-aware: actual tokens processed
136 |     completion_tokens: int = 0
137 |     total_tokens: int = 0
138 |     latency_seconds: float = 0.0
139 |     ttft: float = 0.0  # time to first token
140 |     cost_usd: float = 0.0
141 |     energy_joules: float = 0.0
142 |     power_watts: float = 0.0
143 |     gpu_utilization_pct: float = 0.0
144 |     gpu_memory_used_gb: float = 0.0
145 |     gpu_temperature_c: float = 0.0
146 |     throughput_tok_per_sec: float = 0.0
147 |     energy_per_output_token_joules: float = 0.0
148 |     throughput_per_watt: float = 0.0
149 |     prefill_latency_seconds: float = 0.0
150 |     decode_latency_seconds: float = 0.0
151 |     prefill_energy_joules: float = 0.0
152 |     decode_energy_joules: float = 0.0
153 |     mean_itl_ms: float = 0.0
154 |     median_itl_ms: float = 0.0
155 |     p90_itl_ms: float = 0.0
156 |     p95_itl_ms: float = 0.0
157 |     p99_itl_ms: float = 0.0
158 |     std_itl_ms: float = 0.0
159 |     is_streaming: bool = False
160 |     engine: str = ""
161 |     agent: str = ""
162 |     energy_method: str = ""
163 |     energy_vendor: str = ""
164 |     batch_id: str = ""
165 |     is_warmup: bool = False
166 |     cpu_energy_joules: float = 0.0
167 |     gpu_energy_joules: float = 0.0
168 |     dram_energy_joules: float = 0.0
169 |     tokens_per_joule: float = 0.0
170 |     mining_session_id: Optional[str] = None
171 |     metadata: Dict[str, Any] = field(default_factory=dict)
172 | 
173 | 
174 | # ---------------------------------------------------------------------------
175 | # Trace types — full interaction-level recording
176 | # ---------------------------------------------------------------------------
177 | 
178 | 
179 | def _trace_id() -> str:
180 |     return uuid.uuid4().hex[:16]
181 | 
182 | 
183 | def _message_to_dict(msg: "Message") -> Dict[str, Any]:
184 |     """Serialize a Message to a JSON-safe dict."""
185 |     d: Dict[str, Any] = {"role": msg.role.value, "content": msg.content}
186 |     if msg.name:
187 |         d["name"] = msg.name
188 |     if msg.tool_calls:
189 |         d["tool_calls"] = [
190 |             {"id": tc.id, "name": tc.name, "arguments": tc.arguments}
191 |             for tc in msg.tool_calls
192 |         ]
193 |     if msg.tool_call_id:
194 |         d["tool_call_id"] = msg.tool_call_id
195 |     return d
196 | 
197 | 
198 | @dataclass(slots=True)
199 | class TraceStep:
200 |     """A single step within an agent trace.
201 | 
202 |     Each step records what the agent did (route, retrieve, generate,
203 |     tool_call, respond), its inputs and outputs, and timing.
204 |     """
205 | 
206 |     step_type: StepType
207 |     timestamp: float
208 |     duration_seconds: float = 0.0
209 |     input: Dict[str, Any] = field(default_factory=dict)
210 |     output: Dict[str, Any] = field(default_factory=dict)
211 |     metadata: Dict[str, Any] = field(default_factory=dict)
212 | 
213 | 
214 | @dataclass(slots=True)
215 | class Trace:
216 |     """Complete trace of an agent handling a query.
217 | 
218 |     A trace captures the full sequence of steps an agent took to handle a
219 |     query — which model was selected, what memory was retrieved, which tools
220 |     were called, and the final response.  Traces are the primary input to the
221 |     learning system: by analyzing which decisions led to good outcomes, the
222 |     system can improve routing, tool selection, and memory strategies.
223 |     """
224 | 
225 |     trace_id: str = field(default_factory=_trace_id)
226 |     query: str = ""
227 |     agent: str = ""
228 |     model: str = ""
229 |     engine: str = ""
230 |     steps: List[TraceStep] = field(default_factory=list)
231 |     result: str = ""
232 |     outcome: Optional[str] = None  # None=unknown, "success", "failure"
233 |     feedback: Optional[float] = None  # user quality score [0, 1]
234 |     started_at: float = 0.0
235 |     ended_at: float = 0.0
236 |     total_tokens: int = 0
237 |     total_latency_seconds: float = 0.0
238 |     metadata: Dict[str, Any] = field(default_factory=dict)
239 |     messages: List[Dict[str, Any]] = field(default_factory=list)
240 | 
241 |     def add_step(self, step: TraceStep) -> None:
242 |         """Append a step and update running totals."""
243 |         self.steps.append(step)
244 |         self.total_latency_seconds += step.duration_seconds
245 |         self.total_tokens += step.output.get("tokens", 0)
246 | 
247 | 
248 | @dataclass(slots=True)
249 | class RoutingContext:
250 |     """Context describing a query for model routing decisions."""
251 | 
252 |     query: str = ""
253 |     query_length: int = 0
254 |     has_code: bool = False
255 |     has_math: bool = False
256 |     has_reasoning: bool = False
257 |     language: str = "en"
258 |     urgency: float = 0.5
259 |     complexity_score: float = 0.0  # 0.0 (trivial) to 1.0 (very complex)
260 |     suggested_max_tokens: int = 1024
261 |     metadata: Dict[str, Any] = field(default_factory=dict)
262 | 
263 | 
264 | __all__ = [
265 |     "Conversation",
266 |     "Message",
267 |     "ModelSpec",
268 |     "Quantization",
269 |     "Role",
270 |     "RoutingContext",
271 |     "StepType",
272 |     "TelemetryRecord",
273 |     "ToolCall",
274 |     "ToolResult",
275 |     "Trace",
276 |     "TraceStep",
277 |     "_message_to_dict",
278 | ]
```

---

## FILE: `src/openjarvis/engine/ollama.py`

- bytes: 19948
- lines: 538
- sha256: `EAEC3A42CB25A31F44B2B8EB2EAF05B3F4E5EAB4E2B5D423F2AA40827B5AA7FD`
- line terminator: LF

Line numbers below are 1-based and authoritative. Cite them.

```python
  1 | """Ollama inference engine backend."""
  2 | 
  3 | from __future__ import annotations
  4 | 
  5 | import json
  6 | import logging
  7 | import os
  8 | from collections.abc import AsyncIterator, Sequence
  9 | from typing import Any, Dict, List
 10 | 
 11 | import httpx
 12 | 
 13 | from openjarvis.core.registry import EngineRegistry
 14 | from openjarvis.core.types import Message
 15 | from openjarvis.engine._base import (
 16 |     EngineConnectionError,
 17 |     InferenceEngine,
 18 |     estimate_prompt_tokens,
 19 |     messages_to_dicts,
 20 | )
 21 | from openjarvis.engine._stubs import StreamChunk
 22 | 
 23 | logger = logging.getLogger(__name__)
 24 | 
 25 | 
 26 | @EngineRegistry.register("ollama")
 27 | class OllamaEngine(InferenceEngine):
 28 |     """Ollama backend via its native HTTP API."""
 29 | 
 30 |     engine_id = "ollama"
 31 | 
 32 |     _DEFAULT_HOST = "http://localhost:11434"
 33 | 
 34 |     def __init__(
 35 |         self,
 36 |         host: str | None = None,
 37 |         *,
 38 |         timeout: float = 1800.0,
 39 |     ) -> None:
 40 |         # Priority: explicit host (from config.toml) > OLLAMA_HOST env var > default
 41 |         if host is None:
 42 |             env_host = os.environ.get("OLLAMA_HOST")
 43 |             host = env_host or self._DEFAULT_HOST
 44 |         self._host = host.rstrip("/")
 45 |         self._client = httpx.Client(base_url=self._host, timeout=timeout)
 46 |         # Last stream usage — captured from Ollama's final chunk
 47 |         self._last_stream_usage: Dict[str, int] = {}
 48 | 
 49 |     def generate(
 50 |         self,
 51 |         messages: Sequence[Message],
 52 |         *,
 53 |         model: str,
 54 |         temperature: float = 0.7,
 55 |         max_tokens: int = 1024,
 56 |         **kwargs: Any,
 57 |     ) -> Dict[str, Any]:
 58 |         msg_dicts = messages_to_dicts(messages)
 59 |         # Ollama expects tool_call arguments as dicts, not JSON strings
 60 |         for md in msg_dicts:
 61 |             for tc in md.get("tool_calls", []):
 62 |                 fn = tc.get("function", {})
 63 |                 args = fn.get("arguments")
 64 |                 if isinstance(args, str):
 65 |                     try:
 66 |                         fn["arguments"] = json.loads(args)
 67 |                     except (json.JSONDecodeError, TypeError):
 68 |                         pass
 69 |         payload: Dict[str, Any] = {
 70 |             "model": model,
 71 |             "messages": msg_dicts,
 72 |             "stream": False,
 73 |             "options": {
 74 |                 "temperature": temperature,
 75 |                 "num_predict": max_tokens,
 76 |                 "num_ctx": kwargs.get("num_ctx", _oj_default_num_ctx()),
 77 |             },
 78 |         }
 79 |         # Disable extended thinking by default (Qwen3.5 etc.).
 80 |         # When enabled, thinking tokens consume the entire budget and
 81 |         # the visible content comes back empty.
 82 |         if "think" not in kwargs:
 83 |             payload["think"] = False
 84 |         elif kwargs["think"] is not None:
 85 |             payload["think"] = kwargs["think"]
 86 |         # Pass tools if provided
 87 |         tools = kwargs.get("tools")
 88 |         if tools:
 89 |             payload["tools"] = tools
 90 | 
 91 |         # Apply structured output / JSON mode
 92 |         response_format = kwargs.get("response_format")
 93 |         if response_format is not None:
 94 |             from openjarvis.engine._stubs import ResponseFormat
 95 | 
 96 |             if isinstance(response_format, ResponseFormat):
 97 |                 payload["format"] = "json"
 98 |             elif isinstance(response_format, dict):
 99 |                 payload["format"] = "json"
100 |         try:
101 |             resp = self._client.post("/api/chat", json=payload)
102 |             if resp.status_code == 400 and tools:
103 |                 # Model may not support function calling -- retry without tools
104 |                 _oj_log_retry400(resp, payload, tools)  # openjarvis-retry400-v1
105 |                 payload.pop("tools", None)
106 |                 resp = self._client.post("/api/chat", json=payload)
107 |                 _oj_log_retry400_result(resp)  # openjarvis-retry400-v1
108 |             resp.raise_for_status()
109 |         except (httpx.ConnectError, httpx.TimeoutException) as exc:
110 |             raise EngineConnectionError(
111 |                 f"Ollama not reachable at {self._host}"
112 |             ) from exc
113 |         except httpx.HTTPStatusError as exc:
114 |             body = exc.response.text[:500] if exc.response else ""
115 |             raise RuntimeError(
116 |                 f"Ollama returned {exc.response.status_code}: {body}"
117 |             ) from exc
118 |         data = resp.json()
119 |         # prompt_eval_count = tokens actually evaluated (KV-cache-aware).
120 |         # estimate_prompt_tokens = full prompt size (for cost comparison).
121 |         # We report both so downstream can use the right one:
122 |         #   prompt_tokens        → full size (what cloud would charge)
123 |         #   prompt_tokens_evaluated → actual compute (with KV cache)
124 |         reported_prompt = data.get("prompt_eval_count", 0)
125 |         estimated_prompt = estimate_prompt_tokens(messages)
126 |         prompt_tokens = max(reported_prompt, estimated_prompt)
127 |         prompt_tokens_evaluated = (
128 |             reported_prompt if reported_prompt > 0 else prompt_tokens
129 |         )
130 |         completion_tokens = data.get("eval_count", 0)
131 |         content = data.get("message", {}).get("content", "")
132 |         result: Dict[str, Any] = {
133 |             "content": content,
134 |             "usage": {
135 |                 "prompt_tokens": prompt_tokens,
136 |                 "prompt_tokens_evaluated": prompt_tokens_evaluated,
137 |                 "completion_tokens": completion_tokens,
138 |                 "total_tokens": prompt_tokens + completion_tokens,
139 |             },
140 |             "model": data.get("model", model),
141 |             "finish_reason": "stop",
142 |         }
143 |         # Extract timing from Ollama response (nanoseconds → seconds)
144 |         result["ttft"] = data.get("prompt_eval_duration", 0) / 1e9
145 |         result["engine_timing"] = {
146 |             k: data[k]
147 |             for k in (
148 |                 "total_duration",
149 |                 "load_duration",
150 |                 "prompt_eval_duration",
151 |                 "eval_duration",
152 |             )
153 |             if k in data
154 |         }
155 |         # Extract tool calls if present
156 |         raw_tool_calls = data.get("message", {}).get("tool_calls", [])
157 |         if raw_tool_calls:
158 |             tool_calls = []
159 |             for i, tc in enumerate(raw_tool_calls):
160 |                 raw_args = tc.get("function", {}).get(
161 |                     "arguments",
162 |                     "{}",
163 |                 )
164 |                 tool_calls.append(
165 |                     {
166 |                         "id": tc.get("id", f"call_{i}"),
167 |                         "name": tc.get("function", {}).get("name", ""),
168 |                         "arguments": (
169 |                             json.dumps(raw_args)
170 |                             if isinstance(raw_args, dict)
171 |                             else raw_args
172 |                         ),
173 |                     }
174 |                 )
175 |             result["tool_calls"] = tool_calls
176 |         return result
177 | 
178 |     async def stream(
179 |         self,
180 |         messages: Sequence[Message],
181 |         *,
182 |         model: str,
183 |         temperature: float = 0.7,
184 |         max_tokens: int = 1024,
185 |         **kwargs: Any,
186 |     ) -> AsyncIterator[str]:
187 |         payload: Dict[str, Any] = {
188 |             "model": model,
189 |             "messages": messages_to_dicts(messages),
190 |             "stream": True,
191 |             "options": {
192 |                 "temperature": temperature,
193 |                 "num_predict": max_tokens,
194 |                 "num_ctx": kwargs.get("num_ctx", _oj_default_num_ctx()),
195 |             },
196 |         }
197 |         # Mirror generate()'s default: disable extended thinking unless the
198 |         # caller opted in. Qwen3/etc. with thinking on can stall the visible
199 |         # stream for 60+ seconds before any tokens reach the client, which
200 |         # frontends interpret as a "Load failed" timeout.
201 |         if "think" not in kwargs:
202 |             payload["think"] = False
203 |         elif kwargs["think"] is not None:
204 |             payload["think"] = kwargs["think"]
205 |         try:
206 |             with self._client.stream("POST", "/api/chat", json=payload) as resp:
207 |                 resp.raise_for_status()
208 |                 for line in resp.iter_lines():
209 |                     if not line.strip():
210 |                         continue
211 |                     try:
212 |                         chunk = json.loads(line)
213 |                     except json.JSONDecodeError:
214 |                         continue
215 |                     content = chunk.get("message", {}).get("content", "")
216 |                     if content:
217 |                         yield content
218 |                     if chunk.get("done", False):
219 |                         reported_prompt = chunk.get("prompt_eval_count", 0)
220 |                         est_prompt = estimate_prompt_tokens(messages)
221 |                         full_prompt = max(reported_prompt, est_prompt)
222 |                         evaluated = (
223 |                             reported_prompt if reported_prompt > 0 else full_prompt
224 |                         )
225 |                         comp = chunk.get("eval_count", 0)
226 |                         self._last_stream_usage = {
227 |                             "prompt_tokens": full_prompt,
228 |                             "prompt_tokens_evaluated": evaluated,
229 |                             "completion_tokens": comp,
230 |                             "total_tokens": full_prompt + comp,
231 |                         }
232 |                         break
233 |         except (httpx.ConnectError, httpx.TimeoutException) as exc:
234 |             raise EngineConnectionError(
235 |                 f"Ollama not reachable at {self._host}"
236 |             ) from exc
237 | 
238 |     async def stream_full(
239 |         self,
240 |         messages: Sequence[Message],
241 |         *,
242 |         model: str,
243 |         temperature: float = 0.7,
244 |         max_tokens: int = 1024,
245 |         **kwargs: Any,
246 |     ) -> AsyncIterator[StreamChunk]:
247 |         """Yield ``StreamChunk``s including tool_calls.
248 | 
249 |         Unlike the default ``stream_full`` in the base class (which wraps
250 |         ``stream()`` and drops tools), this posts to ``/api/chat`` with
251 |         ``tools`` from kwargs and parses tool_calls out of the streamed
252 |         response. Falls back to a tools-less retry on 400 (mirrors
253 |         ``generate()``'s behaviour for models that don't support tools).
254 |         """
255 |         msg_dicts = messages_to_dicts(messages)
256 |         for md in msg_dicts:
257 |             for tc in md.get("tool_calls", []):
258 |                 fn = tc.get("function", {})
259 |                 args = fn.get("arguments")
260 |                 if isinstance(args, str):
261 |                     try:
262 |                         fn["arguments"] = json.loads(args)
263 |                     except (json.JSONDecodeError, TypeError):
264 |                         pass
265 | 
266 |         payload: Dict[str, Any] = {
267 |             "model": model,
268 |             "messages": msg_dicts,
269 |             "stream": True,
270 |             "options": {
271 |                 "temperature": temperature,
272 |                 "num_predict": max_tokens,
273 |                 "num_ctx": kwargs.get("num_ctx", _oj_default_num_ctx()),
274 |             },
275 |         }
276 |         if "think" not in kwargs:
277 |             payload["think"] = False
278 |         elif kwargs["think"] is not None:
279 |             payload["think"] = kwargs["think"]
280 | 
281 |         tools = kwargs.get("tools")
282 |         if tools:
283 |             payload["tools"] = tools
284 | 
285 |         async for chunk in self._run_stream(
286 |             payload, messages, retry_without_tools=bool(tools)
287 |         ):
288 |             yield chunk
289 | 
290 |     async def _run_stream(
291 |         self,
292 |         payload: Dict[str, Any],
293 |         messages: Sequence[Message],
294 |         *,
295 |         retry_without_tools: bool,
296 |     ) -> AsyncIterator[StreamChunk]:
297 |         """Execute the streaming request and yield parsed StreamChunks."""
298 |         try:
299 |             with self._client.stream("POST", "/api/chat", json=payload) as resp:
300 |                 if resp.status_code == 400 and retry_without_tools:
301 |                     # Model doesn't support tools — retry without them.
302 |                     payload.pop("tools", None)
303 |                     async for c in self._run_stream(
304 |                         payload, messages, retry_without_tools=False
305 |                     ):
306 |                         yield c
307 |                     return
308 |                 resp.raise_for_status()
309 | 
310 |                 finish_reason: str | None = None
311 |                 for line in resp.iter_lines():
312 |                     if not line.strip():
313 |                         continue
314 |                     try:
315 |                         chunk = json.loads(line)
316 |                     except json.JSONDecodeError:
317 |                         continue
318 | 
319 |                     message = chunk.get("message", {}) or {}
320 |                     content = message.get("content", "")
321 |                     raw_tool_calls = message.get("tool_calls") or []
322 | 
323 |                     if content:
324 |                         yield StreamChunk(content=content)
325 | 
326 |                     if raw_tool_calls:
327 |                         # Ollama emits fully-formed tool_calls in a single
328 |                         # chunk (not fragmented). Convert to the
329 |                         # OpenAI-delta fragment shape that agent_manager_routes
330 |                         # expects in _merge_tool_call_fragments.
331 |                         fragments: List[Dict[str, Any]] = []
332 |                         for i, tc in enumerate(raw_tool_calls):
333 |                             fn = tc.get("function", {}) or {}
334 |                             raw_args = fn.get("arguments", "{}")
335 |                             args_str = (
336 |                                 json.dumps(raw_args)
337 |                                 if isinstance(raw_args, dict)
338 |                                 else str(raw_args)
339 |                             )
340 |                             fragments.append(
341 |                                 {
342 |                                     "index": i,
343 |                                     "id": tc.get("id", f"call_{i}"),
344 |                                     "type": "function",
345 |                                     "function": {
346 |                                         "name": fn.get("name", ""),
347 |                                         "arguments": args_str,
348 |                                     },
349 |                                 }
350 |                             )
351 |                         yield StreamChunk(tool_calls=fragments)
352 |                         finish_reason = "tool_calls"
353 | 
354 |                     if chunk.get("done", False):
355 |                         reported_prompt = chunk.get("prompt_eval_count", 0)
356 |                         est_prompt = estimate_prompt_tokens(messages)
357 |                         full_prompt = max(reported_prompt, est_prompt)
358 |                         evaluated = (
359 |                             reported_prompt if reported_prompt > 0 else full_prompt
360 |                         )
361 |                         comp = chunk.get("eval_count", 0)
362 |                         self._last_stream_usage = {
363 |                             "prompt_tokens": full_prompt,
364 |                             "prompt_tokens_evaluated": evaluated,
365 |                             "completion_tokens": comp,
366 |                             "total_tokens": full_prompt + comp,
367 |                         }
368 |                         if finish_reason is None:
369 |                             finish_reason = chunk.get("done_reason") or "stop"
370 |                         yield StreamChunk(
371 |                             finish_reason=finish_reason,
372 |                             usage=dict(self._last_stream_usage),
373 |                         )
374 |                         break
375 |         except (httpx.ConnectError, httpx.TimeoutException) as exc:
376 |             raise EngineConnectionError(
377 |                 f"Ollama not reachable at {self._host}"
378 |             ) from exc
379 | 
380 |     def list_models(self) -> List[str]:
381 |         try:
382 |             resp = self._client.get("/api/tags")
383 |             resp.raise_for_status()
384 |         except (
385 |             httpx.ConnectError,
386 |             httpx.TimeoutException,
387 |             httpx.HTTPStatusError,
388 |         ) as exc:
389 |             logger.warning(
390 |                 "Failed to list models from Ollama at %s: %s",
391 |                 self._host,
392 |                 exc,
393 |             )
394 |             return []
395 |         data = resp.json()
396 |         return [m["name"] for m in data.get("models", [])]
397 | 
398 |     def health(self) -> bool:
399 |         try:
400 |             resp = self._client.get("/api/tags", timeout=2.0)
401 |             return resp.status_code == 200
402 |         except Exception as exc:
403 |             logger.debug("Ollama health check failed at %s: %s", self._host, exc)
404 |             return False
405 | 
406 |     def close(self) -> None:
407 |         self._client.close()
408 | 
409 | 
410 | __all__ = ["OllamaEngine"]
411 | 
412 | 
413 | # --- openjarvis-retry400-v1 : temporary diagnostic, remove when Defect 1 is fixed ---
414 | def _oj_r400_logger():
415 |     import logging, logging.handlers, os as _os
416 |     lg = logging.getLogger("openjarvis.retry400")
417 |     if getattr(lg, "_oj_ready", False):
418 |         return lg
419 |     try:
420 |         d = _os.path.join(_os.environ.get("LOCALAPPDATA", "."), "OpenJarvis", "logs")
421 |         _os.makedirs(d, exist_ok=True)
422 |         h = logging.handlers.RotatingFileHandler(
423 |             _os.path.join(d, "engine.log"),
424 |             maxBytes=2 * 1024 * 1024,
425 |             backupCount=2,
426 |             encoding="utf-8",
427 |         )
428 |         h.setFormatter(logging.Formatter("%(asctime)s %(message)s"))
429 |         lg.addHandler(h)
430 |     except Exception:
431 |         lg.addHandler(logging.NullHandler())
432 |     lg.setLevel(logging.INFO)
433 |     lg.propagate = False
434 |     lg._oj_ready = True
435 |     return lg
436 | 
437 | 
438 | def _oj_log_retry400(resp, payload, tools):
439 |     try:
440 |         import json as _json
441 |         try:
442 |             body = resp.text[:600]
443 |         except Exception:
444 |             body = "<unreadable>"
445 |         try:
446 |             psize = len(_json.dumps(payload))
447 |         except Exception:
448 |             psize = -1
449 |         _oj_r400_logger().info(
450 |             "RETRY400 dropping tools ntools=%s payloadbytes=%s nmsgs=%s body=%r",
451 |             len(tools) if tools else 0,
452 |             psize,
453 |             len(payload.get("messages", []) or []),
454 |             body,
455 |         )
456 |     except Exception:
457 |         pass
458 | 
459 | 
460 | def _oj_log_retry400_result(resp):
461 |     try:
462 |         _oj_r400_logger().info(
463 |             "RETRY400 retry_status=%s", getattr(resp, "status_code", "?")
464 |         )
465 |     except Exception:
466 |         pass
467 | 
468 | # --- openjarvis-num-ctx-config-v1 -------------------------------------------
469 | # Resolves the DEFAULT num_ctx for this engine from configuration instead of a
470 | # hardcoded literal. Callers that pass num_ctx explicitly are unaffected.
471 | #
472 | # Resolution order:
473 | #   1. env OPENJARVIS_NUM_CTX
474 | #   2. [engine] num_ctx in config.toml
475 | #   3. 8192  (unchanged legacy behavior)
476 | #
477 | # Resolved once per process and cached. Every failure path falls back to 8192.
478 | 
479 | _OJ_NUM_CTX_CACHE = None
480 | 
481 | 
482 | def _oj_config_path():
483 |     import os as _os
484 |     home = _os.environ.get("OPENJARVIS_HOME", "").strip()
485 |     if not home:
486 |         home = _os.path.join(_os.path.expanduser("~"), ".openjarvis")
487 |     return _os.path.join(home, "config.toml")
488 | 
489 | 
490 | def _oj_num_ctx_from_config():
491 |     import re as _re
492 |     try:
493 |         with open(_oj_config_path(), "rb") as _fh:
494 |             raw = _fh.read()
495 |     except Exception:
496 |         return None
497 |     text = raw.decode("utf-8", "replace").lstrip(chr(65279))
498 |     try:
499 |         import tomllib as _tomllib
500 |         data = _tomllib.loads(text)
501 |         val = data.get("engine", {}).get("num_ctx")
502 |         if val is not None:
503 |             return int(val)
504 |         return None
505 |     except Exception:
506 |         pass
507 |     try:
508 |         for chunk in _re.split(r"(?m)^\s*\[", text):
509 |             if chunk.startswith("engine]"):
510 |                 m = _re.search(r"(?m)^\s*num_ctx\s*=\s*(\d+)", chunk)
511 |                 if m:
512 |                     return int(m.group(1))
513 |     except Exception:
514 |         pass
515 |     return None
516 | 
517 | 
518 | def _oj_default_num_ctx():
519 |     global _OJ_NUM_CTX_CACHE
520 |     if _OJ_NUM_CTX_CACHE is not None:
521 |         return _OJ_NUM_CTX_CACHE
522 |     value = 8192
523 |     try:
524 |         import os as _os
525 |         env = _os.environ.get("OPENJARVIS_NUM_CTX", "").strip()
526 |         if env:
527 |             value = int(env)
528 |         else:
529 |             cfg = _oj_num_ctx_from_config()
530 |             if cfg:
531 |                 value = int(cfg)
532 |     except Exception:
533 |         value = 8192
534 |     if value < 512:
535 |         value = 8192
536 |     _OJ_NUM_CTX_CACHE = value
537 |     return _OJ_NUM_CTX_CACHE
538 | # --- end openjarvis-num-ctx-config-v1 ---------------------------------------
```

---

## FILE: `src/openjarvis/agents/types.py`

**NOT FOUND ON DISK.**

Files with this basename elsewhere in the tree:

- `src/openjarvis/core/types.py`
- `src/openjarvis/evals/core/types.py`
- `src/openjarvis/learning/intelligence/orchestrator/types.py`
- `src/openjarvis/learning/optimize/types.py`
- `src/openjarvis/learning/spec_search/diagnose/types.py`
- `src/openjarvis/operators/types.py`
- `src/openjarvis/security/types.py`
- `src/openjarvis/skills/types.py`
- `src/openjarvis/workflow/types.py`

Do not guess at this file's contents. Note its absence in your answer and work from what is present.

---

# MANIFEST

| file | found | bytes | lines | sha256 |
|---|---|---|---|---|
| `src/openjarvis/agents/native_openhands.py` | yes | 25611 | 660 | `ECA4D84D79CD834E...` |
| `src/openjarvis/agents/_stubs.py` | yes | 12689 | 358 | `C9D7C461B96EE868...` |
| `src/openjarvis/core/compression.py` | NO | 0 | 0 | `` |
| `src/openjarvis/core/types.py` | yes | 8109 | 278 | `4FBB732AE4DAAE5B...` |
| `src/openjarvis/engine/ollama.py` | yes | 19948 | 538 | `EAEC3A42CB25A31F...` |
| `src/openjarvis/agents/types.py` | NO | 0 | 0 | `` |

These hashes pin the exact bytes you reviewed. If a later patch is built against different bytes, the mismatch is detectable.

