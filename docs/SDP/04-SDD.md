# VOL 4 - SOFTWARE DESIGN DESCRIPTION (SDD)
Governing DID: DI-IPSC-81435 (verify, GAP-002). v0.2 DRAFT 2026-09-23 (W82), W83 update 2026-09-24 (sections 11, 14, 16 incl. 16.4), harvested from ARCHIVE-W42..W81 plus W82 measurement. W93 update 2026-09-26: 6.5 pointer, 20.9 (POAM-67 executor sites, gate harness), 20.10 (POAM-68 home, logs, port).
Every fact carries a grade and the window that established it. Line numbers are as recorded in that window; files have since
changed, so a line cite is a pointer to verify, not a guarantee (the gate moved from _stubs.py:265 to :390 in W58, for example).
Interfaces (ports, protocols, encoding) are in Vol 3; this volume references them by IF number.

## 1. HOW TO READ THIS VOLUME (plain language)
Each chapter explains one moving part of Jarvis twice: once for an engineer (file, line, order of events) and once in plain
words. Every guard also says what its SILENCE means - whether "no log line" means "nothing happened" or "something broke"
(rule from W44: a guard whose silence is not explained cannot be audited).

## 2. STARTUP AND ASSEMBLY (cli\serve.py)
Technical [R W42-W44, W56]:
- Launcher `start-openjarvis.ps1` (manual, admin session) sets `OPENJARVIS_LOG_LEVEL=INFO`, then runs
  `python -m openjarvis.cli serve --port 8010`. It does NOT set OLLAMA_HOST [M W80 N7]. It does not start the desktop app.
- Chain: click group `cli\__init__.py:55` -> `setup_logging` `:62` (consumes the env dial) -> `serve()` `:86`
  -> `_configure_file_logging()` `serve.py:109` -> ... -> `uvicorn.Config(..., log_config=None)` `serve.py:~653`.
