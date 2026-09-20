"""
patch_filter_move.py - marker openjarvis-filter-move-v1

Adds optional from_addr to mailbox_move_to_trash so the TOOL resolves uids
server-side. The model passes a sender substring and never carries a uid list.

Guarded: backup, anchor checks, abort-if-already-patched, py_compile,
auto-revert on failure.

Usage, PowerShell, repo root:
    python -u patch_filter_move.py            # dry run, reports only
    python -u patch_filter_move.py --apply
"""

import datetime
import os
import py_compile
import shutil
import sys
import tempfile

TARGET = os.path.join("src", "openjarvis", "tools", "mailbox_tools.py")
MARKER = "openjarvis-filter-move-v1"

# ---------------------------------------------------------------- anchor 1
# spec: add the from_addr property just before dry_run
A1_OLD = '''                    "uids": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Message uids from mailbox_find_messages",
                    },
                    "dry_run": {"type": "boolean", "default": True},'''

A1_NEW = '''                    "uids": {
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
                    "dry_run": {"type": "boolean", "default": True},'''

# ---------------------------------------------------------------- anchor 2
A2_OLD = '''                "required": ["folder", "uids"],'''
A2_NEW = '''                "required": ["folder"],'''

# ---------------------------------------------------------------- anchor 3
# execute: resolve from_addr to uids BEFORE the uid type guard runs
A3_OLD = '''        folder = str(params.get("folder", "") or "")
        # openjarvis-uid-typeguard-v1'''

A3_NEW = '''        folder = str(params.get("folder", "") or "")

        # openjarvis-filter-move-v1
        # Server-side selection. The model passes a sender substring; the tool
        # resolves it to uids here so no uid list ever crosses the model.
        _from_addr = str(params.get("from_addr", "") or "").strip()
        _resolved = 0
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
                _hits = conn.find_messages(from_addr=_from_addr, limit=5000)
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

        # openjarvis-uid-typeguard-v1'''

# ---------------------------------------------------------------- anchor 4
# surface how the uids were obtained in the result
A4_OLD = '''            logger.exception("mailbox_move_to_trash failed")
            return ToolResult(
                tool_name=self.tool_id,
                content=_dump({"error": str(exc)}),
                success=False,
            )

        return ToolResult(
            tool_name=self.tool_id,
            content=_dump(result),
            success=bool(result.get("applied")),
        )'''

A4_NEW = '''            logger.exception("mailbox_move_to_trash failed")
            return ToolResult(
                tool_name=self.tool_id,
                content=_dump({"error": str(exc)}),
                success=False,
            )

        if _resolved and isinstance(result, dict):
            result = dict(result)
            result["selected_by"] = "from_addr"
            result["from_addr"] = _from_addr
            result["resolved_uid_count"] = _resolved

        return ToolResult(
            tool_name=self.tool_id,
            content=_dump(result),
            success=bool(result.get("applied")),
        )'''

EDITS = [
    ("spec from_addr property", A1_OLD, A1_NEW),
    ("required list", A2_OLD, A2_NEW),
    ("execute resolution block", A3_OLD, A3_NEW),
    ("result annotation", A4_OLD, A4_NEW),
]


def main() -> int:
    apply = "--apply" in sys.argv

    if not os.path.isfile(TARGET):
        print("ABORT: %s not found. Run from repo root." % TARGET)
        return 2

    with open(TARGET, "r", encoding="utf-8", newline="") as fh:
        src = fh.read()

    eol = "\r\n" if "\r\n" in src else "\n"
    print("target   : %s" % TARGET)
    print("size     : %d bytes" % len(src.encode("utf-8")))
    print("eol      : %s" % ("CRLF" if eol == "\r\n" else "LF"))

    if MARKER in src:
        print("ABORT: already patched (marker %s present). Nothing to do." % MARKER)
        return 0

    # control pattern - must match, proves the grep works at all
    if "class MailboxMoveToTrashTool" not in src:
        print("ABORT: control pattern missing. Wrong file?")
        return 2

    flat = src.replace("\r\n", "\n")
    for label, old, _new in EDITS:
        n = flat.count(old)
        print("anchor   : %-26s matches=%d" % (label, n))
        if n != 1:
            print("ABORT: anchor '%s' matched %d times, expected 1." % (label, n))
            return 2

    out = flat
    for _label, old, new in EDITS:
        out = out.replace(old, new, 1)

    if eol == "\r\n":
        out = out.replace("\n", "\r\n")

    print("post     : %d bytes (delta %+d)"
          % (len(out.encode("utf-8")),
             len(out.encode("utf-8")) - len(src.encode("utf-8"))))

    # compile the candidate before touching the real file
    tmp = tempfile.NamedTemporaryFile("w", suffix=".py", delete=False,
                                      encoding="utf-8", newline="")
    tmp.write(out)
    tmp.close()
    try:
        py_compile.compile(tmp.name, doraise=True)
        print("compile  : OK")
    except Exception as exc:
        print("ABORT: candidate failed to compile: %s" % exc)
        return 2
    finally:
        os.unlink(tmp.name)

    if not apply:
        print("")
        print("DRY RUN. All 4 anchors matched and the result compiles.")
        print("Re-run with --apply to write.")
        return 0

    stamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    bak = "%s.bak-filtermove-%s" % (TARGET, stamp)
    shutil.copy2(TARGET, bak)
    print("backup   : %s" % bak)

    with open(TARGET, "w", encoding="utf-8", newline="") as fh:
        fh.write(out)

    try:
        py_compile.compile(TARGET, doraise=True)
    except Exception as exc:
        shutil.copy2(bak, TARGET)
        print("ABORT: post-write compile failed, REVERTED. %s" % exc)
        return 2

    with open(TARGET, "r", encoding="utf-8") as fh:
        chk = fh.read()
    for token in (MARKER, "openjarvis-uid-typeguard-v1", '"from_addr": {'):
        if token not in chk:
            shutil.copy2(bak, TARGET)
            print("ABORT: verify missed %r, REVERTED." % token)
            return 2

    print("APPLIED  : OK. Restart the backend to load it.")
    print("REVERT   : Copy-Item '%s' '%s' -Force" % (bak, TARGET))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
