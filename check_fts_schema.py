import sqlite3
conn = sqlite3.connect(r"C:\Users\Admin\.openjarvis\memory.db")
cur = conn.cursor()

# Get real column names for the FTS shadow tables
for t in ["documents_fts_content", "documents_fts_data", "documents_fts_idx", "documents_fts_docsize"]:
    cur.execute(f"PRAGMA table_info('{t}')")
    cols = cur.fetchall()
    print(f"{t} columns:")
    for c in cols:
        print(f"    {c}")
    print()

conn.close()
