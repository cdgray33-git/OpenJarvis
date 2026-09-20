# MARKER: openjarvis-fix-synthesize-endpoint-v1
"""Line-anchored patch: use Kokoro's /synthesize instead of /synthesize-stream.

PROBLEM (validated 2026-08-03, not theorised)
    Kokoro's /synthesize-stream returns MULTIPLE COMPLETE WAV FILES
    CONCATENATED. Measured on a 304-character input:

        file bytes  : 1,013,848
        RIFF magics : 2  (offsets 0 and 532,524)
        RIFF field  :   532,516   should be 1,013,840
        data field  :   532,480   should be 1,013,804

    The first header describes only the first segment, so any standards-
    compliant consumer plays ~11s of ~21s and stops. That is exactly why
    the last sentence of every reply was never spoken -- 532,480 of
    1,013,804 bytes is 52.5%, and the chunk carried two sentences.

    speech_router.py is NOT at fault: _pump() is a pure byte passthrough.
    It faithfully relays a malformed stream.

    The same input to Kokoro's non-streaming /synthesize returns:

        file bytes  : 1,038,380
        RIFF magics : 1
        RIFF field  : 1,038,372   correct
        data field  : 1,038,336   correct

    One valid WAV.

SECOND, SEPARATE FINDING
    Non-stream audio data 1,038,336 bytes vs streamed 532,480 + 481,280
    = 1,013,760. Delta 24,576 bytes = 12,288 samples = EXACTLY 0.512s at
    24kHz 16-bit mono. The streaming endpoint returns half a second LESS
    audio for identical input. That is a suspiciously round number --
    a fixed buffer or frame dropped at stream start, not a synthesis
    difference. It is the leading candidate for the missing first word,
    and this patch may fix that too. UNPROVEN -- verify by listening.

WHY THIS COSTS NOTHING
    The frontend's synthesizeSpeech ends in res.blob(), which awaits the
    COMPLETE response. The streaming endpoint's only benefit is already
    discarded client-side. OpenJarvis has been paying the concatenated-WAV
    defect for a property it does not consume.

    Real streaming later needs BOTH a Kokoro wrapper that emits a frame-
    based format or one correct WAV stream, AND a frontend that consumes
    the stream instead of calling res.blob(). Neither alone helps.

WHAT IT CHANGES
    Exactly one line -- 87 -- inside speech_router.py's synthesize handler:
        KOKORO_SERVER + "/synthesize-stream",   ->   KOKORO_SERVER + "/synthesize",

    Nothing else. The request body at 88-92 is already {text, voice, speed},
    which /synthesize accepts (validated by direct POST). media_type at 119
    stays "audio/wav" because the format has not changed. The httpx timeout
    of 60s at line 83 comfortably covers a ~12s synthesis.

USAGE
    python fix_synthesize_endpoint.py                 # dry run, default
    python fix_synthesize_endpoint.py --apply
    python fix_synthesize_endpoint.py --path C:\\Users\\Admin\\Openjarvis

Stdlib only. Read-only unless --apply is passed. Backend restart required.
"""

import argparse
import hashlib
import os
import shutil
import sys
import time

MARKER = "openjarvis-fix-synthesize-endpoint-v1"
REL_TARGET = os.path.join("src", "openjarvis", "server", "speech_router.py")

TARGET_LINE = 87
EXPECT = '                    KOKORO_SERVER + "/synthesize-stream",'
REPLACE = '                    KOKORO_SERVER + "/synthesize",'


def sha256_of(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for block in iter(lambda: fh.read(65536), b""):
            h.update(block)
    return h.hexdigest().upper()


def split_keepends(raw):
    text = raw.decode("utf-8")
    bodies, ends = [], []
    for p in text.splitlines(True):
        if p.endswith("\r\n"):
            bodies.append(p[:-2]); ends.append("\r\n")
        elif p.endswith("\n"):
            bodies.append(p[:-1]); ends.append("\n")
        elif p.endswith("\r"):
            bodies.append(p[:-1]); ends.append("\r")
        else:
            bodies.append(p); ends.append("")
    return bodies, ends


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--path", default=".", help="repo root (default: cwd)")
    ap.add_argument("--apply", action="store_true", help="write changes")
    args = ap.parse_args()

    target = os.path.join(os.path.abspath(args.path), REL_TARGET)
    print("marker : %s" % MARKER)
    print("target : %s" % target)

    if not os.path.isfile(target):
        print("ERROR  : file not found")
        return 2

    raw = open(target, "rb").read()
    text = raw.decode("utf-8")
    print("before : %d bytes / SHA256 %s" % (len(raw), sha256_of(target)))

    if '"/synthesize-stream"' not in text:
        print("")
        print("NO-OP  : '/synthesize-stream' not present. Already patched,")
        print("         or this file has drifted. Nothing written.")
        return 0

    bodies, ends = split_keepends(raw)
    idx = TARGET_LINE - 1
    print("")
    print("anchor check:")
    if idx >= len(bodies) or bodies[idx] != EXPECT:
        actual = bodies[idx] if idx < len(bodies) else "<out of range>"
        print("  FAIL line %d MISMATCH" % TARGET_LINE)
        print("       expected: %r" % EXPECT)
        print("       actual  : %r" % actual)
        print("")
        print("ABORT  : file has drifted. NOT touched.")
        return 3
    print("  ok   line %d matched byte-exact" % TARGET_LINE)

    # only one occurrence should exist, guard against silent multi-edit
    occurrences = sum(1 for b in bodies if '"/synthesize-stream"' in b)
    if occurrences != 1:
        print("")
        print("ABORT  : expected 1 occurrence of '/synthesize-stream', found %d."
              % occurrences)
        print("         Review manually. NOT touched.")
        return 3

    bodies[idx] = REPLACE
    new_text = "".join(b + e for b, e in zip(bodies, ends))
    new_raw = new_text.encode("utf-8")

    try:
        compile(new_text, target, "exec")
        print("compile: OK (patched source parses)")
    except SyntaxError as exc:
        print("ABORT  : patched source does NOT compile: %s" % exc)
        return 4

    predicted = hashlib.sha256(new_raw).hexdigest().upper()
    print("")
    print("  line %d before: %s" % (TARGET_LINE, EXPECT.strip()))
    print("  line %d after : %s" % (TARGET_LINE, REPLACE.strip()))
    print("")
    print("after  : %d bytes / SHA256 %s (predicted)" % (len(new_raw), predicted))
    print("delta  : %+d bytes / %+d lines" % (len(new_raw) - len(raw), 0))

    if not args.apply:
        print("")
        print("DRY RUN. No changes written. Re-run with --apply to write.")
        return 0

    stamp = time.strftime("%Y%m%d_%H%M%S")
    backup = "%s.bak_%s" % (target, stamp)
    shutil.copy2(target, backup)
    print("")
    print("backup : %s" % backup)

    with open(target, "wb") as fh:
        fh.write(new_raw)

    actual_hash = sha256_of(target)
    print("written: %d bytes / SHA256 %s" % (os.path.getsize(target), actual_hash))
    if actual_hash == predicted:
        print("VERIFY : on-disk hash matches prediction. PATCH APPLIED.")
    else:
        print("VERIFY : MISMATCH. Restore with:")
        print('         Copy-Item "%s" "%s" -Force' % (backup, target))
        return 5

    print("")
    print("NEXT   : restart the backend, then send a multi-sentence prompt.")
    print("         Expect: last sentence spoken, and possibly the first")
    print("         word restored. Console ERR_FILE_NOT_FOUND may persist --")
    print("         that is a separate, cosmetic revoke-timing issue.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
