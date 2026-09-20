# HANDOFF - 2026-08-24 TENTH WINDOW
# THE 09:24 NO-BLOCK IS EXPLAINED. THE GATE IS DETERMINISTIC; THE EXECUTOR IS NOT.
# TRACED FROM ANOMALY TO MECHANISM IN ONE READ-ONLY WINDOW. NO SOURCE TOUCHED.

Supersedes `HANDOFF-2026-08-24-D-W9-GATE-LIVE-PROVEN-FIVE-CYCLES-CONFIRM-FRAMES-CAPTURED.md`
for state. Everything in that file stands EXCEPT its section 6 framing, which is RETRACTED and
replaced by section 3 below, and its next-action item 1, which is now CLOSED TO THE
CONSTRUCTION BOUNDARY. Its sections 4, 5, 10, 11, 12 are CARRIED FORWARD; only deltas restated.

**Actions this window: ZERO source patches. Zero host changes. Zero probes written. Fourteen
read-only reads. One unplanned PC reboot (hang, unrelated to OpenJarvis). Nothing left running.**

---

## 0. STANDING RULES FOR THE NEXT WINDOW

Rules 1-16 carry forward UNCHANGED. Three additions, all earned this window:

17. **PIN THE DETAIL OF EVERY WINDOW, INCLUDING THE NEGATIVE RESULTS.** Gray's instruction,
    08/24, and it is now standing. Every handoff documents its window in detailed narrative and
    records what a thing turned out NOT to be and HOW that was established - not only what
    changed. A window that changed nothing still produced knowledge, and that knowledge must be
    retrievable as an SDD artifact. Gray built this same learning into his Cody infrastructure
    agent. **This window is the proof case: zero changes, five theories killed, one mechanism
    found.** Carry this instruction forward in every subsequent handoff.

18. **THE 15-EXCHANGE FLAG IS A FLAG, NOT A STOP.** Do not cut a live trace to write a handoff.
    Flag it, say so, and finish the thread. Gray called this explicitly at exchange 15 of this
    window; the trace ran to 22 and closed properly.

19. **AN "ANOMALY" IS USUALLY A MISSING VARIABLE, NOT A FLAKY CONTROL.** Before calling any
    safety mechanism unreliable, enumerate what differs between the firing and non-firing cases
    down to the object identity. This window's entire premise - "a gate that fires on five runs
    and not on a sixth is not a gate" - was wrong, and it was wrong in the dangerous direction.

---

## 0.5 CARRIED WORKSTREAMS - PARKED, DATED, AND NOT FORGOTTEN

**Standing instruction, added 08/24: this section leads every handoff from here, and the day
counts get updated each window.** These are not checklist items. They are the two workstreams
OpenJarvis exists to deliver, and both have been parked while defect work consumed every window.
Each deferral was individually correct. Fifteen consecutive correct deferrals is still fifteen
days. **The purpose of dating them is to force the choice to be explicit: resume, or say out loud
it is not next and why.**

### WORKSTREAM V - VOICE STREAMING. REQUIREMENT ONE. PARKED 08/09. **15 DAYS.**

Gray's stated requirement one is "talk to Jarvis, Jarvis talks back." It was paused at his
direction on 08/09 so agents and email could move, and has not been touched since.

**Resume state - this is further along than it looks, and the frontend is exonerated:**

- The defect is a **6 to 9 second stall before the first `synthesizeSpeech` fetch resolves**,
  landing first audio ~0.3 s AFTER the text finishes rendering instead of ~7 s before. **This one
  defect is all that stands between the current build and acceptance criterion 4.**
- **Run D killed body consumption:** `res.blob()` took 9 ms. The delay is entirely in `fetch()`
  resolving its headers.
- **Run E killed "TTS defect" outright.** Plain control fetches of a 940 KB static asset, issued at
  800/1800/3000/4500 ms into a chat stream, **all resolved at the same wall-clock instant**. Not
  speech-related at all.
- **The phase breakdown settled the layer.** `fetchStart=+0`, TCP connect 3-10 ms, `requestStart`
  at +3 to +10 ms on every request, `responseStart` seconds late. **Browser queueing is dead for
  good. The block is SERVER-SIDE.**
- **Restated plainly: the backend on 8010 stops answering every same-origin request - including
  static files it is merely reading off disk - for several seconds during chat generation, then
  releases them all at one instant.**
- **DO NOT touch `ttsPlayer.ts`, the chunker, `synthesizeSpeech` or `apiFetch`.** All measured
  correct. The 08/09 recommendation to swap in a plain `<audio>` element is **dead** - it would
  replace ~40 ms of decode and schedule and leave the stall untouched.
- **Hypothesis, NOT confirmed - do not patch on it:** a blocked asyncio event loop in the chat
  generation path; an `async def` route doing blocking I/O would produce exactly this, a sync
  route in a threadpool would not.
- **Probe design is the known blocker.** Three poller runs in a row were null because overlap
  with a live generation was never established. **Do not run a fourth in that shape.** The
  replacement is designed: capture the app's own `/v1/chat/completions` request, fire it from
  PowerShell as a background job while polling `/health` and the 940 KB asset in the same script.
  Overlap guaranteed, self-timestamped, Chrome removed from the picture - **and non-interactive,
  which is the required shape.**
