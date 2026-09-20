# OPENJARVIS CODE REVIEW BUNDLE

- marker: `openjarvis-cloudbundle-v1`
- set: `adhoc` - ad hoc bundle
- generated: 2026-09-06T14:04:58
- repo root: `C:\Users\Admin\OpenJarvis`
- files in bundle: 5

You are reviewing complete source files. Every file is included in full, with authoritative 1-based line numbers in the left gutter. Nothing has been elided.

---

# THE QUESTION

ACTIVATION BASELINE VERSUS A DIVERGED DEPLOYMENT. This is upstream OpenJarvis documentation. The reader cloned the project as operational code and NEVER ran the author's agent-activation steps. He selected the native_openhands agent because his local Qwen 30B handles tools internally, and from that point built every agent behavior himself: custom mailbox tools for reading and trashing email, MCP, memory, debug instrumentation, and a live confirmation gate. His config sets agent.tools explicitly to twelve tools, bypassing the default set. He is now debugging tool-dispatch failures in that self-built path and suspects he may be troubleshooting his own work rather than the author's design. Q1: what EXACTLY does the author's documented installation and activation procedure do, step by step? List every step and what state each one produces on disk or in config. Q2: what does the author say agents require in order to function correctly - configuration keys, registration, tool wiring, prompt files, model requirements? Name every prerequisite and cite the section. Q3: the author's code reads an optional system prompt override and few-shot exemplar file per agent from a directory under the config home. Does the documentation describe these, what they are for, and whether a standard install creates them? Q4: does the documentation describe expected behavior when a model returns no tool call, or any guidance on tool-call parsing, retries, or context budgeting? Q5: based only on these documents, list anything the author already provides that a developer might reasonably have rebuilt from scratch without noticing. Answer each separately and cite file and section. Do not estimate where you can count.

---

# SOURCE

---

## FILE: `docs/getting-started/installation.md`

- bytes: 9918
- lines: 340
- sha256: `13ED46C2FDC05F075E4B7E9ACA67466BA456290229E2E2AAF9BE0D6AEB79A34C`
- line terminator: LF

Line numbers below are 1-based and authoritative. Cite them.

