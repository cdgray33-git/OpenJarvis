#!/usr/bin/env python3
# MARKER: openjarvis-memdb-probe-v1
"""
Read-only structural probe of the OpenJarvis memory.db.

Answers three questions the counting pass could not:
  1. Is documents_fts a plain FTS5 table holding a SECOND full copy of
     the content? (i.e. where did ~11.2 GB go?)
  2. If `source` is empty on 97.6% of rows, does path information live
     in `metadata` instead - and is there anything else to filter on?
  3. What IS the binary content, concretely? Enough bytes to identify it.

SAFETY: opens with URI mode=ro. SELECT and PRAGMA only. No writes.
Stdlib only.
"""

import argparse
import json
import os
import sqlite3
import sys
import time

DEFAULT_SAMPLE_IDS = [288383, 281043, 118635, 111295, 395140, 259218, 89470]


def fmt_bytes(n):
    if n is None:
        return "n/a"
    n = float(n)
    for unit in ("B", "KB", "MB", "GB", "TB"):
        if abs(n) < 1024.0:
            return "%7.2f %s" % (n, unit)
        n /= 1024.0
    return "%7.2f PB" % n


def fmt_int(n):
    return "{:,}".format(n) if n is not None else "n/a"


def dec(v):
    if v is None:
        return ""
    if isinstance(v, bytes):
        return v.decode("utf-8", "replace")
    return str(v)


def open_ro(path):
    uri = "file:{}?mode=ro".format(path.replace("?", "%3f").replace("#", "%23"))
    conn = sqlite3.connect(uri, uri=True, timeout=30.0)
    conn.text_factory = bytes
    conn.execute("PRAGMA busy_timeout = 30000")
    return conn


def hexdump(data, width=16, maxlen=256):
    out = []
    data = data[:maxlen]
    for off in range(0, len(data), width):
        chunk = data[off:off + width]
        hx = " ".join("%02x" % b for b in chunk)
        asc = "".join(chr(b) if 32 <= b <= 126 else "." for b in chunk)
        out.append("    %06x  %-*s  |%s|" % (off, width * 3, hx, asc))
    return "\n".join(out)


def section(t):
    print("\n" + "-" * 78)
    print(t)
    print("-" * 78)