- **CHEAPEST UNTRIED TEST IN THE WHOLE THREAD:** start a brand-new conversation with empty
  history and reproduce the control run. **The full conversation history is resent unbounded on
  every turn** (~20 prior pairs in the captured body), which is also the leading candidate for the
  0.46 s to 52.7 s TTFT spread. If the stall vanishes on an empty history, the stall and TTFT are
  **one bug, not two**. If it persists, prefill is exonerated and Run E stands alone.
- **CROSS-LINK TO THIS WINDOW:** the captured chat body sends `"agent":"native_openhands"` **even
  when the UI dropdown reads "No agent (chat)"**. That is unverified, and it bears directly on
  section 7's carried design question about whether default chat is tool-capable - and on
  D-PROV-1, since it means the agent construction may not be what the UI implies.
- **Also open on requirement one's own file:** D-SPEECH-1, duplicate route registrations in
  `speech_router.py` (`/stream` at 207 AND 243, `/v1/speech/stream` at 171, handler
  `speech_stream_ws` defined at 172/208/244; later registration wins, earlier is dead code). And
  the stale `kokoro-tts` unit on .200, section 7 item 8.
- Closed and staying closed: TTS latency on ollama-mcp2 (cuDNN conv algo search, fixed 08/07).

### WORKSTREAM A - AGENTS OPERATIONAL. PARKED 08/12. **12 DAYS.**

Gray's deliverable, stated 08/11 and never rescinded: **OpenJarvis must manage the mailbox via
NLP.** The direct `connector_for()` calls were a targeting workaround for one session, not the
product. Since 08/12 the mailbox stack has been used only as a **test harness** for Defect 1 and
the confirmation gate - not advanced as a capability.

**Resume state - four layers are built and wired; the gaps are specific:**

- Built, registered, allowlisted and live-validated against the real Yahoo account: the
  `imap_mail` connector, five mailbox tools, and the provisioning utility. **Do not rebuild any of
  it** - Gray's assessment of that stack is positive and his 08/04 standing rule forbids side
  scripts. The deliverable is always connector plus tool surface plus config exposure plus managed
  agent.
- **GAP 1 - "newest" is not expressible.** `find_messages` has no sort anywhere, applies filters
  in folder-walk then UID-ascending order, and **early-returns on the first `limit` matches** - so
  with `folder` omitted it may never reach Inbox at all. Two separate fixes, do not conflate:
  (A) correctness - gather, sort by date descending, then limit; (B) new capability -
  `recent_messages(folder, limit)` plus a `mailbox_recent_messages` tool so the model has
  something to bind "my latest email" to. **Specced 08/09, never built.**
- **GAP 2 - category filing never ran.** All 18 category folders exist on the account and are
  effectively empty (top-10 folders hold ~13,803 of 14,006 messages). `patch_mailbox_categories.py`
  **never reached disk** - confirmed 08/05, state is consistent, nothing half-applied. Needs
  `ensure_folder()` / `move_to_folder()` on the connector plus tools, dry-run default and **no
  `CONFIRM DELETE` token** - moving is reversible and that token is reserved for destructive ops.
- **GAP 3 - no recipient-side filter.** `find_messages` filters `from_addr` only, so Gray's rule
  (delete self-sent mail to the Comcast address, keep self-sent to Yahoo) is not expressible.
  Needs `to_addr` on connector and tool.
- **GAP 4 - throughput.** Batch classification (N headers per call, N labels back) is the only
  workable shape; one message per LLM turn is impractical at ~29 tok/s with the scaffold floor.
  This is also the strongest argument for the planned cloud-model switch.
- **GAP 5 - modified UTF-7 not decoded.** `_list_folders` returns raw wire names, so `AT&T`
  displays as `AT&-T` and a model that selects the readable name fails. All 18 category folders
  are plain ASCII, so it is not blocking - but it is real.
- **CARRIED FROM 08/12, STILL TO DO on `native_openhands.py`:** raise `_default_max_turns` from 3
  to 10 so it is not an outlier when config is absent (**`config.toml` is machine-regenerated**,
  and the live value only reads 15 because the config line was raised), and teach
  `_strip_tool_call_text` at line 141 the Format 4 shape so a cap-out never leaks backend syntax
  to a family member.
- **Sender rulings are partially complete.** Approved and executed: USPS Informed Delivery.
  Approved, not executed: NYT, LinkedIn, Monster, ZipRecruiter. Excluded: Marriott, Costco,
  self-sent Yahoo. **Retail and newsletter senders were never ruled** - Gray wants to review each.
- **INTERSECTS THIS WINDOW DIRECTLY.** Section 7 item 7 (destructive mailbox posture) and D-EXEC-1
  are the same decision: flipping `requires_confirmation` on the destructive mailbox tools is
  pointless while a shadowing tool can silently replace them. And `mailbox_usage_report` at
  **150.8 s** dominates every mailbox turn, which is an architecture fact this workstream has to
  design around, not tune away.

### WHY THIS SECTION EXISTS

Neither workstream stalled because it was forgotten - both were captured accurately the whole
time. They stalled because Defect 1, then Defect 6, then the gate were each genuinely blocking,
and a live trace always beats a resume in the moment. **Capture was never the failure;
follow-through was.** Dating the park is the smallest mechanism that makes the cost visible.

**Apply the same treatment to the carried single items in section 7.** Items 8 through 11 have
been carried for multiple windows. Each should gain a first-seen window number, and any item whose
number keeps climbing should be closed or **deleted honestly** - deciding something is not worth
doing is a real result and costs nothing to record.

---

## 1. WHAT THIS WINDOW DID, IN ORDER - THE NARRATIVE

