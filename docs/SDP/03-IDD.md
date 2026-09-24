# VOL 3 - INTERFACE DESIGN DESCRIPTION (IDD / ICD, SV-6 DATA EXCHANGE)
Governing DID: DI-IPSC-81436 (outline to be verified against the DID text, GAP-002). v0.2 DRAFT 2026-09-23 (W82).
v0.2 harvests W42-W82 archives into this volume (GAP-003 harvest, W82). v0.1 (W71) rows IF-01..IF-05 are kept and completed.
Owner requirement [S 08/22]: ports, protocols and encoding at EVERY gate. Every row carries an evidence grade and source window.
Grades: [M] measured, [R] read from code (file:line), [S] owner statement. [I] is not permitted as a basis (Master section 3).

## 1. PLAIN LANGUAGE - HOW JARVIS TALKS TO THINGS
Jarvis is two computers and a few outside services. The Windows desktop runs the app you see and the Jarvis
"back office" (the backend). The back office never listens to the network: it only answers calls from the same
computer (address 127.0.0.1, port 8010). When Jarvis needs to think, it phones the lab's brain server on the
Ubuntu machine (172.16.33.200, port 11434). When it needs to speak, it phones the voice server (172.16.33.201,
port 8880). Those lab phone calls are not locked (no encryption, no password) - that is written down as an open
item (Vol 8). A few calls leave the house entirely: cloud models (OpenRouter), web search, and your mail provider.
Those use the internet's locked envelope (HTTPS/TLS), except where marked "not yet read".

## 2. ENDPOINTS (NODES)
| Node | Identity | Address | Grade |
|---|---|---|---|
| N1 Workstation (Windows) | Desktop client + backend host | LAN 192.168.1.137 (source address seen on engine calls) | [M W77 E3] |
| N2 Backend (FastAPI/uvicorn) | Python 3.12.10 (Python312), repo src\ editable | 127.0.0.1:8010 TCP, loopback only | [M W42, W77, W80] |
| N3 Model host "ollama-mcp" | Ubuntu, Ollama; faster-whisper per owner | 172.16.33.200:11434 TCP (Ollama) | [M W77, W80, W81] [S W81 whisper] |
| N4 Voice host | Kokoro TTS | 172.16.33.201:8880 TCP | [R/M W64] |
| N5 GitLab (lab) | remote "gitlab" | 172.16.33.126 (repo root/openjarvis-desktop), HTTP | [M W43, v0.1] |
| N6 GitHub | remote "origin" cdgray33-git/OpenJarvis | github.com:443 HTTPS | [M W43] |
| N7 OpenRouter | cloud model broker | openrouter.ai:443 HTTPS | [R W43] [M W43 catalog] |
| N8 Mail provider (Yahoo) | IMAP | host/port/TLS NOT READ (imap_mail.py unread) | GAP-015 |
| N9 WSL2 target (dead) | portproxy target | 172.21.134.21:8000 | [M W79] |

