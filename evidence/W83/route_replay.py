import traceback
Q = "What do my notes say about email? One sentence."
def step(name, fn):
    try:
        v = fn(); print("OK  ", name, "->", (repr(v)[:160] if v is not None else "")); return v
    except Exception:
        print("FAIL", name); traceback.print_exc(); return None
from openjarvis.core.config import load_config
cfg = step("load_config", load_config)
step("memory cfg", lambda: (cfg.memory.default_backend, cfg.memory.db_path, cfg.memory.context_top_k, cfg.memory.context_min_score, cfg.memory.context_max_tokens, cfg.agent.context_from_memory))
import openjarvis.tools.storage
from openjarvis.core.registry import MemoryRegistry
be = step("backend create", lambda: MemoryRegistry.create(cfg.memory.default_backend, db_path=cfg.memory.db_path))
step("backend count", lambda: be.count())
from openjarvis.server.models import ChatMessage, ChatCompletionRequest
req = step("request model", lambda: ChatCompletionRequest(model="qwen3-coder:30b", messages=[ChatMessage(role="user", content=Q)], stream=False, max_tokens=64))
from openjarvis.server.routes import _to_messages
from openjarvis.tools.storage.context import ContextConfig, inject_context
msgs = step("_to_messages", lambda: _to_messages(req.messages))
ctx_cfg = step("ContextConfig", lambda: ContextConfig(top_k=cfg.memory.context_top_k, min_score=cfg.memory.context_min_score, max_context_tokens=cfg.memory.context_max_tokens))
enr = step("inject_context", lambda: inject_context(Q, msgs, be, config=ctx_cfg))
if enr is not None:
    print("LEN in=%d out=%d" % (len(msgs), len(enr)))
    new = step("ChatMessage rebuild", lambda: [ChatMessage(role=m.role.value, content=m.content, name=m.name, tool_call_id=getattr(m, "tool_call_id", None)) for m in enr])
    if new:
        req.messages = new
        prior = step("_handle_agent prior", lambda: _to_messages(req.messages[:-1]))
        if prior: print("PRIOR roles=%s chars=%s" % ([p.role.value for p in prior], [len(p.content) for p in prior]))
