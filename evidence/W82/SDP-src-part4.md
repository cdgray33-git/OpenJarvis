# SDP SOURCE EXTRACT W82 part 4 (deduplicated by section hash)
### [ARCHIVE-W50-2026-09-12.md] 5D. W50 DELTAS TO THE CARRIED SECTIONS
Append these lines to the carried registers below rather than rewriting them.
DIAGNOSTIC TOOLING REGISTER - append:
- `probe_confirm_trace_w50_v2.py` (repo root, marker `openjarvis-confirm-trace-w50-v2`).
  Two-phase confirm gate trace. Phase A listens without answering, phase B auto-denies.
  Output: stdout only, runs to completion, ~3 min, executes nothing. Built on
  `websockets.sync.client`. Output path verified at build time: console, read directly.
- `probe_ws_bare_subscribe.py` - **STATUS CHANGED TO DEAD.** Written against the legacy
  asyncio `websockets` client, removed in `websockets` 15.x; venv has 17.0.1. Cannot
  run. Either port it to `websockets.sync.client` or retire it.
- `probe_confirm_trace_w50.py` (v1) - DEAD ON ARRIVAL, same cause. Superseded by v2.
EXECUTION PATH REGISTER - append:
- PATH: `POST /v1/tools/test-execute`. Entry `agent_manager_routes.py:2142`. Chain:
  route -> `app.state.agent._executor` (`:2177-2178`, constructs nothing) ->
  `_run()` (`:2240`) sets `CURRENT_TURN_ID` to `test-<run_id>` -> `_executor.execute()`
  on an `asyncio.to_thread` worker (`:2258`). Serves the SAME executor built at
  `cli\serve.py:321`. Confirmation gate LIVE on it - structurally cannot run a tool
  without `requires_confirmation=True` (422 at `:2223`), so it is a trigger, not a
  bypass. Emits `tool_confirm_request` and `tool_confirm_resolved` on `app.state.bus`.
  NO human present by default. Guarded by `OPENJARVIS_TEST_EXEC` plus loopback bind.
  Returns 202 before the work starts.
LOGGING TOPOLOGY - append:
- No change this window. `test-execute` failures log via `_log.warning` at `:2247` with
  `exc_info=True` on the `openjarvis.server.agent_manager_routes` logger, which lands
  in `backend.log`. Not exercised this window; recorded from source, unverified at
  runtime.
RULES OF ENGAGEMENT - append:
- **AN INSTRUMENT IS UNVERIFIED ONCE ITS DEPENDENCIES MOVE** (W50). A registered probe
  that has not been run since a venv upgrade is not available tooling. Check the
  import, not just the register.
- **LOCATE THE FAULT WITH A SECOND STACK BEFORE EDITING THE FIRST** (W50). One
  `ClientWebSocket` call cost 92 ms and moved the blame off the server in a single
  exchange.
- **A LONE MEASUREMENT DOES NOT DISCRIMINATE; A PAIRED ONE DOES** (W50). Phase A alone
  looks like a defect. Phase B alone does not explain W49. Design the contrast in.
PROGRAM GOAL - append:
- W50 is the eleventh observability window. Capability moved: none directly, and no
  code changed. What moved is the SAFETY PICTURE, for the second window running. W49
  shrank the open item from "two ungated destructive mailbox tools" to "one unproven
  consumer." W50 removed that too. The confirmation gate has no known defect left on
  the server side. The remaining work is a UI feature, not a debugging problem - which
  is a different kind of task and should be scoped as one.
### [ARCHIVE-W51-2026-09-12.md] Sections 1-4. Sections 5D-12 are carried verbatim from W50 below this block.
---
### [ARCHIVE-W51-2026-09-12.md] 2. THE `subscribeAll` DISCOVERY
`frontend\src\lib\useAgentEvents.ts:33-39` carries a fourth parameter tagged
`openjarvis-agent-events-subscribeall-v1`:
    // Opt in to the unfiltered stream. When true, the socket connects with NO
    // agent_id query parameter, leaving _agent_filter falsy on the server so the
    // filter at ws_bridge.py:56-59 short-circuits. Required for the chat path,
    // where confirmation events carry a CLASS identity (native_openhands) that
    // can never match a managed-agent INSTANCE id.
The guard at `:47` is `if (!agentId && !subscribeAll) return;`. Both call sites,
`AgentsPage.tsx:1736` and `:3338`, pass three arguments. The parameter had never been
passed as true by any caller in the tree.
This matters out of proportion to its size. The class-vs-instance identity problem is
the single hardest design question in 6e's browser half, and it was solved, documented,
and cited to a specific server line before W51 opened. No register - not the execution
path register, not the diagnostic tooling register, not any prior BRIEF - knew it
existed. W50's BRIEF scoped action 1 as "mount it in chat," unaware that the mounting
mechanism already carried the fix.
Had W51 designed from scratch, it would have rebuilt this and probably rebuilt it worse,
producing a fourth version of a thing that already existed twice. Gray's standing
correction about narrow reads producing duplicate implementations is the direct ancestor
of this finding, and it was his refusal to let the window assume that surfaced it.
The server half was then verified independently rather than trusted from the comment.
`ws_bridge.py:58` reads `if agent_filter and event_agent != agent_filter: continue`.
Falsy filter means no filtering. The comment was accurate.
---
### [ARCHIVE-W51-2026-09-12.md] 3.1 What the redaction path turned out NOT to be
`ws_bridge.py:62-73` strips `confirm_id` from confirm frames unless
`_ws_bind_loopback` is true, sourced from `app.state.bind_is_loopback` with
`getattr(..., False)` - absent attribute fails closed. On reading that, W51 treated it
as a probable blocker: a UI receiving redacted frames would render a prompt it could
never answer, producing 120 s timeouts WITH a listener mounted, which is a worse
diagnostic state than no listener at all.
It is not a blocker. Established by two independent facts: `cli\serve.py:622` genuinely
sets `app.state.bind_is_loopback`, so the attribute is not absent; and five live accepts
in `backend.log` all logged `bind_loopback=True` with zero `ws-cid-redact` lines ever
written. The fail-closed branch has never been taken.
Recorded because the hazard is real if the bind posture ever changes - the UI would go
silent by design, with the only evidence being a `ws-cid-redact` warning.
### [ARCHIVE-W51-2026-09-12.md] 3.2 What `OPENJARVIS_WS_TOKEN` turned out NOT to be
Read at `ws_bridge.py:90`, set nowhere in `src\`. `_authed` is therefore always False.
Nothing branches on `_authed` anywhere; `ws-cid-redact-v3` replaced the token check with
the bind check and left the token plumbing in place. Dead field, not a defect, not a
security gap. Do not spend a window on it.
### [ARCHIVE-W51-2026-09-12.md] 3.4 What the connection evidence turned out NOT to prove
At one point W51 read "zero established TCP connections to 8010" as "the exe is not
talking to the backend." Wrong inference. The log showed `/health`,
`/v1/managed-agents`, `/v1/savings` and a `POST /v1/chat/completions` from the same
period. Those are short-lived HTTP connections closed before the sample. The topology
conclusion happened to be right; the evidence cited for it was worthless. Corrected in
the same window.
### [ARCHIVE-W51-2026-09-12.md] 3.5 What `tauri dev` turned out to be
W51 proposed `npm run tauri dev` as the fast validation path. Gray rejected it: dev and
production share the same files and it has caused repeated breakage, and he has
deliberately moved the dev root to prevent it running. W51 checked its carried rules and
confirmed the constraint was NOT pinned anywhere. It is now pinned in the W51 BRIEF
rules of engagement. Recorded here so the omission is traceable rather than mysterious.
---
### [ARCHIVE-W51-2026-09-12.md] 4. W51 DELTAS TO THE CARRIED REGISTERS
Append-only one-liners. The carried sections below are NOT rewritten.
### [ARCHIVE-W51-2026-09-12.md] 4.1 DELTA - EXECUTION PATH REGISTER
- **NEW PATH: browser confirmation listener.** Entry point: `ConfirmPrompt` component
  mounted in `ChatArea.tsx`, opening `ws://127.0.0.1:8010/v1/agents/events` with NO
  `agent_id`. Call chain: `ConfirmPrompt` -> `useAgentEvents(undefined, onEvent,
  CONFIRM_EVENTS, true)` -> `buildWsUrl()` at `useAgentEvents.ts:10-23` -> server
  `agent_events()` at `ws_bridge.py:83-121`. No ToolExecutor serves it; it is a
  subscriber, not an executor. Confirmation gate: this path IS the gate's human half.
  Bus traffic: consumes `tool_confirm_request` and `tool_confirm_resolved`, emits none.
  A human IS present by definition. Return leg is `POST /v1/tools/confirm` via
  `confirmTool()` in `api.ts`.
