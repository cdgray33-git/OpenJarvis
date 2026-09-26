# VOL 3A - AUTHOR BASELINE AND GRAYSTONE DIVERGENCE REGISTER
v0.3 W77 2026-09-22 (v0.2 W76, v0.1 same day). v0.3: section F qualification instruments and results; D-03, D-07 measured. Owner rule 09/22: the author's procedures come first.
Graystone aligns to them, and every departure is recorded in section D with its class and reason.
v0.2: section C maps all 28 core rows; section E explains the confirmation gate; D-13 added;
base pinned to upstream af21bc18 (W73 CM-01).

Plain language: the people who wrote OpenJarvis published instructions for installing and
running it. This document keeps those instructions as the ruler. Every place our setup is
different is written down in section D, so a real bug can be told apart from "we set it up
differently" or "our copy is older than their instructions". Section C says, for each thing
the executive assistant must do, whether the author already built it, built part of it, or
did not build it at all.

## SOURCES
Upstream clone C:\Users\Admin\upstream-OpenJarvis (read-only). Freshness = git last-commit date;
clone file dates are checkout time only (W76 negative result).
| Doc | Last commit | sha256 (first 16) |
|---|---|---|
| docs\getting-started\install.md (canonical, README links it) | 2026-09-04 | e19f1a6937883ed0 |
| docs\getting-started\installation.md (contributor/manual path) | 2026-06-20 | 3d1e68b262fb3c7c |
| docs\getting-started\windows-native.md | 2026-07-01 | 068acfec0041a06f |
| docs\getting-started\configuration.md | 2026-09-21 | b51ef1b5e200432f |
| docs\user-guide\channels-and-connectors.md | 2026-08-14 | 619d390f5076ea78 |
| docs\user-guide\tools.md | 2026-09-04 | 16c83e426674a5f1 |
| docs\user-guide\system-access.md | 2026-07-28 | 412534c98c62adb5 |
| docs\user-guide\security.md | 2026-09-04 | 661570ac4fcf871d |
| docs\deployment\api-server.md | 2026-08-20 | 5b8a3fcbe3f7bf28 |
| docs\user-guide\memory.md | 2026-03-12 | 081bfdb7afaba4ed |
| docs\user-guide\agents.md | 2026-09-04 | 48e11037c3e50ae8 |
| docs\user-guide\morning-digest.md | 2026-04-03 | 63f0c2c1eea32593 |
| docs\user-guide\scheduler.md | 2026-03-12 | 21b215b87898d05c |
| docs\user-guide\cli.md | 2026-09-21 | 64572c26a2b936b2 |
| docs\user-guide\channels.md | 2026-03-27 | e99b2f414438cc03 |
| docs\testing\agent-qa-runbook.md | 2026-03-16 | (Tier A, RTM section 4) |
| quickstart.md, wsl2.md, snippets.md, README.md | see inventory | see inventory |
Evidence (docs\SDP\evidence\W76\): author-docs-inventory.md, graystone-vs-author-install.md,
fork-point.md, author-capability-bundle.md (the 11 capability docs above, verbatim).
VERSION LAG: Graystone is a snapshot import (root f2fcb30, 2026-05-30), based on upstream
af21bc18 (2026-05-19; W73 CM-01). The docs above describe upstream HEAD (09-21), so a documented
feature may not exist in our code. Each section D row states CHOICE, LAG, MATCH or OPEN.

## A. INSTALL PATH
A1 Canonical doc: install.md. installation.md is the older clone + uv sync + maturin + npm run dev
   path, retained by the author (author duplicate, not ours to remove).
A2 Windows: WSL2 is the author's recommended path. Native Windows is "advanced" (RFC #298):
   install.ps1 -> %LOCALAPPDATA%\OpenJarvis\src, uv sync --extra desktop --group desktop-native,
   optional scheduled task deploy\windows\jarvis-service.ps1, loopback 127.0.0.1:8000, verify /health.
A3 Requirements: Python 3.10-3.13, uv, git, Rust (extension for memory + security), Node 18+ for UI.
A4 Health checks: jarvis doctor; GET /health.
A5 Desktop: prebuilt installers or tauri build; app connects to localhost:8000.
Measured W76: Python 3.12.10 OK. uv 0.11.11 OK. openjarvis_rust 0.1.0 built OK.

## B. CONFIGURATION BASELINE
Author: ~/.openjarvis/config.toml; overrides OPENJARVIS_HOME, XDG_DATA_HOME, OPENJARVIS_CONFIG.
Author defaults that matter here:
- [engine.ollama] host (nested form; old flat ollama_host still accepted).
- [agent] default_agent = simple, max_turns = 10, context_from_memory = true.
- Tools come from tools.enabled, falling back to agent.tools; both empty = ZERO tools.
- [tools.storage] replaces [memory] (old name still accepted).
- [server] host 127.0.0.1, port 8000, agent orchestrator. Auth: OPENJARVIS_API_KEY or
  [server.auth].api_key; configure it before binding 0.0.0.0.
- [security] mode warn; enforce_tool_confirmation is read by NOTHING (author, system-access.md).
- [security.capabilities] RBAC and [sandbox] exist, both off by default.
- [telemetry] enabled = true. [traces] enabled = false.
Measured W76: config at the author default path; no override variables set. Values in section D.

## C. CORE REQUIREMENT -> AUTHOR MECHANISM (R1.2, doc level, all 28 measured rows)
Status: COVERED = the author ships a mechanism that does the row. PARTIAL = some of it, or read
only, or one provider. GAP = nothing in the author's product does it.
| Req | Author mechanism | Status | Author's own check | Source |
|---|---|---|---|---|
| RQ-001 | desktop extra "local speech input"; digest TTS via Cartesia/OpenAI (cloud) | PARTIAL | none documented | installation.md, morning-digest.md |
| RQ-002 | data connectors are READ-ONLY; no mailbox-management tools | GAP | - | channels-and-connectors.md |
| RQ-004 | SSE on /v1/chat/completions; managed-agent streaming; WS /v1/chat/stream; stop not documented | PARTIAL | curl -N streaming example | api-server.md, agents.md |
| RQ-005 | gmail_imap connector indexes last 500 (max_messages); email channel IMAP poll UNSEEN | PARTIAL | runbook channel Gmail/Email receive | channels-and-connectors.md, channels.md |
| RQ-006 | email channel (SMTP) via channel_send tool, POST /v1/channels/send, jarvis channel send | PARTIAL | runbook channel Email send | channels.md, tools.md, cli.md |
| RQ-007 | none | GAP | - | - |
| RQ-008 | email channel In-Reply-To; Gmail threadId | PARTIAL | runbook thread/reply tests | agent-qa-runbook.md, channels.md |
| RQ-009 | none | GAP | - | - |
| RQ-010 | none | GAP | - | - |
| RQ-011 | gmail_imap, outlook (IMAP, Inbox only), email channel generic SMTP/IMAP | PARTIAL | - | channels-and-connectors.md, channels.md |
| RQ-012 | requires_confirmation on shell_exec, git_commit, agent_kill only; server and desktop AUTO-APPROVE | GAP | - | system-access.md, security.md |
| RQ-013 | gcontacts connector (People API, read/index) | PARTIAL | - | channels-and-connectors.md |
| RQ-014 | none (connectors are read-only) | GAP | - | - |
| RQ-015 | none | GAP | - | - |
| RQ-016 | gcalendar connector (read/index, all calendars); digest calendar section | PARTIAL | jarvis digest --text-only | channels-and-connectors.md, morning-digest.md |
| RQ-017 | none | GAP | - | - |
| RQ-018 | none | GAP | - | - |
| RQ-019 | none | GAP | - | - |
| RQ-020 | Google Calendar only | GAP | - | channels-and-connectors.md |
| RQ-021 | web_search tool (You.com keyless default, DuckDuckGo fallback) | COVERED | jarvis ask --agent orchestrator --tools calculator,web_search "What is the GDP of France in USD?" | quickstart.md, tools.md |
| RQ-022 | calculator tool (ast-based) | COVERED | jarvis ask --agent orchestrator --tools calculator "What is 137 * 42?" | installation.md, tools.md |
| RQ-024 | memory_store / memory_retrieve / memory_search; MEMORY.md via memory_manage; Obsidian, Apple Notes (read) | PARTIAL | jarvis memory index / search | tools.md, agents.md, memory.md |
| RQ-025 | llm tool; any agent | COVERED | llm tool: prompt "Summarize: ..." | tools.md |
| RQ-026 | orchestrator loop + scheduler tools; chain needs RQ-006, 007, 015, 017 | PARTIAL | - | agents.md, scheduler.md |
| RQ-028 | substrate only: AgentResult.tool_results, TOOL_CALL_START/END events, audit log, traces | GAP | - | agents.md, tools.md, security.md |
| RQ-029 | OpenAI-compatible API, managed-agents API, SDK ask_full, /v1/channels/send | PARTIAL | curl /v1/chat/completions | api-server.md, agents.md |
| RQ-030 | Ollama engine; local-first default when no cloud key in env | COVERED | jarvis model list; call served by engine ollama | install.md, configuration.md |
| RQ-031 | SOUL/MEMORY/USER.md persona; memory_manage; operative session store; traces + learning | PARTIAL | - | agents.md, configuration.md |
TOTALS: COVERED 4 (RQ-021, 022, 025, 030). PARTIAL 12. GAP 12.
FINDING: the author built a research-and-reading assistant. Its connectors read and index data.
The executive-assistant WRITE duties - draft, label, mark read, add or update contacts, create,
update or delete events, approve before send, verify own steps - are not in the author's product
at upstream HEAD. Pulling upstream will not close the 12 GAP rows; those are Graystone's to build,
on the author's mechanisms (tools via ToolRegistry, confirmation via requires_confirmation).

