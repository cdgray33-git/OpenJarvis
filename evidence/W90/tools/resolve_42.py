# resolve_42.py - W90 step 4.2: resolve pyproject.toml, core/config.py, .gitignore, configs/openjarvis/config.toml
# in the UPGRADE WORKTREE only. Per-hunk decisions are fixed below; every hunk is fingerprinted (ours and theirs) before
# it is touched - any mismatch aborts with NOTHING written. Bytes of the chosen side are copied as-is (non-ASCII safe);
# the file's own line ending and BOM are preserved. Does NOT stage (git add) and does NOT commit.
# Rollback per file: git -C <wt> checkout -m -- <file>   (recreates the conflict)
import os, sys, subprocess, py_compile, tomllib

WT = os.environ.get("OJ_WT", r"C:\Users\Admin\OpenJarvis-upgrade")
O, T = "ours", "theirs"

def git_bytes(args):
    r = subprocess.run(["git", "-C", WT, "--no-pager"] + args, capture_output=True)
    if r.returncode != 0:
        sys.exit("GIT FAIL %s: %s" % (args, r.stderr.decode("utf-8", "replace")))
    return r.stdout

def read(rel):
    b = open(os.path.join(WT, rel), "rb").read()
    bom = b.startswith(b"\xef\xbb\xbf")
    t = b[3:].decode("utf-8") if bom else b.decode("utf-8")
    eol = "\r\n" if "\r\n" in t else "\n"
    return t, bom, eol

def write(rel, text, bom):
    data = text.encode("utf-8")
    open(os.path.join(WT, rel), "wb").write((b"\xef\xbb\xbf" if bom else b"") + data)

def hunks(text):
    """Split into [str | (ours_lines, theirs_lines)] keeping line endings."""
    out, cur, state, ours, theirs = [], [], 0, [], []
    for ln in text.splitlines(keepends=True):
        s = ln.rstrip("\r\n")
        if state == 0 and s.startswith("<<<<<<< "):
            out.append("".join(cur)); cur = []; state = 1; ours, theirs = [], []
        elif state == 1 and s == "=======":
            state = 2
        elif state == 2 and s.startswith(">>>>>>> "):
            out.append((ours, theirs)); state = 0
        elif state == 1: ours.append(ln)
        elif state == 2: theirs.append(ln)
        else: cur.append(ln)
    if state != 0: sys.exit("UNBALANCED MARKERS")
    out.append("".join(cur))
    return out

def has(lines, s): return any(s in x for x in lines)

def resolve(rel, plan):
    text, bom, eol = read(rel)
    parts = hunks(text)
    hs = [p for p in parts if isinstance(p, tuple)]
    if len(hs) != len(plan):
        sys.exit("ABORT %s: %d hunks found, plan has %d - NOTHING WRITTEN" % (rel, len(hs), len(plan)))
    for i, ((o, t), (fo, ft, _)) in enumerate(zip(hs, plan), 1):
        if not (has(o, fo) if fo else "".join(o).strip() == "") or not has(t, ft):
            sys.exit("ABORT %s hunk %d: fingerprint mismatch - NOTHING WRITTEN" % (rel, i))
    res, k = [], 0
    for p in parts:
        if isinstance(p, tuple):
            res.append("".join(plan[k][2](p[0], p[1], eol))); k += 1
        else:
            res.append(p)
    return "".join(res), bom

def L(s, eol): return s + eol
def repl(lines, old, new): return [x.replace(old, new) for x in lines]

