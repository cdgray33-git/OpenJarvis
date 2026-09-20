#!/usr/bin/env python3
"""
patch_ws_probe_stream_v1.py

Adds --stream mode to ws_probe.py so the probe can exercise PATH 1b, the
browser streaming path, and corrects verdict prose that still asserts the
dead "PowerShell instrument artifact" theory.

Run from the repo root: PS C:\\Users\\Admin\\OpenJarvis>

Guards, in order:
  1. target exists
  2. marker check - idempotent, safe to re-run
  3. line-ending detection, so verbatim matching works on CRLF or LF
  4. every replacement must match EXACTLY ONCE or the script aborts untouched
  5. compile check in a TEMP file BEFORE the real file is touched
  6. timestamped .bak
  7. post-write compile, self-restoring on failure
  8. post-write "--help" smoke run, self-restoring on failure

Exit codes: 0 applied or already applied, 1 guard failure (file untouched
or restored), 2 usage/environment problem.
"""

import os
import py_compile
import shutil
import subprocess
import sys
import tempfile
import time

MARKER = "openjarvis-ws-probe-stream-v1"
TARGET = "ws_probe.py"


# ---------------------------------------------------------------------------
# the edits
# ---------------------------------------------------------------------------

OLD_PURPOSE = '''PURPOSE
  Split the two candidate causes of the ~247 s WS frame delivery stall:
    (A) server-side: the asyncio event loop is blocked while the confirm gate
        holds a worker, so queued frames are only flushed on release.
    (B) client-side: the PowerShell receive loop is the artifact and the
        server is fine.
'''

NEW_PURPOSE = '''PURPOSE
  Measure whether OpenJarvis delivers event frames promptly during a turn,
  on a NAMED execution path, using three independent channels: WS frames,
  an HTTP heartbeat, and (in --stream mode) SSE chunk arrival.

  HISTORY, recorded so no future reader re-derives a dead theory:
    The ~247 s "WS delivery stall" measured 2026-08-23 07:36 was neither a
    WS defect nor a client artifact. Two plain-def handlers were called
    without await from an async route (routes.py:162 and :165), running
    synchronous work on the event loop and taking the WHOLE SERVER down for
    the duration of a request. Fixed with asyncio.to_thread and confirmed
    clean by the 08:58 run of this probe. The confirm gate was eliminated as
    cause by timestamp order - loop death preceded the first confirm by
    1.2 s - not by argument.
'''

OLD_READING = '''READING THE VERDICT
  HTTP heartbeat stalls in step with the frames -> event loop blocked ->
    SERVER-SIDE. The 6e browser half is blocked until fixed.
  HTTP heartbeat stays responsive while frames queue -> loop is healthy ->
    the fault is in the WS send path or in the PowerShell client, and the
    earlier measurements were an instrument artifact.
'''

NEW_READING = '''READING THE VERDICT
  HTTP heartbeat stalls in step with the frames -> the event loop is blocked.
    Look for synchronous work called without await from a coroutine.
  HTTP heartbeat stays responsive while frames queue -> the loop is healthy,
    so the fault is in the WS send path, the per-client queue, or the
    bridge allowlist.
  Everything clean -> the path just exercised is sound, AND NOTHING MORE.
    Default mode and --stream are two different call chains. A clean result
    on one says nothing about the other. Each needs its own run.
'''

OLD_GLOBALS = '''CLOSE_EVENT = {}          # how and when the socket died, if it did
CHAT = {}                 # sent, returned, status, finish_reason, error
STOP = threading.Event()
'''

NEW_GLOBALS = '''CLOSE_EVENT = {}          # how and when the socket died, if it did
CHAT = {}                 # sent, returned, status, finish_reason, error
SSE = []                  # openjarvis-ws-probe-stream-v1: per-chunk arrivals
STREAM = False            # openjarvis-ws-probe-stream-v1: --stream picks 1b
STOP = threading.Event()
'''

OLD_CHAT_SEND = '''def chat_send(base, model, timeout):
    """POST a chat completion that provokes a confirmation-gated tool call."""
    url = base + "/v1/chat/completions"
    body = {
        "model": model,
        "messages": [{"role": "user", "content": CHAT_PROMPT}],
        "stream": False,
    }
    data = json.dumps(body).encode("utf-8")
    req = urllib.request.Request(
        url, data=data, method="POST",
        headers={"Content-Type": "application/json"},
    )
    CHAT["sent"] = time.time()
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read().decode("utf-8", errors="replace")
            CHAT["status"] = resp.status
            CHAT["returned"] = time.time()
            try:
                parsed = json.loads(raw)
                choices = parsed.get("choices") or []
                if choices:
                    CHAT["finish_reason"] = choices[0].get("finish_reason")
                CHAT["bytes"] = len(raw)
            except Exception:
                CHAT["bytes"] = len(raw)
    except Exception as exc:
        CHAT["returned"] = time.time()
        CHAT["error"] = "%s: %s" % (type(exc).__name__, exc)
'''

