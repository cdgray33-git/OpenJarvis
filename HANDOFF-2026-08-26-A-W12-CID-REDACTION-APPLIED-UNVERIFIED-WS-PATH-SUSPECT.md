# HANDOFF 2026-08-26 A - W12

## CID REDACTION APPLIED AND UNVERIFIED - WS PATH ITSELF IS SUSPECT

Predecessor: `HANDOFF-2026-08-25-A-W11-RESOLVER-SET-IS-ANY-LOCAL-SOCKET-WS-BRIDGE-WAS-LIVE.md`
(copied into repo root this window). W11 remains the authority on everything it
established; this file does not restate it.

Window opened 06:2x, closed at exchange 15. Backend was started once and left
running.

---

## 0. STANDING INSTRUCTIONS CARRIED FORWARD

These are pinned and travel with every handoff. The next window inherits them
without renegotiation.

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
- DESIGN TESTS TO BE NON-INTERACTIVE. Nothing whose success depends on Gray
  reacting to on-screen output inside a time window.
- SDP IS THE SECONDARY THOUGHT AT ALL TIMES. Every window feeds it.
- EXECUTION PATH REGISTER accumulates across windows. Never re-derived.
- PIN THE DETAIL OF EVERY WINDOW, INCLUDING THE NEGATIVE RESULTS. A window that
  changed nothing still produced knowledge.
- 15-exchange flag is a FLAG, NOT A STOP. Do not cut a live trace to write a
  handoff.
- ARCHITECTURE ARTIFACTS need ports, protocols and encoding at each gate, and
  are delivered as downloadable standalone files for the wiki.

NEW RULE ADDED THIS WINDOW (W12-R1):
- A command goes in a fenced code block ONLY if it is the command to run right
  now. Reference commands, restore commands, and "if you need it later"
  commands go inline in prose, unformatted. Gray pastes exactly what he is
  given, in order. See section 3 for the incident that produced this rule.

---

## 1. DECISION RECORDED - D-SEC-1 POSTURE

W11 established D-SEC-1: the resolver set for a pending tool confirmation is
"any local socket". Any process on the box could subscribe to
`ws://127.0.0.1:8010/v1/agents/events`, read a `confirm_id` out of a
`TOOL_CONFIRM_REQUEST` frame, and POST it to `/v1/tools/confirm`. The gate is
therefore advisory against local processes, not an interlock.

Three postures were put to Gray:

- **A. Accept and document.** Localhost bind, single-user box, record it in the
  SDD security chapter as a known property. Zero work.
- **B. Token on the socket.** Shared secret at accept. Closes drive-by
  subscription, does not close a process that can read the token.
- **C. Split the frame.** Broadcast frames omit `confirm_id` entirely; the cid
  reaches only an authenticated channel.

**GRAY'S CALL: resolve it, not document it. Posture C with B folded in.**

Rationale recorded for the SDD: on a single-user box a token can be read out of
the served page, the config, or the process environment, so a token alone buys
enumerability rather than exclusion. The structural property we want is that
the cid never reaches an unauthenticated subscriber at all. W11 section 4
already established that the confirm route validates strictly, so if the key
stops being published the lock does its job.

---

## 2. THE CHANGE - `openjarvis-ws-cid-redact-v1`

One file: `src\openjarvis\server\ws_bridge.py`.
Applied by `patch_ws_cid_redact.py`, now sitting in the repo root.

### 2.1 What it does

Three edits, one behavior change plus its instrument:

1. `import os` added.
2. **Forward loop redaction.** In `_on_event`, the shared `payload` is no longer
   handed to every client queue unmodified. For `TOOL_CONFIRM_REQUEST` only, a
   client whose socket does not carry `_ws_authed == True` receives a per-client
   copy with `confirm_id` popped. `tool`, `args_digest` and `prompt` are
   untouched, so an existing subscriber sees exactly what it saw before minus
   the key. A redaction emits a `logger.warning` naming the peer. The shared
   payload dict is never mutated - the copy is made per client.
3. **Accept-time auth and log.** At WS accept, `token` is read from the query
   string and compared against env `OPENJARVIS_WS_TOKEN`. Result is stashed on
   the socket as `_ws_authed`, peer as `_ws_peer`, and a `ws-accept:` line is
   logged carrying peer, authed, agent_filter and User-Agent.

### 2.2 Design properties to record in the SDP

