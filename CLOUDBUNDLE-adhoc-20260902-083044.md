# OPENJARVIS CODE REVIEW BUNDLE

- marker: `openjarvis-cloudbundle-v1`
- set: `adhoc` - ad hoc bundle
- generated: 2026-09-02T08:30:44
- repo root: `C:\Users\Admin\OpenJarvis`
- files in bundle: 2

You are reviewing complete source files. Every file is included in full, with authoritative 1-based line numbers in the left gutter. Nothing has been elided.

---

# THE QUESTION

Report CURRENT line numbers only, counted from the files as given in this bundle. Do not trust or reuse any line number from prior notes. Task: find every place in these two files where a multi-state operation result is collapsed into a single boolean or single flag. For each site give the current line number, the enclosing function, the exact expression, the distinguishable states being discarded, and whether a caller could be misled into an unsafe retry. Give particular attention to empty_folder and its expunge-based deletion path, and contrast its state space against the COPY-then-STORE path in move_to_trash.

---

# SOURCE

---

## FILE: `src/openjarvis/tools/mailbox_tools.py`

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

## FILE: `src/openjarvis/connectors/imap_mail.py`

- bytes: 34850
- lines: 901
- sha256: `B771AC1FF6DE4C34A17085BDE9F17935B74F58C1855DA6800455254C53538F67`
- line terminator: LF

Line numbers below are 1-based and authoritative. Cite them.

