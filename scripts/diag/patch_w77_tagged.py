import ast, os, shutil, sys, time
R = os.getcwd(); ST = time.strftime('%Y%m%d_%H%M%S')
B = os.path.join(R, 'src', 'openjarvis', 'agents', '_stubs.py')
OLD = 'xml_match = re.search(r"<tool_call>\\s*(\\w+)\\s*(.*?)</\\w+>", text, re.DOTALL)'
NEW = 'xml_match = re.search(r"<tool_call>\\s*(\\w+)\\s*(.*?)(?:</tool_call>|\\Z)", text, re.DOTALL)'
with open(B, 'r', encoding='utf-8', newline='') as f: b = f.read()
print('ANCHOR count', b.count(OLD), '| already applied:', b.count(NEW))
if b.count(OLD) != 1:
    print('ABORT - anchor not unique'); sys.exit(1)
nb = b.replace(OLD, NEW).replace('openjarvis-w77-textparse-v2', 'openjarvis-w77-textparse-v3')
ast.parse(nb); print('AST OK', len(b), '->', len(nb))
bak = B + '.bak_w77tagged_' + ST
shutil.copy2(B, bak)
with open(B, 'w', encoding='utf-8', newline='') as f: f.write(nb)
print('WROTE', B, '| BAK', os.path.basename(bak))
