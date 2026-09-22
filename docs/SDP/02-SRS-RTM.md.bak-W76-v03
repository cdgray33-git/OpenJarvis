# VOL 2 - SOFTWARE REQUIREMENTS SPECIFICATION (SRS) AND TRACEABILITY MATRIX
Governing DID: DI-IPSC-81433 (verify, GAP-002). v0.3 RATIFIED (W75, 2026-09-22).
v0.1 (W72) seeded RQ-001..004. v0.2 adds RQ-005..031 recovered from the pre-OpenJarvis
executive-assistant artifacts (R1.1). Design mapping is R1.2; verification is R1.3.

STATUS: REQUIREMENTS BASELINE RATIFIED BY OWNER 2026-09-22 (W75). GAP-020 CLOSED.
CORE (Phase 1): 29 rows. RQ-003 is a rollup, so 28 rows are measured.
PHASE 2 (supporting roles, deferred by owner): RQ-023, RQ-027, RQ-032, RQ-033.
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
Author Agent QA Runbook (37 scenarios) is the verification set (R1.3). Mapping TBD.

## 5. REQUIREMENTS TRACEABILITY MATRIX
| Req ID | Design element (Vol 1/4) | Interface (Vol 3) | Test evidence | Status |
|---|---|---|---|---|
| RQ-001 | TTS: ttsPlayer.ts, ChatArea TTS driver | IF-03 | F-W71-VOICE-LATE open | PARTIAL |
| RQ-002 | imap_mail connector, mailbox_tools | TBD | 08/11 live usage report | PARTIAL |
| RQ-003 | Decomposed into RQ-005..031 | - | - | ROLLUP |
| RQ-004 | Path 1b, stream_bridge, Option A | IF-01 | stream_probe_w70 | OPEN (POAM-01) |
| RQ-005..RQ-031 core | TBD (R1.2) | TBD | TBD (R1.3) | NOT ASSESSED |
| RQ-023, 027, 032, 033 | - | - | - | DEFERRED (Phase 2) |

## 6. NOTES
- RQ-028 is the original design's control against claims without invocation (Defect 1).
- RQ-012 and the confirmation gate (Defect 6) trace together.
- REUSE CANDIDATE for RQ-005/006/010/011: S-04 embeds a working IMAP/SMTP function set (add/list accounts, fetch unread, mark read, send; Yahoo defaults). Newer copy C:\Users\Admin\executive-assistant\install_executive_assistant_mac.sh (2026-01-19) not yet read.
- Progress measure: core requirements VERIFIED / 28 (Phase 1 measured rows), from section 5. Phase 2 tracked separately.
