# HANDOFF 2026-08-29 B - W17

## THE agent_id CHAIN IS RESOLVED END TO END. BARRIER 2 SURVIVES WITH ITS MECHANISM CORRECTED. SOCKET AUTH DEFERRED BY GRAY'S RULING.

Predecessor: `HANDOFF-2026-08-29-A-W16-6E-BLOCKER-IS-THREE-BARRIERS-AGENT-ID-FILTER-DROPS-CONFIRM-EVENTS.md`

W16 remains the authority on the three-barrier framing, the WS confirm delivery
path (its section 2), the token-source closure, and the discrepancy register D1
through D7. This window CORRECTS W16 on one material point (barrier 2's
mechanism) and adds the resolution chain W16 left open as its next-action 1.

Window opened 08/29 late morning, closed at exchange 13. **NO SOURCE FILE WAS
MODIFIED. NO COMMIT WAS MADE.** One backend restart was performed by Gray. One
design ruling was given. Everything else is read-only measurement.

The headline: the `agent_id` value that has been hunted across several sessions
is `native_openhands`, it is a CLASS ATTRIBUTE resolved through a fallback
chain, and the reason the WS filter drops confirm frames is a NAMESPACE
MISMATCH between class identity and instance identity - not an empty string.
Section 2 documents that chain in full, which is the specific deliverable Gray
asked for.

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
- CARRY THE 550B CLOUD MODEL. When a question needs whole files rather than
  targeted reads, bundle the suspected files into one markdown file for
  `openrouter/nvidia/nemotron-3-ultra-550b-a55b` rather than spending window
  cycles on piecemeal reads. Reproduction pattern in W16 Appendix B.
- ALWAYS PUSH TO BOTH REMOTES, UNPROMPTED. `origin` is GitHub, `gitlab` is the
  lab instance at 172.16.33.126. That naming is a trap worth restating.
- W12-R1: a command goes in a fenced code block ONLY if it is the command to run
  right now. Reference and restore commands go inline in prose, unformatted.
- W13-R1: an instrument that has never produced a positive reading cannot have
  its silence read as a finding.
- W13-R2: look for the existing harness before writing a new one.
- W13-R3: state the execution context for a script, not just its path.
- W14-R1: one command per message means ONE DESTINATION per message.
- W14-R2: write control expectations against the POST state.
- W14-R3: a wildcard that matches nothing is silent in PowerShell. Every
  delivery command assigns to a variable and prints a loud NOT DOWNLOADED
  message.
- W15-R2: a document described as LIVING is not stale between updates. Raise
  internal contradiction, not lateness.
- W15-R3: verify the instrument, not only the result.
- W16-R1: the 550B is an instrument for breadth, not a source of findings. Its
  answers enter the record as CLAIMS TO VERIFY. Ask for facts about code, not
  conclusions about behavior.
- W16-R2: a log absence names a symptom, never a cause.
- W16-R3: read the definition before predicting from the call site.
- W16-R4: an inherited claim is not a verified claim. Three documents agreeing
  is often one measurement copied three times.

NEW RULES ADDED THIS WINDOW:

- **W17-R1. CHECK THE EXISTING RECORD BEFORE SPECIFYING A NEW HUNT.** W16 spent
  its closing exchanges specifying a question whose answer had been established
  on 08/20 and filed. This window answered it in two commands, and the speed was
  entirely retrieval, not insight. Before opening a hunt, search the prior
  windows and the memory record for the same question. This is the practical
  half of W16-R4: the rule says re-verify inherited claims, and this rule says
  find them first.
- **W17-R2. A PREDICATE IS NOT SHARED ACROSS BRANCHES UNTIL READ ON EACH
  BRANCH.** Claude carried the streaming dispatch predicate from the 08/23
  record onto the non-streaming branch and predicted the wrong path for a live
  probe. The two predicates differ materially. See section 3 and D2.
- **W17-R3. A TOKEN COUNT IS A BRANCH FINGERPRINT.** `prompt_tokens: 3979` for a
  six-word prompt proved a system prompt and tool definitions were injected,
  which identified the branch before any file was read. Cheap, non-interactive,
  and available on every non-streaming response. Use it.
