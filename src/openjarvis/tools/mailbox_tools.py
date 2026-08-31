"""Executable mailbox tools - the agent-callable layer over imap_mail.

Connector ``mcp_tools()`` specs are declarative only; ``SystemBuilder``
resolves agent tools from ``MCPServer().get_tools()``, which discovers
``BaseTool`` subclasses registered in ``ToolRegistry``. These classes are
that layer. Each one wraps ``ImapMailConnector`` and returns a JSON string.

Registry constraint: ``MCPServer._auto_discover_tools`` instantiates user
tools with ``ToolRegistry.create(key)`` - no arguments. Every tool here is
therefore zero-arg constructible and resolves its account at execute time.

SAFETY NOTE - why ``requires_confirmation`` is deliberately NOT set:

``ToolExecutor.execute`` treats that flag as a hard requirement, not a
prompt::

    if tool.spec.requires_confirmation:
        if not self._interactive or self._confirm_callback is None:
            return ToolResult(..., success=False)

The server-side agent path builds its executor without ``interactive=True``
and without a confirm callback, so a tool carrying that flag does not ask
for confirmation - it fails every single call. The safety interlock is
implemented in the tool contract instead:

  * ``dry_run`` defaults to True and returns a plan with exact counts
  * applying requires BOTH ``dry_run=False`` AND ``confirm`` set to the
    exact string ``CONFIRM DELETE``

That keeps the destructive path reachable by the agent while making it
impossible to trip by accident or by a single malformed argument.

Account setup: credentials live in
``~/.openjarvis/connectors/imap_mail_<account>.json`` as
``{"email", "password", "provider"}``. Use ``setup_mailbox_account.py``
to write one; nothing here ever logs or returns a password.
"""

from __future__ import annotations

import json
import logging
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional

from openjarvis.connectors.imap_mail import PROVIDERS, ImapMailConnector
from openjarvis.connectors.oauth import load_tokens
from openjarvis.core.config import DEFAULT_CONFIG_DIR
from openjarvis.core.registry import ToolRegistry
from openjarvis.core.types import ToolResult
from openjarvis.tools._stubs import BaseTool, ToolSpec

logger = logging.getLogger(__name__)

CONFIRM_TOKEN = "CONFIRM DELETE"
_CONNECTOR_DIR = DEFAULT_CONFIG_DIR / "connectors"
_PREFIX = "imap_mail_"


# ---------------------------------------------------------------------------
# account resolution
# ---------------------------------------------------------------------------


def list_accounts() -> List[Dict[str, str]]:
    """Return every configured mailbox account, without credentials."""
    out: List[Dict[str, str]] = []
    try:
        if not _CONNECTOR_DIR.exists():
            return out
        for path in sorted(_CONNECTOR_DIR.glob(_PREFIX + "*.json")):
            account = path.stem[len(_PREFIX) :]
            tokens = load_tokens(str(path)) or {}
            out.append(
                {
                    "account": account,
                    "provider": tokens.get("provider", "generic"),
                    "email": tokens.get("email", ""),
                    "configured": bool(tokens.get("email") and tokens.get("password")),
                }
            )
    except Exception as exc:
        logger.warning("mailbox tools: could not enumerate accounts: %s", exc)
    return out


def _resolve_account(account: str) -> str:
    """Pick an account name, defaulting to the only one if unambiguous."""
    # openjarvis-account-resolve-v1: validate the id against configured
    # accounts. Never pass an unknown id through as if it resolved, and
    # accept the account email as an alias for the id (Defect 6).
    configured = [a for a in list_accounts() if a["configured"]]
    if account:
        needle = account.strip().lower()
        for a in configured:
            if a["account"].lower() == needle:
                return a["account"]
        for a in configured:
            email = (a.get("email") or "").lower()
            if email and email == needle:
                return a["account"]
        return ""
    if len(configured) == 1:
        return configured[0]["account"]
    return ""


