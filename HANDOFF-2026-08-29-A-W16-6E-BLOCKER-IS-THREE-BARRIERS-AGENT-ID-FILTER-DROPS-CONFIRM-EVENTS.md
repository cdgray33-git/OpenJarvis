# HANDOFF 2026-08-29 A - W16

## OPEN ITEM 1 CLOSED ON A WRONG PREMISE. 6E IS THREE INDEPENDENT BARRIERS, NOT ONE. THE `agent_id` FILTER DROPS EVERY CHAT-PATH CONFIRM EVENT.

Predecessor: `HANDOFF-2026-08-28-A-W15-BOTH-COMMITS-PUSHED-SDP-REVC-CURRENT-HANDOFF-CHAIN-HAS-GAPS.md`
W15 remains the authority on the two commits, the SDP revision C content, and the
handoff-chain gap inventory.

Window opened 08/29 morning, closed at exchange 22. **NO SOURCE FILE WAS MODIFIED.
NO COMMIT WAS MADE.** Everything below is read-only measurement. This window
produced no change and a large amount of knowledge, which is exactly the case the
PIN-THE-NEGATIVE-RESULTS rule exists for.

The headline: W15 next-action 1 (locate the WS token) is closed, but the thing it
was chasing did not exist. And the real blocker behind 6e turned out to be one
layer deeper than every prior window assumed - it is not the hook mount, it is a
server-side filter comparison that can never match.

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
- W14-R1: one command per message means ONE DESTINATION per message.
- W14-R2: write control expectations against the POST state.
- W14-R3: a wildcard that matches nothing is silent in PowerShell. Every delivery
  command assigns to a variable and prints a loud NOT DOWNLOADED message.
- W15-R1: ALWAYS PUSH TO BOTH REMOTES, UNPROMPTED. `origin` is GitHub, `gitlab`
  is the lab instance at 172.16.33.126. That naming is a trap worth restating.
- W15-R2: a document described as LIVING is not stale between updates. Raise
  internal contradiction, not lateness.
- W15-R3: verify the instrument, not only the result.

NEW RULES ADDED THIS WINDOW:

- **W16-R1. THE 550B IS AN INSTRUMENT FOR BREADTH, NOT A SOURCE OF FINDINGS.**
  Gray's `openrouter/nvidia/nemotron-3-ultra-550b-a55b` path reads whole files at
  once, which this window cannot do cheaply. USE IT for that, deliberately, via a
  generated bundle plus specific questions. But its answers enter the record as
  CLAIMS TO VERIFY, never as established facts. It has no access to the logs, the
  process state, or the negative results of the window that fed it, so it reads
  code AS DESIGNED and reports the happy path. It was both right and wrong in the
  same reply this window - see D5. Record its misses as carefully as its hits;
  the miss data is worth as much as the answers. This is ALWAYS VERIFY and
  W13-R1 applied to a new instrument, not an exception to them.
- **W16-R2. A LOG ABSENCE NAMES A SYMPTOM, NEVER A CAUSE.** Zero `ws-accept`
  lines proved no socket opened. It did NOT prove why, and Claude stated a cause
  ("nothing mounts the hook") that four grep hits immediately falsified. When an
  instrument reads empty, the next move is to READ THE CODE THAT WOULD HAVE
  WRITTEN TO IT, not to name a mechanism.
- **W16-R3. READ THE DEFINITION BEFORE PREDICTING FROM THE CALL SITE.** Claude
  asserted the WS socket was fail-closed - inherited from three prior documents -
  and it is false at the source. Lines 81 through 114 of `ws_bridge.py` took one
  command to read and overturned a claim that had propagated through W12, revB
  and revC unchallenged.
- **W16-R4. AN INHERITED CLAIM IS NOT A VERIFIED CLAIM.** The fail-closed error
  did not originate with Claude this window; it was repeated from the record.
  When a claim is load-bearing for a decision, re-read its source even when three
  documents agree, BECAUSE three documents agreeing is often one measurement
  copied three times.

---

## 1. WHAT WAS DONE

