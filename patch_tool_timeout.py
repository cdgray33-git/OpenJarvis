#!/usr/bin/env python3
"""
patch_tool_timeout.py  -  marker: openjarvis-tool-timeout-v1

Defect 2: the tool timeout is a FALSE NEGATIVE. The ThreadPoolExecutor sits
inside the try, so shutdown(wait=True) blocks until the IMAP work finishes -
the timeout does not cancel anything and does not bound wall clock. It only
decides whether the panel tells the truth.

Change 1  src\\openjarvis\\tools\\mailbox_tools.py
    mailbox_move_to_trash timeout_seconds 300.0 -> 1800.0

Change 2  src\\openjarvis\\tools\\_stubs.py
    the TimeoutError ToolResult keeps success=False but its content now says
    the operation MAY HAVE COMPLETED and must be verified before any retry,
    plus metadata flags timed_out / outcome_verified.

Run from the repo root.
    python patch_tool_timeout.py            (dry run)
    python patch_tool_timeout.py --apply
"""

import hashlib
import os
import py_compile
import shutil
import sys
import tempfile
from datetime import datetime

MARKER = "openjarvis-tool-timeout-v1"

MAILBOX = os.path.join("src", "openjarvis", "tools", "mailbox_tools.py")
STUBS = os.path.join("src", "openjarvis", "tools", "_stubs.py")

# ---- Change 1 -------------------------------------------------------------

M_OLD = "            timeout_seconds=300.0,\n"
M_NEW = "            timeout_seconds=1800.0,  # " + MARKER + "\n"

# ---- Change 2 -------------------------------------------------------------

S_OLD = """            result = ToolResult(
                tool_name=tool_call.name,
                content=(f"Tool '{tool_call.name}' timed out after {timeout:.0f}s."),
                success=False,
            )
"""

S_NEW = """            # """ + MARKER + """
            result = ToolResult(
                tool_name=tool_call.name,
                content=(
                    f"Tool '{tool_call.name}' exceeded its {timeout:.0f}s wait. "
                    "OUTCOME UNKNOWN: the operation was NOT cancelled and may have "
                    "completed successfully. Do NOT retry it and do NOT report it "
                    "as failed. Verify the current state with a read-only check "
                    "first, then report what the verification found."
                ),
                success=False,
            )
            result.metadata["timed_out"] = True
            result.metadata["outcome_verified"] = False
"""

VERIFY_TOKENS = {
    MAILBOX: ["timeout_seconds=1800.0", MARKER],
    STUBS: [MARKER, "OUTCOME UNKNOWN", '"timed_out"', '"outcome_verified"'],
}


def sha(b):
    return hashlib.sha256(b).hexdigest().upper()


def load(path):
    with open(path, "rb") as f:
        raw = f.read()
    crlf = raw.count(b"\r\n")
    lf = raw.count(b"\n") - crlf
    eol = "CRLF" if crlf > lf else "LF"
    return raw, eol


def patch_one(path, old, new, apply_it):
    if not os.path.isfile(path):
        print("  FAIL: not found: %s" % path)
        return None
    raw, eol = load(path)
    text = raw.decode("utf-8")
    norm = text.replace("\r\n", "\n")

    if MARKER in norm:
        print("  SKIP: marker already present in %s" % path)
        return None

    n = norm.count(old)
    print("  %s" % path)
    print("    size %d B  eol %s  sha %s" % (len(raw), eol, sha(raw)[:16]))
    print("    anchor matches: %d" % n)
    if n != 1:
        print("    FAIL: anchor must match exactly once. Aborting.")
        return None

    out_norm = norm.replace(old, new)
    out = out_norm.replace("\n", "\r\n") if eol == "CRLF" else out_norm
    data = out.encode("utf-8")
    print("    new size %d B (delta %+d)" % (len(data), len(data) - len(raw)))

    fd, tmp = tempfile.mkstemp(suffix=".py")
    os.close(fd)
    with open(tmp, "wb") as f:
        f.write(data)
    try:
        py_compile.compile(tmp, doraise=True)
        print("    py_compile: OK")
    except py_compile.PyCompileError as e:
        print("    FAIL: candidate does not compile: %s" % e)
        os.unlink(tmp)
        return None
    os.unlink(tmp)

    if not apply_it:
        print("    DRY RUN - nothing written")
        return True

    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    bak = "%s.bak-tooltimeout-%s" % (path, stamp)
    shutil.copy2(path, bak)
    print("    backup: %s" % bak)
    with open(path, "wb") as f:
        f.write(data)

    chk, _ = load(path)
    ctext = chk.decode("utf-8")
    ok = True
    for t in VERIFY_TOKENS[path]:
        present = t in ctext
        print("    verify %-28s %s" % (t, "OK" if present else "MISSING"))
        ok = ok and present
    print("    written %d B  sha %s" % (len(chk), sha(chk)[:16]))
    print("    REVERT: Copy-Item '%s' '%s' -Force" % (bak, path))
    return ok


def main():
    apply_it = "--apply" in sys.argv
    print("=" * 60)
    print("patch_tool_timeout.py  %s" % ("APPLY" if apply_it else "DRY RUN"))
    print("=" * 60)

    print("\nChange 1 - move_to_trash timeout 300.0 -> 1800.0")
    r1 = patch_one(MAILBOX, M_OLD, M_NEW, apply_it)

    print("\nChange 2 - timeout ToolResult wording + metadata")
    r2 = patch_one(STUBS, S_OLD, S_NEW, apply_it)

    print("\n" + "=" * 60)
    if r1 and r2:
        print("RESULT: both changes %s" % ("APPLIED" if apply_it else "would apply cleanly"))
        if not apply_it:
            print("Re-run with --apply")
        else:
            print("Restart the backend for this to take effect.")
    else:
        print("RESULT: INCOMPLETE - read the output above. If Change 1 applied and")
        print("Change 2 did not, revert Change 1 with the printed command.")
    print("=" * 60)


if __name__ == "__main__":
    main()
