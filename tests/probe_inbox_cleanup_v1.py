#!/usr/bin/env python
r"""openjarvis-inbox-cleanup-v1

Moves messages from an APPROVED, EXACT-MATCH sender list out of the Inbox and
into Trash. DRY RUN BY DEFAULT - it will not move anything unless you pass
--apply explicitly.

Run from the repo root:
    python .\tests\probe_inbox_cleanup_v1.py            <- dry run, safe
    python .\tests\probe_inbox_cleanup_v1.py --apply    <- destructive

Non-interactive. Runs to completion on its own, needs nothing typed.

THIS DOES NOT FREE SPACE ON ITS OWN. Yahoo counts Trash against your quota.
Emptying Trash is a SEPARATE, deliberate step - not in this script.

WHAT THIS BYPASSES - stated up front, per the standing rule:
  - the agent entirely (no NativeOpenHandsAgent, so Defect 1 cannot apply)
  - the tool layer (no MailboxMoveToTrashTool, no ToolExecutor, no dispatch log)
  - the built-in protected-sender guard, which is TOOL-LAYER ONLY (W31 2.1)
  - the confirmation gate (--apply is the confirmation)
Because the real guard is bypassed, this script carries its OWN guard: the
EXCLUDED list below is checked against every target before anything runs, and
a collision aborts the whole run.

MATCHING IS EXACT on the lowercased full address. Not substring. A target that
matches nothing is reported, not silently skipped.
"""

import sys
import time
import inspect
import collections

sys.path.insert(0, "src")

from openjarvis.tools.mailbox_tools import connector_for  # noqa: E402

ACCOUNT = "yahoo_main"
FOLDER = "Inbox"
CHUNK = 200

# Approved by Gray 09/02 from the folder census. Bulk commercial senders only.
TARGETS = [
    "shop@email.stackcommerce.com",
    "shop@learn.stackcommerce.com",
    "noreply@r.groupon.com",
    "shop@bradsdeals.com",
    "noreply@fashionnova.com",
    "editor@members.wayfair.com",
    "thechildrensplace@emails.childrensplace.com",
    "email@navyexchg.com",
    "bananarepublicfactory@email.bananarepublicfactory.com",
    "info@email.purple.com",
    "zalesoutlet@em.zales.com",
    "no-reply@email.sears.com",
    "email@email.etsy.com",
    "no-reply@email.dunhamssports.com",
]

# Hard guard. Nothing here can ever be targeted, whatever the list above says.
EXCLUDED_ADDRESSES = {
    "notifications@github.com",
    "capitalone@notification.capitalone.com",
    "alerts@notify.wellsfargo.com",
    "uspsinformeddelivery@email.informeddelivery.usps.com",
    "monster@notifications.monster.com",
}
EXCLUDED_SUBSTRINGS = (
    "github",
    "capitalone",
    "wellsfargo",
    "chase",
    "bank",
    "irs.gov",
    "usps",
    "paypal",
    "monster",
    "visa.com",
)


def mb(n):
    return round(n / 1048576.0, 1)


def census(conn):
    rows = conn.find_messages(folder=FOLDER, limit=100000)
    if not isinstance(rows, list):
        raise RuntimeError("expected a list from the connector, got " + repr(type(rows)))
    return rows


def summarize(rows):
    dates = sorted([r.get("date") or "" for r in rows])
    total_bytes = 0
    for r in rows:
        try:
            total_bytes += int(r.get("bytes") or 0)
        except (TypeError, ValueError):
            pass
    return {
        "rows": len(rows),
        "bytes": total_bytes,
        "oldest": dates[0] if dates else "-",
        "newest": dates[-1] if dates else "-",
    }


def guard_check():
    problems = []
    for t in TARGETS:
        low = t.strip().lower()
        if low in EXCLUDED_ADDRESSES:
            problems.append("EXCLUDED ADDRESS: " + t)
        for s in EXCLUDED_SUBSTRINGS:
            if s in low:
                problems.append("EXCLUDED SUBSTRING '" + s + "' in: " + t)
    if len(set(x.strip().lower() for x in TARGETS)) != len(TARGETS):
        problems.append("DUPLICATE ENTRY IN TARGETS")
    return problems


