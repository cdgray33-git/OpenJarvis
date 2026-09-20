import sqlite3, os

# Search all db files on the system within OpenJarvis
for root, dirs, files in os.walk(r'C:\Windows\System32\OpenJarvis'):
    # Skip venv
    dirs[:] = [d for d in dirs if d not in ['.venv', 'node_modules']]
    for f in files:
        if f.endswith('.db'):
            path = os.path.join(root, f)
            try:
                conn = sqlite3.connect(path)
                cur = conn.cursor()
                cur.execute('SELECT name FROM sqlite_master WHERE type=\'table\' ORDER BY name')
                tables = [t[0] for t in cur.fetchall()]
                if tables:
                    print('DB: ' + path)
                    print('Tables: ' + str(tables))
                conn.close()
            except Exception as e:
                print('Error: ' + path + ' -> ' + str(e))
