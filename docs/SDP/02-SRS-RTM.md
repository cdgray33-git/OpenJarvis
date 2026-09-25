# VOL 2 - SOFTWARE REQUIREMENTS SPECIFICATION (SRS) AND TRACEABILITY MATRIX
Governing DID: DI-IPSC-81433 (verify, GAP-002). v0.3 RATIFIED (W75, 2026-09-22). v0.4 (W76): section 4 two-tier, section 5 baseline 0/28. v0.5 (W77): first VERIFIED rows (RQ-022, RQ-030); requirements unchanged since W75. v0.7 (W83): R1 qualification ruling; RQ-024 and RQ-031 assessed. v0.8 (W83): RQ-024 VERIFIED by owner ruling, 4/28.
v0.1 (W72) seeded RQ-001..004. v0.2 adds RQ-005..031 recovered from the pre-OpenJarvis
executive-assistant artifacts (R1.1). Design mapping is R1.2; verification is R1.3.

STATUS: REQUIREMENTS BASELINE RATIFIED BY OWNER 2026-09-22 (W75). GAP-020 CLOSED.
CORE (Phase 1): 29 rows. RQ-003 is a rollup, so 28 rows are measured.
PHASE 2 (supporting roles, deferred by owner): RQ-023, RQ-027, RQ-032, RQ-033. W83: PULLED FORWARD by owner (D-39) to test and tune the persona with MS Office.
Owner ruling: document creation, diagrams, and similar output are supporting roles that
enhance the assistant; they are not core and are built in a later phase.

Grade key: [S] owner-stated. [R] read from a named source artifact this window.
[M] measured on the running system. No inferred rows.

## 1. SCOPE
The functional executive assistant: performs at a computer the duties a human executive
assistant would, for the owner and family users (RQ-003).

## 2. REFERENCED DOCUMENTS (requirement sources)
| Src | Artifact (C:\Users\Admin\Downloads unless noted) | Date | Bytes | sha256 (first 16) | What it is |
|---|---|---|---|---|---|
| S-01 | Executive Assistant Functions.txt | 2025-11-30 | 43663 | bd6aa8f735a11168 | n8n parent agent + Email, Contact, Content, Calendar sub-agents (Ollama variant) |
| S-02 | Ultimate Executive Assistant (Ollama).json | 2025-12-28 | 13044 | bec5dea6507c6e81 | n8n parent: Gmail/Yahoo email and calendar split, structured action API, owner-named |
| S-03 | Executive Assistant - Mac.txt | 2025-12-18 | 21756 | 70485e52f28dcebb | Mac installer v1: Docker stack (Ollama, function API, Open WebUI) |
| S-04 | install_executive_assistant_mac_v16.sh | 2026-01-15 | 32142 | 367c662453bb6688 | Mac installer v16: adds multi-account IMAP/SMTP, dictation UI |
| S-05 | executive assistant notes.txt | 2026-04-13 | 1009 | ae92775b286abf3c | Owner architecture note: multi-step orchestration chain |
| S-06 | executive assistant.pdf | 2025-11-26 | 44799 | not hashed (content pasted) | n8n workflows, OpenAI-model variant of S-01; full Email Agent node set |
| S-07 | Owner statements (memory, W1-W74) | various | - | - | [S] rows |

Provenance note: S-01, S-03 (n8n parts) and S-06 are adapted from a public n8n template
(author credited in the prompts). S-02 re-addresses it to the owner, which is the owner's
adoption of that capability set. Excluded: "New build before my requirements document.docx"
(sha 66ae74d77ebbc995) is a Proxmox lab build, not an EA source (W75 negative result).

