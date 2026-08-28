# SDP ARTIFACT - WEBSOCKET EVENT CHANNEL

## `/v1/agents/events` - inputs, outputs, and service communications

Document owner: Graystone Lab / OpenJarvis SDD, transport chapter.
Artifact date: 2026-08-26. Source window: W12 continuation (W13, W14).
REVISION C, 2026-08-28, post-W14: sections 3.2, 3.3, 5, 6, 7, 8, 9 and 10
amended after the redaction was WIDENED to cover both confirm frame types,
verified both ways a second time, and committed. Revision B described a
half-implemented posture; that is no longer the state.
Marker of the change described here: `openjarvis-ws-cid-redact-v2` on the
forward-loop block. The accept-site block deliberately remains at v1 because it
did not change - the v1 marker is NOT unique in that file and any control
asserting that it greps back exactly once would be wrong.
Commit of record: `4c365c1` on `main`, pushed to both remotes.
Predecessor commit: `6c132d6` (the v1 redaction and the confirm registry).

STATUS CHANGE IN THIS REVISION: posture C is FULLY implemented for this
transport. Both `TOOL_CONFIRM_REQUEST` and `TOOL_CONFIRM_RESOLVED` are redacted
for unauthenticated subscribers, proven in both directions on a post-reboot
build. Revision B open item 1 is CLOSED. Revision B open item 4 is CLOSED and
its finding OVERTURNED. Revision B open item 5 is CORRECTED on evidence, not
closed.

Every fact in sections 1 through 6 is labeled VERIFIED or UNVERIFIED. Nothing is
carried as fact on inference alone. Section 8 lists what is still open.

---

## 1. GATE SUMMARY - PORTS, PROTOCOLS, ENCODING

| Property | Value | Status |
|---|---|---|
| Bind address | `127.0.0.1` | VERIFIED |
| Port | `8010` | VERIFIED |
| Route | `/v1/agents/events` | VERIFIED |
| Transport | WebSocket over HTTP/1.1 `Upgrade` | VERIFIED |
| Server | uvicorn `0.41.0` | VERIFIED 08/26 |
| WS backend library | `websockets 15.0.1` | VERIFIED 08/26 |
| Alternative WS backend | `wsproto` NOT installed, NOT required | VERIFIED 08/26 |
| Frame type | Text | VERIFIED |
| Payload encoding | UTF-8 JSON via `websocket.send_json` | VERIFIED |
| Authentication | Query-string `token`, compared to env `OPENJARVIS_WS_TOKEN` | VERIFIED 08/26 |
| Authorization model | Accept is unconditional; auth controls FIELD VISIBILITY only | VERIFIED |
| Source module | `src\openjarvis\server\ws_bridge.py` | VERIFIED |
| Router factory | `create_ws_router(event_bus)` | VERIFIED |
| Mount site | `src\openjarvis\server\api_routes.py:944` | VERIFIED |

Companion HTTP gate, same host and port, used to answer a confirmation:

| Property | Value | Status |
|---|---|---|
| Route | `POST /v1/tools/confirm` | VERIFIED |
| Content type | `application/json` | VERIFIED |
| Request body | `{confirm_id, decision}` | VERIFIED |
| Accepted `decision` values | `approve`, `approved`, `deny`, `denied` | VERIFIED |
| Status codes | 200 first resolve, 400 missing/bad, 404 unknown or expired, 409 already resolved | VERIFIED |
| Hosted on | `tools_router`, prefix `/v1/tools`, defined inside `create_agent_manager_router()` | VERIFIED |

NOTE ON THE REGISTRY CONTRACT, an asymmetry worth carrying: the ROUTE accepts
all four decision spellings and normalizes. `confirm_registry.resolve()` itself
accepts ONLY the full words `approved` and `denied` and raises `ValueError` on
`approve` or `deny`. Any non-route caller must pass the full words.

---

## 2. INPUTS - WHAT A CLIENT SENDS

### 2.1 Connection request

```
GET /v1/agents/events?agent_id=<optional>&token=<optional> HTTP/1.1
Host: 127.0.0.1:8010
Upgrade: websocket
Connection: Upgrade
```

Query parameters, both optional:

- `agent_id` - filter. When present, the client receives only events whose
  payload `agent_id` matches. When absent, the client receives all events.
  Stored on the socket as `_agent_filter`.
- `token` - authentication. Compared at accept against env
  `OPENJARVIS_WS_TOKEN`. Result stored on the socket as `_ws_authed`.

DESIGN CONSEQUENCE, RECORD IT: a client that supplies `agent_id` gets a filtered
stream. The chat-path agent is constructed without an explicit `agent_id`, so a
filtered client can silently receive nothing. Any consumer built for the
confirmation gate must connect UNFILTERED.

### 2.2 Client-to-server frames

None. The channel is server-push only. A client answers a confirmation over the
separate HTTP route in section 1, not over the socket.

---

## 3. OUTPUTS - WHAT THE SERVER SENDS

A single `_on_event` handler is subscribed to 13 event types. Two are
load-bearing for the confirmation gate.

### 3.1 `TOOL_CONFIRM_REQUEST`

Emitted at the confirmation gate in `src\openjarvis\tools\_stubs.py` when a tool
whose spec carries `requires_confirmation=True` is dispatched on an interactive
executor.

