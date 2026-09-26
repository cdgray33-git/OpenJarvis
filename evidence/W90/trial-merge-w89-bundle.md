# TRIAL MERGE W89 BUNDLE - pulled W90 2026-09-25T17:59:21

## ===== FILE: C:\Users\Admin\OpenJarvis\evidence\W89\tools\trial_merge_w89.py =====
# trial_merge_w89.py - W89 upgrade sizing, MEASUREMENT ONLY. Uses `git merge-tree --write-tree --merge-base` (git >= 2.40), which
# merges entirely inside git's object database: NO working tree, NO branch, NO ref, NO checkout, NO index change. Production and
# main are untouched (verified at the end). Side effect: unreferenced objects in .git (removed by the next git gc).
# Merge = base af21bc18, ours HEAD, theirs = the upstream clone's origin/main (fetched into FETCH_HEAD - no ref created).
# Runs twice: plain, and with -X ignore-cr-at-eol (to separate real conflicts from line-ending noise).
# Writes evidence\W89\trial-merge-report.md. Env overrides for dry runs: OJ_REPO, OJ_UP, OJ_A0, OJ_A1.
import os, re, subprocess, collections, datetime
from pathlib import Path

REPO = os.environ.get("OJ_REPO", r"C:\Users\Admin\OpenJarvis")
UP = os.environ.get("OJ_UP", r"C:\Users\Admin\upstream-OpenJarvis")
A0 = os.environ.get("OJ_A0", "af21bc18")
A1 = os.environ.get("OJ_A1", "refs/remotes/origin/main")

