# SDP SOURCE EXTRACT W82 part 9 (deduplicated by section hash)
### [ARCHIVE-W71-2026-09-21.md] W71 - REPOSITORY AND PATH CASE (infrastructure)
Windows NTFS is case-insensitive; git with core.ignorecase=true tolerates
case differences in the working tree but matches pathspecs literally. So a
command can open the file fine and git can still say "nothing to do".
Plain language: the house has one front door, but the mail carrier only
delivers if the name on the envelope is spelled with the exact capitals.
Rollback .bak-* files are git-ignored (.gitignore:20) and live only on disk.
### [ARCHIVE-W71-2026-09-21.md] W71 - SDP CONFORMANCE GAP AND THE PLAN (Gray's ruling pending)
Target structure (MIL-STD-498 DIDs, still cited on contracts; successors IEEE
1016, ISO/IEC/IEEE 12207/15288): SSDD DI-IPSC-81432, SRS -81433, IRS -81434,
SDD -81435, IDD -81436, DBDD -81437; plus RTM, STP/STD/STR, SVD.
Architecture views (DoDAF): OV-1, SV-1, SV-4, SV-6 (data exchange = ports/
protocols/encoding), SV-10c (event trace = end-to-end flow per execution path).
Security package (RMF, NIST SP 800-37 / 800-53, DoDI 8510.01): SSP (SP 800-18)
with boundary, data flows, PPSM (DoDI 8551.01); SAR; POA&M; Contingency Plan
(SP 800-34); AU audit/logging; CM Plan.
Missing today: DID outline, RTM, ICD tables, SVD, CM baseline (author vs
Graystone divergence list), POA&M, contingency (rollback points are local only).
Plan: (1) SDP skeleton with fixed chapters, Gray approves outline; (2) coverage
matrix, components/paths x chapters, empty cells = gaps; (3) harvest W1-W71
archives by 550B self-posting bundle into chapter slots; (4) definition of done
for any fix = SV-10c flow + ICD row + CM entry + RTM status + test evidence.
Plain language: a notebook says what we did each day; a design package says
what the machine is, room by room, so a missing room is obvious.
### [ARCHIVE-W71-2026-09-21.md] CODE MAP - AGENT STREAMING PATH (CARRY EVERY WINDOW; Gray 09/21)
WHO IS THE AGENT: NativeOpenHandsAgent, src\openjarvis\agents\native_openhands.py
(660 lines). Selected when the chat dropdown names an agent -> PATH 1b.
Base agent contract: src\openjarvis\agents\_stubs.py (358).
THE BUFFER: NativeOpenHandsAgent.run() finishes each turn before returning;
src\openjarvis\server\stream_bridge.py (368) then replays the finished text.
Documented as early as 08/23 in the execution path register (routes.py
:143-146 comment: bridge runs agent.run() synchronously and word-splits).
ENGINE STACK (stream_full defined 7 times):
  contract   engine\_stubs.py:90 (129)
  backends   engine\ollama.py:238 (538), engine\_openai_compat.py:158 (248),
             engine\cloud.py:1374
  wrappers   engine\multi.py:117 (141), telemetry\instrumented_engine.py:478
             (507), security\guardrails.py:263 (317)
EVENTS: src\openjarvis\core\events.py (201).
FRONTEND: frontend\src\components\Chat\ChatArea.tsx (542, capital-C Chat in git)
          frontend\src\audio\ttsPlayer.ts (377).
Plain language: the agent is a helper who writes the whole letter before
handing any of it over; the bridge then reads the letter aloud fast. Option A
makes the helper hand over each word as it is written.
### [ARCHIVE-W71-2026-09-21.md] s8 DELTAS TO THE CARRIED REGISTERS
**DIAGNOSTIC TOOLING - DELTA:**
  - Main-thread liveness probe in `ChatArea.tsx` - INSTALLED, READABLE.
    Setup in s6. Satisfies W69's "NEW REQUIRED INSTRUMENT".
  - `tools\stream_probe_w70.py` - backend SSE timing probe. READABLE.
    Setup in s6. The standing instrument for any streaming question:
    re-run it after Option A lands; success is the agent case reporting
    first delta near 0.5 s, not 34 s.
  - Logs: `Downloads\stream-probe-w70.log`,
    `Downloads\stream-probe-w70-after.log`, `Downloads\build-w70.log`.
**LOGGING TOPOLOGY - DELTA:**
  - No new logger trees. Instruments this window deliberately bypass
    logging: one renders into the UI, one writes to stdout.
**EXECUTION PATHS - DELTA:**
  - **Agent chat path fully specified with emission timing** - s6, seven
    gates. Supersedes W69's send-path note: the `lastFlush` question is
    ANSWERED (used, on `updateLastAssistant` only, `:268`).
  - **Managed-agent path (`_stream_managed_agent`) confirmed NOT the chat
    path** at any point in history. It does real `stream_full` with
    multi-turn tools (`agent_manager_routes.py:630`, `:1101`, `:1335`) -
    useful reference for Option A.
  - **No-agent path streams correctly** - measured, code unread.
  - No human confirmation gate on the chat paths. Bus traffic on the agent
    path: the five mapped EventTypes, forwarded as named SSE events.
W71 deltas:
- TOOLING/PATHS: ChatArea.tsx git path is frontend/src/components/Chat/ChatArea.tsx.
- COMMITS: 63257bd = W70 fixup, liveness probe now in both remotes.
- CODE MAP section added to s6; MUST be carried verbatim into every future archive s6 and named in every BRIEF.
- CM: native_openhands = Graystone-chosen, author install skipped. engine\_stubs.py (May) is the live base class.
- OPEN: synthesize route query (F-W71-VOICE-LATE, H-W71-SYNCIO test) not yet run.
- SDP: docs\SDP\ v0.1 created; all future deltas go into SDP volumes first.
### [ARCHIVE-W72-2026-09-21.md] Select-String -Path ARCHIVE-W72-2026-09-21.md -Pattern '^## s<N> ' ; then read that section only.
Registers chain: ARCHIVE-W57 (root) + W61-W71 + this file. W72 appends DELTAS only (s7-s10).
### [ARCHIVE-W72-2026-09-21.md] s0 INDEX
s1 Window narrative | s2 Evidence (measurements) | s3 Negative results
s4 Hazards and defects | s5 Corrections and clarifications from Gray
s6 SDD/SDP feed | s7 Execution paths DELTA | s8 Diagnostic tooling DELTA
s9 Logging topology DELTA | s10 Rules of engagement DELTA | s11 Program goal movement
s12 550B carry | s13 AUTHOR-INTENT-W72-A | s14 AUTHOR-INTENT-W72-B
s15 AUTHOR-INTENT-W72-C | s16 AUTHOR-CODE-W72-D-NOTES | s17 ROADMAP v0.1
### [ARCHIVE-W72-2026-09-21.md] s2 EVIDENCE (all [M], W72 exchange 11)
- Port 8010 LISTEN 127.0.0.1, pid 17884, python.exe at
  C:\Users\Admin\AppData\Local\Programs\Python\Python312\python.exe.
- .venv\pyvenv.cfg: home Python312, CPython 3.12.10, uv 0.11.11.
- wsl -l -v: Ubuntu, Stopped, version 2.
- load_config (win32, CONFIG_DIR C:\Users\Admin\.openjarvis): agent.default_agent and
  server.agent = native_openhands; max_turns 15; agent.tools includes mailbox_list_accounts,
  mailbox_usage_report, mailbox_find_messages, mailbox_move_to_trash, mailbox_empty_folder;
  intelligence.default_model qwen3-coder:30b, max_tokens 1024; scheduler.enabled false;
  agent_manager.enabled true; operators.enabled false; traces.enabled true;
  security: enforce_tool_confirmation true, mode warn, merkle_audit true,
  local_tool_bypass false, profile personal.
- agents.db 524288 bytes: managed_agents 8, agent_tasks 0, channel_bindings 0,
  agent_checkpoints 0, agent_messages 901, agent_learning_log 14.
  Cody-Coder monitor_operative ERROR 783 runs interval 3600; Cody-Builder ERROR 83 runs
  cron 0 9 * * *; Cody idle 9; Nova (inbox_triager tools) 0; Oryan paused 1;
  Oracle 0; My Assistant archived 2; W54-ToolkitTest archived 0.