def connector_for(account: str = "") -> Optional[ImapMailConnector]:
    """Build a connector for a configured account, or None."""
    resolved = _resolve_account(account)
    if not resolved:
        return None
    path = _CONNECTOR_DIR / ("%s%s.json" % (_PREFIX, resolved))
    tokens = load_tokens(str(path)) or {}
    provider = tokens.get("provider", "generic")
    if provider not in PROVIDERS:
        provider = "generic"
    return ImapMailConnector(
        provider=provider,
        account_id=resolved,
        credentials_path=str(path),
        imap_host=tokens.get("host", ""),
    )


def _dump(payload: Any) -> str:
    """Serialize a tool payload as JSON text."""
    return json.dumps(payload, indent=2, default=str)


def _no_account_result(name: str, account: str) -> ToolResult:
    """Uniform failure when no usable account was resolved."""
    known = list_accounts()
    return ToolResult(
        tool_name=name,
        content=_dump(
            {
                "error": (
                    "no configured mailbox account matched %r" % account
                    if account
                    else "no account specified and more than one (or zero) is configured"
                ),
                "known_accounts": known,
                "hint": "run setup_mailbox_account.py to configure an account",
            }
        ),
        success=False,
    )


# ---------------------------------------------------------------------------
# read-only tools
# ---------------------------------------------------------------------------


@ToolRegistry.register("mailbox_list_accounts")
class MailboxListAccountsTool(BaseTool):
    """List configured mailbox accounts."""

    tool_id = "mailbox_list_accounts"
    is_local = True

    @property
    def spec(self) -> ToolSpec:
        return ToolSpec(
            name="mailbox_list_accounts",
            description=(
                "List the configured mailbox accounts and their providers. "
                "Call this first when the user does not name an account."
            ),
            parameters={"type": "object", "properties": {}},
            category="communication",
            latency_estimate=0.1,
            timeout_seconds=15.0,
        )

    def execute(self, **params: Any) -> ToolResult:
        return ToolResult(
            tool_name=self.tool_id,
            content=_dump({"accounts": list_accounts()}),
            success=True,
        )


@ToolRegistry.register("mailbox_usage_report")
class MailboxUsageReportTool(BaseTool):
    """Report what is consuming mailbox storage."""

    tool_id = "mailbox_usage_report"
    is_local = True

    @property
    def spec(self) -> ToolSpec:
        return ToolSpec(
            name="mailbox_usage_report",
            description=(
                "Report what is consuming storage in a mailbox: total size, "
                "size per folder, the senders responsible for the most bytes, "
                "and the largest individual messages. Reads message headers "
                "and sizes only, never message bodies. Use this to answer "
                "questions about a mailbox being full or over quota. ALSO use "
                "this whenever the user asks WHO is sending them mail, which "
                "senders or domains are cluttering the mailbox, or asks for a "
                "list of senders to review, classify, or approve - it is the "
                "correct first call for any such question. Raise top_senders "
                "to 40 or more when the user wants a list to review. "
                "openjarvis-sender-discovery-v1"
            ),
            parameters={
                "type": "object",
                "properties": {
                    "account": {
                        "type": "string",
                        "description": "Account name; omit if only one is configured",
                    },
                    "top_senders": {"type": "integer", "default": 15},
                    "top_messages": {"type": "integer", "default": 25},
                },
            },
            category="communication",
            latency_estimate=30.0,
            timeout_seconds=600.0,
            required_capabilities=["mail.read"],
        )

    def execute(self, **params: Any) -> ToolResult:
        account = str(params.get("account", "") or "")
        conn = connector_for(account)
        if conn is None:
            return _no_account_result(self.tool_id, account)
        try:
            report = conn.usage_report(
                top_senders=int(params.get("top_senders", 15) or 15),
                top_messages=int(params.get("top_messages", 25) or 25),
            )
        except Exception as exc:
            logger.exception("mailbox_usage_report failed")
            return ToolResult(
                tool_name=self.tool_id,
                content=_dump({"error": str(exc)}),
                success=False,
            )
        return ToolResult(
            tool_name=self.tool_id,
            content=_dump(report),
            success="error" not in report,
        )