Nine read-only measurements, in order, each settling one candidate before the
next was opened. No file written, no process restarted, no commit.

### 1.1 Open item 1 - the WS token source

W15 framed this as: the token survived a genuine reboot and nobody can say why.
That framing is now dead. Every persistent source was eliminated by direct read.

| Candidate | Method | Result |
|---|---|---|
| Frontend / Tauri source | recursive grep `.rs .toml .json .ts .tsx .js .cjs .mjs`, excluding node_modules, target, dist, .git, build | NO HITS |
| Whole tree, any extension | recursive grep, files under 2 MB, excluding venv and pycache | 23 hits, ALL of them documentation, patch scripts, or the single consumer |
| Env, all three scopes | `[Environment]::GetEnvironmentVariable` from an ELEVATED shell (PID 2804, elevation confirmed) | Process not set, User not set, Machine not set |
| `credentials.toml` | `_DEFAULT_PATH` read off source, then tested | FILE ABSENT |
| `cloud-keys.env` | key names read, values masked | EXISTS, 93 B, modified 6/21/2026, ONE key: `OPENROUTER_API_KEY` (73 chars) |
| Launching shell 13892 | could not be read - see D4 | UNREAD, and it does not matter |

THE 23 TREE-WIDE HITS, categorized so a future window does not re-run the grep:
handoff files W12/W13/W14/W15, `patch_sdp_revc.py`, `patch_ws_cid_redact.py`,
SDP revB and revC, `src\openjarvis\server\ws_bridge.py:88`, and the `.bak` at
`ws_bridge.py.bak_cidredactv2_20260826_083355:84`.
**There is exactly ONE consumer and ZERO producers in the entire tree.**

### 1.2 The two runtime env-write mechanisms, both eliminated

The grep found no literal producer, so the next theory was a runtime write under
a key built from data rather than a literal. Three such sites exist in `src`:

| Site | Mechanism | Verdict |
|---|---|---|
| `core\credentials.py:95` | `save_credential()` - validates `key` against `TOOL_CREDENTIALS`, writes `~/.openjarvis/credentials.toml` at mode 0600, then `os.environ[key] = stripped` | file absent, cannot have fired |
| `core\credentials.py:110` | `inject_credentials()` - loads the same toml at startup, `os.environ[k] = v` for every key not already set | file absent, cannot have fired |
| `server\routes.py:578` | `/v1/cloud/reload` reads `~/.openjarvis/cloud-keys.env` line by line, `os.environ[k.strip()] = v.strip()` | file exists but holds only `OPENROUTER_API_KEY`, last modified 6/21 |

Two other matches were non-candidates: `connectors\retriever.py:117` is a
`setdefault` on `CUDA_VISIBLE_DEVICES`, and `core\config.py:1735` is a READ of
`OPENJARVIS_CONFIG`, not a write.

**PIN THIS AS A SECURITY OBSERVATION, unrelated to the token.**
`/v1/cloud/reload` injects EVERY key it finds in `cloud-keys.env` into the live
process environment with NO WHITELIST. `save_credential` validates against
`TOOL_CREDENTIALS` and refuses unknown keys; the cloud-reload path does not. A
file named for cloud keys is in practice a general-purpose environment injector
reachable from an HTTP POST route. Not exploited, not urgent on a loopback bind,
but it is an asymmetry in the codebase's own stated posture and it belongs in the
SDP. New open item 13.

### 1.3 What the log actually says about the token

`%LOCALAPPDATA%\OpenJarvis\logs\backend.log`. Ten `ws-accept` lines exist in the
entire log. **ALL TEN ARE FROM 08/26.** Five `authed=True`, five `authed=False`.

Interleaved with uvicorn startup markers, the sequence is:

- 08/24 07:47:46, 08/24 08:16:24, 08/24 18:33:08 - three startups, no accepts
- 08/26 06:30:27 - startup
- 08/26 06:57:44 False, 07:00:03 True, 07:13:05 False, 07:24:17 True, 07:28:39 True
- **08/26 08:54:24 - STARTUP (process restart)**
- 08/26 09:00:21 True, 09:06:58 False, 09:10:38 False, 09:15:31 False, 09:22:38 True
- 08/29 08:42:44 - startup (today)

