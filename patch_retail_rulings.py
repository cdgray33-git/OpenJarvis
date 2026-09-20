import datetime, os, py_compile, shutil, sys, tempfile
T = "move_retail.py"
M = "openjarvis-retail-rulings-v1"
E = [
 ("groupon notify held",
  '    "otp@r.groupon.com",',
  '    "otp@r.groupon.com",\n    "notify@r.groupon.com",'),
 ("stackcommerce removed",
  '    "stackcommerce.com",\n',
  ''),
]
apply = "--apply" in sys.argv
if not os.path.isfile(T):
    print("ABORT: %s not found. Run from repo root." % T); raise SystemExit(2)
src = open(T, encoding="utf-8", newline="").read()
eol = "\r\n" if "\r\n" in src else "\n"
print("target   : %s" % T); print("size     : %d bytes" % len(src.encode("utf-8")))
print("eol      : %s" % ("CRLF" if eol == "\r\n" else "LF"))
if M in src:
    print("ABORT: already patched."); raise SystemExit(0)
if "EXCLUDED_ADDRS" not in src:
    print("ABORT: control pattern missing. Wrong file?"); raise SystemExit(2)
flat = src.replace("\r\n", "\n")
for lab, old, _n in E:
    c = flat.count(old); print("anchor   : %-22s matches=%d" % (lab, c))
    if c != 1:
        print("ABORT: anchor '%s' matched %d, expected 1." % (lab, c)); raise SystemExit(2)
out = flat
for _l, old, new in E:
    out = out.replace(old, new, 1)
out = out.replace("EXCLUDED_ADDRS", "# " + M + "\nEXCLUDED_ADDRS", 1)
if eol == "\r\n":
    out = out.replace("\n", "\r\n")
print("post     : %d bytes (delta %+d)" % (len(out.encode("utf-8")), len(out.encode("utf-8")) - len(src.encode("utf-8"))))
t = tempfile.NamedTemporaryFile("w", suffix=".py", delete=False, encoding="utf-8", newline="")
t.write(out); t.close()
try:
    py_compile.compile(t.name, doraise=True); print("compile  : OK")
except Exception as e:
    print("ABORT: candidate failed to compile: %s" % e); raise SystemExit(2)
finally:
    os.unlink(t.name)
if not apply:
    print(""); print("DRY RUN. Both anchors matched and the result compiles.")
    print("Re-run with --apply to write."); raise SystemExit(0)
b = "%s.bak-rulings-%s" % (T, datetime.datetime.now().strftime("%Y%m%d_%H%M%S"))
shutil.copy2(T, b); print("backup   : %s" % b)
open(T, "w", encoding="utf-8", newline="").write(out)
try:
    py_compile.compile(T, doraise=True)
except Exception as e:
    shutil.copy2(b, T); print("ABORT: post-write compile failed, REVERTED. %s" % e); raise SystemExit(2)
chk = open(T, encoding="utf-8").read()
if M not in chk or "notify@r.groupon.com" not in chk or "stackcommerce" in chk:
    shutil.copy2(b, T); print("ABORT: verify failed, REVERTED."); raise SystemExit(2)
print("APPLIED  : OK")
print("REVERT   : Copy-Item '%s' '%s' -Force" % (b, T))
