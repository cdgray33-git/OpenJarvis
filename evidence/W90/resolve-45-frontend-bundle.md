# RESOLVE 4.5 FRONTEND BUNDLE - W90 2026-09-25T21:13:46 - diff3 markers: <<<<<<< ours 3df27c53 ||||||| base af21bc18 ======= author a6dcf846 >>>>>>>

## ===== frontend/package.json : OUR COMMITS SINCE AUTHOR BASE =====
0389255b TTS: AudioContext playback engine + ChatArea driver rewrite; mailbox IMAP connector and tools; speech/CSP fixes
275a9fa1 feat: Graystone Lab cloud integration
bc498a16 feat: Arc Reactor ThinkingCircle, fix env loading, fix project root, add research types, remove debug code

## ===== frontend/package.json : CONFLICTED WORKING FILE (diff3) =====
{
  "name": "openjarvis-chat",
  "private": true,
  "version": "0.1.0",
  "type": "module",
  "packageManager": "npm@11.19.0",
  "engines": {
    "node": ">=22.22",
    "npm": ">=11.19.0 <12"
  },
  "scripts": {
    "dev": "vite",
    "build": "tsc -b && vite build",
    "build:tauri": "tsc -b && vite build",
    "preview": "vite preview",
    "tauri": "tauri",
    "test": "vitest run"
  },
  "dependencies": {
<<<<<<< ours
    "@base-ui/react": "^1.3.0",
    "@fontsource-variable/geist": "^5.2.8",
    "@tailwindcss/vite": "^4.2.1",
    "@tauri-apps/api": "^2.11.0",
||||||| base
    "@base-ui/react": "^1.3.0",
    "@fontsource-variable/geist": "^5.2.8",
    "@tailwindcss/vite": "^4.2.1",
    "@tauri-apps/api": "^2",
=======
    "@base-ui/react": "^1.8.0",
    "@fontsource-variable/geist": "^5.3.0",
    "@tailwindcss/vite": "^4.3.3",
    "@tauri-apps/api": "^2.11.1",
>>>>>>> theirs
    "@tauri-apps/plugin-autostart": "^2",
    "@tauri-apps/plugin-dialog": "^2.7.3",
    "@tauri-apps/plugin-global-shortcut": "^2",
    "@tauri-apps/plugin-notification": "^2",
    "@tauri-apps/plugin-process": "^2",
    "@tauri-apps/plugin-shell": "^2",
    "@tauri-apps/plugin-updater": "^2",
    "class-variance-authority": "^0.7.1",
    "clsx": "^2.1.1",
<<<<<<< ours
    "katex": "^0.16.38",
    "lucide-react": "^0.576.0",
    "motion": "^12.38.0",
    "posthog-js": "^1.381.0",
    "react": "^19.0.0",
    "react-dom": "^19.0.0",
||||||| base
    "katex": "^0.16.38",
    "lucide-react": "^0.576.0",
    "motion": "^12.38.0",
    "posthog-js": "^1.373.2",
    "react": "^19.0.0",
    "react-dom": "^19.0.0",
=======
    "katex": "^0.18.7",
    "lucide-react": "^1.46.0",
    "motion": "^13.3.0",
    "posthog-js": "^1.433.5",
    "react": "^19.3.0",
    "react-dom": "^19.3.0",
>>>>>>> theirs
    "react-markdown": "^10.1.0",
    "react-router": "^8.4.0",
    "recharts": "^3.10.1",
    "rehype-highlight": "^7.0.2",
    "rehype-katex": "^7.0.1",
    "remark-gfm": "^4.0.1",
    "remark-math": "^6.0.0",
    "shadcn": "^4.21.0",
    "sonner": "^2.0.8",
    "tailwind-merge": "^3.7.0",
    "tailwindcss": "^4.3.3",
    "tw-animate-css": "^1.4.0",
    "zustand": "^5.0.15"
  },
  "devDependencies": {
    "@tauri-apps/cli": "^2.11.4",
    "@types/react": "^19.3.0",
    "@types/react-dom": "^19.3.0",
    "@vitejs/plugin-react": "^5.2.0",
    "typescript": "~7.0.2",
    "vite": "^8.3.0",
    "vite-plugin-pwa": "^1.3.0",
    "vitest": "^5.0.1"
  },
  "allowScripts": {
    "core-js": false,
    "fsevents": false
  }
}


## ===== frontend/src-tauri/Cargo.toml : OUR COMMITS SINCE AUTHOR BASE =====
3782799b feat: speech subsystem, auto-focus, pyproject fixes, pynvml->nvidia-ml-py, startup scripts
bc498a16 feat: Arc Reactor ThinkingCircle, fix env loading, fix project root, add research types, remove debug code

## ===== frontend/src-tauri/Cargo.toml : CONFLICTED WORKING FILE (diff3) =====
[package]
name = "openjarvis-desktop"
version = "0.1.0"
description = "OpenJarvis Desktop â€” Native AI assistant with energy monitoring, trace debugging, and learning visualization"
edition = "2021"
license = "MIT"

[build-dependencies]
tauri-build = { version = "2", features = [] }

[dependencies]
<<<<<<< ours
tauri = { version = "=2.11.0", features = ["tray-icon"] }
||||||| base
tauri = { version = "2", features = ["tray-icon"] }
=======
toml_edit = "0.25"
tauri = { version = "2", features = ["tray-icon"] }
>>>>>>> theirs
tauri-plugin-notification = "2"
tauri-plugin-shell = "2"
tauri-plugin-global-shortcut = "2"
tauri-plugin-autostart = "2"
tauri-plugin-updater = "2"
tauri-plugin-single-instance = "2"
tauri-plugin-process = "2"
tauri-plugin-dialog = "2"
serde = { version = "1", features = ["derive"] }
serde_json = "1"
reqwest = { version = "0.13", features = ["json", "multipart"] }
tokio = { version = "1", features = ["full"] }

# Cloud API keys are stored in the OS credential store via `keyring`. keyring v3
# enables NO backend by default â€” without an explicit per-platform feature it
# silently falls back to a non-persistent in-memory mock, so keys would not
# survive an app restart. Each desktop target opts into its native store.
[target.'cfg(target_os = "macos")'.dependencies]
objc = "0.2"
dispatch = "0.2"
keyring = { version = "3", features = ["apple-native"] }

[target.'cfg(target_os = "windows")'.dependencies]
keyring = { version = "3", features = ["windows-native"] }

[target.'cfg(target_os = "linux")'.dependencies]
# Blocking Secret Service backend (no internal async runtime, so it is safe to
# call from the tokio-driven Tauri commands). Needs libdbus-1-dev at build time.
keyring = { version = "3", features = ["sync-secret-service", "crypto-rust"] }

[features]
default = ["custom-protocol"]
custom-protocol = ["tauri/custom-protocol"]


## ===== frontend/src-tauri/src/lib.rs : OUR COMMITS SINCE AUTHOR BASE =====
0389255b TTS: AudioContext playback engine + ChatArea driver rewrite; mailbox IMAP connector and tools; speech/CSP fixes
bc498a16 feat: Arc Reactor ThinkingCircle, fix env loading, fix project root, add research types, remove debug code
383ccd5e Graystone Lab fixes: - Disable auth middleware for local network use (app.py) - Fix SetupScreen ollama_ready step logic (SetupScreen.tsx) - Add ollama_ready to SetupStatus interface (api.ts) - Remove uv sync and startup model checks from boot sequence (lib.rs) - Fix configured_ollama_host to ensure http:// prefix (lib.rs) - Add system32 hardcoded path to find_project_root (lib.rs) - Fix config.toml: server host 127.0.0.1, port 8010 - Input focus fix after response (InputArea.tsx) - Thinking spinner during generation (InputArea.tsx)
7088cba4 Fix: disable auth middleware, fix project root detection
f2fcb30c Graystone Lab: remote MCP/Ollama integration, Rust extension, UI fixes

## ===== frontend/src-tauri/src/lib.rs : CONFLICTED WORKING FILE (diff3) =====
use std::sync::Arc;
use std::time::Duration;
use tauri::menu::{MenuBuilder, MenuItemBuilder};
use tauri::tray::TrayIconBuilder;
use tauri::Manager;
use tauri_plugin_autostart::MacosLauncher;
use tokio::sync::Mutex;
// ---------------------------------------------------------------------------
// Startup env loader - reads openjarvis.env from next to the exe
// ---------------------------------------------------------------------------

fn exe_dir() -> std::path::PathBuf {
    std::env::current_exe()
        .ok()
        .and_then(|p| p.parent().map(|d| d.to_path_buf()))
        .unwrap_or_else(|| std::path::PathBuf::from("."))
}

fn log_startup(msg: &str) {
    let log_path = exe_dir().join("openjarvis-startup.log");
    use std::io::Write;
    if let Ok(mut f) = std::fs::OpenOptions::new()
        .create(true).append(true).open(&log_path)
    {
        let ts = std::time::SystemTime::now()
            .duration_since(std::time::UNIX_EPOCH)
            .map(|d| d.as_secs())
            .unwrap_or(0);
        let _ = writeln!(f, "[{}] {}", ts, msg);
    }
}

fn load_env_file() {
    let env_path = exe_dir().join("openjarvis.env");
    log_startup(&format!("load_env_file: looking for {:?}", env_path));
    if let Ok(contents) = std::fs::read_to_string(&env_path) {
        for line in contents.lines() {
            let line = line.trim();
            if line.is_empty() || line.starts_with('#') { continue; }
            if let Some((key, val)) = line.split_once('=') {
                let key = key.trim();
                let val = val.trim();
                std::env::set_var(key, val);
                log_startup(&format!("  set {}={}", key, val));
            }
        }
        log_startup("load_env_file: done");
    } else {
        log_startup("load_env_file: openjarvis.env NOT FOUND - falling back to system env");
    }
}


// Check if remote Ollama is configured
fn is_remote_ollama() -> bool {
    std::env::var("OPENJARVIS_OLLAMA_HOST")
        .or_else(|_| std::env::var("OLLAMA_HOST"))
        .map(|h| !h.starts_with("127.0.0.1") && !h.starts_with("localhost") && !h.is_empty())
        .unwrap_or(false)
}

const OLLAMA_PORT: u16 = 11434;
<<<<<<< ours
const JARVIS_PORT: u16 = 8010;
||||||| base
const JARVIS_PORT: u16 = 8000;
=======
const JARVIS_PORT: u16 = 8000;
const DESKTOP_UV_SYNC_COMMAND: &str =
    "uv sync --extra desktop --extra inference-cloud --extra inference-google --group desktop-native";
>>>>>>> theirs

<<<<<<< ours
/// Small, fast model pulled at startup so the app opens quickly.
const STARTUP_MODEL: &str = "qwen2.5-coder:14b-instruct-q4_K_M";
||||||| base
/// Small, fast model pulled at startup so the app opens quickly.
const STARTUP_MODEL: &str = "qwen3.5:4b";
=======
/// Small, fast model used when startup needs a default Ollama tag.
const STARTUP_MODEL: &str = "qwen3.5:4b";
>>>>>>> theirs

/// Tiny fallback model if even the startup model can't be pulled.
const FALLBACK_MODEL: &str = "qwen3:0.6b";

/// Qwen3.5 model variants, ordered smallest to largest.
/// Each entry is (ollama_tag, approximate_download_size_gb, min_ram_gb).
const QWEN35_MODELS: &[(&str, f64, f64)] = &[
    ("qwen3.5:0.8b", 1.0, 4.0),
    ("qwen3.5:2b", 2.7, 6.0),
    ("qwen3.5:4b", 3.4, 8.0),
    ("qwen3.5:9b", 6.6, 12.0),
    ("qwen3.5:27b", 17.0, 24.0),
    ("qwen3.5:35b", 24.0, 32.0),
    ("qwen3.5:122b", 81.0, 96.0),
];

/// Get total system RAM in GB.
fn total_ram_gb() -> f64 {
    #[cfg(target_os = "macos")]
    {
        use std::process::Command;
        if let Ok(output) = Command::new("sysctl").args(["-n", "hw.memsize"]).output() {
            if let Ok(s) = String::from_utf8(output.stdout) {
                if let Ok(bytes) = s.trim().parse::<u64>() {
                    return bytes as f64 / (1024.0 * 1024.0 * 1024.0);
                }
            }
        }
    }
    #[cfg(target_os = "linux")]
    {
        if let Ok(contents) = std::fs::read_to_string("/proc/meminfo") {
            for line in contents.lines() {
                if line.starts_with("MemTotal:") {
                    if let Some(kb_str) = line.split_whitespace().nth(1) {
                        if let Ok(kb) = kb_str.parse::<u64>() {
                            return kb as f64 / (1024.0 * 1024.0);
                        }
                    }
                }
            }
        }
    }
    #[cfg(target_os = "windows")]
    {
        use std::process::Command;
        // wmic returns TotalVisibleMemorySize in KB
        if let Ok(output) = Command::new("wmic")
            .args(["OS", "get", "TotalVisibleMemorySize", "/value"])
            .output()
        {
            if let Ok(s) = String::from_utf8(output.stdout) {
                for line in s.lines() {
                    if let Some(val) = line.strip_prefix("TotalVisibleMemorySize=") {
                        if let Ok(kb) = val.trim().parse::<u64>() {
                            return kb as f64 / (1024.0 * 1024.0);
                        }
                    }
                }
            }
        }
    }
    8.0
}

/// Return the Qwen3.5 models that fit in `ram_gb`, smallest first.
fn models_that_fit_in(ram_gb: f64) -> Vec<&'static str> {
    QWEN35_MODELS
        .iter()
        .filter(|(_, _, min_ram)| ram_gb >= *min_ram)
        .map(|(tag, _, _)| *tag)
        .collect()
}

<<<<<<< ours
/// Pick the default model - prefers STARTUP_MODEL if it fits, otherwise
/// falls back to the third-largest model that fits on this machine.
fn preferred_model() -> &'static str {
    let fitting = models_that_fit();
    // Prefer STARTUP_MODEL when it fits (fast, good quality)
    if fitting.contains(&STARTUP_MODEL) {
        return STARTUP_MODEL;
    }
||||||| base
/// Pick the default model â€” prefers STARTUP_MODEL if it fits, otherwise
/// falls back to the third-largest model that fits on this machine.
fn preferred_model() -> &'static str {
    let fitting = models_that_fit();
    // Prefer STARTUP_MODEL when it fits (fast, good quality)
    if fitting.contains(&STARTUP_MODEL) {
        return STARTUP_MODEL;
    }
=======
/// The default local model: the second-largest Qwen3.5 model that fits in
/// `ram_gb`. Falls back to the only fitting model, or FALLBACK_MODEL if none
/// fit. Deliberately NOT the largest â€” leaves RAM headroom for the OS/app.
fn default_local_model(ram_gb: f64) -> &'static str {
    let fitting = models_that_fit_in(ram_gb);
>>>>>>> theirs
    match fitting.len() {
        0 => FALLBACK_MODEL,
        1 => fitting[0],
        n => fitting[n - 2],
    }
}

/// A resolved boot plan derived purely from the inference config + RAM.
/// Pure and side-effect-free so it can be unit-tested without spawning
/// processes or touching the network.
#[derive(Debug, Clone, PartialEq, Eq)]
struct BootPlan {
    /// Whether to start and wait for the bundled Ollama.
    launch_ollama: bool,
    /// The preferred Ollama model (None for custom endpoints).
    model_to_pull: Option<String>,
    /// Optional `(engine_key, bare_host)` override for a custom endpoint,
    /// e.g. `("lmstudio", "http://localhost:1234")`. Written into
    /// ~/.openjarvis/config.toml so `jarvis serve` picks it up.
    engine_host: Option<(String, String)>,
    /// Args appended after `uv run jarvis serve --port <port>`.
    serve_args: Vec<String>,
}

/// Default OpenAI-compatible engine key used when a custom endpoint config
/// omits one (LM Studio is the canonical local server).
const CUSTOM_FALLBACK_ENGINE: &str = "lmstudio";

/// Decide what to launch/pull/serve from the inference config + system RAM.
/// Pure: no I/O, no spawning.
fn boot_plan(cfg: &InferenceConfig, ram_gb: f64) -> BootPlan {
    match cfg.kind {
        SourceKind::Ollama => {
            let model = cfg
                .model
                .clone()
                .unwrap_or_else(|| default_local_model(ram_gb).to_string());
            BootPlan {
                launch_ollama: true,
                model_to_pull: Some(model.clone()),
                engine_host: None,
                serve_args: vec![
                    "--engine".into(),
                    "ollama".into(),
                    "--model".into(),
                    model,
                    "--agent".into(),
                    "simple".into(),
                ],
            }
        }
        SourceKind::Custom => {
            let engine = cfg
                .engine
                .clone()
                .unwrap_or_else(|| CUSTOM_FALLBACK_ENGINE.to_string());
            // Record (engine_key, bare_host) only when a host is configured, so
            // boot can write `[engine.<key>] host = ...` into config.toml. An
            // empty host is dropped (no override).
            let engine_host = cfg
                .host
                .clone()
                .filter(|h| !h.is_empty())
                .map(|h| (engine.clone(), h));
            // `model` may be empty if the config is malformed; `jarvis serve`
            // surfaces a clear error then (there is no universal default model
            // for an arbitrary endpoint).
            let model = cfg.model.clone().unwrap_or_default();
            BootPlan {
                launch_ollama: false,
                model_to_pull: None,
                engine_host,
                serve_args: vec![
                    "--engine".into(),
                    engine,
                    "--model".into(),
                    model,
                    "--agent".into(),
                    "simple".into(),
                ],
            }
        }
    }
}

/// Get the user home directory, handling both Unix (HOME) and Windows (USERPROFILE).
fn home_dir() -> String {
    std::env::var("HOME")
        .or_else(|_| std::env::var("USERPROFILE"))
        .unwrap_or_default()
}

/// Resolve full path to a binary by checking common locations.
/// macOS .app bundles don't inherit the shell PATH, so we probe manually.
fn resolve_bin(name: &str) -> String {
    let home = home_dir();

    #[cfg(not(target_os = "windows"))]
    let candidates = vec![
        format!("/opt/homebrew/bin/{name}"),
        format!("{home}/.local/bin/{name}"),
        format!("{home}/.cargo/bin/{name}"),
        format!("/usr/local/bin/{name}"),
        format!("/usr/bin/{name}"),
    ];

    #[cfg(target_os = "windows")]
    let candidates = {
        let localappdata = std::env::var("LOCALAPPDATA").unwrap_or_default();
        let programfiles = std::env::var("ProgramFiles").unwrap_or_default();
        let programfiles_x86 = std::env::var("ProgramFiles(x86)").unwrap_or_default();
        vec![
            // Git for Windows - standard install paths
            format!("{programfiles}\\Git\\cmd\\{name}.exe"),
            format!("{programfiles_x86}\\Git\\cmd\\{name}.exe"),
            format!("{localappdata}\\Programs\\Git\\cmd\\{name}.exe"),
            // Scoop package manager
            format!("{home}\\scoop\\shims\\{name}.exe"),
            // Cargo, local bin
            format!("{home}\\.cargo\\bin\\{name}.exe"),
            format!("{home}\\.local\\bin\\{name}.exe"),
            // Generic program locations
            format!("{localappdata}\\Programs\\{name}\\{name}.exe"),
            format!("{programfiles}\\{name}\\{name}.exe"),
            // Ollama installs to LOCALAPPDATA on Windows
            format!("{localappdata}\\Programs\\Ollama\\{name}.exe"),
            // uv installs via pip/pipx
            format!("{home}\\AppData\\Roaming\\Python\\Scripts\\{name}.exe"),
        ]
    };

    for path in &candidates {
        if std::path::Path::new(path).exists() {
            return path.clone();
        }
    }

    // Fallback: ask the OS to find it on PATH.
    // On Windows this uses `where.exe`, on Unix `which`.
    #[cfg(target_os = "windows")]
    {
        if let Ok(output) = std::process::Command::new("where")
            .arg(format!("{name}.exe"))
            .output()
        {
            if output.status.success() {
                let stdout = String::from_utf8_lossy(&output.stdout);
                if let Some(first_line) = stdout.lines().next() {
                    let p = first_line.trim();
                    if !p.is_empty() && std::path::Path::new(p).exists() {
                        return p.to_string();
                    }
                }
            }
        }
    }
    #[cfg(not(target_os = "windows"))]
    {
        if let Ok(output) = std::process::Command::new("which").arg(name).output() {
            if output.status.success() {
                let stdout = String::from_utf8_lossy(&output.stdout);
                if let Some(first_line) = stdout.lines().next() {
                    let p = first_line.trim();
                    if !p.is_empty() && std::path::Path::new(p).exists() {
                        return p.to_string();
                    }
                }
            }
        }
    }

    name.to_string()
}

/// Find the OpenJarvis project root (contains pyproject.toml).
/// Checks OPENJARVIS_ROOT env var, walks up from the executable, then
/// probes common clone locations.
fn find_project_root() -> Option<std::path::PathBuf> {
    // 1. Explicit env var override
    if let Ok(root) = std::env::var("OPENJARVIS_ROOT") {
        let path = std::path::PathBuf::from(&root);
        log_startup(&format!("find_project_root: OPENJARVIS_ROOT={:?} exists={}", path, path.join("pyproject.toml").exists()));
        if path.join("pyproject.toml").exists() {
            log_startup(&format!("find_project_root: using {:?}", path));
            return Some(path);
        } else {
            log_startup("find_project_root: OPENJARVIS_ROOT set but pyproject.toml missing - aborting fallback");
            return None;
        }
    }
    // 2. Walk up from the running executable (works in dev and .app bundle)
    if let Ok(exe) = std::env::current_exe() {
        let mut dir = exe.parent().map(|p| p.to_path_buf());
        for _ in 0..8 {
            if let Some(ref d) = dir {
                if d.join("pyproject.toml").exists() {
                    return Some(d.clone());
                }
                dir = d.parent().map(|p| p.to_path_buf());
            }
        }
    }

    // 3. Fallback: well-known direct paths
    let home = home_dir();
    let direct = [
        format!("{home}/OpenJarvis"),
        format!("{home}/projects/hazy/OpenJarvis"),
        format!("{home}/projects/OpenJarvis"),
        format!("{home}/src/OpenJarvis"),
        format!("{home}/Documents/OpenJarvis"),
        format!("{home}/Desktop/OpenJarvis"),
        format!("{home}/Developer/OpenJarvis"),
        format!("{home}/dev/OpenJarvis"),
        format!("{home}/Code/OpenJarvis"),
        format!("{home}/code/OpenJarvis"),
        format!("{home}/repos/OpenJarvis"),
        format!("{home}/github/OpenJarvis"),
    ];
    for p in &direct {
        let path = std::path::PathBuf::from(p);
        if path.join("pyproject.toml").exists() {
            return Some(path);
        }
    }

    // 4. Shallow scan: look for OpenJarvis one level inside common parent dirs.
    //    This catches clones like ~/Documents/my-stuff/OpenJarvis without
    //    needing to enumerate every possible intermediate folder.
    let scan_parents = [
        format!("{home}/Documents"),
        format!("{home}/Desktop"),
        format!("{home}/Developer"),
        format!("{home}/projects"),
        format!("{home}/repos"),
        format!("{home}/src"),
        format!("{home}/Code"),
        format!("{home}/code"),
        format!("{home}/dev"),
        format!("{home}/github"),
    ];
    for parent in &scan_parents {
        let parent_path = std::path::PathBuf::from(parent);
        if let Ok(entries) = std::fs::read_dir(&parent_path) {
            for entry in entries.flatten() {
                let candidate = entry.path().join("OpenJarvis");
                if candidate.join("pyproject.toml").exists() {
                    return Some(candidate);
                }
                // Also check if the entry itself is OpenJarvis (case-insensitive match)
                if let Some(name) = entry.file_name().to_str() {
                    if name.eq_ignore_ascii_case("openjarvis")
                        && entry.path().join("pyproject.toml").exists()
                    {
                        return Some(entry.path());
                    }
                }
            }
        }
    }

    None
}

// ---------------------------------------------------------------------------
// BackendManager - owns the Ollama + Jarvis server child processes
// ---------------------------------------------------------------------------

struct ChildHandle {
    child: tokio::process::Child,
}

impl ChildHandle {
    async fn kill(&mut self) {
        let _ = self.child.kill().await;
    }
}

/// Spawn a subprocess whose lifetime cannot escape the async operation that
/// created it.  Tokio's default is `kill_on_drop(false)`, which means aborting
/// the boot task in the small window between `spawn()` and storing the child in
/// `BackendManager` would detach it.  The same default also lets one-shot boot
/// commands (`git clone`, `uv sync`, extension verification) continue after a
/// source reset.  Every subprocess on the boot path must opt in here (or call
/// `kill_on_drop(true)` before `output()`).
fn spawn_owned_child(cmd: &mut tokio::process::Command) -> std::io::Result<tokio::process::Child> {
    cmd.kill_on_drop(true);
    cmd.spawn()
}

/// Rolling buffer holding the most recent ~16 KB of jarvis stderr.
///
/// Populated by a background drainer task spawned at boot so the pipe
/// never fills and back-pressures `jarvis serve`; consumed by the boot
/// path when surfacing failure messages.
type StderrTail = Arc<Mutex<Vec<u8>>>;

const STDERR_TAIL_LIMIT: usize = 16 * 1024;

struct BackendManager {
    ollama: Option<ChildHandle>,
    jarvis: Option<ChildHandle>,
    jarvis_stderr_tail: StderrTail,
    boot_task: Option<tauri::async_runtime::JoinHandle<()>>,
}

impl Default for BackendManager {
    fn default() -> Self {
        Self {
            ollama: None,
            jarvis: None,
            jarvis_stderr_tail: Arc::new(Mutex::new(Vec::new())),
            boot_task: None,
        }
    }
}

impl BackendManager {
    async fn stop_all(&mut self) {
        if let Some(task) = self.boot_task.take() {
            task.abort();
            // `abort()` only requests cancellation.  Await it before touching
            // children or returning so the boot future has dropped any local,
            // not-yet-registered child and cannot write config after reset.
            let _ = task.await;
        }
        if let Some(ref mut h) = self.jarvis {
            h.kill().await;
        }
        self.jarvis = None;
        if let Some(ref mut h) = self.ollama {
            h.kill().await;
        }
        self.ollama = None;
    }
}

type SharedBackend = Arc<Mutex<BackendManager>>;

/// Spawn exactly one tracked boot task. Keeping its handle lets recovery
/// abort an in-flight endpoint check/model download before killing children.
async fn start_managed_boot(backend: SharedBackend, status: SharedStatus) {
    let mut manager = backend.lock().await;
    if let Some(task) = manager.boot_task.take() {
        task.abort();
        let _ = task.await;
    }
    let task_backend = backend.clone();
    let task = tauri::async_runtime::spawn(boot_backend(task_backend, status));
    manager.boot_task = Some(task);
}

// ---------------------------------------------------------------------------
// Setup status (reported to frontend)
// ---------------------------------------------------------------------------

#[derive(serde::Serialize, Clone)]
struct SetupStatus {
    phase: String,
    detail: String,
    ollama_ready: bool,
    server_ready: bool,
    model_ready: bool,
    error: Option<String>,
    /// "unconfigured" | "ollama" | "custom" â€” lets the setup UI choose
    /// between the consent screen and source-aware progress labels.
    source: String,
    /// A fresh desktop install must collect an explicit source choice before
    /// any inference process is allowed to start.
    requires_source: bool,
}

impl Default for SetupStatus {
    fn default() -> Self {
        Self {
            phase: "awaiting_source".into(),
            detail: "Choose where OpenJarvis should run models.".into(),
            ollama_ready: false,
            server_ready: false,
            model_ready: false,
            error: None,
            source: "unconfigured".into(),
            requires_source: true,
        }
    }
}

impl SetupStatus {
    fn starting(cfg: &InferenceConfig) -> Self {
        Self {
            phase: "starting".into(),
            detail: "Initializing...".into(),
            source: match cfg.kind {
                SourceKind::Ollama => "ollama",
                SourceKind::Custom => "custom",
            }
            .into(),
            requires_source: false,
            ..Self::default()
        }
    }
}

type SharedStatus = Arc<Mutex<SetupStatus>>;

// ---------------------------------------------------------------------------
// Health-check helpers
// ---------------------------------------------------------------------------

async fn wait_for_url(url: &str, timeout: Duration) -> bool {
    let client = reqwest::Client::builder()
        .timeout(Duration::from_secs(2))
        .build()
        .unwrap();
    let deadline = tokio::time::Instant::now() + timeout;
    while tokio::time::Instant::now() < deadline {
        if let Ok(resp) = client.get(url).send().await {
            if resp.status().is_success() {
                return true;
            }
        }
        tokio::time::sleep(Duration::from_millis(500)).await;
    }
    false
}

/// True if a custom OpenAI-compatible endpoint answers at all (any HTTP
/// status counts â€” even a 404 proves the server is up). `host` is the bare
/// base URL; we probe `<host>/v1/models`.
async fn endpoint_reachable(host: &str, timeout: Duration) -> bool {
    let client = match reqwest::Client::builder()
        .timeout(Duration::from_secs(3))
        .build()
    {
        Ok(c) => c,
        Err(_) => return false,
    };
    let url = format!("{}/v1/models", host.trim_end_matches('/'));
    let deadline = tokio::time::Instant::now() + timeout;
    while tokio::time::Instant::now() < deadline {
        if client.get(&url).send().await.is_ok() {
            return true;
        }
        tokio::time::sleep(Duration::from_millis(500)).await;
    }
    false
}

/// Outcome of waiting for `jarvis serve` to become healthy.
///
/// Unlike [`wait_for_url`] this differentiates "server is up but degraded"
/// (HTTP 503 â€” usually inference engine failed to load) from "server never
/// came up" and from "child process died before serving anything", because
/// each needs a different user-facing message.
#[derive(Debug)]
enum JarvisStartResult {
    /// `/health` returned 2xx.
    Ready,
    /// Server replied 503. The body is the actionable message (typically
    /// "engine not ready" or a model-load error).
    ServiceUnavailable(String),
    /// The `jarvis serve` child exited before `/health` returned 2xx.
    EarlyExit { code: Option<i32>, stderr: String },
    /// Deadline elapsed without ever seeing 2xx or an early exit.
    Timeout,
}

/// Spawn a detached task that continuously drains `jarvis serve`'s
/// stderr into a rolling tail buffer.
///
/// We MUST keep reading stderr for as long as the child runs â€” `jarvis
/// serve` is chatty (engine load progress, request logs), and the OS
/// pipe buffer is small (4 KB on Windows, 64 KB on Linux). Once full,
/// the child's next stderr write blocks indefinitely and the server
/// hangs mid-operation. The drainer reads in chunks and keeps only the
/// last `STDERR_TAIL_LIMIT` bytes â€” enough to surface a tail trace if
/// the child later dies, without unbounded memory growth.
///
/// Returns immediately after spawning the task; the task ends naturally
/// when the child closes stderr (i.e. exits).
fn spawn_jarvis_stderr_drainer(mut stderr: tokio::process::ChildStderr, tail: StderrTail) {
    use tokio::io::AsyncReadExt;
    tokio::spawn(async move {
        let mut buf = vec![0u8; 4096];
        loop {
            match stderr.read(&mut buf).await {
                Ok(0) => break,  // EOF â€” child closed stderr
                Err(_) => break, // pipe broke â€” also done
                Ok(n) => {
                    let mut t = tail.lock().await;
                    t.extend_from_slice(&buf[..n]);
                    if t.len() > STDERR_TAIL_LIMIT {
                        let drop_n = t.len() - STDERR_TAIL_LIMIT;
                        t.drain(..drop_n);
                    }
                }
            }
        }
    });
}

/// Read whatever the stderr drainer has buffered so far.
///
/// Safe to call at any time; returns an empty string before the
/// drainer has seen any bytes. Trimmed.
async fn read_jarvis_stderr_tail(backend: &SharedBackend) -> String {
    let tail = backend.lock().await.jarvis_stderr_tail.clone();
    let bytes = tail.lock().await.clone();
    String::from_utf8_lossy(&bytes).trim().to_string()
}

/// Poll `jarvis serve` health, watching the child process state so we
/// never wait 10 minutes for a process that crashed in the first second.
async fn wait_for_jarvis_health(
    url: &str,
    timeout: Duration,
    backend: &SharedBackend,
) -> JarvisStartResult {
    let client = match reqwest::Client::builder()
        .timeout(Duration::from_secs(2))
        .build()
    {
        Ok(c) => c,
        Err(_) => return JarvisStartResult::Timeout,
    };
    let deadline = tokio::time::Instant::now() + timeout;
    loop {
        // 1. Has the child already exited? `try_wait` is non-blocking; on
        // Windows where uv / python / the Rust extension can fail to load
        // very fast, this catches the crash within ~500ms instead of after
        // the full HTTP timeout window.
        let exit_status = {
            let mut mgr = backend.lock().await;
            match mgr.jarvis.as_mut() {
                Some(h) => h.child.try_wait().ok().flatten(),
                None => None,
            }
        };
        if let Some(status) = exit_status {
            let stderr = read_jarvis_stderr_tail(backend).await;
            return JarvisStartResult::EarlyExit {
                code: status.code(),
                stderr,
            };
        }

        // 2. Try the health endpoint.
        match client.get(url).send().await {
            Ok(resp) => {
                let status = resp.status();
                if status.is_success() {
                    return JarvisStartResult::Ready;
                }
                if status == reqwest::StatusCode::SERVICE_UNAVAILABLE {
                    // Server is up but the inference engine is not. This
                    // is a terminal-for-us state â€” polling won't change
                    // anything; the user has to fix their engine config.
                    let body = resp.text().await.unwrap_or_default();
                    return JarvisStartResult::ServiceUnavailable(body);
                }
                // Other non-2xx (e.g. 404 during a brief routing-table
                // warmup window) â€” fall through and keep polling.
            }
            Err(_) => {
                // Connection refused / DNS / timeout â€” server still
                // booting. Keep polling.
            }
        }

        if tokio::time::Instant::now() >= deadline {
            return JarvisStartResult::Timeout;
        }
        tokio::time::sleep(Duration::from_millis(500)).await;
    }
}

async fn ollama_has_model(model: &str) -> bool {
    let models = ollama_model_names().await;
    matching_installed_model(&models, model).is_some()
}

fn parse_ollama_model_names(body: &serde_json::Value) -> Vec<String> {
    body.get("models")
        .and_then(|m| m.as_array())
        .map(|models| {
            models
                .iter()
                .filter_map(|m| {
                    m.get("name")
                        .or_else(|| m.get("model"))
                        .and_then(|n| n.as_str())
                })
                .filter(|name| !name.trim().is_empty())
                .map(|name| name.to_string())
                .collect()
        })
        .unwrap_or_default()
}

fn model_names_match(installed: &str, requested: &str) -> bool {
    installed == requested
        || installed.strip_suffix(":latest") == Some(requested)
        || requested.strip_suffix(":latest") == Some(installed)
}

fn matching_installed_model(models: &[String], requested: &str) -> Option<String> {
    models
        .iter()
        .find(|model| model_names_match(model, requested))
        .cloned()
}

fn model_name_looks_embedding_only(model: &str) -> bool {
    let name = model.to_ascii_lowercase();
    [
        "embed",
        "embedding",
        "rerank",
        "minilm",
        "bge-",
        "bge_",
        "e5-",
        "e5_",
    ]
    .iter()
    .any(|marker| name.contains(marker))
}

fn preferred_installed_model(models: &[String]) -> Option<String> {
    models
        .iter()
        .find(|model| !model.trim().is_empty() && !model_name_looks_embedding_only(model))
        .or_else(|| models.iter().find(|model| !model.trim().is_empty()))
        .cloned()
}

fn startup_installed_model(requested_model: &str, installed_models: &[String]) -> Option<String> {
    matching_installed_model(installed_models, requested_model)
        .or_else(|| preferred_installed_model(installed_models))
}

fn should_persist_resolved_model(cfg: &InferenceConfig) -> bool {
    cfg.model
        .as_deref()
        .map(|model| model.trim().is_empty())
        .unwrap_or(true)
}

async fn ollama_model_names() -> Vec<String> {
    let url = format!("http://127.0.0.1:{}/api/tags", OLLAMA_PORT);
    let client = reqwest::Client::builder()
        .timeout(Duration::from_secs(5))
        .build()
        .unwrap();
    if let Ok(resp) = client.get(&url).send().await {
        if let Ok(body) = resp.json::<serde_json::Value>().await {
            return parse_ollama_model_names(&body);
        }
    }
    Vec::new()
}

async fn pull_model(model: &str) -> Result<(), String> {
    let url = format!("http://127.0.0.1:{}/api/pull", OLLAMA_PORT);
    let client = reqwest::Client::builder()
        .timeout(Duration::from_secs(600))
        .build()
        .map_err(|e| e.to_string())?;
    let resp = client
        .post(&url)
        .json(&serde_json::json!({"name": model, "stream": false}))
        .send()
        .await
        .map_err(|e| format!("Pull request failed: {}", e))?;
    if !resp.status().is_success() {
        return Err(format!("Pull returned status {}", resp.status()));
    }
    Ok(())
}

// ---------------------------------------------------------------------------
// uv sync error formatting (pure helpers â€” unit-tested, see #331)
// ---------------------------------------------------------------------------

/// Last `max_chars` characters of a `uv sync` stderr stream, trimmed.
///
/// uv's actionable diagnostic almost always lands at the tail of the
/// stream, so when surfacing a failure to the user we show the end, not
/// the (usually noisy progress-spinner) beginning. Operates on `char`
/// boundaries so it never splits a multi-byte UTF-8 codepoint â€” important
/// because Windows consoles emit non-ASCII (cp9xx) bytes.
fn uv_sync_stderr_tail(stderr: &str, max_chars: usize) -> String {
    let total = stderr.chars().count();
    let skip = total.saturating_sub(max_chars);
    stderr
        .chars()
        .skip(skip)
        .collect::<String>()
        .trim()
        .to_string()
}

/// Error message shown when `uv sync` runs but exits non-zero (#331).
///
/// `exit_code` is `None` when the process was terminated by a signal with
/// no exit code (rendered as "unknown" rather than a misleading -1).
fn format_uv_sync_failure(root: &std::path::Path, exit_code: Option<i32>, stderr: &str) -> String {
    let code = exit_code
        .map(|c| c.to_string())
        .unwrap_or_else(|| "unknown".to_string());
    let tail = uv_sync_stderr_tail(stderr, 800);
    let rust_hint = if looks_like_rust_extension_build_error(stderr) {
        format!("\n\n{}", rust_toolchain_install_hint())
    } else {
        String::new()
    };
    format!(
        "`uv sync` failed in {} (exit {}). Last output:\n\n{}\n\n\
         Try opening a terminal in that directory and running \
         `{}` manually for the full output.{}",
        root.display(),
        code,
        tail,
        DESKTOP_UV_SYNC_COMMAND,
        rust_hint,
    )
}

/// Strip AppImage-injected environment from a subprocess command (#455).
///
/// When the OpenJarvis desktop binary is shipped as an AppImage, the AppImage
/// runtime sets `LD_LIBRARY_PATH` (and friends) to the extracted-to-/tmp
/// bundled lib dir. Any child we spawn inherits that env by default â€” but the
/// children we spawn (`uv`, `ollama`, `git`) live outside the AppImage and
/// must NOT load their shared libraries from the AppImage's bundle. The
/// classic symptom: `uv` finds `python3`, `python3` tries to `import numpy`,
/// numpy's `.so` files try to dlopen libstdc++/libssl/libcrypto, the linker
/// picks the AppImage's versions which were built against a different glibc
/// or libcrypto API, and python dies silently â€” before any startup log
/// reaches us. The user sees "API Server â€” starting server..." forever.
///
/// Fix: when we detect we're inside an AppImage (the AppImage runtime sets
/// `$APPIMAGE` to the original image path), strip the leaked env vars before
/// spawn. Conditional on `APPIMAGE` being set so regular Linux installs that
/// legitimately use `LD_LIBRARY_PATH` are untouched. Linux-only â€” the
/// `#[cfg]` makes this a no-op on macOS / Windows.
#[cfg_attr(not(target_os = "linux"), allow(unused_variables))]
fn prepare_subprocess_for_appimage(cmd: &mut tokio::process::Command) {
    #[cfg(target_os = "linux")]
    {
        if std::env::var_os("APPIMAGE").is_some() {
            cmd.env_remove("LD_LIBRARY_PATH");
            cmd.env_remove("LD_PRELOAD");
            cmd.env_remove("APPIMAGE");
            cmd.env_remove("APPIMAGE_UUID");
            cmd.env_remove("APPDIR");
            cmd.env_remove("ARGV0");
        }
    }
}

<<<<<<< ours
    // Skip Ollama startup if remote host is configured
    if is_remote_ollama() {
        let mut s = status.lock().await;
        s.ollama_ready = true;
        s.detail = "Using remote inference engine.".into();
    } else {
        // Try the bundled sidecar first, fall back to system ollama
        let ollama_child = {
            let ollama_bin = resolve_bin("ollama");
            let sidecar = tokio::process::Command::new(&ollama_bin)
                .arg("serve")
                .env("OLLAMA_HOST", format!("127.0.0.1:{}", OLLAMA_PORT))
                .stdout(std::process::Stdio::null())
                .stderr(std::process::Stdio::null())
                .spawn();
            match sidecar {
                Ok(child) => Some(child),
                Err(_) => None,
            }
        };
||||||| base
    // Try the bundled sidecar first, fall back to system ollama
    let ollama_child = {
        let ollama_bin = resolve_bin("ollama");
        let sidecar = tokio::process::Command::new(&ollama_bin)
            .arg("serve")
            .env("OLLAMA_HOST", format!("127.0.0.1:{}", OLLAMA_PORT))
            .stdout(std::process::Stdio::null())
            .stderr(std::process::Stdio::null())
            .spawn();
        match sidecar {
            Ok(child) => Some(child),
            Err(_) => None,
        }
    };
=======
/// Error message shown when `uv sync` can't even be spawned (#331) â€”
/// e.g. the resolved `uv` binary doesn't exist or isn't executable.
fn format_uv_sync_spawn_error(root: &std::path::Path, uv_bin: &str, err: &str) -> String {
    format!(
        "Could not run `uv sync`: {}. Verify uv is installed at \
         `{}` and the OpenJarvis repo is at `{}`.",
        err,
        uv_bin,
        root.display(),
    )
}

fn rust_toolchain_install_hint() -> &'static str {
    "The desktop app needs the Rust toolchain to build `openjarvis_rust`. \
     Install Rust from https://rustup.rs. On Windows, also install Visual Studio \
     Build Tools with the C++ workload, then relaunch."
}

fn looks_like_rust_extension_build_error(stderr: &str) -> bool {
    let lower = stderr.to_ascii_lowercase();
    [
        "openjarvis-rust",
        "openjarvis_rust",
        "maturin",
        "cargo",
        "rustc",
        "link.exe",
        "visual studio",
    ]
    .iter()
    .any(|marker| lower.contains(marker))
}

fn format_missing_rust_toolchain() -> String {
    format!(
        "Could not find Rust's `cargo` command. {}\n\n\
         If Rust is already installed, close and relaunch the desktop app so \
         PATH includes `~/.cargo/bin`.",
        rust_toolchain_install_hint(),
    )
}
>>>>>>> theirs

<<<<<<< ours
        if let Some(child) = ollama_child {
            backend.lock().await.ollama = Some(ChildHandle { child });
        }
||||||| base
    if let Some(child) = ollama_child {
        backend.lock().await.ollama = Some(ChildHandle { child });
    }
=======
fn format_extension_import_failure(root: &std::path::Path, stderr: &str) -> String {
    let tail = uv_sync_stderr_tail(stderr, 4000);
    format!(
        "`openjarvis_rust` is still not importable after building. Last output:\n\n{}\n\n\
         Run these manually for the full build log:\n\n\
           cd {}\n\
           {}\n\
           uv run python -c \"import openjarvis_rust\"",
        if tail.is_empty() {
            "(no stderr output)"
        } else {
            &tail
        },
        root.display(),
        DESKTOP_UV_SYNC_COMMAND,
    )
}

fn add_cargo_bin_to_path(cmd: &mut tokio::process::Command) {
    let mut paths: Vec<std::path::PathBuf> = std::env::var_os("PATH")
        .map(|path| std::env::split_paths(&path).collect())
        .unwrap_or_default();
    paths.insert(
        0,
        std::path::PathBuf::from(home_dir())
            .join(".cargo")
            .join("bin"),
    );
    if let Ok(joined) = std::env::join_paths(paths) {
        cmd.env("PATH", joined);
    }
}
>>>>>>> theirs

<<<<<<< ours
        let ollama_url = format!("http://127.0.0.1:{}/api/tags", OLLAMA_PORT);
        let ollama_ok = wait_for_url(&ollama_url, Duration::from_secs(30)).await;
||||||| base
    let ollama_url = format!("http://127.0.0.1:{}/api/tags", OLLAMA_PORT);
    let ollama_ok = wait_for_url(&ollama_url, Duration::from_secs(30)).await;
=======
async fn verify_openjarvis_rust_extension(
    root: &std::path::Path,
    uv_bin: &str,
) -> Result<(), String> {
    let mut cmd = tokio::process::Command::new(uv_bin);
    cmd.args(["run", "python", "-c", "import openjarvis_rust"])
        .stdout(std::process::Stdio::null())
        .stderr(std::process::Stdio::piped())
        .current_dir(root);
    prepare_subprocess_for_appimage(&mut cmd);
    add_cargo_bin_to_path(&mut cmd);
    cmd.kill_on_drop(true);

    match cmd.output().await {
        Ok(out) if out.status.success() => Ok(()),
        Ok(out) => {
            let stderr = String::from_utf8_lossy(&out.stderr);
            Err(format_extension_import_failure(root, &stderr))
        }
        Err(e) => Err(format!(
            "Could not verify `openjarvis_rust`: {}. Verify uv is installed at `{}`.",
            e, uv_bin
        )),
    }
}
>>>>>>> theirs

<<<<<<< ours
        if !ollama_ok {
            let mut s = status.lock().await;
            s.error = Some("Could not start Ollama. Install it from https://ollama.com".into());
            return;
        }
||||||| base
    if !ollama_ok {
        let mut s = status.lock().await;
        s.error = Some("Could not start Ollama. Install it from https://ollama.com".into());
        return;
    }
=======
fn port_owner_hint() -> String {
    if cfg!(target_os = "windows") {
        format!("netstat -ano | findstr :{}", JARVIS_PORT)
    } else {
        format!("lsof -i :{}", JARVIS_PORT)
    }
}
>>>>>>> theirs

<<<<<<< ours
        {
            let mut s = status.lock().await;
            s.ollama_ready = true;
            s.detail = "Inference engine ready.".into();
        }
||||||| base
    {
        let mut s = status.lock().await;
        s.ollama_ready = true;
        s.detail = "Inference engine ready.".into();
=======
fn format_port_unavailable(port: u16, reason: &str) -> String {
    format!(
        "Port {} is not available: {}. Stop the process using that port or \
         change the OpenJarvis port, then relaunch.\n\nTo identify it:\n  {}",
        port,
        reason,
        port_owner_hint(),
    )
}

fn check_jarvis_port_available() -> Result<(), String> {
    match std::net::TcpListener::bind(("127.0.0.1", JARVIS_PORT)) {
        Ok(listener) => {
            drop(listener);
            Ok(())
        }
        Err(err) => Err(format_port_unavailable(JARVIS_PORT, &err.to_string())),
>>>>>>> theirs
    }
}

// ---------------------------------------------------------------------------
// Backend boot sequence (runs in background after app launch)
// ---------------------------------------------------------------------------

<<<<<<< ours
    // Phase 2: Pull one small model (qwen3.5:2b) so the app can open fast.
    // Skip in remote mode to avoid unwanted downloads.
    if !is_remote_ollama() {
        {
            let mut s = status.lock().await;
            s.phase = "model".into();
            s.detail = format!("Checking for {}...", STARTUP_MODEL);
        }
||||||| base
    // Phase 2: Pull one small model (qwen3.5:2b) so the app can open fast.
    // Remaining models are pulled in the background after the server starts.
    {
        let mut s = status.lock().await;
        s.phase = "model".into();
        s.detail = format!("Checking for {}...", STARTUP_MODEL);
    }
=======
async fn boot_backend(backend: SharedBackend, status: SharedStatus) {
    // Never infer consent from a missing or malformed config. A fresh desktop
    // install must persist an explicit source choice before this function can
    // launch Ollama, contact a custom endpoint, or download a model.
    let Some(mut cfg) = read_configured_inference_config() else {
        *status.lock().await = SetupStatus::default();
        return;
    };
    let mut pending_rollback = PendingInferenceRollback::new(&cfg);
    let plan = boot_plan(&cfg, total_ram_gb());
    {
        let mut s = status.lock().await;
        *s = SetupStatus::starting(&cfg);
        s.source = match cfg.kind {
            SourceKind::Ollama => "ollama",
            SourceKind::Custom => "custom",
        }
        .into();
    }
>>>>>>> theirs

<<<<<<< ours
        if !ollama_has_model(STARTUP_MODEL).await {
||||||| base
    if !ollama_has_model(STARTUP_MODEL).await {
=======
    // For the Ollama path, model resolution may fall back to FALLBACK_MODEL; we
    // record what is actually available here so the serve command below uses
    // it instead of the originally-planned tag. None on the custom path.
    let mut serve_model_override: Option<String> = None;

    if plan.launch_ollama {
        // Phase 1: Start Ollama
        {
            let mut s = status.lock().await;
            s.phase = "ollama".into();
            s.detail = "Starting inference engine...".into();
        }

        // Try the bundled sidecar first, fall back to system ollama
        let ollama_child = {
            let ollama_bin = resolve_bin("ollama");
            let mut sidecar_cmd = tokio::process::Command::new(&ollama_bin);
            sidecar_cmd
                .arg("serve")
                .env("OLLAMA_HOST", format!("127.0.0.1:{}", OLLAMA_PORT))
                .stdout(std::process::Stdio::null())
                .stderr(std::process::Stdio::null());
            // Avoid LD_LIBRARY_PATH leak when running inside an AppImage (#455).
            prepare_subprocess_for_appimage(&mut sidecar_cmd);
            match spawn_owned_child(&mut sidecar_cmd) {
                Ok(child) => Some(child),
                Err(_) => None,
            }
        };

        if let Some(child) = ollama_child {
            backend.lock().await.ollama = Some(ChildHandle { child });
        }

        let ollama_url = format!("http://127.0.0.1:{}/api/tags", OLLAMA_PORT);
        if !wait_for_url(&ollama_url, Duration::from_secs(30)).await {
            let mut s = status.lock().await;
            s.error = Some("Could not start Ollama. Install it from https://ollama.com".into());
            return;
        }

        {
            let mut s = status.lock().await;
            s.ollama_ready = true;
            s.detail = "Inference engine ready.".into();
        }

        // Phase 2: Resolve one model to serve. Prefer an installed model on
        // first run so startup does not depend on a download succeeding.
        let model = plan
            .model_to_pull
            .clone()
            .unwrap_or_else(|| STARTUP_MODEL.to_string());
>>>>>>> theirs
        {
            let mut s = status.lock().await;
            s.phase = "model".into();
            s.detail = format!("Checking for {}...", model);
        }

        let installed_models = ollama_model_names().await;
        let resolved_model = if let Some(installed) =
            startup_installed_model(&model, &installed_models)
        {
            installed
        } else {
            {
                let mut s = status.lock().await;
                s.detail = format!("Downloading {}... (this may take a minute)", model);
            }
            match pull_model(&model).await {
                Ok(()) => model.clone(),
                Err(e) => {
                    eprintln!("Warning: failed to pull {}: {}", model, e);

                    // If a local model appeared while pulling, use it instead of
                    // making startup depend on another network pull.
                    if let Some(installed) = preferred_installed_model(&ollama_model_names().await)
                    {
                        installed
                    } else if ollama_has_model(FALLBACK_MODEL).await {
                        FALLBACK_MODEL.to_string()
                    } else {
                        {
                            let mut s = status.lock().await;
                            s.detail = format!("Downloading {}...", FALLBACK_MODEL);
                        }
                        if let Err(e2) = pull_model(FALLBACK_MODEL).await {
                            if let Some(installed) =
                                preferred_installed_model(&ollama_model_names().await)
                            {
                                installed
                            } else {
                                let mut s = status.lock().await;
                                s.error = Some(format!("Failed to download model: {}", e2));
                                return;
                            }
                        } else {
                            FALLBACK_MODEL.to_string()
                        }
                    }
                }
            }
        };

        if resolved_model != model {
            let mut s = status.lock().await;
            s.detail = format!("Using installed model {}.", resolved_model);
        }

        serve_model_override = Some(resolved_model.clone());

        // Persist only first-run/default resolution. If the user explicitly
        // configured a model, do not overwrite that choice with a temporary
        // fallback selected just to keep startup nonfatal.
        if should_persist_resolved_model(&cfg) {
            let mut persisted = cfg.clone();
            persisted.model = Some(resolved_model);
            if write_inference_config(&persisted).is_ok() {
                cfg = persisted;
            }
        }

<<<<<<< ours
        {
            let mut s = status.lock().await;
            s.model_ready = true;
            s.detail = "Model ready.".into();
        }
    } else {
        // Remote mode - skip model checks
        let mut s = status.lock().await;
        s.model_ready = true;
        s.detail = "Using remote models.".into();
||||||| base
    {
        let mut s = status.lock().await;
        s.model_ready = true;
        s.detail = "Model ready.".into();
=======
        {
            let mut s = status.lock().await;
            s.model_ready = true;
            s.detail = "Model ready.".into();
        }
    } else {
        // Custom OpenAI-compatible endpoint: never start Ollama, never download.
        let host = plan
            .engine_host
            .as_ref()
            .map(|(_, v)| v.clone())
            .unwrap_or_default();
        {
            let mut s = status.lock().await;
            s.phase = "model".into();
            s.detail = format!("Connecting to {}...", host);
        }
        if host.is_empty() || !endpoint_reachable(&host, Duration::from_secs(15)).await {
            let mut s = status.lock().await;
            s.error = Some(format!(
                "Could not reach your custom inference server at {}. \
                 Start the server (e.g. LM Studio), or choose Change inference source below.",
                if host.is_empty() {
                    "(no URL set)"
                } else {
                    host.as_str()
                }
            ));
            return;
        }
        // Point `jarvis serve` at the user's endpoint by writing the engine
        // host into ~/.openjarvis/config.toml (the env var alone is shadowed by
        // the engine's non-empty default host in the Python layer).
        if let Some((engine, host)) = &plan.engine_host {
            if let Err(e) = set_engine_host_in_config(engine, host) {
                let mut s = status.lock().await;
                s.error = Some(format!("Could not write engine config: {}", e));
                return;
            }
        }
        {
            let mut s = status.lock().await;
            s.ollama_ready = true;
            s.model_ready = true;
            s.detail = "Connected to custom endpoint.".into();
        }
>>>>>>> theirs
    }

    // Phase 3: Start jarvis serve
    {
        let mut s = status.lock().await;
        s.phase = "server".into();
        s.detail = "Starting API server...".into();
    }

    let uv_bin = resolve_bin("uv");

    // Verify uv is actually installed. Concrete per-OS instructions â€”
    // the generic "install it from astral.sh" was the #1 source of
    // confusion on the Discord support thread; users couldn't tell whether
    // to use winget, scoop, pip, or the official installer.
    if !std::path::Path::new(&uv_bin).exists() && uv_bin == "uv" {
        let mut s = status.lock().await;
        #[cfg(target_os = "windows")]
        let msg = "Could not find 'uv' (Python package manager). \
                   To install on Windows, open PowerShell and run:\n\n\
                   powershell -ExecutionPolicy Bypass -c \"irm https://astral.sh/uv/install.ps1 | iex\"\n\n\
                   Then close and relaunch this app. \
                   (If the install completes but the app still can't find uv, \
                   you may need to log out and back in so PATH refreshes.)";
        #[cfg(target_os = "macos")]
        let msg = "Could not find 'uv' (Python package manager). \
                   To install on macOS, open Terminal and run:\n\n\
                   curl -LsSf https://astral.sh/uv/install.sh | sh\n\n\
                   Then relaunch this app.";
        #[cfg(target_os = "linux")]
        let msg = "Could not find 'uv' (Python package manager). \
                   To install on Linux, open a terminal and run:\n\n\
                   curl -LsSf https://astral.sh/uv/install.sh | sh\n\n\
                   Then relaunch this app.";
        #[cfg(not(any(target_os = "windows", target_os = "macos", target_os = "linux")))]
        let msg = "Could not find 'uv' (Python package manager). \
                   Install it from https://astral.sh/uv then relaunch.";
        s.error = Some(msg.into());
        return;
    }

    let mut project_root = find_project_root();

    if project_root.is_none() {
        // Auto-clone on first launch
        let git_bin = resolve_bin("git");

        // Check that git is installed
        if !std::path::Path::new(&git_bin).exists() && git_bin == "git" {
            let mut s = status.lock().await;
            s.error = Some(
                "Could not find 'git'. \
                 Install it from https://git-scm.com then relaunch."
                    .into(),
            );
            return;
        }

    let target_path = std::path::PathBuf::from(home_dir()).join("OpenJarvis");
    let clone_target = target_path.display().to_string();

    /* 
    // ONE-CLICK CONSUMER DEPLOY PATCH - DISABLED LOCAL DOWNLOAD LOOP
    if target_path.exists() && !target_path.join("pyproject.toml").exists() {
        let mut s = status.lock().await;
        s.error = Some(format!(
            "{} exists but is not a valid OpenJarvis project. \
            Remove it and relaunch, or set OPENJARVIS_ROOT to the correct path.",
            clone_target,
        ));
        return;
    }
    {
        let mut s = status.lock().await;
        s.detail = "Downloading OpenJarvis (first launch)...".into();
    }
    let clone_result = tokio::process::Command::new(&git_bin)
        .args([
            "clone",
            "--depth",
            "1",
            "https://github.com/open-jarvis/OpenJarvis.git",
            &clone_target,
        ])
        .stdout(std::process::Stdio::null())
        .stderr(std::process::Stdio::piped())
        .spawn();

<<<<<<< ours
    match clone_result {
        Ok(child) => match child.wait_with_output().await {
            Ok(output) if output.status.success() => {
                project_root = Some(target_path);
            }
            Ok(output) => {
                let stderr = String::from_utf8_lossy(&output.stderr);
                let mut s = status.lock().await;
                s.error = Some(format!(
                    "Failed to download OpenJarvis: {}. \
                    Clone manually: git clone https://github.com/open-jarvis/OpenJarvis.git {}",
                    stderr.trim(),
                    clone_target,
                ));
                return;
            }
||||||| base
        let clone_result = tokio::process::Command::new(&git_bin)
            .args([
                "clone",
                "--depth",
                "1",
                "https://github.com/open-jarvis/OpenJarvis.git",
                &clone_target,
            ])
            .stdout(std::process::Stdio::null())
            .stderr(std::process::Stdio::piped())
            .spawn();

        match clone_result {
            Ok(child) => match child.wait_with_output().await {
                Ok(output) if output.status.success() => {
                    project_root = Some(target_path);
                }
                Ok(output) => {
                    let stderr = String::from_utf8_lossy(&output.stderr);
                    let mut s = status.lock().await;
                    s.error = Some(format!(
                        "Failed to download OpenJarvis: {}. \
                         Clone manually: git clone https://github.com/open-jarvis/OpenJarvis.git {}",
                        stderr.trim(),
                        clone_target,
                    ));
                    return;
                }
                Err(e) => {
                    let mut s = status.lock().await;
                    s.error = Some(format!(
                        "Failed to download OpenJarvis: {}. \
                         Clone manually: git clone https://github.com/open-jarvis/OpenJarvis.git {}",
                        e, clone_target,
                    ));
                    return;
                }
            },
=======
        let mut clone_cmd = tokio::process::Command::new(&git_bin);
        clone_cmd
            .args([
                "clone",
                "--depth",
                "1",
                "https://github.com/open-jarvis/OpenJarvis.git",
                &clone_target,
            ])
            .stdout(std::process::Stdio::null())
            .stderr(std::process::Stdio::piped());
        prepare_subprocess_for_appimage(&mut clone_cmd);
        let clone_result = spawn_owned_child(&mut clone_cmd);

        match clone_result {
            Ok(child) => match child.wait_with_output().await {
                Ok(output) if output.status.success() => {
                    project_root = Some(target_path);
                }
                Ok(output) => {
                    let stderr = String::from_utf8_lossy(&output.stderr);
                    let mut s = status.lock().await;
                    s.error = Some(format!(
                        "Failed to download OpenJarvis: {}. \
                         Clone manually: git clone https://github.com/open-jarvis/OpenJarvis.git {}",
                        stderr.trim(),
                        clone_target,
                    ));
                    return;
                }
                Err(e) => {
                    let mut s = status.lock().await;
                    s.error = Some(format!(
                        "Failed to download OpenJarvis: {}. \
                         Clone manually: git clone https://github.com/open-jarvis/OpenJarvis.git {}",
                        e, clone_target,
                    ));
                    return;
                }
            },
>>>>>>> theirs
            Err(e) => {
                let mut s = status.lock().await;
                s.error = Some(format!(
                    "Failed to download OpenJarvis: {}. \
                    Clone manually: git clone https://github.com/open-jarvis/OpenJarvis.git {}",
                    e,
                    clone_target,
                ));
                return;
            }
        },
        Err(e) => {
            let mut s = status.lock().await;
            s.error = Some(format!(
                "Could not run git: {}. \
                Install git from https://git-scm.com then relaunch.",
                e,
            ));
            return;
        }
    }
    */

    // Manually route project root to your populated directory space
    project_root = Some(target_path);
    }

    // If something is already serving on our port, decide what to do based
    // on what it actually responds with â€” don't blindly kill it (#455).
    //
    // The OLD behaviour was: any HTTP response (even 404) â†’ `fuser -k 8000/tcp`
    // / `taskkill /PID /F`. That broke the legitimate case where a user had
    // already started `jarvis serve` in a terminal and then launched the
    // desktop app â€” the app killed their server, then raced to spawn its
    // own, sometimes losing the race and hanging.
    //
    // New behaviour, by response shape:
    //   * 2xx /health        â€” healthy jarvis serve. Attach to it; skip the
    //                          uv-sync + spawn dance entirely. Done.
    //   * 503                â€” server is up but engine isn't ready. Surface
    //                          an actionable message; don't kill (matches
    //                          our wait_for_jarvis_health 503 contract).
    //   * any other status   â€” something else is listening on the port. Tell
    //                          the user via the error banner instead of
    //                          force-killing a foreign service.
    //   * Err (conn refused) â€” nothing is listening. Proceed to spawn.
    //
    // TODO(#455 follow-up): validate /health response body before attaching
    // so a multi-user host can't trivially spoof us. Also accept a port
    // override from config instead of hard-coding JARVIS_PORT.
    {
        let client = reqwest::Client::builder()
            .timeout(Duration::from_secs(2))
            .build()
            .unwrap();
        match client
            .get(format!("http://127.0.0.1:{}/health", JARVIS_PORT))
            .send()
            .await
        {
<<<<<<< ours
            #[cfg(unix)]
            {
                let _ = tokio::process::Command::new("fuser")
                    .args(["-k", &format!("{}/tcp", JARVIS_PORT)])
                    .output()
                    .await;
                tokio::time::sleep(Duration::from_secs(2)).await;
            }
            #[cfg(target_os = "windows")]
            {
                if let Ok(output) = tokio::process::Command::new("cmd")
                    .args(["/C", &format!(
                        "for /f \"tokens=5\" %a in ('netstat -ano ^| findstr :{port} ^| findstr LISTENING') do taskkill /PID %a /F",
                        port = JARVIS_PORT,
                    )])
                    .output()
||||||| base
            // Something is already listening â€” try to kill it
            #[cfg(unix)]
            {
                let _ = tokio::process::Command::new("fuser")
                    .args(["-k", &format!("{}/tcp", JARVIS_PORT)])
                    .output()
                    .await;
                tokio::time::sleep(Duration::from_secs(2)).await;
            }
            #[cfg(target_os = "windows")]
            {
                // Find the PID holding the port via netstat, then kill it
                if let Ok(output) = tokio::process::Command::new("cmd")
                    .args(["/C", &format!(
                        "for /f \"tokens=5\" %a in ('netstat -ano ^| findstr :{port} ^| findstr LISTENING') do taskkill /PID %a /F",
                        port = JARVIS_PORT,
                    )])
                    .output()
=======
            Ok(resp) if resp.status().is_success() => {
                // Confirm with a second probe â€” the first might have caught
                // a flickering server (engine half-loaded, dying mid-stop,
                // etc.) and we don't want to claim ready off a 2-second
                // snapshot. Small sleep between to give the server room.
                tokio::time::sleep(Duration::from_millis(500)).await;
                let confirm = client
                    .get(format!("http://127.0.0.1:{}/health", JARVIS_PORT))
                    .send()
>>>>>>> theirs
                    .await
<<<<<<< ours
                {
                    let _ = output;
||||||| base
                {
                    let _ = output; // best-effort
=======
                    .map(|r| r.status().is_success())
                    .unwrap_or(false);
                if !confirm {
                    // First probe was 2xx but the second wasn't â€” fall
                    // through to the spawn path. The server probably went
                    // away between probes.
                    // (No early return â€” we want to spawn our own.)
                } else {
                    // A newly staged key may only enter a child process that
                    // this desktop instance launched. A listener that merely
                    // answers /health could be a port squatter; never POST or
                    // otherwise disclose the pending secret to it.
                    match pending_rollback.staged_credential_present() {
                        Ok(true) => {
                            let mut s = status.lock().await;
                            s.error = Some(format!(
                                "An API server is already running on port {}, but OpenJarvis cannot securely apply your new inference API key to a server it did not start. Stop that server, then try setup again.",
                                JARVIS_PORT,
                            ));
                            return;
                        }
                        Err(err) => {
                            let mut s = status.lock().await;
                            s.error = Some(format!(
                                "Could not verify the staged inference API key: {}",
                                err
                            ));
                            return;
                        }
                        Ok(false) => {}
                    }
                    // Attach to the existing healthy server. Mark every
                    // pre-spawn step done so the setup UI doesn't show a
                    // half-progress bar (model_ready / ollama_ready stay
                    // false otherwise because we skipped those steps).
                    if let Err(err) = pending_rollback.confirm(&mut cfg) {
                        let mut s = status.lock().await;
                        s.error = Some(format!("Could not confirm inference setup: {}", err));
                        return;
                    }
                    let mut s = status.lock().await;
                    s.phase = "ready".into();
                    s.detail =
                        format!("Connected to existing API server on port {}.", JARVIS_PORT,);
                    s.server_ready = true;
                    s.model_ready = true;
                    s.ollama_ready = true;
                    return;
>>>>>>> theirs
                }
            }
            Ok(resp) if resp.status() == reqwest::StatusCode::SERVICE_UNAVAILABLE => {
                let mut s = status.lock().await;
                s.error = Some(format!(
                    "An API server is already running on port {} but its \
                     inference engine isn't ready (HTTP 503). If this is your \
                     `jarvis serve`, wait for it to finish loading and relaunch. \
                     Otherwise, stop that service or change the port.",
                    JARVIS_PORT,
                ));
                return;
            }
            Ok(resp) => {
                // Something else (a different web server, a stale process,
                // a 4xx-returning instance) is on our port. Don't kill it â€”
                // give the user actionable info instead.
                let mut s = status.lock().await;
                s.error = Some(format!(
                    "Port {} is already in use by another service (it answered \
                     /health with HTTP {}). Stop that service or change the \
                     OpenJarvis port, then relaunch.\n\nTo identify it:\n  {}",
                    JARVIS_PORT,
                    resp.status(),
                    port_owner_hint(),
                ));
                return;
            }
            Err(_) => {
                // Nothing listening â€” proceed to the normal spawn path.
            }
        }
    }
<<<<<<< ours
    // Use configured model in remote mode, otherwise auto-detect
    let startup_model = if is_remote_ollama() {
        STARTUP_MODEL
    } else {
        let pref = preferred_model();
        if ollama_has_model(pref).await {
            pref
        } else if ollama_has_model(STARTUP_MODEL).await {
            STARTUP_MODEL
        } else {
            FALLBACK_MODEL
        }
    };
||||||| base

    // Start with STARTUP_MODEL (just pulled) or preferred if already available.
    let pref = preferred_model();
    let startup_model = if ollama_has_model(pref).await {
        pref
    } else if ollama_has_model(STARTUP_MODEL).await {
        STARTUP_MODEL
    } else {
        FALLBACK_MODEL
    };
=======

    if let Err(err) = check_jarvis_port_available() {
        let mut s = status.lock().await;
        s.error = Some(err);
        return;
    }
>>>>>>> theirs

    let root = project_root.as_ref().unwrap();

    let cargo_bin = resolve_bin("cargo");
    if !std::path::Path::new(&cargo_bin).exists() && cargo_bin == "cargo" {
        let mut s = status.lock().await;
        s.error = Some(format_missing_rust_toolchain());
        return;
    }

    // Install dependencies automatically (handles fresh clones).
    //
    // Previously we ran `uv sync` with both stdout AND stderr piped to
    // /dev/null and discarded the exit code (`let _ = â€¦`). When `uv sync`
    // failed â€” Windows path issues, network problems, lockfile conflicts â€”
    // the user saw no error, the boot continued, `uv run jarvis serve`
    // then ran in an under-provisioned venv, and the user waited the full
    // 600s health-check window before getting "Jarvis server did not
    // become healthy in time" with no actionable detail (issue #331).
    //
    // Now: capture stderr, check the exit status, surface a useful error
    // to the user BEFORE the long server-start wait. The status detail
    // message also indicates this can take a couple of minutes on first
    // boot so users don't restart the app thinking it's stuck.
    {
        let mut s = status.lock().await;
        s.detail = "Installing dependencies (uv sync â€” may take 1-2 min on first boot)...".into();
    }
    let mut sync_cmd = tokio::process::Command::new(&uv_bin);
    sync_cmd
        .args([
            "sync",
            "--extra",
            "desktop",
            "--extra",
            "inference-cloud",
            "--extra",
            "inference-google",
            // openjarvis_rust lives in a uv dependency group (not the published
            // `desktop` extra) so pip installs from PyPI don't require it (#584).
            "--group",
            "desktop-native",
        ])
        .stdout(std::process::Stdio::null())
        .stderr(std::process::Stdio::piped())
        .current_dir(root);
    // Avoid LD_LIBRARY_PATH leak when running inside an AppImage (#455).
    prepare_subprocess_for_appimage(&mut sync_cmd);
    add_cargo_bin_to_path(&mut sync_cmd);
    sync_cmd.kill_on_drop(true);
    let sync_output = sync_cmd.output().await;
    match sync_output {
        Ok(out) if !out.status.success() => {
            let stderr = String::from_utf8_lossy(&out.stderr);
            let mut s = status.lock().await;
            s.error = Some(format_uv_sync_failure(root, out.status.code(), &stderr));
            return;
        }
        Err(e) => {
            let mut s = status.lock().await;
            s.error = Some(format_uv_sync_spawn_error(root, &uv_bin, &e.to_string()));
            return;
        }
        Ok(_) => {} // success â€” fall through
    }

    {
        let mut s = status.lock().await;
        s.detail = "Verifying Rust extension (openjarvis_rust)...".into();
    }
    if let Err(err) = verify_openjarvis_rust_extension(root, &uv_bin).await {
        let mut s = status.lock().await;
        s.error = Some(err);
        return;
    }

    {
        let mut s = status.lock().await;
        s.detail = format!("Starting API server from {}...", root.display());
    }

    let mut cmd = tokio::process::Command::new(&uv_bin);
    let mut serve_argv: Vec<String> = vec![
        "run".into(),
        "jarvis".into(),
        "serve".into(),
        "--port".into(),
        JARVIS_PORT.to_string(),
    ];
    serve_argv.extend(plan.serve_args.iter().cloned());
    // If the Ollama pull fell back to a different tag than planned, serve the
    // tag that is actually present. boot_plan always emits `--model` followed
    // immediately by its value, so `i + 1` is in bounds.
    if let Some(m) = &serve_model_override {
        match serve_argv.iter().position(|a| a == "--model") {
            Some(i) if i + 1 < serve_argv.len() => serve_argv[i + 1] = m.clone(),
            _ => eprintln!(
                "Warning: resolved model {:?} could not be applied; \
                 '--model <value>' not found in serve args {:?}",
                m, serve_argv
            ),
        }
    }
    cmd.args(&serve_argv)
        .stdout(std::process::Stdio::null())
        .stderr(std::process::Stdio::piped())
        .current_dir(root);
    // Avoid LD_LIBRARY_PATH leak when running inside an AppImage (#455) â€”
    // do this BEFORE cmd.env() calls below so our explicit cloud-key env
    // additions aren't accidentally stripped.
    prepare_subprocess_for_appimage(&mut cmd);

    // Inject cloud API keys from secure desktop storage.
    for (key, value) in cloud_keys_for_inference(&cfg) {
        cmd.env(&key, &value);
    }
    let jarvis_child = spawn_owned_child(&mut cmd);

    match jarvis_child {
        Ok(mut child) => {
            // Start draining stderr immediately. If we wait until the
            // health check returns we risk filling the 4 KB Windows pipe
            // buffer during startup logging and hanging the child before
            // it can bind its HTTP port â€” exactly the symptom in #309.
            let stderr_handle = child.stderr.take();
            let mut mgr = backend.lock().await;
            let tail = mgr.jarvis_stderr_tail.clone();
            mgr.jarvis = Some(ChildHandle { child });
            drop(mgr);
            if let Some(stderr) = stderr_handle {
                spawn_jarvis_stderr_drainer(stderr, tail);
            }
        }
        Err(e) => {
            let mut s = status.lock().await;
            s.error = Some(format!(
                "Could not start jarvis server: {}. \
                 Make sure uv is installed (https://astral.sh/uv) and the OpenJarvis repo is cloned at {}",
                e,
                root.display(),
            ));
            return;
        }
    }

    let server_url = format!("http://127.0.0.1:{}/health", JARVIS_PORT);
    match wait_for_jarvis_health(&server_url, Duration::from_secs(600), &backend).await {
        JarvisStartResult::Ready => {}
        JarvisStartResult::ServiceUnavailable(body) => {
            let mut s = status.lock().await;
            s.error = Some(format!(
                "Jarvis server is running but the inference engine is not available \
                 (HTTP 503). This usually means the configured model couldn't be loaded.\n\n\
                 Check the server logs, or run 'uv run jarvis serve --port {}{}' \
                 from {} to see the engine error.\n\n\
                 Server response:\n{}",
                JARVIS_PORT,
                // Show the args actually passed (after `serve --port <port>`),
                // including any post-fallback `--model` override.
                match serve_argv.get(5..) {
                    Some(rest) if !rest.is_empty() => format!(" {}", rest.join(" ")),
                    _ => String::new(),
                },
                root.display(),
                body.trim(),
            ));
            return;
        }
        JarvisStartResult::EarlyExit { code, stderr } => {
            // `None` here means the OS didn't expose an exit code â€” on
            // Unix that's a signal kill (SIGKILL/SIGSEGV/...), on Windows
            // it means the process was terminated externally (Task
            // Manager, parent-of-parent, AV). "unknown" covers both.
            let code_str = code
                .map(|c| c.to_string())
                .unwrap_or_else(|| "unknown".into());
            let mut s = status.lock().await;
            s.error = Some(if stderr.is_empty() {
                format!(
                    "Jarvis server exited (code {}) before becoming ready.\n\n\
                     No stderr output. Check that:\n\
                     1. uv is installed ({})\n\
                     2. The OpenJarvis repo is at {}\n\
                     3. 'uv sync' completes in that directory",
                    code_str,
                    uv_bin,
                    root.display(),
                )
            } else {
                format!(
                    "Jarvis server exited (code {}) before becoming ready.\n\nStderr:\n{}",
                    code_str, stderr,
                )
            });
            return;
        }
        JarvisStartResult::Timeout => {
            let stderr = read_jarvis_stderr_tail(&backend).await;
            let mut s = status.lock().await;
            s.error = Some(if stderr.is_empty() {
                format!(
                    "Jarvis server did not become ready within 10 minutes. Check that:\n\
                     1. uv is installed ({})\n\
                     2. The OpenJarvis repo is at {}\n\
                     3. Run 'uv sync' in that directory",
                    uv_bin,
                    root.display(),
                )
            } else {
                format!(
                    "Jarvis server did not become ready within 10 minutes.\n\nStderr:\n{}",
                    stderr,
                )
            });
            return;
        }
    }

    if let Err(err) = pending_rollback.confirm(&mut cfg) {
        let mut s = status.lock().await;
        s.error = Some(format!("Could not confirm inference setup: {}", err));
        return;
    }

    {
        let mut s = status.lock().await;
        s.server_ready = true;
        s.phase = "ready".into();
        s.detail = "All systems ready.".into();
    }

    // Phase 4: done. We intentionally do NOT auto-pull the rest of the
    // Qwen3.5 ladder here. The previous behavior walked every model that
    // "fit" in RAM (up to qwen3.5:122b â‰ˆ 81 GB) and pulled each one in an
    // un-cancellable background task â€” so the app silently consumed tens of
    // gigabytes with no way to stop short of deleting it. The startup model
    // pulled in Phase 2 is enough to make the app fully usable; additional
    // models are now opt-in (Settings â†’ "ollama pull <model>", or the
    // `pull_model` command invoked from the UI).
}

// ---------------------------------------------------------------------------
// Tauri commands
// ---------------------------------------------------------------------------

fn api_base() -> String {
    std::env::var("OPENJARVIS_API_URL")
        .unwrap_or_else(|_| format!("http://127.0.0.1:{}", JARVIS_PORT))
}

#[tauri::command]
async fn get_setup_status(state: tauri::State<'_, SharedStatus>) -> Result<SetupStatus, String> {
    Ok(state.lock().await.clone())
}

#[tauri::command]
fn get_api_base() -> String {
    api_base()
}

#[tauri::command]
async fn start_backend(
    backend: tauri::State<'_, SharedBackend>,
    status: tauri::State<'_, SharedStatus>,
) -> Result<(), String> {
    if read_configured_inference_config().is_none() {
        *status.lock().await = SetupStatus::default();
        return Err("Choose an inference source before starting OpenJarvis.".into());
    }
    let b = backend.inner().clone();
    let s = status.inner().clone();
    start_managed_boot(b, s).await;
    Ok(())
}

#[tauri::command]
async fn stop_backend(backend: tauri::State<'_, SharedBackend>) -> Result<(), String> {
    backend.lock().await.stop_all().await;
    Ok(())
}

/// Abort startup, stop every child, discard an unworkable source, and return
/// the UI to the inert chooser. This is the recovery path for setup failures.
#[tauri::command]
async fn reset_inference_source(
    backend: tauri::State<'_, SharedBackend>,
    status: tauri::State<'_, SharedStatus>,
) -> Result<(), String> {
    backend.lock().await.stop_all().await;
    discard_pending_inference_setup()?;
    *status.lock().await = SetupStatus::default();
    Ok(())
}

#[tauri::command]
async fn check_health(api_url: String) -> Result<serde_json::Value, String> {
    let url = format!(
        "{}/health",
        if api_url.is_empty() {
            api_base()
        } else {
            api_url
        }
    );
    let resp = reqwest::get(&url)
        .await
        .map_err(|e| format!("Connection failed: {}", e))?;
    resp.json()
        .await
        .map_err(|e| format!("Invalid response: {}", e))
}

#[tauri::command]
async fn fetch_energy(api_url: String) -> Result<serde_json::Value, String> {
    let base = if api_url.is_empty() {
        api_base()
    } else {
        api_url
    };
    let resp = reqwest::get(format!("{}/v1/telemetry/energy", base))
        .await
        .map_err(|e| format!("Connection failed: {}", e))?;
    resp.json()
        .await
        .map_err(|e| format!("Invalid response: {}", e))
}

#[tauri::command]
async fn fetch_telemetry(api_url: String) -> Result<serde_json::Value, String> {
    let base = if api_url.is_empty() {
        api_base()
    } else {
        api_url
    };
    let resp = reqwest::get(format!("{}/v1/telemetry/stats", base))
        .await
        .map_err(|e| format!("Connection failed: {}", e))?;
    resp.json()
        .await
        .map_err(|e| format!("Invalid response: {}", e))
}

#[tauri::command]
async fn fetch_traces(api_url: String, limit: u32) -> Result<serde_json::Value, String> {
    let base = if api_url.is_empty() {
        api_base()
    } else {
        api_url
    };
    let resp = reqwest::get(format!("{}/v1/traces?limit={}", base, limit))
        .await
        .map_err(|e| format!("Connection failed: {}", e))?;
    resp.json()
        .await
        .map_err(|e| format!("Invalid response: {}", e))
}

#[tauri::command]
async fn fetch_trace(api_url: String, trace_id: String) -> Result<serde_json::Value, String> {
    let base = if api_url.is_empty() {
        api_base()
    } else {
        api_url
    };
    let resp = reqwest::get(format!("{}/v1/traces/{}", base, trace_id))
        .await
        .map_err(|e| format!("Connection failed: {}", e))?;
    resp.json()
        .await
        .map_err(|e| format!("Invalid response: {}", e))
}

#[tauri::command]
async fn fetch_learning_stats(api_url: String) -> Result<serde_json::Value, String> {
    let base = if api_url.is_empty() {
        api_base()
    } else {
        api_url
    };
    let resp = reqwest::get(format!("{}/v1/learning/stats", base))
        .await
        .map_err(|e| format!("Connection failed: {}", e))?;
    resp.json()
        .await
        .map_err(|e| format!("Invalid response: {}", e))
}

#[tauri::command]
async fn fetch_learning_policy(api_url: String) -> Result<serde_json::Value, String> {
    let base = if api_url.is_empty() {
        api_base()
    } else {
        api_url
    };
    let resp = reqwest::get(format!("{}/v1/learning/policy", base))
        .await
        .map_err(|e| format!("Connection failed: {}", e))?;
    resp.json()
        .await
        .map_err(|e| format!("Invalid response: {}", e))
}

#[tauri::command]
async fn fetch_memory_stats(api_url: String) -> Result<serde_json::Value, String> {
    let base = if api_url.is_empty() {
        api_base()
    } else {
        api_url
    };
    let resp = reqwest::get(format!("{}/v1/memory/stats", base))
        .await
        .map_err(|e| format!("Connection failed: {}", e))?;
    resp.json()
        .await
        .map_err(|e| format!("Invalid response: {}", e))
}

#[tauri::command]
async fn search_memory(
    api_url: String,
    query: String,
    top_k: u32,
) -> Result<serde_json::Value, String> {
    let base = if api_url.is_empty() {
        api_base()
    } else {
        api_url
    };
    let client = reqwest::Client::new();
    let resp = client
        .post(format!("{}/v1/memory/search", base))
        .json(&serde_json::json!({"query": query, "top_k": top_k}))
        .send()
        .await
        .map_err(|e| format!("Connection failed: {}", e))?;
    resp.json()
        .await
        .map_err(|e| format!("Invalid response: {}", e))
}

#[tauri::command]
async fn fetch_agents(api_url: String) -> Result<serde_json::Value, String> {
    let base = if api_url.is_empty() {
        api_base()
    } else {
        api_url
    };
    let resp = reqwest::get(format!("{}/v1/agents", base))
        .await
        .map_err(|e| format!("Connection failed: {}", e))?;
    resp.json()
        .await
        .map_err(|e| format!("Invalid response: {}", e))
}

#[tauri::command]
async fn fetch_models(api_url: String) -> Result<serde_json::Value, String> {
    let base = if api_url.is_empty() {
        api_base()
    } else {
        api_url
    };
    let resp = reqwest::get(format!("{}/v1/models", base))
        .await
        .map_err(|e| format!("Connection failed: {}", e))?;
    resp.json()
        .await
        .map_err(|e| format!("Invalid response: {}", e))
}

#[tauri::command]
async fn run_jarvis_command(args: Vec<String>) -> Result<String, String> {
    let uv_bin = resolve_bin("uv");

    let mut cmd_args = vec!["run".to_string(), "jarvis".to_string()];
    cmd_args.extend(args.iter().cloned());

    let mut cmd = tokio::process::Command::new(&uv_bin);
    cmd.args(&cmd_args);
    // Run from the project root so `uv run jarvis` resolves the OpenJarvis
    // project regardless of the app's launch cwd. In a packaged install the
    // cwd isn't the checkout, so without this `jarvis` isn't found and the
    // backend never starts â€” the UI then shows "Failed to get response"
    // (see #531).
    if let Some(ref root) = find_project_root() {
        cmd.current_dir(root);
    }

    let is_serve = args.first().map(|a| a.as_str() == "serve").unwrap_or(false);

    if !is_serve {
        // Short-lived command (e.g. `stop`, `status`): wait for it and return
        // its captured output.
        let output = cmd
            .output()
            .await
            .map_err(|e| format!("Failed to launch jarvis: {}", e))?;
        return if output.status.success() {
            Ok(String::from_utf8_lossy(&output.stdout).to_string())
        } else {
            Err(String::from_utf8_lossy(&output.stderr).to_string())
        };
    }

    // `jarvis serve` is a long-running server that never exits. The old code
    // used `.output()`, which waits for the process to exit and so hung this
    // command forever â€” the "Start" button never resolved (#531). Spawn it
    // detached instead, drain stderr (a full 4 KB Windows pipe can otherwise
    // stall the child mid-startup, #309), and poll /health for readiness.
    cmd.stdout(std::process::Stdio::null())
        .stderr(std::process::Stdio::piped());
    let mut child = cmd
        .spawn()
        .map_err(|e| format!("Failed to launch jarvis serve: {}", e))?;

    let tail: StderrTail = Arc::new(Mutex::new(Vec::new()));
    if let Some(stderr) = child.stderr.take() {
        spawn_jarvis_stderr_drainer(stderr, tail.clone());
    }

    let client = reqwest::Client::builder()
        .timeout(Duration::from_secs(2))
        .build()
        .map_err(|e| format!("Failed to build HTTP client: {}", e))?;
    let url = format!("http://127.0.0.1:{}/health", JARVIS_PORT);
    let deadline = tokio::time::Instant::now() + Duration::from_secs(120);

    loop {
        // Surface an early crash (bad venv, missing Rust ext, etc.) right away
        // instead of waiting out the full readiness timeout.
        if let Ok(Some(status)) = child.try_wait() {
            let stderr = String::from_utf8_lossy(tail.lock().await.as_slice()).into_owned();
            return Err(format!(
                "jarvis serve exited (code {:?}) before becoming healthy:\n{}",
                status.code(),
                stderr.trim()
            ));
        }
        if let Ok(resp) = client.get(&url).send().await {
            if resp.status().is_success() {
                // Leave the server running (the Child is detached on drop â€”
                // kill_on_drop defaults to false); `stop` tears it down.
                return Ok(format!(
                    "jarvis serve is ready on http://127.0.0.1:{}",
                    JARVIS_PORT
                ));
            }
        }
        if tokio::time::Instant::now() >= deadline {
            return Err(format!(
                "jarvis serve did not become healthy on port {} within 120s.",
                JARVIS_PORT
            ));
        }
        tokio::time::sleep(Duration::from_millis(500)).await;
    }
}

#[tauri::command]
async fn fetch_savings(api_url: String) -> Result<serde_json::Value, String> {
    let base = if api_url.is_empty() {
        api_base()
    } else {
        api_url
    };
    let resp = reqwest::get(format!("{}/v1/savings", base))
        .await
        .map_err(|e| format!("Connection failed: {}", e))?;
    resp.json()
        .await
        .map_err(|e| format!("Invalid response: {}", e))
}

/// Transcribe audio via the speech API endpoint.
#[tauri::command]
async fn transcribe_audio(
    api_url: String,
    audio_data: Vec<u8>,
    filename: String,
) -> Result<serde_json::Value, String> {
    let url = format!("{}/v1/speech/transcribe", api_url);
    let client = reqwest::Client::new();

    let part = reqwest::multipart::Part::bytes(audio_data)
        .file_name(filename)
        .mime_str("audio/webm")
        .map_err(|e| format!("Failed to create multipart: {}", e))?;

    let form = reqwest::multipart::Form::new().part("file", part);

    let resp = client
        .post(&url)
        .multipart(form)
        .send()
        .await
        .map_err(|e| format!("Connection failed: {}", e))?;
    let status = resp.status();
    let body = resp
        .text()
        .await
        .map_err(|e| format!("Invalid response: {}", e))?;
    if !status.is_success() {
        let detail = serde_json::from_str::<serde_json::Value>(&body)
            .ok()
            .and_then(|value| {
                value
                    .get("detail")
                    .and_then(|detail| detail.as_str())
                    .map(str::to_string)
            })
            .filter(|detail| !detail.is_empty())
            .unwrap_or(body);
        return Err(format!(
            "Transcription failed ({}): {}",
            status.as_u16(),
            detail
        ));
    }
    serde_json::from_str(&body).map_err(|e| format!("Invalid response: {}", e))
}

/// Submit savings to Supabase leaderboard.
#[tauri::command]
async fn submit_savings(
    supabase_url: String,
    supabase_key: String,
    payload: serde_json::Value,
) -> Result<bool, String> {
    if supabase_url.is_empty() || supabase_key.is_empty() {
        return Ok(false);
    }
    let client = reqwest::Client::new();
    let resp = client
        .post(format!(
            "{}/rest/v1/savings_entries?on_conflict=anon_id",
            supabase_url
        ))
        .header("Content-Type", "application/json")
        .header("apikey", &supabase_key)
        .header("Authorization", format!("Bearer {}", supabase_key))
        .header("Prefer", "resolution=merge-duplicates")
        .json(&payload)
        .send()
        .await
        .map_err(|e| format!("Supabase POST failed: {}", e))?;
    Ok(resp.status().is_success())
}

// ---------------------------------------------------------------------------
// Cloud API key management
// ---------------------------------------------------------------------------

const SECURE_KEY_SERVICE: &str = "OpenJarvis Cloud Keys";
// A first-run custom credential is kept in its own secure-storage slot until
// the managed backend has passed every readiness gate.  In particular, do not
// overwrite an existing <ENGINE>_API_KEY while setup can still be cancelled.
const PENDING_INFERENCE_API_KEY: &str = "OPENJARVIS_PENDING_INFERENCE_API_KEY";
const MANAGED_CLOUD_KEY_NAMES: &[&str] = &[
    "OPENAI_API_KEY",
    "ANTHROPIC_API_KEY",
    "GEMINI_API_KEY",
    "GOOGLE_API_KEY",
    "OPENROUTER_API_KEY",
    "MINIMAX_API_KEY",
    "TAVILY_API_KEY",
];

/// Legacy path used by older desktop builds. New saves never write here.
fn legacy_cloud_keys_path() -> std::path::PathBuf {
    let home = home_dir();
    std::path::PathBuf::from(home)
        .join(".openjarvis")
        .join("cloud-keys.env")
}

fn validate_cloud_key_name(key_name: &str) -> Result<(), String> {
    let valid = !key_name.is_empty()
        && key_name.len() <= 128
        && key_name.ends_with("_API_KEY")
        && key_name
            .chars()
            .all(|ch| ch.is_ascii_uppercase() || ch.is_ascii_digit() || ch == '_');
    if valid {
        Ok(())
    } else {
        Err(format!("Invalid API key name: {}", key_name))
    }
}

fn engine_api_key_name(engine: &str) -> String {
    let normalized: String = engine
        .chars()
        .map(|ch| {
            if ch.is_ascii_alphanumeric() {
                ch.to_ascii_uppercase()
            } else {
                '_'
            }
        })
        .collect();
    let trimmed = normalized.trim_matches('_');
    let engine_name = if trimmed.is_empty() {
        CUSTOM_FALLBACK_ENGINE.to_ascii_uppercase()
    } else {
        trimmed.to_string()
    };
    format!("{}_API_KEY", engine_name)
}

fn managed_cloud_key_names() -> Vec<String> {
    let mut names: Vec<String> = MANAGED_CLOUD_KEY_NAMES
        .iter()
        .map(|name| (*name).to_string())
        .collect();

    let cfg = read_inference_config();
    if matches!(&cfg.kind, SourceKind::Custom) {
        let engine = cfg
            .engine
            .unwrap_or_else(|| CUSTOM_FALLBACK_ENGINE.to_string());
        let key_name = engine_api_key_name(&engine);
        if validate_cloud_key_name(&key_name).is_ok() {
            names.push(key_name);
        }
    }

    names.sort();
    names.dedup();
    names
}

fn secure_store_get(key_name: &str) -> Result<Option<String>, String> {
    validate_cloud_key_name(key_name)?;
    let entry = keyring::Entry::new(SECURE_KEY_SERVICE, key_name).map_err(|err| {
        format!(
            "Failed to open secure key storage for {}: {}",
            key_name, err
        )
    })?;
    match entry.get_password() {
        Ok(value) => Ok(Some(value)),
        Err(keyring::Error::NoEntry) => Ok(None),
        Err(err) => Err(format!(
            "Failed to read {} from secure key storage: {}",
            key_name, err
        )),
    }
}

fn secure_store_set(key_name: &str, key_value: &str) -> Result<(), String> {
    validate_cloud_key_name(key_name)?;
    let entry = keyring::Entry::new(SECURE_KEY_SERVICE, key_name).map_err(|err| {
        format!(
            "Failed to open secure key storage for {}: {}",
            key_name, err
        )
    })?;
    if key_value.is_empty() {
        return match entry.delete_credential() {
            Ok(()) => Ok(()),
            Err(keyring::Error::NoEntry) => Ok(()),
            Err(err) => Err(format!(
                "Failed to remove {} from secure key storage: {}",
                key_name, err
            )),
        };
    }
    entry
        .set_password(key_value)
        .map_err(|err| format!("Failed to save {} in secure key storage: {}", key_name, err))
}

trait InferenceCredentialStore: Send + Sync {
    fn get(&self, key_name: &str) -> Result<Option<String>, String>;
    fn set(&self, key_name: &str, key_value: &str) -> Result<(), String>;
}

struct SystemInferenceCredentialStore;

impl InferenceCredentialStore for SystemInferenceCredentialStore {
    fn get(&self, key_name: &str) -> Result<Option<String>, String> {
        secure_store_get(key_name)
    }

    fn set(&self, key_name: &str, key_value: &str) -> Result<(), String> {
        secure_store_set(key_name, key_value)
    }
}

fn read_legacy_cloud_keys() -> Vec<(String, String)> {
    let path = legacy_cloud_keys_path();
    let mut keys = Vec::new();
    if let Ok(contents) = std::fs::read_to_string(&path) {
        for line in contents.lines() {
            let line = line.trim();
            if line.is_empty() || line.starts_with('#') {
                continue;
            }
            if let Some((k, v)) = line.split_once('=') {
                keys.push((k.trim().to_string(), v.trim().to_string()));
            }
        }
    }
    keys
}

fn migrate_legacy_cloud_keys() {
    let path = legacy_cloud_keys_path();
    if !path.exists() {
        return;
    }

    let legacy_keys = read_legacy_cloud_keys();
    if legacy_keys.is_empty() {
        let _ = std::fs::remove_file(&path);
        return;
    }

    let mut migrated_all = true;
    for (key, value) in legacy_keys {
        if value.is_empty() {
            continue;
        }
        if secure_store_set(&key, &value).is_err() {
            migrated_all = false;
        }
    }

    if migrated_all {
        let _ = std::fs::remove_file(path);
    }
}

/// Read cloud keys from secure desktop storage and return key=value pairs.
fn read_cloud_keys() -> Vec<(String, String)> {
    migrate_legacy_cloud_keys();
    managed_cloud_key_names()
        .into_iter()
        .filter_map(|key| match secure_store_get(&key) {
            Ok(Some(value)) if !value.is_empty() => Some((key, value)),
            _ => None,
        })
        .collect()
}

/// Overlay a staged first-run credential onto the child-process environment.
/// The durable provider key remains untouched until setup is confirmed.
fn cloud_keys_for_inference(cfg: &InferenceConfig) -> Vec<(String, String)> {
    let mut keys = read_cloud_keys();
    let Some(credential) = PendingInferenceCredential::for_config(cfg) else {
        return keys;
    };
    let Ok(Some(staged)) = secure_store_get(PENDING_INFERENCE_API_KEY) else {
        return keys;
    };
    if staged.is_empty() {
        return keys;
    }
    keys.retain(|(name, _)| name != &credential.target_key);
    keys.push((credential.target_key, staged));
    keys
}

async fn reload_cloud_keys_at(reload_url: &str, keys: Vec<(String, String)>) {
    let key_map: serde_json::Map<String, serde_json::Value> = keys
        .into_iter()
        .map(|(key, value)| (key, serde_json::Value::String(value)))
        .collect();
    let _ = reqwest::Client::new()
        .post(reload_url)
        .json(&serde_json::json!({ "keys": key_map }))
        .timeout(std::time::Duration::from_secs(10))
        .send()
        .await;
}

/// Hot-reload only a live server process launched and owned by this desktop
/// process.  A healthy-looking loopback listener is not proof of ownership and
/// must never receive raw credentials.
async fn reload_cloud_keys_for_owned_backend(
    backend: &SharedBackend,
    status: &SharedStatus,
    keys: Vec<(String, String)>,
) {
    let reload_url = format!("http://127.0.0.1:{}/v1/cloud/reload", JARVIS_PORT);
    reload_cloud_keys_for_owned_backend_at(backend, status, keys, &reload_url).await;
}

async fn reload_cloud_keys_for_owned_backend_at(
    backend: &SharedBackend,
    status: &SharedStatus,
    keys: Vec<(String, String)>,
    reload_url: &str,
) {
    if !status.lock().await.server_ready {
        return;
    }

    // Keep the manager lock for the request so stop/reset cannot kill our
    // child and let an unrelated process claim the port between the ownership
    // check and the credential POST.
    let mut manager = backend.lock().await;
    let Some(handle) = manager.jarvis.as_mut() else {
        return;
    };
    if !matches!(handle.child.try_wait(), Ok(None)) {
        return;
    }
    reload_cloud_keys_at(reload_url, keys).await;
}

/// Save a single cloud API key to secure desktop storage.
#[tauri::command]
async fn save_cloud_key(
    key_name: String,
    key_value: String,
    backend: tauri::State<'_, SharedBackend>,
    status: tauri::State<'_, SharedStatus>,
) -> Result<(), String> {
    let key_value = key_value.trim().to_string();
    secure_store_set(&key_name, &key_value)?;

    // Tell only our own ready child to hot-reload its cloud engine.  Posting to
    // a merely responsive port would disclose the raw key to a port squatter.
    reload_cloud_keys_for_owned_backend(
        backend.inner(),
        status.inner(),
        vec![(key_name, key_value)],
    )
    .await;

    Ok(())
}

/// Get which cloud providers have keys configured (without exposing values).
#[tauri::command]
async fn get_cloud_key_status() -> Result<serde_json::Value, String> {
    migrate_legacy_cloud_keys();
    let status: Vec<serde_json::Value> = managed_cloud_key_names()
        .into_iter()
        .map(|key| {
            let set = matches!(secure_store_get(&key), Ok(Some(value)) if !value.is_empty());
            serde_json::json!({ "key": key, "set": set })
        })
        .collect();
    Ok(serde_json::json!(status))
}

/// Return the current inference-source config for the Settings UI.
#[tauri::command]
async fn get_inference_source() -> Result<InferenceConfig, String> {
    Ok(read_inference_config())
}

/// Persist the chosen inference source. `host` is normalized to a bare base
/// URL. For custom endpoints, an optional API key is stored in secure desktop
/// storage under `<ENGINE>_API_KEY`. Applies on next app launch.
#[tauri::command]
async fn set_inference_source(
    kind: String,
    model: Option<String>,
    host: Option<String>,
    engine: Option<String>,
    api_key: Option<String>,
    pending: Option<bool>,
) -> Result<(), String> {
    let kind = match kind.as_str() {
        "ollama" => SourceKind::Ollama,
        "custom" => SourceKind::Custom,
        other => return Err(format!("Unknown inference source kind: {:?}", other)),
    };
    let cfg = InferenceConfig {
        kind,
        confirmed: !pending.unwrap_or(false),
        model: model.filter(|m| !m.is_empty()),
        host: host.map(|h| normalize_host(&h)).filter(|h| !h.is_empty()),
        engine: engine.filter(|e| !e.is_empty()),
    };
    let api_key = api_key
        .map(|key| key.trim().to_string())
        .filter(|key| !key.is_empty());
    if let SourceKind::Custom = cfg.kind {
        if cfg.host.is_none() {
            return Err("A server URL is required for a custom endpoint.".into());
        }
        if cfg.model.as_deref().unwrap_or("").is_empty() {
            return Err("A model name is required for a custom endpoint.".into());
        }
    }

    let store = SystemInferenceCredentialStore;
    if cfg.confirmed {
        persist_confirmed_inference_config(&cfg, api_key.as_deref(), &store)
    } else {
        stage_pending_inference_config(&cfg, api_key.as_deref(), &store)
    }
}

/// Pull a model via Ollama (called from frontend download button).
#[tauri::command]
async fn pull_ollama_model(model_name: String) -> Result<serde_json::Value, String> {
    pull_model(&model_name)
        .await
        .map_err(|e| format!("Failed to pull {}: {}", model_name, e))?;
    Ok(serde_json::json!({"status": "ok", "model": model_name}))
}

/// Delete a model from Ollama.
#[tauri::command]
async fn delete_ollama_model(model_name: String) -> Result<serde_json::Value, String> {
    let url = format!("http://127.0.0.1:{}/api/delete", OLLAMA_PORT);
    let client = reqwest::Client::builder()
        .timeout(Duration::from_secs(30))
        .build()
        .map_err(|e| e.to_string())?;
    let resp = client
        .delete(&url)
        .json(&serde_json::json!({"name": model_name}))
        .send()
        .await
        .map_err(|e| format!("Delete failed: {}", e))?;
    if !resp.status().is_success() {
        return Err(format!("Delete returned status {}", resp.status()));
    }
    Ok(serde_json::json!({"status": "deleted", "model": model_name}))
}

// ---------------------------------------------------------------------------
// Inference-source selection (~/.openjarvis/inference.json)
// ---------------------------------------------------------------------------

#[derive(serde::Serialize, serde::Deserialize, Clone, Copy, Debug, PartialEq, Eq)]
#[serde(rename_all = "lowercase")]
enum SourceKind {
    Ollama,
    Custom,
}

impl Default for SourceKind {
    fn default() -> Self {
        SourceKind::Ollama
    }
}

#[derive(serde::Serialize, serde::Deserialize, Clone, Debug, Default)]
struct InferenceConfig {
    #[serde(default)]
    kind: SourceKind,
    /// First-run choices stay pending until the complete backend reaches
    /// ready. Legacy configs predate this field and remain trusted.
    #[serde(default = "legacy_config_is_confirmed")]
    confirmed: bool,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    model: Option<String>,
    /// Bare base URL (no trailing `/v1`), custom only.
    #[serde(default, skip_serializing_if = "Option::is_none")]
    host: Option<String>,
    /// OpenAI-compatible engine key (e.g. "lmstudio"), custom only.
    #[serde(default, skip_serializing_if = "Option::is_none")]
    engine: Option<String>,
}

fn legacy_config_is_confirmed() -> bool {
    true
}

/// Path to the inference-source config (~/.openjarvis/inference.json).
fn inference_config_path() -> std::path::PathBuf {
    std::path::PathBuf::from(home_dir())
        .join(".openjarvis")
        .join("inference.json")
}

fn remove_inference_config_at(path: &std::path::Path) -> Result<(), String> {
    match std::fs::remove_file(path) {
        Ok(()) => Ok(()),
        Err(err) if err.kind() == std::io::ErrorKind::NotFound => Ok(()),
        Err(err) => Err(format!("Failed to clear inference config: {}", err)),
    }
}

#[derive(Clone, Debug, PartialEq, Eq)]
struct PendingInferenceCredential {
    target_key: String,
}

impl PendingInferenceCredential {
    fn for_config(cfg: &InferenceConfig) -> Option<Self> {
        if cfg.confirmed || !matches!(cfg.kind, SourceKind::Custom) {
            return None;
        }
        let engine = cfg.engine.as_deref().unwrap_or(CUSTOM_FALLBACK_ENGINE);
        Some(Self {
            target_key: engine_api_key_name(engine),
        })
    }
}

fn restore_credential(
    store: &dyn InferenceCredentialStore,
    key_name: &str,
    previous: Option<&str>,
) -> Result<(), String> {
    store.set(key_name, previous.unwrap_or(""))
}

/// Persist a returning-user source and its optional credential as one logical
/// transaction. If the config write fails, restore the exact prior key.
fn persist_confirmed_inference_config(
    cfg: &InferenceConfig,
    api_key: Option<&str>,
    store: &dyn InferenceCredentialStore,
) -> Result<(), String> {
    persist_confirmed_inference_config_at(cfg, api_key, store, inference_config_path().as_path())
}

fn persist_confirmed_inference_config_at(
    cfg: &InferenceConfig,
    api_key: Option<&str>,
    store: &dyn InferenceCredentialStore,
    path: &std::path::Path,
) -> Result<(), String> {
    let Some(api_key) = api_key else {
        return write_inference_config_at(cfg, path);
    };
    let Some(target_key) = (matches!(cfg.kind, SourceKind::Custom))
        .then(|| engine_api_key_name(cfg.engine.as_deref().unwrap_or(CUSTOM_FALLBACK_ENGINE)))
    else {
        return write_inference_config_at(cfg, path);
    };

    let previous = store
        .get(&target_key)
        .map_err(|err| format!("Could not read the existing API key: {}", err))?;
    store
        .set(&target_key, api_key)
        .map_err(|err| format!("Could not store the API key: {}", err))?;
    if let Err(config_err) = write_inference_config_at(cfg, path) {
        return match restore_credential(store, &target_key, previous.as_deref()) {
            Ok(()) => Err(config_err),
            Err(restore_err) => Err(format!(
                "{}; additionally could not restore the previous API key: {}",
                config_err, restore_err
            )),
        };
    }
    Ok(())
}

/// Stage a first-run key in a dedicated secure slot. The real provider key is
/// not touched until the managed server is healthy and setup is confirmed.
fn stage_pending_inference_config(
    cfg: &InferenceConfig,
    api_key: Option<&str>,
    store: &dyn InferenceCredentialStore,
) -> Result<(), String> {
    stage_pending_inference_config_at(cfg, api_key, store, inference_config_path().as_path())
}

fn stage_pending_inference_config_at(
    cfg: &InferenceConfig,
    api_key: Option<&str>,
    store: &dyn InferenceCredentialStore,
    path: &std::path::Path,
) -> Result<(), String> {
    // A new choice supersedes any interrupted prior attempt. Fail closed if
    // secure storage cannot clear it: otherwise a stale secret could be bound
    // to the wrong engine when boot begins.
    store
        .set(PENDING_INFERENCE_API_KEY, "")
        .map_err(|err| format!("Could not clear a pending API key: {}", err))?;
    if matches!(cfg.kind, SourceKind::Custom) {
        if let Some(api_key) = api_key {
            store
                .set(PENDING_INFERENCE_API_KEY, api_key)
                .map_err(|err| format!("Could not stage the API key: {}", err))?;
        }
    }

    if let Err(config_err) = write_inference_config_at(cfg, path) {
        return match store.set(PENDING_INFERENCE_API_KEY, "") {
            Ok(()) => Err(config_err),
            Err(cleanup_err) => Err(format!(
                "{}; additionally could not discard the staged API key: {}",
                config_err, cleanup_err
            )),
        };
    }
    Ok(())
}

fn discard_pending_inference_setup() -> Result<(), String> {
    discard_pending_inference_setup_at(
        inference_config_path().as_path(),
        &SystemInferenceCredentialStore,
    )
}

fn discard_pending_inference_setup_at(
    path: &std::path::Path,
    store: &dyn InferenceCredentialStore,
) -> Result<(), String> {
    let key_result = store.set(PENDING_INFERENCE_API_KEY, "");
    let config_result = remove_inference_config_at(path);
    match (key_result, config_result) {
        (Ok(()), Ok(())) => Ok(()),
        (Err(key_err), Ok(())) => Err(format!("Failed to discard pending API key: {}", key_err)),
        (Ok(()), Err(config_err)) => Err(config_err),
        (Err(key_err), Err(config_err)) => Err(format!(
            "{}; additionally failed to discard pending API key: {}",
            config_err, key_err
        )),
    }
}

/// Rolls a first-run choice back whenever boot exits before confirmation.
/// Confirmed returning-user configs are never removed by a transient outage.
struct PendingInferenceRollback {
    path: Option<std::path::PathBuf>,
    credential: Option<PendingInferenceCredential>,
    credential_store: Option<Arc<dyn InferenceCredentialStore>>,
}

impl PendingInferenceRollback {
    fn new(cfg: &InferenceConfig) -> Self {
        Self {
            path: (!cfg.confirmed).then_some(inference_config_path()),
            credential: PendingInferenceCredential::for_config(cfg),
            credential_store: (!cfg.confirmed).then(|| {
                Arc::new(SystemInferenceCredentialStore) as Arc<dyn InferenceCredentialStore>
            }),
        }
    }

    #[cfg(test)]
    fn at_path(cfg: &InferenceConfig, path: std::path::PathBuf) -> Self {
        Self {
            path: (!cfg.confirmed).then_some(path),
            credential: None,
            credential_store: None,
        }
    }

    #[cfg(test)]
    fn at_path_with_store(
        cfg: &InferenceConfig,
        path: std::path::PathBuf,
        credential_store: Arc<dyn InferenceCredentialStore>,
    ) -> Self {
        Self {
            path: (!cfg.confirmed).then_some(path),
            credential: PendingInferenceCredential::for_config(cfg),
            credential_store: (!cfg.confirmed).then_some(credential_store),
        }
    }

    fn disarm(&mut self) {
        self.path = None;
        self.credential = None;
        self.credential_store = None;
    }

    fn staged_credential_present(&self) -> Result<bool, String> {
        let (Some(_), Some(store)) = (&self.credential, &self.credential_store) else {
            return Ok(false);
        };
        Ok(matches!(
            store.get(PENDING_INFERENCE_API_KEY)?,
            Some(value) if !value.is_empty()
        ))
    }

    /// Commit a staged first-run choice only after every readiness gate has
    /// succeeded.  Keeping this operation on the rollback guard makes all
    /// successful exits use the same write-then-disarm ordering: if the write
    /// fails (or the future is cancelled), `Drop` removes the staged file.
    fn confirm(&mut self, cfg: &mut InferenceConfig) -> Result<(), String> {
        if cfg.confirmed {
            self.disarm();
            return Ok(());
        }

        let path = self
            .path
            .as_ref()
            .ok_or_else(|| "Pending inference setup lost its rollback path.".to_string())?;
        let mut confirmed = cfg.clone();
        confirmed.confirmed = true;

        let mut promoted: Option<(String, Option<String>)> = None;
        if let (Some(credential), Some(store)) = (&self.credential, &self.credential_store) {
            if let Some(staged) = store.get(PENDING_INFERENCE_API_KEY)? {
                if !staged.is_empty() {
                    let previous = store.get(&credential.target_key)?;
                    store.set(&credential.target_key, &staged)?;
                    if let Err(cleanup_err) = store.set(PENDING_INFERENCE_API_KEY, "") {
                        let restore_result = restore_credential(
                            store.as_ref(),
                            &credential.target_key,
                            previous.as_deref(),
                        );
                        return match restore_result {
                            Ok(()) => Err(cleanup_err),
                            Err(restore_err) => Err(format!(
                                "{}; additionally could not restore the previous API key: {}",
                                cleanup_err, restore_err
                            )),
                        };
                    }
                    promoted = Some((credential.target_key.clone(), previous));
                }
            }
        }

        if let Err(config_err) = write_inference_config_at(&confirmed, path) {
            if let (Some((target_key, previous)), Some(store)) = (promoted, &self.credential_store)
            {
                return match restore_credential(store.as_ref(), &target_key, previous.as_deref()) {
                    Ok(()) => Err(config_err),
                    Err(restore_err) => Err(format!(
                        "{}; additionally could not restore the previous API key: {}",
                        config_err, restore_err
                    )),
                };
            }
            return Err(config_err);
        }
        *cfg = confirmed;
        self.disarm();
        Ok(())
    }
}

impl Drop for PendingInferenceRollback {
    fn drop(&mut self) {
        if let Some(path) = self.path.take() {
            let _ = std::fs::remove_file(path);
        }
        if self.credential.take().is_some() {
            if let Some(store) = self.credential_store.take() {
                let _ = store.set(PENDING_INFERENCE_API_KEY, "");
            }
        }
    }
}

/// Parse only an explicitly persisted source choice. Missing/invalid config is
/// intentionally `None`: callers on the boot path must wait for setup rather
/// than silently falling back to Ollama.
fn parse_configured_inference_config(text: &str) -> Option<InferenceConfig> {
    let value = serde_json::from_str::<serde_json::Value>(text).ok()?;
    if !value.as_object()?.contains_key("kind") {
        return None;
    }
    serde_json::from_value::<InferenceConfig>(value).ok()
}

fn read_configured_inference_config() -> Option<InferenceConfig> {
    std::fs::read_to_string(inference_config_path())
        .ok()
        .and_then(|text| parse_configured_inference_config(&text))
}

/// Read the on-disk inference config, or the Ollama default if absent.
fn read_inference_config() -> InferenceConfig {
    read_configured_inference_config().unwrap_or_default()
}

/// Write the inference config to disk (pretty JSON).
fn write_inference_config(cfg: &InferenceConfig) -> Result<(), String> {
    let path = inference_config_path();
    write_inference_config_at(cfg, &path)
}

fn write_inference_config_at(cfg: &InferenceConfig, path: &std::path::Path) -> Result<(), String> {
    if let Some(parent) = path.parent() {
        let _ = std::fs::create_dir_all(parent);
    }
    let json = serde_json::to_string_pretty(cfg).map_err(|e| e.to_string())?;
    std::fs::write(path, json + "\n").map_err(|e| format!("Failed to save inference config: {}", e))
}

/// Upsert `[engine.<engine>] host = "<host>"` into an existing config.toml
/// string, preserving all other content/formatting. Pure: string in, string out.
fn upsert_engine_host(existing: &str, engine: &str, host: &str) -> Result<String, String> {
    let mut doc = existing
        .parse::<toml_edit::DocumentMut>()
        .map_err(|e| format!("Invalid config.toml: {}", e))?;
    doc["engine"][engine]["host"] = toml_edit::value(host);
    Ok(doc.to_string())
}

/// Write the custom-endpoint host into ~/.openjarvis/config.toml so
/// `jarvis serve` (which reads that file via load_config) points at it.
/// The `<ENGINE>_HOST` env var is unreliable â€” it is shadowed by the engine's
/// non-empty default host in the Python layer â€” so config.toml is the override.
fn set_engine_host_in_config(engine: &str, host: &str) -> Result<(), String> {
    let path = std::path::PathBuf::from(home_dir())
        .join(".openjarvis")
        .join("config.toml");
    if let Some(parent) = path.parent() {
        let _ = std::fs::create_dir_all(parent);
    }
    let existing = std::fs::read_to_string(&path).unwrap_or_default();
    let updated = upsert_engine_host(&existing, engine, host)?;
    std::fs::write(&path, updated).map_err(|e| format!("Failed to write config.toml: {}", e))
}

/// Normalize a user-entered server URL to a bare base host: trim whitespace,
/// drop a trailing `/v1` segment (the engine re-appends its own api prefix),
/// then drop any trailing slash.
fn normalize_host(raw: &str) -> String {
    let s = raw.trim().trim_end_matches('/');
    let s = s.strip_suffix("/v1").unwrap_or(s);
    s.trim_end_matches('/').to_string()
}

/// Check speech backend health.
#[tauri::command]
async fn speech_health(api_url: String) -> Result<serde_json::Value, String> {
    let url = format!("{}/v1/speech/health", api_url);
    let resp = reqwest::get(&url)
        .await
        .map_err(|e| format!("Connection failed: {}", e))?;
    let body: serde_json::Value = resp
        .json()
        .await
        .map_err(|e| format!("Invalid response: {}", e))?;
    Ok(body)
}

// ---------------------------------------------------------------------------
// Native macOS overlay - NSPanel + WKWebView, entirely bypassing Tauri's
// window management so we get proper always-on-top, transparency, non-
// activating panel behaviour and cross-Space support.
// ---------------------------------------------------------------------------

#[cfg(target_os = "macos")]
mod native_overlay {
    use objc::declare::ClassDecl;
    use objc::runtime::{Class, Object, Sel, BOOL, NO, YES};
    use objc::{class, msg_send, sel, sel_impl};
    use std::sync::atomic::{AtomicUsize, Ordering};

    /// Raw pointer to the NSPanel, stored as usize for atomicity.
    static PANEL_PTR: AtomicUsize = AtomicUsize::new(0);
    /// Raw pointer to the WKWebView inside the panel.
    static WEBVIEW_PTR: AtomicUsize = AtomicUsize::new(0);
    /// Raw pointer to the previously-frontmost NSRunningApplication.
    static PREV_APP: AtomicUsize = AtomicUsize::new(0);

    // CoreGraphics geometry types expected by AppKit.
    #[repr(C)]
    #[derive(Copy, Clone)]
    struct CGPoint {
        x: f64,
        y: f64,
    }
    #[repr(C)]
    #[derive(Copy, Clone)]
    struct CGSize {
        width: f64,
        height: f64,
    }
    #[repr(C)]
    #[derive(Copy, Clone)]
    struct CGRect {
        origin: CGPoint,
        size: CGSize,
    }

    /// Create an autoreleased NSString from a Rust &str.
    unsafe fn nsstring(s: &str) -> *mut Object {
        let obj: *mut Object = msg_send![class!(NSString), alloc];
        msg_send![obj,
            initWithBytes: s.as_ptr()
            length: s.len()
            encoding: 4usize  // NSUTF8StringEncoding
        ]
    }

    // ------------------------------------------------------------------
    // Conversation persistence
    // ------------------------------------------------------------------

    fn conversation_path() -> std::path::PathBuf {
        std::path::PathBuf::from(super::home_dir())
            .join(".openjarvis")
            .join("overlay-conversation.json")
    }

    pub fn load_conversation() -> String {
        std::fs::read_to_string(conversation_path()).unwrap_or_else(|_| "[]".into())
    }

    /// Read cloud API keys and return a JSON array of model IDs
    /// whose provider has a key configured.
    fn cloud_models_json() -> String {
        let keys = super::read_cloud_keys();
        let mut models: Vec<&str> = Vec::new();
        for (name, value) in &keys {
            if value.is_empty() {
                continue;
            }
            match name.as_str() {
                "OPENAI_API_KEY" => models.extend(["gpt-4o", "gpt-4o-mini"]),
                "ANTHROPIC_API_KEY" => {
                    models.extend(["claude-sonnet-4-20250514", "claude-haiku-4-20250414"])
                }
                "GEMINI_API_KEY" | "GOOGLE_API_KEY" => {
                    models.extend(["gemini-2.5-flash", "gemini-2.5-pro"])
                }
                _ => {}
            }
        }
        serde_json::to_string(&models).unwrap_or_else(|_| "[]".into())
    }

    fn save_conversation(json: &str) {
        let path = conversation_path();
        if let Some(parent) = path.parent() {
            let _ = std::fs::create_dir_all(parent);
        }
        let _ = std::fs::write(&path, json);
    }

    /// Apply every transparency trick to the WKWebView.
    /// Called once at creation and again after the page finishes loading.
    unsafe fn force_transparent(wv: *mut Object) {
        let clear: *mut Object = msg_send![class!(NSColor), clearColor];
        let _: () = msg_send![wv, _setDrawsBackground: NO];
        let no_num: *mut Object = msg_send![class!(NSNumber), numberWithBool: NO];
        let _: () = msg_send![wv, setValue: no_num forKey: nsstring("drawsBackground")];
        let _: () = msg_send![wv, setUnderPageBackgroundColor: clear];
        // Also inject CSS to nuke any remaining background
        let js = nsstring(
            "document.documentElement.style.background='transparent';\
             document.body.style.background='transparent';",
        );
        let nil: *mut Object = std::ptr::null_mut();
        let _: () = msg_send![wv, evaluateJavaScript: js completionHandler: nil];
    }

    // ------------------------------------------------------------------
    // Public API (must be called on the main thread)
    // ------------------------------------------------------------------

    /// Build the native overlay panel.  Call once during app setup.
    pub unsafe fn create(html: &str, api_port: u16) {
        // --- Custom NSPanel subclass that accepts keyboard input ------
        if Class::get("JarvisOverlayPanel").is_none() {
            let sup = Class::get("NSPanel").unwrap();
            let mut decl = ClassDecl::new("JarvisOverlayPanel", sup).unwrap();
            extern "C" fn yes(_: &Object, _: Sel) -> BOOL {
                YES
            }
            decl.add_method(
                sel!(canBecomeKeyWindow),
                yes as extern "C" fn(&Object, Sel) -> BOOL,
            );
            decl.register();
        }

        // --- WKNavigationDelegate - re-apply transparency after load --
        if Class::get("JarvisOverlayNavDelegate").is_none() {
            let sup = Class::get("NSObject").unwrap();
            let mut decl = ClassDecl::new("JarvisOverlayNavDelegate", sup).unwrap();
            extern "C" fn did_finish(_: &Object, _: Sel, wv: *mut Object, _nav: *mut Object) {
                unsafe {
                    force_transparent(wv);
                }
            }
            decl.add_method(
                sel!(webView:didFinishNavigation:),
                did_finish as extern "C" fn(&Object, Sel, *mut Object, *mut Object),
            );
            decl.register();
        }

        // --- WKScriptMessageHandler so JS can call hide() ------------
        if Class::get("JarvisOverlayMsgHandler").is_none() {
            let sup = Class::get("NSObject").unwrap();
            let mut decl = ClassDecl::new("JarvisOverlayMsgHandler", sup).unwrap();
            extern "C" fn on_msg(_: &Object, _: Sel, _ctrl: *mut Object, msg: *mut Object) {
                unsafe {
                    let body: *mut Object = msg_send![msg, body];
                    if body.is_null() {
                        return;
                    }
                    let c: *const std::os::raw::c_char = msg_send![body, UTF8String];
                    if c.is_null() {
                        return;
                    }
                    if let Ok(s) = std::ffi::CStr::from_ptr(c).to_str() {
                        if s == "hide" {
                            hide();
                        } else if let Some(json) = s.strip_prefix("save:") {
                            save_conversation(json);
                        } else if let Some(coords) = s.strip_prefix("drag:") {
                            drag(coords);
                        }
                    }
                }
            }
            decl.add_method(
                sel!(userContentController:didReceiveScriptMessage:),
                on_msg as extern "C" fn(&Object, Sel, *mut Object, *mut Object),
            );
            decl.register();
        }

        // --- Create the NSPanel --------------------------------------
        let frame = CGRect {
            origin: CGPoint { x: 0.0, y: 0.0 },
            size: CGSize {
                width: 560.0,
                height: 400.0,
            },
        };
        // NSWindowStyleMaskNonactivatingPanel = 1 << 7
        let style: u64 = 1 << 7;

        let cls = Class::get("JarvisOverlayPanel").unwrap();
        let panel: *mut Object = msg_send![cls, alloc];
        let panel: *mut Object = msg_send![panel,
            initWithContentRect: frame
            styleMask: style
            backing: 2u64       // NSBackingStoreBuffered
            defer: NO
        ];

        // Window level - NSFloatingWindowLevel (3).
        let _: () = msg_send![panel, setLevel: 3_i64];
        // canJoinAllSpaces (1) | fullScreenAuxiliary (1<<8)
        let _: () = msg_send![panel, setCollectionBehavior: 257_u64];
        let _: () = msg_send![panel, setHidesOnDeactivate: NO];
        let _: () = msg_send![panel, setOpaque: NO];
        let _: () = msg_send![panel, setHasShadow: NO];
        let _: () = msg_send![panel, setMovableByWindowBackground: YES];

        let clear: *mut Object = msg_send![class!(NSColor), clearColor];
        let _: () = msg_send![panel, setBackgroundColor: clear];
        let _: () = msg_send![panel, center];

        // --- WKWebView -----------------------------------------------
        let cfg: *mut Object = msg_send![class!(WKWebViewConfiguration), alloc];
        let cfg: *mut Object = msg_send![cfg, init];

        // Attach message handler ("overlay" channel)
        let hcls = Class::get("JarvisOverlayMsgHandler").unwrap();
        let handler: *mut Object = msg_send![hcls, alloc];
        let handler: *mut Object = msg_send![handler, init];
        let uc: *mut Object = msg_send![cfg, userContentController];
        let _: () = msg_send![uc,
            addScriptMessageHandler: handler
            name: nsstring("overlay")
        ];

        let wv: *mut Object = msg_send![class!(WKWebView), alloc];
        let wv: *mut Object = msg_send![wv,
            initWithFrame: frame
            configuration: cfg
        ];

        // ---- Make the webview fully transparent ----
        force_transparent(wv);

        // Set navigation delegate so we re-apply after page loads
        let nav_cls = Class::get("JarvisOverlayNavDelegate").unwrap();
        let nav_del: *mut Object = msg_send![nav_cls, alloc];
        let nav_del: *mut Object = msg_send![nav_del, init];
        let _: () = msg_send![wv, setNavigationDelegate: nav_del];

        let _: () = msg_send![panel, setContentView: wv];
        WEBVIEW_PTR.store(wv as usize, Ordering::SeqCst);

        // Inject saved conversation into the HTML template, then load it.
        // Use the API server as the base URL so fetch() is same-origin.
        // Escape "</" so the JSON can't prematurely close the <script> tag.
        // ("\/" is valid JSON - resolves back to "/" when parsed.)
        let saved = load_conversation().replace("</", "<\\/");
        let cloud = cloud_models_json();
        let filled = html
            .replace("__SAVED_MESSAGES__", &saved)
            .replace("__CLOUD_MODELS__", &cloud);
        let base_str = nsstring(&format!("http://127.0.0.1:{}", api_port));
        let base_url: *mut Object = msg_send![class!(NSURL), URLWithString: base_str];
        let _: () = msg_send![wv,
            loadHTMLString: nsstring(&filled)
            baseURL: base_url
        ];

        PANEL_PTR.store(panel as usize, Ordering::SeqCst);
    }

    pub unsafe fn toggle() {
        let ptr = PANEL_PTR.load(Ordering::SeqCst);
        if ptr == 0 {
            return;
        }
        let panel = ptr as *mut Object;
        let vis: BOOL = msg_send![panel, isVisible];
        if vis != NO {
            hide();
        } else {
            show();
        }
    }

    pub unsafe fn show() {
        let ptr = PANEL_PTR.load(Ordering::SeqCst);
        if ptr == 0 {
            return;
        }
        let panel = ptr as *mut Object;

        // Re-apply transparency every time (the webview can reset it)
        let wv_ptr = WEBVIEW_PTR.load(Ordering::SeqCst);
        if wv_ptr != 0 {
            force_transparent(wv_ptr as *mut Object);
        }

        // Remember the currently-frontmost app so we can restore it.
        let ws: *mut Object = msg_send![class!(NSWorkspace), sharedWorkspace];
        let front: *mut Object = msg_send![ws, frontmostApplication];
        if !front.is_null() {
            let _: () = msg_send![front, retain];
            let old = PREV_APP.swap(front as usize, Ordering::SeqCst);
            if old != 0 {
                let _: () = msg_send![(old as *mut Object), release];
            }
        }

        // Activate our process so the panel receives keyboard input.
        let app: *mut Object = msg_send![class!(NSApplication), sharedApplication];
        let _: () = msg_send![app, activateIgnoringOtherApps: YES];
        let nil: *mut Object = std::ptr::null_mut();
        let _: () = msg_send![panel, makeKeyAndOrderFront: nil];

        // Focus the text field inside the webview.
        let wv: *mut Object = msg_send![panel, contentView];
        let js = nsstring("document.getElementById('input').focus()");
        let _: () = msg_send![wv, evaluateJavaScript: js completionHandler: nil];
    }

    /// Move the panel by a screen-space delta (called from JS drag handler).
    unsafe fn drag(coords: &str) {
        let ptr = PANEL_PTR.load(Ordering::SeqCst);
        if ptr == 0 {
            return;
        }
        let panel = ptr as *mut Object;
        let Some((dxs, dys)) = coords.split_once(',') else {
            return;
        };
        let Ok(dx) = dxs.parse::<f64>() else { return };
        let Ok(dy) = dys.parse::<f64>() else { return };
        // NSWindow frame origin is bottom-left; screen Y increases upward,
        // but mouse screenY increases downward, so invert dy.
        let frame: CGRect = msg_send![panel, frame];
        let origin = CGPoint {
            x: frame.origin.x + dx,
            y: frame.origin.y - dy,
        };
        let _: () = msg_send![panel, setFrameOrigin: origin];
    }

    pub unsafe fn hide() {
        let ptr = PANEL_PTR.load(Ordering::SeqCst);
        if ptr == 0 {
            return;
        }
        let panel = ptr as *mut Object;
        let nil: *mut Object = std::ptr::null_mut();
        let _: () = msg_send![panel, orderOut: nil];

        // Give focus back to whatever app was frontmost before.
        let prev = PREV_APP.swap(0, Ordering::SeqCst);
        if prev != 0 {
            let prev_app = prev as *mut Object;
            let _: BOOL = msg_send![prev_app, activateWithOptions: 2_u64];
            let _: () = msg_send![prev_app, release];
        }
    }
}

/// Dispatch a closure onto the main thread via GCD.
#[cfg(target_os = "macos")]
fn on_main_thread(f: impl FnOnce() + Send + 'static) {
    dispatch::Queue::main().exec_async(f);
}

// ---------------------------------------------------------------------------
// Overlay Tauri commands (thin wrappers that dispatch to the main thread)
// ---------------------------------------------------------------------------

#[tauri::command]
async fn get_overlay_conversation() -> Result<String, String> {
    #[cfg(target_os = "macos")]
    {
        return Ok(native_overlay::load_conversation());
    }
    #[cfg(not(target_os = "macos"))]
    Ok("[]".into())
}

#[tauri::command]
async fn toggle_overlay() -> Result<(), String> {
    #[cfg(target_os = "macos")]
    on_main_thread(|| unsafe { native_overlay::toggle() });
    Ok(())
}

#[tauri::command]
async fn hide_overlay() -> Result<(), String> {
    #[cfg(target_os = "macos")]
    on_main_thread(|| unsafe { native_overlay::hide() });
    Ok(())
}

// ---------------------------------------------------------------------------
// App entry point
// ---------------------------------------------------------------------------

#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
    load_env_file();
    log_startup(&format!("run(): OPENJARVIS_ROOT={:?}", std::env::var("OPENJARVIS_ROOT")));
    let backend: SharedBackend = Arc::new(Mutex::new(BackendManager::default()));
    let configured_at_launch = match read_configured_inference_config() {
        Some(cfg) if cfg.confirmed => {
            // A confirmed source never consumes a staging slot. Clear any
            // remnant from a prior interrupted config write.
            let _ = secure_store_set(PENDING_INFERENCE_API_KEY, "");
            Some(cfg)
        }
        Some(_) => {
            // A prior first-run boot was interrupted or failed before it
            // reached ready. Never replay that unvalidated choice on launch.
            let _ = discard_pending_inference_setup();
            None
        }
        None => {
            // Clean up a stage left behind if the process exited between the
            // secure-store write and the pending config write.
            let _ = secure_store_set(PENDING_INFERENCE_API_KEY, "");
            None
        }
    };
    let initial_status = configured_at_launch
        .as_ref()
        .map(SetupStatus::starting)
        .unwrap_or_default();
    let status: SharedStatus = Arc::new(Mutex::new(initial_status));

    let boot_backend_ref = backend.clone();
    let boot_status_ref = status.clone();

    tauri::Builder::default()
        .manage(backend.clone())
        .manage(status.clone())
        .plugin(tauri_plugin_notification::init())
        .plugin(tauri_plugin_shell::init())
        .plugin(tauri_plugin_global_shortcut::Builder::new().build())
        .plugin(tauri_plugin_autostart::init(
            MacosLauncher::LaunchAgent,
            Some(vec!["--hidden"]),
        ))
        .plugin(tauri_plugin_updater::Builder::new().build())
        .plugin(tauri_plugin_process::init())
        .plugin(tauri_plugin_dialog::init())
        .plugin(tauri_plugin_single_instance::init(|app, _args, _cwd| {
            if let Some(window) = app.get_webview_window("main") {
                let _ = window.set_focus();
            }
        }))
        .setup(move |app| {
            // System tray
            let show = MenuItemBuilder::with_id("show", "Show / Hide").build(app)?;
            let health = MenuItemBuilder::with_id("health", "Health: starting...")
                .enabled(false)
                .build(app)?;
            let quit = MenuItemBuilder::with_id("quit", "Quit OpenJarvis").build(app)?;

            let menu = MenuBuilder::new(app)
                .item(&show)
                .separator()
                .item(&health)
                .separator()
                .item(&quit)
                .build()?;

            let _tray = TrayIconBuilder::with_id("main")
                .icon(app.default_window_icon().unwrap().clone())
                .tooltip("OpenJarvis")
                .menu(&menu)
                .on_menu_event(move |app, event| match event.id().as_ref() {
                    "show" => {
                        if let Some(window) = app.get_webview_window("main") {
                            if window.is_visible().unwrap_or(false) {
                                let _ = window.hide();
                            } else {
                                let _ = window.show();
                                let _ = window.set_focus();
                            }
                        }
                    }
                    "quit" => {
                        app.exit(0);
                    }
                    _ => {}
                })
                .build(app)?;

            // Create native macOS overlay panel
            #[cfg(target_os = "macos")]
            unsafe {
                native_overlay::create(include_str!("overlay.html"), JARVIS_PORT);
            }

            // Register Cmd+Shift+Space to toggle the overlay
            {
                use tauri_plugin_global_shortcut::{
                    Code, GlobalShortcutExt, Modifiers, Shortcut, ShortcutState,
                };
                let sc = Shortcut::new(Some(Modifiers::META | Modifiers::SHIFT), Code::Space);
                if let Err(e) = app.global_shortcut().on_shortcut(sc, |_app, _sc, ev| {
                    if ev.state == ShortcutState::Pressed {
                        #[cfg(target_os = "macos")]
                        unsafe {
                            native_overlay::toggle();
                        }
                    }
                }) {
                    eprintln!("Warning: could not register Cmd+Shift+Space: {e}");
                }
            }

            // Returning users keep automatic startup after they have persisted
            // a source. Fresh installs stay inert until the setup UI records
            // explicit consent and invokes `start_backend`.
            if configured_at_launch.is_some() {
                tauri::async_runtime::spawn(start_managed_boot(boot_backend_ref, boot_status_ref));
            }

            Ok(())
        })
        .invoke_handler(tauri::generate_handler![
            get_setup_status,
            get_api_base,
            start_backend,
            stop_backend,
            reset_inference_source,
            check_health,
            fetch_energy,
            fetch_telemetry,
            fetch_traces,
            fetch_trace,
            fetch_learning_stats,
            fetch_learning_policy,
            fetch_memory_stats,
            search_memory,
            fetch_agents,
            fetch_models,
            run_jarvis_command,
            fetch_savings,
            submit_savings,
            transcribe_audio,
            speech_health,
            pull_ollama_model,
            delete_ollama_model,
            save_cloud_key,
            get_cloud_key_status,
            get_inference_source,
            set_inference_source,
            toggle_overlay,
            hide_overlay,
            get_overlay_conversation,
        ])
        .build(tauri::generate_context!())
        .expect("error while building OpenJarvis Desktop")
        .run(move |_app, event| {
            if let tauri::RunEvent::ExitRequested { .. } = event {
                let b = backend.clone();
                tauri::async_runtime::spawn(async move {
                    b.lock().await.stop_all().await;
                });
            }
        });
}

// ---------------------------------------------------------------------------
// Tests
// ---------------------------------------------------------------------------

#[cfg(test)]
mod tests {
    use super::{
        boot_plan, default_local_model, discard_pending_inference_setup_at,
        format_extension_import_failure, format_missing_rust_toolchain, format_port_unavailable,
        format_uv_sync_failure, format_uv_sync_spawn_error, matching_installed_model,
        model_names_match, normalize_host, parse_configured_inference_config,
        parse_ollama_model_names, persist_confirmed_inference_config_at, preferred_installed_model,
        reload_cloud_keys_for_owned_backend_at, should_persist_resolved_model, spawn_owned_child,
        stage_pending_inference_config_at, startup_installed_model, upsert_engine_host,
        uv_sync_stderr_tail, BackendManager, InferenceConfig, InferenceCredentialStore,
        PendingInferenceRollback, SetupStatus, SourceKind, DESKTOP_UV_SYNC_COMMAND,
        PENDING_INFERENCE_API_KEY,
    };
    use std::collections::HashMap;
    use std::path::Path;
    use std::sync::Mutex as StdMutex;

    #[derive(Default)]
    struct MemoryCredentialStore {
        values: StdMutex<HashMap<String, String>>,
    }

    impl MemoryCredentialStore {
        fn put(&self, key_name: &str, key_value: &str) {
            self.values
                .lock()
                .unwrap()
                .insert(key_name.to_string(), key_value.to_string());
        }

        fn value(&self, key_name: &str) -> Option<String> {
            self.values.lock().unwrap().get(key_name).cloned()
        }
    }

    impl InferenceCredentialStore for MemoryCredentialStore {
        fn get(&self, key_name: &str) -> Result<Option<String>, String> {
            Ok(self.value(key_name))
        }

        fn set(&self, key_name: &str, key_value: &str) -> Result<(), String> {
            let mut values = self.values.lock().unwrap();
            if key_value.is_empty() {
                values.remove(key_name);
            } else {
                values.insert(key_name.to_string(), key_value.to_string());
            }
            Ok(())
        }
    }

    fn unique_test_root(label: &str) -> std::path::PathBuf {
        let nonce = std::time::SystemTime::now()
            .duration_since(std::time::UNIX_EPOCH)
            .unwrap()
            .as_nanos();
        std::env::temp_dir().join(format!(
            "openjarvis-{}-{}-{}",
            label,
            std::process::id(),
            nonce
        ))
    }

    #[test]
    fn tail_returns_whole_string_when_shorter_than_limit() {
        assert_eq!(uv_sync_stderr_tail("short error", 800), "short error");
    }

    #[test]
    fn tail_keeps_the_end_not_the_beginning() {
        // uv's actionable line is at the end; the spinner noise is at the start.
        let s = format!("{}ACTUAL ERROR HERE", "spinner-noise ".repeat(200));
        let tail = uv_sync_stderr_tail(&s, 40);
        assert!(tail.ends_with("ACTUAL ERROR HERE"), "tail was: {tail:?}");
        assert!(!tail.contains("spinner-noise spinner-noise spinner-noise"));
        assert!(tail.chars().count() <= 40);
    }

    #[test]
    fn tail_trims_surrounding_whitespace() {
        assert_eq!(uv_sync_stderr_tail("  \n padded \n  ", 800), "padded");
    }

    #[test]
    fn tail_never_splits_a_multibyte_codepoint() {
        // Each "Ã©" is 2 bytes / 1 char. A byte-based slice could panic or
        // produce invalid UTF-8; the char-based tail must not.
        let s = "Ã©".repeat(500);
        let tail = uv_sync_stderr_tail(&s, 100);
        assert_eq!(tail.chars().count(), 100);
        assert!(tail.chars().all(|c| c == 'Ã©'));
    }

    #[test]
    fn failure_message_includes_exit_code_and_tail_and_hint() {
        let msg = format_uv_sync_failure(
            Path::new("/home/u/.openjarvis/src"),
            Some(2),
            "error: failed to resolve numpy==2.1.3",
        );
        assert!(msg.contains("exit 2"));
        assert!(msg.contains("/home/u/.openjarvis/src"));
        assert!(msg.contains("failed to resolve numpy==2.1.3"));
        assert!(msg.contains(DESKTOP_UV_SYNC_COMMAND)); // actionable next step
    }

    #[test]
    fn failure_message_renders_missing_exit_code_as_unknown() {
        // Process killed by signal â†’ no exit code. Must not show a misleading -1.
        let msg = format_uv_sync_failure(Path::new("/x"), None, "boom");
        assert!(msg.contains("exit unknown"));
        assert!(!msg.contains("exit -1"));
    }

    #[test]
    fn spawn_error_names_the_binary_and_root() {
        let msg = format_uv_sync_spawn_error(
            Path::new("/repo"),
            "C:\\Users\\me\\.local\\bin\\uv.exe",
            "No such file or directory (os error 2)",
        );
        assert!(msg.contains("C:\\Users\\me\\.local\\bin\\uv.exe"));
        assert!(msg.contains("/repo"));
        assert!(msg.contains("No such file or directory"));
    }

    #[test]
    fn missing_rust_toolchain_message_names_cargo_and_installer() {
        let msg = format_missing_rust_toolchain();
        assert!(msg.contains("cargo"));
        assert!(msg.contains("https://rustup.rs"));
        assert!(msg.contains("openjarvis_rust"));
        assert!(msg.contains("Visual Studio Build Tools"));
    }

    #[test]
    fn uv_sync_rust_failure_mentions_toolchain() {
        let msg = format_uv_sync_failure(
            Path::new("C:\\Users\\me\\OpenJarvis"),
            Some(1),
            "maturin failed: linker `link.exe` not found while building openjarvis-rust",
        );
        assert!(msg.contains("exit 1"));
        assert!(msg.contains("link.exe"));
        assert!(msg.contains("https://rustup.rs"));
        assert!(msg.contains("Visual Studio Build Tools"));
    }

    #[test]
    fn extension_import_failure_names_verification_command() {
        let msg = format_extension_import_failure(
            Path::new("C:\\Users\\me\\OpenJarvis"),
            "ModuleNotFoundError: No module named 'openjarvis_rust'",
        );
        assert!(msg.contains("openjarvis_rust"));
        assert!(msg.contains(DESKTOP_UV_SYNC_COMMAND));
        assert!(msg.contains("uv run python -c \"import openjarvis_rust\""));
        assert!(msg.contains("ModuleNotFoundError"));
    }

    #[test]
    fn port_unavailable_message_names_port_and_owner_hint() {
        let msg = format_port_unavailable(8000, "address already in use");
        assert!(msg.contains("Port 8000 is not available"));
        assert!(msg.contains("address already in use"));
        assert!(msg.contains("To identify it"));
        assert!(msg.contains("8000"));
    }

    #[test]
    fn default_local_model_picks_second_largest_that_fits() {
        // QWEN35_MODELS min_ram ladder: 4,6,8,12,24,32,96 GB
        assert_eq!(default_local_model(4.0), "qwen3.5:0.8b"); // only one fits
        assert_eq!(default_local_model(8.0), "qwen3.5:2b"); // fits 0.8/2/4 â†’ 2nd-largest
        assert_eq!(default_local_model(16.0), "qwen3.5:4b"); // fits ..9b â†’ 2nd-largest
        assert_eq!(default_local_model(32.0), "qwen3.5:27b"); // fits 0.8/2/4/9/27/35b â†’ 2nd-largest is 27b
        assert_eq!(default_local_model(128.0), "qwen3.5:35b"); // fits all â†’ 2nd-largest
    }

    #[test]
    fn default_local_model_falls_back_when_nothing_fits() {
        assert_eq!(default_local_model(1.0), super::FALLBACK_MODEL);
    }

    #[test]
    fn parse_ollama_model_names_reads_nonempty_names() {
        let body = serde_json::json!({
            "models": [
                {"name": "llama3.2:latest"},
                {"name": ""},
                {"name": "qwen3.5:4b"},
                {"model": "mistral:latest"}
            ]
        });
        assert_eq!(
            parse_ollama_model_names(&body),
            vec![
                "llama3.2:latest".to_string(),
                "qwen3.5:4b".to_string(),
                "mistral:latest".to_string()
            ]
        );
    }

    #[test]
    fn model_names_match_treats_latest_as_optional() {
        assert!(model_names_match("llama3.2:latest", "llama3.2"));
        assert!(model_names_match("llama3.2", "llama3.2:latest"));
        assert!(model_names_match("qwen3.5:4b", "qwen3.5:4b"));
        assert!(!model_names_match("llama3.2:latest", "qwen3.5:4b"));
    }

    #[test]
    fn installed_model_helpers_pick_matching_or_first_model() {
        let models = vec!["llama3.2:latest".to_string(), "qwen3.5:4b".to_string()];
        assert_eq!(
            matching_installed_model(&models, "llama3.2"),
            Some("llama3.2:latest".to_string())
        );
        assert_eq!(
            preferred_installed_model(&models),
            Some("llama3.2:latest".to_string())
        );
    }

    #[test]
    fn preferred_installed_model_skips_embedding_names_when_chat_model_exists() {
        let models = vec![
            "nomic-embed-text:latest".to_string(),
            "llama3.2:latest".to_string(),
        ];
        assert_eq!(
            preferred_installed_model(&models),
            Some("llama3.2:latest".to_string())
        );
    }

    #[test]
    fn startup_installed_model_uses_existing_model_for_defaults() {
        let models = vec!["llama3.2:latest".to_string()];
        assert_eq!(
            startup_installed_model("qwen3.5:4b", &models),
            Some("llama3.2:latest".to_string())
        );
    }

    #[test]
    fn startup_installed_model_uses_existing_model_when_configured_model_missing() {
        let models = vec!["llama3.2:latest".to_string()];
        assert_eq!(
            startup_installed_model("qwen3.5:4b", &models),
            Some("llama3.2:latest".to_string())
        );
    }

    #[test]
    fn resolved_model_is_only_persisted_when_no_model_was_configured() {
        let default_cfg = InferenceConfig {
            kind: SourceKind::Ollama,
            ..Default::default()
        };
        assert!(should_persist_resolved_model(&default_cfg));

        let empty_cfg = InferenceConfig {
            kind: SourceKind::Ollama,
            model: Some(" ".into()),
            ..Default::default()
        };
        assert!(should_persist_resolved_model(&empty_cfg));

        let user_cfg = InferenceConfig {
            kind: SourceKind::Ollama,
            model: Some("qwen3.5:9b".into()),
            ..Default::default()
        };
        assert!(!should_persist_resolved_model(&user_cfg));
    }

    #[test]
    fn startup_requires_an_explicit_valid_source_config() {
        assert!(parse_configured_inference_config("").is_none());
        assert!(parse_configured_inference_config("not json").is_none());
        assert!(parse_configured_inference_config("{}").is_none());

        let ollama = parse_configured_inference_config(r#"{"kind":"ollama"}"#).unwrap();
        assert!(matches!(ollama.kind, SourceKind::Ollama));
        assert!(ollama.confirmed, "legacy explicit configs remain trusted");

        let custom = parse_configured_inference_config(
            r#"{"kind":"custom","model":"m","host":"http://localhost:1234"}"#,
        )
        .unwrap();
        assert!(matches!(custom.kind, SourceKind::Custom));
        assert!(custom.confirmed);

        let pending = parse_configured_inference_config(
            r#"{"kind":"custom","confirmed":false,"model":"m","host":"http://localhost:1234"}"#,
        )
        .unwrap();
        assert!(!pending.confirmed);
    }

    #[test]
    fn initial_setup_status_is_inert_until_a_source_is_chosen() {
        let status = SetupStatus::default();
        assert!(status.requires_source);
        assert_eq!(status.phase, "awaiting_source");
        assert_eq!(status.source, "unconfigured");
        assert!(!status.ollama_ready);
        assert!(!status.model_ready);
        assert!(!status.server_ready);
    }

    #[test]
    fn persisted_source_status_can_enter_startup() {
        let cfg = InferenceConfig {
            kind: SourceKind::Custom,
            confirmed: true,
            model: Some("m".into()),
            host: Some("http://localhost:1234".into()),
            engine: Some("lmstudio".into()),
        };
        let status = SetupStatus::starting(&cfg);
        assert!(!status.requires_source);
        assert_eq!(status.phase, "starting");
        assert_eq!(status.source, "custom");
    }

    #[test]
    fn parse_reads_custom_endpoint() {
        let cfg = parse_configured_inference_config(
            r#"{"kind":"custom","model":"qwen2.5-7b","host":"http://localhost:1234","engine":"lmstudio"}"#,
        )
        .unwrap();
        assert!(matches!(cfg.kind, SourceKind::Custom));
        assert_eq!(cfg.model.as_deref(), Some("qwen2.5-7b"));
        assert_eq!(cfg.host.as_deref(), Some("http://localhost:1234"));
        assert_eq!(cfg.engine.as_deref(), Some("lmstudio"));
    }

    #[test]
    fn normalize_host_strips_trailing_slash_and_v1() {
        assert_eq!(
            normalize_host("http://localhost:1234/v1"),
            "http://localhost:1234"
        );
        assert_eq!(
            normalize_host("http://localhost:1234/v1/"),
            "http://localhost:1234"
        );
        assert_eq!(
            normalize_host("http://localhost:1234/"),
            "http://localhost:1234"
        );
        assert_eq!(normalize_host("http://host:8000"), "http://host:8000");
    }

    #[test]
    fn boot_plan_ollama_launches_and_pulls_one_model() {
        let cfg = InferenceConfig {
            kind: SourceKind::Ollama,
            ..Default::default()
        };
        let plan = boot_plan(&cfg, 16.0);
        assert!(plan.launch_ollama);
        assert_eq!(plan.model_to_pull.as_deref(), Some("qwen3.5:4b"));
        assert!(plan.engine_host.is_none());
        assert!(plan
            .serve_args
            .windows(2)
            .any(|w| w == ["--engine", "ollama"]));
        assert!(plan
            .serve_args
            .windows(2)
            .any(|w| w == ["--model", "qwen3.5:4b"]));
    }

    #[test]
    fn boot_plan_ollama_respects_pinned_model() {
        let cfg = InferenceConfig {
            kind: SourceKind::Ollama,
            model: Some("qwen3.5:9b".into()),
            ..Default::default()
        };
        let plan = boot_plan(&cfg, 16.0);
        assert_eq!(plan.model_to_pull.as_deref(), Some("qwen3.5:9b"));
    }

    #[test]
    fn boot_plan_custom_skips_ollama_and_sets_engine_host() {
        let cfg = InferenceConfig {
            kind: SourceKind::Custom,
            confirmed: true,
            model: Some("qwen2.5-7b".into()),
            host: Some("http://localhost:1234".into()),
            engine: Some("lmstudio".into()),
        };
        let plan = boot_plan(&cfg, 16.0);
        assert!(!plan.launch_ollama);
        assert!(plan.model_to_pull.is_none());
        assert_eq!(
            plan.engine_host,
            Some(("lmstudio".to_string(), "http://localhost:1234".to_string()))
        );
        assert!(plan
            .serve_args
            .windows(2)
            .any(|w| w == ["--engine", "lmstudio"]));
        assert!(plan
            .serve_args
            .windows(2)
            .any(|w| w == ["--model", "qwen2.5-7b"]));
    }

    #[test]
    fn boot_plan_custom_defaults_engine_to_lmstudio() {
        let cfg = InferenceConfig {
            kind: SourceKind::Custom,
            confirmed: true,
            model: Some("m".into()),
            host: Some("http://h:1".into()),
            engine: None,
        };
        let plan = boot_plan(&cfg, 16.0);
        assert_eq!(plan.engine_host.as_ref().unwrap().0, "lmstudio");
        assert!(plan
            .serve_args
            .windows(2)
            .any(|w| w == ["--engine", "lmstudio"]));
    }

    #[test]
    fn boot_plan_custom_omits_engine_host_when_no_host() {
        // No configured host â†’ don't set engine_host (no override to write).
        let cfg = InferenceConfig {
            kind: SourceKind::Custom,
            confirmed: true,
            model: Some("m".into()),
            host: None,
            engine: Some("lmstudio".into()),
        };
        let plan = boot_plan(&cfg, 16.0);
        assert!(plan.engine_host.is_none());
    }

    #[test]
    fn pending_config_rolls_back_unless_boot_confirms_it() {
        let root = std::env::temp_dir().join(format!(
            "openjarvis-pending-inference-{}",
            std::process::id()
        ));
        std::fs::create_dir_all(&root).unwrap();
        let pending_path = root.join("pending.json");
        std::fs::write(&pending_path, "pending").unwrap();
        let pending = InferenceConfig {
            kind: SourceKind::Custom,
            confirmed: false,
            model: Some("m".into()),
            host: Some("http://localhost:1".into()),
            engine: Some("lmstudio".into()),
        };

        {
            let _rollback = PendingInferenceRollback::at_path(&pending, pending_path.clone());
        }
        assert!(!pending_path.exists());

        let confirmed_path = root.join("confirmed.json");
        std::fs::write(&confirmed_path, "confirmed").unwrap();
        let mut confirmed = pending;
        confirmed.confirmed = true;
        {
            let _rollback = PendingInferenceRollback::at_path(&confirmed, confirmed_path.clone());
        }
        assert!(confirmed_path.exists());

        let committed_path = root.join("committed.json");
        std::fs::write(&committed_path, "pending").unwrap();
        let mut staged = InferenceConfig {
            kind: SourceKind::Ollama,
            confirmed: false,
            model: Some("qwen3.5:4b".into()),
            host: None,
            engine: None,
        };
        {
            let mut rollback = PendingInferenceRollback::at_path(&staged, committed_path.clone());
            rollback.confirm(&mut staged).unwrap();
        }
        assert!(staged.confirmed);
        assert!(committed_path.exists());
        let committed: InferenceConfig =
            serde_json::from_str(&std::fs::read_to_string(&committed_path).unwrap()).unwrap();
        assert!(committed.confirmed);
        std::fs::remove_dir_all(root).unwrap();
    }

    #[test]
    fn pending_custom_key_is_staged_without_overwriting_existing_key() {
        let root = unique_test_root("stage-inference-key");
        std::fs::create_dir_all(&root).unwrap();
        let path = root.join("inference.json");
        let store = MemoryCredentialStore::default();
        store.put("LMSTUDIO_API_KEY", "existing-key");
        let cfg = InferenceConfig {
            kind: SourceKind::Custom,
            confirmed: false,
            model: Some("m".into()),
            host: Some("http://localhost:1234".into()),
            engine: Some("lmstudio".into()),
        };

        stage_pending_inference_config_at(&cfg, Some("new-key"), &store, &path).unwrap();

        assert_eq!(
            store.value("LMSTUDIO_API_KEY").as_deref(),
            Some("existing-key")
        );
        assert_eq!(
            store.value(PENDING_INFERENCE_API_KEY).as_deref(),
            Some("new-key")
        );
        let staged: InferenceConfig =
            serde_json::from_str(&std::fs::read_to_string(&path).unwrap()).unwrap();
        assert!(!staged.confirmed);
        std::fs::remove_dir_all(root).unwrap();
    }

    #[test]
    fn cancelled_pending_setup_discards_stage_and_preserves_existing_key() {
        let root = unique_test_root("cancel-inference-key");
        std::fs::create_dir_all(&root).unwrap();
        let path = root.join("inference.json");
        let store = std::sync::Arc::new(MemoryCredentialStore::default());
        store.put("LMSTUDIO_API_KEY", "existing-key");
        let cfg = InferenceConfig {
            kind: SourceKind::Custom,
            confirmed: false,
            model: Some("m".into()),
            host: Some("http://localhost:1234".into()),
            engine: Some("lmstudio".into()),
        };
        stage_pending_inference_config_at(&cfg, Some("new-key"), store.as_ref(), &path).unwrap();

        {
            let _rollback =
                PendingInferenceRollback::at_path_with_store(&cfg, path.clone(), store.clone());
        }

        assert!(!path.exists());
        assert_eq!(store.value(PENDING_INFERENCE_API_KEY), None);
        assert_eq!(
            store.value("LMSTUDIO_API_KEY").as_deref(),
            Some("existing-key")
        );
        std::fs::remove_dir_all(root).unwrap();
    }

    #[test]
    fn successful_pending_setup_promotes_stage_only_at_confirmation() {
        let root = unique_test_root("confirm-inference-key");
        std::fs::create_dir_all(&root).unwrap();
        let path = root.join("inference.json");
        let store = std::sync::Arc::new(MemoryCredentialStore::default());
        store.put("LMSTUDIO_API_KEY", "existing-key");
        let mut cfg = InferenceConfig {
            kind: SourceKind::Custom,
            confirmed: false,
            model: Some("m".into()),
            host: Some("http://localhost:1234".into()),
            engine: Some("lmstudio".into()),
        };
        stage_pending_inference_config_at(&cfg, Some("new-key"), store.as_ref(), &path).unwrap();

        {
            let mut rollback =
                PendingInferenceRollback::at_path_with_store(&cfg, path.clone(), store.clone());
            rollback.confirm(&mut cfg).unwrap();
        }

        assert!(cfg.confirmed);
        assert_eq!(store.value(PENDING_INFERENCE_API_KEY), None);
        assert_eq!(store.value("LMSTUDIO_API_KEY").as_deref(), Some("new-key"));
        let confirmed: InferenceConfig =
            serde_json::from_str(&std::fs::read_to_string(&path).unwrap()).unwrap();
        assert!(confirmed.confirmed);
        std::fs::remove_dir_all(root).unwrap();
    }

    #[test]
    fn failed_confirmation_restores_existing_key_and_leaves_no_stage() {
        let root = unique_test_root("failed-confirm-inference-key");
        let path = root.join("config-is-a-directory");
        std::fs::create_dir_all(&path).unwrap();
        let store = std::sync::Arc::new(MemoryCredentialStore::default());
        store.put("LMSTUDIO_API_KEY", "existing-key");
        store.put(PENDING_INFERENCE_API_KEY, "new-key");
        let mut cfg = InferenceConfig {
            kind: SourceKind::Custom,
            confirmed: false,
            model: Some("m".into()),
            host: Some("http://localhost:1234".into()),
            engine: Some("lmstudio".into()),
        };

        let result = {
            let mut rollback =
                PendingInferenceRollback::at_path_with_store(&cfg, path.clone(), store.clone());
            rollback.confirm(&mut cfg)
        };

        assert!(result.is_err());
        assert!(!cfg.confirmed);
        assert_eq!(store.value(PENDING_INFERENCE_API_KEY), None);
        assert_eq!(
            store.value("LMSTUDIO_API_KEY").as_deref(),
            Some("existing-key")
        );
        std::fs::remove_dir_all(root).unwrap();
    }

    #[test]
    fn failed_pending_config_write_discards_new_stage() {
        let root = unique_test_root("failed-stage-inference-key");
        let path = root.join("config-is-a-directory");
        std::fs::create_dir_all(&path).unwrap();
        let store = MemoryCredentialStore::default();
        store.put("LMSTUDIO_API_KEY", "existing-key");
        let cfg = InferenceConfig {
            kind: SourceKind::Custom,
            confirmed: false,
            model: Some("m".into()),
            host: Some("http://localhost:1234".into()),
            engine: Some("lmstudio".into()),
        };

        let result = stage_pending_inference_config_at(&cfg, Some("new-key"), &store, &path);

        assert!(result.is_err());
        assert_eq!(store.value(PENDING_INFERENCE_API_KEY), None);
        assert_eq!(
            store.value("LMSTUDIO_API_KEY").as_deref(),
            Some("existing-key")
        );
        std::fs::remove_dir_all(root).unwrap();
    }

    #[test]
    fn failed_confirmed_config_write_restores_existing_key() {
        let root = unique_test_root("failed-confirmed-inference-key");
        let path = root.join("config-is-a-directory");
        std::fs::create_dir_all(&path).unwrap();
        let store = MemoryCredentialStore::default();
        store.put("LMSTUDIO_API_KEY", "existing-key");
        let cfg = InferenceConfig {
            kind: SourceKind::Custom,
            confirmed: true,
            model: Some("m".into()),
            host: Some("http://localhost:1234".into()),
            engine: Some("lmstudio".into()),
        };

        let result = persist_confirmed_inference_config_at(&cfg, Some("new-key"), &store, &path);

        assert!(result.is_err());
        assert_eq!(
            store.value("LMSTUDIO_API_KEY").as_deref(),
            Some("existing-key")
        );
        std::fs::remove_dir_all(root).unwrap();
    }

    #[test]
    fn reset_discards_pending_config_and_stage_without_touching_existing_key() {
        let root = unique_test_root("reset-inference-key");
        std::fs::create_dir_all(&root).unwrap();
        let path = root.join("inference.json");
        std::fs::write(&path, "pending").unwrap();
        let store = MemoryCredentialStore::default();
        store.put("LMSTUDIO_API_KEY", "existing-key");
        store.put(PENDING_INFERENCE_API_KEY, "new-key");

        discard_pending_inference_setup_at(&path, &store).unwrap();

        assert!(!path.exists());
        assert_eq!(store.value(PENDING_INFERENCE_API_KEY), None);
        assert_eq!(
            store.value("LMSTUDIO_API_KEY").as_deref(),
            Some("existing-key")
        );
        std::fs::remove_dir_all(root).unwrap();
    }

    #[tokio::test]
    async fn ready_port_squatter_never_receives_cloud_key_without_owned_child() {
        let listener = std::net::TcpListener::bind("127.0.0.1:0").unwrap();
        listener.set_nonblocking(true).unwrap();
        let reload_url = format!("http://{}/v1/cloud/reload", listener.local_addr().unwrap());
        let backend = std::sync::Arc::new(tokio::sync::Mutex::new(BackendManager::default()));
        let mut setup_status = SetupStatus::default();
        setup_status.server_ready = true;
        let status = std::sync::Arc::new(tokio::sync::Mutex::new(setup_status));

        reload_cloud_keys_for_owned_backend_at(
            &backend,
            &status,
            vec![("OPENAI_API_KEY".into(), "must-not-leak".into())],
            &reload_url,
        )
        .await;

        let error = listener.accept().unwrap_err();
        assert_eq!(error.kind(), std::io::ErrorKind::WouldBlock);
    }

    #[tokio::test]
    async fn stopping_backend_aborts_the_tracked_boot_task() {
        use std::sync::atomic::{AtomicBool, Ordering};
        use std::sync::Arc;

        struct DropSignal(Arc<AtomicBool>);
        impl Drop for DropSignal {
            fn drop(&mut self) {
                self.0.store(true, Ordering::SeqCst);
            }
        }

        let dropped = Arc::new(AtomicBool::new(false));
        let signal = DropSignal(dropped.clone());
        let task = tokio::spawn(async move {
            let _signal = signal;
            std::future::pending::<()>().await;
        });
        tokio::task::yield_now().await;

        let mut manager = BackendManager::default();
        manager.boot_task = Some(tauri::async_runtime::JoinHandle::Tokio(task));
        manager.stop_all().await;

        assert!(manager.boot_task.is_none());
        assert!(
            dropped.load(Ordering::SeqCst),
            "stop_all must not return before the aborted boot future is dropped"
        );
    }

    #[test]
    fn owned_child_process_helper() {
        let Some(started) = std::env::var_os("OPENJARVIS_OWNED_CHILD_STARTED") else {
            return;
        };
        let completed = std::env::var_os("OPENJARVIS_OWNED_CHILD_COMPLETED").unwrap();
        std::fs::write(started, "started").unwrap();
        std::thread::sleep(std::time::Duration::from_millis(500));
        std::fs::write(completed, "completed").unwrap();
    }

    #[tokio::test]
    async fn aborting_boot_kills_child_before_manager_registration() {
        let unique = std::time::SystemTime::now()
            .duration_since(std::time::UNIX_EPOCH)
            .unwrap()
            .as_nanos();
        let root = std::env::temp_dir().join(format!(
            "openjarvis-owned-child-{}-{unique}",
            std::process::id()
        ));
        std::fs::create_dir_all(&root).unwrap();
        let started = root.join("started");
        let completed = root.join("completed");

        let (spawned_tx, spawned_rx) = tokio::sync::oneshot::channel();
        let started_for_child = started.clone();
        let completed_for_child = completed.clone();
        let task = tokio::spawn(async move {
            let mut cmd = tokio::process::Command::new(std::env::current_exe().unwrap());
            cmd.args([
                "--exact",
                "tests::owned_child_process_helper",
                "--nocapture",
            ])
            .env("OPENJARVIS_OWNED_CHILD_STARTED", started_for_child)
            .env("OPENJARVIS_OWNED_CHILD_COMPLETED", completed_for_child)
            .stdout(std::process::Stdio::null())
            .stderr(std::process::Stdio::null());
            let child = spawn_owned_child(&mut cmd).unwrap();
            spawned_tx.send(()).unwrap();
            let _unregistered_child = child;
            std::future::pending::<()>().await;
        });
        spawned_rx.await.unwrap();

        for _ in 0..100 {
            if started.exists() {
                break;
            }
            tokio::time::sleep(std::time::Duration::from_millis(10)).await;
        }
        assert!(started.exists(), "helper process did not start");

        task.abort();
        let _ = task.await;
        tokio::time::sleep(std::time::Duration::from_millis(700)).await;

        assert!(
            !completed.exists(),
            "an aborted boot task left its not-yet-registered child running"
        );
        std::fs::remove_dir_all(root).unwrap();
    }

    #[test]
    fn boot_plan_ollama_uses_fallback_model_on_low_ram() {
        // Below the smallest model's min_ram â†’ default_local_model â†’ FALLBACK_MODEL.
        let cfg = InferenceConfig {
            kind: SourceKind::Ollama,
            ..Default::default()
        };
        let plan = boot_plan(&cfg, 1.0);
        assert_eq!(plan.model_to_pull.as_deref(), Some(super::FALLBACK_MODEL));
    }

    #[test]
    fn upsert_engine_host_writes_into_empty_config() {
        let out = upsert_engine_host("", "lmstudio", "http://localhost:1234").unwrap();
        let doc: toml_edit::DocumentMut = out.parse().unwrap();
        assert_eq!(
            doc["engine"]["lmstudio"]["host"].as_str(),
            Some("http://localhost:1234")
        );
    }

    #[test]
    fn upsert_engine_host_preserves_existing_content() {
        let existing = "[intelligence]\ndefault_model = \"keep-me\"\n";
        let out = upsert_engine_host(existing, "vllm", "http://host:8000").unwrap();
        let doc: toml_edit::DocumentMut = out.parse().unwrap();
        assert_eq!(
            doc["intelligence"]["default_model"].as_str(),
            Some("keep-me")
        );
        assert_eq!(
            doc["engine"]["vllm"]["host"].as_str(),
            Some("http://host:8000")
        );
    }

    #[test]
    fn upsert_engine_host_updates_existing_host() {
        let existing = "[engine.lmstudio]\nhost = \"http://old:1\"\n";
        let out = upsert_engine_host(existing, "lmstudio", "http://new:2").unwrap();
        let doc: toml_edit::DocumentMut = out.parse().unwrap();
        assert_eq!(
            doc["engine"]["lmstudio"]["host"].as_str(),
            Some("http://new:2")
        );
    }

    // -----------------------------------------------------------------
    // #455 â€” AppImage subprocess env-strip helper
    // -----------------------------------------------------------------
    //
    // `prepare_subprocess_for_appimage` strips LD_LIBRARY_PATH (and the
    // related AppImage runtime variables) from a child `Command` ONLY
    // when the parent process is itself running inside an AppImage â€”
    // detected by the presence of the `APPIMAGE` env variable that the
    // AppImage runtime sets to the original .AppImage path. We can't
    // observe the env_remove calls directly through tokio's Command
    // API (it doesn't expose its env map publicly), so these tests
    // exercise the documented contract on each platform:
    //
    //   * on macOS / Windows: the function is a no-op regardless of env.
    //   * on Linux without $APPIMAGE: also a no-op.
    //   * on Linux with $APPIMAGE: it doesn't panic, doesn't return an
    //     error, and the calling code that follows succeeds. The
    //     observable behaviour test is the integration repro on a real
    //     AppImage build (covered in PR test plan).
    //
    // The Mutex serialises any test that touches the process-wide
    // `APPIMAGE` env var so cargo test's parallel runner can't race two
    // tests setting and unsetting it concurrently. `static Mutex` works
    // on a const path since Rust 1.63 (and Tauri's MSRV is well above).

    static APPIMAGE_ENV_LOCK: std::sync::Mutex<()> = std::sync::Mutex::new(());

    // Pick a binary that exists on every test target so the test body is
    // doing something other than constructing an obviously-broken command
    // path on Windows.
    #[cfg(target_os = "windows")]
    const HARMLESS_BIN: &str = "cmd";
    #[cfg(not(target_os = "windows"))]
    const HARMLESS_BIN: &str = "/bin/true";

    #[test]
    fn prepare_subprocess_for_appimage_no_appimage_is_safe() {
        let _guard = APPIMAGE_ENV_LOCK.lock().unwrap_or_else(|e| e.into_inner());
        let prev = std::env::var_os("APPIMAGE");
        // SAFETY: APPIMAGE_ENV_LOCK serialises every test that touches
        // this env var, so the mutation is single-threaded for the
        // duration of the lock. The 2024-edition env mutation rules
        // require the `unsafe` block but the guard makes it sound.
        unsafe {
            std::env::remove_var("APPIMAGE");
        }
        let mut cmd = tokio::process::Command::new(HARMLESS_BIN);
        super::prepare_subprocess_for_appimage(&mut cmd);
        if let Some(v) = prev {
            unsafe {
                std::env::set_var("APPIMAGE", v);
            }
        }
    }

    #[cfg(target_os = "linux")]
    #[test]
    fn prepare_subprocess_for_appimage_with_appimage_set_is_safe() {
        let _guard = APPIMAGE_ENV_LOCK.lock().unwrap_or_else(|e| e.into_inner());
        let prev = std::env::var_os("APPIMAGE");
        unsafe {
            std::env::set_var("APPIMAGE", "/tmp/test.AppImage");
        }
        let mut cmd = tokio::process::Command::new(HARMLESS_BIN);
        super::prepare_subprocess_for_appimage(&mut cmd);
        unsafe {
            if let Some(v) = prev {
                std::env::set_var("APPIMAGE", v);
            } else {
                std::env::remove_var("APPIMAGE");
            }
        }
    }
}


## ===== frontend/src-tauri/tauri.conf.json : OUR COMMITS SINCE AUTHOR BASE =====
c1c940c3 fix(W63): remove remote-debugging-port 9222 from tauri.conf.json; reinstall desktop app from current bundle; W63 BRIEF + ARCHIVE
0389255b TTS: AudioContext playback engine + ChatArea driver rewrite; mailbox IMAP connector and tools; speech/CSP fixes
d472bc91 fix: add media-src blob to CSP, debug TTS logs, unlock WebView2 autoplay - Jarvis now speaks
ef2c754e fix: add WebView2 autoplay and mic permission flags to tauri.conf.json
bc498a16 feat: Arc Reactor ThinkingCircle, fix env loading, fix project root, add research types, remove debug code

## ===== frontend/src-tauri/tauri.conf.json : CONFLICTED WORKING FILE (diff3) =====
{
  "$schema": "https://schema.tauri.app/config/2",
  "productName": "OpenJarvis",
  "version": "0.1.0",
  "identifier": "com.openjarvis.desktop",
  "build": {
    "frontendDist": "../../src/openjarvis/server/static",
    "devUrl": "http://localhost:5173",
    "beforeDevCommand": "npm run dev",
    "beforeBuildCommand": "npm run build:tauri"
  },
  "app": {
    "windows": [
      {
        "title": "OpenJarvis",
        "width": 1280,
        "height": 800,
        "minWidth": 900,
        "minHeight": 600,
        "resizable": true,
        "fullscreen": false,
        "decorations": true,
        "transparent": false,
        "devtools": true,
        "additionalBrowserArgs": "--autoplay-policy=no-user-gesture-required --use-fake-ui-for-media-stream"
      }
    ],
    "security": {
<<<<<<< ours
      "csp": "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; connect-src 'self' http://localhost:* http://127.0.0.1:* http://172.16.33.200:* ws://localhost:* ws://127.0.0.1:* http://ipc.localhost; img-src 'self' data: blob:; media-src blob: data:"
||||||| base
      "csp": "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; connect-src 'self' http://localhost:* http://127.0.0.1:* ws://localhost:* ws://127.0.0.1:*; img-src 'self' data: blob:"
=======
      "csp": "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; connect-src 'self' http: https: ws: wss:; img-src 'self' data: blob:"
>>>>>>> theirs
    }
  },
  "bundle": {
    "active": true,
    "targets": "all",
    "createUpdaterArtifacts": false,
    "icon": [
      "icons/32x32.png",
      "icons/128x128.png",
      "icons/128x128@2x.png",
      "icons/icon.icns",
      "icons/icon.ico",
      "icons/icon.png"
    ],
    "category": "Utility",
    "shortDescription": "On-device AI assistant with energy monitoring and trace debugging",
    "longDescription": "OpenJarvis Desktop wraps the OpenJarvis research framework in a native desktop application with real-time energy monitoring, trace debugging, learning curve visualization, and memory browsing.",
    "macOS": {
      "entitlements": "Entitlements.plist",
      "minimumSystemVersion": "10.15",
      "frameworks": [],
      "providerShortName": null,
      "signingIdentity": "-"
    },
    "windows": {
      "certificateThumbprint": null,
      "digestAlgorithm": "sha256",
      "timestampUrl": "http://timestamp.digicert.com"
    }
  },
  "plugins": {
    "updater": {
      "active": false,
      "pubkey": "dW50cnVzdGVkIGNvbW1lbnQ6IG1pbmlzaWduIHB1YmxpYyBrZXk6IDFFNzUzMzhEOEY2MjNEMDMKUldRRFBXS1BqVE4xSG8vK0lkUWN4WnZQYVIrbmc4RmpoOGlJWTBLTE15RlIya3JvQisvdUR3a0QK",
      "endpoints": []
    },
    "deep-link": {
      "desktop": {
        "schemes": [
          "openjarvis"
        ]
      }
    }
  }
}

## ===== frontend/src/App.tsx : OUR COMMITS SINCE AUTHOR BASE =====
2490f945 Move ConfirmPrompt to App.tsx so confirm UI survives route changes; clear two user-visible mojibake strings in ChatArea
bc498a16 feat: Arc Reactor ThinkingCircle, fix env loading, fix project root, add research types, remove debug code

## ===== frontend/src/App.tsx : CONFLICTED WORKING FILE (diff3) =====
import { useEffect, useState, useCallback, useRef } from 'react';
import { Routes, Route } from 'react-router';
import { Layout } from './components/Layout';
import { ChatPage } from './pages/ChatPage';
import { DashboardPage } from './pages/DashboardPage';
import { SettingsPage } from './pages/SettingsPage';
import { GetStartedPage } from './pages/GetStartedPage';
import { AgentsPage } from './pages/AgentsPage';
import { DataSourcesPage } from './pages/DataSourcesPage';
import { LogsPage } from './pages/LogsPage';
import { CommandPalette } from './components/CommandPalette';
import { SetupScreen } from './components/SetupScreen';
import { Toaster } from './components/ui/sonner';
import { useAppStore } from './lib/store';
import { fetchModels, fetchServerInfo, fetchSavings, submitSavings, isTauri } from './lib/api';
import { OptInModal } from './components/OptInModal';
<<<<<<< ours
// openjarvis-confirm-app-v1
import { ConfirmPrompt } from './components/Chat/ConfirmPrompt';
||||||| base
import { track, hashId } from './lib/analytics';
=======
import { UpdateChecker } from './components/Desktop/UpdateChecker';
import { track, hashId } from './lib/analytics';
>>>>>>> theirs

export default function App() {
  const [setupDone, setSetupDone] = useState(!isTauri());
<<<<<<< ours
  const handleSetupReady = useCallback(() => setSetupDone(true), []);
||||||| base
  const handleSetupReady = useCallback(() => {
    setSetupDone(true);
    track('setup_completed', { preset: 'default' });
  }, []);
  const prevModelRef = useRef<string>('');
=======
  const handleSetupReady = useCallback(() => {
    setSetupDone(true);
    // Only fire once per install â€” guard against setup screen re-appearing
    // on reinstalls or dev reloads.
    if (!localStorage.getItem('oj-setup-completed')) {
      localStorage.setItem('oj-setup-completed', '1');
      track('setup_completed', { preset: 'default' });
    }
  }, []);
  const prevModelRef = useRef<string>('');
>>>>>>> theirs
  const setModels = useAppStore((s) => s.setModels);
  const setModelsLoading = useAppStore((s) => s.setModelsLoading);
  const selectedModel = useAppStore((s) => s.selectedModel);
  const setServerInfo = useAppStore((s) => s.setServerInfo);
  const setSavings = useAppStore((s) => s.setSavings);
  const settings = useAppStore((s) => s.settings);
  const commandPaletteOpen = useAppStore((s) => s.commandPaletteOpen);
  const setCommandPaletteOpen = useAppStore((s) => s.setCommandPaletteOpen);
  const optInEnabled = useAppStore((s) => s.optInEnabled);
  const optInDisplayName = useAppStore((s) => s.optInDisplayName);
  const optInEmail = useAppStore((s) => s.optInEmail);
  const optInAnonId = useAppStore((s) => s.optInAnonId);
  const optInModalSeen = useAppStore((s) => s.optInModalSeen);
  const optInModalOpen = useAppStore((s) => s.optInModalOpen);
  const setOptInModalOpen = useAppStore((s) => s.setOptInModalOpen);
  const markOptInModalSeen = useAppStore((s) => s.markOptInModalSeen);
  const savings = useAppStore((s) => s.savings);

  // Apply theme class to <html>
  useEffect(() => {
    const root = document.documentElement;
    root.classList.remove('dark', 'light');
    if (settings.theme === 'dark') root.classList.add('dark');
    else if (settings.theme === 'light') root.classList.add('light');
  }, [settings.theme]);

  // Sync overlay conversations into the main app
  const importOverlay = useAppStore((s) => s.importOverlayConversation);
  useEffect(() => {
    if (!isTauri()) return;
    importOverlay();
    const interval = setInterval(importOverlay, 5000);
    return () => clearInterval(interval);
  }, [importOverlay]);

  // Fetch models on mount
  useEffect(() => {
    fetchModels()
      .then((m) => {
        setModels(m);
      })
      .catch(() => setModels([]))
      .finally(() => setModelsLoading(false));
  }, []); // eslint-disable-line react-hooks/exhaustive-deps

  // Fetch server info
  useEffect(() => {
    fetchServerInfo().then(setServerInfo).catch(() => {});
  }, []); // eslint-disable-line react-hooks/exhaustive-deps

  // Poll savings and optionally share to Supabase
  useEffect(() => {
    const refresh = () =>
      fetchSavings()
        .then((data) => {
          setSavings(data);
          if (optInEnabled && optInDisplayName && data) {
            const claudeEntry = data.per_provider.find(
              (p) => p.provider === 'claude-fable-5',
            );
            const dollarSavings = claudeEntry ? claudeEntry.total_cost : 0;
            const energySaved = data.per_provider.reduce(
              (sum, p) => sum + (p.energy_wh || 0),
              0,
            );
            const flopsSaved = data.per_provider.reduce(
              (sum, p) => sum + (p.flops || 0),
              0,
            );
            submitSavings({
              anon_id: optInAnonId,
              display_name: optInDisplayName,
              email: optInEmail,
              total_calls: data.total_calls,
              total_tokens: data.total_tokens,
              dollar_savings: dollarSavings,
              energy_wh_saved: energySaved,
              flops_saved: flopsSaved,
              token_counting_version: data.token_counting_version ?? 1,
            });
          }
        })
        .catch(() => {});
    refresh();
    const interval = setInterval(refresh, 30000);
    return () => clearInterval(interval);
  }, [optInEnabled, optInDisplayName, optInAnonId]); // eslint-disable-line react-hooks/exhaustive-deps

  // Show opt-in modal on first visit
  useEffect(() => {
    if (!optInModalSeen) {
      setOptInModalOpen(true);
      markOptInModalSeen();
    }
  }, []); // eslint-disable-line react-hooks/exhaustive-deps

  const toggleSystemPanel = useAppStore((s) => s.toggleSystemPanel);

  // Global keyboard shortcuts
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
        e.preventDefault();
        setCommandPaletteOpen(!commandPaletteOpen);
      }
      if ((e.metaKey || e.ctrlKey) && e.key === 'i') {
        e.preventDefault();
        toggleSystemPanel();
      }
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [commandPaletteOpen, setCommandPaletteOpen, toggleSystemPanel]);


  if (!setupDone) {
    return <SetupScreen onReady={handleSetupReady} />;
  }

  return (
    <>
      <UpdateChecker />
      <Routes>
        <Route element={<Layout />}>
          <Route index element={<ChatPage />} />
          <Route path="dashboard" element={<DashboardPage />} />
          <Route path="settings" element={<SettingsPage />} />
          <Route path="get-started" element={<GetStartedPage />} />
          <Route path="data-sources" element={<DataSourcesPage />} />
          <Route path="agents" element={<AgentsPage />} />
          <Route path="logs" element={<LogsPage />} />
        </Route>
      </Routes>
      <Toaster position="bottom-right" />
      {/* openjarvis-confirm-app-v1 - app level, survives route changes */}
      <ConfirmPrompt />
      {commandPaletteOpen && <CommandPalette />}
      {optInModalOpen && (
        <OptInModal onClose={() => setOptInModalOpen(false)} />
      )}
    </>
  );
}


## ===== frontend/src/components/Chat/ChatArea.tsx : OUR COMMITS SINCE AUTHOR BASE =====
63257bd7 W70 fixup: commit ChatArea.tsx liveness probe missed by cc21932 (git path is Chat\ capital C; lowercase pathspec matched nothing)
bff47ff0 W69: restore stop control lost in 0389255; diagnose UI freeze during generation; handoff
5a28afea W67: restore streaming voice - keepalive gain and first-clause release
2490f945 Move ConfirmPrompt to App.tsx so confirm UI survives route changes; clear two user-visible mojibake strings in ChatArea
73db0c1a W51: confirm prompt UI - render tool_confirm_request, POST approve/deny, dismiss on resolved. Verified live 09/12.
efc28e40 feat(tts): shrink first TTS chunk to 90 chars, keep driver instrumentation
0389255b TTS: AudioContext playback engine + ChatArea driver rewrite; mailbox IMAP connector and tools; speech/CSP fixes
e0e36523 Fix: wire tools to native_openhands agent - file_read, think, calculator, code_interpreter, shell_exec, file_write now loading at startup
daafc769 fix: speech subsystem TTS streaming, backend file logging, uvicorn console fix, restore .gitignore
670c3aaf feat: numbered question UI buttons, sub-bullet fix, trailing text relaxed, shell_exec utf-8 encoding, croniter installed, persistent API keys hydrate from Rust backend, fix: use npx tauri build for full Rust exe compile (npm run build:tauri is frontend only)
6015a448 feat: mic button fix, agent work, cloud router updates, HUD improvements
3782799b feat: speech subsystem, auto-focus, pyproject fixes, pynvml->nvidia-ml-py, startup scripts
bc498a16 feat: Arc Reactor ThinkingCircle, fix env loading, fix project root, add research types, remove debug code

## ===== frontend/src/components/Chat/ChatArea.tsx : CONFLICTED WORKING FILE (diff3) =====
import { useRef, useEffect, useState, useCallback } from 'react';
import { useNavigate } from 'react-router';
import { MessageBubble } from './MessageBubble';
import { InputArea } from './InputArea';
import { StreamingDots } from './StreamingDots';
import { useAppStore, generateId } from '../../lib/store';
import { ThinkingCircle } from '../ThinkingCircle';
import { Sparkles, PanelRightOpen, PanelRightClose, Database, MessageSquare, X, Volume2, VolumeX, Paperclip } from 'lucide-react';
import { listConnectors } from '../../lib/connectors-api';
import { fetchSavings } from '../../lib/api';
import { enqueue, stopAll } from '../../audio/ttsPlayer';
import { streamChat } from '../../lib/sse';
import type { ChatMessage, ToolCallInfo, TokenUsage, MessageTelemetry } from '../../types';

function formatBytes(b: number): string {
  if (b < 1024) return b + ' B';
  if (b < 1048576) return (b / 1024).toFixed(1) + ' KB';
  return (b / 1048576).toFixed(1) + ' MB';
}

function getGreeting(): string {
  const hour = new Date().getHours();
  if (hour < 12) return 'Good morning';
  if (hour < 18) return 'Good afternoon';
  return 'Good evening';
}

const MUTE_KEY = 'openjarvis_tts_muted';

export function ChatArea() {
  const activeId = useAppStore((s) => s.activeId);
  const messages = useAppStore((s) => s.messages);
  const streamState = useAppStore((s) => s.streamState);
  const systemPanelOpen = useAppStore((s) => s.systemPanelOpen);
  const toggleSystemPanel = useAppStore((s) => s.toggleSystemPanel);
  const navigate = useNavigate();
  const listRef = useRef<HTMLDivElement>(null);
  const shouldAutoScroll = useRef(true);
<<<<<<< ours
  const lastSpokenIdRef = useRef<string | null>(null);
  const hasMountedRef = useRef(false);
  const spokenCharsRef = useRef<number>(0);
  const sendAbortRef = useRef<AbortController | null>(null);
  const sendTimerRef = useRef<ReturnType<typeof setInterval> | null>(null);
||||||| base
=======
  const wasStreaming = useRef(false);
  const lastScrollTop = useRef(0);
  const isCurrentChatStreaming = streamState.isStreaming && streamState.conversationId === activeId;
  const currentStreamContent = isCurrentChatStreaming ? streamState.content : '';
>>>>>>> theirs

  const [hasConnectedSources, setHasConnectedSources] = useState<boolean | null>(null);
  const [bannerDismissed, setBannerDismissed] = useState(false);
  const [muted, setMuted] = useState<boolean>(() => {
    try { return localStorage.getItem(MUTE_KEY) === 'true'; } catch { return false; }
  });

  useEffect(() => {
    listConnectors()
      .then((list) => setHasConnectedSources(list.some((c) => c.connected)))
      .catch(() => setHasConnectedSources(null));
  }, []);

  useEffect(() => {
    // Sending a message always pins the view to the bottom, even if the
    // user had scrolled up to read earlier messages.
    if (isCurrentChatStreaming && !wasStreaming.current) {
      shouldAutoScroll.current = true;
    }
    wasStreaming.current = isCurrentChatStreaming;
    if (shouldAutoScroll.current && listRef.current) {
      listRef.current.scrollTop = listRef.current.scrollHeight;
    }
  }, [messages, currentStreamContent, isCurrentChatStreaming]);

  const handleScroll = () => {
    if (!listRef.current) return;
    const { scrollTop, scrollHeight, clientHeight } = listRef.current;
    const distance = scrollHeight - scrollTop - clientHeight;
    const scrolledUp = scrollTop < lastScrollTop.current;
    lastScrollTop.current = scrollTop;
    if (scrolledUp && distance >= 1) {
      // Any upward scroll away from the bottom stops autoscroll immediately,
      // so streaming content never fights the user (no jitter). Sub-1px
      // upward movement (elastic bounce settling at the bottom) is ignored.
      shouldAutoScroll.current = false;
    } else if (!scrolledUp) {
      // Re-engage when scrolled back to the bottom. < 2 rather than < 1:
      // at fractional zoom levels the at-bottom residual can reach 1px,
      // which would otherwise leave autoscroll permanently disengaged.
      shouldAutoScroll.current = distance < 2;
    }
  };

<<<<<<< ours
  const stopStreaming = useCallback(() => {
    const _s = useAppStore.getState();
    _s.addLogEntry({ timestamp: Date.now(), level: 'info', category: 'chat', message: '[STOP] pressed streaming=' + _s.streamState.isStreaming + ' abort=' + (sendAbortRef.current ? 'present' : 'null') });
    sendAbortRef.current?.abort();
    if (sendTimerRef.current) { clearInterval(sendTimerRef.current); sendTimerRef.current = null; }
    useAppStore.getState().resetStream();
    stopAll();
  }, []);

  const toggleMute = useCallback(() => {
    setMuted((prev) => {
      const next = !prev;
      try { localStorage.setItem(MUTE_KEY, String(next)); } catch {}
      if (next) stopAll();
      return next;
    });
  }, []);
||||||| base
  const isEmpty = messages.length === 0 && !streamState.isStreaming;
=======
  const isEmpty = messages.length === 0 && !isCurrentChatStreaming;
>>>>>>> theirs

  // -------------------------------------------------------------------------
  // W70 MAIN-THREAD LIVENESS PROBE (F-W69-FREEZE measurement)
  //
  // Two independent instruments on one readout:
  //   maxGap  - worst delay between 100ms setInterval ticks. Measures TASK
  //             SCHEDULING latency. A large gap means the main thread was
  //             blocked and could not run a queued macrotask - which is
  //             exactly what swallows the stop button click.
  //   minFPS  - lowest 1-second requestAnimationFrame rate seen. Measures
  //             PAINT liveness. Low FPS with small gaps means render churn,
  //             not a blocking task.
  //
  // Counters live in a ref so the measurement survives the freeze; the text
  // is only pushed to state on a stall or every 2s, so the probe itself adds
  // at most 0.5 renders/sec when idle. Readout is in the chat header.
  // -------------------------------------------------------------------------
  const probeRef = useRef({ last: 0, maxGap: 0, stalls: [] as number[], minFps: 999, ticks: 0 });
  const [probeText, setProbeText] = useState('probe armed');
  useEffect(() => {
    const p = probeRef.current;
    p.last = performance.now();
    let frames = 0;
    let fpsMark = performance.now();
    let raf = 0;
    const render = () => {
      setProbeText(
        'gap=' + p.maxGap + 'ms stalls=' + p.stalls.length +
        ' [' + p.stalls.slice(-5).join(',') + '] fps=' + (p.minFps === 999 ? '-' : p.minFps)
      );
    };
    const loop = () => {
      frames++;
      const now = performance.now();
      if (now - fpsMark >= 1000) {
        const fps = Math.round((frames * 1000) / (now - fpsMark));
        if (fps < p.minFps) p.minFps = fps;
        frames = 0;
        fpsMark = now;
      }
      raf = requestAnimationFrame(loop);
    };
    raf = requestAnimationFrame(loop);
    const id = setInterval(() => {
      const now = performance.now();
      const gap = Math.round(now - p.last);
      p.last = now;
      p.ticks += 1;
      if (gap > p.maxGap) p.maxGap = gap;
      if (gap >= 250) {
        p.stalls.push(gap);
        render();
      } else if (p.ticks % 20 === 0) {
        render();
      }
    }, 100);
    return () => { clearInterval(id); cancelAnimationFrame(raf); };
  }, []);

  const resetProbe = useCallback(() => {
    const p = probeRef.current;
    p.last = performance.now();
    p.maxGap = 0;
    p.stalls = [];
    p.minFps = 999;
    p.ticks = 0;
    setProbeText('probe armed');
  }, []);

  // -------------------------------------------------------------------------
  // TTS driver. ONE owner for the whole reply.
  //
  // The previous code had two effects competing over shared refs. The
  // mid-stream effect claimed lastSpokenIdRef as soon as it spoke its first
  // sentence; the post-stream effect then returned early because that id was
  // already claimed. Whatever was still unspoken when streaming ended fell
  // between them. All playback state now lives in ttsPlayer, so this effect
  // decides only WHAT text to hand over and WHEN.
  //
  // While streaming, hand over text up to the last completed sentence. Once
  // streaming ends, hand over everything remaining regardless of punctuation.
  // That final flush is what guarantees the last sentence is spoken, and it
  // works whether the store lands the final text and resetStream() in one
  // render or in two.
  // -------------------------------------------------------------------------
  useEffect(() => {
    const lastMsg = messages[messages.length - 1];

    // On mount, adopt whatever is already on screen as already spoken, so a
    // restored conversation is never read aloud. This is what hasMountedRef
    // was always for: it was declared and read but never assigned anywhere,
    // so the guard below it never opened and mid-stream TTS never ran once.
    if (!hasMountedRef.current) {
      hasMountedRef.current = true;
      if (lastMsg && lastMsg.role === 'assistant' && lastMsg.id) {
        lastSpokenIdRef.current = lastMsg.id;
        spokenCharsRef.current = (lastMsg.content || '').length;
      }
      return;
    }

    if (!lastMsg || lastMsg.role !== 'assistant' || !lastMsg.id) return;

    // A new reply cancels anything still queued from the previous one.
    if (lastMsg.id !== lastSpokenIdRef.current) {
      lastSpokenIdRef.current = lastMsg.id;
      spokenCharsRef.current = 0;
      stopAll();
    }

    const fullText = lastMsg.content || '';
    let take = fullText.length;
    console.log('[TTSDBG] run', Date.now(), 'stream=' + streamState.isStreaming, 'len=' + fullText.length, 'spoken=' + spokenCharsRef.current);

    if (streamState.isStreaming) {
      const unspoken = fullText.slice(spokenCharsRef.current);
      const sentenceEnd = /^[\s\S]*[.!?](?=\s)/;
      // First segment of a reply only: release at the earliest clause
      // boundary past 20 chars so audio starts before the sentence ends.
      const match = spokenCharsRef.current === 0
        ? (unspoken.match(/^[\s\S]{20,}?[.!?,;:](?=\s)/) || unspoken.match(sentenceEnd))
        : unspoken.match(sentenceEnd);
      if (!match) return;
      take = spokenCharsRef.current + match[0].length;
    }

    if (take <= spokenCharsRef.current) return;

    const segment = fullText.slice(spokenCharsRef.current, take);
    spokenCharsRef.current = take;

    // Consumed even while muted, so unmuting mid-reply does not replay text
    // that already went past on screen.
    if (muted) return;

    const plainText = segment
      .replace(/```[\s\S]*?```/g, 'code block.')
      .replace(/`[^`]+`/g, '')
      .replace(/[#*_~>]/g, '')
      .replace(/\[([^\]]+)\]\([^)]+\)/g, '$1')
      .trim();

    if (plainText) { console.log('[TTSDBG] enqueue', Date.now(), 'stream=' + streamState.isStreaming, 'seg=' + plainText.length, 'spoken=' + spokenCharsRef.current); enqueue(plainText); }
  }, [streamState.isStreaming, streamState.content, messages, muted]);

  // Relay numbered-option button clicks into InputArea's submit flow
  useEffect(() => {
    const handler = (e: Event) => {
      const text = (e as CustomEvent<string>).detail;
      if (!text) return;
      window.dispatchEvent(new CustomEvent('jarvis-submit-text', { detail: text }));
    };
    window.addEventListener('jarvis-option-select', handler);
    return () => window.removeEventListener('jarvis-option-select', handler);
  }, []);

  const handleSendMessage = useCallback(async (text: string, attachments?: { name: string; size: number; type: string }[]) => {
    const content = text.trim();
    if (!content && (!attachments || attachments.length === 0)) return;

    const s0 = useAppStore.getState();
    if (s0.streamState.isStreaming) return;

    let convId = s0.activeId;
    if (!convId) convId = s0.createConversation(s0.selectedModel);

    const userMsg: ChatMessage = {
      id: generateId(),
      role: 'user',
      content,
      timestamp: Date.now(),
      attachments: attachments && attachments.length > 0 ? attachments : undefined,
    };
    s0.addMessage(convId, userMsg);

    const apiMessages = useAppStore.getState().messages.map((m) => ({ role: m.role, content: m.content }));

    const assistantMsg: ChatMessage = {
      id: generateId(),
      role: 'assistant',
      content: '',
      timestamp: Date.now(),
    };
    s0.addMessage(convId, assistantMsg);

    const startTime = Date.now();
    sendTimerRef.current = setInterval(() => {
      useAppStore.getState().setStreamState({ elapsedMs: Date.now() - startTime });
    }, 100);

    const controller = new AbortController();
    sendAbortRef.current = controller;

    let acc = '';
    let usage: TokenUsage | undefined;
    let complexity: { score: number; tier: string; suggested_max_tokens: number } | undefined;
    const toolCalls: ToolCallInfo[] = [];
    let lastFlush = 0;
    let ttftMs: number | undefined;

    const st = useAppStore.getState();
    st.setStreamState({ isStreaming: true, phase: 'Generating...', elapsedMs: 0, activeToolCalls: [], content: '' });
    st.addLogEntry({ timestamp: Date.now(), level: 'info', category: 'chat', message: 'Request: ' + content.slice(0, 80) });

    try {
      for await (const sseEvent of streamChat(
        {
          model: st.selectedModel,
          messages: apiMessages,
          stream: true,
          temperature: st.settings.temperature,
          max_tokens: st.settings.maxTokens,
          agent: st.selectedAgentId || '',
        },
        controller.signal,
      )) {
        const eventName = sseEvent.event;
        if (eventName === 'agent_turn_start') {
          useAppStore.getState().setStreamState({ phase: 'Agent thinking...' });
        } else if (eventName === 'inference_start') {
          useAppStore.getState().setStreamState({ phase: 'Generating...' });
        } else if (eventName === 'tool_call_start') {
          try {
            const data = JSON.parse(sseEvent.data);
            toolCalls.push({ id: generateId(), tool: data.tool, arguments: data.arguments || '', status: 'running' });
            useAppStore.getState().setStreamState({ phase: 'Calling ' + data.tool + '...', activeToolCalls: [...toolCalls] });
            useAppStore.getState().updateLastAssistant(convId, acc, [...toolCalls]);
          } catch (e) { void e; }
        } else if (eventName === 'tool_call_end') {
          try {
            const data = JSON.parse(sseEvent.data);
            const tc = toolCalls.find((t) => t.tool === data.tool && t.status === 'running');
            if (tc) {
              tc.status = data.success ? 'success' : 'error';
              tc.latency = data.latency;
              tc.result = data.result;
            }
            useAppStore.getState().setStreamState({ phase: 'Generating...', activeToolCalls: [...toolCalls] });
            useAppStore.getState().updateLastAssistant(convId, acc, [...toolCalls]);
          } catch (e) { void e; }
        } else {
          try {
            const data = JSON.parse(sseEvent.data);
            const delta = data.choices?.[0]?.delta;
            if (data.usage) usage = data.usage;
            if (data.complexity) complexity = data.complexity;
            if (delta?.content) {
              if (!ttftMs) ttftMs = Date.now() - startTime;
              acc += delta.content;
              useAppStore.getState().setStreamState({ content: acc, phase: '' });
              const now = Date.now();
              if (now - lastFlush >= 80) {
                useAppStore.getState().updateLastAssistant(convId, acc, toolCalls.length > 0 ? [...toolCalls] : undefined, undefined, undefined, undefined, false);
                lastFlush = now;
              }
            }
            if (data.choices?.[0]?.finish_reason === 'stop') break;
          } catch (e) { void e; }
        }
      }
    } catch (err) {
      const anyErr = err as { name?: string; message?: string };
      if (anyErr?.name === 'AbortError') {
        useAppStore.getState().addLogEntry({ timestamp: Date.now(), level: 'info', category: 'chat', message: '[STOP] AbortError observed acc=' + acc.length });
        if (!acc) acc = '(Generation stopped)';
      } else {
        const errMsg = anyErr?.message || String(err);
        acc = acc || ('Error: ' + errMsg);
        useAppStore.getState().addLogEntry({ timestamp: Date.now(), level: 'error', category: 'chat', message: 'Stream error: ' + errMsg });
      }
    } finally {
      if (!acc) acc = 'No response was generated. Please try again.';
      const totalMs = Date.now() - startTime;
      const telemetry: MessageTelemetry = {
        engine: 'mcp',
        model_id: st.selectedModel,
        total_ms: totalMs,
        ttft_ms: ttftMs,
        tokens_per_sec: usage?.completion_tokens ? usage.completion_tokens / (totalMs / 1000) : undefined,
        complexity_score: complexity?.score,
        complexity_tier: complexity?.tier,
        suggested_max_tokens: complexity?.suggested_max_tokens,
      };
      useAppStore.getState().updateLastAssistant(convId, acc, toolCalls.length > 0 ? toolCalls : undefined, usage, telemetry);
      if (sendTimerRef.current) { clearInterval(sendTimerRef.current); sendTimerRef.current = null; }
      useAppStore.getState().addLogEntry({ timestamp: Date.now(), level: 'info', category: 'chat', message: '[STOP] stream end acc=' + acc.length + ' elapsed=' + (Date.now() - startTime) + 'ms' });
      useAppStore.getState().resetStream();
      useAppStore.getState().addLogEntry({ timestamp: Date.now(), level: 'info', category: 'chat', message: 'Response: ' + acc.length + ' chars' });
      sendAbortRef.current = null;
      fetchSavings().then((d) => useAppStore.getState().setSavings(d)).catch(() => {});
    }
  }, []);

  const isEmpty = messages.length === 0 && !streamState.isStreaming;
  const PanelIcon = systemPanelOpen ? PanelRightClose : PanelRightOpen;

  return (
    <div className="flex flex-col h-full">
      <div className="flex items-center justify-end px-3 py-1.5 shrink-0 gap-1">
        {/* W70 main-thread liveness readout */}
        <span
          onClick={resetProbe}
          title="Main-thread probe. gap = worst setInterval delay (thread blocked). fps = lowest 1s frame rate (paint). Click to reset."
          className="mr-auto px-2 py-0.5 rounded text-[10px] font-mono cursor-pointer select-none"
          style={{
            color: probeRef.current.stalls.length > 0 ? 'var(--color-accent)' : 'var(--color-text-tertiary)',
            background: 'var(--color-bg-secondary)',
            border: '1px solid var(--color-border)',
          }}
        >
          {probeText}
        </span>
        {/* Mute toggle */}
        <button
          onClick={toggleMute}
          className="p-1.5 rounded-md transition-colors cursor-pointer"
          style={{ color: muted ? 'var(--color-text-tertiary)' : 'var(--color-accent)' }}
          title={muted ? 'Unmute Jarvis voice' : 'Mute Jarvis voice'}
        >
          {muted ? <VolumeX size={16} /> : <Volume2 size={16} />}
        </button>
        <button
          onClick={toggleSystemPanel}
          className="p-1.5 rounded-md transition-colors cursor-pointer"
          style={{ color: 'var(--color-text-tertiary)' }}
          title={`${systemPanelOpen ? 'Hide' : 'Show'} system panel (${navigator.platform.includes('Mac') ? 'Cmd' : 'Ctrl'}+I)`}
        >
          <PanelIcon size={16} />
        </button>
      </div>

      {hasConnectedSources === false && !bannerDismissed && (
        <div
          className="mx-4 mb-2 flex items-center gap-3 px-4 py-3 rounded-lg text-sm shrink-0"
          style={{
            background: 'var(--color-accent-subtle)',
            border: '1px solid var(--color-border)',
          }}
        >
          <Database size={16} style={{ color: 'var(--color-accent)', flexShrink: 0 }} />
          <span style={{ color: 'var(--color-text-secondary)', flex: 1 }}>
            Connect your data sources (Gmail, iMessage, Slack, etc.) to get personalized answers.
          </span>
          <button
            onClick={() => navigate('/data-sources')}
            className="px-3 py-1 rounded text-xs font-medium cursor-pointer"
            style={{ background: 'var(--color-accent)', color: 'var(--color-on-accent)', border: 'none' }}
          >
            Connect
          </button>
          <button
            onClick={() => setBannerDismissed(true)}
            className="p-1 rounded cursor-pointer"
            style={{ color: 'var(--color-text-tertiary)', background: 'transparent', border: 'none' }}
          >
            <X size={14} />
          </button>
        </div>
      )}

      <div
        ref={listRef}
        onScroll={handleScroll}
        className="flex-1 overflow-y-auto"
        style={{ paddingBottom: '0.5rem' }}
      >
        {isEmpty ? (
          <div className="flex flex-col items-center justify-center h-full px-4">
            <div
              className="w-12 h-12 rounded-2xl flex items-center justify-center mb-4"
              style={{ background: 'var(--color-accent-subtle)', color: 'var(--color-accent)' }}
            >
              <Sparkles size={24} />
            </div>
            <h2 className="text-xl font-semibold mb-2" style={{ color: 'var(--color-text)' }}>
              {getGreeting()}
            </h2>
            <p className="text-sm text-center max-w-sm mb-6" style={{ color: 'var(--color-text-secondary)' }}>
              Ask anything. Your AI runs locally - private, fast, and always available.
            </p>

            <div className="flex gap-3">
              <button
                onClick={() => navigate('/data-sources')}
                className="flex items-center gap-2 px-4 py-2.5 rounded-lg text-xs cursor-pointer transition-colors"
                style={{
                  background: 'var(--color-bg-secondary)',
                  border: '1px solid var(--color-border)',
                  color: 'var(--color-text-secondary)',
                }}
                onMouseEnter={(e) => (e.currentTarget.style.borderColor = 'var(--color-accent)')}
                onMouseLeave={(e) => (e.currentTarget.style.borderColor = 'var(--color-border)')}
              >
                <Database size={14} style={{ color: 'var(--color-accent)' }} />
                Connect Data Sources
              </button>
              <button
                onClick={() => { navigate('/data-sources'); setTimeout(() => window.dispatchEvent(new CustomEvent('switch-tab', { detail: 'messaging' })), 100); }}
                className="flex items-center gap-2 px-4 py-2.5 rounded-lg text-xs cursor-pointer transition-colors"
                style={{
                  background: 'var(--color-bg-secondary)',
                  border: '1px solid var(--color-border)',
                  color: 'var(--color-text-secondary)',
                }}
                onMouseEnter={(e) => (e.currentTarget.style.borderColor = 'var(--color-accent)')}
                onMouseLeave={(e) => (e.currentTarget.style.borderColor = 'var(--color-border)')}
              >
                <MessageSquare size={14} style={{ color: 'var(--color-accent)' }} />
                Set Up Messaging Channels
              </button>
            </div>
          </div>
        ) : (
<<<<<<< ours
          <div className="max-w-[var(--chat-max-width)] mx-auto px-4 py-4 pb-2">
            {messages.map((msg) => (
              <div key={msg.id}>
                <MessageBubble message={msg} />
                {msg.attachments && msg.attachments.length > 0 && (
                  <div className='flex flex-wrap gap-2 justify-end mb-4 px-1'>
                    {msg.attachments.map((att, ai) => (
                      <div
                        key={ai}
                        className='flex items-center gap-2 px-3 py-1.5 rounded-lg text-xs'
                        style={{ background: 'var(--color-accent-subtle)', border: '1px solid var(--color-border)', color: 'var(--color-text-secondary)' }}
                      >
                        <Paperclip size={12} />
                        <span className='truncate max-w-[180px]'>{att.name}</span>
                        <span style={{ color: 'var(--color-text-tertiary)' }}>{formatBytes(att.size)}</span>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            ))}
            {streamState.isStreaming && streamState.content === '' && (
              <div className="flex justify-start mb-4">
                <StreamingDots phase={streamState.phase} />
              </div>
            )}
||||||| base
          <div className="max-w-[var(--chat-max-width)] mx-auto px-4 py-6">
            {messages.map((msg, i) => {
              const isLastAssistant =
                i === messages.length - 1 && msg.role === 'assistant';
              return (
                <MessageBubble
                  key={msg.id}
                  message={msg}
                  isLive={isLastAssistant && streamState.isStreaming}
                />
              );
            })}
            {(() => {
              if (!streamState.isStreaming || streamState.content !== '') return null;
              // For research messages the ResearchTimeline handles its own
              // pre-content loading state â€” suppress the generic dots.
              const last = messages[messages.length - 1];
              if (last?.role === 'assistant' && last.isResearch) return null;
              return (
                <div className="flex justify-start mb-4">
                  <StreamingDots phase={streamState.phase} />
                </div>
              );
            })()}
=======
          <div className="max-w-[var(--chat-max-width)] mx-auto px-4 py-6">
            {messages.map((msg, i) => {
              const isLastAssistant =
                i === messages.length - 1 && msg.role === 'assistant';
              return (
                <MessageBubble
                  key={msg.id}
                  message={msg}
                  isLive={isLastAssistant && isCurrentChatStreaming}
                />
              );
            })}
            {(() => {
              if (!isCurrentChatStreaming || streamState.content !== '') return null;
              // For research messages the ResearchTimeline handles its own
              // pre-content loading state â€” suppress the generic dots.
              const last = messages[messages.length - 1];
              if (last?.role === 'assistant' && last.isResearch) return null;
              return (
                <div className="flex justify-start mb-4">
                  <StreamingDots phase={streamState.phase} />
                </div>
              );
            })()}
>>>>>>> theirs
          </div>
        )}
      </div>

      {/* ThinkingCircle component */}
      <div style={{ position: 'fixed', top: 120, right: 20, zIndex: 999998 }}>
        <ThinkingCircle
          isLoading={streamState.isStreaming}
          phase={streamState.isStreaming ? "processing..." : undefined}
          variant="cyan"
        />
      </div>

      <div style={{ paddingBottom: '0.75rem' }}>
        <InputArea onSendMessage={handleSendMessage} onStopGeneration={stopStreaming} />
      </div>
    </div>
  );
}


## ===== frontend/src/components/Chat/InputArea.tsx : OUR COMMITS SINCE AUTHOR BASE =====
bff47ff0 W69: restore stop control lost in 0389255; diagnose UI freeze during generation; handoff
0389255b TTS: AudioContext playback engine + ChatArea driver rewrite; mailbox IMAP connector and tools; speech/CSP fixes
e0e36523 Fix: wire tools to native_openhands agent - file_read, think, calculator, code_interpreter, shell_exec, file_write now loading at startup
670c3aaf feat: numbered question UI buttons, sub-bullet fix, trailing text relaxed, shell_exec utf-8 encoding, croniter installed, persistent API keys hydrate from Rust backend, fix: use npx tauri build for full Rust exe compile (npm run build:tauri is frontend only)
3782799b feat: speech subsystem, auto-focus, pyproject fixes, pynvml->nvidia-ml-py, startup scripts
2e1c5a4d feat: chat input improvements
bc498a16 feat: Arc Reactor ThinkingCircle, fix env loading, fix project root, add research types, remove debug code
f2fcb30c Graystone Lab: remote MCP/Ollama integration, Rust extension, UI fixes

## ===== frontend/src/components/Chat/InputArea.tsx : CONFLICTED WORKING FILE (diff3) =====
<<<<<<< ours
ï»¿// frontend/src/components/Chat/InputArea.tsx
// Updated to use useSpeechStream hook for WebSocket streaming STT
||||||| base
import { useState, useRef, useCallback, useEffect } from 'react';
import { Send, Square, Paperclip, Search } from 'lucide-react';
import { useAppStore, generateId } from '../../lib/store';
import { streamChat, streamResearch } from '../../lib/sse';
import { fetchSavings, getBase } from '../../lib/api';
import { listConnectors, getSyncStatus } from '../../lib/connectors-api';
import { MicButton } from './MicButton';
import { useSpeech } from '../../hooks/useSpeech';
import type {
  ChatMessage,
  MessageTelemetry,
  ResearchSearchTrace,
  ResearchSource,
  TokenUsage,
  ToolCallInfo,
} from '../../types';

// While Deep Research is toggled on, poll connected sources for sync
// progress so we can surface "Searching over N items â€” sync in progress"
// next to the toggle. Polling is gated on `enabled` so toggling DR off
// stops the network chatter immediately.
function useResearchCorpusSync(enabled: boolean): {
  syncing: boolean;
  itemsSynced: number;
} {
  const [state, setState] = useState({ syncing: false, itemsSynced: 0 });
=======
import { useState, useRef, useCallback, useEffect } from 'react';
import { Send, Square, Paperclip, Search } from 'lucide-react';
import { toast } from 'sonner';
import { useAppStore, generateId } from '../../lib/store';
import { streamChat, streamResearch } from '../../lib/sse';
import { fetchSavings, getBase } from '../../lib/api';
import { listConnectors, getSyncStatus } from '../../lib/connectors-api';
import { serializeToolCallArguments } from '../../lib/tool-call';
import {
  engineFromCompletionChunk,
  resolveChatEngine,
} from '../../lib/chat-telemetry';
import { MicButton } from './MicButton';
import { useSpeech } from '../../hooks/useSpeech';
import type {
  ChatMessage,
  MessageTelemetry,
  ResearchSearchTrace,
  ResearchSource,
  TokenUsage,
  ToolCallInfo,
} from '../../types';

// While Deep Research is toggled on, poll connected sources for sync
// progress so we can surface "Searching over N items â€” sync in progress"
// next to the toggle. Polling is gated on `enabled` so toggling DR off
// stops the network chatter immediately.
function useResearchCorpusSync(enabled: boolean): {
  syncing: boolean;
  itemsSynced: number;
} {
  const [state, setState] = useState({ syncing: false, itemsSynced: 0 });
>>>>>>> theirs

import React, { useState, useCallback, useRef, useEffect } from "react";
import { useSpeechStream, TranscriptCallback } from "@/hooks/useSpeechStream";
import { useAppStore } from "@/lib/store";
import { uploadChatFiles, getBase } from "@/lib/api";
import { Mic, MicOff, Send, Square, X, Loader2, Paperclip, ChevronUp, ChevronDown } from "lucide-react";

interface InputAreaProps {
  onSendMessage: (text: string, attachments?: { name: string; size: number; type: string }[]) => void;
  disabled?: boolean;
  onStopGeneration?: () => void;
  placeholder?: string;
}

const CHAT_ACCEPTED_EXTENSIONS = '.txt,.md,.pdf,.docx,.csv,.zip,.png,.jpg,.jpeg,.gif,.webp,.bmp,.tiff,.mp4,.webm,.mov,.mkv,.avi';

interface AttachedFile {
  name: string;
  size: number;
  type: string;
  preview?: string;
  file?: File;
}

export function InputArea({ onSendMessage, onStopGeneration, disabled = false, placeholder = "Type a message..." }: InputAreaProps) {
  const [text, setText] = useState("");
  const [isStreaming, setIsStreaming] = useState(false);
  const [transcriptPreview, setTranscriptPreview] = useState("");
  const [status, setStatus] = useState<"idle" | "connecting" | "streaming" | "open" | "closed" | "error">("idle");
  const [attachedFiles, setAttachedFiles] = useState<AttachedFile[]>([]);
  const [showAttachments, setShowAttachments] = useState(false);
  const [isDragOver, setIsDragOver] = useState(false);
  const textareaRef = useRef<HTMLTextAreaElement>(null);
<<<<<<< ours
  const previewRef = useRef<HTMLDivElement>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);
  const attachmentsRef = useRef<HTMLDivElement>(null);
  const [agents, setAgents] = useState<{ key: string; class: string; accepts_tools: boolean }[]>([]);
  const [selectedAgent, setSelectedAgent] = useState<string>('');
  const setSelectedAgentId = useAppStore((s) => s.setSelectedAgentId);
  const chatStreaming = useAppStore((s) => s.streamState.isStreaming);

  const { addMessage } = useAppStore();

  const handleTranscript: TranscriptCallback = useCallback((text, ttfb, total) => {
    if (text.trim()) {
      setTranscriptPreview(text);
      previewRef.current?.scrollIntoView({ behavior: "smooth", block: "nearest" });
||||||| base
  const abortRef = useRef<AbortController | null>(null);
  const timerRef = useRef<ReturnType<typeof setInterval> | null>(null);

  const activeId = useAppStore((s) => s.activeId);
  const selectedModel = useAppStore((s) => s.selectedModel);
  const streamState = useAppStore((s) => s.streamState);
  const messages = useAppStore((s) => s.messages);
  const speechEnabled = useAppStore((s) => s.settings.speechEnabled);
  const maxTokens = useAppStore((s) => s.settings.maxTokens);
  const temperature = useAppStore((s) => s.settings.temperature);
  const createConversation = useAppStore((s) => s.createConversation);
  const addMessage = useAppStore((s) => s.addMessage);
  const updateLastAssistant = useAppStore((s) => s.updateLastAssistant);
  const setStreamState = useAppStore((s) => s.setStreamState);
  const resetStream = useAppStore((s) => s.resetStream);
  const modelLoading = useAppStore((s) => s.modelLoading);
  const deepResearch = useAppStore((s) => s.deepResearch);
  const setDeepResearch = useAppStore((s) => s.setDeepResearch);
  const corpusSync = useResearchCorpusSync(deepResearch);

  const { state: speechState, available: speechAvailable, startRecording, stopRecording } = useSpeech();

  // Abort in-flight stream when the user switches models mid-generation.
  // This prevents errors from trying to continue a stream with a stale model.
  const prevModelRef = useRef(selectedModel);
  useEffect(() => {
    if (prevModelRef.current !== selectedModel && streamState.isStreaming) {
      abortRef.current?.abort();
      if (timerRef.current) {
        clearInterval(timerRef.current);
        timerRef.current = null;
      }
      resetStream();
      abortRef.current = null;
=======
  const abortRef = useRef<AbortController | null>(null);
  const timerRef = useRef<ReturnType<typeof setInterval> | null>(null);

  const activeId = useAppStore((s) => s.activeId);
  const selectedModel = useAppStore((s) => s.selectedModel);
  const streamState = useAppStore((s) => s.streamState);
  const messages = useAppStore((s) => s.messages);
  const speechEnabled = useAppStore((s) => s.settings.speechEnabled);
  const maxTokens = useAppStore((s) => s.settings.maxTokens);
  const temperature = useAppStore((s) => s.settings.temperature);
  const createConversation = useAppStore((s) => s.createConversation);
  const addMessage = useAppStore((s) => s.addMessage);
  const updateLastAssistant = useAppStore((s) => s.updateLastAssistant);
  const setStreamState = useAppStore((s) => s.setStreamState);
  const resetStream = useAppStore((s) => s.resetStream);
  const modelLoading = useAppStore((s) => s.modelLoading);
  const deepResearch = useAppStore((s) => s.deepResearch);
  const setDeepResearch = useAppStore((s) => s.setDeepResearch);
  const corpusSync = useResearchCorpusSync(deepResearch);
  const isCurrentChatStreaming = streamState.isStreaming && streamState.conversationId === activeId;

  const {
    state: speechState,
    error: speechError,
    available: speechAvailable,
    startRecording,
    stopRecording,
  } = useSpeech();

  // Abort in-flight stream when the user switches models mid-generation.
  // This prevents errors from trying to continue a stream with a stale model.
  const prevModelRef = useRef(selectedModel);
  useEffect(() => {
    if (prevModelRef.current !== selectedModel && streamState.isStreaming) {
      abortRef.current?.abort();
      if (timerRef.current) {
        clearInterval(timerRef.current);
        timerRef.current = null;
      }
      resetStream();
      abortRef.current = null;
>>>>>>> theirs
    }
<<<<<<< ours
  }, []);

  const handleStatusChange = useCallback((s: "connecting" | "open" | "streaming" | "closed" | "error") => {
    setStatus(s);
    setIsStreaming(s === "open" || s === "streaming");
    if (s === "closed" || s === "error") {
      if (transcriptPreview.trim()) {
        onSendMessage(transcriptPreview.trim());
        setTranscriptPreview("");
||||||| base
    prevModelRef.current = selectedModel;
  }, [selectedModel, streamState.isStreaming, resetStream]);

  const micDisabled = !speechEnabled || !speechAvailable || streamState.isStreaming;
  const micReason: 'not-enabled' | 'no-backend' | 'streaming' | undefined =
    !speechEnabled ? 'not-enabled'
    : !speechAvailable ? 'no-backend'
    : streamState.isStreaming ? 'streaming'
    : undefined;

  const handleMicClick = useCallback(async () => {
    if (speechState === 'recording') {
      try {
        const text = await stopRecording();
        if (text) {
          setInput((prev) => (prev ? prev + ' ' + text : text));
        }
      } catch {
        // Error is captured in useSpeech
=======
    prevModelRef.current = selectedModel;
  }, [selectedModel, streamState.isStreaming, resetStream]);

  const micDisabled = !speechEnabled || !speechAvailable || streamState.isStreaming;
  const micReason: 'not-enabled' | 'no-backend' | 'streaming' | undefined =
    !speechEnabled ? 'not-enabled'
    : !speechAvailable ? 'no-backend'
    : streamState.isStreaming ? 'streaming'
    : undefined;

  useEffect(() => {
    if (speechError) {
      toast.error(speechError, { duration: 8000 });
    }
  }, [speechError]);

  const handleMicClick = useCallback(async () => {
    if (speechState === 'recording') {
      try {
        const text = await stopRecording();
        if (text) {
          setInput((prev) => (prev ? prev + ' ' + text : text));
        }
      } catch {
        // Error is captured in useSpeech
>>>>>>> theirs
      }
    }
  }, [onSendMessage, transcriptPreview]);

  const handleError = useCallback((err: Error) => {
    console.error("[InputArea] Speech stream error:", err);
    setStatus("error");
    setTimeout(() => setStatus("idle"), 3000);
  }, []);

  const { connect, disconnect, bargeIn } = useSpeechStream({
    onTranscript: handleTranscript,
    onStatusChange: handleStatusChange,
    onError: handleError,
  });

  const handleMicClick = useCallback(() => {
    if (isStreaming || status === "connecting") {
      disconnect();
    } else {
      connect();
    }
  }, [isStreaming, status, connect, disconnect]);

  const handleFiles = useCallback(async (files: FileList) => {
    const newFiles: AttachedFile[] = []
    for (const file of Array.from(files)) {
      if (file.size > 50 * 1024 * 1024) {
        alert(`File ${file.name} is too large (max 50MB)`)
        continue
      }
      let preview: string | undefined
      if (file.type.startsWith('image/')) {
        preview = await new Promise((resolve) => {
          const reader = new FileReader()
          reader.onload = () => resolve(reader.result as string)
          reader.readAsDataURL(file)
        })
      }
      newFiles.push({
        name: file.name,
        size: file.size,
        type: file.type,
        preview,
        file,
      })
    }
    setAttachedFiles((prev) => [...prev, ...newFiles])
    setShowAttachments(true)
  }, [])

<<<<<<< ours
  const removeFile = useCallback((index: number) => {
    setAttachedFiles((prev) => prev.filter((_, i) => i !== index))
  }, [])
||||||| base
  const sendMessage = useCallback(async () => {
    const content = input.trim();
    if (!content || streamState.isStreaming) return;
=======
  const sendMessage = useCallback(async () => {
    const content = input.trim();
    if (!content || streamState.isStreaming) return;
    if (!selectedModel) {
      toast.error('Pick a model first (âŒ˜K)');
      return;
    }
>>>>>>> theirs

  const handleDragOver = useCallback((e: React.DragEvent) => {
    e.preventDefault()
    e.stopPropagation()
    setIsDragOver(true)
  }, [])

  const handleDragLeave = useCallback((e: React.DragEvent) => {
    e.preventDefault()
    e.stopPropagation()
    setIsDragOver(false)
  }, [])

  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault()
    e.stopPropagation()
    setIsDragOver(false)
    if (e.dataTransfer.files.length > 0) {
      handleFiles(e.dataTransfer.files)
    }
  }, [handleFiles])

<<<<<<< ours
  const handleFileInputChange = useCallback((e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      handleFiles(e.target.files)
      e.target.value = ''
    }
  }, [handleFiles])
||||||| base
    const userMsg: ChatMessage = {
      id: generateId(),
      role: 'user',
      content,
      timestamp: Date.now(),
    };
    addMessage(convId, userMsg);

    // Build API messages before adding assistant placeholder
    const currentMessages = useAppStore.getState().messages;
    const apiMessages = currentMessages.map((m) => ({
      role: m.role,
      content: m.content,
    }));

    const assistantMsg: ChatMessage = {
      id: generateId(),
      role: 'assistant',
      content: '',
      timestamp: Date.now(),
      isResearch: deepResearch || undefined,
    };
    addMessage(convId, assistantMsg);

    // Start streaming
    const startTime = Date.now();
    const timer = setInterval(() => {
      setStreamState({ elapsedMs: Date.now() - startTime });
    }, 100);
    timerRef.current = timer;

    const controller = new AbortController();
    abortRef.current = controller;

    let accumulatedContent = '';
    let usage: TokenUsage | undefined;
    let complexity: { score: number; tier: string; suggested_max_tokens: number } | undefined;
    const toolCalls: ToolCallInfo[] = [];
    const researchTraces: ResearchSearchTrace[] = [];
    const researchSourcesByRef = new Map<number, ResearchSource>();
    const flushSources = () =>
      Array.from(researchSourcesByRef.values()).sort((a, b) => a.ref - b.ref);
    let lastFlush = 0;
    let ttftMs: number | undefined;

    setStreamState({
      isStreaming: true,
      phase: deepResearch ? 'Researching...' : 'Generating...',
      elapsedMs: 0,
      activeToolCalls: [],
      content: '',
    });
    useAppStore.getState().addLogEntry({
      timestamp: Date.now(),
      level: 'info',
      category: 'chat',
      message: deepResearch
        ? `Research: "${content.slice(0, 80)}${content.length > 80 ? '...' : ''}"`
        : `Request: "${content.slice(0, 80)}${content.length > 80 ? '...' : ''}" â†’ ${selectedModel}`,
    });

    try {
      if (deepResearch) {
        for await (const ev of streamResearch(content, controller.signal)) {
          if (ev.type === 'search_call') {
            const trace: ResearchSearchTrace = {
              id: generateId(),
              query: ev.arguments?.query ?? '',
              person: ev.arguments?.person,
              timeRange: ev.arguments?.time_range,
              status: 'pending',
            };
            researchTraces.push(trace);
            setStreamState({ phase: `Searching: ${trace.query}` });
            updateLastAssistant(
              convId,
              accumulatedContent,
              undefined,
              undefined,
              undefined,
              undefined,
              [...researchTraces],
              flushSources(),
            );
            useAppStore.getState().addLogEntry({
              timestamp: Date.now(),
              level: 'info',
              category: 'tool',
              message: `Search: "${trace.query}"${trace.person ? ` (person: ${trace.person})` : ''}`,
            });
          } else if (ev.type === 'search_result') {
            const pending = [...researchTraces].reverse().find((t) => t.status === 'pending');
            if (pending) {
              pending.status = 'complete';
              pending.numHits = ev.num_hits;
              pending.topTitles = ev.top_titles;
            }
            if (ev.sources) {
              for (const src of ev.sources) {
                if (src && typeof src.ref === 'number' && !researchSourcesByRef.has(src.ref)) {
                  researchSourcesByRef.set(src.ref, src);
                }
              }
            }
            updateLastAssistant(
              convId,
              accumulatedContent,
              undefined,
              undefined,
              undefined,
              undefined,
              [...researchTraces],
              flushSources(),
            );
          } else if (ev.type === 'synthesis') {
            if (!ttftMs) ttftMs = Date.now() - startTime;
            accumulatedContent += ev.text;
            setStreamState({ content: accumulatedContent, phase: '' });
            const now = Date.now();
            if (now - lastFlush >= 80) {
              updateLastAssistant(
                convId,
                accumulatedContent,
                undefined,
                undefined,
                undefined,
                undefined,
                [...researchTraces],
                flushSources(),
              );
              lastFlush = now;
            }
          } else if (ev.type === 'system_metrics') {
            // Live GPU sample â€” feed straight to the System panel so Power
            // (W) and Energy (kJ) tick up in real time as the agent runs.
            useAppStore.getState().setLiveEnergy({
              power_w: ev.power_w,
              energy_j: ev.energy_j,
              duration_s: ev.duration_s,
            });
          } else if (ev.type === 'done') {
            if (ev.usage) {
              usage = {
                prompt_tokens: ev.usage.prompt_tokens ?? 0,
                completion_tokens: ev.usage.completion_tokens ?? 0,
                total_tokens:
                  ev.usage.total_tokens ??
                  (ev.usage.prompt_tokens ?? 0) +
                    (ev.usage.completion_tokens ?? 0),
              };
              // Optimistically roll this research turn into the session
              // counters so the Session panel updates the moment the
              // stream finishes, regardless of how /v1/savings aggregates
              // research telemetry server-side.
              useAppStore.getState().incrementSavings(usage);
            }
            // Hold the final live numbers visible for a beat so the panel
            // doesn't flash to 0 between the SSE close and the next
            // /v1/telemetry/energy poll picking up the persisted record.
            window.setTimeout(() => {
              useAppStore.getState().setLiveEnergy(null);
            }, 1500);
            break;
          }
        }
      } else {
      for await (const sseEvent of streamChat(
        { model: selectedModel, messages: apiMessages, stream: true, temperature, max_tokens: maxTokens },
        controller.signal,
      )) {
        const eventName = sseEvent.event;

        if (eventName === 'agent_turn_start') {
          setStreamState({ phase: 'Agent thinking...' });
        } else if (eventName === 'inference_start') {
          setStreamState({ phase: 'Generating...' });
          useAppStore.getState().addLogEntry({
            timestamp: Date.now(), level: 'info', category: 'chat',
            message: `Generating with ${selectedModel}...`,
          });
        } else if (eventName === 'tool_call_start') {
          try {
            const data = JSON.parse(sseEvent.data);
            const tc: ToolCallInfo = {
              id: generateId(),
              tool: data.tool,
              arguments: data.arguments || '',
              status: 'running',
            };
            toolCalls.push(tc);
            setStreamState({
              phase: `Calling ${data.tool}...`,
              activeToolCalls: [...toolCalls],
            });
            updateLastAssistant(convId, accumulatedContent, [...toolCalls]);
            useAppStore.getState().addLogEntry({
              timestamp: Date.now(), level: 'info', category: 'tool',
              message: `Calling ${data.tool}(${data.arguments || ''})`,
            });
          } catch {}
        } else if (eventName === 'tool_call_end') {
          try {
            const data = JSON.parse(sseEvent.data);
            const tc = toolCalls.find(
              (t) => t.tool === data.tool && t.status === 'running',
            );
            if (tc) {
              tc.status = data.success ? 'success' : 'error';
              tc.latency = data.latency;
              tc.result = data.result;
            }
            setStreamState({
              phase: 'Generating...',
              activeToolCalls: [...toolCalls],
            });
            updateLastAssistant(convId, accumulatedContent, [...toolCalls]);
          } catch {}
        } else {
          try {
            const data = JSON.parse(sseEvent.data);
            const delta = data.choices?.[0]?.delta;
            if (data.usage) usage = data.usage;
            if (data.complexity) complexity = data.complexity;
            if (delta?.content) {
              if (!ttftMs) ttftMs = Date.now() - startTime;
              accumulatedContent += delta.content;
              setStreamState({ content: accumulatedContent, phase: '' });

              const now = Date.now();
              if (now - lastFlush >= 80) {
                updateLastAssistant(
                  convId,
                  accumulatedContent,
                  toolCalls.length > 0 ? [...toolCalls] : undefined,
                );
                lastFlush = now;
              }
            }
            if (data.choices?.[0]?.finish_reason === 'stop') break;
          } catch {}
        }
      }
      }
    } catch (err: any) {
      if (err.name === 'AbortError') {
        // User cancelled or model switch â€” keep whatever was accumulated
        if (!accumulatedContent) accumulatedContent = '(Generation stopped)';
      } else {
        const errMsg = err?.message || String(err);
        accumulatedContent =
          accumulatedContent || `Error: ${errMsg}`;
        useAppStore.getState().addLogEntry({
          timestamp: Date.now(), level: 'error', category: 'chat',
          message: `Stream error: ${errMsg}`,
        });
      }
      // If we tore out mid-research, make sure the live System panel
      // numbers don't get stuck on the last sample.
      useAppStore.getState().setLiveEnergy(null);
    } finally {
      if (!accumulatedContent) {
        accumulatedContent = 'No response was generated. Please try again.';
      }
      const totalMs = Date.now() - startTime;
      const _CLOUD_PREFIXES = ['gpt-', 'o1-', 'o3-', 'o4-', 'claude-', 'gemini-', 'openrouter/', 'MiniMax-', 'chatgpt-'];
      const engineLabel = _CLOUD_PREFIXES.some(p => selectedModel.startsWith(p)) ? 'cloud' : 'ollama';
      const telemetry: MessageTelemetry = {
        engine: engineLabel,
        model_id: selectedModel,
        total_ms: totalMs,
        ttft_ms: ttftMs,
        tokens_per_sec: usage?.completion_tokens
          ? usage.completion_tokens / (totalMs / 1000)
          : undefined,
        complexity_score: complexity?.score,
        complexity_tier: complexity?.tier,
        suggested_max_tokens: complexity?.suggested_max_tokens,
      };
      // Check if the response has digest audio available
      let audioMeta: { url: string } | undefined;
      try {
        const digestRes = await fetch(`${getBase()}/api/digest`);
        if (digestRes.ok) {
          const digest = await digestRes.json();
          if (digest.audio_available) {
            audioMeta = { url: `${getBase()}/api/digest/audio` };
          }
        }
      } catch {
        // Not a digest response or server unavailable â€” skip
      }
=======
    const userMsg: ChatMessage = {
      id: generateId(),
      role: 'user',
      content,
      timestamp: Date.now(),
    };
    addMessage(convId, userMsg);

    // Build API messages before adding assistant placeholder
    const currentMessages = useAppStore.getState().messages;
    const apiMessages = currentMessages.map((m) => ({
      role: m.role,
      content: m.content,
    }));

    const assistantMsg: ChatMessage = {
      id: generateId(),
      role: 'assistant',
      content: '',
      timestamp: Date.now(),
      isResearch: deepResearch || undefined,
    };
    addMessage(convId, assistantMsg);

    // Start streaming
    const startTime = Date.now();
    const timer = setInterval(() => {
      setStreamState({ elapsedMs: Date.now() - startTime });
    }, 100);
    timerRef.current = timer;

    const controller = new AbortController();
    abortRef.current = controller;

    let accumulatedContent = '';
    let usage: TokenUsage | undefined;
    let complexity: { score: number; tier: string; suggested_max_tokens: number } | undefined;
    let routedEngine: string | undefined;
    const toolCalls: ToolCallInfo[] = [];
    const researchTraces: ResearchSearchTrace[] = [];
    const researchSourcesByRef = new Map<number, ResearchSource>();
    const flushSources = () =>
      Array.from(researchSourcesByRef.values()).sort((a, b) => a.ref - b.ref);
    let lastFlush = 0;
    let ttftMs: number | undefined;

    setStreamState({
      conversationId: convId,
      isStreaming: true,
      phase: deepResearch ? 'Researching...' : 'Generating...',
      elapsedMs: 0,
      activeToolCalls: [],
      content: '',
    });
    useAppStore.getState().addLogEntry({
      timestamp: Date.now(),
      level: 'info',
      category: 'chat',
      message: deepResearch
        ? `Research: "${content.slice(0, 80)}${content.length > 80 ? '...' : ''}"`
        : `Request: "${content.slice(0, 80)}${content.length > 80 ? '...' : ''}" â†’ ${selectedModel}`,
    });

    try {
      if (deepResearch) {
        for await (const ev of streamResearch(
          content,
          selectedModel,
          controller.signal,
        )) {
          if (ev.type === 'search_call') {
            const trace: ResearchSearchTrace = {
              id: generateId(),
              query: ev.arguments?.query ?? '',
              person: ev.arguments?.person,
              timeRange: ev.arguments?.time_range,
              status: 'pending',
            };
            researchTraces.push(trace);
            setStreamState({ phase: `Searching: ${trace.query}` });
            updateLastAssistant(
              convId,
              accumulatedContent,
              undefined,
              undefined,
              undefined,
              undefined,
              [...researchTraces],
              flushSources(),
            );
            useAppStore.getState().addLogEntry({
              timestamp: Date.now(),
              level: 'info',
              category: 'tool',
              message: `Search: "${trace.query}"${trace.person ? ` (person: ${trace.person})` : ''}`,
            });
          } else if (ev.type === 'search_result') {
            const pending = [...researchTraces].reverse().find((t) => t.status === 'pending');
            if (pending) {
              pending.status = 'complete';
              pending.numHits = ev.num_hits;
              pending.topTitles = ev.top_titles;
            }
            if (ev.sources) {
              for (const src of ev.sources) {
                if (src && typeof src.ref === 'number' && !researchSourcesByRef.has(src.ref)) {
                  researchSourcesByRef.set(src.ref, src);
                }
              }
            }
            updateLastAssistant(
              convId,
              accumulatedContent,
              undefined,
              undefined,
              undefined,
              undefined,
              [...researchTraces],
              flushSources(),
            );
          } else if (ev.type === 'synthesis') {
            if (!ttftMs) ttftMs = Date.now() - startTime;
            accumulatedContent += ev.text;
            setStreamState({ content: accumulatedContent, phase: '' });
            const now = Date.now();
            if (now - lastFlush >= 80) {
              updateLastAssistant(
                convId,
                accumulatedContent,
                undefined,
                undefined,
                undefined,
                undefined,
                [...researchTraces],
                flushSources(),
              );
              lastFlush = now;
            }
          } else if (ev.type === 'system_metrics') {
            // Live GPU sample â€” feed straight to the System panel so Power
            // (W) and Energy (kJ) tick up in real time as the agent runs.
            useAppStore.getState().setLiveEnergy({
              power_w: ev.power_w,
              energy_j: ev.energy_j,
              duration_s: ev.duration_s,
            });
          } else if (ev.type === 'error') {
            // Backend setup/worker failure (Ollama down, planner model
            // missing, KnowledgeStore locked, etc.). Without surfacing the
            // message, the user sees only the generic "No response was
            // generated" fallback and has no way to self-diagnose.
            const msg = ev.message || 'Research failed (no detail provided)';
            accumulatedContent = accumulatedContent
              ? `${accumulatedContent}\n\n**Research stopped:** ${msg}`
              : `**Research failed:** ${msg}`;
            setStreamState({ content: accumulatedContent, phase: '' });
            useAppStore.getState().addLogEntry({
              timestamp: Date.now(),
              level: 'error',
              category: 'chat',
              message: `Deep Research error: ${msg}`,
            });
            toast.error(msg, { duration: 8000 });
          } else if (ev.type === 'done') {
            if (ev.usage) {
              usage = {
                prompt_tokens: ev.usage.prompt_tokens ?? 0,
                completion_tokens: ev.usage.completion_tokens ?? 0,
                total_tokens:
                  ev.usage.total_tokens ??
                  (ev.usage.prompt_tokens ?? 0) +
                    (ev.usage.completion_tokens ?? 0),
              };
              // Optimistically roll this research turn into the session
              // counters so the Session panel updates the moment the
              // stream finishes, regardless of how /v1/savings aggregates
              // research telemetry server-side.
              useAppStore.getState().incrementSavings(usage);
            }
            // Hold the final live numbers visible for a beat so the panel
            // doesn't flash to 0 between the SSE close and the next
            // /v1/telemetry/energy poll picking up the persisted record.
            window.setTimeout(() => {
              useAppStore.getState().setLiveEnergy(null);
            }, 1500);
            break;
          }
        }
      } else {
      for await (const sseEvent of streamChat(
        { model: selectedModel, messages: apiMessages, stream: true, temperature, max_tokens: maxTokens },
        controller.signal,
      )) {
        const eventName = sseEvent.event;

        if (eventName === 'agent_turn_start') {
          setStreamState({ phase: 'Agent thinking...' });
        } else if (eventName === 'inference_start') {
          setStreamState({ phase: 'Generating...' });
          useAppStore.getState().addLogEntry({
            timestamp: Date.now(), level: 'info', category: 'chat',
            message: `Generating with ${selectedModel}...`,
          });
        } else if (eventName === 'tool_call_start') {
          try {
            const data = JSON.parse(sseEvent.data);
            const tc: ToolCallInfo = {
              id: generateId(),
              tool: data.tool,
              arguments: serializeToolCallArguments(data.arguments),
              status: 'running',
            };
            toolCalls.push(tc);
            setStreamState({
              phase: `Calling ${data.tool}...`,
              activeToolCalls: [...toolCalls],
            });
            updateLastAssistant(convId, accumulatedContent, [...toolCalls]);
            useAppStore.getState().addLogEntry({
              timestamp: Date.now(), level: 'info', category: 'tool',
              message: `Calling ${data.tool}(${serializeToolCallArguments(data.arguments)})`,
            });
          } catch {}
        } else if (eventName === 'tool_call_end') {
          try {
            const data = JSON.parse(sseEvent.data);
            const tc = toolCalls.find(
              (t) => t.tool === data.tool && t.status === 'running',
            );
            if (tc) {
              tc.status = data.success ? 'success' : 'error';
              tc.latency = data.latency;
              tc.result = data.result;
            }
            setStreamState({
              phase: 'Generating...',
              activeToolCalls: [...toolCalls],
            });
            updateLastAssistant(convId, accumulatedContent, [...toolCalls]);
          } catch {}
        } else {
          try {
            const data = JSON.parse(sseEvent.data);
            const delta = data.choices?.[0]?.delta;
            if (data.usage) usage = data.usage;
            if (data.complexity) complexity = data.complexity;
            routedEngine = engineFromCompletionChunk(data) ?? routedEngine;
            if (delta?.content) {
              if (!ttftMs) ttftMs = Date.now() - startTime;
              accumulatedContent += delta.content;
              setStreamState({ content: accumulatedContent, phase: '' });

              const now = Date.now();
              if (now - lastFlush >= 80) {
                updateLastAssistant(
                  convId,
                  accumulatedContent,
                  toolCalls.length > 0 ? [...toolCalls] : undefined,
                );
                lastFlush = now;
              }
            }
            if (data.choices?.[0]?.finish_reason === 'stop') break;
          } catch {}
        }
      }
      }
    } catch (err: any) {
      if (err.name === 'AbortError') {
        // User cancelled or model switch â€” keep whatever was accumulated
        if (!accumulatedContent) accumulatedContent = '(Generation stopped)';
      } else {
        const errMsg = err?.message || String(err);
        accumulatedContent =
          accumulatedContent || `Error: ${errMsg}`;
        useAppStore.getState().addLogEntry({
          timestamp: Date.now(), level: 'error', category: 'chat',
          message: `Stream error: ${errMsg}`,
        });
      }
      // If we tore out mid-research, make sure the live System panel
      // numbers don't get stuck on the last sample.
      useAppStore.getState().setLiveEnergy(null);
    } finally {
      if (!accumulatedContent) {
        accumulatedContent = 'No response was generated. Please try again.';
      }
      const totalMs = Date.now() - startTime;
      const appState = useAppStore.getState();
      const selectedOwner = appState.models.find((m) => m.id === selectedModel)?.owned_by;
      const engineLabel = resolveChatEngine({
        routedEngine,
        serverEngine: appState.serverInfo?.engine,
        selectedModel,
        selectedOwner,
      });
      const telemetry: MessageTelemetry = {
        engine: engineLabel,
        model_id: selectedModel,
        total_ms: totalMs,
        ttft_ms: ttftMs,
        tokens_per_sec: usage?.completion_tokens
          ? usage.completion_tokens / (totalMs / 1000)
          : undefined,
        complexity_score: complexity?.score,
        complexity_tier: complexity?.tier,
        suggested_max_tokens: complexity?.suggested_max_tokens,
      };
      // Check if the response has digest audio available
      let audioMeta: { url: string } | undefined;
      try {
        const digestRes = await fetch(`${getBase()}/api/digest`);
        if (digestRes.ok) {
          const digest = await digestRes.json();
          if (digest.audio_available) {
            audioMeta = { url: `${getBase()}/api/digest/audio` };
          }
        }
      } catch {
        // Not a digest response or server unavailable â€” skip
      }
>>>>>>> theirs

  const sendWithAttachments = useCallback(async () => {
    const msg = text.trim() || transcriptPreview.trim()
    if (!msg && attachedFiles.length === 0) return
    
    if (attachedFiles.length > 0) {
      const filesToUpload = attachedFiles.map(f => f.file).filter((f): f is File => !!f)
      if (filesToUpload.length > 0) {
        try {
          await uploadChatFiles(filesToUpload)
        } catch (e) {
          console.error('File upload error:', e)
        }
      }
    }
    
    const attachmentMeta = attachedFiles.map((f) => ({ name: f.name, size: f.size, type: f.type }))
    onSendMessage(msg, attachmentMeta.length > 0 ? attachmentMeta : undefined)
    setText('')
    setTranscriptPreview('')
    setAttachedFiles([])
    setShowAttachments(false)
    if (isStreaming) {
      bargeIn()
      disconnect()
    }
  }, [text, transcriptPreview, attachedFiles, onSendMessage, isStreaming, bargeIn, disconnect])

  const handleSendClick = sendWithAttachments

  const handleKeyDown = useCallback((e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSendClick();
    }
  }, [handleSendClick]);

  const handleTextChange = useCallback((e: React.ChangeEvent<HTMLTextAreaElement>) => {
    setText(e.target.value);
    if (isStreaming && e.target.value.trim()) {
      bargeIn();
      disconnect();
    }
  }, [isStreaming, bargeIn, disconnect]);

  useEffect(() => {
    textareaRef.current?.focus();
  }, []);

  useEffect(() => {
    const handleClickOutside = (e: MouseEvent) => {
      if (attachmentsRef.current && !attachmentsRef.current.contains(e.target as Node)) {
        setShowAttachments(false)
      }
    }
    document.addEventListener('mousedown', handleClickOutside)
    return () => document.removeEventListener('mousedown', handleClickOutside)
  }, [])

  useEffect(() => {
    fetch(getBase() + '/v1/agents')
      .then((r) => (r.ok ? r.json() : { registered: [] }))
      .then((d) => setAgents(d.registered || []))
      .catch(() => {});
  }, [])

  const micIcon = isStreaming ? (
    <MicOff className="w-5 h-5 text-red-500" />
  ) : (
    <Mic className="w-5 h-5 text-gray-600 hover:text-blue-600" />
  );

  const formatSize = (bytes: number) => {
    if (bytes < 1024) return `${bytes} B`
    if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`
    return `${(bytes / (1024 * 1024)).toFixed(1)} MB`
  }

  const getFileIcon = (type: string, preview?: string) => {
    if (preview) return <img src={preview} alt="" className="w-5 h-5 rounded object-cover" />
    if (type.startsWith('image/')) return <span className="text-xs text-gray-500">Ã°Å¸â€“Â¼</span>
    if (type.startsWith('video/')) return <span className="text-xs text-gray-500">Ã°Å¸Å½Â¬</span>
    if (type === 'application/zip' || type === 'application/x-zip-compressed') return <span className="text-xs text-gray-500">Ã°Å¸â€œÂ¦</span>
    if (type === 'application/pdf') return <span className="text-xs text-gray-500">Ã°Å¸â€œâ€ž</span>
    return <span className="text-xs text-gray-500">Ã°Å¸â€œÅ½</span>
  }

  return (
    <div className="flex flex-col gap-2 p-4 border-t border-gray-200 bg-white">
      {(isStreaming || transcriptPreview) && (
        <div
          ref={previewRef}
          className={`px-3 py-2 rounded-lg border transition-all ${
            isStreaming
              ? "bg-blue-50 border-blue-200 text-blue-900"
              : "bg-green-50 border-green-200 text-green-900"
          }`}
        >
          <div className="flex items-center gap-2 text-sm">
            <Loader2 className={`w-4 h-4 animate-spin ${isStreaming ? "text-blue-500" : "hidden"}`} />
            <span className="font-medium">{isStreaming ? "Listening..." : "Ready to send"}</span>
            {isStreaming && (
              <span className="text-xs text-blue-600">(click mic to stop)</span>
            )}
          </div>
          {transcriptPreview && (
            <p className="mt-1 text-sm whitespace-pre-wrap">{transcriptPreview}</p>
          )}
        </div>
      )}

      {attachedFiles.length > 0 && showAttachments && (
        <div
          ref={attachmentsRef}
          className="absolute bottom-full left-0 right-0 mb-2 p-2 rounded-lg border bg-white shadow-lg z-10 max-h-60 overflow-y-auto"
          style={{ borderColor: 'var(--color-border)' }}
        >
          <div className="flex items-center justify-between mb-2 pb-2 border-b text-sm font-medium">
            <span>Attachments ({attachedFiles.length})</span>
            <button
              onClick={() => setShowAttachments(false)}
              className="p-1 text-gray-400 hover:text-gray-600"
              aria-label="Close attachments"
            >
              <X className="w-4 h-4" />
            </button>
          </div>
          {attachedFiles.map((file, idx) => (
            <div key={idx} className="flex items-center gap-2 px-2 py-1.5 rounded hover:bg-gray-50">
              {getFileIcon(file.type, file.preview)}
              <div className="flex-1 min-w-0">
                <p className="text-sm truncate">{file.name}</p>
                <p className="text-xs text-gray-400">{formatSize(file.size)}</p>
              </div>
              <button
                onClick={() => removeFile(idx)}
                className="p-1 text-gray-400 hover:text-red-500"
                aria-label={`Remove ${file.name}`}
              >
                <X className="w-4 h-4" />
              </button>
            </div>
          ))}
          <button
            onClick={() => fileInputRef.current?.click()}
            className="w-full mt-2 px-2 py-1.5 text-xs text-center text-blue-600 hover:bg-blue-50 rounded"
          >
            + Add more files
          </button>
        </div>
      )}

      <div className="flex items-end gap-2 relative">
        <textarea
          ref={textareaRef}
          value={text}
          onChange={handleTextChange}
          onKeyDown={handleKeyDown}
<<<<<<< ours
          placeholder={placeholder}
          disabled={disabled || isStreaming}
||||||| base
          placeholder="Message OpenJarvis..."
=======
          placeholder={selectedModel ? 'Message OpenJarvis...' : 'Pick a model first (âŒ˜K)...'}
>>>>>>> theirs
          rows={1}
          className={`
            flex-1 px-4 py-2.5 rounded-lg border resize-none
            focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent
            transition-colors
            ${disabled || isStreaming ? "bg-gray-50 text-gray-500 cursor-not-allowed" : "bg-white"}
            ${isStreaming ? "border-blue-200" : "border-gray-300"}
            pr-12
          `}
          style={{ minHeight: "44px" }}
        />
<<<<<<< ours

        <div className="relative" ref={attachmentsRef}>
||||||| base
        {streamState.isStreaming ? (
=======
        {isCurrentChatStreaming ? (
>>>>>>> theirs
          <button
            onClick={() => {
              if (attachedFiles.length > 0) {
                setShowAttachments(!showAttachments)
              } else {
                fileInputRef.current?.click()
              }
            }}
            onDragOver={handleDragOver}
            onDragLeave={handleDragLeave}
            onDrop={handleDrop}
            disabled={disabled}
            className={`
              p-2.5 rounded-lg transition-colors flex-shrink-0
              ${attachedFiles.length > 0
                ? "bg-blue-50 text-blue-600 hover:bg-blue-100"
                : "bg-gray-100 text-gray-600 hover:bg-gray-200"}
              ${disabled ? "opacity-50 cursor-not-allowed" : ""}
              ${isDragOver ? "bg-blue-100 border-blue-400" : ""}
            `}
            title={attachedFiles.length > 0 ? `${attachedFiles.length} file(s) attached - click to manage` : "Attach files"}
            aria-label={attachedFiles.length > 0 ? `${attachedFiles.length} file(s) attached` : "Attach files"}
          >
            <Paperclip className="w-5 h-5" />
            {attachedFiles.length > 0 && (
              <span className="absolute -top-1 -right-1 w-5 h-5 text-xs font-medium bg-red-500 text-white rounded-full flex items-center justify-center">
                {attachedFiles.length > 9 ? '9+' : attachedFiles.length}
              </span>
            )}
            {showAttachments && <ChevronUp className="w-4 h-4 ml-1" />}
            {!showAttachments && attachedFiles.length === 0 && <ChevronDown className="w-4 h-4 ml-1 opacity-50" />}
          </button>
          
          <input
            ref={fileInputRef}
            type="file"
            multiple
            accept={CHAT_ACCEPTED_EXTENSIONS}
            onChange={handleFileInputChange}
            className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
            aria-hidden="true"
          />
        </div>

        <select
          value={selectedAgent}
          onChange={(e) => { setSelectedAgent(e.target.value); setSelectedAgentId(e.target.value || null); }}
          disabled={disabled}
          className='h-[44px] px-2 rounded-lg border border-gray-300 bg-white text-xs text-gray-700 flex-shrink-0 max-w-[150px]'
          title='Agent'
          aria-label='Select agent'
        >
          <option value=''>No agent (chat)</option>
          {agents.map((a) => (
            <option key={a.key} value={a.key}>{a.key}</option>
          ))}
        </select>

        <button
          onClick={handleMicClick}
          disabled={disabled || status === "connecting"}
          className={`
            p-2.5 rounded-lg transition-colors flex-shrink-0
            ${isStreaming
              ? "bg-red-50 text-red-600 hover:bg-red-100"
              : "bg-gray-100 text-gray-600 hover:bg-gray-200"}
            ${disabled || status === "connecting" ? "opacity-50 cursor-not-allowed" : ""}
          `}
          title={isStreaming ? "Stop listening" : "Start voice input"}
          aria-label={isStreaming ? "Stop voice input" : "Start voice input"}
        >
          {status === "connecting" ? (
            <Loader2 className="w-5 h-5 animate-spin" />
          ) : (
            micIcon
          )}
        </button>

        <button
          onClick={handleSendClick}
          disabled={disabled || chatStreaming || (!text.trim() && !transcriptPreview.trim() && attachedFiles.length === 0)}
          className={`
            p-2.5 rounded-lg transition-colors flex-shrink-0
            ${text.trim() || transcriptPreview.trim() || attachedFiles.length > 0
              ? "bg-blue-600 text-white hover:bg-blue-700"
              : "bg-gray-100 text-gray-400 cursor-not-allowed"}
          `}
          title="Send message"
          aria-label="Send message"
        >
          <Send className="w-5 h-5" />
        </button>

        {chatStreaming && (
          <button
            onClick={() => onStopGeneration?.()}
            className="p-2.5 rounded-lg bg-red-600 text-white hover:bg-red-700 transition-colors flex-shrink-0"
            title="Stop generating"
            aria-label="Stop generating"
          >
            <Square className="w-5 h-5" />
          </button>
        )}

        {(text.trim() || attachedFiles.length > 0) && (
          <button
            onClick={() => { setText(""); setAttachedFiles([]); setShowAttachments(false); }}
            className="p-2.5 rounded-lg bg-gray-100 text-gray-600 hover:bg-gray-200 transition-colors"
            title="Clear input"
            aria-label="Clear input"
          >
            <X className="w-5 h-5" />
          </button>
<<<<<<< ours
||||||| base
        ) : (
          <div className="flex items-center gap-1">
            <MicButton
              state={speechState}
              onClick={handleMicClick}
              disabled={micDisabled}
              reason={micReason}
            />
            <button
              onClick={sendMessage}
              disabled={!input.trim() || modelLoading}
              className="p-2 rounded-xl transition-colors shrink-0 cursor-pointer disabled:opacity-30 disabled:cursor-default"
              style={{
                background: input.trim() ? 'var(--color-accent)' : 'var(--color-bg-tertiary)',
                color: input.trim() ? 'white' : 'var(--color-text-tertiary)',
              }}
              title="Send message"
            >
              <Send size={16} />
            </button>
          </div>
=======
        ) : (
          <div className="flex items-center gap-1">
            <MicButton
              state={speechState}
              onClick={handleMicClick}
              disabled={micDisabled}
              reason={micReason}
            />
            <button
              onClick={sendMessage}
              disabled={streamState.isStreaming || !input.trim() || modelLoading || !selectedModel}
              title={selectedModel ? 'Send message' : 'Pick a model first (âŒ˜K)'}
              className="p-2 rounded-xl transition-colors shrink-0 cursor-pointer disabled:opacity-30 disabled:cursor-default"
              style={{
                background: input.trim() ? 'var(--color-accent)' : 'var(--color-bg-tertiary)',
                color: input.trim() ? 'white' : 'var(--color-text-tertiary)',
              }}
            >
              <Send size={16} />
            </button>
          </div>
>>>>>>> theirs
        )}
      </div>

      {status === "error" && (
        <div className="text-xs text-red-600 flex items-center gap-1">
          <span>Speech recognition error Ã¢â‚¬â€ click mic to retry</span>
        </div>
      )}
    </div>
  );
}


## ===== frontend/src/components/Chat/MessageBubble.tsx : OUR COMMITS SINCE AUTHOR BASE =====
670c3aaf feat: numbered question UI buttons, sub-bullet fix, trailing text relaxed, shell_exec utf-8 encoding, croniter installed, persistent API keys hydrate from Rust backend, fix: use npx tauri build for full Rust exe compile (npm run build:tauri is frontend only)
bc498a16 feat: Arc Reactor ThinkingCircle, fix env loading, fix project root, add research types, remove debug code

## ===== frontend/src/components/Chat/MessageBubble.tsx : CONFLICTED WORKING FILE (diff3) =====
import { useState, useMemo } from 'react';
import ReactMarkdown from 'react-markdown';
import rehypeHighlight from 'rehype-highlight';
import rehypeKatex from 'rehype-katex';
import remarkGfm from 'remark-gfm';
import remarkMath from 'remark-math';
import 'katex/dist/katex.min.css';
import { Copy, Check } from 'lucide-react';
import { AudioPlayer } from './AudioPlayer';
import { ToolCallCard } from './ToolCallCard';
import { XRayFooter } from './XRayFooter';
import type { ChatMessage } from '../../types';

function stripThinkTags(text: string): string {
  let cleaned = text.replace(/<think>[\s\S]*?<\/think>\s*/gi, '');
  cleaned = cleaned.replace(/^[\s\S]*?<\/think>\s*/i, '');
  return cleaned.trim();
}

interface Props {
  message: ChatMessage;
}

interface ParsedOptions {
  preamble: string;
  options: { number: string; text: string }[];
}

/**
 * Detects numbered lists in assistant responses and extracts them as options.
 * Returns null if the message doesn't look like a question with numbered choices.
 *
 * Matches patterns like:
 *   1. Option text
 *   1) Option text
 *   **1.** Option text  (bold markdown)
 */
function parseNumberedOptions(text: string): ParsedOptions | null {
  const lines = text.split('\n');

  // Find the first numbered item
  const numberedLineRegex = /^\s*\*{0,2}(\d+)[.)]\*{0,2}\s+(.+)/;
  let firstIndex = -1;
  for (let i = 0; i < lines.length; i++) {
    if (numberedLineRegex.test(lines[i])) {
      firstIndex = i;
      break;
    }
  }

  if (firstIndex === -1) return null;

  // Collect consecutive numbered items
  const options: { number: string; text: string }[] = [];
  let lastIndex = firstIndex;

  for (let i = firstIndex; i < lines.length; i++) {
    const match = lines[i].match(numberedLineRegex);
    if (match) {
      options.push({ number: match[1], text: match[2].replace(/\*+/g, '').trim() });
      lastIndex = i;
    } else if (lines[i].trim() === '') {
      // Allow blank lines within the list
      continue;
    } else if (/^\s+[*\-]/.test(lines[i])) {
      // Sub-bullet under a numbered item -- skip
      continue;
    } else {
      // Non-numbered non-blank non-sub-bullet -- stop
      break;
    }
  }

  // Only render as buttons if there are 2â€“8 options
  if (options.length < 2 || options.length > 8) return null;

  const preamble = lines.slice(0, firstIndex).join('\n').trim();

  // Check for trailing content after the list â€” if there's significant text after,
  // it's probably not a "pick one" prompt, just render normally
  const trailing = lines.slice(lastIndex + 1).join('\n').trim();
  if (trailing.length > 500) return null;

  return { preamble, options };
}

function getTextContent(node: any): string {
  if (typeof node === 'string' || typeof node === 'number') {
    return String(node);
  }
  if (Array.isArray(node)) {
    return node.map(getTextContent).join('');
  }
  if (node?.props?.children) {
    return getTextContent(node.props.children);
  }
  return '';
}

function CodeBlockPre({ children, ...props }: any) {
  const [copied, setCopied] = useState(false);
  const codeElement = Array.isArray(children) ? children[0] : children;
  const className = codeElement?.props?.className || '';
  const match = /language-([\w-]+)/.exec(className);
  const lang = match ? match[1] : '';
  const code = getTextContent(codeElement?.props?.children).replace(/\n$/, '');

  const handleCopy = () => {
    navigator.clipboard.writeText(code);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div
      className="code-block-wrapper relative my-3"
      style={{ borderRadius: 'var(--radius-md)', overflow: 'hidden' }}
    >
      <div
        className="flex items-center justify-between px-4 py-1.5 text-xs"
        style={{ background: 'var(--color-bg-tertiary)', color: 'var(--color-text-tertiary)' }}
      >
        <span className="font-mono">{lang || 'code'}</span>
        <button
          onClick={handleCopy}
          className="flex items-center gap-1 px-2 py-0.5 rounded transition-colors cursor-pointer"
          style={{ color: 'var(--color-text-tertiary)' }}
          onMouseEnter={(e) => (e.currentTarget.style.color = 'var(--color-text-secondary)')}
          onMouseLeave={(e) => (e.currentTarget.style.color = 'var(--color-text-tertiary)')}
        >
          {copied ? <Check size={12} /> : <Copy size={12} />}
          {copied ? 'Copied' : 'Copy'}
        </button>
      </div>
      <pre {...props} style={{ margin: 0, borderRadius: 0 }}>
        {children}
      </pre>
    </div>
  );
}

function CopyMessageButton({ content }: { content: string }) {
  const [copied, setCopied] = useState(false);

  const handleCopy = () => {
    navigator.clipboard.writeText(content);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <button
      onClick={handleCopy}
      className="p-1 rounded opacity-0 group-hover:opacity-100 transition-opacity cursor-pointer"
      style={{ color: 'var(--color-text-tertiary)' }}
      title="Copy message"
    >
      {copied ? <Check size={14} /> : <Copy size={14} />}
    </button>
  );
}

function NumberedOptionButtons({ parsed }: { parsed: ParsedOptions }) {
  const [selected, setSelected] = useState<string | null>(null);

  const handleSelect = (option: { number: string; text: string }) => {
    if (selected) return; // already chosen
    setSelected(option.number);
    window.dispatchEvent(
      new CustomEvent('jarvis-option-select', { detail: option.text })
    );
  };

  return (
    <div>
      {/* Preamble text rendered as markdown */}
      {parsed.preamble && (
        <div className="prose max-w-none mb-3">
          <ReactMarkdown
            remarkPlugins={[remarkGfm, remarkMath]}
            rehypePlugins={[[rehypeHighlight, { detect: true }], rehypeKatex]}
            components={{ pre: CodeBlockPre }}
          >
            {parsed.preamble}
          </ReactMarkdown>
        </div>
      )}

      {/* Option buttons */}
      <div
        style={{
          display: 'flex',
          flexDirection: 'column',
          gap: '0.5rem',
          marginTop: parsed.preamble ? '0' : '0.25rem',
        }}
      >
        {parsed.options.map((opt) => {
          const isSelected = selected === opt.number;
          const isDimmed = selected !== null && !isSelected;

          return (
            <button
              key={opt.number}
              onClick={() => handleSelect(opt)}
              disabled={selected !== null}
              style={{
                display: 'flex',
                alignItems: 'center',
                gap: '0.75rem',
                padding: '0.6rem 1rem',
                borderRadius: 'var(--radius-lg)',
                border: isSelected
                  ? '1.5px solid var(--color-accent)'
                  : '1.5px solid var(--color-border)',
                background: isSelected
                  ? 'var(--color-accent-subtle)'
                  : 'var(--color-bg-secondary)',
                color: isDimmed
                  ? 'var(--color-text-tertiary)'
                  : 'var(--color-text)',
                cursor: selected ? 'default' : 'pointer',
                opacity: isDimmed ? 0.45 : 1,
                textAlign: 'left',
                fontSize: '0.875rem',
                transition: 'all 0.15s ease',
                width: '100%',
              }}
              onMouseEnter={(e) => {
                if (!selected) {
                  e.currentTarget.style.borderColor = 'var(--color-accent)';
                  e.currentTarget.style.background = 'var(--color-accent-subtle)';
                }
              }}
              onMouseLeave={(e) => {
                if (!selected) {
                  e.currentTarget.style.borderColor = 'var(--color-border)';
                  e.currentTarget.style.background = 'var(--color-bg-secondary)';
                }
              }}
            >
              {/* Number badge */}
              <span
                style={{
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  minWidth: '1.5rem',
                  height: '1.5rem',
                  borderRadius: '50%',
                  background: isSelected ? 'var(--color-accent)' : 'var(--color-bg-tertiary)',
                  color: isSelected ? 'var(--color-on-accent)' : 'var(--color-text-secondary)',
                  fontSize: '0.75rem',
                  fontWeight: 600,
                  flexShrink: 0,
                  transition: 'all 0.15s ease',
                }}
              >
                {opt.number}
              </span>
              <span>{opt.text}</span>
            </button>
          );
        })}
      </div>
    </div>
  );
}

export function MessageBubble({ message }: Props) {
  const isUser = message.role === 'user';

  const cleanContent = useMemo(() => stripThinkTags(message.content), [message.content]);

  // Build a refâ†’source lookup once per render. Memoized so the rehype plugin
  // identity stays stable until the source list actually changes.
  const sourcesMap = useMemo(() => {
    const m = new Map<number, NonNullable<ChatMessage['researchSources']>[number]>();
    for (const s of message.researchSources ?? []) {
      if (typeof s.ref === 'number') m.set(s.ref, s);
    }
    return m;
  }, [message.researchSources]);

  const rehypePlugins = useMemo(() => {
    const base: any[] = [[rehypeHighlight, { detect: true }], rehypeKatex];
    if (sourcesMap.size > 0) base.push([rehypeCitations, { sources: sourcesMap }]);
    return base;
  }, [sourcesMap]);

  if (isUser) {
    return (
      <div className="flex justify-end mb-4">
        <div
          className="max-w-[85%] px-4 py-2.5 text-sm leading-relaxed"
          style={{
            background: 'var(--color-user-bubble)',
            color: 'var(--color-user-bubble-text)',
            borderRadius: 'var(--radius-xl) var(--radius-xl) var(--radius-sm) var(--radius-xl)',
            whiteSpace: 'pre-wrap',
            wordBreak: 'break-word',
          }}
        >
          {message.content}
        </div>
      </div>
    );
  }

<<<<<<< ours
  const cleanContent = useMemo(() => stripThinkTags(message.content), [message.content]);
  const parsedOptions = useMemo(() => parseNumberedOptions(cleanContent), [cleanContent]);

||||||| base
  const cleanContent = useMemo(() => stripThinkTags(message.content), [message.content]);

  // Build a refâ†’source lookup once per render. Memoized so the rehype plugin
  // identity stays stable until the source list actually changes.
  const sourcesMap = useMemo(() => {
    const m = new Map<number, NonNullable<ChatMessage['researchSources']>[number]>();
    for (const s of message.researchSources ?? []) {
      if (typeof s.ref === 'number') m.set(s.ref, s);
    }
    return m;
  }, [message.researchSources]);

  const rehypePlugins = useMemo(() => {
    const base: any[] = [[rehypeHighlight, { detect: true }], rehypeKatex];
    if (sourcesMap.size > 0) base.push([rehypeCitations, { sources: sourcesMap }]);
    return base;
  }, [sourcesMap]);

=======
>>>>>>> theirs
  return (
    <div className="group mb-6">
      {/* Tool calls */}
      {message.toolCalls && message.toolCalls.length > 0 && (
        <div className="mb-3 flex flex-col gap-2">
          {message.toolCalls.map((tc) => (
            <ToolCallCard key={tc.id} toolCall={tc} />
          ))}
        </div>
      )}

      {/* Audio player (e.g. morning digest) */}
      {message.audio?.url && <AudioPlayer src={message.audio.url} />}

      {/* Assistant message â€” numbered options OR regular markdown */}
      {cleanContent && (
        parsedOptions ? (
          <NumberedOptionButtons parsed={parsedOptions} />
        ) : (
          <div className="prose max-w-none">
            <ReactMarkdown
              remarkPlugins={[remarkGfm, remarkMath]}
              rehypePlugins={[[rehypeHighlight, { detect: true }], rehypeKatex]}
              components={{
                pre: CodeBlockPre,
              }}
            >
              {cleanContent}
            </ReactMarkdown>
          </div>
        )
      )}

      {/* Footer: copy + x-ray */}
      <div className="flex items-center gap-2 mt-1.5">
        <CopyMessageButton content={cleanContent} />
      </div>
      <XRayFooter usage={message.usage} telemetry={message.telemetry} />
    </div>
  );
}


## ===== frontend/src/components/CommandPalette.tsx : OUR COMMITS SINCE AUTHOR BASE =====
f14707c3 fix(ui): tool chip latency is seconds not ms; clear mojibake in chip args and model palette
daafc769 fix: speech subsystem TTS streaming, backend file logging, uvicorn console fix, restore .gitignore
670c3aaf feat: numbered question UI buttons, sub-bullet fix, trailing text relaxed, shell_exec utf-8 encoding, croniter installed, persistent API keys hydrate from Rust backend, fix: use npx tauri build for full Rust exe compile (npm run build:tauri is frontend only)
6015a448 feat: mic button fix, agent work, cloud router updates, HUD improvements
275a9fa1 feat: Graystone Lab cloud integration

## ===== frontend/src/components/CommandPalette.tsx : CONFLICTED WORKING FILE (diff3) =====
import { useState, useRef, useEffect, useCallback } from 'react';
import { Search, Cpu, X, Download, Loader2, Trash2, Check, Cloud, Key, Eye, EyeOff } from 'lucide-react';
import { useAppStore } from '../lib/store';
import {
  pullModel,
  deleteModel,
  fetchModels,
  preloadModel,
  isTauri,
  getCloudKeyStatus,
  saveCloudKey,
} from '../lib/api';

/** Popular models that users can download from the catalogue. */
const CATALOGUE_MODELS = [
  { id: 'qwen3.5:0.8b', size: '~1 GB', desc: 'Qwen 3.5 0.8B - fast, lightweight' },
  { id: 'qwen3.5:2b', size: '~2.7 GB', desc: 'Qwen 3.5 2B' },
  { id: 'qwen3.5:4b', size: '~3.4 GB', desc: 'Qwen 3.5 4B - recommended default' },
  { id: 'qwen3.5:9b', size: '~6.6 GB', desc: 'Qwen 3.5 9B' },
  { id: 'qwen3.5:27b', size: '~17 GB', desc: 'Qwen 3.5 27B' },
  { id: 'qwen3.5:35b', size: '~24 GB', desc: 'Qwen 3.5 35B' },
  { id: 'qwen3.5:122b', size: '~81 GB', desc: 'Qwen 3.5 122B - largest' },
  { id: 'llama3.3:latest', size: '~4.9 GB', desc: 'Llama 3.3 8B' },
  { id: 'mistral:latest', size: '~4.1 GB', desc: 'Mistral 7B' },
  { id: 'gemma3:latest', size: '~3.3 GB', desc: 'Gemma 3 4B' },
  { id: 'deepseek-r1:7b', size: '~4.7 GB', desc: 'DeepSeek R1 7B' },
  { id: 'phi4:latest', size: '~9.1 GB', desc: 'Phi-4 14B' },
];

/** Cloud provider definitions */
interface CloudProvider {
  name: string;
  envKey: string;
  models: Array<{ id: string; desc: string }>;
}

const CLOUD_PROVIDERS: CloudProvider[] = [
  {
    name: 'OpenAI',
    envKey: 'OPENAI_API_KEY',
    models: [
      { id: 'gpt-4o', desc: 'GPT-4o - fast, multimodal' },
      { id: 'gpt-4o-mini', desc: 'GPT-4o Mini - cheap, fast' },
      { id: 'o3-mini', desc: 'o3-mini - reasoning' },
    ],
  },
  {
    name: 'Anthropic',
    envKey: 'ANTHROPIC_API_KEY',
    models: [
      { id: 'claude-sonnet-4-6', desc: 'Claude Sonnet 4.6 - balanced' },
      { id: 'claude-opus-4-6', desc: 'Claude Opus 4.6 - most capable' },
      { id: 'claude-haiku-4-5', desc: 'Claude Haiku 4.5 - fastest' },
    ],
  },
  {
    name: 'Google',
    envKey: 'GEMINI_API_KEY',
    models: [
      { id: 'gemini-2.5-pro', desc: 'Gemini 2.5 Pro - flagship' },
      { id: 'gemini-2.5-flash', desc: 'Gemini 2.5 Flash - fast' },
      { id: 'gemini-3-pro', desc: 'Gemini 3 Pro - latest' },
    ],
  },
  {
    name: 'OpenRouter',
<<<<<<< ours
    storageKey: 'openjarvis-openrouter-key',
    envKey: 'OPENROUTER_API_KEY',
||||||| base
    envKey: 'OPENROUTER_API_KEY',
    storageKey: 'openjarvis-openrouter-key',
=======
    envKey: 'OPENROUTER_API_KEY',
>>>>>>> theirs
    models: [
      { id: 'openrouter/auto', desc: 'Auto - best model for the task' },
      { id: 'openrouter/openai/gpt-oss-120b:free', desc: 'GPT OSS 120B - free' },
      { id: 'openrouter/openai/gpt-oss-20b:free', desc: 'GPT OSS 20B - free' },
      { id: 'openrouter/nvidia/nemotron-3-ultra-550b-a55b:free', desc: 'Nemotron Ultra 550B - free' },
      { id: 'openrouter/nvidia/nemotron-3-super-120b-a12b:free', desc: 'Nemotron Super 120B - free' },
      { id: 'openrouter/nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free', desc: 'Nemotron Nano Omni 30B Reasoning - free' },
      { id: 'openrouter/nvidia/nemotron-3-nano-30b-a3b:free', desc: 'Nemotron Nano 30B - free' },
      { id: 'openrouter/nvidia/nemotron-nano-12b-v2-vl:free', desc: 'Nemotron Nano 12B - free' },
      { id: 'openrouter/nvidia/nemotron-nano-9b-v2:free', desc: 'Nemotron Nano 9B - free' },
      { id: 'openrouter/google/gemma-4-31b-it:free', desc: 'Gemma 4 31B - free' },
      { id: 'openrouter/poolside/laguna-m.1:free', desc: 'Laguna M.1 - free' },
      { id: 'openrouter/poolside/laguna-xs.2:free', desc: 'Laguna XS.2 - free' },
      { id: 'openrouter/liquid/lfm-2.5-1.2b-thinking:free', desc: 'LFM 2.5 1.2B Thinking - free' },
      { id: 'openrouter/liquid/lfm-2.5-1.2b-instruct:free', desc: 'LFM 2.5 1.2B Instruct - free' },
      { id: 'openrouter/nex-agi/nex-n2-pro:free', desc: 'Nex N2 Pro - free' },
      { id: 'openrouter/nvidia/nemotron-3.5-content-safety:free', desc: 'Nemotron 3.5 Content Safety - free' },
      { id: 'openrouter/owl-alpha', desc: 'OWL Alpha' },
    ],
  },
];

type Tab = 'installed' | 'catalogue' | 'cloud';

export function CommandPalette() {
  const [query, setQuery] = useState('');
  const [selectedIdx, setSelectedIdx] = useState(0);
  const [tab, setTab] = useState<Tab>('installed');
  const [pulling, setPulling] = useState<string | null>(null);
  const [pullError, setPullError] = useState<string | null>(null);
  const [pullSuccess, setPullSuccess] = useState<string | null>(null);
  const [deleting, setDeleting] = useState<string | null>(null);
  const [customModel, setCustomModel] = useState('');
  const [showKeys, setShowKeys] = useState<Record<string, boolean>>({});
  const [apiKeys, setApiKeys] = useState<Record<string, string>>({});
  const [cloudKeyStatus, setCloudKeyStatus] = useState<Record<string, boolean>>({});
  const [cloudKeyError, setCloudKeyError] = useState<string | null>(null);
  const [savingKey, setSavingKey] = useState<string | null>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  const models = useAppStore((s) => s.models);
  const selectedModel = useAppStore((s) => s.selectedModel);
  const setSelectedModel = useAppStore((s) => s.setSelectedModel);
  const setModels = useAppStore((s) => s.setModels);
  const setCommandPaletteOpen = useAppStore((s) => s.setCommandPaletteOpen);

  useEffect(() => {
    if (!isTauri()) return;
    import("@tauri-apps/api/core").then(({ invoke }) => {
      invoke("get_cloud_key_status").then((status) => {
        setApiKeys((prev) => {
          const next = { ...prev };
          for (const p of CLOUD_PROVIDERS) {
            const entry = (status as Array<{key: string; value: string; set: boolean}>).find((s) => s.key === p.envKey);
            if (entry && entry.set && !next[p.storageKey]) {
              next[p.storageKey] = "__backend_set__";
            }
          }
          return next;
        });
      }).catch(() => {});
    });
  }, []);

  const installedIds = new Set(models.map((m) => m.id));
  const desktopKeyStorage = isTauri();

  const refreshCloudKeyStatus = useCallback(async () => {
    if (!desktopKeyStorage) {
      setCloudKeyStatus({});
      return;
    }
    try {
      setCloudKeyStatus(await getCloudKeyStatus());
      setCloudKeyError(null);
    } catch (e: any) {
      setCloudKeyError(e?.message || 'Failed to read cloud key status');
    }
  }, [desktopKeyStorage]);

  const filtered = tab === 'installed'
    ? (query
        ? models.filter((m) => m.id.toLowerCase().includes(query.toLowerCase()))
        : models)
    : tab === 'catalogue'
    ? CATALOGUE_MODELS.filter((m) =>
        !installedIds.has(m.id) &&
        (!query || m.id.toLowerCase().includes(query.toLowerCase()) || m.desc.toLowerCase().includes(query.toLowerCase()))
      )
    : []; // cloud tab doesn't use filtered

  useEffect(() => {
    inputRef.current?.focus();
  }, []);

  useEffect(() => {
    void refreshCloudKeyStatus();
  }, [refreshCloudKeyStatus]);

  useEffect(() => {
    setSelectedIdx(0);
  }, [query, tab]);

  useEffect(() => {
    if (pullSuccess) {
      const t = setTimeout(() => setPullSuccess(null), 3000);
      return () => clearTimeout(t);
    }
  }, [pullSuccess]);

  const handleSelect = async (modelId: string, owner?: string) => {
    const previousModel = selectedModel;
    setSelectedModel(modelId);
    setCommandPaletteOpen(false);

    if (modelId !== previousModel) {
      const { setModelLoading, addLogEntry } = useAppStore.getState();
      setModelLoading(true);
      addLogEntry({ timestamp: Date.now(), level: 'info', category: 'model', message: `Switching to ${modelId}...` });
      try {
        await preloadModel(modelId, owner);
        addLogEntry({ timestamp: Date.now(), level: 'info', category: 'model', message: `${modelId} loaded` });
      } catch (e: any) {
        addLogEntry({ timestamp: Date.now(), level: 'error', category: 'model', message: `Failed to load ${modelId}: ${e.message}` });
      } finally {
        setModelLoading(false);
      }
    }
  };

  const refreshModels = async () => {
    try {
      const m = await fetchModels();
      setModels(m);
    } catch {}
  };

  const handlePull = async (modelId: string) => {
    setPulling(modelId);
    setPullError(null);
    try {
      await pullModel(modelId);
      setPullSuccess(modelId);
      useAppStore.getState().addLogEntry({
        timestamp: Date.now(), level: 'info', category: 'model',
        message: `Downloaded ${modelId}`,
      });
      await refreshModels();
      setSelectedModel(modelId);
    } catch (e: any) {
      setPullError(e.message || 'Download failed');
      useAppStore.getState().addLogEntry({
        timestamp: Date.now(), level: 'error', category: 'model',
        message: `Download failed for ${modelId}: ${e.message}`,
      });
    } finally {
      setPulling(null);
    }
  };

  const handleDelete = async (modelId: string) => {
    setDeleting(modelId);
    try {
      await deleteModel(modelId);
      useAppStore.getState().addLogEntry({
        timestamp: Date.now(), level: 'info', category: 'model',
        message: `Deleted ${modelId}`,
      });
      await refreshModels();
      if (selectedModel === modelId) {
        const remaining = models.filter((m) => m.id !== modelId);
        if (remaining.length > 0) setSelectedModel(remaining[0].id);
      }
    } catch {} finally {
      setDeleting(null);
    }
  };

  const handleCustomPull = async () => {
    const name = customModel.trim();
    if (!name) return;
    await handlePull(name);
    setCustomModel('');
  };

  const handleSaveKey = async (provider: CloudProvider, value: string) => {
    const keyValue = value.trim();
    setSavingKey(provider.envKey);
    setCloudKeyError(null);

    try {
      await saveCloudKey(provider.envKey, keyValue);
      setApiKeys((prev) => ({ ...prev, [provider.envKey]: '' }));
      await refreshCloudKeyStatus();
      useAppStore.getState().addLogEntry({
        timestamp: Date.now(), level: 'info', category: 'model',
        message: `${provider.name} API key ${keyValue ? 'saved' : 'removed'}. Refreshing model list...`,
      });
      await refreshModels();
    } catch (e: any) {
      setCloudKeyError(e?.message || `Failed to save ${provider.name} API key`);
    } finally {
      setSavingKey(null);
    }
  };

<<<<<<< ours
    useAppStore.getState().addLogEntry({
      timestamp: Date.now(), level: 'info', category: 'model',
      message: `${provider.name} API key ${value ? 'saved' : 'removed'}. Refreshing model list...`,
    });

    // Refresh the model list so cloud models appear immediately.
    await refreshModels();
||||||| base
    useAppStore.getState().addLogEntry({
      timestamp: Date.now(), level: 'info', category: 'model',
      message: `${provider.name} API key ${value ? 'saved' : 'removed'}. Refreshing model listâ€¦`,
    });

    // Refresh the model list so cloud models appear immediately.
    await refreshModels();
=======
  const handleKeyBlur = (provider: CloudProvider) => {
    const draft = apiKeys[provider.envKey] || '';
    if (draft.trim()) void handleSaveKey(provider, draft);
>>>>>>> theirs
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Escape') {
      setCommandPaletteOpen(false);
    } else if (e.key === 'ArrowDown') {
      e.preventDefault();
      setSelectedIdx((i) => Math.min(i + 1, filtered.length - 1));
    } else if (e.key === 'ArrowUp') {
      e.preventDefault();
      setSelectedIdx((i) => Math.max(i - 1, 0));
    } else if (e.key === 'Enter' && tab === 'installed' && filtered.length > 0) {
      e.preventDefault();
      const model = filtered[selectedIdx] as (typeof models)[number];
      handleSelect(model.id, model.owned_by);
    }
  };

  const TAB_LABELS: Record<Tab, string> = {
    installed: `Installed Models (${models.length})`,
    catalogue: 'Download',
    cloud: 'Cloud Models',
  };

  return (
    <div
      className="fixed inset-0 z-50 flex items-start justify-center pt-[15vh]"
      onClick={() => setCommandPaletteOpen(false)}
    >
      <div className="fixed inset-0" style={{ background: 'rgba(0,0,0,0.5)' }} />

      <div
        className="relative w-full max-w-lg rounded-xl overflow-hidden"
        style={{
          background: 'var(--color-surface)',
          border: '1px solid var(--color-border)',
          boxShadow: 'var(--shadow-lg)',
        }}
        onClick={(e) => e.stopPropagation()}
      >
        {/* Tabs */}
        <div className="flex" style={{ borderBottom: '1px solid var(--color-border)' }}>
          {(['installed', 'catalogue', 'cloud'] as Tab[]).map((t) => (
            <button
              key={t}
              onClick={() => setTab(t)}
              className="flex-1 px-3 py-2.5 text-xs font-medium transition-colors cursor-pointer"
              style={{
                color: tab === t ? 'var(--color-accent)' : 'var(--color-text-tertiary)',
                borderBottom: tab === t ? '2px solid var(--color-accent)' : '2px solid transparent',
                background: 'transparent',
              }}
            >
              {TAB_LABELS[t]}
            </button>
          ))}
        </div>

        {/* Search (not for cloud tab) */}
        {tab !== 'cloud' && (
          <div
            className="flex items-center gap-3 px-4 py-3"
            style={{ borderBottom: '1px solid var(--color-border)' }}
          >
            <Search size={18} style={{ color: 'var(--color-text-tertiary)' }} />
            <input
              ref={inputRef}
              type="text"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder={tab === 'installed' ? 'Search installed models...' : 'Search models to download...'}
              className="flex-1 bg-transparent outline-none text-sm"
              style={{ color: 'var(--color-text)' }}
            />
            <button
              onClick={() => setCommandPaletteOpen(false)}
              className="p-1 rounded cursor-pointer"
              style={{ color: 'var(--color-text-tertiary)' }}
            >
              <X size={16} />
            </button>
          </div>
        )}

        {/* Status messages */}
        {pullError && (
          <div className="px-4 py-2 text-xs" style={{ color: 'var(--color-error)', background: 'rgba(220,38,38,0.05)' }}>
            {pullError}
          </div>
        )}
        {pullSuccess && (
          <div className="px-4 py-2 text-xs flex items-center gap-1.5" style={{ color: 'var(--color-success)', background: 'color-mix(in srgb, var(--color-success) 5%, transparent)' }}>
            <Check size={12} /> Downloaded {pullSuccess} successfully
          </div>
        )}
        {tab === 'cloud' && cloudKeyError && (
          <div className="px-4 py-2 text-xs" style={{ color: 'var(--color-error)', background: 'rgba(220,38,38,0.05)' }}>
            {cloudKeyError}
          </div>
        )}

        {/* Results */}
        <div className="max-h-[400px] overflow-y-auto py-2">
          {tab === 'installed' ? (
            filtered.length === 0 ? (
              <div className="px-4 py-6 text-center text-sm" style={{ color: 'var(--color-text-tertiary)' }}>
                {models.length === 0
                  ? 'No models available - switch to "Download" to get started'
                  : 'No matching models'}
              </div>
            ) : (
              (filtered as typeof models).map((model, idx) => {
                const isActive = model.id === selectedModel;
                const isSelected = idx === selectedIdx;
                const isDeleting = deleting === model.id;
                return (
                  <div
                    key={model.id}
                    className="flex items-center gap-3 w-full px-4 py-2.5 transition-colors"
                    style={{ background: isSelected ? 'var(--color-bg-secondary)' : 'transparent' }}
                    onMouseEnter={() => setSelectedIdx(idx)}
                  >
                    <button
                      onClick={() => handleSelect(model.id, model.owned_by)}
                      className="flex items-center gap-3 flex-1 min-w-0 text-left cursor-pointer"
                      style={{ background: 'none', border: 'none', padding: 0 }}
                    >
                      {model.owned_by === 'litellm' ? (
                        <Cloud size={16} style={{ color: isActive ? 'var(--color-accent)' : 'var(--color-text-tertiary)' }} />
                      ) : (
                        <Cpu size={16} style={{ color: isActive ? 'var(--color-accent)' : 'var(--color-text-tertiary)' }} />
                      )}
                      <div className="flex-1 min-w-0">
                        <div className="text-sm truncate" style={{ color: isActive ? 'var(--color-accent)' : 'var(--color-text)', fontWeight: isActive ? 500 : 400 }}>
                          {model.id}
                        </div>
                      </div>
                      {isActive && (
                        <span className="text-[10px] px-2 py-0.5 rounded-full" style={{ background: 'var(--color-accent-subtle)', color: 'var(--color-accent)' }}>
                          Active
                        </span>
                      )}
                    </button>
                    {model.owned_by !== 'litellm' && (
                      <button
                        onClick={() => handleDelete(model.id)}
                        disabled={isDeleting}
                        className="p-1 rounded transition-colors cursor-pointer"
                        style={{ color: 'var(--color-text-tertiary)', opacity: 0 }}
                        title="Delete model"
                        onMouseEnter={(e) => { e.currentTarget.style.opacity = '1'; e.currentTarget.style.color = 'var(--color-error)'; }}
                        onMouseLeave={(e) => { e.currentTarget.style.opacity = '0'; e.currentTarget.style.color = 'var(--color-text-tertiary)'; }}
                      >
                        {isDeleting ? <Loader2 size={14} className="animate-spin" /> : <Trash2 size={14} />}
                      </button>
                    )}
                  </div>
                );
              })
            )
          ) : tab === 'catalogue' ? (
            <>
              {(filtered as typeof CATALOGUE_MODELS).map((model) => {
                const isPulling = pulling === model.id;
                const justInstalled = pullSuccess === model.id;
                return (
                  <div key={model.id} className="flex items-center gap-3 w-full px-4 py-2.5">
                    <Download size={16} style={{ color: 'var(--color-text-tertiary)' }} />
                    <div className="flex-1 min-w-0">
                      <div className="text-sm truncate" style={{ color: 'var(--color-text)' }}>{model.id}</div>
                      <div className="text-[11px]" style={{ color: 'var(--color-text-tertiary)' }}>{model.desc} &middot; {model.size}</div>
                    </div>
                    <button
                      onClick={() => handlePull(model.id)}
                      disabled={isPulling || !!pulling}
                      className="flex items-center gap-1.5 px-3 py-1 rounded-lg text-xs font-medium cursor-pointer"
                      style={{
                        background: justInstalled ? 'var(--color-accent-subtle)' : 'var(--color-accent)',
                        color: justInstalled ? 'var(--color-accent)' : 'var(--color-on-accent)',
                        opacity: (isPulling || (pulling && !isPulling)) ? 0.5 : 1,
                      }}
                    >
                      {isPulling ? <><Loader2 size={12} className="animate-spin" /> Downloading...</> :
                       justInstalled ? <><Check size={12} /> Installed</> :
                       <><Download size={12} /> Download</>}
                    </button>
                  </div>
                );
              })}
              <div className="px-4 py-3 mt-1" style={{ borderTop: '1px solid var(--color-border)' }}>
                <div className="text-[11px] mb-2" style={{ color: 'var(--color-text-tertiary)' }}>Or enter any Ollama model name:</div>
                <div className="flex gap-2">
                  <input
                    type="text" value={customModel}
                    onChange={(e) => setCustomModel(e.target.value)}
                    onKeyDown={(e) => { if (e.key === 'Enter') { e.preventDefault(); handleCustomPull(); } }}
                    placeholder="e.g. codellama:7b"
                    className="flex-1 text-sm px-3 py-1.5 rounded-lg outline-none"
                    style={{ background: 'var(--color-bg-secondary)', color: 'var(--color-text)', border: '1px solid var(--color-border)' }}
                  />
                  <button
                    onClick={handleCustomPull} disabled={!customModel.trim() || !!pulling}
                    className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-medium cursor-pointer"
                    style={{ background: 'var(--color-accent)', color: 'var(--color-on-accent)', opacity: (!customModel.trim() || pulling) ? 0.5 : 1 }}
                  >
                    <Download size={12} /> Pull
                  </button>
                </div>
              </div>
            </>
          ) : (
            /* -- Cloud Models tab -- */
            <div className="px-4 py-2">
              <div className="text-[11px] mb-3" style={{ color: 'var(--color-text-tertiary)' }}>
                {desktopKeyStorage
                  ? 'Add your API keys to use cloud models. Keys are stored in secure desktop storage.'
                  : 'Configure cloud provider keys in the server environment to use cloud models.'}
              </div>

              {CLOUD_PROVIDERS.map((provider) => {
                const key = apiKeys[provider.envKey] || '';
                const hasSavedKey = !!cloudKeyStatus[provider.envKey];
                const hasKey = hasSavedKey || !!key.trim();
                const isVisible = showKeys[provider.envKey];
                const isSaving = savingKey === provider.envKey;

                return (
                  <div key={provider.name} className="mb-4">
                    <div className="flex items-center gap-2 mb-2">
                      <Cloud size={14} style={{ color: hasKey ? 'var(--color-success)' : 'var(--color-text-tertiary)' }} />
                      <span className="text-xs font-medium" style={{ color: 'var(--color-text)' }}>{provider.name}</span>
                      {hasKey && (
                        <span className="text-[10px] px-1.5 py-0.5 rounded-full" style={{ background: 'color-mix(in srgb, var(--color-success) 10%, transparent)', color: 'var(--color-success)' }}>
                          Connected
                        </span>
                      )}
                    </div>

                    {/* API key input */}
                    <div className="flex gap-1.5 mb-2">
                      <div className="flex-1 flex items-center rounded-lg" style={{ background: 'var(--color-bg-secondary)', border: '1px solid var(--color-border)' }}>
                        <Key size={12} className="ml-2.5 shrink-0" style={{ color: 'var(--color-text-tertiary)' }} />
                        <input
                          type={isVisible ? 'text' : 'password'}
                          value={key}
                          onChange={(e) => setApiKeys((prev) => ({ ...prev, [provider.envKey]: e.target.value }))}
                          onBlur={() => handleKeyBlur(provider)}
                          placeholder={hasSavedKey ? 'Saved in secure storage' : provider.envKey}
                          disabled={!desktopKeyStorage || isSaving}
                          className="flex-1 text-xs px-2 py-1.5 bg-transparent outline-none font-mono"
                          style={{ color: 'var(--color-text)' }}
                        />
                        <button
                          onClick={() => setShowKeys((prev) => ({ ...prev, [provider.envKey]: !prev[provider.envKey] }))}
                          className="px-2 cursor-pointer" style={{ color: 'var(--color-text-tertiary)' }}
                        >
                          {isVisible ? <EyeOff size={12} /> : <Eye size={12} />}
                        </button>
                      </div>
                      {hasSavedKey && (
                        <button
                          onClick={() => handleSaveKey(provider, '')}
                          disabled={isSaving}
                          className="px-2 py-1 rounded-lg text-[10px] cursor-pointer"
                          style={{ color: 'var(--color-error)', border: '1px solid var(--color-error)', opacity: isSaving ? 0.5 : 1 }}
                        >
                          {isSaving ? 'Saving' : 'Remove'}
                        </button>
                      )}
                    </div>

                    {/* Models for this provider (only show if key is set) */}
                    {hasKey && (
                      <div className="ml-5 flex flex-col gap-1">
                        {provider.models.map((model) => {
                          const isActive = model.id === selectedModel;
                          return (
                            <button
                              key={model.id}
                              onClick={() => handleSelect(model.id)}
                              className="flex items-center gap-2 px-2.5 py-1.5 rounded-lg text-left cursor-pointer transition-colors"
                              style={{ background: isActive ? 'var(--color-accent-subtle)' : 'transparent' }}
                              onMouseEnter={(e) => { if (!isActive) e.currentTarget.style.background = 'var(--color-bg-secondary)'; }}
                              onMouseLeave={(e) => { if (!isActive) e.currentTarget.style.background = 'transparent'; }}
                            >
                              <Cloud size={12} style={{ color: isActive ? 'var(--color-accent)' : 'var(--color-text-tertiary)' }} />
                              <div className="flex-1 min-w-0">
                                <div className="text-xs truncate" style={{ color: isActive ? 'var(--color-accent)' : 'var(--color-text)', fontWeight: isActive ? 500 : 400 }}>
                                  {model.id}
                                </div>
                                <div className="text-[10px] truncate" style={{ color: 'var(--color-text-tertiary)' }}>
                                  {model.desc}
                                </div>
                              </div>
                              {isActive && (
                                <span className="text-[9px] px-1.5 py-0.5 rounded-full shrink-0" style={{ background: 'var(--color-accent-subtle)', color: 'var(--color-accent)' }}>
                                  Active
                                </span>
                              )}
                            </button>
                          );
                        })}
                      </div>
                    )}
                  </div>
                );
              })}
            </div>
          )}
        </div>

        {/* Footer */}
        <div
          className="flex items-center gap-4 px-4 py-2 text-[11px]"
          style={{ borderTop: '1px solid var(--color-border)', color: 'var(--color-text-tertiary)' }}
        >
          {tab === 'installed' ? (
            <>
              <span><kbd className="font-mono">Up/Down</kbd> Navigate</span>
              <span><kbd className="font-mono">Enter</kbd> Select</span>
              <span><kbd className="font-mono">Esc</kbd> Close</span>
            </>
          ) : tab === 'catalogue' ? (
            <span>Models are downloaded from the Ollama registry</span>
          ) : (
            <span>API keys are stored locally and never sent to OpenJarvis servers</span>
          )}
        </div>
      </div>
    </div>
  );
}


## ===== frontend/src/components/SetupScreen.tsx : OUR COMMITS SINCE AUTHOR BASE =====
bc498a16 feat: Arc Reactor ThinkingCircle, fix env loading, fix project root, add research types, remove debug code
383ccd5e Graystone Lab fixes: - Disable auth middleware for local network use (app.py) - Fix SetupScreen ollama_ready step logic (SetupScreen.tsx) - Add ollama_ready to SetupStatus interface (api.ts) - Remove uv sync and startup model checks from boot sequence (lib.rs) - Fix configured_ollama_host to ensure http:// prefix (lib.rs) - Add system32 hardcoded path to find_project_root (lib.rs) - Fix config.toml: server host 127.0.0.1, port 8010 - Input focus fix after response (InputArea.tsx) - Thinking spinner during generation (InputArea.tsx)
f2fcb30c Graystone Lab: remote MCP/Ollama integration, Rust extension, UI fixes

## ===== frontend/src/components/SetupScreen.tsx : CONFLICTED WORKING FILE (diff3) =====
<<<<<<< ours
import { useState, useEffect, useCallback } from 'react';
import { Loader2, CheckCircle2, XCircle, Server } from 'lucide-react';
import { getSetupStatus, type SetupStatus } from '../lib/api';
||||||| base
import { useState, useEffect, useCallback } from 'react';
import { Loader2, CheckCircle2, XCircle, Cpu, Server, Database } from 'lucide-react';
import { getSetupStatus, type SetupStatus } from '../lib/api';
=======
import { useState, useEffect, useCallback, useRef } from 'react';
import { Loader2, CheckCircle2, XCircle, Cpu, Server, Database } from 'lucide-react';
import {
  getSetupStatus,
  fetchModels,
  fetchRecommendedModel,
  resetInferenceSource,
  type SetupStatus,
} from '../lib/api';
import { useAppStore } from '../lib/store';
import { isEmbedOnlyModel } from '../lib/model-capabilities';
import { InferenceRecoveryButton, InferenceSourceSetup } from './InferenceSourceSetup';
>>>>>>> theirs

const STEPS = [
  { key: 'server_ready', label: 'API Server', icon: Server, detail: 'Starting server...' },
] as const;

type StepKey = (typeof STEPS)[number]['key'];

function StepRow({
  icon: Icon,
  label,
  done,
  active,
  detail,
}: {
  icon: typeof Server;
  label: string;
  done: boolean;
  active: boolean;
  detail: string;
}) {
  return (
    <div className="flex items-center gap-3 py-3">
      <div className="flex-shrink-0">
        {done ? (
          <CheckCircle2 size={20} style={{ color: 'var(--color-success)' }} />
        ) : active ? (
          <Loader2 size={20} className="animate-spin" style={{ color: 'var(--color-accent)' }} />
        ) : (
          <div
            className="w-5 h-5 rounded-full border-2"
            style={{ borderColor: 'var(--color-border)' }}
          />
        )}
      </div>
      <div className="flex-1">
        <div className="flex items-center gap-2">
          <Icon size={16} style={{ color: 'var(--color-text-secondary)' }} />
          <span className="text-sm font-medium" style={{ color: 'var(--color-text)' }}>
            {label}
          </span>
        </div>
        {active && (
          <div className="text-xs mt-0.5" style={{ color: 'var(--color-text-tertiary)' }}>
            {detail}
          </div>
        )}
      </div>
    </div>
  );
}

export function SetupScreen({ onReady }: { onReady: () => void }) {
  const [status, setStatus] = useState<SetupStatus | null>(null);
<<<<<<< ours

||||||| base
=======
  const [statusChecked, setStatusChecked] = useState(false);
  const [setupInitiated, setSetupInitiated] = useState(false);
  const [recovering, setRecovering] = useState(false);
  const [recoveryError, setRecoveryError] = useState('');
  const handedOffRef = useRef(false);
>>>>>>> theirs
  const poll = useCallback(async () => {
    const s = await getSetupStatus();
    if (s) setStatus(s);
    setStatusChecked(true);
    if (s?.phase === 'ready' && !handedOffRef.current) {
      handedOffRef.current = true;
      // Pre-select a model BEFORE handing off so the chat is usable on
      // first send. Without this, the main app's post-mount fetch can
      // lose a race to a fast first message and Ollama 400s.
      try {
        const [models, rec] = await Promise.all([
          fetchModels().catch(() => []),
          fetchRecommendedModel().catch(() => ({ model: '', reason: '' })),
        ]);
        const store = useAppStore.getState();
        const hadSelection = !!store.selectedModel;
        store.setModels(models);
        store.setModelsLoading(false);
        const chatModels = models.filter((m) => !isEmbedOnlyModel(m.id));
        const recommended = rec.model && chatModels.some((m) => m.id === rec.model)
          ? rec.model
          : chatModels[0]?.id || '';
        if (recommended && !hadSelection) {
          store.setSelectedModel(recommended);
        }
      } catch {
        // Non-fatal: store.setModels auto-selects on later fetch, and
        // the InputArea guards the empty-model case with a toast.
      }
      setTimeout(() => onReady(), 600);
    }
  }, [onReady]);

  const changeInferenceSource = useCallback(async () => {
    setRecovering(true);
    setRecoveryError('');
    try {
      await resetInferenceSource();
      handedOffRef.current = false;
      setSetupInitiated(false);
      setStatus(null);
      await poll();
    } catch (error) {
      setRecoveryError(error instanceof Error ? error.message : String(error));
    } finally {
      setRecovering(false);
    }
  }, [poll]);

  useEffect(() => {
    poll();
    const interval = setInterval(poll, 800);
    return () => clearInterval(interval);
  }, [poll]);

  if (statusChecked && status?.requires_source && !setupInitiated) {
    return (
      <InferenceSourceSetup
        onStarted={() => {
          setSetupInitiated(true);
          void poll();
        }}
      />
    );
  }

  const activeStep: StepKey | null =
    status && !status.server_ready ? 'server_ready' : null;

  return (
    <div
      className="fixed inset-0 flex items-center justify-center"
      style={{ background: 'var(--color-bg)' }}
    >
      <div className="w-full max-w-md px-6">
        <div className="text-center mb-10">
          <div
            className="w-16 h-16 rounded-2xl flex items-center justify-center mx-auto mb-4"
            style={{
              background: 'var(--color-accent-subtle)',
              color: 'var(--color-accent)',
            }}
          >
            <Server size={32} />
          </div>
          <h1 className="text-xl font-semibold mb-2" style={{ color: 'var(--color-text)' }}>
            OpenJarvis
          </h1>
          <p className="text-sm" style={{ color: 'var(--color-text-secondary)' }}>
<<<<<<< ours
            Connecting to backend...
||||||| base
            Setting up your local AI...
=======
            {!statusChecked
              ? 'Checking your saved setup...'
              : status?.source === 'custom'
                ? 'Connecting to your AI server...'
                : 'Setting up your local AI...'}
>>>>>>> theirs
          </p>
        </div>

<<<<<<< ours
        {STEPS.map((step) => (
          <StepRow
            key={step.key}
            icon={step.icon}
            label={step.label}
            done={status?.[step.key] ?? false}
            active={activeStep === step.key}
            detail={
              activeStep === step.key && status?.detail ? status.detail : step.detail
            }
          />
        ))}
||||||| base
        {/* Steps */}
        <div className="flex flex-col gap-2 mb-8">
          {STEPS.map((step) => (
            <StepRow
              key={step.key}
              icon={step.icon}
              label={step.label}
              done={status?.[step.key] ?? false}
              active={activeStep === step.key}
              detail={
                activeStep === step.key && status?.detail
                  ? status.detail
                  : step.detail
              }
            />
          ))}
        </div>
=======
        {/* Steps */}
        <div className="flex flex-col gap-2 mb-8">
          {(status?.source === 'custom'
            ? [
                { key: 'ollama_ready' as const, label: 'Inference Engine', icon: Cpu, detail: 'Connecting to your server...' },
                { key: 'model_ready' as const, label: 'Endpoint', icon: Database, detail: 'Checking endpoint...' },
                { key: 'server_ready' as const, label: 'API Server', icon: Server, detail: 'Starting server...' },
              ]
            : STEPS
          ).map((step) => (
            <StepRow
              key={step.key}
              icon={step.icon}
              label={step.label}
              done={status?.[step.key] ?? false}
              active={activeStep === step.key}
              detail={
                activeStep === step.key && status?.detail
                  ? status.detail
                  : step.detail
              }
            />
          ))}
        </div>
>>>>>>> theirs

        {status?.error && (
          <div
            className="flex items-start gap-3 px-4 py-3 rounded-xl text-sm mt-4"
            style={{
              background: 'color-mix(in srgb, var(--color-error) 10%, transparent)',
              border: '1px solid color-mix(in srgb, var(--color-error) 20%, transparent)',
              color: 'var(--color-error)',
            }}
          >
            <XCircle size={16} className="flex-shrink-0 mt-0.5" />
            <span style={{ wordBreak: 'break-word', overflowWrap: 'anywhere' }}>
              {status.error}
            </span>
          </div>
        )}

<<<<<<< ours
||||||| base
        {/* Progress bar */}
=======
        {recoveryError && (
          <div
            role="alert"
            className="mt-3 px-4 py-3 rounded-xl text-sm"
            style={{ color: 'var(--color-error)' }}
          >
            {recoveryError}
          </div>
        )}

        {statusChecked && status && !status.requires_source && status.phase !== 'ready' && (
          <InferenceRecoveryButton
            recovering={recovering}
            onChange={() => void changeInferenceSource()}
          />
        )}

        {/* Progress bar */}
>>>>>>> theirs
        {!status?.error && (
          <div
            className="h-1 rounded-full overflow-hidden mt-6"
            style={{ background: 'var(--color-bg-tertiary)' }}
          >
            <div
              className="h-full rounded-full transition-all duration-500"
              style={{
                background: 'var(--color-accent)',
                width: `${(status?.server_ready ? 1 : 0) * 100}%`,
              }}
            />
          </div>
        )}
      </div>
    </div>
  );
}


## ===== frontend/src/lib/api.ts : OUR COMMITS SINCE AUTHOR BASE =====
f2e69f20 W67: synthesize timeout, api.ts mojibake, handoff
73db0c1a W51: confirm prompt UI - render tool_confirm_request, POST approve/deny, dismiss on resolved. Verified live 09/12.
efc28e40 feat(tts): shrink first TTS chunk to 90 chars, keep driver instrumentation
0389255b TTS: AudioContext playback engine + ChatArea driver rewrite; mailbox IMAP connector and tools; speech/CSP fixes
b76b1b13 fix(ui): coerce object tool/arguments fields to string + remove PWA service worker (resolves React #31 stale-bundle boot crash)
e0e36523 Fix: wire tools to native_openhands agent - file_read, think, calculator, code_interpreter, shell_exec, file_write now loading at startup
daafc769 fix: speech subsystem TTS streaming, backend file logging, uvicorn console fix, restore .gitignore
a533573a fix: bypass broken Tauri invoke for STT, use direct HTTP to /v1/speech/transcribe
6015a448 feat: mic button fix, agent work, cloud router updates, HUD improvements
3782799b feat: speech subsystem, auto-focus, pyproject fixes, pynvml->nvidia-ml-py, startup scripts
bc498a16 feat: Arc Reactor ThinkingCircle, fix env loading, fix project root, add research types, remove debug code
f2fcb30c Graystone Lab: remote MCP/Ollama integration, Rust extension, UI fixes

## ===== frontend/src/lib/api.ts : CONFLICTED WORKING FILE (diff3) =====
<<<<<<< ours
ï»¿import type { ModelInfo, SavingsData, ServerInfo } from '../types';
||||||| base
import type { ModelInfo, SavingsData, ServerInfo } from '../types';
=======
import type { ModelInfo, SavingsData, ServerInfo } from '../types';
import { SUPABASE_ANON_KEY, SUPABASE_URL } from './supabase';
import { serializeToolCallArguments } from './tool-call';
>>>>>>> theirs

// ---------------------------------------------------------------------------
<<<<<<< ours
// Supabase config - safe to embed (RLS protects writes)
||||||| base
// Supabase config â€” safe to embed (RLS protects writes)
=======
// Supabase config
>>>>>>> theirs
// ---------------------------------------------------------------------------

declare global {
  interface Window {
    __TAURI_INTERNALS__?: unknown;
  }
}

export const isTauri = () => typeof window !== 'undefined' && !!window.__TAURI_INTERNALS__;

export type CloudKeyStatus = Record<string, boolean>;

export async function getCloudKeyStatus(): Promise<CloudKeyStatus> {
  if (!isTauri()) return {};
  try {
    const { invoke } = await import('@tauri-apps/api/core');
    const rows = await invoke<Array<{ key: string; set: boolean }>>('get_cloud_key_status');
    return Object.fromEntries(rows.map((row) => [row.key, row.set]));
  } catch (e: any) {
    throw new Error(e?.message ?? e ?? 'Failed to read cloud key status');
  }
}

export async function saveCloudKey(keyName: string, keyValue: string): Promise<void> {
  if (!isTauri()) {
    throw new Error('Cloud API keys can be saved in the desktop app only.');
  }
  try {
    const { invoke } = await import('@tauri-apps/api/core');
    await invoke('save_cloud_key', { keyName, keyValue });
  } catch (e: any) {
    throw new Error(e?.message ?? e ?? 'Failed to save cloud key');
  }
}

// Cached API base URL fetched from the Tauri backend at startup.
// This avoids hardcoding the port - the Rust backend is the single
// source of truth for JARVIS_PORT.
let _tauriApiBase: string | null = null;

/** Pre-fetch the API base URL from the Tauri backend (call once at init). */
export async function initApiBase(): Promise<void> {
  if (!isTauri()) return;
  try {
    const { invoke } = await import('@tauri-apps/api/core');
    _tauriApiBase = await invoke<string>('get_api_base');
  } catch {
    // Command may not exist on older builds; fall through to default.
  }
}

const DESKTOP_API_FALLBACK = 'http://127.0.0.1:8010';

const getSettingsApiUrl = (): string => {
  try {
    const raw = localStorage.getItem('openjarvis-settings');
    if (raw) {
      const parsed = JSON.parse(raw);
      if (parsed.apiUrl) return parsed.apiUrl.replace(/\/+$/, '');
    }
  } catch {}
  return '';
};

export const getBase = (): string => {
  const settingsUrl = getSettingsApiUrl();
  if (settingsUrl) return settingsUrl;
  if (import.meta.env.VITE_API_URL) return import.meta.env.VITE_API_URL;
  if (isTauri()) return _tauriApiBase || DESKTOP_API_FALLBACK;
  return '';
};
// Authorization helper
function getAuthHeaders(): Record<string, string> {
  try {
    const raw = localStorage.getItem('openjarvis-settings');
    if (raw) {
      const parsed = JSON.parse(raw);
      if (parsed.apiKey) {
        return { Authorization: `Bearer ${parsed.apiKey}` };
      }
    }
  } catch {}
  return {};
}

async function apiFetch(input: string, init: RequestInit = {}): Promise<Response> {
  const headers = new Headers(init.headers || {});
  for (const [key, value] of Object.entries(getAuthHeaders())) {
    headers.set(key, value);
  }
  return fetch(input, { ...init, headers });
}

// Resolve the local server API key (OPENJARVIS_API_KEY). When `jarvis serve`
// is started with a key, AuthMiddleware 401s every /v1 and /api request that
// lacks a Bearer token â€” so the frontend must send it (#266). Sourced from the
// same settings blob as the API URL, with an optional build-time env override.
// Returns '' when unset, so a keyless local server keeps working unchanged.
export const getApiKey = (): string => {
  try {
    const raw = localStorage.getItem('openjarvis-settings');
    if (raw) {
      const parsed = JSON.parse(raw);
      if (parsed.apiKey) return String(parsed.apiKey);
    }
  } catch {}
  if (import.meta.env.VITE_OPENJARVIS_API_KEY) {
    return import.meta.env.VITE_OPENJARVIS_API_KEY as string;
  }
  return '';
};

// Build request headers with the Bearer Authorization token when a local key
// is configured, merging any caller-supplied headers. Adds no Authorization
// header when no key is set, so keyless local dev is byte-for-byte unchanged.
export const authHeaders = (
  extra: Record<string, string> = {},
): Record<string, string> => {
  const key = getApiKey();
  return key ? { ...extra, Authorization: `Bearer ${key}` } : { ...extra };
};

// Centralized fetch for the local server: prepends getBase() and injects the
// Bearer auth header (when a key is set) on every call. Using this everywhere
// guarantees no /v1 or /api request is sent without auth â€” the bug in #266 was
// that direct fetch() calls omitted the header and 401'd. `path` is the
// server-relative path (e.g. "/v1/savings").
export const apiFetch = (
  path: string,
  init: RequestInit = {},
): Promise<Response> => {
  const headers = authHeaders(
    (init.headers as Record<string, string> | undefined) ?? {},
  );
  return fetch(`${getBase()}${path}`, { ...init, headers });
};

async function tauriInvoke<T>(command: string, args: Record<string, unknown> = {}): Promise<T> {
  const { invoke } = await import('@tauri-apps/api/core');
  const apiUrl = getBase();
  return invoke<T>(command, { apiUrl, ...args });
}

// ---------------------------------------------------------------------------
// Setup status (desktop only)
// ---------------------------------------------------------------------------

export interface SetupStatus {
  phase: string;
  detail: string;
  ollama_ready?: boolean;
  server_ready: boolean;
  model_ready: boolean;
  error: string | null;
  source: 'unconfigured' | 'ollama' | 'custom';
  requires_source: boolean;
}

export async function getSetupStatus(): Promise<SetupStatus | null> {
  if (!isTauri()) return null;
  try {
    const { invoke } = await import('@tauri-apps/api/core');
    return await invoke<SetupStatus>('get_setup_status');
  } catch {
    return null;
  }
}

/** Start desktop services after an inference source has been persisted. */
export async function startBackend(): Promise<void> {
  if (!isTauri()) throw new Error('The desktop backend is available in the desktop app only.');
  try {
    const { invoke } = await import('@tauri-apps/api/core');
    await invoke<void>('start_backend');
  } catch (e: any) {
    throw new Error(e?.message ?? e ?? 'Failed to start the desktop backend');
  }
}

/** Stop an in-flight setup and return the desktop to its inert source chooser. */
export async function resetInferenceSource(): Promise<void> {
  if (!isTauri()) throw new Error('Inference setup recovery is available in the desktop app only.');
  try {
    const { invoke } = await import('@tauri-apps/api/core');
    await invoke<void>('reset_inference_source');
  } catch (e: any) {
    throw new Error(e?.message ?? e ?? 'Failed to reset inference setup');
  }
}

// ---------------------------------------------------------------------------
// API functions
// ---------------------------------------------------------------------------

export async function fetchModels(): Promise<ModelInfo[]> {
  if (isTauri()) {
    try {
      const result = await tauriInvoke<{ data?: ModelInfo[] }>('fetch_models');
      return result?.data || [];
    } catch {
      // Fall through to fetch
    }
  }
<<<<<<< ours
  const res = await apiFetch(`${getBase()}/v1/models`);
||||||| base
  const res = await fetch(`${getBase()}/v1/models`);
=======
  const res = await apiFetch(`/v1/models`);
>>>>>>> theirs
  if (!res.ok) throw new Error(`Failed to fetch models: ${res.status}`);
  const data = await res.json();
  return data.data || [];
}

export async function fetchRecommendedModel(): Promise<{ model: string; reason: string }> {
<<<<<<< ours
  const res = await apiFetch(`${getBase()}/v1/recommended-model`);
||||||| base
  const res = await fetch(`${getBase()}/v1/recommended-model`);
=======
  const res = await apiFetch(`/v1/recommended-model`);
>>>>>>> theirs
  if (!res.ok) return { model: '', reason: 'Failed to fetch' };
  return res.json();
}

export async function pullModel(modelName: string): Promise<void> {
<<<<<<< ours
  const res = await apiFetch(`${getBase()}/v1/models/pull`, {
||||||| base
  // In Tauri, go through the Rust backend directly (avoids CORS / timeout
  // issues with long model downloads via fetch).
  if (isTauri()) {
    try {
      const { invoke } = await import('@tauri-apps/api/core');
      await invoke('pull_ollama_model', { modelName });
      return;
    } catch (e: any) {
      throw new Error(e?.message || e || 'Download failed');
    }
  }
  const res = await fetch(`${getBase()}/v1/models/pull`, {
=======
  // In Tauri, go through the Rust backend directly (avoids CORS / timeout
  // issues with long model downloads via fetch).
  if (isTauri()) {
    try {
      const { invoke } = await import('@tauri-apps/api/core');
      await invoke('pull_ollama_model', { modelName });
      return;
    } catch (e: any) {
      throw new Error(e?.message || e || 'Download failed');
    }
  }
  const res = await apiFetch(`/v1/models/pull`, {
>>>>>>> theirs
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ model: modelName }),
  });
  if (!res.ok) {
    const detail = await res.text().catch(() => res.statusText);
    throw new Error(`Failed to pull model: ${detail}`);
  }
}

export async function deleteModel(modelName: string): Promise<void> {
<<<<<<< ours
  const res = await apiFetch(`${getBase()}/v1/models/${encodeURIComponent(modelName)}`, {
||||||| base
  if (isTauri()) {
    try {
      const { invoke } = await import('@tauri-apps/api/core');
      await invoke('delete_ollama_model', { modelName });
      return;
    } catch (e: any) {
      throw new Error(e?.message || e || 'Delete failed');
    }
  }
  const res = await fetch(`${getBase()}/v1/models/${encodeURIComponent(modelName)}`, {
=======
  if (isTauri()) {
    try {
      const { invoke } = await import('@tauri-apps/api/core');
      await invoke('delete_ollama_model', { modelName });
      return;
    } catch (e: any) {
      throw new Error(e?.message || e || 'Delete failed');
    }
  }
  const res = await apiFetch(`/v1/models/${encodeURIComponent(modelName)}`, {
>>>>>>> theirs
    method: 'DELETE',
  });
  if (!res.ok) {
    const detail = await res.text().catch(() => res.statusText);
    throw new Error(`Failed to delete model: ${detail}`);
  }
}

<<<<<<< ours
export async function preloadModel(_modelName: string): Promise<void> {
  return;
||||||| base
const _CLOUD_PREFIXES = ['gpt-', 'o1-', 'o3-', 'o4-', 'claude-', 'gemini-', 'openrouter/'];

export async function preloadModel(modelName: string): Promise<void> {
  // Cloud models don't need Ollama preloading
  if (_CLOUD_PREFIXES.some(p => modelName.startsWith(p))) {
    return;
  }
  // Trigger Ollama to load the model into memory (empty prompt, no generation).
  const ollamaUrl = 'http://127.0.0.1:11434';
  try {
    const res = await fetch(`${ollamaUrl}/api/generate`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ model: modelName, prompt: '', keep_alive: '5m' }),
      signal: AbortSignal.timeout(120_000),
    });
    if (!res.ok) throw new Error(`Preload failed: ${res.status}`);
  } catch (e: any) {
    if (e.name === 'TimeoutError') throw new Error('Model load timed out (120s)');
    throw e;
  }
=======
const _CLOUD_PREFIXES = ['gpt-', 'o1-', 'o3-', 'o4-', 'claude-', 'gemini-', 'openrouter/'];

export async function preloadModel(modelName: string, owner?: string): Promise<void> {
  // Cloud models don't need Ollama preloading
  if (owner === 'litellm' || _CLOUD_PREFIXES.some(p => modelName.startsWith(p))) {
    return;
  }
  // Trigger Ollama to load the model into memory (empty prompt, no generation).
  const ollamaUrl = 'http://127.0.0.1:11434';
  try {
    const res = await fetch(`${ollamaUrl}/api/generate`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ model: modelName, prompt: '', keep_alive: '5m' }),
      signal: AbortSignal.timeout(120_000),
    });
    if (!res.ok) throw new Error(`Preload failed: ${res.status}`);
  } catch (e: any) {
    if (e.name === 'TimeoutError') throw new Error('Model load timed out (120s)');
    throw e;
  }
>>>>>>> theirs
}

export async function fetchSavings(): Promise<SavingsData> {
<<<<<<< ours
  const res = await apiFetch(`${getBase()}/v1/savings`);
||||||| base
  const res = await fetch(`${getBase()}/v1/savings`);
=======
  const res = await apiFetch(`/v1/savings`);
>>>>>>> theirs
  if (!res.ok) throw new Error(`Failed to fetch savings: ${res.status}`);
  return res.json();
}

export async function fetchServerInfo(): Promise<ServerInfo> {
<<<<<<< ours
  const res = await apiFetch(`${getBase()}/v1/info`);
||||||| base
  const res = await fetch(`${getBase()}/v1/info`);
=======
  const res = await apiFetch(`/v1/info`);
>>>>>>> theirs
  if (!res.ok) throw new Error(`Failed to fetch server info: ${res.status}`);
  return res.json();
}

export async function checkHealth(): Promise<boolean> {
  if (isTauri()) {
    try {
      await tauriInvoke('check_health', { apiUrl: getBase() });
      return true;
    } catch {
      return false;
    }
  }
  try {
    const res = await apiFetch(`${getBase()}/health`);
    return res.ok;
  } catch {
    return false;
  }
}

export async function fetchEnergy(): Promise<unknown> {
  if (isTauri()) {
    try {
      return await tauriInvoke('fetch_energy', { apiUrl: getBase() });
    } catch {}
  }
<<<<<<< ours
  const res = await apiFetch(`${getBase()}/v1/telemetry/energy`);
||||||| base
  const res = await fetch(`${getBase()}/v1/telemetry/energy`);
=======
  const res = await apiFetch(`/v1/telemetry/energy`);
>>>>>>> theirs
  if (!res.ok) throw new Error(`Failed: ${res.status}`);
  return res.json();
}

export async function fetchTelemetry(): Promise<unknown> {
  if (isTauri()) {
    try {
      return await tauriInvoke('fetch_telemetry', { apiUrl: getBase() });
    } catch {}
  }
<<<<<<< ours
  const res = await apiFetch(`${getBase()}/v1/telemetry/stats`);
||||||| base
  const res = await fetch(`${getBase()}/v1/telemetry/stats`);
=======
  const res = await apiFetch(`/v1/telemetry/stats`);
>>>>>>> theirs
  if (!res.ok) throw new Error(`Failed: ${res.status}`);
  return res.json();
}

export async function fetchTraces(limit: number = 50): Promise<unknown> {
  if (isTauri()) {
    try {
      return await tauriInvoke('fetch_traces', { apiUrl: getBase(), limit });
    } catch {}
  }
<<<<<<< ours
  const res = await apiFetch(`${getBase()}/v1/traces?limit=${limit}`);
||||||| base
  const res = await fetch(`${getBase()}/v1/traces?limit=${limit}`);
=======
  const res = await apiFetch(`/v1/traces?limit=${limit}`);
>>>>>>> theirs
  if (!res.ok) throw new Error(`Failed: ${res.status}`);
  return res.json();
}

// ---------------------------------------------------------------------------
// Speech
// ---------------------------------------------------------------------------

export interface TranscriptionResult {
  text: string;
  language: string | null;
  confidence: number | null;
  duration_seconds: number;
}

export interface SpeechHealth {
  available: boolean;
  backend?: string;
  reason?: string;
}

export async function transcribeAudio(audioBlob: Blob, filename = 'recording.webm'): Promise<TranscriptionResult> {
<<<<<<< ours
  // Direct HTTP only - Tauri invoke path does not exist in Rust layer
||||||| base
  if (isTauri()) {
    try {
      const buffer = await audioBlob.arrayBuffer();
      return await tauriInvoke<TranscriptionResult>('transcribe_audio', {
        audioData: Array.from(new Uint8Array(buffer)),
        filename,
      });
    } catch {
      // Fall through to fetch
    }
  }
=======
  if (isTauri()) {
    try {
      const buffer = await audioBlob.arrayBuffer();
      return await tauriInvoke<TranscriptionResult>('transcribe_audio', {
        audioData: Array.from(new Uint8Array(buffer)),
        filename,
      });
    } catch (err) {
      const msg = err instanceof Error ? err.message : String(err);
      throw new Error(msg || 'Transcription failed');
    }
  }
>>>>>>> theirs
  const formData = new FormData();
  formData.append('file', audioBlob, filename);
<<<<<<< ours
  const res = await apiFetch(getBase() + '/v1/speech/transcribe', {
||||||| base
  const res = await fetch(`${getBase()}/v1/speech/transcribe`, {
=======
  const res = await apiFetch(`/v1/speech/transcribe`, {
>>>>>>> theirs
    method: 'POST',
    body: formData,
  });
<<<<<<< ours
  if (!res.ok) throw new Error('Transcription failed: ' + res.status);
||||||| base
  if (!res.ok) throw new Error(`Transcription failed: ${res.status}`);
=======
  if (!res.ok) {
    let detail = "";
    try {
      const body = await res.json();
      detail = typeof body.detail === 'string' ? body.detail : "";
    } catch {
      // Keep the status-only message below when the body is not JSON.
    }
    throw new Error(detail || `Transcription failed: ${res.status}`);
  }
>>>>>>> theirs
  return res.json();
}

export async function fetchSpeechHealth(): Promise<SpeechHealth> {
  try {
    const res = await apiFetch(`${getBase()}/v1/speech/health`);
    if (!res.ok) return { available: false };
    return res.json();
  } catch {
    return { available: false };
  }
}
export async function synthesizeSpeech(text: string, voiceId = 'am_adam', speed = 0.85): Promise<Blob> {
  const res = await apiFetch(`${getBase()}/v1/speech/synthesize`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ text, voice_id: voiceId, speed, output_format: 'wav' }),
    // F-W62-2d: a hung synthesize parks the ttsPlayer pump forever -
    // pumping stays true, every later enqueue is dropped, and voice dies
    // for the session with no error. Throws into the pump catch instead.
    signal: AbortSignal.timeout(30000),
  });
  if (!res.ok) throw new Error(`Synthesis failed: ${res.status}`);
  return res.blob();
}
const TTS_MAX_CHUNK_CHARS = 350;
// First TTS unit is one sentence: time-to-first-audio is ~0.65s fixed + 2.45us/byte,
// so a 350-char opening pack costs ~3.1s vs ~1.1s for a single sentence (measured 2026-08-07).
const TTS_FIRST_CHUNK_CHARS = 90;

export function splitIntoTTSChunks(text: string): string[] {
  const sentences = text.split(/(?<=[.!?])\s+/);
  const chunks: string[] = [];
  let current = '';

  for (const sentence of sentences) {
    if (sentence.length > TTS_MAX_CHUNK_CHARS) {
      if (current) {
        chunks.push(current.trim());
        current = '';
      }
      const parts = sentence.split(/(?<=,)\s+/);
      let piece = '';
      for (const part of parts) {
        if ((piece + ' ' + part).trim().length > TTS_MAX_CHUNK_CHARS) {
          if (piece) chunks.push(piece.trim());
          piece = part;
        } else {
          piece = piece ? `${piece} ${part}` : part;
        }
      }
      if (piece) chunks.push(piece.trim());
      continue;
    }

    const limit = chunks.length === 0 ? TTS_FIRST_CHUNK_CHARS : TTS_MAX_CHUNK_CHARS;
    if ((current + ' ' + sentence).trim().length > limit) {
      if (current) chunks.push(current.trim());
      current = sentence;
    } else {
      current = current ? `${current} ${sentence}` : sentence;
    }
  }
<<<<<<< ours

  if (current) chunks.push(current.trim());
  return chunks.filter((c) => c.length > 0);
||||||| base
  const res = await fetch(`${getBase()}/v1/speech/health`);
  if (!res.ok) return { available: false };
  return res.json();
=======
  const res = await apiFetch(`/v1/speech/health`);
  if (!res.ok) return { available: false };
  return res.json();
>>>>>>> theirs
}

export async function synthesizeSpeechChunks(
  text: string,
  onChunk: (blob: Blob, index: number, total: number) => void,
  voiceId = 'am_adam',
  speed = 0.85
): Promise<void> {
  const chunks = splitIntoTTSChunks(text);
  const total = chunks.length;

  for (let i = 0; i < total; i++) {
    const blob = await synthesizeSpeech(chunks[i], voiceId, speed);
    onChunk(blob, i, total);
  }
}
// ---------------------------------------------------------------------------
// Agent Manager
// ---------------------------------------------------------------------------

export interface ManagedAgentConfig extends Record<string, unknown> {
  schedule_type?: string;
  schedule_value?: string | number;
}

export interface ManagedAgent {
  id: string;
  name: string;
  agent_type: string;
  config: ManagedAgentConfig;
  status: 'idle' | 'running' | 'paused' | 'error' | 'archived' | 'needs_attention' | 'budget_exceeded' | 'stalled';
  summary_memory: string;
  created_at: number;
  updated_at: number;
  // Runtime stats
  total_runs?: number;
  total_cost?: number;
  total_tokens?: number;
  input_tokens?: number;
  output_tokens?: number;
  last_run_at?: number | null;
  // Budget
  budget?: number;
  // Learning
  learning_enabled?: boolean;
  // Live progress
  current_activity?: string;
}

export interface AgentTask {
  id: string;
  agent_id: string;
  description: string;
  status: 'pending' | 'active' | 'completed' | 'failed';
  progress: Record<string, unknown>;
  findings: unknown[];
  created_at: number;
}

export interface ChannelBinding {
  id: string;
  agent_id: string;
  channel_type: string;
  config: Record<string, unknown>;
  session_id: string;
  routing_mode: string;
}

export interface AgentTemplate {
  id: string;
  name: string;
  description: string;
  source: 'built-in' | 'user';
  agent_type: string;
  [key: string]: unknown;
}

export interface PersistedToolCall {
  tool: string;
  arguments: string;
  result?: string;
  success?: boolean;
  latency?: number;
}

export interface AgentMessage {
  id: string;
  agent_id: string;
  direction: 'user_to_agent' | 'agent_to_user';
  content: string;
  mode: 'immediate' | 'queued';
  status: 'pending' | 'delivered' | 'responded';
  created_at: number;
  tool_calls?: PersistedToolCall[] | null;
}



export async function uploadChatFiles(files: File[]): Promise<void> {
  const formData = new FormData();
  for (const file of files) {
    formData.append('files', file);
  }
  const res = await apiFetch(getBase() + '/v1/connectors/upload/ingest/files', {
    method: 'POST',
    body: formData,
  });
  if (!res.ok) {
    const err = await res.text().catch(() => res.statusText);
    throw new Error('Upload failed: ' + err);
  }
}
export async function fetchManagedAgents(): Promise<ManagedAgent[]> {
<<<<<<< ours
  const res = await apiFetch(`${getBase()}/v1/managed-agents`);
||||||| base
  const res = await fetch(`${getBase()}/v1/managed-agents`);
=======
  const res = await apiFetch(`/v1/managed-agents`);
>>>>>>> theirs
  if (!res.ok) throw new Error(`Failed: ${res.status}`);
  const data = await res.json();
  return data.agents || [];
}

export async function fetchManagedAgent(agentId: string): Promise<ManagedAgent> {
<<<<<<< ours
  const res = await apiFetch(`${getBase()}/v1/managed-agents/${agentId}`);
||||||| base
  const res = await fetch(`${getBase()}/v1/managed-agents/${agentId}`);
=======
  const res = await apiFetch(`/v1/managed-agents/${agentId}`);
>>>>>>> theirs
  if (!res.ok) throw new Error(`Failed: ${res.status}`);
  return res.json();
}

export async function createManagedAgent(body: {
  name: string;
  agent_type?: string;
  template_id?: string;
  config?: Record<string, unknown>;
}): Promise<ManagedAgent> {
<<<<<<< ours
  const res = await apiFetch(`${getBase()}/v1/managed-agents`, {
||||||| base
  const res = await fetch(`${getBase()}/v1/managed-agents`, {
=======
  const res = await apiFetch(`/v1/managed-agents`, {
>>>>>>> theirs
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  });
  if (!res.ok) throw new Error(`Failed: ${res.status}`);
  return res.json();
}

export async function updateManagedAgent(
  agentId: string,
  body: Partial<{ name: string; agent_type: string; config: Record<string, unknown> }>,
): Promise<ManagedAgent> {
<<<<<<< ours
  const res = await apiFetch(`${getBase()}/v1/managed-agents/${agentId}`, {
||||||| base
  const res = await fetch(`${getBase()}/v1/managed-agents/${agentId}`, {
=======
  const res = await apiFetch(`/v1/managed-agents/${agentId}`, {
>>>>>>> theirs
    method: 'PATCH',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  });
  if (!res.ok) throw new Error(`Failed: ${res.status}`);
  return res.json();
}

export async function deleteManagedAgent(agentId: string): Promise<void> {
<<<<<<< ours
  const res = await apiFetch(`${getBase()}/v1/managed-agents/${agentId}`, { method: 'DELETE' });
||||||| base
  const res = await fetch(`${getBase()}/v1/managed-agents/${agentId}`, { method: 'DELETE' });
=======
  const res = await apiFetch(`/v1/managed-agents/${agentId}`, { method: 'DELETE' });
>>>>>>> theirs
  if (!res.ok) throw new Error(`Failed: ${res.status}`);
}

export async function pauseManagedAgent(agentId: string): Promise<void> {
<<<<<<< ours
  const res = await apiFetch(`${getBase()}/v1/managed-agents/${agentId}/pause`, { method: 'POST' });
||||||| base
  const res = await fetch(`${getBase()}/v1/managed-agents/${agentId}/pause`, { method: 'POST' });
=======
  const res = await apiFetch(`/v1/managed-agents/${agentId}/pause`, { method: 'POST' });
>>>>>>> theirs
  if (!res.ok) throw new Error(`Failed: ${res.status}`);
}

export async function resumeManagedAgent(agentId: string): Promise<void> {
<<<<<<< ours
  const res = await apiFetch(`${getBase()}/v1/managed-agents/${agentId}/resume`, { method: 'POST' });
||||||| base
  const res = await fetch(`${getBase()}/v1/managed-agents/${agentId}/resume`, { method: 'POST' });
=======
  const res = await apiFetch(`/v1/managed-agents/${agentId}/resume`, { method: 'POST' });
>>>>>>> theirs
  if (!res.ok) throw new Error(`Failed: ${res.status}`);
}

export async function fetchAgentTasks(agentId: string): Promise<AgentTask[]> {
<<<<<<< ours
  const res = await apiFetch(`${getBase()}/v1/managed-agents/${agentId}/tasks`);
||||||| base
  const res = await fetch(`${getBase()}/v1/managed-agents/${agentId}/tasks`);
=======
  const res = await apiFetch(`/v1/managed-agents/${agentId}/tasks`);
>>>>>>> theirs
  if (!res.ok) throw new Error(`Failed: ${res.status}`);
  const data = await res.json();
  return data.tasks || [];
}

export async function createAgentTask(agentId: string, description: string): Promise<AgentTask> {
<<<<<<< ours
  const res = await apiFetch(`${getBase()}/v1/managed-agents/${agentId}/tasks`, {
||||||| base
  const res = await fetch(`${getBase()}/v1/managed-agents/${agentId}/tasks`, {
=======
  const res = await apiFetch(`/v1/managed-agents/${agentId}/tasks`, {
>>>>>>> theirs
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ description }),
  });
  if (!res.ok) throw new Error(`Failed: ${res.status}`);
  return res.json();
}

export async function fetchAgentChannels(agentId: string): Promise<ChannelBinding[]> {
<<<<<<< ours
  const res = await apiFetch(`${getBase()}/v1/managed-agents/${agentId}/channels`);
||||||| base
  const res = await fetch(`${getBase()}/v1/managed-agents/${agentId}/channels`);
=======
  const res = await apiFetch(`/v1/managed-agents/${agentId}/channels`);
>>>>>>> theirs
  if (!res.ok) throw new Error(`Failed: ${res.status}`);
  const data = await res.json();
  return data.bindings || [];
}

export async function bindAgentChannel(
  agentId: string,
  channelType: string,
  config?: Record<string, unknown>,
): Promise<ChannelBinding> {
  const res = await fetch(
    `${getBase()}/v1/managed-agents/${agentId}/channels`,
    {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        channel_type: channelType,
        config: config || {},
        routing_mode: 'dedicated',
      }),
    },
  );
  if (!res.ok) throw new Error(`Failed: ${res.status}`);
  return res.json();
}

export async function unbindAgentChannel(
  agentId: string,
  bindingId: string,
): Promise<void> {
  const res = await fetch(
    `${getBase()}/v1/managed-agents/${agentId}/channels/${bindingId}`,
    { method: 'DELETE' },
  );
  if (!res.ok) throw new Error(`Failed: ${res.status}`);
}

// -- SendBlue auto-setup helpers ------------------------------------------

export async function sendblueVerify(
  apiKeyId: string,
  apiSecretKey: string,
): Promise<{ valid: boolean; numbers: string[]; raw: unknown }> {
<<<<<<< ours
  const res = await apiFetch(`${getBase()}/v1/channels/sendblue/verify`, {
||||||| base
  const res = await fetch(`${getBase()}/v1/channels/sendblue/verify`, {
=======
  const res = await apiFetch(`/v1/channels/sendblue/verify`, {
>>>>>>> theirs
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ api_key_id: apiKeyId, api_secret_key: apiSecretKey }),
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: res.statusText }));
    throw new Error(err.detail || `Verification failed: ${res.status}`);
  }
  return res.json();
}

export async function sendblueRegisterWebhook(
  apiKeyId: string,
  apiSecretKey: string,
  webhookUrl: string,
): Promise<{ registered: boolean; status: number }> {
<<<<<<< ours
  const res = await apiFetch(`${getBase()}/v1/channels/sendblue/register-webhook`, {
||||||| base
  const res = await fetch(`${getBase()}/v1/channels/sendblue/register-webhook`, {
=======
  const res = await apiFetch(`/v1/channels/sendblue/register-webhook`, {
>>>>>>> theirs
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      api_key_id: apiKeyId,
      api_secret_key: apiSecretKey,
      webhook_url: webhookUrl,
    }),
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: res.statusText }));
    throw new Error(err.detail || `Webhook registration failed: ${res.status}`);
  }
  return res.json();
}

export async function sendblueTest(
  apiKeyId: string,
  apiSecretKey: string,
  fromNumber: string,
  toNumber: string,
): Promise<{ sent: boolean; status: number }> {
<<<<<<< ours
  const res = await apiFetch(`${getBase()}/v1/channels/sendblue/test`, {
||||||| base
  const res = await fetch(`${getBase()}/v1/channels/sendblue/test`, {
=======
  const res = await apiFetch(`/v1/channels/sendblue/test`, {
>>>>>>> theirs
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      api_key_id: apiKeyId,
      api_secret_key: apiSecretKey,
      from_number: fromNumber,
      to_number: toNumber,
    }),
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: res.statusText }));
    throw new Error(err.detail || `Test message failed: ${res.status}`);
  }
  return res.json();
}

export async function sendblueHealth(): Promise<{ channel_connected: boolean; bridge_wired: boolean; ready: boolean }> {
<<<<<<< ours
  const res = await apiFetch(`${getBase()}/v1/channels/sendblue/health`);
||||||| base
  const res = await fetch(`${getBase()}/v1/channels/sendblue/health`);
=======
  const res = await apiFetch(`/v1/channels/sendblue/health`);
>>>>>>> theirs
  if (!res.ok) return { channel_connected: false, bridge_wired: false, ready: false };
  return res.json();
}

export async function fetchTemplates(): Promise<AgentTemplate[]> {
<<<<<<< ours
  const res = await apiFetch(`${getBase()}/v1/templates`);
||||||| base
  const res = await fetch(`${getBase()}/v1/templates`);
=======
  const res = await apiFetch(`/v1/templates`);
>>>>>>> theirs
  if (!res.ok) throw new Error(`Failed: ${res.status}`);
  const data = await res.json();
  return data.templates || [];
}

export async function runManagedAgent(agentId: string): Promise<void> {
<<<<<<< ours
  const res = await apiFetch(`${getBase()}/v1/managed-agents/${agentId}/run`, { method: 'POST' });
||||||| base
  const res = await fetch(`${getBase()}/v1/managed-agents/${agentId}/run`, { method: 'POST' });
=======
  const res = await apiFetch(`/v1/managed-agents/${agentId}/run`, { method: 'POST' });
>>>>>>> theirs
  if (!res.ok) {
    const body = await res.json().catch(() => ({ detail: res.statusText }));
    throw new Error(body.detail || `Failed: ${res.status}`);
  }
}

export async function recoverManagedAgent(agentId: string): Promise<{ recovered: boolean; checkpoint: unknown }> {
<<<<<<< ours
  const res = await apiFetch(`${getBase()}/v1/managed-agents/${agentId}/recover`, { method: 'POST' });
||||||| base
  const res = await fetch(`${getBase()}/v1/managed-agents/${agentId}/recover`, { method: 'POST' });
=======
  const res = await apiFetch(`/v1/managed-agents/${agentId}/recover`, { method: 'POST' });
>>>>>>> theirs
  if (!res.ok) {
    const body = await res.json().catch(() => ({ detail: res.statusText }));
    throw new Error(body.detail || `Failed: ${res.status}`);
  }
  return res.json();
}

export async function fetchAgentState(agentId: string): Promise<{
  agent: ManagedAgent;
  tasks: AgentTask[];
  channels: ChannelBinding[];
  messages: AgentMessage[];
  checkpoint: unknown;
}> {
<<<<<<< ours
  const res = await apiFetch(`${getBase()}/v1/managed-agents/${agentId}/state`);
||||||| base
  const res = await fetch(`${getBase()}/v1/managed-agents/${agentId}/state`);
=======
  const res = await apiFetch(`/v1/managed-agents/${agentId}/state`);
>>>>>>> theirs
  if (!res.ok) throw new Error(`Failed: ${res.status}`);
  return res.json();
}

export interface AgentToolCallStart {
  tool: string;
  arguments: string;
}

export interface AgentToolCallEnd {
  tool: string;
  success: boolean;
  latency: number;
  result?: string;
}

export async function sendAgentMessage(
  agentId: string,
  content: string,
  mode: 'immediate' | 'queued' = 'queued',
  callbacks?: {
    onProgress?: (label: string) => void;
    onContentDelta?: (delta: string, fullContent: string) => void;
    onToolCallStart?: (info: AgentToolCallStart) => void;
    onToolCallEnd?: (info: AgentToolCallEnd) => void;
    onDone?: (fullContent: string, usage?: Record<string, number>, telemetry?: Record<string, unknown>) => void;
  },
): Promise<AgentMessage> {
<<<<<<< ours
  const res = await apiFetch(`${getBase()}/v1/managed-agents/${agentId}/messages`, {
||||||| base
  const res = await fetch(`${getBase()}/v1/managed-agents/${agentId}/messages`, {
=======
  const res = await apiFetch(`/v1/managed-agents/${agentId}/messages`, {
>>>>>>> theirs
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ content, mode, stream: true }),
  });
  if (!res.ok) throw new Error(`Failed: ${res.status}`);

  // If streaming, consume the SSE response so the agent runs
  const contentType = res.headers.get('content-type') || '';
  if (contentType.includes('text/event-stream') && res.body) {
    const reader = res.body.getReader();
    const decoder = new TextDecoder();
    let fullContent = '';
    let buffer = '';
    let lastUsage: Record<string, number> | undefined;
    let lastTelemetry: Record<string, unknown> | undefined;
    let currentEvent: string | undefined;
    try {
      while (true) {
        const { done, value } = await reader.read();
        if (done) break;
        buffer += decoder.decode(value, { stream: true });
        const lines = buffer.split('\n');
        buffer = lines.pop() || '';
        for (const line of lines) {
          if (line.startsWith('event: ')) {
            currentEvent = line.slice(7).trim();
            continue;
          }
          if (!line.startsWith('data: ')) {
            if (line.trim() === '') currentEvent = undefined;
            continue;
          }
          const data = line.slice(6);
          if (data === '[DONE]') {
            currentEvent = undefined;
            continue;
          }
          const evName = currentEvent;
          currentEvent = undefined;

          if (evName === 'tool_call_start') {
            try {
              const parsed = JSON.parse(data);
              callbacks?.onToolCallStart?.({
                tool: parsed.tool,
<<<<<<< ours
                arguments: typeof parsed.arguments === 'object' && parsed.arguments !== null ? JSON.stringify(parsed.arguments) : (parsed.arguments ?? ''),
||||||| base
                arguments: parsed.arguments ?? '',
=======
                arguments: serializeToolCallArguments(parsed.arguments),
>>>>>>> theirs
              });
            } catch {
              /* skip */
            }
            continue;
          }
          if (evName === 'tool_call_end') {
            try {
              const parsed = JSON.parse(data);
              callbacks?.onToolCallEnd?.({
                tool: parsed.tool,
                success: !!parsed.success,
                latency: typeof parsed.latency === 'number' ? parsed.latency : 0,
                result: parsed.result,
              });
            } catch {
              /* skip */
            }
            continue;
          }

          try {
            const chunk = JSON.parse(data);
            // Deep-research branch still uses tool_progress in a data chunk
            const toolProgress = chunk.choices?.[0]?.tool_progress;
            if (toolProgress) {
              callbacks?.onProgress?.(toolProgress);
            }
            const delta = chunk.choices?.[0]?.delta?.content || '';
            if (delta) {
              fullContent += delta;
              callbacks?.onContentDelta?.(delta, fullContent);
            }
            if (chunk.usage) lastUsage = chunk.usage;
            if (chunk.telemetry) lastTelemetry = chunk.telemetry;
          } catch {
            /* skip malformed chunks */
          }
        }
      }
    } catch { /* stream ended */ }

    callbacks?.onDone?.(fullContent, lastUsage, lastTelemetry);

    return {
      id: '',
      agent_id: agentId,
      direction: 'agent_to_user',
      content: fullContent,
      mode,
      status: 'delivered',
      created_at: Date.now() / 1000,
    };
  }

  return res.json();
}

/**
 * Ask the agent a question by triggering an ad-hoc run.
 *
 * Posts the question as an `immediate`, non-streamed message â€” the backend
 * stores it and spawns a real agent tick (`execute_tick`) that consumes it as
 * the run's input (tools, trace, and all), rather than a raw one-shot chat.
 * Returns immediately with the stored user message; progress is observed via
 * the `/v1/agents/events` WebSocket and the resulting trace.
 */
export async function askAgent(agentId: string, content: string): Promise<AgentMessage> {
  const res = await apiFetch(`/v1/managed-agents/${agentId}/messages`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ content, mode: 'immediate', stream: false }),
  });
  if (!res.ok) throw new Error(`Failed: ${res.status}`);
  return res.json();
}

export async function fetchAgentMessages(agentId: string): Promise<AgentMessage[]> {
<<<<<<< ours
  const res = await apiFetch(`${getBase()}/v1/managed-agents/${agentId}/messages`);
||||||| base
  const res = await fetch(`${getBase()}/v1/managed-agents/${agentId}/messages`);
=======
  const res = await apiFetch(`/v1/managed-agents/${agentId}/messages`);
>>>>>>> theirs
  if (!res.ok) throw new Error(`Failed: ${res.status}`);
  const data = await res.json();
  return data.messages || [];
}

export async function fetchErrorAgents(): Promise<ManagedAgent[]> {
<<<<<<< ours
  const res = await apiFetch(`${getBase()}/v1/agents/errors`);
||||||| base
  const res = await fetch(`${getBase()}/v1/agents/errors`);
=======
  const res = await apiFetch(`/v1/agents/errors`);
>>>>>>> theirs
  if (!res.ok) throw new Error(`Failed: ${res.status}`);
  const data = await res.json();
  return data.agents || [];
}

// ---------------------------------------------------------------------------
// Agent Learning + Traces
// ---------------------------------------------------------------------------

export interface LearningLogEntry {
  id: string;
  agent_id: string;
  event_type: string;
  description: string;
  data: Record<string, unknown>;
  created_at: number;
}

export interface AgentTrace {
  id: string;
  outcome: string;
  duration: number;
  started_at: number;
  steps: number;
  error_message?: string;
  metadata?: Record<string, unknown>;
}

export interface ToolInfo {
  name: string;
  description: string;
  category: string;
  source: 'tool' | 'channel';
  requires_credentials: boolean;
  credential_keys: string[];
  configured: boolean;
}

export async function fetchAvailableTools(): Promise<ToolInfo[]> {
<<<<<<< ours
  const res = await apiFetch(`${getBase()}/v1/tools`);
||||||| base
  const res = await fetch(`${getBase()}/v1/tools`);
=======
  const res = await apiFetch(`/v1/tools`);
>>>>>>> theirs
  if (!res.ok) throw new Error(`Failed: ${res.status}`);
  const data = await res.json();
  return data.tools || [];
}

export async function saveToolCredentials(
  toolName: string,
  credentials: Record<string, string>,
): Promise<void> {
<<<<<<< ours
  const res = await apiFetch(`${getBase()}/v1/tools/${toolName}/credentials`, {
||||||| base
  const res = await fetch(`${getBase()}/v1/tools/${toolName}/credentials`, {
=======
  const res = await apiFetch(`/v1/tools/${toolName}/credentials`, {
>>>>>>> theirs
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(credentials),
  });
  if (!res.ok) throw new Error(`Failed: ${res.status}`);
}

export async function fetchToolCredentialStatus(
  toolName: string,
): Promise<Record<string, boolean>> {
  const res = await apiFetch(`/v1/tools/${toolName}/credentials/status`);
  if (!res.ok) throw new Error(`Failed: ${res.status}`);
  return await res.json();
}

export async function deleteToolCredential(
  toolName: string,
  keyName: string,
): Promise<void> {
  const res = await apiFetch(
    `/v1/tools/${encodeURIComponent(toolName)}/credentials/${encodeURIComponent(keyName)}`,
    { method: 'DELETE' },
  );
  if (!res.ok) throw new Error(`Failed: ${res.status}`);
}

export interface AgentTraceDetail {
  id: string;
  agent: string;
  outcome: string;
  duration: number;
  started_at: number;
  steps: Array<{
    step_type: string;
    input: unknown;
    output: string;
    duration: number;
    metadata: Record<string, unknown>;
  }>;
}

export async function fetchLearningLog(agentId: string): Promise<LearningLogEntry[]> {
<<<<<<< ours
  const res = await apiFetch(`${getBase()}/v1/managed-agents/${agentId}/learning`);
||||||| base
  const res = await fetch(`${getBase()}/v1/managed-agents/${agentId}/learning`);
=======
  const res = await apiFetch(`/v1/managed-agents/${agentId}/learning`);
>>>>>>> theirs
  if (!res.ok) throw new Error(`Failed: ${res.status}`);
  const data = await res.json();
  return data.learning_log || [];
}

export async function triggerLearning(agentId: string): Promise<void> {
<<<<<<< ours
  const res = await apiFetch(`${getBase()}/v1/managed-agents/${agentId}/learning/run`, { method: 'POST' });
||||||| base
  const res = await fetch(`${getBase()}/v1/managed-agents/${agentId}/learning/run`, { method: 'POST' });
=======
  const res = await apiFetch(`/v1/managed-agents/${agentId}/learning/run`, { method: 'POST' });
>>>>>>> theirs
  if (!res.ok) throw new Error(`Failed: ${res.status}`);
}

export async function fetchAgentTraces(agentId: string, limit = 20): Promise<AgentTrace[]> {
<<<<<<< ours
  const res = await apiFetch(`${getBase()}/v1/managed-agents/${agentId}/traces?limit=${limit}`);
||||||| base
  const res = await fetch(`${getBase()}/v1/managed-agents/${agentId}/traces?limit=${limit}`);
=======
  const res = await apiFetch(`/v1/managed-agents/${agentId}/traces?limit=${limit}`);
>>>>>>> theirs
  if (!res.ok) throw new Error(`Failed: ${res.status}`);
  const data = await res.json();
  return data.traces || [];
}

export async function fetchAgentTrace(agentId: string, traceId: string): Promise<AgentTraceDetail> {
<<<<<<< ours
  const res = await apiFetch(`${getBase()}/v1/managed-agents/${agentId}/traces/${traceId}`);
||||||| base
  const res = await fetch(`${getBase()}/v1/managed-agents/${agentId}/traces/${traceId}`);
=======
  const res = await apiFetch(`/v1/managed-agents/${agentId}/traces/${traceId}`);
>>>>>>> theirs
  if (!res.ok) throw new Error(`Failed: ${res.status}`);
  return res.json();
}

// ---------------------------------------------------------------------------
// Leaderboard savings submission (Supabase)
// ---------------------------------------------------------------------------

export interface SavingsSubmission {
  anon_id: string;
  display_name: string;
  email: string;
  total_calls: number;
  total_tokens: number;
  dollar_savings: number;
  energy_wh_saved: number;
  flops_saved: number;
  token_counting_version?: number;
}

export async function submitSavings(data: SavingsSubmission): Promise<boolean> {
  if (!SUPABASE_URL || !SUPABASE_ANON_KEY) return false;
  try {
    const res = await fetch(
      `${SUPABASE_URL}/rest/v1/savings_entries?on_conflict=anon_id`,
      {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          apikey: SUPABASE_ANON_KEY,
          Authorization: `Bearer ${SUPABASE_ANON_KEY}`,
          Prefer: 'resolution=merge-duplicates',
        },
        body: JSON.stringify(data),
      },
    );
    return res.ok || res.status === 201 || res.status === 200;
  } catch {
    return false;
  }
}

// ---------------------------------------------------------------------------
// Memory
// ---------------------------------------------------------------------------

export interface MemorySearchResult {
  content: string;
  score: number;
  metadata: Record<string, unknown>;
}

export interface MemoryStats {
  entries: number;
  backend: string;
  [key: string]: unknown;
}

export interface MemoryConfig {
  backend: string;
  // Set by the server when the native `openjarvis_rust` extension is missing,
  // so the UI can show the real cause instead of a healthy-looking config.
  available?: boolean;
  detail?: string | null;
  context_from_memory: boolean;
  context_top_k: number;
  context_min_score: number;
  context_max_tokens: number;
}

/**
 * Extract the server's `detail` message from a failed JSON response so the UI
 * surfaces the real cause (e.g. "openjarvis_rust extension is not installed")
 * instead of a blanket fallback string (#502).
 */
async function memoryErrorDetail(res: Response, fallback: string): Promise<string> {
  try {
    const data = await res.json();
    if (data && typeof data.detail === 'string' && data.detail) return data.detail;
  } catch {
    // Non-JSON body â€” fall through to the generic message below.
  }
  return fallback;
}

export async function getMemoryStats(): Promise<MemoryStats> {
<<<<<<< ours
  const res = await apiFetch(`${getBase()}/v1/memory/stats`);
||||||| base
  const res = await fetch(`${getBase()}/v1/memory/stats`);
=======
  const res = await apiFetch(`/v1/memory/stats`);
>>>>>>> theirs
  if (!res.ok) throw new Error('Failed to fetch memory stats');
  return res.json();
}

export async function searchMemory(query: string, topK: number = 5): Promise<MemorySearchResult[]> {
<<<<<<< ours
  const res = await apiFetch(`${getBase()}/v1/memory/search`, {
||||||| base
  const res = await fetch(`${getBase()}/v1/memory/search`, {
=======
  const res = await apiFetch(`/v1/memory/search`, {
>>>>>>> theirs
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ query, top_k: topK }),
  });
  if (!res.ok) throw new Error('Failed to search memory');
  const data = await res.json();
  return data.results;
}

export async function storeMemory(content: string, metadata?: Record<string, unknown>): Promise<void> {
<<<<<<< ours
  const res = await apiFetch(`${getBase()}/v1/memory/store`, {
||||||| base
  const res = await fetch(`${getBase()}/v1/memory/store`, {
=======
  const res = await apiFetch(`/v1/memory/store`, {
>>>>>>> theirs
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ content, metadata }),
  });
  if (!res.ok) throw new Error(await memoryErrorDetail(res, 'Failed to store memory'));
}

<<<<<<< ours
export async function indexMemoryPath(path: string): Promise<{ chunks_indexed: number }> {
  const res = await apiFetch(`${getBase()}/v1/memory/index`, {
||||||| base
export async function indexMemoryPath(path: string): Promise<{ chunks_indexed: number }> {
  const res = await fetch(`${getBase()}/v1/memory/index`, {
=======
export async function indexMemoryPath(path: string): Promise<{ chunks_indexed: number; note?: string }> {
  const res = await apiFetch(`/v1/memory/index`, {
>>>>>>> theirs
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ path }),
  });
  if (!res.ok) throw new Error(await memoryErrorDetail(res, 'Failed to index path'));
  return res.json();
}

export async function getMemoryConfig(): Promise<MemoryConfig> {
<<<<<<< ours
  const res = await apiFetch(`${getBase()}/v1/memory/config`);
||||||| base
  const res = await fetch(`${getBase()}/v1/memory/config`);
=======
  const res = await apiFetch(`/v1/memory/config`);
>>>>>>> theirs
  if (!res.ok) throw new Error('Failed to fetch memory config');
  return res.json();
}
<<<<<<< ours




// ---------------------------------------------------------------------------
// openjarvis-confirm-ui-v1 - Defect 6 confirmation gate, inbound half
//
// Route read live 2026-09-12 at agent_manager_routes.py:2046-2110.
// Body is confirm_id + decision ONLY. turn_id is NOT sent - it comes back in
// the response from the registry entry (:2100). decision must be the lowercase
// word approve or deny (:2062-2067); anything else is a 400 before the
// registry is touched. Registry is write-once: a second POST reports 409 with
// the decision already held. 404 means the id expired (:2085).
// ---------------------------------------------------------------------------

export interface ConfirmToolResponse {
  ok: boolean;
  status: number;
  body: Record<string, unknown>;
}

export async function confirmTool(
  confirmId: string,
  decision: 'approve' | 'deny',
): Promise<ConfirmToolResponse> {
  const res = await apiFetch(`${getBase()}/v1/tools/confirm`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ confirm_id: confirmId, decision }),
  });
  let body: Record<string, unknown> = {};
  try {
    body = (await res.json()) as Record<string, unknown>;
  } catch {
    body = {};
  }
  return { ok: res.ok, status: res.status, body };
}
||||||| base
=======

// ---------------------------------------------------------------------------
// Approvals
// ---------------------------------------------------------------------------

export interface PendingApproval {
  id: string;
  action_type: string;
  description: string;
  payload: Record<string, unknown>;
  permission_key: string;
  tier: 'trivial' | 'low' | 'medium' | 'high';
  status: string;
  created_at: string;
  expires_at: string;
}

export async function fetchPendingApprovals(): Promise<PendingApproval[]> {
  const res = await apiFetch(`/v1/approvals/pending`);
  if (!res.ok) throw new Error(`Failed: ${res.status}`);
  const data = await res.json();
  return data.actions || [];
}

export async function approveAction(actionId: string): Promise<void> {
  const res = await apiFetch(`/v1/approvals/${actionId}/approve`, { method: 'POST' });
  if (!res.ok) throw new Error(`Failed: ${res.status}`);
}

export async function denyAction(actionId: string): Promise<void> {
  const res = await apiFetch(`/v1/approvals/${actionId}/deny`, { method: 'POST' });
  if (!res.ok) throw new Error(`Failed: ${res.status}`);
}

// ---------------------------------------------------------------------------
// Inference source (desktop only)
// ---------------------------------------------------------------------------

export type InferenceSource = {
  kind: 'ollama' | 'custom';
  model?: string;
  host?: string;
  engine?: string;
};

export async function getInferenceSource(): Promise<InferenceSource> {
  if (isTauri()) {
    try {
      const { invoke } = await import('@tauri-apps/api/core');
      return await invoke<InferenceSource>('get_inference_source');
    } catch (e: any) {
      throw new Error(e?.message ?? e ?? 'Failed to read inference source');
    }
  }
  return { kind: 'ollama' };
}

export async function setInferenceSource(
  src: InferenceSource & { apiKey?: string },
  options: { pending?: boolean } = {},
): Promise<void> {
  if (!isTauri()) throw new Error('Inference source is configurable in the desktop app only.');
  try {
    const { invoke } = await import('@tauri-apps/api/core');
    await invoke<void>('set_inference_source', {
      kind: src.kind,
      model: src.model ?? null,
      host: src.host ?? null,
      engine: src.engine ?? null,
      apiKey: src.apiKey ?? null,
      pending: options.pending ?? null,
    });
  } catch (e: any) {
    // Surface the backend's actionable error strings (e.g. "A server URL is
    // requiredâ€¦", "Could not store the API keyâ€¦") as proper Error instances.
    throw new Error(e?.message ?? e ?? 'Failed to save inference source');
  }
}

/** Stage a first-run choice; Rust confirms it only after backend readiness. */
export const stageInferenceSource = (
  src: InferenceSource & { apiKey?: string },
): Promise<void> => setInferenceSource(src, { pending: true });
>>>>>>> theirs


## ===== frontend/src/lib/sse.ts : OUR COMMITS SINCE AUTHOR BASE =====
0389255b TTS: AudioContext playback engine + ChatArea driver rewrite; mailbox IMAP connector and tools; speech/CSP fixes
bc498a16 feat: Arc Reactor ThinkingCircle, fix env loading, fix project root, add research types, remove debug code
f2fcb30c Graystone Lab: remote MCP/Ollama integration, Rust extension, UI fixes

## ===== frontend/src/lib/sse.ts : CONFLICTED WORKING FILE (diff3) =====
<<<<<<< ours
import type { SSEEvent } from '../types';
import { getBase } from './api';
||||||| base
import type { ResearchEvent, SSEEvent } from '../types';
import { getBase } from './api';
=======
import type { ResearchEvent, SSEEvent } from '../types';
import { getBase, authHeaders } from './api';
>>>>>>> theirs

export type ResearchEvent = SSEEvent;

export interface ChatRequest {
  model: string;
  messages: Array<{ role: string; content: string }>;
  stream: true;
  temperature?: number;
  max_tokens?: number;
  agent?: string;
}

function getAuthHeaders(): Record<string, string> {
  try {
    const raw = localStorage.getItem('openjarvis-settings');
    if (raw) {
      const parsed = JSON.parse(raw);
      if (parsed.apiKey) {
        return { Authorization: `Bearer ${parsed.apiKey}` };
      }
    }
  } catch {}
  return {};
}

export async function* streamChat(
  request: ChatRequest,
  signal?: AbortSignal,
): AsyncGenerator<SSEEvent> {
  const base = getBase();
<<<<<<< ours
||||||| base
  const response = await fetch(`${base}/v1/chat/completions`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(request),
    signal,
  });
=======
  const response = await fetch(`${base}/v1/chat/completions`, {
    method: 'POST',
    headers: authHeaders({ 'Content-Type': 'application/json' }),
    body: JSON.stringify(request),
    signal,
  });
>>>>>>> theirs

  if (!base) {
    throw new Error(
      'API URL not configured. Set VITE_API_URL environment variable or configure in Settings.'
    );
  }

  const timeoutController = new AbortController();
  const timeoutId = setTimeout(() => timeoutController.abort(), 30000);
  const combinedSignal = signal || timeoutController.signal;

  try {
    const response = await fetch(`${base}/v1/chat/completions`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        ...getAuthHeaders(),
      },
      body: JSON.stringify(request),
      signal: combinedSignal,
    });

    clearTimeout(timeoutId);

    if (!response.ok) {
      const errorText = await response.text();
      throw new Error(`Chat request failed (${response.status}): ${errorText}`);
    }

    const reader = response.body?.getReader();
    if (!reader) {
      throw new Error('Streaming response body is not available');
    }

    const decoder = new TextDecoder();
    let buffer = '';

    try {
      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        buffer += decoder.decode(value, { stream: true });
        const lines = buffer.split('\n');
        buffer = lines.pop() || '';

        let currentEvent: string | undefined;

        for (const line of lines) {
          if (line.startsWith('event: ')) {
            currentEvent = line.slice(7).trim();
          } else if (line.startsWith('data: ')) {
            const data = line.slice(6);
            if (data === '[DONE]') return;
            yield { event: currentEvent, data };
            currentEvent = undefined;
          } else if (line.trim() === '') {
            currentEvent = undefined;
          }
        }
      }
    } finally {
      reader.releaseLock();
    }
  } catch (error) {
    clearTimeout(timeoutId);
    throw error;
  }
}

export async function* streamResearch(
<<<<<<< ours
  agentId: string,
  prompt: string,
||||||| base
  query: string,
=======
  query: string,
  model?: string,
>>>>>>> theirs
  signal?: AbortSignal,
): AsyncGenerator<ResearchEvent> {
  const base = getBase();

  if (!base) {
    throw new Error(
      'API URL not configured. Set VITE_API_URL environment variable or configure in Settings.'
    );
  }

  const response = await fetch(`${base}/v1/research/stream`, {
    method: 'POST',
<<<<<<< ours
    headers: {
      'Content-Type': 'application/json',
      ...getAuthHeaders(),
    },
    body: JSON.stringify({ agent_id: agentId, prompt }),
||||||| base
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ query }),
=======
    headers: authHeaders({ 'Content-Type': 'application/json' }),
    body: JSON.stringify({ query, ...(model ? { model } : {}) }),
>>>>>>> theirs
    signal,
  });

  if (!response.ok) {
    const errorText = await response.text();
    throw new Error(`Research stream failed (${response.status}): ${errorText}`);
  }

  const reader = response.body?.getReader();
  if (!reader) {
    throw new Error('Streaming response body is not available');
  }

  const decoder = new TextDecoder();
  let buffer = '';

  try {
    while (true) {
      const { done, value } = await reader.read();
      if (done) break;

      buffer += decoder.decode(value, { stream: true });
      const lines = buffer.split('\n');
      buffer = lines.pop() || '';

      let currentEvent: string | undefined;

      for (const line of lines) {
        if (line.startsWith('event: ')) {
          currentEvent = line.slice(7).trim();
        } else if (line.startsWith('data: ')) {
          const data = line.slice(6);
          if (data === '[DONE]') return;
          yield { event: currentEvent, data };
          currentEvent = undefined;
        } else if (line.trim() === '') {
          currentEvent = undefined;
        }
      }
    }
  } finally {
    reader.releaseLock();
  }
}


## ===== frontend/src/lib/store.ts : OUR COMMITS SINCE AUTHOR BASE =====
0389255b TTS: AudioContext playback engine + ChatArea driver rewrite; mailbox IMAP connector and tools; speech/CSP fixes
e0e36523 Fix: wire tools to native_openhands agent - file_read, think, calculator, code_interpreter, shell_exec, file_write now loading at startup
2e1c5a4d feat: chat input improvements
bc498a16 feat: Arc Reactor ThinkingCircle, fix env loading, fix project root, add research types, remove debug code

## ===== frontend/src/lib/store.ts : CONFLICTED WORKING FILE (diff3) =====
import { create } from 'zustand';
import type {
  Conversation,
  ChatMessage,
  LogEntry,
  ModelInfo,
  MessageTelemetry,
  SavingsData,
  ServerInfo,
  StreamState,
  ToolCallInfo,
  TokenUsage,
} from '../types';
import type { ManagedAgent } from './api';
import { isEmbedOnlyModel } from './model-capabilities';
import { serializeToolCallArguments } from './tool-call';

export interface CachedConnector {
  connector_id: string;
  display_name: string;
  connected: boolean;
  chunks: number;
  auth_type: string;
}

export interface AgentEvent {
  type: string;
  timestamp: number;
  data: Record<string, unknown>;
}

// â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
// localStorage persistence
// â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

const CONVERSATIONS_KEY = 'openjarvis-conversations';
const SETTINGS_KEY = 'openjarvis-settings';
const OPTIN_KEY = 'openjarvis-optin';
const OPTIN_NAME_KEY = 'openjarvis-display-name';
const OPTIN_EMAIL_KEY = 'openjarvis-email';
const OPTIN_ANONID_KEY = 'openjarvis-anon-id';
const OPTIN_SEEN_KEY = 'openjarvis-optin-seen';

interface ConversationStore {
  version: 1;
  conversations: Record<string, Conversation>;
  activeId: string | null;
}

function generateId(): string {
  return Date.now().toString(36) + Math.random().toString(36).slice(2, 8);
}

function loadConversations(): ConversationStore {
  try {
    const raw = localStorage.getItem(CONVERSATIONS_KEY);
    if (!raw) return { version: 1, conversations: {}, activeId: null };
    const parsed = JSON.parse(raw);
    if (parsed.version === 1) {
      let repaired = false;
      for (const conversation of Object.values(parsed.conversations ?? {}) as Conversation[]) {
        for (const message of conversation.messages ?? []) {
          for (const toolCall of message.toolCalls ?? []) {
            const argumentsText = serializeToolCallArguments(toolCall.arguments);
            if (argumentsText !== toolCall.arguments) {
              toolCall.arguments = argumentsText;
              repaired = true;
            }
          }
        }
      }
      if (repaired) {
        try {
          localStorage.setItem(CONVERSATIONS_KEY, JSON.stringify(parsed));
        } catch {
          // Keep the repaired conversations usable in memory when storage is
          // read-only or full. A failed best-effort writeback must not make
          // otherwise readable conversation history disappear from the UI.
        }
      }
      return parsed;
    }
    return { version: 1, conversations: {}, activeId: null };
  } catch {
    return { version: 1, conversations: {}, activeId: null };
  }
}

function saveConversations(store: ConversationStore): void {
  localStorage.setItem(CONVERSATIONS_KEY, JSON.stringify(store));
}

export type ThemeMode = 'light' | 'dark' | 'system';

interface Settings {
  theme: ThemeMode;
  apiUrl: string;
<<<<<<< ours
  apiKey?: string;
||||||| base
=======
  // Local server API key (OPENJARVIS_API_KEY). Sent as a Bearer token on
  // /v1 + /api requests so a key-protected `jarvis serve` doesn't 401 the
  // frontend (#266). Empty = no auth header (keyless local default).
  apiKey: string;
>>>>>>> theirs
  fontSize: 'small' | 'default' | 'large';
  defaultModel: string;
  defaultAgent: string;
  temperature: number;
  maxTokens: number;
  speechEnabled: boolean;
}

function loadSettings(): Settings {
  const defaults: Settings = {
    theme: 'system',
    apiUrl: '',
    apiKey: '',
    fontSize: 'default',
    defaultModel: '',
    defaultAgent: '',
    temperature: 0.7,
    maxTokens: 4096,
    speechEnabled: true,
  };
  try {
    const raw = localStorage.getItem(SETTINGS_KEY);
    if (!raw) return defaults;
    return { ...defaults, ...JSON.parse(raw) };
  } catch {
    return defaults;
  }
}

function saveSettings(settings: Settings): void {
  localStorage.setItem(SETTINGS_KEY, JSON.stringify(settings));
}

// â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
// Store
// â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

const INITIAL_STREAM: StreamState = {
  conversationId: null,
  isStreaming: false,
  phase: '',
  elapsedMs: 0,
  activeToolCalls: [],
  content: '',
};

interface AppState {
  // Conversations
  conversations: Conversation[];
  activeId: string | null;
  setActiveId: (id: string | null) => void;
  messages: ChatMessage[];
  streamState: StreamState;

  // Models & server
  models: ModelInfo[];
  modelsLoading: boolean;
  selectedModel: string;
  serverInfo: ServerInfo | null;
  savings: SavingsData | null;

  // Settings
  settings: Settings;
  updateSettings: (partial: Partial<Settings>) => void;

  // Command palette
  commandPaletteOpen: boolean;
  setCommandPaletteOpen: (open: boolean) => void;

  // Sidebar
  sidebarOpen: boolean;
  toggleSidebar: () => void;
  setSidebarOpen: (open: boolean) => void;

  // System panel
  systemPanelOpen: boolean;
  toggleSystemPanel: () => void;
  setSystemPanelOpen: (open: boolean) => void;

  // Opt-in sharing
  optInEnabled: boolean;
  optInDisplayName: string;
  optInEmail: string;
  optInAnonId: string;
  optInModalSeen: boolean;
  optInModalOpen: boolean;

  // Actions: conversations
  loadConversations: () => void;
  importOverlayConversation: () => Promise<void>;
  createConversation: (model?: string) => string;
  selectConversation: (id: string) => void;
  deleteConversation: (id: string) => void;
  loadMessages: (conversationId: string | null) => void;
  addMessage: (conversationId: string, message: ChatMessage) => void;
  updateLastAssistant: (
    conversationId: string,
    content: string,
    toolCalls?: ToolCallInfo[],
    usage?: TokenUsage,
    telemetry?: MessageTelemetry,
    audio?: { url: string },
    persist?: boolean,
  ) => void;
  setStreamState: (state: Partial<StreamState>) => void;
  resetStream: () => void;

  // Actions: models & server
  setModels: (models: ModelInfo[]) => void;
  setModelsLoading: (loading: boolean) => void;
  setSelectedModel: (model: string) => void;
  setServerInfo: (info: ServerInfo | null) => void;
  setSavings: (data: SavingsData | null) => void;

  // Data sources (cached between visits to avoid empty-state flicker)
  cachedConnectors: CachedConnector[] | null;
  setCachedConnectors: (list: CachedConnector[] | null) => void;

  // Agents
  managedAgents: ManagedAgent[];
  managedAgentsLoading: boolean;
  selectedAgentId: string | null;

  // Actions: agents
  setManagedAgents: (agents: ManagedAgent[]) => void;
  setManagedAgentsLoading: (loading: boolean) => void;
  setSelectedAgentId: (id: string | null) => void;

  // Agent events (live stream)
  agentEvents: AgentEvent[];
  addAgentEvent: (event: AgentEvent) => void;
  clearAgentEvents: () => void;

  // Actions: opt-in sharing
  setOptIn: (enabled: boolean, displayName: string, email: string) => void;
  setOptInModalOpen: (open: boolean) => void;
  markOptInModalSeen: () => void;

  // Logs
  logEntries: LogEntry[];
  addLogEntry: (entry: Omit<LogEntry, 'id'>) => void;
  clearLogs: () => void;

  // Model loading
  modelLoading: boolean;
  setModelLoading: (loading: boolean) => void;
}

export const useAppStore = create<AppState>((set, get) => {
  const initial = loadConversations();
  const convList = Object.values(initial.conversations).sort(
    (a, b) => b.updatedAt - a.updatedAt,
  );

  return {
    conversations: convList,
    activeId: initial.activeId,
    messages:
      initial.activeId && initial.conversations[initial.activeId]
        ? initial.conversations[initial.activeId].messages
        : [],
    streamState: INITIAL_STREAM,

    models: [],
    modelsLoading: true,
    selectedModel: '',
    serverInfo: null,
    savings: null,

    settings: loadSettings(),

    commandPaletteOpen: false,
    sidebarOpen: true,
    systemPanelOpen: true,

    optInEnabled: localStorage.getItem(OPTIN_KEY) === 'true',
    optInDisplayName: localStorage.getItem(OPTIN_NAME_KEY) || '',
    optInEmail: localStorage.getItem(OPTIN_EMAIL_KEY) || '',
    optInAnonId: localStorage.getItem(OPTIN_ANONID_KEY) || crypto.randomUUID(),
    optInModalSeen: localStorage.getItem(OPTIN_SEEN_KEY) === 'true',
    optInModalOpen: false,

    // â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
    // Conversations
    // â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

    loadConversations: () => {
      const store = loadConversations();
      set({
        conversations: Object.values(store.conversations).sort(
          (a, b) => b.updatedAt - a.updatedAt,
        ),
        activeId: store.activeId,
      });
    },

    importOverlayConversation: async () => {
      try {
        const { invoke } = await import('@tauri-apps/api/core');
        const raw = await invoke<string>('get_overlay_conversation');
        if (!raw || raw === '[]') return;
        const overlay = JSON.parse(raw);
        if (!overlay.id || !overlay.messages?.length) return;
        const store = loadConversations();
        const existing = store.conversations[overlay.id];
        // Only update if the overlay has newer/more messages
        if (existing && existing.messages.length >= overlay.messages.length) return;
        store.conversations[overlay.id] = {
          id: overlay.id,
          title: overlay.title || 'Overlay chat',
          createdAt: overlay.createdAt || Date.now(),
          updatedAt: overlay.updatedAt || Date.now(),
          model: overlay.model || 'default',
          messages: overlay.messages,
        };
        saveConversations(store);
        set({
          conversations: Object.values(store.conversations).sort(
            (a, b) => b.updatedAt - a.updatedAt,
          ),
        });
      } catch {
        // Overlay command unavailable (non-Tauri or no overlay data)
      }
    },

    createConversation: (model?: string) => {
      const store = loadConversations();
      const conv: Conversation = {
        id: generateId(),
        title: 'New chat',
        createdAt: Date.now(),
        updatedAt: Date.now(),
        model: model || get().selectedModel || 'default',
        messages: [],
      };
      store.conversations[conv.id] = conv;
      store.activeId = conv.id;
      saveConversations(store);
      set({
        conversations: Object.values(store.conversations).sort(
          (a, b) => b.updatedAt - a.updatedAt,
        ),
        activeId: conv.id,
        messages: [],
      });
      return conv.id;
    },

    selectConversation: (id: string) => {
      const store = loadConversations();
      store.activeId = id;
      saveConversations(store);
      const conv = store.conversations[id];
      set({
        activeId: id,
        messages: conv ? conv.messages : [],
      });
    },

    deleteConversation: (id: string) => {
      const streamState = get().streamState;
      if (streamState.isStreaming && streamState.conversationId === id) return;

      const store = loadConversations();
      delete store.conversations[id];
      if (store.activeId === id) {
        const remaining = Object.keys(store.conversations);
        store.activeId = remaining.length > 0 ? remaining[0] : null;
      }
      saveConversations(store);
      const convList = Object.values(store.conversations).sort(
        (a, b) => b.updatedAt - a.updatedAt,
      );
      const activeConv = store.activeId
        ? store.conversations[store.activeId]
        : null;
      set({
        conversations: convList,
        activeId: store.activeId,
        messages: activeConv ? activeConv.messages : [],
      });
    },

    loadMessages: (conversationId: string | null) => {
      if (!conversationId) {
        set({ messages: [] });
        return;
      }
      const store = loadConversations();
      const conv = store.conversations[conversationId];
      set({ messages: conv ? conv.messages : [] });
    },

    addMessage: (conversationId: string, message: ChatMessage) => {
      const store = loadConversations();
      const conv = store.conversations[conversationId];
      if (!conv) return;
      conv.messages.push(message);
      conv.updatedAt = Date.now();
      if (message.role === 'user' && conv.title === 'New chat') {
        conv.title =
          message.content.slice(0, 50) +
          (message.content.length > 50 ? '...' : '');
      }
      saveConversations(store);
      const conversations = Object.values(store.conversations).sort(
        (a, b) => b.updatedAt - a.updatedAt,
      );
      if (get().activeId === conversationId) {
        set({ messages: [...conv.messages], conversations });
      } else {
        set({ conversations });
      }
    },

    updateLastAssistant: (
      conversationId: string,
      content: string,
      toolCalls?: ToolCallInfo[],
      usage?: TokenUsage,
      telemetry?: MessageTelemetry,
      audio?: { url: string },
      persist: boolean = true,
    ) => {
      const store = loadConversations();
      const conv = store.conversations[conversationId];
      if (!conv) return;
      const lastMsg = conv.messages[conv.messages.length - 1];
      if (lastMsg && lastMsg.role === 'assistant') {
        lastMsg.content = content;
        if (toolCalls) lastMsg.toolCalls = toolCalls;
        if (usage) lastMsg.usage = usage;
        if (telemetry) lastMsg.telemetry = telemetry;
        if (audio) lastMsg.audio = audio;
        conv.updatedAt = Date.now();
<<<<<<< ours
        if (persist) saveConversations(store);
        set({ messages: [...conv.messages] });
||||||| base
        saveConversations(store);
        set({ messages: [...conv.messages] });
=======
        saveConversations(store);
        if (get().activeId === conversationId) {
          set({ messages: [...conv.messages] });
        }
>>>>>>> theirs
      }
    },
    setStreamState: (partial: Partial<StreamState>) => {
      set((s) => ({ streamState: { ...s.streamState, ...partial } }));
    },

    resetStream: () => {
      set({ streamState: INITIAL_STREAM });
    },
    setActiveId: (id: string | null) => {
      const store = loadConversations();
      store.activeId = id;
      saveConversations(store);
      const conv = id ? store.conversations[id] : null;
      set({ activeId: id, messages: conv ? conv.messages : [] });
    },

    // â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
    // Models & server
    // â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

    setModels: (models: ModelInfo[]) =>
      set((state) => {
        // Ollama returns embed-only models (e.g. nomic-embed-text) in the
        // same list as chat models. Auto-picking models[0] selected the
        // embedder and every chat failed with HTTP 400 "does not support
        // chat". Prefer a real chat model for selection / fallback.
        const chatModels = models.filter((m) => !isEmbedOnlyModel(m.id));
        const preferred =
          (state.settings.defaultModel &&
            chatModels.some((m) => m.id === state.settings.defaultModel) &&
            state.settings.defaultModel) ||
          chatModels[0]?.id ||
          models.find((m) => !isEmbedOnlyModel(m.id))?.id ||
          '';

        const currentIsBad =
          !!state.selectedModel && isEmbedOnlyModel(state.selectedModel);
        const currentMissing =
          !!state.selectedModel &&
          !models.some((m) => m.id === state.selectedModel);

        if (!state.selectedModel || currentIsBad || currentMissing) {
          // Prefer a real chat model. If none exist, clear a bad/missing
          // selection rather than keeping an embed-only id that 400s on chat.
          return {
            models,
            selectedModel: preferred,
          };
        }
        return { models };
      }),
    setModelsLoading: (loading: boolean) => set({ modelsLoading: loading }),
    setSelectedModel: (model: string) => set({ selectedModel: model }),
    setServerInfo: (info: ServerInfo | null) => set({ serverInfo: info }),
    setSavings: (data: SavingsData | null) => set({ savings: data }),

    cachedConnectors: null,
    setCachedConnectors: (list) => set({ cachedConnectors: list }),

    // â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
    // Settings
    // â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

    updateSettings: (partial: Partial<Settings>) => {
      const updated = { ...get().settings, ...partial };
      saveSettings(updated);
      set({ settings: updated });
    },

    // â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
    // UI
    // â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

    setCommandPaletteOpen: (open: boolean) => set({ commandPaletteOpen: open }),
    toggleSidebar: () => set((s) => ({ sidebarOpen: !s.sidebarOpen })),
    setSidebarOpen: (open: boolean) => set({ sidebarOpen: open }),
    toggleSystemPanel: () => set((s) => ({ systemPanelOpen: !s.systemPanelOpen })),
    setSystemPanelOpen: (open: boolean) => set({ systemPanelOpen: open }),

    // â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
    // Agents
    // â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

    managedAgents: [],
    managedAgentsLoading: false,
    selectedAgentId: null,

    setManagedAgents: (agents) => set({ managedAgents: agents }),
    setManagedAgentsLoading: (loading) => set({ managedAgentsLoading: loading }),
    setSelectedAgentId: (id) => set({ selectedAgentId: id }),

    agentEvents: [],
    addAgentEvent: (event) => set((s) => ({
      agentEvents: [...s.agentEvents.slice(-99), event],
    })),
    clearAgentEvents: () => set({ agentEvents: [] }),

    // â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
    // Logs
    // â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
    logEntries: [],
    addLogEntry: (entry) => set((s) => ({
      logEntries: [...s.logEntries.slice(-499), { ...entry, id: generateId() }],
    })),
    clearLogs: () => set({ logEntries: [] }),

    // â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
    // Model loading
    // â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
    modelLoading: false,
    setModelLoading: (loading) => set({ modelLoading: loading }),

    // â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
    // Opt-in sharing
    // â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

    setOptIn: (enabled: boolean, displayName: string, email: string) => {
      const anonId = get().optInAnonId;
      localStorage.setItem(OPTIN_KEY, String(enabled));
      localStorage.setItem(OPTIN_NAME_KEY, displayName);
      localStorage.setItem(OPTIN_EMAIL_KEY, email);
      localStorage.setItem(OPTIN_ANONID_KEY, anonId);
      set({ optInEnabled: enabled, optInDisplayName: displayName, optInEmail: email });
    },
    setOptInModalOpen: (open: boolean) => set({ optInModalOpen: open }),
    markOptInModalSeen: () => {
      localStorage.setItem(OPTIN_SEEN_KEY, 'true');
      set({ optInModalSeen: true });
    },
  };
});

export { generateId };

## ===== frontend/src/pages/AgentsPage.tsx : OUR COMMITS SINCE AUTHOR BASE =====
b76b1b13 fix(ui): coerce object tool/arguments fields to string + remove PWA service worker (resolves React #31 stale-bundle boot crash)
bc498a16 feat: Arc Reactor ThinkingCircle, fix env loading, fix project root, add research types, remove debug code
f2fcb30c Graystone Lab: remote MCP/Ollama integration, Rust extension, UI fixes

## ===== frontend/src/pages/AgentsPage.tsx : CONFLICTED WORKING FILE (diff3) =====
import { useEffect, useState, useCallback, useRef } from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import { toast } from 'sonner';
import { useAppStore } from '../lib/store';
import {
  fetchManagedAgents,
  fetchAgentTasks,
  fetchAgentChannels,
  bindAgentChannel,
  unbindAgentChannel,
  fetchTemplates,
  createManagedAgent,
  pauseManagedAgent,
  resumeManagedAgent,
  deleteManagedAgent,
  runManagedAgent,
  recoverManagedAgent,
  askAgent,
  fetchLearningLog,
  triggerLearning,
  fetchAgentTraces,
  fetchAgentTrace,
  fetchManagedAgent,
  fetchAvailableTools,
  fetchModels,
  updateManagedAgent,
  fetchRecommendedModel,
  sendblueVerify,
  sendblueRegisterWebhook,
  sendblueTest,
  sendblueHealth,
} from '../lib/api';
import type { AgentTask, ChannelBinding, AgentTemplate, ManagedAgent, LearningLogEntry, AgentTrace, AgentTraceDetail, ToolInfo } from '../lib/api';
import { useAgentEvents } from '../lib/useAgentEvents';
import type { AgentEvent } from '../lib/useAgentEvents';
import {
  Plus,
  Bot,
  Pause,
  Play,
  Trash2,
  ChevronLeft,
  ListTodo,
  Brain,
  Zap,
  MoreHorizontal,
  AlertTriangle,
  DollarSign,
  Activity,
  MessageSquare,
  Settings,
  FileText,
  X,
  ChevronRight,
  Send,
  RefreshCw,
  Wifi,
  Database,
  Copy,
  Check,
  Pencil,
  Loader2,
} from 'lucide-react';
import { SOURCE_CATALOG } from '../types/connectors';
import type { ConnectRequest } from '../types/connectors';
import { listConnectors, connectSource } from '../lib/connectors-api';
import type { ToolCallInfo } from '../types';
import { ToolCallCard } from '../components/Chat/ToolCallCard';
import { getAgentSchedule, normalizeAgentSchedule } from '../lib/agent-schedule';

// ---------------------------------------------------------------------------
// Status helpers
// ---------------------------------------------------------------------------

type AgentStatus =
  | 'idle'
  | 'running'
  | 'paused'
  | 'error'
  | 'archived'
  | 'needs_attention'
  | 'budget_exceeded'
  | 'stalled';

const STATUS_COLOR: Record<AgentStatus, string> = {
  idle: 'var(--color-success)',
  running: 'var(--color-accent)',
  paused: 'var(--color-text-tertiary)',
  error: 'var(--color-error)',
  archived: 'var(--color-text-tertiary)',
  needs_attention: 'var(--color-warning)',
  budget_exceeded: 'var(--color-warning)',
  stalled: 'var(--color-warning)',
};

function statusColor(s: string): string {
  return STATUS_COLOR[s as AgentStatus] || 'var(--color-text-tertiary)';
}

function StatusBadge({ status }: { status: string }) {
  const color = statusColor(status);
  return (
    <span
      className="px-2 py-0.5 rounded-full text-xs font-medium"
      style={{ background: color + '20', color }}
    >
      {status.replace('_', ' ')}
    </span>
  );
}

function StatusDot({ status }: { status: string }) {
  const color = statusColor(status);
  return (
    <span
      className="w-2 h-2 rounded-full inline-block flex-shrink-0"
      style={{ background: color }}
      title={status}
    />
  );
}

function formatCost(cost?: number): string {
  if (cost === undefined || cost === null) return 'â€”';
  return `$${cost.toFixed(4)}`;
}

function formatRelativeTime(ts?: number | null): string {
  if (!ts) return 'Never';
  const diff = Date.now() - ts * 1000;
  const mins = Math.floor(diff / 60000);
  if (mins < 1) return 'Just now';
  if (mins < 60) return `${mins}m ago`;
  const hours = Math.floor(mins / 60);
  if (hours < 24) return `${hours}h ago`;
  return `${Math.floor(hours / 24)}d ago`;
}

function formatSchedule(type?: string, value?: string): string {
  if (!type || type === 'manual') return 'Manual';
  if (type === 'cron' && value) {
    // Try to display human-readable for common cron patterns
    const parts = value.trim().split(/\s+/);
    if (parts.length === 5) {
      const [min, hour, , , dow] = parts;
      const hourNum = parseInt(hour, 10);
      const formatHour = (h: number) => {
        if (h === 0) return '12:00 AM';
        if (h < 12) return `${h}:00 AM`;
        if (h === 12) return '12:00 PM';
        return `${h - 12}:00 PM`;
      };
      // Daily pattern: 0 H * * *
      if (min === '0' && !isNaN(hourNum) && parts[2] === '*' && parts[3] === '*' && dow === '*') {
        return `Daily at ${formatHour(hourNum)}`;
      }
      // Weekly pattern: 0 H * * days
      if (min === '0' && !isNaN(hourNum) && parts[2] === '*' && parts[3] === '*' && dow !== '*') {
        const DAY_NAMES: Record<string, string> = { '1': 'Mon', '2': 'Tue', '3': 'Wed', '4': 'Thu', '5': 'Fri', '6': 'Sat', '7': 'Sun' };
        const dayList = dow.split(',').map(d => DAY_NAMES[d] || d).join(', ');
        return `Weekly on ${dayList} at ${formatHour(hourNum)}`;
      }
    }
    return `Cron: ${value}`;
  }
  if (type === 'cron') return 'Cron';
  if (type === 'interval' && value) {
    const total = parseInt(value);
    if (!isNaN(total) && total > 0) {
      const h = Math.floor(total / 3600);
      const m = Math.floor((total % 3600) / 60);
      const s = total % 60;
      const parts: string[] = [];
      if (h > 0) parts.push(`${h}h`);
      if (m > 0) parts.push(`${m}m`);
      if (s > 0) parts.push(`${s}s`);
      return `Every ${parts.join(' ') || '0s'}`;
    }
    return `Every ${value}`;
  }
  return type || 'Manual';
}

function formatAgentSchedule(agent: ManagedAgent): string {
  const { type, value } = getAgentSchedule(agent);
  return formatSchedule(type, value);
}

// ---------------------------------------------------------------------------
// Launch Wizard
// ---------------------------------------------------------------------------

const CATEGORY_MAP: Record<string, string> = {
  communication: 'Communication',
  channel: 'Communication',
  search: 'Search & Browse',
  browser: 'Search & Browse',
  code: 'Code & Dev',
  system: 'Code & Dev',
  filesystem: 'Files & Data',
  memory: 'Memory & Knowledge',
  knowledge_graph: 'Memory & Knowledge',
  reasoning: 'Reasoning & AI',
  math: 'Reasoning & AI',
  inference: 'Reasoning & AI',
  agents: 'Reasoning & AI',
  media: 'Media',
};

const TOOL_NAME_FALLBACK: Record<string, string> = {
  file_read: 'Files & Data',
  file_write: 'Files & Data',
  pdf_extract: 'Files & Data',
  db_query: 'Files & Data',
  http_request: 'Files & Data',
  apply_patch: 'Code & Dev',
  git_status: 'Code & Dev',
  git_diff: 'Code & Dev',
  git_log: 'Code & Dev',
  git_commit: 'Code & Dev',
  channel_send: 'Communication',
  channel_list: 'Communication',
  channel_status: 'Communication',
};

const CATEGORY_ORDER = [
  'Communication', 'Search & Browse', 'Code & Dev', 'Files & Data',
  'Memory & Knowledge', 'Reasoning & AI', 'Media',
];

const POPULAR_TOOLS = new Set([
  'slack', 'email', 'telegram', 'whatsapp',
  'web_search', 'browser',
  'code_interpreter', 'shell_exec', 'git_status', 'git_diff',
  'file_read', 'file_write', 'pdf_extract',
  'retrieval', 'memory_store',
  'think', 'llm', 'calculator',
  'image_generate',
]);

const BROWSER_SUB_TOOLS = [
  'browser_navigate', 'browser_click', 'browser_type',
  'browser_screenshot', 'browser_extract', 'browser_axtree',
];

function parseIntervalParts(val: string): { hours: number; minutes: number; seconds: number } {
  const total = parseInt(val) || 0;
  const hours = Math.floor(total / 3600);
  const minutes = Math.floor((total % 3600) / 60);
  const seconds = total % 60;
  return { hours, minutes, seconds };
}

function serializeInterval(hours: number, minutes: number, seconds: number): string {
  return String(hours * 3600 + minutes * 60 + seconds);
}

interface WizardState {
  step: 1 | 2;
  templateId: string;
  templateData: AgentTemplate | null;
  name: string;
  instruction: string;
  model: string;
  scheduleType: string;
  scheduleValue: string;
  selectedTools: string[];
  budget: string;
  routerPolicy: string;
  memoryExtraction: string;
  observationCompression: string;
  retrievalStrategy: string;
  taskDecomposition: string;
  maxTurns: number;
  temperature: number;
}


const TEMPLATE_INSTRUCTIONS: Record<string, string> = {
  'daily-briefing': 'Every morning, give me a fun quote of the day, summarize my top important emails, list any meetings today from my calendar, and tell me the weather for [my city].',
  'daily_briefing': 'Every morning, give me a fun quote of the day, summarize my top important emails, list any meetings today from my calendar, and tell me the weather for [my city].',
  'research-monitor': 'Search for the latest news and papers on [your topic]. Summarize the top 3 most relevant findings and explain why they matter.',
  'research_monitor': 'Search for the latest news and papers on [your topic]. Summarize the top 3 most relevant findings and explain why they matter.',
  'code-reviewer': 'Review the latest commits in [repo]. Check for bugs, security issues, and style violations. Summarize findings with file paths and line numbers.',
  'code_reviewer': 'Review the latest commits in [repo]. Check for bugs, security issues, and style violations. Summarize findings with file paths and line numbers.',
  'meeting-prep': 'Before my next meeting, pull context from my emails, messages, and past meetings with the attendees. Summarize key topics and suggest talking points.',
  'meeting_prep': 'Before my next meeting, pull context from my emails, messages, and past meetings with the attendees. Summarize key topics and suggest talking points.',
  'personal_deep_research': 'Search across all my personal data â€” messages, emails, meetings, documents, and notes â€” to answer [my question]. Cite your sources.',
  'inbox_triager': 'Check my recent emails and messages. Categorize them by priority (urgent, important, FYI, spam). Summarize the top items I should act on.',
};

function Tooltip({ text }: { text: string }) {
  return <span className="inline-block ml-1 cursor-help" style={{ color: 'var(--color-text-tertiary)', fontSize: 10 }} title={text}>(?)</span>;
}

// ---------------------------------------------------------------------------
// ToolsPicker â€” dev-inventory style tool selector used by the launch wizard
// ---------------------------------------------------------------------------

const TOOL_CATEGORY_ORDER = [
  'filesystem',
  'system',
  'code',
  'vcs',
  'storage',
  'memory',
  'knowledge',
  'knowledge_graph',
  'search',
  'network',
  'browser',
  'database',
  'data',
  'math',
  'reasoning',
  'inference',
  'media',
  'audio',
  'skill',
  'channel',
  'communication',
  'other',
];

const TOOL_CATEGORY_LABELS: Record<string, string> = {
  filesystem: 'filesystem',
  system: 'shell & exec',
  code: 'code & repl',
  vcs: 'git',
  storage: 'memory Â· storage',
  memory: 'memory',
  knowledge: 'knowledge',
  knowledge_graph: 'knowledge graph',
  search: 'search',
  network: 'network',
  browser: 'browser',
  database: 'database',
  data: 'data',
  math: 'math',
  reasoning: 'reasoning',
  inference: 'inference',
  media: 'media',
  audio: 'audio',
  skill: 'skills',
  channel: 'channel primitives',
  communication: 'channels',
  other: 'other',
};

function ToolsPicker({
  tools,
  selected,
  onChange,
}: {
  tools: ToolInfo[];
  selected: string[];
  onChange: (next: string[]) => void;
}) {
  const [hovered, setHovered] = useState<ToolInfo | null>(null);
  const [pulseKey, setPulseKey] = useState(0);

  // Channels (source === 'channel') live in ChannelRegistry and aren't
  // directly callable by the LLM â€” the agent talks to them through the
  // `channel_send` tool. Showing them in the tools picker is misleading,
  // so filter them out; channel bindings are configured separately.
  const tollableTools = tools.filter((t) => t.source !== 'channel');

  // Group by category, respecting the preferred order then alphabetical.
  const grouped = (() => {
    const buckets: Record<string, ToolInfo[]> = {};
    for (const t of tollableTools) {
      const cat = TOOL_CATEGORY_ORDER.includes(t.category) ? t.category : 'other';
      (buckets[cat] ||= []).push(t);
    }
    for (const cat of Object.keys(buckets)) {
      buckets[cat].sort((a, b) => a.name.localeCompare(b.name));
    }
    return TOOL_CATEGORY_ORDER
      .filter((cat) => buckets[cat]?.length)
      .map((cat) => ({ category: cat, items: buckets[cat] }));
  })();

  const configurable = tollableTools.filter((t) => t.configured).map((t) => t.name);
  const allSelected =
    configurable.length > 0 && configurable.every((n) => selected.includes(n));

  const toggle = (name: string) => {
    const next = selected.includes(name)
      ? selected.filter((t) => t !== name)
      : [...selected, name];
    onChange(next);
    setPulseKey((k) => k + 1);
  };

  const hint = hovered
    ? hovered.configured
      ? hovered.description || hovered.name
      : `Needs ${hovered.credential_keys.join(', ') || 'credentials'}`
    : 'hover a tool for details';

  return (
    <div>
      <div className="flex items-baseline justify-between mb-1">
        <label
          className="block text-[13px] font-medium"
          style={{ color: 'var(--color-text-secondary)' }}
        >
          Tools
        </label>
        <div className="flex items-center gap-2">
          <span
            key={pulseKey}
            className="tools-count"
            style={{
              fontFamily:
                'ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas, monospace',
              fontSize: 10.5,
              color: 'var(--color-text-tertiary)',
            }}
          >
            <span style={{ color: 'var(--color-accent)' }}>
              {selected.length}
            </span>
            <span style={{ opacity: 0.5 }}> / {tollableTools.length}</span>
          </span>
          <span style={{ color: 'var(--color-text-tertiary)', opacity: 0.3 }}>Â·</span>
          <button
            type="button"
            onClick={() => onChange(allSelected ? [] : configurable)}
            disabled={tools.length === 0}
            className="transition-colors"
            style={{
              fontFamily:
                'ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas, monospace',
              fontSize: 10,
              color: 'var(--color-text-tertiary)',
              background: 'none',
              border: 'none',
              padding: 0,
              cursor: tools.length === 0 ? 'default' : 'pointer',
              textDecoration: 'underline',
              textUnderlineOffset: 2,
            }}
            onMouseEnter={(e) =>
              (e.currentTarget.style.color = 'var(--color-text)')
            }
            onMouseLeave={(e) =>
              (e.currentTarget.style.color = 'var(--color-text-tertiary)')
            }
          >
            {allSelected ? 'none' : 'all'}
          </button>
        </div>
      </div>
      <p
        className="text-[10.5px] mb-2"
        style={{ color: 'var(--color-text-tertiary)' }}
      >
        What the agent is allowed to call. An empty selection makes a
        chat-only agent.
      </p>
      {tools.length === 0 ? (
        <div
          className="px-3 py-2 rounded-lg text-xs"
          style={{
            background: 'var(--color-bg-secondary)',
            border: '1px solid var(--color-border)',
            color: 'var(--color-text-tertiary)',
          }}
        >
          Loading available toolsâ€¦
        </div>
      ) : (
        <div
          className="rounded-lg overflow-hidden"
          style={{
            background: 'var(--color-bg-secondary)',
            border: '1px solid var(--color-border)',
          }}
          onMouseLeave={() => setHovered(null)}
        >
          <div
            className="px-2.5 py-2 overflow-y-auto"
            style={{ maxHeight: 200 }}
          >
            {grouped.map(({ category, items }, idx) => (
              <div key={category} style={{ marginTop: idx === 0 ? 0 : 10 }}>
                <div
                  className="flex items-center gap-1.5 mb-1.5"
                  style={{
                    fontFamily:
                      'ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas, monospace',
                    fontSize: 9.5,
                    color: 'var(--color-text-tertiary)',
                    textTransform: 'uppercase',
                    letterSpacing: '0.1em',
                  }}
                >
                  <span style={{ opacity: 0.5 }}>â”€</span>
                  <span>{TOOL_CATEGORY_LABELS[category] || category}</span>
                  <span
                    className="flex-1"
                    style={{
                      borderBottom: '1px dashed var(--color-border)',
                      marginBottom: 3,
                      opacity: 0.5,
                    }}
                  />
                </div>
                <div className="flex flex-wrap gap-1">
                  {items.map((tool) => {
                    const isSelected = selected.includes(tool.name);
                    const disabled = !tool.configured;
                    return (
                      <button
                        key={tool.name}
                        type="button"
                        disabled={disabled}
                        onClick={() => toggle(tool.name)}
                        onMouseEnter={() => setHovered(tool)}
                        onFocus={() => setHovered(tool)}
                        className="tool-chip"
                        style={{
                          fontFamily:
                            'ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas, monospace',
                          fontSize: 11,
                          lineHeight: 1.2,
                          padding: '3px 7px 3px 5px',
                          borderRadius: 4,
                          display: 'inline-flex',
                          alignItems: 'center',
                          gap: 5,
                          background: isSelected
                            ? 'color-mix(in srgb, var(--color-accent) 14%, transparent)'
                            : 'var(--color-bg)',
                          color: disabled
                            ? 'var(--color-text-tertiary)'
                            : isSelected
                              ? 'var(--color-accent)'
                              : 'var(--color-text-secondary)',
                          border: disabled
                            ? '1px dashed var(--color-border)'
                            : `1px solid ${isSelected ? 'var(--color-accent)' : 'var(--color-border)'}`,
                          boxShadow: isSelected
                            ? 'inset 0 0 0 1px color-mix(in srgb, var(--color-accent) 30%, transparent)'
                            : 'none',
                          cursor: disabled ? 'not-allowed' : 'pointer',
                          opacity: disabled ? 0.55 : 1,
                          transition:
                            'background 120ms, color 120ms, border-color 120ms, transform 80ms',
                        }}
                        onMouseDown={(e) =>
                          !disabled && (e.currentTarget.style.transform = 'scale(0.97)')
                        }
                        onMouseUp={(e) =>
                          (e.currentTarget.style.transform = 'scale(1)')
                        }
                      >
                        <span
                          style={{
                            opacity: isSelected ? 1 : 0.5,
                            color: disabled
                              ? 'var(--color-text-tertiary)'
                              : isSelected
                                ? 'var(--color-accent)'
                                : 'var(--color-text-tertiary)',
                            fontSize: 10.5,
                          }}
                        >
                          {disabled ? 'â¨¯' : isSelected ? 'â–£' : 'â–¡'}
                        </span>
                        <span>{tool.name}</span>
                      </button>
                    );
                  })}
                </div>
              </div>
            ))}
          </div>
          {/* Live description strip */}
          <div
            className="flex items-start gap-2 px-2.5 py-1.5"
            style={{
              borderTop: '1px solid var(--color-border)',
              background: 'var(--color-bg)',
              fontFamily:
                'ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas, monospace',
              fontSize: 10.5,
              color: 'var(--color-text-tertiary)',
              minHeight: 26,
            }}
          >
            <span
              style={{
                color: hovered
                  ? hovered.configured
                    ? 'var(--color-accent)'
                    : '#f59e0b'
                  : 'var(--color-text-tertiary)',
                opacity: hovered ? 1 : 0.5,
              }}
            >
              {hovered ? (hovered.configured ? 'â–¸' : '!') : 'Â·'}
            </span>
            {hovered && (
              <span
                style={{
                  color: 'var(--color-text)',
                  fontWeight: 500,
                }}
              >
                {hovered.name}
              </span>
            )}
            <span
              className="min-w-0 whitespace-normal break-words"
              style={{
                flex: 1,
                color: 'var(--color-text-tertiary)',
                lineHeight: 1.4,
              }}
            >
              {hovered ? `â€” ${hint}` : hint}
            </span>
          </div>
        </div>
      )}
      <style>{`
        @keyframes tools-count-pulse {
          0% { transform: scale(1); }
          40% { transform: scale(1.18); }
          100% { transform: scale(1); }
        }
        .tools-count {
          display: inline-block;
          animation: tools-count-pulse 220ms ease-out;
        }
      `}</style>
    </div>
  );
}

function LaunchWizard({
  templates,
  onClose,
  onLaunched,
}: {
  templates: AgentTemplate[];
  onClose: () => void;
  onLaunched: () => void;
}) {
  const UNIVERSAL_DEFAULTS = {
    memoryExtraction: 'structured_json',
    observationCompression: 'summarize',
    retrievalStrategy: 'sqlite',
    taskDecomposition: 'hierarchical',
    maxTurns: 25,
    temperature: 0.3,
  };

  const [wizard, setWizard] = useState<WizardState>({
    step: 1,
    templateId: '',
    templateData: null,
    name: '',
    instruction: '',
    model: '',
    scheduleType: 'manual',
    scheduleValue: '',
    selectedTools: [],
    budget: '',
    routerPolicy: '',
    ...UNIVERSAL_DEFAULTS,
  });
  const [launching, setLaunching] = useState(false);
  const [recommendedModel, setRecommendedModel] = useState('');
  const [availableTools, setAvailableTools] = useState<ToolInfo[]>([]);
  const models = useAppStore((s) => s.models);

  useEffect(() => {
    fetchRecommendedModel().then((r) => {
      setRecommendedModel(r.model);
      if (!wizard.model) {
        setWizard((w) => ({ ...w, model: r.model }));
      }
    }).catch(() => {});
    fetchAvailableTools().then((tools) => {
      setAvailableTools(tools);
    }).catch(() => {});
  }, []);

  function selectTemplate(tpl: AgentTemplate | null) {
    if (tpl) {
      setWizard((w) => ({
        ...w,
        step: 2,
        templateId: tpl.id,
        templateData: tpl,
        name: '',
        instruction: (tpl as any).instruction || TEMPLATE_INSTRUCTIONS[tpl.id] || '',
        model: recommendedModel || w.model,
        scheduleType: (tpl as any).schedule_type || 'manual',
        scheduleValue: (tpl as any).schedule_value || '',
        selectedTools: (tpl as any).tools || [],
        memoryExtraction: (tpl as any).memory_extraction || UNIVERSAL_DEFAULTS.memoryExtraction,
        observationCompression: (tpl as any).observation_compression || UNIVERSAL_DEFAULTS.observationCompression,
        retrievalStrategy: (tpl as any).retrieval_strategy || UNIVERSAL_DEFAULTS.retrievalStrategy,
        taskDecomposition: (tpl as any).task_decomposition || UNIVERSAL_DEFAULTS.taskDecomposition,
        maxTurns: (tpl as any).max_turns || UNIVERSAL_DEFAULTS.maxTurns,
        temperature: (tpl as any).temperature ?? UNIVERSAL_DEFAULTS.temperature,
      }));
    } else {
      setWizard((w) => ({
        ...w,
        step: 2,
        templateId: '',
        templateData: null,
        name: '',
        instruction: '',
        model: recommendedModel || w.model,
        scheduleType: 'manual',
        scheduleValue: '',
        selectedTools: [],
        ...UNIVERSAL_DEFAULTS,
      }));
    }
  }

  async function handleLaunch() {
    if (!wizard.name.trim()) { toast.error('Name is required'); return; }
    setLaunching(true);
    try {
      const { type: apiScheduleType, value: apiScheduleValue } = normalizeAgentSchedule(
        wizard.scheduleType,
        wizard.scheduleValue,
      );

      const config: Record<string, unknown> = {
        schedule_type: apiScheduleType,
        schedule_value: apiScheduleValue || undefined,
        tools: wizard.selectedTools,
        learning_enabled: !!wizard.routerPolicy,
        memory_extraction: wizard.memoryExtraction,
        observation_compression: wizard.observationCompression,
        retrieval_strategy: wizard.retrievalStrategy,
        task_decomposition: wizard.taskDecomposition,
        max_turns: wizard.maxTurns,
        temperature: wizard.temperature,
      };
      if (wizard.budget) config.budget = parseFloat(wizard.budget);
      if (wizard.instruction.trim()) config.instruction = wizard.instruction.trim();
      if (wizard.model) config.model = wizard.model;
      if (wizard.routerPolicy) config.router_policy = wizard.routerPolicy;

      await createManagedAgent({
        name: wizard.name.trim(),
        template_id: wizard.templateId || undefined,
        config,
      });
      toast.success(`Agent "${wizard.name}" created`);
      onLaunched();
    } catch (err: any) {
      toast.error(err.message || 'Failed to create agent');
    } finally {
      setLaunching(false);
    }
  }

  const formatScheduleLabel = (type: string, value: string) => {
    if (type === 'manual') return 'Manual (run on demand)';
    if (type === 'cron') return `Cron: ${value}`;
    if (type === 'interval') {
      const secs = parseInt(value, 10);
      if (secs >= 3600) return `Every ${secs / 3600}h`;
      if (secs >= 60) return `Every ${secs / 60}m`;
      return `Every ${secs}s`;
    }
    return type;
  };

  // â”€â”€ Step 1: Template Selection â”€â”€
  if (wizard.step === 1) {
    return (
      <div className="fixed inset-0 z-50 flex items-center justify-center" style={{ background: 'rgba(0,0,0,0.6)' }}>
        <div className="rounded-xl p-6 w-full max-w-lg" style={{ background: 'var(--color-bg)', border: '1px solid var(--color-border)' }}>
          <div className="flex justify-between items-center mb-4">
            <h2 className="text-lg font-semibold" style={{ color: 'var(--color-text)' }}>New Agent â€” Choose Template</h2>
            <button onClick={onClose} className="p-1 rounded hover:bg-opacity-10" style={{ color: 'var(--color-text-tertiary)' }}><X size={18} /></button>
          </div>
          <div className="grid grid-cols-2 gap-3">
            {templates.map((tpl) => (
              <button
                key={tpl.id}
                onClick={() => selectTemplate(tpl)}
                className="text-left p-4 rounded-lg transition-all items-start"
                style={{ border: '1px solid var(--color-border)', background: 'var(--color-bg-secondary)' }}
                onMouseEnter={(e) => { e.currentTarget.style.borderColor = 'var(--color-accent)'; e.currentTarget.style.background = 'color-mix(in srgb, var(--color-accent-purple) 6%, transparent)'; }}
                onMouseLeave={(e) => { e.currentTarget.style.borderColor = 'var(--color-border)'; e.currentTarget.style.background = 'var(--color-bg-secondary)'; }}
              >
                <div className="flex items-center gap-2 mb-1">
                  <span className="text-lg">{(tpl as any).icon || 'ðŸ¤–'}</span>
                  <span className="font-semibold text-sm" style={{ color: 'var(--color-text)' }}>{tpl.name}</span>
                </div>
                <div className="text-xs mt-1" style={{ color: 'var(--color-text-tertiary)', textAlign: 'left' }}>{tpl.description}</div>
                {(tpl as any).tools && (
                  <div className="flex flex-wrap gap-1 mt-2">
                    {((tpl as any).tools as string[]).slice(0, 4).map((t: string) => (
                      <span key={t} className="text-xs px-1.5 py-0.5 rounded" style={{ background: 'color-mix(in srgb, var(--color-accent-purple) 12%, transparent)', color: 'var(--color-accent-purple)' }}>{t}</span>
                    ))}
                    {((tpl as any).tools as string[]).length > 4 && (
                      <span className="text-xs px-1.5 py-0.5 rounded" style={{ color: 'var(--color-text-tertiary)' }}>+{((tpl as any).tools as string[]).length - 4}</span>
                    )}
                  </div>
                )}
              </button>
            ))}
            <button
              onClick={() => selectTemplate(null)}
              className="text-left p-4 rounded-lg transition-all items-start"
              style={{ border: '1px solid var(--color-border)', background: 'var(--color-bg-secondary)' }}
              onMouseEnter={(e) => { e.currentTarget.style.borderColor = 'var(--color-accent)'; e.currentTarget.style.background = 'color-mix(in srgb, var(--color-accent-purple) 6%, transparent)'; }}
              onMouseLeave={(e) => { e.currentTarget.style.borderColor = 'var(--color-border)'; e.currentTarget.style.background = 'var(--color-bg-secondary)'; }}
            >
              <div className="flex items-center gap-2 mb-1">
                <span className="text-lg">âš™ï¸</span>
                <span className="font-semibold text-sm" style={{ color: 'var(--color-text)' }}>Custom Agent</span>
              </div>
              <div className="text-xs mt-1" style={{ color: 'var(--color-text-tertiary)', textAlign: 'left' }}>Start from scratch. Pick your own tools, schedule, and behavior.</div>
            </button>
          </div>
        </div>
      </div>
    );
  }

  // â”€â”€ Step 2: Configuration â”€â”€
  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center" style={{ background: 'rgba(0,0,0,0.6)' }}>
      <div className="rounded-xl p-6 w-full max-w-lg max-h-[85vh] overflow-y-auto" style={{ background: 'var(--color-bg)', border: '1px solid var(--color-border)' }}>
        <div className="flex justify-between items-center mb-4">
          <div className="flex items-center gap-2">
            <button onClick={() => setWizard((w) => ({ ...w, step: 1 }))} className="p-1 rounded" style={{ color: 'var(--color-text-tertiary)' }}><ChevronLeft size={18} /></button>
            <h2 className="text-lg font-semibold" style={{ color: 'var(--color-text)' }}>
              {wizard.templateData ? `New ${wizard.templateData.name}` : 'New Custom Agent'}
            </h2>
          </div>
          <button onClick={onClose} className="p-1 rounded" style={{ color: 'var(--color-text-tertiary)' }}><X size={18} /></button>
        </div>

        <div className="space-y-4">
          {/* Name */}
          <div>
            <label className="block text-sm font-medium mb-1" style={{ color: 'var(--color-text-secondary)' }}>Agent Name</label>
            <input
              value={wizard.name}
              onChange={(e) => setWizard((w) => ({ ...w, name: e.target.value }))}
              placeholder="e.g. AI Research Tracker"
              className="w-full px-3 py-2 rounded-lg text-sm bg-transparent"
              style={{ border: '1px solid var(--color-border)', color: 'var(--color-text)' }}
            />
          </div>

          {/* Instruction */}
          <div>
            <label className="block text-sm font-medium mb-1" style={{ color: 'var(--color-text-secondary)' }}>What should this agent do?</label>
            <textarea
              value={wizard.instruction}
              onChange={(e) => setWizard((w) => ({ ...w, instruction: e.target.value }))}
              placeholder="e.g. Monitor the latest research papers on reasoning and chain-of-thought in LLMs"
              rows={3}
              className="w-full px-3 py-2 rounded-lg text-sm bg-transparent resize-none"
              style={{ border: '1px solid var(--color-border)', color: 'var(--color-text)' }}
            />
            {wizard.instruction.includes('[') && (
              <p className="text-[10px] mt-1" style={{ color: 'var(--color-warning)' }}>
                Replace the [bracketed text] with your own values
              </p>
            )}
          </div>

          {/* Tools picker */}
          <ToolsPicker
            tools={availableTools}
            selected={wizard.selectedTools}
            onChange={(next) =>
              setWizard((w) => ({ ...w, selectedTools: next }))
            }
          />

          {/* Model + Schedule row */}
          <div className="grid grid-cols-2 gap-3">
            <div>
              <label className="block text-sm font-medium mb-1" style={{ color: 'var(--color-text-secondary)' }}>Intelligence</label>
              <select
                value={wizard.model}
                onChange={(e) => setWizard((w) => ({ ...w, model: e.target.value }))}
                className="w-full px-3 py-2 rounded-lg text-sm"
                style={{ background: 'var(--color-bg-secondary)', border: '1px solid var(--color-border)', color: 'var(--color-text)' }}
              >
                {models.map((m) => (
                  <option key={m.id} value={m.id}>
                    {m.id}{m.id === recommendedModel ? ' (recommended)' : ''}
                  </option>
                ))}
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium mb-1" style={{ color: 'var(--color-text-secondary)' }}>Schedule</label>
              <select
                value={wizard.scheduleType}
                onChange={(e) => setWizard((w) => ({ ...w, scheduleType: e.target.value, scheduleValue: e.target.value === 'manual' ? '' : w.scheduleValue }))}
                className="w-full px-3 py-2 rounded-lg text-sm"
                style={{ background: 'var(--color-bg-secondary)', border: '1px solid var(--color-border)', color: 'var(--color-text)' }}
              >
                <option value="manual">Manual (run on demand)</option>
                <option value="daily">Daily</option>
                <option value="weekly">Weekly</option>
                <option value="hourly">Every N hours</option>
                <option value="cron">Custom (cron expression)</option>
              </select>
              {wizard.scheduleType === 'daily' && (
                <select
                  value={(() => { const m = wizard.scheduleValue.match(/^0\s+(\d+)\s/); return m ? m[1] : '9'; })()}
                  onChange={(e) => setWizard((w) => ({ ...w, scheduleValue: `0 ${e.target.value} * * *` }))}
                  className="w-full px-3 py-1.5 rounded-lg text-xs mt-1.5"
                  style={{ background: 'var(--color-bg)', border: '1px solid var(--color-border)', color: 'var(--color-text)' }}
                >
                  {Array.from({ length: 24 }, (_, i) => {
                    const label = i === 0 ? '12 AM' : i < 12 ? `${i} AM` : i === 12 ? '12 PM' : `${i - 12} PM`;
                    return <option key={i} value={String(i)}>{label}</option>;
                  })}
                </select>
              )}
              {wizard.scheduleType === 'weekly' && (
                <div className="mt-1.5 space-y-1.5">
                  <div className="flex gap-1">
                    {(['Mon','Tue','Wed','Thu','Fri','Sat','Sun'] as const).map((day, idx) => {
                      const dayNum = String(idx + 1);
                      const cronParts = wizard.scheduleValue.match(/\*\s+\*\s+(.+)$/);
                      const selectedDays = cronParts ? cronParts[1].split(',') : [];
                      const isSelected = selectedDays.includes(dayNum);
                      return (
                        <button
                          key={day}
                          type="button"
                          onClick={() => {
                            const newDays = isSelected ? selectedDays.filter(d => d !== dayNum) : [...selectedDays, dayNum].sort();
                            const hourMatch = wizard.scheduleValue.match(/^0\s+(\d+)\s/);
                            const hour = hourMatch ? hourMatch[1] : '9';
                            setWizard((w) => ({ ...w, scheduleValue: newDays.length > 0 ? `0 ${hour} * * ${newDays.join(',')}` : '' }));
                          }}
                          className="px-1.5 py-1 rounded text-xs font-medium"
                          style={{
                            background: isSelected ? 'var(--color-accent)' : 'var(--color-bg)',
                            color: isSelected ? 'var(--color-on-accent)' : 'var(--color-text-tertiary)',
                            border: `1px solid ${isSelected ? 'var(--color-accent)' : 'var(--color-border)'}`,
                          }}
                        >
                          {day}
                        </button>
                      );
                    })}
                  </div>
                  <select
                    value={(() => { const m = wizard.scheduleValue.match(/^0\s+(\d+)\s/); return m ? m[1] : '9'; })()}
                    onChange={(e) => {
                      const cronParts = wizard.scheduleValue.match(/\*\s+\*\s+(.+)$/);
                      const days = cronParts ? cronParts[1] : '1';
                      setWizard((w) => ({ ...w, scheduleValue: `0 ${e.target.value} * * ${days}` }));
                    }}
                    className="w-full px-3 py-1.5 rounded-lg text-xs"
                    style={{ background: 'var(--color-bg)', border: '1px solid var(--color-border)', color: 'var(--color-text)' }}
                  >
                    {Array.from({ length: 24 }, (_, i) => {
                      const label = i === 0 ? '12 AM' : i < 12 ? `${i} AM` : i === 12 ? '12 PM' : `${i - 12} PM`;
                      return <option key={i} value={String(i)}>{label}</option>;
                    })}
                  </select>
                </div>
              )}
              {wizard.scheduleType === 'hourly' && (
                <div className="flex items-center gap-2 mt-1.5">
                  <span className="text-xs" style={{ color: 'var(--color-text-tertiary)' }}>Every</span>
                  <input
                    type="number" min="1" max="24"
                    value={(() => { const secs = parseInt(wizard.scheduleValue || '0', 10); return secs > 0 ? Math.round(secs / 3600) : 1; })()}
                    onChange={(e) => {
                      const hrs = Math.min(24, Math.max(1, parseInt(e.target.value, 10) || 1));
                      setWizard((w) => ({ ...w, scheduleValue: String(hrs * 3600) }));
                    }}
                    className="w-14 px-2 py-1 rounded text-xs text-center"
                    style={{ background: 'var(--color-bg)', border: '1px solid var(--color-border)', color: 'var(--color-text)' }}
                  />
                  <span className="text-xs" style={{ color: 'var(--color-text-tertiary)' }}>hours</span>
                </div>
              )}
              {wizard.scheduleType === 'cron' && (
                <input
                  value={wizard.scheduleValue}
                  onChange={(e) => setWizard((w) => ({ ...w, scheduleValue: e.target.value }))}
                  placeholder="0 9 * * *"
                  className="w-full px-3 py-1.5 rounded-lg text-xs bg-transparent mt-1.5"
                  style={{ border: '1px solid var(--color-border)', color: 'var(--color-text)' }}
                />
              )}
            </div>
          </div>

          {/* Tools tags */}
          {wizard.selectedTools.length > 0 && (
            <div>
              <label className="block text-sm font-medium mb-1" style={{ color: 'var(--color-text-secondary)' }}>
                Tools <span style={{ color: 'var(--color-text-tertiary)', fontWeight: 400 }}>(from template)</span>
              </label>
              <div className="flex flex-wrap gap-1.5">
                {wizard.selectedTools.map((t) => (
                  <span key={t} className="text-xs px-2 py-1 rounded" style={{ background: 'color-mix(in srgb, var(--color-accent-purple) 12%, transparent)', color: 'var(--color-accent-purple)' }}>{t}</span>
                ))}
              </div>
            </div>
          )}

          {/* Advanced Settings */}
          <details className="rounded-lg" style={{ border: '1px solid var(--color-border)' }}>
            <summary className="px-3 py-2 cursor-pointer text-sm font-medium" style={{ color: 'var(--color-text-tertiary)' }}>
              Advanced Settings <span className="text-xs font-normal">(optional)</span>
            </summary>
            <div className="px-3 pb-3 pt-1 space-y-3" style={{ borderTop: '1px solid var(--color-border)' }}>
              <div className="grid grid-cols-2 gap-3 text-sm">
                <div>
                  <label className="block text-xs mb-1" style={{ color: 'var(--color-text-tertiary)' }}>Memory Extraction<Tooltip text="How the agent remembers context between runs" /></label>
                  <select value={wizard.memoryExtraction} onChange={(e) => setWizard((w) => ({ ...w, memoryExtraction: e.target.value }))}
                    className="w-full px-2 py-1 rounded text-xs" style={{ background: 'var(--color-bg)', border: '1px solid var(--color-border)', color: 'var(--color-text)' }}>
                    <option value="structured_json">Structured JSON</option>
                    <option value="causality_graph">Causality Graph</option>
                    <option value="scratchpad">Scratchpad</option>
                    <option value="none">None</option>
                  </select>
                </div>
                <div>
                  <label className="block text-xs mb-1" style={{ color: 'var(--color-text-tertiary)' }}>Observation Compression<Tooltip text="How the agent summarizes long tool outputs" /></label>
                  <select value={wizard.observationCompression} onChange={(e) => setWizard((w) => ({ ...w, observationCompression: e.target.value }))}
                    className="w-full px-2 py-1 rounded text-xs" style={{ background: 'var(--color-bg)', border: '1px solid var(--color-border)', color: 'var(--color-text)' }}>
                    <option value="summarize">Summarize</option>
                    <option value="truncate">Truncate</option>
                    <option value="none">None</option>
                  </select>
                </div>
                <div>
                  <label className="block text-xs mb-1" style={{ color: 'var(--color-text-tertiary)' }}>Retrieval Strategy<Tooltip text="How the agent searches your knowledge base" /></label>
                  <select value={wizard.retrievalStrategy} onChange={(e) => setWizard((w) => ({ ...w, retrievalStrategy: e.target.value }))}
                    className="w-full px-2 py-1 rounded text-xs" style={{ background: 'var(--color-bg)', border: '1px solid var(--color-border)', color: 'var(--color-text)' }}>
                    <option value="sqlite">BM25 (SQLite FTS5)</option>
                    <option value="hybrid">Hybrid (BM25 + Semantic)</option>
                    <option value="colbert">ColBERTv2</option>
                    <option value="none">None</option>
                  </select>
                </div>
                <div>
                  <label className="block text-xs mb-1" style={{ color: 'var(--color-text-tertiary)' }}>Task Decomposition<Tooltip text="How the agent breaks complex tasks into steps" /></label>
                  <select value={wizard.taskDecomposition} onChange={(e) => setWizard((w) => ({ ...w, taskDecomposition: e.target.value }))}
                    className="w-full px-2 py-1 rounded text-xs" style={{ background: 'var(--color-bg)', border: '1px solid var(--color-border)', color: 'var(--color-text)' }}>
                    <option value="hierarchical">Hierarchical</option>
                    <option value="phased">Phased</option>
                    <option value="monolithic">Monolithic</option>
                  </select>
                </div>
                <div>
                  <label className="block text-xs mb-1" style={{ color: 'var(--color-text-tertiary)' }}>Max Turns</label>
                  <input type="number" value={wizard.maxTurns} onChange={(e) => setWizard((w) => ({ ...w, maxTurns: parseInt(e.target.value, 10) || 25 }))}
                    className="w-full px-2 py-1 rounded text-xs" style={{ background: 'var(--color-bg)', border: '1px solid var(--color-border)', color: 'var(--color-text)' }} />
                </div>
                <div>
                  <label className="block text-xs mb-1" style={{ color: 'var(--color-text-tertiary)' }}>Temperature</label>
                  <input type="number" step="0.1" min="0" max="2" value={wizard.temperature}
                    onChange={(e) => setWizard((w) => ({ ...w, temperature: parseFloat(e.target.value) || 0.3 }))}
                    className="w-full px-2 py-1 rounded text-xs" style={{ background: 'var(--color-bg)', border: '1px solid var(--color-border)', color: 'var(--color-text)' }} />
                </div>
                <div>
                  <label className="block text-xs mb-1" style={{ color: 'var(--color-text-tertiary)' }}>Budget ($)</label>
                  <input type="number" step="0.01" value={wizard.budget} onChange={(e) => setWizard((w) => ({ ...w, budget: e.target.value }))}
                    placeholder="Unlimited"
                    className="w-full px-2 py-1 rounded text-xs" style={{ background: 'var(--color-bg)', border: '1px solid var(--color-border)', color: 'var(--color-text)' }} />
                </div>
                <div>
                  <label className="block text-xs mb-1" style={{ color: 'var(--color-text-tertiary)' }}>Schedule Type</label>
                  <select value={wizard.scheduleType} onChange={(e) => setWizard((w) => ({ ...w, scheduleType: e.target.value, scheduleValue: e.target.value === 'manual' ? '' : w.scheduleValue }))}
                    className="w-full px-2 py-1 rounded text-xs" style={{ background: 'var(--color-bg)', border: '1px solid var(--color-border)', color: 'var(--color-text)' }}>
                    <option value="manual">Manual</option>
                    <option value="daily">Daily</option>
                    <option value="weekly">Weekly</option>
                    <option value="hourly">Every N hours</option>
                    <option value="cron">Custom (cron)</option>
                  </select>
                </div>
              </div>
            </div>
          </details>

          {/* Launch */}
          <div className="flex gap-3 pt-2">
            <button
              onClick={handleLaunch}
              disabled={launching || !wizard.name.trim()}
              className="flex-1 py-2.5 rounded-lg text-sm font-semibold"
              style={{ background: 'var(--color-accent)', color: 'var(--color-on-accent)', opacity: launching || !wizard.name.trim() ? 0.5 : 1 }}
            >
              {launching ? 'Creating...' : 'Launch Agent'}
            </button>
            <button onClick={onClose} className="px-4 py-2.5 rounded-lg text-sm" style={{ border: '1px solid var(--color-border)', color: 'var(--color-text-secondary)' }}>
              Cancel
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}

// ---------------------------------------------------------------------------
// Overflow menu
// ---------------------------------------------------------------------------

function OverflowMenu({
  agentId,
  onDelete,
}: {
  agentId: string;
  onDelete: (id: string) => void;
}) {
  const [open, setOpen] = useState(false);
  const ref = useRef<HTMLDivElement>(null);

  useEffect(() => {
    function handler(e: MouseEvent) {
      if (ref.current && !ref.current.contains(e.target as Node)) setOpen(false);
    }
    document.addEventListener('mousedown', handler);
    return () => document.removeEventListener('mousedown', handler);
  }, []);

  return (
    <div ref={ref} className="relative">
      <button
        onClick={(e) => {
          e.stopPropagation();
          setOpen((v) => !v);
        }}
        className="p-1 rounded cursor-pointer"
        style={{ color: 'var(--color-text-tertiary)' }}
        title="More actions"
      >
        <MoreHorizontal size={14} />
      </button>
      {open && (
        <div
          className="absolute right-0 top-6 z-20 rounded-lg py-1 min-w-[120px]"
          style={{ background: 'var(--color-bg)', border: '1px solid var(--color-border)', boxShadow: '0 4px 12px rgba(0,0,0,0.15)' }}
        >
          <button
            onClick={(e) => {
              e.stopPropagation();
              onDelete(agentId);
              setOpen(false);
            }}
            className="w-full text-left px-3 py-1.5 text-xs cursor-pointer flex items-center gap-2"
            style={{ color: 'var(--color-error)' }}
          >
            <Trash2 size={12} /> Delete
          </button>
        </div>
      )}
    </div>
  );
}

// ---------------------------------------------------------------------------
// Agent List Card
// ---------------------------------------------------------------------------

function AgentCard({
  agent,
  onClick,
  onPause,
  onResume,
  onRun,
  onRecover,
  onDelete,
  onChat,
  onEdit,
}: {
  agent: ManagedAgent;
  onClick: () => void;
  onPause: (id: string) => void;
  onResume: (id: string) => void;
  onRun: (id: string) => void;
  onRecover: (id: string) => void;
  onDelete: (id: string) => void;
  onChat: (id: string) => void;
  onEdit: (id: string) => void;
}) {
  const canPause = agent.status === 'running' || agent.status === 'idle';
  const canResume = agent.status === 'paused';
  const canRecover = agent.status === 'error' || agent.status === 'stalled' || agent.status === 'needs_attention';

  return (
    <div
      onClick={onClick}
      className="p-4 rounded-lg cursor-pointer transition-colors"
      style={{ background: 'var(--color-bg-secondary)', border: '1px solid var(--color-border)' }}
      onMouseEnter={(e) => (e.currentTarget.style.borderColor = 'var(--color-accent)')}
      onMouseLeave={(e) => (e.currentTarget.style.borderColor = 'var(--color-border)')}
    >
      {/* Row 1: Name + status dot */}
      <div className="flex items-center justify-between mb-2">
        <div className="flex items-center gap-2 min-w-0">
          <Bot size={16} style={{ color: 'var(--color-accent)', flexShrink: 0 }} />
          <span className="font-medium text-sm truncate" style={{ color: 'var(--color-text)' }}>
            {agent.name}
          </span>
        </div>
        <StatusDot status={agent.status} />
      </div>

      {/* Row 2: Schedule + last run */}
      <div className="text-xs mb-2 flex items-center gap-3" style={{ color: 'var(--color-text-tertiary)' }}>
        <span>{formatAgentSchedule(agent)}</span>
        <span>Â·</span>
        <span>Last run: {formatRelativeTime(agent.last_run_at)}</span>
      </div>

      {/* Row 3: Stats */}
      <div className="flex items-center gap-4 mb-3 text-xs" style={{ color: 'var(--color-text-secondary)' }}>
        <span className="flex items-center gap-1">
          <Activity size={11} />
          {agent.total_runs ?? 0} runs
        </span>
        <span className="flex items-center gap-1">
          <DollarSign size={11} />
          {formatCost(agent.total_cost)}
        </span>
      </div>

      {/* Budget progress bar */}
      {(agent.config?.max_cost as number) > 0 && (
        <div className="mb-3">
          <div className="flex justify-between text-xs mb-1" style={{ color: 'var(--color-text-tertiary)' }}>
            <span>Budget</span>
            <span>
              {formatCost(agent.total_cost)} / ${(agent.config?.max_cost as number).toFixed(0)}
            </span>
          </div>
          <div className="w-full rounded-full h-1.5" style={{ background: 'var(--color-bg)' }}>
            <div
              className="h-1.5 rounded-full transition-all"
              style={{
                width: `${Math.min(100, ((agent.total_cost ?? 0) / (agent.config?.max_cost as number)) * 100)}%`,
                background:
                  ((agent.total_cost ?? 0) / (agent.config?.max_cost as number)) > 0.9
                    ? 'var(--color-error)'
                    : ((agent.total_cost ?? 0) / (agent.config?.max_cost as number)) > 0.75
                      ? 'var(--color-warning)'
                      : 'var(--color-success)',
              }}
            />
          </div>
        </div>
      )}

      {/* Row 4: Actions */}
      <div className="flex items-center gap-1" onClick={(e) => e.stopPropagation()}>
        <button
          onClick={(e) => { e.stopPropagation(); onChat(agent.id); }}
          className="p-1.5 rounded cursor-pointer transition-colors"
          style={{ background: 'var(--color-bg-tertiary)', color: 'var(--color-text-secondary)' }}
          title="Chat with agent"
        >
          <MessageSquare size={13} />
        </button>
        <button
          onClick={(e) => { e.stopPropagation(); onEdit(agent.id); }}
          className="p-1.5 rounded cursor-pointer transition-colors"
          style={{ background: 'var(--color-bg-tertiary)', color: 'var(--color-text-secondary)' }}
          title="Edit agent"
        >
          <Pencil size={13} />
        </button>
        <button
          onClick={() => onRun(agent.id)}
          className="flex items-center gap-1 px-2 py-1 rounded text-xs cursor-pointer transition-colors"
          style={{ background: 'var(--color-accent)' + '15', color: 'var(--color-accent)' }}
          title="Run now"
        >
          <Zap size={11} /> Run Now
        </button>
        {canPause && (
          <button
            onClick={() => onPause(agent.id)}
            className="p-1 rounded cursor-pointer"
            style={{ color: 'var(--color-text-secondary)' }}
            title="Pause"
          >
            <Pause size={13} />
          </button>
        )}
        {canResume && (
          <button
            onClick={() => onResume(agent.id)}
            className="p-1 rounded cursor-pointer"
            style={{ color: 'var(--color-success)' }}
            title="Resume"
          >
            <Play size={13} />
          </button>
        )}
        {canRecover && (
          <button
            onClick={() => onRecover(agent.id)}
            className="flex items-center gap-1 px-2 py-1 rounded text-xs cursor-pointer"
            style={{ background: 'var(--color-error)20', color: 'var(--color-error)' }}
            title="Recover agent"
          >
            <AlertTriangle size={11} /> Recover
          </button>
        )}
        <div className="ml-auto">
          <OverflowMenu agentId={agent.id} onDelete={onDelete} />
        </div>
      </div>
    </div>
  );
}

// ---------------------------------------------------------------------------
// Detail view â€” Configuration grid with editable model
// ---------------------------------------------------------------------------

function AgentInstructionSection({ agent, onAgentUpdated }: { agent: ManagedAgent; onAgentUpdated: () => void }) {
  const [editing, setEditing] = useState(false);
  const [draft, setDraft] = useState('');
  const currentInstruction = (agent.config?.instruction as string) || '';

  async function save() {
    try {
      const newConfig = { ...(agent.config || {}), instruction: draft.trim() };
      await updateManagedAgent(agent.id, { config: newConfig });
      onAgentUpdated();
    } catch { /* ignore */ }
    setEditing(false);
  }

  return (
    <div
      className="p-3 rounded-lg"
      style={{ background: 'var(--color-bg-secondary)', border: '1px solid var(--color-border)' }}
    >
      <div className="flex items-center gap-2 mb-2">
        <h3 className="text-sm font-semibold" style={{ color: 'var(--color-text)' }}>Instruction</h3>
        {!editing && (
          <button
            onClick={() => { setDraft(currentInstruction); setEditing(true); }}
            className="text-xs px-2 py-0.5 rounded cursor-pointer"
            style={{ color: 'var(--color-accent)', border: '1px solid var(--color-accent)', opacity: 0.8 }}
          >
            Edit
          </button>
        )}
      </div>
      {editing ? (
        <div className="space-y-2">
          <textarea
            autoFocus
            value={draft}
            onChange={(e) => setDraft(e.target.value)}
            rows={3}
            className="w-full px-3 py-2 rounded-lg text-sm bg-transparent resize-none"
            style={{ border: '1px solid var(--color-border)', color: 'var(--color-text)' }}
          />
          <div className="flex gap-2">
            <button onClick={save} className="text-xs px-3 py-1 rounded font-medium cursor-pointer" style={{ background: 'var(--color-accent)', color: 'var(--color-on-accent)' }}>Save</button>
            <button onClick={() => setEditing(false)} className="text-xs px-3 py-1 rounded cursor-pointer" style={{ color: 'var(--color-text-tertiary)', border: '1px solid var(--color-border)' }}>Cancel</button>
          </div>
        </div>
      ) : (
        <p className="text-sm" style={{ color: currentInstruction ? 'var(--color-text)' : 'var(--color-text-tertiary)' }}>
          {currentInstruction || '(No instruction set â€” click Edit to add one)'}
        </p>
      )}
    </div>
  );
}

function AgentConfigGrid({ agent, onAgentUpdated }: { agent: ManagedAgent; onAgentUpdated: () => void }) {
  const [editingModel, setEditingModel] = useState(false);
  const [changingModel, setChangingModel] = useState(false);
  const [models, setModels] = useState<string[]>([]);
  const currentModel = (agent.config?.model as string) || '(default)';

  // Model availability status: 'available' | 'unavailable' | 'unknown'
  const [modelAvailable, setModelAvailable] = useState<'available' | 'unavailable' | 'unknown'>('unknown');
  const [ollamaModels, setOllamaModels] = useState<string[]>([]);

  useEffect(() => {
    let cancelled = false;
    async function checkModel() {
      try {
        // Ask the backend which models are installed rather than hitting
        // Ollama directly from the browser: the backend always knows where
        // Ollama lives (incl. remote) and there's no cross-origin/CORS issue,
        // which is what made the check spuriously report "Not available".
        const installed = (await fetchModels()).map((m) => m.id);
        if (cancelled) return;
        setOllamaModels(installed);
        if (currentModel === '(default)') {
          setModelAvailable(installed.length > 0 ? 'available' : 'unknown');
        } else {
          const isInstalled = installed.some(
            (n) => n === currentModel || n.startsWith(currentModel + ':') || currentModel.startsWith(n.split(':')[0])
          );
          setModelAvailable(isInstalled ? 'available' : 'unavailable');
        }
      } catch {
        if (!cancelled) setModelAvailable('unknown');
      }
    }
    checkModel();
    return () => { cancelled = true; };
  }, [currentModel]);

  async function startEditingModel() {
    try {
      const fetched = (await fetchModels()).map((m) => m.id);
      setModels(fetched);
      // Same backend list drives both the dropdown and the availability dots.
      setOllamaModels(fetched);
    } catch { /* ignore */ }
    setEditingModel(true);
  }

  function isModelInstalled(modelId: string): boolean {
    return ollamaModels.some(
      (n) => n === modelId || n.startsWith(modelId + ':') || modelId.startsWith(n.split(':')[0])
    );
  }

  async function changeModel(newModel: string) {
    setChangingModel(true);
    try {
      const newConfig = { ...(agent.config || {}), model: newModel };
      await updateManagedAgent(agent.id, { config: newConfig });
      onAgentUpdated();
      toast.success(`Model changed to ${newModel}`);
    } catch { /* ignore */ }
    setEditingModel(false);
    setChangingModel(false);
  }

  const modelStatusDot = modelAvailable === 'available'
    ? 'var(--color-success)'
    : modelAvailable === 'unavailable'
      ? 'var(--color-error)'
      : 'var(--color-text-tertiary)';

  const rows: [string, React.ReactNode][] = [
    ['Intelligence', editingModel ? (
      changingModel ? (
        <span className="text-sm" style={{ color: 'var(--color-text-tertiary)' }}>Switching model...</span>
      ) : (
        <select
          autoFocus
          defaultValue={currentModel}
          onChange={(e) => changeModel(e.target.value)}
          onBlur={() => setEditingModel(false)}
          className="text-sm rounded px-1 py-0.5"
          style={{ background: 'var(--color-bg)', border: '1px solid var(--color-border)', color: 'var(--color-text)' }}
        >
          {models.map((m) => {
            const installed = isModelInstalled(m);
            return (
              <option key={m} value={m} style={!installed ? { color: 'var(--color-text-tertiary)' } : undefined}>
                {m}{!installed ? ' (not installed)' : ''}
              </option>
            );
          })}
        </select>
      )
    ) : (
      <span className="flex items-center gap-2">
        <span
          style={{
            width: 8,
            height: 8,
            borderRadius: '50%',
            background: modelStatusDot,
            display: 'inline-block',
            flexShrink: 0,
          }}
          title={
            modelAvailable === 'available' ? 'Model running'
              : modelAvailable === 'unavailable' ? 'Model not available'
                : 'Could not check model status'
          }
        />
        <span style={{ color: 'var(--color-text)' }}>{currentModel}</span>
        {modelAvailable === 'unavailable' && (
          <span className="text-xs" style={{ color: 'var(--color-error)' }}>Not available</span>
        )}
        <button
          onClick={startEditingModel}
          className="text-xs px-2 py-0.5 rounded cursor-pointer"
          style={{
            color: modelAvailable === 'unavailable' ? 'var(--color-error)' : 'var(--color-accent)',
            border: `1px solid ${modelAvailable === 'unavailable' ? 'var(--color-error)' : 'var(--color-accent)'}`,
            opacity: 0.8,
          }}
        >
          Change
        </button>
      </span>
    )],
    ['Agent Type', <span key="at">{agent.agent_type}</span>],
    ['Schedule', <span key="sc">{formatAgentSchedule(agent)}</span>],
    ['Last Run', <span key="lr">{formatRelativeTime(agent.last_run_at)}</span>],
    ['Budget', <span key="bg">{agent.budget ? formatCost(agent.budget) : 'Unlimited'}</span>],
    ['Learning', <span key="le">{agent.learning_enabled ? 'Enabled' : 'Disabled'}</span>],
  ];

  return (
    <div className="grid grid-cols-2 gap-x-6 gap-y-1.5">
      {rows.map(([label, value]) => (
        <div key={label as string} className="flex gap-2 items-center text-sm">
          <span className="font-medium" style={{ color: 'var(--color-text-secondary)', minWidth: 110 }}>{label}</span>
          <span style={{ color: 'var(--color-text)' }}>{value}</span>
        </div>
      ))}
    </div>
  );
}

// ---------------------------------------------------------------------------
// Detail view â€” Interact tab
// ---------------------------------------------------------------------------

<<<<<<< ours
/** AgentMessage extended with optional response metadata for the footer. */
type InteractMessage = AgentMessage & {
  _elapsed?: string;
  _toolCalls?: number;
  _usage?: Record<string, number>;
  _telemetry?: Record<string, unknown>;
  _toolCallDetails?: ToolCallInfo[];
};

function AgentResponseFooter({
  msg, copiedId, onCopy,
}: {
  msg: InteractMessage;
  copiedId: string | null;
  onCopy: (id: string) => void;
}) {
  const [expanded, setExpanded] = useState(false);
  const u = msg._usage;
  const t = msg._telemetry as Record<string, unknown> | undefined;
  const elapsed = msg._elapsed;
  const toolCallDetails = msg._toolCallDetails || [];
  const toolCalls = msg._toolCalls ?? toolCallDetails.length;

  // Build summary line like Chat: "ollama - qwen3.5:9b - 18.3s - 50 tokens"
  const parts: string[] = [];
  if (t?.engine) parts.push(String(t.engine));
  if (t?.model_id) parts.push(String(t.model_id));
  if (elapsed) parts.push(`${elapsed}s`);
  if (u?.prompt_tokens) parts.push(`${u.prompt_tokens} input tokens`);
  if (u?.completion_tokens) parts.push(`${u.completion_tokens} output tokens`);
  if (toolCalls > 0) parts.push(`${toolCalls} tool ${toolCalls === 1 ? 'call' : 'calls'}`);

  const summary = parts.length > 0 ? parts.join(' - ') : elapsed ? `${elapsed}s` : '';

  // Build expanded rows
  const rows: Array<{ label: string; value: string }> = [];
  if (t?.engine) rows.push({ label: 'Engine', value: `${t.engine}${t.model_id ? ` (${t.model_id})` : ''}` });
  if (u) {
    const tokenParts = [];
    if (u.completion_tokens) tokenParts.push(`${u.completion_tokens} generated`);
    if (u.prompt_tokens) tokenParts.push(`${u.prompt_tokens} prompt`);
    if (tokenParts.length) rows.push({ label: 'Tokens', value: tokenParts.join(' Â· ') });
  }
  if (toolCallDetails.length > 0) {
    toolCallDetails.forEach((tc, i) => {
      const prefix = toolCallDetails.length > 1 ? `Tool ${i + 1}` : 'Tool';
      const args = tc.arguments ? ` ${typeof tc.arguments === "object" ? JSON.stringify(tc.arguments) : tc.arguments}` : '';
      rows.push({ label: prefix, value: `${tc.tool}(${args.trim()})` });
    });
  } else if (toolCalls > 0) {
    rows.push({ label: 'Tool calls', value: `${toolCalls}` });
  }
  if (t?.tokens_per_sec) rows.push({ label: 'Speed', value: `${Math.round(Number(t.tokens_per_sec))} tok/s` });
  if (t?.total_ms) rows.push({ label: 'Latency', value: `${(Number(t.total_ms) / 1000).toFixed(1)}s total` });

  if (!summary) return null;

  return (
    <div style={{ borderTop: '1px solid var(--color-border-subtle)', marginTop: 6 }}>
      <div style={{ display: 'flex', alignItems: 'center', paddingTop: 4 }}>
        <button
          onClick={() => rows.length > 0 && setExpanded(!expanded)}
          style={{
            flex: 1, display: 'flex', alignItems: 'center', gap: 6,
            background: 'none', border: 'none', cursor: rows.length > 0 ? 'pointer' : 'default',
            padding: 0, textAlign: 'left',
          }}
        >
          <span style={{ width: 4, height: 4, borderRadius: '50%', background: 'var(--color-accent)', flexShrink: 0 }} />
          <span style={{ fontSize: 11, color: 'var(--color-text-tertiary)', fontFamily: 'system-ui' }}>
            {summary}
          </span>
          {rows.length > 0 && (
            <span style={{ fontSize: 10, color: 'var(--color-text-tertiary)' }}>
              {expanded ? 'â–²' : 'â–¼'}
            </span>
          )}
        </button>
        <button
          onClick={() => onCopy(msg.id)}
          style={{
            background: 'none', border: 'none', cursor: 'pointer',
            color: 'var(--color-text-tertiary)', padding: 2,
            display: 'flex', alignItems: 'center',
          }}
          title="Copy response"
        >
          {copiedId === msg.id ? <Check size={12} /> : <Copy size={12} />}
        </button>
      </div>
      {expanded && rows.length > 0 && (
        <div style={{
          borderRadius: 6, marginTop: 4, padding: '6px 10px',
          background: 'rgba(0, 0, 0, 0.15)',
        }}>
          <div style={{
            display: 'grid', gridTemplateColumns: 'auto 1fr',
            columnGap: 12, rowGap: 2,
          }}>
            {rows.map((row) => (
              <div key={row.label} style={{ display: 'contents' }}>
                <span style={{ fontSize: 11, color: 'var(--color-text-tertiary)', fontFamily: 'monospace' }}>
                  {row.label}
                </span>
                <span style={{ fontSize: 11, color: 'var(--color-text-secondary)', fontFamily: 'monospace' }}>
                  {typeof row.value === "object" && row.value !== null ? JSON.stringify(row.value) : row.value}
                </span>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
||||||| base
/** AgentMessage extended with optional response metadata for the footer. */
type InteractMessage = AgentMessage & {
  _elapsed?: string;
  _toolCalls?: number;
  _usage?: Record<string, number>;
  _telemetry?: Record<string, unknown>;
  _toolCallDetails?: ToolCallInfo[];
};

function AgentResponseFooter({
  msg, copiedId, onCopy,
}: {
  msg: InteractMessage;
  copiedId: string | null;
  onCopy: (id: string) => void;
}) {
  const [expanded, setExpanded] = useState(false);
  const u = msg._usage;
  const t = msg._telemetry as Record<string, unknown> | undefined;
  const elapsed = msg._elapsed;
  const toolCallDetails = msg._toolCallDetails || [];
  const toolCalls = msg._toolCalls ?? toolCallDetails.length;

  // Build summary line like Chat: "ollama - qwen3.5:9b - 18.3s - 50 tokens"
  const parts: string[] = [];
  if (t?.engine) parts.push(String(t.engine));
  if (t?.model_id) parts.push(String(t.model_id));
  if (elapsed) parts.push(`${elapsed}s`);
  if (u?.prompt_tokens) parts.push(`${u.prompt_tokens} input tokens`);
  if (u?.completion_tokens) parts.push(`${u.completion_tokens} output tokens`);
  if (toolCalls > 0) parts.push(`${toolCalls} tool ${toolCalls === 1 ? 'call' : 'calls'}`);

  const summary = parts.length > 0 ? parts.join(' - ') : elapsed ? `${elapsed}s` : '';

  // Build expanded rows
  const rows: Array<{ label: string; value: string }> = [];
  if (t?.engine) rows.push({ label: 'Engine', value: `${t.engine}${t.model_id ? ` (${t.model_id})` : ''}` });
  if (u) {
    const tokenParts = [];
    if (u.completion_tokens) tokenParts.push(`${u.completion_tokens} generated`);
    if (u.prompt_tokens) tokenParts.push(`${u.prompt_tokens} prompt`);
    if (tokenParts.length) rows.push({ label: 'Tokens', value: tokenParts.join(' Â· ') });
  }
  if (toolCallDetails.length > 0) {
    toolCallDetails.forEach((tc, i) => {
      const prefix = toolCallDetails.length > 1 ? `Tool ${i + 1}` : 'Tool';
      const args = tc.arguments ? ` ${tc.arguments}` : '';
      rows.push({ label: prefix, value: `${tc.tool}(${args.trim()})` });
    });
  } else if (toolCalls > 0) {
    rows.push({ label: 'Tool calls', value: `${toolCalls}` });
  }
  if (t?.tokens_per_sec) rows.push({ label: 'Speed', value: `${Math.round(Number(t.tokens_per_sec))} tok/s` });
  if (t?.total_ms) rows.push({ label: 'Latency', value: `${(Number(t.total_ms) / 1000).toFixed(1)}s total` });

  if (!summary) return null;

  return (
    <div style={{ borderTop: '1px solid var(--color-border-subtle)', marginTop: 6 }}>
      <div style={{ display: 'flex', alignItems: 'center', paddingTop: 4 }}>
        <button
          onClick={() => rows.length > 0 && setExpanded(!expanded)}
          style={{
            flex: 1, display: 'flex', alignItems: 'center', gap: 6,
            background: 'none', border: 'none', cursor: rows.length > 0 ? 'pointer' : 'default',
            padding: 0, textAlign: 'left',
          }}
        >
          <span style={{ width: 4, height: 4, borderRadius: '50%', background: 'var(--color-accent)', flexShrink: 0 }} />
          <span style={{ fontSize: 11, color: 'var(--color-text-tertiary)', fontFamily: 'system-ui' }}>
            {summary}
          </span>
          {rows.length > 0 && (
            <span style={{ fontSize: 10, color: 'var(--color-text-tertiary)' }}>
              {expanded ? 'â–²' : 'â–¼'}
            </span>
          )}
        </button>
        <button
          onClick={() => onCopy(msg.id)}
          style={{
            background: 'none', border: 'none', cursor: 'pointer',
            color: 'var(--color-text-tertiary)', padding: 2,
            display: 'flex', alignItems: 'center',
          }}
          title="Copy response"
        >
          {copiedId === msg.id ? <Check size={12} /> : <Copy size={12} />}
        </button>
      </div>
      {expanded && rows.length > 0 && (
        <div style={{
          borderRadius: 6, marginTop: 4, padding: '6px 10px',
          background: 'rgba(0, 0, 0, 0.15)',
        }}>
          <div style={{
            display: 'grid', gridTemplateColumns: 'auto 1fr',
            columnGap: 12, rowGap: 2,
          }}>
            {rows.map((row) => (
              <div key={row.label} style={{ display: 'contents' }}>
                <span style={{ fontSize: 11, color: 'var(--color-text-tertiary)', fontFamily: 'monospace' }}>
                  {row.label}
                </span>
                <span style={{ fontSize: 11, color: 'var(--color-text-secondary)', fontFamily: 'monospace' }}>
                  {row.value}
                </span>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
=======
/** One entry in the live activity feed assembled from agent events. */
type LiveItem =
  | { kind: 'note'; id: string; label: string }
  | { kind: 'tool'; id: string; tool: ToolCallInfo };

/** Convert a persisted trace step into a ToolCallInfo for ToolCallCard. */
function stepToToolCall(
  step: AgentTraceDetail['steps'][number],
  idx: number,
): ToolCallInfo {
  const input = (step.input ?? {}) as { tool?: string; args?: unknown };
  const out = step.output as unknown;
  const result =
    typeof out === 'string'
      ? out
      : out && typeof out === 'object' && 'result' in out
        ? String((out as { result: unknown }).result ?? '')
        : out != null
          ? JSON.stringify(out)
          : '';
  const args = input.args;
  return {
    id: `step-${idx}`,
    tool: input.tool || step.step_type || 'step',
    arguments:
      typeof args === 'string' ? args : args != null ? JSON.stringify(args) : '',
    status: 'success',
    result,
    latency: step.duration ? step.duration * 1000 : undefined,
  };
>>>>>>> theirs
}

// ---------------------------------------------------------------------------
// Interact tab â€” trace viewer (top) + follow-up chat (bottom).
//
// The chat input doesn't open a side-channel chat; it triggers a real ad-hoc
// agent run (execute_tick) with the user's question as input. The trace area
// shows that run live (tick + tool calls over the events WebSocket) and, when
// idle, the last run's trace steps plus the agent's resulting findings â€” so
// users can interrogate the agent about its work ("tell me more about X").
// ---------------------------------------------------------------------------
function InteractTab({ agentId, agentStatus, onRunStateChange }: { agentId: string; agentStatus: string; onRunStateChange?: () => void }) {
  const [agent, setAgent] = useState<ManagedAgent | null>(null);
  const [activity, setActivity] = useState('');
  const [running, setRunning] = useState(agentStatus === 'running');
  const [liveItems, setLiveItems] = useState<LiveItem[]>([]);
  const [lastTrace, setLastTrace] = useState<AgentTraceDetail | null>(null);
  const [input, setInput] = useState('');
  const [sending, setSending] = useState(false);
  const [errorMsg, setErrorMsg] = useState('');
  const [question, setQuestion] = useState(''); // question driving the current/last run
  const [elapsedMs, setElapsedMs] = useState(0);

  const startRef = useRef(0);
  const timerRef = useRef<ReturnType<typeof setInterval> | null>(null);
  const runningRef = useRef(running);
  runningRef.current = running;
  const bottomRef = useRef<HTMLDivElement>(null);

  const clearTimer = useCallback(() => {
    if (timerRef.current) {
      clearInterval(timerRef.current);
      timerRef.current = null;
    }
  }, []);

  // Load idle snapshot: agent record (status + findings) and the latest trace.
  const loadIdle = useCallback(async () => {
    try {
<<<<<<< ours
      const [msgs, agent] = await Promise.all([
        fetchAgentMessages(agentId),
        fetchManagedAgent(agentId),
      ]);
      // Merge server messages with locally-stored metadata, and hydrate
      // server-persisted tool_calls into _toolCallDetails so they survive
      // page reloads.
      const merged: InteractMessage[] = msgs.map((m) => {
        const meta = localMetaRef.current.get(m.content?.slice(0, 100) || '');
        const base = meta ? { ...m, ...meta } : { ...m };
        if (!base._toolCallDetails && m.tool_calls && m.tool_calls.length > 0) {
          base._toolCallDetails = m.tool_calls.map((tc, i) => ({
            id: `${m.id}-tc-${i}`,
            tool: typeof tc.tool === 'object' && tc.tool !== null ? JSON.stringify(tc.tool) : tc.tool,
            arguments: typeof tc.arguments === 'object' && tc.arguments !== null ? JSON.stringify(tc.arguments) : (tc.arguments || ''),
            status: tc.success === false ? 'error' : 'success',
            result: tc.result,
            latency: tc.latency,
          }));
          if (base._toolCalls == null) base._toolCalls = m.tool_calls.length;
||||||| base
      const [msgs, agent] = await Promise.all([
        fetchAgentMessages(agentId),
        fetchManagedAgent(agentId),
      ]);
      // Merge server messages with locally-stored metadata, and hydrate
      // server-persisted tool_calls into _toolCallDetails so they survive
      // page reloads.
      const merged: InteractMessage[] = msgs.map((m) => {
        const meta = localMetaRef.current.get(m.content?.slice(0, 100) || '');
        const base = meta ? { ...m, ...meta } : { ...m };
        if (!base._toolCallDetails && m.tool_calls && m.tool_calls.length > 0) {
          base._toolCallDetails = m.tool_calls.map((tc, i) => ({
            id: `${m.id}-tc-${i}`,
            tool: tc.tool,
            arguments: tc.arguments || '',
            status: tc.success === false ? 'error' : 'success',
            result: tc.result,
            latency: tc.latency,
          }));
          if (base._toolCalls == null) base._toolCalls = m.tool_calls.length;
=======
      const a = await fetchManagedAgent(agentId);
      setAgent(a);
      setActivity(a.current_activity || '');
      try {
        const traces = await fetchAgentTraces(agentId, 1);
        if (traces.length > 0) {
          const detail = await fetchAgentTrace(agentId, traces[0].id);
          setLastTrace(detail);
>>>>>>> theirs
        }
      } catch {
        /* trace store may be empty */
      }
    } catch {
      /* ignore */
    }
  }, [agentId]);

  useEffect(() => {
    loadIdle();
  }, [loadIdle]);

  // Tick the elapsed timer while running.
  useEffect(() => {
    if (!running) {
      clearTimer();
      return;
    }
    if (!startRef.current) startRef.current = Date.now();
    timerRef.current = setInterval(
      () => setElapsedMs(Date.now() - startRef.current),
      100,
    );
    return clearTimer;
  }, [running, clearTimer]);

  const finishRun = useCallback(() => {
    setRunning(false);
    startRef.current = 0;
    clearTimer();
    // Give the backend a beat to persist summary_memory + trace, then refresh
    // both this tab and the parent (so the detail/list status badge flips back
    // from "running" to "idle" without waiting for the slow background poll).
    setTimeout(() => {
      loadIdle();
      onRunStateChange?.();
    }, 500);
  }, [clearTimer, loadIdle, onRunStateChange]);

  // Live trace: assemble events from the agent events WebSocket.
  const onEvent = useCallback(
    (ev: AgentEvent) => {
      const data = ev.data || {};
      switch (ev.type) {
        case 'agent_tick_start': {
          startRef.current = Date.now();
          setElapsedMs(0);
          setRunning(true);
          setErrorMsg('');
          setLiveItems([{ kind: 'note', id: `start-${ev.timestamp}`, label: 'Run started' }]);
          break;
        }
        case 'tool_call_start': {
          const id = `tc-${ev.timestamp}-${Math.random().toString(36).slice(2, 6)}`;
          const args = data.arguments;
          const tc: ToolCallInfo = {
            id,
            tool: String(data.tool || 'tool'),
            arguments:
              typeof args === 'string' ? args : args != null ? JSON.stringify(args) : '',
            status: 'running',
          };
          setLiveItems((prev) => [...prev, { kind: 'tool', id, tool: tc }]);
          break;
        }
        case 'tool_call_end': {
          setLiveItems((prev) => {
            const next = [...prev];
            for (let i = next.length - 1; i >= 0; i--) {
              const it = next[i];
              if (
                it.kind === 'tool' &&
                it.tool.tool === String(data.tool) &&
                it.tool.status === 'running'
              ) {
                next[i] = {
                  ...it,
                  tool: {
                    ...it.tool,
                    status: data.success === false ? 'error' : 'success',
                    result:
                      typeof data.result === 'string' ? data.result : it.tool.result,
                    latency:
                      typeof data.latency === 'number'
                        ? data.latency * 1000
                        : it.tool.latency,
                  },
                };
                break;
              }
            }
            return next;
          });
          break;
        }
        case 'agent_tick_end':
        case 'agent_tick_error': {
          if (ev.type === 'agent_tick_error') {
            setErrorMsg(String(data.error || 'The run failed.'));
          }
          finishRun();
          break;
        }
      }
    },
    [finishRun],
  );

  useAgentEvents(agentId, onEvent, [
    'agent_tick_start',
    'tool_call_start',
    'tool_call_end',
    'agent_tick_end',
    'agent_tick_error',
  ]);

  // Fallback poll â€” WS is primary, but this catches missed tick_end events and
  // runs started elsewhere (e.g. the scheduler or the Overview "Run" button).
  useEffect(() => {
    const iv = setInterval(async () => {
      try {
        const a = await fetchManagedAgent(agentId);
        setActivity(a.current_activity || '');
        if (a.status === 'running' && !runningRef.current) {
          setRunning(true);
        } else if (a.status !== 'running' && runningRef.current) {
          finishRun();
        }
      } catch {
        /* ignore */
      }
    }, 3000);
    return () => clearInterval(iv);
  }, [agentId, finishRun]);

  // Keep pinned to the newest live item.
  useEffect(() => {
    if (running) bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [liveItems, running]);

  async function handleAsk() {
    const q = input.trim();
    if (!q || running || sending) return;
    setInput('');
    setQuestion(q);
    setErrorMsg('');
    setSending(true);
    setLiveItems([{ kind: 'note', id: 'queued', label: 'Starting runâ€¦' }]);
    startRef.current = Date.now();
    setElapsedMs(0);
    try {
      // immediate, non-streamed â†’ triggers a real agent run that consumes the
      // question as input. tick_start over the WS confirms; poll is the backstop.
      await askAgent(agentId, q);
      setRunning(true);
      onRunStateChange?.(); // flip the parent status badge to "running" now
    } catch {
      setErrorMsg('Could not start the agent run.');
      setLiveItems([]);
    } finally {
      setSending(false);
    }
  }

  const isBusy = running || sending;
  const findings = agent?.summary_memory?.trim() || '';
  const traceSteps = lastTrace?.steps ?? [];

  return (
    <div className="flex flex-col" style={{ minHeight: 360 }}>
      {/* â”€â”€ Trace area header â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€ */}
      <div className="flex items-center justify-between mb-2">
        <div
          className="flex items-center gap-2 text-sm font-medium"
          style={{ color: 'var(--color-text)' }}
        >
          <Activity size={14} style={{ color: 'var(--color-accent)' }} />
          Activity trace
        </div>
        <div
          className="flex items-center gap-2 text-xs"
          style={{ color: 'var(--color-text-tertiary)' }}
        >
          {isBusy ? (
            <>
              <span
                className="inline-block w-2 h-2 rounded-full animate-pulse"
                style={{ background: 'var(--color-accent)' }}
              />
              Running{elapsedMs > 0 ? ` Â· ${(elapsedMs / 1000).toFixed(1)}s` : ''}
            </>
          ) : (
            <>
              {agent?.last_run_at
                ? `Last run ${new Date(agent.last_run_at * 1000).toLocaleString()}`
                : 'Idle'}
              {lastTrace && ` Â· ${lastTrace.outcome}`}
            </>
          )}
        </div>
      </div>

      {/* â”€â”€ Trace area body â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€ */}
      <div
        className="flex-1 overflow-y-auto rounded-lg p-3 space-y-3"
        style={{
          background: 'var(--color-bg-secondary)',
          border: '1px solid var(--color-border)',
          maxHeight: 'calc(100vh - 360px)',
          minHeight: 200,
        }}
      >
        {question && (
          <div className="text-xs" style={{ color: 'var(--color-text-tertiary)' }}>
            <span style={{ color: 'var(--color-text-secondary)' }}>Question:</span> {question}
          </div>
        )}

        {errorMsg && (
          <div
            className="text-sm px-3 py-2 rounded-lg"
            style={{
              background: 'rgba(255,80,80,0.08)',
              border: '1px solid var(--color-error)',
              color: 'var(--color-error)',
            }}
          >
            {errorMsg}
          </div>
        )}

        {isBusy ? (
          /* LIVE view â€” current tick */
          <>
            {liveItems.map((it) =>
              it.kind === 'tool' ? (
                <ToolCallCard key={it.id} toolCall={it.tool} />
              ) : (
                <div
                  key={it.id}
                  className="flex items-center gap-2 text-sm"
                  style={{ color: 'var(--color-text-secondary)' }}
                >
                  <span
                    className="inline-block w-2 h-2 rounded-full animate-pulse"
                    style={{ background: 'var(--color-accent)' }}
                  />
                  {it.label}
                </div>
              ),
            )}
            <div
              className="flex items-center gap-2 text-sm"
              style={{ color: 'var(--color-text-secondary)' }}
            >
              <Loader2 size={13} className="animate-spin" style={{ color: 'var(--color-accent)' }} />
              {activity || 'Agent is workingâ€¦'}
            </div>
          </>
        ) : (
          /* IDLE view â€” last run's trace + findings */
          <>
            {traceSteps.length > 0 && (
              <div className="space-y-2">
                {traceSteps.map((s, i) => (
                  <ToolCallCard key={i} toolCall={stepToToolCall(s, i)} />
                ))}
              </div>
            )}
            {findings ? (
              <div
                className="px-3 py-2 rounded-lg text-sm"
                style={{
                  background: 'var(--color-bg)',
                  border: '1px solid var(--color-border)',
                  color: 'var(--color-text)',
                }}
              >
                <div className="text-xs mb-1" style={{ color: 'var(--color-text-tertiary)' }}>
                  Result
                </div>
                <div className="prose prose-sm prose-invert max-w-none">
                  <ReactMarkdown remarkPlugins={[remarkGfm]}>{findings}</ReactMarkdown>
                </div>
              </div>
            ) : (
              traceSteps.length === 0 && (
                <div
                  className="text-sm text-center py-8"
                  style={{ color: 'var(--color-text-tertiary)' }}
                >
                  No runs yet. Ask a question below to run the agent.
                </div>
              )
            )}
          </>
        )}
        <div ref={bottomRef} />
      </div>

      {/* â”€â”€ Follow-up chat input â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€ */}
      <div className="mt-3 pt-3" style={{ borderTop: '1px solid var(--color-border)' }}>
        <textarea
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
              e.preventDefault();
              handleAsk();
            }
          }}
          placeholder={isBusy ? 'Agent is runningâ€¦' : "Ask a follow-up about this agent's workâ€¦"}
          disabled={isBusy}
          className="w-full px-3 py-2 rounded-lg text-sm bg-transparent outline-none resize-none"
          style={{
            border: '1px solid var(--color-border)',
            color: 'var(--color-text)',
            minHeight: 64,
            opacity: isBusy ? 0.6 : 1,
          }}
        />
        <div className="flex items-center justify-between mt-2">
          <span className="text-xs" style={{ color: 'var(--color-text-tertiary)' }}>
            Sends your question as an ad-hoc run â€” results appear in the trace above.
          </span>
          <button
            onClick={handleAsk}
            disabled={isBusy || !input.trim()}
            className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-sm cursor-pointer font-medium"
            style={{
              background: 'var(--color-accent)',
              color: 'var(--color-on-accent)',
              opacity: isBusy || !input.trim() ? 0.5 : 1,
            }}
          >
            {isBusy ? <Loader2 size={13} className="animate-spin" /> : <Send size={13} />}
            {isBusy ? 'Running' : 'Ask'}
          </button>
        </div>
      </div>
    </div>
  );
}

// ---------------------------------------------------------------------------
// Channels tab component (data sources)
// ---------------------------------------------------------------------------

function ChannelsTab({ agentId }: { agentId: string }) {
  const [connectors, setConnectors] = useState<
    Array<{ connector_id: string; display_name: string; connected: boolean; chunks: number }>
  >([]);
  const [expandedId, setExpandedId] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  // suppress unused var â€“ agentId reserved for future per-agent source binding
  void agentId;

  const loadConnectors = useCallback(() => {
    listConnectors()
      .then((list) =>
        setConnectors(
          list.map((c) => ({
            connector_id: c.connector_id,
            display_name: c.display_name,
            connected: c.connected,
            chunks: (c as any).chunks || 0,
          })),
        ),
      )
      .catch(() => {});
  }, []);

  useEffect(() => {
    loadConnectors();
    // Poll every 10s to catch background OAuth completions
    const interval = setInterval(loadConnectors, 10000);
    return () => clearInterval(interval);
  }, [loadConnectors]);

  const handleConnect = async (id: string, req: ConnectRequest) => {
    setLoading(true);
    try {
      await connectSource(id, req);
      setExpandedId(null);
      // Poll for connection status (OAuth flow runs in background thread)
      for (let i = 0; i < 30; i++) {
        await new Promise((r) => setTimeout(r, 3000));
        await loadConnectors();
        // Check if this connector is now connected
        const updated = await listConnectors();
        const target = updated.find((c) => c.connector_id === id);
        if (target?.connected) break;
      }
    } catch {
      // error handling
    } finally {
      setLoading(false);
    }
  };

  const connected = connectors.filter((c) => c.connected);
  const notConnected = connectors.filter((c) => !c.connected);

  // Merge with SOURCE_CATALOG for icons/descriptions
  const getMeta = (id: string) =>
    SOURCE_CATALOG.find((s) => s.connector_id === id);

  const iconMap: Record<string, string> = {
    gmail: '\u2709\uFE0F', gmail_imap: '\u2709\uFE0F', slack: '#',
    imessage: '\uD83D\uDCAC', gdrive: '\uD83D\uDCC1', notion: '\uD83D\uDCC4',
    obsidian: '\uD83D\uDCC1', granola: '\uD83C\uDF99\uFE0F', gcalendar: '\uD83D\uDCC5',
    gcontacts: '\uD83D\uDCC7', outlook: '\u2709\uFE0F', apple_notes: '\uD83C\uDF4E',
    dropbox: '\uD83D\uDCE6', whatsapp: '\uD83D\uDCF1',
  };

  return (
    <div style={{ padding: 16 }}>
      <div style={{
        color: 'var(--color-text-secondary)',
        fontSize: 12, marginBottom: 12,
      }}>
        Data sources your agent can search across
      </div>

      {/* Connected sources grid */}
      {connected.length > 0 && (
        <div style={{
          display: 'grid',
          gridTemplateColumns: '1fr 1fr',
          gap: 6, marginBottom: 12,
        }}>
          {connected.map((c) => {
            const meta = SOURCE_CATALOG.find(s => s.connector_id === c.connector_id);
            const unit = meta?.unitLabel || 'items';
            const isReconnecting = expandedId === c.connector_id;
            return (
            <div
              key={c.connector_id}
              style={{
                background: 'var(--color-bg-secondary)',
                border: '1px solid color-mix(in srgb, var(--color-success) 22%, transparent)',
                borderRadius: 6,
                overflow: 'hidden',
                gridColumn: isReconnecting ? '1 / -1' : undefined,
              }}
            >
              <div style={{
                padding: '12px 14px',
                display: 'flex', alignItems: 'center', gap: 8,
              }}>
                <span style={{ fontSize: 20 }}>{iconMap[c.connector_id] || '\uD83D\uDD17'}</span>
                <div style={{ flex: 1 }}>
                  <div style={{ fontSize: 14, fontWeight: 600 }}>
                    {c.display_name}
                  </div>
                  <div style={{ fontSize: 12, color: c.chunks > 0 ? 'var(--color-success)' : 'var(--color-warning)' }}>
                    {c.chunks > 0
                      ? `${c.chunks.toLocaleString()} ${unit}`
                      : 'Connected â€” no data synced yet'}
                  </div>
                </div>
                <button
                  onClick={() => setExpandedId(isReconnecting ? null : c.connector_id)}
                  style={{
                    fontSize: 10, padding: '3px 10px',
                    background: 'transparent',
                    color: 'var(--color-text-secondary)',
                    border: '1px solid var(--color-border)',
                    borderRadius: 4, cursor: 'pointer',
                  }}
                >
                  {isReconnecting ? 'Cancel' : 'Reconnect'}
                </button>
              </div>
              {isReconnecting && meta?.steps && (
                <div style={{
                  borderTop: '1px solid var(--color-border)',
                  padding: 12,
                }}>
                  <div style={{
                    fontSize: 12, color: 'var(--color-warning)',
                    marginBottom: 8,
                  }}>
                    Re-enter credentials to reconnect this source.
                  </div>
                  {meta.steps.map((step, i) => (
                    <div
                      key={i}
                      style={{
                        background: 'var(--color-bg)',
                        border: '1px solid var(--color-border)',
                        borderRadius: 6, padding: 10,
                        marginBottom: 8,
                      }}
                    >
                      <div style={{
                        color: 'var(--color-accent-purple)', fontSize: 10,
                        fontWeight: 600, marginBottom: 3,
                      }}>
                        STEP {i + 1}
                      </div>
                      <div style={{ fontSize: 12, marginBottom: step.url ? 4 : 0 }}>
                        {step.label}
                      </div>
                      {step.url && (
                        <a
                          href={step.url}
                          target="_blank"
                          rel="noopener noreferrer"
                          style={{
                            color: 'var(--color-accent)', fontSize: 11,
                            textDecoration: 'underline',
                          }}
                        >
                          {step.urlLabel || 'Open'} â†’
                        </a>
                      )}
                    </div>
                  ))}
                  {meta.inputFields && (
                    <InlineConnectForm
                      fields={meta.inputFields}
                      loading={loading}
                      onSubmit={(req) => handleConnect(c.connector_id, req)}
                    />
                  )}
                </div>
              )}
            </div>
            );
          })}
        </div>
      )}

      {/* Not connected grid */}
      {notConnected.length > 0 && (
        <div style={{
          display: 'grid',
          gridTemplateColumns: '1fr 1fr',
          gap: 6,
        }}>
          {notConnected.map((c) => {
            const meta = getMeta(c.connector_id);
            const isExpanded = expandedId === c.connector_id;

            return (
              <div
                key={c.connector_id}
                style={{
                  background: 'var(--color-bg-secondary)',
                  border: '1px dashed var(--color-border)',
                  borderRadius: 6, overflow: 'hidden',
                  opacity: isExpanded ? 1 : 0.6,
                  gridColumn: isExpanded ? '1 / -1' : undefined,
                }}
              >
                <div
                  style={{
                    padding: '12px 14px', display: 'flex',
                    alignItems: 'center', gap: 8,
                    cursor: 'pointer',
                  }}
                  onClick={() =>
                    setExpandedId(isExpanded ? null : c.connector_id)
                  }
                >
                  <span style={{ fontSize: 20 }}>{iconMap[c.connector_id] || '\uD83D\uDD17'}</span>
                  <div style={{ flex: 1 }}>
                    <div style={{ fontSize: 14, fontWeight: 600,
                      color: 'var(--color-text-secondary)' }}>
                      {c.display_name}
                    </div>
                    <div style={{ fontSize: 12,
                      color: 'var(--color-text-secondary)' }}>
                      Not connected
                    </div>
                  </div>
                  <span style={{
                    color: 'var(--color-accent-purple)', fontSize: 11, fontWeight: 500,
                  }}>
                    {isExpanded ? '\u2715 Close' : '+ Add'}
                  </span>
                </div>

                {/* Inline setup panel */}
                {isExpanded && meta?.steps && (
                  <div style={{
                    borderTop: '1px solid var(--color-border)',
                    padding: 12,
                  }}>
                    {meta.steps.map((step, i) => (
                      <div
                        key={i}
                        style={{
                          background: 'var(--color-bg)',
                          border: '1px solid var(--color-border)',
                          borderRadius: 6, padding: 10,
                          marginBottom: 8,
                        }}
                      >
                        <div style={{
                          color: 'var(--color-accent-purple)', fontSize: 10,
                          fontWeight: 600, marginBottom: 3,
                        }}>
                          STEP {i + 1}
                        </div>
                        <div style={{
                          fontSize: 12, marginBottom: step.url ? 4 : 0,
                        }}>
                          {step.label}
                        </div>
                        {step.url && (
                          <a
                            href={step.url}
                            target="_blank"
                            rel="noopener noreferrer"
                            style={{
                              color: 'var(--color-accent)', fontSize: 11,
                              textDecoration: 'underline',
                            }}
                          >
                            {step.urlLabel || 'Open'} {'\u2192'}
                          </a>
                        )}
                      </div>
                    ))}
                    {meta.inputFields && (
                      <InlineConnectForm
                        fields={meta.inputFields}
                        loading={loading}
                        onSubmit={(req) =>
                          handleConnect(c.connector_id, req)
                        }
                      />
                    )}
                    <div style={{
                      fontSize: 10, color: 'var(--color-text-secondary)',
                      textAlign: 'center', marginTop: 8,
                    }}>
                      {'\uD83D\uDD12'} Read-only access {'\u00B7'} No data leaves your device
                    </div>
                  </div>
                )}
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}

function InlineConnectForm({
  fields,
  loading,
  onSubmit,
}: {
  fields: Array<{ name: string; placeholder: string; type?: string }>;
  loading: boolean;
  onSubmit: (req: ConnectRequest) => void;
}) {
  const [inputs, setInputs] = useState<Record<string, string>>({});

  const update = (name: string, value: string) =>
    setInputs((p) => ({ ...p, [name]: value }));

  const allFilled = fields.every((f) => inputs[f.name]?.trim());

  const submit = () => {
    const req: ConnectRequest = {};
    for (const f of fields) {
      if (f.name === 'email') req.email = inputs.email;
      else if (f.name === 'password') req.password = inputs.password;
      else if (f.name === 'token') req.token = inputs.token;
      else if (f.name === 'path') req.path = inputs.path;
    }
    if (req.email && req.password) {
      req.token = `${req.email}:${req.password}`;
      req.code = req.token;
    }
    if (req.token && !req.code) req.code = req.token;
    onSubmit(req);
  };

  return (
    <div>
      {fields.map((f) => (
        <input
          key={f.name}
          value={inputs[f.name] || ''}
          onChange={(e) => update(f.name, e.target.value)}
          placeholder={f.placeholder}
          type={f.type || 'text'}
          style={{
            width: '100%', padding: '7px 10px',
            background: 'var(--color-bg)',
            border: '1px solid var(--color-border)',
            borderRadius: 4, color: 'var(--color-text)',
            fontSize: 12, marginBottom: 6,
            boxSizing: 'border-box',
          }}
        />
      ))}
      <button
        onClick={submit}
        disabled={loading || !allFilled}
        style={{
          width: '100%', padding: 8,
          background: loading || !allFilled ? 'var(--color-disabled-bg)' : 'var(--color-accent-purple)',
          color: 'var(--color-on-accent)', border: 'none',
          borderRadius: 6, fontSize: 12, cursor: 'pointer',
        }}
      >
        {loading ? 'Connecting...' : 'Connect'}
      </button>
    </div>
  );
}

// ---------------------------------------------------------------------------
// Messaging tab component
// ---------------------------------------------------------------------------

interface ChannelField {
  key: string;
  label: string;
  placeholder: string;
  type?: 'text' | 'password';
  required?: boolean;
}

interface MessagingChannelConfig {
  type: string;
  name: string;
  icon: string;
  description: string;
  setupSteps: string[];
  fields: ChannelField[];
  activeLabel: (cfg: Record<string, unknown>) => string;
  howToUse: (cfg: Record<string, unknown>) => string;
}

const MESSAGING_CHANNELS: MessagingChannelConfig[] = [
  // SendBlue (iMessage + SMS) is handled by the dedicated SendBlueWizard above.
  // These are the other supported channels.
  {
    type: 'slack',
    name: 'Slack',
    icon: '#',
    description: 'DM your agent in any Slack workspace',
    setupSteps: [
      '1. Go to api.slack.com/apps â†’ click "Create New App" â†’ choose "From an app manifest"',
      '2. Select your workspace. When asked for the manifest format, choose JSON. Then paste the manifest below (click "Copy" to copy it):',
      'COPYABLE:{"display_information":{"name":"OpenJarvis"},"features":{"app_home":{"home_tab_enabled":true,"messages_tab_enabled":true,"messages_tab_read_only_enabled":false},"bot_user":{"display_name":"OpenJarvis","always_online":true}},"oauth_config":{"scopes":{"bot":["chat:write","im:write","im:read","im:history","mpim:read","mpim:history","users:read","channels:read","channels:history","channels:join","groups:read","groups:history","app_mentions:read"]}},"settings":{"event_subscriptions":{"bot_events":["message.im"]},"socket_mode_enabled":true}}',
      '3. Click "Next" â†’ review the summary â†’ click "Create". Then go to "Install App" in the left sidebar â†’ click "Install to Workspace" â†’ click "Allow"',
      '4. In the left sidebar, click "OAuth & Permissions". Copy the "Bot User OAuth Token" (starts with xoxb-...)',
      '5. In the left sidebar, click "Basic Information" â†’ scroll to "App-Level Tokens" â†’ click "Generate Token and Scopes" â†’ name it "socket" â†’ click "Add Scope" â†’ select "connections:write" â†’ click "Generate" â†’ copy the token (starts with xapp-...)',
      '6. (Optional) Still in "Basic Information", scroll to "Display Information" â†’ upload the OpenJarvis icon as the app icon',
      '7. Paste both tokens below and click Connect',
    ],
    fields: [
      { key: 'bot_token', label: 'Bot Token', placeholder: 'xoxb-...', type: 'password', required: true },
      { key: 'app_token', label: 'App Token', placeholder: 'xapp-...', type: 'password', required: true },
    ],
    activeLabel: () => 'Connected to Slack',
    howToUse: () => 'Open Slack and DM @OpenJarvis to talk to your agent.',
  },
];

// ---------------------------------------------------------------------------
// SendBlue webhook step â€” ngrok tunnel + registration
// ---------------------------------------------------------------------------

function SendBlueWebhookStep({
  apiKey, apiSecret, selectedNumber,
}: {
  apiKey: string; apiSecret: string; selectedNumber: string;
}) {
  const [webhookUrl, setWebhookUrl] = useState('');
  const [webhookStatus, setWebhookStatus] = useState<'idle' | 'registering' | 'done' | 'error'>('idle');

  const registerWebhook = async () => {
    if (!webhookUrl.trim()) return;
    setWebhookStatus('registering');
    try {
      const url = webhookUrl.trim().replace(/\/+$/, '') + '/v1/channels/sendblue/webhook';
      await sendblueRegisterWebhook(apiKey, apiSecret, url);
      setWebhookStatus('done');
    } catch {
      setWebhookStatus('error');
    }
  };

  return (
    <div style={{ borderTop: '1px solid var(--color-border)', padding: 14, background: 'var(--color-bg)' }}>
      <div style={{
        background: 'color-mix(in srgb, var(--color-success) 10%, var(--color-bg))', border: '1px solid color-mix(in srgb, var(--color-success) 22%, transparent)',
        borderRadius: 6, padding: 12, marginBottom: 12, textAlign: 'center',
      }}>
        <div style={{ fontSize: 11, color: 'var(--color-success)', fontWeight: 600, marginBottom: 4 }}>
          {'\u2713'} Your agent is now reachable via iMessage / SMS
        </div>
        <div style={{ fontSize: 18, fontWeight: 700, color: 'var(--color-success)' }}>{selectedNumber}</div>
      </div>

      {/* Webhook / ngrok step */}
      <div style={{ marginTop: 12 }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: 8, marginBottom: 10 }}>
          <span style={{ background: 'var(--color-accent-purple)', color: 'var(--color-on-accent)', borderRadius: '50%', width: 20, height: 20, display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: 11, fontWeight: 700, flexShrink: 0 }}>4</span>
          <span style={{ fontSize: 12, fontWeight: 600 }}>Set up webhook to receive texts</span>
        </div>
        <div style={{
          fontSize: 11, lineHeight: 1.6,
          color: 'var(--color-text-secondary)',
          padding: '8px 10px', marginBottom: 10,
          background: 'var(--color-bg-secondary)',
          borderRadius: 6,
          borderLeft: '3px solid var(--color-accent, var(--color-accent-purple))',
        }}>
          <div><strong>1.</strong> Open a terminal and run: <code style={{ color: 'var(--color-accent)', background: 'var(--color-bg)', padding: '1px 4px', borderRadius: 3 }}>ngrok http 8000</code></div>
          <div style={{ marginTop: 4 }}><strong>2.</strong> Copy the <code style={{ color: 'var(--color-accent)', background: 'var(--color-bg)', padding: '1px 4px', borderRadius: 3 }}>https://</code> forwarding URL</div>
          <div style={{ marginTop: 4 }}><strong>3.</strong> Paste it below and click "Register Webhook"</div>
        </div>
        <div style={{ display: 'flex', gap: 6 }}>
          <input
            value={webhookUrl}
            onChange={(e) => { setWebhookUrl(e.target.value); setWebhookStatus('idle'); }}
            placeholder="https://abc123.ngrok-free.app"
            style={{
              flex: 1, padding: '7px 10px', background: 'var(--color-bg-secondary)',
              border: '1px solid var(--color-border)', borderRadius: 4,
              color: 'var(--color-text)', fontSize: 12, boxSizing: 'border-box' as const,
            }}
          />
          <button
            onClick={registerWebhook}
            disabled={!webhookUrl.trim() || webhookStatus === 'registering'}
            style={{
              fontSize: 11, padding: '7px 14px', whiteSpace: 'nowrap' as const,
              background: webhookStatus === 'done' ? 'var(--color-success)' : 'var(--color-accent-purple)',
              color: 'var(--color-on-accent)', border: 'none', borderRadius: 5,
              cursor: 'pointer', fontWeight: 600,
              opacity: !webhookUrl.trim() || webhookStatus === 'registering' ? 0.5 : 1,
            }}
          >
            {webhookStatus === 'registering' ? 'Registering...'
              : webhookStatus === 'done' ? 'Registered!'
              : webhookStatus === 'error' ? 'Retry'
              : 'Register Webhook'}
          </button>
        </div>
        {webhookStatus === 'done' && (
          <div style={{ fontSize: 11, color: 'var(--color-success)', marginTop: 6 }}>
            Webhook registered! Incoming texts will be forwarded to your agent.
          </div>
        )}
        {webhookStatus === 'error' && (
          <div style={{ fontSize: 11, color: 'var(--color-error)', marginTop: 6 }}>
            Failed to register. Check your ngrok URL and try again.
          </div>
        )}
        <div style={{ fontSize: 10, color: 'var(--color-text-tertiary)', marginTop: 8 }}>
          Don't have ngrok? <a href="https://ngrok.com/download" target="_blank" rel="noopener noreferrer" style={{ color: 'var(--color-accent)', textDecoration: 'underline' }}>Download it free</a>
        </div>
      </div>
    </div>
  );
}

// ---------------------------------------------------------------------------
// SendBlue setup wizard â€” guided multi-step flow
// ---------------------------------------------------------------------------

function SendBlueWizard({
  agentId,
  binding,
  onDone,
  onRemove,
}: {
  agentId: string;
  binding: ChannelBinding | undefined;
  onDone: () => void;
  onRemove: (id: string) => void;
}) {
  const [expanded, setExpanded] = useState(false);
  const [step, setStep] = useState<'idle' | 'creds' | 'verifying' | 'verified' | 'connecting' | 'done' | 'test'>('idle');
  const [apiKey, setApiKey] = useState('');
  const [apiSecret, setApiSecret] = useState('');
  const [numbers, setNumbers] = useState<string[]>([]);
  const [selectedNumber, setSelectedNumber] = useState('');
  const [error, setError] = useState('');
  const [testNumber, setTestNumber] = useState('');
  const [testSent, setTestSent] = useState(false);

  const [healthy, setHealthy] = useState(true);
  const [reconnecting, setReconnecting] = useState(false);

  const isActive = !!binding;
  const activeNumber = (binding?.config?.from_number as string) || '';

  // Check health on mount when active
  useEffect(() => {
    if (!isActive) return;
    sendblueHealth().then((h) => setHealthy(h.ready)).catch(() => setHealthy(false));
  }, [isActive]);

  const handleReconnect = async () => {
    if (!binding) return;
    setReconnecting(true);
    try {
      // Re-bind to re-create the bridge
      const cfg = binding.config || {};
      await unbindAgentChannel(agentId, binding.id);
      await bindAgentChannel(agentId, 'sendblue', cfg as Record<string, unknown>);
      setHealthy(true);
      onDone();
    } catch { /* */ } finally { setReconnecting(false); }
  };

  const cardStyle: React.CSSProperties = {
    background: 'var(--color-bg-secondary)',
    border: isActive ? '1px solid color-mix(in srgb, var(--color-success) 22%, transparent)' : '1px dashed var(--color-border)',
    borderRadius: 8, marginBottom: 10, overflow: 'hidden',
  };

  const btnPrimary: React.CSSProperties = {
    fontSize: 12, padding: '7px 18px', background: 'var(--color-accent-purple)', color: 'var(--color-on-accent)',
    border: 'none', borderRadius: 5, cursor: 'pointer', fontWeight: 600,
  };

  const btnSecondary: React.CSSProperties = {
    fontSize: 11, padding: '5px 14px', background: 'transparent',
    color: 'var(--color-text-secondary)', border: '1px solid var(--color-border)',
    borderRadius: 4, cursor: 'pointer',
  };

  const inputStyle: React.CSSProperties = {
    width: '100%', padding: '7px 10px', background: 'var(--color-bg-secondary)',
    border: '1px solid var(--color-border)', borderRadius: 4,
    color: 'var(--color-text)', fontSize: 12, boxSizing: 'border-box',
  };

  const handleVerify = async () => {
    setError('');
    setStep('verifying');
    try {
      const result = await sendblueVerify(apiKey, apiSecret);
      if (result.valid && result.numbers.length > 0) {
        setNumbers(result.numbers);
        setSelectedNumber(result.numbers[0]);
        setStep('verified');
      } else if (result.valid) {
        // Free tier / shared line â€” no dedicated number returned
        // Move to verified step so user can enter the number manually
        setNumbers([]);
        setSelectedNumber('');
        setStep('verified');
      } else {
        setError('Invalid credentials. Check your API key and secret.');
        setStep('creds');
      }
    } catch (e) {
      setError((e as Error).message);
      setStep('creds');
    }
  };

  const handleConnect = async () => {
    setError('');
    setStep('connecting');
    try {
      // 1. Bind the channel
      await bindAgentChannel(agentId, 'sendblue', {
        api_key_id: apiKey,
        api_secret_key: apiSecret,
        from_number: selectedNumber,
      });
      // 2. Try to auto-register webhook (best effort)
      try {
        const webhookUrl = `${window.location.origin}/webhooks/sendblue`;
        await sendblueRegisterWebhook(apiKey, apiSecret, webhookUrl);
      } catch {
        // Non-fatal â€” user may need to set up ngrok manually
      }
      setStep('done');
      onDone();
    } catch (e) {
      setError((e as Error).message);
      setStep('verified');
    }
  };

  const handleTest = async () => {
    if (!testNumber.trim()) return;
    setError('');
    try {
      const cfg = binding?.config || {};
      await sendblueTest(
        (cfg.api_key_id as string) || apiKey,
        (cfg.api_secret_key as string) || apiSecret,
        activeNumber || selectedNumber,
        testNumber.trim(),
      );
      setTestSent(true);
    } catch (e) {
      setError((e as Error).message);
    }
  };

  // Active state
  if (isActive && !expanded) {
    return (
      <div style={cardStyle}>
        <div style={{ display: 'flex', alignItems: 'center', padding: '12px 14px' }}>
          <span style={{ fontSize: 18, marginRight: 10 }}>{'\uD83D\uDCAC'}</span>
          <div style={{ flex: 1 }}>
            <div style={{ fontWeight: 600, fontSize: 13 }}>iMessage / SMS</div>
            <div style={{ fontSize: 11, color: healthy ? 'var(--color-success)' : 'var(--color-warning)' }}>
              {healthy ? `Active on ${activeNumber}` : `Disconnected â€” ${activeNumber}`}
            </div>
          </div>
          <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
            {!healthy && (
              <button
                onClick={handleReconnect}
                disabled={reconnecting}
                style={{ ...btnPrimary, fontSize: 10, padding: '3px 10px' }}
              >
                {reconnecting ? '...' : 'Reconnect'}
              </button>
            )}
            <span style={{
              background: healthy ? 'color-mix(in srgb, var(--color-success) 22%, transparent)' : 'color-mix(in srgb, var(--color-warning) 18%, var(--color-bg))',
              color: healthy ? 'var(--color-success)' : 'var(--color-warning)',
              padding: '2px 8px', borderRadius: 10, fontSize: 10, fontWeight: 600,
            }}>{healthy ? 'Active' : 'Disconnected'}</span>
            <button onClick={() => setExpanded(true)} style={btnSecondary}>
              Details
            </button>
          </div>
        </div>
      </div>
    );
  }

  // Active + expanded (show how to use + test)
  if (isActive && expanded) {
    return (
      <div style={cardStyle}>
        <div style={{ display: 'flex', alignItems: 'center', padding: '12px 14px' }}>
          <span style={{ fontSize: 18, marginRight: 10 }}>{'\uD83D\uDCAC'}</span>
          <div style={{ flex: 1 }}>
            <div style={{ fontWeight: 600, fontSize: 13 }}>iMessage / SMS</div>
            <div style={{ fontSize: 11, color: 'var(--color-success)' }}>Active on {activeNumber}</div>
          </div>
          <div style={{ display: 'flex', gap: 8 }}>
            <button onClick={() => setExpanded(false)} style={btnSecondary}>Collapse</button>
            <button onClick={() => onRemove(binding!.id)} style={{ ...btnSecondary, color: 'var(--color-error)' }}>Remove</button>
          </div>
        </div>
        <div style={{ borderTop: '1px solid var(--color-border)', padding: 14, background: 'var(--color-bg)' }}>
          <div style={{ fontSize: 12, marginBottom: 10, lineHeight: 1.6 }}>
            {'\u2192'} Text <strong>{activeNumber}</strong> from any phone to talk to your agent.
            Responses arrive as iMessage (blue bubbles) when possible, SMS otherwise.
          </div>

          <div style={{ fontSize: 11, color: 'var(--color-text-secondary)', marginBottom: 8, fontWeight: 600 }}>
            Send a test message
          </div>
          <div style={{ display: 'flex', gap: 6 }}>
            <input
              value={testNumber}
              onChange={(e) => { setTestNumber(e.target.value); setTestSent(false); }}
              placeholder="Your phone number (+1...)"
              style={{ ...inputStyle, flex: 1 }}
            />
            <button
              onClick={handleTest}
              disabled={!testNumber.trim() || testSent}
              style={{ ...btnPrimary, opacity: !testNumber.trim() ? 0.5 : 1 }}
            >
              {testSent ? 'Sent!' : 'Send Test'}
            </button>
          </div>
          {error && <div style={{ color: 'var(--color-error)', fontSize: 11, marginTop: 6 }}>{error}</div>}
        </div>
      </div>
    );
  }

  // Not active â€” setup wizard
  return (
    <div style={cardStyle}>
      {/* Header */}
      <div
        style={{ display: 'flex', alignItems: 'center', padding: '12px 14px', cursor: 'pointer' }}
        onClick={() => setStep(step === 'idle' ? 'creds' : 'idle')}
      >
        <span style={{ fontSize: 18, marginRight: 10 }}>{'\uD83D\uDCAC'}</span>
        <div style={{ flex: 1 }}>
          <div style={{ fontWeight: 600, fontSize: 13 }}>iMessage / SMS</div>
          <div style={{ fontSize: 11, color: 'var(--color-text-secondary)' }}>
            Your agent gets its own phone number â€” text it via iMessage or SMS
          </div>
        </div>
        <button
          onClick={(e) => { e.stopPropagation(); setStep(step === 'idle' ? 'creds' : 'idle'); }}
          style={{ fontSize: 10, padding: '3px 12px', background: 'var(--color-accent-purple)', color: 'var(--color-on-accent)', border: 'none', borderRadius: 5, cursor: 'pointer', fontWeight: 600 }}
        >
          {step === 'idle' ? 'Set Up' : 'Cancel'}
        </button>
      </div>

      {/* Step 1: Sign up + enter credentials */}
      {(step === 'creds' || step === 'verifying') && (
        <div style={{ borderTop: '1px solid var(--color-border)', padding: 14, background: 'var(--color-bg)' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: 8, marginBottom: 10 }}>
            <span style={{ background: 'var(--color-accent-purple)', color: 'var(--color-on-accent)', borderRadius: '50%', width: 20, height: 20, display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: 11, fontWeight: 700, flexShrink: 0 }}>1</span>
            <span style={{ fontSize: 12, fontWeight: 600 }}>Create a SendBlue account</span>
          </div>
          <button
            onClick={() => window.open('https://dashboard.sendblue.com/company-signup', '_blank')}
            style={{ ...btnPrimary, marginBottom: 14, display: 'flex', alignItems: 'center', gap: 6 }}
          >
            Open SendBlue signup {'\u2192'}
          </button>

          <div style={{ display: 'flex', alignItems: 'center', gap: 8, marginBottom: 10 }}>
            <span style={{ background: 'var(--color-accent-purple)', color: 'var(--color-on-accent)', borderRadius: '50%', width: 20, height: 20, display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: 11, fontWeight: 700, flexShrink: 0 }}>2</span>
            <span style={{ fontSize: 12, fontWeight: 600 }}>Paste your API credentials</span>
          </div>
          <div style={{ fontSize: 11, color: 'var(--color-text-secondary)', marginBottom: 8 }}>
            Go to your{' '}
            <a href="https://dashboard.sendblue.co/api-credentials" target="_blank" rel="noopener noreferrer" style={{ color: 'var(--color-accent)', textDecoration: 'underline' }}>
              SendBlue API Credentials page
            </a>{' '}
            and copy the API Key and API Secret.
          </div>

          <div style={{ marginBottom: 8 }}>
            <label style={{ display: 'block', fontSize: 11, color: 'var(--color-text-secondary)', marginBottom: 3, fontWeight: 500 }}>
              API Key ID *
            </label>
            <input value={apiKey} onChange={(e) => setApiKey(e.target.value)} placeholder="Your API key ID" style={inputStyle} />
          </div>
          <div style={{ marginBottom: 12 }}>
            <label style={{ display: 'block', fontSize: 11, color: 'var(--color-text-secondary)', marginBottom: 3, fontWeight: 500 }}>
              API Secret Key *
            </label>
            <input value={apiSecret} onChange={(e) => setApiSecret(e.target.value)} placeholder="Your API secret key" type="password" style={inputStyle} />
          </div>

          {error && <div style={{ color: 'var(--color-error)', fontSize: 11, marginBottom: 8 }}>{error}</div>}

          <button
            onClick={handleVerify}
            disabled={!apiKey.trim() || !apiSecret.trim() || step === 'verifying'}
            style={{ ...btnPrimary, opacity: !apiKey.trim() || !apiSecret.trim() ? 0.5 : 1 }}
          >
            {step === 'verifying' ? 'Verifying...' : 'Verify & Find Number'}
          </button>
        </div>
      )}

      {/* Step 2: Number found â€” confirm + connect */}
      {(step === 'verified' || step === 'connecting') && (
        <div style={{ borderTop: '1px solid var(--color-border)', padding: 14, background: 'var(--color-bg)' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: 8, marginBottom: 10 }}>
            <span style={{ background: 'var(--color-success)', color: 'var(--color-on-accent)', borderRadius: '50%', width: 20, height: 20, display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: 11, fontWeight: 700, flexShrink: 0 }}>{'\u2713'}</span>
            <span style={{ fontSize: 12, fontWeight: 600, color: 'var(--color-success)' }}>Credentials verified</span>
          </div>

          <div style={{ display: 'flex', alignItems: 'center', gap: 8, marginBottom: 10 }}>
            <span style={{ background: 'var(--color-accent-purple)', color: 'var(--color-on-accent)', borderRadius: '50%', width: 20, height: 20, display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: 11, fontWeight: 700, flexShrink: 0 }}>3</span>
            <span style={{ fontSize: 12, fontWeight: 600 }}>Your agent's phone number</span>
          </div>

          {numbers.length > 1 ? (
            <div style={{ marginBottom: 12 }}>
              <label style={{ display: 'block', fontSize: 11, color: 'var(--color-text-secondary)', marginBottom: 3, fontWeight: 500 }}>
                Select a number for your agent
              </label>
              <select
                value={selectedNumber}
                onChange={(e) => setSelectedNumber(e.target.value)}
                style={{ ...inputStyle, padding: '8px 10px' }}
              >
                {numbers.map((n) => <option key={n} value={n}>{n}</option>)}
              </select>
            </div>
          ) : numbers.length === 1 ? (
            <div style={{
              background: 'var(--color-bg-secondary)', border: '1px solid color-mix(in srgb, var(--color-success) 22%, transparent)',
              borderRadius: 6, padding: '10px 12px', marginBottom: 12,
              display: 'flex', alignItems: 'center', gap: 8,
            }}>
              <span style={{ fontSize: 20 }}>{'\uD83D\uDCF1'}</span>
              <div>
                <div style={{ fontSize: 14, fontWeight: 700, color: 'var(--color-success)' }}>{selectedNumber}</div>
                <div style={{ fontSize: 11, color: 'var(--color-text-secondary)' }}>This will be your agent's phone number</div>
              </div>
            </div>
          ) : (
            <div style={{ marginBottom: 12 }}>
              <div style={{
                fontSize: 11, color: 'var(--color-text-secondary)',
                marginBottom: 8, lineHeight: 1.5,
                padding: '8px 10px', background: 'var(--color-bg-secondary)',
                borderRadius: 6, borderLeft: '3px solid var(--color-accent-purple)',
              }}>
                Copy the phone number shown under <strong>"Send from"</strong> in your SendBlue dashboard
                and paste it below. On the free tier this is a shared number.
              </div>
              <label style={{ display: 'block', fontSize: 11, color: 'var(--color-text-secondary)', marginBottom: 3, fontWeight: 500 }}>
                SendBlue phone number *
              </label>
              <input
                value={selectedNumber}
                onChange={(e) => setSelectedNumber(e.target.value)}
                placeholder="+16452468235"
                style={inputStyle}
              />
            </div>
          )}

          {error && <div style={{ color: 'var(--color-error)', fontSize: 11, marginBottom: 8 }}>{error}</div>}

          <button
            onClick={handleConnect}
            disabled={step === 'connecting' || !selectedNumber.trim()}
            style={{ ...btnPrimary, opacity: !selectedNumber.trim() ? 0.5 : 1 }}
          >
            {step === 'connecting' ? 'Connecting...' : 'Activate Phone Number'}
          </button>
        </div>
      )}

      {/* Step 3: Done â€” success + webhook setup */}
      {step === 'done' && (
        <SendBlueWebhookStep
          apiKey={apiKey}
          apiSecret={apiSecret}
          selectedNumber={selectedNumber}
        />
      )}
    </div>
  );
}

function MessagingTab({ agentId }: { agentId: string }) {
  const [bindings, setBindings] = useState<ChannelBinding[]>([]);
  const [setupType, setSetupType] = useState<string | null>(null);
  const [formValues, setFormValues] = useState<Record<string, string>>({});
  const [loading, setLoading] = useState(false);

  const loadBindings = useCallback(() => {
    fetchAgentChannels(agentId).then(setBindings).catch(() => setBindings([]));
  }, [agentId]);

  useEffect(() => { loadBindings(); }, [loadBindings]);

  const setField = (key: string, value: string) => {
    setFormValues((prev) => ({ ...prev, [key]: value }));
  };

  const handleSetup = async (ch: MessagingChannelConfig) => {
    // Check required fields
    const missing = ch.fields.filter(
      (f) => f.required && !formValues[f.key]?.trim(),
    );
    if (missing.length > 0) return;

    setLoading(true);
    try {
      const config: Record<string, string> = {};
      for (const f of ch.fields) {
        const v = formValues[f.key]?.trim();
        if (v) config[f.key] = v;
      }
      await bindAgentChannel(agentId, ch.type, config);
      setSetupType(null);
      setFormValues({});
      loadBindings();
    } catch { /* */ } finally { setLoading(false); }
  };

  const handleRemove = async (bindingId: string) => {
    try {
      await unbindAgentChannel(agentId, bindingId);
      loadBindings();
    } catch { /* */ }
  };

  const inputStyle: React.CSSProperties = {
    width: '100%', padding: '6px 10px',
    background: 'var(--color-bg-secondary)',
    border: '1px solid var(--color-border)',
    borderRadius: 4, color: 'var(--color-text)',
    fontSize: 12, boxSizing: 'border-box',
  };

  return (
    <div style={{ padding: 16 }}>
      <div style={{
        color: 'var(--color-text-secondary)',
        fontSize: 12, marginBottom: 14,
      }}>
        Connect a messaging channel so you can talk to your agent from your phone or other devices.
      </div>

      {/* SendBlue wizard â€” primary option */}
      <SendBlueWizard
        agentId={agentId}
        binding={bindings.find((b) => b.channel_type === 'sendblue')}
        onDone={loadBindings}
        onRemove={(id) => { unbindAgentChannel(agentId, id).then(loadBindings).catch(() => {}); }}
      />

      {/* Divider */}
      <div style={{
        fontSize: 10, color: 'var(--color-text-secondary)',
        textTransform: 'uppercase', letterSpacing: 1,
        margin: '14px 0 8px', fontWeight: 600,
      }}>
        Other messaging channels
      </div>

      {MESSAGING_CHANNELS.map((ch) => {
        const binding = bindings.find((b) => b.channel_type === ch.type);
        const cfg = (binding?.config || {}) as Record<string, unknown>;
        const isSetup = setupType === ch.type;

        // Check if required fields are filled
        const canConnect = ch.fields.every(
          (f) => !f.required || formValues[f.key]?.trim(),
        );

        return (
          <div
            key={ch.type}
            style={{
              background: 'var(--color-bg-secondary)',
              border: binding
                ? '1px solid color-mix(in srgb, var(--color-success) 22%, transparent)'
                : '1px dashed var(--color-border)',
              borderRadius: 8, marginBottom: 10,
              overflow: 'hidden',
            }}
          >
            {/* Header row */}
            <div style={{
              display: 'flex', alignItems: 'center',
              padding: '12px 14px',
            }}>
              <span style={{ fontSize: 18, marginRight: 10 }}>{ch.icon}</span>
              <div style={{ flex: 1 }}>
                <div style={{ fontWeight: 600, fontSize: 13 }}>{ch.name}</div>
                <div style={{
                  fontSize: 11,
                  color: binding ? 'var(--color-success)' : 'var(--color-text-secondary)',
                }}>
                  {binding ? ch.activeLabel(cfg) : ch.description}
                </div>
              </div>
              {binding ? (
                <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
                  <span style={{
                    background: 'color-mix(in srgb, var(--color-success) 22%, transparent)', color: 'var(--color-success)',
                    padding: '2px 8px', borderRadius: 10,
                    fontSize: 10, fontWeight: 600,
                  }}>Active</span>
                  <button
                    onClick={() => handleRemove(binding.id)}
                    style={{
                      fontSize: 10, padding: '2px 8px',
                      background: 'transparent',
                      color: 'var(--color-text-secondary)',
                      border: '1px solid var(--color-border)',
                      borderRadius: 4, cursor: 'pointer',
                    }}
                  >Remove</button>
                </div>
              ) : (
                <button
                  onClick={() => {
                    setSetupType(isSetup ? null : ch.type);
                    setFormValues({});
                  }}
                  style={{
                    fontSize: 10, padding: '3px 12px',
                    background: 'var(--color-accent-purple)', color: 'var(--color-on-accent)',
                    border: 'none', borderRadius: 5,
                    cursor: 'pointer', fontWeight: 600,
                  }}
                >
                  {isSetup ? 'Cancel' : 'Set Up'}
                </button>
              )}
            </div>

            {/* Active state: how to use */}
            {binding && (
              <div style={{
                borderTop: '1px solid var(--color-border)',
                padding: '10px 14px',
                background: 'var(--color-bg)',
              }}>
                <div style={{
                  fontSize: 11, color: 'var(--color-text-secondary)',
                  display: 'flex', alignItems: 'flex-start', gap: 6,
                }}>
                  <span style={{ flexShrink: 0 }}>{'\u2192'}</span>
                  <span>{ch.howToUse(cfg)}</span>
                </div>
              </div>
            )}

            {/* Setup form */}
            {isSetup && (
              <div style={{
                borderTop: '1px solid var(--color-border)',
                padding: '14px',
                background: 'var(--color-bg)',
              }}>
                {/* Setup instructions */}
                <div style={{
                  fontSize: 11, lineHeight: 1.5,
                  color: 'var(--color-text-secondary)',
                  marginBottom: 12,
                  padding: '8px 10px',
                  background: 'var(--color-bg-secondary)',
                  borderRadius: 6,
                  borderLeft: '3px solid var(--color-accent, var(--color-accent-purple))',
                }}>
                  {ch.setupSteps.map((step, i) => {
                    if (step.startsWith('COPYABLE:')) {
                      const text = step.slice(9);
                      return (
                        <div key={i} style={{ marginBottom: 6, marginTop: 4 }}>
                          <div style={{
                            position: 'relative',
                            background: 'var(--color-bg)',
                            border: '1px solid var(--color-border)',
                            borderRadius: 4, padding: '8px 10px',
                            fontSize: 10, fontFamily: 'monospace',
                            wordBreak: 'break-all', lineHeight: 1.4,
                            maxHeight: 80, overflowY: 'auto',
                          }}>
                            {text}
                            <button
                              onClick={() => { navigator.clipboard.writeText(text); }}
                              style={{
                                position: 'sticky', float: 'right', top: 0,
                                fontSize: 10, padding: '2px 8px',
                                background: 'var(--color-accent-purple)', color: 'var(--color-on-accent)',
                                border: 'none', borderRadius: 3,
                                cursor: 'pointer', fontWeight: 600,
                              }}
                            >Copy</button>
                          </div>
                        </div>
                      );
                    }
                    return (
                      <div key={i} style={{ marginBottom: i < ch.setupSteps.length - 1 ? 4 : 0 }}>
                        {step}
                      </div>
                    );
                  })}
                </div>

                {/* Form fields */}
                {ch.fields.map((field) => (
                  <div key={field.key} style={{ marginBottom: 8 }}>
                    <label style={{
                      display: 'block', fontSize: 11,
                      color: 'var(--color-text-secondary)',
                      marginBottom: 3, fontWeight: 500,
                    }}>
                      {field.label}{field.required ? ' *' : ''}
                    </label>
                    <input
                      type={field.type || 'text'}
                      value={formValues[field.key] || ''}
                      onChange={(e) => setField(field.key, e.target.value)}
                      placeholder={field.placeholder}
                      style={inputStyle}
                    />
                  </div>
                ))}

                {/* Connect button */}
                <button
                  onClick={() => handleSetup(ch)}
                  disabled={loading || !canConnect}
                  style={{
                    fontSize: 12, padding: '7px 20px',
                    background: 'var(--color-accent-purple)', color: 'var(--color-on-accent)',
                    border: 'none', borderRadius: 5,
                    cursor: 'pointer', fontWeight: 600,
                    opacity: loading || !canConnect ? 0.5 : 1,
                    marginTop: 4,
                  }}
                >
                  {loading ? 'Connecting...' : 'Connect'}
                </button>
              </div>
            )}
          </div>
        );
      })}
    </div>
  );
}

// ---------------------------------------------------------------------------
// Learning tab component
// ---------------------------------------------------------------------------

function LearningTab({ agentId, learningEnabled }: { agentId: string; learningEnabled: boolean }) {
  const [logs, setLogs] = useState<LearningLogEntry[]>([]);
  const [triggering, setTriggering] = useState(false);

  useEffect(() => {
    fetchLearningLog(agentId).then(setLogs).catch(() => {});
  }, [agentId]);

  async function handleTrigger() {
    setTriggering(true);
    try {
      await triggerLearning(agentId);
      // Refresh after a short delay
      setTimeout(() => fetchLearningLog(agentId).then(setLogs).catch(() => {}), 1000);
    } catch {
      // ignore
    } finally {
      setTriggering(false);
    }
  }

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2">
          <span className="text-sm font-medium" style={{ color: 'var(--color-text)' }}>Learning</span>
          <span
            className="text-xs px-2 py-0.5 rounded-full"
            style={{
              background: learningEnabled ? 'var(--color-success)20' : 'var(--color-bg-secondary)',
              color: learningEnabled ? 'var(--color-success)' : 'var(--color-text-tertiary)',
            }}
          >
            {learningEnabled ? 'Enabled' : 'Disabled'}
          </span>
        </div>
        <button
          onClick={handleTrigger}
          disabled={triggering}
          className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs cursor-pointer font-medium"
          style={{
            background: 'var(--color-accent)',
            color: 'var(--color-on-accent)',
            opacity: triggering ? 0.6 : 1,
          }}
        >
          <RefreshCw size={12} className={triggering ? 'animate-spin' : ''} />
          Run Learning
        </button>
      </div>
      {logs.length === 0 ? (
        <div className="text-sm text-center py-8" style={{ color: 'var(--color-text-tertiary)' }}>
          No learning events yet. Run the agent or trigger learning manually.
        </div>
      ) : (
        <div className="space-y-2">
          {logs.map((entry) => (
            <div
              key={entry.id}
              className="rounded-lg p-3 text-sm"
              style={{ background: 'var(--color-bg-secondary)', border: '1px solid var(--color-border)' }}
            >
              <div className="flex items-center justify-between mb-1">
                <span
                  className="text-xs px-2 py-0.5 rounded"
                  style={{ background: 'var(--color-accent)' + '20', color: 'var(--color-accent)' }}
                >
                  {entry.event_type}
                </span>
                <span className="text-xs" style={{ color: 'var(--color-text-tertiary)' }}>
                  {formatRelativeTime(entry.created_at)}
                </span>
              </div>
              {entry.description && (
                <p style={{ color: 'var(--color-text-secondary)' }}>{entry.description}</p>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

// ---------------------------------------------------------------------------
// Logs tab component
// ---------------------------------------------------------------------------

function LogsTab({ agentId }: { agentId: string }) {
  const [traces, setTraces] = useState<AgentTrace[]>([]);
  const [learningEntries, setLearningEntries] = useState<LearningLogEntry[]>([]);
  const [expandedTrace, setExpandedTrace] = useState<string | null>(null);

  const loadData = useCallback(async () => {
    try {
      const [t, l] = await Promise.all([
        fetchAgentTraces(agentId),
        fetchLearningLog(agentId),
      ]);
      setTraces(t);
      setLearningEntries(l);
    } catch {
      // ignore
    }
  }, [agentId]);

  useEffect(() => {
    loadData();
    // Fallback slow poll â€” WS is primary, this catches missed events
    const interval = setInterval(loadData, 30000);
    return () => clearInterval(interval);
  }, [loadData]);

  // Event-driven refresh â€” trace/learning entries are created by tick + tool events
  useAgentEvents(agentId, loadData, [
    'agent_tick_end',
    'agent_tick_error',
    'tool_call_end',
    'inference_end',
    'agent_learning_completed',
  ]);

  // Merge traces and learning entries into a unified timeline
  type TimelineEntry =
    | { kind: 'trace'; data: AgentTrace; ts: number }
    | { kind: 'learning'; data: LearningLogEntry; ts: number };

  const timeline: TimelineEntry[] = [
    ...traces.map((t): TimelineEntry => ({ kind: 'trace', data: t, ts: t.started_at })),
    ...learningEntries.map((e): TimelineEntry => ({ kind: 'learning', data: e, ts: e.created_at })),
  ].sort((a, b) => b.ts - a.ts);

  const learningEventColor = (eventType: string) => {
    if (eventType === 'query_start') return 'var(--color-accent)';
    if (eventType === 'query_complete') return 'var(--color-success)';
    if (eventType === 'tool_call') return 'var(--color-warning)';
    if (eventType === 'tool_result') return 'var(--color-accent-purple)';
    if (eventType === 'query_error') return 'var(--color-error)';
    return 'var(--color-text-secondary)';
  };

  const learningEventLabel = (eventType: string) => {
    if (eventType === 'query_start') return 'Query';
    if (eventType === 'query_complete') return 'Complete';
    if (eventType === 'tool_call') return 'Tool Call';
    if (eventType === 'tool_result') return 'Tool Result';
    if (eventType === 'query_error') return 'Error';
    return eventType;
  };

  return (
    <div className="space-y-3">
      <div className="flex items-center justify-between">
        <span className="text-sm font-medium" style={{ color: 'var(--color-text)' }}>
          Activity Log
        </span>
        <span className="text-xs" style={{ color: 'var(--color-text-tertiary)' }}>
          {timeline.length} entr{timeline.length !== 1 ? 'ies' : 'y'} (auto-refreshing)
        </span>
      </div>
      {timeline.length === 0 ? (
        <div className="text-sm text-center py-8" style={{ color: 'var(--color-text-tertiary)' }}>
          No activity yet. Send a message or run the agent to generate logs.
        </div>
      ) : (
        <div className="space-y-2">
          {timeline.map((entry) => {
            if (entry.kind === 'learning') {
              const e = entry.data;
              return (
                <div
                  key={`learn-${e.id}`}
                  className="rounded-lg p-3 text-sm"
                  style={{ background: 'var(--color-bg-secondary)', border: '1px solid var(--color-border)' }}
                >
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-2">
                      <span
                        className="w-2 h-2 rounded-full inline-block"
                        style={{ background: learningEventColor(e.event_type) }}
                      />
                      <span
                        className="text-[10px] px-1.5 py-0.5 rounded font-medium"
                        style={{
                          background: `${learningEventColor(e.event_type)}20`,
                          color: learningEventColor(e.event_type),
                        }}
                      >
                        {learningEventLabel(e.event_type)}
                      </span>
                    </div>
                    <span className="text-xs" style={{ color: 'var(--color-text-tertiary)' }}>
                      {formatRelativeTime(e.created_at)}
                    </span>
                  </div>
                  <div className="mt-1 text-xs" style={{ color: 'var(--color-text-secondary)' }}>
                    {e.description}
                  </div>
                </div>
              );
            }

            // Trace entry
            const t = entry.data;
            const errorDetail = t.metadata?.error_detail as
              | { error_type: string; error_message: string; suggested_action: string }
              | undefined;
            const isError = t.outcome !== 'success';
            const isExpanded = expandedTrace === t.id;

            return (
              <div
                key={`trace-${t.id}`}
                className="rounded-lg p-3 text-sm cursor-pointer"
                style={{ background: 'var(--color-bg-secondary)', border: '1px solid var(--color-border)' }}
                onClick={() => isError && errorDetail && setExpandedTrace(isExpanded ? null : t.id)}
              >
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    <span
                      className="w-2 h-2 rounded-full inline-block"
                      style={{ background: t.outcome === 'success' ? 'var(--color-success)' : 'var(--color-error)' }}
                    />
                    <span style={{ color: 'var(--color-text)' }}>{t.outcome}</span>
                    <span
                      className="text-[10px] px-1.5 py-0.5 rounded font-medium"
                      style={{ background: 'var(--color-bg)', color: 'var(--color-text-secondary)' }}
                    >
                      Trace
                    </span>
                    {errorDetail && (
                      <span
                        className="text-[10px] px-1.5 py-0.5 rounded font-medium"
                        style={{
                          background: errorDetail.error_type === 'fatal' ? 'var(--color-error)20' :
                            errorDetail.error_type === 'escalate' ? 'var(--color-warning)20' : 'var(--color-accent)20',
                          color: errorDetail.error_type === 'fatal' ? 'var(--color-error)' :
                            errorDetail.error_type === 'escalate' ? 'var(--color-warning)' : 'var(--color-accent)',
                        }}
                      >
                        {errorDetail.error_type}
                      </span>
                    )}
                  </div>
                  <span className="text-xs" style={{ color: 'var(--color-text-tertiary)' }}>
                    {formatRelativeTime(t.started_at)}
                  </span>
                </div>
                <div className="flex items-center gap-3 mt-1 text-xs" style={{ color: 'var(--color-text-tertiary)' }}>
                  <span>{t.duration.toFixed(1)}s</span>
                  <span>{t.steps} step{t.steps !== 1 ? 's' : ''}</span>
                </div>
                {isExpanded && errorDetail && (
                  <div className="mt-2 pt-2 space-y-1.5 text-xs" style={{ borderTop: '1px solid var(--color-border)' }}>
                    <div>
                      <span className="font-medium" style={{ color: 'var(--color-text-secondary)' }}>Error: </span>
                      <span style={{ color: 'var(--color-text)' }}>{errorDetail.error_message}</span>
                    </div>
                    <div>
                      <span className="font-medium" style={{ color: 'var(--color-text-secondary)' }}>Action: </span>
                      <span style={{ color: 'var(--color-text)' }}>{errorDetail.suggested_action}</span>
                    </div>
                  </div>
                )}
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}

// ---------------------------------------------------------------------------
// Main page component
// ---------------------------------------------------------------------------

export function AgentsPage() {
  const managedAgents = useAppStore((s) => s.managedAgents);
  const setManagedAgents = useAppStore((s) => s.setManagedAgents);
  const selectedAgentId = useAppStore((s) => s.selectedAgentId);
  const setSelectedAgentId = useAppStore((s) => s.setSelectedAgentId);
  const savings = useAppStore((s) => s.savings);
  const [loading, setLoading] = useState(true);
  const [agentManagerAvailable, setAgentManagerAvailable] = useState<boolean | null>(null);
  const [tasks, setTasks] = useState<AgentTask[]>([]);
  const [channels, setChannels] = useState<ChannelBinding[]>([]);
  const [templates, setTemplates] = useState<AgentTemplate[]>([]);
  const [showWizard, setShowWizard] = useState(false);
  const [detailTab, setDetailTab] = useState<'overview' | 'interact' | 'channels' | 'messaging' | 'tasks' | 'memory' | 'learning' | 'logs'>('interact');

  const refresh = useCallback(async () => {
    try {
      const agents = await fetchManagedAgents();
      setManagedAgents(agents);
      setAgentManagerAvailable(true);
    } catch (err: any) {
      if (err.message?.includes('404')) {
        setAgentManagerAvailable(false);
      }
      setManagedAgents([]);
    } finally {
      setLoading(false);
    }
  }, [setManagedAgents]);

  useEffect(() => {
    refresh();
    fetchTemplates().then(setTemplates).catch(() => {});
  }, [refresh]);

  const selectedAgent = managedAgents.find((a) => a.id === selectedAgentId);

  useEffect(() => {
    if (selectedAgentId) {
      fetchAgentTasks(selectedAgentId).then(setTasks).catch(() => setTasks([]));
      fetchAgentChannels(selectedAgentId).then(setChannels).catch(() => setChannels([]));
    }
  }, [selectedAgentId]);

  const handlePause = async (id: string) => {
    await pauseManagedAgent(id).catch(() => {});
    await refresh();
  };

  const handleResume = async (id: string) => {
    await resumeManagedAgent(id).catch(() => {});
    await refresh();
  };

  const handleDelete = async (id: string) => {
    await deleteManagedAgent(id).catch(() => {});
    if (selectedAgentId === id) setSelectedAgentId(null);
    await refresh();
  };

  const handleRun = async (id: string) => {
    try {
      await runManagedAgent(id);
    } catch (err: any) {
      toast.error('Failed to start agent', {
        description: err.message || 'Unknown error',
      });
      await refresh();
      return;
    }
    await refresh();
    setTimeout(async () => {
      try {
        const agent = await fetchManagedAgent(id);
        if (agent.status === 'error') {
          toast.error(`Agent "${agent.name}" failed`, {
            description: agent.summary_memory?.replace(/^ERROR: /, '') || 'Unknown error',
          });
          useAppStore.getState().addLogEntry({
            timestamp: Date.now(), level: 'error', category: 'model',
            message: `Agent "${agent.name}" failed: ${agent.summary_memory || 'Unknown error'}`,
          });
        }
      } catch {}
      await refresh();
    }, 3000);
  };

  const handleRecover = async (id: string) => {
    try {
      const result = await recoverManagedAgent(id);
      if (result.checkpoint) {
        toast.success('Agent recovered from checkpoint');
      } else {
        toast.success('Agent reset to idle (no checkpoint available)');
      }
      setDetailTab('overview');
    } catch (err: any) {
      toast.error('Recovery failed', {
        description: err.message || 'Unknown error',
      });
    }
    await refresh();
  };

  const prevStatuses = useRef<Record<string, string>>({});
  useEffect(() => {
    const interval = setInterval(async () => {
      try {
        const agents = await fetchManagedAgents();
        for (const agent of agents) {
          const prev = prevStatuses.current[agent.id];
          if (prev && prev !== 'error' && agent.status === 'error') {
            toast.error(`Agent "${agent.name}" failed`, {
              description: agent.summary_memory?.replace(/^ERROR: /, '') || 'Unknown error',
            });
          }
          prevStatuses.current[agent.id] = agent.status;
        }
        // Keep the agent list â€” and the derived selectedAgent status badge â€”
        // live. This poll previously fetched statuses only to fire error
        // toasts and threw the result away, so a detail header could stay
        // stuck on "running" after a tick finished on the backend.
        setManagedAgents(agents);
      } catch {}
    }, 5000);
    return () => clearInterval(interval);
  }, [setManagedAgents]);

  if (loading) {
    return (
      <div className="flex-1 flex items-center justify-center" style={{ color: 'var(--color-text-tertiary)' }}>
        Loading agents...
      </div>
    );
  }

  // â”€â”€ Detail View â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

  if (selectedAgent) {
    const successRate =
      tasks.length > 0
        ? Math.round((tasks.filter((t) => t.status === 'completed').length / tasks.length) * 100)
        : null;

    const DETAIL_TABS = [
      { id: 'interact', label: 'Interact', icon: MessageSquare },
      { id: 'overview', label: 'Overview', icon: Activity },
      { id: 'channels', label: 'Data Sources', icon: Database },
      { id: 'messaging', label: 'Messaging Channels', icon: Wifi },
      { id: 'tasks', label: 'Tasks', icon: ListTodo },
      { id: 'memory', label: 'Memory', icon: Brain },
      { id: 'learning', label: 'Learning', icon: Settings },
      { id: 'logs', label: 'Logs', icon: FileText },
    ] as const;

    return (
      <div className="flex-1 overflow-y-auto px-6 py-10">
        <div className="max-w-5xl mx-auto">
        {/* Back button */}
        <button
          onClick={() => setSelectedAgentId(null)}
          className="flex items-center gap-1 mb-4 text-sm cursor-pointer"
          style={{ color: 'var(--color-text-secondary)' }}
        >
          <ChevronLeft size={16} /> Back to agents
        </button>

        {/* Header */}
        <div className="flex items-start justify-between mb-6">
          <div className="flex items-center gap-3">
            <Bot size={24} style={{ color: 'var(--color-accent)' }} />
            <div>
              <h1 className="text-xl font-semibold" style={{ color: 'var(--color-text)' }}>
                {selectedAgent.name}
              </h1>
              <div className="flex items-center gap-2 mt-1">
                <StatusBadge status={selectedAgent.status} />
                <span className="text-xs" style={{ color: 'var(--color-text-tertiary)' }}>
                  {selectedAgent.agent_type}
                </span>
              </div>
            </div>
          </div>
          {/* Header actions */}
          <div className="flex items-center gap-2">
            {detailTab === 'interact' ? (
              <span
                className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs"
                style={{ background: 'var(--color-success)20', color: 'var(--color-success)', border: '1px solid var(--color-success)40' }}
              >
                <MessageSquare size={13} /> Chat ready â€” just type below
              </span>
            ) : (
              <button
                onClick={() => handleRun(selectedAgent.id)}
                className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-sm cursor-pointer font-medium"
                style={{ background: 'var(--color-accent)', color: 'var(--color-on-accent)' }}
              >
                <Zap size={13} /> Run Now
              </button>
            )}
            {(selectedAgent.status === 'running' || selectedAgent.status === 'idle') && (
              <button
                onClick={() => handlePause(selectedAgent.id)}
                className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-sm cursor-pointer"
                style={{ background: 'var(--color-bg-secondary)', border: '1px solid var(--color-border)', color: 'var(--color-text)' }}
              >
                <Pause size={13} /> Pause
              </button>
            )}
            {selectedAgent.status === 'paused' && (
              <button
                onClick={() => handleResume(selectedAgent.id)}
                className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-sm cursor-pointer"
                style={{ background: 'var(--color-success)20', color: 'var(--color-success)', border: '1px solid var(--color-success)40' }}
              >
                <Play size={13} /> Resume
              </button>
            )}
            {(selectedAgent.status === 'error' || selectedAgent.status === 'stalled' || selectedAgent.status === 'needs_attention') && (
              <button
                onClick={() => handleRecover(selectedAgent.id)}
                className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-sm cursor-pointer"
                style={{ background: 'var(--color-error)20', color: 'var(--color-error)', border: '1px solid var(--color-error)40' }}
              >
                <AlertTriangle size={13} /> Recover
              </button>
            )}
            <button
              onClick={async () => {
                if (window.confirm(`Delete ${selectedAgent.name}? This cannot be undone.`)) {
                  await deleteManagedAgent(selectedAgent.id);
                  setSelectedAgentId(null);
                  await refresh();
                }
              }}
              className="p-1.5 rounded-lg cursor-pointer transition-colors"
              style={{ color: 'var(--color-error)', background: 'var(--color-error)15' }}
              title="Delete agent"
            >
              <Trash2 size={15} />
            </button>
          </div>
        </div>

        {/* Tabs */}
        <div className="flex gap-1 mb-6 p-1 rounded-lg overflow-x-auto" style={{ background: 'var(--color-bg-secondary)' }}>
          {DETAIL_TABS.map(({ id, label, icon: Icon }) => (
            <button
              key={id}
              onClick={() => setDetailTab(id)}
              className="px-3 py-2 rounded-md text-xs flex items-center gap-1.5 whitespace-nowrap cursor-pointer transition-colors"
              style={{
                background: detailTab === id ? 'var(--color-bg)' : 'transparent',
                color: detailTab === id ? 'var(--color-text)' : 'var(--color-text-secondary)',
                fontWeight: detailTab === id ? 500 : 400,
              }}
            >
              <Icon size={13} />
              {label}
            </button>
          ))}
        </div>

        {/* Tab: Overview */}
        {detailTab === 'overview' && (
          <div className="space-y-3">
            {/* Instruction */}
            <AgentInstructionSection agent={selectedAgent} onAgentUpdated={refresh} />

            {/* Configuration */}
            <div
              className="p-3 rounded-lg"
              style={{ background: 'var(--color-bg-secondary)', border: '1px solid var(--color-border)' }}
            >
              <h3 className="text-sm font-semibold mb-2" style={{ color: 'var(--color-text)' }}>
                Configuration
              </h3>
              <AgentConfigGrid agent={selectedAgent} onAgentUpdated={refresh} />
              <div className="mt-2 pt-2" style={{ borderTop: '1px solid var(--color-border)' }}>
                <span className="text-xs font-mono" style={{ color: 'var(--color-text-tertiary)' }}>
                  ID: {selectedAgent.id}
                </span>
              </div>
            </div>

            {/* Hint for deep research agents */}
            {selectedAgent.agent_type === 'deep_research' && (
              <div
                className="flex items-start gap-3 p-3 rounded-lg text-sm"
                style={{
                  background: 'var(--color-accent-subtle)',
                  border: '1px solid var(--color-border)',
                }}
              >
                <Database size={16} style={{ color: 'var(--color-accent)', flexShrink: 0, marginTop: 2 }} />
                <div style={{ color: 'var(--color-text-secondary)' }}>
                  <strong>Tip:</strong> Connect your personal data in the{' '}
                  <button
                    onClick={() => setDetailTab('channels')}
                    className="cursor-pointer underline"
                    style={{ color: 'var(--color-accent)', background: 'none', border: 'none', padding: 0, font: 'inherit' }}
                  >Data Sources</button>{' '}
                  tab, then set up{' '}
                  <button
                    onClick={() => setDetailTab('messaging')}
                    className="cursor-pointer underline"
                    style={{ color: 'var(--color-accent)', background: 'none', border: 'none', padding: 0, font: 'inherit' }}
                  >Messaging Channels</button>{' '}
                  to talk to this agent from your phone.
                </div>
              </div>
            )}

            {/* Usage stats + savings â€” single compact row */}
            {(() => {
              const inTok = selectedAgent.input_tokens ?? 0;
              const outTok = selectedAgent.output_tokens ?? 0;
              const modelName = (selectedAgent.config?.model as string) || '';
              const paramMatch = modelName.match(/:(\d+(?:\.\d+)?)b/i);
              const paramsB = paramMatch ? parseFloat(paramMatch[1]) : 9;
              const flops = 2 * paramsB * 1e9 * (inTok + outTok);
              const providers = [
                { label: 'GPT-5.6 Sol', inPer1M: 5.0, outPer1M: 30.0 },
                { label: 'Claude Fable 5', inPer1M: 10.0, outPer1M: 50.0 },
                { label: 'Gemini 3.1 Pro', inPer1M: 2.0, outPer1M: 12.0 },
              ];
              const energyWh = (inTok + outTok) / 1000 * 0.4;
              const energyKj = energyWh * 3.6;
              const fmtFlops = flops >= 1e15 ? `${(flops / 1e15).toFixed(1)} PFLOPs` : `${(flops / 1e12).toFixed(1)} TFLOPs`;
              const hasSavings = inTok + outTok > 0;
              const sectionTitle = { fontSize: 11, fontWeight: 600, color: 'var(--color-text-tertiary)', textTransform: 'uppercase' as const, letterSpacing: '0.05em', marginBottom: 8 };
              return (
                <div className="p-4 rounded-xl" style={{ background: 'var(--color-bg-secondary)', border: '1px solid var(--color-border)' }}>
                  <div className="flex gap-0 flex-wrap items-stretch">
                    {/* Agent Statistics */}
                    <div className="pr-5">
                      <p style={sectionTitle}>Agent Statistics</p>
                      <div className="flex gap-5">
                        <div>
                          <p className="text-xl font-bold leading-none" style={{ color: 'var(--color-text)' }}>{selectedAgent.total_runs ?? 0}</p>
                          <p className="text-xs mt-1" style={{ color: 'var(--color-text-tertiary)' }}>Total Queries</p>
                        </div>
                        <div>
                          <p className="text-xl font-bold leading-none" style={{ color: 'var(--color-text)' }}>{inTok.toLocaleString()}</p>
                          <p className="text-xs mt-1" style={{ color: 'var(--color-text-tertiary)' }}>Input Tokens</p>
                        </div>
                        <div>
                          <p className="text-xl font-bold leading-none" style={{ color: 'var(--color-text)' }}>{outTok.toLocaleString()}</p>
                          <p className="text-xs mt-1" style={{ color: 'var(--color-text-tertiary)' }}>Output Tokens</p>
                        </div>
                      </div>
                    </div>
                    {hasSavings && (<>
                      <div style={{ width: 1, background: 'var(--color-border)' }} />
                      {/* Local Utilization */}
                      <div className="px-5">
                        <p style={sectionTitle}>Local Utilization</p>
                        <div className="flex gap-5">
                          <div>
                            <p className="text-xl font-bold leading-none" style={{ color: 'var(--color-success)' }}>{fmtFlops}</p>
                            <p className="text-xs mt-1" style={{ color: 'var(--color-text-tertiary)' }}>Compute</p>
                          </div>
                          <div>
                            <p className="text-xl font-bold leading-none" style={{ color: 'var(--color-success)' }}>{energyKj.toFixed(2)} kJ</p>
                            <p className="text-xs mt-1" style={{ color: 'var(--color-text-tertiary)' }}>Energy</p>
                          </div>
                        </div>
                      </div>
                      <div style={{ width: 1, background: 'var(--color-border)' }} />
                      {/* Dollars Saved */}
                      <div className="pl-5">
                        <p style={sectionTitle}>Dollars Saved vs.</p>
                        <div className="flex gap-5">
                          {providers.map((p) => {
                            const cost = (inTok / 1e6) * p.inPer1M + (outTok / 1e6) * p.outPer1M;
                            return (
                              <div key={p.label}>
                                <p className="text-xl font-bold leading-none" style={{ color: 'var(--color-success)' }}>${cost.toFixed(4)}</p>
                                <p className="text-xs mt-1" style={{ color: 'var(--color-text-tertiary)' }}>{p.label}</p>
                              </div>
                            );
                          })}
                        </div>
                      </div>
                    </>)}
                  </div>
                </div>);
            })()}

            {/* Channels summary */}
            {channels.length > 0 && (
              <div
                className="p-4 rounded-lg"
                style={{ background: 'var(--color-bg-secondary)', border: '1px solid var(--color-border)' }}
              >
                <h3 className="text-sm font-medium mb-2" style={{ color: 'var(--color-text-secondary)' }}>
                  Messaging Channels
                </h3>
                {channels.map((b) => (
                  <div key={b.id} className="text-sm py-1" style={{ color: 'var(--color-text)' }}>
                    {b.channel_type}: {b.routing_mode}
                  </div>
                ))}
              </div>
            )}
          </div>
        )}

        {/* Tab: Interact */}
        {detailTab === 'interact' && <InteractTab agentId={selectedAgent.id} agentStatus={selectedAgent.status} onRunStateChange={refresh} />}

        {/* Tab: Channels */}
        {detailTab === 'channels' && (
          <ChannelsTab agentId={selectedAgent.id} />
        )}

        {/* Tab: Messaging */}
        {detailTab === 'messaging' && (
          <MessagingTab agentId={selectedAgent.id} />
        )}

        {/* Tab: Tasks */}
        {detailTab === 'tasks' && (
          <div className="space-y-2">
            {tasks.map((t) => (
              <div
                key={t.id}
                className="p-3 rounded-lg"
                style={{ background: 'var(--color-bg-secondary)', border: '1px solid var(--color-border)' }}
              >
                <div className="flex justify-between items-start gap-3">
                  <span className="text-sm" style={{ color: 'var(--color-text)' }}>
                    {t.description}
                  </span>
                  <span
                    className="text-xs px-2 py-0.5 rounded flex-shrink-0"
                    style={{
                      background: statusColor(t.status) + '20',
                      color: statusColor(t.status),
                    }}
                  >
                    {t.status}
                  </span>
                </div>
              </div>
            ))}
            {tasks.length === 0 && (
              <div className="text-sm py-8 text-center" style={{ color: 'var(--color-text-tertiary)' }}>
                No tasks assigned.
              </div>
            )}
          </div>
        )}

        {/* Tab: Memory */}
        {detailTab === 'memory' && (
          <div
            className="p-4 rounded-lg"
            style={{ background: 'var(--color-bg-secondary)', border: '1px solid var(--color-border)' }}
          >
            <h3 className="text-sm font-medium mb-3 flex items-center gap-2" style={{ color: 'var(--color-text-secondary)' }}>
              <Brain size={14} /> Summary Memory
            </h3>
            <p className="whitespace-pre-wrap text-sm" style={{ color: 'var(--color-text)' }}>
              {selectedAgent.summary_memory || 'Agent has no stored memory yet.'}
            </p>
          </div>
        )}

        {/* Tab: Learning */}
        {detailTab === 'learning' && (
          <LearningTab agentId={selectedAgent.id} learningEnabled={!!selectedAgent.learning_enabled} />
        )}

        {/* Tab: Logs */}
        {detailTab === 'logs' && (
          <LogsTab agentId={selectedAgent.id} />
        )}
        </div>
      </div>
    );
  }

  // â”€â”€ List View â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

  return (
    <div className="flex-1 overflow-y-auto px-6 py-10">
      <div className="max-w-5xl mx-auto">
      {/* Launch wizard modal */}
      {showWizard && (
        <LaunchWizard
          templates={templates}
          onClose={() => setShowWizard(false)}
          onLaunched={() => {
            setShowWizard(false);
            refresh();
          }}
        />
      )}

      <header className="mb-6">
        <div className="flex justify-between items-center">
          <h1 className="text-lg font-semibold" style={{ color: 'var(--color-text)' }}>
            Agents
          </h1>
          <button
            onClick={() => agentManagerAvailable && setShowWizard(true)}
            disabled={agentManagerAvailable === false}
            className="flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-medium cursor-pointer transition-colors disabled:opacity-40 disabled:cursor-not-allowed"
            style={{
              background: agentManagerAvailable === false ? 'var(--color-bg-tertiary)' : 'var(--color-accent)',
              color: agentManagerAvailable === false ? 'var(--color-text-tertiary)' : 'var(--color-on-accent)',
            }}
          >
            <Plus size={15} /> New Agent
          </button>
        </div>
        <p className="text-sm mt-2 max-w-2xl" style={{ color: 'var(--color-text-secondary)' }}>
          Long-running autonomous agents that can monitor sources, run tasks on a schedule, and message you through connected channels.
        </p>
      </header>

      {agentManagerAvailable === false && (
        <div
          className="mx-4 mt-2 px-4 py-3 rounded-lg flex items-center gap-3 text-sm"
          style={{
            background: 'var(--color-accent-amber-subtle)',
            border: '1px solid color-mix(in srgb, var(--color-warning) 20%, transparent)',
            color: 'var(--color-accent-amber)',
          }}
        >
          <AlertTriangle size={16} />
          <span>Agent manager is not enabled. Set <code className="font-mono text-xs">agent_manager.enabled = true</code> in your config.</span>
        </div>
      )}

      {/* Agent cards grid */}
      <div className="grid gap-3" style={{ gridTemplateColumns: 'repeat(auto-fill, minmax(300px, 1fr))' }}>
        {managedAgents.map((a) => (
          <AgentCard
            key={a.id}
            agent={a}
            onClick={() => {
              setSelectedAgentId(a.id);
              setDetailTab('overview');
            }}
            onPause={handlePause}
            onResume={handleResume}
            onRun={handleRun}
            onRecover={handleRecover}
            onDelete={handleDelete}
            onChat={(id) => {
              setSelectedAgentId(id);
              setDetailTab('interact');
            }}
            onEdit={(id) => {
              setSelectedAgentId(id);
              setDetailTab('overview');
            }}
          />
        ))}
      </div>

      {managedAgents.length === 0 && (
        <div className="text-center py-16" style={{ color: 'var(--color-text-tertiary)' }}>
          <Bot size={48} className="mx-auto mb-4 opacity-30" />
          <p className="mb-2 font-medium" style={{ color: 'var(--color-text-secondary)' }}>
            No agents yet
          </p>
          <p className="text-sm mb-6">Create your first agent to get started with autonomous task management.</p>
          <button
            onClick={() => agentManagerAvailable && setShowWizard(true)}
            disabled={agentManagerAvailable === false}
            className="inline-flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-medium cursor-pointer disabled:opacity-40 disabled:cursor-not-allowed"
            style={{
              background: agentManagerAvailable === false ? 'var(--color-bg-tertiary)' : 'var(--color-accent)',
              color: agentManagerAvailable === false ? 'var(--color-text-tertiary)' : 'var(--color-on-accent)',
            }}
          >
            <Plus size={15} /> Launch your first agent
          </button>
        </div>
      )}
      </div>
    </div>
  );
}


## ===== frontend/src/pages/DataSourcesPage.tsx : OUR COMMITS SINCE AUTHOR BASE =====
0389255b TTS: AudioContext playback engine + ChatArea driver rewrite; mailbox IMAP connector and tools; speech/CSP fixes
bc498a16 feat: Arc Reactor ThinkingCircle, fix env loading, fix project root, add research types, remove debug code

## ===== frontend/src/pages/DataSourcesPage.tsx : CONFLICTED WORKING FILE (diff3) =====
import { useEffect, useState, useCallback, useRef } from 'react';
import { motion } from 'motion/react';
import { useAppStore } from '../lib/store';
import {
  fetchManagedAgents,
  fetchAgentChannels,
  bindAgentChannel,
  unbindAgentChannel,
  createManagedAgent,
  sendblueRegisterWebhook,
  sendblueHealth,
  getMemoryStats,
  searchMemory,
  storeMemory,
  indexMemoryPath,
} from '../lib/api';
import type { ChannelBinding, ManagedAgent, MemoryStats, MemorySearchResult } from '../lib/api';
import { getBase, isTauri } from '../lib/api';
import {
  Database, MessageSquare, Loader2, Brain, Search, FolderOpen, FileText,
  Mail, Hash, MessageCircle, CalendarDays, Contact, StickyNote, BookText,
  Package, Upload, Link2, PhoneCall,
} from 'lucide-react';
import type { LucideIcon } from 'lucide-react';
import { SOURCE_CATALOG } from '../types/connectors';
<<<<<<< ours
import type { ConnectRequest } from '../types/connectors';
import { listConnectors, connectSource, getSyncStatus, triggerSync } from '../lib/connectors-api';
import type { SyncStatus } from '../types/connectors';
||||||| base
import type { ConnectRequest } from '../types/connectors';
import { listConnectors, connectSource, disconnectSource, getSyncStatus, triggerSync } from '../lib/connectors-api';
import type { SyncStatus } from '../types/connectors';
=======
import type { ConnectRequest, ConnectorMeta, SyncStatus, OAuthSetupInfo } from '../types/connectors';
import { listConnectors, connectSource, disconnectSourceUntilComplete, getConnector, getSyncStatus, triggerSync, startServerOAuth } from '../lib/connectors-api';
>>>>>>> theirs

// ---------------------------------------------------------------------------
// Inline connect form (reused from AgentsPage pattern)
// ---------------------------------------------------------------------------

function InlineConnectForm({
  fields,
  loading,
  disabled = false,
  onSubmit,
}: {
  fields: NonNullable<ConnectorMeta['inputFields']>;
  loading: boolean;
  disabled?: boolean;
  onSubmit: (req: ConnectRequest) => void;
}) {
  const [inputs, setInputs] = useState<Record<string, string>>(() =>
    Object.fromEntries(fields.map((field) => [field.name, field.defaultValue || ''])),
  );

  const update = (name: string, value: string) =>
    setInputs((p) => ({ ...p, [name]: value }));

  const allFilled = fields
    .filter((field) => field.required !== false)
    .every((field) => inputs[field.name]?.trim());
  const submitDisabled = loading || disabled || !allFilled;

  const submit = () => {
    const req: ConnectRequest = {};
    for (const f of fields) {
      if (f.name === 'email') req.email = inputs.email;
      else if (f.name === 'password') req.password = inputs.password;
      else if (f.name === 'token') req.token = inputs.token;
      else if (f.name === 'path') req.path = inputs.path;
      else if (f.name === 'host' && inputs.host?.trim()) req.host = inputs.host.trim();
      else if (f.name === 'port' && inputs.port?.trim()) req.port = Number(inputs.port);
      else if (f.name === 'security' && (inputs.security === 'tls' || inputs.security === 'starttls')) {
        req.security = inputs.security;
      }
      else req.config = { ...(req.config || {}), [f.name]: inputs[f.name] };
    }
    if (req.email && req.password) {
      req.token = `${req.email}:${req.password}`;
      req.code = req.token;
    }
    if (req.token && !req.code) req.code = req.token;
    onSubmit(req);
  };

  return (
    <div>
      {fields.map((f) => (
        f.type === 'select' ? (
          <select
            key={f.name}
            value={inputs[f.name] || f.defaultValue || ''}
            onChange={(e) => update(f.name, e.target.value)}
            aria-label={f.placeholder}
            style={{
              width: '100%', padding: '7px 10px',
              background: 'var(--color-bg)',
              border: '1px solid var(--color-border)',
              borderRadius: 4, color: 'var(--color-text)',
              fontSize: 12, marginBottom: 6,
              boxSizing: 'border-box',
            }}
          >
            {(f.options || []).map((option) => (
              <option key={option.value} value={option.value}>{option.label}</option>
            ))}
          </select>
        ) : (
          <input
            key={f.name}
            value={inputs[f.name] || ''}
            onChange={(e) => update(f.name, e.target.value)}
            placeholder={f.placeholder}
            type={f.type || 'text'}
            required={f.required !== false}
            style={{
              width: '100%', padding: '7px 10px',
              background: 'var(--color-bg)',
              border: '1px solid var(--color-border)',
              borderRadius: 4, color: 'var(--color-text)',
              fontSize: 12, marginBottom: 6,
              boxSizing: 'border-box',
            }}
          />
        )
      ))}
      <button
        onClick={submit}
        disabled={submitDisabled}
        style={{
          width: '100%', padding: 8,
          background: submitDisabled ? 'var(--color-disabled-bg)' : 'var(--color-accent-purple)',
          color: 'var(--color-on-accent)', border: 'none',
          borderRadius: 6, fontSize: 12,
          cursor: submitDisabled ? 'default' : 'pointer',
        }}
      >
        Connect
      </button>
    </div>
  );
}

// ---------------------------------------------------------------------------
// Generic fallback connect panel â€” for any backend connector that has no
// hardcoded SOURCE_CATALOG entry (no `steps`). Without this, expanding such
// a connector's "+ Add" card rendered nothing at all: no button, no input,
// no explanation, just an empty box (e.g. Spotify, Strava, Oura, GitHub
// Notifications, Google Tasks, Weather, and the Apple/News local sources).
// Branches on auth_type using the same primitives the hardcoded catalog
// entries already use (InlineConnectForm, oauth start+poll).
// ---------------------------------------------------------------------------

function GenericConnectPanel({
  connectorId,
  displayName,
  authType,
  loading,
  disabled = false,
  onConnect,
  onOAuthStart,
}: {
  connectorId: string;
  displayName: string;
  authType: string;
  loading: boolean;
  disabled?: boolean;
  onConnect: (req: ConnectRequest) => void;
  onOAuthStart: () => void;
}) {
  const [oauthSetup, setOauthSetup] = useState<OAuthSetupInfo | null>(null);
  const [feedUrls, setFeedUrls] = useState('');

  useEffect(() => {
    if (authType !== 'oauth') return;
    let cancelled = false;
    getConnector(connectorId)
      .then((info) => {
        if (!cancelled) setOauthSetup(info.oauth_setup ?? null);
      })
      .catch(() => {});
    return () => {
      cancelled = true;
    };
  }, [connectorId, authType]);

  if (authType === 'local') {
    if (connectorId === 'news_rss') {
      const feeds = feedUrls
        .split('\n')
        .map((url) => url.trim())
        .filter(Boolean)
        .map((url) => ({ url }));
      return (
        <div>
          <div style={{ fontSize: 12, color: 'var(--color-text-secondary)', marginBottom: 10 }}>
            Add one RSS or Atom feed URL per line.
          </div>
          <textarea
            value={feedUrls}
            onChange={(event) => setFeedUrls(event.target.value)}
            placeholder={'https://example.com/feed.xml\nhttps://example.org/rss'}
            rows={4}
            style={{ width: '100%', padding: '7px 10px', background: 'var(--color-bg)', border: '1px solid var(--color-border)', borderRadius: 4, color: 'var(--color-text)', fontSize: 12, marginBottom: 6, boxSizing: 'border-box' }}
          />
          <button
            onClick={() => onConnect({ config: { feeds } })}
            disabled={loading || disabled || feeds.length === 0}
            style={{ width: '100%', padding: 8, background: loading || disabled || feeds.length === 0 ? 'var(--color-disabled-bg)' : 'var(--color-accent-purple)', color: 'var(--color-on-accent)', border: 'none', borderRadius: 6, fontSize: 12, cursor: loading || disabled || feeds.length === 0 ? 'default' : 'pointer' }}
          >
            {loading ? 'Connecting...' : 'Save feeds'}
          </button>
        </div>
      );
    }
    return (
      <div>
        <div style={{ fontSize: 12, color: 'var(--color-text-secondary)', marginBottom: 10 }}>
          {displayName} reads data directly from this device. Grant access if
          prompted, then connect.
        </div>
        <button
          onClick={() => onConnect({})}
          disabled={loading || disabled}
          style={{
            width: '100%', padding: 8,
            background: loading || disabled ? 'var(--color-disabled-bg)' : 'var(--color-accent-purple)',
            color: 'var(--color-on-accent)', border: 'none',
            borderRadius: 6, fontSize: 12,
            cursor: loading || disabled ? 'default' : 'pointer',
          }}
        >
          {loading ? 'Connecting...' : `Connect ${displayName}`}
        </button>
      </div>
    );
  }

  if (authType === 'token') {
    return (
      <div>
        <div style={{ fontSize: 12, color: 'var(--color-text-secondary)', marginBottom: 10 }}>
          Enter your {displayName} API token.
        </div>
        <InlineConnectForm
          fields={connectorId === 'weather'
            ? [
                { name: 'token', placeholder: 'OpenWeather API key', type: 'password' },
                { name: 'location', placeholder: 'City, country (for example: Boston,US)', type: 'text' },
              ]
            : [{ name: 'token', placeholder: `${displayName} API token`, type: 'password' }]}
          loading={loading}
          disabled={disabled}
          onSubmit={onConnect}
        />
      </div>
    );
  }

  // auth_type === 'oauth' (default for anything else without a catalog entry)
  if (oauthSetup?.has_credentials) {
    return (
      <div>
        <div style={{ fontSize: 12, color: 'var(--color-text-secondary)', marginBottom: 10 }}>
          OAuth app credentials are already configured. Continue directly to
          {oauthSetup.provider ? ` ${oauthSetup.provider}` : ' the provider'} sign-in.
        </div>
        <button
          onClick={onOAuthStart}
          disabled={loading || disabled}
          style={{
            width: '100%', padding: 8,
            background: loading || disabled ? 'var(--color-disabled-bg)' : 'var(--color-accent-purple)',
            color: 'var(--color-on-accent)', border: 'none',
            borderRadius: 6, fontSize: 12,
            cursor: loading || disabled ? 'default' : 'pointer',
          }}
        >
          {loading ? 'Connecting...' : `Continue with ${oauthSetup.provider || displayName}`}
        </button>
      </div>
    );
  }

  return (
    <div>
      {oauthSetup && !oauthSetup.has_credentials && (
        <div style={{
          background: 'var(--color-bg)',
          border: '1px solid var(--color-border)',
          borderRadius: 6, padding: 10, marginBottom: 10,
        }}>
          <div style={{ color: 'var(--color-accent-purple)', fontSize: 10, fontWeight: 600, marginBottom: 3 }}>
            SETUP REQUIRED
          </div>
          <div style={{ fontSize: 12, marginBottom: 6 }}>{oauthSetup.setup_hint}</div>
          <a
            href={oauthSetup.setup_url}
            target="_blank"
            rel="noopener noreferrer"
            style={{ color: 'var(--color-accent)', fontSize: 11, textDecoration: 'underline' }}
          >
            Open developer dashboard &rarr;
          </a>
        </div>
      )}
      <div style={{ fontSize: 12, color: 'var(--color-text-secondary)', marginBottom: 10 }}>
        Paste the Client ID and Client Secret from the app you created above.
      </div>
      <InlineConnectForm
        fields={[
          { name: 'email', placeholder: 'Client ID', type: 'text' },
          { name: 'password', placeholder: 'Client Secret', type: 'password' },
        ]}
        loading={loading}
        disabled={disabled}
        onSubmit={onConnect}
      />
    </div>
  );
}

// ---------------------------------------------------------------------------
// Upload / Paste form
// ---------------------------------------------------------------------------

const ACCEPTED_EXTENSIONS = '.txt,.md,.pdf,.docx,.csv,.zip,.png,.jpg,.jpeg,.gif,.webp,.bmp,.tiff,.mp4,.webm,.mov,.mkv,.avi';

function UploadForm({ onDone }: { onDone?: () => void }) {
  const [tab, setTab] = useState<'paste' | 'upload'>('paste');
  const [title, setTitle] = useState('');
  const [content, setContent] = useState('');
  const [files, setFiles] = useState<File[]>([]);
  const [busy, setBusy] = useState(false);
  const [result, setResult] = useState('');
  const [error, setError] = useState('');

  const handlePaste = async () => {
    if (!content.trim()) return;
    setBusy(true);
    setError('');
    setResult('');
    try {
      const res = await fetch(`${getBase()}/v1/connectors/upload/ingest`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ title: title.trim(), content }),
      });
      if (!res.ok) {
        const err = await res.json().catch(() => ({ detail: res.statusText }));
        throw new Error(err.detail || `Upload failed: ${res.status}`);
      }
      const data = await res.json();
      setResult(`Added ${data.chunks_added} chunk${data.chunks_added !== 1 ? 's' : ''} to knowledge base`);
      setTitle('');
      setContent('');
      onDone?.();
    } catch (err: any) {
      setError(err.message || 'Upload failed');
    } finally {
      setBusy(false);
    }
  };

  const handleUpload = async () => {
    if (files.length === 0) return;
    setBusy(true);
    setError('');
    setResult('');
    try {
      const formData = new FormData();
      for (const f of files) formData.append('files', f);
      if (title.trim()) formData.append('title', title.trim());

      const res = await fetch(`${getBase()}/v1/connectors/upload/ingest/files`, {
        method: 'POST',
        body: formData,
      });
      if (!res.ok) {
        const err = await res.json().catch(() => ({ detail: res.statusText }));
        throw new Error(err.detail || `Upload failed: ${res.status}`);
      }
      const data = await res.json();
      setResult(`Added ${data.chunks_added} chunk${data.chunks_added !== 1 ? 's' : ''} from ${files.length} file${files.length !== 1 ? 's' : ''}`);
      setFiles([]);
      setTitle('');
      onDone?.();
    } catch (err: any) {
      setError(err.message || 'Upload failed');
    } finally {
      setBusy(false);
    }
  };

  const tabStyle = (active: boolean): React.CSSProperties => ({
    flex: 1, padding: '6px 0', textAlign: 'center',
    fontSize: 12, fontWeight: 600, cursor: 'pointer',
    background: active ? 'var(--color-accent-purple)' : 'transparent',
    color: active ? 'white' : 'var(--color-text-secondary)',
    border: 'none', borderRadius: 4,
  });

  const inputStyle: React.CSSProperties = {
    width: '100%', padding: '7px 10px',
    background: 'var(--color-bg)',
    border: '1px solid var(--color-border)',
    borderRadius: 4, color: 'var(--color-text)',
    fontSize: 12, marginBottom: 6,
    boxSizing: 'border-box' as const,
  };

  return (
    <div>
      {/* Tab bar */}
      <div style={{ display: 'flex', gap: 4, marginBottom: 10,
        background: 'var(--color-bg)', borderRadius: 6, padding: 2 }}>
        <button style={tabStyle(tab === 'paste')} onClick={() => setTab('paste')}>
          Paste Text
        </button>
        <button style={tabStyle(tab === 'upload')} onClick={() => setTab('upload')}>
          Upload Files
        </button>
      </div>

      {/* Title input (shared) */}
      <input
        value={title}
        onChange={(e) => setTitle(e.target.value)}
        placeholder="Title (optional)"
        style={inputStyle}
      />

      {tab === 'paste' && (
        <>
          <textarea
            value={content}
            onChange={(e) => setContent(e.target.value)}
            placeholder="Paste your text here..."
            rows={6}
            style={{
              ...inputStyle,
              resize: 'vertical',
              fontFamily: 'inherit',
              minHeight: 100,
            }}
          />
          <button
            onClick={handlePaste}
            disabled={busy || !content.trim()}
            style={{
              width: '100%', padding: 8,
              background: busy || !content.trim() ? 'var(--color-disabled-bg)' : 'var(--color-accent-purple)',
              color: 'var(--color-on-accent)', border: 'none',
              borderRadius: 6, fontSize: 12, cursor: 'pointer',
            }}
          >
            {busy ? 'Adding...' : 'Add to Knowledge Base'}
          </button>
        </>
      )}

      {tab === 'upload' && (
        <>
          <input
            type="file"
            multiple
            accept={ACCEPTED_EXTENSIONS}
            onChange={(e) => {
              const selected = Array.from(e.target.files || []);
              setFiles(selected);
            }}
            style={{ ...inputStyle, padding: 6 }}
          />
          {files.length > 0 && (
            <div style={{ fontSize: 11, color: 'var(--color-text-secondary)', marginBottom: 6 }}>
              {files.map((f) => f.name).join(', ')}
            </div>
          )}
          <button
            onClick={handleUpload}
            disabled={busy || files.length === 0}
            style={{
              width: '100%', padding: 8,
              background: busy || files.length === 0 ? 'var(--color-disabled-bg)' : 'var(--color-accent-purple)',
              color: 'var(--color-on-accent)', border: 'none',
              borderRadius: 6, fontSize: 12, cursor: 'pointer',
            }}
          >
            {busy ? 'Uploading...' : 'Upload & Index'}
          </button>
        </>
      )}

      {result && (
        <div style={{ fontSize: 12, color: 'var(--color-success)', marginTop: 8 }}>
          {result}
        </div>
      )}
      {error && (
        <div style={{ fontSize: 12, color: 'var(--color-error)', marginTop: 8 }}>
          {error}
        </div>
      )}
    </div>
  );
}

// ---------------------------------------------------------------------------
// Icon map
// ---------------------------------------------------------------------------

const iconMap: Record<string, LucideIcon> = {
  gmail: Mail,
  gmail_imap: Mail,
  gmail_api: Mail,
  outlook: Mail,
  slack: Hash,
  imessage: MessageCircle,
  whatsapp: PhoneCall,
  gdrive: FolderOpen,
  dropbox: Package,
  notion: BookText,
  obsidian: FileText,
  apple_notes: StickyNote,
  granola: FileText,
  gcalendar: CalendarDays,
  gcontacts: Contact,
  apple_contacts: Contact,
  upload: Upload,
};

const IconFor = ({ id, size = 18 }: { id: string; size?: number }) => {
  const Ico = iconMap[id] ?? Link2;
  return <Ico size={size} />;
};

<<<<<<< ours
||||||| base
// The Gmail card unifies the OAuth (`gmail`) and IMAP (`gmail_imap`) backend
// connectors â€” both should resolve to the gmail_imap catalog entry so the
// connected card shows the same name, unit label, and troubleshooting tips
// regardless of which underlying flow the user picked.
function metaFor(connectorId: string) {
  const id = connectorId === 'gmail' ? 'gmail_imap' : connectorId;
  return SOURCE_CATALOG.find((s) => s.connector_id === id);
}

// Advanced OAuth disclosure for the unified Gmail card. Hidden by default;
// expands to a Client ID + Client Secret form that POSTs to the OAuth
// `gmail` backend connector. Lives here rather than in SOURCE_CATALOG
// because the Gmail card is the only one with a dual-flow shape.
function GmailOAuthAdvanced({
  loading,
  onConnect,
}: {
  loading: boolean;
  onConnect: (req: ConnectRequest) => void;
}) {
  const [open, setOpen] = useState(false);
  return (
    <div style={{ marginTop: 12 }}>
      <button
        type="button"
        onClick={() => setOpen((o) => !o)}
        style={{
          background: 'transparent',
          border: 'none',
          padding: 0,
          fontSize: 11,
          color: 'var(--color-text-tertiary)',
          cursor: 'pointer',
          textDecoration: 'underline',
        }}
      >
        {open ? 'Hide advanced' : 'Advanced: Connect with Google OAuth'}
      </button>
      {open && (
        <div
          style={{
            marginTop: 8,
            padding: 10,
            background: 'var(--color-bg)',
            border: '1px solid var(--color-border)',
            borderRadius: 6,
          }}
        >
          <div style={{ fontSize: 11, color: 'var(--color-text-tertiary)', marginBottom: 8 }}>
            For developers with an existing Google Cloud project. Enable the
            Gmail API and create a Desktop OAuth client at{' '}
            <a
              href="https://console.cloud.google.com/apis/credentials"
              target="_blank"
              rel="noopener noreferrer"
              style={{ color: 'var(--color-accent)', textDecoration: 'underline' }}
            >
              Google Cloud Credentials â†’
            </a>{' '}
            then paste the Client ID and Client Secret below.
          </div>
          <InlineConnectForm
            fields={[
              { name: 'email', placeholder: 'Client ID', type: 'text' },
              { name: 'password', placeholder: 'Client Secret', type: 'password' },
            ]}
            loading={loading}
            onSubmit={onConnect}
          />
        </div>
      )}
    </div>
  );
}

=======
// The Gmail card unifies the OAuth (`gmail`) and IMAP (`gmail_imap`) backend
// connectors â€” both should resolve to the gmail_imap catalog entry so the
// connected card shows the same name, unit label, and troubleshooting tips
// regardless of which underlying flow the user picked.
function metaFor(connectorId: string) {
  const id = connectorId === 'gmail' ? 'gmail_imap' : connectorId;
  return SOURCE_CATALOG.find((s) => s.connector_id === id);
}

// Advanced OAuth disclosure for the unified Gmail card. Hidden by default;
// expands to a Client ID + Client Secret form that POSTs to the OAuth
// `gmail` backend connector. Lives here rather than in SOURCE_CATALOG
// because the Gmail card is the only one with a dual-flow shape.
function GmailOAuthAdvanced({
  loading,
  disabled = false,
  onConnect,
}: {
  loading: boolean;
  disabled?: boolean;
  onConnect: (req: ConnectRequest) => void;
}) {
  const [open, setOpen] = useState(false);
  return (
    <div style={{ marginTop: 12 }}>
      <button
        type="button"
        onClick={() => setOpen((o) => !o)}
        disabled={disabled}
        style={{
          background: 'transparent',
          border: 'none',
          padding: 0,
          fontSize: 11,
          color: 'var(--color-text-tertiary)',
          cursor: disabled ? 'default' : 'pointer',
          opacity: disabled ? 0.5 : 1,
          textDecoration: 'underline',
        }}
      >
        {open ? 'Hide advanced' : 'Advanced: Connect with Google OAuth'}
      </button>
      {open && (
        <div
          style={{
            marginTop: 8,
            padding: 10,
            background: 'var(--color-bg)',
            border: '1px solid var(--color-border)',
            borderRadius: 6,
          }}
        >
          <div style={{ fontSize: 11, color: 'var(--color-text-tertiary)', marginBottom: 8 }}>
            For developers with an existing Google Cloud project. Enable the
            Gmail API and create a Desktop OAuth client at{' '}
            <a
              href="https://console.cloud.google.com/apis/credentials"
              target="_blank"
              rel="noopener noreferrer"
              style={{ color: 'var(--color-accent)', textDecoration: 'underline' }}
            >
              Google Cloud Credentials â†’
            </a>{' '}
            then paste the Client ID and Client Secret below.
          </div>
          <InlineConnectForm
            fields={[
              { name: 'email', placeholder: 'Client ID', type: 'text' },
              { name: 'password', placeholder: 'Client Secret', type: 'password' },
            ]}
            loading={loading}
            disabled={disabled}
            onSubmit={onConnect}
          />
        </div>
      )}
    </div>
  );
}

>>>>>>> theirs
// ---------------------------------------------------------------------------
// Data Sources section
// ---------------------------------------------------------------------------

// Sync status display component with progress bar
<<<<<<< ours
function SyncStatusDisplay({
||||||| base
function formatTimeAgo(iso: string | null | undefined): string | null {
  if (!iso) return null;
  const t = new Date(iso).getTime();
  if (Number.isNaN(t)) return null;
  const diffSec = (Date.now() - t) / 1000;
  if (diffSec < 30) return 'just now';
  if (diffSec < 60) return 'less than a min ago';
  if (diffSec < 3600) {
    const m = Math.round(diffSec / 60);
    return `${m} min${m === 1 ? '' : 's'} ago`;
  }
  if (diffSec < 86400) {
    const h = Math.round(diffSec / 3600);
    return `${h} hr${h === 1 ? '' : 's'} ago`;
  }
  const d = Math.round(diffSec / 86400);
  return `${d} day${d === 1 ? '' : 's'} ago`;
}

/** Render how far back the corpus extends, given the oldest indexed
 *  item's timestamp. Returns null when there isn't enough data yet. */
function formatBacklogRange(iso: string | null | undefined): string | null {
  if (!iso) return null;
  const t = new Date(iso).getTime();
  if (Number.isNaN(t)) return null;
  const days = (Date.now() - t) / 86400_000;
  if (days < 7) return 'past few days';
  if (days < 30) return 'past month';
  if (days < 90) return 'past 3 months';
  if (days < 365) return 'past year';
  const years = Math.round(days / 365);
  return `past ${years} year${years === 1 ? '' : 's'}`;
}

function SyncStatusDisplay({
=======
function formatTimeAgo(iso: string | null | undefined): string | null {
  if (!iso) return null;
  const t = new Date(iso).getTime();
  if (Number.isNaN(t)) return null;
  const diffSec = (Date.now() - t) / 1000;
  if (diffSec < 30) return 'just now';
  if (diffSec < 60) return 'less than a min ago';
  if (diffSec < 3600) {
    const m = Math.round(diffSec / 60);
    return `${m} min${m === 1 ? '' : 's'} ago`;
  }
  if (diffSec < 86400) {
    const h = Math.round(diffSec / 3600);
    return `${h} hr${h === 1 ? '' : 's'} ago`;
  }
  const d = Math.round(diffSec / 86400);
  return `${d} day${d === 1 ? '' : 's'} ago`;
}

/** Render how far back the corpus extends, given the oldest indexed
 *  item's timestamp. Returns null when there isn't enough data yet. */
function formatBacklogRange(iso: string | null | undefined): string | null {
  if (!iso) return null;
  const t = new Date(iso).getTime();
  if (Number.isNaN(t)) return null;
  const days = (Date.now() - t) / 86400_000;
  if (days < 7) return 'past few days';
  if (days < 30) return 'past month';
  if (days < 90) return 'past 3 months';
  if (days < 365) return 'past year';
  const years = Math.round(days / 365);
  return `past ${years} year${years === 1 ? '' : 's'}`;
}

export function SyncStatusDisplay({
>>>>>>> theirs
  chunks,
  sync,
  unitLabel,
  connectorId,
  disabled = false,
  onSyncTriggered,
}: {
  chunks: number;
  sync: SyncStatus | undefined;
  unitLabel: string;
  connectorId: string;
  disabled?: boolean;
  onSyncTriggered: () => void;
}) {
  const [syncing, setSyncing] = useState(false);
  const [syncError, setSyncError] = useState('');

  const handleSync = async () => {
    if (disabled || sync?.state === 'stopping') return;
    setSyncing(true);
    setSyncError('');
    try {
      await triggerSync(connectorId);
      onSyncTriggered();
    } catch (err: any) {
      setSyncError(err.message || 'Sync failed');
    } finally {
      setSyncing(false);
    }
  };

  // Disconnect cleanup only begins after the active sync worker exits. Keep
  // every competing lifecycle action unavailable while the backend reports
  // this transitional state; the disconnect handler retries automatically.
  if (sync?.state === 'stopping') {
    return (
      <div>
        <div style={{ fontSize: 12, color: 'var(--color-warning)', marginBottom: 4 }}>
          Disconnect pending â€” waiting for the active sync to stop.
        </div>
        <div style={{ fontSize: 10.5, color: 'var(--color-text-tertiary)' }}>
          Indexed data will be cleaned up before this source disconnects.
        </div>
      </div>
    );
  }

  // Error state
  if (sync?.error) {
    return (
      <div>
        <div style={{ fontSize: 12, color: 'var(--color-error)', marginBottom: 4 }}>
          Error: {sync.error}
        </div>
        <button
          onClick={handleSync}
          disabled={syncing || disabled}
          style={{
            fontSize: 10, padding: '2px 10px',
            background: 'var(--color-accent-purple)', color: 'var(--color-on-accent)',
            border: 'none', borderRadius: 3,
            cursor: syncing || disabled ? 'default' : 'pointer', fontWeight: 600,
            opacity: syncing || disabled ? 0.5 : 1,
          }}
        >{syncing ? 'Retrying...' : 'Retry Sync'}</button>
      </div>
    );
  }

  // Done â€” has chunks
  if (chunks > 0) {
    return (
      <div>
        <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
          <span style={{ fontSize: 12, color: 'var(--color-success)' }}>
            {chunks.toLocaleString()} {unitLabel}
          </span>
          <button
            onClick={handleSync}
            disabled={syncing || disabled}
            style={{
              fontSize: 9, padding: '1px 6px',
              background: 'transparent',
              color: 'var(--color-text-tertiary)',
              border: '1px solid var(--color-border)',
              borderRadius: 3,
              cursor: syncing || disabled ? 'default' : 'pointer',
              opacity: syncing || disabled ? 0.5 : 1,
            }}
          >{syncing ? '...' : 'Re-sync'}</button>
        </div>
        {syncError && (
          <div style={{ fontSize: 11, color: 'var(--color-error)', marginTop: 4 }}>
            {syncError}
          </div>
        )}
      </div>
    );
  }

  // Actively syncing
  if (sync?.state === 'syncing' || syncing) {
    const pct = sync?.items_total && sync.items_total > 0
      ? Math.round((sync.items_synced / sync.items_total) * 100)
      : null;
    const label = sync?.items_total && sync.items_total > 0
      ? `${sync.items_synced.toLocaleString()} / ${sync.items_total.toLocaleString()}`
      : sync?.items_synced && sync.items_synced > 0
        ? `${sync.items_synced.toLocaleString()} items so far`
        : 'Starting...';
    return (
      <div>
        <div style={{ fontSize: 11, color: 'var(--color-warning)', marginBottom: 4 }}>
          Syncing â€” {label}
        </div>
        <div style={{
          height: 4, borderRadius: 2,
          background: 'var(--color-bg-tertiary)',
          overflow: 'hidden',
        }}>
          <div style={{
            height: '100%', borderRadius: 2,
            background: 'var(--color-warning)',
            width: pct != null ? `${pct}%` : '30%',
            transition: 'width 0.5s ease',
            animationName: pct == null ? 'pulse' : undefined,
            animationDuration: pct == null ? '1.5s' : undefined,
            animationIterationCount: pct == null ? 'infinite' : undefined,
          }} />
        </div>
      </div>
    );
  }

  // Idle with items synced but no chunks yet (indexing)
  if (sync?.state === 'idle' && sync.items_synced > 0) {
    return (
      <div>
        <div style={{ fontSize: 11, color: 'var(--color-warning)', marginBottom: 4 }}>
          Indexing {sync.items_synced.toLocaleString()} items...
        </div>
        <div style={{
          height: 4, borderRadius: 2,
          background: 'var(--color-bg-tertiary)',
          overflow: 'hidden',
        }}>
          <div style={{
            height: '100%', borderRadius: 2, background: 'var(--color-warning)',
            width: '60%',
            animationName: 'pulse', animationDuration: '1.5s', animationIterationCount: 'infinite',
          }} />
        </div>
      </div>
    );
  }

  // Connected but no chunks yet
  const hasSynced = sync?.last_sync != null;
  return (
    <div>
      <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
        <span style={{ fontSize: 12, color: 'var(--color-text-tertiary)' }}>
          {hasSynced
            ? 'Synced â€” 0 items found'
            : 'Connected â€” not synced yet'}
        </span>
        <button
          onClick={handleSync}
          disabled={syncing || disabled}
          style={{
            fontSize: 10, padding: '2px 10px',
            background: 'var(--color-accent-purple)', color: 'var(--color-on-accent)',
            border: 'none', borderRadius: 3,
            cursor: syncing || disabled ? 'default' : 'pointer', fontWeight: 600,
            opacity: syncing || disabled ? 0.5 : 1,
          }}
        >{syncing ? 'Syncing...' : hasSynced ? 'Re-sync' : 'Sync Now'}</button>
      </div>
      {hasSynced && connectorId === 'slack' && (
        <div style={{ fontSize: 10, color: 'var(--color-text-tertiary)', marginTop: 4 }}>
          Tip: invite the bot to channels with /invite @OpenJarvis, then re-sync
        </div>
      )}
      {syncError && (
        <div style={{ fontSize: 11, color: 'var(--color-error)', marginTop: 4 }}>
          {syncError}
        </div>
      )}
    </div>
  );
}

function DataSourcesSection() {
  const cachedConnectors = useAppStore((s) => s.cachedConnectors);
  const setCachedConnectors = useAppStore((s) => s.setCachedConnectors);
  const connectors = cachedConnectors ?? [];
  const isFirstLoad = cachedConnectors === null;
  const [syncStatuses, setSyncStatuses] = useState<Record<string, SyncStatus>>({});
  const [expandedId, setExpandedId] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [disconnectingId, setDisconnectingId] = useState<string | null>(null);
  const [disconnectError, setDisconnectError] = useState<{ id: string; message: string } | null>(null);
  const disconnectAbortRef = useRef<AbortController | null>(null);

  const loadConnectors = useCallback(async () => {
    try {
      const list = await listConnectors();
      setCachedConnectors(
        list.map((c) => ({
          connector_id: c.connector_id,
          display_name: c.display_name,
          connected: c.connected,
          chunks: (c as any).chunks || 0,
          auth_type: c.auth_type,
        })),
      );
    } catch {
      // The periodic refresh will try again.
    }
  }, [setCachedConnectors]);

  const setConnectors = setCachedConnectors;

  // Poll sync status for connected sources
  const loadSyncStatuses = useCallback(async () => {
    const connected = connectors.filter((c) => c.connected);
    const statuses: Record<string, SyncStatus> = {};
    await Promise.all(
      connected.map(async (c) => {
        try {
          statuses[c.connector_id] = await getSyncStatus(c.connector_id);
        } catch { /* */ }
      }),
    );
    setSyncStatuses((prev) => ({ ...prev, ...statuses }));
  }, [connectors]);

  useEffect(() => {
    void loadConnectors();
    const interval = setInterval(() => void loadConnectors(), 10000);
    return () => clearInterval(interval);
  }, [loadConnectors]);

  useEffect(() => {
    if (connectors.some((c) => c.connected)) {
      loadSyncStatuses();
      const interval = setInterval(loadSyncStatuses, 5000);
      return () => clearInterval(interval);
    }
  }, [connectors, loadSyncStatuses]);

  const [connectingId, setConnectingId] = useState<string | null>(null);
  const [connectStage, setConnectStage] = useState<string>('');
  const [connectError, setConnectError] = useState<string>('');
<<<<<<< ours
||||||| base
  const [disconnectingId, setDisconnectingId] = useState<string | null>(null);

  const handleDisconnect = async (id: string) => {
    if (disconnectingId) return;
    setDisconnectingId(id);
    try {
      await disconnectSource(id);
      loadConnectors();
    } catch {
      // Surface failures silently â€” the connector list will refresh on the
      // next poll and reflect the true state regardless.
    } finally {
      setDisconnectingId(null);
    }
  };
=======

  useEffect(() => () => disconnectAbortRef.current?.abort(), []);

  const handleDisconnect = async (id: string) => {
    if (disconnectAbortRef.current || loading) return;
    const controller = new AbortController();
    disconnectAbortRef.current = controller;
    setDisconnectingId(id);
    setDisconnectError(null);
    try {
      await disconnectSourceUntilComplete(id, {
        signal: controller.signal,
        onPending: () => {
          setSyncStatuses((prev) => {
            const current = prev[id];
            return {
              ...prev,
              [id]: {
                state: 'stopping',
                items_synced: current?.items_synced ?? 0,
                items_total: current?.items_total ?? 0,
                new_items_synced: current?.new_items_synced ?? null,
                oldest_item_date: current?.oldest_item_date ?? null,
                last_sync: current?.last_sync ?? null,
                error: null,
              },
            };
          });
        },
      });
      setSyncStatuses((prev) => {
        const next = { ...prev };
        delete next[id];
        return next;
      });
      await loadConnectors();
    } catch (err) {
      if (!(err instanceof DOMException && err.name === 'AbortError')) {
        setDisconnectError({
          id,
          message: err instanceof Error ? err.message : 'Disconnect failed',
        });
      }
    } finally {
      if (disconnectAbortRef.current === controller) {
        disconnectAbortRef.current = null;
        setDisconnectingId(null);
      }
    }
  };
>>>>>>> theirs

  const handleConnect = async (id: string, req: ConnectRequest | null) => {
    if (loading || disconnectAbortRef.current) return;
    setLoading(true);
    setConnectingId(id);
    setConnectStage('Connecting...');
    setConnectError('');
    try {
      const resp = req === null ? null : await connectSource(id, req);

      // OAuth connectors (Google Drive/Calendar/Contacts/Gmail/Tasks): pasting
      // a Client ID / Secret only registers the app credentials. The backend
      // returns `oauth_required` with the path to the in-process consent flow,
      // which is the only path that actually mints an access token. Open it now
      // and wait for the callback to flip the connector to connected. Without
      // this the connector would stay "pending" forever â€” the exact #512 bug.
      if (req === null || resp?.status === 'oauth_required') {
        setConnectStage('Opening provider sign-in...');
        await startServerOAuth(id, resp?.oauth_start);
      }

      setConnectStage('Connected! Starting sync...');

      // Wait for connector to show as connected
      for (let i = 0; i < 20; i++) {
        await new Promise((r) => setTimeout(r, 2000));
        const updated = await listConnectors();
        const target = updated.find((c) => c.connector_id === id);
        if (target?.connected) {
          setConnectors(updated.map((c) => ({
            connector_id: c.connector_id,
            display_name: c.display_name,
            connected: c.connected,
            chunks: (c as any).chunks || 0,
            auth_type: c.auth_type,
          })));
          break;
        }
        setConnectStage(i < 5 ? 'Authenticating...' : 'Waiting for connection...');
      }

      // Trigger sync
      setConnectStage('Syncing data...');
      try {
        await triggerSync(id);
      } catch { /* sync may already be running */ }

      // Close form after a brief moment
      await new Promise((r) => setTimeout(r, 1500));
      setExpandedId(null);
      loadConnectors();
      loadSyncStatuses();
    } catch (err: any) {
      let errorMsg = err.message || 'Connection failed';
      if (id === 'gmail_imap' && (errorMsg.includes('auth') || errorMsg.includes('credentials') || errorMsg.includes('LOGIN'))) {
        errorMsg = 'Invalid credentials â€” make sure you\'re using an App Password (16 characters), not your regular Gmail password.';
      }
      setConnectError(errorMsg);
      setConnectStage('');
    } finally {
      setLoading(false);
      setConnectingId(null);
      setConnectStage('');
    }
  };

  const connected = connectors.filter((c) => c.connected);
  const notConnectedBase = connectors.filter((c) => !c.connected);
  // Always show the upload card in the not-connected list (it has no backend connector)
  const uploadEntry = { connector_id: 'upload', display_name: 'Upload / Paste', connected: false, chunks: 0, auth_type: 'local' };
  const notConnected = notConnectedBase.some((c) => c.connector_id === 'upload')
    ? notConnectedBase
    : [...notConnectedBase, uploadEntry];
  const connectorActionsBusy = loading || disconnectingId !== null;

  if (isFirstLoad) {
    return (
      <div className="flex flex-col gap-5">
        <section>
          <div className="hud-label mb-2" style={{ color: 'var(--color-text-tertiary)' }}>
            Loading sourcesâ€¦
          </div>
          <div className="flex flex-col gap-2">
            {[0, 1, 2, 3].map((i) => (
              <div
                key={i}
                className="hud-panel data-skeleton"
                style={{
                  padding: '14px 18px',
                  height: 60,
                  opacity: 0.6 - i * 0.08,
                }}
              />
            ))}
          </div>
        </section>
      </div>
    );
  }

  return (
    <div className="flex flex-col gap-5">
      {/* Connected sources */}
      {connected.length > 0 && (
        <section>
          <div className="hud-label mb-2 flex items-center gap-2">
            <span style={{ display: 'inline-block', width: 6, height: 6, borderRadius: 999, background: 'var(--color-success)' }} />
            Connected Â· {connected.length}
          </div>
          <div className="flex flex-col gap-2">
          {connected.map((c) => {
            const meta = SOURCE_CATALOG.find(s => s.connector_id === c.connector_id);
            const unit = meta?.unitLabel || 'items';
            const sync = syncStatuses[c.connector_id];
            const isReconnecting = expandedId === c.connector_id;
            const hasError = !!sync?.error;
            return (
              <div
                key={c.connector_id}
                className="hud-panel"
                style={{
                  borderColor: hasError
                    ? 'color-mix(in srgb, var(--color-error) 28%, transparent)'
                    : 'var(--color-border)',
                }}
              >
                <div style={{
                  padding: '14px 18px',
                  display: 'flex', alignItems: 'center', gap: 14,
                }}>
                  <div style={{ flex: 1, minWidth: 0 }}>
                    <div className="font-semibold" style={{ fontSize: 14, fontWeight: 600, color: 'var(--color-text)' }}>
                      {c.display_name}
                    </div>
                    <SyncStatusDisplay
                      chunks={c.chunks}
                      sync={sync}
                      unitLabel={unit}
                      connectorId={c.connector_id}
                      disabled={connectorActionsBusy}
                      onSyncTriggered={loadConnectors}
                    />
                    {disconnectError?.id === c.connector_id && (
                      <div style={{ fontSize: 11, color: 'var(--color-error)', marginTop: 4 }}>
                        Disconnect failed: {disconnectError.message}
                      </div>
                    )}
                  </div>
                  <button
<<<<<<< ours
                    onClick={() => setExpandedId(isReconnecting ? null : c.connector_id)}
||||||| base
                    onClick={() => handleDisconnect(c.connector_id)}
                    disabled={disconnectingId === c.connector_id}
=======
                    onClick={() => handleDisconnect(c.connector_id)}
                    disabled={connectorActionsBusy}
>>>>>>> theirs
                    className="hud-label"
                    style={{
                      padding: '6px 12px',
                      background: 'transparent',
                      color: 'var(--color-text-secondary)',
                      border: '1px solid var(--color-border)',
<<<<<<< ours
                      borderRadius: 4, cursor: 'pointer',
||||||| base
                      borderRadius: 4,
                      cursor: disconnectingId === c.connector_id ? 'default' : 'pointer',
=======
                      borderRadius: 4,
                      cursor: connectorActionsBusy ? 'default' : 'pointer',
>>>>>>> theirs
                      letterSpacing: '0.15em',
<<<<<<< ours
||||||| base
                      opacity: disconnectingId === c.connector_id ? 0.5 : 1,
=======
                      opacity: connectorActionsBusy ? 0.5 : 1,
>>>>>>> theirs
                    }}
                  >
<<<<<<< ours
                    {isReconnecting ? 'Cancel' : 'Reconnect'}
||||||| base
                    {disconnectingId === c.connector_id ? 'Disconnectingâ€¦' : 'Disconnect'}
=======
                    {disconnectingId === c.connector_id
                      ? sync?.state === 'stopping' ? 'Cleaning upâ€¦' : 'Disconnectingâ€¦'
                      : sync?.state === 'stopping' ? 'Finish disconnect' : 'Disconnect'}
>>>>>>> theirs
                  </button>
                </div>
                {isReconnecting && meta?.steps && (
                  <div style={{ borderTop: '1px solid var(--color-border)', padding: 12 }}>
                    <div style={{ fontSize: 12, color: 'var(--color-warning)', marginBottom: 8 }}>
                      Re-enter credentials to reconnect this source.
                    </div>
                    {meta.steps.map((step, i) => (
                      <div
                        key={i}
                        style={{
                          background: 'var(--color-bg)',
                          border: '1px solid var(--color-border)',
                          borderRadius: 6, padding: 10,
                          marginBottom: 8,
                        }}
                      >
                        <div style={{ color: 'var(--color-accent-purple)', fontSize: 10, fontWeight: 600, marginBottom: 3 }}>
                          STEP {i + 1}
                        </div>
                        <div style={{ fontSize: 12, marginBottom: step.url ? 4 : 0 }}>{step.label}</div>
                        {step.url && (
                          <a
                            href={step.url}
                            target="_blank"
                            rel="noopener noreferrer"
                            style={{ color: 'var(--color-accent)', fontSize: 11, textDecoration: 'underline' }}
                          >
                            {step.urlLabel || 'Open'} &rarr;
                          </a>
                        )}
                      </div>
                    ))}
                    {meta.inputFields && (
                      <InlineConnectForm
                        fields={meta.inputFields}
                        loading={loading}
                        onSubmit={(req) => handleConnect(c.connector_id, req)}
                      />
                    )}
                  </div>
                )}
              </div>
            );
          })}
          </div>
        </section>
      )}

      {/* Not connected list */}
      {notConnected.length > 0 && (
        <section>
          <div className="hud-label mb-2 flex items-center gap-2">
            <span style={{ display: 'inline-block', width: 6, height: 6, borderRadius: 999, background: 'var(--color-text-tertiary)' }} />
            Available Â· {notConnected.length}
          </div>
          <div className="grid grid-cols-2 gap-2">
          {notConnected.map((c) => {
            const meta = SOURCE_CATALOG.find(s => s.connector_id === c.connector_id);
            const isExpanded = expandedId === c.connector_id;

            return (
              <div
                key={c.connector_id}
                className="hud-panel"
                style={{
                  gridColumn: isExpanded ? '1 / -1' : undefined,
                  opacity: isExpanded ? 1 : 0.85,
                  borderStyle: isExpanded ? 'solid' : 'dashed',
                }}
              >
                <div
                  style={{
                    padding: '12px 14px', display: 'flex',
                    alignItems: 'center', gap: 12,
                    cursor: 'pointer',
                  }}
                  onClick={() => setExpandedId(isExpanded ? null : c.connector_id)}
                >
                  <div style={{ flex: 1, minWidth: 0 }}>
                    <div className="font-semibold" style={{ fontSize: 14, fontWeight: 600, color: 'var(--color-text)' }}>
                      {c.display_name}
                    </div>
                    <div style={{ fontSize: 11, color: 'var(--color-text-tertiary)', marginTop: 2 }}>
                      Not connected
                    </div>
                  </div>
                  <span style={{ color: 'var(--color-text-secondary)', fontSize: 12, fontWeight: 500 }}>
                    {isExpanded ? 'Ã— Close' : '+ Add'}
                  </span>
                </div>

                {isExpanded && c.connector_id === 'upload' && (
                  <div style={{ borderTop: '1px solid var(--color-border)', padding: 12 }}>
                    <div style={{ fontSize: 12, color: 'var(--color-text-secondary)', marginBottom: 10 }}>
                      Paste text or upload files (.txt, .md, .pdf, .docx, .csv) to add them to your knowledge base.
                    </div>
                    <UploadForm onDone={loadConnectors} />
                  </div>
                )}

                {isExpanded && c.connector_id !== 'upload' && meta?.steps && (
                  <div style={{ borderTop: '1px solid var(--color-border)', padding: 12 }}>
                    {meta.steps.map((step, i) => (
                      <div
                        key={i}
                        style={{
                          background: 'var(--color-bg)',
                          border: '1px solid var(--color-border)',
                          borderRadius: 6, padding: 10,
                          marginBottom: 8,
                        }}
                      >
                        <div style={{ color: 'var(--color-accent-purple)', fontSize: 10, fontWeight: 600, marginBottom: 3 }}>
                          STEP {i + 1}
                        </div>
                        <div style={{ fontSize: 12, marginBottom: step.url ? 4 : 0 }}>{step.label}</div>
                        {step.url && (
                          <a
                            href={step.url}
                            target="_blank"
                            rel="noopener noreferrer"
                            style={{ color: 'var(--color-accent)', fontSize: 11, textDecoration: 'underline' }}
                          >
                            {step.urlLabel || 'Open'} &rarr;
                          </a>
                        )}
                      </div>
                    ))}
                    {meta?.inputFields && (
                      <InlineConnectForm
                        fields={meta.inputFields}
                        loading={loading && connectingId === c.connector_id}
                        disabled={connectorActionsBusy}
                        onSubmit={(req) => handleConnect(c.connector_id, req)}
                      />
                    )}
<<<<<<< ours
||||||| base
                    {c.connector_id === 'gmail_imap' && (
                      <GmailOAuthAdvanced
                        loading={loading && connectingId === 'gmail'}
                        onConnect={(req) => handleConnect('gmail', req)}
                      />
                    )}
=======
                    {c.connector_id === 'gmail_imap' && (
                      <GmailOAuthAdvanced
                        loading={loading && connectingId === 'gmail'}
                        disabled={connectorActionsBusy}
                        onConnect={(req) => handleConnect('gmail', req)}
                      />
                    )}
>>>>>>> theirs
                    {meta?.troubleshooting && (
                      <details className="mt-2">
                        <summary className="text-[11px] cursor-pointer" style={{ color: 'var(--color-text-tertiary)' }}>
                          Having trouble?
                        </summary>
                        <ul className="mt-1 space-y-1">
                          {meta.troubleshooting.map((tip: string, i: number) => (
                            <li key={i} className="text-[11px]" style={{ color: 'var(--color-text-tertiary)' }}>
                              {tip}
                            </li>
                          ))}
                        </ul>
                      </details>
                    )}
                    {/* Connection progress */}
                    {connectingId === c.connector_id && connectStage && (
                      <div style={{ marginTop: 8 }}>
                        <div style={{
                          display: 'flex', alignItems: 'center', gap: 6,
                          fontSize: 12, color: 'var(--color-warning)',
                        }}>
                          <div className="animate-spin" style={{
                            width: 12, height: 12, borderRadius: '50%',
                            border: '2px solid var(--color-warning)',
                            borderTopColor: 'transparent',
                          }} />
                          {connectStage}
                        </div>
                        <div style={{
                          height: 3, borderRadius: 2, marginTop: 6,
                          background: 'var(--color-bg-tertiary)',
                          overflow: 'hidden',
                        }}>
                          <div style={{
                            height: '100%', borderRadius: 2, background: 'var(--color-warning)',
                            width: connectStage.includes('Sync') ? '75%' : connectStage.includes('Connected') ? '50%' : '25%',
                            transition: 'width 0.5s ease',
                          }} />
                        </div>
                      </div>
                    )}
                    {/* Connection error */}
                    {connectError && connectingId === null && expandedId === c.connector_id && (
                      <div style={{ fontSize: 11, color: 'var(--color-error)', marginTop: 6 }}>
                        {connectError}
                      </div>
                    )}
                  </div>
                )}

                {isExpanded && c.connector_id !== 'upload' && !meta?.steps && (
                  <div style={{ borderTop: '1px solid var(--color-border)', padding: 12 }}>
                    <GenericConnectPanel
                      connectorId={c.connector_id}
                      displayName={meta?.display_name ?? c.display_name}
                      authType={c.auth_type || 'oauth'}
                      loading={loading && connectingId === c.connector_id}
                      disabled={connectorActionsBusy}
                      onConnect={(req) => handleConnect(c.connector_id, req)}
                      onOAuthStart={() => handleConnect(c.connector_id, null)}
                    />
                    {connectingId === c.connector_id && connectStage && (
                      <div style={{ marginTop: 8, fontSize: 12, color: 'var(--color-warning)' }}>
                        {connectStage}
                      </div>
                    )}
                    {connectError && connectingId === null && expandedId === c.connector_id && (
                      <div style={{ fontSize: 11, color: 'var(--color-error)', marginTop: 6 }}>
                        {connectError}
                      </div>
                    )}
                  </div>
                )}
              </div>
            );
          })}
          </div>
        </section>
      )}
    </div>
  );
}

// ---------------------------------------------------------------------------
// Messaging channels section
// ---------------------------------------------------------------------------

interface ChannelField {
  key: string;
  label: string;
  placeholder: string;
  type?: 'text' | 'password';
  required?: boolean;
}

interface MessagingChannelConfig {
  type: string;
  name: string;
  icon: string;
  description: string;
  setupSteps: string[];
  fields: ChannelField[];
  activeLabel: (cfg: Record<string, unknown>) => string;
  howToUse: (cfg: Record<string, unknown>) => string;
}

const MESSAGING_CHANNELS: MessagingChannelConfig[] = [
  {
    type: 'slack',
    name: 'Slack',
    icon: '#',
    description: 'DM your agent in any Slack workspace',
    setupSteps: [
      '1. Go to api.slack.com/apps \u2192 click "Create New App" \u2192 choose "From an app manifest"',
      '2. Select your workspace. When asked for the manifest format, choose JSON. Then paste the manifest below (click "Copy" to copy it):',
      'COPYABLE:{"display_information":{"name":"OpenJarvis"},"features":{"app_home":{"home_tab_enabled":true,"messages_tab_enabled":true,"messages_tab_read_only_enabled":false},"bot_user":{"display_name":"OpenJarvis","always_online":true}},"oauth_config":{"scopes":{"bot":["chat:write","im:write","im:read","im:history","mpim:read","mpim:history","users:read","channels:read","channels:history","channels:join","groups:read","groups:history","app_mentions:read"]}},"settings":{"event_subscriptions":{"bot_events":["message.im"]},"socket_mode_enabled":true}}',
      '3. Click "Next" \u2192 review the summary \u2192 click "Create". Then go to "Install App" in the left sidebar \u2192 click "Install to Workspace" \u2192 click "Allow"',
      '4. In the left sidebar, click "OAuth & Permissions". Copy the "Bot User OAuth Token" (starts with xoxb-...)',
      '5. In the left sidebar, click "Basic Information" \u2192 scroll to "App-Level Tokens" \u2192 click "Generate Token and Scopes" \u2192 name it "socket" \u2192 click "Add Scope" \u2192 select "connections:write" \u2192 click "Generate" \u2192 copy the token (starts with xapp-...)',
      '6. (Optional) Still in "Basic Information", scroll to "Display Information" \u2192 upload the OpenJarvis icon as the app icon',
      '7. Paste both tokens below and click Connect',
    ],
    fields: [
      { key: 'bot_token', label: 'Bot Token', placeholder: 'xoxb-...', type: 'password', required: true },
      { key: 'app_token', label: 'App Token', placeholder: 'xapp-...', type: 'password', required: true },
    ],
    activeLabel: () => 'Connected to Slack',
    howToUse: () => 'Open Slack and DM @OpenJarvis to talk to your agent.',
  },
];

// SendBlue wizard â€” simplified for standalone page
function SendBlueSection({
  agentId,
  binding,
  onDone,
  onRemove,
}: {
  agentId: string;
  binding?: ChannelBinding;
  onDone: () => void;
  onRemove: (id: string) => void;
}) {
  const [step, setStep] = useState(0);
  const [apiKey, setApiKey] = useState('');
  const [apiSecret, setApiSecret] = useState('');
  const [phone, setPhone] = useState('');
  const [webhookUrl, setWebhookUrl] = useState('');
  const [webhookStatus, setWebhookStatus] = useState<'idle' | 'registering' | 'done' | 'error'>('idle');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [health, setHealth] = useState<any>(null);

  useEffect(() => {
    if (binding) {
      sendblueHealth().then(setHealth).catch(() => {});
    }
  }, [agentId, binding]);

  const registerWebhook = async () => {
    if (!webhookUrl.trim()) return;
    setWebhookStatus('registering');
    try {
      const url = webhookUrl.trim().replace(/\/+$/, '') + '/v1/channels/sendblue/webhook';
      await sendblueRegisterWebhook(apiKey.trim(), apiSecret.trim(), url);
      setWebhookStatus('done');
    } catch {
      setWebhookStatus('error');
    }
  };

  if (binding) {
    const cfg = (binding.config || {}) as Record<string, unknown>;
    return (
      <div style={{
        background: 'var(--color-bg-secondary)',
        border: '1px solid color-mix(in srgb, var(--color-success) 22%, transparent)',
        borderRadius: 8, marginBottom: 10,
        overflow: 'hidden',
      }}>
        <div style={{ display: 'flex', alignItems: 'center', padding: '12px 14px' }}>
          <span style={{ fontSize: 18, marginRight: 10 }}>{'\uD83D\uDCF1'}</span>
          <div style={{ flex: 1 }}>
            <div style={{ fontWeight: 600, fontSize: 13 }}>iMessage + SMS</div>
            <div style={{ fontSize: 11, color: 'var(--color-success)' }}>
              Active &mdash; text {(cfg.phone_number as string) || 'your number'} to chat
            </div>
          </div>
          <button
            onClick={() => onRemove(binding.id)}
            style={{
              fontSize: 10, padding: '2px 8px',
              background: 'transparent',
              color: 'var(--color-text-secondary)',
              border: '1px solid var(--color-border)',
              borderRadius: 4, cursor: 'pointer',
            }}
          >Remove</button>
        </div>
        {health && (
          <div style={{
            borderTop: '1px solid var(--color-border)',
            padding: '8px 14px', fontSize: 11,
            color: 'var(--color-text-secondary)',
          }}>
            Webhook: {health.webhook_registered ? 'registered' : 'not registered'}
            {health.phone_number && ` \u2022 ${health.phone_number}`}
          </div>
        )}
      </div>
    );
  }

  const inputStyle: React.CSSProperties = {
    width: '100%', padding: '6px 10px',
    background: 'var(--color-bg)', border: '1px solid var(--color-border)',
    borderRadius: 4, color: 'var(--color-text)', fontSize: 12,
    boxSizing: 'border-box',
  };

  // Not active â€” setup wizard
  const steps = [
    {
      title: 'Get SendBlue API keys',
      content: (
        <div>
          <div style={{ fontSize: 12, marginBottom: 8 }}>
            SendBlue lets your agent send and receive iMessages and SMS. You need an account and API credentials.
          </div>
          <div style={{ display: 'flex', gap: 8, marginBottom: 8 }}>
            <a
              href="https://sendblue.co"
              target="_blank"
              rel="noopener noreferrer"
              style={{ color: 'var(--color-accent)', fontSize: 12, textDecoration: 'underline' }}
            >
              1. Sign up at sendblue.co &rarr;
            </a>
          </div>
          <div style={{ marginBottom: 8 }}>
            <a
              href="https://dashboard.sendblue.co/api-credentials"
              target="_blank"
              rel="noopener noreferrer"
              style={{ color: 'var(--color-accent)', fontSize: 12, textDecoration: 'underline' }}
            >
              2. Go to your API Credentials page &rarr;
            </a>
          </div>
          <div style={{ fontSize: 11, color: 'var(--color-text-secondary)', marginBottom: 6 }}>
            Copy the "API Key" and "API Secret" from the credentials page and paste them below.
          </div>
          <input value={apiKey} onChange={(e) => setApiKey(e.target.value)}
            placeholder="API Key" style={{ ...inputStyle, marginTop: 4 }} />
          <input value={apiSecret} onChange={(e) => setApiSecret(e.target.value)}
            placeholder="API Secret" type="password" style={{ ...inputStyle, marginTop: 4 }} />
        </div>
      ),
      canAdvance: apiKey.trim() && apiSecret.trim(),
    },
    {
      title: 'Enter your phone number',
      content: (
        <div>
          <div style={{ fontSize: 12, marginBottom: 8 }}>
            Which phone number should SendBlue use? This is the number people will text to reach your agent.
          </div>
          <input value={phone} onChange={(e) => setPhone(e.target.value)}
            placeholder="+1XXXXXXXXXX" style={inputStyle} />
        </div>
      ),
      canAdvance: phone.trim().length >= 10,
    },
    {
      title: 'Set up webhook (ngrok tunnel)',
      content: (
        <div>
          <div style={{ fontSize: 12, marginBottom: 8 }}>
            SendBlue needs a public URL to send incoming messages to your local server. Use ngrok to create a tunnel.
          </div>
          <div style={{
            fontSize: 11, lineHeight: 1.6,
            color: 'var(--color-text-secondary)',
            padding: '8px 10px', marginBottom: 10,
            background: 'var(--color-bg-secondary)',
            borderRadius: 6,
            borderLeft: '3px solid var(--color-accent, var(--color-accent-purple))',
          }}>
            <div><strong>1.</strong> Open a terminal and run: <code style={{ color: 'var(--color-accent)', background: 'var(--color-bg)', padding: '1px 4px', borderRadius: 3 }}>ngrok http 8000</code></div>
            <div style={{ marginTop: 4 }}><strong>2.</strong> Copy the <code style={{ color: 'var(--color-accent)', background: 'var(--color-bg)', padding: '1px 4px', borderRadius: 3 }}>https://</code> forwarding URL (e.g. https://abc123.ngrok.io)</div>
            <div style={{ marginTop: 4 }}><strong>3.</strong> Paste it below and click "Register Webhook"</div>
          </div>
          <div style={{ display: 'flex', gap: 6 }}>
            <input
              value={webhookUrl}
              onChange={(e) => { setWebhookUrl(e.target.value); setWebhookStatus('idle'); }}
              placeholder="https://abc123.ngrok-free.app"
              style={{ ...inputStyle, flex: 1 }}
            />
            <button
              onClick={registerWebhook}
              disabled={!webhookUrl.trim() || webhookStatus === 'registering'}
              style={{
                fontSize: 11, padding: '6px 12px', whiteSpace: 'nowrap',
                background: webhookStatus === 'done' ? 'var(--color-success)' : 'var(--color-accent-purple)',
                color: 'var(--color-on-accent)', border: 'none', borderRadius: 4,
                cursor: 'pointer', fontWeight: 600,
                opacity: !webhookUrl.trim() || webhookStatus === 'registering' ? 0.5 : 1,
              }}
            >
              {webhookStatus === 'registering' ? 'Registering...'
                : webhookStatus === 'done' ? 'Registered!'
                : webhookStatus === 'error' ? 'Retry'
                : 'Register Webhook'}
            </button>
          </div>
          {webhookStatus === 'done' && (
            <div style={{ fontSize: 11, color: 'var(--color-success)', marginTop: 6 }}>
              Webhook registered! Incoming texts will be forwarded to your agent.
            </div>
          )}
          {webhookStatus === 'error' && (
            <div style={{ fontSize: 11, color: 'var(--color-error)', marginTop: 6 }}>
              Failed to register webhook. Check your ngrok URL and SendBlue credentials.
            </div>
          )}
          <div style={{ fontSize: 10, color: 'var(--color-text-tertiary)', marginTop: 8 }}>
            Don't have ngrok? <a href="https://ngrok.com/download" target="_blank" rel="noopener noreferrer" style={{ color: 'var(--color-accent)', textDecoration: 'underline' }}>Download it free</a>. You can also skip this step and register the webhook later.
          </div>
        </div>
      ),
      canAdvance: true, // webhook is optional â€” user can skip
    },
  ];

  const handleFinish = async () => {
    setLoading(true);
    setError('');
    try {
      await bindAgentChannel(agentId, 'sendblue', {
        api_key: apiKey.trim(),
        api_secret: apiSecret.trim(),
        phone_number: phone.trim(),
      });
      // If webhook was registered in the wizard, that's already done.
      // If not, try a best-effort registration with the provided URL.
      if (webhookUrl.trim() && webhookStatus !== 'done') {
        try {
          const url = webhookUrl.trim().replace(/\/+$/, '') + '/v1/channels/sendblue/webhook';
          await sendblueRegisterWebhook(apiKey.trim(), apiSecret.trim(), url);
        } catch { /* */ }
      }
      onDone();
      setStep(0);
      setApiKey('');
      setApiSecret('');
      setPhone('');
      setWebhookUrl('');
      setWebhookStatus('idle');
    } catch (err: any) {
      setError(err.message || 'Failed to connect');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{
      background: 'var(--color-bg-secondary)',
      border: '1px dashed var(--color-border)',
      borderRadius: 8, marginBottom: 10,
      overflow: 'hidden',
    }}>
      <div
        style={{
          display: 'flex', alignItems: 'center',
          padding: '12px 14px', cursor: 'pointer',
        }}
        onClick={() => setStep(step === 0 && !apiKey ? -1 : 0)}
      >
        <span style={{ fontSize: 18, marginRight: 10 }}>{'\uD83D\uDCF1'}</span>
        <div style={{ flex: 1 }}>
          <div style={{ fontWeight: 600, fontSize: 13 }}>iMessage + SMS (SendBlue)</div>
          <div style={{ fontSize: 11, color: 'var(--color-text-secondary)' }}>
            Let people text your agent from any phone
          </div>
        </div>
        <span style={{ color: 'var(--color-accent-purple)', fontSize: 11, fontWeight: 500 }}>
          {step >= 0 ? 'Set Up' : '+ Add'}
        </span>
      </div>

      {step >= 0 && (
        <div style={{ borderTop: '1px solid var(--color-border)', padding: 14 }}>
          {/* Step indicator */}
          <div style={{ display: 'flex', gap: 4, marginBottom: 12 }}>
            {steps.map((_, i) => (
              <div
                key={i}
                style={{
                  flex: 1, height: 3, borderRadius: 2,
                  background: i <= step ? 'var(--color-accent-purple)' : 'var(--color-border)',
                }}
              />
            ))}
          </div>

          <div style={{ fontSize: 12, fontWeight: 600, marginBottom: 8 }}>
            {steps[step]?.title}
          </div>
          {steps[step]?.content}

          {error && (
            <div style={{ fontSize: 11, color: 'var(--color-error)', marginTop: 6 }}>{error}</div>
          )}

          <div style={{ display: 'flex', gap: 8, marginTop: 12 }}>
            {step > 0 && (
              <button
                onClick={() => setStep(step - 1)}
                style={{
                  fontSize: 12, padding: '6px 16px',
                  background: 'var(--color-bg)',
                  color: 'var(--color-text-secondary)',
                  border: '1px solid var(--color-border)',
                  borderRadius: 5, cursor: 'pointer',
                }}
              >Back</button>
            )}
            {step < steps.length - 1 ? (
              <button
                onClick={() => setStep(step + 1)}
                disabled={!steps[step]?.canAdvance}
                style={{
                  fontSize: 12, padding: '6px 16px',
                  background: 'var(--color-accent-purple)', color: 'var(--color-on-accent)',
                  border: 'none', borderRadius: 5,
                  cursor: 'pointer', fontWeight: 600,
                  opacity: steps[step]?.canAdvance ? 1 : 0.5,
                }}
              >Next</button>
            ) : (
              <button
                onClick={handleFinish}
                disabled={loading || !steps[step]?.canAdvance}
                style={{
                  fontSize: 12, padding: '6px 16px',
                  background: 'var(--color-accent-purple)', color: 'var(--color-on-accent)',
                  border: 'none', borderRadius: 5,
                  cursor: 'pointer', fontWeight: 600,
                  opacity: loading || !steps[step]?.canAdvance ? 0.5 : 1,
                }}
              >{loading ? 'Connecting...' : 'Connect'}</button>
            )}
          </div>
        </div>
      )}
    </div>
  );
}

function MessagingSection({ agentId }: { agentId: string }) {
  const [bindings, setBindings] = useState<ChannelBinding[]>([]);
  const [setupType, setSetupType] = useState<string | null>(null);
  const [formValues, setFormValues] = useState<Record<string, string>>({});
  const [loading, setLoading] = useState(false);

  const loadBindings = useCallback(() => {
    fetchAgentChannels(agentId).then(setBindings).catch(() => setBindings([]));
  }, [agentId]);

  useEffect(() => { loadBindings(); }, [loadBindings]);

  const setField = (key: string, value: string) =>
    setFormValues((prev) => ({ ...prev, [key]: value }));

  const handleSetup = async (ch: MessagingChannelConfig) => {
    const missing = ch.fields.filter((f) => f.required && !formValues[f.key]?.trim());
    if (missing.length > 0) return;
    setLoading(true);
    try {
      const config: Record<string, string> = {};
      for (const f of ch.fields) {
        const v = formValues[f.key]?.trim();
        if (v) config[f.key] = v;
      }
      await bindAgentChannel(agentId, ch.type, config);
      setSetupType(null);
      setFormValues({});
      loadBindings();
    } catch { /* */ } finally { setLoading(false); }
  };

  const handleRemove = async (bindingId: string) => {
    try {
      await unbindAgentChannel(agentId, bindingId);
      loadBindings();
    } catch { /* */ }
  };

  const inputStyle: React.CSSProperties = {
    width: '100%', padding: '6px 10px',
    background: 'var(--color-bg-secondary)',
    border: '1px solid var(--color-border)',
    borderRadius: 4, color: 'var(--color-text)',
    fontSize: 12, boxSizing: 'border-box',
  };

  return (
    <div>
      {/* SendBlue */}
      <SendBlueSection
        agentId={agentId}
        binding={bindings.find((b) => b.channel_type === 'sendblue')}
        onDone={loadBindings}
        onRemove={(id) => { unbindAgentChannel(agentId, id).then(loadBindings).catch(() => {}); }}
      />

      {/* Other messaging channels */}
      {MESSAGING_CHANNELS.map((ch) => {
        const binding = bindings.find((b) => b.channel_type === ch.type);
        const cfg = (binding?.config || {}) as Record<string, unknown>;
        const isSetup = setupType === ch.type;
        const canConnect = ch.fields.every((f) => !f.required || formValues[f.key]?.trim());

        return (
          <div
            key={ch.type}
            style={{
              background: 'var(--color-bg-secondary)',
              border: binding ? '1px solid color-mix(in srgb, var(--color-success) 22%, transparent)' : '1px dashed var(--color-border)',
              borderRadius: 8, marginBottom: 10, overflow: 'hidden',
            }}
          >
            <div style={{ display: 'flex', alignItems: 'center', padding: '12px 14px' }}>
              <span style={{ fontSize: 18, marginRight: 10 }}>{ch.icon}</span>
              <div style={{ flex: 1 }}>
                <div style={{ fontWeight: 600, fontSize: 13 }}>{ch.name}</div>
                <div style={{
                  fontSize: 11,
                  color: binding ? 'var(--color-success)' : 'var(--color-text-secondary)',
                }}>
                  {binding ? ch.activeLabel(cfg) : ch.description}
                </div>
              </div>
              {binding ? (
                <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
                  <span style={{
                    background: 'color-mix(in srgb, var(--color-success) 22%, transparent)', color: 'var(--color-success)',
                    padding: '2px 8px', borderRadius: 10,
                    fontSize: 10, fontWeight: 600,
                  }}>Active</span>
                  <button
                    onClick={() => handleRemove(binding.id)}
                    style={{
                      fontSize: 10, padding: '2px 8px', background: 'transparent',
                      color: 'var(--color-text-secondary)',
                      border: '1px solid var(--color-border)',
                      borderRadius: 4, cursor: 'pointer',
                    }}
                  >Remove</button>
                </div>
              ) : (
                <button
                  onClick={() => { setSetupType(isSetup ? null : ch.type); setFormValues({}); }}
                  style={{
                    fontSize: 10, padding: '3px 12px', background: 'var(--color-accent-purple)',
                    color: 'var(--color-on-accent)', border: 'none', borderRadius: 5,
                    cursor: 'pointer', fontWeight: 600,
                  }}
                >{isSetup ? 'Cancel' : 'Set Up'}</button>
              )}
            </div>

            {binding && (
              <div style={{
                borderTop: '1px solid var(--color-border)',
                padding: '10px 14px', background: 'var(--color-bg)',
              }}>
                <div style={{ fontSize: 11, color: 'var(--color-text-secondary)', display: 'flex', alignItems: 'flex-start', gap: 6 }}>
                  <span style={{ flexShrink: 0 }}>{'\u2192'}</span>
                  <span>{ch.howToUse(cfg)}</span>
                </div>
              </div>
            )}

            {isSetup && (
              <div style={{
                borderTop: '1px solid var(--color-border)',
                padding: 14, background: 'var(--color-bg)',
              }}>
                <div style={{
                  fontSize: 11, lineHeight: 1.5,
                  color: 'var(--color-text-secondary)',
                  marginBottom: 12, padding: '8px 10px',
                  background: 'var(--color-bg-secondary)',
                  borderRadius: 6,
                  borderLeft: '3px solid var(--color-accent, var(--color-accent-purple))',
                }}>
                  {ch.setupSteps.map((s, i) => {
                    if (s.startsWith('COPYABLE:')) {
                      const text = s.slice(9);
                      return (
                        <div key={i} style={{ marginBottom: 6, marginTop: 4 }}>
                          <div style={{
                            position: 'relative',
                            background: 'var(--color-bg)',
                            border: '1px solid var(--color-border)',
                            borderRadius: 4, padding: '8px 10px',
                            fontSize: 10, fontFamily: 'monospace',
                            wordBreak: 'break-all', lineHeight: 1.4,
                            maxHeight: 80, overflowY: 'auto',
                          }}>
                            {text}
                            <button
                              onClick={() => { navigator.clipboard.writeText(text); }}
                              style={{
                                position: 'sticky', float: 'right', top: 0,
                                fontSize: 10, padding: '2px 8px',
                                background: 'var(--color-accent-purple)', color: 'var(--color-on-accent)',
                                border: 'none', borderRadius: 3,
                                cursor: 'pointer', fontWeight: 600,
                              }}
                            >Copy</button>
                          </div>
                        </div>
                      );
                    }
                    return (
                      <div key={i} style={{ marginBottom: i < ch.setupSteps.length - 1 ? 4 : 0 }}>{s}</div>
                    );
                  })}
                </div>
                {ch.fields.map((field) => (
                  <div key={field.key} style={{ marginBottom: 8 }}>
                    <label style={{
                      display: 'block', fontSize: 11,
                      color: 'var(--color-text-secondary)',
                      marginBottom: 3, fontWeight: 500,
                    }}>
                      {field.label}{field.required ? ' *' : ''}
                    </label>
                    <input
                      type={field.type || 'text'}
                      value={formValues[field.key] || ''}
                      onChange={(e) => setField(field.key, e.target.value)}
                      placeholder={field.placeholder}
                      style={inputStyle}
                    />
                  </div>
                ))}
                <button
                  onClick={() => handleSetup(ch)}
                  disabled={loading || !canConnect}
                  style={{
                    fontSize: 12, padding: '7px 20px', background: 'var(--color-accent-purple)',
                    color: 'var(--color-on-accent)', border: 'none', borderRadius: 5,
                    cursor: 'pointer', fontWeight: 600,
                    opacity: loading || !canConnect ? 0.5 : 1, marginTop: 4,
                  }}
                >{loading ? 'Connecting...' : 'Connect'}</button>
              </div>
            )}
          </div>
        );
      })}
    </div>
  );
}

// ---------------------------------------------------------------------------
// Memory section
// ---------------------------------------------------------------------------

function MemorySection() {
  const [stats, setStats] = useState<MemoryStats | null>(null);
  const [statsError, setStatsError] = useState('');

  // Search
  const [searchQuery, setSearchQuery] = useState('');
  const [searchResults, setSearchResults] = useState<MemorySearchResult[]>([]);
  const [searching, setSearching] = useState(false);
  const [searchDone, setSearchDone] = useState(false);

  // Index
  const [indexPath, setIndexPath] = useState('');
  const [indexing, setIndexing] = useState(false);
  const [indexResult, setIndexResult] = useState('');
  const [indexError, setIndexError] = useState('');

  // Store
  const [storeContent, setStoreContent] = useState('');
  const [storing, setStoring] = useState(false);
  const [storeResult, setStoreResult] = useState('');
  const [storeError, setStoreError] = useState('');

  const statsInterval = useRef<ReturnType<typeof setInterval> | null>(null);

  const loadStats = useCallback(() => {
    getMemoryStats()
      .then((s) => { setStats(s); setStatsError(''); })
      .catch(() => setStatsError('Could not reach memory backend'));
  }, []);

  useEffect(() => {
    loadStats();
    statsInterval.current = setInterval(loadStats, 10000);
    return () => { if (statsInterval.current) clearInterval(statsInterval.current); };
  }, [loadStats]);

  const handleSearch = async () => {
    if (!searchQuery.trim()) return;
    setSearching(true);
    setSearchDone(false);
    try {
      const results = await searchMemory(searchQuery.trim());
      setSearchResults(results || []);
      setSearchDone(true);
    } catch {
      setSearchResults([]);
      setSearchDone(true);
    } finally {
      setSearching(false);
    }
  };

  const handleBrowse = async () => {
    if (isTauri()) {
      try {
        const { open } = await import('@tauri-apps/plugin-dialog');
        const selected = await open({ directory: true, multiple: false, title: 'Select folder to index' });
        if (selected) setIndexPath(selected as string);
        return;
      } catch {
        // fall through to browser picker
      }
    }
    const input = document.createElement('input');
    input.type = 'file';
    input.setAttribute('webkitdirectory', '');
    input.onchange = () => {
      const files = input.files;
      if (files && files.length > 0) {
        const rel = (files[0] as any).webkitRelativePath || '';
        const folder = rel.split('/')[0];
        if (folder) setIndexPath(folder);
      }
    };
    input.click();
  };

  const handleIndex = async () => {
    if (!indexPath.trim()) return;
    setIndexing(true);
    setIndexResult('');
    setIndexError('');
    try {
      const res = await indexMemoryPath(indexPath.trim());
      setIndexResult(`Indexed ${res.chunks_indexed} chunk${res.chunks_indexed !== 1 ? 's' : ''}`);
      setIndexPath('');
      loadStats();
    } catch (err: any) {
      setIndexError(err.message || 'Indexing failed');
    } finally {
      setIndexing(false);
    }
  };

  const handleStore = async () => {
    if (!storeContent.trim()) return;
    setStoring(true);
    setStoreResult('');
    setStoreError('');
    try {
      await storeMemory(storeContent.trim());
      setStoreResult('Stored successfully');
      setStoreContent('');
      loadStats();
    } catch (err: any) {
      setStoreError(err.message || 'Failed to store');
    } finally {
      setStoring(false);
    }
  };

  return (
    <div className="space-y-4">
      {/* Stats overview */}
      <div
        className="rounded-xl p-5 relative overflow-hidden"
        style={{ background: 'var(--color-surface)', border: '1px solid var(--color-border)' }}
      >
        {/* Subtle gradient accent along top edge */}
        <div className="absolute top-0 left-0 right-0 h-[2px]" style={{
          background: 'linear-gradient(90deg, var(--color-accent-purple), var(--color-accent), transparent)',
        }} />
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-9 h-9 rounded-lg flex items-center justify-center" style={{
              background: 'var(--color-accent-purple-subtle)',
            }}>
              <Brain size={18} style={{ color: 'var(--color-accent-purple)' }} />
            </div>
            <div>
              <h3 className="text-sm font-semibold" style={{ color: 'var(--color-text)' }}>Memory Backend</h3>
              {statsError ? (
                <p className="text-xs mt-0.5" style={{ color: 'var(--color-text-tertiary)' }}>{statsError}</p>
              ) : stats ? (
                <div className="flex items-center gap-2 mt-0.5">
                  <span className="w-1.5 h-1.5 rounded-full" style={{
                    background: stats.entries > 0 ? 'var(--color-success)' : 'var(--color-text-tertiary)',
                  }} />
                  <span className="text-xs" style={{ color: 'var(--color-text-secondary)' }}>
                    {stats.backend} &middot; {stats.entries.toLocaleString()} {stats.entries === 1 ? 'chunk' : 'chunks'}
                  </span>
                </div>
              ) : (
                <p className="text-xs mt-0.5" style={{ color: 'var(--color-text-tertiary)' }}>Connecting...</p>
              )}
            </div>
          </div>
          {stats && stats.entries > 0 && (
            <div className="text-right">
              <div className="text-lg font-bold tabular-nums" style={{ color: 'var(--color-text)' }}>
                {stats.entries.toLocaleString()}
              </div>
              <div className="text-[10px] uppercase tracking-wider" style={{ color: 'var(--color-text-tertiary)' }}>
                indexed
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Search */}
      <div
        className="rounded-xl p-5"
        style={{ background: 'var(--color-surface)', border: '1px solid var(--color-border)' }}
      >
        <div className="flex items-center gap-2 mb-3">
          <Search size={14} style={{ color: 'var(--color-accent-purple)' }} />
          <h3 className="text-sm font-semibold" style={{ color: 'var(--color-text)' }}>Search Memory</h3>
        </div>
        <div className="flex gap-2">
          <div className="flex-1 relative">
            <input
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              onKeyDown={(e) => { if (e.key === 'Enter') handleSearch(); }}
              placeholder="What are you looking for?"
              className="w-full text-sm px-3 py-2 rounded-lg outline-none transition-colors"
              style={{
                background: 'var(--color-bg)',
                border: '1px solid var(--color-border)',
                color: 'var(--color-text)',
              }}
            />
          </div>
          <button
            onClick={handleSearch}
            disabled={searching || !searchQuery.trim()}
            className="flex items-center gap-1.5 px-4 py-2 rounded-lg text-sm font-medium transition-all cursor-pointer whitespace-nowrap"
            style={{
              background: searching || !searchQuery.trim() ? 'var(--color-bg-tertiary)' : 'var(--color-accent-purple)',
              color: searching || !searchQuery.trim() ? 'var(--color-text-tertiary)' : 'var(--color-on-accent)',
              opacity: searching || !searchQuery.trim() ? 0.6 : 1,
            }}
          >
            {searching ? <Loader2 size={13} className="animate-spin" /> : <Search size={13} />}
            {searching ? 'Searching' : 'Search'}
          </button>
        </div>

        {/* Results */}
        {searchDone && searchResults.length === 0 && (
          <div className="flex flex-col items-center py-6 gap-2">
            <Search size={20} style={{ color: 'var(--color-text-tertiary)', opacity: 0.4 }} />
            <p className="text-xs" style={{ color: 'var(--color-text-tertiary)' }}>No matching memories found</p>
          </div>
        )}
        {searchResults.length > 0 && (
          <div className="mt-3 space-y-2">
            {searchResults.map((r, i) => (
              <div
                key={i}
                className="rounded-lg p-3 transition-colors"
                style={{
                  background: 'var(--color-bg)',
                  border: '1px solid var(--color-border)',
                }}
              >
                <p className="text-xs leading-relaxed" style={{ color: 'var(--color-text)' }}>
                  {r.content.length > 250 ? r.content.slice(0, 250) + '...' : r.content}
                </p>
                <div className="flex items-center gap-3 mt-2">
                  <span className="inline-flex items-center gap-1 px-1.5 py-0.5 rounded text-[10px] font-medium" style={{
                    background: r.score > 0.5
                      ? 'rgba(74, 222, 128, 0.1)'
                      : r.score > 0.2
                        ? 'var(--color-accent-amber-subtle)'
                        : 'var(--color-bg-tertiary)',
                    color: r.score > 0.5
                      ? 'var(--color-success)'
                      : r.score > 0.2
                        ? 'var(--color-warning)'
                        : 'var(--color-text-tertiary)',
                  }}>
                    {(r.score * 100).toFixed(0)}% match
                  </span>
                  {r.metadata?.source != null && (
                    <span className="text-[10px]" style={{ color: 'var(--color-text-tertiary)' }}>
                      {String(r.metadata.source)}
                    </span>
                  )}
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Add to Memory â€” two-column grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {/* Index folder */}
        <div
          className="rounded-xl p-5"
          style={{ background: 'var(--color-surface)', border: '1px solid var(--color-border)' }}
        >
          <div className="flex items-center gap-2 mb-3">
            <FolderOpen size={14} style={{ color: 'var(--color-accent-purple)' }} />
            <h3 className="text-sm font-semibold" style={{ color: 'var(--color-text)' }}>Index Folder</h3>
          </div>
          <p className="text-xs mb-3" style={{ color: 'var(--color-text-tertiary)' }}>
            Scan a folder and index all supported files into memory.
          </p>
          <div className="flex gap-2 mb-2">
            <input
              value={indexPath}
              onChange={(e) => setIndexPath(e.target.value)}
              placeholder="~/Documents/notes"
              className="flex-1 text-sm px-3 py-2 rounded-lg outline-none"
              style={{
                background: 'var(--color-bg)',
                border: '1px solid var(--color-border)',
                color: 'var(--color-text)',
              }}
            />
            {isTauri() && (
              <button
                onClick={handleBrowse}
                className="flex items-center gap-1.5 px-3 py-2 rounded-lg text-xs font-medium cursor-pointer transition-colors whitespace-nowrap"
                style={{
                  background: 'var(--color-bg)',
                  border: '1px solid var(--color-border)',
                  color: 'var(--color-text-secondary)',
                }}
              >
                <FolderOpen size={12} />
                Browse
              </button>
            )}
          </div>
          <button
            onClick={handleIndex}
            disabled={indexing || !indexPath.trim()}
            className="w-full flex items-center justify-center gap-1.5 py-2 rounded-lg text-sm font-medium cursor-pointer transition-all"
            style={{
              background: indexing || !indexPath.trim() ? 'var(--color-bg-tertiary)' : 'var(--color-accent-purple)',
              color: indexing || !indexPath.trim() ? 'var(--color-text-tertiary)' : 'var(--color-on-accent)',
              opacity: indexing || !indexPath.trim() ? 0.6 : 1,
            }}
          >
            {indexing && <Loader2 size={13} className="animate-spin" />}
            {indexing ? 'Indexing files...' : 'Index'}
          </button>
          {indexResult && (
            <p className="text-xs mt-2 font-medium" style={{ color: 'var(--color-success)' }}>{indexResult}</p>
          )}
          {indexError && (
            <p className="text-xs mt-2 font-medium" style={{ color: 'var(--color-error)' }}>{indexError}</p>
          )}
        </div>

        {/* Paste content */}
        <div
          className="rounded-xl p-5"
          style={{ background: 'var(--color-surface)', border: '1px solid var(--color-border)' }}
        >
          <div className="flex items-center gap-2 mb-3">
            <FileText size={14} style={{ color: 'var(--color-accent-purple)' }} />
            <h3 className="text-sm font-semibold" style={{ color: 'var(--color-text)' }}>Store Text</h3>
          </div>
          <p className="text-xs mb-3" style={{ color: 'var(--color-text-tertiary)' }}>
            Paste any text to add directly to your memory store.
          </p>
          <textarea
            value={storeContent}
            onChange={(e) => setStoreContent(e.target.value)}
            placeholder="Paste or type content here..."
            rows={4}
            className="w-full text-sm px-3 py-2 rounded-lg outline-none resize-y"
            style={{
              background: 'var(--color-bg)',
              border: '1px solid var(--color-border)',
              color: 'var(--color-text)',
              fontFamily: 'inherit',
              minHeight: 80,
              marginBottom: 8,
            }}
          />
          <button
            onClick={handleStore}
            disabled={storing || !storeContent.trim()}
            className="w-full flex items-center justify-center gap-1.5 py-2 rounded-lg text-sm font-medium cursor-pointer transition-all"
            style={{
              background: storing || !storeContent.trim() ? 'var(--color-bg-tertiary)' : 'var(--color-accent-purple)',
              color: storing || !storeContent.trim() ? 'var(--color-text-tertiary)' : 'var(--color-on-accent)',
              opacity: storing || !storeContent.trim() ? 0.6 : 1,
            }}
          >
            {storing && <Loader2 size={13} className="animate-spin" />}
            {storing ? 'Storing...' : 'Store'}
          </button>
          {storeResult && (
            <p className="text-xs mt-2 font-medium" style={{ color: 'var(--color-success)' }}>{storeResult}</p>
          )}
          {storeError && (
            <p className="text-xs mt-2 font-medium" style={{ color: 'var(--color-error)' }}>{storeError}</p>
          )}
        </div>
      </div>
    </div>
  );
}

// ---------------------------------------------------------------------------
// Main page
// ---------------------------------------------------------------------------

export function DataSourcesPage() {
  const [agents, setAgents] = useState<ManagedAgent[]>([]);
  const [activeTab, setActiveTab] = useState<'sources' | 'messaging' | 'memory'>('sources');
  const [creatingAgent, setCreatingAgent] = useState(false);

  const loadAgents = useCallback(() => {
    fetchManagedAgents().then(setAgents).catch(() => {});
  }, []);

  useEffect(() => { loadAgents(); }, [loadAgents]);

  // Pick the first agent for messaging channel bindings.
  // If none exists and user opens Messaging tab, auto-create a default one.
  const firstAgent = agents[0];

  const ensureAgent = useCallback(async (): Promise<string | null> => {
    if (firstAgent) return firstAgent.id;
    setCreatingAgent(true);
    try {
      const agent = await createManagedAgent({
        name: "My Assistant",
        template_id: "personal_deep_research",
      });
      setAgents((prev) => [...prev, agent]);
      return agent.id;
    } catch {
      return null;
    } finally {
      setCreatingAgent(false);
    }
  }, [firstAgent]);

  // Auto-create agent when switching to messaging tab
  useEffect(() => {
    if (activeTab === 'messaging' && !firstAgent && !creatingAgent) {
      ensureAgent();
    }
  }, [activeTab, firstAgent, creatingAgent, ensureAgent]);

  const tabs = [
    { id: 'sources' as const, label: 'Data Sources', icon: Database },
    { id: 'messaging' as const, label: 'Messaging Channels', icon: MessageSquare },
    { id: 'memory' as const, label: 'Memory', icon: Brain },
  ];

  return (
    <div className="flex-1 overflow-y-auto px-6 py-10">
      <div className="max-w-5xl mx-auto">
      <header className="mb-6">
        <h1 className="text-lg font-semibold" style={{ color: 'var(--color-text)' }}>
          Data Sources, Channels &amp; Memory
        </h1>
        <p className="text-sm mt-2 max-w-2xl" style={{ color: 'var(--color-text-secondary)' }}>
          Connect personal data so the assistant can search across everything, and set up messaging channels to chat from your phone.
        </p>
      </header>

      <div
        className="flex gap-1 mb-6"
        style={{ borderBottom: '1px solid var(--color-border)' }}
      >
        {tabs.map((tab) => {
          const isActive = activeTab === tab.id;
          return (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className="relative px-4 py-2.5 text-sm transition-colors cursor-pointer"
              style={{
                color: isActive ? 'var(--color-text)' : 'var(--color-text-secondary)',
                fontWeight: isActive ? 600 : 400,
              }}
            >
              {tab.label}
              {isActive && (
                <motion.span
                  layoutId="data-sources-tab-indicator"
                  className="absolute left-0 right-0 -bottom-px h-[2px]"
                  style={{ background: 'var(--color-text)' }}
                  transition={{ type: 'spring', stiffness: 380, damping: 30 }}
                />
              )}
            </button>
          );
        })}
      </div>

      <div>
        {activeTab === 'sources' && <DataSourcesSection />}
        {activeTab === 'messaging' && (
          firstAgent ? (
            <MessagingSection agentId={firstAgent.id} />
          ) : creatingAgent ? (
            <div className="flex items-center gap-3 p-4 text-sm" style={{ color: 'var(--color-text-secondary)' }}>
              <Loader2 size={16} className="animate-spin" style={{ color: 'var(--color-accent)' }} />
              Setting up your assistant...
            </div>
          ) : null
        )}
        {activeTab === 'memory' && <MemorySection />}
      </div>
      </div>
    </div>
  );
}


## ===== frontend/src/pages/SettingsPage.tsx : OUR COMMITS SINCE AUTHOR BASE =====
525ccde6 W66: explicit audio output endpoint selection (setSinkId) - closes the silent-output fault class
bc498a16 feat: Arc Reactor ThinkingCircle, fix env loading, fix project root, add research types, remove debug code
f2fcb30c Graystone Lab: remote MCP/Ollama integration, Rust extension, UI fixes

## ===== frontend/src/pages/SettingsPage.tsx : CONFLICTED WORKING FILE (diff3) =====
import { useState, useEffect, useCallback } from 'react';
import {
  Sun,
  Moon,
  Monitor,
  Download,
  Upload,
  Trash2,
  Check,
  Key,
  Brain,
<<<<<<< ours
  Server,
  Volume2,
||||||| base
=======
  RefreshCw,
>>>>>>> theirs
} from 'lucide-react';
import { useAppStore, type ThemeMode } from '../lib/store';
<<<<<<< ours
import { checkHealth, getMemoryStats } from '../lib/api';
import {
  isSinkSelectionSupported,
  isEnumerationSupported,
  requestDeviceLabels,
  listAudioOutputs,
  getSavedSinkId,
  type AudioOutputDevice,
} from '../lib/audioOutput';
import { setOutputDevice } from '../audio/ttsPlayer';
||||||| base
import { checkHealth, fetchSpeechHealth, getMemoryStats } from '../lib/api';
=======
import {
  checkHealth,
  fetchSpeechHealth,
  getMemoryStats,
  getInferenceSource,
  setInferenceSource,
  getCloudKeyStatus,
  saveCloudKey,
  fetchToolCredentialStatus,
  saveToolCredentials,
  deleteToolCredential,
  isTauri,
  type InferenceSource,
} from '../lib/api';
import { isAutoUpdateDisabled, setAutoUpdateDisabled } from '../components/Desktop/UpdateChecker';

const CLOUD_KEY_STATUS_CHANGED = 'openjarvis-cloud-key-status-changed';
>>>>>>> theirs

function Section({ title, children }: { title: string; children: React.ReactNode }) {
  return (
    <div
      className="rounded-xl p-5"
      style={{ background: 'var(--color-surface)', border: '1px solid var(--color-border)' }}
    >
      <h3 className="text-sm font-semibold mb-4" style={{ color: 'var(--color-text)' }}>
        {title}
      </h3>
      {children}
    </div>
  );
}

function SettingRow({ label, description, children }: { label: string; description?: string; children: React.ReactNode }) {
  return (
    <div className="flex items-center justify-between py-3" style={{ borderBottom: '1px solid var(--color-border-subtle)' }}>
      <div>
        <div className="text-sm" style={{ color: 'var(--color-text)' }}>{label}</div>
        {description && (
          <div className="text-xs mt-0.5" style={{ color: 'var(--color-text-tertiary)' }}>{description}</div>
        )}
      </div>
      <div>{children}</div>
    </div>
  );
}

function ApiKeyInput({
  keyName,
  placeholder,
  toolName,
}: {
  keyName: string;
  placeholder: string;
  toolName?: string;
}) {
  const [value, setValue] = useState('');
  const [saved, setSaved] = useState(false);
  const [hasKey, setHasKey] = useState(false);
  const [error, setError] = useState('');
  const desktopKeyStorage = isTauri();
  const serverToolStorage = !desktopKeyStorage && !!toolName;
  const canManage = desktopKeyStorage || serverToolStorage;

  const refresh = useCallback(async () => {
    if (!canManage) {
      setHasKey(false);
      return;
    }
    try {
      const status = desktopKeyStorage
        ? await getCloudKeyStatus()
        : await fetchToolCredentialStatus(toolName!);
      setHasKey(!!status[keyName]);
    } catch {
      setHasKey(false);
    }
  }, [canManage, desktopKeyStorage, keyName, toolName]);

  useEffect(() => {
    void refresh();
    window.addEventListener(CLOUD_KEY_STATUS_CHANGED, refresh);
    return () => window.removeEventListener(CLOUD_KEY_STATUS_CHANGED, refresh);
  }, [refresh]);

  const save = async (v: string) => {
    const next = v.trim();
    if (!next) return;
    setError('');
    try {
      if (desktopKeyStorage) {
        await saveCloudKey(keyName, next);
      } else if (toolName) {
        await saveToolCredentials(toolName, { [keyName]: next });
      } else {
        return;
      }
      setValue('');
      setHasKey(true);
      setSaved(true);
      window.dispatchEvent(new Event(CLOUD_KEY_STATUS_CHANGED));
      setTimeout(() => setSaved(false), 2000);
    } catch (e: any) {
      setError(e?.message || 'Failed to save API key');
    }
  };

  const remove = async () => {
    setError('');
    try {
      if (desktopKeyStorage) {
        await saveCloudKey(keyName, '');
      } else if (toolName) {
        await deleteToolCredential(toolName, keyName);
      } else {
        return;
      }
      setValue('');
      setHasKey(false);
      setSaved(true);
      window.dispatchEvent(new Event(CLOUD_KEY_STATUS_CHANGED));
      setTimeout(() => setSaved(false), 2000);
    } catch (e: any) {
      setError(e?.message || 'Failed to remove API key');
    }
  };

  return (
    <div className="flex items-center gap-2">
      <input
        type="password"
        value={value}
        onChange={e => setValue(e.target.value)}
        onBlur={() => { if (value.trim()) void save(value); }}
        placeholder={hasKey ? (desktopKeyStorage ? 'Saved in secure storage' : 'Saved by local server') : placeholder}
        disabled={!canManage}
        className="w-48 px-2 py-1 rounded text-xs"
        style={{ background: 'var(--color-bg)', border: '1px solid var(--color-border)', color: 'var(--color-text)' }} />
      {hasKey && (
        <button
          onClick={() => void remove()}
          className="px-2 py-1 rounded text-[10px] cursor-pointer"
          style={{ color: 'var(--color-error)', border: '1px solid var(--color-error)' }}
        >
          Remove
        </button>
      )}
      {saved && <span className="text-[10px]" style={{ color: 'var(--color-success)' }}>Saved</span>}
      {error && <span className="text-[10px]" style={{ color: 'var(--color-error)' }}>{error}</span>}
    </div>
  );
}

function CloudProviderStatus({ label, keyName }: { label: string; keyName: string }) {
  const [hasKey, setHasKey] = useState(false);
  const desktopKeyStorage = isTauri();

  const refresh = useCallback(async () => {
    if (!desktopKeyStorage) {
      setHasKey(false);
      return;
    }
    try {
      const status = await getCloudKeyStatus();
      setHasKey(!!status[keyName]);
    } catch {
      setHasKey(false);
    }
  }, [desktopKeyStorage, keyName]);

  useEffect(() => {
    void refresh();
    window.addEventListener(CLOUD_KEY_STATUS_CHANGED, refresh);
    return () => window.removeEventListener(CLOUD_KEY_STATUS_CHANGED, refresh);
  }, [refresh]);

  return (
    <span className="flex items-center gap-1 text-xs" style={{ color: 'var(--color-text-secondary)' }}>
      <span style={{
        width: 6, height: 6, borderRadius: '50%', display: 'inline-block',
        background: hasKey ? 'var(--color-success)' : 'var(--color-text-tertiary)',
      }} />
      {label}
    </span>
  );
}

const themeOptions: { value: ThemeMode; label: string; icon: typeof Sun }[] = [
  { value: 'light', label: 'Light', icon: Sun },
  { value: 'dark', label: 'Dark', icon: Moon },
  { value: 'system', label: 'System', icon: Monitor },
];

export function SettingsPage() {
  const settings = useAppStore((s) => s.settings);
  const updateSettings = useAppStore((s) => s.updateSettings);
  const serverInfo = useAppStore((s) => s.serverInfo);
  const [healthy, setHealthy] = useState<boolean | null>(null);
  const [saved, setSaved] = useState(false);
<<<<<<< ours
||||||| base

=======

  const [autoUpdateEnabled, setAutoUpdateEnabled] = useState(() => !isAutoUpdateDisabled());
  const [updateCheckState, setUpdateCheckState] = useState<'idle' | 'checking' | 'available' | 'latest'>('idle');

  const handleAutoUpdateToggle = useCallback((enabled: boolean) => {
    setAutoUpdateEnabled(enabled);
    setAutoUpdateDisabled(!enabled);
  }, []);

  const handleCheckNow = useCallback(async () => {
    if (!(window as any).__TAURI_INTERNALS__) return;
    setUpdateCheckState('checking');
    try {
      const { check } = await import('@tauri-apps/plugin-updater');
      const update = await check();
      setUpdateCheckState(update ? 'available' : 'latest');
      setTimeout(() => setUpdateCheckState('idle'), 4000);
    } catch {
      setUpdateCheckState('idle');
    }
  }, []);

>>>>>>> theirs
  const [memoryStats, setMemoryStats] = useState<{ entries: number; backend: string } | null>(null);
  const [memoryEnabled, setMemoryEnabled] = useState(() => {
    try { return localStorage.getItem('openjarvis-memory-enabled') !== 'false'; } catch { return true; }
  });
  const [confirmClear, setConfirmClear] = useState(false);

<<<<<<< ours
  /* Audio output endpoint selection - see lib/audioOutput.ts for why. */
  const [audioDevices, setAudioDevices] = useState<AudioOutputDevice[]>([]);
  const [sinkId, setSinkId] = useState<string>(() => getSavedSinkId());
  const [audioProbe, setAudioProbe] = useState<string>('Not checked yet');
  const [labelsUnlocked, setLabelsUnlocked] = useState(false);
||||||| base
  useEffect(() => {
    checkHealth().then(setHealthy);
    fetchSpeechHealth()
      .then((h) => setSpeechBackendAvailable(h.available))
      .catch(() => setSpeechBackendAvailable(false));
    getMemoryStats()
      .then(setMemoryStats)
      .catch(() => setMemoryStats(null));
  }, []);
=======
  const [srcKind, setSrcKind] = useState<InferenceSource['kind']>('ollama');
  const [customHost, setCustomHost] = useState('http://localhost:1234/v1');
  const [customModel, setCustomModel] = useState('');
  const [customEngine, setCustomEngine] = useState('lmstudio');
  const [customKey, setCustomKey] = useState('');
  const [srcMsg, setSrcMsg] = useState('');

  useEffect(() => {
    getInferenceSource().then((s) => {
      setSrcKind(s.kind);
      if (s.host) setCustomHost(s.host);
      if (s.model) setCustomModel(s.model);
      if (s.engine) setCustomEngine(s.engine);
    }).catch(() => {});
  }, []);

  const saveSource = useCallback(async () => {
    try {
      if (srcKind === 'custom') {
        await setInferenceSource({ kind: 'custom', host: customHost, model: customModel, engine: customEngine, apiKey: customKey || undefined });
      } else {
        await setInferenceSource({ kind: 'ollama' });
      }
      setSrcMsg('Saved â€” restart the app to apply.');
    } catch (e: any) {
      setSrcMsg(e?.message ?? 'Failed to save.');
    }
  }, [srcKind, customHost, customModel, customEngine, customKey]);

  useEffect(() => {
    checkHealth().then(setHealthy);
    fetchSpeechHealth()
      .then((h) => setSpeechBackendAvailable(h.available))
      .catch(() => setSpeechBackendAvailable(false));
    getMemoryStats()
      .then(setMemoryStats)
      .catch(() => setMemoryStats(null));
  }, []);
>>>>>>> theirs

  const showSaved = () => {
    setSaved(true);
    setTimeout(() => setSaved(false), 1500);
  };

  useEffect(() => {
    checkHealth().then(ok => setHealthy(ok));
    getMemoryStats().then(stats => setMemoryStats(stats)).catch(() => setMemoryStats(null));
  }, []);

  /*
   * On-screen capability readout. The webview console is unreadable without a
   * CDP opt-in, so this line IS the instrument: it reports setSinkId support,
   * how many audiooutput endpoints were found, and whether their labels came
   * back named or blank.
   */
  const probeAudio = async (unlockLabels: boolean) => {
    const sinkOk = isSinkSelectionSupported();
    const enumOk = isEnumerationSupported();
    if (!enumOk) {
      setAudioProbe('setSinkId=' + sinkOk + ' | enumerateDevices UNAVAILABLE');
      setAudioDevices([]);
      return;
    }
    let granted = labelsUnlocked;
    if (unlockLabels && !granted) {
      granted = await requestDeviceLabels();
      setLabelsUnlocked(granted);
    }
    const devices = await listAudioOutputs();
    setAudioDevices(devices);
    const named = devices.filter((d) => d.label && d.label.trim().length > 0).length;
    setAudioProbe(
      'setSinkId=' + sinkOk +
      ' | endpoints=' + devices.length +
      ' | named=' + named +
      (granted ? ' | labels unlocked' : ' | labels LOCKED (click Detect)')
    );
  };

  useEffect(() => {
    void probeAudio(false);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  /*
   * setOutputDevice persists the choice AND retargets the live AudioContext, so
   * a device change takes effect immediately. Before this, selection was
   * persist-only and needed an app relaunch to be picked up at context
   * creation - which is how W66's device test had to be run.
   */
  const handleSinkChange = (id: string) => {
    setSinkId(id);
    void setOutputDevice(id);
    showSaved();
  };

  const handleExport = () => {
    const data = localStorage.getItem('openjarvis-conversations') || '{}';
    const blob = new Blob([data], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `openjarvis-export-${new Date().toISOString().slice(0, 10)}.json`;
    a.click();
    URL.revokeObjectURL(url);
  };

  const handleImport = () => {
    const input = document.createElement('input');
    input.type = 'file';
    input.accept = '.json';
    input.onchange = (e) => {
      const file = (e.target as HTMLInputElement).files?.[0];
      if (!file) return;
      const reader = new FileReader();
      reader.onload = (ev) => {
        try {
          const data = JSON.parse(ev.target?.result as string);
          if (data.version === 1) {
            localStorage.setItem('openjarvis-conversations', JSON.stringify(data));
            useAppStore.getState().loadConversations();
            showSaved();
          }
        } catch {}
      };
      reader.readAsText(file);
    };
    input.click();
  };

  const handleClear = () => {
    if (!confirmClear) {
      setConfirmClear(true);
      setTimeout(() => setConfirmClear(false), 3000);
      return;
    }
    localStorage.removeItem('openjarvis-conversations');
    useAppStore.getState().loadConversations();
    setConfirmClear(false);
    showSaved();
  };

  return (
    <div className="flex-1 overflow-y-auto px-6 py-10">
      <div className="max-w-2xl mx-auto">
        <header className="mb-6">
          <div className="flex items-center justify-between gap-3">
            <h1 className="text-lg font-semibold" style={{ color: 'var(--color-text)' }}>
              Settings
            </h1>
            {saved && (
              <span className="flex items-center gap-1 text-xs px-2 py-1 rounded-full" style={{
                background: 'var(--color-accent-subtle)',
                color: 'var(--color-success)',
              }}>
                <Check size={12} /> Saved
              </span>
            )}
          </div>
          <p className="text-sm mt-2 max-w-2xl" style={{ color: 'var(--color-text-secondary)' }}>
            App preferences - appearance, model defaults, keyboard shortcuts, and data management.
          </p>
        </header>

        <div className="flex flex-col gap-4">
          <Section title="Appearance">
            <SettingRow label="Theme" description="Choose how OpenJarvis looks">
              <div className="flex gap-1 p-0.5 rounded-lg" style={{ background: 'var(--color-bg-secondary)' }}>
                {themeOptions.map((opt) => {
                  const isActive = settings.theme === opt.value;
                  return (
                    <button
                      key={opt.value}
                      onClick={() => { updateSettings({ theme: opt.value }); showSaved(); }}
                      className="flex items-center gap-1.5 px-3 py-1.5 rounded-md text-xs font-medium transition-colors cursor-pointer"
                      style={{
                        background: isActive ? 'var(--color-surface)' : 'transparent',
                        color: isActive ? 'var(--color-text)' : 'var(--color-text-tertiary)',
                        boxShadow: isActive ? 'var(--shadow-sm)' : 'none',
                      }}
                    >
                      <opt.icon size={14} />
                      {opt.label}
                    </button>
                  );
                })}
              </div>
            </SettingRow>
            <SettingRow label="Font size">
              <select
                value={settings.fontSize}
                onChange={(e) => { updateSettings({ fontSize: e.target.value as any }); showSaved(); }}
                className="text-sm px-3 py-1.5 rounded-lg outline-none cursor-pointer"
                style={{
                  background: 'var(--color-bg-secondary)',
                  color: 'var(--color-text)',
                  border: '1px solid var(--color-border)',
                }}
              >
                <option value="small">Small</option>
                <option value="default">Default</option>
                <option value="large">Large</option>
              </select>
            </SettingRow>
          </Section>

          <Section title="Audio Output">
            <SettingRow
              label="Speech output device"
              description="Where Jarvis speaks. Default follows Windows, which can silently select a phantom endpoint."
            >
              <select
                value={sinkId}
                onChange={(e) => handleSinkChange(e.target.value)}
                className="text-sm px-3 py-1.5 rounded-lg outline-none cursor-pointer w-64"
                style={{
                  background: 'var(--color-bg-secondary)',
                  color: 'var(--color-text)',
                  border: '1px solid var(--color-border)',
                }}
              >
                <option value="">System default</option>
                {audioDevices.map((d, i) => (
                  <option key={d.deviceId || i} value={d.deviceId}>
                    {d.label || `Endpoint ${i + 1} (unnamed)`}
                  </option>
                ))}
              </select>
            </SettingRow>
            <SettingRow label="Detect devices" description={audioProbe}>
              <button
                onClick={() => { void probeAudio(true); }}
                className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-medium cursor-pointer transition-colors"
                style={{
                  background: 'var(--color-bg-secondary)',
                  color: 'var(--color-text)',
                  border: '1px solid var(--color-border)',
                }}
              >
                <Volume2 size={14} />
                Detect
              </button>
            </SettingRow>
          </Section>

          <Section title="Connection">
            <SettingRow label="Server status" description={serverInfo ? `${serverInfo.engine} / ${serverInfo.model}` : 'Not connected'}>
              <div className="flex items-center gap-2">
                <span
                  className="w-2 h-2 rounded-full"
                  style={{ background: healthy === true ? 'var(--color-success)' : healthy === false ? 'var(--color-error)' : 'var(--color-text-tertiary)' }}
                />
                <span className="text-xs" style={{ color: 'var(--color-text-secondary)' }}>
                  {healthy === true ? 'Connected' : healthy === false ? 'Disconnected' : 'Checking...'}
                </span>
              </div>
            </SettingRow>
            <SettingRow label="API URL" description="Set if backend runs on a different port or host">
              <input
                type="text"
                value={settings.apiUrl}
                onChange={(e) => { updateSettings({ apiUrl: e.target.value }); showSaved(); }}
                placeholder="http://localhost:8000"
                className="text-sm px-3 py-1.5 rounded-lg outline-none w-56"
                style={{
                  background: 'var(--color-bg-secondary)',
                  color: 'var(--color-text)',
                  border: '1px solid var(--color-border)',
                }}
              />
            </SettingRow>
            <SettingRow label="API key" description="Required only if the server was started with an API key">
              <input
                type="password"
                value={settings.apiKey}
                onChange={(e) => { updateSettings({ apiKey: e.target.value }); showSaved(); }}
                placeholder="OPENJARVIS_API_KEY"
                autoComplete="off"
                className="text-sm px-3 py-1.5 rounded-lg outline-none w-56"
                style={{
                  background: 'var(--color-bg-secondary)',
                  color: 'var(--color-text)',
                  border: '1px solid var(--color-border)',
                }}
              />
            </SettingRow>
          </Section>

          {/* Inference source */}
          <Section title="Inference source">
            <SettingRow label="Source" description="Where the app runs models. Applies after restart.">
              <select
                value={srcKind}
                onChange={(e) => { setSrcKind(e.target.value as InferenceSource['kind']); setSrcMsg(''); }}
                className="text-sm px-3 py-1.5 rounded-lg outline-none w-56"
                style={{ background: 'var(--color-bg-secondary)', color: 'var(--color-text)', border: '1px solid var(--color-border)' }}
              >
                <option value="ollama">Bundled Ollama (default)</option>
                <option value="custom">Custom OpenAI-compatible server</option>
              </select>
            </SettingRow>
            {srcKind === 'custom' && (
              <>
                <SettingRow label="Server URL" description="e.g. LM Studio: http://localhost:1234/v1">
                  <input type="text" value={customHost} onChange={(e) => { setCustomHost(e.target.value); setSrcMsg(''); }} placeholder="http://localhost:1234/v1"
                    className="text-sm px-3 py-1.5 rounded-lg outline-none w-56"
                    style={{ background: 'var(--color-bg-secondary)', color: 'var(--color-text)', border: '1px solid var(--color-border)' }} />
                </SettingRow>
                <SettingRow label="Model" description="Model id served by your endpoint">
                  <input type="text" value={customModel} onChange={(e) => { setCustomModel(e.target.value); setSrcMsg(''); }} placeholder="qwen2.5-7b-instruct"
                    className="text-sm px-3 py-1.5 rounded-lg outline-none w-56"
                    style={{ background: 'var(--color-bg-secondary)', color: 'var(--color-text)', border: '1px solid var(--color-border)' }} />
                </SettingRow>
                <SettingRow label="Server type" description="OpenAI-compatible engine">
                  <select value={customEngine} onChange={(e) => { setCustomEngine(e.target.value); setSrcMsg(''); }}
                    className="text-sm px-3 py-1.5 rounded-lg outline-none w-56"
                    style={{ background: 'var(--color-bg-secondary)', color: 'var(--color-text)', border: '1px solid var(--color-border)' }}>
                    <option value="lmstudio">LM Studio</option>
                    <option value="vllm">vLLM</option>
                    <option value="sglang">SGLang</option>
                    <option value="llamacpp">llama.cpp</option>
                    <option value="mlx">MLX</option>
                  </select>
                </SettingRow>
                <SettingRow label="API key (optional)" description="Only if your server requires one">
                  <input type="password" value={customKey} onChange={(e) => { setCustomKey(e.target.value); setSrcMsg(''); }} placeholder="leave blank if none"
                    className="text-sm px-3 py-1.5 rounded-lg outline-none w-56"
                    style={{ background: 'var(--color-bg-secondary)', color: 'var(--color-text)', border: '1px solid var(--color-border)' }} />
                </SettingRow>
              </>
            )}
            <SettingRow label="" description={srcMsg}>
              <button onClick={saveSource}
                className="text-sm px-3 py-1.5 rounded-lg outline-none cursor-pointer"
                style={{ background: 'var(--color-accent, var(--color-bg-tertiary))', color: 'var(--color-text)', border: '1px solid var(--color-border)' }}>
                Save inference source
              </button>
            </SettingRow>
          </Section>

          <Section title="Cloud Providers">
            <SettingRow label="Status" description="Green dot means API key is configured">
              <div className="flex flex-wrap gap-3">
                <CloudProviderStatus label="OpenAI" keyName="OPENAI_API_KEY" />
                <CloudProviderStatus label="Anthropic" keyName="ANTHROPIC_API_KEY" />
                <CloudProviderStatus label="Google" keyName="GEMINI_API_KEY" />
                <CloudProviderStatus label="OpenRouter" keyName="OPENROUTER_API_KEY" />
              </div>
            </SettingRow>
          </Section>

          <Section title="API Keys">
            <SettingRow label="OpenAI" description="GPT-4, GPT-3.5, etc.">
              <ApiKeyInput keyName="OPENAI_API_KEY" placeholder="sk-..." />
            </SettingRow>
            <SettingRow label="Anthropic" description="Claude models">
              <ApiKeyInput keyName="ANTHROPIC_API_KEY" placeholder="sk-ant-..." />
            </SettingRow>
            <SettingRow label="Google" description="Gemini models">
              <ApiKeyInput keyName="GEMINI_API_KEY" placeholder="AI..." />
            </SettingRow>
            <SettingRow label="OpenRouter" description="Multi-provider routing">
              <ApiKeyInput keyName="OPENROUTER_API_KEY" placeholder="sk-or-..." />
            </SettingRow>
          </Section>

<<<<<<< ours
||||||| base
          {/* Tools */}
          <Section title="Tools">
            <SettingRow label="Web Search" description="SerpAPI or Tavily key for web search tool">
              <ApiKeyInput storageKey="openjarvis-search-key" placeholder="API key..." />
            </SettingRow>
          </Section>

          {/* Memory */}
=======
          {/* Tools */}
          <Section title="Tools">
            <SettingRow label="Web Search" description="Tavily key for web search tool">
              <ApiKeyInput keyName="TAVILY_API_KEY" placeholder="tvly-..." toolName="web_search" />
            </SettingRow>
          </Section>

          {/* Memory */}
>>>>>>> theirs
          <Section title="Memory">
            <SettingRow label="Memory status" description={memoryStats ? `${memoryStats.backend} backend - ${memoryStats.entries} entries` : 'Unable to reach memory service'}>
              <div className="flex items-center gap-2">
                <Brain size={14} style={{ color: memoryStats ? 'var(--color-accent)' : 'var(--color-text-tertiary)' }} />
                <span className="text-xs" style={{ color: 'var(--color-text-secondary)' }}>
                  {memoryStats ? `${memoryStats.entries} entries` : 'Unavailable'}
                </span>
              </div>
            </SettingRow>
            <SettingRow label="Use memory context" description="Automatically inject relevant memories into conversations">
              <button
                onClick={() => {
                  const next = !memoryEnabled;
                  setMemoryEnabled(next);
                  try { localStorage.setItem('openjarvis-memory-enabled', String(next)); } catch {}
                  showSaved();
                }}
                className="relative w-11 h-6 rounded-full transition-colors cursor-pointer"
                style={{
                  background: memoryEnabled ? 'var(--color-accent)' : 'var(--color-bg-tertiary)',
                }}
              >
                <span
                  className="absolute top-0.5 w-5 h-5 rounded-full transition-transform bg-white"
                  style={{
                    left: memoryEnabled ? 'calc(100% - 22px)' : '2px',
                  }}
                />
              </button>
            </SettingRow>
          </Section>

          <Section title="Data">
            <SettingRow label="Export conversations" description="Download all chats as JSON">
              <button
                onClick={handleExport}
                className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-medium cursor-pointer transition-colors"
                style={{
                  background: 'var(--color-bg-secondary)',
                  color: 'var(--color-text)',
                  border: '1px solid var(--color-border)',
                }}
              >
                <Download size={14} />
                Export
              </button>
            </SettingRow>
            <SettingRow label="Import conversations" description="Restore from a backup file">
              <button
                onClick={handleImport}
                className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-medium cursor-pointer transition-colors"
                style={{
                  background: 'var(--color-bg-secondary)',
                  color: 'var(--color-text)',
                  border: '1px solid var(--color-border)',
                }}
              >
                <Upload size={14} />
                Import
              </button>
            </SettingRow>
            <SettingRow label="Clear all data" description="Permanently delete all conversations">
              <button
                onClick={handleClear}
                className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-medium cursor-pointer transition-colors"
                style={{
                  background: confirmClear ? 'var(--color-error)' : 'var(--color-bg-secondary)',
                  color: confirmClear ? 'white' : 'var(--color-error)',
                  border: `1px solid ${confirmClear ? 'var(--color-error)' : 'var(--color-border)'}`,
                }}
              >
                <Trash2 size={14} />
                {confirmClear ? 'Click again to confirm' : 'Clear All'}
              </button>
            </SettingRow>
          </Section>
<<<<<<< ours
||||||| base

          {/* About */}
          <Section title="About">
            <div className="text-sm" style={{ color: 'var(--color-text-secondary)' }}>
              <p className="mb-2">
                <span className="font-semibold" style={{ color: 'var(--color-text)' }}>OpenJarvis</span> â€” Programming abstractions for on-device AI.
              </p>
              <p className="text-xs" style={{ color: 'var(--color-text-tertiary)' }}>
                Part of Intelligence Per Watt, a research initiative at Stanford SAIL.
              </p>
              <div className="flex gap-3 mt-3 text-xs">
                <a
                  href="https://scalingintelligence.stanford.edu/blogs/openjarvis/"
                  target="_blank"
                  rel="noopener noreferrer"
                  style={{ color: 'var(--color-accent)' }}
                >
                  Project site
                </a>
                <a
                  href="https://open-jarvis.github.io/OpenJarvis/"
                  target="_blank"
                  rel="noopener noreferrer"
                  style={{ color: 'var(--color-accent)' }}
                >
                  Documentation
                </a>
              </div>
            </div>
          </Section>
=======

          {/* Updates */}
          <Section title="Updates">
            <SettingRow label="Auto-update" description="Check for new desktop builds automatically every 30 minutes">
              <button
                onClick={() => handleAutoUpdateToggle(!autoUpdateEnabled)}
                className="relative inline-flex h-5 w-9 items-center rounded-full transition-colors"
                style={{ background: autoUpdateEnabled ? 'var(--color-accent)' : 'var(--color-bg-tertiary)', border: '1px solid var(--color-border)' }}
              >
                <span
                  className="inline-block h-3.5 w-3.5 rounded-full transition-transform"
                  style={{
                    background: 'white',
                    transform: autoUpdateEnabled ? 'translateX(18px)' : 'translateX(2px)',
                  }}
                />
              </button>
            </SettingRow>
            <SettingRow label="Check for updates" description="Manually check for a new version right now">
              <button
                onClick={handleCheckNow}
                className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-medium transition-colors"
                style={{ background: 'var(--color-bg-tertiary)', border: '1px solid var(--color-border)', color: 'var(--color-text)', cursor: 'pointer' }}
                disabled={updateCheckState === 'checking'}
              >
                <RefreshCw size={12} className={updateCheckState === 'checking' ? 'animate-spin' : ''} />
                {updateCheckState === 'checking' && 'Checking...'}
                {updateCheckState === 'available' && 'Update available â€” see banner above'}
                {updateCheckState === 'latest' && 'Already up to date'}
                {updateCheckState === 'idle' && 'Check now'}
              </button>
            </SettingRow>
          </Section>

          {/* About */}
          <Section title="About">
            <div className="text-sm" style={{ color: 'var(--color-text-secondary)' }}>
              <p className="mb-2">
                <span className="font-semibold" style={{ color: 'var(--color-text)' }}>OpenJarvis</span> â€” Programming abstractions for on-device AI.
              </p>
              <p className="text-xs" style={{ color: 'var(--color-text-tertiary)' }}>
                Part of Intelligence Per Watt, a research initiative at Stanford SAIL.
              </p>
              <div className="flex gap-3 mt-3 text-xs">
                <a
                  href="https://openjarvis.stanford.edu/"
                  target="_blank"
                  rel="noopener noreferrer"
                  style={{ color: 'var(--color-accent)' }}
                >
                  Project site
                </a>
                <a
                  href="https://open-jarvis.github.io/OpenJarvis/"
                  target="_blank"
                  rel="noopener noreferrer"
                  style={{ color: 'var(--color-accent)' }}
                >
                  Documentation
                </a>
              </div>
            </div>
          </Section>
>>>>>>> theirs
        </div>
      </div>
    </div>
  );
}


## ===== frontend/vite.config.ts : OUR COMMITS SINCE AUTHOR BASE =====
b76b1b13 fix(ui): coerce object tool/arguments fields to string + remove PWA service worker (resolves React #31 stale-bundle boot crash)
e0e36523 Fix: wire tools to native_openhands agent - file_read, think, calculator, code_interpreter, shell_exec, file_write now loading at startup
bc498a16 feat: Arc Reactor ThinkingCircle, fix env loading, fix project root, add research types, remove debug code

## ===== frontend/vite.config.ts : CONFLICTED WORKING FILE (diff3) =====
import path from 'path';
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import tailwindcss from '@tailwindcss/vite';

// VITE_SUPABASE_ANON_KEY is intentionally NOT required here: a missing key
// disables the savings leaderboard at runtime (see src/lib/supabase.ts) rather
// than failing the build, so the package/app stays publishable without it.
export default defineConfig({
  resolve: {
    alias: {
      '@': path.resolve(import.meta.dirname, './src'),
    },
  },
  plugins: [
    react(),
    tailwindcss(),

  ],
  build: {
    outDir: '../src/openjarvis/server/static',
    emptyOutDir: true,
<<<<<<< ours
    sourcemap: true,
    minify: 'esbuild',
    rollupOptions: {
||||||| base
    minify: 'esbuild',
    rollupOptions: {
=======
    // Preserve the Vite 6 browser baseline for existing desktop webviews.
    target: ['es2020', 'edge88', 'firefox78', 'chrome87', 'safari14'],
    rolldownOptions: {
>>>>>>> theirs
      output: {
        codeSplitting: {
          groups: [
            { name: 'react', test: /node_modules[\\/](react|react-dom)[\\/]/ },
            {
              name: 'markdown',
              test: /node_modules[\\/](react-markdown|rehype-highlight|remark-gfm)[\\/]/,
            },
            { name: 'charts', test: /node_modules[\\/]recharts[\\/]/ },
            { name: 'router', test: /node_modules[\\/]react-router[\\/]/ },
          ],
        },
      },
    },
  },
  server: {
    port: 5173,
    proxy: {
<<<<<<< ours
      '/v1': process.env.VITE_API_URL || 'http://localhost:8010',
      '/health': process.env.VITE_API_URL || 'http://localhost:8010',
||||||| base
      '/v1': process.env.VITE_API_URL || 'http://localhost:8000',
      '/health': process.env.VITE_API_URL || 'http://localhost:8000',
      '/api': process.env.VITE_API_URL || 'http://localhost:8000',
=======
      // ws: true is required for the /v1/agents/events WebSocket. Without it
      // Vite proxies the HTTP request but not the upgrade, so the socket never
      // opens â€” no error, no close event, just silence â€” and every live agent
      // view sits empty in dev while working in a production build.
      '/v1': {
        target: process.env.VITE_API_URL || 'http://localhost:8000',
        changeOrigin: true,
        ws: true,
      },
      '/health': process.env.VITE_API_URL || 'http://localhost:8000',
      '/api': process.env.VITE_API_URL || 'http://localhost:8000',
>>>>>>> theirs
    },
  },
});

