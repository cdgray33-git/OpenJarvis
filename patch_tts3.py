path = r'C:\Windows\System32\openjarvis\frontend\src\components\Chat\ChatArea.tsx'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

old = '    synthesizeSpeech(plainText)\n      .then((blob) => {\n        const url = URL.createObjectURL(blob);\n        const audio = new Audio(url);\n        audioRef.current = audio;\n        audio.play().catch(() => {});\n        audio.onended = () => { URL.revokeObjectURL(url); ttsInFlightRef.current = false; };\n      })\n      .catch(() => { ttsInFlightRef.current = false; });'

new = '    synthesizeSpeech(plainText)\n      .then((blob) => {\n        const url = URL.createObjectURL(blob);\n        const audio = new Audio(url);\n        audioRef.current = audio;\n        const release = () => { URL.revokeObjectURL(url); ttsInFlightRef.current = false; };\n        audio.onended = release;\n        audio.onerror = release;\n        audio.play().catch(release);\n        // Safety timeout - release lock after 60s max\n        setTimeout(() => { ttsInFlightRef.current = false; }, 60000);\n      })\n      .catch(() => { ttsInFlightRef.current = false; });'

if old in content:
    content = content.replace(old, new, 1)
    with open(path, 'w', encoding='utf-8', newline='\n') as f:
        f.write(content)
    print('OK')
else:
    print('MATCH FAILED')
