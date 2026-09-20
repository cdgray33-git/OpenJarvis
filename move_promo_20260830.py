"""
move_promo_20260830.py  -  READ ONLY unless --apply is passed.

Moves ruled promotional senders to Trash. Gray reviews Trash and empties it
himself; this script never empties anything.

Rulings carried (see mailbox notes):
  - 9 senders previously ruled clear
  - 24 senders ruled clear by Gray on 08/30
  - HELD: stackcommerce (both), self-sent cdgray33@yahoo.com, whyy.org,
    github, capitalone, usps informed delivery, groupon notify/orders/verify/otp

SAFETY DESIGN
  - Folder ALLOWLIST, not a protected blacklist. Anything outside the six
    allowed folders is held automatically.
  - Full-address search, not substring tokens. No collision with protected
    addresses on the same domain.
  - Report pass prints the message-dict key set. If no sender field can be
    identified, --apply is refused.
  - --apply also requires the sentinel below to be uncommented.

USAGE  (PowerShell, from PS C:\\Users\\Admin\\OpenJarvis>)
    $env:PYTHONIOENCODING="utf-8"; python .\\move_promo_20260830.py
    $env:PYTHONIOENCODING="utf-8"; python .\\move_promo_20260830.py --apply
"""
import sys

from openjarvis.tools.mailbox_tools import connector_for

ACCOUNT = "yahoo_main"
LIMIT = 5000

# Uncomment the next line ONLY when the report has been read and approved.
# APPLY_SENTINEL = "reviewed_report_20260830"
APPLY_SENTINEL = None

ALLOWED_FOLDERS = {
    "Inbox",
    "Archive",
    "Promotions",
    "Newsletters",
    "Social",
    "Social_Media",
}

# Exact addresses. Nothing is matched by token.
TARGETS = [
    # previously ruled
    "noreply@r.groupon.com",
    "express@b.express.com",
    "shop@bradsdeals.com",
    "editor@members.wayfair.com",
    "monster@notifications.monster.com",
    "thechildrensplace@emails.childrensplace.com",
    "newsletters@nl.technologyadvice.com",
    "funships@carnivalcruiselineemail.com",
    "nytdirect@nytimes.com",
    # ruled 08/30
    "noreply@fashionnova.com",
    "email@navyexchg.com",
    "bananarepublicfactory@email.bananarepublicfactory.com",
    "zalesoutlet@em.zales.com",
    "bestbuy@email.bestbuy.com",
    "info@email.purple.com",
    "no-reply@email.sears.com",
    "email@email.etsy.com",
    "angi@em.angi.com",
    "no-reply@email.dunhamssports.com",
    "info@thetourguy.com",
    "amf@bowl.amf.com",
    "anisa@pulsetv.com",
    "promos-coming@your-way.bk.com",
    "shop@e.containerstore.com",
    "noreply@skool.com",
    "extracare@mystore.cvs.com",
    "dailydeals@m.untilgone.com",
    "menswearhouse@imktg.menswearhouse.com",
    "daily@wh.womenshealthfirstly.com",
    "trivia@mail.wordstrivia.com",
    "send@sperry.com",
    "info@email.shoemall.com",
    "mail@mail.retailmenot.com",
]

# Never move, even if some search returns them.
NEVER = {
    "shop@email.stackcommerce.com",
    "shop@learn.stackcommerce.com",
    "cdgray33@yahoo.com",
    "hello@whyy.org",
    "notifications@github.com",
    "capitalone@notification.capitalone.com",
    "uspsinformeddelivery@email.informeddelivery.usps.com",
    "notify@r.groupon.com",
    "orders@r.groupon.com",
    "verify@r.groupon.com",
    "otp@r.groupon.com",
    "orders@sidedeal.com",
    "account@email.subway.com",
}

SENDER_KEYS = ("from_addr", "from", "sender", "address", "from_address")


def collision_check():
    """Abort if any target is also on the never list."""
    bad = [t for t in TARGETS if t.lower() in {n.lower() for n in NEVER}]
    if bad:
        print(f"ABORT: target is also on the NEVER list: {bad}")
        sys.exit(1)
    if len(set(TARGETS)) != len(TARGETS):
        print("ABORT: duplicate address in TARGETS.")
        sys.exit(1)


def sender_of(msg, key):
    return str(msg.get(key, "") or "").lower()


