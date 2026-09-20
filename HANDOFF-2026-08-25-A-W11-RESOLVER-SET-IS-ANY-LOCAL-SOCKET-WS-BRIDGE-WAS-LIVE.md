# HANDOFF - 2026-08-25 ELEVENTH WINDOW
# THE CONFIRM CLIENT IS STILL UNNAMED, BUT THE MECHANISM IS FULLY EXPLAINED.
# THE RESOLVER SET IS "ANY LOCAL PROCESS THAT CAN OPEN A SOCKET" - AND THAT IS THE REAL FINDING.

Supersedes `HANDOFF-2026-08-24-E-W10-GATE-FIRED-ON-ALL-SIX-ANOMALY-RETRACTED-CONFIRM-CLIENT-UNIDENTIFIED.md`
for state. Everything in W10 stands EXCEPT its section 2 elimination of the desktop app, which is
VOID, and its "third possibility" on the endpoint, which is CLOSED. W10 sections 1, 3, 4, 5, 6 are
CARRIED FORWARD UNCHANGED; only deltas are restated.

**Actions this window: ZERO source patches. Zero host changes. Zero probes run. Nine read-only
reads - six log/filesystem greps, three source reads. Nothing started. Nothing left running.**

---

## 0. STANDING RULES FOR THE NEXT WINDOW

Rules 1-19 carry forward UNCHANGED. Rule 19 (grep must search the running system) was executed
this window and produced a true negative. Three additions:

20. **A NEGATIVE FROM A FILTERED SEARCH IS NOT A NEGATIVE UNTIL THE FILTER IS PROVEN NON-EMPTY.**
    Two greps this window returned zero hits, and neither was interpretable until a POSITIVE
    CONTROL proved the file set was non-empty and the search string could match at all. The
    section 1 result only became evidence when `chat/completions` and `agents/events` returned 2
    and 2 against the same file set. **Every zero-hit claim from here carries a control in the same
    command.**

21. **DO NOT INFER PROCESS IDENTITY FROM AN EPHEMERAL PORT NUMBER IN THIS SYSTEM.** Ports here are
    fully randomized across the whole ephemeral range and are never reused within a session. I
    built a "port band" theory this window on a grep that had SELECTED for `609xx`, and the
    unfiltered ten-minute dump destroyed it immediately. **The corollary is the important part: a
    port's low request count is not evidence about the process behind it, because no port here
    carries more than a few requests.** See section 3.

22. **WHEN A CORRELATION BREAKS, RECORD THE BREAK BEFORE REACHING FOR THE NEXT THEORY.** The
    WS-presence theory looked clean until the 12:42-12:46 session showed a subscriber attached
    across a gate that still reaped. Writing that down first is what forced the `agent_id` filter
    reading, which turned out to be the actual answer.

---

## 1. NO FRONTEND CODE ANSWERS THE GATE - TRUE NEGATIVE, WITH CONTROLS

W10's item 1 said search the built bundle before concluding an unidentified process exists. Done,
and the search W10 specified would not have found it either - **it searched the wrong tree.**

- W10's command filtered `\dist\|\build\|src-tauri`. The frontend that the running server actually
  serves lives at `src\openjarvis\server\static\assets`, which matches NONE of those.
- W10's source grep excluded `dist` and `build`, so it missed the same tree from the other side.
- **Neither W10's source grep nor W10's bundle grep ever touched the bundle the app loads.**

RESULT against `src\openjarvis\server\static`, 16 files / 9,395,517 B:

```
CONTROL  chat/completions   2 hits
CONTROL  agents/events      2 hits
TARGET   tools/confirm      0 hits
```

**No frontend code - source tree or served bundle - POSTs to `/v1/tools/confirm`.** The premise
carried across three windows is now confirmed for the running system, not just the source.

**THE TAURI EMBEDDED COPY DIES ON TIMING, NO GREP NEEDED.** `openjarvis-desktop.exe` in
`frontend\src-tauri\target\release` is dated 08/07. `/v1/tools/confirm` was created 08/20. A build
cannot contain a caller for a route thirteen days in its future. **Do not re-search the Tauri
bundle for this.**

**WHAT THE CONTROLS ALSO TOLD US, and it matters:** `agents/events` hits twice in the bundle. **The
shipped frontend SUBSCRIBES to the bus. It can learn a `cid`; it simply has no code to answer with
one.** Those are two separate capabilities and W10 treated them as one.

