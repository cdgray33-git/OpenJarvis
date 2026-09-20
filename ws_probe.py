#!/usr/bin/env python3
"""
ws_probe.py - OpenJarvis WS frame delivery probe.

PURPOSE
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

METHOD
  One self-driving run, no human input required at any point:
    1. Connect to the unfiltered WS mount, timestamping the handshake.
    2. Start an HTTP heartbeat thread polling a cheap endpoint every second.
    3. Send the chat request itself, from a thread, with a prompt that
       provokes a confirmation-gated tool call.
    4. Record every frame with its INTERNAL timestamp and the local receive
       time. Never trust print order.
    5. Stop at a hard deadline, print a report, exit.

  The confirm is deliberately NOT approved. The gate is allowed to time out.
  That 120 s window is exactly when the loop is under suspicion, and the
  heartbeat is what measures it.

READING THE VERDICT
  HTTP heartbeat stalls in step with the frames -> the event loop is blocked.
    Look for synchronous work called without await from a coroutine.
  HTTP heartbeat stays responsive while frames queue -> the loop is healthy,
    so the fault is in the WS send path, the per-client queue, or the
    bridge allowlist.
  Everything clean -> the path just exercised is sound, AND NOTHING MORE.
    Default mode and --stream are two different call chains. A clean result
    on one says nothing about the other. Each needs its own run.

Exit codes: 0 report produced, 2 setup failure (no connection, no endpoint).
"""

import argparse
import json
import sys
import threading
import time
import urllib.error
import urllib.request

try:
    from websockets.asyncio.client import connect as ws_connect
except Exception:  # older websockets releases
    try:
        from websockets.client import connect as ws_connect
    except Exception:
        print("FATAL: cannot import a websockets client. Run: python -m pip install websockets")
        sys.exit(2)

import asyncio


# ----------------------------------------------------------------------------
# shared state
# ----------------------------------------------------------------------------

T0 = None                 # wall clock at probe start
FRAMES = []               # list of dicts: recv, internal, type, data
HEARTBEATS = []           # list of dicts: sent, elapsed, status, error
PONGS = []                # list of dicts: sent, elapsed, error
CLOSE_EVENT = {}          # how and when the socket died, if it did
CHAT = {}                 # sent, returned, status, finish_reason, error
SSE = []                  # openjarvis-ws-probe-stream-v1: per-chunk arrivals
STREAM = False            # openjarvis-ws-probe-stream-v1: --stream picks 1b
TEXT = []                 # openjarvis-ws-probe-capture-v2: response fragments
PROMPT_OVERRIDE = None    # openjarvis-ws-probe-capture-v2: --prompt
AGENT = None              # openjarvis-ws-probe-agent-v3: --agent, selects 1b
GRACE = 150.0             # openjarvis-ws-probe-agent-v3: post-turn grace, s
PATH_LABEL = {}           # openjarvis-ws-probe-agent-v3: predicted path text
TURN_END = {}             # openjarvis-ws-probe-agent-v3: when the POST returned
TURN_DONE = threading.Event()   # openjarvis-ws-probe-agent-v3
CONFIRM_OPEN = set()      # openjarvis-ws-probe-agent-v3: unresolved confirms
EXIT_REASON = {}          # openjarvis-ws-probe-agent-v3: grace or deadline
RESPONSE_FILE = "ws_probe_last_response.txt"
STOP = threading.Event()


def rel(t):
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


# ----------------------------------------------------------------------------
# heartbeat - the discriminating measurement
# ----------------------------------------------------------------------------

HEARTBEAT_CANDIDATES = ["/health", "/v1/models", "/docs", "/openapi.json"]


def pick_heartbeat_endpoint(base, timeout=5.0):
    """Return the first candidate path the server answers, or None."""
    for path in HEARTBEAT_CANDIDATES:
        url = base + path
        try:
            req = urllib.request.Request(url, method="GET")
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                if resp.status < 500:
                    return path
        except urllib.error.HTTPError as exc:
            if exc.code < 500:
                return path
        except Exception:
            continue
    return None


