#!/usr/bin/env python3
"""
patch_ws_probe_agent_v3.py - ws_probe.py v2 -> v3.

Adds:
  1. --agent <id>. When set, the chat POST body carries "agent": "<id>".
     When unset, the body is UNCHANGED from v2, so no-agent runs stay
     byte-identical to the two already in the record.
  2. A banner that names the predicted path AND the request shape that
     selects it, in the same sentence, every time. The instrument carries
     the rule so the operator does not have to remember it.
  3. Early exit: stop once the turn has been over for --grace seconds
     (default 150 s, longer than the 120 s confirm TTL) and no
     tool_confirm_request is outstanding. An unresolved confirm suppresses
     the exit entirely, so it can never truncate a confirm cycle.

Guards, same pattern as v1 and v2:
  marker idempotency, prerequisite marker check, line-ending detection with
  search-text translation, exactly-once verbatim match verified across ALL
  replacements before any substitution, temp-file compile, timestamped .bak,
  post-write compile with self-restore, --help smoke run with self-restore
  asserting the new flags are present.

Run from PS C:\\Users\\Admin\\OpenJarvis>  as:  python .\\patch_ws_probe_agent_v3.py
Exit codes: 0 applied or already applied, 2 refused or failed (file restored).
"""

import os
import py_compile
import shutil
import subprocess
import sys
import tempfile
import time

TARGET = "ws_probe.py"
MARKER = "openjarvis-ws-probe-agent-v3"
PREREQ = "openjarvis-ws-probe-capture-v2"


# ---------------------------------------------------------------------------
# replacements - each old block must appear EXACTLY ONCE
# ---------------------------------------------------------------------------

R = []

# --- 1. globals -----------------------------------------------------------
R.append((
'''PROMPT_OVERRIDE = None    # openjarvis-ws-probe-capture-v2: --prompt
RESPONSE_FILE = "ws_probe_last_response.txt"
STOP = threading.Event()
''',
'''PROMPT_OVERRIDE = None    # openjarvis-ws-probe-capture-v2: --prompt
AGENT = None              # openjarvis-ws-probe-agent-v3: --agent, selects 1b
GRACE = 150.0             # openjarvis-ws-probe-agent-v3: post-turn grace, s
PATH_LABEL = {}           # openjarvis-ws-probe-agent-v3: predicted path text
TURN_END = {}             # openjarvis-ws-probe-agent-v3: when the POST returned
TURN_DONE = threading.Event()   # openjarvis-ws-probe-agent-v3
CONFIRM_OPEN = set()      # openjarvis-ws-probe-agent-v3: unresolved confirms
EXIT_REASON = {}          # openjarvis-ws-probe-agent-v3: grace or deadline
RESPONSE_FILE = "ws_probe_last_response.txt"
STOP = threading.Event()
'''))

