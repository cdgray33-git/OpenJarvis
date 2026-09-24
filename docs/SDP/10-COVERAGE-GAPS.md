# VOL 10 - COVERAGE MATRIX AND GAP REGISTER
v0.2 DRAFT 2026-09-23 (W82). An empty cell is a documentation gap, visible by design.

## 1. COVERAGE (element x volume) after the W82 harvest
| Element | SSDD | RTM | IDD | SDD | DBDD | CM | SSP | POAM |
|---|---|---|---|---|---|---|---|---|
| Startup / assembly | X | | | X | | X | | |
| Chat paths 1a-1d, B1, B2 | X | X | X | X | | | | X |
| Cloud routing / OpenRouter | X | | X | X | X | | X | X |
| Tool dispatch gate chain | X | | | X | X | | X | X |
| Confirmation gate (Defect 6) GREAT DETAIL | X | X | X | X | X | X | X | X |
| Mailbox service | X | X | partial (IMAP) | X | X | | X | X |
| Managed agents / operators | X | | | X | X | | X | X |
| Model host resolution | X | | X | X | X | X | X | X |
| Concurrency / workers | X | | | X | | | | X |
| Logging topology | | | X | X | X | | X | X |
| Voice out / in, stop | X | X | partial (whisper) | X | | | | X |
| Build and delivery | | | X | X | | X | | |
| Memory / RAG / embeddings | | X | | partial | X | | | X |
| Event bus | | | X | X | | | | |

## 2. GAP REGISTER
CLOSED by W82 harvest or earlier windows: GAP-003 harvest W42-W81 (W82; W1-W41 still unharvested -> GAP-003b);
GAP-010 author procedures located (W76); GAP-011 Ollama port 11434 (W77/W80); GAP-016 per-unit design (partial, Vol 4);
GAP-019 author baseline af21bc18 (W73); GAP-020 requirements baseline (W75).
OPEN: GAP-001 AO and security contact. GAP-002 verify outlines against DID texts. GAP-003b harvest W1-W41 archives.
GAP-012 faster-whisper host/port/protocol. GAP-013 OV-1/SV-1 diagrams as standalone files. GAP-014 glossary.
GAP-015 IMAP host/port/TLS/auth (read imap_mail.py whole). GAP-017 datastore schemas. GAP-018 full commit history with hashes.
GAP-030 FIPS 199 categorization. GAP-031 boundary diagram. GAP-032 interconnection agreements. GAP-033 full SP 800-53 baseline
selection. GAP-040 backup scope and restore test. GAP-041 (new) out-of-git configuration baseline.

## 3. MAINTENANCE RULE (Master section 4, restated)
A window is not finished until the volumes it touched are updated in the same window and each handoff lists "SDP sections
touched". The W82 finding was that this rule lapsed after W71 for Vols 1, 3-10; the harvest restores them.
