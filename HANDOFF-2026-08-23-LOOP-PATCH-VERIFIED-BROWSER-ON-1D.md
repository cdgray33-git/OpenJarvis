# HANDOFF - 2026-08-23 second window
# LOOP PATCH VERIFIED. CHAT DISPATCH HAS FOUR BRANCHES, NOT TWO.
# THE BROWSER IS ON PATH 1d BY DEFAULT - NO AGENT, NO TOOLS, NO GATE.

Supersedes `HANDOFF-2026-08-23-STALL-DIAGNOSED-LOOP-BLOCK-PATCHED.md` for state.
That file's section 4 claim that "the browser path is 1b" is SUPERSEDED - see section 3 below.
Its section 1 diagnosis stands and is now VERIFIED. Hazards register carried forward with changes.

**Three changes were made this window. All three are applied AND verified. Nothing is left
dangling. The next window starts clean.**

---

## 0. STANDING RULES FOR THE NEXT WINDOW

1. **TOKEN CONSERVATION MODE.** Short replies, minimal restating, one command at a time, no preambles.
2. **ALWAYS STATE SHELL AND HOST.** Default PowerShell on the Windows box. Anything for the Ubuntu
   ollama host (172.16.33.200) must be labeled or wrapped as a PowerShell ssh command.
3. **WORKING DIRECTORY IS FIXED: `PS C:\Users\Admin\OpenJarvis>`.** Every command must run correctly
   from there. If a command needs a different path, shell, or host, say so IN THE REQUEST, BEFORE it
   is run. When a file is delivered for download, state where it lands and give the command that
   already accounts for that location, in the same message.
4. **NO NON-ASCII SYMBOLS.** They render garbled on Gray's display.
5. **ALWAYS VERIFY. Never stack a second change on an unverified first one.** Held this window:
   routes.py patch verified alone before the probe was touched; probe v1 verified before v2.
6. **FINISH THE THING BEFORE STARTING THE NEXT.** No dangling processes.
7. **DESIGN TESTS TO BE NON-INTERACTIVE.** `ws_probe.py` remains the standing instrument.
8. Every handoff carries an SDD section, an SDP section, and an EXECUTION PATHS section.

---

## 1. THE HEADLINE

Two findings, in order of importance.

**FINDING A - the loop-block patch is VERIFIED.** `asyncio.to_thread` at `routes.py:162/:165` fixed
the event-loop block. Same instrument, same prompt, before and after:

| signal | 07:36 pre-patch | 08:58 post-patch |
|---|---|---|
| HTTP `/health` | 23 consecutive 10 s timeouts | 288 samples, 0 failed, mean 0.033 s |
| WS frames | zero, then 18 in a 7 ms burst | 14 delivered as emitted, mean lag 0.007 s |
| WS pong | 120 s timeout | 60 attempts, 0 failed, mean 0.031 s |

Verdict line: NO STALL REPRODUCED. Turn wall time 270 s, of which 240 s was two 120 s confirm TTLs
and roughly 30 s was real work. **Never quote the wall time of a gated turn as a performance number.**

**FINDING B - `POST /v1/chat/completions` has FOUR branches, and the browser default is the one
with no tools.** The prior handoff's "path 1a / 1b split" was an undercount. Actual dispatch:

```
:152  cloud model            -> _handle_stream        no agent, no tools     (call it 1e)
:157  stream + agent + bus + (tools OR agent) -> _handle_agent_stream        PATH 1b
:159  stream, predicate fails -> _handle_stream       no agent, no tools     PATH 1d
:162  non-stream, agent present -> _handle_agent      PATH 1a   (patched)
:165  non-stream, no agent      -> _handle_direct     PATH 1c   (patched)
```

`ChatArea.tsx:215` sends `agent: st.selectedAgentId || ''`. **Empty string is falsy, so with no agent
selected the predicate at :157 fails and the browser lands on 1d.** `lib\sse.ts` has no `tools` field
in its request interface at all (`:9 stream: true`, `:12 agent?: string`), so `tools` can never
satisfy that predicate from the browser. **The only route from the browser to 1b is a selected agent
id.**

