import sqlite3
conn = sqlite3.connect(r"C:\Users\Admin\.openjarvis\memory.db")
cur = conn.cursor()

# Size of the FTS shadow tables directly
cur.execute("SELECT SUM(LENGTH(content)) FROM documents_fts_content")
fts_content_bytes = cur.fetchone()[0] or 0
print(f"documents_fts_content total bytes: {fts_content_bytes:,} ({fts_content_bytes/1e6:.1f} MB)")

cur.execute("SELECT SUM(LENGTH(block)) FROM documents_fts_data")
fts_data_bytes = cur.fetchone()[0] or 0
print(f"documents_fts_data total bytes: {fts_data_bytes:,} ({fts_data_bytes/1e9:.2f} GB)")

# Confirm: how many junk/garbage rows and how much raw content they carry
cur.execute("""
    SELECT COUNT(*), SUM(LENGTH(content))
    FROM documents
    WHERE source = '' OR source IS NULL
""")
junk_count, junk_bytes = cur.fetchone()
print(f"\nRows with empty/null source: {junk_count:,}, totaling {junk_bytes:,} bytes ({(junk_bytes or 0)/1e6:.1f} MB)")

conn.close()
