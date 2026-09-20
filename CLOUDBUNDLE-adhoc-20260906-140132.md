# OPENJARVIS CODE REVIEW BUNDLE

- marker: `openjarvis-cloudbundle-v1`
- set: `adhoc` - ad hoc bundle
- generated: 2026-09-06T14:01:32
- repo root: `C:\Users\Admin\OpenJarvis`
- files in bundle: 5

You are reviewing complete source files. Every file is included in full, with authoritative 1-based line numbers in the left gutter. Nothing has been elided.

---

# THE QUESTION

REQUIREMENTS AND PROGRESS BASELINE. This is the upstream OpenJarvis project's own documentation. The reader is the sole developer of a heavily modified deployment who never ran the author's agent-activation steps and built all agent behavior himself. His goal is a functional executive assistant that performs all the duties at a computer that a human would. He is approaching one year of work, believes he is under 50 percent of his initial requirements, and has no way to measure progress. Q1: extract from these documents the COMPLETE list of capabilities the author states OpenJarvis provides or intends to provide. Present it as a flat checklist, one capability per line, each traceable to a file and section. Do not editorialize or group by theme. Q2: from the roadmap specifically, separate what the author marks as DONE from what is PLANNED or ASPIRATIONAL, and say how the author signals that difference. Q3: identify any capability the author describes that would be required by an executive assistant performing computer duties for a person - email, calendar, file management, scheduling, web tasks, document work, recall of past actions. Q4: what does the author say about agents specifically - how they are meant to be activated, configured, and given tools? Cite the exact section. Q5: state what these documents DO NOT cover that a progress measure would need. Answer each separately and cite file and section. Do not estimate where you can count.

---

# SOURCE

---

## FILE: `docs/development/roadmap.md`

- bytes: 12120
- lines: 141
- sha256: `CED58799640D40997858F2F1E0C0F39081B23C2925A5EBC44170AD5C071608EE`
- line terminator: LF

Line numbers below are 1-based and authoritative. Cite them.

```markdown
  1 | # Roadmap
  2 | 
  3 | ## Current Focus Areas
  4 | 
  5 | These are the areas where active development is happening and contributions are most impactful:
  6 | 
  7 | - **Post-training data** — building datasets and training pipelines from execution traces to improve agent routing and tool selection
  8 | - **Multi-model orchestration pipelines** — coordinating multiple models within a single query (e.g., small model for classification, large model for generation)
  9 | - **Energy-aware routing** — using power consumption data from telemetry to optimize for energy efficiency alongside latency and quality
 10 | - **Plugin ecosystem** — community-contributed engines, tools, and agents distributed as Python packages
 11 | - **Federated memory** — memory backends that synchronize across devices
 12 | - **LLM-guided spec search:** Frontier-driven harness learning — a frontier model analyzes your traces and proposes config improvements. See [user guide](../user-guide/llm-guided-spec-search.md) and [architecture](../architecture/learning.md#llm-guided-spec-search-frontier-driven-harness-learning).
 13 | 
 14 | ---
 15 | 
 16 | ## How to Get Involved
 17 | 
 18 | 1. Browse the workstreams below for an item that interests you
 19 | 2. Check if a [GitHub issue](https://github.com/open-jarvis/OpenJarvis/issues) already exists for it — if not, [open one](https://github.com/open-jarvis/OpenJarvis/issues/new/choose)
 20 | 3. Comment **"take"** on the issue to get auto-assigned
 21 | 4. Read the [Contributing Guide](https://github.com/open-jarvis/OpenJarvis/blob/main/CONTRIBUTING.md) for development setup and PR process
 22 | 
 23 | ---
 24 | 
 25 | ## Workstreams
 26 | 
 27 | OpenJarvis development is organized into **five independent workstreams**. Contributors can pick any track that matches their skills and interests — workstreams are designed to be worked on in parallel without blocking each other.
 28 | 
 29 | Every item carries a maturity tag:
 30 | 
 31 | | Tag | Meaning | Contributor guidance |
 32 | |-----|---------|---------------------|
 33 | | **Ready** | Well-scoped, implementation path is clear | Pick it up — check [issues](https://github.com/open-jarvis/OpenJarvis/issues) for a spec or write one |
 34 | | **Design Needed** | Concept is clear but needs a spec before code | Start a [design discussion](https://github.com/open-jarvis/OpenJarvis/discussions) or draft an RFC |
 35 | | **Research-Stage** | Exploratory, needs investigation before designing | Read the relevant papers, prototype, share findings |
 36 | 
 37 | ---
 38 | 
 39 | ### Workstream 1: Continuous Operators & Agents
 40 | 
 41 | Operators are OpenJarvis's key differentiator — persistent, scheduled, stateful agents that run autonomously on personal devices. The current tick-based architecture (OperatorManager → TaskScheduler → AgentExecutor → OperativeAgent) is solid but needs hardening for truly long-horizon autonomy.
 42 | 
 43 | #### Where you can help
 44 | 
 45 | | Item | Maturity | Details |
 46 | |------|----------|---------|
 47 | | Operator health checks & heartbeat monitoring | **Ready** | Add liveness probes to OperatorManager; surface in `jarvis operators status`. Detect stalled operators beyond the existing reconciliation loop. |
 48 | | Metrics collection for operator manifests | **Ready** | The `metrics` field exists in `OperatorManifest` but is not collected. Wire it to telemetry. **Good first issue.** |
 49 | | Capability policy enforcement | **Ready** | `required_capabilities` field exists in manifests but is not enforced. Connect to the existing RBAC `CapabilityPolicy` system. **Good first issue.** |
 50 | | Rate limiting per operator | **Ready** | Prevent runaway operators from hammering inference. Add configurable rate limits to OperatorManager. |
 51 | | Operator composition / chaining | **Design Needed** | Express dependencies between operators (operator A feeds results to operator B). Requires design for data passing and scheduling semantics. |
 52 | | Event-driven operators | **Design Needed** | Operators that trigger on EventBus events (e.g., new file indexed, channel message received) rather than only cron/interval schedules. |
 53 | | Operator versioning & rollback | **Design Needed** | Run v2 of an operator alongside v1. Roll back automatically on repeated failures. |
 54 | | Self-improving operators via Learning | **Research-Stage** | Operators that use trace feedback to tune their own prompts, tool selection, and routing policies through the Learning primitive. |
 55 | 
 56 | ---
 57 | 
 58 | ### Workstream 2: Mobile & Messaging Clients
 59 | 
 60 | Personal AI must be accessible from the devices people actually carry. OpenJarvis runs on laptops, workstations, and servers — users interact via their phones.
 61 | 
 62 | **Currently supported:**
 63 | 
 64 | - **iMessage + SMS** via SendBlue — bidirectional, auto-detects iMessage vs SMS, thread replies, progress updates
 65 | - **Slack** via Socket Mode (slack-bolt) — bidirectional DMs, thread replies, Slack formatting, progress updates
 66 | - **Desktop/Browser** — Interact tab with real-time streaming, tool progress, telemetry footer
 67 | 
 68 | #### Where you can help
 69 | 
 70 | | Item | Maturity | Details |
 71 | |------|----------|---------|
 72 | | WhatsApp via Meta Cloud API | **Design Needed** | Baileys protocol is blocked by WhatsApp (405 errors). Need to implement via the official Meta WhatsApp Business API. Requires Meta Business account registration. |
 73 | | WhatsApp via Baileys (workaround) | **Blocked** | WhatsApp is actively blocking unofficial Baileys connections (405 Method Not Allowed). Monitor the [Baileys repo](https://github.com/WhiskeySockets/Baileys) for protocol updates. |
 74 | | Slack rich messages (Block Kit) | **Ready** | Current Slack responses use mrkdwn formatting. Add Block Kit support for structured responses with buttons, sections, and attachments. **Good first issue.** |
 75 | | Unified notification system | **Design Needed** | Push notifications when operators complete tasks or need user attention. Requires per-channel notification adapters. |
 76 | | Signal bidirectional | **Design Needed** | Currently send-only via signal-cli REST API. Add incoming message listener with background polling. |
 77 | | Voice interface | **Research-Stage** | Speech-to-text (Whisper) → agent → text-to-speech loop over phone channels. Existing `speech/` module provides a foundation. |
 78 | | Auto-restore channels on restart | **Ready** | Slack daemon and SendBlue auto-restore from saved bindings on server restart. Need to make this more robust for edge cases. |
 79 | 
 80 | ---
 81 | 
 82 | ### Workstream 3: Secure Cloud Collaboration
 83 | 
 84 | Personal AI's core tension: local models preserve privacy but lack capability; cloud models are powerful but require trusting a provider with your data. This workstream resolves that through **Minions-style collaborative inference** (local handles context, cloud handles reasoning) and **TEE-based confidential computing** (cloud cannot see your data even during inference).
 85 | 
 86 | **References:**
 87 | 
 88 | - [Minions: Cost-Efficient Local-Cloud LLM Collaboration](https://github.com/HazyResearch/minions)
 89 | - [TEE for Confidential AI Inference](https://openreview.net/forum?id=ey87M5iKcX) ([PDF](https://openreview.net/pdf?id=ey87M5iKcX))
 90 | 
 91 | #### Where you can help
 92 | 
 93 | | Item | Maturity | Details |
 94 | |------|----------|---------|
 95 | | Query complexity analyzer | **Ready** | Classify incoming queries by difficulty to decide local vs. cloud routing. Extends the existing `MultiEngine` routing logic. |
 96 | | Cost tracking per-query | **Ready** | `CloudEngine` already has pricing data. Surface per-query cost in traces and telemetry dashboards. **Good first issue.** |
 97 | | Redaction-before-cloud pipeline | **Ready** | Wire the existing `GuardrailsEngine` in REDACT mode as a mandatory pre-step before any cloud transmission. |
 98 | | Minion protocol (sequential) | **Design Needed** | Local model extracts and summarizes long context → cloud model reasons over the compressed result. Native reimplementation of the core [Minions](https://github.com/HazyResearch/minions) idea. |
 99 | | Minion protocol (parallel) | **Design Needed** | Local and cloud models work simultaneously on different aspects of a query; results are merged. Requires a new `HybridInferenceEngine` abstraction. |
100 | | TEE attestation verification | **Design Needed** | Verify that cloud inference ran inside a trusted execution environment via cryptographic attestation. |
101 | | Taint tracking across local/cloud boundary | **Design Needed** | The `TaintSet` already tracks PII/Secret labels. Add routing enforcement so tainted data only routes to attested TEE endpoints. |
102 | | Speculative decoding (local draft + cloud verify) | **Research-Stage** | Local model generates candidate tokens; cloud model validates in parallel for latency reduction. |
103 | 
104 | ---
105 | 
106 | ### Workstream 4: Tutorials & Documentation
107 | 
108 | OpenJarvis has reference docs and four tutorials, but critical gaps remain in continuous agents, LM evaluation, learning approaches, and custom tools. Video tutorials are scoped as a contributor opportunity — written tutorials come first, with video scripts included so anyone can record.
109 | 
110 | #### Where you can help
111 | 
112 | | Item | Maturity | Details |
113 | |------|----------|---------|
114 | | "Building Continuous Agents" tutorial | **Ready** | Writing an operator TOML manifest, activating it, session persistence across ticks, daemon mode. Example: a research operator that monitors arxiv daily. |
115 | | "Adding Custom Tools" tutorial | **Ready** | Implementing `BaseTool`, registering via `ToolRegistry`, wiring into agents. Example: a weather API tool. **Good first issue.** |
116 | | "Testing & Comparing LMs" tutorial | **Ready** | Running benchmarks, comparing local vs. cloud models, interpreting telemetry (latency, cost, energy per token). Uses the existing `bench/` framework. |
117 | | Per-platform installation guides | **Ready** | Expand `installation.md` with platform-specific walkthroughs: macOS + Ollama, Ubuntu + NVIDIA + vLLM, Windows + Ollama, Raspberry Pi. **Good first issue.** |
118 | | "Learning & Model Selection" tutorial | **Design Needed** | Router policies (heuristic, learned, GRPO), proposed approaches like Thompson Sampling, trace-based reward signals. |
119 | | Video tutorial infrastructure | **Design Needed** | Establish recording workflow, hosting (YouTube), MkDocs embedding. Write video scripts alongside written tutorials. |
120 | | Interactive Jupyter notebook tutorials | **Design Needed** | Notebook versions of key tutorials for exploratory, cell-by-cell learning. |
121 | 
122 | ---
123 | 
124 | ### Workstream 5: Hardware Breadth
125 | 
126 | Personal AI means running on the hardware people actually own. Each new hardware target expands who can use OpenJarvis and generates data for the research agenda (energy, cost, latency tradeoffs across silicon).
127 | 
128 | Adding a new hardware target involves up to four components: hardware detection in `core/config.py`, an inference engine adapter in `engine/`, an energy monitor in `telemetry/`, and an entry in the GPU specs database in `telemetry/gpu_monitor.py`.
129 | 
130 | #### Where you can help
131 | 
132 | | Item | Maturity | Details |
133 | |------|----------|---------|
134 | | AMD Ryzen AI iGPU path | **Ready** | Strix Point RDNA 3.5 iGPU handles 7-8B via Vulkan. llama.cpp Vulkan backend works today. Needs hardware detection and energy monitor. **Good first issue.** |
135 | | GPU specs database expansion | **Ready** | Add Intel Arc, Jetson Orin, Snapdragon specs to `GPU_SPECS` in `telemetry/gpu_monitor.py` (TFLOPS, bandwidth, TDP). **Good first issue.** |
136 | | Intel Arc GPU (B580/B570) | **Design Needed** | 12GB VRAM, ~$250 consumer GPU. Viable for 7-8B models. Engine path: IPEX-LLM or llama.cpp SYCL backend. |
137 | | NVIDIA Jetson Orin | **Design Needed** | Best-in-class edge device. Orin NX 16GB handles 7-8B models at 15-25 tok/s. Needs hardware detection, energy monitor (tegrastats), deployment guide. |
138 | | Qualcomm Snapdragon X Elite NPU | **Design Needed** | 45 TOPS, Windows Arm laptops. ONNX Runtime + QNN Execution Provider is the viable path. |
139 | | Intel Lunar Lake NPU via OpenVINO | **Design Needed** | 48 TOPS — most mature NPU software stack for x86 laptops. New engine wrapping OpenVINO GenAI. |
140 | | Raspberry Pi 5 | **Design Needed** | CPU-only via llama.cpp ARM NEON for 1-3B models. $100 entry point for hobbyists. |
141 | | Unified hardware benchmark suite | **Design Needed** | Standardized benchmark that runs the same workloads across all supported hardware, producing comparable energy/latency/throughput/cost numbers. |
```

