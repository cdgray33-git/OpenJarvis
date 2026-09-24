import os, sys, shutil, tempfile, py_compile, hashlib
from pathlib import Path
p = os.path.join(os.getcwd(), "src", "openjarvis", "tools", "storage", "ingest.py")
t = open(p, "rb").read().decode("utf-8")
e = [('    if text and nul * 10 > len(text):',
      '    ctl = sum(1 for ch in text if ord(ch) < 32 and ch not in "\\t\\n\\r\\f\\v")\n    if text and (nul > 0 or ctl * 20 > len(text)):'),
     ('        logger.warning("DECODE refused %s: %d of %d chars NUL after %s decode - not stored", name, nul, len(text), enc)',
      '        logger.warning("DECODE refused %s: nul=%d ctl=%d of %d chars after %s decode - not stored", name, nul, ctl, len(text), enc)'),
     ('# accepted as text. BOM first, then utf-8, then latin-1; refuse results still >10% NUL (returns None).',
      '# accepted as text. BOM first, then utf-8, then latin-1; refuse any NUL or >5% control chars (returns None).')]
cnt = [t.count(a) for a, _ in e]; print("ANCHORS", cnt, "(want [1, 1, 1])")
if cnt != [1, 1, 1]: print("ABORT - nothing written"); sys.exit(1)
for a, b in e: t = t.replace(a, b)
compile(t, p, "exec"); open(p, "wb").write(t.encode("utf-8")); py_compile.compile(p, doraise=True)
print("AFTER ingest.py sha256=%s bytes=%d" % (hashlib.sha256(t.encode()).hexdigest().upper()[:16], len(t.encode())))
from openjarvis.tools.storage.ingest import decode_text_bytes as D, read_document, ingest_path
from openjarvis.server.upload_router import _oj_decode_text as U
s = "ollama remote host line\r\n"
print("U1", D(b"\xff\xfe" + s.encode("utf-16-le"), "u1") == s, "U2", D(b"\xef\xbb\xbf" + s.encode(), "u2") == s, "U3", D(s.encode(), "u3") == s,
      "U4", D("caf\xe9".encode("latin-1"), "u4") == "caf\xe9", "U5", D(s.encode("utf-16-le"), "u5") is None, "U6 tabs/newlines ok", D(b"a\tb\r\nc\n", "u6") == "a\tb\r\nc\n")
print("S1 upload_router uses shared helper", U is D)
d = Path(tempfile.mkdtemp()); note = " ".join("word%d" % k for k in range(60))
(d / "note.txt").write_bytes(b"\xff\xfe" + note.encode("utf-16-le")); (d / "lib.rlib").write_bytes(bytes(range(256)) * 20)
(d / "nonul.bin").write_bytes(bytes(range(1, 32)) * 40 + b"abc")
t1, _ = read_document(d / "note.txt"); print("I1 read_document utf16 clean", t1 == note)
ch = ingest_path(d); srcs = sorted(set(Path(x.source).name for x in ch))
print("I2 ingest_path chunks=%d sources=%s nul=%d PASS=%s" % (len(ch), srcs, sum(x.content.count("\x00") for x in ch), srcs == ["note.txt"] and all("\x00" not in x.content for x in ch)))
shutil.rmtree(d)
