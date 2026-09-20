# MARKER: openjarvis-census-target-v3
from openjarvis.tools.mailbox_tools import connector_for
c = connector_for("yahoo_main")
for tok in ["sears", "amf", "navyexchg", "zales"]:
    r = c.find_messages(from_addr=tok, limit=5000)
    assert isinstance(r, list), ("NOT A LIST", type(r))
    folders = {}
    for x in r:
        folders[x.get("folder")] = folders.get(x.get("folder"), 0) + 1
    print(tok, "total=", len(r), folders)