Seven fields, VERIFIED present and complete by in-process probe and by live
frame capture:

| Field | Meaning |
|---|---|
| `confirm_id` | The key. Presented to `POST /v1/tools/confirm` to resolve. |
| `agent_id` | Read from `self._agent_id` on the executor. Inside `data`. |
| `turn_id` | From the `CURRENT_TURN_ID` ContextVar. Format `a8172e4c-t1`. |
| `tool` | Tool name. |
| `args_digest` | Bounded argument digest, 400-char cap. |
| `prompt` | Human-readable prompt, built FROM the digest, not from the raw params dict. |
| `expires_at` | Absolute expiry. Default TTL 120.0 s. |

`agent_id` is INSIDE `data` and not an attribute of the `Event` object. This is
structural, not stylistic: `Event` is `@dataclass(slots=True)` with exactly
`event_type`, `timestamp`, `data`, so an attribute assignment would raise.

`args_digest` and `prompt` are both bounded deliberately. The pre-patch prompt
interpolated the full params dict unbounded, which is the same failure class as
the model-side payload-size blocker on the mailbox path.

### 3.2 `TOOL_CONFIRM_RESOLVED`

Fields observed on live capture: `confirm_id`, `agent_id`, `turn_id`, `tool`,
`decision`, `state`, `created_at`, `expires_at`.

THIS FRAME IS NOW REDACTED for unauthenticated subscribers, as of the
`openjarvis-ws-cid-redact-v2` change (commit `4c365c1`). An authenticated
subscriber receives `confirm_id`; an unauthenticated one receives every other
field intact and no `confirm_id`. Section 6.5 records the proof in both
directions. Revision B's "still carries it unredacted" framing is obsolete and
should not be quoted from older copies of this artifact.

ORDERING FINDING, 08/26, and it changes the severity of that open item: the
resolved frame is broadcast BEFORE the tool runs, not after. Measured on one
approved cycle - `tool_confirm_resolved` at 07:30:03.388, `tool_call_start` at
07:30:03.392, a 4 ms gap. Revision A deferred this leak on the reasoning that a
resolved cid is spent. That reasoning covers replay, and replay is genuinely
blocked (409, verified against a real out-of-band resolver). It does NOT cover
disclosure: an unauthenticated local subscriber learns a valid cid, its tool, its
turn_id and the fact of approval at the instant execution begins. Under posture C
- the cid never reaches an unauthenticated subscriber at all - that is unfinished
business, not accepted risk.

### 3.3 Redaction rule (the `openjarvis-ws-cid-redact-v2` behavior)

For BOTH `TOOL_CONFIRM_REQUEST` and `TOOL_CONFIRM_RESOLVED`:

- Socket has `_ws_authed == True` -> receives the full seven-field payload.
- Socket has `_ws_authed` false or absent -> receives a PER-CLIENT COPY with
  `confirm_id` popped. `tool`, `args_digest` and `prompt` are untouched.
- A redaction emits a `logger.warning` naming BOTH the frame type and the
  peer. The frame type is passed as a parameter rather than hardcoded, so the
  log discriminates which frame was redacted for which subscriber. Before v2 the
  string hardcoded `TOOL_CONFIRM_REQUEST`; widening the predicate without this
  would have written a false statement into the audit log on every resolved-frame
  redaction, in the same class as the fail-quiet hazards section 7.4 tracks.
- The shared payload dict is NEVER mutated. The copy is per client, so one
  unauthenticated subscriber cannot degrade what an authenticated one receives.

FAIL-CLOSED BY CONSTRUCTION: if `OPENJARVIS_WS_TOKEN` is unset or empty, no
socket can authenticate, so no socket receives a live `confirm_id`. This is the
deliberate inverse of the defaults-fail-open pattern documented as a
cross-cutting hazard class in this codebase.

CONSEQUENCE OF FAIL-CLOSED, stated so it is not later mistaken for a defect: a
gated tool sits its full 120 s TTL and reaps unless a token-holding client
answers. This breaks nothing that currently works, because no shipped frontend
code POSTs to `/v1/tools/confirm` today.

VERIFIED BOTH WAYS, BOTH FRAME TYPES. The rule above is not a description of
intent. Section 6.2 records the request-frame pair; section 6.5 records the
resolved-frame pair on the v2 build, unauthenticated and authenticated, against
the same server. Section 6.3 records the forward loop read at source. Behavior,
implementation and this document agree.

SCOPE CORRECTION WORTH PINNING: revision B scoped this change as one line at
`ws_bridge.py:51`. It is four edits. The predicate at 51 is consumed at 58, and
the warning text at 64-65 hardcoded the frame type. A scope estimate carried in
a handoff is an estimate; re-derive it from source before patching.

---

## 4. SERVICE COMMUNICATIONS - THE FULL PATH