- **W17-R4. AN INFRASTRUCTURE SYMPTOM IS NOT A CODE DEFECT.** Two windows have
  now spent exchanges on the litellm `ModuleNotFoundError`. It is what this
  system does when NO INFERENCE ENGINE IS AVAILABLE. Gray identified the actual
  cause immediately: the Ollama guest is not set to start at boot on the
  R730xd, so a power outage strands OpenJarvis on a fallback. Before treating a
  runtime failure as a code defect, establish that the infrastructure it depends
  on is up.

---

## 1. WHAT WAS DONE

Seven read-only measurements, one restart by Gray, one design ruling. No file
written, no commit.

1. Read `agents\_stubs.py` construction site (barrier 2 premise check).
2. Read all `agent_id` class assignments across `src\openjarvis\agents`.
3. Read `backend.log` startup and bind markers.
4. Fired a non-streaming chat probe. FAILED, 500 in 36 ms.
5. Read the backend.log tail, confirming the litellm `ModuleNotFoundError`.
6. Probed the Ollama host at 172.16.33.200:11434. UP, 29 models.
7. Gray restarted the backend. Re-fired the probe. SUCCESS in 24.3 s.
8. Read `routes.py:155-185`, the dispatch region.

---

## 2. THE agent_id RESOLUTION CHAIN - THE DELIVERABLE

This is the full process path and flow for the value that has been hunted across
several sessions. Every stage below is a direct read. Where a stage rests on an
unverified claim it is labeled. Read this section before any 6e work.

### 2.0 What the question actually is

A `TOOL_CONFIRM_REQUEST` event carries an `agent_id` inside its `data` payload.
`ws_bridge.py` compares that value against a per-client filter taken from the
WebSocket query string. If they do not match, the frame is dropped BEFORE it
reaches the client queue. So the identity of `agent_id` decides whether a human
can ever see a confirmation prompt. That is why this value gates 6e.

### 2.1 STAGE 1 - the default, and why it is a red herring

`src\openjarvis\tools\_stubs.py`, `ToolExecutor.__init__`, declares
`agent_id: str = ""` and assigns it to `self._agent_id`.

LINE NUMBER HAZARD: the 08/20 read recorded 158 (signature) and 167
(assignment); W16 recorded 162 and 171. The file gained lines from the 08/19
thread-probe patch, which is the likely cause of the drift. **Locate this by
content, never by line number.** Both reads agree on the values, which is what
matters.

**W16 predicted the runtime value from this default and got it wrong.** The
default only fires when the executor is constructed WITHOUT the kwarg. On the
chat path it is always constructed WITH it. See stage 2.

### 2.2 STAGE 2 - the chat-path construction site (VERIFIED THIS WINDOW)

`src\openjarvis\agents\_stubs.py`, the agent base class, builds its own executor:

```
306         agent_id: Optional[str] = None,
324         _aid = agent_id or getattr(self, "agent_id", "")
325         self._executor = ToolExecutor(
329             agent_id=_aid,
```

Read directly on 08/29 with a grep whose positive control was the presence of
`ToolExecutor(` in the same output. This matches the 08/20 record exactly.

**The executor is NOT built bare on this path.** It receives `agent_id=_aid`.
The `or` on line 324 is a two-level fallback and the whole question turns on it.

### 2.3 STAGE 3 - fallback level one: the constructor kwarg

`agent_id` at line 306 defaults to `None`. Is it ever passed?

08/20 grep result, carried and NOT re-verified this window: `system\builder.py`
and `system\orchestrator.py` return ZERO hits for `agent_id`, with a positive
control of 3 `ToolExecutor` hits in builder.py on the same glob. So nothing in
the construction chain supplies it.

**CARRIED AS A CLAIM, NOT A FINDING.** Per W16-R4 this deserves a re-read before
any patch depends on it. It is one grep.

Consequence: `agent_id` is `None`, which is falsy, so `_aid` falls through to
level two.

### 2.4 STAGE 4 - fallback level two: the class attribute (VERIFIED THIS WINDOW)

`getattr(self, "agent_id", "")` looks up the attribute on the concrete agent
instance, which resolves through its class.

**The base class does NOT provide one.** `agents\_stubs.py:58` is
`agent_id: str` - an ANNOTATION WITH NO ASSIGNMENT. Annotations do not create
class attributes. If a concrete class failed to assign one, `getattr` would
return the `""` default and W16's barrier 2 would have been right by accident.

