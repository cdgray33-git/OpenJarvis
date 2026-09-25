import os, sys, time, shutil, py_compile, hashlib
from pathlib import Path
M = "openjarvis-w83-codecwd-v1"; R = os.getcwd()
p = os.path.join(R, "src", "openjarvis", "tools", "code_interpreter.py")
t = open(p, "rb").read().decode("utf-8")
if M in t: print("ALREADY PATCHED - no change"); sys.exit(0)
nl = "\r\n" if "\r\n" in t else "\n"
a = nl.join(["                [sys.executable, \"-c\", code],", "                capture_output=True,", "                text=True,", "                timeout=self._timeout,", "            )"])
b = nl.join(["                [sys.executable, \"-c\", code],", "                capture_output=True,", "                text=True,", "                timeout=self._timeout,", "                cwd=_oj_workdir(),  # " + M, "            )"])
h = nl.join(["", "", "# " + M + " (W83 G-2): author runs the subprocess with no cwd, so relative saves (a .docx, a .pptx) land",
             "# wherever the server started - usually the repo root. Use the same folder file_write is confined to.",
             "def _oj_workdir():",
             "    try:",
             "        from openjarvis.core.config import load_config, resolve_file_write_dirs",
             "        d = resolve_file_write_dirs(load_config())[0]",
             "    except Exception:",
             "        d = str(Path.home() / \".openjarvis\" / \"workspace\")",
             "    Path(d).mkdir(parents=True, exist_ok=True)",
             "    return d", ""])
print("ANCHOR count=%d (want 1)" % t.count(a))
if t.count(a) != 1: print("ABORT - nothing written"); sys.exit(1)
t = t.replace(a, b)
if "from pathlib import Path" not in t: t = t.replace("import subprocess" + nl, "import subprocess" + nl + "from pathlib import Path" + nl, 1)
t = t.replace(nl + nl + "__all__", h + nl + "__all__", 1)
bak = os.path.join(R, "evidence", "W83", "backup", "code_interpreter.py.bak-W83-codecwd-" + time.strftime("%Y%m%d_%H%M%S"))
shutil.copy2(p, bak); print("BACKUP", bak)
compile(t, p, "exec"); open(p, "wb").write(t.encode("utf-8")); py_compile.compile(p, doraise=True)
print("AFTER sha=%s marker=%d" % (hashlib.sha256(t.encode()).hexdigest().upper()[:16], t.count(M)))
from openjarvis.tools.code_interpreter import CodeInterpreterTool, _oj_workdir
wd = Path(_oj_workdir()).resolve()
r = CodeInterpreterTool().execute(code="from pathlib import Path\nprint(Path.cwd())\nfrom docx import Document\nd = Document()\nd.add_paragraph('s2 cwd test')\nd.save('w83_s2_test.docx')\nprint('SAVED')")
print("T1 success=%s cwd_reported=%r workspace=%r PASS=%s" % (r.success, r.content.splitlines()[0] if r.content else "", str(wd), bool(r.content) and Path(r.content.splitlines()[0]).resolve() == wd))
f = wd / "w83_s2_test.docx"
print("T2 file_in_workspace=%s" % f.exists())
print("T3 file_in_repo_root=%s (want False)" % (Path(R) / "w83_s2_test.docx").exists())
if f.exists(): f.unlink()
