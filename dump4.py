f = open(r'C:\Windows\System32\OpenJarvis\src\openjarvis\server\cloud_router.py', 'r', encoding='utf-8')
lines = f.readlines()
f.close()
for i, line in enumerate(lines[175:190], start=176):
    print(f"{i}: {repr(line)}")
