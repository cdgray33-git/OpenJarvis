#!/usr/bin/env python
# openjarvis-h1-toolprobe-v1
#
# Extends probe_h1_store_v1 UP one layer. The W28 probe stopped at the
# connector, so `success` was COMPUTED by the harness from `applied`. This one
# drives MailboxMoveToTrashTool.execute, so `success` is OBSERVED.
#
# What is REAL: the whole tool body (mailbox_tools.py:513-712) including the
# confirm interlock and the new result contract, AND the whole connector body
# (imap_mail.py:537-653).
# What is FAKE: only the object returned by ImapMailConnector._connect.
#
# BYPASSES, stated per the W27 2.5 rule - see the banner the script prints.
#
# No network. No mailbox writes. Non-interactive, runs to completion.
# Run from the repo root:  python .\probe_h1_toolprobe_v1.py

import json
import os
import sys
import time

sys.path.insert(0, os.path.join(os.getcwd(), "src"))

CONNECTOR_CANDIDATES = [
    "openjarvis.connectors.imap_mail",
    "openjarvis.tools.imap_mail",
    "openjarvis.mail.imap_mail",
    "openjarvis.imap_mail",
]

UIDS = [str(n) for n in range(1, 13)]   # 12 uids
FOLDER = "Inbox"


class FakeIMAP(object):
    """Records what it was ASKED to do. Methodology entry 12."""

    def __init__(self, copy_mode, store_mode):
        self.copy_mode = copy_mode      # "ok" | "partial" | "fail"
        self.store_mode = store_mode    # "ok" | "fail"
        self.copy_calls = []
        self.store_calls = []
        self.copied_uids = []
        self.expunged = False
        self.logged_out = False

    def select(self, quoted, readonly=False):
        return ("OK", [b"12"])

    def uid(self, cmd, *args):
        c = str(cmd).upper()
        if c == "COPY":
            uid_set = args[0]
            members = [u for u in str(uid_set).split(",") if u]
            self.copy_calls.append(uid_set)
            if self.copy_mode == "fail":
                return ("NO", [b"copy refused"])
            if self.copy_mode == "partial" and "7" in members:
                return ("NO", [b"copy refused"])
            self.copied_uids.extend(members)
            return ("OK", [b""])
        if c == "STORE":
            uid_set = args[0]
            self.store_calls.append(uid_set)
            if self.store_mode == "fail":
                return ("NO", [b"store refused"])
            return ("OK", [b""])
        return ("NO", [b"unexpected"])

    def expunge(self):
        self.expunged = True
        return ("OK", [b""])

    def logout(self):
        self.logged_out = True
        return ("BYE", [b""])


def load_connector():
    last = None
    for name in CONNECTOR_CANDIDATES:
        try:
            mod = __import__(name, fromlist=["ImapMailConnector"])
            return name, mod, getattr(mod, "ImapMailConnector")
        except Exception as exc:
            last = "%s: %s" % (name, exc)
    print("FAIL: could not import ImapMailConnector. Last error -> %s" % last)
    print("Add the correct module path to CONNECTOR_CANDIDATES and rerun.")
    sys.exit(2)


