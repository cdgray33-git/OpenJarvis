import re
path = r'C:\Windows\System32\OpenJarvis\frontend\src\components\chat\InputArea.tsx'
text = open(path, 'r', encoding='utf-8-sig').read()

# Replace the paperclip button handler
text = text.replace(
  "        <button\n          onClick={() => fileInputRef.current?.click()}\n          disabled={streamState.isStreaming}",
  "        <button\n          onClick={async () => { const { open } = await import('@tauri-apps/plugin-dialog'); const file = await open({ multiple: false, filters: [{ name: 'Files', extensions: ['png','jpg','jpeg','pdf','txt','md','csv','json'] }] }); if (file) setInput((prev) => prev + (prev ? ' ' : '') + `[Attached: ${file}]`); }}\n          disabled={streamState.isStreaming}"
)
open(path, 'w', encoding='utf-8', newline='\n').write(text)
print('Done')
