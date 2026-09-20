import ast, os, sys, time

PATH = os.path.join("src", "openjarvis", "server", "api_routes.py")
OLD = 'ws_router = create_ws_router(get_event_bus())'
NEW = 'ws_router = create_ws_router(getattr(app.state, "bus", None) or get_event_bus())  # openjarvis-ws-bus-v1'
APPLY = "--apply" in sys.argv

with open(PATH, "r", encoding="utf-8", newline="") as f:
    src = f.read()

before = len(src.encode("utf-8"))
print("file:", PATH)
print("size:", before)
print("eol:", "CRLF" if "\r\n" in src else "LF")

n = src.count(OLD)
print("anchor matches:", n)
if n != 1:
    print("ABORT: anchor must match exactly 1")
    sys.exit(1)
if "openjarvis-ws-bus-v1" in src:
    print("ABORT: marker already present")
    sys.exit(1)

cand = src.replace(OLD, NEW)
predicted = len(cand.encode("utf-8"))
print("predicted size:", predicted, "delta:", predicted - before)

ast.parse(cand)
print("ast.parse: OK")

if not APPLY:
    print("DRY RUN - nothing written. Re-run with --apply")
    sys.exit(0)

bak = PATH + ".bak_wsbus_" + time.strftime("%Y%m%d_%H%M%S")
with open(bak, "w", encoding="utf-8", newline="") as f:
    f.write(src)
print("backup:", bak)

with open(PATH, "w", encoding="utf-8", newline="") as f:
    f.write(cand)

actual = os.path.getsize(PATH)
print("on-disk size:", actual)
if actual != predicted:
    print("ABORT MISMATCH - restore with:")
    print("Copy-Item '" + bak + "' '" + PATH + "' -Force")
    sys.exit(1)

with open(PATH, "r", encoding="utf-8", newline="") as f:
    print("marker present:", "openjarvis-ws-bus-v1" in f.read())
print("APPLIED OK")
