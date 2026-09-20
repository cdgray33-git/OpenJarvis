"""probe_confirm_emit.py - Defect 6 / 6c STEP 3 acceptance probe

Read-only against the repo. Touches no backend, needs no restart, needs no 6d.
Builds a ToolExecutor directly with interactive=True and a real blocking
waiter, the same pattern that proved the dispatch instrument on 08/17.

Proves, per the agreed definition of "6c satisfied":
  1. the TOOL_CONFIRM_REQUEST event fires at all
  2. the payload carries all seven fields, with agent_id INSIDE data
  3. the callback blocks the worker and resolve() releases it
  4. approved / denied / timeout each produce a DISTINCT ToolResult
  5. the 409 body shape (attempted in-process; SKIPs loudly if the router
     cannot be constructed here, and prints its signature so the next
     window can finish it in one step)

Run from the repo root with the venv python.
"""

import inspect
import json
import os
import sys
import threading
import time

# Short TTL so the timeout case does not take two minutes. Set BEFORE import
# because default_ttl() reads the environment.
os.environ["OPENJARVIS_CONFIRM_TTL"] = "4"

sys.path.insert(0, os.path.join(os.getcwd(), "src"))

from openjarvis.core import confirm_registry as cr          # noqa: E402
from openjarvis.core.events import EventBus, EventType      # noqa: E402
from openjarvis.core.types import ToolCall                  # noqa: E402
from openjarvis.tools import _stubs                         # noqa: E402
from openjarvis.tools._stubs import ToolExecutor            # noqa: E402

RESULTS = []
SEVEN = ["confirm_id", "agent_id", "turn_id", "tool",
         "args_digest", "prompt", "expires_at"]


def check(name, ok, detail=""):
    RESULTS.append((name, bool(ok), detail))
    print("  %-52s %s%s" % (name, "PASS" if ok else "FAIL",
                            ("  " + detail) if detail else ""))


def banner(text):
    print("")
    print("=" * 70)
    print(text)
    print("=" * 70)


# ---------------------------------------------------------------------------
# Preflight - the patch is on disk and importable
# ---------------------------------------------------------------------------
banner("PREFLIGHT")
check("CURRENT_CONFIRM_ID exists on the module",
      hasattr(_stubs, "CURRENT_CONFIRM_ID"))
check("confirm_registry imports", hasattr(cr, "register") and hasattr(cr, "wait"))
check("EventType.TOOL_CONFIRM_REQUEST exists",
      hasattr(EventType, "TOOL_CONFIRM_REQUEST"))
print("  ToolExecutor signature : %s" % (inspect.signature(ToolExecutor.__init__),))
print("  EventBus.subscribe sig : %s" % (inspect.signature(EventBus.subscribe),))
print("  cr.register signature  : %s" % (inspect.signature(cr.register),))


# ---------------------------------------------------------------------------
# Build a confirm-required tool out of a real, harmless, read-only tool
# ---------------------------------------------------------------------------
banner("FIXTURE")
from openjarvis.tools.mailbox_tools import MailboxListAccountsTool  # noqa: E402

_base = MailboxListAccountsTool()
_spec = _base.spec
try:
    _spec.requires_confirmation = True
    _how = "mutated in place"
except Exception:
    import dataclasses
    _spec = dataclasses.replace(_spec, requires_confirmation=True)
    _how = "dataclasses.replace"


class ConfirmTool(MailboxListAccountsTool):
    @property
    def spec(self):
        return _spec


TOOL = ConfirmTool()
check("fixture tool requires_confirmation is True",
      TOOL.spec.requires_confirmation is True, _how)
check("fixture tool name matches the base tool",
      TOOL.spec.name == _base.spec.name, TOOL.spec.name)


def subscribe(bus, handler):
    """EventBus.subscribe signature is not assumed - try the plausible forms."""
    try:
        bus.subscribe(handler)
        return "subscribe(handler)"
    except TypeError:
        pass
    try:
        bus.subscribe(EventType.TOOL_CONFIRM_REQUEST, handler)
        return "subscribe(event_type, handler)"
    except TypeError:
        pass
    bus.subscribe("*", handler)
    return "subscribe('*', handler)"


