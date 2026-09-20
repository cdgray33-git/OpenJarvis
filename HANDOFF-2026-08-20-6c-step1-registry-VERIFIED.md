# HANDOFF - 2026-08-20 - 6c STEP 1 (REGISTRY) BUILT AND VERIFIED

Carry this into a fresh window. Continues
`HANDOFF-2026-08-19-evening-6c-prereq-CLOSED.md`.

## Windows in play

- **PowerShell, Windows box**, prompt `PS C:\Users\Admin\OpenJarvis>` - everything
  below. Gray works from the project root and pastes commands exactly as given.
- **bash, ollama-mcp (172.16.33.200)** - not needed.

## HEADLINE

Two things closed this window, nothing dangling.

1. **The ws_bridge `agent_id` filter hazard is CLOSED** - source and runtime.
   `_aid` on the chat path is `native_openhands`, non-empty.
2. **6c step 1 is BUILT AND VERIFIED IN ISOLATION.**
   `src\openjarvis\core\confirm_registry.py` exists, compiles, and passes a
   19-case self-test. Nothing imports it yet, so no restart was required.

**Next action is 6c step 2. See NEXT ACTIONS - there is a proposed reorder
awaiting Gray's ruling before anything is written.**

---

## SYSTEM DESIGN PACKAGE - PINNED, SECONDARY THOUGHT AT ALL TIMES

Gray is authoring a detailed System Design Document / Package (SDD/SDP)
covering all OpenJarvis work to date.

**This section is PINNED and must appear in EVERY handoff from here forward.**
Gray's standing instruction, given 08/20: while working any issue, the SDP is
the secondary thought - capture the architecture, the decisions, the evidence
behind them, and the hazards found, as the work happens. Every window feeds it.

**Gray called out the Defect 6 confirmation gate as needing GREAT DETAIL in
the SDP specifically** - registry, payload, transport, and threading model.

### SDP feed from this window - confirmation gate

- **Threading model.** SSE chat path runs the whole sync tool chain on an
  `asyncio.to_thread` worker (`asyncio_0`, runtime-proven 08/19), matching
  `server\stream_bridge.py:155`. The waiter blocks a WORKER thread; the
  resolver runs on the LOOP thread. That is why the registry uses
  `threading.Event` and never `asyncio.Event`. `Event.set()` from the loop
  thread is non-blocking, so the approval POST returns immediately.
- **Write-once decision contract.** `resolve()` never flips a recorded
  decision; it returns False instead. That is exactly what lets the route
  answer 409 with the decision it already holds, rather than racing.
- **A timeout is not a refusal.** `timeout` is a first-class return value,
  distinct from `denied`, all the way through. The gate must carry that
  distinction into the ToolResult or the model is told a human refused when
  nobody was looking.
- **TTL source.** Env var `OPENJARVIS_CONFIRM_TTL`, default 120 s.
  `config.toml` is deliberately NOT consulted - it is machine-regenerated and
  can silently revert.
- **No background task.** Expired entries are reaped inside `register()`.
  No new task, no new failure mode.
- **Capacity constraint that caps the TTL.** `asyncio.to_thread` uses the
  loop's DEFAULT ThreadPoolExecutor, shared with `speech_router.py:326/421/523`
  transcription and the `webhook_routes.py` handlers. Every pending confirm
  parks one worker for its whole TTL. Long TTL plus concurrent confirms starves
  speech. Keep 120 s; do not raise it.
- **Transport asymmetry.** Prompt goes OUT on the `/v1/agents/events` WS
  (outbound only, lossy, broadcast, filtered). Approval comes BACK on a NEW
  POST route. There is no inbound path on the chat SSE stream.
- **Loss absorption.** A prompt lost to the lossy `put_nowait` at
  `ws_bridge.py:52-55` is indistinguishable from a user who never looked. Both
  land on timeout. That is how Option A absorbs the WS drop, by design.

---

## WHAT WAS ESTABLISHED THIS WINDOW

