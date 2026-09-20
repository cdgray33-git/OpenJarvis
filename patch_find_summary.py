"""patch_find_summary.py - marker openjarvis-find-summary-v1

Closes the Section 4 read/write asymmetry in MailboxFindMessagesTool:
  1. adds a `detail` parameter (summary | full), default summary
  2. raises the default limit from 200 to 5000 (parity with the move path)
  3. reports `truncated` / `total_matched` honestly, with an instruction
     string telling the model a cap is a floor and not a count

Guarded: backup, anchor count check, abort if already patched, compile the
candidate before writing, auto-revert on failure, verify tokens after write.

Run from the repo root:  python -u patch_find_summary.py
"""

from __future__ import annotations

import datetime
import shutil
import sys
from pathlib import Path

TARGET = Path("src/openjarvis/tools/mailbox_tools.py")
MARKER = "openjarvis-find-summary-v1"

# ---------------------------------------------------------------------------
# anchors: (label, old_text, new_text) - each old_text must match exactly once
# ---------------------------------------------------------------------------

A1_OLD = '@ToolRegistry.register("mailbox_find_messages")'
A1_NEW = '# ' + MARKER + '\n@ToolRegistry.register("mailbox_find_messages")'

A2_OLD = '                "to build a deletion candidate list before removing anything."'
A2_NEW = (
    '                "to build a deletion candidate list before removing anything. "\n'
    '                "Defaults to detail=summary, which returns counts grouped by "\n'
    '                "sender and folder and no message objects. Use detail=full "\n'
    '                "only when you actually need uids."'
)

A3_OLD = '                    "limit": {"type": "integer", "default": 200},'
A3_NEW = (
    '                    "limit": {"type": "integer", "default": 5000},\n'
    '                    "detail": {\n'
    '                        "type": "string",\n'
    '                        "enum": ["summary", "full"],\n'
    '                        "default": "summary",\n'
    '                        "description": (\n'
    '                            "summary returns counts grouped by sender and "\n'
    '                            "folder; full returns every message object "\n'
    '                            "including uids"\n'
    '                        ),\n'
    '                    },'
)

A4_OLD = '        before: Optional[datetime] = None'
A4_NEW = (
    '        before: Optional[datetime] = None\n'
    '        try:\n'
    '            limit = int(params.get("limit", 5000) or 5000)\n'
    '        except (TypeError, ValueError):\n'
    '            limit = 5000\n'
    '        if limit <= 0:\n'
    '            limit = 5000\n'
    '        detail = str(params.get("detail", "summary") or "summary").lower()\n'
    '        if detail not in ("summary", "full"):\n'
    '            detail = "summary"'
)

A5_OLD = '                limit=int(params.get("limit", 200) or 200),'
A5_NEW = '                limit=limit,'

A6_OLD = """        total = sum(h["bytes"] for h in hits)
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
        )"""

A6_NEW = '''        total = sum(h["bytes"] for h in hits)
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
        }
        if truncated:
            payload["note"] = (
                "RESULT TRUNCATED AT THE LIMIT. match_count is a FLOOR, not a "
                "total. Tell the user the true number is at least this many and "
                "is not yet known, and re-run with a higher limit before acting."
            )
        if detail == "full":
            payload["matches"] = hits
        return ToolResult(
            tool_name=self.tool_id,
            content=_dump(payload),
            success=True,
        )'''

ANCHORS = [
    ("1 marker", A1_OLD, A1_NEW),
    ("2 description", A2_OLD, A2_NEW),
    ("3 spec params", A3_OLD, A3_NEW),
    ("4 execute prologue", A4_OLD, A4_NEW),
    ("5 limit passthrough", A5_OLD, A5_NEW),
    ("6 return payload", A6_OLD, A6_NEW),
]

VERIFY_TOKENS = [
    MARKER,
    '"detail": {',
    '"by_address"',
    '"truncated": truncated',
    'limit=limit,',
    '"default": 5000',
]


def fail(msg: str) -> None:
    print("ABORT: " + msg)
    sys.exit(1)


def main() -> None:
    if not TARGET.exists():
        fail("target not found: " + str(TARGET) + " (run from the repo root)")

    raw = TARGET.read_bytes()
    crlf = raw.count(b"\r\n")
    lf_only = raw.count(b"\n") - crlf
    newline = "\r\n" if crlf > lf_only else "\n"
    print("line endings: " + ("CRLF" if newline == "\r\n" else "LF"))

    text = raw.decode("utf-8")
    print("pre-patch size: " + str(len(raw)) + " B")

    if MARKER in text:
        fail("marker " + MARKER + " already present - already patched")

    def conv(s: str) -> str:
        return s.replace("\n", newline) if newline == "\r\n" else s

    # count every anchor before touching anything
    for label, old, _new in ANCHORS:
        n = text.count(conv(old))
        print("anchor " + label + ": " + str(n) + " match(es)")
        if n != 1:
            fail("anchor " + label + " matched " + str(n) + " times, expected 1")

    candidate = text
    for _label, old, new in ANCHORS:
        candidate = candidate.replace(conv(old), conv(new), 1)

    try:
        compile(candidate.replace("\r\n", "\n"), str(TARGET), "exec")
    except SyntaxError as exc:
        fail("candidate failed to compile: " + str(exc))
    print("candidate compiles OK")

    stamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    backup = TARGET.with_name(TARGET.name + ".bak-findsummary-" + stamp)
    shutil.copy2(TARGET, backup)
    print("backup: " + backup.name)

    try:
        with open(TARGET, "w", encoding="utf-8", newline="") as fh:
            fh.write(candidate)

        after = TARGET.read_bytes().decode("utf-8")
        missing = [t for t in VERIFY_TOKENS if t not in after]
        if missing:
            raise RuntimeError("verify tokens missing: " + ", ".join(missing))
        compile(after.replace("\r\n", "\n"), str(TARGET), "exec")
    except Exception as exc:
        shutil.copy2(backup, TARGET)
        fail("post-write check failed, REVERTED from backup: " + str(exc))

    new_size = TARGET.stat().st_size
    print("post-patch size: " + str(new_size) + " B, delta +" + str(new_size - len(raw)))
    print("all verify tokens present")
    print("PATCHED with marker " + MARKER)
    print("")
    print("REVERT:")
    print("Copy-Item '" + str(backup).replace("/", "\\") + "' '" +
          str(TARGET).replace("/", "\\") + "' -Force")


if __name__ == "__main__":
    main()