```markdown
  1 | ---
  2 | title: Installation
  3 | description: Get OpenJarvis running — browser app, desktop app, CLI, or Python SDK
  4 | search:
  5 |   boost: 3
  6 | ---
  7 | 
  8 | # Installation
  9 | 
 10 | OpenJarvis runs entirely on your hardware. Choose the interface that fits your workflow.
 11 | 
 12 | ---
 13 | 
 14 | ## Browser App
 15 | 
 16 | Run the full chat UI in your browser. Everything stays local — the backend runs on
 17 | your machine and the frontend connects via `localhost`.
 18 | 
 19 | ### One-command setup
 20 | 
 21 | ```bash
 22 | git clone https://github.com/open-jarvis/OpenJarvis.git
 23 | cd OpenJarvis
 24 | ./scripts/quickstart.sh
 25 | ```
 26 | 
 27 | The script handles everything:
 28 | 
 29 | 1. Checks for Python 3.10+ and Node.js 18+
 30 | 2. Installs Ollama if not present and pulls a starter model
 31 | 3. Installs Python and frontend dependencies
 32 | 4. Starts the backend API server and frontend dev server
 33 | 5. Opens `http://localhost:5173` in your browser
 34 | 
 35 | ### Manual setup
 36 | 
 37 | If you prefer to run each step yourself:
 38 | 
 39 | === "Step 1: Clone and install"
 40 | 
 41 |     ```bash
 42 |     git clone https://github.com/open-jarvis/OpenJarvis.git
 43 |     cd OpenJarvis
 44 |     uv sync --extra server
 45 |     uv run maturin develop -m rust/crates/openjarvis-python/Cargo.toml
 46 |     cd frontend && npm install && cd ..
 47 |     ```
 48 | 
 49 |     !!! note "Prerequisites"
 50 |         Requires [Rust](https://rustup.rs/) (`curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh`).
 51 |         On Python 3.14+, set `PYO3_USE_ABI3_FORWARD_COMPATIBILITY=1` before the `maturin` command.
 52 | 
 53 | === "Step 2: Start Ollama"
 54 | 
 55 |     ```bash
 56 |     # Install from https://ollama.com if not already installed
 57 |     ollama serve &
 58 |     ollama pull qwen3:0.6b
 59 |     ```
 60 | 
 61 | === "Step 3: Start backend"
 62 | 
 63 |     ```bash
 64 |     uv run jarvis serve --port 8000
 65 |     ```
 66 | 
 67 | === "Step 4: Start frontend"
 68 | 
 69 |     ```bash
 70 |     cd frontend
 71 |     npm run dev
 72 |     ```
 73 | 
 74 | Then open [http://localhost:5173](http://localhost:5173).
 75 | 
 76 | ---
 77 | 
 78 | ## Desktop App
 79 | 
 80 | The desktop app is a native window for the OpenJarvis chat UI. All inference and backend
 81 | processing happens on your local machine — the app connects to the backend you start locally.
 82 | 
 83 | ### Setup
 84 | 
 85 | **Step 1.** Start the backend (same as Browser App):
 86 | 
 87 | ```bash
 88 | git clone https://github.com/open-jarvis/OpenJarvis.git
 89 | cd OpenJarvis
 90 | ./scripts/quickstart.sh
 91 | ```
 92 | 
 93 | **Step 2.** Download and open the desktop app:
 94 | 
 95 | | Platform | Download |
 96 | |----------|----------|
 97 | | macOS (Apple Silicon) | [:material-download: **OpenJarvis.dmg**](https://github.com/open-jarvis/OpenJarvis/releases/download/desktop-latest/OpenJarvis_0.1.0_aarch64.dmg) |
 98 | | Windows (64-bit) | [:material-download: **OpenJarvis-setup.exe**](https://github.com/open-jarvis/OpenJarvis/releases/download/desktop-latest/OpenJarvis_0.1.0_x64-setup.exe) |
 99 | | Linux (DEB) | [:material-download: **OpenJarvis.deb**](https://github.com/open-jarvis/OpenJarvis/releases/download/desktop-latest/OpenJarvis_0.1.0_amd64.deb) |
100 | | Linux (RPM) | [:material-download: **OpenJarvis.rpm**](https://github.com/open-jarvis/OpenJarvis/releases/download/desktop-latest/OpenJarvis-0.1.0-1.x86_64.rpm) |
101 | | Linux (AppImage) | [:material-download: **OpenJarvis.AppImage**](https://github.com/open-jarvis/OpenJarvis/releases/download/desktop-latest/OpenJarvis_0.1.0_amd64.AppImage) |
102 | 
103 | The app connects to `http://localhost:8000` automatically.
104 | 
105 | !!! warning "macOS: \"app is damaged\""
106 |     If macOS says the app is damaged, clear the Gatekeeper quarantine flag:
107 |     ```bash
108 |     xattr -cr /Applications/OpenJarvis.app
109 |     ```
110 |     This is normal for open-source apps distributed outside the App Store.
111 | 
112 | !!! tip "All releases"
113 |     Browse all versions on the [GitHub Releases](https://github.com/open-jarvis/OpenJarvis/releases) page.
114 | 
115 | ### Build from source
116 | 
117 | ```bash
118 | git clone https://github.com/open-jarvis/OpenJarvis.git
119 | cd OpenJarvis/desktop
120 | npm install
121 | npm run tauri build
122 | ```
123 | 
124 | The built installer will be in `frontend/src-tauri/target/release/bundle/`.
125 | 
126 | ---
127 | 
128 | ## CLI
129 | 
130 | The command-line interface is the fastest way to interact with OpenJarvis
131 | programmatically. Every feature is accessible from the terminal.
132 | 
133 | ### Install
134 | 
135 | ```bash
136 | git clone https://github.com/open-jarvis/OpenJarvis.git
137 | cd OpenJarvis
138 | uv sync
139 | uv run maturin develop -m rust/crates/openjarvis-python/Cargo.toml
140 | ```
141 | 
142 | Requires [Rust](https://rustup.rs/). On Python 3.14+, set `PYO3_USE_ABI3_FORWARD_COMPATIBILITY=1` before the `maturin` command.
143 | 
144 | ### Verify
145 | 
146 | ```bash
147 | jarvis --version
148 | # jarvis, version 0.1.0
149 | ```
150 | 
151 | ### First commands
152 | 
153 | ```bash
154 | jarvis ask "What is the capital of France?"
155 | 
156 | jarvis ask --agent orchestrator --tools calculator "What is 137 * 42?"
157 | 
158 | jarvis serve --port 8000
159 | 
160 | jarvis doctor
161 | 
162 | jarvis model list
163 | 
164 | jarvis chat
165 | ```
166 | 
167 | !!! info "Inference backend required"
168 |     The CLI requires a running inference backend (e.g., Ollama). See
169 |     [Setting up an inference backend](#setting-up-an-inference-backend) below.
170 | 
171 | ---
172 | 
173 | ## Python SDK
174 | 
175 | For programmatic access, the `Jarvis` class provides a high-level sync API.
176 | 
177 | ### Install
178 | 
179 | ```bash
180 | git clone https://github.com/open-jarvis/OpenJarvis.git
181 | cd OpenJarvis
182 | uv sync
183 | uv run maturin develop -m rust/crates/openjarvis-python/Cargo.toml
184 | ```
185 | 
186 | Requires [Rust](https://rustup.rs/). On Python 3.14+, set `PYO3_USE_ABI3_FORWARD_COMPATIBILITY=1` before the `maturin` command.
187 | 
188 | ### Quick example
189 | 
190 | ```python
191 | from openjarvis import Jarvis
192 | 
193 | j = Jarvis()
194 | print(j.ask("Explain quicksort in two sentences."))
195 | j.close()
196 | ```
197 | 
198 | ### With agents and tools
199 | 
200 | ```python
201 | result = j.ask_full(
202 |     "What is the square root of 144?",
203 |     agent="orchestrator",
204 |     tools=["calculator", "think"],
205 | )
206 | print(result["content"])       # "12"
207 | print(result["tool_results"])  # tool invocations
208 | print(result["turns"])         # number of agent turns
209 | ```
210 | 
211 | ### Composition layer
212 | 
213 | For full control, use the `SystemBuilder`:
214 | 
215 | ```python
216 | from openjarvis import SystemBuilder
217 | 
218 | system = (
219 |     SystemBuilder()
220 |     .engine("ollama")
221 |     .model("qwen3:8b")
222 |     .agent("orchestrator")
223 |     .tools(["calculator", "web_search", "file_read"])
224 |     .enable_telemetry()
225 |     .enable_traces()
226 |     .build()
227 | )
228 | 
229 | result = system.ask("Summarize the latest AI news.")
230 | system.close()
231 | ```
232 | 
233 | See the [Python SDK guide](../user-guide/python-sdk.md) for the full API reference.
234 | 
235 | ---
236 | 
237 | ## Requirements
238 | 
239 | | Requirement | Version | Install | Notes |
240 | |-------------|---------|---------|-------|
241 | | Python | 3.10+ | [python.org](https://www.python.org/downloads/) | Required |
242 | | uv | latest | `curl -LsSf https://astral.sh/uv/install.sh \| sh` or `brew install uv` (macOS) | Python package & project manager |
243 | | Git | any | [git-scm.com](https://git-scm.com/) or `brew install git` (macOS) | Required |
244 | | Rust | stable | `curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs \| sh` | Required for the Rust extension |
245 | | Inference backend | any | See [below](#setting-up-an-inference-backend) | At least one of Ollama, vLLM, llama.cpp, SGLang, or a cloud API |
246 | | Node.js | 18+ | [nodejs.org](https://nodejs.org/) or `brew install node` (macOS) | Required for the browser UI; 22+ for the WhatsApp Baileys channel bridge |
247 | 
248 | !!! tip "macOS users"
249 |     See the [macOS Installation Guide](macos.md) for a complete step-by-step walkthrough
250 |     covering Homebrew, uv, Rust, llama.cpp, and common pitfalls.
251 | 
252 | ## Optional Extras
253 | 
254 | OpenJarvis uses optional extras to keep the base installation lightweight.
255 | 
256 | ### Inference Backends
257 | 
258 | | Extra | Install Command | Description |
259 | |-------|----------------|-------------|
260 | | `inference-cloud` | `uv sync --extra inference-cloud` | OpenAI and Anthropic APIs |
261 | | `inference-google` | `uv sync --extra inference-google` | Google Gemini API |
262 | 
263 | !!! note "Ollama, vLLM, and llama.cpp are HTTP-based"
264 |     These engines have no additional Python dependencies — OpenJarvis communicates over HTTP. You still need the engine software running on your machine.
265 | 
266 | ### Memory Backends
267 | 
268 | | Extra | Install Command | Description |
269 | |-------|----------------|-------------|
270 | | `memory-faiss` | `uv sync --extra memory-faiss` | FAISS vector store |
271 | | `memory-colbert` | `uv sync --extra memory-colbert` | ColBERTv2 late-interaction retrieval |
272 | | `memory-bm25` | `uv sync --extra memory-bm25` | BM25 sparse retrieval |
273 | 
274 | !!! tip "SQLite memory is always available"
275 |     The default SQLite/FTS5 memory backend requires no additional dependencies.
276 | 
277 | ### Server & Other
278 | 
279 | | Extra | Install Command | Description |
280 | |-------|----------------|-------------|
281 | | `server` | `uv sync --extra server` | OpenAI-compatible API server (`jarvis serve`) |
282 | | `dev` | `uv sync --extra dev` | Development and testing tools |
283 | | `docs` | `uv sync --extra docs` | Documentation build tools |
284 | 
285 | Combine extras:
286 | 
287 | ```bash
288 | uv sync --extra server --extra memory-faiss --extra inference-cloud
289 | ```
290 | 
291 | ## Setting Up an Inference Backend
292 | 
293 | OpenJarvis requires at least one inference backend. Choose the one that matches your hardware.
294 | 
295 | ### Ollama (Recommended)
296 | 
297 | The easiest way to get started. Handles model downloading and serving automatically.
298 | 
299 | 1. Install from [ollama.com](https://ollama.com)
300 | 2. Start the server and pull a model:
301 | 
302 |     ```bash
303 |     ollama serve
304 |     ollama pull qwen3:0.6b
305 |     ```
306 | 
307 | 3. Verify: `jarvis model list`
308 | 
309 | !!! tip "Best for: Apple Silicon Macs, consumer NVIDIA GPUs, CPU-only systems"
310 | 
311 | ### vLLM
312 | 
313 | High-throughput serving optimized for datacenter GPUs.
314 | 
315 | 1. Install following the [official guide](https://docs.vllm.ai)
316 | 2. Start: `vllm serve Qwen/Qwen2.5-7B-Instruct`
317 | 3. Auto-detected at `http://localhost:8000`
318 | 
319 | !!! tip "Best for: NVIDIA datacenter GPUs (A100, H100), AMD GPUs"
320 | 
321 | ### llama.cpp
322 | 
323 | Efficient CPU and GPU inference with GGUF quantized models.
324 | 
325 | 1. Build from [github.com/ggerganov/llama.cpp](https://github.com/ggerganov/llama.cpp)
326 | 2. Start: `llama-server -m /path/to/model.gguf --port 8080`
327 | 3. Auto-detected at `http://localhost:8080`
328 | 
329 | ### Cloud APIs
330 | 
331 | ```bash
332 | uv sync --extra inference-cloud --extra inference-google
333 | export OPENAI_API_KEY="sk-..."
334 | export ANTHROPIC_API_KEY="sk-ant-..."
335 | ```
336 | 
337 | ## Next Steps
338 | 
339 | - [Quick Start](quickstart.md) — Run your first query
340 | - [Configuration](configuration.md) — Customize engine hosts, model routing, memory, and more
```

---

## FILE: `docs/getting-started/configuration.md`

- bytes: 35541
- lines: 1115
- sha256: `FAA23D2DF03E1706844150EDAE194F8C817FE8459571B7D508C7F04664186437`
- line terminator: LF

Line numbers below are 1-based and authoritative. Cite them.

```markdown
   1 | ---
   2 | title: Configuration
   3 | description: Complete reference for OpenJarvis configuration
   4 | ---
   5 | 
   6 | # Configuration
   7 | 
   8 | OpenJarvis uses a TOML configuration file to control engine selection, model identity, memory backends, agent behavior, and more. This page is the complete reference for every configuration option, organized by primitive.
   9 | 
  10 | ## Config File Location
  11 | 
  12 | The configuration file lives at:
  13 | 
  14 | ```
  15 | ~/.openjarvis/config.toml
  16 | ```
  17 | 
  18 | OpenJarvis creates the `~/.openjarvis/` directory and populates it with a default config when you run `jarvis init`.
  19 | 
  20 | ## Generating Configuration
  21 | 
  22 | ### First-Time Setup
  23 | 
  24 | ```bash
  25 | jarvis init
  26 | ```
  27 | 
  28 | This command:
  29 | 
  30 | 1. Runs hardware auto-detection (GPU vendor/model/VRAM, CPU brand/cores, RAM)
  31 | 2. Selects the recommended engine based on your hardware
  32 | 3. Writes `~/.openjarvis/config.toml` with sensible defaults
  33 | 
  34 | ### Regenerating Configuration
  35 | 
  36 | To overwrite an existing config:
  37 | 
  38 | ```bash
  39 | jarvis init --force
  40 | ```
  41 | 
  42 | !!! warning
  43 |     `--force` overwrites your existing config file. Back up your config first if you have custom settings.
  44 | 
  45 | ## Configuration Sections
  46 | 
  47 | The config file is organized into TOML sections corresponding to the five primitives. Every field has a default value, so you only need to specify values you want to change.
  48 | 
  49 | ---
  50 | 
  51 | ### `[engine]` — Inference Engine
  52 | 
  53 | Controls which inference engine is used and how each engine is reached. Engine settings are now **nested** under per-engine sub-sections instead of flat fields.
  54 | 
  55 | ```toml
  56 | [engine]
  57 | default = "ollama"
  58 | 
  59 | [engine.ollama]
  60 | host = "http://localhost:11434"
  61 | 
  62 | [engine.vllm]
  63 | host = "http://localhost:8000"
  64 | 
  65 | [engine.sglang]
  66 | host = "http://localhost:30000"
  67 | 
  68 | # [engine.llamacpp]
  69 | # host = "http://localhost:8080"
  70 | # binary_path = ""
  71 | ```
  72 | 
  73 | **`[engine]` top-level:**
  74 | 
  75 | | Field | Type | Default | Description |
  76 | |-------|------|---------|-------------|
  77 | | `default` | string | Auto-detected | Default engine backend. One of: `ollama`, `vllm`, `llamacpp`, `sglang`, `cloud`. Set automatically by `jarvis init` based on hardware detection. |
  78 | 
  79 | **`[engine.ollama]`:**
  80 | 
  81 | | Field | Type | Default | Description |
  82 | |-------|------|---------|-------------|
  83 | | `host` | string | `http://localhost:11434` | Base URL for the Ollama API server. |
  84 | 
  85 | **`[engine.vllm]`:**
  86 | 
  87 | | Field | Type | Default | Description |
  88 | |-------|------|---------|-------------|
  89 | | `host` | string | `http://localhost:8000` | Base URL for the vLLM OpenAI-compatible server. |
  90 | 
  91 | **`[engine.sglang]`:**
  92 | 
  93 | | Field | Type | Default | Description |
  94 | |-------|------|---------|-------------|
  95 | | `host` | string | `http://localhost:30000` | Base URL for the SGLang server. |
  96 | 
  97 | **`[engine.llamacpp]`:**
  98 | 
  99 | | Field | Type | Default | Description |
 100 | |-------|------|---------|-------------|
 101 | | `host` | string | `http://localhost:8080` | Base URL for the llama.cpp HTTP server (`llama-server`). |
 102 | | `binary_path` | string | `""` | Path to the llama.cpp binary, if not on `$PATH`. |
 103 | 
 104 | !!! tip "Engine fallback"
 105 |     If the configured default engine is unreachable, OpenJarvis automatically probes all registered engines and falls back to any healthy one.
 106 | 
 107 | !!! note "Backward compatibility"
 108 |     The old flat field names (`ollama_host`, `vllm_host`, `llamacpp_host`, `llamacpp_path`, `sglang_host`) are still accepted as backward-compatible properties. New configurations should use the nested sub-section format.
 109 | 
 110 | ---
 111 | 
 112 | ### `[intelligence]` — Model Identity and Generation Defaults
 113 | 
 114 | Controls which model is used, its weight paths, quantization, and the default sampling parameters for generation. Generation parameters such as `temperature` and `max_tokens` now live here rather than under `[agent]`.
 115 | 
 116 | ```toml
 117 | [intelligence]
 118 | default_model = ""
 119 | fallback_model = ""
 120 | # model_path = ""
 121 | # checkpoint_path = ""
 122 | # quantization = "none"
 123 | # preferred_engine = ""
 124 | # provider = ""
 125 | temperature = 0.7
 126 | max_tokens = 1024
 127 | # top_p = 0.9
 128 | # top_k = 40
 129 | # repetition_penalty = 1.0
 130 | # stop_sequences = ""
 131 | ```
 132 | 
 133 | **Model identity fields:**
 134 | 
 135 | | Field | Type | Default | Description |
 136 | |-------|------|---------|-------------|
 137 | | `default_model` | string | `""` | Preferred model identifier (e.g., `qwen3:8b`). When empty, the router policy selects the model dynamically. |
 138 | | `fallback_model` | string | `""` | Model to use if the default is unavailable. |
 139 | | `model_path` | string | `""` | Path or HuggingFace repo ID for local weights (e.g., `"./models/qwen3-8b.gguf"` or `"Qwen/Qwen3-8B"`). |
 140 | | `checkpoint_path` | string | `""` | Path to a fine-tuned checkpoint or LoRA adapter directory. |
 141 | | `quantization` | string | `"none"` | Quantization format. Accepted values: `none`, `fp8`, `int8`, `int4`, `gguf_q4`, `gguf_q8`. |
 142 | | `preferred_engine` | string | `""` | Override engine for this model (e.g., `"vllm"`). Takes priority over `engine.default`. |
 143 | | `provider` | string | `""` | Model provider hint: `local`, `openai`, `anthropic`, `google`, `minimax`. Used by the Cloud engine to route API calls. |
 144 | 
 145 | **Generation default fields** (overridable per-call):
 146 | 
 147 | | Field | Type | Default | Description |
 148 | |-------|------|---------|-------------|
 149 | | `temperature` | float | `0.7` | Sampling temperature. Lower values produce more deterministic output. |
 150 | | `max_tokens` | int | `1024` | Maximum number of tokens to generate per call. |
 151 | | `top_p` | float | `0.9` | Nucleus sampling probability mass. |
 152 | | `top_k` | int | `40` | Top-k sampling: only consider the top-k tokens at each step. |
 153 | | `repetition_penalty` | float | `1.0` | Penalize repeated tokens. Values > 1 reduce repetition. |
 154 | | `stop_sequences` | string | `""` | Comma-separated stop strings. Generation halts when any stop string is produced. |
 155 | 
 156 | When both `default_model` and `fallback_model` are empty, OpenJarvis uses the configured router policy (see `[learning]`) to select a model from those available on the active engine.
 157 | 
 158 | ### Engine Selection Priority
 159 | 
 160 | When resolving which engine to use for a model, `SystemBuilder`, `sdk.py`, and `cli/ask.py` check fields in this order:
 161 | 
 162 | ```
 163 | 1. Explicit --engine CLI flag or engine_key= SDK parameter
 164 | 2. config.intelligence.preferred_engine
 165 | 3. config.engine.default
 166 | 4. First healthy engine discovered at runtime
 167 | ```
 168 | 
 169 | This lets you pin a specific model to a specific engine without changing the global engine default:
 170 | 
 171 | ```toml
 172 | [engine]
 173 | default = "ollama"
 174 | 
 175 | [intelligence]
 176 | default_model = "llama3.2:3b"
 177 | model_path = "./models/llama-3.2-3b.Q4_K_M.gguf"
 178 | quantization = "gguf_q4"
 179 | preferred_engine = "llamacpp"
 180 | ```
 181 | 
 182 | ---
 183 | 
 184 | ### `[agent]` — Agent Behavior
 185 | 
 186 | Controls the default agent, turn limits, tool selection, system prompt, and memory context injection.
 187 | 
 188 | ```toml
 189 | [agent]
 190 | default_agent = "simple"
 191 | max_turns = 10
 192 | # tools = ""
 193 | # objective = ""
 194 | # system_prompt = ""
 195 | # system_prompt_path = ""
 196 | context_from_memory = true
 197 | ```
 198 | 
 199 | | Field | Type | Default | Description |
 200 | |-------|------|---------|-------------|
 201 | | `default_agent` | string | `"simple"` | Default agent to use. Available: `simple`, `orchestrator`, `react`, `operative`, `monitor_operative`. |
 202 | | `max_turns` | int | `10` | Maximum number of tool-calling turns for the orchestrator agent before it must produce a final answer. |
 203 | | `tools` | string | `""` | Comma-separated list of tools to enable by default (e.g., `"calculator,think"`). |
 204 | | `objective` | string | `""` | Concise purpose string for routing, learning, and documentation. |
 205 | | `system_prompt` | string | `""` | Inline system prompt. Takes precedence over `system_prompt_path` when set. |
 206 | | `system_prompt_path` | string | `""` | Path to a system prompt file (`.txt` or `.md`). |
 207 | | `context_from_memory` | bool | `true` | Whether to automatically inject relevant memory context into queries. |
 208 | 
 209 | !!! note "Generation parameters moved"
 210 |     `temperature` and `max_tokens` have moved from `[agent]` to `[intelligence]`. Old configs with these fields under `[agent]` are automatically migrated to `[intelligence]` at load time.
 211 | 
 212 | !!! note "Backward compatibility"
 213 |     The old field name `default_tools` is still accepted as a backward-compatible property for `tools`. New configurations should use `tools`.
 214 | 
 215 | !!! info "Context injection"
 216 |     When `context_from_memory = true` and documents have been indexed, every query automatically searches memory for relevant chunks and prepends them as system context. This gives the model access to your indexed knowledge base without any extra steps. Disable with `--no-context` on the CLI or `context=False` in the SDK.
 217 | 
 218 | ---
 219 | 
 220 | ### `[learning]` — Learning Policies
 221 | 
 222 | Controls whether the learning system is enabled and configures per-primitive policies through nested sub-sections.
 223 | 
 224 | ```toml
 225 | [learning]
 226 | enabled = false
 227 | update_interval = 100
 228 | # auto_update = false
 229 | 
 230 | [learning.routing]
 231 | policy = "heuristic"
 232 | # min_samples = 5
 233 | 
 234 | # [learning.intelligence]
 235 | # policy = "none"
 236 | 
 237 | # [learning.agent]
 238 | # policy = "none"
 239 | 
 240 | # [learning.metrics]
 241 | # accuracy_weight = 0.6
 242 | # latency_weight = 0.2
 243 | # cost_weight = 0.1
 244 | # efficiency_weight = 0.1
 245 | ```
 246 | 
 247 | **`[learning]` top-level:**
 248 | 
 249 | | Field | Type | Default | Description |
 250 | |-------|------|---------|-------------|
 251 | | `enabled` | bool | `false` | Whether the learning system is active. |
 252 | | `update_interval` | int | `100` | Number of traces between automatic policy updates. |
 253 | | `auto_update` | bool | `false` | Whether to trigger policy updates automatically when the interval is reached. |
 254 | 
 255 | **`[learning.routing]` — Router policy:**
 256 | 
 257 | | Field | Type | Default | Description |
 258 | |-------|------|---------|-------------|
 259 | | `policy` | string | `"heuristic"` | Router policy for model selection. Available: `heuristic`, `learned` (trace-driven), `sft` (supervised fine-tuning), `grpo` (RL stub). |
 260 | | `min_samples` | int | `5` | Minimum number of traces required before trusting a learned routing decision. |
 261 | 
 262 | **`[learning.intelligence]` — Intelligence learning policy:**
 263 | 
 264 | | Field | Type | Default | Description |
 265 | |-------|------|---------|-------------|
 266 | | `policy` | string | `"none"` | Intelligence learning policy. Available: `none`, `sft`. Use `sft` to learn model routing from accumulated traces. |
 267 | 
 268 | **`[learning.agent]` — Agent learning policy:**
 269 | 
 270 | | Field | Type | Default | Description |
 271 | |-------|------|---------|-------------|
 272 | | `policy` | string | `"none"` | Agent learning policy. Available: `none`, `agent_advisor`, `icl_updater`. |
 273 | | `max_icl_examples` | int | `20` | Maximum number of in-context examples to maintain in the ICL example library. |
 274 | | `advisor_confidence_threshold` | float | `0.7` | Minimum confidence score for the advisor to recommend a strategy change. |
 275 | 
 276 | **`[learning.metrics]` — Reward / optimization metric weights:**
 277 | 
 278 | | Field | Type | Default | Description |
 279 | |-------|------|---------|-------------|
 280 | | `accuracy_weight` | float | `0.6` | Weight for outcome accuracy in the composite reward score. |
 281 | | `latency_weight` | float | `0.2` | Weight for inference latency in the composite reward score. |
 282 | | `cost_weight` | float | `0.1` | Weight for per-call cost in the composite reward score. |
 283 | | `efficiency_weight` | float | `0.1` | Weight for token efficiency in the composite reward score. |
 284 | 
 285 | **Router policies:**
 286 | 
 287 | | Policy | Description |
 288 | |--------|-------------|
 289 | | `heuristic` | Rule-based selection using 6 priority rules. Considers model availability, parameter count, context length, and query characteristics. Default. |
 290 | | `learned` | Trace-driven policy that learns from past interaction outcomes stored in the trace system. |
 291 | | `sft` | Supervised fine-tuning policy that learns routing from labeled trace data. |
 292 | | `grpo` | Group Relative Policy Optimization stub for future RL-based routing. |
 293 | 
 294 | **Agent policies:**
 295 | 
 296 | | Policy | Description |
 297 | |--------|-------------|
 298 | | `agent_advisor` | Advises on agent strategy (tool sets, turn limits) based on trace patterns. |
 299 | | `icl_updater` | In-context learning updater — discovers reusable ICL examples and multi-tool skill sequences from traces. |
 300 | 
 301 | You can also override the router policy per-query via the CLI:
 302 | 
 303 | ```bash
 304 | jarvis ask --router heuristic "Hello"
 305 | ```
 306 | 
 307 | !!! note "Backward compatibility"
 308 |     The old flat field names `default_policy`, `intelligence_policy`, `agent_policy`, and the comma-separated `reward_weights` string are still accepted as backward-compatible properties. New configurations should use the nested sub-section format. The `tools_policy` field has been removed; use `learning.agent.policy = "icl_updater"` instead.
 309 | 
 310 | ---
 311 | 
 312 | ### `[tools.storage]` — Storage Backend
 313 | 
 314 | Controls the storage backend used for document memory and context injection. The `context_injection` field has moved to `agent.context_from_memory`.
 315 | 
 316 | ```toml
 317 | [tools.storage]
 318 | default_backend = "sqlite"
 319 | db_path = "~/.openjarvis/memory.db"
 320 | context_top_k = 5
 321 | context_min_score = 0.1
 322 | context_max_tokens = 2048
 323 | chunk_size = 512
 324 | chunk_overlap = 64
 325 | ```
 326 | 
 327 | | Field | Type | Default | Description |
 328 | |-------|------|---------|-------------|
 329 | | `default_backend` | string | `"sqlite"` | Storage backend. Available: `sqlite` (FTS5), `faiss`, `colbert`, `bm25`, `hybrid`. |
 330 | | `db_path` | string | `~/.openjarvis/memory.db` | Path to the SQLite memory database. Used by the `sqlite` backend. |
 331 | | `context_top_k` | int | `5` | Number of top memory results to inject as context. |
 332 | | `context_min_score` | float | `0.1` | Minimum relevance score for a memory result to be included in context. |
 333 | | `context_max_tokens` | int | `2048` | Maximum number of tokens to use for injected context. |
 334 | | `chunk_size` | int | `512` | Size of document chunks (in tokens) when indexing documents. |
 335 | | `chunk_overlap` | int | `64` | Overlap between adjacent chunks (in tokens) when indexing. |
 336 | 
 337 | **Memory backends:**
 338 | 
 339 | | Backend | Extra Required | Description |
 340 | |---------|---------------|-------------|
 341 | | `sqlite` | None | SQLite with FTS5 full-text search. Zero dependencies. Default. |
 342 | | `faiss` | `memory-faiss` | Facebook AI Similarity Search with sentence-transformer embeddings. |
 343 | | `colbert` | `memory-colbert` | ColBERTv2 late-interaction retrieval. Requires PyTorch. |
 344 | | `bm25` | `memory-bm25` | BM25 sparse retrieval via `rank-bm25`. |
 345 | | `hybrid` | Depends on sub-backends | Reciprocal Rank Fusion combining multiple backends. |
 346 | 
 347 | !!! note "Backward compatibility"
 348 |     The `[memory]` TOML section is still supported and maps to `[tools.storage]`. New configurations should use `[tools.storage]`. The `context_injection` field under `[memory]` or `[tools.storage]` is automatically migrated to `agent.context_from_memory` at load time.
 349 | 
 350 | ---
 351 | 
 352 | ### `[tools.mcp]` — MCP (Model Context Protocol)
 353 | 
 354 | Controls the MCP server and external MCP tool provider integration. The MCP adapter supports protocol version 2025-11-25.
 355 | 
 356 | ```toml
 357 | [tools.mcp]
 358 | enabled = true
 359 | # servers = ""  # JSON list of external MCP server configs
 360 | ```
 361 | 
 362 | | Field | Type | Default | Description |
 363 | |-------|------|---------|-------------|
 364 | | `enabled` | bool | `true` | Whether to enable the MCP adapter for exposing and consuming tools via MCP. |
 365 | | `servers` | string | `""` | JSON-encoded list of external MCP server configuration objects. |
 366 | 
 367 | ---
 368 | 
 369 | ### `[server]` — API Server
 370 | 
 371 | Controls the OpenAI-compatible API server started by `jarvis serve`.
 372 | 
 373 | ```toml
 374 | [server]
 375 | host = "0.0.0.0"
 376 | port = 8000
 377 | agent = "orchestrator"
 378 | model = ""
 379 | workers = 1
 380 | ```
 381 | 
 382 | | Field | Type | Default | Description |
 383 | |-------|------|---------|-------------|
 384 | | `host` | string | `"0.0.0.0"` | Bind address for the server. Use `"127.0.0.1"` to restrict to localhost. |
 385 | | `port` | int | `8000` | Port number for the server. |
 386 | | `agent` | string | `"orchestrator"` | Agent to use for chat completion requests. |
 387 | | `model` | string | `""` | Default model for the server. When empty, uses `intelligence.default_model` or the first available model. |
 388 | | `workers` | int | `1` | Number of uvicorn worker processes. |
 389 | 
 390 | CLI options override config values:
 391 | 
 392 | ```bash
 393 | jarvis serve --host 127.0.0.1 --port 9000 --model qwen3:8b --agent simple
 394 | ```
 395 | 
 396 | ---
 397 | 
 398 | ### `[telemetry]` — Telemetry Persistence
 399 | 
 400 | Controls whether inference telemetry is recorded and where it is stored.
 401 | 
 402 | ```toml
 403 | [telemetry]
 404 | enabled = true
 405 | db_path = "~/.openjarvis/telemetry.db"
 406 | ```
 407 | 
 408 | | Field | Type | Default | Description |
 409 | |-------|------|---------|-------------|
 410 | | `enabled` | bool | `true` | Whether to record telemetry for each inference call. Records timing, token counts, model, engine, and cost. |
 411 | | `db_path` | string | `~/.openjarvis/telemetry.db` | Path to the SQLite telemetry database. |
 412 | 
 413 | !!! info "Telemetry is local-only"
 414 |     All telemetry data is stored locally in a SQLite database. No data is ever sent to external services.
 415 | 
 416 | ---
 417 | 
 418 | ### `[traces]` — Trace Recording
 419 | 
 420 | Controls the trace system that records full interaction sequences for the learning system.
 421 | 
 422 | ```toml
 423 | [traces]
 424 | enabled = false
 425 | db_path = "~/.openjarvis/traces.db"
 426 | ```
 427 | 
 428 | | Field | Type | Default | Description |
 429 | |-------|------|---------|-------------|
 430 | | `enabled` | bool | `false` | Whether to record traces for each agent interaction. |
 431 | | `db_path` | string | `~/.openjarvis/traces.db` | Path to the SQLite trace database. |
 432 | 
 433 | ---
 434 | 
 435 | ### `[skills]` — Skills System
 436 | 
 437 | Controls the skills system — reusable compositions of tools and agent instructions. Skills teach agents how to better use tools and improve their reasoning. See the [Skills User Guide](../user-guide/skills.md) for full documentation.
 438 | 
 439 | ```toml
 440 | [skills]
 441 | enabled = true
 442 | skills_dir = "~/.openjarvis/skills/"
 443 | active = "*"
 444 | auto_discover = true
 445 | auto_sync = false
 446 | max_depth = 5
 447 | sandbox_dangerous = true
 448 | ```
 449 | 
 450 | | Field | Type | Default | Description |
 451 | |-------|------|---------|-------------|
 452 | | `enabled` | bool | `true` | Whether to enable the skills system. When disabled, no skills are loaded or exposed to agents. |
 453 | | `skills_dir` | string | `~/.openjarvis/skills/` | Directory where skills are installed. |
 454 | | `active` | string | `"*"` | Comma-separated list of skill names to activate, or `"*"` for all discovered skills. |
 455 | | `auto_discover` | bool | `true` | Whether to scan `skills_dir` for skills on startup. |
 456 | | `auto_sync` | bool | `false` | Whether to pull from configured sources on session start (checks freshness every 24h). |
 457 | | `max_depth` | int | `5` | Maximum sub-skill nesting depth for composed skills. |
 458 | | `sandbox_dangerous` | bool | `true` | Whether to warn about skills with dangerous capabilities (`shell:execute`, `network:listen`, `filesystem:write`). |
 459 | 
 460 | #### `[[skills.sources]]` — Skill Import Sources
 461 | 
 462 | Configure one or more skill sources for automatic import. Each `[[skills.sources]]` entry defines a source to pull from.
 463 | 
 464 | ```toml
 465 | [[skills.sources]]
 466 | source = "hermes"
 467 | filter = { category = ["research", "coding", "productivity"] }
 468 | auto_update = true
 469 | 
 470 | [[skills.sources]]
 471 | source = "openclaw"
 472 | filter = { search = "web3|crypto" }
 473 | 
 474 | [[skills.sources]]
 475 | source = "github"
 476 | url = "https://github.com/myorg/internal-skills"
 477 | auto_update = true
 478 | ```
 479 | 
 480 | | Field | Type | Default | Description |
 481 | |-------|------|---------|-------------|
 482 | | `source` | string | `""` | Source type: `"hermes"`, `"openclaw"`, or `"github"`. |
 483 | | `url` | string | `""` | Repository URL. Required when `source = "github"`. |
 484 | | `filter` | table | `{}` | Filter criteria. Supported keys: `category` (list of strings), `search` (regex string). |
 485 | | `auto_update` | bool | `false` | Whether to pull latest commits when syncing this source. |
 486 | 
 487 | #### `[learning.skills]` — Skills Learning Loop
 488 | 
 489 | Controls the automatic optimization of skill descriptions and few-shot examples from trace data. Requires `[traces] enabled = true` to collect the traces that the optimizer analyzes.
 490 | 
 491 | ```toml
 492 | [learning.skills]
 493 | auto_optimize = false
 494 | optimizer = "dspy"
 495 | min_traces_per_skill = 20
 496 | optimization_interval_seconds = 86400
 497 | overlay_dir = "~/.openjarvis/learning/skills/"
 498 | ```
 499 | 
 500 | | Field | Type | Default | Description |
 501 | |-------|------|---------|-------------|
 502 | | `auto_optimize` | bool | `false` | Whether to run skill optimization automatically after each learning cycle. |
 503 | | `optimizer` | string | `"dspy"` | Optimization policy: `"dspy"` (bootstrap few-shot) or `"gepa"` (evolutionary). |
 504 | | `min_traces_per_skill` | int | `20` | Minimum trace count for a skill to be eligible for optimization. |
 505 | | `optimization_interval_seconds` | int | `86400` | Run optimization at most once per this interval (default: once per day). |
 506 | | `overlay_dir` | string | `~/.openjarvis/learning/skills/` | Where optimized skill overlays are stored. |
 507 | 
 508 | ---
 509 | 
 510 | ### `[channel]` — Channel Messaging
 511 | 
 512 | Controls the channel messaging bridge for multi-platform communication. Each supported platform has its own nested sub-section.
 513 | 
 514 | ```toml
 515 | [channel]
 516 | enabled = false
 517 | default_channel = ""
 518 | default_agent = "simple"
 519 | 
 520 | # [channel.telegram]
 521 | # bot_token = ""
 522 | 
 523 | # [channel.discord]
 524 | # bot_token = ""
 525 | 
 526 | # [channel.slack]
 527 | # bot_token = ""
 528 | # app_token = ""
 529 | 
 530 | # [channel.webhook]
 531 | # url = ""
 532 | # secret = ""
 533 | # method = "POST"
 534 | ```
 535 | 
 536 | | Field | Type | Default | Description |
 537 | |-------|------|---------|-------------|
 538 | | `enabled` | bool | `false` | Whether to enable channel messaging support. |
 539 | | `default_channel` | string | `""` | Default channel to use when not specified. |
 540 | | `default_agent` | string | `"simple"` | Default agent for handling channel messages. |
 541 | 
 542 | ---
 543 | 
 544 | ### `[security]` — Security Guardrails
 545 | 
 546 | Controls the security scanning pipeline for input/output content.
 547 | 
 548 | ```toml
 549 | [security]
 550 | enabled = true
 551 | mode = "warn"
 552 | scan_input = true
 553 | scan_output = true
 554 | secret_scanner = true
 555 | pii_scanner = true
 556 | enforce_tool_confirmation = true
 557 | ```
 558 | 
 559 | | Field | Type | Default | Description |
 560 | |-------|------|---------|-------------|
 561 | | `enabled` | bool | `true` | Whether to enable security guardrails. |
 562 | | `mode` | string | `"warn"` | Action on findings: `"warn"` (log only), `"redact"` (replace sensitive content), or `"block"` (raise error). |
 563 | | `scan_input` | bool | `true` | Whether to scan user input messages. |
 564 | | `scan_output` | bool | `true` | Whether to scan model output. |
 565 | | `secret_scanner` | bool | `true` | Enable secret detection (API keys, tokens, passwords). |
 566 | | `pii_scanner` | bool | `true` | Enable PII detection (emails, SSNs, credit cards). |
 567 | | `enforce_tool_confirmation` | bool | `true` | Require confirmation before executing tools. |
 568 | 
 569 | !!! tip "Choosing a security mode"
 570 |     Use `"warn"` during development to see what would be flagged without disrupting output.
 571 |     Use `"redact"` in production to automatically sanitize sensitive content.
 572 |     Use `"block"` for strict environments where any sensitive data should halt generation.
 573 | 
 574 | ---
 575 | 
 576 | ## Hardware Auto-Detection
 577 | 
 578 | When you run `jarvis init`, OpenJarvis probes your system to detect available hardware. The detection runs in this order:
 579 | 
 580 | ### GPU Detection
 581 | 
 582 | 1. **NVIDIA GPU** — Checks for `nvidia-smi` on `$PATH`. If found, queries GPU name, VRAM (in MB), and GPU count via:
 583 | 
 584 |     ```
 585 |     nvidia-smi --query-gpu=name,memory.total,count --format=csv,noheader,nounits
 586 |     ```
 587 | 
 588 | 2. **AMD GPU** — Checks for `rocm-smi` on `$PATH`. If found, queries the product name via:
 589 | 
 590 |     ```
 591 |     rocm-smi --showproductname
 592 |     ```
 593 | 
 594 | 3. **Apple Silicon** — On macOS only. Runs `system_profiler SPDisplaysDataType` and looks for "Apple" in the chipset model line.
 595 | 
 596 | If none of these detect a GPU, the system is treated as CPU-only.
 597 | 
 598 | ### CPU and RAM Detection
 599 | 
 600 | - **CPU brand**: Reads from `sysctl -n machdep.cpu.brand_string` on macOS, or parses `model name` from `/proc/cpuinfo` on Linux.
 601 | - **CPU count**: Uses Python's `os.cpu_count()`.
 602 | - **RAM**: Reads from `sysctl -n hw.memsize` on macOS, or parses `MemTotal` from `/proc/meminfo` on Linux.
 603 | 
 604 | ### Detected Hardware Dataclass
 605 | 
 606 | The detection result is stored as a `HardwareInfo` dataclass:
 607 | 
 608 | ```python
 609 | @dataclass
 610 | class HardwareInfo:
 611 |     platform: str      # "linux", "darwin", "windows"
 612 |     cpu_brand: str     # e.g., "AMD EPYC 7763"
 613 |     cpu_count: int     # e.g., 128
 614 |     ram_gb: float      # e.g., 512.0
 615 |     gpu: GpuInfo | None
 616 | 
 617 | @dataclass
 618 | class GpuInfo:
 619 |     vendor: str             # "nvidia", "amd", "apple"
 620 |     name: str               # e.g., "NVIDIA A100-SXM4-80GB"
 621 |     vram_gb: float          # e.g., 80.0
 622 |     compute_capability: str # (NVIDIA only)
 623 |     count: int              # e.g., 8
 624 | ```
 625 | 
 626 | ---
 627 | 
 628 | ## Engine Recommendation Logic
 629 | 
 630 | Based on the detected hardware, `recommend_engine()` selects the optimal default engine:
 631 | 
 632 | ```mermaid
 633 | graph TD
 634 |     A[detect_hardware] --> B{GPU detected?}
 635 |     B -->|No| C[llamacpp]
 636 |     B -->|Yes| D{GPU vendor?}
 637 |     D -->|Apple| E[ollama]
 638 |     D -->|NVIDIA| F{Datacenter GPU?}
 639 |     D -->|AMD| G[vllm]
 640 |     F -->|Yes: A100, H100, H200, L40, A10, A30| H[vllm]
 641 |     F -->|No: consumer GPU| I[ollama]
 642 | ```
 643 | 
 644 | | Hardware | Recommended Engine | Reason |
 645 | |----------|--------------------|--------|
 646 | | No GPU | `llamacpp` | Efficient CPU inference with GGUF quantized models |
 647 | | Apple Silicon | `ollama` | Native Metal acceleration, easy model management |
 648 | | NVIDIA consumer GPU (RTX 3090, 4090, etc.) | `ollama` | Simple setup, good performance for single-user |
 649 | | NVIDIA datacenter GPU (A100, H100, H200, L40, A10, A30) | `vllm` | High-throughput batched serving, continuous batching |
 650 | | AMD GPU | `vllm` | ROCm support via vLLM |
 651 | 
 652 | ---
 653 | 
 654 | ## Example Configurations
 655 | 
 656 | ### Apple Silicon Mac
 657 | 
 658 | ```toml
 659 | # ~/.openjarvis/config.toml
 660 | # Apple Silicon MacBook Pro (M3 Max, 128 GB unified memory)
 661 | 
 662 | [engine]
 663 | default = "ollama"
 664 | 
 665 | [engine.ollama]
 666 | host = "http://localhost:11434"
 667 | 
 668 | [intelligence]
 669 | default_model = "qwen3:8b"
 670 | fallback_model = "llama3.2:3b"
 671 | temperature = 0.7
 672 | max_tokens = 1024
 673 | 
 674 | [agent]
 675 | default_agent = "simple"
 676 | max_turns = 10
 677 | context_from_memory = true
 678 | 
 679 | [tools.storage]
 680 | default_backend = "sqlite"
 681 | 
 682 | [server]
 683 | host = "127.0.0.1"
 684 | port = 8000
 685 | agent = "orchestrator"
 686 | 
 687 | [learning]
 688 | enabled = false
 689 | 
 690 | [learning.routing]
 691 | policy = "heuristic"
 692 | 
 693 | [telemetry]
 694 | enabled = true
 695 | ```
 696 | 
 697 | ### NVIDIA Datacenter (Multi-GPU)
 698 | 
 699 | ```toml
 700 | # ~/.openjarvis/config.toml
 701 | # 8x NVIDIA A100 80GB server
 702 | 
 703 | [engine]
 704 | default = "vllm"
 705 | 
 706 | [engine.vllm]
 707 | host = "http://localhost:8000"
 708 | 
 709 | [engine.ollama]
 710 | host = "http://localhost:11434"
 711 | 
 712 | [intelligence]
 713 | default_model = "Qwen/Qwen2.5-72B-Instruct"
 714 | fallback_model = "Qwen/Qwen2.5-7B-Instruct"
 715 | temperature = 0.5
 716 | max_tokens = 4096
 717 | 
 718 | [agent]
 719 | default_agent = "orchestrator"
 720 | max_turns = 15
 721 | tools = "calculator,think,retrieval"
 722 | context_from_memory = true
 723 | 
 724 | [tools.storage]
 725 | default_backend = "faiss"
 726 | context_top_k = 10
 727 | context_min_score = 0.05
 728 | context_max_tokens = 4096
 729 | chunk_size = 1024
 730 | chunk_overlap = 128
 731 | 
 732 | [server]
 733 | host = "0.0.0.0"
 734 | port = 8000
 735 | agent = "orchestrator"
 736 | model = "Qwen/Qwen2.5-72B-Instruct"
 737 | workers = 1
 738 | 
 739 | [learning]
 740 | enabled = false
 741 | 
 742 | [learning.routing]
 743 | policy = "heuristic"
 744 | 
 745 | [telemetry]
 746 | enabled = true
 747 | ```
 748 | 
 749 | ### CPU-Only (No GPU)
 750 | 
 751 | ```toml
 752 | # ~/.openjarvis/config.toml
 753 | # CPU-only machine
 754 | 
 755 | [engine]
 756 | default = "llamacpp"
 757 | 
 758 | [engine.llamacpp]
 759 | host = "http://localhost:8080"
 760 | 
 761 | [intelligence]
 762 | default_model = ""
 763 | fallback_model = ""
 764 | temperature = 0.7
 765 | max_tokens = 512
 766 | 
 767 | [agent]
 768 | default_agent = "simple"
 769 | max_turns = 5
 770 | context_from_memory = true
 771 | 
 772 | [tools.storage]
 773 | default_backend = "sqlite"
 774 | context_top_k = 3
 775 | context_max_tokens = 1024
 776 | chunk_size = 256
 777 | chunk_overlap = 32
 778 | 
 779 | [server]
 780 | host = "127.0.0.1"
 781 | port = 8000
 782 | 
 783 | [learning]
 784 | enabled = false
 785 | 
 786 | [learning.routing]
 787 | policy = "heuristic"
 788 | 
 789 | [telemetry]
 790 | enabled = true
 791 | ```
 792 | 
 793 | ### Trace-Driven Learning Enabled
 794 | 
 795 | ```toml
 796 | # ~/.openjarvis/config.toml
 797 | # Research setup with trace-driven learning active
 798 | 
 799 | [engine]
 800 | default = "ollama"
 801 | 
 802 | [engine.ollama]
 803 | host = "http://localhost:11434"
 804 | 
 805 | [intelligence]
 806 | default_model = "qwen3:8b"
 807 | temperature = 0.7
 808 | max_tokens = 1024
 809 | 
 810 | [agent]
 811 | default_agent = "orchestrator"
 812 | max_turns = 10
 813 | context_from_memory = true
 814 | 
 815 | [tools.storage]
 816 | default_backend = "sqlite"
 817 | 
 818 | [learning]
 819 | enabled = true
 820 | update_interval = 50
 821 | auto_update = true
 822 | 
 823 | [learning.routing]
 824 | policy = "learned"
 825 | min_samples = 10
 826 | 
 827 | [learning.intelligence]
 828 | policy = "sft"
 829 | 
 830 | [learning.agent]
 831 | policy = "agent_advisor"
 832 | advisor_confidence_threshold = 0.8
 833 | 
 834 | [learning.metrics]
 835 | accuracy_weight = 0.6
 836 | latency_weight = 0.2
 837 | cost_weight = 0.1
 838 | efficiency_weight = 0.1
 839 | 
 840 | [traces]
 841 | enabled = true
 842 | 
 843 | [telemetry]
 844 | enabled = true
 845 | ```
 846 | 
 847 | ---
 848 | 
 849 | ## Migration Guide
 850 | 
 851 | If you have an existing `~/.openjarvis/config.toml` from a previous version, here is what changed and how to update it.
 852 | 
 853 | ### Engine: Nested Sub-Sections
 854 | 
 855 | === "Old Format"
 856 | 
 857 |     ```toml
 858 |     [engine]
 859 |     default = "ollama"
 860 |     ollama_host = "http://localhost:11434"
 861 |     vllm_host = "http://localhost:8000"
 862 |     llamacpp_path = "/usr/local/bin/llama-server"
 863 |     ```
 864 | 
 865 | === "New Format"
 866 | 
 867 |     ```toml
 868 |     [engine]
 869 |     default = "ollama"
 870 | 
 871 |     [engine.ollama]
 872 |     host = "http://localhost:11434"
 873 | 
 874 |     [engine.vllm]
 875 |     host = "http://localhost:8000"
 876 | 
 877 |     [engine.llamacpp]
 878 |     binary_path = "/usr/local/bin/llama-server"
 879 |     ```
 880 | 
 881 | !!! note
 882 |     The old flat names still work as backward-compatible properties. You only need to update your config if you want to use the new fields (e.g., `binary_path`).
 883 | 
 884 | ### Intelligence: Generation Parameters
 885 | 
 886 | === "Old Format"
 887 | 
 888 |     ```toml
 889 |     [agent]
 890 |     temperature = 0.7
 891 |     max_tokens = 1024
 892 |     ```
 893 | 
 894 | === "New Format"
 895 | 
 896 |     ```toml
 897 |     [intelligence]
 898 |     temperature = 0.7
 899 |     max_tokens = 1024
 900 |     ```
 901 | 
 902 | !!! note
 903 |     Old configs with `temperature` or `max_tokens` under `[agent]` are automatically migrated to `[intelligence]` at load time. No manual update is required, but updating is recommended for clarity.
 904 | 
 905 | ### Agent: Renamed and Added Fields
 906 | 
 907 | === "Old Format"
 908 | 
 909 |     ```toml
 910 |     [agent]
 911 |     default_tools = "calculator,think"
 912 |     ```
 913 | 
 914 | === "New Format"
 915 | 
 916 |     ```toml
 917 |     [agent]
 918 |     tools = "calculator,think"
 919 |     ```
 920 | 
 921 | The `default_tools` name still works via a backward-compatible property.
 922 | 
 923 | ### Memory: Context Injection Moved
 924 | 
 925 | === "Old Format"
 926 | 
 927 |     ```toml
 928 |     [memory]
 929 |     context_injection = true
 930 |     default_backend = "sqlite"
 931 |     ```
 932 | 
 933 | === "New Format"
 934 | 
 935 |     ```toml
 936 |     [agent]
 937 |     context_from_memory = true
 938 | 
 939 |     [tools.storage]
 940 |     default_backend = "sqlite"
 941 |     ```
 942 | 
 943 | !!! note
 944 |     `context_injection` under `[memory]` or `[tools.storage]` is automatically migrated to `agent.context_from_memory` at load time.
 945 | 
 946 | ### Learning: Nested Sub-Sections
 947 | 
 948 | === "Old Format"
 949 | 
 950 |     ```toml
 951 |     [learning]
 952 |     default_policy = "heuristic"
 953 |     intelligence_policy = "sft"
 954 |     agent_policy = "agent_advisor"
 955 |     tools_policy = "icl_updater"
 956 |     reward_weights = "accuracy=0.6,latency=0.2,cost=0.1,efficiency=0.1"
 957 |     update_interval = 100
 958 |     ```
 959 | 
 960 | === "New Format"
 961 | 
 962 |     ```toml
 963 |     [learning]
 964 |     enabled = true
 965 |     update_interval = 100
 966 | 
 967 |     [learning.routing]
 968 |     policy = "heuristic"
 969 | 
 970 |     [learning.intelligence]
 971 |     policy = "sft"
 972 | 
 973 |     [learning.agent]
 974 |     policy = "agent_advisor"
 975 | 
 976 |     [learning.metrics]
 977 |     accuracy_weight = 0.6
 978 |     latency_weight = 0.2
 979 |     cost_weight = 0.1
 980 |     efficiency_weight = 0.1
 981 |     ```
 982 | 
 983 | !!! note
 984 |     The flat field names `default_policy`, `intelligence_policy`, `agent_policy`, and `reward_weights` are still accepted as backward-compatible properties. The `tools_policy` field has been removed; use `learning.agent.policy = "icl_updater"` instead.
 985 | 
 986 | ---
 987 | 
 988 | ## Programmatic Configuration
 989 | 
 990 | You can configure OpenJarvis entirely from Python without a TOML file:
 991 | 
 992 | ```python
 993 | from openjarvis import Jarvis
 994 | from openjarvis.core.config import (
 995 |     AgentConfig,
 996 |     EngineConfig,
 997 |     IntelligenceConfig,
 998 |     JarvisConfig,
 999 |     LearningConfig,
1000 |     OllamaEngineConfig,
1001 |     StorageConfig,
1002 |     ToolsConfig,
1003 | )
1004 | 
1005 | config = JarvisConfig(
1006 |     engine=EngineConfig(
1007 |         default="ollama",
1008 |         ollama=OllamaEngineConfig(host="http://my-server:11434"),
1009 |     ),
1010 |     intelligence=IntelligenceConfig(
1011 |         default_model="qwen3:8b",
1012 |         temperature=0.7,
1013 |         max_tokens=2048,
1014 |     ),
1015 |     agent=AgentConfig(
1016 |         default_agent="orchestrator",
1017 |         max_turns=15,
1018 |         context_from_memory=True,
1019 |     ),
1020 |     tools=ToolsConfig(
1021 |         storage=StorageConfig(
1022 |             default_backend="sqlite",
1023 |             context_top_k=10,
1024 |         ),
1025 |     ),
1026 | )
1027 | 
1028 | j = Jarvis(config=config)
1029 | response = j.ask("Hello")
1030 | j.close()
1031 | ```
1032 | 
1033 | Or load from a custom path:
1034 | 
1035 | ```python
1036 | j = Jarvis(config_path="/path/to/my-config.toml")
1037 | ```
1038 | 
1039 | ---
1040 | 
1041 | ## Environment Variables
1042 | 
1043 | OpenJarvis respects the following environment variables:
1044 | 
1045 | | Variable | Description |
1046 | |----------|-------------|
1047 | | `OPENAI_API_KEY` | API key for OpenAI cloud inference. Required for the `cloud` engine with OpenAI models. |
1048 | | `ANTHROPIC_API_KEY` | API key for Anthropic cloud inference. Required for the `cloud` engine with Claude models. |
1049 | | `GOOGLE_API_KEY` | API key for Google Gemini inference. Required for the `google` engine. |
1050 | | `MINIMAX_API_KEY` | API key for MiniMax cloud inference. Required for the `cloud` engine with MiniMax models (MiniMax-M2.7, MiniMax-M2.7-highspeed, MiniMax-M2.5, MiniMax-M2.5-highspeed). |
1051 | | `TAVILY_API_KEY` | API key for the Tavily web search tool. Required for the `web_search` tool. |
1052 | 
1053 | ## Next Steps
1054 | 
1055 | - [Quick Start](quickstart.md) — Run your first query
1056 | - [CLI Reference](../user-guide/cli.md) — Full reference for all CLI commands
1057 | - [Architecture Overview](../architecture/overview.md) — Understand how the pieces fit together
1058 | - [Intelligence Primitive](../architecture/intelligence.md) — Model identity and generation defaults
1059 | - [Learning & Traces](../architecture/learning.md) — Router policies and the trace-driven feedback loop
1060 | 
1061 | ---
1062 | 
1063 | ## Learning & spec search
1064 | 
1065 | LLM-guided spec search uses a frontier model to automatically improve your local agent configuration. See the [user guide](../user-guide/llm-guided-spec-search.md) for a full walkthrough.
1066 | 
1067 | ### `[learning.spec_search]`
1068 | 
1069 | | Key | Type | Default | Description |
1070 | |-----|------|---------|-------------|
1071 | | `enabled` | bool | `true` | Gate the entire spec-search subsystem |
1072 | | `autonomy_mode` | string | `"tiered"` | `auto`, `tiered`, or `manual` |
1073 | | `teacher_model` | string | `"claude-opus-4-6"` | Frontier model for diagnosis and planning |
1074 | | `max_cost_per_session_usd` | float | `5.0` | Per-session teacher API budget |
1075 | | `max_tool_calls_per_diagnosis` | int | `30` | Max teacher tool calls in diagnosis phase |
1076 | 
1077 | ### `[learning.spec_search.triggers]`
1078 | 
1079 | | Key | Type | Default | Description |
1080 | |-----|------|---------|-------------|
1081 | | `scheduled_enabled` | bool | `true` | Enable daily scheduled sessions |
1082 | | `scheduled_cron` | string | `"0 3 * * *"` | Cron expression for scheduled trigger |
1083 | | `scheduled_min_new_traces` | int | `20` | Minimum new traces to trigger |
1084 | | `cluster_enabled` | bool | `true` | Enable failure cluster trigger |
1085 | | `cluster_check_interval_minutes` | int | `60` | How often to check for clusters |
1086 | | `cluster_min_size` | int | `5` | Minimum traces in a cluster |
1087 | | `cluster_failure_threshold` | float | `0.3` | Feedback <= this counts as failure |
1088 | 
1089 | ### `[learning.spec_search.gate]`
1090 | 
1091 | | Key | Type | Default | Description |
1092 | |-----|------|---------|-------------|
1093 | | `min_improvement` | float | `0.0` | Minimum overall score improvement to accept |
1094 | | `max_regression` | float | `0.05` | Maximum per-cluster score drop before rejecting |
1095 | | `benchmark_subsample_size` | int | `50` | Tasks per gate run |
1096 | | `full_benchmark` | bool | `false` | Disable subsampling (slower, more accurate) |
1097 | 
1098 | ### `[learning.spec_search.benchmark]`
1099 | 
1100 | | Key | Type | Default | Description |
1101 | |-----|------|---------|-------------|
1102 | | `synthesis_feedback_threshold` | float | `0.7` | Min feedback for benchmark traces |
1103 | | `max_benchmark_size` | int | `200` | Max tasks in the benchmark |
1104 | | `auto_refresh` | bool | `true` | Auto-mine new high-feedback traces |
1105 | | `max_synthesis_cost_usd_per_refresh` | float | `2.0` | Cost cap per benchmark refresh |
1106 | 
1107 | ### `[learning.spec_search.tier_overrides]`
1108 | 
1109 | Override the default risk tier for any operation. Keys are operation names, values are tier strings (`auto`, `review`, `manual`).
1110 | 
1111 | ```toml
1112 | [learning.spec_search.tier_overrides]
1113 | # patch_system_prompt = "auto"     # promote to auto after trust
1114 | # replace_system_prompt = "auto"
1115 | ```
```

---

## FILE: `docs/getting-started/install.md`

- bytes: 3767
- lines: 113
- sha256: `1F878AB0D08F78BB5DEDDFE147C3850106DD0DEFB45A9D0ECFAAFA38DFE52751`
- line terminator: LF

Line numbers below are 1-based and authoritative. Cite them.

```markdown
  1 | # Installation
  2 | 
  3 | OpenJarvis ships a one-line installer for macOS, Linux, and WSL2.
  4 | 
  5 | ```bash
  6 | curl -fsSL https://openjarvis.ai/install.sh | bash
  7 | ```
  8 | 
  9 | About 3 minutes on a typical broadband connection. Type `jarvis` to start chatting.
 10 | 
 11 | ## What the installer does
 12 | 
 13 | | Phase | Step | Where |
 14 | |---|---|---|
 15 | | Foreground | Install `uv` (Python package manager) | `~/.cargo/bin/` or `~/.local/bin/` |
 16 | | Foreground | Clone OpenJarvis repo | `~/.openjarvis/src/` |
 17 | | Foreground | Create Python 3.11 venv | `~/.openjarvis/.venv/` |
 18 | | Foreground | `uv pip install -e .` (editable install) | venv |
 19 | | Foreground | Install Ollama | system default |
 20 | | Foreground | Start `ollama serve` | systemd-user / launchd / nohup |
 21 | | Foreground | Pull `qwen3.5:2b` (~1.5 GB) | Ollama's model store |
 22 | | Foreground | Write `config.toml` (auto-detected hardware + engine + model) | `~/.openjarvis/config.toml` |
 23 | | Foreground | Symlink `jarvis` and `jarvis-uninstall` | `~/.local/bin/` |
 24 | | Foreground | Add `~/.local/bin` to PATH if missing (with on-screen notice) | `~/.bashrc` or `~/.zshrc` |
 25 | | Background | Install Rust toolchain via rustup | `~/.cargo/` |
 26 | | Background | Build the maturin extension (memory + security features) | venv |
 27 | | Background | Pull hardware-tier and tier+1 models | Ollama's model store |
 28 | 
 29 | ## What the installer does NOT touch
 30 | 
 31 | - Your existing Python installations
 32 | - Your `~/.bashrc` / `~/.zshrc` other than appending one PATH line (with on-screen notice)
 33 | - Your existing Ollama models
 34 | - Any other tool or dotfile
 35 | 
 36 | ## Idempotent re-runs
 37 | 
 38 | Re-running the curl line is safe. The installer reads `~/.openjarvis/.state/install-state.json` and skips completed steps. If your venv got nuked, re-running heals it.
 39 | 
 40 | ## Cloud quick-path
 41 | 
 42 | If any of these env vars are set when you install or run `jarvis init`, the installer/init proposes cloud as the default and writes the matching provider into `config.toml`:
 43 | 
 44 | - `OPENROUTER_API_KEY`
 45 | - `ANTHROPIC_API_KEY`
 46 | - `OPENAI_API_KEY`
 47 | - `GOOGLE_API_KEY` (or `GEMINI_API_KEY`)
 48 | 
 49 | Local-first remains the default when no key is in env. Precedence is OpenRouter > Anthropic > OpenAI > Google.
 50 | 
 51 | ## Flags
 52 | 
 53 | | Flag | Effect |
 54 | |---|---|
 55 | | `--minimal` | Skip the foreground model pull. First chat will need to wait for the bg pull to finish. |
 56 | | `--no-bg-orchestrator` | Don't detach the background work pipeline. (Mostly for testing.) |
 57 | | `--force` | Re-run all steps even if `install-state.json` says they're done. |
 58 | 
 59 | ## Environment overrides
 60 | 
 61 | | Variable | Default | Purpose |
 62 | |---|---|---|
 63 | | `OPENJARVIS_HOME` | `$HOME/.openjarvis` | Install location. |
 64 | | `OPENJARVIS_REPO_URL` | `https://github.com/open-jarvis/OpenJarvis.git` | Source repo for the clone step. |
 65 | 
 66 | ## Uninstall
 67 | 
 68 | ```bash
 69 | jarvis-uninstall
 70 | ```
 71 | 
 72 | Removes `~/.openjarvis/`, `~/.local/bin/jarvis`, and `~/.local/bin/jarvis-uninstall`. Leaves Ollama, uv, and the Rust toolchain in place (they may be used by other tools); the script prints removal hints.
 73 | 
 74 | ## Updating
 75 | 
 76 | ```bash
 77 | jarvis update
 78 | ```
 79 | 
 80 | Pulls the latest source, refreshes the editable install, and rebuilds the Rust extension in the background. Models are not touched.
 81 | 
 82 | ## Troubleshooting
 83 | 
 84 | ### "command not found: jarvis"
 85 | 
 86 | `~/.local/bin` isn't on your PATH. Run `source ~/.bashrc` (or `~/.zshrc`) or open a new terminal.
 87 | 
 88 | ### "memory features unavailable"
 89 | 
 90 | Rust extension hasn't finished building yet (or failed). Check status:
 91 | 
 92 | ```bash
 93 | jarvis doctor
 94 | ```
 95 | 
 96 | Manually retry:
 97 | 
 98 | ```bash
 99 | ~/.openjarvis/.scripts/install-rust.sh && ~/.openjarvis/.scripts/build-extension.sh
100 | ```
101 | 
102 | ### A bigger model failed to download
103 | 
104 | Check status and retry:
105 | 
106 | ```bash
107 | jarvis doctor
108 | ~/.openjarvis/.scripts/pull-model.sh qwen3.5:9b
109 | ```
110 | 
111 | ### Behind a corporate proxy
112 | 
113 | Set `HTTPS_PROXY` and `CURL_CA_BUNDLE` in your environment before running the installer.
```

---

## FILE: `docs/architecture/design-principles.md`

- bytes: 10353
- lines: 299
- sha256: `4F9ED52CAE44D7603DC2730A66DDE9B63A87468230DE6BFA236DEB7BB7B4C151`
- line terminator: LF

Line numbers below are 1-based and authoritative. Cite them.

```markdown
  1 | # Design Principles
  2 | 
  3 | OpenJarvis follows a set of design principles that guide every architectural decision. These principles ensure the framework remains extensible, portable, and easy to work with.
  4 | 
  5 | ---
  6 | 
  7 | ## 1. Pluggable Everything
  8 | 
  9 | Every major component in OpenJarvis is defined as an **abstract base class** (ABC) with concrete implementations registered at runtime. This means you can swap, extend, or replace any part of the system without modifying existing code.
 10 | 
 11 | ```mermaid
 12 | graph LR
 13 |     subgraph "ABC Interface"
 14 |         ABC["InferenceEngine ABC<br/><code>generate(), stream(),<br/>list_models(), health()</code>"]
 15 |     end
 16 | 
 17 |     subgraph "Implementations"
 18 |         A["OllamaEngine"]
 19 |         B["VLLMEngine"]
 20 |         C["SGLangEngine"]
 21 |         D["LlamaCppEngine"]
 22 |         E["CloudEngine"]
 23 |         F["YourCustomEngine"]
 24 |     end
 25 | 
 26 |     ABC --> A
 27 |     ABC --> B
 28 |     ABC --> C
 29 |     ABC --> D
 30 |     ABC --> E
 31 |     ABC -.->|"extend"| F
 32 | ```
 33 | 
 34 | This pattern applies across all five primitives:
 35 | 
 36 | | Primitive | ABC | Implementations |
 37 | |--------|-----|----------------|
 38 | | Engine | `InferenceEngine` | Ollama, vLLM, SGLang, llama.cpp, Cloud |
 39 | | Memory | `MemoryBackend` | SQLite, FAISS, ColBERT, BM25, Hybrid |
 40 | | Agents | `BaseAgent` | Simple, Orchestrator, NativeReAct, NativeOpenHands, RLM, OpenHands, ClaudeCode, Operative, MonitorOperative |
 41 | | Learning | `RouterPolicy` | Heuristic, TraceDriven, GRPO |
 42 | | Tools | `BaseTool` | Calculator, Think, Retrieval, LLM, FileRead |
 43 | 
 44 | Adding a new implementation requires two things: implement the ABC and register it. The rest of the system discovers and uses it automatically.
 45 | 
 46 | ---
 47 | 
 48 | ## 2. Registry-Driven
 49 | 
 50 | All extensible components use the **`@XRegistry.register("name")` decorator** pattern. Registration happens at import time, and no factory function or configuration file needs modification.
 51 | 
 52 | ```python
 53 | from openjarvis.core.registry import EngineRegistry
 54 | from openjarvis.engine._stubs import InferenceEngine
 55 | 
 56 | @EngineRegistry.register("my-engine")
 57 | class MyEngine(InferenceEngine):
 58 |     engine_id = "my-engine"
 59 | 
 60 |     def generate(self, messages, *, model, **kwargs):
 61 |         ...
 62 |     def stream(self, messages, *, model, **kwargs):
 63 |         ...
 64 |     def list_models(self):
 65 |         ...
 66 |     def health(self):
 67 |         ...
 68 | ```
 69 | 
 70 | The `RegistryBase[T]` generic base class provides:
 71 | 
 72 | - **Class-specific isolation** -- Each typed subclass (`EngineRegistry`, `MemoryRegistry`, etc.) has its own entry storage, so registrations never leak between registries
 73 | - **Duplicate detection** -- Registering the same key twice raises `ValueError`
 74 | - **Runtime instantiation** -- `Registry.create(key, *args)` looks up and instantiates in one step
 75 | - **Introspection** -- `keys()`, `items()`, `contains()` for discovering available components
 76 | 
 77 | !!! info "Why decorators instead of configuration files?"
 78 |     The decorator pattern means that adding a new component is a single-file change.
 79 |     There is no central registry file to edit, no YAML to update, and no factory to modify.
 80 |     The component self-registers simply by being imported.
 81 | 
 82 | ---
 83 | 
 84 | ## 3. Offline-First
 85 | 
 86 | OpenJarvis is designed to work **entirely without network access**. All core functionality -- inference, memory, agents, tools, telemetry -- operates locally. Cloud APIs are optional extensions, never requirements.
 87 | 
 88 | | Feature | Offline Behavior |
 89 | |---------|-----------------|
 90 | | Inference | Ollama, vLLM, SGLang, llama.cpp all run locally |
 91 | | Memory | SQLite/FTS5 uses built-in Python `sqlite3` module |
 92 | | Embeddings | `sentence-transformers` models run locally |
 93 | | Telemetry | SQLite-based, fully local |
 94 | | Traces | SQLite-based, fully local |
 95 | | Tools | Calculator, Think, FileRead all local |
 96 | | Configuration | TOML file on disk |
 97 | 
 98 | Cloud engines (OpenAI, Anthropic, Google) are available through the optional `cloud` backend, but they are:
 99 | 
100 | - Only registered if the corresponding SDK packages are installed
101 | - Only activated if API keys are set as environment variables
102 | - Never required for any core functionality
103 | 
104 | ```python
105 | # This works without any network connection
106 | from openjarvis import Jarvis
107 | 
108 | j = Jarvis(engine_key="ollama")  # Local Ollama server
109 | response = j.ask("Hello")
110 | ```
111 | 
112 | ---
113 | 
114 | ## 4. Hardware-Aware
115 | 
116 | OpenJarvis **auto-detects system hardware** at startup and recommends the optimal inference engine. The `detect_hardware()` function probes:
117 | 
118 | | Hardware | Detection Method |
119 | |----------|-----------------|
120 | | NVIDIA GPUs | `nvidia-smi` (name, VRAM, count) |
121 | | AMD GPUs | `rocm-smi` (product name) |
122 | | Apple Silicon | `system_profiler SPDisplaysDataType` |
123 | | CPU | `/proc/cpuinfo` or `sysctl` (brand string) |
124 | | RAM | `/proc/meminfo` or `sysctl hw.memsize` |
125 | 
126 | The `recommend_engine()` function maps hardware to engines:
127 | 
128 | | Hardware | Recommended Engine |
129 | |----------|-------------------|
130 | | No GPU | `llamacpp` (CPU-optimized) |
131 | | Apple Silicon | `ollama` (Metal acceleration) |
132 | | NVIDIA datacenter (A100, H100, etc.) | `vllm` (high throughput) |
133 | | NVIDIA consumer | `ollama` (easy setup) |
134 | | AMD GPU | `vllm` (ROCm support) |
135 | 
136 | This recommendation is written to `config.toml` during `jarvis init` and used as the default engine:
137 | 
138 | ```bash
139 | jarvis init --force
140 | # Detects hardware, writes ~/.openjarvis/config.toml with:
141 | # [engine]
142 | # default = "vllm"  # (for A100)
143 | ```
144 | 
145 | ---
146 | 
147 | ## 5. Telemetry-Native
148 | 
149 | Every inference call automatically records timing, token counts, energy usage, and cost to a local SQLite database. Telemetry is a **first-class concern**, not an afterthought.
150 | 
151 | ```python
152 | @dataclass(slots=True)
153 | class TelemetryRecord:
154 |     timestamp: float
155 |     model_id: str
156 |     prompt_tokens: int
157 |     completion_tokens: int
158 |     total_tokens: int
159 |     latency_seconds: float
160 |     ttft: float              # Time to first token
161 |     cost_usd: float
162 |     energy_joules: float
163 |     power_watts: float
164 |     engine: str
165 |     agent: str
166 | ```
167 | 
168 | The `instrumented_generate()` wrapper handles all telemetry transparently:
169 | 
170 | 1. Records start time
171 | 2. Calls the engine's `generate()` method
172 | 3. Records end time and extracts token counts
173 | 4. Publishes a `TELEMETRY_RECORD` event on the EventBus
174 | 5. The `TelemetryStore` (subscribed to the bus) persists the record
175 | 
176 | The `TelemetryAggregator` provides read-only queries over stored records:
177 | 
178 | ```bash
179 | jarvis telemetry stats          # Aggregated statistics
180 | jarvis telemetry export --json  # Export all records
181 | ```
182 | 
183 | !!! note "Telemetry is best-effort"
184 |     If telemetry setup fails (e.g., database is locked), the system continues
185 |     without telemetry rather than raising an error. Telemetry never blocks
186 |     the query flow.
187 | 
188 | ---
189 | 
190 | ## 6. Python-First
191 | 
192 | OpenJarvis provides a **clean Python API** through the `Jarvis` class. There is no framework lock-in -- the SDK is a standard Python package with dataclass-based types and no required web framework.
193 | 
194 | ```python
195 | from openjarvis import Jarvis
196 | 
197 | j = Jarvis()
198 | response = j.ask("Hello")
199 | 
200 | # Full control
201 | result = j.ask_full(
202 |     "Explain quantum computing",
203 |     model="qwen3:8b",
204 |     agent="orchestrator",
205 |     tools=["think"],
206 |     temperature=0.5,
207 |     max_tokens=2048,
208 | )
209 | 
210 | # Memory operations
211 | j.memory.index("./docs/")
212 | results = j.memory.search("quantum computing")
213 | 
214 | # Resource cleanup
215 | j.close()
216 | ```
217 | 
218 | Design choices that support this principle:
219 | 
220 | - **Dataclasses** for all structured types (`Message`, `ModelSpec`, `Trace`, etc.)
221 | - **Type hints** throughout the codebase
222 | - **No magic** -- explicit initialization, clear method signatures
223 | - **Optional dependencies** via extras (`openjarvis[server]`, `openjarvis[memory-colbert]`, etc.)
224 | - **Standard packaging** with `hatchling` build backend and `uv` package manager
225 | 
226 | ---
227 | 
228 | ## 7. OpenAI-Compatible
229 | 
230 | The API server (`jarvis serve`) implements the **OpenAI chat completions API format**, making OpenJarvis a drop-in replacement for OpenAI in existing applications.
231 | 
232 | Supported endpoints:
233 | 
234 | | Endpoint | Method | Description |
235 | |----------|--------|-------------|
236 | | `/v1/chat/completions` | POST | Chat completions (streaming and non-streaming) |
237 | | `/v1/models` | GET | List available models |
238 | | `/health` | GET | Health check |
239 | 
240 | Request and response formats match the OpenAI API specification:
241 | 
242 | ```bash
243 | curl http://localhost:8000/v1/chat/completions \
244 |   -H "Content-Type: application/json" \
245 |   -d '{
246 |     "model": "qwen3:8b",
247 |     "messages": [{"role": "user", "content": "Hello"}],
248 |     "temperature": 0.7,
249 |     "max_tokens": 1024,
250 |     "stream": false
251 |   }'
252 | ```
253 | 
254 | Streaming responses use Server-Sent Events (SSE) with `data: [DONE]` termination, matching the OpenAI streaming protocol.
255 | 
256 | Any OpenAI client library can connect to OpenJarvis:
257 | 
258 | ```python
259 | from openai import OpenAI
260 | 
261 | client = OpenAI(base_url="http://localhost:8000/v1", api_key="not-needed")
262 | response = client.chat.completions.create(
263 |     model="qwen3:8b",
264 |     messages=[{"role": "user", "content": "Hello"}],
265 | )
266 | ```
267 | 
268 | ---
269 | 
270 | ## 8. Standalone
271 | 
272 | OpenJarvis requires **no external services** for core functionality. Everything needed to run the system is included or uses standard system libraries.
273 | 
274 | | Component | Dependency |
275 | |-----------|-----------|
276 | | Configuration | TOML file, built-in `tomllib` (Python 3.11+) or `tomli` |
277 | | Memory (default) | Built-in `sqlite3` module |
278 | | Telemetry | Built-in `sqlite3` module |
279 | | Traces | Built-in `sqlite3` module |
280 | | HTTP client | `httpx` (lightweight, pure Python) |
281 | | CLI | `click` + `rich` |
282 | | Event bus | Built-in `threading` module |
283 | 
284 | The only external requirement is a running inference engine (Ollama, vLLM, etc.), which is the model server itself -- not a dependency of OpenJarvis.
285 | 
286 | Optional features that require additional packages:
287 | 
288 | | Feature | Extra | Packages |
289 | |---------|-------|----------|
290 | | FAISS memory | `openjarvis[memory-faiss]` | `faiss-cpu`, `sentence-transformers` |
291 | | ColBERT memory | `openjarvis[memory-colbert]` | `colbert-ai`, `torch` |
292 | | BM25 memory | `openjarvis[memory-bm25]` | `rank-bm25` |
293 | | API server | `openjarvis[server]` | `fastapi`, `uvicorn` |
294 | | Cloud inference | `openjarvis[inference-cloud]` | `openai`, `anthropic`, `google-genai` |
295 | | vLLM engine | `openjarvis[inference-vllm]` | `vllm` |
296 | | PDF ingestion | `openjarvis[memory-pdf]` | `pdfplumber` |
297 | | WhatsApp Baileys | `openjarvis[channel-whatsapp-baileys]` | Node.js 22+ |
298 | 
299 | This design ensures that a minimal installation (`uv sync`) gives you a fully functional system with SQLite memory, local inference, and the complete CLI -- no Docker, no external databases, no cloud accounts required.
```

---

## FILE: `docs/architecture/query-flow.md`

- bytes: 10255
- lines: 319
- sha256: `63008E8141225775CAE6BD0EDCECED072468BFED2503F82103CF8975623FD5EF`
- line terminator: LF

Line numbers below are 1-based and authoritative. Cite them.

```markdown
  1 | # Query Flow
  2 | 
  3 | This page traces the end-to-end journey of a user query through the OpenJarvis system, from the moment it enters the CLI or SDK to the final response and telemetry recording.
  4 | 
  5 | ---
  6 | 
  7 | ## Sequence Diagram
  8 | 
  9 | ```mermaid
 10 | sequenceDiagram
 11 |     actor User
 12 |     participant CLI as CLI / SDK
 13 |     participant CFG as Config & Discovery
 14 |     participant LRN as Learning (Router)
 15 |     participant AGT as Agent
 16 |     participant MEM as Memory Backend
 17 |     participant CTX as Context Injection
 18 |     participant ENG as Inference Engine
 19 |     participant TEL as Telemetry
 20 |     participant TRC as Trace Collector
 21 | 
 22 |     User->>CLI: jarvis ask "query" / j.ask("query")
 23 |     CLI->>CFG: load_config()
 24 |     CFG-->>CLI: JarvisConfig (hardware, engine defaults)
 25 | 
 26 |     CLI->>CFG: get_engine(config)
 27 |     CFG-->>CLI: (engine_key, engine_instance)
 28 | 
 29 |     CLI->>CFG: discover_engines() + discover_models()
 30 |     CFG-->>CLI: available models per engine
 31 | 
 32 |     alt Model not specified
 33 |         CLI->>LRN: select_model(RoutingContext)
 34 |         LRN-->>CLI: model_key (e.g., "qwen3:8b")
 35 |     end
 36 | 
 37 |     alt Agent mode (--agent flag)
 38 |         CLI->>AGT: agent.run(query, context)
 39 |         AGT->>MEM: retrieve(query, top_k=5)
 40 |         MEM-->>AGT: RetrievalResult[]
 41 |         AGT->>CTX: inject_context(query, messages, backend)
 42 |         CTX-->>AGT: messages with context prepended
 43 | 
 44 |         loop Tool-calling loop (max_turns)
 45 |             AGT->>ENG: generate(messages, model, tools)
 46 |             ENG-->>AGT: {content, tool_calls, usage}
 47 |             opt Tool calls present
 48 |                 AGT->>AGT: ToolExecutor.execute(tool_call)
 49 |                 AGT->>AGT: Append tool results to messages
 50 |             end
 51 |         end
 52 | 
 53 |         AGT-->>CLI: AgentResult(content, tool_results, turns)
 54 |     else Direct mode (no agent)
 55 |         CLI->>MEM: retrieve(query)
 56 |         MEM-->>CLI: RetrievalResult[]
 57 |         CLI->>CTX: inject_context(query, messages, backend)
 58 |         CTX-->>CLI: messages with context
 59 | 
 60 |         CLI->>ENG: instrumented_generate(messages, model)
 61 |         ENG-->>CLI: {content, usage}
 62 |     end
 63 | 
 64 |     CLI->>TEL: TelemetryStore records metrics
 65 |     CLI->>TRC: TraceCollector saves Trace
 66 |     CLI-->>User: Response text
 67 | ```
 68 | 
 69 | ---
 70 | 
 71 | ## Direct Mode vs Agent Mode
 72 | 
 73 | OpenJarvis supports two query processing paths, selected by the `--agent` CLI flag or the `agent` parameter in the SDK.
 74 | 
 75 | ### Direct Mode (Default)
 76 | 
 77 | In direct mode, the query goes straight to the inference engine with optional memory context. This is the simplest path -- one inference call, no tool loop.
 78 | 
 79 | ```bash
 80 | # CLI
 81 | jarvis ask "What is the capital of France?"
 82 | 
 83 | # SDK
 84 | j = Jarvis()
 85 | response = j.ask("What is the capital of France?")
 86 | ```
 87 | 
 88 | ### Agent Mode
 89 | 
 90 | In agent mode, the query is handled by a named agent that can perform multiple inference rounds and invoke tools. The `OrchestratorAgent` is the most common choice, enabling a multi-turn tool-calling loop.
 91 | 
 92 | ```bash
 93 | # CLI
 94 | jarvis ask --agent orchestrator --tools calculator,think "What is 2^10 + 3^5?"
 95 | 
 96 | # SDK
 97 | response = j.ask("What is 2^10 + 3^5?", agent="orchestrator", tools=["calculator"])
 98 | ```
 99 | 
100 | ---
101 | 
102 | ## Step-by-Step Walkthrough
103 | 
104 | ### Step 1: Configuration Loading
105 | 
106 | The journey begins with loading the system configuration:
107 | 
108 | ```python
109 | config = load_config()  # Reads ~/.openjarvis/config.toml
110 | ```
111 | 
112 | This step:
113 | 
114 | - Detects system hardware (GPU vendor/model, CPU, RAM)
115 | - Recommends the best inference engine for the detected hardware
116 | - Overlays any user overrides from the TOML file
117 | - Returns a `JarvisConfig` dataclass with all settings
118 | 
119 | ### Step 2: Engine Discovery
120 | 
121 | Next, the system finds a running inference engine:
122 | 
123 | ```python
124 | resolved = get_engine(config, engine_key)
125 | # Returns (engine_key, engine_instance) or None
126 | ```
127 | 
128 | The discovery process:
129 | 
130 | 1. If a specific engine was requested (`--engine` flag), try that engine
131 | 2. Otherwise, try the default engine from config (e.g., `"ollama"`)
132 | 3. If the default is unhealthy, probe all registered engines and use the first healthy one
133 | 4. If no engine is available, exit with an error message
134 | 
135 | ### Step 3: Model Discovery and Registration
136 | 
137 | Once an engine is found, the system discovers available models:
138 | 
139 | ```python
140 | register_builtin_models()          # Register known models (catalog)
141 | all_engines = discover_engines(config)
142 | all_models = discover_models(all_engines)
143 | for ek, model_ids in all_models.items():
144 |     merge_discovered_models(ek, model_ids)  # Register runtime-discovered models
145 | ```
146 | 
147 | ### Step 4: Model Routing
148 | 
149 | If no model was explicitly specified, the router policy selects one:
150 | 
151 | ```python
152 | from openjarvis.learning import ensure_registered
153 | from openjarvis.learning.router import build_routing_context
154 | ensure_registered()  # Ensure learning policies are registered
155 | 
156 | policy_key = router_policy or config.learning.routing.policy
157 | router_cls = RouterPolicyRegistry.get(policy_key)
158 | router = router_cls(
159 |     available_models=all_models.get(engine_name, []),
160 |     default_model=config.intelligence.default_model,
161 |     fallback_model=config.intelligence.fallback_model,
162 | )
163 | 
164 | ctx = build_routing_context(query_text)
165 | model_name = router.select_model(ctx)
166 | ```
167 | 
168 | The `build_routing_context()` function (in `learning/router.py`) analyzes the query for code patterns, math keywords, length, and urgency. The router then applies its rules (heuristic or learned) to select the optimal model.
169 | 
170 | ### Step 5: Memory Context Injection
171 | 
172 | If memory context injection is enabled (default: `true`) and the memory backend has indexed documents:
173 | 
174 | ```python
175 | backend = _get_memory_backend(config)
176 | if backend is not None:
177 |     ctx_cfg = ContextConfig(
178 |         top_k=config.memory.context_top_k,        # Default: 5
179 |         min_score=config.memory.context_min_score,  # Default: 0.1
180 |         max_context_tokens=config.memory.context_max_tokens,  # Default: 2048
181 |     )
182 |     messages = inject_context(query_text, messages, backend, config=ctx_cfg)
183 | ```
184 | 
185 | This retrieves relevant chunks from the memory backend and prepends a system message with the retrieved context and source attribution.
186 | 
187 | !!! tip "Disabling context injection"
188 |     Use `--no-context` on the CLI or `context=False` in the SDK to skip memory context injection.
189 | 
190 | ### Step 6: Inference Generation
191 | 
192 | **In direct mode**, the query is sent to the engine via the instrumented wrapper:
193 | 
194 | ```python
195 | result = instrumented_generate(
196 |     engine, messages,
197 |     model=model_name,
198 |     bus=bus,
199 |     temperature=temperature,
200 |     max_tokens=max_tokens,
201 | )
202 | ```
203 | 
204 | The `instrumented_generate()` wrapper:
205 | 
206 | 1. Publishes `INFERENCE_START` on the event bus
207 | 2. Records the start time
208 | 3. Calls `engine.generate()`
209 | 4. Records end time, calculates latency
210 | 5. Publishes `INFERENCE_END` with timing and token counts
211 | 6. Publishes `TELEMETRY_RECORD` with the full `TelemetryRecord`
212 | 
213 | **In agent mode**, the agent manages inference calls internally, potentially making multiple rounds with tool calls in between.
214 | 
215 | ### Step 7: Tool Execution (Agent Mode Only)
216 | 
217 | When the `OrchestratorAgent` receives tool calls in the model's response:
218 | 
219 | 1. Each tool call is dispatched to the `ToolExecutor`
220 | 2. The executor publishes `TOOL_CALL_START`, executes the tool, publishes `TOOL_CALL_END`
221 | 3. Tool results are appended to the message history as `TOOL` messages
222 | 4. The updated messages are sent back to the engine for the next round
223 | 5. This loop continues until the model responds without tool calls or `max_turns` is reached
224 | 
225 | ### Step 8: Telemetry Recording
226 | 
227 | After every inference call, a `TelemetryRecord` is created and persisted:
228 | 
229 | ```python
230 | @dataclass(slots=True)
231 | class TelemetryRecord:
232 |     timestamp: float
233 |     model_id: str
234 |     prompt_tokens: int
235 |     completion_tokens: int
236 |     total_tokens: int
237 |     latency_seconds: float
238 |     ttft: float              # Time to first token
239 |     cost_usd: float
240 |     energy_joules: float
241 |     power_watts: float
242 |     engine: str
243 |     agent: str
244 |     metadata: Dict[str, Any]
245 | ```
246 | 
247 | The `TelemetryStore` subscribes to `TELEMETRY_RECORD` events on the EventBus and writes records to `~/.openjarvis/telemetry.db`.
248 | 
249 | ### Step 9: Trace Recording
250 | 
251 | When a `TraceCollector` is wrapping the agent, a complete `Trace` is built from the events captured during execution:
252 | 
253 | 1. All `INFERENCE_START`/`END` events become `GENERATE` steps
254 | 2. All `TOOL_CALL_START`/`END` events become `TOOL_CALL` steps
255 | 3. All `MEMORY_RETRIEVE` events become `RETRIEVE` steps
256 | 4. A final `RESPOND` step captures the output
257 | 5. The trace is saved to the `TraceStore` and `TRACE_COMPLETE` is published
258 | 
259 | ### Step 10: Response Delivery
260 | 
261 | The final response is delivered to the user:
262 | 
263 | - **CLI:** Printed to stdout (or as JSON with `--json`)
264 | - **SDK:** Returned as a string from `ask()` or as a dict from `ask_full()`
265 | 
266 | ---
267 | 
268 | ## EventBus Activity During a Query
269 | 
270 | The following events are published during a typical query in agent mode:
271 | 
272 | ```
273 | AGENT_TURN_START    {agent: "orchestrator", input: "What is 2+2?"}
274 | INFERENCE_START     {model: "qwen3:8b", engine: "ollama", turn: 1}
275 | INFERENCE_END       {model: "qwen3:8b", engine: "ollama", turn: 1}
276 | TELEMETRY_RECORD    {model_id: "qwen3:8b", latency: 0.8, tokens: 150}
277 | TOOL_CALL_START     {tool: "calculator", arguments: {expression: "2+2"}}
278 | TOOL_CALL_END       {tool: "calculator", success: true, latency: 0.01}
279 | INFERENCE_START     {model: "qwen3:8b", engine: "ollama", turn: 2}
280 | INFERENCE_END       {model: "qwen3:8b", engine: "ollama", turn: 2}
281 | TELEMETRY_RECORD    {model_id: "qwen3:8b", latency: 0.5, tokens: 80}
282 | AGENT_TURN_END      {agent: "orchestrator", turns: 2, content_length: 12}
283 | TRACE_COMPLETE      {trace: Trace(...)}
284 | ```
285 | 
286 | ---
287 | 
288 | ## SDK Query Flow
289 | 
290 | The `Jarvis` class in `sdk.py` provides the same query flow through a Python API:
291 | 
292 | ```python
293 | from openjarvis import Jarvis
294 | 
295 | j = Jarvis(model="qwen3:8b", engine_key="ollama")
296 | 
297 | # Direct mode
298 | response = j.ask("Hello")
299 | 
300 | # Agent mode with tools
301 | response = j.ask(
302 |     "What is 2^10?",
303 |     agent="orchestrator",
304 |     tools=["calculator"],
305 | )
306 | 
307 | # Full result with metadata
308 | result = j.ask_full("Hello")
309 | # {
310 | #     "content": "Hello! How can I help you?",
311 | #     "usage": {"prompt_tokens": 10, "completion_tokens": 15, "total_tokens": 25},
312 | #     "model": "qwen3:8b",
313 | #     "engine": "ollama",
314 | # }
315 | 
316 | j.close()
317 | ```
318 | 
319 | The SDK handles lazy engine initialization, telemetry setup, memory context injection, and resource cleanup internally. The `ask()` method delegates to `ask_full()` and extracts just the content string.
```

---

# MANIFEST

| file | found | bytes | lines | sha256 |
|---|---|---|---|---|
| `docs/getting-started/installation.md` | yes | 9918 | 340 | `13ED46C2FDC05F07...` |
| `docs/getting-started/configuration.md` | yes | 35541 | 1115 | `FAA23D2DF03E1706...` |
| `docs/getting-started/install.md` | yes | 3767 | 113 | `1F878AB0D08F78BB...` |
| `docs/architecture/design-principles.md` | yes | 10353 | 299 | `4F9ED52CAE44D760...` |
| `docs/architecture/query-flow.md` | yes | 10255 | 319 | `63008E8141225775...` |

These hashes pin the exact bytes you reviewed. If a later patch is built against different bytes, the mismatch is detectable.

