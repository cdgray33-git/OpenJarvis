#!/usr/bin/env python3
# MARKER: openjarvis-memdb-count-v1
"""
Read-only inventory pass over the OpenJarvis memory.db.

SAFETY: this script never writes to the database. It opens the file with
URI mode=ro and issues only SELECT and PRAGMA statements. It is safe to
run against a live database while the backend is up.

Stdlib only - no third-party imports, so it runs under the venv python or
the system python equally well.

Modes:
  fingerprint (default)  reads length + first 2048 bytes of each row.
                         Fast. Duplicate count is an UPPER BOUND estimate.
  full                   reads every byte and hashes it. Exact duplicate
                         numbers. Run this before any DELETE.
  light                  lengths and sources only. No content read at all.
"""

import argparse
import hashlib
import json
import os
import sqlite3
import sys
import time
from collections import Counter, defaultdict

FLAG_PATTERNS = [
    "rust\\target", "rust/target",
    "target\\debug", "target/debug",
    "target\\release", "target/release",
    ".venv", "site-packages",
    "node_modules",
    "__pycache__",
    "\\.git\\", "/.git/",
    "\\dist\\", "/dist/",
    "\\build\\", "/build/",
]

SIZE_BUCKETS = [
    ("       <1 KB", 0, 1024),
    ("   1 - 4 KB", 1024, 4 * 1024),
    ("  4 - 16 KB", 4 * 1024, 16 * 1024),
    (" 16 - 64 KB", 16 * 1024, 64 * 1024),
    ("64 - 256 KB", 64 * 1024, 256 * 1024),
    ("256 KB - 1 MB", 256 * 1024, 1024 * 1024),
    ("      >1 MB", 1024 * 1024, float("inf")),
]

FTS_SUFFIXES = ("_data", "_idx", "_content", "_docsize", "_config")


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


def open_ro(path):
    uri = "file:{}?mode=ro".format(path.replace("?", "%3f").replace("#", "%23"))
    try:
        conn = sqlite3.connect(uri, uri=True, timeout=30.0)
    except sqlite3.OperationalError as e:
        print("\nFAILED to open the database read-only: %s" % e, file=sys.stderr)
        print(
            "If the backend is STOPPED and a stale -wal file needs recovery, a\n"
            "read-only connection cannot replay it. Start the backend, or copy\n"
            "the .db/-wal/-shm trio elsewhere and point --db at the copy.",
            file=sys.stderr,
        )
        sys.exit(2)
    conn.text_factory = bytes
    conn.execute("PRAGMA busy_timeout = 30000")
    return conn


def discover_db():
    candidates = []
    home = os.path.expanduser("~")
    candidates.append(os.path.join(home, ".openjarvis", "memory.db"))
    for c in candidates:
        if os.path.isfile(c):
            return c
    return None


def decode(v):
    if v is None:
        return ""
    if isinstance(v, bytes):
        return v.decode("utf-8", "replace")
    return str(v)


def inspect_schema(conn, forced_table=None):
    rows = conn.execute(
        "SELECT name, type, sql FROM sqlite_master WHERE type IN ('table','view')"
    ).fetchall()
    tables = []
    for name, typ, sql in rows:
        tables.append((decode(name), decode(typ), decode(sql)))

    fts_bases = set()
    for name, typ, sql in tables:
        if sql and "fts5" in sql.lower():
            fts_bases.add(name)

    shadow = set()
    for name, _, _ in tables:
        for base in fts_bases:
            for suf in FTS_SUFFIXES:
                if name == base + suf:
                    shadow.add(name)

    main = forced_table
    scored = []
    if not main:
        for name, _, _ in tables:
            if name.startswith("sqlite_") or name in shadow:
                continue
            try:
                cols = [decode(r[1]).lower()
                        for r in conn.execute('PRAGMA table_info("%s")' % name)]
            except sqlite3.Error:
                continue
            score = 0
            if "content" in cols:
                score += 2
            if "source" in cols:
                score += 1
            if "metadata" in cols:
                score += 1
            if score:
                scored.append((score, name, cols))
        scored.sort(reverse=True)
        if scored:
            main = scored[0][1]

    return tables, fts_bases, shadow, main


