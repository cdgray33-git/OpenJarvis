import os, sys, hashlib, time, py_compile, shutil
MARK = "openjarvis-w83-sysmerge-v1"
p = os.path.join(os.getcwd(), "src", "openjarvis", "engine", "ollama.py")
raw = open(p, "rb").read(); t = raw.decode("utf-8")
print("BEFORE sha256", hashlib.sha256(raw).hexdigest().upper(), len(raw), "bytes")
if MARK in t:
    print("ALREADY PATCHED - no change"); sys.exit(0)
nl = "\r\n" if "\r\n" in t else "\n"
a1 = "        msg_dicts = messages_to_dicts(messages)"
a2 = '            "messages": messages_to_dicts(messages),'
n1, n2 = t.count(a1 + nl), t.count(a2 + nl)
print("ANCHORS a1=%d (want 2) a2=%d (want 1) newline=%r" % (n1, n2, nl))
if n1 != 2 or n2 != 1:
    print("ABORT - anchors do not match, nothing written"); sys.exit(1)
t = t.replace(a1 + nl, "        msg_dicts = _oj_merge_system(messages_to_dicts(messages))  # " + MARK + nl)
t = t.replace(a2 + nl, '            "messages": _oj_merge_system(messages_to_dicts(messages)),  # ' + MARK + nl)
helper = [
"", "",
"# --- " + MARK + " ---",
"# The qwen3-coder Ollama chat template renders only the FIRST system message;",
"# later system messages are silently dropped (measured W83 H4: +1 token vs +180 merged).",
"# The author's context injection prepends its own system message, so it never reached",
"# the model on agent paths. Merge all system messages into one, at the first's position.",
"def _oj_merge_system(msg_dicts):",
"    try:",
"        idx = [i for i, m in enumerate(msg_dicts) if isinstance(m, dict) and m.get(\"role\") == \"system\"]",
"        if len(idx) < 2:",
"            return msg_dicts",
"        parts = []",
"        for i in idx:",
"            c = msg_dicts[i].get(\"content\")",
"            if c is None:",
"                c = \"\"",
"            if not isinstance(c, str):",
"                logger.info(\"SYSMERGE skipped non-text system content count=%d\", len(idx))",
"                return msg_dicts",
"            if c.strip():",
"                parts.append(c)",
"        merged = dict(msg_dicts[idx[0]])",
"        merged[\"content\"] = \"\\n\\n\".join(parts)",
"        drop = set(idx[1:])",
"        out = [merged if i == idx[0] else m for i, m in enumerate(msg_dicts) if i not in drop]",
"        logger.info(\"SYSMERGE merged=%d chars=%d\", len(idx), len(merged[\"content\"]))",
"        return out",
"    except Exception:",
"        logger.warning(\"SYSMERGE error - messages unchanged\", exc_info=True)",
"        return msg_dicts",
""]
t = t.rstrip("\r\n") + nl + nl.join(helper)
bdir = os.path.join(os.getcwd(), "evidence", "W83", "backup"); os.makedirs(bdir, exist_ok=True)
bak = os.path.join(bdir, "ollama.py.bak-W83-sysmerge-" + time.strftime("%Y%m%d_%H%M%S"))
shutil.copy2(p, bak); print("BACKUP", bak)
compile(t, p, "exec")
open(p, "wb").write(t.encode("utf-8"))
py_compile.compile(p, doraise=True)
new = open(p, "rb").read()
print("AFTER  sha256", hashlib.sha256(new).hexdigest().upper(), len(new), "bytes  marker_count=%d" % new.decode("utf-8").count(MARK))
from openjarvis.engine.ollama import _oj_merge_system as M
S = lambda c: {"role": "system", "content": c}; U = {"role": "user", "content": "q"}
r1 = M([S("A"), S("B"), U]); print("T1", len(r1) == 2 and r1[0]["content"] == "A\n\nB" and r1[1] is U)
r2 = [S("A"), U]; print("T2", M(r2) is r2)
r3 = [U]; print("T3", M(r3) is r3)
r4 = [S("A"), {"role": "system", "content": [{"type": "text"}]}, U]; print("T4", M(r4) is r4)
