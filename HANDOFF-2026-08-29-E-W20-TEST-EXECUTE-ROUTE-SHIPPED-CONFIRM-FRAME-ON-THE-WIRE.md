# HANDOFF 2026-08-29 E / WINDOW 20
# TEST-EXECUTE ROUTE SHIPPED - CONFIRM FRAME ON THE WIRE - REDACTION STILL UNMEASURED

Predecessor: HANDOFF-2026-08-29-D-W19-REDACTION-REPOINTED-TO-BIND-VERIFIED-AND-SHIPPED.md
Window start budget: 55 percent session used. Window end: near cap.
Host: Windows box. Shell: PowerShell 5.1. Working dir: `PS C:\Users\Admin\OpenJarvis>`.
Backend: 127.0.0.1:8010, ollama, qwen3-coder:30b, agent native_openhands.

---

## 0. ONE PARAGRAPH FOR THE NEXT WINDOW

Open item 22 is CLOSED. There is now a direct tool-execution route that reaches the
confirmation gate deterministically with no model in the path, and the gate's
`TOOL_CONFIRM_REQUEST` was observed arriving at a bare WebSocket client for the first
time. Open item 20 - whether the v3 redaction preserves `confirm_id` on the wire - is
STILL NOT MEASURED, and the reason is a defect in the probe, not in the server. Do not
record item 20 as verified. The next window's first job is a one-line read of the
probe's confirm-frame collector, then a re-run of the exact same two-window procedure
documented in section 5.

---

## 1. WHAT WAS DECIDED (rulings, do not revisit)

- **RULING: TEST-ONLY ROUTE.** Of W18 section 6.E's three options for reaching the gate
  deterministically, Gray chose the dedicated test entry point. The managed-agent route
  was rejected because it runs the four auto-approve sites (item 6), so the gate reached
  is not the gate under measurement. The model-selection route was rejected because it
  inherits Defect 1 and cannot be made deterministic.
- **RULING: THE FIRST LIVE RUN DENIES**, not approves. Denial proves the whole chain and
  executes nothing. Honored - see section 5, nothing was ever executed.
- **RULING: THE DISCRIMINATOR IS `CURRENT_TURN_ID`**, set by the test route to
  `test-<run_id>` immediately before `execute()` is called. Gray's reason, recorded
  verbatim: "then we have control and know exactly the variable."
  This SUPERSEDED Claude's proposal to add a new `run_id` field to the emit payload.
  Claude's proposal was worse and Claude withdrew it: the gate already emits `turn_id`
  from the ContextVar at `tools\_stubs.py:97`, so the discriminator was already
  available for free, and adding a field would have required a second edit to
  `tools\_stubs.py`. **Net effect: `tools\_stubs.py` was not touched at all in W20.**
  The gate, the emit, and the three-way ToolResult keep exactly the shape verified in
  6c and 6d.

---

## 2. WHAT WAS BUILT

### 2.1 The route

`POST /v1/tools/test-execute`, added to the existing `tools_router` inside
`create_agent_manager_router()` in `src\openjarvis\server\agent_manager_routes.py`.

Same host router as `/v1/tools/confirm`, chosen so it inherits a mount already proven
live and never goes near the bare-except swallow at `api_routes.py:946`.

Behavior:

- Takes `request.app.state.agent._executor`. **It constructs nothing.** This is the
  single most important property of the design. An ad-hoc `ToolExecutor` would have
  measured an executor built for the test rather than the one 6d wired. By using the
  live agent's instance the route inherits, without re-establishing any of them:
  `interactive=True`, the 6d server confirm callback, `agent_id="native_openhands"`,
  and serve.py's EventBus - which is the bus the WS bridge reads after the bridge fix.
- Guard, four conditions, all required:
  1. env `OPENJARVIS_TEST_EXEC` truthy (default OFF)
  2. `app.state.bind_is_loopback` is True (reuses W19's published stamp, does not
     re-derive a bind fact)
  3. the tool is on the live agent's own list, via the public `available_tools()`
  4. **the tool's spec declares `requires_confirmation=True`, else 422**
- Condition 4 is the answer to the surface-area objection. The route is structurally
  incapable of executing anything that does not first park on the gate and wait for a
  POST to `/v1/tools/confirm`. **It adds a trigger, not a bypass.** This was proven at
  runtime, not asserted - see section 5.1.
