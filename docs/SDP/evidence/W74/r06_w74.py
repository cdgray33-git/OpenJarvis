import sys, os, re, json, csv, subprocess, urllib.request, urllib.error
REPO=r'C:\Users\Admin\OpenJarvis'; UP=r'C:\Users\Admin\upstream-OpenJarvis'; BASE='af21bc18'; HEADC='88a71af'
CSVIN=os.path.join(REPO,'PROVENANCE-W74-classified.csv'); PLAN=os.path.join(REPO,'R06-W74-PLAN.json')
mode=sys.argv[1] if len(sys.argv)>1 else 'plan'
PROMPT='''You are assisting an authorization-to-operate (ATO) review of a software system.
BASELINE: upstream open-jarvis/OpenJarvis commit af21bc18 (2026-05-19). TARGET: Graystone fork commit 88a71af.
Below are unified diffs for every file in this batch. Status A = new file (shown whole). Status M = modified vs baseline.
For EACH file listed, write exactly one line in this pipe-delimited format and nothing else (no header, no table, no commentary):
PATH|STATUS|CHANGE|PURPOSE|CLASS|SECURITY|RISK|CARRY|EVIDENCE
PATH: exactly as listed. STATUS: A or M. CHANGE: what changed, 25 words max.
PURPOSE: why, as evident from code, comments, or names; write UNKNOWN if not evident. Do not guess.
CLASS: one of BUGFIX, FEATURE, PLATFORM-WINDOWS, CONFIG, INTEGRATION, UI, INSTRUMENTATION, SECURITY-FIX, REFACTOR, UNCLEAR.
SECURITY: comma list from NONE, AUTH, NETWORK, SECRETS, SUBPROCESS, FILESYSTEM-WRITE, TOOL-EXECUTION, CONFIRMATION-GATE, CORS-CSP, EMAIL, EXTERNAL-API.
RISK: LOW, MEDIUM or HIGH, then a colon and the reason in 12 words max.
CARRY: carry into a clean rebuild on Ubuntu Linux? YES, NO (Windows-only or obsolete), or REVIEW.
EVIDENCE: function or hunk names supporting PURPOSE, 15 words max.
Never use the pipe character inside a field. Every listed file must get a line. ASCII only.
'''
SEC=[re.compile(r'sk-[A-Za-z0-9_-]{16,}'),re.compile(r'AKIA[0-9A-Z]{16}'),re.compile(r'(api[_-]?key|password|passwd|secret|token)\s*[:=]\s*["\'][^"\'\s]{8,}["\']',re.I)]
def diff(p):
    r=subprocess.run(['git','-C',UP,'--no-pager','diff','--no-renames','-U10',BASE,HEADC,'--',p],capture_output=True)
    return r.stdout.decode('utf-8','replace')
if mode=='plan':
    rows=sorted([r for r in csv.DictReader(open(CSVIN,newline='',encoding='ascii')) if r['Category']=='PRODUCT'],key=lambda r:r['Path'])
    ms=json.load(urllib.request.urlopen(urllib.request.Request('https://openrouter.ai/api/v1/models',headers={'User-Agent':'r06-w74'}),timeout=60))['data']
    hit=[m for m in ms if 'nemotron' in m['id'].lower() and '550' in m['id']]
    if not hit:
        print('NO 550B MODEL FOUND. nemotron ids:',[m['id'] for m in ms if 'nemotron' in m['id'].lower()]); sys.exit(1)
    m=hit[0]; ctx=int(m.get('context_length') or 0); budget=int(ctx*4*0.35)-len(PROMPT)-4000
    print('model:',m['id'],'| context_length:',ctx,'| batch budget chars:',budget)
    batches=[]; cur=[]; size=0; secs=[]; over=[]
    for r in rows:
        d=diff(r['Path']); blk='\n===== FILE: %s (status %s) =====\n%s'%(r['Path'],r['Status'],d)
        for i,ln in enumerate(d.splitlines()):
            if ln.startswith('+') and any(s.search(ln) for s in SEC): secs.append('%s diffline %d'%(r['Path'],i+1))
        if len(blk)>budget: over.append(r['Path'])
        if cur and size+len(blk)>budget: batches.append(cur); cur=[]; size=0
        cur.append((r['Path'],r['Status'],blk)); size+=len(blk)
    if cur: batches.append(cur)
    plan={'model':m['id'],'context':ctx,'batches':[]}
    for n,b in enumerate(batches,1):
        fn=os.path.join(REPO,'R06-W74-B%d.md'%n); lst='\n'.join('%s (%s)'%(p,s) for p,s,_ in b)
        open(fn,'w',encoding='utf-8',newline='\n').write(PROMPT+'\nFILES IN THIS BATCH (%d):\n%s\n'%(len(b),lst)+''.join(x for _,_,x in b))
        plan['batches'].append({'file':fn,'paths':[p for p,_,_ in b]}); print('B%d: %d files, %d chars'%(n,len(b),os.path.getsize(fn)))
    json.dump(plan,open(PLAN,'w'),indent=1)
    print('files planned:',sum(len(b) for b in batches),'of',len(rows)); print('oversize single files:',over or 'none')
    print('secret-pattern hits:',len(secs)); [print('  SEC',s) for s in secs]
    print('PLAN ->',PLAN)