# --- 2. helpers after rel() ----------------------------------------------
R.append((
'''def rel(t):
    """Seconds since probe start, for readable output."""
    if t is None or T0 is None:
        return None
    return round(t - T0, 3)
''',
'''def rel(t):
    """Seconds since probe start, for readable output."""
    if t is None or T0 is None:
        return None
    return round(t - T0, 3)


# openjarvis-ws-probe-agent-v3 ----------------------------------------------
# Path naming and early exit.
#
# PATH NAMING: never name a path without naming what in the request selected
# it. That rule was learned the expensive way - three windows of believing the
# browser was on 1b - so the instrument enforces it rather than the operator.
#
# EARLY EXIT: v2 held the socket until --deadline even after the turn ended;
# the 09:12 run sat idle 394 s after a 6 s turn. Exit only when the turn has
# been over for GRACE seconds AND no confirm is outstanding. GRACE defaults
# longer than the 120 s TTL, and an unresolved tool_confirm_request suppresses
# the exit outright, so an early exit cannot truncate a confirm cycle.

CONFIRM_REQUEST_TYPES = ("tool_confirm_request",)
CONFIRM_RESOLVED_TYPES = ("tool_confirm_resolved",)


def _confirm_key(data):
    """Best-effort id for a confirm frame. Unknown shape is not an error."""
    for field in ("confirm_id", "confirmation_id", "request_id", "id",
                  "call_id", "tool_call_id"):
        val = data.get(field)
        if val:
            return str(val)
    return "<unkeyed>"


def _track_confirm(etype, data):
    if etype in CONFIRM_REQUEST_TYPES:
        CONFIRM_OPEN.add(_confirm_key(data))
    elif etype in CONFIRM_RESOLVED_TYPES:
        key = _confirm_key(data)
        CONFIRM_OPEN.discard(key)
        if key == "<unkeyed>":
            # A resolved frame we cannot key against a request clears the
            # set. Erring toward exit is safe here only because the turn
            # must ALSO have ended and GRACE elapsed before exit happens.
            CONFIRM_OPEN.clear()


def _grace_expired():
    """True when it is safe to stop listening before --deadline."""
    if CONFIRM_OPEN:
        return False
    if not TURN_DONE.is_set():
        return False
    ended = TURN_END.get("at")
    if ended is None:
        return False
    return (time.time() - ended) >= GRACE


def _set_path_label():
    """Name the path and the request shape that selects it, together."""
    if AGENT:
        PATH_LABEL["short"] = "1b AGENT STREAM"
        PATH_LABEL["long"] = (
            "1b AGENT STREAM - selected by agent='%s', a non-empty string, "
            "which satisfies the routes.py:157 predicate. The server does "
            "not check that the id resolves. stream=%s"
            % (AGENT, "true" if STREAM else "false"))
    elif STREAM:
        PATH_LABEL["short"] = "1d PLAIN ENGINE STREAM"
        PATH_LABEL["long"] = (
            "1d PLAIN ENGINE STREAM - no agent field and no tools field in "
            "the body, so the routes.py:157 predicate is false and dispatch "
            "falls through to :159. stream=true")
    else:
        PATH_LABEL["short"] = "1a NON-STREAMING"
        PATH_LABEL["long"] = (
            "1a NON-STREAMING - stream=false, no agent field, no tools field")
'''))

# --- 3. request body ------------------------------------------------------
R.append((
'''    body = {
        "model": model,
        "messages": [{"role": "user",
                      "content": PROMPT_OVERRIDE or CHAT_PROMPT}],
        "stream": bool(STREAM),
    }
''',
'''    body = {
        "model": model,
        "messages": [{"role": "user",
                      "content": PROMPT_OVERRIDE or CHAT_PROMPT}],
        "stream": bool(STREAM),
    }
    if AGENT:
        # openjarvis-ws-probe-agent-v3: present ONLY when --agent is given.
        # Sending "agent": "" would be functionally identical to omitting it
        # - the server model stores '' and the predicate tests truthiness -
        # but it would stop no-agent runs being byte-identical to the two
        # already in the record, so it is not sent.
        body["agent"] = AGENT
'''))

# --- 4. turn end marker ---------------------------------------------------
R.append((
'''            chat_send(base, model, chat_timeout)
            print("chat POST returned   t+%s" % rel(CHAT.get("returned")))
''',
'''            chat_send(base, model, chat_timeout)
            TURN_END["at"] = time.time()   # openjarvis-ws-probe-agent-v3
            TURN_DONE.set()                # openjarvis-ws-probe-agent-v3
            print("chat POST returned   t+%s" % rel(CHAT.get("returned")))
'''))