### 1. The `agent_id` / ws_bridge filter hazard - CLOSED

Chain read end to end:

- `tools\_stubs.py:158` - `ToolExecutor.__init__` takes `agent_id: str = ""`,
  stored as `self._agent_id` at 167, consumed at 213/221/230.
- `agents\_stubs.py:324-329` - the chat-path construction site:
  `_aid = agent_id or getattr(self, "agent_id", "")`, then
  `ToolExecutor(..., agent_id=_aid, interactive=interactive,
  confirm_callback=confirm_callback)`.
- `system\builder.py` and `system\orchestrator.py` grep **ZERO** for
  `agent_id`. Positive control on the same command: `ToolExecutor` 3 hits in
  builder.py, `def ` 27 hits in builder.py and 6 in orchestrator.py. So the
  kwarg is never passed and `_aid` falls to the CLASS ATTRIBUTE.
- Every agent class declares one: `native_openhands.py:60`
  `agent_id = "native_openhands"`, plus native_react, operative, orchestrator,
  rlm, monitor_operative, deep_research, morning_digest, simple, claude_code,
  openhands. Base `agents\_stubs.py:58` is annotation-only.
- **RUNTIME CONFIRMATION** from `agent.log`: every RUNSTART on the chat path
  reads `agent=NativeOpenHandsAgent` (latest `a8172e4c`, 08/19 18:54:26,
  model qwen3-coder:30b, tools=12, maxturns=15).

**Conclusion: `agent_id` in the confirm payload will be `native_openhands`.
Non-empty, so the `ws_bridge.py:48-51` filter cannot drop it for a client that
connected without a filter.**

### 2. CONSEQUENCE FOR 6e - record it now, do not rediscover it later

`_aid` is a CLASS ID STRING, not a managed-agent UUID. `agents\manager.py:168`
mints managed-agent ids as `uuid4().hex[:12]`. A WS client connecting with
`?agent_id=<uuid>` will NEVER match `native_openhands`, and `ws_bridge.py:52`
drops the confirm event.

**The chat-path WS client must connect with NO `agent_id` query param** - a
falsy `_agent_filter` means no filtering. Today both `useAgentEvents` call
sites in `pages\AgentsPage.tsx` pass an agentId, which is precisely why the
chat path is dark.

### 3. 6c STEP 1 - `core\confirm_registry.py` BUILT AND VERIFIED

New file, 6478 bytes, pure ASCII, marker `openjarvis-confirm-registry-v1`.
In `core` rather than `server` so `tools\_stubs.py` and the route layer both
import it without a cycle.

**API as built:**

```
APPROVED / DENIED / TIMEOUT        module constants
RESOLVABLE = (APPROVED, DENIED)    resolve() raises ValueError on anything
                                   else; TIMEOUT is settable internally only

default_ttl() -> float             env var OPENJARVIS_CONFIRM_TTL, falls back
                                   to 120.0 on unset/unparseable/non-positive

register(tool, agent_id="", turn_id="", ttl=None) -> confirm_id
                                   uuid4 hex; reaps expired inside register

wait(confirm_id, timeout=None) -> "approved" | "denied" | "timeout"
                                   unknown id returns timeout - the gate fails
                                   closed

resolve(confirm_id, decision) -> bool
                                   write-once; False on unknown, expired, or
                                   already-set; never flips

get(confirm_id) -> dict | None     for the route's 404/409 logic; carries
                                   state "pending" | "resolved"

reap() / pending_count() / clear()
```

Internals: module-level `_LOCK = threading.Lock()` guarding `_PENDING`, a dict
of `_Pending` dataclasses (confirm_id, tool, agent_id, turn_id, created_at,
expires_at, `threading.Event`, decision).

**Verification, all green:** py_compile OK; ASCII byte-vs-char encoding control
OK (6478/6478); 19-case self-test covering approve, deny, timeout, timeout
bounded, first/second resolve, decision-not-flipped, state resolved/pending,
unknown-id resolve/wait/get, TTL expiry wait and resolve, agent_id and turn_id
carried, bad-decision ValueError, clear, default TTL 120.0. Then a corrected
negative control: `import asyncio` occurs **0** times in the file.

