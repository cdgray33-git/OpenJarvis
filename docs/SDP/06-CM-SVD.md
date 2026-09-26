# VOL 6 - CONFIGURATION MANAGEMENT PLAN, BASELINE, VERSION DESCRIPTION
Governing: NIST SP 800-53 CM family; SVD per DI-IPSC-81442 (verify). v0.2 DRAFT 2026-09-23 (W82).
Plain language: this is the change diary. It says what the starting point was, what was changed and when, and how to undo each change.

## 1. CHANGE CONTROL [S/M]
- Every change is a commit pushed to BOTH remotes: `origin` = GitHub, `gitlab` = lab (naming is a known trap). Plain `git push`,
  never --mirror. Stage explicit paths from `git ls-files`, never `git add -A`.
- A patch and its commit are separate blocks; commit only after live end-to-end verification (owner 09/22). Every change is
  backed up first (evidence\W8x\backup), verified in isolation, and gets an AO-grade record (W81 s5.1 pattern).
- Owner decisions carry a risk assessment (author intent, effects, risks) before the decision (owner 09/23).
- `.gitignore` line 20 excludes *.bak-*; line 23 `*.txt` silently drops .txt evidence at git add (H-W74-GITIGNORE) - use -f.
- CRLF working copy, LF in repo: git's CRLF->LF warning is expected.

## 2. BASELINE AND PROVENANCE
- Author baseline: upstream open-jarvis/OpenJarvis commit af21bc18 (2026-05-19), the author's last commit before the 05/30
  clone; found W73 by per-commit diff count against f2fcb30, verified by ancestry [M W73]. All HEAD-vs-base changes classified
  (PROVENANCE-W73-classified.csv) and justified (docs\SDP\evidence\W74\R06-W74-JUSTIFY.csv, 133 rows) [M W74].
- f2fcb30 (2026-05-30) is the first GRAYSTONE commit and already mixes author and Graystone code; git blame cannot separate them.
  Author intent statements must diff against af21bc18 in the local upstream clone (W82 correction: W81 s5.1 part 3 compared
  against upstream MAIN and must be re-grounded).
- Upstream main has moved since: security fixes #415 (template-loader RCE), #416 (WebSocket/A2A auth), #417 (default deploy auth)
  post-date the base (H-W73-BEHIND). Upstream is a catalog of enhancements to borrow, not a sync target (owner W82).
- Files measured IDENTICAL to af21bc18 in W82: cli\init_cmd.py, cli\model.py, connectors\embeddings.py,
  tools\storage\embeddings.py, agents\scheduler.py, agents\executor.py, agents\manager.py, workflow\engine.py.
  agents\orchestrator.py differs only by the W77 text-call fallback (64b0660).

## 3. CONFIGURATION ITEMS OUTSIDE GIT (CM-2 gap)
config.toml; cloud-keys.env; connectors\imap_mail_*.json; protected_senders.json; env vars OLLAMA_HOST (3 scopes),
OPENJARVIS_OLLAMA_HOST (2 scopes, no reader); Python 3.12.10 pin (Python312); the installed desktop exe. Rebuilding from the
repo alone misses all of these (GAP-041, new).

