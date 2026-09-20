"""
move_retail.py - batch retail/promotional sender pass, modeled on move_linkedin.py.

Two modes:
  python move_retail.py                 REPORT ONLY. No writes. Prints distinct real
                                        sender addresses, per-folder counts and bytes.
  python move_retail.py --apply "CONFIRM DELETE"
                                        Moves to Trash, grouped per folder.

Guards:
  - Report mode is the default. --apply alone is refused without the confirm string.
  - PROTECTED_FOLDERS are never touched in either mode; hits there are reported only.
  - EXCLUDED tokens are never searched.
  - Substring matches are coarse, so REPORT MODE MUST BE READ BEFORE --apply.
"""

import sys
from collections import defaultdict

from openjarvis.tools.mailbox_tools import connector_for

ACCOUNT = "yahoo_main"
LIMIT = 2000

# Deliberately-filed mail. Never moved by this script.
PROTECTED_FOLDERS = {
    "Work", "Personal", "2025 Job Search", "Trash", "Sent", "Draft", "Drafts",
}

# Ruled OUT by Gray - never searched.
EXCLUDED = ["costco", "marriott", "cdgray33@yahoo.com"]

# Ruled IN. Full domains where known, to keep the substring tight.
SENDERS = [
    "b.express.com",
    "stackcommerce.com",
    "bradsdeals.com",
    "childrensplace.com",
    "groupon.com",
    "wayfair.com",
    "technologyadvice.com",
    "carnivalcruiselineemail.com",
    "slickdeals.net",
    "menswearhouse.com",
    "michaels.com",
    "retailmenot.com",
    "aviationweek.com",
    "ahealthyliving.com",
    "shoemall.com",
    "daily.comms.yahoo.net",
    "tourtrivia.com",
    "microcenter.com",
    "mail.zillow.com",
    "reebok.com",
    "ilovedooney.com",
    "temuemail.com",
    "morningbrew.com",
    # tail - full domains unknown, report mode will show the real addresses
    "womenshealthfirstly",
    "heavy.com",
    "uncoverwords",
    "subway",
    "explainitdaily",
    "neighborhoodalerts",
    "wesalute",
    "sidedeal",
    "ollies",
    "thewealthminded",
    "shopmyexchange",
    "baerskintactical",
    "royalcaribbean",
    "safeway",
    # Archive-only, in scope under the standing archive ruling
    "bachrach",
    "weisnewsletter",
]

ADDR_KEYS = ("from_addr", "from", "sender", "address", "from_address")
FOLDER_KEYS = ("folder", "mailbox", "folder_name")


def pick(d, keys):
    for k in keys:
        if k in d and d[k]:
            return d[k]
    return "?"


def parse_args():
    argv = sys.argv[1:]
    if not argv:
        return False
    if argv[0] != "--apply":
        print("ABORT: unknown argument %r" % argv[0])
        sys.exit(2)
    if len(argv) < 2 or argv[1] != "CONFIRM DELETE":
        print('ABORT: --apply requires the exact string "CONFIRM DELETE" as the next argument.')
        sys.exit(2)
    return True


def main():
    apply_mode = parse_args()
    print("MODE: %s" % ("APPLY - messages will move to Trash" if apply_mode else "REPORT ONLY - no writes"))
    print("account=%s  senders=%d  excluded=%s" % (ACCOUNT, len(SENDERS), ",".join(EXCLUDED)))
    print("=" * 78)

    c = connector_for(ACCOUNT)

    grand_msgs = 0
    grand_bytes = 0
    protected_hits = defaultdict(int)
    move_plan = defaultdict(list)   # folder -> uids
    failures = []

    for token in SENDERS:
        try:
            hits = c.find_messages(from_addr=token, limit=LIMIT)
        except Exception as e:
            print("\n[%s] FIND FAILED: %s" % (token, e))
            failures.append((token, "find", str(e)))
            continue

        if not hits:
            print("\n[%s] 0 matches" % token)
            continue

        by_folder = defaultdict(lambda: [0, 0])   # folder -> [count, bytes]
        by_addr = defaultdict(lambda: [0, 0])
        for h in hits:
            f = pick(h, FOLDER_KEYS)
            a = pick(h, ADDR_KEYS)
            b = int(h.get("bytes") or 0)
            by_folder[f][0] += 1
            by_folder[f][1] += b
            by_addr[a][0] += 1
            by_addr[a][1] += b
            if f in PROTECTED_FOLDERS:
                protected_hits[f] += 1
            else:
                move_plan[f].append(h["uid"])

        tot_n = len(hits)
        tot_b = sum(v[1] for v in by_folder.values())
        grand_msgs += tot_n
        grand_bytes += tot_b

        print("\n[%s] %d msgs / %.1f MB" % (token, tot_n, tot_b / 1048576.0))
        if tot_n >= LIMIT:
            print("  WARNING: hit the %d limit - this is a CEILING, not a count." % LIMIT)
        for a in sorted(by_addr, key=lambda k: -by_addr[k][1]):
            n, b = by_addr[a]
            print("    addr  %-52s %5d  %7.1f MB" % (a[:52], n, b / 1048576.0))
        for f in sorted(by_folder, key=lambda k: -by_folder[k][1]):
            n, b = by_folder[f]
            flag = "  <-- PROTECTED, will NOT move" if f in PROTECTED_FOLDERS else ""
            print("    fold  %-52s %5d  %7.1f MB%s" % (f[:52], n, b / 1048576.0, flag))

    print("\n" + "=" * 78)
    print("TOTAL MATCHED: %d msgs / %.1f MB" % (grand_msgs, grand_bytes / 1048576.0))
    movable = sum(len(v) for v in move_plan.values())
    print("MOVABLE: %d uids across %d folders" % (movable, len(move_plan)))
    if protected_hits:
        print("HELD IN PROTECTED FOLDERS (need a per-case ruling):")
        for f in sorted(protected_hits):
            print("    %-30s %d" % (f, protected_hits[f]))

    if not apply_mode:
        print("\nREPORT ONLY. Read the addr lines above before applying.")
        print('To apply:  python move_retail.py --apply "CONFIRM DELETE"')
        return

    print("\nApplying, per folder...")
    tot_copied = tot_deleted = 0
    all_failed = []
    for folder in sorted(move_plan):
        uids = move_plan[folder]
        print("\n  %s: %d uids" % (folder, len(uids)))
        try:
            r = c.move_to_trash(folder, uids, dry_run=False)
        except Exception as e:
            print("    MOVE FAILED: %s" % e)
            failures.append((folder, "move", str(e)))
            continue
        copied = r.get("copied_count")
        deleted = r.get("deleted_count")
        failed = r.get("failed_uids") or []
        print("    copied=%s deleted=%s failed=%d" % (copied, deleted, len(failed)))
        tot_copied += int(copied or 0)
        tot_deleted += int(deleted or 0)
        all_failed.extend(failed)

    print("\n" + "=" * 78)
    print("APPLIED: copied=%d deleted=%d failed=%d" % (tot_copied, tot_deleted, len(all_failed)))
    if all_failed:
        print("FAILED UIDS (left in place, safe to re-run): %s" % all_failed[:50])
    if failures:
        print("ERRORS: %s" % failures)
    print("Next: review Trash in Yahoo's web UI, then empty it. That step is Gray's.")


if __name__ == "__main__":
    main()