if mode=='send':
    from collections import Counter
    import time
    plan=json.load(open(PLAN)); key=os.environ.get('OPENROUTER_API_KEY',''); src='env'; keyf=r'C:\Users\Admin\.openjarvis\cloud-keys.env'
    if not key and os.path.exists(keyf):
        src=keyf
        for ln in open(keyf,encoding='utf-8',errors='replace'):
            k,_,v=ln.strip().partition('=')
            if k.strip()=='OPENROUTER_API_KEY': key=v.strip().strip('"').strip("'"); break
    if not key: print('NO KEY in env or',keyf); sys.exit(1)
    print('key: found in',src,'| prefix_ok',key.startswith('sk-or-'))
    cands=[plan['model'],plan['model']+':free']
    ms={m['id']:m for m in json.load(urllib.request.urlopen(urllib.request.Request('https://openrouter.ai/api/v1/models',headers={'User-Agent':'r06-w74'}),timeout=60))['data']}
    for c in cands: print('candidate',c,'| listed',c in ms,'| context',ms.get(c,{}).get('context_length'))
    rows=[]; dead=set()
    for n,b in enumerate(plan['batches'],1):
        content=open(b['file'],encoding='utf-8').read(); resp=None; used=None
        for mid in [c for c in cands if c in ms and c not in dead]:
            for attempt in range(3):
                body=json.dumps({'model':mid,'messages':[{'role':'user','content':content}],'max_tokens':32000,'temperature':0}).encode()
                req=urllib.request.Request('https://openrouter.ai/api/v1/chat/completions',data=body,headers={'Authorization':'Bearer '+key,'Content-Type':'application/json','X-Title':'r06-w74'})
                try: resp=urllib.request.urlopen(req,timeout=1200).read().decode('utf-8','replace'); used=mid; break
                except urllib.error.HTTPError as e:
                    print('B%d %s HTTP %d: %s'%(n,mid,e.code,e.read().decode('utf-8','replace')[:300]))
                    if e.code==429 and attempt<2: time.sleep(60); continue
                    if e.code==402: dead.add(mid)
                    break
                except Exception as e: print('B%d %s FAILED: %r'%(n,mid,e)); break
            if resp: break
        if not resp: print('B%d: NO RESPONSE'%n); continue
        open(os.path.join(REPO,'R06-W74-B%d-RAW.json'%n),'w',encoding='utf-8').write(resp)
        j=json.loads(resp)
        if 'error' in j: print('B%d API ERROR: %s'%(n,str(j['error'])[:400])); continue
        ch=(j.get('choices') or [{}])[0]; mg=ch.get('message',{}); txt=mg.get('content') or ''
        if not txt.strip() and mg.get('reasoning'): txt=mg['reasoning']; print('B%d: content empty, parsing reasoning field'%n)
        u=j.get('usage',{}); print('B%d via %s: in %s out %s finish %s | chars %d'%(n,used,u.get('prompt_tokens'),u.get('completion_tokens'),ch.get('finish_reason'),len(txt)))
        want=set(b['paths'])
        for ln in txt.splitlines():
            f=[re.sub(r'^(PATH|STATUS|CHANGE|PURPOSE|CLASS|SECURITY|RISK|CARRY|EVIDENCE)\s*:\s*','',x.strip().strip('`')) for x in ln.strip().lstrip('-* ').split('|')]
            if len(f)>=9 and f[0] in want: rows.append([n]+f[:8]+['|'.join(f[8:])])
    out=os.path.join(REPO,'R06-W74-JUSTIFY.csv')
    with open(out,'w',newline='',encoding='utf-8') as fh:
        w=csv.writer(fh); w.writerow(['Batch','Path','Status','Change','Purpose','Class','Security','Risk','Carry','Evidence']); w.writerows(rows)
    allp=[p for b in plan['batches'] for p in b['paths']]; got=[r[1] for r in rows]
    miss=[p for p in allp if p not in got]; dup=sorted({p for p in got if got.count(p)>1})
    print('covered: %d of %d | missing: %d | duplicates: %d'%(len(set(got)),len(allp),len(miss),len(dup)))
    for p in miss: print('  MISSING',p)
    for p in dup: print('  DUP',p)
    print('CARRY:',dict(Counter((r[8].split() or [''])[0] for r in rows))); print('CLASS:',dict(Counter(r[5] for r in rows)))
    print('RISK HIGH:'); [print('  ',r[1],'-',r[7]) for r in rows if r[7].upper().startswith('HIGH')]
    print('OUT ->',out)