**No restart needed - nothing imports it yet.**

---

## TWO CLAUDE ERRORS THIS WINDOW - BOTH INSTRUCTIVE

### 1. A negative control that tested the documentation, not the code

The patch script asserted the string `asyncio.Event` was ABSENT from the module
and reported `FAIL - present`, printing `6c STEP 1 FAILED - DO NOT BUILD ON
THIS`. The hit was the module's own DOCSTRING, which explains that it uses
`threading.Event` and never `asyncio.Event`.

`Get-Content | Select-String 'asyncio\.Event'` returned exactly one line, and
that line is prose. The corrected control - `import asyncio` count - returned 0.

**RULE: a negative control on a substring must exclude comments and docstrings,
or test the import instead of the mention.** A prose mention is not a code fact.

### 2. Handing Gray a path that does not work from the project root

Twice. The `.ps1` downloads to `%USERPROFILE%\Downloads`, and Claude gave a
`.\patch_confirm_registry.ps1` command to run from the repo root, then only
explained the mismatch after it errored.

**GRAY'S RULING, now a standing rule** - see STANDING RULES below.

---

## NEW ENVIRONMENT HAZARD - .NET DOES NOT SHARE POWERSHELL'S LOCATION

From `PS C:\Users\Admin\OpenJarvis>`:

```
[System.IO.File]::ReadAllText('src\openjarvis\core\confirm_registry.py')
  -> DirectoryNotFoundException, resolved against C:\WINDOWS\system32
Get-Content 'src\openjarvis\core\confirm_registry.py'
  -> works
```

Cmdlets use the PowerShell provider path; .NET methods use the PROCESS working
directory. **Any `[System.IO.File]` call handed to Gray must use an absolute
path or `Join-Path (Get-Location)`.** The patch script itself was unaffected -
it builds absolute paths from a resolved repo root.

---

## NEXT ACTIONS IN ORDER

**1. RULING NEEDED FIRST - the order of 6c steps 2 and 3.**

The carried spec says registry -> emit -> route. Claude proposes **route
before emit**, for this reason: if the emit lands first, the only thing that
can be verified is a timeout, because no approval can arrive. If the route
lands first, it is independently testable (mount, 404 on an unknown
confirm_id), and then the very first live emit can be exercised fully -
approve, deny, AND timeout - in one pass. Gray rules; do not proceed until he
does.

**2. 6c step 2 - `POST /v1/tools/confirm`.**

```
Request:  {"confirm_id": "<hex>", "decision": "approve" | "deny"}
200:      {"confirm_id", "tool", "turn_id", "state": "resolved", "decision"}
404:      unknown or already reaped
409:      already resolved - returns the recorded decision, never flips it
```

Echoing `tool` back lets the UI confirm it approved the thing it displayed.
Open question: whatever auth the existing v1 routes carry, this one carries -
approving is the privilege. Maps onto the registry as built:
`get()` None -> 404; `resolve()` False on an existing entry -> 409 with the
recorded decision; `resolve()` True -> 200.

**3. 6c step 3 - the emit at the gate, `tools\_stubs.py:262-280`.**

```
EventType.TOOL_CONFIRM_REQUEST
data = {
  "confirm_id":  <uuid4 hex from register()>,
  "agent_id":    <self._agent_id - proven "native_openhands" on chat>,
  "turn_id":     <CURRENT_TURN_ID.get()>,
  "tool":        <tool name>,
  "args_digest": <reuse _args_digest, 400 char cap>,
  "prompt":      <the string the gate already builds at _stubs.py:274>,
  "expires_at":  <epoch seconds>
}

EventType.TOOL_CONFIRM_RESOLVED
data = { "confirm_id", "agent_id", "turn_id",
         "decision": "approved" | "denied" | "timeout" }
```

