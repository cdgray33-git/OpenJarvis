import sqlite3
conn = sqlite3.connect(r"C:\Users\Admin\.openjarvis\memory.db")
cur = conn.cursor()

# Average content length in the main documents table
cur.execute("SELECT AVG(LENGTH(content)), MAX(LENGTH(content)), MIN(LENGTH(content)) FROM documents")
avg, mx, mn = cur.fetchone()
print(f"Content length - avg: {avg:.0f} chars, max: {mx}, min: {mn}")

# Check for potential duplicate content (same content repeated)
cur.execute("SELECT content, COUNT(*) as cnt FROM documents GROUP BY content HAVING cnt > 5 ORDER BY cnt DESC LIMIT 10")
dupes = cur.fetchall()
print("Top duplicate content (if any):")
for content, cnt in dupes:
    preview = content[:80].replace(chr(10), " ") if content else "(empty)"
    print(f"  {cnt}x: {preview}...")

# Oldest and newest entries to see the time range this data covers
cur.execute("SELECT name FROM pragma_table_info('documents')")
cols = [r[0] for r in cur.fetchall()]
print("Columns:", cols)

conn.close()
