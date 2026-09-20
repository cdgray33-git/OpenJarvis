f = open(r'C:\Windows\System32\OpenJarvis\frontend\src\components\Chat\ChatArea.tsx', 'r', encoding='latin-1')
content = f.read()
f.close()

old = '''      <div style={{
        position: 'fixed',
        top: 120,
        right: 20,
        zIndex: 999998
      }}>
        <ThinkingCircle
          state={streamState.isStreaming ? "thinking" : "idle"}
          size={80}
        />
      </div>'''

new = '''      <div style={{
        position: 'fixed',
        top: 120,
        right: 20,
        zIndex: 999998
      }}>
        <ThinkingCircle
          isLoading={streamState.isStreaming}
          phase={streamState.isStreaming ? "processing..." : undefined}
          variant="cyan"
        />
      </div>'''

if old in content:
    content = content.replace(old, new)
    f = open(r'C:\Windows\System32\OpenJarvis\frontend\src\components\Chat\ChatArea.tsx', 'w', encoding='latin-1')
    f.write(content)
    f.close()
    print('Done - replaced successfully')
else:
    print('MATCH FAILED - old string not found')
