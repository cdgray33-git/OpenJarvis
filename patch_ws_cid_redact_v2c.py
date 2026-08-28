#!/usr/bin/env python3
"""
patch_ws_cid_redact_v2c.py
Marker: openjarvis-ws-cid-redact-v2

Widens the confirm_id redaction in src/openjarvis/server/ws_bridge.py so it
covers TOOL_CONFIRM_RESOLVED as well as TOOL_CONFIRM_REQUEST.

Closes SDP open item 1. The resolved frame is broadcast 4 ms BEFORE
tool_call_start, so an unauthenticated local subscriber currently learns a valid
confirm_id, its tool, its turn_id and the fact of approval at the instant
execution begins. Replay is blocked by the 409 write-once, but disclosure is not.

FOUR edits:
  1. the predicate  (_is_confirm_request -> _is_confirm_event, widened test)
  2. its use in the per-client branch
  3. the warning text, so it names the actual frame type instead of hardcoding
     TOOL_CONFIRM_REQUEST (a widened predicate with the old text would log a
     false statement)
  4. the forward-loop marker comment, v1 -> v2, so the change greps back

MARKER NOTE, found by the v2 dry run aborting: "# openjarvis-ws-cid-redact-v1"
appears TWICE at the same indent - forward-loop block and accept-site block. It
is NOT a unique anchor. The forward-loop one is located positionally (the line
above the predicate, asserted) and bumped; the accept-site one correctly stays
v1 because that block is unchanged by this patch.

EOL SAFETY: ws_bridge.py is pure CRLF. This splits on "\\n" and rejoins on
"\\n", which is byte-identical on a mixed or CRLF file because each stray "\\r"
stays attached to the end of its line. Anchors are compared with "\\r" stripped.
Inserted lines are given a trailing "\\r" to match surrounding style.

Usage, PowerShell, from PS C:\\Users\\Admin\\OpenJarvis>:
    python .\\patch_ws_cid_redact_v2c.py            (dry run, writes nothing)
    python .\\patch_ws_cid_redact_v2c.py --apply    (backs up, then writes)

A RESTART of the backend is required after --apply. The running process holds
the old code.
"""

import hashlib
import os
import py_compile
import shutil
import sys
import tempfile
from datetime import datetime

TARGET = os.path.join("src", "openjarvis", "server", "ws_bridge.py")
MARKER = "openjarvis-ws-cid-redact-v2"

V1_MARKER = "        # openjarvis-ws-cid-redact-v1"
PREDICATE = "        _is_confirm_request = event.event_type is EventType.TOOL_CONFIRM_REQUEST"

# NOTE: the v1 marker appears TWICE at this indent - once on the forward-loop
# block and once on the accept-site block. It is not a unique anchor. Only the
# forward-loop one is bumped, and it is located POSITIONALLY as the line
# immediately above the predicate, with an assertion that it really is the v1
# marker. The accept-site marker correctly stays v1: that block does not change.

# (anchor_stripped, replacement_stripped, description)
EDITS = [
    (
        PREDICATE,
        "        _is_confirm_event = event.event_type in (\n"
        "            EventType.TOOL_CONFIRM_REQUEST,\n"
        "            EventType.TOOL_CONFIRM_RESOLVED,\n"
        "        )",
        "predicate widened to both confirm event types",
    ),
    (
        '            if _is_confirm_request and not getattr(ws, "_ws_authed", False):',
        '            if _is_confirm_event and not getattr(ws, "_ws_authed", False):',
        "per-client branch uses the widened predicate",
    ),
    (
        '                        "ws-cid-redact: stripped confirm_id from "',
        '                        "ws-cid-redact: stripped confirm_id from %s "',
        "warning text part 1 - frame type becomes a parameter",
    ),
    (
        '                        "TOOL_CONFIRM_REQUEST for unauthenticated subscriber %s",',
        '                        "for unauthenticated subscriber %s",\n'
        "                        event.event_type.value,",
        "warning text part 2 plus the event-type argument",
    ),
]


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest().upper()


def eol_counts(text):
    crlf = text.count("\r\n")
    bare = text.count("\n") - crlf
    return crlf, bare