```
  tool dispatch (worker thread)
        |
        |  ToolExecutor gate, tools\_stubs.py
        |  requires_confirmation=True
        v
  confirm_registry.register()  -> confirm_id
        |
        |  bus.publish(EventType.TOOL_CONFIRM_REQUEST, {seven fields})
        v
  EventBus  (app.state.bus)
        |
        |  ws_bridge._on_event, subscribed to 13 event types
        v
  per-client fan-out
        |
        |  asyncio.Queue(maxsize=100) per client
        |  loop.call_soon_threadsafe  <-- THREAD BOUNDARY CROSSING
        |  per-client redaction keyed on _ws_authed
        v
  WebSocket text frame, UTF-8 JSON, 127.0.0.1:8010 /v1/agents/events
        |
        v
  client reads confirm_id  (only if authed)
        |
        |  POST /v1/tools/confirm  {confirm_id, decision}   HTTP/1.1 JSON
        v
  confirm_registry.resolve()  -> releases the blocked worker thread
        |
        v
  ToolExecutor builds one of three DISTINCT ToolResults:
    approved / denied / timeout
```

### 4.1 Bus topology - why this leg exists at all

There are exactly two `EventBus` instances in the running system.

- BUS A, the agent's: constructed at `cli\serve.py:132` as
  `EventBus(record_history=False)`, handed to the agent and into `create_app`,
  which sets `app.state.bus` at `server\app.py:215`.
- BUS B, the lazy singleton: `get_event_bus()` in `core\events.py`.

The WS bridge originally subscribed to BUS B while the gate emitted on BUS A, so
the browser-facing channel was structurally dark regardless of gate correctness.
Fixed by `openjarvis-ws-bus-v1` at `api_routes.py:944`, which now reads
`getattr(app.state, "bus", None) or get_event_bus()`. Ordering was proven before
applying: `app.py:215` runs before `app.py:295 include_all_routes(app)`, so the
getattr cannot return `None` on the serve path. Had the order been reversed the
patch would have silently fallen through to the singleton and LOOKED fixed,
inside a bare `except` that only logs at debug level.

### 4.2 Threading model

The event is raised on the tool worker thread. The socket lives on the event
loop. `loop.call_soon_threadsafe` is the crossing. The worker thread BLOCKS in
`confirm_registry.wait(cid)` for the duration.

`asyncio.to_thread` uses the loop's DEFAULT ThreadPoolExecutor, shared with
speech transcription and webhooks. A blocked confirmation therefore occupies a
slot in a pool that other subsystems draw from. This is why the TTL is capped at
120 s and why `interactive` is opt-in per run rather than a blanket default.

RE-REQUEST AMPLIFICATION, carry this into capacity planning: the agent
RE-REQUESTS confirmation on the next turn after a TIMEOUT ToolResult, with a new
`confirm_id` and an incremented turn suffix. An unanswered confirmation costs
N x 120 s of shared-pool occupancy, not 120 s once.

---

## 5. OBSERVED TIMINGS - LIVE, NOT SYNTHETIC

| Measurement | Value | Discriminates |
|---|---|---|
| Emit to frame arrival at client | 10 ms after `inference_end` | Frame is not TTL-driven |
| Approve POST round trip | 186 ms (also 49 ms and 121 ms on a two-gate turn) | Route is live |
| Emit to `tool_call_start` | 287 ms | Resolve released the worker, it did not time out |
| Resolved frame after approve | ~170 ms | Resolved frame is published, not merely defined |
| Full two-gate sequence in one turn | ~410 ms against a 120 s TTL | Multi-cycle works |
| Unanswered confirmation | 120.004 s, then reap | TTL is 120.0 s as configured |
| Unanswered confirmation, second measurement | 120.027 s, then reap | Matches `confirm_registry.default_ttl = 120.0` on an independent run |
| Approve POST round trip, authed run | 200 in 115 ms | Route is live for a token-holding client |
| Emit to `tool_call_start`, authed run | 143 ms against a 120 s TTL | Resolve released the worker on the redacted-channel build |
| `tool_call_end` latency, authed run | 0.094 s, real stdout, exit 0 | The approved path executes the tool, it does not merely skip the gate |
| Replay of a spent cid by an out-of-band resolver | 409 in 16 ms | Write-once holds against a real adversary, not just a probe |
| `tool_confirm_resolved` to `tool_call_start` | 4 ms, resolved frame FIRST | Disclosure window opens before execution - see section 3.2 |
| Unanswered confirmation, third measurement | 120.013 s (emit 09:16:12.2346845, reap 09:18:12.24768) | Third independent run consistent with 120.004 and 120.027 - the TTL is stable, not coincidental |
| Reap to re-request | 1.6 s (t1 reaped 09:18:12.247, t2 issued 09:18:13.833) | One user request consumes TWO 120 s worker slots on the shared pool, not one |
| Total user-visible time, unanswered gate | 245.8 s, ending in an apology | The cost of open item 2a stated in wall-clock time rather than as a design note |

METHOD NOTE, and it is the reason these numbers are recorded rather than just
the pass results: an elapsed time UNDER the TTL is what separates "resolve
released the worker" from "it timed out and happened to look correct." A
lower-bound-only assertion cannot make that distinction. Every acceptance test
in this package should name what a passing result RULES OUT.

---

## 6. VERIFICATION RECORD - 2026-08-26

### 6.1 Part one - the channel

Instrument: `System.Net.WebSockets.ClientWebSocket` from PowerShell 5.1 on the
Windows box. Read-only, non-interactive, runs to completion without operator
timing.