---

## 2. W10's ELIMINATION OF THE DESKTOP APP IS VOID

W10 section 2: "It made exactly two requests all day... **It is not the desktop app**, whose ports
carry all of that." That reasoning does not survive contact with the access log.

**THE PORTS ARE FULLY RANDOMIZED.** From the unfiltered 09:15-09:29 dump: 58206, 55138, 51761,
62879, 54684, 60772, 52052, 62740, 50912, 64810, 56813, 59725, 51942... every request in that
window comes from a fresh ephemeral port. **No port makes more than a handful of requests, because
no port is ever reused.** The chat client's own port 53694 made exactly three.

So "60958 made only two requests" is a property of every port in this system and discriminates
nothing. **The desktop app is not eliminated. Nothing is eliminated by that argument.**

Independently confirmed at the socket layer: `Get-NetTCPConnection -RemotePort 8010` today shows
**five sockets** to the backend from `msedgewebview2.exe` PID 8308 (the desktop app's WebView
network process) - one CloseWait on 60858 plus four in TimeWait. The app holds many concurrent
ephemeral ports by design.

**ALSO KILLED:** the `/v1/savings` polling signature does not separate clients either. Port 53694 -
the chat client itself - issued `GET /v1/savings` at 09:24:26.

---

## 3. THE MECHANISM IS NOW FULLY EXPLAINED - `ws_bridge.py:52`

**READ DIRECTLY, `src\openjarvis\server\ws_bridge.py`, 84 lines.** This settles D-WS-1 and it
answers the 08/24 question at the same time.

```python
 49:  for ws, (queue, loop) in list(clients.items()):
 50:      agent_filter = getattr(ws, "_agent_filter", None)
 51:      event_agent = (event.data or {}).get("agent_id")
 52:      if agent_filter and event_agent != agent_filter:
 53:          continue
```

```python
 67:  agent_id = websocket.query_params.get("agent_id")
 68:  websocket._agent_filter = agent_id
```

**A CLIENT THAT CONNECTS WITH NO `agent_id` QUERY PARAM GETS `_agent_filter = None`, WHICH IS
FALSY, SO THE FILTER IS SKIPPED AND IT RECEIVES EVERY EVENT FROM EVERY AGENT.** Including
`TOOL_CONFIRM_REQUEST`, which carries `confirm_id`, `tool`, `args_digest` and `prompt` as plain
JSON. `_AGENT_EVENTS` at lines 31-32 explicitly forwards both confirm event types.

**There is no authentication on `/v1/agents/events`.** `await websocket.accept()` at line 65 is
unconditional - no token, no origin check, no localhost assertion beyond the bind.

**AND THE BRIDGE WAS LIVE ON 08/24.** `api_routes.py:944` carries marker `openjarvis-ws-bus-v1`:
`create_ws_router(getattr(app.state, "bus", None) or get_event_bus())`, with backup
`api_routes.py.bak_wsbus_20260822_090130` dated **08/22 09:01** - two days before the runs.
`app.state.bus` is the agent's bus (`app.py:215`), so the gate's emit reached WS subscribers.
**The bus split was NOT in play on 08/24. The cid was deliverable over the socket.**

**THE 08/24 09:24 SEQUENCE, END TO END:**

```
09:21:58,289  WebSocket /v1/agents/events  [accepted]   <- 127.0.0.1:59728
09:21:58,290  connection open
09:24:21,874  POST /v1/chat/completions  200            <- 127.0.0.1:53694
09:24:24,026  ATTEMPT  turn=ad902101-t1  tool=shell_exec
09:24:24,139  POST /v1/tools/confirm  200               <- 127.0.0.1:60958  (+113 ms)
09:24:24,242  OUTCOME  success=True
09:24:24,242  ATTEMPT  turn=ad902101-t1  tool=shell_exec
09:24:24,298  POST /v1/tools/confirm  200               <- 127.0.0.1:60958  (+56 ms)
09:24:24,379  OUTCOME  success=True
09:31:58,354  connection closed
```

A subscriber was attached for 2.5 minutes before the ATTEMPT and stayed 7 minutes after. The frame
carried the cid. 113 ms later it came back approved. **How the resolver obtained two live cids is
no longer open.**

