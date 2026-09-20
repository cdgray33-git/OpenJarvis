# HANDOFF 2026-08-26 B - W13

## REDACTION PROVEN BOTH WAYS. GATE COMMITTED AND PUSHED. 6e IS NOW THE BLOCKER.

Predecessor: `HANDOFF-2026-08-26-A-W12-CID-REDACTION-APPLIED-UNVERIFIED-WS-PATH-SUSPECT.md`
W12 remains the authority on the D-SEC-1 decision and the change description. This
file corrects W12 section 5 and closes W12 next-actions 1, 2, 3 and 6.

Window opened 06:48, closed at exchange 18. Backend was started once before this
window and left running throughout. No restart was needed.

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

NEW RULES ADDED THIS WINDOW:

- **W13-R1. AN INSTRUMENT THAT HAS NEVER PRODUCED A POSITIVE READING CANNOT HAVE
  ITS SILENCE READ AS A FINDING.** Establish the positive reading first, then
  interpret absence. See section 2.
- **W13-R2. LOOK FOR THE EXISTING HARNESS BEFORE WRITING A NEW ONE.** Section 4
  found four candidate scripts already in the repo root, one of which did the job
  unmodified. A `Get-ChildItem | Sort LastWriteTime` costs one exchange and saved
  a rewrite.
- **W13-R3. STATE THE EXECUTION CONTEXT FOR A SCRIPT, NOT JUST ITS PATH.** A bare
  `.\script.ps1` failed on execution policy in a fresh window. Say how to launch
  it, including policy scope, in the same message.

---

## 1. GRAY'S CALL THAT OPENED THE WINDOW

Gray's opening position, before any command was run:

> "I ran one command to install websockets the other day. We appear to be looking
> for a component that we never validated existed or what it does. We should
> verify all components and not chase ghosts."

**He was right, and W12's central blocker did not exist.** Record this as a
judgment call that changed the window's direction, not as a lucky guess. It is
the third instance of this failure class in the project record: the retracted
"Defect 5 broken folder quoting", the three windows planned around
`patch_confirm_resolved.py` which had already been applied, and now this.

---

## 2. W12 SECTION 5 IS OVERTURNED - THERE WAS NO MISSING COMPONENT

W12 recorded verification as BLOCKED on a suspected missing `websockets` package.
The evidence was that zero `ws-accept:` lines had ever appeared in the log.

**That absence proved nothing.** `ws-accept:` is a log line created BY the patch
under test. No subscriber had connected since the patch was applied, and 6e does
not exist, so no shipped code subscribes. Zero subscribers produces zero accept
lines on a completely healthy path.

Measured, PowerShell, Windows box, repo root:

    $env:VIRTUAL_ENV="C:\Users\Admin\OpenJarvis\.venv"; uv pip list | Select-String -Pattern 'websockets','uvicorn','wsproto'

Result: `uvicorn 0.41.0` (positive control) and `websockets 15.0.1` both present.
`wsproto` absent and NOT required - uvicorn needs one WS backend and has one.
`wsproto` was only ever in the search because it is an alternative uvicorn
backend, never because it was found in this tree. It is a ghost; drop it.

W12 next-action 2 - "fix it durably in `start-openjarvis.ps1`'s dependency set" -
would have been work against a non-problem. **Do not do it.**

Note the venv has NO pip (`No module named pip`); it is uv-managed, hence the
`VIRTUAL_ENV` prefix.

---

## 3. PART ONE CLOSED - THE CHANNEL

Two runs, one variable changed, using `System.Net.WebSockets.ClientWebSocket`
from PowerShell 5.1.

| Run | Input | STATE | Log line |
|---|---|---|---|
| A | connect, no token | Open | `06:57:44,923 ws-accept: peer=127.0.0.1:62390 authed=False agent_filter=None ua=None` |
| B | connect with `?token=w12-verify-2f7a91c4` | Open | `07:00:03,261 ws-accept: peer=127.0.0.1:64453 authed=True agent_filter=None ua=None` |

Run A is the control for run B. Together they prove the WS upgrade succeeds,
`websockets` is functional in the running process, the accept log fires, the
token reaches the backend environment, and the comparison distinguishes a correct
token from none.

### 3.1 NEGATIVE RESULT - the `ua=` field is dead

