import sqlite3

conn = sqlite3.connect(r'C:\Windows\System32\OpenJarvis\jarvis.db')
cur = conn.cursor()
cur.execute('SELECT name FROM sqlite_master WHERE type=\'table\' ORDER BY name')
tables = cur.fetchall()
print('Tables found:')
for t in tables:
    print('  -', t[0])
conn.close()
