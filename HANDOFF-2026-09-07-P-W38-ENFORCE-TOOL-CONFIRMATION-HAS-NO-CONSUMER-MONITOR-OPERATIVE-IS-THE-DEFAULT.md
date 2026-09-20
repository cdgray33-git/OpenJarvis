# HANDOFF 2026-09-07 P / W38 - `enforce_tool_confirmation` HAS NO CONSUMER, SO DEFECT 6 WAS NECESSARY. AND `monitor_operative` IS NOT AN UNUSED AGENT - IT IS THE DEFAULT AGENT TYPE OF THE ENTIRE MANAGED-AGENT SUBSYSTEM. NO CODE WAS MODIFIED.

Predecessor: HANDOFF-2026-09-06-O-W37-TRUNCATE-IS-TWO-FUNCTIONS-T-A-T-B-SPLIT.md

All evidence in this window is dated 09/07 and was produced live in-window by
direct greps, direct file reads, and one Python import executed in the venv.
The 550B cloud model was NOT used this window. Section 8 records why, because
declining to use it was a deliberate decision and not an oversight.

---

## 0. READ THIS FIRST - WHERE THE SYSTEM ACTUALLY SITS

**Nothing in the tree was modified this window. The backend was not restarted.
No probe was built. No patch was applied. No commit was issued.**

`411cd59` remains HEAD on `origin/main` and `gitlab/main`. It was verified as
HEAD by W37 at the start of that window and nothing since has touched the tree,
so it is carried forward as HEAD on assertion, NOT re-verified this window.
**If the next window needs HEAD to be certain, re-run the check. Do not inherit
it from this line.**

Exactly ONE command executed code this window: a Python import of
`openjarvis.agents.monitor_operative`. Everything else was a grep or a read.

W37 next-action 1 is ANSWERED. W37 next-action 2 is READ. W37 next-action 3 is
STARTED and its premise survived a challenge - see section 2.9.

**THE MOST IMPORTANT LINE IN THIS HANDOFF IS IN SECTION 3. READ SECTION 3
BEFORE SECTION 2.** It is a method correction Gray issued mid-window and it
governs how every finding below should be read.

---

## 1. WHAT WAS DONE, IN ORDER

1. Grep for `enforce_tool_confirmation` across `src\openjarvis\*.py`. Two hits,
   both `config.py`.
2. Widened the same grep to the whole repo across `.py`, `.toml`, `.md`, with
   `.venv`, `node_modules`, `.git`, `site-packages`, `dist`, `build` excluded.
   Done because the first grep covered only `src\openjarvis` and Gray's tree has
   code outside it.
3. Census of every `SecurityConfig` field access in the tree, `config.py`
   excluded, to catch a dynamic consumer that a literal-string grep would miss.
4. Header-and-keyword scan of `docs\user-guide\security.md`.
5. Header map of `docs\architecture\agents.md`.
6. Read `agents.md:257-286` whole - the `NativeOpenHandsAgent` section.
7. Read `agents.md:492-519` whole - the `ToolExecutor` section.
8. **Gray issued the method correction here.** See section 3.
9. Directory listing of `src\openjarvis\agents\*.py` with sizes.
10. Python import of `monitor_operative` in the venv. First executed code.
11. `inspect.signature` of `MonitorOperativeAgent.__init__` plus its docstring.
12. Grep for `confirm_callback|memory_backend|session_store` inside
    `monitor_operative.py`.
13. Grep for `MonitorOperativeAgent|monitor_operative` across `src\openjarvis`.

---

## 2. THE FINDINGS

### 2.1 W37 ITEM 1 IS ANSWERED: `enforce_tool_confirmation` HAS NO CONSUMER

Repo-wide, the flag appears in exactly these places:

```
docs\getting-started\configuration.md:556   sample config line
docs\getting-started\configuration.md:567   reference table row
docs\user-guide\security.md:381             sample config line
docs\user-guide\security.md:395             reference table row
src\openjarvis\core\config.py:1198          dataclass default = True
src\openjarvis\core\config.py:2028          written into generated configs
tests\core\test_config.py:121               asserts the default is True
```

Plus our own artifacts (a CLOUDBUNDLE and the W37 handoff), which are noise.