# openjarvis-find-summary-v1 openjarvis-find-spec-v1
@ToolRegistry.register("mailbox_find_messages")
class MailboxFindMessagesTool(BaseTool):
    """Find messages by sender, subject, size, or age."""

    tool_id = "mailbox_find_messages"
    is_local = True

    @property
    def spec(self) -> ToolSpec:
        return ToolSpec(
            name="mailbox_find_messages",
            description=(
                "Find messages in a mailbox by sender address, subject text, "
                "minimum size in bytes, or age in days. Defaults to "
                "detail=summary, which returns counts grouped by sender and "
                "folder. Summary is a complete and authoritative answer to "
                "how many, from whom, and which folder. Do NOT call this "
                "tool a second time with detail=full to confirm or expand a "
                "count you already have. Use detail=full only when you are "
                "about to move or delete specific messages and need their "
                "uids to do it. from_addr is OPTIONAL: OMIT it entirely to "
                "enumerate senders rather than confirm one. An unfiltered "
                "summary call returns by_address rows for every sender in the "
                "search window, which answers who is sending mail and how "
                "much. NEVER guess a sender name to search for - if the user "
                "has not named one, omit from_addr or call "
                "mailbox_usage_report instead."
            ),
            parameters={
                "type": "object",
                "properties": {
                    "account": {"type": "string"},
                    "folder": {
                        "type": "string",
                        "description": "Restrict to one folder; omit to search all",
                    },
                    "from_addr": {
                        "type": "string",
                        "description": "Substring match on the sender address",
                    },
                    "subject": {
                        "type": "string",
                        "description": "Substring match on the subject",
                    },
                    "larger_than_bytes": {"type": "integer", "default": 0},
                    "older_than_days": {
                        "type": "integer",
                        "default": 0,
                        "description": "Only messages older than this many days",
                    },
                    "limit": {"type": "integer", "default": 5000},
                    "detail": {
                        "type": "string",
                        "enum": ["summary", "full"],
                        "default": "summary",
                        "description": (
                            "summary returns counts grouped by sender and "
                            "folder and is sufficient for every counting or "
                            "location question; full returns every message "
                            "object including uids and is only for when you "
                            "need uids to act on messages"
                        ),
                    },
                },
            },
            category="communication",
            latency_estimate=20.0,
            timeout_seconds=600.0,
            required_capabilities=["mail.read"],
        )

    def execute(self, **params: Any) -> ToolResult:
        account = str(params.get("account", "") or "")
        conn = connector_for(account)
        if conn is None:
            return _no_account_result(self.tool_id, account)

        before: Optional[datetime] = None
        try:
            limit = int(params.get("limit", 5000) or 5000)
        except (TypeError, ValueError):
            limit = 5000
        if limit <= 0:
            limit = 5000
        detail = str(params.get("detail", "summary") or "summary").lower()
        if detail not in ("summary", "full"):
            detail = "summary"
        try:
            days = int(params.get("older_than_days", 0) or 0)
        except (TypeError, ValueError):
            days = 0
        if days > 0:
            before = datetime.now() - timedelta(days=days)

        try:
            hits = conn.find_messages(
                folder=str(params.get("folder", "") or ""),
                from_addr=str(params.get("from_addr", "") or ""),
                subject=str(params.get("subject", "") or ""),
                larger_than_bytes=int(params.get("larger_than_bytes", 0) or 0),
                before=before,
                limit=limit,
            )
        except Exception as exc:
            logger.exception("mailbox_find_messages failed")
            return ToolResult(
                tool_name=self.tool_id,
                content=_dump({"error": str(exc)}),
                success=False,
            )

        total = sum(h["bytes"] for h in hits)
        truncated = len(hits) >= limit
        by_address: Dict[str, Dict[str, Any]] = {}
        by_folder: Dict[str, Dict[str, Any]] = {}
        for h in hits:
            addr = str(h.get("from_addr", "") or "")
            fold = str(h.get("folder", "") or "")
            size = int(h.get("bytes", 0) or 0)
            row_a = by_address.setdefault(
                addr, {"from_addr": addr, "count": 0, "bytes": 0}
            )
            row_a["count"] += 1
            row_a["bytes"] += size
            row_f = by_folder.setdefault(
                fold, {"folder": fold, "count": 0, "bytes": 0}
            )
            row_f["count"] += 1
            row_f["bytes"] += size
        payload: Dict[str, Any] = {
            "match_count": len(hits),
            "total_matched": len(hits),
            "total_bytes": total,
            "limit": limit,
            "truncated": truncated,
            "detail": detail,
            "by_address": sorted(by_address.values(), key=lambda r: -r["count"]),
            "by_folder": sorted(by_folder.values(), key=lambda r: -r["count"]),
            "coverage": "newest ~10000 per folder (IMAP server window)",  # openjarvis-find-window-v1
        }
        notes = [
            "COUNTS ARE WINDOWED. The mail server exposes only the newest "
            "~10,000 messages per folder and does not index past them. "
            "match_count is therefore a FLOOR within that window and is NEVER "
            "a mailbox total. When reporting a count, say plainly that it "
            "covers only the most recent mail the server exposes. Do not claim "
            "all matching mail was found, moved, or deleted."
        ]
        if truncated:
            notes.append(
                "RESULT ALSO TRUNCATED AT THE RESULT LIMIT, below even the "
                "server window. Re-run with a higher limit before acting."
            )
        payload["note"] = " ".join(notes)
        if detail == "full":
            payload["matches"] = hits
        return ToolResult(
            tool_name=self.tool_id,
            content=_dump(payload),
            success=True,
        )