---

## FILE: `docs/architecture/overview.md`

- bytes: 15462
- lines: 242
- sha256: `D71F7625F7F6564BE01B9C3FDA7978FA939480BBCD19E7534838BABCE0A3DEA1`
- line terminator: LF

Line numbers below are 1-based and authoritative. Cite them.

```markdown
  1 | ---
  2 | title: Architecture Overview
  3 | description: The five-primitive architecture behind OpenJarvis — Intelligence, Engine, Agents, Tools, and Learning
  4 | search:
  5 |   boost: 2
  6 | ---
  7 | 
  8 | # Architecture Overview
  9 | 
 10 | OpenJarvis is a research framework for studying on-device AI systems. Its architecture is organized around **five core abstractions** -- Intelligence, Engine, Agentic Logic, Memory, and Learning -- that work together through trace-driven feedback.
 11 | 
 12 | ![OpenJarvis Architecture](../assets/OpenJarvis_Architecture.png)
 13 | 
 14 | ---
 15 | 
 16 | ## Primitive Descriptions
 17 | 
 18 | ### Intelligence
 19 | 
 20 | The Intelligence primitive handles **model definition and catalog**. It maintains a catalog of known models (`BUILTIN_MODELS`) with metadata such as parameter count, context length, VRAM requirements, and supported engines. The `IntelligenceConfig` captures the full identity of the configured model — its weight path, quantization format, preferred engine, fallback chain, and generation defaults (`temperature`, `max_tokens`, `top_p`, `top_k`, `repetition_penalty`, `stop_sequences`).
 21 | 
 22 | Models discovered at runtime from running engines are automatically merged into the `ModelRegistry`, so the system always has an up-to-date view of what is available. Query routing has moved to the Learning primitive — see the [Learning & Traces](learning.md) documentation.
 23 | 
 24 | ### Engine
 25 | 
 26 | The Engine primitive provides the **inference runtime** — the layer that actually runs language models. All backends implement the `InferenceEngine` ABC with a uniform interface: `generate()`, `stream()`, `list_models()`, and `health()`. Supported backends include Ollama, vLLM, SGLang, llama.cpp, and Cloud (OpenAI, Anthropic, Google).
 27 | 
 28 | Each engine is configured via its own sub-section in `config.toml` (e.g., `[engine.ollama]`, `[engine.vllm]`, `[engine.llamacpp]`). Engine discovery probes all registered backends for health, returning healthy engines sorted with the user's configured default first. The system automatically falls back to any available engine if the preferred one is unavailable.
 29 | 
 30 | ### Agentic Logic
 31 | 
 32 | The Agentic Logic primitive implements **pluggable agents** that handle queries with varying levels of sophistication. The agent hierarchy is organized around `BaseAgent` (ABC with concrete helpers) and `ToolUsingAgent` (intermediate base for agents that accept tools, with `accepts_tools = True`). Nine agent types are available: `SimpleAgent` (single-turn, no tools), `OrchestratorAgent` (multi-turn tool-calling loop with function_calling and structured modes), `NativeReActAgent` (Thought-Action-Observation loop), `NativeOpenHandsAgent` (CodeAct-style code execution), `RLMAgent` (recursive LM with persistent REPL), `OpenHandsAgent` (wraps real `openhands-sdk`), `ClaudeCodeAgent` (Claude Agent SDK via Node.js subprocess), `OperativeAgent` (persistent scheduled agent with state management), and `MonitorOperativeAgent` (long-horizon agent with configurable strategy axes).
 33 | 
 34 | The sandbox module (`openjarvis.sandbox`) adds a `SandboxedAgent` wrapper that runs any `BaseAgent` inside a Docker or Podman container with mount-security enforcement, and a `ContainerRunner` that manages the container lifecycle.
 35 | 
 36 | Agent behavior is configured through `[agent]` in `config.toml`, including the default agent, turn limits, tool list, optional system prompt, and the `context_from_memory` flag (previously `context_injection`) that controls automatic memory context injection. Sandbox configuration lives in `[sandbox]`. All agents implement the `BaseAgent` ABC with a `run()` method, and are registered via `@AgentRegistry.register("name")`.
 37 | 
 38 | ### Memory
 39 | 
 40 | The Memory primitive provides **persistent, searchable storage** for documents and knowledge. Five backends are available: SQLite/FTS5 (zero-dependency default), FAISS (dense vector retrieval), ColBERTv2 (late interaction), BM25 (classic term-frequency), and Hybrid (Reciprocal Rank Fusion of sparse + dense). Storage backends are configured under `[tools.storage]` in `config.toml` (the `[memory]` section is still accepted as a backward-compatible alias).
 41 | 
 42 | The memory pipeline includes document ingestion, chunking, embedding generation, and context injection. When a user sends a query and `agent.context_from_memory` is enabled, relevant documents are retrieved and prepended to the prompt with source attribution.
 43 | 
 44 | ### Learning & Traces
 45 | 
 46 | The Learning system is the fifth primitive, connecting the other four through **trace-driven feedback**. Every agent interaction can produce a `Trace` capturing the full sequence of steps — routing decisions, memory retrieval, inference calls, tool invocations, and final responses. The `TraceAnalyzer` computes statistics from accumulated traces, and the `TraceDrivenPolicy` uses these statistics to learn which model/agent/tool combinations produce the best outcomes for different query types.
 47 | 
 48 | The learning system is configured through nested sub-sections in `config.toml`: `[learning.routing]` controls the router policy (heuristic, learned, sft, grpo), `[learning.intelligence]` controls the model-level learning policy, `[learning.agent]` controls agent advisor and ICL updater policies, and `[learning.metrics]` sets the composite reward function weights. The pillar also includes LLM-guided spec search, a frontier-driven loop that improves the local harness — see [Learning architecture: LLM-guided spec search](learning.md#llm-guided-spec-search-frontier-driven-harness-learning).
 49 | 
 50 | ---
 51 | 
 52 | ## The Registry Pattern
 53 | 
 54 | All extensible components in OpenJarvis use a **decorator-based registry** for runtime discovery. The pattern is implemented in `RegistryBase[T]`, a generic base class that provides isolated storage per typed subclass.
 55 | 
 56 | ```python
 57 | from openjarvis.core.registry import EngineRegistry
 58 | 
 59 | @EngineRegistry.register("ollama")
 60 | class OllamaEngine(InferenceEngine):
 61 |     ...
 62 | ```
 63 | 
 64 | Each registry provides:
 65 | 
 66 | | Method | Description |
 67 | |--------|-------------|
 68 | | `register(key)` | Decorator that registers a class under a key |
 69 | | `register_value(key, value)` | Imperative registration |
 70 | | `get(key)` | Retrieve by key (raises `KeyError` if missing) |
 71 | | `create(key, *args, **kwargs)` | Look up and instantiate |
 72 | | `items()` | All `(key, entry)` pairs |
 73 | | `keys()` | All registered keys |
 74 | | `contains(key)` | Check if key exists |
 75 | | `clear()` | Remove all entries (for tests) |
 76 | 
 77 | **Typed registries** in the system:
 78 | 
 79 | | Registry | Type Parameter | Purpose |
 80 | |----------|---------------|---------|
 81 | | `ModelRegistry` | `Any` (ModelSpec) | Model metadata |
 82 | | `EngineRegistry` | `Type[InferenceEngine]` | Inference backends |
 83 | | `MemoryRegistry` | `Type[MemoryBackend]` | Memory backends |
 84 | | `AgentRegistry` | `Type[BaseAgent]` | Agent implementations |
 85 | | `ToolRegistry` | `Any` (BaseTool classes) | Tool implementations |
 86 | | `RouterPolicyRegistry` | `Any` (RouterPolicy classes) | Router policies |
 87 | | `BenchmarkRegistry` | `Any` (BaseBenchmark classes) | Benchmark implementations |
 88 | | `ChannelRegistry` | `Any` (BaseChannel classes) | Channel implementations |
 89 | 
 90 | !!! info "Adding a new component"
 91 |     To add a new backend, implement the appropriate ABC and decorate it with
 92 |     the corresponding registry decorator. No factory modifications are needed --
 93 |     the component becomes automatically discoverable at runtime.
 94 | 
 95 | ---
 96 | 
 97 | ## Source Directory Layout
 98 | 
 99 | ```
