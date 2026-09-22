import ast, os, shutil, sys, time
R = os.getcwd(); ST = time.strftime('%Y%m%d_%H%M%S')
B = os.path.join(R, 'src', 'openjarvis', 'agents', '_stubs.py')
OLD = '''            return (tool_name, _json.dumps(params) if params else "{}")
'''
NEW = '''            if not params:
                for m in re.finditer(r"(\\w+)\\s*:\\s*(.+?)(?=\\n\\w+\\s*:|$)", raw_params, re.DOTALL):
                    key, val = m.group(1), m.group(2).strip().strip(chr(34) + chr(39))
                    try:
                        params[key] = int(val)
                    except ValueError:
                        params[key] = val
            return (tool_name, _json.dumps(params) if params else "{}")
'''
with open(B, 'r', encoding='utf-8', newline='') as f: b = f.read()
print('ANCHOR count', b.count(OLD), '| already patched:', 'w77-textparse-v2' in b)
if b.count(OLD) != 1 or 'w77-textparse-v2' in b:
    print('ABORT - anchor not unique or already applied'); sys.exit(1)
nb = b.replace(OLD, NEW).replace('openjarvis-w77-textparse-v1', 'openjarvis-w77-textparse-v2')
ast.parse(nb); print('AST OK', len(b), '->', len(nb))
bak = B + '.bak_w77parity_' + ST
shutil.copy2(B, bak)
with open(B, 'w', encoding='utf-8', newline='') as f: f.write(nb)
print('WROTE', B, '| BAK', os.path.basename(bak))