`authed=True` appears on BOTH SIDES of the 08:54:24 restart. Line 90 of
`ws_bridge.py` requires a non-empty `_expected` for that, so the token was
genuinely present in both processes.

**BUT A PROCESS RESTART IS NOT A REBOOT.** Nothing in this log shows the token
crossing a machine boundary. The reboot-survival claim in W15 open item 1 has no
evidence behind it that this window could find.

THE RECONCILIATION, stated as the surviving explanation and not as proof: the
token was set INTERACTIVELY, by hand, into the environment of one shell session.
It is not persisted anywhere on this machine. It survived a server restart
because the restart was launched from that same still-live shell, and it appears
in no file because it was never written to one. That is consistent with every
measurement: ten accepts on one morning, zero since, no producer in the tree, all
three env scopes clean when read elevated.

The last accept, 08/26 09:22:38, carries `ua='Python/3.12 websockets/17.0.1'`.
**Every `authed=True` in the entire log came from a Python probe script.** No
browser client has ever authenticated on this socket.

### 1.4 THE 6E MECHANISM - established end to end

This is the material result of the window. Three independent barriers, each read
off disk, each sufficient on its own to prevent a user from answering a gate.

**BARRIER 1 - the hook returns before it connects.**
`frontend\src\lib\useAgentEvents.ts`, 90 lines total. Line 40 is
`if (!agentId) return;` inside the `useEffect`. No socket is constructed when
`agentId` is falsy. Both call sites in `AgentsPage.tsx` (lines 1736 and 3338)
pass `agentId`, which is undefined on the agent LIST view. Measured directly:
the frontend was launched, chat requests reached the backend and produced errors,
the Agents page was opened and rendered all six agents - and the log still shows
ZERO `ws-accept` lines for 08/29. The page mounted, `loadData` ran, and no socket
opened.

**BARRIER 2 - the server-side filter can never match a chat-path event.**
`ws_bridge.py:56-59`, inside `_on_event`:
`agent_filter = getattr(ws, "_agent_filter", None)`, `event_agent = (event.data or {}).get("agent_id")`, then `if agent_filter and event_agent != agent_filter: continue`.
`buildWsUrl` at lines 10-23 of the hook ALWAYS appends `?agent_id=<id>` when an
id is present, and the id is required for the socket to open at all (barrier 1).
So a real frontend socket always has a non-empty `agent_filter`.
Meanwhile `tools\_stubs.py:162` declares `agent_id: str = ""` in the
`ToolExecutor.__init__` signature, assigned at line 171 and published into the
event payload at line 225. **A chat-path executor constructed without an explicit
`agent_id` publishes `agent_id: ""`.** The comparison is then `"" != "<real-id>"`,
which is true, so the frame hits `continue` and is dropped BEFORE it ever reaches
the client queue.

**BARRIER 3 - the frontend never sends a token, so it would be redacted anyway.**
`buildWsUrl` constructs `?agent_id=` and NOTHING ELSE. There is no `token`
parameter anywhere in the hook. So any real app socket is `authed=False`, and the
v2 redaction we shipped at `ws_bridge.py:61-71` strips `confirm_id` from both
confirm event types for unauthenticated subscribers. Without `confirm_id` the
client cannot call `POST /v1/tools/confirm`. **The redaction we built in W12
through W14 is, for the actual app, a self-inflicted barrier.** It is correct
behavior for an unauthenticated subscriber. The app is an unauthenticated
subscriber.

**WHY THIS MATTERS MORE THAN THE MOUNT.** W15 open item 2 prescribed: mount
`useAgentEvents` with NO `agent_id` param. Barrier 2 explains why that
prescription was right for the wrong reason, and barrier 3 explains why it would
still have failed. Had a future window simply mounted the hook as instructed, it
would have connected, received nothing (barrier 2 if an id was passed) or
received redacted frames with no `confirm_id` (barrier 3), and the failure would
have looked like a mount problem all over again.

