"""openjarvis-confirm-policy-v1 harness (W56, ask.py + serve.py).

Sweeps the tree for surviving auto-approve lambdas, then checks the two
files patched this round. Criterion 1 tokenizes before it judges: the
first cut of this sweep matched its OWN documentation in _stubs.py and
reported a site that does not exist. A regex cannot tell prose from code.
Exits nonzero on any FAIL.
"""
import ast, io, os, re, sys, tokenize

sys.path.insert(0, os.path.join(os.getcwd(), "src"))
ASK = os.path.join("src", "openjarvis", "cli", "ask.py")
SRV = os.path.join("src", "openjarvis", "cli", "serve.py")

results = []
def check(n, ok, detail=""):
    results.append((n, ok))
    print(("PASS " if ok else "FAIL ") + n + ("  " + detail if detail else ""))

pat = re.compile(r"confirm_callback\s*[=:]\s*.{0,20}lambda[^\n]*True")

def noncode_lines(fp):
    out = set()
    try:
        with io.open(fp, encoding="utf-8") as fh:
            for tok in tokenize.generate_tokens(fh.readline):
                if tok.type in (tokenize.COMMENT, tokenize.STRING):
                    for ln in range(tok.start[0], tok.end[0] + 1):
                        out.add(ln)
    except Exception:
        return None
    return out

# 1 tree-wide, code only
hits = []
for root, dirs, files in os.walk("src"):
    for f in files:
        if not f.endswith(".py"):
            continue
        fp = os.path.join(root, f)
        try:
            body = open(fp, encoding="utf-8", errors="replace").read()
        except OSError:
            continue
        found = [body[:m.start()].count(chr(10)) + 1 for m in pat.finditer(body)]
        if not found:
            continue
        skip = noncode_lines(fp)
        if skip is None:
            hits.append(fp + ":UNPARSEABLE")
            continue
        real = [ln for ln in found if ln not in skip]
        if real:
            hits.append("%s:%s" % (fp, real))
check("1 zero auto-approve lambdas in CODE tree-wide", not hits, str(hits))

# 2 ask.py builds a ConfirmPolicy
atext = open(ASK, encoding="utf-8").read()
atree = ast.parse(atext)
akw = []
for node in ast.walk(atree):
    if isinstance(node, ast.Assign):
        v = node.value
        if isinstance(v, ast.Call) and getattr(v.func, "id", "") == "ConfirmPolicy":
            akw.append(v)
check("2 ask.py constructs exactly one ConfirmPolicy", len(akw) == 1)

# 3 human_present=True is the distinguishing fact at this site
ok3 = False
site = ""
if akw:
    for kk in akw[0].keywords:
        if kk.arg == "human_present" and isinstance(kk.value, ast.Constant):
            ok3 = kk.value.value is True
        if kk.arg == "site" and isinstance(kk.value, ast.Constant):
            site = kk.value.value
check("3 ask.py policy is human_present=True", ok3, "site=%r" % site)

# 4 distinct site token
check("4 ask.py site token is cli-ask", site == "cli-ask")

# 5 serve.py real gate names its branch
stext = open(SRV, encoding="utf-8").read()
ast.parse(stext)
need = ["decision=DENY_NO_CONFIRM_ID", "decision=WAIT", "site=chat-agent-live"]
missing = [x for x in need if x not in stext]
check("5 serve.py gate logs all three branches", not missing, str(missing))

# 6 serve.py gate is still a REAL gate
seg = stext[stext.find("def _server_confirm_callback"):]
cut = seg.find('agent_kwargs["interactive"]')
seg = seg[:cut] if cut > 0 else seg
check("6 serve.py gate still returns the registry outcome",
      "_outcome == _cr.APPROVED" in seg and "return True" not in seg)

# 7 both modules import for real
err = ""
try:
    import importlib
    importlib.import_module("openjarvis.cli.ask")
    importlib.import_module("openjarvis.cli.serve")
    ok7 = True
except Exception as e:
    ok7, err = False, "%s: %s" % (type(e).__name__, e)
check("7 ask.py and serve.py both import", ok7, err)

n_bad = len([1 for _, ok in results if not ok])
print("")
print("RESULT %d/%d PASS" % (len(results) - n_bad, len(results)))
sys.exit(1 if n_bad else 0)