```python
  1 | """Provider-agnostic IMAP mail connector - Yahoo, Gmail, or any IMAP host.
  2 | 
  3 | Supersedes the read-only, INBOX-only ``gmail_imap`` connector for mailbox
  4 | work that needs to see and change the whole account:
  5 | 
  6 |   * every selectable folder, not just INBOX
  7 |   * size-aware enumeration via ``RFC822.SIZE`` plus header-only fetches,
  8 |     so quota questions are answered without downloading message bodies
  9 |   * UID-based mutation (move-to-trash, delete, empty folder) so that
 10 |     sequence-number shifts during EXPUNGE cannot delete the wrong mail
 11 | 
 12 | Authentication is an app password over IMAP4_SSL. No OAuth, no
 13 | dependencies outside the standard library.
 14 | 
 15 |   Yahoo app password : https://login.yahoo.com/account/security
 16 |   Gmail app password : https://myaccount.google.com/apppasswords
 17 | 
 18 | Provider differences that this module handles for you:
 19 | 
 20 |   * Gmail's "All Mail" mirrors every other folder, so it is excluded
 21 |     from usage totals by default to avoid double counting.
 22 |   * On Gmail, setting ``\\Deleted`` on a label only unlabels the
 23 |     message. Space is reclaimed only by copying to ``[Gmail]/Trash``
 24 |     and then emptying it. ``move_to_trash`` does the provider-correct
 25 |     thing for both backends.
 26 | 
 27 | EVERY destructive method defaults to ``dry_run=True`` and returns a plan
 28 | describing what it would do. Nothing is removed until it is called again
 29 | with ``dry_run=False``.
 30 | """
 31 | 
 32 | from __future__ import annotations
 33 | 
 34 | import email as email_lib
 35 | import imaplib
 36 | import logging
 37 | import re
 38 | from collections import defaultdict
 39 | from datetime import datetime
 40 | from email.header import decode_header
 41 | from email.utils import parsedate_to_datetime, parseaddr
 42 | from typing import Any, Dict, Iterator, List, Optional, Sequence, Tuple
 43 | 
 44 | from openjarvis.connectors._stubs import BaseConnector, Document, SyncStatus
 45 | from openjarvis.connectors.oauth import delete_tokens, load_tokens, save_tokens
 46 | from openjarvis.core.config import DEFAULT_CONFIG_DIR
 47 | from openjarvis.core.registry import ConnectorRegistry
 48 | from openjarvis.tools._stubs import ToolSpec
 49 | import time
 50 | 
 51 | logger = logging.getLogger(__name__)
 52 | 
 53 | _DEFAULT_CREDENTIALS_PATH = str(DEFAULT_CONFIG_DIR / "connectors" / "imap_mail.json")
 54 | 
 55 | # Per-provider defaults. ``trash`` is where deleted mail must land for the
 56 | # space to actually be reclaimed; ``exclude`` folders are skipped in usage
 57 | # totals because they mirror other folders.
 58 | PROVIDERS: Dict[str, Dict[str, Any]] = {
 59 |     "yahoo": {
 60 |         "host": "imap.mail.yahoo.com",
 61 |         "port": 993,
 62 |         "trash": "Trash",
 63 |         "exclude": (),
 64 |         "app_password_url": "https://login.yahoo.com/account/security",
 65 |     },
 66 |     "gmail": {
 67 |         "host": "imap.gmail.com",
 68 |         "port": 993,
 69 |         "trash": "[Gmail]/Trash",
 70 |         "exclude": ("[Gmail]/All Mail",),
 71 |         "app_password_url": "https://myaccount.google.com/apppasswords",
 72 |     },
 73 |     "generic": {
 74 |         "host": "",
 75 |         "port": 993,
 76 |         "trash": "Trash",
 77 |         "exclude": (),
 78 |         "app_password_url": "",
 79 |     },
 80 | }
 81 | 
 82 | # (\HasNoChildren) "/" "INBOX"
 83 | _LIST_RE = re.compile(
 84 |     rb'\((?P<flags>[^)]*)\)\s+"?(?P<delim>[^"\s]*)"?\s+(?P<name>.*)'
 85 | )
 86 | 
 87 | _HEADER_FIELDS = "(FROM TO SUBJECT DATE MESSAGE-ID)"
 88 | 
 89 | 
 90 | def _decode_header_value(raw: str) -> str:
 91 |     """Decode a possibly RFC2047-encoded header into plain text."""
 92 |     if not raw:
 93 |         return ""
 94 |     try:
 95 |         parts = decode_header(raw)
 96 |     except Exception:
 97 |         return raw
 98 |     return "".join(
 99 |         part.decode(enc or "utf-8", errors="replace") if isinstance(part, bytes) else part
100 |         for part, enc in parts
101 |     )
102 | 
103 | 
104 | def _extract_text_body(msg: email_lib.message.Message) -> str:
105 |     """Extract a plain-text body, falling back to text/html."""
106 |     if msg.is_multipart():
107 |         for wanted in ("text/plain", "text/html"):
108 |             for part in msg.walk():
109 |                 if part.get_content_type() == wanted:
110 |                     payload = part.get_payload(decode=True)
111 |                     if payload:
112 |                         return payload.decode("utf-8", errors="replace")
113 |         return ""
114 |     payload = msg.get_payload(decode=True)
115 |     if payload:
116 |         return payload.decode("utf-8", errors="replace")
117 |     return ""
118 | 
119 | 
120 | def _parse_date(msg: email_lib.message.Message) -> datetime:
121 |     """Parse the Date header, falling back to now."""
122 |     raw = msg.get("Date", "")
123 |     if not raw:
124 |         return datetime.now()
125 |     try:
126 |         return parsedate_to_datetime(raw)
127 |     except Exception:
128 |         return datetime.now()
129 | 
130 | 
131 | def _quote_folder(name: str) -> str:
132 |     """Quote a folder name for SELECT. IMAP names may contain spaces."""
133 |     return '"%s"' % name.replace('"', '\\"')
134 | 
135 | 
136 | def _human_bytes(n: int) -> str:
137 |     """Render a byte count for display in tool output."""
138 |     step = 1024.0
139 |     value = float(n)
140 |     for unit in ("B", "KB", "MB", "GB"):
141 |         if value < step or unit == "GB":
142 |             return "%.1f %s" % (value, unit)
143 |         value /= step
144 |     return "%.1f GB" % value
145 | 
146 | 
147 | @ConnectorRegistry.register("imap_mail")
148 | class ImapMailConnector(BaseConnector):
149 |     """IMAP mail connector with folder enumeration, sizing, and mutation.
150 | 
151 |     Instantiate one per account::
152 | 
153 |         yahoo = ConnectorRegistry.create(
154 |             "imap_mail", provider="yahoo", account_id="yahoo_main",
155 |         )
156 |         gmail = ConnectorRegistry.create(
157 |             "imap_mail", provider="gmail", account_id="agent_gmail",
158 |         )
159 | 
160 |     Credentials resolve from the constructor first, then from
161 |     ``~/.openjarvis/connectors/imap_mail_<account_id>.json``.
162 |     """
163 | 
164 |     connector_id = "imap_mail"
165 |     display_name = "Mail (IMAP)"
166 |     auth_type = "local"
167 | 
168 |     def __init__(
169 |         self,
170 |         email_address: str = "",
171 |         app_password: str = "",
172 |         credentials_path: str = "",
173 |         *,
174 |         provider: str = "generic",
175 |         account_id: str = "",
176 |         imap_host: str = "",
177 |         imap_port: int = 0,
178 |         folders: Optional[Sequence[str]] = None,
179 |         trash_folder: str = "",
180 |         max_messages: Optional[int] = None,
181 |     ) -> None:
182 |         prov = PROVIDERS.get(provider.lower().strip(), PROVIDERS["generic"])
183 |         self._provider = provider.lower().strip() or "generic"
184 |         self._email = email_address
185 |         self._password = app_password
186 |         self._account_id = account_id or self._provider
187 |         self._credentials_path = credentials_path or str(
188 |             DEFAULT_CONFIG_DIR / "connectors" / ("imap_mail_%s.json" % self._account_id)
189 |         )
190 |         self._imap_host = imap_host or prov["host"]
191 |         self._imap_port = imap_port or prov["port"]
192 |         self._trash_folder = trash_folder or prov["trash"]
193 |         self._exclude_from_usage = tuple(prov["exclude"])
194 |         self._app_password_url = prov["app_password_url"]
195 |         # ``None`` means no cap. A positive value bounds enumeration,
196 |         # which is useful for a first look at a very large mailbox.
197 |         self._max_messages = max_messages
198 |         self._folders_filter = list(folders) if folders else None
199 |         self._items_synced = 0
200 |         self._items_total = 0
201 |         self._last_error: Optional[str] = None
202 | 
203 |     # ------------------------------------------------------------------
204 |     # credentials / BaseConnector contract
205 |     # ------------------------------------------------------------------
206 | 
207 |     def _resolve_credentials(self) -> Tuple[str, str]:
208 |         """Return (email, password). Constructor args take priority."""
209 |         if self._email and self._password:
210 |             return self._email, self._password
211 |         tokens = load_tokens(self._credentials_path)
212 |         if tokens:
213 |             return tokens.get("email", ""), tokens.get("password", "")
214 |         return "", ""
215 | 
216 |     def is_connected(self) -> bool:
217 |         em, pw = self._resolve_credentials()
218 |         return bool(em and pw and self._imap_host)
219 | 
220 |     def disconnect(self) -> None:
221 |         self._email = ""
222 |         self._password = ""
223 |         delete_tokens(self._credentials_path)
224 | 
225 |     def auth_url(self) -> str:
226 |         return self._app_password_url or "https://support.google.com/mail/answer/7126229"
227 | 
228 |     def handle_callback(self, code: str) -> None:
229 |         """Store credentials. ``code`` is ``"email:app_password"``."""
230 |         if ":" in code:
231 |             em, pw = code.split(":", 1)
232 |             save_tokens(
233 |                 self._credentials_path,
234 |                 {"email": em.strip(), "password": pw.strip()},
235 |             )
236 |         else:
237 |             save_tokens(self._credentials_path, {"email": "", "password": code.strip()})
238 | 
239 |     def sync_status(self) -> SyncStatus:
240 |         return SyncStatus(
241 |             state="error" if self._last_error else "idle",
242 |             items_synced=self._items_synced,
243 |             items_total=self._items_total,
244 |             error=self._last_error,
245 |         )
246 | 
247 |     # ------------------------------------------------------------------
248 |     # connection
249 |     # ------------------------------------------------------------------
250 | 
251 |     def _connect(self) -> Optional[imaplib.IMAP4_SSL]:
252 |         """Open and authenticate an IMAP connection, or return None."""
253 |         em, pw = self._resolve_credentials()
254 |         if not em or not pw:
255 |             self._last_error = "no credentials configured"
256 |             logger.error("imap_mail[%s]: no credentials configured", self._account_id)
257 |             return None
258 |         if not self._imap_host:
259 |             self._last_error = "no IMAP host configured"
260 |             logger.error("imap_mail[%s]: no IMAP host configured", self._account_id)
261 |             return None
262 |         try:
263 |             imap = imaplib.IMAP4_SSL(self._imap_host, self._imap_port)
264 |             imap.login(em, pw)
265 |         except (imaplib.IMAP4.error, OSError) as exc:
266 |             self._last_error = "login failed: %s" % exc
267 |             logger.error("imap_mail[%s] login failed: %s", self._account_id, exc)
268 |             return None
269 |         self._last_error = None
270 |         return imap
271 | 
272 |     @staticmethod
273 |     def _close(imap: imaplib.IMAP4_SSL) -> None:
274 |         """Close a connection without letting teardown raise."""
275 |         try:
276 |             imap.logout()
277 |         except Exception:
278 |             pass
279 | 
280 |     # ------------------------------------------------------------------
281 |     # folder enumeration
282 |     # ------------------------------------------------------------------
283 | 
284 |     def _list_folders(self, imap: imaplib.IMAP4_SSL) -> List[str]:
285 |         """Return every selectable folder name on the account."""
286 |         typ, data = imap.list()
287 |         if typ != "OK" or not data:
288 |             return []
289 |         names: List[str] = []
290 |         for line in data:
291 |             if not isinstance(line, bytes):
292 |                 continue
293 |             match = _LIST_RE.match(line)
294 |             if not match:
295 |                 continue
296 |             flags = match.group("flags").decode("utf-8", errors="replace")
297 |             if "\\Noselect" in flags:
298 |                 continue
299 |             raw = match.group("name").decode("utf-8", errors="replace").strip()
300 |             names.append(raw[1:-1] if raw.startswith('"') and raw.endswith('"') else raw)
301 |         return names
302 | 
303 |     def list_folders(self) -> List[str]:
304 |         """Public folder listing. Opens and closes its own connection."""
305 |         imap = self._connect()
306 |         if imap is None:
307 |             return []
308 |         try:
309 |             return self._list_folders(imap)
310 |         finally:
311 |             self._close(imap)
312 | 
313 |     def _target_folders(self, imap: imaplib.IMAP4_SSL, *, for_usage: bool) -> List[str]:
314 |         """Apply the configured folder filter and provider exclusions."""
315 |         folders = self._folders_filter or self._list_folders(imap)
316 |         if for_usage and self._exclude_from_usage:
317 |             folders = [f for f in folders if f not in self._exclude_from_usage]
318 |         return folders
319 | 
320 |     # ------------------------------------------------------------------
321 |     # sizing - the quota question
322 |     # ------------------------------------------------------------------
323 | 
324 |     def _fetch_summaries(
325 |         self,
326 |         imap: imaplib.IMAP4_SSL,
327 |         folder: str,
328 |         *,
329 |         limit: Optional[int] = None,
330 |     ) -> List[Dict[str, Any]]:
331 |         """Return per-message summaries for one folder.
332 | 
333 |         Fetches ``RFC822.SIZE`` plus a header-only peek. No message body
334 |         is transferred, so this stays cheap on very large mailboxes.
335 |         """
336 |         typ, _ = imap.select(_quote_folder(folder), readonly=True)
337 |         if typ != "OK":
338 |             logger.warning("imap_mail: cannot select folder %r", folder)
339 |             return []
340 | 
341 |         typ, data = imap.uid("SEARCH", None, "ALL")
342 |         if typ != "OK" or not data or not data[0]:
343 |             return []
344 |         uids = data[0].split()
345 |         if limit is not None and limit > 0:
346 |             uids = uids[-limit:]
347 |         if not uids:
348 |             return []
349 | 
350 |         summaries: List[Dict[str, Any]] = []
351 |         # Batch to keep command lines well inside server limits.
352 |         batch = 200
353 |         for start in range(0, len(uids), batch):
354 |             chunk = uids[start : start + batch]
355 |             uid_set = b",".join(chunk).decode("ascii")
356 |             typ, resp = imap.uid(
357 |                 "FETCH",
358 |                 uid_set,
359 |                 "(RFC822.SIZE BODY.PEEK[HEADER.FIELDS %s])" % _HEADER_FIELDS,
360 |             )
361 |             if typ != "OK" or not resp:
362 |                 continue
363 |             for item in resp:
364 |                 if not isinstance(item, tuple) or len(item) < 2:
365 |                     continue
366 |                 meta = item[0] if isinstance(item[0], bytes) else b""
367 |                 header_bytes = item[1] if isinstance(item[1], bytes) else b""
368 |                 uid_match = re.search(rb"UID\s+(\d+)", meta)
369 |                 size_match = re.search(rb"RFC822\.SIZE\s+(\d+)", meta)
370 |                 if not uid_match:
371 |                     continue
372 |                 msg = email_lib.message_from_bytes(header_bytes)
373 |                 sender_name, sender_addr = parseaddr(msg.get("From", ""))
374 |                 summaries.append(
375 |                     {
376 |                         "uid": uid_match.group(1).decode("ascii"),
377 |                         "folder": folder,
378 |                         "size_bytes": int(size_match.group(1)) if size_match else 0,
379 |                         "subject": _decode_header_value(msg.get("Subject", "")),
380 |                         "from_name": _decode_header_value(sender_name),
381 |                         "from_addr": (sender_addr or "").lower(),
382 |                         "date": _parse_date(msg),
383 |                         "message_id": msg.get("Message-ID", ""),
384 |                     }
385 |                 )
386 |         return summaries
387 | 
388 |     def usage_report(
389 |         self,
390 |         *,
391 |         top_senders: int = 15,
392 |         top_messages: int = 25,
393 |         per_folder_limit: Optional[int] = None,
394 |     ) -> Dict[str, Any]:
395 |         """Answer "what is filling up this mailbox".
396 | 
397 |         Returns folder totals, the heaviest senders by cumulative bytes,
398 |         and the single largest messages, all without downloading bodies.
399 |         """
400 |         imap = self._connect()
401 |         if imap is None:
402 |             return {"error": self._last_error, "folders": [], "account": self._account_id}
403 | 
404 |         try:
405 |             folders = self._target_folders(imap, for_usage=True)
406 |             all_rows: List[Dict[str, Any]] = []
407 |             folder_rows: List[Dict[str, Any]] = []
408 | 
409 |             for folder in folders:
410 |                 rows = self._fetch_summaries(imap, folder, limit=per_folder_limit)
411 |                 total = sum(r["size_bytes"] for r in rows)
412 |                 folder_rows.append(
413 |                     {
414 |                         "folder": folder,
415 |                         "messages": len(rows),
416 |                         "bytes": total,
417 |                         "human": _human_bytes(total),
418 |                     }
419 |                 )
420 |                 all_rows.extend(rows)
421 | 
422 |             by_sender: Dict[str, Dict[str, Any]] = defaultdict(
423 |                 lambda: {"messages": 0, "bytes": 0, "name": ""}
424 |             )
425 |             for row in all_rows:
426 |                 entry = by_sender[row["from_addr"] or "(unknown)"]
427 |                 entry["messages"] += 1
428 |                 entry["bytes"] += row["size_bytes"]
429 |                 if not entry["name"]:
430 |                     entry["name"] = row["from_name"]
431 | 
432 |             senders = sorted(
433 |                 (
434 |                     {
435 |                         "address": addr,
436 |                         "name": vals["name"],
437 |                         "messages": vals["messages"],
438 |                         "bytes": vals["bytes"],
439 |                         "human": _human_bytes(vals["bytes"]),
440 |                     }
441 |                     for addr, vals in by_sender.items()
442 |                 ),
443 |                 key=lambda d: d["bytes"],
444 |                 reverse=True,
445 |             )[:top_senders]
446 | 
447 |             largest = sorted(all_rows, key=lambda r: r["size_bytes"], reverse=True)
448 |             largest_out = [
449 |                 {
450 |                     "uid": r["uid"],
451 |                     "folder": r["folder"],
452 |                     "subject": r["subject"],
453 |                     "from_addr": r["from_addr"],
454 |                     "date": r["date"].isoformat(),
455 |                     "bytes": r["size_bytes"],
456 |                     "human": _human_bytes(r["size_bytes"]),
457 |                 }
458 |                 for r in largest[:top_messages]
459 |             ]
460 | 
461 |             grand_total = sum(r["size_bytes"] for r in all_rows)
462 |             self._items_total = len(all_rows)
463 |             return {
464 |                 "account": self._account_id,
465 |                 "provider": self._provider,
466 |                 "total_messages": len(all_rows),
467 |                 "total_bytes": grand_total,
468 |                 "total_human": _human_bytes(grand_total),
469 |                 "excluded_folders": list(self._exclude_from_usage),
470 |                 "folders": sorted(folder_rows, key=lambda d: d["bytes"], reverse=True),
471 |                 "top_senders": senders,
472 |                 "largest_messages": largest_out,
473 |             }
474 |         finally:
475 |             self._close(imap)
476 | 
477 |     def find_messages(
478 |         self,
479 |         *,
480 |         folder: str = "",
481 |         from_addr: str = "",
482 |         subject: str = "",
483 |         larger_than_bytes: int = 0,
484 |         before: Optional[datetime] = None,
485 |         limit: int = 200,
486 |     ) -> List[Dict[str, Any]]:
487 |         """Return message summaries matching the given criteria.
488 | 
489 |         The result rows carry ``folder`` and ``uid``, which is exactly
490 |         what the deletion methods take - so a search result can be handed
491 |         straight to ``move_to_trash`` without re-resolving anything.
492 |         """
493 |         imap = self._connect()
494 |         if imap is None:
495 |             return []
496 |         try:
497 |             folders = [folder] if folder else self._target_folders(imap, for_usage=True)
498 |             hits: List[Dict[str, Any]] = []
499 |             needle_from = (from_addr or "").lower().strip()
500 |             needle_subj = (subject or "").lower().strip()
501 | 
502 |             for name in folders:
503 |                 for row in self._fetch_summaries(imap, name):
504 |                     if needle_from and needle_from not in row["from_addr"]:
505 |                         continue
506 |                     if needle_subj and needle_subj not in row["subject"].lower():
507 |                         continue
508 |                     if larger_than_bytes and row["size_bytes"] < larger_than_bytes:
509 |                         continue
510 |                     if before is not None:
511 |                         stamp = row["date"]
512 |                         naive = stamp.replace(tzinfo=None) if stamp.tzinfo else stamp
513 |                         cutoff = before.replace(tzinfo=None) if before.tzinfo else before
514 |                         if naive >= cutoff:
515 |                             continue
516 |                     hits.append(
517 |                         {
518 |                             "uid": row["uid"],
519 |                             "folder": row["folder"],
520 |                             "subject": row["subject"],
521 |                             "from_addr": row["from_addr"],
522 |                             "date": row["date"].isoformat(),
523 |                             "bytes": row["size_bytes"],
524 |                             "human": _human_bytes(row["size_bytes"]),
525 |                         }
526 |                     )
527 |                     if len(hits) >= limit:
528 |                         return hits
529 |             return hits
530 |         finally:
531 |             self._close(imap)
532 | 
533 |     # ------------------------------------------------------------------
534 |     # mutation - every entry point is dry-run by default
535 |     # ------------------------------------------------------------------
536 | 
537 |     def move_to_trash(
538 |         self,
539 |         folder: str,
540 |         uids: Sequence[str],
541 |         *,
542 |         dry_run: bool = True,
543 |         chunk_size: int = 10,
544 |         pause_s: float = 1.0,
545 |         max_retries: int = 4,
546 |     ) -> Dict[str, Any]:
547 |         """Move messages to the provider's trash folder.
548 | 
549 |         This is the correct operation for reclaiming space. On Gmail a
550 |         bare ``\\Deleted`` flag only removes a label; the message has to
551 |         reach ``[Gmail]/Trash``. Trash still counts against quota until
552 |         it is emptied - see ``empty_folder``.
553 | 
554 |         Yahoo rate-limits bulk UID COPY and reports it inconsistently
555 |         (``[LIMIT]`` on large sets, ``[SERVERBUG]`` on small ones). Both
556 |         are transient, so copies are chunked, paced and retried. Messages
557 |         are only flagged ``\\Deleted`` after their COPY returned OK.
558 |         """
559 |         uids = [str(u) for u in uids]
560 |         plan = {
561 |             "action": "move_to_trash",
562 |             "account": self._account_id,
563 |             "folder": folder,
564 |             "trash": self._trash_folder,
565 |             "uid_count": len(uids),
566 |             "uids": list(uids),
567 |             "dry_run": dry_run,
568 |             "applied": False,
569 |         }
570 |         if not uids:
571 |             plan["note"] = "no uids supplied; nothing to do"
572 |             return plan
573 |         if dry_run:
574 |             plan["note"] = "DRY RUN. Re-run with dry_run=False to apply."
575 |             return plan
576 |         imap = self._connect()
577 |         if imap is None:
578 |             plan["error"] = self._last_error
579 |             return plan
580 |         try:
581 |             typ, _ = imap.select(_quote_folder(folder), readonly=False)
582 |             if typ != "OK":
583 |                 plan["error"] = "cannot select folder %r for writing" % folder
584 |                 return plan
585 | 
586 |             trash = self._trash_folder
587 |             copied = []
588 |             failed = []
589 |             errors = []
590 | 
591 |             if folder == trash:
592 |                 copied = list(uids)
593 |             else:
594 |                 qtrash = _quote_folder(trash)
595 |                 chunks = [uids[i:i + chunk_size]
596 |                           for i in range(0, len(uids), chunk_size)]
597 |                 for idx, chunk in enumerate(chunks):
598 |                     uid_set = ",".join(chunk)
599 |                     ok = False
600 |                     delay = pause_s
601 |                     for _attempt in range(max_retries):
602 |                         typ, data = imap.uid("COPY", uid_set, qtrash)
603 |                         if typ == "OK":
604 |                             ok = True
605 |                             break
606 |                         errors.append(self._imap_text(data))
607 |                         time.sleep(delay)
608 |                         delay *= 2
609 |                     if ok:
610 |                         copied.extend(chunk)
611 |                     else:
612 |                         # Chunk is still failing. Degrade to one UID at a
613 |                         # time so a single poisoned message cannot strand
614 |                         # the other nine.
615 |                         for u in chunk:
616 |                             t2, d2 = imap.uid("COPY", u, qtrash)
617 |                             if t2 == "OK":
618 |                                 copied.append(u)
619 |                             else:
620 |                                 failed.append(u)
621 |                                 errors.append(self._imap_text(d2))
622 |                             time.sleep(pause_s)
623 |                     if idx + 1 < len(chunks):
624 |                         time.sleep(pause_s)
625 | 
626 |             plan["copied_count"] = len(copied)
627 |             plan["failed_uids"] = failed
628 |             if errors:
629 |                 plan["copy_errors"] = errors[:10]
630 | 
631 |             if not copied:
632 |                 plan["error"] = "COPY to %r failed for all uids" % trash
633 |                 return plan
634 | 
635 |             deleted = 0
636 |             for i in range(0, len(copied), chunk_size):
637 |                 sub = copied[i:i + chunk_size]
638 |                 typ, _ = imap.uid("STORE", ",".join(sub), "+FLAGS", "(\\Deleted)")
639 |                 if typ == "OK":
640 |                     deleted += len(sub)
641 |                 else:
642 |                     plan.setdefault("store_failed", []).extend(sub)
643 |                 time.sleep(pause_s)
644 | 
645 |             imap.expunge()
646 |             plan["deleted_count"] = deleted
647 |             plan["applied"] = deleted > 0
648 |             if failed:
649 |                 plan["note"] = (
650 |                     "%d uid(s) could not be copied and were left in place"
651 |                     % len(failed)
652 |                 )
653 |             return plan
654 |         finally:
655 |             self._close(imap)
656 | 
657 |     @staticmethod
658 |     def _imap_text(data) -> str:
659 |         """Flatten an imaplib response payload into a readable string."""
660 |         try:
661 |             parts = []
662 |             for item in (data or []):
663 |                 if isinstance(item, bytes):
664 |                     parts.append(item.decode("utf-8", "replace"))
665 |                 elif item is not None:
666 |                     parts.append(str(item))
667 |             return " ".join(parts)
668 |         except Exception:
669 |             return repr(data)
670 | 
671 |     def empty_folder(self, folder: str, *, dry_run: bool = True) -> Dict[str, Any]:
672 |         """Permanently remove every message in a folder.
673 | 
674 |         Intended for the trash folder. This is irreversible - the dry run
675 |         reports the exact message count and byte total first.
676 |         """
677 |         plan = {
678 |             "action": "empty_folder",
679 |             "account": self._account_id,
680 |             "folder": folder,
681 |             "dry_run": dry_run,
682 |             "applied": False,
683 |         }
684 |         imap = self._connect()
685 |         if imap is None:
686 |             plan["error"] = self._last_error
687 |             return plan
688 |         try:
689 |             rows = self._fetch_summaries(imap, folder)
690 |             total = sum(r["size_bytes"] for r in rows)
691 |             plan["message_count"] = len(rows)
692 |             plan["bytes"] = total
693 |             plan["human"] = _human_bytes(total)
694 |             if not rows:
695 |                 plan["note"] = "folder already empty"
696 |                 return plan
697 |             if dry_run:
698 |                 plan["note"] = (
699 |                     "DRY RUN. Would permanently delete %d messages (%s). "
700 |                     "Re-run with dry_run=False to apply."
701 |                     % (len(rows), _human_bytes(total))
702 |                 )
703 |                 return plan
704 | 
705 |             typ, _ = imap.select(_quote_folder(folder), readonly=False)
706 |             if typ != "OK":
707 |                 plan["error"] = "cannot select folder %r for writing" % folder
708 |                 return plan
709 |             uid_set = ",".join(r["uid"] for r in rows)
710 |             typ, _ = imap.uid("STORE", uid_set, "+FLAGS", "(\\Deleted)")
711 |             if typ != "OK":
712 |                 plan["error"] = "STORE +FLAGS \\Deleted failed"
713 |                 return plan
714 |             imap.expunge()
715 |             plan["applied"] = True
716 |             return plan
717 |         finally:
718 |             self._close(imap)
719 | 
720 |     # ------------------------------------------------------------------
721 |     # ingestion
722 |     # ------------------------------------------------------------------
723 | 
724 |     def sync(
725 |         self,
726 |         *,
727 |         since: Optional[datetime] = None,
728 |         cursor: Optional[str] = None,
729 |     ) -> Iterator[Document]:
730 |         """Yield documents from every targeted folder, newest first.
731 | 
732 |         Like the gmail_imap connector this always enumerates fully and
733 |         relies on pipeline-level dedup, because IMAP has no cursor that
734 |         survives a server restart.
735 |         """
736 |         imap = self._connect()
737 |         if imap is None:
738 |             return
739 | 
740 |         try:
741 |             folders = self._target_folders(imap, for_usage=True)
742 |             synced = 0
743 |             total = 0
744 | 
745 |             for folder in folders:
746 |                 typ, _ = imap.select(_quote_folder(folder), readonly=True)
747 |                 if typ != "OK":
748 |                     continue
749 |                 typ, data = imap.uid("SEARCH", None, "ALL")
750 |                 if typ != "OK" or not data or not data[0]:
751 |                     continue
752 |                 uids = list(reversed(data[0].split()))
753 |                 total += len(uids)
754 |                 if self._max_messages is not None and self._max_messages > 0:
755 |                     uids = uids[: self._max_messages]
756 | 
757 |                 for uid in uids:
758 |                     try:
759 |                         typ, msg_data = imap.uid("FETCH", uid.decode("ascii"), "(RFC822)")
760 |                         if typ != "OK" or not msg_data or not isinstance(msg_data[0], tuple):
761 |                             continue
762 |                         msg = email_lib.message_from_bytes(msg_data[0][1])
763 |                     except Exception:
764 |                         continue
765 | 
766 |                     timestamp = _parse_date(msg)
767 |                     if since is not None:
768 |                         naive = timestamp.replace(tzinfo=None) if timestamp.tzinfo else timestamp
769 |                         floor = since.replace(tzinfo=None) if since.tzinfo else since
770 |                         if naive < floor:
771 |                             continue
772 | 
773 |                     subject = _decode_header_value(msg.get("Subject", ""))
774 |                     sender = msg.get("From", "")
775 |                     to = msg.get("To", "")
776 |                     message_id = msg.get("Message-ID", "") or "%s:%s" % (
777 |                         folder,
778 |                         uid.decode("ascii"),
779 |                     )
780 | 
781 |                     synced += 1
782 |                     yield Document(
783 |                         doc_id="imap_mail:%s:%s" % (self._account_id, message_id),
784 |                         source="imap_mail",
785 |                         doc_type="email",
786 |                         content=_extract_text_body(msg),
787 |                         title=subject,
788 |                         author=sender,
789 |                         participants=[a.strip() for a in (to or "").split(",") if a.strip()],
790 |                         timestamp=timestamp,
791 |                         thread_id=msg.get("In-Reply-To", ""),
792 |                         source_id=message_id,
793 |                         channel=folder,
794 |                         metadata={
795 |                             "message_id": message_id,
796 |                             "folder": folder,
797 |                             "uid": uid.decode("ascii"),
798 |                             "account": self._account_id,
799 |                             "provider": self._provider,
800 |                         },
801 |                     )
802 | 
803 |             self._items_synced = synced
804 |             self._items_total = total
805 |         finally:
806 |             self._close(imap)
807 | 
808 |     # ------------------------------------------------------------------
809 |     # declarative specs
810 |     # ------------------------------------------------------------------
811 | 
812 |     def mcp_tools(self) -> List[ToolSpec]:
813 |         """Declarative specs for the connector API surface.
814 | 
815 |         NOTE: specs returned here are enumerated by the connectors router
816 |         for display; they are NOT what the agent executes. Executable
817 |         tools must be BaseTool subclasses registered in ToolRegistry,
818 |         which is what MCPServer.get_tools() feeds to the agent builder.
819 |         """
820 |         return [
821 |             ToolSpec(
822 |                 name="mailbox_usage_report",
823 |                 description=(
824 |                     "Report what is consuming mailbox storage: totals per folder, "
825 |                     "heaviest senders, and largest individual messages."
826 |                 ),
827 |                 parameters={
828 |                     "type": "object",
829 |                     "properties": {
830 |                         "account": {"type": "string", "description": "Account id"},
831 |                         "top_senders": {"type": "integer", "default": 15},
832 |                         "top_messages": {"type": "integer", "default": 25},
833 |                     },
834 |                 },
835 |                 category="communication",
836 |                 latency_estimate=20.0,
837 |                 timeout_seconds=300.0,
838 |             ),
839 |             ToolSpec(
840 |                 name="mailbox_find_messages",
841 |                 description=(
842 |                     "Find messages by sender, subject, minimum size, or age. "
843 |                     "Returns folder and uid for each hit."
844 |                 ),
845 |                 parameters={
846 |                     "type": "object",
847 |                     "properties": {
848 |                         "account": {"type": "string"},
849 |                         "folder": {"type": "string"},
850 |                         "from_addr": {"type": "string"},
851 |                         "subject": {"type": "string"},
852 |                         "larger_than_bytes": {"type": "integer", "default": 0},
853 |                         "limit": {"type": "integer", "default": 200},
854 |                     },
855 |                 },
856 |                 category="communication",
857 |                 latency_estimate=15.0,
858 |                 timeout_seconds=300.0,
859 |             ),
860 |             ToolSpec(
861 |                 name="mailbox_move_to_trash",
862 |                 description=(
863 |                     "Move specific messages to trash. Destructive. Runs as a dry "
864 |                     "run unless explicitly confirmed."
865 |                 ),
866 |                 parameters={
867 |                     "type": "object",
868 |                     "properties": {
869 |                         "account": {"type": "string"},
870 |                         "folder": {"type": "string"},
871 |                         "uids": {"type": "array", "items": {"type": "string"}},
872 |                         "dry_run": {"type": "boolean", "default": True},
873 |                     },
874 |                     "required": ["folder", "uids"],
875 |                 },
876 |                 category="communication",
877 |                 requires_confirmation=True,
878 |                 required_capabilities=["mail.write"],
879 |                 timeout_seconds=120.0,
880 |             ),
881 |             ToolSpec(
882 |                 name="mailbox_empty_folder",
883 |                 description=(
884 |                     "Permanently delete every message in a folder, normally trash. "
885 |                     "Irreversible. Runs as a dry run unless explicitly confirmed."
886 |                 ),
887 |                 parameters={
888 |                     "type": "object",
889 |                     "properties": {
890 |                         "account": {"type": "string"},
891 |                         "folder": {"type": "string"},
892 |                         "dry_run": {"type": "boolean", "default": True},
893 |                     },
894 |                     "required": ["folder"],
895 |                 },
896 |                 category="communication",
897 |                 requires_confirmation=True,
898 |                 required_capabilities=["mail.write"],
899 |                 timeout_seconds=300.0,
900 |             ),
901 |         ]
```

---

# MANIFEST

| file | found | bytes | lines | sha256 |
|---|---|---|---|---|
| `src/openjarvis/tools/mailbox_tools.py` | yes | 33666 | 822 | `4DB19C1EF90EEAB3...` |
| `src/openjarvis/connectors/imap_mail.py` | yes | 34850 | 901 | `B771AC1FF6DE4C34...` |

These hashes pin the exact bytes you reviewed. If a later patch is built against different bytes, the mismatch is detectable.

