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
