# HANDOFF - 2026-08-24 SEVENTH WINDOW
# COLD START CONFIRMED AND CLOSED. PROBE v3 CLEARED. THE SECOND CONFIRM CYCLE IS PROVEN.
# TOOL_CONFIRM_RESOLVED IS LIVE AND NO HANDOFF EVER RECORDED IT.

Supersedes `HANDOFF-2026-08-24-A-W2-CLOSED-VERIFIED-SENDER-STALL-RELOCATED-TO-SERVER.md`
for state. Everything in that file stands EXCEPT the sender-stall magnitude question and the
`TOOL_CONFIRM_RESOLVED` entry, both corrected below. Its sections 5, 7, 8, 9, 10, 11 are
CARRIED FORWARD; only deltas are restated here.

**Actions this window: ZERO source patches. Five measurements, two read-only file reads, one
live two-cycle confirm test through the real chat UI. No backend restart. Nothing left running.**

This was a measurement window, not a patch window. There is no new rollback point because
nothing was changed.

---

## 0. STANDING RULES FOR THE NEXT WINDOW

Rules 1-11 from the prior handoffs carry forward UNCHANGED. One addition, earned this window:

12. **AN UNRECORDED PATCH IS AS DANGEROUS AS AN UNAPPLIED ONE.** Rule 11 covers "the handoff
    says applied, the disk disagrees." This window found the inverse: **the disk had a patch the
    record denied.** `patch_confirm_resolved.py` was applied on 08/22 and no handoff mentions it,
    so three windows of planning treated a solved problem as an open blocker. **Every patch script
    in the repo root is a claim about the disk that must be either confirmed or explicitly marked
    unknown.** See section 3.

---

## 1. COLD START - CONFIRMED, CLOSED

The `send -> first byte` gap on PATH 1a is **model load into VRAM on the ollama host**. Not server
code, not the client, not the probe.

Method - the unload was forced, so this is a controlled experiment and not an observation:

```
POST /api/generate {"model":"qwen3-coder:30b","keep_alive":0}   then verify /api/ps == []
```

Results, raw-socket instrument, PATH 1a, trivial prompt:

```
RUN 1 (forced cold)   send -> first byte   16.692 s
RUN 2 (warm)          send -> first byte    0.380 s      44x
```

`/api/ps` before the unload showed `qwen3-coder:30b` resident, `size_vram` 19,488,159,872 equal to
`size` - fully in VRAM, not partially offloaded. TTL field is `expires_at`.

**THE FIX IS A KEEP-ALIVE SETTING, NOT A CODE CHANGE. IT WAS DELIBERATELY NOT APPLIED.** Changing
the host TTL mid-investigation would have altered the machine under test before item 2 could use a
controlled cold/warm condition. **It is now a config decision, unblocked, and it is the cheapest
open win in the project.** Options: `OLLAMA_KEEP_ALIVE` on the host service, or a `keep_alive`
field on the request from OpenJarvis. Decide which layer owns it - that is an architecture call,
not a tuning call, and it belongs in the SDD.

---

## 2. PROBE v3 IS CLEARED - THE SENDER-STALL ATTRIBUTION IS DEAD

The prior handoff relocated the stall from v3 to the server but explicitly refused to merge the
magnitudes. **They are now measured and they are the same mechanism.**

```
raw socket, forced cold, PATH 1a        16.692 s
ws_probe.py v3, forced cold, PATH 1a    16.778 s     delta 86 ms
ws_probe.py v3, warm, PATH 1a            0.642 s     max frame lag 0.002 s, NO STALL
```

**An 86 ms spread between two instruments that share no code.** v3 adds nothing measurable.

**FURTHER LOCALIZATION, from the v3 cold run:** the wait sits BETWEEN `inference_start` (t+3.117)
and `inference_end` (t+19.881). The server entered inference immediately. **This rules out
dispatch-side, routing-side and queueing delay** and puts the whole gap inside the model call.

**CONSEQUENCE FOR THE RECORD:** "v3's sender thread can stall hundreds of seconds" was carried
across two handoffs and **no instrument ever supported it.** The queued patch to v3 would have
changed nothing. That is the SECOND time a patch was queued against the wrong artifact - see
section 9.

**RE-DATE, DO NOT DELETE:** any latency figure recorded in this project without stating model
residency is uninterpretable. It is not wrong, it is unlabeled, and it cannot be compared to
anything until the cold/warm axis is known.

