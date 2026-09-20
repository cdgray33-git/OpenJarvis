# OPENJARVIS CODE REVIEW BUNDLE

- marker: `openjarvis-cloudbundle-v1`
- set: `adhoc` - ad hoc bundle
- generated: 2026-09-02T09:21:54
- repo root: `C:\Users\Admin\OpenJarvis`
- files in bundle: 1

You are reviewing complete source files. Every file is included in full, with authoritative 1-based line numbers in the left gutter. Nothing has been elided.

---

# THE QUESTION

Trace every parameter path through this file that reaches a destructive mailbox operation. For EACH tool class with an execute() method: list every distinct combination of input parameters that leads to a delete, move, or empty operation, and state for each whether it passes through the protected-sender check marked openjarvis-protected-senders-v1. Name explicitly any path that reaches a destructive operation WITHOUT passing that check. Also list every early return in each execute() and what condition triggers it. Report CURRENT line numbers counted from this bundle, do not trust any line number from prior notes. Do not assess severity, only locate and enumerate.

---

# SOURCE

---

## FILE: `./src/openjarvis/tools/mailbox_tools.py`

- bytes: 33666
- lines: 822
- sha256: `4DB19C1EF90EEAB33C7340F9F05B5CC57C02F5E262758FDE2D8FE2646E29E268`
- line terminator: CRLF

Line numbers below are 1-based and authoritative. Cite them.

