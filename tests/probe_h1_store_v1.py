"""probe_h1_store_v1.py - marker openjarvis-h1-store-probe-v1

Exercises ImapMailConnector.move_to_trash (imap_mail.py:537-655) against a
stubbed IMAP object. No network. No mailbox writes. Runs to completion with
no interaction.

What is real: the whole body of move_to_trash, 560-653, unmodified.
What is faked: the object returned by self._connect().

Scenarios
  A  COPY ok, STORE ok            expect applied=True,  clean
  B  COPY partial, STORE ok       expect applied=True,  failed_uids non-empty   <- H1 as stated
  C  COPY ok, STORE all NO        expect applied=False, but COPY already ran    <- the new mode
  D  COPY all fail                expect early return at 631-633, applied=False

Read-only with respect to the account. The connector is constructed with no
credentials; PROVIDERS supplies host/port/trash and nothing dials out.
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "src"))

from openjarvis.connectors.imap_mail import ImapMailConnector


class FakeImap(object):
    """Minimal stand-in for imaplib.IMAP4_SSL.

    Only the calls move_to_trash actually makes are implemented:
    select, uid("COPY", ...), uid("STORE", ...), expunge, logout.
    Every COPY and STORE is recorded so the harness can report what the
    server was actually asked to do, not just what the plan dict claims.
    """

    def __init__(self, copy_fail_uids=None, copy_fail_all=False,
                 store_result="OK"):
        self.copy_fail_uids = set(copy_fail_uids or [])
        self.copy_fail_all = copy_fail_all
        self.store_result = store_result
        self.copied_uids = []      # uids the server accepted a COPY for
        self.store_calls = []      # uid sets STORE was called with
        self.expunged = False
        self.logged_out = False

    def select(self, folder, readonly=False):
        return ("OK", [b"1"])

    def uid(self, command, *args):
        if command == "COPY":
            uid_set = args[0]
            uids = uid_set.split(",")
            if self.copy_fail_all:
                return ("NO", [b"COPY rejected by harness"])
            if any(u in self.copy_fail_uids for u in uids):
                return ("NO", [b"COPY rejected for poisoned uid"])
            self.copied_uids.extend(uids)
            return ("OK", [b"COPY completed"])
        if command == "STORE":
            self.store_calls.append(args[0])
            return (self.store_result, [b"store"])
        raise AssertionError("unexpected uid command: %r" % command)

    def expunge(self):
        self.expunged = True
        return ("OK", [b"expunged"])

    def logout(self):
        self.logged_out = True
        return ("BYE", [b"logout"])


def run(label, fake, uids, folder="Inbox"):
    conn = ImapMailConnector(provider="yahoo", account_id="harness")
    conn._connect = lambda: fake
    plan = conn.move_to_trash(
        folder, uids, dry_run=False, chunk_size=10, pause_s=0.0, max_retries=4
    )

    print("=" * 68)
    print(label)
    print("-" * 68)
    print("  PLAN DICT")
    for key in ("applied", "copied_count", "deleted_count", "failed_uids",
                "store_failed", "error", "note"):
        if key in plan:
            print("    %-14s %r" % (key, plan[key]))
    missing = [k for k in ("failed_uids", "store_failed") if k not in plan]
    if missing:
        print("    (absent: %s)" % ", ".join(missing))

    print("  WHAT THE SERVER ACTUALLY SAW")
    print("    uids COPIED into trash : %d %r" %
          (len(fake.copied_uids), fake.copied_uids))
    print("    STORE calls issued     : %d %r" %
          (len(fake.store_calls), fake.store_calls))
    print("    expunge called         : %s" % fake.expunged)
    print("    logout called          : %s" % fake.logged_out)

    tool_success = bool(plan.get("applied"))
    print("  TOOL LAYER (mailbox_tools.py:689)")
    print("    success=bool(applied)  : %s" % tool_success)

    left = len(fake.copied_uids) > 0 and not tool_success
    if left:
        print("    *** DIVERGENCE: %d message(s) copied into trash while the "
              "tool reports success=False" % len(fake.copied_uids))
    print()
    return plan


def main():
    uids = [str(n) for n in range(1, 13)]   # 12 uids -> 2 chunks at chunk_size=10

    run("SCENARIO A  COPY ok, STORE ok  (clean baseline)",
        FakeImap(), uids)

    run("SCENARIO B  COPY partial, STORE ok  (H1 as stated)",
        FakeImap(copy_fail_uids=["7"]), uids)

    run("SCENARIO C  COPY ok, STORE all NO  (the new mode)",
        FakeImap(store_result="NO"), uids)

    run("SCENARIO D  COPY all fail  (early return 631-633)",
        FakeImap(copy_fail_all=True), uids)

    print("=" * 68)
    print("Done. No network calls, no mailbox writes.")


if __name__ == "__main__":
    main()
