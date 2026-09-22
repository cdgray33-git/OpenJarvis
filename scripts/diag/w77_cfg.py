from openjarvis.core.config import load_config
c = load_config()
t = getattr(c.agent, 'tools', None)
print('agent.tools TYPE :', type(t).__name__)
print('default_agent    :', c.agent.default_agent)
print('server.agent     :', getattr(getattr(c, 'server', None), 'agent', 'NO server.agent'))
print('max_turns        :', c.agent.max_turns)
ts = getattr(c, 'tools', None)
print('[tools] section  :', 'ABSENT' if ts is None else repr(getattr(ts, 'enabled', 'present, no .enabled')))
if isinstance(t, str):
    print('SPLIT WOULD GIVE :', len([x for x in t.split(',') if x.strip()]), 'tools')
    print('ITER GIVES       :', len(t), 'single CHARACTERS (if iterated as-is)')
