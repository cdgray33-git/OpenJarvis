import json, sys
from openjarvis import Jarvis
j = Jarvis()
out = []
for rq, tools, prompt in [('RQ-022', ['calculator'], 'What is 137 * 42?'),
                          ('RQ-021', ['calculator', 'web_search'], 'What is the GDP of France in USD?')]:
    try:
        d = j.ask_full(prompt, agent='native_openhands', tools=tools)
        tr = d.get('tool_results') or []
        names = [(x.get('tool_name') if isinstance(x, dict) else getattr(x, 'tool_name', '?')) for x in tr]
        print(f"{rq} tool_results={len(tr)} names={names} turns={d.get('turns')}")
        print('   ANSWER:', str(d.get('content', ''))[:120].encode('ascii', 'replace').decode().replace('\n', ' '))
        out.append({'rq': rq, 'result': d})
    except Exception as e:
        print(f"{rq} EXC {e!r}"); out.append({'rq': rq, 'error': repr(e)})
json.dump(out, open(sys.argv[1], 'w'), indent=1, default=str); print('WROTE', sys.argv[1])