| Run | Input | Result | Log line |
|---|---|---|---|
| Control | Venv package listing, `uvicorn` as positive control | `uvicorn 0.41.0` and `websockets 15.0.1` both present | n/a |
| A | Connect, no `token` | `STATE: Open` | `06:57:44,799 ws-accept: peer=127.0.0.1:62390 authed=False agent_filter=None ua=None` |
| B | Connect with `token=<session token>` | `STATE: Open` | `07:00:03,261 ws-accept: peer=127.0.0.1:64453 authed=True agent_filter=None ua=None` |

A and B differ in exactly one variable. A is the control for B. Together they
prove: the WS upgrade succeeds; `websockets` is present and functional in the
running process; the accept-time log fires; the token reaches the backend
environment; and the comparison distinguishes a correct token from no token.

### 6.2 Part two - the redaction, proven both ways

METHOD, and it is the part worth carrying: no new harness was written. The repo
root already held `watch_confirm_auto.ps1` (08/22), which subscribes
UNAUTHENTICATED, scrapes a `confirm_id` off the broadcast by regex, and POSTs it
to resolve the gate. That script IS the D-SEC-1 finding, running. It is not a
hypothetical local process; it is a real one already on the box. So part two ran
the known-working exploit against the patched server, where a PASS means the
exploit STOPS working.

This removes the ambiguity of a null capture. The question is not "did a frame
arrive" but "did a known-working exploit stop working."

| | Run 1, no token | Run 2, token |
|---|---|---|
| `tool_confirm_request` carries `confirm_id` | NO, on both frames | YES |
| Fields `tool`, `args_digest`, `prompt`, `agent_id`, `turn_id`, `expires_at` | All present | All present |
| Resolve attempt | 409, cid already spent | 200 in 115 ms |
| Tool executed | No - reaped at 120.027 s | Yes - 143 ms after emit |

Neither run alone proves the redaction. The pair does.

THE ACCIDENTAL POSITIVE CONTROL - the load-bearing part. On the same socket, in
the same unauthenticated run, a `tool_confirm_resolved` frame arrived WITH its
`confirm_id` plainly visible, and the same regex fired on it. That simultaneously
kills "the matcher was broken" and "no frame arrived" as explanations for the
absence on the request frames. One frame type redacted and one not, same second,
same client, same regex, is a self-validating instrument. It was not designed,
and it is better evidence than the test that was. DESIGN FOR THIS DELIBERATELY
where an unredacted sibling frame exists.

TEST-HYGIENE FINDING that cost one run: the first authenticated attempt produced
NO confirm frame at all. The model called `think`, told itself it could not run
shell commands "due to security restrictions", and answered from that. The thread
already carried three of its own prose refusals from the run-1 provocations. This
is the known Defect 1 trigger - once prior assistant prose claiming a limitation
is in context, the model answers from its prose instead of dispatching. The
"security restrictions" line is confabulation; no such restriction exists. The
gate parks and reaps invisibly, which is what the user actually experienced.
RULE FOR THIS PACKAGE: every gate test runs in a genuinely fresh thread. Verify
by `message_count`, not by prompt-token count, which looked fresh when it was not.

LAUNCH CONTEXT for anyone reproducing: a bare `.\watch_confirm_auto.ps1` fails
with `PSSecurityException` in a fresh window because the file is unsigned. Prefix
`Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process -Force;`. Process
scope needs no admin rights, does not touch CurrentUser or LocalMachine, and
reverts when the window closes.

### 6.3 Source read - implementation confirmed, not just behavior

Everything above is behavioral. The forward loop in
`src\openjarvis\server\ws_bridge.py` was then read directly, because a patch
description standing in for an observation is exactly what produced the
`websockets` ghost in section 7.1.

| Line | Fact | Why it matters |
|---|---|---|
| 32-33 | Both `TOOL_CONFIRM_REQUEST` and `TOOL_CONFIRM_RESOLVED` are in the subscribed set | Confirms the resolved frame is in scope of this transport, hence open item 1 |
| 51 | `_is_confirm_request = event.event_type is EventType.TOOL_CONFIRM_REQUEST` | Identity comparison on the enum member, computed ONCE outside the client loop, scoped to one event type |
| 52 | `for ws, (queue, loop) in list(clients.items())` | Iterates a snapshot, so the client dict can mutate during fan-out |
| 57-58 | `client_payload = payload` first, then branch on `_is_confirm_request and not getattr(ws, "_ws_authed", False)` | The `getattr` default of `False` IS the fail-closed mechanism - a socket that never reached accept, or where the assignment failed, reads unauthenticated. It cannot fail open |
| 59-61 | `_data = dict(payload["data"])` then `client_payload = dict(payload, data=_data)` | Two fresh dicts. The shared payload is genuinely never mutated and the copy is genuinely per client, so an authed and an unauthed subscriber on one emit cannot interfere |
| 60 | `_had_cid = _data.pop("confirm_id", None) is not None` | The warning is gated on the key having actually been present, so it cannot fire spuriously - and the guard makes widening line 51 to cover both confirm types safe on a frame with no cid |
| 89 | `websocket._ws_authed = _authed` set at accept | The attribute read at 58 is set exactly once, at the only accept site |

Implementation matches behavior matches this document. Closed.

### 6.4 Reproduction reference

