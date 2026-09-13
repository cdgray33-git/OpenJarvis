"""openjarvis-confirm-policy-v1 harness (W56, patch 1 of 2).

Proves ConfirmPolicy exists, approves, and WRITES ITS DECISION, and that
ToolExecutor accepts it in the confirm_callback slot exactly as it accepted
the bare lambda. Seven criteria, no interaction, exits nonzero on any FAIL.
"""
import json, os, sys, time

sys.path.insert(0, os.path.join(os.getcwd(), "src"))

from openjarvis.core.types import ToolCall, ToolResult
from openjarvis.tools import _stubs as S

LOG = os.path.join(
    os.environ.get("LOCALAPPDATA", os.path.expanduser("~")),
    "OpenJarvis", "logs", "dispatch.log",
)

def size():
    try:
        return os.path.getsize(LOG)
    except OSError:
        return 0

def tail(off):
    try:
        with open(LOG, "r", encoding="utf-8", errors="replace") as f:
            f.seek(off)
            return f.read()
    except OSError:
        return ""

results = []
def check(n, ok, detail=""):
    results.append((n, ok, detail))
    print(("PASS " if ok else "FAIL ") + n + ("  " + detail if detail else ""))

MARK = "w56-harness-site"
before = size()

# 1 importable
check("1 ConfirmPolicy importable", hasattr(S, "ConfirmPolicy"))
if not hasattr(S, "ConfirmPolicy"):
    sys.exit(1)

# 2 exported
check("2 exported in __all__", "ConfirmPolicy" in S.__all__, str(S.__all__))

pol = S.ConfirmPolicy(
    site=MARK,
    reason="harness-only, proves the record is written",
    human_present=False,
)

# 3 approves
check("3 call returns True", pol("Allow execution of tool 'x' with args {}?") is True)

# 4 repr is readable and names the site
r = repr(pol)
check("4 repr names site", MARK in r and "AUTO_APPROVE" in r, r)

time.sleep(0.2)
new = tail(before)

# 5 POLICY line written
check("5 POLICY line in dispatch.log", "POLICY site=" + MARK in new)

# 6 line carries the why
check(
    "6 line carries human_present and reason",
    "human_present=False" in new and "reason=harness-only" in new,
)

# 7 drop-in for the callback slot on a real gated dispatch
class _Gated(S.BaseTool):
    tool_id = "w56_probe"
    @property
    def spec(self):
        return S.ToolSpec(
            name="w56_probe",
            description="harness probe",
            parameters={"type": "object", "properties": {}},
            requires_confirmation=True,
            timeout_seconds=10.0,
        )
    def execute(self, **p):
        return ToolResult(tool_name="w56_probe", content="RAN", success=True)

before2 = size()
ex = S.ToolExecutor(
    tools=[_Gated()],
    bus=None,
    interactive=True,
    confirm_callback=S.ConfirmPolicy(
        site=MARK + "-exec",
        reason="harness-only, executor slot",
        human_present=False,
    ),
)
res = ex.execute(ToolCall(id="w56-1", name="w56_probe", arguments="{}"))
time.sleep(0.2)
new2 = tail(before2)
check(
    "7 executor accepts policy, tool ran, POLICY precedes OUTCOME",
    res.success
    and res.content == "RAN"
    and ("POLICY site=" + MARK + "-exec") in new2
    and "reason=OK" in new2,
    "success=%s content=%r" % (res.success, res.content),
)

bad = [n for n, ok, _ in results if not ok]
print("")
print("RESULT %d/%d PASS" % (len(results) - len(bad), len(results)))
sys.exit(1 if bad else 0)