**Every concrete agent class assigns one.** Full inventory, read 08/29 across
`src\openjarvis\agents` recursive, positive control 40 `^class ` hits on the
same glob:

| File | Line | Value |
|---|---|---|
| advisors.py | 91 | `advisors` |
| archon.py | 376 | `archon` |
| claude_code.py | 54 | `claude_code` |
| conductor.py | 338 | `conductor` |
| deep_research.py | 162 | `deep_research` |
| mini_swe_agent.py | 589 | `mini_swe_agent` |
| minions.py | 317 | `minions` |
| monitor_operative.py | 99 | `monitor_operative` |
| morning_digest.py | 36 | `morning_digest` |
| native_openhands.py | 60 | `native_openhands` |
| native_react.py | 60 | `native_react` |
| openhands.py | 27 | `openhands` |
| operative.py | 39 | `operative` |
| orchestrator.py | 43 | `orchestrator` |
| rlm.py | 90 | `rlm` |
| simple.py | 15 | `simple` |
| skillorchestra.py | 197 | `skillorchestra` |
| toolorchestra.py | 327 | `toolorchestra` |

TWO NON-CONSTANT SITES in the same output, and they are the other half of the
story:

| File | Line | Expression |
|---|---|---|
| manager.py | 168 | `agent_id = uuid.uuid4().hex[:12]` |
| scheduler.py | 288 | `agent_id = event.data.get("agent_id")` |

`manager.py:168` is the managed-agent instance id. **This is the second
namespace and the actual cause of barrier 2.** See 2.7.

### 2.5 STAGE 5 - which agent class is actually constructed

`src\openjarvis\system\orchestrator.py:197`:
`ag = agent_cls(s.engine, s.model, **agent_kwargs)`, with fallbacks
`agent_cls(s.engine, s.model)` at 200 and `agent_cls()` at 202. Class resolved
at 132 via `agent_cls = AgentRegistry.get(agent_name)`; `agent_name` comes from
`s.config.agent.default_agent` via `system\core.py`.

Carried from 08/20, not re-read this window.

RUNTIME CONFIRMATION, from `agent.log`: every RUNSTART on the chat path reads
`agent=NativeOpenHandsAgent`.

**PATCH-DESIGN HAZARD, restated because it will bite 6d.** The construction at
196-202 is a try/except TypeError ladder. An unsupported kwarg makes it silently
retry with ZERO kwargs, losing tools, max_turns and capability_policy with no
log. Any patch adding a kwarg there MUST verify the constructed agent actually
received it, not merely that construction succeeded.

### 2.6 STAGE 6 - the resolved value

For the chat path: `_aid` = `"native_openhands"`. NON-EMPTY.

The complete flow, in one line:

```
config.agent.default_agent
  -> AgentRegistry.get(agent_name)
  -> agent_cls == NativeOpenHandsAgent
  -> class attr native_openhands.py:60 agent_id = "native_openhands"
  -> agents\_stubs.py:324  _aid = None or getattr(self,"agent_id","")
  -> agents\_stubs.py:329  ToolExecutor(agent_id="native_openhands")
  -> self._agent_id
  -> TOOL_CONFIRM_REQUEST data["agent_id"] = "native_openhands"
```

### 2.7 STAGE 7 - where it meets the filter, and why the frame dies

`server\ws_bridge.py:56-59`, inside `_on_event`:

```
agent_filter = getattr(ws, "_agent_filter", None)
event_agent  = (event.data or {}).get("agent_id")
if agent_filter and event_agent != agent_filter: continue
```

`_agent_filter` is the `agent_id` query parameter from the WS handshake,
stashed at line 86.

**THE MISMATCH.** The event carries a CLASS IDENTITY (`native_openhands`). A
managed-agent UI client connects with an INSTANCE IDENTITY (a 12-char uuid4 hex
from `manager.py:168`). These are two different namespaces that were never
reconciled. `"native_openhands" != "a3f9c2e18b04"` is true, so the frame hits
`continue` and is dropped silently.

**This is barrier 2, correctly stated.** W16 said the cause was an empty string
from an executor built without the kwarg. That is false on this path. The
correction matters because it changes the fix: stamping a "real" agent_id onto
the payload accomplishes nothing, since the payload ALREADY carries a real id -
of the wrong kind.

