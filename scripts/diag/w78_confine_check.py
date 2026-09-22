# W78 openjarvis-file-confine-v1 verification. Non-interactive. PASS only on disk state.
import os, py_compile, sys, tempfile
root = os.getcwd()
for rel in ("src/openjarvis/core/config.py", "src/openjarvis/cli/ask.py", "src/openjarvis/cli/serve.py"):
    py_compile.compile(os.path.join(root, rel), doraise=True)
    print("COMPILE OK", rel)
import openjarvis
print("IMPORT FROM", openjarvis.__file__)
from openjarvis.core.config import load_config, resolve_file_write_dirs
import openjarvis.tools  # noqa: F401
from openjarvis.cli.ask import _build_tools
cfg = load_config()
dirs = resolve_file_write_dirs(cfg)
print("RESOLVED DIRS", dirs, "EXISTS", [os.path.isdir(d) for d in dirs])
t = _build_tools(["file_write"], cfg, None, "m")[0]
print("TOOL", type(t).__name__, "ALLOWED", [str(d) for d in t._allowed_dirs])
inside = os.path.join(dirs[0], "w78_confine_probe.txt")
outside = os.path.join(tempfile.gettempdir(), "w78_confine_outside.txt")
for p in (inside, outside):
    if os.path.exists(p):
        os.remove(p)
r1 = t.execute(path=inside, content="w78-inside")
ok1 = r1.success and os.path.isfile(inside) and open(inside, encoding="utf-8").read() == "w78-inside"
print("INSIDE  success=%s content=%r on_disk=%s" % (r1.success, r1.content, os.path.isfile(inside)))
r2 = t.execute(path=outside, content="w78-outside")
ok2 = (not r2.success) and ("outside allowed directories" in r2.content) and not os.path.exists(outside)
print("OUTSIDE success=%s content=%r on_disk=%s" % (r2.success, r2.content, os.path.exists(outside)))
if os.path.exists(inside):
    os.remove(inside)
print("RESULT INSIDE:", "PASS" if ok1 else "FAIL")
print("RESULT OUTSIDE:", "PASS" if ok2 else "FAIL")
print("OVERALL:", "PASS" if (ok1 and ok2 and dirs) else "FAIL")
