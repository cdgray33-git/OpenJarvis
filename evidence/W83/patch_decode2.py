import os, sys, hashlib, time, py_compile, shutil, tempfile
from pathlib import Path
M = "openjarvis-w83-decode-v2"; root = os.getcwd()
ing = os.path.join(root, "src", "openjarvis", "tools", "storage", "ingest.py")
upr = os.path.join(root, "src", "openjarvis", "server", "upload_router.py")
ti = open(ing, "rb").read().decode("utf-8"); tu = open(upr, "rb").read().decode("utf-8")
if M in ti or M in tu: print("ALREADY PATCHED - no change"); sys.exit(0)
nl = "\r\n" if "\r\n" in ti else "\n"; nu = "\r\n" if "\r\n" in tu else "\n"
a1 = "from openjarvis.tools.storage.chunking import Chunk, ChunkConfig, chunk_text" + nl
a2 = nl.join(['def _read_text(path: Path) -> str:', '    """Read a text file with UTF-8, falling back to latin-1."""', '    try:', '        return path.read_text(encoding="utf-8")', '    except UnicodeDecodeError:', '        return path.read_text(encoding="latin-1")']) + nl
a3 = "# --- openjarvis-w83-decode-v1 ---"
c = (ti.count(a1), ti.count(a2), tu.count(a3)); print("ANCHORS a1=%d a2=%d a3=%d (want 1 1 1) nl_ing=%r nl_upr=%r" % (c + (nl, nu)))
if c != (1, 1, 1) or "def _oj_decode_text" not in tu[tu.index(a3):]: print("ABORT - anchors, nothing written"); sys.exit(1)
ti = ti.replace(a1, a1 + nl + "import logging" + nl + nl + "logger = logging.getLogger(__name__)" + nl)
helper = [
"# " + M + " (D-29): ONE decoder for both ingest paths (this file and server/upload_router.py).",
"# Author defect: utf-8 then latin-1. latin-1 never fails, so UTF-16 text was stored as char+NUL and binaries were",
"# accepted as text. BOM first, then utf-8, then latin-1; refuse results still >10% NUL (returns None).",
"def decode_text_bytes(data: bytes, name: str = \"\") -> Optional[str]:",
"    enc = None",
"    try:",
"        if data[:3] == b\"\\xef\\xbb\\xbf\":",
"            text, enc = data[3:].decode(\"utf-8\", errors=\"replace\"), \"utf-8-sig\"",
"        elif data[:2] in (b\"\\xff\\xfe\", b\"\\xfe\\xff\"):",
"            text, enc = data.decode(\"utf-16\"), \"utf-16\"",
"    except UnicodeDecodeError:",
"        enc = None",
"    if enc is None:",
"        try:",
"            text, enc = data.decode(\"utf-8\"), \"utf-8\"",
"        except UnicodeDecodeError:",
"            text, enc = data.decode(\"latin-1\"), \"latin-1\"",
"    nul = text.count(\"\\x00\")",
"    if text and nul * 10 > len(text):",
"        logger.warning(\"DECODE refused %s: %d of %d chars NUL after %s decode - not stored\", name, nul, len(text), enc)",
"        return None",
"    logger.info(\"DECODE %s as %s chars=%d\", name, enc, len(text))",
"    return text",
"",
"",
"def _read_text(path: Path) -> str:",
"    \"\"\"Read a text file through decode_text_bytes; refused content raises OSError (walker skips it).\"\"\"",
"    text = decode_text_bytes(path.read_bytes(), str(path))",
"    if text is None:",
"        raise OSError(\"refused undecodable file: %s\" % path)",
"    return text"]
ti = ti.replace(a2, nl.join(helper) + nl)
i = tu.index(a3)
tu = tu[:i] + nu.join(["# --- " + M + " --- (was openjarvis-w83-decode-v1; single implementation now in tools/storage/ingest.py)",
                        "from openjarvis.tools.storage.ingest import decode_text_bytes as _oj_decode_text  # noqa: E402", ""])
bdir = os.path.join(root, "evidence", "W83", "backup"); ts = time.strftime("%Y%m%d_%H%M%S")
for p in (ing, upr): shutil.copy2(p, os.path.join(bdir, os.path.basename(p) + ".bak-W83-decode2-" + ts)); print("BACKUP", os.path.basename(p) + ".bak-W83-decode2-" + ts)
for p, t in ((ing, ti), (upr, tu)):
    compile(t, p, "exec"); open(p, "wb").write(t.encode("utf-8")); py_compile.compile(p, doraise=True)
    b = open(p, "rb").read(); print("AFTER %-17s sha256=%s bytes=%d marker=%d" % (os.path.basename(p), hashlib.sha256(b).hexdigest().upper()[:16], len(b), b.decode("utf-8").count(M)))
from openjarvis.tools.storage.ingest import decode_text_bytes as D, read_document, ingest_path
from openjarvis.server.upload_router import _oj_decode_text as U
s = "ollama remote host line\r\n"
print("U1", D(b"\xff\xfe" + s.encode("utf-16-le"), "u1") == s, "U2", D(b"\xef\xbb\xbf" + s.encode(), "u2") == s, "U3", D(s.encode(), "u3") == s,
      "U4", D("caf\xe9".encode("latin-1"), "u4") == "caf\xe9", "U5", D(s.encode("utf-16-le"), "u5") is None)
print("S1 upload_router uses shared helper", U is D)
d = Path(tempfile.mkdtemp()); note = " ".join("word%d" % k for k in range(60))
(d / "note.txt").write_bytes(b"\xff\xfe" + note.encode("utf-16-le")); (d / "lib.rlib").write_bytes(bytes(range(256)) * 20)
t1, _ = read_document(d / "note.txt"); print("I1 read_document utf16 clean", t1 == note)
ch = ingest_path(d); srcs = sorted(set(Path(x.source).name for x in ch))
print("I2 ingest_path chunks=%d sources=%s nul=%d PASS=%s" % (len(ch), srcs, sum(x.content.count("\x00") for x in ch), srcs == ["note.txt"] and all("\x00" not in x.content for x in ch)))
shutil.rmtree(d)