**AND IT EXPLAINS THE FIVE REAPED RUNS WITH THE SAME MECHANISM.** The 12:42:05-12:46:16 WS session
spanned the 12:44:10 gate and nothing answered. Under the filter reading that is expected: **those
clients passed an `agent_id` param and were filtered out at line 52; the 09:24 client did not.**
Same code, same process, opposite outcomes - which is precisely the resolver-set property W10 wrote
into the SDP, now with a named mechanism.

---

## 4. THE ENDPOINT DOES NOT ACCEPT ANYTHING WEAKER THAN AN EXACT CID - W10's WORST BRANCH IS CLOSED

W10 flagged "the endpoint accepts something weaker than a specific cid" as **"the third
possibility is the serious one and is UNTESTED."** Read directly at
`agent_manager_routes.py:2046-2102`, marker `openjarvis-confirm-route-v1`:

- `confirm_id` is read, stripped, and **400 if empty** (2059, 2069-2073).
- `decision` must be one of exactly `approve|approved|deny|denied`, else **400** (2060-2081).
- `_cr.get(confirm_id)` must return a live entry, else **404 "unknown or expired confirm_id"**
  (2085-2093).
- Only then `_cr.resolve(confirm_id, decision)` (2095).

**No wildcard. No "resolve latest." No unauthenticated bypass. A caller MUST hold the exact live
cid.** The route is correct and is not the weakness.

**THE WEAKNESS IS UPSTREAM: the cid is broadcast unauthenticated to every unfiltered subscriber.**
The lock is sound; the key is published.

---

## 5. THE FINDING, STATED FOR THE SDD - DO NOT SOFTEN THIS

**THE RESOLVER SET FOR THE CONFIRMATION GATE IS: ANY LOCAL PROCESS THAT CAN OPEN A WEBSOCKET TO
`ws://127.0.0.1:8010/v1/agents/events`.**

That process needs no credential, no agent id, and no prior knowledge. It connects, receives every
`TOOL_CONFIRM_REQUEST` for every agent, reads `confirm_id` out of the JSON, and POSTs an approval.
The tool then executes for real. On 08/24 this happened twice and ran `shell_exec` both times.

This is a DESIGN finding and it stands **independently of whoever port 60958 turns out to be.**
Naming that process is still worth doing, but it no longer gates the conclusion: even if it proves
to be something benign of ours, the capability is open to anything else on the box.

Same hazard family as the already-recorded "bus frames carry full tool arguments to every
subscriber" item - **this is that item's consequence, now demonstrated end to end with a real
destructive-capable tool.**

---

## 6. WHAT IS STILL OPEN ON THE 60958 QUESTION

Reduced from "unexplained" to one identification question. What is established: it held two live
cids, both POSTs returned 200, and a WS subscription capable of supplying those cids was open at
the time. What is NOT established: which process.

**DO NOT RE-RUN THESE - RECORDED NEGATIVES:**

- Frontend source tree: no `tools/confirm`. (W10)
- Served bundle `server\static\assets`: no `tools/confirm`, with positive controls. (This window)
- Tauri bundle: excluded on build-date timing, 08/07 build vs 08/20 route.
- `probe_confirm_emit.py`: ruled out on three independent grounds. (W10)
- Backend restart / process-predates-gate (theory B): dead, no restart 09:24-11:17. (W10)
- Port-number-based process inference: invalid in this system, see rule 21.
- `/v1/tools/confirm` accepting a weak credential: closed, section 4.
- WS-presence-alone as the discriminator: broken by the 12:42-12:46 session, section 3.

**THE LIVE APPROACH:** the ephemeral-port record is gone from the OS, so 60958 cannot be attributed
retrospectively. Identification has to be prospective - see next actions item 1.

---

## 7. STATE AT WINDOW CLOSE

- No source modified, no host touched, no probe run, nothing left running.
- W10's next-action item 1: **RESOLVED as to mechanism, OPEN as to identity.** Its safety branch is
  confirmed and is now broader than W10 framed it.
- **D-WS-1 CLOSED.** `ws_bridge.py:49-53, 63-71` read. Answer: unfiltered clients receive
  everything; 6e can rely on connecting with no `agent_id` param, and MUST filter client-side if it
  ever wants scoping.
- **NEW: D-SEC-1** - unauthenticated event bus publishes live confirm ids to any local subscriber.
- 6c SATISFIED. 6d LIVE-PROVEN CLOSED. 6e transport CLOSED. 6e approve branch live-proven.
  **6e browser UI half OPEN and no longer blocked by anything.**
