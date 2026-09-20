f = open(r'C:\Windows\System32\OpenJarvis\src\openjarvis\server\cloud_router.py', 'r', encoding='utf-8')
content = f.read()
f.close()

content = content.replace('import asyncio`nimport asyncio\nimport httpx', 'import asyncio\nimport httpx')
content = content.replace('import asyncio`nimport asyncio\r\nimport httpx', 'import asyncio\nimport httpx')

f = open(r'C:\Windows\System32\OpenJarvis\src\openjarvis\server\cloud_router.py', 'w', encoding='utf-8')
f.write(content)
f.close()
print('Done')