### 2.8 THE CONTRIBUTING FACTORS, collected

Everything that had to be true for the hunted value to be `native_openhands`:

1. `ToolExecutor` accepts `agent_id` as a kwarg with an empty-string default.
2. The agent base class builds its OWN executor rather than receiving one, so
   the base class controls the value.
3. `system\builder.py` and `system\orchestrator.py` never pass `agent_id`, so
   the constructor kwarg is `None`. (CARRIED CLAIM - re-verify.)
4. `agents\_stubs.py:58` is annotation-only, so the base contributes nothing.
5. Every concrete agent class hard-codes a class-attribute string.
6. `config.agent.default_agent` selects `native_openhands` on the chat path.
7. `manager.py:168` mints managed-agent ids in a DIFFERENT format, and nothing
   translates between the two namespaces.
8. `ws_bridge` filters on exact string equality with no namespace awareness.

Remove any one of 4, 5 or 6 and the value changes. Remove 7 or 8 and barrier 2
disappears entirely.

### 2.9 WHAT THIS MEANS FOR THE 6e FIX

Barrier 2 is resolved by a FRONTEND URL DECISION, not a server change: a chat
client must connect to `/v1/agents/events` with NO `agent_id` query parameter,
so `_agent_filter` is falsy and the filter at 56-59 short-circuits. That is
consistent with the 08/20 note and is now established on a corrected mechanism.

The alternative - teaching the filter about both namespaces - is more code and
buys nothing the chat path needs.

---

## 3. THE DISPATCH BRANCH DIVERGENCE - NEW FINDING

`server\routes.py`, read 08/29, lines 155-185.

**Streaming predicate, line 157:**
`if agent is not None and bus is not None and (request_body.tools or request_body.agent):`

**Non-streaming predicate, line 162:**
`if agent is not None:`

**These are not the same test and the difference is material.** On the streaming
path the CLIENT decides whether an agent runs, by sending `tools` or `agent`.
On the non-streaming path the client CANNOT opt out - if an agent exists on app
state, every non-streaming chat request goes through `_handle_agent`, receives
the full system prompt and tool definitions, and carries an executor.

EVIDENCE, in order:
- Probe body sent `stream: false`, no `agent`, no `tools`.
- Response carried `prompt_tokens: 3979` for a six-word prompt.
- Traceback from the failed run showed `routes.py:168` -> `_handle_agent`
  (routes.py:278) -> `native_openhands.py:406`.
- Then confirmed by reading the predicate at 162.

CONSEQUENCE FOR THE REGISTER: the confirmation gate is REACHABLE on the
non-streaming chat path, with an executor whose `agent_id` is
`native_openhands`. W16 listed the executor construction site for the WS confirm
path as NOT YET ESTABLISHED. For this path it now is.

Lines 163-170 also carry the `openjarvis-offload-sync-handlers-v1` marker and a
comment recording the 253 s event-loop pin with 23 consecutive `/health`
timeouts that motivated the `asyncio.to_thread` offload. That is good SDP
material - a measured defect with its fix documented at the site.

---

## 4. GRAY'S RULING - SOCKET AUTHENTICATION DEFERRED

**RULING: DEFER. Lock it down once the system is up and operational.**

Do not revisit this inside a patch. It is settled.

CONTEXT THAT PRODUCED THE RULING:
- Gray has NOT established his CA yet, so the Step-CA / mTLS option is not
  currently available.
- Scope is family members connecting remotely to home servers.
- No route in OpenJarvis has auth today. `tools_router` handlers carry no
  `Depends`, and neither do the other v1 routes.
- W16 established that NO BROWSER CLIENT HAS EVER AUTHENTICATED on this socket.
  Every `authed=True` in the log came from a Python probe script. The system is
  already running unauthenticated.
- The bind is `127.0.0.1:8010`, confirmed from six startup lines in
  `backend.log` spanning 08/24 through 08/29.
- Anything that can reach loopback is already a process on that Windows box and
  can call the unguarded HTTP routes directly. Redacting `confirm_id` on the
  socket protects one interior door in an unlocked house.

**CONSEQUENCES, all three of which must reach revision D:**