---

## 2. WHAT CHANGED - THREE PATCHES, ALL VERIFIED

### 2.1 `routes.py` - verified, not changed this window
Applied last window, marker `openjarvis-offload-sync-handlers-v1`. Verified at 08:58 (section 1).
Comments now in place at `:163-167` and `:173-175` explaining the defect and naming
`stream_bridge.py:155` as the house idiom.

### 2.2 `ws_probe.py` v1 - `--stream` mode
`patch_ws_probe_stream_v1.py`, marker `openjarvis-ws-probe-stream-v1`, applied 09:11:18.
Nine replacements, all matched exactly once. Adds `--stream`, incremental SSE reading with
per-chunk arrival timestamps, an SSE STREAM report section, and a banner line naming the path.
**Also rewrote stale verdict prose** that still asserted the dead "PowerShell instrument artifact"
theory - the instrument was about to print a conclusion the evidence had already killed.

### 2.3 `ws_probe.py` v2 - response capture and `--prompt`
`patch_ws_probe_capture_v2.py`, marker `openjarvis-ws-probe-capture-v2`, applied 09:21:52.
Six replacements. Refuses to apply if v1 is absent. Adds: assembled response text written to
`ws_probe_last_response.txt` with a 600-char preview in the report, an explicit TOOL ACTIVITY
section stating presence or absence of tool frames, and `--prompt` to override the built-in prompt.

**Why v2 was necessary and is the method lesson of the window:** the 09:12 run reported 96 SSE
chunks, zero tool calls, and threw the text away. Three very different causes produce that identical
report - the model answering in prose, the model falsely claiming it ran the tool (Defect 1), or the
chain never offering tools. **A report that cannot separate its own hypotheses is not evidence.**

Guards on both patch scripts, all exercised: marker idempotency, prerequisite marker (v2), line-ending
detection with search-text translation, exactly-once verbatim match checked across ALL replacements
BEFORE any substitution (so partial application is impossible), temp-file compile before touching the
real file, timestamped `.bak`, post-write compile with self-restore, and a `--help` smoke run with
self-restore that also asserts the new flag is present.

---

## 3. THE EVIDENCE - AND A CORRECTION THAT MUST NOT BE LOST

**Two streaming probe runs measured the WRONG BRANCH.** 09:12:55 and 09:22:35 both sent
`"stream": true` with neither `tools` nor `agent`, so both fell through `:157` to `:159` and
exercised 1d, not 1b. I called the first one "1b clean" in-session. That was wrong and is corrected
here.

Both runs, identical shape:

| run | frames | SSE chunks | body bytes | tool frames | finish |
|---|---|---|---|---|---|
| 09:12 | 2 | 96 | 19,407 | none | stop |
| 09:22 | 2 | 101 | 20,467 | none | stop |

Response text captured on the second run:

> The model states it cannot execute shell commands or use tools like shell_exec, that it is a
> language model without the capability to execute code or access system resources, and offers to
> explain or write commands instead.

**This is CORRECT behavior, not a defect.** The model was asked to call a tool on a branch that
offers it none. It is NOT Defect 1 - it made no claim of having acted. Rule that out explicitly in
the record, because "asked for a tool call, got prose" is the exact surface signature of Defect 1 and
a future reader will pattern-match to it.

**What the 1d runs DO establish, and it is worth keeping:** transport on 1d is clean. Time to first
SSE chunk 2-8 ms, mean inter-chunk gap 0.029-0.030 s, 98-101 token-level chunks, heartbeat max
0.687 s with zero failures across 386 and 58 samples, pong max 0.028 s. This corroborates the
`:143-146` comment: 1d streams token-by-token, while the agent bridge word-splits a completed result.

