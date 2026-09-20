from openjarvis.tools.mailbox_tools import connector_for

c = connector_for("yahoo_main")
obj = c._connect()
cm = obj if hasattr(obj, "__enter__") else None

def run(imap):
    print("=== A. REACH TEST on Inbox ===")
    styp, sdata = imap.select("Inbox", readonly=True)
    print("select:", styp, sdata)
    tests = [
        ("ALL", ("ALL",)),
        ('FROM "updates-noreply@linkedin.com"', ("FROM", '"updates-noreply@linkedin.com"')),
        ('FROM "linkedin"', ("FROM", '"linkedin"')),
        ('FROM "@linkedin.com"', ("FROM", '"@linkedin.com"')),
    ]
    for label, args in tests:
        try:
            typ, data = imap.uid("SEARCH", None, *args)
            n = len(data[0].split()) if data and data[0] else 0
            print("  {:<45} {:>4}  uids={}".format(label, str(typ), n))
        except Exception as e:
            print("  {:<45} EXC {}".format(label, e))

    print("")
    print("=== B. QUOTING TEST (Defect 5) ===")
    q = getattr(c, "_quote_folder", None)
    print("_quote_folder exists:", callable(q))
    if callable(q):
        print("  _quote_folder('2025 Job Search') ->", repr(q("2025 Job Search")))
    for f in ["2025 Job Search", "Online Purchases"]:
        for label, arg in [("raw", f), ("quoted", '"' + f + '"')]:
            try:
                typ, d = imap.select(arg, readonly=True)
                print("  {:<22} {:<7} {:>4} {}".format(f, label, str(typ), d))
            except Exception as e:
                print("  {:<22} {:<7} EXC {}".format(f, label, e))

if cm:
    with cm as imap:
        run(imap)
else:
    run(obj)