- **SCOPE HAZARD ON THAT PATH:** the listener is mounted inside `ChatArea`, so it is
  torn down on navigation to any other page while the backend may still be blocking on
  a live gate. `App.tsx` (190 lines) is the correct mount point. Not fixed in W51.
- **CONFIRMED:** `data.agent_id` on confirm frames is the executor CLASS identity
  (`native_openhands`), never a managed-agent instance id. Read at the emit site,
  `_stubs.py:365-373`.
### [ARCHIVE-W51-2026-09-12.md] 4.2 DELTA - DIAGNOSTIC TOOLING REGISTER
- **`ws-accept` (`ws_bridge.py:103-110`) IS A VERIFIED, READABLE INSTRUMENT.** Lands in
  `backend.log`. Reports peer, authed, bind_loopback, agent_filter, and user-agent on
  every WebSocket accept. It is the primary evidence that a client subscribed, and the
  user-agent field discriminates browser from probe.
- **`ws-cid-redact` (`ws_bridge.py:67-73`) IS A LATENT INSTRUMENT.** Never fired to
  date. If it appears, `confirm_id` is being stripped and the UI will go silent.
- **UVICORN ACCESS LOG IS NOT AN INSTRUMENT FOR PAGE LOADS.** Records API routes only.
  `GET /` and `/assets/*` produce nothing. Do not grep it to decide whether the
  frontend loaded; check `ws-accept` or a direct `Invoke-WebRequest` instead.
- **`Invoke-WebRequest http://127.0.0.1:8010/` IS A CHEAP BUNDLE CHECK.** Returns the
  served `index.html` and its asset references without touching the exe. Confirms
  whether the backend is serving patched frontend code.
- **NEW: `[confirm-ui]` console warning** in `ConfirmPrompt.tsx`, fires in the webview
  devtools if a confirm frame arrives with no `confirm_id`. Devtools are enabled
  (`tauri.conf.json:24`) and remote debugging is on port 9222 (`:25`).
### [ARCHIVE-W51-2026-09-12.md] 4.3 DELTA - LOGGING TOPOLOGY REGISTER
- `openjarvis.server.ws_bridge` logs at WARNING via the `logging` module and reaches
  `backend.log`. Two lines: `ws-accept` on every accept, `ws-cid-redact` on every strip.
- `uvicorn.access` reaches `backend.log` at INFO but covers API routes only, NOT static
  or root page requests. This is a known gap in the sink, not a missing logger.
- Frontend `console.log`/`console.warn` land in the WEBVIEW devtools only, never in
  `backend.log`. `ChatArea.tsx:120` and `:145` already emit `[TTSDBG]` lines there.
### [ARCHIVE-W51-2026-09-12.md] 4.4 DELTA - SDD / SDP FEED
- **SDP, guard chapter, plain-language section.** The confirmation gate's human half now
  exists and can be described end to end for the eight-year-old explanation Gray
  requires: Jarvis wants to use a tool that could change something; before it does, it
  writes a note with a unique ticket number and posts it on a channel anyone in the
  house can listen to; the app is now listening on that channel and shows you the note
  with Approve and Deny buttons; your answer goes back with the same ticket number; the
  ticket can only be answered once, and if nobody answers within the time limit the tool
  does NOT run and Jarvis is told it was a timeout, not a refusal.
- **SDP, guard chapter, technical section.** Full round trip, all line-cited: register at
  `_stubs.py:356-360`; publish at `:362-374`; block at `:377`; human answer at
  `agent_manager_routes.py:2046-2110`; resolve and re-publish at `_stubs.py:380-399`;
  outcome branching at `:400-425` with three distinct agent-facing messages for DENIED,
  APPROVED-but-callback-false, and TIMEOUT.
- **SDD, architecture chapter.** Ports, protocols and encoding at each gate for this
  path: browser to backend `ws://127.0.0.1:8010/v1/agents/events`, WebSocket, JSON text
  frames via `send_json`; browser to backend `POST http://127.0.0.1:8010/v1/tools/confirm`,
  HTTP/1.1, `application/json`, Bearer auth header when an apiKey is set in localStorage.
  Redaction gate sits on the WS leg only and is keyed to server bind posture.
- **SDD, build topology chapter.** The two frontend delivery paths are now documented
  with evidence: vite writes to `src\openjarvis\server\static`, the backend serves that
  directory at `/`, and Tauri EMBEDS the same directory into the exe at build time.
  A vite build reaches the browser path immediately and the exe path never. This is the
  mechanism behind the recurring drift.
### [ARCHIVE-W51-2026-09-12.md] 4.5 DELTA - FILES CHANGED
- NEW `frontend\src\components\Chat\ConfirmPrompt.tsx` - queue-based, renders oldest
  pending confirm, Approve/Deny, dismiss on resolved frame, handles 404/409, countdown.
- `frontend\src\lib\api.ts` - appended `confirmTool()` and `ConfirmToolResponse`,
  tagged `openjarvis-confirm-ui-v1`. Backup at `api.ts.w51.bak`.
- `frontend\src\components\Chat\ChatArea.tsx` - import at the `sse` import line, render
  above the InputArea wrapper. Backup at `ChatArea.tsx.w51.bak`.
- NEW `apply-w51-confirm-ui.ps1` in the repo root - idempotent, verifies anchors are
  unique before writing, aborts without writing on any mismatch, prints its own rollback.
- UNCOMMITTED as of window close. Commit and push to BOTH remotes after action 1.
### [ARCHIVE-W51-2026-09-12.md] 4.6 HAZARDS FOUND, NOT CHASED
- `frontend\src\lib\api.ts:8` carries a hardcoded Supabase anon key with a comment
  asserting RLS makes it safe to embed. Own subject, own window. Not evaluated.