`$ws.Options.SetRequestHeader("User-Agent", ...)` **THROWS** on the .NET Framework
`ClientWebSocket` under PowerShell 5.1. That header is property-controlled and is
not settable through that method. The exception is non-terminating, so the connect
still succeeds and the operator sees `STATE: Open` next to a red error block.

Both accept lines show `ua=None` as a result. **The prospective
process-identification purpose recorded for this field in W12 section 2.2 is NOT
satisfied.** Attribution in runs A and B rests on timestamp correlation alone,
adequate only because nothing else subscribes. Either find a client that can set
the header, or remove the field rather than leave a permanently-null column.

This was a Claude error: a control was specified without checking it could execute
in the target shell.

---

## 4. THE HARNESS SEARCH - W13-R2 IN ACTION

Before writing a part-two harness, a listing of repo-root scripts by mtime turned
up four candidates. Reading two headers settled it.

- **`probe_confirm_frames.py`** (7,154 B, 08/24, marker
  `openjarvis-confirm-frames-v1`). Opens the socket itself, `--url` override,
  `--deadline` / `--grace`, exits on its own, prints full untruncated JSON, writes
  `confirm_frames_capture.log`. Sends nothing, provokes nothing, resolves nothing.
  Single socket only, and the capture log filename is hardcoded, so two instances
  would collide.
- **`watch_confirm_auto.ps1`** (5,246 B, 08/22). The auto-approve harness behind
  the 08/22 HTTP-200-in-186ms result. Parameters `-MaxSeconds`, `-Url`,
  `-ConfirmUrl`, `-NoApprove`. Header already names four outcomes and what each
  discriminates.
- `ws_probe.py` (32,571 B, 08/23) and `post_timing_probe.py` (5,970 B, 08/24) were
  not needed and were not read.

**`watch_confirm_auto.ps1` reads `confirm_id` by regex** at line 109
(`[regex]::Match($txt, '"confirm_id"\s*:\s*"([^"]+)"')`) guarded by
`if ($cm.Success)` at 110. It does not dereference a key blindly, so an absent
`confirm_id` produces no exception - the approve block at 117-120 is simply
skipped. That makes the pass/fail a clean binary on whether the yellow
`CONFIRM_ID:` banner prints.

### 4.1 THE KEY REFRAME - the harness IS the adversary

`watch_confirm_auto.ps1` was written 08/22 with no token support. It subscribes
unauthenticated, reads a `confirm_id` off the broadcast, and resolves the gate
with it. **That script is the D-SEC-1 finding, running.** It is not a
hypothetical local process; it is a real one sitting in the repo root.

So part two did not need a new test. It needed the known-working exploit run
against the patched server, where a PASS means the exploit STOPS working. This
removes the ambiguity of a null capture: the question is not "did a frame arrive"
but "did a known-working exploit stop working."

### 4.2 Launch context

A bare `.\watch_confirm_auto.ps1` fails in a fresh window with
`PSSecurityException` - the file is unsigned. Launch with
`Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process -Force;` prefixed.
`-Scope Process` needs no admin rights, does not touch CurrentUser or
LocalMachine, and reverts when the window closes. This is W13-R3.

---

## 5. PART TWO CLOSED - THE REDACTION, PROVEN BOTH WAYS

### 5.1 RUN 1 - unauthenticated adversary. PASS.

`watch_confirm_auto.ps1 -MaxSeconds 240`, unmodified, no token. Provocation:
"run the shell command hostname" in the desktop app.

Two `tool_confirm_request` frames arrived (07:14:26.326 and 07:16:50.472). Both
carried `agent_id`, `turn_id`, `tool`, `args_digest`, `prompt`, `expires_at`.
**NEITHER carried `confirm_id`.**

**THE ACCIDENTAL POSITIVE CONTROL - this is the load-bearing part.** On the same
socket, in the same run, the `tool_confirm_resolved` frame at 07:16:26.353
arrived WITH `"confirm_id":"e9d78f479ddc443aa630a0510135018a"` plainly visible,
and the regex fired on it. That simultaneously kills "the matcher was broken" and
"no frame arrived" as explanations for the absence on the request frames. One
frame type redacted, one not, same second, same client, same regex.

This was not designed. It is better evidence than the test that was designed.

### 5.2 THREE FINDINGS FROM RUN 1

- **A REAP DOES EMIT A RESOLVED FRAME.** This was an open question at the start of
  the window. Timeout reap at 07:16:26.353 published
  `decision:"timeout"`, `state:"resolved"`.
