# HANDOFF 2026-08-26 C - W14

## OPEN ITEM 1 CLOSED. REDACTION NOW COVERS BOTH CONFIRM FRAMES, PROVEN BOTH WAYS. NOT YET COMMITTED.

Predecessor: `HANDOFF-2026-08-26-B-W13-REDACTION-PROVEN-GATE-COMMITTED-6E-IS-THE-BLOCKER.md`
W13 remains the authority on the D-SEC-1 verification method and the `6c132d6` commit.
This file closes W13 next-actions 1 and 2, corrects W13 open items 2 and 7, and
overturns part of SDP section 7.2.

Window opened 12:15 UTC, closed at exchange 17. The box was REBOOTED mid-window
(08:47:25 local) between the patch and its verification - unplanned, and it
produced the window's most useful negative result.

---

## 0. STANDING INSTRUCTIONS CARRIED FORWARD

Pinned. The next window inherits these without renegotiation.

- TOKEN CONSERVATION MODE on working sessions. Short replies, one command at a
  time, minimal restating.
- ALWAYS STATE SHELL AND HOST. Default is PowerShell on the Windows box from
  `PS C:\Users\Admin\OpenJarvis>`. Anything for the Ubuntu ollama host
  (172.16.33.200) must be labeled or wrapped as an ssh command.
- WORKING DIRECTORY IS FIXED at the repo root. Every command must run correctly
  from there. Path, shell or host differences are stated IN THE REQUEST, before
  it is run, never after it fails.
- NO non-ASCII symbols in replies.
- ALWAYS VERIFY. Never stack a second change on an unverified first one.
- FINISH THE THING BEFORE STARTING THE NEXT. No dangling processes.
- DESIGN TESTS TO BE NON-INTERACTIVE.
- SDP IS THE SECONDARY THOUGHT AT ALL TIMES. Every window feeds it.
- EXECUTION PATH REGISTER accumulates across windows. Never re-derived.
- PIN THE DETAIL OF EVERY WINDOW, INCLUDING THE NEGATIVE RESULTS.
- 15-exchange flag is a FLAG, NOT A STOP.
- ARCHITECTURE ARTIFACTS need ports, protocols and encoding at each gate, and
  are delivered as downloadable standalone files for the wiki.
- W12-R1: a command goes in a fenced code block ONLY if it is the command to run
  right now. Reference and restore commands go inline in prose, unformatted.
- W13-R1: an instrument that has never produced a positive reading cannot have
  its silence read as a finding.
- W13-R2: look for the existing harness before writing a new one.
- W13-R3: state the execution context for a script, not just its path.

NEW RULES ADDED THIS WINDOW:

- **W14-R1. ONE COMMAND PER MESSAGE MEANS ONE DESTINATION PER MESSAGE.** A reply
  that contains both a PowerShell command and a chat-app message to type WILL be
  pasted into the wrong window. It happened this window: the harness invocation
  went into the desktop app, where the model described it back instead of a tool
  running. Cost one full 240 s cycle. Split by destination, always.
- **W14-R2. WRITE CONTROL EXPECTATIONS AGAINST THE POST STATE.** Two dry-run
  aborts this window were both control-authoring errors, not patch errors: an
  anchor that was not unique, and a needle whose expected count was computed
  against the pre-patch file while the control ran against the patched text.
  The controls fired correctly both times. Author them against what the file
  will look like AFTER the edit.
- **W14-R3. A WILDCARD THAT MATCHES NOTHING IS SILENT IN POWERSHELL.** A delivery
  one-liner built on `Get-ChildItem <glob> | Select -First 1 | ForEach-Object`
  does nothing at all, with no error, when the file has not been downloaded yet.
  This is a fail-quiet instance in Claude's own delivery mechanism. Every
  delivery command now assigns to a variable and prints a red NOT DOWNLOADED
  message on the empty case.

---

## 1. WHAT WAS DONE

Two W13 next-actions, in order, each verified before the next was started.

### 1.1 Next-action 1 - SDP artifact brought current (revision B)

`SDP-WS-EVENT-CHANNEL-2026-08-26.md` was half a window stale: written 07:04:53,
before run 2, the source read, the commit and the EOL finding.

AMENDED IN PLACE, not rewritten. Ten anchored replacements, each asserted to
match exactly 1. 17,853 B -> 32,391 B, pure LF preserved, 0 non-ASCII. Gate
table, frame contracts, path diagram and D-SEC-1 rationale are byte-identical to
revision A.

Delivered as `SDP-WS-EVENT-CHANNEL-2026-08-26-revB.md` and landed in the repo
root at 08:18:37, 32,391 B confirmed.

