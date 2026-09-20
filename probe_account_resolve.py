"""probe_account_resolve.py - READ ONLY. What does a bad account id do?"""
from openjarvis.tools.mailbox_tools import connector_for

for acct in ("yahoo_main", "cdgray33@yahoo.com", "", "nonsense_xyz"):
    try:
        c = connector_for(acct)
        if c is None:
            print("%-22s -> connector_for returned None" % repr(acct))
            continue
        hits = c.find_messages(from_addr="michaels", limit=5000)
        print("%-22s -> connector OK, hits=%d" % (repr(acct), len(hits)))
    except Exception as exc:
        print("%-22s -> RAISED %s: %s" % (repr(acct), type(exc).__name__, exc))