1. Auth on `/v1/agents/events` is DELIBERATELY ABSENT, bounded to loopback,
   deferred by decision on 08/29. It is a recorded posture, not an oversight.
2. Barrier 3 is RETIRED as a barrier. The v2 redaction shipped in W12 through
   W14 becomes conditional on the bind rather than on a token.
3. **THE BIND ASSERTION IS MANDATORY AND IT MUST LOG.** Gray stated this
   explicitly and repeated it. The condition that relaxes the redaction must be
   a RUNTIME CHECK that reads the actual bind address and EMITS A LOG LINE AT
   STARTUP. Not a comment. Not a constant. Not an assumption in a docstring.

WHY 3 IS NON-NEGOTIABLE: the day someone binds `0.0.0.0` for a Tailscale test,
the confirm channel opens to the tailnet with no code change and no log line.
That is the same silent-failure class as the bare `except Exception` at
`api_routes.py:946` and the uninstrumented queue drop at `ws_bridge.py:74-75`.
This codebase has a documented pattern of failing quietly and it has cost weeks.

OPTIONS PRESENTED AND NOT CHOSEN, recorded so the next window does not re-derive
them when the deferral ends:
- **A. Fix token delivery.** Frontend fetches the token over HTTP at startup and
  appends it to the WS URL. About a dozen lines. Weak unless the HTTP endpoint
  is itself guarded; honest only as explicit scaffolding.
- **B. Perimeter identity.** Cloudflare Access or Tailscale asserts identity
  before the request reaches OpenJarvis. Backend stays on loopback. Matches the
  Zero Trust posture already built in Graystone Lab, and gives per-person
  attribution without OpenJarvis implementing accounts. Cost: trust becomes a
  deployment property, which is exactly what the bind assertion guards.
- **C. Notification-only socket.** The WS carries "a confirmation is pending";
  the client retrieves details and answers over authenticated HTTP.
  `confirm_id` never crosses the socket. Makes the v2 redaction correct as
  designed instead of self-defeating, and downgrades the lossy `put_nowait`
  drop from "tool call stranded for the full TTL" to "delayed until the next
  poll". Claude's recommendation on the merits.
- **D. mTLS via Step-CA.** Strongest, worst fit for family users, and blocked
  until the CA exists.

B and C compose. That is the shape to revisit when the deferral ends.

TRANSPORT CONSTRAINT THAT SURVIVES ANY CHOICE: browsers and Tauri webviews
CANNOT set headers on a WebSocket handshake. Only three carriers exist - query
parameter, cookie, or `Sec-WebSocket-Protocol` abused as a token field. Any
future design that assumes a bearer header is dead on arrival.

---

## 5. THE OLLAMA OUTAGE - INFRASTRUCTURE, NOT CODE

Gray identified the cause and it closes W16's section 1.5 correctly.

**The Ollama guest on the R730xd is not set to start at boot.** A power outage
on 08/28 took it down. OpenJarvis started 08/29 08:42:44 with no inference
engine reachable and bound the litellm fallback. The engine binds at startup and
never re-evaluates, so restarting the Ollama service mid-window did not move it.

MEASURED THIS WINDOW:
- Non-streaming chat probe against PID 13076: **500 in 36 ms**, body was the
  generic FastAPI string.
- `backend.log` tail carried the full traceback ending
  `ModuleNotFoundError: No module named 'litellm.responses.mcp'` at
  `litellm\main.py:1112`, reached via `engine\litellm.py:65`.
- Ollama host 172.16.33.200:11434 returned **UP, 29 models**, including
  `qwen3-coder:30b` at 18,556,700,761 bytes.
- Gray restarted the backend manually.
- Same probe re-fired: **HTTP OK in 24.3 s**, content `OK`, finish_reason
  `stop`, usage 3979/2/3981, complexity tier `trivial`.

**THE FIX IS ONE CHECKBOX AND IT IS NOT IN THIS REPO.** Proxmox per-VM "Start at
boot" on the R730xd Ollama guest. This was already logged as a gap on 07/31
after the previous outage, when the Ollama VM was the only guest that failed to
come back. It has now cost two windows. Setting it removes the failure mode
permanently.