def page_accounting(conn, path, want_dbstat):
    out = {}
    for pragma in ("page_count", "page_size", "freelist_count", "journal_mode",
                   "auto_vacuum", "encoding"):
        try:
            v = conn.execute("PRAGMA %s" % pragma).fetchone()
            out[pragma] = decode(v[0]) if isinstance(v[0], bytes) else v[0]
        except sqlite3.Error:
            out[pragma] = None

    out["file_size"] = os.path.getsize(path) if os.path.isfile(path) else None
    for side in ("-wal", "-shm"):
        p = path + side
        out["file_size" + side] = os.path.getsize(p) if os.path.isfile(p) else 0

    out["dbstat"] = None
    if want_dbstat:
        try:
            t0 = time.time()
            rows = conn.execute(
                "SELECT name, SUM(pgsize), COUNT(*) FROM dbstat "
                "GROUP BY name ORDER BY 2 DESC"
            ).fetchall()
            out["dbstat"] = [(decode(r[0]), r[1], r[2]) for r in rows]
            out["dbstat_seconds"] = round(time.time() - t0, 1)
        except sqlite3.Error as e:
            out["dbstat_error"] = str(e)
    return out


def classify_binary(head):
    if not head:
        return False
    if b"\x00" in head:
        return True
    printable = sum(
        1 for b in head
        if 32 <= b <= 126 or b in (9, 10, 13)
    )
    return (printable / float(len(head))) < 0.70


def flag_for(source):
    s = source.lower()
    for pat in FLAG_PATTERNS:
        if pat in s:
            return pat
    return None


def path_prefix(source, depth):
    s = source.replace("/", "\\")
    parts = [p for p in s.split("\\") if p]
    if not parts:
        return "(empty source)"
    if len(parts) <= depth:
        return "\\".join(parts[:-1]) or parts[0]
    return "\\".join(parts[:depth])


