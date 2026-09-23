import openjarvis, openjarvis.engine
from openjarvis.core.config import JarvisConfig, _apply_toml_section
from openjarvis.engine import _discovery
print("SRC", openjarvis.__file__)
ok = True
c = JarvisConfig()
print("FIELD default", repr(c.engine.disabled))
for k in ("vllm", "ollama"):
    try: _discovery._make_engine(k, c); print("EMPTY LIST construct", k, "PASS")
    except Exception as e: print("EMPTY LIST construct", k, "FAIL", e); ok = False
c.engine.disabled = "vllm, uzu,lemonade"
for k in ("vllm", "uzu", "lemonade"):
    try: _discovery._make_engine(k, c); print("DISABLED", k, "FAIL constructed"); ok = False
    except _discovery.EngineDisabled as e: print("DISABLED", k, "PASS", e)
try: _discovery._make_engine("ollama", c); print("OLLAMA constructs with list set PASS")
except Exception as e: print("OLLAMA FAIL", e); ok = False
keys = [k for k, _ in _discovery.discover_engines(c)]
print("DISCOVER healthy =", keys)
bad = set(keys) & {"vllm", "uzu", "lemonade"}
if bad: print("DISCOVER FAIL", bad); ok = False
if "ollama" not in keys: print("DISCOVER FAIL ollama missing"); ok = False
c2 = JarvisConfig(); _apply_toml_section(c2.engine, {"disabled": ["vllm", "uzu", "lemonade"]})
print("TOML array ->", repr(c2.engine.disabled))
if c2.engine.disabled != "vllm,uzu,lemonade": print("TOML FAIL"); ok = False
print("OVERALL", "PASS" if ok else "FAIL")