SECONDARY OBSERVATION, parked on open item 12, NOT chased: the litellm fallback
is a broken install, so the no-engine condition surfaces as a stack trace rather
than a clean "no inference engine available" error. Cosmetic while Ollama is up.
It belongs with the 65-package venv mutation.

**`Engine:` DOES NOT APPEAR IN `backend.log`.** A grep across the entire file
returned zero hits, with two of three patterns hitting as the control. W16
stated the backend "bound `Engine: litellm` at startup" - that string is not in
this log. Either W16 read it elsewhere (the UI, or `engine.log`) and attributed
it wrongly, or the engine binding is not logged at all. **If it is not logged,
that is a gap worth closing** - the engine a process is bound to should be
recoverable from the log, especially given that it never re-evaluates.

---

## 6. EXECUTION PATHS REGISTER

Carried from W16, plus one path materially advanced.

- Orchestrator `ask()` via `system\orchestrator.py`.
- Managed-agent SSE via `_stream_managed_agent()` in
  `server\agent_manager_routes.py`.
- `routes.py` chat dispatch branches 1a/1b/1c/1d.
- The confirm-gate flow as verified, W14 Appendix B.1, stages 1 through 11b.
- WS confirm delivery path, W16 section 2. Entry point
  `@router.websocket("/v1/agents/events")` at `ws_bridge.py:81`.
- **UPDATED - NON-STREAMING CHAT PATH.** Entry
  `POST /v1/chat/completions` -> `routes.py:162` (predicate `agent is not
  None`, NO client opt-out) -> `asyncio.to_thread(_handle_agent, ...)` at 168
  -> `routes.py:278 agent.run(...)` -> `native_openhands.py:406` ->
  `agents\_stubs.py:178 self._engine.generate(...)`. **Executor: the one built
  at `agents\_stubs.py:325` with `agent_id="native_openhands"`.** Confirmation
  gate: LIVE. Human present: YES. Runs on a worker thread, so the loop stays
  free to serve `POST /v1/tools/confirm`.

---

## 7. SDP / SDD FEED FROM THIS WINDOW

REVISION D MUST NOW CARRY, in addition to everything W16 section 4 listed:

- **Section 2 of this document in full.** The agent_id resolution chain is the
  answer to a question that has consumed parts of several sessions and it
  belongs in the architecture chapter as a worked example of how identity
  resolves through a fallback ladder.
- **The two-namespace finding.** Class identity (`native_openhands`) versus
  instance identity (`uuid4().hex[:12]` from `manager.py:168`), unreconciled,
  compared by string equality at `ws_bridge.py:56-59`. This is an architectural
  defect, not a wiring bug, and it will resurface anywhere else the two
  namespaces meet.
- **The barrier 2 correction.** W16's empty-string mechanism is wrong. Any
  revision D text derived from it must be rewritten.
- **The dispatch branch divergence,** section 3. Two predicates for the same
  logical decision, one client-controlled and one not.
- **The auth deferral,** section 4, as a recorded posture decision with its
  date, its rationale, and the bind assertion as its enforcing control.
- **The engine-binding log gap,** section 5.

METHODOLOGY CHAPTER MATERIAL:

- **The retrieval failure (W17-R1).** W16 closed by specifying a hunt for an
  answer that was already in the record from 08/20. The next window resolved it
  in two commands. The cost of not searching the record first was an entire
  window's closing sequence plus the risk of a wrong mechanism propagating into
  revision D. Pair this with W16-R4: that rule says do not trust inherited
  claims, this one says find them before hunting.
- **Predicate divergence (W17-R2).** A worked example of carrying a verified
  fact across a boundary where it does not hold. The 08/23 streaming predicate
  was correctly measured and correctly recorded; it was applied to a branch
  nobody had read.
- **Token counts as branch fingerprints (W17-R3).** A free, non-interactive
  discriminator available on every non-streaming response.
- **Infrastructure versus code (W17-R4).** Two windows spent exchanges treating
  an outage symptom as a defect. The owner identified the cause in one message.

---

## 8. OPEN ITEMS, ORDERED

Renumbered from W16. Item 1 has a ruling, item 2 is CLOSED.

1. **6E - TWO BARRIERS REMAIN, BOTH SPECIFIED.** Barrier 1 (hook guard) and
   barrier 2 (namespace mismatch). Barrier 3 retired by the section 4 ruling.
   Ready for design.
