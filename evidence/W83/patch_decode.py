import os, sys, hashlib, time, py_compile, shutil
MARK = "openjarvis-w83-decode-v1"
p = os.path.join(os.getcwd(), "src", "openjarvis", "server", "upload_router.py")
raw = open(p, "rb").read(); t = raw.decode("utf-8")
print("BEFORE sha256", hashlib.sha256(raw).hexdigest().upper(), len(raw), "bytes")
if MARK in t: print("ALREADY PATCHED - no change"); sys.exit(0)
nl = "\r\n" if "\r\n" in t else "\n"
old = nl.join(['        try:', '            text = data.decode("utf-8")', '        except UnicodeDecodeError:', '            text = data.decode("latin-1")']) + nl
n = t.count(old); print("ANCHOR count=%d (want 1) newline=%r" % (n, nl))
if n != 1: print("ABORT - anchor mismatch, nothing written"); sys.exit(1)
new = nl.join(['        text = _oj_decode_text(data, filename)  # ' + MARK, '        if text is None:', '            return']) + nl
t = t.replace(old, new)
helper = ["", "", "# --- " + MARK + " ---",
"# Author defect (af21bc18 upload_router.py:182-184): utf-8 then latin-1. A UTF-16 file (PowerShell 5.1 '>' output,",
"# many Windows exports) fails utf-8, and latin-1 never fails, so each char is stored followed by NUL: unsearchable.",
"# Fix: BOM first, then utf-8, then latin-1; refuse text still >10% NUL (binary or BOM-less UTF-16).",
"def _oj_decode_text(data, filename):",
"    enc = None",
"    try:",
"        if data[:3] == b'\\xef\\xbb\\xbf':",
"            text, enc = data[3:].decode('utf-8', errors='replace'), 'utf-8-sig'",
"        elif data[:2] in (b'\\xff\\xfe', b'\\xfe\\xff'):",
"            text, enc = data.decode('utf-16'), 'utf-16'",
"    except UnicodeDecodeError:",
"        enc = None",
"    if enc is None:",
"        try:",
"            text, enc = data.decode('utf-8'), 'utf-8'",
"        except UnicodeDecodeError:",
"            text, enc = data.decode('latin-1'), 'latin-1'",
"    nul = text.count('\\x00')",
"    if text and nul * 10 > len(text):",
"        logger.warning('DECODE refused %s: %d of %d chars NUL after %s decode - not stored', filename, nul, len(text), enc)",
"        return None",
"    logger.info('DECODE %s as %s chars=%d', filename, enc, len(text))",
"    return text", ""]
t = t.rstrip("\r\n") + nl + nl.join(helper)
bdir = os.path.join(os.getcwd(), "evidence", "W83", "backup"); os.makedirs(bdir, exist_ok=True)
bak = os.path.join(bdir, "upload_router.py.bak-W83-decode-" + time.strftime("%Y%m%d_%H%M%S"))
shutil.copy2(p, bak); print("BACKUP", bak)
compile(t, p, "exec"); open(p, "wb").write(t.encode("utf-8")); py_compile.compile(p, doraise=True)
new_raw = open(p, "rb").read()
print("AFTER  sha256", hashlib.sha256(new_raw).hexdigest().upper(), len(new_raw), "bytes  marker_count=%d" % new_raw.decode("utf-8").count(MARK))
from openjarvis.server.upload_router import _oj_decode_text as D
s = "ollama remote host line\r\n"
print("U1 utf16", D(b"\xff\xfe" + s.encode("utf-16-le"), "u1") == s)
print("U2 utf8sig", D(b"\xef\xbb\xbf" + s.encode("utf-8"), "u2") == s)
print("U3 utf8", D(s.encode("utf-8"), "u3") == s)
print("U4 latin1", D("caf\xe9".encode("latin-1"), "u4") == "caf\xe9")
print("U5 nul-junk refused", D(s.encode("utf-16-le"), "u5") is None)