Read this section as the record of method. Every step is reproducible from the commands in it.

**Start state.** W9 closed items 1-3 and left the 09:24 no-block (run `ad902101`) as "the single
most important open item," blocking the 6e UI. That is where this window began.

**Step 1 - the run block.** `Select-String` on `agent.log` for `ad902101` returned the full run:
`ntc=2` on t1, two dispatches, RAWGEN-to-TURN gap of 0.359 s, `exit=final turns=2 dispatched=2`.
The model reported both `echo` commands succeeding with exit code 0. Immediate observation: every
gated run on record is `ntc=1`; this is the only `ntc=2` run in the log. That framed two
hypotheses - H1 process identity, H2 a multi-call dispatch branch.

**Step 2 - process table.** Both live python processes had started 18:31:44 that evening. Neither
served 09:24 or 11:17, so the process table could not settle H1. It did surface an unrelated
oddity: **two different interpreters serving port 8010** - `.venv\Scripts\python.exe` and system
`Python312\python.exe`, identical start time. Registered, not chased (see section 6).

**Step 3 - the reboot.** Gray's PC had hung and been rebooted; that explains the 18:31:44 pair.
`Invoke-RestMethod http://127.0.0.1:8010/health` returned `ok`, so the backend came up clean and
no state was lost - all evidence for this trace was already on disk.

**Step 4 - the day dump. H1 DIED HERE.** Eighty lines of RUNSTART/RAWGEN/RUNEND with the `raw=`
and `head=` payloads stripped. Gated runs (120-124 s RAWGEN-to-TURN gaps) appear on **08/23**
(`a36e8ddf` 122.2 s, `eb9bdabb` 122.2 s and 124.2 s, `0b72fbc9` 121.8 s) and on **08/24** both
before and after 09:24. There is no restart boundary and no time boundary. H1 is dead.

The dump also produced what looked like a much stronger finding: run `eb9bdabb` had **three
dispatches in one run** - gated, gated, then a 5.3 s dispatch that was NOT gated. Same run, same
process, same registry. That appeared to prove the gate was per-dispatch and conditional.

**Step 5 - the `TOOL_CALL_START` lever, and its failure.** W9 established that a gate-blocked call
returns before the start event, so `backend.log` should name exactly the ungated calls. It
returned nothing. Rather than treat the absence as evidence, the instrument was checked: a
directory listing plus a grep across all logs showed **`TOOL_CALL` appears in no log file at
all.** Lever dead, discarded - correctly, and cheaply.

**Step 6 - `dispatch.log`. THE TURN OF THE WINDOW.** The same directory listing surfaced
`dispatch.log`, 9,200 bytes, last written **08/23 20:45:05** - the exact second `eb9bdabb` ended.
A purpose-built dispatch instrument, live since 08/17, that no window had ever read. Its format:

```
ATTEMPT turn=<turn> tool=<name> args=<digest> thread=<thread>
OUTCOME turn=<turn> tool=<name> success=<bool> latency=<seconds> timed_out=<bool>
```

**Step 7 - the specimen, and the first retraction.** `eb9bdabb`'s three dispatches read:

```
20:40:59  ATTEMPT t1 tool=shell_exec  args={"command": "echo openjarvis_ws_probe"}   (no OUTCOME)
20:43:01  ATTEMPT t2 tool=shell_exec  args={"command": "echo openjarvis_ws_probe"}   (no OUTCOME)
20:45:05  ATTEMPT t3 tool=think       args={"thought": "...shell_exec is timing out..."}
20:45:05  OUTCOME t3 tool=think       success=True latency=0.001 timed_out=False
```

**The ungated third dispatch was a different tool.** `think`, not `shell_exec`. The step-4
"per-dispatch conditional gate" finding was an artifact of not knowing tool names. Retracted.

It also handed us a **gate oracle**: gated calls log ATTEMPT and never OUTCOME, because the gate
returns before the outcome write - the same structural reason they never reach the start event.
**ATTEMPT without OUTCOME = gated. ATTEMPT with OUTCOME = not gated.**

**Step 8 - the oracle applied to three runs.** `ad902101` (anomaly), `fb015fea` (known-gated
control), `65fd4b13` (the mailbox run):

```
ad902101-t1  shell_exec  {"command": "echo cycle-one"}   OUTCOME success=True latency=0.092  NOT GATED
ad902101-t1  shell_exec  {"command": "echo cycle-two"}   OUTCOME success=True latency=0.085  NOT GATED
fb015fea-t1  shell_exec  {"command": "hostname"}         no OUTCOME                          GATED
65fd4b13-t1  mailbox_list_accounts                       OUTCOME success=True latency=0.033  NOT GATED
65fd4b13-t2  mailbox_usage_report                        OUTCOME success=True latency=150.817 NOT GATED
65fd4b13-t3  mailbox_find_messages                       OUTCOME success=True latency=33.784  NOT GATED
65fd4b13-t4  mailbox_find_messages                       OUTCOME success=True latency=2.182   NOT GATED
```

**This is a genuine same-tool split.** `shell_exec` with an `echo` argument was gated on 08/23 and
ungated on 08/24 09:24, so it is not the arguments. The mailbox rows independently confirm W9's
section 5 finding (those tools are ungated) and independently confirm D-USAGE-1 and D-LAT-1 from
a second instrument.