# ---------------------------------------------------------------------------
# destructive tools - dry run by default, explicit token to apply
# ---------------------------------------------------------------------------


def _confirmed(params: Dict[str, Any]) -> bool:
    """True only when the caller explicitly asked to apply."""
    dry_run = params.get("dry_run", True)
    if isinstance(dry_run, str):
        dry_run = dry_run.strip().lower() not in ("false", "0", "no")
    if dry_run:
        return False
    return str(params.get("confirm", "")).strip() == CONFIRM_TOKEN


def _needs_confirmation_result(name: str, plan: Any) -> ToolResult:
    """Return the plan plus instructions for how to actually apply it."""
    return ToolResult(
        tool_name=name,
        content=_dump(
            {
                "status": "dry_run",
                "plan": plan,
                "to_apply": {
                    "dry_run": False,
                    "confirm": CONFIRM_TOKEN,
                },
                "instruction": (
                    "Nothing was changed. Show this plan to the user and ask "
                    "them to approve it. Only if they explicitly approve, call "
                    "this tool again with dry_run=false and confirm set to the "
                    "exact string above."
                ),
            }
        ),
        success=True,
    )


@ToolRegistry.register("mailbox_move_to_trash")
class MailboxMoveToTrashTool(BaseTool):
    """Move specific messages to the trash folder."""

    tool_id = "mailbox_move_to_trash"
    is_local = True

    @property
    def spec(self) -> ToolSpec:
        return ToolSpec(
            name="mailbox_move_to_trash",
            description=(
                "Move specific messages to the mailbox trash folder. "
                "DESTRUCTIVE. Defaults to a dry run that reports exactly what "
                "would move and changes nothing. To actually move messages you "
                "must pass dry_run=false AND confirm='" + CONFIRM_TOKEN + "'. "
                "Never pass those without the user's explicit approval of a "
                "dry-run plan you have already shown them. Note that trash "
                "still counts against quota until it is emptied."
            ),
            parameters={
                "type": "object",
                "properties": {
                    "account": {"type": "string"},
                    "folder": {
                        "type": "string",
                        "description": "Folder the messages currently live in",
                    },
                    "uids": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": (
                            "Message uids from mailbox_find_messages. Omit this "
                            "and pass from_addr instead for anything larger than "
                            "a handful of messages."
                        ),
                    },
                    "from_addr": {
                        "type": "string",
                        "description": (
                            "Sender substring, e.g. 'microcenter'. When given, "
                            "the tool finds the matching messages in the named "
                            "folder itself and moves them. Preferred over uids. "
                            "Do not pass both."
                        ),
                    },
                    "dry_run": {"type": "boolean", "default": True},
                    "confirm": {
                        "type": "string",
                        "description": "Must be '" + CONFIRM_TOKEN + "' to apply",
                    },
                },
                "required": ["folder"],
            },
            category="communication",
            latency_estimate=5.0,
            timeout_seconds=1800.0,  # openjarvis-tool-timeout-v1
            required_capabilities=["mail.write"],
        )

    def execute(self, **params: Any) -> ToolResult:
        account = str(params.get("account", "") or "")
        conn = connector_for(account)
        if conn is None:
            return _no_account_result(self.tool_id, account)

        folder = str(params.get("folder", "") or "")

        # openjarvis-filter-move-v1
        # Server-side selection. The model passes a sender substring; the tool
        # resolves it to uids here so no uid list ever crosses the model.
        _from_addr = str(params.get("from_addr", "") or "").strip()
        _resolved = 0
        _blocked_report = {}
        if _from_addr:
            if params.get("uids"):
                return ToolResult(
                    tool_name=self.tool_id,
                    content=_dump({
                        "error": (
                            "Pass either from_addr or uids, not both. Use "
                            "from_addr and let the tool select the messages."
                        )
                    }),
                    success=False,
                )
            if not folder:
                return ToolResult(
                    tool_name=self.tool_id,
                    content=_dump({"error": "folder is required when using from_addr"}),
                    success=False,
                )
            try:
                _hits = conn.find_messages(folder=folder, from_addr=_from_addr, limit=5000)  # openjarvis-h2-folder-scope-v1
            except Exception as exc:
                logger.exception("mailbox_move_to_trash from_addr lookup failed")
                return ToolResult(
                    tool_name=self.tool_id,
                    content=_dump({"error": "sender lookup failed: %s" % exc}),
                    success=False,
                )
            _sel = []
            for _h in _hits or []:
                if not isinstance(_h, dict):
                    continue
                if str(_h.get("folder", "") or "") != folder:
                    continue
                _u = str(_h.get("uid", "") or "").strip()
                if _u.isdigit():
                    _sel.append(_u)
            # openjarvis-protected-senders-v1
            import json as _json
            from pathlib import Path as _Path
            _defaults = ['stackcommerce.com', 'cdgray33@yahoo.com',
                'notify@r.groupon.com', 'orders@r.groupon.com',
                'verify@r.groupon.com', 'otp@r.groupon.com',
                'orders@sidedeal', 'account@', 'ratings@',
                'noreply@service.wayfair.com']
            _prot = _defaults
            try:
                _pf = _Path.cwd() / 'protected_senders.json'
                if _pf.is_file():
                    _ld = _json.loads(_pf.read_text(encoding='utf-8'))
                    if isinstance(_ld, list) and _ld:
                        _prot = [str(x).lower() for x in _ld if str(x).strip()]
            except Exception:
                logger.exception('protected_senders.json unreadable; using built-in list')
            _keep = []
            for _h in _hits or []:
                if not isinstance(_h, dict):
                    continue
                if str(_h.get('folder', '') or '') != folder:
                    continue
                _u2 = str(_h.get('uid', '') or '').strip()
                if not _u2.isdigit():
                    continue
                _a = str(_h.get('from_addr', '') or '').lower()
                _m = ''
                for _p in _prot:
                    if _p and _p in _a:
                        _m = _p
                        break
                if _m:
                    _blocked_report[_a] = _blocked_report.get(_a, 0) + 1
                else:
                    _keep.append(_u2)
            _sel = _keep
            if _blocked_report:
                logger.warning('protected senders blocked from move: %s', _blocked_report)
            if _blocked_report and not _sel:
                return ToolResult(
                    tool_name=self.tool_id,
                    content=_dump({
                        'error': 'all matched messages are from protected senders; nothing moved',
                        'protected_blocked': _blocked_report,
                        'from_addr': _from_addr,
                        'folder': folder,
                    }),
                    success=False,
                )
            if not _sel:
                return ToolResult(
                    tool_name=self.tool_id,
                    content=_dump({
                        "error": "no messages matched",
                        "from_addr": _from_addr,
                        "folder": folder,
                        "searched": len(_hits or []),
                    }),
                    success=False,
                )
            params["uids"] = _sel
            _resolved = len(_sel)

        # openjarvis-uid-typeguard-v1
        uids = params.get("uids")
        if isinstance(uids, (str, bytes)) or not isinstance(uids, (list, tuple)):
            return ToolResult(
                tool_name=self.tool_id,
                content=_dump({
                    "error": (
                        "uids must be a JSON array of numeric uid strings taken "
                        "from a prior mailbox_find_messages result. A string was "
                        "rejected. Do not construct uids yourself."
                    ),
                    "received_type": type(uids).__name__,
                }),
                success=False,
            )
        uids = [str(u).strip() for u in uids]
        _bad = [u for u in uids if not u.isdigit()]
        if _bad:
            return ToolResult(
                tool_name=self.tool_id,
                content=_dump({
                    "error": (
                        "uids must be numeric strings from mailbox_find_messages. "
                        "Non-numeric values were rejected and nothing was moved."
                    ),
                    "invalid_sample": _bad[:5],
                    "invalid_count": len(_bad),
                }),
                success=False,
            )

        if not folder or not uids:
            return ToolResult(
                tool_name=self.tool_id,
                content=_dump({"error": "folder and a non-empty uids list are required"}),
                success=False,
            )

        try:
            if not _confirmed(params):
                plan = conn.move_to_trash(folder, uids, dry_run=True)
                return _needs_confirmation_result(self.tool_id, plan)
            result = conn.move_to_trash(folder, uids, dry_run=False)
        except Exception as exc:
            logger.exception("mailbox_move_to_trash failed")
            return ToolResult(
                tool_name=self.tool_id,
                content=_dump({"error": str(exc)}),
                success=False,
            )

        if _resolved and isinstance(result, dict):
            result = dict(result)
            result["selected_by"] = "from_addr"
            if _blocked_report:
                result["protected_blocked"] = _blocked_report
            result["from_addr"] = _from_addr
            result["resolved_uid_count"] = _resolved

        return ToolResult(
            tool_name=self.tool_id,
            content=_dump(result),
            success=bool(result.get("applied")),
        )