- Conditions 1 and 2 fail with **403 and a distinct body**, never 404, so a probe can
  discriminate "route present but disabled" from "route never mounted". This is the
  400-not-404 standard from 08/20 applied to new code.
- Returns **202 immediately** with `run_id`, `turn_id`, `tool`, `marker`, and dispatches
  `execute()` on a background thread via `asyncio.to_thread`, matching what
  `stream_bridge.py:155` already does on the chat path. Blocking the HTTP response for
  the full 120 s TTL would have made the probe a concurrency exercise; returning at once
  keeps it a straight sequential script, per the non-interactive rule.
- The thread target sets `CURRENT_TURN_ID` to `test-<run_id>` before calling execute and
  resets it in a `finally`. `asyncio.to_thread` runs the target in a copied context, so
  the set is scoped to that run and cannot leak into a chat turn.

### 2.2 Reads taken before writing (W16-R3 compliance)

Nothing in the route was predicted from a call site. Every load-bearing fact was read:

| Fact | Where read | Value |
|---|---|---|
| `CURRENT_TURN_ID` | `tools\_stubs.py:97` | `contextvars.ContextVar` |
| gate reads it | `tools\_stubs.py:291,300,323` | emitted as `turn_id` |
| executor tool storage | `tools\_stubs.py:165` | `self._tools: Dict[str, BaseTool]` keyed by `t.spec.name` |
| public spec accessor | `tools\_stubs.py:471-473` | `available_tools() -> List[ToolSpec]` |
| `ToolCall` origin | `tools\_stubs.py:23` | `from openjarvis.core.types import ToolCall, ToolResult` |
| `ToolCall` shape | `core\types.py` | `id: str`, `name: str`, **`arguments: str  # JSON string`** |

**The last row changed the code.** `ToolCall.arguments` is a JSON STRING, not a dict.
Had this not been read, the handler would have passed a dict and failed at runtime
somewhere downstream of the gate, which is the worst place to discover it. The route
does `json.dumps(args)`. Pin this: it is a recurring shape trap.

### 2.3 The patch script

`patch_testexec_v1.py`, delivered to Downloads, copied to repo root, run from there.

- Marker `openjarvis-test-exec-v1`, refuses to apply twice on marker presence.
- SHA gate against the exact pre-image. This is the load-bearing check.
- Three-line anchor ending on `"decision": entry.get("decision", "")`, required to match
  **exactly once**, inserting AFTER the confirm handler's closing paren (line 2125) and
  BEFORE the SendBlue rule comment (line 2127). The SendBlue comment is double-encoded
  on disk; anchoring on ASCII-clean text meant **no rule comment was touched**.
- Replica dry run (W19-R4): builds a synthetic CRLF replica, asserts single anchor hit,
  CRLF delta equals inserted line count, bare LF unchanged, marker present, control line
  survives, and block lands BEFORE the sendblue router.
- Prints `sys.executable` (W19-R2).
- Encoding control: counts occurrences of `SendBlue auto-setup helpers` pre and post and
  aborts on any change.
- Timestamped backup, then py_compile with a printed restore command on failure.

---

## 3. VERIFIED FACTS (measured this window)

### 3.1 Patch application

| | Pre | Post |
|---|---|---|
| Bytes | 93952 | 99076 |
| SHA256 | 94EC6F3F...9AD00E1C | 5B3577A9...42E0C10B3 |
| CRLF | 2302 | 2448 (+146, equals inserted lines) |
| Bare LF | 0 | 0 |

Marker count 4, route count 1, confirm-route control 1, sendblue control 1,
py_compile OK. Predicted length matched on-disk length exactly.

### 3.2 Route liveness, three-way discriminated

`POST /v1/tools/test-execute {"tool":"mailbox_list_accounts"}` returned **422**.

Discriminator stated BEFORE the run: 404 would mean the route never mounted in the live
process; 403 would mean mounted but the env flag did not reach the backend; 422 means
mounted, enabled, and the guard refused a tool that does not declare
`requires_confirmation`. 422 was observed, so all three propositions are settled by one
call, and the guard's refusal property is proven at runtime rather than asserted.

### 3.3 The gate reached without a model, and the frame on the wire

`POST /v1/tools/test-execute` with `shell_exec` returned **202**:

```
{"accepted":true,"run_id":"586d81ba","turn_id":"test-586d81ba",
 "tool":"shell_exec","marker":"openjarvis-test-exec-v1"}
```

With `probe_ws_bare_subscribe.py` already attached, the probe received:

```
[ws] #3   tool_confirm_request         agent_id=native_openhands
```

**This is the first time the gate's request event has ever been observed on the wire.**
Delivery to a bare, unfiltered WS client is proven. `agent_id=native_openhands` confirms
the frame came from the live chat agent's executor, which is what the design intended.

Backend `ws-accept` lines for this run, fresh peer ports 60805 and 54173, both
`authed=False bind_loopback=True agent_filter=None`. The v3 stamp is arriving.

### 3.4 Nothing was executed

The run parked on the gate and was allowed to reach its 120 s TTL. No confirm decision
was ever POSTed. `shell_exec` did not run. The deny-first ruling is satisfied in the
strongest possible form: not denied, never even offered.

---

## 4. NEGATIVE RESULTS - WHAT THINGS TURNED OUT NOT TO BE

Pinned per the 08/24 rule. A window that establishes what something is NOT has produced
knowledge, and these cost real cycles to establish.

### 4.1 THE PROBE'S SUMMARY IS DEFECTIVE. ITS SILENCE IS NOT A FINDING.

`probe_ws_bare_subscribe.py` received a `tool_confirm_request` frame at #3 and then
printed `NO CONFIRM EVENTS - EXPECTED, NOT A FAILURE` in its summary block. Those two
outputs contradict each other. The frame arrived; the summary denied it.

Therefore the collector at lines 174-175 is keyed on something that did not match the
string `tool_confirm_request`, and the same mismatch explains why the live line at 132
did not append `confirm_id=PRESENT/ABSENT` to frame #3.

**Consequence: `confirm_id` presence is UNMEASURED.** Not absent. Not redacted. Not
present. Unmeasured. Item 20 stays open. Do not let a future window read this handoff
and conclude the redaction was verified.

**Also: the probe's static text is now stale and actively misleading.** It prints
"there is no direct tool-execution route on this server" - that statement was true when
it was written and is false as of this window.

### 4.2 The probe is not a passive listener

Read at `probe_ws_bare_subscribe.py:106`: it starts `trigger_traffic()` on a daemon
thread unconditionally. There is no argparse and no flag to suppress it. So it fires its
own chat completion every run - which is the Defect 1 path we are deliberately routing
around - and the `inference_start` / `inference_end` frames it reports are its own noise,
not evidence about our trigger. It cannot be pointed at the test route as written.

### 4.3 A WebSocket is not a replay log

The first live run, `run_id=d16eeb21`, was lost. The 202 was fired BEFORE the probe
attached, so the `TOOL_CONFIRM_REQUEST` was broadcast to an audience of nobody. This was
a Claude sequencing error, corrected by the two-window procedure in section 5. Any future
measurement must attach the listener first. The frame is not retrievable after the fact.

### 4.4 The PID capture filter does not match the backend process

`Get-CimInstance Win32_Process -Filter "Name='python.exe'" | Where-Object CommandLine
-like '*openjarvis*serve*'` returned EMPTY while the backend was demonstrably up and
serving. So that filter is wrong - the real command line does not contain both tokens in
that arrangement. **The PID-with-CreationDate capture gap is now FOUR windows old and the
cause is finally localized: it is the filter, not the timing.**

What does work as a discriminator, proven this window:
`Get-NetTCPConnection -LocalPort 8010 -State Listen` correctly reported NO LISTENER when
the backend was down, and the owning PID and StartTime are reachable from it. Use that
shape next time instead of the CommandLine match.

### 4.5 The EXPECT_LEN mismatch was a Claude error, not a file anomaly

The script printed `LEN 93952 (expected 91395)`. Claude derived the expected value from
PowerShell's `$t.Length`, which counts decoded characters, while Python reports bytes.
93952 bytes is correct. The SHA matched exactly and the SHA is what gates the apply.
Length is informational. Fix the constant or drop it.

### 4.6 The unexplained ws-accept on port 64525

Appeared in backend output before the restart. Nothing we ran opened it. It is NOT
W19's stale 63212, so it is not the known artifact. Gray confirmed no reboot, so it is
plausibly scrollback from earlier in the same uptime. Recorded, not chased, not resolved.