### 1.5 Incidental: the engine is on a broken fallback

Not chased, recorded because it shaped the window and will shape the next one.

A power outage yesterday left the Ollama MCP host down. The backend started today
at 08:39:15 with Ollama unreachable and bound `Engine: litellm` at startup.
Gray restarted the Ollama service mid-window and rebooted the frontend, after
which local models were visible in the UI again.

TWO FACTS, both pinned:

1. **The engine is selected at startup and is not re-evaluated.** Restarting the
   Ollama service does not move a running process off the fallback.
2. **The fallback is non-functional.** Every chat request dies with
   `ModuleNotFoundError: No module named 'litellm.responses.mcp'`, thrown from
   `litellm\main.py:1112` via `engine\litellm.py:65`. The venv holds a broken or
   partial litellm install. Timing observed: 32.1 s on the first request, then
   346 ms on subsequent ones - the first pays an import attempt, then it fails
   fast.

This plausibly relates to open item 12, the 65-package venv mutation on start.
NOT ESTABLISHED, and deliberately not chased. Full stack trace path for the next
window: `stream_bridge.py:189` -> `stream_bridge.py:141` ->
`agents\native_openhands.py:406` -> `tools\_stubs.py:178` ->
`telemetry\instrumented_engine.py:121` -> `security\guardrails.py:199` ->
`engine\litellm.py:65`.

**UNVERIFIED AT WINDOW CLOSE:** whether the BACKEND restarted after the Ollama
service came back, or whether PID 12952 is still bound to litellm. Only the
frontend was confirmed rebooted. The last startup marker in the log is 08:42:44.
Re-measure; do not inherit.

---

## 2. THE FULL EXECUTION PATH - WS CONFIRM DELIVERY

Gray asked for thorough documentation of how this really works. This is the path
as READ, with ports, protocols and encoding at each gate per the standing rule.

### 2.1 Publish side

- `ToolExecutor.execute()` in `src\openjarvis\tools\_stubs.py`, line 174 onward.
- Confirmation branch fires only when `tool.spec.requires_confirmation` is true.
- Registers with `core\confirm_registry.register(tool=, agent_id=self._agent_id, turn_id=CURRENT_TURN_ID.get())`, returning `_cid`.
- Publishes `EventType.TOOL_CONFIRM_REQUEST` on `self._bus` with payload keys:
  `confirm_id`, `agent_id`, `turn_id`, `tool`, `args_digest`, `prompt`, `expires_at`.
- `self._agent_id` comes from `__init__` at line 162, **default `""`**.
- Payload-shape source: the 550B read of the whole file. The `agent_id` default
  and the assignment line were independently verified off disk this window; the
  exact key list was NOT, and is carried as a claim. See D5.

### 2.2 Bus to socket

- `create_ws_router(event_bus)` in `server\ws_bridge.py:37`.
- Subscribes `_on_event` to 13 event types listed at lines 20-34, including both
  `TOOL_CONFIRM_REQUEST` and `TOOL_CONFIRM_RESOLVED`.
- `clients` is a dict of `WebSocket -> (asyncio.Queue, event loop)`. Queue
  `maxsize=100`, created per connection at line 102.
- `_on_event` builds `{"type": ..., "timestamp": ..., "data": ...}` then, per
  client: **filter (56-59)**, then **redact (61-71)**, then
  `loop.call_soon_threadsafe(queue.put_nowait, client_payload)` at line 73.
- Overflow and dead-loop handling at 74-75 is a bare `except (RuntimeError, asyncio.QueueFull): pass`. **This is the silent frame drop of open item 7,
  located.** It is not instrumented - no counter, no log line.

### 2.3 Transport and gate

- Bind `127.0.0.1:8010`. Route `/v1/agents/events`. WebSocket over an HTTP/1.1
  upgrade. UTF-8 JSON via `send_json`.