## 3. REQUIREMENTS
### 3.1 Owner-stated (v0.1)
| Req ID | Requirement | Source | Grade |
|---|---|---|---|
| RQ-001 | Voice conversation: talk to Jarvis, Jarvis talks back (requirement one). Includes dictation input (S-04) | S-07, S-04 | [S] |
| RQ-002 | Manage mailboxes by natural language (family use case) | S-07 08/11 | [S] |
| RQ-003 | Perform the computer duties of a human executive assistant | S-07 09/06 | [S] |
| RQ-004 | Visible, interruptible replies (stream and stop) | W69-W71 | [S] |
### 3.2 Email
| Req ID | Requirement | Source | Grade |
|---|---|---|---|
| RQ-005 | Retrieve recent or unread mail, filtered by count, sender, date | S-01 S-02 S-04 S-06 | [R] |
| RQ-006 | Send email | S-01 S-02 S-04 S-06 | [R] |
| RQ-007 | Create a draft | S-01 S-06 | [R] |
| RQ-008 | Reply to a specific message (lookup first for message id) | S-01 S-06 | [R] |
| RQ-009 | Label, flag, categorize mail; list available labels | S-06, S-07 | [R] |
| RQ-010 | Mark read / unread | S-04 S-06 | [R] |
| RQ-011 | Multiple accounts and providers (Gmail, Yahoo, Hotmail, Apple, Outlook, SMTP send) | S-02 S-04, S-07 | [R]+[S] Hotmail added by owner 09/22 |
| RQ-012 | Human approval before a send | S-07 | [S] |
### 3.3 Contacts
| Req ID | Requirement | Source | Grade |
|---|---|---|---|
| RQ-013 | Search / get contacts | S-01 S-02 S-03 S-04 | [R] |
| RQ-014 | Add / update contacts | S-01 S-03 S-04 | [R] |
| RQ-015 | Resolve recipient from contacts before send, draft, or invite | S-01 S-02 | [R] |
### 3.4 Calendar
| Req ID | Requirement | Source | Grade |
|---|---|---|---|
| RQ-016 | Get events for a date range (default next 7 days) | S-01 S-02 S-03 S-04 | [R] |
| RQ-017 | Create event, solo or with attendees (default 1 hour) | S-01 S-02 S-03 S-04 | [R] |
| RQ-018 | Update event (lookup first for event id) | S-01 S-06 | [R] |
| RQ-019 | Delete event (lookup first for event id) | S-01 S-06 | [R] |
| RQ-020 | Multiple calendar providers (Gmail, Yahoo) | S-02 | [R] |
### 3.5 Research, content, notes
| Req ID | Requirement | Source | Grade |
|---|---|---|---|
| RQ-021 | Web search | S-01 S-02 S-03 S-04 | [R] |
| RQ-022 | Calculator | S-01 S-02 | [R] |
| RQ-024 | Notes: take, get, list | S-03 S-04 | [R] |
| RQ-025 | Summarize text | S-03 S-04 | [R] |
### 3.6 Orchestration and integrity
| Req ID | Requirement | Source | Grade |
|---|---|---|---|
| RQ-026 | Multi-step task chain: schedule meeting, get attendees, draft, send, calendar, notify | S-05 | [R] |
| RQ-028 | Verify own steps after every action before reporting completion | S-01 S-02 | [R] |
| RQ-029 | Structured action API alongside natural language | S-02 | [R] |
| RQ-030 | Local models (Ollama) as default inference | S-01 S-02 S-03 S-04 | [R] |
| RQ-031 | Recall prior conversations and actions; lessons-learned loop to repeatable actions | S-07 09/06 | [S] |

### 3.7 Phase 2 - supporting roles (deferred by owner 09/22, not core)
| Req ID | Requirement | Source | Grade |
|---|---|---|---|
| RQ-023 | Content creation (HTML, citations preserved as links) | S-01 S-02 S-06 | [R] |
| RQ-027 | Notify through a chat channel (Slack) | S-05 | [R] |
| RQ-032 | Create documents | S-07 09/22 | [S] |
| RQ-033 | Create diagrams (Visio and similar) | S-07 09/22 | [S] |

## 4. QUALIFICATION PROVISIONS
Two tiers, owner-approved W76 2026-09-22.
TIER A - author Agent QA Runbook, docs\testing\agent-qa-runbook.md (37 scenarios, 75 lines,
sha256 LF-normalized EFD739690939836A5E5262CD59BA9910DC47C3D29D7C89216DECFCBE715E0AFA,
unchanged upstream as of 09-21). PARTIAL SET ONLY:
  Direct (partial): RQ-005, 006, 008, 011 via Channel Gmail and Channel Email (SMTP/IMAP).
  Partial/indirect: RQ-021, 025 (CLI 3); RQ-031 (CLI 7, Desktop 7, Desktop 9); RQ-028 (Desktop 8).
  No core row: CLI 1,2,4,5,6,8,9,11,12; Desktop 1-6,10; Stress 1-7 (platform evidence for R1.2).
  Phase 2: CLI 10 and Channel Slack (RQ-027). Out of scope: iMessage, Twitter/X, Discord, Telegram, WhatsApp.
  Prerequisite conflicts with Graystone rules: desktop via npm run dev (use production build),
  qwen3:8b model, manual click steps (automate before use as evidence).