def git(args, cwd=REPO, check=True):
    r = subprocess.run(["git", "--no-pager"] + args, cwd=cwd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    if check and r.returncode not in (0, 1):
        raise SystemExit("GIT FAIL %s: %s" % (args, r.stderr.strip()))
    return r

ver = git(["--version"]).stdout.strip()
m = re.search(r"(\d+)\.(\d+)", ver)
if not m or (int(m.group(1)), int(m.group(2))) < (2, 40):
    raise SystemExit("STOP: %s - need git 2.40+ for merge-tree --merge-base. Nothing done." % ver)
before = {"head": git(["rev-parse", "HEAD"]).stdout.strip(), "status": git(["status", "--porcelain", "--untracked-files=no"]).stdout}
git(["fetch", "--quiet", UP, A1])
theirs = git(["rev-parse", "FETCH_HEAD"]).stdout.strip()
base = git(["rev-parse", A0]).stdout.strip()

SERVICE = [
    ("1 Chat", ["src/openjarvis/server/", "src/openjarvis/prompt/", "src/openjarvis/system/", "src/openjarvis/cli/"]),
    ("2 Managed agents", ["src/openjarvis/agents/", "src/openjarvis/operators/", "src/openjarvis/scheduler/", "src/openjarvis/workflow/"]),
    ("4 Memory and RAG", ["src/openjarvis/tools/storage/", "src/openjarvis/memory/"]),
    ("3 Tools and Office", ["src/openjarvis/tools/", "src/openjarvis/sandbox/"]),
    ("5 Speech", ["src/openjarvis/speech/"]), ("6 Connectors", ["src/openjarvis/connectors/"]), ("7 Channels", ["src/openjarvis/channels/"]),
    ("8 Skills", ["src/openjarvis/skills/"]),
    ("9 Traces/telemetry/learning", ["src/openjarvis/traces/", "src/openjarvis/telemetry/", "src/openjarvis/learning/", "src/openjarvis/evals/", "src/openjarvis/bench/"]),
    ("10 Security", ["src/openjarvis/security/"]), ("11 Engine/models", ["src/openjarvis/engine/", "src/openjarvis/intelligence/"]),
    ("12 MCP", ["src/openjarvis/mcp/"]), ("13 Frontend", ["frontend/"]),
    ("Core/other src", ["src/openjarvis/"]), ("Tests", ["tests/"]), ("Rust extension", ["rust/"]),
    ("Dependencies", ["pyproject.toml", "uv.lock"]), ("Docs", ["docs/", "mkdocs.yml", "README.md", "CHANGELOG.md"]),
]
def svc(p):
    for name, pre in SERVICE:
        if any(p == x or p.startswith(x) for x in pre):
            return name
    return "Build/scripts/other"

def names(a, b, extra=()):
    r = git(["diff", "--name-only"] + list(extra) + [a, b])
    return set(x for x in r.stdout.splitlines() if x)
their_ch = names(base, theirs)
our_ch = names(base, "HEAD")
our_ch_real = names(base, "HEAD", ["--ignore-cr-at-eol", "--diff-filter=ACDMR"])
our_real = set()
for ln in git(["diff", "--numstat", "--ignore-cr-at-eol", base, "HEAD"]).stdout.splitlines():
    p = ln.split("\t")
    if len(p) >= 3 and (p[0], p[1]) != ("0", "0"):
        our_real.add(p[2])

def run(extra):
    r = git(["merge-tree", "--write-tree", "--merge-base=" + base] + extra + ["HEAD", theirs])
    lines = r.stdout.splitlines()
    tree = lines[0] if lines else ""
    conflicted, i = [], 1
    while i < len(lines) and lines[i].strip():
        parts = lines[i].split("\t")
        conflicted.append(parts[-1]); i += 1
    msgs = [x for x in lines[i + 1:] if x.strip()]
    conflicted = sorted(set(conflicted))
    kinds = collections.Counter(); kind_of = {}
    for mline in msgs:
        mm = re.match(r"CONFLICT \(([^)]+)\): .*?(?:in|of) (\S+)", mline)
        if mm:
            kinds[mm.group(1)] += 1; kind_of.setdefault(mm.group(2), mm.group(1))
    hunks = {}
    for p in conflicted:
        b = git(["cat-file", "-p", "%s:%s" % (tree, p)], check=False).stdout
        hunks[p] = sum(1 for x in b.splitlines() if x.startswith("<<<<<<<"))
    return {"rc": r.returncode, "tree": tree, "conflicted": conflicted, "kinds": kinds, "kind_of": kind_of, "hunks": hunks, "msgs": msgs}

plain = run([])
eol = run(["-X", "ignore-cr-at-eol"])

both = their_ch & our_ch
both_real = their_ch & our_real
L = []; w = L.append
w("# TRIAL MERGE REPORT - author %s -> upstream %s onto Graystone HEAD %s" % (base[:8], theirs[:8], before["head"][:8]))
w("")
w("Generated %s by trial_merge_w89.py. MEASUREMENT ONLY: git merge-tree (in the object database) - no working tree, branch, ref" % datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))
w("or checkout was changed. %s." % ver)
w("")
w("## 1. Summary")
w("| Measure | Plain merge | Ignoring CR at EOL |")
w("|---|---|---|")
w("| Files the author changed (base -> upstream) | %d | %d |" % (len(their_ch), len(their_ch)))
w("| Files Graystone changed (base -> HEAD) | %d (all) | %d (real content) |" % (len(our_ch), len(our_real)))
w("| Files changed by BOTH | %d | %d |" % (len(both), len(both_real)))
w("| Files the author changed that apply CLEANLY (we did not touch them) | %d | %d |" % (len(their_ch - our_ch), len(their_ch - our_real)))
w("| CONFLICTED files | %d | %d |" % (len(plain["conflicted"]), len(eol["conflicted"])))
w("| Conflict hunks (<<<<<<< markers) | %d | %d |" % (sum(plain["hunks"].values()), sum(eol["hunks"].values())))
w("| Conflict kinds | %s | %s |" % (", ".join("%s %d" % kv for kv in sorted(plain["kinds"].items())) or "-",
                                       ", ".join("%s %d" % kv for kv in sorted(eol["kinds"].items())) or "-"))
w("")
w("The right-hand column is the real size of the job (line-ending-only differences are not conflicts).")
w("")
w("## 2. By service (ignoring CR at EOL)")
w("| Service | author changed | Graystone changed | both | auto-merged | CONFLICTED files | hunks |")
w("|---|---|---|---|---|---|---|")
agg = collections.defaultdict(collections.Counter)
for p in their_ch: agg[svc(p)]["a"] += 1
for p in our_real: agg[svc(p)]["g"] += 1
for p in both_real: agg[svc(p)]["b"] += 1
for p in eol["conflicted"]:
    agg[svc(p)]["c"] += 1; agg[svc(p)]["h"] += eol["hunks"][p]
