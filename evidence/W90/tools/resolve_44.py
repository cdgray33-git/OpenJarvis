# resolve_44.py - W90 step 4.4 BACKEND: 10 files / 23 hunks (agents, tools, speech, telemetry, engine) in the UPGRADE
# WORKTREE only, plus 2 targeted edits to the already-staged cli/serve.py: (a) W83 native_openhands persona block restored
# (the author's generic serve builder would REPLACE the OpenHands tool prompt - see decision note), (b) uvicorn start via the
# author's DaemonServer (#924) keeping loop="asyncio" + log_config=None. Every hunk/edit fingerprinted; any mismatch aborts
# with NOTHING written. Stages ONLY IF ALL CHECKS PASS. Never commits. Rollback: git -C <wt> checkout -m -- <file>
#   (serve.py was already resolved+staged by resolve_43: rollback = re-run resolve_43 after checkout -m)
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
OT = lambda o, t, e: o + t          # ours then theirs
def L(s, e): return s + e

AG_STUBS = [("openjarvis-w83-persona-v1", "prompt_builder: Optional[Any] = None,", T),   # author now forwards (D-35 closed)
            ("", "capability_policy=capability_policy,", T)]
NOH = [("prompt_builder=None", "capability_policy: Optional[Any] = None", OT),        # keep persona opt-in + author security
       ("prompt_builder=prompt_builder", "capability_policy=capability_policy", OT),
       ("_oj_raw = content", 'result.get("content") or ""',
        lambda o, t, e: t + [x for x in o if "_oj_raw = content" in x])]              # author None-safety + RAWGEN capture
DIGEST = [("GREETING + PRIORITIES", "CONFIGURED SECTIONS", T),
          ("Synthesize my morning briefing", "<collected_data>", T),
          ("Load TTS config from config.toml", "output_dir = str(", OT),              # Graystone [tts] override kept
          ('"voice_id": voice_id,', '"output_dir": output_dir,',
           lambda o, t, e: o + [x for x in t if '"output_dir": output_dir' in x])]
TOOLS_INIT = [("mailbox_tools", "scan_chunks",
               lambda o, t, e: o + [L("except ImportError:", e), L("    pass", e), e, L("try:", e)] + t)]
TOOLS_STUBS = [("import logging.handlers", "import queue", OT)]
CODE = [("_oj_strip_fence(code)", "_validate_ast(code)",
         lambda o, t, e: o[:2] + t),                                                   # fence strip + snapshot BEFORE author AST check
        ("_oj_workdir()", "OPENJARVIS_CODE_CWD",
         lambda o, t, e: [x.replace('os.environ.get("OPENJARVIS_CODE_CWD") or None',
                                    'os.environ.get("OPENJARVIS_CODE_CWD") or _oj_workdir()') for x in t]),
        ("def _oj_workdir", '__all__ = ["CodeInterpreterTool", "UnsafeCodeError"]',
         lambda o, t, e: [x for x in o if not x.startswith("__all__")] + t)]
KSQL = [("_ALLOWED_TABLE", "_FORBIDDEN_RE = re.compile", OT),
        ("set_authorizer(_authorizer)", "forbidden = _FORBIDDEN_RE.search",
         lambda o, t, e: t[:idx(t, "try:")] + o)]                                      # author keyword check, then Graystone authorizer
WHISPER = [("", "import logging", T),
           ("WINDOWS FIX", "with tmp:", T),                                            # author fixed the same Windows lock (1ff11f0e)
           ("os.unlink(tmp_path)", "self._last_error", T)]
GPU = [("pynvml", "issue #389", T)]
NUMCTX = lambda o, t, e: [x.replace("kwargs=kwargs,",
          'kwargs=kwargs if kwargs.get("num_ctx") is not None else {**kwargs, "num_ctx": _oj_default_num_ctx()},'
          '  # Graystone num_ctx from config (c37d8b16)') for x in t]
OLLAMA = [("_oj_default_num_ctx()", "_ollama_request_options(", NUMCTX)] * 3

W83 = [
 '                # openjarvis-w83-persona-v1 (P3/W3, owner): author SystemPromptBuilder through the author prompt_builder hook',
 '                # W90: kept AFTER the author generic wiring above. The author builder uses agent_template=default_system_prompt,',
 '                # and BaseAgent._build_messages lets prompt_builder.build() REPLACE the agent system prompt - for native_openhands',
 '                # that would drop the tool-calling template. This block overrides it with the OpenHands template + tools.',
 '                if agent_key == "native_openhands" and getattr(agent_cls, "accepts_tools", False):',
 '                    try:',
 '                        from openjarvis.prompt.builder import SystemPromptBuilder',
 '                        from openjarvis.agents.native_openhands import OPENHANDS_SYSTEM_PROMPT',
 '                        from openjarvis.agents.prompt_loader import load_system_prompt_override',
 '                        from openjarvis.tools._stubs import build_tool_descriptions',
 '                        _oj_tmpl = (load_system_prompt_override("native_openhands") or OPENHANDS_SYSTEM_PROMPT).format(',
 '                            tool_descriptions=build_tool_descriptions(agent_kwargs.get("tools") or []))',
 '                        agent_kwargs["prompt_builder"] = SystemPromptBuilder(agent_template=_oj_tmpl, memory_files_config=config.memory_files, system_prompt_config=config.system_prompt)',
 '                        logger.info("PERSONA prompt_builder wired agent=%s template_chars=%d", agent_key, len(_oj_tmpl))',
 '                    except Exception:',
 '                        logger.warning("PERSONA prompt_builder not wired - agent runs without persona", exc_info=True)']

