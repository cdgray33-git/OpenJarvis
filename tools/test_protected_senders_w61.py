#!/usr/bin/env python3
"""W61 harness - openjarvis-protected-senders-v2 (mailbox_tools.py).

Non-interactive. No IMAP: the move tool is driven through a fake
connector. The loader is pointed at temp files; the REAL per-user file is
only READ, in the LIVE check. dispatch.log is redirected to a temp dir
before any openjarvis import. Supersedes scenario E of
tests/probe_h3_protected_v1.py, which assumes the old CWD location.

Run from the repo root with the .venv python. Exits nonzero on any FAIL.
"""
import ast
import json
import logging
import os
import sys
import tempfile
from pathlib import Path

TMP = Path(tempfile.mkdtemp(prefix="w61prot_"))
os.environ["LOCALAPPDATA"] = str(TMP)
sys.path.insert(0, os.path.join(os.getcwd(), "src"))
MTP = os.path.join("src", "openjarvis", "tools", "mailbox_tools.py")

results = []


def check(n, ok, detail=""):
    results.append((n, bool(ok)))
    print(("PASS " if ok else "FAIL ") + n + ("  " + detail if detail else ""))


# ---------------------------------------------------------------- static --
src = open(MTP, encoding="utf-8-sig").read()
tree = ast.parse(src)
cwd_calls = [n for n in ast.walk(tree)
             if isinstance(n, ast.Attribute) and n.attr == "cwd"]
check("01 mailbox_tools.py has no .cwd() in code", not cwd_calls,
      "found %d" % len(cwd_calls))
check("02 v2 marker present, v1 marker gone",
      "openjarvis-protected-senders-v2" in src
      and "openjarvis-protected-senders-v1" not in src)
site = src.count("_prot = _load_protected_senders()")
check("03 move tool calls the loader exactly once", site == 1,
      "found %d" % site)

try:
    import openjarvis.tools.mailbox_tools as mt
    from openjarvis.core.config import DEFAULT_CONFIG_DIR
    ok4, err = True, ""
except Exception as e:
    ok4, err = False, "%s: %s" % (type(e).__name__, e)
check("04 mailbox_tools imports", ok4, err)
if not ok4:
    print("\nRESULT %d/%d PASS" % (sum(1 for _, o in results if o),
                                   len(results)))
    sys.exit(1)

REAL = mt.PROTECTED_SENDERS_PATH
check("05 path is DEFAULT_CONFIG_DIR/protected_senders.json",
      REAL == Path(DEFAULT_CONFIG_DIR) / "protected_senders.json",
      str(REAL))
dflt = [d.lower() for d in mt._PROTECTED_DEFAULTS]
check("06 defaults lifted (10 entries, stackcommerce first)",
      len(dflt) == 10 and dflt[0] == "stackcommerce.com", str(len(dflt)))


# ------------------------------------------------------------ behavioral --
class Grab(logging.Handler):
    def __init__(self):
        super().__init__(logging.DEBUG)
        self.lines = []

    def emit(self, record):
        self.lines.append((record.levelno, record.getMessage()))


grab = Grab()
mt.logger.addHandler(grab)
mt.logger.setLevel(logging.DEBUG)


def load_with(content, name):
    """content: None = missing; bytes = written verbatim."""
    p = TMP / name
    if content is not None:
        p.write_bytes(content)
    mt.PROTECTED_SENDERS_PATH = p
    grab.lines.clear()
    try:
        return mt._load_protected_senders(), list(grab.lines)
    finally:
        mt.PROTECTED_SENDERS_PATH = REAL


def has(lines, text, level=None):
    return any(text in m and (level is None or lv == level)
               for lv, m in lines)