- Frontend mojibake confirmed at `AgentsPage.tsx:1730`, `:3332`, `api.ts:4`, `:19`.
  Extends the mojibake audit beyond `.py` under `src\`.
- `npm run build` warns that `index-*.js` exceeds 500 kB (945 kB raw, 271 kB gzip).
  Pre-existing, cosmetic, noted only.
- `src-tauri\src\lib.rs:598` unused variable warning, pre-existing.
- Duplicate FastAPI Operation ID `speech_health_v1_speech_health_get` warned at
  `api_routes.py` on every start. Pre-existing, cosmetic.
---
### [ARCHIVE-W52-2026-09-12.md] 1. WINDOW NARRATIVE
W52 took W51 action 1 and closed it. The confirmation gate is now proven end to end
with a human in the loop on BOTH decisions, and one real defect found mid-window was
patched, verified and pushed in the same window per Gray's ruling.
Sequence: located the test-execute recipe in ARCHIVE-W50 (after two wrong-file misses,
see section 3); confirmed OPENJARVIS_TEST_EXEC live in the backend via a bogus-tool 404
probe; read shell_exec.py whole to get the argument name from source; fired three probes.
Probe 1 (test-428d2bc1) rendered a prompt that expired unanswered at 120.001 s - which
itself proved mount, subscribeAll, frame receipt, confirm_id match and dismiss-on-resolved,
because the "expired" banner is ConfirmPrompt.tsx:93, client-side, not server text.
Probe 2 (test-93193435) proved the Deny POST resolves the gate, 16.357 s, GATE_DENIED.
Probe 3 (test-697df383) proved Approve, and the tool RAN: success=True reason=OK 10.865 s
with the real command in the ATTEMPT line.
Between probes 2 and 3 the prompt displayed "with args {}" for a call that carried a
command. Whole-file reads of _stubs.py (610 lines) and agent_manager_routes.py (2448
lines) localised it: the handler reads _body.get("arguments"); the probe had been sent
with "args". Operator error at the wire, not a code fault - but the handler COERCED the
bad key silently to {} and asked a human to approve a command it never displayed.
That silent coercion was patched (openjarvis-test-exec-argguard-v1), verified 400/400/202
live, committed 74cde22 and pushed to both remotes. Frontend work from W51 committed
73db0c1 earlier in the window.
### [ARCHIVE-W52-2026-09-12.md] 2. THE ARGUMENT-KEY FAULT AND ITS PATCH
- Contract is `arguments`, an object. Defined agent_manager_routes.py:2196 pre-patch.
- Pre-patch: `_args = _body.get("arguments")` then `if not isinstance(_args, dict): _args = {}`.
  Any wrong key, string, or null became {} with no error. Route returned 202, gate fired,
  human was shown `Allow execution of tool 'shell_exec' with args {}?` and asked to approve.
  Approving would have run a command the operator never saw. That is the gate's own
  failure mode, in the gate's own trigger.
- Post-patch at :2197-2222: unknown top-level keys return 400 naming them and listing
  expected; non-dict `arguments` returns 400 with the type received; absent `arguments`
  remains legal as {}; explicit null coerces to {}.
- ORDERING NOTE: the unknown-field check now runs BEFORE the `if not _tool_name` check
  (:2224). A body with both faults returns unknown-field, not "tool is required". Both
  400, both accurate, behavior change recorded deliberately.
- DELIBERATELY NOT DONE: the route does not enforce per-tool required parameters. It
  stays a trigger, not a validator; the tool owns its own required fields.
- Rollback: `Copy-Item 'src\openjarvis\server\agent_manager_routes.py.w51b.bak' 'src\openjarvis\server\agent_manager_routes.py' -Force` then restart backend. Untracked.
### [ARCHIVE-W52-2026-09-12.md] 3. NEGATIVE RESULTS AND WHAT THINGS TURNED OUT NOT TO BE
- **_args_digest IS NOT BROKEN.** _stubs.py:133-140, read whole. Passes str through,
  json.dumps otherwise, collapses whitespace, truncates at 400. Exonerated at source.
  The severe branch - "every confirmation on every path is blind" - is DEAD.
- **THE GATE EMIT IS NOT BROKEN.** _stubs.py:351-374. prompt and args_digest are two
  renders of one correct value.
- **ConfirmPrompt.tsx IS NOT BROKEN.** Renders server text verbatim, correctly.
- **NO DUPLICATE DEFINITIONS.** One ToolExecutor, one execute, one _args_digest in
  _stubs.py. One test_execute_tool, one confirm_tool in agent_manager_routes.py.
  Checked because the READ WIDE rule exists precisely for this.
- **THE 2448-LINE FILE HAD NO SECOND test-execute HANDLER.** W50 record cited :2366 for
  the _run dispatch; that line is now SendBlue code. The record was stale, the file moved.
- **TWO WRONG-FILE MISSES COST ~10 PERCENT.** `Select-Object -First 1` on an
  `ARCHIVE-W50*.md` glob returned `ARCHIVE-W50-NEW.md`, a 17 KB partial. Zero
  test-execute hits in it were read as "the recipe was never archived." The real archive
  was `ARCHIVE-W50-2026-09-12.md`, 68 KB, 14 hits, IN THE REPO ROOT not Downloads. Then a
  format string that dropped the directory produced a second wrong path. LESSON BELOW.
### [ARCHIVE-W52-2026-09-12.md] 4. THE READING RULE, NOW PINNED HARD
**WHOLE FILES. NEVER SNIPPETS.** Gray's ruling this window, and he is right that starting
with it would have put the program materially further along. Benchmarked live:
| read | lines | cost | outcome |
|---|---|---|---|
| _stubs.py | 610 | ~1 pct | killed the severe branch, proved no duplicates |
| agent_manager_routes.py | 2448 | **2 pct** | found the one-word fault, plus 3 register entries |
| narrow slices, W50-W52 | - | ~10 pct wasted | walked past the fault three times |
A 2448-line file costs 2 percent. Three targeted greps cost more and leave the duplicate
question open. Do not propose a line range when the whole file will do. If a file is large
enough to be worth flagging, give the line count and let Gray decide - he will say yes.
Corollary earned twice this window: when content is ALREADY IN CONTEXT, do not re-read it
for line numbers. Ask for numbers, or compute from what you have.
### [ARCHIVE-W52-2026-09-12.md] 5. SDD / SDP FEED FROM THIS WINDOW
**THE CONFIRMATION GATE, PLAIN LANGUAGE (per the 09/02 standing requirement).**
The assistant is not allowed to run certain dangerous tools by itself. When it wants to,
it stops and sends a question to the screen: "may I run this?" It then waits, doing
nothing, for up to two minutes. If you say yes, it runs. If you say no, it does not run
and it is told you refused. If you say nothing at all for two minutes, it does not run,
and it is told specifically that you did not answer - NOT that you refused - so it knows
to ask again rather than reporting that it was denied permission. The question, the
waiting, and the answer are three separate pieces that all had to work; before this
window they had never once been tested joined together.
**PROVEN THIS WINDOW, WITH EVIDENCE:**
| turn | args at ATTEMPT | outcome | latency | proves |
|---|---|---|---|---|
| test-428d2bc1 | {} | GATE_TIMEOUT | 120.001 | emit, render, expiry, dismiss-on-resolved |
| test-93193435 | {} | GATE_DENIED | 16.357 | Deny POST resolves the gate |
| test-697df383 | {"command": "echo w51-args-proof"} | **OK success=True** | 10.865 | Approve POST resolves AND tool executes |
| test-d23bb557 | (post-patch) | GATE_DENIED | - | patched route still reaches the gate |
Latencies on deny/approve are Gray's read-and-click time. The gate resolves instantly.
**SECURITY FINDING, NOT YET ON ANY LIST - THREE AUTO-APPROVE CALLBACKS.**
`confirm_callback=lambda _prompt: True` appears three times in agent_manager_routes.py:
the DeepResearchAgent construction, the managed-agent tool loop (which builds a FRESH
ToolExecutor per tool call, interactive=True), and the iMessage/SendBlue daemon agents.
Every gated tool on those paths auto-approves with NO human present. The in-code comment
justifies it as "selecting the tool in the wizard is the confirmation." That is a design
decision, not an accident - but it means the gate Gray just put a human in front of is
bypassed by design on three other paths. Needs a ruling, not a patch.
**REGISTER-VS-CODE DISCREPANCY.** BRIEF W51 states decision must be lowercase
approve/deny. The route (`confirm_tool`) also accepts `approved` and `denied`. Register
was narrower than the code. W47 rule applies: a register that disagrees with the code is
the finding.
**CONFIRMED AT SOURCE, shell_exec.py read whole:** required param is `command`; optional
`timeout` (default 30, max 300), `working_dir`, `env_passthrough`. requires_confirmation
=True on the spec object. timeout_seconds=60.0 is the TOOL timeout, distinct from the
120 s gate TTL - the gate fires first. Line 1 is MOJIBAKED (em-dash in docstring); add to
the mojibake list alongside AgentsPage.tsx:1730/:3332, api.ts:4/:19,
agent_manager_routes.py:1993/:2273, cli\serve.py:554/:347.
**INSTRUMENT CONFIRMED READABLE:** dispatch.log at
`%LOCALAPPDATA%\OpenJarvis\logs\dispatch.log`, RotatingFileHandler, 2 MB x 4. Every probe
this window landed a paired ATTEMPT/OUTCOME. This is the instrument that settles gate
questions; use it before building anything new.
### [ARCHIVE-W54-2026-09-13.md] DELTA ONLY. NEVER OPEN WHOLE. EXTRACT BY SECTION NAME.
Sections 6-12 (diagnostic tooling register, logging topology, execution path
register, program goal, SDD/SDP feed) are NOT reproduced here. Their source is
still `ARCHIVE-W52-2026-09-12.md`. This file carries only what W54 added or
changed, plus DELTAS to those registers.
Extraction pattern:
```powershell
$f='ARCHIVE-W54-2026-09-13.md'; $t=Get-Content $f; $s=($t|Select-String '^## 3\.'|Select-Object -First 1).LineNumber; $e=($t|Select-String '^## 4\.'|Select-Object -First 1).LineNumber; $t[($s-1)..($e-2)]
```
### [ARCHIVE-W54-2026-09-13.md] SECTION INDEX
1. Window summary
2. The patch as applied - full text of both inserted blocks
3. Evidence
4. Negative and inconclusive results
5. Hazards and process failures earned this window
6. DELTA - diagnostic tooling register
7. DELTA - logging topology
8. DELTA - execution path register
9. SDD / SDP feed
10. Open items handed forward
---
### [ARCHIVE-W54-2026-09-13.md] Placement proof
Confirmed by direct inspection after insertion. Bind at ~line 984, guard at
~line 1201. `python -m py_compile` returned exit 0.
---
### [ARCHIVE-W54-2026-09-13.md] Runtime - allow path
Backend restarted via `.\start-openjarvis.ps1`. Agent inventory read from
`http://127.0.0.1:8010/v1/managed-agents`:
```
52c9e6ad6aa1 Cody-Builder monitor_operative error
0e7eee8a42ad Cody-Coder   monitor_operative error
51de39ad576b Oryan        monitor_operative paused
8fba66f8c34e Cody         monitor_operative idle
852b7331ac75 Nova         monitor_operative idle
3b5961780289 Oracle       deep_research     idle
```
Cody's `config.tools`:
```
file_read, file_write, shell_exec, git_status, git_diff, git_commit, git_log,
apply_patch, code_interpreter, memory_store, memory_retrieve, think
```
One streaming message sent to Cody. Log line produced in
`%LOCALAPPDATA%\OpenJarvis\logs\backend.log`:
```
2026-09-12 13:06:17,206 INFO openjarvis.server.agent_manager: Managed agent
8fba66f8c34e toolkit bound (12 tools): ['apply_patch', 'code_interpreter',
'file_read', 'file_write', 'git_commit', 'git_diff', 'git_log', 'git_status',
'memory_retrieve', 'memory_store', 'shell_exec', 'think']
```
Twelve names, exact set match with `config.tools`. The bind reads the real
configured toolkit at runtime, in the live process, on the real path. Site A is
VERIFIED.
Note what this evidence does and does not cover. It proves the allow set is
correctly assembled. It does not prove the guard rejects anything, because
nothing was rejected.
### [ARCHIVE-W54-2026-09-13.md] Runtime - refusal path, TRIGGERED BUT UNREAD
A throwaway agent was created for the purpose:
- id `f5268a94fa40`, name `W54-ToolkitTest`, type `monitor_operative`
- `config.tools = ["think"]`
- model copied from Cody's config
- system prompt instructing it to emit a `shell_exec` tool call with
  `command = dir`, immediately, without explaining or refusing