**Step 9 - the spec. THE DUPLICATE-SPEC THEORY DIED HERE.** A tree-wide grep for `shell_exec`
returned exactly one `@ToolRegistry.register("shell_exec")` (`tools\shell_exec.py:27`) and exactly
one `ToolSpec(` for it (`:35`). Reading it: `spec` is a **`@property`**, rebuilt on every access,
and `requires_confirmation=True` at **line 71 is a hard literal** - no config lookup, no env var,
no mutable state. `ShellExecTool` declares True in every process, every time, forever.

**Consequence: the `ad902101` calls cannot have reached line 269 holding a `ShellExecTool`
object.** This is the hinge of the whole trace.

**Step 10 - the early-return audit. H4 DIED HERE.** Every early return in
`ToolExecutor.execute()` above the gate - lines 184 (unknown tool), 194 (bad JSON), 207 (boundary
guard), 230 (RBAC denial) - returns `success=False`. `ad902101` returned `success=True` with real
command output. **No successful bypass exists above the gate.** H4 dead.

**Step 11 - `ToolSpec` defaults.** Line 40: `requires_confirmation: bool = False`. **Fail-open
default.** Any `ToolSpec` constructed anywhere without explicitly setting it is ungated, silently.

**Step 12 - `ToolExecutor.__init__`. THE MECHANISM.** Line 165:

```python
self._tools: Dict[str, BaseTool] = {t.spec.name: t for t in tools}
```

A dict comprehension keyed on `spec.name`. **Last entry wins, silently - no collision check, no
warning, no exception.** And `execute()` at line 182 binds `tool = self._tools.get(tool_call.name)`
- **executor-local state, no registry lookup at dispatch time.** Line 269 then reads
`tool.spec.requires_confirmation` off whatever object won that dict.

Also at 158-159: `interactive: bool = False` and `confirm_callback: ... = None`, both defaults.

**Step 13 - construction sites.** Five in the tree:

```
system\builder.py:168               ToolExecutor(tool_list, bus) if tool_list else None
system\builder.py:193               ToolExecutor(tool_list, bus)      <- rebuilt AFTER skill_tools at 188
agents\_stubs.py:325                ToolExecutor(..., interactive=, confirm_callback=)
server\agent_manager_routes.py:1202 ToolExecutor(
mcp\server.py:58                    ToolExecutor(tools)
```

`agents\_stubs.py:320-332` sets `self._tools = tools or []` and passes `interactive` and
`confirm_callback` **straight through from the agent constructor's arguments**. So on the agent
path, both the tool membership AND whether the gate is armed are decided by whoever builds the
agent - **per run**.

**Step 14 - process boundaries. THE DECISIVE READ.** uvicorn lifecycle lines from `backend.log`:

```
2026-08-24 07:45:18  Shutting down
2026-08-24 07:47:46  Started server process [21036]
2026-08-24 08:15:07  Shutting down
2026-08-24 08:16:24  Started server process [21560]
                     (no shutdown logged - killed by the reboot)
2026-08-24 18:33:08  Started server process [14256]
```

**PID 21560 served every run from 08:16 until the reboot** - `ad902101` (09:24), `65fd4b13`
(10:36), `fb015fea` (11:17), `3747e140` (11:22), `fc948797` (11:25), `30e3c905` (12:44),
`f5c3b148` (12:50). One interpreter. One import of `shell_exec.py`. One `ToolRegistry`.

**Therefore any module-level, import-time, config-file or environment explanation is impossible.**
Within a single process the same tool name went ungated at 09:24 and blocked 120 s at 11:17. The
only per-run variable remaining is the executor built at `agents\_stubs.py:325`.

---

## 2. THE FINDING

**The gate is deterministic. The executor is not.**

`tools\_stubs.py:269` fires if and only if two conditions hold on the object that won the dict at
line 165: its spec says `requires_confirmation=True`, and the executor has `interactive=True` with
a non-None `confirm_callback`. Given those, it always fires. Given either missing, it never does.
There is no race, no intermittency, no conditional branch, and no flakiness anywhere in it.

What varies run to run is **which `ToolExecutor` was constructed, with which tool list and which
confirm arguments.** Three distinct outcomes have now been observed, and each implies a different
construction:

| Observed outcome | Implies |
|---|---|
| 120.00 s block, ATTEMPT with no OUTCOME | `requires_confirmation=True`, `interactive=True`, live callback |
| fast `success=False`, "no confirmation callback is available" | gate reached, `interactive=False` or callback None |
| fast `success=True` with real output (`ad902101`) | the `shell_exec` object in that executor's dict had a spec saying False |

The third is only reachable through line 165 - a second object claiming the name `shell_exec`,
carrying a `ToolSpec` that never set `requires_confirmation` and so inherited the False default at
line 40, landing later in the list and silently overwriting the real tool.

**Two plausible sources for such an object, both unread and both to be checked next window:**
`skills\tool_adapter.py:128` builds a `ToolSpec` dynamically from skill metadata, and
`skills\tool_translator.py:22` maps the name `"Bash"` to `"shell_exec"`. `system\builder.py:188`
fetches `skill_tools` and `:193` **rebuilds the executor with them** - exactly the shape required.

**NOT YET PROVEN.** The mechanism is proven to exist and to be sufficient. That a shadowing object
actually entered `ad902101`'s executor is inference, one step wide. It is settled by reading the
construction path or by instrumenting it (section 5, items 1 and 2).

---

## 3. RETRACTION - W9 SECTION 6 WAS WRONG, AND WRONG IN THE DANGEROUS DIRECTION

