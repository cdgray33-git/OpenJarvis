import os, sys, time, shutil, py_compile, hashlib
from pathlib import Path
M = "openjarvis-w83-codefence-v1"; R = os.getcwd()
p = os.path.join(R, "src", "openjarvis", "tools", "code_interpreter.py")
t = open(p, "rb").read().decode("utf-8")
if M in t: print("ALREADY PATCHED - no change"); sys.exit(0)
nl = "\r\n" if "\r\n" in t else "\n"
a = "        # Security check" + nl
tail = nl + nl + "__all__"
print("ANCHORS security=%d all=%d (want 1 1)" % (t.count(a), t.count(tail)))
if t.count(a) != 1 or t.count(tail) != 1: print("ABORT - nothing written"); sys.exit(1)
t = t.replace(a, "        code = _oj_strip_fence(code)  # " + M + nl + a)
h = nl.join(["", "", "# " + M + " (W83 G-9): models often wrap the code argument in a markdown fence (```python ... ```);",
             "# the author tool ran it verbatim, so line 1 was a SyntaxError. Strip one leading fence line and a trailing fence.",
             "def _oj_strip_fence(code):",
             "    s = code.strip()",
             "    if not s.startswith(\"```\"):",
             "        return code",
             "    i = s.find(\"\\n\")",
             "    s = s[i + 1:] if i != -1 else \"\"",
             "    s = s.rstrip()",
             "    if s.endswith(\"```\"):",
             "        s = s[:-3].rstrip()",
             "    return s"])
t = t.replace(tail, h + tail, 1)
bak = os.path.join(R, "evidence", "W83", "backup", "code_interpreter.py.bak-W83-codefence-" + time.strftime("%Y%m%d_%H%M%S"))
shutil.copy2(p, bak); print("BACKUP", bak)
compile(t, p, "exec"); open(p, "wb").write(t.encode("utf-8")); py_compile.compile(p, doraise=True)
print("AFTER sha=%s marker=%d" % (hashlib.sha256(t.encode()).hexdigest().upper()[:16], t.count(M)))
from openjarvis.tools.code_interpreter import CodeInterpreterTool, _oj_workdir
ci = CodeInterpreterTool()
r1 = ci.execute(code="```python\nprint(2+2)\n```"); print("U1 fenced runs=%s out=%r" % (r1.success, r1.content.strip()))
r2 = ci.execute(code="print(2+2)"); print("U2 plain unchanged=%s out=%r" % (r2.success, r2.content.strip()))
r3 = ci.execute(code="```python\nimport os\nos.system('echo x')\n```"); print("U3 fenced blocked still blocked=%s msg=%r" % (not r3.success and "Blocked" in r3.content, r3.content[:70]))
r4 = ci.execute(code="```py\nfrom openpyxl import Workbook\nwb = Workbook(); wb.active['A1'] = 'x'; wb.save('w83_f9_test.xlsx')\nprint('SAVED')\n```")
f = Path(_oj_workdir()) / "w83_f9_test.xlsx"
print("U4 fenced openpyxl success=%s file_in_workspace=%s" % (r4.success, f.exists()))
if f.exists(): f.unlink()
