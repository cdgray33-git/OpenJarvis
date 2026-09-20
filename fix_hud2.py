f = open(r'C:\Windows\System32\OpenJarvis\frontend\src\components\Chat\ChatArea.tsx', 'r', encoding='latin-1')
content = f.read()
f.close()

old = "      <div style={{ \n        position: 'fixed', \n        top: 120, \n        right: 20, \n        zIndex: 999998 \n      }}>\n        <ThinkingCircle \n          state={streamState.isStreaming ? \"thinking\" : \"idle\"} \n          size={80} \n        />\n      </div>"

new = "      <div style={{ \n        position: 'fixed', \n        top: 120, \n        right: 20, \n        zIndex: 999998 \n      }}>\n        <ThinkingCircle \n          isLoading={streamState.isStreaming}\n          phase={streamState.isStreaming ? \"processing...\" : undefined}\n          variant=\"cyan\"\n        />\n      </div>"

if old in content:
    content = content.replace(old, new)
    f = open(r'C:\Windows\System32\OpenJarvis\frontend\src\components\Chat\ChatArea.tsx', 'w', encoding='latin-1')
    f.write(content)
    f.close()
    print('Done - replaced successfully')
else:
    print('MATCH FAILED - old string not found')
