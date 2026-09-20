"""move_costco_marriott.py - report-then-apply pass for the two released domains."""
import sys
from collections import defaultdict
from openjarvis.tools.mailbox_tools import connector_for

ACCOUNT = "yahoo_main"
LIMIT = 5000

PROTECTED_FOLDERS = {
    "Work", "Personal", "2025 Job Search", "Bulk", "Online Purchases",
    "Finance", "Health_Medical", "Shopping", "Trash", "Sent", "Draft", "Drafts",
}

# Fill in after reading the report. Transactional addresses only.
EXCLUDED_ADDRS = {"__none_found_ruled_08_16__"}

SENDERS = ["costco", "marriott"]

def main():
    apply = "--apply" in sys.argv and "CONFIRM DELETE" in sys.argv
    if "--apply" in sys.argv and not apply:
        print("REFUSED: --apply requires the exact string \"CONFIRM DELETE\"")
        return 2
    print("MODE: %s" % ("APPLY - WILL MOVE TO TRASH" if apply else "REPORT ONLY, no writes"))
    if apply and not EXCLUDED_ADDRS:
        print("ABORT: EXCLUDED_ADDRS is empty. Read the report and rule on the")
        print("       transactional addresses before applying. These domains carry")
        print("       membership renewals, Bonvoy statements and reservations.")
        return 2
    conn = connector_for(ACCOUNT)
    if conn is None:
        print("ABORT: connector_for(%r) returned None" % ACCOUNT)
        return 2

    sel = {}
    held_addr = defaultdict(int)
    held_fold = defaultdict(int)
    print("=" * 74)
    for tok in SENDERS:
        try:
            hits = conn.find_messages(from_addr=tok, limit=LIMIT)
        except Exception as exc:
            print("[%s] LOOKUP FAILED: %s" % (tok, exc))
            continue
        if not hits:
            print("[%s] 0" % tok)
            continue
        a = defaultdict(lambda: [0, 0])
        f = defaultdict(lambda: [0, 0])
        n = b = 0
        for h in hits:
            addr = str(h.get("from_addr", "") or "").lower()
            fold = str(h.get("folder", "") or "")
            uid = str(h.get("uid", "") or "").strip()
            by = int(h.get("bytes", 0) or 0)
            n += 1
            b += by
            a[addr][0] += 1
            a[addr][1] += by
            f[fold][0] += 1
            f[fold][1] += by
            if fold in PROTECTED_FOLDERS:
                held_fold[fold] += 1
                continue
            if addr in EXCLUDED_ADDRS:
                held_addr[addr] += 1
                continue
            if uid.isdigit():
                sel[(fold, uid)] = by
        print("[%s] %d msgs / %.1f MB" % (tok, n, b / 1048576.0))
        for addr, (c, by) in sorted(a.items(), key=lambda x: -x[1][0]):
            tag = "  <-- HELD, transactional" if addr in EXCLUDED_ADDRS else ""
            print("    addr  %-52s %5d  %7.1f MB%s" % (addr[:52], c, by / 1048576.0, tag))
        for fold, (c, by) in sorted(f.items(), key=lambda x: -x[1][0]):
            tag = "  <-- PROTECTED, will NOT move" if fold in PROTECTED_FOLDERS else ""
            print("    fold  %-52s %5d  %7.1f MB%s" % (fold[:52], c, by / 1048576.0, tag))
        print("    subjects, newest-visible sample:")
        for h in hits[:12]:
            print("      %-46s | %s" % (str(h.get("from_addr", ""))[:46],
                                        str(h.get("subject", ""))[:70]))

    per = defaultdict(list)
    tot = 0
    for (fold, uid), by in sel.items():
        per[fold].append(uid)
        tot += by
    print("=" * 74)
    print("MOVABLE: %d msgs / %.1f MB across %d folders" % (len(sel), tot / 1048576.0, len(per)))
    for fold in sorted(per):
        print("    %-30s %5d" % (fold, len(per[fold])))
    if held_addr:
        print("HELD, transactional addresses:")
        for addr, c in sorted(held_addr.items()):
            print("    %-52s %5d" % (addr, c))
    if held_fold:
        print("HELD, protected folders:")
        for fold, c in sorted(held_fold.items()):
            print("    %-30s %5d" % (fold, c))

    if not apply:
        print("")
        print("REPORT ONLY. Nothing moved.")
        print("Read the addr lines and the subject sample. Add any transactional")
        print("address to EXCLUDED_ADDRS, then re-run with:")
        print('  python -u move_costco_marriott.py --apply "CONFIRM DELETE"')
        return 0

    print("")
    print("APPLYING")
    gc = gd = 0
    gf = []
    for fold in sorted(per):
        uids = per[fold]
        print("  %s: %d uids ..." % (fold, len(uids)))
        try:
            r = conn.move_to_trash(fold, uids, dry_run=False)
        except Exception as exc:
            print("    FAILED: %s" % exc)
            continue
        c = int(r.get("copied_count", 0) or 0)
        d = int(r.get("deleted_count", 0) or 0)
        fu = list(r.get("failed_uids", []) or [])
        gc += c
        gd += d
        gf.extend(fu)
        print("    copied %d / deleted %d / failed %d" % (c, d, len(fu)))
    print("=" * 74)
    print("TOTAL copied %d / deleted %d / failed %d" % (gc, gd, len(gf)))
    if gf:
        print("failed sample: %s" % gf[:10])
    print("Messages are in Trash. Review, then empty Trash yourself.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())

