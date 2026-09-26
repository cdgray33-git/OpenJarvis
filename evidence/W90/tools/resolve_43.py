# resolve_43.py - W90 step 4.3 CHAT: 8 files / 25 hunks in the UPGRADE WORKTREE only, plus 2 targeted Graystone
# re-applications outside hunks (routes.py cloud bypass, serve.py memory backfill + _build_agent_tools on the author's
# tool resolver). Every hunk and every targeted edit is fingerprinted; any mismatch aborts with NOTHING written.
# Verified in-script (no markers, every file compiles); STAGES (git add) ONLY IF ALL CHECKS PASS. Never commits.
# Rollback per file: git -C <wt> checkout -m -- <file>
import os, sys, subprocess, py_compile

WT = os.environ.get("OJ_WT", r"C:\Users\Admin\OpenJarvis-upgrade")
NO_STAGE = os.environ.get("OJ_NO_STAGE") == "1"
S = "src/openjarvis/"

def read(rel):
    b = open(os.path.join(WT, rel), "rb").read()
    bom = b.startswith(b"\xef\xbb\xbf")
    t = b[3:].decode("utf-8") if bom else b.decode("utf-8")
    return t, bom, ("\r\n" if "\r\n" in t else "\n")

def hunks(text):
    out, cur, state, o, t = [], [], 0, [], []
    for ln in text.splitlines(keepends=True):
        s = ln.rstrip("\r\n")
        if state == 0 and s.startswith("<<<<<<< "):
            out.append("".join(cur)); cur = []; state = 1; o, t = [], []
        elif state == 1 and s == "=======": state = 2
        elif state == 2 and s.startswith(">>>>>>> "): out.append((o, t)); state = 0
        elif state == 1: o.append(ln)
        elif state == 2: t.append(ln)
        else: cur.append(ln)
    if state: sys.exit("UNBALANCED MARKERS")
    out.append("".join(cur)); return out

def has(lines, s): return (s == "" and not "".join(lines).strip()) or (s != "" and any(s in x for x in lines))
def idx(lines, s):
    for i, x in enumerate(lines):
        if s in x: return i
    sys.exit("ABORT: anchor not found: %r - NOTHING WRITTEN" % s)

def resolve(rel, plan):
    text, bom, eol = read(rel)
    parts = hunks(text); hs = [p for p in parts if isinstance(p, tuple)]
    if len(hs) != len(plan): sys.exit("ABORT %s: %d hunks, plan %d - NOTHING WRITTEN" % (rel, len(hs), len(plan)))
    for i, ((o, t), (fo, ft, _)) in enumerate(zip(hs, plan), 1):
        if not has(o, fo) or not has(t, ft): sys.exit("ABORT %s hunk %d: fingerprint mismatch - NOTHING WRITTEN" % (rel, i))
    res, k = [], 0
    for p in parts:
        if isinstance(p, tuple): res.append("".join(plan[k][2](p[0], p[1], eol))); k += 1
        else: res.append(p)
    return "".join(res), bom, eol

def once(text, old, new, rel):
    n = text.count(old)
    if n != 1: sys.exit("ABORT %s: targeted edit anchor found %d times (need 1) - NOTHING WRITTEN" % (rel, n))
    return text.replace(old, new)

T = lambda o, t, e: t
def L(s, e): return s + e

# ---------- per-file hunk plans ----------
ASK = [("TerminalConfirmGate()", "agent_security_kwargs",
        lambda o, t, e: o[:idx(o, "TerminalConfirmGate()") + 1] + t[idx(t, "lambda prompt: True") + 1:])]
AUTH = [("def record_bind", "def websocket_authorized", lambda o, t, e: o + [e] + t)]
CONN = [("from fastapi import Request", "issue #512", T)]
ROUTES = [("CLOUD_BYPASS_AGENT", "_remember_exchange", T)]
BRIDGE = [("used_real_streaming = False", "if content:", T)]
API = [("iterate in a thread", "_iterate_sync_stream", T),
       ("single-shot generate", "asyncio.to_thread", T),
       ("openjarvis-ws-bus-v1", "create_ws_router(", T)]
