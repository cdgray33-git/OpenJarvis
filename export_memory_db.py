# MARKER: openjarvis-memdb-export-v1
"""
export_memory_db.py -- read-only export + pre-deletion triage for OpenJarvis memory.db

Purpose
-------
Run this BEFORE deleting memory.db. It answers two questions and preserves the
only part of the corpus that has provenance:

  Phase A  Dump the ~13,930 rows that carry a populated `source` (upload / docs\\*)
           to JSONL. Small (~13 MB). This is the only citable content in the DB.

  Phase B  Classify the ~558,286 sourceless rows. Most are latin-1 -> UTF-8
           mojibake (binary read with a text decoder). The remainder -- roughly
           19,500 rows -- decoded cleanly, meaning the ingester walked over real
           text files. Those get pulled in full and scanned for credentials, so
           you know whether anything needs rotating before the DB goes away.

Safety
------
  * Opens the database with URI `mode=ro` and issues only SELECT / PRAGMA.
  * Sets `PRAGMA query_only=1` as a second guard.
  * Never writes to, moves, or deletes the database.
  * text_factory decodes with errors='replace' so undecodable TEXT does not
    raise mid-scan (this DB is a corruption case; assume nothing decodes).
  * Secret matches are written MASKED. The point is to learn *which* credential
    to rotate, not to create a second plaintext copy of it on disk.

Stdlib only -- runs under the venv python or the system python.

Usage (single-line, per standing rule -- no heredocs)
----------------------------------------------------
  uv run --no-sync python export_memory_db.py --out C:\\Users\\Admin\\.openjarvis\\export_20260730

  Fast smoke test first (stops after 20k sourceless rows):
  uv run --no-sync python export_memory_db.py --out .\\export_test --limit 20000

Runtime
-------
  Phase A: seconds.
  Phase B: I/O bound across ~8.68 GB. Budget 8-12 minutes, comparable to the
  count_memory_db.py fingerprint pass. Use --limit to sanity-check first.
"""

from __future__ import annotations

import argparse
import json
import re
import sqlite3
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

MARKER = "openjarvis-memdb-export-v1"
DEFAULT_DB = r"C:\Users\Admin\.openjarvis\memory.db"
HEAD_CHARS = 4096          # bytes-as-chars inspected per row during classification
BATCH = 500                # id batch size when re-reading clean rows in full
PROGRESS_EVERY = 25_000

# --- fast character-class tables (str.translate runs at C speed) -------------
# Deleting a char set and measuring the length delta is ~100x faster than a
# per-character Python loop, which matters at 558k rows x 4 KB.

_HI_LATIN1 = {c: None for c in range(0x80, 0x100)}          # the mojibake tell
_ASCII_OK = {c: None for c in list(range(0x20, 0x7F)) + [0x09, 0x0A, 0x0D]}


def classify(head: str) -> tuple[str, dict]:
    """Classify a row's leading chunk as 'clean' text, 'mojibake', or 'other'."""
    n = len(head)
    if n == 0:
        return "empty", {"n": 0}

    nul = head.count("\x00")
    repl = head.count("\ufffd")                              # decode failures
    hi = n - len(head.translate(_HI_LATIN1))                 # U+0080..U+00FF
    odd = len(head.translate(_ASCII_OK))                     # not printable ASCII

    stats = {
        "n": n,
        "nul": nul,
        "replacement": repl,
        "hi_latin1_pct": round(100.0 * hi / n, 2),
        "non_ascii_pct": round(100.0 * odd / n, 2),
    }

    if nul or repl > n * 0.001:
        return "mojibake", stats
    if hi > n * 0.02 or odd > n * 0.05:
        return "mojibake", stats
    return "clean", stats


# --- credential patterns -----------------------------------------------------
# Ordered most-specific first. Group 1 (or group 0) is what gets masked.

SECRET_PATTERNS = [
    ("github_pat",      re.compile(r"\b(gh[pousr]_[A-Za-z0-9]{16,}|github_pat_[A-Za-z0-9_]{20,})")),
    ("gitlab_pat",      re.compile(r"\b(glpat-[A-Za-z0-9\-_]{10,})")),
    ("vault_token",     re.compile(r"\b(hvs\.[A-Za-z0-9\-_.]{10,})")),
    ("aws_access_key",  re.compile(r"\b(AKIA[0-9A-Z]{16})\b")),
    ("slack_token",     re.compile(r"\b(xox[baprs]-[A-Za-z0-9\-]{10,})")),
    ("private_key",     re.compile(r"(-----BEGIN (?:RSA |EC |OPENSSH |PGP )?PRIVATE KEY-----)")),
    ("conn_string",     re.compile(r"://[^/\s:@]{1,64}:([^/\s:@]{3,64})@")),
    ("assigned_secret", re.compile(
        r"(?i)\b(?:password|passwd|pwd|secret|token|api[_-]?key|client[_-]?secret|bearer)\b"
        r"\s*[:=]\s*[\"']?([^\s\"',;]{6,120})")),
]

