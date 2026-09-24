import sqlite3, json, sys
con = sqlite3.connect("file:C:/Users/Admin/.openjarvis/memory.db?mode=ro", uri=True)
rows = con.execute("select metadata, length(content), source from documents").fetchall()
agg = {}
for md, ln, src in rows:
    try: t = json.loads(md or "{}").get("title") or "(no title)"
    except Exception: t = "(bad metadata)"
    a = agg.setdefault((src or "(empty)", t), [0, 0]); a[0] += 1; a[1] += ln or 0
print("TOTAL docs=%d titles=%d" % (len(rows), len(agg)))
for (src, t), (n, b) in sorted(agg.items(), key=lambda kv: -kv[1][0]):
    print("DOC src=%-7s chunks=%3d bytes=%7d  %s" % (src, n, b, t[:90]))
