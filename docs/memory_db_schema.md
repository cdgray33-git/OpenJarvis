# memory.db Schema Reference

**Location:** `C:\Users\Admin\.openjarvis\memory.db`
**NOT** `C:\Users\Admin\OpenJarvis\memory.db` (stray 0-byte file at this path — investigate why it exists)
**Size (as of 2026-07-08):** ~21.3GB, 559K+ rows

## Tables

### documents (primary table)
```sql
CREATE TABLE documents (
    id TEXT PRIMARY KEY,
    content TEXT NOT NULL,
    source TEXT DEFAULT '',
    metadata TEXT DEFAULT '{}',
    created_at REAL DEFAULT (julianday('now'))
)
```

### documents_fts (FTS5 virtual table for full-text search)
```sql
CREATE VIRTUAL TABLE documents_fts USING fts5(
    content, source, tokenize='porter unicode61'
)
```
Backing tables (auto-managed by SQLite, do not touch directly):
- documents_fts_data
- documents_fts_idx
- documents_fts_content
- documents_fts_docsize
- documents_fts_config

## Notes
- `source` and `metadata` on `documents` correspond to `SQLiteMemory.store()`'s 
  `source` and `metadata` kwargs (see upload_router.py fix, June 2026).
- Open investigation: 44x discrepancy between SQL `SUM(LENGTH(content))` (~187MB) 
  and Python row-iteration count (8.25B chars) — unreconciled as of last check.
