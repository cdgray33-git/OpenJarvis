import ast, os, shutil, sys, time

TARGET = os.path.join("src", "openjarvis", "agents", "native_openhands.py")
MARKER = "openjarvis-raw-gen-v1"

A1 = 'content = result.get("content", "")'
A2 = 'raw_tool_calls = result.get("tool_calls", [])'
A3 = '__all__ = ["NativeOpenHandsAgent"]'

HELPER = [
    "",
    "",
    "def _oj_raw_gen(run_id, turn_id, raw, stripped, n_tool_calls):",
    '    """' + MARKER + ' - log the pre-strip generation for one turn."""',
    "    try:",
    '        raw = raw or ""',
    '        stripped = stripped or ""',
    "        _oj_get_agent_logger().info(",
    '            "RAWGEN run=%s turn=%s rawlen=%d striplen=%d changed=%s ntc=%d raw=%s",',
    "            run_id, turn_id, len(raw), len(stripped),",
    "            (raw != stripped), n_tool_calls, repr(raw[:1500]),",
    "        )",
    "    except Exception:",
    "        pass",
]

apply = "--apply" in sys.argv

with open(TARGET, "r", encoding="utf-8", newline="") as f:
    src = f.read()

if MARKER in src:
    print("NO-OP: marker already present")
    sys.exit(0)

eol = "\r\n" if "\r\n" in src else "\n"
print("detected EOL:", repr(eol), "| size:", len(src.encode("utf-8")))
lines = src.split(eol)

def find_one(anchor):
    hits = [i for i, ln in enumerate(lines) if ln.strip() == anchor]
    if len(hits) != 1:
        print("ABORT: anchor matched", len(hits), "times:", anchor)
        sys.exit(1)
    print("anchor OK line", hits[0] + 1, "|", anchor)
    return hits[0]

i1 = find_one(A1)
i2 = find_one(A2)
i3 = find_one(A3)

ind1 = lines[i1][: len(lines[i1]) - len(lines[i1].lstrip())]
ind2 = lines[i2][: len(lines[i2]) - len(lines[i2].lstrip())]

new = list(lines)
new[i3:i3] = HELPER
new.insert(i2 + 1, ind2 + "_oj_raw_gen(_oj_run_id, _oj_turn_id, _oj_raw, content, len(raw_tool_calls))")
new.insert(i1 + 1, ind1 + "_oj_raw = content")

cand = eol.join(new)
ast.parse(cand)
pred = len(cand.encode("utf-8"))
print("py_compile OK | predicted size:", pred, "| delta:", pred - len(src.encode("utf-8")))

if not apply:
    print("DRY RUN - nothing written. Re-run with --apply")
    sys.exit(0)

bak = TARGET + ".bak_rawgen_" + time.strftime("%Y%m%d_%H%M%S")
shutil.copy2(TARGET, bak)
print("backup:", bak)
with open(TARGET, "w", encoding="utf-8", newline="") as f:
    f.write(cand)
actual = os.path.getsize(TARGET)
print("on-disk size:", actual)
if actual != pred:
    print("SIZE MISMATCH - RESTORE WITH: Copy-Item '" + bak + "' '" + TARGET + "' -Force")
    sys.exit(1)
with open(TARGET, "r", encoding="utf-8", newline="") as f:
    chk = f.read()
print("marker present:", MARKER in chk)
print("call site present:", "_oj_raw_gen(_oj_run_id" in chk)
print("APPLIED OK")