NEW_CHAT_SEND = '''def _read_sse(resp):
    """Consume an SSE body line by line, timestamping every chunk.

    readline returns as soon as the transport delivers, so what is recorded
    is arrival time, not parse time. This is the third measurement channel:
    the WS frames say what the bus emitted, the heartbeat says whether the
    server was alive, and these say whether the streaming RESPONSE itself
    kept flowing.
    """
    total = 0
    while True:
        line = resp.readline()
        if not line:
            break
        recv = time.time()
        total += len(line)
        text = line.decode("utf-8", errors="replace").rstrip("\\r\\n")
        if not text:
            continue  # SSE event separator, not a chunk
        payload = text[5:].strip() if text.startswith("data:") else text
        record = {"recv": recv, "bytes": len(line), "kind": None, "done": False}
        if payload == "[DONE]":
            record["kind"] = "[DONE]"
            record["done"] = True
        else:
            try:
                obj = json.loads(payload)
                choices = obj.get("choices") or []
                if choices:
                    fin = choices[0].get("finish_reason")
                    delta = choices[0].get("delta") or {}
                    if fin:
                        CHAT["finish_reason"] = fin
                        record["kind"] = "finish:%s" % fin
                    elif delta.get("tool_calls"):
                        record["kind"] = "tool_calls"
                    elif delta.get("content"):
                        record["kind"] = "content"
                    else:
                        record["kind"] = "delta"
                else:
                    record["kind"] = obj.get("type") or "json"
            except Exception:
                record["kind"] = "raw"
        SSE.append(record)
        if record["done"]:
            break
    CHAT["returned"] = time.time()
    CHAT["bytes"] = total


def chat_send(base, model, timeout):
    """POST a chat completion that provokes a confirmation-gated tool call.

    Default: stream=false, PATH 1a. With --stream: stream=true, PATH 1b, the
    chain the browser actually uses, read incrementally.
    """
    url = base + "/v1/chat/completions"
    body = {
        "model": model,
        "messages": [{"role": "user", "content": CHAT_PROMPT}],
        "stream": bool(STREAM),
    }
    data = json.dumps(body).encode("utf-8")
    headers = {"Content-Type": "application/json"}
    if STREAM:
        headers["Accept"] = "text/event-stream"
    req = urllib.request.Request(url, data=data, method="POST", headers=headers)
    CHAT["sent"] = time.time()
    CHAT["mode"] = "stream" if STREAM else "non-stream"
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            CHAT["status"] = resp.status
            if STREAM:
                _read_sse(resp)
            else:
                raw = resp.read().decode("utf-8", errors="replace")
                CHAT["returned"] = time.time()
                try:
                    parsed = json.loads(raw)
                    choices = parsed.get("choices") or []
                    if choices:
                        CHAT["finish_reason"] = choices[0].get("finish_reason")
                    CHAT["bytes"] = len(raw)
                except Exception:
                    CHAT["bytes"] = len(raw)
    except Exception as exc:
        CHAT["returned"] = time.time()
        CHAT["error"] = "%s: %s" % (type(exc).__name__, exc)
'''

OLD_REPORT_ANCHOR = '''    # ---- heartbeat
    print()
    print("HTTP HEARTBEAT  (%d samples)" % len(HEARTBEATS))
'''

NEW_REPORT_ANCHOR = '''    # ---- sse chunks (stream mode)
    if STREAM or SSE:
        print()
        print("SSE STREAM  (%d chunks)" % len(SSE))
        if not SSE:
            print("  NONE. stream=true was requested and no chunk arrived.")
            print("  That is a finding, not a null result. Check that the")
            print("  streaming branch was actually taken.")
        else:
            first = SSE[0]["recv"]
            last = SSE[-1]["recv"]
            if CHAT.get("sent"):
                print("  time to first chunk  %.3f s" % (first - CHAT["sent"]))
            print("  first chunk t+%s   last chunk t+%s"
                  % (rel(first), rel(last)))
            gaps = [SSE[i]["recv"] - SSE[i - 1]["recv"]
                    for i in range(1, len(SSE))]
            if gaps:
                mx = max(gaps)
                ends_at = SSE[gaps.index(mx) + 1]["recv"]
                print("  chunk gap  min %.3f s   max %.3f s   mean %.3f s"
                      % (min(gaps), mx, sum(gaps) / len(gaps)))
                print("  largest gap ends t+%s" % rel(ends_at))
                print("  NOTE: a gap spanning a confirm wait is EXPECTED. Read")
                print("  it against the WS frame times, not on its own.")
            kinds = {}
            for s in SSE:
                kinds[str(s["kind"])] = kinds.get(str(s["kind"]), 0) + 1
            print("  chunk kinds: %s"
                  % ", ".join("%s x%d" % (k, kinds[k]) for k in sorted(kinds)))
            print("  total body bytes: %s" % CHAT.get("bytes"))

    # ---- heartbeat
    print()
    print("HTTP HEARTBEAT  (%d samples)" % len(HEARTBEATS))
'''