---

## 3. `TOOL_CONFIRM_RESOLVED` IS LIVE - THE RECORD WAS WRONG

**The carried record states: `TOOL_CONFIRM_RESOLVED` (`core\events.py:82`) exists but NOTHING
publishes it, so a mounted UI cannot dismiss a stale prompt, and emit-vs-poll must be decided
BEFORE the 6e UI patch.**

**That is false as of this window.** Two `tool_confirm_resolved` frames arrived on the live test,
each ~170 ms after its approve, carrying `confirm_id`, `agent_id`, `turn_id`, `tool`, `decision`,
`state`, `created_at`, `expires_at`, and a `reape...`-prefixed field (truncated in capture - read
the full frame next window).

`patch_confirm_resolved.py` sits in the repo root, 4,348 bytes, mtime 08/22 12:43:26. **No handoff
records it as applied.** It was applied.

**IMPACT: a stated pre-6e blocker was already closed and three windows of planning did not know.**
The 6e UI can subscribe to the resolved frame; it does not need a poll loop and does not need a
design decision first.

**NOT YET DONE, and it is small:** read `patch_confirm_resolved.py` and hash its target to
establish exactly what shipped, and capture one full untruncated resolved frame. Do that before
the 6e UI patch depends on the field set.

---

## 4. THE SECOND CONFIRM CYCLE IS PROVEN - HIGHEST-VALUE OPEN QUESTION, CLOSED

Deferred three windows, blocked on instrument trust. Section 2 unblocked it.

Test: fresh chat thread, PATH 1b, `watch_confirm_auto.ps1` auto-approving, prompt requesting two
sequential `shell_exec` calls with distinct stdout markers.

```
09:24:24.042  tool_confirm_request   7f8e99f8...  shell_exec  echo cycle-one
              APPROVE -> HTTP 200 in  49 ms   decision approved
09:24:24.209  tool_confirm_resolved  7f8e99f8...
09:24:24.226  tool_call_start        echo cycle-one
09:24:24.240  tool_call_end          success=true  latency 0.0917 s  stdout cycle-one
09:24:24.251  tool_confirm_request   a4552642...  shell_exec  echo cycle-two
              APPROVE -> HTTP 200 in 121 ms   decision approved
09:24:24.433  tool_confirm_resolved  a4552642...
09:24:24.439  tool_call_start        echo cycle-two
09:24:24.452  tool_call_end          success=true  latency 0.0850 s  stdout cycle-two
```

**WHAT IS PROVEN:**

1. **A second confirm cycle emits, delivers, resolves and executes.** Delivery does not die after
   the first resolve.
2. **BOTH CYCLES SHARE ONE TURN - `ad902101-t1`.** This is STRONGER than the question asked. The
   prior record only knew that a TIMEOUT causes a re-request on the NEXT turn with an incremented
   suffix. **Two gates inside a single turn is a different case and it works.**
3. **Distinct confirm_ids**, `7f8e99f8...` and `a4552642...`. The registry issues per-gate, not
   per-turn.
4. **Whole two-cycle sequence: ~410 ms**, against a 120 s TTL. That margin is the discriminator -
   it rules out "it timed out and happened to look right."
5. **Real execution both times**, `cycle-one` and `cycle-two` in stdout, exit 0. Defect 1 did NOT
   occur.
6. **Approve round trips 49 ms and 121 ms** - both well under 08/22's 186 ms baseline.

**6e's TRANSPORT HALF IS NOW CLOSED FOR MULTI-CYCLE, not just first-cycle.** The browser half
remains the only open piece, and it is no longer blocked on the resolved-frame design question.

---

## 5. THE 0 ms UI LATENCY DISPLAY IS AN ARTIFACT

The chat UI rendered `0ms` on both `shell_exec` calls. The bus says 0.0917 s and 0.0850 s.

**Cosmetic, logged, NOT chased (rule 6).** Recorded because it is actively misleading during
confirm-gate work - a `0ms` reading looks exactly like a bypassed gate, which is precisely the
wrong impression for a tool that is supposed to block. **Fix it before the 6e UI ships**, or the
first person to see a gated call will think the gate failed.

---

## 6. TOOLING NOTE - EXECUTION POLICY