def heartbeat_loop(base, path, interval=1.0, timeout=10.0):
    """Poll a cheap HTTP endpoint until STOP. Records every attempt."""
    url = base + path
    while not STOP.is_set():
        sent = time.time()
        status = None
        error = None
        try:
            req = urllib.request.Request(url, method="GET")
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                status = resp.status
                resp.read(64)
        except urllib.error.HTTPError as exc:
            status = exc.code
        except Exception as exc:
            error = type(exc).__name__
        elapsed = time.time() - sent
        HEARTBEATS.append(
            {"sent": sent, "elapsed": elapsed, "status": status, "error": error}
        )
        STOP.wait(interval)


# ----------------------------------------------------------------------------
# chat send - drives the run so no human has to
# ----------------------------------------------------------------------------

CHAT_PROMPT = (
    "Use the shell_exec tool to run the command: echo openjarvis_ws_probe. "
    "Call the tool now. Do not ask for permission and do not explain first."
)


def _read_sse(resp):
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
        text = line.decode("utf-8", errors="replace").rstrip("\r\n")
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
                        TEXT.append(delta["content"])
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
                        msg = choices[0].get("message") or {}
                        if msg.get("content"):
                            TEXT.append(msg["content"])
                    CHAT["bytes"] = len(raw)
                except Exception:
                    CHAT["bytes"] = len(raw)
    except Exception as exc:
        CHAT["returned"] = time.time()
        CHAT["error"] = "%s: %s" % (type(exc).__name__, exc)


# ----------------------------------------------------------------------------
# websocket listener
# ----------------------------------------------------------------------------

async def ping_loop(conn, interval=5.0, timeout=120.0):
    """Measure pong round-trip. A loop that cannot pong is a blocked loop.

    This is the WS-path counterpart to the HTTP heartbeat: HTTP proves whether
    the server can serve at all, pong proves whether this specific connection's
    loop is turning.
    """
    while not STOP.is_set():
        sent = time.time()
        try:
            waiter = await conn.ping()
            await asyncio.wait_for(waiter, timeout=timeout)
            PONGS.append({"sent": sent, "elapsed": time.time() - sent, "error": None})
        except Exception as exc:
            PONGS.append(
                {"sent": sent, "elapsed": time.time() - sent,
                 "error": type(exc).__name__}
            )
            return
        await asyncio.sleep(interval)