order = [n for n, _ in SERVICE] + ["Build/scripts/other"]
for s in order:
    c = agg.get(s)
    if c:
        w("| %s | %d | %d | %d | %d | %d | %d |" % (s, c["a"], c["g"], c["b"], c["b"] - c["c"], c["c"], c["h"]))
w("")
w("## 3. Conflicted files (ignoring CR at EOL) - service | file | kind | hunks")
w("| Service | File | Kind | Hunks |")
w("|---|---|---|---|")
for p in sorted(eol["conflicted"], key=lambda x: (order.index(svc(x)), x)):
    w("| %s | %s | %s | %d |" % (svc(p), p, eol["kind_of"].get(p, "content"), eol["hunks"][p]))
w("")
w("## 4. Files that conflict ONLY because of line endings (plain merge minus EOL-ignoring merge)")
for p in sorted(set(plain["conflicted"]) - set(eol["conflicted"])):
    w("- %s" % p)
w("")
w("## 5. Merge messages (ignoring CR at EOL), CONFLICT lines")
for x in eol["msgs"]:
    if x.startswith("CONFLICT"):
        w("- %s" % x)

after = {"head": git(["rev-parse", "HEAD"]).stdout.strip(), "status": git(["status", "--porcelain", "--untracked-files=no"]).stdout}
untouched = before == after
w("")
w("## 6. Safety check: HEAD and tracked working tree unchanged by this run: %s" % untouched)
out = Path(REPO) / "evidence" / "W89" / "trial-merge-report.md"
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text("\n".join(L) + "\n", encoding="utf-8", newline="\n")
print("REPORT:", out)
print("  author changed %d | Graystone real %d | both %d | CONFLICTED plain %d / eol-ignored %d | hunks %d | untouched %s" % (
    len(their_ch), len(our_real), len(both_real), len(plain["conflicted"]), len(eol["conflicted"]), sum(eol["hunks"].values()), untouched))


## ===== FILE: C:\Users\Admin\OpenJarvis\evidence\W89\trial-merge-report.md =====
# TRIAL MERGE REPORT - author af21bc18 -> upstream a6dcf846 onto Graystone HEAD 252c7362

Generated 2026-09-25 14:15 by trial_merge_w89.py. MEASUREMENT ONLY: git merge-tree (in the object database) - no working tree, branch, ref
or checkout was changed. git version 2.52.0.windows.1.

## 1. Summary
| Measure | Plain merge | Ignoring CR at EOL |
|---|---|---|
| Files the author changed (base -> upstream) | 811 | 811 |
| Files Graystone changed (base -> HEAD) | 753 (all) | 725 (real content) |
| Files changed by BOTH | 73 | 67 |
| Files the author changed that apply CLEANLY (we did not touch them) | 738 | 744 |
| CONFLICTED files | 43 | 43 |
| Conflict hunks (<<<<<<< markers) | 380 | 380 |
| Conflict kinds | content 42, modify/delete 1 | content 42, modify/delete 1 |

The right-hand column is the real size of the job (line-ending-only differences are not conflicts).

## 2. By service (ignoring CR at EOL)
| Service | author changed | Graystone changed | both | auto-merged | CONFLICTED files | hunks |
|---|---|---|---|---|---|---|
| 1 Chat | 58 | 19 | 16 | 8 | 8 | 25 |
| 2 Managed agents | 67 | 4 | 4 | 1 | 3 | 9 |
| 4 Memory and RAG | 9 | 2 | 1 | 1 | 0 | 0 |
| 3 Tools and Office | 24 | 7 | 5 | 1 | 4 | 7 |
| 5 Speech | 5 | 1 | 1 | 0 | 1 | 3 |
| 6 Connectors | 25 | 1 | 0 | 0 | 0 | 0 |
| 7 Channels | 7 | 0 | 0 | 0 | 0 | 0 |
| 8 Skills | 9 | 0 | 0 | 0 | 0 | 0 |
| 9 Traces/telemetry/learning | 55 | 1 | 1 | 0 | 1 | 1 |
| 10 Security | 12 | 0 | 0 | 0 | 0 | 0 |
| 11 Engine/models | 18 | 3 | 3 | 2 | 1 | 3 |
| 12 MCP | 4 | 0 | 0 | 0 | 0 | 0 |
| 13 Frontend | 58 | 91 | 27 | 7 | 20 | 225 |
| Core/other src | 19 | 3 | 2 | 1 | 1 | 4 |
| Tests | 283 | 14 | 1 | 1 | 0 | 0 |
| Rust extension | 39 | 1 | 0 | 0 | 0 | 0 |
| Dependencies | 2 | 2 | 2 | 0 | 2 | 100 |
| Docs | 59 | 39 | 0 | 0 | 0 | 0 |
| Build/scripts/other | 58 | 537 | 4 | 2 | 2 | 3 |

