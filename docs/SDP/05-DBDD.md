# VOL 5 - DATABASE DESIGN DESCRIPTION (DBDD)
Governing DID: DI-IPSC-81437 (verify, GAP-002). v0.2 DRAFT 2026-09-23 (W82), W83 update 2026-09-24 (memory.db schema, memory.db.old, config [memory]; content cleaned, NUL-free guarantee, memory stores). Harvest of W42-W83.
Plain language: this volume lists every place Jarvis keeps information on disk - what is in it, who writes it, who reads it,
and whether it holds anything sensitive. Schemas not yet read are marked as gaps rather than guessed.

## 1. DATASTORES AND CONFIGURATION ITEMS
| Store | Location | Format | Contents | Writer / reader | Sensitivity | In git | Grade |
|---|---|---|---|---|---|---|---|
| config.toml | C:\Users\Admin\.openjarvis\config.toml | TOML, UTF-8 NO BOM (tomllib rejects BOM), CRLF | [engine] (num_ctx, default, disabled "vllm,uzu,lemonade,litellm"), [engine.ollama] host, [intelligence], [memory] (no backend key -> sqlite default; context_top_k 5, context_min_score 0.0, context_max_tokens 2048 = author defaults since W83, D-24), [agent] tools (13 names incl web_search), [security], [analytics] enabled=false, [server] host "0.0.0.0", [speech] | owner / load_config (lru_cached, restart to reload); OPENJARVIS_CONFIG can redirect | low | NO (H-W80-7) | [M W80, W82] |
| cloud-keys.env | C:\Users\Admin\.openjarvis\cloud-keys.env | KEY=VALUE text | OPENROUTER_API_KEY (sk-or-, 73 chars); Anthropic/Gemini empty | UI Cloud Models tab / cloud_router._load_keys every request | SECRET | NO | [M W43] |
| IMAP credentials | C:\Users\Admin\.openjarvis\connectors\imap_mail_<account>.json | JSON {email, password, provider, [host]} plaintext | family mail credentials | setup_mailbox_account.py / mailbox_tools load_tokens, connector_for | SECRET | NO | [R W61] |
| protected_senders.json | C:\Users\Admin\.openjarvis\protected_senders.json | JSON array of strings, UTF-8 (BOM tolerated) | senders never trashed | owner / mailbox_tools | PII | NO | [R W61] |
| memory.db | C:\Users\Admin\.openjarvis\memory.db (405 KB) | SQLite via Rust SQLiteMemory; tables documents(id TEXT PK, content TEXT, source TEXT, metadata TEXT JSON, created_at REAL = JULIAN DAY, not epoch) + documents_fts FTS5(content, source, tokenize porter unicode61) and its 5 shadow tables | W83 close: 3 documents - owner EA notes (S-05, 2 chunks) and the BLUEHERON memory_store test fact; 113 test chunks removed 4ee2053 (snapshot evidence\W83\backup\memory.db.snap-20260924_171031); stored text NUL-free since D-29 (0 NUL rows measured); metadata {chunk_index, doc_id, doc_type, title}; memory_store rows carry empty source | upload ingest / memory tools, context injection, /v1/memory/* | today test data; intended family data | NO | [M W83 memdb-inventory.txt, author-intent-context.txt] |
| memory.db.old | C:\Users\Admin\.openjarvis\memory.db.old | SQLite | pre-cutover corpus, 21,356,789,760 bytes, last write 2026-07-18 | none (retained) | may hold family data | NO | [M W83]; retention condition: ingester fix + one real ingestion cycle (not met) - do not delete |
| agents.db | ~\.openjarvis (per W72) | SQLite | managed agents (8), 901 messages, 14 learning-log rows | agent manager | personal agent data | NO | [M W72] |
| telemetry.db | C:\Users\Admin\.openjarvis\telemetry.db | SQLite | one row per MODEL call (engine, model, timing); no tool columns | InstrumentedEngine | low | NO | [M W77] |
| traces.db | ~\.openjarvis | SQLite | 0 traces ([traces] disabled; trace modules deleted H-W73-TRACELOST) | - | - | NO | [M W72-W73] |
| knowledge.db | ~\.openjarvis | SQLite | knowledge_chunks (deep research) | DR tools; knowledge_sql limited to knowledge_chunks by SQLite authorizer (2fb87cf) | depends on ingested data | NO | [M W55] |
| scheduler.db | absent | - | operators never run | - | - | - | [M W72] |
| Workspace (scratch pad) | C:\Users\Admin\.openjarvis\workspace | files | only location file_write may write (D-14) | file_write | variable | NO | [M W78] |
| MEMORY.md | ~\.openjarvis\MEMORY.md | Markdown | memory_manage store - SEPARATE from memory.db, not synchronized | memory_manage (loaded W83, D-26) | owner notes | NO | [M W83] seeded c792038 (author default), 64 bytes after P2 (AMBERFINCH test note); since 6429769 ALSO in every chat prompt as "## Agent Memory" (D-36, cap 2500 chars); holds the user notes by N1 routing (D-37) |
| Persona files | ~\.openjarvis\SOUL.md, MEMORY.md, USER.md, skills\ | Markdown | persona and memory notes | jarvis init / memory_manage | personal | NO | [R W82 init_cmd] | W83: SOUL.md 69 B and USER.md 18 B seeded with author defaults (D-32); no reader of SOUL.md; USER.md read only by user_profile_manage (not loaded) | W83 later: SOUL.md carries the N1 routing line; USER.md "preferred name is Gray" (P4); SOUL and USER in every chat prompt (D-36) |
| Logs | %LOCALAPPDATA%\OpenJarvis\logs\ backend.log (10 MiB x4), dispatch.log (2 MB x4), agent.log (2.5 MiB x4), engine.log (2 MiB x2) | text UTF-8 | runtime records; backend.log via SanitizingFormatter (credential stripper) | loggers (Vol 4 section 11) | may hold prompts/args digests | NO | [M W45, W52] |
| cli.log | ~\.openjarvis\cli.log | text | only with --verbose | log_config | - | NO | [R W45] |
| .env (repo) | C:\Users\Admin\OpenJarvis\.env | dotenv | GITLAB_URL, WIKI_JS_URL and others; lines malformed (H-W79-DOTENV); loaded twice | CLI | may hold secrets - never print | git-ignored (verify) | [M W79-W80] |
| Environment variables | Process/User/Machine scopes | - | OLLAMA_HOST (3 scopes), OPENJARVIS_OLLAMA_HOST (Process/User, no reader), OPENJARVIS_LOG_LEVEL (launcher), OPENJARVIS_CONFIRM_INTERACTIVE (default on), OPENJARVIS_CONFIRM_TTL, OPENJARVIS_TEST_EXEC | owner / backend | low | NO | [M W80, R] |
| Rollback copies | *.bak-* beside sources and in evidence\W8x\backup | copies | prior versions | patch harnesses | same as source | git-ignored (.gitignore line 20) | [M v0.1] |

## 2. OPEN
memory.db schema RECORDED W83 (row above). Schemas, retention and access units for agents.db, telemetry.db, knowledge.db: GAP-017. Encryption at rest: none
recorded for any store (feeds Vol 7 SC-28).
