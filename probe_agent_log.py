import os
LOGDIR = os.path.join(os.environ.get("LOCALAPPDATA", os.path.expanduser("~")), "OpenJarvis", "logs")
AGENT = os.path.join(LOGDIR, "agent.log")
DISP  = os.path.join(LOGDIR, "dispatch.log")

def size(p):
    try: return os.path.getsize(p)
    except OSError: return -1

def tail(p, n=10):
    try:
        with open(p, "r", encoding="utf-8", errors="replace") as f:
            return [l.rstrip("\n") for l in f.readlines()[-n:]]
    except OSError:
        return []

a0, d0 = size(AGENT), size(DISP)
print("BEFORE  agent.log=%d  dispatch.log=%d" % (a0, d0))

import openjarvis.agents.native_openhands as noh
from openjarvis.tools import _stubs

fails = []

class StubAgent:
    _tools = [1, 2, 3]
    _max_turns = 15
    _model = "probe-model"

class StubCtx:
    conversation_id = "probe-conv-1"

run_id = noh._oj_run_start(StubAgent(), StubCtx(), "probe input text")
print("run_id=%r" % (run_id,))
if not run_id:
    fails.append("_oj_run_start returned no run id")

turn_id = noh._oj_set_turn(run_id, 1)
got = _stubs.CURRENT_TURN_ID.get()
print("turn_id=%r  contextvar=%r" % (turn_id, got))
if got != turn_id:
    fails.append("ACCEPT 3: CURRENT_TURN_ID is %r, expected %r" % (got, turn_id))

noh._oj_run_end(run_id, "final", 1, [], "probe final answer text")

from openjarvis.tools.mailbox_tools import MailboxListAccountsTool
ex = _stubs.ToolExecutor([MailboxListAccountsTool()])
res = ex.execute(_stubs.ToolCall(id="probe-call-1", name="mailbox_list_accounts", arguments={}))
print("tool success=%r" % (getattr(res, "success", None),))

a1, d1 = size(AGENT), size(DISP)
print("AFTER   agent.log=%d (delta %d)  dispatch.log=%d (delta %d)" % (a1, a1 - a0, d1, d1 - d0))

at = tail(AGENT)
dt = tail(DISP)
print("--- agent.log tail ---")
for l in at: print(l)
print("--- dispatch.log tail ---")
for l in dt: print(l)

if a1 <= 0 or a1 <= a0:
    fails.append("ACCEPT 1: agent.log did not grow")
for kind in ("RUNSTART", "TURN", "RUNEND"):
    if not any(kind in l and ("run=%s" % run_id) in l for l in at):
        fails.append("ACCEPT 2: no %s line with run=%s" % (kind, run_id))
new_d = [l for l in dt if "probe-call-1" in l or "mailbox_list_accounts" in l]
if not new_d:
    fails.append("ACCEPT 4: no new dispatch lines found")
for l in new_d:
    if ("turn=%s" % turn_id) not in l:
        fails.append("ACCEPT 4: dispatch line does not carry turn=%s -> %s" % (turn_id, l))

print()
print("VERDICT: PASS" if not fails else "VERDICT: FAIL")
for f in fails: print("  " + f)