## 3. Conflicted files (ignoring CR at EOL) - service | file | kind | hunks
| Service | File | Kind | Hunks |
|---|---|---|---|
| 1 Chat | src/openjarvis/cli/ask.py | content | 1 |
| 1 Chat | src/openjarvis/cli/serve.py | content | 6 |
| 1 Chat | src/openjarvis/server/agent_manager_routes.py | content | 11 |
| 1 Chat | src/openjarvis/server/api_routes.py | content | 3 |
| 1 Chat | src/openjarvis/server/auth_middleware.py | content | 1 |
| 1 Chat | src/openjarvis/server/connectors_router.py | content | 1 |
| 1 Chat | src/openjarvis/server/routes.py | content | 1 |
| 1 Chat | src/openjarvis/server/stream_bridge.py | content | 1 |
| 2 Managed agents | src/openjarvis/agents/_stubs.py | content | 2 |
| 2 Managed agents | src/openjarvis/agents/morning_digest.py | content | 4 |
| 2 Managed agents | src/openjarvis/agents/native_openhands.py | content | 3 |
| 3 Tools and Office | src/openjarvis/tools/__init__.py | content | 1 |
| 3 Tools and Office | src/openjarvis/tools/_stubs.py | content | 1 |
| 3 Tools and Office | src/openjarvis/tools/code_interpreter.py | content | 3 |
| 3 Tools and Office | src/openjarvis/tools/knowledge_sql.py | content | 2 |
| 5 Speech | src/openjarvis/speech/faster_whisper.py | content | 3 |
| 9 Traces/telemetry/learning | src/openjarvis/telemetry/gpu_monitor.py | content | 1 |
| 11 Engine/models | src/openjarvis/engine/ollama.py | content | 3 |
| 13 Frontend | frontend/package-lock.json | content | 100 |
| 13 Frontend | frontend/package.json | content | 2 |
| 13 Frontend | frontend/src-tauri/Cargo.lock | content | 30 |
| 13 Frontend | frontend/src-tauri/Cargo.toml | content | 1 |
| 13 Frontend | frontend/src-tauri/src/lib.rs | content | 8 |
| 13 Frontend | frontend/src-tauri/tauri.conf.json | content | 1 |
| 13 Frontend | frontend/src/App.tsx | content | 1 |
| 13 Frontend | frontend/src/components/Chat/ChatArea.tsx | content | 3 |
| 13 Frontend | frontend/src/components/Chat/InputArea.tsx | content | 5 |
| 13 Frontend | frontend/src/components/Chat/MessageBubble.tsx | content | 1 |
| 13 Frontend | frontend/src/components/CommandPalette.tsx | content | 2 |
| 13 Frontend | frontend/src/components/SetupScreen.tsx | content | 4 |
| 13 Frontend | frontend/src/lib/api.ts | content | 46 |
| 13 Frontend | frontend/src/lib/sse.ts | content | 3 |
| 13 Frontend | frontend/src/lib/store.ts | content | 2 |
| 13 Frontend | frontend/src/pages/AgentsPage.tsx | content | 2 |
| 13 Frontend | frontend/src/pages/DataSourcesPage.tsx | content | 7 |
| 13 Frontend | frontend/src/pages/SettingsPage.tsx | content | 5 |
| 13 Frontend | frontend/tsconfig.tsbuildinfo | content | 0 |
| 13 Frontend | frontend/vite.config.ts | content | 2 |
| Core/other src | src/openjarvis/core/config.py | content | 4 |
| Dependencies | pyproject.toml | content | 6 |
| Dependencies | uv.lock | content | 94 |
| Build/scripts/other | .gitignore | content | 2 |
| Build/scripts/other | configs/openjarvis/config.toml | content | 1 |