`.\watch_confirm_auto.ps1` fails with `UnauthorizedAccess` / not digitally signed. Correct
invocation, process-scoped, leaves `Get-ExecutionPolicy` unchanged on the box:

```
powershell.exe -ExecutionPolicy Bypass -File .\watch_confirm_auto.ps1 -MaxSeconds 600
```

**Applies to every `.ps1` instrument in the repo root**, not just this one. It worked on 08/22
because that window was launched differently; the policy is per-process and was never carried in a
handoff. It is now.

`watch_confirm_auto.ps1` READ IN FULL this window and is correct for multi-cycle work unmodified:
it loops on `-MaxSeconds` rather than exiting after one approval, and **dedupes on `confirm_id`**,
so a second cycle's new id is approved rather than skipped. Had it deduped on tool name, cycle two
would have been silently skipped and the result would have read as a delivery failure.

---

## 7. WHAT CHANGED IN THE SYSTEM

**NOTHING. No source file was modified this window. No patch was applied. No restart.**

- `qwen3-coder:30b` was force-unloaded from VRAM twice and reloaded by test traffic. Host state
  only, no config written. **The host TTL is unchanged and the model is warm as of window close
  unless its TTL has since lapsed.**
- No new files. No new rollback points.
- All prior rollback points remain active and untouched, including
  `app.py.bak-20260824-081250` from the W2 work.

---

## 8. STATE AT WINDOW CLOSE

- Backend UP on port 8010, W2 guard live, gate live, WS verified Open.
- **No probe running. No listener alive. Nothing left to come back to.** The auto-approver ran its
  600 s budget to completion and exited on its own.
- 6c SATISFIED. 6d LIVE-PROVEN, CLOSED. **6e transport CLOSED on 1a and 1d, and now CLOSED on 1b
  for MULTI-CYCLE, not just the first cycle.** 6e backend emit APPLIED and verified.
  **`TOOL_CONFIRM_RESOLVED` LIVE.** 6e browser half OPEN, blocked only by the 1d default-path
  question.
- W1 CLOSED. W2 CLOSED AND VERIFIED. W3 WITHDRAWN. W4 OPEN.
- **Cold start CLOSED. Probe v3 CLEARED. Second confirm cycle CLOSED.**
- Repo root cleanup list carries forward unchanged - no additions this window.

---

## 9. NEXT ACTION - IN ORDER, START HERE

1. **APPLY THE KEEP-ALIVE SETTING.** Section 1. Cheapest open win, fully diagnosed, zero code.
   Decide the owning layer first - host service env var vs a `keep_alive` field on OpenJarvis's
   request - because that is an architecture call the SDD has to record either way.
2. **READ `patch_confirm_resolved.py` AND HASH ITS TARGET.** Section 3. Establish what actually
   shipped on 08/22, and capture one full untruncated `tool_confirm_resolved` frame so the 6e UI
   can be written against a known field set. Small, and it unblocks item 3 properly.
3. **THE 6e UI WORK IS NOW UNBLOCKED AND IS THE HEAD OF THE QUEUE.** Mount site `ChatArea.tsx`,
   design call option (b), new hook, `AgentsPage` untouched. Subscribe to `tool_confirm_request`
   AND `tool_confirm_resolved` - the resolved frame exists, so stale-prompt dismissal is an event,
   not a poll.
4. **Fix the 0 ms latency display** before the UI ships. Section 5.
5. **Re-run step 3** - bogus agent id, gate-provoking prompt. Whether a ToolExecutor is
   constructed at all on the unresolvable-id sub-case is still UNKNOWN. Unchanged, still open.
6. **Decide the System32 housekeeping.** Two stale `start-openjarvis.ps1` copies on PATH. The stub
   option is still the strongest. Unchanged.
7. **Optional, low:** the clean W1 proof - remove websockets, `.\start-openjarvis.ps1`, re-test.

**Open design question, carried forward unchanged and still unsettled:** if the browser only
reaches a tool-capable path when an agent is selected, then either the gate is irrelevant to
default chat, or default chat should be tool-capable and currently is not. **Product decision, not
a bug fix. Do not let it be settled implicitly.**

**ALSO STILL OPEN, carried and not chased:** `mailbox_move_to_trash` and `mailbox_empty_folder`
carry NO `requires_confirmation` at the spec level. **The destructive mailbox tools remain ungated
and no amount of confirm-gate wiring reaches them.** This is the oldest live safety item in the
project and it has now survived several windows as a carried note. It deserves a decision.