```python
  1 | """Executable mailbox tools - the agent-callable layer over imap_mail.
  2 | 
  3 | Connector ``mcp_tools()`` specs are declarative only; ``SystemBuilder``
  4 | resolves agent tools from ``MCPServer().get_tools()``, which discovers
  5 | ``BaseTool`` subclasses registered in ``ToolRegistry``. These classes are
  6 | that layer. Each one wraps ``ImapMailConnector`` and returns a JSON string.
  7 | 
  8 | Registry constraint: ``MCPServer._auto_discover_tools`` instantiates user
  9 | tools with ``ToolRegistry.create(key)`` - no arguments. Every tool here is
 10 | therefore zero-arg constructible and resolves its account at execute time.
 11 | 
 12 | SAFETY NOTE - why ``requires_confirmation`` is deliberately NOT set:
 13 | 
 14 | ``ToolExecutor.execute`` treats that flag as a hard requirement, not a
 15 | prompt::
 16 | 
 17 |     if tool.spec.requires_confirmation:
 18 |         if not self._interactive or self._confirm_callback is None:
 19 |             return ToolResult(..., success=False)
 20 | 
 21 | The server-side agent path builds its executor without ``interactive=True``
 22 | and without a confirm callback, so a tool carrying that flag does not ask
 23 | for confirmation - it fails every single call. The safety interlock is
 24 | implemented in the tool contract instead:
 25 | 
 26 |   * ``dry_run`` defaults to True and returns a plan with exact counts
 27 |   * applying requires BOTH ``dry_run=False`` AND ``confirm`` set to the
 28 |     exact string ``CONFIRM DELETE``
 29 | 
 30 | That keeps the destructive path reachable by the agent while making it
 31 | impossible to trip by accident or by a single malformed argument.
 32 | 
 33 | Account setup: credentials live in
 34 | ``~/.openjarvis/connectors/imap_mail_<account>.json`` as
 35 | ``{"email", "password", "provider"}``. Use ``setup_mailbox_account.py``
 36 | to write one; nothing here ever logs or returns a password.
 37 | """
 38 | 
 39 | from __future__ import annotations
 40 | 
 41 | import json
 42 | import logging
 43 | from datetime import datetime, timedelta
 44 | from typing import Any, Dict, List, Optional
 45 | 
 46 | from openjarvis.connectors.imap_mail import PROVIDERS, ImapMailConnector
 47 | from openjarvis.connectors.oauth import load_tokens
 48 | from openjarvis.core.config import DEFAULT_CONFIG_DIR
 49 | from openjarvis.core.registry import ToolRegistry
 50 | from openjarvis.core.types import ToolResult
 51 | from openjarvis.tools._stubs import BaseTool, ToolSpec
 52 | 
 53 | logger = logging.getLogger(__name__)
 54 | 
 55 | CONFIRM_TOKEN = "CONFIRM DELETE"
 56 | _CONNECTOR_DIR = DEFAULT_CONFIG_DIR / "connectors"
 57 | _PREFIX = "imap_mail_"
 58 | 
 59 | 
 60 | # ---------------------------------------------------------------------------
 61 | # account resolution
 62 | # ---------------------------------------------------------------------------
 63 | 
 64 | 
 65 | def list_accounts() -> List[Dict[str, str]]:
 66 |     """Return every configured mailbox account, without credentials."""
 67 |     out: List[Dict[str, str]] = []
 68 |     try:
 69 |         if not _CONNECTOR_DIR.exists():
 70 |             return out
 71 |         for path in sorted(_CONNECTOR_DIR.glob(_PREFIX + "*.json")):
 72 |             account = path.stem[len(_PREFIX) :]
 73 |             tokens = load_tokens(str(path)) or {}
 74 |             out.append(
 75 |                 {
 76 |                     "account": account,
 77 |                     "provider": tokens.get("provider", "generic"),
 78 |                     "email": tokens.get("email", ""),
 79 |                     "configured": bool(tokens.get("email") and tokens.get("password")),
 80 |                 }
 81 |             )
 82 |     except Exception as exc:
 83 |         logger.warning("mailbox tools: could not enumerate accounts: %s", exc)
 84 |     return out
 85 | 
 86 | 
 87 | def _resolve_account(account: str) -> str:
 88 |     """Pick an account name, defaulting to the only one if unambiguous."""
 89 |     # openjarvis-account-resolve-v1: validate the id against configured
 90 |     # accounts. Never pass an unknown id through as if it resolved, and
 91 |     # accept the account email as an alias for the id (Defect 6).
 92 |     configured = [a for a in list_accounts() if a["configured"]]
 93 |     if account:
 94 |         needle = account.strip().lower()
 95 |         for a in configured:
 96 |             if a["account"].lower() == needle:
 97 |                 return a["account"]
 98 |         for a in configured:
 99 |             email = (a.get("email") or "").lower()
100 |             if email and email == needle:
101 |                 return a["account"]
102 |         return ""
103 |     if len(configured) == 1:
104 |         return configured[0]["account"]
105 |     return ""
106 | 
107 | 
108 | def connector_for(account: str = "") -> Optional[ImapMailConnector]:
109 |     """Build a connector for a configured account, or None."""
110 |     resolved = _resolve_account(account)
111 |     if not resolved:
112 |         return None
113 |     path = _CONNECTOR_DIR / ("%s%s.json" % (_PREFIX, resolved))
114 |     tokens = load_tokens(str(path)) or {}
115 |     provider = tokens.get("provider", "generic")
116 |     if provider not in PROVIDERS:
117 |         provider = "generic"
118 |     return ImapMailConnector(
119 |         provider=provider,
120 |         account_id=resolved,
121 |         credentials_path=str(path),
122 |         imap_host=tokens.get("host", ""),
123 |     )
124 | 
125 | 
126 | def _dump(payload: Any) -> str:
127 |     """Serialize a tool payload as JSON text."""
128 |     return json.dumps(payload, indent=2, default=str)
129 | 
130 | 
131 | def _no_account_result(name: str, account: str) -> ToolResult:
132 |     """Uniform failure when no usable account was resolved."""
133 |     known = list_accounts()
134 |     return ToolResult(
135 |         tool_name=name,
136 |         content=_dump(
137 |             {
138 |                 "error": (
139 |                     "no configured mailbox account matched %r" % account
140 |                     if account
141 |                     else "no account specified and more than one (or zero) is configured"
142 |                 ),
143 |                 "known_accounts": known,
144 |                 "hint": "run setup_mailbox_account.py to configure an account",
145 |             }
146 |         ),
147 |         success=False,
148 |     )
149 | 
150 | 
151 | # ---------------------------------------------------------------------------
152 | # read-only tools
153 | # ---------------------------------------------------------------------------
154 | 
155 | 
156 | @ToolRegistry.register("mailbox_list_accounts")
157 | class MailboxListAccountsTool(BaseTool):
158 |     """List configured mailbox accounts."""
159 | 
160 |     tool_id = "mailbox_list_accounts"
161 |     is_local = True
162 | 
163 |     @property
164 |     def spec(self) -> ToolSpec:
165 |         return ToolSpec(
166 |             name="mailbox_list_accounts",
167 |             description=(
168 |                 "List the configured mailbox accounts and their providers. "
169 |                 "Call this first when the user does not name an account."
170 |             ),
171 |             parameters={"type": "object", "properties": {}},
172 |             category="communication",
173 |             latency_estimate=0.1,
174 |             timeout_seconds=15.0,
175 |         )
176 | 
177 |     def execute(self, **params: Any) -> ToolResult:
178 |         return ToolResult(
179 |             tool_name=self.tool_id,
180 |             content=_dump({"accounts": list_accounts()}),
181 |             success=True,
182 |         )
183 | 
184 | 
185 | @ToolRegistry.register("mailbox_usage_report")
186 | class MailboxUsageReportTool(BaseTool):
187 |     """Report what is consuming mailbox storage."""
188 | 
189 |     tool_id = "mailbox_usage_report"
190 |     is_local = True
191 | 
192 |     @property
193 |     def spec(self) -> ToolSpec:
194 |         return ToolSpec(
195 |             name="mailbox_usage_report",
196 |             description=(
197 |                 "Report what is consuming storage in a mailbox: total size, "
198 |                 "size per folder, the senders responsible for the most bytes, "
199 |                 "and the largest individual messages. Reads message headers "
200 |                 "and sizes only, never message bodies. Use this to answer "
201 |                 "questions about a mailbox being full or over quota. ALSO use "
202 |                 "this whenever the user asks WHO is sending them mail, which "
203 |                 "senders or domains are cluttering the mailbox, or asks for a "
204 |                 "list of senders to review, classify, or approve - it is the "
205 |                 "correct first call for any such question. Raise top_senders "
206 |                 "to 40 or more when the user wants a list to review. "
207 |                 "openjarvis-sender-discovery-v1"
208 |             ),
209 |             parameters={
210 |                 "type": "object",
211 |                 "properties": {
212 |                     "account": {
213 |                         "type": "string",
214 |                         "description": "Account name; omit if only one is configured",
215 |                     },
216 |                     "top_senders": {"type": "integer", "default": 15},
217 |                     "top_messages": {"type": "integer", "default": 25},
218 |                 },
219 |             },
220 |             category="communication",
221 |             latency_estimate=30.0,
222 |             timeout_seconds=600.0,
223 |             required_capabilities=["mail.read"],
224 |         )
225 | 
226 |     def execute(self, **params: Any) -> ToolResult:
227 |         account = str(params.get("account", "") or "")
228 |         conn = connector_for(account)
229 |         if conn is None:
230 |             return _no_account_result(self.tool_id, account)
231 |         try:
232 |             report = conn.usage_report(
233 |                 top_senders=int(params.get("top_senders", 15) or 15),
234 |                 top_messages=int(params.get("top_messages", 25) or 25),
235 |             )
236 |         except Exception as exc:
237 |             logger.exception("mailbox_usage_report failed")
238 |             return ToolResult(
239 |                 tool_name=self.tool_id,
240 |                 content=_dump({"error": str(exc)}),
241 |                 success=False,
242 |             )
243 |         return ToolResult(
244 |             tool_name=self.tool_id,
245 |             content=_dump(report),
246 |             success="error" not in report,
247 |         )
248 | 
249 | 
250 | # openjarvis-find-summary-v1 openjarvis-find-spec-v1
251 | @ToolRegistry.register("mailbox_find_messages")
252 | class MailboxFindMessagesTool(BaseTool):
253 |     """Find messages by sender, subject, size, or age."""
254 | 
255 |     tool_id = "mailbox_find_messages"
256 |     is_local = True
257 | 
258 |     @property
259 |     def spec(self) -> ToolSpec:
260 |         return ToolSpec(
261 |             name="mailbox_find_messages",
262 |             description=(
263 |                 "Find messages in a mailbox by sender address, subject text, "
264 |                 "minimum size in bytes, or age in days. Defaults to "
265 |                 "detail=summary, which returns counts grouped by sender and "
266 |                 "folder. Summary is a complete and authoritative answer to "
267 |                 "how many, from whom, and which folder. Do NOT call this "
268 |                 "tool a second time with detail=full to confirm or expand a "
269 |                 "count you already have. Use detail=full only when you are "
270 |                 "about to move or delete specific messages and need their "
271 |                 "uids to do it. from_addr is OPTIONAL: OMIT it entirely to "
272 |                 "enumerate senders rather than confirm one. An unfiltered "
273 |                 "summary call returns by_address rows for every sender in the "
274 |                 "search window, which answers who is sending mail and how "
275 |                 "much. NEVER guess a sender name to search for - if the user "
276 |                 "has not named one, omit from_addr or call "
277 |                 "mailbox_usage_report instead."
278 |             ),
279 |             parameters={
280 |                 "type": "object",
281 |                 "properties": {
282 |                     "account": {"type": "string"},
283 |                     "folder": {
284 |                         "type": "string",
285 |                         "description": "Restrict to one folder; omit to search all",
286 |                     },
287 |                     "from_addr": {
288 |                         "type": "string",
289 |                         "description": "Substring match on the sender address",
290 |                     },
291 |                     "subject": {
292 |                         "type": "string",
293 |                         "description": "Substring match on the subject",
294 |                     },
295 |                     "larger_than_bytes": {"type": "integer", "default": 0},
296 |                     "older_than_days": {
297 |                         "type": "integer",
298 |                         "default": 0,
299 |                         "description": "Only messages older than this many days",
300 |                     },
301 |                     "limit": {"type": "integer", "default": 5000},
302 |                     "detail": {
303 |                         "type": "string",
304 |                         "enum": ["summary", "full"],
305 |                         "default": "summary",
306 |                         "description": (
307 |                             "summary returns counts grouped by sender and "
308 |                             "folder and is sufficient for every counting or "
309 |                             "location question; full returns every message "
310 |                             "object including uids and is only for when you "
311 |                             "need uids to act on messages"
312 |                         ),
313 |                     },
314 |                 },
315 |             },
316 |             category="communication",
317 |             latency_estimate=20.0,
318 |             timeout_seconds=600.0,
319 |             required_capabilities=["mail.read"],
320 |         )
321 | 
322 |     def execute(self, **params: Any) -> ToolResult:
323 |         account = str(params.get("account", "") or "")
324 |         conn = connector_for(account)
325 |         if conn is None:
326 |             return _no_account_result(self.tool_id, account)
327 | 
328 |         before: Optional[datetime] = None
329 |         try:
330 |             limit = int(params.get("limit", 5000) or 5000)
331 |         except (TypeError, ValueError):
332 |             limit = 5000
333 |         if limit <= 0:
334 |             limit = 5000
335 |         detail = str(params.get("detail", "summary") or "summary").lower()
336 |         if detail not in ("summary", "full"):
337 |             detail = "summary"
338 |         try:
339 |             days = int(params.get("older_than_days", 0) or 0)
340 |         except (TypeError, ValueError):
341 |             days = 0
342 |         if days > 0:
343 |             before = datetime.now() - timedelta(days=days)
344 | 
345 |         try:
346 |             hits = conn.find_messages(
347 |                 folder=str(params.get("folder", "") or ""),
348 |                 from_addr=str(params.get("from_addr", "") or ""),
349 |                 subject=str(params.get("subject", "") or ""),
350 |                 larger_than_bytes=int(params.get("larger_than_bytes", 0) or 0),
351 |                 before=before,
352 |                 limit=limit,
353 |             )
354 |         except Exception as exc:
355 |             logger.exception("mailbox_find_messages failed")
356 |             return ToolResult(
357 |                 tool_name=self.tool_id,
358 |                 content=_dump({"error": str(exc)}),
359 |                 success=False,
360 |             )
361 | 
362 |         total = sum(h["bytes"] for h in hits)
363 |         truncated = len(hits) >= limit
364 |         by_address: Dict[str, Dict[str, Any]] = {}
365 |         by_folder: Dict[str, Dict[str, Any]] = {}
366 |         for h in hits:
367 |             addr = str(h.get("from_addr", "") or "")
368 |             fold = str(h.get("folder", "") or "")
369 |             size = int(h.get("bytes", 0) or 0)
370 |             row_a = by_address.setdefault(
371 |                 addr, {"from_addr": addr, "count": 0, "bytes": 0}
372 |             )
373 |             row_a["count"] += 1
374 |             row_a["bytes"] += size
375 |             row_f = by_folder.setdefault(
376 |                 fold, {"folder": fold, "count": 0, "bytes": 0}
377 |             )
378 |             row_f["count"] += 1
379 |             row_f["bytes"] += size
380 |         payload: Dict[str, Any] = {
381 |             "match_count": len(hits),
382 |             "total_matched": len(hits),
383 |             "total_bytes": total,
384 |             "limit": limit,
385 |             "truncated": truncated,
386 |             "detail": detail,
387 |             "by_address": sorted(by_address.values(), key=lambda r: -r["count"]),
388 |             "by_folder": sorted(by_folder.values(), key=lambda r: -r["count"]),
389 |             "coverage": "newest ~10000 per folder (IMAP server window)",  # openjarvis-find-window-v1
390 |         }
391 |         notes = [
392 |             "COUNTS ARE WINDOWED. The mail server exposes only the newest "
393 |             "~10,000 messages per folder and does not index past them. "
394 |             "match_count is therefore a FLOOR within that window and is NEVER "
395 |             "a mailbox total. When reporting a count, say plainly that it "
396 |             "covers only the most recent mail the server exposes. Do not claim "
397 |             "all matching mail was found, moved, or deleted."
398 |         ]
399 |         if truncated:
400 |             notes.append(
401 |                 "RESULT ALSO TRUNCATED AT THE RESULT LIMIT, below even the "
402 |                 "server window. Re-run with a higher limit before acting."
403 |             )
404 |         payload["note"] = " ".join(notes)
405 |         if detail == "full":
406 |             payload["matches"] = hits
407 |         return ToolResult(
408 |             tool_name=self.tool_id,
409 |             content=_dump(payload),
410 |             success=True,
411 |         )
412 | 
413 | 
414 | # ---------------------------------------------------------------------------
415 | # destructive tools - dry run by default, explicit token to apply
416 | # ---------------------------------------------------------------------------
417 | 
418 | 
419 | def _confirmed(params: Dict[str, Any]) -> bool:
420 |     """True only when the caller explicitly asked to apply."""
421 |     dry_run = params.get("dry_run", True)
422 |     if isinstance(dry_run, str):
423 |         dry_run = dry_run.strip().lower() not in ("false", "0", "no")
424 |     if dry_run:
425 |         return False
426 |     return str(params.get("confirm", "")).strip() == CONFIRM_TOKEN
427 | 
428 | 
429 | def _needs_confirmation_result(name: str, plan: Any) -> ToolResult:
430 |     """Return the plan plus instructions for how to actually apply it."""
431 |     return ToolResult(
432 |         tool_name=name,
433 |         content=_dump(
434 |             {
435 |                 "status": "dry_run",
436 |                 "plan": plan,
437 |                 "to_apply": {
438 |                     "dry_run": False,
439 |                     "confirm": CONFIRM_TOKEN,
440 |                 },
441 |                 "instruction": (
442 |                     "Nothing was changed. Show this plan to the user and ask "
443 |                     "them to approve it. Only if they explicitly approve, call "
444 |                     "this tool again with dry_run=false and confirm set to the "
445 |                     "exact string above."
446 |                 ),
447 |             }
448 |         ),
449 |         success=True,
450 |     )
451 | 
452 | 
453 | @ToolRegistry.register("mailbox_move_to_trash")
454 | class MailboxMoveToTrashTool(BaseTool):
455 |     """Move specific messages to the trash folder."""
456 | 
457 |     tool_id = "mailbox_move_to_trash"
458 |     is_local = True
459 | 
460 |     @property
461 |     def spec(self) -> ToolSpec:
462 |         return ToolSpec(
463 |             name="mailbox_move_to_trash",
464 |             description=(
465 |                 "Move specific messages to the mailbox trash folder. "
466 |                 "DESTRUCTIVE. Defaults to a dry run that reports exactly what "
467 |                 "would move and changes nothing. To actually move messages you "
468 |                 "must pass dry_run=false AND confirm='" + CONFIRM_TOKEN + "'. "
469 |                 "Never pass those without the user's explicit approval of a "
470 |                 "dry-run plan you have already shown them. Note that trash "
471 |                 "still counts against quota until it is emptied."
472 |             ),
473 |             parameters={
474 |                 "type": "object",
475 |                 "properties": {
476 |                     "account": {"type": "string"},
477 |                     "folder": {
478 |                         "type": "string",
479 |                         "description": "Folder the messages currently live in",
480 |                     },
481 |                     "uids": {
482 |                         "type": "array",
483 |                         "items": {"type": "string"},
484 |                         "description": (
485 |                             "Message uids from mailbox_find_messages. Omit this "
486 |                             "and pass from_addr instead for anything larger than "
487 |                             "a handful of messages."
488 |                         ),
489 |                     },
490 |                     "from_addr": {
491 |                         "type": "string",
492 |                         "description": (
493 |                             "Sender substring, e.g. 'microcenter'. When given, "
494 |                             "the tool finds the matching messages in the named "
495 |                             "folder itself and moves them. Preferred over uids. "
496 |                             "Do not pass both."
497 |                         ),
498 |                     },
499 |                     "dry_run": {"type": "boolean", "default": True},
500 |                     "confirm": {
501 |                         "type": "string",
502 |                         "description": "Must be '" + CONFIRM_TOKEN + "' to apply",
503 |                     },
504 |                 },
505 |                 "required": ["folder"],
506 |             },
507 |             category="communication",
508 |             latency_estimate=5.0,
509 |             timeout_seconds=1800.0,  # openjarvis-tool-timeout-v1
510 |             required_capabilities=["mail.write"],
511 |         )
512 | 
513 |     def execute(self, **params: Any) -> ToolResult:
514 |         account = str(params.get("account", "") or "")
515 |         conn = connector_for(account)
516 |         if conn is None:
517 |             return _no_account_result(self.tool_id, account)
518 | 
519 |         folder = str(params.get("folder", "") or "")
520 | 
521 |         # openjarvis-filter-move-v1
522 |         # Server-side selection. The model passes a sender substring; the tool
523 |         # resolves it to uids here so no uid list ever crosses the model.
524 |         _from_addr = str(params.get("from_addr", "") or "").strip()
525 |         _resolved = 0
526 |         _blocked_report = {}
527 |         if _from_addr:
528 |             if params.get("uids"):
529 |                 return ToolResult(
530 |                     tool_name=self.tool_id,
531 |                     content=_dump({
532 |                         "error": (
533 |                             "Pass either from_addr or uids, not both. Use "
534 |                             "from_addr and let the tool select the messages."
535 |                         )
536 |                     }),
537 |                     success=False,
538 |                 )
539 |             if not folder:
540 |                 return ToolResult(
541 |                     tool_name=self.tool_id,
542 |                     content=_dump({"error": "folder is required when using from_addr"}),
543 |                     success=False,
544 |                 )
545 |             try:
546 |                 _hits = conn.find_messages(folder=folder, from_addr=_from_addr, limit=5000)  # openjarvis-h2-folder-scope-v1
547 |             except Exception as exc:
548 |                 logger.exception("mailbox_move_to_trash from_addr lookup failed")
549 |                 return ToolResult(
550 |                     tool_name=self.tool_id,
551 |                     content=_dump({"error": "sender lookup failed: %s" % exc}),
552 |                     success=False,
553 |                 )
554 |             _sel = []
555 |             for _h in _hits or []:
556 |                 if not isinstance(_h, dict):
557 |                     continue
558 |                 if str(_h.get("folder", "") or "") != folder:
559 |                     continue
560 |                 _u = str(_h.get("uid", "") or "").strip()
561 |                 if _u.isdigit():
562 |                     _sel.append(_u)
563 |             # openjarvis-protected-senders-v1
564 |             import json as _json
565 |             from pathlib import Path as _Path
566 |             _defaults = ['stackcommerce.com', 'cdgray33@yahoo.com',
567 |                 'notify@r.groupon.com', 'orders@r.groupon.com',
568 |                 'verify@r.groupon.com', 'otp@r.groupon.com',
569 |                 'orders@sidedeal', 'account@', 'ratings@',
570 |                 'noreply@service.wayfair.com']
571 |             _prot = _defaults
572 |             try:
573 |                 _pf = _Path.cwd() / 'protected_senders.json'
574 |                 if _pf.is_file():
575 |                     _ld = _json.loads(_pf.read_text(encoding='utf-8'))
576 |                     if isinstance(_ld, list) and _ld:
577 |                         _prot = [str(x).lower() for x in _ld if str(x).strip()]
578 |             except Exception:
579 |                 logger.exception('protected_senders.json unreadable; using built-in list')
580 |             _keep = []
581 |             for _h in _hits or []:
582 |                 if not isinstance(_h, dict):
583 |                     continue
584 |                 if str(_h.get('folder', '') or '') != folder:
585 |                     continue
586 |                 _u2 = str(_h.get('uid', '') or '').strip()
587 |                 if not _u2.isdigit():
588 |                     continue
589 |                 _a = str(_h.get('from_addr', '') or '').lower()
590 |                 _m = ''
591 |                 for _p in _prot:
592 |                     if _p and _p in _a:
593 |                         _m = _p
594 |                         break
595 |                 if _m:
596 |                     _blocked_report[_a] = _blocked_report.get(_a, 0) + 1
597 |                 else:
598 |                     _keep.append(_u2)
599 |             _sel = _keep
600 |             if _blocked_report:
601 |                 logger.warning('protected senders blocked from move: %s', _blocked_report)
602 |             if _blocked_report and not _sel:
603 |                 return ToolResult(
604 |                     tool_name=self.tool_id,
605 |                     content=_dump({
606 |                         'error': 'all matched messages are from protected senders; nothing moved',
607 |                         'protected_blocked': _blocked_report,
608 |                         'from_addr': _from_addr,
609 |                         'folder': folder,
610 |                     }),
611 |                     success=False,
612 |                 )
613 |             if not _sel:
614 |                 return ToolResult(
615 |                     tool_name=self.tool_id,
616 |                     content=_dump({
617 |                         "error": "no messages matched",
618 |                         "from_addr": _from_addr,
619 |                         "folder": folder,
620 |                         "searched": len(_hits or []),
621 |                     }),
622 |                     success=False,
623 |                 )
624 |             params["uids"] = _sel
625 |             _resolved = len(_sel)
626 | 
627 |         # openjarvis-uid-typeguard-v1
628 |         uids = params.get("uids")
629 |         if isinstance(uids, (str, bytes)) or not isinstance(uids, (list, tuple)):
630 |             return ToolResult(
631 |                 tool_name=self.tool_id,
632 |                 content=_dump({
633 |                     "error": (
634 |                         "uids must be a JSON array of numeric uid strings taken "
635 |                         "from a prior mailbox_find_messages result. A string was "
636 |                         "rejected. Do not construct uids yourself."
637 |                     ),
638 |                     "received_type": type(uids).__name__,
639 |                 }),
640 |                 success=False,
641 |             )
642 |         uids = [str(u).strip() for u in uids]
643 |         _bad = [u for u in uids if not u.isdigit()]
644 |         if _bad:
645 |             return ToolResult(
646 |                 tool_name=self.tool_id,
647 |                 content=_dump({
648 |                     "error": (
649 |                         "uids must be numeric strings from mailbox_find_messages. "
650 |                         "Non-numeric values were rejected and nothing was moved."
651 |                     ),
652 |                     "invalid_sample": _bad[:5],
653 |                     "invalid_count": len(_bad),
654 |                 }),
655 |                 success=False,
656 |             )
657 | 
658 |         if not folder or not uids:
659 |             return ToolResult(
660 |                 tool_name=self.tool_id,
661 |                 content=_dump({"error": "folder and a non-empty uids list are required"}),
662 |                 success=False,
663 |             )
664 | 
665 |         try:
666 |             if not _confirmed(params):
667 |                 plan = conn.move_to_trash(folder, uids, dry_run=True)
668 |                 return _needs_confirmation_result(self.tool_id, plan)
669 |             result = conn.move_to_trash(folder, uids, dry_run=False)
670 |         except Exception as exc:
671 |             logger.exception("mailbox_move_to_trash failed")
672 |             return ToolResult(
673 |                 tool_name=self.tool_id,
674 |                 content=_dump({"error": str(exc)}),
675 |                 success=False,
676 |             )
677 | 
678 |         if _resolved and isinstance(result, dict):
679 |             result = dict(result)
680 |             result["selected_by"] = "from_addr"
681 |             if _blocked_report:
682 |                 result["protected_blocked"] = _blocked_report
683 |             result["from_addr"] = _from_addr
684 |             result["resolved_uid_count"] = _resolved
685 | 
686 |         # openjarvis-h1-result-contract-v1
687 |         # move_to_trash has FOUR outcomes. Projecting them onto bool(applied)
688 |         # reports B as success and reports C as failure while messages are
689 |         # already sitting in trash, which invites a duplicating retry.
690 |         _requested = len(uids)
691 |         if isinstance(result, dict):
692 |             _copied = int(result.get("copied_count") or 0)
693 |             _deleted = int(result.get("deleted_count") or 0)
694 |             _failed = list(result.get("failed_uids") or [])
695 |             _store_failed = list(result.get("store_failed") or [])
696 |         else:
697 |             _copied = _deleted = 0
698 |             _failed = _store_failed = []
699 | 
700 |         if _copied == 0:
701 |             _outcome = "no_op"
702 |         elif _deleted == 0:
703 |             _outcome = "copied_not_removed"
704 |         elif _failed or _store_failed or _deleted != _requested:
705 |             _outcome = "partial"
706 |         else:
707 |             _outcome = "complete"
708 | 
709 |         if isinstance(result, dict):
710 |             result = dict(result)
711 |             result["outcome"] = _outcome
712 |             result["requested_count"] = _requested
713 |             if _outcome == "copied_not_removed":
714 |                 result["retry_unsafe"] = True
715 |                 result["warning"] = (
716 |                     "%d message(s) were COPIED into the trash folder but NOT "
717 |                     "removed from %r. They now exist in BOTH places. Do NOT "
718 |                     "retry this call - a retry copies them into trash a second "
719 |                     "time. Report this to the user and stop."
720 |                     % (_copied, folder)
721 |                 )
722 |             elif _outcome == "partial":
723 |                 result["retry_unsafe"] = False
724 |                 result["warning"] = (
725 |                     "Partial move: %d of %d message(s) were removed from %r. "
726 |                     "The remainder are still in place. This operation did NOT "
727 |                     "fully succeed - report the shortfall to the user."
728 |                     % (_deleted, _requested, folder)
729 |                 )
730 | 
731 |         return ToolResult(
732 |             tool_name=self.tool_id,
733 |             content=_dump(result),
734 |             success=(_outcome == "complete"),
735 |         )
736 | 
737 | 
738 | @ToolRegistry.register("mailbox_empty_folder")
739 | class MailboxEmptyFolderTool(BaseTool):
740 |     """Permanently delete every message in a folder."""
741 | 
742 |     tool_id = "mailbox_empty_folder"
743 |     is_local = True
744 | 
745 |     @property
746 |     def spec(self) -> ToolSpec:
747 |         return ToolSpec(
748 |             name="mailbox_empty_folder",
749 |             description=(
750 |                 "Permanently delete every message in a folder, normally the "
751 |                 "trash folder, to reclaim storage. IRREVERSIBLE AND "
752 |                 "DESTRUCTIVE. Defaults to a dry run reporting the exact "
753 |                 "message count and byte total. To actually delete you must "
754 |                 "pass dry_run=false AND confirm='" + CONFIRM_TOKEN + "'. Never "
755 |                 "pass those without the user's explicit approval of a dry-run "
756 |                 "plan you have already shown them."
757 |             ),
758 |             parameters={
759 |                 "type": "object",
760 |                 "properties": {
761 |                     "account": {"type": "string"},
762 |                     "folder": {
763 |                         "type": "string",
764 |                         "description": "Folder to empty, e.g. Trash",
765 |                     },
766 |                     "dry_run": {"type": "boolean", "default": True},
767 |                     "confirm": {
768 |                         "type": "string",
769 |                         "description": "Must be '" + CONFIRM_TOKEN + "' to apply",
770 |                     },
771 |                 },
772 |                 "required": ["folder"],
773 |             },
774 |             category="communication",
775 |             latency_estimate=10.0,
776 |             timeout_seconds=600.0,
777 |             required_capabilities=["mail.write"],
778 |         )
779 | 
780 |     def execute(self, **params: Any) -> ToolResult:
781 |         account = str(params.get("account", "") or "")
782 |         conn = connector_for(account)
783 |         if conn is None:
784 |             return _no_account_result(self.tool_id, account)
785 | 
786 |         folder = str(params.get("folder", "") or "")
787 |         if not folder:
788 |             return ToolResult(
789 |                 tool_name=self.tool_id,
790 |                 content=_dump({"error": "folder is required"}),
791 |                 success=False,
792 |             )
793 | 
794 |         try:
795 |             if not _confirmed(params):
796 |                 plan = conn.empty_folder(folder, dry_run=True)
797 |                 return _needs_confirmation_result(self.tool_id, plan)
798 |             result = conn.empty_folder(folder, dry_run=False)
799 |         except Exception as exc:
800 |             logger.exception("mailbox_empty_folder failed")
801 |             return ToolResult(
802 |                 tool_name=self.tool_id,
803 |                 content=_dump({"error": str(exc)}),
804 |                 success=False,
805 |             )
806 | 
807 |         return ToolResult(
808 |             tool_name=self.tool_id,
809 |             content=_dump(result),
810 |             success=bool(result.get("applied")),
811 |         )
812 | 
813 | 
814 | __all__ = [
815 |     "MailboxListAccountsTool",
816 |     "MailboxUsageReportTool",
817 |     "MailboxFindMessagesTool",
818 |     "MailboxMoveToTrashTool",
819 |     "MailboxEmptyFolderTool",
820 |     "connector_for",
821 |     "list_accounts",
822 | ]
```

---

# MANIFEST

| file | found | bytes | lines | sha256 |
|---|---|---|---|---|
| `./src/openjarvis/tools/mailbox_tools.py` | yes | 33666 | 822 | `4DB19C1EF90EEAB3...` |

These hashes pin the exact bytes you reviewed. If a later patch is built against different bytes, the mismatch is detectable.

