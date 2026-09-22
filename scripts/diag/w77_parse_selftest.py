from openjarvis.agents._stubs import ToolUsingAgent
class T:
    name = "web_search"
class P(ToolUsingAgent):
    def __init__(self): self._tools = [T()]
    def run(self, *a, **k): pass
p = P()
payload = "<function=web_search>\n<parameter=query>\nFrance GDP 2023 USD\n</parameter>\n</function>\n</tool_call>"
print('RQ-021 PARSE:', p._extract_text_tool_call(payload))
print('KNOWN GATE  :', (p._extract_text_tool_call(payload) or ("",))[0] in p._known_tool_names())
print('PROSE SAFE  :', p._extract_text_tool_call("The GDP of France was about 2.86 trillion USD in 2023."))
print('JSON FORM   :', p._extract_text_tool_call('{"name": "web_search", "arguments": {"query": "x"}}'))
print('GLM  KEYVAL:', p._extract_text_tool_call("<tool_call>web_search\nquery: France GDP\n</tool_call>"))
print('XML  DOLLAR:', p._extract_text_tool_call("<tool_call>web_search\n$query=France GDP\n</tool_call>"))
print('XML  TAGGED:', p._extract_text_tool_call("<tool_call>web_search\n<query>France GDP</query></tool_call>"))
