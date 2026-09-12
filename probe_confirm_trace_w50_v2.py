"""probe_confirm_trace_w50_v2.py

W50 - DOES A REGISTERED confirm_id REACH TTL BECAUSE NOBODY ANSWERED?

v2. The v1 asyncio client hung in the opening handshake against a server
that a .NET ClientWebSocket opens in 92 ms, so the fault was the client.
This build uses websockets.sync.client (proven 56 ms in this venv,
websockets 17.0.1, python 3.12.10). NOTE FOR THE REGISTER: the legacy
asyncio client is GONE in 17.x, so probe_ws_bare_subscribe.py cannot run
in this venv either.

Two phases, one invocation, fully non-interactive. Nothing is executed in
either phase: phase A never answers and phase B denies, so the tool body
never runs. Safe against the live backend.

PHASE A - LISTEN ONLY, DO NOT ANSWER
  Reproduces the W49 condition exactly. Socket open BEFORE the trigger,
  fire test-execute, watch the confirm frame arrive, then deliberately
  say nothing. Expect a timeout at ~120 s.

PHASE B - LISTEN AND AUTO-DENY
  Same trigger, POST decision=deny the instant the frame arrives.
  Expect resolution in well under a second.

THE FINDING IS THE CONTRAST, NOT EITHER PHASE ALONE.
  timeout + fast deny   = registry and consumer both work. The W49
                          120.007 s was the no-listener case, which is
                          the DESIGNED outcome. No defect. The open item
                          is the browser half of 6e.
  timeout + slow/failed = the consumer is genuinely broken. Real find.
  no frame at all       = the gate was not reached; this instrument
                          cannot speak to the consumer.

DISCRIMINATOR, PRINTED NOT INFERRED
  test-execute returns turn_id = "test-<run_id>" and the gate emits
  turn_id in the frame. Every frame is matched on that value. Closes the
  08/30 limit where turn_id was never displayed.

RUN FROM: repo root.
"""

from __future__ import annotations

import json
import sys
import time
import urllib.error
import urllib.request

HOST = "127.0.0.1"
PORT = 8010

WS_URL = f"ws://{HOST}:{PORT}/v1/agents/events"          # BARE, no agent_id
EXEC_URL = f"http://{HOST}:{PORT}/v1/tools/test-execute"
CONFIRM_URL = f"http://{HOST}:{PORT}/v1/tools/confirm"

TOOL = "shell_exec"
ARGS = {"command": "echo w50-trace-never-runs"}

PHASE_A_SECONDS = 145.0      # TTL is 120 s; margin for the resolved frame
PHASE_B_SECONDS = 45.0

REQUEST_TYPE = "tool.confirm.request"
RESOLVED_TYPE = "tool.confirm.resolved"


def _norm(etype) -> str:
    return str(etype or "").replace("_", ".")


def _post(url: str, payload: dict, timeout: float):
    """POST json. Returns (status, body_dict_or_text, elapsed_seconds)."""
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url, data=data, headers={"Content-Type": "application/json"}, method="POST"
    )
    t0 = time.time()
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read().decode("utf-8", "replace")
            status = resp.getcode()
    except urllib.error.HTTPError as exc:
        raw = exc.read().decode("utf-8", "replace")
        status = exc.code
    except Exception as exc:  # noqa: BLE001
        return (0, f"{type(exc).__name__}: {exc}", time.time() - t0)
    try:
        body = json.loads(raw)
    except Exception:  # noqa: BLE001
        body = raw
    return (status, body, time.time() - t0)


