f = open(r'C:\Windows\System32\OpenJarvis\src\openjarvis\server\cloud_router.py', 'r', encoding='utf-8')
content = f.read()
f.close()

old = '    async with httpx.AsyncClient(timeout=180) as client:\n        async with client.stream(\n            "POST",\n            f"{base_url}/chat/completions",\n            json=payload,\n            headers={\n                "Authorization": f"Bearer {api_key}",\n                "Content-Type": "application/json",\n            },\n        ) as resp:\n            resp.raise_for_status()'

new = '    _retry_delays = [5, 10, 20]\n    async with httpx.AsyncClient(timeout=180) as client:\n        for _attempt, _delay in enumerate([0] + _retry_delays):\n            if _delay:\n                import sys; print(f"[RETRY] 429 received, waiting {_delay}s", flush=True, file=sys.stderr)\n                await asyncio.sleep(_delay)\n            async with client.stream(\n                "POST",\n                f"{base_url}/chat/completions",\n                json=payload,\n                headers={\n                    "Authorization": f"Bearer {api_key}",\n                    "Content-Type": "application/json",\n                },\n            ) as resp:\n                if resp.status_code == 429:\n                    if _attempt < len(_retry_delays):\n                        continue\n                    yield "\n\n?? Rate limited by OpenRouter. Try a different model or wait a moment."\n                    return\n                resp.raise_for_status()'

if old in content:
    content = content.replace(old, new)
    f = open(r'C:\Windows\System32\OpenJarvis\src\openjarvis\server\cloud_router.py', 'w', encoding='utf-8')
    f.write(content)
    f.close()
    print('Done - replaced successfully')
else:
    print('MATCH FAILED - old string not found')