- W1 CLOSED. W2 CLOSED AND VERIFIED. W3 WITHDRAWN. W4 OPEN.
- Carried unchanged: `engine.log` still 179 B, Patch 5 never fired. `conv=-` on every run,
  `/v1/sessions` still on the critical path.

---

## 8. NEXT ACTION - IN ORDER, START HERE

1. **DECIDE THE POSTURE ON D-SEC-1 BEFORE BUILDING 6e.** This is a product decision, not a patch:
   should `/v1/agents/events` require a token, and should `TOOL_CONFIRM_REQUEST` frames carry the
   cid to every subscriber or only to an authenticated one? **6e is a client of this exact
   channel**, so building it first bakes in whatever the answer turns out to be. Do not let this be
   settled implicitly.
2. **IDENTIFY 60958 PROSPECTIVELY.** Retrospective attribution is impossible. The cheap instrument:
   log the peer and the `User-Agent` at WS accept and at the confirm route, then run one gated
   `shell_exec` and see who answers. Non-interactive by design per the standing rule - it runs to
   completion without Gray reacting in a time window.
3. **FIX D-LAT-1 IN THE TOOL PANEL COMPONENT.** Carried from W10 item 2, unchanged. Ships before
   6e or the panel renders a 120 s gate as "120ms".
4. **THE 6e UI WORK.** Mount site `ChatArea.tsx`, option (b), new hook, `AgentsPage` untouched.
   Connect with NO `agent_id` param. Reference transaction: W10 section 4. **Now unblocked** - the
   bundle grep proved there is nothing partial to finish; this is a build, not a finish-and-surface.
5. **DECIDE THE DESTRUCTIVE MAILBOX TOOL POSTURE.** W9 section 5. `mailbox_move_to_trash` and
   `mailbox_empty_folder` carry no `requires_confirmation`, so the gate cannot stop them.
6. **DISABLE THE STALE `kokoro-tts` UNIT ON .200.** `sudo systemctl disable --now kokoro-tts` on
   **.200 ONLY** - Ubuntu host 172.16.33.200, via ssh, NOT PowerShell. **Verify the hostname in the
   same command**; the unit exists on both boxes and running it against .201 takes speech down.
7. **DECIDE THE `unattended-upgrades` POLICY ON THE MODEL HOSTS.** Carried from W8, unchanged.
8. **Re-run W7 step 3** - bogus agent id, gate-provoking prompt. Still UNKNOWN.
9. **D-SPEECH-1** - duplicate route registrations on `speech_router.py` (171, 207, 243; handler
   `speech_stream_ws` at 172, 208, 244). On REQUIREMENT ONE's own router.
10. **System32 housekeeping** - two stale `start-openjarvis.ps1` copies on PATH.
11. `memdb_audit.log` still outside the 30 MB scheme.

**Open design question, carried and still unsettled:** if the browser only reaches a tool-capable
path when an agent is selected, then either the gate is irrelevant to default chat, or default chat
should be tool-capable and currently is not. Product decision.

---

## 9. EXECUTION PATHS REGISTER

Paths 1a, 1b, 1d and 2-5 carry forward. Host and driver columns from W8 carry forward. Deltas:

- **THE `RESOLVER` COLUMN W10 ADDED NOW HAS A REAL VALUE, and it is not a client name.** Browser
  agent path: **ANY LOCAL PROCESS THAT CAN OPEN A WEBSOCKET. Unauthenticated. Unenumerable by
  design.** That is the honest entry and it is more useful than a process name would have been.
- **EVENT DELIVERY IS FILTER-OPTIONAL AND DEFAULTS TO UNFILTERED.** `ws_bridge.py:52` skips the
  filter when `_agent_filter` is falsy. Record per path whether its subscriber passes `agent_id`.
  This is the property that decided which 08/24 runs got answered.
- **WS TRANSPORT ROW:** `ws://127.0.0.1:8010/v1/agents/events`, WebSocket, JSON, publish-to-all,
  **NO AUTH**, queue maxsize 100, silent drop on QueueFull (`ws_bridge.py:56-57`).
- **RESOLUTION ENDPOINT, hardened description:** `POST /v1/tools/confirm`, JSON
  `{confirm_id, decision}`. 400 on empty cid or bad decision, 404 on unknown/expired, 200 first
  resolve, 409 second. **Requires an exact live cid - no weaker credential accepted.**
