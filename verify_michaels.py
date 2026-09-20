"""verify_michaels.py - READ ONLY. Ground-truths the agent's michaels count."""
from collections import defaultdict
from openjarvis.tools.mailbox_tools import connector_for

NEEDLE = "michaels"
LIMIT = 5000

c = connector_for("yahoo_main")
if c is None:
    raise SystemExit("REFUSED: connector_for returned None")

hits = c.find_messages(from_addr=NEEDLE, limit=LIMIT)
n = len(hits)
print("needle   : %s" % NEEDLE)
print("limit    : %d" % LIMIT)
print("total    : %d" % n)
print("truncated: %s" % (n >= LIMIT))
print("bytes    : %d" % sum(int(h.get("bytes", 0) or 0) for h in hits))

by_a = defaultdict(lambda: [0, 0])
by_f = defaultdict(lambda: [0, 0])
for h in hits:
    b = int(h.get("bytes", 0) or 0)
    a = by_a[str(h.get("from_addr", ""))]; a[0] += 1; a[1] += b
    f = by_f[str(h.get("folder", ""))];    f[0] += 1; f[1] += b

print("\nBY ADDRESS")
for k, v in sorted(by_a.items(), key=lambda kv: -kv[1][0]):
    print("  %-45s %5d  %12d" % (k, v[0], v[1]))
print("\nBY FOLDER")
for k, v in sorted(by_f.items(), key=lambda kv: -kv[1][0]):
    print("  %-45s %5d  %12d" % (k, v[0], v[1]))