## D. DIVERGENCE REGISTER
| ID | Area | Author | Graystone (measured W76) | Class | Note |
|---|---|---|---|---|---|
| D-01 | Install location | %LOCALAPPDATA%\OpenJarvis\src or ~/.openjarvis/src | C:\Users\Admin\OpenJarvis repo, own .venv | CHOICE | W73 E14: author-shape ~/.openjarvis also exists in WSL2 Ubuntu |
| D-02 | Service | scheduled task jarvis-service.ps1 | none; manual admin start-openjarvis.ps1; file absent from repo | LAG | author added after base af21bc18 |
| D-03 | Engine host | [engine.ollama] host | no [engine.ollama] section; remote Ollama 172.16.33.200 | OPEN | W77 E3: runtime peer 172.16.33.200:11434 measured; config source of host still open |
| D-04 | Storage section | [tools.storage] | legacy [memory] | LAG | backward compatible |
| D-05 | Default agent | simple / server orchestrator | native_openhands (both) | CHOICE | CodeAct agent |
| D-06 | Default tools | none (zero tools) | code_interpreter, file_read, file_write, shell_exec, think, calculator, retrieval, 5 mailbox tools incl move_to_trash, empty_folder | CHOICE | destructive set, see H-W76-EXPOSURE |
| D-07 | Server bind and auth | 127.0.0.1:8000; API key before 0.0.0.0 | 0.0.0.0:8010; no [server.auth] section; OPENJARVIS_API_KEY unmeasured | CHOICE/OPEN | author auth may postdate base; H-W74-AUTHOFF. W77 E1: RUNTIME binds 127.0.0.1:8010 (pid 17884) although config says 0.0.0.0 |
| D-08 | Tool confirmation | only 3 tools marked; server/desktop auto-approve | enforce_tool_confirmation unset; behaviour on our 05-19 code not yet measured | MATCH | gap is the author's; RQ-012, Defect 6 |
| D-09 | Traces | false | unset (false) | MATCH | blocks RQ-031 learning, runbook Desktop 9 |
| D-10 | Extra sections | not in configuration.md | [speech] model base; [analytics] enabled false | OPEN | verify against author docs |
| D-11 | Default model | empty (router) | qwen3-coder:30b | CHOICE | |
| D-12 | Desktop | prebuilt or tauri build | production tauri build from repo | CHOICE | production only (owner rule) |
| D-13 | Traces modules | ships traces\analyzer.py, traces\collector.py (+7 tests) | deleted at Graystone HEAD (W73 E6) | OPEN | reason unrecorded; affects RQ-031 |
HAZARD H-W76-EXPOSURE: D-05 + D-06 + D-07 + D-08 together = LAN-bound server with no configured
API key, CodeAct agent holding shell_exec (no allowlist, author-stated) and destructive mailbox
tools, and every tool in the toolkit auto-approved on the server and desktop paths. Confirm auth
state by whole-file upload of server\app.py (BRIEF W75 item 6).

## E. THE CONFIRMATION GATE - PLAIN LANGUAGE AND TECHNICAL
Plain language: some tools are dangerous, like typing commands into the computer. The author put
an "ask me first" sticker on three of them: shell_exec, git_commit and agent_kill. Whether anyone
actually asks depends on the door you came in through. Through jarvis chat, Jarvis stops and asks
you every time. Through jarvis ask, the web server, or the desktop app, Jarvis treats the sticker
as already signed and goes ahead without asking. If a programmer builds the agent in their own
code and forgets to give it a way to ask, the tool refuses to run at all. There is a setting
called enforce_tool_confirmation that looks like a master switch; it is not connected to
anything. Sending email and deleting mail have no sticker at all in the author's version. Our
desktop app and server are the "goes ahead without asking" doors, which is why Graystone is
building its own asking mechanism (Defect 6).
Technical (system-access.md, 07-28):
| Entry point | Behaviour |
|---|---|
| jarvis chat | prompts before each requires_confirmation call |
| jarvis ask | auto-approves |
| jarvis agent ask | auto-approves; --no-yes enables prompts |
| HTTP server, desktop app | auto-approves; tools in an agent's toolkit count as pre-approved |
| Embedded via SystemBuilder | no callback wired; tool fails closed with "requires confirmation but no confirmation callback is available" |
security.enforce_tool_confirmation: accepted by the loader, read by nothing on the execution path.
Capability RBAC ([security.capabilities]) is opt-in; grants never bypass requires_confirmation.
Policy identity per path (security.md): managed-agent tick or stream = the agent ID; CLI, SDK or
selected server agent = the runtime agent name; server agent-management API = server:api;
standalone MCP executor = mcp; scheduler without an agent = scheduler.
Trace: RQ-012 -> this section -> Defect 6 (confirm registry, POST /v1/tools/confirm).

## F. QUALIFICATION INSTRUMENTS AND RESULTS (W77)
Plain language: a requirement row only counts as VERIFIED when we can SHOW the tool actually ran,
not just that the answer looks right. If you ask a student "what is 137 times 42" and they write
5754, you still do not know whether they used the calculator or remembered it. Jarvis is the same:
the model can answer many questions from memory, so a correct answer proves nothing about the tool.
We need a receipt from the machine that says "the calculator ran, here is what it returned".
Finding that receipt is what this section is about. Defect 1 (Jarvis claiming actions it never
took) is why this rule exists.

### F1. The test infrastructure, gate by gate (measured W77)
Gate 1 OPERATOR: PowerShell on the Windows box, working directory C:\Users\Admin\OpenJarvis.
Gate 2a SURFACE A - LIVE SERVER: HTTP/1.1, JSON body UTF-8, POST http://127.0.0.1:8010/v1/chat/completions,
  OpenAI chat-completions shape, stream false. Listener measured on LOOPBACK 127.0.0.1:8010 only
  (config says 0.0.0.0 - see D-07). Process pid 17884 = GLOBAL C:\Users\Admin\AppData\Local\Programs\
  Python\Python312\python.exe, which imports C:\Users\Admin\OpenJarvis\src\openjarvis (editable install,
  so it IS our repo code). Agent: server default native_openhands (D-05). This is NOT the author's check.
Gate 2b SURFACE B - AUTHOR CLI: jarvis ask --agent orchestrator --tools <tool> "<prompt>" - the author's
  own check, verbatim from section C. jarvis.exe = global Python312\Scripts\jarvis.exe, same src.
  Runs in-process (builds its own agent; does not go through the server). Auto-approves (section E).
  Output: final answer text only - no tool trace printed.