W9 wrote: *"A gate that fires on five runs and not on a sixth is not a gate."* That framed the
confirmation gate as unreliable. It is not unreliable; it is exactly correct on every run.

The true statement is worse: **the gate is correct, and we could not tell which executor served
any given run.** "Our safety control is flaky" is a bug to fix. "Our safety control is correct and
we cannot attribute a run to the construction that served it" is an observability failure that
makes every past gate observation unattributable. **The 6e UI would have been built against a
gate that is fine, to solve a problem that lives one layer up.**

Second retraction, same window: the step-4 reading of `eb9bdabb` as a per-dispatch conditional
gate. Refuted at step 7 by `dispatch.log` - the ungated dispatch was `think`.

**DIAGNOSIS QUALITY PATTERN, NINTH AND TENTH INSTANCES.** Both are the same shape as the seven
before: characterizing behaviour from the cheapest available surface while a purpose-built
instrument sat unread. `dispatch.log` was live since **08/17**, recorded every tool name and
latency this project has been guessing at for a week, and answered in one command.

**The countermeasure is no longer advisory.** W9 made it procedural for `agent.log`. Extend it:
**before characterizing any dispatch, read `dispatch.log` for that turn.** It names the tool,
which `agent.log` never has.

---

## 4. NEGATIVE RESULTS - WHAT THE 09:24 NO-BLOCK IS **NOT**, AND HOW EACH WAS ESTABLISHED

Per standing rule 17. Each of these is closed; do not re-open without new evidence.

1. **NOT a restart or time boundary (H1).** Gated runs exist on 08/23 and on both sides of 09:24
   on 08/24. Established by the 80-line `agent.log` dump. Reinforced at step 14: one process
   served all of them.
2. **NOT a duplicate/contradictory ToolSpec.** Tree-wide grep: one registration, one `ToolSpec`
   for `shell_exec`. **This is explicitly NOT the `imap_mail.py` trap shape from W9 section 5.**
3. **NOT config-, env- or file-driven.** `requires_confirmation=True` is a literal at
   `shell_exec.py:71`, and `spec` is a `@property` rebuilt on every access - no cached value can
   drift.
4. **NOT a different `ToolExecutor` instance within a run.** All three `execute()` call sites in
   `native_openhands.py` (448, 476, 495) use the same `self._executor`.
5. **NOT the multi-call / `ntc=2` loop branch (H2).** The native branch at 427-429 loops over all
   tool calls and every iteration dispatches through the same line 448. `fb015fea` (`ntc=1`) and
   `ad902101` (`ntc=2`) used the identical call site.
6. **NOT an early-return bypass (H4).** All four early returns above the gate are `success=False`;
   `ad902101` was `success=True`.
7. **NOT a missing confirm callback.** That path returns `success=False` at line 270 with a
   specific message. Not what was observed.
8. **NOT the arguments.** `echo` was gated on 08/23 and ungated on 08/24.
9. **NOT Defect 1 and NOT a model refusal.** The model's report matched the real tool outcomes;
   `dispatch.log` shows the calls genuinely ran. Consistent with W9.
10. **NOT the two-interpreter oddity.** Both current PIDs started at boot, after every run in
    question; PID 21560 alone served them.

---

## 5. NEW DEFECTS AND HAZARDS FOUND THIS WINDOW - NONE CHASED, ALL REGISTERED

**D-EXEC-1 - SILENT TOOL SHADOWING AT `_stubs.py:165`. HIGHEST-SEVERITY FINDING OF THIS WINDOW.**
`{t.spec.name: t for t in tools}` lets any later tool claiming an existing name silently replace
it. No collision detection, no log, no error. **A shadowing tool inherits nothing from the tool it
replaces - including its confirmation requirement.** This is a general gate-bypass vector, not
specific to `shell_exec`. It applies equally to the destructive mailbox tools.

**D-SPEC-1 - `ToolSpec.requires_confirmation` DEFAULTS FALSE (`_stubs.py:40`).** Fail-open. Every
`ToolSpec` built without the explicit flag is ungated. Combined with D-EXEC-1, a spec authored
anywhere in the tree - including one generated from skill metadata at `tool_adapter.py:128` - is
ungated by default and can take over a gated tool's name. **Same family as D-CONFIRM-2: defaults
that fail open.**

**D-PROV-1 - NO CONSTRUCTION PROVENANCE IN THE RUN RECORD.** RUNSTART logs `agent=`, `model=`,
`conv=-`, `tools=12`, `maxturns=15`. It does not log which tool objects, whether `interactive` was
True, or whether a `confirm_callback` was present. **`tools=12` is a count, and a shadowed tool
keeps the count at 12.** Every gate observation in this project to date is therefore
unattributable to a construction. **This is what actually blocks the 6e UI.**

**D-DISPATCH-1 (observation, not a defect) - `dispatch.log` IS THE PROJECT'S BEST TOOL
INSTRUMENT AND WENT UNREAD FOR SEVEN DAYS.** It carries tool name, argument digest, thread name,
success, latency in SECONDS, and `timed_out`. It is also a clean gate oracle by the
ATTEMPT-without-OUTCOME property. Add it to the standing instrument list beside `agent.log`,
`engine.log` and the bus frames.

**D-LAT-1 CORROBORATED FROM A SECOND SOURCE.** `dispatch.log` records
`mailbox_usage_report ... latency=150.817` where the UI rendered "151ms". Two independent
instruments now confirm the unit bug. **`dispatch.log` latency is seconds. Treat every latency
figure in this project as seconds until proven otherwise.**