W, E, I = logging.WARNING, logging.ERROR, logging.INFO
CASES = [
    ("missing", None, dflt, "reason=missing", W),
    ("valid", b'[" Foo.com ", "bar@"]', ["foo.com", "bar@"],
     "source=file", I),
    ("bom", b'\xef\xbb\xbf["x.com"]', ["x.com"], "bom_stripped", W),
    ("notlist", b'{"a": 1}', dflt, "reason=not_a_list", W),
    ("empty", b"[]", dflt, "reason=no_usable_entries", W),
    ("allblank", b'["  ", ""]', dflt, "reason=no_usable_entries", W),
    ("garbage", b"{not json", dflt, "reason=unparseable", E),
    ("mixed", b'[1, null, "y.com"]', ["y.com"], "dropped=2", W),
]
n = 7
for label, content, want, token, level in CASES:
    got, lines = load_with(content, "c_%s.json" % label)
    ok = got == want and has(lines, token, level) and len(got) > 0
    check("%02d loader %-8s -> %s" % (n, label, token), ok,
          "got=%d entries logged=%s" % (len(got), has(lines, token, level)))
    n += 1

# LIVE: the real per-user file, read only.
grab.lines.clear()
live = mt._load_protected_senders()
check("%02d LIVE %s loads from file" % (n, REAL),
      REAL.is_file() and has(grab.lines, "source=file", I) and live,
      "exists=%s entries=%d" % (REAL.is_file(), len(live)))
n += 1


# --------------------------------------- end-to-end through the move tool --
class FakeConn:
    def __init__(self, hits):
        self.hits = hits
        self.moved = []

    def find_messages(self, **kw):
        return list(self.hits)

    def move_to_trash(self, folder, uids, dry_run=True):
        self.moved.append((folder, list(uids), dry_run))
        return {"dry_run": dry_run, "count": len(uids)}


HITS = [
    {"uid": "1", "folder": "Inbox", "from_addr": "deals@protected.com"},
    {"uid": "2", "folder": "Inbox", "from_addr": "spam@other.com"},
    {"uid": "3", "folder": "Inbox", "from_addr": "cdgray33@yahoo.com"},
]


def run_move(list_bytes, hits):
    p = TMP / "e2e.json"
    p.write_bytes(list_bytes)
    fake = FakeConn(hits)
    saved = mt.connector_for
    mt.PROTECTED_SENDERS_PATH = p
    mt.connector_for = lambda account="": fake
    try:
        res = mt.MailboxMoveToTrashTool().execute(
            folder="Inbox", from_addr="x", dry_run=True)
    finally:
        mt.connector_for = saved
        mt.PROTECTED_SENDERS_PATH = REAL
    return fake, res


fake, res = run_move(b'["protected.com"]', HITS)
got = fake.moved[0][1] if fake.moved else None
check("%02d e2e file list: protected.com held back, dry run only" % n,
      got == ["2", "3"] and fake.moved[0][2] is True,
      "uids=%s" % got)
n += 1

fake, res = run_move(b'["  "]', HITS)
got = fake.moved[0][1] if fake.moved else None
check("%02d e2e all-blank list: DEFAULTS apply (v1 failed open here)" % n,
      got == ["1", "2"],
      "uids=%s (cdgray33@yahoo.com must be held back)" % got)
n += 1

fake, res = run_move(b'["protected.com", "other.com", "yahoo.com"]', HITS)
body = json.loads(res.content) if res.content else {}
check("%02d e2e everything protected: nothing moved, error returned" % n,
      not fake.moved and not res.success
      and "protected_blocked" in body,
      "moved=%s success=%s" % (fake.moved, res.success))
n += 1

dlog = TMP / "OpenJarvis" / "logs" / "dispatch.log"
dtext = dlog.read_text(encoding="utf-8") if dlog.is_file() else ""
check("%02d PROTECTED lines also land in (temp) dispatch.log" % n,
      "PROTECTED source=file" in dtext and "reason=missing" in dtext,
      str(dlog))
n += 1

bad = [k for k, ok in results if not ok]
print("")
print("RESULT %d/%d PASS" % (len(results) - len(bad), len(results)))
sys.exit(1 if bad else 0)
