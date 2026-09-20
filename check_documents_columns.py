import sqlite3
conn = sqlite3.connect(r"C:\Users\Admin\.openjarvis\memory.db")
cur = conn.cursor()

# Full schema of the documents table
cur.execute("PRAGMA table_info('documents')")
cols = cur.fetchall()
print("documents table columns:")
for c in cols:
    print(f"    {c}")

# Measure byte size of EVERY column, not just content
col_names = [c[1] for c in cols]
print("\nByte totals per column:")
for col in col_names:
    try:
        cur.execute(f"SELECT SUM(LENGTH(\"{col}\")) FROM documents")
        total = cur.fetchone()[0] or 0
        print(f"  {col}: {total:,} bytes ({total/1e9:.2f} GB)")
    except Exception as e:
        print(f"  {col}: error ({e})")

conn.close()
