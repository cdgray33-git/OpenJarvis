#!/usr/bin/env python3
r"""
stream_probe_w70.py -- F-W70-NOSTREAM measurement.

PURPOSE
    Determine whether the OpenJarvis backend emits chat completion deltas
    INCREMENTALLY over the life of a generation, or accumulates the whole
    reply and flushes it as ONE BURST at the end.

    W70 established that the frontend is not at fault:
      - sse.ts reads response.body via reader.read() in a loop and yields
        per line. No body buffering. Incremental by construction.
      - ChatArea.tsx:266 sets stream content on every delta it receives.
      - A main-thread liveness probe measured gap=283ms / fps=17 during a
        31s generation: the UI thread was ALIVE, not starved.
    Yet StreamingDots (rendered only when content == '') were still on
    screen 31 seconds into a 382-token reply, and the text landed in one
    lump. So the deltas were not arriving. This probe asks the backend
    directly, with the frontend removed from the picture entirely.

METHOD
    Posts a real streaming request to /v1/chat/completions and records a
    monotonic timestamp for EVERY delta as it is read off the socket.
    Runs the request twice: once with agent=native_openhands (the agent
    selected during both observed failures) and once with no agent. That
    settles the agent-path question in the same pass.

READING THE RESULT
    SPREAD is the wall time between the first delta and the last one.
      - SPREAD close to TOTAL  -> backend streams correctly. The fault is
        downstream in the Tauri webview transport (proxy, compression, or
        buffering between the server socket and the webview fetch).
      - SPREAD near zero with a large TOTAL -> backend buffered the whole
        completion and flushed it at the end. The fault is server-side.

    Per the standing rule, this test is NON-INTERACTIVE: it runs to
    completion on its own and prints a verdict. Nothing depends on
    reacting to output inside a time window.

USAGE
    python .\tools\stream_probe_w70.py
    python .\tools\stream_probe_w70.py http://127.0.0.1:8000
    python .\tools\stream_probe_w70.py http://127.0.0.1:8000 qwen3-coder:30b

    Stdlib only. No third-party packages.
"""

import json
import sys
import time
import urllib.error
import urllib.request

# Python block-buffers stdout when it is piped (Tee-Object, redirection).
# Without this the probe prints NOTHING until it exits, which makes a live
# run indistinguishable from a hang. Line buffering makes it readable as it
# runs -- an instrument you cannot read is an instrument you do not have.
try:
    sys.stdout.reconfigure(line_buffering=True)
except Exception:
    pass

DEFAULT_BASES = [
    "http://127.0.0.1:8000",
    "http://localhost:8000",
    "http://127.0.0.1:8080",
    "http://127.0.0.1:5000",
    "http://127.0.0.1:3001",
]

DEFAULT_MODEL = "qwen3-coder:30b"

# Long enough to make buffering obvious, cheap enough to run twice.
PROMPT = (
    "Count slowly from 1 to 40. Put each number on its own line "
    "with a short sentence about it. Do not use any tools."
)

READ_TIMEOUT = 180


def probe_base(base):
    """Return True if something answers on this base URL."""
    for path in ("/v1/models", "/health", "/"):
        try:
            req = urllib.request.Request(base + path, method="GET")
            with urllib.request.urlopen(req, timeout=2) as r:
                if r.status < 500:
                    return True
        except urllib.error.HTTPError:
            return True
        except Exception:
            continue
    return False


def find_base(argv_base):
    if argv_base:
        if probe_base(argv_base):
            print("BASE: " + argv_base + " (from argument)")
            return argv_base
        print("FATAL: nothing answering at " + argv_base)
        print("Is the backend running? Pass the correct base URL as argument 1.")
        sys.exit(2)

    for b in DEFAULT_BASES:
        if probe_base(b):
            print("BASE: " + b + " (auto-detected)")
            return b

    print("FATAL: no backend found on any default port.")
    print("Tried: " + ", ".join(DEFAULT_BASES))
    print("Pass the correct base URL as argument 1, e.g.:")
    print("    python .\\tools\\stream_probe_w70.py http://127.0.0.1:9000")
    sys.exit(2)