- Carried: gate TTL 120.000 s exactly, six measurements within 13 ms. Executor `default_timeout`
  30.0 s. Dispatch thread `asyncio_0`. No batch dispatch path.

---

## 10. SDP FEED

Prior windows' SDP feed carries forward IN FULL. Additions:

- **AN INTERLOCK WHOSE REQUEST FRAME IS BROADCAST UNAUTHENTICATED HAS NO RESOLVER SET.** W10 wrote
  "an unenumerated resolver set is an open finding." This window shows it is not merely
  unenumerated - **it is unenumerABLE**, because the credential needed to resolve is published to
  every subscriber. The SDP must state this as a property of the design, not as an open question
  awaiting an identification.
- **THE LOCK WAS SOUND AND THE KEY WAS PUBLISHED.** `/v1/tools/confirm` validates strictly and
  correctly; the compromise is entirely upstream in event distribution. **The SDP security chapter
  should present these as one system**, or a reader auditing the endpoint alone will conclude the
  gate is safe.
- **A ZERO-HIT SEARCH IS NOT EVIDENCE WITHOUT A POSITIVE CONTROL.** Two searches this window
  returned zero and neither meant anything until the same command proved the file set non-empty and
  the matcher functional. **Every negative in the SDP should record the control that made it
  interpretable** - this is the ninth diagnosis-quality instance and the first that is purely
  methodological.
- **EPHEMERAL PORT NUMBERS ARE NOT IDENTITY IN THIS SYSTEM.** Fully randomized, never reused. Any
  argument of the form "that port only did X, so it isn't Y" is void here. The SDP observability
  chapter must say so where access-log analysis is described, because the log's format invites
  exactly that inference.
- **BUILD ARTIFACTS AND SOURCE ARE SEPARATE SYSTEMS OF RECORD - and there are THREE trees, not
  two.** `frontend\src` (source), `frontend\src-tauri\target\release` (desktop build, 08/07), and
  `src\openjarvis\server\static\assets` (**what the server actually serves**). W10's rule 19 was
  right and its command still missed. **The SDP must name the served tree explicitly**, in the same
  place a reader's grep will land.
- Carried unchanged from W10 and prior: the approve branch is documented end to end; three
  independent duration sources measure different things; `dispatch.log` is a first-class
  instrument; the operator surface is a defect surface; a second tool spec declaration is a trap;
  a safety decision carries its premise and premises expire; defaults fail open on explicit nulls;
  the purpose-built instrument goes unread while the cheap surface gets believed.

---

## 11. SDD SECTION

Gray is building a detailed System Design Document covering all OpenJarvis work to date. This
window feeds it:

- **SECURITY CHAPTER - THIS IS THE HEADLINE AND IT NEEDS GREAT DETAIL.** The confirmation gate's
  resolver set is unauthenticated and open to any local socket. Include `ws_bridge.py:49-53` and
  `63-71` verbatim, the confirm route's validation chain at `agent_manager_routes.py:2059-2095`
  verbatim, and the 08/24 09:24 sequence from section 3 verbatim as the demonstration. **State
  plainly that a real `shell_exec` executed twice on an approval from an unidentified client.**
- **CONFIRMATION GATE CHAPTER - the transport row is now complete and carries an AUTH column.**
  `ws://127.0.0.1:8010/v1/agents/events` WS/JSON publish-to-all **NO AUTH**;
  `POST http://127.0.0.1:8010/v1/tools/confirm` HTTP/JSON, exact-cid required. Joins `.200:11434`
  HTTP/JSON inference and `.201:8880` HTTP/JSON speech. **Deliver as a downloadable standalone file
  for the wiki, with the HOST and DRIVER columns W8 specified, plus PORT, PROTOCOL, ENCODING and
  now AUTH at each gate.**
- **EVENT DISTRIBUTION - `agent_id` FILTERING IS OPT-IN AND FAILS OPEN.** Document that omitting
  the query param yields a firehose. This is simultaneously how 6e will work and why D-SEC-1
  exists. The SDD should not present it as a bug without also presenting it as the mechanism 6e
  depends on.