AMR = [("import ConfirmPolicy", "_start_managed_worker", lambda o, t, e: o + [e] + t)] + \
      [(fo, ft, T) for fo, ft in [
          ("self.memory_backend = memory_backend", "_get_or_create_memory_backend"),
          ("memory_backend: Any = None", "runtime: Any = None"),
          ("_LightweightSystem(engine, model, config, memory_backend)", "_LightweightSystem(engine, model, config, runtime)"),
          ("Special handling", "_SAMPLER_PARAM_KEYS"),
          ("def _spec_dict_for", "def _sampler_kwargs"),
          ("ChannelRegistry.contains(entry)", "def _instantiate_managed_tool"),
          ("openjarvis-toolkit-bind-v1", "resolved_by_name"),
          ("site=\"managed-agent-tool\"", ""),
          ("_srv_mem,", "app_state,"),
          ("_srv_mem,", "_app_state,")]]

def serve_h1(o, t, e):
    head = t[:idx(t, "import openjarvis.tools")]
    while head and not head[-1].strip(): head.pop()
    return head + [e,
        L('                    allowed, tools_configured = _resolve_allowed_tools(config)', e),
        L('                    tools = _build_agent_tools(config, "chat")  # openjarvis-tools-dedupe-v1 (file_write confined, D-06)', e),
        e] + t[idx(t, "# MCP server tools"):]
def serve_h2(o, t, e):
    conf = o[:idx(o, "openjarvis-w83-persona-v1")]
    while conf and not conf[-1].strip(): conf.pop()
    return t + conf + [e]
def serve_h3(o, t, e):
    return [L('                        _allowed, _tools_configured = _resolve_allowed_tools(config)', e),
            L('                        _channel_tools = _build_agent_tools(config, "channel")  # openjarvis-tools-dedupe-v1', e),
            e] + t[idx(t, "# Reuse the process-owned MCP pool"):]
SERVE = [("openjarvis-tools-dedupe-v1", "tools_configured", serve_h1),
         ("_server_confirm_callback", "agent_security_kwargs", serve_h2),
         ("openjarvis-tools-dedupe-v1", "_ch_mcp_tools", serve_h3),
         ("wired memory_backend into", "", lambda o, t, e: t),
         ("BIND_ASSERT", "cors_origins", lambda o, t, e: o[:-1] + t),
         ("uvicorn.Config", "run_server(", lambda o, t, e: o)]   # H6 provisional OURS - decided after daemon.py read

# ---------- targeted Graystone edits outside hunks ----------
def edit_routes(text, e, rel):
    old = '        and (not request_body.stream or bool(getattr(agent, "_tools", None)))' + e + '    )'
    new = ('        and (not request_body.stream or bool(getattr(agent, "_tools", None)))' + e +
           '        # Graystone CLOUD_BYPASS_AGENT (8ad19526, re-applied W90 onto the author dispatch):' + e +
           '        # cloud model ids go to the direct paths, which route them via cloud_router.' + e +
           '        and not _uses_direct_cloud_router(engine, model)' + e + '    )')
    text = once(text, old, new, rel)
    # both sides added `import asyncio`; keep the author's single import (CLEANUP REGISTER W90)
    return once(text, 'from __future__ import annotations' + e + 'import asyncio' + e + e + 'import asyncio' + e,
                'from __future__ import annotations' + e + e + 'import asyncio' + e, rel)

