import ast, os, shutil, sys, time

TARGET = os.path.join("src", "openjarvis", "engine", "ollama.py")
MARKER = "openjarvis-retry400-v1"

OLD = '''            if resp.status_code == 400 and tools:
                # Model may not support function calling -- retry without tools
                payload.pop("tools", None)
                resp = self._client.post("/api/chat", json=payload)
'''

NEW = '''            if resp.status_code == 400 and tools:
                # Model may not support function calling -- retry without tools
                _oj_log_retry400(resp, payload, tools)  # openjarvis-retry400-v1
                payload.pop("tools", None)
                resp = self._client.post("/api/chat", json=payload)
                _oj_log_retry400_result(resp)  # openjarvis-retry400-v1
'''

HELPERS = '''

# --- openjarvis-retry400-v1 : temporary diagnostic, remove when Defect 1 is fixed ---
def _oj_r400_logger():
    import logging, logging.handlers, os as _os
    lg = logging.getLogger("openjarvis.retry400")
    if getattr(lg, "_oj_ready", False):
        return lg
    try:
        d = _os.path.join(_os.environ.get("LOCALAPPDATA", "."), "OpenJarvis", "logs")
        _os.makedirs(d, exist_ok=True)
        h = logging.handlers.RotatingFileHandler(
            _os.path.join(d, "engine.log"),
            maxBytes=2 * 1024 * 1024,
            backupCount=2,
            encoding="utf-8",
        )
        h.setFormatter(logging.Formatter("%(asctime)s %(message)s"))
        lg.addHandler(h)
    except Exception:
        lg.addHandler(logging.NullHandler())
    lg.setLevel(logging.INFO)
    lg.propagate = False
    lg._oj_ready = True
    return lg


def _oj_log_retry400(resp, payload, tools):
    try:
        import json as _json
        try:
            body = resp.text[:600]
        except Exception:
            body = "<unreadable>"
        try:
            psize = len(_json.dumps(payload))
        except Exception:
            psize = -1
        _oj_r400_logger().info(
            "RETRY400 dropping tools ntools=%s payloadbytes=%s nmsgs=%s body=%r",
            len(tools) if tools else 0,
            psize,
            len(payload.get("messages", []) or []),
            body,
        )
    except Exception:
        pass


def _oj_log_retry400_result(resp):
    try:
        _oj_r400_logger().info(
            "RETRY400 retry_status=%s", getattr(resp, "status_code", "?")
        )
    except Exception:
        pass
'''

apply = "--apply" in sys.argv

with open(TARGET, "r", encoding="utf-8", newline="") as f:
    src = f.read()

print("size before:", len(src.encode("utf-8")))
print("CRLF present:", "\r\n" in src)
if MARKER in src:
    print("ABORT: marker already present")
    sys.exit(1)

n = src.count(OLD)
print("anchor matches:", n)
if n != 1:
    print("ABORT: anchor must match exactly once")
    sys.exit(1)

cand = src.replace(OLD, NEW) + HELPERS
try:
    ast.parse(cand)
except SyntaxError as e:
    print("ABORT: candidate does not parse:", e)
    sys.exit(1)
print("candidate parses OK")

predicted = len(cand.encode("utf-8"))
print("predicted size:", predicted, "delta:", predicted - len(src.encode("utf-8")))

if not apply:
    print("DRY RUN ONLY - rerun with --apply")
    sys.exit(0)

bak = TARGET + ".bak_retry400_" + time.strftime("%Y%m%d_%H%M%S")
shutil.copy2(TARGET, bak)
print("backup:", bak)

with open(TARGET, "w", encoding="utf-8", newline="") as f:
    f.write(cand)

actual = os.path.getsize(TARGET)
print("actual size:", actual)
if actual != predicted:
    print("MISMATCH - restore with:")
    print("Copy-Item '" + bak + "' '" + TARGET + "' -Force")
    sys.exit(1)

with open(TARGET, "r", encoding="utf-8", newline="") as f:
    after = f.read()
print("marker present:", MARKER in after)
print("call site present:", "_oj_log_retry400(resp, payload, tools)" in after)
print("APPLIED CLEAN")