- **THE BUS SPLIT IS FIXED AND WAS FIXED BEFORE 08/24.** Marker `openjarvis-ws-bus-v1` at
  `api_routes.py:944`, backup dated 08/22 09:01. Any analysis of 08/24 behaviour that assumes a
  dark bus is wrong. Cross-reference the event bus chapter.
- **FRONTEND ARCHITECTURE - NAME THE THREE TREES.** Source, Tauri release build, and the served
  static bundle. State which is authoritative for runtime behaviour (the served bundle) and give
  its path.
- **PERFORMANCE CHAPTER** - D-LAT-1 scope unchanged from W10: run footer honest, tool panel wrong
  by 1000x. The 1a cold baseline re-measure still stands.
- **OBSERVABILITY CHAPTER** - add the access-log caveat from section 2: ephemeral ports are
  randomized and carry no identity. `dispatch.log` entry from W10 carries forward.
- **DEPLOYMENT AND RUNTIME ENVIRONMENT** - W8's host table carries forward verbatim, unchanged.
- **DIAGNOSIS QUALITY subsection gains TWO entries. Both are mine, this window.** (1) I inferred a
  process identity from a port-number band that my own grep had selected for; the unfiltered dump
  killed it in one command. (2) I proposed WS presence as the discriminator and the 12:42-12:46
  session contradicted it. **Both were caught inside the window and both were caught by widening
  the read rather than by reasoning harder.** Ten total instances. Countermeasure, stated
  generally: **when a pattern appears in filtered output, re-run unfiltered before building on it.**
- **Evidence provenance:** `backend.log` uvicorn.access and uvicorn.error lines across the current
  file and rotations `.1` through `.5`; a filesystem enumeration of `server\static` with byte
  counts and positive controls; `Get-NetTCPConnection` plus `Win32_Process` for live socket
  ownership; direct reads of `ws_bridge.py` (84 lines, full), `agent_manager_routes.py:2033-2102`,
  `serve.py:126-140`, and `api_routes.py:941-944`; a `.bak` listing for both patched files.
  **No OpenJarvis source was modified, no host was changed, and no probe was run.** Firmest tier.
  The section 3 mechanism rests on source read plus two independent logs; the section 6 identity
  question is explicitly NOT claimed.

**Standing instruction:** every handoff from here carries an SDD section, and every window feeds it.

---

## 12. METHOD LESSONS

1. **W10's ITEM 1 WAS THE RIGHT QUESTION WITH THE WRONG COMMAND.** It said search the built bundle,
   and it specified a path filter that could not reach the bundle the server serves. The rule was
   correct; the execution missed by one directory. **A standing rule does not verify its own
   instances** - the command under a rule needs the same scrutiny as the rule.
2. **THE ANSWER WAS IN A LINE NOBODY HAD CITED IN THREE WINDOWS.** `WebSocket /v1/agents/events
   [accepted]` sat in `backend.log` at 09:21:58, 2.5 minutes before the approval, through W8, W9
   and W10. It was found by grepping for the mechanism rather than for the suspect. **Searching for
   "who did this" found nothing for three windows; searching for "what capability was present"
   answered it in one command.**
3. **I BUILT A THEORY ON MY OWN FILTER AND IT SURVIVED EXACTLY ONE COMMAND.** The `609xx` band was
   an artifact of a grep for `609\d\d`. The lesson is not "be careful" - it is procedural: **the
   unfiltered dump costs one command and should precede any pattern claim, not follow it.**
4. **THE BROKEN CORRELATION WAS MORE PRODUCTIVE THAN THE CLEAN ONE.** WS-presence looked like the
   answer until 12:42-12:46 contradicted it. Chasing the contradiction is what produced the
   `agent_id` filter reading - which explains ALL SIX runs with one mechanism instead of explaining
   one run with a coincidence. **Gray's rule to pin the negatives is why the contradiction got
   written down instead of explained away.**
5. **THE SCARIEST OPEN BRANCH CLOSED CLEAN AND THE FINDING GOT WORSE ANYWAY.** W10 feared the
   endpoint accepted a weak credential. It does not - the route is genuinely well written. The
   exposure turned out to be upstream, in a component nobody had flagged. **Auditing the obvious
   surface and finding it sound is not the same as the system being sound.**
6. **THIRD CONSECUTIVE READ-ONLY WINDOW TO RESOLVE THE PRIOR WINDOW'S HEADLINE ITEM.** Zero
   patches, zero probes, zero host changes. Reading is cheap and this project keeps proving it.