Changes: revision B header with commit of record; 3.2 gained the 4 ms ordering
finding; 3.3 marked verified both ways; 5 gained seven timing rows; 6 split into
6.1 channel / 6.2 redaction both ways / 6.3 source read / 6.4 reproduction; 7.4
raised to five fail-quiet instances; new 7.5 ghost-chasing class; new 7.6 EOL
contradiction; 8 item 1 escalated and item 2 closed with a new 2a for the
no-user-can-answer blocker; 9 marked VERIFIED with adversary inversion recorded
as method and posture C stated as HALF implemented; new section 10 on git and
release state.

**REVISION B IS NOW ITSELF STALE.** It does not contain anything in sections 2
through 6 below. See next actions.

### 1.2 Next-action 2 - the widened redaction

Read the live file first rather than patching from W13's description. Lines
25-95 of `src\openjarvis\server\ws_bridge.py` matched W13 section 6 exactly.

SCOPE CORRECTION MADE BEFORE PATCHING: W13 called this a one-line change at line
51. It is four edits. The predicate at 51 is consumed at 58, and the warning text
at 64-65 hardcodes `TOOL_CONFIRM_REQUEST`. Widening 51 alone would have produced
a log line that names the wrong frame type on every resolved-frame redaction - a
false statement in the log, in the same class as the fail-quiet hazards this
package tracks.

Applied by `patch_ws_cid_redact_v2c.py` (repo root, marker
`openjarvis-ws-cid-redact-v2`), dry run clean then `--apply`.

| Property | Value |
|---|---|
| Pre | 4,414 B, CRLF 113 / bare LF 0, SHA256 `3DA94417EB2B0661DDEB7FE56293C0035B577E047AA14C9275FFA06EC0CF5685` |
| Post | 4,514 B (delta +100), CRLF 117 / bare LF 0, SHA256 `BD8904CD9564D7FA07AF4566CF2B41ACD10774A4C02D46A633CE2B68FB2AD3F6` |
| Controls | 9 positive controls, all pass; round-trip byte-identical; py_compile on patched text AND on written file |
| On-disk check | 4,514 predicted, 4,514 actual |

ROLLBACK: Copy-Item 'src\openjarvis\server\ws_bridge.py.bak_cidredactv2_20260826_083355' 'src\openjarvis\server\ws_bridge.py' -Force - then RESTART.

WHAT THE PATCH DID, read back off disk independently at lines 48-75 after apply:

- 50: marker bumped to v2 on the forward-loop block only.
- 51-54: `_is_confirm_event = event.event_type in (TOOL_CONFIRM_REQUEST,
  TOOL_CONFIRM_RESOLVED)`.
- 61: branch consumes the widened predicate.
- 66-71: warning takes the frame type as a parameter,
  `event.event_type.value` first and peer second, in format-string order.
- `_had_cid` guard at 63 untouched, so a frame with no cid still cannot produce
  a spurious warning.

### 1.3 THE MARKER IS NOT A UNIQUE ANCHOR - PIN THIS

The first dry run aborted because `# openjarvis-ws-cid-redact-v1` appears TWICE
at the same indent: once on the forward-loop block (line 50) and once on the
accept-site block (line 83). Both belong to the v1 change.

Consequence for the record: **any future control asserting that the v1 marker
greps back exactly once would have been wrong.** The v2 patch locates the
forward-loop marker POSITIONALLY - the line immediately above the predicate,
with an assertion that it really is the v1 marker - and deliberately leaves the
accept-site marker at v1, because that block did not change.

---

## 2. VERIFICATION - BOTH HALVES, BOTH FRAME TYPES

### 2.1 Unauthenticated half - the exploit stopped working

`watch_confirm_auto.ps1 -MaxSeconds 240`, unmodified, no token, launched with
`Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process -Force;` prefixed.
Provocation "run the shell command hostname" in a FRESH desktop conversation
(`message_count: 2`).

The load-bearing observation is not the missing banner. The
`tool_confirm_resolved` frame at 09:18:12.250 printed UNTRUNCATED in the capture:
`agent_id`, `turn_id`, `tool`, `decision:"timeout"`, `state:"resolved"`,
`created_at`, `expires_at`, `reaped:false` - **and no `confirm_id`.** In W13 run
1 that exact frame type, on that exact script, carried its cid in the clear and
the regex fired on it. Same harness, same regex, same server, opposite result.

Server log, and this is the first positive reading the resolved-frame branch has
ever produced:

- `ws-cid-redact: stripped confirm_id from tool_confirm_request ... 127.0.0.1:56454` (t1)
- `ws-cid-redact: stripped confirm_id from tool_confirm_resolved ... 127.0.0.1:56454` (NEW in v2)
- `ws-cid-redact: stripped confirm_id from tool_confirm_request ... 127.0.0.1:56454` (t2)

**HONEST LIMIT ON THIS RUN, stated because it is a real weakening:** it has NO
in-run positive control. W13 run 1 got one for free precisely because the
resolved frame was unredacted, and v2 removes that. The regex is proven live by
the earlier run against the same build, not by this one. Acceptable only because
the before-picture is the same script on the same server. A future window
wanting an in-run control must use a third frame type that legitimately carries
an id-like field.

