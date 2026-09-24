import sqlite3, datetime
con = sqlite3.connect("file:C:/Users/Admin/.openjarvis/memory.db?mode=ro", uri=True)
print("TABLES", [r[0] for r in con.execute("select name from sqlite_master where type in ('table','view')")])
print("COLS", [r[1] for r in con.execute("pragma table_info(documents)")])
f = lambda t: datetime.datetime.fromtimestamp(t).strftime("%Y-%m-%d") if t else "-"
for src, n, sz, a, b in con.execute("select source, count(*), sum(length(content)), min(created_at), max(created_at) from documents group by source order by 2 desc"):
    print("SRC n=%3d bytes=%8d %s..%s  %s" % (n, sz or 0, f(a), f(b), (src or "(empty)")[:110]))
for (md,) in con.execute("select metadata from documents limit 3"):
    print("META", (md or "")[:140])
