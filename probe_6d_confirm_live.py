"""
6d VERIFICATION PROBE - read-only. No backend, no restart, no writes.

Proves four things about the openjarvis-confirm-live-v1 patch:

  A. The block in cli\\serve.py, executed with the real accepts_tools
     condition true, actually PUTS interactive/confirm_callback into
     agent_kwargs - and does NOT when OPENJARVIS_CONFIRM_INTERACTIVE=0.
  B. A real agent constructed with those kwargs ends up with a
     ToolExecutor whose _interactive is True and _confirm_callback is
     set - and whose tools survived (the serve.py failure mode is a
     silently agent-less server, so tool survival is checked too).
  C. The callback returns True on approved, False on denied, False on
     an unset ContextVar.
  D. TIMING, the load-bearing part. approved/denied must resolve well
     UNDER the TTL. A lower bound alone would also be satisfied by a
     TTL expiry, so the upper bound is what discriminates "resolve()
     released it" from "it timed out and happened to look right."
     Same standard as the 6c gate probe.
"""

import os
import re
import sys
import threading
import time

MARKER = "openjarvis-confirm-live-v1"
TARGET = os.path.join("src", "openjarvis", "cli", "serve.py")

PASS = 0
FAIL = 0


def check(label, ok, detail=""):
    global PASS, FAIL
    if ok:
        PASS += 1
        print("  PASS  %s %s" % (label, detail))
    else:
        FAIL += 1
        print("  FAIL  %s %s" % (label, detail))
    return ok


def extract_block():
    """Pull the inserted block out of serve.py and dedent it to top level."""
    with open(TARGET, "r", encoding="utf-8", newline="") as fh:
        raw = fh.read()
    if MARKER not in raw:
        return None
    lines = [ln.rstrip("\r") for ln in raw.split("\n")]
    start = None
    for i, ln in enumerate(lines):
        if MARKER in ln:
            start = i
            break
    end = None
    for i in range(start, len(lines)):
        if "agent = agent_cls(engine, model_name" in lines[i]:
            end = i
            break
    block = lines[start:end]
    # Drop trailing blank lines, then dedent by the common indent.
    while block and not block[-1].strip():
        block.pop()
    indents = [len(ln) - len(ln.lstrip()) for ln in block if ln.strip()]
    pad = min(indents)
    return "\n".join(ln[pad:] if ln.strip() else "" for ln in block)


def main():
    print("PROBE  :", os.path.abspath(__file__))
    print("TARGET :", os.path.abspath(TARGET))
    print("")

    block = extract_block()
    if block is None:
        print("ABORT: marker not found in", TARGET)
        return 1
    print("Extracted %d lines of patched block." % len(block.split("\n")))
    print("")

    class FakeCls:
        accepts_tools = True

    # --- A. block semantics -------------------------------------------
    print("A. BLOCK SEMANTICS")
    ns = {"agent_cls": FakeCls, "agent_kwargs": {}}
    os.environ.pop("OPENJARVIS_CONFIRM_INTERACTIVE", None)
    exec(compile(block, "<serve-block>", "exec"), ns)
    kw = ns["agent_kwargs"]
    check("default-on sets interactive", kw.get("interactive") is True)
    cb = kw.get("confirm_callback")
    check("default-on sets callback", callable(cb))

    ns2 = {"agent_cls": FakeCls, "agent_kwargs": {}}
    os.environ["OPENJARVIS_CONFIRM_INTERACTIVE"] = "0"
    exec(compile(block, "<serve-block>", "exec"), ns2)
    check("env 0 leaves kwargs clean", ns2["agent_kwargs"] == {},
          str(ns2["agent_kwargs"]))
    os.environ.pop("OPENJARVIS_CONFIRM_INTERACTIVE", None)

    ns3 = {"agent_cls": type("NoTools", (), {"accepts_tools": False}),
           "agent_kwargs": {}}
    exec(compile(block, "<serve-block>", "exec"), ns3)
    check("no-tools agent left alone", ns3["agent_kwargs"] == {})
    print("")

    # --- B. real agent construction ------------------------------------
    print("B. REAL AGENT GETS THE WIRING")
    try:
        import openjarvis.agents  # noqa: F401
        import openjarvis.tools  # noqa: F401
        from openjarvis.core.registry import AgentRegistry, ToolRegistry

        agent_key = None
        for key in AgentRegistry.keys():
            cls = AgentRegistry.get(key)
            if getattr(cls, "accepts_tools", False):
                agent_key = key
                break
        print("  using agent_cls:", agent_key)
        agent_cls = AgentRegistry.get(agent_key)

        tool_cls = ToolRegistry.get("calculator")
        tools = [tool_cls() if isinstance(tool_cls, type) else tool_cls]

        real_kwargs = {
            "bus": None,
            "tools": tools,
            "interactive": kw["interactive"],
            "confirm_callback": kw["confirm_callback"],
        }
        agent = agent_cls(None, "", **real_kwargs)
        ex = getattr(agent, "_executor", None)
        check("agent constructed", agent is not None)
        check("executor exists", ex is not None)
        if ex is not None:
            check("executor._interactive is True",
                  getattr(ex, "_interactive", None) is True)
            check("executor._confirm_callback set",
                  getattr(ex, "_confirm_callback", None) is not None)
            check("tools survived", len(getattr(agent, "_tools", [])) == 1,
                  "n=%d" % len(getattr(agent, "_tools", [])))
    except Exception as exc:
        check("real agent construction", False, repr(exc))
    print("")

    # --- C/D. callback behaviour and timing -----------------------------
    print("C/D. CALLBACK OUTCOMES AND TIMING")
    from openjarvis.core import confirm_registry as cr
    from openjarvis.tools import _stubs as st

    TTL = 4.0

    check("unset ContextVar returns False", cb("no id set") is False)

    for decision, expect in (("approved", True), ("denied", False)):
        cid = cr.register(tool="probe_6d", agent_id="probe_agent",
                          turn_id="probe-6d", ttl=TTL)
        st.CURRENT_CONFIRM_ID.set(cid)
        threading.Timer(0.3, cr.resolve, args=(cid, decision)).start()
        t0 = time.time()
        got = cb("probe prompt")
        dt = time.time() - t0
        check("%s -> %r" % (decision, expect), got is expect)
        check("%s released early" % decision, dt < TTL * 0.5,
              "%.2f s against %.1f s TTL" % (dt, TTL))

    cid = cr.register(tool="probe_6d_to", agent_id="probe_agent",
                      turn_id="probe-6d", ttl=2.0)
    st.CURRENT_CONFIRM_ID.set(cid)
    t0 = time.time()
    got = cb("probe prompt")
    dt = time.time() - t0
    check("timeout -> False", got is False)
    check("timeout waited the TTL out", 1.9 <= dt < 3.5, "%.2f s" % dt)
    st.CURRENT_CONFIRM_ID.set("")
    print("")

    print("RESULT: %d PASS / %d FAIL" % (PASS, FAIL))
    print("VERDICT:", "ALL PROVEN" if FAIL == 0 else "NOT PROVEN - DO NOT PROCEED")
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