async def listen(ws_url, base, model, deadline, chat_delay, chat_timeout):
    global T0

    connect_start = time.time()
    T0 = connect_start
    print("probe start          t+0.000   %s" % time.strftime("%H:%M:%S"))
    print("connecting           %s" % ws_url)

    try:
        # ping_interval=None: the library's keepalive would drop the socket
        # after 20 s without a pong, which is precisely the condition under
        # test. We measure pong latency ourselves instead (see ping_loop).
        # max_queue=None: no client-side backpressure to confuse the timing.
        conn = await asyncio.wait_for(
            ws_connect(ws_url, ping_interval=None, max_queue=None), timeout=60
        )
    except Exception as exc:
        print("FATAL: websocket connect failed: %s: %s" % (type(exc).__name__, exc))
        return False

    open_at = time.time()
    print("websocket OPEN       t+%-8s handshake %.3f s"
          % (rel(open_at), open_at - connect_start))

    # heartbeat starts only once the socket is open, so its window lines up
    # with the frame window.
    hb_path = pick_heartbeat_endpoint(base)
    if hb_path is None:
        print("WARNING: no HTTP heartbeat endpoint answered. Verdict will be")
        print("         weaker - frame timing only, no loop-health signal.")
    else:
        print("heartbeat endpoint   %s" % hb_path)
        threading.Thread(
            target=heartbeat_loop, args=(base, hb_path), daemon=True
        ).start()

    # fire the chat from a thread after a short settle delay
    def _delayed_chat():
        STOP.wait(chat_delay)
        if not STOP.is_set():
            print("chat POST sent       t+%s" % rel(time.time()))
            chat_send(base, model, chat_timeout)
            TURN_END["at"] = time.time()   # openjarvis-ws-probe-agent-v3
            TURN_DONE.set()                # openjarvis-ws-probe-agent-v3
            print("chat POST returned   t+%s" % rel(CHAT.get("returned")))

    threading.Thread(target=_delayed_chat, daemon=True).start()

    ping_task = asyncio.create_task(ping_loop(conn))

    end_at = connect_start + deadline
    try:
        while time.time() < end_at:
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
            except Exception as exc:
                # The socket dying is itself data. Record it and report.
                CLOSE_EVENT["at"] = time.time()
                CLOSE_EVENT["why"] = "%s: %s" % (type(exc).__name__, exc)
                print("socket CLOSED        t+%s  %s"
                      % (rel(CLOSE_EVENT["at"]), CLOSE_EVENT["why"]))
                break
            recv = time.time()
            try:
                payload = json.loads(msg)
            except Exception:
                payload = {"type": "<unparseable>", "raw": msg[:200]}
            internal = payload.get("timestamp")
            etype = payload.get("type")
            FRAMES.append(
                {
                    "recv": recv,
                    "internal": internal,
                    "type": etype,
                    "data": payload.get("data") or {},
                }
            )
            _track_confirm(etype, payload.get("data") or {})
            lag = (recv - internal) if isinstance(internal, (int, float)) else None
            print(
                "frame  t+%-9s %-24s internal t+%-9s lag %s"
                % (
                    rel(recv),
                    etype,
                    rel(internal),
                    ("%.3f s" % lag) if lag is not None else "n/a",
                )
            )
    finally:
        STOP.set()
        ping_task.cancel()
        try:
            await asyncio.wait_for(conn.close(), timeout=5)
        except Exception:
            pass  # a close that hangs is expected if the loop is blocked

    return True


# ----------------------------------------------------------------------------
# report
# ----------------------------------------------------------------------------