- **TTL MEASURED AT 120.027 s.** Emit 07:14:26.326, reap 07:16:26.353. Matches
  `confirm_registry.default_ttl = 120.0` exactly.
- **409 WRITE-ONCE HOLDS AGAINST A REAL OUT-OF-BAND RESOLVER.** The adversary
  obtained a cid from the resolved frame and POSTed approve: HTTP 409 in 16 ms.
  The key was already spent.

### 5.3 RUN 2, FIRST ATTEMPT - INCONCLUSIVE, NOT A FAIL

Authed socket, `?token=w12-verify-2f7a91c4`. **No `tool_confirm_request` frame
fired at all.** The model called `think`, told itself it could not execute shell
commands "due to security restrictions", and answered from that. `shell_exec` was
never dispatched, the gate was never reached, the redaction was never tested.

Cause: `message_count` 6 then 8. **The thread was poisoned** - it already held
three of the model's own prose refusals from the run-1 provocations. This is the
known Defect 1 trigger: once prior assistant prose claiming a limitation is in
context, the model answers from its own prose instead of invoking the tool. The
"security restrictions" line is confabulation; no such restriction exists, the
gate simply parks and reaps invisibly.

### 5.4 RUN 2, FRESH THREAD - PASS. ALL FOUR CRITERIA IN ONE PASS.

Same command, brand-new conversation, `message_count: 2`.

- `tool_confirm_request` at 07:30:03.249 **WITH** `confirm_id`
  `0288e8d0ec7a4d87b1c0156b9c9a67f4`.
- Approve POST: **HTTP 200 in 115 ms.** Body
  `{"confirm_id":"...","tool":"shell_exec","turn_id":"626fa33c-t1","state":"resolved","decision":"approved"}`.
- `tool_confirm_resolved` at 07:30:03.388, `decision:"approved"`.
- `tool_call_start` at 07:30:03.392, **143 ms after the emit** against a 120 s TTL.
  The upper bound is what discriminates "resolve released the worker" from "it
  timed out and looked right."
- `tool_call_end` success=true, latency 0.094 s, real stdout `WIN-OCBK1PNL3G6`,
  exit code 0.

### 5.5 THE PAIR

| | Run 1, no token | Run 2, token |
|---|---|---|
| `tool_confirm_request` carries `confirm_id` | NO (twice) | YES |
| Approve result | 409, cid spent | 200 in 115 ms |
| Tool executed | No, reaped at 120.027 s | Yes, 143 ms after emit |

Neither run alone proves the redaction. The pair does.

---

## 6. SOURCE READ - IMPLEMENTATION CONFIRMED, NOT JUST BEHAVIOR

Everything above is behavioral. The forward loop in
`src\openjarvis\server\ws_bridge.py` was then read directly, because a patch
description standing in for an observation is exactly what produced the
`websockets` ghost.

- **32-33**: both `TOOL_CONFIRM_REQUEST` and `TOOL_CONFIRM_RESOLVED` are in the
  subscribed event set.
- **51**: `_is_confirm_request = event.event_type is EventType.TOOL_CONFIRM_REQUEST`
  - identity comparison against the enum member, computed ONCE outside the client
  loop, scoped to one event type.
- **52**: `for ws, (queue, loop) in list(clients.items())` - iterates a snapshot.
- **57-58**: `client_payload = payload` first, then the branch on
  `_is_confirm_request and not getattr(ws, "_ws_authed", False)`. **The `getattr`
  default of `False` IS the fail-closed mechanism** - a socket that never went
  through accept, or where the attribute assignment failed, reads as
  unauthenticated. It cannot fail open.
- **59-61**: `_data = dict(payload["data"])` then
  `client_payload = dict(payload, data=_data)`. Two fresh dicts. The shared payload
  is genuinely never mutated and the copy is genuinely per client, so an authed and
  an unauthed subscriber on the same emit cannot interfere.
- **60**: `_had_cid = _data.pop("confirm_id", None) is not None` - the warning at
  62-67 is gated on the key having actually been present, so it cannot fire
  spuriously.
- **89**: `websocket._ws_authed = _authed` set at accept.

Implementation matches behavior matches documentation. Closed.

---

## 7. COMMITTED AND PUSHED

### 7.1 The find that changed the commit