- **FAIL-CLOSED BY CONSTRUCTION.** If `OPENJARVIS_WS_TOKEN` is unset or empty,
  no socket can authenticate, so no socket receives a live cid. This is
  deliberate and is the opposite of the defaults-fail-open pattern that has bitten
  this codebase repeatedly (the `_confirm_callback = None` shape of Defect 6, and
  the missing-`websockets` HTTP 200 shape in section 5 below).
- **CONSEQUENCE OF FAIL-CLOSED:** a gated tool will sit its full TTL and reap
  unless a token-holding client answers. This breaks nothing that currently
  works, because W11 section 1 proved with positive controls that no shipped
  frontend code POSTs to `/v1/tools/confirm`. 6e is not built. There is no
  legitimate consumer of the cid today.
- **ACCEPT IS STILL UNCONDITIONAL.** An unauthenticated socket is not rejected;
  it connects and receives redacted frames. This was chosen so the patch carries
  exactly one behavior change (cid delivery) and does not also change connection
  behavior for whatever is already subscribing.
- **THE ACCEPT LOG IS NOT A STACKED FEATURE.** It is the only way to distinguish
  an authed from an unauthed socket during verification, so it is part of
  verifying change one. It cannot affect delivery.
- **DOUBLES AS THE ITEM-2 INSTRUMENT.** W11 next-action item 2 was prospective
  identification of process `60958`. Every subscriber now names itself at accept
  via `ua=`. No separate probe needed.

### 2.3 Deliberately out of scope

`TOOL_CONFIRM_RESOLVED` also carries a cid. Re-resolving an already-resolved cid
returns 409 per W11 section 4, so it is not a live key. Left visible until the
primary change is verified. **This is an open item, not a closed one.**

### 2.4 Rollback

Live rollback point: `src\openjarvis\server\ws_bridge.py.bak_cidredact_20260826_062427`
Restore with Copy-Item from that path onto `src\openjarvis\server\ws_bridge.py` with -Force.

An earlier backup `...bak_cidredact_20260825_093635` holds byte-identical
pre-patch content. Either restores the same file. Both should be reaped once
the change is verified and committed.

---

## 3. INCIDENT - THE ACCIDENTAL REVERT (W12-R1)

Sequence: patch applied cleanly at 09:36:35. Claude's next message was about
starting the backend, but it contained the restore command in a fenced code
block as reference material. Gray pastes exactly what he is given. The patch was
reverted.

Root cause is Claude's formatting, not Gray's paste. A code block in this
working relationship means "run this". Using it for reference material is a
defect in Claude's output format. Rule W12-R1 in section 0 is the fix.

Recovery was clean: the patch script is idempotent-guarded by its marker check,
the file was confirmed back at pre-patch state, and re-running produced an
identical result with a fresh backup stamp.

Cost: roughly four exchanges, plus the verification detour in section 4.

---

## 4. NEGATIVE RESULTS AND INSTRUMENT FAILURES - PIN THESE

This window produced more knowledge about our instruments than about the code.
All of the following are Claude errors, recorded so the next window does not
repeat them.

### 4.1 Three wrong grep-count predictions in a row

Claude stated expected `Select-String` counts from memory of a file it had read
once, through a paste that had stripped blank lines:

- Predicted `import os` would have 1 hit in the ORIGINAL file. It has 0 - the
  patch is what adds it. A zero across all three patterns was in fact the
  correct clean-revert signature, and Claude's prediction was wrong.
- Predicted `create_ws_router` count of 2. Actual is 3 - the `def`, the
  ImportError comment referencing it, and `__all__`.

**Lesson: state what a control must PROVE, and let the output supply the number.
Do not offer predicted counts for a file not currently in context.**

### 4.2 A zero-hit check with no positive control

Claude issued a three-pattern `Select-String` and called a zero result a
confirmed revert. That is precisely the trap W11 rule 20 exists for. It was
re-run with `_agent_filter` and `create_ws_router` as controls, which returned
2 and 3, proving the matcher functional and the absence real.

### 4.3 `Group-Object` hides zeros

`Select-String ... | Group-Object Pattern` emits NO ROW for a pattern with zero
matches. Absence appears as a missing line, not as a `0`. Any future control
built this way must be read for which rows are present, not for a zero value.

### 4.4 The startup banner is console-only

Claude used `Starting OpenJarvis API server` as a positive control against
`backend.log`. It returned 0. The banner goes to the console and does not appear
in the log file. **A control string must be one known to be in THAT FILE, not
one seen anywhere in the session.** This cost two exchanges.

### 4.5 What the log actually looks like

