f = open(r'C:\Windows\System32\OpenJarvis\src\openjarvis\server\cloud_router.py', 'r', encoding='utf-8')
content = f.read()
f.close()
print(repr(content[content.find('yield "'):content.find('yield "')+80]))
