import os, sys, time, shutil, tempfile, py_compile, hashlib
from pathlib import Path
M = "openjarvis-w83-skipdirs-v1"
p = os.path.join(os.getcwd(), "src", "openjarvis", "tools", "storage", "ingest.py")
t = open(p, "rb").read().decode("utf-8")
if M in t: print("ALREADY PATCHED - no change"); sys.exit(0)
nl = "\r\n" if "\r\n" in t else "\n"
a = '        "__pycache__",' + nl
print("ANCHOR count=%d (want 1)" % t.count(a))
if t.count(a) != 1: print("ABORT - nothing written"); sys.exit(1)
t = t.replace(a, a + '        # ' + M + ' (owner O-a, W83): build output trees - likely route to the 21 GB corpus' + nl + '        "target",' + nl + '        "dist",' + nl + '        "build",' + nl)
bak = os.path.join(os.getcwd(), "evidence", "W83", "backup", "ingest.py.bak-W83-skipdirs-" + time.strftime("%Y%m%d_%H%M%S"))
shutil.copy2(p, bak); print("BACKUP", bak)
compile(t, p, "exec"); open(p, "wb").write(t.encode("utf-8")); py_compile.compile(p, doraise=True)
print("AFTER sha256=%s bytes=%d marker=%d" % (hashlib.sha256(t.encode()).hexdigest().upper()[:16], len(t.encode()), t.count(M)))
from openjarvis.tools.storage.ingest import ingest_path
d = Path(tempfile.mkdtemp()); words = " ".join("word%d" % k for k in range(60))
for rel in ("target/x.txt", "dist/y.txt", "build/z.txt", "docs/keep.txt", "docs/sub/target_notes.txt"):
    f = d / rel; f.parent.mkdir(parents=True, exist_ok=True); f.write_text(words, encoding="utf-8")
names = sorted(set(Path(c.source).name for c in ingest_path(d)))
print("T1+T3 ingest_path sources=%s PASS=%s" % (names, names == ["keep.txt", "target_notes.txt"]))
from openjarvis.tools.storage.sqlite import SQLiteMemory
from openjarvis.tools.storage_tools import MemoryIndexTool
dbp = str(d / "throwaway.db")
try:
    be = SQLiteMemory(db_path=dbp)
except TypeError:
    be = SQLiteMemory(dbp)
(d / "throwaway.db").exists() or print("NOTE throwaway db path not honoured - T2 skipped"); 
if (d / "throwaway.db").exists():
    r = MemoryIndexTool(backend=be).execute(path=str(d / "docs"))
    print("T2 memory_index success=%s count=%d content=%r" % (getattr(r, "success", None), be.count(), str(getattr(r, "content", ""))[:90]))
    print("T2 PASS=%s" % (getattr(r, "success", False) and be.count() == 2))
try: be.close()
except Exception: pass
shutil.rmtree(d, ignore_errors=True)
