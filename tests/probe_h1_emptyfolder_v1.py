#!/usr/bin/env python
"""openjarvis-h1-emptyfolder-v1

Tool-layer harness for MailboxEmptyFolderTool / ImapMailConnector.empty_folder.

REAL:  mailbox_tools.MailboxEmptyFolderTool.execute  (whole body)
       imap_mail.ImapMailConnector.empty_folder      (whole body)
       imap_mail.ImapMailConnector._fetch_summaries  (whole body)
       imap_mail.ImapMailConnector._close            (whole body)
FAKE:  only the object returned by ImapMailConnector._connect

Run from the repo root:
    python .\\tests\\probe_h1_emptyfolder_v1.py

Stdlib only. No network. No mailbox. Exits 2 if imports do not resolve,
1 if any scenario FAILS, 0 if all PASS.

Expectations below encode the POST-FIX contract (option A: check the
expunge return). Against UNPATCHED code scenario B is EXPECTED TO FAIL.
A test that passes before the fix is not a test.
"""

import json
import os
import sys
import traceback

sys.path.insert(0, os.path.join(os.getcwd(), "src"))

try:
    from openjarvis.connectors import imap_mail as imap_mod
    from openjarvis.connectors.imap_mail import ImapMailConnector
    from openjarvis.tools import mailbox_tools as mt_mod
    from openjarvis.tools.mailbox_tools import (
        CONFIRM_TOKEN,
        MailboxEmptyFolderTool,
    )
except Exception:
    sys.stderr.write("IMPORT FAILED - run from the repo root.\n")
    traceback.print_exc()
    sys.exit(2)


# ---------------------------------------------------------------- fake socket

class FakeImap(object):
    """Stands in for imaplib.IMAP4_SSL. Records every verb it is asked for."""

    def __init__(self, uids, select_typ="OK", search_typ="OK",
                 fetch_typ="OK", store_typ="OK", expunge_typ="OK"):
        self.uids = list(uids)
        self.select_typ = select_typ
        self.search_typ = search_typ
        self.fetch_typ = fetch_typ
        self.store_typ = store_typ
        self.expunge_typ = expunge_typ
        self.calls = []

    def select(self, name, readonly=False):
        self.calls.append("select(readonly=%s)" % readonly)
        return self.select_typ, [b"%d" % len(self.uids)]

    def uid(self, verb, *args):
        self.calls.append("uid(%s)" % verb)
        if verb == "SEARCH":
            if self.search_typ != "OK" or not self.uids:
                return self.search_typ, [b""]
            return "OK", [" ".join(self.uids).encode("ascii")]
        if verb == "FETCH":
            if self.fetch_typ != "OK":
                return self.fetch_typ, []
            resp = []
            for u in self.uids:
                meta = (b"1 (UID " + u.encode("ascii") +
                        b" RFC822.SIZE 2048 BODY[HEADER.FIELDS (FROM)] {90}")
                hdr = (b"From: sender@example.com\r\n"
                       b"To: cdgray33@yahoo.com\r\n"
                       b"Subject: probe message " + u.encode("ascii") + b"\r\n"
                       b"Date: Tue, 2 Sep 2026 09:00:00 -0400\r\n"
                       b"Message-ID: <probe-" + u.encode("ascii") + b"@x>\r\n\r\n")
                resp.append((meta, hdr))
                resp.append(b")")
            return "OK", resp
        if verb == "STORE":
            self.calls.append("STORE_uidset=%s" % (args[0] if args else "?"))
            return self.store_typ, [b""]
        return "OK", [b""]

    def expunge(self):
        self.calls.append("expunge")
        return self.expunge_typ, [b""]

    def logout(self):
        self.calls.append("logout")
        return "BYE", [b""]

    def close(self):
        self.calls.append("close")
        return "OK", [b""]


def make_connector(fake):
    conn = object.__new__(ImapMailConnector)
    conn._account_id = "probe"
    conn._last_error = None
    conn._connect = lambda: fake
    return conn


def make_tool():
    try:
        return MailboxEmptyFolderTool()
    except Exception:
        return object.__new__(MailboxEmptyFolderTool)


# ------------------------------------------------------------------ scenarios

SCENARIOS = [
    # label, FakeImap kwargs, expected applied, expected success, note
    ("A clean expunge",
     dict(uids=["101", "102", "103"]),
     True, True, "STORE OK, EXPUNGE OK"),
    ("B expunge NOT OK",
     dict(uids=["101", "102", "103"], expunge_typ="NO"),
     False, False, "STORE OK, EXPUNGE refused - THE DEFECT"),
    ("C store NOT OK",
     dict(uids=["101", "102", "103"], store_typ="NO"),
     False, False, "STORE refused, expunge never reached"),
    ("D already empty",
     dict(uids=[]),
     False, False, "no rows, early return"),
]


def run():
    print("=" * 72)
    print("openjarvis-h1-emptyfolder-v1   tool + connector layer")
    print("=" * 72)
    print("")
    print("THIS HARNESS DOES NOT COVER:")
    print("  - a server that answers EXPUNGE OK and expunges nothing")
    print("    (that residual is option B, re-verify by re-listing)")
    print("  - real Yahoo responses; proves what the code does with given")
    print("    replies, not which replies Yahoo sends")
    print("  - the unchunked STORE at imap_mail.py:709 against a large")
    print("    folder; no payload-size limit is simulated")
    print("  - protected senders (empty_folder does not consult them)")
    print("  - mailbox_move_to_trash (see probe_h1_toolprobe_v1.py)")
    print("")

    rows = []
    failures = 0

    for label, kwargs, exp_applied, exp_success, note in SCENARIOS:
        fake = FakeImap(**kwargs)
        conn = make_connector(fake)
        mt_mod.connector_for = lambda account, _c=conn: _c
        tool = make_tool()

        try:
            res = tool.execute(
                account="probe",
                folder="Trash",
                dry_run=False,
                confirm=CONFIRM_TOKEN,
            )
            payload = json.loads(res.content)
            got_applied = bool(payload.get("applied"))
            got_success = bool(res.success)
            err = payload.get("error")
        except Exception as exc:
            got_applied = None
            got_success = None
            err = "EXCEPTION: %s" % exc
            payload = {}

        ok = (got_applied == exp_applied and got_success == exp_success)
        if not ok:
            failures += 1

        rows.append((label, got_applied, got_success, exp_success, ok))

        print("-" * 72)
        print("%s   (%s)" % (label, note))
        print("  applied = %r   success = %r   expected success = %r"
              % (got_applied, got_success, exp_success))
        print("  error   = %r" % (err,))
        print("  expunge_failed = %r" % (payload.get("expunge_failed"),))
        print("  message_count  = %r" % (payload.get("message_count"),))
        print("  IMAP verbs asked for: %s" % (", ".join(fake.calls),))
        print("  -> %s" % ("PASS" if ok else "FAIL"))

    print("")
    print("=" * 72)
    for label, ga, gs, es, ok in rows:
        print("  %-22s applied=%-5r success=%-5r want=%-5r  %s"
              % (label, ga, gs, es, "PASS" if ok else "FAIL"))
    print("")
    print("OVERALL: %s   (%d/%d)"
          % ("PASS" if failures == 0 else "FAIL",
             len(rows) - failures, len(rows)))
    print("=" * 72)
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(run())
