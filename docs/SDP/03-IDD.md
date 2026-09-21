# VOL 3 - INTERFACE DESIGN DESCRIPTION (IDD / ICD, SV-6 DATA EXCHANGE)
Governing DID: DI-IPSC-81436 (verify, GAP-002). v0.1 DRAFT.
Owner requirement: ports, protocols, and encoding at EVERY gate [S 08/22].

## 3.1 Interface identification
| IF | From -> To | Port | Protocol | Payload / encoding | Grade |
|---|---|---|---|---|---|
| IF-01 | C-01 client -> C-02 backend, `POST /v1/chat/completions` | 8010 | HTTP/1.1, SSE response | Request JSON UTF-8; response `data:` lines of ChatCompletionChunk JSON, named `event:` lines, terminator `data: [DONE]` | [R]/[M] |
| IF-02 | C-02 backend -> C-03 Ollama, `/api/chat` | TBD (GAP-011) | HTTP, httpx SYNC client | Request JSON; streamed NDJSON lines; tool_calls arrive whole in one chunk | [R] |
| IF-03 | C-01 client -> speech synthesis (`synthesizeSpeech`) | TBD (GAP-012) | HTTP | Text in; audio blob out, decoded by WebAudio | [R] partial |
| IF-04 | C-02 internal EventBus -> SSE named events | n/a (in-process) | pub/sub, thread-safe | agent_turn_start, inference_start, inference_end, tool_call_start, tool_call_end, tool_results | [R] |
| IF-05 | Workstation -> GitHub / GitLab | 443 / 80 | HTTPS / HTTP | git pack protocol | [M] |

## 3.2 IF-01 detail
Request fields used by client: model, messages, stream=true, temperature,
max_tokens, agent. Client ends read on finish_reason "stop". [R ChatArea.tsx]
## 3.3 IF-02 detail
stream_full passes tools; retries without tools on HTTP 400 (no log line on
this path, POAM-05). think=false by default; num_ctx from config/env. [R ollama.py]
## 3.x Remaining interfaces (memory.db, telemetry.db, IMAP 993 to Yahoo,
tool confirm route, WebSocket bridge) - GAP-015.