Gate 2c SURFACE C - AUTHOR SDK: Jarvis.ask_full(...) returns AgentResult with tool_results - the
  author's own invocation record (section C, RQ-028/RQ-029). Instrument scripts\diag\sdk_verify.py.
Gate 3 ENGINE: HTTP/1.1 JSON from 192.168.1.137 (Windows box) to 172.16.33.200:11434 (Ubuntu Ollama
  host, Graystone lab), model qwen3-coder:30b. Measured as an ESTABLISHED TCP connection owned by pid 17884.
Gate 4 EVIDENCE STORES - what each can and cannot prove:
  - telemetry.db (C:\Users\Admin\.openjarvis\telemetry.db, SQLite, one row per MODEL call): proves
    engine and model. Has NO tool columns. agent column EMPTY and metadata {} on both surfaces.
  - /v1/traces (HTTP GET): [traces] disabled (D-09) - recorded 0 traces. Cannot prove anything today.
  - Response body tool_calls (OpenAI shape): null on every run.
  - CLI stdout: answer only.
  - AgentResult.tool_results (SDK): the only author-shipped per-call tool record. Surface C.

### F2. Instruments (all in the tooling register)
- surface probe (inline block, output docs\SDP\evidence\W77\surface-probe.txt): listener, 94 routes from
  /openapi.json, CLI path, telemetry.db schema.
- scripts\diag\rtm_verify.py: Surface A. Snapshots trace ids and telemetry max id, sends each check,
  collects the new traces, new telemetry rows and raw response. Output evidence\W77\rtm-verify.json.
- scripts\diag\w77_tel.py: telemetry max id / rows after an id. Used around the author CLI checks.
- author-check-RQ-0xx.txt (evidence\W77): raw CLI output of each author check.
- scripts\diag\sdk_verify.py: Surface C. Output evidence\W77\sdk-verify.json.

### F3. Results
| Run | Surface | RQ-022 calc | RQ-021 web_search | RQ-025 llm | Invocation proven? |
|---|---|---|---|---|---|
| 1 | A server, native_openhands | "5,754" correct, tool_calls null | stale 3.12.2 "based on my knowledge", 6 model calls | correct, 2 calls | NO - model knowledge |
| 2 | B author CLI, orchestrator | "5754", 2 model calls | "$2.86T (2023)", 2 calls | correct, 1 call | NO - CLI shows no trace |
| 3 | C author SDK | see F5 | see F5 | see F5 | see F5 |
Model-call count is an INDIRECT signal only: 2 calls fits "ask, run tool, answer"; 1 call for RQ-025
means the llm tool (which makes its own model call) most likely did not run.
RQ-030: engine=ollama on telemetry 7118-7132; host proven by TCP peer 172.16.33.200:11434; author's
jarvis model list recorded in evidence\W77\model-list.txt.

### F4. Negative results and hazards
- REGISTERED IS NOT INVOKED: /v1/tools lists calculator, web_search, llm as configured; that proves
  availability, not use.
- Surface A (our server default agent) did not invoke tools for any author check.
- /v1/traces is not an invocation instrument while [traces] is disabled; this is also why RQ-028
  (verify own steps) has no durable record.
- H-W77-GLOBALPY (downgraded): server and CLI run the global interpreter against repo src; the global
  and .venv dependency sets may differ. Logged in the CLEANUP REGISTER.

### F5. Run 3 - SDK results
Run 3 = Surface C, the author SDK (Jarvis.ask_full), the only surface that returns a per-call tool
record. Signature confirmed by introspection before use: ask_full(query, *, model, agent, tools,
temperature, max_tokens, context, channel) -> Dict. Source C:\Users\Admin\OpenJarvis\src\openjarvis\sdk.py.
Result keys: content, engine, model, tool_results, turns, usage.
| Req | tool_results | turns | Verdict | Evidence |
|---|---|---|---|---|
| RQ-022 calculator | [{tool_name calculator, content "5754.0", success true}] | 2 | VERIFIED | sdk-verify.json |
| RQ-021 web_search | [] | 1 | NOT VERIFIED - PARSER | defect1-raw-payload.txt |
| RQ-025 llm | [] | 1 | NOT VERIFIED - not delegated | sdk-verify.json |
| RQ-030 ollama engine | n/a | n/a | VERIFIED | E3 TCP peer + model-list.txt + telemetry |

### F6. RQ-021 IS DEFECT 1, CAPTURED WHOLE
Plain language: Jarvis did ask for the web search. It wrote the request out in its own shorthand,
and the part of our code that reads those requests did not recognise that shorthand, so nothing
ran and the shorthand itself was handed back to the user as if it were the answer. Nothing was
broken about the tool or the network. The handwriting was simply not one of the four styles the
reader knows.
Technical: content was the literal OpenHands XML call - <function=web_search><parameter=query>
France GDP 2023 USD</parameter></function></tool_call> - with a stray </tool_call> closer and no
opener. tool_results empty, turns 1, so the agent loop never saw a call and never took turn 2.
This is the first capture where the unparsed payload survives in the returned answer instead of
being masked by a plausible from-memory reply (Surface A and B both masked it).
Feeds [[openjarvis-defect1-parser]]: compare this shape against the four formats _extract_tool_call
accepts. Feeds Defect 1 engine work: the ENGINE emitted a well-formed intent; the PARSER dropped it.
Reproduce: python scripts\diag\sdk_verify.py <out.json> (RQ-021 case), no server needed.

### F7. QUALIFICATION RULE ESTABLISHED IN W77
A row is VERIFIED only on a machine-produced invocation record. Today exactly one exists:
AgentResult.tool_results via the SDK. telemetry.db proves engine/model only; /v1/traces is disabled;
the OpenAI response tool_calls field was null on every run; CLI stdout shows the answer only.
Therefore Tier B tests for tool-backed rows are written against ask_full, not against the server or
the CLI, until an invocation record exists on those surfaces. Making one exist on the server path is
Defect 6 / event-bus work, and closing RQ-028 (verify own steps) needs it too.

### F8. THE W77 FIX - TWO CAUSES, CODE AND CONFIG (verified on every surface)
Plain language: Jarvis could not search the web, for two separate reasons that hid each other.
First, when Jarvis wrote a request for a tool in its own shorthand, the orchestrator could not read
that shorthand and handed it back to the user as the answer. Only one agent knew how to read it.
Second, and worse, the server had never been given the search tool at all - it had twelve tools and
none of them could search - so when asked for France's GDP it simply made up 7.8 trillion dollars.
Fixing only the reading would not have helped, because there was nothing to call. Fixing only the
toolbox would not have helped, because the request could not be read. Both were needed.
CAUSE 1 - CODE (orchestrator.py _run_function_calling): content and raw_tool_calls are read from
the engine result; when raw_tool_calls is empty the agent returned content as the final answer and
never inspected the text for a call. OrchestratorAgent extends ToolUsingAgent and had no parser;
only native_openhands did. Patch chain, each verified in isolation:
  v1 openjarvis-w77-textparse-v1 - _extract_text_tool_call, _extract_json_text_call and
     _known_tool_names added to ToolUsingAgent (agents\_stubs.py); orchestrator's empty
     raw_tool_calls branch wired to try a text call. SAFETY GATE: a parsed call is accepted only
     if the name matches a REGISTERED tool, neutralising the Format 1 "Action:" prose false
     positive. native_openhands untouched at this step so the working path could not regress.
  v2 textparse-v2 - Format 2 "key: value" (GLM style) parity added to the base.
  v3 textparse-v3 - TAGGED-PARAMETER FIX, a real behaviour change, not parity: the inherited regex
     <tool_call>\s*(\w+)\s*(.*?)</\w+> is non-greedy and stopped at the FIRST closing tag, so
     <key>value</key> parameters were cut off and the call executed with {}. Re-anchored on
     (?:</tool_call>|\Z). native_openhands had carried this defect and was silently dropping
     arguments on tagged-style calls before W77.
  v4 dedupe-v1 - _extract_tool_call (161-250) and _extract_json_tool_call (252-313) removed from
     native_openhands.py by AST boundary, 152 lines / 6510 bytes; call site at 487 repointed to the
     inherited _extract_text_tool_call. Residual count 0. ONE parser on the shared base.