# --- 5. recv loop, sliced wait + grace exit -------------------------------
R.append((
'''        while time.time() < end_at:
            remaining = end_at - time.time()
            try:
                msg = await asyncio.wait_for(conn.recv(), timeout=remaining)
            except asyncio.TimeoutError:
                break
''',
'''        while time.time() < end_at:
            remaining = end_at - time.time()
            # openjarvis-ws-probe-agent-v3: wait in short slices so the
            # post-turn grace check runs between frames rather than only at
            # the deadline.
            try:
                msg = await asyncio.wait_for(conn.recv(),
                                             timeout=min(remaining, 1.0))
            except asyncio.TimeoutError:
                if time.time() >= end_at:
                    EXIT_REASON["why"] = "deadline"
                    break
                if _grace_expired():
                    EXIT_REASON["why"] = "grace"
                    print("early exit           t+%-9s turn ended %.1f s ago,"
                          " no confirm outstanding"
                          % (rel(time.time()),
                             time.time() - TURN_END["at"]))
                    break
                continue
'''))

# --- 6. confirm tracking on every frame -----------------------------------
R.append((
'''            FRAMES.append(
                {
                    "recv": recv,
                    "internal": internal,
                    "type": etype,
                    "data": payload.get("data") or {},
                }
            )
''',
'''            FRAMES.append(
                {
                    "recv": recv,
                    "internal": internal,
                    "type": etype,
                    "data": payload.get("data") or {},
                }
            )
            _track_confirm(etype, payload.get("data") or {})
'''))

# --- 7. report: state the path and the selecting field --------------------
R.append((
'''    print("CHAT REQUEST")
    if not CHAT:
        print("  never sent")
''',
'''    print("CHAT REQUEST")
    print("  path          %s" % PATH_LABEL.get("long", "unknown"))
    print("  agent field   %s"
          % (("'%s' - sent in the body" % AGENT) if AGENT
             else "not present in the body"))
    print("  listener exit %s" % EXIT_REASON.get("why", "not recorded"))
    if not CHAT:
        print("  never sent")
'''))

# --- 8. verdict: use the same label -------------------------------------
R.append((
'''        print("  NO STALL REPRODUCED on the %s path."
              % ("STREAMING 1b (browser)" if STREAM else "NON-STREAMING 1a"))
''',
'''        print("  NO STALL REPRODUCED on the %s path."
              % PATH_LABEL.get("short", "UNKNOWN"))
'''))

# --- 9. args --------------------------------------------------------------
R.append((
'''    ap.add_argument("--prompt", default=None,
                    help="override the built-in prompt, to provoke the gate "
                         "deliberately rather than hope for it")
    args = ap.parse_args()

    global STREAM, PROMPT_OVERRIDE
    STREAM = bool(args.stream)
    PROMPT_OVERRIDE = args.prompt
''',
'''    ap.add_argument("--prompt", default=None,
                    help="override the built-in prompt, to provoke the gate "
                         "deliberately rather than hope for it")
    ap.add_argument("--agent", default=None,
                    help="agent id to send in the request body, selecting "
                         "PATH 1b. Any non-empty string satisfies the "
                         "routes.py:157 predicate and the server does not "
                         "check that it resolves. Omitted from the body "
                         "entirely when unset.")
    ap.add_argument("--grace", type=float, default=150.0,
                    help="seconds to keep listening after the turn ends "
                         "before exiting early. Never applies while a "
                         "confirm is outstanding.")
    args = ap.parse_args()

    global STREAM, PROMPT_OVERRIDE, AGENT, GRACE
    STREAM = bool(args.stream)
    PROMPT_OVERRIDE = args.prompt
    AGENT = args.agent or None
    GRACE = float(args.grace)
    _set_path_label()
'''))

# --- 10. banner -----------------------------------------------------------
R.append((
'''    print("  path      %s"
          % ("1b STREAMING - the browser chain" if STREAM
             else "1a NON-STREAMING"))
    print("  confirm   NOT approved - the gate is allowed to time out")
''',
'''    print("  path      %s" % PATH_LABEL.get("long", "unknown"))
    print("  grace     %.0f s after the turn ends, suppressed while a "
          "confirm is outstanding" % GRACE)
    print("  confirm   NOT approved - the gate is allowed to time out")
'''))