- Process model [M W62, W79 EV7]: `.venv\Scripts\python.exe` launcher spawns base Python312 3.12.10, which imports repo `src\`
  (editable). The listening PID is the Python312 child.
- `serve()` is ONE function (~:96 to EOF). Three hard exits: dependencies (:115-124), engine (:151-157), model (:224-232).
  Everything after is fail-soft (try/except, log, continue) [R W44]. A running server may therefore lack subsystems.
- Assembly order [R W56]: get_engine -> setup_security -> optional MultiEngine -> InstrumentedEngine; chat agent and toolkit
  (one `_build_agent_tools(config, builder)` for chat and channel, D-15, 854b9c7); confirmation callback; channel bridge
  (disabled: no [channel] section, CHANNEL_ASSERT); speech backend; agent manager; scheduler; memory backend (SQLite default,
  injected into memory/retrieval tools); credential count report; bind safety (BIND_ASSERT, app.state.bind_is_loopback).
- Startup banner in backend.log [M W77 F9]: `allowed=`, `registry_keys=` (about 41-43), `tools_loaded=` (13 classes),
  `wired memory_backend into 1 agent tool(s)`, `BIND-ASSERT host=127.0.0.1 port=8010 loopback=True api_key_set=True`.
- Credential line :553-554 logs COUNTS only ("web_search: 1/2 keys"). Silence means no tool credentials are configured
  (24 tools, 0 keys measured W45), not a fault [M W45].
Plain language: pressing Start runs one long checklist. Three items are "stop if missing" (parts, brain, model). Everything
else is "note it and keep going", so Jarvis can start with some rooms dark. The startup note in the log says which tools it
actually picked up.

## 3. CHAT DISPATCH (server\routes.py POST /v1/chat/completions, IF-01)
| Path | Condition | Behavior | Grade |
|---|---|---|---|
| 1a | non-streaming, agent | agent.run() via asyncio.to_thread | [R W71] |
| 1b | streaming + agent/tools | create_agent_stream -> AgentStreamBridge; agent.run() in worker thread; reply BUFFERED then replayed (POAM-01) | [M W70] |
| 1c | non-streaming, no agent | engine via asyncio.to_thread | [R W71] |
| 1d | streaming, no agent | live engine token stream (Path A) | [M W71, W81 PONG 0.7 s] |
| B1 | streaming, non-cloud model, MultiEngine would route local model to a cloud engine (routes.py:374-388) | cloud_router.stream_local() direct to Ollama (IF-02a) | [R W81] never fired live |
| B2 | GET /v1/models when engine lists no local models (:480-483) | cloud_router.list_local_models() (IF-02b) | [R W81] |
| Cloud | model name routes to a cloud provider (get_provider) | cloud_router.stream_cloud() (IF-10); NO tools | [R W43, W80] |
Client chooses: ChatArea sends `agent: selectedAgentId || ''`; empty string lands on 1d [R v0.1].
Path 1b gate by gate [M W70]: webview POST (sse.ts, AbortSignal honored) -> SecurityHeadersMiddleware (middleware.py:33,
app.py:306) and AuthMiddleware (auth_middleware.py:16, app.py:315), both pass-through for streams -> routes.py:318-320
create_agent_stream -> StreamingResponse -> AgentStreamBridge subscribes AGENT_TURN_START, INFERENCE_START/END,
TOOL_CALL_START/END; agent.run() on asyncio.to_thread; callbacks cross threads by loop.call_soon_threadsafe into an
asyncio.Queue -> NativeOpenHandsAgent, max 3 turns, each turn a BLOCKING full completion (_generate) then classification
(native tool_calls, code blocks, text calls) -> text replayed only after run() returns.
Design decision DD-04 (owner, W70): Option A - stream each turn live, retract if the turn becomes a tool call. NOT built.
Plain language: with an agent, Jarvis writes the whole letter before reading any of it to you, because until it finishes it
does not know whether it will answer or go fetch something first.

## 4. CLOUD ROUTING (server\cloud_router.py)
Technical [R W43, W81, W82]: docstring says it bypasses the engine system and uses httpx directly (no cloud SDKs).
`get_provider()` (:69) routes by name prefix: gpt-/o1-/o3-/o4-/chatgpt- OpenAI; claude- Anthropic; gemini- Google;
MiniMax- MiniMax; four HuggingFace orgs (mlx-community/, bartowski/, unsloth/, lmstudio-community/) forced LOCAL; ANY other
name containing "/" goes to OpenRouter (catch-all, not a whitelist). Keys are read from cloud-keys.env on EVERY request
(`_load_keys` :39) so UI-entered keys work without restart; six env names override. Graystone additions: openrouter/ prefix
strip, HTTP-Referer/X-Title headers, 429 retry 5/10/20 s (retries every HTTPStatusError - H-W82-2), [DEBUG]/[RETRY] print()
to stderr (unreadable, H-W81-2). Local Ollama helpers `_ollama_host()` resolve config [engine.ollama] host > OLLAMA_HOST >
raise (F1a, 0da22e8). `list_local_models()` calls `_ollama_host()` outside its try (H-W81-3, deferred W82).
Guard statement: there is NO confirmation at the cloud request, by design - asking a model to write text cannot change
anything. Governance is downstream at the tool gate; cloud models are served WITHOUT tools [R W43, W80].
Silence: a cloud 404 with a valid key means an unknown model slug (the UI list carried a retired gpt-oss-120b:free) [M W43].
Plain language: when you pick a cloud model, Jarvis looks up the right key in its key drawer, addresses the envelope and
posts it. Nobody is asked first because a question cannot delete anything; the "ask first" guards sit on the tools.

## 5. TOOL DISPATCH GATE CHAIN (tools\_stubs.py ToolExecutor)
`execute()` is a wrapper (openjarvis-dispatch-outcome-v1, W46): it logs ATTEMPT, runs `_execute_inner`, and logs exactly
one OUTCOME with a reason code on EVERY exit including exceptions, so a future early return cannot be missed [R/M W46-W47].
| Order | Stage | Terminates with | Grade |
|---|---|---|---|
| 1 | tool lookup | UNKNOWN_TOOL | [R W46] |
| 2 | JSON argument parse | BAD_ARGS | [R W46] |
| 3 | boundary guard (non-local tools) | BOUNDARY_BLOCK | [R W46] |
| 4 | RBAC capability policy | CAPABILITY_DENIED (+ bus) | [R W46] |
| 5 | taint / sink policy | TAINT_VIOLATION (+ bus) | [R W46] |
| 6 | GATEPRED per-call predicate (W58) | NARROWED_NO_GATE or FAIL_CLOSED logged | [R/M W58] |
| 7 | CONFIRMATION GATE (section 6) | GATE_NO_CALLBACK, GATE_DENIED, GATE_TIMEOUT, GATE_INTERNAL_ERROR (+ bus) | [R/M W46-W60] |
| 8 | execution | OK, TIMEOUT_TOOL, TOOL_ERROR | [R W46] |
Execution runs on a ONE-WORKER ThreadPoolExecutor per call with future.result(timeout). A tool timeout ABANDONS the future;
it does not cancel the work, and the result is flagged outcome_verified=False - the tool may still finish later [R W46].
Security stages run BEFORE the human gate: a denied or tainted call never reaches a person.
Silence: an ATTEMPT with no OUTCOME means a call is still waiting (for example at the gate), not a lost record [M W47].
Record: dispatch.log (Vol 5) - ATTEMPT / OUTCOME reason= / GATEPRED / POLICY / PROTECTED lines, each with turn id [M W52].

## 6. THE CONFIRMATION GATE - GREAT DETAIL (Defect 6; owner requirement 08/20)
### 6.1 Plain language (09/02 requirement)
Some tools can change things that matter - run a command, move your mail to the trash. Before Jarvis uses one, it writes a
note with a ticket number, puts the note in a box, and announces the ticket on a channel the app listens to. The app shows
you the note with Approve and Deny buttons and a countdown. Your answer goes back with the same ticket number; a ticket can
be answered only once. Approve: the tool runs. Deny: it does not, and Jarvis is told you refused. No answer in two minutes:
it does not run, and Jarvis is told you did NOT answer - not that you refused - so it asks again instead of telling you
something untrue. If no one could ever answer (no listener wired), the tool is refused outright. For mail, the button only
appears when mail is actually about to move, not when Jarvis is only looking.

### 6.2 Components (three, plus the per-call predicate)
1. ELIGIBILITY - `ToolSpec.requires_confirmation` (declarative, readable by ast from outside the process). Declared by
   shell_exec, git_commit, agent_kill, apply_patch, and (W58) mailbox_move_to_trash and mailbox_empty_folder [R W50, W56, W58].
2. PER-CALL PREDICATE - `BaseTool.needs_confirmation(params)`, default True; the two mailbox tools override it with
   `_confirmed(params)` (dry_run false AND confirm == "CONFIRM DELETE"). Both must be true for the gate to fire [R/M W58].
   Rejected alternative (recorded so it is not revisited): a hidden predicate with the spec flag left False - the spec would
   lie to the external validator and the test route.
3. REGISTRY AND ROUND TRIP - `core\confirm_registry.py` [R/M W50, W61]: register() returns a uuid4 hex id, reaps expired
   entries inline; TTL 120 s (`_DEFAULT_TTL`, env OPENJARVIS_CONFIRM_TTL); decisions approved / denied / timeout, WRITE-ONCE;
   wait blocks on a threading.Event; resolve() sets it.
4. CALLBACK POLICY LAYER - what sits in the executor's callback slot at each construction site, and what it records (6.5).

### 6.3 Sequence, with measured timings [M W50, W52, W60]
1. Gate test in `_execute_inner` (flag AND predicate). Prompt and args digest built here - the only place holding both the
   tool object and resolved params (`_args_digest` caps at 400 chars).
2. register(tool, agent_id, turn_id) -> confirm_id.
3. Publish TOOL_CONFIRM_REQUEST on the bus: confirm_id, agent_id (inside data; Event is slots=True), turn_id, tool,
   args_digest, prompt, expires_at. Emitted +0.000-0.001 s after trigger.
4. CURRENT_CONFIRM_ID ContextVar set; callback called with the prompt only; reset in finally.
5. Transport: app.state.bus -> ws_bridge (bus-split fix 08/22) -> WS /v1/agents/events, unfiltered (IF-07).
6. Browser: ConfirmPrompt.tsx (useAgentEvents(undefined, onEvent, CONFIRM_EVENTS, subscribeAll=true)); dedupe on confirm_id;
   dismiss on tool_confirm_resolved (so no local timer); expires_at normalized (below 1e12 treated as seconds - unit unverified).
7. Answer: POST /v1/tools/confirm (IF-08) -> resolve() -> Event.set(): 7 ms. Waiter releases: 0.014 s end to end.
8. Registry re-read; TOOL_CONFIRM_RESOLVED published {decision, state, created_at, expires_at, reaped}.
9. Three-way result to the model: DENIED; APPROVED-but-callback-False (reported as internal error, not refusal); TIMEOUT
   (reported as "the user did not deny it, ask again"). No answer: TTL expiry measured 119.986 s, tool does not run.
Proof runs [M W52]: GATE_TIMEOUT 120.001 s; GATE_DENIED; OK success=True after Approve (echo w51-args-proof); live mailbox
gate timeouts twice with mailbox checked afterwards [M W60].

### 6.4 Threading model (load-bearing)
The tool chain runs on an asyncio.to_thread worker; the answering POST is served on the event-loop thread. The registry
therefore uses threading.Event, never asyncio.Event; Event.set() from the loop is non-blocking, which is why the POST returns
in 7 ms and why a 120 s wait does not hang the server [M W50]. Hazard: anything that stalls the event loop (a console write
frozen by QuickEdit, W62) delays the answer and can expire an approval with the human present. QuickEdit disabled (cd2d1db).

### 6.5 Callback slot by construction site (who can answer)
| Site | Path | Slot | Human present | Live or inert | Grade |
|---|---|---|---|---|---|
| chat-agent-live | serve.py chat agent (Path 1b; test-execute drives it) | `_server_confirm_callback` (serve.py:310): no confirm_id -> DENY_NO_CONFIRM_ID; else logs WAIT, blocks _cr.wait, logs decision, returns decision == APPROVED. interactive=True :316, callback :317, agent_cls :321. Opt-out OPENJARVIS_CONFIRM_INTERACTIVE=0 (default ON) | YES | LIVE | [R/M W49, W56] |
| managed-agent-tool | _stream_managed_agent non-DR loop; FRESH ToolExecutor per tool call | ConfirmPolicy (auto-approve, logs POLICY) | no (consent = wizard selection) | LIVE if a confirmable tool is selected (shell_exec, apply_patch) | [R W54-W56] |
| dr-sse-stream | generate_deep_research (background thread) | ConfirmPolicy | no | INERT (DR tools declare none) | [R W55-W56] |
| imessage-daemon | bind_channel imessage | ConfirmPolicy | no | INERT | [R W56] |
| sendblue-bridge | bind_channel sendblue | ConfirmPolicy | no | INERT | [R W56] |
| cli-ask | jarvis ask, ask.py::_run_agent | ConfirmPolicy -> TerminalConfirmGate designed W61 (stderr prompt, TTY stdin, only y/yes approves, writes decision to registry) | YES | build status: verify (W61-W62) | [R W56, W61] |
| SDK / SystemBuilder | sdk.py | none wired -> fail closed | - | - | [R Vol 3A E] |
ConfirmPolicy (openjarvis-confirm-policy-v1) returns True unconditionally BY DESIGN; its contract is attribution, not
enforcement. Turning it into a gate would change five sites at once [R W56]. Open owner question: are the DR sites inert by
intent or oversight (never ruled).
W93 UPDATE (upgrade branch upgrade/a6dcf846 at da752fbd; production main unchanged): the author's merge added executor sites.
Full measured table, options, risks and decisions in 20.9.4. New tokens: cli-ask-skill (real terminal gate on the skills
pipeline), cli-agent-ask / cli-skill-run / cli-chat (real terminal gate, decision recorded), cli-agent-ask-yes (ConfirmPolicy,
human_present=True, author --yes default kept). managed-agent-tool restored after the merge dropped it; in the upgrade it is one
request-local executor per stream (author design with taint seeding), not one per call. cli-ask build status: TerminalConfirmGate
behaviour measured through the real ToolExecutor by the W93 harness (20.9.5) [M W93]. Threading note: 6.4 applies to the chat
path; the managed-agent stream runs tools on the event-loop thread (H-W93-1), which is why that site cannot host a real gate.

### 6.6 Two mechanisms called "confirmation" (do not conflate) [M/S W57, W59]
A - the real gate above (buttons, structurally enforced). B - the mailbox model-side interlock: dry_run defaults TRUE and
apply requires confirm="CONFIRM DELETE". B is satisfied by the MODEL; it is a contract guard, NOT user consent. W59 removed
the duplicate prose approval; the tool still reports counts in dry-run.

### 6.7 Known limits of the gate
- The prompt shows tool and raw arguments, NOT the count or scope of mail affected (counts are computed after approval) [M W60].
- Gate fires before from_addr resolves to UIDs; long UID lists truncated at 400 chars in the prompt [R W58].
- Anything that reaches the loopback WebSocket receives an answerable confirm_id (socket unauthenticated; owner deferred
  auth 08/29; blast radius local) [R W50, M W81].
- Listener mounted in ChatArea: navigating away closes the socket while a gate may be waiting (App.tsx is the right mount) [R W51, W57].
- `enforce_tool_confirmation` in config is read by nothing on the execution path (author) [R Vol 3A E].
Silence: a gate with no POLICY/decision line on a confirmable tool means the gate did not fire (not eligible or predicate
narrowed - see GATEPRED line); POLICY decision=AUTO_APPROVE means an unattended site approved by posture.

## 7. MAILBOX SERVICE [R W61; M W58-W60]
Tools (JSON-string results): mailbox_list_accounts; mailbox_usage_report (mail.read, 600 s); mailbox_find_messages (mail.read,
600 s, counts windowed to newest ~10,000 per folder); mailbox_move_to_trash (mail.write, 1800 s); mailbox_empty_folder
(mail.write, 600 s). Writes MOVE to Trash; permanent deletion is left to the human; residual risk is scale (one call can move
many messages; Trash auto-purge limits the undo window) [R W49].
PROTECTED SENDERS v2: C:\Users\Admin\.openjarvis\protected_senders.json (JSON array, UTF-8, BOM tolerated), lowercase
substring on from_addr; replaces 10 built-in defaults; unusable file falls back to defaults, never empty. NOT applied when
exact UIDs are passed (open gap). Credentials: connectors\imap_mail_<account>.json (plaintext JSON), load_tokens()/connector_for().
Plain language: two locks on the mail bin - a password the assistant types itself (stops accidents) and a button only you can
press (your consent). A short "never throw away" list protects your own and receipt senders, except when exact message
numbers are handed over.

## 8. MANAGED AGENTS AND OPERATORS (autonomy layer)
Managed-agent SSE [R W54-W56]: POST /v1/managed-agents/{id}/messages (stream=true or mode=immediate) -> send_message ->
_stream_managed_agent -> generate -> engine.stream_full -> tool loop; SSE tool_call_start/tool_call_end.
TOOLKIT BIND (W54, verified W55): executed set == stream_kwargs["tools"] (resolved specs + MCP tools); a name outside it is
refused with PermissionError before ToolRegistry.get(). Invariant: what an agent can execute is by construction what it was
offered. Such a guard is unreachable through a well-behaved model, so it ships with an injected-denial harness.
DR branch: KnowledgeSearchTool, KnowledgeSQLTool (SQLite authorizer: knowledge_chunks only, 2fb87cf), ScanChunksTool, ThinkTool.
Manual/UI runs: route calls start_tick then a daemon threading.Thread per run - different agents run concurrently [R W74 bundle].
Author operators (OperatorManager -> TaskScheduler -> AgentExecutor -> OperativeAgent) have NEVER RUN here ([scheduler],
[operators] disabled) [M W72]. Managed agents in agents.db are the owner's personal agents, not the Jarvis build [S W72].
Defect class named (W54): consent granted against one set while a different set executes (W52 args {}, W53 toolkit, W54).
Inventory W82 [M evidence\W82\agents-inventory.txt]: 19 agent types registered (10 accept tools: deep_research, monitor_operative,
morning_digest, native_openhands, native_react/react, operative, orchestrator, rlm). Owner's 8 managed agents (agents.db): none has a
schedule (scheduler active with nothing to run); Cody-Builder ERROR litellm "LLM Provider NOT provided" (model string lacks provider
prefix); Cody-Coder ERROR "No module named 'litellm.responses.mcp'" (dependency); Cody max turns; agent_tasks and agent_checkpoints empty.
R3.1 closed by record: both errors are configuration/dependency, not agent logic.
DISPATCHER: the author ships agent_spawn / agent_send / agent_list / agent_kill (tools\agent_tools.py, registered by decorator) for an
orchestrator to spawn and direct sub-agents by type. They are ABSENT from the live registry_keys (startup banner 09/23 21:35) - the
dispatcher exists in code but is not loaded on this server [M W82]. Operators layer never run [M W72].

## 9. MODEL HOST RESOLUTION
| Reader | Order | Grade |
|---|---|---|
| engine\ollama.py:40 | config [engine.ollama] host > OLLAMA_HOST > localhost:11434 | [R W79-W80] |
| cloud_router._ollama_host | config > OLLAMA_HOST > raise (0da22e8) | [M W81] |
| cli\model.py:228 | config (deprecated config.py:430 property) > env | [R W80] |
| agent_manager_routes.py:109 | config only | [R W81] |
| cli\init_cmd.py:200 _do_download | env > localhost (ignores --host; ACCEPTED RISK, author defect, W82 F1b) | [M W82] |
| connectors\embeddings.py / tools\storage\embeddings.py | caller arg > localhost; no caller passes one; nomic-embed-text not pulled on .200 (DEFERRED, W82 F2) | [M W82] |
Owner decision W80: keep OLLAMA_HOST (3 scopes) and OPENJARVIS_OLLAMA_HOST (no reader). load_config is lru_cached: config
changes need a restart. Engine turn-down D-16: [engine] disabled list raises EngineDisabled at `_discovery._make_engine`, the
single choke point, preventing the self-loop to port 8010 (a0704c4) [M W79].

## 10. CONCURRENCY AND WORKER MODEL [M/R W82]
| Layer | Behavior | Grade |
|---|---|---|
| Scheduled managed agents | ONE at a time in total: single scheduler thread runs each due tick to completion (agents\scheduler.py:151-191) | [R af21bc18, identical locally M W82] |
| Per agent | one tick at a time (manager.start_tick refuses status "running") | [R] |
| Manual/UI agent runs | one thread per run; different agents concurrent | [R W74 bundle] |
| Chat SSE path | tool chain on asyncio.to_thread worker | [M W50] |
| Orchestrator tools | native calls in one turn run in parallel (ThreadPoolExecutor max_workers=len(calls)); W77 text-parsed calls are one per turn | [R W82] |
| Workflow / channel / sandbox | 4 / 2 / 5 | [R af21bc18] |
| Server | one uvicorn process, async routes overlap | [R] |
| GPU host (Ollama) | about 2 requests at once, rest queue; eval ~44 tok/s steady (qwen3-coder:30b, 18.9 GB VRAM); cold reload ~11.7 s after idle unload | [M W82 ollama-parallel.txt]; slot count inferred from timing |
Plain language: Jarvis can start many helpers, but only about two can talk to the brain at once; the rest wait in line. Helpers
on a timer take turns strictly one at a time. After a quiet spell the brain has to be woken up, which costs about 12 seconds.

## 11. OBSERVABILITY - LOGGING TOPOLOGY [R/M W42-W45, W52]
| Tree | Configured at | Sink (%LOCALAPPDATA%\OpenJarvis\logs unless noted) | Cap | Notes |
|---|---|---|---|---|
| root | cli\serve.py:60-74 | backend.log | 10 MiB x (1+3) = 40 MB | SanitizingFormatter; _TelemetryNoiseFilter drops telemetry polls; handlers.clear() makes startup order significant |
| openjarvis | cli\log_config.py setup_logging | console; ~\.openjarvis\cli.log only with --verbose | 5 MiB x3 | level: --quiet > --verbose > OPENJARVIS_LOG_LEVEL > WARNING |
| openjarvis.dispatch | tools\_stubs.py | dispatch.log | 2 MB x4 | propagate=False; ATTEMPT/OUTCOME/GATEPRED/POLICY/PROTECTED |
| openjarvis.agent | agents\native_openhands.py | agent.log | 2.5 MiB x4 | propagate=False |
| openjarvis.retry400 | engine\ollama.py | engine.log | 2 MiB x2 | propagate=False; never fired (W45) |
| openjarvis.engine.ollama | module logger (propagates to root) | backend.log | root cap | INFO "SYSMERGE merged=N chars=M" (W83); openjarvis.server "Memory context injection failed" is DEBUG - invisible at INFO |
Four gates a log line must pass: logging not print(); logger level; propagate; a handler. print() and the warnings module go to
a detached console and produce zero readable bytes (FastAPI duplicate-route warning H-W81-5 is console-only). No log path crosses
a network. Starting the server without start-openjarvis.ps1 drops the tree to WARNING (single point of darkness).

## 12. VOICE AND STOP PATHS (frontend)
Voice out [M W64-W67]: ChatArea TTS effect (release gate: first segment at first clause boundary past 20 chars; later segments at
last completed sentence; muted = consumed) -> ttsPlayer.enqueue -> splitIntoUnits (first <=90 chars, rest <=350) -> pump (single
consumer, `pumping` guard, `generation` cancel token; W68 re-kick on queue depth) -> synthesizeSpeech (IF-03, 30 s) -> Kokoro
(IF-03a) -> decodeAudioData -> schedule (lead 0.08 s) -> masterGain -> destination bound by setSinkId to an explicit endpoint
(W66) -> keepalive source gain 0.0001 holds the endpoint awake (W67). Never rebuild the AudioContext (drops keepalive).
Time to first audio = release gate 1.5-2.3 s + TTFB 1.0-1.5 s. No confirmation gate (non-destructive). An active audio
session proves nothing about audibility.
Voice in [R/M W82]: speech routes are split across two routers. Graystone `server\speech_router.py` is mounted FIRST (app.py:294) and
now carries only POST /synthesize (Kokoro proxy) and the streaming sockets; the AUTHOR routes in api_routes.py (mounted by
include_all_routes, app.py:297) serve POST /transcribe and GET /health since W82 H5 (marker openjarvis-w82-h5-author-speech-routes-v1).
The frontend types (api.ts TranscriptionResult, SpeechHealth) were written for the author shapes. Upload transcription path:
useSpeech.ts MediaRecorder -> transcribeAudio -> author route -> app.state.speech_backend (faster-whisper) - proven W82 V3.
Streaming path (useSpeechStream.ts -> WS /v1/speech/stream) is DEAD: speech_router.py holds three stacked copies of the WS block;
the first-registered /stream handler is a stub; the full handler calls _transcribe_and_send with 3 args while the final module-level
definition takes 2 (POAM-38). A Graystone TEMP DIAGNOSTIC wrote every uploaded mic clip to %LOCALAPPDATA%\OpenJarvis\audio_debug
(18 clips 07/13-07/15 remain; removed W82, disposition pending owner - POAM-39).
Stop [M W69]: Square button -> ChatArea.stopStreaming -> AbortController (ChatArea.tsx:198) -> fetch aborts -> "(Generation
stopped)". Capability gap: UI main thread starved during generation; stop does not cancel backend generation.

## 13. BUILD AND DELIVERY TOPOLOGY [M W51, W63, W68-W69]
source -> vite -> src\openjarvis\server\static -> EMBEDDED in exe at Rust build -> NSIS bundle -> installed
%LOCALAPPDATA%\OpenJarvis\openjarvis-desktop.exe -> OpenJarvis.lnk -> Tauri host -> msedgewebview2.exe. The backend also serves
static at /, so a vite build reaches the browser immediately and the exe only after a full tauri build and install. Production
build only (DD-02). `npm run build:tauri` is frontend only; a running app blocks the build; installed exe timestamp is the only
install proof. CDP port 9222 removed W63; `--use-fake-ui-for-media-stream` auto-approves mic permission (hazard).

## 14. CODE MAP - AGENT STREAMING PATH (carried from v0.1, [R/M 2026-09-21])
| Unit | File | Role |
|---|---|---|
| NativeOpenHandsAgent | agents\native_openhands.py | agent on path 1b |
| BaseAgent / ToolUsingAgent | agents\_stubs.py | agent contract; shared text tool-call parser (textparse v1-v3, W77) |
| OrchestratorAgent | agents\orchestrator.py | W77 text-call fallback (64b0660) |
| InferenceEngine | engine\_stubs.py | engine contract |
| OllamaEngine | engine\ollama.py | live backend; stream_full retries without tools on HTTP 400; W83 _oj_merge_system (one system message per request) |
| MultiEngine / InstrumentedEngine / GuardrailsEngine | engine\multi.py, telemetry\instrumented_engine.py, security\guardrails.py | routing, telemetry, secret/PII scan (stream_full gaps POAM-04/05) |
| EventBus | core\events.py | pub/sub |
| AgentStreamBridge | server\stream_bridge.py | path 1b SSE bridge |
| ToolExecutor / ConfirmPolicy | tools\_stubs.py | gate chain, policy layer |
| confirm_registry | core\confirm_registry.py | registry |
| cloud_router | server\cloud_router.py | cloud + local-direct paths |
| ChatArea / ConfirmPrompt / ttsPlayer | frontend\src\components\Chat\, frontend\src\audio\ttsPlayer.ts | UI, gate UI, audio |

## 15. RECURRING DESIGN LESSONS (for designers and assessors)
- A guard has three separable properties: it exists, it fires, and you can tell afterwards what it did (W56).
- A correctly bound guard is unreachable through its normal caller; every allow/deny boundary needs a harness that injects the
  denied case (W55).
- Consent granted against one set while another executes is a recurring failure class (W52-W54).
- Enforcement belongs where the work happens (SQLite authorizer, toolkit bind), not where the request is read (W55).
- An instrument you cannot read is an instrument you do not have (09/06); register it and verify its output path at build time.

## 16. RETRIEVAL-AUGMENTED GENERATION (RAG) - STATE AT W83 [M evidence\W83\*; R af21bc18]
Author stack: MemoryRegistry backends sqlite (FTS5 keyword, default), bm25, dense (embeddings), faiss, colbert, hybrid (reciprocal rank
fusion of two retrievers), knowledge_graph, knowledge (connectors KnowledgeStore); ingestion tools\storage\ingest.py + chunking.py,
`jarvis memory index`, /v1/connectors/upload/ingest[/files]; use in answers by context injection on the chat path ([agent]
context_from_memory), RetrievalTool, and deep_research over knowledge.db.
Author intent [M W83, af21bc18 core\config.py:874-876, :923]: context injection ON by default - context_top_k 5, context_min_score 0.0,
context_max_tokens 2048, context_from_memory True. tools\storage\context.py is byte-identical to af21bc18 [M W83].

### 16.1 Context injection flow, gate by gate (all in-process, no network until gate 7)
| Gate | Where | What happens | Record / silence |
|---|---|---|---|
| 1 | serve.py:2589-2613 | if context_from_memory: MemoryRegistry.create(default_backend, db_path) -> SQLiteMemory (Rust FTS5); console "Memory: active"; backfilled into retrieval tool | "[DEBUG] wired memory_backend into 1 agent tool(s)" in backend.log |
| 2 | app.py:225-226 | app.state.config, app.state.memory_backend set | - |
| 3 | routes.py chat_completions (before ANY dispatch branch: 1a/1b/1c/1d) | guard: config + backend + context_from_memory + messages; query = last user message | failure logged at DEBUG on openjarvis.server - INVISIBLE at INFO (H-W83-3) |
| 4 | context.py inject_context | backend.retrieve(query, top_k) - FTS5 OR-of-terms, BM25 score (positive, small: 0.03-8.3 measured) | MEMORY_RETRIEVE {backend, num_results} on the GLOBAL bus - in-process only, NOT carried by WS /v1/agents/events [M W83] |
| 5 | context.py | filter score >= min_score; truncate to max_context_tokens (whitespace words); prepend ONE SYSTEM message "The following context was retrieved..." | MEMORY_RETRIEVE {context_injection: True, num_results, total_tokens} - in-process only |
| 6 | routes.py rebuild -> _handle_agent / stream_bridge._run_agent -> agents\_stubs.py _build_messages (author, unchanged) | injected system message rides in ctx.conversation; output = [agent system prompt, context system message, user] | - |
| 7 | engine\ollama.py generate / stream / stream_full (Graystone W83 sysmerge, 675cda6) | _oj_merge_system joins all system messages, in order, blank-line separated, into ONE at the first's position | "SYSMERGE merged=N chars=M" INFO openjarvis.engine.ollama -> backend.log [M]; no line = one or zero system messages |
| 8 | HTTP POST 172.16.33.200:11434 /api/chat, JSON UTF-8 (IF-02) | Ollama applies the model chat template | prompt_eval_count = prompt_tokens_evaluated in inference_end events |

### 16.2 Why injection never worked before W83 (two stacked faults, both measured)
- Fault A (Graystone config): context_min_score 20.0 (set against the old 21 GB corpus) vs measured scores max 8.32 -> nothing passed
  the filter [M W83 memory-search-scores, inject-probe]. Restored to author defaults 5 / 0.0 / 2048 (owner ruling W83, config.toml
  out of git, backup config.toml.bak-W83-A-20260924_102149).
- Fault B (author code vs model template): qwen3-coder:30b's Ollama template renders ONLY THE FIRST system message; a second is
  silently dropped (+1 token vs +180 merged, H4 test). The author's context arrives as the SECOND system message, so on the agent paths
  it never reached the model at any threshold [M W83 optionA-VV: config live, prompt_tokens_evaluated unchanged at 4194].
  Fixed at the engine (openjarvis-w83-sysmerge-v1). V&V: 4194 -> 5314 (+1120, predicted ~1100), SYSMERGE lines present [M sysmerge-VV].
- Direct paths 1c/1d already had one system message (the injected one) - not affected by Fault B.

### 16.3 State after W83
memory.db: 115 chunks, 405 KB, all source=upload, test material (probe files, code-companion.md, README text); created_at stored as
JULIAN DAY (2461252.39 = 2026-07-30), not epoch. memory.db.old 21.36 GB retained (condition: ingester fix + one real ingestion cycle).
knowledge.db 0 chunks. Chat toolkit: retrieval only (memory_store/retrieve/search not loaded). Semantic retrieval impossible (F2).
DELIVERY proven; RECALL QUALITY not proven - with only test content, the model declines to treat it as "your notes" (H-W83-1).
Cost: about +1,100 prompt tokens per agent turn at current content.
Plain language: Jarvis has a notebook and now actually opens it before answering - before today it opened the notebook and then a
filter threw every page away, and even when a page got through, the brain's reading glasses only showed it the first note on the desk.
Both are fixed. The notebook itself is still full of test scribbles, so what Jarvis reads is not yet useful to you.

### 16.4 Memory stores - they are SEPARATE by author design (W83) [M/R]
| Store | Written by | Read by | Synchronized with | State W83 close |
|---|---|---|---|---|
| memory.db (SQLite FTS5, author default) | upload route (IF-19), memory_index, memory_store | memory_search, memory_retrieve, retrieval tool, context injection (16.1), /v1/memory/* | nothing else | 3 docs, NUL-free, all writers and readers use the ONE app.state backend object [M] |
| MEMORY.md | memory_manage | memory_manage (SystemPromptBuilder would, but is unwired - D-33) | nothing | seeded W83 (D-32), directed take/list verified (P2) |
| knowledge.db | connectors (KnowledgeStore) | deep_research, knowledge tools | nothing | 0 chunks |
| memory.db.old (21 GB) | nothing | nothing | - | retained, condition unmet |
Ingest paths into memory.db, gate by gate: (1) upload route -> _process_single_file -> decode_text_bytes -> _chunk_text (~1000
chars, paragraph then last-space split) -> backend.store; (2) memory_index -> ingest_path (rglob; skips hidden, _SKIP_DIRS incl.
target/dist/build, sensitive files, binary extensions) -> read_document -> decode_text_bytes -> chunk_text (512 tokens, 64 overlap,
min 50 - shorter content dropped) -> backend.store; (3) memory_store -> backend.store (no chunking, no minimum).
Decoder (D-29, one implementation): BOM -> utf-8 -> latin-1; refuse any NUL or >5% control chars; logs DECODE lines to backend.log.
Memory tools (D-26): wired to the backend by the Graystone backfill (D-27 author ordering defect); no memory tool is gate-eligible.
CLEANUP REGISTER: memory_search, memory_retrieve and retrieval are three model-visible readers of the same store, plus context
injection - redundant access points; kept by owner decision (O3), logged for later consolidation.
Plain language: Jarvis has four separate filing cabinets. Only one (memory.db) is in daily use, and everything that files or looks
things up uses that same cabinet. The other three are either empty, unused, or not yet inspected.
### 16.5 Persona layer (W83) - WIRED since 6429769
Gate flow: (1) serve.py at agent construction builds SystemPromptBuilder(agent_template = override or OPENHANDS_SYSTEM_PROMPT +
tool descriptions, config.memory_files, config.system_prompt) and passes it as prompt_builder -> logs "PERSONA prompt_builder wired"
(backend.log). (2) ToolUsingAgent forwards it to BaseAgent (D-35). (3) Every turn _build_messages calls builder.build(): template +
"## Agent Persona" (SOUL.md <=4000) + "## Agent Memory" (MEMORY.md <=2500) + "## User Profile" (USER.md <=1500); the prefix is
rebuilt only when one of the three files changes (mtime+size). (4) Context injection (16.1) adds its system message; (5) sysmerge
joins them into ONE system message at the engine. Edits by memory_manage / user_profile_manage / the owner appear on the next turn
with no restart. Notes routing is one owner line in SOUL.md (D-37). Scope: native_openhands only.

## 17. OFFICE DOCUMENT PATH (W83) - gate by gate, and where it is VISIBLE [M evidence\W83\s3-*; R code]
Owner ultimate goal (W83): a clear communications data flow of Jarvis that can be visualized with NO GAPS IN VISIBILITY. This section
records the flow and marks each gate's record so gaps are explicit.
| Gate | Hop | Port / protocol / encoding | Record produced | Visible? |
|---|---|---|---|---|
| 1 | Client -> backend POST /v1/chat/completions | TCP 127.0.0.1:8010, HTTP/1.1, JSON UTF-8 | uvicorn access line | yes (backend.log) |
| 2 | Context injection + persona (16.1, 16.5; SOUL office line D-44) | in-process | SYSMERGE line | yes (backend.log) |
| 3 | Engine -> Ollama /api/chat | TCP 172.16.33.200:11434, HTTP/1.1, JSON UTF-8 | inference_end event (prompt_tokens_evaluated) | yes (WS /v1/agents/events) |
| 4 | Model tool call -> ToolExecutor | in-process | dispatch.log ATTEMPT (tool, args) / OUTCOME (success, reason) | PARTIAL - reason code only; the tool's error TEXT is not recorded (G-11: FAIL_OTHER had to be reproduced by replay) |
| 5a | code_interpreter: fence strip (D-42) -> blocklist -> subprocess `python -c` -> workspace snapshot diff (D-46) | child process, same venv, cwd workspace (D-41), 30 s, stdout <=10,000 chars | content: Files line FIRST, then stdout; metadata files[path, size_bytes] on TOOL_CALL_END (D-46) | PARTIAL - file creation VISIBLE; stdout/stderr and exit code not recorded durably (G-11) |
| 5b | file_write: relative anchor (D-43) -> Office guard (D-45) -> confinement check | in-process, UTF-8 text | OUTCOME only | PARTIAL - success message shows the given name, not the full path (G-10) |
| 6 | python-docx / python-pptx / openpyxl write the file | local disk, OOXML (zip + XML) | the file itself in ~\.openjarvis\workspace; code_interpreter writes at the workspace top level are listed in content and TOOL_CALL_END metadata (D-46) | PARTIAL - top level only; subfolders and absolute-path writes (G-1) are not listed (H-W83-28) |
| 7 | Tool result -> model -> reply | in-process -> gate 1 response | reply text | yes; the model reads CONTENT only (4000-char cut). Re-run 4: replies honest 6/6 vs the filesystem (R2 class closed). The Files line reaching the model is INFERRED from outcomes, not observed (G-11) |
| 8 | Delivery to the family member | none | none | NO path exists (G-3) |
Gaps named here feed the POA&M (POAM-50..56). The downloadable architecture artifact (ports, protocols, encoding at each gate) is a
queued owner deliverable built from sections 16 and 17.
W87 delta (D-46, c85fcf9; recorded W88): at the code_interpreter gate, file creation is now VISIBLE - in content (what the model
reads) and in TOOL_CALL_END metadata (the author's machine record on the event bus). Still NOT visible: tool content text is not
recorded durably (G-11, POAM-54) and dispatch.log OUTCOME remains a reason code. Plain language: Jarvis now checks its own folder
after running a program and says which files are new; what we still cannot see afterward is the exact words each tool sent back.

## 18. TRACE SYSTEM (W88) - author design, how it was lost, restore, and what it records [M evidence\W88\*; R af21bc18]
### 18.1 Plain language
A trace is Jarvis's flight recorder for one job: what was asked, what the model said, which tools it used, what each tool sent
back (including the exact error words), what memory it looked up, and the final answer, each with a time. The author built
this so the system can be checked afterward and so the learning system can improve from real jobs. In our copy the recorder
was missing and a do-nothing stand-in sat in its place, so nothing was ever written down. W88 put the author's recorder back.
### 18.2 Author design, gate by gate (af21bc18; all in-process in the backend python process unless stated)
| Gate | Component (file) | What it does | Transport / encoding | Record |
|---|---|---|---|---|
| 1 | ToolExecutor (tools\_stubs.py:574-590 ours) | publishes TOOL_CALL_START {tool, arguments} and TOOL_CALL_END {tool, success, latency, result = tool CONTENT cut at 10240 chars, metadata = JSON-safe ToolResult.metadata incl. D-46 files[]} | in-process EventBus, python dicts | event only (not durable by itself) |
| 2 | InstrumentedEngine | publishes INFERENCE_START {model, engine} and INFERENCE_END {usage, content, tool_calls, finish_reason, ttft, energy} | in-process EventBus | event only |
| 3 | TraceCollector (traces\collector.py) | wraps ONE agent.run(): subscribes to INFERENCE_START/END, TOOL_CALL_START/END, MEMORY_RETRIEVE for the run only; converts each into a TraceStep (generate / tool_call / retrieve), adds a respond step, builds a Trace (query, agent, model, engine, steps, result, messages, timing, tokens) | in-process objects | Trace object; collector.last_trace |
| 4 | TraceStore.save (traces\store.py) | persists the Trace and every step | local file ~\.openjarvis\traces.db, SQLite WAL mode, check_same_thread=False; JSON (UTF-8) in TEXT columns | tables traces (trace_id UNIQUE), trace_steps (input/output/metadata JSON per step), traces_fts (FTS5 over query/result/agent, trigger traces_fts_ai) |
| 5 | TRACE_COMPLETE | collector publishes {trace}; TraceStore.subscribe_to_bus listens and also saves (server: app.py:227-241) | in-process EventBus | second save path (see 18.6 double-save risk) |
| 6 | TraceAnalyzer (traces\analyzer.py) | summaries, per-route and per-tool stats, export - input to the learning system | reads traces.db | reports |
### 18.3 Where the collector is wired (entry points)
| Entry point | Traced at af21bc18? | Evidence |
|---|---|---|
| JarvisSystem.ask() (system\core.py:133) -> QueryOrchestrator.ask() -> _run_agent() (orchestrator.py:212-225) | YES, when SystemBuilder built a trace_store (builder.py:204-209, traces enabled) | vv_orch_trace_w88: 1 trace, steps generate + respond |
| Server chat route POST /v1/chat/completions (server\routes.py, native_openhands) | NO - no trace code at af21bc18 (git grep: no match) | vv_traces_w88 gate B: HTTP 200, 0 new traces |
| CLI jarvis ask (cli\ask.py) | NO - calls engine.generate() directly, or with --agent builds the agent itself (own _run_agent, TerminalConfirmGate W61); no trace code, same as the author's ask.py | W88 read of ask.py whole; jarvis ask returned PONG with 0 traces |
| Upstream after the baseline (ef005703) | the author wired a TraceCollector into the chat endpoints (store.save() directly) and REMOVED the app.py bus subscription to prevent double saves | upstream app.py comment, W88 diff |
builder.py subscribes ONLY the telemetry store to the bus (builder.py:336), never the trace store: JarvisSystem.ask() cannot double-save.
### 18.4 How the package was lost (measured W88)
| Fact | How established |
|---|---|
| The author's repo is complete at af21bc18 (__init__ 638 B, analyzer 11552, collector 8264, store 10185) and at current upstream main a6dcf846 (collector 10069, store 11363 - still developed) | git ls-tree -l in the upstream clone |
| Graystone's repo is not a clone: first commit f2fcb30 2026-05-30 "Graystone Lab: remote MCP/Ollama integration, Rust extension, UI fixes" | git log --reverse |
| The author's .gitignore has a bare `traces/` line that matches src\openjarvis\traces\ | git show af21bc18:.gitignore |
| The package was untracked until 08-05; 58c05e2 (2026-08-05) un-ignored it and committed a 1-line __init__ and an 18-line store.py | git log --diff-filter=A; no deletion commit exists (--diff-filter=D empty) |
| The 18-line store.py wraps openjarvis_rust.TraceStore (importable, has TraceStore) or falls back to a class that does nothing; it has no subscribe_to_bus | W88 bundle read; import probe |
| The author never wrote it: no RustTraceStore anywhere in the author's history (all branches) | git log --all -S RustTraceStore (empty) |
| The Rust store created traces.db (2026-06-09) with an incompatible schema: trace_id PRIMARY KEY, steps_json, metadata_json; no trace_steps; 0 rows | read-only sqlite_master probe |
| The server built the stub at every start (traces.db-shm touched at start) and app.py:240 subscribe_to_bus raised AttributeError, swallowed by the author's except/pass | code read + file times |
| collector.py and analyzer.py absent -> the orchestrator path would raise ModuleNotFoundError whenever a trace store was set | import probe: collector FAIL |
### 18.5 Restore (D-47, commit 1d4b3ae4) and V&V
Pre-restore probe (probe_trace_restore_w88, read-only): every dependency present (core.events, core.types StepType/Trace/TraceStep,
agents._stubs, security.file_utils; all six EventTypes); the author's store/collector/analyzer loaded from git into memory and ran
a synthetic turn against in-memory SQLite: 1 trace, 3 steps; the tool step held "Tool execution error: PROBE-ERROR-TEXT" and the
files[] metadata. Patch (patch_traces_restore_w88): server stopped (PID 20320); stub files backed up; traces.db/-shm/-wal moved to
evidence\W88\backup\tracesdb-ruststub-20260925_112010; four files written from git cat-file blobs, every hash = author blob;
fresh import OK. Live V&V after restart (PID 27988, 11:21:39): A - the author's store created traces, trace_steps, traces_fts and
triggers; B - chat path HTTP 200 "PONG" in 10.0 s, 0 new traces (baseline behaviour); C - 0 tracebacks after the last start marker;
D - JarvisSystem.ask("Reply with the single word PONG.") built in 4.7 s, answered in 9.9 s, TraceCollector recorded 1 trace
(98f48c8c1a194968, native_openhands, qwen3-coder:30b) with steps generate (prompt_tokens 6183, completion 3) and respond.
### 18.6 Visibility now (feeds section 17 and the data-flow artifact)
| Path | Tool content / error text durable? | Where |
|---|---|---|
| JarvisSystem.ask() (orchestrator) | YES - every step, tool result up to 10240 chars, error text, files[] metadata, model content, tokens | traces.db trace_steps |
| Chat route (what the family uses) | NO - not traced (author baseline); dispatch.log OUTCOME is a reason code only | G-11 remainder, POAM-57 |
Open risk (unmeasured): in the server, app.py subscribes its store to TRACE_COMPLETE on app.state.bus. If an orchestrator turn runs
inside the server on that same bus, the collector saves the trace AND publishes TRACE_COMPLETE, so it is saved twice; the second
INSERT violates UNIQUE(trace_id). SYMPTOM would be an IntegrityError after the answer. The author found and fixed this upstream
(ef005703). Measure before porting chat-path tracing (POAM-58).
### 18.7 Negative results (what things turned out NOT to be)
- POAM-32 said "trace modules deleted": no deletion commit exists; the package was never tracked before 08-05 (git log -D empty).
- The config was not the cause: config.toml has no [traces] section; the author default enabled=True applies, as in the author's template.
- jarvis ask producing 0 traces is NOT a restore failure: cli\ask.py never reaches the orchestrator (author baseline behaviour).
- vv_traces_w88 gate C reported 151 Traceback lines: all historical. Its timestamp filter let un-timestamped lines through;
  tb_since_start_w88 (anchored on the last start marker) found 0.
- The first author diff was against the upstream clone HEAD ef005703, NOT the baseline af21bc18 - it mixed the author's later work
  with Graystone changes (evidence\W88\trace-wiring-diff-vs-author.txt is labelled accordingly). The byte-identity checks named
  af21bc18 explicitly and stand.
- The W88 SDP-owed patch v1 inserted CRLF lines into LF files: the bundle written by PowerShell Set-Content had rewritten every line
  as CRLF. Restored from backup and redone (v2) with line endings read per anchor from the real file.
- The newest-by-timestamp ARCHIVE picker chose evidence\W83\backup\pre-handoff-d, which lacks PART 5; the live file is the repo-root copy.
### 18.8 Hazards
H-W88-1 The upstream clone's checked-out HEAD is NOT the author baseline (it is ef005703). Always name af21bc18 explicitly.
H-W88-2 A PowerShell Set-Content bundle rewrites line endings (CRLF); never infer a file's EOL from a bundle.
H-W88-3 The author's .gitignore bare `traces/` line hides the traces SOURCE package in any copy-not-clone install.
H-W88-4 Un-timestamped log lines (tracebacks) defeat time-based filters; anchor on the last start marker instead.
H-W88-5 "Newest file by timestamp" pickers select backups (evidence\*\backup\pre-handoff-*); pin the live path.
H-W88-6 jarvis ask does not exercise the orchestrator; the traced entry point is JarvisSystem.ask() (vv_orch_trace_w88).
H-W88-7 git diff / git log with long output opens the pager in PowerShell and waits at ':' - use git --no-pager in blocks.
H-W88-8 The venv has no test tooling by default; install the author's LOCKED dev versions with uv pip install (never uv sync).
### 18.9 Author test verification (W88)
The author's own tests for the package (tests\traces, 7 files from af21bc18 - lost to the same `traces/` gitignore trap) were
restored and run with the author's locked pytest 9.0.2: 52 passed. Four FTS tests raised teardown errors on Windows only (an
author test-fixture defect, D-48, still present upstream); fixed by closing the store in the fixture: 52 passed, 0 errors.
The author documented the gitignore cause as fix #372 (CHANGELOG v1.0.2), which confirms 18.4 cause (1).
### 18.10 POAM-58 double-save - reachability analysis (W89) [R code, ours = af21bc18 + Graystone as built; M static inventory]
PLAIN LANGUAGE: the trace recorder writes a finished job into the notebook itself, and then also announces "job done!" on a
loudspeaker. The notebook keeper (the server's trace store) listens to one loudspeaker and writes down whatever it hears. If the
recorder announces on the SAME loudspeaker the keeper listens to, the job is written twice - and the notebook refuses a
duplicate page, so an error is raised after Jarvis has already answered. We checked every loudspeaker in the server. The keeper
listens only to the server's own loudspeaker; the only recorder that can run in the server announces on a different one. So it
cannot happen today. It WILL happen if someone later puts a recorder on the server's loudspeaker without first telling the
keeper to stop listening - which is exactly what the author changed upstream.
MECHANISM: TraceCollector.run saves the trace (traces\collector.py:103) and then publishes TRACE_COMPLETE {trace}
(collector.py:106). A TraceStore subscribed to TRACE_COMPLETE on the same bus (store.py:225-232) saves it again. The second
INSERT violates traces.trace_id UNIQUE -> sqlite3.IntegrityError raised inside the publisher's call stack (EventBus handlers run
synchronously), i.e. out of collector.run after the agent has already produced its answer. Requires BOTH on ONE bus.
INVENTORY (git grep over src, W89):
| Item | Where | Count |
|---|---|---|
| TRACE_COMPLETE publishers | traces\collector.py:106 | 1 (only the collector) |
| TraceStore subscribed to a bus | server\app.py:239-240 (on app.state.bus) | 1 (builder.py never subscribes a trace store - only telemetry, builder.py:336) |
| TraceCollector constructions | system\orchestrator.py:218 (JarvisSystem.ask, only when s.trace_store is set) | 1 |
| Trace writers that NEVER publish | agents\executor.py:660 (AgentExecutor, managed agents: store = app.state.trace_store via agent_manager_routes.py:1483 and :1852, or serve.py:492-499 for the scheduler); learning\spec_search\external_adapter.py:65 | 2 |
BUS TOPOLOGY (who creates which EventBus):
| Bus | Created at | Used by |
|---|---|---|
| SERVER bus | cli\serve.py:176 EventBus(record_history=False) -> create_app -> app.state.bus (app.py:215) | app trace store subscription (app.py:239-240); channel _wire_system (serve.py:428-430); ChannelBridge wrappers (serve.py:608-612); SendBlue restore (app.py:94-106 uses app.state.bus, or a NEW EventBus() if it is None) |
| GLOBAL bus | core\events.py:178 get_event_bus() - module singleton; only reset_event_bus() (events.py:187); NO setter anywhere in src | SystemBuilder when no bus is given (builder.py:100) - the scheduler JarvisSystem (serve.py:503) |
| SDK bus | sdk.py:172 - every Jarvis() creates its own EventBus() | the digest route (digest_routes.py:77-79) |
EVERY SERVER-SIDE JarvisSystem.ask() CALLER:
| Caller | System / bus | Trace store | Double save? |
|---|---|---|---|
| POST digest generate (digest_routes.py:73-81): `with Jarvis() as j: j.ask(..., agent="morning_digest")` | SDK system / SDK bus (sdk.py:172) | not established (sdk.py has no trace wiring by grep; whether its build creates one is unread) | NO - whatever it records, it announces on the SDK bus, where no store listens |
| Channel messages (serve.py:410-437): `_wire_system = JarvisSystem(bus=bus, ...)`; `wire_channel(channel_bridge)` | JarvisSystem / SERVER bus | NONE (no trace_store argument) -> orchestrator.py:216 skips the collector | NO - untraced; inactive while config channel.enabled=False (startup CHANNEL_ASSERT enabled=False) |
| ChannelBridge wrapper (serve.py:596-612) | ChannelBridge(system=None) / SERVER bus | none | NO - _handle_chat calls ask() only when system is not None (channel_bridge.py:266-268) |
| SendBlue restore (app.py:83-106) | ChannelBridge (no system argument) / SERVER bus | none | NO |
VERDICT: POAM-58 is NOT reachable in the system as built (af21bc18 + Graystone, W89). The only collector that can run in the
server process (the digest's SDK system) publishes on its own bus; the only subscribed store listens on the server bus; the
systems on the server bus carry no trace store. REACHABLE IF: (1) a JarvisSystem WITH a trace_store is built on app.state.bus
and runs ask() - e.g. adding trace_store to the channel _wire_system (serve.py:428); or (2) the author's chat-path collector
(#513) is ported on app.state.bus while app.py:239-240 still subscribes the store. The author's own resolution (upstream
ef005703, app.py comment): do NOT subscribe the store; the collector is the single writer. That removal is a precondition of
POAM-57.
NEGATIVE RESULTS: no code installs a bus globally (no setter; only reset); the SDK never shares the server bus; the channel
system has no trace store; managed-agent traces are saved directly by AgentExecutor and never announced on TRACE_COMPLETE.
SIDE FINDING (POAM-62, CORRECTED and MEASURED W89): the managed-agent trace read-back routes open a NEW TraceStore per request
and do not call close() - agent_manager_routes.py list_traces (:1964) and get_trace (:1989), routes GET
/v1/managed-agents/{agent_id}/traces and .../traces/{trace_id}. AUTHOR CODE: identical lines at af21bc18 (:1877, :1902) and still
present at upstream a6dcf846 (:2260, :2288; only the fallback path changed to get_config_dir()). CORRECTION: the feedback route
api_routes.py DOES close its store (:821; author :804; upstream :1065) - the earlier text said it did not; that was wrong. Its
hard-coded DEFAULT_CONFIG_DIR/traces.db is author code, unchanged upstream, and only matters if traces.db_path is moved.
MEASURED (server PID 27988, Windows HandleCount): baseline 468; after 50 get_trace calls (50 x 200) 503; after 50 list_traces calls
on agent 52c9e6ad6aa1 (50 x 200) 493. A per-call leak would add at least 1-3 handles per call (db, -wal, -shm) in BOTH batches;
the count FELL in the second batch. VERDICT: NOT a live leak - CPython closes each sqlite3 connection when the route returns
(TraceStore holds no reference cycle). The +35 / -10 movement is thread-pool and socket churn.
OWNER RULING W89: "we will work this when we get to fixing the upstream code. That should be done as one complete service
we are repairing." The explicit close() is DEFERRED to the upstream-code repair of the managed-agents service, done as one
complete service - not patched piecemeal now. Until then the author code stays byte-identical (no live leak measured).
H-W89-3 A missing close() is not proof of a leak in CPython - measure the process handle count across repeated calls first.
EXECUTION PATH REGISTER additions: (d) managed agents - AgentExecutor saves its own trace (executor.py:660) with the app store;
(e) digest route - SDK Jarvis() with its own bus, trace recording not established; (f) channel messages - JarvisSystem on the
server bus with no trace store: UNTRACED.
HAZARDS: H-W89-1 a TRACE_COMPLETE-subscribed store and a collector on the same bus = every trace saved twice (IntegrityError).
H-W89-2 long git grep output pasted from the console can lose its first section header - write such output into a bundle file.

## 19. SKILLS (W89) - author design, which paths get skills, the startup warning [R af21bc18 + a6dcf846; M probe_skills_w89]
### 19.1 Plain language
A skill is a folder with a SKILL.md file: a short name, a one-line description, and written instructions for a kind of job
("search arXiv", "write a research paper"). OpenJarvis turns each skill into a tool the agent can call; calling it hands the
agent the instructions (or runs the skill's steps). Some skills come from other projects (Hermes) and carry extra labels
OpenJarvis does not use; it keeps them and prints a warning. The warning is harmless. Today the main planner and background
agents get the skills; the chat window does not - that is how the author built it, and still builds it.
### 19.2 Author design, gate by gate (all in-process in the backend python process; files are UTF-8 on local disk)
| Gate | Component (file) | What it does | Record |
|---|---|---|---|
| 1 | Skill on disk | ~\.openjarvis\skills\<source>\<name>\SKILL.md (YAML frontmatter + markdown) and .source (TOML: source, commit, category, installed_at, translated_tools, missing_tools, scripts_imported) | the files |
| 2 | SkillParser (skills\parser.py) | strict pass: name and description required, length and naming rules (a failure rejects the skill); tolerant pass: FIELD_MAPPING maps version/author/tags/depends/required_capabilities/user_invocable/disable_model_invocation onto the manifest and platforms/prerequisites under metadata.openjarvis; any other field -> WARNING, value kept in metadata.openjarvis.original_frontmatter | backend.log WARNING (logger openjarvis.skills.parser) |
| 3 | SkillManager.discover (skills\manager.py) | scans config.skills.skills_dir (~/.openjarvis/skills/) and .\skills (relative to the server cwd; absent here); first-seen name wins; loads overlays (few_shot) | in-memory registry |
| 4 | SkillManager.get_skill_tools | wraps each skill as a SkillTool (skills\tool_adapter.py): tool name skill_<name>, description = skill description, parameters = one optional `task` string for instruction-only skills or the {placeholders} of pipeline steps; category skill | tool list |
| 5 | SystemBuilder.build (system\builder.py:171-194) | adds the SkillTools to the tool list, rebuilds the ToolExecutor, collects few-shot examples | JarvisSystem.tools, skill_manager |
| 6 | SkillTool.execute | pipeline skill: runs its steps through SkillExecutor; instruction-only skill: returns the markdown instructions as ToolResult.content; metadata {skill, skill_source, skill_kind, steps} rides TOOL_CALL_END into traces | trace step (orchestrator path) |
get_catalog_xml() (an <available_skills> prompt catalog, 553 chars for 5 skills) exists but NOTHING calls it at af21bc18 or a6dcf846.
No platform filtering: platforms [linux, macos] is stored, never checked - a Windows host does not exclude the skill.
### 19.3 Which execution paths get skills (measured W89)
| Path | Skills? | Evidence |
|---|---|---|
| JarvisSystem.ask() (orchestrator) | YES - 5 SkillTools among 24 tools | probe_skills_w89 section D |
| Scheduler / managed agents (serve.py builds a JarvisSystem with SystemBuilder for the AgentExecutor) | YES (same builder; the startup warnings come from this build) | serve.py SystemBuilder(config).build(); startup console |
| Server chat route (native_openhands, the family path) | NO - tools come from config [agent] tools (19 names); no skill code in serve.py, routes.py or app.py | startup tools_loaded list; git grep; SAME at upstream a6dcf846 (probe section E: NONE) |
| CLI jarvis ask | NO at af21bc18 (the author wired skills and traces into ask later: #920) | delta report s7 |
### 19.4 Installed skills (5, all imported from Hermes - none is an author built-in)
arxiv, blogwatcher, llm-wiki, polymarket, research-paper-writing (~\.openjarvis\skills\hermes\). research-paper-writing was
installed 2026-06-05 (commit 6f6eb871 of the Hermes source); its .source lists translated_tools Task->delegate_agent and 25
missing_tools (mostly false positives: LaTeX, NeurIPS, GitHub, PowerPoint). Few-shot examples: 0.
### 19.5 The startup warning
Only research-paper-writing warns: fields `title` (a display name) and `dependencies` (in Hermes, a list of PYTHON PACKAGES:
semanticscholar, arxiv, habanero, requests, scipy, numpy, matplotlib, SciencePlots). It must NOT be mapped to OpenJarvis
`depends`, which lists other SKILLS - the dependency resolver would look for skills named numpy. Leaving it unmapped is correct.
The skill loads. Decision: no change (author design; parser unchanged upstream).
### 19.6 Negative results
- The warning is not a load failure (strict pass passed; skill discovered and wrapped as skill_research-paper-writing).
- Not a Graystone divergence: skills modules 18/18 identical to af21bc18; parser.py unchanged at a6dcf846 (empty diff).
- Platform is not a filter: a linux/macos skill still loads on Windows.
- The chat window having no skills is not a Graystone regression: the author's current upstream does not wire skills there either.
### 19.7 Chat-path skills - options and OWNER RULING W89 (2026-09-25): A
AUTHOR INTENT: skills are tools on the SystemBuilder paths (planner and managed agents); the author has not put them on the
server chat route as of a6dcf846, and built a prompt catalog (get_catalog_xml) that nothing uses yet.
A. Keep the author design. Effect: skills are testable today through the planner and managed agents. Risk: none new; the family
   chat cannot use skills.
B. Add SkillTools to the chat agent (serve.py, mirroring builder.py:171-194). Effect: chat can call skills. Risks: divergence the
   author has not made; one tool schema per skill (200 skills = 200 schemas in every chat request - prompt size and model choice
   quality); instruction-only skills return long markdown cut at 4000 chars (research-paper-writing SKILL.md is ~2400 lines);
   skills reference tools we lack; shell-based skills hit the confirmation gate (120 s wait unattended).
C. Use the author's catalog (get_catalog_xml) in the chat prompt plus one loader tool. Effect: scales better (one line per skill).
   Risks: still a divergence (no author caller); prompt grows about 110 chars per skill (200 skills ~ 22,000 chars).
OWNER RULING W89: "we will do A for now." Skills stay on the author design (planner and managed agents). Section 19 and
POAM-60 are WHERE the skills will be added; B or C is decided at that time, with this assessment.
### 19.8 Skills install placeholder (POAM-60)
Owner W89: several repos give over 200 skills; they will be installed LATER, not now. Before installing: decide 19.7; use the
author's importer (jarvis skill ... with the github / hermes / openclaw sources); note the author's later safeguards not in our
baseline - #639 capability and trust-tier checks at install and run time, #961 reject symlinks in imported skills, #781 prune
cyclic skills, #780 log discovery failures; import a small batch first and measure prompt size and tool choice.
SEQUENCE (owner W89): first the owner approves the author's baseline against the Graystone baseline, to his satisfaction on
services offered; THEN the skills install. Not far off - possibly the same window if this version is close to final.

## 20. SERVICES BASELINE APPROVAL AND THE UPSTREAM-LEVEL DIRECTIVE (W89, 2026-09-25)
### 20.1 Plain language
We lined up three versions of OpenJarvis side by side: what the author published when we started (af21bc18), what the author
has now (a6dcf846), and ours. Ours turned out to be the author's original almost untouched, plus a small layer of our own
work. The owner approved that picture for every service, and directed that Jarvis be brought up to the author's current
version, keeping only the parts we built that the author does not already provide.
### 20.2 Evidence
evidence\W89\services-catalog-af21bc18-a6dcf846-HEAD.md (services_catalog_w89.py, read-only; 735 lines; owner wiki copy).
Measured: 33 packages; 0 author baseline files absent in ours; 23 of 33 packages untouched by Graystone (line-ending-only
differences ignored); Graystone layer = 41 changed author files (server 14, tools 9, agents 4, cli 4, core 3, engine 3,
prompt 1, speech 1, telemetry 1) + 5 Graystone files (connectors\imap_mail.py, core\confirm_registry.py,
server\speech_router.py, server\serve.py 0-line shadow, and the mailbox tools inside tools). Routes A0 107 / A1 111 / G 112;
12 registries; 74 CLI commands. Author since the baseline: agents proactive, opencode, baseline_cloud, baseline_local (+
skillorchestra); connectors imap, apple_calendar; engines nim, afm; new memory package (FactStore local); tools queue_action,
get_pending_actions, execute_pending_actions, check_permission, record_decision, get_weather, calendar_search,
calendar_upcoming; routes /v1/approvals/* (3) and a credentials DELETE; CLI path, run-task, trust; config classes Afm,
DeepResearch, Proactive, WeatherTool. Graystone-only services: 5 mailbox tools + imap_mail; POST /v1/tools/confirm (Defect 6);
POST /v1/speech/synthesize and the speech WebSocket; POST /v1/tools/test-execute.
### 20.3 The 13 services - OWNER APPROVED ALL 13 (W89): "I approve them all"
| # | Service | Graystone layer vs af21bc18 | Author since af21bc18 | Overlap to settle in the repair |
|---|---|---|---|---|
| 1 | Chat (server, prompt, system, cli) | server 14, cli 4, prompt 1; speech_router, confirm route, test-execute | server 20 changed + 3 new (approvals, daemon, model capabilities); WS auth, CORS, chat-path traces #513, persona wiring | 11 server files changed by both |
| 2 | Managed agents | agents 4 | agents 64 + 21 new | POAM-62 |
| 3 | Tools and Office | tools 9 + 5 mailbox tools | tools 29 + 4 new; code_interpreter AST validation #1002 | Patch B, G-1 |
| 4 | Memory and RAG | tools\storage | new memory package (facts, cross-session recall, provenance) | vs W83 context work |
| 5 | Speech | speech 1 + speech_router | speech 5 + voice_io | POAM-38 |
| 6 | Connectors and mailbox | + imap_mail | 25 changed + imap (any provider) + apple_calendar | author imap vs our imap_mail |
| 7 | Channels | none | 7 fixes | - |
| 8 | Skills | none | 9 fixes (#639, #961, #781, #780) | ruling A; install (POAM-60) |
| 9 | Traces, telemetry, learning | traces restored (D-47); telemetry 1 | traces 3, telemetry 9, learning 9 | POAM-57 |
| 10 | Security | none | 12 + 2 new (taint, SSRF, symlink, audit chain, CORS) | - |
| 11 | Engine and models | engine 3 | 16 + 5 new (NIM, AFM, async HTTP) | - |
| 12 | MCP | none | 4 + loader (external JSON config) | remote MCP |
| 13 | Frontend (desktop) | outside src; many files changed by both (W88 delta s8) | heavy (Tauri lib.rs +2920) | production build only |
| - | Approvals vs confirmation | confirm_registry + /v1/tools/confirm (Defect 6) | approvals queue (approval_routes, approval_store, 5 tools) | same problem solved two ways |
### 20.4 OWNER DIRECTIVE W89
"I want the Author's original and updated services placed on OpenJarvis ... we should get our Jarvis to the same level as the
current GitHub OpenJarvis project is at. We added a small portion of code and I do not believe in re-creating the wheel if it
suits our needs." -> Target: the author's current build (upstream main) + the Graystone layer. Where the author solved what we
patched, the author's version replaces ours (D-25 -> #823; D-35/D-36 -> #546/#637/ef28e5f8; POAM-57 -> #513/#930; G-1 -> #1002;
H-W81-6 -> subprotocol WS auth). Graystone code is kept only where the author has no equivalent.
### 20.5 Feasibility assessment (W89) - possible; size to be MEASURED by a trial merge
WHY POSSIBLE: 0 author files missing; git holds the common ancestor af21bc18, the author's current build and ours, so this is a
standard three-way merge in which only lines changed by BOTH sides conflict. METHOD (recommended): a separate git worktree built
from the author's current build, the Graystone layer re-applied service by service in the approved order, its own venv built by
the author's install procedure, its own port (e.g. 8011); production (8010) untouched until V&V passes; V&V = the author's test
suite first, then live checks, then the 4 VERIFIED requirements re-verified; then the switch, pushed to both remotes.
RISKS: conflicts in files changed by both (33 in src, 11 in server; frontend incl. Tauri lib.rs; pyproject.toml +127/-21 and
uv.lock) - resolved per service; DEPENDENCIES - never in the production venv; the worktree venv follows the author's procedure;
the Rust extension (rust\, 38 files changed upstream) must be rebuilt; STATE LOCATION - author #549 consolidated state under one
env-aware home directory: memory.db, traces.db, agents.db, config.toml paths must be checked before the switch; FRONTEND - the
Graystone changes (TTS player, CSP, VitePWA removal) re-applied, production build only; SKILLS - installing after the upgrade
brings the author's safeguards (#639 trust tiers, #961 symlinks, #781 cycles) - recommended order: upgrade, then skills.
NEXT: trial merge in a temporary worktree (%TEMP%), conflict count per service, then deleted - main and production untouched.
### 20.6 Findings from the catalog (recorded; worked in their service repair)
F1 (POAM-63) duplicate access point: speech_router.py exposes the speech WebSocket twice - /v1/speech/stream and a double-
prefixed /v1/speech/v1/speech/stream. F2 (POAM-64) POST /v1/tools/test-execute is Graystone-only; if it executes tools directly
it may bypass the confirmation gate - read in the Chat/Tools repair. F3 (POAM-65) live config.toml carries [analytics] (owner
09/22: remove that path as dead code) and lacks [traces], [telemetry], [learning*], [tools.storage], [tools.mcp] (author
defaults apply).
### 20.7 Trial merge results and the OWNER-APPROVED upgrade plan (W89) [M trial_merge_w89 -> evidence\W89\trial-merge-report.md]
MEASURED (git merge-tree --merge-base af21bc18, in the object database only; HEAD and tracked files verified unchanged):
author changed 811 files; Graystone changed 725 with real content (537 of them build/scripts/handoff/evidence files, 39 docs,
91 frontend - none conflict); changed by BOTH 67; applied or auto-merged with no hand work 768 of 811; CONFLICTED 43 files,
380 hunks; line-ending-only conflicts 0 (plain and EOL-ignoring merges identical).
THE 43 CONFLICTS BY KIND: (1) GENERATED - no hand work: frontend\package-lock.json 100, uv.lock 94, frontend\src-tauri\Cargo.lock
30, frontend\tsconfig.tsbuildinfo (modify/delete) -> take the author's, regenerate (uv lock re-adds python-pptx and openpyxl);
(2) SMALL CONFIG: pyproject.toml 6, core\config.py 4, .gitignore 2, configs\openjarvis\config.toml 1, frontend\package.json 2;
(3) REAL CODE: Python 18 files / 51 hunks - Chat 8/25 (agent_manager_routes 11, serve 6, api_routes 3, routes 1, ask 1,
auth_middleware 1, connectors_router 1, stream_bridge 1), Managed agents 3/9 (_stubs, morning_digest, native_openhands),
Tools 4/7 (code_interpreter 3, knowledge_sql 2, tools\_stubs 1, tools\__init__ 1), speech faster_whisper 3, engine ollama 3,
telemetry gpu_monitor 1; Frontend about 16 files / about 95 hunks (api.ts 46, lib.rs 8, DataSourcesPage 7, InputArea 5,
SettingsPage 5, SetupScreen 4, others 1-3). CAREFUL MERGES: tools\_stubs.py (our dispatch log + Defect 6 confirm emit vs the
author's taint work), code_interpreter.py (our D-41/D-42/D-46 vs the author's AST validation #1002), native_openhands.py.
Where the author superseded a Graystone change, the author's side is taken (sysmerge #823, persona wiring, WS auth, #513).
OWNER APPROVED W89 ("I approve and it makes sense") - METHOD: (1) TEMPORARY LOCAL GRAFT: git replace --graft <our root commit>
af21bc18, so git sees the author's baseline as our common history (replace refs are local; never pushed); (2) an upgrade branch
in a SEPARATE git worktree; git merge of the author's current main (expect exactly these 43 conflicts); resolve service by
service; (3) remove the graft - the merge commit keeps the author's main as a real parent, so every FUTURE author update is a
normal git merge; (4) the worktree gets its own venv by the author's install procedure (the production venv is never touched),
the Rust extension rebuilt, its own port 8011; V&V = the author's test suite first, then live checks, then the 4 VERIFIED
requirements; the #549 state-path check; then the switch, pushed to both remotes. ORDER: dependencies + config -> Chat ->
Tools and Office -> Managed agents -> speech / engine / telemetry -> Frontend (production build) -> V&V -> switch.
ESTIMATE: 3-4 windows. PLAIN LANGUAGE: git lined our copy up against the author's latest and found that almost everything
slots in by itself; 43 files need a person to choose between two edits of the same lines, and a third of those are machine
lists that are simply rebuilt. We will do it on a spare copy while the working Jarvis keeps running, and swap only when the
spare copy passes every check.

### 20.8 Upgrade execution record W90-W92: merge committed, frontend by Method B, desktop build verified [M evidence\W90..W92; R git history]
#### 20.8.1 Plain language
We put the author's newest Jarvis and our Graystone changes together on a spare copy, not on the working Jarvis. W90 and W91
settled the Python side and made a careful plan for the screen side. In W92 we found that the plan would have quietly thrown
away about 860 lines of the author's screen code, because one bad save in our history (June 2, commit bc498a16) had deleted
them and git carried that deletion forward without asking anyone. So we rebuilt the screen side a different way (Method B):
we undid that one bad save in a practice area, merged again, and only then touched the spare copy. The result compiles, builds,
passes all 68 of the author's own screen tests, and the desktop program builds. The working Jarvis on port 8010 was never touched.

#### 20.8.2 W90 - worktree, graft, merge, 26 non-frontend files [M]
Worktree C:\Users\Admin\OpenJarvis-upgrade, branch upgrade/a6dcf846 from 3df27c53. Local graft git replace --graft f2fcb30c
af21bc18 (replace ref local only, never pushed). git merge a6dcf846: 43 conflicted files as predicted by 20.7. 26 non-frontend
files resolved and staged per the per-file decisions in Vol 3A section G.9 row group "backend" (full per-file text: ARCHIVE-W83
s36). Two owner-reviewed departures from the W89 plan: (1) persona - author wins except native_openhands, because the author's
BaseAgent._build_messages lets prompt_builder.build() replace the system prompt and would drop the OpenHands tool template;
(2) sysmerge - the author's #823 folds only the agent and direct paths; ours also covers the managed-agent stream; kept pending
V&V. The venv question was left for owner approval (closed W92, 20.8.4 step 6).

#### 20.8.3 W91 - frontend hunk decisions for 14 of 17 files [M]
115 diff3 hunks on disk (the W90 record of 117 was a counting error). Owner decisions: Option A (careful merge), Option 1
(restore author code that our bc498a16 deleted, inside hunks), Option B (keep our CSP allowlist; App analytics stays out). Two
silent defects found that a green build would not catch: H-W91-4 (taking the author's sse.ts hunk would send every chat POST
twice) and H-W91-5 (the author's apiFetch is path-only; four Graystone calls kept their own getBase() prefix and would request
8010http://...). The 550B model was asked about lib.rs, ChatArea and InputArea (paid, 170 s, USD 0.087): useful leads, lib.rs
11 of 15 hunks mapped, InputArea answer unreliable and discarded. The W91 hunk specification (ARCHIVE s41) was SUPERSEDED in W92
by Method B; its per-hunk reasoning was reused as knowledge.

#### 20.8.4 W92 - what was found and what was done, in order [M]
STEP 0 (open): state verified; port 8000 cause measured: PID 3488 is iphlpsvc serving netsh portproxy 0.0.0.0:8000 ->
172.21.134.21:8000, so 8010 is a required Graystone port (Vol 3A G.9).
FINDING: byte-true copies of the 17 files and of both sides (git archive, never a PowerShell text pipe) showed the author's
MessageBubble has isLive, ResearchTimeline and citation plugins while the merged file had none of them - in CLEAN regions that
no hunk covered. Audit instrument: resolve every hunk to the author's side, diff against the author's real file; every
remaining line must be an intended Graystone change. Result: about 580 unexplained author lines missing inside the 17 files and
about 280 in 13 files that merged clean and were never reviewed (SettingsPanel 153, index.css 37, types/index.ts 37, XRayFooter
13, types/connectors.ts 12, UpdateChecker 7, Sidebar 7, SystemPanel 5, main.tsx 4, Layout 2).
HYPOTHESIS REFUTED: "the graft base af21bc18 is older than our root" - our root f2fcb30c already contained those features.
ATTRIBUTION: per-commit deletion totals root..HEAD: bc498a16 1867 deleted lines in 32 files (and the commit that removed
isLive), 383ccd5e 1668 (SetupScreen/auth, deliberate), 0389255b 705 (TTS engine, deliberate), b76b1b13 26 (PWA removed,
deliberate). ROOT CAUSE of bc498a16 (Vol 3A G.9, 20.8.5): a working folder holding older copies was committed wholesale.
METHOD B (owner W92-D2, "scrap test case if it does not work and does not impact our current build") - full mechanism 20.8.7.
Step 1 revert of bc498a16 on our side: 54 conflicts in 14 files, all decided (rules in 20.8.7). Step 2 merge with the author:
52 hunks in 15 files (was 115 in 17; SetupScreen and DataSourcesPage merged clean), all decided. Sandbox gate on identical
bytes: tsc -b 0 errors, vite build PASS, author vitest 12 files 68/68 PASS, exactly one chat POST in streamChat, zero apiFetch
calls with a getBase() prefix, R4 fixed (our ChatArea send now sets streamState.conversationId), R5 closed.
APPLY: the 103 files copied into the worktree from evidence\W92\W92-methodB-sandbox-result.zip (SHA256 DB38CD7E...61C5C3),
every file re-hashed against the manifest, 0 conflict markers, ThinkingCircle.tsx removed (W92-D1), staged; staged frontend
entries 66 reconciled exactly (60 source files differing from HEAD, 1 deletion, 5 author-changed non-source files).
WORKTREE GATE: npm upgraded 11.12.1 -> 11.20.0 (author engines need >=11.19.0, enforced by the author's .npmrc engine-strict);
npm ci exit 0 (784 packages), production build (tsc -b + vite) exit 0, vitest exit 0.
COMMITS on upgrade/a6dcf846 (none pushed): 533f9bfe merge (parents 3df27c53 and a6dcf846; graft ref deleted after the commit);
ac33e27f remove 36 tracked backup copies; 8eda697d uv.lock re-lock (W92-D5); 0dd22107 .python-version 3.12 (W92-D6); 6c9a2bc3
author defect AD-W92-1 fix; 93f96395 tauri.conf Graystone values (W92-D7). A pre-commit guard refused the first merge commit
because tsc -b had rewritten the tracked frontend\tsconfig.tsbuildinfo (H-W92-8); the file was restored from the index first.
STEP 6 VENV (owner approval W92): uv sync --python 3.12 --extra desktop --extra inference-cloud --extra inference-google
--group desktop-native in the worktree only - exactly the author's boot-time command plus the interpreter pin, so the author's
boot sync is a no-op instead of re-shaping the venv (H-W92-10). Author release tags (235) fetched into local refs only
(push.followTags unset; tags never pushed); version 1.0.5.dev161+gac33e27f; Python 3.12.10; openjarvis_rust imports (lead R1
closed); jarvis --version runs.
LOCK (W92-D5 P2): the merged uv.lock was stale against the merged pyproject; re-lock added 7 Graystone dependencies kept in s36
and bumped the STT stack. Production venv measured: ctranslate2 4.8.0, av 17.1.0, onnxruntime 1.26.0. Locked to ctranslate2
4.8.0 and av 17.1.0; onnxruntime stays at the author's 1.24.2 (a 1.26.0 pin collides with the author's python<3.11 constraint in
uv's universal lock). This box has no NVIDIA driver in use: local STT runs on CPU in production and upgrade alike (H-W92-14).
DESKTOP BUILD: tauri build --no-bundle exit 0, openjarvis-desktop.exe 23,270,912 bytes, after AD-W92-1 and W92-D7.

#### 20.8.5 Negative results (what things turned out NOT to be, and how that was established)
The graft base is not the cause (root f2fcb30c already had isLive, ResearchTimeline, citations). evidence\W91 held 5 files, not 6
(the BRIEF counted two files stored elsewhere). bc498a16 is not only damage: it also added features still live at HEAD (Reconnect
button, SetupScreen remote text, remote-mode lib.rs, frontendDist and updater settings) - the first four were accepted as
removed (W92-D4), the last two were restored (W92-D7). The comment "Tauri transcribe path does not exist in Rust" was wrong:
transcribe_audio is defined and registered in both lib.rs versions. Kokoro-onnx is not used by this repository's code (TTS is
served by the kokoro-tts unit on 172.16.33.201); its absence from the upgrade venv is harmless. The resolve-45 bundle mojibake
and bc498a16's config.toml mojibake share one mechanism: PowerShell text round-trips. A first onnxruntime 1.26.0 lock pin was
refused by uv; nothing was written.

#### 20.8.6 Hazards recorded W92
H-W92-1 our send never set conversationId (fixed). H-W92-2 clean regions silently carry our post-root deletions; every merged
file needs the take-theirs audit. H-W92-3 the author's boot runs uv sync in the project root every start; root = walk up from
the exe, then C:\Users\Admin\OpenJarvis; a test exe must pin OPENJARVIS_ROOT. H-W92-4 npm >= 11.19.0. H-W92-5 bc498a16 root
cause. H-W92-6 git archive output is CRLF (autocrlf); normalize before comparing. H-W92-7 Compress-Archive writes backslash
paths. H-W92-8 any tsc -b dirties the tracked tsbuildinfo. H-W92-9 Windows PowerShell 5.1 mangles embedded double quotes in
native-command arguments. H-W92-10 a manual uv sync must equal the author's boot command. H-W92-11 never pipe a long native
command to Select-Object -Last; Tee-Object to a log. H-W92-12 Python must stay 3.12 (inference layer). H-W92-13 closed (see
20.8.5). H-W92-14 no NVIDIA driver on this box. H-W92-15 PowerShell 5.1 ConvertFrom-Json cannot parse package-lock.json (empty
root key). H-W92-16 production and the upgrade share C:\Users\Admin\.openjarvis (config, skills, memory.db) - POAM-68.
H-W92-17 SDP edits go to main; the upgrade branch holds an older docs\SDP.

#### 20.8.7 Method B and the sandbox instrument - setup and flow, gate by gate
PLAIN: an old save overwrote good pages with old pages. Instead of repairing page by page, we took our history, undid exactly
that one save, then merged with the author. Every place where our later work touched what the bad save wrote showed up as a
visible question instead of a silent loss. Nothing touched the spare copy until the practice area passed every check.
GATE 1 EXTRACT (Windows host, git, local disk): git archive --format=zip -o <absolute path> <rev> frontend [configs] for each
side - HEAD, a6dcf846, af21bc18 and f2fcb30c (--no-replace-objects), bc498a16^, bc498a16; git diff --output=<absolute path> for
the bc498a16 patch (863,774 bytes). Git writes the bytes; no PowerShell text pipe. SHA256 printed for every artifact.
GATE 2 TRANSFER: one zip per upload; the sandbox verifies SHA256 before use; Python zipfile extraction (H-W92-7).
GATE 3 NORMALIZE: CRLF to LF on every side (H-W92-6); worktree files are LF.
GATE 4 SIMULATE: merge(base, ours, theirs): identical sides shortcut, one-side-changed shortcut, modify/delete reported,
otherwise git merge-file -p --diff3. VALIDATION: the simulator's output equalled the real worktree bytes for all 17 conflicted
files (17 of 17) before any decision was made on its output.
GATE 5 RESOLVE: resolve.py consumes a per-file specification of per-hunk choices (ours, theirs, both in either order, explicit
lines, or a function); it refuses an undecided hunk or a hunk number that does not exist. Clean-region edits are exact
(old, new, expected count) replacements with the count asserted. Output asserted valid UTF-8 with zero markers.
STEP 1 RULES: (R-S1-a) where HEAD only repaired bc498a16's mojibake, restore the original text; later deliberate Graystone work
wins; COMBINE where both sides are real (MessageBubble option buttons with author isLive/citations; ChatArea attachment chips
with author isLive and research-aware dots; SettingsPage audio probe with the author's speech-backend indicator; index.css);
InputArea is a later whole-file Graystone rewrite - HEAD for all hunks; store signature keeps the author's research parameters
at positions 7-8 and moves our persist to 9 with one caller edit; ThinkingCircle dropped (W92-D1).
STEP 2 RULES: W91 reasoning reused; lib.rs = author file plus JARVIS_PORT 8010 (W92-D3); InputArea all ours (verified
byte-identical to our file); App analytics calls removed (Option B); four getBase() prefixes stripped (H-W91-5, including
confirmTool); our duplicate cloud-key effect in CommandPalette removed (C-W92-1).
GATE 6 AUDIT: (a) HEAD lines lost that bc498a16 did not add - each explained; (b) bc498a16-deleted author lines still missing -
each a recorded decision; (c) bc498a16 additions still live at HEAD that the method removes - produced the W92-D4 list.
GATE 7 BUILD: author frontend tree plus the merged files; npm 11 in the sandbox; npm ci; tsc -b; vite build; vitest run.
PACKAGE: evidence\W92\W92-methodB-sandbox-result.zip = final\ (103 files) + MANIFEST (SHA256, size, path) + tooling\ (all
scripts and specifications). GAP FOUND LATER: the sandbox gate ran vite, not tauri build, so it could not see the tauri.conf
pairing that Method B split (frontendDist vs the build script) - caught in the worktree by tauri build and fixed by W92-D7.
Lesson: a gate must build every artifact the merge touches.
Owner pin (W92): Jarvis and the Cody infrastructure agent need this sandbox capability (Vol 2 / program goals).

#### 20.8.8 Status at W92 (measured)
Merge committed and building (web, tests, desktop exe). Not yet done, in order: the confirmation gate at the author's new
executor sites (POAM-67); separating the test instance's home directory from production's (POAM-68); serving on 8011 with
OPENJARVIS_ROOT pinned (H-W92-3) and the inference source set in the author's setup screen (custom, engine ollama, host
http://172.16.33.200:11434); V&V; the four VERIFIED requirements; GitHub Actions check (POAM-74); switch and push to both remotes.

### 20.9 POAM-67 - the confirmation gate at every tool-executor site of the upgrade (W93, 2026-09-26) [M evidence\W93\step1a..1i; R upgrade/a6dcf846]
#### 20.9.1 Plain language
Some of Jarvis's tools can change things that matter: run a command, commit code, move mail to the trash. Before one of those
runs, Jarvis has to ask. The part of Jarvis that runs tools is called an executor, and every executor has one slot for
"who do I ask". In the author's newest code, a few new executors had that slot filled with a note that just says "yes, always"
and leaves no trace. That is like a door with a doorbell wired straight to the lock: the door opens and nobody knows anybody
rang. W93 went through every executor in the upgrade and did one of three things. Where a person is sitting at the keyboard,
the slot now really asks them, and "no" means no. Where the author deliberately chose "yes, always" (and a person chose it by
typing --yes), the "yes" stays but is now written down with a name, so the record can tell an automatic yes from a person's yes.
Where Graystone had already named the automatic yes and the merge quietly lost the name, the name was put back. One more fix:
at three keyboard prompts, when you answered "no", Jarvis was told "the user did not answer, ask again" - so it could keep asking
after you refused. Now your "no" is recorded and Jarvis is told you refused. Nothing here touched the working Jarvis on port 8010.

#### 20.9.2 How the gate decides, and why only some sites matter [R W93 tools\_stubs.py:600-700 at da752fbd]
The executor asks only when BOTH are true: the tool declares requires_confirmation (and its per-call predicate agrees, 6.2), and
the executor was built with interactive=True AND a callback in the slot. If either construction condition is missing, a
confirmable tool is refused outright (fail-closed). So an executor with an empty slot is safe; an executor whose slot holds an
approve-all function is the only kind that can let a confirmable tool run without a person. When a callback returns False, the
executor re-reads confirm_registry: a recorded DENIED is reported to the model as "denied by user"; no recorded decision is
reported as TIMEOUT - "the user did not deny it, ask the user again" (openjarvis-confirm-resolved-v1). CONTRACT (H-W93-4): every
callback that can return False must write its decision into confirm_registry, or a refusal is reported as a timeout.

#### 20.9.3 The inventory instrument - setup and flow [M evidence\W93\step1a-poam67-inventory.log]
Host: the Windows box, Windows PowerShell 5.1, run from the main repo root. Input: every *.py under
C:\Users\Admin\OpenJarvis-upgrade\src (worktree at 93f96395). Mechanism: Select-String with the pattern
ToolExecutor\( | confirm_callback | _confirm_callback | stream_tool_executor | ConfirmPolicy | confirm_registry |
requires_confirmation. Output: file:line: text to the log; every matching file copied WHOLE with its relative path into
evidence\W93\poam67-stage and zipped (evidence\W93\W93-poam67-files.zip, 182,419 bytes, 28 files, 88 hits). The zip was read
whole in the analysis sandbox (not piecemeal). A second instrument (step1b) printed the same pattern from main's committed files
(git show main:<path>, no working-tree text round trip) to establish what production had before the merge; step1c printed
main:agent_manager_routes.py 1240-1275 so the restored text could be verbatim. Encoding: git object bytes and UTF-8 source; the
PowerShell console renders the author's UTF-8 em dash as three characters (display only, file bytes unchanged).

#### 20.9.4 Site-by-site record: before, after, options, risks, decision, evidence
Every executor construction in the upgrade, measured W93. Human present = could a person answer a prompt on this path.

| Site token | Where (upgrade) | Path | Human | Before (author a6dcf846 / merge) | Main (production) before merge | After W93 | Commit |
|---|---|---|---|---|---|---|---|
| managed-agent-tool | server\agent_manager_routes.py:1326 stream_tool_executor | managed-agent SSE stream (_stream_managed_agent, execution path 2) | desktop user, but no prompt channel on this path | bare lambda _prompt: True, no trace | ConfirmPolicy site=managed-agent-tool (main:1256), fresh executor per call | ConfirmPolicy site=managed-agent-tool restored VERBATIM (reason, human_present=False) | 13dbd764 |
| cli-ask-skill | cli\ask.py:600 pipeline_executor (SkillPipelineConfirmGate) | jarvis ask with skills enabled; skill steps execute through this executor | YES, terminal | bare lambda prompt: True - skill steps bypassed the agent's TerminalConfirmGate | site did not exist | real terminal gate, deny by default, non-TTY denies without reading, decision recorded | 6edfe885 |
| cli-agent-ask-yes | cli\agent_cmd.py:845 (--yes, default ON) | jarvis agent ask | YES, the operator chose --yes | bare lambda _prompt: True, no trace | site did not exist | ConfirmPolicy site=cli-agent-ask-yes, human_present=True: same approval, now logged | da752fbd |
| cli-agent-ask | cli\agent_cmd.py:857 (--no-yes) | jarvis agent ask --no-yes | YES | click.confirm, decision NOT recorded (a no reached the model as TIMEOUT) | site did not exist | TerminalConfirmGate(site="cli-agent-ask") | da752fbd |
| cli-skill-run | cli\skill_cmd.py:191 | jarvis skill run | YES | click.confirm, decision NOT recorded | no executor on main | TerminalConfirmGate(site="cli-skill-run") | da752fbd |
| cli-chat | cli\chat_cmd.py:240 | jarvis chat | YES | input() prompt, decision NOT recorded | same defect on main (chat_cmd.py:123) | TerminalConfirmGate(site="cli-chat"); dead _confirm removed | da752fbd |
| cli-ask | cli\ask.py:650 agent executor | jarvis ask | YES | TerminalConfirmGate (Graystone W61, kept by the merge) | same | unchanged; class gained an optional site= keyword, default token still cli-ask | da752fbd |
| chat-agent-live | cli\serve.py:520 _server_confirm_callback | server chat agent (path 1b) | YES, desktop Approve/Deny | real gate (Graystone Defect 6, kept) | same | unchanged | - |
| dr-sse-stream, imessage-daemon, sendblue-bridge | agent_manager_routes.py:1035, :1942, :2031 | deep research SSE, channel daemons | no | ConfirmPolicy (Graystone W56, kept) | same | unchanged | - |

Fail-closed constructions (no callback; confirmable tools refused; no action) [R W93]: cli\serve.py:811 scheduler executor;
agents\rlm.py:246 REPL executor; system\builder.py:219 and :253; mcp\server.py:78; security\runtime.py:148
execute_secured_tool; learning\intelligence\orchestrator\environment.py:51; skills\manager.py _NullToolExecutor.
agents\executor.py:520 (AgentExecutor) forwards whatever callback its caller sets - that is how the cli-agent-ask sites reach
the managed agent. deep_research.py and the other agent classes only pass their callback parameter through.

SITE A - managed-agent-tool. Author intent: tools the user selected for a managed agent run without prompting (the author's own
comment on main: selecting the tool in the wizard is the confirmation). Graystone intent on main: the same approval, attributed.
What happened: the merge took the author's rewrite of this block (one request-local executor with taint seeding via
begin_session - kept, it is an improvement) and with it the author's bare lambda; our named policy vanished in a region with no
conflict marker (the H-W92-2 pattern). Options: (1) restore ConfirmPolicy - behaviour unchanged, attribution back; (2) remove the
callback - fail-closed, a posture main never had, breaks shell_exec/apply_patch/mailbox tools on managed agents; (3) the real
gate - NOT POSSIBLE here: stream_tool_executor.execute() is called inside async def generate() (upgrade :1437/:1584 at da752fbd; main
:1062/:1264), i.e. on the event-loop thread, while the answer arrives by POST /v1/tools/confirm on that same loop; a blocking
wait would freeze the loop, no answer could ever be served, and every prompt would expire as TIMEOUT (H-W93-1, POAM-80).
Decision: option 1, verbatim from main:1256 (the reason text says "toolkit bind enforced above", describing main's layout; the
bind openjarvis-toolkit-bind-v1 is still present in the upgrade and still runs before dispatch). Risk: none to behaviour.
Verify [M W93 step1d]: AST OK; site count 1; bare lambda count 0; ConfirmPolicy import present; module imports.

SITE B - cli-ask-skill. Author intent: skill pipelines run their steps unprompted. Effect: a skill (65 files in the shared home,
several third-party - POAM-78) could run shell_exec, git_* or a destructive mailbox tool that the agent itself must ask about.
Options: (1) the real terminal gate with its own site token; (2) ConfirmPolicy - attribution only, bypass kept. Risk of (1):
scripted, non-TTY runs of a skill that uses a confirmable tool are now denied; that is the posture W61 already chose for the
agent on this same command. Decision: option 1 [S W93 - owner ran the offered block and approved the result].
Verify [M W93 step1f harness]: non-TTY -> not run, "denied by user"; typed n -> not run, "denied by user"; typed y -> ran;
POLICY lines DENY_NO_TTY, WAIT, DENY, WAIT, APPROVE under site=cli-ask-skill, every decision registry=recorded.

SITE C - cli-agent-ask-yes. Author intent: explicit and documented in the option help - --yes is the default for
non-interactive CLI use. Options: (1) attribute with ConfirmPolicy (behaviour unchanged); (2) flip the default to --no-yes
(changes the author's user experience). Decision: option 1, staying true to the author's intent. Residual risk recorded, not
changed: a person who types a destructive request on jarvis agent ask without --no-yes is auto-approved (POAM-81).
Verify [M W93 step1h]: ConfirmPolicy run -> tool ran, POLICY decision=AUTO_APPROVE site=cli-agent-ask-yes.

SITE D - cli-agent-ask, cli-skill-run, cli-chat (integration defect, found W93). Author intent: ask the person, deny by default -
these three already did that. Defect: none recorded the decision, so under Graystone's three-way result contract (20.9.2) a
person's "no" reached the model as TIMEOUT "ask again". Symptom: after a refusal the model may re-request the same tool or tell
the user they did not answer. Trigger: any of the three CLI commands, a confirmable tool, the person answers no. Origin: the
author's callbacks predate Graystone's registry contract; not an author defect in isolation. The chat_cmd instance predates the
merge (main:123) and remains in production until the switch (POAM-82). Fix: TerminalConfirmGate with a per-site token (one
optional site= keyword added to the class; default unchanged). Side effect (improvement): a non-TTY or end-of-input now denies
cleanly instead of raising click.Abort or EOFError. Cleanup register: the dead chat _confirm function removed (backup
evidence\W93\bak\chat_cmd.py.W93-pre-CD.bak). Verify [M W93 step1h]: AST site lists exactly [cli-agent-ask], [cli-agent-ask-yes],
[cli-skill-run], [cli-chat]; zero approve-all lambdas in the three files; four modules import; defaults cli-ask and
cli-ask-skill unchanged; 12 of 12 gate cases PASS plus the ConfirmPolicy case.

#### 20.9.5 The non-interactive gate harness - setup and flow, gate by gate (reusable instrument)
Purpose: prove a confirm callback's behaviour through the REAL ToolExecutor without a person, a server, a port, or the network
(owner rule 08/22: tests run to completion on their own).
GATE 1 HOST: Windows box; the worktree venv interpreter C:\Users\Admin\OpenJarvis-upgrade\.venv\Scripts\python.exe (3.12.10);
the script is an ASCII PowerShell single-quoted here-string piped to python on stdin; working directory pushed to the worktree
so the editable package resolves to the upgrade source.
GATE 2 ISOLATION: LOCALAPPDATA is set to C:\Users\Admin\OpenJarvis\evidence\W93\harness inside the process BEFORE the first
dispatch-logger call; the dispatch logger derives its path from LOCALAPPDATA, so the harness writes
evidence\W93\harness\OpenJarvis\logs\dispatch.log and production's dispatch.log is untouched. confirm_registry is process memory.
GATE 3 CONSTRUCTION: a dummy BaseTool w93_dummy with requires_confirmation=True (per-call predicate default True) and an execute
that increments a side-effect counter; a real ToolExecutor(interactive=True, confirm_callback=<gate under test>).
GATE 4 INPUT: injected streams replace the terminal - NoTTY (isatty False, empty), TTY with "n\n", TTY with "y\n"; stderr is a
StringIO that captures the prompt text.
GATE 5 DISPATCH: executor.execute(ToolCall(name="w93_dummy", arguments="{}")) runs the full chain (rate limit, boundary,
capability, taint, then the gate): register -> CURRENT_CONFIRM_ID set -> callback -> registry resolve -> three-way result.
GATE 6 ASSERT: success flag; whether the tool body ran (counter); that a refusal says "denied by user" (DENIED, not TIMEOUT).
GATE 7 READ-BACK: the harness dispatch.log is read and each POLICY line reduced to (site, decision).
STATIC CHECK: an AST walk of each patched file lists every TerminalConfirmGate(...) and ConfirmPolicy(...) call and its site=
constant, so the wiring is proven without executing the CLI command.
PATCH MECHANISM (all W93 patches): Python in the worktree venv; every anchor must occur exactly once and all anchors are checked
before any file is written (a miss aborts with nothing written); the result must parse (ast); the original is copied to
evidence\W93\bak\<file>.W93-pre-<site>.bak before the write; files are read and written UTF-8 with newline="" so LF is preserved.

#### 20.9.6 Negative results (what things turned out NOT to be, and how that was established)
- The deep-research agent is NOT a bypass site: deep_research.py only passes its callback through, and all three of its
  construction sites already carry ConfirmPolicy (dr-sse-stream, imessage-daemon, sendblue-bridge) [R W93].
- POAM-67 as written in W92 named "two more sites in agent_manager_routes"; measured, there is ONE bare lambda there (:1330);
  the other hits are the three ConfirmPolicy sites above.
- The nine other executor constructions are NOT exposures: none has a callback, so confirmable tools fail closed.
- The mailbox_tools.py docstring citing cli/serve.py:310 (the callback now sits at :520) is NOT a defect: it is a dated W49
  status paragraph, and SDD section 1 records that a line cite is valid as of its window. Left unchanged.
- The TIMEOUT misreport at chat_cmd was NOT introduced by the upgrade: main carries it (main:123).
- A real gate at site A was NOT rejected by preference; it is structurally impossible while execute() runs on the event loop.

#### 20.9.7 Hazards recorded W93
H-W93-1 the managed-agent stream executes tools on the event-loop thread; no blocking gate can be placed there without moving
execution to a worker (asyncio.to_thread), and any slow tool already stalls the loop for every request (POAM-80).
H-W93-2 dispatch.log lives at %LOCALAPPDATA%\OpenJarvis\logs\dispatch.log - a second location shared by production and the
upgrade instance, beyond C:\Users\Admin\.openjarvis (POAM-68).
H-W93-3 SkillPipelineConfirmGate and the per-site instances print repr "<TerminalConfirmGate site=... default=DENY>" (inherited
__repr__); the site token is correct; cosmetic.
H-W93-4 callback contract: a callback that can return False must record its decision in confirm_registry, or the refusal is
reported to the model as a TIMEOUT.

#### 20.9.8 Configuration management and rollback [M W93]
Commits on upgrade/a6dcf846, each pushed to gitlab only (origin excluded until POAM-74): 13dbd764 site A; 6edfe885 site B;
da752fbd sites C and D. Each patch was verified before its commit, and each commit was its own block with the staged set
guarded to the named files. Backups: evidence\W93\bak\agent_manager_routes.py.W93-pre-A.bak, ask.py.W93-pre-B.bak,
{ask,agent_cmd,skill_cmd,chat_cmd}.py.W93-pre-CD.bak. Undo one site: git -C C:\Users\Admin\OpenJarvis-upgrade revert <hash>.
Production (main, 8010, PID 27988) was not touched.

#### 20.9.9 Status and program goal
POAM-67 closed on the upgrade branch: no executor in the upgrade can approve a confirmable tool without either a person's
recorded answer or a named, logged policy. Remaining before 8011 is served, in order: POAM-68 (separate home, now including the
dispatch.log location), the ARCHIVE s37 post-merge items, serve on 8011, V&V. Program goal: VERIFIED 4/28 unchanged; W93 removed
a precondition to serving the upgrade that the remaining requirements are built on.

### 20.10 POAM-68 - separating the upgrade instance's home, logs and port from production (W93, 2026-09-26) [M evidence\W93\step2a..3d; R upgrade/a6dcf846 e9acdacd, 70a74188]
#### 20.10.1 Plain language
Jarvis keeps its memory, settings, skills and diaries in one home folder. The working Jarvis and the upgraded copy were going
to share that folder, the same diary folder, and the same door number (port 8010). Two programs writing one diary at once
mix their entries; two programs on one door means the new screen can quietly talk to the old Jarvis and every test would be a
lie. The author already built a switch to give Jarvis a different home (OPENJARVIS_HOME), but three parts ignored it: the
desktop program's own settings writer, Graystone's four diaries, and one fallback in the code tool. We taught all three to
honor the switch, and we added the port switch the author had written down as a to-do. With no switch set, everything behaves
exactly as before, so the working Jarvis is unchanged.

#### 20.10.2 How it was measured (instruments) [M]
STEP 2a inventory: Select-String over every *.py under the worktree src and every *.rs under frontend\src-tauri\src for
get_config_dir | DEFAULT_CONFIG_DIR | OPENJARVIS_* | .openjarvis | LOCALAPPDATA | APPDATA | Path.home() | expanduser( ; plus the
author's *.md docs for home mentions; 158 code files zipped whole (evidence\W93\W93-home-files.zip, 686,490 bytes) and read in
the analysis sandbox. STEP 2b inventory: production home top level (name, size or file count, last write), config.toml lines
that carry paths, hosts or ports only (cloud-keys.env and connector credentials never opened), inference.json presence, the
worktree CSP, and every hard-coded port or base-URL source in the frontend and Tauri code. STEP 3a: the four frontend files plus
lib.rs and tauri.conf.json zipped whole with SHA256, so the Rust patch was written against exact bytes and refused otherwise.

#### 20.10.3 Findings [R/M W93]
AUTHOR MECHANISM: core\paths.py get_config_dir(): OPENJARVIS_HOME > XDG_DATA_HOME\openjarvis > ~\.openjarvis; refuses a home
inside the source tree (ConfigurationError); DEFAULT_CONFIG_DIR is fixed at import (config.py:62), so the variable must be set
before the process starts. Documented in docs\getting-started\configuration.md:25-57. About 150 Python sites use it.
BREAK 1 (author defect AD-W93-1, Vol 3A G.10): lib.rs hard-coded <HOME or USERPROFILE>\.openjarvis at four sites -
legacy_cloud_keys_path, inference_config_path, set_engine_host_in_config (writes [engine.<x>] host into config.toml during
setup), conversation_path (macOS overlay). The backend the exe spawns inherits the environment and honors OPENJARVIS_HOME, so
the setup screen would write the Ollama host into PRODUCTION's config.toml while the separated backend read its own file.
BREAK 2 (author design): lib.rs:10 const JARVIS_PORT 8010 was compiled in. At start the exe probes 127.0.0.1:<port>/health
and, if a healthy server answers, ATTACHES to it instead of spawning (lib.rs:1302-1388, #455). Launched beside production, the
upgrade exe would silently use production's backend (H-W93-5). The author's own comment asks for a port override (TODO #455).
BREAK 3 (Graystone): backend.log (cli\serve.py:148), engine.log (engine\ollama.py:566), agent.log (agents\native_openhands.py:414)
and dispatch.log (tools\_stubs.py:223) were written to %LOCALAPPDATA%\OpenJarvis\logs regardless of home. LOCALAPPDATA itself
must not be redirected: uv's cache and the exe's binary search (lib.rs:203-220) depend on it.
BREAK 4 (Graystone W83): code_interpreter _oj_workdir fallback hard-coded Path.home()\.openjarvis\workspace (only on an
exception from load_config).
FRONTEND: getBase() (api.ts:71) order is localStorage openjarvis-settings.apiUrl, then VITE_API_URL, then the Rust value from
invoke('get_api_base') (api.ts:52 -> lib.rs:1687 api_base), then a fallback http://127.0.0.1:8010. The CSP connect-src already
allows http://127.0.0.1:* and ws://127.0.0.1:*, so no CSP change is needed. Fallbacks that still name 8010: api.ts:58,
useTauriApi.ts:30 (browser fallback), SettingsPanel.tsx:15 (default saved setting), AdminPanel.tsx:276 (Start button runs
serve --port 8010).
WEBVIEW PROFILE (H-W93-6): both exes carry identifier com.openjarvis.desktop and set no data directory, so they share one
WebView2 profile, including localStorage. A saved apiUrl from the production UI would override the Rust base in the upgrade UI.
PRODUCTION HOME (measured): config.toml 915 bytes holds no absolute paths; [engine.ollama] host http://172.16.33.200:11434;
[server] host 0.0.0.0 port 8010 (the production backend listens on all interfaces - observation, recorded for the end-of-build
review). inference.json absent. Largest items: memory.db.old 21,356,789,760 bytes (not to be copied), skill-cache 4,809 files
(regenerable cache), skills 65 files, workspace 7 files, connectors 2 files (IMAP credentials), cloud-keys.env.

#### 20.10.4 Options, risks and the owner decision [S W93: "B brother"]
A - backend only on 8011 (uv run jarvis serve --port 8011 with OPENJARVIS_HOME): fixes 3 and 4 only; low risk; but no UI V&V
(TTS/STT, Approve/Deny buttons, persona in the app) until the switch, which then needs a production outage.
B - full side by side: A plus two Rust changes (home resolver mirroring core\paths.py; OPENJARVIS_PORT with default 8010), then
a rebuild. Full UI V&V without downtime; with no variables set production behaves exactly as today. Risk: one more Rust change
and a rebuild, gated by the author's tests. CHOSEN.
C - stop production for V&V and run the upgrade on 8010 with production's home: no separation code, but downtime and V&V
against live family data and live config.

#### 20.10.5 What was changed, and the flow gate by gate after the change
e9acdacd (Python): new core\log_paths.py get_log_dir() (openjarvis-log-home-v1): OPENJARVIS_HOME or XDG_DATA_HOME set ->
get_config_dir()\logs; neither -> %LOCALAPPDATA%\OpenJarvis\logs exactly as before. The four loggers call it. code_interpreter
fallback uses get_config_dir()\workspace. Side effect: engine.log's fallback when LOCALAPPDATA is missing moves from the current
directory to the user home (never occurs on Windows).
70a74188 (Rust, lib.rs): DEFAULT_JARVIS_PORT 8010 + parse_jarvis_port + jarvis_port() (OnceLock, reads OPENJARVIS_PORT once;
unset, empty, non-numeric or below 1024 -> 8010), used at all 19 code sites (openjarvis-desktop-port-v1); resolve_openjarvis_home
+ openjarvis_home() with the core\paths.py precedence, used at the four hard-coded sites (openjarvis-desktop-home-v1). The
author's TODO comment is left in place.
FLOW (Windows box, all local unless stated):
GATE 1 LAUNCH: the operator's PowerShell session sets OPENJARVIS_ROOT (worktree), OPENJARVIS_HOME, OPENJARVIS_PORT and
WEBVIEW2_USER_DATA_FOLDER, then starts the exe from the worktree target. Environment variables are inherited by every child.
GATE 2 EXE (Rust): find_project_root -> OPENJARVIS_ROOT; jarvis_port() -> 8011; health probe GET http://127.0.0.1:8011/health
(HTTP/1.1, TCP loopback) finds nothing and proceeds to spawn; setup writes inference.json and the engine host into
openjarvis_home()\config.toml (TOML UTF-8).
GATE 3 SPAWN: uv sync (author boot, H-W92-3) then uv run jarvis serve --port 8011 in the worktree; the child inherits
OPENJARVIS_HOME.
GATE 4 BACKEND (Python): config.py import fixes DEFAULT_CONFIG_DIR = get_config_dir() = the separate home; every database,
skills, persona file and credential resolves there; get_log_dir() puts backend, engine, agent and dispatch logs in <home>\logs.
GATE 5 UI: WebView2 loads the static frontend; getBase() -> invoke get_api_base -> http://127.0.0.1:8011 (unless a localStorage
apiUrl overrides it, H-W93-6); chat POST and SSE on HTTP 127.0.0.1:8011 (JSON and text/event-stream, UTF-8); confirm events on
WS ws://127.0.0.1:8011/v1/agents/events; answers POST /v1/tools/confirm on the same port.
GATE 6 INFERENCE: backend -> Ollama HTTP http://172.16.33.200:11434 (JSON UTF-8), unchanged.

#### 20.10.6 Verification [M W93]
Log harness (evidence\W93\step2d): a child Python process started with OPENJARVIS_HOME = evidence\W93\harness-home and
SyntaxWarning promoted to an error wrote a unique marker through all four real loggers and forced the code_interpreter
fallback: all four files and the workspace resolved under harness-home, the marker was in all four, the resolver with no
variables returned C:\Users\Admin\AppData\Local\OpenJarvis\logs, and production's four logs did not contain the marker. PASS.
Rust (evidence\W93\step3b, step3c): the patch script refused to run unless lib.rs had the reviewed SHA256 (6d6968ce...), made
exactly 19 port replacements and 4 home replacements, left no hard-coded .openjarvis join, and produced 82bd8053...;
cargo test graystone_w93 4 of 4 (default port, valid override, invalid values, home precedence); cargo test --lib 51 of 51
including all 47 author tests.
NOT YET VERIFIED: the rebuilt exe (the exe in the worktree target is from 93f96395 and predates both commits - do not run it);
WebView2 profile separation by WEBVIEW2_USER_DATA_FOLDER (to be measured at first launch).

#### 20.10.7 Negative results
- No CSP change is needed (127.0.0.1:* already allowed). No TypeScript change is needed on the main path (the base comes from Rust).
- config.toml holds no absolute paths; production has no inference.json.
- The first log-harness run FAILED for two instrument faults, not product faults: a docstring escape in the new file written by
  the patch script (fixed before commit; the fix compiles with warnings as errors) and `from openjarvis.cli import serve`
  returning the click command that cli\__init__ exports under that name (H-W93-7). The code edits were correct on the first run.

#### 20.10.8 Hazards recorded W93 (continued)
H-W93-5 a desktop exe attaches to any healthy backend already on its port; always set OPENJARVIS_PORT for a second instance and
check /health is free first. H-W93-6 shared WebView2 profile (identifier com.openjarvis.desktop): a saved apiUrl in localStorage
overrides the Rust base. H-W93-7 `from openjarvis.cli import serve` yields a click Command, not the module; use
importlib.import_module("openjarvis.cli.serve"). H-W93-8 production config binds the backend to 0.0.0.0 (observation).

#### 20.10.9 Status
POAM-68 code complete on upgrade/a6dcf846 (e9acdacd, 70a74188, gitlab only). Remaining in order: rebuild the exe (tauri build
--no-bundle; restore tsbuildinfo, H-W92-8); owner decision on what to seed into the separate home (memory.db copy, persona
files, skills, IMAP connectors, cloud keys - each with risk); launch per 20.10.5 and measure the WebView2 profile location;
V&V. Program goal: VERIFIED 4/28 unchanged; the upgrade can now be exercised without touching production's data or port.