def main():
    apply = "--apply" in sys.argv

    if not os.path.isfile(TARGET):
        print("ABORT: not found: %s" % TARGET)
        print("Run this from the repo root, PS C:\\Users\\Admin\\OpenJarvis>")
        return 1

    with open(TARGET, "r", encoding="utf-8", newline="") as fh:
        original = fh.read()

    pre_bytes = len(original.encode("utf-8"))
    pre_crlf, pre_bare = eol_counts(original)
    pre_hash = sha256(TARGET)

    print("TARGET      : %s" % TARGET)
    print("PRE  bytes  : %d" % pre_bytes)
    print("PRE  EOL    : CRLF %d / bare LF %d" % (pre_crlf, pre_bare))
    print("PRE  SHA256 : %s" % pre_hash)
    print("")

    if MARKER in original:
        print("ABORT: marker %s already present. Already applied." % MARKER)
        return 1

    lines = original.split("\n")

    # Round-trip control BEFORE any change.
    if "\n".join(lines) != original:
        print("ABORT: split/join round trip is not byte-identical.")
        return 1
    print("control: split/join round trip byte-identical  OK")

    inserted_lines = 0

    # Forward-loop marker bump, located positionally. Same line count in and
    # out, so it cannot shift the indices the EDITS loop then resolves.
    phits = [i for i, ln in enumerate(lines) if ln.rstrip("\r") == PREDICATE]
    if len(phits) != 1:
        print("ABORT: predicate anchor matched %d times (need exactly 1)." % len(phits))
        return 1
    midx = phits[0] - 1
    if midx < 0 or lines[midx].rstrip("\r") != V1_MARKER:
        print("ABORT: line above the predicate is not the v1 marker.")
        print("       expected %r" % V1_MARKER)
        print("       found    %r" % (lines[midx] if midx >= 0 else "<start of file>"))
        return 1
    _cr = "\r" if lines[midx].endswith("\r") else ""
    lines[midx] = "        # " + MARKER + _cr
    print("marker bumped  line %-4d  forward-loop block only (accept site stays v1)" % (midx + 1))

    for anchor, replacement, desc in EDITS:
        hits = [i for i, ln in enumerate(lines) if ln.rstrip("\r") == anchor]
        if len(hits) != 1:
            print("ABORT: anchor matched %d times (need exactly 1): %s" % (len(hits), desc))
            print("       %r" % anchor)
            return 1
        idx = hits[0]
        had_cr = lines[idx].endswith("\r")
        new_lines = replacement.split("\n")
        if had_cr:
            new_lines = [nl + "\r" for nl in new_lines]
        lines[idx:idx + 1] = new_lines
        inserted_lines += len(new_lines) - 1
        print("anchor matched 1  line %-4d  %s" % (idx + 1, desc))

    patched = "\n".join(lines)

    post_crlf, post_bare = eol_counts(patched)
    expected_crlf = pre_crlf + inserted_lines
    print("")
    print("lines inserted net : %d" % inserted_lines)
    print("POST EOL           : CRLF %d / bare LF %d" % (post_crlf, post_bare))
    print("EOL control        : CRLF expected %d  %s | bare LF expected %d  %s" % (
        expected_crlf, "OK" if post_crlf == expected_crlf else "FAIL",
        pre_bare, "OK" if post_bare == pre_bare else "FAIL"))
    if post_crlf != expected_crlf or post_bare != pre_bare:
        print("ABORT: EOL control failed.")
        return 1

    # Syntax control on the patched text, before anything touches the real file.
    tmp = tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False,
                                      encoding="utf-8", newline="")
    tmp.write(patched)
    tmp.close()
    try:
        py_compile.compile(tmp.name, doraise=True)
        print("py_compile on patched text  OK")
    except py_compile.PyCompileError as exc:
        print("ABORT: py_compile failed on patched text:")
        print(exc)
        return 1
    finally:
        os.unlink(tmp.name)

    # Positive controls: things that must still be true after the patch.
    controls = [
        ("\n    EventType.TOOL_CONFIRM_RESOLVED,", 1, "subscribed set entry intact (4-space indent)"),
        ("\n            EventType.TOOL_CONFIRM_RESOLVED,", 1, "resolved type added to predicate (12-space indent)"),
        ("\n            EventType.TOOL_CONFIRM_REQUEST,", 1, "request type in predicate (12-space indent)"),
        ("_is_confirm_event", 2, "widened predicate defined once, used once"),
        ("_is_confirm_request", 0, "old identifier fully removed"),
        ('_had_cid = _data.pop("confirm_id", None) is not None', 1, "cid pop guard untouched"),
        ("websocket._ws_authed = _authed", 1, "accept-site auth assignment untouched"),
        (MARKER, 1, "new v2 marker present exactly once"),
        ("openjarvis-ws-cid-redact-v1", 1, "v1 marker remains on the accept site only"),
    ]
    print("")
    ok = True
    for needle, want, desc in controls:
        got = patched.count(needle)
        flag = "OK" if got == want else "FAIL"
        if got != want:
            ok = False
        print("control: %-58s want %d got %d  %s" % (desc, want, got, flag))
    if not ok:
        print("ABORT: a positive control failed.")
        return 1

    post_bytes = len(patched.encode("utf-8"))
    print("")
    print("PRE  bytes : %d" % pre_bytes)
    print("POST bytes : %d  (delta %+d)" % (post_bytes, post_bytes - pre_bytes))

    if not apply:
        print("")
        print("DRY RUN. Nothing written. Re-run with --apply to write.")
        return 0

    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup = "%s.bak_cidredactv2_%s" % (TARGET, stamp)
    shutil.copy2(TARGET, backup)
    print("")
    print("BACKUP : %s" % backup)

    with open(TARGET, "w", encoding="utf-8", newline="") as fh:
        fh.write(patched)

    on_disk = os.path.getsize(TARGET)
    print("WRITTEN: %s" % TARGET)
    print("on-disk bytes %d  predicted %d  %s" % (
        on_disk, post_bytes, "OK" if on_disk == post_bytes else "FAIL"))
    print("POST SHA256 : %s" % sha256(TARGET))

    try:
        py_compile.compile(TARGET, doraise=True)
        print("py_compile on written file  OK")
    except py_compile.PyCompileError as exc:
        print("WARNING: py_compile failed on the written file:")
        print(exc)
        print("RESTORE: Copy-Item '%s' '%s' -Force" % (backup, TARGET))
        return 1

    print("")
    print("APPLIED. RESTART THE BACKEND - the running process holds the old code.")
    print("RESTORE: Copy-Item '%s' '%s' -Force" % (backup, TARGET))
    return 0


if __name__ == "__main__":
    sys.exit(main())
