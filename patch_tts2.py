import re

path = r'C:\Windows\System32\openjarvis\frontend\src\components\Chat\ChatArea.tsx'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

old = '  const lastSpokenIdRef = useRef<string | null>(null);'
new = (
    '  const lastSpokenIdRef = useRef<string | null>(null);\n'
    '  const ttsInFlightRef = useRef<boolean>(false);'
)

if old in content:
    content = content.replace(old, new, 1)
    print('REF: OK')
else:
    print('REF: MATCH FAILED')

old2 = '    lastSpokenIdRef.current = lastMsg.id;\n\n    // Stop any currently playing audio'
new2 = (
    '    if (ttsInFlightRef.current) return;\n'
    '    lastSpokenIdRef.current = lastMsg.id;\n'
    '    ttsInFlightRef.current = true;\n\n'
    '    // Stop any currently playing audio'
)

if old2 in content:
    content = content.replace(old2, new2, 1)
    print('GUARD: OK')
else:
    print('GUARD: MATCH FAILED')

old3 = '    synthesizeSpeech(plainText)\n      .then((blob) => {'
new3 = (
    '    synthesizeSpeech(plainText)\n'
    '      .then((blob) => {'
)

old4 = '        audio.onended = () => URL.revokeObjectURL(url);\n      })\n      .catch(() => {});\n  }, [streamState.isStreaming, messages, muted]);'
new4 = (
    '        audio.onended = () => { URL.revokeObjectURL(url); ttsInFlightRef.current = false; };\n'
    '      })\n'
    '      .catch(() => { ttsInFlightRef.current = false; });\n'
    '  }, [streamState.isStreaming, messages, muted]);'
)

if old4 in content:
    content = content.replace(old4, new4, 1)
    print('RESET: OK')
else:
    print('RESET: MATCH FAILED')

with open(path, 'w', encoding='utf-8', newline='\n') as f:
    f.write(content)