**Evidence grade, per path, as of this window:**
- **1a NON-STREAMING AGENT: MEASURED, PATCHED, VERIFIED.** 08:58 run.
- **1c NON-STREAMING DIRECT: SHAPE-CONFIRMED, PATCHED, NOT MEASURED.** Unchanged from last window.
- **1d PLAIN ENGINE STREAM: MEASURED CLEAN.** Twice. No gate exists on it to test.
- **1b AGENT STREAM: STILL COMPLETELY UNTESTED.** Three windows have now believed otherwise.
- **1e CLOUD BYPASS: UNTESTED.** Noted at `:152`, no tools by construction.

---

## 4. NEXT ACTION - IN ORDER

1. **Confirm the falsy-empty-string reading against the server, not against my reading of it.**
   `request_body.agent` is `''` from the browser default. Read the Pydantic model for
   `ChatCompletionRequest` to confirm `agent` is not coerced to `None` or defaulted elsewhere, and
   confirm `tools` exists server-side even though the TS interface omits it.
2. **Add `--agent` to the probe** so it can set the field and actually reach 1b. This is probe v3.
   Keep the same guard pattern. **Do not skip this and hand-craft a curl - the probe is the
   instrument of record and every timing claim should come from it.**
3. **Run the probe against 1b with an agent id.** THIS is the run that answers 6e: does the confirm
   gate fire on the agent stream, and do `tool_confirm_request` / `tool_confirm_resolved` frames
   reach a client promptly while the turn is in flight.
4. **Only then** the 6e UI work. Mount site remains `ChatArea.tsx`, design call remains option (b),
   a new hook, `AgentsPage` untouched.

**Open design question that step 3 will force, and it is not a small one:** if the browser only
reaches a tool-capable path when an agent is selected, then either the gate is irrelevant to default
chat, or default chat should be tool-capable and currently is not. **That is a product decision, not
a bug fix.** Do not let it be settled implicitly by whatever the next patch happens to do.

**Do not write UI code until step 3 has produced a number.**

---

## 5. THE INSTRUMENT - `ws_probe.py`

In repo root. Now at v2. Args: `--host --port --model --deadline --chat-delay --chat-timeout
--stream --prompt`. Dependency: `websockets`.

Three measurement channels, and the design reason for each:
- **WS frames** - what the bus emitted and when, by internal timestamp versus receive time.
- **HTTP heartbeat** - whether the server was alive at all. Frame lag alone cannot tell a slow
  transport from a dead server. This channel is what cracked the 07:36 stall.
- **SSE chunk arrival** (stream mode) - whether the response body itself kept flowing.

**Known instrument limitation, worth fixing in v3:** the probe holds the socket until `--deadline`
even after the chat returns. The 09:12 run sat idle for 394 s after a 6 s turn. Add an early exit
once the turn completes and a grace period has passed. Cost this window: about six wasted minutes.

**`ws_probe_last_response.txt` is overwritten every run.** Copy it if a response matters.

---

## 6. STATE AT WINDOW CLOSE

- **Backend RUNNING and CURRENT.** Restarted this window at approximately 08:57 with the
  `routes.py` patch loaded. Port 8010, engine ollama, model `qwen3-coder:30b`, agent
  `native_openhands`. Logs: `C:\Users\Admin\AppData\Local\OpenJarvis\logs\backend.log`.
- **ROLLBACK POINTS, all three active:**
  - `Copy-Item 'src\openjarvis\server\routes.py.bak-20260823-081543' 'src\openjarvis\server\routes.py' -Force` (restart required)
  - `Copy-Item 'ws_probe.py.bak-20260823-091118' 'ws_probe.py' -Force` (pre-v1)
  - `Copy-Item 'ws_probe.py.bak-20260823-092152' 'ws_probe.py' -Force` (pre-v2, has v1)
- **No auto-approver alive.** The probe does not approve. Gate allowed to time out by design.
- **NEW FILES IN REPO ROOT:** `patch_ws_probe_stream_v1.py`, `patch_ws_probe_capture_v2.py`,
  `ws_probe_last_response.txt`. Add to the cleanup list alongside `ws_probe.py` and
  `patch_offload_sync_handlers.py`.