- `await websocket.accept()` at line 83 is **UNCONDITIONAL AND FIRST**. Auth is
  evaluated AFTER the connection is established.
- Auth is a query-string `token` compared to `os.environ["OPENJARVIS_WS_TOKEN"]`
  at 88-90. Result is stashed as `websocket._ws_authed`; the peer as `_ws_peer`;
  the `agent_id` query param as `_agent_filter` at 86.
- Every accept logs at WARNING: `ws-accept: peer=%s authed=%s agent_filter=%s ua=%r`.
- Delivery loop at 106-108 pulls from the queue and sends. Disconnect is caught;
  `finally` pops the client from `clients`.

### 2.4 Consume side

- `frontend\src\lib\useAgentEvents.ts`, mounted twice in `AgentsPage.tsx`.
- URL built at 10-23 from `getBase()`, `http` rewritten to `ws`. Falls back to
  `window.location` with `wss:` when the page is https.
- Reconnect: exponential backoff `min(30000, 1000 * 2 ** min(retry, 5))`, so
  1 s doubling to a 30 s ceiling. `retry` resets to 0 on `onopen`.
- Teardown on unmount sets `closed`, clears the timer, closes the socket.
- Event filtering client-side at 60-61 against the `eventTypes` array.
- `useEffect` dependency array is `[agentId]` ONLY. `onEvent` and `eventTypes`
  are held in refs (34-37) specifically so they do not retrigger the effect.

**THE HOOK IS WELL BUILT.** Backoff, teardown, ref-stability and reconnect are
all correct. It has exactly two defects for this purpose: the line 40 guard, and
the absence of a `token` param in `buildWsUrl`.

---

## 3. EXECUTION PATHS REGISTER

Carried from W15, plus one path now fully specified.

- Orchestrator `ask()` via `system\orchestrator.py`.
- Managed-agent SSE via `_stream_managed_agent()` in `server\agent_manager_routes.py`.
- `routes.py` chat dispatch branches 1a/1b/1c/1d.
- The confirm-gate flow as verified, W14 Appendix B.1, stages 1 through 11b.
- **NEW - WS confirm delivery path, section 2 above.** Entry point
  `@router.websocket("/v1/agents/events")` at `ws_bridge.py:81`. Executor is the
  one holding `self._bus`; construction site and whether it receives a real
  `agent_id` is NOT YET ESTABLISHED and is next-action 1. Confirmation gate is
  LIVE on this path (it publishes the request). Emits all 13 event types in
  `_AGENT_EVENTS`. Human presence: **NONE, for the three reasons in 1.4.**

---

## 4. SDP / SDD FEED FROM THIS WINDOW

**SDP revC NOW CONTAINS A KNOWN FALSE STATEMENT. This overturns W15 section 4.**

W15 recorded that revC "contains no known false statement" and called that a
first for the artifact. That is no longer true, and the falsehood was already in
it when the claim was made.

**"FAIL-CLOSED BY CONSTRUCTION: if `OPENJARVIS_WS_TOKEN` is unset or empty, no
socket can ..."** appears at revB:151, revC:169, and in W12 at line 101, and it
is FALSE against `ws_bridge.py:83`. The socket accepts unconditionally. An unset
token does not close the socket - it makes `_authed` false, which causes
`confirm_id` to be stripped while the client stays connected and keeps receiving
every other frame. That is fail-OPEN-but-redacted, which is a materially
different security posture from fail-closed.

This is precisely the W15-R2 case: an internally contradicted assertion a reader
cannot distinguish from a current one. It is the defect to raise, and it needs a
revision D.

WHAT REVISION D MUST CARRY:

- The fail-closed correction, in all three places, with `ws_bridge.py:83` cited.
- Section 2 of this document in full - the WS confirm delivery path.
- The three-barrier finding, replacing any framing of 6e as a mount problem.
- Open item 7 (silent frame drop) relocated to `ws_bridge.py:74-75` with the
  note that it is uninstrumented.
- New open item 13, the unwhitelisted env injection at `routes.py:578`.
- Open item 1 rewritten: not a mystery, an unpersisted interactive shell
  variable, with the log evidence from 1.3.

