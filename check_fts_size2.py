import sqlite3
conn = sqlite3.connect(r"C:\Users\Admin\.openjarvis\memory.db")
cur = conn.cursor()

# Size of the FTS shadow content mirror
cur.execute("SELECT SUM(LENGTH(c0)) + SUM(LENGTH(c1)) FROM documents_fts_content")
fts_content_bytes = cur.fetchone()[0] or 0
print(f"documents_fts_content total bytes (c0+c1): {fts_content_bytes:,} ({fts_content_bytes/1e6:.1f} MB)")

# Size of the actual FTS index segments -- likely the real culprit
cur.execute("SELECT SUM(LENGTH(block)) FROM documents_fts_data")
fts_data_bytes = cur.fetchone()[0] or 0
print(f"documents_fts_data total bytes (block): {fts_data_bytes:,} ({fts_data_bytes/1e9:.2f} GB)")

cur.execute("SELECT COUNT(*), AVG(LENGTH(block)), MAX(LENGTH(block)) FROM documents_fts_data")
cnt, avg_len, max_len = cur.fetchone()
print(f"documents_fts_data rows: {cnt:,}, avg block size: {avg_len:,.0f} bytes, max block size: {max_len:,} bytes")

# Confirm junk row footprint again for the cleanup plan
cur.execute("""
    SELECT COUNT(*), SUM(LENGTH(content))
    FROM documents
    WHERE source = '' OR source IS NULL
""")
junk_count, junk_bytes = cur.fetchone()
print(f"\nRows with empty/null source: {junk_count:,}, totaling {(junk_bytes or 0):,} bytes ({(junk_bytes or 0)/1e6:.1f} MB)")

conn.close()
