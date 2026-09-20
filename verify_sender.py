import sys
from openjarvis.tools.mailbox_tools import connector_for
pat = sys.argv[1]
c = connector_for("yahoo_main")
allhits = c.find_messages(from_addr=pat, limit=5000)
print("ALLFOLDERS", len(allhits))
for f in ("Inbox", "Archive", "Trash", "Bulk"):
    try:
        h = c.find_messages(folder=f, from_addr=pat, limit=5000)
        print(f, len(h))
    except Exception as e:
        print(f, "ERR", e)