---

## 10. EXECUTION PATHS REGISTER

Paths 1a, 1b, 1d and 2-5 carry forward UNCHANGED. Three deltas:

- **PATH 1a COLD/WARM ROW IS NOW SETTLED.** Cold 16.692 s (raw socket) / 16.778 s (v3), warm
  0.380 s / 0.642 s. **Cause established: VRAM model load, located between `inference_start` and
  `inference_end`.** The prior row said "cause not yet established" - replace it, keep the date.
- **PATH 1b GAINS A MULTI-CYCLE ROW.** Two confirmation gates within a single turn (`ad902101-t1`)
  both emit, deliver, resolve and execute; distinct confirm_ids; full sequence ~410 ms. **The
  register should carry "gates per turn" as a property of every tool-capable path**, because the
  single-gate case and the multi-gate case are different behaviors and only one of them was ever
  measured before today.
- **THE COLD/WARM AXIS IS NOW MANDATORY ON EVERY PATH ROW.** Carried forward from the prior
  handoff and reinforced: a single latency number for a path is meaningless without stating which
  it is.

---

## 11. SDP FEED

Prior windows' SDP feed carries forward IN FULL. Additions:

- **THE UNRECORDED PATCH IS A NEW OPERATOR-SURFACE DEFECT AND IT IS THE INVERSE OF THE 08/24
  SILENT NO-OP.** One is disk-without-record, the other record-without-disk. **Together they
  establish that the handoff chain and the filesystem are two independent stores that drift in
  both directions.** The SDP should state the consequence plainly: the record is a claim about the
  system, not the system.
- **EVIDENCE QUALITY, EXTENDED:** the prior rule was "a tool's self-report of success is not
  evidence of effect." Add the converse - **the absence of a record is not evidence of absence.**
  Three windows planned around a blocker that was already fixed.
- **INSTRUMENT INDEPENDENCE, THIRD DEMONSTRATED INSTANCE.** The .NET WS client cleared the WS
  transport; the raw-socket sender cleared the client; **this window the raw-socket sender and v3
  agreed to within 86 ms on a forced-cold measurement, which is what CLEARED v3 itself.** Two
  instruments sharing nothing and agreeing is a stronger result than either alone.
- **CONTROLLED CONDITIONS BEAT OBSERVED ONES.** The cold-start hypothesis had been observable for
  two windows and unprovable, because run 1 was never observed cold. **Forcing the unload turned an
  observation into an experiment and closed it in one command.** State this as method.
- **THE GATE NOW WRITES TO THE BUS ON BOTH EDGES** - request and resolved. The carried entry "the
  gate still writes nothing to the log" stands for the LOG, but the bus-side audit trail is now
  complete enough that after-the-fact reconstruction is possible from a bus subscriber. **Rewrite
  the entry to separate the two surfaces; they no longer have the same answer.**
- **ROUTING INPUTS ARE UNVALIDATED.** Carried unchanged, still half-resolved.
- **A `0ms` LATENCY DISPLAY ON A GATED TOOL IS AN OPERATOR-SURFACE HAZARD, not a cosmetic bug.**
  It renders a blocking confirmation as if it never blocked. File it under the same heading as the
  auto-approve stubs: **the UI tells the operator the gate did not happen.**

---

## 12. SDD SECTION

Gray is building a detailed System Design Document covering all OpenJarvis work to date. This
window feeds it:

- **PERFORMANCE CHAPTER - THE COLD/WARM AXIS IS NOW QUANTIFIED, NOT JUST FLAGGED.** 1a cold
  16.7 s, warm 0.4-0.6 s, 44x, cause located inside the model call. 1d streams 2-8 ms to first
  chunk. 1b gated 0.017 s, short runs 0.006-0.008 s. **Every prior latency figure in the project
  was recorded without stating model residency and is not comparable until relabeled.** The
  chapter needs a residency column, not a footnote.
- **DEPLOYMENT AND RUNTIME ENVIRONMENT - THE MODEL HOST IS A DOCUMENTED DEPENDENCY WITH ITS OWN
  LIFECYCLE.** `qwen3-coder:30b`, 19.5 GB fully resident in VRAM, TTL-evicted, reloaded on demand
  at ~17 s cost. **The SDD must treat the ollama host's residency state as part of the runtime
  environment**, alongside the existing finding that the listener on 8010 is a system-Python child
  of the venv parent. Both are environment facts invisible from the source tree.
