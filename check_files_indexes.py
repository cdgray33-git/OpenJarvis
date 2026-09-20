import sqlite3, os

db_path = r"C:\Users\Admin\.openjarvis\memory.db"

# Check for companion files
for suffix in ["", "-wal", "-shm", "-journal"]:
    p = db_path + suffix
    if os.path.exists(p):
        size = os.path.getsize(p)
        print(f"{p}: {size:,} bytes ({size/1e9:.2f} GB)")
    else:
        print(f"{p}: does not exist")

conn = sqlite3.connect(db_path)
cur = conn.cursor()

# List ALL indexes, not just tables
cur.execute("SELECT name, tbl_name, sql FROM sqlite_master WHERE type='index'")
print("\nAll indexes:")
for name, tbl, sql in cur.fetchall():
    print(f"  {name} on {tbl}: {sql}")

# Double check current journal mode
cur.execute("PRAGMA journal_mode")
print(f"\njournal_mode: {cur.fetchone()[0]}")

# Fresh page_count re-read (paranoia check, in case of stale cache)
cur.execute("PRAGMA page_count")
print(f"page_count (fresh): {cur.fetchone()[0]:,}")

conn.close()