def scan(conn, table, mode, pk, top_n, progress_every):
    if mode == "light":
        sql = ('SELECT "{pk}", source, LENGTH(CAST(content AS BLOB)) '
               'FROM "{t}"').format(pk=pk, t=table)
    elif mode == "fingerprint":
        sql = ('SELECT "{pk}", source, LENGTH(CAST(content AS BLOB)), '
               'SUBSTR(CAST(content AS BLOB), 1, 2048) '
               'FROM "{t}"').format(pk=pk, t=table)
    else:
        sql = ('SELECT "{pk}", source, content '
               'FROM "{t}"').format(pk=pk, t=table)

    cur = conn.execute(sql)
    cur.arraysize = 200

    st = {
        "rows": 0,
        "bytes": 0,
        "null_content": 0,
        "buckets": Counter(),
        "src_rows": Counter(),
        "src_bytes": Counter(),
        "pfx_rows": Counter(),
        "pfx_bytes": Counter(),
        "flag_rows": Counter(),
        "flag_bytes": Counter(),
        "binary_rows": 0,
        "binary_bytes": 0,
        "flagged_ids": set(),
        "dupe_ids": set(),
        "largest": [],
    }
    hashes = defaultdict(lambda: [0, 0])  # digest -> [count, length]

    t0 = time.time()
    while True:
        batch = cur.fetchmany()
        if not batch:
            break
        for row in batch:
            rid = row[0]
            source = decode(row[1])
            if mode == "full":
                content = row[2]
                if content is None:
                    length = 0
                    st["null_content"] += 1
                    head = b""
                else:
                    if isinstance(content, str):
                        content = content.encode("utf-8", "surrogateescape")
                    length = len(content)
                    head = content[:2048]
            else:
                length = row[2]
                if length is None:
                    length = 0
                    st["null_content"] += 1
                head = row[3] if mode == "fingerprint" and len(row) > 3 else b""
                if head is None:
                    head = b""

            st["rows"] += 1
            st["bytes"] += length

            for label, lo, hi in SIZE_BUCKETS:
                if lo <= length < hi:
                    st["buckets"][label] += 1
                    break

            st["src_rows"][source] += 1
            st["src_bytes"][source] += length
            pfx = path_prefix(source, 3)
            st["pfx_rows"][pfx] += 1
            st["pfx_bytes"][pfx] += length

            fl = flag_for(source)
            if fl:
                st["flag_rows"][fl] += 1
                st["flag_bytes"][fl] += length
                st["flagged_ids"].add(rid)

            if mode != "light":
                if classify_binary(head):
                    st["binary_rows"] += 1
                    st["binary_bytes"] += length

                if mode == "full":
                    dig = hashlib.blake2b(
                        content or b"", digest_size=16).digest()
                else:
                    h = hashlib.blake2b(digest_size=16)
                    h.update(head)
                    h.update(str(length).encode("ascii"))
                    dig = h.digest()
                slot = hashes[dig]
                if slot[0] == 0:
                    slot[1] = length
                else:
                    st["dupe_ids"].add(rid)
                slot[0] += 1

            st["largest"].append((length, rid, source))
            if len(st["largest"]) > top_n * 4:
                st["largest"].sort(reverse=True)
                del st["largest"][top_n:]

            if progress_every and st["rows"] % progress_every == 0:
                el = time.time() - t0
                rate = st["rows"] / el if el else 0
                print(
                    "  ... %s rows, %s read, %.0f rows/s, %.0fs elapsed"
                    % (fmt_int(st["rows"]), fmt_bytes(st["bytes"]), rate, el),
                    file=sys.stderr,
                )

    st["largest"].sort(reverse=True)
    del st["largest"][top_n:]
    st["elapsed"] = time.time() - t0
    st["hashes"] = hashes
    return st


