import sqlite3, json, sys
from openjarvis.tools.storage.sqlite import SQLiteMemory
DB = "C:/Users/Admin/.openjarvis/memory.db"; KEEP_TITLE = "executive assistant notes.txt"
con = sqlite3.connect("file:%s?mode=ro" % DB, uri=True)
rows = con.execute("select id, source, metadata from documents").fetchall(); con.close()
def title(md):
    try: return json.loads(md or "{}").get("title") or ""
    except Exception: return ""
dele = [i for i, s, md in rows if s == "upload" and title(md) != KEEP_TITLE]
keep = [i for i, s, md in rows if i not in set(dele)]
print("PLAN total=%d delete=%d keep=%d" % (len(rows), len(dele), len(keep)))
if len(dele) != 113 or len(keep) != 3:
    print("ABORT - counts differ from inventory, nothing deleted"); sys.exit(1)
m = SQLiteMemory()
if not hasattr(m, "delete"):
    print("ABORT - author backend has no delete(), nothing deleted"); sys.exit(1)
ok = sum(1 for i in dele if m.delete(i))
print("DELETED ok=%d of %d" % (ok, len(dele)))
print("COUNT after=%d" % m.count())
con = sqlite3.connect("file:%s?mode=ro" % DB, uri=True)
for s, md, c in con.execute("select source, metadata, substr(content,1,60) from documents"):
    print("REMAIN src=%-7s title=%-32s content=%r" % (s or "(empty)", title(md)[:32], c))
r = m.retrieve("BLUEHERON", top_k=3)
print("RECALL BLUEHERON hits=%d top=%r" % (len(r), (r[0].content[:60] if r else "")))
