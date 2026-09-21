# VOL 1 - SYSTEM/SUBSYSTEM DESIGN DESCRIPTION (SSDD)
Governing DID: DI-IPSC-81432 (outline to be verified, GAP-002). v0.1 DRAFT.

## 1. SCOPE
### 1.1 Identification
OpenJarvis, Graystone Lab deployment. Repo: github.com/cdgray33-git/OpenJarvis
(remote `origin`) and 172.16.33.126/root/openjarvis-desktop (remote `gitlab`). [M]
### 1.2 System overview
Purpose [S]: a functional executive assistant that performs the computer duties
a human assistant would. Self-hosted; desktop client plus backend plus local
model host.
### 1.3 Document overview
Records system-wide design decisions, components, concept of execution, and
interfaces. Detail per component is in Vol 4; interfaces in Vol 3.

## 2. REFERENCED DOCUMENTS
Upstream author installation procedures (location TBD, GAP-010). MIL-STD-498
DIDs. NIST SP 800-18, 800-34, 800-37, 800-53. DoDI 8510.01, 8551.01.

## 3. SYSTEM-WIDE DESIGN DECISIONS
| ID | Decision | Grade | Rationale / evidence |
|---|---|---|---|
| DD-01 | Agent = `NativeOpenHandsAgent` (`native_openhands`), chosen and modified by Graystone; author agent installation procedure NOT run | [S] 09/06, 09/21 | Owner adopted it because qwen3-coder:30b handles tools internally |
| DD-02 | Production build only; dev mode (`tauri dev`) prohibited | [S] 09/12 | Dev and prod share files; caused defects |
| DD-03 | Local inference via Ollama engine (`engine\ollama.py`) | [R] | OllamaEngine registered as "ollama" |
| DD-04 | Agent reply streaming: Option A (stream each turn live; retract if turn is a tool call) | [S] W70 | Not yet built; see Vol 8 POAM-01 |
| DD-05 | Destructive mailbox tools use a two-part interlock (dry_run=False AND exact token) instead of `requires_confirmation` | [S]/[R] 08/04 | `requires_confirmation` hard-fails on the server path |

## 4. SYSTEM ARCHITECTURAL DESIGN
### 4.1 System components
| ID | Component | Host / location | Grade |
|---|---|---|---|
| C-01 | Desktop client (Tauri + React), `openjarvis-desktop.exe` | Windows workstation, `%LOCALAPPDATA%\OpenJarvis\` | [M] |
| C-02 | Backend (Python/FastAPI), source `src\openjarvis\`, interpreter `.venv\Scripts\python.exe` | Windows workstation, TCP 8010 | [M] |
| C-03 | Model host (Ollama) | Ubuntu, 172.16.33.200, port TBD (GAP-011) | [S] |
| C-04 | TTS service (Kokoro) | "ollama-mcp2", address TBD (GAP-012) | [S] |
| C-05 | Source control mirrors | GitHub (HTTPS); GitLab 172.16.33.126 (HTTP) | [M] |
Diagrams OV-1 and SV-1 required - GAP-013.

### 4.2 Concept of execution - chat dispatch
`POST /v1/chat/completions` in `src\openjarvis\server\routes.py` dispatches to
four branches [R, 08/23 register]:
| Path | Condition | Behavior |
|---|---|---|
| 1a | non-streaming, agent | agent.run() offloaded via asyncio.to_thread |
| 1b | streaming AND agent/tools in request body | `create_agent_stream` -> `stream_bridge.py`; agent.run() in thread; reply BUFFERED then replayed [M W70] |
| 1c | non-streaming, no agent | offloaded via asyncio.to_thread |
| 1d | streaming, no agent | plain engine token stream; live streaming confirmed [M W71] |
The client selects the path: ChatArea sends `agent: selectedAgentId || ''`;
an empty string lands on 1d [R].

#### 4.2.1 Path 1b flow, gate by gate [R W71]
1. Client POST (SSE) -> routes.py -> `create_agent_stream`.
2. `AgentStreamBridge.stream()` subscribes EventBus callbacks
   (agent_turn_start, inference_start/end, tool_call_start/end) and starts
   `agent.run()` in a worker thread.
3. `NativeOpenHandsAgent.run()` loops up to max_turns; each turn calls
   `BaseAgent._generate()` -> `engine.generate()` (synchronous, full text).
4. A turn with native tool_calls, python code, or a text tool call executes
   the tool via ToolExecutor and loops; a plain-text turn is the final answer.
5. Only after run() returns does the bridge emit tool_results and replay the
   final text word by word. Result: no text reaches the client until the
   whole answer exists.
Plain language: the helper writes the whole letter before handing over any
of it; the bridge then reads the letter aloud quickly.

## 5. REQUIREMENTS TRACEABILITY
Blocked: no requirements baseline exists (Vol 2, GAP-020).

## 6. NOTES
Acronyms and glossary - GAP-014.