## 3. INTERFACE TABLE (every gate)
| IF | From -> To | Transport | Protocol / route | Payload and encoding | Auth / TLS | Timeout | Grade |
|---|---|---|---|---|---|---|---|
| IF-01 | Desktop webview -> backend | TCP 127.0.0.1:8010 | HTTP/1.1 POST /v1/chat/completions, SSE response (text/event-stream; charset=utf-8, chunked) | Request JSON UTF-8 {model, messages, stream, temperature, max_tokens, agent}; response `data:` ChatCompletionChunk JSON lines, named `event:` lines, terminator `data: [DONE]`; client decodes with TextDecoder | Optional `Authorization: Bearer` from localStorage `openjarvis-settings.apiKey`; no challenge on loopback [M W80 EV11]; no TLS (loopback) | Client builds a timeout controller but chat has no effective timeout (H-W69) | [M W70, W80] [R sse.ts] |
| IF-02 | Backend engine -> Ollama (Path A) | TCP 172.16.33.200:11434 from 192.168.1.137 | HTTP/1.1 POST /api/chat (stream), GET /api/tags health about every 30 s | Request JSON UTF-8; streamed NDJSON; tool_calls arrive whole in one chunk; think=false default; num_ctx from config/env; httpx pooled, 3 keep-alive | NONE (Ollama has no auth); NO TLS - plaintext on lab segment | per engine config | [M W80 EV8/EV11] [R ollama.py] |
| IF-02a | Backend cloud_router -> Ollama (Path B1, fallback) | same as IF-02 | POST {host}/api/chat via httpx.AsyncClient | JSON UTF-8 {model, messages, stream:true, think:false, options}; NDJSON response | NONE / no TLS | 300 s | [R W81 s5.1] |
| IF-02b | Backend cloud_router -> Ollama (Path B2, model list fallback) | same | GET {host}/api/tags | JSON UTF-8 | NONE / no TLS | 10 s | [R W81 s5.1] |
| IF-03 | Webview -> backend speech synthesis | TCP 127.0.0.1:8010 | HTTP/1.1 POST /v1/speech/synthesize | JSON in {text, voice_id am_adam, speed 0.85, output_format wav}; audio/wav blob out | Bearer optional; no TLS | 30 s client timeout (W67) | [M W62, W64, W67] |
| IF-03a | Backend speech_router -> Kokoro | TCP 172.16.33.201:8880 | HTTP/1.1 POST /synthesize (proxy) | JSON request; WAV response 24 kHz 16-bit mono | NONE / no TLS | not recorded | [R/M W64] |
| IF-03b | Webview AudioContext -> Windows audio | in-host | WASAPI shared session on an explicit endpoint (setSinkId, W66) | PCM float32 at context sample rate | n/a | n/a | [M W64-W66] |
| IF-04 | Backend EventBus -> SSE named events (Path 1b) | in-process | pub/sub; AgentStreamBridge; call_soon_threadsafe into asyncio.Queue | agent_turn_start, inference_start, inference_end, tool_call_start, tool_call_end, tool_results | n/a | n/a | [R W70] |
| IF-05 | Workstation -> GitHub / GitLab | TCP 443 / 80 | HTTPS / HTTP, git pack protocol | git objects | GitHub HTTPS credential; GitLab plain HTTP | n/a | [M v0.1, W43] |
| IF-06 | Webview -> backend speech transcription | TCP 127.0.0.1:8010 | HTTP/1.1 POST /v1/speech/transcribe | multipart/form-data, recording.webm | Bearer optional; no TLS | not recorded | [R W62] |
| IF-06a | Backend -> faster-whisper | host stated 172.16.33.200 [S W81]; port NOT RECORDED | NOT RECORDED | audio in, text out | NOT RECORDED | - | GAP-012 |
| IF-07 | Backend -> webview confirmation events | TCP 127.0.0.1:8010 | WebSocket ws://127.0.0.1:8010/v1/agents/events (no agent_id = unfiltered, subscribeAll) | JSON text frames via send_json: tool_confirm_request {confirm_id, agent_id, turn_id, tool, args_digest, prompt, expires_at}; tool_confirm_resolved {decision, state, created_at, expires_at, reaped} | NONE on socket: ws-accept authed=False while api_key_set=True [M W81 H-W81-6]; owner deferred socket auth 08/29; redaction on WS leg keyed to app.state.bind_is_loopback | TTL 120 s on the gate | [R W50-W51, W57] [M W50 timings] |
| IF-08 | Webview -> backend confirmation answer | TCP 127.0.0.1:8010 | HTTP/1.1 POST /v1/tools/confirm | application/json {confirm_id, decision}; decision approve/deny/approved/denied, normalized; 404 unknown id, 409 already decided (returns recorded decision) | Bearer when apiKey set | resolve measured 7 ms; end to end 0.014 s | [R W51-W52, W57] [M W50] |
| IF-09 | Operator harness -> backend gate trigger | TCP 127.0.0.1:8010 | HTTP/1.1 POST /v1/tools/test-execute | JSON {tool, arguments(object)}; 202 {run_id, turn_id, tool, marker}; 400 unknown keys / bad type / missing tool; 403 OPENJARVIS_TEST_EXEC unset or bind not loopback; 404 tool not on live agent; 409 no live executor; 422 tool not confirmable | loopback enforced by route | fire-and-forget worker thread | [R W49, W52] |
| IF-10 | Backend -> OpenRouter (cloud model) | TCP openrouter.ai:443 | HTTPS POST /api/v1/chat/completions, SSE response | JSON UTF-8 {model (openrouter/ prefix stripped), messages, temperature, max_tokens, stream:true}; `data:` lines, `[DONE]`; headers HTTP-Referer https://openjarvis.local, X-Title OpenJarvis | Bearer key from C:\Users\Admin\.openjarvis\cloud-keys.env (read every request; 6 env names override); TLS | httpx 180 s; retry 5/10/20 s (retries every HTTP error, H-W82-2) | [R W43, W82] |
| IF-10a | Backend -> Anthropic / Google / OpenAI / MiniMax (same router, keys empty today) | TCP 443 | api.anthropic.com/v1/messages (x-api-key, anthropic-version 2023-06-01); generativelanguage.googleapis.com ...:streamGenerateContent?alt=sse&key= (key in URL query); api.openai.com/v1; api.minimax.io/v1 | JSON UTF-8, SSE | TLS; key per provider | 180 s | [R af21bc18 read W82] [M W43 keys empty] |
| IF-11 | Backend -> mail provider (Yahoo) IMAP | NOT READ | IMAP via ImapMailConnector(provider, account_id, credentials_path, imap_host) | message metadata/bodies | credentials C:\Users\Admin\.openjarvis\connectors\imap_mail_<account>.json {email, password, provider, [host]}; TLS mode NOT READ | tools: 600 s / 1800 s | [R W61] GAP-015 |
| IF-12 | Backend -> web search | TCP 443 | You.com keyless default, DuckDuckGo fallback (author) | HTTPS JSON/HTML | TLS | - | [R Vol 3A C, W77] |
| IF-13 | Backend -> Google OAuth (gcontacts etc., not configured) | localhost:8789 redirect | OAuth 2.0 | - | - | - | [R W72 author docs] not deployed |
| IF-14 | Frontend static assets | TCP 127.0.0.1:8010 GET / | backend serves src\openjarvis\server\static (vite output); the exe EMBEDS the same directory at build time | HTML/JS/CSS | - | - | [M W51, W63] |
| IF-15 | Desktop renderer debug port (REMOVED) | 127.0.0.1:9222 | Chrome DevTools Protocol | - | NONE - any local process could drive approvals | - | [M W63] CLOSED W63 |
| IF-16 | Windows portproxy (not Jarvis) | 0.0.0.0:8000 -> 172.21.134.21:8000 | TCP forward (iphlpsvc) | - | none; LAN reachable; dead target | - | [M W79] H-W79-PORTPROXY |
| IF-17 | Backend -> PostHog analytics (author default, DISABLED here) | 34.231.106.201.sslip.io | HTTPS | telemetry | hardcoded key | - | [R W78] config sets enabled=false (D-10) |

