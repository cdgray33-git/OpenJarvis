#!/usr/bin/env python
"""openjarvis-bulk-census-v1

READ ONLY. Census of the Yahoo Bulk (Spam) folder via the direct connector
path. Writes nothing, moves nothing, expunges nothing.

Run from the repo root:  python .\tests\probe_bulk_census_v1.py
(or from wherever it sits, as long as CWD is the repo root)

WHAT THIS BYPASSES - stated up front, per the standing rule:
  - the agent entirely (no NativeOpenHandsAgent, so Defect 1 cannot apply)
  - the tool layer (no MailboxFindMessagesTool, no ToolExecutor, no dispatch log)
  - the protected-sender guard, which is TOOL-LAYER ONLY (W31 2.1)
  - the confirmation gate
It is read-only, so none of those matter here. They WILL matter if a move
script is ever built on this same connector-direct shape.
"""

import sys
import collections

sys.path.insert(0, "src")

from openjarvis.tools.mailbox_tools import connector_for  # noqa: E402

ACCOUNT = "yahoo_main"
FOLDER = "Bulk"
SIZE_KEY_CANDIDATES = ("size", "bytes", "rfc822_size", "size_bytes", "length")


def main():
    print("MARKER openjarvis-bulk-census-v1   READ ONLY")
    print("ACCOUNT " + ACCOUNT + "   FOLDER " + FOLDER)

    conn = connector_for(ACCOUNT)
    if conn is None:
        print("FAIL: no connector for account " + ACCOUNT)
        return 1

    rows = conn.find_messages(folder=FOLDER, limit=100000)

    if not isinstance(rows, list):
        print("FAIL: expected a list from the connector, got " + repr(type(rows)))
        print("      (the dict shape with match_count belongs to the TOOL layer)")
        return 1

    print("ROWS RETURNED " + str(len(rows)))
    if not rows:
        print("Bulk is empty, or the folder name is not 'Bulk' on this account.")
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

    for r in rows:
        addr = (r.get("from_addr") or "unknown").strip().lower()
        count_by[addr] += 1
        n = 0
        if size_key:
            try:
                n = int(r.get(size_key) or 0)
            except (TypeError, ValueError):
                n = 0
        total_bytes += n
        bytes_by[addr] += n

    print("")
    print("TOTAL MESSAGES " + str(len(rows)))
    print("TOTAL BYTES    " + str(total_bytes)
          + "   (" + str(round(total_bytes / 1048576.0, 1)) + " MB)")
    print("DISTINCT SENDERS " + str(len(count_by)))
    print("")
    print("TOP 30 SENDERS BY MESSAGE COUNT")
    print("   COUNT        MB  SENDER")
    for addr, n in count_by.most_common(30):
        mb = round(bytes_by[addr] / 1048576.0, 1)
        print("  " + str(n).rjust(6) + "  " + str(mb).rjust(8) + "  " + addr)

    print("")
    print("TOP 15 SENDERS BY SIZE")
    print("   COUNT        MB  SENDER")
    for addr, b in bytes_by.most_common(15):
        mb = round(b / 1048576.0, 1)
        print("  " + str(count_by[addr]).rjust(6) + "  " + str(mb).rjust(8) + "  " + addr)

    print("")
    print("READ ONLY - nothing was moved, deleted or expunged.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
