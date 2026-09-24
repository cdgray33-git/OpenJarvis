# VOL 1 - SYSTEM/SUBSYSTEM DESIGN DESCRIPTION (SSDD)
Governing DID: DI-IPSC-81432 (outline to be verified, GAP-002). v0.2 DRAFT 2026-09-23 (W82). Harvest of W42-W82.

## 1. SCOPE
### 1.1 Identification
OpenJarvis, Graystone Lab deployment. Repo github.com/cdgray33-git/OpenJarvis (remote `origin`) and
172.16.33.126/root/openjarvis-desktop (remote `gitlab`). Fork of upstream open-jarvis/OpenJarvis; author baseline commit
af21bc18 (2026-05-19), first Graystone commit f2fcb30 (2026-05-30) [M W73, W82].
### 1.2 System overview
Purpose [S 09/06]: a functional executive assistant that performs the computer duties a human assistant would, for the owner's
family. Self-hosted: desktop client and backend on a Windows workstation, models and speech on lab servers.
Operational status [S]: development, in personal use. Progress measure: requirements VERIFIED / 28 (Vol 2) = 3/28.
Next build platform: Ubuntu VM (owner W74); this native-Windows tree is the documented legacy build.
### 1.3 Plain language
Jarvis is a helper program. The part you see and its "back office" run on the Windows computer. The thinking (language models)
and hearing run on a lab server; the speaking runs on a second lab server. A few things - cloud models, web search and your mail
provider - are outside the house and reached over the internet.

## 2. REFERENCED DOCUMENTS
Author procedures (upstream clone C:\Users\Admin\upstream-OpenJarvis; list in Vol 3A SOURCES). MIL-STD-498 DIDs. NIST SP 800-18,
800-34, 800-37, 800-53. DoDI 8510.01, 8551.01. Handoff archives ARCHIVE-W42..W81 (repo root) and W82 records (evidence\W82).

## 3. SYSTEM CONTEXT AND AUTHORIZATION BOUNDARY
### 3.1 Trust zones
| Zone | Contents | Trust | Grade |
|---|---|---|---|
| Z1 Workstation loopback | backend 127.0.0.1:8010, desktop webview, local files (config, keys, logs, stores) | owner-controlled; any local process can reach loopback | [M] |
| Z2 Lab segment | Ollama/faster-whisper 172.16.33.200; Kokoro 172.16.33.201; GitLab 172.16.33.126 | owner-controlled; no TLS, no service auth on model and voice APIs | [M] |
| Z3 Internet | OpenRouter and other cloud model APIs, web search, mail provider (Yahoo IMAP), GitHub | external; TLS | [R] |
Boundary diagram (OV-1/SV-1, standalone file): GAP-013/GAP-031.
### 3.2 What crosses the boundary (see Vol 3 section 5)
Cloud-model prompts (can include family email content), mail operations under the family credential, web-search queries, git
pushes to GitHub, and owner-requested 550B analysis bundles (W74 egress record).

## 4. SYSTEM COMPONENTS
| ID | Component | Host / location | Grade |
|---|---|---|---|
| C-01 | Desktop client (Tauri + React, WebView2), openjarvis-desktop.exe | %LOCALAPPDATA%\OpenJarvis\ | [M W63] |
| C-02 | Backend (Python 3.12.10 FastAPI/uvicorn), src\openjarvis\, launched by start-openjarvis.ps1 | Windows, 127.0.0.1:8010 | [M W80] |
| C-03 | Model host Ollama, model qwen3-coder:30b (18.9 GB VRAM), 29-model inventory | 172.16.33.200:11434 | [M W80-W82] |
| C-04 | TTS Kokoro, voice am_adam | 172.16.33.201:8880 | [R/M W64] |
| C-05 | Source control mirrors | GitHub (HTTPS) / GitLab 172.16.33.126 (HTTP) | [M] |
| C-06 | STT faster-whisper | on 172.16.33.200 per owner; port not recorded | [S W81] GAP-012 |
| C-07 | External services | OpenRouter, web search, Yahoo IMAP | [R] |
| C-08 | Local stores | config.toml, memory.db, agents.db, telemetry.db, traces.db, knowledge.db, logs, key files (Vol 5) | [M/R] |

