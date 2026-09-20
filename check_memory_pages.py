import sqlite3
conn = sqlite3.connect(r"C:\Users\Admin\.openjarvis\memory.db")
cur = conn.cursor()

# 1. List every table and its row count
cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = [r[0] for r in cur.fetchall()]
print("Tables in db:", tables)
print()
for t in tables:
    try:
        cur.execute(f"SELECT COUNT(*) FROM '{t}'")
        cnt = cur.fetchone()[0]
        print(f"  {t}: {cnt:,} rows")
    except Exception as e:
        print(f"  {t}: error ({e})")

# 2. Page-level breakdown (this is the real file-size math)
cur.execute("PRAGMA page_size")
page_size = cur.fetchone()[0]
cur.execute("PRAGMA page_count")
page_count = cur.fetchone()[0]
cur.execute("PRAGMA freelist_count")
freelist_count = cur.fetchone()[0]

total_size = page_size * page_count
free_size = page_size * freelist_count
used_size = total_size - free_size

print(f"\npage_size: {page_size:,} bytes")
print(f"page_count: {page_count:,}  -> total file size: {total_size:,} bytes ({total_size/1e9:.2f} GB)")
print(f"freelist_count: {freelist_count:,}  -> free/unreclaimed: {free_size:,} bytes ({free_size/1e9:.2f} GB)")
print(f"actual used size: {used_size:,} bytes ({used_size/1e9:.2f} GB)")
print(f"% of file that is free/reclaimable: {100*free_size/total_size:.1f}%")

# 3. Per-table byte usage via dbstat (if available)
try:
    cur.execute("SELECT name, SUM(pgsize) as bytes FROM dbstat GROUP BY name ORDER BY bytes DESC")
    print("\nBytes per table/index (via dbstat):")
    for name, b in cur.fetchall():
        print(f"  {name}: {b:,} bytes ({b/1e6:.1f} MB)")
except Exception as e:
    print(f"\ndbstat not available: {e}")

conn.close()
