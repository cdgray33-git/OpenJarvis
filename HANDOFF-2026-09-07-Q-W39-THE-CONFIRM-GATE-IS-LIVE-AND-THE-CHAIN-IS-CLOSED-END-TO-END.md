# HANDOFF 2026-09-07 Q / W39 - THE CONFIRMATION GATE ON THE CHAT PATH IS INSTALLED, LIVE, AND FAILS CLOSED, PROVEN END TO END THROUGH A FOUR-LINK CHAIN. AND THE GATE HAS A SECOND DEATH MODE WE NEVER AUDITED FOR: A CALLBACK THAT EXISTS AND ALWAYS SAYS YES. NO CODE WAS MODIFIED.

Predecessor: HANDOFF-2026-09-07-P-W38-ENFORCE-TOOL-CONFIRMATION-HAS-NO-CONSUMER-MONITOR-OPERATIVE-IS-THE-DEFAULT.md

All evidence in this window is dated 09/07 and was produced live in-window by
direct greps, direct file reads, and two Python invocations against the real
`load_config()` in the venv. The 550B cloud model was NOT used this window;
section 8 records why.

---

## 0. READ THIS FIRST - WHERE THE SYSTEM ACTUALLY SITS

**Nothing in the tree was modified this window. The backend was not restarted.
No probe was built. No patch was applied. No commit was issued.**

`411cd59` is carried forward as HEAD on assertion. **W38 inherited it on
assertion and did not re-verify it. This window did not re-verify it either. It
is now TWO windows removed from its last actual check.** If the next window
needs HEAD to be certain, re-run the check. Do not inherit it from this line.
This is the second consecutive handoff carrying that warning; treat the next
inheritance as a defect in our own process, not a note.

Two commands executed code this window, both read-only calls to
`openjarvis.core.config.load_config()`. Everything else was a grep or a read.

**W38's next-action 1 was MIS-TARGETED and is formally retired. See 2.1.**

**THE HEADLINE: the chat-path confirmation gate is live. Not inferred - every
link in the chain that installs it is now verified from source or live config.
The 08/21 live result (a 120.007 s block) was the gate working correctly, and
we now know exactly why it was reachable.**

---

## 1. WHAT WAS DONE, IN ORDER

1. Read `agents\manager.py:495-565` - the range W38 named as "the single read
   that answers all three." **It answered none of them.** See 2.1.
2. Grep of `manager.py` for `def create_agent|MonitorOperativeAgent|
   monitor_operative|confirm_callback|memory_backend|session_store`.
3. Repo-wide grep across `src\openjarvis\*.py` and `src\openjarvis\**\*.py` for
   `MonitorOperativeAgent\(|confirm_callback|memory_backend|session_store`.
   **This is the command that produced most of this window's value.**
4. Read `cli\serve.py:300-322` - the `_server_confirm_callback` body.
5. Read `cli\serve.py:282-300` - the env-var guard wrapping it.
6. Shell env check plus grep of `.env` and `src\openjarvis\**\*.py` for
   `OPENJARVIS_CONFIRM_INTERACTIVE|accepts_tools`.
7. Grep of `cli\serve.py` for `agent_cls\s*=|agent_type|model_name\s*=`.
8. Read `cli\serve.py:230-250` - the agent-resolution block.
9. `load_config()` call 1: `server.agent`, `server.model`,
   `agent.default_agent`. **Included a `LOADERS:` probe in the same run so a
   wrong function name would not have cost an exchange.**
10. `load_config()` call 2: `intelligence.default_model`, `agent.max_turns`,
    `security.profile`, `security.enforce_tool_confirmation`.
11. Grep of `cli\serve.py` for `getLogger|^import logging|^from logging|
    logger\.` and separately for `print\(` - the pre-patch safety check for
    next-action 1. See section 4.

---

## 2. THE FINDINGS

### 2.1 NEGATIVE RESULT - W38's NEXT-ACTION 1 WAS AIMED AT THE WRONG FILE

W38 asserted that `agents\manager.py:500-560` was "the single read that answers
all three" open questions (does the managed-agent path pass `memory_backend`,
`session_store`, `confirm_callback`). **It answers none of them.**