def run_case(label, decide, delay=0.3):
    """decide: 'approve', 'deny', or None to let it time out."""
    captured = []
    bus = EventBus()

    def on_event(*args):
        # Handler shape is not assumed either - find the Event in the args.
        for a in args:
            et = getattr(a, "event_type", None)
            if et is not None:
                captured.append(a)
        return None

    how = subscribe(bus, on_event)

    timings = {}

    def waiter(prompt):
        cid = _stubs.CURRENT_CONFIRM_ID.get()
        timings["cid_seen_by_callback"] = cid
        timings["wait_start"] = time.time()
        decision = cr.wait(cid)
        timings["wait_end"] = time.time()
        timings["decision"] = decision
        return decision == cr.APPROVED

    ex = ToolExecutor([TOOL], bus, interactive=True,
                      confirm_callback=waiter, agent_id="probe_agent")

    def resolver():
        deadline = time.time() + 3.0
        while time.time() < deadline:
            if captured:
                ev = captured[0]
                cid = (ev.data or {}).get("confirm_id")
                if cid:
                    time.sleep(delay)
                    try:
                        timings["resolve_returned"] = cr.resolve(cid, decide)
                        timings["second_resolve"] = cr.resolve(cid, decide)
                    except Exception as exc:
                        timings["resolver_error"] = repr(exc)
                    return
            time.sleep(0.02)

    if decide is not None:
        t = threading.Thread(target=resolver, daemon=True)
        t.start()

    _stubs.CURRENT_TURN_ID.set("probe-t1")
    t0 = time.time()
    result = ex.execute(ToolCall(id="probe-1", name=TOOL.spec.name, arguments="{}"))
    elapsed = time.time() - t0

    return {
        "label": label,
        "captured": captured,
        "subscribe_form": how,
        "result": result,
        "elapsed": elapsed,
        "timings": timings,
    }


# ---------------------------------------------------------------------------
# CASE 1 - APPROVED
# ---------------------------------------------------------------------------
banner("CASE 1 - APPROVED")
c1 = run_case("approved", cr.APPROVED, delay=0.4)
print("  subscribe form  : %s" % c1["subscribe_form"])
print("  events captured : %d" % len(c1["captured"]))
check("1.1 an event fired", len(c1["captured"]) >= 1)

ev = c1["captured"][0] if c1["captured"] else None
if ev is not None:
    print("  event_type      : %s" % (ev.event_type,))
    print("  data keys       : %s" % sorted((ev.data or {}).keys()))
    check("1.2 event_type is TOOL_CONFIRM_REQUEST",
          ev.event_type == EventType.TOOL_CONFIRM_REQUEST)
    data = ev.data or {}
    missing = [f for f in SEVEN if f not in data]
    check("1.3 all seven payload fields present", not missing,
          "missing=%s" % missing if missing else "")
    check("1.4 agent_id is INSIDE data and non-empty",
          bool(data.get("agent_id")), repr(data.get("agent_id")))
    check("1.5 turn_id carried", data.get("turn_id") == "probe-t1",
          repr(data.get("turn_id")))
    check("1.6 args_digest is bounded (<=400)",
          len(str(data.get("args_digest", ""))) <= 400)
    check("1.7 prompt does NOT contain a raw dict repr",
          "with args {'" not in str(data.get("prompt", "")))
    check("1.8 expires_at is in the future at emit time",
          isinstance(data.get("expires_at"), (int, float))
          and data["expires_at"] > time.time() - 1)
    check("1.9 confirm_id reached the callback via the ContextVar",
          c1["timings"].get("cid_seen_by_callback") == data.get("confirm_id"),
          repr(c1["timings"].get("cid_seen_by_callback")))

if c1["timings"].get("resolver_error"):
    print("  resolver error  : %s" % c1["timings"]["resolver_error"])
check("1.10 callback BLOCKED until resolve()",
      c1["elapsed"] >= 0.35, "elapsed=%.2fs" % c1["elapsed"])
check("1.10b RELEASED BY resolve(), not by the TTL expiring",
      c1["elapsed"] < 2.5, "elapsed=%.2fs vs TTL 4s" % c1["elapsed"])
check("1.11 wait() returned APPROVED",
      c1["timings"].get("decision") == cr.APPROVED,
      repr(c1["timings"].get("decision")))
check("1.12 first resolve() returned True",
      c1["timings"].get("resolve_returned") is True)
check("1.13 second resolve() returned False (write-once)",
      c1["timings"].get("second_resolve") is False)
r1 = c1["result"]
print("  ToolResult      : success=%s content=%r" % (r1.success, str(r1.content)[:110]))
check("1.14 APPROVED case actually EXECUTED the tool",
      "denied" not in str(r1.content).lower()
      and "TIMEOUT" not in str(r1.content))


# ---------------------------------------------------------------------------
# CASE 2 - DENIED
# ---------------------------------------------------------------------------
banner("CASE 2 - DENIED")
c2 = run_case("denied", cr.DENIED, delay=0.4)
r2 = c2["result"]
print("  ToolResult      : success=%s content=%r" % (r2.success, str(r2.content)[:110]))
if c2["timings"].get("resolver_error"):
    print("  resolver error  : %s" % c2["timings"]["resolver_error"])
check("2.1 an event fired", len(c2["captured"]) >= 1)
check("2.1b released by resolve(), not the TTL",
      c2["elapsed"] < 2.5, "elapsed=%.2fs vs TTL 4s" % c2["elapsed"])
