import json, pathlib, sqlite3, sys, urllib.request
out = []; P = out.append
sys.path.insert(0, r"C:\Users\Admin\OpenJarvis\src")
P("=== 1. REGISTERED AGENT TYPES ===")
try:
    import openjarvis.agents  # side-effect registration
    reg = None
    for mod, name in (("openjarvis.core.registry", "AgentRegistry"), ("openjarvis.agents._registry", "AgentRegistry"), ("openjarvis.agents", "AgentRegistry")):
        try:
            reg = getattr(__import__(mod, fromlist=[name]), name); break
        except Exception:
            continue
    if reg is None: P("AgentRegistry not found")
    else:
        keys = reg.keys() if hasattr(reg, "keys") else getattr(reg, "_registry", {}).keys()
        for k in sorted(keys):
            try: cls = reg.get(k); P(f"  {k:24s} {cls.__module__}.{cls.__name__}  accepts_tools={getattr(cls, 'accepts_tools', '?')}")
            except Exception as e: P(f"  {k:24s} (get failed {e!r})")
except Exception as e:
    P(f"registry import failed {e!r}")
P("=== 2. MANAGED AGENTS (read-only) ===")
home = pathlib.Path.home() / ".openjarvis"
for db in sorted(home.glob("*.db")):
    con = sqlite3.connect(f"file:{db}?mode=ro", uri=True); cur = con.cursor()
    tabs = [r[0] for r in cur.execute("select name from sqlite_master where type='table'")]
    if "managed_agents" not in tabs: con.close(); continue
    P(f"DB {db}  tables={tabs}")
    cols = [r[1] for r in cur.execute("pragma table_info(managed_agents)")]
    for row in cur.execute("select * from managed_agents"):
        d = dict(zip(cols, row))
        cfg = d.get("config") or "{}"
        try: tools = json.loads(cfg).get("tools")
        except Exception: tools = "?"
        sm = str(d.get("summary_memory") or "")[:120].replace("\n", " ")
        P(f"  {str(d.get('name')):16s} id={str(d.get('id'))[:8]} type={d.get('agent_type')} status={d.get('status')} sched={d.get('schedule_type')}:{d.get('schedule_value')} tools={tools}")
        P(f"      summary_memory[:120]={sm!r}")
    for t in tabs:
        tc = [r[1] for r in cur.execute(f"pragma table_info({t})")]
        if "agent_id" in tc and t != "managed_agents":
            if "status" in tc:
                rows = cur.execute(f"select agent_id, status, count(*) from {t} group by agent_id, status").fetchall()
            else:
                rows = cur.execute(f"select agent_id, count(*) from {t} group by agent_id").fetchall()
            P(f"  table {t}: " + "; ".join(" ".join(str(x)[:8] if i == 0 else str(x) for i, x in enumerate(r)) for r in rows))
    con.close()
P("=== 3. LIVE AGENT ROUTES ===")
try:
    spec = json.load(urllib.request.urlopen("http://127.0.0.1:8010/openapi.json", timeout=15))
    for p, ops in sorted(spec.get("paths", {}).items()):
        if "agent" in p or "operator" in p or "scheduler" in p:
            P(f"  {p}  [{','.join(sorted(ops))}]")
except Exception as e:
    P(f"openapi failed {e!r}")
text = "\n".join(out); print(text)
pathlib.Path(r"C:\Users\Admin\OpenJarvis\evidence\W82\agents-inventory.txt").write_text(text, encoding="utf-8")