Log location and format for anyone reproducing this:
`C:\Users\Admin\AppData\Local\OpenJarvis\logs\backend.log`, format
`YYYY-MM-DD HH:MM:SS,mmm LEVEL logger.name: message`. Rotation `.1` through
`.5` in place. `uvicorn.access` is a known-present positive control for reads
against this file. The startup banner `Starting OpenJarvis API server` is NOT -
it goes to the console only.

### 6.5 Part three - the v2 widening, both frame types, post-reboot

Ran 2026-08-26 after the predicate was widened to cover `TOOL_CONFIRM_RESOLVED`.
Same instruments as 6.2, same server, opposite expected result on one frame.

PRECONDITION, and it nearly invalidated the run: the box REBOOTED at 08:47:25,
between the patch write (08:33:55) and the verification. Before any behavioral
claim was made, both python process creation times were read at 08:52:53 -
19 minutes AFTER the patch and 5 minutes after boot. The running server therefore
serves post-patch code. Command lines were deliberately NOT printed; they can
carry secrets and creation time answers the question alone. THIS CHECK IS NOW A
PREREQUISITE for any behavioral claim following a patch, not an optional step.

| | Unauthenticated (peer 56454) | Authenticated (peer 58294) |
|---|---|---|
| `tool_confirm_request` carries `confirm_id` | NO, on both t1 and t2 | YES, `0e5e7140...` |
| `tool_confirm_resolved` carries `confirm_id` | NO - the v2 change, proven | YES, the same cid |
| `ws-cid-redact` lines naming this peer | 3, both frame types named | none |

The unauthenticated resolved frame printed UNTRUNCATED in the capture with
`agent_id`, `turn_id`, `tool`, `decision:"timeout"`, `state:"resolved"`,
`created_at`, `expires_at` and `reaped:false` - and no `confirm_id`. In the 6.2
run that same frame type, on that same script, carried its cid in the clear.
Same harness, same regex, same server, opposite result.

The authenticated half is not a formality. Over-redaction was the plausible
regression from widening a predicate, and it is the only thing that
distinguishes a working redaction from a broken one.

HONEST LIMIT, stated because it is a real weakening of the evidence: this run
has NO in-run positive control. The 6.2 run got one for free precisely BECAUSE
the resolved frame was unredacted - the regex firing on it proved the instrument
live. The v2 change removes that. The regex is proven by the earlier run against
the same build, not by this one. Acceptable only because the before-picture is
the same script on the same server. Any future window wanting an in-run control
must use a third frame type that legitimately carries an id-like field.

METHODOLOGICAL CONSEQUENCE, and it generalizes past this transport: THE
STRONGEST AVAILABLE VERIFICATION MAY DESTROY THE CONTROL THAT MADE THE PREVIOUS
ONE STRONG. A hardening change can reduce future observability. That cost should
be named at design time, not discovered afterward.

---

## 7. NEGATIVE RESULTS - PIN THESE

A window that changed nothing still produced knowledge. These are recorded so
they are not rediscovered.

### 7.1 The missing-`websockets` blocker did not exist

W12 recorded verification as BLOCKED on a suspected missing `websockets`
package, on the evidence that zero `ws-accept:` lines had ever appeared. That
absence proved nothing. `ws-accept:` was a log line created BY the patch under
test, and no subscriber had connected since the patch was applied. Zero
subscribers produces zero accept lines on a completely healthy path.

The package was present the whole time. A manual install was not needed, and the
proposed durable fix to `start-openjarvis.ps1`'s dependency set would have been
work against a non-problem.

RULE: an instrument that has never produced a positive reading cannot have its
silence read as a finding. Establish the positive reading first.

### 7.2 The `ua=` attribution field is dead ONLY FROM POWERSHELL - OVERTURNED

`$ws.Options.SetRequestHeader("User-Agent", ...)` THROWS on the .NET Framework
`ClientWebSocket` under PowerShell 5.1 - that header is property-controlled and
is not settable through that method. The exception is non-terminating, so the
connect still succeeds and the operator sees `STATE: Open` next to a red error
block. Both accept lines above show `ua=None` as a result.

OVERTURNED 2026-08-26. The limitation is specific to the .NET Framework
`ClientWebSocket` under PowerShell 5.1. It is NOT a property of the field and
NOT a server-side defect. A client that sets the header was already sitting in
the repo root: `probe_confirm_frames.py` produced
`ua='Python/3.12 websockets/17.0.1'` on the authenticated accept for peer 58294.

CONSEQUENCE, corrected: KEEP THE FIELD. Revision B recommended removing it as a
permanently-null column; that recommendation is withdrawn. Subscriber
attribution no longer rests on timestamp correlation alone - use a Python client
for any test where attribution matters, and expect `ua=None` from a PowerShell
one.

NOTED, NOT A CONTRADICTION: that string reports `websockets/17.0.1` while the
venv holds 15.0.1. Different interpreters - the probe ran on system Python 3.12,
the server on the venv. Worth confirming once if any future test depends on
client library behavior rather than protocol behavior.

LESSON FOR THIS PACKAGE: a capability was recorded as ABSENT when what was
actually established was that ONE CLIENT could not exercise it. Before a field,
route or feature is written down as dead, name the instrument that failed to
reach it and ask whether a different instrument would.

### 7.3 `wsproto` was never a dependency of this project