- scheduler.db MISSING. traces.db 12288 bytes, traces 0. No user operators/templates dir.
### [ARCHIVE-W72-2026-09-21.md] s3 NEGATIVE RESULTS (what things turned out NOT to be)
- The author guides were NOT missing from our tree (found by git ls-files).
- The author has NO user docs for Operators or the persistent-agent layer (filter over
  docs/ and configs/ returned nothing beyond files already read). Intent lives in code.
- The CLI reference does NOT document agents/scheduler/digest/connect/doctor.
- Graystone's managed-agent routes are NOT a rebuild: agent_manager_routes.py is the file
  behind the author's /v1/managed-agents API (existence [M], identity [R]).
- The running backend is NOT the WSL2 build (s2).
- The Operators/TaskScheduler half has NEVER run (scheduler.db absent).
- No `agent_executor` file exists; the executor is agents/executor.py.
- Batch D bundle did NOT include agent_manager_routes.py (possibly read in W71; left out
  per the ask-first rule).
### [ARCHIVE-W72-2026-09-21.md] s4 HAZARDS AND DEFECTS (found by read; not patched - development is stopped)
- H-W72-WINKILL: cli/daemon_cmd.py uses os.kill(pid, 0); on Windows that is
  TerminateProcess. `jarvis start|stop|status` from the Windows venv would kill the
  server; signal.SIGKILL absent on Windows. LIVE on this box per s2. Never run them.
- D-W72-OPLOGS: `jarvis operators logs` calls store.get_runs(); store has get_run_logs().
- D-W72-CKPT: AgentExecutor never calls save_checkpoint; confirmed [M] (0 checkpoints
  after ~878 ticks). `jarvis agents recover` restores nothing.
- D-W72-TRACES: traces enabled, 0 traces after ~878 ticks. Cause unmeasured.
- D-W72-EPHEM: AgentExecutor.run_ephemeral omits the model argument.
- Executor tool construction: ToolRegistry.get(name)() with no args; deps injected only
  for llm / retrieval / memory_* / channel_*. Custom mailbox tools get none.
- Executor imports _ensure_registries_populated from server/agent_manager_routes.py.
- daemon/gateway.py GatewayDaemon is a stub.
- Scheduler cron is UTC; without croniter only "M H * * *" is honored.
### [ARCHIVE-W72-2026-09-21.md] s6 SDD/SDP FEED
- New chapter needed: the two autonomy subsystems (managed agents: AgentManager +
  AgentExecutor + agent scheduler + agents.db; operators: OperatorManager +
  TaskScheduler + scheduler.db), their shared bus, and their stores.
- Managed-agent tick flow, gate by gate, is in s16 section 2 (plain-language version
  still to be written per the 09/02 rule).
- Divergence register: D1 native Windows [M]; D2 port 8010 vs 8000 [M]; D3 agent
  native_openhands vs orchestrator [M]; D4 local Kokoro vs cloud TTS; D5 Yahoo IMAP (no
  author connector); D6 operators never run [M].
- Verification source candidate for the RTM: author Agent QA Runbook (37 scenarios).
### [ARCHIVE-W72-2026-09-21.md] s7 EXECUTION PATHS DELTA
- NEW P-MA-TICK (managed-agent tick): entry = agent scheduler (interval/cron) OR
  `jarvis agents run|ask` OR server /run route. Chain = AgentExecutor.execute_tick ->
  _run_with_retries -> _invoke_agent -> AgentRegistry.get(agent_type)(engine, model,
  tools=...) -> agent.run(input, context). ToolExecutor: built inside the agent from
  instances created in _invoke_agent (no-arg construction). Confirmation gate: NOT
  MEASURED on this path. Bus: AGENT_TICK_START/END/ERROR, AGENT_BUDGET_EXCEEDED on the
  executor's bus; subscribes to TOOL_CALL_START/END, INFERENCE_START. Human present:
  NO for scheduled ticks; YES for CLI ask/run. file:line not yet recorded.
- NEW P-OP-TICK (operator tick): entry = TaskScheduler poll (60 s) -> _execute_task ->
  system.ask(prompt, agent="operative", tools, system_prompt, operator_id). NEVER RUN
  on this box (s2). Bus: string events scheduler_task_start/end.
### [ARCHIVE-W72-2026-09-21.md] s8 DIAGNOSTIC TOOLING DELTA
- w72_measure.py: written to %TEMP% by a here-string; run with .\.venv\Scripts\python.exe.
  Read-only (sqlite mode=ro). Prints effective config sections, db table counts, managed
  agents (tools/schedule only, no credentials), scheduler tasks. Output: console.
- Bundler one-liner pattern (git paths -> single .md with FILE headers and line counts);
  outputs AUTHOR-GUIDES-W72-A/B/C.md and AUTHOR-CODE-W72-D.md in repo root, NOT in git.
### [ARCHIVE-W72-2026-09-21.md] s9 LOGGING TOPOLOGY DELTA
- agents/executor.py, agents/manager.py, operators/manager.py, scheduler/scheduler.py
  each use logging.getLogger(__name__) (read). Landing file not measured this window.
### [ARCHIVE-W72-2026-09-21.md] s10 RULES OF ENGAGEMENT DELTA
- Docs are author INTENT [R]; code and runtime are [M]. Never grade a docs claim [M].
- Never run `jarvis start|stop|status` from the Windows venv (H-W72-WINKILL).
- Build the handoff scaffold in exchange 1 (missed in W72).
### [ARCHIVE-W72-2026-09-21.md] 2. AUTHOR'S AGENT ORCHESTRATION (what was never set up here)
- Two query modes: DIRECT (one inference, no tools) and AGENT (named agent, tool loop).
- Author guidance: pick the simplest agent. `orchestrator` is THE DEFAULT for tool use
  (native OpenAI function-calling loop, max_turns 10). `[server] agent = "orchestrator"`
  is the documented server default.
