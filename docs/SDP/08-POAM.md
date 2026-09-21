# VOL 8 - PLAN OF ACTION AND MILESTONES (POA&M)
v0.1 DRAFT. Populated from W70-W71; W1-W69 items pending harvest (GAP-003).
| ID | Weakness | Source | Grade | Remediation | Status |
|---|---|---|---|---|---|
| POAM-01 | Agent replies buffered server-side (no live text on path 1b) | W70 | [M] | Option A | Open |
| POAM-02 | Voice starts only after last word (F-W71-VOICE-LATE) | W71 | [M] | Locate synthesize route; test SYNCIO | Open |
| POAM-03 | Ollama stream uses sync client in async code; blocks event loop | W71 | [R] | Async client or thread offload | Open |
| POAM-04 | Telemetry lost on stream_full path | W71 | [R] | Add events to InstrumentedEngine.stream_full | Open |
| POAM-05 | Input redaction bypassed on stream_full path; no RETRY400 log | W71 | [R] | Add input scan and log line | Open |
| POAM-06 | Rollback points not backed up | W71 | [M] | Vol 9 | Open |
| POAM-07 | No author baseline; provenance unprovable | W71 | [M] | GAP-019 | Open |
| POAM-08 | No requirements baseline / RTM | standing | [S] | Vol 2 | Open |
| POAM-09 | Frontend TTS debug logs unreadable in production build | W71 | [R] | Route to a readable sink | Open |
| POAM-10 | Credential exposure 08/01 requiring rotation (status unverified) | 08/01 | [S] | Verify rotation | Verify |
