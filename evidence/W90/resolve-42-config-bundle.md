# RESOLVE 4.2 CONFIG BUNDLE - W90 2026-09-25T20:51:16 - stages: 1=base af21bc18, 2=ours (Graystone 3df27c53), 3=theirs (author a6dcf846)

## ===== pyproject.toml : OUR COMMITS SINCE AUTHOR BASE =====
685947be W83 Office S1 (Phase 2 pulled forward by owner): python-pptx 1.0.2 + openpyxl 3.1.5 via uv add --no-sync (pyproject +2, uv.lock +49/-0) and uv pip install of the locked versions (+et-xmlfile, xlsxwriter; nothing removed); python-docx 1.2.0 already an author dependency; round-trip docx/pptx/xlsx and author docx reader verified; findings: venv has no pip (uv-managed), grpcio 1.78.1 yanked in lock
e0e36523 Fix: wire tools to native_openhands agent - file_read, think, calculator, code_interpreter, shell_exec, file_write now loading at startup
670c3aaf feat: numbered question UI buttons, sub-bullet fix, trailing text relaxed, shell_exec utf-8 encoding, croniter installed, persistent API keys hydrate from Rust backend, fix: use npx tauri build for full Rust exe compile (npm run build:tauri is frontend only)
3782799b feat: speech subsystem, auto-focus, pyproject fixes, pynvml->nvidia-ml-py, startup scripts

## ===== pyproject.toml : CONFLICTED WORKING FILE (markers) =====
[build-system]
requires = ["hatchling", "hatch-vcs"]
build-backend = "hatchling.build"

[project]
name = "OpenJarvis"
<<<<<<< HEAD
version = "1.1.0"
description = "OpenJarvis Ã¢â‚¬â€ modular AI assistant backend with composable intelligence primitives"
readme = "README.md"
requires-python = ">=3.11"
=======
dynamic = ["version"]
description = "OpenJarvis â€” modular AI assistant backend with composable intelligence primitives"
readme = "README.md"
# Upper bound: numpy 2.2.x (pinned transitively via datasets/pandas) ships no
# cp314 Windows wheel, so under Python 3.14 uv would compile numpy from source
# (Meson) and fail on Windows boxes without a C toolchain (#350). Cap to the
# range that has prebuilt wheels; matches the classifiers (3.10â€“3.13).
requires-python = ">=3.10,<3.14"
>>>>>>> a6dcf846
license = {text = "Apache-2.0"}
authors = [
    {name = "Open Jarvis Contributors"},
]
classifiers = [
    "Development Status :: 3 - Alpha",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: Apache Software License",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
    "Programming Language :: Python :: 3.13",
    "Topic :: Scientific/Engineering :: Artificial Intelligence",
]
dependencies = [
    "click>=8",
    "croniter>=2.0",
    "datasets>=4.5.0",
    "ddgs>=9.11.4",
    "httpx>=0.27",
    "kokoro>=0.9.4",
    "numpy>=2.2.6",
    "openai>=1.30",
    "nvidia-ml-py>=12.560.30",
    "posthog>=3.0",
<<<<<<< HEAD
    "nvidia-ml-py>=12.0",
    "python-telegram-bot>=22.6",
=======
    "python-telegram-bot>=22.8",
>>>>>>> a6dcf846
    "rich>=13",
    "soundfile>=0.14.0",
    "tomli>=2.0; python_version < '3.11'",
    "tomlkit>=0.12",
<<<<<<< HEAD
    "croniter>=6.0.0",
    "pdfplumber>=0.11.9",
    "python-docx>=1.2.0",
    "python-pptx>=1.0.2",
    "openpyxl>=3.1.5",
=======
    "websockets>=15.0.1",
>>>>>>> a6dcf846
]

[project.optional-dependencies]
dev = [
    "maturin>=1.12.6",
    "pytest>=8",
    "pytest-asyncio>=0.24",
    "pytest-cov>=5",
    "pytest-xdist>=3",
    "respx>=0.22",
    "ruff>=0.4",
    "pre-commit>=3.0",
]
inference-mlx = ["mlx-lm>=0.31.1; sys_platform == 'darwin'"]
inference-vllm = ["vllm>=0.16.0"]
inference-cloud = [
    "openai>=1.30",
    "anthropic>=0.30",
]
inference-google = [
    "google-genai>=1.0",
]
# Exact security pin covering the LiteLLM command-injection advisories.
# Avoid 1.82.7/1.82.8, which were affected by the March supply-chain incident.
inference-litellm = ["litellm==1.100.1"]
inference-gemma = ["pygemma>=0.1.3"]
tools-search = [
    "tavily-python>=0.3",
    "ddgs>=9.11.4",
]
memory-faiss = [
    "faiss-cpu>=1.7",
    "sentence-transformers>=2.2",
    "numpy>=1.24",
]
memory-colbert = [
    "colbert-ai>=0.2",
    "torch>=2.0",
]
memory-pdf = ["pdfplumber>=0.10"]
memory-bm25 = ["rank-bm25>=0.2.2"]
server = [
    "fastapi>=0.110",
    "uvicorn>=0.30",
    "pydantic>=2.0",
    "python-multipart>=0.0.9",
]
desktop = [
    "fastapi>=0.110",
    "uvicorn>=0.30",
    "pydantic>=2.0",
    "python-multipart>=0.0.9",
    "faster-whisper>=1.0",
    # 1.24.x declares Python 3.10 support but publishes no cp310 wheels (#917).
    "onnxruntime<1.24; python_version < '3.11'",
    "numpy>=1.24",
    "sounddevice>=0.5",
    "soundfile>=0.12",
]
# Local neural TTS. Kokoro pulls spacy/misaki for G2P; espeak-ng must also be
# present on PATH (brew install espeak-ng) for out-of-dictionary words.
voice = [
    "kokoro>=0.9",
    "soundfile>=0.12",
    "sounddevice>=0.5",  # play_wav / record_until_silence in speech/voice_io.py
    "numpy>=1.24",
]
openhands = ["openhands-sdk>=1.0; python_version >= '3.12'"]
# Apple Foundation Models (on-device AFM 3). Needs an Apple Silicon Mac on
# macOS 26+ with Apple Intelligence enabled. The SDK compiles Swift bindings
# at install time, so a full Xcode is required -- Command Line Tools alone
# fail:
#   DEVELOPER_DIR=/Applications/Xcode.app/Contents/Developer \
#       uv pip install -e '.[afm]'
# 0.2.1 is the floor: it added SystemLanguageModel.context_size and
# token_count, which the engine uses for token accounting.
afm = ["apple-fm-sdk>=0.2.1; sys_platform == 'darwin'"]
gpu-metrics = ["pynvml>=12.0"]
energy-amd = ["amdsmi>=6.1"]
# `zeus-ml[apple]` was the previous spelling and never worked: zeus-ml has no
# `apple` extra, and its `zeus.device.soc` package (which wraps this library)
# landed on master after the last zeus release, so no published zeus-ml
# contains it. Depend on the underlying IOReport extension directly.
energy-apple = ["zeus-apple-silicon>=1.1.0; sys_platform == 'darwin'"]
energy-all = [
    "pynvml>=12.0",
    "amdsmi>=6.1",
    "zeus-apple-silicon>=1.1.0; sys_platform == 'darwin'",
]
orchestrator-training = ["torch>=2.0", "transformers>=4.40"]
learning-dspy = ["dspy>=2.6"]
learning-gepa = ["gepa>=0.1"]
channel-telegram = ["python-telegram-bot>=21.0"]
channel-discord = ["discord.py>=2.3"]
channel-slack = ["slack-sdk>=3.27"]
channel-line = ["line-bot-sdk>=3.0"]
channel-viber = ["viberbot>=1.0"]
channel-messenger = ["pymessenger>=0.0.7"]
channel-reddit = ["praw>=7.0"]
channel-mastodon = ["Mastodon.py>=1.8"]
channel-xmpp = ["slixmpp>=1.8"]
channel-rocketchat = ["rocketchat-API>=1.30"]
channel-zulip = ["zulip>=0.9"]
channel-twitter = ["httpx>=0.27"]
channel-twitch = ["twitchio>=2.6"]
channel-nostr = ["pynostr>=0.6"]
channel-twilio = ["twilio>=9.0"]
channel-gmail = [
    "google-api-python-client>=2.0",
    "google-auth-oauthlib>=1.0",
    "google-auth-httplib2>=0.2",
]
browser = ["playwright>=1.40"]
media = ["openai>=1.30"]
mining-pearl-vllm = ["docker>=7.0", "httpx>=0.27"]
pdf = ["pdfplumber>=0.10"]
# Kept as a compatibility extra for existing install commands. Cron support is
# a core scheduler contract now, so croniter is also installed unconditionally.
scheduler = ["croniter>=2.0"]
security-signing = ["cryptography>=43"]
sandbox-wasm = ["wasmtime>=25"]
sandbox-docker = ["docker>=7.0"]
dashboard = ["textual>=0.80"]
<<<<<<< HEAD
speech = ["faster-whisper>=1.2.1", "kokoro-onnx>=0.5.0", "ctranslate2>=4.8.0", "onnxruntime>=1.14", "av>=17.1.0", "sounddevice>=0.4.6"]
=======
speech = [
    "faster-whisper>=1.0",
    # Keep the pip-visible speech extra installable on supported Python 3.10.
    "onnxruntime<1.24; python_version < '3.11'",
    "numpy>=1.24",
    "sounddevice>=0.5",
    "soundfile>=0.12",
]
>>>>>>> a6dcf846
speech-deepgram = ["deepgram-sdk>=3.0"]
eval-wandb = ["wandb>=0.17"]
eval-sheets = ["gspread>=6.0", "google-auth>=2.0"]
mining-pearl-cpu = [
    # Pearl Python packages (py-pearl-mining, miner-base, pearl-gateway) are
    # not on PyPI yet. They are installed at first `mine init` via the
    # build-from-pin path in src/openjarvis/mining/_install.py:build_from_pin().
    # When Pearl publishes wheels, replace the line below with version pins.
    #
    # The extra remains as a feature-flag namespace so users can run
    # `uv sync --extra mining-pearl-cpu` to opt-in (it succeeds with no
    # additional resolution today; the actual install happens on demand).
]
framework-comparison = ["polars>=1.0"]
docs = [
    "mkdocs>=1.6",
    "mkdocs-material>=9.5",
    "mkdocstrings[python]>=0.25",
    "mkdocs-gen-files>=0.5",
    "mkdocs-literate-nav>=0.6",
]

[project.urls]
Homepage = "https://github.com/open-jarvis/OpenJarvis"
Documentation = "https://open-jarvis.github.io/OpenJarvis/"
Repository = "https://github.com/open-jarvis/OpenJarvis"
Issues = "https://github.com/open-jarvis/OpenJarvis/issues"

[project.scripts]
jarvis = "openjarvis.cli:main"
openjarvis-eval = "openjarvis.evals.cli:main"

# Version is derived from git tags by hatch-vcs (see #526). For source/editable
# checkouts this yields the true `git describe` version (e.g. 1.0.3.dev109+g<sha>)
# rather than a stale static string. CI release builds override this with
# SETUPTOOLS_SCM_PRETEND_VERSION so the published version equals the pushed tag.
#
# setuptools_scm cannot bump custom `.devN` tags (only `.dev0`), so the autotag
# `vX.Y.Z.devN` tags are deliberately EXCLUDED from version derivation here; the
# base is taken from the latest plain release tag (vX.Y.Z) and the dev distance
# is computed from commit count since that release.
[tool.hatch.version]
source = "vcs"

[tool.hatch.version.raw-options]
tag_regex = '^v(?P<version>[0-9]+\.[0-9]+\.[0-9]+)$'
git_describe_command = [
    "git", "describe", "--dirty", "--tags", "--long",
    "--match", "v[0-9]*", "--exclude", "*dev*", "--exclude", "*rc*", "--exclude", "desktop-*",
]
# Builds without a git checkout (e.g. the `COPY src/ src/` Docker stages, which
# never include .git) can't run `git describe`. Without a fallback that would
# hard-fail the build. Mirror the runtime sentinel in src/openjarvis/__init__.py.
# Such builds can inject the real version via SETUPTOOLS_SCM_PRETEND_VERSION.
fallback_version = "0.0.0+unknown"

[tool.uv.sources]
openjarvis-rust = { path = "rust/crates/openjarvis-python" }

[tool.hatch.build.targets.sdist]
# Tauri release bundles carry these executables; Python source distributions
# must not duplicate platform binaries on every PyPI release.
exclude = [
    "/desktop/src-tauri/binaries",
    "/frontend/src-tauri/binaries",
]
# The publishing workflow builds this UI before packaging. Keep its generated
# files even though the directory is intentionally ignored by Git.
artifacts = ["/src/openjarvis/server/static/**"]

[tool.hatch.build.targets.wheel]
packages = ["src/openjarvis"]
artifacts = ["/src/openjarvis/server/static/**"]
exclude = [
    "/src/openjarvis/agents/claude_code_runner",
]

[tool.hatch.build.targets.wheel.force-include]
"src/openjarvis/agents/claude_code_runner/index.mjs" = "_node_modules/claude_code_runner/index.mjs"
"src/openjarvis/agents/claude_code_runner/package.json" = "_node_modules/claude_code_runner/package.json"
"src/openjarvis/channels/whatsapp_baileys_bridge" = "_node_modules/whatsapp_baileys_bridge"
"scripts/install" = "_install_scripts"
"deploy/windows" = "_deploy/windows"

[tool.pytest.ini_options]
testpaths = ["tests"]
markers = [
    "amd: requires AMD GPU",
    "apple: requires Apple Silicon",
    "cloud: requires cloud API keys",
    "docker: requires a working Docker daemon (no GPU required)",
    "live: requires running inference engine",
    "macos15: requires macOS 15+ (Sequoia) for Apple FM",
    "live_channel: requires real channel credentials (env vars)",
    "nvidia: requires NVIDIA GPU",
    "slow: long-running test",
    "hub: downloads real datasets from the HuggingFace Hub at runtime; excluded from the default CI lane (run with -m hub)",
    "live_external: requires HERMES_AGENT_PATH and OPENCLAW_PATH; spawns real foreign-framework subprocesses",
    "modal: requires Modal token + network; runs real swebench harness on Modal",
]

[tool.ruff]
target-version = "py310"
src = ["src", "tests"]

[tool.ruff.lint]
select = ["E", "F", "I", "W"]

[tool.ruff.lint.per-file-ignores]
"src/openjarvis/evals/datasets/*.py" = ["E501"]
"src/openjarvis/evals/scorers/*.py" = ["E501"]
# hybrid/ is research code with long prompt strings and paradigm-specific
<<<<<<< HEAD
# config dicts Ã¢â‚¬â€ same relaxation as evals research code above.
"src/openjarvis/agents/hybrid/*.py" = ["E501"]
# research_loop.py carries the multi-paragraph planner system prompt as
# inline string literals; line-length wrapping would harm readability of
# the prompt itself.
=======
# config dicts â€” same relaxation as evals research code above. The ``**`` glob
# also covers subpackages (e.g. hybrid/skillorchestra/), which the prior
# ``hybrid/*.py`` glob missed.
"src/openjarvis/agents/hybrid/**/*.py" = ["E501"]
# research_loop.py carries long prompt strings too (documented in CLAUDE.md);
# the ignore was missing here.
>>>>>>> a6dcf846
"src/openjarvis/agents/research_loop.py" = ["E501"]

[dependency-groups]
dev = [
    "maturin>=1.12.6",
]
<<<<<<< HEAD

=======
# openjarvis_rust is the native PyO3 extension, built from the local Rust
# workspace. It lives in a uv dependency group (PEP 735) â€” not the published
# `desktop` extra â€” so `uv sync --group desktop-native` builds it from source
# for the desktop app, while `pip install openjarvis[desktop]` from PyPI does
# NOT try to resolve openjarvis-rust from PyPI, where it isn't published
# (dependency groups are excluded from wheel metadata). See #584 / #615.
desktop-native = [
    "openjarvis-rust",
]
>>>>>>> a6dcf846


## ===== pyproject.toml : STAGE 1 =====
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "OpenJarvis"
version = "1.0.1"
description = "OpenJarvis ΓÇö modular AI assistant backend with composable intelligence primitives"
readme = "README.md"
requires-python = ">=3.10"
license = {text = "Apache-2.0"}
authors = [
    {name = "Open Jarvis Contributors"},
]
classifiers = [
    "Development Status :: 3 - Alpha",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: Apache Software License",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
    "Programming Language :: Python :: 3.13",
    "Topic :: Scientific/Engineering :: Artificial Intelligence",
]
dependencies = [
    "click>=8",
    "datasets>=4.5.0",
    "ddgs>=9.11.4",
    "httpx>=0.27",
    "openai>=1.30",
    "posthog>=3.0",
    "pynvml>=13.0.1",
    "python-telegram-bot>=22.6",
    "rich>=13",
    "tomli>=2.0; python_version < '3.11'",
    "tomlkit>=0.12",
]

[project.optional-dependencies]
dev = [
    "maturin>=1.12.6",
    "pytest>=8",
    "pytest-asyncio>=0.24",
    "pytest-cov>=5",
    "respx>=0.22",
    "ruff>=0.4",
    "pre-commit>=3.0",
]
inference-mlx = ["mlx-lm>=0.31.1; sys_platform == 'darwin'"]
inference-vllm = ["vllm>=0.16.0"]
inference-cloud = [
    "openai>=1.30",
    "anthropic>=0.30",
]
inference-google = [
    "google-genai>=1.0",
]
inference-litellm = ["litellm>=1.40"]
inference-gemma = ["pygemma>=0.1.3"]
tools-search = [
    "tavily-python>=0.3",
    "ddgs>=9.11.4",
]
memory-faiss = [
    "faiss-cpu>=1.7",
    "sentence-transformers>=2.2",
    "numpy>=1.24",
]
memory-colbert = [
    "colbert-ai>=0.2",
    "torch>=2.0",
]
memory-pdf = ["pdfplumber>=0.10"]
memory-bm25 = ["rank-bm25>=0.2.2"]
server = [
    "fastapi>=0.110",
    "uvicorn>=0.30",
    "pydantic>=2.0",
    "python-multipart>=0.0.9",
]
openhands = ["openhands-sdk>=1.0; python_version >= '3.12'"]
gpu-metrics = ["pynvml>=12.0"]
energy-amd = ["amdsmi>=6.1"]
energy-apple = ["zeus-ml[apple]"]
energy-all = ["pynvml>=12.0", "amdsmi>=6.1", "zeus-ml[apple]"]
orchestrator-training = ["torch>=2.0", "transformers>=4.40"]
learning-dspy = ["dspy>=2.6"]
learning-gepa = ["gepa>=0.1"]
# ACE (Agentic Context Engineering) is supported via
# ``openjarvis.learning.agents.ace_optimizer`` but ACE upstream isn't on
# PyPI and isn't structured as an installable Python package as of
# v1.0.1, so there's no ``learning-ace`` extra. To use ACE, follow the
# manual setup in docs/learning/ace.md (clone the upstream repo, add
# its ``src/`` to PYTHONPATH).
channel-telegram = ["python-telegram-bot>=21.0"]
channel-discord = ["discord.py>=2.3"]
channel-slack = ["slack-sdk>=3.27"]
channel-line = ["line-bot-sdk>=3.0"]
channel-viber = ["viberbot>=1.0"]
channel-messenger = ["pymessenger>=0.0.7"]
channel-reddit = ["praw>=7.0"]
channel-mastodon = ["Mastodon.py>=1.8"]
channel-xmpp = ["slixmpp>=1.8"]
channel-rocketchat = ["rocketchat-API>=1.30"]
channel-zulip = ["zulip>=0.9"]
channel-twitter = ["httpx>=0.27"]
channel-twitch = ["twitchio>=2.6"]
channel-nostr = ["pynostr>=0.6"]
channel-twilio = ["twilio>=9.0"]
channel-gmail = [
    "google-api-python-client>=2.0",
    "google-auth-oauthlib>=1.0",
    "google-auth-httplib2>=0.2",
]
browser = ["playwright>=1.40"]
media = ["openai>=1.30"]
mining-pearl-vllm = ["docker>=7.0", "httpx>=0.27"]
pdf = ["pdfplumber>=0.10"]
scheduler = ["croniter>=2.0"]
security-signing = ["cryptography>=43"]
sandbox-wasm = ["wasmtime>=25"]
sandbox-docker = ["docker>=7.0"]
dashboard = ["textual>=0.80"]
speech = ["faster-whisper>=1.0"]
speech-deepgram = ["deepgram-sdk>=3.0"]
eval-wandb = ["wandb>=0.17"]
eval-sheets = ["gspread>=6.0", "google-auth>=2.0"]
mining-pearl-cpu = [
    # Pearl Python packages (py-pearl-mining, miner-base, pearl-gateway) are
    # not on PyPI yet. They are installed at first `mine init` via the
    # build-from-pin path in src/openjarvis/mining/_install.py:build_from_pin().
    # When Pearl publishes wheels, replace the line below with version pins.
    #
    # The extra remains as a feature-flag namespace so users can run
    # `uv sync --extra mining-pearl-cpu` to opt-in (it succeeds with no
    # additional resolution today; the actual install happens on demand).
]
framework-comparison = ["polars>=1.0"]
docs = [
    "mkdocs>=1.6",
    "mkdocs-material>=9.5",
    "mkdocstrings[python]>=0.25",
    "mkdocs-gen-files>=0.5",
    "mkdocs-literate-nav>=0.6",
]

[project.urls]
Homepage = "https://github.com/open-jarvis/OpenJarvis"
Documentation = "https://open-jarvis.github.io/OpenJarvis/"
Repository = "https://github.com/open-jarvis/OpenJarvis"
Issues = "https://github.com/open-jarvis/OpenJarvis/issues"

[project.scripts]
jarvis = "openjarvis.cli:main"

[tool.hatch.build.targets.wheel]
packages = ["src/openjarvis"]

[tool.hatch.build.targets.wheel.force-include]
"src/openjarvis/agents/claude_code_runner" = "_node_modules/claude_code_runner"
"src/openjarvis/channels/whatsapp_baileys_bridge" = "_node_modules/whatsapp_baileys_bridge"
"scripts/install" = "_install_scripts"

[tool.pytest.ini_options]
testpaths = ["tests"]
markers = [
    "amd: requires AMD GPU",
    "apple: requires Apple Silicon",
    "cloud: requires cloud API keys",
    "docker: requires a working Docker daemon (no GPU required)",
    "live: requires running inference engine",
    "macos15: requires macOS 15+ (Sequoia) for Apple FM",
    "live_channel: requires real channel credentials (env vars)",
    "nvidia: requires NVIDIA GPU",
    "slow: long-running test",
    "live_external: requires HERMES_AGENT_PATH and OPENCLAW_PATH; spawns real foreign-framework subprocesses",
]

[tool.ruff]
target-version = "py310"
src = ["src", "tests"]

[tool.ruff.lint]
select = ["E", "F", "I", "W"]

[tool.ruff.lint.per-file-ignores]
"src/openjarvis/evals/datasets/*.py" = ["E501"]
"src/openjarvis/evals/scorers/*.py" = ["E501"]
# hybrid/ is research code with long prompt strings and paradigm-specific
# config dicts ΓÇö same relaxation as evals research code above.
"src/openjarvis/agents/hybrid/*.py" = ["E501"]
# research_loop.py carries the multi-paragraph planner system prompt as
# inline string literals; line-length wrapping would harm readability of
# the prompt itself.
"src/openjarvis/agents/research_loop.py" = ["E501"]

[dependency-groups]
dev = [
    "maturin>=1.12.6",
]

## ===== pyproject.toml : STAGE 2 =====
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "OpenJarvis"
version = "1.1.0"
description = "OpenJarvis ├óΓé¼ΓÇ¥ modular AI assistant backend with composable intelligence primitives"
readme = "README.md"
requires-python = ">=3.11"
license = {text = "Apache-2.0"}
authors = [
    {name = "Open Jarvis Contributors"},
]
classifiers = [
    "Development Status :: 3 - Alpha",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: Apache Software License",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
    "Programming Language :: Python :: 3.13",
    "Topic :: Scientific/Engineering :: Artificial Intelligence",
]
dependencies = [
    "click>=8",
    "datasets>=4.5.0",
    "ddgs>=9.11.4",
    "httpx>=0.27",
    "kokoro>=0.9.4",
    "numpy>=2.2.6",
    "openai>=1.30",
    "posthog>=3.0",
    "nvidia-ml-py>=12.0",
    "python-telegram-bot>=22.6",
    "rich>=13",
    "soundfile>=0.14.0",
    "tomli>=2.0; python_version < '3.11'",
    "tomlkit>=0.12",
    "croniter>=6.0.0",
    "pdfplumber>=0.11.9",
    "python-docx>=1.2.0",
    "python-pptx>=1.0.2",
    "openpyxl>=3.1.5",
]

[project.optional-dependencies]
dev = [
    "maturin>=1.12.6",
    "pytest>=8",
    "pytest-asyncio>=0.24",
    "pytest-cov>=5",
    "respx>=0.22",
    "ruff>=0.4",
    "pre-commit>=3.0",
]
inference-mlx = ["mlx-lm>=0.31.1; sys_platform == 'darwin'"]
inference-vllm = ["vllm>=0.16.0"]
inference-cloud = [
    "openai>=1.30",
    "anthropic>=0.30",
]
inference-google = [
    "google-genai>=1.0",
]
inference-litellm = ["litellm>=1.40"]
inference-gemma = ["pygemma>=0.1.3"]
tools-search = [
    "tavily-python>=0.3",
    "ddgs>=9.11.4",
]
memory-faiss = [
    "faiss-cpu>=1.7",
    "sentence-transformers>=2.2",
    "numpy>=1.24",
]
memory-colbert = [
    "colbert-ai>=0.2",
    "torch>=2.0",
]
memory-pdf = ["pdfplumber>=0.10"]
memory-bm25 = ["rank-bm25>=0.2.2"]
server = [
    "fastapi>=0.110",
    "uvicorn>=0.30",
    "pydantic>=2.0",
    "python-multipart>=0.0.9",
]
openhands = ["openhands-sdk>=1.0; python_version >= '3.12'"]
gpu-metrics = ["pynvml>=12.0"]
energy-amd = ["amdsmi>=6.1"]
energy-apple = ["zeus-ml[apple]"]
energy-all = ["pynvml>=12.0", "amdsmi>=6.1", "zeus-ml[apple]"]
orchestrator-training = ["torch>=2.0", "transformers>=4.40"]
learning-dspy = ["dspy>=2.6"]
learning-gepa = ["gepa>=0.1"]
# ACE (Agentic Context Engineering) is supported via
# ``openjarvis.learning.agents.ace_optimizer`` but ACE upstream isn't on
# PyPI and isn't structured as an installable Python package as of
# v1.0.1, so there's no ``learning-ace`` extra. To use ACE, follow the
# manual setup in docs/learning/ace.md (clone the upstream repo, add
# its ``src/`` to PYTHONPATH).
channel-telegram = ["python-telegram-bot>=21.0"]
channel-discord = ["discord.py>=2.3"]
channel-slack = ["slack-sdk>=3.27"]
channel-line = ["line-bot-sdk>=3.0"]
channel-viber = ["viberbot>=1.0"]
channel-messenger = ["pymessenger>=0.0.7"]
channel-reddit = ["praw>=7.0"]
channel-mastodon = ["Mastodon.py>=1.8"]
channel-xmpp = ["slixmpp>=1.8"]
channel-rocketchat = ["rocketchat-API>=1.30"]
channel-zulip = ["zulip>=0.9"]
channel-twitter = ["httpx>=0.27"]
channel-twitch = ["twitchio>=2.6"]
channel-nostr = ["pynostr>=0.6"]
channel-twilio = ["twilio>=9.0"]
channel-gmail = [
    "google-api-python-client>=2.0",
    "google-auth-oauthlib>=1.0",
    "google-auth-httplib2>=0.2",
]
browser = ["playwright>=1.40"]
media = ["openai>=1.30"]
mining-pearl-vllm = ["docker>=7.0", "httpx>=0.27"]
pdf = ["pdfplumber>=0.10"]
scheduler = ["croniter>=2.0"]
security-signing = ["cryptography>=43"]
sandbox-wasm = ["wasmtime>=25"]
sandbox-docker = ["docker>=7.0"]
dashboard = ["textual>=0.80"]
speech = ["faster-whisper>=1.2.1", "kokoro-onnx>=0.5.0", "ctranslate2>=4.8.0", "onnxruntime>=1.14", "av>=17.1.0", "sounddevice>=0.4.6"]
speech-deepgram = ["deepgram-sdk>=3.0"]
eval-wandb = ["wandb>=0.17"]
eval-sheets = ["gspread>=6.0", "google-auth>=2.0"]
mining-pearl-cpu = [
    # Pearl Python packages (py-pearl-mining, miner-base, pearl-gateway) are
    # not on PyPI yet. They are installed at first `mine init` via the
    # build-from-pin path in src/openjarvis/mining/_install.py:build_from_pin().
    # When Pearl publishes wheels, replace the line below with version pins.
    #
    # The extra remains as a feature-flag namespace so users can run
    # `uv sync --extra mining-pearl-cpu` to opt-in (it succeeds with no
    # additional resolution today; the actual install happens on demand).
]
framework-comparison = ["polars>=1.0"]
docs = [
    "mkdocs>=1.6",
    "mkdocs-material>=9.5",
    "mkdocstrings[python]>=0.25",
    "mkdocs-gen-files>=0.5",
    "mkdocs-literate-nav>=0.6",
]

[project.urls]
Homepage = "https://github.com/open-jarvis/OpenJarvis"
Documentation = "https://open-jarvis.github.io/OpenJarvis/"
Repository = "https://github.com/open-jarvis/OpenJarvis"
Issues = "https://github.com/open-jarvis/OpenJarvis/issues"

[project.scripts]
jarvis = "openjarvis.cli:main"

[tool.hatch.build.targets.wheel]
packages = ["src/openjarvis"]

[tool.hatch.build.targets.wheel.force-include]
"src/openjarvis/agents/claude_code_runner" = "_node_modules/claude_code_runner"
"src/openjarvis/channels/whatsapp_baileys_bridge" = "_node_modules/whatsapp_baileys_bridge"
"scripts/install" = "_install_scripts"

[tool.pytest.ini_options]
testpaths = ["tests"]
markers = [
    "amd: requires AMD GPU",
    "apple: requires Apple Silicon",
    "cloud: requires cloud API keys",
    "docker: requires a working Docker daemon (no GPU required)",
    "live: requires running inference engine",
    "macos15: requires macOS 15+ (Sequoia) for Apple FM",
    "live_channel: requires real channel credentials (env vars)",
    "nvidia: requires NVIDIA GPU",
    "slow: long-running test",
    "live_external: requires HERMES_AGENT_PATH and OPENCLAW_PATH; spawns real foreign-framework subprocesses",
]

[tool.ruff]
target-version = "py310"
src = ["src", "tests"]

[tool.ruff.lint]
select = ["E", "F", "I", "W"]

[tool.ruff.lint.per-file-ignores]
"src/openjarvis/evals/datasets/*.py" = ["E501"]
"src/openjarvis/evals/scorers/*.py" = ["E501"]
# hybrid/ is research code with long prompt strings and paradigm-specific
# config dicts ├óΓé¼ΓÇ¥ same relaxation as evals research code above.
"src/openjarvis/agents/hybrid/*.py" = ["E501"]
# research_loop.py carries the multi-paragraph planner system prompt as
# inline string literals; line-length wrapping would harm readability of
# the prompt itself.
"src/openjarvis/agents/research_loop.py" = ["E501"]

[dependency-groups]
dev = [
    "maturin>=1.12.6",
]


## ===== pyproject.toml : STAGE 3 =====
[build-system]
requires = ["hatchling", "hatch-vcs"]
build-backend = "hatchling.build"

[project]
name = "OpenJarvis"
dynamic = ["version"]
description = "OpenJarvis ΓÇö modular AI assistant backend with composable intelligence primitives"
readme = "README.md"
# Upper bound: numpy 2.2.x (pinned transitively via datasets/pandas) ships no
# cp314 Windows wheel, so under Python 3.14 uv would compile numpy from source
# (Meson) and fail on Windows boxes without a C toolchain (#350). Cap to the
# range that has prebuilt wheels; matches the classifiers (3.10ΓÇô3.13).
requires-python = ">=3.10,<3.14"
license = {text = "Apache-2.0"}
authors = [
    {name = "Open Jarvis Contributors"},
]
classifiers = [
    "Development Status :: 3 - Alpha",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: Apache Software License",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
    "Programming Language :: Python :: 3.13",
    "Topic :: Scientific/Engineering :: Artificial Intelligence",
]
dependencies = [
    "click>=8",
    "croniter>=2.0",
    "datasets>=4.5.0",
    "ddgs>=9.11.4",
    "httpx>=0.27",
    "openai>=1.30",
    "nvidia-ml-py>=12.560.30",
    "posthog>=3.0",
    "python-telegram-bot>=22.8",
    "rich>=13",
    "tomli>=2.0; python_version < '3.11'",
    "tomlkit>=0.12",
    "websockets>=15.0.1",
]

[project.optional-dependencies]
dev = [
    "maturin>=1.12.6",
    "pytest>=8",
    "pytest-asyncio>=0.24",
    "pytest-cov>=5",
    "pytest-xdist>=3",
    "respx>=0.22",
    "ruff>=0.4",
    "pre-commit>=3.0",
]
inference-mlx = ["mlx-lm>=0.31.1; sys_platform == 'darwin'"]
inference-vllm = ["vllm>=0.16.0"]
inference-cloud = [
    "openai>=1.30",
    "anthropic>=0.30",
]
inference-google = [
    "google-genai>=1.0",
]
# Exact security pin covering the LiteLLM command-injection advisories.
# Avoid 1.82.7/1.82.8, which were affected by the March supply-chain incident.
inference-litellm = ["litellm==1.100.1"]
inference-gemma = ["pygemma>=0.1.3"]
tools-search = [
    "tavily-python>=0.3",
    "ddgs>=9.11.4",
]
memory-faiss = [
    "faiss-cpu>=1.7",
    "sentence-transformers>=2.2",
    "numpy>=1.24",
]
memory-colbert = [
    "colbert-ai>=0.2",
    "torch>=2.0",
]
memory-pdf = ["pdfplumber>=0.10"]
memory-bm25 = ["rank-bm25>=0.2.2"]
server = [
    "fastapi>=0.110",
    "uvicorn>=0.30",
    "pydantic>=2.0",
    "python-multipart>=0.0.9",
]
desktop = [
    "fastapi>=0.110",
    "uvicorn>=0.30",
    "pydantic>=2.0",
    "python-multipart>=0.0.9",
    "faster-whisper>=1.0",
    # 1.24.x declares Python 3.10 support but publishes no cp310 wheels (#917).
    "onnxruntime<1.24; python_version < '3.11'",
    "numpy>=1.24",
    "sounddevice>=0.5",
    "soundfile>=0.12",
]
# Local neural TTS. Kokoro pulls spacy/misaki for G2P; espeak-ng must also be
# present on PATH (brew install espeak-ng) for out-of-dictionary words.
voice = [
    "kokoro>=0.9",
    "soundfile>=0.12",
    "sounddevice>=0.5",  # play_wav / record_until_silence in speech/voice_io.py
    "numpy>=1.24",
]
openhands = ["openhands-sdk>=1.0; python_version >= '3.12'"]
# Apple Foundation Models (on-device AFM 3). Needs an Apple Silicon Mac on
# macOS 26+ with Apple Intelligence enabled. The SDK compiles Swift bindings
# at install time, so a full Xcode is required -- Command Line Tools alone
# fail:
#   DEVELOPER_DIR=/Applications/Xcode.app/Contents/Developer \
#       uv pip install -e '.[afm]'
# 0.2.1 is the floor: it added SystemLanguageModel.context_size and
# token_count, which the engine uses for token accounting.
afm = ["apple-fm-sdk>=0.2.1; sys_platform == 'darwin'"]
gpu-metrics = ["pynvml>=12.0"]
energy-amd = ["amdsmi>=6.1"]
# `zeus-ml[apple]` was the previous spelling and never worked: zeus-ml has no
# `apple` extra, and its `zeus.device.soc` package (which wraps this library)
# landed on master after the last zeus release, so no published zeus-ml
# contains it. Depend on the underlying IOReport extension directly.
energy-apple = ["zeus-apple-silicon>=1.1.0; sys_platform == 'darwin'"]
energy-all = [
    "pynvml>=12.0",
    "amdsmi>=6.1",
    "zeus-apple-silicon>=1.1.0; sys_platform == 'darwin'",
]
orchestrator-training = ["torch>=2.0", "transformers>=4.40"]
learning-dspy = ["dspy>=2.6"]
learning-gepa = ["gepa>=0.1"]
channel-telegram = ["python-telegram-bot>=21.0"]
channel-discord = ["discord.py>=2.3"]
channel-slack = ["slack-sdk>=3.27"]
channel-line = ["line-bot-sdk>=3.0"]
channel-viber = ["viberbot>=1.0"]
channel-messenger = ["pymessenger>=0.0.7"]
channel-reddit = ["praw>=7.0"]
channel-mastodon = ["Mastodon.py>=1.8"]
channel-xmpp = ["slixmpp>=1.8"]
channel-rocketchat = ["rocketchat-API>=1.30"]
channel-zulip = ["zulip>=0.9"]
channel-twitter = ["httpx>=0.27"]
channel-twitch = ["twitchio>=2.6"]
channel-nostr = ["pynostr>=0.6"]
channel-twilio = ["twilio>=9.0"]
channel-gmail = [
    "google-api-python-client>=2.0",
    "google-auth-oauthlib>=1.0",
    "google-auth-httplib2>=0.2",
]
browser = ["playwright>=1.40"]
media = ["openai>=1.30"]
mining-pearl-vllm = ["docker>=7.0", "httpx>=0.27"]
pdf = ["pdfplumber>=0.10"]
# Kept as a compatibility extra for existing install commands. Cron support is
# a core scheduler contract now, so croniter is also installed unconditionally.
scheduler = ["croniter>=2.0"]
security-signing = ["cryptography>=43"]
sandbox-wasm = ["wasmtime>=25"]
sandbox-docker = ["docker>=7.0"]
dashboard = ["textual>=0.80"]
speech = [
    "faster-whisper>=1.0",
    # Keep the pip-visible speech extra installable on supported Python 3.10.
    "onnxruntime<1.24; python_version < '3.11'",
    "numpy>=1.24",
    "sounddevice>=0.5",
    "soundfile>=0.12",
]
speech-deepgram = ["deepgram-sdk>=3.0"]
eval-wandb = ["wandb>=0.17"]
eval-sheets = ["gspread>=6.0", "google-auth>=2.0"]
mining-pearl-cpu = [
    # Pearl Python packages (py-pearl-mining, miner-base, pearl-gateway) are
    # not on PyPI yet. They are installed at first `mine init` via the
    # build-from-pin path in src/openjarvis/mining/_install.py:build_from_pin().
    # When Pearl publishes wheels, replace the line below with version pins.
    #
    # The extra remains as a feature-flag namespace so users can run
    # `uv sync --extra mining-pearl-cpu` to opt-in (it succeeds with no
    # additional resolution today; the actual install happens on demand).
]
framework-comparison = ["polars>=1.0"]
docs = [
    "mkdocs>=1.6",
    "mkdocs-material>=9.5",
    "mkdocstrings[python]>=0.25",
    "mkdocs-gen-files>=0.5",
    "mkdocs-literate-nav>=0.6",
]

[project.urls]
Homepage = "https://github.com/open-jarvis/OpenJarvis"
Documentation = "https://open-jarvis.github.io/OpenJarvis/"
Repository = "https://github.com/open-jarvis/OpenJarvis"
Issues = "https://github.com/open-jarvis/OpenJarvis/issues"

[project.scripts]
jarvis = "openjarvis.cli:main"
openjarvis-eval = "openjarvis.evals.cli:main"

# Version is derived from git tags by hatch-vcs (see #526). For source/editable
# checkouts this yields the true `git describe` version (e.g. 1.0.3.dev109+g<sha>)
# rather than a stale static string. CI release builds override this with
# SETUPTOOLS_SCM_PRETEND_VERSION so the published version equals the pushed tag.
#
# setuptools_scm cannot bump custom `.devN` tags (only `.dev0`), so the autotag
# `vX.Y.Z.devN` tags are deliberately EXCLUDED from version derivation here; the
# base is taken from the latest plain release tag (vX.Y.Z) and the dev distance
# is computed from commit count since that release.
[tool.hatch.version]
source = "vcs"

[tool.hatch.version.raw-options]
tag_regex = '^v(?P<version>[0-9]+\.[0-9]+\.[0-9]+)$'
git_describe_command = [
    "git", "describe", "--dirty", "--tags", "--long",
    "--match", "v[0-9]*", "--exclude", "*dev*", "--exclude", "*rc*", "--exclude", "desktop-*",
]
# Builds without a git checkout (e.g. the `COPY src/ src/` Docker stages, which
# never include .git) can't run `git describe`. Without a fallback that would
# hard-fail the build. Mirror the runtime sentinel in src/openjarvis/__init__.py.
# Such builds can inject the real version via SETUPTOOLS_SCM_PRETEND_VERSION.
fallback_version = "0.0.0+unknown"

[tool.uv.sources]
openjarvis-rust = { path = "rust/crates/openjarvis-python" }

[tool.hatch.build.targets.sdist]
# Tauri release bundles carry these executables; Python source distributions
# must not duplicate platform binaries on every PyPI release.
exclude = [
    "/desktop/src-tauri/binaries",
    "/frontend/src-tauri/binaries",
]
# The publishing workflow builds this UI before packaging. Keep its generated
# files even though the directory is intentionally ignored by Git.
artifacts = ["/src/openjarvis/server/static/**"]

[tool.hatch.build.targets.wheel]
packages = ["src/openjarvis"]
artifacts = ["/src/openjarvis/server/static/**"]
exclude = [
    "/src/openjarvis/agents/claude_code_runner",
]

[tool.hatch.build.targets.wheel.force-include]
"src/openjarvis/agents/claude_code_runner/index.mjs" = "_node_modules/claude_code_runner/index.mjs"
"src/openjarvis/agents/claude_code_runner/package.json" = "_node_modules/claude_code_runner/package.json"
"src/openjarvis/channels/whatsapp_baileys_bridge" = "_node_modules/whatsapp_baileys_bridge"
"scripts/install" = "_install_scripts"
"deploy/windows" = "_deploy/windows"

[tool.pytest.ini_options]
testpaths = ["tests"]
markers = [
    "amd: requires AMD GPU",
    "apple: requires Apple Silicon",
    "cloud: requires cloud API keys",
    "docker: requires a working Docker daemon (no GPU required)",
    "live: requires running inference engine",
    "macos15: requires macOS 15+ (Sequoia) for Apple FM",
    "live_channel: requires real channel credentials (env vars)",
    "nvidia: requires NVIDIA GPU",
    "slow: long-running test",
    "hub: downloads real datasets from the HuggingFace Hub at runtime; excluded from the default CI lane (run with -m hub)",
    "live_external: requires HERMES_AGENT_PATH and OPENCLAW_PATH; spawns real foreign-framework subprocesses",
    "modal: requires Modal token + network; runs real swebench harness on Modal",
]

[tool.ruff]
target-version = "py310"
src = ["src", "tests"]

[tool.ruff.lint]
select = ["E", "F", "I", "W"]

[tool.ruff.lint.per-file-ignores]
"src/openjarvis/evals/datasets/*.py" = ["E501"]
"src/openjarvis/evals/scorers/*.py" = ["E501"]
# hybrid/ is research code with long prompt strings and paradigm-specific
# config dicts ΓÇö same relaxation as evals research code above. The ``**`` glob
# also covers subpackages (e.g. hybrid/skillorchestra/), which the prior
# ``hybrid/*.py`` glob missed.
"src/openjarvis/agents/hybrid/**/*.py" = ["E501"]
# research_loop.py carries long prompt strings too (documented in CLAUDE.md);
# the ignore was missing here.
"src/openjarvis/agents/research_loop.py" = ["E501"]

[dependency-groups]
dev = [
    "maturin>=1.12.6",
]
# openjarvis_rust is the native PyO3 extension, built from the local Rust
# workspace. It lives in a uv dependency group (PEP 735) ΓÇö not the published
# `desktop` extra ΓÇö so `uv sync --group desktop-native` builds it from source
# for the desktop app, while `pip install openjarvis[desktop]` from PyPI does
# NOT try to resolve openjarvis-rust from PyPI, where it isn't published
# (dependency groups are excluded from wheel metadata). See #584 / #615.
desktop-native = [
    "openjarvis-rust",
]

## ===== src/openjarvis/core/config.py : OUR COMMITS SINCE AUTHOR BASE =====
a0704c4c W79: openjarvis-engine-disable-v1 (Graystone D-16). [engine] disabled comma list; _discovery._make_engine raises EngineDisabled for listed keys - single choke point for doctor, discover_engines, get_engine, quickstart. Closes the fallback self-loop: vllm/uzu/lemonade defaults target the OpenJarvis server's own port (author 8000; e0e3652 moved them to 8010 with the server). Proven: harness w79_disable_check PASS; doctor with config shows 4 disabled, ollama reachable; w79_fallback_check PASS - outage returns None, control without list fell back to lemonade at localhost:8010; live server 10:47 restart serves chat on 172.16.33.200:11434, no self-connection. Not proven live: outage behavior on the running server. config.toml entry (vllm,uzu,lemonade,litellm) is out of git.
829cea7a W78 openjarvis-file-confine-v1: confine file_write to [tools] file_allowed_dirs (default ~/.openjarvis/workspace) in serve.py chat+channel builders and cli/ask.py _build_tools; author never passed allowed_dirs so file_write could write anywhere (D-06). Verified: SDK in/out write test PASS, server banner allowed_dirs line 17:41. Channel builder compile-verified only (channel disabled).
0389255b TTS: AudioContext playback engine + ChatArea driver rewrite; mailbox IMAP connector and tools; speech/CSP fixes
e0e36523 Fix: wire tools to native_openhands agent - file_read, think, calculator, code_interpreter, shell_exec, file_write now loading at startup

## ===== src/openjarvis/core/config.py : CONFLICTED WORKING FILE (markers) =====
"""Configuration loading, hardware detection, and engine recommendation.

User configuration lives at ``~/.openjarvis/config.toml``.  ``load_config()``
detects hardware, fills sensible defaults, then overlays any user overrides
found in the TOML file.
"""

from __future__ import annotations

import functools
import os
import platform
import shutil
import subprocess
from dataclasses import dataclass, field, is_dataclass
from pathlib import Path
from typing import (
    TYPE_CHECKING,
    Any,
    Dict,
    List,
    Optional,
    get_args,
    get_origin,
    get_type_hints,
)

from openjarvis.core.paths import (
    ConfigurationError,
    get_cache_dir,
    get_config_dir,
    get_config_path,
    get_data_dir,
)

if TYPE_CHECKING:
    # Only used by type-checkers (mypy/pyright) for the ``JarvisConfig.mining``
    # field annotation. The runtime import is deferred inside
    # ``_parse_mining_section()`` to break the import cycle:
    # ``mining/_stubs.py`` imports ``HardwareInfo`` from this module at its
    # top level.
    from openjarvis.mining._stubs import MiningConfig

try:
    import tomllib  # Python 3.11+
except ModuleNotFoundError:
    import tomli as tomllib  # type: ignore[no-redef]

# ---------------------------------------------------------------------------
# Hardware dataclasses
# ---------------------------------------------------------------------------

# Legacy names, kept for the ~45 modules that import them. They are resolved
# once at import via the env-aware resolver in ``openjarvis.core.paths`` (the
# install-script model: ``OPENJARVIS_HOME`` / ``XDG_DATA_HOME`` are set before
# the process starts). They are real module attributes â€” not computed lazily â€”
# so existing tests can ``monkeypatch.setattr`` them and so dataclass-instance
# defaults stay consistent. Code that must react to a mid-process env change
# (or wants the override regardless of import order) should call
# ``get_config_dir()`` / ``get_config_path()`` directly; the dataclass field
# defaults below already do this via ``default_factory``.
DEFAULT_CONFIG_DIR = get_config_dir()
DEFAULT_CONFIG_PATH = get_config_path()


def _ensure_config_dir() -> Path:
    """Ensure the config directory exists with restrictive permissions."""
    from openjarvis.security.file_utils import secure_mkdir

    return secure_mkdir(get_config_dir())


@dataclass(slots=True)
class GpuInfo:
    """Detected GPU metadata."""

    vendor: str = ""
    name: str = ""
    vram_gb: float = 0.0
    compute_capability: str = ""
    count: int = 0


@dataclass(slots=True)
class HardwareInfo:
    """Detected system hardware."""

    platform: str = ""
    cpu_brand: str = ""
    cpu_count: int = 0
    ram_gb: float = 0.0
    gpu: Optional[GpuInfo] = None


# ---------------------------------------------------------------------------
# Hardware detection helpers
# ---------------------------------------------------------------------------


def _run_cmd(cmd: list[str]) -> str:
    """Run a command and return stripped stdout, or empty string on failure."""
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=10,  # noqa: S603
        )
        return result.stdout.strip()
    except (FileNotFoundError, subprocess.TimeoutExpired, OSError):
        return ""


def _detect_nvidia_gpu() -> Optional[GpuInfo]:
    if not shutil.which("nvidia-smi"):
        return None
    raw = _run_cmd(
        [
            "nvidia-smi",
            "--query-gpu=name,memory.total,count,compute_cap",
            "--format=csv,noheader,nounits",
        ]
    )
    if not raw:
        return None
    try:
        first_line = raw.splitlines()[0]
        parts = [p.strip() for p in first_line.split(",")]
        name = parts[0]
        vram_mb = float(parts[1])
        count = int(parts[2])
        compute_capability = parts[3] if len(parts) > 3 else ""
        return GpuInfo(
            vendor="nvidia",
            name=name,
            vram_gb=round(vram_mb / 1024, 1),
            compute_capability=compute_capability,
            count=count,
        )
    except (IndexError, ValueError):
        return None


def _detect_amd_gpu() -> Optional[GpuInfo]:
    if not shutil.which("rocm-smi"):
        return None
    raw = _run_cmd(["rocm-smi", "--showproductname"])
    if not raw:
        return None
    name = raw.splitlines()[0] if raw else "AMD GPU"

    # Parse VRAM from rocm-smi --showmeminfo vram
    vram_gb = 0.0
    try:
        vram_raw = _run_cmd(["rocm-smi", "--showmeminfo", "vram"])
        for line in vram_raw.splitlines():
            if "Total Memory (B):" in line:
                vram_bytes = int(line.split(":")[-1].strip())
                vram_gb = round(vram_bytes / (1024**3), 1)
                break
    except (ValueError, IndexError):
        vram_gb = 0.0

    # Parse GPU count from rocm-smi --showallinfo
    count = 1
    try:
        allinfo_raw = _run_cmd(["rocm-smi", "--showallinfo"])
        import re

        gpu_ids = set(re.findall(r"GPU\[(\d+)\]", allinfo_raw))
        if gpu_ids:
            count = len(gpu_ids)
    except (ValueError, IndexError):
        count = 1

    return GpuInfo(vendor="amd", name=name, vram_gb=vram_gb, count=count)


def _detect_apple_gpu() -> Optional[GpuInfo]:
    if platform.system() != "Darwin":
        return None
    raw = _run_cmd(["system_profiler", "SPDisplaysDataType"])
    if "Apple" not in raw:
        return None
    # Rough extraction â€” "Apple M2 Max" etc.
    ram_gb = _total_ram_gb()
    for line in raw.splitlines():
        line = line.strip()
        if "Chipset Model" in line:
            name = line.split(":")[-1].strip()
            return GpuInfo(vendor="apple", name=name, vram_gb=ram_gb, count=1)
    return GpuInfo(vendor="apple", name="Apple Silicon", vram_gb=ram_gb, count=1)


def _detect_cpu_brand() -> str:
    """Best-effort CPU brand string."""
    if platform.system() == "Darwin":
        brand = _run_cmd(["sysctl", "-n", "machdep.cpu.brand_string"])
        if brand:
            return brand
    cpuinfo = Path("/proc/cpuinfo")
    if cpuinfo.exists():
        try:
            for line in cpuinfo.read_text().splitlines():
                if line.startswith("model name"):
                    return line.split(":", 1)[1].strip()
        except OSError:
            pass
    return platform.processor() or "unknown"


def _total_ram_gb() -> float:
    try:
        if platform.system() == "Darwin":
            raw = _run_cmd(["sysctl", "-n", "hw.memsize"])
            return round(int(raw) / (1024**3), 1) if raw else 0.0
        if platform.system() == "Windows":
            import ctypes

            class _MemoryStatusEx(ctypes.Structure):
                _fields_ = [
                    ("dwLength", ctypes.c_ulong),
                    ("dwMemoryLoad", ctypes.c_ulong),
                    ("ullTotalPhys", ctypes.c_ulonglong),
                    ("ullAvailPhys", ctypes.c_ulonglong),
                    ("ullTotalPageFile", ctypes.c_ulonglong),
                    ("ullAvailPageFile", ctypes.c_ulonglong),
                    ("ullTotalVirtual", ctypes.c_ulonglong),
                    ("ullAvailVirtual", ctypes.c_ulonglong),
                    ("sullAvailExtendedVirtual", ctypes.c_ulonglong),
                ]

            stat = _MemoryStatusEx()
            stat.dwLength = ctypes.sizeof(_MemoryStatusEx)
            if ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(stat)):
                return round(stat.ullTotalPhys / (1024**3), 1)
            return 0.0
        meminfo = Path("/proc/meminfo")
        if meminfo.exists():
            for line in meminfo.read_text().splitlines():
                if line.startswith("MemTotal"):
                    kb = int(line.split()[1])
                    return round(kb / (1024**2), 1)
    except (OSError, ValueError, AttributeError):
        pass
    return 0.0


def detect_hardware() -> HardwareInfo:
    """Auto-detect hardware capabilities with graceful fallbacks."""
    gpu = _detect_nvidia_gpu() or _detect_amd_gpu() or _detect_apple_gpu()
    return HardwareInfo(
        platform=platform.system().lower(),
        cpu_brand=_detect_cpu_brand(),
        cpu_count=os.cpu_count() or 1,
        ram_gb=_total_ram_gb(),
        gpu=gpu,
    )


# ---------------------------------------------------------------------------
# Engine recommendation
# ---------------------------------------------------------------------------


def recommend_engine(hw: HardwareInfo) -> str:
    """Suggest the best inference engine for the detected hardware."""
    gpu = hw.gpu
    if gpu is None:
        return "llamacpp"
    if gpu.vendor == "apple":
        return "mlx"
    if gpu.vendor == "nvidia":
        # Datacenter cards (A100, H100, L40, etc.) â†’ vllm; consumer â†’ ollama
        datacenter_keywords = ("A100", "H100", "H200", "L40", "A10", "A30")
        if any(kw in gpu.name for kw in datacenter_keywords):
            return "vllm"
        return "ollama"
    if gpu.vendor == "amd":
        # Datacenter cards (MI300, MI325, MI350, MI355) â†’ vllm; consumer â†’ lemonade
        amd_datacenter_keywords = ("MI300", "MI325", "MI350", "MI355")
        if any(kw in gpu.name for kw in amd_datacenter_keywords):
            return "vllm"
        return "lemonade"
    return "llamacpp"


def _available_memory_gb(hw: HardwareInfo) -> float:
    """Return usable memory in GB for model loading."""
    gpu = hw.gpu
    if gpu and gpu.vram_gb > 0:
        return gpu.vram_gb * max(gpu.count, 1) * 0.9
    if hw.ram_gb > 0:
        return (hw.ram_gb - 4) * 0.8
    return 0.0


# Explicit tier table: (max_ram_gb, model_id).
# Walked in order â€” first tier where available_gb <= max_ram is chosen.
# Uses Qwen3.5 MoE models â€” better quality per GB than dense models since
# only a fraction of parameters are active per token.
_MODEL_TIERS = [
    (8, "qwen3.5:2b"),
    (16, "qwen3.5:4b"),
    (32, "qwen3.5:9b"),
    (64, "qwen2.5-coder:32b"),
]
<<<<<<< HEAD
_MODEL_TIER_FALLBACK = "qwen3.5:9b"
=======
_MODEL_TIER_FALLBACK = "qwen3.5:27b"
_LEMONADE_DEFAULT_MODEL = "Qwen3.6-35B-A3B-GGUF"
>>>>>>> a6dcf846


def recommend_model(hw: HardwareInfo, engine: str) -> str:
    """Suggest a default model for the selected engine and hardware.

    For Lemonade, prefer the validated Qwen3.6 35B A3B GGUF default.
    For other local engines, use the generic Qwen3.5 tier mapping.
    """
    from openjarvis.intelligence.model_catalog import BUILTIN_MODELS

    available_gb = _available_memory_gb(hw)
    if available_gb <= 0:
        return ""

    if engine == "lemonade":
        return _LEMONADE_DEFAULT_MODEL

    # Build a lookup for quick engine-compatibility checks
    catalog = {spec.model_id: spec for spec in BUILTIN_MODELS}

    # Try explicit tier mapping first
    model_id = _MODEL_TIER_FALLBACK
    for max_ram, tier_model in _MODEL_TIERS:
        if available_gb <= max_ram:
            model_id = tier_model
            break

    spec = catalog.get(model_id)
    if spec and engine in spec.supported_engines:
        return model_id

    # Fallback: scan all Qwen3.5 models for engine compatibility
    candidates = [
        s
        for s in BUILTIN_MODELS
        if s.provider == "alibaba"
        and s.model_id.startswith("qwen3.5:")
        and engine in s.supported_engines
    ]
    candidates.sort(key=lambda s: s.parameter_count_b, reverse=True)
    for s in candidates:
        estimated_gb = s.parameter_count_b * 0.5 * 1.1
        if estimated_gb <= available_gb:
            return s.model_id

    return ""


def estimated_download_gb(parameter_count_b: float) -> float:
    """Estimate download size in GB for Q4_K_M quantized model."""
    return parameter_count_b * 0.5 * 1.1


# ---------------------------------------------------------------------------
# Configuration hierarchy
# ---------------------------------------------------------------------------


@dataclass(slots=True)
class OllamaEngineConfig:
    """Per-engine config for Ollama."""

    host: str = ""


@dataclass(slots=True)
class VLLMEngineConfig:
    """Per-engine config for vLLM."""

    host: str = "http://localhost:8010"


@dataclass(slots=True)
class SGLangEngineConfig:
    """Per-engine config for SGLang."""

    host: str = "http://localhost:30000"


@dataclass(slots=True)
class LlamaCppEngineConfig:
    """Per-engine config for llama.cpp."""

    host: str = "http://localhost:8080"
    binary_path: str = ""


@dataclass(slots=True)
class MLXEngineConfig:
    """Per-engine config for MLX."""

    host: str = "http://localhost:8080"


@dataclass(slots=True)
class LMStudioEngineConfig:
    """Per-engine config for LM Studio."""

    host: str = "http://localhost:1234"


@dataclass(slots=True)
class ExoEngineConfig:
    """Per-engine config for Exo."""

    host: str = "http://localhost:52415"


@dataclass(slots=True)
class NexaEngineConfig:
    """Per-engine config for Nexa."""

    host: str = "http://localhost:18181"
    device: str = ""


@dataclass(slots=True)
class UzuEngineConfig:
    """Per-engine config for Uzu."""

    host: str = "http://localhost:8010"


@dataclass(slots=True)
class AppleFmEngineConfig:
    """Per-engine config for Apple Foundation Models."""

    host: str = "http://localhost:8079"


@dataclass(slots=True)
class GemmaCppEngineConfig:
    """Per-engine config for gemma.cpp."""

    model_path: str = ""
    tokenizer_path: str = ""
    model_type: str = ""
    num_threads: int = 0


@dataclass(slots=True)
class AfmEngineConfig:
    """Per-engine config for in-process Apple Foundation Models.

    No ``host``: this engine runs the SDK in-process rather than talking to a
    server. (The separate ``apple_fm`` engine does have a host â€” it speaks to
    the FastAPI shim.)
    """

    # Standing instructions applied to every session, on top of any system
    # message in the request.
    instructions: str = ""
    # "general" or "content_tagging".
    use_case: str = "general"
    # "default" or "permissive_content_transformations".
    guardrails: str = "default"
    # "greedy" (reproducible, the default here) or "random" (the SDK default).
    sampling: str = "greedy"


@dataclass(slots=True)
class LemonadeEngineConfig:
    """Per-engine config for Lemonade."""

<<<<<<< HEAD
    host: str = "http://localhost:8010"
=======
    host: str = "http://localhost:13305"
>>>>>>> a6dcf846


@dataclass
class EngineConfig:
    """Inference engine settings with nested per-engine configs."""

    default: str = "ollama"
    # openjarvis-engine-disable-v1 (Graystone D-16): comma-separated engine keys that are
    # never constructed or probed. The author ships no engine off-switch.
    disabled: str = ""
    ollama: OllamaEngineConfig = field(default_factory=OllamaEngineConfig)
    vllm: VLLMEngineConfig = field(default_factory=VLLMEngineConfig)
    sglang: SGLangEngineConfig = field(default_factory=SGLangEngineConfig)
    llamacpp: LlamaCppEngineConfig = field(default_factory=LlamaCppEngineConfig)
    mlx: MLXEngineConfig = field(default_factory=MLXEngineConfig)
    lmstudio: LMStudioEngineConfig = field(default_factory=LMStudioEngineConfig)
    exo: ExoEngineConfig = field(default_factory=ExoEngineConfig)
    nexa: NexaEngineConfig = field(default_factory=NexaEngineConfig)
    uzu: UzuEngineConfig = field(default_factory=UzuEngineConfig)
    apple_fm: AppleFmEngineConfig = field(default_factory=AppleFmEngineConfig)
    afm: AfmEngineConfig = field(default_factory=AfmEngineConfig)
    gemma_cpp: GemmaCppEngineConfig = field(default_factory=GemmaCppEngineConfig)
    lemonade: LemonadeEngineConfig = field(default_factory=LemonadeEngineConfig)

    # Backward-compat properties for old flat attribute names
    @property
    def ollama_host(self) -> str:
        """Deprecated: use ``engine.ollama.host``."""
        return self.ollama.host

    @ollama_host.setter
    def ollama_host(self, value: str) -> None:
        self.ollama.host = value

    @property
    def vllm_host(self) -> str:
        """Deprecated: use ``engine.vllm.host``."""
        return self.vllm.host

    @vllm_host.setter
    def vllm_host(self, value: str) -> None:
        self.vllm.host = value

    @property
    def llamacpp_host(self) -> str:
        """Deprecated: use ``engine.llamacpp.host``."""
        return self.llamacpp.host

    @llamacpp_host.setter
    def llamacpp_host(self, value: str) -> None:
        self.llamacpp.host = value

    @property
    def llamacpp_path(self) -> str:
        """Deprecated: use ``engine.llamacpp.binary_path``."""
        return self.llamacpp.binary_path

    @llamacpp_path.setter
    def llamacpp_path(self, value: str) -> None:
        self.llamacpp.binary_path = value

    @property
    def sglang_host(self) -> str:
        """Deprecated: use ``engine.sglang.host``."""
        return self.sglang.host

    @sglang_host.setter
    def sglang_host(self, value: str) -> None:
        self.sglang.host = value

    @property
    def mlx_host(self) -> str:
        """Deprecated: use ``engine.mlx.host``."""
        return self.mlx.host

    @mlx_host.setter
    def mlx_host(self, value: str) -> None:
        self.mlx.host = value

    @property
    def lmstudio_host(self) -> str:
        """Deprecated: use ``engine.lmstudio.host``."""
        return self.lmstudio.host

    @lmstudio_host.setter
    def lmstudio_host(self, value: str) -> None:
        self.lmstudio.host = value

    @property
    def exo_host(self) -> str:
        """Deprecated: use ``engine.exo.host``."""
        return self.exo.host

    @exo_host.setter
    def exo_host(self, value: str) -> None:
        self.exo.host = value

    @property
    def nexa_host(self) -> str:
        """Deprecated: use ``engine.nexa.host``."""
        return self.nexa.host

    @nexa_host.setter
    def nexa_host(self, value: str) -> None:
        self.nexa.host = value

    @property
    def uzu_host(self) -> str:
        """Deprecated: use ``engine.uzu.host``."""
        return self.uzu.host

    @uzu_host.setter
    def uzu_host(self, value: str) -> None:
        self.uzu.host = value

    @property
    def apple_fm_host(self) -> str:
        """Deprecated: use ``engine.apple_fm.host``."""
        return self.apple_fm.host

    @apple_fm_host.setter
    def apple_fm_host(self, value: str) -> None:
        self.apple_fm.host = value

    @property
    def lemonade_host(self) -> str:
        """Deprecated: use ``engine.lemonade.host``."""
        return self.lemonade.host

    @lemonade_host.setter
    def lemonade_host(self, value: str) -> None:
        self.lemonade.host = value


@dataclass(slots=True)
class IntelligenceConfig:
    """The model â€” identity, paths, quantization, and generation defaults."""

    default_model: str = ""
    # Optional per-CLI preset (used when ``-m`` omitted or ``-m smart``).
    model_chat: str = ""
    model_short: str = ""
    model_long: str = ""
    model_code: str = ""
    fallback_model: str = ""
    model_path: str = ""  # Local weights (HF repo, GGUF file, etc.)
    checkpoint_path: str = ""  # Checkpoint/adapter path
    quantization: str = "none"  # none, fp8, int8, int4, gguf_q4, gguf_q8
    preferred_engine: str = ""  # Override engine for this model (e.g., "vllm")
    provider: str = ""  # local, openai, anthropic, google
    # Generation defaults (overridable per-call)
    temperature: float = 0.7
    max_tokens: int = 1024
    top_p: float = 0.9
    top_k: int = 40
    repetition_penalty: float = 1.0
    stop_sequences: str = ""  # Comma-separated stop strings


@dataclass(slots=True)
class DeepResearchConfig:
    """Planner settings for the web Deep Research endpoint."""

    engine: str = ""  # Empty means use the active chat engine.
    model: str = ""  # Empty means use the active chat model.


@dataclass(slots=True)
class RoutingLearningConfig:
    """Routing sub-policy config within Learning."""

    policy: str = "heuristic"  # heuristic | learned
    min_samples: int = 5  # Min traces before trusting learned routing


@dataclass(slots=True)
class SFTConfig:
    """General-purpose SFT training config. Maps to [learning.intelligence.sft]."""

    model_name: str = "Qwen/Qwen3-1.7B"
    max_seq_length: int = 4096
    num_epochs: int = 3
    batch_size: int = 8
    learning_rate: float = 2e-5
    weight_decay: float = 0.01
    warmup_ratio: float = 0.1
    max_grad_norm: float = 1.0
    gradient_checkpointing: bool = True
    use_lora: bool = True
    lora_rank: int = 16
    lora_alpha: int = 32
    lora_dropout: float = 0.05
    target_modules: str = "q_proj,v_proj"  # comma-separated for TOML compat
    use_4bit: bool = False
    checkpoint_dir: str = "checkpoints/sft"
    min_pairs: int = 10
    agent_filter: str = ""


@dataclass(slots=True)
class GRPOConfig:
    """General-purpose GRPO training config. Maps to [learning.intelligence.grpo]."""

    model_name: str = "Qwen/Qwen3-1.7B"
    max_seq_length: int = 4096
    max_response_length: int = 2048
    num_epochs: int = 10
    batch_size: int = 16
    learning_rate: float = 1e-6
    max_grad_norm: float = 1.0
    gradient_checkpointing: bool = True
    num_samples_per_prompt: int = 8
    temperature: float = 1.0
    kl_coef: float = 0.0001
    clip_ratio: float = 0.2
    use_8bit_ref: bool = True
    checkpoint_dir: str = "checkpoints/grpo"
    save_every_n_epochs: int = 1
    keep_last_n: int = 3
    min_prompts: int = 10
    agent_filter: str = ""


@dataclass(slots=True)
class DSPyOptimizerConfig:
    """DSPy agent optimizer config. Maps to [learning.agent.dspy]."""

    optimizer: str = "BootstrapFewShotWithRandomSearch"
    task_lm: str = ""
    teacher_lm: str = ""
    max_bootstrapped_demos: int = 4
    max_labeled_demos: int = 4
    num_candidate_programs: int = 10
    max_rounds: int = 1
    optimize_system_prompt: bool = True
    optimize_few_shot: bool = True
    optimize_tool_descriptions: bool = True
    min_traces: int = 20
    metric_threshold: float = 0.7
    agent_filter: str = ""
    config_dir: str = ""


@dataclass(slots=True)
class GEPAOptimizerConfig:
    """GEPA agent optimizer config. Maps to [learning.agent.gepa]."""

    reflection_lm: str = ""
    max_metric_calls: int = 150
    population_size: int = 10
    optimize_system_prompt: bool = True
    optimize_tools: bool = True
    optimize_max_turns: bool = True
    optimize_temperature: bool = True
    min_traces: int = 20
    assessment_batch_size: int = 10
    agent_filter: str = ""
    config_dir: str = ""


@dataclass(slots=True)
class ACEOptimizerConfig:
    """ACE agent optimizer config. Maps to ``[learning.agent.ace]``.

    ACE (Agentic Context Engineering) evolves a *playbook* â€” annotated
    natural-language strategies that get prepended to the agent's
    context â€” using a Generator / Reflector / Curator triad. Unlike
    DSPy (few-shot bootstrapping) or GEPA (Pareto-evolutionary prompt
    mutation), ACE writes a textual playbook that the agent reads at
    inference time.

    See https://github.com/ace-agent/ace for the upstream reference.
    Install via ``pip install -e openjarvis[learning-ace]`` once the
    optional dep is available (ACE is not on PyPI as of v1.0.1; the
    extra installs from the upstream git repo).
    """

    # Models for ACE's three roles. Empty string = inherit from the
    # intelligence primitive's default cloud model.
    generator_model: str = ""
    reflector_model: str = ""
    curator_model: str = ""

    # Provider passed to ACE (``sambanova`` | ``together`` | ``openai``
    # | ``commonstack``). We default to ``openai`` since that's what
    # most OpenJarvis users have credentials for.
    api_provider: str = "openai"

    # Run parameters. Defaults mirror ACE's offline-mode quickstart.
    num_epochs: int = 1
    max_num_rounds: int = 3
    eval_steps: int = 100
    playbook_token_budget: int = 80_000
    max_tokens: int = 4_096

    # Where ACE writes intermediate playbooks + final_results.json.
    # Empty string defaults to ``~/.openjarvis/learning/ace/<task>/``.
    save_dir: str = ""
    task_name: str = "openjarvis"

    # Standard filter / threshold knobs shared with DSPy / GEPA.
    min_traces: int = 20
    agent_filter: str = ""
    config_dir: str = ""


@dataclass(slots=True)
class IntelligenceLearningConfig:
    """Intelligence sub-policy config within Learning."""

    policy: str = "none"  # none | sft | grpo
    sft: SFTConfig = field(default_factory=SFTConfig)
    grpo: GRPOConfig = field(default_factory=GRPOConfig)


@dataclass(slots=True)
class AgentLearningConfig:
    """Agent sub-policy config within Learning."""

    policy: str = "none"  # none | dspy | gepa | ace
    dspy: DSPyOptimizerConfig = field(default_factory=DSPyOptimizerConfig)
    gepa: GEPAOptimizerConfig = field(default_factory=GEPAOptimizerConfig)
    ace: ACEOptimizerConfig = field(default_factory=ACEOptimizerConfig)


@dataclass(slots=True)
class SkillsLearningConfig:
    """Configuration for the skills learning loop (Plan 2A)."""

    auto_optimize: bool = False  # opt in via config
    optimizer: str = "dspy"  # "dspy" or "gepa"
    min_traces_per_skill: int = 20
    optimization_interval_seconds: int = 86400
    overlay_dir: str = field(
        default_factory=lambda: str(get_config_dir() / "learning" / "skills")
    )


@dataclass(slots=True)
class MetricsConfig:
    """Reward / optimization metric weights."""

    accuracy_weight: float = 0.6
    latency_weight: float = 0.2
    cost_weight: float = 0.1
    efficiency_weight: float = 0.1


@dataclass(slots=True)
class SpecSearchCompositeRewardConfig:
    """Composite reward weights for Intelligence-edit training (paper Eq. 1).

    R(q, y) = alpha * R_acc - beta * E_hat - gamma * L_hat - delta * C_hat
    """

    alpha: float = 0.5
    beta: float = 0.1
    gamma: float = 0.1
    delta: float = 0.3


@dataclass(slots=True)
class SpecSearchLearningConfig:
    """LLM-guided spec search config (paper Â§3.3, Algorithm 1).

    Maps to ``[learning.spec_search]`` and is consumed by
    ``SpecSearchOrchestrator.from_config`` and ``SpecSearchLoop``.
    """

    enabled: bool = False
    teacher_model: str = "claude-opus-4-6"
    teacher_engine: str = "cloud"  # registry key for the cloud engine
    autonomy_mode: str = "tiered"  # auto | tiered | manual

    # Per-session bounds (one diagnose/plan/execute pass)
    min_traces: int = 20
    max_cost_per_session_usd: float = 5.0
    max_tool_calls_per_diagnosis: int = 30

    # Multi-session loop (paper Algorithm 1)
    stagnation_k: int = 5
    max_total_cost_usd: float = 50.0
    stagnation_eps: float = 0.001  # gate-score delta below this counts as no progress

    # Gate (GateOK predicate)
    max_regression: float = 0.01  # paper default: epsilon = 1%
    min_improvement: float = 0.0
    benchmark_subsample_size: int = 50
    benchmark_version: str = "personal_v1"

    # Composite reward (only used when an Intelligence edit triggers training)
    composite_reward: SpecSearchCompositeRewardConfig = field(
        default_factory=SpecSearchCompositeRewardConfig,
    )


@dataclass
class LearningConfig:
    """Learning system settings with per-primitive sub-policies."""

    enabled: bool = False
    update_interval: int = 100
    auto_update: bool = False
    routing: RoutingLearningConfig = field(default_factory=RoutingLearningConfig)
    intelligence: IntelligenceLearningConfig = field(
        default_factory=IntelligenceLearningConfig,
    )
    agent: AgentLearningConfig = field(default_factory=AgentLearningConfig)
    skills: SkillsLearningConfig = field(default_factory=SkillsLearningConfig)
    spec_search: SpecSearchLearningConfig = field(
        default_factory=SpecSearchLearningConfig,
    )
    metrics: MetricsConfig = field(default_factory=MetricsConfig)

    # Training pipeline
    training_enabled: bool = False
    training_schedule: str = ""
    min_improvement: float = 0.02

    # Backward-compat properties for old flat field names
    @property
    def default_policy(self) -> str:
        """Deprecated: use ``learning.routing.policy``."""
        return self.routing.policy

    @default_policy.setter
    def default_policy(self, value: str) -> None:
        self.routing.policy = value

    @property
    def intelligence_policy(self) -> str:
        """Deprecated: use ``learning.intelligence.policy``."""
        return self.intelligence.policy

    @intelligence_policy.setter
    def intelligence_policy(self, value: str) -> None:
        self.intelligence.policy = value

    @property
    def agent_policy(self) -> str:
        """Deprecated: use ``learning.agent.policy``."""
        return self.agent.policy

    @agent_policy.setter
    def agent_policy(self, value: str) -> None:
        self.agent.policy = value

    @property
    def reward_weights(self) -> str:
        """Deprecated: use ``learning.metrics.*``."""
        parts = []
        m = self.metrics
        if m.latency_weight:
            parts.append(f"latency={m.latency_weight}")
        if m.cost_weight:
            parts.append(f"cost={m.cost_weight}")
        if m.efficiency_weight:
            parts.append(f"efficiency={m.efficiency_weight}")
        if m.accuracy_weight:
            parts.append(f"accuracy={m.accuracy_weight}")
        return ",".join(parts)

    @reward_weights.setter
    def reward_weights(self, value: str) -> None:
        if not value:
            return
        for part in value.split(","):
            if "=" not in part:
                continue
            key, val = part.strip().split("=", 1)
            key = key.strip()
            fval = float(val.strip())
            if key == "accuracy":
                self.metrics.accuracy_weight = fval
            elif key == "latency":
                self.metrics.latency_weight = fval
            elif key == "cost":
                self.metrics.cost_weight = fval
            elif key == "efficiency":
                self.metrics.efficiency_weight = fval


@dataclass(slots=True)
class StorageConfig:
    """Storage (memory) backend settings.

    Covers both the retrieval/document store (``default_backend``, ``db_path``,
    chunking, context injection) and the automatic long-term memory service
    (``enabled``, ``backend``, ``extraction_model``, ``max_facts``,
    ``facts_path``) configured under ``[memory]`` in ``config.toml``.
    """

    default_backend: str = "sqlite"
    db_path: str = field(default_factory=lambda: str(get_config_dir() / "memory.db"))
    context_top_k: int = 5
    context_min_score: float = 0.0
    context_max_tokens: int = 2048
    chunk_size: int = 512
    chunk_overlap: int = 64

    # Automatic memory service â€” extracts durable facts from conversations in
    # the background and persists them across sessions (see openjarvis.memory).
    enabled: bool = False  # start the memory service with serve/chat
    backend: str = "local"  # fact-store backend ("local" = on-disk JSONL)
    extraction_model: str = ""  # model for fact extraction ("" = active model)
    max_facts: int = 1000  # cap on stored facts (oldest evicted past the cap)
    facts_path: str = field(
        default_factory=lambda: str(get_config_dir() / "memory_facts.jsonl")
    )


# Backward-compatibility alias
MemoryConfig = StorageConfig


@dataclass(slots=True)
class MCPConfig:
    """MCP (Model Context Protocol) settings."""

    enabled: bool = True
    servers: str = ""  # JSON list of MCP server configs


_MAX_EXTERNAL_JSON_BYTES = 4 * 1024 * 1024


def resolve_json_or_file(raw: str, config_dir: Path) -> Any:
    """Resolve a config value that is either inline JSON or a path to a JSON file.

    Parameters
    ----------
    raw:
        Either a JSON string (starts with '[' or '{') or a file path
        to a .json file containing the data.
    config_dir:
        Directory of config.toml, used to resolve relative file paths.

    Returns
    -------
    Parsed JSON value (dict, list, etc.), or ``None`` if *raw* is empty.

    Raises
    ------
    ValueError: If a relative path escapes the config directory.
    FileNotFoundError: If the referenced file does not exist.
    json.JSONDecodeError: If the JSON content is malformed.
    """
    import json

    if not isinstance(raw, str):
        raise TypeError("JSON config value must be a string")

    stripped = raw.strip()
    if not stripped:
        return None

    # Inline JSON
    if stripped.startswith("[") or stripped.startswith("{"):
        return json.loads(stripped)

    # File path reference
    file_path = Path(stripped).expanduser()
    was_relative = not file_path.is_absolute()
    if was_relative:
        file_path = config_dir / file_path

    resolved = file_path.resolve()

    # Security check: relative paths must not escape the config directory
    if was_relative:
        config_resolved = config_dir.expanduser().resolve()
        try:
            resolved.relative_to(config_resolved)
        except ValueError as exc:
            raise ValueError(
                f"Path '{stripped}' resolves to '{resolved}' which is outside "
                f"the config directory '{config_resolved}'"
            ) from exc

    if not resolved.exists():
        raise FileNotFoundError(
            f"MCP config file not found: {resolved} (from '{stripped}')"
        )
    if not resolved.is_file():
        raise ValueError(f"JSON config path is not a regular file: {resolved}")
    if resolved.stat().st_size > _MAX_EXTERNAL_JSON_BYTES:
        raise ValueError(
            f"JSON config file exceeds {_MAX_EXTERNAL_JSON_BYTES} bytes: {resolved}"
        )

    content = resolved.read_text(encoding="utf-8")
    return json.loads(content)


def resolve_mcp_servers(raw: str, config_dir: Path) -> list[dict[str, Any]]:
    """Resolve MCP server configuration from inline JSON or an external file.

    Wraps :func:`resolve_json_or_file` with MCP-specific validation:
    a single server object ``{...}`` is automatically wrapped in a list,
    and the result must be a ``list``.
    """
    import json

    result = resolve_json_or_file(raw, config_dir)
    if result is None:
        return []
    if isinstance(result, dict):
        result = [result]
    if not isinstance(result, list):
        raise ValueError(
            "MCP servers config must be a JSON array or object, "
            f"got {type(result).__name__}"
        )

    servers: list[dict[str, Any]] = []
    for index, server in enumerate(result):
        if isinstance(server, str):
            try:
                server = json.loads(server)
            except json.JSONDecodeError as exc:
                raise ValueError(
                    f"MCP server entry {index} is not a valid JSON object"
                ) from exc
        if not isinstance(server, dict):
            raise ValueError(f"MCP server entry {index} must be a JSON object")
        servers.append(server)
    return servers


@dataclass(slots=True)
class BrowserConfig:
    """Browser automation settings (Playwright)."""

    headless: bool = True
    timeout_ms: int = 30000
    viewport_width: int = 1280
    viewport_height: int = 720


@dataclass(slots=True)
class WeatherToolConfig:
    """Native weather tool settings (credentials stay outside config.toml)."""

    provider: str = "openweathermap"
    default_location: str = ""
    units: str = "metric"
    lang: str = "en"


@dataclass(slots=True)
class ToolsConfig:
    """Tools primitive settings â€” wraps storage and MCP configuration."""

    storage: StorageConfig = field(default_factory=StorageConfig)
    mcp: MCPConfig = field(default_factory=MCPConfig)
    browser: BrowserConfig = field(default_factory=BrowserConfig)
    weather: WeatherToolConfig = field(default_factory=WeatherToolConfig)
    enabled: str = ""  # comma-separated default tools
    file_allowed_dirs: str = ""  # openjarvis-file-confine-v1 (W78): comma-separated; empty = scratch pad


def resolve_file_write_dirs(cfg: "JarvisConfig") -> List[str]:
    """Directories file_write may write to. openjarvis-file-confine-v1 (W78).

    FileWriteTool accepts allowed_dirs, but no builder ever passed it, so on
    every surface an empty list meant write anywhere. Graystone confines it
    to [tools] file_allowed_dirs, or to the Jarvis scratch pad
    (~/.openjarvis/workspace) when unset. Never returns an empty list.
    """
    raw = getattr(getattr(cfg, "tools", None), "file_allowed_dirs", "") or ""
    dirs = [d.strip() for d in str(raw).split(",") if d.strip()]
    if not dirs:
        dirs = [str(DEFAULT_CONFIG_DIR / "workspace")]
    out: List[str] = []
    for d in dirs:
        p = Path(d).expanduser()
        try:
            p.mkdir(parents=True, exist_ok=True)
        except OSError:
            pass
        out.append(str(p))
    return out


@dataclass
class AgentConfig:
    """Agent harness settings â€” orchestration, tools, system prompt."""

    default_agent: str = "simple"
    max_turns: int = 10
    tools: str = ""  # comma-separated tool names
    objective: str = ""  # concise purpose for routing/learning/docs
    system_prompt: str = ""  # inline system prompt (takes precedence if set)
    system_prompt_path: str = ""  # path to system prompt file (.txt, .md)
    context_from_memory: bool = True  # inject relevant memory context into prompts
    default_system_prompt: str = (
        "You are OpenJarvis, a helpful AI assistant running locally on the "
        "user's own hardware. You are not a cloud service, and you are not "
        "Claude, ChatGPT, Gemini, or any other branded assistant. If asked "
        "who or what you are, identify yourself as OpenJarvis. Respond "
        "helpfully, concisely, and accurately."
    )

    # Backward-compat property for old field name
    @property
    def default_tools(self) -> str:
        """Deprecated: use ``agent.tools``."""
        return self.tools

    @default_tools.setter
    def default_tools(self, value: str) -> None:
        self.tools = value


@dataclass(slots=True)
class ServerConfig:
    """API server settings."""

    host: str = "127.0.0.1"
    port: int = 8010
    agent: str = "orchestrator"
    model: str = ""
    workers: int = 1
    cors_origins: list = field(
        default_factory=lambda: [
            "http://localhost:3000",
            "http://localhost:5173",
            "http://localhost:5174",
            "http://127.0.0.1:3000",
            "http://127.0.0.1:5173",
            "http://127.0.0.1:5174",
            # Tauri 2 production webview origins.
            # macOS / Linux / iOS use the custom scheme; Windows /
            # Android use http(s)://tauri.localhost. All three must
            # be allowed so the desktop app's chat-completions stream
            # is not blocked by CORS in production builds.
            "tauri://localhost",
            "http://tauri.localhost",
            "https://tauri.localhost",
        ]
    )


@dataclass(slots=True)
class TelemetryConfig:
    """Telemetry persistence settings."""

    enabled: bool = True
    db_path: str = field(default_factory=lambda: str(get_config_dir() / "telemetry.db"))
    gpu_metrics: bool = False
    gpu_poll_interval_ms: int = 50
    energy_vendor: str = ""  # auto-detect or force "nvidia"/"amd"/"apple"/"cpu_rapl"
    # Permit a modelled energy estimate when no hardware counters are
    # readable. Off by default: an estimate written to the telemetry DB is
    # indistinguishable from a measurement at query time except via
    # `energy_method`, and on Apple Silicon the estimate is a function of
    # wall-clock alone, so it cannot tell an idle window from a busy one.
    allow_energy_estimates: bool = False
    warmup_samples: int = 0
    steady_state_window: int = 5
    steady_state_threshold: float = 0.05


@dataclass(slots=True)
class AnalyticsConfig:
    """External anonymous usage analytics (PostHog).

    Separate concern from :class:`TelemetryConfig`, which stores local
    FLOPs/energy/inference metrics in SQLite. This controls anonymized
    usage events sent to the OpenJarvis team's PostHog instance to
    measure setup success, retention, feature usage, and churn.

    No chat content, prompts, model outputs, file paths, emails, IPs,
    or hardware identifiers are ever sent. See ``docs/telemetry.md``.
    """

    enabled: bool = True
    host: str = "https://34.231.106.201.sslip.io"
    key: str = "phc_ysKu72QaxzYNmDpHFcesD2ZZAe68zkdWJEKoYYkc5e3n"
    anon_id_path: str = field(default_factory=lambda: str(get_config_dir() / "anon_id"))
    flush_interval_seconds: int = 30
    flush_at_size: int = 100


@dataclass(slots=True)
class TracesConfig:
    """Trace system settings."""

    enabled: bool = True
    db_path: str = field(default_factory=lambda: str(get_config_dir() / "traces.db"))


@dataclass(slots=True)
class ProactiveConfig:
    """Proactive agent â€” autonomous action scheduling and approval routing."""

    enabled: bool = False
    schedule: str = "0 5 * * *"  # cron expression (default: 5am daily)
    hours_back: int = 24  # how many hours of unacted items to scan
    timezone: str = "America/Los_Angeles"
    # Channel to send approval notifications and receive yes/no replies.
    # Format: "{type}:{id}", e.g. "imessage:+15551234567" or "telegram:123456789"
    notification_channel: str = ""


@dataclass(slots=True)
class TelegramChannelConfig:
    """Per-channel config for Telegram."""

    bot_token: str = ""
    allowed_chat_ids: str = ""
    parse_mode: str = "Markdown"


@dataclass(slots=True)
class DiscordChannelConfig:
    """Per-channel config for Discord."""

    bot_token: str = ""


@dataclass(slots=True)
class SlackChannelConfig:
    """Per-channel config for Slack."""

    bot_token: str = ""
    app_token: str = ""


@dataclass(slots=True)
class WebhookChannelConfig:
    """Per-channel config for generic webhooks."""

    url: str = ""
    secret: str = ""
    method: str = "POST"


@dataclass(slots=True)
class EmailChannelConfig:
    """Per-channel config for email (SMTP/IMAP)."""

    smtp_host: str = ""
    smtp_port: int = 587
    imap_host: str = ""
    imap_port: int = 993
    username: str = ""
    password: str = ""
    use_tls: bool = True


@dataclass(slots=True)
class WhatsAppChannelConfig:
    """Per-channel config for WhatsApp Cloud API."""

    access_token: str = ""
    phone_number_id: str = ""


@dataclass(slots=True)
class SignalChannelConfig:
    """Per-channel config for Signal (via signal-cli REST API)."""

    api_url: str = ""
    phone_number: str = ""


@dataclass(slots=True)
class GoogleChatChannelConfig:
    """Per-channel config for Google Chat webhooks."""

    webhook_url: str = ""


@dataclass(slots=True)
class IRCChannelConfig:
    """Per-channel config for IRC."""

    server: str = ""
    port: int = 6667
    nick: str = ""
    password: str = ""
    use_tls: bool = False


@dataclass(slots=True)
class WebChatChannelConfig:
    """Per-channel config for in-memory webchat."""

    pass


@dataclass(slots=True)
class TeamsChannelConfig:
    """Per-channel config for Microsoft Teams (Bot Framework)."""

    app_id: str = ""
    app_password: str = ""
    service_url: str = ""


@dataclass(slots=True)
class MatrixChannelConfig:
    """Per-channel config for Matrix."""

    homeserver: str = ""
    access_token: str = ""


@dataclass(slots=True)
class MattermostChannelConfig:
    """Per-channel config for Mattermost."""

    url: str = ""
    token: str = ""


@dataclass(slots=True)
class FeishuChannelConfig:
    """Per-channel config for Feishu (Lark)."""

    app_id: str = ""
    app_secret: str = ""


@dataclass(slots=True)
class BlueBubblesChannelConfig:
    """Per-channel config for BlueBubbles (iMessage bridge)."""

    url: str = ""
    password: str = ""


@dataclass(slots=True)
class WhatsAppBaileysChannelConfig:
    """Per-channel config for WhatsApp via Baileys protocol."""

    auth_dir: str = ""  # Defaults to ~/.openjarvis/whatsapp_auth
    assistant_name: str = "Jarvis"
    assistant_has_own_number: bool = False


@dataclass
class ChannelConfig:
    """Channel messaging settings."""

    enabled: bool = False
    default_channel: str = ""
    default_agent: str = "simple"
    telegram: TelegramChannelConfig = field(default_factory=TelegramChannelConfig)
    discord: DiscordChannelConfig = field(default_factory=DiscordChannelConfig)
    slack: SlackChannelConfig = field(default_factory=SlackChannelConfig)
    webhook: WebhookChannelConfig = field(default_factory=WebhookChannelConfig)
    email: EmailChannelConfig = field(default_factory=EmailChannelConfig)
    whatsapp: WhatsAppChannelConfig = field(default_factory=WhatsAppChannelConfig)
    signal: SignalChannelConfig = field(default_factory=SignalChannelConfig)
    google_chat: GoogleChatChannelConfig = field(
        default_factory=GoogleChatChannelConfig,
    )
    irc: IRCChannelConfig = field(default_factory=IRCChannelConfig)
    webchat: WebChatChannelConfig = field(default_factory=WebChatChannelConfig)
    teams: TeamsChannelConfig = field(default_factory=TeamsChannelConfig)
    matrix: MatrixChannelConfig = field(default_factory=MatrixChannelConfig)
    mattermost: MattermostChannelConfig = field(default_factory=MattermostChannelConfig)
    feishu: FeishuChannelConfig = field(default_factory=FeishuChannelConfig)
    bluebubbles: BlueBubblesChannelConfig = field(
        default_factory=BlueBubblesChannelConfig,
    )
    whatsapp_baileys: WhatsAppBaileysChannelConfig = field(
        default_factory=WhatsAppBaileysChannelConfig,
    )


@dataclass(slots=True)
class CapabilitiesConfig:
    """RBAC capability system settings."""

    enabled: bool = False
    policy_path: str = ""
    default_deny: bool = False


@dataclass(slots=True)
class SecurityConfig:
    """Security guardrails settings."""

    enabled: bool = True
    scan_input: bool = True
    scan_output: bool = True
    mode: str = "redact"  # "redact" | "warn" | "block"
    secret_scanner: bool = True
    pii_scanner: bool = True
    audit_log_path: str = field(
        default_factory=lambda: str(get_config_dir() / "audit.db")
    )
    enforce_tool_confirmation: bool = True
    merkle_audit: bool = True
    signing_key_path: str = ""
    ssrf_protection: bool = True
    rate_limit_enabled: bool = True
    rate_limit_rpm: int = 60
    rate_limit_burst: int = 10
    local_engine_bypass: bool = False
    local_tool_bypass: bool = False
    profile: str = ""
    vault_key_path: str = field(
        default_factory=lambda: str(get_config_dir() / ".vault_key")
    )
    capabilities: CapabilitiesConfig = field(default_factory=CapabilitiesConfig)


# ---------------------------------------------------------------------------
# Security profile presets
# ---------------------------------------------------------------------------

_SECURITY_PROFILES: Dict[str, Dict[str, Dict[str, Any]]] = {
    "personal": {
        "security": {
            "mode": "redact",
            "rate_limit_enabled": True,
            "local_engine_bypass": False,
            "local_tool_bypass": False,
        },
        "server": {
            "host": "127.0.0.1",
        },
    },
    "shared": {
        "security": {
            "mode": "redact",
            "rate_limit_enabled": True,
            "local_engine_bypass": False,
            "local_tool_bypass": False,
            "capabilities": {"enabled": True, "default_deny": True},
        },
        "server": {
            "host": "127.0.0.1",
        },
    },
    "server": {
        "security": {
            "mode": "block",
            "rate_limit_enabled": True,
            "rate_limit_rpm": 30,
            "rate_limit_burst": 5,
            "local_engine_bypass": False,
            "local_tool_bypass": False,
            "capabilities": {"enabled": True, "default_deny": True},
        },
        "server": {
            "host": "0.0.0.0",
        },
    },
}


def apply_security_profile(
    security_cfg: "SecurityConfig",
    server_cfg: "ServerConfig | None",
    *,
    overrides: "set[str] | None" = None,
) -> None:
    """Expand a named security profile into config fields.

    Fields in *overrides* (explicitly set by the user in TOML) are
    not overwritten by the profile.
    """
    profile = security_cfg.profile
    if not profile:
        return

    if profile not in _SECURITY_PROFILES:
        raise ValueError(
            f"Unknown security profile '{profile}'. "
            f"Valid profiles: {', '.join(_SECURITY_PROFILES)}"
        )

    _overrides = overrides or set()
    pdef = _SECURITY_PROFILES[profile]

    for key, value in pdef.get("security", {}).items():
        if key == "capabilities" and isinstance(value, dict):
            # Preserve explicitly selected fields while inheriting the
            # profile's remaining defaults. A policy_path alone must not
            # silently disable the profile's capability gate.
            if "capabilities" in _overrides:
                continue
            for cap_key, cap_value in value.items():
                if f"capabilities.{cap_key}" not in _overrides and hasattr(
                    security_cfg.capabilities, cap_key
                ):
                    setattr(security_cfg.capabilities, cap_key, cap_value)
            continue
        if key not in _overrides and hasattr(security_cfg, key):
            setattr(security_cfg, key, value)

    if server_cfg is not None:
        for key, value in pdef.get("server", {}).items():
            if key not in _overrides and hasattr(server_cfg, key):
                setattr(server_cfg, key, value)


@dataclass(slots=True)
class SandboxConfig:
    """Container sandbox settings."""

    enabled: bool = False
    image: str = "openjarvis-sandbox:latest"
    timeout: int = 300
    workspace: str = ""
    mount_allowlist_path: str = ""
    max_concurrent: int = 5
    runtime: str = "docker"
    wasm_fuel_limit: int = 1_000_000
    wasm_memory_limit_mb: int = 256


@dataclass(slots=True)
class SchedulerConfig:
    """Task scheduler settings."""

    enabled: bool = False
    poll_interval: int = 60
    db_path: str = ""  # Defaults to ~/.openjarvis/scheduler.db


@dataclass(slots=True)
class WorkflowConfig:
    """Workflow engine settings."""

    enabled: bool = False
    max_parallel: int = 4
    default_node_timeout: int = 300


@dataclass(slots=True)
class SessionConfig:
    """Cross-channel session settings."""

    enabled: bool = False
    max_age_hours: float = 24.0
    consolidation_threshold: int = 100
    db_path: str = field(default_factory=lambda: str(get_config_dir() / "sessions.db"))


@dataclass(slots=True)
class A2AConfig:
    """Agent-to-Agent protocol settings."""

    enabled: bool = False
    # Bearer token required for inbound A2A requests. Empty = unauthenticated
    # (only safe on a trusted network). See ``A2AServer(auth_token=...)``.
    auth_token: str = ""


@dataclass(slots=True)
class OperatorsConfig:
    """Operator lifecycle settings."""

    enabled: bool = False
    manifests_dir: str = field(
        default_factory=lambda: str(get_config_dir() / "operators")
    )
    auto_activate: str = ""  # Comma-separated operator IDs


@dataclass(slots=True)
class SpeechConfig:
    """Speech-to-text settings."""

    backend: str = "auto"  # "auto", "faster-whisper", "openai", "deepgram"
    model: str = "base"  # Whisper model size: tiny, base, small, medium, large-v3
    language: str = ""  # Empty = auto-detect
<<<<<<< HEAD
    device: str = "auto"  # "auto", "cpu", "cuda" - CTranslate2 resolves
    compute_type: str = "auto"  # "auto" = fastest type the HARDWARE supports
=======
    device: str = "auto"  # "auto", "cpu", "cuda"
    compute_type: str = "float16"  # "float16", "int8", "float32"
    # Text-to-speech. ``voice_id`` is interpreted by ``tts_backend`` only --
    # voice IDs are not portable between backends, so if voice output falls
    # back to a different backend that backend's own default voice is used.
    # Kokoro IDs: bm_george / bm_lewis (British male), bf_emma / bf_isabella
    # (British female), af_* / am_* (American).
    tts_backend: str = "kokoro"  # "kokoro", "openai_tts", "cartesia"
    voice_id: str = "bm_george"
    voice_speed: float = 1.0
>>>>>>> a6dcf846


@dataclass(slots=True)
class OptimizeConfig:
    """Configuration optimization settings."""

    max_trials: int = 20
    early_stop_patience: int = 5
    optimizer_model: str = "claude-sonnet-4-6"
    optimizer_provider: str = "anthropic"
    benchmark: str = ""
    max_samples: int = 50
    judge_model: str = "gpt-5-mini-2025-08-07"
    db_path: str = field(default_factory=lambda: str(get_config_dir() / "optimize.db"))


@dataclass(slots=True)
class AgentManagerConfig:
    """Persistent agent manager settings."""

    enabled: bool = True
    db_path: str = field(default_factory=lambda: str(get_config_dir() / "agents.db"))


@dataclass(slots=True)
class MemoryFilesConfig:
    """Persistent memory-file paths and nudge settings."""

    soul_path: str = field(default_factory=lambda: str(get_config_dir() / "SOUL.md"))
    memory_path: str = field(
        default_factory=lambda: str(get_config_dir() / "MEMORY.md")
    )
    user_path: str = field(default_factory=lambda: str(get_config_dir() / "USER.md"))
    nudge_interval: int = 10
    persona_name: str = ""  # named persona dir under <config-dir>/personas/<name>/


@dataclass(slots=True)
class SystemPromptConfig:
    """Limits and strategy for system-prompt assembly."""

    prefix: str = ""
    soul_max_chars: int = 4000
    memory_max_chars: int = 2500
    user_max_chars: int = 1500
    skill_desc_max_chars: int = 60
    truncation_strategy: str = "head_tail"


@dataclass(slots=True)
class CompressionConfig:
    """Configuration for context compression."""

    enabled: bool = True
    threshold: float = 0.50
    strategy: str = "session_consolidation"


@dataclass(slots=True)
class SkillSourceConfig:
    """Configuration for a single skill source (Hermes, OpenClaw, GitHub)."""

    source: str = ""  # "hermes", "openclaw", or "github"
    url: str = ""  # required when source = "github"
    filter: Dict[str, Any] = field(default_factory=dict)
    auto_update: bool = False


@dataclass(slots=True)
class SkillsConfig:
    """Configuration for agent-authored procedural skills."""

    enabled: bool = True
    skills_dir: str = field(default_factory=lambda: str(get_config_dir() / "skills"))
    active: str = "*"
    auto_discover: bool = True
    auto_sync: bool = False
    nudge_interval: int = 15
    index_repo: str = "https://github.com/openjarvis/skill-index.git"
    index_dir: str = field(
        default_factory=lambda: str(get_config_dir() / "skill-index")
    )
    max_depth: int = 5
    sandbox_dangerous: bool = True
    sources: List[SkillSourceConfig] = field(default_factory=list)


@dataclass
class DigestSectionConfig:
    """Configuration for a single digest section."""

    sources: List[str] = field(default_factory=list)
    max_items: int = 10
    priority_contacts: List[str] = field(default_factory=list)


@dataclass
class DigestConfig:
    """Configuration for the morning digest feature."""

    enabled: bool = False
    schedule: str = "0 6 * * *"
    timezone: str = "America/Los_Angeles"
    persona: str = "jarvis"
    sections: List[str] = field(
        default_factory=lambda: ["messages", "calendar", "health", "world"]
    )
    optional_sections: List[str] = field(
        default_factory=lambda: ["github", "financial", "music", "fitness"]
    )
    honorific: str = "sir"
    voice_id: str = ""
    voice_speed: float = 1.0
    tts_backend: str = "cartesia"
    messages: DigestSectionConfig = field(
        default_factory=lambda: DigestSectionConfig(
            sources=["gmail", "slack", "google_tasks"]
        )
    )
    calendar: DigestSectionConfig = field(
        default_factory=lambda: DigestSectionConfig(sources=["gcalendar"])
    )
    health: DigestSectionConfig = field(
        default_factory=lambda: DigestSectionConfig(sources=["oura", "apple_health"])
    )
    world: DigestSectionConfig = field(
        default_factory=lambda: DigestSectionConfig(sources=[])
    )


@dataclass
class JarvisConfig:
    """Top-level configuration for OpenJarvis."""

    installed_at: str = ""
    installer_version: str = ""
    hardware: HardwareInfo = field(default_factory=HardwareInfo)
    engine: EngineConfig = field(default_factory=EngineConfig)
    intelligence: IntelligenceConfig = field(default_factory=IntelligenceConfig)
    deep_research: DeepResearchConfig = field(default_factory=DeepResearchConfig)
    learning: LearningConfig = field(default_factory=LearningConfig)
    tools: ToolsConfig = field(default_factory=ToolsConfig)
    agent: AgentConfig = field(default_factory=AgentConfig)
    server: ServerConfig = field(default_factory=ServerConfig)
    telemetry: TelemetryConfig = field(default_factory=TelemetryConfig)
    analytics: AnalyticsConfig = field(default_factory=AnalyticsConfig)
    traces: TracesConfig = field(default_factory=TracesConfig)
    channel: ChannelConfig = field(default_factory=ChannelConfig)
    security: SecurityConfig = field(default_factory=SecurityConfig)
    sandbox: SandboxConfig = field(default_factory=SandboxConfig)
    scheduler: SchedulerConfig = field(default_factory=SchedulerConfig)
    workflow: WorkflowConfig = field(default_factory=WorkflowConfig)
    sessions: SessionConfig = field(default_factory=SessionConfig)
    a2a: A2AConfig = field(default_factory=A2AConfig)
    operators: OperatorsConfig = field(default_factory=OperatorsConfig)
    speech: SpeechConfig = field(default_factory=SpeechConfig)
    optimize: OptimizeConfig = field(default_factory=OptimizeConfig)
    agent_manager: AgentManagerConfig = field(default_factory=AgentManagerConfig)
    memory_files: MemoryFilesConfig = field(default_factory=MemoryFilesConfig)
    system_prompt: SystemPromptConfig = field(default_factory=SystemPromptConfig)
    compression: CompressionConfig = field(default_factory=CompressionConfig)
    skills: SkillsConfig = field(default_factory=SkillsConfig)
    digest: DigestConfig = field(default_factory=DigestConfig)
    proactive: ProactiveConfig = field(default_factory=ProactiveConfig)
    mining: Optional["MiningConfig"] = None

    @property
    def _config_dir(self) -> Path:
        """Directory containing the loaded config, or the env-aware default."""
        return self.__dict__.get("_config_source_dir", get_config_dir())

    @_config_dir.setter
    def _config_dir(self, value: Path) -> None:
        self.__dict__["_config_source_dir"] = Path(value)

    @property
    def memory(self) -> StorageConfig:
        """Backward-compatible accessor â€” canonical location is tools.storage."""
        return self.tools.storage

    @memory.setter
    def memory(self, value: StorageConfig) -> None:
        """Backward-compatible setter."""
        self.tools.storage = value


# ---------------------------------------------------------------------------
# Config key validation
# ---------------------------------------------------------------------------

# Sections that users may set via ``jarvis config set``.
# ``hardware`` is auto-detected and not user-settable.
_SETTABLE_SECTIONS = frozenset(JarvisConfig.__dataclass_fields__.keys()) - {
    "hardware",
    "mining",
}


def validate_config_key(dotted_key: str) -> type:
    """Validate a dotted config key and return the leaf field's Python type.

    Raises :class:`ValueError` when the key does not map to a known field.
    The function walks the ``JarvisConfig`` dataclass hierarchy using
    ``dataclasses.fields()``.

    Examples::

        validate_config_key("engine.ollama.host")      # -> str
        validate_config_key("intelligence.temperature") # -> float
    """
    from dataclasses import fields as dc_fields

    def contains_dataclass(annotation: Any) -> bool:
        if is_dataclass(annotation):
            return True
        return any(contains_dataclass(arg) for arg in get_args(annotation))

    parts = dotted_key.split(".")
    if len(parts) < 2:
        raise ValueError(
            f"Config key must have at least two segments (e.g. engine.default), "
            f"got: {dotted_key!r}"
        )

    if parts[0] not in _SETTABLE_SECTIONS:
        raise ValueError(
            f"Unknown config key: {dotted_key!r} "
            f"(valid top-level sections: {sorted(_SETTABLE_SECTIONS)})"
        )

    # Walk the dataclass tree
    current_cls = JarvisConfig
    for i, part in enumerate(parts):
        field_map = {f.name: f for f in dc_fields(current_cls)}
        if part not in field_map:
            path_so_far = ".".join(parts[: i + 1])
            raise ValueError(
                f"Unknown config key: {dotted_key!r} "
                f"(no field {part!r} at {path_so_far}; "
                f"valid fields: {sorted(field_map.keys())})"
            )
        fld = field_map[part]
        # Resolve the type â€” unwrap Optional, etc.
        fld_type = fld.type
        if isinstance(fld_type, str):
            # Evaluate forward references in the config module namespace
            import openjarvis.core.config as _cfg_mod

            fld_type = eval(fld_type, vars(_cfg_mod))  # noqa: S307

        if i == len(parts) - 1:
            if contains_dataclass(fld_type):
                suggestions = ""
                if is_dataclass(fld_type):
                    child_keys = [
                        f"{dotted_key}.{child.name}" for child in dc_fields(fld_type)
                    ]
                    suggestions = f"; set one of: {', '.join(child_keys)}"
                raise ValueError(
                    f"Config key {dotted_key!r} names a section, not a settable value"
                    f"{suggestions}"
                )
            # Leaf â€” return the primitive/container type
            return fld_type
        else:
            # Must be a nested dataclass
            if not hasattr(fld_type, "__dataclass_fields__"):
                path_so_far = ".".join(parts[: i + 1])
                raise ValueError(
                    f"Unknown config key: {dotted_key!r} "
                    f"({path_so_far} is a leaf of type {fld_type.__name__}, "
                    f"not a section)"
                )
            current_cls = fld_type

    # Should not reach here, but satisfy type checker
    raise ValueError(f"Unknown config key: {dotted_key!r}")


# ---------------------------------------------------------------------------
# TOML loading
# ---------------------------------------------------------------------------


def _apply_toml_section(target: Any, section: Dict[str, Any]) -> None:
    """Overlay TOML key/value pairs onto a dataclass instance.

    Recursively handles nested dicts when the target attribute is itself
    a dataclass, including dict entries in lists of dataclasses.  Normalises
    TOML arrays to comma-separated strings â€” both for dataclass fields annotated
    as ``str`` and for backward-compat property setters that expect string input.
    """
    try:
        type_hints = get_type_hints(type(target))
    except (NameError, TypeError):
        # Some config types contain optional runtime-only forward references.
        type_hints = {}

    for key, value in section.items():
        if hasattr(target, key):
            if isinstance(value, dict):
                nested = getattr(target, key)
                if hasattr(nested, "__dataclass_fields__"):
                    _apply_toml_section(nested, value)
                else:
                    setattr(target, key, value)
            else:
                # Normalise TOML arrays â†’ comma-separated string.
                # Covers both real dataclass fields and backward-compat
                # property setters (e.g. reward_weights, default_tools).
                if isinstance(value, list):
                    is_str_field = False
                    item_dataclass = None
                    if hasattr(target, "__dataclass_fields__"):
                        field_obj = target.__dataclass_fields__.get(key)
                        if field_obj is not None:
                            field_type = type_hints.get(key, field_obj.type)
                            type_args = get_args(field_type)
                            if (
                                get_origin(field_type) is list
                                and len(type_args) == 1
                                and is_dataclass(type_args[0])
                            ):
                                item_dataclass = type_args[0]
                            elif field_obj.type in ("str", str):
                                is_str_field = True
                        else:
                            # Property, not a real field â€” normalise to string
                            is_str_field = True

                    if item_dataclass is not None:
                        converted = []
                        for item in value:
                            if isinstance(item, dict):
                                nested = item_dataclass()
                                _apply_toml_section(nested, item)
                                converted.append(nested)
                            else:
                                converted.append(item)
                        value = converted
                    elif is_str_field:
                        value = ",".join(str(v) for v in value)
                setattr(target, key, value)


def _migrate_toml_data(data: Dict[str, Any], cfg: "JarvisConfig") -> None:
    """Migrate old-format TOML keys to new structure in-place.

    Handles cross-section moves that can't be solved by backward-compat
    properties alone (e.g. ``agent.temperature`` â†’ ``intelligence.temperature``).
    """
    # agent.temperature / agent.max_tokens â†’ intelligence.*
    if "agent" in data:
        agent_data = data["agent"]
        intel_data = data.setdefault("intelligence", {})
        for moved_key in ("temperature", "max_tokens"):
            if moved_key in agent_data:
                intel_data.setdefault(moved_key, agent_data.pop(moved_key))

    # context_injection from memory / tools.storage â†’ agent.context_from_memory
    for src_section in ("memory",):
        src = data.get(src_section, {})
        if isinstance(src, dict) and "context_injection" in src:
            data.setdefault("agent", {}).setdefault(
                "context_from_memory",
                src.pop("context_injection"),
            )

    if "tools" in data:
        tools_data = data["tools"]
        if isinstance(tools_data, dict):
            storage_sub = tools_data.get("storage", {})
            if isinstance(storage_sub, dict) and "context_injection" in storage_sub:
                data.setdefault("agent", {}).setdefault(
                    "context_from_memory",
                    storage_sub.pop("context_injection"),
                )


def _parse_mining_section(data: dict) -> Optional["MiningConfig"]:
    """Parse the ``[mining]`` TOML section into a ``MiningConfig``.

    Returns None if the section is absent. Resolves the ``submit_target``
    string into a ``SoloTarget`` or ``PoolTarget`` tagged union.
    """
    if "mining" not in data:
        return None

    # Lazy runtime import to break the import cycle: ``mining/_stubs.py``
    # imports ``HardwareInfo`` from this module at its top level. By the
    # time ``_parse_mining_section`` is called, ``core.config`` is already
    # fully initialized in ``sys.modules``, so the cycle is harmless.
    from openjarvis.mining._stubs import MiningConfig, PoolTarget, SoloTarget

    section = data["mining"]
    extra = section.get("extra", {}) or {}

    target_str = section.get("submit_target", "solo")
    submit_target: Any
    if target_str == "solo":
        submit_target = SoloTarget(
            pearld_rpc_url=extra.get("pearld_rpc_url", "http://localhost:44107")
        )
    elif isinstance(target_str, str) and target_str.startswith("pool:"):
        submit_target = PoolTarget(url=target_str[len("pool:") :])
    else:
        raise ValueError(
            f"[mining].submit_target must be 'solo' or 'pool:<url>', got {target_str!r}"
        )

    return MiningConfig(
        provider=section["provider"],
        wallet_address=section["wallet_address"],
        submit_target=submit_target,
        fee_bps=int(section.get("fee_bps", 0)),
        fee_payout_address=section.get("fee_payout_address") or None,
        extra={k: v for k, v in extra.items()},
    )


@functools.lru_cache(maxsize=1)
def load_config(path: Optional[Path] = None) -> JarvisConfig:
    """Detect hardware, build defaults, overlay TOML overrides.

    Parameters
    ----------
    path:
        Explicit config file. If not set, uses ``OPENJARVIS_CONFIG`` when set,
        otherwise ``~/.openjarvis/config.toml``.
    """
    _ensure_config_dir()
    hw = detect_hardware()
    cfg = JarvisConfig(hardware=hw)
    cfg.engine.default = recommend_engine(hw)

    if path is not None:
        config_path = Path(path).expanduser().resolve()
    elif os.environ.get("OPENJARVIS_CONFIG"):
        config_path = Path(os.environ["OPENJARVIS_CONFIG"]).expanduser().resolve()
    else:
        config_path = get_config_path()
    cfg._config_dir = config_path.parent
    if config_path.exists():
        with open(config_path, "rb") as fh:
            data = tomllib.load(fh)

        # Run backward-compat migrations before applying
        _migrate_toml_data(data, cfg)

        # All top-level sections â€” recursive _apply_toml_section handles
        # nested sub-configs (engine.ollama, learning.routing, channel.*, etc.)
        top_sections = (
            "engine",
            "intelligence",
            "deep_research",
            "learning",
            "agent",
            "server",
            "telemetry",
            "analytics",
            "traces",
            "security",
            "channel",
            "tools",
            "sandbox",
            "scheduler",
            "workflow",
            "sessions",
            "a2a",
            "operators",
            "speech",
            "optimize",
            "agent_manager",
            "digest",
            "proactive",
            "memory_files",
            "system_prompt",
            "compression",
            "skills",
        )
        for section_name in top_sections:
            if section_name in data:
                _apply_toml_section(
                    getattr(cfg, section_name),
                    data[section_name],
                )

        # Memory: accept [memory] (old) â†’ maps to tools.storage
        if "memory" in data:
            _apply_toml_section(cfg.tools.storage, data["memory"])

        # Top-level install provenance (installed_at, installer_version)
        for key in ("installed_at", "installer_version"):
            if key in data:
                setattr(cfg, key, data[key])

        # Expand security profile (user TOML overrides take precedence)
        _security_data = data.get("security", {})
        _user_security_keys = set(_security_data)
        if isinstance(_security_data.get("capabilities"), dict):
            _user_security_keys.discard("capabilities")
            _user_security_keys.update(
                f"capabilities.{key}" for key in _security_data["capabilities"]
            )
        apply_security_profile(cfg.security, cfg.server, overrides=_user_security_keys)

        # Mining: dedicated parser for tagged-union submit_target
        cfg.mining = _parse_mining_section(data)

    # Apply profile even without a config file (in case defaults set one)
    if not config_path.exists() and cfg.security.profile:
        apply_security_profile(cfg.security, cfg.server)

    return cfg


# ---------------------------------------------------------------------------
# Default TOML generation (for ``jarvis init``)
# ---------------------------------------------------------------------------


def generate_minimal_toml(
    hw: HardwareInfo, engine: str | None = None, *, host: str | None = None
) -> str:
    """Render a minimal TOML config with only essential settings."""
    engine = engine or recommend_engine(hw)
    model = recommend_model(hw, engine)
    gpu_comment = ""
    if hw.gpu:
        mem_label = "unified memory" if hw.gpu.vendor == "apple" else "VRAM"
        gpu_comment = f"\n# GPU: {hw.gpu.name} ({hw.gpu.vram_gb} GB {mem_label})"
    if host:
        engine_host_section = f'\n[engine.{engine}]\nhost = "{host}"\n'
    else:
        engine_host_section = (
            f"\n[engine.{engine}]\n"
            f'# host = "http://localhost:11434"  '
            f"# set to remote URL if engine runs elsewhere\n"
        )
    return f"""\
# OpenJarvis configuration
# Hardware: {hw.cpu_brand} ({hw.cpu_count} cores, {hw.ram_gb} GB RAM){gpu_comment}
# Full reference config: jarvis init --full

[engine]
default = "{engine}"
{engine_host_section}
[intelligence]
default_model = "{model}"

[agent]
default_agent = "simple"

[tools]
enabled = ["code_interpreter", "web_search", "file_read", "shell_exec"]
"""


def generate_default_toml(
    hw: HardwareInfo, engine: str | None = None, *, host: str | None = None
) -> str:
    """Render a commented TOML string suitable for ``~/.openjarvis/config.toml``."""
    engine = engine or recommend_engine(hw)
    model = recommend_model(hw, engine)
    gpu_line = ""
    if hw.gpu:
        gpu_line = f"# Detected GPU: {hw.gpu.name} ({hw.gpu.vram_gb} GB VRAM)"

    model_comment = ""
    if model:
        model_comment = "  # recommended for your hardware"

    result = f"""\
# OpenJarvis configuration
# Generated by `jarvis init`
#
# Hardware: {hw.cpu_brand} ({hw.cpu_count} cores, {hw.ram_gb} GB RAM)
{gpu_line}

[engine]
default = "{engine}"

[engine.ollama]
host = "http://localhost:11434"

[engine.vllm]
host = "http://localhost:8010"

[engine.sglang]
host = "http://localhost:30000"

# [engine.llamacpp]
# host = "http://localhost:8080"
# binary_path = ""

[engine.mlx]
host = "http://localhost:8080"

# [engine.lmstudio]
# host = "http://localhost:1234"

# [engine.exo]
# host = "http://localhost:52415"

# [engine.nexa]
# host = "http://localhost:18181"
# device = ""  # cpu, gpu, npu

# [engine.uzu]
# host = "http://localhost:8080"

# [engine.apple_fm]
# host = "http://localhost:8079"

[intelligence]
default_model = "{model}"{model_comment}
fallback_model = ""
# model_path = ""              # Local weights (HF repo, GGUF file, etc.)
# checkpoint_path = ""         # Checkpoint/adapter path
# quantization = "none"        # none, fp8, int8, int4, gguf_q4, gguf_q8
# preferred_engine = ""        # Override engine for this model (e.g., "vllm")
# provider = ""                # local, openai, anthropic, google
temperature = 0.7
max_tokens = 1024
# top_p = 0.9
# top_k = 40
# repetition_penalty = 1.0
# stop_sequences = ""

# [deep_research]
# engine = ""                  # empty = use [engine].default
# model = ""                   # empty = use [intelligence].default_model

[agent]
default_agent = "simple"
max_turns = 10
# tools = ""                   # Comma-separated tool names
# objective = ""               # Concise purpose string
# system_prompt = ""           # Inline system prompt
# system_prompt_path = ""      # Path to system prompt file
context_from_memory = true

[tools.storage]
default_backend = "sqlite"

# Automatic long-term memory: extracts durable facts from conversations in the
# background and persists them. Starts/stops with `jarvis serve` and
# `jarvis chat`; manage stored facts with `jarvis memory list` / `clear`.
[memory]
enabled = false               # set true to enable the memory service
backend = "local"             # fact-store backend (local = on-disk JSONL)
extraction_model = ""         # model for fact extraction ("" = active model)
max_facts = 1000              # cap on stored facts

[tools.mcp]
enabled = true

# [tools.browser]
# headless = true
# timeout_ms = 30000
# viewport_width = 1280
# viewport_height = 720

# Weather API credentials belong in credentials.toml or the environment, not here.
# [tools.weather]
# provider = "openweathermap"
# default_location = ""
# units = "metric"             # metric or imperial
# lang = "en"                  # OpenWeatherMap language code

[server]
<<<<<<< HEAD
host = "0.0.0.0"
port = 8010
agent = "native_openhands"
=======
# Loopback is safe for local use and works without API authentication.
host = "127.0.0.1"
# To serve other machines, configure an API key before using:
# host = "0.0.0.0"
port = 8000
agent = "orchestrator"
>>>>>>> a6dcf846

[learning]
enabled = false
update_interval = 100
# auto_update = false

[learning.routing]
policy = "heuristic"
# min_samples = 5

# [learning.intelligence]
# policy = "none"              # "sft" to learn from traces

# [learning.agent]
# policy = "none"              # "agent_advisor" | "icl_updater"

# [learning.metrics]
# accuracy_weight = 0.6
# latency_weight = 0.2
# cost_weight = 0.1
# efficiency_weight = 0.1

[telemetry]
enabled = true
# gpu_metrics = false
# gpu_poll_interval_ms = 50

[traces]
enabled = false

[channel]
enabled = false
default_agent = "simple"

# [channel.telegram]
# bot_token = ""  # Or set TELEGRAM_BOT_TOKEN env var

# [channel.discord]
# bot_token = ""  # Or set DISCORD_BOT_TOKEN env var

# [channel.slack]
# bot_token = ""  # Or set SLACK_BOT_TOKEN env var

# [channel.webhook]
# url = ""

# [channel.whatsapp]
# access_token = ""      # Or set WHATSAPP_ACCESS_TOKEN env var
# phone_number_id = ""   # Or set WHATSAPP_PHONE_NUMBER_ID env var

# [channel.signal]
# api_url = ""            # signal-cli REST API URL
# phone_number = ""       # Or set SIGNAL_PHONE_NUMBER env var

# [channel.google_chat]
# webhook_url = ""        # Or set GOOGLE_CHAT_WEBHOOK_URL env var

# [channel.irc]
# server = ""
# port = 6667
# nick = ""
# use_tls = false

# [channel.teams]
# app_id = ""             # Or set TEAMS_APP_ID env var
# app_password = ""       # Or set TEAMS_APP_PASSWORD env var

# [channel.matrix]
# homeserver = ""         # Or set MATRIX_HOMESERVER env var
# access_token = ""       # Or set MATRIX_ACCESS_TOKEN env var

# [channel.mattermost]
# url = ""                # Or set MATTERMOST_URL env var
# token = ""              # Or set MATTERMOST_TOKEN env var

# [channel.feishu]
# app_id = ""             # Or set FEISHU_APP_ID env var
# app_secret = ""         # Or set FEISHU_APP_SECRET env var

# [channel.bluebubbles]
# url = ""                # Or set BLUEBUBBLES_URL env var
# password = ""           # Or set BLUEBUBBLES_PASSWORD env var

[security]
enabled = true
mode = "warn"
scan_input = true
scan_output = true
secret_scanner = true
pii_scanner = true
enforce_tool_confirmation = true
ssrf_protection = true
# rate_limit_enabled = false
# rate_limit_rpm = 60
# rate_limit_burst = 10

# [sandbox]
# enabled = false
# image = "openjarvis-sandbox:latest"
# timeout = 300
# max_concurrent = 5
# runtime = "docker"

# [scheduler]
# enabled = false
# poll_interval = 60
# db_path = ""                # Defaults to ~/.openjarvis/scheduler.db

# [channel.whatsapp_baileys]
# auth_dir = ""               # Defaults to ~/.openjarvis/whatsapp_auth
# assistant_name = "Jarvis"
# assistant_has_own_number = false
"""
    if host:
        import re as _re

        pattern = _re.escape(f"[engine.{engine}]") + r"\nhost = \"[^\"]*\""
        replacement = f'[engine.{engine}]\\nhost = "{host}"'
        result = _re.sub(pattern, replacement, result)
    return result


__all__ = [
    "A2AConfig",
    "AgentConfig",
    "AgentManagerConfig",
    "OperatorsConfig",
    "AgentLearningConfig",
    "BlueBubblesChannelConfig",
    "BrowserConfig",
    "CapabilitiesConfig",
    "ChannelConfig",
    "ConfigurationError",
    "DEFAULT_CONFIG_DIR",
    "DEFAULT_CONFIG_PATH",
    "DiscordChannelConfig",
    "DeepResearchConfig",
    "get_cache_dir",
    "get_config_dir",
    "get_config_path",
    "get_data_dir",
    "EmailChannelConfig",
    "EngineConfig",
    "FeishuChannelConfig",
    "GoogleChatChannelConfig",
    "GpuInfo",
    "HardwareInfo",
    "IRCChannelConfig",
    "IntelligenceConfig",
    "IntelligenceLearningConfig",
    "JarvisConfig",
    "LearningConfig",
    "LMStudioEngineConfig",
    "LlamaCppEngineConfig",
    "MCPConfig",
    "MLXEngineConfig",
    "MatrixChannelConfig",
    "MattermostChannelConfig",
    "MemoryConfig",
    "MetricsConfig",
    "OllamaEngineConfig",
    "OptimizeConfig",
    "RoutingLearningConfig",
    "SGLangEngineConfig",
    "SandboxConfig",
    "SchedulerConfig",
    "SecurityConfig",
    "ServerConfig",
    "SessionConfig",
    "SignalChannelConfig",
    "SlackChannelConfig",
    "SpeechConfig",
    "StorageConfig",
    "TeamsChannelConfig",
    "TelegramChannelConfig",
    "TelemetryConfig",
    "ToolsConfig",
    "TracesConfig",
    "VLLMEngineConfig",
    "WebChatChannelConfig",
    "WebhookChannelConfig",
    "WeatherToolConfig",
    "WhatsAppBaileysChannelConfig",
    "WhatsAppChannelConfig",
    "WorkflowConfig",
    "detect_hardware",
    "generate_default_toml",
    "generate_minimal_toml",
    "load_config",
    "recommend_engine",
    "recommend_model",
    "validate_config_key",
]


## ===== src/openjarvis/core/config.py : STAGE 1 =====
"""Configuration loading, hardware detection, and engine recommendation.

User configuration lives at ``~/.openjarvis/config.toml``.  ``load_config()``
detects hardware, fills sensible defaults, then overlays any user overrides
found in the TOML file.
"""

from __future__ import annotations

import functools
import os
import platform
import shutil
import subprocess
from dataclasses import dataclass, field
from pathlib import Path
from typing import TYPE_CHECKING, Any, Dict, List, Optional

if TYPE_CHECKING:
    # Only used by type-checkers (mypy/pyright) for the ``JarvisConfig.mining``
    # field annotation. The runtime import is deferred inside
    # ``_parse_mining_section()`` to break the import cycle:
    # ``mining/_stubs.py`` imports ``HardwareInfo`` from this module at its
    # top level.
    from openjarvis.mining._stubs import MiningConfig

try:
    import tomllib  # Python 3.11+
except ModuleNotFoundError:
    import tomli as tomllib  # type: ignore[no-redef]

# ---------------------------------------------------------------------------
# Hardware dataclasses
# ---------------------------------------------------------------------------

DEFAULT_CONFIG_DIR = Path.home() / ".openjarvis"
DEFAULT_CONFIG_PATH = DEFAULT_CONFIG_DIR / "config.toml"


def _ensure_config_dir() -> Path:
    """Ensure the config directory exists with restrictive permissions."""
    from openjarvis.security.file_utils import secure_mkdir

    return secure_mkdir(DEFAULT_CONFIG_DIR)


@dataclass(slots=True)
class GpuInfo:
    """Detected GPU metadata."""

    vendor: str = ""
    name: str = ""
    vram_gb: float = 0.0
    compute_capability: str = ""
    count: int = 0


@dataclass(slots=True)
class HardwareInfo:
    """Detected system hardware."""

    platform: str = ""
    cpu_brand: str = ""
    cpu_count: int = 0
    ram_gb: float = 0.0
    gpu: Optional[GpuInfo] = None


# ---------------------------------------------------------------------------
# Hardware detection helpers
# ---------------------------------------------------------------------------


def _run_cmd(cmd: list[str]) -> str:
    """Run a command and return stripped stdout, or empty string on failure."""
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=10,  # noqa: S603
        )
        return result.stdout.strip()
    except (FileNotFoundError, subprocess.TimeoutExpired, OSError):
        return ""


def _detect_nvidia_gpu() -> Optional[GpuInfo]:
    if not shutil.which("nvidia-smi"):
        return None
    raw = _run_cmd(
        [
            "nvidia-smi",
            "--query-gpu=name,memory.total,count,compute_cap",
            "--format=csv,noheader,nounits",
        ]
    )
    if not raw:
        return None
    try:
        first_line = raw.splitlines()[0]
        parts = [p.strip() for p in first_line.split(",")]
        name = parts[0]
        vram_mb = float(parts[1])
        count = int(parts[2])
        compute_capability = parts[3] if len(parts) > 3 else ""
        return GpuInfo(
            vendor="nvidia",
            name=name,
            vram_gb=round(vram_mb / 1024, 1),
            compute_capability=compute_capability,
            count=count,
        )
    except (IndexError, ValueError):
        return None


def _detect_amd_gpu() -> Optional[GpuInfo]:
    if not shutil.which("rocm-smi"):
        return None
    raw = _run_cmd(["rocm-smi", "--showproductname"])
    if not raw:
        return None
    name = raw.splitlines()[0] if raw else "AMD GPU"

    # Parse VRAM from rocm-smi --showmeminfo vram
    vram_gb = 0.0
    try:
        vram_raw = _run_cmd(["rocm-smi", "--showmeminfo", "vram"])
        for line in vram_raw.splitlines():
            if "Total Memory (B):" in line:
                vram_bytes = int(line.split(":")[-1].strip())
                vram_gb = round(vram_bytes / (1024**3), 1)
                break
    except (ValueError, IndexError):
        vram_gb = 0.0

    # Parse GPU count from rocm-smi --showallinfo
    count = 1
    try:
        allinfo_raw = _run_cmd(["rocm-smi", "--showallinfo"])
        import re

        gpu_ids = set(re.findall(r"GPU\[(\d+)\]", allinfo_raw))
        if gpu_ids:
            count = len(gpu_ids)
    except (ValueError, IndexError):
        count = 1

    return GpuInfo(vendor="amd", name=name, vram_gb=vram_gb, count=count)


def _detect_apple_gpu() -> Optional[GpuInfo]:
    if platform.system() != "Darwin":
        return None
    raw = _run_cmd(["system_profiler", "SPDisplaysDataType"])
    if "Apple" not in raw:
        return None
    # Rough extraction ΓÇö "Apple M2 Max" etc.
    ram_gb = _total_ram_gb()
    for line in raw.splitlines():
        line = line.strip()
        if "Chipset Model" in line:
            name = line.split(":")[-1].strip()
            return GpuInfo(vendor="apple", name=name, vram_gb=ram_gb, count=1)
    return GpuInfo(vendor="apple", name="Apple Silicon", vram_gb=ram_gb, count=1)


def _detect_cpu_brand() -> str:
    """Best-effort CPU brand string."""
    if platform.system() == "Darwin":
        brand = _run_cmd(["sysctl", "-n", "machdep.cpu.brand_string"])
        if brand:
            return brand
    cpuinfo = Path("/proc/cpuinfo")
    if cpuinfo.exists():
        try:
            for line in cpuinfo.read_text().splitlines():
                if line.startswith("model name"):
                    return line.split(":", 1)[1].strip()
        except OSError:
            pass
    return platform.processor() or "unknown"


def _total_ram_gb() -> float:
    try:
        if platform.system() == "Darwin":
            raw = _run_cmd(["sysctl", "-n", "hw.memsize"])
            return round(int(raw) / (1024**3), 1) if raw else 0.0
        meminfo = Path("/proc/meminfo")
        if meminfo.exists():
            for line in meminfo.read_text().splitlines():
                if line.startswith("MemTotal"):
                    kb = int(line.split()[1])
                    return round(kb / (1024**2), 1)
    except (OSError, ValueError):
        pass
    return 0.0


def detect_hardware() -> HardwareInfo:
    """Auto-detect hardware capabilities with graceful fallbacks."""
    gpu = _detect_nvidia_gpu() or _detect_amd_gpu() or _detect_apple_gpu()
    return HardwareInfo(
        platform=platform.system().lower(),
        cpu_brand=_detect_cpu_brand(),
        cpu_count=os.cpu_count() or 1,
        ram_gb=_total_ram_gb(),
        gpu=gpu,
    )


# ---------------------------------------------------------------------------
# Engine recommendation
# ---------------------------------------------------------------------------


def recommend_engine(hw: HardwareInfo) -> str:
    """Suggest the best inference engine for the detected hardware."""
    gpu = hw.gpu
    if gpu is None:
        return "llamacpp"
    if gpu.vendor == "apple":
        return "mlx"
    if gpu.vendor == "nvidia":
        # Datacenter cards (A100, H100, L40, etc.) ΓåÆ vllm; consumer ΓåÆ ollama
        datacenter_keywords = ("A100", "H100", "H200", "L40", "A10", "A30")
        if any(kw in gpu.name for kw in datacenter_keywords):
            return "vllm"
        return "ollama"
    if gpu.vendor == "amd":
        # Datacenter cards (MI300, MI325, MI350, MI355) ΓåÆ vllm; consumer ΓåÆ lemonade
        amd_datacenter_keywords = ("MI300", "MI325", "MI350", "MI355")
        if any(kw in gpu.name for kw in amd_datacenter_keywords):
            return "vllm"
        return "lemonade"
    return "llamacpp"


def _available_memory_gb(hw: HardwareInfo) -> float:
    """Return usable memory in GB for model loading."""
    gpu = hw.gpu
    if gpu and gpu.vram_gb > 0:
        return gpu.vram_gb * max(gpu.count, 1) * 0.9
    if hw.ram_gb > 0:
        return (hw.ram_gb - 4) * 0.8
    return 0.0


# Explicit tier table: (max_ram_gb, model_id).
# Walked in order ΓÇö first tier where available_gb <= max_ram is chosen.
# Uses Qwen3.5 MoE models ΓÇö better quality per GB than dense models since
# only a fraction of parameters are active per token.
_MODEL_TIERS = [
    (8, "qwen3.5:2b"),
    (16, "qwen3.5:4b"),
    (32, "qwen3.5:9b"),
    (64, "qwen3.5:27b"),
]
_MODEL_TIER_FALLBACK = "qwen3.5:27b"


def recommend_model(hw: HardwareInfo, engine: str) -> str:
    """Suggest the best Qwen3.5 model that fits the detected hardware.

    Uses an explicit tier table mapping available memory to model size.
    Falls back to scanning the full catalog if the tiered model is not
    compatible with the selected engine.
    """
    from openjarvis.intelligence.model_catalog import BUILTIN_MODELS

    available_gb = _available_memory_gb(hw)
    if available_gb <= 0:
        return ""

    # Build a lookup for quick engine-compatibility checks
    catalog = {spec.model_id: spec for spec in BUILTIN_MODELS}

    # Try explicit tier mapping first
    model_id = _MODEL_TIER_FALLBACK
    for max_ram, tier_model in _MODEL_TIERS:
        if available_gb <= max_ram:
            model_id = tier_model
            break

    spec = catalog.get(model_id)
    if spec and engine in spec.supported_engines:
        return model_id

    # Fallback: scan all Qwen3.5 models for engine compatibility
    candidates = [
        s
        for s in BUILTIN_MODELS
        if s.provider == "alibaba"
        and s.model_id.startswith("qwen3.5:")
        and engine in s.supported_engines
    ]
    candidates.sort(key=lambda s: s.parameter_count_b, reverse=True)
    for s in candidates:
        estimated_gb = s.parameter_count_b * 0.5 * 1.1
        if estimated_gb <= available_gb:
            return s.model_id

    return ""


def estimated_download_gb(parameter_count_b: float) -> float:
    """Estimate download size in GB for Q4_K_M quantized model."""
    return parameter_count_b * 0.5 * 1.1


# ---------------------------------------------------------------------------
# Configuration hierarchy
# ---------------------------------------------------------------------------


@dataclass(slots=True)
class OllamaEngineConfig:
    """Per-engine config for Ollama."""

    host: str = ""


@dataclass(slots=True)
class VLLMEngineConfig:
    """Per-engine config for vLLM."""

    host: str = "http://localhost:8000"


@dataclass(slots=True)
class SGLangEngineConfig:
    """Per-engine config for SGLang."""

    host: str = "http://localhost:30000"


@dataclass(slots=True)
class LlamaCppEngineConfig:
    """Per-engine config for llama.cpp."""

    host: str = "http://localhost:8080"
    binary_path: str = ""


@dataclass(slots=True)
class MLXEngineConfig:
    """Per-engine config for MLX."""

    host: str = "http://localhost:8080"


@dataclass(slots=True)
class LMStudioEngineConfig:
    """Per-engine config for LM Studio."""

    host: str = "http://localhost:1234"


@dataclass(slots=True)
class ExoEngineConfig:
    """Per-engine config for Exo."""

    host: str = "http://localhost:52415"


@dataclass(slots=True)
class NexaEngineConfig:
    """Per-engine config for Nexa."""

    host: str = "http://localhost:18181"
    device: str = ""


@dataclass(slots=True)
class UzuEngineConfig:
    """Per-engine config for Uzu."""

    host: str = "http://localhost:8000"


@dataclass(slots=True)
class AppleFmEngineConfig:
    """Per-engine config for Apple Foundation Models."""

    host: str = "http://localhost:8079"


@dataclass(slots=True)
class GemmaCppEngineConfig:
    """Per-engine config for gemma.cpp."""

    model_path: str = ""
    tokenizer_path: str = ""
    model_type: str = ""
    num_threads: int = 0


@dataclass(slots=True)
class LemonadeEngineConfig:
    """Per-engine config for Lemonade."""

    host: str = "http://localhost:8000"


@dataclass
class EngineConfig:
    """Inference engine settings with nested per-engine configs."""

    default: str = "ollama"
    ollama: OllamaEngineConfig = field(default_factory=OllamaEngineConfig)
    vllm: VLLMEngineConfig = field(default_factory=VLLMEngineConfig)
    sglang: SGLangEngineConfig = field(default_factory=SGLangEngineConfig)
    llamacpp: LlamaCppEngineConfig = field(default_factory=LlamaCppEngineConfig)
    mlx: MLXEngineConfig = field(default_factory=MLXEngineConfig)
    lmstudio: LMStudioEngineConfig = field(default_factory=LMStudioEngineConfig)
    exo: ExoEngineConfig = field(default_factory=ExoEngineConfig)
    nexa: NexaEngineConfig = field(default_factory=NexaEngineConfig)
    uzu: UzuEngineConfig = field(default_factory=UzuEngineConfig)
    apple_fm: AppleFmEngineConfig = field(default_factory=AppleFmEngineConfig)
    gemma_cpp: GemmaCppEngineConfig = field(default_factory=GemmaCppEngineConfig)
    lemonade: LemonadeEngineConfig = field(default_factory=LemonadeEngineConfig)

    # Backward-compat properties for old flat attribute names
    @property
    def ollama_host(self) -> str:
        """Deprecated: use ``engine.ollama.host``."""
        return self.ollama.host

    @ollama_host.setter
    def ollama_host(self, value: str) -> None:
        self.ollama.host = value

    @property
    def vllm_host(self) -> str:
        """Deprecated: use ``engine.vllm.host``."""
        return self.vllm.host

    @vllm_host.setter
    def vllm_host(self, value: str) -> None:
        self.vllm.host = value

    @property
    def llamacpp_host(self) -> str:
        """Deprecated: use ``engine.llamacpp.host``."""
        return self.llamacpp.host

    @llamacpp_host.setter
    def llamacpp_host(self, value: str) -> None:
        self.llamacpp.host = value

    @property
    def llamacpp_path(self) -> str:
        """Deprecated: use ``engine.llamacpp.binary_path``."""
        return self.llamacpp.binary_path

    @llamacpp_path.setter
    def llamacpp_path(self, value: str) -> None:
        self.llamacpp.binary_path = value

    @property
    def sglang_host(self) -> str:
        """Deprecated: use ``engine.sglang.host``."""
        return self.sglang.host

    @sglang_host.setter
    def sglang_host(self, value: str) -> None:
        self.sglang.host = value

    @property
    def mlx_host(self) -> str:
        """Deprecated: use ``engine.mlx.host``."""
        return self.mlx.host

    @mlx_host.setter
    def mlx_host(self, value: str) -> None:
        self.mlx.host = value

    @property
    def lmstudio_host(self) -> str:
        """Deprecated: use ``engine.lmstudio.host``."""
        return self.lmstudio.host

    @lmstudio_host.setter
    def lmstudio_host(self, value: str) -> None:
        self.lmstudio.host = value

    @property
    def exo_host(self) -> str:
        """Deprecated: use ``engine.exo.host``."""
        return self.exo.host

    @exo_host.setter
    def exo_host(self, value: str) -> None:
        self.exo.host = value

    @property
    def nexa_host(self) -> str:
        """Deprecated: use ``engine.nexa.host``."""
        return self.nexa.host

    @nexa_host.setter
    def nexa_host(self, value: str) -> None:
        self.nexa.host = value

    @property
    def uzu_host(self) -> str:
        """Deprecated: use ``engine.uzu.host``."""
        return self.uzu.host

    @uzu_host.setter
    def uzu_host(self, value: str) -> None:
        self.uzu.host = value

    @property
    def apple_fm_host(self) -> str:
        """Deprecated: use ``engine.apple_fm.host``."""
        return self.apple_fm.host

    @apple_fm_host.setter
    def apple_fm_host(self, value: str) -> None:
        self.apple_fm.host = value

    @property
    def lemonade_host(self) -> str:
        """Deprecated: use ``engine.lemonade.host``."""
        return self.lemonade.host

    @lemonade_host.setter
    def lemonade_host(self, value: str) -> None:
        self.lemonade.host = value


@dataclass(slots=True)
class IntelligenceConfig:
    """The model ΓÇö identity, paths, quantization, and generation defaults."""

    default_model: str = ""
    fallback_model: str = ""
    model_path: str = ""  # Local weights (HF repo, GGUF file, etc.)
    checkpoint_path: str = ""  # Checkpoint/adapter path
    quantization: str = "none"  # none, fp8, int8, int4, gguf_q4, gguf_q8
    preferred_engine: str = ""  # Override engine for this model (e.g., "vllm")
    provider: str = ""  # local, openai, anthropic, google
    # Generation defaults (overridable per-call)
    temperature: float = 0.7
    max_tokens: int = 1024
    top_p: float = 0.9
    top_k: int = 40
    repetition_penalty: float = 1.0
    stop_sequences: str = ""  # Comma-separated stop strings


@dataclass(slots=True)
class RoutingLearningConfig:
    """Routing sub-policy config within Learning."""

    policy: str = "heuristic"  # heuristic | learned
    min_samples: int = 5  # Min traces before trusting learned routing


@dataclass(slots=True)
class SFTConfig:
    """General-purpose SFT training config. Maps to [learning.intelligence.sft]."""

    model_name: str = "Qwen/Qwen3-1.7B"
    max_seq_length: int = 4096
    num_epochs: int = 3
    batch_size: int = 8
    learning_rate: float = 2e-5
    weight_decay: float = 0.01
    warmup_ratio: float = 0.1
    max_grad_norm: float = 1.0
    gradient_checkpointing: bool = True
    use_lora: bool = True
    lora_rank: int = 16
    lora_alpha: int = 32
    lora_dropout: float = 0.05
    target_modules: str = "q_proj,v_proj"  # comma-separated for TOML compat
    use_4bit: bool = False
    checkpoint_dir: str = "checkpoints/sft"
    min_pairs: int = 10
    agent_filter: str = ""


@dataclass(slots=True)
class GRPOConfig:
    """General-purpose GRPO training config. Maps to [learning.intelligence.grpo]."""

    model_name: str = "Qwen/Qwen3-1.7B"
    max_seq_length: int = 4096
    max_response_length: int = 2048
    num_epochs: int = 10
    batch_size: int = 16
    learning_rate: float = 1e-6
    max_grad_norm: float = 1.0
    gradient_checkpointing: bool = True
    num_samples_per_prompt: int = 8
    temperature: float = 1.0
    kl_coef: float = 0.0001
    clip_ratio: float = 0.2
    use_8bit_ref: bool = True
    checkpoint_dir: str = "checkpoints/grpo"
    save_every_n_epochs: int = 1
    keep_last_n: int = 3
    min_prompts: int = 10
    agent_filter: str = ""


@dataclass(slots=True)
class DSPyOptimizerConfig:
    """DSPy agent optimizer config. Maps to [learning.agent.dspy]."""

    optimizer: str = "BootstrapFewShotWithRandomSearch"
    task_lm: str = ""
    teacher_lm: str = ""
    max_bootstrapped_demos: int = 4
    max_labeled_demos: int = 4
    num_candidate_programs: int = 10
    max_rounds: int = 1
    optimize_system_prompt: bool = True
    optimize_few_shot: bool = True
    optimize_tool_descriptions: bool = True
    min_traces: int = 20
    metric_threshold: float = 0.7
    agent_filter: str = ""
    config_dir: str = ""


@dataclass(slots=True)
class GEPAOptimizerConfig:
    """GEPA agent optimizer config. Maps to [learning.agent.gepa]."""

    reflection_lm: str = ""
    max_metric_calls: int = 150
    population_size: int = 10
    optimize_system_prompt: bool = True
    optimize_tools: bool = True
    optimize_max_turns: bool = True
    optimize_temperature: bool = True
    min_traces: int = 20
    assessment_batch_size: int = 10
    agent_filter: str = ""
    config_dir: str = ""


@dataclass(slots=True)
class ACEOptimizerConfig:
    """ACE agent optimizer config. Maps to ``[learning.agent.ace]``.

    ACE (Agentic Context Engineering) evolves a *playbook* ΓÇö annotated
    natural-language strategies that get prepended to the agent's
    context ΓÇö using a Generator / Reflector / Curator triad. Unlike
    DSPy (few-shot bootstrapping) or GEPA (Pareto-evolutionary prompt
    mutation), ACE writes a textual playbook that the agent reads at
    inference time.

    See https://github.com/ace-agent/ace for the upstream reference.
    Install via ``pip install -e openjarvis[learning-ace]`` once the
    optional dep is available (ACE is not on PyPI as of v1.0.1; the
    extra installs from the upstream git repo).
    """

    # Models for ACE's three roles. Empty string = inherit from the
    # intelligence primitive's default cloud model.
    generator_model: str = ""
    reflector_model: str = ""
    curator_model: str = ""

    # Provider passed to ACE (``sambanova`` | ``together`` | ``openai``
    # | ``commonstack``). We default to ``openai`` since that's what
    # most OpenJarvis users have credentials for.
    api_provider: str = "openai"

    # Run parameters. Defaults mirror ACE's offline-mode quickstart.
    num_epochs: int = 1
    max_num_rounds: int = 3
    eval_steps: int = 100
    playbook_token_budget: int = 80_000
    max_tokens: int = 4_096

    # Where ACE writes intermediate playbooks + final_results.json.
    # Empty string defaults to ``~/.openjarvis/learning/ace/<task>/``.
    save_dir: str = ""
    task_name: str = "openjarvis"

    # Standard filter / threshold knobs shared with DSPy / GEPA.
    min_traces: int = 20
    agent_filter: str = ""
    config_dir: str = ""


@dataclass(slots=True)
class IntelligenceLearningConfig:
    """Intelligence sub-policy config within Learning."""

    policy: str = "none"  # none | sft | grpo
    sft: SFTConfig = field(default_factory=SFTConfig)
    grpo: GRPOConfig = field(default_factory=GRPOConfig)


@dataclass(slots=True)
class AgentLearningConfig:
    """Agent sub-policy config within Learning."""

    policy: str = "none"  # none | dspy | gepa | ace
    dspy: DSPyOptimizerConfig = field(default_factory=DSPyOptimizerConfig)
    gepa: GEPAOptimizerConfig = field(default_factory=GEPAOptimizerConfig)
    ace: ACEOptimizerConfig = field(default_factory=ACEOptimizerConfig)


@dataclass(slots=True)
class SkillsLearningConfig:
    """Configuration for the skills learning loop (Plan 2A)."""

    auto_optimize: bool = False  # opt in via config
    optimizer: str = "dspy"  # "dspy" or "gepa"
    min_traces_per_skill: int = 20
    optimization_interval_seconds: int = 86400
    overlay_dir: str = "~/.openjarvis/learning/skills/"


@dataclass(slots=True)
class MetricsConfig:
    """Reward / optimization metric weights."""

    accuracy_weight: float = 0.6
    latency_weight: float = 0.2
    cost_weight: float = 0.1
    efficiency_weight: float = 0.1


@dataclass(slots=True)
class SpecSearchCompositeRewardConfig:
    """Composite reward weights for Intelligence-edit training (paper Eq. 1).

    R(q, y) = alpha * R_acc - beta * E_hat - gamma * L_hat - delta * C_hat
    """

    alpha: float = 0.5
    beta: float = 0.1
    gamma: float = 0.1
    delta: float = 0.3


@dataclass(slots=True)
class SpecSearchLearningConfig:
    """LLM-guided spec search config (paper ┬º3.3, Algorithm 1).

    Maps to ``[learning.spec_search]`` and is consumed by
    ``SpecSearchOrchestrator.from_config`` and ``SpecSearchLoop``.
    """

    enabled: bool = False
    teacher_model: str = "claude-opus-4-6"
    teacher_engine: str = "cloud"  # registry key for the cloud engine
    autonomy_mode: str = "tiered"  # auto | tiered | manual

    # Per-session bounds (one diagnose/plan/execute pass)
    min_traces: int = 20
    max_cost_per_session_usd: float = 5.0
    max_tool_calls_per_diagnosis: int = 30

    # Multi-session loop (paper Algorithm 1)
    stagnation_k: int = 5
    max_total_cost_usd: float = 50.0
    stagnation_eps: float = 0.001  # gate-score delta below this counts as no progress

    # Gate (GateOK predicate)
    max_regression: float = 0.01  # paper default: epsilon = 1%
    min_improvement: float = 0.0
    benchmark_subsample_size: int = 50
    benchmark_version: str = "personal_v1"

    # Composite reward (only used when an Intelligence edit triggers training)
    composite_reward: SpecSearchCompositeRewardConfig = field(
        default_factory=SpecSearchCompositeRewardConfig,
    )


@dataclass
class LearningConfig:
    """Learning system settings with per-primitive sub-policies."""

    enabled: bool = False
    update_interval: int = 100
    auto_update: bool = False
    routing: RoutingLearningConfig = field(default_factory=RoutingLearningConfig)
    intelligence: IntelligenceLearningConfig = field(
        default_factory=IntelligenceLearningConfig,
    )
    agent: AgentLearningConfig = field(default_factory=AgentLearningConfig)
    skills: SkillsLearningConfig = field(default_factory=SkillsLearningConfig)
    spec_search: SpecSearchLearningConfig = field(
        default_factory=SpecSearchLearningConfig,
    )
    metrics: MetricsConfig = field(default_factory=MetricsConfig)

    # Training pipeline
    training_enabled: bool = False
    training_schedule: str = ""
    min_improvement: float = 0.02

    # Backward-compat properties for old flat field names
    @property
    def default_policy(self) -> str:
        """Deprecated: use ``learning.routing.policy``."""
        return self.routing.policy

    @default_policy.setter
    def default_policy(self, value: str) -> None:
        self.routing.policy = value

    @property
    def intelligence_policy(self) -> str:
        """Deprecated: use ``learning.intelligence.policy``."""
        return self.intelligence.policy

    @intelligence_policy.setter
    def intelligence_policy(self, value: str) -> None:
        self.intelligence.policy = value

    @property
    def agent_policy(self) -> str:
        """Deprecated: use ``learning.agent.policy``."""
        return self.agent.policy

    @agent_policy.setter
    def agent_policy(self, value: str) -> None:
        self.agent.policy = value

    @property
    def reward_weights(self) -> str:
        """Deprecated: use ``learning.metrics.*``."""
        parts = []
        m = self.metrics
        if m.latency_weight:
            parts.append(f"latency={m.latency_weight}")
        if m.cost_weight:
            parts.append(f"cost={m.cost_weight}")
        if m.efficiency_weight:
            parts.append(f"efficiency={m.efficiency_weight}")
        if m.accuracy_weight:
            parts.append(f"accuracy={m.accuracy_weight}")
        return ",".join(parts)

    @reward_weights.setter
    def reward_weights(self, value: str) -> None:
        if not value:
            return
        for part in value.split(","):
            if "=" not in part:
                continue
            key, val = part.strip().split("=", 1)
            key = key.strip()
            fval = float(val.strip())
            if key == "accuracy":
                self.metrics.accuracy_weight = fval
            elif key == "latency":
                self.metrics.latency_weight = fval
            elif key == "cost":
                self.metrics.cost_weight = fval
            elif key == "efficiency":
                self.metrics.efficiency_weight = fval


@dataclass(slots=True)
class StorageConfig:
    """Storage (memory) backend settings."""

    default_backend: str = "sqlite"
    db_path: str = str(DEFAULT_CONFIG_DIR / "memory.db")
    context_top_k: int = 5
    context_min_score: float = 0.0
    context_max_tokens: int = 2048
    chunk_size: int = 512
    chunk_overlap: int = 64


# Backward-compatibility alias
MemoryConfig = StorageConfig


@dataclass(slots=True)
class MCPConfig:
    """MCP (Model Context Protocol) settings."""

    enabled: bool = True
    servers: str = ""  # JSON list of MCP server configs


@dataclass(slots=True)
class BrowserConfig:
    """Browser automation settings (Playwright)."""

    headless: bool = True
    timeout_ms: int = 30000
    viewport_width: int = 1280
    viewport_height: int = 720


@dataclass(slots=True)
class ToolsConfig:
    """Tools primitive settings ΓÇö wraps storage and MCP configuration."""

    storage: StorageConfig = field(default_factory=StorageConfig)
    mcp: MCPConfig = field(default_factory=MCPConfig)
    browser: BrowserConfig = field(default_factory=BrowserConfig)
    enabled: str = ""  # comma-separated default tools


@dataclass
class AgentConfig:
    """Agent harness settings ΓÇö orchestration, tools, system prompt."""

    default_agent: str = "simple"
    max_turns: int = 10
    tools: str = ""  # comma-separated tool names
    objective: str = ""  # concise purpose for routing/learning/docs
    system_prompt: str = ""  # inline system prompt (takes precedence if set)
    system_prompt_path: str = ""  # path to system prompt file (.txt, .md)
    context_from_memory: bool = True  # inject relevant memory context into prompts
    default_system_prompt: str = (
        "You are a helpful AI assistant running locally on the user's own "
        "hardware through OpenJarvis. You are not a cloud service. Respond "
        "helpfully, concisely, and accurately."
    )

    # Backward-compat property for old field name
    @property
    def default_tools(self) -> str:
        """Deprecated: use ``agent.tools``."""
        return self.tools

    @default_tools.setter
    def default_tools(self, value: str) -> None:
        self.tools = value


@dataclass(slots=True)
class ServerConfig:
    """API server settings."""

    host: str = "127.0.0.1"
    port: int = 8000
    agent: str = "orchestrator"
    model: str = ""
    workers: int = 1
    cors_origins: list = field(
        default_factory=lambda: [
            "http://localhost:3000",
            "http://localhost:5173",
            "http://127.0.0.1:3000",
            "http://127.0.0.1:5173",
            # Tauri 2 production webview origins.
            # macOS / Linux / iOS use the custom scheme; Windows /
            # Android use http(s)://tauri.localhost. All three must
            # be allowed so the desktop app's chat-completions stream
            # is not blocked by CORS in production builds.
            "tauri://localhost",
            "http://tauri.localhost",
            "https://tauri.localhost",
        ]
    )


@dataclass(slots=True)
class TelemetryConfig:
    """Telemetry persistence settings."""

    enabled: bool = True
    db_path: str = str(DEFAULT_CONFIG_DIR / "telemetry.db")
    gpu_metrics: bool = False
    gpu_poll_interval_ms: int = 50
    energy_vendor: str = ""  # auto-detect or force "nvidia"/"amd"/"apple"/"cpu_rapl"
    warmup_samples: int = 0
    steady_state_window: int = 5
    steady_state_threshold: float = 0.05


@dataclass(slots=True)
class AnalyticsConfig:
    """External anonymous usage analytics (PostHog).

    Separate concern from :class:`TelemetryConfig`, which stores local
    FLOPs/energy/inference metrics in SQLite. This controls anonymized
    usage events sent to the OpenJarvis team's PostHog instance to
    measure setup success, retention, feature usage, and churn.

    No chat content, prompts, model outputs, file paths, emails, IPs,
    or hardware identifiers are ever sent. See ``docs/telemetry.md``.
    """

    enabled: bool = True
    host: str = "https://34.231.106.201.sslip.io"
    key: str = "phc_ysKu72QaxzYNmDpHFcesD2ZZAe68zkdWJEKoYYkc5e3n"
    anon_id_path: str = str(DEFAULT_CONFIG_DIR / "anon_id")
    flush_interval_seconds: int = 30
    flush_at_size: int = 100


@dataclass(slots=True)
class TracesConfig:
    """Trace system settings."""

    enabled: bool = True
    db_path: str = str(DEFAULT_CONFIG_DIR / "traces.db")


@dataclass(slots=True)
class TelegramChannelConfig:
    """Per-channel config for Telegram."""

    bot_token: str = ""
    allowed_chat_ids: str = ""
    parse_mode: str = "Markdown"


@dataclass(slots=True)
class DiscordChannelConfig:
    """Per-channel config for Discord."""

    bot_token: str = ""


@dataclass(slots=True)
class SlackChannelConfig:
    """Per-channel config for Slack."""

    bot_token: str = ""
    app_token: str = ""


@dataclass(slots=True)
class WebhookChannelConfig:
    """Per-channel config for generic webhooks."""

    url: str = ""
    secret: str = ""
    method: str = "POST"


@dataclass(slots=True)
class EmailChannelConfig:
    """Per-channel config for email (SMTP/IMAP)."""

    smtp_host: str = ""
    smtp_port: int = 587
    imap_host: str = ""
    imap_port: int = 993
    username: str = ""
    password: str = ""
    use_tls: bool = True


@dataclass(slots=True)
class WhatsAppChannelConfig:
    """Per-channel config for WhatsApp Cloud API."""

    access_token: str = ""
    phone_number_id: str = ""


@dataclass(slots=True)
class SignalChannelConfig:
    """Per-channel config for Signal (via signal-cli REST API)."""

    api_url: str = ""
    phone_number: str = ""


@dataclass(slots=True)
class GoogleChatChannelConfig:
    """Per-channel config for Google Chat webhooks."""

    webhook_url: str = ""


@dataclass(slots=True)
class IRCChannelConfig:
    """Per-channel config for IRC."""

    server: str = ""
    port: int = 6667
    nick: str = ""
    password: str = ""
    use_tls: bool = False


@dataclass(slots=True)
class WebChatChannelConfig:
    """Per-channel config for in-memory webchat."""

    pass


@dataclass(slots=True)
class TeamsChannelConfig:
    """Per-channel config for Microsoft Teams (Bot Framework)."""

    app_id: str = ""
    app_password: str = ""
    service_url: str = ""


@dataclass(slots=True)
class MatrixChannelConfig:
    """Per-channel config for Matrix."""

    homeserver: str = ""
    access_token: str = ""


@dataclass(slots=True)
class MattermostChannelConfig:
    """Per-channel config for Mattermost."""

    url: str = ""
    token: str = ""


@dataclass(slots=True)
class FeishuChannelConfig:
    """Per-channel config for Feishu (Lark)."""

    app_id: str = ""
    app_secret: str = ""


@dataclass(slots=True)
class BlueBubblesChannelConfig:
    """Per-channel config for BlueBubbles (iMessage bridge)."""

    url: str = ""
    password: str = ""


@dataclass(slots=True)
class WhatsAppBaileysChannelConfig:
    """Per-channel config for WhatsApp via Baileys protocol."""

    auth_dir: str = ""  # Defaults to ~/.openjarvis/whatsapp_auth
    assistant_name: str = "Jarvis"
    assistant_has_own_number: bool = False


@dataclass
class ChannelConfig:
    """Channel messaging settings."""

    enabled: bool = False
    default_channel: str = ""
    default_agent: str = "simple"
    telegram: TelegramChannelConfig = field(default_factory=TelegramChannelConfig)
    discord: DiscordChannelConfig = field(default_factory=DiscordChannelConfig)
    slack: SlackChannelConfig = field(default_factory=SlackChannelConfig)
    webhook: WebhookChannelConfig = field(default_factory=WebhookChannelConfig)
    email: EmailChannelConfig = field(default_factory=EmailChannelConfig)
    whatsapp: WhatsAppChannelConfig = field(default_factory=WhatsAppChannelConfig)
    signal: SignalChannelConfig = field(default_factory=SignalChannelConfig)
    google_chat: GoogleChatChannelConfig = field(
        default_factory=GoogleChatChannelConfig,
    )
    irc: IRCChannelConfig = field(default_factory=IRCChannelConfig)
    webchat: WebChatChannelConfig = field(default_factory=WebChatChannelConfig)
    teams: TeamsChannelConfig = field(default_factory=TeamsChannelConfig)
    matrix: MatrixChannelConfig = field(default_factory=MatrixChannelConfig)
    mattermost: MattermostChannelConfig = field(default_factory=MattermostChannelConfig)
    feishu: FeishuChannelConfig = field(default_factory=FeishuChannelConfig)
    bluebubbles: BlueBubblesChannelConfig = field(
        default_factory=BlueBubblesChannelConfig,
    )
    whatsapp_baileys: WhatsAppBaileysChannelConfig = field(
        default_factory=WhatsAppBaileysChannelConfig,
    )


@dataclass(slots=True)
class CapabilitiesConfig:
    """RBAC capability system settings."""

    enabled: bool = False
    policy_path: str = ""


@dataclass(slots=True)
class SecurityConfig:
    """Security guardrails settings."""

    enabled: bool = True
    scan_input: bool = True
    scan_output: bool = True
    mode: str = "redact"  # "redact" | "warn" | "block"
    secret_scanner: bool = True
    pii_scanner: bool = True
    audit_log_path: str = str(DEFAULT_CONFIG_DIR / "audit.db")
    enforce_tool_confirmation: bool = True
    merkle_audit: bool = True
    signing_key_path: str = ""
    ssrf_protection: bool = True
    rate_limit_enabled: bool = True
    rate_limit_rpm: int = 60
    rate_limit_burst: int = 10
    local_engine_bypass: bool = False
    local_tool_bypass: bool = False
    profile: str = ""
    vault_key_path: str = str(DEFAULT_CONFIG_DIR / ".vault_key")
    capabilities: CapabilitiesConfig = field(default_factory=CapabilitiesConfig)


# ---------------------------------------------------------------------------
# Security profile presets
# ---------------------------------------------------------------------------

_SECURITY_PROFILES: Dict[str, Dict[str, Dict[str, Any]]] = {
    "personal": {
        "security": {
            "mode": "redact",
            "rate_limit_enabled": True,
            "local_engine_bypass": False,
            "local_tool_bypass": False,
        },
        "server": {
            "host": "127.0.0.1",
        },
    },
    "shared": {
        "security": {
            "mode": "redact",
            "rate_limit_enabled": True,
            "local_engine_bypass": False,
            "local_tool_bypass": False,
        },
        "server": {
            "host": "127.0.0.1",
        },
    },
    "server": {
        "security": {
            "mode": "block",
            "rate_limit_enabled": True,
            "rate_limit_rpm": 30,
            "rate_limit_burst": 5,
            "local_engine_bypass": False,
            "local_tool_bypass": False,
        },
        "server": {
            "host": "0.0.0.0",
        },
    },
}


def apply_security_profile(
    security_cfg: "SecurityConfig",
    server_cfg: "ServerConfig | None",
    *,
    overrides: "set[str] | None" = None,
) -> None:
    """Expand a named security profile into config fields.

    Fields in *overrides* (explicitly set by the user in TOML) are
    not overwritten by the profile.
    """
    profile = security_cfg.profile
    if not profile:
        return

    if profile not in _SECURITY_PROFILES:
        raise ValueError(
            f"Unknown security profile '{profile}'. "
            f"Valid profiles: {', '.join(_SECURITY_PROFILES)}"
        )

    _overrides = overrides or set()
    pdef = _SECURITY_PROFILES[profile]

    for key, value in pdef.get("security", {}).items():
        if key not in _overrides and hasattr(security_cfg, key):
            setattr(security_cfg, key, value)

    if server_cfg is not None:
        for key, value in pdef.get("server", {}).items():
            if key not in _overrides and hasattr(server_cfg, key):
                setattr(server_cfg, key, value)


@dataclass(slots=True)
class SandboxConfig:
    """Container sandbox settings."""

    enabled: bool = False
    image: str = "openjarvis-sandbox:latest"
    timeout: int = 300
    workspace: str = ""
    mount_allowlist_path: str = ""
    max_concurrent: int = 5
    runtime: str = "docker"
    wasm_fuel_limit: int = 1_000_000
    wasm_memory_limit_mb: int = 256


@dataclass(slots=True)
class SchedulerConfig:
    """Task scheduler settings."""

    enabled: bool = False
    poll_interval: int = 60
    db_path: str = ""  # Defaults to ~/.openjarvis/scheduler.db


@dataclass(slots=True)
class WorkflowConfig:
    """Workflow engine settings."""

    enabled: bool = False
    max_parallel: int = 4
    default_node_timeout: int = 300


@dataclass(slots=True)
class SessionConfig:
    """Cross-channel session settings."""

    enabled: bool = False
    max_age_hours: float = 24.0
    consolidation_threshold: int = 100
    db_path: str = str(DEFAULT_CONFIG_DIR / "sessions.db")


@dataclass(slots=True)
class A2AConfig:
    """Agent-to-Agent protocol settings."""

    enabled: bool = False


@dataclass(slots=True)
class OperatorsConfig:
    """Operator lifecycle settings."""

    enabled: bool = False
    manifests_dir: str = "~/.openjarvis/operators"
    auto_activate: str = ""  # Comma-separated operator IDs


@dataclass(slots=True)
class SpeechConfig:
    """Speech-to-text settings."""

    backend: str = "auto"  # "auto", "faster-whisper", "openai", "deepgram"
    model: str = "base"  # Whisper model size: tiny, base, small, medium, large-v3
    language: str = ""  # Empty = auto-detect
    device: str = "auto"  # "auto", "cpu", "cuda"
    compute_type: str = "float16"  # "float16", "int8", "float32"


@dataclass(slots=True)
class OptimizeConfig:
    """Configuration optimization settings."""

    max_trials: int = 20
    early_stop_patience: int = 5
    optimizer_model: str = "claude-sonnet-4-6"
    optimizer_provider: str = "anthropic"
    benchmark: str = ""
    max_samples: int = 50
    judge_model: str = "gpt-5-mini-2025-08-07"
    db_path: str = str(DEFAULT_CONFIG_DIR / "optimize.db")


@dataclass(slots=True)
class AgentManagerConfig:
    """Persistent agent manager settings."""

    enabled: bool = True
    db_path: str = str(DEFAULT_CONFIG_DIR / "agents.db")


@dataclass(slots=True)
class MemoryFilesConfig:
    """Persistent memory-file paths and nudge settings."""

    soul_path: str = "~/.openjarvis/SOUL.md"
    memory_path: str = "~/.openjarvis/MEMORY.md"
    user_path: str = "~/.openjarvis/USER.md"
    nudge_interval: int = 10


@dataclass(slots=True)
class SystemPromptConfig:
    """Limits and strategy for system-prompt assembly."""

    soul_max_chars: int = 4000
    memory_max_chars: int = 2500
    user_max_chars: int = 1500
    skill_desc_max_chars: int = 60
    truncation_strategy: str = "head_tail"


@dataclass(slots=True)
class CompressionConfig:
    """Configuration for context compression."""

    enabled: bool = True
    threshold: float = 0.50
    strategy: str = "session_consolidation"


@dataclass(slots=True)
class SkillSourceConfig:
    """Configuration for a single skill source (Hermes, OpenClaw, GitHub)."""

    source: str = ""  # "hermes", "openclaw", or "github"
    url: str = ""  # required when source = "github"
    filter: Dict[str, Any] = field(default_factory=dict)
    auto_update: bool = False


@dataclass(slots=True)
class SkillsConfig:
    """Configuration for agent-authored procedural skills."""

    enabled: bool = True
    skills_dir: str = "~/.openjarvis/skills/"
    active: str = "*"
    auto_discover: bool = True
    auto_sync: bool = False
    nudge_interval: int = 15
    index_repo: str = "https://github.com/openjarvis/skill-index.git"
    index_dir: str = "~/.openjarvis/skill-index/"
    max_depth: int = 5
    sandbox_dangerous: bool = True
    sources: List[SkillSourceConfig] = field(default_factory=list)


@dataclass
class DigestSectionConfig:
    """Configuration for a single digest section."""

    sources: List[str] = field(default_factory=list)
    max_items: int = 10
    priority_contacts: List[str] = field(default_factory=list)


@dataclass
class DigestConfig:
    """Configuration for the morning digest feature."""

    enabled: bool = False
    schedule: str = "0 6 * * *"
    timezone: str = "America/Los_Angeles"
    persona: str = "jarvis"
    sections: List[str] = field(
        default_factory=lambda: ["messages", "calendar", "health", "world"]
    )
    optional_sections: List[str] = field(
        default_factory=lambda: ["github", "financial", "music", "fitness"]
    )
    honorific: str = "sir"
    voice_id: str = ""
    voice_speed: float = 1.0
    tts_backend: str = "cartesia"
    messages: DigestSectionConfig = field(
        default_factory=lambda: DigestSectionConfig(
            sources=["gmail", "slack", "google_tasks"]
        )
    )
    calendar: DigestSectionConfig = field(
        default_factory=lambda: DigestSectionConfig(sources=["gcalendar"])
    )
    health: DigestSectionConfig = field(
        default_factory=lambda: DigestSectionConfig(sources=["oura", "apple_health"])
    )
    world: DigestSectionConfig = field(
        default_factory=lambda: DigestSectionConfig(sources=[])
    )


@dataclass
class JarvisConfig:
    """Top-level configuration for OpenJarvis."""

    installed_at: str = ""
    installer_version: str = ""
    hardware: HardwareInfo = field(default_factory=HardwareInfo)
    engine: EngineConfig = field(default_factory=EngineConfig)
    intelligence: IntelligenceConfig = field(default_factory=IntelligenceConfig)
    learning: LearningConfig = field(default_factory=LearningConfig)
    tools: ToolsConfig = field(default_factory=ToolsConfig)
    agent: AgentConfig = field(default_factory=AgentConfig)
    server: ServerConfig = field(default_factory=ServerConfig)
    telemetry: TelemetryConfig = field(default_factory=TelemetryConfig)
    analytics: AnalyticsConfig = field(default_factory=AnalyticsConfig)
    traces: TracesConfig = field(default_factory=TracesConfig)
    channel: ChannelConfig = field(default_factory=ChannelConfig)
    security: SecurityConfig = field(default_factory=SecurityConfig)
    sandbox: SandboxConfig = field(default_factory=SandboxConfig)
    scheduler: SchedulerConfig = field(default_factory=SchedulerConfig)
    workflow: WorkflowConfig = field(default_factory=WorkflowConfig)
    sessions: SessionConfig = field(default_factory=SessionConfig)
    a2a: A2AConfig = field(default_factory=A2AConfig)
    operators: OperatorsConfig = field(default_factory=OperatorsConfig)
    speech: SpeechConfig = field(default_factory=SpeechConfig)
    optimize: OptimizeConfig = field(default_factory=OptimizeConfig)
    agent_manager: AgentManagerConfig = field(default_factory=AgentManagerConfig)
    memory_files: MemoryFilesConfig = field(default_factory=MemoryFilesConfig)
    system_prompt: SystemPromptConfig = field(default_factory=SystemPromptConfig)
    compression: CompressionConfig = field(default_factory=CompressionConfig)
    skills: SkillsConfig = field(default_factory=SkillsConfig)
    digest: DigestConfig = field(default_factory=DigestConfig)
    mining: Optional["MiningConfig"] = None

    @property
    def memory(self) -> StorageConfig:
        """Backward-compatible accessor ΓÇö canonical location is tools.storage."""
        return self.tools.storage

    @memory.setter
    def memory(self, value: StorageConfig) -> None:
        """Backward-compatible setter."""
        self.tools.storage = value


# ---------------------------------------------------------------------------
# Config key validation
# ---------------------------------------------------------------------------

# Sections that users may set via ``jarvis config set``.
# ``hardware`` is auto-detected and not user-settable.
_SETTABLE_SECTIONS = frozenset(JarvisConfig.__dataclass_fields__.keys()) - {
    "hardware",
    "mining",
}


def validate_config_key(dotted_key: str) -> type:
    """Validate a dotted config key and return the leaf field's Python type.

    Raises :class:`ValueError` when the key does not map to a known field.
    The function walks the ``JarvisConfig`` dataclass hierarchy using
    ``dataclasses.fields()``.

    Examples::

        validate_config_key("engine.ollama.host")      # -> str
        validate_config_key("intelligence.temperature") # -> float
    """
    from dataclasses import fields as dc_fields

    parts = dotted_key.split(".")
    if len(parts) < 2:
        raise ValueError(
            f"Config key must have at least two segments (e.g. engine.default), "
            f"got: {dotted_key!r}"
        )

    if parts[0] not in _SETTABLE_SECTIONS:
        raise ValueError(
            f"Unknown config key: {dotted_key!r} "
            f"(valid top-level sections: {sorted(_SETTABLE_SECTIONS)})"
        )

    # Walk the dataclass tree
    current_cls = JarvisConfig
    for i, part in enumerate(parts):
        field_map = {f.name: f for f in dc_fields(current_cls)}
        if part not in field_map:
            path_so_far = ".".join(parts[: i + 1])
            raise ValueError(
                f"Unknown config key: {dotted_key!r} "
                f"(no field {part!r} at {path_so_far}; "
                f"valid fields: {sorted(field_map.keys())})"
            )
        fld = field_map[part]
        # Resolve the type ΓÇö unwrap Optional, etc.
        fld_type = fld.type
        if isinstance(fld_type, str):
            # Evaluate forward references in the config module namespace
            import openjarvis.core.config as _cfg_mod

            fld_type = eval(fld_type, vars(_cfg_mod))  # noqa: S307

        if i == len(parts) - 1:
            # Leaf ΓÇö return the primitive type
            return fld_type
        else:
            # Must be a nested dataclass
            if not hasattr(fld_type, "__dataclass_fields__"):
                path_so_far = ".".join(parts[: i + 1])
                raise ValueError(
                    f"Unknown config key: {dotted_key!r} "
                    f"({path_so_far} is a leaf of type {fld_type.__name__}, "
                    f"not a section)"
                )
            current_cls = fld_type

    # Should not reach here, but satisfy type checker
    raise ValueError(f"Unknown config key: {dotted_key!r}")


# ---------------------------------------------------------------------------
# TOML loading
# ---------------------------------------------------------------------------


def _apply_toml_section(target: Any, section: Dict[str, Any]) -> None:
    """Overlay TOML key/value pairs onto a dataclass instance.

    Recursively handles nested dicts when the target attribute is itself
    a dataclass.  Normalises TOML arrays to comma-separated strings ΓÇö both
    for dataclass fields annotated as ``str`` and for backward-compat
    property setters that expect string input.
    """
    for key, value in section.items():
        if hasattr(target, key):
            if isinstance(value, dict):
                nested = getattr(target, key)
                if hasattr(nested, "__dataclass_fields__"):
                    _apply_toml_section(nested, value)
                else:
                    setattr(target, key, value)
            else:
                # Normalise TOML arrays ΓåÆ comma-separated string.
                # Covers both real dataclass fields and backward-compat
                # property setters (e.g. reward_weights, default_tools).
                if isinstance(value, list):
                    is_str_field = False
                    if hasattr(target, "__dataclass_fields__"):
                        field_obj = target.__dataclass_fields__.get(key)
                        if field_obj is not None and field_obj.type in ("str", str):
                            is_str_field = True
                        elif field_obj is None:
                            # Property, not a real field ΓÇö normalise to string
                            is_str_field = True
                    if is_str_field:
                        value = ",".join(str(v) for v in value)
                setattr(target, key, value)


def _migrate_toml_data(data: Dict[str, Any], cfg: "JarvisConfig") -> None:
    """Migrate old-format TOML keys to new structure in-place.

    Handles cross-section moves that can't be solved by backward-compat
    properties alone (e.g. ``agent.temperature`` ΓåÆ ``intelligence.temperature``).
    """
    # agent.temperature / agent.max_tokens ΓåÆ intelligence.*
    if "agent" in data:
        agent_data = data["agent"]
        intel_data = data.setdefault("intelligence", {})
        for moved_key in ("temperature", "max_tokens"):
            if moved_key in agent_data:
                intel_data.setdefault(moved_key, agent_data.pop(moved_key))

    # context_injection from memory / tools.storage ΓåÆ agent.context_from_memory
    for src_section in ("memory",):
        src = data.get(src_section, {})
        if isinstance(src, dict) and "context_injection" in src:
            data.setdefault("agent", {}).setdefault(
                "context_from_memory",
                src.pop("context_injection"),
            )

    if "tools" in data:
        tools_data = data["tools"]
        if isinstance(tools_data, dict):
            storage_sub = tools_data.get("storage", {})
            if isinstance(storage_sub, dict) and "context_injection" in storage_sub:
                data.setdefault("agent", {}).setdefault(
                    "context_from_memory",
                    storage_sub.pop("context_injection"),
                )


def _parse_mining_section(data: dict) -> Optional["MiningConfig"]:
    """Parse the ``[mining]`` TOML section into a ``MiningConfig``.

    Returns None if the section is absent. Resolves the ``submit_target``
    string into a ``SoloTarget`` or ``PoolTarget`` tagged union.
    """
    if "mining" not in data:
        return None

    # Lazy runtime import to break the import cycle: ``mining/_stubs.py``
    # imports ``HardwareInfo`` from this module at its top level. By the
    # time ``_parse_mining_section`` is called, ``core.config`` is already
    # fully initialized in ``sys.modules``, so the cycle is harmless.
    from openjarvis.mining._stubs import MiningConfig, PoolTarget, SoloTarget

    section = data["mining"]
    extra = section.get("extra", {}) or {}

    target_str = section.get("submit_target", "solo")
    submit_target: Any
    if target_str == "solo":
        submit_target = SoloTarget(
            pearld_rpc_url=extra.get("pearld_rpc_url", "http://localhost:44107")
        )
    elif isinstance(target_str, str) and target_str.startswith("pool:"):
        submit_target = PoolTarget(url=target_str[len("pool:") :])
    else:
        raise ValueError(
            f"[mining].submit_target must be 'solo' or 'pool:<url>', got {target_str!r}"
        )

    return MiningConfig(
        provider=section["provider"],
        wallet_address=section["wallet_address"],
        submit_target=submit_target,
        fee_bps=int(section.get("fee_bps", 0)),
        fee_payout_address=section.get("fee_payout_address") or None,
        extra={k: v for k, v in extra.items()},
    )


@functools.lru_cache(maxsize=1)
def load_config(path: Optional[Path] = None) -> JarvisConfig:
    """Detect hardware, build defaults, overlay TOML overrides.

    Parameters
    ----------
    path:
        Explicit config file. If not set, uses ``OPENJARVIS_CONFIG`` when set,
        otherwise ``~/.openjarvis/config.toml``.
    """
    _ensure_config_dir()
    hw = detect_hardware()
    cfg = JarvisConfig(hardware=hw)
    cfg.engine.default = recommend_engine(hw)

    if path is not None:
        config_path = Path(path)
    elif os.environ.get("OPENJARVIS_CONFIG"):
        config_path = Path(os.environ["OPENJARVIS_CONFIG"]).expanduser().resolve()
    else:
        config_path = DEFAULT_CONFIG_PATH
    if config_path.exists():
        with open(config_path, "rb") as fh:
            data = tomllib.load(fh)

        # Run backward-compat migrations before applying
        _migrate_toml_data(data, cfg)

        # All top-level sections ΓÇö recursive _apply_toml_section handles
        # nested sub-configs (engine.ollama, learning.routing, channel.*, etc.)
        top_sections = (
            "engine",
            "intelligence",
            "learning",
            "agent",
            "server",
            "telemetry",
            "analytics",
            "traces",
            "security",
            "channel",
            "tools",
            "sandbox",
            "scheduler",
            "workflow",
            "sessions",
            "a2a",
            "operators",
            "speech",
            "optimize",
            "agent_manager",
            "digest",
        )
        for section_name in top_sections:
            if section_name in data:
                _apply_toml_section(
                    getattr(cfg, section_name),
                    data[section_name],
                )

        # Memory: accept [memory] (old) ΓåÆ maps to tools.storage
        if "memory" in data:
            _apply_toml_section(cfg.tools.storage, data["memory"])

        # Top-level install provenance (installed_at, installer_version)
        for key in ("installed_at", "installer_version"):
            if key in data:
                setattr(cfg, key, data[key])

        # Expand security profile (user TOML overrides take precedence)
        _user_security_keys = set(data.get("security", {}).keys())
        apply_security_profile(cfg.security, cfg.server, overrides=_user_security_keys)

        # Mining: dedicated parser for tagged-union submit_target
        cfg.mining = _parse_mining_section(data)

    # Apply profile even without a config file (in case defaults set one)
    if not config_path.exists() and cfg.security.profile:
        apply_security_profile(cfg.security, cfg.server)

    return cfg


# ---------------------------------------------------------------------------
# Default TOML generation (for ``jarvis init``)
# ---------------------------------------------------------------------------


def generate_minimal_toml(
    hw: HardwareInfo, engine: str | None = None, *, host: str | None = None
) -> str:
    """Render a minimal TOML config with only essential settings."""
    engine = engine or recommend_engine(hw)
    model = recommend_model(hw, engine)
    gpu_comment = ""
    if hw.gpu:
        mem_label = "unified memory" if hw.gpu.vendor == "apple" else "VRAM"
        gpu_comment = f"\n# GPU: {hw.gpu.name} ({hw.gpu.vram_gb} GB {mem_label})"
    if host:
        engine_host_section = f'\n[engine.{engine}]\nhost = "{host}"\n'
    else:
        engine_host_section = (
            f"\n[engine.{engine}]\n"
            f'# host = "http://localhost:11434"  '
            f"# set to remote URL if engine runs elsewhere\n"
        )
    return f"""\
# OpenJarvis configuration
# Hardware: {hw.cpu_brand} ({hw.cpu_count} cores, {hw.ram_gb} GB RAM){gpu_comment}
# Full reference config: jarvis init --full

[engine]
default = "{engine}"
{engine_host_section}
[intelligence]
default_model = "{model}"

[agent]
default_agent = "simple"

[tools]
enabled = ["code_interpreter", "web_search", "file_read", "shell_exec"]
"""


def generate_default_toml(
    hw: HardwareInfo, engine: str | None = None, *, host: str | None = None
) -> str:
    """Render a commented TOML string suitable for ``~/.openjarvis/config.toml``."""
    engine = engine or recommend_engine(hw)
    model = recommend_model(hw, engine)
    gpu_line = ""
    if hw.gpu:
        gpu_line = f"# Detected GPU: {hw.gpu.name} ({hw.gpu.vram_gb} GB VRAM)"

    model_comment = ""
    if model:
        model_comment = "  # recommended for your hardware"

    result = f"""\
# OpenJarvis configuration
# Generated by `jarvis init`
#
# Hardware: {hw.cpu_brand} ({hw.cpu_count} cores, {hw.ram_gb} GB RAM)
{gpu_line}

[engine]
default = "{engine}"

[engine.ollama]
host = "http://localhost:11434"

[engine.vllm]
host = "http://localhost:8000"

[engine.sglang]
host = "http://localhost:30000"

# [engine.llamacpp]
# host = "http://localhost:8080"
# binary_path = ""

[engine.mlx]
host = "http://localhost:8080"

# [engine.lmstudio]
# host = "http://localhost:1234"

# [engine.exo]
# host = "http://localhost:52415"

# [engine.nexa]
# host = "http://localhost:18181"
# device = ""  # cpu, gpu, npu

# [engine.uzu]
# host = "http://localhost:8080"

# [engine.apple_fm]
# host = "http://localhost:8079"

[intelligence]
default_model = "{model}"{model_comment}
fallback_model = ""
# model_path = ""              # Local weights (HF repo, GGUF file, etc.)
# checkpoint_path = ""         # Checkpoint/adapter path
# quantization = "none"        # none, fp8, int8, int4, gguf_q4, gguf_q8
# preferred_engine = ""        # Override engine for this model (e.g., "vllm")
# provider = ""                # local, openai, anthropic, google
temperature = 0.7
max_tokens = 1024
# top_p = 0.9
# top_k = 40
# repetition_penalty = 1.0
# stop_sequences = ""

[agent]
default_agent = "simple"
max_turns = 10
# tools = ""                   # Comma-separated tool names
# objective = ""               # Concise purpose string
# system_prompt = ""           # Inline system prompt
# system_prompt_path = ""      # Path to system prompt file
context_from_memory = true

[tools.storage]
default_backend = "sqlite"

[tools.mcp]
enabled = true

# [tools.browser]
# headless = true
# timeout_ms = 30000
# viewport_width = 1280
# viewport_height = 720

[server]
host = "0.0.0.0"
port = 8000
agent = "orchestrator"

[learning]
enabled = false
update_interval = 100
# auto_update = false

[learning.routing]
policy = "heuristic"
# min_samples = 5

# [learning.intelligence]
# policy = "none"              # "sft" to learn from traces

# [learning.agent]
# policy = "none"              # "agent_advisor" | "icl_updater"

# [learning.metrics]
# accuracy_weight = 0.6
# latency_weight = 0.2
# cost_weight = 0.1
# efficiency_weight = 0.1

[telemetry]
enabled = true
# gpu_metrics = false
# gpu_poll_interval_ms = 50

[traces]
enabled = false

[channel]
enabled = false
default_agent = "simple"

# [channel.telegram]
# bot_token = ""  # Or set TELEGRAM_BOT_TOKEN env var

# [channel.discord]
# bot_token = ""  # Or set DISCORD_BOT_TOKEN env var

# [channel.slack]
# bot_token = ""  # Or set SLACK_BOT_TOKEN env var

# [channel.webhook]
# url = ""

# [channel.whatsapp]
# access_token = ""      # Or set WHATSAPP_ACCESS_TOKEN env var
# phone_number_id = ""   # Or set WHATSAPP_PHONE_NUMBER_ID env var

# [channel.signal]
# api_url = ""            # signal-cli REST API URL
# phone_number = ""       # Or set SIGNAL_PHONE_NUMBER env var

# [channel.google_chat]
# webhook_url = ""        # Or set GOOGLE_CHAT_WEBHOOK_URL env var

# [channel.irc]
# server = ""
# port = 6667
# nick = ""
# use_tls = false

# [channel.teams]
# app_id = ""             # Or set TEAMS_APP_ID env var
# app_password = ""       # Or set TEAMS_APP_PASSWORD env var

# [channel.matrix]
# homeserver = ""         # Or set MATRIX_HOMESERVER env var
# access_token = ""       # Or set MATRIX_ACCESS_TOKEN env var

# [channel.mattermost]
# url = ""                # Or set MATTERMOST_URL env var
# token = ""              # Or set MATTERMOST_TOKEN env var

# [channel.feishu]
# app_id = ""             # Or set FEISHU_APP_ID env var
# app_secret = ""         # Or set FEISHU_APP_SECRET env var

# [channel.bluebubbles]
# url = ""                # Or set BLUEBUBBLES_URL env var
# password = ""           # Or set BLUEBUBBLES_PASSWORD env var

[security]
enabled = true
mode = "warn"
scan_input = true
scan_output = true
secret_scanner = true
pii_scanner = true
enforce_tool_confirmation = true
ssrf_protection = true
# rate_limit_enabled = false
# rate_limit_rpm = 60
# rate_limit_burst = 10

# [sandbox]
# enabled = false
# image = "openjarvis-sandbox:latest"
# timeout = 300
# max_concurrent = 5
# runtime = "docker"

# [scheduler]
# enabled = false
# poll_interval = 60
# db_path = ""                # Defaults to ~/.openjarvis/scheduler.db

# [channel.whatsapp_baileys]
# auth_dir = ""               # Defaults to ~/.openjarvis/whatsapp_auth
# assistant_name = "Jarvis"
# assistant_has_own_number = false
"""
    if host:
        import re as _re

        pattern = _re.escape(f"[engine.{engine}]") + r"\nhost = \"[^\"]*\""
        replacement = f'[engine.{engine}]\\nhost = "{host}"'
        result = _re.sub(pattern, replacement, result)
    return result


__all__ = [
    "A2AConfig",
    "AgentConfig",
    "AgentManagerConfig",
    "OperatorsConfig",
    "AgentLearningConfig",
    "BlueBubblesChannelConfig",
    "BrowserConfig",
    "CapabilitiesConfig",
    "ChannelConfig",
    "DEFAULT_CONFIG_DIR",
    "DEFAULT_CONFIG_PATH",
    "DiscordChannelConfig",
    "EmailChannelConfig",
    "EngineConfig",
    "FeishuChannelConfig",
    "GoogleChatChannelConfig",
    "GpuInfo",
    "HardwareInfo",
    "IRCChannelConfig",
    "IntelligenceConfig",
    "IntelligenceLearningConfig",
    "JarvisConfig",
    "LearningConfig",
    "LMStudioEngineConfig",
    "LlamaCppEngineConfig",
    "MCPConfig",
    "MLXEngineConfig",
    "MatrixChannelConfig",
    "MattermostChannelConfig",
    "MemoryConfig",
    "MetricsConfig",
    "OllamaEngineConfig",
    "OptimizeConfig",
    "RoutingLearningConfig",
    "SGLangEngineConfig",
    "SandboxConfig",
    "SchedulerConfig",
    "SecurityConfig",
    "ServerConfig",
    "SessionConfig",
    "SignalChannelConfig",
    "SlackChannelConfig",
    "SpeechConfig",
    "StorageConfig",
    "TeamsChannelConfig",
    "TelegramChannelConfig",
    "TelemetryConfig",
    "ToolsConfig",
    "TracesConfig",
    "VLLMEngineConfig",
    "WebChatChannelConfig",
    "WebhookChannelConfig",
    "WhatsAppBaileysChannelConfig",
    "WhatsAppChannelConfig",
    "WorkflowConfig",
    "detect_hardware",
    "generate_default_toml",
    "generate_minimal_toml",
    "load_config",
    "recommend_engine",
    "recommend_model",
    "validate_config_key",
]

## ===== src/openjarvis/core/config.py : STAGE 2 =====
"""Configuration loading, hardware detection, and engine recommendation.

User configuration lives at ``~/.openjarvis/config.toml``.  ``load_config()``
detects hardware, fills sensible defaults, then overlays any user overrides
found in the TOML file.
"""

from __future__ import annotations

import functools
import os
import platform
import shutil
import subprocess
from dataclasses import dataclass, field
from pathlib import Path
from typing import TYPE_CHECKING, Any, Dict, List, Optional

if TYPE_CHECKING:
    # Only used by type-checkers (mypy/pyright) for the ``JarvisConfig.mining``
    # field annotation. The runtime import is deferred inside
    # ``_parse_mining_section()`` to break the import cycle:
    # ``mining/_stubs.py`` imports ``HardwareInfo`` from this module at its
    # top level.
    from openjarvis.mining._stubs import MiningConfig

try:
    import tomllib  # Python 3.11+
except ModuleNotFoundError:
    import tomli as tomllib  # type: ignore[no-redef]

# ---------------------------------------------------------------------------
# Hardware dataclasses
# ---------------------------------------------------------------------------

DEFAULT_CONFIG_DIR = Path.home() / ".openjarvis"
DEFAULT_CONFIG_PATH = DEFAULT_CONFIG_DIR / "config.toml"


def _ensure_config_dir() -> Path:
    """Ensure the config directory exists with restrictive permissions."""
    from openjarvis.security.file_utils import secure_mkdir

    return secure_mkdir(DEFAULT_CONFIG_DIR)


@dataclass(slots=True)
class GpuInfo:
    """Detected GPU metadata."""

    vendor: str = ""
    name: str = ""
    vram_gb: float = 0.0
    compute_capability: str = ""
    count: int = 0


@dataclass(slots=True)
class HardwareInfo:
    """Detected system hardware."""

    platform: str = ""
    cpu_brand: str = ""
    cpu_count: int = 0
    ram_gb: float = 0.0
    gpu: Optional[GpuInfo] = None


# ---------------------------------------------------------------------------
# Hardware detection helpers
# ---------------------------------------------------------------------------


def _run_cmd(cmd: list[str]) -> str:
    """Run a command and return stripped stdout, or empty string on failure."""
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=10,  # noqa: S603
        )
        return result.stdout.strip()
    except (FileNotFoundError, subprocess.TimeoutExpired, OSError):
        return ""


def _detect_nvidia_gpu() -> Optional[GpuInfo]:
    if not shutil.which("nvidia-smi"):
        return None
    raw = _run_cmd(
        [
            "nvidia-smi",
            "--query-gpu=name,memory.total,count,compute_cap",
            "--format=csv,noheader,nounits",
        ]
    )
    if not raw:
        return None
    try:
        first_line = raw.splitlines()[0]
        parts = [p.strip() for p in first_line.split(",")]
        name = parts[0]
        vram_mb = float(parts[1])
        count = int(parts[2])
        compute_capability = parts[3] if len(parts) > 3 else ""
        return GpuInfo(
            vendor="nvidia",
            name=name,
            vram_gb=round(vram_mb / 1024, 1),
            compute_capability=compute_capability,
            count=count,
        )
    except (IndexError, ValueError):
        return None


def _detect_amd_gpu() -> Optional[GpuInfo]:
    if not shutil.which("rocm-smi"):
        return None
    raw = _run_cmd(["rocm-smi", "--showproductname"])
    if not raw:
        return None
    name = raw.splitlines()[0] if raw else "AMD GPU"

    # Parse VRAM from rocm-smi --showmeminfo vram
    vram_gb = 0.0
    try:
        vram_raw = _run_cmd(["rocm-smi", "--showmeminfo", "vram"])
        for line in vram_raw.splitlines():
            if "Total Memory (B):" in line:
                vram_bytes = int(line.split(":")[-1].strip())
                vram_gb = round(vram_bytes / (1024**3), 1)
                break
    except (ValueError, IndexError):
        vram_gb = 0.0

    # Parse GPU count from rocm-smi --showallinfo
    count = 1
    try:
        allinfo_raw = _run_cmd(["rocm-smi", "--showallinfo"])
        import re

        gpu_ids = set(re.findall(r"GPU\[(\d+)\]", allinfo_raw))
        if gpu_ids:
            count = len(gpu_ids)
    except (ValueError, IndexError):
        count = 1

    return GpuInfo(vendor="amd", name=name, vram_gb=vram_gb, count=count)


def _detect_apple_gpu() -> Optional[GpuInfo]:
    if platform.system() != "Darwin":
        return None
    raw = _run_cmd(["system_profiler", "SPDisplaysDataType"])
    if "Apple" not in raw:
        return None
    # Rough extraction ΓÇö "Apple M2 Max" etc.
    ram_gb = _total_ram_gb()
    for line in raw.splitlines():
        line = line.strip()
        if "Chipset Model" in line:
            name = line.split(":")[-1].strip()
            return GpuInfo(vendor="apple", name=name, vram_gb=ram_gb, count=1)
    return GpuInfo(vendor="apple", name="Apple Silicon", vram_gb=ram_gb, count=1)


def _detect_cpu_brand() -> str:
    """Best-effort CPU brand string."""
    if platform.system() == "Darwin":
        brand = _run_cmd(["sysctl", "-n", "machdep.cpu.brand_string"])
        if brand:
            return brand
    cpuinfo = Path("/proc/cpuinfo")
    if cpuinfo.exists():
        try:
            for line in cpuinfo.read_text().splitlines():
                if line.startswith("model name"):
                    return line.split(":", 1)[1].strip()
        except OSError:
            pass
    return platform.processor() or "unknown"


def _total_ram_gb() -> float:
    try:
        if platform.system() == "Darwin":
            raw = _run_cmd(["sysctl", "-n", "hw.memsize"])
            return round(int(raw) / (1024**3), 1) if raw else 0.0
        meminfo = Path("/proc/meminfo")
        if meminfo.exists():
            for line in meminfo.read_text().splitlines():
                if line.startswith("MemTotal"):
                    kb = int(line.split()[1])
                    return round(kb / (1024**2), 1)
    except (OSError, ValueError):
        pass
    return 0.0


def detect_hardware() -> HardwareInfo:
    """Auto-detect hardware capabilities with graceful fallbacks."""
    gpu = _detect_nvidia_gpu() or _detect_amd_gpu() or _detect_apple_gpu()
    return HardwareInfo(
        platform=platform.system().lower(),
        cpu_brand=_detect_cpu_brand(),
        cpu_count=os.cpu_count() or 1,
        ram_gb=_total_ram_gb(),
        gpu=gpu,
    )


# ---------------------------------------------------------------------------
# Engine recommendation
# ---------------------------------------------------------------------------


def recommend_engine(hw: HardwareInfo) -> str:
    """Suggest the best inference engine for the detected hardware."""
    gpu = hw.gpu
    if gpu is None:
        return "llamacpp"
    if gpu.vendor == "apple":
        return "mlx"
    if gpu.vendor == "nvidia":
        # Datacenter cards (A100, H100, L40, etc.) ΓåÆ vllm; consumer ΓåÆ ollama
        datacenter_keywords = ("A100", "H100", "H200", "L40", "A10", "A30")
        if any(kw in gpu.name for kw in datacenter_keywords):
            return "vllm"
        return "ollama"
    if gpu.vendor == "amd":
        # Datacenter cards (MI300, MI325, MI350, MI355) ΓåÆ vllm; consumer ΓåÆ lemonade
        amd_datacenter_keywords = ("MI300", "MI325", "MI350", "MI355")
        if any(kw in gpu.name for kw in amd_datacenter_keywords):
            return "vllm"
        return "lemonade"
    return "llamacpp"


def _available_memory_gb(hw: HardwareInfo) -> float:
    """Return usable memory in GB for model loading."""
    gpu = hw.gpu
    if gpu and gpu.vram_gb > 0:
        return gpu.vram_gb * max(gpu.count, 1) * 0.9
    if hw.ram_gb > 0:
        return (hw.ram_gb - 4) * 0.8
    return 0.0


# Explicit tier table: (max_ram_gb, model_id).
# Walked in order ΓÇö first tier where available_gb <= max_ram is chosen.
# Uses Qwen3.5 MoE models ΓÇö better quality per GB than dense models since
# only a fraction of parameters are active per token.
_MODEL_TIERS = [
    (8, "qwen3.5:2b"),
    (16, "qwen3.5:4b"),
    (32, "qwen3.5:9b"),
    (64, "qwen2.5-coder:32b"),
]
_MODEL_TIER_FALLBACK = "qwen3.5:9b"


def recommend_model(hw: HardwareInfo, engine: str) -> str:
    """Suggest the best Qwen3.5 model that fits the detected hardware.

    Uses an explicit tier table mapping available memory to model size.
    Falls back to scanning the full catalog if the tiered model is not
    compatible with the selected engine.
    """
    from openjarvis.intelligence.model_catalog import BUILTIN_MODELS

    available_gb = _available_memory_gb(hw)
    if available_gb <= 0:
        return ""

    # Build a lookup for quick engine-compatibility checks
    catalog = {spec.model_id: spec for spec in BUILTIN_MODELS}

    # Try explicit tier mapping first
    model_id = _MODEL_TIER_FALLBACK
    for max_ram, tier_model in _MODEL_TIERS:
        if available_gb <= max_ram:
            model_id = tier_model
            break

    spec = catalog.get(model_id)
    if spec and engine in spec.supported_engines:
        return model_id

    # Fallback: scan all Qwen3.5 models for engine compatibility
    candidates = [
        s
        for s in BUILTIN_MODELS
        if s.provider == "alibaba"
        and s.model_id.startswith("qwen3.5:")
        and engine in s.supported_engines
    ]
    candidates.sort(key=lambda s: s.parameter_count_b, reverse=True)
    for s in candidates:
        estimated_gb = s.parameter_count_b * 0.5 * 1.1
        if estimated_gb <= available_gb:
            return s.model_id

    return ""


def estimated_download_gb(parameter_count_b: float) -> float:
    """Estimate download size in GB for Q4_K_M quantized model."""
    return parameter_count_b * 0.5 * 1.1


# ---------------------------------------------------------------------------
# Configuration hierarchy
# ---------------------------------------------------------------------------


@dataclass(slots=True)
class OllamaEngineConfig:
    """Per-engine config for Ollama."""

    host: str = ""


@dataclass(slots=True)
class VLLMEngineConfig:
    """Per-engine config for vLLM."""

    host: str = "http://localhost:8010"


@dataclass(slots=True)
class SGLangEngineConfig:
    """Per-engine config for SGLang."""

    host: str = "http://localhost:30000"


@dataclass(slots=True)
class LlamaCppEngineConfig:
    """Per-engine config for llama.cpp."""

    host: str = "http://localhost:8080"
    binary_path: str = ""


@dataclass(slots=True)
class MLXEngineConfig:
    """Per-engine config for MLX."""

    host: str = "http://localhost:8080"


@dataclass(slots=True)
class LMStudioEngineConfig:
    """Per-engine config for LM Studio."""

    host: str = "http://localhost:1234"


@dataclass(slots=True)
class ExoEngineConfig:
    """Per-engine config for Exo."""

    host: str = "http://localhost:52415"


@dataclass(slots=True)
class NexaEngineConfig:
    """Per-engine config for Nexa."""

    host: str = "http://localhost:18181"
    device: str = ""


@dataclass(slots=True)
class UzuEngineConfig:
    """Per-engine config for Uzu."""

    host: str = "http://localhost:8010"


@dataclass(slots=True)
class AppleFmEngineConfig:
    """Per-engine config for Apple Foundation Models."""

    host: str = "http://localhost:8079"


@dataclass(slots=True)
class GemmaCppEngineConfig:
    """Per-engine config for gemma.cpp."""

    model_path: str = ""
    tokenizer_path: str = ""
    model_type: str = ""
    num_threads: int = 0


@dataclass(slots=True)
class LemonadeEngineConfig:
    """Per-engine config for Lemonade."""

    host: str = "http://localhost:8010"


@dataclass
class EngineConfig:
    """Inference engine settings with nested per-engine configs."""

    default: str = "ollama"
    # openjarvis-engine-disable-v1 (Graystone D-16): comma-separated engine keys that are
    # never constructed or probed. The author ships no engine off-switch.
    disabled: str = ""
    ollama: OllamaEngineConfig = field(default_factory=OllamaEngineConfig)
    vllm: VLLMEngineConfig = field(default_factory=VLLMEngineConfig)
    sglang: SGLangEngineConfig = field(default_factory=SGLangEngineConfig)
    llamacpp: LlamaCppEngineConfig = field(default_factory=LlamaCppEngineConfig)
    mlx: MLXEngineConfig = field(default_factory=MLXEngineConfig)
    lmstudio: LMStudioEngineConfig = field(default_factory=LMStudioEngineConfig)
    exo: ExoEngineConfig = field(default_factory=ExoEngineConfig)
    nexa: NexaEngineConfig = field(default_factory=NexaEngineConfig)
    uzu: UzuEngineConfig = field(default_factory=UzuEngineConfig)
    apple_fm: AppleFmEngineConfig = field(default_factory=AppleFmEngineConfig)
    gemma_cpp: GemmaCppEngineConfig = field(default_factory=GemmaCppEngineConfig)
    lemonade: LemonadeEngineConfig = field(default_factory=LemonadeEngineConfig)

    # Backward-compat properties for old flat attribute names
    @property
    def ollama_host(self) -> str:
        """Deprecated: use ``engine.ollama.host``."""
        return self.ollama.host

    @ollama_host.setter
    def ollama_host(self, value: str) -> None:
        self.ollama.host = value

    @property
    def vllm_host(self) -> str:
        """Deprecated: use ``engine.vllm.host``."""
        return self.vllm.host

    @vllm_host.setter
    def vllm_host(self, value: str) -> None:
        self.vllm.host = value

    @property
    def llamacpp_host(self) -> str:
        """Deprecated: use ``engine.llamacpp.host``."""
        return self.llamacpp.host

    @llamacpp_host.setter
    def llamacpp_host(self, value: str) -> None:
        self.llamacpp.host = value

    @property
    def llamacpp_path(self) -> str:
        """Deprecated: use ``engine.llamacpp.binary_path``."""
        return self.llamacpp.binary_path

    @llamacpp_path.setter
    def llamacpp_path(self, value: str) -> None:
        self.llamacpp.binary_path = value

    @property
    def sglang_host(self) -> str:
        """Deprecated: use ``engine.sglang.host``."""
        return self.sglang.host

    @sglang_host.setter
    def sglang_host(self, value: str) -> None:
        self.sglang.host = value

    @property
    def mlx_host(self) -> str:
        """Deprecated: use ``engine.mlx.host``."""
        return self.mlx.host

    @mlx_host.setter
    def mlx_host(self, value: str) -> None:
        self.mlx.host = value

    @property
    def lmstudio_host(self) -> str:
        """Deprecated: use ``engine.lmstudio.host``."""
        return self.lmstudio.host

    @lmstudio_host.setter
    def lmstudio_host(self, value: str) -> None:
        self.lmstudio.host = value

    @property
    def exo_host(self) -> str:
        """Deprecated: use ``engine.exo.host``."""
        return self.exo.host

    @exo_host.setter
    def exo_host(self, value: str) -> None:
        self.exo.host = value

    @property
    def nexa_host(self) -> str:
        """Deprecated: use ``engine.nexa.host``."""
        return self.nexa.host

    @nexa_host.setter
    def nexa_host(self, value: str) -> None:
        self.nexa.host = value

    @property
    def uzu_host(self) -> str:
        """Deprecated: use ``engine.uzu.host``."""
        return self.uzu.host

    @uzu_host.setter
    def uzu_host(self, value: str) -> None:
        self.uzu.host = value

    @property
    def apple_fm_host(self) -> str:
        """Deprecated: use ``engine.apple_fm.host``."""
        return self.apple_fm.host

    @apple_fm_host.setter
    def apple_fm_host(self, value: str) -> None:
        self.apple_fm.host = value

    @property
    def lemonade_host(self) -> str:
        """Deprecated: use ``engine.lemonade.host``."""
        return self.lemonade.host

    @lemonade_host.setter
    def lemonade_host(self, value: str) -> None:
        self.lemonade.host = value


@dataclass(slots=True)
class IntelligenceConfig:
    """The model ΓÇö identity, paths, quantization, and generation defaults."""

    default_model: str = ""
    fallback_model: str = ""
    model_path: str = ""  # Local weights (HF repo, GGUF file, etc.)
    checkpoint_path: str = ""  # Checkpoint/adapter path
    quantization: str = "none"  # none, fp8, int8, int4, gguf_q4, gguf_q8
    preferred_engine: str = ""  # Override engine for this model (e.g., "vllm")
    provider: str = ""  # local, openai, anthropic, google
    # Generation defaults (overridable per-call)
    temperature: float = 0.7
    max_tokens: int = 1024
    top_p: float = 0.9
    top_k: int = 40
    repetition_penalty: float = 1.0
    stop_sequences: str = ""  # Comma-separated stop strings


@dataclass(slots=True)
class RoutingLearningConfig:
    """Routing sub-policy config within Learning."""

    policy: str = "heuristic"  # heuristic | learned
    min_samples: int = 5  # Min traces before trusting learned routing


@dataclass(slots=True)
class SFTConfig:
    """General-purpose SFT training config. Maps to [learning.intelligence.sft]."""

    model_name: str = "Qwen/Qwen3-1.7B"
    max_seq_length: int = 4096
    num_epochs: int = 3
    batch_size: int = 8
    learning_rate: float = 2e-5
    weight_decay: float = 0.01
    warmup_ratio: float = 0.1
    max_grad_norm: float = 1.0
    gradient_checkpointing: bool = True
    use_lora: bool = True
    lora_rank: int = 16
    lora_alpha: int = 32
    lora_dropout: float = 0.05
    target_modules: str = "q_proj,v_proj"  # comma-separated for TOML compat
    use_4bit: bool = False
    checkpoint_dir: str = "checkpoints/sft"
    min_pairs: int = 10
    agent_filter: str = ""


@dataclass(slots=True)
class GRPOConfig:
    """General-purpose GRPO training config. Maps to [learning.intelligence.grpo]."""

    model_name: str = "Qwen/Qwen3-1.7B"
    max_seq_length: int = 4096
    max_response_length: int = 2048
    num_epochs: int = 10
    batch_size: int = 16
    learning_rate: float = 1e-6
    max_grad_norm: float = 1.0
    gradient_checkpointing: bool = True
    num_samples_per_prompt: int = 8
    temperature: float = 1.0
    kl_coef: float = 0.0001
    clip_ratio: float = 0.2
    use_8bit_ref: bool = True
    checkpoint_dir: str = "checkpoints/grpo"
    save_every_n_epochs: int = 1
    keep_last_n: int = 3
    min_prompts: int = 10
    agent_filter: str = ""


@dataclass(slots=True)
class DSPyOptimizerConfig:
    """DSPy agent optimizer config. Maps to [learning.agent.dspy]."""

    optimizer: str = "BootstrapFewShotWithRandomSearch"
    task_lm: str = ""
    teacher_lm: str = ""
    max_bootstrapped_demos: int = 4
    max_labeled_demos: int = 4
    num_candidate_programs: int = 10
    max_rounds: int = 1
    optimize_system_prompt: bool = True
    optimize_few_shot: bool = True
    optimize_tool_descriptions: bool = True
    min_traces: int = 20
    metric_threshold: float = 0.7
    agent_filter: str = ""
    config_dir: str = ""


@dataclass(slots=True)
class GEPAOptimizerConfig:
    """GEPA agent optimizer config. Maps to [learning.agent.gepa]."""

    reflection_lm: str = ""
    max_metric_calls: int = 150
    population_size: int = 10
    optimize_system_prompt: bool = True
    optimize_tools: bool = True
    optimize_max_turns: bool = True
    optimize_temperature: bool = True
    min_traces: int = 20
    assessment_batch_size: int = 10
    agent_filter: str = ""
    config_dir: str = ""


@dataclass(slots=True)
class ACEOptimizerConfig:
    """ACE agent optimizer config. Maps to ``[learning.agent.ace]``.

    ACE (Agentic Context Engineering) evolves a *playbook* ΓÇö annotated
    natural-language strategies that get prepended to the agent's
    context ΓÇö using a Generator / Reflector / Curator triad. Unlike
    DSPy (few-shot bootstrapping) or GEPA (Pareto-evolutionary prompt
    mutation), ACE writes a textual playbook that the agent reads at
    inference time.

    See https://github.com/ace-agent/ace for the upstream reference.
    Install via ``pip install -e openjarvis[learning-ace]`` once the
    optional dep is available (ACE is not on PyPI as of v1.0.1; the
    extra installs from the upstream git repo).
    """

    # Models for ACE's three roles. Empty string = inherit from the
    # intelligence primitive's default cloud model.
    generator_model: str = ""
    reflector_model: str = ""
    curator_model: str = ""

    # Provider passed to ACE (``sambanova`` | ``together`` | ``openai``
    # | ``commonstack``). We default to ``openai`` since that's what
    # most OpenJarvis users have credentials for.
    api_provider: str = "openai"

    # Run parameters. Defaults mirror ACE's offline-mode quickstart.
    num_epochs: int = 1
    max_num_rounds: int = 3
    eval_steps: int = 100
    playbook_token_budget: int = 80_000
    max_tokens: int = 4_096

    # Where ACE writes intermediate playbooks + final_results.json.
    # Empty string defaults to ``~/.openjarvis/learning/ace/<task>/``.
    save_dir: str = ""
    task_name: str = "openjarvis"

    # Standard filter / threshold knobs shared with DSPy / GEPA.
    min_traces: int = 20
    agent_filter: str = ""
    config_dir: str = ""


@dataclass(slots=True)
class IntelligenceLearningConfig:
    """Intelligence sub-policy config within Learning."""

    policy: str = "none"  # none | sft | grpo
    sft: SFTConfig = field(default_factory=SFTConfig)
    grpo: GRPOConfig = field(default_factory=GRPOConfig)


@dataclass(slots=True)
class AgentLearningConfig:
    """Agent sub-policy config within Learning."""

    policy: str = "none"  # none | dspy | gepa | ace
    dspy: DSPyOptimizerConfig = field(default_factory=DSPyOptimizerConfig)
    gepa: GEPAOptimizerConfig = field(default_factory=GEPAOptimizerConfig)
    ace: ACEOptimizerConfig = field(default_factory=ACEOptimizerConfig)


@dataclass(slots=True)
class SkillsLearningConfig:
    """Configuration for the skills learning loop (Plan 2A)."""

    auto_optimize: bool = False  # opt in via config
    optimizer: str = "dspy"  # "dspy" or "gepa"
    min_traces_per_skill: int = 20
    optimization_interval_seconds: int = 86400
    overlay_dir: str = "~/.openjarvis/learning/skills/"


@dataclass(slots=True)
class MetricsConfig:
    """Reward / optimization metric weights."""

    accuracy_weight: float = 0.6
    latency_weight: float = 0.2
    cost_weight: float = 0.1
    efficiency_weight: float = 0.1


@dataclass(slots=True)
class SpecSearchCompositeRewardConfig:
    """Composite reward weights for Intelligence-edit training (paper Eq. 1).

    R(q, y) = alpha * R_acc - beta * E_hat - gamma * L_hat - delta * C_hat
    """

    alpha: float = 0.5
    beta: float = 0.1
    gamma: float = 0.1
    delta: float = 0.3


@dataclass(slots=True)
class SpecSearchLearningConfig:
    """LLM-guided spec search config (paper ┬º3.3, Algorithm 1).

    Maps to ``[learning.spec_search]`` and is consumed by
    ``SpecSearchOrchestrator.from_config`` and ``SpecSearchLoop``.
    """

    enabled: bool = False
    teacher_model: str = "claude-opus-4-6"
    teacher_engine: str = "cloud"  # registry key for the cloud engine
    autonomy_mode: str = "tiered"  # auto | tiered | manual

    # Per-session bounds (one diagnose/plan/execute pass)
    min_traces: int = 20
    max_cost_per_session_usd: float = 5.0
    max_tool_calls_per_diagnosis: int = 30

    # Multi-session loop (paper Algorithm 1)
    stagnation_k: int = 5
    max_total_cost_usd: float = 50.0
    stagnation_eps: float = 0.001  # gate-score delta below this counts as no progress

    # Gate (GateOK predicate)
    max_regression: float = 0.01  # paper default: epsilon = 1%
    min_improvement: float = 0.0
    benchmark_subsample_size: int = 50
    benchmark_version: str = "personal_v1"

    # Composite reward (only used when an Intelligence edit triggers training)
    composite_reward: SpecSearchCompositeRewardConfig = field(
        default_factory=SpecSearchCompositeRewardConfig,
    )


@dataclass
class LearningConfig:
    """Learning system settings with per-primitive sub-policies."""

    enabled: bool = False
    update_interval: int = 100
    auto_update: bool = False
    routing: RoutingLearningConfig = field(default_factory=RoutingLearningConfig)
    intelligence: IntelligenceLearningConfig = field(
        default_factory=IntelligenceLearningConfig,
    )
    agent: AgentLearningConfig = field(default_factory=AgentLearningConfig)
    skills: SkillsLearningConfig = field(default_factory=SkillsLearningConfig)
    spec_search: SpecSearchLearningConfig = field(
        default_factory=SpecSearchLearningConfig,
    )
    metrics: MetricsConfig = field(default_factory=MetricsConfig)

    # Training pipeline
    training_enabled: bool = False
    training_schedule: str = ""
    min_improvement: float = 0.02

    # Backward-compat properties for old flat field names
    @property
    def default_policy(self) -> str:
        """Deprecated: use ``learning.routing.policy``."""
        return self.routing.policy

    @default_policy.setter
    def default_policy(self, value: str) -> None:
        self.routing.policy = value

    @property
    def intelligence_policy(self) -> str:
        """Deprecated: use ``learning.intelligence.policy``."""
        return self.intelligence.policy

    @intelligence_policy.setter
    def intelligence_policy(self, value: str) -> None:
        self.intelligence.policy = value

    @property
    def agent_policy(self) -> str:
        """Deprecated: use ``learning.agent.policy``."""
        return self.agent.policy

    @agent_policy.setter
    def agent_policy(self, value: str) -> None:
        self.agent.policy = value

    @property
    def reward_weights(self) -> str:
        """Deprecated: use ``learning.metrics.*``."""
        parts = []
        m = self.metrics
        if m.latency_weight:
            parts.append(f"latency={m.latency_weight}")
        if m.cost_weight:
            parts.append(f"cost={m.cost_weight}")
        if m.efficiency_weight:
            parts.append(f"efficiency={m.efficiency_weight}")
        if m.accuracy_weight:
            parts.append(f"accuracy={m.accuracy_weight}")
        return ",".join(parts)

    @reward_weights.setter
    def reward_weights(self, value: str) -> None:
        if not value:
            return
        for part in value.split(","):
            if "=" not in part:
                continue
            key, val = part.strip().split("=", 1)
            key = key.strip()
            fval = float(val.strip())
            if key == "accuracy":
                self.metrics.accuracy_weight = fval
            elif key == "latency":
                self.metrics.latency_weight = fval
            elif key == "cost":
                self.metrics.cost_weight = fval
            elif key == "efficiency":
                self.metrics.efficiency_weight = fval


@dataclass(slots=True)
class StorageConfig:
    """Storage (memory) backend settings."""

    default_backend: str = "sqlite"
    db_path: str = str(DEFAULT_CONFIG_DIR / "memory.db")
    context_top_k: int = 5
    context_min_score: float = 0.0
    context_max_tokens: int = 2048
    chunk_size: int = 512
    chunk_overlap: int = 64


# Backward-compatibility alias
MemoryConfig = StorageConfig


@dataclass(slots=True)
class MCPConfig:
    """MCP (Model Context Protocol) settings."""

    enabled: bool = True
    servers: str = ""  # JSON list of MCP server configs


@dataclass(slots=True)
class BrowserConfig:
    """Browser automation settings (Playwright)."""

    headless: bool = True
    timeout_ms: int = 30000
    viewport_width: int = 1280
    viewport_height: int = 720


@dataclass(slots=True)
class ToolsConfig:
    """Tools primitive settings ΓÇö wraps storage and MCP configuration."""

    storage: StorageConfig = field(default_factory=StorageConfig)
    mcp: MCPConfig = field(default_factory=MCPConfig)
    browser: BrowserConfig = field(default_factory=BrowserConfig)
    enabled: str = ""  # comma-separated default tools
    file_allowed_dirs: str = ""  # openjarvis-file-confine-v1 (W78): comma-separated; empty = scratch pad


def resolve_file_write_dirs(cfg: "JarvisConfig") -> List[str]:
    """Directories file_write may write to. openjarvis-file-confine-v1 (W78).

    FileWriteTool accepts allowed_dirs, but no builder ever passed it, so on
    every surface an empty list meant write anywhere. Graystone confines it
    to [tools] file_allowed_dirs, or to the Jarvis scratch pad
    (~/.openjarvis/workspace) when unset. Never returns an empty list.
    """
    raw = getattr(getattr(cfg, "tools", None), "file_allowed_dirs", "") or ""
    dirs = [d.strip() for d in str(raw).split(",") if d.strip()]
    if not dirs:
        dirs = [str(DEFAULT_CONFIG_DIR / "workspace")]
    out: List[str] = []
    for d in dirs:
        p = Path(d).expanduser()
        try:
            p.mkdir(parents=True, exist_ok=True)
        except OSError:
            pass
        out.append(str(p))
    return out


@dataclass
class AgentConfig:
    """Agent harness settings ΓÇö orchestration, tools, system prompt."""

    default_agent: str = "simple"
    max_turns: int = 10
    tools: str = ""  # comma-separated tool names
    objective: str = ""  # concise purpose for routing/learning/docs
    system_prompt: str = ""  # inline system prompt (takes precedence if set)
    system_prompt_path: str = ""  # path to system prompt file (.txt, .md)
    context_from_memory: bool = True  # inject relevant memory context into prompts
    default_system_prompt: str = (
        "You are a helpful AI assistant running locally on the user's own "
        "hardware through OpenJarvis. You are not a cloud service. Respond "
        "helpfully, concisely, and accurately."
    )

    # Backward-compat property for old field name
    @property
    def default_tools(self) -> str:
        """Deprecated: use ``agent.tools``."""
        return self.tools

    @default_tools.setter
    def default_tools(self, value: str) -> None:
        self.tools = value


@dataclass(slots=True)
class ServerConfig:
    """API server settings."""

    host: str = "127.0.0.1"
    port: int = 8010
    agent: str = "orchestrator"
    model: str = ""
    workers: int = 1
    cors_origins: list = field(
        default_factory=lambda: [
            "http://localhost:3000",
            "http://localhost:5173",
            "http://127.0.0.1:3000",
            "http://127.0.0.1:5173",
            # Tauri 2 production webview origins.
            # macOS / Linux / iOS use the custom scheme; Windows /
            # Android use http(s)://tauri.localhost. All three must
            # be allowed so the desktop app's chat-completions stream
            # is not blocked by CORS in production builds.
            "tauri://localhost",
            "http://tauri.localhost",
            "https://tauri.localhost",
        ]
    )


@dataclass(slots=True)
class TelemetryConfig:
    """Telemetry persistence settings."""

    enabled: bool = True
    db_path: str = str(DEFAULT_CONFIG_DIR / "telemetry.db")
    gpu_metrics: bool = False
    gpu_poll_interval_ms: int = 50
    energy_vendor: str = ""  # auto-detect or force "nvidia"/"amd"/"apple"/"cpu_rapl"
    warmup_samples: int = 0
    steady_state_window: int = 5
    steady_state_threshold: float = 0.05


@dataclass(slots=True)
class AnalyticsConfig:
    """External anonymous usage analytics (PostHog).

    Separate concern from :class:`TelemetryConfig`, which stores local
    FLOPs/energy/inference metrics in SQLite. This controls anonymized
    usage events sent to the OpenJarvis team's PostHog instance to
    measure setup success, retention, feature usage, and churn.

    No chat content, prompts, model outputs, file paths, emails, IPs,
    or hardware identifiers are ever sent. See ``docs/telemetry.md``.
    """

    enabled: bool = True
    host: str = "https://34.231.106.201.sslip.io"
    key: str = "phc_ysKu72QaxzYNmDpHFcesD2ZZAe68zkdWJEKoYYkc5e3n"
    anon_id_path: str = str(DEFAULT_CONFIG_DIR / "anon_id")
    flush_interval_seconds: int = 30
    flush_at_size: int = 100


@dataclass(slots=True)
class TracesConfig:
    """Trace system settings."""

    enabled: bool = True
    db_path: str = str(DEFAULT_CONFIG_DIR / "traces.db")


@dataclass(slots=True)
class TelegramChannelConfig:
    """Per-channel config for Telegram."""

    bot_token: str = ""
    allowed_chat_ids: str = ""
    parse_mode: str = "Markdown"


@dataclass(slots=True)
class DiscordChannelConfig:
    """Per-channel config for Discord."""

    bot_token: str = ""


@dataclass(slots=True)
class SlackChannelConfig:
    """Per-channel config for Slack."""

    bot_token: str = ""
    app_token: str = ""


@dataclass(slots=True)
class WebhookChannelConfig:
    """Per-channel config for generic webhooks."""

    url: str = ""
    secret: str = ""
    method: str = "POST"


@dataclass(slots=True)
class EmailChannelConfig:
    """Per-channel config for email (SMTP/IMAP)."""

    smtp_host: str = ""
    smtp_port: int = 587
    imap_host: str = ""
    imap_port: int = 993
    username: str = ""
    password: str = ""
    use_tls: bool = True


@dataclass(slots=True)
class WhatsAppChannelConfig:
    """Per-channel config for WhatsApp Cloud API."""

    access_token: str = ""
    phone_number_id: str = ""


@dataclass(slots=True)
class SignalChannelConfig:
    """Per-channel config for Signal (via signal-cli REST API)."""

    api_url: str = ""
    phone_number: str = ""


@dataclass(slots=True)
class GoogleChatChannelConfig:
    """Per-channel config for Google Chat webhooks."""

    webhook_url: str = ""


@dataclass(slots=True)
class IRCChannelConfig:
    """Per-channel config for IRC."""

    server: str = ""
    port: int = 6667
    nick: str = ""
    password: str = ""
    use_tls: bool = False


@dataclass(slots=True)
class WebChatChannelConfig:
    """Per-channel config for in-memory webchat."""

    pass


@dataclass(slots=True)
class TeamsChannelConfig:
    """Per-channel config for Microsoft Teams (Bot Framework)."""

    app_id: str = ""
    app_password: str = ""
    service_url: str = ""


@dataclass(slots=True)
class MatrixChannelConfig:
    """Per-channel config for Matrix."""

    homeserver: str = ""
    access_token: str = ""


@dataclass(slots=True)
class MattermostChannelConfig:
    """Per-channel config for Mattermost."""

    url: str = ""
    token: str = ""


@dataclass(slots=True)
class FeishuChannelConfig:
    """Per-channel config for Feishu (Lark)."""

    app_id: str = ""
    app_secret: str = ""


@dataclass(slots=True)
class BlueBubblesChannelConfig:
    """Per-channel config for BlueBubbles (iMessage bridge)."""

    url: str = ""
    password: str = ""


@dataclass(slots=True)
class WhatsAppBaileysChannelConfig:
    """Per-channel config for WhatsApp via Baileys protocol."""

    auth_dir: str = ""  # Defaults to ~/.openjarvis/whatsapp_auth
    assistant_name: str = "Jarvis"
    assistant_has_own_number: bool = False


@dataclass
class ChannelConfig:
    """Channel messaging settings."""

    enabled: bool = False
    default_channel: str = ""
    default_agent: str = "simple"
    telegram: TelegramChannelConfig = field(default_factory=TelegramChannelConfig)
    discord: DiscordChannelConfig = field(default_factory=DiscordChannelConfig)
    slack: SlackChannelConfig = field(default_factory=SlackChannelConfig)
    webhook: WebhookChannelConfig = field(default_factory=WebhookChannelConfig)
    email: EmailChannelConfig = field(default_factory=EmailChannelConfig)
    whatsapp: WhatsAppChannelConfig = field(default_factory=WhatsAppChannelConfig)
    signal: SignalChannelConfig = field(default_factory=SignalChannelConfig)
    google_chat: GoogleChatChannelConfig = field(
        default_factory=GoogleChatChannelConfig,
    )
    irc: IRCChannelConfig = field(default_factory=IRCChannelConfig)
    webchat: WebChatChannelConfig = field(default_factory=WebChatChannelConfig)
    teams: TeamsChannelConfig = field(default_factory=TeamsChannelConfig)
    matrix: MatrixChannelConfig = field(default_factory=MatrixChannelConfig)
    mattermost: MattermostChannelConfig = field(default_factory=MattermostChannelConfig)
    feishu: FeishuChannelConfig = field(default_factory=FeishuChannelConfig)
    bluebubbles: BlueBubblesChannelConfig = field(
        default_factory=BlueBubblesChannelConfig,
    )
    whatsapp_baileys: WhatsAppBaileysChannelConfig = field(
        default_factory=WhatsAppBaileysChannelConfig,
    )


@dataclass(slots=True)
class CapabilitiesConfig:
    """RBAC capability system settings."""

    enabled: bool = False
    policy_path: str = ""


@dataclass(slots=True)
class SecurityConfig:
    """Security guardrails settings."""

    enabled: bool = True
    scan_input: bool = True
    scan_output: bool = True
    mode: str = "redact"  # "redact" | "warn" | "block"
    secret_scanner: bool = True
    pii_scanner: bool = True
    audit_log_path: str = str(DEFAULT_CONFIG_DIR / "audit.db")
    enforce_tool_confirmation: bool = True
    merkle_audit: bool = True
    signing_key_path: str = ""
    ssrf_protection: bool = True
    rate_limit_enabled: bool = True
    rate_limit_rpm: int = 60
    rate_limit_burst: int = 10
    local_engine_bypass: bool = False
    local_tool_bypass: bool = False
    profile: str = ""
    vault_key_path: str = str(DEFAULT_CONFIG_DIR / ".vault_key")
    capabilities: CapabilitiesConfig = field(default_factory=CapabilitiesConfig)


# ---------------------------------------------------------------------------
# Security profile presets
# ---------------------------------------------------------------------------

_SECURITY_PROFILES: Dict[str, Dict[str, Dict[str, Any]]] = {
    "personal": {
        "security": {
            "mode": "redact",
            "rate_limit_enabled": True,
            "local_engine_bypass": False,
            "local_tool_bypass": False,
        },
        "server": {
            "host": "127.0.0.1",
        },
    },
    "shared": {
        "security": {
            "mode": "redact",
            "rate_limit_enabled": True,
            "local_engine_bypass": False,
            "local_tool_bypass": False,
        },
        "server": {
            "host": "127.0.0.1",
        },
    },
    "server": {
        "security": {
            "mode": "block",
            "rate_limit_enabled": True,
            "rate_limit_rpm": 30,
            "rate_limit_burst": 5,
            "local_engine_bypass": False,
            "local_tool_bypass": False,
        },
        "server": {
            "host": "0.0.0.0",
        },
    },
}


def apply_security_profile(
    security_cfg: "SecurityConfig",
    server_cfg: "ServerConfig | None",
    *,
    overrides: "set[str] | None" = None,
) -> None:
    """Expand a named security profile into config fields.

    Fields in *overrides* (explicitly set by the user in TOML) are
    not overwritten by the profile.
    """
    profile = security_cfg.profile
    if not profile:
        return

    if profile not in _SECURITY_PROFILES:
        raise ValueError(
            f"Unknown security profile '{profile}'. "
            f"Valid profiles: {', '.join(_SECURITY_PROFILES)}"
        )

    _overrides = overrides or set()
    pdef = _SECURITY_PROFILES[profile]

    for key, value in pdef.get("security", {}).items():
        if key not in _overrides and hasattr(security_cfg, key):
            setattr(security_cfg, key, value)

    if server_cfg is not None:
        for key, value in pdef.get("server", {}).items():
            if key not in _overrides and hasattr(server_cfg, key):
                setattr(server_cfg, key, value)


@dataclass(slots=True)
class SandboxConfig:
    """Container sandbox settings."""

    enabled: bool = False
    image: str = "openjarvis-sandbox:latest"
    timeout: int = 300
    workspace: str = ""
    mount_allowlist_path: str = ""
    max_concurrent: int = 5
    runtime: str = "docker"
    wasm_fuel_limit: int = 1_000_000
    wasm_memory_limit_mb: int = 256


@dataclass(slots=True)
class SchedulerConfig:
    """Task scheduler settings."""

    enabled: bool = False
    poll_interval: int = 60
    db_path: str = ""  # Defaults to ~/.openjarvis/scheduler.db


@dataclass(slots=True)
class WorkflowConfig:
    """Workflow engine settings."""

    enabled: bool = False
    max_parallel: int = 4
    default_node_timeout: int = 300


@dataclass(slots=True)
class SessionConfig:
    """Cross-channel session settings."""

    enabled: bool = False
    max_age_hours: float = 24.0
    consolidation_threshold: int = 100
    db_path: str = str(DEFAULT_CONFIG_DIR / "sessions.db")


@dataclass(slots=True)
class A2AConfig:
    """Agent-to-Agent protocol settings."""

    enabled: bool = False


@dataclass(slots=True)
class OperatorsConfig:
    """Operator lifecycle settings."""

    enabled: bool = False
    manifests_dir: str = "~/.openjarvis/operators"
    auto_activate: str = ""  # Comma-separated operator IDs


@dataclass(slots=True)
class SpeechConfig:
    """Speech-to-text settings."""

    backend: str = "auto"  # "auto", "faster-whisper", "openai", "deepgram"
    model: str = "base"  # Whisper model size: tiny, base, small, medium, large-v3
    language: str = ""  # Empty = auto-detect
    device: str = "auto"  # "auto", "cpu", "cuda" - CTranslate2 resolves
    compute_type: str = "auto"  # "auto" = fastest type the HARDWARE supports


@dataclass(slots=True)
class OptimizeConfig:
    """Configuration optimization settings."""

    max_trials: int = 20
    early_stop_patience: int = 5
    optimizer_model: str = "claude-sonnet-4-6"
    optimizer_provider: str = "anthropic"
    benchmark: str = ""
    max_samples: int = 50
    judge_model: str = "gpt-5-mini-2025-08-07"
    db_path: str = str(DEFAULT_CONFIG_DIR / "optimize.db")


@dataclass(slots=True)
class AgentManagerConfig:
    """Persistent agent manager settings."""

    enabled: bool = True
    db_path: str = str(DEFAULT_CONFIG_DIR / "agents.db")


@dataclass(slots=True)
class MemoryFilesConfig:
    """Persistent memory-file paths and nudge settings."""

    soul_path: str = "~/.openjarvis/SOUL.md"
    memory_path: str = "~/.openjarvis/MEMORY.md"
    user_path: str = "~/.openjarvis/USER.md"
    nudge_interval: int = 10


@dataclass(slots=True)
class SystemPromptConfig:
    """Limits and strategy for system-prompt assembly."""

    soul_max_chars: int = 4000
    memory_max_chars: int = 2500
    user_max_chars: int = 1500
    skill_desc_max_chars: int = 60
    truncation_strategy: str = "head_tail"


@dataclass(slots=True)
class CompressionConfig:
    """Configuration for context compression."""

    enabled: bool = True
    threshold: float = 0.50
    strategy: str = "session_consolidation"


@dataclass(slots=True)
class SkillSourceConfig:
    """Configuration for a single skill source (Hermes, OpenClaw, GitHub)."""

    source: str = ""  # "hermes", "openclaw", or "github"
    url: str = ""  # required when source = "github"
    filter: Dict[str, Any] = field(default_factory=dict)
    auto_update: bool = False


@dataclass(slots=True)
class SkillsConfig:
    """Configuration for agent-authored procedural skills."""

    enabled: bool = True
    skills_dir: str = "~/.openjarvis/skills/"
    active: str = "*"
    auto_discover: bool = True
    auto_sync: bool = False
    nudge_interval: int = 15
    index_repo: str = "https://github.com/openjarvis/skill-index.git"
    index_dir: str = "~/.openjarvis/skill-index/"
    max_depth: int = 5
    sandbox_dangerous: bool = True
    sources: List[SkillSourceConfig] = field(default_factory=list)


@dataclass
class DigestSectionConfig:
    """Configuration for a single digest section."""

    sources: List[str] = field(default_factory=list)
    max_items: int = 10
    priority_contacts: List[str] = field(default_factory=list)


@dataclass
class DigestConfig:
    """Configuration for the morning digest feature."""

    enabled: bool = False
    schedule: str = "0 6 * * *"
    timezone: str = "America/Los_Angeles"
    persona: str = "jarvis"
    sections: List[str] = field(
        default_factory=lambda: ["messages", "calendar", "health", "world"]
    )
    optional_sections: List[str] = field(
        default_factory=lambda: ["github", "financial", "music", "fitness"]
    )
    honorific: str = "sir"
    voice_id: str = ""
    voice_speed: float = 1.0
    tts_backend: str = "cartesia"
    messages: DigestSectionConfig = field(
        default_factory=lambda: DigestSectionConfig(
            sources=["gmail", "slack", "google_tasks"]
        )
    )
    calendar: DigestSectionConfig = field(
        default_factory=lambda: DigestSectionConfig(sources=["gcalendar"])
    )
    health: DigestSectionConfig = field(
        default_factory=lambda: DigestSectionConfig(sources=["oura", "apple_health"])
    )
    world: DigestSectionConfig = field(
        default_factory=lambda: DigestSectionConfig(sources=[])
    )


@dataclass
class JarvisConfig:
    """Top-level configuration for OpenJarvis."""

    installed_at: str = ""
    installer_version: str = ""
    hardware: HardwareInfo = field(default_factory=HardwareInfo)
    engine: EngineConfig = field(default_factory=EngineConfig)
    intelligence: IntelligenceConfig = field(default_factory=IntelligenceConfig)
    learning: LearningConfig = field(default_factory=LearningConfig)
    tools: ToolsConfig = field(default_factory=ToolsConfig)
    agent: AgentConfig = field(default_factory=AgentConfig)
    server: ServerConfig = field(default_factory=ServerConfig)
    telemetry: TelemetryConfig = field(default_factory=TelemetryConfig)
    analytics: AnalyticsConfig = field(default_factory=AnalyticsConfig)
    traces: TracesConfig = field(default_factory=TracesConfig)
    channel: ChannelConfig = field(default_factory=ChannelConfig)
    security: SecurityConfig = field(default_factory=SecurityConfig)
    sandbox: SandboxConfig = field(default_factory=SandboxConfig)
    scheduler: SchedulerConfig = field(default_factory=SchedulerConfig)
    workflow: WorkflowConfig = field(default_factory=WorkflowConfig)
    sessions: SessionConfig = field(default_factory=SessionConfig)
    a2a: A2AConfig = field(default_factory=A2AConfig)
    operators: OperatorsConfig = field(default_factory=OperatorsConfig)
    speech: SpeechConfig = field(default_factory=SpeechConfig)
    optimize: OptimizeConfig = field(default_factory=OptimizeConfig)
    agent_manager: AgentManagerConfig = field(default_factory=AgentManagerConfig)
    memory_files: MemoryFilesConfig = field(default_factory=MemoryFilesConfig)
    system_prompt: SystemPromptConfig = field(default_factory=SystemPromptConfig)
    compression: CompressionConfig = field(default_factory=CompressionConfig)
    skills: SkillsConfig = field(default_factory=SkillsConfig)
    digest: DigestConfig = field(default_factory=DigestConfig)
    mining: Optional["MiningConfig"] = None

    @property
    def memory(self) -> StorageConfig:
        """Backward-compatible accessor ΓÇö canonical location is tools.storage."""
        return self.tools.storage

    @memory.setter
    def memory(self, value: StorageConfig) -> None:
        """Backward-compatible setter."""
        self.tools.storage = value


# ---------------------------------------------------------------------------
# Config key validation
# ---------------------------------------------------------------------------

# Sections that users may set via ``jarvis config set``.
# ``hardware`` is auto-detected and not user-settable.
_SETTABLE_SECTIONS = frozenset(JarvisConfig.__dataclass_fields__.keys()) - {
    "hardware",
    "mining",
}


def validate_config_key(dotted_key: str) -> type:
    """Validate a dotted config key and return the leaf field's Python type.

    Raises :class:`ValueError` when the key does not map to a known field.
    The function walks the ``JarvisConfig`` dataclass hierarchy using
    ``dataclasses.fields()``.

    Examples::

        validate_config_key("engine.ollama.host")      # -> str
        validate_config_key("intelligence.temperature") # -> float
    """
    from dataclasses import fields as dc_fields

    parts = dotted_key.split(".")
    if len(parts) < 2:
        raise ValueError(
            f"Config key must have at least two segments (e.g. engine.default), "
            f"got: {dotted_key!r}"
        )

    if parts[0] not in _SETTABLE_SECTIONS:
        raise ValueError(
            f"Unknown config key: {dotted_key!r} "
            f"(valid top-level sections: {sorted(_SETTABLE_SECTIONS)})"
        )

    # Walk the dataclass tree
    current_cls = JarvisConfig
    for i, part in enumerate(parts):
        field_map = {f.name: f for f in dc_fields(current_cls)}
        if part not in field_map:
            path_so_far = ".".join(parts[: i + 1])
            raise ValueError(
                f"Unknown config key: {dotted_key!r} "
                f"(no field {part!r} at {path_so_far}; "
                f"valid fields: {sorted(field_map.keys())})"
            )
        fld = field_map[part]
        # Resolve the type ΓÇö unwrap Optional, etc.
        fld_type = fld.type
        if isinstance(fld_type, str):
            # Evaluate forward references in the config module namespace
            import openjarvis.core.config as _cfg_mod

            fld_type = eval(fld_type, vars(_cfg_mod))  # noqa: S307

        if i == len(parts) - 1:
            # Leaf ΓÇö return the primitive type
            return fld_type
        else:
            # Must be a nested dataclass
            if not hasattr(fld_type, "__dataclass_fields__"):
                path_so_far = ".".join(parts[: i + 1])
                raise ValueError(
                    f"Unknown config key: {dotted_key!r} "
                    f"({path_so_far} is a leaf of type {fld_type.__name__}, "
                    f"not a section)"
                )
            current_cls = fld_type

    # Should not reach here, but satisfy type checker
    raise ValueError(f"Unknown config key: {dotted_key!r}")


# ---------------------------------------------------------------------------
# TOML loading
# ---------------------------------------------------------------------------


def _apply_toml_section(target: Any, section: Dict[str, Any]) -> None:
    """Overlay TOML key/value pairs onto a dataclass instance.

    Recursively handles nested dicts when the target attribute is itself
    a dataclass.  Normalises TOML arrays to comma-separated strings ΓÇö both
    for dataclass fields annotated as ``str`` and for backward-compat
    property setters that expect string input.
    """
    for key, value in section.items():
        if hasattr(target, key):
            if isinstance(value, dict):
                nested = getattr(target, key)
                if hasattr(nested, "__dataclass_fields__"):
                    _apply_toml_section(nested, value)
                else:
                    setattr(target, key, value)
            else:
                # Normalise TOML arrays ΓåÆ comma-separated string.
                # Covers both real dataclass fields and backward-compat
                # property setters (e.g. reward_weights, default_tools).
                if isinstance(value, list):
                    is_str_field = False
                    if hasattr(target, "__dataclass_fields__"):
                        field_obj = target.__dataclass_fields__.get(key)
                        if field_obj is not None and field_obj.type in ("str", str):
                            is_str_field = True
                        elif field_obj is None:
                            # Property, not a real field ΓÇö normalise to string
                            is_str_field = True
                    if is_str_field:
                        value = ",".join(str(v) for v in value)
                setattr(target, key, value)


def _migrate_toml_data(data: Dict[str, Any], cfg: "JarvisConfig") -> None:
    """Migrate old-format TOML keys to new structure in-place.

    Handles cross-section moves that can't be solved by backward-compat
    properties alone (e.g. ``agent.temperature`` ΓåÆ ``intelligence.temperature``).
    """
    # agent.temperature / agent.max_tokens ΓåÆ intelligence.*
    if "agent" in data:
        agent_data = data["agent"]
        intel_data = data.setdefault("intelligence", {})
        for moved_key in ("temperature", "max_tokens"):
            if moved_key in agent_data:
                intel_data.setdefault(moved_key, agent_data.pop(moved_key))

    # context_injection from memory / tools.storage ΓåÆ agent.context_from_memory
    for src_section in ("memory",):
        src = data.get(src_section, {})
        if isinstance(src, dict) and "context_injection" in src:
            data.setdefault("agent", {}).setdefault(
                "context_from_memory",
                src.pop("context_injection"),
            )

    if "tools" in data:
        tools_data = data["tools"]
        if isinstance(tools_data, dict):
            storage_sub = tools_data.get("storage", {})
            if isinstance(storage_sub, dict) and "context_injection" in storage_sub:
                data.setdefault("agent", {}).setdefault(
                    "context_from_memory",
                    storage_sub.pop("context_injection"),
                )


def _parse_mining_section(data: dict) -> Optional["MiningConfig"]:
    """Parse the ``[mining]`` TOML section into a ``MiningConfig``.

    Returns None if the section is absent. Resolves the ``submit_target``
    string into a ``SoloTarget`` or ``PoolTarget`` tagged union.
    """
    if "mining" not in data:
        return None

    # Lazy runtime import to break the import cycle: ``mining/_stubs.py``
    # imports ``HardwareInfo`` from this module at its top level. By the
    # time ``_parse_mining_section`` is called, ``core.config`` is already
    # fully initialized in ``sys.modules``, so the cycle is harmless.
    from openjarvis.mining._stubs import MiningConfig, PoolTarget, SoloTarget

    section = data["mining"]
    extra = section.get("extra", {}) or {}

    target_str = section.get("submit_target", "solo")
    submit_target: Any
    if target_str == "solo":
        submit_target = SoloTarget(
            pearld_rpc_url=extra.get("pearld_rpc_url", "http://localhost:44107")
        )
    elif isinstance(target_str, str) and target_str.startswith("pool:"):
        submit_target = PoolTarget(url=target_str[len("pool:") :])
    else:
        raise ValueError(
            f"[mining].submit_target must be 'solo' or 'pool:<url>', got {target_str!r}"
        )

    return MiningConfig(
        provider=section["provider"],
        wallet_address=section["wallet_address"],
        submit_target=submit_target,
        fee_bps=int(section.get("fee_bps", 0)),
        fee_payout_address=section.get("fee_payout_address") or None,
        extra={k: v for k, v in extra.items()},
    )


@functools.lru_cache(maxsize=1)
def load_config(path: Optional[Path] = None) -> JarvisConfig:
    """Detect hardware, build defaults, overlay TOML overrides.

    Parameters
    ----------
    path:
        Explicit config file. If not set, uses ``OPENJARVIS_CONFIG`` when set,
        otherwise ``~/.openjarvis/config.toml``.
    """
    _ensure_config_dir()
    hw = detect_hardware()
    cfg = JarvisConfig(hardware=hw)
    cfg.engine.default = recommend_engine(hw)

    if path is not None:
        config_path = Path(path)
    elif os.environ.get("OPENJARVIS_CONFIG"):
        config_path = Path(os.environ["OPENJARVIS_CONFIG"]).expanduser().resolve()
    else:
        config_path = DEFAULT_CONFIG_PATH
    if config_path.exists():
        with open(config_path, "rb") as fh:
            data = tomllib.load(fh)

        # Run backward-compat migrations before applying
        _migrate_toml_data(data, cfg)

        # All top-level sections ΓÇö recursive _apply_toml_section handles
        # nested sub-configs (engine.ollama, learning.routing, channel.*, etc.)
        top_sections = (
            "engine",
            "intelligence",
            "learning",
            "agent",
            "server",
            "telemetry",
            "analytics",
            "traces",
            "security",
            "channel",
            "tools",
            "sandbox",
            "scheduler",
            "workflow",
            "sessions",
            "a2a",
            "operators",
            "speech",
            "optimize",
            "agent_manager",
            "digest",
        )
        for section_name in top_sections:
            if section_name in data:
                _apply_toml_section(
                    getattr(cfg, section_name),
                    data[section_name],
                )

        # Memory: accept [memory] (old) ΓåÆ maps to tools.storage
        if "memory" in data:
            _apply_toml_section(cfg.tools.storage, data["memory"])

        # Top-level install provenance (installed_at, installer_version)
        for key in ("installed_at", "installer_version"):
            if key in data:
                setattr(cfg, key, data[key])

        # Expand security profile (user TOML overrides take precedence)
        _user_security_keys = set(data.get("security", {}).keys())
        apply_security_profile(cfg.security, cfg.server, overrides=_user_security_keys)

        # Mining: dedicated parser for tagged-union submit_target
        cfg.mining = _parse_mining_section(data)

    # Apply profile even without a config file (in case defaults set one)
    if not config_path.exists() and cfg.security.profile:
        apply_security_profile(cfg.security, cfg.server)

    return cfg


# ---------------------------------------------------------------------------
# Default TOML generation (for ``jarvis init``)
# ---------------------------------------------------------------------------


def generate_minimal_toml(
    hw: HardwareInfo, engine: str | None = None, *, host: str | None = None
) -> str:
    """Render a minimal TOML config with only essential settings."""
    engine = engine or recommend_engine(hw)
    model = recommend_model(hw, engine)
    gpu_comment = ""
    if hw.gpu:
        mem_label = "unified memory" if hw.gpu.vendor == "apple" else "VRAM"
        gpu_comment = f"\n# GPU: {hw.gpu.name} ({hw.gpu.vram_gb} GB {mem_label})"
    if host:
        engine_host_section = f'\n[engine.{engine}]\nhost = "{host}"\n'
    else:
        engine_host_section = (
            f"\n[engine.{engine}]\n"
            f'# host = "http://localhost:11434"  '
            f"# set to remote URL if engine runs elsewhere\n"
        )
    return f"""\
# OpenJarvis configuration
# Hardware: {hw.cpu_brand} ({hw.cpu_count} cores, {hw.ram_gb} GB RAM){gpu_comment}
# Full reference config: jarvis init --full

[engine]
default = "{engine}"
{engine_host_section}
[intelligence]
default_model = "{model}"

[agent]
default_agent = "simple"

[tools]
enabled = ["code_interpreter", "web_search", "file_read", "shell_exec"]
"""


def generate_default_toml(
    hw: HardwareInfo, engine: str | None = None, *, host: str | None = None
) -> str:
    """Render a commented TOML string suitable for ``~/.openjarvis/config.toml``."""
    engine = engine or recommend_engine(hw)
    model = recommend_model(hw, engine)
    gpu_line = ""
    if hw.gpu:
        gpu_line = f"# Detected GPU: {hw.gpu.name} ({hw.gpu.vram_gb} GB VRAM)"

    model_comment = ""
    if model:
        model_comment = "  # recommended for your hardware"

    result = f"""\
# OpenJarvis configuration
# Generated by `jarvis init`
#
# Hardware: {hw.cpu_brand} ({hw.cpu_count} cores, {hw.ram_gb} GB RAM)
{gpu_line}

[engine]
default = "{engine}"

[engine.ollama]
host = "http://localhost:11434"

[engine.vllm]
host = "http://localhost:8010"

[engine.sglang]
host = "http://localhost:30000"

# [engine.llamacpp]
# host = "http://localhost:8080"
# binary_path = ""

[engine.mlx]
host = "http://localhost:8080"

# [engine.lmstudio]
# host = "http://localhost:1234"

# [engine.exo]
# host = "http://localhost:52415"

# [engine.nexa]
# host = "http://localhost:18181"
# device = ""  # cpu, gpu, npu

# [engine.uzu]
# host = "http://localhost:8080"

# [engine.apple_fm]
# host = "http://localhost:8079"

[intelligence]
default_model = "{model}"{model_comment}
fallback_model = ""
# model_path = ""              # Local weights (HF repo, GGUF file, etc.)
# checkpoint_path = ""         # Checkpoint/adapter path
# quantization = "none"        # none, fp8, int8, int4, gguf_q4, gguf_q8
# preferred_engine = ""        # Override engine for this model (e.g., "vllm")
# provider = ""                # local, openai, anthropic, google
temperature = 0.7
max_tokens = 1024
# top_p = 0.9
# top_k = 40
# repetition_penalty = 1.0
# stop_sequences = ""

[agent]
default_agent = "simple"
max_turns = 10
# tools = ""                   # Comma-separated tool names
# objective = ""               # Concise purpose string
# system_prompt = ""           # Inline system prompt
# system_prompt_path = ""      # Path to system prompt file
context_from_memory = true

[tools.storage]
default_backend = "sqlite"

[tools.mcp]
enabled = true

# [tools.browser]
# headless = true
# timeout_ms = 30000
# viewport_width = 1280
# viewport_height = 720

[server]
host = "0.0.0.0"
port = 8010
agent = "native_openhands"

[learning]
enabled = false
update_interval = 100
# auto_update = false

[learning.routing]
policy = "heuristic"
# min_samples = 5

# [learning.intelligence]
# policy = "none"              # "sft" to learn from traces

# [learning.agent]
# policy = "none"              # "agent_advisor" | "icl_updater"

# [learning.metrics]
# accuracy_weight = 0.6
# latency_weight = 0.2
# cost_weight = 0.1
# efficiency_weight = 0.1

[telemetry]
enabled = true
# gpu_metrics = false
# gpu_poll_interval_ms = 50

[traces]
enabled = false

[channel]
enabled = false
default_agent = "simple"

# [channel.telegram]
# bot_token = ""  # Or set TELEGRAM_BOT_TOKEN env var

# [channel.discord]
# bot_token = ""  # Or set DISCORD_BOT_TOKEN env var

# [channel.slack]
# bot_token = ""  # Or set SLACK_BOT_TOKEN env var

# [channel.webhook]
# url = ""

# [channel.whatsapp]
# access_token = ""      # Or set WHATSAPP_ACCESS_TOKEN env var
# phone_number_id = ""   # Or set WHATSAPP_PHONE_NUMBER_ID env var

# [channel.signal]
# api_url = ""            # signal-cli REST API URL
# phone_number = ""       # Or set SIGNAL_PHONE_NUMBER env var

# [channel.google_chat]
# webhook_url = ""        # Or set GOOGLE_CHAT_WEBHOOK_URL env var

# [channel.irc]
# server = ""
# port = 6667
# nick = ""
# use_tls = false

# [channel.teams]
# app_id = ""             # Or set TEAMS_APP_ID env var
# app_password = ""       # Or set TEAMS_APP_PASSWORD env var

# [channel.matrix]
# homeserver = ""         # Or set MATRIX_HOMESERVER env var
# access_token = ""       # Or set MATRIX_ACCESS_TOKEN env var

# [channel.mattermost]
# url = ""                # Or set MATTERMOST_URL env var
# token = ""              # Or set MATTERMOST_TOKEN env var

# [channel.feishu]
# app_id = ""             # Or set FEISHU_APP_ID env var
# app_secret = ""         # Or set FEISHU_APP_SECRET env var

# [channel.bluebubbles]
# url = ""                # Or set BLUEBUBBLES_URL env var
# password = ""           # Or set BLUEBUBBLES_PASSWORD env var

[security]
enabled = true
mode = "warn"
scan_input = true
scan_output = true
secret_scanner = true
pii_scanner = true
enforce_tool_confirmation = true
ssrf_protection = true
# rate_limit_enabled = false
# rate_limit_rpm = 60
# rate_limit_burst = 10

# [sandbox]
# enabled = false
# image = "openjarvis-sandbox:latest"
# timeout = 300
# max_concurrent = 5
# runtime = "docker"

# [scheduler]
# enabled = false
# poll_interval = 60
# db_path = ""                # Defaults to ~/.openjarvis/scheduler.db

# [channel.whatsapp_baileys]
# auth_dir = ""               # Defaults to ~/.openjarvis/whatsapp_auth
# assistant_name = "Jarvis"
# assistant_has_own_number = false
"""
    if host:
        import re as _re

        pattern = _re.escape(f"[engine.{engine}]") + r"\nhost = \"[^\"]*\""
        replacement = f'[engine.{engine}]\\nhost = "{host}"'
        result = _re.sub(pattern, replacement, result)
    return result


__all__ = [
    "A2AConfig",
    "AgentConfig",
    "AgentManagerConfig",
    "OperatorsConfig",
    "AgentLearningConfig",
    "BlueBubblesChannelConfig",
    "BrowserConfig",
    "CapabilitiesConfig",
    "ChannelConfig",
    "DEFAULT_CONFIG_DIR",
    "DEFAULT_CONFIG_PATH",
    "DiscordChannelConfig",
    "EmailChannelConfig",
    "EngineConfig",
    "FeishuChannelConfig",
    "GoogleChatChannelConfig",
    "GpuInfo",
    "HardwareInfo",
    "IRCChannelConfig",
    "IntelligenceConfig",
    "IntelligenceLearningConfig",
    "JarvisConfig",
    "LearningConfig",
    "LMStudioEngineConfig",
    "LlamaCppEngineConfig",
    "MCPConfig",
    "MLXEngineConfig",
    "MatrixChannelConfig",
    "MattermostChannelConfig",
    "MemoryConfig",
    "MetricsConfig",
    "OllamaEngineConfig",
    "OptimizeConfig",
    "RoutingLearningConfig",
    "SGLangEngineConfig",
    "SandboxConfig",
    "SchedulerConfig",
    "SecurityConfig",
    "ServerConfig",
    "SessionConfig",
    "SignalChannelConfig",
    "SlackChannelConfig",
    "SpeechConfig",
    "StorageConfig",
    "TeamsChannelConfig",
    "TelegramChannelConfig",
    "TelemetryConfig",
    "ToolsConfig",
    "TracesConfig",
    "VLLMEngineConfig",
    "WebChatChannelConfig",
    "WebhookChannelConfig",
    "WhatsAppBaileysChannelConfig",
    "WhatsAppChannelConfig",
    "WorkflowConfig",
    "detect_hardware",
    "generate_default_toml",
    "generate_minimal_toml",
    "load_config",
    "recommend_engine",
    "recommend_model",
    "validate_config_key",
]

## ===== src/openjarvis/core/config.py : STAGE 3 =====
"""Configuration loading, hardware detection, and engine recommendation.

User configuration lives at ``~/.openjarvis/config.toml``.  ``load_config()``
detects hardware, fills sensible defaults, then overlays any user overrides
found in the TOML file.
"""

from __future__ import annotations

import functools
import os
import platform
import shutil
import subprocess
from dataclasses import dataclass, field, is_dataclass
from pathlib import Path
from typing import (
    TYPE_CHECKING,
    Any,
    Dict,
    List,
    Optional,
    get_args,
    get_origin,
    get_type_hints,
)

from openjarvis.core.paths import (
    ConfigurationError,
    get_cache_dir,
    get_config_dir,
    get_config_path,
    get_data_dir,
)

if TYPE_CHECKING:
    # Only used by type-checkers (mypy/pyright) for the ``JarvisConfig.mining``
    # field annotation. The runtime import is deferred inside
    # ``_parse_mining_section()`` to break the import cycle:
    # ``mining/_stubs.py`` imports ``HardwareInfo`` from this module at its
    # top level.
    from openjarvis.mining._stubs import MiningConfig

try:
    import tomllib  # Python 3.11+
except ModuleNotFoundError:
    import tomli as tomllib  # type: ignore[no-redef]

# ---------------------------------------------------------------------------
# Hardware dataclasses
# ---------------------------------------------------------------------------

# Legacy names, kept for the ~45 modules that import them. They are resolved
# once at import via the env-aware resolver in ``openjarvis.core.paths`` (the
# install-script model: ``OPENJARVIS_HOME`` / ``XDG_DATA_HOME`` are set before
# the process starts). They are real module attributes ΓÇö not computed lazily ΓÇö
# so existing tests can ``monkeypatch.setattr`` them and so dataclass-instance
# defaults stay consistent. Code that must react to a mid-process env change
# (or wants the override regardless of import order) should call
# ``get_config_dir()`` / ``get_config_path()`` directly; the dataclass field
# defaults below already do this via ``default_factory``.
DEFAULT_CONFIG_DIR = get_config_dir()
DEFAULT_CONFIG_PATH = get_config_path()


def _ensure_config_dir() -> Path:
    """Ensure the config directory exists with restrictive permissions."""
    from openjarvis.security.file_utils import secure_mkdir

    return secure_mkdir(get_config_dir())


@dataclass(slots=True)
class GpuInfo:
    """Detected GPU metadata."""

    vendor: str = ""
    name: str = ""
    vram_gb: float = 0.0
    compute_capability: str = ""
    count: int = 0


@dataclass(slots=True)
class HardwareInfo:
    """Detected system hardware."""

    platform: str = ""
    cpu_brand: str = ""
    cpu_count: int = 0
    ram_gb: float = 0.0
    gpu: Optional[GpuInfo] = None


# ---------------------------------------------------------------------------
# Hardware detection helpers
# ---------------------------------------------------------------------------


def _run_cmd(cmd: list[str]) -> str:
    """Run a command and return stripped stdout, or empty string on failure."""
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=10,  # noqa: S603
        )
        return result.stdout.strip()
    except (FileNotFoundError, subprocess.TimeoutExpired, OSError):
        return ""


def _detect_nvidia_gpu() -> Optional[GpuInfo]:
    if not shutil.which("nvidia-smi"):
        return None
    raw = _run_cmd(
        [
            "nvidia-smi",
            "--query-gpu=name,memory.total,count,compute_cap",
            "--format=csv,noheader,nounits",
        ]
    )
    if not raw:
        return None
    try:
        first_line = raw.splitlines()[0]
        parts = [p.strip() for p in first_line.split(",")]
        name = parts[0]
        vram_mb = float(parts[1])
        count = int(parts[2])
        compute_capability = parts[3] if len(parts) > 3 else ""
        return GpuInfo(
            vendor="nvidia",
            name=name,
            vram_gb=round(vram_mb / 1024, 1),
            compute_capability=compute_capability,
            count=count,
        )
    except (IndexError, ValueError):
        return None


def _detect_amd_gpu() -> Optional[GpuInfo]:
    if not shutil.which("rocm-smi"):
        return None
    raw = _run_cmd(["rocm-smi", "--showproductname"])
    if not raw:
        return None
    name = raw.splitlines()[0] if raw else "AMD GPU"

    # Parse VRAM from rocm-smi --showmeminfo vram
    vram_gb = 0.0
    try:
        vram_raw = _run_cmd(["rocm-smi", "--showmeminfo", "vram"])
        for line in vram_raw.splitlines():
            if "Total Memory (B):" in line:
                vram_bytes = int(line.split(":")[-1].strip())
                vram_gb = round(vram_bytes / (1024**3), 1)
                break
    except (ValueError, IndexError):
        vram_gb = 0.0

    # Parse GPU count from rocm-smi --showallinfo
    count = 1
    try:
        allinfo_raw = _run_cmd(["rocm-smi", "--showallinfo"])
        import re

        gpu_ids = set(re.findall(r"GPU\[(\d+)\]", allinfo_raw))
        if gpu_ids:
            count = len(gpu_ids)
    except (ValueError, IndexError):
        count = 1

    return GpuInfo(vendor="amd", name=name, vram_gb=vram_gb, count=count)


def _detect_apple_gpu() -> Optional[GpuInfo]:
    if platform.system() != "Darwin":
        return None
    raw = _run_cmd(["system_profiler", "SPDisplaysDataType"])
    if "Apple" not in raw:
        return None
    # Rough extraction ΓÇö "Apple M2 Max" etc.
    ram_gb = _total_ram_gb()
    for line in raw.splitlines():
        line = line.strip()
        if "Chipset Model" in line:
            name = line.split(":")[-1].strip()
            return GpuInfo(vendor="apple", name=name, vram_gb=ram_gb, count=1)
    return GpuInfo(vendor="apple", name="Apple Silicon", vram_gb=ram_gb, count=1)


def _detect_cpu_brand() -> str:
    """Best-effort CPU brand string."""
    if platform.system() == "Darwin":
        brand = _run_cmd(["sysctl", "-n", "machdep.cpu.brand_string"])
        if brand:
            return brand
    cpuinfo = Path("/proc/cpuinfo")
    if cpuinfo.exists():
        try:
            for line in cpuinfo.read_text().splitlines():
                if line.startswith("model name"):
                    return line.split(":", 1)[1].strip()
        except OSError:
            pass
    return platform.processor() or "unknown"


def _total_ram_gb() -> float:
    try:
        if platform.system() == "Darwin":
            raw = _run_cmd(["sysctl", "-n", "hw.memsize"])
            return round(int(raw) / (1024**3), 1) if raw else 0.0
        if platform.system() == "Windows":
            import ctypes

            class _MemoryStatusEx(ctypes.Structure):
                _fields_ = [
                    ("dwLength", ctypes.c_ulong),
                    ("dwMemoryLoad", ctypes.c_ulong),
                    ("ullTotalPhys", ctypes.c_ulonglong),
                    ("ullAvailPhys", ctypes.c_ulonglong),
                    ("ullTotalPageFile", ctypes.c_ulonglong),
                    ("ullAvailPageFile", ctypes.c_ulonglong),
                    ("ullTotalVirtual", ctypes.c_ulonglong),
                    ("ullAvailVirtual", ctypes.c_ulonglong),
                    ("sullAvailExtendedVirtual", ctypes.c_ulonglong),
                ]

            stat = _MemoryStatusEx()
            stat.dwLength = ctypes.sizeof(_MemoryStatusEx)
            if ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(stat)):
                return round(stat.ullTotalPhys / (1024**3), 1)
            return 0.0
        meminfo = Path("/proc/meminfo")
        if meminfo.exists():
            for line in meminfo.read_text().splitlines():
                if line.startswith("MemTotal"):
                    kb = int(line.split()[1])
                    return round(kb / (1024**2), 1)
    except (OSError, ValueError, AttributeError):
        pass
    return 0.0


def detect_hardware() -> HardwareInfo:
    """Auto-detect hardware capabilities with graceful fallbacks."""
    gpu = _detect_nvidia_gpu() or _detect_amd_gpu() or _detect_apple_gpu()
    return HardwareInfo(
        platform=platform.system().lower(),
        cpu_brand=_detect_cpu_brand(),
        cpu_count=os.cpu_count() or 1,
        ram_gb=_total_ram_gb(),
        gpu=gpu,
    )


# ---------------------------------------------------------------------------
# Engine recommendation
# ---------------------------------------------------------------------------


def recommend_engine(hw: HardwareInfo) -> str:
    """Suggest the best inference engine for the detected hardware."""
    gpu = hw.gpu
    if gpu is None:
        return "llamacpp"
    if gpu.vendor == "apple":
        return "mlx"
    if gpu.vendor == "nvidia":
        # Datacenter cards (A100, H100, L40, etc.) ΓåÆ vllm; consumer ΓåÆ ollama
        datacenter_keywords = ("A100", "H100", "H200", "L40", "A10", "A30")
        if any(kw in gpu.name for kw in datacenter_keywords):
            return "vllm"
        return "ollama"
    if gpu.vendor == "amd":
        # Datacenter cards (MI300, MI325, MI350, MI355) ΓåÆ vllm; consumer ΓåÆ lemonade
        amd_datacenter_keywords = ("MI300", "MI325", "MI350", "MI355")
        if any(kw in gpu.name for kw in amd_datacenter_keywords):
            return "vllm"
        return "lemonade"
    return "llamacpp"


def _available_memory_gb(hw: HardwareInfo) -> float:
    """Return usable memory in GB for model loading."""
    gpu = hw.gpu
    if gpu and gpu.vram_gb > 0:
        return gpu.vram_gb * max(gpu.count, 1) * 0.9
    if hw.ram_gb > 0:
        return (hw.ram_gb - 4) * 0.8
    return 0.0


# Explicit tier table: (max_ram_gb, model_id).
# Walked in order ΓÇö first tier where available_gb <= max_ram is chosen.
# Uses Qwen3.5 MoE models ΓÇö better quality per GB than dense models since
# only a fraction of parameters are active per token.
_MODEL_TIERS = [
    (8, "qwen3.5:2b"),
    (16, "qwen3.5:4b"),
    (32, "qwen3.5:9b"),
    (64, "qwen3.5:27b"),
]
_MODEL_TIER_FALLBACK = "qwen3.5:27b"
_LEMONADE_DEFAULT_MODEL = "Qwen3.6-35B-A3B-GGUF"


def recommend_model(hw: HardwareInfo, engine: str) -> str:
    """Suggest a default model for the selected engine and hardware.

    For Lemonade, prefer the validated Qwen3.6 35B A3B GGUF default.
    For other local engines, use the generic Qwen3.5 tier mapping.
    """
    from openjarvis.intelligence.model_catalog import BUILTIN_MODELS

    available_gb = _available_memory_gb(hw)
    if available_gb <= 0:
        return ""

    if engine == "lemonade":
        return _LEMONADE_DEFAULT_MODEL

    # Build a lookup for quick engine-compatibility checks
    catalog = {spec.model_id: spec for spec in BUILTIN_MODELS}

    # Try explicit tier mapping first
    model_id = _MODEL_TIER_FALLBACK
    for max_ram, tier_model in _MODEL_TIERS:
        if available_gb <= max_ram:
            model_id = tier_model
            break

    spec = catalog.get(model_id)
    if spec and engine in spec.supported_engines:
        return model_id

    # Fallback: scan all Qwen3.5 models for engine compatibility
    candidates = [
        s
        for s in BUILTIN_MODELS
        if s.provider == "alibaba"
        and s.model_id.startswith("qwen3.5:")
        and engine in s.supported_engines
    ]
    candidates.sort(key=lambda s: s.parameter_count_b, reverse=True)
    for s in candidates:
        estimated_gb = s.parameter_count_b * 0.5 * 1.1
        if estimated_gb <= available_gb:
            return s.model_id

    return ""


def estimated_download_gb(parameter_count_b: float) -> float:
    """Estimate download size in GB for Q4_K_M quantized model."""
    return parameter_count_b * 0.5 * 1.1


# ---------------------------------------------------------------------------
# Configuration hierarchy
# ---------------------------------------------------------------------------


@dataclass(slots=True)
class OllamaEngineConfig:
    """Per-engine config for Ollama."""

    host: str = ""


@dataclass(slots=True)
class VLLMEngineConfig:
    """Per-engine config for vLLM."""

    host: str = "http://localhost:8000"


@dataclass(slots=True)
class SGLangEngineConfig:
    """Per-engine config for SGLang."""

    host: str = "http://localhost:30000"


@dataclass(slots=True)
class LlamaCppEngineConfig:
    """Per-engine config for llama.cpp."""

    host: str = "http://localhost:8080"
    binary_path: str = ""


@dataclass(slots=True)
class MLXEngineConfig:
    """Per-engine config for MLX."""

    host: str = "http://localhost:8080"


@dataclass(slots=True)
class LMStudioEngineConfig:
    """Per-engine config for LM Studio."""

    host: str = "http://localhost:1234"


@dataclass(slots=True)
class ExoEngineConfig:
    """Per-engine config for Exo."""

    host: str = "http://localhost:52415"


@dataclass(slots=True)
class NexaEngineConfig:
    """Per-engine config for Nexa."""

    host: str = "http://localhost:18181"
    device: str = ""


@dataclass(slots=True)
class UzuEngineConfig:
    """Per-engine config for Uzu."""

    host: str = "http://localhost:8000"


@dataclass(slots=True)
class AppleFmEngineConfig:
    """Per-engine config for Apple Foundation Models."""

    host: str = "http://localhost:8079"


@dataclass(slots=True)
class GemmaCppEngineConfig:
    """Per-engine config for gemma.cpp."""

    model_path: str = ""
    tokenizer_path: str = ""
    model_type: str = ""
    num_threads: int = 0


@dataclass(slots=True)
class AfmEngineConfig:
    """Per-engine config for in-process Apple Foundation Models.

    No ``host``: this engine runs the SDK in-process rather than talking to a
    server. (The separate ``apple_fm`` engine does have a host ΓÇö it speaks to
    the FastAPI shim.)
    """

    # Standing instructions applied to every session, on top of any system
    # message in the request.
    instructions: str = ""
    # "general" or "content_tagging".
    use_case: str = "general"
    # "default" or "permissive_content_transformations".
    guardrails: str = "default"
    # "greedy" (reproducible, the default here) or "random" (the SDK default).
    sampling: str = "greedy"


@dataclass(slots=True)
class LemonadeEngineConfig:
    """Per-engine config for Lemonade."""

    host: str = "http://localhost:13305"


@dataclass
class EngineConfig:
    """Inference engine settings with nested per-engine configs."""

    default: str = "ollama"
    ollama: OllamaEngineConfig = field(default_factory=OllamaEngineConfig)
    vllm: VLLMEngineConfig = field(default_factory=VLLMEngineConfig)
    sglang: SGLangEngineConfig = field(default_factory=SGLangEngineConfig)
    llamacpp: LlamaCppEngineConfig = field(default_factory=LlamaCppEngineConfig)
    mlx: MLXEngineConfig = field(default_factory=MLXEngineConfig)
    lmstudio: LMStudioEngineConfig = field(default_factory=LMStudioEngineConfig)
    exo: ExoEngineConfig = field(default_factory=ExoEngineConfig)
    nexa: NexaEngineConfig = field(default_factory=NexaEngineConfig)
    uzu: UzuEngineConfig = field(default_factory=UzuEngineConfig)
    apple_fm: AppleFmEngineConfig = field(default_factory=AppleFmEngineConfig)
    afm: AfmEngineConfig = field(default_factory=AfmEngineConfig)
    gemma_cpp: GemmaCppEngineConfig = field(default_factory=GemmaCppEngineConfig)
    lemonade: LemonadeEngineConfig = field(default_factory=LemonadeEngineConfig)

    # Backward-compat properties for old flat attribute names
    @property
    def ollama_host(self) -> str:
        """Deprecated: use ``engine.ollama.host``."""
        return self.ollama.host

    @ollama_host.setter
    def ollama_host(self, value: str) -> None:
        self.ollama.host = value

    @property
    def vllm_host(self) -> str:
        """Deprecated: use ``engine.vllm.host``."""
        return self.vllm.host

    @vllm_host.setter
    def vllm_host(self, value: str) -> None:
        self.vllm.host = value

    @property
    def llamacpp_host(self) -> str:
        """Deprecated: use ``engine.llamacpp.host``."""
        return self.llamacpp.host

    @llamacpp_host.setter
    def llamacpp_host(self, value: str) -> None:
        self.llamacpp.host = value

    @property
    def llamacpp_path(self) -> str:
        """Deprecated: use ``engine.llamacpp.binary_path``."""
        return self.llamacpp.binary_path

    @llamacpp_path.setter
    def llamacpp_path(self, value: str) -> None:
        self.llamacpp.binary_path = value

    @property
    def sglang_host(self) -> str:
        """Deprecated: use ``engine.sglang.host``."""
        return self.sglang.host

    @sglang_host.setter
    def sglang_host(self, value: str) -> None:
        self.sglang.host = value

    @property
    def mlx_host(self) -> str:
        """Deprecated: use ``engine.mlx.host``."""
        return self.mlx.host

    @mlx_host.setter
    def mlx_host(self, value: str) -> None:
        self.mlx.host = value

    @property
    def lmstudio_host(self) -> str:
        """Deprecated: use ``engine.lmstudio.host``."""
        return self.lmstudio.host

    @lmstudio_host.setter
    def lmstudio_host(self, value: str) -> None:
        self.lmstudio.host = value

    @property
    def exo_host(self) -> str:
        """Deprecated: use ``engine.exo.host``."""
        return self.exo.host

    @exo_host.setter
    def exo_host(self, value: str) -> None:
        self.exo.host = value

    @property
    def nexa_host(self) -> str:
        """Deprecated: use ``engine.nexa.host``."""
        return self.nexa.host

    @nexa_host.setter
    def nexa_host(self, value: str) -> None:
        self.nexa.host = value

    @property
    def uzu_host(self) -> str:
        """Deprecated: use ``engine.uzu.host``."""
        return self.uzu.host

    @uzu_host.setter
    def uzu_host(self, value: str) -> None:
        self.uzu.host = value

    @property
    def apple_fm_host(self) -> str:
        """Deprecated: use ``engine.apple_fm.host``."""
        return self.apple_fm.host

    @apple_fm_host.setter
    def apple_fm_host(self, value: str) -> None:
        self.apple_fm.host = value

    @property
    def lemonade_host(self) -> str:
        """Deprecated: use ``engine.lemonade.host``."""
        return self.lemonade.host

    @lemonade_host.setter
    def lemonade_host(self, value: str) -> None:
        self.lemonade.host = value


@dataclass(slots=True)
class IntelligenceConfig:
    """The model ΓÇö identity, paths, quantization, and generation defaults."""

    default_model: str = ""
    # Optional per-CLI preset (used when ``-m`` omitted or ``-m smart``).
    model_chat: str = ""
    model_short: str = ""
    model_long: str = ""
    model_code: str = ""
    fallback_model: str = ""
    model_path: str = ""  # Local weights (HF repo, GGUF file, etc.)
    checkpoint_path: str = ""  # Checkpoint/adapter path
    quantization: str = "none"  # none, fp8, int8, int4, gguf_q4, gguf_q8
    preferred_engine: str = ""  # Override engine for this model (e.g., "vllm")
    provider: str = ""  # local, openai, anthropic, google
    # Generation defaults (overridable per-call)
    temperature: float = 0.7
    max_tokens: int = 1024
    top_p: float = 0.9
    top_k: int = 40
    repetition_penalty: float = 1.0
    stop_sequences: str = ""  # Comma-separated stop strings


@dataclass(slots=True)
class DeepResearchConfig:
    """Planner settings for the web Deep Research endpoint."""

    engine: str = ""  # Empty means use the active chat engine.
    model: str = ""  # Empty means use the active chat model.


@dataclass(slots=True)
class RoutingLearningConfig:
    """Routing sub-policy config within Learning."""

    policy: str = "heuristic"  # heuristic | learned
    min_samples: int = 5  # Min traces before trusting learned routing


@dataclass(slots=True)
class SFTConfig:
    """General-purpose SFT training config. Maps to [learning.intelligence.sft]."""

    model_name: str = "Qwen/Qwen3-1.7B"
    max_seq_length: int = 4096
    num_epochs: int = 3
    batch_size: int = 8
    learning_rate: float = 2e-5
    weight_decay: float = 0.01
    warmup_ratio: float = 0.1
    max_grad_norm: float = 1.0
    gradient_checkpointing: bool = True
    use_lora: bool = True
    lora_rank: int = 16
    lora_alpha: int = 32
    lora_dropout: float = 0.05
    target_modules: str = "q_proj,v_proj"  # comma-separated for TOML compat
    use_4bit: bool = False
    checkpoint_dir: str = "checkpoints/sft"
    min_pairs: int = 10
    agent_filter: str = ""


@dataclass(slots=True)
class GRPOConfig:
    """General-purpose GRPO training config. Maps to [learning.intelligence.grpo]."""

    model_name: str = "Qwen/Qwen3-1.7B"
    max_seq_length: int = 4096
    max_response_length: int = 2048
    num_epochs: int = 10
    batch_size: int = 16
    learning_rate: float = 1e-6
    max_grad_norm: float = 1.0
    gradient_checkpointing: bool = True
    num_samples_per_prompt: int = 8
    temperature: float = 1.0
    kl_coef: float = 0.0001
    clip_ratio: float = 0.2
    use_8bit_ref: bool = True
    checkpoint_dir: str = "checkpoints/grpo"
    save_every_n_epochs: int = 1
    keep_last_n: int = 3
    min_prompts: int = 10
    agent_filter: str = ""


@dataclass(slots=True)
class DSPyOptimizerConfig:
    """DSPy agent optimizer config. Maps to [learning.agent.dspy]."""

    optimizer: str = "BootstrapFewShotWithRandomSearch"
    task_lm: str = ""
    teacher_lm: str = ""
    max_bootstrapped_demos: int = 4
    max_labeled_demos: int = 4
    num_candidate_programs: int = 10
    max_rounds: int = 1
    optimize_system_prompt: bool = True
    optimize_few_shot: bool = True
    optimize_tool_descriptions: bool = True
    min_traces: int = 20
    metric_threshold: float = 0.7
    agent_filter: str = ""
    config_dir: str = ""


@dataclass(slots=True)
class GEPAOptimizerConfig:
    """GEPA agent optimizer config. Maps to [learning.agent.gepa]."""

    reflection_lm: str = ""
    max_metric_calls: int = 150
    population_size: int = 10
    optimize_system_prompt: bool = True
    optimize_tools: bool = True
    optimize_max_turns: bool = True
    optimize_temperature: bool = True
    min_traces: int = 20
    assessment_batch_size: int = 10
    agent_filter: str = ""
    config_dir: str = ""


@dataclass(slots=True)
class ACEOptimizerConfig:
    """ACE agent optimizer config. Maps to ``[learning.agent.ace]``.

    ACE (Agentic Context Engineering) evolves a *playbook* ΓÇö annotated
    natural-language strategies that get prepended to the agent's
    context ΓÇö using a Generator / Reflector / Curator triad. Unlike
    DSPy (few-shot bootstrapping) or GEPA (Pareto-evolutionary prompt
    mutation), ACE writes a textual playbook that the agent reads at
    inference time.

    See https://github.com/ace-agent/ace for the upstream reference.
    Install via ``pip install -e openjarvis[learning-ace]`` once the
    optional dep is available (ACE is not on PyPI as of v1.0.1; the
    extra installs from the upstream git repo).
    """

    # Models for ACE's three roles. Empty string = inherit from the
    # intelligence primitive's default cloud model.
    generator_model: str = ""
    reflector_model: str = ""
    curator_model: str = ""

    # Provider passed to ACE (``sambanova`` | ``together`` | ``openai``
    # | ``commonstack``). We default to ``openai`` since that's what
    # most OpenJarvis users have credentials for.
    api_provider: str = "openai"

    # Run parameters. Defaults mirror ACE's offline-mode quickstart.
    num_epochs: int = 1
    max_num_rounds: int = 3
    eval_steps: int = 100
    playbook_token_budget: int = 80_000
    max_tokens: int = 4_096

    # Where ACE writes intermediate playbooks + final_results.json.
    # Empty string defaults to ``~/.openjarvis/learning/ace/<task>/``.
    save_dir: str = ""
    task_name: str = "openjarvis"

    # Standard filter / threshold knobs shared with DSPy / GEPA.
    min_traces: int = 20
    agent_filter: str = ""
    config_dir: str = ""


@dataclass(slots=True)
class IntelligenceLearningConfig:
    """Intelligence sub-policy config within Learning."""

    policy: str = "none"  # none | sft | grpo
    sft: SFTConfig = field(default_factory=SFTConfig)
    grpo: GRPOConfig = field(default_factory=GRPOConfig)


@dataclass(slots=True)
class AgentLearningConfig:
    """Agent sub-policy config within Learning."""

    policy: str = "none"  # none | dspy | gepa | ace
    dspy: DSPyOptimizerConfig = field(default_factory=DSPyOptimizerConfig)
    gepa: GEPAOptimizerConfig = field(default_factory=GEPAOptimizerConfig)
    ace: ACEOptimizerConfig = field(default_factory=ACEOptimizerConfig)


@dataclass(slots=True)
class SkillsLearningConfig:
    """Configuration for the skills learning loop (Plan 2A)."""

    auto_optimize: bool = False  # opt in via config
    optimizer: str = "dspy"  # "dspy" or "gepa"
    min_traces_per_skill: int = 20
    optimization_interval_seconds: int = 86400
    overlay_dir: str = field(
        default_factory=lambda: str(get_config_dir() / "learning" / "skills")
    )


@dataclass(slots=True)
class MetricsConfig:
    """Reward / optimization metric weights."""

    accuracy_weight: float = 0.6
    latency_weight: float = 0.2
    cost_weight: float = 0.1
    efficiency_weight: float = 0.1


@dataclass(slots=True)
class SpecSearchCompositeRewardConfig:
    """Composite reward weights for Intelligence-edit training (paper Eq. 1).

    R(q, y) = alpha * R_acc - beta * E_hat - gamma * L_hat - delta * C_hat
    """

    alpha: float = 0.5
    beta: float = 0.1
    gamma: float = 0.1
    delta: float = 0.3


@dataclass(slots=True)
class SpecSearchLearningConfig:
    """LLM-guided spec search config (paper ┬º3.3, Algorithm 1).

    Maps to ``[learning.spec_search]`` and is consumed by
    ``SpecSearchOrchestrator.from_config`` and ``SpecSearchLoop``.
    """

    enabled: bool = False
    teacher_model: str = "claude-opus-4-6"
    teacher_engine: str = "cloud"  # registry key for the cloud engine
    autonomy_mode: str = "tiered"  # auto | tiered | manual

    # Per-session bounds (one diagnose/plan/execute pass)
    min_traces: int = 20
    max_cost_per_session_usd: float = 5.0
    max_tool_calls_per_diagnosis: int = 30

    # Multi-session loop (paper Algorithm 1)
    stagnation_k: int = 5
    max_total_cost_usd: float = 50.0
    stagnation_eps: float = 0.001  # gate-score delta below this counts as no progress

    # Gate (GateOK predicate)
    max_regression: float = 0.01  # paper default: epsilon = 1%
    min_improvement: float = 0.0
    benchmark_subsample_size: int = 50
    benchmark_version: str = "personal_v1"

    # Composite reward (only used when an Intelligence edit triggers training)
    composite_reward: SpecSearchCompositeRewardConfig = field(
        default_factory=SpecSearchCompositeRewardConfig,
    )


@dataclass
class LearningConfig:
    """Learning system settings with per-primitive sub-policies."""

    enabled: bool = False
    update_interval: int = 100
    auto_update: bool = False
    routing: RoutingLearningConfig = field(default_factory=RoutingLearningConfig)
    intelligence: IntelligenceLearningConfig = field(
        default_factory=IntelligenceLearningConfig,
    )
    agent: AgentLearningConfig = field(default_factory=AgentLearningConfig)
    skills: SkillsLearningConfig = field(default_factory=SkillsLearningConfig)
    spec_search: SpecSearchLearningConfig = field(
        default_factory=SpecSearchLearningConfig,
    )
    metrics: MetricsConfig = field(default_factory=MetricsConfig)

    # Training pipeline
    training_enabled: bool = False
    training_schedule: str = ""
    min_improvement: float = 0.02

    # Backward-compat properties for old flat field names
    @property
    def default_policy(self) -> str:
        """Deprecated: use ``learning.routing.policy``."""
        return self.routing.policy

    @default_policy.setter
    def default_policy(self, value: str) -> None:
        self.routing.policy = value

    @property
    def intelligence_policy(self) -> str:
        """Deprecated: use ``learning.intelligence.policy``."""
        return self.intelligence.policy

    @intelligence_policy.setter
    def intelligence_policy(self, value: str) -> None:
        self.intelligence.policy = value

    @property
    def agent_policy(self) -> str:
        """Deprecated: use ``learning.agent.policy``."""
        return self.agent.policy

    @agent_policy.setter
    def agent_policy(self, value: str) -> None:
        self.agent.policy = value

    @property
    def reward_weights(self) -> str:
        """Deprecated: use ``learning.metrics.*``."""
        parts = []
        m = self.metrics
        if m.latency_weight:
            parts.append(f"latency={m.latency_weight}")
        if m.cost_weight:
            parts.append(f"cost={m.cost_weight}")
        if m.efficiency_weight:
            parts.append(f"efficiency={m.efficiency_weight}")
        if m.accuracy_weight:
            parts.append(f"accuracy={m.accuracy_weight}")
        return ",".join(parts)

    @reward_weights.setter
    def reward_weights(self, value: str) -> None:
        if not value:
            return
        for part in value.split(","):
            if "=" not in part:
                continue
            key, val = part.strip().split("=", 1)
            key = key.strip()
            fval = float(val.strip())
            if key == "accuracy":
                self.metrics.accuracy_weight = fval
            elif key == "latency":
                self.metrics.latency_weight = fval
            elif key == "cost":
                self.metrics.cost_weight = fval
            elif key == "efficiency":
                self.metrics.efficiency_weight = fval


@dataclass(slots=True)
class StorageConfig:
    """Storage (memory) backend settings.

    Covers both the retrieval/document store (``default_backend``, ``db_path``,
    chunking, context injection) and the automatic long-term memory service
    (``enabled``, ``backend``, ``extraction_model``, ``max_facts``,
    ``facts_path``) configured under ``[memory]`` in ``config.toml``.
    """

    default_backend: str = "sqlite"
    db_path: str = field(default_factory=lambda: str(get_config_dir() / "memory.db"))
    context_top_k: int = 5
    context_min_score: float = 0.0
    context_max_tokens: int = 2048
    chunk_size: int = 512
    chunk_overlap: int = 64

    # Automatic memory service ΓÇö extracts durable facts from conversations in
    # the background and persists them across sessions (see openjarvis.memory).
    enabled: bool = False  # start the memory service with serve/chat
    backend: str = "local"  # fact-store backend ("local" = on-disk JSONL)
    extraction_model: str = ""  # model for fact extraction ("" = active model)
    max_facts: int = 1000  # cap on stored facts (oldest evicted past the cap)
    facts_path: str = field(
        default_factory=lambda: str(get_config_dir() / "memory_facts.jsonl")
    )


# Backward-compatibility alias
MemoryConfig = StorageConfig


@dataclass(slots=True)
class MCPConfig:
    """MCP (Model Context Protocol) settings."""

    enabled: bool = True
    servers: str = ""  # JSON list of MCP server configs


_MAX_EXTERNAL_JSON_BYTES = 4 * 1024 * 1024


def resolve_json_or_file(raw: str, config_dir: Path) -> Any:
    """Resolve a config value that is either inline JSON or a path to a JSON file.

    Parameters
    ----------
    raw:
        Either a JSON string (starts with '[' or '{') or a file path
        to a .json file containing the data.
    config_dir:
        Directory of config.toml, used to resolve relative file paths.

    Returns
    -------
    Parsed JSON value (dict, list, etc.), or ``None`` if *raw* is empty.

    Raises
    ------
    ValueError: If a relative path escapes the config directory.
    FileNotFoundError: If the referenced file does not exist.
    json.JSONDecodeError: If the JSON content is malformed.
    """
    import json

    if not isinstance(raw, str):
        raise TypeError("JSON config value must be a string")

    stripped = raw.strip()
    if not stripped:
        return None

    # Inline JSON
    if stripped.startswith("[") or stripped.startswith("{"):
        return json.loads(stripped)

    # File path reference
    file_path = Path(stripped).expanduser()
    was_relative = not file_path.is_absolute()
    if was_relative:
        file_path = config_dir / file_path

    resolved = file_path.resolve()

    # Security check: relative paths must not escape the config directory
    if was_relative:
        config_resolved = config_dir.expanduser().resolve()
        try:
            resolved.relative_to(config_resolved)
        except ValueError as exc:
            raise ValueError(
                f"Path '{stripped}' resolves to '{resolved}' which is outside "
                f"the config directory '{config_resolved}'"
            ) from exc

    if not resolved.exists():
        raise FileNotFoundError(
            f"MCP config file not found: {resolved} (from '{stripped}')"
        )
    if not resolved.is_file():
        raise ValueError(f"JSON config path is not a regular file: {resolved}")
    if resolved.stat().st_size > _MAX_EXTERNAL_JSON_BYTES:
        raise ValueError(
            f"JSON config file exceeds {_MAX_EXTERNAL_JSON_BYTES} bytes: {resolved}"
        )

    content = resolved.read_text(encoding="utf-8")
    return json.loads(content)


def resolve_mcp_servers(raw: str, config_dir: Path) -> list[dict[str, Any]]:
    """Resolve MCP server configuration from inline JSON or an external file.

    Wraps :func:`resolve_json_or_file` with MCP-specific validation:
    a single server object ``{...}`` is automatically wrapped in a list,
    and the result must be a ``list``.
    """
    import json

    result = resolve_json_or_file(raw, config_dir)
    if result is None:
        return []
    if isinstance(result, dict):
        result = [result]
    if not isinstance(result, list):
        raise ValueError(
            "MCP servers config must be a JSON array or object, "
            f"got {type(result).__name__}"
        )

    servers: list[dict[str, Any]] = []
    for index, server in enumerate(result):
        if isinstance(server, str):
            try:
                server = json.loads(server)
            except json.JSONDecodeError as exc:
                raise ValueError(
                    f"MCP server entry {index} is not a valid JSON object"
                ) from exc
        if not isinstance(server, dict):
            raise ValueError(f"MCP server entry {index} must be a JSON object")
        servers.append(server)
    return servers


@dataclass(slots=True)
class BrowserConfig:
    """Browser automation settings (Playwright)."""

    headless: bool = True
    timeout_ms: int = 30000
    viewport_width: int = 1280
    viewport_height: int = 720


@dataclass(slots=True)
class WeatherToolConfig:
    """Native weather tool settings (credentials stay outside config.toml)."""

    provider: str = "openweathermap"
    default_location: str = ""
    units: str = "metric"
    lang: str = "en"


@dataclass(slots=True)
class ToolsConfig:
    """Tools primitive settings ΓÇö wraps storage and MCP configuration."""

    storage: StorageConfig = field(default_factory=StorageConfig)
    mcp: MCPConfig = field(default_factory=MCPConfig)
    browser: BrowserConfig = field(default_factory=BrowserConfig)
    weather: WeatherToolConfig = field(default_factory=WeatherToolConfig)
    enabled: str = ""  # comma-separated default tools


@dataclass
class AgentConfig:
    """Agent harness settings ΓÇö orchestration, tools, system prompt."""

    default_agent: str = "simple"
    max_turns: int = 10
    tools: str = ""  # comma-separated tool names
    objective: str = ""  # concise purpose for routing/learning/docs
    system_prompt: str = ""  # inline system prompt (takes precedence if set)
    system_prompt_path: str = ""  # path to system prompt file (.txt, .md)
    context_from_memory: bool = True  # inject relevant memory context into prompts
    default_system_prompt: str = (
        "You are OpenJarvis, a helpful AI assistant running locally on the "
        "user's own hardware. You are not a cloud service, and you are not "
        "Claude, ChatGPT, Gemini, or any other branded assistant. If asked "
        "who or what you are, identify yourself as OpenJarvis. Respond "
        "helpfully, concisely, and accurately."
    )

    # Backward-compat property for old field name
    @property
    def default_tools(self) -> str:
        """Deprecated: use ``agent.tools``."""
        return self.tools

    @default_tools.setter
    def default_tools(self, value: str) -> None:
        self.tools = value


@dataclass(slots=True)
class ServerConfig:
    """API server settings."""

    host: str = "127.0.0.1"
    port: int = 8000
    agent: str = "orchestrator"
    model: str = ""
    workers: int = 1
    cors_origins: list = field(
        default_factory=lambda: [
            "http://localhost:3000",
            "http://localhost:5173",
            "http://localhost:5174",
            "http://127.0.0.1:3000",
            "http://127.0.0.1:5173",
            "http://127.0.0.1:5174",
            # Tauri 2 production webview origins.
            # macOS / Linux / iOS use the custom scheme; Windows /
            # Android use http(s)://tauri.localhost. All three must
            # be allowed so the desktop app's chat-completions stream
            # is not blocked by CORS in production builds.
            "tauri://localhost",
            "http://tauri.localhost",
            "https://tauri.localhost",
        ]
    )


@dataclass(slots=True)
class TelemetryConfig:
    """Telemetry persistence settings."""

    enabled: bool = True
    db_path: str = field(default_factory=lambda: str(get_config_dir() / "telemetry.db"))
    gpu_metrics: bool = False
    gpu_poll_interval_ms: int = 50
    energy_vendor: str = ""  # auto-detect or force "nvidia"/"amd"/"apple"/"cpu_rapl"
    # Permit a modelled energy estimate when no hardware counters are
    # readable. Off by default: an estimate written to the telemetry DB is
    # indistinguishable from a measurement at query time except via
    # `energy_method`, and on Apple Silicon the estimate is a function of
    # wall-clock alone, so it cannot tell an idle window from a busy one.
    allow_energy_estimates: bool = False
    warmup_samples: int = 0
    steady_state_window: int = 5
    steady_state_threshold: float = 0.05


@dataclass(slots=True)
class AnalyticsConfig:
    """External anonymous usage analytics (PostHog).

    Separate concern from :class:`TelemetryConfig`, which stores local
    FLOPs/energy/inference metrics in SQLite. This controls anonymized
    usage events sent to the OpenJarvis team's PostHog instance to
    measure setup success, retention, feature usage, and churn.

    No chat content, prompts, model outputs, file paths, emails, IPs,
    or hardware identifiers are ever sent. See ``docs/telemetry.md``.
    """

    enabled: bool = True
    host: str = "https://34.231.106.201.sslip.io"
    key: str = "phc_ysKu72QaxzYNmDpHFcesD2ZZAe68zkdWJEKoYYkc5e3n"
    anon_id_path: str = field(default_factory=lambda: str(get_config_dir() / "anon_id"))
    flush_interval_seconds: int = 30
    flush_at_size: int = 100


@dataclass(slots=True)
class TracesConfig:
    """Trace system settings."""

    enabled: bool = True
    db_path: str = field(default_factory=lambda: str(get_config_dir() / "traces.db"))


@dataclass(slots=True)
class ProactiveConfig:
    """Proactive agent ΓÇö autonomous action scheduling and approval routing."""

    enabled: bool = False
    schedule: str = "0 5 * * *"  # cron expression (default: 5am daily)
    hours_back: int = 24  # how many hours of unacted items to scan
    timezone: str = "America/Los_Angeles"
    # Channel to send approval notifications and receive yes/no replies.
    # Format: "{type}:{id}", e.g. "imessage:+15551234567" or "telegram:123456789"
    notification_channel: str = ""


@dataclass(slots=True)
class TelegramChannelConfig:
    """Per-channel config for Telegram."""

    bot_token: str = ""
    allowed_chat_ids: str = ""
    parse_mode: str = "Markdown"


@dataclass(slots=True)
class DiscordChannelConfig:
    """Per-channel config for Discord."""

    bot_token: str = ""


@dataclass(slots=True)
class SlackChannelConfig:
    """Per-channel config for Slack."""

    bot_token: str = ""
    app_token: str = ""


@dataclass(slots=True)
class WebhookChannelConfig:
    """Per-channel config for generic webhooks."""

    url: str = ""
    secret: str = ""
    method: str = "POST"


@dataclass(slots=True)
class EmailChannelConfig:
    """Per-channel config for email (SMTP/IMAP)."""

    smtp_host: str = ""
    smtp_port: int = 587
    imap_host: str = ""
    imap_port: int = 993
    username: str = ""
    password: str = ""
    use_tls: bool = True


@dataclass(slots=True)
class WhatsAppChannelConfig:
    """Per-channel config for WhatsApp Cloud API."""

    access_token: str = ""
    phone_number_id: str = ""


@dataclass(slots=True)
class SignalChannelConfig:
    """Per-channel config for Signal (via signal-cli REST API)."""

    api_url: str = ""
    phone_number: str = ""


@dataclass(slots=True)
class GoogleChatChannelConfig:
    """Per-channel config for Google Chat webhooks."""

    webhook_url: str = ""


@dataclass(slots=True)
class IRCChannelConfig:
    """Per-channel config for IRC."""

    server: str = ""
    port: int = 6667
    nick: str = ""
    password: str = ""
    use_tls: bool = False


@dataclass(slots=True)
class WebChatChannelConfig:
    """Per-channel config for in-memory webchat."""

    pass


@dataclass(slots=True)
class TeamsChannelConfig:
    """Per-channel config for Microsoft Teams (Bot Framework)."""

    app_id: str = ""
    app_password: str = ""
    service_url: str = ""


@dataclass(slots=True)
class MatrixChannelConfig:
    """Per-channel config for Matrix."""

    homeserver: str = ""
    access_token: str = ""


@dataclass(slots=True)
class MattermostChannelConfig:
    """Per-channel config for Mattermost."""

    url: str = ""
    token: str = ""


@dataclass(slots=True)
class FeishuChannelConfig:
    """Per-channel config for Feishu (Lark)."""

    app_id: str = ""
    app_secret: str = ""


@dataclass(slots=True)
class BlueBubblesChannelConfig:
    """Per-channel config for BlueBubbles (iMessage bridge)."""

    url: str = ""
    password: str = ""


@dataclass(slots=True)
class WhatsAppBaileysChannelConfig:
    """Per-channel config for WhatsApp via Baileys protocol."""

    auth_dir: str = ""  # Defaults to ~/.openjarvis/whatsapp_auth
    assistant_name: str = "Jarvis"
    assistant_has_own_number: bool = False


@dataclass
class ChannelConfig:
    """Channel messaging settings."""

    enabled: bool = False
    default_channel: str = ""
    default_agent: str = "simple"
    telegram: TelegramChannelConfig = field(default_factory=TelegramChannelConfig)
    discord: DiscordChannelConfig = field(default_factory=DiscordChannelConfig)
    slack: SlackChannelConfig = field(default_factory=SlackChannelConfig)
    webhook: WebhookChannelConfig = field(default_factory=WebhookChannelConfig)
    email: EmailChannelConfig = field(default_factory=EmailChannelConfig)
    whatsapp: WhatsAppChannelConfig = field(default_factory=WhatsAppChannelConfig)
    signal: SignalChannelConfig = field(default_factory=SignalChannelConfig)
    google_chat: GoogleChatChannelConfig = field(
        default_factory=GoogleChatChannelConfig,
    )
    irc: IRCChannelConfig = field(default_factory=IRCChannelConfig)
    webchat: WebChatChannelConfig = field(default_factory=WebChatChannelConfig)
    teams: TeamsChannelConfig = field(default_factory=TeamsChannelConfig)
    matrix: MatrixChannelConfig = field(default_factory=MatrixChannelConfig)
    mattermost: MattermostChannelConfig = field(default_factory=MattermostChannelConfig)
    feishu: FeishuChannelConfig = field(default_factory=FeishuChannelConfig)
    bluebubbles: BlueBubblesChannelConfig = field(
        default_factory=BlueBubblesChannelConfig,
    )
    whatsapp_baileys: WhatsAppBaileysChannelConfig = field(
        default_factory=WhatsAppBaileysChannelConfig,
    )


@dataclass(slots=True)
class CapabilitiesConfig:
    """RBAC capability system settings."""

    enabled: bool = False
    policy_path: str = ""
    default_deny: bool = False


@dataclass(slots=True)
class SecurityConfig:
    """Security guardrails settings."""

    enabled: bool = True
    scan_input: bool = True
    scan_output: bool = True
    mode: str = "redact"  # "redact" | "warn" | "block"
    secret_scanner: bool = True
    pii_scanner: bool = True
    audit_log_path: str = field(
        default_factory=lambda: str(get_config_dir() / "audit.db")
    )
    enforce_tool_confirmation: bool = True
    merkle_audit: bool = True
    signing_key_path: str = ""
    ssrf_protection: bool = True
    rate_limit_enabled: bool = True
    rate_limit_rpm: int = 60
    rate_limit_burst: int = 10
    local_engine_bypass: bool = False
    local_tool_bypass: bool = False
    profile: str = ""
    vault_key_path: str = field(
        default_factory=lambda: str(get_config_dir() / ".vault_key")
    )
    capabilities: CapabilitiesConfig = field(default_factory=CapabilitiesConfig)


# ---------------------------------------------------------------------------
# Security profile presets
# ---------------------------------------------------------------------------

_SECURITY_PROFILES: Dict[str, Dict[str, Dict[str, Any]]] = {
    "personal": {
        "security": {
            "mode": "redact",
            "rate_limit_enabled": True,
            "local_engine_bypass": False,
            "local_tool_bypass": False,
        },
        "server": {
            "host": "127.0.0.1",
        },
    },
    "shared": {
        "security": {
            "mode": "redact",
            "rate_limit_enabled": True,
            "local_engine_bypass": False,
            "local_tool_bypass": False,
            "capabilities": {"enabled": True, "default_deny": True},
        },
        "server": {
            "host": "127.0.0.1",
        },
    },
    "server": {
        "security": {
            "mode": "block",
            "rate_limit_enabled": True,
            "rate_limit_rpm": 30,
            "rate_limit_burst": 5,
            "local_engine_bypass": False,
            "local_tool_bypass": False,
            "capabilities": {"enabled": True, "default_deny": True},
        },
        "server": {
            "host": "0.0.0.0",
        },
    },
}


def apply_security_profile(
    security_cfg: "SecurityConfig",
    server_cfg: "ServerConfig | None",
    *,
    overrides: "set[str] | None" = None,
) -> None:
    """Expand a named security profile into config fields.

    Fields in *overrides* (explicitly set by the user in TOML) are
    not overwritten by the profile.
    """
    profile = security_cfg.profile
    if not profile:
        return

    if profile not in _SECURITY_PROFILES:
        raise ValueError(
            f"Unknown security profile '{profile}'. "
            f"Valid profiles: {', '.join(_SECURITY_PROFILES)}"
        )

    _overrides = overrides or set()
    pdef = _SECURITY_PROFILES[profile]

    for key, value in pdef.get("security", {}).items():
        if key == "capabilities" and isinstance(value, dict):
            # Preserve explicitly selected fields while inheriting the
            # profile's remaining defaults. A policy_path alone must not
            # silently disable the profile's capability gate.
            if "capabilities" in _overrides:
                continue
            for cap_key, cap_value in value.items():
                if f"capabilities.{cap_key}" not in _overrides and hasattr(
                    security_cfg.capabilities, cap_key
                ):
                    setattr(security_cfg.capabilities, cap_key, cap_value)
            continue
        if key not in _overrides and hasattr(security_cfg, key):
            setattr(security_cfg, key, value)

    if server_cfg is not None:
        for key, value in pdef.get("server", {}).items():
            if key not in _overrides and hasattr(server_cfg, key):
                setattr(server_cfg, key, value)


@dataclass(slots=True)
class SandboxConfig:
    """Container sandbox settings."""

    enabled: bool = False
    image: str = "openjarvis-sandbox:latest"
    timeout: int = 300
    workspace: str = ""
    mount_allowlist_path: str = ""
    max_concurrent: int = 5
    runtime: str = "docker"
    wasm_fuel_limit: int = 1_000_000
    wasm_memory_limit_mb: int = 256


@dataclass(slots=True)
class SchedulerConfig:
    """Task scheduler settings."""

    enabled: bool = False
    poll_interval: int = 60
    db_path: str = ""  # Defaults to ~/.openjarvis/scheduler.db


@dataclass(slots=True)
class WorkflowConfig:
    """Workflow engine settings."""

    enabled: bool = False
    max_parallel: int = 4
    default_node_timeout: int = 300


@dataclass(slots=True)
class SessionConfig:
    """Cross-channel session settings."""

    enabled: bool = False
    max_age_hours: float = 24.0
    consolidation_threshold: int = 100
    db_path: str = field(default_factory=lambda: str(get_config_dir() / "sessions.db"))


@dataclass(slots=True)
class A2AConfig:
    """Agent-to-Agent protocol settings."""

    enabled: bool = False
    # Bearer token required for inbound A2A requests. Empty = unauthenticated
    # (only safe on a trusted network). See ``A2AServer(auth_token=...)``.
    auth_token: str = ""


@dataclass(slots=True)
class OperatorsConfig:
    """Operator lifecycle settings."""

    enabled: bool = False
    manifests_dir: str = field(
        default_factory=lambda: str(get_config_dir() / "operators")
    )
    auto_activate: str = ""  # Comma-separated operator IDs


@dataclass(slots=True)
class SpeechConfig:
    """Speech-to-text settings."""

    backend: str = "auto"  # "auto", "faster-whisper", "openai", "deepgram"
    model: str = "base"  # Whisper model size: tiny, base, small, medium, large-v3
    language: str = ""  # Empty = auto-detect
    device: str = "auto"  # "auto", "cpu", "cuda"
    compute_type: str = "float16"  # "float16", "int8", "float32"
    # Text-to-speech. ``voice_id`` is interpreted by ``tts_backend`` only --
    # voice IDs are not portable between backends, so if voice output falls
    # back to a different backend that backend's own default voice is used.
    # Kokoro IDs: bm_george / bm_lewis (British male), bf_emma / bf_isabella
    # (British female), af_* / am_* (American).
    tts_backend: str = "kokoro"  # "kokoro", "openai_tts", "cartesia"
    voice_id: str = "bm_george"
    voice_speed: float = 1.0


@dataclass(slots=True)
class OptimizeConfig:
    """Configuration optimization settings."""

    max_trials: int = 20
    early_stop_patience: int = 5
    optimizer_model: str = "claude-sonnet-4-6"
    optimizer_provider: str = "anthropic"
    benchmark: str = ""
    max_samples: int = 50
    judge_model: str = "gpt-5-mini-2025-08-07"
    db_path: str = field(default_factory=lambda: str(get_config_dir() / "optimize.db"))


@dataclass(slots=True)
class AgentManagerConfig:
    """Persistent agent manager settings."""

    enabled: bool = True
    db_path: str = field(default_factory=lambda: str(get_config_dir() / "agents.db"))


@dataclass(slots=True)
class MemoryFilesConfig:
    """Persistent memory-file paths and nudge settings."""

    soul_path: str = field(default_factory=lambda: str(get_config_dir() / "SOUL.md"))
    memory_path: str = field(
        default_factory=lambda: str(get_config_dir() / "MEMORY.md")
    )
    user_path: str = field(default_factory=lambda: str(get_config_dir() / "USER.md"))
    nudge_interval: int = 10
    persona_name: str = ""  # named persona dir under <config-dir>/personas/<name>/


@dataclass(slots=True)
class SystemPromptConfig:
    """Limits and strategy for system-prompt assembly."""

    prefix: str = ""
    soul_max_chars: int = 4000
    memory_max_chars: int = 2500
    user_max_chars: int = 1500
    skill_desc_max_chars: int = 60
    truncation_strategy: str = "head_tail"


@dataclass(slots=True)
class CompressionConfig:
    """Configuration for context compression."""

    enabled: bool = True
    threshold: float = 0.50
    strategy: str = "session_consolidation"


@dataclass(slots=True)
class SkillSourceConfig:
    """Configuration for a single skill source (Hermes, OpenClaw, GitHub)."""

    source: str = ""  # "hermes", "openclaw", or "github"
    url: str = ""  # required when source = "github"
    filter: Dict[str, Any] = field(default_factory=dict)
    auto_update: bool = False


@dataclass(slots=True)
class SkillsConfig:
    """Configuration for agent-authored procedural skills."""

    enabled: bool = True
    skills_dir: str = field(default_factory=lambda: str(get_config_dir() / "skills"))
    active: str = "*"
    auto_discover: bool = True
    auto_sync: bool = False
    nudge_interval: int = 15
    index_repo: str = "https://github.com/openjarvis/skill-index.git"
    index_dir: str = field(
        default_factory=lambda: str(get_config_dir() / "skill-index")
    )
    max_depth: int = 5
    sandbox_dangerous: bool = True
    sources: List[SkillSourceConfig] = field(default_factory=list)


@dataclass
class DigestSectionConfig:
    """Configuration for a single digest section."""

    sources: List[str] = field(default_factory=list)
    max_items: int = 10
    priority_contacts: List[str] = field(default_factory=list)


@dataclass
class DigestConfig:
    """Configuration for the morning digest feature."""

    enabled: bool = False
    schedule: str = "0 6 * * *"
    timezone: str = "America/Los_Angeles"
    persona: str = "jarvis"
    sections: List[str] = field(
        default_factory=lambda: ["messages", "calendar", "health", "world"]
    )
    optional_sections: List[str] = field(
        default_factory=lambda: ["github", "financial", "music", "fitness"]
    )
    honorific: str = "sir"
    voice_id: str = ""
    voice_speed: float = 1.0
    tts_backend: str = "cartesia"
    messages: DigestSectionConfig = field(
        default_factory=lambda: DigestSectionConfig(
            sources=["gmail", "slack", "google_tasks"]
        )
    )
    calendar: DigestSectionConfig = field(
        default_factory=lambda: DigestSectionConfig(sources=["gcalendar"])
    )
    health: DigestSectionConfig = field(
        default_factory=lambda: DigestSectionConfig(sources=["oura", "apple_health"])
    )
    world: DigestSectionConfig = field(
        default_factory=lambda: DigestSectionConfig(sources=[])
    )


@dataclass
class JarvisConfig:
    """Top-level configuration for OpenJarvis."""

    installed_at: str = ""
    installer_version: str = ""
    hardware: HardwareInfo = field(default_factory=HardwareInfo)
    engine: EngineConfig = field(default_factory=EngineConfig)
    intelligence: IntelligenceConfig = field(default_factory=IntelligenceConfig)
    deep_research: DeepResearchConfig = field(default_factory=DeepResearchConfig)
    learning: LearningConfig = field(default_factory=LearningConfig)
    tools: ToolsConfig = field(default_factory=ToolsConfig)
    agent: AgentConfig = field(default_factory=AgentConfig)
    server: ServerConfig = field(default_factory=ServerConfig)
    telemetry: TelemetryConfig = field(default_factory=TelemetryConfig)
    analytics: AnalyticsConfig = field(default_factory=AnalyticsConfig)
    traces: TracesConfig = field(default_factory=TracesConfig)
    channel: ChannelConfig = field(default_factory=ChannelConfig)
    security: SecurityConfig = field(default_factory=SecurityConfig)
    sandbox: SandboxConfig = field(default_factory=SandboxConfig)
    scheduler: SchedulerConfig = field(default_factory=SchedulerConfig)
    workflow: WorkflowConfig = field(default_factory=WorkflowConfig)
    sessions: SessionConfig = field(default_factory=SessionConfig)
    a2a: A2AConfig = field(default_factory=A2AConfig)
    operators: OperatorsConfig = field(default_factory=OperatorsConfig)
    speech: SpeechConfig = field(default_factory=SpeechConfig)
    optimize: OptimizeConfig = field(default_factory=OptimizeConfig)
    agent_manager: AgentManagerConfig = field(default_factory=AgentManagerConfig)
    memory_files: MemoryFilesConfig = field(default_factory=MemoryFilesConfig)
    system_prompt: SystemPromptConfig = field(default_factory=SystemPromptConfig)
    compression: CompressionConfig = field(default_factory=CompressionConfig)
    skills: SkillsConfig = field(default_factory=SkillsConfig)
    digest: DigestConfig = field(default_factory=DigestConfig)
    proactive: ProactiveConfig = field(default_factory=ProactiveConfig)
    mining: Optional["MiningConfig"] = None

    @property
    def _config_dir(self) -> Path:
        """Directory containing the loaded config, or the env-aware default."""
        return self.__dict__.get("_config_source_dir", get_config_dir())

    @_config_dir.setter
    def _config_dir(self, value: Path) -> None:
        self.__dict__["_config_source_dir"] = Path(value)

    @property
    def memory(self) -> StorageConfig:
        """Backward-compatible accessor ΓÇö canonical location is tools.storage."""
        return self.tools.storage

    @memory.setter
    def memory(self, value: StorageConfig) -> None:
        """Backward-compatible setter."""
        self.tools.storage = value


# ---------------------------------------------------------------------------
# Config key validation
# ---------------------------------------------------------------------------

# Sections that users may set via ``jarvis config set``.
# ``hardware`` is auto-detected and not user-settable.
_SETTABLE_SECTIONS = frozenset(JarvisConfig.__dataclass_fields__.keys()) - {
    "hardware",
    "mining",
}


def validate_config_key(dotted_key: str) -> type:
    """Validate a dotted config key and return the leaf field's Python type.

    Raises :class:`ValueError` when the key does not map to a known field.
    The function walks the ``JarvisConfig`` dataclass hierarchy using
    ``dataclasses.fields()``.

    Examples::

        validate_config_key("engine.ollama.host")      # -> str
        validate_config_key("intelligence.temperature") # -> float
    """
    from dataclasses import fields as dc_fields

    def contains_dataclass(annotation: Any) -> bool:
        if is_dataclass(annotation):
            return True
        return any(contains_dataclass(arg) for arg in get_args(annotation))

    parts = dotted_key.split(".")
    if len(parts) < 2:
        raise ValueError(
            f"Config key must have at least two segments (e.g. engine.default), "
            f"got: {dotted_key!r}"
        )

    if parts[0] not in _SETTABLE_SECTIONS:
        raise ValueError(
            f"Unknown config key: {dotted_key!r} "
            f"(valid top-level sections: {sorted(_SETTABLE_SECTIONS)})"
        )

    # Walk the dataclass tree
    current_cls = JarvisConfig
    for i, part in enumerate(parts):
        field_map = {f.name: f for f in dc_fields(current_cls)}
        if part not in field_map:
            path_so_far = ".".join(parts[: i + 1])
            raise ValueError(
                f"Unknown config key: {dotted_key!r} "
                f"(no field {part!r} at {path_so_far}; "
                f"valid fields: {sorted(field_map.keys())})"
            )
        fld = field_map[part]
        # Resolve the type ΓÇö unwrap Optional, etc.
        fld_type = fld.type
        if isinstance(fld_type, str):
            # Evaluate forward references in the config module namespace
            import openjarvis.core.config as _cfg_mod

            fld_type = eval(fld_type, vars(_cfg_mod))  # noqa: S307

        if i == len(parts) - 1:
            if contains_dataclass(fld_type):
                suggestions = ""
                if is_dataclass(fld_type):
                    child_keys = [
                        f"{dotted_key}.{child.name}" for child in dc_fields(fld_type)
                    ]
                    suggestions = f"; set one of: {', '.join(child_keys)}"
                raise ValueError(
                    f"Config key {dotted_key!r} names a section, not a settable value"
                    f"{suggestions}"
                )
            # Leaf ΓÇö return the primitive/container type
            return fld_type
        else:
            # Must be a nested dataclass
            if not hasattr(fld_type, "__dataclass_fields__"):
                path_so_far = ".".join(parts[: i + 1])
                raise ValueError(
                    f"Unknown config key: {dotted_key!r} "
                    f"({path_so_far} is a leaf of type {fld_type.__name__}, "
                    f"not a section)"
                )
            current_cls = fld_type

    # Should not reach here, but satisfy type checker
    raise ValueError(f"Unknown config key: {dotted_key!r}")


# ---------------------------------------------------------------------------
# TOML loading
# ---------------------------------------------------------------------------


def _apply_toml_section(target: Any, section: Dict[str, Any]) -> None:
    """Overlay TOML key/value pairs onto a dataclass instance.

    Recursively handles nested dicts when the target attribute is itself
    a dataclass, including dict entries in lists of dataclasses.  Normalises
    TOML arrays to comma-separated strings ΓÇö both for dataclass fields annotated
    as ``str`` and for backward-compat property setters that expect string input.
    """
    try:
        type_hints = get_type_hints(type(target))
    except (NameError, TypeError):
        # Some config types contain optional runtime-only forward references.
        type_hints = {}

    for key, value in section.items():
        if hasattr(target, key):
            if isinstance(value, dict):
                nested = getattr(target, key)
                if hasattr(nested, "__dataclass_fields__"):
                    _apply_toml_section(nested, value)
                else:
                    setattr(target, key, value)
            else:
                # Normalise TOML arrays ΓåÆ comma-separated string.
                # Covers both real dataclass fields and backward-compat
                # property setters (e.g. reward_weights, default_tools).
                if isinstance(value, list):
                    is_str_field = False
                    item_dataclass = None
                    if hasattr(target, "__dataclass_fields__"):
                        field_obj = target.__dataclass_fields__.get(key)
                        if field_obj is not None:
                            field_type = type_hints.get(key, field_obj.type)
                            type_args = get_args(field_type)
                            if (
                                get_origin(field_type) is list
                                and len(type_args) == 1
                                and is_dataclass(type_args[0])
                            ):
                                item_dataclass = type_args[0]
                            elif field_obj.type in ("str", str):
                                is_str_field = True
                        else:
                            # Property, not a real field ΓÇö normalise to string
                            is_str_field = True

                    if item_dataclass is not None:
                        converted = []
                        for item in value:
                            if isinstance(item, dict):
                                nested = item_dataclass()
                                _apply_toml_section(nested, item)
                                converted.append(nested)
                            else:
                                converted.append(item)
                        value = converted
                    elif is_str_field:
                        value = ",".join(str(v) for v in value)
                setattr(target, key, value)


def _migrate_toml_data(data: Dict[str, Any], cfg: "JarvisConfig") -> None:
    """Migrate old-format TOML keys to new structure in-place.

    Handles cross-section moves that can't be solved by backward-compat
    properties alone (e.g. ``agent.temperature`` ΓåÆ ``intelligence.temperature``).
    """
    # agent.temperature / agent.max_tokens ΓåÆ intelligence.*
    if "agent" in data:
        agent_data = data["agent"]
        intel_data = data.setdefault("intelligence", {})
        for moved_key in ("temperature", "max_tokens"):
            if moved_key in agent_data:
                intel_data.setdefault(moved_key, agent_data.pop(moved_key))

    # context_injection from memory / tools.storage ΓåÆ agent.context_from_memory
    for src_section in ("memory",):
        src = data.get(src_section, {})
        if isinstance(src, dict) and "context_injection" in src:
            data.setdefault("agent", {}).setdefault(
                "context_from_memory",
                src.pop("context_injection"),
            )

    if "tools" in data:
        tools_data = data["tools"]
        if isinstance(tools_data, dict):
            storage_sub = tools_data.get("storage", {})
            if isinstance(storage_sub, dict) and "context_injection" in storage_sub:
                data.setdefault("agent", {}).setdefault(
                    "context_from_memory",
                    storage_sub.pop("context_injection"),
                )


def _parse_mining_section(data: dict) -> Optional["MiningConfig"]:
    """Parse the ``[mining]`` TOML section into a ``MiningConfig``.

    Returns None if the section is absent. Resolves the ``submit_target``
    string into a ``SoloTarget`` or ``PoolTarget`` tagged union.
    """
    if "mining" not in data:
        return None

    # Lazy runtime import to break the import cycle: ``mining/_stubs.py``
    # imports ``HardwareInfo`` from this module at its top level. By the
    # time ``_parse_mining_section`` is called, ``core.config`` is already
    # fully initialized in ``sys.modules``, so the cycle is harmless.
    from openjarvis.mining._stubs import MiningConfig, PoolTarget, SoloTarget

    section = data["mining"]
    extra = section.get("extra", {}) or {}

    target_str = section.get("submit_target", "solo")
    submit_target: Any
    if target_str == "solo":
        submit_target = SoloTarget(
            pearld_rpc_url=extra.get("pearld_rpc_url", "http://localhost:44107")
        )
    elif isinstance(target_str, str) and target_str.startswith("pool:"):
        submit_target = PoolTarget(url=target_str[len("pool:") :])
    else:
        raise ValueError(
            f"[mining].submit_target must be 'solo' or 'pool:<url>', got {target_str!r}"
        )

    return MiningConfig(
        provider=section["provider"],
        wallet_address=section["wallet_address"],
        submit_target=submit_target,
        fee_bps=int(section.get("fee_bps", 0)),
        fee_payout_address=section.get("fee_payout_address") or None,
        extra={k: v for k, v in extra.items()},
    )


@functools.lru_cache(maxsize=1)
def load_config(path: Optional[Path] = None) -> JarvisConfig:
    """Detect hardware, build defaults, overlay TOML overrides.

    Parameters
    ----------
    path:
        Explicit config file. If not set, uses ``OPENJARVIS_CONFIG`` when set,
        otherwise ``~/.openjarvis/config.toml``.
    """
    _ensure_config_dir()
    hw = detect_hardware()
    cfg = JarvisConfig(hardware=hw)
    cfg.engine.default = recommend_engine(hw)

    if path is not None:
        config_path = Path(path).expanduser().resolve()
    elif os.environ.get("OPENJARVIS_CONFIG"):
        config_path = Path(os.environ["OPENJARVIS_CONFIG"]).expanduser().resolve()
    else:
        config_path = get_config_path()
    cfg._config_dir = config_path.parent
    if config_path.exists():
        with open(config_path, "rb") as fh:
            data = tomllib.load(fh)

        # Run backward-compat migrations before applying
        _migrate_toml_data(data, cfg)

        # All top-level sections ΓÇö recursive _apply_toml_section handles
        # nested sub-configs (engine.ollama, learning.routing, channel.*, etc.)
        top_sections = (
            "engine",
            "intelligence",
            "deep_research",
            "learning",
            "agent",
            "server",
            "telemetry",
            "analytics",
            "traces",
            "security",
            "channel",
            "tools",
            "sandbox",
            "scheduler",
            "workflow",
            "sessions",
            "a2a",
            "operators",
            "speech",
            "optimize",
            "agent_manager",
            "digest",
            "proactive",
            "memory_files",
            "system_prompt",
            "compression",
            "skills",
        )
        for section_name in top_sections:
            if section_name in data:
                _apply_toml_section(
                    getattr(cfg, section_name),
                    data[section_name],
                )

        # Memory: accept [memory] (old) ΓåÆ maps to tools.storage
        if "memory" in data:
            _apply_toml_section(cfg.tools.storage, data["memory"])

        # Top-level install provenance (installed_at, installer_version)
        for key in ("installed_at", "installer_version"):
            if key in data:
                setattr(cfg, key, data[key])

        # Expand security profile (user TOML overrides take precedence)
        _security_data = data.get("security", {})
        _user_security_keys = set(_security_data)
        if isinstance(_security_data.get("capabilities"), dict):
            _user_security_keys.discard("capabilities")
            _user_security_keys.update(
                f"capabilities.{key}" for key in _security_data["capabilities"]
            )
        apply_security_profile(cfg.security, cfg.server, overrides=_user_security_keys)

        # Mining: dedicated parser for tagged-union submit_target
        cfg.mining = _parse_mining_section(data)

    # Apply profile even without a config file (in case defaults set one)
    if not config_path.exists() and cfg.security.profile:
        apply_security_profile(cfg.security, cfg.server)

    return cfg


# ---------------------------------------------------------------------------
# Default TOML generation (for ``jarvis init``)
# ---------------------------------------------------------------------------


def generate_minimal_toml(
    hw: HardwareInfo, engine: str | None = None, *, host: str | None = None
) -> str:
    """Render a minimal TOML config with only essential settings."""
    engine = engine or recommend_engine(hw)
    model = recommend_model(hw, engine)
    gpu_comment = ""
    if hw.gpu:
        mem_label = "unified memory" if hw.gpu.vendor == "apple" else "VRAM"
        gpu_comment = f"\n# GPU: {hw.gpu.name} ({hw.gpu.vram_gb} GB {mem_label})"
    if host:
        engine_host_section = f'\n[engine.{engine}]\nhost = "{host}"\n'
    else:
        engine_host_section = (
            f"\n[engine.{engine}]\n"
            f'# host = "http://localhost:11434"  '
            f"# set to remote URL if engine runs elsewhere\n"
        )
    return f"""\
# OpenJarvis configuration
# Hardware: {hw.cpu_brand} ({hw.cpu_count} cores, {hw.ram_gb} GB RAM){gpu_comment}
# Full reference config: jarvis init --full

[engine]
default = "{engine}"
{engine_host_section}
[intelligence]
default_model = "{model}"

[agent]
default_agent = "simple"

[tools]
enabled = ["code_interpreter", "web_search", "file_read", "shell_exec"]
"""


def generate_default_toml(
    hw: HardwareInfo, engine: str | None = None, *, host: str | None = None
) -> str:
    """Render a commented TOML string suitable for ``~/.openjarvis/config.toml``."""
    engine = engine or recommend_engine(hw)
    model = recommend_model(hw, engine)
    gpu_line = ""
    if hw.gpu:
        gpu_line = f"# Detected GPU: {hw.gpu.name} ({hw.gpu.vram_gb} GB VRAM)"

    model_comment = ""
    if model:
        model_comment = "  # recommended for your hardware"

    result = f"""\
# OpenJarvis configuration
# Generated by `jarvis init`
#
# Hardware: {hw.cpu_brand} ({hw.cpu_count} cores, {hw.ram_gb} GB RAM)
{gpu_line}

[engine]
default = "{engine}"

[engine.ollama]
host = "http://localhost:11434"

[engine.vllm]
host = "http://localhost:8000"

[engine.sglang]
host = "http://localhost:30000"

# [engine.llamacpp]
# host = "http://localhost:8080"
# binary_path = ""

[engine.mlx]
host = "http://localhost:8080"

# [engine.lmstudio]
# host = "http://localhost:1234"

# [engine.exo]
# host = "http://localhost:52415"

# [engine.nexa]
# host = "http://localhost:18181"
# device = ""  # cpu, gpu, npu

# [engine.uzu]
# host = "http://localhost:8080"

# [engine.apple_fm]
# host = "http://localhost:8079"

[intelligence]
default_model = "{model}"{model_comment}
fallback_model = ""
# model_path = ""              # Local weights (HF repo, GGUF file, etc.)
# checkpoint_path = ""         # Checkpoint/adapter path
# quantization = "none"        # none, fp8, int8, int4, gguf_q4, gguf_q8
# preferred_engine = ""        # Override engine for this model (e.g., "vllm")
# provider = ""                # local, openai, anthropic, google
temperature = 0.7
max_tokens = 1024
# top_p = 0.9
# top_k = 40
# repetition_penalty = 1.0
# stop_sequences = ""

# [deep_research]
# engine = ""                  # empty = use [engine].default
# model = ""                   # empty = use [intelligence].default_model

[agent]
default_agent = "simple"
max_turns = 10
# tools = ""                   # Comma-separated tool names
# objective = ""               # Concise purpose string
# system_prompt = ""           # Inline system prompt
# system_prompt_path = ""      # Path to system prompt file
context_from_memory = true

[tools.storage]
default_backend = "sqlite"

# Automatic long-term memory: extracts durable facts from conversations in the
# background and persists them. Starts/stops with `jarvis serve` and
# `jarvis chat`; manage stored facts with `jarvis memory list` / `clear`.
[memory]
enabled = false               # set true to enable the memory service
backend = "local"             # fact-store backend (local = on-disk JSONL)
extraction_model = ""         # model for fact extraction ("" = active model)
max_facts = 1000              # cap on stored facts

[tools.mcp]
enabled = true

# [tools.browser]
# headless = true
# timeout_ms = 30000
# viewport_width = 1280
# viewport_height = 720

# Weather API credentials belong in credentials.toml or the environment, not here.
# [tools.weather]
# provider = "openweathermap"
# default_location = ""
# units = "metric"             # metric or imperial
# lang = "en"                  # OpenWeatherMap language code

[server]
# Loopback is safe for local use and works without API authentication.
host = "127.0.0.1"
# To serve other machines, configure an API key before using:
# host = "0.0.0.0"
port = 8000
agent = "orchestrator"

[learning]
enabled = false
update_interval = 100
# auto_update = false

[learning.routing]
policy = "heuristic"
# min_samples = 5

# [learning.intelligence]
# policy = "none"              # "sft" to learn from traces

# [learning.agent]
# policy = "none"              # "agent_advisor" | "icl_updater"

# [learning.metrics]
# accuracy_weight = 0.6
# latency_weight = 0.2
# cost_weight = 0.1
# efficiency_weight = 0.1

[telemetry]
enabled = true
# gpu_metrics = false
# gpu_poll_interval_ms = 50

[traces]
enabled = false

[channel]
enabled = false
default_agent = "simple"

# [channel.telegram]
# bot_token = ""  # Or set TELEGRAM_BOT_TOKEN env var

# [channel.discord]
# bot_token = ""  # Or set DISCORD_BOT_TOKEN env var

# [channel.slack]
# bot_token = ""  # Or set SLACK_BOT_TOKEN env var

# [channel.webhook]
# url = ""

# [channel.whatsapp]
# access_token = ""      # Or set WHATSAPP_ACCESS_TOKEN env var
# phone_number_id = ""   # Or set WHATSAPP_PHONE_NUMBER_ID env var

# [channel.signal]
# api_url = ""            # signal-cli REST API URL
# phone_number = ""       # Or set SIGNAL_PHONE_NUMBER env var

# [channel.google_chat]
# webhook_url = ""        # Or set GOOGLE_CHAT_WEBHOOK_URL env var

# [channel.irc]
# server = ""
# port = 6667
# nick = ""
# use_tls = false

# [channel.teams]
# app_id = ""             # Or set TEAMS_APP_ID env var
# app_password = ""       # Or set TEAMS_APP_PASSWORD env var

# [channel.matrix]
# homeserver = ""         # Or set MATRIX_HOMESERVER env var
# access_token = ""       # Or set MATRIX_ACCESS_TOKEN env var

# [channel.mattermost]
# url = ""                # Or set MATTERMOST_URL env var
# token = ""              # Or set MATTERMOST_TOKEN env var

# [channel.feishu]
# app_id = ""             # Or set FEISHU_APP_ID env var
# app_secret = ""         # Or set FEISHU_APP_SECRET env var

# [channel.bluebubbles]
# url = ""                # Or set BLUEBUBBLES_URL env var
# password = ""           # Or set BLUEBUBBLES_PASSWORD env var

[security]
enabled = true
mode = "warn"
scan_input = true
scan_output = true
secret_scanner = true
pii_scanner = true
enforce_tool_confirmation = true
ssrf_protection = true
# rate_limit_enabled = false
# rate_limit_rpm = 60
# rate_limit_burst = 10

# [sandbox]
# enabled = false
# image = "openjarvis-sandbox:latest"
# timeout = 300
# max_concurrent = 5
# runtime = "docker"

# [scheduler]
# enabled = false
# poll_interval = 60
# db_path = ""                # Defaults to ~/.openjarvis/scheduler.db

# [channel.whatsapp_baileys]
# auth_dir = ""               # Defaults to ~/.openjarvis/whatsapp_auth
# assistant_name = "Jarvis"
# assistant_has_own_number = false
"""
    if host:
        import re as _re

        pattern = _re.escape(f"[engine.{engine}]") + r"\nhost = \"[^\"]*\""
        replacement = f'[engine.{engine}]\\nhost = "{host}"'
        result = _re.sub(pattern, replacement, result)
    return result


__all__ = [
    "A2AConfig",
    "AgentConfig",
    "AgentManagerConfig",
    "OperatorsConfig",
    "AgentLearningConfig",
    "BlueBubblesChannelConfig",
    "BrowserConfig",
    "CapabilitiesConfig",
    "ChannelConfig",
    "ConfigurationError",
    "DEFAULT_CONFIG_DIR",
    "DEFAULT_CONFIG_PATH",
    "DiscordChannelConfig",
    "DeepResearchConfig",
    "get_cache_dir",
    "get_config_dir",
    "get_config_path",
    "get_data_dir",
    "EmailChannelConfig",
    "EngineConfig",
    "FeishuChannelConfig",
    "GoogleChatChannelConfig",
    "GpuInfo",
    "HardwareInfo",
    "IRCChannelConfig",
    "IntelligenceConfig",
    "IntelligenceLearningConfig",
    "JarvisConfig",
    "LearningConfig",
    "LMStudioEngineConfig",
    "LlamaCppEngineConfig",
    "MCPConfig",
    "MLXEngineConfig",
    "MatrixChannelConfig",
    "MattermostChannelConfig",
    "MemoryConfig",
    "MetricsConfig",
    "OllamaEngineConfig",
    "OptimizeConfig",
    "RoutingLearningConfig",
    "SGLangEngineConfig",
    "SandboxConfig",
    "SchedulerConfig",
    "SecurityConfig",
    "ServerConfig",
    "SessionConfig",
    "SignalChannelConfig",
    "SlackChannelConfig",
    "SpeechConfig",
    "StorageConfig",
    "TeamsChannelConfig",
    "TelegramChannelConfig",
    "TelemetryConfig",
    "ToolsConfig",
    "TracesConfig",
    "VLLMEngineConfig",
    "WebChatChannelConfig",
    "WebhookChannelConfig",
    "WeatherToolConfig",
    "WhatsAppBaileysChannelConfig",
    "WhatsAppChannelConfig",
    "WorkflowConfig",
    "detect_hardware",
    "generate_default_toml",
    "generate_minimal_toml",
    "load_config",
    "recommend_engine",
    "recommend_model",
    "validate_config_key",
]

## ===== .gitignore : OUR COMMITS SINCE AUTHOR BASE =====
971e78f4 fix(mailbox): protected senders v2 - list moved to DEFAULT_CONFIG_DIR beside connector creds, every fallback logged, never empty (v1 failed open on blank lists); harness 19/19; untrack repo-root list; W61 handoff
58c05e28 gitignore: scope tools/ to repo root, stop ignoring traces package source
0389255b TTS: AudioContext playback engine + ChatArea driver rewrite; mailbox IMAP connector and tools; speech/CSP fixes
daafc769 fix: speech subsystem TTS streaming, backend file logging, uvicorn console fix, restore .gitignore
6015a448 feat: mic button fix, agent work, cloud router updates, HUD improvements
275a9fa1 feat: Graystone Lab cloud integration
f2fcb30c Graystone Lab: remote MCP/Ollama integration, Rust extension, UI fixes

## ===== .gitignore : CONFLICTED WORKING FILE (markers) =====
# venv / build
.venv/
__pycache__/
*.pyc
*.pyd
*.so
target/
dist/
build/
*.egg-info/

<<<<<<< HEAD
# node
node_modules/
=======
# Virtual environments
.venv/
venv/
env/

# IDE
.idea/
.vscode/
*.swp
*.swo
*~

# Testing
.pytest_cache/
.ruff_cache/
.coverage
htmlcov/

# uv
# Note: uv.lock is intentionally tracked â€” it pins all transitive deps for reproducibility.
# Uncomment the line below only if you deliberately choose not to commit the lock file.
# uv.lock

# OS
.DS_Store
Thumbs.db

# Secrets
.env
.env.*
# ...but keep checked-in example/templates (never contain real secrets)
!.env.example
!**/.env.example

# Project
*.sqlite
*.db
*.jsonl
*.npz
*.log
results/
logs/
# Anchored to repo root â€” DO NOT use the unanchored form `traces/`.
# hatchling honors .gitignore when building the wheel; an unanchored
# `traces/` pattern matches src/openjarvis/traces/ and silently drops
# the runtime module from the wheel (issue #372).
/traces/
coding_task_*
get-pip.py
# Junk from mocked-path tests that write to their mock's __repr__ as a path
MagicMock/

# MkDocs build output
site/

# Frontend
frontend/node_modules/
>>>>>>> a6dcf846
frontend/dist/
frontend/src-tauri/target/

# session diagnostics + scratch
/tools/
*.bak
*.bak-*
*.bak2_*
.fix_backups_*/
*.txt
!requirements*.txt

# stray root-level session scripts
/inspect-*.ps1
/patch-*.ps1
/check-*.ps1
/fix_*.ps1
/find-*.ps1
/cdp_*.ps1
/fe_stream_*.ps1
/stream_*.ps1
/toolcall_*.ps1
/apply-render-guard.ps1
/verify-build.ps1
/update-verify.ps1
/update_speech_backend.ps1
/vacuum_test.py
/OPENJARVIS_BUILD_VERIFIER.ps1

# binaries
*.exe
!frontend/src-tauri/**/*.exe

# local config / secrets
.env
cloud-keys.env
*.db
*.wav

# added 2026-08-05
*.bak_*
_bak/
export_full/
export_test/
temp_repo.zip
digest.mp3
diagnostics.json
memdb_*.json
frontend/tsconfig.tsbuildinfo
frontend/src-tauri/gen/
frontend/src-tauri/tauri.conf.json.backup1
src/openjarvis/traces/Engineering_Wiki/
src/openjarvis/server/static/

<<<<<<< HEAD
# W61: protected list lives in C:\Users\Admin\.openjarvis, not the repo
/protected_senders.json
=======
# NFS lock artifacts
.nfs*
**/.nfs*

# Research output
research_mining_*
.python-version
src/openjarvis/channels/whatsapp_baileys_bridge/node_modules/
src/openjarvis/agents/claude_code_runner/node_modules/

# SQLite in-memory artifacts
:memory:

# Dogfood reports (regenerated locally; not for VCS)
dogfood_report*.md

# Second Repos
Inline/
scratch/

# ---------------------------------------------------------------------------
# Distillation runtime artifacts (defense in depth â€” these should always live
# in ~/.openjarvis/, never inside the source tree, but we ignore them here in
# case OPENJARVIS_HOME is misconfigured during dev)
# ---------------------------------------------------------------------------
.openjarvis/
learning.db
**/learning/sessions/
**/learning/pending_review/
**/learning/benchmarks/
**/teacher_traces/
*.session.json

# Local dev artifacts (hybrid worker logs + cli debug dumps)
minion_logs/
*.oj-debug.json
oj-debug.*.json
>>>>>>> a6dcf846


## ===== .gitignore : STAGE 1 =====
# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class

# Distribution / packaging
dist/
build/
*.egg-info/
*.egg

# Virtual environments
.venv/
venv/
env/

# IDE
.idea/
.vscode/
*.swp
*.swo
*~

# Testing
.pytest_cache/
.ruff_cache/
.coverage
htmlcov/

# uv
# Note: uv.lock is intentionally tracked ΓÇö it pins all transitive deps for reproducibility.
# Uncomment the line below only if you deliberately choose not to commit the lock file.
# uv.lock

# OS
.DS_Store
Thumbs.db

# Secrets
.env
.env.*

# Project
*.sqlite
*.db
*.jsonl
*.npz
*.log
results/
logs/
traces/
coding_task_*
get-pip.py
# Junk from mocked-path tests that write to their mock's __repr__ as a path
MagicMock/

# MkDocs build output
site/

# Frontend
frontend/node_modules/
frontend/dist/

# Desktop
desktop/node_modules/
desktop/dist/
src/openjarvis/server/static/

# Desktop (Tauri)
frontend/src-tauri/target/

# Worktrees
.worktrees/

# Rust
target/

# Claude plan artifacts
docs/plans/
docs/superpowers/
.superpowers/

# Claude Code project instructions (per-developer)
CLAUDE.md
.claude/

# Tauri auto-generated schemas
**/src-tauri/gen/schemas/

# NFS lock artifacts
.nfs*
**/.nfs*

# Research output
research_mining_*
.python-version
src/openjarvis/channels/whatsapp_baileys_bridge/node_modules/

# SQLite in-memory artifacts
:memory:

# Dogfood reports (regenerated locally; not for VCS)
dogfood_report*.md

# Second Repos
Inline/
scratch/

# ---------------------------------------------------------------------------
# Distillation runtime artifacts (defense in depth ΓÇö these should always live
# in ~/.openjarvis/, never inside the source tree, but we ignore them here in
# case OPENJARVIS_HOME is misconfigured during dev)
# ---------------------------------------------------------------------------
.openjarvis/
learning.db
**/learning/sessions/
**/learning/pending_review/
**/learning/benchmarks/
**/teacher_traces/
*.session.json

## ===== .gitignore : STAGE 2 =====
# venv / build
.venv/
__pycache__/
*.pyc
*.pyd
*.so
target/
dist/
build/
*.egg-info/

# node
node_modules/
frontend/dist/
frontend/src-tauri/target/

# session diagnostics + scratch
/tools/
*.bak
*.bak-*
*.bak2_*
.fix_backups_*/
*.txt
!requirements*.txt

# stray root-level session scripts
/inspect-*.ps1
/patch-*.ps1
/check-*.ps1
/fix_*.ps1
/find-*.ps1
/cdp_*.ps1
/fe_stream_*.ps1
/stream_*.ps1
/toolcall_*.ps1
/apply-render-guard.ps1
/verify-build.ps1
/update-verify.ps1
/update_speech_backend.ps1
/vacuum_test.py
/OPENJARVIS_BUILD_VERIFIER.ps1

# binaries
*.exe
!frontend/src-tauri/**/*.exe

# local config / secrets
.env
cloud-keys.env
*.db
*.wav

# added 2026-08-05
*.bak_*
_bak/
export_full/
export_test/
temp_repo.zip
digest.mp3
diagnostics.json
memdb_*.json
frontend/tsconfig.tsbuildinfo
frontend/src-tauri/gen/
frontend/src-tauri/tauri.conf.json.backup1
src/openjarvis/traces/Engineering_Wiki/
src/openjarvis/server/static/

# W61: protected list lives in C:\Users\Admin\.openjarvis, not the repo
/protected_senders.json

## ===== .gitignore : STAGE 3 =====
# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class

# Distribution / packaging
dist/
build/
*.egg-info/
*.egg

# Virtual environments
.venv/
venv/
env/

# IDE
.idea/
.vscode/
*.swp
*.swo
*~

# Testing
.pytest_cache/
.ruff_cache/
.coverage
htmlcov/

# uv
# Note: uv.lock is intentionally tracked ΓÇö it pins all transitive deps for reproducibility.
# Uncomment the line below only if you deliberately choose not to commit the lock file.
# uv.lock

# OS
.DS_Store
Thumbs.db

# Secrets
.env
.env.*
# ...but keep checked-in example/templates (never contain real secrets)
!.env.example
!**/.env.example

# Project
*.sqlite
*.db
*.jsonl
*.npz
*.log
results/
logs/
# Anchored to repo root ΓÇö DO NOT use the unanchored form `traces/`.
# hatchling honors .gitignore when building the wheel; an unanchored
# `traces/` pattern matches src/openjarvis/traces/ and silently drops
# the runtime module from the wheel (issue #372).
/traces/
coding_task_*
get-pip.py
# Junk from mocked-path tests that write to their mock's __repr__ as a path
MagicMock/

# MkDocs build output
site/

# Frontend
frontend/node_modules/
frontend/dist/

# Desktop
desktop/node_modules/
desktop/dist/
src/openjarvis/server/static/

# Desktop (Tauri)
frontend/src-tauri/target/

# Worktrees
.worktrees/

# Rust
target/

# Claude plan artifacts
docs/plans/
docs/superpowers/
.superpowers/

# Claude Code project instructions (per-developer)
CLAUDE.md
.claude/

# Tauri auto-generated schemas
**/src-tauri/gen/schemas/

# NFS lock artifacts
.nfs*
**/.nfs*

# Research output
research_mining_*
.python-version
src/openjarvis/channels/whatsapp_baileys_bridge/node_modules/
src/openjarvis/agents/claude_code_runner/node_modules/

# SQLite in-memory artifacts
:memory:

# Dogfood reports (regenerated locally; not for VCS)
dogfood_report*.md

# Second Repos
Inline/
scratch/

# ---------------------------------------------------------------------------
# Distillation runtime artifacts (defense in depth ΓÇö these should always live
# in ~/.openjarvis/, never inside the source tree, but we ignore them here in
# case OPENJARVIS_HOME is misconfigured during dev)
# ---------------------------------------------------------------------------
.openjarvis/
learning.db
**/learning/sessions/
**/learning/pending_review/
**/learning/benchmarks/
**/teacher_traces/
*.session.json

# Local dev artifacts (hybrid worker logs + cli debug dumps)
minion_logs/
*.oj-debug.json
oj-debug.*.json

## ===== configs/openjarvis/config.toml : OUR COMMITS SINCE AUTHOR BASE =====
cc84aaec chore(config): memory context tuning block and fix_interface.ps1 path repair
e0e36523 Fix: wire tools to native_openhands agent - file_read, think, calculator, code_interpreter, shell_exec, file_write now loading at startup
6015a448 feat: mic button fix, agent work, cloud router updates, HUD improvements
3782799b feat: speech subsystem, auto-focus, pyproject fixes, pynvml->nvidia-ml-py, startup scripts
bc498a16 feat: Arc Reactor ThinkingCircle, fix env loading, fix project root, add research types, remove debug code
f2fcb30c Graystone Lab: remote MCP/Ollama integration, Rust extension, UI fixes

## ===== configs/openjarvis/config.toml : CONFLICTED WORKING FILE (markers) =====
# OpenJarvis configuration Ã¢â‚¬â€ remote Ollama host

# Ã¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢Â
# PILLAR 1: Intelligence Ã¢â‚¬â€ The Model
# Ã¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢Â
[intelligence]
default_model = "qwen2.5-coder:32b"
fallback_model = "qwen3.5:9b"
preferred_engine = "ollama"
provider = "remote"
quantization = "none"
# Generation defaults
temperature = 0.0
max_tokens = 2048
top_p = 0.9
top_k = 40
repetition_penalty = 1.0

# Ã¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢Â
# PILLAR 2: Agent Ã¢â‚¬â€ The Agentic Harness
# Ã¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢Â
[agent]
default_agent = "native_openhands"
max_turns = 8
tools = "code_interpreter,file_read,file_write,shell_exec,think,calculator"
objective = "Answer questions accurately using available tools and documents"
context_from_memory = true

# Ã¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢Â
# PILLAR 3: Tools Ã¢â‚¬â€ MCP Interface
# Ã¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢Â
[tools.storage]
default_backend = "sqlite"
db_path = "~/.openjarvis/memory.db"

[tools.mcp]
enabled = true

# Ã¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢Â
# PILLAR 4: Engine Ã¢â‚¬â€ The Inference Runtime
# Ã¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢Â
[engine]
default = "ollama"

[engine.vllm]
host = "http://localhost:8010"

[engine.ollama]
host = "http://172.16.33.200:11434"

[engine.sglang]
host = "http://localhost:30000"

[engine.llamacpp]
host = "http://localhost:8080"

[engine.exo]
host = "http://localhost:52415"

[engine.nexa]
host = "http://localhost:18181"
# device = "npu"  # optional: cpu, gpu, npu

[engine.uzu]
host = "http://localhost:8080"

[engine.apple_fm]
host = "http://localhost:8079"                # OpenAI-compatible shim

# In-process Apple Foundation Models (macOS 26+, Apple Intelligence enabled).
# Install with: uv pip install -e '.[afm]'
[engine.afm]
# instructions = ""                           # applied to every session
# use_case = "general"                        # or "content_tagging"
# guardrails = "default"                      # or "permissive_content_transformations"
sampling = "greedy"                           # or "random" (the SDK default)

# Ã¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢Â
# PILLAR 5: Learning Ã¢â‚¬â€ Improvement Methodologies
# Ã¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢Â
[learning]
enabled = false

[learning.routing]
policy = "heuristic"

[learning.intelligence]
policy = "none"

[learning.agent]
policy = "none"

[learning.metrics]
accuracy_weight = 0.6
latency_weight = 0.2
cost_weight = 0.1
efficiency_weight = 0.1

# Ã¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢Â
# Supporting config
# Ã¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢Â
[telemetry]
enabled = true
db_path = "~/.openjarvis/telemetry.db"
gpu_metrics = true
gpu_poll_interval_ms = 50
energy_vendor = ""
warmup_samples = 0
steady_state_window = 5
steady_state_threshold = 0.05

[traces]
enabled = true
db_path = "~/.openjarvis/traces.db"

[server]
<<<<<<< HEAD
host = "0.0.0.0"
port = 8010
=======
# Bind to loopback by default so the API is not exposed to the local network.
# To serve other devices on your LAN, set host = "0.0.0.0" AND set an API key
# (OPENJARVIS_API_KEY / `jarvis auth generate-key`) â€” startup refuses a
# non-loopback bind without a key. The "server" security profile also flips
# this to 0.0.0.0 intentionally.
host = "127.0.0.1"
port = 8000
>>>>>>> a6dcf846
agent = "native_openhands"

# Ã¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢Â
# PILLAR 6: Speech Ã¢â‚¬â€ Voice Input/Output
# Ã¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢Â
[speech]
backend = "faster-whisper"
model = "base"           # Options: tiny, base, small, medium, large-v3
device = "cpu"           # Use "cuda" for GPU, "cpu" for CPU
compute_type = "int8"    # For CPU. Use "float16" for GPU


# Ã¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢Â
# PILLAR 7: TTS Ã¢â‚¬â€ Text-to-Speech (Kokoro)
# Ã¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢ÂÃ¢â€¢Â
[tts]
backend = "kokoro"
voice = "am_adam"
speed = 1.0

[memory]
context_min_score = 20.0
context_top_k = 3
context_max_tokens = 1200


## ===== configs/openjarvis/config.toml : STAGE 1 =====
# OpenJarvis configuration ΓÇö GLM-4.7-Flash eval on 8x A100-80GB

# ΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉ
# PILLAR 1: Intelligence ΓÇö The Model
# ΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉ
[intelligence]
default_model = "zai-org/GLM-4.7-Flash"   # HuggingFace model ID
fallback_model = "glm-4.7-flash"          # Catalog alias fallback
preferred_engine = "vllm"                 # MoE model, vLLM is best for A100s
provider = "local"                        # Running locally on this machine
quantization = "none"                     # Full precision, we have 640GB VRAM
# Generation defaults for eval
temperature = 0.0                         # Deterministic for reproducibility
max_tokens = 2048                         # Standard eval output length
top_p = 0.9
top_k = 40
repetition_penalty = 1.0

# ΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉ
# PILLAR 2: Agent ΓÇö The Agentic Harness
# ΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉ
[agent]
default_agent = "native_openhands"        # CodeAct-style agent
max_turns = 10                            # Up to 10 tool-calling turns
tools = "code_interpreter,web_search,file_read,calculator,think"
objective = "Answer questions accurately using available tools"
context_from_memory = false               # No memory injection during eval

# ΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉ
# PILLAR 3: Tools ΓÇö MCP Interface
# ΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉ
[tools.storage]
default_backend = "sqlite"
db_path = "~/.openjarvis/memory.db"

[tools.mcp]
enabled = true

# ΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉ
# PILLAR 4: Engine ΓÇö The Inference Runtime
# ΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉ
[engine]
default = "vllm"

[engine.vllm]
host = "http://localhost:8001"            # vLLM serving port

[engine.ollama]
host = "http://localhost:11434"

[engine.sglang]
host = "http://localhost:30000"

[engine.llamacpp]
host = "http://localhost:8080"

[engine.exo]
host = "http://localhost:52415"

[engine.nexa]
host = "http://localhost:18181"
# device = "npu"  # optional: cpu, gpu, npu

[engine.uzu]
host = "http://localhost:8080"

[engine.apple_fm]
host = "http://localhost:8079"

# ΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉ
# PILLAR 5: Learning ΓÇö Improvement Methodologies
# ΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉ
[learning]
enabled = false                           # No learning during eval

[learning.routing]
policy = "heuristic"

[learning.intelligence]
policy = "none"

[learning.agent]
policy = "none"

[learning.metrics]
accuracy_weight = 0.6
latency_weight = 0.2
cost_weight = 0.1
efficiency_weight = 0.1

# ΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉ
# Supporting config
# ΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉ
[telemetry]
enabled = true
db_path = "~/.openjarvis/telemetry.db"
gpu_metrics = true
gpu_poll_interval_ms = 50
energy_vendor = ""                       # Auto-detect; or force "nvidia"/"amd"/"apple"/"cpu_rapl"
warmup_samples = 0                       # Warmup iterations before steady-state measurement
steady_state_window = 5                  # Sliding window size for CV stability check
steady_state_threshold = 0.05            # Coefficient of variation threshold for steady state

[traces]
enabled = true                            # Record traces for analysis
db_path = "~/.openjarvis/traces.db"

[server]
host = "0.0.0.0"
port = 8000
agent = "native_openhands"

## ===== configs/openjarvis/config.toml : STAGE 2 =====
# OpenJarvis configuration ├óΓé¼ΓÇ¥ remote Ollama host

# ├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É
# PILLAR 1: Intelligence ├óΓé¼ΓÇ¥ The Model
# ├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É
[intelligence]
default_model = "qwen2.5-coder:32b"
fallback_model = "qwen3.5:9b"
preferred_engine = "ollama"
provider = "remote"
quantization = "none"
# Generation defaults
temperature = 0.0
max_tokens = 2048
top_p = 0.9
top_k = 40
repetition_penalty = 1.0

# ├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É
# PILLAR 2: Agent ├óΓé¼ΓÇ¥ The Agentic Harness
# ├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É
[agent]
default_agent = "native_openhands"
max_turns = 8
tools = "code_interpreter,file_read,file_write,shell_exec,think,calculator"
objective = "Answer questions accurately using available tools and documents"
context_from_memory = true

# ├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É
# PILLAR 3: Tools ├óΓé¼ΓÇ¥ MCP Interface
# ├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É
[tools.storage]
default_backend = "sqlite"
db_path = "~/.openjarvis/memory.db"

[tools.mcp]
enabled = true

# ├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É
# PILLAR 4: Engine ├óΓé¼ΓÇ¥ The Inference Runtime
# ├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É
[engine]
default = "ollama"

[engine.vllm]
host = "http://localhost:8010"

[engine.ollama]
host = "http://172.16.33.200:11434"

[engine.sglang]
host = "http://localhost:30000"

[engine.llamacpp]
host = "http://localhost:8080"

[engine.exo]
host = "http://localhost:52415"

[engine.nexa]
host = "http://localhost:18181"
# device = "npu"  # optional: cpu, gpu, npu

[engine.uzu]
host = "http://localhost:8080"

[engine.apple_fm]
host = "http://localhost:8079"

# ├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É
# PILLAR 5: Learning ├óΓé¼ΓÇ¥ Improvement Methodologies
# ├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É
[learning]
enabled = false

[learning.routing]
policy = "heuristic"

[learning.intelligence]
policy = "none"

[learning.agent]
policy = "none"

[learning.metrics]
accuracy_weight = 0.6
latency_weight = 0.2
cost_weight = 0.1
efficiency_weight = 0.1

# ├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É
# Supporting config
# ├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É
[telemetry]
enabled = true
db_path = "~/.openjarvis/telemetry.db"
gpu_metrics = true
gpu_poll_interval_ms = 50
energy_vendor = ""
warmup_samples = 0
steady_state_window = 5
steady_state_threshold = 0.05

[traces]
enabled = true
db_path = "~/.openjarvis/traces.db"

[server]
host = "0.0.0.0"
port = 8010
agent = "native_openhands"

# ├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É
# PILLAR 6: Speech ├óΓé¼ΓÇ¥ Voice Input/Output
# ├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É
[speech]
backend = "faster-whisper"
model = "base"           # Options: tiny, base, small, medium, large-v3
device = "cpu"           # Use "cuda" for GPU, "cpu" for CPU
compute_type = "int8"    # For CPU. Use "float16" for GPU


# ├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É
# PILLAR 7: TTS ├óΓé¼ΓÇ¥ Text-to-Speech (Kokoro)
# ├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É├óΓÇó┬É
[tts]
backend = "kokoro"
voice = "am_adam"
speed = 1.0

[memory]
context_min_score = 20.0
context_top_k = 3
context_max_tokens = 1200

## ===== configs/openjarvis/config.toml : STAGE 3 =====
# OpenJarvis configuration ΓÇö GLM-4.7-Flash eval on 8x A100-80GB

# ΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉ
# PILLAR 1: Intelligence ΓÇö The Model
# ΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉ
[intelligence]
default_model = "zai-org/GLM-4.7-Flash"   # HuggingFace model ID
fallback_model = "glm-4.7-flash"          # Catalog alias fallback
preferred_engine = "vllm"                 # MoE model, vLLM is best for A100s
provider = "local"                        # Running locally on this machine
quantization = "none"                     # Full precision, we have 640GB VRAM
# Generation defaults for eval
temperature = 0.0                         # Deterministic for reproducibility
max_tokens = 2048                         # Standard eval output length
top_p = 0.9
top_k = 40
repetition_penalty = 1.0

# ΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉ
# PILLAR 2: Agent ΓÇö The Agentic Harness
# ΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉ
[agent]
default_agent = "native_openhands"        # CodeAct-style agent
max_turns = 10                            # Up to 10 tool-calling turns
tools = "code_interpreter,web_search,file_read,calculator,think"
objective = "Answer questions accurately using available tools"
context_from_memory = false               # No memory injection during eval

# ΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉ
# PILLAR 3: Tools ΓÇö MCP Interface
# ΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉ
[tools.storage]
default_backend = "sqlite"
db_path = "~/.openjarvis/memory.db"

[tools.mcp]
enabled = true

# ΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉ
# PILLAR 4: Engine ΓÇö The Inference Runtime
# ΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉ
[engine]
default = "vllm"

[engine.vllm]
host = "http://localhost:8001"            # vLLM serving port

[engine.ollama]
host = "http://localhost:11434"

[engine.sglang]
host = "http://localhost:30000"

[engine.llamacpp]
host = "http://localhost:8080"

[engine.exo]
host = "http://localhost:52415"

[engine.nexa]
host = "http://localhost:18181"
# device = "npu"  # optional: cpu, gpu, npu

[engine.uzu]
host = "http://localhost:8080"

[engine.apple_fm]
host = "http://localhost:8079"                # OpenAI-compatible shim

# In-process Apple Foundation Models (macOS 26+, Apple Intelligence enabled).
# Install with: uv pip install -e '.[afm]'
[engine.afm]
# instructions = ""                           # applied to every session
# use_case = "general"                        # or "content_tagging"
# guardrails = "default"                      # or "permissive_content_transformations"
sampling = "greedy"                           # or "random" (the SDK default)

# ΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉ
# PILLAR 5: Learning ΓÇö Improvement Methodologies
# ΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉ
[learning]
enabled = false                           # No learning during eval

[learning.routing]
policy = "heuristic"

[learning.intelligence]
policy = "none"

[learning.agent]
policy = "none"

[learning.metrics]
accuracy_weight = 0.6
latency_weight = 0.2
cost_weight = 0.1
efficiency_weight = 0.1

# ΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉ
# Supporting config
# ΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉΓòÉ
[telemetry]
enabled = true
db_path = "~/.openjarvis/telemetry.db"
gpu_metrics = true
gpu_poll_interval_ms = 50
energy_vendor = ""                       # Auto-detect; or force "nvidia"/"amd"/"apple"/"cpu_rapl"
warmup_samples = 0                       # Warmup iterations before steady-state measurement
steady_state_window = 5                  # Sliding window size for CV stability check
steady_state_threshold = 0.05            # Coefficient of variation threshold for steady state

[traces]
enabled = true                            # Record traces for analysis
db_path = "~/.openjarvis/traces.db"

[server]
# Bind to loopback by default so the API is not exposed to the local network.
# To serve other devices on your LAN, set host = "0.0.0.0" AND set an API key
# (OPENJARVIS_API_KEY / `jarvis auth generate-key`) ΓÇö startup refuses a
# non-loopback bind without a key. The "server" security profile also flips
# this to 0.0.0.0 intentionally.
host = "127.0.0.1"
port = 8000
agent = "native_openhands"
