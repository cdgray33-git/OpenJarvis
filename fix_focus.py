import re
path = r'C:\Windows\System32\OpenJarvis\frontend\src\components\chat\InputArea.tsx'
text = open(path, 'r', encoding='utf-8-sig').read()
text = text.replace(
  '  // Auto-focus textarea on mount and after streaming completes\n  useEffect(() => {\n    textareaRef.current?.focus();\n  }, []);',
  '  // Auto-focus textarea on mount and after streaming completes\n  useEffect(() => {\n    const t = setTimeout(() => textareaRef.current?.focus(), 300);\n    return () => clearTimeout(t);\n  }, []);'
)
open(path, 'w', encoding='utf-8', newline='\n').write(text)
print('Done')
