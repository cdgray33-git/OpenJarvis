# Graystone vs author install baseline - W76 2026-09-22

OPENJARVIS_HOME=[] XDG_DATA_HOME=[] OPENJARVIS_CONFIG=[]
config.toml at author default: True
  cfg: [engine]
  cfg: default = "ollama"
  cfg: [intelligence]
  cfg: default_model = "qwen3-coder:30b"
  cfg: [memory]
  cfg: [agent]
  cfg: context_from_memory = true
  cfg: default_agent = "native_openhands"
  cfg: tools = "code_interpreter,file_read,file_write,shell_exec,think,calculator,retrieval,mailbox_list_accounts,mailbox_usage_report,mailbox_find_messages,mailbox_move_to_trash,mailbox_empty_folder"
  cfg: [security]
  cfg: mode = "warn"
  cfg: [analytics]
  cfg: enabled = false
  cfg: [server]
  cfg: host = "0.0.0.0"
  cfg: port = 8010
  cfg: agent = "native_openhands"
  cfg: [speech]
  cfg: model = "base"
author native src (%LOCALAPPDATA%\OpenJarvis\src): False
repo deploy\windows\jarvis-service.ps1: False
scheduled tasks matching jarvis: none
venv python: Python 3.12.10
uv on PATH: uv 0.11.11 (ed7b06001 2026-05-06 x86_64-pc-windows-msvc)
rust extension (openjarvis_rust*): openjarvis_rust, openjarvis_rust-0.1.0.dist-info

## upstream last-commit dates (real freshness)
  docs/getting-started/install.md : 2026-09-04 18:03:57 -0400
  docs/getting-started/installation.md : 2026-06-20 17:08:24 -0700
  docs/getting-started/windows-native.md : 2026-07-01 13:02:13 -0700
  docs/getting-started/configuration.md : 2026-09-21 15:37:48 -0400
  docs/testing/agent-qa-runbook.md : 2026-03-16 21:05:37 -0700
