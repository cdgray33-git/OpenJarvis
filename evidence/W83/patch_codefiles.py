# patch_codefiles.py - W87 G-10 patch A (openjarvis-w87-codefiles-v1)
# code_interpreter reports every file created or changed in the workspace during the run:
#   - in ToolResult.content (the ONLY part the model sees - native_openhands passes content only), placed FIRST so the
#     agent's 4000-char truncation cannot cut it off
#   - in ToolResult.metadata["files"] as [{"path", "size_bytes"}] - the same keys the author's file_write/file_read use;
#     the author's ToolExecutor already forwards JSON-safe metadata on TOOL_CALL_END, so this IS the file-created record
# Run from PS C:\Users\Admin\OpenJarvis> with the venv python. Backs up first. Does NOT commit. Does NOT restart.
import sys, time, shutil, py_compile
from pathlib import Path

ROOT = Path.cwd()
TGT = ROOT / "src" / "openjarvis" / "tools" / "code_interpreter.py"
BAKDIR = ROOT / "evidence" / "W83" / "backup"
MARK = "openjarvis-w87-codefiles-v1"
if not TGT.is_file():
    sys.exit("STOP: %s not found - run from the repo root" % TGT)

raw = TGT.read_bytes().decode("utf-8")
nl = "\r\n" if "\r\n" in raw else "\n"
def L(s): return s.replace("\n", nl)
if MARK in raw:
    sys.exit("STOP: marker already present - patch was applied before; nothing written")

A1 = L("        code = _oj_strip_fence(code)  # openjarvis-w83-codefence-v1\n")
N1 = A1 + L("        _oj_before = _oj_snapshot()  # openjarvis-w87-codefiles-v1\n")

A2 = L('''            return ToolResult(
                tool_name="code_interpreter",
                content=output or "(no output)",
                success=result.returncode == 0,
                metadata={"returncode": result.returncode},
            )
''')
N2 = L('''            # openjarvis-w87-codefiles-v1 (W87 G-10): report files the run created or changed, FIRST in content
            _oj_files = _oj_changed(_oj_before)
            _oj_content = output or "(no output)"
            if _oj_files:
                _oj_content = (
                    "Files created or changed in the workspace:\\n"
                    + "\\n".join("%s (%d bytes)" % (f["path"], f["size_bytes"]) for f in _oj_files)
                    + "\\n\\nOutput:\\n" + _oj_content
                )
            return ToolResult(
                tool_name="code_interpreter",
                content=_oj_content,
                success=result.returncode == 0,
                metadata={"returncode": result.returncode, "files": _oj_files},
            )
''')

A3 = L('__all__ = ["CodeInterpreterTool"]')
N3 = L('''# openjarvis-w87-codefiles-v1 (W87 G-10): the author returns stdout only, so a script that saves a document and prints
# nothing gives the model "(no output)" and no proof the file exists (S3 R2: valid .docx made, model then tried shell_exec to
# check, hit the confirmation gate, and told the user it failed). Snapshot the workspace top level before the run and
# report what changed after it. Files written OUTSIDE the workspace by absolute path are not seen here (G-1, POAM-50).
def _oj_snapshot():
    try:
        d = Path(_oj_workdir())
        return {p.name: (p.stat().st_mtime_ns, p.stat().st_size) for p in d.iterdir() if p.is_file()}
    except Exception:
        return None

def _oj_changed(before):
    if before is None:
        return []
    try:
        d = Path(_oj_workdir())
        out = []
        for p in sorted(d.iterdir()):
            if not p.is_file():
                continue
            st = p.stat()
            if before.get(p.name) != (st.st_mtime_ns, st.st_size):
                out.append({"path": str(p.resolve()), "size_bytes": st.st_size})
        return out
    except Exception:
        return []

''') + A3

for name, a in (("A1", A1), ("A2", A2), ("A3", A3)):
    n = raw.count(a)
    if n != 1:
        sys.exit("STOP: anchor %s found %d times (need 1) - nothing written" % (name, n))

new = raw.replace(A1, N1).replace(A2, N2).replace(A3, N3)
BAKDIR.mkdir(parents=True, exist_ok=True)
bak = BAKDIR / ("code_interpreter.py.bak-W87-codefiles-" + time.strftime("%Y%m%d_%H%M%S"))
shutil.copy2(TGT, bak)
TGT.write_bytes(new.encode("utf-8"))
print("backup:", bak)
print("bytes old %d new %d  marker count %d" % (len(raw.encode("utf-8")), len(new.encode("utf-8")), new.count(MARK)))
try:
    py_compile.compile(str(TGT), doraise=True)
    print("COMPILE PASS")
except Exception as e:
    print("COMPILE FAIL:", e)
    shutil.copy2(bak, TGT)
    sys.exit("ROLLED BACK from backup")

# ---- in-process V&V (patched source, not an installed copy) ----
sys.path.insert(0, str(ROOT / "src"))
from openjarvis.tools.code_interpreter import CodeInterpreterTool, _oj_workdir
import openjarvis.tools.code_interpreter as ci
print("module file:", ci.__file__)
ws = Path(_oj_workdir())
probes = [ws / "w87_g10_probe.txt", ws / "w87_g10_probe.docx"]
for p in probes:
    if p.exists():
        p.unlink()
t = CodeInterpreterTool()
res = []
r1 = t.execute(code="print(2+2)")
res.append(("V1 no file -> no Files line, content unchanged", r1.success and "Files created" not in r1.content and r1.content.strip() == "4" and r1.metadata.get("files") == []))
r2 = t.execute(code="from pathlib import Path\nPath('w87_g10_probe.txt').write_text('g10')")
res.append(("V2 silent text save -> full path in content + metadata", r2.success and str(probes[0]) in r2.content and "(no output)" in r2.content and r2.metadata.get("files", [{}])[0].get("path") == str(probes[0])))
r3 = t.execute(code="from docx import Document\nd = Document()\nd.add_paragraph('g10 probe')\nd.save('w87_g10_probe.docx')\nprint('saved')")
res.append(("V3 docx save + print -> path first, Output after", r3.success and r3.content.startswith("Files created or changed in the workspace:") and str(probes[1]) in r3.content and r3.content.rstrip().endswith("saved")))
r4 = t.execute(code="from pathlib import Path\nprint(Path('w87_g10_probe.txt').read_text())")
res.append(("V4 read-only run -> no Files line", r4.success and "Files created" not in r4.content and r4.metadata.get("files") == []))
r5 = t.execute(code="raise SystemExit(3)")
res.append(("V5 failing run -> success False, returncode 3, files []", (not r5.success) and r5.metadata.get("returncode") == 3 and r5.metadata.get("files") == []))
import json
res.append(("V6 metadata JSON-safe (reaches TOOL_CALL_END)", json.dumps(r3.metadata) is not None))
for p in probes:
    if p.exists():
        p.unlink()
for name, ok in res:
    print(("PASS " if ok else "FAIL ") + name)
print("V3 content was:\n" + r3.content)
print("RESULT %d/%d" % (sum(1 for _, ok in res if ok), len(res)))
