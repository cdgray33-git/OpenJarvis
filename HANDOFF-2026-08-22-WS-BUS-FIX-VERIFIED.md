# HANDOFF - 2026-08-22 morning window
# THE WS-BRIDGE BUS FIX IS APPLIED AND RUNTIME-VERIFIED. THE CHAT PATH IS NO LONGER DARK.
# ONE ITEM OPEN: the approve half of 6e. Fully staged, not yet run.

Supersedes `HANDOFF-2026-08-21-6d-LIVE-PROVEN-BUS-SPLIT.md`.

One patch applied this window. It is verified at both the file level and the runtime level.
Nothing is left unverified. Nothing is dangling.

---

## 0. STANDING RULES FOR THE NEXT WINDOW

Read these before the first command.

1. **TOKEN CONSERVATION MODE.** Short replies, minimal restating, one command at a time, no long preambles. Gray is budget-constrained within a session.
2. **ALWAYS STATE SHELL AND HOST.** Default is PowerShell on the Windows box. Anything for the Ubuntu ollama host (172.16.33.200) must be labeled or wrapped as a PowerShell ssh command.
3. **WORKING DIRECTORY IS FIXED: `PS C:\Users\Admin\OpenJarvis>`.** Every command must run correctly from there. If a command needs a different path, shell, or host, say so IN THE REQUEST, BEFORE it is run. When a file is delivered for download, state where it lands and give the command that already accounts for that location.
4. **NO NON-ASCII SYMBOLS.** They render garbled on Gray's display.
5. **ALWAYS VERIFY. Never stack a second change on an unverified first one.** Verify-first is not a close call.
6. **FINISH THE THING BEFORE STARTING THE NEXT.** No dangling processes. Do not propose the next patch while the current one is unverified.
7. **TRACK INTERACTION COUNT, flag at 15, then produce a handoff.**
8. Every handoff carries an SDD section, an SDP section, and an EXECUTION PATHS section. Sections 8, 9 and 10 below.

---

## 1. WHAT CHANGED THIS WINDOW

The one-line WS-bridge fix spec'd on 08/21 is **APPLIED, FILE-VERIFIED, AND RUNTIME-VERIFIED**.

**File:** `src\openjarvis\server\api_routes.py`, line 944.

**Before:**
```python
ws_router = create_ws_router(get_event_bus())
```

**After:**
```python
ws_router = create_ws_router(getattr(app.state, "bus", None) or get_event_bus())  # openjarvis-ws-bus-v1
```

Applied by `patch_ws_bus.py` (repo root). Anchor matched exactly 1. Pre-patch **32,717 B, EOL CRLF**; post-patch **32,776 B, delta +59**, on-disk size matched prediction exactly. `ast.parse` passed pre-write, `py_compile` OK post-write, marker greps back on line 944.

The +59 decomposes cleanly: 35 bytes of `getattr` wrapper, 24 bytes of trailing marker comment. No hidden newline translation - the CRLF file stayed CRLF.

---

## 2. ROLLBACK REGISTER DELTA

**NEW ROLLBACK POINT - api_routes.py WS bus (08/22, APPLIED 09:01, VERIFIED runtime 09:15 and 09:27)**

```
Copy-Item 'src\openjarvis\server\api_routes.py.bak_wsbus_20260822_090130' 'src\openjarvis\server\api_routes.py' -Force
```

Then RESTART the backend, or the running process keeps the new routing.

Filed in `[[openjarvis-event-bus]]`, NOT in `[[openjarvis-rollback-points]]`, because that register is at its size cap. **Condense the rollback register before adding anything else to it.** Two entries now live outside it: Patch 4 RAWGEN in `[[openjarvis-defect1-engine]]`, and this one in `[[openjarvis-event-bus]]`.

Bak uses the UNDERSCORE form `.bak_wsbus_<ts>`, covered by `.gitignore`'s `*.bak_*`.

**Retire when:** the approve half completes end to end and the confirm UI is mounted (6e).

---

## 3. THE RUNTIME EVIDENCE

Three live runs. All read from the WebSocket listener, not from a log.

**Listener setup:** `.\ws_listen.ps1` (repo root, written this window). Opens a `System.Net.WebSockets.ClientWebSocket` to `ws://127.0.0.1:8010/v1/agents/events` with **NO `agent_id` query param** - a filtered client drops the frame (`ws_bridge.py:48-51`). Reported `STATE: Open`.

