"""patch_find_window.py - marker openjarvis-find-window-v1

Makes mailbox_find_messages state that every count is windowed by the
IMAP server (newest ~10,000 per folder), not a mailbox total.
Guarded: refuses unless both anchors are present exactly once.
"""
import ast, pathlib, shutil, sys

MARKER = "openjarvis-find-window-v1"
P = pathlib.Path("src/openjarvis/tools/mailbox_tools.py")

A1 = '            "by_folder": sorted(by_folder.values(), key=lambda r: -r["count"]),\n        }\n'
A2 = ('            "by_folder": sorted(by_folder.values(), key=lambda r: -r["count"]),\n'
      '            "coverage": "newest ~10000 per folder (IMAP server window)",  # ' + MARKER + '\n'
      '        }\n')

B1 = ('        if truncated:\n'
      '            payload["note"] = (\n'
      '                "RESULT TRUNCATED AT THE LIMIT. match_count is a FLOOR, not a "\n'
      '                "total. Tell the user the true number is at least this many and "\n'
      '                "is not yet known, and re-run with a higher limit before acting."\n'
      '            )\n')

B2 = ('        notes = [\n'
      '            "COUNTS ARE WINDOWED. The mail server exposes only the newest "\n'
      '            "~10,000 messages per folder and does not index past them. "\n'
      '            "match_count is therefore a FLOOR within that window and is NEVER "\n'
      '            "a mailbox total. When reporting a count, say plainly that it "\n'
      '            "covers only the most recent mail the server exposes. Do not claim "\n'
      '            "all matching mail was found, moved, or deleted."\n'
      '        ]\n'
      '        if truncated:\n'
      '            notes.append(\n'
      '                "RESULT ALSO TRUNCATED AT THE RESULT LIMIT, below even the "\n'
      '                "server window. Re-run with a higher limit before acting."\n'
      '            )\n'
      '        payload["note"] = " ".join(notes)\n')

def die(m):
    print("REFUSED: " + m); sys.exit(1)

if not P.exists(): die("file not found: %s" % P)
src = P.read_text(encoding="utf-8")
if MARKER in src: die("already patched")
for name, a in (("A1", A1), ("B1", B1)):
    n = src.count(a)
    if n != 1: die("anchor %s found %d times, expected 1" % (name, n))

new = src.replace(A1, A2).replace(B1, B2)
try:
    ast.parse(new)
except SyntaxError as e:
    die("patched source does not parse: %s" % e)

bak = P.with_suffix(P.suffix + ".bak_findwindow")
if bak.exists(): die("backup already exists: %s" % bak)
shutil.copy2(P, bak)
P.write_text(new, encoding="utf-8")
print("PATCHED %s" % P)
print("BACKUP  %s" % bak)
print("ROLLBACK: Copy-Item -Force %s %s" % (bak, P))