### 2.2 Authenticated half - no over-redaction

Over-redaction was the plausible regression from widening the predicate, so the
authed half is not a formality.

`probe_confirm_frames.py --url "ws://127.0.0.1:8010/v1/agents/events?token=<token>" --deadline 240`,
fresh conversation, `message_count: 2`.

- FRAME 3 `tool_confirm_request` WITH `confirm_id` `0e5e7140bbe84f96a0fc610f2b6b5bc6`.
- FRAME 4 `tool_confirm_resolved` WITH the SAME `confirm_id`.
- No `ws-cid-redact` warning naming peer `127.0.0.1:58294` anywhere in the log.

### 2.3 THE PAIR, now complete for both frame types

| | Unauthed (56454) | Authed (58294) |
|---|---|---|
| `tool_confirm_request` carries cid | NO (t1 and t2) | YES |
| `tool_confirm_resolved` carries cid | NO | YES |
| Redaction warning in log | 3 lines, both types named | none |

D-SEC-1 posture C is now FULLY implemented for this transport, not half.

### 2.4 Timings measured this window

- TTL 120.013 s (emit 09:16:12.2346845, reap 09:18:12.24768). Third independent
  measurement, consistent with 120.004 and 120.027.
- Re-request amplification reproduced live: t1 reaped, t2 issued 1.6 s later
  (09:18:13.833), a second 120 s worker slot on the shared pool for one user
  request. The authed run repeated it (t1 09:23:45.254, t2 09:25:46.977).
- Total user-visible time for the failed run: 245.8 s, ending in an apology.

---

## 3. THE REBOOT - W13 OPEN ITEM 2 IS WRONG AS WRITTEN

Unplanned reboot at 08:47:25 between patch and verification. W13 open item 2
predicted the exact consequence: "after a reboot no client can authenticate, so
every confirm-required tool parks a worker 120 s and reaps."

**That prediction failed. The token survived.** Accept log at 09:00:21 read
`authed=True`.

Discriminated rather than assumed, in this order:

1. `authed=True` with the W12 token value.
2. Deliberately wrong token -> `authed=False` (09:06:58). So the auth check
   works and the value in the process is genuinely the expected one. This
   control mattered: without it, "it authenticates" could not be separated from
   "the check is broken."
3. `[Environment]::GetEnvironmentVariable` at Process, User and Machine scope:
   **all three unset.** Presence and length only; no value printed.
4. `OPENJARVIS_WS_TOKEN` in `start-openjarvis.ps1`: **no match.**
5. `^\s*OPENJARVIS_WS_TOKEN\s*=` in `.env`: **no match.** Line numbers and a
   boolean only, per the standing 08/01 rule.
6. All repo-root `.ps1` files: **no match.**

7. Process forensics settled the one theory that would have invalidated
   everything: boot 08:47:25, both python processes created 08:52:53, patch
   written 08:33:55. **The running server started 19 minutes AFTER the patch and
   5 minutes after the reboot, so it serves the new code.** The "stale process
   serving old code" theory is dead, and every measurement in section 2 is
   post-patch. Command lines were deliberately NOT printed - they can carry
   secrets and creation time answers the question alone.

**WHERE THE TOKEN COMES FROM IS UNESTABLISHED.** Remaining candidates: the shell
that launched Jarvis, or something in the desktop app's spawn chain. The hunt
was STOPPED there deliberately - it does not change what the patch does, and
chasing it would have left the verification dangling.

**CORRECTION TO OPEN ITEM 2, on evidence:** "after a reboot no client can
authenticate" is FALSE as stated. What is true is narrower and still a real gap:
the token has no durable, discoverable home, so whether a fresh start comes up
authenticated depends on how it was launched, and nobody can currently say why
it worked. 6e cannot depend on an unlocated secret.

---

## 4. SDP SECTION 7.2 IS OVERTURNED - THE `ua=` FIELD WORKS

The authed accept line read:
`ws-accept: peer=127.0.0.1:58294 authed=True agent_filter=None ua='Python/3.12 websockets/17.0.1'`

W13 section 3.1 and SDP 7.2 recorded the field as permanently null and offered
"find a client that can set the header, or remove the field." **A client that
can set it was already in the repo root.** The limitation is specific to the
.NET Framework `ClientWebSocket` under PowerShell 5.1, not to the field.

CONSEQUENCE: subscriber attribution no longer rests on timestamp correlation
alone. W13 open item 7 closes as KEEP THE FIELD, use a Python client for any
test where attribution matters.

NOTE, not a contradiction: that string reports `websockets/17.0.1` while the
venv holds 15.0.1. Different interpreters - the probe ran on system Python 3.12,
the server on the venv. Worth confirming once if any test ever depends on client
library behavior.

