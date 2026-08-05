#!/usr/bin/env python3
# MARKER: openjarvis-patch-chatarea-tts-v1
"""
Rewire ChatArea.tsx TTS onto the new ttsPlayer module.

Three edits, all contiguous line ranges, applied by INDEX not by content match,
because this file carries mojibake elsewhere and must never be decoded and
re-encoded as a whole. Everything is done on byte lines; the existing line
terminator is detected and preserved.

  line 10       drop the now-unused synthesizeSpeechChunks import, add ttsPlayer
  lines 37-43   seven playback refs collapse to the three the driver still needs
  lines 71-198  toggleMute repointed at stopAll(); playNextChunk and BOTH
                competing effects replaced by one TTS driver effect

Dry run by default. Pass --apply to write. Backs up to .bak_<timestamp>,
predicts the post-patch SHA256 during the dry run, and re-hashes on disk after
writing so the two can be compared.

Read-only except under --apply.
"""

import argparse
import hashlib
import os
import shutil
import sys
import time

REL_PATH = os.path.join("frontend", "src", "components", "Chat", "ChatArea.tsx")

# ---------------------------------------------------------------------------
# Anchors. Compared after .strip() so indentation and terminator cannot break
# the match. Every one of these must hold or nothing is written.
# ---------------------------------------------------------------------------

ANCHORS = [
    (10, b"import { synthesizeSpeechChunks, fetchSavings } from '../../lib/api';"),
    (37, b"const audioRef = useRef<HTMLAudioElement | null>(null);"),
    (43, b"const spokenCharsRef = useRef<number>(0);"),
    (71, b"const toggleMute = useCallback(() => {"),
    (198, b"}, [streamState.isStreaming, messages, muted, playNextChunk]);"),
]

# ---------------------------------------------------------------------------
# Replacement text
# ---------------------------------------------------------------------------

IMPORT_BLOCK = r"""import { fetchSavings } from '../../lib/api';
import { enqueue, stopAll } from '../../audio/ttsPlayer';"""

REFS_BLOCK = r"""  const lastSpokenIdRef = useRef<string | null>(null);
  const hasMountedRef = useRef(false);
  const spokenCharsRef = useRef<number>(0);"""

DRIVER_BLOCK = r"""  const toggleMute = useCallback(() => {
    setMuted((prev) => {
      const next = !prev;
      try { localStorage.setItem(MUTE_KEY, String(next)); } catch {}
      if (next) stopAll();
      return next;
    });
  }, []);

  // -------------------------------------------------------------------------
  // TTS driver. ONE owner for the whole reply.
  //
  // The previous code had two effects competing over shared refs. The
  // mid-stream effect claimed lastSpokenIdRef as soon as it spoke its first
  // sentence; the post-stream effect then returned early because that id was
  // already claimed. Whatever was still unspoken when streaming ended fell
  // between them. All playback state now lives in ttsPlayer, so this effect
  // decides only WHAT text to hand over and WHEN.
  //
  // While streaming, hand over text up to the last completed sentence. Once
  // streaming ends, hand over everything remaining regardless of punctuation.
  // That final flush is what guarantees the last sentence is spoken, and it
  // works whether the store lands the final text and resetStream() in one
  // render or in two.
  // -------------------------------------------------------------------------
  useEffect(() => {
    const lastMsg = messages[messages.length - 1];

    // On mount, adopt whatever is already on screen as already spoken, so a
    // restored conversation is never read aloud. This is what hasMountedRef
    // was always for: it was declared and read but never assigned anywhere,
    // so the guard below it never opened and mid-stream TTS never ran once.
    if (!hasMountedRef.current) {
      hasMountedRef.current = true;
      if (lastMsg && lastMsg.role === 'assistant' && lastMsg.id) {
        lastSpokenIdRef.current = lastMsg.id;
        spokenCharsRef.current = (lastMsg.content || '').length;
      }
      return;
    }

    if (!lastMsg || lastMsg.role !== 'assistant' || !lastMsg.id) return;

    // A new reply cancels anything still queued from the previous one.
    if (lastMsg.id !== lastSpokenIdRef.current) {
      lastSpokenIdRef.current = lastMsg.id;
      spokenCharsRef.current = 0;
      stopAll();
    }

    const fullText = lastMsg.content || '';
    let take = fullText.length;

    if (streamState.isStreaming) {
      const unspoken = fullText.slice(spokenCharsRef.current);
      const match = unspoken.match(/^[\s\S]*[.!?](?=\s)/);
      if (!match) return;
      take = spokenCharsRef.current + match[0].length;
    }

    if (take <= spokenCharsRef.current) return;

    const segment = fullText.slice(spokenCharsRef.current, take);
    spokenCharsRef.current = take;

    // Consumed even while muted, so unmuting mid-reply does not replay text
    // that already went past on screen.
    if (muted) return;

    const plainText = segment
      .replace(/```[\s\S]*?```/g, 'code block.')
      .replace(/`[^`]+`/g, '')
      .replace(/[#*_~>]/g, '')
      .replace(/\[([^\]]+)\]\([^)]+\)/g, '$1')
      .trim();

    if (plainText) enqueue(plainText);
  }, [streamState.isStreaming, streamState.content, messages, muted]);"""