**RUN 1 - 09:15, contaminated thread (`message_count: 18`)**
```
09:15:14.570  inference_end     tool_calls: [shell_exec {"command": "echo openjarvis-6d-live"}]
09:15:14.580  tool_confirm_request   confirm_id 0a52171b..., turn_id d5054cc8-t1
09:17:14.584  inference_start   (TTL expired, 120.004 s)
```
**Frame arrived 10 ms after inference_end.** All seven fields present: confirm_id, agent_id=`native_openhands`, turn_id, tool, args_digest, prompt, expires_at.

**RUN 2 - 09:22, same contaminated thread (`message_count: 20`)**
`tool_calls: []`. No tool call emitted, therefore no frame expected and none missing. Model refused, reasoning from the prior turn's "no confirmation" message sitting in its context: it generalized that into a claimed inability to run shell commands at all. **Not a bus finding. Not a Defect 1 finding.** A context artifact.

**RUN 3 - 09:27, GENUINELY fresh thread (`message_count: 2`)**
```
09:27:02.703  inference_end     content:""  tool_calls: [shell_exec {"command": "echo openjarvis-6d-live"}]
09:27:02.716  tool_confirm_request   confirm_id ea9d9e8e..., turn_id e2ac65b6-t1
09:29:02.731  inference_start   (TTL expired, 120.015 s)
```
**Frame arrived 13 ms after inference_end.** Second clean frame, on a clean thread, with empty content and a bare tool call - textbook behavior.

**THE DISCRIMINATOR IS PASSED.** The 08/21 verification plan set it explicitly: the frame must arrive WELL UNDER 120 s, because a run that simply times out again proves nothing changed. Ten and thirteen milliseconds against a 120,000 ms TTL is not a marginal result.

---

## 4. WHAT REMAINS OPEN - THE APPROVE HALF

The TTL expired on every run because nothing answered inside the window. That is expected with no listener mounted, but it means **`POST /v1/tools/confirm` has never been exercised against a live confirm_id inside its TTL.** The 200 path, the actual tool execution, and the model reporting real output are all still unproven end to end.

**FULLY STAGED. Next window runs this and nothing before it.**

Step 1 - define the helper. **PowerShell, Windows box, from `PS C:\Users\Admin\OpenJarvis>`.** Note it dies with the session, so redefine it in any new window:
```powershell
function Approve-OJ($id) { Invoke-RestMethod -Uri http://127.0.0.1:8010/v1/tools/confirm -Method Post -ContentType 'application/json' -Body (@{confirm_id=$id; decision='approve'} | ConvertTo-Json) }
```

Step 2 - start the listener in a SECOND PowerShell window (it blocks):
```powershell
powershell -ExecutionPolicy Bypass -File .\ws_listen.ps1
```

Step 3 - **BRAND NEW conversation** in the chat UI, single message, nothing before it:
```
Run the shell command: echo openjarvis-6d-live
```

Step 4 - check `inference_start`'s `message_count` FIRST. It must be a single digit. If it is not, the thread is contaminated and the run is void.

Step 5 - copy the `confirm_id` from the frame and run `Approve-OJ <id>` immediately. There are 120 seconds. Have the window focused and ready before sending the chat message.

**ACCEPTANCE:** `Approve-OJ` returns 200, the tool executes, and the model's prose carries the literal string `openjarvis-6d-live` as real echo output. **A claim of success WITHOUT that string in the output is a FAILURE, not a pass** - that would be Defect 1 wearing a confirmation costume.

**WHAT A PASS RULES OUT:** that the registry's 200 path is unreachable in practice; that the callback cannot be released early; that the three-way approved/denied/timeout resolution collapses to timeout in the live path. That closes 6e's transport half.

---

## 5. NEW FINDING - CONTEXT CONTAMINATION IS THE DOMINANT TEST HAZARD

This window burned two runs on it, and it changes how every future behavioral test must be designed.

- **`message_count` in the `inference_start` frame is the ONLY reliable freshness tell.** Run 1 showed `message_count: 18`; Run 3 showed `2`.
- **INPUT TOKEN COUNT IS NOT A RELIABLE TELL AND THE PRIOR GUIDANCE ON THIS IS NOW SUPERSEDED.** The 08/16 note said ~5-6k input tokens indicates a fresh thread. Run 1 was 5,186 prompt tokens on an 18-message thread; Run 3 was 3,986 on a 2-message thread. The bands overlap. **Retire the token-count heuristic. Use `message_count`.**
- **Contamination causes the model to invent capability limits.** Run 2 produced a confident, fluent, entirely false statement that it cannot execute shell commands even with confirmation. Nothing in the system changed between Run 1 (which fired the tool) and Run 2 (which refused) except conversation history.
- **The model volunteers unprompted mailbox/Sears context** even on threads where the user never mentioned mail. Worth understanding before it distorts another test. NOT CHASED THIS WINDOW - it is a side finding, deliberately left alone under the finish-the-thing rule.

