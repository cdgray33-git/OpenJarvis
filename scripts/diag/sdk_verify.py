# W77 Surface C: author SDK ask_full -> AgentResult.tool_results = proof of INVOCATION. Non-interactive.
import inspect, json, sys
try:
    from openjarvis import Jarvis
except Exception:
    from openjarvis.sdk import Jarvis
print('JARVIS', inspect.getsourcefile(Jarvis))
print('INIT', inspect.signature(Jarvis.__init__)); sig = inspect.signature(Jarvis.ask_full); print('ASK_FULL', sig)
CHECKS = [('RQ-022', ['calculator'], 'What is 137 * 42?'),
          ('RQ-021', ['calculator', 'web_search'], 'What is the GDP of France in USD?'),
          ('RQ-025', ['llm'], 'Summarize: The quarterly review found that support tickets fell 18 percent after the new triage process, while response times improved from 9 hours to 4 hours, and customer satisfaction rose to its highest level in two years.')]
ser = lambda o: getattr(o, '__dict__', repr(o))
j = Jarvis(); out = []
for rq, tools, prompt in CHECKS:
    kw = {k: v for k, v in (('agent', 'orchestrator'), ('tools', tools)) if k in sig.parameters}
    try:
        r = j.ask_full(prompt, **kw)
        d = r if isinstance(r, dict) else ser(r)
        tr = d.get('tool_results') or []
        names = [(x.get('tool_name') or x.get('name')) if isinstance(x, dict) else getattr(x, 'tool_name', getattr(x, 'name', repr(x))) for x in tr]
        content = str(d.get('content', ''))
        print(f"{rq} kwargs={list(kw)} keys={sorted(d)} tool_results={len(tr)} names={names}")
        print('   ANSWER:', content[:150].encode('ascii', 'replace').decode().replace('\n', ' '))
        out.append({'rq': rq, 'kwargs': kw, 'result': d})
    except Exception as e:
        print(f"{rq} EXC {e!r}"); out.append({'rq': rq, 'kwargs': kw, 'error': repr(e)})
try: j.close()
except Exception: pass
json.dump(out, open(sys.argv[1], 'w'), indent=1, default=ser); print('WROTE', sys.argv[1])
