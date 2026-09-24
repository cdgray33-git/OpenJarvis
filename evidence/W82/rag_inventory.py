import json, pathlib, sqlite3, tomllib, urllib.request
out = []; P = out.append; home = pathlib.Path.home() / ".openjarvis"
for name in ("memory.db", "knowledge.db"):
    db = home / name
    if not db.exists(): P(f"{name}: ABSENT"); continue
    con = sqlite3.connect(f"file:{db}?mode=ro", uri=True); cur = con.cursor()
    P(f"{name}: {db.stat().st_size/1048576:.1f} MB  modified={__import__('datetime').datetime.fromtimestamp(db.stat().st_mtime)}")
    for (t, sql) in cur.execute("select name, sql from sqlite_master where type in ('table') order by name").fetchall():
        try: n = cur.execute(f'select count(*) from "{t}"').fetchone()[0]
        except Exception as e: n = f"ERR {e}"
        P(f"   table {t:32s} rows={n}  {'FTS5' if sql and 'fts5' in sql.lower() else ''}")
    con.close()
cfg = tomllib.loads((home / "config.toml").read_text(encoding="utf-8"))
for sect in ("memory", "tools", "agent"):
    v = cfg.get(sect, {})
    keep = {k: v[k] for k in v if any(s in k for s in ("backend", "context", "top_k", "min_score", "db_path", "chunk", "tools"))} if isinstance(v, dict) else v
    P(f"config [{sect}] {keep}")
try:
    spec = json.load(urllib.request.urlopen("http://127.0.0.1:8010/openapi.json", timeout=15))
    P("routes: " + ", ".join(p for p in sorted(spec["paths"]) if any(s in p for s in ("memory", "knowledge", "upload", "research", "retriev"))))
except Exception as e: P(f"openapi failed {e!r}")
text = "\n".join(out); print(text)
pathlib.Path(r"C:\Users\Admin\OpenJarvis\evidence\W82\rag-inventory.txt").write_text(text, encoding="utf-8")
