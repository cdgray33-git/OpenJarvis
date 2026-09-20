import io, os, re, shutil, sys, datetime, py_compile
P = r"src\openjarvis\tools\mailbox_tools.py"
src = io.open(P, encoding="utf-8", newline="").read()
if "openjarvis-find-spec-v1" in src:
    sys.exit("ALREADY APPLIED")

A1 = '''            description=(
                "Find messages in a mailbox by sender address, subject text, "
                "minimum size in bytes, or age in days. Each result includes "
                "the folder and uid needed to act on that message. Use this "
                "to build a deletion candidate list before removing anything. "
                "Defaults to detail=summary, which returns counts grouped by "
                "sender and folder and no message objects. Use detail=full "
                "only when you actually need uids."
            ),'''
B1 = '''            description=(
                "Find messages in a mailbox by sender address, subject text, "
                "minimum size in bytes, or age in days. Defaults to "
                "detail=summary, which returns counts grouped by sender and "
                "folder. Summary is a complete and authoritative answer to "
                "how many, from whom, and which folder. Do NOT call this "
                "tool a second time with detail=full to confirm or expand a "
                "count you already have. Use detail=full only when you are "
                "about to move or delete specific messages and need their "
                "uids to do it."
            ),'''

A2 = '''                        "description": (
                            "summary returns counts grouped by sender and "
                            "folder; full returns every message object "
                            "including uids"
                        ),'''
B2 = '''                        "description": (
                            "summary returns counts grouped by sender and "
                            "folder and is sufficient for every counting or "
                            "location question; full returns every message "
                            "object including uids and is only for when you "
                            "need uids to act on messages"
                        ),'''

A3 = "# openjarvis-find-summary-v1"
B3 = "# openjarvis-find-summary-v1 openjarvis-find-spec-v1"

for i, a in enumerate((A1, A2, A3), 1):
    n = src.count(a)
    if n != 1:
        sys.exit("ANCHOR %d matched %d times - ABORT" % (i, n))

out = src.replace(A1, B1).replace(A2, B2).replace(A3, B3)
ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
bak = P + ".bak-findspec-" + ts
shutil.copy2(P, bak)
tmp = P + ".cand"
io.open(tmp, "w", encoding="utf-8", newline="").write(out)
py_compile.compile(tmp, doraise=True)
os.remove(tmp)
io.open(P, "w", encoding="utf-8", newline="").write(out)
print("BACKUP", bak)
print("SIZE", len(src), "->", len(out), "delta", len(out) - len(src))
for t in ("openjarvis-find-spec-v1", "authoritative answer", "Do NOT call this",
          "sufficient for every counting"):
    print("TOKEN", t, t in out)
