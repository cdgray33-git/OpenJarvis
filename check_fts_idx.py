import sqlite3
conn = sqlite3.connect(r"C:\Users\Admin\.openjarvis\memory.db")
cur = conn.cursor()

# Size and cardinality of the actual inverted index
cur.execute("SELECT COUNT(*), COUNT(DISTINCT term), SUM(LENGTH(term)) FROM documents_fts_idx")
row_count, distinct_terms, term_bytes = cur.fetchone()
print(f"documents_fts_idx rows: {row_count:,}")
print(f"distinct terms: {distinct_terms:,}")
print(f"total term bytes: {term_bytes:,} ({(term_bytes or 0)/1e6:.1f} MB)")

# docsize table (small, but let's confirm)
cur.execute("SELECT SUM(LENGTH(sz)) FROM documents_fts_docsize")
docsize_bytes = cur.fetchone()[0] or 0
print(f"documents_fts_docsize total bytes: {docsize_bytes:,}")

# Sanity check: are content rows genuinely text, or is a huge fraction binary garbage?
# Heuristic: count rows whose content contains a lot of non-printable/high bytes
cur.execute("SELECT id, content FROM documents WHERE LENGTH(content) > 50000")
big_rows = cur.fetchall()
binary_like = 0
for _id, content in big_rows:
    if content is None:
        continue
    sample = content[:2000] if isinstance(content, str) else content[:2000].decode('latin1', errors='replace')
    non_printable = sum(1 for ch in sample if ord(ch) < 32 and ch not in '\n\r\t' or ord(ch) > 126)
    if non_printable > len(sample) * 0.3:
        binary_like += 1
print(f"\nOf {len(big_rows)} rows >50KB, {binary_like} look binary/non-text")

conn.close()
