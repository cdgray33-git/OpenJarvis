# MARKER: openjarvis-patch-ttsplayer-pumpdbg-v1
"""
Temporary instrumentation for the OpenJarvis TTS pump.

Measured 08/09: unit 1's audio bytes were in hand 11.3 s before the voice was
heard, and unit 2's request did not fire until 212 ms AFTER the stream ended.
Something inside pump() blocks for ~11 s between one unit finishing and the next
starting. This logs a timestamp and elapsed-ms at every phase boundary in the
loop so the blocking await is named rather than inferred:

  [PUMPDBG] take       loop iteration entered, unit size, queue depth
  [PUMPDBG] fetched    synthesizeSpeech resolved, blob size
  [PUMPDBG] buffered   blob.arrayBuffer resolved
  [PUMPDBG] ctx        AudioContext state and currentTime BEFORE decode
  [PUMPDBG] decoded    decodeAudioData resolved, buffer duration
  [PUMPDBG] scheduled  after schedule(), context state and nextStartTime

The ctx lines are the point of the exercise. A suspended AudioContext would
explain both symptoms at once -- decodeAudioData stalling and src.start()
producing no sound while currentTime stays frozen.

Two edits, applied bottom-up so the first does not shift the second's anchors.
Operates on BYTE lines and preserves the file's line terminator (ttsPlayer.ts
is LF; ChatArea.tsx is CRLF -- never assume).

Dry-run by default. Pass --apply to write. Backs up to .bak_<timestamp>.
THIS IS TEMPORARY DEBUG CODE -- revert from the .bak before any commit.
"""

import argparse
import hashlib
import os
import sys
import time

MARKER = "openjarvis-patch-ttsplayer-pumpdbg-v1"
SENTINEL = "[PUMPDBG]"

REL_PATH = os.path.join("src", "audio", "ttsPlayer.ts")

# Each edit: (first_line, last_line, [replacement lines]) -- 1-based inclusive.
# ANCHORS are checked before anything is written.
ANCHORS = [
    (245, "const unit = pending.shift() as string;"),
    (246, "let buffer: AudioBuffer;"),
    (247, ""),
    (248, "try {"),
    (249, "const blob = await synthesizeSpeech(unit);"),
    (250, "if (myGeneration !== generation) return;"),
    (251, ""),
    (252, "const bytes = await blob.arrayBuffer();"),
    (253, "const context = ensureContext();"),
    (254, "if (!context) return;"),
    (255, ""),
    (256, "buffer = await context.decodeAudioData(bytes.slice(0));"),
    (266, "if (myGeneration !== generation) return;"),
    (267, "schedule(buffer);"),
]

BLOCK_A = [
    "      const unit = pending.shift() as string;",
    "      let buffer: AudioBuffer;",
    "      const t0 = Date.now();",
    "      console.log('[PUMPDBG] take', t0, 'chars=' + unit.length, 'pending=' + pending.length);",
    "",
    "      try {",
    "        const blob = await synthesizeSpeech(unit);",
    "        const t1 = Date.now();",
    "        console.log('[PUMPDBG] fetched', t1, '+' + (t1 - t0) + 'ms', 'bytes=' + blob.size);",
    "        if (myGeneration !== generation) return;",
    "",
    "        const bytes = await blob.arrayBuffer();",
    "        const t2 = Date.now();",
    "        console.log('[PUMPDBG] buffered', t2, '+' + (t2 - t1) + 'ms');",
    "        const context = ensureContext();",
    "        if (!context) return;",
    "        console.log('[PUMPDBG] ctx', Date.now(), 'state=' + context.state, 'currentTime=' + context.currentTime.toFixed(3));",
    "",
    "        buffer = await context.decodeAudioData(bytes.slice(0));",
    "        const t3 = Date.now();",
    "        console.log('[PUMPDBG] decoded', t3, '+' + (t3 - t2) + 'ms', 'dur=' + buffer.duration.toFixed(2) + 's');",
]

BLOCK_B = [
    "      if (myGeneration !== generation) return;",
    "      schedule(buffer);",
    "      console.log('[PUMPDBG] scheduled', Date.now(), 'state=' + (ctx ? ctx.state : 'null'), 'now=' + (ctx ? ctx.currentTime.toFixed(3) : '-'), 'next=' + nextStartTime.toFixed(3));",
]

EDITS = [
    (245, 256, BLOCK_A),
    (266, 267, BLOCK_B),
]


def self_check():
    """Verify the payload survived delivery before it touches the real file."""
    problems = []
    text = "\n".join(BLOCK_A + BLOCK_B)
    if text.count(SENTINEL) != 6:
        problems.append("expected 6 PUMPDBG tags, found %d" % text.count(SENTINEL))
    if text.count("(") != text.count(")"):
        problems.append(
            "paren imbalance: %d open, %d close" % (text.count("("), text.count(")"))
        )
    if text.count("'") % 2 != 0:
        problems.append("odd number of single quotes: %d" % text.count("'"))
    for needed in (
        "await synthesizeSpeech(unit)",
        "await blob.arrayBuffer()",
        "await context.decodeAudioData(bytes.slice(0))",
        "schedule(buffer);",
        "context.state",
        "nextStartTime.toFixed(3)",
    ):
        if needed not in text:
            problems.append("lost required fragment: %s" % needed)
    if problems:
        print("PAYLOAD SELF-CHECK FAILED:")
        for p in problems:
            print("  - " + p)
        return False
    print("payload self-check OK (%d lines)" % len(BLOCK_A + BLOCK_B))
    return True


def sha256(data):
    return hashlib.sha256(data).hexdigest().upper()


def detect_terminator(raw):
    if b"\r\n" in raw:
        return b"\r\n"
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

    if SENTINEL.encode("ascii") in raw or MARKER.encode("ascii") in raw:
        print("")
        print("ALREADY INSTRUMENTED -- PUMPDBG found in the file. Refusing.")
        return 3

    ok = True
    for lineno, expected in ANCHORS:
        if lineno > len(lines):
            print("ANCHOR %d: MISSING (file has %d lines)" % (lineno, len(lines)))
            ok = False
            continue
        actual = lines[lineno - 1].decode("latin-1").strip()
        if actual == expected:
            shown = expected if expected else "<blank>"
            print("ANCHOR %d: OK  %s" % (lineno, shown))
        else:
            print("ANCHOR %d: MISMATCH" % lineno)
            print("  expected: %r" % expected)
            print("  actual:   %r" % actual)
            ok = False

    if not ok:
        print("")
        print("ABORTED -- anchors did not match, nothing written.")
        return 4

    out = list(lines)
    # Bottom-up so an earlier edit cannot shift a later edit's line numbers.
    for first, last, block in sorted(EDITS, key=lambda e: e[0], reverse=True):
        out[first - 1 : last] = [s.encode("ascii") for s in block]

    new_raw = term.join(out) + trailing

    print("")
    print("--- predicted result ---")
    print("lines:  %d -> %d" % (len(lines), len(out)))
    print("bytes:  %d -> %d" % (len(raw), len(new_raw)))
    print("sha256: %s" % sha256(new_raw))
    print("")
    print("--- instrumented pump loop ---")
    for i in range(243, 243 + len(BLOCK_A) + 4):
        if 0 <= i < len(out):
            print("%3d: %s" % (i + 1, out[i].decode("latin-1")))

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
    print("Now: npm run build:tauri")
    print("REMEMBER: temporary debug code. Revert from the .bak.")
    return 0


if __name__ == "__main__":
    sys.exit(main())