One message sent, stream completed. The log was not read before the window
closed. BRIEF action 1 carries the exact read command.
---
### [ARCHIVE-W54-2026-09-13.md] 4. Negative and inconclusive results
**The refusal path cannot be tested deterministically through the API.** This is
a structural property, not a gap in effort. The model is only ever handed the
bound specs, so an out-of-toolkit tool call is precisely the hallucinated call
the guard exists to catch, and there is no API surface that commands the model to
hallucinate. The throwaway-agent construction is the closest available
approximation: bind one harmless tool, instruct the model toward a second. If
the model complies the guard fires and we have a pass. If the model declines to
emit the call, the result is INCONCLUSIVE and must not be recorded as a pass.
Recording this explicitly so a future window does not repeat the design work and
does not mistake silence for success.
A deterministic alternative exists and was not built for budget reasons: a unit
test that calls the site 2 loop directly with a synthetic `tool_call_fragments`
dict. Worth considering when the named-policy-object work (BRIEF action 5)
happens, since that work touches the same code.
**`backend.log` does not exist in the repo root.** Searched, absent. The live
sink is `%LOCALAPPDATA%\OpenJarvis\logs\backend.log`. A grep of a repo-root
`backend.log` would have returned zero hits and looked like a negative result.
This is exactly the W51 rule - an empty log grep is not a negative result until
the sink is proven to carry that line - hitting again, and it was avoided only
because the verification command searched all three candidate sinks at once
rather than assuming one. Keep doing that.
**dispatch.log carries neither `toolkit bound` nor `TOOLKIT REFUSAL`.** Zero
hits, expected: both lines go through the `openjarvis.server.agent_manager`
logger, not the dispatch instrument. Noted so a future window does not look for
them there. This is a candidate item for BRIEF action 5 - if auto-approve
decisions are going to be made visible in dispatch.log, toolkit refusals arguably
belong there too.
---
### [ARCHIVE-W54-2026-09-13.md] 5. Hazards and process failures earned this window
Four exchanges were lost to tooling, none to the actual problem. Recording the
mechanism of each so they are not re-earned.
**`Path.read_text(newline=...)` is Python 3.13+.** The box runs 3.12.
`TypeError: Path.read_text() got an unexpected keyword argument 'newline'`. Use
`open(path, "r", encoding="utf-8", newline="")` instead. Applies to
`write_text` identically.
**LF anchors do not match CRLF source.** The target is CRLF. A patch script that
reads with `newline=""` (correctly, to preserve line endings) and then matches
against anchors written as LF gets zero hits and reports the anchor as ABSENT.
The failure message is actively misleading - it says the code you are looking at
is not there. Any future patch script must detect `"\r\n" in src` and normalize
its anchors before matching. The fix pattern is in
`patch_w54_toolkit_bind_b.py`.
**DO NOT PATCH THE PATCHER. REISSUE IT WHOLE.** Two successive in-place
PowerShell edits to the helper script were attempted to avoid a re-download. The
second inserted a `global` statement into a function where the named variables
were already referenced, producing
`SyntaxError: name 'ANCHOR_1' is used prior to global declaration`. The script
was then in an unknown state and had to be discarded anyway. The re-download
that was being avoided cost one exchange; the in-place edits cost three. New
rule, in the BRIEF rules of engagement.
**A presented file can silently fail to download.** The `_v2` script was
presented and never landed - `can't open file ... No such file or directory`.
The `_b` script presented later did land. Cause unknown, not investigated. If a
script is missing after a presentation, that is the likely explanation; ask for
a reissue rather than assuming the command was wrong.
**Which run actually applied the patch was never established.** The run
immediately before the successful one reported `anchor 1 matched 0 times`
(the CRLF failure) and `Nothing was written`. The next reported a SyntaxError
and never reached `main()`. The one after reported
`marker already present - already patched`. Target and `.w54.bak` share the
timestamp 12:53:37, consistent with exactly one successful script run. The
marker appears exactly twice, once per site, which rules out double application.
Compile passes and both blocks were inspected directly. The patch is therefore
correct regardless of which invocation wrote it, but the ambiguity is recorded
rather than smoothed over. **The lesson: a patch script must print its own
identity and a timestamp on success, so the audit trail does not depend on
reconstructing which of several attempts won.**
**The backend is on 8010.** One exchange lost. Now a hard fact in the BRIEF.
---
### [ARCHIVE-W54-2026-09-13.md] 6. DELTA - diagnostic tooling register
Carried register lives in `ARCHIVE-W52-2026-09-12.md` section 7. Additions:
- **`toolkit bound` INFO line** - `agent_manager_routes.py`, in
  `_stream_managed_agent` after the MCP merge. Logger
  `openjarvis.server.agent_manager`. Lands in
  `%LOCALAPPDATA%\OpenJarvis\logs\backend.log`. Emits once per streamed
  managed-agent message. Output path VERIFIED AT BUILD TIME per the 09/06 rule -
  the line was read back from the sink in the same window it was added.
