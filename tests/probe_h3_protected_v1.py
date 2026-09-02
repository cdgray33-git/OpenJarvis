#!/usr/bin/env python
# openjarvis-h3-protected-v1
# Exercises the protected-sender guard in MailboxMoveToTrashTool.
#
# RUN FROM THE REPO ROOT:  python .\tests\probe_h3_protected_v1.py
#
# REAL:  the whole MailboxMoveToTrashTool.execute body, the real guard at
#        mailbox_tools.py:563-612, the real uid typeguard, the real _confirmed.
# FAKE:  only the object returned by connector_for(). find_messages and
#        move_to_trash are stubs that record what they were asked to do.
#
# Stdlib only. No sockets. No mailbox. No writes to the tree except an
# optional protected_senders.json in CWD for scenario E, which is refused
# if the file already exists and is removed in a finally block.

import json
import os
import sys
import traceback

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SRC = os.path.join(ROOT, "src")
if os.path.isdir(SRC) and SRC not in sys.path:
    sys.path.insert(0, SRC)

try:
    from openjarvis.tools import mailbox_tools as MT
except Exception:
    print("IMPORT FAILED - are you running from the repo root?")
    traceback.print_exc()
    sys.exit(2)

TOKEN = MT.CONFIRM_TOKEN

# ---------------------------------------------------------------- fake conn

class FakeConn(object):
    """Records what the tool asked it to do. Never touches a network."""

    def __init__(self, hits):
        self._hits = hits
        self.calls = []            # every method the tool invoked, in order
        self.moved_uids = None     # uid list handed to a REAL (dry_run=False) move

    def find_messages(self, folder=None, from_addr=None, limit=None):
        self.calls.append(
            "find_messages(folder=%r, from_addr=%r, limit=%r)"
            % (folder, from_addr, limit)
        )
        return [h for h in self._hits if h.get("folder") == folder]

    def move_to_trash(self, folder, uids, dry_run=True):
        self.calls.append(
            "move_to_trash(folder=%r, uids=%r, dry_run=%r)" % (folder, list(uids), dry_run)
        )
        if not dry_run:
            self.moved_uids = list(uids)
        # The tool derives success from the W29 four-state contract at
        # mailbox_tools.py:686-735, NOT from "applied". A fake that omits
        # copied_count/deleted_count reports _outcome="no_op" and the tool
        # correctly returns success=False. The fake must satisfy the real
        # CONSUMER of its return value, not just the caller's signature.
        return {
            "applied": not dry_run,
            "moved": len(uids),
            "folder": folder,
            "uids": list(uids),
            "copied_count": len(uids),
            "deleted_count": len(uids),
            "failed_uids": [],
            "store_failed": [],
        }


def hit(uid, addr, folder="INBOX"):
    return {"uid": str(uid), "from_addr": addr, "folder": folder, "subject": "x"}


# ------------------------------------------------------------------- runner

def run(name, hits, params, expect):
    """Execute the real tool against a fake connector and grade the result."""
    conn = FakeConn(hits)
    orig = MT.connector_for
    MT.connector_for = lambda account: conn
    try:
        tool = MT.MailboxMoveToTrashTool()
        res = tool.execute(**params)
    finally:
        MT.connector_for = orig

    try:
        payload = json.loads(res.content)
    except Exception:
        payload = {"__unparsed__": str(res.content)}

    ok = True
    notes = []

    if res.success != expect["success"]:
        ok = False
        notes.append("success=%r want=%r" % (res.success, expect["success"]))

    # Did the connector actually get told to move, and with WHICH uids?
    if conn.moved_uids != expect["moved_uids"]:
        ok = False
        notes.append("moved_uids=%r want=%r" % (conn.moved_uids, expect["moved_uids"]))

    # Presence, not truthiness. W30 5.4.
    present = "protected_blocked" in payload
    if present != expect["blocked_present"]:
        ok = False
        notes.append(
            "protected_blocked present=%r want=%r" % (present, expect["blocked_present"])
        )
    if expect["blocked_present"] and present:
        if not payload.get("protected_blocked"):
            ok = False
            notes.append("protected_blocked present but EMPTY")

    print("--- %s : %s" % (name, "PASS" if ok else "FAIL"))
    print("    params        : %r" % (params,))
    print("    success       : %r" % (res.success,))
    print("    moved_uids    : %r" % (conn.moved_uids,))
    print("    blocked       : present=%r value=%r"
          % (present, payload.get("protected_blocked")))
    print("    selected_by   : present=%r" % ("selected_by" in payload,))
    print("    error         : %r" % (payload.get("error"),))
    print("    CONNECTOR WAS ASKED:")
    for c in conn.calls:
        print("      - %s" % c)
    if notes:
        for n in notes:
            print("    MISMATCH: %s" % n)
    print("")
    return ok