def phase(name: str, answer: bool, listen_seconds: float) -> dict:
    from websockets.sync.client import connect

    result = {
        "name": name,
        "connected": False,
        "trigger_status": None,
        "turn_id": None,
        "run_id": None,
        "request_at": None,     # trigger -> confirm frame
        "resolved_at": None,    # confirm frame -> resolved frame
        "decision": None,
        "post_status": None,
        "post_ms": None,
        "post_body": None,
        "frame_count": 0,
    }

    print("\n" + "=" * 72)
    print(f"PHASE {name} - {'AUTO-DENY ON ARRIVAL' if answer else 'LISTEN ONLY, NO ANSWER'}")
    print("=" * 72)

    print(f"[ws] connecting BARE: {WS_URL}")
    try:
        conn = connect(WS_URL, open_timeout=15)
    except Exception as exc:  # noqa: BLE001
        print(f"FAIL: could not connect: {type(exc).__name__}: {exc}")
        return result
    result["connected"] = True
    print("[ws] CONNECTED")

    try:
        # Socket is open BEFORE the trigger, so no frame can be missed.
        status, body, dt = _post(EXEC_URL, {"tool": TOOL, "arguments": ARGS}, 20.0)
        result["trigger_status"] = status
        print(f"[trigger] test-execute -> HTTP {status} in {dt*1000:.0f} ms")
        if status != 202:
            print(f"[trigger] BODY: {body}")
            print("ABORT PHASE: no 202, nothing will park on the gate.")
            return result

        result["turn_id"] = body.get("turn_id")
        result["run_id"] = body.get("run_id")
        print(f"[trigger] run_id={result['run_id']}  turn_id={result['turn_id']}")

        t_trigger = time.time()
        t_request = None
        deadline = t_trigger + listen_seconds

        while True:
            remaining = deadline - time.time()
            if remaining <= 0:
                print(f"[ws] listen budget exhausted after {listen_seconds:.0f}s")
                break
            try:
                raw = conn.recv(timeout=remaining)
            except TimeoutError:
                print(f"[ws] listen budget exhausted after {listen_seconds:.0f}s")
                break
            except Exception as exc:  # noqa: BLE001
                print(f"[ws] recv ended: {type(exc).__name__}: {exc}")
                break

            try:
                evt = json.loads(raw)
            except Exception:  # noqa: BLE001
                print(f"[ws] MALFORMED FRAME: {str(raw)[:160]!r}")
                continue

            result["frame_count"] += 1
            etype = _norm(evt.get("type"))
            data = evt.get("data") or {}
            ftid = data.get("turn_id", "")
            elapsed = time.time() - t_trigger
            mine = (ftid == result["turn_id"])

            if mine or etype.startswith("tool.confirm"):
                tag = "MINE" if mine else "other"
                print(f"[ws] +{elapsed:7.3f}s  {etype:<26} "
                      f"turn_id={ftid or '<absent>'} [{tag}]")

            if not mine:
                continue

            if etype == REQUEST_TYPE:
                t_request = time.time()
                result["request_at"] = round(elapsed, 3)
                cid = data.get("confirm_id")
                print(f"[gate] CONFIRM FRAME MATCHED. confirm_id="
                      f"{'PRESENT' if cid else 'ABSENT/REDACTED'}")
                if not answer:
                    print("[gate] PHASE A: deliberately NOT answering. Waiting for TTL.")
                    continue
                if not cid:
                    print("[gate] cannot answer - confirm_id absent from the frame.")
                    continue
                pstatus, pbody, pdt = _post(
                    CONFIRM_URL, {"confirm_id": cid, "decision": "deny"}, 20.0
                )
                result["post_status"] = pstatus
                result["post_ms"] = round(pdt * 1000, 1)
                result["post_body"] = pbody
                print(f"[gate] POST deny -> HTTP {pstatus} in {pdt*1000:.0f} ms")
                print(f"[gate] BODY: {pbody}")

            elif etype == RESOLVED_TYPE:
                result["decision"] = data.get("decision")
                if t_request is not None:
                    result["resolved_at"] = round(time.time() - t_request, 3)
                print(f"[gate] RESOLVED decision={result['decision']} "
                      f"({result['resolved_at']}s after the request frame)")
                break
    finally:
        try:
            conn.close()
        except Exception:  # noqa: BLE001
            pass

    return result


def verdict(a: dict, b: dict) -> int:
    print("\n" + "=" * 72)
    print("VERDICT")
    print("=" * 72)

    if a.get("request_at") is None and b.get("request_at") is None:
        print("NO CONFIRM FRAME IN EITHER PHASE.")
        print(f"Frames seen: A={a.get('frame_count')} B={b.get('frame_count')}")
        print("The gate was not reached, so this run says NOTHING about the")
        print("consumer. If the trigger returned 202, the first suspect is the")
        print("shell_exec argument name failing validation ahead of the gate")
        print("at _stubs.py:265 - NOT the consumer.")
        return 1

    print(f"PHASE A  frame at +{a.get('request_at')}s  "
          f"resolved after {a.get('resolved_at')}s  decision={a.get('decision')}")
    print(f"PHASE B  frame at +{b.get('request_at')}s  "
          f"resolved after {b.get('resolved_at')}s  decision={b.get('decision')}  "
          f"POST {b.get('post_status')} in {b.get('post_ms')} ms")

    a_timeout = a.get("decision") == "timeout" or (
        a.get("resolved_at") is not None and a["resolved_at"] > 100
    )
    b_fast = (
        b.get("post_status") == 200
        and b.get("decision") == "denied"
        and b.get("resolved_at") is not None
        and b["resolved_at"] < 10
    )

    print("")
    if a_timeout and b_fast:
        print("A TIMED OUT WITH NOBODY LISTENING; B RESOLVED IN UNDER A SECOND.")
        print("Registry and consumer both work. The W49 120.007 s was the")
        print("no-listener case - the designed outcome, not a defect. The open")
        print("item is the BROWSER half of 6e, not the route.")
        return 0
    if a_timeout and not b_fast:
        print("A TIMED OUT AND B DID NOT RESOLVE CLEANLY.")
        print("This is the real break. The POST status and body above are the")
        print("evidence - carry them verbatim.")
        return 1
    print("UNEXPECTED SHAPE - do not summarise. Read the two phase lines above.")
    print("Neither the clean-pass nor the clean-fail pattern was produced.")
    return 1


def main() -> int:
    try:
        import websockets.sync.client  # noqa: F401
    except ImportError:
        print("FAIL: websockets.sync.client unavailable (needs websockets >= 13).")
        return 2

    print("W50 CONFIRM GATE TRACE v2 (sync client)")
    print(f"tool={TOOL}  (never executes: phase A never answers, phase B denies)")
    print(f"phase A budget {PHASE_A_SECONDS:.0f}s, phase B budget {PHASE_B_SECONDS:.0f}s")

    a = phase("A", answer=False, listen_seconds=PHASE_A_SECONDS)
    if not a["connected"]:
        return 2
    print("\n[wait] 3 s between phases so they cannot overlap on the bus.")
    time.sleep(3)
    b = phase("B", answer=True, listen_seconds=PHASE_B_SECONDS)

    return verdict(a, b)


if __name__ == "__main__":
    sys.exit(main())

# openjarvis-confirm-trace-w50-v2