def edit_serve(text, e, rel):
    old = ('    _DEFAULT_TOOLS = {"think", "calculator", "web_search"}' + e + '    configured = config.agent.tools' + e +
           '    if configured:' + e + '        if isinstance(configured, list):' + e +
           '            allowed = {t.strip() for t in configured if isinstance(t, str) and t.strip()}' + e +
           '        else:' + e + '            allowed = {t.strip() for t in configured.split(",") if t.strip()}' + e +
           '    else:' + e + '        allowed = _DEFAULT_TOOLS' + e)
    new = '    allowed, _ = _resolve_allowed_tools(config)  # W90: author resolver (tools.enabled -> agent.tools -> default)' + e
    text = once(text, old, new, rel)
    anchor = '            console.print("  Memory:    [cyan]active[/cyan]")' + e
    block = [
        '            # Graystone (93829e27, re-applied W90): the chat agent tools were built before',
        '            # memory_backend existed; inject the live backend into retrieval/memory_* tools.',
        '            try:',
        '                _wired = 0',
        '                for _t in (getattr(agent, "_tools", None) or []):',
        '                    _tname = getattr(getattr(_t, "spec", None), "name", "")',
        '                    if (_tname == "retrieval" or _tname.startswith("memory_")) and hasattr(_t, "_backend"):',
        '                        _t._backend = memory_backend',
        '                        _wired += 1',
        '                logger.info("MEMORY-BACKFILL wired memory_backend into %d agent tool(s)", _wired)',
        '            except Exception as _exc:',
        '                logger.debug("Agent tool backend injection failed: %s", _exc)']
    return once(text, anchor, anchor + e.join(block) + e, rel)

PLANS = [("cli/ask.py", ASK, None), ("cli/serve.py", SERVE, edit_serve),
         ("server/agent_manager_routes.py", AMR, None), ("server/api_routes.py", API, None),
         ("server/auth_middleware.py", AUTH, None), ("server/connectors_router.py", CONN, None),
         ("server/routes.py", ROUTES, edit_routes), ("server/stream_bridge.py", BRIDGE, None)]

out = {}
for short, plan, edit in PLANS:
    rel = S + short
    txt, bom, eol = resolve(rel, plan)
    if edit: txt = edit(txt, eol, rel)
    if any(x.startswith(("<<<<<<< ", ">>>>>>> ")) or x == "=======" for x in txt.splitlines()):
        sys.exit("ABORT %s: markers remain - NOTHING WRITTEN" % rel)
    try:
        compile(txt, rel, "exec")
    except SyntaxError as ex:
        sys.exit("ABORT %s: does not compile (%s) - NOTHING WRITTEN" % (rel, ex))
    out[rel] = (txt, bom)
for rel, (txt, bom) in out.items():
    open(os.path.join(WT, rel), "wb").write((b"\xef\xbb\xbf" if bom else b"") + txt.encode("utf-8"))
    py_compile.compile(os.path.join(WT, rel), doraise=True)
    print("WROTE + COMPILES", rel)
chk = open(os.path.join(WT, S + "cli/serve.py"), encoding="utf-8").read()
for s in ["_server_confirm_callback", "agent_security_kwargs", "MEMORY-BACKFILL", "allowed, _ = _resolve_allowed_tools",
          "BIND_ASSERT", "uvicorn.Config", "file_write confined"]:
    print("  serve.py has %-38s %s" % (s, s in chk))
print("  ask.py TerminalConfirmGate kept:", "TerminalConfirmGate()" in out[S + "cli/ask.py"][0],
      "| remaining bare lambdas (expect 1, author skills site - W56 re-apply after merge):", out[S + "cli/ask.py"][0].count("lambda prompt: True"))
print("  routes.py cloud guard:", "_uses_direct_cloud_router(engine, model)" in out[S + "server/routes.py"][0])
if NO_STAGE:
    print("OJ_NO_STAGE=1 - not staged"); sys.exit(0)
r = subprocess.run(["git", "-C", WT, "add", "--"] + list(out), capture_output=True, text=True)
if r.returncode: sys.exit("STAGE FAILED: " + r.stderr)
print("STAGED %d files" % len(out))
