#!/usr/bin/env python3
# MARKER: openjarvis-memdb-provenance-v1
"""
Read-only provenance probe of the OpenJarvis memory.db.

Goal: find a purge axis safer than "delete rows that look binary".

  1. What is in documents.id? If it encodes a path or a file hash,
     provenance is recoverable and the purge becomes surgical.
  2. Does created_at cluster into discrete ingestion runs? If the
     garbage arrived in 2-3 batches, we can delete by time window
     and review exactly what falls inside it.
  3. What are the ~19,500 sourceless rows that are NOT mojibake?
     Those are the ones a content heuristic would wrongly spare or
     wrongly destroy, so look at them before deciding.

SAFETY: opens with URI mode=ro. SELECT and PRAGMA only. No writes.
Stdlib only. Runs in seconds - no full content scan.
"""

import argparse
import os
import sqlite3
import sys
import time
from collections import Counter

TABLE = "documents"


def dec(v):
    if v is None:
        return ""
    if isinstance(v, bytes):
        return v.decode("utf-8", "replace")
    return str(v)


def fmt_int(n):
    return "{:,}".format(n) if n is not None else "n/a"


def fmt_bytes(n):
    if n is None:
        return "n/a"
    n = float(n)
    for u in ("B", "KB", "MB", "GB", "TB"):
        if abs(n) < 1024.0:
            return "%7.2f %s" % (n, u)
        n /= 1024.0
    return "%7.2f PB" % n


def open_ro(path):
    uri = "file:{}?mode=ro".format(path.replace("?", "%3f").replace("#", "%23"))
    conn = sqlite3.connect(uri, uri=True, timeout=30.0)
    conn.text_factory = bytes
    conn.execute("PRAGMA busy_timeout = 30000")
    return conn


def section(t):
    print("\n" + "-" * 78)
    print(t)
    print("-" * 78)


