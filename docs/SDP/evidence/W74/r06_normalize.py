import csv, re
from collections import Counter
R=r'C:\Users\Admin\OpenJarvis'; lab=re.compile(r'^(PATH|STATUS|CHANGE|PURPOSE|CLASS|SECURITY|RISK|CARRY|EVIDENCE)\s*:\s*')
rows=list(csv.reader(open(R+r'\R06-W74-JUSTIFY-RAWPARSE.csv',newline='',encoding='utf-8'))); hdr=rows[0]; body=rows[1:]; fixed=0
for r in body:
    for i in range(2,len(r)):
        n=lab.sub('',r[i].strip())
        if n!=r[i]: fixed+=1; r[i]=n
    r[8]=(r[8].split() or [''])[0].upper()
csv.writer(open(R+r'\R06-W74-JUSTIFY.csv','w',newline='',encoding='utf-8')).writerows([hdr]+body)
print('rows',len(body),'| fields de-labelled',fixed,'| labelled rows by batch',dict(Counter(r[0] for r in rows[1:] if any(lab.match(x) for x in r[2:]))) if False else '')
print('CLASS:',dict(Counter(r[5] for r in body))); print('CARRY:',dict(Counter(r[8] for r in body)))
print('RISK:',dict(Counter(r[7].split(':')[0].strip().upper() for r in body)))
print('SECURITY:',dict(Counter(s.strip() for r in body for s in r[6].split(','))))
print('== HIGH'); [print('  ',r[1],'|',r[5],'|',r[6],'|',r[7]) for r in body if r[7].upper().startswith('HIGH')]
print('== PURPOSE UNKNOWN'); [print('  ',r[1],'|',r[5]) for r in body if r[4].upper().startswith('UNKNOWN')]
print('== CARRY REVIEW'); [print('  ',r[1],'|',r[3][:90]) for r in body if r[8]=='REVIEW']
