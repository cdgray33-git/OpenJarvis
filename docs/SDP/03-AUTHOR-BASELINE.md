# VOL 3A - AUTHOR BASELINE AND GRAYSTONE DIVERGENCE REGISTER
v0.2 W76 2026-09-22 (v0.1 same day). Owner rule 09/22: the author's procedures come first.
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
| D-03 | Engine host | [engine.ollama] host | no [engine.ollama] section; remote Ollama 172.16.33.200 | OPEN | source of host not yet measured |
| D-04 | Storage section | [tools.storage] | legacy [memory] | LAG | backward compatible |
| D-05 | Default agent | simple / server orchestrator | native_openhands (both) | CHOICE | CodeAct agent |
| D-06 | Default tools | none (zero tools) | code_interpreter, file_read, file_write, shell_exec, think, calculator, retrieval, 5 mailbox tools incl move_to_trash, empty_folder | CHOICE | destructive set, see H-W76-EXPOSURE |
| D-07 | Server bind and auth | 127.0.0.1:8000; API key before 0.0.0.0 | 0.0.0.0:8010; no [server.auth] section; OPENJARVIS_API_KEY unmeasured | CHOICE/OPEN | author auth may postdate base; H-W74-AUTHOFF |
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
