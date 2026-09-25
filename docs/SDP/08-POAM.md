# VOL 8 - PLAN OF ACTION AND MILESTONES (POA&M)
v0.2 DRAFT 2026-09-23 (W82), W83 update 2026-09-24 (POAM-40..56, CLOSED rows), W87 update 2026-09-24 (POAM-53 partial, POAM-54 note). Harvest of W42-W83; v0.1 items kept with status updated. Control mapping is an engineering
assessment; the assessor and AO make the determination. Owner ruling W82 (DD-14): dormant findings are recorded and assessed at
the end-of-build security review, not changed piecemeal.

| ID | Weakness | Controls | Source | Status |
|---|---|---|---|---|
| POAM-01 | Agent replies buffered server-side on path 1b | - | W70 [M] | Open (Option A not built) |
| POAM-02 | Voice starts late (F-W71-VOICE-LATE) | - | W71 | Improved W67 (gate 5.0 s -> 1.5-2.3 s); open |
| POAM-03 | Ollama stream uses sync client in async code | SC-5 | W71 [R] | Open |
| POAM-04 | Telemetry lost on stream_full path | AU-2 | W71 [R] | Open |
| POAM-05 | Input redaction bypassed on stream_full; no RETRY400 log | SI-4 | W71 [R] | Open |
| POAM-06 | Rollback points and out-of-git config on one disk | CP-9 | W71 [M] | Open (GAP-040) |
| POAM-07 | No author baseline | CM-2 | W71 | CLOSED W73 (af21bc18) |
| POAM-08 | No requirements baseline | - | standing | CLOSED W75 (RTM ratified) |
| POAM-09 | Frontend debug logs unreadable ([PUMPDBG], [STOP]) | AU-2 | W68-W69 | Open |
| POAM-10 | Credential exposure 08/01 - rotation unverified | IA-5 | 08/01 [S] | Verify |
| POAM-11 | Model and voice traffic plaintext on the lab segment (IF-02, IF-02a/b, IF-03a) | SC-8 | W81 | Open |
| POAM-12 | Ollama and Kokoro APIs unauthenticated both ways | IA-9, IA-3 | W81 | Open |
| POAM-13 | Confirmation WebSocket accepts unauthenticated clients (authed=False with api_key_set=True); any loopback client can answer a gate | AC-3, IA-2 | W50, W81 H-W81-6 | Open; owner deferred socket auth 08/29 |
| POAM-14 | Config says [server] host 0.0.0.0; runtime binds 127.0.0.1 via an unmapped override | CM-6 | W77, H-W80-4 | Open (safe today) |
| POAM-15 | Base predates upstream security fixes #415 RCE, #416 WS auth, #417 deploy auth | SI-2, RA-5 | H-W73-BEHIND | Open - assess each against our tree |
| POAM-16 | AuthMiddleware possibly disabled in app.py (`if False`) - 550B claim, unverified | AC-3 | H-W74-AUTHOFF | Verify (BIND-ASSERT api_key_set=True observed) |
| POAM-17 | Auto-approve on managed-agent tool loop (wizard selection = consent); live if shell_exec/apply_patch selected | AC-6, AU-12 | W52-W56 | Open - attributed by ConfirmPolicy; owner ruling needed |
| POAM-18 | cli-ask auto-approves with a human present (TerminalConfirmGate designed W61) | AC-3 | W56-W61 | Verify build |
| POAM-19 | Gate prompt lacks count/scope of mail affected | AC-3 (informed consent) | W60 | Open |
| POAM-20 | Protected senders not applied on direct UID path | AC-3 | W61 | Open |
| POAM-21 | file_read unconfined; workspace security unreviewed | AC-6 | H-W78 | Open (owner: after function) |
| POAM-22 | Rust shell_exec bridge ignores sanitized env and timeout, always returncode 0 | SI-10 | H-W78-RUSTSHELL, H-W79-RUSTBUILD | Open (only if Rust build lands) |
| POAM-23 | Analytics/PostHog code with hardcoded key present (disabled by config) | SC-7, SA-9 | H-W78-ANALYTICS | Open - owner ruled remove |
| POAM-24 | Credentials stored plaintext (cloud-keys.env, imap_mail_*.json); no encryption at rest | SC-28, IA-5 | W43, W61 | Open |
| POAM-25 | Git history may contain secrets (bundle_for_cloud_model.txt) | SC-28 | H-W79-E0E3652 | Open - history rewrite is an owner decision |
| POAM-26 | Windows portproxy 0.0.0.0:8000 -> dead WSL target, LAN reachable | SC-7, CM-7 | H-W79-PORTPROXY | Open (lab item) |
| POAM-27 | Cloud catch-all: any model name with "/" goes to OpenRouter | SC-7 | W43 | Open |
| POAM-28 | Cloud retry loop retries every HTTP error (401 waits 35 s) | SI-11 | H-W82-2 | Open (own window) |
| POAM-29 | list_local_models raises outside its try (500 not []) | SI-11 | H-W81-3 | Deferred W82 (dormant) |
| POAM-30 | jarvis init --host ignored by model download | CM-6 | H-W81-1 / F1b | ACCEPTED RISK W82 (rebuild rule, Vol 9) |
| POAM-31 | Embeddings default to localhost; nomic-embed-text absent on .200 | - | H-W80-5 / F2 | Deferred W82 (dormant; prerequisite for semantic research) |
| POAM-32 | Trace system: the author package was never tracked (author .gitignore `traces/` + copy-not-clone repo) and a Graystone stub replaced the store. RESTORED byte-exact from af21bc18 (D-47, 1d4b3ae4): the orchestrator path (JarvisSystem.ask) now records every step durably in traces.db. The chat path is still untraced (POAM-57) (RQ-028) | AU-2, AU-12 | H-W73-TRACELOST, W77 F7, W88 SDD 18 | Partially closed (W88) |
| POAM-33 | UI unresponsive during generation; stop does not cancel backend; no chat timeout | SC-5 | W68-W69 | Open |
| POAM-34 | Mic permission auto-approved (--use-fake-ui-for-media-stream) | AC-3 | W63 | Open |
| POAM-35 | Out-of-git configuration items not in any baseline | CM-2 | W80 H-W80-7 | Open (GAP-041) |
| POAM-36 | Many .bak files inside src\; duplicate implementations (two OllamaEmbedder, server\serve.py 0-line shadow) | CM-7 | H-W80-6, W82, H-W74-TWOSERVE | Open (cleanup register) |
| POAM-37 | First request after idle pays ~11.7 s model reload | - | W82 [M] | Open (record) |
| POAM-38 | Streaming speech input dead: stub WS handler registered first; 3 stacked copies; _transcribe_and_send signature mismatch | - (Requirement One) | W82 [R/M] | Open - own change after H5 |
| POAM-39 | 18 family mic clips (4.6 MB, 07/13-07/15) left in %LOCALAPPDATA%\OpenJarvis\audio_debug by a temp diagnostic | SC-28, data minimization | W82 [M] | Writer removed W82 (H5); clip disposition = owner decision |
| POAM-40 | memory.db test uploads injected into every agent turn; OBSERVED W83: model presented author tutorial chunks as the user's stored notes | SI-10 | H-W83-1 [M rq024-list-test] | CLOSED W83 4ee2053 (113 test chunks removed; snapshot kept) |
| POAM-41 | Context-injection failure in routes.py logs only at DEBUG (openjarvis.server) - dark at INFO | AU-2 | H-W83-3 [R] | Open (record) |
| POAM-42 | Multi-system-message handling not assessed for other models' templates or non-Ollama engines | CM-4 | H-W83-5 | Open (assess when a model or engine is added) |
| POAM-43 | memory_index loaded (D-26): model-invoked, ungated, path unconfined; walks a whole tree into memory.db | AC-6, CM-7 | [R W83] | Open - mitigated by D-29 (binaries refused) and D-30 (build trees skipped); path confinement not built |
| POAM-44 | Upload route reports chunks_added as +1 per FILE, including refused files (measured 2 reported, 1 stored) | SI-11 | [M W83 decode-VV] | Open (record; author code not yet diffed for this line) |
| POAM-45 | Upload chunker can leave a one-word tail chunk (owner EA notes chunk 2 = 'attached') | SI-10 (quality) | [M W83 memdb-selective-clear] | Open (record) |
| POAM-46 | Walker drops any file or tail under 50 tokens (author min_chunk_size) - short notes via memory_index are silently not stored | SI-10 | [R W83 chunking.py] | Accepted by owner (keep author 50; short notes use memory_store) |
| POAM-47 | memory_manage remove and user_profile_manage remove are ungated edits of the persona files | AC-6 | [R W83] | Open (record) |
| POAM-48 | Notes list in the prompt is capped at 2,500 chars (head_tail truncation); a long notes list is cut in the prompt (memory_manage read still returns all) | SI-10 | [R builder.py] | Open (record) |
| POAM-49 | Agent system-prompt override now read at startup, not per turn (D-36 side effect) | CM-3 | [R W83] | Accepted with D-36 |
| POAM-50 | code_interpreter can save to ANY absolute path (substring blocklist; library save() and pathlib writes pass) - bypasses the file_write confinement | AC-6, CM-7 | G-1 [R] | Open - assessment due (options: accept, author code_interpreter_docker, path guard) |
| POAM-51 | No delivery path: a created document is never returned to the family member | SI-10 | G-3 [M] | Open |
| POAM-52 | Skills catalog not passed to the persona builder - installed Hermes skills are invisible to the model | CM-8 | G-6 [R] | Open (W89: measured - 5 skills reach the planner and managed agents, not chat; SDD 19) |
| POAM-53 | No self-verification path: file_write success message lacks the full path, no file-created event; model self-check via shell_exec hits the gate -> false 'failed' reply (R2) | AU-2, SI-10 | G-10 [M] | PARTLY CLOSED W87 c85fcf9 (D-46: code_interpreter lists created files first in content and in metadata on TOOL_CALL_END; S3 re-run 4 honest replies 6/6, shell_exec 0). Remaining: file_write message echoes the requested name, not the resolved path (patch B) |
| POAM-54 | dispatch.log OUTCOME records a reason code but not the tool's error text; code_interpreter stdout/stderr/exit code not logged | AU-3 | G-11 [M] | Open - visibility gap (owner goal). W87: blocked measurement twice (R2 tool content; R1 t2/t3 exit 0 with no file) and leaves D-46's Files line unobserved live |
| POAM-55 | Model detail fidelity: Excel formulas requested but values written in 2 of 3 runs | SI-10 (quality) | S3 R3 [M] | Open (tuning) |
| POAM-56 | grpcio 1.78.1 in uv.lock is YANKED upstream (outage); zeus-ml asked for a nonexistent extra | SI-2 | [M uv output] | Open (pre-existing lock) |
| POAM-57 | Chat path (server routes.py, native_openhands - the family path) records no trace: tool content and error text are not durable (G-11 remainder). Author wired chat-path tracing after the baseline (upstream ef005703) | AU-2, AU-12 | W88 SDD 18.3, 18.6 | Open |
| POAM-58 | Possible double save of a trace inside the server (app.py store subscribed to TRACE_COMPLETE + collector save -> UNIQUE violation). Unmeasured; author fix upstream ef005703. Measure before porting POAM-57 | SI-11 | W88 SDD 18.6, W89 SDD 18.10 | Closed (W89) - not reachable as built: the only server collector (digest SDK) is on its own bus; reopens if a trace-store-bearing system runs on app.state.bus or POAM-57 is ported without removing app.py:239-240 |
| POAM-59 | Author .gitignore bare `traces/` matches the traces source package (copy-not-clone installs lose it); untracked Engineering_Wiki doc inside src\openjarvis\traces (gitignored at .gitignore:65) | CM-2, CM-7 | W88 H-W88-3 | Open (cleanup register) |
| POAM-60 | Skills install (PLACEHOLDER, owner W89): over 200 skills from owner repos to be installed later via the author's importer; prerequisites in SDD 19.8 (decide chat-path design, author safeguards #639/#961/#781/#780 not in baseline, small-batch measurement) | CM-7, SI-7 | W89 SDD 19.8 | Planned - after the owner approves author vs Graystone baseline (services offered) |
| POAM-61 | Skills do not reach the server chat route (author design, same at upstream a6dcf846); planner and managed agents have them. Owner decision pending with assessment in SDD 19.7 (options A/B/C) | CM-2 | W89 SDD 19.3, 19.7 | Closed - owner ruling W89: option A (author design) until the skills install (POAM-60) |
| POAM-62 | Trace read-back routes open a new TraceStore per request and never close it (agent_manager_routes.py:1961-1965, :1986-1990; api_routes.py:813-820, which also hard-codes DEFAULT_CONFIG_DIR/traces.db); origin not established | SC-5, CM-6 | W89 SDD 18.10 | Deferred (owner W89) - fix with the upstream-code repair of the managed-agents service as ONE complete service; measured no live leak (handles 468 -> 503 -> 493 over 100 calls) |
| POAM-63 | Duplicate speech WebSocket: /v1/speech/stream and a double-prefixed /v1/speech/v1/speech/stream (server\speech_router.py, Graystone) - cleanup register: back up and remove the duplicate | CM-7 | W89 SDD 20.6 F1 | Open (speech service repair) |
| POAM-64 | POST /v1/tools/test-execute (Graystone-only): confirm whether it executes tools directly and whether it bypasses the confirmation gate | AC-3, AC-6 | W89 SDD 20.6 F2 | Open (chat/tools service repair) |
| POAM-65 | Live config.toml: [analytics] present (owner 09/22: remove the analytics path as dead code); [traces], [telemetry], [learning*], [tools.storage], [tools.mcp] absent (author defaults) | CM-6 | W89 SDD 20.6 F3 | Open (upgrade config review) |
| CLOSED | Office files: relative saves in repo root (G-2), fenced code failed (G-9), file_write relative names denied (G-7), text written into .docx/.pptx with false 'created' claims | CM-2, SI-10 | W83 [M] | CLOSED 5883f98, 5a6735d, 0507c8c (D-41..D-45) |
| CLOSED | Author persona layer never reached any tool agent (hook not forwarded, builder never built) | CM-2 | W83 [M] | CLOSED W83 6429769 (D-35, D-36) |
| CLOSED | Ingest decode stored UTF-16 as char+NUL and accepted binaries (author defect, both paths) | SI-10 | W83 [M] | CLOSED W83 a457239 + 00edd61 (D-28, D-29) |
| CLOSED | Author context injection never reached the model: min_score 20.0 above every score, and qwen3-coder template dropped the second system message | SI-11 | W83 [M] | CLOSED W83 (D-24 config, D-25 675cda6; V&V +1120 tokens) |
| CLOSED | Duplicate /v1/speech/health and /transcribe (Graystone shadowing author routes; mic dump in the live route) | CM-7, SI-11 | H-W81-5 | CLOSED W82 H5 (author routes serve; V1-V5 PASS) |
| CLOSED | CDP port 9222 on production exe | AC-17 | W63 | CLOSED W63 |
| CLOSED | Self-loop engines at port 8010 | SC-5 | W79 | CLOSED a0704c4 |