**TWO INTERPRETERS SERVING 8010 - REGISTERED, NOT CHASED.**
`.venv\Scripts\python.exe` (PID 10776) and `Python312\python.exe` (PID 14256), both
`-m openjarvis.cli serve --port 8010`, identical start time 18:31:44. Only 14256 logged the
uvicorn startup line at 18:33:08, which is consistent with a benign parent/child or launcher
relationship - **unconfirmed.** Not a stale listener from a prior session. Promoted from
housekeeping to a register row because a second interpreter is another way to get two
constructions. **Do not touch it until D-PROV-1 is instrumented.**

---

## 6. STATE AT WINDOW CLOSE

- OpenJarvis backend up on 8010, `/health` ok, post-reboot. PID 14256 (plus 10776, see above).
- No source file modified. No host modified. No probe written. No process left running.
- **No new rollback points** - nothing to roll back. The rollback register is unchanged.
- `dispatch.log` last write 08/23 20:45:05; nothing has dispatched since (no chat runs this
  window). `agent.log` last write 08/24 12:52:10.
- Log inventory: `agent.log` 56,098 B; `backend.log` 245,441 B plus `.1`-`.5` rotations;
  `dispatch.log` 9,200 B; `engine.log` 179 B (unchanged since 08/18 - Patch 5 still a passive
  armed trap with zero false positives); `memdb_audit.log` 2,276 B.
- W9 items 1-3 remain closed. **W9 next-action item 1 (the 09:24 anomaly) is CLOSED TO THE
  CONSTRUCTION BOUNDARY** - mechanism identified, attribution outstanding.
- 6c SATISFIED. 6d LIVE-PROVEN CLOSED. 6e transport CLOSED. **6e browser UI half OPEN and now
  blocked on D-PROV-1 rather than on the anomaly.**
- W1 CLOSED. W2 CLOSED AND VERIFIED. W3 WITHDRAWN. W4 OPEN.

---

## 7. NEXT ACTION - IN ORDER, START HERE

1. **FIND THE CALLER THAT CONSTRUCTS THE AGENT FOR A BROWSER CHAT RUN.** This is the closer.
   Read the chat dispatch in `routes.py` (paths 1a/1b/1c/1d are already in the register) down to
   the `NativeOpenHandsAgent` construction, and record: which tool list it passes, and what it
   passes for `interactive` and `confirm_callback`. Then read `system\builder.py:160-200` for the
   `skill_tools` rebuild at 188-193. **Read-only. No patch.**
2. **INSTRUMENT D-PROV-1.** Extend the RUNSTART line to log, per run: `interactive`,
   `confirm_callback is not None`, and the tool names with their `requires_confirmation` values
   (or a stable hash of that set). Small, passive, no behaviour change - same shape as Patch 4 and
   Patch 5, both of which paid for themselves. **This makes every future gate observation
   attributable and turns the execution-path register into something the system maintains itself.**
   Verify in isolation before anything else lands on top of it.
3. **DUMP THE LIVE TOOL SET.** For one real chat run, list the 12 tools actually in
   `self._tools` with their spec `requires_confirmation` and their class/module. If `shell_exec`
   resolves to anything other than `tools.shell_exec.ShellExecTool`, D-EXEC-1 goes from proven
   mechanism to proven cause.
4. **FIX D-LAT-1 BEFORE THE 6e UI SHIPS.** Carried from W9, unchanged. The 6e panel would render
   a 120 s gate as "120ms".
5. **ONE READ OF `ws_bridge.py:40-80`** to settle D-WS-1. Carried from W9, trivial.
6. **THE 6e UI WORK.** Unblocked once items 1-3 land. Mount site `ChatArea.tsx`, design option
   (b), new hook, `AgentsPage` untouched. Subscribe to `tool_confirm_request` AND
   `tool_confirm_resolved`; field sets in W9 section 3.
7. **DECIDE THE DESTRUCTIVE MAILBOX TOOL POSTURE.** Carried from W9 section 5. **Now informed by
   D-EXEC-1: even if the flag is flipped, a shadowing tool would silently defeat it.** The
   posture decision and the D-EXEC-1 fix are the same decision.
8. **DISABLE THE STALE `kokoro-tts` UNIT ON .200.** Carried. `sudo systemctl disable --now
   kokoro-tts` on **.200 ONLY**. **Verify the hostname in the same command** - the unit exists on
   both boxes and running it against .201 takes speech down.
9. **DECIDE THE `unattended-upgrades` POLICY ON THE MODEL HOSTS.** Carried, unchanged.
10. **Re-run W7 step 3** - bogus agent id, gate-provoking prompt. Still UNKNOWN.
11. **System32 housekeeping** - two stale `start-openjarvis.ps1` copies on PATH. Unchanged.

**BEFORE STARTING ITEM 1, READ SECTION 0.5 AND MAKE ONE EXPLICIT CALL:** does this window advance
a defect, or does it resume Workstream V (voice, parked 15 days) or Workstream A (agents, parked
12 days)? Any of the three is a legitimate answer. **Defaulting into defect work without deciding
is what produced the 15 days.** If a workstream is not next, record why in this handoff's
successor - one line is enough.

**AGE THE CARRIED ITEMS.** Items 8-11 above carry from prior windows with no first-seen number.
Next window, tag each with the window it first appeared in, then either close it or delete it
deliberately. A number that keeps climbing is the point.

