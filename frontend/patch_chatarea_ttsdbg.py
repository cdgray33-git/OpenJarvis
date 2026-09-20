# MARKER: openjarvis-patch-chatarea-ttsdbg-v1
"""
Temporary instrumentation for the OpenJarvis TTS driver effect in ChatArea.tsx.

Inserts two console.log statements:
  * after line 119 (`let take = fullText.length;`) -- fires on EVERY effect run
    that gets past the role/id guards, so a driver that silently bails at the
    line 124 or 128 early-returns is distinguishable from an effect that never
    re-ran at all.
  * at line 144 (`if (plainText) enqueue(plainText);`) -- fires only on an
    actual handover to ttsPlayer.

Both lines are tagged [TTSDBG] for console filtering.

Operates on BYTE lines and preserves the file's existing line terminator,
because ChatArea.tsx carries mojibake and must never be round-tripped through
a text decoder.

Dry-run by default. Pass --apply to write. Backs up to .bak_<timestamp>.
THIS IS TEMPORARY DEBUG CODE -- revert from the .bak before any commit.
"""

import argparse
import hashlib
import os
import sys
import time

MARKER = "openjarvis-patch-chatarea-ttsdbg-v1"

REL_PATH = os.path.join("src", "components", "Chat", "ChatArea.tsx")

# 1-based line numbers and their expected content (compared after .strip())
ANCHOR_TAKE = 119
ANCHOR_TAKE_TEXT = "let take = fullText.length;"

ANCHOR_ENQUEUE = 144
ANCHOR_ENQUEUE_TEXT = "if (plainText) enqueue(plainText);"

# Inserted after ANCHOR_TAKE. Indentation matches the surrounding block (4 sp).
LOG_TAKE = (
    "    console.log('[TTSDBG] run', Date.now(), "
    "'stream=' + streamState.isStreaming, "
    "'len=' + fullText.length, "
    "'spoken=' + spokenCharsRef.current);"
)

# Replaces ANCHOR_ENQUEUE.
LOG_ENQUEUE = (
    "    if (plainText) { console.log('[TTSDBG] enqueue', Date.now(), "
    "'stream=' + streamState.isStreaming, "
    "'seg=' + plainText.length, "
    "'spoken=' + spokenCharsRef.current); enqueue(plainText); }"
)


def self_check():
    """Verify this script's own payload survived delivery intact.

    A previous delivery arrived with characters stripped, so the payload is
    asserted before it is allowed anywhere near the real file.
    """
    problems = []
    if "[TTSDBG] run" not in LOG_TAKE:
        problems.append("LOG_TAKE lost its tag")
    if "[TTSDBG] enqueue" not in LOG_ENQUEUE:
        problems.append("LOG_ENQUEUE lost its tag")
    if LOG_ENQUEUE.count("'") != 8:
        problems.append(
            "LOG_ENQUEUE quote count is %d, expected 8" % LOG_ENQUEUE.count("'")
        )
    if LOG_TAKE.count("'") != 8:
        problems.append(
            "LOG_TAKE quote count is %d, expected 8" % LOG_TAKE.count("'")
        )
    if "enqueue(plainText);" not in LOG_ENQUEUE:
        problems.append("LOG_ENQUEUE no longer calls enqueue")
    if LOG_ENQUEUE.count("{") != 1 or LOG_ENQUEUE.count("}") != 1:
        problems.append("LOG_ENQUEUE brace count wrong")
    if problems:
        print("PAYLOAD SELF-CHECK FAILED:")
        for p in problems:
            print("  - " + p)
        return False
    print("payload self-check OK")
    return True


def sha256(data):
    return hashlib.sha256(data).hexdigest().upper()


def detect_terminator(raw):
    if b"\r\n" in raw:
        return b"\r\n"
    if b"\n" in raw:
        return b"\n"
    return b"\n"


def split_lines(raw, term):
    body = raw
    trailing = b""
    if body.endswith(term):
        body = body[: -len(term)]
        trailing = term
    return body.split(term), trailing


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--path", default=".", help="frontend dir (default: cwd)")
    ap.add_argument("--apply", action="store_true", help="write changes")
    args = ap.parse_args()

    if not self_check():
        return 2

    target = os.path.join(args.path, REL_PATH)
    if not os.path.isfile(target):
        print("NOT FOUND: %s" % target)
        print("Run this from the frontend dir, or pass --path.")
        return 2

    with open(target, "rb") as fh:
        raw = fh.read()

    print("file:   %s" % os.path.abspath(target))
    print("bytes:  %d" % len(raw))
    print("sha256: %s" % sha256(raw))

    term = detect_terminator(raw)
    print("term:   %s" % ("CRLF" if term == b"\r\n" else "LF"))

    lines, trailing = split_lines(raw, term)
    print("lines:  %d" % len(lines))

    if MARKER.encode("ascii") in raw or b"[TTSDBG]" in raw:
        print("")
        print("ALREADY INSTRUMENTED -- [TTSDBG] found in the file. Refusing.")
        print("Restore the .bak first if you want to re-apply.")
        return 3

    ok = True
    for lineno, expected in (
        (ANCHOR_TAKE, ANCHOR_TAKE_TEXT),
        (ANCHOR_ENQUEUE, ANCHOR_ENQUEUE_TEXT),
    ):
        if lineno > len(lines):
            print("ANCHOR %d: MISSING (file has %d lines)" % (lineno, len(lines)))
            ok = False
            continue
        actual = lines[lineno - 1].decode("latin-1").strip()
        if actual == expected:
            print("ANCHOR %d: OK  %s" % (lineno, expected))
        else:
            print("ANCHOR %d: MISMATCH" % lineno)
            print("  expected: %r" % expected)
            print("  actual:   %r" % actual)
            ok = False

    if not ok:
        print("")
        print("ABORTED -- no anchor match, nothing written.")
        return 4

    # Apply bottom-up so the first edit does not shift the second anchor.
    out = list(lines)
    out[ANCHOR_ENQUEUE - 1] = LOG_ENQUEUE.encode("ascii")
    out.insert(ANCHOR_TAKE, LOG_TAKE.encode("ascii"))

    new_raw = term.join(out) + trailing

    print("")
    print("--- predicted result ---")
    print("lines:  %d -> %d" % (len(lines), len(out)))
    print("bytes:  %d -> %d" % (len(raw), len(new_raw)))
    print("sha256: %s" % sha256(new_raw))
    print("")
    print("--- new lines 118-122 ---")
    for i in range(117, 122):
        print("%3d: %s" % (i + 1, out[i].decode("latin-1")))
    print("")
    print("--- new line 145 (was 144) ---")
    print("%3d: %s" % (145, out[144].decode("latin-1")))

    if not args.apply:
        print("")
        print("DRY RUN -- nothing written. Re-run with --apply.")
        return 0

    stamp = time.strftime("%Y%m%d_%H%M%S")
    backup = target + ".bak_" + stamp
    with open(backup, "wb") as fh:
        fh.write(raw)
    print("")
    print("backup: %s" % backup)

    with open(target, "wb") as fh:
        fh.write(new_raw)

    with open(target, "rb") as fh:
        check = fh.read()
    print("on-disk bytes:  %d" % len(check))
    print("on-disk sha256: %s" % sha256(check))
    print("matches prediction: %s" % (sha256(check) == sha256(new_raw)))
    print("")
    print("Now: npm run build:tauri   (served bundle on 8010)")
    print("REMEMBER: this is temporary debug code. Revert from the .bak.")
    return 0


if __name__ == "__main__":
    sys.exit(main())