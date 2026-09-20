"""peek_michaels.py - READ ONLY. Cross-tab address x folder, plus subjects."""
from collections import defaultdict
from openjarvis.tools.mailbox_tools import connector_for

c = connector_for("yahoo_main")
if c is None:
    raise SystemExit("REFUSED: connector_for returned None")

hits = c.find_messages(from_addr="michaels", limit=5000)
grid = defaultdict(int)
for h in hits:
    grid[(str(h.get("from_addr","")), str(h.get("folder","")))] += 1
print("ADDRESS x FOLDER")
for (a, f), n in sorted(grid.items(), key=lambda kv: -kv[1]):
    print("  %-45s %-14s %4d" % (a, f, n))

print("\nCUSTOMFRAME SUBJECTS")
for h in hits:
    if "customframe" in str(h.get("from_addr","")):
        print("  [%s] %s" % (h.get("folder",""), str(h.get("subject",""))[:80]))
