# SDP SOURCE EXTRACT W82 part 10 (deduplicated by section hash)
### [ARCHIVE-W78-2026-09-22.md] INDEX
s1 Window subject and narrative
s2 Evidence
s3 Negative results
s4 Hazards
s5 SDD/SDP feed
s6 Progress against the 28
s7 Deltas to carried registers
CARRIED VERBATIM FROM ARCHIVE-W77 lines 43-EOF (W77 section numbers inside; extract W78 s1-s7 with ^## s<N> Window|Evidence|... names):
  ## W77 DELTAS
  ## CARRIED VERBATIM FROM ARCHIVE-W72 s7-s12 (W73 deltas appended as one-liners)
  ## s7 EXECUTION PATHS DELTA
  ## s8 DIAGNOSTIC TOOLING DELTA
  ## s9 LOGGING TOPOLOGY DELTA
  ## s10 RULES OF ENGAGEMENT DELTA
  ## s11 PROGRAM GOAL MOVEMENT
  ## s12 550B CARRY
  ## W73 DELTAS TO s7-s12
  ## s13 ROADMAP (CARRIED VERBATIM FROM ARCHIVE-W72 s17; W73 deltas below)
  ## A. MEASURED BASELINE - W72 [M]
  ## B. TRACK 0 - BASELINE TRUTH (finish before building anything)
  ## C. TRACK 1 - REQUIREMENTS AND THE PROGRESS MEASURE
  ## D. TRACK 2 - SDP RESTRUCTURE (ATO-led; follows Track 1)
  ## E. TRACK 3 - AGENT LAYER (measure first, then decide)
  ## F. TRACK 4 - EXECUTIVE-ASSISTANT CAPABILITIES (author mechanism -> status)
  ## G. STANDING HAZARDS AND AUTHOR DEFECTS (read, not traced)
  ## W73 ROADMAP DELTAS
  ## s14 UNUSED / ORPHANED CODE REGISTER (ATO)
  ## W74 DELTAS
  ## W75 DELTAS
  ## CLEANUP REGISTER (duplicates and redundant access points - remove at completion if unused)
### [ARCHIVE-W78-2026-09-22.md] s2 Evidence
EV1 Banner 16:37 (pre-W78): allowed = 13 names; tools_loaded = CalculatorTool ThinkTool
    RetrievalTool FileReadTool WebSearchTool CodeInterpreterTool ShellExecTool FileWriteTool
    MailboxListAccountsTool MailboxUsageReportTool MailboxFindMessagesTool MailboxMoveToTrashTool
    MailboxEmptyFolderTool. registry_keys = 43.
EV2 RTM fix: diff vs .bak-W78-v06 = exactly 1 line (L71); 135 lines both; CRLF preserved.
EV3 Confine, SDK builder (scripts\diag\w78_confine_check.py, server interpreter): RESOLVED DIRS
    C:\Users\Admin\.openjarvis\workspace EXISTS True; INSIDE write success and on disk; OUTSIDE
    (%TEMP%) refused "outside allowed directories", not on disk. OVERALL PASS.
EV4 Confine, live chat builder: backend.log 17:41:09 [DEBUG] file_write allowed_dirs=
    ['C:\\Users\\Admin\\.openjarvis\\workspace'], after restart at 17:40:15.
EV5 Dedupe (scripts\diag\w78_dedupe_check.py): STRUCT loop_once, no_channel_loop, chat_call_once,
    channel_call_once, channel_assert all True; chat and channel toolkits identical, 13 tools,
    match [agent] tools; both file_write instances confined; channel instance inside write PASS,
    outside refused. OVERALL PASS.
EV6 Dedupe, live: restart 17:52:23; 17:53:17 file_write allowed_dirs=... builder=chat;
    tools_loaded=[13] builder=chat; CHANNEL_ASSERT enabled=False default_channel=- default_agent=simple;
    wired memory_backend into 1 agent tool(s); BIND-ASSERT loopback=True api_key_set=True.
EV7 Server process model: PID 17996 (Python312\python.exe) PARENT 11440 (.venv\Scripts\python.exe),
    same start time, both "-m openjarvis.cli serve --port 8010". Repeated at 17:52 (7060 -> 10576).
EV8 Line counts: serve.py 702 -> 676 (-76 removed spans, +2 call lines, +6 assert, +42 helper).
### [ARCHIVE-W78-2026-09-22.md] s3 Negative results
N1 The BRIEF's "TOOLING register at EOF" is not a heading; it is the last bullet (- W77 TOOLING:)
   inside the CLEANUP region. A ^# scan finds no TOOLING header by design.
N2 RQ-025 is NOT explained by the missing llm config entry. sdk_verify.py passed tools=['llm'] and
   ask.py _build_tools wires it (engine, model). The model chose to answer directly. Candidate 2
   closed.
N3 channel_send is NOT an email tool (spec: Telegram, Discord, Slack) and is unwired on the server.
N4 RQ-005 is NOT class A: find_messages has no unread filter, no since/recent filter, no body
   fetch, and its limit keeps the OLDEST hits (UIDs ascending).
N5 My exchange-6 hazard claim "mailbox destructive tools ungated" was WRONG: requires_confirmation
   plus argument-aware gate (W58) plus CONFIRM DELETE interlock are in force.
N6 config.py [sandbox] workspace is NOT a file-tool key (container sandbox). No author key feeds
   allowed_dirs anywhere; the constructor parameter existed but no builder ever passed it.
N7 "Server runs global Python312" (W77) was half right, and my first correction (".venv") was also
   half right: the .venv launcher spawns base Python312. Environment = .venv.
N8 The first banner check after the confine patch was not a failure: the server had not been
   restarted (start 16:36:31). Measured, not assumed.
N9 OVERSTATEMENT, corrected here: commit 854b9c7 says "channel path proven". What is proven is the
   channel TOOL BUILDER. A live channel (message in, agent, tools, reply out) is NOT proven and
   cannot be until a channel is configured.
N10 Harness failure in E7 was the harness, not the patch: import openjarvis.cli.serve as s returns
   the click Command because cli\__init__ shadows the submodule.
N11 The author's "MCP" is not a server Graystone must build; it is the [tools.mcp] client.
### [ARCHIVE-W78-2026-09-22.md] s4 Hazards
H-W78-FILEREAD: file_read unconfined (reads anywhere except "sensitive" files). Deliberately left:
   confining breaks "read my document". For the owner's security pass.
H-W78-SCRATCHPAD: security of C:\Users\Admin\.openjarvis\workspace itself not reviewed (owner:
   after everything works).
H-W78-RUSTSHELL: shell_exec Rust bridge path ignores the sanitised env and the timeout and always
   reports returncode 0. Only when the Rust module provides ShellExecTool.
H-W78-CLISHADOW: openjarvis.cli.serve attribute is the click Command. Use sys.modules.
H-W78-PSCASE: PowerShell variable names are case-insensitive ($b and $B are one variable).
H-W78-ANALYTICS: config.py AnalyticsConfig defaults enabled=True, host 34.231.106.201.sslip.io,
   hardcoded PostHog key. Graystone config sets enabled=false (D-10, W76). OWNER RULING W78:
   nothing leaves the lab unless Gray requests it; this code goes on the dead-code removal
   register (s14) for outright removal.
H-W78-CRLF: git warns CRLF->LF on committed files; repo stores LF, working copy CRLF. Normal.
D-06 STANDS for shell_exec (gated) and the mailbox destructive tools (gated); file_write exposure
   CLOSED by confinement.
### [ARCHIVE-W78-2026-09-22.md] s5 SDD/SDP feed
Vol 3A section D additions:
 D-14 file_write confinement | author: allowed_dirs parameter never passed (writes anywhere) |
      Graystone: [tools] file_allowed_dirs, default ~/.openjarvis/workspace, helper
      config.resolve_file_write_dirs (never returns empty) | CHOICE (security) | 829cea7.
 D-15 Tool builders | author: two inline loops in serve.py + ask._build_tools | Graystone: one
      serve._build_agent_tools for chat and channel; ask._build_tools unchanged | CHOICE | 854b9c7.
 D-03 note: remote engine host is the owner's on-prem to off-prem conversion; the author's form is
      [engine.ollama] host. Source of the current host still unmeasured (W79 item 2).
Plain language (scratch pad): Jarvis has a sandbox drawer. It may put papers only in that drawer.
   If it tries to put a paper anywhere else in the house, the drawer's fence says no and nothing is
   written. Before W78 there was no fence at all. It still may READ papers around the house.
Execution path register delta: three tool builders.
   P-chat  serve.py serve() -> _build_agent_tools(config,"chat") -> agent_cls(... tools=...),
           then memory backfill injects backend into retrieval/memory_*. Gate live (confirm cb).
   P-chan  serve.py -> _build_agent_tools(config,"channel") -> JarvisSystem.wire_channel. Only when
           [channel] enabled and default_channel set. Today: disabled (CHANNEL_ASSERT).
   P-sdk   sdk.Jarvis._run_agent / cli ask._run_agent -> ask._build_tools(names, config, engine,
           model, channel) - injects llm engine+model, memory backend, channel; file_write confined.
   Consequence: an SDK PASS does not transfer to the server for llm or channel_* tools.
Logging topology delta: openjarvis.cli.serve now also emits CHANNEL_ASSERT (WARNING) and every
   [DEBUG] banner line carries a builder=<chat|channel> suffix (prefixes unchanged). All to
   backend.log via the logging module.
Infrastructure for the SDP (09/20 rule): verification harnesses run with the server's own
   interpreter (.venv launcher), from the repo root, write probes only inside the scratch pad and
   %TEMP%, and score PASS on disk state, never on tool reply text.
### [ARCHIVE-W78-2026-09-22.md] s7 Deltas to carried registers
TOOLING +: scripts\diag\w78_confine_check.py, scripts\diag\w78_dedupe_check.py (committed);
   CHANNEL_ASSERT line; builder= suffix; bundle-concat pattern (W78-*-bundle.md, untracked,
   regenerable); server-interpreter locator (Win32_Process CommandLine match 'serve').
CLEANUP +: imap_mail.mcp_tools() divergent display-only duplicate of the mailbox tool specs
   (check connectors router consumer, then remove). serve.py duplicate tool loop REMOVED W78
   (backup serve.py.bak_w78dedupe_20260922_174849). Remaining builder split serve vs ask is by
   design (ask injects dependencies) - candidate to unify so the server wires llm.
DEAD CODE (s14) +: AnalyticsConfig / PostHog path - remove outright (owner ruling W78).
RULES +: no case-only PowerShell variable names; extract W78 sections by name; "proven" must name
   the exact piece proven; locate the server interpreter by measurement.
EXECUTION PATHS +: see s5. LOGGING +: see s5.
550B: not used in W78; pattern unchanged.
### [ARCHIVE-W79-2026-09-23.md] INDEX
s1 Window subject and narrative
s2 Evidence
s3 Negative results
s4 Hazards
s5 SDD/SDP feed
s6 Progress against the 28
s7 Deltas to carried registers
CARRIED VERBATIM FROM ARCHIVE-W78 lines 34-362 (W78 s1-s7 plus W77 and earlier carries; extract W79 s1-s7 by name).
### [ARCHIVE-W79-2026-09-23.md] s1 Window subject and narrative
SUBJECT (owner-set): FINISH THE AUTHOR'S INITIAL BUILD, THEN ITS EXTENSION POINTS. Opened on Opus 5.5.
Grew, by PATCH WHAT WE FIND, into one committed fix (engine turn-down, D-16) after doctor exposed a
live engine self-loop.
E1 Scaffold by LINE RANGE: W78 lines 34-362 carried verbatim (329 lines, diff 0). Item 0 was already
   done at W78 close: RTM section 7 = 12a1f8f on HEAD, origin and gitlab.
E2 Item 1, author's doctor (.venv interpreter): 17 pass / 13 warn / 0 fail. Flagged: lemonade, vllm,
   uzu "Reachable" with the ollama model list; .env dotenv parse failures (known, not re-derived);
   "Rust extension: building (run in background)" (unmeasured, see H-W79-RUSTBUILD).
E3 Item 2 (D-03) measured: the ollama host comes from the OLLAMA_HOST env var (Process, User, Machine
   = http://172.16.33.200:11434). config.toml [engine] has no [engine.ollama] host.
   OPENJARVIS_OLLAMA_HOST (Process, User) has no reader anywhere in src.
E4 Port 8000: listener is svchost iphlpsvc = netsh portproxy 0.0.0.0:8000 -> 172.21.134.21:8000, dead
   target (GET timed out). Owner history: Jarvis was moved 8000 -> 8010 because of this conflict; the
   decision was correct on the information held.
E5 Engine bundle read whole (ollama.py, _discovery.py, _openai_compat.py, openai_compat_engines.py,
   config.py, litellm.py). ROOT CAUSE: config.py defaults for vllm, uzu and lemonade = localhost:8010
   = the OpenJarvis server itself. _make_engine passes the config host over the engine-file default.
   get_engine falls back to any healthy engine (alphabetical after the default) -> lemonade -> Jarvis
   calls itself.
E6 git: e0e3652 (07/04, "wire tools to native_openhands") introduced 8010 on 4 lines of config.py
   (329, 380, 404, init template 1894). The same commit changed jarvis init model tiers and committed
   three .fix_backups_* dirs and bundle_for_cloud_model.txt (13,989 lines). Pre-sweep author values:
   8000. Author server port default: also 8000 -> the author's own code collides with itself whenever
   his server runs. Owner hypothesis (consistent with code): hidden on the author's machine because
   doctor runs with the server stopped.
E7 Enumerator bundle read whole (ask, bench_cmd, chat_cmd, doctor_cmd, model, quickstart_cmd, serve,
   engine __init__, sdk, system builder). Every engine construction goes through
   _discovery._make_engine, and every caller catches exceptions and skips. The TOML loader silently
   ignores unknown keys, so a real EngineConfig field is required.
E8 Patch A openjarvis-engine-disable-v1 (D-16). First run failed: Path.read_text(newline=) is Python
   3.13+, server runs 3.12.10; died before backup, nothing written. Rerun: 3 anchors count=1, both
   files compiled, harness w79_disable_check OVERALL PASS.
E9 I proposed a commit after the unit harness. OWNER STOPPED IT: commit only after verification AND
   validation; the word "should" in my result text marked outcomes I had not measured. The rules were
   already pinned (ALWAYS VERIFY, FINISH THE THING, VALIDATE). Plan V1-V3 run before any commit.
E10 A2: config.toml [engine] disabled = "vllm,uzu,lemonade,litellm" (UTF-8 no BOM). V1 doctor PASS.
    V2 fallback harness PASS with a control. V3 live: first attempt measured the OLD server (PIDs
    7060/10576, W78 17:52 pair - no restart had occurred); after the owner's restart at 10:47:29, PASS.
E11 Commit a0704c4 (5 files, staged-set asserted), pushed to origin and gitlab, hashes equal.
### [ARCHIVE-W79-2026-09-23.md] s2 Evidence
EV1 evidence\W79\doctor-090348.txt: 17/13/0. Reachable: lemonade, litellm, ollama, uzu, vllm.
    Models lemonade = ollama = vllm (same 29). Default qwen3-coder:30b on ollama. Security profile
    'personal'. Node v24.15.0. Python 3.12.10.
EV2 Env: OLLAMA_HOST Process/User/Machine = http://172.16.33.200:11434. OPENJARVIS_OLLAMA_HOST
    Process/User = 172.16.33.200:11434. Repo .env host keys: GITLAB_URL, WIKI_JS_URL only.
    ~\.openjarvis\.env absent.
EV3 ollama.py __init__: explicit host (config) > OLLAMA_HOST > http://localhost:11434.
    OllamaEngineConfig.host default "". _openai_compat: host arg > <ENGINE>_HOST env > class default.
EV4 Portproxy: 0.0.0.0:8000 -> 172.21.134.21:8000; PID 3488 svchost -k NetSvcs -s iphlpsvc, started
    09/20 11:48:27. GET localhost:8000/v1/models timed out.
EV5 git log -S localhost:8010 -- config.py -> e0e3652 only. e0e3652^: vllm/uzu/lemonade 8000;
    server port config.py:946 and template :1936 = 8000.
EV6 Patch: NEWLINE LF (both files); ANCHOR cfg a1 / dsc a2 / dsc a3 count=1; backups
    *.bak_w79disable_20260923_095915; COMPILE OK both.
EV7 w79_disable_check: SRC repo src; FIELD default ''; empty list constructs vllm and ollama;
    vllm/uzu/lemonade raise EngineDisabled; ollama constructs with list set; DISCOVER healthy =
    ['ollama','litellm'] (list without litellm); TOML array -> 'vllm,uzu,lemonade'; OVERALL PASS.
EV8 evidence\W79\doctor-A2-101926.txt: 11/16/0. lemonade, litellm, uzu, vllm = "Unreachable (engine
    'x' disabled ...)"; ollama Reachable; Default model qwen3-coder:30b (on ollama). Delta reconciled:
    -6 pass (4 engines + Models lemonade, vllm); +4 warn (engines); -1 warn (Models litellm).
EV9 w79_fallback_check: LOADED disabled 4 keys, ollama.host ''; NORMAL -> ollama
    http://172.16.33.200:11434; OUTAGE (ollama host 127.0.0.1:9) with list -> None; CONTROL, list
    emptied -> lemonade http://localhost:8010 (hazard reproduced); OVERALL PASS, exit 0.
EV10 V3 live: PIDs 21684 (.venv launcher) -> 18480 (Python312), 09/23 10:47:29. 3 ESTABLISHED
    192.168.1.137 -> 172.16.33.200:11434. Server-originated connections to :8010 = 0. backend.log:
    10:48:05 tools_loaded=[13] builder=chat; 10:48:06 CHANNEL_ASSERT enabled=False; 10:48:31
    BIND-ASSERT loopback=True api_key_set=True; 10:48:31 BIND_ASSERT engine=ollama
    model=qwen3-coder:30b agent=native_openhands; 10:48:32 startup complete (63 s from launch);
    10:49:38 POST http://172.16.33.200:11434/api/chat 200. /api/tags health about every 30 s.
EV11 Commit a0704c4: config.py, _discovery.py, patch_w79_engine_disable.py, w79_disable_check.py,
    w79_fallback_check.py. HEAD = origin = gitlab = a0704c4.
### [ARCHIVE-W79-2026-09-23.md] s3 Negative results
N1 af21bc18 (BRIEF author-base hash) is NOT a local object. Pre-change truth taken from e0e3652^.
N2 Port 8000 was NOT serving ollama models - my exchange-6 claim was wrong. The identical model lists
   were the 8010 self-loop. 8000 is a dead portproxy.
N3 OPENJARVIS_OLLAMA_HOST is read by nothing in src (py, rs, ts, tsx).
N4 Restoring the author defaults would NOT fix the loop: the author server and the three engines
   share 8000. Repointing the engines at 8010 was also not an option (that IS the loop).
N5 "litellm sends chats out of the lab" was NOT established. health() only checks the import; no
   api_base is passed; with un-prefixed model names litellm most likely errors locally. Disabled
   anyway: is_cloud=True engine sitting in the fallback path under the no-egress ruling.
N6 The author has NO engine off-switch. Discovery and doctor probe every registered key.
N7 The first patch failure was the Python version (read_text newline is 3.13+), not the anchors.
N8 The first V3 read was the old server, not a failure of the patch: same PIDs as W78 EV7.
N9 The 10:46:52 CancelledError traceback is the OLD server's shutdown, not the new one. My log-window
   harness admitted it: a text compare of the first 19 chars ranks non-date lines ("Traceback...")
   above any date. Fix: select lines matching ^\d{4}-\d{2}-\d{2} before comparing.
N10 No EngineDisabled line appears live. Expected: get_engine resolves ollama first, and
   discover_engines logs construction failures at DEBUG, below the INFO gate.
N11 The working copies of config.py and _discovery.py are LF, not CRLF. Newline style is per file;
   measure, do not assume (H-W78-CRLF is about committed files).
### [ARCHIVE-W79-2026-09-23.md] s4 Hazards
H-W79-SELFLOOP CLOSED (a0704c4 + config): any engine whose host is the OpenJarvis port calls Jarvis
   itself; author-inherent at 8000. Outage behavior proven by harness (V2), NOT on the live server.
H-W79-PORTPROXY: portproxy 0.0.0.0:8000 -> 172.21.134.21:8000 on all interfaces (LAN reachable),
   dead target. Lab item - own window, together with the "Jarvis back to 8000" decision.
H-W79-E0E3652: git history holds bundle_for_cloud_model.txt (13,989 lines, may contain secrets) and
   three .fix_backups_* dirs. Security pass; any history rewrite is an owner decision.
H-W79-MODELTIERS: e0e3652 changed jarvis init tiers (64 GB -> qwen2.5-coder:32b, fallback
   qwen3.5:9b). Divergence, affects jarvis init recommendations only.
H-W79-RUSTBUILD: doctor reports "Rust extension: building (run in background)". If a build lands,
   shell_exec may switch to the Rust bridge (H-W78-RUSTSHELL: ignores timeout, returncode always 0).
   Unmeasured.
H-W79-DOTENV: repo .env lines 8, 10-20, 23, 25-27, 41-44 unparseable; loaded twice per invocation.
   Known (openjarvis-config-secrets); not re-derived; owner to schedule. Never print its values.
H-W79-PY312: server interpreter is Python 3.12.10 - harness code must be 3.12-compatible.
H-W79-LOGWINDOW: see N9.
### [ARCHIVE-W79-2026-09-23.md] s5 SDD/SDP feed
Vol 3A section D additions:
 D-16 Engine turn-down | author: no off-switch; discovery, doctor and get_engine probe every
      registered engine; get_engine falls back to any healthy one | Graystone: [engine] disabled
      (comma list, TOML array accepted); _discovery._make_engine raises EngineDisabled - one choke
      point for every enumerator | CHOICE (security, availability) | a0704c4. Live value:
      "vllm,uzu,lemonade,litellm" in ~\.openjarvis\config.toml (out of git).
 D-17 Server port 8010 | author 8000 | Graystone 8010 because a Windows portproxy (iphlpsvc) holds
      0.0.0.0:8000 | CONSTRAINT | e0e3652 (which also moved the vllm/uzu/lemonade defaults - the
      self-loop source).
 D-03 update: measured source = OLLAMA_HOST env (3 scopes). Author form [engine.ollama] host is
      honored first by ollama.py. Not yet set in config (W80 item 1).
Plain language (engine switch): Jarvis keeps a phone book of "brains" it can call for answers. Three
   numbers in that book were Jarvis's own number. If the real brain stopped answering, Jarvis would
   dial the next number - itself - and that call would dial itself again, around and around. We added
   a "do not call" list that crosses those numbers out. Now, if the real brain is down, Jarvis says
   so plainly instead of calling itself.
Infrastructure (09/20 rule), gate by gate:
   G1 ~\.openjarvis\config.toml [engine] disabled = "..." (TOML, UTF-8 without BOM - tomllib rejects
      a BOM).
   G2 load_config -> _apply_toml_section: unknown keys ignored; arrays normalized to a comma string
      for str fields -> EngineConfig.disabled.
   G3 Every engine build calls _discovery._make_engine(key, config); key in set -> EngineDisabled.
   G4 Callers catch and skip: doctor prints "Unreachable (engine 'x' disabled ...)"; discover_engines
      drops it (DEBUG log); get_engine skips, then returns None when nothing healthy remains.
   G5 serve.py startup: get_engine None -> engine hard exit (serve.py:151-157) instead of looping.
   Engine transport: server child process -> 172.16.33.200:11434, TCP, HTTP/1.1 plaintext JSON
      (GET /api/tags health about every 30 s, POST /api/chat), source 192.168.1.137.
Execution path delta: engine resolution for P-chat and P-chan (serve.py:193 get_engine, :260
   discover_engines/discover_models) and P-sdk (sdk.py:209, ask.py:802/854, chat_cmd, model,
   bench_cmd, system builder:310) all pass through _make_engine and inherit D-16.
Logging delta: none added. EngineDisabled during discovery logs at DEBUG (invisible at INFO).
### [ARCHIVE-W79-2026-09-23.md] s6 Progress against the 28
VERIFIED 3/28 unchanged. W79 moved the base beneath every row: the author's install baseline
(doctor) is measured and recorded, and the engine layer can no longer fail into itself - a
reliability precondition for all 28 rows. BRIEF W79 items 2 (host in config), 3 (connectors, moves
RQ-013 and RQ-016) and 4 ([tools.mcp]) not started.
### [ARCHIVE-W79-2026-09-23.md] s7 Deltas to carried registers
TOOLING +: scripts\diag\patch_w79_engine_disable.py, w79_disable_check.py, w79_fallback_check.py
   (committed a0704c4); evidence\W79\doctor-*.txt (doctor capture: .venv interpreter,
   PYTHONIOENCODING=utf-8, Out-File); W79-engine-bundle.md and W79-enum-bundle.md (untracked,
   regenerable); V3 live-check block (process start, TCP peers, self-loop count, log window) - apply
   the N9 date-regex fix before reuse.
CLEANUP +: OPENJARVIS_OLLAMA_HOST env var (Process, User) - no reader; remove after owner check.
   .fix_backups_* dirs committed in e0e3652.
DEAD CODE +: none.
RULES +: "should" in a result = unmeasured -> measure before committing; commit only after end-to-end
   V&V including the live server, never after a unit harness alone; harness code targets Python
   3.12; measure newline style per file; log windows anchor on a date regex.
EXECUTION PATHS +: see s5. LOGGING +: none.
ROLLBACK +: git revert a0704c4; src\openjarvis\core\config.py.bak_w79disable_20260923_095915;
   src\openjarvis\engine\_discovery.py.bak_w79disable_20260923_095915;
   C:\Users\Admin\.openjarvis\config.toml.bak-W79-A2-<time> (printed at A2).
550B: not used in W79.
### [ARCHIVE-W80-2026-09-23.md] Below CARRIED marker: W79-s7 deltas, then ARCHIVE-W79 carried registers verbatim.
Subject: continue the author's build - D-03 ollama host into config.toml first.
### [ARCHIVE-W80-2026-09-23.md] s1 Window subject and narrative
Subject: continue the author's build. Item 1 = D-03, ollama host moved into the author's config form.
X1 Scaffold built by extraction from ARCHIVE-W79 (W79-s7 deltas retitled, W79 carried region
   verbatim, carry diff 0). Defect in Claude's scaffold: INDEX lines began "## s1 ..." and matched the
   by-name extraction pattern. Fixed by prefixing "## INDEX: " (2 lines changed, verified). Also
   established: carried sections reuse s-numbers, so by-name extraction must be BOUNDED ABOVE the
   CARRIED marker (line 29 in this file).
X2 config.toml measured before write: 770 bytes, no BOM, CRLF 36 / bare LF 0, [engine] lines 1-5,
   no [engine.ollama] table, tomllib parse OK. Backup taken.
X3 Write: [engine.ollama] host = "http://172.16.33.200:11434" inserted before [intelligence].
   UTF-8 no BOM, CRLF preserved (39/0), 826 bytes, diff = exactly 3 inserted lines. tomllib and the
   project's load_config both return the host.
X4 Claude then asked for a whole-file bundle to prove config-over-env precedence. Gray stopped it:
   the record should already hold it. Archive search confirmed W79 s2 EV2/EV3, s3 N3, s5 D-03 update,
   s7 CLEANUP all carry it. Claude's miss (record not checked), not an SDP gap. Bundle built but
   NOT uploaded (evidence\W80\W80-ollama-bundle.md, untracked, 747 lines).
X5 Record shows precedence was established by CODE READ (W79 EV3 + _make_engine line 29). Runtime
   only ever measured env as the source (config had no host). Env and config have never disagreed.
X6 Gray required a risk assessment before the keep/remove decision on OLLAMA_HOST (new standing
   rule: NO BLIND OWNER DECISIONS). Author intent assessed from code; reader census measured.
   Census found cloud_router._ollama_host() reads ENV ONLY and raises if unset -> removal would
   break a live path. Recommendation: keep OLLAMA_HOST. Owner chose option 2: keep BOTH env vars
   (OLLAMA_HOST and OPENJARVIS_OLLAMA_HOST), restart backend only.
X7 Live V&V: baseline (PID 18480, START 10:47:29, self-loop 0), owner restart, post (PID 21784,
   START 12:04:19, self-loop 0), traceback at 12:03:52 read in full = old-process SIGINT shutdown,
   chat routes read from live openapi.json, scripted round trip PASS.
Proven: config holds the host; load_config returns it; restarted server reaches .200 for /api/tags
   AND /api/chat; no self-loop; chat completes end to end.
NOT proven: config wins over env AT RUNTIME (values identical; code read only). Discriminating test
   arrives with the F1 patch.
### [ARCHIVE-W80-2026-09-23.md] s2 Evidence
EV1 Scaffold: anchors s7=162 marker=180 in ARCHIVE-W79; W80 377 lines, carry diff 0; index fix
    2 lines changed, 7 section hits above marker line 29.
EV2 config.toml pre-write: 770 B, BOM False, CRLF 36, LF 0. Tables: [engine] 1, [intelligence] 6,
    [memory] 9, [agent] 14, [security] 20, [analytics] 24, [server] 27 (host = "0.0.0.0"), [speech] 32.
    tomllib: engine keys num_ctx, default, disabled; engine.ollama None.
EV3 Post-write: 826 B, BOM False, CRLF 39, LF 0. Lines 6-8 = [engine.ollama] / host / blank.
    tomllib engine.ollama = {'host': 'http://172.16.33.200:11434'}.
    load_config().engine.ollama.host = 'http://172.16.33.200:11434' (.venv python, src on path).
EV4 OLLAMA_HOST reader census (live files, .bak excluded):
    engine\ollama.py:40-42 config > env > default | _discovery.py:20 -> config.py:430 ollama_host
    property | cli\model.py:228-229 config then env | server\cloud_router.py:311-316 ENV ONLY,
    raises "OLLAMA_HOST environment variable not set", called at :344 and :364 |
    cli\init_cmd.py:200 env then localhost | connectors\embeddings.py:24,45 DEFAULT_OLLAMA_HOST =
    localhost:11434, caller-supplied | ask.py:813, hints.py:29 help text | scripts\quickstart.sh
    Linux, sets env. Root *.ps1 (start-openjarvis.ps1): ZERO hits - start script does not set it.
EV5 Env scopes: OLLAMA_HOST Process/User/Machine = http://172.16.33.200:11434.
    OPENJARVIS_OLLAMA_HOST Process/User = 172.16.33.200:11434 (no scheme), Machine empty.
EV6 Windows box: no ollama CLI, no service, no process, nothing listening on 11434.
EV7 evidence\W80\pre-restart.txt 12:02:13: listener 127.0.0.1:8010 PID 18480 START 10:47:29
    Python312; 3 ESTABLISHED to .200:11434 idle; self-loop 0; backend.log 61062 lines.
EV8 evidence\W80\post-restart.txt 12:06:13: PID 21784 START 12:04:19 RESTARTED True; 3 peers .200;
    self-loop 0; /api/tags to .200 every 30 s; BIND_ASSERT host=127.0.0.1 port=8010 engine=ollama
    model=qwen3-coder:30b agent=native_openhands; CHANNEL_ASSERT enabled=False.
EV9 Traceback 12:03:52 (backend.log line 61082): follows "Finished server process [18480]";
    uvicorn capture_signals -> _on_sigint -> KeyboardInterrupt, then lifespan CancelledError.
EV10 Live openapi.json chat routes: /v1/chat/completions [post]; /v1/agents/{agent_id}/message
    [post]; /v1/managed-agents/{agent_id}/tasks [get,post], /tasks/{task_id} [get,patch,delete],
    /messages [get,post].
EV11 evidence\W80\roundtrip.txt: PID 21784, 12:09:50.941 -> 12:09:57.241, RESULT OK PONG; max
    peers .200:11434 in flight 3; self-loop samples 0; only non-loopback remote 172.16.33.200:11434;
    log: 12:09:56,674 httpx POST http://172.16.33.200:11434/api/chat 200, 12:09:56,685
    uvicorn.access POST /v1/chat/completions 200. No auth challenge on loopback.
### [ARCHIVE-W80-2026-09-23.md] s3 Negative results
N1 The config-over-env precedence was NOT missing from the SDP record. W79 s2/s3/s5/s7 carry it.
   Established by archive search across 37 archives (hits only in W79). The miss was not checking.
N2 The 12:03:52 ERROR is NOT a fault of the D-03 change. It is the OLD process (18480) exiting on
   SIGINT: KeyboardInterrupt then lifespan CancelledError, 27 s before the new START. EV9.
N3 The four 127.0.0.1 peers in EV7 are NOT a self-loop. They are inbound clients on 8010 (frontend
   polling); self-loop filter (remote port 8010) = 0.
N4 Three idle peers to .200 are NOT evidence of chat. Keep-alive pool; /api/tags poll every 30 s.
N5 W79 V3 did NOT include a chat round trip (EV10 of W79 = PIDs, peers, log window). The W80 BRIEF
   line "live server serves chat" rested on peers. Closed by EV11.
N6 There is NO local Ollama on the Windows box (EV6). Removing OLLAMA_HOST would not strand one.
N7 start-openjarvis.ps1 does NOT set OLLAMA_HOST (EV4). The server inherits User/Machine scope.
N8 OPENJARVIS_OLLAMA_HOST still has NO reader (re-confirmed by EV4 census). Kept by owner decision.
### [ARCHIVE-W80-2026-09-23.md] s4 Hazards
H-W80-1 TWO HOST SOURCES (accepted risk until F1). Engine path = config then env. cloud_router and
        init_cmd = env only. If the ollama host moves and only config changes, paths silently split.
        Do NOT remove OLLAMA_HOST before F1 lands: cloud_router raises without it.
H-W80-2 By-name section extraction must be bounded above the CARRIED marker; carried sections reuse
        s-numbers. INDEX lines must not begin "## s<N> ".
H-W80-3 PYTHON PIN: server interpreter is 3.12.10 at C:\Users\Admin\AppData\Local\Programs\Python\
        Python312\python.exe. Must NOT be upgraded until the Tesla P100 is installed (owner, 09/23).
        Risk sources: python.org installer, winget, uv python updates, launcher swap .venv vs Python312.
H-W80-4 Listener binds 127.0.0.1 while config.toml [server] host = "0.0.0.0". Some launch input
        overrides config. Unmapped.
H-W80-5 (F2) connectors\embeddings.py defaults to localhost:11434 - dead on this box (EV6). Callers
        unmeasured; if any rely on the default, embeddings fail today regardless of D-03.
H-W80-6 Many .bak copies live inside src\ (ask.py x3, config.py x4, ollama.py x3, cloud_router.py x2,
        _discovery.py x1 seen in EV4 alone). Noise in every grep; cleanup register item.
H-W80-7 config.toml remains OUT OF GIT. D-03 host is now a third out-of-git config item.
### [ARCHIVE-W80-2026-09-23.md] s5 SDD/SDP feed
D-03 CLOSED (author form): [engine.ollama] host = "http://172.16.33.200:11434" in config.toml.
     OLLAMA_HOST (3 scopes) and OPENJARVIS_OLLAMA_HOST (Process, User) KEPT - owner decision 09/23,
     option 2, after risk assessment.
AUTHOR INTENT (inferred from code, no author doc found): three tiers in ollama.py __init__ - explicit
     config host, then OLLAMA_HOST (Ollama's own standard variable), then localhost:11434. Stock
     install assumes Ollama on the same machine; config is the deliberate override for a remote host.
     Graystone's two-server topology is the case the author put in config. Before W80 Graystone ran on
     tier 2 by accident of environment.
HOST RESOLUTION - TWO CONFIGURATION SOURCES, ONE ENDPOINT (for the AO):
  Endpoint: 172.16.33.200:11434, TCP, HTTP/1.1, JSON (UTF-8), no TLS inside the lab segment.
  Path A - local model engine (chat, /api/tags health poll): config.toml [engine.ollama] host, then
     OLLAMA_HOST, then localhost. Entry /v1/chat/completions -> engine -> POST /api/chat. Proven live
     EV11. Precedence proven by code read only.
  Path B - cloud_router (openrouter/ models): OLLAMA_HOST env ONLY, raises if unset (:311-316), used
     at :344 and :364. WHAT :344/:364 do with the ollama host is UNMEASURED (cloud call vs fallback
     to local). Must be read whole before the SDP states it. Behind Path B sits the external boundary:
     prompt content leaves the lab to OpenRouter. SDP owes: data that can cross (includes family email
     content), authentication and where the key lives, logging, human presence. Recorded constraints:
     cloud models run without tools (is_cloud_model tradeoff); uv sync exact-state deletes cloud SDK
     packages on launch; asyncio and 429 retry fixes recorded as not working.
  Path C - install-time CLI (jarvis init, init_cmd.py:200): env then localhost.
  Path D - embeddings connector: caller arg then localhost default (F2, unmeasured).
  Configuration items outside git for the baseline: config.toml (engine.disabled, engine.ollama.host,
     W77 web_search), OLLAMA_HOST x3 scopes, OPENJARVIS_OLLAMA_HOST x2 scopes, Python 3.12.10 pin.
  Evidence levels: config value - measured (EV3); reachability and chat - measured live (EV8, EV11);
     config-over-env at runtime - code read only; Path B behavior - unmeasured.
PLAIN LANGUAGE: Jarvis needs one address to find its brain server. Most of Jarvis reads that address
     from its settings file. One part (the piece that talks to cloud models) still reads it from a
     sticky note on the computer instead. Today both say the same thing, so everything works. The risk
     is that someone updates the settings file and forgets the sticky note. We are fixing that one part
     so there is only one place to look, and until then the sticky note stays.
GATE-BY-GATE (chat, as measured EV11): G1 client -> 127.0.0.1:8010 TCP, HTTP/1.1 POST
     /v1/chat/completions, JSON UTF-8, no auth on loopback | G2 FastAPI route -> agent native_openhands
     -> engine ollama (qwen3-coder:30b) | G3 engine -> 172.16.33.200:11434 TCP, HTTP/1.1 POST /api/chat,
     JSON UTF-8, httpx pooled (3 keep-alive) | G4 response 200 back through G3/G1.
EXECUTION PATH DELTA: /v1/chat/completions live and measured end to end (entry route, engine, remote).
     Managed-agent routes enumerated from openapi (EV10); not exercised.
V&V PATTERN (reusable): baseline block -> owner restart -> post block (START, self-loop, bounded log
     window) -> scripted round trip as Start-Job with 250 ms TCP sampling. Evidence files in
     evidence\W80\.
### [ARCHIVE-W80-2026-09-23.md] s6 Progress against the 28
VERIFIED 3/28 unchanged (RQ-021, 022, 030). Moved: the engine now reaches its model host through the
author's documented configuration, not an ambient env var, and chat is proven end to end on the live
server with no self-loop. That is a reliability and configuration-management precondition under every
row. The host-resolution map (four paths, one endpoint, one external boundary) is the first piece of
the SDP's data-flow chapter an AO would sign against.
### [ARCHIVE-W80-2026-09-23.md] s7 Deltas to carried registers
TOOLING +: evidence\W80\pre-restart.txt, post-restart.txt, roundtrip.txt capture pattern; round-trip
   instrument (Start-Job + 250 ms Get-NetTCPConnection sampling + bounded log window);
   evidence\W80\W80-ollama-bundle.md (ollama.py, _discovery.py, w79_fallback_check.py; untracked,
   not uploaded).
CLEANUP +: F1 cloud_router._ollama_host() and init_cmd.py:200 - duplicate host resolution bypassing
   config; patch to config > env > default. .bak files inside src\ (H-W80-6).
EXECUTION PATHS +: /v1/chat/completions measured (s5 gate list).
CONFIG BASELINE +: [engine.ollama] host; env vars kept; Python 3.12.10 pin.
RULES +: NO BLIND OWNER DECISIONS (author intent, effects, risks first). Check the archive record
   before any re-derivation. Bound by-name extraction above the CARRIED marker.
### [ARCHIVE-W81-2026-09-23.md] INDEX
s1 Window subject and narrative | s2 Evidence | s3 Negative results | s4 Hazards | s5 SDD/SDP feed | s6 Progress against the 28 | s7 Deltas to carried registers
Carried: W80 s5-s7 verbatim, then W80 carried block (W79 and earlier). Extract by name BOUNDED ABOVE '## ---------- CARRIED FROM ARCHIVE-W80 BELOW ----------'.
### [ARCHIVE-W81-2026-09-23.md] s1 Window subject and narrative
Subject: F1 host resolution (cloud_router.py, init_cmd.py), then F2 embeddings.py. Same subject: model host resolution.
Ex1: cloud_router.py (434 lines) and init_cmd.py (556 lines) bundled whole and uploaded (W81-F1-bundle.md, root, untracked).
Ex2: callers and config accessors mapped by Select-String across src\ excluding .bak (evidence\W81\F1-callers.txt).
Ex3: this scaffold; bundle 2 (routes, config, engine ollama, agent_manager_routes, _discovery, embeddings).
Ex4: bundle 2 read whole. Path B conditions pinned (routes.py:374-388, :480-483). load_config lru_cached (config.py:1744). OllamaEngineConfig.host default "" (config.py:322).
Ex5: owner corrected Claude - raise is NOT author intent; author had local inference, Graystone rebuilt comms for remote MCP/Ollama/faster-whisper.
Ex6: MEASURED - upstream raw main cloud_router :297-298 = env > localhost; pickaxe + blame = f2fcb30 (repo ROOT commit, so blame alone cannot separate author from Graystone). F1a reframed and applied (backup 20260923_130442).
Ex7: test_F1a.py T1-T3 PASS; T1 discriminating (dead env -> .200, 29 live models).
Ex8: s5.1 SDP change record written. Logging: openjarvis.server reaches backend.log - confirmed by ARCHIVE-W45 :159/:255.
Ex10-11: console review - FastAPI duplicate operation ID (lazy, fires at first /openapi.json or /docs); ws-accept authed=False (typical boot, frontend).
Ex12-14: live V&V PASS (V3 rerun with qwen3-coder:30b after instrument miss). Ex14: commit 0da22e8, pushed both remotes, hashes matched.
### [ARCHIVE-W81-2026-09-23.md] s3 Negative results
- cloud_router :344 and :364 are NOT cloud calls. Established by whole-file read: :344 is in stream_local(), POST {host}/api/chat; :364 is in list_local_models(), GET {host}/api/tags, returns [] on any error. Both are a local Ollama client that bypasses the engine.
- _detect_running_engines() (init_cmd) probing localhost only is NOT a defect: author intent is to detect engines on this machine.
### [ARCHIVE-W81-2026-09-23.md] s4 Hazards
- H-W81-1: jarvis init --host is ignored by _do_download (init_cmd.py:200 reads OLLAMA_HOST else localhost). A remote-host init pulls the model against localhost, where no Ollama exists on this box.
- H-W81-2: cloud_router [DEBUG] prints go to sys.stderr = detached console, unreadable (logging topology lesson).
- H-W81-5: DUPLICATE route - FastAPI UserWarning Duplicate Operation ID speech_health_v1_speech_health_get, api_routes.py. Emitted via warnings module = CONSOLE ONLY, never in backend.log. Reproducer: GET /openapi.json.
- H-W81-6: ws_bridge ws-accept authed=False while api_key_set=True (loopback only). AC/IA question for AO. Check event-bus record before re-deriving.
- H-W81-7: speech_router logs TTS START/TTFB/DONE timing at WARNING level (level misuse; benign).
### [ARCHIVE-W81-2026-09-23.md] s5 SDD/SDP feed
- Path B = cloud_router local Ollama client. Callers: routes.py:330-385 stream_local() as engine fallback (condition PENDING whole read); routes.py:473-482 list_local_models() for model listing.
- Sixth host reader, not in W80 list: agent_manager_routes.py:109 cfg.engine.ollama.host (config only, "" without cfg).
- Author intent: two equal operator procedures for a remote host, `jarvis config set engine.ollama.host URL` or `export OLLAMA_HOST=URL` (ask.py:812-813, hints.py:29). engine/ollama.py:40 states priority config > env > default.
- Accessor: core.config.load_config() (config.py:1745) -> cfg.engine.ollama.host.
### [ARCHIVE-W81-2026-09-23.md] s5.1 CHANGE RECORD F1a - cloud_router Ollama host resolution (for AO review)
STATUS: COMMITTED 0da22e8 (main), pushed origin (GitHub) + gitlab (lab), hashes matched. Unit T1-T3 PASS; live V1-V4 PASS on PID 9880 (START 13:15:07). NOT PROVEN: live Path B1 fire.
Control mapping below is the engineering assessment for the package; the assessor and AO make the determination.
1. IDENTIFICATION
- File: src\openjarvis\server\cloud_router.py. Function _ollama_host() (was :311-320) plus "import logging".
- Marker tag in code: openjarvis-w81-f1-host-order-v1. Diff: 24 insertions, 5 deletions.
- Backup: evidence\W81\backup\cloud_router.py.bak-W81-F1a-20260923_130442. Patch script: evidence\W81\patch_F1a_cloud_router.py.
- Change authority: owner (Gray). Authoring assistant: Claude. Pre-change git HEAD a0704c4.
- Line endings: file is CRLF in the working copy; git normalizes to LF on commit (warning expected, not a fault).
2. PURPOSE (technical)
Make cloud_router resolve the Ollama host the same way the engine does: config.toml [engine.ollama] host first,
OLLAMA_HOST environment variable second, and stop with a clear error if neither is set. Removes cloud_router's hard
dependency on the environment variable, which is the precondition for the owner decision on removing OLLAMA_HOST.
3. BASELINE AND PROVENANCE (how each fact was established)
- Author original: upstream open-jarvis/OpenJarvis main, cloud_router.py :297-298 = env OLLAMA_HOST else
  http://localhost:11434 (local inference design). Fetched raw 09/23 and diffed against ours. Caveat: current
  upstream main, not the 05/30 snapshot we forked; upstream has since moved (keys from env, _openrouter_model_id).
- Graystone f2fcb30 (2026-05-30, "remote MCP/Ollama integration"): replaced the localhost default with a raise.
  Reason (owner): Ollama and faster-whisper run on the remote MCP host 172.16.33.200; a localhost fallback on the
  Windows box silently self-loops to a port with nothing behind it.
- Blame alone could not attribute this: f2fcb30 is the repo root commit (^) and carries author lines too. The
  upstream diff is the evidence.
- W81 result: config > env > raise. Keeps the Graystone guard; adopts the author's config-first priority
  (engine\ollama.py:40) and the author's accessor (core.config.load_config -> cfg.engine.ollama.host, same as
  agent_manager_routes.py:109).
4. WHERE THIS CODE RUNS (execution paths affected - Path B)
- Path B1, routes.py:374-388 _handle_stream: stream_local() is used ONLY when the request streams, the model is not
  a cloud model, the engine is a MultiEngine, and that MultiEngine would route the local model to a cloud engine.
  A guard against routing confusion, not the normal chat path. Normal local chat uses engine.stream() (Path A).
- Path B2, routes.py:480-483 GET /v1/models: list_local_models() is used ONLY when engine.list_models() returns
  no local model IDs (for example, engine down).
- Path A (engine) is NOT changed by this patch.
5. GATE DETAIL - Path B data flow
- Source: OpenJarvis backend on the Windows box, Python 3.12.10, served on 127.0.0.1:8010.
- Destination: Ollama on 172.16.33.200 (ollama-mcp), TCP 11434, internal lab segment.
- Protocol: HTTP/1.1 over plain TCP via httpx.AsyncClient. NO TLS. NO authentication (Ollama API has none).
- B1 POST /api/chat: request JSON, UTF-8, body {model, messages, stream:true, think:false, options}; response is
  NDJSON (one JSON object per line), streamed; timeout 300 s.
- B2 GET /api/tags: response JSON, UTF-8; timeout 10 s.
- Host value source after W81: config.toml [engine.ollama] host = "http://172.16.33.200:11434" (UTF-8 no BOM,
  CRLF, OUTSIDE GIT), else OLLAMA_HOST.
6. SECURITY IMPACT ANALYSIS
- Before: host from OLLAMA_HOST only. Missing variable = hard failure on B1; B2 raised outside its try (500).
- After: host from config first. A config read failure is logged as a WARNING on logger "openjarvis.server" and
  falls back to OLLAMA_HOST. Neither set = same hard stop as before, with a clearer message.
- Error text reaches the chat client (routes.py:407-429 surfaces exception text as a content chunk). The new
  message contains no secret, key, path, or host address.
- load_config() is lru_cached (config.py:1744): the host is read once per process. A config change takes effect
  only after a restart - same as the engine. OPENJARVIS_CONFIG, if set, redirects which config file is read.
- No new port, protocol, listener, dependency, or credential. Attack surface unchanged.
7. RESIDUAL RISKS AND POA&M CANDIDATES (not fixed by F1a, stated plainly)
- SC-8 transmission confidentiality: Path B (and Path A) to 172.16.33.200:11434 is plaintext HTTP.
- IA-9 service identification and authentication: the Ollama API accepts any caller on the segment; OpenJarvis
  does not authenticate the service and the service does not authenticate OpenJarvis.
- H-W81-3: list_local_models() calls _ollama_host() outside its try; a missing host returns 500, not [].
  To be patched in W81 as its own change.
- H-W81-2: [DEBUG]/[RETRY] print() to stderr in cloud_router (Graystone additions) are not captured by backend.log.
- OLLAMA_HOST (3 scopes) and OPENJARVIS_OLLAMA_HOST (2 scopes) remain set; removal is an owner decision after F1.
8. CONTROL MAPPING (assessment)
CM-2 baseline (author vs Graystone vs W81 recorded) | CM-3 change control (backup, tag, record, commit in own
block) | CM-4 impact analysis (section 6) | CM-6 configuration settings (config.toml authoritative, env fallback)
| SA-10 developer configuration management (provenance, upstream diff) | SA-11 developer testing (section 9) |
SI-11 error handling (section 6) | AU-2/AU-3 event logging (warning logger; reaches backend.log - CONFIRMED BY RECORD
ARCHIVE-W45 :159/:255, openjarvis.server lines measured in backend.log) | SC-8 and IA-9 residual gaps (section 7).
9. TEST EVIDENCE - evidence\W81\F1a-test.txt, driver evidence\W81\test_F1a.py (non-interactive, child processes,
controlled env, each child prints the imported module path = src\openjarvis\server\cloud_router.py)
- T1 PASS: OLLAMA_HOST=http://127.0.0.1:9 (dead), real config -> host http://172.16.33.200:11434; live
  list_local_models() returned 29 models (matches pinned inventory of 29). DISCRIMINATING: old code returns the dead
  host and 0 models.
- T2 PASS: config with no host, OLLAMA_HOST=http://10.255.255.1:11434 sentinel -> sentinel. Env fallback holds.
- T3 PASS: config with no host, no env -> RuntimeError "Ollama host not configured...". Guard holds.
- Parent context: OPENJARVIS_CONFIG unset; OLLAMA_HOST=http://172.16.33.200:11434.
10. NOT PROVEN (as of this entry)
- The live server executing the patched code (requires restart; pending live V&V).
- A live Path B1 fire (cannot be driven without contriving a MultiEngine misroute; T1 exercised the function
  with real network traffic instead).
11. ROLLBACK
Copy-Item -LiteralPath 'C:\Users\Admin\OpenJarvis\evidence\W81\backup\cloud_router.py.bak-W81-F1a-20260923_130442' -Destination 'C:\Users\Admin\OpenJarvis\src\openjarvis\server\cloud_router.py' -Force
then restart the backend and confirm by process START time.
12. PLAIN LANGUAGE
Jarvis needs to know which computer does its thinking. It has a phone book (the settings file) and a sticky note
(an environment variable). One part of Jarvis used to read only the sticky note, and if the note was missing it
stopped and said so. Now it reads the phone book first and the sticky note second. If both are empty it still
stops and says so, instead of guessing and calling a phone that nobody answers. The call itself goes across the
lab network without a lock on it (no encryption, no password); that is written down as an open item to fix.
### [ARCHIVE-W81-2026-09-23.md] s6 Progress against the 28
VERIFIED 3/28 unchanged. W81 moved infrastructure: all Ollama host readers now honor config first except init_cmd/embeddings (F1b, F2); the OLLAMA_HOST env dependency that blocked removal is gone from cloud_router.
### [ARCHIVE-W81-2026-09-23.md] s7 Deltas to carried registers
- CLEANUP: cloud_router [DEBUG] stderr prints; stream_local removeprefix("openrouter/") copy artifact; deprecated config.py:430 ollama_host property still used by cli\model.py:228 and engine\_discovery.py:20.
- EXEC PATHS: Path B callers above.
- TOOLING: bundler must read with Get-Content -Encoding UTF8; default PS 5.1 read double-encodes non-ASCII (seen W81 bundles). Files on disk unaffected.
- TOOLING +: evidence\W81\test_F1a.py host-resolution test driver (child processes, controlled env, module-path proof).
- TOOLING CORRECTION: cli\serve.py:513 "[DEBUG] wired memory_backend" now logs as INFO openjarvis.cli.serve (seen in console 09/23) - register listed it unreadable; re-confirm in backend.log.
- TOOLING LESSON: verify an instrument input exists before relying on it (V3 assumed a model string in evidence\W80\roundtrip.txt; none). PS -match is case-insensitive: use -cmatch on level field.
- CLEANUP +: H-W81-5 duplicate speech_health route; speech_router WARNING-level timing; cloud_router [DEBUG]/[RETRY] stderr prints; stream_local openrouter/ strip.
- EXEC PATHS +: Path B1 stream_local fallback, Path B2 list_local_models fallback (conditions in s5.1 section 4). Sixth host reader agent_manager_routes.py:109.

