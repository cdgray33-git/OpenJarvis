#!/usr/bin/env python
"""openjarvis-folder-census-v1

READ ONLY. Census of any one IMAP folder via the direct connector path.
Writes nothing, moves nothing, expunges nothing.

Run from the repo root:
    python .\tests\probe_folder_census_v1.py Inbox
    python .\tests\probe_folder_census_v1.py Bulk
    python .\tests\probe_folder_census_v1.py "Online Purchases"

Folder defaults to Inbox if no argument is given. Non-interactive - it runs
to completion on its own and needs nothing typed while it works.

WHAT THIS BYPASSES - stated up front, per the standing rule:
  - the agent entirely (no NativeOpenHandsAgent, so Defect 1 cannot apply)
  - the tool layer (no MailboxFindMessagesTool, no ToolExecutor, no dispatch log)
  - the protected-sender guard, which is TOOL-LAYER ONLY (W31 2.1)
  - the confirmation gate
Read-only, so none of those matter here. They WILL matter if a move script is
ever built on this same connector-direct shape.

KNOWN CEILING: Yahoo's IMAP gateway indexes only the newest ~10,000 messages
per folder (measured 08/14, absolute - server-side SEARCH does not reach past
it either). If ROWS RETURNED comes back at exactly 10000 this census is a
window, not a total, and the script says so.
"""

import sys
import collections

sys.path.insert(0, "src")

from openjarvis.tools.mailbox_tools import connector_for  # noqa: E402

ACCOUNT = "yahoo_main"
DEFAULT_FOLDER = "Inbox"
WINDOW_CEILING = 10000
SIZE_KEY_CANDIDATES = ("size", "bytes", "rfc822_size", "size_bytes", "length")


def mb(n):
    return round(n / 1048576.0, 1)


def main(argv):
    folder = argv[1] if len(argv) > 1 else DEFAULT_FOLDER

    print("MARKER openjarvis-folder-census-v1   READ ONLY")
    print("ACCOUNT " + ACCOUNT + "   FOLDER " + repr(folder))

    conn = connector_for(ACCOUNT)
    if conn is None:
        print("FAIL: no connector for account " + ACCOUNT)
        return 1

    rows = conn.find_messages(folder=folder, limit=100000)

    if not isinstance(rows, list):
        print("FAIL: expected a list from the connector, got " + repr(type(rows)))
        print("      (the dict shape with match_count belongs to the TOOL layer)")
        return 1

    print("ROWS RETURNED " + str(len(rows)))
    if len(rows) >= WINDOW_CEILING:
        print("")
        print("*** CEILING WARNING ***")
        print("Row count is at or above " + str(WINDOW_CEILING) + ". This is Yahoo's")
        print("per-folder IMAP window, not the true folder total. Everything below")
        print("describes the NEWEST " + str(len(rows)) + " messages only. Older mail")
        print("exists and is invisible to IMAP - no code change can reach it.")
        print("")

    if not rows:
        print("Folder is empty, or the folder name does not exist on this account.")
        return 0

    print("ROW KEYS " + repr(sorted(rows[0].keys())))

    size_key = None
    for k in SIZE_KEY_CANDIDATES:
        if k in rows[0]:
            size_key = k
            break
    print("SIZE KEY " + repr(size_key))
    if size_key is None:
        print("NOTE: no size field found on the rows - byte totals will read 0.")

    total_bytes = 0
    count_by = collections.Counter()
    bytes_by = collections.Counter()
    count_by_dom = collections.Counter()
    bytes_by_dom = collections.Counter()

    for r in rows:
        addr = (r.get("from_addr") or "unknown").strip().lower()
        dom = addr.split("@")[-1] if "@" in addr else "unknown"
        n = 0
        if size_key:
            try:
                n = int(r.get(size_key) or 0)
            except (TypeError, ValueError):
                n = 0
        total_bytes += n
        count_by[addr] += 1
        bytes_by[addr] += n
        count_by_dom[dom] += 1
        bytes_by_dom[dom] += n

    print("")
    print("TOTAL MESSAGES   " + str(len(rows)))
    print("TOTAL BYTES      " + str(total_bytes) + "   (" + str(mb(total_bytes)) + " MB)")
    print("DISTINCT SENDERS " + str(len(count_by)))
    print("DISTINCT DOMAINS " + str(len(count_by_dom)))

    print("")
    print("TOP 40 SENDERS BY MESSAGE COUNT")
    print("   COUNT        MB  SENDER")
    for addr, n in count_by.most_common(40):
        print("  " + str(n).rjust(6) + "  " + str(mb(bytes_by[addr])).rjust(8) + "  " + addr)

    print("")
    print("TOP 20 SENDERS BY SIZE")
    print("   COUNT        MB  SENDER")
    for addr, b in bytes_by.most_common(20):
        print("  " + str(count_by[addr]).rjust(6) + "  " + str(mb(b)).rjust(8) + "  " + addr)

    print("")
    print("TOP 25 DOMAINS BY SIZE")
    print("   COUNT        MB  DOMAIN")
    for dom, b in bytes_by_dom.most_common(25):
        print("  " + str(count_by_dom[dom]).rjust(6) + "  " + str(mb(b)).rjust(8) + "  " + dom)

    top40 = sum(n for _, n in count_by.most_common(40))
    top40b = sum(bytes_by[a] for a, _ in count_by.most_common(40))
    print("")
    print("CONCENTRATION")
    print("  top 40 senders cover " + str(top40) + " of " + str(len(rows))
          + " messages (" + str(round(100.0 * top40 / len(rows), 1)) + " percent)")
    print("  and " + str(mb(top40b)) + " MB of " + str(mb(total_bytes)) + " MB ("
          + str(round(100.0 * top40b / total_bytes, 1) if total_bytes else "0")
          + " percent)")

    print("")
    print("READ ONLY - nothing was moved, deleted or expunged.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
