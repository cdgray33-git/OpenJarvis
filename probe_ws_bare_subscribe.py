"""probe_ws_bare_subscribe.py

BARRIER 2 DELIVERY PROOF - half 1, transport only. Non-interactive, runs to
completion, no human timing dependency.

WHAT IT PROVES
  Connects to /v1/agents/events with a BARE URL (no agent_id query parameter).
  If _agent_filter is falsy on the server, the filter at ws_bridge.py:56-59
  short-circuits and every agent event is forwarded to this client.

POSITIVE CONTROL (required by W13-R1 - this instrument has never produced a
positive reading, so its silence cannot be read as a finding):
  The script asserts it receives SOME event before drawing any conclusion about
  the absence of TOOL_CONFIRM_REQUEST. It generates traffic by hitting
  /v1/chat/completions, which on the non-streaming branch always runs an agent
  (routes.py:162, predicate `agent is not None`, no client opt-out - W17 s3).
  That produces INFERENCE_START / INFERENCE_END / TOOL_CALL_* at minimum.

WHAT IT DOES NOT PROVE
  It does not prove a confirming tool can be reached. There is no direct
  tool-execution route on this server (/v1/tools is GET only), so triggering the
  gate deterministically is a separate problem. If no TOOL_CONFIRM_REQUEST
  arrives, that is EXPECTED and is not a barrier-2 failure.

QUEUE HAZARD
  ws_bridge.py:74-75 drops frames silently on QueueFull, maxsize 100. This
  script counts received frames and warns loudly if it approaches that bound,
  so a drop is never mistaken for a filter rejection.

RUN FROM: repo root, any interpreter that has `websockets` available.
"""

from __future__ import annotations

import asyncio
import json
import sys
import threading
import time
import urllib.error
import urllib.request

HOST = "127.0.0.1"
PORT = 8010
WS_URL = f"ws://{HOST}:{PORT}/v1/agents/events"   # BARE. No agent_id. This is the point.
CHAT_URL = f"http://{HOST}:{PORT}/v1/chat/completions"

LISTEN_SECONDS = 90
QUEUE_MAXSIZE = 100          # must match ws_bridge.py:102
QUEUE_WARN_AT = 80

frames: list[dict] = []
errors: list[str] = []


def trigger_traffic() -> None:
    """Fire a non-streaming chat completion to generate agent events.

    Runs on a worker thread so the socket keeps reading while this blocks.
    Per W17, this takes ~24 s against ollama, so it must not block the reader.
    """
    body = json.dumps({
        "model": "qwen3-coder:30b",
        "stream": False,
        "messages": [{"role": "user", "content": "Reply with the single word OK."}],
    }).encode("utf-8")
    req = urllib.request.Request(
        CHAT_URL, data=body, headers={"Content-Type": "application/json"}, method="POST"
    )
    t0 = time.time()
    try:
        with urllib.request.urlopen(req, timeout=LISTEN_SECONDS) as resp:
            payload = json.loads(resp.read().decode("utf-8"))
        dt = time.time() - t0
        usage = payload.get("usage", {})
        print(f"[trigger] HTTP OK in {dt:.1f}s  usage={usage}")
    except urllib.error.HTTPError as exc:
        errors.append(f"trigger HTTPError {exc.code}")
        print(f"[trigger] HTTP ERROR {exc.code} after {time.time()-t0:.1f}s")
    except Exception as exc:  # noqa: BLE001
        errors.append(f"trigger {type(exc).__name__}")
        print(f"[trigger] FAILED after {time.time()-t0:.1f}s: {type(exc).__name__}: {exc}")