def run_one(label, copy_mode, store_mode, ToolCls, ConnCls, mailbox_tools,
            confirm_token):
    fake = FakeIMAP(copy_mode, store_mode)
    conn = ConnCls(provider="yahoo", account_id="harness")
    conn._connect = lambda *a, **k: fake

    mailbox_tools.connector_for = lambda account: conn

    tool = ToolCls()
    res = tool.execute(
        account="harness",
        folder=FOLDER,
        uids=list(UIDS),
        dry_run=False,
        confirm=confirm_token,
    )

    try:
        payload = json.loads(res.content)
    except Exception:
        payload = {"_unparsed": res.content}

    print("")
    print("--- SCENARIO %s  (COPY=%s STORE=%s)" % (label, copy_mode, store_mode))
    print("  asked: COPY chunks=%d uids_copied=%d | STORE chunks=%d | expunge=%s | logout=%s"
          % (len(fake.copy_calls), len(fake.copied_uids),
             len(fake.store_calls), fake.expunged, fake.logged_out))
    print("  OBSERVED success   : %s" % res.success)
    print("  outcome            : %s" % payload.get("outcome"))
    print("  requested/copied/deleted: %s/%s/%s"
          % (payload.get("requested_count"), payload.get("copied_count"),
             payload.get("deleted_count")))
    print("  failed_uids        : %s" % payload.get("failed_uids"))
    print("  store_failed       : %s" % payload.get("store_failed", "<absent>"))
    print("  retry_unsafe       : %s" % payload.get("retry_unsafe", "<absent>"))
    w = payload.get("warning")
    if w:
        print("  warning            : %s" % w)

    truth_copied = len(fake.copied_uids)
    if truth_copied > 0 and payload.get("deleted_count") in (0, None):
        if not payload.get("retry_unsafe"):
            print("  *** DIVERGENCE: %d copied into trash and retry_unsafe is not set"
                  % truth_copied)
        else:
            print("  OK: copied-not-removed is surfaced with retry_unsafe")
    if res.success and (payload.get("failed_uids") or payload.get("store_failed")):
        print("  *** DIVERGENCE: success=True with a populated failure list")
    return res.success, payload.get("outcome")


def main():
    print("openjarvis-h1-toolprobe-v1")
    print("BYPASSES (per W27 2.5):")
    print("  - time.sleep PATCHED in the connector module. The tool calls")
    print("    move_to_trash positionally, so pause_s cannot be passed. Retry")
    print("    LADDER TIMING IS NOT COVERED by this run.")
    print("  - from_addr NOT used, so openjarvis-protected-senders-v1 is again")
    print("    NOT exercised. Still owed.")
    print("  - No real IMAP server. This proves what the CODE does with given")
    print("    responses, not which responses Yahoo gives.")
    print("  - folder == trash branch (imap_mail.py:591-592) not exercised.")
    print("  - mailbox_empty_folder (:765, same bool(applied)) not covered.")

    modname, connmod, ConnCls = load_connector()
    print("connector module: %s" % modname)
    connmod.time.sleep = lambda *a, **k: None

    from openjarvis.tools import mailbox_tools
    ToolCls = mailbox_tools.MailboxMoveToTrashTool
    confirm_token = getattr(mailbox_tools, "CONFIRM_TOKEN")
    print("CONFIRM_TOKEN: %r" % confirm_token)
    print("contract marker present: %s"
          % ("openjarvis-h1-result-contract-v1" in
             open(mailbox_tools.__file__, "r", encoding="utf-8").read()))

    expect = {
        "A": ("complete", True),
        "B": ("partial", False),
        "C": ("copied_not_removed", False),
        "D": ("no_op", False),
    }
    plan = [("A", "ok", "ok"), ("B", "partial", "ok"),
            ("C", "ok", "fail"), ("D", "fail", "fail")]

    results = {}
    for label, cm, sm in plan:
        results[label] = run_one(label, cm, sm, ToolCls, ConnCls,
                                 mailbox_tools, confirm_token)

    print("")
    print("=== VERDICT")
    allok = True
    for label, _, _ in plan:
        got_success, got_outcome = results[label]
        want_outcome, want_success = expect[label]
        ok = (got_outcome == want_outcome and got_success == want_success)
        allok = allok and ok
        print("  %s expected outcome=%-18s success=%-5s | got outcome=%-18s success=%-5s | %s"
              % (label, want_outcome, want_success, got_outcome, got_success,
                 "PASS" if ok else "FAIL"))
    print("  OVERALL: %s" % ("PASS" if allok else "FAIL"))
    return 0 if allok else 1


if __name__ == "__main__":
    sys.exit(main())
