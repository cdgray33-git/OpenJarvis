# OPENJARVIS ROADMAP v0.1 - LIVING LIST (W72, 2026-09-21)
Built from: author docs (39 files, [R] intent only), author agent-layer code (28 files,
read), and runtime measurement on the Windows box (W72 exchange 11, [M]).
Rule: an item is crossed off only with its evidence recorded. Improve this list as items
close. Status: [ ] open  [~] in progress  [x] done (evidence cited)

## A. MEASURED BASELINE - W72 [M]
- M1 Backend on 127.0.0.1:8010 is NATIVE WINDOWS python (Python312, CPython 3.12.10,
  venv by uv). WSL2 distro "Ubuntu" EXISTS but was STOPPED. The running Jarvis is not
  the WSL2 build.
- M2 Server + default agent = native_openhands; model qwen3-coder:30b; max_tokens 1024;
  mailbox_* tools on the default agent tool list.
- M3 MANAGED-AGENT LAYER IS SET UP AND IN USE: agents.db, 8 agents, 901 messages,
  14 learning-log rows. Cody-Coder 783 runs (ERROR), Cody-Builder 83 runs (ERROR),
  Nova = author inbox_triager template (0 runs), Oryan = research_monitor (1 run,
  paused), Oracle/My Assistant = deep_research.
- M4 OPERATORS LAYER HAS NEVER RUN: [scheduler] enabled=false, scheduler.db absent,
  [operators] enabled=false, no user operators dir.
- M5 traces enabled, traces.db has 0 traces despite ~878 managed-agent ticks.
- M6 agent_checkpoints 0 (confirms D-W72-CKPT). agent_tasks 0. channel_bindings 0.
- M7 security: enforce_tool_confirmation=true, mode warn, local_tool_bypass=false.
CLARIFIED BY GRAY (W72): the managed agents in agents.db (Cody, Cody-Coder, Cody-Builder,
Nova, Oryan, Oracle) are GRAY'S PERSONAL AGENTS, not the Jarvis executive-assistant build.
"Not following the author's installation" means: the author's code was pulled into Gray's
GitHub and has been changed and updated since. The Operators half has never run (M4).

## B. TRACK 0 - BASELINE TRUTH (finish before building anything)
- [x] R0.1 Read author docs whole (A 13, B 20, C 6 files). Evidence: AUTHOR-INTENT-W72-A/B/C.
- [x] R0.2 Read author agent-layer code whole (D, 28 files). Evidence: AUTHOR-CODE-W72-D-NOTES.
- [x] R0.3 Measure runtime platform + agent state. Evidence: W72 exchange 11 output.
- [ ] R0.4 Measure the WSL2 Ubuntu distro read-only: does it hold an author install
      (~/.openjarvis, repo, venv)? Gray reports he built Jarvis in WSL2.
- [ ] R0.5 Obtain the upstream author repo at a pinned revision; diff our tree against it.
      Only this closes provenance (CM-01) and shows exactly what Graystone changed.

## C. TRACK 1 - REQUIREMENTS AND THE PROGRESS MEASURE
- [ ] R1.1 Recover Gray's initial requirements list into an RTM (one row per requirement).
- [ ] R1.2 Map each requirement to the author mechanism that serves it (managed agent,
      operator, digest, channel, connector, MCP) or mark GAP.
- [ ] R1.3 Adopt the author's Agent QA Runbook (37 scenarios) as the verification set;
      record a baseline pass count. That count is the first honest progress number.

## D. TRACK 2 - SDP RESTRUCTURE (ATO-led; follows Track 1)
- [ ] R2.1 Restructure SDP v0.1 to MIL-STD-498 DIDs + RMF package; RTM is the spine.
- [ ] R2.2 Divergence register D1-D6 with evidence grades (D1 now [M]).
- [ ] R2.3 SDD chapter: two autonomy subsystems, stores, bus; execution-path entries for
      managed-agent tick and operator tick (gate by gate, plain language + technical).

## E. TRACK 3 - AGENT LAYER (measure first, then decide)
- [ ] R3.1 Why are Cody-Coder and Cody-Builder in ERROR? Read their summary_memory
      (executor writes "ERROR: ..." there) - read-only measurement.
- [ ] R3.2 Why 0 traces on ~878 ticks (M5)? Is trace_store None on the managed path?
- [ ] R3.3 Decide the executive-assistant agent type with evidence: author intends
      orchestrator / operative / monitor_operative; Graystone runs native_openhands.
- [ ] R3.4 Managed-agent tool construction gives custom tools no dependencies
      (executor step 5). Measure whether mailbox_* tools work on the managed path.
- [ ] R3.5 Nova (inbox_triager) has no mailbox tool; decide author-path wiring
      (EmailChannel vs mailbox tools) for Yahoo triage.
- [ ] R3.6 Operators: decide whether to enable [scheduler]/[operators] at all.

## F. TRACK 4 - EXECUTIVE-ASSISTANT CAPABILITIES (author mechanism -> status)
- [ ] Mail triage ............ author: inbox_triager / inbox_triage / correspondent -> GAP (R3.5)
- [ ] Morning briefing ....... author: digest (digest_collect + TTS)               -> unmeasured
- [ ] Calendar ............... author: gcalendar connector                         -> unmeasured
- [ ] Scheduling ............. author: agent scheduler / TaskScheduler             -> managed yes, operators no
- [ ] Memory recall .......... author: memory_store/search, context injection      -> wired, never observed
- [ ] Voice .................. Graystone Kokoro (author: cloud TTS)                -> HELD (F-W71-VOICE-LATE)
- [ ] Cloud models ........... author: CloudEngine                                 -> possibly broken (logged W72)

## G. STANDING HAZARDS AND AUTHOR DEFECTS (read, not traced)
- H-W72-WINKILL  never run `jarvis start|stop|status` from the Windows venv (M1 makes it live).
- D-W72-OPLOGS   `jarvis operators logs` calls a missing store method.
- D-W72-CKPT     executor never writes checkpoints ([M] via M6).
- D-W72-EPHEM    run_ephemeral omits the model argument.
- C10            server agent serves NON-streaming only (matches W71 buffered agent path).