### 4.7 Interpreter drift on the probe

Backend-window output showed the probe's UA as `websockets/15.0.1` in one run and
`websockets/17.0.1` in another. The probe resolves the system Python, not the venv.
Not chased. Flag it before it becomes a false negative in some later run.

---

## 5. THE MEASUREMENT PROCEDURE (reuse this verbatim)

Two PowerShell windows are required because the probe's built-in trigger cannot be
suppressed and a WS does not replay. This brushes the non-interactive rule, but the
reaction window is the gate's 120 s TTL, not seconds, so read-then-act fits comfortably.

WINDOW A, from `PS C:\Users\Admin\OpenJarvis>`, start first and leave running:

```
python .\probe_ws_bare_subscribe.py
```

WINDOW B, second PowerShell at the same path, as soon as A prints `[ws] CONNECTED`:

```
$body = '{"tool":"shell_exec","arguments":{"command":"echo openjarvis-testexec"}}'; $r = Invoke-WebRequest -Uri http://127.0.0.1:8010/v1/tools/test-execute -Method POST -ContentType 'application/json' -Body $body -UseBasicParsing; "STATUS $($r.StatusCode)"; $r.Content
```

Backend must have been started with the flag set in the SAME session, before launch:

```
$env:OPENJARVIS_TEST_EXEC = "1"; "FLAG=$($env:OPENJARVIS_TEST_EXEC)"; .\start-openjarvis.ps1
```

Success criterion: a `tool_confirm_request` frame in Window A carrying
`turn_id=test-<run_id>` matching Window B's response body, with `confirm_id=PRESENT`.
The `turn_id` is the discriminator - it cannot exist in any prior frame or log line.

---

## 6. ROLLBACK POINTS (added this window)

| File | Backup | Restore |
|---|---|---|
| `src\openjarvis\server\agent_manager_routes.py` | `...\agent_manager_routes.py.bak_testexec_20260829_165411` | `copy "C:\Users\Admin\OpenJarvis\src\openjarvis\server\agent_manager_routes.py.bak_testexec_20260829_165411" "C:\Users\Admin\OpenJarvis\src\openjarvis\server\agent_manager_routes.py"` |

Pre-patch SHA for verification after restore:
`94EC6F3F3351EB8F7FAFA09200FF5B393A1D92D4314430F50B273DF59AD00E1C`

The patch script is idempotent on its marker, so re-running it after a restore is safe.

---

## 7. GIT STATE - ACTION REQUIRED

**NOTHING FROM THIS WINDOW IS COMMITTED.** Uncommitted:

- `src\openjarvis\server\agent_manager_routes.py` (the route)
- `patch_testexec_v1.py` (copied into repo root - decide whether it belongs in the repo
  or in a scripts/ directory before committing)

**PUSH TO BOTH REMOTES.** `origin` is GitHub, `gitlab` is the lab instance. Every commit
goes to both, without being asked. Restating the trap because the naming invites it.

---

## 8. EXECUTION PATHS REGISTER

Standing structure. Carried forward and extended, not re-derived.

### PATH 3 (NEW THIS WINDOW): test-execute trigger

| Field | Value |
|---|---|
| Entry point | `POST /v1/tools/test-execute` |
| Router | `tools_router` in `server\agent_manager_routes.py`, inside `create_agent_manager_router()` |
| Call chain | route handler -> `asyncio.create_task(asyncio.to_thread(_run))` -> `_run` sets `CURRENT_TURN_ID` -> `executor.execute(ToolCall)` -> gate at `tools\_stubs.py:264-282` |
| Executor instance | `app.state.agent._executor` - the LIVE chat agent's, constructed at `agents\_stubs.py:325`. Constructs nothing of its own. |
| Confirmation gate | **LIVE.** Not auto-approved, not absent. Proven: 202 then a `tool_confirm_request` on the wire, then TTL expiry with nothing executed. |
| Event bus traffic | `TOOL_CONFIRM_REQUEST` on serve.py's EventBus, reaching WS via the bridge fix. `agent_id=native_openhands`. `turn_id=test-<run_id>`. |
| Human present | Yes by construction - the run cannot proceed without a POST to `/v1/tools/confirm`. |
| Guard | env + loopback + tool-on-agent + `requires_confirmation=True`. Cannot execute a non-confirming tool. |