Format is `YYYY-MM-DD HH:MM:SS,mmm LEVEL logger.name: message`. A 25-line tail at
06:34 showed only `uvicorn.access` GETs on a poll loop - `/health`,
`/v1/models`, `/v1/managed-agents`, `/v1/savings`, plus `httpx` client lines and
one call out to `http://172.16.33.200:11434/api/tags`. Log file is
`C:\Users\Admin\AppData\Local\OpenJarvis\logs\backend.log`, 1,491,472 bytes,
current. Rotation is in place: `.1` through `.5` exist, `.1` and `.2` at ~4 MB,
`.3` through `.5` at ~10 MB. Also present in that directory: `agent.log`,
`dispatch.log`, `engine.log`, `memdb_audit.log`.

---

## 5. THE LIVE BLOCKER - NO WEBSOCKET UPGRADES AT ALL

**Verification of the patch is BLOCKED and the patch is UNVERIFIED.**

Zero `ws-accept:` lines were observed. That absence currently proves nothing,
because there is a strong candidate reason no socket can open.

W11-era finding, 08/23, recorded in the config-secrets thread: the venv sync
inside `start-openjarvis.ps1` UNINSTALLS `websockets==15.0.1` on some runs.
With `websockets` gone, uvicorn cannot perform the upgrade and
`/v1/agents/events` SILENTLY RETURNS THE SPA `index.html` WITH HTTP 200 rather
than failing. Any manual `uv pip install` into the venv is undone by the next
start; the durable fix belongs in the script's dependency set.

This morning's start installed 65 packages, so the venv was mutated again.

The 06:34 tail is consistent with this: the desktop app is clearly alive and
polling over plain HTTP, but not one upgrade appears.

**THE UNRUN COMMAND. This is where the next window starts.** PowerShell,
Windows box, from `PS C:\Users\Admin\OpenJarvis>`:

    $env:VIRTUAL_ENV="C:\Users\Admin\OpenJarvis\.venv"; uv pip list | Select-String -Pattern 'websockets','uvicorn','wsproto'

`uvicorn` present is the positive control - it must appear or the listing itself
is wrong. The real question is whether `websockets` or `wsproto` is there. If
neither is, the WS path is dead in this venv and that must be fixed before any
part-two verification, because a working patch and a socket that never opens are
currently indistinguishable.

Note for that command: the venv has NO pip (`No module named pip`); it is
uv-managed, hence the `VIRTUAL_ENV` prefix.

---

## 6. VERIFICATION PLAN - WHAT REMAINS

**Part one, half done.** Backend imports the patched module without error - that
half passed at 06:24. The accept-log half is unproven pending section 5.

**Part two, not started.** Must prove, non-interactively:

1. An unauthenticated subscriber receives `TOOL_CONFIRM_REQUEST` WITHOUT
   `confirm_id`, but WITH `tool`, `args_digest` and `prompt` intact.
2. A subscriber presenting the correct token receives the full frame including
   `confirm_id`.
3. A `ws-accept:` line appears per socket with correct `authed=` values.
4. The redaction warning fires and names the peer.

Shape it as a single script that opens both sockets, provokes one gate, collects
frames to completion and prints a verdict. It must not depend on Gray reacting
to output in a time window. **Not yet designed - the gate-provocation mechanism
needs to be re-read from the W10/W11 record before writing it.**

Token used this window, session-scoped only, set in the same PowerShell that
launched the server: `w12-verify-2f7a91c4`. It does NOT persist across a reboot
or a new window. Deliberate - no secret is going into `.env` until the posture is
proven. Any start from a fresh window comes up fail-closed.

---

## 7. CONFIG AND SECRETS - ANSWERED THIS WINDOW

Gray asked directly whether a `.env` exists. It does:
`C:\Users\Admin\OpenJarvis\.env`, 45 lines, only 11 valid `KEY=value`. The
remainder is a credential scratchpad - docker-compose fragments indented as
`KEY: value`, a curl example carrying a bearer token, bare values on the line
after their key name. python-dotenv silently fails on those. Loaded twice per
boot by two separate paths.

Claude's position on putting `OPENJARVIS_WS_TOKEN` there: it would probably
parse, since a clean `KEY=value` line is a working shape, but nothing should be
built on that file while it is in this state.

STANDING RULE REAFFIRMED (08/01): never generate a command that reads the
secrets file and echoes ANY line content back, however filtered. Line numbers
plus a boolean "parses as KEY=value" only.

---

## 8. SIDE FINDING PARKED - NOT CHASED

The 06:24 start installed **65 packages** into the venv. A steady-state start
should install zero. This belongs with the existing config-reproducibility and
venv-mutation thread and is very likely the same mechanism as section 5.