2. **CLOSED.** Which executor serves the chat path and does it get a real
   `agent_id`. Answer: `agents\_stubs.py:325`, value `native_openhands`. See
   section 2.
3. **W10 is two documents that disagree.** Unchanged.
4. **W3 through W6 have no handoff anywhere.** Unchanged.
5. **Destructive mailbox tools are ungated at the spec level.** Only
   `agent_tools.py:289` (agent_kill), `git_tool.py:283` (git_commit),
   `shell_exec.py:71` declare `requires_confirmation=True`. Needs a Gray
   decision.
6. **Four auto-approve sites live** in `server\agent_manager_routes.py`
   (720-721, 1202-1206, 1562-1563, 1639-1640). Needs a Gray decision.
7. **Silent frame drop on queue overflow.** `ws_bridge.py:74-75`, bare
   `except (RuntimeError, asyncio.QueueFull): pass`, maxsize 100,
   uninstrumented. Needs a counter.
8. **`"reaped": false` on timeout resolutions** unexplained.
9. **Four `[DEBUG]` prints in `cli\serve.py`** at 268, 280, 281, 513.
10. **`_stubs.py` EOL baseline contradiction** unresolved.
11. **08/05 GitLab history damage below the tip** still unassessed.
12. **65-package venv mutation on start,** now with two probable symptoms: the
    broken litellm install, and the parent/child interpreter split.
13. **`/v1/cloud/reload` injects arbitrary env keys with no whitelist,**
    `routes.py:571-578`. Loopback-bound, not exploited. Needs a Gray decision.
14. **The engine binds at startup and never re-evaluates.** Now understood as
    behavioral rather than defective, but see item 16.
15. **NEW. Ollama guest has no autostart on the R730xd.** Infrastructure, not
    code. One Proxmox checkbox. Has now caused two outages. Logged 07/31, still
    open.
16. **NEW. The bound engine is not recorded in `backend.log`.** Given item 14,
    a process can run for hours on a fallback with nothing in the log naming it.

CLOSED THIS WINDOW: open item 2 (chat-path executor identity), on a direct read
of the construction site and the full class-attribute inventory.

---

## 9. NEXT ACTIONS, ORDERED

1. **Re-verify the carried claim in section 2.3** - that `system\builder.py` and
   `system\orchestrator.py` never pass `agent_id`. One grep with a positive
   control. It is the only unverified link in the chain and everything in 6e
   rests on the chain.
2. **Design the 6e change.** Now bounded to: the `useAgentEvents` line 40 guard
   (barrier 1), a chat-path mount that connects with NO `agent_id` parameter
   (barrier 2), and the bind assertion with its startup log line (section 4,
   mandatory). Design it whole, apply it in verified isolation per the standing
   rule.
3. **Revision D of the SDP.** It carries a known false statement (the
   fail-closed claim, W16 D1) and now also needs the barrier 2 correction.
4. **Set Proxmox autostart on the Ollama guest** (open item 15). Not code work,
   costs one checkbox, removes a recurring failure mode.

Do not skip to 2. Action 1 is one command and it is the last unverified link in
the chain that action 2 depends on.

---

## APPENDIX A. DISCREPANCY REGISTER

### D1. W16's barrier 2 mechanism - FALSE, CORRECTED
- CLAIMED BY: W16 section 1.4, that a chat-path executor is "constructed without
  an explicit `agent_id`" and therefore publishes `agent_id: ""`.
- FOUND: `agents\_stubs.py:325-329` passes `agent_id=_aid` explicitly, and
  `_aid` resolves to the class attribute `native_openhands`.
- HOW W16 GOT THERE: it read the default at `tools\_stubs.py` and predicted the
  runtime value without opening the construction site. That is W16's own rule
  W16-R3 (read the definition before predicting from the call site) inverted -
  it predicted from the definition without reading the call site.
- ALSO: the correct answer was already in the record from 08/20 and was not
  consulted. See W17-R1.
- DISPOSITION: barrier 2 SURVIVES, mechanism corrected to a namespace mismatch.
  The conclusion held; the reasoning did not. Revision D must not inherit the
  empty-string framing.

### D2. Claude predicted the wrong dispatch branch - CLAUDE'S ERROR
- CLAIMED BY: Claude, exchange 9, that a `stream: false` body with no `agent`
  and no `tools` would land on a branch with no executor and no reachable gate.
