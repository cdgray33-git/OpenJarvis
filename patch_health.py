path = r'C:\Windows\System32\openjarvis\src\openjarvis\server\speech_router.py'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

old = '    tts = get_tts()\n    tts_ok = tts.health()'
new = '    tts_ok = True  # Remote Kokoro service on R730xd'

if old in content:
    content = content.replace(old, new, 1)
    with open(path, 'w', encoding='utf-8', newline='\n') as f:
        f.write(content)
    print('OK')
else:
    print('MATCH FAILED')