_PLACEHOLDERS = {
    "changeme", "password", "secret", "xxxxxx", "your_token_here",
    "none", "null", "true", "false", "example",
}


def mask(value: str) -> str:
    """Show enough to identify the credential, not enough to use it."""
    v = value.strip()
    if len(v) <= 6:
        return f"***[len={len(v)}]"
    return f"{v[:4]}***[len={len(v)}]"


def scan_secrets(text: str, row_id: str, context: int) -> list[dict]:
    hits = []
    for name, rx in SECRET_PATTERNS:
        for m in rx.finditer(text):
            raw = m.group(len(m.groups())) if m.groups() else m.group(0)
            if raw.strip().lower() in _PLACEHOLDERS:
                continue
            start, end = m.span()
            lo = max(0, start - context)
            hi = min(len(text), end + context)
            snippet = text[lo:start] + mask(raw) + text[end:hi]
            snippet = snippet.replace("\n", "\\n").replace("\r", "")
            hits.append({
                "row_id": row_id,
                "pattern": name,
                "offset": start,
                "masked": mask(raw),
                "context": snippet,
            })
    return hits


# --- db helpers --------------------------------------------------------------

def open_ro(db_path: Path) -> sqlite3.Connection:
    uri = db_path.resolve().as_uri() + "?mode=ro"
    conn = sqlite3.connect(uri, uri=True)
    conn.text_factory = lambda b: b.decode("utf-8", errors="replace")
    try:
        conn.execute("PRAGMA query_only=1")
    except sqlite3.Error:
        pass  # older builds; mode=ro already covers us
    return conn


def log(msg: str) -> None:
    print(f"[{time.strftime('%H:%M:%S')}] {msg}", flush=True)


# --- phases ------------------------------------------------------------------

def phase_a(conn, outdir: Path) -> int:
    log("PHASE A -- dumping rows with a populated source")
    path = outdir / "sourced_rows.jsonl"
    prefixes: dict[str, dict] = {}
    written = 0

    cur = conn.execute(
        "SELECT id, content, source, metadata, created_at FROM documents "
        "WHERE source IS NOT NULL AND source != ''"
    )
    with path.open("w", encoding="utf-8", newline="\n") as fh:
        for rid, content, source, metadata, created in cur:
            fh.write(json.dumps({
                "id": rid, "source": source, "metadata": metadata,
                "created_at": created, "content": content,
            }, ensure_ascii=False) + "\n")
            key = source.split("\\")[0].split("/")[0]
            slot = prefixes.setdefault(key, {"rows": 0, "chars": 0})
            slot["rows"] += 1
            slot["chars"] += len(content or "")
            written += 1
            if written % 5000 == 0:
                log(f"  ... {written:,} rows")

    with (outdir / "sourced_summary.txt").open("w", encoding="utf-8", newline="\n") as fh:
        fh.write(f"sourced rows: {written:,}\n\nby source prefix:\n")
        for key, slot in sorted(prefixes.items(), key=lambda kv: -kv[1]["chars"]):
            fh.write(f"  {key:<24} {slot['rows']:>8,} rows  {slot['chars'] / 1e6:>10.2f} MB\n")

    log(f"PHASE A done -- {written:,} rows -> {path.name}")
    return written