`:522` (`config.pop("agent_type", "monitor_operative")`) sits inside
`create_from_template` (`:510-532`), which does template lookup, key filtering,
prompt expansion, and then hands a STRING to `self.create_agent(...)` at `:532`.
Lines `:534-565` are the message queue (`send_message`, `store_agent_response`).
No construction, no kwargs.

Confirmed by grep rather than by the single read: **`manager.py` has ZERO hits
for `confirm_callback`, `memory_backend`, `session_store`, or
`MonitorOperativeAgent`.** Its only four hits are the `agent_type` string at
`:24` (a SQL column default), `:162` (`def create_agent`), `:165` (its default
param), and `:522`. **`manager.py` is a DB/registry layer. It constructs no
agent at any line.**

**METHOD LESSON, and it is the same class as W38's own "search the schema"
rule:** W38 derived that line range by reasoning about what SHOULD be near
`config.pop("agent_type", ...)`, not by locating the construction site. **A
one-line grep for the symbols would have aimed it correctly for a fraction of
the cost. Grep for the SYMBOL before spending a read on a RANGE.**

### 2.2 THE GATE HAS A SECOND DEATH MODE. THIS IS THE MOST IMPORTANT FINDING IN THE WINDOW.

For months the confirmation question has been asked as a binary: **is
`_confirm_callback` None or not?** That is Defect 6 and it is only two thirds
of the picture. **The confirm state of this tree is THREE-VALUED:**

1. **REAL GATE** - `cli\serve.py:308` `_server_confirm_callback`. The ONLY
   genuine gate in the tree.
2. **AUTO-APPROVE** - a callback that EXISTS and unconditionally returns True.
   **FIVE sites:** `server\agent_manager_routes.py:721`, `:1206`, `:1563`,
   `:1640` (all `lambda _prompt: True`) and **`cli\ask.py:356`
   (`lambda prompt: True`) - which was NOT on the carried four-site list.**
3. **ABSENT** - None. Defect 6 proper.

**Why this matters mechanically:** at `tools\_stubs.py:270` the guard is
`if not self._interactive or self._confirm_callback is None`. An auto-approve
lambda PASSES that guard. Execution proceeds to `:309`, `_approved =
self._confirm_callback(prompt)`, which returns True, and the tool runs. **From
outside, an auto-approve path is indistinguishable from a protected one. It
emits, it registers, it looks correct in every log - and it never blocks
anything.**

**CONSEQUENCE FOR THE SDP AND FOR EVERY FUTURE AUDIT: a gate audit that greps
only for None is structurally incapable of finding two thirds of the failures.
Any future confirm-state question must be asked as "which of the three."**

### 2.3 THE FOUR-LINK CHAIN - ALL FOUR LINKS NOW VERIFIED

The chat-path gate is installed only if FOUR conditions hold, all in
`cli\serve.py`. Any one failing kills the gate silently, with no log line.

| # | Link | Line | Status 09/07 | Evidence |
|---|------|------|--------------|----------|
| 1 | `if agent_key:` where `agent_key = agent_name or config.server.agent` | `:234-235` | **PASS** | `server.agent = 'native_openhands'` from live `load_config()` |
| 2 | `AgentRegistry.contains(agent_key)` | `:240` | **PASS** | agent loaded cleanly at the 08/21 restart |
| 3 | `getattr(agent_cls, "accepts_tools", False)` | `:293` | **PASS** | `accepts_tools = True` on the `ToolUsingAgent` BASE, `agents\_stubs.py:292` |
| 4 | `OPENJARVIS_CONFIRM_INTERACTIVE` not in `0/false/no/off` | `:296-304` | **PASS** | var UNSET in shell, absent from `.env`, default is `"1"` |

**LINK 1 HAD NEVER BEEN CHECKED IN ANY WINDOW.** It is the widest of the four:
if `agent_key` is falsy, `agent` stays None, and NOTHING below `:235` executes -
no tool loading (`:247`), no gate block (`:293`), no construction (`:319`).
`routes.py` then falls through to `_handle_direct` and the UI simply looks
toolless. **A single empty config value silently disables tools AND the gate
together, and the only symptom is an agent that seems not to try.**

### 2.4 `_server_confirm_callback` FAILS CLOSED - CONFIRMED IN SOURCE

`cli\serve.py:308-312`, read directly:

```
def _server_confirm_callback(_prompt: str) -> bool:
    _cid = _confirm_stubs.CURRENT_CONFIRM_ID.get()
    if not _cid:
        return False
    return _cr.wait(_cid) == _cr.APPROVED
```

No confirm id means denial, not approval. This is the correct shape and it
matches the 6d spec exactly. `:314-317` sets `agent_kwargs["interactive"] = True`
and the callback; `:319` constructs. **`openjarvis-confirm-live-v1` is doing
precisely what it was designed to do.**

### 2.5 THE GATE IS MODEL-INDEPENDENT, BUT THE MODEL DECIDES WHETHER IT EVER FIRES

`accepts_tools` is a property of the AGENT CLASS resolved at `:241`. The model
is a separate value resolved at `:223` (`config.server.model or
config.intelligence.default_model`). **Changing models does not arm or disarm
the gate.**

But: **a live gate that is never reached is externally indistinguishable from an
absent one.** Defect 1 sits UPSTREAM of Defect 6. If the model narrates instead
of emitting a tool call, the dispatch never happens and the gate never runs.
This is exactly the trap that produced the 08/21 false headline ("gate never
reached"), later overturned by RAWGEN.

**STANDING RULE FOR EVERY FUTURE GATE TEST: prove a tool call was EMITTED
before drawing any conclusion about the gate. Log-absence at the gate is
consistent with both "gate broken" and "nothing ever asked it."**

### 2.6 `memory_backend` IS WIRED FURTHER THAN W38 ESTIMATED

W38 moved persistent recall from "unbuilt" to "built upstream, possibly
unwired." **The repo-wide grep moves it again: WIRED AT THE SERVER LEVEL.**

- `cli\serve.py:489` `memory_backend = None` -> `:497`
  `memory_backend = MemoryRegistry.create(...)` -> `:511` `_t._backend =
  memory_backend` (injection into agent tools) -> `:592` passed onward.
- `server\app.py:222` `app.state.memory_backend = memory_backend`.
- `server\routes.py:56-83` reads it ON THE CHAT PATH.
- `system\orchestrator.py:167-168` passes BOTH `session_store` AND
  `memory_backend` into `agent_kwargs`.
- `server\agent_manager_routes.py:1616/:1649` passes `session_store` on the
  managed-agent path.
- `system\builder.py:159/:165/:202/:280/:289` resolves and threads both.
- Consumers: `api_routes.py` (6 sites), `upload_router.py` (10 sites),
  `sdk.py:525-576`, `cli\ask.py:216-792`.

**So `MonitorOperativeAgent`'s eight None-guards are NOT obviously inert - a
backend exists at runtime on at least the orchestrator and server paths.**

**STATED HONESTLY: this is a source reading. No managed agent was run. No recall
was observed. The estimate moved; nothing was validated. That distinction is
W38's section 3 method correction and it still governs.**

### 2.7 CONFIG VALUES READ LIVE - FOUR QUESTIONS CLOSED IN TWO CALLS

```
server.agent                        = 'native_openhands'
server.model                        = ''          -> falls through to intelligence.default_model
agent.default_agent                 = 'native_openhands'
intelligence.default_model          = 'qwen3-coder:30b'
agent.max_turns                     = 15
security.profile                    = 'personal'
security.enforce_tool_confirmation  = True
```

Note the method: the first call included a `LOADERS:` introspection print
BEFORE the `load_config()` call, so a wrong function name would still have
returned the right one in the same run. **Cheap insurance on any call into an
unfamiliar module; worth repeating.**

### 2.8 CONFIG FILE IS NOT IN THE REPO ROOT

`.\config.toml` does not exist. A `Select-String` against it errored. Config
lives under `C:\Users\Admin\.openjarvis\`. **Do not guess config paths - ask
`load_config()`, which returns the value the server actually resolves rather
than the one a file appears to contain.** One exchange lost.

---

## 3. THE DIVERGENCE CHAPTER - ENTRIES READY TO WRITE

W38 established that the author's docs and the implementation disagree in both
directions. Three more entries, all confirmed against LIVE config this window
rather than against notes.

### 3.1 DOCUMENTED MODEL vs ACTUAL MODEL
Documented: `qwen3:8b`. Actual: **`qwen3-coder:30b`**, via
`config.intelligence.default_model` (since `server.model` is empty). Matches the
08/21 live run. **Docs divergence, not a config problem.**

### 3.2 DOCUMENTED `max_turns` vs ACTUAL
`agents.md` documents default 3. Live value is **15**. Confirmed from primary
source in W38 and from live config here. **Divergence stands.**

### 3.3 THE SHARPEST ENTRY: A SECURITY CONTROL THAT IS ENABLED AND INERT
`security.enforce_tool_confirmation = True`. W38 proved by full `SecurityConfig`
field census that **nothing reads it.** So:

- It is documented in `configuration.md` AND `security.md`.
- It is defined in the dataclass, written into generated configs, and asserted
  by `tests\core\test_config.py:121`.
- It is **True**.
- **It does nothing.**

Meanwhile the gate that DOES protect the chat path is ours, driven by an
**undocumented environment variable**.

**THE HAZARD, STATED FOR THE SDP: the config layer and the enforcement layer are
disconnected in BOTH directions.** An operator reading the author's
documentation would set `enforce_tool_confirmation = false` and believe the gate
was off - **it would still be live.** Or set it true and believe the
managed-agent path was protected - **five auto-approve stubs run there.** The
documented control is a decoy in both directions.

**CANDIDATE FIX, NOT THIS WINDOW'S WORK:** have `serve.py:296` consult
`config.security.enforce_tool_confirmation` alongside (or instead of)
`OPENJARVIS_CONFIRM_INTERACTIVE`, making the documented flag real. Deliberately
NOT proposed as an action - the current patch is verified and nothing should be
stacked on it (08/17 rule). Recorded as the candidate so it is not re-derived.

### 3.4 `profile = "personal"` - NARROWED, STILL OPEN
It loads and is present on the config object. Outside `config.py` it appears
only in a `doctor` status message. **Still unproven: whether `config.py` BRANCHES
on it at load time.** Narrowed from "what does profile do" to a single question
about one file. Low priority.

---

## 4. NEXT-ACTION 1 IS FULLY SPECIFIED AND SAFE TO BUILD - THE `print()` FIX

Gray asked whether all investigation was complete before writing the patch
script. **It was not, and the check found two things.** Recording that, because
the instinct to verify first is what prevented a bad patch.

### 4.1 THE TWO CONDITIONS THAT HAD TO BE PROVEN FIRST
1. **Does a logger exist in this module's scope?** If not, `logger.info(...)`
   raises NameError at startup, the broad `except Exception` at `:320` swallows
   it, and `agent` is left None - trading an unreadable instrument for a
   silently dead agent. **PROVEN: `logger = logging.getLogger(__name__)` at
   `serve.py:25`.**
2. **Is that logger captured by `backend.log` at INFO?** **PROVEN:** `:69-72`
   clears root handlers, adds the `RotatingFileHandler`, and sets
   `root_logger.setLevel(logging.INFO)`. INFO records will land.

### 4.2 EXACTLY FOUR TARGET LINES - AND A TRAP
Bare `print(` appears at **`:268`, `:280`, `:281`, `:513` ONLY**. Every other
print in the file is `console.print` (Rich, deliberate startup UI - 18 sites).
**A naive `print(` match hits 22 lines and would wreck the startup display.
Anchor on the four full lines.**

```
268: print(f'[DEBUG] allowed={allowed}', flush=True)
280: print(f'[DEBUG] registry_keys={list(ToolRegistry.keys())}', flush=True)
281: print(f'[DEBUG] tools_loaded={[t.__class__.__name__ for t in tools]}', flush=True)
513: print(f"[DEBUG] wired memory_backend into {_wired} agent tool(s)", flush=True)
```

**`:513` IS THE FOURTH PRINT AND IT WAS NOT ON ANY CARRIED LIST.** The register
has tracked 268/280/281 since 08/20. **`:513` reports the count of agent tools
that received the memory backend - precisely the number that would tell us
whether the 2.6 recall wiring takes effect at startup. A fix that converts only
three leaves the most valuable of the four dark.**

### 4.3 HAZARD IN THE SAME FILE - `serve.py:552` IS MOJIBAKE
`logger.info("Credentials loaded <thousands of garbled bytes> %s", ...)` -
a separator character that has been through repeated encoding round-trips.
**Pre-existing, not caused by us, cosmetic in effect but enormous in bytes.**

**It sits in the file we are about to rewrite.** Therefore the patch must:
- anchor on the four exact lines, never rewrite the file wholesale from a
  re-encoded read;
- **NOT normalize encoding** and not touch `:552`;
- read and write with `UTF8Encoding($false)` / explicit encoding and prove a
  read-write round trip is byte-identical BEFORE applying;
- assert the CRLF/bare-LF counts are unchanged (`serve.py` was 574 CRLF / 22
  bare LF pre-6d, 605 CRLF / 22 bare LF post-6d - **re-measure, do not inherit**);
- carry an encoding control that reads `:552` before and after and asserts the
  bytes are identical;
- `py_compile` after.

### 4.4 THE CHANGE ITSELF
`print(` -> `logger.info(` on those four lines, dropping `flush=True`
(meaningless for the logging module). Preserve the f-strings as-is. Marker
suggestion: `openjarvis-debug-readable-v1`. Take a `.bak_debugreadable_<ts>`
copy and record the restore command in the rollback register BEFORE applying.

**Requires a backend restart to take effect. The patch is verifiable on disk
without one; the OUTPUT is not verifiable until the restart.** Do not claim the
instrument is readable until a restart has produced the lines in `backend.log`.

---

## 5. SDP FEED - THIS WINDOW'S DEPOSIT

### 5.1 THE GUARD, IN PLAIN LANGUAGE (09/02 PIN)
Think of the confirmation gate as a guard at a door. For months we asked one
question: **is there a guard on duty?** But there are three possible answers,
not two. There can be **no guard at all** - nobody is there, and anyone walks
through. There can be a **real guard** who stops you and waits for permission
before letting you in. Or - and this is the one we never looked for - there can
be a **guard who waves everybody through without ever looking up.**

From outside the door, the third one looks exactly like the second. There is
someone standing there. There is a uniform. Everything appears correct. But
nothing is ever actually stopped. **We spent months checking whether anyone was
standing at the door, and never checked whether the person standing there was
actually looking at anyone.**

The good news: on the main chat door, we now know there is a real guard, and we
know he refuses entry when he cannot tell who is asking. The bad news: on five
other doors into the same building, the guard waves everyone through.

### 5.2 TECHNICAL, FOR THE ARCHITECTURE CHAPTER
- The three-valued confirm state (2.2), with all five auto-approve sites named.
- The four-link chain (2.3) as a table, with the note that link 1 disables tools
  and gate together and produces no log line.
- `_server_confirm_callback` fail-closed semantics (2.4).
- Gate is agent-scoped, not model-scoped; Defect 1 is upstream of Defect 6 (2.5).
- The config/enforcement disconnect (3.3) as a HAZARDS-register entry.

### 5.3 EVIDENCE-STANDARD ENTRIES
- **Grep for the symbol before spending a read on a range (2.1).**
- **Ask the loader, not the file (2.8).**
- **Prove the tool call was emitted before judging the gate (2.5).**
- **A gate audit that greps only for None cannot find two thirds of the failures
  (2.2).** This generalizes: an audit is only worth the states it can
  DISCRIMINATE - the same principle as 400-not-404 and the 0.44 s timing bound.

---

## 6. EXECUTION PATHS - REGISTER UPDATE

**PATH 1 (chat, `routes.py` -> `app.state.agent`), gains its confirm properties
as VERIFIED rather than inferred:**
- Entry: `POST /v1/chat/completions`, `server\routes.py:46`.
- Agent constructed at `cli\serve.py:319`, resolved at `:241` from
  `config.server.agent` = `native_openhands`.
- Executor: the agent builds its OWN at `agents\_stubs.py:325`.
  `builder.py`'s executor is NOT on this path (settled 08/20).
- **Confirmation gate: LIVE. Real callback, fails closed. Installed via the
  four-link chain at `:235/:240/:293/:296`, all four links PASS as of 09/07.**
- Model: `qwen3-coder:30b`.
- Human present: yes.
- `memory_backend`: available via `app.state` and injected into agent tools at
  `serve.py:511`.

**PATH 2 (managed-agent SSE, `_stream_managed_agent()`):**
- **Confirmation gate: AUTO-APPROVED at four sites** (`:721`, `:1206`, `:1563`,
  `:1640`). Not absent - defeated.
- `session_store`: **YES**, `:1616/:1649`.
- `memory_backend`: reaches it via `_LightweightSystem` (`:79-127`) and
  `app.state` (`:1433`, `:1790`).
- Default agent type remains `monitor_operative` (W38).
- **`monitor_operative.py:138` forwarding target still UNREAD** - carried.

**PATH 3 (orchestrator `ask()`):** passes `session_store` AND `memory_backend`
(`orchestrator.py:167-168`). Serves the no-human callers. Gate state on this
path NOT established this window.

**PATH 4 (CLI `ask`):** **AUTO-APPROVE at `cli\ask.py:356`.** New to the
register. `cli\chat_cmd.py:123` sets a callback (`_confirm`) whose body is
unread - **it may be a fifth path with a real gate, or a sixth auto-approve.**

---

## 7. DIAGNOSTIC TOOLING REGISTER - 09/06 PIN

**Nothing was built this window. Nothing was run.** One correction and one
addition:

- **CORRECTION: there are FOUR unreadable `[DEBUG] print()` calls, not three.**
  `:513` joins `:268/:280/:281`. See 4.2. The register has under-counted since
  08/20.
- **`serve.py:552` mojibake** recorded as a file-level hazard for any patch to
  `cli\serve.py`. See 4.3.
- Carried unchanged: `telemetry.db` recording since July - **SEARCH THE SCHEMA
  BEFORE BUILDING AN INSTRUMENT**; `backend.log` captures the `logging` module
  only; `bundle_for_cloud.py`; the two W37 telemetry probes; `/api/ps` on the
  ollama host; Patch 4 RAWGEN.
- Untracked files in the repo root now include this handoff. The W37/W38
  artifacts and five `CLOUDBUNDLE-adhoc-*` files remain.

**Standing rule intact: verify where an instrument's output lands at the moment
it is added, never when it is needed. `:513` is the fourth proof of that rule in
two days.**

---

## 8. THE 550B CLOUD MODEL - 08/29 PIN

**Offered by Gray this window and not used. Reasoning recorded because the call
could have gone the other way.**

Every question this window was a SYMBOL question - where does this identifier
appear, what does this line say, what does this config value resolve to. Those
are answered exactly by grep and by `load_config()`, at near-zero cost, with
zero interpretation risk. **The 550B is for questions needing WHOLE FILES we
cannot afford to read in-window. It is not for questions a targeted grep closes,
and a symbol grep is the cheapest instrument we have.**

**WHERE IT WOULD EARN ITS COST NEXT, unchanged from W38 and now better
motivated by 2.6:** `docs\architecture\memory.md` plus `docs\memory_db_schema.md`
together, scoped to the single question **"what does upstream expect a
`memory_backend` to be, and does `MemoryRegistry.create` at `serve.py:497`
produce one that satisfies `MonitorOperativeAgent`'s `.store()` / `.retrieve()`
calls?"** That is a genuine whole-file, multi-file question and it is now the
highest-value 550B job on the board.

**Standing caution, unchanged: the 550B returns cited answers and concluded
answers in the same reply, in the same register. Trust the citations. Treat
every conclusion as a hypothesis.**

---

## 9. THE PROGRAM GOAL - 09/06 PIN

**Goal: a functional executive assistant that performs the duties at a computer
that a human would. Approaching one year. Not yet 50 percent of the initial
requirements. There is still no progress denominator.**

**What this window moved toward the goal:**

1. **The safety precondition for autonomous action is now MET on the chat path.**
   An executive assistant that acts on a computer must be stoppable before
   destructive actions. The gate that does that is verified live end to end.
   **This is not a debugging result; it is a requirements result.** Every future
   autonomy increment on Path 1 now sits on a verified gate rather than an
   assumed one.
2. **The recall estimate moved again** (2.6), from "possibly unwired" to "wired
   at the server level." Remaining work on recall continues to look like WIRING
   and OBSERVATION, not BUILDING.
3. **A counter-weight, stated plainly: the gate protects only what asks for
   protection.** From 08/21: of the twelve allowlisted chat tools, only
   `shell_exec` declares `requires_confirmation=True`. **`mailbox_move_to_trash`
   and `mailbox_empty_folder` do NOT.** The two most destructive tools in the
   assistant's reach are ungated AT THE SPEC LEVEL, and no amount of gate work
   changes that. **A perfect guard cannot stop a tool that never knocks.** For
   an executive assistant handling a family mailbox, this is a requirements-level
   gap, not a defect ticket.

**Requirements denominator: STILL MISSING.** Gray's original initial
requirements document has not been located. Carried unchanged from W37 15.2 and
W38. **Without it, items 1 through 3 above cannot be scored, only described.**

---

## 10. NEXT ACTIONS

**1. APPLY THE `print()` -> `logger.info()` FIX** at `serve.py:268/:280/:281/
:513`. **Fully specified in section 4 - conditions verified, targets enumerated,
hazards named.** The only code change on the board and the one that makes future
instrumentation readable. Restart required before claiming the output is
readable.

**2. READ WHAT `monitor_operative.py:138` HANDS `confirm_callback` TO.** The
parent constructor. Carried from W38 unchanged. Bears on Path 2.

**3. READ `cli\chat_cmd.py:123`'s `_confirm` BODY.** New. It is either a second
real gate or a sixth auto-approve, and the three-valued model (2.2) says we
cannot know which without reading it.

**4. THE 550B JOB:** `docs\architecture\memory.md` + `docs\memory_db_schema.md`,
scoped per section 8.

**5. THE SPEC-LEVEL GAP (9.3):** decide whether `mailbox_move_to_trash` and
`mailbox_empty_folder` should carry `requires_confirmation=True`. **This is a
Gray decision, not a Claude one** - it changes the assistant's behavior on the
family mailbox. Do not patch it unilaterally.

**6. LOCATE GRAY'S ORIGINAL INITIAL REQUIREMENTS.** No progress denominator
without it. Upstream cannot supply one.

**7. CLOSE T-B.** Provable from source and arithmetic alone. Carried from W37
14.8 and 15.6 and W38 - **now THRICE-deferred. Do not let it fall off.**

**8. READ `estimate_prompt_tokens`.** Carried from W37 14.8 item 2, unread
through three windows.

**9. WRITE THE DIVERGENCE CHAPTER** with W38's three entries plus 3.1, 3.2, 3.3,
3.4 from this window, and the fails-quiet pattern.

**10. RE-VERIFY HEAD BEFORE ANY COMMIT.** `411cd59` is now TWO windows deep on
assertion. Section 0.

**11. Carry W37 section 10 items 8-16 and 14.8 items 4, 6, 7 unchanged.**

**Ordering note: item 1 is the only code change and its investigation is
complete - start there and FINISH it (verify, restart, confirm the lines appear
in `backend.log`) before opening item 2. One thing finished before the next is
started, per the 08/17 rule. Do not stack item 3 on an unverified item 1.**

---

## 11. WINDOW CLOSE

**15 interactions. No code modified. No commit issued. Backend not restarted.
Two lines of code executed, both read-only config calls.**

Established this window: one mis-aimed predecessor action retired (2.1), one
structural blind spot in months of gate work found and named (2.2), a four-link
chain closed end to end with the widest link checked for the first time (2.3),
three divergence entries confirmed against live config (3.1-3.4), a fourth
unreadable instrument found (4.2), a file-level encoding hazard located before
it could damage a patch (4.3), and one requirements-level gap stated plainly
enough that it cannot be mistaken for a defect ticket (9.3).

**One patch was NOT written**, because the pre-flight check found two unproven
conditions and one trap. **The check cost one exchange. The NameError it would
have caught costs a silently dead agent and an unknown number of windows finding
out why.**

To W37's standing judgement - EVERYTHING ABOUT STRUCTURE IS VERIFIED, EVERYTHING
ABOUT MAGNITUDE IS ASSUMED - and W38's - AND WHAT THE AUTHOR WROTE IS NOT ALWAYS
WHAT THE AUTHOR BUILT - add:

**AND A CONTROL THAT IS PRESENT, ENABLED, AND DOCUMENTED IS NOT THEREFORE A
CONTROL THAT RUNS. WE PROVED THE GUARD IS REAL ON ONE DOOR AND FOUND FIVE MORE
WHERE HE WAVES EVERYONE THROUGH.**

New untracked file in the repo root from this window: this handoff.
