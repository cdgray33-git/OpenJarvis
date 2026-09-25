import os, sys, time, shutil, py_compile, hashlib
from pathlib import Path
M = "openjarvis-w83-fwanchor-v1"; R = os.getcwd()
p = os.path.join(R, "src", "openjarvis", "tools", "file_write.py")
t = open(p, "rb").read().decode("utf-8")
if M in t: print("ALREADY PATCHED - no change"); sys.exit(0)
nl = "\r\n" if "\r\n" in t else "\n"
a = "        path = Path(file_path)" + nl
print("ANCHOR count=%d (want 1)" % t.count(a))
if t.count(a) != 1: print("ABORT - nothing written"); sys.exit(1)
t = t.replace(a, a + nl.join([
 "        # " + M + " (W83 G-7): the author resolves a relative path against the server's working directory, so with",
 "        # allowed_dirs set (Graystone W78) every relative name was denied. Anchor it to the first allowed dir;",
 "        # absolute and ~ paths are unchanged and _is_path_allowed still checks the final path.",
 "        if self._allowed_dirs and not path.is_absolute() and not str(file_path).startswith(\"~\"):",
 "            path = self._allowed_dirs[0] / path"]) + nl)
bak = os.path.join(R, "evidence", "W83", "backup", "file_write.py.bak-W83-fwanchor-" + time.strftime("%Y%m%d_%H%M%S"))
shutil.copy2(p, bak); print("BACKUP", bak)
compile(t, p, "exec"); open(p, "wb").write(t.encode("utf-8")); py_compile.compile(p, doraise=True)
print("AFTER sha=%s marker=%d" % (hashlib.sha256(t.encode()).hexdigest().upper()[:16], t.count(M)))
from openjarvis.core.config import load_config, resolve_file_write_dirs
from openjarvis.tools.file_write import FileWriteTool
dirs = resolve_file_write_dirs(load_config()); ws = Path(dirs[0]); fw = FileWriteTool(allowed_dirs=dirs)
def run(label, path, want, **kw):
    r = fw.execute(path=path, content="f7", **kw); print("%s path=%r success=%s PASS=%s msg=%r" % (label, path, r.success, r.success == want, str(r.content)[:90]))
run("T1 relative", "w83_f7.txt", True); print("   T1 in_workspace=%s" % (ws / "w83_f7.txt").exists())
run("T2 absolute ws", str(ws / "w83_f7b.txt"), True)
run("T3 traversal", "..\\w83_f7_escape.txt", False); print("   T3 escaped_file_exists=%s (want False)" % (ws.parent / "w83_f7_escape.txt").exists())
run("T4 absolute outside", os.path.join(R, "w83_f7_out.txt"), False); print("   T4 repo_file_exists=%s (want False)" % Path(R, "w83_f7_out.txt").exists())
run("T5 relative subdir", "sub\\w83_f7.txt", True, create_dirs=True); print("   T5 in_workspace_sub=%s" % (ws / "sub" / "w83_f7.txt").exists())
for q in (ws / "w83_f7.txt", ws / "w83_f7b.txt", ws / "sub" / "w83_f7.txt"):
    if q.exists(): q.unlink()
if (ws / "sub").exists() and not any((ws / "sub").iterdir()): (ws / "sub").rmdir()
