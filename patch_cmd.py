path = r'C:\Windows\System32\openjarvis\frontend\src\components\CommandPalette.tsx'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

old = 'const entry = status.find((s) => s.key === p.envKey);'
new = 'const entry = (status as Array<{key: string; value: string}>).find((s) => s.key === p.envKey);'

if old in content:
    content = content.replace(old, new, 1)
    with open(path, 'w', encoding='utf-8', newline='\n') as f:
        f.write(content)
    print('OK')
else:
    print('MATCH FAILED')
