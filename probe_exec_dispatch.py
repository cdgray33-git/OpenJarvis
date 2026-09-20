from openjarvis.tools import _stubs
from openjarvis.core.registry import ToolRegistry
import openjarvis.tools.mailbox_tools

tool = None
for t in ToolRegistry().all() if hasattr(ToolRegistry(), "all") else []:
    pass

from openjarvis.tools._stubs import ToolCall, ToolExecutor
import openjarvis.tools as T
cands = [o for o in vars(openjarvis.tools.mailbox_tools).values()
         if isinstance(o, type) and o.__name__.endswith("Tool")]
print("candidates:", [c.__name__ for c in cands])
inst = [c() for c in cands if "ListAccounts" in c.__name__]
print("instantiated:", inst)
ex = ToolExecutor(inst)
_stubs.CURRENT_TURN_ID.set("probe-exec-1")
r = ex.execute(ToolCall(id="p1", name=inst[0].spec.name, arguments={}))
print("success:", r.success)
