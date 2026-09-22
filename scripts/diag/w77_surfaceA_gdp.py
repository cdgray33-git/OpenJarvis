import json, os, sqlite3, time, urllib.request
DB = os.path.join(os.environ['USERPROFILE'], '.openjarvis', 'telemetry.db')
c = sqlite3.connect(DB)
m0 = c.execute('select coalesce(max(id),0) from telemetry').fetchone()[0]
body = {'model': 'qwen3-coder:30b', 'stream': False,
        'messages': [{'role': 'user', 'content': 'What is the GDP of France in USD?'}]}
req = urllib.request.Request('http://127.0.0.1:8010/v1/chat/completions',
                             data=json.dumps(body).encode(), headers={'Content-Type': 'application/json'})
st = time.time()
with urllib.request.urlopen(req, timeout=300) as r:
    d = json.loads(r.read().decode('utf-8', 'replace'))
el = round(time.time() - st, 1)
msg = d['choices'][0]['message']
ans = str(msg.get('content', ''))
rows = list(c.execute('select id,agent,round(latency_seconds,2) from telemetry where id>?', (m0,)))
print('SECS', el, '| MODEL CALLS', len(rows), '| tool_calls', msg.get('tool_calls'))
print('SEARCH RAN:', any(k in ans for k in ('2.7', '2.8', '3.0', '3.1', '3.3', 'trillion', 'billion')))
print('ANSWER:', ans[:400].encode('ascii', 'replace').decode().replace('\n', ' '))
open(os.path.join('docs', 'SDP', 'evidence', 'W77', 'surfaceA-gdp.json'), 'w').write(json.dumps(d, indent=1))
