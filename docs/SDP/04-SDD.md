# VOL 4 - SOFTWARE DESIGN DESCRIPTION (SDD)
Governing DID: DI-IPSC-81435 (verify, GAP-002). v0.2 DRAFT 2026-09-23 (W82), W83 update 2026-09-24 (sections 11, 14, 16 incl. 16.4), harvested from ARCHIVE-W42..W81 plus W82 measurement.
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
SIDE FINDING (POAM-62): the trace read-back routes open a NEW TraceStore per request and never close it -
agent_manager_routes.py:1961-1965 (list_traces) and :1986-1990 (get_trace); api_routes.py:813-820 (feedback, which also
hard-codes DEFAULT_CONFIG_DIR/traces.db instead of config.traces.db_path). /v1/traces uses app.state.trace_store correctly
(api_routes.py:307-331). Effect: one SQLite connection left open per call (Windows file handles accumulate until garbage
collection). Origin (author vs Graystone) not yet established - both files differ from af21bc18.
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
