import ast, pathlib, shutil, sys

TARGET = pathlib.Path("src/openjarvis/tools/mailbox_tools.py")
MARKER = "openjarvis-sender-discovery-v1"

OLD_A = '''                "and the largest individual messages. Reads message headers "
                "and sizes only, never message bodies. Use this to answer "
                "questions about a mailbox being full or over quota."'''

NEW_A = '''                "and the largest individual messages. Reads message headers "
                "and sizes only, never message bodies. Use this to answer "
                "questions about a mailbox being full or over quota. ALSO use "
                "this whenever the user asks WHO is sending them mail, which "
                "senders or domains are cluttering the mailbox, or asks for a "
                "list of senders to review, classify, or approve - it is the "
                "correct first call for any such question. Raise top_senders "
                "to 40 or more when the user wants a list to review. "
                "openjarvis-sender-discovery-v1"'''

OLD_B = '''                "about to move or delete specific messages and need their "
                "uids to do it."'''

NEW_B = '''                "about to move or delete specific messages and need their "
                "uids to do it. from_addr is OPTIONAL: OMIT it entirely to "
                "enumerate senders rather than confirm one. An unfiltered "
                "summary call returns by_address rows for every sender in the "
                "search window, which answers who is sending mail and how "
                "much. NEVER guess a sender name to search for - if the user "
                "has not named one, omit from_addr or call "
                "mailbox_usage_report instead."'''

src = TARGET.read_text(encoding="utf-8")
if MARKER in src:
    print("ABORT: already applied")
    sys.exit(1)
for label, old in (("A", OLD_A), ("B", OLD_B)):
    n = src.count(old)
    print("anchor", label, "matches:", n)
    if n != 1:
        print("ABORT: anchor", label, "did not match exactly once")
        sys.exit(1)
out = src.replace(OLD_A, NEW_A).replace(OLD_B, NEW_B)
ast.parse(out)
print("ast.parse OK")
bak = TARGET.with_name(TARGET.name + ".bak_senderdisc")
shutil.copy2(TARGET, bak)
TARGET.write_text(out, encoding="utf-8")
print("backup:", bak)
print("bytes:", len(src), "->", len(out))