---

## 5. OTHER FINDINGS - CAPTURED, NOT CHASED

- **`"reaped": false` on every timeout resolution.** Present on both runs'
  resolved frames. Reads backwards from what the field name implies for a
  timeout reap. Either the name is misleading or the flag is set elsewhere. New
  to the register; the W13 frame-contract table does not list this field.
- **A live Defect 1 datapoint on a HEALTHY run.** Authed run FRAME 2
  `inference_end` shows `tool_calls: []` while `content` carries the call in text
  form: `<function=shell_exec><parameter=command>hostname</parameter></function>`
  plus a stray `</tool_call>`. The gate fired anyway at FRAME 3, so the parser
  handled the text form. FRAME 6, one turn later, shows `tool_calls` POPULATED
  with `{"name":"shell_exec","id":"call_zuunmmwt"}`. Same model, same prompt, two
  different emission shapes within one turn pair. Cross-reference
  [[openjarvis-defect1-parser]] and [[openjarvis-defect1-engine]].
- **Confabulated limitation on a clean thread.** At 4,002 input tokens,
  `message_count: 2`, the model answered "I don't have the ability to execute
  scripts or commands on your system." `shell_exec` is in its allowlist. This is
  the section 6.2 pattern WITHOUT the poisoned thread that was blamed for it -
  which weakens thread-poisoning as the sole explanation.
- **The user-visible failure mode, again.** 245.8 s, two gates, two reaped
  workers, and an apology mentioning "technical difficulties" and "restrictions
  on executing shell commands." No such restriction exists. This is item 2a.

---

## 6. EXECUTION PATHS REGISTER

Carried unchanged: orchestrator `ask()` via `system\orchestrator.py`;
managed-agent SSE via `_stream_managed_agent()` in `server\agent_manager_routes.py`;
`routes.py` chat dispatch branches 1a/1b/1c/1d.

**AMENDED - the event fan-out leg.** Redaction stage now covers TWO event types
rather than one. Per-client copy path is unchanged: `dict(payload["data"])` then
`dict(payload, data=_data)`, two fresh dicts, shared payload never mutated. The
`getattr(ws, "_ws_authed", False)` default remains the fail-closed mechanism.
Warning now parameterizes the frame type, so the log discriminates which frame
was redacted for which peer - that is what made section 2.1 readable.

Gate/transport facts unchanged: bind `127.0.0.1:8010`, route
`/v1/agents/events`, WebSocket over HTTP/1.1 upgrade, UTF-8 JSON via
`send_json`, accept unconditional, auth via query-string `token` against env
`OPENJARVIS_WS_TOKEN`, field redaction now on TWO event types.

---

## 7. SDP / SDD FEED FROM THIS WINDOW

**`SDP-WS-EVENT-CHANNEL-2026-08-26-revB.md` needs a revision C** covering
sections 2 through 5 above. Specifically:

- Section 3.2: the resolved frame is now redacted for unauthenticated
  subscribers. The whole "still carries confirm_id unredacted" framing is
  obsolete.
- Section 3.3: the redaction rule applies to both confirm event types.
- Section 5: three new timing rows (TTL 120.013, re-request at +1.6 s,
  245.8 s user-visible failure).
- Section 6: new subsection for the v2 verification pair, including the honest
  limit about the lost in-run positive control.
- Section 7.2: OVERTURNED. Rewrite per section 4 above.
- Section 8: item 1 CLOSED; item 2 CORRECTED per section 3; item 7 CLOSED.
- Section 9: posture C is now FULLY implemented for this transport, not half.
- Section 10: add the v2 commit once it exists.

- **The fail-quiet class gains a sixth instance** and it is ours: a PowerShell
  wildcard that matches nothing produces no error and no output, so a delivery
  one-liner silently does nothing. Claude's own tooling exhibited the hazard
  class the package tracks. W14-R3 is the countermeasure.
- **Control-authoring is now a named failure mode** (W14-R2). Two aborts, both
  from expectations written against the pre-patch file. Both were caught by the
  dry run, which is the process working, but the pattern is worth naming: the
  control runs against the POST state.
- **Evidence standard, extended:** the strongest verification available may
  DESTROY the control that made the previous one strong. Redacting the resolved
  frame removed the accidental positive control that W13 celebrated. Record this
  tension in the verification methodology appendix - a hardening change can
  reduce future observability, and that cost should be named at design time.
- **Non-uniqueness of markers** (section 1.3) belongs in the patch-discipline
  chapter alongside the newest-file-selector rule.

---

## 8. OPEN ITEMS, ORDERED