NEW MATERIAL FOR THE METHODOLOGY CHAPTER:

- **The inherited-claim failure mode (W16-R4).** A false statement propagated
  through three documents and two windows unchallenged because each inherited it
  rather than re-reading a file that took one command to open. Three documents
  agreeing was one measurement copied three times. This is the single most
  valuable methodology finding of the window.
- **Log absence names symptoms, not causes (W16-R2).** Worked example: zero
  `ws-accept` lines was a true and useful reading; the cause Claude attached to
  it was falsified within one command.
- **A large-context model as a breadth instrument (W16-R1).** The bundle-and-ask
  pattern is genuinely additive for whole-file questions and should be standard.
  Its output is claims, not findings, and it reports code as designed rather than
  as behaving - it asserted the frontend shows a confirmation prompt, which every
  measurement in this window contradicts.
- **A window that changes nothing can still be the most productive one.** Zero
  commits, zero patches, and the actual blocker behind the project's top open
  item was located and specified.

---

## 5. OPEN ITEMS, ORDERED

Renumbered from W15. Item 1 closed, item 2 restated on mechanism, item 7 located.

1. **6E - THREE BARRIERS, ALL SPECIFIED.** Section 1.4. Was "no user can answer a
   gate"; now fully mechanized. Needs a design decision from Gray before any
   code: how the app authenticates on this socket (barrier 3) is a security
   question, not a wiring question.
2. **Which executor serves the chat path, and does it get a real `agent_id`?**
   Barrier 2 assumes the default `""` is what actually reaches the bus. The
   default is verified; the construction site is not. This is the cheapest
   remaining read and it gates the barrier-2 fix.
3. **W10 is two documents that disagree.** W15 section 2.2. Unchanged.
4. **W3 through W6 have no handoff anywhere.** W15 section 2.1. Unchanged.
5. **Destructive mailbox tools are ungated at the spec level.** Only
   `agent_tools.py:289`, `git_tool.py:283`, `shell_exec.py:71` declare
   `requires_confirmation=True`. Needs a Gray decision.
6. **Four auto-approve sites live** in `server\agent_manager_routes.py`
   (720-721, 1202-1206, 1562-1563, 1639-1640). Needs a Gray decision.
7. **Silent frame drop on queue overflow - LOCATED.** `ws_bridge.py:74-75`, bare
   `except (RuntimeError, asyncio.QueueFull): pass` on a queue of maxsize 100.
   Still uninstrumented. No longer needs a hunt, only a counter.
8. **`"reaped": false` on timeout resolutions** unexplained. Read
   `confirm_registry._snapshot()`.
9. **Four `[DEBUG]` prints in `cli\serve.py`** at 268, 280, 281, 513.
10. **`_stubs.py` EOL baseline contradiction** unresolved. Re-measure; see the
    autocrlf note in W15 section 1.1.
11. **08/05 GitLab history damage below the tip** still unassessed.
12. **65-package venv mutation on start** still unchased - and now with a
    probable symptom, the broken litellm install in section 1.5.
13. **NEW. `/v1/cloud/reload` injects arbitrary env keys with no whitelist**,
    `routes.py:571-578`, in contrast to `save_credential`'s `TOOL_CREDENTIALS`
    validation. Loopback-bound, not exploited. Needs a Gray decision.
14. **NEW. The engine binds at startup and never re-evaluates.** An Ollama outage
    strands the process on a fallback until OpenJarvis itself restarts.
    Behavioral, possibly intended. Needs a Gray decision.

CLOSED THIS WINDOW: W15 open item 1 (token source), on the finding that the thing
being hunted was never persisted.

---

## 6. NEXT ACTIONS, ORDERED

1. **Read the chat-path `ToolExecutor` construction site** (open item 2). One or
   two reads. It confirms or kills barrier 2 as stated, and everything in the 6e
   design rests on it.
