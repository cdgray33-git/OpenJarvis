import sys
from openjarvis.tools.mailbox_tools import connector_for

c = connector_for("yahoo_main")
print("connector:", type(c).__name__)

found = None
for n in ["_connect", "connect", "_imap", "_open", "_session", "_client"]:
    if hasattr(c, n):
        found = n
        break
if found is None:
    print("no connect helper. callables:")
    for n in dir(c):
        if not n.startswith("__") and callable(getattr(c, n, None)):
            print("   ", n)
    sys.exit(2)
print("connect helper:", found)

obj = getattr(c, found)
obj = obj() if callable(obj) else obj

class Null:
    def __init__(self, v): self.v = v
    def __enter__(self): return self.v
    def __exit__(self, *a): return False

cm = obj if hasattr(obj, "__enter__") else Null(obj)

def quote(f):
    q = getattr(c, "_quote_folder", None)
    return q(f) if callable(q) else f

with cm as imap:
    print("imap object:", type(imap).__name__)
    try:
        folders = c._target_folders(imap, for_usage=True)
    except TypeError:
        folders = c._target_folders(imap)
    print("folder count:", len(folders))
    print("folders:", folders)
    print("")
    print("FOLDER".ljust(28), "SEL", "SRCH", "len(d)", "bytes", "UIDS", "EXISTS")
    for f in folders:
        name = f if isinstance(f, str) else str(f)
        try:
            styp, sdata = imap.select(quote(name), readonly=True)
        except Exception as e:
            print(name[:28], "SELECT EXC", e)
            continue
        try:
            ex = sdata[0].decode() if sdata and sdata[0] else ""
        except Exception:
            ex = str(sdata)
        try:
            rtyp, rdata = imap.uid("SEARCH", None, "ALL")
        except Exception as e:
            print(name[:28], styp, "SEARCH EXC", e)
            continue
        nparts = len(rdata) if rdata else 0
        nbytes = len(rdata[0]) if rdata and rdata[0] else 0
        nuids = len(rdata[0].split()) if rdata and rdata[0] else 0
        print(name[:28].ljust(28), styp, rtyp, nparts, nbytes, nuids, ex)
