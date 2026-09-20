import ast, pathlib, shutil, sys

TARGET = pathlib.Path("src/openjarvis/tools/mailbox_tools.py")
MARKER = "openjarvis-account-resolve-v1"

OLD = '''    if account:
        return account
    accounts = [a["account"] for a in list_accounts() if a["configured"]]
    if len(accounts) == 1:
        return accounts[0]
    return ""
'''

NEW = '''    # openjarvis-account-resolve-v1: validate the id against configured
    # accounts. Never pass an unknown id through as if it resolved, and
    # accept the account email as an alias for the id (Defect 6).
    configured = [a for a in list_accounts() if a["configured"]]
    if account:
        needle = account.strip().lower()
        for a in configured:
            if a["account"].lower() == needle:
                return a["account"]
        for a in configured:
            email = (a.get("email") or "").lower()
            if email and email == needle:
                return a["account"]
        return ""
    if len(configured) == 1:
        return configured[0]["account"]
    return ""
'''

src = TARGET.read_text(encoding="utf-8")
if MARKER in src:
    print("ABORT: already applied")
    sys.exit(1)
n = src.count(OLD)
print("anchor matches:", n)
if n != 1:
    print("ABORT: anchor did not match exactly once")
    sys.exit(1)
out = src.replace(OLD, NEW)
ast.parse(out)
print("ast.parse OK")
bak = TARGET.with_name(TARGET.name + ".bak_acctresolve")
shutil.copy2(TARGET, bak)
TARGET.write_text(out, encoding="utf-8")
print("backup:", bak)
print("bytes:", len(src), "->", len(out))