100 | src/openjarvis/
101 |     core/               Core infrastructure shared by all primitives
102 |         registry.py         RegistryBase[T] and typed subclass registries
103 |         types.py            Message, ModelSpec, Trace, TelemetryRecord, etc.
104 |         config.py           JarvisConfig, hardware detection, TOML loading
105 |         events.py           EventBus pub/sub system (EventType, Event)
106 | 
107 |     intelligence/       Intelligence primitive -- model definition & catalog
108 |         model_catalog.py    BUILTIN_MODELS list, merge_discovered_models()
109 |         _stubs.py           (backward-compat shim -- re-exports from learning._stubs)
110 |         router.py           (backward-compat shim -- re-exports from learning.router)
111 | 
112 |     engine/             Engine primitive -- inference runtime backends
113 |         _stubs.py           InferenceEngine ABC
114 |         _base.py            EngineConnectionError, messages_to_dicts()
115 |         _openai_compat.py   Shared base for OpenAI-compatible engines
116 |         _discovery.py       discover_engines(), discover_models(), get_engine()
117 |         ollama.py           Ollama backend (native HTTP API)
118 |         openai_compat_engines.py  Data-driven registration (vLLM, SGLang, llama.cpp, MLX, LM Studio)
119 |         cloud.py            Cloud backend (OpenAI, Anthropic, Google SDKs)
120 | 
121 |     agents/             Agentic Logic primitive -- pluggable agents
122 |         _stubs.py           BaseAgent ABC, ToolUsingAgent, AgentContext, AgentResult
123 |         simple.py           SimpleAgent (single-turn, no tools)
124 |         orchestrator.py     OrchestratorAgent (multi-turn tool loop, function_calling + structured)
125 |         native_react.py     NativeReActAgent (Thought-Action-Observation loop)
126 |         native_openhands.py NativeOpenHandsAgent (CodeAct-style code execution)
127 |         rlm.py              RLMAgent (recursive LM with persistent REPL)
128 |         openhands.py        OpenHandsAgent (wraps real openhands-sdk)
129 |         react.py            Backward-compat shim (re-exports NativeReActAgent as ReActAgent)
130 |         claude_code.py      ClaudeCodeAgent (Claude Agent SDK via Node.js subprocess)
131 |         claude_code_runner/ Bundled Node.js runner for the Claude Agent SDK
132 | 
133 |     sandbox/            Container sandbox for isolated agent execution
134 |         runner.py           ContainerRunner (Docker/Podman lifecycle), SandboxedAgent wrapper
135 |         mount_security.py   MountAllowlist, validate_mounts() (path security)
136 | 
137 |     memory/             Memory primitive -- persistent searchable storage
138 |         _stubs.py           MemoryBackend ABC, RetrievalResult
139 |         sqlite.py           SQLite/FTS5 backend (zero-dependency default)
140 |         faiss_backend.py    FAISS dense retrieval backend
141 |         colbert_backend.py  ColBERTv2 late interaction backend
142 |         bm25.py             BM25 (Okapi) term-frequency backend
143 |         hybrid.py           Hybrid RRF fusion backend
144 |         chunking.py         ChunkConfig, Chunk, chunk_text()
145 |         ingest.py           Document ingestion (file reading, directory walking)
146 |         context.py          Context injection (inject_context, source attribution)
147 |         embeddings.py       Embedder ABC, SentenceTransformerEmbedder
148 | 
149 |     learning/           Learning system -- router policies & rewards
150 |         _stubs.py           RouterPolicy ABC, QueryAnalyzer ABC, RewardFunction ABC, RoutingContext
151 |         router.py           HeuristicRouter, DefaultQueryAnalyzer, build_routing_context()
152 |         heuristic_policy.py Wires HeuristicRouter into RouterPolicyRegistry
153 |         trace_policy.py     TraceDrivenPolicy (learns from trace outcomes)
154 |         grpo_policy.py      GRPORouterPolicy (stub for future RL)
155 |         heuristic_reward.py HeuristicRewardFunction (latency/cost/efficiency)
156 | 
157 |     traces/             Trace system -- interaction recording
158 |         store.py            TraceStore (SQLite persistence)
159 |         collector.py        TraceCollector (wraps agents, records traces)
160 |         analyzer.py         TraceAnalyzer (aggregated statistics)
161 | 
162 |     tools/              Tool system -- pluggable tool implementations
163 |         _stubs.py           BaseTool ABC, ToolSpec, ToolExecutor
164 |         calculator.py       CalculatorTool (ast-based safe eval)
165 |         think.py            ThinkTool (reasoning scratchpad)
166 |         retrieval.py        RetrievalTool (memory search)
167 |         llm.py              LLMTool (sub-model calls)
168 |         file_read.py        FileReadTool (safe file reading)
169 | 
170 |     telemetry/          Telemetry -- inference metrics recording
171 |         store.py            TelemetryStore (SQLite, EventBus subscription)
172 |         aggregator.py       TelemetryAggregator (per-model/engine stats)
173 |         wrapper.py          instrumented_generate() wrapper
174 | 
175 |     server/             API server -- OpenAI-compatible HTTP API
176 |         app.py              FastAPI application factory
177 |         routes.py           /v1/chat/completions, /v1/models, /health
178 | 
179 |     bench/              Benchmarking framework
180 |         _stubs.py           BaseBenchmark ABC, BenchmarkSuite
181 |         latency.py          LatencyBenchmark (per-call latency)
182 |         throughput.py       ThroughputBenchmark (tokens/second)
183 | 
184 |     security/           Security guardrails
185 |         _stubs.py           BaseScanner ABC
186 |         types.py            ThreatLevel, RedactionMode, ScanFinding, ScanResult
187 |         scanner.py          SecretScanner, PIIScanner
188 |         guardrails.py       GuardrailsEngine (wraps InferenceEngine)
189 |         file_policy.py      is_sensitive_file(), DEFAULT_SENSITIVE_PATTERNS
190 |         audit.py            AuditLogger (SQLite security events)
191 | 
192 |     channels/           Channel messaging
193 |         _stubs.py           BaseChannel ABC, ChannelMessage, ChannelStatus
194 |         whatsapp_baileys.py WhatsAppBaileysChannel (Baileys protocol via Node.js bridge)
195 |         whatsapp_baileys_bridge/ Bundled Node.js Baileys bridge
196 | 
197 |     scheduler/          Task scheduling system
198 |         scheduler.py        TaskScheduler (cron/interval/once, background polling)
199 |         store.py            SchedulerStore (SQLite persistence + run logs)
200 |         tools.py            MCP scheduler tools (schedule_task, list, pause, resume, cancel)
201 | 
202 |     cli/                CLI commands (Click-based)
203 |         ask.py              jarvis ask -- query the assistant
204 |         serve.py            jarvis serve -- start API server
205 | 
206 |     sdk.py              Jarvis class -- high-level Python SDK
207 |     mcp/                MCP (Model Context Protocol) layer
208 | ```
209 | 
210 | ---
211 | 
212 | ## How the Primitives Interact
213 | 
214 | ### EventBus: The Connective Tissue
215 | 
216 | All primitives communicate through a **thread-safe pub/sub EventBus** defined in `core/events.py`. The bus uses synchronous dispatch -- subscribers are called in registration order within the publishing thread.
217 | 
218 | **Event types** in the system:
219 | 
220 | | Event | Publisher | Purpose |
221 | |-------|----------|---------|
222 | | `INFERENCE_START` / `INFERENCE_END` | Engine / Agent | Track inference calls |
223 | | `TOOL_CALL_START` / `TOOL_CALL_END` | ToolExecutor | Track tool usage |
224 | | `MEMORY_STORE` / `MEMORY_RETRIEVE` | Memory backends | Track memory operations |
225 | | `AGENT_TURN_START` / `AGENT_TURN_END` | Agents | Track agent lifecycle |
226 | | `TELEMETRY_RECORD` | TelemetryStore | Publish telemetry records |
227 | | `TRACE_STEP` / `TRACE_COMPLETE` | TraceCollector | Trace lifecycle events |
228 | | `CHANNEL_MESSAGE_RECEIVED` / `CHANNEL_MESSAGE_SENT` | WhatsAppBaileysChannel | Track channel messaging |
229 | | `SECURITY_SCAN` / `SECURITY_ALERT` / `SECURITY_BLOCK` | GuardrailsEngine | Track security scanning |
230 | | `scheduler_task_start` / `scheduler_task_end` | TaskScheduler | Track scheduled task execution |
231 | 
232 | ### Dependency Flow
233 | 
234 | The primitives form a directed dependency graph:
235 | 
236 | 1. **Agentic Logic** depends on Engine (for inference) and Memory (for context)
237 | 2. **Intelligence** provides model selection to agents via Learning policies
238 | 3. **Learning** reads from Traces, which are produced by Agentic Logic
239 | 4. **Memory** is independent but consumed by agents and tools
240 | 5. **Engine** is independent but consumed by agents and the SDK
241 | 
242 | This creates a feedback loop: agents produce traces, traces inform learning, learning improves routing, and better routing improves agent performance.
```