`git status --short` showed **`src/openjarvis/core/confirm_registry.py` as
UNTRACKED.** The module the entire gate runs on - register, wait, resolve, TTL,
409 write-once - had never been in the repo. Every piece of work since 08/20
depended on a single on-disk copy with no git rollback point. Any repo-root
cleanup would have destroyed it.

This is why the commit is the whole coherent feature set and not just
`ws_bridge.py`. Committing the redaction alone would have put a redaction into
HEAD for an event type HEAD did not emit, on top of a registry HEAD did not have.

### 7.2 `.env` is protected - verified, not assumed

`git check-ignore -v .env` returns `.gitignore:48:.env`. Confirmed by matching
rule. `check-ignore` prints the rule and path only and reads no content, so the
08/01 standing rule on the secrets file holds.

### 7.3 The commit

**`6c132d6`** on `main`. 6 files, 524 insertions, 7 deletions.
`create mode 100644 src/openjarvis/core/confirm_registry.py`.

Staged by explicit path, never `-A`. Staged count verified at exactly 6 before
committing. The other 11 modified files in the tree (TTS, mailbox, engine,
frontend, weeks old) were left untouched.

Files: `core/confirm_registry.py` (new, 197 lines), `server/ws_bridge.py` (+33),
`tools/_stubs.py` (+153), `cli/serve.py` (+55), `server/agent_manager_routes.py`
(+91), `server/api_routes.py` (+2/-1).

The commit message carries eight `-m` blocks including the known-open item, so
the reasoning survives outside the handoffs.

### 7.4 Both remotes

**REMOTE NAMING IS A TRAP. `origin` is GitHub. `gitlab` is GitLab.**

- `gitlab` -> `http://172.16.33.126/root/openjarvis-desktop.git`
- `origin` -> `https://github.com/cdgray33-git/OpenJarvis.git`

Before pushing, `main` had **no upstream configured** - the safe state, since a
bare `git push` cannot fire or pick a remote.

**THE 08/05 MIRROR DAMAGE IS NOT VISIBLE AT THE TIP.** Both remotes were at
`58c05e28`, and `git merge-base --is-ancestor 58c05e28 main` returned exit 0 -
that tip IS an ancestor of local main. GitLab holds real OpenJarvis history, not
`claude-code-templates`. So no divergence, no force, no recovery decision needed.

**HONEST LIMIT:** exit 0 proves the TIP is in our history. It does NOT prove
GitLab's older history matches GitHub's. Good enough to fast-forward safely,
since a fast-forward cannot destroy anything, but **not a clean bill of health on
the 08/05 damage. That question remains open and is separate.**

Both pushes clean, explicit refspec, no `--mirror`, no `--force`:
`58c05e2..6c132d6  main -> main` on each.

### 7.5 Backups reaped

Both `ws_bridge.py.bak_cidredact_*` files hashed identically to each other
(2,877 B, `EB5A92C2...`) and differently from the live file (`3DA94417...`),
confirming genuine pre-patch content and that the committed file is the patched
one. Deleted by explicit path, not wildcard. Count 0 confirmed after.

Rollback for this change is now `git revert 6c132d6` or checkout of `58c05e2`.

---

## 8. NEGATIVE RESULT - THE `_stubs.py` EOL BASELINE CONTRADICTS THE RECORD

EOL byte-count of the working copy, taken immediately after the commit:

| File | CRLF | bare LF |
|---|---|---|
| `tools\_stubs.py` | **547** | **0** |
| `cli\serve.py` | 605 | 22 |
| `server\ws_bridge.py` | 113 | 0 |

**`_stubs.py` is now a PURE CRLF file.** The record since 08/20 says it has 2 CRLF
lines (16 and 175, from the 08/19 PowerShell splice) in an otherwise LF file.
Every patch script written against it used that shape - the split-on-`\n`
round-trip proof and the "assert CRLF count unchanged" control both rest on it.
**That premise is false as of now.**

Two candidate explanations, not discriminated: the file was converted since 08/20
by a patch script, an editor, or git; or the original finding was wrong in the
same way W12 section 5 was wrong. `serve.py` at 605/22 DOES match the record, so
the measuring instrument is sound, which makes the `_stubs.py` figure a real
change rather than a measurement error.

**ACTION FOR THE NEXT PATCH TO `_stubs.py`: re-measure, do not inherit.** And git
warned six times it will normalize CRLF to LF next time it touches these files, so
the baseline will move again. A future window must not read a failed EOL
assertion as file corruption.