It entered the search because it is an alternative uvicorn WS backend, not
because it was found anywhere in the tree or the venv. uvicorn requires one WS
backend and has one.

### 7.4 The fail-quiet pattern - a cross-cutting hazard class, five instances

This belongs in the SDD as one named theme, not four separate bugs.

1. `_confirm_callback = None` accepted silently, leaving the gate absent rather
   than erroring.
2. A missing WS backend causes `/v1/agents/events` to fall through to the SPA
   catch-all and return `index.html` with HTTP 200 rather than failing.
3. The per-client queue swallows overflow: `except (RuntimeError,
   asyncio.QueueFull): pass`. A slow client loses frames with NO log line.
4. A bad `account` id on the mailbox path returned a silent zero instead of an
   error, and a correct-sounding caveat then explained the wrong number
   confidently.
5. The four auto-approve executor sites approve every gated tool unconditionally
   and log nothing when they do. The gate appears present and is not.

Instance 3 is inside the transport described by this document and is an open
hazard. See section 8.

### 7.5 The ghost-chasing pattern - a second named class, three instances

Same root as 7.4, inverted: a DESCRIPTION or an ABSENCE treated as an
OBSERVATION.

1. A retracted "broken folder quoting" defect that was never observed.
2. Three windows planned around a patch script that had already been applied.
3. The missing-`websockets` blocker of section 7.1.

COUNTERMEASURE, and it is the rule that opened this window: verify that the
component exists and that the instrument can produce a positive reading, before
interpreting its silence.

### 7.6 The `_stubs.py` EOL baseline contradicts the record - UNRESOLVED

EOL byte-count of the working copy, taken immediately after the commit:

| File | CRLF | bare LF |
|---|---|---|
| `tools\_stubs.py` | 547 | 0 |
| `cli\serve.py` | 605 | 22 |
| `server\ws_bridge.py` | 113 | 0 |

`_stubs.py` is now a PURE CRLF file. The record since 08/20 says it holds 2 CRLF
lines in an otherwise LF file, and every patch script written against it used
that shape - the split-on-`\n` round-trip proof and the "assert CRLF count
unchanged" control both rest on it. THAT PREMISE IS FALSE AS OF NOW.

Two candidate explanations, NOT discriminated: the file was converted since 08/20
by a patch script, an editor, or git; or the original finding was wrong in the
same way section 7.1 was wrong. `serve.py` at 605/22 DOES match the record, so
the measuring instrument is sound, which makes the `_stubs.py` figure a real
change rather than a measurement error.

ACTION FOR THE NEXT PATCH TO `_stubs.py`: re-measure, do not inherit. Git has
also warned it will normalize CRLF to LF the next time it touches these files, so
the baseline will move again. A future window must not read a failed EOL
assertion as file corruption.

---

## 8. OPEN ITEMS

1. **CLOSED by section 6.5.** `TOOL_CONFIRM_RESOLVED` is redacted for
   unauthenticated subscribers as of `openjarvis-ws-cid-redact-v2`, commit
   `4c365c1`. Verified in both directions on a confirmed post-patch build. The
   fix was four edits, not the one line revision B scoped. Retained as a numbered
   item so references to "open item 1" from earlier documents resolve correctly.
2. **CLOSED by section 6.** Part two of verification is complete. An
   unauthenticated subscriber received `TOOL_CONFIRM_REQUEST` without
   `confirm_id` and with `tool`, `args_digest` and `prompt` intact; an
   authenticated subscriber received the full frame and resolved it; the
   implementation was confirmed at source. Retained here as a numbered item so
   references to "open item 2" from earlier documents resolve correctly.
2a. **NO USER CAN ANSWER A GATE.** Not an open item of this transport, but the
   item this transport now blocks on. The only reason a gated tool has ever
   executed is that a PowerShell script stood in for a UI that does not exist. In
   the unauthenticated run the model asked permission in prose, the operator said
   yes, and it apologized and gave up - twice. Two gates fired, both parked a
   worker 120 s on the shared pool, and the user-visible result was an assistant
   that looks broken. This is the gating item for the feature being USABLE rather
   than merely CORRECT. Consumer already exists at
   `frontend\src\lib\useAgentEvents.ts`, pointing at `/v1/agents/events` at
   line 19; it must mount with NO `agent_id` param and carry a token, which makes
   open item 5 a prerequisite.
3. **Silent frame drop on queue overflow** (7.4 instance 3) has no instrument. A
   slow client cannot currently tell it missed a frame.
4. **CLOSED and OVERTURNED.** The `ua=` field works. See section 7.2. The
   removal recommendation is withdrawn; use a Python client where attribution
   matters. Retained as a numbered item for reference resolution.
