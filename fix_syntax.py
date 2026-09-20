f = open(r'C:\Windows\System32\OpenJarvis\src\openjarvis\server\cloud_router.py', 'r', encoding='utf-8')
content = f.read()
f.close()

old = '                    yield "\n\n?? Rate limited by OpenRouter. Try a different model or wait a moment."'
new = '                    yield "\\n\\nRate limited by OpenRouter. Try a different model or wait a moment."'

if old in content:
    content = content.replace(old, new)
    f = open(r'C:\Windows\System32\OpenJarvis\src\openjarvis\server\cloud_router.py', 'w', encoding='utf-8')
    f.write(content)
    f.close()
    print('Done - replaced successfully')
else:
    print('MATCH FAILED - old string not found')