- 6c SATISFIED. 6d LIVE-PROVEN, CLOSED. 6e transport CLOSED on 1a and 1d. 6e backend emit APPLIED,
  timeout branch verified, approved/denied/reaped still UNPROVEN. **6e browser half OPEN, and the
  blocker is now understood: the browser default never reaches a tool-capable branch.**

---

## 7. PARKED OBSERVATIONS - NOTED, NOT CHASED

1. **Cold first inference 16.4 s** on the 08:58 run versus 2.3 s on later turns in the same run and
   2.8 s on both streaming runs. Almost certainly model load after restart. Not investigated.
2. **One 3.771 s `/health` sample** at t+3.229 on the 08:58 run, coincident with the chat POST, with
   a 4.778 s inter-sample gap. The following 287 samples were clean. Not a stall, but it is the one
   moment the loop is still tight, and it is the only blemish on an otherwise flat trace.
3. **`sse.ts` has no `tools` field.** Whether that is deliberate or an omission is unknown.
4. Dead `bus` lookup at `routes.py:172`, unreachable because `:162` returns first. Harmless.

---

## 8. EXECUTION PATHS REGISTER

Standing structure. Per path: entry point, call chain with file:line, which ToolExecutor instance
serves it and how it is constructed, gate status live / auto-approved / absent, event bus traffic,
whether a human is present.

**Paths 2-5 carry forward unchanged from `HANDOFF-2026-08-23-STALL-DIAGNOSED-LOOP-BLOCK-PATCHED.md`
section 8. PATH 1 is restated in full below because it changed materially.**

### PATH 1 - THE CHAT ROUTE, `POST /v1/chat/completions`, `server\routes.py:46`
Handler `chat_completions` (47-171). Agent off `request.app.state.agent` (:50); never calls
`JarvisSystem.ask()`. Bus A via `app.state.bus`. **Dispatch is a four-way branch on request body
contents - the CLIENT selects the path.**

- **1a NON-STREAMING AGENT** - `:162` -> `_handle_agent`, plain `def`, now wrapped in
  `asyncio.to_thread`. Executor built by the agent at `agents\_stubs.py:325`; `serve.py` passes no
  `tool_executor`. **Gate LIVE AND FULLY PROVEN.** REQUEST at `_stubs.py:294-306`, RESOLVED at
  `312-331`, both allowlisted at `ws_bridge.py:31-32`, both observed live. Human present only if a
  client answers; `ws_probe.py` deliberately does not. **VERIFIED clean 08:58.**
- **1b AGENT STREAM** - `:157` predicate `agent is not None and bus is not None and
  (request_body.tools or request_body.agent)` -> `:158 _handle_agent_stream` (:316) ->
  `create_agent_stream` -> `stream_bridge.py:155`, agent run via `asyncio.to_thread`. **Correct by
  construction, never had the loop defect. Gate presumed live, NEVER OBSERVED. Reachable from the
  browser only when an agent id is selected.**
- **1c NON-STREAMING DIRECT** - `:165` -> `_handle_direct`, plain `def`, synchronous engine calls at
  `:189/:199`. Patched alongside 1a. Gate ABSENT (no agent, no executor). Shape-confirmed only.
- **1d PLAIN ENGINE STREAM** - `:159` -> `_handle_stream` (:323), async generator, `engine.stream()`
  at `:389`. **No agent, no executor, no tools, GATE ABSENT.** Token-by-token output. **THIS IS WHAT
  THE BROWSER GETS BY DEFAULT** (`ChatArea.tsx:215` sends `agent: ''`). Emits `inference_start` and
  `inference_end` only. MEASURED CLEAN twice.
- **1e CLOUD BYPASS** - `:152`, `is_cloud_model(model)` -> `_handle_stream`. Deliberate: the agent
  path builds a plain OllamaEngine with no provider awareness, so a cloud model string would be
  POSTed to Ollama and 404. **Gate ABSENT. Cloud models are structurally tool-less on this route.**
  UNTESTED.