check("2.2 wait() returned DENIED",
      c2["timings"].get("decision") == cr.DENIED,
      repr(c2["timings"].get("decision")))
check("2.3 success is False", r2.success is False)
check("2.4 content says denied by user", "denied by user" in str(r2.content).lower())
check("2.5 content does NOT claim a timeout", "TIMEOUT" not in str(r2.content))


# ---------------------------------------------------------------------------
# CASE 3 - TIMEOUT (nobody answers)
# ---------------------------------------------------------------------------
banner("CASE 3 - TIMEOUT (TTL 4s, nobody answers)")
c3 = run_case("timeout", None)
r3 = c3["result"]
print("  elapsed         : %.2fs" % c3["elapsed"])
print("  ToolResult      : success=%s content=%r" % (r3.success, str(r3.content)[:160]))
check("3.1 an event fired", len(c3["captured"]) >= 1)
check("3.2 wait() returned TIMEOUT",
      c3["timings"].get("decision") == cr.TIMEOUT,
      repr(c3["timings"].get("decision")))
check("3.3 it actually waited out the TTL", c3["elapsed"] >= 3.0,
      "elapsed=%.2fs" % c3["elapsed"])
check("3.4 success is False", r3.success is False)
check("3.5 content names it a TIMEOUT", "TIMEOUT" in str(r3.content))
check("3.6 content explicitly says NOT a refusal",
      "not a refusal" in str(r3.content).lower())
check("3.7 content does NOT say denied by user",
      "denied by user" not in str(r3.content).lower())


# ---------------------------------------------------------------------------
# CASE 4 - the three ToolResults are DISTINCT
# ---------------------------------------------------------------------------
banner("CASE 4 - DISTINCTNESS")
bodies = [str(r1.content), str(r2.content), str(r3.content)]
check("4.1 approved / denied / timeout contents are all different",
      len(set(bodies)) == 3)
for lbl, b in zip(["approved", "denied ", "timeout"], bodies):
    print("  %s : %s" % (lbl, b[:100]))


# ---------------------------------------------------------------------------
# CASE 5 - 409 body shape, in-process via the real router
# ---------------------------------------------------------------------------
banner("CASE 5 - 409 BODY SHAPE")
try:
    from fastapi import FastAPI
    from fastapi.testclient import TestClient
    from openjarvis.server import agent_manager_routes as amr

    sig = inspect.signature(amr.create_agent_manager_router)
    print("  create_agent_manager_router%s" % (sig,))
    from unittest.mock import MagicMock
    routers = amr.create_agent_manager_router(MagicMock())
    if not isinstance(routers, (list, tuple)):
        routers = [routers]
    print("  routers returned: %d" % len(routers))
    app = FastAPI()
    for r in routers:
        app.include_router(r)
    client = TestClient(app)

    cid = cr.register(tool="probe_409", agent_id="probe_agent", turn_id="probe-t1")
    a = client.post("/v1/tools/confirm", json={"confirm_id": cid, "decision": "approve"})
    b = client.post("/v1/tools/confirm", json={"confirm_id": cid, "decision": "deny"})
    print("  first  : %s %s" % (a.status_code, a.text[:220]))
    print("  second : %s %s" % (b.status_code, b.text[:220]))
    check("5.1 first resolve returns 200", a.status_code == 200)
    check("5.2 second resolve returns 409", b.status_code == 409)
    try:
        body = b.json()
    except Exception:
        body = {}
    check("5.3 409 body carries the RECORDED decision (approved)",
          "approved" in json.dumps(body), json.dumps(body)[:160])
    check("5.4 409 body did NOT flip to the second request's decision",
          json.dumps(body).count("denied") == 0, json.dumps(body)[:160])
except Exception as exc:
    print("  SKIP - could not exercise the route in-process: %r" % (exc,))
    print("  This is the ONLY criterion not proven by this run.")
    RESULTS.append(("5.x 409 body shape", None, "SKIPPED: %r" % (exc,)))


# ---------------------------------------------------------------------------
banner("SUMMARY")
passed = [n for n, ok, _ in RESULTS if ok is True]
failed = [n for n, ok, _ in RESULTS if ok is False]
skipped = [n for n, ok, _ in RESULTS if ok is None]
print("  PASS %d / FAIL %d / SKIP %d" % (len(passed), len(failed), len(skipped)))
for n, ok, d in RESULTS:
    if ok is False:
        print("  FAILED: %s  %s" % (n, d))
for n, ok, d in RESULTS:
    if ok is None:
        print("  SKIPPED: %s  %s" % (n, d))
print("")
print("VERDICT: " + ("ALL PROVEN" if not failed and not skipped else
                     ("PROVEN EXCEPT SKIPS" if not failed else "FAILURES PRESENT")))