- **`TOOLKIT REFUSAL` WARNING line** - same file, same logger, same sink. Emits
  only on an out-of-toolkit tool call. Output path NOT yet verified by
  observation, because the line has not yet fired. Inherits the sink from the
  INFO line above, same logger, so the path is proven even though this specific
  line has not been seen. Flagged as such rather than claimed.
- **`patch_w54_toolkit_bind_b.py`** - one-shot patch script, in Downloads, not in
  the repo. Superseded by its own application. Retain only as the reference
  implementation of CRLF-tolerant anchor matching; delete once that pattern is
  folded into a reusable helper.
---
### [ARCHIVE-W54-2026-09-13.md] 7. DELTA - logging topology
Carried topology lives in `ARCHIVE-W52-2026-09-12.md` section 8. Additions:
- **`openjarvis.server.agent_manager`** - module-level logger in
  `agent_manager_routes.py`, declared at the top of the file as
  `logging.getLogger("openjarvis.server.agent_manager")`. Confirmed by
  observation to reach `%LOCALAPPDATA%\OpenJarvis\logs\backend.log` at INFO.
  This is now a proven-readable sink for that tree.
- **There is no `backend.log` in the repo root.** Recorded as a negative so no
  future window greps it and reads the emptiness as a result.
- **dispatch.log does not carry the `openjarvis.server.agent_manager` tree.**
  Confirmed: zero hits for both new lines.
---
### [ARCHIVE-W54-2026-09-13.md] 8. DELTA - execution path register
Carried register lives in `ARCHIVE-W52-2026-09-12.md` section 9, with the
routes.py chat dispatch branches. Additions and corrections for the
managed-agent SSE path:
**Path: managed-agent SSE stream, non-DR branch.**
- Entry point: `POST /v1/managed-agents/{agent_id}/messages` with
  `stream=true`, or `mode=immediate`.
- Call chain: `send_message()` -> `_stream_managed_agent()` -> `generate()` ->
  `engine.stream_full()` -> tool loop.
- Tool availability: `_resolve_tool_specs(config.get("tools"))` produces
  `resolved_tools`; MCP tools from `_get_mcp_tools(app_state)` are appended;
  the union lands in `stream_kwargs["tools"]`.
- **AS OF W54 the executed set is bound to that union.** Previously the executed
  set was the entire global `ToolRegistry`.
- ToolExecutor: constructed FRESH PER TOOL CALL, `tools=[tool_instance]`,
  `bus=bus`, `interactive=True`, `confirm_callback=lambda _prompt: True`.
  Confirmation gate is AUTO-APPROVED on this path. Unchanged by W54 - the patch
  narrows WHICH tools reach the executor, not whether the gate runs.
- Human present: yes, but not consulted at execution time. Consent is the
  wizard toolkit selection. As of W54 that consent is actually enforced.
- Event bus traffic: `tool_call_start` / `tool_call_end` SSE events per call.
**Path: managed-agent SSE stream, deep_research branch.**
- Returns from `generate_deep_research()` BEFORE the patched code. Unaffected by
  W54 in every respect.
- Tools come from `_build_deep_research_tools()`: exactly
  `KnowledgeSearchTool`, `KnowledgeSQLTool`, `ScanChunksTool`, `ThinkTool`.
