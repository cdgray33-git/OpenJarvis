import sqlite3
conn = sqlite3.connect(r"C:\Users\Admin\.openjarvis\memory.db")
cur = conn.cursor()

# Find the biggest rows by content length
cur.execute("""
    SELECT id, LENGTH(content) as len, source, substr(content, 1, 100) as preview
    FROM documents
    ORDER BY len DESC
    LIMIT 20
""")
print("Top 20 largest rows:")
for id_, length, source, preview in cur.fetchall():
    preview_clean = preview.replace(chr(10), " ") if preview else "(empty)"
    print(f"  id={id_}  len={length:,}  source={source}  preview={preview_clean}...")

# Total bytes consumed by just the top 1000 largest rows vs whole table
cur.execute("SELECT SUM(LENGTH(content)) FROM documents")
total_content_bytes = cur.fetchone()[0]
print(f"\nTotal content bytes (all rows): {total_content_bytes:,}")

cur.execute("""
    SELECT SUM(len) FROM (
        SELECT LENGTH(content) as len FROM documents ORDER BY len DESC LIMIT 1000
    )
""")
top1000_bytes = cur.fetchone()[0]
print(f"Bytes in top 1000 largest rows: {top1000_bytes:,} ({100*top1000_bytes/total_content_bytes:.1f}% of total content)")

# Distribution: how many rows are over 10KB, 100KB, 500KB
for threshold in [10_000, 100_000, 500_000]:
    cur.execute(f"SELECT COUNT(*) FROM documents WHERE LENGTH(content) > {threshold}")
    c = cur.fetchone()[0]
    print(f"Rows over {threshold:,} chars: {c}")

conn.close()