- **KEEP-ALIVE OWNERSHIP IS AN ARCHITECTURE DECISION.** Host service config vs per-request field
  is a boundary question - it decides whether OpenJarvis declares its latency requirements or
  inherits them. Record the decision and the reasoning, not just the setting.
- **CONFIRMATION GATE CHAPTER - GREAT DETAIL, per the standing instruction.** The gate is now
  characterized end to end on PATH 1b including the multi-cycle case: registry issues per-gate
  ids; both edges publish to the bus (`tool_confirm_request`, `tool_confirm_resolved`); the route
  accepts approve/approved/deny/denied and normalizes; write-once is honored with 409 carrying the
  recorded decision; TTL 120 s; approve round trip 49-186 ms observed across three runs;
  gate-to-execution 184-287 ms. **Two gates in one turn is proven and belongs in the chapter as a
  named case.**
- **PORTS, PROTOCOLS, ENCODING AT EACH GATE, with the PRECONDITION field.** Add the ollama host
  row: 172.16.33.200:11434, HTTP, JSON; `/api/ps` for residency, `/api/generate` with
  `keep_alive:0` to force eviction. **`/api/ps` returning `models: []` is the post-condition for a
  forced unload and is the only reliable way to establish a cold precondition.**
- **DIAGNOSIS QUALITY subsection gains a THIRD entry, and it is mine from this window.** On seeing
  `mcp -` in the UI result line and a `0ms` latency, I raised a possible live safety inversion - a
  confirm-required tool executing ungated - while the listener that would settle it was already
  running and already asked for. **The frames showed `agent_id: native_openhands`, gate live, 6d's
  path.** Same pattern as the two prior entries: **attributing a symptom to the nearest suspicious
  artifact before the available evidence was read.** The cost here was one exchange and some
  alarm; the prior two cost queued patches to wrong artifacts. **Three instances is a pattern, and
  the SDD should state the countermeasure explicitly: when an instrument is already running that
  discriminates the hypotheses, say nothing until it is read.**
- **COMPONENT-LEVEL GUARANTEES DO NOT SURVIVE COMPOSITION - still five worked examples**, none
  added this window.
- **Safety inversions - still four, unchanged**, plus the standing spec-level gap on the
  destructive mailbox tools, which is not an inversion but an absence and should be its own entry.
- **Evidence provenance:** this window's findings rest on a raw-socket client, an independent .NET
  WS listener, forced host-state control, read-only file reads, and one live end-to-end run
  through the real chat UI. **No source file was modified, so nothing here is contingent on a
  patch landing.** Firmest tier.

**Standing instruction:** every handoff from here carries an SDD section, and every window feeds
it.

---

## 13. METHOD LESSONS

1. **FORCING A CONDITION BEATS WAITING FOR IT.** The cold-start hypothesis sat unprovable for two
   windows because nobody had observed run 1 cold. One `keep_alive:0` turned it into a controlled
   experiment and closed it in a single command.
2. **WHEN TWO INSTRUMENTS THAT SHARE NOTHING AGREE TO 86 ms, THE QUESTION IS OVER.** That
   agreement is what cleared v3 - not any amount of reading v3's source.
3. **READ THE INSTRUMENT BEFORE TRUSTING ITS RESULT.** `watch_confirm_auto.ps1` dedupes on
   `confirm_id`. Had it deduped on tool name, cycle two would have been silently skipped and the
   run would have read as a delivery failure. **A negative result from an unread instrument is not
   a finding.**
4. **THE RECORD DRIFTS IN BOTH DIRECTIONS.** Rule 11 was written for patches that claim to land
   and do not. This window found a patch that landed and never claimed anything. Both are the same
   defect in the operator surface.
5. **DO NOT NARRATE AN ALARMING HYPOTHESIS WHILE THE DISCRIMINATING EVIDENCE IS ONE PASTE AWAY.**
   See section 12, DIAGNOSIS QUALITY. The right move was to ask for window 2 and say nothing else.
6. **A MEASUREMENT WINDOW IS A LEGITIMATE WINDOW.** Zero patches, five measurements, three
   questions closed - two of them carried for multiple windows. Nothing was left half-wired
   because nothing was started that could be.