# ---------------------------------------------------------------- scenarios

def main():
    results = []

    base = dict(account="", folder="INBOX", dry_run=False, confirm=TOKEN)

    # A: every hit is a protected sender. Nothing may be moved at all.
    p = dict(base); p["from_addr"] = "groupon"
    results.append(run(
        "A  from_addr, ALL protected",
        [hit(11, "notify@r.groupon.com"), hit(12, "orders@r.groupon.com")],
        p,
        dict(success=False, moved_uids=None, blocked_present=True),
    ))

    # B: mixed. Only the clean uids may reach the connector.
    p = dict(base); p["from_addr"] = "@"
    results.append(run(
        "B  from_addr, MIXED - guard must filter",
        [hit(21, "notify@r.groupon.com"), hit(22, "sales@example.com"),
         hit(23, "cdgray33@yahoo.com"), hit(24, "news@example.org")],
        p,
        dict(success=True, moved_uids=["22", "24"], blocked_present=True),
    ))

    # C: none protected. protected_blocked must be ABSENT, not empty.
    p = dict(base); p["from_addr"] = "example"
    results.append(run(
        "C  from_addr, NONE protected",
        [hit(31, "sales@example.com"), hit(32, "news@example.org")],
        p,
        dict(success=True, moved_uids=["31", "32"], blocked_present=False),
    ))

    # D: BYPASS PROBE. uids passed directly, belonging to a protected sender.
    #    Expectation is written to CURRENT behaviour: the guard is skipped.
    #    If this scenario ever FAILS, the bypass has been closed.
    p = dict(base); p["uids"] = ["41", "42"]
    results.append(run(
        "D  uids direct, protected sender - BYPASS PROBE",
        [hit(41, "notify@r.groupon.com"), hit(42, "cdgray33@yahoo.com")],
        p,
        dict(success=True, moved_uids=["41", "42"], blocked_present=False),
    ))

    # E: does protected_senders.json in CWD actually load?
    pf = os.path.join(os.getcwd(), "protected_senders.json")
    if os.path.exists(pf):
        print("--- E  override load : SKIPPED")
        print("    %s already exists. Refusing to touch it." % pf)
        print("")
    else:
        try:
            with open(pf, "w") as fh:
                fh.write(json.dumps(["ONLYTHIS@example.net"]))
            # groupon is in the BUILT-IN list but NOT in the override.
            # If the override loaded, groupon is no longer protected.
            p = dict(base); p["from_addr"] = "@"
            results.append(run(
                "E  override file present - built-in list must be REPLACED",
                [hit(51, "notify@r.groupon.com"), hit(52, "ONLYTHIS@example.net")],
                p,
                dict(success=True, moved_uids=["51"], blocked_present=True),
            ))
        finally:
            try:
                os.remove(pf)
            except Exception:
                print("WARNING: could not remove %s - REMOVE IT MANUALLY" % pf)

    # ------------------------------------------------------------ bypass list
    print("=" * 62)
    print("WHAT THIS HARNESS BYPASSED - read before trusting a PASS")
    print("  - No real IMAP server. Proves what the TOOL does with given hits.")
    print("  - find_messages is a stub. Server-side search correctness is NOT")
    print("    exercised; the guard is only as good as the hits it is handed.")
    print("  - from_addr values come from the stub, not from parsed headers.")
    print("  - mailbox_empty_folder is NOT covered. It has no protected-sender")
    print("    check at all, by design - folder-scoped, nothing to select on.")
    print("  - Substring matching is exercised, not adjudicated. Entries like")
    print("    'account@' and 'ratings@' match broadly. Over-blocking is the")
    print("    fail-safe direction and is NOT graded here.")
    print("  - Scenario D asserts the CURRENT bypass. A FAIL there means the")
    print("    bypass was closed, not that the harness broke.")
    print("=" * 62)

    total = len(results)
    good = len([r for r in results if r])
    print("")
    print("OVERALL: %s   (%d/%d)" % ("PASS" if good == total else "FAIL", good, total))
    return 0 if good == total else 1


if __name__ == "__main__":
    sys.exit(main())