Previously registered: PATH 1 orchestrator `ask()` via `system\orchestrator.py`;
PATH 2 managed-agent SSE via `_stream_managed_agent()` in `server\agent_manager_routes.py`
(carries the four auto-approve sites, item 6); plus the routes.py chat dispatch branches
1a/1b/1c/1d.

---

## 9. SDP / SDD FEED

Gray is building a System Design Document covering all OpenJarvis work to date. Every
handoff carries this section. What W20 owes the SDP:

**Architecture.** The confirmation gate now has a documented, guarded, non-model entry
path. Chapter on the gate should present three entry paths (orchestrator, managed-agent
SSE, test-execute) and state for each whether the gate is live, auto-approved, or absent.
That table is now fillable for the first time.

**Decisions and the evidence behind them.** Record the test-only ruling with the two
rejected alternatives and the reason each was rejected - the managed-agent route's
auto-approve sites and the model route's Defect 1 dependency. Record the ContextVar
discriminator decision and, importantly, that it replaced a worse proposal that would
have required editing the verified gate file. That is an example of the design process
working and belongs in the narrative, not just the outcome.

**Defect 6 confirmation gate - Gray flagged this for GREAT DETAIL.** W20 supplies:
- registry: write-once contract, 409 on re-decision, TIMEOUT settable only internally
- payload: seven fields, `turn_id` sourced from the `CURRENT_TURN_ID` ContextVar
- transport: EventBus -> ws_bridge -> bare WS client, DELIVERY NOW PROVEN, redaction of
  `confirm_id` STILL UNMEASURED
- threading model: gate blocks a worker thread up to the 120 s TTL; callers must use
  `asyncio.to_thread` to avoid parking the event loop; note the pool-starvation
  constraint that follows

**Hazards found.** `ToolCall.arguments` is a JSON string, a shape trap. Instruments can
report false negatives - section 4.1 is a case study and should appear in the SDD's
verification-methodology chapter as the reason every probe needs its own positive
control. WS frames are not replayable, so listener-before-trigger is a hard ordering
constraint for any event-bus measurement.

---

## 10. 550B CLOUD MODEL

Carried forward per the 08/29 pin. When a question needs whole files rather than targeted
reads, bundle the suspected files into a single markdown file for Gray's 550B cloud model
(openrouter nemotron-3-ultra-550b) rather than spending window cycles on piecemeal reads.

**Candidate for the next window if the probe fix is not a one-liner:**
`probe_ws_bare_subscribe.py` is small and self-contained. If the collector condition at
lines 120-180 does not explain the contradiction in section 4.1 on sight, bundle the
whole probe plus `server\ws_bridge.py` and send it out rather than reading around it.

---

## 11. NEXT ACTIONS, ORDERED

1. **Read the probe's confirm-frame collector.** Lines roughly 120-180 of
   `probe_ws_bare_subscribe.py`. Find why a frame typed `tool_confirm_request` did not
   satisfy the condition that appends `confirm_id=` and did not land in the summary
   collector. One read; do not patch before reading.
2. **Fix the probe, verify in isolation.** Do not bundle any other change with it.
3. **Re-run section 5's two-window procedure.** Obtain `confirm_id=PRESENT` or
   `ABSENT - REDACTED`. This closes item 20, which is the last blocker on the v3
   redaction question.
4. **Commit and push to BOTH remotes.**
5. Optional, cheap, do not let it displace 1-3: add a `--no-trigger` flag to the probe so
   the measurement collapses to one window; and fix the PID capture using the
   `Get-NetTCPConnection -LocalPort 8010` shape from section 4.4.

---

## 12. STANDING RULES IN FORCE

- ALWAYS VERIFY. Never stack a second change on an unverified first one.
- FINISH THE THING BEFORE STARTING THE NEXT. No dangling processes.
- State shell and host on every command. Default PowerShell on the Windows box; anything
  for the Ubuntu ollama host (172.16.33.200) must be labeled or PowerShell-wrapped ssh.
- Commands must run from `PS C:\Users\Admin\OpenJarvis>` as pasted. If a command needs a
  different path, say so IN THE REQUEST, before it runs.
- No non-ASCII symbols in replies.
- Tests must be non-interactive wherever possible.
- Pin the detail of every window including negative results.
- Push to both remotes, always.
- Token conservation on working sessions.