`test_config.py:121` is the only code hit outside `config.py` and it asserts
`sc.enforce_tool_confirmation is True`. **That tests that the field exists and
defaults True. It does not test that anything acts on it.** A test of a
dataclass default is not a consumer.

### 2.2 THE FIELD CENSUS - WHAT ACTUALLY READS `SecurityConfig`

A literal grep cannot see `getattr(cfg.security, ...)` or a dict walk, so the
whole of `SecurityConfig` was censused instead. With module-path import noise
(`from openjarvis.security.x import y`) stripped, every real field access in
`src\openjarvis`, outside `config.py`, is:

```
security\__init__.py:50   config.security.enabled
security\__init__.py:56   config.security.secret_scanner
security\__init__.py:58   config.security.pii_scanner
security\__init__.py:62   config.security.mode
security\__init__.py:67   config.security.scan_input
security\__init__.py:68   config.security.scan_output
security\__init__.py:76   config.security.capabilities.enabled
security\__init__.py:81   config.security.capabilities.policy_path
security\__init__.py:90   config.security.audit_log_path
cli\dashboard.py:145      config.security.enabled       (status string only)
cli\doctor_cmd.py:232     config.security.profile       (status string only)
cli\doctor_cmd.py:236     config.security.profile       (status string only)
```

Nine fields consumed by `setup_security`, two read for display. **The flag is in
none of them.** The negative is verified by enumeration, not by absence of a
grep hit.

**CONCLUSION: documented in two guides, defined in the dataclass, written into
generated configs, asserted by a test - and read by nothing. Defect 6, 6c, 6d,
6e and `openjarvis-confirm-live-v1` were NECESSARY, not duplicative. We did not
rebuild a documented feature. We discovered that below the config layer the
feature was never implemented, and built it.**

### 2.3 `mode = "warn"` IS CONSUMED. A WEEKS-OLD PARKED QUESTION IS RETIRED.

`security\__init__.py:62`: `mode = RedactionMode(config.security.mode)`.

`mode = "warn"` in Gray's `[security]` block is the **scanner redaction mode**.
It has nothing to do with tool confirmation. It has been sitting unexplained in
the config for weeks and it is now explained. It is consumed, it is meaningful,
and it is not related to any gate work.

`profile = "personal"` appears outside `config.py` only in a `doctor` status
message. **That one is NOT closed** - `config.py` was excluded from the census
and may apply profiles at load time. Open, low priority.

### 2.4 `security.md` IS A SCANNER DOCUMENT. THE GATE HAS NO SECTION IN IT.

Header scan of all 8,348 bytes. The document's sections are: Overview,
GuardrailsEngine (with Modes, Basic Usage, Constructor Parameters, Event Bus
Integration, Custom Scanners, Streaming), SecretScanner, PIIScanner, File
Policy, Audit Logger, Configuration, Writing a Custom Scanner, See Also.

**There is no tool-confirmation section.** The flag appears twice in the entire
file - a sample config line at :381 and a table row at :395. No prose, no usage
example, no behavioral description.

The author never implemented tool confirmation at the config layer, and he never
wrote a section about it either. It is a config-table entry and nothing more.
**Consistent with 2.1 from a completely independent direction.**

### 2.5 THE AUTHOR DOCUMENTS THE DEFECT 1 SIGNATURE AS DESIGNED BEHAVIOR

`agents.md:257-286`, the `NativeOpenHandsAgent` section, read directly and whole
per W37's standing rule. Its step 3 lists four branches per turn:

