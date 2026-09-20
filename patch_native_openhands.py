"""Guarded patch: teach NativeOpenHandsAgent._extract_tool_call to parse
bare JSON tool calls ({"name": ..., "arguments": ...}) that qwen2.5-coder
and similar Ollama models emit as content. Also reports current memory
context-injection config so we can tune the token-bloat separately.

Run:  python patch_native_openhands.py
"""
import io
import os
import sys
import shutil
import datetime
import py_compile

PATH = r"C:\Users\Admin\OpenJarvis\src\openjarvis\agents\native_openhands.py"

# ---- read (preserve CRLF) ----
with io.open(PATH, "r", encoding="utf-8", newline="") as f:
    raw = f.read()
use_crlf = "\r\n" in raw
src = raw.replace("\r\n", "\n")

# ---- guards ----
if "_extract_json_tool_call" in src:
    print("ABORT: already patched (found _extract_json_tool_call). No change made.")
    sys.exit(1)

ANCHOR = "        return None\n\n    def run(\n"
n = src.count(ANCHOR)
print("anchor matches:", n)
if n != 1:
    print("ABORT: anchor not found exactly once. No change made.")
    sys.exit(1)

# ---- new code (inserts Format 3 hook + helper before run()) ----
NEW = '''        # Format 3: bare JSON tool call {"name": "...", "arguments": {...}}
        # Some Ollama models (notably qwen2.5-coder) emit tool calls as JSON
        # in content instead of the structured tool_calls field. Catch it here
        # so the call executes instead of leaking raw JSON into the chat.
        json_call = self._extract_json_tool_call(text)
        if json_call is not None:
            return json_call

        return None

    def _extract_json_tool_call(self, text):
        """Extract a bare JSON tool call: {"name": "...", "arguments": {...}}.

        Fires only on a real tool-call shape (a string ``name``/``tool`` plus an
        ``arguments``/``parameters``/``input`` key), so ordinary JSON in a normal
        answer is left untouched. Scans for the first balanced, string-aware
        JSON object in the text.
        """
        known = set()
        for _t in (self._tools or []):
            _n = getattr(_t, "name", None) or getattr(_t, "tool_id", None)
            if _n:
                known.add(str(_n))
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
                    elif ch == chr(92):  # backslash
                        esc = True
                    elif ch == '"':
                        in_str = False
                    continue
                if ch == '"':
                    in_str = True
                elif ch == "{":
                    depth += 1
                elif ch == "}":
                    depth -= 1
                    if depth == 0:
                        candidate = text[start:j + 1]
                        try:
                            obj = _json.loads(candidate)
                        except Exception:
                            obj = None
                        if isinstance(obj, dict):
                            name = obj.get("name") or obj.get("tool")
                            has_args = (
                                "arguments" in obj
                                or "parameters" in obj
                                or "input" in obj
                            )
                            if isinstance(name, str) and name and (has_args or name in known):
                                if "arguments" in obj:
                                    args = obj.get("arguments")
                                elif "parameters" in obj:
                                    args = obj.get("parameters")
                                else:
                                    args = obj.get("input", {})
                                if isinstance(args, str):
                                    args_json = args
                                else:
                                    args_json = _json.dumps(args or {})
                                return (name, args_json)
                        break
            start = text.find("{", start + 1)
        return None

    def run(
'''

src2 = src.replace(ANCHOR, NEW, 1)

# ---- post-checks ----
if "_extract_json_tool_call" not in src2:
    print("ABORT: insertion marker missing after replace. No change made.")
    sys.exit(1)
if src2.count("def run(\n") != src.count("def run(\n"):
    print("ABORT: run() count changed unexpectedly. No change made.")
    sys.exit(1)

out = src2.replace("\n", "\r\n") if use_crlf else src2

# ---- write to temp, compile-check, then swap ----
tmp = PATH + ".tmp_patch"
with io.open(tmp, "w", encoding="utf-8", newline="") as f:
    f.write(out)
try:
    py_compile.compile(tmp, doraise=True)
except py_compile.PyCompileError as e:
    print("ABORT: patched file failed to compile. Original untouched.")
    print(e)
    os.remove(tmp)
    sys.exit(1)

bak = PATH + ".bak_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
shutil.copy2(PATH, bak)
os.replace(tmp, PATH)
print("PATCH APPLIED OK.")
print("  backup:", bak)
print("  added: _extract_json_tool_call + Format-3 hook")

# ---- report memory context config (read-only, for the bloat fix) ----
print("\n----- memory context config (for the 22K-token bloat) -----")
cfg_path = os.path.expanduser(r"~\.openjarvis\config.toml")
print("config.toml:", cfg_path)
if os.path.exists(cfg_path):
    keys = ("context_from_memory", "context_top_k", "context_min_score",
            "context_max_tokens")
    with io.open(cfg_path, "r", encoding="utf-8") as f:
        found = False
        for ln in f:
            s = ln.strip()
            if any(k in s for k in keys):
                print("  ", s)
                found = True
    if not found:
        print("  (none of the context_* keys set -> using code defaults:")
        print("   context_top_k=5, context_max_tokens=2048, min_score=0.0)")
else:
    print("  NOT FOUND (using code defaults)")