def report(args, path, schema, pages, st, mode):
    tables, fts_bases, shadow, table = schema
    W = 78
    line = "-" * W

    def hdr(t):
        print("\n" + line)
        print(t)
        print(line)

    print("=" * W)
    print("OpenJarvis memory.db inventory  (READ-ONLY)")
    print("=" * W)
    print("db path      : %s" % path)
    print("scan mode    : %s" % mode)
    print("generated    : %s" % time.strftime("%Y-%m-%d %H:%M:%S"))

    hdr("1. FILE AND PAGE ACCOUNTING")
    print("file size          : %s" % fmt_bytes(pages["file_size"]))
    print("-wal               : %s" % fmt_bytes(pages["file_size-wal"]))
    print("-shm               : %s" % fmt_bytes(pages["file_size-shm"]))
    print("journal mode       : %s" % pages["journal_mode"])
    print("page size          : %s" % fmt_int(pages["page_size"]))
    print("page count         : %s" % fmt_int(pages["page_count"]))
    fl = pages["freelist_count"] or 0
    ps = pages["page_size"] or 0
    print("freelist pages     : %s  (%s reclaimable by VACUUM alone)"
          % (fmt_int(fl), fmt_bytes(fl * ps)))

    if pages.get("dbstat"):
        print("\nper-object size (dbstat, %ss):" % pages.get("dbstat_seconds"))
        for name, b, pg in pages["dbstat"][:20]:
            print("  %-34s %s  %s pages" % (name[:34], fmt_bytes(b), fmt_int(pg)))
        print("\n  ^ this is where the gap between content bytes and file size lives.")
    elif pages.get("dbstat_error"):
        print("\ndbstat unavailable: %s" % pages["dbstat_error"])
    else:
        print("\ndbstat not run (pass --dbstat to break the file down per table;")
        print("it walks every page, so expect several minutes on a 20 GB file).")

    hdr("2. SCHEMA")
    print("main content table : %s" % table)
    print("fts5 tables        : %s" % (", ".join(sorted(fts_bases)) or "none"))
    print("fts5 shadow tables : %s" % fmt_int(len(shadow)))
    print("all tables/views   : %s" % fmt_int(len(tables)))

    hdr("3. ROW AND CONTENT TOTALS")
    print("rows                    : %s" % fmt_int(st["rows"]))
    print("content bytes           : %s" % fmt_bytes(st["bytes"]))
    print("null/empty content rows : %s" % fmt_int(st["null_content"]))
    if st["rows"]:
        print("mean row                : %s"
              % fmt_bytes(st["bytes"] / float(st["rows"])))
    print("scan wall time          : %.1fs" % st["elapsed"])

    hdr("4. SIZE DISTRIBUTION")
    for label, _, _ in SIZE_BUCKETS:
        c = st["buckets"][label]
        pct = (100.0 * c / st["rows"]) if st["rows"] else 0
        bar = "#" * int(pct / 2)
        print("  %-14s %10s  %5.1f%%  %s" % (label, fmt_int(c), pct, bar))

    hdr("5. LARGEST ROWS")
    for length, rid, source in st["largest"]:
        print("  %s  id=%-10s %s" % (fmt_bytes(length), rid, source[:44]))

    hdr("6. SOURCE PREFIXES (top %d by bytes)" % args.top)
    for pfx, b in st["pfx_bytes"].most_common(args.top):
        print("  %s  %8s rows  %s"
              % (fmt_bytes(b), fmt_int(st["pfx_rows"][pfx]), pfx[:44]))

    hdr("7. FLAGGED PATTERNS (purge candidates by path)")
    if st["flag_rows"]:
        for pat, c in st["flag_rows"].most_common():
            print("  %-20s %10s rows  %s"
                  % (pat, fmt_int(c), fmt_bytes(st["flag_bytes"][pat])))
        tot_r = len(st["flagged_ids"])
        tot_b = sum(st["flag_bytes"].values())
        print("  %-20s %10s rows  %s   <-- union, de-overlapped"
              % ("TOTAL", fmt_int(tot_r), fmt_bytes(tot_b)))
    else:
        print("  none matched")

    if mode != "light":
        hdr("8. CONTENT CLASSIFICATION")
        pct = (100.0 * st["binary_rows"] / st["rows"]) if st["rows"] else 0
        print("  binary-ish rows : %s  (%.1f%%)  %s"
              % (fmt_int(st["binary_rows"]), pct, fmt_bytes(st["binary_bytes"])))
        print("  heuristic: NUL byte present, or <70%% printable in first 2 KB")

        hdr("9. DUPLICATES")
        hashes = st["hashes"]
        uniq = len(hashes)
        dupe_rows = st["rows"] - uniq
        reclaim = sum((c - 1) * ln for c, ln in hashes.values())
        pct = (100.0 * dupe_rows / st["rows"]) if st["rows"] else 0
        print("  distinct content : %s" % fmt_int(uniq))
        print("  duplicate rows   : %s  (%.1f%%)" % (fmt_int(dupe_rows), pct))
        print("  reclaimable      : %s" % fmt_bytes(reclaim))
        if mode == "fingerprint":
            print("\n  NOTE: fingerprint mode keys on (first 2 KB + length), so two")
            print("  rows sharing a header but differing later collide. These")
            print("  numbers are an UPPER BOUND. Re-run with --mode full for the")
            print("  exact figures before anything is deleted.")

        hdr("10. PURGE SCOPE ESTIMATE")
        union = st["flagged_ids"] | st["dupe_ids"]
        overlap = st["flagged_ids"] & st["dupe_ids"]
        print("  rows matching a flagged path : %s" % fmt_int(len(st["flagged_ids"])))
        print("  rows that are duplicates     : %s" % fmt_int(len(st["dupe_ids"])))
        print("  in both categories           : %s" % fmt_int(len(overlap)))
        print("  union (total purge candidates): %s  of %s  (%.1f%%)"
              % (fmt_int(len(union)), fmt_int(st["rows"]),
                 100.0 * len(union) / st["rows"] if st["rows"] else 0))
        print("\n  Deleting rows returns pages to the freelist. The file does not")
        print("  shrink until a VACUUM, which needs free space alongside it.")

    print("\n" + "=" * W)
    print("No writes were issued. Nothing has been deleted.")
    print("=" * W)


