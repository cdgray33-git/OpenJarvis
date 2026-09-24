import sys, json
from openjarvis.tools.storage.sqlite import SQLiteMemory
from openjarvis.tools.storage.context import ContextConfig, inject_context
from openjarvis.core.types import Message, Role
from openjarvis.core.events import EventType, get_event_bus
seen = []
try:
    get_event_bus().subscribe(EventType.MEMORY_RETRIEVE, lambda e: seen.append(getattr(e, "data", e)))
    print("BUS subscribe OK")
except Exception as exc:
    print("BUS subscribe FAIL", type(exc).__name__, exc)
m = SQLiteMemory()
print("DB", m._db_path, "count", m.count())
Q = "What do my notes say about email? One sentence."
for q in (Q, "email", "notes email"):
    r = m.retrieve(q, top_k=10)
    print("RAW q=%r hits=%d scores=%s" % (q, len(r), [round(x.score, 3) for x in r]))
msgs = [Message(role=Role.USER, content=Q)]
for ms in (20.0, 0.0):
    seen.clear()
    out = inject_context(Q, msgs, m, config=ContextConfig(top_k=3, min_score=ms, max_context_tokens=1200))
    inj = [s for s in seen if isinstance(s, dict) and s.get("context_injection")]
    print("INJECT min_score=%s in=%d out=%d injected=%s events=%d inj_event=%s" % (ms, len(msgs), len(out), len(out) > len(msgs), len(seen), json.dumps(inj)[:200]))