Deliberately not chased, per FINISH THE THING BEFORE STARTING THE NEXT. Recorded
so it is not rediscovered from scratch. Full package list is in the W12
transcript if the next window needs the diff.

Runtime facts observed at that start, for the SDD: engine `ollama`, model
`qwen3-coder:30b`, agent `native_openhands`, URL `http://127.0.0.1:8010`,
speech `faster-whisper`, scheduler active, memory active, memory_backend wired
into 1 agent tool. Twelve tools loaded against a 41-key registry - allowlist
holding at 12 per the 08/04 expansion, so line 15 of the live config has NOT
reverted. Rust extension rebuilt on start as always.

---

## 9. EXECUTION PATHS REGISTER

Standing structure per path: entry point, call chain with file:line, which
ToolExecutor instance serves it and how that executor is constructed, whether
the confirmation gate is live / auto-approved / absent, what event bus traffic
it emits, whether a human is present.

Carried from prior windows, unchanged this window:

- Orchestrator `ask()` path via `system\orchestrator.py`.
- Managed-agent SSE stream via `_stream_managed_agent()` in
  `server\agent_manager_routes.py`.
- `routes.py` chat dispatch branches 1a / 1b / 1c / 1d, with their concurrency
  and tool-availability properties.

**AMENDED THIS WINDOW - the event fan-out leg of every gated path:**

`ws_bridge.create_ws_router(event_bus)` subscribes a single `_on_event` handler
to 13 event types, including `TOOL_CONFIRM_REQUEST` and
`TOOL_CONFIRM_RESOLVED`. Fan-out is per-client via an `asyncio.Queue(maxsize=100)`
plus a stored loop reference, delivered with `loop.call_soon_threadsafe` - this
is the thread-boundary crossing between whatever thread raises the event and the
socket's event loop. A full queue or a closed loop is swallowed silently
(`except (RuntimeError, asyncio.QueueFull): pass`), so a slow client loses frames
without any log line. **That silent drop is a hazard worth its own SDP entry** -
it is a third instance of the fail-quiet pattern.

Filtering before this window was `_agent_filter` only, taken from the `agent_id`
query param. As of `openjarvis-ws-cid-redact-v1` there is a second filter stage:
per-client cid redaction keyed on `_ws_authed`.

Gate/transport facts for the SDD architecture chapter: bind `127.0.0.1:8010`,
route `/v1/agents/events`, protocol WebSocket over HTTP/1.1 upgrade, payload
JSON via `websocket.send_json`, no authentication on accept, now with
authentication-conditional field redaction on one event type.

---

## 10. SDP / SDD FEED FROM THIS WINDOW

Gray is building the System Design Document and its System Design Package. Every
window feeds it. The Defect 6 confirmation gate - registry, payload, transport,
threading model - was called out as needing GREAT DETAIL specifically.

From W12:

- **Security chapter, D-SEC-1:** now has a decision and a rationale, not just a
  finding. Record the three postures considered and why C-with-B was chosen over
  accept-and-document. Record fail-closed as a deliberate design property and
  its TTL-reap consequence.
- **Threading model:** section 9's `call_soon_threadsafe` fan-out and the silent
  drop-on-full-queue are transport facts the gate chapter needs.
- **The fail-quiet pattern is now a named theme with three instances:**
  `_confirm_callback = None` accepting silently, missing `websockets` returning
  HTTP 200 with the wrong body, and the WS queue swallowing overflow. This
  belongs in the SDD as a cross-cutting hazard class, not three separate bugs.
- **Instrument discipline:** section 4 is material for a verification-methodology
  appendix. Rule 20 held again, and the three ways a control can be worthless
  (no control, `Group-Object` zero-suppression, control string not in the target
  file) are worth writing down once, properly.

---

## 11. NEXT ACTIONS, ORDERED

1. **Run the section 5 command.** Determine whether `websockets` is in the venv.
   Nothing else can be verified until the WS path is known good.
2. If absent: fix it durably in `start-openjarvis.ps1`'s dependency set, not
   with a manual install that the next start undoes. Verify a socket can open
   and that `ws-accept:` fires.
3. **Complete part two of verification** per section 6. One non-interactive
   script, both sockets, one gate, printed verdict.
4. Only then decide `TOOL_CONFIRM_RESOLVED` (section 2.3).
5. Only then build 6e against the now-authenticated channel.
6. Commit `ws_bridge.py` and reap both `.bak_cidredact_*` files.

Do not skip ahead to 5. The whole point of the posture Gray chose is that the
interlock is real, and an unverified interlock is worth less than a documented
absence of one.
