# SDP SOURCE EXTRACT W82 part 3 (deduplicated by section hash)
### [ARCHIVE-W47-2026-09-10.md] 4. NEGATIVE RESULTS AND REFUTED TESTS
- **`dispatch.log` IS NOT IN THE REPO.** A `Get-ChildItem -Recurse -Filter dispatch.log` from
  the repo root returns ZERO rows. This is not a missing file - the path is
  `%LOCALAPPDATA%\OpenJarvis\logs\`, read out of `_get_dispatch_logger` at `_stubs.py:160-167`.
  Do not re-run that search.
- **`backend.log` CARRIES NO CONFIRM RECORD.** `Select-String CONFIRM` returns zero matches
  after a live gate event. The confirm_id is bus-only. Do not go looking again.
- **`config.toml` DOES NOT HOLD THE API KEY.** Printed in full with key/token/secret values
  redacted; there is no `[server.auth]` section. The `:534` fallback path is dead on this box.
- **THE `/v1/tools/test-execute` OPENAPI SCHEMA IS EMPTY.** `requestBody` returns nothing and no
  `TestExec`/`ToolExec` component schema exists - the handler reads `await request.json()`
  untyped at `:2297`. The body shape (`{tool, arguments}`) came from source, not the spec. Same
  for `/v1/tools/confirm` (`{confirm_id, decision}`, from `:2059-2060`). **Do not probe the
  OpenAPI spec for these two routes again; read the handler.**
- **`mailbox_find_messages` CANNOT DRIVE THE GATE.** 422, verified live. Neither can
  `mailbox_move_to_trash` or `mailbox_empty_folder`. Only `shell_exec` can, of the live twelve.
- **`agents\builder.py` DOES NOT EXIST.** The file is `system\builder.py`. There are three
  `builder.py` under `src`: `prompt\`, `system\`, `workflow\`.
- **NOT REFUTED, NOT CONFIRMED:** which executor actually served the probe. The three live
  candidates are (a) something other than a `system\builder.py` construction, (b) a
  construction that sets `_interactive`/`_confirm_callback` after `__init__` somewhere not yet
  found, (c) the `:338` return not being reached at all. **This is the first question of W48.**
### [ARCHIVE-W47-2026-09-10.md] 5. HAZARDS FOUND
- **A USER-LEVEL ENV VAR DOES NOT REACH AN OPEN SHELL.** Ctrl+C and restart in the same window
  inherits the stale environment. Cost a full restart cycle. Echo the flag in the target shell
  before starting.
- **STALE `$i` SILENTLY OFFSETS A NUMBERING LOOP.** A counter left over from an earlier loop in
  the same shell offset one read by +108 lines and produced confident wrong line references.
  Reset `$i = 0` immediately before every loop, and prefer `Select-String` line numbers.
- **`Select-String` ON A GLOB PRINTS FILENAME WITHOUT DIRECTORY.** Nine hits for `ToolExecutor(`
  showed `builder.py` with no path; assuming `agents\` cost an exchange. Use
  `Get-ChildItem -Recurse -Filter` first.
- **`_get_dispatch_logger` CAN SILENTLY DISARM ITSELF** at `_stubs.py:172-173` - a
  `NullHandler` on any construction exception, no error surfaced. See 6.8.
- **`test-execute` IS FIRE-AND-FORGET.** 200 means accepted, NOT executed. The dispatch runs on
  an `asyncio.to_thread` worker and the HTTP response tells you nothing about the outcome. Always
  read `dispatch.log` after, with a sleep long enough to cover the 120 s TTL if a gate is
  involved.
- Carried, still true: `_stubs.py` is CRLF and git normalises to LF; never pass multi-line
  Python to `python -c` through PowerShell; `Select-String` has no `-Recurse`;
  `Select-Object -First N` truncates silently.
### [ARCHIVE-W47-2026-09-10.md] 6.8 CHANGED THIS WINDOW (W47)
- **`dispatch.log` PATH CONFIRMED FROM SOURCE, NOT SEARCH.**
  `C:\Users\Admin\AppData\Local\OpenJarvis\logs\dispatch.log`. It is OUTSIDE the repo, which is
  why a `Get-ChildItem -Recurse` from the repo root returns nothing. Producer confirmed at
  `tools\_stubs.py:154-177` (`_get_dispatch_logger`), sink `openjarvis.dispatch`,
  `RotatingFileHandler` 2 MB x 4, `propagate=False`, `setLevel(INFO)`. W46 Brief was right that
  `_stubs.py` is the producer; the line number is `:154`, not `:111`, after the patch shifted
  the file.
- **HAZARD IN THE INSTRUMENT ITSELF (`:172-173`):** if `makedirs` or handler construction
  throws, the except attaches a `NullHandler` and the instrument goes permanently silent with
  no error anywhere. Same failure class as the 09/06 `print()` lesson. Nothing checks this at
  startup. An instrument that can silently disarm itself is not yet a trustworthy instrument.
- **INSTRUMENT STATUS: PARTIALLY VERIFIED, DO NOT TRUST `reason=` YET.** See 8.5. `reason=OK`
  is proven faithful. `reason=GATE_TIMEOUT` is proven UNFAITHFUL on at least one path.
- **NEW INSTRUMENT AVAILABLE AND NOW PROVEN: `POST /v1/tools/confirm` + `POST
  /v1/tools/test-execute`.** test-execute is a synthetic dispatch injector - it drives a single
  tool through the REAL live agent executor with a known `turn_id` (`test-<runid>`) and no model
  in the loop. This is the first instrument that can exercise the tool boundary deterministically
  and non-interactively. Preconditions: `OPENJARVIS_TEST_EXEC` set in the SERVER's process env
  AND loopback bind. It REFUSES (422) any tool whose spec does not set `requires_confirmation`,
  so it can only ever drive gate-bearing tools. Registered as a permanent diagnostic asset.
### [ARCHIVE-W47-2026-09-10.md] 7.8 CHANGED THIS WINDOW (W47)
- **THE CONFIRM CORRELATION ID IS BUS-ONLY AND REACHES NO LOG SINK.** `Select-String CONFIRM`
  against `backend.log` returns ZERO matches after a live gate event. The `confirm_id` is
  published only as a `TOOL_CONFIRM_REQUEST` payload field (`_stubs.py:363-374`) on the
  `/v1/agents/events` WS. It is never logged, and `confirm_registry` exposes NO listing
  accessor - only `get(confirm_id)` and `pending_count()`. Consequence: a client that misses
  the WS event can never resolve that confirmation, and `wait()` fails closed to `timeout`
  by design (`confirm_registry.py:125-127`). **There is no operator-visible way to enumerate
  pending confirmations.** This is a logging-topology gap AND an SDP guard finding.
- Carried unchanged and re-confirmed: `dispatch.log` remains immune to the `uvicorn.access`
  flood by construction, and is the only sink carrying tool-boundary records.
### [ARCHIVE-W47-2026-09-10.md] 8.5 CHANGED THIS WINDOW (W47)
**THE GATE COLUMN IS NO LONGER BLANK - AND WHAT IT SAYS CONTRADICTS THE CODE.**
**Path: `POST /v1/tools/test-execute` (NEW, registered W47).**
- Entry: `server\agent_manager_routes.py:2142` (`@tools_router.post("/test-execute")`),
  handler `test_execute_tool` at `:2143`.
- Preconditions, both 403 with distinct bodies: `OPENJARVIS_TEST_EXEC` unset (`:2161`), bind
  not loopback (`:2171`). 409 if no live agent executor. 404 if tool not on the live agent -
  and that 404 body RETURNS THE FULL LIVE TOOL LIST, which is how the register was populated
  without touching the model.
- 422 if `requires_confirmation` is falsy on the spec - a deliberate refusal, not a defect.
- Executor served: `request.app.state.agent._executor` - THE LIVE CHAT AGENT'S EXECUTOR. This
  is the same executor the chat path uses, which is what makes the probe meaningful.
- Dispatch: `asyncio.create_task(asyncio.to_thread(_run))` at `:2366`; `_run` sets
  `CURRENT_TURN_ID` to `test-<runid>` and calls `_executor.execute(_call)`. Returns 200
  `{accepted:true, run_id, turn_id, tool, marker}` IMMEDIATELY - the dispatch is fire-and-forget
  on a worker thread. Human present: no. Bus traffic: whatever the gate emits.
- **Confirmation gate on this path: LIVE. Runtime-proven to block.**
**LIVE TOOL SET ON THE CHAT AGENT (from the 404 body, 2026-09-10):** calculator, think,
retrieval, file_read, code_interpreter, shell_exec, file_write, mailbox_list_accounts,
mailbox_usage_report, mailbox_find_messages, mailbox_move_to_trash, mailbox_empty_folder.
**TOOLS DECLARING `requires_confirmation=True` ANYWHERE IN `tools\*.py`:** exactly three -
`agent_tools.py:289`, `git_tool.py:283`, `shell_exec.py:71`. **Of the twelve live tools, only
`shell_exec` carries the flag.**
**THEREFORE: `mailbox_move_to_trash` AND `mailbox_empty_folder` ARE UNGATED.** The two
destructive mailbox tools at the centre of Defect 1 declare no confirmation requirement and
were REFUSED BY test-execute WITH 422 on exactly that basis. Verified twice, once per tool,
against the live spec objects rather than source. This is the single most consequential finding
of the window and it belongs at the top of the next list.
**THE CONTRADICTION - OPEN, UNRESOLVED, LOAD-BEARING.**
- Observed: `test-execute` on `shell_exec` produced ATTEMPT at 14:08:49.626, then OUTCOME at
  14:10:49.632 - `success=False latency=120.007 timed_out=False reason=GATE_TIMEOUT`. The
  120.007 s matches `confirm_registry._DEFAULT_TTL = 120.0` to the millisecond.
- But the gate's own precondition at `_stubs.py:337-338` is
  `if tool.spec.requires_confirmation:` then `if not self._interactive or self._confirm_callback
  is None:` -> immediate return, "no confirmation callback is available" (the intended
  `GATE_NO_CALLBACK`).
- `ToolExecutor.__init__` (`:190-209`) defaults `interactive=False`, `confirm_callback=None`.
- The chat agent's executor is built at `system\builder.py:168` and `:193` as
  `ToolExecutor(tool_list, bus)` - POSITIONAL, no `interactive`, no callback, and no
  post-construction assignment of either anywhere in `builder.py`.
- A tree-wide search for `interactive\s*=\s*True` returns SIX hits: four in
  `agent_manager_routes.py` (`:720`, `:1205`, `:1562`, `:1639`), each paired with
  `confirm_callback=lambda _prompt: True` on the adjacent line - all MANAGED-AGENT paths, not
  the chat agent; one in `cli\deep_research_setup_cmd.py:323`; and one that is a COMMENT in
  `tools\mailbox_tools.py:21` stating outright that the server-side agent path builds its
  executor WITHOUT `interactive=True`.
- **So the executor that served the probe should have returned in microseconds. It blocked for
  the full TTL instead.** Both cannot be true. Either the OUTCOME's `reason` is derived from
  registry state rather than the terminal path actually taken, or the `:338` early return is
  not being reached and control falls through to a wait it should never see.
- **CONSEQUENCE: `reason=` IS NOT YET A FAITHFUL REPORT OF THE TERMINAL PATH.** That is the one
  property the instrument exists to provide. `_stubs.py` MUST NOT be committed until the
  reason-selection logic in the `execute` wrapper is read wide and the contradiction resolved.
**ALSO REGISTERED: the four managed-agent constructions AUTO-APPROVE.** `interactive=True` with
`confirm_callback=lambda _prompt: True` means every confirmation on those four paths is
approved unconditionally, with no human and no registry consultation. The gate is present and
permanently open. Gate column for those paths: AUTO-APPROVED.
**NO CALLBACK ANYWHERE IN THE CODEBASE CONSULTS `confirm_registry`.** Every
`confirm_callback=` site in the tree is either `None` or `lambda _prompt: True`
(`deep_research.py:178/191`, `monitor_operative.py:126/138`, `native_openhands.py:76/87`,
`native_react.py:76/88`, `operative.py:60/72`, `orchestrator.py:62/73`, `rlm.py:111/122` all
default to None and pass through; the four route sites auto-approve). **`POST /v1/tools/confirm`
has no consumer.** 6c step 2 built the route, step 3 built the emit, and the callback that
joins them was never written. `GATE_APPROVED` is unreachable on every path in this codebase.
### [ARCHIVE-W47-2026-09-10.md] 11.3 CHANGED THIS WINDOW (W47)
**W47 is the eighth observability window and the first that touched capability.** It did not
add capability, but it produced the first hard, runtime-sourced statement about what the
assistant is actually permitted to do without asking:
**`mailbox_move_to_trash` and `mailbox_empty_folder` - the two tools that can destroy the
family mailbox - are ungated.** No `requires_confirmation`, no gate, no human. This is a direct
statement about the executive-assistant goal: the system currently CAN take destructive action
on the primary use case with nobody in the loop, and the reason it has not is that Defect 1
stops it from invoking the tools at all. The defect is masking the exposure.
Zero connector credentials remain provisioned across all 24 tools - carried from W46, still
the largest unaddressed gap, still on nobody's list, still not measured.
**The requirements-measurement window is now on its NINTH deferral.** It has been deferred
through eight consecutive observability windows. The argument for running it BEFORE more
debugging is now stronger, not weaker: W47 proved the registers themselves can be wrong, and a
progress measure built on unverified carried claims will be wrong the same way. Run it against
source, once, and stop re-deriving.
### [ARCHIVE-W47-2026-09-10.md] 12.3 CHANGED THIS WINDOW (W47)
- **VERIFY THE HALVES SEPARATELY, THEN VERIFY THEM JOINED** (W47). Gray's call, and it was the
  correct one: two half-paths verified in isolation (a success that never reached the gate, a
  gate that timed out unattended) do NOT constitute a verified path. Demanding the full
  designed flow - dispatch, human decision, execution, one coded outcome - is what exposed the
  contradiction in 8.5. A patch that passes every half-test can still be wrong about the whole.
- **A REGISTER THAT DISAGREES WITH THE CODE IS THE FINDING** (W47). When an observation and the
  source contradict, that gap IS the result - do not pick whichever one lets the work continue.
  W47 could have committed a passing instrument and moved on; the contradiction would have
  shipped as ground truth into every later window.
- **AN ENV VAR SET AT USER LEVEL DOES NOT REACH AN ALREADY-OPEN SHELL** (W47). Cost one full
  restart cycle. `SetEnvironmentVariable(...,'User')` requires a NEW process to inherit it -
  Ctrl+C and restart inside the same window keeps the stale environment. Always echo the flag
  in the target shell before starting the server.
- **TAKE FILE PATHS FROM RESULTS, NOT FROM MEMORY** (W47). `Select-String` on a `**` glob prints
  the FILENAME only, not the directory; assuming `agents\builder.py` when the file was
  `system\builder.py` cost an exchange. `Get-ChildItem -Recurse -Filter <name>` first, then read.
- **RESET `$i` BEFORE EVERY NUMBERING LOOP** (W47). A stale `$i` from an earlier loop in the same
  shell silently offset a whole read by +108 lines. Trust `Select-String` line numbers over a
  hand-rolled counter.
- **THE ARCHIVE'S OWN DELTAS MUST SIT INSIDE THEIR SECTIONS** (W47). W46 appended 11.2 and 12.2
  after the end of section 12, so `sed -n '/^## 11\./,/^## 12\./p'` would have silently missed
  11.2. Corrected in this archive; both are now inside their own sections. When appending a
  delta, append it before the NEXT `## ` heading, never at end of file.
### [ARCHIVE-W48-2026-09-11.md] 1. WINDOW SHAPE
Nine exchanges. ONE subject: resolve the W47 contradiction before anything commits. No code
changed, no service restarted, no commit made. The window is entirely a source-reading and
instrument-repair window, and it ended with the contradiction resolved on source but the
confirming external read still unsent.
Sequence: read BRIEF; build the archive scaffold by extraction (first execution of the 09/10
cost rule - one command, 687 lines, worked); wide read of `_stubs.py:191-390`; wide read of
`_stubs.py:100-189` and `:390-470`; enumerate the 45 `confirm_callback`/`interactive` sites;
build a 550B bundler; hit Mark-of-the-Web; build the bundle (364 KB) and fail the send on 400;
recover the working transport config from `ask-550b-554.ps1` and locate the real
`test-execute` route. Handoff on request.
### [ARCHIVE-W48-2026-09-11.md] 2.1 The classifier is faithful - VERIFIED ON SOURCE
`_outcome_reason` at `_stubs.py:143-176` is a pure, read-only content classifier. It never
inspects the executor, the registry, or any timing. Its decision procedure, in order:
`success` true -> `OK`; `metadata.timed_out` -> `TIMEOUT_TOOL`; then a ladder of string
matches against `result.content`.
`GATE_TIMEOUT` is returned at `:171` on exactly one condition: the content contains the
substring "confirmation answer arrived". That substring is produced in the bundle at exactly
one PRODUCING site - `_stubs.py:416`, inside the `else` at `:413`, inside `if not _approved:`
at `:400`. (A grep returns two hits, `:170` and `:416`; `:170` is the matcher itself, not a
producer. That distinction was initially overstated in-window and is corrected here.)
The `:400` block sits AFTER the gate test at `:338`:
    if tool.spec.requires_confirmation:
        if not self._interactive or self._confirm_callback is None:
            return ToolResult(... "no confirmation callback is available." ...)
Therefore any dispatch that produced `reason=GATE_TIMEOUT` MUST have been served by an executor
with `interactive=True` and a non-None `confirm_callback`, must have called that callback at
`:377`, and must have received False from it.
**Conclusion: the W47 observation was internally consistent. `reason=GATE_TIMEOUT` was a
truthful report. The register entry describing the serving executor was the false statement.**
This is the W47 rule "A REGISTER THAT DISAGREES WITH THE CODE IS THE FINDING" landing on the
register for the second window running.
### [ARCHIVE-W48-2026-09-11.md] 2.2 The tree inventory was wrong - 45 sites enumerated
`Select-String` for `confirm_callback|interactive\s*=` across `src` returns 45 sites. The W47
claim that every one is `None` or `lambda _prompt: True` is FALSIFIED by:
    cli\serve.py:310: def _server_confirm_callback(_prompt: str) -> bool:
    cli\serve.py:317: agent_kwargs["confirm_callback"] = (
    cli\serve.py:318:     _server_confirm_callback
A real named function, not a stub. Its body was NOT read this window and is the first read of
W49.
Also present: `cli\ask.py:356` assigns `lambda prompt: True`; `cli\chat_cmd.py:123` assigns a
`_confirm`; seven agent modules (`deep_research`, `monitor_operative`, `native_openhands`,
`native_react`, `operative`, `orchestrator`, `rlm`) each default `confirm_callback=None` and
then forward `interactive=interactive, confirm_callback=confirm_callback`, i.e. they are
pass-throughs, not deciders.
### [ARCHIVE-W48-2026-09-11.md] 2.3 The four managed-agent executors are EXCLUDED as the 120 s source
`server\agent_manager_routes.py` builds four executors with `interactive=True` and
`confirm_callback=lambda _prompt: True` (`:720/721`, `:1205/1206`, `:1562/1563`,
`:1639/1640`). That lambda returns immediately and returns TRUE. With `_approved` true, control
skips the `:400` block entirely and falls through to the start event at `:428` and execution.
Such an executor can never produce `GATE_TIMEOUT`, and cannot block for 120 s.
**So the executor that served the `test-execute` probe was none of those four.** It used a
callback that blocked for the full `_DEFAULT_TTL = 120.0` and then returned False.
`_server_confirm_callback` is the only remaining named candidate in the tree. **This is a
strong deduction, not a confirmed trace - the construction site was not read.**
### [ARCHIVE-W48-2026-09-11.md] 2.4 The gate tail, read in full
`:348-425` is the Defect 6 / 6c step 3 emit path. It registers a confirm id (`:356`), publishes
`TOOL_CONFIRM_REQUEST` with `expires_at` (`:363`), sets `CURRENT_CONFIRM_ID` (`:375`), calls the
callback (`:377`), re-reads the registry (`:381`), publishes `TOOL_CONFIRM_RESOLVED` including
a `reaped` flag (`:397`), and only then branches on `_approved`. The three terminal contents at
`:404` (denied by user), `:408` (approved but callback returned False - explicitly labelled an
internal error), and `:414` (no answer arrived - explicitly labelled a TIMEOUT, not a refusal)
map one-to-one onto `GATE_DENIED`, `GATE_INTERNAL_ERROR`, and `GATE_TIMEOUT`. The mapping is
sound.
### [ARCHIVE-W48-2026-09-11.md] 4. NEGATIVE RESULTS AND REFUTED TESTS
- **REFUTED: "the executor serving test-execute is built at `system\builder.py:168/193` as
  `ToolExecutor(tool_list, bus)` with defaults."** Carried as fact by W47. Refuted by the
  reachability argument in 2.1. How established: read the only producer of the GATE_TIMEOUT
  trigger string and walked back the guard that dominates it.
- **REFUTED: "Every `confirm_callback=` in the tree is `None` or `lambda _prompt: True`."**
  Refuted by `cli\serve.py:310`. How established: full-tree enumeration of 45 sites.
- **NOW UNPROVEN, PREVIOUSLY ASSERTED: "`POST /v1/tools/confirm` has no consumer" and
  "`GATE_APPROVED` is unreachable on every path."** Neither was disproved, but the evidence
  they rested on (no real callbacks anywhere) is gone. Do not carry them as fact.
- **NOT ESTABLISHED: which of three sender defects caused the HTTP 400.** Slug, missing
  `max_tokens`, and missing Tls12 are all candidates. All three will be fixed together, so the
  attribution will remain unknown unless someone bisects it. Recorded so a future window does
  not claim a cause it never proved.
- **NOT ESTABLISHED: the construction site of the serving executor.** Deduced to be
  `_server_confirm_callback`-bearing; not traced.
### [ARCHIVE-W48-2026-09-11.md] 5. HAZARDS FOUND
- **MARK-OF-THE-WEB BLOCKS EVERY DELIVERED SCRIPT.** A `.ps1` downloaded from the chat fails
  with `PSSecurityException` / "not digitally signed" even though Gray's own scripts in the
  same directory run. Remedy, and the standing pattern for every future delivered script:
  `Unblock-File .\x.ps1` then `powershell -NoProfile -ExecutionPolicy Bypass -File .\x.ps1`.
  Nothing about the machine policy needs to change.
- **RE-DERIVING A WORKING TRANSPORT IS A SELF-INFLICTED DEFECT.** The new sender was authored
  from scratch and shipped three faults - wrong model slug (missing the `-a55b:free` suffix),
  no `max_tokens`, no forced Tls12 - every one of which was already solved in
  `ask-550b-554.ps1` sitting in the repo root. This is the 09/06 "author's resources first"
  rule applied to Gray's OWN scripts, and it is now a rule of engagement.
- **A BUNDLE BUILT FROM A STALE FILE LIST ANSWERS THE WRONG QUESTION.** `bundle-w48-gate.md`
  included `server\routes.py` on the strength of the W47 ":2297" fact. Even a successful send
  could not have answered question 1. Verify that the file you are bundling actually contains
  the line you are asking about, at build time.
- **POWERSHELL VARIABLE NAMES ARE CASE-INSENSITIVE.** The first assemble script defined
  `$Out` as the output filename and then `$out` as the line buffer. PowerShell treats those as
  ONE variable: the buffer silently overwrote the path and `Set-Content` failed on an empty
  string. Never let two variables in a script differ only by case. Note that .NET
  `String.Replace` IS case-sensitive, which is what made the repair a two-line fix.
### [ARCHIVE-W48-2026-09-11.md] 6.9 CHANGED THIS WINDOW (W48)
- **`POST /v1/tools/test-execute` - LOCATION CORRECTED.** Registered at
  `server\agent_manager_routes.py:2142`, handler `test_execute_tool` at `:2143`. NOT in
  `routes.py`. The register's W47 entry pointing at `routes.py:2297` is wrong.
- **`ask-550b-w48-gate.ps1` - BUILT, NOT YET WORKING.** Self-contained bundler plus sender with
  the question embedded at the top per the 09/09 rule. Bundles whole files, resolves the
  OpenRouter key from `C:\Users\Admin\.openjarvis\cloud-keys.env` without echoing it, posts,
  writes `answer-w48-gate.md`. Currently fails on HTTP 400; three known defects listed in
  Archive 5. Output lands in the repo root. Keep as the template once fixed.
- **`bundle-w48-gate.md` - ON DISK, REBUILD BEFORE USE.** 364 KB, ~91 k tokens. Contains the
  wrong routes file.
- **`ask-550b-554.ps1` is PROMOTED to the authoritative cloud-send template.** Transport config
  to copy verbatim: endpoint `https://openrouter.ai/api/v1/chat/completions`, model
  `nvidia/nemotron-3-ultra-550b-a55b:free`, `max_tokens 6000`, Tls12 forced at
  `[Net.ServicePointManager]::SecurityProtocol`, `TimeoutSec 900`.
- **Unchanged and still readable:** `dispatch.log` at
  `C:\Users\Admin\AppData\Local\OpenJarvis\logs\dispatch.log`, producer `_stubs.py:154`,
  rotating 2 MB x 4, `propagate = False`, INFO.
### [ARCHIVE-W48-2026-09-11.md] 7.9 CHANGED THIS WINDOW (W48)
No logging configuration changed. One clarification recorded from a full read of
`_get_dispatch_logger` at `_stubs.py:107-130`:
- The dispatch logger is a module-global singleton (`_dispatch_logger`, `:104`), attached once
  on first call, guarded by `if not lg.handlers`. It builds its own directory under
  `LOCALAPPDATA`, falls back to a `NullHandler` on any exception (`:126`) - meaning a failure
  to create the log directory is SILENT and produces a logger that discards everything. Worth
  noting as a blind spot: an empty `dispatch.log` and an absent `dispatch.log` are not
  distinguishable from inside the app.
- `lg.propagate = False` at `:128` confirms dispatch records never reach `backend.log`. The two
  sinks are disjoint by construction, which is why CONFIRM greps against `backend.log` return
  zero. That is expected behaviour, not a defect.
### [ARCHIVE-W48-2026-09-11.md] 8.6 CHANGED THIS WINDOW (W48)
**PATH: `POST /v1/tools/test-execute` - PARTIALLY CORRECTED, ONE HOP STILL UNKNOWN.**
- Entry point: `server\agent_manager_routes.py:2142`, `@tools_router.post("/test-execute")`,
  handler `test_execute_tool` (`:2143`). Gated by `OPENJARVIS_TEST_EXEC` (disabled bodies at
  `:2161`, `:2171`). Failure path logs at `:2247`.
- Call chain into the executor: **UNKNOWN. Not traced this window.** The W47 entry naming
  `system\builder.py:168/193` with `ToolExecutor(tool_list, bus)` is REFUTED - see Archive 2.1.
- Which executor serves it: an executor with `interactive=True` and a BLOCKING
  `confirm_callback` that returns False after `confirm_registry._DEFAULT_TTL` (120.0 s).
  Deduced, not traced. Strongest candidate `_server_confirm_callback`, `cli\serve.py:310`.
- Confirmation gate on this path: **LIVE, and it blocks.** Not auto-approved, not absent. This
  is the first path in the register demonstrated to actually reach `_stubs.py:377`.
- Dispatch internals, now fully read: `execute` wrapper `:211-246` (ATTEMPT, inner call,
  OUTCOME on all paths incl. `BaseException` at `:230`); `_execute_inner` `:248`; seven early
  returns - unknown tool `:251`, bad args `:261`, boundary block `:274`, capability denied
  `:282`, taint violation `:310`, gate-no-callback `:338`, gate-denied/timeout `:400`; start
  event `:428`; execution under a single-worker `ThreadPoolExecutor` with
  `future.result(timeout=...)` at `:438-440`; tool timeout handling `:441-460` setting
  `metadata.timed_out` and `outcome_verified=False`.
- Event bus traffic on this path: `TOOL_CONFIRM_REQUEST` (`:363`), `TOOL_CONFIRM_RESOLVED`
  (`:386`), then `TOOL_CALL_START` (`:429`) only if approved. `CAPABILITY_DENIED`,
  `TAINT_VIOLATION`, `TOOL_TIMEOUT` on their respective branches.
- Human present: no. That is the point of the instrument.
**PATHS EXCLUDED AS THE 120 s SOURCE:** the four managed-agent executors at
`agent_manager_routes.py:720/721`, `:1205/1206`, `:1562/1563`, `:1639/1640`. All pass
`confirm_callback=lambda _prompt: True`. On those paths the gate is AUTO-APPROVED: the callback
returns instantly and truthfully approves, execution proceeds, and `GATE_*` reasons are
unreachable. **Recorded as a capability-safety statement in its own right: four managed-agent
paths approve every confirmation-requiring tool automatically, with no human in the loop.**
### [ARCHIVE-W48-2026-09-11.md] 11.4 CHANGED THIS WINDOW (W48)
W48 is the ninth consecutive observability window. Capability moved toward the executive
assistant goal: **none.** No requirement advanced. The requirements-measurement window is now
at its tenth deferral.
What the window bought, stated honestly: the picture of the confirmation gate got BETTER, not
worse. W47 closed believing the gate was universally dead - no consumer, `GATE_APPROVED`
unreachable everywhere. W48 shows a real callback exists and blocks for the full TTL on at
least one path, so some of that machinery is live. Against that, W48 also establishes that four
managed-agent paths auto-approve everything, and the two destructive mailbox tools remain
ungated and unchanged since W47.
The argument from 11.3 stands and strengthens: nine windows of observability work, and the
program still cannot state what percentage of the initial requirements are met. The measurement
window should come BEFORE further debugging. It has now lost to a live trace ten times, and
each time the reason was good. That pattern is itself the finding.
### [ARCHIVE-W48-2026-09-11.md] 12.4 CHANGED THIS WINDOW (W48)
Two rules added.
**THE LOG LINE IS EVIDENCE ABOUT THE SYSTEM, NOT ONLY ABOUT THE INSTRUMENT.** When a classifier
whose logic you can read reports something your model of the system says is impossible, the
default suspicion must fall on the model, not the reading. W47 closed with "the instrument is
not yet trustworthy" and held a correct patch uncommitted for a window on that basis. The
instrument was faithful the whole time; the register was wrong. Before doubting an instrument,
read the instrument's decision procedure end to end and ask what the report would REQUIRE to be
true.
**REUSE GRAY'S OWN WORKING SCRIPT BEFORE AUTHORING A NEW ONE.** The 09/06 "author's resources
first" rule extends to the repo's own working artifacts. A re-derived 550B sender shipped three
defects - all three already solved in `ask-550b-554.ps1` in the repo root. Read the working one
first, then enhance it.
**Handoff process note:** the 09/10 scaffold-by-extraction rule was executed for the first time
this window and worked as designed. One command in exchange one sliced sections 6-12 verbatim
from the prior archive and prepended stubbed 1-5; 687 lines, zero retyping, no register
rewritten. The only authored content at close is sections 1-5 plus these five deltas. Keep it.
### [ARCHIVE-W49-2026-09-11.md] 1. WINDOW SUMMARY
W49 opened on the W48 list and closed four of its five items in seventeen exchanges, at a
measured cost of roughly 15 percentage points of window budget. Nothing was run. No server was
started. Every finding in this window came from reading source files wide and comparing them to
what the register claimed. Two commits were produced and pushed to both remotes: `f7d3138`
(`_stubs.py`) and `ab173c4` (`mailbox_tools.py`).
The window's shape was set in exchange one by building the handoff scaffold before doing any
work, per the 09/10 cost rule. That cost a single command and carried sections 6-12 verbatim
from the W48 archive starting at line 146. The scaffold was 792 lines on creation, against an
estimate of 687 - the archive had grown, which was noted and not chased.
The first substantive act was a judgement call about cost. Action 1 on the W48 list was to
repair a three-defect PowerShell sender and re-send a 364 KB bundle to the 550B cloud model.
Action 2 was to read `cli\serve.py` around line 310. Before authoring the sender, the sizing
of the three candidate bundle inputs was run alongside a proposal: the local read might answer
the same question for two orders of magnitude less. Gray agreed to verify before executing.
That call was correct and it decided the window. Two `Get-Content` slices - `serve.py:280-400`
and `agent_manager_routes.py:2120-2270` - closed the entire question the bundle had been built
to ask. The 550B send was dropped as obsolete rather than deferred, and the W48 artifacts
supporting it were marked for deletion.
Reading those two regions established the confirmation gate's construction site and its
consumer in one pass, resolved the W47/W48 contradiction definitively on source, and produced
four corrections to the carried register. It also surfaced, incidentally, that `cli\serve.py`
is 248 KB across 655 lines - far more damage than the known `:554` literal accounts for.
The commit of `_stubs.py` was then stopped at the diff. The diff showed two comment lines whose
em dashes had become three-character cp1252 sequences - lines the dispatch-outcome patch had no
functional reason to touch. The patch script had re-encoded the file on write. Gray asked
directly whether a push of that damage would be revertible; it would have been, but the real
cost identified was silence rather than unrecoverability: mojibake in comments breaks nothing at
runtime, so it becomes the baseline and every later patch builds on it, which is the road
`serve.py` is already far down. A full-file scan found five affected lines, all comments and
one docstring, zero code. They were rewritten to ASCII and the file committed clean.
The window's last act was the `mailbox_tools.py` safety note, and it reversed a register entry
that had been the top-line safety item for many windows. Gray's correction supplied half of it -
the tools move messages to Trash and only a human deletes, so "destructive" was wrong. Reading
the author's own safety note at `:12-31` supplied the other half: the tools are not ungated
either. A two-key interlock is in force and always was. The note's stated premise was stale, but
its conclusion was still right, for a reason the note could not have known. Item 3 moved from
"largest live capability-safety hole" to "blocked on evidence."
### [ARCHIVE-W49-2026-09-11.md] 2.1 The construction site - `cli\serve.py:290-321`
Read wide (280-400) rather than the brief's suggested 300-340, per READ WIDE.
`_server_confirm_callback` is defined at `:310` inside the `accepts_tools` block opened at
`:295`. Its body is three statements: fetch `CURRENT_CONFIRM_ID` from `_stubs` (`:311`), return
False immediately if absent (`:312-313`), otherwise return `_cr.wait(_cid) == _cr.APPROVED`
(`:314`). It is assigned into `agent_kwargs["confirm_callback"]` at `:317`, alongside
`agent_kwargs["interactive"] = True` at `:316`, and both are consumed by
`agent_cls(engine, model_name, **agent_kwargs)` at `:321`.
The whole block is gated by `OPENJARVIS_CONFIRM_INTERACTIVE`, read at `:298-300` with a default
of `"1"` and tested against a false-set at `:301-306`. **The gate is LIVE BY DEFAULT on the chat
path.** The marker comment at `:290-294` calls this "Defect 6 / 6d" and states the opt-in was
designed so unattended entry points never inherit a blocking gate.
This body matches the measured probe behaviour exactly. A 120.007 s block returning False is
`_cr.wait` reaching its TTL at `:314`. Nothing else in the callback can consume time.
### [ARCHIVE-W49-2026-09-11.md] 2.2 The consumer - `agent_manager_routes.py:2127-2270`
`test-execute` is at `:2142`, handler `test_execute_tool` at `:2143`. Its own comment block at
`:2127-2141` states the design intent: it uses the LIVE chat agent's executor and constructs
nothing, so what is measured is the instance 6d wired, on serve.py's bus, with the real confirm
callback and the real agent id.
The code confirms the comment. `:2177` reads `request.app.state.agent`; `:2178` takes its
`_executor`; `:2179-2186` returns 409 if that is None. There is no constructor call anywhere in
the handler. **The executor serving the probe is the instance built at `serve.py:321`.**
The chain is therefore closed end to end on source: probe -> `app.state.agent._executor` ->
built at `serve.py:321` with `interactive=True` and `_server_confirm_callback` -> blocks in
`_cr.wait` -> returns False at TTL -> ToolResult content -> `_outcome_reason` classifies
`GATE_TIMEOUT`. `reason=GATE_TIMEOUT` was faithful. The W47 register entry was wrong.
Route surface, recorded because no prior brief carried it correctly:
- **202** accepted (`:2262-2270`), NOT 200. Body carries `run_id`, `turn_id`, `tool`, `marker`.
- **403** twice, distinct reasons: `OPENJARVIS_TEST_EXEC` not set (`:2156-2165`), bind not
  loopback (`:2167-2175`).
- **409** no live agent executor (`:2179-2186`) - carried by no prior brief.
- **400** tool name missing (`:2200-2204`).
- **404** tool not on the live agent (`:2213-2221`), body includes the live tool inventory.
- **422** tool does not declare `requires_confirmation` (`:2223-2230`).
- Execution is fire-and-forget: `_run` (`:2240`) sets `CURRENT_TURN_ID`, calls
  `_executor.execute(_call)` at `:2245`, dispatched via `asyncio.to_thread` at `:2258` with the
  task held in an `app.state._testexec_tasks` set (`:2254-2260`).
### [ARCHIVE-W49-2026-09-11.md] 2.4 The mailbox safety note - `mailbox_tools.py:1-57`
The docstring at `:12-31` is a deliberate SAFETY NOTE explaining why `requires_confirmation` is
NOT set. Its argument, as written: `ToolExecutor.execute` treats the flag as a hard requirement
rather than a prompt (quoted at `:17-19`); the server-side agent path builds its executor
without `interactive=True` and without a confirm callback (`:21-23`); therefore a tool carrying
the flag does not ask for confirmation, it fails every call. The interlock is implemented in the
tool contract instead (`:26-28`): `dry_run` defaults True and returns a plan with exact counts,
and applying requires BOTH `dry_run=False` AND `confirm` set to the exact string
`CONFIRM DELETE`, defined as `CONFIRM_TOKEN` at `:55`.
The premise at `:21-23` is now false - `serve.py:316-317` sets both. The conclusion still holds
for a different reason, established in 2.1: the callback blocks to the 120 s TTL. The note was
corrected to record both, plus Gray's naming correction, and committed as `ab173c4`.
Tool inventory from the bounded scan: `MailboxListAccountsTool` (`:157`),
`MailboxUsageReportTool` (`:186`), `MailboxFindMessagesTool` (`:252`), `MailboxMoveToTrashTool`
(`:454`), `MailboxEmptyFolderTool` (`:739`). Two write-capable, matching the register's count.
`mailbox_empty_folder` has NOT been read and its semantics are UNVERIFIED - by name it may not
be a move. Open question for W50.
### [ARCHIVE-W49-2026-09-11.md] 3. NEGATIVE RESULTS
- **The 550B send was never made, and did not need to be.** `bundle-w48-gate.md` (364 KB,
  ~91 k tokens) was built in W48 and is now obsolete. The three sender defects identified in the
  W48 brief were never tested, so which one caused the HTTP 400 remains UNPROVEN and is now
  moot. Do not carry the sender forward as a pending item.
- **`ask-550b-554.ps1` is single-file, not multi-file.** It binds one `$src` and numbers one
  file. The W48 brief's instruction to "swap `server\routes.py` out of `$Files`" described a
  script shape the template does not have. A multi-file question needs a `$Files` loop written
  around its transport block.
- **"Two ungated destructive mailbox tools" was wrong on both words** and had been the register's
  top-line safety item for many windows. They are interlocked (2.4) and they move to Trash.
- **`POST /v1/tools/confirm` having no consumer is STILL not established, and the question has
  changed.** W48 downgraded it from fact to unproven. W49 sharpens it: `_cid` must have been
  truthy, because `serve.py:312-313` returns False instantly otherwise, and the probe took
  120.007 s. So an id WAS registered and `_cr.wait` still reached TTL. The question is no longer
  "is there a consumer" but "why did a registered id fail to resolve."
- **The extent of the mojibake damage across the tree is UNKNOWN.** Two files are confirmed
  affected (`serve.py`, `_stubs.py`). No tree-wide scan has been run in this window. Gray
  recalls a scan roughly a month ago and believes it was `_stubs.py`-scoped; that was NOT
  verified, by his own standing instruction not to re-derive prior-window work without approval.
### [ARCHIVE-W49-2026-09-11.md] 4. HAZARDS
- **THE PATCH TOOLING RE-ENCODES WHOLE FILES.** The dispatch-outcome patch script damaged five
  comment lines in `_stubs.py` that it had no functional reason to touch. Any patch script that
  reads and rewrites a file can do this. **Scan the whole working file for non-ASCII before
  committing any patch**, not just the diff - the diff only shows lines the patch touched.
- **`cli\serve.py` IS 248 KB ACROSS 655 LINES.** The known `:554` literal (49,789 chars)
  accounts for roughly a fifth of that. `:347` is visibly corrupted. The file is in worse
  condition than the register records, and anything that reads and rewrites it risks compounding
  the damage. Do not run a patch script against `serve.py` without a byte-level backup.
- **Setting `requires_confirmation=True` on the mailbox tools TODAY would break them.** Every
  call would park 120 s on `_cr.wait` and then fail - the exact failure the original safety note
  feared, arriving by a different road. The flag is correct only after the confirm consumer is
  proven.
- **The dry-run interlock depends on an exact string.** `CONFIRM_TOKEN = "CONFIRM DELETE"` at
  `:55`. A model producing `"CONFIRM_DELETE"` or lowercase fails closed, which is safe, but
  means interlock failures will look like tool failures in the logs.
- **`mailbox_empty_folder` is unread.** Its name does not promise a move. Verify before assuming
  it shares `move_to_trash` semantics.
### [ARCHIVE-W49-2026-09-11.md] 5. SDD / SDP FEED
**Confirmation gate, Defect 6 - the mechanism is now documentable end to end on the chat path.**
*Plain-language version, per the 09/02 standing requirement:* When Jarvis wants to use a tool
that could change something important, it is supposed to stop and ask first. This window found
where that "stop and ask" is switched on: when the server starts up, it hands the assistant a
little function whose only job is to wait for a human to say yes. It also found that the switch
is ON unless somebody deliberately turns it off. So the asking part works. What does not work
yet is the answering part - when a human says yes, that answer is not getting back to the
function that is waiting. It waits two minutes, gives up, and treats the silence as a no. That
is the safe way to fail, but it means the tool never runs. Fixing the answering part is the
only thing left between here and a working gate.
*Technical version, for the registry/payload/transport/threading chapter Gray flagged as needing
GREAT DETAIL:*
- **Registry:** `openjarvis.core.confirm_registry`, 197 lines, UNREAD as of W49 close.
  `_cr.wait(cid)` blocks; `_cr.APPROVED` is the success sentinel. TTL observed at 120 s.
- **Payload:** the id travels via `_stubs.CURRENT_CONFIRM_ID`, a ContextVar, read at
  `serve.py:311`. Turn id travels via `_stubs.CURRENT_TURN_ID`, set at
  `agent_manager_routes.py:2243` and reset in a finally at `:2250`. Confirm ids are bus-only and
  never logged - carried forward from W48 and unchanged.
- **Transport:** the gate emit goes to the event bus; the human answer is expected at
  `POST /v1/tools/confirm`. The link between that route and `_cr` resolution is the ONE
  UNPROVEN SEGMENT.
- **Threading model:** the executor call runs off the event loop. `test-execute` dispatches
  `_run` through `asyncio.to_thread` (`:2258`), so `_cr.wait` blocks a worker thread, not the
  loop. This is why a 120 s gate timeout does not hang the server. The chat path's threading is
  NOT established here and should be confirmed before the SDP chapter is written.
- **Opt-out:** `OPENJARVIS_CONFIRM_INTERACTIVE`, default ON, `serve.py:298-306`. Design intent
  per `:290-294` is that unattended entry points never inherit a blocking gate.
**Capability-safety chapter correction.** The SDP must NOT describe the mailbox tools as ungated
or destructive. The correct description is: two write-capable tools protected by a two-key
contract interlock (dry-run-by-default returning exact counts, plus an exact-string confirm
token), performing a MOVE to Trash, with deletion reserved to the human. The residual risk is
scale, not permanence - one call can relocate a very large number of messages, and Trash
auto-purge gives the reversal a finite window. The value of a future confirmation prompt is that
it surfaces the COUNT and the SCOPE before execution.
**Execution path register delta** - see section 8 for the carried register. Path `test-execute`
is now fully specified: entry `POST /v1/tools/test-execute` (`agent_manager_routes.py:2142`);
executor NOT constructed, borrowed from `app.state.agent._executor` (`:2177-2178`); confirmation
gate LIVE via `serve.py:316-317`; emits to serve.py's bus; human present but answering through a
channel whose resolution is unproven; fire-and-forget on a worker thread (`:2258`).
### [ARCHIVE-W50-2026-09-12.md] SECTION INDEX
1. Window summary
2. Evidence
3. Negative results
4. Hazards
5. SDD/SDP feed
5D. W50 deltas to the carried sections
6-12 carried verbatim from W49
---
### [ARCHIVE-W50-2026-09-12.md] 1. WINDOW SUMMARY
W50 had ONE subject: prove or disprove the `/v1/tools/confirm` consumer, carried out of
W49 as "the last thing standing between the gate and working."
It was disproved as a defect. The consumer works. The window closed the item by
DISPROOF, not by a fix, and it changed nothing in the tree - no patch, no commit to
`src\`. The deliverable is an instrument plus a measurement.
Narrative, in order:
W49 handed forward a sharpened question: `_cid` was truthy and `_cr.wait` still hit TTL
at 120.007 s, so the gate registered an id and the waiter still expired. The brief read
that as an unproven consumer.
Exchange one built the handoff scaffold by extraction per the 09/10 rule - one command,
785 lines, sections 6-12 pulled verbatim from the W49 archive.
The wide read of `core\confirm_registry.py` (197 lines, whole) settled the registry
question on source alone. `wait()` has exactly one fast path at 129-134: an unknown id
returns TIMEOUT instantly, a recorded decision returns instantly. Neither fired. A
120.007 s block is therefore only reachable when the entry WAS in `_PENDING` and no
`resolve()` arrived inside the budget. That does not indict the registry. It proves the
registry did its job.
Memory then produced the reframe. The confirm consumer had already been proven live
three times - 08/22 approve at HTTP 200 in 186 ms with `tool_call_start` 287 ms after
the emit, 08/24 two gates inside one turn, 08/30 `confirm_id` surviving the v3
redaction on the wire. And the 08/22 run had ALSO produced a 120.004 s TTL expiry,
recorded at the time as expected because nobody answered. The W49 120.007 s and the
08/22 120.004 s are the same measurement of the same non-event.
Gray's call was to trace it rather than argue it. Correct call: the reframe was an
argument from the register, and W47's own lesson says a carried register describes the
system as of when it was written.
Before building, the route contracts were verified rather than trusted. A bogus-tool
POST to `test-execute` returned our handler's 404 with a live tool inventory, proving
route mounted, `OPENJARVIS_TEST_EXEC` set in the live process, bind loopback accepted,
and a live agent executor present - four guards cleared in one call. Then a 311-line
wide read of `agent_manager_routes.py` 1980-2290 put both handlers on the record whole.
The instrument was two-phase by design and by Gray's choice: phase A listens and
deliberately does not answer, phase B answers with a deny. The contrast is the finding;
neither phase alone discriminates.
v1 failed on the client, not the server - the asyncio `websockets` client hung in the
opening handshake. A .NET `ClientWebSocket` against the identical URL reached Open in
92 ms, which located the fault immediately. `websockets` is 17.0.1 in `.venv` and the
legacy asyncio client is gone. The sync client opened in 56 ms. v2 was rebuilt on it.
v2 ran clean and produced the answer.
---
### [ARCHIVE-W50-2026-09-12.md] 2. EVIDENCE
`probe_confirm_trace_w50_v2.py`, repo root, marker `openjarvis-confirm-trace-w50-v2`.
Single invocation, non-interactive, ~3 minutes. Nothing executed in either phase.
PHASE A - listen only, no answer
```
[trigger] test-execute -> HTTP 202 in 48 ms
[trigger] run_id=4791c868  turn_id=test-4791c868
[ws] +  0.000s  tool.confirm.request    turn_id=test-4791c868 [MINE]
[gate] CONFIRM FRAME MATCHED. confirm_id=PRESENT
[ws] +119.986s  tool.confirm.resolved   turn_id=test-4791c868 [MINE]
[gate] RESOLVED decision=timeout (119.986s after the request frame)
```
PHASE B - listen and auto-deny
```
[trigger] test-execute -> HTTP 202 in 7 ms
[trigger] run_id=0ba5048f  turn_id=test-0ba5048f
[ws] +  0.001s  tool.confirm.request    turn_id=test-0ba5048f [MINE]
[gate] POST deny -> HTTP 200 in 7 ms
[gate] BODY: {'confirm_id': 'c730fc892cf7496a8a5fde1b71da2e5b', 'tool': 'shell_exec',
       'turn_id': 'test-0ba5048f', 'state': 'resolved', 'decision': 'denied'}
[ws] +  0.010s  tool.confirm.resolved   turn_id=test-0ba5048f [MINE]
[gate] RESOLVED decision=denied (0.014s after the request frame)
```
**THE LOAD-BEARING RESULT IS THE 119.986 s AGAINST THE 0.014 s.** Same instrument, same
tool, same server process, same executor, back to back, three seconds apart. ONE
variable differed: whether anything answered. An 8,500x spread cannot be produced by
anything else. Neither phase alone would have proven it - a lone timeout looks like a
break, a lone fast deny does not explain the W49 reading.
Subsidiary facts established by the same run:
- The confirm route round trip is 7 ms. Registry, route, bus and WS are all healthy.
- The deny path is proven live for the first time. Every prior proof (08/22, 08/24) was
  an approve. Gray's 08/29 ruling that the first live run denies is now satisfied, and
  nothing was executed to satisfy it.
- `turn_id` was PRINTED and matched on the wire in both phases (`test-4791c868`,
  `test-0ba5048f`). The 08/30 honest limit - the probe never displayed `turn_id`, so
  frame attribution was by inference - is CLOSED.
- `confirm_id` PRESENT in both frames, corroborating the 08/30 redaction finding.
- The emit is effectively instantaneous after the 202: +0.000 s and +0.001 s.
SOURCE READS THIS WINDOW, all wide, none sliced:
- `core\confirm_registry.py`, 197 lines, whole.
- `probe_ws_bare_subscribe.py`, 193 lines, whole.
- `server\agent_manager_routes.py` 1980-2290, 311 lines, both handlers whole.
CONTRACTS NOW VERIFIED IN SOURCE, previously carried on an 08/20 register entry:
- `POST /v1/tools/confirm` (`:2046-2125`). Body `{confirm_id, decision}`. Accepts
  approve/approved/deny/denied, normalized at `:2062-2067`. 400 missing id, 400 bad
  decision, 404 unknown or expired, 200 first resolve, 409 already resolved carrying
  the held decision. It calls `_cr.get()` at `:2085` BEFORE `resolve()`, so an expired
  id gives 404 and never a false 200.
- `POST /v1/tools/test-execute` (`:2142-2271`). Returns 202 with
  `{accepted, run_id, turn_id, tool, marker}`; `turn_id` is `"test-" + run_id`
  (`:2233`). Guards in order: 403 flag unset (`:2157`), 403 bind not loopback
  (`:2167`), 409 no live executor (`:2179`), 400 no tool (`:2200`), 404 unknown tool
  with a live inventory (`:2213`), 422 tool does not require confirmation (`:2223`).
  It reads `app.state.agent._executor` at `:2177-2178` and constructs nothing.
`confirm_registry.py` structure, on the record:
- Module-level `_PENDING` dict guarded by `_LOCK` (`:46-47`). `_DEFAULT_TTL = 120.0`
  (`:43`), overridable by `OPENJARVIS_CONFIRM_TTL` only, deliberately not from
  `config.toml` because that file is machine-regenerated and can silently revert
  (`:51-52`).
- `wait()` fast paths at `:129-134`. Unknown id returns TIMEOUT - fail closed, and the
  docstring states why: a prompt lost to the lossy ws `put_nowait` is indistinguishable
  from a human who never looked.
- Decisions are WRITE-ONCE (`:19-23`, enforced at `:161`). A timeout is NOT a refusal
  and the two must stay distinct all the way into the ToolResult.
- Reaping happens inside `register()` (`:110`), no background task.
- `resolve()` raises ValueError on anything but the full words `approved`/`denied`
  (`:155-158`); the route normalizes first. The asymmetry recorded 08/20 is confirmed.
---
### [ARCHIVE-W50-2026-09-12.md] 3. NEGATIVE RESULTS
**THE `/v1/tools/confirm` CONSUMER IS NOT BROKEN.** W49's headline item - "the last
thing standing between the gate and working" - was based on a stale premise, not a
defect. Do not carry it forward. Established by the phase A / phase B contrast above,
and independently by the source structure of `wait()`.
**THE 120 s TTL EXPIRY IS NOT A SYMPTOM.** It is the designed fail-closed outcome when
no client answers. Three separate measurements now agree: 120.004 s (08/22), 120.007 s
(W49), 119.986 s (W50). Any future window that sees ~120 s should read it as "nobody
answered," not as a fault.
**THE `websockets` HANDSHAKE HANG WAS NOT THE SERVER.** A .NET `ClientWebSocket`
reached Open in 92 ms against the identical URL while the python asyncio client timed
out at 15 s. The WS bridge, the bus fix and the route are all sound; the 08/21 and
08/22 WS proofs remain valid.
**THE W49 BRIEF'S ACTION 1 REQUIRED NO CODE CHANGE.** The window ends with the working
tree untouched under `src\`.
---
### [ARCHIVE-W50-2026-09-12.md] 4. HAZARDS
**`probe_ws_bare_subscribe.py` IS DEAD IN THIS VENV AND THE REGISTER DID NOT KNOW.**
`websockets` 17.0.1, python 3.12.10, `hasattr(websockets, 'legacy')` is False. The
legacy asyncio client the probe was written against was removed in 15.x. The registered
listener has been silently unusable since whenever that upgrade landed, and no window
noticed because nobody ran it. Two consequences: the diagnostic tooling register needs
this entry corrected, and any other instrument written against `websockets.connect`
before the upgrade is suspect. Replacement idiom, proven this window:
`from websockets.sync.client import connect` then `connect(url, open_timeout=15)` and
`conn.recv(timeout=...)`, which raises `TimeoutError`.
**A DEPENDENCY UPGRADE CAN KILL AN INSTRUMENT SILENTLY.** This is the same family as the
09/06 "instrumentation you cannot read is instrumentation you do not have," with a new
cause: the instrument is readable and correct but no longer runnable. Nothing in the
tree warns about it. An instrument that has not been run since its dependencies moved
is UNVERIFIED, not available.
**PHASE A PARKED A WORKER ON THE SHARED ThreadPoolExecutor FOR 120 s.** Third
measurement of this. `asyncio.to_thread` uses the loop's default executor, shared with
speech transcription and webhooks. The 08/22 finding that the agent RE-REQUESTS after a
TIMEOUT ToolResult means an unanswered confirm on the chat path costs N x 120 s, not
120 s once. Unchanged, and still the strongest argument for the 6e browser half.
**UNVERIFIED ASSUMPTION THAT DID NOT BITE:** `shell_exec` argument name was assumed to
be `command`. It was never validated, because neither phase executed the tool. If a
future run needs actual execution, confirm the arg name first.
**MOJIBAKE STILL PRESENT IN `agent_manager_routes.py`.** Visible at `:1993` and `:2273`
in this window's read - the double-encoded box-drawing section rules, pre-existing, not
caused by us, cosmetic (comment lines only). W49's tree-wide mojibake audit remains
unrun and unasked.
---
### [ARCHIVE-W50-2026-09-12.md] 5. SDD / SDP FEED
**THE CONFIRMATION GATE ROUND TRIP IS NOW FULLY DOCUMENTED END TO END AND ALL OF IT IS
MEASURED.** This is the SDP's Defect 6 confirmation-gate chapter, and every link now has
a source citation and a live timing.
Plain-language version, per the 09/02 requirement that an eight-year-old could follow it:
> When Jarvis wants to do something that could matter - like run a command on the
> computer - it is not allowed to just do it. It has to stop and ask first.
>
> So it writes a note with a special number on it and puts the note in a box. Then it
> shouts the number out of the window so anybody listening outside can hear it. Then it
> waits by the box.
>
> If somebody outside hears the number and shouts back "yes" or "no", the answer goes
> in the box, Jarvis wakes up straight away, and it does what it was told. That takes
> about the time it takes to blink.
>
> If nobody is listening out of the window, nobody shouts back. Jarvis waits by the box
> for two whole minutes, and then gives up and does NOT do the thing.
>
> Waiting two minutes and giving up is not Jarvis being broken. That is Jarvis being
> careful. It means: if I cannot ask a person, I do not do it.
>
> What we found this window is that there is nothing wrong with the box, or the note,
> or the number, or the shouting. All of that works. The only thing missing is that
> the window Jarvis normally shouts out of - the chat screen a person actually looks
> at - has nobody standing at it yet. We can put our own listener there with a script,
> and when we do, it works perfectly. We just have not built the one for the person.
Technical version, with the evidence for each link:
1. GATE. `tools\_stubs.py:265` `if tool.spec.requires_confirmation:`. Only three specs
   in the tree declare it: `agent_tools.py:289`, `git_tool.py:283`, `shell_exec.py:71`.
2. REGISTER. `confirm_registry.register()` creates the entry, reaps expired ones
   inline, returns a uuid4 hex. TTL 120 s from `_DEFAULT_TTL`.
3. CORRELATE. `CURRENT_CONFIRM_ID` ContextVar carries the id to the callback, which
   receives only a prompt string and could not otherwise learn it.
4. EMIT. Seven fields on the bus, `agent_id` inside `data` because `Event` is
   `slots=True`. Measured this window at +0.000 s and +0.001 s after the 202.
5. TRANSPORT. `app.state.bus` -> `create_ws_router` (the 08/22 one-line bus-split fix)
   -> `/v1/agents/events`. Bare subscription, no `agent_id` filter.
6. WAIT. `_server_confirm_callback` at `cli\serve.py:310`, assigned `:317`, alongside
   `agent_kwargs["interactive"] = True` at `:316`, consumed at `:321`. Gated by
   `OPENJARVIS_CONFIRM_INTERACTIVE`, default ON.
7. ANSWER. `POST /v1/tools/confirm` -> `_cr.resolve()` -> `Event.set()`. Measured 7 ms.
8. RELEASE. Waiter wakes, three-way ToolResult. Measured 0.014 s end to end.
9. NO ANSWER. TTL, `decision=timeout`, fail closed, tool does not run. Measured
   119.986 s.
THREADING MODEL, load-bearing and now doubly confirmed: the tool chain runs on an
`asyncio.to_thread` worker while the inbound POST is served on the loop thread, which
is why the registry uses `threading.Event` and never `asyncio.Event`. `Event.set()`
from the loop thread is non-blocking, so the POST handler returns immediately - the
7 ms measurement is the observable consequence of that design choice.
EVIDENCE STANDARD, for the SDP methods chapter. The 400-not-404 template (08/20) gets a
second worked example: a verification is worth only what it can DISCRIMINATE. A lone
timeout is consistent with both a broken consumer and an unanswered prompt. Only the
paired run separates them. State, for every acceptance test in the SDP, what a passing
result RULES OUT.
SAFETY PROPERTY, carried forward unchanged: an unauthed bare WS client on loopback
receives an answerable `confirm_id`. Anything that can reach the socket can answer a
gate. Blast radius local because bind is loopback. Socket auth deferred by Gray's 08/29
ruling.
---