---

## 9. OPEN ITEMS, ORDERED

1. **`TOOL_CONFIRM_RESOLVED` still leaks `confirm_id` to unauthenticated
   subscribers.** Subscribed at `ws_bridge.py:33`, no treatment in the forward
   loop. W12 deferred this on the reasoning that a resolved cid is spent, which
   run 1 confirmed for the TIMEOUT case (409). **But run 2 exposed the case that
   reasoning did not cover:** `tool_confirm_resolved` at 07:30:03.388,
   `tool_call_start` at 07:30:03.392 - **the resolved frame is broadcast 4 ms
   BEFORE the tool starts running.** An unauthenticated local process learns a
   valid cid, its tool, its turn_id, and that it was approved, as execution
   begins. Not replayable (409 enforced), but it is an unauthenticated
   intelligence feed on every gated operation. Under posture C - the cid never
   reaches an unauthenticated subscriber at all - this is unfinished business, not
   accepted risk. **Fix is small: widen line 51 to cover both confirm event types.
   The `_had_cid` guard already handles a frame with no cid, so the branch is safe
   on either.** Own change, own verification pass.
2. **TOKEN PERSISTENCE. The system is fail-closed in normal operation right now.**
   `w12-verify-2f7a91c4` is session-scoped, set in the shell that launched the
   server. After a reboot no client can authenticate, so every confirm-required
   tool parks a worker 120 s and reaps. Run 1 is what that looks like from the
   user's seat. Must be solved before 6e. No secret goes into `.env` while that
   file is in its current state (45 lines, 11 valid `KEY=value`, remainder a
   credential scratchpad python-dotenv silently skips).
3. **6e. NO USER CAN ANSWER A GATE.** The only reason `hostname` ran is that a
   PowerShell script stood in for a UI that does not exist. In run 1 the model
   asked permission in prose, Gray said yes, and it apologized and gave up - twice.
   Two gates fired, both parked a worker 120 s on the shared ThreadPoolExecutor,
   and the user-visible result was an assistant that looks broken. **This is now
   the gating item for the feature being USABLE rather than merely CORRECT.**
   Mount `useAgentEvents` (`frontend\src\lib\useAgentEvents.ts`, already exists,
   points at `/v1/agents/events` at line 19) with NO `agent_id` query param, plus
   the token from item 2.
4. **Destructive mailbox tools are ungated at the spec level.** Only
   `agent_tools.py:289`, `git_tool.py:283` and `shell_exec.py:71` declare
   `requires_confirmation=True`. `mailbox_move_to_trash` and
   `mailbox_empty_folder` do NOT. No amount of gate wiring reaches them. Coverage
   gap, not a mechanism gap.
5. **Four auto-approve sites live** in `server\agent_manager_routes.py` (720-721,
   1202-1206, 1562-1563, 1639-1640), each `confirm_callback=lambda _prompt: True`.
   Three are DeepResearchAgent-only. The fourth builds an ad-hoc per-tool executor
   and calls `execute()` directly, bypassing the agent, on the managed-agent SSE
   stream. Its rationale is stated as deliberate - wizard-added tools as
   pre-approved. Accept or overturn explicitly.
6. **Silent frame drop on queue overflow** has no instrument. A slow client cannot
   tell it missed a frame.
7. **`ua=` field is dead** (section 3.1). Fix the client or remove the field.
8. **Four `[DEBUG]` prints in `cli\serve.py`** at lines 268, 280, 281, 513 shipped
   in `6c132d6`. Line 513 (memory_backend wiring) is NEW to the register - the
   record had only three. Removal is a tracked follow-up: four lines, one restart
   to verify the agent still comes up with 12 tools loaded.
9. **08/05 GitLab history damage below the tip** (section 7.4) still unassessed.
10. **65-package venv mutation on start** (W12 section 8) still unchased.

---

## 10. EXECUTION PATHS REGISTER

Standing structure per path: entry point, call chain with file:line, which
ToolExecutor instance serves it and how constructed, whether the confirmation gate
is live / auto-approved / absent, what event bus traffic it emits, whether a human
is present.

Carried unchanged: orchestrator `ask()` via `system\orchestrator.py`;
managed-agent SSE via `_stream_managed_agent()` in `server\agent_manager_routes.py`;
`routes.py` chat dispatch branches 1a/1b/1c/1d.