## 4. VERSION DESCRIPTION (commits recorded in the harvest; full W1+ history GAP-018)
| Commit | Window | Change |
|---|---|---|
| f2fcb30 | 05/30 | Graystone root: remote MCP/Ollama integration, Rust extension, UI fixes |
| b4cbd81 | W43 | logging: openjarvis tree at INFO into backend.log (env dial, 40 MB, SanitizingFormatter) |
| 2fb87cf | W55 | knowledge_sql SQLite authorizer (knowledge_chunks only) |
| cd2d1db | W62 | console QuickEdit off in start script |
| 8728267 | W62 | console, audio and CDP instruments |
| 0389255 | pre-W69 | send flow and AbortController moved to ChatArea |
| e0e3652 | pre-W79 | port 8010; also moved vllm/uzu/lemonade defaults (self-loop source); history holds bundle_for_cloud_model.txt (H-W79-E0E3652) |
| cc21932, 63257bd, e5b35c9 | W70-W71 | stream probe, ChatArea liveness probe, W71 handoff |
| a72d2c6 | W71 | SDP v0.1 (10 volumes) |
| fb05108 | W74 | Track 0 closed, R0.6 justification evidence |
| 6a555c6 | W75 | RTM v0.3 ratified |
| b6556ac | W76 | RTM v0.4, Vol 3A v0.2 |
| 64b0660 | W77 | shared text tool-call parser, dedupe, RQ-021 VERIFIED, Vol 3A v0.3 |
| 7fe51ac, 12a1f8f | W78 | RTM row restore; RTM v0.6 class table |
| 829cea7 | W78 | file_write confinement (D-14) |
| 854b9c7 | W78 | single _build_agent_tools, CHANNEL_ASSERT (D-15) |
| a0704c4 | W79 | engine turn-down list (D-16) |
| 0da22e8 | W81 | cloud_router host order config > env > raise (F1a) |
| e79a11c | W82 | SDP v0.2 harvest of ARCHIVE-W42..W81 |
| (this) | W82 | H5: remove Graystone /transcribe and /health from speech_router.py (author routes serve; mic dump removed); SDP rows updated. Backup evidence\W82\backup\speech_router.py.bak-W82-H5-20260923_213342 |
| 955fe451 | W91 | main: W91 closeout (frontend decisions, BRIEF-W92) |
| 533f9bfe | W90-W92 | upgrade/a6dcf846: MERGE author a6dcf846 (parents 3df27c53, a6dcf846); backend W90, frontend Method B W92 (SDD 20.8) |
| ac33e27f | W92 | upgrade/a6dcf846: remove 36 tracked frontend backup copies (C-W91-3, C-W92-2) |
| 8eda697d | W92 | upgrade/a6dcf846: uv.lock re-lock; STT pins ctranslate2 4.8.0, av 17.1.0 (W92-D5) |
| 0dd22107 | W92 | upgrade/a6dcf846: .python-version 3.12 + labeled .gitignore exception (W92-D6) |
| 6c9a2bc3 | W92 | upgrade/a6dcf846: fix author defect AD-W92-1 (Tauri plugin crates aligned with npm) |
| 93f96395 | W92 | upgrade/a6dcf846: tauri.conf Graystone values restored - frontendDist, updater off (W92-D7) |
| 13dbd764 | W93 | upgrade/a6dcf846 (gitlab only): POAM-67 site A - ConfirmPolicy site=managed-agent-tool restored verbatim on stream_tool_executor (SDD 20.9) |
| 6edfe885 | W93 | upgrade/a6dcf846 (gitlab only): POAM-67 site B - skills pipeline_executor real terminal gate SkillPipelineConfirmGate site=cli-ask-skill |
| da752fbd | W93 | upgrade/a6dcf846 (gitlab only): POAM-67 sites C+D - agent ask --yes attributed (cli-agent-ask-yes); agent ask --no-yes, skill run, chat use TerminalConfirmGate with recorded decision; site= keyword; dead chat _confirm removed |
| e9acdacd | W93 | upgrade/a6dcf846 (gitlab only): POAM-68 part 1 - core/log_paths.get_log_dir; backend, engine, agent, dispatch logs follow OPENJARVIS_HOME; code_interpreter fallback via get_config_dir (SDD 20.10) |
| 70a74188 | W93 | upgrade/a6dcf846 (gitlab only): POAM-68 part 2 - lib.rs OPENJARVIS_PORT (default 8010, 19 sites) and openjarvis_home() at 4 sites (AD-W93-1); 4 Rust unit tests; cargo test --lib 51/51 |
Also recorded without hash in the harvest: W46 dispatch-outcome wrapper, W51-W52 test-execute argument guard, W54 toolkit bind,
W56 ConfirmPolicy, W58 argument-aware gate, W59 prose-approval removal, W61 protected senders v2 and CLI gate, W63 CDP removal,
W66-W68 audio fixes, W69 stop button. Hash each at GAP-018.

## 5. ROLLBACK POINTS (current)
F1a: `git revert 0da22e8` or copy evidence\W81\backup\cloud_router.py.bak-W81-F1a-20260923_130442 over
src\openjarvis\server\cloud_router.py, restart, confirm START time. D-16: `git revert a0704c4` (+ .bak_w79disable files).
Config: config.toml.bak-W80-D03-20260923_110839. Unused W82 backup: evidence\W82\backup\init_cmd.py.bak-W82-F1b-20260923_192841.
Older points: openjarvis-rollback registers (W56-W80 valid per BRIEF W82).
W92 upgrade branch (not pushed; production untouched). Abandon the upgrade: git worktree remove --force
C:\Users\Admin\OpenJarvis-upgrade, then git branch -D upgrade/a6dcf846 (the replace ref was already deleted at 533f9bfe).
Undo one commit on the branch: git -C C:\Users\Admin\OpenJarvis-upgrade revert <hash>. Method B result and tooling:
evidence\W92\W92-methodB-sandbox-result.zip (DB38CD7E...61C5C3). Author tags are local refs only (git tag -d to remove).
W93 (upgrade branch, gitlab only): undo one POAM-67 site with git -C C:\Users\Admin\OpenJarvis-upgrade revert 13dbd764 | 6edfe885 |
da752fbd. Pre-patch copies: evidence\W93\bak\agent_manager_routes.py.W93-pre-A.bak, ask.py.W93-pre-B.bak,
{ask,agent_cmd,skill_cmd,chat_cmd}.py.W93-pre-CD.bak. Evidence logs evidence\W93\step*.log; harness log
evidence\W93\harness\OpenJarvis\logs\dispatch.log.
W93 POAM-68: undo with git -C C:\Users\Admin\OpenJarvis-upgrade revert 70a74188 (Rust) or e9acdacd (Python; also removes
core\log_paths.py). Pre-patch copies: evidence\W93\bak\*.W93-pre-logs.bak (serve, ollama, native_openhands, _stubs,
code_interpreter) and evidence\W93\bak\lib.rs.W93-pre-port-home.bak. Patch script evidence\W93\W93-rustpatch.py
(SHA256 b91eef5b...). Harness home evidence\W93\harness-home (test artifacts only).