## 4. LOCAL (NON-NETWORK) INTERFACES
| IF | Path | Mechanism | Encoding | Grade |
|---|---|---|---|---|
| IL-01 | Logs %LOCALAPPDATA%\OpenJarvis\logs\ (backend.log, dispatch.log, engine.log, agent.log) | Python RotatingFileHandler, filesystem | UTF-8 | [R/M W45, W52] |
| IL-02 | Config C:\Users\Admin\.openjarvis\config.toml | tomllib at load_config (lru_cached, restart to reload) | UTF-8 NO BOM (tomllib rejects BOM), CRLF | [M W80] |
| IL-03 | Secrets cloud-keys.env; connectors\imap_mail_<account>.json; protected_senders.json | file read per request (cloud keys) or per tool call | UTF-8 | [R W43, W61] |
| IL-04 | Confirmation registry core\confirm_registry.py | in-process dict + threading.Event; ContextVars CURRENT_CONFIRM_ID, CURRENT_TURN_ID | Python objects; _json_safe_metadata strips TaintSet before bus | [R W46, W50] |
| IL-05 | EventBus core\events.py; app.state.bus bridged to WS (08/22 bus-split fix) | in-process pub/sub, thread-safe | dict payloads, Event slots=True | [R W50, v0.1] |

## 5. DATA THAT CAN LEAVE THE LAB (external boundary, for the AO)
| Flow | What can cross | Control today | Grade |
|---|---|---|---|
| IF-10 cloud models | the full chat prompt and history, which can include family email content read by mailbox tools | only when the user selects a cloud model; cloud models run WITHOUT tools; no confirmation at request | [R W43, W80] |
| IF-11 mail provider | IMAP commands under the family account credential | two-key interlock + human gate on destructive tools (Vol 4 section 6) | [R W58-W61] |
| IF-12 web search | search query text chosen by the model | none at request | [R] |
| IF-05 GitHub | source, handoff archives, evidence (may include lab IPs, file paths) | owner push | [M] |
| W74 R06 and similar 550B bundles | source diffs and records sent to OpenRouter by owner request | secret scan before send (W74) | [M W74 H-W74-EGRESS] |

## 6. OPEN INTERFACE ITEMS
GAP-012 faster-whisper port/protocol. GAP-015 IMAP host/port/TLS/auth (read imap_mail.py whole). SC-8 plaintext on IF-02/03a;
IA-9 no service authentication on IF-02/03a; IF-07 socket unauthenticated (H-W81-6). All carried to Vol 8.
