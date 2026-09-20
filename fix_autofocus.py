import re
path = r'C:\Windows\System32\OpenJarvis\frontend\src\components\chat\InputArea.tsx'
text = open(path, 'r', encoding='utf-8-sig').read()
text = text.replace(
  '  // Auto-focus textarea after streaming completes\n  useEffect(() => {\n    if (!streamState.isStreaming) {\n      textareaRef.current?.focus();\n    }\n  }, [streamState.isStreaming]);',
  '  // Auto-focus textarea on mount and after streaming completes\n  useEffect(() => {\n    textareaRef.current?.focus();\n  }, []);\n\n  useEffect(() => {\n    if (!streamState.isStreaming) {\n      textareaRef.current?.focus();\n    }\n  }, [streamState.isStreaming]);'
)
open(path, 'w', encoding='utf-8', newline='\n').write(text)
print('Done')