@ToolRegistry.register("mailbox_empty_folder")
class MailboxEmptyFolderTool(BaseTool):
    """Permanently delete every message in a folder."""

    tool_id = "mailbox_empty_folder"
    is_local = True

    @property
    def spec(self) -> ToolSpec:
        return ToolSpec(
            name="mailbox_empty_folder",
            description=(
                "Permanently delete every message in a folder, normally the "
                "trash folder, to reclaim storage. IRREVERSIBLE AND "
                "DESTRUCTIVE. Defaults to a dry run reporting the exact "
                "message count and byte total. To actually delete you must "
                "pass dry_run=false AND confirm='" + CONFIRM_TOKEN + "'. Never "
                "pass those without the user's explicit approval of a dry-run "
                "plan you have already shown them."
            ),
            parameters={
                "type": "object",
                "properties": {
                    "account": {"type": "string"},
                    "folder": {
                        "type": "string",
                        "description": "Folder to empty, e.g. Trash",
                    },
                    "dry_run": {"type": "boolean", "default": True},
                    "confirm": {
                        "type": "string",
                        "description": "Must be '" + CONFIRM_TOKEN + "' to apply",
                    },
                },
                "required": ["folder"],
            },
            category="communication",
            latency_estimate=10.0,
            timeout_seconds=600.0,
            required_capabilities=["mail.write"],
        )

    def execute(self, **params: Any) -> ToolResult:
        account = str(params.get("account", "") or "")
        conn = connector_for(account)
        if conn is None:
            return _no_account_result(self.tool_id, account)

        folder = str(params.get("folder", "") or "")
        if not folder:
            return ToolResult(
                tool_name=self.tool_id,
                content=_dump({"error": "folder is required"}),
                success=False,
            )

        try:
            if not _confirmed(params):
                plan = conn.empty_folder(folder, dry_run=True)
                return _needs_confirmation_result(self.tool_id, plan)
            result = conn.empty_folder(folder, dry_run=False)
        except Exception as exc:
            logger.exception("mailbox_empty_folder failed")
            return ToolResult(
                tool_name=self.tool_id,
                content=_dump({"error": str(exc)}),
                success=False,
            )

        return ToolResult(
            tool_name=self.tool_id,
            content=_dump(result),
            success=bool(result.get("applied")),
        )


__all__ = [
    "MailboxListAccountsTool",
    "MailboxUsageReportTool",
    "MailboxFindMessagesTool",
    "MailboxMoveToTrashTool",
    "MailboxEmptyFolderTool",
    "connector_for",
    "list_accounts",
]