- FOUND: `routes.py:162` is `if agent is not None:` with no client-facing
  condition. An agent ran. `prompt_tokens: 3979` and the traceback both show it.
- CAUSE: carried the streaming predicate from the 08/23 record onto a branch
  nobody had read.
- DISPOSITION: rule W17-R2. The error was productive - it surfaced the branch
  divergence in section 3 - but it was still an unverified claim stated as fact.

### D3. Claude treated an infrastructure symptom as a code defect - CLAUDE'S ERROR
- WHAT: spent exchanges 8 and 9 pursuing the litellm `ModuleNotFoundError` as a
  venv defect, including a stack-trace read.
- FOUND: Gray identified it immediately as what happens when no inference engine
  is available, caused by the Ollama guest not starting after the 08/28 power
  outage.
- IMPACT: cost roughly two exchanges. W16 had already recorded the same trace
  and also framed it as a broken install.
- DISPOSITION: rule W17-R4. Establish that dependencies are up before treating a
  runtime failure as a defect.

### D4. W16's `Engine: litellm` startup line - NOT IN THE LOG
- CLAIMED BY: W16 section 1.5, that the backend "bound `Engine: litellm` at
  startup".
- FOUND: zero `Engine:` hits across the whole of `backend.log`, with the uvicorn
  patterns hitting as the control.
- DISPOSITION: unverified in W16 and not inherited here. Either it was read
  somewhere else, or the binding is not logged. Filed as open item 16.

### D5. Traceback attribution - DELIBERATELY NOT CLAIMED
- WHAT: the traceback in the log tail could not be timestamp-matched to Claude's
  probe within the 60-line window.
- DISPOSITION: NOT attributed at the time, per W16-R2. It was later corroborated
  independently by the token count and the predicate read, so the conclusion
  stands on evidence that does not depend on the attribution. Recorded as a case
  where withholding a claim cost nothing.

---

## APPENDIX B. GIT AND SYSTEM STATE AT WINDOW CLOSE

| Property | Value |
|---|---|
| HEAD | `38e907d` on `main` - CARRIED FROM W15, NOT RE-VERIFIED SINCE |
| Commits this window | NONE |
| Files modified this window | NONE |
| Backend process | RESTARTED by Gray mid-window. Pre-restart PID 13076 (started 08/29 08:42:44). Post-restart PIDs NOT CAPTURED - see below |
| Bind | `127.0.0.1:8010`, confirmed on all six startup lines 08/24 through 08/29 |
| Engine | OLLAMA, live. Verified by a successful completion in 24.3 s after restart |
| Ollama host | 172.16.33.200:11434 UP, 29 models, `qwen3-coder:30b` present |

**GAP, RECORDED HONESTLY: the post-restart PIDs and start time were never
captured.** The restart was verified by BEHAVIOR (a working completion where
there had been a 500) rather than by process identity. That is sufficient
evidence that the process changed, since the engine binds only at startup. But
it means the next window cannot identify the current process by PID from this
document. Re-measure with `Get-CimInstance Win32_Process` before relying on it,
and remember the PID-REUSE HAZARD from 08/19: identify a process by
CreationDate, never by PID alone across a restart.

STILL DIRTY IN THE TREE, untouched and intentionally so: 12 modified files and
roughly 150 untracked probe and patch scripts, plus `WS-6E-BUNDLE-2026-08-29.md`
from W16. None of it belongs to this work. Do not clean it up as a side task.

---

## APPENDIX C. THE 550B BUNDLE - CARRIED FORWARD

Not used this window; every question was answerable with targeted reads.

Use it when a question needs whole files. Generate
`WS-6E-BUNDLE-<date>.md` at the repo root from a fixed file list, each fenced
with a language tag and a `## FILE:` header, with a loud MISSING line for any
path that does not resolve. Feed it to
`openrouter/nvidia/nemotron-3-ultra-550b-a55b` with NARROW questions about code
facts. Do not ask it for conclusions about behavior - it reads code as designed
and reports the happy path, with no access to logs or negative results. Its
answers are CLAIMS TO VERIFY. W16 Appendix B has the full pattern and the
observed cost (58.1 s, free tier, one turn).
