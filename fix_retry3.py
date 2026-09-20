f = open(r'C:\Windows\System32\OpenJarvis\src\openjarvis\server\cloud_router.py', 'r', encoding='utf-8')
content = f.read()
f.close()

old = '                resp.raise_for_status()\n            async for line in resp.aiter_lines():\n                if not line.startswith("data: "):\n                    continue\n                data = line[6:].strip()\n                if data == "[DONE]":\n                    break\n                try:\n                    chunk = json.loads(data)\n                    delta = chunk["choices"][0]["delta"].get("content") or ""\n                    if delta:\n                        yield delta\n                except Exception:\n                    pass'

new = '                resp.raise_for_status()\n                async for line in resp.aiter_lines():\n                    if not line.startswith("data: "):\n                        continue\n                    data = line[6:].strip()\n                    if data == "[DONE]":\n                        break\n                    try:\n                        chunk = json.loads(data)\n                        delta = chunk["choices"][0]["delta"].get("content") or ""\n                        if delta:\n                            yield delta\n                    except Exception:\n                        pass\n                return'

if old in content:
    content = content.replace(old, new)
    f = open(r'C:\Windows\System32\OpenJarvis\src\openjarvis\server\cloud_router.py', 'w', encoding='utf-8')
    f.write(content)
    f.close()
    print('Done - replaced successfully')
else:
    print('MATCH FAILED - old string not found')