CAUSE 2 - CONFIG (the author-baseline finding, and the reason Surface A first looked like a failed
patch): ~/.openjarvis/config.toml [agent] tools listed 12 tools and web_search was NOT among them.
The comma-separated STRING form is correct and is what the server expects - cli\serve.py:255-265
and :401-412 split it, config.py:933 documents agent.tools as current - so the shape was never the
problem; the CONTENT was. /v1/tools reports the REGISTRY (about 40 tools incl. web_search and llm),
NOT the agent's toolkit, so "registered: True" proved nothing about what the agent could call.
Fixed by adding web_search to [agent] tools; loader then reports 13.
PROOF FROM THE SERVER'S OWN STARTUP BANNER (see F9): allowed= / registry_keys= / tools_loaded=.
Before: allowed had no web_search, tools_loaded had no WebSearchTool. After: both present.
VERIFICATION CHAIN (evidence\W77):
  w77_parse_selftest.py 7/7 - RQ-021 payload, prose -> None, all three Format 2 styles.
  sdk-verify-after.json - orchestrator RQ-021 tool_results [web_search] turns 2.
  sdk-verify-dedupe.json - unchanged after the dedupe (no regression).
  native-after-dedupe.json - the CUT class itself: calculator and web_search, turns 2.
  surfaceA-gdp.json - LIVE SERVER 8010 after config fix: "Based on the search results", World Bank
  and Statista figures, 18.8 s, 2 model calls. Before the config fix the same prompt returned a
  fabricated $7.8 trillion in 2.3 s.
DEFECT 1 BEARING: on the orchestrator path an emitted-but-unparsed text call is now EXECUTED rather
than returned as prose. The separate engine-layer case (model emits no call at all) remains open,
see [[openjarvis-defect1-engine]].
NEGATIVE RESULTS: (a) the first Surface A re-run used MY prompt wording, not the author's check -
not a valid comparison, re-run with the author's prompt; (b) my SEARCH RAN detector matched the
bare word "trillion" and scored the fabricated $7.8T as a PASS - a bad instrument that would have
hidden a Defect 1 event; read the FIGURE, not the flag; (c) agent.tools being a string is NOT a
defect - the loader splits it.
THIRD COPY NOT TOUCHED: agents\monitor_operative.py defines _extract_tool_call at 396 as a
MODULE-LEVEL function but calls it at 280 as self._extract_tool_call(content). Shapes do not match,
so it was not cut blind. Own whole-file step. CLEANUP REGISTER.

### F9. THE STARTUP BANNER - A READABLE INSTRUMENT WE ALREADY HAD
openjarvis.cli.serve emits three [DEBUG] lines through the LOGGING module at every start, so unlike
the serve.py print() statements they DO land in backend.log
(C:\Users\Admin\AppData\Local\OpenJarvis\logs\backend.log):
  allowed={...}        the tool names from config [agent] tools, post-split - the agent's ALLOWED set
  registry_keys=[...]  every tool the registry knows (about 40) - what /v1/tools reports
  tools_loaded=[...]   the tool CLASSES actually handed to the agent - the real toolkit
