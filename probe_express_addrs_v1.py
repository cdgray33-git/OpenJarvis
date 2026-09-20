from collections import defaultdict
from openjarvis.tools.mailbox_tools import connector_for

c = connector_for("yahoo_main")
if c is None:
    raise SystemExit("connector_for returned None - account did not resolve")

rows = c.find_messages(from_addr="express", limit=5000)
if not isinstance(rows, list):
    raise SystemExit("expected list, got %r" % type(rows))

agg = defaultdict(lambda: defaultdict(int))
for m in rows:
    agg[(m.get("from_addr") or "?").lower()][m.get("folder") or "?"] += 1

print("TOTAL", len(rows))
for addr in sorted(agg, key=lambda a: -sum(agg[a].values())):
    n = sum(agg[addr].values())
    folders = ", ".join("%s %d" % (f, c2) for f, c2 in sorted(agg[addr].items()))
    print("%-45s %4d   %s" % (addr, n, folders))