# ---------------------------------------------------------------------------

def fail(msg):
    print("REFUSED: %s" % msg)
    return 2


def main():
    if not os.path.isfile(TARGET):
        return fail("%s not found in %s" % (TARGET, os.getcwd()))

    raw = open(TARGET, "rb").read()
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        return fail("%s is not utf-8: %s" % (TARGET, exc))

    # idempotency
    if MARKER in text:
        print("ALREADY APPLIED: marker %s present. No change." % MARKER)
        return 0

    # prerequisite
    if PREREQ not in text:
        return fail("prerequisite marker %s absent - target is not at v2"
                    % PREREQ)

    # line endings
    crlf = "\r\n" in text
    print("line endings: %s" % ("CRLF" if crlf else "LF"))

    def xlate(s):
        return s.replace("\n", "\r\n") if crlf else s

    # exactly-once check across ALL replacements BEFORE any substitution
    prepared = []
    problems = []
    for i, (old, new) in enumerate(R, 1):
        o = xlate(old)
        n = xlate(new)
        count = text.count(o)
        if count != 1:
            head = old.strip().split("\n")[0][:66]
            problems.append("  replacement %d matched %d times: %s"
                            % (i, count, head))
        prepared.append((o, n))
    if problems:
        print("REFUSED: not every replacement matched exactly once.")
        for p in problems:
            print(p)
        return 2
    print("all %d replacements matched exactly once" % len(R))

    patched = text
    for o, n in prepared:
        patched = patched.replace(o, n, 1)

    if MARKER not in patched:
        return fail("patched text does not contain the marker - aborting")

    # temp-file compile before touching the real file
    tmpdir = tempfile.mkdtemp(prefix="ws_probe_v3_")
    tmpfile = os.path.join(tmpdir, "ws_probe_candidate.py")
    with open(tmpfile, "wb") as fh:
        fh.write(patched.encode("utf-8"))
    try:
        py_compile.compile(tmpfile, doraise=True)
        print("candidate compiles clean")
    except Exception as exc:
        shutil.rmtree(tmpdir, ignore_errors=True)
        return fail("candidate failed to compile, real file untouched: %s"
                    % exc)
    shutil.rmtree(tmpdir, ignore_errors=True)

    # timestamped backup
    bak = "%s.bak-%s" % (TARGET, time.strftime("%Y%m%d-%H%M%S"))
    shutil.copy2(TARGET, bak)
    print("backup: %s" % bak)

    with open(TARGET, "wb") as fh:
        fh.write(patched.encode("utf-8"))
    print("written: %s" % TARGET)

    def restore(why):
        shutil.copy2(bak, TARGET)
        print("RESTORED %s from %s" % (TARGET, bak))
        return fail(why)

    # post-write compile with self-restore
    try:
        py_compile.compile(TARGET, doraise=True)
        print("post-write compile clean")
    except Exception as exc:
        return restore("post-write compile failed: %s" % exc)

    # --help smoke run with self-restore
    try:
        proc = subprocess.run([sys.executable, TARGET, "--help"],
                              capture_output=True, text=True, timeout=60)
    except Exception as exc:
        return restore("--help smoke run could not start: %s" % exc)

    out = (proc.stdout or "") + (proc.stderr or "")
    if proc.returncode != 0:
        return restore("--help exited %d: %s" % (proc.returncode, out[:400]))
    for flag in ("--agent", "--grace"):
        if flag not in out:
            return restore("--help output does not list %s" % flag)
    print("--help smoke run clean, --agent and --grace present")

    print()
    print("V3 APPLIED. marker %s" % MARKER)
    print("rollback: Copy-Item '%s' '%s' -Force" % (bak, TARGET))
    return 0


if __name__ == "__main__":
    sys.exit(main())