OLD_VERDICT_CLEAN = '''    elif not stalled_frames:
        print("  NO STALL REPRODUCED under a non-PowerShell client.")
        print("  Max frame lag %.3f s. The earlier ~247 s measurement is" % max_lag)
        print("  most likely a PowerShell instrument artifact. 6e is unblocked;")
        print("  proceed to the remaining emit branches with this probe.")
'''

NEW_VERDICT_CLEAN = '''    elif not stalled_frames:
        print("  NO STALL REPRODUCED on the %s path."
              % ("STREAMING 1b (browser)" if STREAM else "NON-STREAMING 1a"))
        print("  Max frame lag %.3f s, HTTP responsive throughout." % max_lag)
        print("  Frames arrived as emitted rather than in a release burst,")
        print("  so the event loop was free for the whole turn.")
        print("  SCOPE: this clears the path just exercised and no other.")
'''

OLD_VERDICT_SERVER = '''    elif stalled_frames and stalled_http:
        print("  SERVER-SIDE. Frames lagged %.1f s AND plain HTTP stalled" % max_lag)
        print("  alongside them. The asyncio event loop is blocked, which is")
        print("  consistent with the confirm gate holding it. The 6e browser")
        print("  half stays blocked. Next: find what runs the gate wait on the")
        print("  loop rather than a worker thread.")
'''

NEW_VERDICT_SERVER = '''    elif stalled_frames and stalled_http:
        print("  EVENT LOOP BLOCKED. Frames lagged %.1f s AND plain HTTP" % max_lag)
        print("  stalled alongside them, so the whole server was unavailable,")
        print("  not just this route. NOT the confirm gate - eliminated as")
        print("  cause 2026-08-23 by timestamp order. Look for a plain def")
        print("  called without await from a coroutine on this path.")
'''

OLD_ARGS = '''    ap.add_argument("--chat-timeout", type=float, default=280.0)
    args = ap.parse_args()
'''

NEW_ARGS = '''    ap.add_argument("--chat-timeout", type=float, default=280.0)
    ap.add_argument("--stream", action="store_true",
                    help="exercise PATH 1b, the browser streaming path, and "
                         "record SSE chunk arrival times")
    args = ap.parse_args()

    global STREAM
    STREAM = bool(args.stream)
'''

OLD_BANNER = '''    print("  deadline  %.0f s" % args.deadline)
    print("  confirm   NOT approved - the gate is allowed to time out")
'''

NEW_BANNER = '''    print("  deadline  %.0f s" % args.deadline)
    print("  path      %s"
          % ("1b STREAMING - the browser chain" if STREAM
             else "1a NON-STREAMING"))
    print("  confirm   NOT approved - the gate is allowed to time out")
'''

REPLACEMENTS = [
    ("docstring PURPOSE", OLD_PURPOSE, NEW_PURPOSE),
    ("docstring READING THE VERDICT", OLD_READING, NEW_READING),
    ("module globals", OLD_GLOBALS, NEW_GLOBALS),
    ("chat_send + _read_sse", OLD_CHAT_SEND, NEW_CHAT_SEND),
    ("report SSE section", OLD_REPORT_ANCHOR, NEW_REPORT_ANCHOR),
    ("verdict clean branch", OLD_VERDICT_CLEAN, NEW_VERDICT_CLEAN),
    ("verdict server branch", OLD_VERDICT_SERVER, NEW_VERDICT_SERVER),
    ("argparse --stream", OLD_ARGS, NEW_ARGS),
    ("banner path line", OLD_BANNER, NEW_BANNER),
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

    # guard 3: line endings. Verbatim matching fails silently on CRLF unless
    # the search text is translated to match the file.
    crlf = original.count("\r\n")
    lf_only = original.count("\n") - crlf
    if crlf and lf_only:
        print("NOTE: mixed line endings (%d CRLF, %d LF). Matching CRLF."
              % (crlf, lf_only))
    use_crlf = crlf > lf_only
    print("line endings: %s" % ("CRLF" if use_crlf else "LF"))

    def conv(text):
        return text.replace("\n", "\r\n") if use_crlf else text

    # guard 4: every replacement matches exactly once, checked BEFORE any
    # substitution, so a partial application is impossible.
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

    # guard 5: compile the RESULT in a temp file before touching the real one
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

    # guard 6: backup
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

    # guard 7: post-write compile
    try:
        py_compile.compile(TARGET, doraise=True)
        print("post-write compile OK")
    except py_compile.PyCompileError as exc:
        print(exc)
        restore("post-write compile failed")

    # guard 8: argparse smoke run. Exercises the new --stream wiring without
    # touching the server.
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
    if "--stream" not in proc.stdout:
        print(proc.stdout)
        restore("--stream did not appear in --help output")
    print("--help smoke run OK, --stream present")

    print()
    print("DONE. Rollback if needed:")
    print("  Copy-Item '%s' '%s' -Force" % (bak, TARGET))
    print()
    print("Next: run the streaming probe. Default mode is unchanged.")


if __name__ == "__main__":
    main()