### FRONTEND CALL SHAPE - new sub-register, keep it
- `ChatArea.tsx:12` imports `streamChat`, sole importer. Call at `:208-215`.
- Body sent: `model: st.selectedModel`, `messages: apiMessages`, `stream: true`,
  `agent: st.selectedAgentId || ''`. **No `tools` key, ever.**
- `lib\sse.ts`: `:9 stream: true`, `:12 agent?: string`, POST at `:45`, body at `:51`.
- `:220` handles an `agent_turn_start` event name - the UI already anticipates agent events it
  cannot currently receive on the default path.

---

## 9. SDP FEED

**Defect 6 confirmation gate - GREAT DETAIL required, per standing instruction.**

- **The gate's browser-coverage problem is structural, not cosmetic, and the SDP must say so.** The
  prior framing was "the gate has zero browser presence," implying a missing dialog. The real
  statement is: **on the default browser request the gate cannot fire, because the request never
  reaches a branch that constructs a ToolExecutor.** A confirmation dialog added today would be
  unreachable code on the default path.
- **Record the dispatch predicate verbatim in the SDP**, with the falsy-empty-string consequence
  spelled out. `agent: st.selectedAgentId || ''` is a frontend idiom that silently changes which
  server branch runs. **This is a ports-and-protocols fact: the request body is the routing key.**
- **Add a "path selection" column to the gate table** alongside ports, protocols, encoding, and the
  thread-boundary column added last window. Per path record: what in the request selects it, is the
  entry point a coroutine, is the work synchronous, is there a thread boundary, is there an executor,
  is the gate live.
- **Concurrency model, carried and now verified:** 1a and 1c had no thread boundary and blocked the
  loop; 1b has one at `stream_bridge.py:155`; 1d is async throughout. The general rule stands: **in
  an async server a synchronous call is a global outage, not a local slowdown.**
- **Component-level guarantees do not survive composition** - the registry docstring claim from last
  window remains the best worked example. Keep it.
- **Confirm cost measured:** two cycles, 120.0 s each, 240 s of a 253 s turn (07:36) and of a 270 s
  turn (08:58). The N x 120 s hazard is confirmed live and is UNCHANGED by this window's work.
- **Instrument provenance:** every timing claim in this window comes from `ws_probe.py` runs at
  08:58:01, 09:12:55, and 09:22:35. Code claims come from direct reads of `routes.py`, `sse.ts`, and
  `ChatArea.tsx` on 08/23.

**Hazards register - additions and changes.**
- **RESOLVED AND VERIFIED:** blocking sync handlers on the event loop, `routes.py:162/:165`.
  Was HIGH and system-wide. Verified by control-on-both-sides comparison at 08:58.
- **NEW, HIGH:** the browser default request cannot reach a tool-capable branch. The confirmation
  gate, the tool executor, and every tool safety property are absent from default browser chat.
  **This subsumes and reframes the previous "gate has no browser presence" entry.**
- **NEW, MEDIUM:** `agent: st.selectedAgentId || ''` converts "no selection" into a falsy value that
  silently selects a different server branch. No log, no error, no user-visible difference except
  that tools stop existing.
- **NEW, LOW:** `ws_probe.py` holds its socket to `--deadline` after the turn ends. Instrument-only.
- **CARRIED, MEDIUM:** `_handle_direct` now called positionally where it was called by keyword. A
  future signature change will silently mis-bind. The AST guard lives in the patch script, not at
  runtime.
- **CARRIED, STILL THE LARGEST OPEN SAFETY GAP:** `mailbox_move_to_trash` and
  `mailbox_empty_folder` have NO `requires_confirmation` at spec level. Only `agent_tools.py:289`,
  `git_tool.py:283`, `shell_exec.py:71` declare confirmation. **The gate is proven on 1a and does not
  protect the destructive tools.**
