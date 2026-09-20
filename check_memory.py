import sqlite3
import os

db_path = os.path.expanduser('~/.openjarvis/memory.db')
print('DB Path:', db_path)
print('DB Exists:', os.path.exists(db_path))

if os.path.exists(db_path):
    size = os.path.getsize(db_path)
    print('DB Size:', size, 'bytes')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('SELECT name FROM sqlite_master WHERE type="table"')
    tables = cursor.fetchall()
    print('Tables found:', [t[0] for t in tables])
    for table in tables:
        cursor.execute('SELECT COUNT(*) FROM ' + table[0])
        count = cursor.fetchone()[0]
        print(' ', table[0], ':', count, 'rows')
    conn.close()
else:
    print('DATABASE DOES NOT EXIST!')