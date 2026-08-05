"""Provider-agnostic IMAP mail connector - Yahoo, Gmail, or any IMAP host.

Supersedes the read-only, INBOX-only ``gmail_imap`` connector for mailbox
work that needs to see and change the whole account:

  * every selectable folder, not just INBOX
  * size-aware enumeration via ``RFC822.SIZE`` plus header-only fetches,
    so quota questions are answered without downloading message bodies
  * UID-based mutation (move-to-trash, delete, empty folder) so that
    sequence-number shifts during EXPUNGE cannot delete the wrong mail

Authentication is an app password over IMAP4_SSL. No OAuth, no
dependencies outside the standard library.

  Yahoo app password : https://login.yahoo.com/account/security
  Gmail app password : https://myaccount.google.com/apppasswords

Provider differences that this module handles for you:

  * Gmail's "All Mail" mirrors every other folder, so it is excluded
    from usage totals by default to avoid double counting.
  * On Gmail, setting ``\\Deleted`` on a label only unlabels the
    message. Space is reclaimed only by copying to ``[Gmail]/Trash``
    and then emptying it. ``move_to_trash`` does the provider-correct
    thing for both backends.

EVERY destructive method defaults to ``dry_run=True`` and returns a plan
describing what it would do. Nothing is removed until it is called again
with ``dry_run=False``.
"""

from __future__ import annotations

import email as email_lib
import imaplib
import logging
import re
from collections import defaultdict
from datetime import datetime
from email.header import decode_header
from email.utils import parsedate_to_datetime, parseaddr
from typing import Any, Dict, Iterator, List, Optional, Sequence, Tuple

from openjarvis.connectors._stubs import BaseConnector, Document, SyncStatus
from openjarvis.connectors.oauth import delete_tokens, load_tokens, save_tokens
from openjarvis.core.config import DEFAULT_CONFIG_DIR
from openjarvis.core.registry import ConnectorRegistry
from openjarvis.tools._stubs import ToolSpec

logger = logging.getLogger(__name__)

_DEFAULT_CREDENTIALS_PATH = str(DEFAULT_CONFIG_DIR / "connectors" / "imap_mail.json")

# Per-provider defaults. ``trash`` is where deleted mail must land for the
# space to actually be reclaimed; ``exclude`` folders are skipped in usage
# totals because they mirror other folders.
PROVIDERS: Dict[str, Dict[str, Any]] = {
    "yahoo": {
        "host": "imap.mail.yahoo.com",
        "port": 993,
        "trash": "Trash",
        "exclude": (),
        "app_password_url": "https://login.yahoo.com/account/security",
    },
    "gmail": {
        "host": "imap.gmail.com",
        "port": 993,
        "trash": "[Gmail]/Trash",
        "exclude": ("[Gmail]/All Mail",),
        "app_password_url": "https://myaccount.google.com/apppasswords",
    },
    "generic": {
        "host": "",
        "port": 993,
        "trash": "Trash",
        "exclude": (),
        "app_password_url": "",
    },
}

# (\HasNoChildren) "/" "INBOX"
_LIST_RE = re.compile(
    rb'\((?P<flags>[^)]*)\)\s+"?(?P<delim>[^"\s]*)"?\s+(?P<name>.*)'
)

_HEADER_FIELDS = "(FROM TO SUBJECT DATE MESSAGE-ID)"


def _decode_header_value(raw: str) -> str:
    """Decode a possibly RFC2047-encoded header into plain text."""
    if not raw:
        return ""
    try:
        parts = decode_header(raw)
    except Exception:
        return raw
    return "".join(
        part.decode(enc or "utf-8", errors="replace") if isinstance(part, bytes) else part
        for part, enc in parts
    )


def _extract_text_body(msg: email_lib.message.Message) -> str:
    """Extract a plain-text body, falling back to text/html."""
    if msg.is_multipart():
        for wanted in ("text/plain", "text/html"):
            for part in msg.walk():
                if part.get_content_type() == wanted:
                    payload = part.get_payload(decode=True)
                    if payload:
                        return payload.decode("utf-8", errors="replace")
        return ""
    payload = msg.get_payload(decode=True)
    if payload:
        return payload.decode("utf-8", errors="replace")
    return ""


def _parse_date(msg: email_lib.message.Message) -> datetime:
    """Parse the Date header, falling back to now."""
    raw = msg.get("Date", "")
    if not raw:
        return datetime.now()
    try:
        return parsedate_to_datetime(raw)
    except Exception:
        return datetime.now()