async def run() -> int:
    try:
        import websockets
    except ImportError:
        print("FAIL: the 'websockets' package is not available to this interpreter.")
        print("Install it, or run this with the interpreter that has it.")
        return 2

    print(f"[ws] connecting BARE: {WS_URL}")
    try:
        conn = await asyncio.wait_for(websockets.connect(WS_URL), timeout=15)
    except Exception as exc:  # noqa: BLE001
        print(f"FAIL: could not connect: {type(exc).__name__}: {exc}")
        print("Is the backend running on 8010?")
        return 2

    print("[ws] CONNECTED. Check backend.log for a matching line:")
    print("     ws-accept: peer=... authed=... agent_filter=None")
    print("     agent_filter=None is barrier 2 cleared AT THE MECHANISM.")

    async with conn:
        threading.Thread(target=trigger_traffic, daemon=True).start()

        deadline = time.time() + LISTEN_SECONDS
        while time.time() < deadline:
            remaining = deadline - time.time()
            try:
                raw = await asyncio.wait_for(conn.recv(), timeout=remaining)
            except asyncio.TimeoutError:
                break
            except Exception as exc:  # noqa: BLE001
                errors.append(f"recv {type(exc).__name__}")
                print(f"[ws] recv ended: {type(exc).__name__}: {exc}")
                break

            try:
                evt = json.loads(raw)
            except Exception:  # noqa: BLE001
                print(f"[ws] MALFORMED FRAME: {raw[:200]!r}")
                continue

            frames.append(evt)
            etype = evt.get("type", "?")
            data = evt.get("data", {}) or {}
            aid = data.get("agent_id", "<absent>")
            extra = ""
            if etype.replace("_", ".").startswith("tool.confirm"):
                extra = f"  confirm_id={'PRESENT' if 'confirm_id' in data else 'ABSENT/REDACTED'}"
            print(f"[ws] #{len(frames):<3} {etype:<28} agent_id={aid}{extra}")

            if len(frames) >= QUEUE_WARN_AT:
                print(f"[ws] WARNING: {len(frames)} frames, queue maxsize is "
                      f"{QUEUE_MAXSIZE}. Drops become possible.")

    # ---------------- verdict ----------------
    print("\n" + "=" * 70)
    print(f"FRAMES RECEIVED: {len(frames)}")
    if errors:
        print(f"ERRORS: {errors}")

    if not frames:
        print("POSITIVE CONTROL FAILED - NO FRAMES RECEIVED AT ALL.")
        print("Nothing can be concluded about barrier 2 from this run.")
        print("Check: did the trigger actually run an agent? Is the bus the same")
        print("one ws_bridge subscribed to? (see the two-bus split finding)")
        return 1

    print("POSITIVE CONTROL PASSED - the bare subscription receives events.")
    print("Barrier 2 is CLEARED for delivery: a client with no agent_id filter")
    print("is not dropped by ws_bridge.py:56-59.")

    types = {}
    for f in frames:
        types[f.get("type", "?")] = types.get(f.get("type", "?"), 0) + 1
    print("\nBY TYPE:")
    for t, c in sorted(types.items()):
        print(f"  {c:>4}  {t}")

    ids = {(f.get("data") or {}).get("agent_id") for f in frames}
    print(f"\nDISTINCT agent_id VALUES SEEN: {ids}")
    print("Expect 'native_openhands' on the chat path (W17 section 2.6).")
    print("A managed-agent UI client would filter on a 12-char uuid4 hex and")
    print("would therefore have dropped every one of these frames.")

    confirms = [f for f in frames
                if str(f.get("type", "")).replace("_", ".").startswith("tool.confirm")]
    if confirms:
        print(f"\nCONFIRM EVENTS: {len(confirms)}")
        for c in confirms:
            d = c.get("data") or {}
            print(f"  {c.get('type')}  confirm_id="
                  f"{'PRESENT' if 'confirm_id' in d else 'ABSENT - REDACTED'}")
        print("If confirm_id is ABSENT, ws_bridge.py:61 redacted it because")
        print("_ws_authed is False. OPENJARVIS_WS_TOKEN is likely unset, which")
        print("makes _expected empty and _authed always False. A UI cannot")
        print("answer a confirmation whose confirm_id was stripped.")
    else:
        print("\nNO CONFIRM EVENTS - EXPECTED, NOT A FAILURE.")
        print("Nothing in this run asked for a confirming tool. Reaching the")
        print("gate deterministically is half 2 and is a separate problem:")
        print("there is no direct tool-execution route on this server.")

    return 0


if __name__ == "__main__":
    sys.exit(asyncio.run(run()))

# openjarvis-probe-confirmkey-v1