---

## FILE: `docs/architecture/agents.md`

- bytes: 22888
- lines: 567
- sha256: `032FC4D346D8407859194FAE6F516F6FA1A759661D4C6552C5AE7CFB74799BF2`
- line terminator: LF

Line numbers below are 1-based and authoritative. Cite them.

```markdown
  1 | # Agentic Logic Primitive
  2 | 
  3 | The Agentic Logic primitive provides **pluggable agents** that handle queries with varying levels of sophistication -- from simple single-turn responses to multi-turn tool-calling loops, ReAct-style reasoning, CodeAct code execution, recursive decomposition, and external agent communication.
  4 | 
  5 | ---
  6 | 
  7 | ## BaseAgent ABC
  8 | 
  9 | All agents implement the `BaseAgent` abstract base class, which provides both the `run()` contract and concrete helper methods that eliminate boilerplate in subclasses:
 10 | 
 11 | ```python
 12 | class BaseAgent(ABC):
 13 |     agent_id: str
 14 |     accepts_tools: bool = False  # overridden by ToolUsingAgent
 15 | 
 16 |     def __init__(
 17 |         self,
 18 |         engine: InferenceEngine,
 19 |         model: str,
 20 |         *,
 21 |         bus: Optional[EventBus] = None,
 22 |         temperature: float = 0.7,
 23 |         max_tokens: int = 1024,
 24 |     ) -> None: ...
 25 | 
 26 |     @abstractmethod
 27 |     def run(
 28 |         self,
 29 |         input: str,
 30 |         context: Optional[AgentContext] = None,
 31 |         **kwargs: Any,
 32 |     ) -> AgentResult:
 33 |         """Execute the agent on *input* and return an AgentResult."""
 34 | ```
 35 | 
 36 | ### Class Attribute: `accepts_tools`
 37 | 
 38 | The `accepts_tools` class attribute (default `False`) enables the CLI and SDK to auto-detect which agents support tool-passing. Agents that set `accepts_tools = True` can receive `--tools` on the CLI and `tools=` in the SDK.
 39 | 
 40 | ### Concrete Helper Methods
 41 | 
 42 | `BaseAgent` provides five concrete helpers that subclasses use to avoid duplicating common logic:
 43 | 
 44 | | Helper | Purpose |
 45 | |--------|---------|
 46 | | `_emit_turn_start(input)` | Publish `AGENT_TURN_START` on the event bus |
 47 | | `_emit_turn_end(**data)` | Publish `AGENT_TURN_END` on the event bus |
 48 | | `_build_messages(input, context, *, system_prompt)` | Assemble the message list from optional system prompt, conversation context, and user input |
 49 | | `_generate(messages, **extra_kwargs)` | Call `engine.generate()` with stored defaults (model, temperature, max_tokens) |
 50 | | `_max_turns_result(tool_results, turns, content)` | Build the standard `AgentResult` for when `max_turns` is exceeded |
 51 | | `_strip_think_tags(text)` | Remove `<think>...</think>` blocks from model output (static method) |
 52 | 
 53 | ### The `run()` Contract
 54 | 
 55 | The `run()` method is the single entry point for all agent implementations. It receives:
 56 | 
 57 | - **`input`** -- The user's query text
 58 | - **`context`** -- An optional `AgentContext` with conversation history, tool names, and memory results
 59 | - **`**kwargs`** -- Additional implementation-specific parameters
 60 | 
 61 | It returns an `AgentResult` containing the response content, any tool results, the number of turns taken, and metadata.
 62 | 
 63 | ### Supporting Dataclasses
 64 | 
 65 | ```python
 66 | @dataclass(slots=True)
 67 | class AgentContext:
 68 |     conversation: Conversation    # Prior messages for multi-turn context
 69 |     tools: List[str]              # Available tool names
 70 |     memory_results: List[Any]     # Pre-fetched memory search results
 71 |     metadata: Dict[str, Any]      # Arbitrary key-value pairs
 72 | 
 73 | @dataclass(slots=True)
 74 | class AgentResult:
 75 |     content: str                  # The agent's response text
 76 |     tool_results: List[ToolResult]  # Results from tool invocations
 77 |     turns: int                    # Number of inference turns taken
 78 |     metadata: Dict[str, Any]      # Arbitrary metadata
 79 | ```
 80 | 
 81 | ---
 82 | 
 83 | ## ToolUsingAgent
 84 | 
 85 | `ToolUsingAgent` is an intermediate base class for agents that accept and use tools. It extends `BaseAgent` with:
 86 | 
 87 | - **`accepts_tools = True`** -- Enables CLI/SDK tool introspection
 88 | - **`ToolExecutor`** -- Initialized from the provided tool list, handles dispatch with JSON argument parsing, latency tracking, and event bus integration
 89 | - **`max_turns`** -- Configurable loop iteration limit (default: 10)
 90 | 
 91 | ```python
 92 | class ToolUsingAgent(BaseAgent):
 93 |     accepts_tools: bool = True
 94 | 
 95 |     def __init__(
 96 |         self,
 97 |         engine: InferenceEngine,
 98 |         model: str,
 99 |         *,
100 |         tools: Optional[List[BaseTool]] = None,
101 |         bus: Optional[EventBus] = None,
102 |         max_turns: int = 10,
103 |         temperature: float = 0.7,
104 |         max_tokens: int = 1024,
105 |     ) -> None: ...
106 | ```
107 | 
108 | All tool-using agents (`OrchestratorAgent`, `NativeReActAgent`, `NativeOpenHandsAgent`, `RLMAgent`) extend this class.
109 | 
110 | !!! info "Agents that bypass ToolUsingAgent"
111 |     Some agents extend `BaseAgent` directly and set `accepts_tools = False`: `SimpleAgent` (single-turn, no tools), `OpenHandsAgent` (tool management is handled by the openhands-sdk), and `ClaudeCodeAgent` (tools are managed by the Claude Agent SDK). `SandboxedAgent` also extends `BaseAgent` directly because it wraps another agent rather than calling tools itself.
112 | 
113 | ---
114 | 
115 | ## Choosing an Agent
116 | 
117 | Start here. Pick the simplest agent that handles your task — simpler agents are faster, use fewer tokens, and are easier to debug. Reach for more complex agents only when the task demands it.
118 | 
119 | | Use case | Agent | Why |
120 | |---|---|---|
121 | | Simple Q&A, single-turn | `simple` | No overhead, one inference call |
122 | | Multi-step with tools (calculator, search, files) | `orchestrator` | Function-calling loop, most compatible with OpenAI-format models |
123 | | Explicit reasoning chains | `native_react` | Thought-Action-Observation loop based on [ReAct (Yao et al., 2023)](https://arxiv.org/abs/2210.03629); reasoning traces are visible and debuggable |
124 | | Code generation + execution | `native_openhands` | CodeAct pattern inspired by [OpenHands (Wang et al., 2024)](https://arxiv.org/abs/2407.16741); generates and executes Python inline |
125 | | Long documents, recursive decomposition | `rlm` | Stores context in a persistent REPL, decomposes via recursive sub-LM calls |
126 | | Untrusted inputs | `sandboxed` wrapping any agent | Container isolation with network disabled and mount allowlists |
127 | 
128 | **General guidance:** `orchestrator` is the default for most tool-using tasks. Use `native_react` when you want visible reasoning traces (e.g., for debugging or auditing agent behavior). Use `native_openhands` when the task involves writing and running code. Use `rlm` when context is too long to fit in a single prompt window.
129 | 
130 | ---
131 | 
132 | ## Agent Implementations
133 | 
134 | ### SimpleAgent
135 | 
136 | **Registry key:** `simple`
137 | 
138 | The simplest agent implementation -- a single-turn, no-tool query-to-response pipeline. Extends `BaseAgent` directly (does not accept tools).
139 | 
140 | ```mermaid
141 | graph LR
142 |     Q["User Query"] --> M["Build Messages"]
143 |     M --> E["Engine.generate()"]
144 |     E --> R["AgentResult"]
145 | ```
146 | 
147 | How it works:
148 | 
149 | 1. Calls `_emit_turn_start()` to publish `AGENT_TURN_START` on the event bus
150 | 2. Calls `_build_messages()` to assemble the message list from conversation context plus user input
151 | 3. Calls `_generate()` to invoke the engine with stored defaults
152 | 4. Calls `_emit_turn_end()` and returns an `AgentResult` with `turns=1`
153 | 
154 | ```python
155 | from openjarvis.agents.simple import SimpleAgent
156 | 
157 | agent = SimpleAgent(engine, model="qwen3:8b", bus=bus)
158 | result = agent.run("What is the capital of France?")
159 | print(result.content)  # "The capital of France is Paris."
160 | ```
161 | 
162 | ### OrchestratorAgent
163 | 
164 | **Registry key:** `orchestrator`
165 | 
166 | A multi-turn agent that implements a **tool-calling loop**. Extends `ToolUsingAgent`. The LLM can request tool invocations, and the results are fed back for further processing until the model produces a final text response.
167 | 
168 | Supports two modes:
169 | 
170 | - **`function_calling`** (default) -- Uses OpenAI function-calling format via `ToolExecutor.get_openai_tools()`
171 | - **`structured`** -- Uses structured output format for models that support it
172 | 
173 | ```mermaid
174 | graph TD
175 |     Q["User Query"] --> BUILD["Build messages +<br/>tool definitions"]
176 |     BUILD --> GEN["Engine.generate()<br/>with tools"]
177 |     GEN --> CHECK{"Tool calls<br/>in response?"}
178 |     CHECK -->|No| DONE["Return final answer"]
179 |     CHECK -->|Yes| EXEC["Execute each tool<br/>via ToolExecutor"]
180 |     EXEC --> APPEND["Append tool results<br/>to messages"]
181 |     APPEND --> MAXCHECK{"Max turns<br/>exceeded?"}
182 |     MAXCHECK -->|No| GEN
183 |     MAXCHECK -->|Yes| TIMEOUT["Return with<br/>max_turns_exceeded"]
184 | ```
185 | 
186 | How it works:
187 | 
188 | 1. Builds initial messages from context and user input
189 | 2. Converts available tools to OpenAI function-calling format via `ToolExecutor.get_openai_tools()`
190 | 3. Enters a loop (up to `max_turns` iterations):
191 |     - Calls `engine.generate()` with messages and tool definitions
192 |     - If the response contains `tool_calls`, executes each tool and appends the results as `TOOL` messages
193 |     - If no `tool_calls` are present, returns the content as the final answer
194 | 4. If `max_turns` is exceeded, returns the last content or a warning message
195 | 
196 | ```python
197 | from openjarvis.agents.orchestrator import OrchestratorAgent
198 | from openjarvis.tools.calculator import CalculatorTool
199 | from openjarvis.tools.think import ThinkTool
200 | 
201 | agent = OrchestratorAgent(
202 |     engine,
203 |     model="qwen3:8b",
204 |     tools=[CalculatorTool(), ThinkTool()],
205 |     bus=bus,
206 |     max_turns=10,
207 | )
208 | result = agent.run("What is 2^10 + 3^5?")
209 | # The agent may call the calculator tool, get "1267", then respond
210 | ```
211 | 
212 | ### NativeReActAgent
213 | 
214 | **Registry key:** `native_react` (alias: `react`)
215 | 
216 | A ReAct (Reasoning + Acting) agent that implements a **Thought-Action-Observation** loop. Extends `ToolUsingAgent`. The LLM is prompted to output structured text with `Thought:`, `Action:`, `Action Input:`, and `Final Answer:` fields, which the agent parses to drive tool execution.
217 | 
218 | ```mermaid
219 | graph TD
220 |     Q["User Query"] --> SYS["Build system prompt<br/>with tool descriptions"]
221 |     SYS --> GEN["Generate response"]
222 |     GEN --> PARSE["Parse ReAct output"]
223 |     PARSE --> FINAL{"Final Answer?"}
224 |     FINAL -->|Yes| DONE["Return answer"]
225 |     FINAL -->|No| ACTION{"Has Action?"}
226 |     ACTION -->|No| DONE2["Return content as-is"]
227 |     ACTION -->|Yes| EXEC["Execute tool<br/>via ToolExecutor<br/>(case-insensitive)"]
228 |     EXEC --> OBS["Append Observation"]
229 |     OBS --> MAXCHECK{"Max turns<br/>exceeded?"}
230 |     MAXCHECK -->|No| GEN
231 |     MAXCHECK -->|Yes| TIMEOUT["Return max_turns_result"]
232 | ```
233 | 
234 | How it works:
235 | 
236 | 1. Builds a system prompt with enriched tool descriptions via `build_tool_descriptions()`. Parsing is case-insensitive.
237 | 2. Generates a response and parses the ReAct-structured output
238 | 3. If a `Final Answer:` is found, returns it
239 | 4. If an `Action:` is found, executes the tool and feeds the result back as an `Observation:`
240 | 5. Loops until a final answer is produced or `max_turns` is exceeded
241 | 
242 | !!! note "Backward compatibility"
243 |     The old `from openjarvis.agents.react import ReActAgent` import path still works via a backward-compat shim. The registry alias `"react"` also maps to `NativeReActAgent`.
244 | 
245 | ```python
246 | from openjarvis.agents.native_react import NativeReActAgent
247 | 
248 | agent = NativeReActAgent(
249 |     engine,
250 |     model="qwen3:8b",
251 |     tools=[CalculatorTool(), ThinkTool()],
252 |     max_turns=10,
253 | )
254 | result = agent.run("What is the square root of 256?")
255 | ```
256 | 
257 | ### NativeOpenHandsAgent
258 | 
259 | **Registry key:** `native_openhands`
260 | 
261 | A CodeAct-style agent that generates and executes Python code. Extends `ToolUsingAgent`. It can also invoke tools via structured `Action:` / `Action Input:` output. URLs in the input are automatically pre-fetched and inlined for the LLM.
262 | 
263 | How it works:
264 | 
265 | 1. Builds a detailed system prompt with enriched tool descriptions (via shared `build_tool_descriptions()` builder) and code execution instructions
266 | 2. Pre-fetches any URLs in the user input, inlining the content directly
267 | 3. For each turn:
268 |     - Generates a response and strips `<think>` tags
269 |     - If a `\`\`\`python` code block is found, executes it via `code_interpreter`
270 |     - If an `Action:` / `Action Input:` is found, dispatches the tool
271 |     - If neither is found, returns the content as the final answer
272 | 4. Handles context window overflow with automatic truncation
273 | 
274 | ```python
275 | from openjarvis.agents.native_openhands import NativeOpenHandsAgent
276 | 
277 | agent = NativeOpenHandsAgent(
278 |     engine,
279 |     model="qwen3:8b",
280 |     tools=[CalculatorTool(), WebSearchTool()],
281 |     max_turns=3,
282 |     max_tokens=2048,
283 | )
284 | result = agent.run("Summarize https://example.com/article")
285 | ```
286 | 
287 | ### RLMAgent
288 | 
289 | **Registry key:** `rlm`
290 | 
291 | A Recursive Language Model agent based on the [RLM paper](https://arxiv.org/abs/2512.24601). Instead of passing long context directly in the LLM prompt, RLM stores context as a Python variable in a persistent REPL. A "Root LM" writes Python code to inspect, decompose, and process context using recursive sub-LM calls via `llm_query()` and `llm_batch()`. Extends `ToolUsingAgent`.
292 | 
293 | ```mermaid
294 | graph TD
295 |     Q["User Query +<br/>Context"] --> REPL["Create persistent REPL<br/>(context stored as variable)"]
296 |     REPL --> GEN["Generate code"]
297 |     GEN --> CODE{"Code block<br/>found?"}
298 |     CODE -->|No| DONE["Return content<br/>as final answer"]
299 |     CODE -->|Yes| EXEC["Execute in REPL"]
300 |     EXEC --> TERM{"FINAL() called?"}
301 |     TERM -->|Yes| RESULT["Return final answer"]
302 |     TERM -->|No| FEED["Feed output back<br/>as user message"]
303 |     FEED --> MAXCHECK{"Max turns<br/>exceeded?"}
304 |     MAXCHECK -->|No| GEN
305 |     MAXCHECK -->|Yes| TIMEOUT["Return max_turns_result"]
306 | ```
307 | 
308 | How it works:
309 | 
310 | 1. Creates a persistent REPL with `llm_query()` and `llm_batch()` callbacks. Tool descriptions are injected via the shared `build_tool_descriptions()` builder when tools are provided.
311 | 2. Injects context from `AgentContext` metadata or memory results into the REPL as a variable
312 | 3. Generates code and executes it in the REPL
313 | 4. If `FINAL(value)` or `FINAL_VAR("name")` is called, returns the final answer
314 | 5. If no code block is found, treats the content as a direct answer
315 | 
316 | The agent supports configurable sub-model parameters for recursive calls:
317 | 
318 | | Parameter | Default | Description |
319 | |-----------|---------|-------------|
320 | | `sub_model` | same as `model` | Model for sub-LM calls |
321 | | `sub_temperature` | `0.3` | Temperature for sub-LM calls |
322 | | `sub_max_tokens` | `1024` | Max tokens for sub-LM calls |
323 | | `max_output_chars` | `10000` | Max REPL output characters |
324 | | `system_prompt` | `RLM_SYSTEM_PROMPT` | Override the system prompt |
325 | 
326 | ```python
327 | from openjarvis.agents.rlm import RLMAgent
328 | 
329 | agent = RLMAgent(
330 |     engine,
331 |     model="qwen3:8b",
332 |     max_turns=10,
333 |     sub_model="qwen3:1.7b",  # smaller model for sub-queries
334 |     sub_temperature=0.3,
335 | )
336 | result = agent.run("Summarize this document", context=ctx)
337 | ```
338 | 
339 | ### OpenHandsAgent (SDK)
340 | 
341 | **Registry key:** `openhands`
342 | 
343 | A thin wrapper around the real `openhands-sdk` package for AI-driven software development tasks. Extends `BaseAgent` directly (does not use `ToolUsingAgent` since tool management is handled by the SDK).
344 | 
345 | !!! warning "Optional dependency"
346 |     This agent requires the `openhands-sdk` package (`uv sync --extra openhands`). The SDK requires Python 3.12+.
347 | 
348 | How it works:
349 | 
350 | 1. Imports `openhands.sdk` at runtime (lazy import)
351 | 2. Creates an LLM, Agent, and Conversation from the SDK
352 | 3. Sends the user input as a message and runs the conversation
353 | 4. Extracts the final message content from the conversation
354 | 
355 | ```python
356 | from openjarvis.agents.openhands import OpenHandsAgent
357 | 
358 | agent = OpenHandsAgent(
359 |     engine,
360 |     model="gpt-4",
361 |     workspace="/path/to/project",
362 |     api_key="sk-...",
363 | )
364 | result = agent.run("Fix the failing test in test_utils.py")
365 | ```
366 | 
367 | ### ClaudeCodeAgent
368 | 
369 | **Registry key:** `claude_code`
370 | 
371 | Wraps the `@anthropic-ai/claude-code` SDK via a bundled Node.js subprocess bridge. Unlike every other agent, inference is handled entirely by the Claude Agent SDK -- the OpenJarvis inference engine is not used. This makes `ClaudeCodeAgent` a true external agent, similar in spirit to `OpenHandsAgent` but implemented via subprocess rather than an importable Python SDK.
372 | 
373 | ```mermaid
374 | graph LR
375 |     Q["User Query"] --> PY["Python: build JSON request"]
376 |     PY --> SPAWN["Spawn: node dist/index.js"]
377 |     SPAWN --> NODE["Node.js runner<br/>@anthropic-ai/claude-code SDK"]
378 |     NODE --> SDK["Claude Agent SDK<br/>(cloud inference)"]
379 |     SDK --> NODE
380 |     NODE --> JSON["Sentinel-delimited JSON<br/>on stdout"]
381 |     JSON --> PARSE["Python: parse output"]
382 |     PARSE --> R["AgentResult"]
383 | ```
384 | 
385 | How it works:
386 | 
387 | 1. On first call, copies the bundled `claude_code_runner/` to `~/.openjarvis/claude_code_runner/` and runs `npm install --production` if `node_modules` is absent
388 | 2. Builds a JSON request with `prompt`, `api_key`, `workspace`, `allowed_tools`, `system_prompt`, and `session_id`
389 | 3. Spawns `node dist/index.js` and writes the request to stdin
390 | 4. Reads stdout and extracts the JSON payload between `---OPENJARVIS_OUTPUT_START---` and `---OPENJARVIS_OUTPUT_END---` sentinels
391 | 5. Falls back to treating all stdout as plain text content if sentinels are absent
392 | 
393 | !!! warning "Requires Node.js 22+"
394 |     `ClaudeCodeAgent` raises `RuntimeError` at `run()` time if `node` is not found on `PATH`. An `ANTHROPIC_API_KEY` environment variable is required for the Claude Agent SDK to authenticate.
395 | 
396 | ```python
397 | from openjarvis.agents.claude_code import ClaudeCodeAgent
398 | 
399 | agent = ClaudeCodeAgent(
400 |     engine=None,   # not used
401 |     model="",      # not used
402 |     workspace="/path/to/project",
403 |     timeout=120,
404 | )
405 | result = agent.run("Add type hints to all functions in utils.py")
406 | ```
407 | 
408 | ### SandboxedAgent and ContainerRunner
409 | 
410 | `SandboxedAgent` and `ContainerRunner` together implement **container-isolated agent execution** following the `GuardrailsEngine` wrapper pattern. `SandboxedAgent` wraps any `BaseAgent` and delegates execution to a Docker (or Podman) container managed by `ContainerRunner`.
411 | 
412 | ```mermaid
413 | graph LR
414 |     Q["User Query"] --> SA["SandboxedAgent.run()"]
415 |     SA --> CR["ContainerRunner.run()"]
416 |     CR --> VALIDATE["Validate mounts<br/>vs allowlist"]
417 |     VALIDATE --> DOCKER["docker run --rm<br/>--network none<br/>-i image"]
418 |     DOCKER --> STDIN["Write JSON payload<br/>to stdin"]
419 |     STDIN --> CONTAINER["Container: run agent,<br/>write output to stdout"]
420 |     CONTAINER --> PARSE["Parse sentinel-<br/>delimited JSON"]
421 |     PARSE --> R["AgentResult"]
422 | ```
423 | 
424 | **ContainerRunner** manages the full container lifecycle:
425 | 
426 | - Validates mount paths against a `MountAllowlist` before container start (raises `ValueError` for blocked or out-of-root paths)
427 | - Constructs `docker run --rm --network none -i <image>` with validated read-only bind mounts
428 | - Sends a JSON payload to container stdin (prompt, agent ID, model, and optional secrets)
429 | - Reads stdout and parses sentinel-delimited JSON output
430 | - On timeout, force-kills the container via `docker rm -f`
431 | - `cleanup_orphans()` removes any stale containers labelled `openjarvis-sandbox=true`
432 | 
433 | **Mount security** (`sandbox/mount_security.py`) enforces two independent checks on every mount path:
434 | 
435 | 1. **Blocked patterns:** Path components are matched against `DEFAULT_BLOCKED_PATTERNS` (`.ssh`, `.env`, `*.pem`, `*.key`, cloud configs, etc.). A match raises `ValueError`.
436 | 2. **Allowed roots:** If `roots` are configured in the allowlist, the resolved path must be under one of them. An empty `roots` list allows any non-blocked path.
437 | 
438 | ```python
439 | from openjarvis.sandbox import ContainerRunner, SandboxedAgent
440 | 
441 | runner = ContainerRunner(
442 |     image="openjarvis-sandbox:latest",
443 |     timeout=60,
444 |     runtime="docker",
445 | )
446 | # Wrap any BaseAgent
447 | inner = SimpleAgent(engine, model="qwen3:8b")
448 | sandboxed = SandboxedAgent(
449 |     agent=inner,
450 |     runner=runner,
451 |     mounts=["/home/user/data"],
452 | )
453 | result = sandboxed.run("Summarize the reports in /home/user/data")
454 | ```
455 | 
456 | !!! warning "accepts_tools = False"
457 |     `SandboxedAgent` does not accept tools via `--tools` or `tools=`. Tool calling within the sandbox is the responsibility of the wrapped inner agent.
458 | 
459 | ---
460 | 
461 | ## Tool System Integration
462 | 
463 | All `ToolUsingAgent` subclasses use the `ToolExecutor` to dispatch tool calls. The tool system is built on the `BaseTool` ABC:
464 | 
465 | ```python
466 | class BaseTool(ABC):
467 |     tool_id: str
468 | 
469 |     @property
470 |     @abstractmethod
471 |     def spec(self) -> ToolSpec:
472 |         """Return the tool specification."""
473 | 
474 |     @abstractmethod
475 |     def execute(self, **params: Any) -> ToolResult:
476 |         """Execute the tool with the given parameters."""
477 | 
478 |     def to_openai_function(self) -> Dict[str, Any]:
479 |         """Convert to OpenAI function-calling format."""
480 | ```
481 | 
482 | ### Built-in Tools
483 | 
484 | | Tool | Registry Key | Description |
485 | |------|-------------|-------------|
486 | | `CalculatorTool` | `calculator` | AST-based safe expression evaluator |
487 | | `ThinkTool` | `think` | Reasoning scratchpad (returns input as-is) |
488 | | `RetrievalTool` | `retrieval` | Memory search via a memory backend |
489 | | `LLMTool` | `llm` | Sub-model calls (query a different model) |
490 | | `FileReadTool` | `file_read` | Safe file reading with path validation |
491 | 
492 | ### ToolExecutor
493 | 
494 | The `ToolExecutor` handles tool dispatch with JSON argument parsing, latency tracking, and event bus integration:
495 | 
496 | ```python
497 | class ToolExecutor:
498 |     def __init__(self, tools: List[BaseTool], bus: Optional[EventBus] = None):
499 |         self._tools = {t.spec.name: t for t in tools}
500 |         self._bus = bus
501 | 
502 |     def execute(self, tool_call: ToolCall) -> ToolResult:
503 |         """Parse arguments, dispatch to tool, measure latency, emit events."""
504 | 
505 |     def get_openai_tools(self) -> List[Dict[str, Any]]:
506 |         """Return tools in OpenAI function-calling format."""
507 | ```
508 | 
509 | For each tool call:
510 | 
511 | 1. Looks up the tool by name
512 | 2. Parses the JSON arguments string
513 | 3. Publishes `TOOL_CALL_START` on the event bus
514 | 4. Executes the tool with timing
515 | 5. Publishes `TOOL_CALL_END` with success status and latency
516 | 6. Returns the `ToolResult`
517 | 
518 | ---
519 | 
520 | ## Event Bus Integration
521 | 
522 | All agents integrate with the `EventBus` for telemetry and trace collection:
523 | 
524 | | Event | Published By | When |
525 | |-------|-------------|------|
526 | | `AGENT_TURN_START` | All agents (via `_emit_turn_start` helper) | Before starting query processing |
527 | | `AGENT_TURN_END` | All agents (via `_emit_turn_end` helper) | After producing a response |
528 | | `TOOL_CALL_START` | ToolExecutor (all `ToolUsingAgent` subclasses) | Before executing a tool |
529 | | `TOOL_CALL_END` | ToolExecutor (all `ToolUsingAgent` subclasses) | After executing a tool |
530 | 
531 | !!! info "Inference events"
532 |     `INFERENCE_START` and `INFERENCE_END` events are published by the `InstrumentedEngine` wrapper (in `telemetry/instrumented_engine.py`), not by agents directly. This keeps telemetry opt-in and transparent to agent code.
533 | 
534 | These events are consumed by the `TelemetryStore` (for metrics) and `TraceCollector` (for interaction traces).
535 | 
536 | ---
537 | 
538 | ## Agent Registration
539 | 
540 | Agents are registered via the `@AgentRegistry.register("name")` decorator:
541 | 
542 | ```python
543 | from openjarvis.core.registry import AgentRegistry
544 | from openjarvis.agents._stubs import BaseAgent
545 | 
546 | @AgentRegistry.register("my-agent")
547 | class MyAgent(BaseAgent):
548 |     agent_id = "my-agent"
549 | 
550 |     def run(self, input, context=None, **kwargs):
551 |         ...
552 | ```
553 | 
554 | To list all registered agents:
555 | 
556 | ```python
557 | from openjarvis.core.registry import AgentRegistry
558 | 
559 | print(AgentRegistry.keys())
560 | # ("simple", "orchestrator", "native_react", "react", "native_openhands", "rlm", "openhands")
561 | ```
562 | 
563 | To instantiate an agent by key:
564 | 
565 | ```python
566 | agent = AgentRegistry.create("orchestrator", engine, model, tools=tools, bus=bus)
567 | ```
```

---

## FILE: `docs/index.md`

- bytes: 8592
- lines: 227
- sha256: `4456D67FB045E729A941C62921C0623FA133D1B4314312C8194A87B65886F019`
- line terminator: LF

Line numbers below are 1-based and authoritative. Cite them.

```markdown
  1 | ---
  2 | title: OpenJarvis
  3 | description: Personal AI, On Personal Devices
  4 | search:
  5 |   boost: 2
  6 | hide:
  7 |   - navigation
  8 | ---
  9 | 
 10 | # Personal AI, On Personal Devices
 11 | 
 12 | <p class="hero-tagline">
 13 | OpenJarvis is a research framework for composable, on-device AI systems.
 14 | Build personal AI that runs on your hardware. Cloud APIs are optional.
 15 | </p>
 16 | 
 17 | ---
 18 | 
 19 | ## Why OpenJarvis?
 20 | 
 21 | Personal AI agents are exploding in popularity, but nearly all of them still route intelligence through cloud APIs. Your "personal" AI continues to depend on someone else's server. At the same time, our [Intelligence Per Watt](https://www.intelligence-per-watt.ai/) research showed that local language models already handle 88.7% of single-turn chat and reasoning queries, with intelligence efficiency improving 5.3× from 2023 to 2025. The models and hardware are increasingly ready. What has been missing is the software stack to make local-first personal AI practical.
 22 | 
 23 | OpenJarvis is that stack. It is an opinionated framework for local-first personal AI, built around three core ideas: shared primitives for building on-device agents; evaluations that treat energy, FLOPs, latency, and dollar cost as first-class constraints alongside accuracy; and a learning loop that improves models using local trace data. The goal is simple: make it possible to build personal AI agents that run locally by default, calling the cloud only when truly necessary. OpenJarvis aims to be both a research platform and a production foundation for local AI, in the spirit of PyTorch.
 24 | 
 25 | ---
 26 | 
 27 | ## Get Started
 28 | 
 29 | === "Browser App"
 30 | 
 31 |     Run the full chat UI locally with one script:
 32 | 
 33 |     ```bash
 34 |     git clone https://github.com/open-jarvis/OpenJarvis.git
 35 |     cd OpenJarvis
 36 |     ./scripts/quickstart.sh
 37 |     ```
 38 | 
 39 |     This installs dependencies, starts Ollama + a local model, launches the backend
 40 |     and frontend, and opens `http://localhost:5173` in your browser.
 41 | 
 42 | === "Desktop App"
 43 | 
 44 |     The desktop app is a native window for the OpenJarvis UI.
 45 |     The backend (Ollama + inference) runs on your machine — start it first, then open the app.
 46 | 
 47 |     **Step 1.** Start the backend:
 48 | 
 49 |     ```bash
 50 |     git clone https://github.com/open-jarvis/OpenJarvis.git
 51 |     cd OpenJarvis
 52 |     ./scripts/quickstart.sh
 53 |     ```
 54 | 
 55 |     **Step 2.** Download and open the desktop app:
 56 | 
 57 |     [Download for macOS](https://github.com/open-jarvis/OpenJarvis/releases/download/desktop-latest/OpenJarvis_0.1.0_universal.dmg){ .md-button .md-button--primary }
 58 | 
 59 |     Also available for [Windows](https://github.com/open-jarvis/OpenJarvis/releases/download/desktop-latest/OpenJarvis_0.1.0_x64-setup.exe), [Linux (DEB)](https://github.com/open-jarvis/OpenJarvis/releases/download/desktop-latest/OpenJarvis_0.1.0_amd64.deb), and [Linux (RPM)](https://github.com/open-jarvis/OpenJarvis/releases/download/desktop-latest/OpenJarvis-0.1.0-1.x86_64.rpm). See the [Downloads](downloads.md) page for details.
 60 | 
 61 |     The app connects to `http://localhost:8000` automatically.
 62 | 
 63 |     !!! warning "macOS: run `xattr -cr /Applications/OpenJarvis.app` if the app shows as \"damaged\"."
 64 | 
 65 | === "Python SDK"
 66 | 
 67 |     ```python
 68 |     from openjarvis import Jarvis
 69 | 
 70 |     j = Jarvis()                              # auto-detect engine
 71 |     response = j.ask("Explain quicksort.")
 72 |     print(response)
 73 |     ```
 74 | 
 75 |     For more control, use `ask_full()` to get usage stats, model info, and tool results:
 76 | 
 77 |     ```python
 78 |     result = j.ask_full(
 79 |         "What is 2 + 2?",
 80 |         agent="orchestrator",
 81 |         tools=["calculator"],
 82 |     )
 83 |     print(result["content"])       # "4"
 84 |     print(result["tool_results"])  # [{tool_name: "calculator", ...}]
 85 |     ```
 86 | 
 87 | === "CLI"
 88 | 
 89 |     ```bash
 90 |     jarvis ask "What is the capital of France?"
 91 | 
 92 |     jarvis ask --agent orchestrator --tools calculator "What is 137 * 42?"
 93 | 
 94 |     jarvis serve --port 8000
 95 | 
 96 |     jarvis memory index ./docs/
 97 |     jarvis memory search "configuration options"
 98 |     ```
 99 | 
100 | ---
101 | 
102 | ## Five Primitives for Personal AI
103 | 
104 | OpenJarvis is built around five composable layers. Each has a clean interface and can be swapped independently.
105 | 
106 | 1. **Intelligence** — Pick a model, or let OpenJarvis pick one for your hardware. Manages the full catalog of local models across providers.
107 | 2. **Agents** — Multi-step reasoning with tool use. Seven built-in agent types from simple chat to orchestrated workflows.
108 | 3. **Tools** — Web search, calculator, file I/O, code interpreter, retrieval, and any external MCP server.
109 | 4. **Engine** — The inference runtime: [Ollama](https://ollama.com), [vLLM](https://github.com/vllm-project/vllm), [SGLang](https://github.com/sgl-project/sglang), [llama.cpp](https://github.com/ggerganov/llama.cpp), cloud APIs, and more. Auto-detects your hardware and recommends the best fit.
110 | 5. **Learning** — Your AI gets better over time. Every interaction generates traces that drive automatic improvements to model weights, prompts, and agent behavior.
111 | 
112 | ---
113 | 
114 | ## Key Features
115 | 
116 | <div class="grid cards" markdown>
117 | 
118 | -   **10+ Engine Backends**
119 | 
120 |     ---
121 | 
122 |     [Ollama](https://ollama.com), [vLLM](https://github.com/vllm-project/vllm), [SGLang](https://github.com/sgl-project/sglang), [llama.cpp](https://github.com/ggerganov/llama.cpp), [MLX](https://github.com/ml-explore/mlx), [Exo](https://github.com/exo-explore/exo), [LiteLLM](https://github.com/BerriAI/litellm), cloud (OpenAI/Anthropic/Google), and more. Same `InferenceEngine` interface, swap freely.
123 | 
124 | -   **Automated Workflows**
125 | 
126 |     ---
127 | 
128 |     Cron-based agents that monitor, summarize, and act. Code review, email triage, research digests — running 24/7 on your hardware.
129 | 
130 | -   **Hardware-Aware**
131 | 
132 |     ---
133 | 
134 |     Auto-detects GPU vendor, model, and VRAM. Recommends the optimal engine for your hardware.
135 | 
136 | -   **Offline-First**
137 | 
138 |     ---
139 | 
140 |     All core functionality works without a network connection. Cloud APIs are optional extras.
141 | 
142 | -   **OpenAI-Compatible API**
143 | 
144 |     ---
145 | 
146 |     `jarvis serve` starts a FastAPI server with SSE streaming. Drop-in replacement for OpenAI clients.
147 | 
148 | -   **Energy & Cost Tracking**
149 | 
150 |     ---
151 | 
152 |     Built-in telemetry for GPU power draw, token costs, and latency. See exactly what each query costs in watts and dollars.
153 | 
154 | </div>
155 | 
156 | ---
157 | 
158 | ## Documentation
159 | 
160 | <div class="grid cards" markdown>
161 | 
162 | -   **[Getting Started](getting-started/installation.md)**
163 | 
164 |     ---
165 | 
166 |     Install OpenJarvis, configure your first engine, and run your first query.
167 | 
168 | -   **[User Guide](user-guide/cli.md)**
169 | 
170 |     ---
171 | 
172 |     CLI, Python SDK, and guides for [Morning Digest](user-guide/morning-digest.md), [Deep Research](user-guide/deep-research.md), [Code Assistant](user-guide/code-assistant.md), [Scheduled Monitor](user-guide/scheduled-monitor.md), [Simple Chat](user-guide/chat-simple.md), agents, memory, tools, and telemetry.
173 | 
174 | -   **[Architecture](architecture/overview.md)**
175 | 
176 |     ---
177 | 
178 |     Five-primitive design, registry pattern, query flow, and cross-cutting learning.
179 | 
180 | -   **[API Reference](api-reference/openjarvis/index.md)**
181 | 
182 |     ---
183 | 
184 |     Auto-generated reference for every module.
185 | 
186 | -   **[Deployment](deployment/docker.md)**
187 | 
188 |     ---
189 | 
190 |     Docker, systemd, launchd. GPU-accelerated container images.
191 | 
192 | -   **[Development](development/contributing.md)**
193 | 
194 |     ---
195 | 
196 |     Contributing guide, extension patterns, roadmap, and changelog.
197 | 
198 | </div>
199 | 
200 | ## Research
201 | 
202 | OpenJarvis is part of [Intelligence Per Watt](https://www.intelligence-per-watt.ai/), a research initiative studying the efficiency of on-device AI systems. Developed at [Hazy Research](https://hazyresearch.stanford.edu/) and the [Scaling Intelligence Lab](https://scalingintelligence.stanford.edu/) at [Stanford SAIL](https://ai.stanford.edu/).
203 | 
204 | Read the [blog post](https://scalingintelligence.stanford.edu/blogs/openjarvis/) for the full research motivation, architecture details, and experimental results.
205 | 
206 | ## Citation
207 | 
208 | ```bibtex
209 | @misc{saadfalcon2026openjarvis,
210 |   title={OpenJarvis: Personal AI, On Personal Devices},
211 |   author={Jon Saad-Falcon and Avanika Narayan and Herumb Shandilya and Hakki Orhun Akengin and Robby Manihani and Gabriel Bo and John Hennessy and Christopher R\'{e} and Azalia Mirhoseini},
212 |   year={2026},
213 |   howpublished={\url{https://scalingintelligence.stanford.edu/blogs/openjarvis/}},
214 | }
215 | ```
216 | 
217 | ## Sponsors
218 | 
219 | <p>
220 |   <a href="https://www.laude.org/">Laude Institute</a> &bull;
221 |   <a href="https://datascience.stanford.edu/marlowe">Stanford Marlowe</a> &bull;
222 |   <a href="https://cloud.google.com/">Google Cloud Platform</a> &bull;
223 |   <a href="https://lambda.ai/">Lambda Labs</a> &bull;
224 |   <a href="https://ollama.com/">Ollama</a> &bull;
225 |   <a href="https://research.ibm.com/">IBM Research</a> &bull;
226 |   <a href="https://hai.stanford.edu/">Stanford HAI</a>
227 | </p>
```

---

## FILE: `README.md`

- bytes: 8822
- lines: 177
- sha256: `D4805CD49629B719B1B8BA5ABD2F618FA42A26810E72503B05E3A1A37E877521`
- line terminator: LF

Line numbers below are 1-based and authoritative. Cite them.

```markdown
  1 | <div align="center">
  2 |   <img alt="OpenJarvis" src="assets/OpenJarvis_Horizontal_Logo.png" width="400">
  3 | 
  4 |   <p><i>Personal AI, On Personal Devices.</i></p>
  5 | 
  6 |   <p>
  7 |     <a href="https://scalingintelligence.stanford.edu/blogs/openjarvis/"><img src="https://img.shields.io/badge/project-OpenJarvis-blue" alt="Project"></a>
  8 |     <a href="https://open-jarvis.github.io/OpenJarvis/"><img src="https://img.shields.io/badge/docs-mkdocs-blue" alt="Docs"></a>
  9 |     <img src="https://img.shields.io/badge/python-%3E%3D3.10-blue" alt="Python">
 10 |     <img src="https://img.shields.io/badge/license-Apache%202.0-green" alt="License">
 11 |     <a href="https://discord.gg/YZZRxCAhmm"><img src="https://img.shields.io/badge/discord-join-7289da?logo=discord&logoColor=white" alt="Discord"></a>
 12 |   </p>
 13 | </div>
 14 | 
 15 | ---
 16 | 
 17 | > **[Documentation](https://open-jarvis.github.io/OpenJarvis/)**
 18 | >
 19 | > **[Project Site](https://scalingintelligence.stanford.edu/blogs/openjarvis/)**
 20 | >
 21 | > **[Leaderboard](https://open-jarvis.github.io/OpenJarvis/leaderboard/)**
 22 | >
 23 | > **[Roadmap](https://open-jarvis.github.io/OpenJarvis/development/roadmap/)**
 24 | 
 25 | ## Why OpenJarvis?
 26 | 
 27 | Personal AI agents are exploding in popularity, but nearly all of them still route intelligence through cloud APIs. Your "personal" AI continues to depend on someone else's server. At the same time, our [Intelligence Per Watt](https://www.intelligence-per-watt.ai/) research showed that local language models already handle 88.7% of single-turn chat and reasoning queries, with intelligence efficiency improving 5.3× from 2023 to 2025. The models and hardware are increasingly ready. What has been missing is the software stack to make local-first personal AI practical.
 28 | 
 29 | OpenJarvis is that stack. It is an opinionated framework for local-first personal AI, built around three core ideas: shared primitives for building on-device agents; evaluations that treat energy, FLOPs, latency, and dollar cost as first-class constraints alongside accuracy; and a learning loop that improves models using local trace data. The goal is simple: make it possible to build personal AI agents that run locally by default, calling the cloud only when truly necessary. OpenJarvis aims to be both a research platform and a production foundation for local AI, in the spirit of PyTorch.
 30 | 
 31 | ## Installation
 32 | 
 33 | ```bash
 34 | curl -fsSL https://openjarvis.ai/install.sh | bash
 35 | ```
 36 | 
 37 | That's it. The installer handles everything: uv, the Python venv, Ollama, and pulling a small starter model. About 3 minutes on a typical broadband connection. Then:
 38 | 
 39 | ```bash
 40 | jarvis
 41 | ```
 42 | 
 43 | The Rust extension and bigger models continue downloading in the background while you chat. Run `jarvis doctor` to see status.
 44 | 
 45 | **Platforms:** macOS (Intel + Apple Silicon), Linux, WSL2 on Windows.
 46 | 
 47 | **Manual install / contributors:** see [docs/getting-started/install.md](docs/getting-started/install.md).
 48 | 
 49 | ## Quick Start
 50 | 
 51 | ```bash
 52 | curl -fsSL https://openjarvis.ai/install.sh | bash
 53 | jarvis
 54 | ```
 55 | 
 56 | `jarvis init --preset <name>` switches to a starter config. Available presets: `morning-digest-mac`, `morning-digest-linux`, `morning-digest-minimal`, `deep-research`, `code-assistant`, `scheduled-monitor`, `chat-simple`.
 57 | 
 58 | ## Starter Configs
 59 | 
 60 | Install any preset with one command:
 61 | 
 62 | ```bash
 63 | uv run jarvis init --preset morning-digest-mac   # or any preset below
 64 | ```
 65 | 
 66 | > Prefix every `jarvis ...` invocation with `uv run`, or activate the venv first (`source .venv/bin/activate`) so plain `jarvis ...` works for the rest of your shell session.
 67 | 
 68 | | Preset | Use Case | What it does |
 69 | |--------|----------|-------------|
 70 | | `morning-digest-mac` | Daily Briefing (Mac) | Spoken briefing from email, calendar, health, news with Jarvis voice |
 71 | | `morning-digest-linux` | Daily Briefing (Linux) | Same, with vLLM support for GPU servers |
 72 | | `morning-digest-minimal` | Daily Briefing (minimal) | Just Gmail + Calendar, runs on any machine |
 73 | | `deep-research` | Research Assistant | Multi-hop research across indexed docs with citations |
 74 | | `code-assistant` | Code Companion | Agent with code execution, file I/O, and shell access |
 75 | | `scheduled-monitor` | Persistent Monitor | Stateful agent that runs on a schedule with memory |
 76 | | `chat-simple` | Simple Chat | Lightweight conversation, no tools needed |
 77 | 
 78 | ```bash
 79 | # Example: Morning Digest on Mac
 80 | uv run jarvis init --preset morning-digest-mac
 81 | uv run jarvis connect gdrive          # one OAuth flow covers Gmail, Calendar, Tasks
 82 | uv run jarvis digest --fresh          # generate and play your first briefing
 83 | 
 84 | # Example: Deep Research
 85 | uv run jarvis init --preset deep-research
 86 | uv run jarvis memory index ./docs/    # requires the Rust extension — see Setup above
 87 | uv run jarvis ask "Summarize all emails about Project X"
 88 | ```
 89 | 
 90 | ### Skills
 91 | 
 92 | Skills teach agents how to better use tools and improve their reasoning. Every skill is a tool — agents discover them from a catalog and invoke them on demand.
 93 | 
 94 | ```bash
 95 | # Install skills from public sources
 96 | jarvis skill install hermes:arxiv
 97 | jarvis skill sync hermes --category research
 98 | 
 99 | # Use skills with any agent
100 | jarvis ask "Use the code-explainer skill to explain this Python code: for i in range(5): print(i*2)"
101 | 
102 | # Optimize skills from your trace history
103 | jarvis optimize skills --policy dspy
104 | 
105 | # Benchmark the impact
106 | jarvis bench skills --max-samples 5 --seeds 42
107 | ```
108 | 
109 | Import from [Hermes Agent](https://github.com/NousResearch/hermes-agent) (~150 skills), [OpenClaw](https://github.com/openclaw/skills) (~13,700 community skills), or any GitHub repo. Skills follow the [agentskills.io](https://agentskills.io/specification) open standard.
110 | 
111 | See the [Skills User Guide](https://open-jarvis.github.io/OpenJarvis/user-guide/skills/) and [Skills Tutorial](https://open-jarvis.github.io/OpenJarvis/tutorials/skills-workflow/) for details.
112 | 
113 | ### Built-in Agents
114 | 
115 | | Agent | Type | What it does |
116 | |-------|------|-------------|
117 | | `morning_digest` | Scheduled | Daily briefing from email, calendar, health, news — with TTS audio |
118 | | `deep_research` | On-demand | Multi-hop research with citations across web and local docs |
119 | | `monitor_operative` | Continuous | Long-horizon monitoring with memory, compression, and retrieval |
120 | | `orchestrator` | On-demand | Multi-turn reasoning with automatic tool selection |
121 | | `native_react` | On-demand | ReAct (Thought-Action-Observation) loop agent |
122 | | `operative` | Continuous | Persistent autonomous agent with state management |
123 | | `native_openhands` | On-demand | CodeAct — generates and executes Python code |
124 | | `simple` | On-demand | Single-turn chat, no tools |
125 | 
126 | See the [User Guide](https://open-jarvis.github.io/OpenJarvis/user-guide/morning-digest/) and [Tutorials](https://open-jarvis.github.io/OpenJarvis/tutorials/) for detailed setup instructions.
127 | 
128 | Full documentation — including Docker deployment, cloud engines, development setup, and tutorials — at **[open-jarvis.github.io/OpenJarvis](https://open-jarvis.github.io/OpenJarvis/)**.
129 | 
130 | ## Contributing
131 | 
132 | We welcome contributions! See the [Contributing Guide](CONTRIBUTING.md) for incentives, contribution types, and the PR process.
133 | 
134 | Quick start for contributors:
135 | 
136 | ```bash
137 | git clone https://github.com/open-jarvis/OpenJarvis.git
138 | cd OpenJarvis
139 | uv sync --extra dev
140 | uv run pre-commit install
141 | uv run pytest tests/ -v
142 | ```
143 | 
144 | Browse the [Roadmap](https://open-jarvis.github.io/OpenJarvis/development/roadmap/) for areas where help is needed. Comment **"take"** on any issue to get auto-assigned.
145 | 
146 | ## About
147 | 
148 | OpenJarvis is part of [Intelligence Per Watt](https://www.intelligence-per-watt.ai/), a research initiative studying the intelligence efficiency of AI systems. The project is developed at [Hazy Research](https://hazyresearch.stanford.edu/) and the [Scaling Intelligence Lab](https://scalingintelligence.stanford.edu/) at [Stanford SAIL](https://ai.stanford.edu/).
149 | 
150 | ## Sponsors
151 | 
152 | <p>
153 |   <a href="https://www.laude.org/">Laude Institute</a> &bull;
154 |   <a href="https://datascience.stanford.edu/marlowe">Stanford Marlowe</a> &bull;
155 |   <a href="https://cloud.google.com/">Google Cloud Platform</a> &bull;
156 |   <a href="https://lambda.ai/">Lambda Labs</a> &bull;
157 |   <a href="https://ollama.com/">Ollama</a> &bull;
158 |   <a href="https://research.ibm.com/">IBM Research</a> &bull;
159 |   <a href="https://hai.stanford.edu/">Stanford HAI</a>
160 | </p>
161 | 
162 | ## Citation
163 | ```bibtex
164 | @misc{saadfalcon2026openjarvispersonalaipersonal,
165 |       title={OpenJarvis: Personal AI, On Personal Devices}, 
166 |       author={Jon Saad-Falcon and Avanika Narayan and Robby Manihani and Tanvir Bhathal and Herumb Shandilya and Hakki Orhun Akengin and Gabriel Bo and Andrew Park and Matthew Hart and Caia Costello and Chuan Li and Christopher Ré and Azalia Mirhoseini},
167 |       year={2026},
168 |       eprint={2605.17172},
169 |       archivePrefix={arXiv},
170 |       primaryClass={cs.LG},
171 |       url={https://arxiv.org/abs/2605.17172}, 
172 | }
173 | ```
174 | 
175 | ## License
176 | 
177 | [Apache 2.0](LICENSE)
```

---

# MANIFEST

| file | found | bytes | lines | sha256 |
|---|---|---|---|---|
| `docs/development/roadmap.md` | yes | 12120 | 141 | `CED58799640D4099...` |
| `docs/architecture/overview.md` | yes | 15462 | 242 | `D71F7625F7F6564B...` |
| `docs/architecture/agents.md` | yes | 22888 | 567 | `032FC4D346D84078...` |
| `docs/index.md` | yes | 8592 | 227 | `4456D67FB045E729...` |
| `README.md` | yes | 8822 | 177 | `D4805CD49629B719...` |

These hashes pin the exact bytes you reviewed. If a later patch is built against different bytes, the mismatch is detectable.

