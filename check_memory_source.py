import sqlite3
conn = sqlite3.connect(r"C:\Users\Admin\.openjarvis\memory.db")
cur = conn.cursor()

# Look at the 'source' field for these junk rows to find the ingestion path
cur.execute("""
    SELECT source, COUNT(*) as cnt 
    FROM documents 
    WHERE content LIKE '%DisplayString%' OR content LIKE '%DISCR_BEGIN%' OR content LIKE '%Eric Young%'
    GROUP BY source 
    ORDER BY cnt DESC 
    LIMIT 20
""")
for source, cnt in cur.fetchall():
    print(f"{cnt}x  source={source}")

# Total junk vs legitimate row count
cur.execute("""
    SELECT COUNT(*) FROM documents 
    WHERE content LIKE '%DisplayString%' OR content LIKE '%DISCR_BEGIN%' OR content LIKE '%Eric Young%' OR content LIKE '%two_po%'
""")
junk_count = cur.fetchone()[0]
cur.execute("SELECT COUNT(*) FROM documents")
total = cur.fetchone()[0]
print(f"\nLikely junk rows: {junk_count} / {total} total ({100*junk_count/total:.1f}%)")

conn.close()