def phase_b(conn, outdir: Path, limit: int | None, sample_max: int,
            dump_all_clean: bool, context: int) -> dict:
    log("PHASE B -- classifying sourceless rows (this is the slow one)")
    counts = {"clean": 0, "mojibake": 0, "empty": 0, "other": 0}
    clean_ids: list[str] = []
    scanned = 0
    t0 = time.time()

    cur = conn.execute(
        "SELECT id, substr(content, 1, ?) FROM documents "
        "WHERE source IS NULL OR source = ''", (HEAD_CHARS,)
    )
    for rid, head in cur:
        kind, _ = classify(head or "")
        counts[kind] = counts.get(kind, 0) + 1
        if kind == "clean":
            clean_ids.append(rid)
        scanned += 1
        if scanned % PROGRESS_EVERY == 0:
            rate = scanned / max(time.time() - t0, 0.001)
            log(f"  ... {scanned:,} scanned  ({counts['clean']:,} clean)  {rate:,.0f} rows/s")
        if limit and scanned >= limit:
            log(f"  --limit {limit:,} reached, stopping scan early")
            break
    cur.close()

    log(f"  classified {scanned:,} rows: "
        f"{counts['clean']:,} clean / {counts['mojibake']:,} mojibake / {counts['empty']:,} empty")

    # Pull the clean rows in full -- they are text files, so this is cheap.
    log(f"PHASE B2 -- re-reading {len(clean_ids):,} clean rows in full and scanning for credentials")
    sample_path = outdir / "clean_sourceless_sample.jsonl"
    hits_path = outdir / "secret_hits.txt"
    sampled = 0
    all_hits: list[dict] = []

    with sample_path.open("w", encoding="utf-8", newline="\n") as fh:
        for i in range(0, len(clean_ids), BATCH):
            chunk = clean_ids[i:i + BATCH]
            q = ("SELECT id, content, metadata, created_at FROM documents "
                 f"WHERE id IN ({','.join('?' * len(chunk))})")
            for rid, content, metadata, created in conn.execute(q, chunk):
                content = content or ""
                all_hits.extend(scan_secrets(content, rid, context))
                if dump_all_clean or sampled < sample_max:
                    fh.write(json.dumps({
                        "id": rid, "metadata": metadata, "created_at": created,
                        "chars": len(content), "content": content,
                    }, ensure_ascii=False) + "\n")
                    sampled += 1
            if (i // BATCH) % 10 == 0:
                log(f"  ... {min(i + BATCH, len(clean_ids)):,}/{len(clean_ids):,} clean rows read")

    with hits_path.open("w", encoding="utf-8", newline="\n") as fh:
        fh.write(f"credential-pattern hits in sourceless clean-text rows\n")
        fh.write(f"generated {datetime.now(timezone.utc).isoformat()}\n")
        fh.write("values are MASKED -- first 4 chars + length. Rotate at the source system.\n\n")
        if not all_hits:
            fh.write("no matches.\n")
        else:
            by_pattern: dict[str, int] = {}
            for h in all_hits:
                by_pattern[h["pattern"]] = by_pattern.get(h["pattern"], 0) + 1
            fh.write("summary:\n")
            for k, v in sorted(by_pattern.items(), key=lambda kv: -kv[1]):
                fh.write(f"  {k:<20} {v:>6}\n")
            fh.write("\ndetail:\n")
            for h in all_hits:
                fh.write(f"\n  row {h['row_id']}  [{h['pattern']}]  offset {h['offset']}\n")
                fh.write(f"    {h['masked']}\n")
                fh.write(f"    ...{h['context']}...\n")

    log(f"PHASE B done -- {sampled:,} clean rows written, {len(all_hits):,} credential hits")
    return {"counts": counts, "scanned": scanned, "clean_total": len(clean_ids),
            "sampled": sampled, "hits": len(all_hits)}


def main() -> int:
    ap = argparse.ArgumentParser(description="Read-only export/triage for OpenJarvis memory.db")
    ap.add_argument("--db", default=DEFAULT_DB)
    ap.add_argument("--out", default=None, help="output directory (default: <db dir>/export_<date>)")
    ap.add_argument("--limit", type=int, default=None, help="stop the sourceless scan after N rows")
    ap.add_argument("--sample-max", type=int, default=200, help="clean rows to dump in full")
    ap.add_argument("--dump-all-clean", action="store_true", help="dump every clean row, not a sample")
    ap.add_argument("--context", type=int, default=60, help="chars of context around a credential hit")
    args = ap.parse_args()

    db_path = Path(args.db)
    if not db_path.exists():
        print(f"ERROR: database not found: {db_path}", file=sys.stderr)
        return 2

    outdir = Path(args.out) if args.out else db_path.parent / f"export_{datetime.now():%Y%m%d}"
    outdir.mkdir(parents=True, exist_ok=True)

    log(f"MARKER {MARKER}")
    log(f"python  {sys.executable}")
    log(f"sqlite  {sqlite3.sqlite_version}")
    log(f"db      {db_path}  ({db_path.stat().st_size / 1e9:.2f} GB)")
    log(f"out     {outdir}")

    conn = open_ro(db_path)
    try:
        total = conn.execute("SELECT COUNT(*) FROM documents").fetchone()[0]
        log(f"documents: {total:,} rows -- opened read-only, query_only set")

        t0 = time.time()
        sourced = phase_a(conn, outdir)
        result = phase_b(conn, outdir, args.limit, args.sample_max,
                         args.dump_all_clean, args.context)
        elapsed = time.time() - t0

        summary = {
            "marker": MARKER,
            "generated": datetime.now(timezone.utc).isoformat(),
            "db": str(db_path),
            "documents_total": total,
            "sourced_rows_dumped": sourced,
            "sourceless_scanned": result["scanned"],
            "classification": result["counts"],
            "clean_rows_total": result["clean_total"],
            "clean_rows_written": result["sampled"],
            "credential_hits": result["hits"],
            "elapsed_seconds": round(elapsed, 1),
            "limit_applied": args.limit,
        }
        with (outdir / "export_summary.json").open("w", encoding="utf-8", newline="\n") as fh:
            json.dump(summary, fh, indent=2)

        log("")
        log(f"COMPLETE in {elapsed / 60:.1f} min")
        log(f"  sourced_rows.jsonl          {sourced:,} rows")
        log(f"  clean_sourceless_sample     {result['sampled']:,} rows "
            f"(of {result['clean_total']:,} clean)")
        log(f"  secret_hits.txt             {result['hits']:,} masked hits")
        log(f"  export_summary.json")
        if result["hits"]:
            log("")
            log("  >> credential patterns matched. Review secret_hits.txt before deleting the DB.")
        return 0
    finally:
        conn.close()


if __name__ == "__main__":
    raise SystemExit(main())
