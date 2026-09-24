import hashlib, pathlib, py_compile, shutil, sys, time
ROOT = pathlib.Path(r"C:\Users\Admin\OpenJarvis"); F = ROOT / r"src\openjarvis\server\speech_router.py"
BK = ROOT / r"evidence\W82\backup"; BK.mkdir(parents=True, exist_ok=True)
raw = F.read_bytes(); bom = raw.startswith(b"\xef\xbb\xbf"); crlf = raw.count(b"\r\n"); lf = raw.count(b"\n") - crlf
bak = BK / ("speech_router.py.bak-W82-H5-" + time.strftime("%Y%m%d_%H%M%S")); shutil.copy2(F, bak)
print("BACKUP", bak); print("BEFORE sha256", hashlib.sha256(raw).hexdigest()[:16], "bytes", len(raw), "BOM", bom, "CRLF", crlf, "LF", lf)
t = raw.decode("utf-8-sig") if bom else raw.decode("utf-8")
def once(s):
    n = t.count(s)
    if n != 1: sys.exit(f"ABORT anchor count {n} for {s!r}")
    return t.index(s)
nl = "\r\n" if crlf > lf else "\n"
MARK = "# openjarvis-w82-h5-author-speech-routes-v1: /transcribe and /health removed here (W82, owner-approved A1)." + nl + "# The author's routes in api_routes.py (speech_router, include_all_routes) now serve them." + nl + nl
a = once('@speech_router.post("/transcribe")'); b = once("# --- Remote TTS Backend")
if not a < b: sys.exit("ABORT transcribe anchors out of order")
t = t[:a] + MARK + t[b:]
h = once('@speech_router.get("/health")'); e = t.index("# Silero VAD + Whisper Streaming WS", h)
t = t[:h] + t[e:]
out = t.encode("utf-8"); out = (b"\xef\xbb\xbf" + out) if bom else out
F.write_bytes(out)
crlf2 = out.count(b"\r\n"); lf2 = out.count(b"\n") - crlf2
print("AFTER  sha256", hashlib.sha256(out).hexdigest()[:16], "bytes", len(out), "BOM", out.startswith(b"\xef\xbb\xbf"), "CRLF", crlf2, "LF", lf2)
def restore(msg):
    shutil.copy2(bak, F); sys.exit("RESTORED BACKUP - " + msg)
try:
    py_compile.compile(str(F), doraise=True); print("py_compile OK")
except Exception as ex:
    restore(f"compile failed {ex}")
sys.path.insert(0, str(ROOT / "src"))
try:
    from openjarvis.server import speech_router as sr
    from openjarvis.server import api_routes as ar
except Exception as ex:
    restore(f"import failed {ex!r}")
ours = sorted({(getattr(r, "path", ""), ",".join(sorted(getattr(r, "methods", None) or ["WS"]))) for r in sr.speech_router.routes})
auth = sorted({(getattr(r, "path", ""), ",".join(sorted(getattr(r, "methods", None) or ["WS"]))) for r in ar.speech_router.routes})
print("OURS  ", ours); print("AUTHOR", auth)
op = [p for p, _ in ours]
checks = {"ours has no /transcribe": "/v1/speech/transcribe" not in op, "ours has no /health": "/v1/speech/health" not in op,
          "ours keeps /synthesize": "/v1/speech/synthesize" in op,
          "author has /transcribe": any(p == "/v1/speech/transcribe" for p, _ in auth), "author has /health": any(p == "/v1/speech/health" for p, _ in auth),
          "mic dump gone": "MIC CAPTURE" not in t, "marker present": "openjarvis-w82-h5-author-speech-routes-v1" in t}
for k, v in checks.items(): print(("PASS " if v else "FAIL ") + k)
if not all(checks.values()): restore("a check failed")
print("OVERALL PASS - patch applied, NOT restarted, NOT committed")