**AMENDED THIS WINDOW - the event fan-out leg, now with source-read confirmation:**

`ws_bridge.create_ws_router(event_bus)` subscribes one `_on_event` handler to 13
event types including both confirm types (lines 32-33). Fan-out is per client via
`asyncio.Queue(maxsize=100)` plus a stored loop reference, delivered with
`loop.call_soon_threadsafe` - the thread-boundary crossing between the tool worker
thread and the socket's event loop. A full queue or closed loop is swallowed
silently (`except (RuntimeError, asyncio.QueueFull): pass`).

Two filter stages: `_agent_filter` from the `agent_id` query param (line 53), and
per-client cid redaction keyed on `_ws_authed` (lines 57-61).

Gate/transport facts: bind `127.0.0.1:8010`, route `/v1/agents/events`, protocol
WebSocket over HTTP/1.1 upgrade, `websockets 15.0.1` under `uvicorn 0.41.0`,
payload UTF-8 JSON via `websocket.send_json`, accept unconditional, auth via
query-string `token` against env `OPENJARVIS_WS_TOKEN`, field redaction on one
event type.

**MEASURED PATH LATENCY, live, run 2:** emit 07:30:03.249 -> frame at client
(same ms) -> approve POST 200 in 115 ms -> `tool_call_start` 07:30:03.392, 143 ms
after emit -> `tool_call_end` latency 0.094 s.

---

## 11. SDP / SDD FEED FROM THIS WINDOW

Standalone artifact already delivered for the wiki:
**`SDP-WS-EVENT-CHANNEL-2026-08-26.md`** - gate table with ports/protocol/encoding,
inputs, outputs, full frame contracts, the path diagram through both buses with the
thread boundary marked, observed timings with what each discriminates, the
verification record, negative results, and the D-SEC-1 posture with rationale.
**That artifact predates sections 5 through 8 of this handoff and needs updating
with the run-1/run-2 pair, the source read, the commit, and the EOL finding.**

- **Security chapter, D-SEC-1: the decision is now VERIFIED, not merely applied.**
  Record the adversary-inversion method - the exploit script itself as the test -
  as the strongest form of the evidence standard. A verification is worth what it
  can discriminate; "a known-working exploit stopped working" discriminates more
  than "a frame arrived."
- **The accidental positive control in run 1** belongs in the verification
  methodology appendix. Two frame types on one socket, one redacted and one not,
  in the same second, is a self-validating instrument. Design for this deliberately
  where possible.
- **The fail-quiet pattern, now FIVE instances**, is a cross-cutting hazard class,
  not five separate bugs: `_confirm_callback = None` accepting silently; a missing
  WS backend returning HTTP 200 with the SPA body; the WS queue swallowing
  overflow; a bad mailbox `account` id returning a silent zero; and the four
  `[DEBUG]`-free but silent auto-approve stubs. Instance 3 lives inside this
  transport and has no instrument.
- **The ghost-chasing pattern is also now a named class with three instances**
  (section 1). Both classes have the same root: a description or an absence
  treated as an observation. W13-R1 is the countermeasure.
- **Threading model:** the 120.027 s measured TTL, the shared-pool occupancy, and
  the re-request amplification (N x 120 s, not 120 s once) are capacity facts the
  gate chapter needs.
- **Git hygiene:** the untracked-registry find is worth one paragraph on why a
  verified change and a committed change are different states.

---

## 12. NEXT ACTIONS, ORDERED

1. **Update `SDP-WS-EVENT-CHANNEL-2026-08-26.md`** with sections 5 through 8 of
   this handoff. It is the wiki artifact and is currently half a window stale.
2. **Close open item 1** - widen `ws_bridge.py:51` to cover
   `TOOL_CONFIRM_RESOLVED`. One-line change, own verification: re-run
   `watch_confirm_auto.ps1` unauthed and confirm the `CONFIRM_ID:` banner NEVER
   prints, not even at +120 s. Run 1 of this window is the before-picture.
3. **Solve token persistence** (open item 2). Decide where the token lives given
   the `.env` state. This gates 6e.
4. **Build 6e** (open item 3). Only after 2 and 3.
5. Then open items 4 and 5 - the coverage gap and the auto-approve ruling. Both
   need a Gray decision, not just code.

Do not skip ahead to 4. An unverified interlock is worth less than a documented
absence of one, and a gate no user can answer is worth less than no gate at all.