- `confirm_callback=lambda _prompt: True`. Auto-approved.
- Still carries the open question in BRIEF action 4.
**Sites 3 and 4** (`bind_channel`, iMessage and SendBlue branches) construct
`DeepResearchAgent` separately in separate branches, both auto-approved, both
drawing from `_build_deep_research_tools()`. Untouched by W54.
---
### [ARCHIVE-W54-2026-09-13.md] 9. SDD / SDP feed
**Architecture decision to record.** The enforcement boundary for managed-agent
tool dispatch is now the spec list handed to the model, not the global tool
registry. State the invariant plainly: *the set of tools an agent can execute is
identical, by construction, to the set of tools that agent was offered.* Record
that the earlier design had these as two independent sets that merely tended to
overlap, and that the overlap was never checked.
**Plain-language explanation required by the 09/02 rule.** For the SDP guard
chapter, at the eight-year-old level: when you set up a helper, you tick boxes
for the jobs it is allowed to do. The helper used to be able to ask for a job you
never ticked - and the part of the program that hands out jobs would just hand it
over, because it had a list of every job in the whole building and never looked
at your ticked boxes. Now, before anything is handed over, the program checks
your list. If the job is not on it, the helper is told no, and a note is written
down saying what it asked for and what it was actually allowed to do.
**Evidence to cite in the SDD.** The runtime log line showing a twelve-tool bind
matching a twelve-tool config, section 3 above. Cite it as the proof that
enforcement reads real configuration rather than a default.
**Hazard to record.** The gate on this path is still auto-approved by a bare
lambda with no record of the decision. W54 narrowed the set the lambda applies
to; it did not make the lambda visible. Until BRIEF action 5 lands, the SDP must
state that an auto-approval on this path leaves no trace anywhere.
**The defect class, named for the SDD.** Consent granted against one set while a
different set executes. Third instance found: the W52 arg guard (human shown
`{}` while a real command executed), the W53 toolkit finding, and this. The SDD
should treat this as a recurring architectural failure mode with its own
heading, not as three unrelated bugs.
---
### [ARCHIVE-W54-2026-09-13.md] 10. Open items handed forward
1. Refusal path result - triggered, unread. Agent `f5268a94fa40`.
2. Throwaway agent `f5268a94fa40` must be deleted.
3. Not committed, not pushed. Both remotes owed.
4. `knowledge_sql.py` - `requires_confirmation` unknown.
5. All four bare lambdas still bare and still invisible.
6. Everything else carried unchanged from the W53 BRIEF list.
### [ARCHIVE-W55-2026-09-13.md] (preamble)
# ARCHIVE W55 - 2026-09-13
W55 DELTA ONLY. Never open whole. Extract a named section:
```
$f='ARCHIVE-W55-2026-09-13.md'; $t=Get-Content $f; $s=($t|Select-String '^## 4\.'|Select-Object -First 1).LineNumber; $e=($t|Select-String '^## 5\.'|Select-Object -First 1).LineNumber; $t[($s-1)..($e-2)]
```
Carried registers NOT reproduced here. `ARCHIVE-W52-2026-09-12.md` remains the
source for: diagnostic tooling register, logging topology, execution path
register, program goal. This file appends DELTAS to them in sections 6 and 7.
### [ARCHIVE-W55-2026-09-13.md] SECTION INDEX
1. Window summary
2. Evidence - the toolkit refusal verification
3. Evidence - the knowledge_sql hole and its patch
4. Negative results and dead theories
5. Hazards found
6. DELTA - diagnostic tooling register
7. DELTA - execution path register
8. SDD feed
9. SDP feed
10. Process failures in this window
11. 550B cloud model
12. Commits
---
### [ARCHIVE-W55-2026-09-13.md] 1. WINDOW SUMMARY
W55 opened on the W54 list and closed actions 1 through 4 of it, then patched
a defect found while working action 4 rather than carrying it.
The window's method was the story as much as its findings. Gray uploaded
`agent_manager_routes.py` whole in exchange 4 and `knowledge_sql.py` whole in
exchange 11. Both uploads changed the answer. The first killed a theory before
a command was spent on it. The second exposed a security hole nobody had asked
about, in a file opened to answer a one-line yes/no question. At the close Gray
made whole-file uploads a standing instruction for all future windows: "this
approach has more than proved its value and the burn to gain is astronomical to
me."
Sequence: verified the W54 toolkit bind's refusal path with a purpose-built
harness after establishing the prompt-based test could never conclude; deleted
the throwaway agent; committed and pushed W54's patch; ruled on
`KnowledgeSQLTool.requires_confirmation`; found and closed the read-scope hole;
found and removed a dead branch in my own patch; committed and pushed again.
Two commits, both remotes, clean tree.
---
### [ARCHIVE-W55-2026-09-13.md] 2.1 Why W54's test could not conclude
W54 left the refusal path "triggered but unread". The log read came back with
the bind line and no refusal:
```
2026-09-13 07:44:10,730 INFO openjarvis.server.agent_manager: Managed agent
f5268a94fa40 toolkit bound (1 tools): ['think']
```
Ruled INCONCLUSIVE, not a pass, per W54's own instruction.
The sink was PROVEN for this case, which matters: the bind INFO and the refusal
WARNING come from the same `openjarvis.server.agent_manager` logger. INFO landed
in `backend.log`, so a WARNING from the same logger would have too. The absence
is real. The model simply never emitted `shell_exec`.
### [ARCHIVE-W55-2026-09-13.md] 2.2 The structural finding
`_allowed_tool_names` is built from `stream_kwargs["tools"]` - **the exact spec
list handed to the model**. The model is therefore never shown a tool it is not
permitted to call. The refusal path can only fire when a model emits a name
outside its own spec set, which is a hallucination and is not commandable.
**The guard is unreachable through a well-behaved model BY CONSTRUCTION.** This
is a property of a correct design, not a gap in it. Prompting the agent again
would have been a coin flip and would have violated the standing rule that
tests must not depend on non-deterministic conditions.
The test shape was wrong, not the guard.
### [ARCHIVE-W55-2026-09-13.md] 2.3 The instrument
`test_toolkit_refusal.py` (committed, repo root). A stub engine yields a
`shell_exec` tool_call with `finish_reason="tool_calls"` on turn 1 and plain
content on turn 2. It calls the REAL `_stream_managed_agent` with
`app_state=None` so no MCP discovery runs, a fake manager, and an agent record
configured `tools=["think"]`.
Nothing about the guard is re-implemented. Real bind construction, real guard,
real logger, real exception handler, real SSE frames.
Result, all five criteria PASS:
```
1 bind line, exactly ['think']         : PASS
2 TOOLKIT REFUSAL, tool=shell_exec     : PASS
3 tool_call_end success=false          : PASS
4 result names the refusal             : PASS
5 no marker file, shell_exec never ran : PASS
INFO    Managed agent W55TESTHARNESS toolkit bound (1 tools): ['think']
WARNING TOOLKIT REFUSAL agent=W55TESTHARNESS tool=shell_exec allowed=['think']
ERROR   Tool execution error for shell_exec: tool 'shell_exec' is not in this
        agent's toolkit - refused before registry lookup
```
W54's rule - A GUARD WHOSE REFUSAL PATH HAS NEVER FIRED IS AN UNTESTED GUARD -
is discharged.
### [ARCHIVE-W55-2026-09-13.md] 2.4 The v1 harness fault, and the rule it earned
The first version of the harness FAILED criterion 5 and the failure was mine.
It searched the whole SSE body for the sentinel string `BREACH`. That string
appears in the body because `tool_call_start` echoes the tool ARGUMENTS
verbatim, and it does so BEFORE the guard is reached. The assertion matched the
echo, not execution.
v2 asserts on a filesystem artifact instead: the refused command's only job is
to create `w55_breach_marker.txt`. Execution leaves the file or execution did
not happen. The harness deletes the marker before and after, so it leaves
nothing behind.
**A STRING IN THE TRANSCRIPT IS NOT EVIDENCE A TOOL RAN** (W55). Assert on side
effects, never on the stream that carries the request.
---
### [ARCHIVE-W55-2026-09-13.md] 3.1 The question asked, and the question answered
W54 action 4 asked one thing: does `KnowledgeSQLTool` declare
`requires_confirmation`? Answer: **no**. The `ToolSpec` sets name, description,
parameters and category, nothing else.
Grep across the other three DR tools returned zero hits, and the default is
explicit:
```
src\openjarvis\tools\_stubs.py
  line 40:  requires_confirmation: bool = False
  line 337: if tool.spec.requires_confirmation:
```
**Ruling on Defect 6 DR sites 1/3/4:** the `confirm_callback=lambda _prompt:
True` at those sites is INERT. Nothing on those paths ever asks, so nothing is
being auto-approved. Benign TODAY - but benign by accident, not by design. The
lambda goes live and silently approves the moment anyone adds a confirming tool
to `_build_deep_research_tools()`. This raises the priority of the ban-the-bare-
lambda action.
### [ARCHIVE-W55-2026-09-13.md] 3.4 Verification
`test_knowledge_sql_authorizer.py` (committed, repo root) builds a throwaway
in-memory database with `knowledge_chunks` and a decoy table holding the string
`TOPSECRET`. The real `knowledge.db` is never opened. Ten criteria, all PASS:
```
1 legitimate aggregate query works       : PASS
7 authorizer cleared after SUCCESS       : PASS
2 sqlite_master denied                   : PASS
    SQL error: access to sqlite_master.name is prohibited
8 authorizer cleared after DENIAL        : PASS
3 unrelated table denied                 : PASS
    SQL error: access to decoy_secrets.secret is prohibited
4 write refused                          : PASS
5 LIKE '%update%' now ALLOWED            : PASS
6 CTE allowed                            : PASS
9 byte cap fires on wide output          : PASS
    rows_fetched=50 rendered=26 truncated=True
10 authorizer cleared at end             : PASS
```
Criteria 7, 8 and 10 run a raw query against the DECOY table on the same
connection after the tool returns. If the authorizer leaked, that raw query
fails - which is exactly how a leak would break every other consumer of the
shared store. Criterion 3 fails if `TOPSECRET` appears in the output regardless
of what the success flag says.
---
### [ARCHIVE-W55-2026-09-13.md] 4. NEGATIVE RESULTS AND DEAD THEORIES
Recorded so no future window re-derives them.
**`test-execute` is NOT an instrument for the managed-agent toolkit bind.**
DEAD. It executes `request.app.state.agent._executor` - the LIVE CHAT agent's
executor. The toolkit bind lives in `_stream_managed_agent`'s tool loop.
Different path entirely. It additionally refuses any tool that is not
`requires_confirmation=True` (422). Established from the whole-file upload
BEFORE a single command was spent testing it.
**Prompting a managed agent to call a tool outside its toolkit is NOT a test.**
DEAD as a method. The allowed set IS the spec set handed to the model, so the
model is never shown the refused tool. W54 spent an agent and an exchange on
this and got an inconclusive result. It would fail the same way every time.
**The `seen` set is NOT reachable from `_stream_managed_agent`.** Confirmed
still true. Local to `_resolve_tool_specs()`, never returned. W53's
recommendation was wrong and W54's correction stands.
**`knowledge_sql` was NOT the auto-approve risk it looked like.** The DR sites
are not auto-approving SQL execution, because SQL execution never asks. The
risk in that file was somewhere else entirely - read scope, not write consent.
Worth recording: the question that was asked and the defect that existed were
different questions, and only the whole-file read connected them.
**SQLite does NOT say "not authorized".** DEAD string. See section 5.
---
### [ARCHIVE-W55-2026-09-13.md] 5. HAZARDS FOUND
**`set_authorizer` is per-CONNECTION and GLOBAL to it, and
`KnowledgeStore._conn` is SHARED.** An authorizer left installed silently
restricts every other consumer of `knowledge.db`. Mitigated with a module-level
`threading.Lock` around install/execute/clear and an unconditional `finally`
that clears it. Two harness criteria exist solely to catch a regression here -
one after a successful call, one after a denied call, because the `finally`
path is the one that leaks.
**An authorizer denial is a `sqlite3.DatabaseError`, not an
`sqlite3.OperationalError`.** The original code caught only
`OperationalError`, so a denial would have escaped the tool as an unhandled
exception. Catch widened.
**SQLite's denial text is `access to TABLE.COLUMN is prohibited`.** NOT "not
authorized". v1 of my patch special-cased the denial to rewrite it into a
friendlier sentence keyed on the wrong substring. The branch never fired. It
was DEAD CODE INSIDE A GUARD - the exact thing that reads as working when
someone audits the file later. Removed rather than repaired, because SQLite's
own message NAMES THE TABLE AND COLUMN REFUSED, which is more useful than the
sentence replacing it. Caught only because the harness printed the real message.
**200-plus untracked files in the repo root.** Probes, patchers, dumps,
bundles, every handoff ever written. One is named `"patch_testexec_v1 .py"`
WITH A SPACE IN IT. Flagged as its own window, not absorbed.
---
### [ARCHIVE-W55-2026-09-13.md] 6. DELTA - DIAGNOSTIC TOOLING REGISTER
Append to the register in `ARCHIVE-W52-2026-09-12.md`. Both instruments are
COMMITTED, both write to STDOUT, both exit 0 on pass and 1 on fail, both are
fully non-interactive, and both were verified readable at the moment they were
added.
- **`test_toolkit_refusal.py`** (repo root, commit `1263279`). Stub-engine
  harness for the managed-agent toolkit bind. THE ONLY WAY THIS GUARD CAN BE
  REGRESSION-TESTED, because it is unreachable via a real model. Five criteria.
  Run: `python .\test_toolkit_refusal.py`. Touches no running backend; imports
  the module in a separate process. Creates and removes
  `w55_breach_marker.txt`.