Reading: allowed vs registry_keys is exactly the config gap above; tools_loaded is ground truth for
what the agent can call. Extract: Select-String -Path <backend.log> -Pattern '\[DEBUG\] (allowed|
registry_keys|tools_loaded)=' | Select-Object -Last 3
Same banner also emits: "wired memory_backend into 1 agent tool(s)" (bears on RQ-024, RQ-031) and
openjarvis.server.auth_middleware BIND-ASSERT host=127.0.0.1 port=8010 loopback=True api_key_set=True.
BIND-ASSERT REVISES D-07 AND H-W76-EXPOSURE: config says host 0.0.0.0, but the server asserts
LOOPBACK and an API KEY IS SET. The LAN-exposure hazard is not live as configured today. The
destructive-toolkit half of that hazard (D-06: shell_exec, file_write, mailbox_move_to_trash,
mailbox_empty_folder in the agent's toolkit, auto-approved on the server path) STANDS UNCHANGED.
D-06 UPDATE: the toolkit is now 13 tools (web_search added W77).

## G. DIVERGENCE AND DECISION REGISTER UPDATE - W78 TO W82 (appended 2026-09-23, W82)
Supersedes section D rows where stated. Section D above is left as written for history.
| ID | Area | Author (af21bc18) | Graystone | Class | Evidence / commit |
|---|---|---|---|---|---|
| D-03 UPDATE | Engine host | [engine.ollama] host; env OLLAMA_HOST; localhost | CLOSED W80: [engine.ollama] host = http://172.16.33.200:11434 in config.toml; OLLAMA_HOST (3 scopes) and OPENJARVIS_OLLAMA_HOST (no reader) KEPT by owner decision, option 2, after risk assessment | MATCH (author form) | [M W80] config out of git |
| D-07 UPDATE | Server bind | 127.0.0.1:8000 | runtime 127.0.0.1:8010 (BIND_ASSERT), config says 0.0.0.0 - unmapped override (H-W80-4); api_key_set=True | CHOICE/OPEN | [M W77, W80] |
| D-14 | file_write scope | allowed_dirs parameter never passed (writes anywhere) | confined to ~\.openjarvis\workspace via [tools] file_allowed_dirs + config.resolve_file_write_dirs (never empty); file_read NOT confined | CHOICE (security) | 829cea7 [M W78] |
| D-15 | Tool builders | two inline loops in serve.py + ask._build_tools | one serve._build_agent_tools for chat and channel; ask._build_tools unchanged (injects llm, memory, channel) - an SDK PASS does not transfer to the server for llm or channel tools | CHOICE | 854b9c7 [M W78] |
| D-16 | Engine turn-down | no off-switch; discovery probes every engine; get_engine falls back to any healthy one | [engine] disabled list -> EngineDisabled at _discovery._make_engine (single choke point); live "vllm,uzu,lemonade,litellm" | CHOICE (security, availability) | a0704c4 [M W79] |
| D-17 | Server port | 8000 | 8010 because a Windows portproxy holds 0.0.0.0:8000 | CONSTRAINT | e0e3652 [M W79] |
| D-18 | cloud_router Ollama host | env OLLAMA_HOST else localhost (local-inference design) | config > env > RAISE (Graystone f2fcb30 replaced localhost with a raise: remote host, localhost would self-loop; W81 adopted author config-first order) | CHOICE | 0da22e8 [M W81]; author comparison was against upstream MAIN, re-ground on af21bc18 (W82) |
| D-19 | init download host (F1b) | env else localhost, ignores --host (author defect, identical to af21bc18) | NO CHANGE - ACCEPTED RISK; rebuild rule: set OLLAMA_HOST before jarvis init or run jarvis model pull after | MATCH (author) | [M W82] evidence\W82\F1b-record.txt |
| D-20 | list_local_models error path (H-W81-3) | same placement; harmless because author host lookup never raises | NO CHANGE - DEFERRED to end security review (our raise makes it fail 500 instead of [] if both host sources are absent) | OPEN (Graystone deviation) | [R W82] evidence\W82\H-W81-3-record.txt |
| D-21 | Embeddings host and model (F2) | localhost default, nomic-embed-text; both files identical to af21bc18; two OllamaEmbedder classes (connectors vs tools\storage) | NO CHANGE - DEFERRED; no live consumer (memory backend is sqlite; research path never run); model not pulled on .200 | MATCH (author) / OPEN | [M W82] evidence\W82\F2-record.txt |
| D-22 | Agent text tool-call parsing | only native_openhands parsed text calls | shared parser on ToolUsingAgent (textparse v1-v3) + orchestrator fallback; one parser, 152 lines removed | CHOICE (fix) | 64b0660 [M W77] |
Owner rulings recorded W82: (1) author baseline for intent = af21bc18 in the local upstream clone, not upstream main; upstream is
a catalog of enhancements to borrow, not a sync target. (2) Dormant findings are recorded, not changed, until the full system is
operational; security assessment is performed at the end (DD-14).
Plain language: this table lists every place our Jarvis is set up differently from the author's, why, and who decided. Three new
items this window were left exactly as the author wrote them and written down instead of changed, because they only matter if
Jarvis is rebuilt or a setting goes missing.


### G.1 W82 H5 addition (appended 2026-09-23)
| ID | Area | Author (af21bc18) | Graystone | Class | Evidence / commit |
|---|---|---|---|---|---|
| D-23 | Speech routes /transcribe, /health | author routes in api_routes.py (speech_backend driven) | Graystone speech_router.py duplicated both and was mounted first (app.py:294), shadowing the author; W82 H5 removed the duplicates so the AUTHOR routes serve again; Graystone keeps /synthesize (Kokoro, D4) and /stream (dead, POAM-38) | MATCH (restored) | [M W82 H5-live V1-V5] |


### G.2 W83 additions - context injection (appended 2026-09-24)
| ID | Area | Author (af21bc18) | Graystone | Class | Evidence / commit |
|---|---|---|---|---|---|
| D-24 | [memory] context injection settings | context_top_k 5, context_min_score 0.0, context_max_tokens 2048, context_from_memory True (core\config.py:874-876, :923) - injection ON by default | Was 3 / 20.0 / 1200 (set against the old 21 GB corpus). 20.0 sat above every score this corpus produces (max 8.32), so injection never fired. RESTORED to author values W83 | MATCH (restored) | [M W83] evidence\W83\author-intent-context.txt, memory-search-scores.txt, inject-probe.txt, optionA-VV.txt; config.toml out of git, backup config.toml.bak-W83-A-20260924_102149 |
| D-25 | System messages sent to Ollama | messages passed through unchanged; _build_messages (agents\_stubs.py, author-unchanged) emits [agent system prompt, context system message, user] | engine\ollama.py _oj_merge_system merges all system messages into one, in order, at the first's position, at generate / stream / stream_full; logs SYSMERGE to backend.log | CHOICE (compatibility fix enabling author intent) | 675cda6 openjarvis-w83-sysmerge-v1 [M W83] h4-multisystem.txt, sysmerge-VV.txt |

Assessment behind D-24 (owner ruling A, W83; "the 20 was based on raw data but was more than 50% noise"):
| Option | Effect | Risk |
|---|---|---|
| A restore author 5 / 0.0 / 2048 (CHOSEN) | author baseline; up to 5 chunks / 2048 words injected on any term match | noise from test content (H-W83-1); per-turn prompt cost; the old 143k blowup cannot recur because top_k and max_tokens bound it |
| B min_score 0.0 only, keep 3 / 1200 | works at lower cost | recorded divergence remains |
| C keep 20.0 | nothing changes | the author feature stays dark; memory requirements unverifiable |

Assessment behind D-25 (owner ruling option 2, W83; "the author's full intent is the requirement"). Root cause measured: the
qwen3-coder:30b Ollama chat template renders only the FIRST system message (one system 58 tokens, two system 59, merged 238).
| Option | Where | Effect | Risk |
|---|---|---|---|
| 1 merge in _build_messages | agents\_stubs.py (shared base class) | fixes agent paths | broad blast radius across all tool-using agents |
| 2 merge at the engine (CHOSEN) | engine\ollama.py, 3 call sites | fixes the defect class for every Ollama caller; cloud path untouched | engine-wide; a mid-conversation system message moves to the top (before: dropped) |
| 3 inject into the user message | routes.py | local | REJECTED - _truncate_if_needed cuts the tail of the last user message, would cut the user's question; diverges from context.py |
| 4 custom Modelfile template | .200 | no code change | REJECTED - diverges from the stock model, hides the defect |
V&V: first-inference prompt_tokens_evaluated 4194 -> 5314 (+1120, predicted about 1100); SYSMERGE merged=2 in backend.log; tool events unchanged.
Owner statement recorded W83: author-first due diligence had been missed; the author's full intent is the requirement.
Plain language: Jarvis's author built it to glance at its notebook before every answer. We had set the "only show me pages this
relevant" dial so high that no page ever qualified - that dial is back where the author set it. Separately, the brain only reads the
first instruction card on the desk, and the notebook page arrived as a second card, so it was never read; Jarvis now staples the cards
together before handing them over.

### G.3 W83 additions - memory tools, ingestion, content (appended 2026-09-24, second package)
Defect record format (owner rule W83): symptom, trigger conditions, fix, evidence.
| ID | Area | Author (af21bc18) | Graystone | Class | Evidence / commit |
|---|---|---|---|---|---|
| D-26 | Memory tools in the chat toolkit | memory_store/retrieve/search/index (storage_tools.py) and memory_manage registered, IDENTICAL to ours; NOT in any author default toolkit (fallback {think, calculator, web_search}, serve.py:197/:275); docstring says MCP-exposed | all five added to [agent] tools (config.toml out of git, backup config.toml.bak-W83-memtools-20260924_114429) | CHOICE (installer decision, owner O3) | 430742c; memtools-VV.txt: store 115->116 dispatch OUTCOME OK, recall BLUEHERON-7731 via injection, +923 prompt tokens per turn |
| D-27 | Toolkit built before the memory backend | serve.py:197 builds tools with tool_cls() (no backend); memory_backend created later at :386 | pre-W83 Graystone backfill wires the backend into retrieval and memory_* tools after both exist ("wired memory_backend into N agent tool(s)") | AUTHOR DEFECT, fixed pre-W83 (backfill), recorded W83 | [R W83 memtools-author-bundle; M W83 wired into 5] |
| D-28 | Upload decode | upload_router.py:182-184 utf-8 then latin-1 | BOM-aware decode + refusal (superseded by D-29) | AUTHOR DEFECT, fixed | a457239; decode-VV.txt |
| D-29 | One decoder for both ingest paths | ingest.py _read_text has the same utf-8 then latin-1 defect | shared decode_text_bytes in tools\storage\ingest.py; upload_router imports it (duplicate removed); refuse ANY NUL or >5% control characters | AUTHOR DEFECT, fixed | 00edd61; decode2-patch (FIRST RULE >10% NUL FAILED on a low-NUL binary - negative result), decode2b-patch, decode2-VV |
| D-30 | Ingest walker skip list | _SKIP_DIRS: hidden dirs, .git, node_modules, .venv, caches, egg-info | + target, dist, build | CHOICE (owner O-a) | 2277df0; skipdirs-patch.txt |
| D-31 | memory.db content | installer content (author leaves it to the installer) | 113 test chunks removed via the author's SQLiteMemory.delete; kept owner EA notes (S-05) and BLUEHERON; snapshot evidence\W83\backup\memory.db.snap-20260924_171031 | CONTENT (owner) | 4ee2053; memdb-titles, memdb-selective-clear |

Defect record D-28/D-29 (decode):
- SYMPTOM: an uploaded or indexed text file is stored but can never be found by search; the model sees letter-by-letter noise;
  SQLite length() reports almost 0 bytes for the chunk (it stops at the first NUL), which misled W83's own first inventory.
- TRIGGER: the file is UTF-16 (PowerShell 5.1 ">" redirection, some Windows editors) or is binary with an allowed extension.
  utf-8 fails, latin-1 never fails, so each character is stored followed by NUL, or binary bytes are stored as text.
- FIX: BOM first (utf-8-sig, utf-16), then utf-8, then latin-1; refuse any NUL or >5% control characters, logged as
  "DECODE refused <file>: nul=N ctl=M" (WARNING, openjarvis.tools.storage.ingest, backend.log). Accepted files log "DECODE <file> as <enc>".
- EVIDENCE: boot_backend_dump.txt (FF FE, 24,438 NUL) produced 50 unsearchable chunks; after the fix a UTF-16 file ingests clean
  and searchable, junk is refused, stats count exactly.
Defect record D-27 (toolkit ordering): SYMPTOM - retrieval and memory tools answer "no backend" in an author-built server.
TRIGGER - any [agent] tools list naming them. FIX - backfill after backend creation (present); verified W83 "wired into 5".
Assessment behind D-26 (owner chose O3 over the O1 lean): O1 store only - minimal; O2 + manage; O3 all five - adds
memory_index (ungated, unconfined path, walker) and redundant readers; O4 none. Owner: "the author put it there for a reason".
Risks carried as POAM-43 (memory_index) and the cleanup register (redundant readers).
Plain language: Jarvis can now write things into its notebook and read them back. Files you give it are read properly even
when Windows saved them in an unusual format, and junk files are turned away at the door instead of filling the notebook with noise.

### G.4 W83 additions - persona layer (appended 2026-09-24, third package)
| ID | Area | Author (af21bc18) | Graystone | Class | Evidence / commit |
|---|---|---|---|---|---|
| D-32 | Persona files seeded | _seed_memory_files() (cli\_bootstrap.py:170) creates SOUL.md, MEMORY.md, USER.md, skills\ if absent; its only callers are write_initial_config() (which FIRST OVERWRITES config.toml) and jarvis init (config behaviour NOT MEASURED) | called _seed_memory_files() ALONE; author default texts; config.toml sha unchanged | MATCH (author function, author content) | c792038; persona-seed.txt |
| D-33 | Persona layer in the prompt | prompt\builder.py SystemPromptBuilder loads SOUL/MEMORY/USER into the system prompt (4000/2500/1500 chars, head_tail truncation) - but has NO CALLER in af21bc18 or locally | none yet (P3 owner-approved next) | AUTHOR INTENT NOT IMPLEMENTED | c792038; persona-wiring.txt |
| D-34 | user_profile_manage | author tool for USER.md (read/add/update/remove), registered, not in any toolkit | none yet (P4 owner-approved after P3) | NOT LOADED | [R W83 persona-wiring] |
Finding: the persona gap is the footprint of the author's installation procedure never having been followed on this install
(owner W83). HAZARD: never run `jarvis _bootstrap --write-config` (overwrites config.toml); do not run `jarvis init` until its
config behaviour is measured.
P2 (b66d8d1): memory_manage DIRECTED take and list PASS (dispatch OUTCOME OK, reply lists AMBERFINCH-5520, MEMORY.md holds it);
UNDIRECTED "What notes do I have?" FAILED - the model called think only and said it has no access to notes. Cause: nothing tells
the model it has notes; D-33 is the author mechanism that would.
Plain language: the author wrote Jarvis a name tag, a diary and a card about you, and a machine to read them to Jarvis before every
conversation - but never plugged that machine in. We have now put the name tag, diary and card on the desk; plugging in the
machine is next.

### G.5 W83 additions - persona layer wired (appended 2026-09-24, fourth package)
| ID | Area | Author (af21bc18) | Graystone | Class | Evidence / commit |
|---|---|---|---|---|---|
| D-35 | prompt_builder hook | BaseAgent accepts prompt_builder and _build_messages uses builder.build() in place of the agent prompt; ToolUsingAgent.__init__ does NOT accept or forward it, so no tool agent can receive it | ToolUsingAgent and NativeOpenHandsAgent accept and forward prompt_builder | AUTHOR DEFECT, fixed | 6429769; persona-patch.txt |
| D-36 | Persona wiring (owner W3) | SystemPromptBuilder has no constructor anywhere; its prefix freezes on first build | serve.py builds SystemPromptBuilder for native_openhands (template = override or OPENHANDS_SYSTEM_PROMPT + tool descriptions, config.memory_files, config.system_prompt), logs "PERSONA prompt_builder wired"; builder rebuilds its prefix only when SOUL/MEMORY/USER.md change (mtime+size) | CHOICE enabling author intent | 6429769; persona-VV.txt |
| D-37 | Notes routing (owner N1) | SOUL.md is installer content | one line: user notes are the Agent Memory entries, add with memory_manage (backup SOUL.md.bak-W83-N1-20260924_191528) | INSTALLER CONTENT, no code | e25b7c0; n1-notes-routing.txt |
| D-38 | user_profile_manage (owner P4) | author tool, in no default toolkit | added to [agent] tools (19; backup config.toml.bak-W83-P4-20260924_191802) | CHOICE (installer) | f898da4; p4-VV.txt |
Defect record D-35: SYMPTOM - the author's persona layer (SOUL/MEMORY/USER.md) never reaches the model on any tool-using agent;
the model does not know its name, its notes or the user. TRIGGER - any tool agent (all chat agents). FIX - forward the hook
(D-35) and construct the builder (D-36). EVIDENCE - "I am Jarvis, a helpful personal AI assistant" (SOUL text) after the fix.
Effects of D-36: with the hook set, the author _build_messages ignores the per-turn prompt the agent formats; the template is built
at startup with the same tool descriptions (8,609 chars measured). A system-prompt override is now read at startup, not per turn.
Still ONE system message (sysmerge unaffected). Only native_openhands is wired; other agents unchanged.
V&V results: W3 V4 undirected notes FAILED before N1 (model used memory_retrieve); after N1, undirected take -> memory_manage OK and
undirected list names both notes (framing awkward, memory_search called first). P4: undirected "what do you know about me" answers
from User Profile with no tool call. The live un-freeze was proven by the N1 SOUL edit taking effect with no restart.
Negative result: the W3 V3 cost comparison against 6237 is invalid - that baseline was measured with 116 memory.db docs injected;
after D-31 injection is far smaller (delta -811 is not a persona cost).
Plain language: we plugged in the author's machine that reads Jarvis its name tag, its diary and the card about you before every
conversation, and taught it (with one sentence in its name tag) that your notes live in its diary. It now knows its name, your
notes and your preferred name without being told which tool to use.

### G.6 W83 additions - Office documents, Phase 2 pulled forward (appended 2026-09-24, fifth package)
| ID | Area | Author (af21bc18) | Graystone | Class | Evidence / commit |
|---|---|---|---|---|---|
| D-39 | Phase 2 scope | RQ-023/027/032/033 deferred by owner 09/22 | OWNER RULING W83: Phase 2 pulled forward - MS Office is needed to test and tune the agent persona | SCOPE RULING | office-inventory.txt |
| D-40 | Office libraries | python-docx 1.2.0 is an AUTHOR dependency (pyproject.toml:43); no pptx/xlsx/COM code anywhere; no document tool in the 43-tool registry | python-pptx 1.0.2 + openpyxl 3.1.5 via `uv add --no-sync` (pyproject +2, uv.lock +49/-0) then `uv pip install` of the locked versions (+et-xmlfile 2.0.0, xlsxwriter 3.2.9); nothing removed | CHOICE (installer) | 685947b; office-s1-measure, office-s1 |
| D-41 | code_interpreter working dir | subprocess.run with no cwd | cwd = first file_write allowed dir (~\.openjarvis\workspace) | AUTHOR DEFECT, fixed | 5883f98; codecwd-patch, codecwd-VV |
| D-42 | code_interpreter fenced code | code run verbatim | strip one leading ``` fence line and a trailing fence BEFORE the blocklist check | AUTHOR DEFECT, fixed | 5a6735d; codefence-patch |
| D-43 | file_write relative paths | relative path resolved against the server cwd | anchored to the first allowed dir; absolute and ~ paths unchanged; confinement check still on the final path | AUTHOR x GRAYSTONE INTERACTION DEFECT, fixed | 5a6735d; fwanchor-patch, s3-failure-probe |
| D-44 | Persona office guidance | none | SOUL.md line: Office files via code_interpreter + python-docx/python-pptx/openpyxl, plain filename, workspace; file_write is plain text only (backup SOUL.md.bak-W83-F8-20260924_202629) | INSTALLER CONTENT | s3-rerun2 |
| D-45 | file_write Office guard | none | file_write refuses .docx/.pptx/.xlsx (any case) and steers to code_interpreter | CHOICE (owner F-11) | 0507c8c; fwoffice-patch, s3-rerun3 |
| D-46 | code_interpreter file report | returns stdout only; a script that saves a file and prints nothing returns "(no output)" | workspace top level snapshotted before and after the run; files created/changed listed FIRST in content (survives the 4000-char cut) and in metadata files[path, size_bytes] on TOOL_CALL_END (same shape file_write/file_read use) | AUTHOR DEFECT, fixed | c85fcf9; patch_codefiles, s3-rerun4 |
Defect record D-41: SYMPTOM - a document Jarvis creates by a plain filename lands in whatever folder the server was started from (the
repo root), mixed into git and hard to find. TRIGGER - any relative save inside code_interpreter. FIX - cwd set to the workspace.
Defect record D-42: SYMPTOM - "Execution error", the document is never made, the model falls back to pasting text. TRIGGER - the
model wraps its code in ```python fences (common). FIX - strip the fence lines before the security check (the blocklist still sees
the real code; a fenced os.system is still blocked, tested).
Defect record D-43: SYMPTOM - every file_write by the model fails with "Access denied ... outside allowed directories". TRIGGER - any
relative filename once allowed_dirs is set (Graystone W78 confinement) - the model never knows the absolute workspace path. FIX -
anchor relative names to the workspace; traversal (..\) and absolute outside paths are still denied (tested).
Assessment behind D-45 (owner): persona guidance alone (D-44) reached 4/6 and left false "I've created a Word document" claims
(text written into .docx names); a code guard makes it deterministic. Result 6/6, no false Office claims.
S3 family-request test (6 requests, machine-checked): baseline 0/6 real files -> after D-42/D-43 2/6 -> after D-44 4/6 (23/34
detail) -> after D-45 6/6 (33/34). Remaining: R3 formulas omitted in 2 of 3 runs (model detail-following); R2 false NEGATIVE (a
valid .docx made, then a shell_exec self-check was held by the confirmation gate, GATE_TIMEOUT 120s, and the reply said it failed).
Plain language: Jarvis can now make real Word, PowerPoint and Excel files for the family. We fixed four places where the author's
tools tripped over each other or over our safety fence, told Jarvis in its name tag which tool to use, and put a lock on the wrong
tool so it cannot pretend a text file is a Word document.
G.6 addendum (appended 2026-09-25, W88; D-46 made in W87):
Defect record D-46: AUTHOR INTENT - ToolResult content is what the model reads; metadata is the machine record on the author's
TOOL_CALL_END event (file_write/file_read already carry {path, size_bytes}). The author's code_interpreter returns stdout only.
SYMPTOM - a document is created but the reply says it failed, or the model detours to shell_exec to check and waits 120 s on the
confirmation gate (R2 false negative). TRIGGER - the model's script saves a file and prints nothing ("(no output)"). FIX - snapshot
the workspace top level before and after the run; list changed files FIRST in content and in metadata files[path, size_bytes].
LIMIT - workspace top level only; subfolders and absolute-path writes (G-1) are not listed (H-W83-28).
Result, S3 re-run 4 (s3_family_office_w87.py): files 5/6, replies honest 6/6 vs the filesystem, shell_exec 0, 32/40. R2 false
negative GONE. R1 = model code error (no pptx made anywhere). R3 formulas still omitted. RQ-032 criterion (6/6 real files AND 6/6
honest replies in ONE run) NOT MET - PARTIAL.
Plain language: after Jarvis runs its little program, it now looks in its own folder and says "these files are new", so it does
not have to guess whether it worked.

### G.7 W88 additions - trace system restored (appended 2026-09-25)
| ID | Area | Author (af21bc18) | Graystone | Class | Evidence / commit |
|---|---|---|---|---|---|
| D-47 | Trace system (src\openjarvis\traces) | full package: store.py (SQLite traces / trace_steps / FTS5, subscribe_to_bus), collector.py (wraps an agent run, records every inference, tool, memory and respond step), analyzer.py, __init__.py; TracesConfig enabled=True by default | restored BYTE-EXACT from af21bc18 (git hash-object = author blob, all 4 files); replaces a Graystone 18-line Rust-stub store.py and 1-line __init__.py (no collector, no analyzer, no subscribe_to_bus); the stub's traces.db (0 rows, incompatible schema) moved to evidence\W88\backup\tracesdb-ruststub-20260925_112010 | AUTHOR x GRAYSTONE INTERACTION DEFECT, fixed | 1d4b3ae4; probe_trace_restore_w88, vv_traces_w88, tb_since_start_w88, vv_orch_trace_w88 |
| D-48 | Trace test fixture (tests\traces\test_store_fts.py) | store fixture yields a TraceStore inside tempfile.TemporaryDirectory and never closes it | fixture closes the store in teardown (try/finally, s.close() - the author's own method); test code only | AUTHOR TEST DEFECT (Windows), fixed | W88 tests commit; patch_fts_fixture_w88, pytest tests/traces 52 passed |
Defect record D-47: AUTHOR INTENT - traces are the author's full interaction record and the input to the learning system
(traces\__init__.py: "Traces are the primary input to the learning system"). SYMPTOMS - traces.db stays empty (POAM-32);
no durable record of what a tool returned or why it failed (G-11); any JarvisSystem.ask() agent turn with traces enabled
raises ModuleNotFoundError: openjarvis.traces.collector (orchestrator.py:216-217, author code, byte-identical to af21bc18);
the server builds a store that silently never subscribes (app.py:240 AttributeError swallowed by the author's except/pass).
TRIGGER - two causes stacked: (1) the AUTHOR's .gitignore carries a bare `traces/` line (meant for trace output folders) that
also matches the source package src\openjarvis\traces\; Graystone's repo is not a clone (first commit f2fcb30, 2026-05-30,
built from copied files), so the package was left untracked from 05-30 to 08-05; (2) while untracked, the author's store was
replaced by a Graystone stub wrapping openjarvis_rust.TraceStore and the collector and analyzer were absent; commit 58c05e2
(08-05, "stop ignoring traces package source") then committed the stub as found. FIX - restore the four author files
byte-exact from af21bc18; move the stub's traces.db aside so the author's store creates its own schema. Config unchanged: no
[traces] section in config.toml, author default enabled=True applies (same effect as the author's shipped template).
NOT ESTABLISHED - when the stub replaced the author's store (git holds nothing before 08-05; the 05-30 Rust-extension work
is the likely context - inference only). The author's full history contains no RustTraceStore: the Python stub is Graystone's.
LIMIT - at af21bc18 the author wires the collector ONLY on JarvisSystem.ask() (QueryOrchestrator); the server chat route and
cli\ask.py record no trace. The author wired the chat endpoints later (upstream ef005703) - POAM-57. Details: SDD section 18.
Plain language: Jarvis came with a flight recorder that writes down every step of every job. When our copy of the project was
set up, a rule in the author's own file list hid the recorder's folder, and the part that does the recording went missing. We put
the author's recorder back exactly as written. It now records jobs run through Jarvis's main planner; the chat window is next.
G.7 addendum (W88, same day) - the cause is AUTHOR-DOCUMENTED: the author's CHANGELOG v1.0.2 (2026-05-24), fix #372, records
that the unanchored `traces/` .gitignore line made hatchling drop src/openjarvis/traces/ from the v1.0.1 PyPI wheel, so every
fresh install failed with ModuleNotFoundError: No module named 'openjarvis.traces' on the first jarvis ask, learning or server
call; the author anchored it to `/traces/`. Our baseline af21bc18 (2026-05-19) predates that fix. The same bare pattern also
matched tests/traces/, so the author's 7 trace test files were never in our repo (collision matrix: tests/traces/* = D on our
side). Most likely origin of the Rust stub - still inference, now supported by the author's record: the 05-30 Graystone setup
hit that ModuleNotFoundError and a stand-in was written to satisfy the import.
AUTHOR TESTS: tests/traces restored from af21bc18 (git checkout af21bc18 -- tests/traces, 7 files) and run with the author's
LOCKED test tooling (pytest 9.0.2, pytest-asyncio 1.3.0, pytest-cov 7.0.0 from uv.lock, installed with uv pip install; pyproject
and uv.lock unchanged; deps resolved coverage 7.16.1, iniconfig 2.3.0, pluggy 1.6.0). First run: 52 passed, 4 errors - all four
ERROR at teardown of TestFTS5Search tests that had PASSED. After D-48: 52 passed, 0 errors. Rollback of the tooling:
uv pip uninstall --python .venv\Scripts\python.exe pytest pytest-asyncio pytest-cov iniconfig pluggy coverage.
Defect record D-48: SYMPTOM - on Windows the 4 TestFTS5Search tests pass, then ERROR at teardown with PermissionError
[WinError 32] on the temp traces.db. TRIGGER - the store fixture yields a TraceStore inside tempfile.TemporaryDirectory and
never closes it; Windows cannot delete an open SQLite file (Linux and macOS can, so it passes in the author's usual lanes).
Still present upstream: the only author change to the file since the baseline is ruff formatting (928776a7). FIX - close the
store in the fixture teardown. Plain language: we ran the author's own checklist for the recorder and all 52 checks pass. One
check tripped over a Windows rule - you cannot throw away a file that is still open - so the check now closes the file first.

### G.8 W89 - skills: NO divergence (recorded 2026-09-25)
All 18 files in src\openjarvis\skills are byte-identical to af21bc18 (git hash-object = author blob). The startup warning
"Unmapped frontmatter field 'title' / 'dependencies' in skill 'research-paper-writing'" is the author's parser working as
designed (parser.py:196, tolerant pass) and is unchanged at upstream a6dcf846. No change made. Details: SDD section 19.

### G.9 W90-W92 divergence re-baseline to author a6dcf846 (appended 2026-09-26, W92)
Method: every row was decided with the author's intent, the options and the risks (owner rule 09/23). Evidence: SDD 20.8.
Row group "backend" (W90, full per-file text ARCHIVE-W83 s36): pyproject.toml author dynamic version (hatch-vcs), author
python range, KEPT Office and speech extras; core/config.py KEPT qwen3.5:9b fallback, STT compute_type auto, template port 8010
+ native_openhands; config.toml author loopback host, KEPT port 8010; cli/ask.py KEPT TerminalConfirmGate; cli/serve.py KEPT
Defect 6 live confirm callback, BIND_ASSERT, _build_agent_tools, memory backfill, W83 persona block; server/routes.py KEPT the
cloud bypass as one condition; agent_manager_routes KEPT ConfirmPolicy import; auth_middleware KEPT bind records; tools/_stubs
dispatch log + Defect 6 emit + ConfirmPolicy merged with the author's taint; code_interpreter KEPT fence strip before the
author's AST check; knowledge_sql author keyword check THEN our SQLite authorizer.
Row group "frontend and desktop" (W91-W92):
| Item | Author a6dcf846 | Graystone as built | Reason | Decision |
|---|---|---|---|---|
| Web CSP (tauri.conf) | connect-src http: https: ws: wss: | explicit allowlist incl. 172.16.33.200, ipc.localhost, media-src blob: data: | least privilege | OWNER OPTION B (W91) |
| App analytics calls | setup_completed, model_changed, app_opened | removed; analytics module left in main.tsx/store.ts, egress blocked by CSP | owner 09/22 analytics is dead code | OPTION B; POAM-71 |
| Backend port | 8000 | 8010 (lib.rs JARVIS_PORT, vite proxy) | 8000 held by iphlpsvc portproxy -> 172.21.134.21:8000 (measured W92) | required |
| lib.rs | full file | author file byte-for-byte except JARVIS_PORT 8010 | author SourceKind::Custom supports a remote Ollama natively (launch_ollama false, host written to config.toml); ~100 lines of our remote-mode Rust retired | W92-D3 |
| frontendDist + build:tauri | ../dist + vite build --outDir dist | ../../src/openjarvis/server/static + vite build | one delivery path for exe and backend (fixes two-path drift / white screen) | W92-D7 B |
| Desktop updater | active, endpoint open-jarvis desktop-latest | active false, endpoints [] | upstream binaries would replace the Graystone fork; updater runs in Rust outside the CSP | W92-D7 B; POAM-73 |
| Python interpreter | 3.10-3.13, .python-version git-ignored (line 103) | .python-version 3.12 tracked via labeled exception | inference layer requires 3.12; author boot sync could rebuild a venv on another interpreter | W92-D6 |
| STT stack lock | ctranslate2 4.7.1, av 16.1.0, onnxruntime 1.24.2 | ctranslate2 4.8.0, av 17.1.0 (= production), onnxruntime 1.24.2 | keep the proven decode path | W92-D5 P2; POAM-76 |
| ThinkingCircle | absent | removed | owner rebuilding later; author code supersedes | W92-D1 |
| Reconnect button, SetupScreen remote text | absent | removed (bc498a16 features) | author Disconnect flow and inference-source setup cover them | W92-D4; POAM-70 |
| InputArea | author component (Deep Research toggle, send path, toasts) | Graystone whole-file rewrite (useSpeechStream, attachments; send in ChatArea) | voice and attachments requirement | kept; gap POAM-69 |
| MessageBubble / ChatArea | isLive, ResearchTimeline, citations | author features restored + Graystone option buttons, attachment chips, TTS driver, probe, conversationId set on send | Option 1 extended by Method B | W92-D2 |
| sse.ts | top-level POST | fail-fast guard + single POST inside try with author authHeaders | avoids double POST (H-W91-4) | kept; POAM-72 |
| store updateLastAssistant | research traces/sources at 7-8 | same + persist at 9 | author positional contract kept | kept |
| confirmTool / ConfirmPrompt | absent | present (Defect 6 inbound), path-only apiFetch | confirmation gate | kept |
| useTauriApi fallback | author value | http://127.0.0.1:8010 | avoids localhost resolving to IPv6 | kept |
AUTHOR DEFECT AD-W92-1 (fixed 6c9a2bc3). SYMPTOM: tauri build aborts before compiling with "Found version mismatched Tauri
packages". CONDITIONS: author a6dcf846 ships package-lock with @tauri-apps/plugin-updater 2.11.0 and plugin-notification 2.4.0
but Cargo.lock with tauri-plugin-updater 2.10.1 and tauri-plugin-notification 2.3.3; the Tauri CLI requires matching
major.minor. Any build of the author's own tree fails the same way. FIX: cargo update -p tauri-plugin-notification (-> 2.4.0) and
cargo update -p tauri-plugin-updater --precise 2.11.0 (a plain update overshot to 2.12.0; a guard stopped the build); Cargo.lock
only, 2 crates moved, 155 unchanged. VERIFIED: the version gate passes and the release exe builds. Candidate upstream report.
OBSERVATION (not a defect): the author tracks frontend\tsconfig.tsbuildinfo, a build cache (POAM-75).
Upstream tags: the author's 235 release tags were fetched into local refs so hatch-vcs stamps the author's version
(1.0.5.dev...); they are never pushed (push.followTags unset; push commands never use --tags).

### G.10 W93 - confirmation callbacks at the author's executor sites (appended 2026-09-26, W93)
Method: every row decided with the author's intent, the options and the risks (owner rule 09/23); evidence SDD 20.9.
| Item | Author a6dcf846 | Graystone as built (upgrade da752fbd) | Reason | Decision |
|---|---|---|---|---|
| agent_manager_routes stream_tool_executor | lambda _prompt: True | ConfirmPolicy site=managed-agent-tool (verbatim from main) | attribution was Graystone W56; lost silently in the merge | restore (W93 A); real gate impossible on the event loop, POAM-80 |
| cli\ask.py skills pipeline_executor | lambda prompt: True | SkillPipelineConfirmGate (TerminalConfirmGate, site cli-ask-skill) | skill steps bypassed the terminal gate the agent uses; third-party skills (POAM-78) | real gate (W93 B, option 1) |
| cli\agent_cmd.py ask --yes (default) | lambda _prompt: True | ConfirmPolicy site=cli-agent-ask-yes, human_present=True | author-documented posture kept; attribution added | attribute only (W93 C); POAM-81 |
| cli\agent_cmd.py ask --no-yes, cli\skill_cmd.py run, cli\chat_cmd.py chat | click.confirm / input() prompt, no registry write | TerminalConfirmGate(site=cli-agent-ask / cli-skill-run / cli-chat) | Graystone three-way result contract: an unrecorded False is reported as TIMEOUT | fix (W93 D); integration defect, not an author defect in isolation; POAM-82 for main |
| cli\ask.py TerminalConfirmGate | absent | optional site= keyword, default cli-ask | one class, per-site attribution | W93 D |