PYPROJECT = [
    ('version = "1.1.0"', 'dynamic = ["version"]', lambda o, t, e: t),
    ('nvidia-ml-py>=12.0', 'python-telegram-bot>=22.8', lambda o, t, e: t),
    ('python-pptx', 'websockets>=15.0.1',
     lambda o, t, e: t + [x for x in o if "croniter" not in x]),
    ('kokoro-onnx', 'soundfile>=0.12',
     lambda o, t, e: t[:-1] + [L('    # Graystone (W90 merge): kept from our speech extra', e),
                               L('    "kokoro-onnx>=0.5.0",', e), L('    "ctranslate2>=4.8.0",', e),
                               L('    "onnxruntime>=1.14",', e), L('    "av>=17.1.0",', e)] + t[-1:]),
    ('hybrid/*.py', 'hybrid/**/*.py', lambda o, t, e: t),
    (None, 'desktop-native', lambda o, t, e: t),
]
CONFIG_PY = [
    ('qwen3.5:9b', '_LEMONADE_DEFAULT_MODEL',
     lambda o, t, e: o + [x for x in t if "_LEMONADE_DEFAULT_MODEL" in x]),
    ('localhost:8010', 'localhost:13305', lambda o, t, e: t),
    ('compute_type: str = "auto"', 'tts_backend', lambda o, t, e: o + t[2:]),
    ('native_openhands', 'Loopback is safe',
     lambda o, t, e: repl(repl(t, 'port = 8000', 'port = 8010'), 'agent = "orchestrator"', 'agent = "native_openhands"')),
]
CONFIG_TOML = [
    ('port = 8010', 'host = "127.0.0.1"', lambda o, t, e: repl(t, 'port = 8000', 'port = 8010')),
]

def gitignore():
    rel = ".gitignore"
    text, bom, eol = read(rel)
    if "<<<<<<< " not in text: sys.exit("ABORT .gitignore: not conflicted - NOTHING WRITTEN")
    ours = git_bytes(["show", ":2:.gitignore"]).decode("utf-8").splitlines()
    theirs = git_bytes(["show", ":3:.gitignore"]).decode("utf-8").splitlines()
    tset = set(x.strip() for x in theirs)
    extra = [x for x in ours if x.strip() and x.strip() not in tset]
    body = list(theirs)
    while body and not body[-1].strip(): body.pop()
    body += ["", "# ---------------------------------------------------------------------------",
             "# Graystone additions (W90 merge onto author a6dcf846): our entries the author lacks",
             "# ---------------------------------------------------------------------------"] + extra
    return eol.join(body) + eol, bom, extra

results = {}
for rel, plan in [("pyproject.toml", PYPROJECT), ("src/openjarvis/core/config.py", CONFIG_PY),
                  ("configs/openjarvis/config.toml", CONFIG_TOML)]:
    results[rel] = resolve(rel, plan)
gi_text, gi_bom, gi_extra = gitignore()
results[".gitignore"] = (gi_text, gi_bom)
# all four validated in memory - now write
for rel, (txt, bom) in results.items():
    if any(x.startswith(("<<<<<<< ", ">>>>>>> ")) or x == "=======" for x in txt.splitlines()):
        sys.exit("ABORT %s: markers remain - NOTHING WRITTEN" % rel)
for rel, (txt, bom) in results.items():
    write(rel, txt, bom)
    print("WROTE", rel)

# verification
py_compile.compile(os.path.join(WT, "src/openjarvis/core/config.py"), doraise=True); print("VERIFY config.py compiles: OK")
pp = tomllib.loads(read("pyproject.toml")[0])
deps = pp["project"]["dependencies"]
names = lambda lst: [d.split(">")[0].split("<")[0].split("=")[0].split(";")[0].strip() for d in lst]
print("VERIFY pyproject parses: OK | dynamic =", pp["project"].get("dynamic"), "| requires-python =", pp["project"]["requires-python"])
for n in ["websockets", "pdfplumber", "python-docx", "python-pptx", "openpyxl", "croniter", "nvidia-ml-py", "kokoro"]:
    print("  core dep %-14s count=%d" % (n, names(deps).count(n)))
print("  speech extra =", pp["project"]["optional-dependencies"]["speech"])
print("  dependency-groups =", list(pp.get("dependency-groups", {}).keys()))
ct = tomllib.loads(read("configs/openjarvis/config.toml")[0])
print("VERIFY config.toml parses: OK | server =", {k: ct.get("server", {}).get(k) for k in ("host", "port", "agent")})
print("VERIFY .gitignore: author file + %d Graystone lines appended" % len(gi_extra))
for x in gi_extra: print("   +", x)
