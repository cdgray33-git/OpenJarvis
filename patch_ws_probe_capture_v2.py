#!/usr/bin/env python3
"""
patch_ws_probe_capture_v2.py

Second patch to ws_probe.py. Requires v1 (--stream) already applied.

WHY
  The 09:12 streaming run returned 19,407 bytes of prose and zero tool
  calls, on the same prompt that produced two confirm cycles on the
  non-streaming path. The probe discarded the text, so the run cannot
  distinguish "the model answered in prose" from "the streaming chain did
  not offer tools" from "the model claimed to have run the tool without
  invoking it" - which is Defect 1. All three look identical in a report
  that only counts chunk kinds.

WHAT
  1. Capture assembled response text; write it to ws_probe_last_response.txt
     and preview it in the report.
  2. Add an explicit TOOL ACTIVITY section - which tool-related WS frames
     were seen, stated as a presence/absence finding rather than left to be
     inferred from a frame list.
  3. Add --prompt so the gate can be provoked deliberately.

Run from the repo root: PS C:\\Users\\Admin\\OpenJarvis>

Guards: marker check, exactly-once verbatim matching, EOL detection,
temp-file compile before touching the real file, timestamped .bak,
post-write compile and --help smoke run, both self-restoring.

Exit codes: 0 applied or already applied, 1 guard failure, 2 environment.
"""

import os
import py_compile
import shutil
import subprocess
import sys
import tempfile
import time

MARKER = "openjarvis-ws-probe-capture-v2"
PREREQ_MARKER = "openjarvis-ws-probe-stream-v1"
TARGET = "ws_probe.py"


# ---------------------------------------------------------------------------
# the edits
# ---------------------------------------------------------------------------

OLD_GLOBALS = '''SSE = []                  # openjarvis-ws-probe-stream-v1: per-chunk arrivals
STREAM = False            # openjarvis-ws-probe-stream-v1: --stream picks 1b
STOP = threading.Event()
'''

NEW_GLOBALS = '''SSE = []                  # openjarvis-ws-probe-stream-v1: per-chunk arrivals
STREAM = False            # openjarvis-ws-probe-stream-v1: --stream picks 1b
TEXT = []                 # openjarvis-ws-probe-capture-v2: response fragments
PROMPT_OVERRIDE = None    # openjarvis-ws-probe-capture-v2: --prompt
RESPONSE_FILE = "ws_probe_last_response.txt"
STOP = threading.Event()
'''

OLD_CONTENT_BRANCH = '''                    elif delta.get("content"):
                        record["kind"] = "content"
'''

NEW_CONTENT_BRANCH = '''                    elif delta.get("content"):
                        record["kind"] = "content"
                        TEXT.append(delta["content"])
'''

OLD_PROMPT_USE = '''        "messages": [{"role": "user", "content": CHAT_PROMPT}],
'''

NEW_PROMPT_USE = '''        "messages": [{"role": "user",
                      "content": PROMPT_OVERRIDE or CHAT_PROMPT}],
'''

OLD_NONSTREAM_PARSE = '''                    parsed = json.loads(raw)
                    choices = parsed.get("choices") or []
                    if choices:
                        CHAT["finish_reason"] = choices[0].get("finish_reason")
                    CHAT["bytes"] = len(raw)
'''

NEW_NONSTREAM_PARSE = '''                    parsed = json.loads(raw)
                    choices = parsed.get("choices") or []
                    if choices:
                        CHAT["finish_reason"] = choices[0].get("finish_reason")
                        msg = choices[0].get("message") or {}
                        if msg.get("content"):
                            TEXT.append(msg["content"])
                    CHAT["bytes"] = len(raw)
'''

OLD_REPORT_ANCHOR = '''    # ---- heartbeat
    print()
    print("HTTP HEARTBEAT  (%d samples)" % len(HEARTBEATS))
'''

NEW_REPORT_ANCHOR = '''    # ---- tool activity: presence/absence stated, not inferred
    print()
    print("TOOL ACTIVITY")
    seen = {}
    for f in FRAMES:
        if f["type"]:
            seen[f["type"]] = seen.get(f["type"], 0) + 1
    tool_types = [t for t in seen if "tool" in str(t)]
    if tool_types:
        for t in sorted(tool_types):
            print("  %-28s x%d" % (t, seen[t]))
    else:
        print("  NO tool-related frame of any kind was emitted this run.")
        print("  No confirm request, no tool_call_start. The gate was never")
        print("  entered, so this run says NOTHING about gate delivery on")
        print("  this path. Distinguish before drawing a conclusion:")
        print("    - model answered in prose            -> read the text below")
        print("    - model claimed the tool ran         -> Defect 1, escalate")
        print("    - chain never offered tools          -> read the call chain")

    # ---- response text: the evidence the report used to throw away
    print()
    body = "".join(TEXT)
    print("RESPONSE TEXT  (%d chars)" % len(body))
    if not body:
        print("  none captured")
    else:
        try:
            with open(RESPONSE_FILE, "w", encoding="utf-8") as _fh:
                _fh.write(body)
            print("  full text written to %s" % RESPONSE_FILE)
        except Exception as _exc:
            print("  could not write %s: %s" % (RESPONSE_FILE, _exc))
        preview = body[:600].replace("\\r", "")
        print("  ---- first 600 chars ----")
        for _ln in preview.split("\\n"):
            print("  %s" % _ln)
        if len(body) > 600:
            print("  ---- truncated, %d chars remain ----" % (len(body) - 600))

    # ---- heartbeat
    print()
    print("HTTP HEARTBEAT  (%d samples)" % len(HEARTBEATS))
'''