def _quote_folder(name: str) -> str:
    """Quote a folder name for SELECT. IMAP names may contain spaces."""
    return '"%s"' % name.replace('"', '\\"')


def _human_bytes(n: int) -> str:
    """Render a byte count for display in tool output."""
    step = 1024.0
    value = float(n)
    for unit in ("B", "KB", "MB", "GB"):
        if value < step or unit == "GB":
            return "%.1f %s" % (value, unit)
        value /= step
    return "%.1f GB" % value


@ConnectorRegistry.register("imap_mail")
class ImapMailConnector(BaseConnector):
    """IMAP mail connector with folder enumeration, sizing, and mutation.

    Instantiate one per account::

        yahoo = ConnectorRegistry.create(
            "imap_mail", provider="yahoo", account_id="yahoo_main",
        )
        gmail = ConnectorRegistry.create(
            "imap_mail", provider="gmail", account_id="agent_gmail",
        )

    Credentials resolve from the constructor first, then from
    ``~/.openjarvis/connectors/imap_mail_<account_id>.json``.
    """

    connector_id = "imap_mail"
    display_name = "Mail (IMAP)"
    auth_type = "local"

    def __init__(
        self,
        email_address: str = "",
        app_password: str = "",
        credentials_path: str = "",
        *,
        provider: str = "generic",
        account_id: str = "",
        imap_host: str = "",
        imap_port: int = 0,
        folders: Optional[Sequence[str]] = None,
        trash_folder: str = "",
        max_messages: Optional[int] = None,
    ) -> None:
        prov = PROVIDERS.get(provider.lower().strip(), PROVIDERS["generic"])
        self._provider = provider.lower().strip() or "generic"
        self._email = email_address
        self._password = app_password
        self._account_id = account_id or self._provider
        self._credentials_path = credentials_path or str(
            DEFAULT_CONFIG_DIR / "connectors" / ("imap_mail_%s.json" % self._account_id)
        )
        self._imap_host = imap_host or prov["host"]
        self._imap_port = imap_port or prov["port"]
        self._trash_folder = trash_folder or prov["trash"]
        self._exclude_from_usage = tuple(prov["exclude"])
        self._app_password_url = prov["app_password_url"]
        # ``None`` means no cap. A positive value bounds enumeration,
        # which is useful for a first look at a very large mailbox.
        self._max_messages = max_messages
        self._folders_filter = list(folders) if folders else None
        self._items_synced = 0
        self._items_total = 0
        self._last_error: Optional[str] = None

    # ------------------------------------------------------------------
    # credentials / BaseConnector contract
    # ------------------------------------------------------------------

    def _resolve_credentials(self) -> Tuple[str, str]:
        """Return (email, password). Constructor args take priority."""
        if self._email and self._password:
            return self._email, self._password
        tokens = load_tokens(self._credentials_path)
        if tokens:
            return tokens.get("email", ""), tokens.get("password", "")
        return "", ""

    def is_connected(self) -> bool:
        em, pw = self._resolve_credentials()
        return bool(em and pw and self._imap_host)

    def disconnect(self) -> None:
        self._email = ""
        self._password = ""
        delete_tokens(self._credentials_path)

    def auth_url(self) -> str:
        return self._app_password_url or "https://support.google.com/mail/answer/7126229"

    def handle_callback(self, code: str) -> None:
        """Store credentials. ``code`` is ``"email:app_password"``."""
        if ":" in code:
            em, pw = code.split(":", 1)
            save_tokens(
                self._credentials_path,
                {"email": em.strip(), "password": pw.strip()},
            )
        else:
            save_tokens(self._credentials_path, {"email": "", "password": code.strip()})

    def sync_status(self) -> SyncStatus:
        return SyncStatus(
            state="error" if self._last_error else "idle",
            items_synced=self._items_synced,
            items_total=self._items_total,
            error=self._last_error,
        )

    # ------------------------------------------------------------------
    # connection
    # ------------------------------------------------------------------

    def _connect(self) -> Optional[imaplib.IMAP4_SSL]:
        """Open and authenticate an IMAP connection, or return None."""
        em, pw = self._resolve_credentials()
        if not em or not pw:
            self._last_error = "no credentials configured"
            logger.error("imap_mail[%s]: no credentials configured", self._account_id)
            return None
        if not self._imap_host:
            self._last_error = "no IMAP host configured"
            logger.error("imap_mail[%s]: no IMAP host configured", self._account_id)
            return None
        try:
            imap = imaplib.IMAP4_SSL(self._imap_host, self._imap_port)
            imap.login(em, pw)
        except (imaplib.IMAP4.error, OSError) as exc:
            self._last_error = "login failed: %s" % exc
            logger.error("imap_mail[%s] login failed: %s", self._account_id, exc)
            return None
        self._last_error = None
        return imap

    @staticmethod
    def _close(imap: imaplib.IMAP4_SSL) -> None:
        """Close a connection without letting teardown raise."""
        try:
            imap.logout()
        except Exception:
            pass

    # ------------------------------------------------------------------
    # folder enumeration
    # ------------------------------------------------------------------

    def _list_folders(self, imap: imaplib.IMAP4_SSL) -> List[str]:
        """Return every selectable folder name on the account."""
        typ, data = imap.list()
        if typ != "OK" or not data:
            return []
        names: List[str] = []
        for line in data:
            if not isinstance(line, bytes):
                continue
            match = _LIST_RE.match(line)
            if not match:
                continue
            flags = match.group("flags").decode("utf-8", errors="replace")
            if "\\Noselect" in flags:
                continue
            raw = match.group("name").decode("utf-8", errors="replace").strip()
            names.append(raw[1:-1] if raw.startswith('"') and raw.endswith('"') else raw)
        return names

    def list_folders(self) -> List[str]:
        """Public folder listing. Opens and closes its own connection."""
        imap = self._connect()
        if imap is None:
            return []
        try:
            return self._list_folders(imap)
        finally:
            self._close(imap)

    def _target_folders(self, imap: imaplib.IMAP4_SSL, *, for_usage: bool) -> List[str]:
        """Apply the configured folder filter and provider exclusions."""
        folders = self._folders_filter or self._list_folders(imap)
        if for_usage and self._exclude_from_usage:
            folders = [f for f in folders if f not in self._exclude_from_usage]
        return folders

    # ------------------------------------------------------------------
    # sizing - the quota question
    # ------------------------------------------------------------------

    def _fetch_summaries(
        self,
        imap: imaplib.IMAP4_SSL,
        folder: str,
        *,
        limit: Optional[int] = None,
    ) -> List[Dict[str, Any]]:
        """Return per-message summaries for one folder.

        Fetches ``RFC822.SIZE`` plus a header-only peek. No message body
        is transferred, so this stays cheap on very large mailboxes.
        """
        typ, _ = imap.select(_quote_folder(folder), readonly=True)
        if typ != "OK":
            logger.warning("imap_mail: cannot select folder %r", folder)
            return []

        typ, data = imap.uid("SEARCH", None, "ALL")
        if typ != "OK" or not data or not data[0]:
            return []
        uids = data[0].split()
        if limit is not None and limit > 0:
            uids = uids[-limit:]
        if not uids:
            return []

        summaries: List[Dict[str, Any]] = []
        # Batch to keep command lines well inside server limits.
        batch = 200
        for start in range(0, len(uids), batch):
            chunk = uids[start : start + batch]
            uid_set = b",".join(chunk).decode("ascii")
            typ, resp = imap.uid(
                "FETCH",
                uid_set,
                "(RFC822.SIZE BODY.PEEK[HEADER.FIELDS %s])" % _HEADER_FIELDS,
            )
            if typ != "OK" or not resp:
                continue
            for item in resp:
                if not isinstance(item, tuple) or len(item) < 2:
                    continue
                meta = item[0] if isinstance(item[0], bytes) else b""
                header_bytes = item[1] if isinstance(item[1], bytes) else b""
                uid_match = re.search(rb"UID\s+(\d+)", meta)
                size_match = re.search(rb"RFC822\.SIZE\s+(\d+)", meta)
                if not uid_match:
                    continue
                msg = email_lib.message_from_bytes(header_bytes)
                sender_name, sender_addr = parseaddr(msg.get("From", ""))
                summaries.append(
                    {
                        "uid": uid_match.group(1).decode("ascii"),
                        "folder": folder,
                        "size_bytes": int(size_match.group(1)) if size_match else 0,
                        "subject": _decode_header_value(msg.get("Subject", "")),
                        "from_name": _decode_header_value(sender_name),
                        "from_addr": (sender_addr or "").lower(),
                        "date": _parse_date(msg),
                        "message_id": msg.get("Message-ID", ""),
                    }
                )
        return summaries

    def usage_report(
        self,
        *,
        top_senders: int = 15,
        top_messages: int = 25,
        per_folder_limit: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Answer "what is filling up this mailbox".

        Returns folder totals, the heaviest senders by cumulative bytes,
        and the single largest messages, all without downloading bodies.
        """
        imap = self._connect()
        if imap is None:
            return {"error": self._last_error, "folders": [], "account": self._account_id}

        try:
            folders = self._target_folders(imap, for_usage=True)
            all_rows: List[Dict[str, Any]] = []
            folder_rows: List[Dict[str, Any]] = []

            for folder in folders:
                rows = self._fetch_summaries(imap, folder, limit=per_folder_limit)
                total = sum(r["size_bytes"] for r in rows)
                folder_rows.append(
                    {
                        "folder": folder,
                        "messages": len(rows),
                        "bytes": total,
                        "human": _human_bytes(total),
                    }
                )
                all_rows.extend(rows)

            by_sender: Dict[str, Dict[str, Any]] = defaultdict(
                lambda: {"messages": 0, "bytes": 0, "name": ""}
            )
            for row in all_rows:
                entry = by_sender[row["from_addr"] or "(unknown)"]
                entry["messages"] += 1
                entry["bytes"] += row["size_bytes"]
                if not entry["name"]:
                    entry["name"] = row["from_name"]

            senders = sorted(
                (
                    {
                        "address": addr,
                        "name": vals["name"],
                        "messages": vals["messages"],
                        "bytes": vals["bytes"],
                        "human": _human_bytes(vals["bytes"]),
                    }
                    for addr, vals in by_sender.items()
                ),
                key=lambda d: d["bytes"],
                reverse=True,
            )[:top_senders]

            largest = sorted(all_rows, key=lambda r: r["size_bytes"], reverse=True)
            largest_out = [
                {
                    "uid": r["uid"],
                    "folder": r["folder"],
                    "subject": r["subject"],
                    "from_addr": r["from_addr"],
                    "date": r["date"].isoformat(),
                    "bytes": r["size_bytes"],
                    "human": _human_bytes(r["size_bytes"]),
                }
                for r in largest[:top_messages]
            ]

            grand_total = sum(r["size_bytes"] for r in all_rows)
            self._items_total = len(all_rows)
            return {
                "account": self._account_id,
                "provider": self._provider,
                "total_messages": len(all_rows),
                "total_bytes": grand_total,
                "total_human": _human_bytes(grand_total),
                "excluded_folders": list(self._exclude_from_usage),
                "folders": sorted(folder_rows, key=lambda d: d["bytes"], reverse=True),
                "top_senders": senders,
                "largest_messages": largest_out,
            }
        finally:
            self._close(imap)

    def find_messages(
        self,
        *,
        folder: str = "",
        from_addr: str = "",
        subject: str = "",
        larger_than_bytes: int = 0,
        before: Optional[datetime] = None,
        limit: int = 200,
    ) -> List[Dict[str, Any]]:
        """Return message summaries matching the given criteria.

        The result rows carry ``folder`` and ``uid``, which is exactly
        what the deletion methods take - so a search result can be handed
        straight to ``move_to_trash`` without re-resolving anything.
        """
        imap = self._connect()
        if imap is None:
            return []
        try:
            folders = [folder] if folder else self._target_folders(imap, for_usage=True)
            hits: List[Dict[str, Any]] = []
            needle_from = (from_addr or "").lower().strip()
            needle_subj = (subject or "").lower().strip()

            for name in folders:
                for row in self._fetch_summaries(imap, name):
                    if needle_from and needle_from not in row["from_addr"]:
                        continue
                    if needle_subj and needle_subj not in row["subject"].lower():
                        continue
                    if larger_than_bytes and row["size_bytes"] < larger_than_bytes:
                        continue
                    if before is not None:
                        stamp = row["date"]
                        naive = stamp.replace(tzinfo=None) if stamp.tzinfo else stamp
                        cutoff = before.replace(tzinfo=None) if before.tzinfo else before
                        if naive >= cutoff:
                            continue
                    hits.append(
                        {
                            "uid": row["uid"],
                            "folder": row["folder"],
                            "subject": row["subject"],
                            "from_addr": row["from_addr"],
                            "date": row["date"].isoformat(),
                            "bytes": row["size_bytes"],
                            "human": _human_bytes(row["size_bytes"]),
                        }
                    )
                    if len(hits) >= limit:
                        return hits
            return hits
        finally:
            self._close(imap)

    # ------------------------------------------------------------------
    # mutation - every entry point is dry-run by default
    # ------------------------------------------------------------------

    def move_to_trash(
        self,
        folder: str,
        uids: Sequence[str],
        *,
        dry_run: bool = True,
    ) -> Dict[str, Any]:
        """Move messages to the provider's trash folder.

        This is the correct operation for reclaiming space. On Gmail a
        bare ``\\Deleted`` flag only removes a label; the message has to
        reach ``[Gmail]/Trash``. Trash still counts against quota until
        it is emptied - see ``empty_folder``.
        """
        plan = {
            "action": "move_to_trash",
            "account": self._account_id,
            "folder": folder,
            "trash": self._trash_folder,
            "uid_count": len(uids),
            "uids": list(uids),
            "dry_run": dry_run,
            "applied": False,
        }
        if not uids:
            plan["note"] = "no uids supplied; nothing to do"
            return plan
        if dry_run:
            plan["note"] = "DRY RUN. Re-run with dry_run=False to apply."
            return plan

        imap = self._connect()
        if imap is None:
            plan["error"] = self._last_error
            return plan
        try:
            typ, _ = imap.select(_quote_folder(folder), readonly=False)
            if typ != "OK":
                plan["error"] = "cannot select folder %r for writing" % folder
                return plan
            uid_set = ",".join(str(u) for u in uids)

            if folder != self._trash_folder:
                typ, _ = imap.uid("COPY", uid_set, _quote_folder(self._trash_folder))
                if typ != "OK":
                    plan["error"] = "COPY to %r failed" % self._trash_folder
                    return plan

            typ, _ = imap.uid("STORE", uid_set, "+FLAGS", "(\\Deleted)")
            if typ != "OK":
                plan["error"] = "STORE +FLAGS \\Deleted failed"
                return plan

            imap.expunge()
            plan["applied"] = True
            return plan
        finally:
            self._close(imap)

    def empty_folder(self, folder: str, *, dry_run: bool = True) -> Dict[str, Any]:
        """Permanently remove every message in a folder.

        Intended for the trash folder. This is irreversible - the dry run
        reports the exact message count and byte total first.
        """
        plan = {
            "action": "empty_folder",
            "account": self._account_id,
            "folder": folder,
            "dry_run": dry_run,
            "applied": False,
        }
        imap = self._connect()
        if imap is None:
            plan["error"] = self._last_error
            return plan
        try:
            rows = self._fetch_summaries(imap, folder)
            total = sum(r["size_bytes"] for r in rows)
            plan["message_count"] = len(rows)
            plan["bytes"] = total
            plan["human"] = _human_bytes(total)
            if not rows:
                plan["note"] = "folder already empty"
                return plan
            if dry_run:
                plan["note"] = (
                    "DRY RUN. Would permanently delete %d messages (%s). "
                    "Re-run with dry_run=False to apply."
                    % (len(rows), _human_bytes(total))
                )
                return plan

            typ, _ = imap.select(_quote_folder(folder), readonly=False)
            if typ != "OK":
                plan["error"] = "cannot select folder %r for writing" % folder
                return plan
            uid_set = ",".join(r["uid"] for r in rows)
            typ, _ = imap.uid("STORE", uid_set, "+FLAGS", "(\\Deleted)")
            if typ != "OK":
                plan["error"] = "STORE +FLAGS \\Deleted failed"
                return plan
            imap.expunge()
            plan["applied"] = True
            return plan
        finally:
            self._close(imap)

    # ------------------------------------------------------------------
    # ingestion
    # ------------------------------------------------------------------

    def sync(
        self,
        *,
        since: Optional[datetime] = None,
        cursor: Optional[str] = None,
    ) -> Iterator[Document]:
        """Yield documents from every targeted folder, newest first.

        Like the gmail_imap connector this always enumerates fully and
        relies on pipeline-level dedup, because IMAP has no cursor that
        survives a server restart.
        """
        imap = self._connect()
        if imap is None:
            return

        try:
            folders = self._target_folders(imap, for_usage=True)
            synced = 0
            total = 0

            for folder in folders:
                typ, _ = imap.select(_quote_folder(folder), readonly=True)
                if typ != "OK":
                    continue
                typ, data = imap.uid("SEARCH", None, "ALL")
                if typ != "OK" or not data or not data[0]:
                    continue
                uids = list(reversed(data[0].split()))
                total += len(uids)
                if self._max_messages is not None and self._max_messages > 0:
                    uids = uids[: self._max_messages]

                for uid in uids:
                    try:
                        typ, msg_data = imap.uid("FETCH", uid.decode("ascii"), "(RFC822)")
                        if typ != "OK" or not msg_data or not isinstance(msg_data[0], tuple):
                            continue
                        msg = email_lib.message_from_bytes(msg_data[0][1])
                    except Exception:
                        continue

                    timestamp = _parse_date(msg)
                    if since is not None:
                        naive = timestamp.replace(tzinfo=None) if timestamp.tzinfo else timestamp
                        floor = since.replace(tzinfo=None) if since.tzinfo else since
                        if naive < floor:
                            continue

                    subject = _decode_header_value(msg.get("Subject", ""))
                    sender = msg.get("From", "")
                    to = msg.get("To", "")
                    message_id = msg.get("Message-ID", "") or "%s:%s" % (
                        folder,
                        uid.decode("ascii"),
                    )

                    synced += 1
                    yield Document(
                        doc_id="imap_mail:%s:%s" % (self._account_id, message_id),
                        source="imap_mail",
                        doc_type="email",
                        content=_extract_text_body(msg),
                        title=subject,
                        author=sender,
                        participants=[a.strip() for a in (to or "").split(",") if a.strip()],
                        timestamp=timestamp,
                        thread_id=msg.get("In-Reply-To", ""),
                        source_id=message_id,
                        channel=folder,
                        metadata={
                            "message_id": message_id,
                            "folder": folder,
                            "uid": uid.decode("ascii"),
                            "account": self._account_id,
                            "provider": self._provider,
                        },
                    )

            self._items_synced = synced
            self._items_total = total
        finally:
            self._close(imap)

    # ------------------------------------------------------------------
    # declarative specs
    # ------------------------------------------------------------------

    def mcp_tools(self) -> List[ToolSpec]:
        """Declarative specs for the connector API surface.

        NOTE: specs returned here are enumerated by the connectors router
        for display; they are NOT what the agent executes. Executable
        tools must be BaseTool subclasses registered in ToolRegistry,
        which is what MCPServer.get_tools() feeds to the agent builder.
        """
        return [
            ToolSpec(
                name="mailbox_usage_report",
                description=(
                    "Report what is consuming mailbox storage: totals per folder, "
                    "heaviest senders, and largest individual messages."
                ),
                parameters={
                    "type": "object",
                    "properties": {
                        "account": {"type": "string", "description": "Account id"},
                        "top_senders": {"type": "integer", "default": 15},
                        "top_messages": {"type": "integer", "default": 25},
                    },
                },
                category="communication",
                latency_estimate=20.0,
                timeout_seconds=300.0,
            ),
            ToolSpec(
                name="mailbox_find_messages",
                description=(
                    "Find messages by sender, subject, minimum size, or age. "
                    "Returns folder and uid for each hit."
                ),
                parameters={
                    "type": "object",
                    "properties": {
                        "account": {"type": "string"},
                        "folder": {"type": "string"},
                        "from_addr": {"type": "string"},
                        "subject": {"type": "string"},
                        "larger_than_bytes": {"type": "integer", "default": 0},
                        "limit": {"type": "integer", "default": 200},
                    },
                },
                category="communication",
                latency_estimate=15.0,
                timeout_seconds=300.0,
            ),
            ToolSpec(
                name="mailbox_move_to_trash",
                description=(
                    "Move specific messages to trash. Destructive. Runs as a dry "
                    "run unless explicitly confirmed."
                ),
                parameters={
                    "type": "object",
                    "properties": {
                        "account": {"type": "string"},
                        "folder": {"type": "string"},
                        "uids": {"type": "array", "items": {"type": "string"}},
                        "dry_run": {"type": "boolean", "default": True},
                    },
                    "required": ["folder", "uids"],
                },
                category="communication",
                requires_confirmation=True,
                required_capabilities=["mail.write"],
                timeout_seconds=120.0,
            ),
            ToolSpec(
                name="mailbox_empty_folder",
                description=(
                    "Permanently delete every message in a folder, normally trash. "
                    "Irreversible. Runs as a dry run unless explicitly confirmed."
                ),
                parameters={
                    "type": "object",
                    "properties": {
                        "account": {"type": "string"},
                        "folder": {"type": "string"},
                        "dry_run": {"type": "boolean", "default": True},
                    },
                    "required": ["folder"],
                },
                category="communication",
                requires_confirmation=True,
                required_capabilities=["mail.write"],
                timeout_seconds=300.0,
            ),
        ]
