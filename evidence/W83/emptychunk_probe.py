import sqlite3, json, glob
snap = sorted(glob.glob(r"C:\Users\Admin\OpenJarvis\evidence\W83\backup\memory.db.snap-*"))[-1]
con = sqlite3.connect("file:%s?mode=ro" % snap.replace("\\", "/"), uri=True)
rows = [(json.loads(md or "{}"), c) for md, c in con.execute("select metadata, content from documents")]
bad = [(m.get("chunk_index"), c) for m, c in rows if m.get("title") == "boot_backend_dump.txt"]
print("SNAP", snap, "bad_chunks=%d" % len(bad))
lens = sorted(set(len(c or "") for _, c in bad)); print("LENGTHS", lens)
idx = sorted(i for i, _ in bad if i is not None); print("CHUNK_INDEX min=%s max=%s" % (idx[:1], idx[-1:]))
for i, c in sorted(bad, key=lambda t: t[0] or 0)[:5]:
    print("CHUNK", i, repr(c), (c or "").encode("utf-8").hex())
