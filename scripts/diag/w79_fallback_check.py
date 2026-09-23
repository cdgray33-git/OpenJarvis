import openjarvis.engine
from openjarvis.core.config import load_config
from openjarvis.engine import _discovery
c = load_config()
print("LOADED disabled =", repr(c.engine.disabled), "ollama.host =", repr(c.engine.ollama.host))
ok = True
exp = {"vllm", "uzu", "lemonade", "litellm"}
if {k.strip() for k in c.engine.disabled.split(",") if k.strip()} != exp: print("CONFIG FAIL"); ok = False
r = _discovery.get_engine(c)
print("NORMAL get_engine ->", r[0] if r else None, getattr(r[1], "_host", None) if r else None)
if not r or r[0] != "ollama": print("NORMAL FAIL"); ok = False
c.engine.ollama.host = "http://127.0.0.1:9"
r = _discovery.get_engine(c)
print("OUTAGE with list ->", r[0] if r else None, getattr(r[1], "_host", None) if r else None)
if r is not None: print("OUTAGE FAIL: fell back to", r[0]); ok = False
c.engine.disabled = ""
r = _discovery.get_engine(c)
print("CONTROL outage, list emptied ->", r[0] if r else None, getattr(r[1], "_host", None) if r else None)
print("OVERALL", "PASS" if ok else "FAIL")