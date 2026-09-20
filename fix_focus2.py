import re
path = r'C:\Windows\System32\OpenJarvis\frontend\src\components\chat\InputArea.tsx'
text = open(path, 'r', encoding='utf-8-sig').read()
text = text.replace(
    'const t = setTimeout(() => textareaRef.current?.focus(), 300);',
    'const t = setTimeout(() => textareaRef.current?.focus(), 1000);'
)
open(path, 'w', encoding='utf-8', newline='\n').write(text)
print('Done')
