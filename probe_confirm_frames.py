"""
probe_confirm_frames.py
6e UI prep: capture one FULL, UNTRUNCATED tool_confirm_request / tool_confirm_resolved
frame off the event bus WebSocket, so the frontend is written against observed fields
rather than against patch source.

Marker: openjarvis-confirm-frames-v1

WHAT IT DOES
  Connects to ws://127.0.0.1:8010/v1/agents/events (read-only subscriber).
  Prints every frame it receives, full JSON, no truncation.
  Writes the same to confirm_frames_capture.log in the current directory.
  Exits ON ITS OWN when it has seen a tool_confirm_resolved frame (plus a short
  trailing grace to catch anything that follows it), or at the deadline.

WHAT IT DOES NOT DO
  It sends nothing. It provokes nothing. It resolves no confirmation.
  It leaves no process, listener or socket behind.

USAGE
  Start it FIRST, then send a shell_exec-provoking prompt in the desktop app
  (for example: run hostname). There is no time pressure - the default deadline
  is 600 s and the gate TTL is 120 s.

  PS C:\\Users\\Admin\\OpenJarvis> python .\\probe_confirm_frames.py

  Options:
    --deadline 600     total seconds to listen before giving up
    --grace 5          seconds to keep listening after the resolved frame
    --url ws://...     override the endpoint
"""

from __future__ import annotations

import argparse
import asyncio
import datetime
import json
import sys

MARKER = "openjarvis-confirm-frames-v1"
DEFAULT_URL = "ws://127.0.0.1:8010/v1/agents/events"
LOGNAME = "confirm_frames_capture.log"

WANT_RESOLVED = "tool_confirm_resolved"
WANT_REQUEST = "tool_confirm_request"


def stamp() -> str:
    return datetime.datetime.now().strftime("%H:%M:%S.%f")[:-3]


class Sink:
    def __init__(self, path: str) -> None:
        self.path = path
        self.fh = open(path, "w", encoding="utf-8", newline="")

    def write(self, line: str) -> None:
        print(line)
        self.fh.write(line + "\n")
        self.fh.flush()

    def close(self) -> None:
        try:
            self.fh.close()
        except OSError:
            pass


def describe(obj) -> str:
    """Full JSON, sorted keys, no truncation anywhere."""
    try:
        return json.dumps(obj, indent=2, sort_keys=True, ensure_ascii=False)
    except (TypeError, ValueError):
        return repr(obj)


def event_name(obj) -> str:
    """Frames may carry the type under any of several keys - do not assume one."""
    if not isinstance(obj, dict):
        return ""
    for key in ("type", "event", "event_type", "name"):
        val = obj.get(key)
        if isinstance(val, str):
            return val.lower()
        if isinstance(val, dict):
            inner = val.get("value") or val.get("name")
            if isinstance(inner, str):
                return inner.lower()
    return ""


async def run(url: str, deadline: float, grace: float, sink: Sink) -> int:
    try:
        import websockets
    except ImportError:
        sink.write(
            "ABORT: the 'websockets' package is not importable in this "
            "interpreter.\n"
            "Use the same interpreter the backend runs under, or install it "
            "with: pip install websockets"
        )
        return 2

    sink.write("=== " + MARKER + " ===")
    sink.write("url      : " + url)
    sink.write("deadline : " + str(deadline) + " s")
    sink.write("started  : " + stamp())
    sink.write("Send a shell_exec prompt in the desktop app now. No rush.")
    sink.write("")

    loop = asyncio.get_event_loop()
    started = loop.time()
    seen_request = False
    seen_resolved = False
    resolved_at = None
    count = 0

    try:
        async with websockets.connect(url, ping_interval=20) as ws:
            sink.write("[" + stamp() + "] CONNECTED")
            while True:
                now = loop.time()
                if now - started > deadline:
                    sink.write("")
                    sink.write("[" + stamp() + "] DEADLINE REACHED")
                    break
                if resolved_at is not None and now - resolved_at > grace:
                    sink.write("")
                    sink.write("[" + stamp() + "] GRACE ELAPSED AFTER RESOLVED")
                    break

                remaining = deadline - (now - started)
                if resolved_at is not None:
                    remaining = min(remaining, grace - (now - resolved_at))
                remaining = max(remaining, 0.1)

                try:
                    raw = await asyncio.wait_for(ws.recv(), timeout=remaining)
                except asyncio.TimeoutError:
                    continue

                count += 1
                try:
                    obj = json.loads(raw)
                except (TypeError, ValueError):
                    sink.write("[" + stamp() + "] FRAME " + str(count) + " NON-JSON")
                    sink.write(repr(raw))
                    continue

                name = event_name(obj)
                sink.write(
                    "[" + stamp() + "] FRAME " + str(count) + "  type=" + (name or "?")
                )
                sink.write(describe(obj))
                sink.write("")

                if WANT_REQUEST in name:
                    seen_request = True
                if WANT_RESOLVED in name:
                    seen_resolved = True
                    resolved_at = loop.time()
                    sink.write(
                        "[" + stamp() + "] *** RESOLVED FRAME CAPTURED - "
                        "closing after " + str(grace) + " s grace ***"
                    )
                    sink.write("")
    except OSError as exc:
        sink.write("ABORT: could not connect to " + url)
        sink.write("  " + repr(exc))
        sink.write("Is the backend up on 8010?")
        return 2
    except Exception as exc:  # noqa: BLE001 - a probe must never mask its own failure
        sink.write("ABORT: unexpected error: " + repr(exc))
        return 2

    sink.write("=== SUMMARY ===")
    sink.write("frames seen        : " + str(count))
    sink.write("confirm_request    : " + ("YES" if seen_request else "NO"))
    sink.write("confirm_resolved   : " + ("YES" if seen_resolved else "NO"))
    sink.write("capture file       : " + sink.path)
    if not count:
        sink.write("")
        sink.write(
            "NOTE: zero frames. Either no turn was sent, or this bus is not the "
            "one the executor publishes to. Zero frames is a finding, not a "
            "failed run - record it."
        )
    return 0 if seen_resolved else 1


def main() -> None:
    ap = argparse.ArgumentParser(description="Capture confirm-gate bus frames.")
    ap.add_argument("--url", default=DEFAULT_URL)
    ap.add_argument("--deadline", type=float, default=600.0)
    ap.add_argument("--grace", type=float, default=5.0)
    args = ap.parse_args()

    sink = Sink(LOGNAME)
    try:
        rc = asyncio.run(run(args.url, args.deadline, args.grace, sink))
    except KeyboardInterrupt:
        sink.write("")
        sink.write("[" + stamp() + "] INTERRUPTED - socket closed cleanly")
        rc = 130
    finally:
        sink.close()
    sys.exit(rc)


if __name__ == "__main__":
    main()