def main():
    ap = argparse.ArgumentParser(description="Read-only memory.db probe")
    ap.add_argument("--db", default=os.path.join(
        os.path.expanduser("~"), ".openjarvis", "memory.db"))
    ap.add_argument("--table", default="documents")
    ap.add_argument("--fts", default="documents_fts")
    ap.add_argument("--ids", default="",
                    help="comma-separated rowids to hexdump")
    ap.add_argument("--meta-sample", type=int, default=8)
    ap.add_argument("--dump-bytes", type=int, default=256)
    ap.add_argument("--skip-sizing", action="store_true",
                    help="skip shadow-table SUM(LENGTH()) scans")
    args = ap.parse_args()

    path = os.path.abspath(args.db)
    if not os.path.isfile(path):
        print("Not a file: %s" % path, file=sys.stderr)
        sys.exit(2)

    conn = open_ro(path)
    print("=" * 78)
    print("OpenJarvis memory.db structural probe  (READ-ONLY)")
    print("=" * 78)
    print("db path   : %s" % path)
    print("generated : %s" % time.strftime("%Y-%m-%d %H:%M:%S"))

    # ---------------------------------------------------------------- 1
    section("1. FULL SCHEMA")
    rows = conn.execute(
        "SELECT type, name, sql FROM sqlite_master ORDER BY name").fetchall()
    for typ, name, sql in rows:
        print("\n  [%s] %s" % (dec(typ), dec(name)))
        s = dec(sql).strip()
        for ln in s.splitlines():
            print("      " + ln)

    # ---------------------------------------------------------------- 2
    section("2. FTS5 CONFIGURATION  <-- the 11.2 GB question")
    fts_sql = ""
    for typ, name, sql in rows:
        if dec(name) == args.fts:
            fts_sql = dec(sql)
    low = fts_sql.lower()
    external = "content=" in low.replace(" ", "")
    print("  create statement contains 'content=' : %s" % external)
    if external:
        print("  -> EXTERNAL CONTENT. No second copy. The 11.2 GB is index only.")
    else:
        print("  -> PLAIN FTS5. documents_fts_content should hold a full")
        print("     second copy of every indexed column. This is the ~8.7 GB.")

    try:
        cfg = conn.execute(
            'SELECT k, v FROM "%s_config"' % args.fts).fetchall()
        print("\n  %s_config:" % args.fts)
        for k, v in cfg:
            print("    %-16s %s" % (dec(k), dec(v)))
    except sqlite3.Error as e:
        print("\n  config table unreadable: %s" % e)

    # ---------------------------------------------------------------- 3
    section("3. SHADOW TABLE SIZING")
    if args.skip_sizing:
        print("  skipped (--skip-sizing)")
    else:
        print("  (each SUM scans that table; the _content scan is the slow one)")
        targets = [
            (args.fts + "_content", None),
            (args.fts + "_data", "block"),
            (args.fts + "_docsize", "sz"),
            (args.fts + "_idx", "term"),
        ]
        for tname, col in targets:
            try:
                cnt = conn.execute(
                    'SELECT COUNT(*) FROM "%s"' % tname).fetchone()[0]
            except sqlite3.Error as e:
                print("  %-28s unreadable (%s)" % (tname, e))
                continue
            cols = [dec(r[1]) for r in
                    conn.execute('PRAGMA table_info("%s")' % tname)]
            if col is None:
                blobcols = [c for c in cols if c.lower() != "id"]
            else:
                blobcols = [c for c in cols if c == col] or cols[1:]
            expr = " + ".join(
                'COALESCE(LENGTH(CAST("%s" AS BLOB)),0)' % c for c in blobcols)
            t0 = time.time()
            try:
                total = conn.execute(
                    'SELECT SUM(%s) FROM "%s"' % (expr, tname)).fetchone()[0]
            except sqlite3.Error as e:
                print("  %-28s sum failed (%s)" % (tname, e))
                continue
            print("  %-28s %10s rows  %s  (%.0fs)  cols=%s"
                  % (tname, fmt_int(cnt), fmt_bytes(total),
                     time.time() - t0, ",".join(blobcols)))

    # ---------------------------------------------------------------- 4
    section("4. MAIN TABLE COLUMNS")
    cols = [(dec(r[1]), dec(r[2])) for r in
            conn.execute('PRAGMA table_info("%s")' % args.table)]
    for name, typ in cols:
        print("  %-20s %s" % (name, typ))
    colnames = [c[0] for c in cols]

    section("5. SOURCE COLUMN - NULL vs EMPTY STRING")
    q = ('SELECT SUM(source IS NULL), SUM(source = \'\'), '
         'SUM(source IS NOT NULL AND source <> \'\') FROM "%s"' % args.table)
    try:
        nulls, empties, populated = conn.execute(q).fetchone()
        print("  source IS NULL        : %s" % fmt_int(nulls))
        print("  source = '' (empty)   : %s" % fmt_int(empties))
        print("  source populated      : %s" % fmt_int(populated))
    except sqlite3.Error as e:
        print("  failed: %s" % e)

    # ---------------------------------------------------------------- 6
    section("6. METADATA SAMPLE  <-- does the path live here instead?")
    if "metadata" not in colnames:
        print("  no metadata column on %s" % args.table)
    else:
        try:
            n_meta = conn.execute(
                'SELECT SUM(metadata IS NOT NULL AND metadata <> \'\') '
                'FROM "%s"' % args.table).fetchone()[0]
            print("  rows with non-empty metadata: %s\n" % fmt_int(n_meta))
        except sqlite3.Error as e:
            print("  count failed: %s" % e)
        try:
            srows = conn.execute(
                'SELECT rowid, metadata FROM "%s" '
                'WHERE metadata IS NOT NULL AND metadata <> \'\' '
                'LIMIT %d' % (args.table, args.meta_sample)).fetchall()
            keyset = set()
            for rid, meta in srows:
                m = dec(meta)
                print("  rowid %-10s %s" % (rid, m[:180]))
                try:
                    obj = json.loads(m)
                    if isinstance(obj, dict):
                        keyset.update(obj.keys())
                except Exception:
                    pass
            if keyset:
                print("\n  observed JSON keys: %s" % ", ".join(sorted(keyset)))
        except sqlite3.Error as e:
            print("  sample failed: %s" % e)

    # ---------------------------------------------------------------- 7
    section("7. BINARY CONTENT IDENTIFICATION")
    ids = [int(x) for x in args.ids.split(",") if x.strip()] \
        if args.ids else DEFAULT_SAMPLE_IDS
    for rid in ids:
        try:
            r = conn.execute(
                'SELECT rowid, source, LENGTH(CAST(content AS BLOB)), '
                'SUBSTR(CAST(content AS BLOB),1,%d) '
                'FROM "%s" WHERE rowid = ?'
                % (args.dump_bytes, args.table), (rid,)).fetchone()
        except sqlite3.Error as e:
            print("  rowid %s: query failed (%s)" % (rid, e))
            continue
        if not r:
            print("  rowid %s: not found" % rid)
            continue
        print("\n  rowid %s  len=%s  source=%r"
              % (r[0], fmt_bytes(r[2]), dec(r[1])))
        print(hexdump(r[3] or b"", maxlen=args.dump_bytes))

    print("\n" + "=" * 78)
    print("No writes were issued.")
    print("=" * 78)
    conn.close()


if __name__ == "__main__":
    main()
