# MARKER: openjarvis-patch-ttsplayer-firstunit-v1
"""
Bound the FIRST TTS unit so time-to-first-audio stops depending on how long
the model's opening clause happens to be.

Today, splitIntoUnits lines 177-182 emit any piece longer than the cap WHOLE:

    if (piece.length > cap) {
      flush();
      units.push(piece);
      cap = max;
      continue;
    }

That is correct for later units but defeats FIRST_UNIT_MAX_CHARS = 90 whenever
the opening clause exceeds 90 chars -- measured 08/09 at ~157 chars / 2,349 ms
against ~1.28 s predicted for a 90-char unit.

This patch cuts an oversized piece at the last word boundary at or before the
cap, but ONLY while the first unit is still being built. The `cap < max` test is
what scopes it: on every later enqueue firstMax === UNIT_MAX_CHARS === max, so
the branch cannot fire and behaviour is unchanged. A piece with no space inside
the cap falls through to the existing emit-whole path rather than cutting
mid-word.

Operates on BYTE lines and preserves the file's line terminator.
Dry-run by default. Pass --apply to write. Backs up to .bak_<timestamp>.
"""

import argparse
import hashlib
import os
import sys
import time

MARKER = "openjarvis-patch-ttsplayer-firstunit-v1"
SENTINEL = "First unit only: bound time-to-first-audio"

REL_PATH = os.path.join("src", "audio", "ttsPlayer.ts")

# 1-based line numbers -> expected content, compared after .strip()
ANCHORS = [
    (177, "if (piece.length > cap) {"),
    (178, "flush();"),
    (179, "units.push(piece);"),
    (180, "cap = max;"),
    (181, "continue;"),
    (182, "}"),
]

FIRST_LINE = ANCHORS[0][0]
LAST_LINE = ANCHORS[-1][0]

REPLACEMENT = [
    "    if (piece.length > cap) {",
    "      flush();",
    "      /*",
    "       * First unit only: bound time-to-first-audio by cutting an oversized",
    "       * piece at a word boundary instead of emitting it whole. `cap < max`",
    "       * is true only while the first unit is still being built -- on every",
    "       * later enqueue firstMax === max, so this branch cannot fire.",
    "       */",
    "      if (cap < max) {",
    "        const head = piece.slice(0, cap);",
    "        const cut = head.lastIndexOf(' ');",
    "        if (cut > 0) {",
    "          units.push(piece.slice(0, cut).trim());",
    "          cap = max;",
    "          current = piece.slice(cut + 1);",
    "          continue;",
    "        }",
    "      }",
    "      units.push(piece);",
    "      cap = max;",
    "      continue;",
    "    }",
]


def self_check():
    """Verify the payload survived delivery before it touches the real file."""
    problems = []
    text = "\n".join(REPLACEMENT)
    if SENTINEL not in text:
        problems.append("sentinel comment missing")
    if text.count("{") != text.count("}"):
        problems.append(
            "brace imbalance: %d open, %d close" % (text.count("{"), text.count("}"))
        )
    if text.count("(") != text.count(")"):
        problems.append(
            "paren imbalance: %d open, %d close" % (text.count("("), text.count(")"))
        )
    if text.count("continue;") != 2:
        problems.append("expected 2 continue statements, found %d" % text.count("continue;"))
    if text.count("units.push") != 2:
        problems.append("expected 2 units.push calls, found %d" % text.count("units.push"))
    if "lastIndexOf(' ')" not in text:
        problems.append("word-boundary search lost its quoted space")
    if "cap < max" not in text:
        problems.append("first-unit scope guard missing")
    if problems:
        print("PAYLOAD SELF-CHECK FAILED:")
        for p in problems:
            print("  - " + p)
        return False
    print("payload self-check OK (%d lines)" % len(REPLACEMENT))
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
        print("Run from the frontend dir, or pass --path.")
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
        print("ALREADY PATCHED -- sentinel found in the file. Refusing.")
        print("Restore the .bak first if you want to re-apply.")
        return 3

    ok = True
    for lineno, expected in ANCHORS:
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
        print("ABORTED -- anchors did not match, nothing written.")
        return 4

    out = (
        lines[: FIRST_LINE - 1]
        + [s.encode("ascii") for s in REPLACEMENT]
        + lines[LAST_LINE:]
    )
    new_raw = term.join(out) + trailing

    print("")
    print("--- predicted result ---")
    print("lines:  %d -> %d" % (len(lines), len(out)))
    print("bytes:  %d -> %d" % (len(raw), len(new_raw)))
    print("sha256: %s" % sha256(new_raw))
    print("")
    print("--- new lines %d-%d ---" % (FIRST_LINE - 1, FIRST_LINE + len(REPLACEMENT) + 1))
    for i in range(FIRST_LINE - 2, FIRST_LINE + len(REPLACEMENT) + 1):
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
    return 0


if __name__ == "__main__":
    sys.exit(main())