def is_mojibake(head):
    """Head is the UTF-8 bytes as stored. Mojibake shows a high density of
    c2/c3 lead bytes: latin-1 round-tripped through UTF-8."""
    if not head:
        return False
    pairs = sum(1 for i in range(len(head) - 1) if head[i] in (0xC2, 0xC3))
    return (pairs / float(len(head))) > 0.15


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", default=os.path.join(
        os.path.expanduser("~"), ".openjarvis", "memory.db"))
    ap.add_argument("--id-samples", type=int, default=20)
    ap.add_argument("--text-samples", type=int, default=15)
    ap.add_argument("--scan-cap", type=int, default=80000,
                    help="max sourceless rows to examine for clean text")
    args = ap.parse_args()

    path = os.path.abspath(args.db)
    if not os.path.isfile(path):
        print("Not a file: %s" % path, file=sys.stderr)
        sys.exit(2)
    conn = open_ro(path)

    print("=" * 78)
    print("OpenJarvis memory.db provenance probe  (READ-ONLY)")
    print("=" * 78)
    print("db path   : %s" % path)
    print("generated : %s" % time.strftime("%Y-%m-%d %H:%M:%S"))

    # ---------------------------------------------------------------- 1
    section("1. WHAT IS IN documents.id ?")
    rows = conn.execute(
        'SELECT id, LENGTH(id), source FROM "%s" LIMIT %d'
        % (TABLE, args.id_samples)).fetchall()
    for rid, ln, src in rows:
        print("  len=%-4s %-64s src=%r" % (ln, dec(rid)[:64], dec(src)[:20]))

    print("\n  id length distribution:")
    for ln, c in conn.execute(
            'SELECT LENGTH(id), COUNT(*) FROM "%s" '
            'GROUP BY 1 ORDER BY 2 DESC LIMIT 12' % TABLE):
        print("    length %-5s %10s rows" % (ln, fmt_int(c)))

    print("\n  ids from the far end of the table (later ingest):")
    for rid, ln, src in conn.execute(
            'SELECT id, LENGTH(id), source FROM "%s" '
            'ORDER BY rowid DESC LIMIT 8' % TABLE):
        print("  len=%-4s %-64s src=%r" % (ln, dec(rid)[:64], dec(src)[:20]))

    # ---------------------------------------------------------------- 2
    section("2. created_at RANGE")
    r = conn.execute(
        'SELECT MIN(created_at), MAX(created_at), '
        'datetime(MIN(created_at)), datetime(MAX(created_at)), '
        'SUM(created_at IS NULL) FROM "%s"' % TABLE).fetchone()
    print("  earliest : %s  (julian %s)" % (dec(r[2]), r[0]))
    print("  latest   : %s  (julian %s)" % (dec(r[3]), r[1]))
    print("  null      : %s" % fmt_int(r[4]))

    section("3. INGESTION RUNS - rows per day")
    q = ('SELECT date(created_at) d, COUNT(*), '
         "SUM(CASE WHEN source='' THEN 1 ELSE 0 END), "
         "SUM(CASE WHEN source<>'' THEN 1 ELSE 0 END), "
         'SUM(LENGTH(CAST(content AS BLOB))) '
         'FROM "%s" GROUP BY d ORDER BY d' % TABLE)
    t0 = time.time()
    days = conn.execute(q).fetchall()
    print("  %-12s %12s %12s %12s  %s"
          % ("date", "rows", "sourceless", "sourced", "content"))
    for d, tot, nosrc, src, b in days:
        print("  %-12s %12s %12s %12s  %s"
              % (dec(d), fmt_int(tot), fmt_int(nosrc), fmt_int(src),
                 fmt_bytes(b)))
    print("  (%.0fs)" % (time.time() - t0))

    section("4. BUSIEST DAYS BROKEN OUT BY HOUR")
    top_days = sorted(days, key=lambda x: -x[1])[:3]
    for d, tot, _, _, _ in top_days:
        dd = dec(d)
        print("\n  %s" % dd)
        for h, c, b in conn.execute(
                "SELECT strftime('%%H', created_at) h, COUNT(*), "
                'SUM(LENGTH(CAST(content AS BLOB))) '
                'FROM "%s" WHERE date(created_at) = ? '
                'GROUP BY h ORDER BY h' % TABLE, (dd,)):
            bar = "#" * min(60, int(c / max(1, tot / 400.0)))
            print("    %s:00  %10s  %s  %s"
                  % (dec(h), fmt_int(c), fmt_bytes(b), bar))

    # ---------------------------------------------------------------- 5
    section("5. SOURCELESS ROWS THAT ARE *NOT* MOJIBAKE")
    print("  scanning up to %s sourceless rows...\n" % fmt_int(args.scan_cap))
    cur = conn.execute(
        'SELECT rowid, id, LENGTH(CAST(content AS BLOB)), '
        'SUBSTR(CAST(content AS BLOB),1,400), datetime(created_at) '
        'FROM "%s" WHERE source = \'\'' % TABLE)
    cur.arraysize = 500
    seen = 0
    clean = 0
    clean_bytes = 0
    moji = 0
    shown = 0
    while seen < args.scan_cap:
        batch = cur.fetchmany()
        if not batch:
            break
        for rid, did, ln, head, ts in batch:
            seen += 1
            if is_mojibake(head or b""):
                moji += 1
                continue
            clean += 1
            clean_bytes += ln or 0
            if shown < args.text_samples:
                shown += 1
                txt = (head or b"").decode("utf-8", "replace")
                txt = " ".join(txt.split())[:200]
                print("  rowid %-9s %s  %s" % (rid, fmt_bytes(ln), dec(ts)))
                print("    id   : %s" % dec(did)[:70])
                print("    text : %s\n" % txt)
            if seen >= args.scan_cap:
                break

    print("  examined      : %s sourceless rows" % fmt_int(seen))
    print("  mojibake      : %s (%.1f%%)"
          % (fmt_int(moji), 100.0 * moji / seen if seen else 0))
    print("  non-mojibake  : %s (%.1f%%)  %s"
          % (fmt_int(clean), 100.0 * clean / seen if seen else 0,
             fmt_bytes(clean_bytes)))
    print("\n  ^ these are the rows a naive binary heuristic would spare.")
    print("    Read the samples above before agreeing to any DELETE.")

    print("\n" + "=" * 78)
    print("No writes were issued.")
    print("=" * 78)
    conn.close()


if __name__ == "__main__":
    main()