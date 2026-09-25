import os, sys, time, shutil, py_compile, hashlib
from pathlib import Path
M = "openjarvis-w83-fwoffice-v1"; R = os.getcwd()
p = os.path.join(R, "src", "openjarvis", "tools", "file_write.py")
t = open(p, "rb").read().decode("utf-8")
if M in t: print("ALREADY PATCHED - no change"); sys.exit(0)
nl = "\r\n" if "\r\n" in t else "\n"
a = "            path = self._allowed_dirs[0] / path" + nl
print("ANCHOR count=%d (want 1)" % t.count(a))
if t.count(a) != 1: print("ABORT - nothing written"); sys.exit(1)
t = t.replace(a, a + nl.join([
 "        # " + M + " (W83 F-11, owner): writing plain text into an Office file name produced files Office cannot open,",
 "        # and the model then claimed it had created a document. Refuse and steer to the right tool.",
 "        if path.suffix.lower() in (\".docx\", \".pptx\", \".xlsx\"):",
 "            return ToolResult(",
 "                tool_name=\"file_write\",",
 "                content=(",
 "                    f\"file_write writes plain text only and cannot create a real {path.suffix.lower()} file. \"",
 "                    \"To create Word, PowerPoint or Excel files use the code_interpreter tool with python-docx, \"",
 "                    \"python-pptx or openpyxl and save with a plain filename.\"",
 "                ),",
 "                success=False,",
 "            )"]) + nl)
bak = os.path.join(R, "evidence", "W83", "backup", "file_write.py.bak-W83-fwoffice-" + time.strftime("%Y%m%d_%H%M%S"))
shutil.copy2(p, bak); print("BACKUP", bak)
compile(t, p, "exec"); open(p, "wb").write(t.encode("utf-8")); py_compile.compile(p, doraise=True)
print("AFTER sha=%s marker=%d" % (hashlib.sha256(t.encode()).hexdigest().upper()[:16], t.count(M)))
from openjarvis.core.config import load_config, resolve_file_write_dirs
from openjarvis.tools.file_write import FileWriteTool
dirs = resolve_file_write_dirs(load_config()); ws = Path(dirs[0]); fw = FileWriteTool(allowed_dirs=dirs)
for lab, name in (("T1", "w83_f11.docx"), ("T2", "w83_f11.pptx"), ("T3", "w83_f11.xlsx"), ("T4", "W83_F11.DOCX")):
    r = fw.execute(path=name, content="text")
    print("%s %-14s refused=%s file_created=%s steers=%s" % (lab, name, not r.success, (ws / name).exists(), "code_interpreter" in str(r.content)))
r = fw.execute(path="w83_f11.txt", content="ok")
print("T5 w83_f11.txt success=%s in_workspace=%s" % (r.success, (ws / "w83_f11.txt").exists()))
for q in ws.glob("w83_f11*"): q.unlink()