- `native_openhands` is intended for CODE GENERATION + EXECUTION (CodeAct: parses
  ```python blocks and text Action:/Action Input:), default max_turns 3. It is NOT the
  author's choice for general or executive tasks. Graystone chose it (W71 hard fact).
- The author's executive-assistant shape is OPERATORS: "OpenJarvis's key differentiator".
  Chain: OperatorManager -> TaskScheduler -> AgentExecutor -> OperativeAgent. Persistent,
  scheduled, stateful (session store + memory-backend state between ticks). Operator
  TOML manifests. Roadmap calls it solid but not yet hardened for long-horizon autonomy.
- Presets map directly to Gray's goal: morning-digest (email, calendar, health, news,
  spoken via TTS), scheduled-monitor (operative on cron), deep-research, code-assistant.
  `jarvis connect gdrive` = one OAuth for Gmail, Calendar, Tasks.
- ToolExecutor contract: lookup -> parse JSON args -> TOOL_CALL_START -> execute ->
  TOOL_CALL_END. Inference events come from InstrumentedEngine, not agents.
- Managed Agent streaming (/v1/managed-agents/{id}/messages, stream:true) is documented
  as calling engine.stream_full(), accumulating tool-call fragments, executing tools on
  finish_reason="tool_calls", emitting `event: tool_result`, looping to max_turns.
- Sandbox: SandboxedAgent runs any agent in Docker/Podman, --network none, mount
  allowlist with blocked patterns (.ssh, .env, *.pem, *.key).
- Security defaults: [security] enabled, mode "warn", scan_input/scan_output true,
  enforce_tool_confirmation = TRUE.
### [ARCHIVE-W72-2026-09-21.md] 3. AUTHOR'S OWN ROADMAP (what the author says is NOT done)
- Operators: health/heartbeat, manifest metrics, capability enforcement, rate limits
  (Ready); chaining, event-driven, versioning (Design Needed).
- Redaction-before-cloud pipeline: Ready, i.e. NOT BUILT by the author.
- Voice interface over channels: Research-Stage.
- Per-platform install guides incl. "Windows + Ollama": Ready, i.e. NOT WRITTEN.
- Channels shipped: SendBlue (iMessage/SMS), Slack, Desktop/Browser. WhatsApp blocked.
### [ARCHIVE-W72-2026-09-21.md] 4. CURIOSITIES - ONE LINE EACH, NOT TRACED
- C1 enforce_tool_confirmation defaults TRUE; relates to Defect 6 `_confirm_callback = None`.
- C2 Author's managed-agent stream already describes Option A's shape; compare before building.
- C3 instrumented_generate publishes TELEMETRY_RECORD; relates to H-W71-TELEM.
- C4 Redaction-before-cloud unbuilt upstream; relates to H-W71-GUARD.
- C5 Docs drift: [agent] default_agent list omits native_openhands; quickstart lists a
  `custom` agent found nowhere else; overview says 9 agents, index says 7.
- C6 Rust extension build status on Graystone unknown.
- C7 Cloud quick-path: OpenRouter > Anthropic > OpenAI > Google precedence; relates to
  Gray's note that cloud-model communication may be broken.
- C8 Pearl/mining design docs in tree; unrelated to goal.
- C9 hybrid/README points at a CLAUDE.md "full recipe"; check whether it is in tree.
### [ARCHIVE-W72-2026-09-21.md] 5. SDP FEED
- Baseline definition for divergence register: author target = Linux/macOS/WSL2,
  port 8000, orchestrator default, operators for autonomy, presets via `jarvis init`.
- Graystone divergences observed so far: native Windows backend, port 8010,
  NativeOpenHandsAgent as the agent, author install never run.
### [ARCHIVE-W72-2026-09-21.md] 1. PLATFORM - NOW EXPLICIT
- wsl2.md, verbatim sense: OpenJarvis runs in WSL2 on Windows; NATIVE WINDOWS IS NOT
  SUPPORTED. Graystone runs the backend natively on Windows. This is the single largest
  divergence from the author baseline.
- Deployment targets: Docker (recommended for production), systemd, launchd, API server.
- Production guidance: bind 127.0.0.1, put TLS/auth at a reverse proxy (Nginx/Caddy),
  proxy_buffering off for SSE. Server has NO built-in auth.
### [ARCHIVE-W72-2026-09-21.md] 5. SECURITY
- GuardrailsEngine is "composable, not mandatory": must be WRAPPED explicitly around
  an engine. Modes warn/redact/block. AuditLogger -> audit.db (append-only).
- Docs say streaming scans INPUT before the stream and output post-hoc only.
- ToolSpec.requires_confirmation per tool + [security] enforce_tool_confirmation.
- FileReadTool always refuses sensitive files (.env, *.pem, id_rsa, ...).
- PIIScanner ignores RFC1918 IPs by design.
### [ARCHIVE-W72-2026-09-21.md] 6. TOOLS AND CONNECTORS
- 23 built-in tools listed (code, search, file, http w/ SSRF protection, memory x5,
  llm, channel x3, scheduler x5, mcp_adapter).
- Connectors: gmail_imap (app password), Outlook IMAP (Inbox only), gdrive/gcalendar/
  gcontacts OAuth (redirect localhost:8789), Slack, Notion, Granola, Obsidian, Dropbox,
  Apple Notes/iMessage (macOS). NO YAHOO CONNECTOR: Graystone's Yahoo IMAP is original.
- Credentials at ~/.openjarvis/connectors/*.json, 0600.
### [ARCHIVE-W72-2026-09-21.md] 8. CURIOSITIES - ONE LINE EACH, NOT TRACED
- C10 api-server doc: agent serves non-streaming only. Matches W71's measurement that
  no-agent chat streams and the agent path is buffered. Author-documented, not a bug?
- C11 Docs say guardrails stream scans input first; W71 H-W71-GUARD found our
  stream_full skips input redaction. Compare code to author intent.
- C12 Graystone "managed-agent" routes vs author `jarvis agents` layer: same system or
  a rebuild? Measure before building anything agentic.
- C13 inbox_triager template may already implement mailbox triage.
- C14 Scheduler UTC vs Gray's local time for any briefing schedule.
- C15 CLAUDE.md referenced by hybrid README is absent from our tree.
### [ARCHIVE-W72-2026-09-21.md] 9. SDP FEED - DIVERGENCE REGISTER ADDITIONS
- D1 Native Windows backend (author: not supported). D2 port 8010 (author 8000).
- D3 NativeOpenHandsAgent as the agent (author: orchestrator / operative / templates).
- D4 Local Kokoro TTS (author: Cartesia/OpenAI cloud). D5 Yahoo IMAP (no author connector).
- D6 Persistent-agent layer status on Graystone: UNKNOWN - to be measured.
### [ARCHIVE-W72-2026-09-21.md] s15 AUTHOR-INTENT-W72-C
# AUTHOR INTENT - W72 BATCH C (6 files, 2272 lines, read whole)
Source: AUTHOR-GUIDES-W72-C.md. Grade [R] (CM-01).
NEGATIVE RESULT: the git ls-files filter for docs/ or configs/ paths containing
operator|agent|template returned NOTHING beyond what was already read. The author has
NO user documentation for Operators or the persistent-agent layer. It exists only in
the QA runbook (Batch B) and, per the messaging-hub tutorial, as CODE:
`src/openjarvis/recipes/data/operators/` ("ready-made examples").
### [ARCHIVE-W72-2026-09-21.md] 1. CLI REFERENCE
- Documents: init, ask, model, pearl, memory, telemetry, bench, channel, serve.
- Does NOT document `jarvis agents ...`, `jarvis scheduler`, `jarvis digest`,
  `jarvis connect`, `jarvis doctor`, `jarvis add`. Docs drift: CLI ref is stale.
- serve: agent applies to NON-STREAMING requests only; tool-capable agents
  (orchestrator, react, openhands) get ALL registered tools automatically.
- init detects Platform incl. Windows (hardware detect only; install still WSL2).
### [ARCHIVE-W72-2026-09-21.md] 2. PYTHON SDK
- Jarvis(config, config_path, engine_key, model); ask / ask_full / memory / close.
- SDK-documented agents: simple, orchestrator, operative, monitor_operative.
### [ARCHIVE-W72-2026-09-21.md] 3. MEMORY
- SQLite/FTS5 default and the ONLY persistent backend. FAISS, ColBERT, BM25 are
  in-memory (lost on restart). Hybrid = RRF of sparse + dense.
- Context injection: top_k 5, min_score 0.1, max_context_tokens 2048, system message
  prepended with [Source: ...] attribution.
- Canonical import path is openjarvis.tools.storage.* (memory.* are shims).
### [ARCHIVE-W72-2026-09-21.md] 4. MCP EXTERNAL SERVERS
- [tools.mcp] servers = JSON STRING (not TOML array). Streamable HTTP (url) or stdio
  (command). include_tools / exclude_tools filters. 10 s connect, 60 s request timeout.
  One failed server never blocks others. This is the author's path to wire external
  lab services as agent tools without writing tool code.
### [ARCHIVE-W72-2026-09-21.md] 7. CURIOSITIES - ONE LINE EACH, NOT TRACED
- C16 Operator recipes live in src/openjarvis/recipes/data/operators/ - read before
  designing any agent. Author resource first.
- C17 EmailChannel (SMTP/IMAP) could be the author-intended carrier for Yahoo mail.
- C18 Recipe TOMLs (load_recipe) are a declarative agent-config mechanism we may not use.
- C19 memory_store/memory_search tools are the author's persistent-memory recall path;
  relates to the unfinished recall work in the program-goals file.
### [ARCHIVE-W72-2026-09-21.md] 2. HOW A MANAGED-AGENT TICK WORKS (executor, gate by gate)
1 start_tick (DB status=running guard) -> 2 AGENT_TICK_START on bus -> 3 resolve
agent class from AgentRegistry, engine+model from JarvisSystem -> 4 optional router
policy -> 5 tools: ToolRegistry.get(name)() with NO constructor args, deps injected ONLY
for llm / retrieval / memory_* / channel_* -> 6 input = date + standing instruction +
summary_memory (2000 chars) + pending queued messages (marked delivered) -> 7 optional
memory context prepended -> 8 agent.run(); if empty content, run ONCE more -> 9 retries
x3 on retryable errors -> 10 finalize: runs++, tokens/cost, summary_memory = first 2000
chars of reply, store response, budget check -> 11 AGENT_TICK_END / ERROR -> 12 trace.
### [ARCHIVE-W72-2026-09-21.md] 5. HAZARDS / DEFECTS FOUND BY READ (not measured, not traced)
- H-W72-WINKILL: cli/daemon_cmd.py `jarvis start|stop|status` uses os.kill(pid, 0) as a
  liveness probe. On Windows, os.kill with any signal other than CTRL events calls
  TerminateProcess: `jarvis status` would KILL the running server. signal.SIGKILL does
  not exist on Windows. DO NOT RUN these commands on the Windows box.
- D-W72-OPLOGS: `jarvis operators logs` calls store.get_runs(); SchedulerStore defines
  get_run_logs(). AttributeError, caught and printed. Author defect.
- D-W72-CKPT: AgentExecutor never calls save_checkpoint, so `jarvis agents recover` and
  `logs` have no checkpoints unless another caller (routes?) writes them.
- D-W72-EPHEM: run_ephemeral constructs agent_cls(engine=..., system_prompt=...) with no
  model argument; BaseAgent requires model.
- daemon/gateway.py GatewayDaemon is a stub (start() only sets a flag).
- Executor imports _ensure_registries_populated FROM server/agent_manager_routes.py:
  the executor depends on the server module.
- `jarvis agents watch` subscribes to the process-local get_event_bus(); relates to the
  known two-bus split ([[openjarvis-event-bus]]).
- Scheduler: cron in UTC; without croniter only "M H * * *" is honored, anything else
  falls back to +1 hour. Scheduler thread only runs inside a process that started it.
### [ARCHIVE-W72-2026-09-21.md] 6. SDP FEED
- Two autonomy subsystems, two stores, one bus: needs its own SDD chapter and two
  execution-path entries (managed-agent tick; operator tick).
### [ARCHIVE-W72-2026-09-21.md] D. TRACK 2 - SDP RESTRUCTURE (ATO-led; follows Track 1)
- [ ] R2.1 Restructure SDP v0.1 to MIL-STD-498 DIDs + RMF package; RTM is the spine.
- [ ] R2.2 Divergence register D1-D6 with evidence grades (D1 now [M]).
- [ ] R2.3 SDD chapter: two autonomy subsystems, stores, bus; execution-path entries for
      managed-agent tick and operator tick (gate by gate, plain language + technical).
### [ARCHIVE-W72-2026-09-21.md] E. TRACK 3 - AGENT LAYER (measure first, then decide)
- [ ] R3.1 Why are Cody-Coder and Cody-Builder in ERROR? Read their summary_memory
      (executor writes "ERROR: ..." there) - read-only measurement.
- [ ] R3.2 Why 0 traces on ~878 ticks (M5)? Is trace_store None on the managed path?
- [ ] R3.3 Decide the executive-assistant agent type with evidence: author intends
      orchestrator / operative / monitor_operative; Graystone runs native_openhands.
- [ ] R3.4 Managed-agent tool construction gives custom tools no dependencies
      (executor step 5). Measure whether mailbox_* tools work on the managed path.
- [ ] R3.5 Nova (inbox_triager) has no mailbox tool; decide author-path wiring
      (EmailChannel vs mailbox tools) for Yahoo triage.
- [ ] R3.6 Operators: decide whether to enable [scheduler]/[operators] at all.
### [ARCHIVE-W72-2026-09-21.md] G. STANDING HAZARDS AND AUTHOR DEFECTS (read, not traced)
- H-W72-WINKILL  never run `jarvis start|stop|status` from the Windows venv (M1 makes it live).
- D-W72-OPLOGS   `jarvis operators logs` calls a missing store method.
- D-W72-CKPT     executor never writes checkpoints ([M] via M6).
- D-W72-EPHEM    run_ephemeral omits the model argument.
- C10            server agent serves NON-streaming only (matches W71 buffered agent path).
### [ARCHIVE-W73-2026-09-21.md] s0 INDEX
s1 narrative | s2 evidence | s3 negative results | s4 hazards/defects | s5 corrections
s6 SDD/SDP feed | s14 unused/orphaned code register | s7-s12 CARRIED from ARCHIVE-W72 + W73 deltas | s13 roadmap (carried + deltas)
### [ARCHIVE-W73-2026-09-21.md] s1 WINDOW NARRATIVE
 Subject R0.5 provenance. git history starts at Graystone root f2fcb30
(2026-05-30, 2000 files); no upstream remote and no author commits in our history, so git
alone could not name the base. Gray confirmed source = github.com/open-jarvis/OpenJarvis.
Cloned upstream to C:\Users\Admin\upstream-OpenJarvis (outside repo, never pushed), fetched
our HEAD into it, and scored every upstream commit <= 2026-06-01 (696 + ~110) by count of
files differing from f2fcb30. Minimum found and verified with --no-renames. Produced the HEAD-vs-
base change list (591 rows), classified it, and built the ATO unused/orphaned code register (s14)
at Gray's direction. Explained all 12 author files absent at HEAD; traced the trace-recorder loss
to an inherited unanchored gitignore pattern. Then measured WSL2 (R0.4): author-shape runtime data
from 05-26..05-28 exists; /opt and the tarball are not the code; WSL traces also 0. No code changed.
### [ARCHIVE-W73-2026-09-21.md] s3 NEGATIVE RESULTS (what things turned out NOT to be)
- N1 git history is NOT a record of the author baseline: root commit already mixes author + Graystone.
- N2 The base is NOT the root commit date (05-30): best match is 11 days earlier (05-19).
- N3 NOT the v1.0.1 release tag exactly (129 vs 127) - it is main one day after.
- N4 Rename detection did NOT change the ranking (127 with and without renames).
- N5 My exchange-4 note was WRONG: upstream native-Windows support (#432/#433/#436/#438/#445,
  05-29..05-30) is NEWER than our base, so our tree predates it. wsl2.md in our tree is
  accurate for our base: we run native Windows on a base the author did not support then.
- N6 E7 was WRONG: "no commits 06-21..09-21" was read off TRUNCATED output (first 15 + HEAD only).
  58c05e2 on 2026-08-05 disproves it. Lesson: never state a gap from a Select-Object -First N view.
- N7 The traces files were NOT deleted by Graystone and NOT an uninstalled author component
  (Gray's first read): they are author source lost at import via the inherited gitignore pattern.
- N8 No OTHER author file was lost: the D list (12) is the complete set of author files absent
  at HEAD, and all 12 are now explained (E10, E13).
- N10 First WSL probe measured NOTHING: Windows PowerShell stripped embedded double quotes passing
  the script to wsl.exe -> bash syntax error. Fixed by base64-encoding the script (no quotes to strip).
- N11 Gray's report CONFIRMED in part: an author-shape install WAS stood up in WSL2 (05-26..05-28),
  then the running system moved to native Windows. Not yet known: /opt/openjarvis revision.
- N12 The WSL traces.db WAL did NOT hold traces: 0 rows (E17). The 49 KB WAL was schema/FTS init.
- N13 The WSL install ALSO recorded 0 traces, so the missing collector (H-W73-TRACELOST) is a real
  defect but is NOT proven to be the sole cause of M5. Trace recording may also need a path or
  setting that neither install exercised. Downgraded from "leading explanation" to "necessary fix".
- N14 /opt/openjarvis is NOT an install and the tarball is NOT the import source (E15, E16).
  WSL code location remains UNKNOWN (no git repo under ~ depth 3 or /opt; possibly pip/uv tool).
- N15 Downloads naming: repeat downloads of one name became "(1)(2)(3)"; stale copies removed
  after a hash match proved (3) == E15. Interim downloads now carry -E<exchange>.
- N9 Instrument defect caught: PowerShell -match is case-insensitive; qwen_* hit the QWEN_ rule.
  Fixed with -cmatch; counts in E8 are the corrected ones.
### [ARCHIVE-W73-2026-09-21.md] s4 HAZARDS AND DEFECTS
- H-W73-TRACELOST [M absence, R consequence]: TraceCollector/TraceAnalyzer source missing on disk
  while 4 system modules import it. Strong candidate cause of M5 / R3.2 (traces.db 0 traces).
  Fix = restore both files + tests from upstream af21bc18. HELD: development stopped. (Was TRACEDEL.)
  N13: WSL install also shows 0 traces - fix is necessary, not proven sufficient.
- H-W73-WIKIINPKG: Engineering_Wiki lives inside the author package dir src/openjarvis/traces/.
- H-W73-BEHIND: base predates upstream security fixes merged 05-25: #415 template-loader RCE
  (eval + shell=True), #416 WebSocket/A2A auth, #417 default deploy auth; plus ~550 later PRs
  incl. #418 managed-agent streaming parity, #407 monitor_operative repair, #454/#460 tool
  requests bypass agent (relates to W71 buffered path). ATO vulnerability-register input.
- H-W73-REPOHYGIENE: backups, build logs, applied patchers and mailbox one-shots are tracked in
  git; one file name contains a space ("patch_testexec_v1 .py"). Classify before any cleanup.
### [ARCHIVE-W73-2026-09-21.md] s5 CORRECTIONS AND CLARIFICATIONS FROM GRAY
- Source repo confirmed by Gray: github.com/open-jarvis/OpenJarvis.
- Gray: capture EVERY true route and EVERY dead end; the SDP must explain unused code for an
  ATO auditor. -> new register s14 (Unused / Orphaned Code Register) with disposition per file.
### [ARCHIVE-W73-2026-09-21.md] s6 SDD/SDP FEED
- PROVENANCE INSTRUMENT (setup + flow, plain language + technical):
  Plain: we did not know which copy of the author's code we started from, so we got the
  author's full history and compared every one of their saved versions to our first saved
  version, counting how many files are different. The version with the fewest differences
  is the one we started from. Then we listed every file we added, changed, or removed.
  Technical: (1) git clone upstream -> sibling dir; (2) git -C clone fetch <our repo> HEAD
  (objects only, our repo untouched); (3) per upstream commit: git diff --name-only <c> f2fcb30,
  count lines, sort ascending; (4) verify top 3 with --no-renames + merge-base --is-ancestor;
  (5) git diff --no-renames --name-status af21bc18 FETCH_HEAD -> PROVENANCE-W73-af21bc18.txt.
  Protocols: HTTPS 443 to github.com (clone); local file transport for fetch. Output UTF-8 text.
- SDP chapter "Configuration Baseline": baseline = upstream af21bc18; delta list = E5 file.
- SDP chapter "Unused and Orphaned Code": fed by s14.
### [ARCHIVE-W73-2026-09-21.md] W73 DELTAS TO s7-s12
- s7 EXEC PATHS: none. (Trace hook on orchestrator path imports a missing module - E12.)
- s8 TOOLING: +T-W73-UPSTREAM clone C:\Users\Admin\upstream-OpenJarvis (full upstream history + our
  HEAD objects via FETCH_HEAD; never pushed). +T-W73-SCORE per-commit file-diff scorer (s6).
  +T-W73-CLASSIFY rule-based classifier -> PROVENANCE-W73-classified.csv (case-sensitive -cmatch).
  +T-W73-WSLB64 base64 transport for bash into WSL from PowerShell. Output lands on the console.
- s9 LOGGING: none.
- s10 RULES: (a) scripts into wsl.exe go base64-encoded, never with embedded double quotes;
  (b) PowerShell regex classification uses -cmatch; (c) never assert a gap or absence from
  output cut by Select-Object -First N; (d) interim downloads carry -E<exchange>, final name
  applied at commit; (e) pipe git through --no-pager in any scripted block.
- s11 GOAL: the configuration baseline is now fixed [M]; every future divergence and every RTM
  row can be measured against af21bc18. One author capability (tracing) found broken by import.
### [ARCHIVE-W73-2026-09-21.md] W73 ROADMAP DELTAS
- R0.5 [~] base pinned af21bc18 [M] (E4); change list produced (E5); classification in progress (s14).
- R3.2 gains H-W73-TRACELOST (evidence E10-E12).
- NEW R0.6: per-file justification of PRODUCT M 95 / A 72 (ATO); candidate for the 550B pattern.
- R0.4 [~] WSL2 runtime data confirmed (E14-E17). Residual: locate WSL code (command -v jarvis; uv tool list; pip show openjarvis).
- R0.5 [x] base af21bc18 [M] (E4), change list (E5), classified (E8), all 12 deletions explained (E10-E13, N8).
- NEW R0.7: Gray rules on s14 dispositions before any repo cleanup.
### [ARCHIVE-W73-2026-09-21.md] s14 UNUSED / ORPHANED CODE REGISTER (ATO)
Purpose: every file in HEAD-vs-base that is not product code gets a category, a reason it
exists, and a disposition (KEEP-PRODUCT, KEEP-TOOLING registered, RETIRE-ARCHIVE, REMOVE).
Also records author code Graystone DELETED and why. Source: PROVENANCE-W73-classified.csv.
| Category | Count | Disposition (proposed, Gray to rule) | Basis |
| PRODUCT M/A | 95/72 | KEEP-PRODUCT; per-file justification owed (R0.6) | E5 |
| AUTHOR-DELETED traces x10 | 10 | RESTORE from af21bc18 (held) | E10-E12 |
| AUTHOR-DELETED other | 2 | ACCEPT (macOS binary, stray file) | E13 |
| ROOT-MODULE-COPY model_catalog.py | 1 | REMOVE - orphan, zero importers | E9 |
| PATCHER | 74 | RETIRE-ARCHIVE (applied one-shots) | E8 |
| DIAGNOSTIC | 62 | KEEP-TOOLING if in tooling register, else RETIRE | E8 |
| MAILBOX-OPS | 12 | RETIRE-ARCHIVE (one-shot actions on family mailbox) | E8 |
| HANDOFF-DOC / SDP-DOC | 110/13 | KEEP-RECORD (move under docs/ later) | E8 |
| CLOUD-BUNDLE / MODEL-INPUT-DATA | 20/56 | RETIRE-ARCHIVE; check for secrets/PII before any move | E8 |
| BACKUP-IN-GIT / LOG-IN-GIT | 11/6 | REMOVE from index | E8 |
| OPS-SCRIPT / GRAYSTONE-TOOLS / ADHOC-TEST | 11/30/6 | REVIEW per file | E8 |
Per-file rows: PROVENANCE-W73-classified.csv.
### [ARCHIVE-W74-2026-09-21.md] s0 INDEX
s1 narrative | s2 evidence | s3 negative results | s4 hazards | s5 Gray corrections | s6 SDD/SDP feed
s7-s12 carried registers | s13 roadmap | s14 orphan register | W74 DELTAS at end
### [ARCHIVE-W74-2026-09-21.md] s1 WINDOW NARRATIVE
- E1: W73 commit 153d708 carried 3 of 4 files; PROVENANCE-W73-af21bc18.txt refused by .gitignore.
  Force-added in d85cc13, pushed to origin and gitlab, ls-files confirms both PROVENANCE files [M].
- E2: Gray ruled R0.7 (see s5). Scaffold built by extraction from ARCHIVE-W73 lines 127-282.
- E3-E5: R0.4 CLOSED. No global/uv/pip install in WSL; ~/OpenJarvis existed per shell history, since removed; history-named Windows trees all ABSENT.
- E6-E9: PRODUCT 167 measured at 1.3M tokens whole / 740K diff. Top-25 lists exposed backups, 2 wav, 3 lock files inside PRODUCT (T-W73-CLASSIFY defect). Re-noted -> PROVENANCE-W74-classified.csv: PRODUCT 133 (M92/A41), diff ~184K tokens.
- E10: T-W74-R06 PLAN: model lookup, 3 batches (53/50/30), 0 secret hits.
- E11-E13: SEND found no key in env or .env. Gray pointed to existing ask-550b-554.ps1; key lives in ~/.openjarvis/cloud-keys.env. SEND patched to read it, with paid->:free fallback.
- E14-E16: SEND covered 133/133 on the PAID model. Parser defect (field names inside 300 values) fixed by normalizer + parser patch; first parse kept as RAWPARSE. TRACK 0 CLOSED.
### [ARCHIVE-W74-2026-09-21.md] s2 EVIDENCE
- E1: git ls-files PROVENANCE-W73-* lists both; log -2 = d85cc13 over 153d708; both remotes up-to-date.
- E10: model nvidia/nemotron-3-ultra-550b-a55b context 262144 [M]; :free variant context 1000000 [M].
- E14: B1 in 103069/out 2930, B2 84189/5930, B3 45769/2547 tokens; all finish stop; covered 133 of 133, 0 missing, 0 dup [M].
- E16 [550B]: CLASS CONFIG 41, FEATURE 29, INSTRUMENTATION 19, BUGFIX 13, REFACTOR 9, SECURITY-FIX 8, UNCLEAR 6, PLATFORM-WINDOWS 4, UI 3, INTEGRATION 1. CARRY YES 112 / NO 17 / REVIEW 4. RISK HIGH 19 / MED 26 / LOW 88. SECURITY: CONFIRMATION-GATE 13, TOOL-EXECUTION 14, AUTH 5, SECRETS 5, NETWORK 26. REVIEW: scripts/quickstart.sh, server/app.py, server/speech_router.py, traces/store.py. UNKNOWN purpose: server/connectors_router.py, server/serve.py.
### [ARCHIVE-W74-2026-09-21.md] s3 NEGATIVE RESULTS (what things turned out NOT to be)
- git check-ignore -v on a TRACKED file prints nothing. That does NOT mean no rule matches;
  it means tracked files are exempt. Use --no-index to see the rule.
- R0.4 (E3): default WSL distro has NO global openjarvis: command -v jarvis empty; uv tool list none; pip show not found; import ModuleNotFoundError [M]. Rules out global/uv-tool/system-python install. Does NOT rule out a project venv or source checkout (E4 probe).
- R0.4 (E4): WSL home today holds NO OpenJarvis checkout, venv, or pyproject (find depth 4/7) [M]. Shell history shows one existed at ~/OpenJarvis (/home/Admin/OpenJarvis, npm run build:tauri run there), since removed. R0.4 CLOSED: WSL code location = ~/OpenJarvis, no longer present. History untimestamped: existence [M], dates unknown.
- H-W74-OLDTREES (E5): C:\WINDOWS\system32\openjarvis, C:\Users\Cornell\.openjarvis, C:\Users\Admin\openjavis all ABSENT (Test-Path -LiteralPath) [M]. No pre-f2fcb30 copy survives on this box outside the upstream clone; /opt/openjarvis = one script (W73). Track 0 code-location search CLOSED.
- H-W74-CLASSIFY (E8): T-W73-CLASSIFY keyed on directory before file kind, so PRODUCT held backups (.bak/.backupN/.bak.<date>/.fixbackup/.repair), 2 .wav files, and 3 lock files [M]. Fixed by re-noting only (no deletion, R0.7): PROVENANCE-W74-classified.csv; W73 csv kept as evidence. New categories TEST-AUDIO, DEPENDENCY-LOCK.
- 550B key is NOT in the process env and NOT in repo .env (no OPENROUTER names there) [M]. It is in C:\Users\Admin\.openjarvis\cloud-keys.env.
- The :free fallback was NOT needed: the key has paid access [M].
- 550B output is JUDGMENT, not measurement. Tag [550B]. Example of noise: ttsPlayer.ts tagged TOOL-EXECUTION. No HIGH row is confirmed until its whole file is read.
### [ARCHIVE-W74-2026-09-21.md] s4 HAZARDS AND DEFECTS
- H-W74-GITIGNORE: a .gitignore rule silently drops .txt instrument outputs at git add. Rule = .gitignore line 23 "*.txt" [M].
  Any future .txt deliverable needs git add -f or the rule narrowed. Verify with ls-files after every handoff commit.
- AUTHOR-CODE-W72-D.md, AUTHOR-GUIDES-W72-A/B/C.md in repo root are W72 bundler outputs, NOT in git by design (ARCHIVE-W73 s8). Do not commit.
- H-W74-OLDTREES: WSL history names other trees: C:\WINDOWS\system32\openjarvis, C:\Users\Cornell\.openjarvis\src, C:\Users\Admin\openjavis (sic), /opt/openjarvis. Candidate pre-f2fcb30 copies (E5 probe). History also holds PowerShell lines typed into bash - evidence for the state-the-shell rule.
- H-W74-AUTHOFF [550B, unverified]: server/app.py disables AuthMiddleware (if False). With base predating upstream #416/#417 this is the top ATO item. Confirm by whole-file upload of src/openjarvis/server/app.py.
- H-W74-TRACESTORE [550B, unverified]: traces/store.py replaced the SQLite TraceStore with a Rust wrapper that falls back to a no-op - a possible second cause of W73 zero traces.
- H-W74-TWOSERVE: src/openjarvis/server/serve.py exists beside cli/serve.py; 550B could not state its purpose. Possible duplicate implementation.
- H-W74-EGRESS: R0.6 sent 133 files of source diffs to OpenRouter (external). Record as an ATO data flow. Exact payloads kept in docs\SDP\evidence\W74\R06-W74-B1..B3.md.
### [ARCHIVE-W74-2026-09-21.md] s6 SDD/SDP FEED
- SDD: next-build target platform = Ubuntu VM (Gray, W74). Current native-Windows tree becomes the
  documented legacy build; s14 register ships as-is into the Unused and Orphaned Code chapter.
- CHANGE JUSTIFICATION chapter source = docs\SDP\evidence\W74\R06-W74-JUSTIFY.csv (133 rows, [550B]).
- PLAIN LANGUAGE: we asked a very large cloud model to read every change we made to the author's code and write one line per file: what changed, why, how risky, and whether to keep it for the Ubuntu rebuild. Then we counted the answers to make sure no file was skipped. Its answers are opinions to check, not facts.
- INSTRUMENT FLOW, gate by gate: G1 INPUT = PRODUCT rows of PROVENANCE-W74-classified.csv + upstream clone refs af21bc18 and 88a71af (local disk). G2 PLAN = GET https://openrouter.ai/api/v1/models (HTTPS/TCP 443, JSON, no auth) -> model id + context; git diff -U10 per file (local process) -> UTF-8 markdown bundles sized to 35 pct of context; regex secret scan of added lines, 0 hits. G3 SEND = key read from ~/.openjarvis/cloud-keys.env (never printed); POST https://openrouter.ai/api/v1/chat/completions (HTTPS/TCP 443, JSON UTF-8, Bearer auth), temperature 0, max_tokens 32000; full response saved as RAW json. G4 MERGE = parse pipe-delimited lines, strip field labels, write CSV UTF-8, coverage check against the plan file list.
### [ARCHIVE-W74-2026-09-21.md] W74 DELTAS
- s14: R0.7 ruled KEEP ALL, NOTE ALL. No code removed. Target platform for next build = Ubuntu VM.
- s8 tooling: T-W74-IGNORECHK = git check-ignore -v --no-index <file> (shows rule even for tracked files).
- s10 rules: after every handoff commit, verify with git ls-files that every named file is tracked.
- s8 tooling: EXISTING ask-550b-554.ps1 (repo root, 09-09): single-file 550B sender; key = C:\Users\Admin\.openjarvis\cloud-keys.env OPENROUTER_API_KEY; model :free; falls back to message.reasoning. REUSE before building.
- s8 tooling: T-W74-R06 = %TEMP%\r06_w74.py plan|send. PLAN: model lookup + diffs vs af21bc18 from upstream clone + 35%-context batches + secret scan -> R06-W74-B*.md, R06-W74-PLAN.json. SEND: key env->cloud-keys.env, paid->:free fallback, RAW json per batch, merge -> R06-W74-JUSTIFY.csv with coverage.
- s8 tooling: EXISTING ask-550b-554.ps1 (repo root, 09-09): single-file 550B sender; key = C:\Users\Admin\.openjarvis\cloud-keys.env OPENROUTER_API_KEY; model :free; falls back to message.reasoning. REUSE before building.
- s8 tooling: T-W74-R06 = %TEMP%\r06_w74.py plan|send. PLAN: model lookup + diffs vs af21bc18 from upstream clone + 35%-context batches + secret scan -> R06-W74-B*.md, R06-W74-PLAN.json. SEND: key env->cloud-keys.env, paid->:free fallback, RAW json per batch, merge -> R06-W74-JUSTIFY.csv with coverage.
- s7 exec paths: none. s9 logging: none.
- s8 tooling: T-W74-NORM normalizer (label strip). r06_w74.py and r06_normalize.py preserved in docs\SDP\evidence\W74\ (TEMP copies are volatile).
- s11 goal: Track 0 CLOSED. Every product change now has a justification line and an Ubuntu carry verdict - the input for rebuild scope and the RTM.
- s12 550B: used W74 on the paid tier; T-W74-R06 is the batch form of the pattern.
- s13 roadmap: TRACK 0 CLOSED W74 (R0.4, R0.5, R0.6, R0.7). Track 1 opens W75.
### [ARCHIVE-W75-2026-09-21.md] s0 INDEX
s1 narrative | s2 evidence | s3 negative results | s4 hazards | s5 corrections from Gray |
s6 SDD/SDP feed | s7-s12 carried registers | s13 roadmap | s14 orphan register | W74 DELTAS | W75 DELTAS
### [ARCHIVE-W75-2026-09-21.md] s3 NEGATIVE RESULTS (what things turned out NOT to be)
N1 "New build before my requirements document.docx" is NOT a requirements source: it is a Proxmox
   VE 9 Phase 6 Ansible lab build. Established by reading it whole; zero EA terms (grep).
N2 "Executive Assistant - Mac.txt" is NOT the n8n JSON the chat rendered: on disk it is Mac
   installer v1 with no email functions. Established by file(1) and grep, not by the rendering.
N3 The Tavily key in the n8n files is NOT a hazard: it is the template author's key, unused by
   Gray, no plans to use. Owner ruling 09/22. Do not chase it.
N4 The n8n requirement set is NOT Gray-authored from scratch; it is an adopted public template.
   Its rows are graded [R] and were ratified by the owner, which is what makes them requirements.
N5 The author's Agent QA Runbook was NOT found by name (qa|runbook) or content ('Agent QA Runbook')
   under docs\ or C:\Users\Admin\upstream-OpenJarvis\docs. Its location must come from the
   prior window that cited "37 scenarios" (ARCHIVE-W72/W73) - ask before re-deriving.
### [ARCHIVE-W75-2026-09-21.md] s4 HAZARDS AND DEFECTS
H-W75-DOWNLOADNAME: browser saves repeat downloads as "name (1).md"; selecting "newest by time"
   can pick a stale copy if the new download has not landed. Select downloads by CONTENT marker.
H-W75-MACDUPES: Mac v16 has two helpers doing the same job (_load_email_accounts :286,
   _read_accounts :395). Pick one on any reuse (same family as the 3-versions problem).
H-W75-MACSEEN: unverified whether Mac fetch_unread_emails sets \Seen. Check BEFORE any live run.
### [ARCHIVE-W75-2026-09-21.md] s5 CORRECTIONS AND CLARIFICATIONS FROM GRAY
- Tavily key: template author's, unused; do not spend cycles on things not in use.
- Pin the Mac email get/respond code as possibly reusable (filed in memory, executive-assistant).
- Add a validation of that code as a fallback if the primary path fails (R1.2a).
- RQ-023, RQ-027 are Phase 2 supporting roles (documents, Visio drawings); not core.
- RQ-011 must include Hotmail.
### [ARCHIVE-W75-2026-09-21.md] s6 SDD/SDP FEED
Vol 2 (SRS/RTM) now has a ratified baseline. SDP must carry:
- WHAT IT IS (plain language): a numbered list of every job Jarvis must do, where each job came
  from, and a box for "proven working". Progress = boxes proven / 28. Before W75 there was no list,
  so "not yet 50 percent" could not be measured; now it can.
- HOW IT WAS BUILT (infrastructure and flow): sweep of the user profile for requirement-like file
  names -> owner uploads candidates whole -> read, hashed (sha256) and graded [R]/[S] -> rows
  drafted with source IDs -> owner ratifies by strike/edit -> file copied into docs\SDP by content
  marker -> markers verified with Select-String. No model judgment is used in any row.
- TRACE LINKS: RQ-028 (verify own steps before reporting) is the original design's control for
  Defect 1 (claims without invocation). RQ-012 (approval before send) traces to the Defect 6
  confirmation gate. RQ-005/006/010/011 have a fallback implementation candidate (Mac v16).
- ATO: the requirement sources include a third-party template; provenance recorded in RTM section 2.
### [ARCHIVE-W75-2026-09-21.md] W75 DELTAS
- R1.1 [x] 02-SRS-RTM v0.3 RATIFIED by owner 09/22: 29 core rows (measure = verified/28, RQ-003 rollup), Phase 2 deferred RQ-023/027/032/033, Hotmail added to RQ-011. GAP-020 CLOSED. [M] markers verified in docs\SDP.
- NEW R1.2a MAC EMAIL FALLBACK VALIDATION (Gray 09/22). Order for RQ-005/006/010/011: author mechanism -> existing imap_mail/mailbox_tools -> Mac code as fallback. Steps: read C:\Users\Admin\executive-assistant\install_executive_assistant_mac.sh (2026-01-19, newer than v16) whole; extract its Python function server; confirm fetch does not set \Seen BEFORE any live run; run standalone read-only on a test mailbox; diff vs imap_mail; verdict INCORPORATE / REFERENCE / DISCARD. Runs when R1.2 reaches the email rows.
- R1.3 [ ] OPEN: runbook not found under docs or upstream docs (s3 N5). Locate first.
- s10 RULES DELTA W75: select downloads by CONTENT marker, not by name or newest time.
- s10 RULES DELTA W75: do not spend cycles on assets Gray does not use (owner 09/22).
- s11 PROGRAM GOAL MOVEMENT W75: the progress measure now exists. Baseline 28 core rows ratified; verified count to be set by R1.3.
### [ARCHIVE-W76-2026-09-22.md] INDEX
- s1 Window narrative (Track 1: R1.3 runbook baseline, then R1.2 mechanism map)
- s2 Evidence
- s3 Negative results (what it was NOT, and how established)
- s4 Hazards
- s5 SDD/SDP feed (infrastructure setup + gate-by-gate flow, plain language + technical)
- s6 Progress vs program goal (core VERIFIED / 28)
- W76 DELTAS (one-line appends to carried registers)
- CLEANUP REGISTER at EOF (inside carried block, carries forward)
- CARRIED VERBATIM from ARCHIVE-W75 line 84 to EOF
### [ARCHIVE-W76-2026-09-22.md] s3 Negative results
N1 W75 N5 was false: the runbook existed in the repo since 05-19. Established by name scan.
N2 The repo/upstream runbook difference is NOT content: normalized hashes identical.
N3 The runbook is NOT an EA verification set: no scenario fully covers any core row.
N4 Upstream clone file dates are NOT authorship dates: all read 09-21 (checkout); git
   last-commit dates range 03-12 to 09-21.
N5 The object-store fork probe is INVALID: 88a71af is present in upstream objects without any
   ref or ancestry (likely fetched for the W73 diff). Its "1154 commits" was every upstream
   commit, not commits since base. Replaced by merge-base --is-ancestor and ref checks.
N6 "Expect 7 sections" for Vol 3A v0.1 was a Claude miscount; the file had its intended 5.
N7 Pulling upstream is NOT a route to the EA write duties: at HEAD the author's connectors
   are still read-only and no draft/label/event-write/contact-write tools exist.
N8 enforce_tool_confirmation is NOT a control: the author states nothing reads it.
### [ARCHIVE-W76-2026-09-22.md] s4 Hazards
H-W76-EXPOSURE: LAN-bound server (0.0.0.0:8010), no [server.auth] section, CodeAct default
  agent with shell_exec (no allowlist per author) and destructive mailbox tools; author states
  server and desktop paths auto-approve toolkit tools; file_read/file_write allowed_dirs is not
  populated by any config key. Queued: confirm via server\app.py (W75 item 6).
H-W76-SECRET: Google OAuth client_secret_*.json (2025-11-19) sits in Downloads, outside the repo.
  Recorded only.
FIXED IN WINDOW: inventory instrument read UTF-8 without -Encoding (mojibake) and lacked an
  array guard (System.Object[] headings); regenerated in the close block with both fixed and with
  git last-commit dates instead of checkout dates.
### [ARCHIVE-W76-2026-09-22.md] s5 SDD/SDP feed
NEW VOLUME: docs\SDP\03-AUTHOR-BASELINE.md (Vol 3A) - the author's procedures as the ruler.
Plain language: before fixing or building anything, we write down what the authors told people
to do, then list every way our setup differs. That turns "is this a bug?" into "is this a
difference we chose, a difference from our older copy, or a real fault?".
How it was built, gate by gate (instrument -> input -> encoding -> output -> readable):
G1 Inventory generator: PowerShell walks upstream docs\ plus root README/CONTRIBUTING; per file
   SHA256 (first 16), first heading (UTF-8 read), git last-commit date -> markdown table,
   docs\SDP\evidence\W76\author-docs-inventory.md (UTF-8). Readable: yes.
G2 Install-baseline probe: reads config.toml as UTF-8; emits only section headers and an
   allowlist of keys; drops any line matching key|token|secret|pass; checks author install
   markers (native src, service script, scheduled task, Python, uv, Rust extension) ->
   graystone-vs-author-install.md. Readable: yes. No jarvis command run (H-W72-WINKILL).
G3 Fork-point probe: git merge-base --is-ancestor and for-each-ref --contains against the
   upstream clone; tree-hash match of our root commit; W73 CM-01 extracted verbatim ->
   fork-point.md with a CORRECTION section. Readable: yes.
G4 Multi-file bundler: concatenates N upstream docs into ONE markdown file with a header table
   (path, bytes, sha16, last commit) and '===== FILE:' / '===== END FILE:' delimiters ->
   author-capability-bundle.md, delivered in one upload. Owner's standing pattern for any
   multi-file read (09/22).
RTM v0.4: qualification is two-tier. Tier A = author runbook (partial set). Tier B = one
  non-interactive, production-build test per core row with one pass criterion. A row is VERIFIED
  only when its full row text passes.
Confirmation gate: Vol 3A section E carries the plain-language and technical explanation.
Trace: RQ-012 -> Vol 3A section E (author auto-approve on server/desktop) -> Defect 6.
Trace: RQ-031 -> D-09 (traces off) and D-13 (traces modules deleted).
### [ARCHIVE-W76-2026-09-22.md] CLEANUP REGISTER (duplicates and redundant access points - remove at completion if unused)
Rule: owner 09/22. Log when found; never remove mid-window. One line per item: id, what, locations, used?, window found.
- C-01 Unitemized: owner 09/08 reports up to 3 versions of the same functions from narrow reads. Itemize each as found. (W76)
### [ARCHIVE-W77-2026-09-22.md] INDEX
s1 Window narrative | s2 Evidence | s3 Negative results | s4 Hazards | s5 SDD/SDP feed | s6 Progress vs program goal | W77 DELTAS | CARRIED VERBATIM (from ARCHIVE-W76 line 
133
)
### [ARCHIVE-W77-2026-09-22.md] s2 Evidence
- E1 surface-probe.txt (evidence\W77): listener 127.0.0.1:8010 pid 17884 - config says 0.0.0.0, runtime binds loopback (feeds H-W76-EXPOSURE). 94 routes. telemetry.db = one table, NO tool columns; proves engine/model only.
- E2 rtm-verify.json run 1 via POST /v1/chat/completions, model qwen3-coder:30b: calculator, web_search, llm all registered+configured in /v1/tools. All 3 checks: tool_calls null, 0 new /v1/traces, answers from model knowledge. RQ-021: 6 model calls, ~32.8k prompt tokens, still no web_search, stale answer (3.12.2). telemetry ids 7118-7127: engine ollama on all, agent column EMPTY, metadata {}.
- E3 RQ-030 host: pid 17884 ESTABLISHED 192.168.1.137:52889 -> 172.16.33.200:11434; with engine=ollama on telemetry 7118-7127 = served by self-hosted lab Ollama, no cloud. D-03: runtime peer measured; config source still open.
- E4 HAZARD H-W77-GLOBALPY: live server pid 17884 runs GLOBAL Python312\python.exe, not repo .venv; jarvis.exe is the same global. Live tests exercise the global site-packages openjarvis (import path in author-check run).
- E5 PKG: global Python312 and .venv BOTH import C:\Users\Admin\OpenJarvis\src\openjarvis (editable). H-W77-GLOBALPY downgraded to dependency-set divergence.
- E6 run 2 author CLI (jarvis ask --agent orchestrator --tools X): exit 0 all three; stdout = answer only; telemetry 7128-7132 agent empty; model calls 2/2/1. Invocation unproven. SDP: Vol 3A v0.3 section F.
- E7 run 3 Surface C SDK ask_full: RQ-022 tool_results=[calculator "5754.0" success] turns 2 = VERIFIED. RQ-030 VERIFIED (E3 + model-list.txt). RQ-021 tool_results=[] turns 1, content = raw OpenHands XML call (evidence\W77\defect1-raw-payload.txt) = DEFECT 1 PARSER, captured whole. RQ-025 tool_results=[] turns 1, model answered directly. VERIFIED 2/28. SDP: Vol 3A v0.3 F5-F7.
- E8 CODE FIX + DEDUPE: orchestrator had no text-call parse; parser moved to ToolUsingAgent (textparse-v1/v2/v3), 152 lines cut from native_openhands (dedupe-v1), tagged-parameter defect fixed. Self-test 7/7; both SDK paths clean. SDP Vol 3A F8.
- E9 CONFIG FIX: [agent] tools had 12 tools, NO web_search. Server agent could not search; fabricated $7.8T for France GDP in 2.3 s. After adding web_search (13 tools) the SAME prompt returned World Bank/Statista figures in 18.8 s. surfaceA-gdp.json.
- E10 STARTUP BANNER INSTRUMENT: openjarvis.cli.serve logs allowed= / registry_keys= / tools_loaded= to backend.log via the logging module (readable, unlike the serve.py prints). Ground truth for the agent toolkit. Also BIND-ASSERT loopback=True api_key_set=True. SDP Vol 3A F9.
### [ARCHIVE-W77-2026-09-22.md] s3 Negative results
- N1 REGISTERED IS NOT INVOKED: the 4 author-COVERED rows are covered by mechanism, but the live chat path did not invoke calculator/web_search/llm. "5,754" was correct and still NOT evidence (Defect 1 class). VERIFIED stays 0/28 after run 1.
- N2 /v1/traces records nothing for the /v1/chat/completions path - not an invocation instrument for this surface.
- N3 Instrument defect: expect check missed "5,754" (comma). Fixed in scripts\diag\rtm_verify.py; verdicts unchanged.
- N4 First Surface A re-run used Claude prompt wording, not the author check - invalid comparison. Re-run with the author prompt.
- N5 The SEARCH RAN detector matched the bare word "trillion" and scored a FABRICATED $7.8T as PASS. Bad instrument; read the figure, not the flag.
- N6 agent.tools as a comma STRING is NOT a defect - cli\serve.py splits it; config.py:933 documents agent.tools as current. The content was wrong, not the shape.
### [ARCHIVE-W77-2026-09-22.md] s4 Hazards
- W77: the ONLY invocation record that exists today is AgentResult.tool_results (SDK). Server and CLI surfaces cannot qualify a tool-backed row. Tier B tests target ask_full until that changes.
- W77: native_openhands silently dropped <key>value</key> tool arguments before textparse-v3 (non-greedy regex). Pre-W77 tagged-style calls executed with {}.
- W77: /v1/tools reports the REGISTRY, not the agent toolkit. "registered: True" never meant the agent could call it. Use tools_loaded= from the startup banner.
- W77 REVISES H-W76-EXPOSURE: BIND-ASSERT shows loopback=True, api_key_set=True - LAN exposure not live as configured. D-06 destructive toolkit (now 13 tools, auto-approved on server) STANDS.
### [ARCHIVE-W77-2026-09-22.md] s6 Progress vs program goal
- VERIFIED at close: 2/28 (RQ-022 calculator, RQ-030 local ollama). First non-zero measure of the program.
- VERIFIED at close: 3/28 (RQ-021 web_search, RQ-022 calculator, RQ-030 local ollama). RQ-021 proven on TWO surfaces: SDK tool_results and the live server product path.
- VERIFIED at open: 0/28
### [ARCHIVE-W77-2026-09-22.md] CLEANUP REGISTER (duplicates and redundant access points - remove at completion if unused)
Rule: owner 09/22. Log when found; never remove mid-window. One line per item: id, what, locations, used?, window found.
- C-01 Unitemized: owner 09/08 reports up to 3 versions of the same functions from narrow reads. Itemize each as found. (W76)
- W77: jarvis.exe resolves to global Python312\Scripts\jarvis.exe, NOT the repo .venv - second access point to the CLI.
- W77 REMOVED: native_openhands.py _extract_tool_call + _extract_json_tool_call (152 lines), now inherited from ToolUsingAgent. Retrievable: native_openhands.py.bak_w77dedupe_20260922_160049.
- W77 OPEN: monitor_operative.py third parser copy - module-level def at 396 vs self. call at 280. Own whole-file step.
- W77 ROLLBACK: _stubs.py.bak_w77parser_* / .bak_w77parity_* / .bak_w77tagged_20260922_155752 ; native_openhands.py.bak_w77dedupe_20260922_160049 ; config.toml.bak-W77-* (in ~/.openjarvis) ; docs\SDP\02-SRS-RTM.md.bak-W77-v05 ; docs\SDP\03-AUTHOR-BASELINE.md.bak-W77-v03.
- W77 TOOLING: scripts\diag\ rtm_verify.py, sdk_verify.py, w77_native_check.py, w77_surfaceA_gdp.py, w77_parse_selftest.py, w77_cfg.py, w77_tel.py, patch_w77_parser.py, patch_w77_parity.py, patch_w77_tagged.py, patch_w77_dedupe.py. Plus the startup banner (E10) - no build needed, already running.