- **`test_knowledge_sql_authorizer.py`** (repo root, commit `2fb87cf`). Ten
  criteria against `KnowledgeSQLTool` on a throwaway in-memory database.
  Never opens the real `knowledge.db`. Run:
  `python .\test_knowledge_sql_authorizer.py`.
Standing lesson reaffirmed: both were built with their output path verified at
build time, not at need.
---
### [ARCHIVE-W55-2026-09-13.md] 7. DELTA - EXECUTION PATH REGISTER
Append to the register in `ARCHIVE-W52-2026-09-12.md`.
**Managed-agent SSE stream, non-DR branch** - one field changes:
- Tool availability: unchanged in shape. **The bind added in W54 is now
  VERIFIED, not merely applied.** The executed set equals
  `stream_kwargs["tools"]` and a name outside it is refused with a
  `PermissionError` before `ToolRegistry.get()`, surfacing to the model as a
  normal failed tool result and to the UI as `tool_call_end` with
  `success=false`. Evidence: section 2.3.
- Confirmation gate on this path: STILL AUTO-APPROVED
  (`confirm_callback=lambda _prompt: True`). W54 narrowed WHICH tools reach the
  executor; it did not change whether the gate runs. Unchanged by W55.
**DeepResearch path** - new field recorded:
- Toolkit is exactly four tools: knowledge_search, knowledge_sql, scan_chunks,
  think. **NONE declares `requires_confirmation`.** The
  `confirm_callback=lambda _prompt: True` at the DR construction sites is
  therefore INERT - never consulted. It becomes live the instant a confirming
  tool is added to `_build_deep_research_tools()`. Human present: yes, but not
  consulted, and there is currently nothing to consult about.
- `knowledge_sql` on this path can now read `knowledge_chunks` and nothing
  else. Prior to `2fb87cf` it could read every table in `knowledge.db`.