def main(argv):
    apply_mode = "--apply" in argv

    print("MARKER openjarvis-inbox-cleanup-v1")
    print("MODE " + ("APPLY - DESTRUCTIVE" if apply_mode else "DRY RUN - nothing will move"))
    print("ACCOUNT " + ACCOUNT + "   FOLDER " + FOLDER)
    print("TARGETS " + str(len(TARGETS)))

    print("")
    print("--- GUARD ---")
    problems = guard_check()
    if problems:
        for p in problems:
            print("  ABORT: " + p)
        print("Run stopped. No connection was opened.")
        return 2
    print("  clean - no target collides with the excluded list")

    conn = connector_for(ACCOUNT)
    if conn is None:
        print("FAIL: no connector for account " + ACCOUNT)
        return 1

    try:
        print("")
        print("CONNECTOR move_to_trash signature: "
              + str(inspect.signature(conn.move_to_trash)))
    except Exception as e:
        print("could not read move_to_trash signature: " + repr(e))

    print("")
    print("--- BEFORE ---")
    rows = census(conn)
    before = summarize(rows)
    print("  rows   " + str(before["rows"]))
    print("  bytes  " + str(before["bytes"]) + "  (" + str(mb(before["bytes"])) + " MB)")
    print("  oldest " + before["oldest"])
    print("  newest " + before["newest"])
    if before["rows"] >= 10000:
        print("  NOTE: at the Yahoo 10,000 window ceiling - this is the visible pane.")

    wanted = set(t.strip().lower() for t in TARGETS)
    uids_by = collections.defaultdict(list)
    bytes_by = collections.Counter()
    for r in rows:
        addr = (r.get("from_addr") or "").strip().lower()
        if addr in wanted:
            uid = r.get("uid")
            if uid is None:
                continue
            uids_by[addr].append(str(uid))
            try:
                bytes_by[addr] += int(r.get("bytes") or 0)
            except (TypeError, ValueError):
                pass

    print("")
    print("--- PLAN ---")
    print("   COUNT        MB  SENDER")
    plan_total = 0
    plan_bytes = 0
    for t in TARGETS:
        low = t.strip().lower()
        n = len(uids_by.get(low, []))
        plan_total += n
        plan_bytes += bytes_by[low]
        flag = "" if n else "   <- NO MATCHES"
        print("  " + str(n).rjust(6) + "  " + str(mb(bytes_by[low])).rjust(8) + "  " + t + flag)
    print("")
    print("  TOTAL " + str(plan_total) + " messages, " + str(mb(plan_bytes)) + " MB")

    if not apply_mode:
        print("")
        print("DRY RUN COMPLETE - nothing was moved.")
        print("Re-run with --apply to move these to Trash.")
        return 0

    if plan_total == 0:
        print("")
        print("Nothing to move. Stopping.")
        return 0

    print("")
    print("--- APPLYING ---")
    print("Observed throughput on past runs is roughly 0.8 messages/second, so")
    print("expect this to take a while. Do not interrupt it.")
    started = time.time()
    moved = 0
    failed = []

    for t in TARGETS:
        low = t.strip().lower()
        uids = uids_by.get(low, [])
        if not uids:
            continue
        print("")
        print(t + "  (" + str(len(uids)) + " messages)")
        for i in range(0, len(uids), CHUNK):
            batch = uids[i:i + CHUNK]
            try:
                res = conn.move_to_trash(FOLDER, batch, dry_run=False)
                moved += len(batch)
                print("  chunk " + str(i // CHUNK + 1) + ": " + str(len(batch))
                      + " uids, result=" + repr(res)[:120])
            except Exception as e:
                failed.append((t, i, repr(e)))
                print("  chunk " + str(i // CHUNK + 1) + ": FAILED " + repr(e)[:200])

    elapsed = time.time() - started
    print("")
    print("--- APPLY DONE ---")
    print("  attempted " + str(plan_total) + " messages")
    print("  chunks reported moved " + str(moved))
    print("  failures " + str(len(failed)))
    for f in failed:
        print("    " + f[0] + " offset " + str(f[1]) + ": " + f[2][:160])
    print("  elapsed " + str(round(elapsed, 1)) + " s")

    print("")
    print("--- AFTER (re-census, the real verification) ---")
    rows2 = census(conn)
    after = summarize(rows2)
    still = collections.Counter()
    for r in rows2:
        addr = (r.get("from_addr") or "").strip().lower()
        if addr in wanted:
            still[addr] += 1
    print("  rows   " + str(after["rows"]) + "   (was " + str(before["rows"])
          + ", delta " + str(after["rows"] - before["rows"]) + ")")
    print("  bytes  " + str(after["bytes"]) + "  (" + str(mb(after["bytes"])) + " MB, was "
          + str(mb(before["bytes"])) + " MB)")
    print("  oldest " + after["oldest"] + "   (was " + before["oldest"] + ")")
    print("  newest " + after["newest"])
    print("  target messages still in Inbox: " + str(sum(still.values())))
    for a, n in still.most_common():
        print("    " + str(n).rjust(6) + "  " + a)

    print("")
    print("--- THE WINDOW QUESTION ---")
    if after["rows"] >= 10000 and after["oldest"] < before["oldest"]:
        print("  Row count held at the ceiling AND oldest moved BACK in time.")
        print("  Yahoo refilled the window with older mail. Repeated passes CAN")
        print("  reach further back. This is the good outcome.")
    elif after["rows"] < before["rows"]:
        print("  Row count dropped and the window did not refill. The 10,000 pane")
        print("  is a fixed set - clearing it does not expose older mail.")
    else:
        print("  Inconclusive from this run. Compare oldest/newest above by hand.")

    print("")
    print("SPACE IS NOT FREED YET. These messages are in Trash, which still counts")
    print("against your Yahoo quota. Empty Trash to actually reclaim the space.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
