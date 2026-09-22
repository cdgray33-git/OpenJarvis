# W77 RTM verification instrument - proves INVOCATION, not reply text. Non-interactive.
import json, sqlite3, time, urllib.request, urllib.error, os, sys
BASE = 'http://127.0.0.1:8010'
DB = os.path.join(os.environ['USERPROFILE'], '.openjarvis', 'telemetry.db')
OUT = sys.argv[1]
CHECKS = [
 ('RQ-022', 'What is 137 * 42?', ['"calculator"'], '5754'),
 ('RQ-021', 'Search the web for the latest stable Python release and tell me the version number.', ['"web_search"'], None),
 ('RQ-025', 'Summarize in one sentence: The quarterly review found that support tickets fell 18 percent after the new triage process, while response times improved from 9 hours to 4 hours, and customer satisfaction rose to its highest level in two years.', ['"llm"'], None)]
def get(p, t=30):
    with urllib.request.urlopen(BASE + p, timeout=t) as r: return r.status, r.read().decode('utf-8', 'replace')
def post(p, body, t=300):
    req = urllib.request.Request(BASE + p, data=json.dumps(body).encode(), headers={'Content-Type': 'application/json'})
    try:
        with urllib.request.urlopen(req, timeout=t) as r: return r.status, r.read().decode('utf-8', 'replace')
    except urllib.error.HTTPError as e: return e.code, e.read().decode('utf-8', 'replace')
    except Exception as e: return 0, 'EXC ' + repr(e)
def trace_ids():
    try:
        d = json.loads(get('/v1/traces')[1])
        L = d if isinstance(d, list) else d.get('traces', d.get('data', []))
        return [str(x.get('trace_id', x.get('id'))) for x in L if isinstance(x, dict)]
    except Exception: return []
a = lambda s: str(s).encode('ascii', 'replace').decode()
c = sqlite3.connect(DB)
maxid = lambda: c.execute('select coalesce(max(id),0) from telemetry').fetchone()[0]
model = c.execute('select model_id from telemetry order by id desc limit 1').fetchone()[0]
ts, tools = get('/v1/tools')
reg = {k: ('"%s"' % k) in tools for k in ('calculator', 'web_search', 'llm')}
report = {'model': model, 'tools_http': ts, 'registered': reg, 'tools_raw': tools, 'checks': []}
print('MODEL', model, '| /v1/tools', ts, '| registered', reg)
engines_all = set()
for rq, prompt, names, expect in CHECKS:
    t0 = set(trace_ids()); m0 = maxid(); st = time.time()
    s, body = post('/v1/chat/completions', {'model': model, 'messages': [{'role': 'user', 'content': prompt}], 'stream': False})
    el = round(time.time() - st, 1); time.sleep(2)
    new = [t for t in trace_ids() if t not in t0]; tr = {}
    for t in new:
        try: tr[t] = get('/v1/traces/' + t)[1]
        except Exception as e: tr[t] = 'ERR ' + repr(e)
    rows = [dict(zip(['id', 'model_id', 'engine', 'agent', 'latency', 'metadata'], r)) for r in
            c.execute('select id,model_id,engine,agent,latency_seconds,metadata from telemetry where id>?', (m0,))]
    engines_all |= {r['engine'] for r in rows}
    hits_trace = {n: any(n in v for v in tr.values()) for n in names}
    hits_resp = {n: n in body for n in names}
    ans = body
    try: ans = json.loads(body)['choices'][0]['message']['content']
    except Exception: pass
    rec = {'rq': rq, 'prompt': prompt, 'http': s, 'secs': el, 'hits_trace': hits_trace, 'hits_response': hits_resp,
           'response_has_tool_results': 'tool_results' in body, 'new_traces': new, 'telemetry_rows': rows,
           'answer': ans, 'response_raw': body, 'traces_raw': tr}
    if expect: rec['expected_in_answer'] = expect in str(ans).replace(',', '')
    report['checks'].append(rec)
    print(a(f"{rq} http={s} {el}s traces+{len(new)} telem+{len(rows)} engines={sorted(map(str, {r['engine'] for r in rows}))} "
            f"trace_hit={hits_trace} resp_hit={hits_resp} tool_results_key={rec['response_has_tool_results']}"
            + (f" expect={rec['expected_in_answer']}" if expect else '')))
    print('   ANSWER:', a(ans)[:160].replace('\n', ' '))
report['rq030_engines'] = sorted(map(str, engines_all))
print('RQ-030 engines serving the checks:', report['rq030_engines'])
json.dump(report, open(OUT, 'w'), indent=1, default=str)
print('WROTE', OUT)