def run_case(base, model, agent, label):
    print("")
    print("=" * 68)
    print("CASE: " + label)
    print("  agent=" + (repr(agent) if agent else "(none)"))
    print("=" * 68)

    payload = {
        "model": model,
        "messages": [{"role": "user", "content": PROMPT}],
        "stream": True,
        "temperature": 0.0,
        "max_tokens": 900,
    }
    if agent:
        payload["agent"] = agent

    body = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        base + "/v1/chat/completions",
        data=body,
        method="POST",
        headers={"Content-Type": "application/json", "Accept": "text/event-stream"},
    )

    deltas = []          # (elapsed_seconds, n_chars)
    events = {}          # named SSE event -> count
    total_chars = 0
    first_byte = None

    t0 = time.perf_counter()
    try:
        resp = urllib.request.urlopen(req, timeout=READ_TIMEOUT)
    except urllib.error.HTTPError as e:
        print("HTTP ERROR " + str(e.code))
        try:
            print(e.read().decode("utf-8", "replace")[:800])
        except Exception:
            pass
        return None
    except Exception as e:
        print("REQUEST FAILED: " + repr(e))
        return None

    print("  status=" + str(resp.status))
    ct = resp.headers.get("Content-Type", "?")
    print("  content-type=" + ct)
    # These three headers are the usual culprits when a server streams but a
    # proxy does not. Recorded regardless of outcome.
    for h in ("Transfer-Encoding", "Content-Encoding", "Content-Length",
              "X-Accel-Buffering", "Cache-Control", "Connection"):
        v = resp.headers.get(h)
        if v:
            print("  " + h.lower() + "=" + v)
    print("  --- reading stream ---")

    current_event = None
    try:
        while True:
            line = resp.readline()
            if not line:
                break
            now = time.perf_counter() - t0
            if first_byte is None:
                first_byte = now

            try:
                text = line.decode("utf-8", "replace").rstrip("\r\n")
            except Exception:
                continue

            if text.startswith("event: "):
                current_event = text[7:].strip()
                events[current_event] = events.get(current_event, 0) + 1
                continue
            if not text.startswith("data: "):
                if text.strip() == "":
                    current_event = None
                continue

            data = text[6:]
            if data.strip() == "[DONE]":
                break

            try:
                obj = json.loads(data)
            except Exception:
                continue

            choices = obj.get("choices") or []
            if choices:
                delta = choices[0].get("delta") or {}
                content = delta.get("content")
                if content:
                    deltas.append((now, len(content)))
                    total_chars += len(content)
                if choices[0].get("finish_reason") == "stop":
                    break
    except Exception as e:
        print("  READ ABORTED: " + repr(e))
    finally:
        try:
            resp.close()
        except Exception:
            pass

    total = time.perf_counter() - t0

    print("")
    print("  RESULTS")
    print("    total wall time   : %.2f s" % total)
    print("    first byte        : %s" % ("%.2f s" % first_byte if first_byte is not None else "never"))
    print("    delta count       : %d" % len(deltas))
    print("    chars received    : %d" % total_chars)
    if events:
        print("    named events      : " + ", ".join(
            k + "=" + str(v) for k, v in sorted(events.items())))

    if not deltas:
        print("    NO CONTENT DELTAS SEEN.")
        print("    VERDICT: cannot measure spread. Check status/content-type above.")
        return {"label": label, "verdict": "no-deltas", "total": total}

    first = deltas[0][0]
    last = deltas[-1][0]
    spread = last - first

    print("    first delta at    : %.2f s" % first)
    print("    last delta at     : %.2f s" % last)
    print("    SPREAD            : %.2f s" % spread)

    # Timeline sample: enough to see the shape without flooding the log.
    print("")
    print("  TIMELINE (first 5 / last 5 deltas, seconds from request)")
    for t, n in deltas[:5]:
        print("    %8.3f s  +%d chars" % (t, n))
    if len(deltas) > 10:
        print("    ...  %d deltas omitted  ..." % (len(deltas) - 10))
    for t, n in deltas[-5:]:
        print("    %8.3f s  +%d chars" % (t, n))

    # Largest inter-delta gaps: where the stream stalled, if it stalled.
    gaps = []
    for i in range(1, len(deltas)):
        gaps.append((deltas[i][0] - deltas[i - 1][0], deltas[i - 1][0]))
    gaps.sort(reverse=True)
    if gaps:
        print("")
        print("  LARGEST INTER-DELTA GAPS")
        for g, at in gaps[:5]:
            print("    %6.3f s gap, starting at %.2f s" % (g, at))

    # Verdict.
    print("")
    if len(deltas) < 5:
        verdict = "too-few-deltas"
        print("  VERDICT: only %d deltas. Reply may be short or chunked coarsely." % len(deltas))
    elif spread < 0.5 and total > 3.0:
        verdict = "BUFFERED"
        print("  VERDICT: BUFFERED BURST.")
        print("  %d deltas arrived within %.2f s at the END of a %.2f s" % (len(deltas), spread, total))
        print("  generation. The backend accumulated the reply and flushed it")
        print("  at once. The fault is SERVER-SIDE. The frontend never had")
        print("  anything to render incrementally.")
    elif spread > (total * 0.5):
        verdict = "STREAMING"
        print("  VERDICT: BACKEND STREAMS CORRECTLY.")
        print("  %d deltas spread over %.2f s of a %.2f s generation." % (len(deltas), spread, total))
        print("  The backend is not the fault. Since sse.ts and ChatArea are")
        print("  already cleared, the collapse is in the TAURI WEBVIEW")
        print("  TRANSPORT between this socket and the app's fetch.")
    else:
        verdict = "PARTIAL"
        print("  VERDICT: PARTIAL / AMBIGUOUS.")
        print("  Spread %.2f s against total %.2f s. Inspect the gaps above:" % (spread, total))
        print("  a long lead-in then a fast tail usually means the model was")
        print("  still loading or a tool call ran before generation started.")

    return {
        "label": label,
        "verdict": verdict,
        "total": total,
        "spread": spread,
        "deltas": len(deltas),
        "chars": total_chars,
    }