# ---------------------------------------------------------------------------
# Self-check. On 08/01 a delivered artifact arrived with backticks stripped,
# which silently turned a markdown-strip regex into a different regex. Refuse to
# run if this script's own payload lost them in transit.
# ---------------------------------------------------------------------------

REQUIRED_SUBSTRINGS = [
    "/```[\\s\\S]*?```/g",
    "/`[^`]+`/g",
    "from '../../audio/ttsPlayer'",
    "hasMountedRef.current = true;",
    "if (plainText) enqueue(plainText);",
]


def self_check():
    missing = [s for s in REQUIRED_SUBSTRINGS if s not in DRIVER_BLOCK + IMPORT_BLOCK]
    if missing:
        print("REFUSING TO RUN - this script's payload is corrupt.")
        for s in missing:
            print("  missing: " + repr(s))
        return False
    # Six in the fenced-code regex, three in the inline-code regex.
    if DRIVER_BLOCK.count("`") != 9:
        print("REFUSING TO RUN - expected 9 backticks in the driver block, found %d"
              % DRIVER_BLOCK.count("`"))
        return False
    return True


def detect_terminator(data):
    if b"\r\n" in data:
        return b"\r\n"
    return b"\n"


def sha256_hex(data):
    return hashlib.sha256(data).hexdigest().upper()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true", help="write the change")
    ap.add_argument("--path", default=".", help="repo root (default: cwd)")
    args = ap.parse_args()

    if not self_check():
        return 2

    target = os.path.abspath(os.path.join(args.path, REL_PATH))
    if not os.path.isfile(target):
        print("NOT FOUND: " + target)
        return 2

    with open(target, "rb") as fh:
        original = fh.read()

    term = detect_terminator(original)
    lines = original.split(term)

    print("file        : " + target)
    print("bytes       : %d" % len(original))
    print("sha256      : " + sha256_hex(original))
    print("terminator  : " + repr(term))
    print("lines       : %d" % len(lines))
    print("")

    if len(lines) < 200:
        print("REFUSING - file has %d lines, expected at least 200" % len(lines))
        return 2

    ok = True
    for lineno, expected in ANCHORS:
        actual = lines[lineno - 1].strip()
        hit = actual == expected.strip()
        print("anchor %4d : %s" % (lineno, "OK" if hit else "MISMATCH"))
        if not hit:
            print("    expected: " + repr(expected))
            print("    actual  : " + repr(actual))
            ok = False
    if not ok:
        print("")
        print("REFUSING - anchors do not match. The file has changed since it was read.")
        return 2

    def as_lines(block):
        return [s.encode("ascii") for s in block.split("\n")]

    patched = (
        lines[0:9]
        + as_lines(IMPORT_BLOCK)
        + lines[10:36]
        + as_lines(REFS_BLOCK)
        + lines[43:70]
        + as_lines(DRIVER_BLOCK)
        + lines[198:]
    )
    new_data = term.join(patched)

    print("")
    print("--- prediction ---")
    print("lines       : %d -> %d" % (len(lines), len(patched)))
    print("bytes       : %d -> %d" % (len(original), len(new_data)))
    print("sha256      : " + sha256_hex(new_data))

    removed = [b"playNextChunk", b"chunkQueueRef", b"isPlayingRef",
               b"ttsInFlightRef", b"audioRef", b"synthesizeSpeechChunks"]
    print("")
    print("--- symbols after patch (all should be 0) ---")
    for sym in removed:
        print("  %-24s %d" % (sym.decode(), new_data.count(sym)))

    if not args.apply:
        print("")
        print("DRY RUN - nothing written. Re-run with --apply.")
        return 0

    stamp = time.strftime("%Y%m%d_%H%M%S")
    backup = target + ".bak_" + stamp
    shutil.copy2(target, backup)
    with open(target, "wb") as fh:
        fh.write(new_data)

    with open(target, "rb") as fh:
        verify = fh.read()

    print("")
    print("--- applied ---")
    print("backup      : " + backup)
    print("bytes       : %d" % len(verify))
    print("sha256      : " + sha256_hex(verify))
    print("matches prediction: " + str(sha256_hex(verify) == sha256_hex(new_data)))
    print("")
    print("NEXT: cd frontend  &&  npm run build:tauri")
    return 0


if __name__ == "__main__":
    sys.exit(main())