def main():
    apply_mode = "--apply" in sys.argv
    collision_check()

    print(f"python: {sys.executable}")
    print(f"MODE: {'APPLY' if apply_mode else 'REPORT (read only)'}")
    print(f"targets: {len(TARGETS)}   allowed folders: {sorted(ALLOWED_FOLDERS)}")
    print("=" * 70)

    conn = connector_for(ACCOUNT)
    if conn is None:
        print(f"ABORT: connector_for({ACCOUNT!r}) returned None - account did not resolve.")
        return 1

    sender_key = None
    shape_printed = False

    grand_target = 0
    grand_bytes = 0
    grand_held_folder = 0
    grand_held_addr = 0
    plan = {}   # (folder) -> list of uids
    per_sender = []

    for addr in TARGETS:
        res = conn.find_messages(from_addr=addr, limit=LIMIT)

        if not isinstance(res, list):
            print(f"ABORT: find_messages returned {type(res).__name__}, expected list. "
                  f"Connector shape has changed - stop and re-read.")
            return 1

        if not shape_printed and res:
            print(f"MESSAGE DICT KEYS: {sorted(res[0].keys())}")
            for k in SENDER_KEYS:
                if k in res[0]:
                    sender_key = k
                    break
            print(f"sender key detected: {sender_key!r}")
            print("=" * 70)
            shape_printed = True

        n_target = 0
        n_bytes = 0
        n_held_folder = 0
        n_held_addr = 0
        folders_hit = {}

        for m in res:
            folder = m.get("folder", "")

            if sender_key is not None:
                s = sender_of(m, sender_key)
                if s and addr.lower() not in s:
                    n_held_addr += 1
                    continue
                if s and any(nv.lower() in s for nv in NEVER):
                    n_held_addr += 1
                    continue

            if folder not in ALLOWED_FOLDERS:
                n_held_folder += 1
                continue

            n_target += 1
            n_bytes += int(m.get("bytes", 0) or 0)
            folders_hit[folder] = folders_hit.get(folder, 0) + 1
            plan.setdefault(folder, []).append(m.get("uid"))

        per_sender.append((addr, n_target, n_bytes, n_held_folder, n_held_addr, folders_hit))
        grand_target += n_target
        grand_bytes += n_bytes
        grand_held_folder += n_held_folder
        grand_held_addr += n_held_addr

        hits = ", ".join(f"{f}:{c}" for f, c in sorted(folders_hit.items())) or "-"
        print(f"{addr:<52} target {n_target:>4}  {n_bytes/1048576:>7.1f} MB  "
              f"heldFolder {n_held_folder:>3}  heldAddr {n_held_addr:>3}  [{hits}]")

    print("=" * 70)
    print(f"TOTAL TARGETED : {grand_target} messages, {grand_bytes/1048576:.1f} MB")
    print(f"HELD (folder)  : {grand_held_folder}")
    print(f"HELD (address) : {grand_held_addr}")
    print("Counts cover the window the server exposes (about 10,000 per folder), "
          "so they are a FLOOR, not a total.")
    print("\nPER FOLDER:")
    for f, uids in sorted(plan.items()):
        print(f"  {f:<16} {len(uids)}")

    if not apply_mode:
        print("\nREPORT ONLY. Nothing was moved.")
        print("To apply: uncomment APPLY_SENTINEL near the top, then re-run with --apply")
        return 0

    # ---------------- apply ----------------
    if sender_key is None:
        print("\nREFUSING TO APPLY: no sender field found on the message dicts, so the "
              "exact-address gate never ran. Only the folder allowlist would protect you. "
              "Re-read the connector before applying.")
        return 1

    if APPLY_SENTINEL != "reviewed_report_20260830":
        print("\nREFUSING TO APPLY: APPLY_SENTINEL is not set. Read the report, then "
              "uncomment the sentinel line near the top of this file.")
        return 1

    print("\nAPPLYING. Trash is NOT emptied - review it yourself afterwards.")
    total_copied = 0
    total_deleted = 0
    all_failed = []

    for folder, uids in sorted(plan.items()):
        if folder not in ALLOWED_FOLDERS:
            print(f"  SKIP {folder} - not on the allowlist")
            continue
        if not uids:
            continue
        print(f"  {folder}: moving {len(uids)} ...")
        r = conn.move_to_trash(folder, uids, dry_run=False,
                               chunk_size=10, pause_s=1.0, max_retries=4)
        copied = r.get("copied_count", 0)
        deleted = r.get("deleted_count", 0)
        failed = r.get("failed_uids", []) or []
        total_copied += copied
        total_deleted += deleted
        all_failed.extend(failed)
        print(f"    copied {copied}  deleted {deleted}  failed {len(failed)}")

    print("=" * 70)
    print(f"APPLY RESULT: copied {total_copied} / deleted {total_deleted} / "
          f"failed {len(all_failed)}")
    if all_failed:
        print(f"FAILED UIDS: {all_failed}")
    print("Verify in Yahoo's own settings UI, not usage_report.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
