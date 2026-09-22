import sqlite3, os, sys
c = sqlite3.connect(os.path.join(os.environ['USERPROFILE'], '.openjarvis', 'telemetry.db'))
if sys.argv[1] == 'max': print(c.execute('select coalesce(max(id),0) from telemetry').fetchone()[0])
else:
    for r in c.execute('select id,engine,model_id,agent,round(latency_seconds,2),metadata from telemetry where id>?', (int(sys.argv[2]),)): print('   TEL', r)
