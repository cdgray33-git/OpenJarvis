# VOL 7 - SYSTEM SECURITY PLAN (SSP)
Governing: NIST SP 800-18 Rev 1; controls NIST SP 800-53; DoDI 8510.01. v0.2 DRAFT 2026-09-23 (W82).
Control statements below are the engineering ASSESSMENT for the package; the assessor and AO make determinations. Status:
IMPL = implemented and evidenced; PART = partial; PLAN = POA&M item; N/A-DEV = development system, not yet in scope.

## 1. SYSTEM IDENTIFICATION (SP 800-18 elements)
| Element | Content | State |
|---|---|---|
| Name / identifier | OpenJarvis (Graystone Lab) | Done |
| Owner / AO / security contact | Gray / TBD / TBD | GAP-001 |
| Categorization (FIPS 199 / SP 800-60) | Owner decision; handles family mail credentials and content | GAP-030 |
| Operational status | Development, in personal use | [S] |
| Description / purpose | Vol 1 section 1.2 | Done |
| Environment and boundary | Vol 1 section 3 (zones Z1-Z3); diagram owed | PART (GAP-031) |
| Interconnections | Vol 3 IF table and section 5 | PART (IMAP GAP-015, whisper GAP-012) |
| Ports, protocols, services (PPSM) | Vol 3 section 3 | PART |

## 2. CONTROL IMPLEMENTATION (assessment)
| Control | Implementation in this system | Evidence | Status |
|---|---|---|---|
| AC-3 Access enforcement | Toolkit bind: an agent executes only tools it was offered (PermissionError) | W54-W55 harness | IMPL (managed agents) |
| AC-3 / AC-6 | Human confirmation gate on confirmable tools (chat path, live by default); argument-aware for mailbox writes | W50, W52, W58, W60 measured | IMPL (chat); PLAN POAM-17/18 |
| AC-6 Least privilege | file_write confined to workspace; knowledge_sql limited to one table by SQLite authorizer | W78, W55 | IMPL; file_read PLAN POAM-21 |
| AC-17 / SC-7 Boundary | Backend binds 127.0.0.1 only (BIND_ASSERT every start); CDP port removed | W42, W63, W80 | IMPL; config/runtime mismatch POAM-14; portproxy POAM-26 |
| AU-2 / AU-3 / AU-12 Audit | backend.log (sanitized), dispatch.log ATTEMPT/OUTCOME reason codes, POLICY attribution for every auto-approval, gate decision lines | W46, W52, W56 | IMPL (tools); PLAN POAM-32 (traces) |
| AU-9 | Logs local, rotated, 40 MB budget; no integrity protection | W42 | PART |
| CM-2 Baseline | Author base af21bc18; divergence register Vol 3A | W73-W74 | IMPL; out-of-git items POAM-35 |
| CM-3 / CM-4 Change control and impact | Backup, isolated verify, separate commit, both remotes, AO change record | W81 s5.1, W82 records | IMPL |
| CM-6 Settings | config.toml authoritative for model host; env fallback kept by owner decision | W80-W81 | IMPL |
| CM-7 Least functionality | Engine turn-down list; analytics disabled | W79, D-10 | IMPL; removal POAM-23 |
| CP-9 Backup | Code on two remotes; config and stores not backed up | - | PLAN POAM-06 |
| IA-2 / IA-9 | API key set for HTTP (api_key_set=True); WS unauthenticated; model/voice services unauthenticated | W81 | PART; PLAN POAM-12/13 |
| IA-5 Authenticators | Cloud and IMAP secrets in per-user files, plaintext; logs count keys, never values | W43-W45, W61 | PART; PLAN POAM-24 |
| SA-10 / SA-11 Developer CM and testing | Provenance diff, non-interactive discriminating harnesses, live V&V before commit | W73, W81 | IMPL |
| SC-5 Availability | Fail-soft startup; gate waits on worker threads not the event loop | W44, W50 | PART (POAM-03/33) |
| SC-8 Transmission confidentiality | TLS on internet flows; lab model/voice traffic plaintext | W81 | PLAN POAM-11 |
| SC-28 Data at rest | none | - | PLAN POAM-24/25 |
| SI-2 Flaw remediation | Upstream security fixes post-date base | H-W73-BEHIND | PLAN POAM-15 |
| SI-10 / SI-11 Input validation, error handling | test-execute argument guard (400 on unknown keys); tool outcome reason codes; timeout reported as timeout, not refusal | W52, W46 | IMPL |

## 3. PLAIN LANGUAGE
Jarvis keeps its door locked to the outside (it only answers the same computer), asks you before it does anything that could
change your mail or run commands, writes down every tool it tries and why it stopped, and keeps a list of every change made to it.
What it does not do yet: lock its conversations with the lab servers, lock its own event channel, protect its saved passwords with
encryption, or keep backups of its settings and memory. Those are listed in Vol 8 with the controls they fall under.