**Open design question, carried and still unsettled:** if the browser only reaches a tool-capable
path when an agent is selected, then either the gate is irrelevant to default chat, or default
chat should be tool-capable and currently is not. **Product decision. Do not let it be settled
implicitly.**

---

## 8. EXECUTION PATHS REGISTER

Paths 1a, 1b, 1d and 2-5 carry forward. Host and driver columns carry forward. Deltas:

- **A NEW MANDATORY COLUMN: EXECUTOR CONSTRUCTION SITE.** Per the finding in section 2, a path is
  not characterized by its route and call chain alone. Each row must record the `ToolExecutor`
  construction site by `file:line`, the tool list source, and the `interactive` /
  `confirm_callback` arguments at that site. **Five known construction sites:**
  `system\builder.py:168`, `system\builder.py:193`, `agents\_stubs.py:325`,
  `server\agent_manager_routes.py:1202`, `mcp\server.py:58`.
- **THE POSITIONAL SITES FAIL CLOSED, NOT OPEN.** `builder.py:168`, `builder.py:193` and
  `mcp\server.py:58` construct positionally, so `interactive=False` and `confirm_callback=None`.
  On those executors a `requires_confirmation=True` tool returns `success=False` with "no
  confirmation callback is available" - **fast failure, not a bypass, and never a 120 s block.**
  Record this per row; it is a third distinguishable outcome and it has a distinct signature.
- **THE BROWSER AGENT PATH** remains gate-live-confirmed (W9). Entry: desktop app chat. Agent
  `NativeOpenHandsAgent`, `tools=12`, `maxturns=15`, `conv=-`. Executor built at
  `agents\_stubs.py:325`, arguments passed through from the agent constructor - **caller UNREAD,
  next-action item 1.** Human present but cannot currently respond (no 6e UI).
- **THE GATE-FIRES COLUMN IS RESOLVED IN PRINCIPLE.** W9 required "fires, condition unknown." The
  condition is now known and deterministic: `spec.requires_confirmation` on the object that won
  the executor dict, AND `interactive` True, AND a non-None callback. **The correct value per row
  is now the three-way construction record, not a boolean.**
- **GATE TTL IS A PATH PROPERTY: 120.000 s exactly**, five measurements within 6 ms (W9).
- **THE TOOL TIMEOUT AND THE GATE TTL ARE DIFFERENT NUMBERS.** Executor `default_timeout` 30.0 s;
  `ShellExecTool.spec.timeout_seconds` 60.0 s; gate blocks 120 s. **Three different numbers - a
  120 s block is the gate, never a timeout.** Record all three per row.
- **`shell_exec` REQUIRES THE `code:execute` CAPABILITY** (`shell_exec.py:73`). The RBAC check at
  `_stubs.py:214-230` is a separate control from the gate and returns `success=False` on denial.
  Record capability requirements per path.

---

## 9. SDP FEED

Prior windows' SDP feed carries forward IN FULL. Additions:

- **NAME BINDING IS A SECURITY BOUNDARY AND THE SDP DID NOT MODEL IT.** D-EXEC-1. Tools are bound
  by string name into a plain dict with last-write-wins semantics. **Any component that can
  contribute a tool object can silently replace any other tool, inheriting none of its controls.**
  The SDP needs a tool-identity section: what may register a name, what resolves it at dispatch,
  and what detects a collision (currently: nothing).
- **A CONTROL'S CORRECTNESS AND A CONTROL'S ATTRIBUTABILITY ARE DIFFERENT PROPERTIES.** The gate
  is correct and was never in doubt once measured. What failed is our ability to say which
  construction served a run. **Every safety control in the SDD needs an attribution story
  alongside its correctness argument** - otherwise a correct control produces unexplainable
  observations and the next window concludes the control is broken.
- **DEFAULTS THAT FAIL OPEN, THIRD INSTANCE.** D-SPEC-1 joins D-CONFIRM-2 and the
  `params.get(x, True)` family. **This is now a pattern, not a set of bugs.** The SDP should state
  a project-wide rule: security-relevant fields have no default, or default to the safe value, and
  a sweep should confirm it.
- **A COUNT IS NOT AN INVENTORY.** `tools=12` looked like verification for weeks and cannot
  distinguish a shadowed tool set from a clean one. **Wherever the SDD cites a count as evidence,
  it needs the membership instead.**
- **THE OPERATOR SURFACE IS A DEFECT SURFACE** (carried, W9) - now with a fourth instance:
  `dispatch.log` latency confirms the UI unit bug from an independent source.
- Carried unchanged and still live: a second declaration of a tool spec is a trap not a duplicate;
  a safety decision carries its premise and premises expire; an interlock that publishes its own
  bypass is an accident guard; bus frames carry full tool arguments to every subscriber and the
  event bus is an unmodelled data-egress surface; a `.bak` chain's timestamps lie but its names do
  not; the purpose-built instrument goes unread while the cheap surface gets believed; routing
  inputs unvalidated; component-level guarantees do not survive composition; a unit reporting
  `running` may be crash-looping; automated updates are an unmanaged change source.

---

## 10. SDD SECTION

Gray is building a detailed System Design Document covering all OpenJarvis work to date. This
window feeds it:

- **CONFIRMATION GATE CHAPTER - THE MECHANISM SECTION, GREAT DETAIL per the standing instruction.**
  The gate's firing condition is now fully specified with file:line evidence:
  `tools\_stubs.py:269` reads `tool.spec.requires_confirmation` where `tool` comes from
  `self._tools.get(name)` at `:182`, populated by the dict comprehension at `:165`
  (`{t.spec.name: t for t in tools}`, last-wins), with `interactive` and `confirm_callback` from
  `__init__` at `:158-159`. Gate reached and armed leads to a 120.000 s TTL block; gate reached
  and unarmed leads to a fast `success=False`; gate not reached leads to normal execution.
  **Include the three-outcome table from section 2 verbatim.**
- **TOOL IDENTITY AND BINDING - NEW CHAPTER.** `ToolRegistry.register` is authoritative for
  discovery (W9), but **`ToolExecutor._tools` is authoritative for dispatch**, and the two can
  disagree. Document the binding chain, the last-wins semantics, the absence of collision
  detection, and the two candidate shadowing sources (`skills\tool_adapter.py:128`,
  `skills\tool_translator.py:22` mapping `"Bash"` to `"shell_exec"`).
- **OBSERVABILITY CHAPTER - `dispatch.log` DOCUMENTED IN FULL.** Path
  `%LOCALAPPDATA%\OpenJarvis\logs\dispatch.log`. Format: `ATTEMPT turn tool args thread` and
  `OUTCOME turn tool success latency timed_out`. **Latency is in SECONDS.** Live since 08/17.
  **Its ATTEMPT-without-OUTCOME property is a gate oracle** and should be stated as such, because
  it is the only instrument in the project that names the tool per dispatch. `agent.log` never
  records a tool name; `backend.log` contains no `TOOL_CALL` lines at all.
- **INSTRUMENT INVENTORY, NEW SUBSECTION.** `agent.log` (RUNSTART/TURN/RAWGEN/RUNEND, run-level),
  `dispatch.log` (per-dispatch, tool names), `engine.log` (RETRACTION400 trap, 179 B, never
  fired), `backend.log` (uvicorn only - **contains no tool events; do not reason from its
  absences**), the agent-events WebSocket frames, and `memdb_audit.log`. **State what each can and
  cannot answer.**
- **PROCESS LIFECYCLE AS EVIDENCE.** uvicorn `Started server process [PID]` / `Shutting down`
  lines in `backend.log` bound which runs shared an interpreter. **This is how the import-time
  explanation was eliminated** and it belongs in the SDD's method chapter as a standard technique.
  Record the 08/24 boundaries: 07:47:46 PID 21036, 08:16:24 PID 21560 (served everything through
  the reboot), 18:33:08 PID 14256.
- **DEPLOYMENT - TWO INTERPRETERS SERVING 8010.** `.venv` and system `Python312`, both running
  `-m openjarvis.cli serve --port 8010`. Document the intended startup topology so the SDD says
  whether this is by design.
- **PERFORMANCE CHAPTER** - D-LAT-1 corroborated; `mailbox_usage_report` at 150.817 s confirmed
  from a second instrument. Carried: re-source every UI-derived latency figure.
- **DIAGNOSIS QUALITY subsection gains TWO entries, both mine** (section 3). Nine and ten. Same
  shape every time. **The generalized countermeasure now names three instruments:
  read `agent.log` for the run, `dispatch.log` for the dispatch, and the bus frames for the gate -
  before characterizing anything.**
- **Evidence provenance for this window:** `agent.log` and `dispatch.log` reads, `backend.log`
  uvicorn lifecycle lines, direct numbered source reads of `tools\_stubs.py`,
  `tools\shell_exec.py` and `agents\_stubs.py`, tree-wide greps, one process-table read, one
  `/health` check. **No OpenJarvis source was modified and no host was changed**, so nothing here
  is contingent on a patch landing. **Firmest tier.**

**Standing instruction:** every handoff from here carries an SDD section, an SDP feed, an
execution paths section, and - per rule 17 - a detailed narrative of the window including its
negative results. Every window feeds all four.

---

## 11. METHOD LESSONS

1. **THE INSTRUMENT THAT NAMES THE THING BEATS THE INSTRUMENT THAT TIMES THE THING.** Four windows
   inferred gate behaviour from RAWGEN-to-TURN gaps. One read of `dispatch.log` gave tool names
   and settled in minutes what timing analysis had made steadily more confident and partly wrong.
   **When reasoning from a proxy, ask what would name the thing directly.**
2. **A DIRECTORY LISTING IS A CHEAP, HIGH-YIELD MOVE.** `dispatch.log` was found while checking
   whether a *different* instrument existed. The failed lever was worth more than the lever would
   have been.
3. **AN ABSENCE WAS CHECKED BEFORE IT WAS BELIEVED.** The empty `TOOL_CALL` grep could have become
   a finding. Proving the instrument could say yes cost one command and prevented a false
   conclusion. **This is the standing rule working as intended.**
4. **ELIMINATION BEAT SEARCH.** H1, H2, H4, the duplicate-spec theory and the config-drift theory
   all died on reads that took one command each. The survivor was then the answer. **Cheap
   falsification first; the expensive read last.**
5. **ONE PROCESS BOUNDARY COLLAPSED AN ENTIRE HYPOTHESIS CLASS.** Establishing that all runs shared
   PID 21560 killed every import-time, config, and environment explanation at once.
6. **A WINDOW THAT CHANGED NOTHING PRODUCED THE MOST IMPORTANT RESULT SO FAR.** Zero patches, zero
   host changes, five theories killed, one gate-bypass mechanism found, three new defects
   registered, and a retraction that changed what "blocked" means for the 6e UI. **This is the
   case for rule 17.**