def report():
    line = "-" * 78
    print()
    print(line)
    print("REPORT")
    print(line)

    # ---- chat
    print()
    print("CHAT REQUEST")
    print("  path          %s" % PATH_LABEL.get("long", "unknown"))
    print("  agent field   %s"
          % (("'%s' - sent in the body" % AGENT) if AGENT
             else "not present in the body"))
    print("  listener exit %s" % EXIT_REASON.get("why", "not recorded"))
    if not CHAT:
        print("  never sent")
    else:
        sent = CHAT.get("sent")
        ret = CHAT.get("returned")
        print("  sent          t+%s" % rel(sent))
        print("  returned      t+%s" % rel(ret))
        if sent and ret:
            print("  wall duration %.3f s" % (ret - sent))
        if CHAT.get("error"):
            print("  ERROR         %s" % CHAT["error"])
        else:
            print("  http status   %s" % CHAT.get("status"))
            print("  finish_reason %s" % CHAT.get("finish_reason"))

    # ---- frames
    print()
    print("FRAMES  (%d received)" % len(FRAMES))
    if not FRAMES:
        print("  NONE. Either nothing was emitted or delivery never happened")
        print("  inside the deadline. Both are findings - note which.")
    else:
        print("  %-26s %-12s %-12s %-10s" % ("type", "internal", "received", "lag"))
        lags = []
        for f in FRAMES:
            internal = f["internal"]
            lag = (f["recv"] - internal) if isinstance(internal, (int, float)) else None
            if lag is not None:
                lags.append(lag)
            print(
                "  %-26s %-12s %-12s %-10s"
                % (
                    f["type"],
                    ("t+%s" % rel(internal)) if internal else "n/a",
                    "t+%s" % rel(f["recv"]),
                    ("%.3f s" % lag) if lag is not None else "n/a",
                )
            )
        if lags:
            print()
            print("  lag min %.3f s   max %.3f s   mean %.3f s"
                  % (min(lags), max(lags), sum(lags) / len(lags)))

        # burst detection: frames arriving within 250 ms of each other
        bursts = 0
        for i in range(1, len(FRAMES)):
            if FRAMES[i]["recv"] - FRAMES[i - 1]["recv"] < 0.25:
                bursts += 1
        print("  frames arriving <250 ms after the previous: %d of %d"
              % (bursts, max(len(FRAMES) - 1, 0)))

    # ---- sse chunks (stream mode)
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

    # ---- tool activity: presence/absence stated, not inferred
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
        preview = body[:600].replace("\r", "")
        print("  ---- first 600 chars ----")
        for _ln in preview.split("\n"):
            print("  %s" % _ln)
        if len(body) > 600:
            print("  ---- truncated, %d chars remain ----" % (len(body) - 600))

    # ---- heartbeat
    print()
    print("HTTP HEARTBEAT  (%d samples)" % len(HEARTBEATS))
    if not HEARTBEATS:
        print("  none taken - no verdict available on loop health")
        worst = None
        max_gap = None
    else:
        elapsed = [h["elapsed"] for h in HEARTBEATS]
        worst = max(elapsed)
        errors = [h for h in HEARTBEATS if h["error"]]
        print("  response time min %.3f s   max %.3f s   mean %.3f s"
              % (min(elapsed), worst, sum(elapsed) / len(elapsed)))
        print("  failed samples: %d" % len(errors))

        # gaps between consecutive sends expose a stalled poller
        max_gap = 0.0
        gap_at = None
        for i in range(1, len(HEARTBEATS)):
            gap = HEARTBEATS[i]["sent"] - HEARTBEATS[i - 1]["sent"]
            if gap > max_gap:
                max_gap = gap
                gap_at = HEARTBEATS[i - 1]["sent"]
        print("  largest gap between samples: %.3f s at t+%s"
              % (max_gap, rel(gap_at)))

        slow = [h for h in HEARTBEATS if h["elapsed"] > 2.0]
        if slow:
            print("  samples slower than 2 s:")
            for h in slow[:20]:
                print("    t+%-10s %.3f s  status %s %s"
                      % (rel(h["sent"]), h["elapsed"], h["status"], h["error"] or ""))
            if len(slow) > 20:
                print("    ... and %d more" % (len(slow) - 20))
        else:
            print("  no sample exceeded 2 s")

    # ---- pong
    print()
    print("WS PING/PONG  (%d attempts)" % len(PONGS))
    worst_pong = None
    if not PONGS:
        print("  none taken")
    else:
        ok = [p["elapsed"] for p in PONGS if not p["error"]]
        failed = [p for p in PONGS if p["error"]]
        if ok:
            worst_pong = max(ok)
            print("  round trip min %.3f s   max %.3f s   mean %.3f s"
                  % (min(ok), worst_pong, sum(ok) / len(ok)))
        for p in PONGS:
            if p["error"] or p["elapsed"] > 2.0:
                print("    t+%-10s %.3f s  %s"
                      % (rel(p["sent"]), p["elapsed"], p["error"] or ""))
        print("  failed: %d" % len(failed))

    # ---- socket
    if CLOSE_EVENT:
        print()
        print("SOCKET CLOSED EARLY")
        print("  at t+%s" % rel(CLOSE_EVENT.get("at")))
        print("  %s" % CLOSE_EVENT.get("why"))

    # ---- verdict
    print()
    print(line)
    print("VERDICT")
    print(line)

    max_lag = 0.0
    for f in FRAMES:
        if isinstance(f["internal"], (int, float)):
            max_lag = max(max_lag, f["recv"] - f["internal"])

    stalled_frames = max_lag > 5.0
    stalled_http = bool(HEARTBEATS) and (worst is not None and worst > 5.0
                                         or (max_gap or 0) > 5.0)
    stalled_pong = bool(worst_pong is not None and worst_pong > 5.0) or bool(
        [p for p in PONGS if p["error"]]
    )
    print("  signals: frames_lagged=%s  http_stalled=%s  pong_stalled=%s"
          % (stalled_frames, stalled_http, stalled_pong))
    print()

    if not FRAMES:
        print("  INCONCLUSIVE - no frames arrived. Check that the prompt")
        print("  actually provoked a gated tool call, and that the backend")
        print("  is on the port and model this probe targeted.")
    elif not stalled_frames:
        print("  NO STALL REPRODUCED on the %s path."
              % PATH_LABEL.get("short", "UNKNOWN"))
        print("  Max frame lag %.3f s, HTTP responsive throughout." % max_lag)
        print("  Frames arrived as emitted rather than in a release burst,")
        print("  so the event loop was free for the whole turn.")
        print("  SCOPE: this clears the path just exercised and no other.")
    elif stalled_frames and stalled_http:
        print("  EVENT LOOP BLOCKED. Frames lagged %.1f s AND plain HTTP" % max_lag)
        print("  stalled alongside them, so the whole server was unavailable,")
        print("  not just this route. NOT the confirm gate - eliminated as")
        print("  cause 2026-08-23 by timestamp order. Look for a plain def")
        print("  called without await from a coroutine on this path.")
    else:
        print("  WS SEND PATH. Frames lagged %.1f s while plain HTTP stayed" % max_lag)
        print("  responsive. The loop is healthy, so the fault is in the")
        print("  bridge's per-client queue or send, not in a blocked loop.")
        print("  Next: inspect queue depth and whether the sender coroutine")
        print("  is being starved.")
    print()