5. **Token persistence - CORRECTED, NOT CLOSED.** Revision B stated that the
   token is session-scoped and does not survive a reboot, so any fresh start
   comes up fail-closed. THAT IS FALSE AS STATED. A genuine reboot occurred at
   08:47:25 on 08/26 and the token survived it: `authed=True` at 09:00:21.
   Discriminated rather than assumed - a deliberately WRONG token returned
   `authed=False` at 09:06:58, which is the load-bearing control, because without
   it "it authenticates" cannot be separated from "the auth check is broken."
   The source was then hunted and NOT found: `OPENJARVIS_WS_TOKEN` is unset at
   Process, User and Machine scope; absent from `start-openjarvis.ps1`; absent
   from `.env`; absent from every repo-root `.ps1`. Remaining candidates are the
   launching shell and the desktop app's spawn chain. THE TRUE STATEMENT IS
   NARROWER AND STILL A REAL GAP: the token has no durable, discoverable home,
   so whether a fresh start comes up authenticated depends on how it was
   launched, and nobody can currently explain why it worked. Open item 2a cannot
   depend on an unlocated secret. No secret goes into `.env` while that
   file is in its current state: 45 lines, only 11 valid `KEY=value`, the
   remainder a credential scratchpad that python-dotenv silently skips. Standing
   rule: never generate a command that echoes any line content from that file.
   Line numbers and a boolean parse result only.
6. **Destructive mailbox tools are ungated at the spec level.** Only
   `agent_tools.py`, `git_tool.py` and `shell_exec.py` declare
   `requires_confirmation=True`. `mailbox_move_to_trash` and
   `mailbox_empty_folder` do NOT, so no amount of confirmation-gate wiring
   reaches them. This is a gap in the gate's COVERAGE, not in its mechanism, and
   it belongs in the security chapter alongside the transport work.
7. **Four auto-approve sites remain live** in `server\agent_manager_routes.py`
   (lines 720-721, 1202-1206, 1562-1563, 1639-1640), each passing
   `confirm_callback=lambda _prompt: True`. Three are DeepResearchAgent-only. The
   fourth builds an ad-hoc per-tool executor and calls `execute()` directly,
   bypassing the agent, on the managed-agent SSE stream. Its rationale is stated
   as deliberate - wizard-added tools treated as pre-approved. That argument must
   be explicitly accepted or overturned, not left implicit.
8. **`"reaped": false` on a timeout resolution.** The resolved frame carries a
   `reaped` field that the section 3.2 frame contract does not list, and it reads
   `false` on a resolution whose `decision` is `timeout`. Observed on both the
   unauthenticated (09:18:12.250) and authenticated (09:25:45.263) runs. Either
   the field name is misleading or the flag is set at a later stage than the
   emit. Read `confirm_registry._snapshot()` before the frame contract in this
   document is treated as complete.

---

## 9. SECURITY POSTURE - D-SEC-1

FINDING: the resolver set for a pending tool confirmation was "any local
socket." Any process on the box could subscribe, read a `confirm_id` from a
broadcast frame, and POST it. The gate was advisory against local processes, not
an interlock.

Three postures were considered:

- **A. Accept and document.** Localhost bind, single-user box, record as a known
  property. Zero work.
- **B. Token on the socket.** Shared secret at accept. Closes drive-by
  subscription; does not close a process that can read the token.
- **C. Split the frame.** Broadcast frames omit `confirm_id` entirely; the cid
  reaches only an authenticated channel.

DECISION: **C with B folded in.** Resolve it, do not merely document it.

RATIONALE: on a single-user box a token can be read out of the served page, the
config, or the process environment, so a token alone buys enumerability rather
than exclusion. The structural property wanted is that the cid never reaches an
unauthenticated subscriber at all. The confirm route already validates strictly,
so once the key stops being published the lock does its job.

ACCEPT REMAINS UNCONDITIONAL. An unauthenticated socket is not rejected; it
connects and receives redacted frames. Chosen so the change carries exactly one
behavior difference - cid delivery - and does not also alter connection behavior
for whatever is already subscribing.

STATUS: **VERIFIED, not merely applied.** Section 6.2 establishes it
behaviorally in both directions; section 6.3 establishes it at source.

METHOD WORTH GENERALIZING - ADVERSARY INVERSION. The strongest available form of
this evidence standard is not "a frame arrived." It is "a known-working exploit
stopped working." Where an exploit script already exists, the exploit IS the
test, and a PASS is its failure. A verification is worth what it can
discriminate; this one discriminates more than any purpose-built capture could,
because the tool being denied is the same tool that previously succeeded.

POSTURE C IS FULLY IMPLEMENTED FOR THIS TRANSPORT as of commit `4c365c1`.
Revision B recorded it as HALF IMPLEMENTED because the resolved frame still
carried the cid. Both confirm frame types are now redacted for unauthenticated
subscribers, verified in both directions (section 6.5). No `confirm_id` reaches
an unauthenticated socket on this channel by any frame.

SCOPE OF THAT CLAIM, stated so it is not read wider than it is: it covers
`/v1/agents/events` and nothing else. It says nothing about whether a local
process can obtain the token by other means, nothing about the three other
execution paths in the register, and nothing about tools that never reach a gate
at all - open item 6 remains a coverage gap that no amount of transport
hardening touches.

THE FEATURE IS CORRECT AND STILL NOT USABLE. Every gate measured in section 6.5
reaped at 120 s and the user saw an apology. Correctness and usability are
different states and this document should not be read as claiming the second.
See open item 2a.

---

## 10. GIT AND RELEASE STATE

Recorded because a VERIFIED change and a COMMITTED change are different states,
and this package spent six days conflating them.

