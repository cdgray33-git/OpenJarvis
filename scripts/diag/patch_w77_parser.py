import ast, os, shutil, sys, time
R = os.getcwd(); ST = time.strftime('%Y%m%d_%H%M%S')
B = os.path.join(R, 'src', 'openjarvis', 'agents', '_stubs.py')
O = os.path.join(R, 'src', 'openjarvis', 'agents', 'orchestrator.py')
METHODS = '''
    # --- openjarvis-w77-textparse-v1: shared text tool-call parser ---
    def _extract_text_tool_call(self, text):
        """Parse a tool call emitted as TEXT when native tool_calls is empty."""
        action_match = re.search(r"Action:\\s*(.+)", text, re.IGNORECASE)
        input_match = re.search(r"Action Input:\\s*(.+?)(?=\\n\\n|\\Z)", text, re.DOTALL | re.IGNORECASE)
        if action_match:
            return (action_match.group(1).strip(), input_match.group(1).strip() if input_match else "{}")
        xml_match = re.search(r"<tool_call>\\s*(\\w+)\\s*(.*?)</\\w+>", text, re.DOTALL)
        if xml_match:
            tool_name = xml_match.group(1).strip()
            raw_params = xml_match.group(2).strip()
            params = {}
            for m in re.finditer(r"\\$(\\w+)=(.+?)(?=\\$|\\n<|</|$)", raw_params, re.DOTALL):
                params[m.group(1)] = m.group(2).strip().rstrip("</>\\n")
            for m in re.finditer(r"<(\\w+)>(.*?)</\\1>", raw_params, re.DOTALL):
                key, val = m.group(1), m.group(2).strip()
                try:
                    params[key] = int(val)
                except ValueError:
                    params[key] = val
            return (tool_name, _json.dumps(params) if params else "{}")
        fn_match = re.search(r"<function\\s*=\\s*[\\"\\']?([\\w.\\-]+)[\\"\\']?\\s*>(.*?)(?:</function>|\\Z)", text, re.DOTALL)
        if fn_match:
            fn_params = {}
            for _pm in re.finditer(r"<parameter\\s*=\\s*[\\"\\']?([\\w.\\-]+)[\\"\\']?\\s*>(.*?)(?:</parameter>|\\Z)", fn_match.group(2), re.DOTALL):
                _val = _pm.group(2).strip()
                try:
                    fn_params[_pm.group(1)] = int(_val)
                except ValueError:
                    fn_params[_pm.group(1)] = _val
            return (fn_match.group(1).strip(), _json.dumps(fn_params))
        return self._extract_json_text_call(text)

    def _extract_json_text_call(self, text):
        """Bare JSON tool call: {"name": "...", "arguments": {...}}."""
        start = text.find("{")
        while start != -1:
            depth = 0
            in_str = False
            esc = False
            for j in range(start, len(text)):
                ch = text[j]
                if in_str:
                    if esc:
                        esc = False
                    elif ch == chr(92):
                        esc = True
                    elif ch == chr(34):
                        in_str = False
                    continue
                if ch == chr(34):
                    in_str = True
                elif ch == "{":
                    depth += 1
                elif ch == "}":
                    depth -= 1
                    if depth == 0:
                        try:
                            obj = _json.loads(text[start:j + 1])
                        except Exception:
                            obj = None
                        if isinstance(obj, dict):
                            nm = obj.get("name") or obj.get("tool")
                            ar = obj.get("arguments", obj.get("parameters", obj.get("input")))
                            if isinstance(nm, str) and ar is not None:
                                return (nm, ar if isinstance(ar, str) else _json.dumps(ar))
                        break
            start = text.find("{", start + 1)
        return None

    def _known_tool_names(self):
        names = set()
        for _t in (self._tools or []):
            _n = getattr(_t, "name", None) or getattr(_t, "tool_id", None)
            if _n:
                names.add(str(_n))
        return names

'''
WIRE = '''            # openjarvis-w77-textparse-v1: native tool_calls empty -> try a TEXT call
            if not raw_tool_calls and self._tools:
                _tc = self._extract_text_tool_call(content)
                if _tc is not None and _tc[0] in self._known_tool_names():
                    raw_tool_calls = [{"id": "orch_text_%d" % turns, "name": _tc[0], "arguments": _tc[1]}]

'''
def rd(p):
    with open(p, 'r', encoding='utf-8', newline='') as f: return f.read()
def wr(p, s):
    with open(p, 'w', encoding='utf-8', newline='') as f: f.write(s)
edits = []
b = rd(B)
a1 = 'import re\nfrom abc import ABC, abstractmethod'
a2 = '\n__all__ = ["AgentContext", "AgentResult", "BaseAgent", "ToolUsingAgent"]'
for a in (a1, a2, 'openjarvis-w77-textparse-v1'):
    print('ANCHOR', repr(a[:40]), b.count(a))
if b.count(a1) != 1 or b.count(a2) != 1 or 'openjarvis-w77-textparse-v1' in b:
    print('STUBS ANCHORS BAD - ABORT'); sys.exit(1)
nb = b.replace(a1, 'import json as _json\nimport re\nfrom abc import ABC, abstractmethod').replace(a2, METHODS + a2)
o = rd(O)
a3 = '            # No tool calls -> check continuation, then final answer\n            if not raw_tool_calls:'
print('ANCHOR orch', o.count(a3), 'marker', o.count('openjarvis-w77-textparse-v1'))
if o.count(a3) != 1 or 'openjarvis-w77-textparse-v1' in o:
    print('ORCH ANCHOR BAD - ABORT'); sys.exit(1)
no = o.replace(a3, WIRE + a3)
for p, s in ((B, nb), (O, no)):
    ast.parse(s); print('AST OK', os.path.basename(p), len(s))
if '--apply' not in sys.argv:
    print('DRY RUN ONLY'); sys.exit(0)
for p, s in ((B, nb), (O, no)):
    bak = p + '.bak_w77parser_' + ST
    shutil.copy2(p, bak); wr(p, s); print('WROTE', p, '| BAK', os.path.basename(bak))