1. **THE v2 CHANGE IS VERIFIED AND UNCOMMITTED.** `ws_bridge.py` at 4,514 B,
   SHA256 `BD8904CD...`, plus `patch_ws_cid_redact_v2c.py` and the revB SDP in
   the repo root. W13 section 7.1 is the precedent: verified and committed are
   different states, and the last window found the entire confirm registry
   untracked. Commit by explicit path, never `-A`. A backup file
   `ws_bridge.py.bak_cidredactv2_20260826_083355` sits in the tree and must NOT
   be committed.
2. **TOKEN PERSISTENCE - reframed, not closed.** See section 3. The token has no
   discoverable home and its survival across the reboot is unexplained. Locate
   the source, then decide where it should live. Gates 6e. No secret goes into
   `.env` while that file is in its current state.
3. **6e. NO USER CAN ANSWER A GATE.** Unchanged and now the only thing between
   this feature and being usable. Mount `useAgentEvents`
   (`frontend\src\lib\useAgentEvents.ts`, points at `/v1/agents/events` at line
   19) with NO `agent_id` param, plus the token from item 2. Every gate this
   window reaped at 120 s; the user saw an apology both times.
4. **Destructive mailbox tools are ungated at the spec level.** Only
   `agent_tools.py:289`, `git_tool.py:283`, `shell_exec.py:71` declare
   `requires_confirmation=True`. Coverage gap, not a mechanism gap.
5. **Four auto-approve sites live** in `server\agent_manager_routes.py`
   (720-721, 1202-1206, 1562-1563, 1639-1640). Accept or overturn explicitly.
6. **Silent frame drop on queue overflow** still has no instrument.
7. **`"reaped": false` on timeout resolutions** (section 5) - unexplained.
8. **Four `[DEBUG]` prints in `cli\serve.py`** at 268, 280, 281, 513, shipped in
   `6c132d6`.
9. **`_stubs.py` EOL baseline contradiction** (W13 section 8) unresolved.
   Re-measure, do not inherit.
10. **08/05 GitLab history damage below the tip** still unassessed.
11. **65-package venv mutation on start** still unchased.

CLOSED THIS WINDOW: W13 open item 1 (resolved-frame cid leak) and W13 open item
7 (`ua=` field dead).

---

## 9. NEXT ACTIONS, ORDERED

1. **Commit the v2 change**, explicit paths only, backup file excluded. Verify
   the staged count before committing. Push to both remotes with an explicit
   refspec - `origin` is GitHub, `gitlab` is GitLab, and that naming is a trap.
2. **SDP revision C** per section 7. Do it in the same window as the commit so
   the artifact does not go stale a third time.
3. **Locate the WS token source** (open item 2), then decide its durable home.
4. **Build 6e.** Only after 3.
5. Then open items 4 and 5 - both need a Gray decision, not just code.

Do not skip ahead to 4. Everything this window measured says the gate is
correct; nothing says it is usable.


---

## APPENDIX A. DISCREPANCY REGISTER

Every point this window where the WRITTEN RECORD disagreed with DIRECT
OBSERVATION. Each entry names the claim, what was actually found, how it was
established, and what a future window should do with it. Discrepancies are
recorded whether or not they changed the outcome - a claim that was wrong and
harmless is still a claim that was wrong.

### D1. "One-line change at ws_bridge.py:51" - INCOMPLETE
- CLAIMED BY: W13 open item 1 and W13 next-action 2.
- FOUND: four edits required. The predicate at 51 is consumed at 58, and the
  warning string at 64-65 hardcodes `TOOL_CONFIRM_REQUEST`.
- ESTABLISHED BY: direct read of lines 25-95 before patching.
- IMPACT IF UNCAUGHT: every resolved-frame redaction would have logged
  "stripped confirm_id from TOOL_CONFIRM_REQUEST" - a false statement in the
  audit log, and the log is the primary instrument for this feature.
- DISPOSITION: corrected in the patch. Scope estimates in a handoff are
  estimates; re-derive from source.