OLD_ARGS = '''    ap.add_argument("--stream", action="store_true",
                    help="exercise PATH 1b, the browser streaming path, and "
                         "record SSE chunk arrival times")
    args = ap.parse_args()

    global STREAM
    STREAM = bool(args.stream)
'''

NEW_ARGS = '''    ap.add_argument("--stream", action="store_true",
                    help="exercise PATH 1b, the browser streaming path, and "
                         "record SSE chunk arrival times")
    ap.add_argument("--prompt", default=None,
                    help="override the built-in prompt, to provoke the gate "
                         "deliberately rather than hope for it")
    args = ap.parse_args()

    global STREAM, PROMPT_OVERRIDE
    STREAM = bool(args.stream)
    PROMPT_OVERRIDE = args.prompt
'''

REPLACEMENTS = [
    ("module globals", OLD_GLOBALS, NEW_GLOBALS),
    ("sse content capture", OLD_CONTENT_BRANCH, NEW_CONTENT_BRANCH),
    ("prompt override in body", OLD_PROMPT_USE, NEW_PROMPT_USE),
    ("non-stream text capture", OLD_NONSTREAM_PARSE, NEW_NONSTREAM_PARSE),
    ("report tool activity + text", OLD_REPORT_ANCHOR, NEW_REPORT_ANCHOR),
    ("argparse --prompt", OLD_ARGS, NEW_ARGS),
]


# ---------------------------------------------------------------------------

def fail(msg):
    print("ABORT: %s" % msg)
    print("The target file was NOT modified.")
    sys.exit(1)


def main():
    if not os.path.isfile(TARGET):
        print("ABORT: %s not found. Run this from the repo root:" % TARGET)
        print("  PS C:\\Users\\Admin\\OpenJarvis>")
        sys.exit(2)

    with open(TARGET, "r", encoding="utf-8", newline="") as fh:
        original = fh.read()

    if MARKER in original:
        print("Already applied - marker %s present. Nothing to do." % MARKER)
        sys.exit(0)

    if PREREQ_MARKER not in original:
        print("ABORT: prerequisite patch %s is not present." % PREREQ_MARKER)
        print("Apply patch_ws_probe_stream_v1.py first.")
        sys.exit(1)

    crlf = original.count("\r\n")
    lf_only = original.count("\n") - crlf
    if crlf and lf_only:
        print("NOTE: mixed line endings (%d CRLF, %d LF). Matching CRLF."
              % (crlf, lf_only))
    use_crlf = crlf > lf_only
    print("line endings: %s" % ("CRLF" if use_crlf else "LF"))

    def conv(text):
        return text.replace("\n", "\r\n") if use_crlf else text

    problems = []
    for name, old, _new in REPLACEMENTS:
        n = original.count(conv(old))
        if n != 1:
            problems.append("  %-32s matched %d times (need exactly 1)"
                            % (name, n))
    if problems:
        print("Verbatim match check FAILED:")
        for p in problems:
            print(p)
        fail("ws_probe.py is not the version this patch was written against")

    patched = original
    for name, old, new in REPLACEMENTS:
        patched = patched.replace(conv(old), conv(new), 1)
    print("all %d replacements matched exactly once" % len(REPLACEMENTS))

    tmpdir = tempfile.mkdtemp(prefix="ws_probe_patch_")
    tmp = os.path.join(tmpdir, "ws_probe_candidate.py")
    with open(tmp, "w", encoding="utf-8", newline="") as fh:
        fh.write(patched)
    try:
        py_compile.compile(tmp, doraise=True)
        print("temp-file compile OK - real file still untouched")
    except py_compile.PyCompileError as exc:
        print(exc)
        fail("patched content does not compile")
    finally:
        shutil.rmtree(tmpdir, ignore_errors=True)

    stamp = time.strftime("%Y%m%d-%H%M%S")
    bak = "%s.bak-%s" % (TARGET, stamp)
    shutil.copy2(TARGET, bak)
    print("backup written: %s" % bak)

    with open(TARGET, "w", encoding="utf-8", newline="") as fh:
        fh.write(patched)
    print("applied to %s" % TARGET)

    def restore(why):
        shutil.copy2(bak, TARGET)
        print("RESTORED %s from %s" % (TARGET, bak))
        fail(why)

    try:
        py_compile.compile(TARGET, doraise=True)
        print("post-write compile OK")
    except py_compile.PyCompileError as exc:
        print(exc)
        restore("post-write compile failed")

    try:
        proc = subprocess.run([sys.executable, TARGET, "--help"],
                              capture_output=True, text=True, timeout=60)
    except Exception as exc:
        restore("--help smoke run raised %s" % type(exc).__name__)
        return
    if proc.returncode != 0:
        print(proc.stdout)
        print(proc.stderr)
        restore("--help smoke run exited %d" % proc.returncode)
    if "--prompt" not in proc.stdout:
        print(proc.stdout)
        restore("--prompt did not appear in --help output")
    print("--help smoke run OK, --prompt present")

    print()
    print("DONE. Rollback if needed:")
    print("  Copy-Item '%s' '%s' -Force" % (bak, TARGET))


if __name__ == "__main__":
    main()