2. **Get a Gray decision on socket authentication** (open item 1, barrier 3).
   Three shapes exist: the frontend learns the token, the loopback socket drops
   token auth for confirm frames, or confirm answering moves off this transport.
   This is a posture decision and it should not be made inside a patch.
3. **Only then design the 6e change.** It is at minimum a hook change and a
   filter change, and possibly a redaction change. It is no longer a one-line
   mount.
4. **Re-measure the engine binding** (section 1.5) before any work that needs a
   live model, since the current process may still be on a broken litellm.
5. **Revision D of the SDP** - it now carries a known false statement.

Do not skip to 3. The W15 prescription for 6e was correct in direction and would
have failed in practice; the difference was one unread file.

---

## APPENDIX A. DISCREPANCY REGISTER

Every point this window where the WRITTEN RECORD disagreed with DIRECT
OBSERVATION, or where Claude was wrong. Recorded whether or not it changed the
outcome.

### D1. "FAIL-CLOSED BY CONSTRUCTION" - FALSE, AND INHERITED
- CLAIMED BY: W12 line 101, SDP revB line 151, SDP revC line 169, and Claude
  this window while reasoning about the running server.
- FOUND: `ws_bridge.py:83` is `await websocket.accept()`, unconditional, executed
  BEFORE any auth evaluation. An empty token yields `_authed = False`, not a
  refused connection. The client stays connected and receives redacted confirm
  frames plus all other frames unmodified.
- ESTABLISHED BY: reading lines 75-114 directly.
- DISPOSITION: **the most serious finding in this register.** It is a false
  security-posture claim sitting in the current SDP revision, and it survived
  three documents because each inherited it. Rules W16-R3 and W16-R4. Revision D
  must correct all three sites.

### D2. "The frontend never opens the WebSocket - nothing mounts the hook" - CLAUDE'S ERROR
- CLAIMED BY: Claude, stated as established, from the absence of `ws-accept`
  lines on 08/29.
- FOUND: `useAgentEvents` has four references - the definition at
  `lib\useAgentEvents.ts:29`, the import at `AgentsPage.tsx:36`, and TWO call
  sites at `AgentsPage.tsx:1736` and `3338`. It is mounted.
- ESTABLISHED BY: one grep, immediately after the claim.
- DISPOSITION: the log reading was sound; the cause attached to it was invented.
  The true narrower statement is that no socket opened, which the line 40 guard
  then explained. Rule W16-R2.

### D3. Elevated-shell inheritance - THEORY DEAD
- CLAIMED BY: Claude. Shell 13892 is elevated, W14 measured env scopes from a
  non-elevated session, therefore the token might live in an admin-visible scope.
- FOUND: all three scopes clean when read from a confirmed-elevated shell
  (PID 2804, `IsInRole(Administrator)` True).
- DISPOSITION: dead. Cost one command. Worth having run - it was the last
  plausible persistence mechanism and its death is what makes the
  interactive-variable explanation the surviving one rather than a guess.

### D4. The launching-shell read landed in the wrong shell - A MISS, NOT A FINDING
- WHAT: Claude asked Gray to run the env check in the shell that launched the
  server (PID 13892). It ran in PID 2804.
- WHY: 13892 is the elevated window with the server running in the FOREGROUND. It
  cannot accept a command without stopping the server. Claude should have
  recognized that before writing the request - the process table already showed
  the server as a child of that shell.
- IMPACT: none to the outcome, but the result was briefly at risk of being read
  as "the launching shell has no token," which it does not show.
- DISPOSITION: recorded as a miss. A foreground process makes its shell
  unreadable; plan around it rather than through it.

### D5. The 550B's closing claim - CONTRADICTED BY MEASUREMENT
- CLAIMED BY: `openrouter/nvidia/nemotron-3-ultra-550b-a55b`, unprompted, at the
  end of an otherwise good answer: that `ws_bridge.py` forwards the event and the
  frontend "receives it to show the confirmation prompt."
- FOUND: no socket exists to receive it (barrier 1), the filter would drop it
  (barrier 2), and it would arrive without `confirm_id` (barrier 3).
