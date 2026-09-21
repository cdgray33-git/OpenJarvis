# OPENJARVIS (GRAYSTONE LAB) - SYSTEM DESIGN PACKAGE (SDP)
## MASTER INDEX AND DOCUMENT CONTROL
Version 0.1 DRAFT - 2026-09-21 - NOT FOR SUBMISSION

## 1. DOCUMENT CONTROL
| Field | Value |
|---|---|
| System name | OpenJarvis, Graystone Lab deployment (fork of upstream OpenJarvis) |
| System owner | Gray (Solutions Architect, sole developer) |
| Authorizing Official (AO) | TBD - GAP-001 |
| Package status | DRAFT v0.1 - skeleton with measured content only |
| Master location | `docs\SDP\` in repo; mirrored to origin (GitHub) and gitlab (lab) |
| Change control | Every change is a git commit to both remotes (see Vol 6 CM Plan) |

### 1.1 Revision history
| Ver | Date | Author | Change |
|---|---|---|---|
| 0.1 | 2026-09-21 | Claude with system owner | Initial package structure; W71 measured content; gap register |

### 1.2 Approval block
| Role | Name | Signature | Date |
|---|---|---|---|
| System owner | Gray | | |
| Authorizing Official | TBD | | |

## 2. PACKAGE STRUCTURE AND CONFORMANCE
Design volumes follow the MIL-STD-498 Data Item Descriptions (standard
cancelled 1998; DIDs remain cited on contracts; successors IEEE 1016 and
ISO/IEC/IEEE 12207/15288). Security volumes follow the NIST Risk Management
Framework (SP 800-37 Rev 2; controls SP 800-53; SSP per SP 800-18; DoD
application DoDI 8510.01; ports/protocols under DoDI 8551.01 PPSM).
CAVEAT: outlines below were written from knowledge of the DIDs, not copied
from the DID texts. Verify each against the official DID (ASSIST) before
submission - GAP-002.

| Vol | Document | Governing standard | File | State |
|---|---|---|---|---|
| 1 | System/Subsystem Design Description (SSDD) | DI-IPSC-81432 | 01-SSDD.md | Skeleton + measured |
| 2 | Software Requirements Spec (SRS) + RTM | DI-IPSC-81433 | 02-SRS-RTM.md | Skeleton; no baseline |
| 3 | Interface Design Description (IDD/ICD) | DI-IPSC-81436 | 03-IDD.md | Skeleton + measured |
| 4 | Software Design Description (SDD) | DI-IPSC-81435 | 04-SDD.md | Skeleton + measured |
| 5 | Database Design Description (DBDD) | DI-IPSC-81437 | 05-DBDD.md | Skeleton |
| 6 | CM Plan, Baseline, Version Description | SP 800-53 CM family; SVD DI-IPSC-81442 | 06-CM-SVD.md | Skeleton + findings |
| 7 | System Security Plan (SSP) | NIST SP 800-18 / 800-53 | 07-SSP.md | Skeleton |
| 8 | Plan of Action and Milestones (POA&M) | SP 800-37 | 08-POAM.md | Populated from W70-W71 |
| 9 | Contingency Plan | NIST SP 800-34 | 09-CP.md | Skeleton + finding |
| 10 | Coverage matrix and gap register | package control | 10-COVERAGE-GAPS.md | Populated |

## 3. EVIDENCE GRADES (MANDATORY ON EVERY FACT)
| Grade | Meaning | Acceptable as basis for AO review |
|---|---|---|
| [M] | MEASURED - command output or instrument, recorded with date | Yes |
| [R] | READ - taken directly from source code, file:line cited | Yes |
| [S] | STATED - system owner's statement, dated | Yes, for intent and decisions |
| [I] | INFERRED - reasoning, not verified | NO. Must be converted to M/R or removed |
Rule adopted 2026-09-21 after an [I] provenance claim (file dates = author
original) was disproven by measurement. See Vol 6 section 4.

## 4. MAINTENANCE PROCEDURE (DEFINITION OF DONE)
A fix, feature, or instrument is NOT complete until, in the same window:
1. Vol 1/4 concept-of-execution flow (SV-10c style) for the affected path is updated.
2. Vol 3 interface row (port, protocol, encoding, direction) is updated.
3. Vol 6 CM entry: commit hash (both remotes), files, rollback point.
4. Vol 2 RTM row status changes, with test evidence reference.
5. Vol 8 POA&M item opened or closed.
6. Vol 10 coverage cells touched are marked.
Each handoff lists "SDP sections touched". A window that documents nothing
has not finished.

## 5. SOURCE MATERIAL NOT YET HARVESTED
Handoff archives W1-W71 (repo root and Downloads) and the memory register
files hold findings not yet placed in chapters. Harvest method: extraction
by a self-posting 550B bundle into chapter slots, then owner review. GAP-003.