def main():
    argv_base = sys.argv[1] if len(sys.argv) > 1 else None
    model = sys.argv[2] if len(sys.argv) > 2 else DEFAULT_MODEL

    print("stream_probe_w70 -- F-W70-NOSTREAM")
    print("started " + time.strftime("%Y-%m-%d %H:%M:%S"))
    print("model: " + model)

    base = find_base(argv_base)

    results = []
    # Agent case first: it is the configuration both observed failures used.
    r1 = run_case(base, model, "native_openhands", "WITH AGENT (native_openhands)")
    if r1:
        results.append(r1)
    r2 = run_case(base, model, "", "NO AGENT (plain completion)")
    if r2:
        results.append(r2)

    print("")
    print("=" * 68)
    print("SUMMARY")
    print("=" * 68)
    for r in results:
        if "spread" in r:
            print("  %-32s %-10s total=%6.2fs spread=%6.2fs deltas=%d" % (
                r["label"], r["verdict"], r["total"], r["spread"], r["deltas"]))
        else:
            print("  %-32s %s" % (r["label"], r["verdict"]))

    verdicts = set(r["verdict"] for r in results)
    print("")
    if verdicts == {"BUFFERED"}:
        print("  BOTH paths buffer. The agent is not the variable.")
        print("  NEXT: find where the completion is accumulated server-side.")
    elif "BUFFERED" in verdicts and "STREAMING" in verdicts:
        print("  THE PATHS DIFFER. The agent path is the variable.")
        print("  NEXT: the agent wrapper accumulates the turn before emitting.")
    elif verdicts == {"STREAMING"}:
        print("  BOTH paths stream at the socket. The backend is cleared.")
        print("  NEXT: the Tauri webview transport is the remaining suspect.")
    else:
        print("  Mixed or ambiguous. Read the per-case output above.")
    print("")
    print("finished " + time.strftime("%Y-%m-%d %H:%M:%S"))


if __name__ == "__main__":
    main()