`agent_id` must sit INSIDE `data` - `Event` has no such field
(`core\events.py:82-88`). `turn_id` correlates the prompt to the same turn in
`dispatch.log` and `agent.log`; the live ATTEMPT line confirms the format:
`a8172e4c-t1`.

**The gate at `_stubs.py:275` currently makes a False callback return say
"execution denied by user."** That is FALSE on a timeout and violates the
standing rule that a timeout is not a refusal. Step 3 must make the ToolResult
distinguish the two.

The gate sits BEFORE the ThreadPoolExecutor, so the wait is not bounded by
`default_timeout=30.0`. It is bounded by whatever the SSE client tolerates -
UNVERIFIED, worth measuring.

**4. 6d** - thread `interactive=True` and `confirm_callback` into
`agent_kwargs` at `system\orchestrator.py:150-168`. **HAZARD at 196-202:** an
unsupported kwarg makes construction silently retry with ZERO kwargs, losing
tools, max_turns, capability_policy, everything, with no log. Verify the
constructed agent actually RECEIVED its kwargs.

**5. 6e** - frontend: mount `useAgentEvents` in chat **with no agent_id
param** (see section 2 above), render the prompt, POST the answer.

**6.** Condense `openjarvis-rollback-points` - at its size cap.
**7.** Bring `memdb_audit.log` under the 30 MB scheme.
**8.** The `/v1/sessions` patch - fully spec'd, still untouched.
**9.** Decide what to do with `/v1/traces`.

### Parked, at Gray's explicit instruction - do not chase mid-mission

Gray noted the tree has many agent selections beyond `native_openhands`
(native_react, operative, orchestrator, rlm, monitor_operative, deep_research,
simple, claude_code, openhands, morning_digest) and wants them discussed -
but said plainly it is NOT to pull the current mission off course. **Raise it
after 6c/6d/6e closes.**

---

## THE TWO ROUTE-LAYER HAZARDS - UNCHANGED

1. **Other entry points reach `ask()` with no proven thread hand-off:**
   `channel_bridge.py:268` and `digest_routes.py:79`. The gate lives in the
   shared ToolExecutor, so every entry point inherits it. The morning digest
   runs scheduled with **no human present** - a confirm there parks a worker
   for the full TTL then times out. Argument for `interactive` defaulting to
   False and being opt-in per run at 6d. **The `asyncio_0` proof covers the SSE
   chat path ONLY. It does NOT cover these two.**
2. **`asyncio.to_thread` uses the loop's default ThreadPoolExecutor**, shared
   with speech transcription and webhook handlers. Keep the 120 s default.

---

## ROLLBACK POINTS - ACTIVE

```powershell
Remove-Item 'C:\Users\Admin\OpenJarvis\src\openjarvis\core\confirm_registry.py' -Force
Copy-Item 'src\openjarvis\tools\_stubs.py.bak_defect6_threadprobe_20260819_184937' 'src\openjarvis\tools\_stubs.py' -Force
Copy-Item 'src\openjarvis\core\events.py.bak_defect6_confirm_20260819_081500' 'src\openjarvis\core\events.py' -Force
Copy-Item 'src\openjarvis\server\ws_bridge.py.bak_defect6_confirm_20260819_082934' 'src\openjarvis\server\ws_bridge.py' -Force
Copy-Item 'src\openjarvis\engine\ollama.py.bak_retry400_20260818_160710' 'src\openjarvis\engine\ollama.py' -Force
```

The first removes this window's new registry module (also clear
`src\openjarvis\core\__pycache__\confirm_registry*.pyc`). The second reverts
the thread probe - **leave it in place**, it costs one field per dispatch and
it is the only runtime evidence of the thread question. The last returns
`ollama.py` to STOCK and disarms the Defect 1 Patch 5 trap. Restart the backend
after any of these.

---

## ENVIRONMENT - ESTABLISHED BY TEST

- **`--reload` is NOT active.** Every patch needs a manual restart before it
  can be verified live. HTTP 200 proves only that something answers; the
  discriminator is process creation time.
