# W78 openjarvis-tools-dedupe-v1 verification. Non-interactive. PASS only on structure + disk state.
import os, py_compile, tempfile
root = os.getcwd()
sp = os.path.join(root, "src", "openjarvis", "cli", "serve.py")
py_compile.compile(sp, doraise=True); print("COMPILE OK serve.py")
txt = open(sp, encoding="utf-8").read()
checks = {
    "loop_once": txt.count("for name in ToolRegistry.keys():") == 1,
    "no_channel_loop": txt.count("for _tname in ToolRegistry.keys():") == 0,
    "chat_call_once": txt.count('_build_agent_tools(config, "chat")') == 1,
    "channel_call_once": txt.count('_build_agent_tools(config, "channel")') == 1,
    "channel_assert": "CHANNEL_ASSERT enabled=" in txt,
}
for k, v in checks.items(): print("STRUCT", k, v)
from openjarvis.core.config import load_config, resolve_file_write_dirs
import importlib, sys; importlib.import_module("openjarvis.cli.serve"); s = sys.modules["openjarvis.cli.serve"]  # cli/__init__ shadows the submodule with the click command
cfg = load_config()
dirs = resolve_file_write_dirs(cfg)
chat = s._build_agent_tools(cfg, "chat")
chan = s._build_agent_tools(cfg, "channel")
cn = [type(t).__name__ for t in chat]; hn = [type(t).__name__ for t in chan]
print("CHAT   ", len(cn), cn)
print("CHANNEL", len(hn), hn)
want = sorted(x.strip() for x in str(cfg.agent.tools).split(",") if x.strip())
got = sorted(t.spec.name for t in chan)
same = cn == hn and got == want
print("SAME TOOLKIT AND MATCHES [agent] tools:", same, "count", len(got))
fw = [t for t in chan if t.spec.name == "file_write"]
fwc = [t for t in chat if t.spec.name == "file_write"]
conf = bool(fw) and bool(fwc) and [str(d) for d in fw[0]._allowed_dirs] == dirs and [str(d) for d in fwc[0]._allowed_dirs] == dirs
print("BOTH CONFINED TO", dirs, ":", conf)
inside = os.path.join(dirs[0], "w78_dedupe_probe.txt"); outside = os.path.join(tempfile.gettempdir(), "w78_dedupe_outside.txt")
for p in (inside, outside):
    if os.path.exists(p): os.remove(p)
r1 = fw[0].execute(path=inside, content="w78-channel-inside")
ok1 = r1.success and os.path.isfile(inside) and open(inside, encoding="utf-8").read() == "w78-channel-inside"
r2 = fw[0].execute(path=outside, content="w78-channel-outside")
ok2 = (not r2.success) and ("outside allowed directories" in r2.content) and not os.path.exists(outside)
print("CHANNEL INSIDE  success=%s on_disk=%s" % (r1.success, os.path.isfile(inside)))
print("CHANNEL OUTSIDE success=%s msg=%r on_disk=%s" % (r2.success, r2.content, os.path.exists(outside)))
if os.path.exists(inside): os.remove(inside)
overall = all(checks.values()) and same and conf and ok1 and ok2
print("OVERALL:", "PASS" if overall else "FAIL")
