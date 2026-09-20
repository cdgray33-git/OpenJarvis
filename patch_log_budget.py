"""patch_log_budget.py - marker openjarvis-log-budget-v1

Patch 1 of 3 for the 30 MB FIFO log budget.
serve.py backend.log: 10MB x 5 (60 MB) -> 4MB x 3 (12 MB), plus a filter
that drops uvicorn.access records for the telemetry polling endpoints.
"""
import argparse, ast, hashlib, shutil, sys, time
from pathlib import Path

TARGET = Path("src/openjarvis/cli/serve.py")
MARKER = "openjarvis-log-budget-v1"

A1_OLD = "maxBytes=10 * 1024 * 1024, backupCount=5"
A1_NEW = "maxBytes=4 * 1024 * 1024, backupCount=3"

A2_OLD = "def _configure_file_logging() -> str:"
A2_NEW = '''class _TelemetryNoiseFilter(logging.Filter):
    """Drop uvicorn.access records for the telemetry polling endpoints.

    openjarvis-log-budget-v1: these two paths are polled roughly every 3
    seconds and accounted for 98 percent of backend.log volume, crowding
    every record worth keeping out of the rotation budget.
    """

    _NOISE = ("/v1/telemetry/energy", "/v1/telemetry/stats")

    def filter(self, record):
        if record.name != "uvicorn.access":
            return True
        try:
            msg = record.getMessage()
        except Exception:
            return True
        return not any(p in msg for p in self._NOISE)


def _configure_file_logging() -> str:'''

A3_OLD = "    root_logger = logging.getLogger()"
A3_NEW = """    file_handler.addFilter(_TelemetryNoiseFilter())  # openjarvis-log-budget-v1

    root_logger = logging.getLogger()"""

ANCHORS = [("A1 rotation budget", A1_OLD, A1_NEW),
           ("A2 filter class", A2_OLD, A2_NEW),
           ("A3 attach filter", A3_OLD, A3_NEW)]

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()

    if not TARGET.exists():
        sys.exit("FAIL: %s not found (run from repo root)" % TARGET)

    raw = TARGET.read_bytes()
    eol = "CRLF" if b"\r\n" in raw else "LF"
    text = raw.decode("utf-8")
    print("target   : %s" % TARGET)
    print("size     : %d bytes, EOL %s" % (len(raw), eol))
    print("sha256   : %s" % hashlib.sha256(raw).hexdigest().upper()[:16])

    if MARKER in text:
        sys.exit("FAIL: marker %s already present - already patched" % MARKER)

    new = text
    for name, old, repl in ANCHORS:
        n = new.count(old)
        print("anchor %-20s matches=%d" % (name, n))
        if n != 1:
            sys.exit("FAIL: anchor %s matched %d times, need exactly 1" % (name, n))
        new = new.replace(old, repl, 1)

    try:
        ast.parse(new)
    except SyntaxError as e:
        sys.exit("FAIL: candidate does not parse: %s" % e)
    print("ast.parse: OK")
    print("delta    : %+d bytes" % (len(new.encode("utf-8")) - len(raw)))

    if not args.apply:
        print("\nDRY RUN ONLY - rerun with --apply to write")
        return

    bak = TARGET.with_suffix(TARGET.suffix + ".bak_logbudget_%s" % time.strftime("%Y%m%d_%H%M%S"))
    shutil.copy2(TARGET, bak)
    print("backup   : %s" % bak)
    TARGET.write_bytes(new.encode("utf-8"))
    after = TARGET.read_bytes()
    print("written  : %d bytes, sha256 %s" % (len(after), hashlib.sha256(after).hexdigest().upper()[:16]))
    print("marker   : %s" % ("present" if MARKER in after.decode("utf-8") else "MISSING"))

main()
