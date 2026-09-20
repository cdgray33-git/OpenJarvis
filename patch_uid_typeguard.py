#!/usr/bin/env python3
"""
patch_uid_typeguard.py  -  marker: openjarvis-uid-typeguard-v1

Replaces the permissive uid coercion in MailboxMoveToTrashTool.execute with a
strict type guard:

  - a STRING for `uids` is rejected outright (this is what split into junk
    tokens like "['1001'" and produced drifting uid_count on the 08/12 run)
  - every uid must be a digit string; anything else is rejected with a sample

Dry run by default. Pass --apply to write.

  python patch_uid_typeguard.py
  python patch_uid_typeguard.py --apply
"""

import argparse
import os
import py_compile
import shutil
import sys
import tempfile
import time

MARKER = "openjarvis-uid-typeguard-v1"
DEFAULT_REL = os.path.join("src", "openjarvis", "tools", "mailbox_tools.py")

ANCHOR = 'if isinstance(uids, str):'
EXPECT_PREV = 'uids = params.get("uids") or []'
EXPECT_NEXT1 = 'uids = [u.strip() for u in uids.split(",") if u.strip()]'
EXPECT_NEXT2 = 'uids = [str(u) for u in uids]'

NEW_BLOCK = '''{i}# {marker}
{i}uids = params.get("uids")
{i}if isinstance(uids, (str, bytes)) or not isinstance(uids, (list, tuple)):
{i}    return ToolResult(
{i}        tool_name=self.tool_id,
{i}        content=_dump({{
{i}            "error": (
{i}                "uids must be a JSON array of numeric uid strings taken "
{i}                "from a prior mailbox_find_messages result. A string was "
{i}                "rejected. Do not construct uids yourself."
{i}            ),
{i}            "received_type": type(uids).__name__,
{i}        }}),
{i}        success=False,
{i}    )
{i}uids = [str(u).strip() for u in uids]
{i}_bad = [u for u in uids if not u.isdigit()]
{i}if _bad:
{i}    return ToolResult(
{i}        tool_name=self.tool_id,
{i}        content=_dump({{
{i}            "error": (
{i}                "uids must be numeric strings from mailbox_find_messages. "
{i}                "Non-numeric values were rejected and nothing was moved."
{i}            ),
{i}            "invalid_sample": _bad[:5],
{i}            "invalid_count": len(_bad),
{i}        }}),
{i}        success=False,
{i}    )
'''


def fail(msg):
    print("ABORT: " + msg)
    sys.exit(1)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--path", default=None, help="path to mailbox_tools.py")
    ap.add_argument("--apply", action="store_true", help="write the change")
    args = ap.parse_args()

    target = args.path or DEFAULT_REL
    if not os.path.isfile(target):
        fail("file not found: " + os.path.abspath(target))

    with open(target, "rb") as fh:
        raw = fh.read()
    text = raw.decode("utf-8")

    if raw.startswith(b"\xef\xbb\xbf"):
        fail("file has a UTF-8 BOM; not touching it")

    if MARKER in text:
        print("Already patched (marker present). Nothing to do.")
        return

    newline = "\r\n" if "\r\n" in text else "\n"
    lines = text.split(newline)

    hits = [n for n, ln in enumerate(lines) if ln.strip() == ANCHOR]
    if len(hits) != 1:
        fail("expected exactly 1 anchor line %r, found %d" % (ANCHOR, len(hits)))
    i = hits[0]

    if i < 1 or i + 2 >= len(lines):
        fail("anchor too close to file edge")

    checks = [
        (i - 1, EXPECT_PREV),
        (i + 1, EXPECT_NEXT1),
        (i + 2, EXPECT_NEXT2),
    ]
    for idx, expected in checks:
        if lines[idx].strip() != expected:
            fail("line %d does not match expected source.\n  expected: %s\n  found:    %s"
                 % (idx + 1, expected, lines[idx].strip()))

    indent = lines[i][: len(lines[i]) - len(lines[i].lstrip())]
    block = NEW_BLOCK.format(i=indent, marker=MARKER).rstrip("\n").split("\n")

    new_lines = lines[: i - 1] + block + lines[i + 3 :]
    new_text = newline.join(new_lines)

    print("Target : " + os.path.abspath(target))
    print("Anchor : line %d" % (i + 1))
    print("Replacing %d lines with %d lines" % (4, len(block)))
    print("Size   : %d -> %d bytes" % (len(raw), len(new_text.encode("utf-8"))))

    tmp = os.path.join(tempfile.gettempdir(), "uidguard_check.py")
    with open(tmp, "w", encoding="utf-8", newline="") as fh:
        fh.write(new_text)
    try:
        py_compile.compile(tmp, doraise=True)
    except Exception as exc:
        os.unlink(tmp)
        fail("py_compile FAILED on the proposed result, nothing written:\n  " + str(exc))
    os.unlink(tmp)
    print("py_compile: OK (on proposed result)")

    if not args.apply:
        print("\nDRY RUN. Re-run with --apply to write.")
        return

    stamp = time.strftime("%Y%m%d_%H%M%S")
    backup = target + ".bak-uidguard-" + stamp
    shutil.copy2(target, backup)
    print("Backup : " + backup)

    with open(target, "w", encoding="utf-8", newline="") as fh:
        fh.write(new_text)

    try:
        py_compile.compile(target, doraise=True)
    except Exception as exc:
        shutil.copy2(backup, target)
        fail("py_compile FAILED after write; file REVERTED from backup:\n  " + str(exc))

    with open(target, "r", encoding="utf-8") as fh:
        check = fh.read()
    if MARKER not in check:
        shutil.copy2(backup, target)
        fail("marker missing after write; file REVERTED from backup")

    print("APPLIED and verified.")
    print("Rollback: Copy-Item '%s' '%s' -Force" % (backup, target))


if __name__ == "__main__":
    main()