- WHAT SURVIVES: its actual answer - that `TOOL_CONFIRM_REQUEST` carries
  `agent_id` and is constructed in `_stubs.py` `ToolExecutor.execute()` - was
  correct and materially useful. The `agent_id` default and assignment were then
  verified off disk.
- DISPOSITION: rule W16-R1. The model read the code as designed. It had no access
  to the logs that show the design does not run. Use it for breadth; verify
  anything load-bearing.

### D6. HTTP GET on the WebSocket route - NO FINDING
- WHAT: `Invoke-RestMethod` on `http://127.0.0.1:8010/v1/agents/events` returned
  404.
- DISPOSITION: uninformative either way - a plain GET on a WS route says nothing
  about whether the route is healthy. Recorded ONLY so a future window does not
  find it in the transcript and read it as evidence of a missing route.

### D7. Guessing config paths before reading the constant - MINOR PROCESS ERROR
- WHAT: Claude tested three candidate `credentials.toml` locations by guess, got
  a NOT FOUND, and only then read `_DEFAULT_PATH` off the source.
- OUTCOME: the guess list happened to contain the correct path, so the negative
  held. That was luck, not method - a miss would have produced a false negative
  on a live candidate.
- DISPOSITION: read the constant first. It cost one command to do it in the wrong
  order.

---

## APPENDIX B. THE 550B BUNDLE - REPRODUCTION

The delegation pattern from W16-R1, recorded so it is repeatable.

Generated by a one-liner from `PS C:\Users\Admin\OpenJarvis>` that writes
`WS-6E-BUNDLE-2026-08-29.md` to the repo root: a fixed list of seven files
(`ws_bridge.py`, `core\events.py`, `agent_manager_routes.py`, `tools\_stubs.py`,
`server\routes.py`, `useAgentEvents.ts`, `AgentsPage.tsx`) plus any `src` python
file whose name matches `confirm`, each fenced with a language tag and a
`## FILE:` header, and a loud MISSING line for any path that does not resolve.

THE PROMPT SHAPE THAT WORKED: the bundle, plus exactly two narrow questions -
does `TOOL_CONFIRM_REQUEST` include `agent_id` in `data`, and which code path
constructs that event. Narrow questions produced a verifiable answer. The model
then volunteered an unrequested conclusion about frontend behavior, which was
wrong. **Ask for facts about code, not conclusions about behavior.**

Cost observed: 58.1 s, free tier, one turn.

---

## APPENDIX C. GIT AND SYSTEM STATE AT WINDOW CLOSE

| Property | Value |
|---|---|
| HEAD | `38e907d` on `main` - CARRIED FROM W15, NOT RE-VERIFIED THIS WINDOW |
| Commits this window | NONE |
| Files modified this window | NONE |
| Backend process | PID 12952, venv python, `-m openjarvis.cli serve --port 8010`, started 08/29 08:39:15 |
| Child process | PID 13076, SYSTEM Python312 interpreter, identical command line |
| Launching shell | PID 13892, elevated `powershell.exe`, no arguments, parent `explorer.exe` (9652), started 08:37:25 |
| Engine at last read | `litellm` with `qwen3-coder:30b`, agent `native_openhands`, and litellm is broken |
| Ollama MCP host | restarted mid-window by Gray; local models visible in UI after a frontend reboot |

**PIN THE INTERPRETER SPLIT.** The parent runs
`C:\Users\Admin\OpenJarvis\.venv\Scripts\python.exe` and the child runs
`C:\Users\Admin\AppData\Local\Programs\Python\Python312\python.exe` with the same
arguments. Two different interpreters in one process tree. Not investigated, not
known to be a defect - uvicorn reload and multiprocessing both produce parent
and child - but the interpreters differing is worth one read someday, and it
touches open item 12 and the broken litellm in the venv.

STILL DIRTY IN THE TREE, untouched and intentionally so: 12 modified files and
roughly 150 untracked probe and patch scripts, plus `WS-6E-BUNDLE-2026-08-29.md`
generated this window. None of it belongs to this work. Do not clean it up as a
side task.