- **CARRIED:** unanswered confirm costs N x 120 s, measured at N=2 in a single turn.
- **CARRIED:** `useAgentEvents` has no replay on reconnect; expired entries are popped.
- **CARRIED:** bare `except Exception` at `api_routes.py:946` logs at debug only.
- **CARRIED:** reaped-None branch of the resolved emit is written but untested.
- **DOWNGRADED:** possible UTF-8/cp1252 hazard on `.tsx` reads - `-Encoding UTF8` read of
  `ChatArea.tsx` was clean this window. Keep the practice, lower the concern.

---

## 10. SDD SECTION

Gray is building a detailed System Design Document covering all OpenJarvis work to date. **Gray
explicitly pinned this window's branch topology for the final document, to be written up with full
explanations.** This window feeds it:

- **The architecture chapter needs a REQUEST DISPATCH section, and it is more than a diagram.** One
  route resolves to five materially different execution paths with different concurrency properties,
  different tool availability, and different safety properties, **selected by the contents of the
  request body**. That is an architectural fact of the first order, not an implementation detail.
- **The general lesson, and it is the transferable one: when a branch predicate reads the request
  body, the client chooses the code path.** Any claim of the form "we tested the browser path" is
  only as strong as the claim about what the browser sends. Two runs measured the wrong branch this
  window before anyone checked the frontend. **State this as a testing principle in the SDD: name the
  path AND the request shape that selects it, in the same sentence, every time.**
- **The concurrency model section from last window stands and is now verified**, with the before/after
  table in section 1 as its evidence.
- **Safety inversions, restated again - the set has changed because the third was wrong twice:**
  1. a proven gate that does not cover the destructive tools;
  2. a proven gate on a path the browser does not take by default;
  3. a correct event stream that was rendered unobservable by a defect in an unrelated layer
     (diagnosed, fixed, verified).
  **Inversion 2 is the one that grew this window.** It was "no browser UI"; it is now "no browser
  path."
- **Performance chapter:** 1d streams token-by-token with a 2-8 ms time to first chunk. 1b word-splits
  a completed result and cannot stream live, per the comment at `:143-146`. **These are different
  user-visible latency characters on the same route, and selecting an agent silently switches
  between them.** That belongs in the SDD as a user-facing consequence of an architectural choice.
- **Frontend event consumption** unchanged as an SDD area: `ChatArea.tsx` is the pane owner, and the
  decision to fork rather than modify `useAgentEvents` stands on blast radius plus incompatible hook
  semantics.

**Standing instruction:** every handoff from here carries an SDD section, and every window feeds it.

---

## 11. METHOD LESSONS

1. **Verify the branch, not just the endpoint.** Three windows believed the browser used 1b. The
   route was right, the branch was wrong, and nothing in a URL or a status code would ever have shown
   it. **Cost: two probe runs and a wrong claim I made in-session and had to retract.**
2. **A report that cannot separate its own hypotheses is not evidence.** The 09:12 report was
   internally consistent, well-formatted, and could not distinguish three causes with completely
   different consequences. One more captured field settled it in a single re-run.
3. **Correct the record in place, loudly.** I called the 09:12 run "1b clean" and it was 1d. The
   correction is in section 3 with the reason, not quietly fixed, because a future reader who finds
   only the fixed version learns nothing about how the error happened.
4. **Read the caller before concluding about the callee.** The dispatch predicate at `:157` was
   readable at any point in the last three windows. What made it matter was reading `sse.ts` and
   `ChatArea.tsx` and finding out what the client actually sends.
5. **Guard clauses paid for themselves a third time.** Nine and six replacements respectively, all
   checked for exactly-once matching BEFORE any substitution, so a partial application was
   structurally impossible. Neither patch needed its rollback.
6. **The instrument is a deliverable and needs the same rigor as the system.** Two of the three
   changes this window were to the probe: one added a capability, one fixed a report that was about
   to state a dead theory as a conclusion. **An instrument that lies is worse than no instrument.**
