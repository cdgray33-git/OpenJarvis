from collections import defaultdict
from openjarvis.tools.mailbox_tools import connector_for

c = connector_for('yahoo_main')
h = c.find_messages(from_addr='linkedin', limit=3000)
g = defaultdict(list)
for x in h:
    if x['folder'] != 'Trash':
        g[x['folder']].append(x['uid'])

print('plan', {k: len(v) for k, v in g.items()}, 'total', sum(len(v) for v in g.values()))
tot = 0
for f, u in sorted(g.items(), key=lambda kv: -len(kv[1])):
    r = c.move_to_trash(f, u, dry_run=False)
    d = r.get('deleted_count') or 0
    tot += d
    print(f, 'copied', r.get('copied_count'), 'deleted', d, 'failed', r.get('failed_uids'))
print('TOTAL DELETED', tot)
