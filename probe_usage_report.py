from openjarvis.tools.mailbox_tools import connector_for
c = connector_for("yahoo_main")
print("connector:", c)
r = c.usage_report(top_senders=40, top_messages=5)
print("TYPE:", type(r))
print("KEYS:", list(r.keys()) if isinstance(r, dict) else "n/a")
if isinstance(r, dict):
    if "error" in r:
        print("ERROR:", r["error"])
    ts = r.get("top_senders") or []
    print("top_senders rows:", len(ts))
    for row in ts[:40]:
        print("  ", row)