def main():
    ap = argparse.ArgumentParser(description="Read-only memory.db inventory")
    ap.add_argument("--db", help="path to memory.db (auto-discovers if omitted)")
    ap.add_argument("--table", help="override main content table detection")
    ap.add_argument("--pk", default="rowid", help="primary key column (default rowid)")
    ap.add_argument("--mode", choices=("light", "fingerprint", "full"),
                    default="fingerprint")
    ap.add_argument("--top", type=int, default=15)
    ap.add_argument("--dbstat", action="store_true",
                    help="per-table page accounting (slow: full page walk)")
    ap.add_argument("--progress", type=int, default=25000,
                    help="progress line every N rows (0 to disable)")
    ap.add_argument("--json", help="also write the raw numbers to this JSON file")
    args = ap.parse_args()

    path = args.db or discover_db()
    if not path:
        print("Could not locate memory.db. Pass --db explicitly.", file=sys.stderr)
        sys.exit(2)
    path = os.path.abspath(path)
    if not os.path.isfile(path):
        print("Not a file: %s" % path, file=sys.stderr)
        sys.exit(2)

    conn = open_ro(path)
    try:
        schema = inspect_schema(conn, args.table)
        table = schema[3]
        if not table:
            print("Could not identify a content table. Pass --table.", file=sys.stderr)
            print("Tables found: %s"
                  % ", ".join(t[0] for t in schema[0]), file=sys.stderr)
            sys.exit(2)

        print("Scanning %s (mode=%s). This is read-only." % (table, args.mode),
              file=sys.stderr)
        pages = page_accounting(conn, path, args.dbstat)
        st = scan(conn, table, args.mode, args.pk, args.top, args.progress)
        report(args, path, schema, pages, st, args.mode)

        if args.json:
            hashes = st.get("hashes") or {}
            payload = {
                "db": path,
                "table": table,
                "mode": args.mode,
                "generated": time.strftime("%Y-%m-%dT%H:%M:%S"),
                "file_size": pages["file_size"],
                "page_size": pages["page_size"],
                "page_count": pages["page_count"],
                "freelist_count": pages["freelist_count"],
                "rows": st["rows"],
                "content_bytes": st["bytes"],
                "null_content": st["null_content"],
                "binary_rows": st["binary_rows"],
                "binary_bytes": st["binary_bytes"],
                "distinct_content": len(hashes),
                "duplicate_rows": st["rows"] - len(hashes) if hashes else None,
                "reclaimable_bytes": sum((c - 1) * ln for c, ln in hashes.values())
                if hashes else None,
                "flagged_rows": len(st["flagged_ids"]),
                "flag_breakdown": dict(st["flag_rows"]),
                "purge_union_rows": len(st["flagged_ids"] | st["dupe_ids"]),
                "size_buckets": dict(st["buckets"]),
                "top_prefixes": [
                    {"prefix": p, "rows": st["pfx_rows"][p], "bytes": b}
                    for p, b in st["pfx_bytes"].most_common(args.top)
                ],
            }
            with open(args.json, "w", encoding="utf-8") as f:
                json.dump(payload, f, indent=2)
            print("\nWrote %s" % args.json, file=sys.stderr)
    finally:
        conn.close()


if __name__ == "__main__":
    main()