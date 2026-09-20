"""Guarded patch: teach NativeOpenHandsAgent._extract_tool_call to parse
OpenHands-style XML tool calls emitted as CONTENT:

    <function=mailbox_find_messages><parameter=from_addr>ziprecruiter</parameter></function>

qwen3-coder:30b emitted exactly this into the chat on 2026-08-12 instead of
firing a structured tool call. _extract_tool_call knew three formats
(Action/Action Input, <tool_call>tool_name..., bare JSON) and none of them
match this shape, so it fell through to the user as prose.

Run:  uv run --no-sync python patch_native_openhands_fmt4.py

Safe to run twice: it aborts if already patched, and aborts if the insertion
anchor is not found exactly once. Takes its own timestamped backup.
"""
import io
import os
import sys
import hashlib
import datetime
import py_compile

PATH = r"C:\Users\Admin\OpenJarvis\src\openjarvis\agents\native_openhands.py"
MARKER = "Format 4: OpenHands XML tool call"
ANCHOR = "        # Format 3: bare JSON tool call"


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        h.update(fh.read())
    return h.hexdigest().upper()


# ---- read (preserve line terminator) ----
if not os.path.exists(PATH):
    print("ABORT: file not found:", PATH)
    sys.exit(1)

with io.open(PATH, "r", encoding="utf-8", newline="") as f:
    raw = f.read()

use_crlf = "\r\n" in raw
src = raw.replace("\r\n", "\n")

print("pre-patch  bytes :", os.path.getsize(PATH))
print("pre-patch  sha256:", sha256(PATH))
print("line ending      :", "CRLF" if use_crlf else "LF")

# ---- guards ----
if MARKER in src:
    print("ABORT: already patched (found marker). No change made.")
    sys.exit(1)

n = src.count(ANCHOR)
print("anchor matches   :", n)
if n != 1:
    print("ABORT: anchor not found exactly once. No change made.")
    sys.exit(1)

# ---- new code, inserted immediately above the Format 3 block ----
NEW = '''        # Format 4: OpenHands XML tool call
        # <function=NAME><parameter=KEY>value</parameter></function>
        # Emitted as content by qwen3-coder when native tool_calls do not fire.
        # \\s*=\\s* and the \\Z fallbacks tolerate the malformed spacing and
        # missing closing tags observed in the wild, so the call executes
        # instead of leaking backend syntax into the chat.
        fn_match = re.search(
            r"<function\\s*=\\s*[\\"\\']?([\\w.\\-]+)[\\"\\']?\\s*>(.*?)(?:</function>|\\Z)",
            text,
            re.DOTALL,
        )
        if fn_match:
            fn_name = fn_match.group(1).strip()
            fn_params: dict[str, Any] = {}
            for _pm in re.finditer(
                r"<parameter\\s*=\\s*[\\"\\']?([\\w.\\-]+)[\\"\\']?\\s*>(.*?)(?:</parameter>|\\Z)",
                fn_match.group(2),
                re.DOTALL,
            ):
                _val = _pm.group(2).strip()
                try:
                    fn_params[_pm.group(1)] = int(_val)
                except ValueError:
                    fn_params[_pm.group(1)] = _val
            return (fn_name, _json.dumps(fn_params))

'''

out = src.replace(ANCHOR, NEW + ANCHOR, 1)

if out == src:
    print("ABORT: replacement produced no change. No change made.")
    sys.exit(1)

# ---- backup ----
stamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
bak = PATH + ".bak-fmt4-" + stamp
with io.open(bak, "w", encoding="utf-8", newline="") as f:
    f.write(raw)
print("backup written   :", bak)

# ---- write ----
if use_crlf:
    out = out.replace("\n", "\r\n")
with io.open(PATH, "w", encoding="utf-8", newline="") as f:
    f.write(out)

print("post-patch bytes :", os.path.getsize(PATH))
print("post-patch sha256:", sha256(PATH))

# ---- compile check, auto-revert on failure ----
try:
    py_compile.compile(PATH, doraise=True)
    print("py_compile       : OK")
except Exception as exc:  # noqa: BLE001
    print("py_compile FAILED:", exc)
    with io.open(bak, "r", encoding="utf-8", newline="") as f:
        restore = f.read()
    with io.open(PATH, "w", encoding="utf-8", newline="") as f:
        f.write(restore)
    print("REVERTED to backup. No change left on disk.")
    sys.exit(1)

# ---- verify ----
with io.open(PATH, "r", encoding="utf-8", newline="") as f:
    check = f.read()
for label, needle in (
    ("Format 3 present", "# Format 3: bare JSON tool call"),
    ("Format 4 present", MARKER),
    ("function regex   ", "<function"),
):
    print(label, ":", needle in check)

print("")
print("PATCHED. Restart the backend with .\\start-openjarvis.ps1 (health 503 for ~95 s),")
print("then re-send the ziprecruiter request and read the tool-call ARGS panel.")
print("Revert with: Copy-Item '" + bak + "' '" + PATH + "' -Force")
