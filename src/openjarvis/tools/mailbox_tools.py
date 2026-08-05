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
    if account:
        return account
    accounts = [a["account"] for a in list_accounts() if a["configured"]]
    if len(accounts) == 1:
        return accounts[0]
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
                "questions about a mailbox being full or over quota."
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
                "minimum size in bytes, or age in days. Each result includes "
                "the folder and uid needed to act on that message. Use this "
                "to build a deletion candidate list before removing anything."
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
                    "limit": {"type": "integer", "default": 200},
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
                limit=int(params.get("limit", 200) or 200),
            )
        except Exception as exc:
            logger.exception("mailbox_find_messages failed")
            return ToolResult(
                tool_name=self.tool_id,
                content=_dump({"error": str(exc)}),
                success=False,
            )

        total = sum(h["bytes"] for h in hits)
        return ToolResult(
            tool_name=self.tool_id,
            content=_dump(
                {
                    "match_count": len(hits),
                    "total_bytes": total,
                    "matches": hits,
                }
            ),
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
                        "description": "Message uids from mailbox_find_messages",
                    },
                    "dry_run": {"type": "boolean", "default": True},
                    "confirm": {
                        "type": "string",
                        "description": "Must be '" + CONFIRM_TOKEN + "' to apply",
                    },
                },
                "required": ["folder", "uids"],
            },
            category="communication",
            latency_estimate=5.0,
            timeout_seconds=300.0,
            required_capabilities=["mail.write"],
        )

    def execute(self, **params: Any) -> ToolResult:
        account = str(params.get("account", "") or "")
        conn = connector_for(account)
        if conn is None:
            return _no_account_result(self.tool_id, account)

        folder = str(params.get("folder", "") or "")
        uids = params.get("uids") or []
        if isinstance(uids, str):
            uids = [u.strip() for u in uids.split(",") if u.strip()]
        uids = [str(u) for u in uids]

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
