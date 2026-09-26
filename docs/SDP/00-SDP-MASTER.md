# OPENJARVIS (GRAYSTONE LAB) - SYSTEM DESIGN PACKAGE (SDP)
## MASTER INDEX AND DOCUMENT CONTROL
Version 0.2 DRAFT - 2026-09-23 - NOT FOR SUBMISSION

## 1. DOCUMENT CONTROL
| Field | Value |
|---|---|
| System name | OpenJarvis, Graystone Lab deployment (fork of upstream OpenJarvis, base af21bc18) |
| System owner | Gray (Solutions Architect, sole developer) |
| Authorizing Official (AO) | TBD - GAP-001 |
| Package status | DRAFT v0.2 - harvested from handoff archives W42-W81 plus W82 measurement |
| Master location | `docs\SDP\` in repo; mirrored to origin (GitHub) and gitlab (lab) |
| Change control | Every change is a git commit to both remotes (Vol 6) |
### 1.1 Revision history
| Ver | Date | Author | Change |
|---|---|---|---|
| 0.1 | 2026-09-21 | Claude with system owner | Initial package structure; W71 measured content; gap register |
| 0.2 | 2026-09-23 | Claude with system owner (W82) | Harvest of ARCHIVE-W42..W81 (40 archives, section-hash deduplicated, 477 SDP-relevant sections) into Vols 1, 3, 4, 5, 6, 7, 8, 9, 10; Vol 3A section G added; Vol 2 unchanged |
| 0.3 | 2026-09-26 | Claude with system owner (W92) | Upgrade execution W90-W92: Vol 4 SDD 20.8 (merge, Method B setup and flow gate by gate, gates, commits, negative results, hazards); Vol 3A G.9 (divergence re-baseline to a6dcf846, author defect AD-W92-1); Vol 8 POAM-67..79, POAM-66 status; Vol 6 version rows and rollback |
### 1.2 Approval block
| Role | Name | Signature | Date |
|---|---|---|---|
| System owner | Gray | | |
| Authorizing Official | TBD | | |

## 2. PACKAGE STRUCTURE AND CONFORMANCE
Design volumes follow the MIL-STD-498 Data Item Descriptions (standard cancelled 1998; DIDs remain cited on contracts; successors
IEEE 1016 and ISO/IEC/IEEE 12207/15288). Security volumes follow the NIST RMF (SP 800-37 Rev 2; controls SP 800-53; SSP per
SP 800-18; DoD application DoDI 8510.01; ports/protocols under DoDI 8551.01 PPSM). CAVEAT: outlines were written from knowledge
of the DIDs, not copied from the DID texts - GAP-002.
| Vol | Document | Governing standard | File | State |
|---|---|---|---|---|
| 1 | System/Subsystem Design Description (SSDD) | DI-IPSC-81432 | 01-SSDD.md | v0.2 harvested |
| 2 | Software Requirements Spec (SRS) + RTM | DI-IPSC-81433 | 02-SRS-RTM.md | Ratified 09/22; VERIFIED 3/28 |
| 3 | Interface Design Description (IDD/ICD) | DI-IPSC-81436 | 03-IDD.md | v0.2 harvested; IMAP and whisper open |
| 3A | Author baseline and divergence register | package control | 03-AUTHOR-BASELINE.md | v0.3 + section G (W82) |
| 4 | Software Design Description (SDD) | DI-IPSC-81435 | 04-SDD.md | v0.2 harvested; confirmation gate in great detail |
| 5 | Database Design Description (DBDD) | DI-IPSC-81437 | 05-DBDD.md | v0.2; schemas open |
| 6 | CM Plan, Baseline, Version Description | SP 800-53 CM; DI-IPSC-81442 | 06-CM-SVD.md | v0.2 |
| 7 | System Security Plan (SSP) | NIST SP 800-18 / 800-53 | 07-SSP.md | v0.2 control assessment |
| 8 | Plan of Action and Milestones (POA&M) | SP 800-37 | 08-POAM.md | v0.2, 37 items |
| 9 | Contingency Plan | NIST SP 800-34 | 09-CP.md | v0.2; backup open |
| 10 | Coverage matrix and gap register | package control | 10-COVERAGE-GAPS.md | v0.2 |

## 3. EVIDENCE GRADES (MANDATORY ON EVERY FACT)
| Grade | Meaning | Acceptable as basis for AO review |
|---|---|---|
| [M] | MEASURED - command output or instrument, recorded with date | Yes |
| [R] | READ - taken directly from source code, file:line cited | Yes |
| [S] | STATED - system owner's statement, dated | Yes, for intent and decisions |
| [I] | INFERRED - reasoning, not verified | NO. Must be converted to M/R or removed |
v0.2 adds the source window to each fact (e.g. [M W50]). A line number is valid as of that window; verify before relying on it.
Facts carried from the archives keep the grade the archive recorded; they were not re-measured in W82 unless marked W82.

## 4. MAINTENANCE PROCEDURE (DEFINITION OF DONE)
A fix, feature, or instrument is NOT complete until, in the same window:
1. Vol 1/4 concept-of-execution flow for the affected path is updated.
2. Vol 3 interface row (port, protocol, encoding, direction) is updated.
3. Vol 6 CM entry: commit hash (both remotes), files, rollback point.
4. Vol 2 RTM row status changes, with test evidence reference.
5. Vol 8 POA&M item opened or closed.
6. Vol 10 coverage cells touched are marked.
Each handoff lists "SDP sections touched". A window that documents nothing has not finished.
W82 FINDING: this rule lapsed after W71 for every volume except 2 and 3A; SDP feed accumulated in the archives instead. v0.2
restores the package. Every BRIEF from W83 on carries an "SDP sections touched" line, verified against git.

## 5. HARVEST METHOD AND SOURCE MATERIAL (GAP-003)
W82 method: every ARCHIVE-W42..W81 in the repo root split into sections; sections byte-identical to one already seen (carried
material) dropped; SDP-relevant sections kept by heading/content filter; every drop logged with its reason
(evidence\W82\SDP-src-dropped.txt); result in evidence\W82\SDP-src-part1..10.md (580 KB). Ingested lab-local (nothing sent off
the lab); working notes evidence\W82\sdp\notes.md. Not harvested: archives W1-W41 (GAP-003b).