THE FIND: `git status --short` showed
`src/openjarvis/core/confirm_registry.py` as UNTRACKED. The module the entire
gate runs on - register, wait, resolve, TTL, 409 write-once - had never been in
the repository. Every result in this document depended on a single on-disk copy
with no rollback point, and any repo-root cleanup would have destroyed it.

That is why the commit is the whole coherent feature set rather than the
redaction alone. Committing `ws_bridge.py` by itself would have put a redaction
into HEAD for an event type HEAD did not emit, on top of a registry HEAD did not
have.

| Property | Value |
|---|---|
| Commit | `6c132d6` on `main` |
| Scope | 6 files, 524 insertions, 7 deletions |
| New file | `src/openjarvis/core/confirm_registry.py`, 197 lines |
| Changed | `server/ws_bridge.py` +33, `tools/_stubs.py` +153, `cli/serve.py` +55, `server/agent_manager_routes.py` +91, `server/api_routes.py` +2/-1 |
| Staging method | Explicit paths only, never `-A`; staged count verified at exactly 6 before committing |
| Untouched | The other 11 modified files in the tree (TTS, mailbox, engine, frontend) |
| Message | Eight `-m` blocks, including the known-open item, so the reasoning survives outside the handoff chain |
| Rollback | `git revert 6c132d6`, or checkout of `58c05e2` |

SECRETS: `.env` protection was verified rather than assumed.
`git check-ignore -v .env` returned `.gitignore:48:.env` - confirmed by matching
rule. That command prints rule and path only and reads no file content, so it
does not violate the standing rule against echoing any line of that file.

REMOTES, and the naming is a trap worth pinning: `origin` is GitHub
(`https://github.com/cdgray33-git/OpenJarvis.git`), `gitlab` is GitLab
(`http://172.16.33.126/root/openjarvis-desktop.git`). Before pushing, `main` had
NO upstream configured, which is the safe state - a bare `git push` could not
fire or pick a remote. Both pushes were clean with an explicit refspec, no
`--mirror` and no `--force`: `58c05e2..6c132d6  main -> main` on each.

08/05 MIRROR DAMAGE - PARTIAL CLEARANCE ONLY. Both remotes were at `58c05e28`
and `git merge-base --is-ancestor 58c05e28 main` returned exit 0, so that tip IS
an ancestor of local main and GitLab holds real OpenJarvis history rather than
the `claude-code-templates` history that was force-pushed over it. No divergence,
no force, no recovery decision needed to proceed. HONEST LIMIT: exit 0 proves the
TIP is in our history. It does NOT prove GitLab's older history matches
GitHub's. That is enough to fast-forward safely, since a fast-forward cannot
destroy anything, but it is NOT a clean bill of health on the 08/05 damage. That
question remains open and separate.

BACKUP HYGIENE: both `ws_bridge.py.bak_cidredact_*` files hashed identically to
each other and differently from the live file, confirming genuine pre-patch
content and that the committed file is the patched one. Deleted by explicit path,
never by wildcard, with a count of 0 confirmed after.

### 10.1 The v2 commit - `4c365c1`, 2026-08-28

| Property | Value |
|---|---|
| Commit | `4c365c1` on `main`, parent `6c132d6` |
| Scope | 3 files, 890 insertions, 5 deletions |
| Changed | `server/ws_bridge.py` 4,414 B -> 4,514 B, SHA256 `BD8904CD9564D7FA07AF4566CF2B41ACD10774A4C02D46A633CE2B68FB2AD3F6` |
| Added | `patch_ws_cid_redact_v2c.py`, `SDP-WS-EVENT-CHANNEL-2026-08-26-revB.md` |
| Staging method | Explicit paths only, never `-A`; staged count verified at exactly 3 before committing |
| Excluded | `ws_bridge.py.bak_cidredactv2_20260826_083355` and 12 other dirty files in the tree |
| Remotes | `6c132d6..4c365c1` fast-forward on BOTH; `git ls-remote --heads` returned the identical hash from each |
| Rollback | `git revert 4c365c1`, or restore the backup and restart |

EOL NOTE, so a future window does not read it as damage: the commit emitted
`warning: in the working copy of 'src/openjarvis/server/ws_bridge.py', CRLF will
be replaced by LF the next time Git touches it`. The working copy is CRLF and the
committed blob is LF. That is autocrlf normalization, not corruption. Any EOL
measurement taken from a fresh clone will differ from one taken on this working
copy, and the difference is expected. This bears directly on the unresolved
`_stubs.py` EOL contradiction in section 7.6 - re-measure, do not inherit.

PATCH DISCIPLINE, two items from the v2 work worth carrying into the methodology
chapter:

- A MARKER IS NOT AUTOMATICALLY A UNIQUE ANCHOR. `# openjarvis-ws-cid-redact-v1`
  appears TWICE in `ws_bridge.py` at identical indent - forward-loop block and
  accept-site block. The v2 patch located the forward-loop instance positionally
  with an assertion, and deliberately left the accept-site marker at v1 because
  that block did not change.
- WRITE CONTROL EXPECTATIONS AGAINST THE POST STATE. Two dry runs aborted on
  control-authoring errors, not patch errors: a non-unique anchor, and a needle
  whose expected count was computed against the pre-patch file while the control
  ran against the patched text. Both were caught before anything was written.
  The dry-run-before-apply discipline is what made two authoring errors cost
  nothing.
