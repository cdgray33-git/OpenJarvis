from openjarvis.tools.mailbox_tools import connector_for
c = connector_for("yahoo_main")
for f in ("Archive", "Trash"):
    h = c.find_messages(folder=f, from_addr="bachrach", limit=5000)
    print(f, len(h))
