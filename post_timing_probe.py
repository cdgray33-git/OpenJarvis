"""
post_timing_probe.py

Isolates the v3 "sender thread stalls before the POST leaves" finding.

Shares NOTHING with ws_probe.py: no urllib, no websockets, no asyncio, no
threads. A single raw socket, written and read inline, with a timestamp at
every stage boundary. If a stall exists it lands in one named gap.

Stages measured:
  socket create -> TCP connect -> request bytes handed to the OS ->
  first response byte -> headers complete -> body complete

Interpretation:
  stall in CONNECT            -> network / listener backlog
  stall in SEND               -> client side, and NOT v3-specific
  stall in WAIT_FIRST_BYTE    -> server: request accepted, response not started
  stall in BODY               -> server: generating slowly (expected for a model)
  no stall anywhere           -> the stall belongs to v3's own machinery

Runs to completion on its own. No interaction required.

Run from repo root: C:\\Users\\Admin\\OpenJarvis
"""

import argparse
import json
import socket
import sys
import time

T0 = time.time()


def rel(t):
    return "t+%7.3f" % (t - T0)


def mark(label, t, prev):
    gap = t - prev
    flag = "   <-- STALL" if gap > 2.0 else ""
    print("  %-18s %s   gap %8.3f s%s" % (label, rel(t), gap, flag))
    return t


def run(host, port, model, prompt, timeout, agent):
    body = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "stream": False,
    }
    if agent:
        body["agent"] = agent
    payload = json.dumps(body).encode("utf-8")

    request = (
        "POST /v1/chat/completions HTTP/1.1\r\n"
        "Host: %s:%d\r\n"
        "Content-Type: application/json\r\n"
        "Content-Length: %d\r\n"
        "Connection: close\r\n"
        "\r\n"
    ) % (host, port, len(payload))
    raw = request.encode("ascii") + payload

    print("request bytes       %d (headers %d + body %d)"
          % (len(raw), len(raw) - len(payload), len(payload)))
    print("")
    print("STAGE TIMELINE")

    t = time.time()
    start = t
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(timeout)
    t = mark("socket created", time.time(), t)

    try:
        s.connect((host, port))
    except Exception as exc:
        print("  CONNECT FAILED: %s: %s" % (type(exc).__name__, exc))
        return 1
    t = mark("tcp connected", time.time(), t)

    try:
        s.sendall(raw)
    except Exception as exc:
        print("  SEND FAILED: %s: %s" % (type(exc).__name__, exc))
        return 1
    t_sent = time.time()
    t = mark("request sent", t_sent, t)

    chunks = []
    first_byte_at = None
    header_end_at = None
    seen = b""
    try:
        while True:
            buf = s.recv(65536)
            if not buf:
                break
            now = time.time()
            if first_byte_at is None:
                first_byte_at = now
                t = mark("first byte", now, t)
            if header_end_at is None:
                seen += buf
                if b"\r\n\r\n" in seen:
                    header_end_at = now
                    t = mark("headers complete", now, t)
            chunks.append(buf)
    except socket.timeout:
        print("  RECV TIMEOUT after %.1f s" % timeout)
    except Exception as exc:
        print("  RECV FAILED: %s: %s" % (type(exc).__name__, exc))
    finally:
        try:
            s.close()
        except Exception:
            pass

    t_done = time.time()
    if first_byte_at is not None:
        mark("body complete", t_done, t)

    data = b"".join(chunks)
    print("")
    print("SUMMARY")
    print("  total elapsed        %8.3f s" % (t_done - start))
    if first_byte_at is not None:
        print("  send -> first byte   %8.3f s   <-- the number in question"
              % (first_byte_at - t_sent))
        print("  first byte -> done   %8.3f s" % (t_done - first_byte_at))
    else:
        print("  NO RESPONSE BYTES RECEIVED")
    print("  bytes received       %d" % len(data))

    head, _, tail = data.partition(b"\r\n\r\n")
    status = head.split(b"\r\n")[0].decode("ascii", "replace") if head else "(none)"
    print("  status line          %s" % status)
    try:
        parsed = json.loads(tail.decode("utf-8", "replace"))
        choices = parsed.get("choices") or []
        if choices:
            msg = choices[0].get("message") or {}
            content = (msg.get("content") or "")[:200]
            print("  finish_reason        %s" % choices[0].get("finish_reason"))
            print("  content (200 chars)  %s" % content.replace("\n", " "))
    except Exception:
        print("  body not JSON-parseable, first 200 bytes:")
        print("  %s" % tail[:200].decode("utf-8", "replace").replace("\n", " "))

    return 0


def main():
    ap = argparse.ArgumentParser(description="raw-socket POST timing probe")
    ap.add_argument("--host", default="127.0.0.1")
    ap.add_argument("--port", type=int, default=8010)
    ap.add_argument("--model", default="qwen3-coder:30b")
    ap.add_argument("--prompt", default="Reply with the single word: ping")
    ap.add_argument("--timeout", type=float, default=300.0)
    ap.add_argument("--agent", default=None,
                    help="send an agent id, selecting PATH 1b")
    ap.add_argument("--repeat", type=int, default=1)
    args = ap.parse_args()

    print("=" * 74)
    print("POST timing probe - raw socket, nothing shared with ws_probe.py")
    print("  target   http://%s:%d/v1/chat/completions" % (args.host, args.port))
    print("  model    %s" % args.model)
    print("  path     %s" % ("1b (agent sent)" if args.agent else "1a (no agent)"))
    print("=" * 74)

    rc = 0
    for i in range(args.repeat):
        if args.repeat > 1:
            print("")
            print("--- RUN %d of %d ---" % (i + 1, args.repeat))
        rc = run(args.host, args.port, args.model, args.prompt,
                 args.timeout, args.agent) or rc
    return rc


if __name__ == "__main__":
    sys.exit(main())
