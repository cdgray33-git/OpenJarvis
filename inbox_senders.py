from collections import defaultdict
from openjarvis.tools.mailbox_tools import connector_for

c = connector_for('yahoo_main')
h = c.find_messages(folder='Inbox', limit=20000)
print('inbox messages seen:', len(h))

agg = defaultdict(lambda: [0, 0])
for x in h:
    a = (x.get('from_addr') or '?').lower()
    agg[a][0] += 1
    agg[a][1] += x.get('bytes') or 0

rows = sorted(agg.items(), key=lambda kv: -kv[1][1])[:40]
tot = 0
for a, (n, b) in rows:
    tot += b
    print('%8.1f MB %6d  %s' % (b / 1048576, n, a))
print('top-40 total MB:', round(tot / 1048576, 1))
print('inbox total MB:', round(sum(v[1] for v in agg.values()) / 1048576, 1))