## 4. Files that conflict ONLY because of line endings (plain merge minus EOL-ignoring merge)

## 5. Merge messages (ignoring CR at EOL), CONFLICT lines
- CONFLICT (content): Merge conflict in .gitignore
- CONFLICT (content): Merge conflict in configs/openjarvis/config.toml
- CONFLICT (content): Merge conflict in frontend/package-lock.json
- CONFLICT (content): Merge conflict in frontend/package.json
- CONFLICT (content): Merge conflict in frontend/src-tauri/Cargo.lock
- CONFLICT (content): Merge conflict in frontend/src-tauri/Cargo.toml
- CONFLICT (content): Merge conflict in frontend/src-tauri/src/lib.rs
- CONFLICT (content): Merge conflict in frontend/src-tauri/tauri.conf.json
- CONFLICT (content): Merge conflict in frontend/src/App.tsx
- CONFLICT (content): Merge conflict in frontend/src/components/Chat/ChatArea.tsx
- CONFLICT (content): Merge conflict in frontend/src/components/Chat/InputArea.tsx
- CONFLICT (content): Merge conflict in frontend/src/components/Chat/MessageBubble.tsx
- CONFLICT (content): Merge conflict in frontend/src/components/CommandPalette.tsx
- CONFLICT (content): Merge conflict in frontend/src/components/SetupScreen.tsx
- CONFLICT (content): Merge conflict in frontend/src/lib/api.ts
- CONFLICT (content): Merge conflict in frontend/src/lib/sse.ts
- CONFLICT (content): Merge conflict in frontend/src/lib/store.ts
- CONFLICT (content): Merge conflict in frontend/src/pages/AgentsPage.tsx
- CONFLICT (content): Merge conflict in frontend/src/pages/DataSourcesPage.tsx
- CONFLICT (content): Merge conflict in frontend/src/pages/SettingsPage.tsx
- CONFLICT (modify/delete): frontend/tsconfig.tsbuildinfo deleted in HEAD and modified in a6dcf84637571ce3e38c0bdb77c7e50937f6cba9.  Version a6dcf84637571ce3e38c0bdb77c7e50937f6cba9 of frontend/tsconfig.tsbuildinfo left in tree.
- CONFLICT (content): Merge conflict in frontend/vite.config.ts
- CONFLICT (content): Merge conflict in pyproject.toml
- CONFLICT (content): Merge conflict in src/openjarvis/agents/_stubs.py
- CONFLICT (content): Merge conflict in src/openjarvis/agents/morning_digest.py
- CONFLICT (content): Merge conflict in src/openjarvis/agents/native_openhands.py
- CONFLICT (content): Merge conflict in src/openjarvis/cli/ask.py
- CONFLICT (content): Merge conflict in src/openjarvis/cli/serve.py
- CONFLICT (content): Merge conflict in src/openjarvis/core/config.py
- CONFLICT (content): Merge conflict in src/openjarvis/engine/ollama.py
- CONFLICT (content): Merge conflict in src/openjarvis/server/agent_manager_routes.py
- CONFLICT (content): Merge conflict in src/openjarvis/server/api_routes.py
- CONFLICT (content): Merge conflict in src/openjarvis/server/auth_middleware.py
- CONFLICT (content): Merge conflict in src/openjarvis/server/connectors_router.py
- CONFLICT (content): Merge conflict in src/openjarvis/server/routes.py
- CONFLICT (content): Merge conflict in src/openjarvis/server/stream_bridge.py
- CONFLICT (content): Merge conflict in src/openjarvis/speech/faster_whisper.py
- CONFLICT (content): Merge conflict in src/openjarvis/telemetry/gpu_monitor.py
- CONFLICT (content): Merge conflict in src/openjarvis/tools/__init__.py
- CONFLICT (content): Merge conflict in src/openjarvis/tools/_stubs.py
- CONFLICT (content): Merge conflict in src/openjarvis/tools/code_interpreter.py
- CONFLICT (content): Merge conflict in src/openjarvis/tools/knowledge_sql.py
- CONFLICT (content): Merge conflict in uv.lock

## 6. Safety check: HEAD and tracked working tree unchanged by this run: True

