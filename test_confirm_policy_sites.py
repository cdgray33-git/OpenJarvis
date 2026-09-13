"""openjarvis-confirm-policy-v1 harness (W56, patch 2 of 2).

Proves the four bare lambdas in agent_manager_routes.py are gone and that
each site now constructs a real, distinctly-named ConfirmPolicy. Static on
the source plus a live import, so a syntactically valid but unimportable
module cannot pass. Exits nonzero on any FAIL.
"""
import ast, os, sys

sys.path.insert(0, os.path.join(os.getcwd(), "src"))
SRC = os.path.join("src", "openjarvis", "server", "agent_manager_routes.py")

results = []
def check(n, ok, detail=""):
    results.append((n, ok))
    print(("PASS " if ok else "FAIL ") + n + ("  " + detail if detail else ""))

text = open(SRC, encoding="utf-8").read()
tree = ast.parse(text)

# 1 no bare lambda remains anywhere in the file
check("1 zero bare lambdas remain", "lambda _prompt: True" not in text)

# 2 every confirm_callback= keyword is now a ConfirmPolicy call
kws = []
for node in ast.walk(tree):
    if isinstance(node, ast.Call):
        for k in node.keywords:
            if k.arg == "confirm_callback":
                kws.append(k.value)
bad = [k for k in kws if not (isinstance(k, ast.Call)
        and getattr(k.func, "id", "") == "ConfirmPolicy")]
check("2 all confirm_callback args are ConfirmPolicy(...)",
      len(kws) == 4 and not bad, "found=%d bad=%d" % (len(kws), len(bad)))

# 3 four distinct site tokens, each nonempty
sites = []
for k in kws:
    if isinstance(k, ast.Call):
        for kk in k.keywords:
            if kk.arg == "site" and isinstance(kk.value, ast.Constant):
                sites.append(kk.value.value)
check("3 four distinct nonempty site tokens",
      len(sites) == 4 and len(set(sites)) == 4 and all(sites),
      repr(sorted(sites)))

# 4 every site carries a reason and human_present
ok4 = True
for k in kws:
    names = {kk.arg for kk in k.keywords} if isinstance(k, ast.Call) else set()
    if not {"site", "reason", "human_present"} <= names:
        ok4 = False
check("4 every site has site+reason+human_present", ok4)

# 5 reasons are substantive, not placeholders
reasons = []
for k in kws:
    for kk in k.keywords:
        if kk.arg == "reason" and isinstance(kk.value, ast.Constant):
            reasons.append(kk.value.value)
check("5 four reasons, each over 30 chars",
      len(reasons) == 4 and all(len(r) > 30 for r in reasons),
      "lens=%s" % [len(r) for r in reasons])

# 6 the module imports for real
try:
    import importlib
    m = importlib.import_module("openjarvis.server.agent_manager_routes")
    err = ""
    ok6 = hasattr(m, "ConfirmPolicy") and hasattr(m, "create_agent_manager_router")
except Exception as e:
    ok6, err = False, "%s: %s" % (type(e).__name__, e)
check("6 module imports, ConfirmPolicy bound", ok6, err)

# 7 the bound name is the same class the executor validated
ok7 = False
if ok6:
    from openjarvis.tools._stubs import ConfirmPolicy as CP
    ok7 = m.ConfirmPolicy is CP
check("7 bound ConfirmPolicy is tools._stubs.ConfirmPolicy", ok7)

n_bad = len([1 for _, ok in results if not ok])
print("")
print("RESULT %d/%d PASS" % (len(results) - n_bad, len(results)))
sys.exit(1 if n_bad else 0)