### D2. "`# openjarvis-ws-cid-redact-v1` is a unique anchor" - FALSE
- CLAIMED BY: implicit in the v2 patch design (Claude's).
- FOUND: appears TWICE at identical 8-space indent - forward-loop block (line
  50) and accept-site block (line 83).
- ESTABLISHED BY: `patch_ws_cid_redact_v2.py` dry run, ABORT: anchor matched 2
  times.
- DISPOSITION: forward-loop marker located positionally (line above the
  predicate, asserted); accept-site marker deliberately left at v1 because that
  block is unchanged. Any future control asserting "v1 marker greps back once"
  would have been WRONG.

### D3. "After a reboot no client can authenticate" - FALSE AS STATED
- CLAIMED BY: W13 open item 2.
- FOUND: token survived a genuine reboot. `authed=True` at 09:00:21.
- ESTABLISHED BY, in order:
  1. Authed connect with the W12 token -> `authed=True` (09:00:21, peer 56864).
  2. NEGATIVE CONTROL, deliberately wrong token -> `authed=False` (09:06:58,
     peer 54939). This is the load-bearing step: without it, "it
     authenticates" cannot be distinguished from "the auth check is broken."
  3. `[Environment]::GetEnvironmentVariable('OPENJARVIS_WS_TOKEN', <scope>)` at
     Process / User / Machine -> all three `set=False len=0`.
  4. `start-openjarvis.ps1` -> no match.
  5. `.env` -> no match on `^\s*OPENJARVIS_WS_TOKEN\s*=`.
  6. All repo-root `.ps1` files -> no match.
- UNRESOLVED: where the value comes from. Candidates are the launch shell or the
  desktop app's spawn chain.
- DISPOSITION: open item 2 REWRITTEN, not closed. True statement is narrower:
  the token has no durable, discoverable home, so authentication after a fresh
  start depends on launch method and nobody can currently explain why it worked.
- WHY THE HUNT STOPPED: it does not change what the patch does, and continuing
  would have left the verification dangling. Deliberate, not an oversight.

### D4. "The running process may be serving pre-patch code" - DISPROVEN
- CLAIMED BY: Claude, as the leading theory explaining D3.
- FOUND: boot 08:47:25, both python processes created 08:52:53, patch written
  08:33:55. Server started 19 minutes AFTER the patch.
- ESTABLISHED BY: `Get-CimInstance Win32_Process` creation dates plus
  `Win32_OperatingSystem.LastBootUpTime`. Command lines deliberately NOT
  printed - they can carry secrets, and creation time answers it alone.
- DISPOSITION: theory dead. Every measurement in section 2 is post-patch. This
  check is a PREREQUISITE for any behavioral claim after a patch and should be
  standing procedure.

### D5. "The `ua=` field is permanently null, consider removing it" - OVERTURNED
- CLAIMED BY: W13 section 3.1 and SDP section 7.2.
- FOUND: `ua='Python/3.12 websockets/17.0.1'` on the authed accept (peer 58294).
- ESTABLISHED BY: `probe_confirm_frames.py` run, server accept log.
- CAUSE: the limitation is specific to the .NET Framework `ClientWebSocket`
  under PowerShell 5.1, which cannot set the header. Not a server-side defect.
- DISPOSITION: KEEP THE FIELD. W13 open item 7 CLOSED. Use a Python client for
  any test where subscriber attribution matters. Attribution no longer rests on
  timestamp correlation alone.

### D6. "A resolved cid is spent, so the leak is low severity" - ALREADY
SUPERSEDED, NOW MOOT
- CLAIMED BY: W12, carried into SDP revision A.
- FOUND (W13): the resolved frame is broadcast 4 ms BEFORE `tool_call_start`, so
  it is a pre-execution disclosure channel, not a spent key.
- DISPOSITION: escalated in SDP revision B, and CLOSED by the v2 patch. Recorded
  here so the reasoning chain survives: the original claim was true about REPLAY
  and false about DISCLOSURE. Those are different threat properties and the
  distinction should be explicit in the security chapter.

### D7. Control expectation written against the PRE-patch file - CLAUDE'S ERROR
- WHAT: control `EventType.TOOL_CONFIRM_RESOLVED,` expected count 1, got 2. The
  string legitimately appears in the subscribed set AND in the new predicate
  tuple.
- ESTABLISHED BY: `patch_ws_cid_redact_v2b.py` dry run, ABORT.
- DISPOSITION: fixed by indentation-precise controls (4-space set entry vs
  12-space tuple entries), raising the control count from 7 to 9. Rule W14-R2.
- NOTE: this is the SECOND control-authoring error on the same script. Both were
  caught by the dry run and neither reached the file. The dry-run-before-apply
  discipline is what made two authoring errors cost nothing.

### D8. Delivery command fails silently on a missing file - CLAUDE'S TOOLING
- WHAT: `Get-ChildItem <glob> | Sort | Select -First 1 | ForEach-Object {...}`
  produces NO output and NO error when the glob matches nothing. Two exchanges
  were spent before this was recognized - one of them re-ran a stale command
  from history whose output was byte-identical to the previous abort.
- DISPOSITION: this is a SIXTH instance of the fail-quiet hazard class the
  package tracks, and it is in Claude's own delivery mechanism. Rule W14-R3:
  assign to a variable, test it, print a loud NOT DOWNLOADED message.

### D9. `"reaped": false` on a timeout resolution - FIELD NOT IN THE CONTRACT
- WHAT: the resolved frame carries `reaped` and it reads `false` on a resolution
  whose `decision` is `timeout`.
- DISCREPANCY: the W13 frame-contract table does not list this field at all, and
  its value reads backwards from what the name implies for a TTL reap.
- OBSERVED: both runs, both unauthed (09:18:12.250) and authed (09:25:45.263).
- DISPOSITION: open item 7. Either the field name is misleading or the flag is
  set at a later stage than the emit. Read `confirm_registry._snapshot()` before
  documenting the frame contract in the SDP.

### D10. "The confabulated-limitation failure is caused by thread poisoning" -
WEAKENED
- CLAIMED BY: SDP section 6.2, based on a thread carrying three prior prose
  refusals.
- FOUND: the same failure at `message_count: 2`, 4,002 prompt tokens, on a
  genuinely fresh conversation - "I don't have the ability to execute scripts or
  commands on your system," with `shell_exec` in the allowlist.
- DISPOSITION: thread poisoning is not a sufficient explanation. Do not carry it
  as the cause. Cross-reference [[openjarvis-defect1-engine]].

### D11. `websockets` version mismatch - NOTED, NOT A CONTRADICTION
- WHAT: probe client reports 17.0.1; the venv holds 15.0.1.
- CAUSE: different interpreters. The probe ran on system Python 3.12, the server
  on the venv.
- DISPOSITION: harmless for this window. Confirm once if any future test depends
  on client library behavior rather than protocol behavior.

### D12. `_stubs.py` EOL baseline - CARRIED, STILL UNRESOLVED
- The record says 2 CRLF lines in an LF file; the working copy measured pure
  CRLF (547/0). `serve.py` matched its record (605/22), so the instrument is
  sound and the change is real.
- DISPOSITION: open item 9. Re-measure at the next patch to that file. Do NOT
  inherit the old baseline, and do not read a failed EOL assertion there as
  corruption.

---

## APPENDIX B. PROCESS FLOW AS VERIFIED, WITH REPRODUCTION

This is the confirm-gate flow as it actually behaves on the post-v2 build.
Every stage cites the evidence that establishes it. File and line references are
post-patch.

### B.1 End-to-end flow, one gated tool call

```
[1] Desktop app  --HTTP POST /v1/chat/completions-->  serveroutes.py:46
        evidence: frontend\src\lib\sse.ts:45 (chat UI posts here, not to
        /v1/managed-agents)

[2] routes.py:50  picks up the PRE-BUILT agent from request.app.state.agent
        evidence: app.state.agent assigned serverpp.py:214, from
        cli\serve.py:551-554. The chat path NEVER calls JarvisSystem.ask().

[3] Agent builds its OWN ToolExecutor  agents\_stubs.py:325-332
        with interactive=True and confirm_callback=_server_confirm_callback,
        injected at cli\serve.py:288-318 (marker openjarvis-confirm-live-v1)
        evidence: builder.py's executor is NOT on this path - serve.py passes no
        tool_executor in agent_kwargs (read of serve.py:232-293)

[4] Model emits a tool call
        OBSERVED TWO SHAPES in one turn pair, authed run:
          FRAME 2  tool_calls: []  and the call in content as
                   <function=shell_exec><parameter=command>hostname</parameter>
          FRAME 6  tool_calls: [{"name":"shell_exec","id":"call_zuunmmwt"}]
        Both dispatched. The parser accepts the text form.

[5] GATE  tools\_stubs.py:265  if tool.spec.requires_confirmation:
        guard at 266 passes because 6d supplied interactive + callback
        evidence: only 3 specs declare requires_confirmation - agent_tools.py:289,
        git_tool.py:283, shell_exec.py:71. Of the 12 allowlisted chat tools only
        shell_exec carries it, which is why shell_exec is the test tool.

[6] Registry  confirm_registry.register(tool, agent_id, turn_id)
        returns a 32-hex confirm_id, default_ttl 120.0 s
        evidence: observed 0e5e7140bbe84f96a0fc610f2b6b5bc6 (authed run)

[7] EMIT  self._bus.publish(EventType.TOOL_CONFIRM_REQUEST, {...7 fields...})
        onto BUS A, the agent's instance (cli\serve.py:132)
        evidence: the seven fields observed intact on both runs

[8] WS BRIDGE reaches Bus A via the one-line getattr fix at
        serverpi_routes.py:944 (marker openjarvis-ws-bus-v1)
        without it the chat path is dark regardless of everything above

[9] FAN-OUT  server\ws_bridge.py:43-75  _on_event
        51-54  _is_confirm_event = event_type in (REQUEST, RESOLVED)   <-- v2
        55     iterate list(clients.items()), a snapshot
        56-59  agent_id filter (None for an unfiltered client)
        60     client_payload = payload
        61     if _is_confirm_event and not getattr(ws,"_ws_authed",False):
        62-64    two fresh dicts, confirm_id popped from the copy
        65-71    warning, frame type as parameter                       <-- v2
        73     loop.call_soon_threadsafe(queue.put_nowait, client_payload)
        74-75  RuntimeError / QueueFull swallowed  <-- open item 6, silent drop

[10] CALLBACK BLOCKS a worker thread on confirm_registry.wait(cid)
        shared default ThreadPoolExecutor via asyncio.to_thread

[11a] RESOLVED  POST /v1/tools/confirm {confirm_id, decision}
        200 first resolve, 409 with the recorded decision on a second
        -> tool executes, tool_call_start fires
[11b] TIMEOUT   TTL expires, TOOL_CONFIRM_RESOLVED emitted with
        decision:"timeout", state:"resolved", reaped:false  <-- D9
        -> agent RE-REQUESTS on the next turn, NEW confirm_id, turn suffix +1
```

### B.2 The redaction decision, stated exactly

At stage [9], for EACH connected client independently:

| Client state | REQUEST frame | RESOLVED frame | Log line |
|---|---|---|---|
| `_ws_authed` True | full, cid present | full, cid present | none |
| `_ws_authed` False | cid stripped, all other fields intact | cid stripped, all other fields intact | one `ws-cid-redact` line naming frame type and peer |

FAIL-CLOSED MECHANISM: `getattr(ws, "_ws_authed", False)`. A socket that never
reached the accept site, or where the attribute assignment failed, reads as
UNAUTHENTICATED. It cannot fail open. `_ws_authed` is assigned at exactly one
place, `ws_bridge.py:89`, at accept.

NO MUTATION OF SHARED STATE: `_data = dict(payload["data"])` then
`dict(payload, data=_data)`. Two fresh dicts per client, so an authed and an
unauthed subscriber on the SAME emit cannot interfere. Verified this window -
both client types observed against the same server, correct result each.

### B.3 Reproduction procedure

Anyone re-running this must reproduce BOTH halves. Neither alone proves the
redaction: a null capture with no authed control cannot distinguish redaction
from a broken transport, and an authed capture alone proves nothing about the
adversary.

PRECONDITION CHECK, mandatory before any behavioral claim (see D4):
compare the backend process CreationDate against the patch write time. A process
older than the patch is serving old code and every result is void.

UNAUTHENTICATED HALF - the adversary. From `PS C:\Users\Admin\OpenJarvis>`:
`Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process -Force; .\watch_confirm_auto.ps1 -MaxSeconds 240`
Then, in a SEPARATE window - the desktop app, a BRAND NEW conversation - send:
run the shell command hostname
PASS: no `CONFIRM_ID:` banner at any point, and the `tool_confirm_resolved`
frame prints with no `confirm_id` key.

AUTHENTICATED HALF - the regression control. From the same prompt:
`python .\probe_confirm_frames.py --url "ws://127.0.0.1:8010/v1/agents/events?token=<token>" --deadline 240`
Then a BRAND NEW conversation, same message.
PASS: both `tool_confirm_request` and `tool_confirm_resolved` carry
`confirm_id`, and no `ws-cid-redact` line names that peer.

SERVER-SIDE CORROBORATION for both halves:
Get-Content 'C:\Users\Admin\AppData\Local\OpenJarvis\logs\backend.log' -Tail 300 | Select-String 'ws-accept|ws-cid-redact'

MANDATORY HYGIENE:
- FRESH conversation every run. Verify by `message_count: 2` in the
  `inference_start` frame, NOT by prompt-token count - 4,002 tokens looked fresh
  on a thread that was not.
- ONE destination per instruction. The harness command goes in PowerShell, the
  provocation goes in the app. Mixing them in one message caused a wasted cycle
  this window (W14-R1).
- Expect ~245 s and an apology from the assistant. That is item 2a, not a
  failure of the transport.

### B.4 Evidence index for this window

| Time | Peer | Event | Establishes |
|---|---|---|---|
| 08:33:55 | - | patch written, 4,514 B, SHA256 `BD8904CD...` | the change on disk |
| 08:47:25 | - | system boot | the reboot is real |
| 08:52:53 | - | both python processes created | server is POST-patch (D4) |
| 09:00:21 | 56864 | `authed=True` | token survived reboot (D3) |
| 09:06:58 | 54939 | `authed=False`, wrong token | auth check discriminates (D3) |
| 09:16:12.234 | 56454 | `tool_confirm_request`, no cid | request redaction |
| 09:18:12.247 | 56454 | `tool_confirm_resolved`, NO cid | **the v2 change, proven** |
| 09:18:12 | - | TTL 120.013 s measured | third consistent TTL measurement |
| 09:18:13.833 | - | t2 issued +1.6 s | re-request amplification |
| 09:23:45.254 | 58294 | `tool_confirm_request` WITH cid `0e5e7140...` | no over-redaction |
| 09:25:45.263 | 58294 | `tool_confirm_resolved` WITH same cid | no over-redaction |
| 09:22:38 | 58294 | `ua='Python/3.12 websockets/17.0.1'` | `ua=` field works (D5) |
| all | 56454 | 3 `ws-cid-redact` lines, both frame types named | server-side corroboration |

Capture files in the repo root: `confirm_frames_capture.log` (authed run) and
the `watch_confirm_auto.ps1` console output (unauthed run, not written to file -
capture it next time).