## 5. SYSTEM-WIDE DESIGN DECISIONS (full author-vs-Graystone register in Vol 3A section D and G)
| ID | Decision | Rationale | Owner ruling | Grade |
|---|---|---|---|---|
| DD-01 | Agent = NativeOpenHandsAgent (native_openhands) | qwen3-coder:30b handles tools internally | owner 09/06, 09/21 | [S] |
| DD-02 | Production build only; tauri dev prohibited | dev and prod share files; caused defects | owner 09/12 | [S] |
| DD-03 | Local inference via Ollama on a remote lab host, host in config [engine.ollama] host (author form), OLLAMA_HOST kept as fallback | two-server topology; author puts remote host in config | owner W80 option 2 | [M W80] |
| DD-04 | Agent reply streaming Option A (stream each turn, retract on tool call) | conversational latency | owner W70; NOT built | [S] |
| DD-05 | Destructive mailbox tools: model-side two-key interlock PLUS argument-aware human gate (fires on apply only) | spec flag alone cannot gate a tool with safe and destructive modes | owner insisted mail be human-confirmed; built W58, live-proven W60 | [M] |
| DD-06 | Confirmation gate live by default on the chat path; unattended sites auto-approve WITH attribution (ConfirmPolicy) | unattended paths must not block; every auto-approval must leave a record | W49 design, W56 build | [R/M] |
| DD-07 | Socket authentication on the confirmation WebSocket deferred | loopback-only bind limits blast radius | owner 08/29 | [S] |
| DD-08 | Single logging authority: level dial inside the author's setup_logging (OPENJARVIS_LOG_LEVEL), 40 MB backend.log budget | no third configuration authority | owner 09/09 | [M W42] |
| DD-09 | Engine turn-down list [engine] disabled (D-16) | prevents self-loop to the Jarvis port | a0704c4 | [M W79] |
| DD-10 | Server port 8010 (author 8000) | a Windows portproxy holds 0.0.0.0:8000 | constraint | [M W79] |
| DD-11 | file_write confined to ~\.openjarvis\workspace (D-14); file_read NOT confined | writes anywhere were unsafe; confining reads breaks "read my document" | owner W78 (rejected gating) | [M W78] |
| DD-12 | Nothing leaves the lab unless the owner requests it; analytics/PostHog code to be removed | privacy | owner W78 | [S] |
| DD-13 | Python 3.12.10 pinned until the Tesla P100 is installed | dependency stability | owner 09/23 | [S] |
| DD-14 | Dormant findings are recorded, not changed, until the full system is operational; security assessment at the end | a fix to a dormant path may itself be a bug | owner W82 | [S] |
| DD-15 | Author's code and procedures are the baseline; every divergence recorded; enhance after finishing the author's build | measurable divergence | owner 09/06, W79 | [S] |

## 6. CONCEPT OF EXECUTION (summary; detail in Vol 4)
- Start: start-openjarvis.ps1 -> uvicorn backend on 127.0.0.1:8010 (Vol 4 section 2). Desktop app started separately by shortcut.
- Chat: desktop -> POST /v1/chat/completions -> agent or engine -> Ollama -> SSE back (Vol 4 section 3; Vol 3 IF-01/IF-02).
- Tool use: agent -> ToolExecutor gate chain -> (human gate over WebSocket + POST for confirmable tools) -> tool (Vol 4 sections 5-6).
- Voice: reply text -> Kokoro -> speakers (Vol 4 section 12). Hearing: microphone -> faster-whisper.
- Autonomy: managed agents (manual and scheduled, one scheduled tick at a time); author operators never run (Vol 4 section 8).
- Concurrency: about 2 simultaneous model requests at the GPU; the rest queue (Vol 4 section 10).

## 7. REQUIREMENTS TRACEABILITY
Vol 2 (02-SRS-RTM.md) ratified 09/22: 28 core rows, VERIFIED 3/28 (RQ-021, RQ-022, RQ-030). Author mechanism per row in
Vol 3A section C (COVERED 4, PARTIAL 12, GAP 12).

## 8. NOTES
Glossary: GAP-014.