---

## 6. WHAT THE 08/21 HANDOFF GOT RIGHT

Recorded because the method worked and should be repeated.

The ordering check (`app.py:215` before `app.py:295`) was run specifically because a passing-but-meaningless outcome was possible. It held, and the patch worked on the first apply with no debugging cycle. **The pre-flight check that costs one command is the cheapest thing in this project.**

---

## 7. STATE AT WINDOW CLOSE

- One patch applied, verified at file and runtime level. Rollback registered.
- Backend restarted 08/22 ~09:0x. The running process HAS the fix.
- 6c: SATISFIED. 6d: LIVE-PROVEN, CLOSED. **Bus split: FIXED AND VERIFIED.** 6e: transport half half-proven - frame delivery YES, approve round-trip NOT YET.
- Next action is section 4, and nothing before it.
- Artifacts created this window, both in repo root, both temporary: `patch_ws_bus.py`, `ws_listen.ps1`. `ws_listen.ps1` is worth keeping - it is the only instrument that sees bus traffic live.

---

## 8. EXECUTION PATHS REGISTER

Standing structure. Per path: entry point, call chain with file:line, which ToolExecutor instance serves it and how it is constructed, whether the confirmation gate is live / auto-approved / absent, what event bus traffic it emits, whether a human is present.

### PATH 1 - THE CHAT PATH (primary; 6d proved the gate, this window proved the transport)
- **Entry:** `POST /v1/chat/completions`, `server\routes.py:46`, handler `chat_completions` (47-171).
- **Chain:** handler takes the PRE-BUILT agent off `request.app.state.agent` (:50). **It never calls `JarvisSystem.ask()`.** Dispatch: streaming with tools or explicit agent -> `_handle_agent_stream` (157); cloud model no tools -> `_handle_stream` (155); plain streaming -> `_handle_stream` (158); non-streaming with agent -> `_handle_agent` (162); else `_handle_direct` (165).
- **Agent construction:** `cli\serve.py:233 agent = None`, `:288 agent = agent_cls(engine, model_name, **agent_kwargs)`, `:551 create_app(... agent=agent ...)` -> `server\app.py:214 app.state.agent = agent`.
- **Executor:** the agent builds its OWN at `agents\_stubs.py:325`. `serve.py` passes NO `tool_executor`, so `builder.py`'s executor (168/193) is NOT on this path.
- **Gate:** **LIVE.** 6d wires `interactive=True` + `_server_confirm_callback` into `agent_kwargs` at `cli\serve.py:288-318`, gated on env `OPENJARVIS_CONFIRM_INTERACTIVE` (default ON). PROVEN LIVE 08/21.
- **Bus:** emits on BUS A (serve's instance). **The WS bridge now listens on BUS A too, as of the 08/22 fix. NO LONGER DARK - frame delivery verified 10 ms and 13 ms end to end.**
- **Human present:** YES.
- **Configured agent:** `native_openhands`, engine ollama, model qwen3-coder:30b, port 8010.
- **Allowlist (`c.agent.tools`, 12):** code_interpreter, file_read, file_write, shell_exec, think, calculator, retrieval, mailbox_list_accounts, mailbox_usage_report, mailbox_find_messages, mailbox_move_to_trash, mailbox_empty_folder.
- **Failure mode to know:** `serve.py:289` broad `except Exception` prints "Agent failed to load" and leaves `agent = None`; `routes.py` then falls through to `_handle_direct` with no tools. Console-visible, but the UI just looks toolless.

### PATH 2 - MANAGED-AGENT SSE STREAM
- **Entry:** `POST /v1/managed-agents/{agent_id}/messages`, `send_message` (1744-1850) in `server\agent_manager_routes.py`, inside `create_agent_manager_router` (1319-2302).
- **Chain:** `_stream_managed_agent()` (619) -> nested `generate()` (1026).
- **Executor:** an ad-hoc PER-TOOL `ToolExecutor([tool_instance], bus=bus, interactive=True, confirm_callback=lambda _prompt: True)` at :1202-1207, calling `executor.execute()` DIRECTLY and bypassing the agent.
- **Gate:** **AUTO-APPROVED.** Deliberately - the in-code rationale is that tools the user added in the wizard are pre-approved, and without it `shell_exec` / `apply_patch` would fail with "requires confirmation but no callback available". **6d must decide what replaces this; the wizard-as-consent argument has to be accepted or overturned explicitly.**
- **Driven by:** the agent-manager UI (`frontend\src\lib\api.ts:656,762`; `frontend\src\components\Desktop\lib\api.ts:77,123`). NOT the chat UI.
- **Human present:** yes, but consent is assumed rather than asked.

### PATH 3 - ORCHESTRATOR `ask()`
- **Entry:** `system\core.py:133 ask()` -> `:146 self._get_orchestrator().ask(...)` -> `system\orchestrator.py:21 ask()`.
- **Callers, ALL no-human-present:** `scheduler\scheduler.py:237`, `operators\manager.py:191`, `workflow\engine.py:222` and `:320`, `server\channel_bridge.py:268`, `server\digest_routes.py:79`, `cli\compose_cmd.py:203`, `cli\digest_cmd.py:187`, `evals\backends\jarvis_agent.py:110`, `evals\core\agentic_runner.py:374,394`.
- **Gate:** ABSENT.
- **CONSTRAINT THIS IMPOSES:** `interactive` must stay OPT-IN PER RUN. A blanket default would park a worker for the full TTL on scheduler, workflow, operator, digest and eval runs. Same reason the TTL stays capped at 120 s - `asyncio.to_thread` uses the loop's DEFAULT ThreadPoolExecutor, shared with speech transcription and webhooks.
- **HAZARD:** `orchestrator.py:196-202` constructs `agent_cls(engine, model, **agent_kwargs)` and on TypeError silently retries with ZERO kwargs, losing tools, max_turns and capability_policy with no log.

### PATH 4 - THREE DEEPRESEARCH AUTO-APPROVE SITES
- `agent_manager_routes.py` 714-722 (`generate_deep_research()`, 687), 1558-1564 (`bind_channel()`, 1519), 1635-1641 (nested `handler()`, 1566). All pass `interactive=True, confirm_callback=lambda _prompt: True`.
- **Gate:** AUTO-APPROVED. Human present: NO on the channel-bound ones.

### PATH 5 - UNGATED EXECUTOR CONSTRUCTIONS
- `system\builder.py:168` and `:193` (rebuilt, discarding any wiring added only at 168; `skill_manager.set_tool_executor()` at 187 and `get_skill_tools(tool_executor=...)` at 189 hold references to the FIRST instance).
- `mcp\server.py:58`, `learning\...\environment.py:40`.
- `cli\ask.py:356` (auto-approve `lambda prompt: True`), `cli\chat_cmd.py:123`.

---

## 9. SDP FEED - WHAT THE SYSTEM DESIGN PACKAGE TAKES FROM THIS WINDOW

**Architecture.**
- The two-bus topology is now a RESOLVED architectural finding, not an open one. Document the split, the single bridging point (`app.state.bus`, assigned once at `app.py:215`), the fix, and the reason the narrow fix was chosen over unification.
- **The event stream is now an observable interface, and that is new capability, not just a bug fix.** `inference_start` / `inference_end` / `tool_confirm_request` are all visible to any WebSocket client on `/v1/agents/events`. `inference_end` carries the full generation record: content, tool_calls, tool_results, finish_reason, and a complete usage/latency block. **This is a better instrument than any log file in the project** and the SDP should name it as the primary observability surface.
- The confirmation gate returns BEFORE the `TOOL_CALL_START` emit at `_stubs.py:284-285`. Any observability design that assumes "dispatch implies a start event" is wrong on this codebase.

**Decisions and the evidence behind them.**
- Narrow WS-bridge fix chosen over global bus unification. Deciding axis: event volume blast radius. Evidence: the singleton's consumer set is dominated by `tools\storage\*`, which publishes on every retrieval operation.
- The `getattr(app.state, "bus", None) or get_event_bus()` form preserves the singleton as a fallback for any `create_app` caller that passes no bus. Document why the fallback is retained rather than assuming `app.state.bus`.
- Tool identity established by elimination over the allowlist rather than by log evidence. Document the reasoning form - it is reusable wherever the gate suppresses the naming instrument.

**The Defect 6 confirmation gate - GREAT DETAIL required, per Gray's standing instruction.**
- Registry: module-level state INSIDE the backend process. The 200 and 409 paths are unreachable externally.
- Payload: seven fields, `agent_id` inside `data` because `Event` is `@dataclass(slots=True)`. **All seven CONFIRMED PRESENT on the wire 08/22** - previously known only from code.
- Transport: `POST /v1/tools/confirm`, accepts `approve|approved|deny|denied`, 400 bad, 404 unknown/expired, 200 first resolve, 409 with recorded decision on second. Write-once honored. **The 200 path is still unexercised against a live TTL.**
- Emit latency, measured: **10 ms and 13 ms** from `inference_end` to `tool_confirm_request` on the wire. The gate is not a latency cost; the human is.
- Threading model: callback blocks a worker on the loop's shared default ThreadPoolExecutor for up to 120 s. **THREE live measurements now: 120.004 s, 120.007 s, 120.015 s.** Consistent to within 11 ms across three runs on two different days. That is the measured cost of an unanswered confirm and it belongs in the SDP as a hard number, not an estimate.
- Contract asymmetry: `confirm_registry.resolve()` accepts only the full words `approved` / `denied`; the route normalizes. Any non-route caller must pass full words.
- Three-way outcome: approved / denied / timeout, resolved by re-reading the registry entry after a False callback return, because the callback contract is `Callable[[str], bool]` and a bool cannot carry three states.

**Hazards register additions.**
- An unanswered confirm costs a full 120 s worker occupancy on a SHARED executor. Measured three times.
- **NEW - the model fabricates capability limits under context contamination.** On a dirty thread it stated it cannot execute shell commands even with confirmation, fluently and falsely, while the identical prompt on a clean thread fired the tool in 1.4 s. This is a REPORTING failure mode adjacent to Defect 1 and it must be in the hazards register: the model's account of its own capabilities is not evidence about the system.
- `mailbox_move_to_trash` and `mailbox_empty_folder` have NO `requires_confirmation` at the spec level. **The destructive mailbox tools are ungated and no amount of gate wiring reaches them.** Only three specs in `src\openjarvis\tools` declare it: `agent_tools.py:289`, `git_tool.py:283`, `shell_exec.py:71`.
- Bare `except Exception` at `api_routes.py:946` logs at debug only and can silently drop the entire WS bridge.

**Evidence standard, as method.** Every acceptance test in the SDP should name what a passing result RULES OUT. Templates now on record: 400-not-404; the 0.44 s release against a 4 s TTL; the ordering check at `app.py:215` vs `:295`; and from this window, **the 10 ms frame against a 120 s TTL** - a discriminator chosen precisely because a slow pass and a timeout would have been indistinguishable.

**Test methodology - MUST be in the SDP.** Behavioral tests against the chat path require a verified-clean thread. `message_count` from the `inference_start` frame is the freshness assertion. Input token count is NOT - it produced overlapping bands and is retired as a heuristic.

---

## 10. SDD SECTION

Gray is building a detailed System Design Document covering all OpenJarvis work to date. This window feeds it:

- **The bus split moves from OPEN DEFECT to RESOLVED**, with the fix, the one-line diff, the byte-level evidence, and the runtime proof. The SDD should carry both the broken and fixed topology - the broken one explains a year of dark events.
- **The event stream as the system's primary observability interface**, documented as a designed surface rather than a debugging accident.
- **Execution path register**, section 8, five paths with gate status; Path 1's bus row is now updated to reflect delivery.
- **The confirmation gate's end-to-end behavior**, with emit latency (10-13 ms) and unanswered-confirm cost (120.0 s, three measurements).
- **A test-methodology section.** Two of this window's runs were void for context contamination. The SDD needs a stated protocol for behavioral testing, or future windows will re-learn this.

**Standing instruction:** every handoff from here carries an SDD section, and every window feeds it.

---

## 11. METHOD LESSONS FROM THIS WINDOW

1. **The pre-flight ordering check paid for itself.** One command on 08/21 meant the patch worked first try with zero debugging.
2. **Predict the byte delta and check it.** +59 was predicted and +59 landed. That single comparison is what caught the CRLF disaster on 08/17 and it caught nothing this time - which is exactly what a good check looks like most of the time.
3. **When a run produces no result, read the instrument before theorizing.** Run 2's refusal looked like a regression. The listener showed `tool_calls: []` and the question was answered in one glance. Same lesson as 08/21, applied correctly this time.
4. **Verify the test conditions, not just the test result.** Two runs were void because the thread was not clean. The assertion (`message_count`) was available in the instrument the whole time and was not checked until after the second void run.