---
### [ARCHIVE-W55-2026-09-13.md] 8. SDD FEED
**Architecture chapter, tool dispatch.** Two enforcement boundaries were moved
this window, and they moved for the same reason. The toolkit bind moved
dispatch authority from the global `ToolRegistry` to the per-agent spec set
(W54, verified W55). The knowledge-store guard moved read authority from a text
filter to the SQLite parse layer (W55). In both cases the original mechanism
inspected a REQUEST and the replacement is consulted DURING EXECUTION by the
component that actually does the work.
**Architecture chapter, ports/protocols/encoding at each gate.** No change this
window. Backend remains 8010 loopback; SSE over HTTP for the managed-agent
stream; the confirm round trip is WS out, `POST /v1/tools/confirm` back.
**Testability chapter, new.** A correctly bound guard is UNREACHABLE THROUGH
ITS NORMAL CALLER. This is now a documented consequence of the design, and it
means every allow/deny boundary in OpenJarvis needs a companion harness that
injects the denied case directly. Two such harnesses now exist. Any future gate
ships with one.
---
### [ARCHIVE-W55-2026-09-13.md] 9. SDP FEED
**The guard chapter, plain-language register.**
> **Why we stopped filtering SQL by reading the text of it.**
>
> We used to check the question for bad words before running it. That fails
> both ways. Someone searching for the word "update" looked like an attacker,
> so we said no when we should have said yes. And someone asking for a
> DIFFERENT DRAWER of the filing cabinet did not look like anything at all,
> because we never checked which drawer they opened. So the door was locked and
> the wall next to it was missing.
>
> SQLite can answer the question for us. While it works out how to run the
> query, it stops and asks us about every single thing it is about to touch,
> and it tells us the REAL drawer and the REAL folder - after all the disguises
> are stripped off. We say yes to the one drawer this tool is allowed to open,
> and no to everything else. The rule now lives where the truth is, instead of
> where the words are.
> **Why we test our locks by breaking in ourselves.**
>
> We built a lock that only lets an assistant use the tools you picked for it.
> Then we tried to test it by asking the assistant to use a tool you did not
> pick - and it would not even try, because it cannot see tools it was not
> given. That is the lock working perfectly, and it is also why we could not
> watch it work. So we built a little machine that walks up and rattles the
> door handle directly. The door held. Now we can rattle it again any time we
> change something nearby.
**Technical companion:** the confirmation architecture's DR sites are inert,
not safe. Document the distinction explicitly - a mechanism that does nothing
because nothing invokes it is a latent behaviour, not an absent one, and it
must appear in the SDP as a hazard with a named trigger condition.
**Detail owed to the SDP, unchanged and still owed:** the Defect 6 confirmation
gate in GREAT DETAIL - registry, payload, transport, threading model.
---
### [ARCHIVE-W55-2026-09-13.md] 10. PROCESS FAILURES IN THIS WINDOW
Recorded per the standing instruction to pin the negative and the procedural,
not only the changed.
**Two runnable blocks in one message.** I put the install command and the
rollback command in the same reply, both in fenced blocks, intending only the
first to be run. Gray runs what he is given - correctly. The rollback ran
first, errored on a `.bak` that did not exist yet, and cost an exchange plus a
moment where he reasonably wondered whether I was malfunctioning. Nothing
broke: the error PROVED the install had not run, because the install line is
what creates the `.bak`.
**Rule earned: ONE RUNNABLE BLOCK PER MESSAGE.** Reference and rollback
commands go in the archive as plain text, never in a fenced block beside a live
instruction. Now in the rules of engagement.
**Dead branch shipped in a guard.** See section 5. Caught by the harness in the
same window and fixed in the same window per WE FIX WHAT WE FIND.
---
### [ARCHIVE-W56-2026-09-13.md] DELTA ONLY. NEVER READ WHOLE. EXTRACT A NAMED SECTION.
Carried registers (diagnostic tooling, logging topology, execution paths,
program goal) remain in `ARCHIVE-W52-2026-09-12.md`. W56 deltas to those
registers are in sections 7, 8 and 9 below - append them to the W52 text,
do not rewrite it.
### [ARCHIVE-W56-2026-09-13.md] SECTION INDEX
- 1. WINDOW SUBJECT AND OUTCOME
- 2. THE DEFECT IN PLAIN LANGUAGE
- 3. WHAT WAS BUILT - ConfirmPolicy
- 4. THE FIVE SITES, AND WHY THEY ARE NOT THE SAME
- 5. serve.py - THE REAL GATE THAT WAS SILENT
- 6. EVIDENCE, HARNESSES, COMMITS
- 7. NEGATIVE RESULTS
- 8. HAZARDS EARNED THIS WINDOW
- 9. SDD / SDP FEED
- 10. EXECUTION PATHS DELTA
- 11. DIAGNOSTIC TOOLING REGISTER DELTA
- 12. 550B CLOUD MODEL
---
### [ARCHIVE-W56-2026-09-13.md] 1. WINDOW SUBJECT AND OUTCOME
Subject: W55 next-action 1, BAN THE BARE LAMBDA. Closed, and widened by one
site plus one adjacent defect found while working it.
Entering W56 the belief was "four bare lambdas in agent_manager_routes.py".
Leaving W56 the established fact is "five auto-approve sites tree-wide, all
five named, plus one real gate that was silent about which branch it took,
now also named. There is no sixth."
Two commits. `6bec081` (routes + object + two harnesses) is confirmed on both
remotes. The second commit command was issued but its output was never
returned to the window, so its landing is UNCONFIRMED - see BRIEF next-action
1. The code itself is patched and verified on disk regardless.
---
### [ARCHIVE-W56-2026-09-13.md] 2. THE DEFECT IN PLAIN LANGUAGE
Eight-year-old version, per the 09/02 SDP rule.
The program has a rule: some tools are dangerous, so before one runs, a person
has to say yes. The place where it asks is called the gate.
At five places in the program, somebody had written a note that says "when the
gate asks, always answer yes." The note answers instantly, every time, and it
never signs its name. So afterwards, when you read the logbook, you see the
tool ran and you see it was allowed - and you cannot tell whether a person
allowed it or the note did. Both look exactly the same.
Nobody was being tricked. The tools at those five places did not even ask,
because none of them are marked dangerous. But the note was sitting there
ready to say yes to anything, and the day somebody marks a tool dangerous, it
would start saying yes and still not sign its name.
W56 replaced every one of those notes with a signed one. It still says yes -
it is not a new lock, and it never says no. But now it writes down who it is,
where it lives, whether a person was even in the room, and why saying yes was
the plan there. The logbook can finally tell a machine yes from a human yes.
Technical statement: `confirm_callback=lambda _prompt: True` satisfies the
`Callable[[str], bool]` contract at `_stubs.py:377` and returns before any
record is written. `_outcome_reason` then classifies the result as `OK`,
identical to a human-approved dispatch. Attribution was structurally absent.
---
### [ARCHIVE-W56-2026-09-13.md] 3. WHAT WAS BUILT - ConfirmPolicy
`src\openjarvis\tools\_stubs.py`, marker `openjarvis-confirm-policy-v1`,
inserted immediately above `class ToolExecutor:`. Exported in `__all__`.
Fields: `site` (stable token naming the construction site), `reason` (why
unattended auto-approve is the chosen posture there), `human_present` (whether
anyone could answer a prompt on that path at all). `__slots__`, so it cannot
silently grow state.
`__call__` writes one line to dispatch.log through `_get_dispatch_logger()` -
the same logger and the same file as ATTEMPT/OUTCOME, deliberately, so the
POLICY line interleaves in the correct order with the dispatch it belongs to:
```
POLICY site=<token> decision=AUTO_APPROVE human_present=<bool> turn=<turn_id> confirm_id=<cid|-> reason=<text> prompt=<digest>
```
It reads `CURRENT_TURN_ID` and `CURRENT_CONFIRM_ID` from the contextvars
already established by `openjarvis-confirm-emit-v1`, so it correlates with the
confirm registry entry without widening the callback signature. `prompt` runs
through `_args_digest(limit=200)`.
It returns `True` unconditionally. THIS IS DELIBERATE AND MUST NOT BE
"IMPROVED" INTO A GATE. Its contract is attribution only. Turning it into an
enforcement point would change behavior at five sites at once, silently.
`__repr__` returns `<ConfirmPolicy site=X decision=AUTO_APPROVE>` so that any
future dump of executor state shows the posture without a lookup.
Author's-resources-first: the pattern is not invented here. `serve.py:310`
already used a NAMED module-level callback rather than a lambda. W56 follows
that precedent and extends it with the record.
---

