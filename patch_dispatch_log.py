import ast, os, re, shutil, sys, datetime
P = r"src\openjarvis\tools\_stubs.py"
MARK = "openjarvis-dispatch-log-v1"

raw = open(P, "rb").read()
crlf = b"\r\n" in raw
text = raw.decode("utf-8")
if crlf:
    text = text.replace("\r\n", "\n")
if MARK in text:
    print("ALREADY PATCHED"); sys.exit(1)

BLOCK = '''
# --- ''' + MARK + ''' ---------------------------------------------------
# Tool-boundary dispatch record in its own rotating file, so a turn that
# dispatched NOTHING is distinguishable from one never instrumented.
CURRENT_TURN_ID: contextvars.ContextVar = contextvars.ContextVar(
    "openjarvis_turn_id", default="-"
)
_dispatch_logger = None


def _get_dispatch_logger():
    global _dispatch_logger
    if _dispatch_logger is not None:
        return _dispatch_logger
    lg = logging.getLogger("openjarvis.dispatch")
    if not lg.handlers:
        log_dir = os.path.join(
            os.environ.get("LOCALAPPDATA", os.path.expanduser("~")),
            "OpenJarvis", "logs",
        )
        try:
            os.makedirs(log_dir, exist_ok=True)
            h = logging.handlers.RotatingFileHandler(
                os.path.join(log_dir, "dispatch.log"),
                maxBytes=2 * 1024 * 1024, backupCount=4, encoding="utf-8",
            )
            h.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
            lg.addHandler(h)
        except Exception:
            lg.addHandler(logging.NullHandler())
    lg.setLevel(logging.INFO)
    lg.propagate = False
    _dispatch_logger = lg
    return lg


def _args_digest(rawargs, limit: int = 400) -> str:
    try:
        s = rawargs if isinstance(rawargs, str) else json.dumps(rawargs, default=str)
    except Exception:
        s = str(rawargs)
    s = " ".join(s.split())
    return s[:limit] + ("...TRUNC" if len(s) > limit else "")


'''

A1_OLD = "import concurrent.futures\nimport json\nimport time\n"
A1_NEW = ("import concurrent.futures\nimport contextvars\nimport json\n"
          "import logging\nimport logging.handlers\nimport os\nimport time\n")

A2_OLD = "\nclass ToolExecutor:\n"
A2_NEW = "\n" + BLOCK + "class ToolExecutor:\n"

A3_OLD = '        """Parse arguments, dispatch to tool, measure latency, emit events."""\n'
A3_NEW = (A3_OLD +
          "        _get_dispatch_logger().info(\n"
          '            "ATTEMPT turn=%s tool=%s args=%s",\n'
          "            CURRENT_TURN_ID.get(), tool_call.name,\n"
          "            _args_digest(tool_call.arguments),\n"
          "        )\n")

A4_OLD = "        return result\n\n    @staticmethod\n"
A4_NEW = ("        _get_dispatch_logger().info(\n"
          '            "OUTCOME turn=%s tool=%s success=%s latency=%.3f timed_out=%s",\n'
          "            CURRENT_TURN_ID.get(), tool_call.name, result.success,\n"
          "            latency, bool(result.metadata.get(\"timed_out\")),\n"
          "        )\n"
          "        return result\n\n    @staticmethod\n")

new = text
for i, (old, rep) in enumerate([(A1_OLD, A1_NEW), (A2_OLD, A2_NEW),
                                (A3_OLD, A3_NEW), (A4_OLD, A4_NEW)], 1):
    n = new.count(old)
    print("anchor %d matches: %d" % (i, n))
    if n != 1:
        print("ABORT: anchor %d matched %d times" % (i, n)); sys.exit(2)
    new = new.replace(old, rep)

ast.parse(new)
print("ast.parse OK")
print("pre  bytes:", len(raw))
out = new.replace("\n", "\r\n").encode("utf-8") if crlf else new.encode("utf-8")
print("post bytes:", len(out), "delta", len(out) - len(raw), "| EOL:", "CRLF" if crlf else "LF")

if "--apply" not in sys.argv:
    print("DRY RUN ONLY - rerun with --apply"); sys.exit(0)

bak = P + ".bak_dispatchlog_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
shutil.copy2(P, bak)
open(P, "wb").write(out)
chk = open(P, "rb").read().decode("utf-8")
print("BACKUP:", bak)
print("marker present:", MARK in chk)
print("final bytes:", os.path.getsize(P))