TIER B - Graystone acceptance test per core row, written from the row text: non-interactive,
production build, one pass criterion each. First priority, the 20 rows with no Tier A coverage:
RQ-001, 002, 004, 007, 009, 010, 012, 013-020, 022, 024, 026, 029, 030.
A row is VERIFIED only when its full row text passes. Tier A evidence supplements, not substitutes.

## 5. REQUIREMENTS TRACEABILITY MATRIX
| Req ID | Design element (Vol 1/4) | Interface (Vol 3) | Test evidence | Status |
|---|---|---|---|---|
| RQ-001 | TTS: ttsPlayer.ts, ChatArea TTS driver | IF-03 | F-W71-VOICE-LATE open | PARTIAL |
| RQ-002 | imap_mail connector, mailbox_tools | TBD | 08/11 live usage report | PARTIAL |
| RQ-003 | Decomposed into RQ-005..031 | - | - | ROLLUP |
| RQ-004 | Path 1b, stream_bridge, Option A | IF-01 | stream_probe_w70 | OPEN (POAM-01) |
| RQ-021 | web_search tool; shared ToolUsingAgent text parser (textparse-v3) + [agent] tools config - Vol 3A C, F8 | SDK ask_full AND live server 8010 | W77: SDK tool_results [web_search] turns 2 (sdk-verify-after.json); server sourced World Bank/Statista answer (surfaceA-gdp.json) | VERIFIED |
| RQ-022 | calculator tool (ast-based) - Vol 3A C | SDK ask_full (Surface C) | W77 run 3: tool_results [calculator -> "5754.0" success], turns 2 - evidence\W77\sdk-verify.json | VERIFIED |
| RQ-024 | memory_store / memory_search / memory_retrieve (author tools, D-26) + author context injection (D-24, D-25) | IF-18, dispatch.log | W83: TAKE PASS - memory_store dispatch OUTCOME reason=OK, memory.db 115->116; GET PASS - reply 'BLUEHERON-7731' via injection; LIST FAIL - memory backend has no list operation, memory_search('stored notes') returned other documents (rq024-list-test.txt); W83 P2: LIST via author memory_manage DIRECTED PASS (read lists AMBERFINCH-5520, dispatch OK); UNDIRECTED ask FAILED (model unaware of notes, D-33). P3 wired persona (D-36); N1 (e25b7c0): UNDIRECTED take -> memory_manage OUTCOME OK + MEMORY.md, UNDIRECTED list names every note (framing caveat: memory_search called first). OWNER RULED VERIFIED W83 2026-09-24 (framing caveat recorded) | VERIFIED |
| RQ-031 | memory tools + context injection | IF-18 | W83: fact recall PASS (BLUEHERON); recall of prior conversations and actions NOT TESTED; lessons-learned loop NOT BUILT (enhancement list: self-learning, author learning package first) | PARTIAL |
| RQ-025 | llm tool, any agent - Vol 3A C | SDK ask_full (Surface C) | W77 run 3: tool_results EMPTY, turns 1, model answered directly - evidence\W77\sdk-verify.json | NOT VERIFIED (not delegated) |
| RQ-030 | Ollama engine, local-first default - Vol 3A C | engine gate, TCP 11434 | W77: engine=ollama telemetry 7118-7132; TCP peer 172.16.33.200:11434 (E3); jarvis model list - evidence\W77\model-list.txt, surface-probe.txt | VERIFIED |
| RQ-005..RQ-031 core (remaining 22) | TBD (R1.2) | TBD | TBD (R1.3) | NOT ASSESSED |
| RQ-032 | code_interpreter + python-docx/python-pptx/openpyxl (D-40..D-45); SOUL Office line (D-44) | dispatch.log, workspace files | W83 S3 re-run 3: 6/6 real .docx/.pptx/.xlsx from undirected family requests, 33/34 requested details machine-checked; open: G-3 delivery, G-10 self-verification (R2 false negative) | PARTIAL - owner ruling pending |
| RQ-023, 027, 033 | - | - | - | Phase 2, pulled forward W83 (D-39), not yet assessed |