- Live backend runs the repo tree. Port is **8010**, not 8000.
- **PID REUSE:** identify a process by creation time, never by pid alone.
- **Execution policy is AllSigned.** Run patch scripts as
  `powershell -ExecutionPolicy Bypass -File .\script.ps1` - which also runs
  them in a child process, protecting the parent session.
- Logs live in `%LOCALAPPDATA%\OpenJarvis\logs`, not the repo tree.
- venv python is `.venv\Scripts\python.exe`; a system Python 3.12 also
  resolves openjarvis to the repo tree.

```powershell
Get-CimInstance Win32_Process -Filter "Name like '%python%'" | Select-Object ProcessId, @{n='Started';e={$_.CreationDate}} | Format-Table -AutoSize | Out-String -Width 80
```

---

## DEFECT 1 - UNCHANGED, PATCH 5 STILL ARMED

Not touched. Passive armed trap. Check `engine.log` after any spontaneous
sighting. Do not burn sessions trying to trigger it.

## LIVE TEST TARGETS

Censused 08/18 late. **RE-CENSUS BEFORE USING ANY OF THESE.**

```
sears     total=101  {'Inbox': 99,  'Personal': 1, 'Promotions': 1}
amf       total=105  {'Bulk': 3, 'Inbox': 100, 'Personal': 2}
navyexchg total=101  {'Inbox': 99,  'Promotions': 2}
zales     total=91   {'Inbox': 88,  'Personal': 2, 'Promotions': 1}
```

`sears` approved as a destructive target. `bachrach` is DEAD. Probe:
`probe_census_target.py`, marker `openjarvis-census-target-v3`, repo root,
read-only. Connector-level `find_messages` returns a plain list, not a dict.

---

## STANDING RULES

> "We finish off a project and do not leave dangling processes to come back to."

> **Always verify.** Verify each patch in isolation before building on it. A
> negative grep needs a positive control on the same pattern syntax.

**GRAY'S WORKING DIRECTORY RULE - added 08/20, after Claude broke it twice:**

> Gray works from `PS C:\Users\Admin\OpenJarvis>` and pastes commands exactly
> as given. **Every command must run correctly FROM THERE.** If a command needs
> a different path, shell, or host, say so IN THE REQUEST, BEFORE he runs it -
> never after it fails. When a file is produced for download, state where it
> lands and give the command that already accounts for that location, in the
> same message.

Read before patching - anchor patches on text, never on line numbers. A patch
script must verify its own write. Prove an instrument writes before trusting
its silence. Verify a destructive outcome against the mailbox, never against
the transcript. A file-level grep hit is not a file-level fact. The existence
of a thing is not the use of a thing. A timeout is not a refusal. An inference
about the runtime is not a fact about the runtime.

A patch script pasted into an interactive shell must not contain a bare `exit`
- it kills the session and takes the output with it. Put the guard in an
if/else and put the patch in a `.ps1` file.

A live log's `LastWriteTime` is not evidence of when it was last written. Open
handles defer the metadata update. Read the tail.

**Added this window:** a negative control on a substring must exclude comments
and docstrings, or test the import instead of the mention. And .NET file
methods do not share PowerShell's location - give them absolute paths.

**Patch script pattern that works - `patch_confirm_registry.ps1` is the current
template:** it resolves the repo root itself (from `-Root`, `$PSScriptRoot`,
the current location, then the known default), so it runs from wherever the
file lands; it writes the target file itself so nothing has to be pasted;
it backs up only if a file is already there; it writes with
`UTF8Encoding($false)`; then it verifies markers, runs an encoding control,
runs `py_compile`, runs an isolated self-test from `%TEMP%` with `PYTHONPATH`
set to `src`, cleans up after itself, and prints the rollback command.

## STANDING NOTE

This window closed both of its inherited items and opened none. The next window
starts on 6c step 2, with one ruling to take from Gray first: route before
emit, or emit before route.
