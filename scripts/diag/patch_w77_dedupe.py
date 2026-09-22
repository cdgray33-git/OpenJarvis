import ast, os, shutil, sys, time
R = os.getcwd(); ST = time.strftime('%Y%m%d_%H%M%S')
N = os.path.join(R, 'src', 'openjarvis', 'agents', 'native_openhands.py')
with open(N, 'r', encoding='utf-8', newline='') as f: src = f.read()
lines = src.split('\n')
tree = ast.parse(src)
cls = [n for n in ast.walk(tree) if isinstance(n, ast.ClassDef) and n.name == 'NativeOpenHandsAgent']
if len(cls) != 1: print('CLASS NOT FOUND - ABORT'); sys.exit(1)
targets = {}
for m in cls[0].body:
    if isinstance(m, ast.FunctionDef) and m.name in ('_extract_tool_call', '_extract_json_tool_call'):
        targets[m.name] = (m.lineno, m.end_lineno)
print('FOUND', {k: v for k, v in targets.items()})
if len(targets) != 2: print('EXPECTED 2 METHODS - ABORT'); sys.exit(1)
call_old = 'tool_info = self._extract_tool_call(content)'
print('CALL SITE count', src.count(call_old))
if src.count(call_old) != 1: print('CALL SITE NOT UNIQUE - ABORT'); sys.exit(1)
cut = set()
for name, (a, b) in targets.items():
    for i in range(a - 1, b): cut.add(i)
print('LINES TO REMOVE', len(cut))
kept = [ln for i, ln in enumerate(lines) if i not in cut]
new = '\n'.join(kept).replace(call_old, 'tool_info = self._extract_text_tool_call(content)  # openjarvis-w77-dedupe-v1 (base ToolUsingAgent)')
ast.parse(new); print('AST OK', len(src), '->', len(new))
for bad in ('def _extract_tool_call', 'def _extract_json_tool_call'):
    print('RESIDUAL', bad, new.count(bad))
bak = N + '.bak_w77dedupe_' + ST
shutil.copy2(N, bak)
with open(N, 'w', encoding='utf-8', newline='') as f: f.write(new)
print('WROTE', N, '| BAK', os.path.basename(bak))