def edit_serve(text, e, rel):
    a = ('                        agent_kwargs["confirm_callback"] = (' + e + '                            _server_confirm_callback' + e +
         '                        )' + e)
    text = once(text, a, a + e + e.join(W83) + e, rel)
    old = ('    from openjarvis.server.daemon import run_server' + e + e +
           '    config = uvicorn.Config(app, host=bind_host, port=bind_port, log_level="info", loop="asyncio", log_config=None)' + e +
           '    server = uvicorn.Server(config)' + e + '    asyncio.run(server.serve())' + e)
    new = e.join([
        '    # Graystone (W90): the author DaemonServer (records daemon state, #924) with our uvicorn settings -',
        '    # loop="asyncio" under the Windows selector policy set at the top of serve(), log_config=None so the',
        '    # backend.log topology (b4cbd819) is not replaced. asyncio.run(serve()) as before: server.run() would let',
        '    # newer uvicorn choose its own Windows loop factory.',
        '    import asyncio',
        '',
        '    from openjarvis.cli.daemon_cmd import clear_server_state',
        '    from openjarvis.server.daemon import DaemonServer',
        '',
        '    server = DaemonServer(',
        '        uvicorn.Config(app, host=bind_host, port=bind_port, log_level="info", loop="asyncio", log_config=None)',
        '    )',
        '    try:',
        '        asyncio.run(server.serve())',
        '    finally:',
        '        clear_server_state(os.getpid())']) + e
    return once(text, old, new, rel)

PLANS = [("agents/_stubs.py", AG_STUBS), ("agents/native_openhands.py", NOH), ("agents/morning_digest.py", DIGEST),
         ("tools/__init__.py", TOOLS_INIT), ("tools/_stubs.py", TOOLS_STUBS), ("tools/code_interpreter.py", CODE),
         ("tools/knowledge_sql.py", KSQL), ("speech/faster_whisper.py", WHISPER), ("telemetry/gpu_monitor.py", GPU),
         ("engine/ollama.py", OLLAMA)]

out = {}
for short, plan in PLANS:
    rel = S + short
    out[rel] = resolve(rel, plan)
rel = S + "cli/serve.py"
t, b, e = read(rel)
if "<<<<<<< " in t: sys.exit("ABORT serve.py still conflicted - run resolve_43 first")
out[rel] = (edit_serve(t, e, rel), b, e)
for rel, (txt, bom, eol) in out.items():
    if any(x.startswith(("<<<<<<< ", ">>>>>>> ")) or x == "=======" for x in txt.splitlines()):
        sys.exit("ABORT %s: markers remain - NOTHING WRITTEN" % rel)
    try: compile(txt, rel, "exec")
    except SyntaxError as ex: sys.exit("ABORT %s: does not compile (%s) - NOTHING WRITTEN" % (rel, ex))
for rel, (txt, bom, eol) in out.items():
    open(os.path.join(WT, rel), "wb").write((b"\xef\xbb\xbf" if bom else b"") + txt.encode("utf-8"))
    py_compile.compile(os.path.join(WT, rel), doraise=True)
    print("WROTE + COMPILES", rel)
g = lambda r: out[S + r][0]
print("  serve: W83 persona block %s | DaemonServer %s | run_server import gone %s" % (
    "openjarvis-w83-persona-v1" in g("cli/serve.py"), "DaemonServer(" in g("cli/serve.py"),
    "import run_server" not in g("cli/serve.py")))
print("  code_interpreter: fence-before-AST %s | cwd workdir fallback %s | AST check %s" % (
    g("tools/code_interpreter.py").find("_oj_strip_fence(code)") < g("tools/code_interpreter.py").find("_validate_ast(code)"),
    'or _oj_workdir()' in g("tools/code_interpreter.py"), "_validate_ast(code)" in g("tools/code_interpreter.py")))
print("  knowledge_sql: keyword check %s | authorizer %s" % ("_FORBIDDEN_RE.search" in g("tools/knowledge_sql.py"),
      "set_authorizer(_authorizer)" in g("tools/knowledge_sql.py")))
print("  ollama: num_ctx override x%d | sysmerge kept x%d" % (g("engine/ollama.py").count('"num_ctx": _oj_default_num_ctx()'),
      g("engine/ollama.py").count("_oj_merge_system(messages_to_dicts")))
print("  native_openhands: prompt_builder param %s | RAWGEN %s" % ("prompt_builder=None" in g("agents/native_openhands.py"),
      "_oj_raw = content" in g("agents/native_openhands.py")))
if NO_STAGE: print("OJ_NO_STAGE=1 - not staged"); sys.exit(0)
r = subprocess.run(["git", "-C", WT, "add", "--"] + list(out), capture_output=True, text=True)
if r.returncode: sys.exit("STAGE FAILED: " + r.stderr)
print("STAGED %d files" % len(out))
