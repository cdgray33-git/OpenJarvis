# VOL 4 - SOFTWARE DESIGN DESCRIPTION (SDD)
Governing DID: DI-IPSC-81435 (verify, GAP-002). v0.1 DRAFT.

## 3. CSCI-WIDE DESIGN DECISIONS - see Vol 1 section 3
## 4. CSCI ARCHITECTURAL DESIGN
### 4.1 Components - agent streaming path code map [R/M 2026-09-21]
| Unit | File | Lines | Role |
|---|---|---|---|
| NativeOpenHandsAgent | src\openjarvis\agents\native_openhands.py | 660 | The agent on path 1b |
| BaseAgent / ToolUsingAgent | src\openjarvis\agents\_stubs.py | 358 | Agent contract; `_generate()`; executor construction |
| InferenceEngine / StreamChunk | src\openjarvis\engine\_stubs.py | 129 | Engine contract; `engine\_base.py` re-exports the same class [M] |
| OllamaEngine | src\openjarvis\engine\ollama.py | 538 | Live backend; stream_full at :238 |
| OpenAI-compat base | src\openjarvis\engine\_openai_compat.py | 248 | stream_full :158 |
| MultiEngine | src\openjarvis\engine\multi.py | 141 | Routes by model name |
| InstrumentedEngine | src\openjarvis\telemetry\instrumented_engine.py | 507 | Telemetry wrapper |
| GuardrailsEngine | src\openjarvis\security\guardrails.py | 317 | Secret/PII scanning |
| EventBus | src\openjarvis\core\events.py | 201 | Pub/sub |
| AgentStreamBridge | src\openjarvis\server\stream_bridge.py | 368 | Path 1b SSE bridge; `if False` branch at :246 deliberate [M W70] |
| ChatArea | frontend\src\components\Chat\ChatArea.tsx (capital C in git) | 542 | Chat UI, TTS driver |
| ttsPlayer | frontend\src\audio\ttsPlayer.ts | 377 | Audio playback |
All five backend modules load from `src\` under `.venv` - no installed copy [M].

### 4.2 Known design hazards on this path [R W71]
- InstrumentedEngine.stream_full emits no INFERENCE/TELEMETRY events.
- GuardrailsEngine.stream_full does not scan or redact input.
- Ollama stream methods block the event loop (sync client in async generator).
## 5. DETAILED DESIGN - GAP-016 (per unit, from harvest)