PROGRESS BASELINE (W76, 2026-09-22, before any test run): VERIFIED 0/28.
PROGRESS (W77, 2026-09-22, after the parser + config fix): VERIFIED 3/28 - RQ-021, RQ-022, RQ-030.
PARTIAL: RQ-001, RQ-002. OPEN: RQ-004. NOT VERIFIED (tested, failed): RQ-025 (model did not delegate to the llm tool; not a parse failure). NOT ASSESSED: 22.
PROGRESS (W83, 2026-09-24): VERIFIED 3/28 unchanged. PARTIAL: RQ-001, RQ-002, RQ-024, RQ-031.
PROGRESS (W83 owner ruling, 2026-09-24): VERIFIED 4/28 - RQ-021, RQ-022, RQ-024, RQ-030.
PHASE 2 PROGRESS (W83): RQ-032 evidence 6/6 real documents (S3 re-run 3, 0507c8c), owner ruling pending; RQ-023/027/033 not assessed. PARTIAL: RQ-001, RQ-002, RQ-031. OPEN: RQ-004. NOT VERIFIED: RQ-025. NOT ASSESSED: 20. OPEN: RQ-004. NOT VERIFIED: RQ-025. NOT ASSESSED: 20.
QUALIFICATION RULE AMENDMENT (owner ruling R1, W83): dispatch.log ATTEMPT/OUTCOME lines (per call, turn id, reason code,
%LOCALAPPDATA%\OpenJarvis\logs\dispatch.log) are ACCEPTED as the server-path machine invocation record, provided the pass
criterion also checks the reply content. It records that a tool ran, not that the reply was faithful to it.
QUALIFICATION RULE (W77, Vol 3A F7): a tool-backed row is VERIFIED only on a machine invocation
record. The only one that exists today is AgentResult.tool_results via the SDK. telemetry.db proves
engine and model only; [traces] is disabled; the OpenAI response tool_calls field was null on every
run; CLI stdout shows the answer only. Tier B tests for tool-backed rows target ask_full until the
server path emits a record of its own (Defect 6 / event bus; RQ-028 depends on it too).

## 6. NOTES
- RQ-028 is the original design's control against claims without invocation (Defect 1).
- RQ-012 and the confirmation gate (Defect 6) trace together.
- REUSE CANDIDATE for RQ-005/006/010/011: S-04 embeds a working IMAP/SMTP function set (add/list accounts, fetch unread, mark read, send; Yahoo defaults). Newer copy C:\Users\Admin\executive-assistant\install_executive_assistant_mac.sh (2026-01-19) not yet read.
- Progress measure: core requirements VERIFIED / 28 (Phase 1 measured rows), from section 5. Phase 2 tracked separately.

## 7. W78 TOOLKIT AUDIT - AGENT TOOLKIT VS ROW MECHANISM (v0.6, W78 2026-09-22)
Source: startup banner tools_loaded= (ground truth for what the agent can call) against each
row's needed mechanism; tool sources read whole. Requirements unchanged. VERIFIED 3/28 unchanged.
| Class | Meaning | Rows | Count |
|---|---|---|---|
| A | Tool loaded and wired on the server | RQ-002, RQ-011 (read half), RQ-021 V, RQ-022 V | 4 |
| B | Config-only unlock (server memory backfill wires memory_*) | RQ-024, RQ-031 | 2 |
| B2 | Needs dependency wiring on the server (SDK already wires it) | RQ-025 (llm) | 1 |
| C | Capability not in the tool registry | RQ-005, 006, 007, 008, 009, 010, 013-020 | 14 |
| D | Not a tool (UI, transport, gate, record) | RQ-001, 004, 012, 028, 029, RQ-030 V | 6 |
| E | Composite | RQ-026 | 1 |
Notes: RQ-025 SDK non-delegation was the model's choice (llm tool offered and wired); owner to
rule whether a direct summary satisfies the row text. RQ-005 needs unread/recent/body support.
W83: Class B UNLOCKED (memory tools loaded, D-26); RQ-024 and RQ-031 now PARTIAL (section 5).
Class C is next assessed against the author's read-only connectors and [tools.mcp] (W79).
file_write confined to the Jarvis scratch pad (829cea7); tool builders deduplicated (854b9c7).