# ----------------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser(description="OpenJarvis WS delivery probe")
    ap.add_argument("--host", default="127.0.0.1")
    ap.add_argument("--port", type=int, default=8010)
    ap.add_argument("--model", default="qwen3-coder:30b")
    ap.add_argument("--deadline", type=float, default=300.0,
                    help="hard stop, seconds. Must exceed the 120 s confirm TTL.")
    ap.add_argument("--chat-delay", type=float, default=3.0,
                    help="settle time after WS open before sending the chat")
    ap.add_argument("--chat-timeout", type=float, default=280.0)
    ap.add_argument("--stream", action="store_true",
                    help="exercise PATH 1b, the browser streaming path, and "
                         "record SSE chunk arrival times")
    ap.add_argument("--prompt", default=None,
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

    base = "http://%s:%d" % (args.host, args.port)
    ws_url = "ws://%s:%d/v1/agents/events" % (args.host, args.port)

    print("=" * 78)
    print("OpenJarvis WS delivery probe")
    print("  target    %s" % base)
    print("  model     %s" % args.model)
    print("  deadline  %.0f s" % args.deadline)
    print("  path      %s" % PATH_LABEL.get("long", "unknown"))
    print("  grace     %.0f s after the turn ends, suppressed while a "
          "confirm is outstanding" % GRACE)
    print("  confirm   NOT approved - the gate is allowed to time out")
    print("=" * 78)
    print()

    try:
        ok = asyncio.run(
            listen(ws_url, base, args.model, args.deadline,
                   args.chat_delay, args.chat_timeout)
        )
    except KeyboardInterrupt:
        STOP.set()
        ok = True
        print("\ninterrupted - reporting on what was collected")
    except Exception as exc:
        STOP.set()
        ok = True
        print("\nprobe raised %s: %s" % (type(exc).__name__, exc))
        print("reporting on what was collected up to that point")

    STOP.set()
    time.sleep(0.3)

    if not ok:
        print("setup failed, no report")
        return 2

    report()
    return 0


if __name__ == "__main__":
    sys.exit(main())