```
- Generates a response and strips <think> tags
- If a ```python code block is found, executes it via code_interpreter
- If an Action: / Action Input: is found, dispatches the tool
- If neither is found, returns the content as the final answer
```

**The fourth branch is the Defect 1 signature, written down by the author as
normal operation.** There is no failure mode in the design for "the model
narrated an action without emitting a call." That path IS the success path. This
confirms 15.4D of W37 from the source document rather than via the 550B.

**Implication for how Defect 1 should be framed from here: windows that searched
for a fault in dispatch were searching for a bug in code that is doing exactly
what its author specified.** The defect is that the specified behavior is wrong
for our use case, not that the implementation deviates from it.

### 2.6 A SECOND DOCUMENTED-VERSUS-IMPLEMENTED DIVERGENCE, FOUND THE SAME DAY

`agents.md:257-286` step 4 claims the agent **"Handles context window overflow
with automatic truncation."**

W37 read `_truncate_if_needed` whole at `native_openhands.py:113-138` and
established that it sums SYSTEM into a total it cannot cut, can only ever modify
the most recent `Role.USER` message, and silently no-ops when the `:129` guard
fails.

**The documented capability and the implemented function are not the same
thing.** This is the second documented-versus-implemented divergence found in
this window, the first being the confirm flag. **It strengthens T-A rather than
weakening it** - the author believes overflow is handled, so no other guard was
written.

Also in the same section, confirmed directly rather than via the 550B:

- The example sets **`max_turns=3`**. Gray's `config.toml:17` sets 15. W37's
  15.4B is confirmed from the primary source.
- The example uses **`model="qwen3:8b"`**. Worth reconciling against whatever
  the chat path actually runs. Not investigated.

### 2.7 THE AUTHOR'S `ToolExecutor` HAS NO CONFIRMATION MECHANISM

`agents.md:492-519`, read whole. Documented constructor:

```
def __init__(self, tools: List[BaseTool], bus: Optional[EventBus] = None)
```

Two parameters. Documented dispatch, six steps: look up the tool by name, parse
the JSON arguments, publish `TOOL_CALL_START`, execute with timing, publish
`TOOL_CALL_END` with success and latency, return the `ToolResult`.

**No confirmation step. No `_confirm_callback` parameter to hold one.** Third
independent confirmation of 2.1: the class that would have to honor the flag has
no mechanism by which to honor it.

**Caveat that must travel with this finding:** this is the DOCUMENTED
constructor, and this project's documentation has now diverged from its code
twice in one window. Whether Gray's actual `ToolExecutor` signature matches is a
separate question, and we already know from the Defect 6 work that
`_confirm_callback` lives in `tools\_stubs.py`, which is upstream's file. Either
the author added it after this doc was written, or it arrived by another route.
**Not investigated. Do not assume.**

### 2.8 CORRECTION ISSUED IN-WINDOW: UPSTREAM DOES HAVE A CONFIRMATION CONCEPT

`inspect.signature(MonitorOperativeAgent.__init__)` returned, among others:

```
interactive: bool = False,
confirm_callback=None,
```

and `monitor_operative.py:138` passes `confirm_callback=confirm_callback`
straight through to the parent constructor. It is not stored on `self` in this
class.

**This corrects a reading I was one step away from stating as a finding.**
"Upstream has no confirmation mechanism at all" would have been WRONG. Upstream
has one - it lives on the operative agents as a constructor argument, not on the
executor and not behind the config flag.

**This does not un-answer 2.1.** `enforce_tool_confirmation` still has no
consumer, and the chat path still had no gate. But the divergence chapter must
state the correct version: **the author put confirmation on the operative agent
constructors and documented a config flag that reaches none of it.**

**ACTION FOR A FUTURE WINDOW: read what the parent does with `confirm_callback`.
It bears directly on Defect 6 and on the confirm-live work.** Where `:138` sends
it was not read.

### 2.9 `monitor_operative` IS THE DEFAULT AGENT TYPE OF THE MANAGED-AGENT SUBSYSTEM

This is the finding with the largest consequence for the program goal, and it
arrived from a grep that was run for an entirely different reason (to test
whether `configuration.md` or `agents.md` was the stale document).

`monitor_operative` is the DEFAULT `agent_type` at six independent sites:

```
agents\manager.py:24                 SQLite schema column DEFAULT 'monitor_operative'
agents\manager.py:165                create(agent_type: str = "monitor_operative")
agents\manager.py:522                config.pop("agent_type", "monitor_operative")
agents\executor.py:249               agent.get("agent_type", "monitor_operative")
cli\agent_cmd.py:98                  --type default
cli\agent_cmd.py:385                 interactive prompt default
server\agent_manager_routes.py:26    API model default
```

Registered at `monitor_operative.py:81` via `@AgentRegistry.register`, imported
at `agents\__init__.py:68`.

**`server\agent_manager_routes.py` is the file carrying the managed-agent SSE
stream - execution path 2 in the register.** So the recall machinery is not a
dormant entry in a dropdown. **It is what every managed agent already runs on
unless something overrode the type.**

W37's 15.3 framed `monitor_operative` as "registered, appears in the dropdown,
and has never been used." **That framing is now wrong and must be corrected in
the SDD.** Whether any managed agent has actually been RUN is a separate
question that this window did not touch.

### 2.10 THE RECALL MACHINERY IS HONORED, AND SILENTLY NO-OPS WITHOUT A BACKEND

Docstring of `MonitorOperativeAgent`, four strategy axes with defaults:

```
memory_extraction         = 'causality_graph'    (or scratchpad, structured_json, none)
observation_compression   = 'summarize'          (or truncate, none)
retrieval_strategy        = 'hybrid_with_self_eval'  (or keyword, semantic, none)
task_decomposition        = 'phased'             (or monolithic, hierarchical)
```

Stated purpose: persist findings across sessions, compress tool outputs before
adding to context, and recall prior context at the start of each run.

`session_store` and `memory_backend` are **honored, not accepted-and-ignored**:

```
:169/:170   stored on self
:613/:638/:654/:659   memory_backend.store(...)
:677        memory_backend.retrieve(state_key)
:693        session_store.get_or_create(session_id)
:717/:721   session_store.save_message(...)
:735-:741   auto-persist state
```

Keys are namespaced `monitor_operative:{operator_id}:state` (:340, :675, :735).

**But every single one is behind `if not self._memory_backend: return` or
`if not self._session_store or not self._operator_id: return`** - see :559,
:575, :627, :644, :673, :689, :713, :733.

**So the agent runs perfectly happily with `memory_backend=None` and performs no
recall at all, silently, with no error.** This is the THIRD instance of the
silent-no-op shape in this codebase, alongside `_truncate_if_needed`'s `:129`
guard and the confirm flag. **Add it to the SDP as a recurring architectural
pattern in this project: capability present, inert by default, fails quiet.**

### 2.11 `agents.md` IS STALE, AND THE TWO DOCS DISAGREE IN OPPOSITE DIRECTIONS

- `configuration.md:201` lists valid `default_agent`: simple, orchestrator,
  react, operative, monitor_operative. **`native_openhands` absent.**
- `agents.md:560` lists registry keys: simple, orchestrator, native_react,
  react, native_openhands, rlm, openhands. **`operative` and `monitor_operative`
  absent.**

The directory listing settles it. Both modules exist and are substantial:
`monitor_operative.py` at 29,568 bytes, `operative.py` at 11,643 bytes. The
import of `monitor_operative` succeeds. **`agents.md` is the stale document.**

W37's 15.4A read the `native_openhands` omission as "we built a year of work on
the least-documented agent in the project." **Soften that.** The correct reading
is that the author's docs are out of sync with each other in both directions.
`native_openhands` IS documented, in `agents.md:257-285` - just not in the
configuration reference.

---

## 3. THE METHOD CORRECTION GRAY ISSUED THIS WINDOW - READ THIS TWICE

At interaction 9, after I wrote that items 1 and 2 were "closed," Gray asked:

> "you say it closes items. are the items working and validated working per
> expectations?"

**The answer was no, and the wording was wrong.**

**NOTHING IN THIS WINDOW IS VALIDATED AS WORKING. NOTHING WAS EXECUTED EXCEPT ONE
IMPORT.** What was closed is a QUESTION, not a CAPABILITY. The distinction:

- "Item 1 is closed" means **we now know `enforce_tool_confirmation` has no
  consumer.** It says NOTHING about whether our replacement gate fires at
  runtime.
- **The Defect 6 gate has never been observed blocking a real tool call in the
  chat path.** That is still open and belongs to the confirm-live work.

I let "the flag has no consumer" drift into language that sounded like our gate
was proven. It is not. **The distinction between documented and implemented is
this window's central finding, and I made exactly that error inside the window
that found it.**

**STANDING RULE FOR EVERY FUTURE WINDOW, ADD TO THE METHOD CHAPTER:
SAY "ANSWERED" FOR A QUESTION. SAY "VALIDATED" ONLY FOR OBSERVED RUNTIME
BEHAVIOR. NEVER LET THE FIRST WORD DO THE SECOND WORD'S JOB.** A read closes a
question. Only an execution validates a capability.

This is the same family as W37's "read the artifact, not the report of the
artifact" and W35/W36/W37's silent-substitution lesson. Fourth instance of the
family.

---

## 4. NEGATIVE RESULTS AND DEAD ASSUMPTIONS - PINNED PER THE 08/24 RULE

**Things established as NOT true this window:**

1. **`enforce_tool_confirmation` is NOT wired to anything.** Established by
   enumeration of all twelve `SecurityConfig` field accesses, not merely by a
   grep returning nothing. Verified negative.
2. **The fifteen-plus windows of gate work were NOT duplicative.** The harder
   answer W37's 15.5 braced for did not materialize.
3. **`security.md` does NOT contain a tool-confirmation section.** It is a
   scanner and redaction document. The 8,348 bytes did not need reading in full.
4. **`agents.md` is NOT current.** It omits two agents that exist and import.
5. **`monitor_operative` is NOT an unused dropdown entry.** It is the subsystem
   default at six sites. W37's 15.3 framing is retired.
6. **"Upstream has no confirmation mechanism" is NOT true** - see 2.8. A reading
   I nearly recorded as a finding, corrected before it landed.
7. **`mode = "warn"` is NOT gate-related.** It is scanner redaction mode.
   Parked question retired.
8. **`test_config.py:121` is NOT a consumer.** It asserts a dataclass default.

**What a window that changed no code produced:** eight negatives, one method
correction, and a re-framing of the program-goal item from "unbuilt" to
"possibly unwired." That is the knowledge this window exists to pin.

---

## 5. SDP / SDD ADDITIONS FROM THIS WINDOW

**5.1 The divergence chapter gains its strongest entry.**
Author documents a tool-confirmation gate at `security.md:395` and
`configuration.md:567`. `core\config.py:1198` defines the field.
`core\config.py:2028` writes it into every generated config.
`tests\core\test_config.py:121` asserts its default. **No consumer exists
anywhere in the codebase.** Graystone built the real gate: Defect 6, 6c, 6d, 6e,
`openjarvis-confirm-live-v1`. State it as: author documents X, codebase
implements the field and not the behavior, Graystone implements the behavior.

**5.2 Second divergence entry, same window.** Author documents automatic context
overflow handling at `agents.md:257-286` step 4. `_truncate_if_needed` at
`native_openhands.py:113-138` cannot do what that sentence claims (W37 section
2.2). Documented capability, absent implementation.

**5.3 Third divergence entry, corrected form.** Upstream's confirmation
mechanism exists on the operative agent constructors
(`monitor_operative.py:126/:138`), not on `ToolExecutor` and not behind the
config flag. Two mechanisms that do not meet - same shape as W37's 15.4E.

**5.4 NEW ARCHITECTURAL PATTERN FOR THE SDP, THREE INSTANCES:
CAPABILITY PRESENT, INERT BY DEFAULT, FAILS QUIET.**
- `_truncate_if_needed` `:129` guard - no-ops silently, no log, no exception.
- `enforce_tool_confirmation` - defined, defaulted True, consumed by nothing.
- `monitor_operative` recall - eight `if not self._memory_backend` guards; full
  persistence machinery inert without a backend, no warning.
**This is a project-wide idiom and it is the single most important thing for the
SDP to warn a future reader about.** In this codebase, "the setting is on" and
"the behavior happens" are independent facts.

**5.5 The plain-language guard explanation (09/02 pin) gains its best framing.**
For the eight-year-old version: the manual for the house says there is a lock on
the door. There is a switch on the wall labelled LOCK, and it is switched on.
But no wire runs from that switch to any lock, and there is no lock on the door.
Nobody lied - the person who wrote the manual meant to fit one. We found the
door open, and we fitted the lock ourselves. **Now the technical version, and
both go in the SDP.**

**5.6 The Defect 1 framing changes.** `agents.md:257-286` step 3's fourth branch
documents "returns the content as the final answer" when no code block and no
`Action:` are found. **The Defect 1 signature is the author's specified success
path.** The SDD chapter on Defect 1 must open with this, because it reframes
every prior window: we were looking for a deviation from spec in behavior that
IS the spec.

**5.7 Method chapter, new top-level rule.** Section 3's ANSWERED-versus-
VALIDATED rule. Place it beside W37's "read the project's own documentation
before deriving anything from source" and "read the artifact, not the report of
the artifact."

**5.8 Requirements baseline.** The four strategy axes of
`MonitorOperativeAgent` (2.10) are upstream's own statement of what long-horizon
memory means in this system. That is the closest thing yet found to a written
specification of Gray's persistent-recall requirement. Capture the docstring
verbatim in the SDP.

---

## 6. EXECUTION PATHS - REGISTER UPDATE

No new path was traced this window. One existing path gains a material property.

**PATH 2, MANAGED-AGENT SSE STREAM (`_stream_managed_agent()` in
`server\agent_manager_routes.py`):**
- **NEW: its default agent type is `monitor_operative`**, set at
  `agent_manager_routes.py:26`, and reinforced by `manager.py:24/:165/:522` and
  `executor.py:249`. Any managed agent created without an explicit type runs
  `MonitorOperativeAgent`.
- **NEW: that agent's constructor accepts `confirm_callback` and `interactive`**
  (`monitor_operative.py:126`), forwarded to the parent at `:138`. **Whether
  path 2 supplies either is NOT KNOWN.** This is the most direct open question
  about the confirmation gate on this path.
- **NEW: that agent's constructor accepts `memory_backend` and `session_store`,
  both defaulting to None**, and performs no recall when they are None.
  **Whether path 2 supplies either is NOT KNOWN.**

**THE SINGLE READ THAT ANSWERS ALL THREE: `agents\manager.py` around :500-560**,
where `config.pop("agent_type", ...)` at `:522` precedes the construction call.
That construction site was NOT read this window. **It is next action 1.**

Paths 1a/1b/1c/1d (routes.py chat dispatch) and the orchestrator `ask()` path
are unchanged this window.

---

## 7. DIAGNOSTIC TOOLING REGISTER - 09/06 PIN

**Nothing was built this window. Nothing was run. The register is unchanged.**

Carried forward and still true:
- `telemetry.db` has been recording on every call since July. **SEARCH THE
  SCHEMA BEFORE BUILDING AN INSTRUMENT.**
- `serve.py:268/:280/:281` `[DEBUG]` `print()` calls still produce zero readable
  bytes - `print()` goes to a detached console, `backend.log` captures only the
  `logging` module. **Still unfixed. Carried as next action.**
- Untracked probe files remain in the repo root from W37:
  `probe_telemetry_truncation.py`, `probe_telemetry_ceiling.py`, plus five
  `CLOUDBUNDLE-adhoc-2026090*.md` files and the W37 handoff. **This handoff adds
  a sixth untracked file to the root.**

**Standing rule intact: verify where an instrument's output lands at the moment
it is added, never when it is needed.**

---

## 8. THE 550B CLOUD MODEL - CONSIDERED AND DECLINED, WITH REASONING

Gray offered to send `security.md` (8,348 bytes) to the 550B. **Declined, and
the reasoning is recorded because the decision could have gone the other way.**

The header-and-keyword scan (2.4) had already established that the flag appears
exactly twice in the file, both in config tables, with no prose section. A
whole-file read by the 550B would have returned the same two lines plus a
summary of scanner documentation we did not need. **The cheap instrument had
already answered the question; the expensive one would have re-answered it.**

**The rule that produced this, carried forward:** the 550B is for questions that
need whole files that we cannot afford to read in-window. It is NOT for
questions a targeted grep has already closed. W37's own caution applies - keep
bundles scoped to files bearing on ONE question, because accuracy degrades on
large one-shot uploads.

**Standing caution, unchanged, three instances (W37 3.3, 12.4, 15.5): the 550B
returns cited answers and concluded answers in the same reply, in the same
register. Trust the citations. Treat every conclusion as a hypothesis.**

**Where the 550B WOULD earn its cost next:** `docs\architecture\memory.md` plus
`docs\memory_db_schema.md` together, scoped to the single question "what does
upstream expect a `memory_backend` to be, and does anything in this tree provide
one?" That is a genuine whole-file, multi-file question.

---

## 9. THE PROGRAM GOAL - 09/06 PIN

**Goal: a functional executive assistant that performs the duties at a computer
that a human would. Approaching one year. Not yet 50 percent of the initial
requirements. There is still no progress denominator.**

**What this window moved toward the goal:**

The persistent-recall requirement - stated as set up but never finished - moved
from **"unbuilt"** to **"built upstream, possibly unwired."** That is a large
change in estimate. `MonitorOperativeAgent` has 29,568 bytes of memory
extraction, observation compression, retrieval, and session persistence, it is
the default agent type of the managed-agent subsystem, and it imports clean.
Every recall call site is guarded on a `memory_backend` that defaults to None.

**If nothing constructs it with a backend, the remaining work is WIRING, not
BUILDING.** That is a different order of effort and it is the highest-value
open question in the project right now.

**Stated honestly per section 3: this is a source reading. No managed agent was
run. No recall was observed. The estimate moved; nothing was validated.**

**Requirements denominator: still missing.** Gray's original initial
requirements document has not been located. Without it there is no progress
measure. Carried as a next action, unchanged from W37's 15.2. **The four
strategy axes (2.10) are a partial substitute for the recall requirement
specifically, and nothing else.**

---

## 10. NEXT ACTIONS

**1. READ `agents\manager.py:500-560`.** The construction site after
`config.pop("agent_type", ...)` at `:522`. Answers three open questions at once:
does the managed-agent path pass `memory_backend`, does it pass `session_store`,
does it pass `confirm_callback`. **Cheapest high-value read on the list, and it
is where this window stopped.**

**2. READ WHAT `monitor_operative.py:138` HANDS `confirm_callback` TO.** The
parent constructor. Bears directly on Defect 6 and confirm-live.

**3. READ `docs\architecture\memory.md` AND `docs\memory_db_schema.md`**, scoped
to "what is a `memory_backend` and does this tree provide one?" **This is the
550B's next earned job** - see section 8.

**4. LOCATE GRAY'S ORIGINAL INITIAL REQUIREMENTS.** No progress denominator
without it. Upstream cannot supply one.

**5. CLOSE T-B.** Still provable from source and arithmetic alone. Carried from
W37 14.8 and 15.6, now twice-deferred. **Do not let it fall off.**

**6. READ `estimate_prompt_tokens`.** Carried from W37 14.8 item 2.

**7. FIX THE THREE `print()` CALLS TO `logger.info()`** at
`serve.py:268/:280/:281`. Carried from W37 14.8 item 3. **This is the only item
on the list that modifies code, and it is the one that makes future
instrumentation readable.**

**8. BUILD THE DIVERGENCE CHAPTER** (W37 14.6) with the three entries at 5.1,
5.2, 5.3 plus the pattern at 5.4, and correct 15.4A per 2.11.

**9. RE-VERIFY HEAD** before any commit. This window inherited `411cd59` on
assertion.

**10. Carry W37 section 10 items 8-16 and 14.8 items 4, 6, 7 unchanged.**

**Ordering note: 1 and 2 are reads that cost almost nothing and unblock the
program-goal item. Do them first. Do not start 7 until 1 and 2 are done - one
thing finished before the next is started, per the 08/17 rule.**

---

## 11. WINDOW CLOSE

**14 interactions. No code modified. No commit issued. Backend not restarted.
One line of code executed, an import.**

Eight negatives established, one near-miss finding caught and corrected before
it was recorded (2.8), one method correction issued by Gray that outranks every
technical finding in this handoff (section 3), and one program-goal estimate
materially revised (section 9).

**The window's summary judgement: WE ANSWERED THREE QUESTIONS AND VALIDATED
NOTHING, AND THOSE ARE DIFFERENT THINGS.**

To W37's standing judgement - EVERYTHING ABOUT STRUCTURE IS VERIFIED, EVERYTHING
ABOUT MAGNITUDE IS ASSUMED, AND EVERYTHING WE BUILT, WE BUILT WITHOUT READING
WHAT THE AUTHOR ALREADY WROTE - add:

**AND WHAT THE AUTHOR WROTE IS NOT ALWAYS WHAT THE AUTHOR BUILT.**

New untracked file in the repo root from this window: this handoff.
