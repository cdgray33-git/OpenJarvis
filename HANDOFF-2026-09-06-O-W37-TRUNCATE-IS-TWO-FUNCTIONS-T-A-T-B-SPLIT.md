# HANDOFF 2026-09-06 O / W37 - W36's HINGE QUESTION IS ANSWERED AND THE ANSWER IS "BOTH". `_truncate_if_needed` IS TWO DIFFERENT FUNCTIONS DEPENDING ON DISPATCH PATH, AND NEITHER IS WHAT ITS OWN COMMENT CLAIMS. NO CODE WAS MODIFIED.

Predecessor: HANDOFF-2026-09-05-N-W36-CTX-THEORY-DEAD-V3-VOID-BY-DESIGN.md
All evidence in this window is dated 09/06 and was produced live in-window by
direct source reads. Where the 550B cloud model was used, that is labelled
explicitly and its unsourced claims are quarantined in section 3.

---

## 0. READ THIS FIRST - WHERE THE SYSTEM ACTUALLY SITS

**Nothing in the tree was modified this window. The backend was not restarted.
No probe was built or run.** This was a pure read-and-localize window.

W36's next-action 1 is CLOSED and VERIFIED. Commit `411cd59` is HEAD on
`origin/main` and `gitlab/main`. Both `tests/probe_ctx_ceiling_v3.py` and
`tests/ctx_ceiling_v3_run_20260905-123036.txt` are tracked.

W36's next-action 2 is CLOSED. The hinge question - "are tool schemas an API
parameter or prompt text?" - is answered: **BOTH.** See section 2.1.

**W36's next-action 3 is now OBSOLETE AS WRITTEN.** It offered two branches,
each predicated on the hinge resolving one way or the other. It resolved both
ways at once, and the mechanism actually found is neither of the two branches
anticipated. Do not execute next-action 3. Read section 2.3 instead.

The truncation theory of Defect 1 is **not dead and not alive.** It has SPLIT
into two independent theories on two different dispatch paths, T-A and T-B.
T-B is provable from source and arithmetic alone. T-A needs an instrument.

---

## 1. WHAT WAS DONE, IN ORDER

### 1.1 Section 8 verification - the commit landed

W36 section 8 recorded a commit issued at window end whose output was never
seen. Verified first thing, before anything was built on it:

```
411cd59 (HEAD -> main, origin/main, origin/HEAD, gitlab/main, gitlab/HEAD)
        tests: add probe_ctx_ceiling_v3 paired ctx experiment and its run log
c37d8b1 num_ctx: thread 16384 through the ollama engine
fce0b78 tests: exercise the protected-sender guard, move path

tests/ctx_ceiling_v3_run_20260905-123036.txt
tests/probe_ctx_ceiling_v3.py
```

Both remotes at the same SHA. Both v3 files tracked. The `-f` staging worked and
`.gitignore:23` did not swallow the run log. **No re-issue needed.**

### 1.2 The handoff arrived in the chat body as the wrong content

The W36 handoff was uploaded correctly, but the text pasted into the chat body
was a `Select-String -Pattern '120'` dump across the handoff corpus, not the
handoff. Caught by reading the file from disk rather than trusting the pasted
block. Cost: nothing. Worth recording because it is the same SILENT-substitution
failure shape as W35's BOM and W36's `.gitignore` exclusion - the wrong thing
arrived and nothing raised an error.

**Standing lesson, third instance of this shape: read the artifact, not the
report of the artifact.**

### 1.3 The hinge read - `native_openhands.py:324-374` plus a targeted grep

Read the prompt build directly, with a grep for the tool handoff in the same
command so a schema pass outside the 50-line range could not hide.

### 1.4 `_truncate_if_needed` read in full, then its call sites

Found via a grep for the definition across `agents\*.py`. Read :113-138 whole.
Then located every call site and every reference to `max_prompt_tokens`.

### 1.5 The message-role census

Established what role each appended message carries, because the truncation
function keys on role. This is the read that produced the window's main finding.

### 1.6 The cloud bundle - built twice

Assembled a whole-file bundle for the 550B per the standing rule. **The first
bundle was built against two guessed paths and came back 4 of 6.** Rebuilt with
resolved paths, 5 of 5. Details and the correction in section 3.

---

## 2. THE FINDINGS

### 2.1 THE HINGE IS ANSWERED: BOTH. Tool definitions travel TWICE.

`native_openhands.py:324-330`:

```
324: tool_descriptions = build_tool_descriptions(self._tools)
325: prompt_template = (
326:     load_system_prompt_override("native_openhands") or OPENHANDS_SYSTEM_PROMPT
327: )
328: system_prompt = prompt_template.format(
329:     tool_descriptions=tool_descriptions,
330: )
```

`native_openhands.py:390` and `:403`:

```
390: openai_tools = self._executor.get_openai_tools() if self._tools else []
403: gen_kwargs["tools"] = openai_tools
```

**The tool SCHEMAS go out as a top-level `tools` API parameter, outside the
messages array, and cannot be touched by message truncation at any window size.
The tool DESCRIPTIONS - the prose that tells the model how to behave with those
tools - are formatted as TEXT into the SYSTEM message, and that text sits inside
the truncatable region.**

This is the architecturally important distinction and it is new. The exposure is
not "the model loses its tools." It is **"the model keeps its tools and loses
its instructions."** A model in that state has a valid `tools` parameter it was
never told to use, which is an extremely good fit for the Defect 1 signature:
narrates the action, emits no call.

W36 section 2.2 framed this as an either/or. It is not. Record the correction.

### 2.2 THE MAIN FINDING: `_truncate_if_needed` IS TWO DIFFERENT FUNCTIONS

The function, whole, at `native_openhands.py:113-138`:

```
113: def _truncate_if_needed(
114:     self,
115:     messages: list[Message],
116:     max_prompt_tokens: int = 3000,
117: ) -> list[Message]:
118:     """Truncate messages if estimated token count exceeds limit."""
119:     total_chars = sum(len(m.content) for m in messages)
120:     estimated_tokens = total_chars // 4
121:     if estimated_tokens <= max_prompt_tokens:
122:         return messages
123:     # Find the last user message and truncate its content
124:     for i in range(len(messages) - 1, -1, -1):
125:         if messages[i].role == Role.USER:
126:             excess_tokens = estimated_tokens - max_prompt_tokens
127:             excess_chars = excess_tokens * 4
128:             original = messages[i].content
129:             if len(original) > excess_chars + 200:
130:                 truncated = original[: len(original) - excess_chars]
131:                 messages[i] = Message(
132:                     role=Role.USER,
133:                     content=(
134:                         truncated + "\n\n[Input truncated to fit context window]"
135:                     ),
136:                 )
137:             break
138:     return messages
```

Three properties, all load-bearing:

1. **It sums ALL messages including SYSTEM** (:119), but can only ever modify a
   `Role.USER` message (:125).
2. **It scans BACKWARD and breaks on the first `Role.USER` hit** (:124, :137).
   So its behavior is entirely determined by *what the most recent `Role.USER`
   message happens to be*.
3. **It cuts from the TAIL** (:130), and if the guard at :129 fails it does
   nothing at all, silently, with no log line and no exception.

Call sites, all using the default 3000:

```
349: direct_messages = self._truncate_if_needed(direct_messages)   # url_expanded branch
382: messages = self._truncate_if_needed(messages)                 # once, before the loop
399: messages = self._truncate_if_needed(messages)                 # EVERY TURN, inside the loop
```

`:399` sits immediately before `gen_kwargs["tools"]` at :403 and `_generate` at
:406. It runs on every turn of every production agent turn.

**Now the message-role census, which is what makes this two functions:**

| Line | Path | Appended as |
|---|---|---|
| 442 | native, assistant turn | `Role.ASSISTANT` |
| 455 | native, tool observation | **`Role.TOOL`** |
| 468 | CodeAct, assistant turn | `Role.ASSISTANT` |
| 483 | CodeAct, tool observation | **`Role.USER`** |
| 490 | Action-Input, assistant turn | `Role.ASSISTANT` |
| 502 | Action-Input, tool observation | **`Role.USER`** |
| 379 | few-shot exemplar input | `Role.USER`, via `insert(-1, ...)` |
| 380 | few-shot exemplar output | `Role.ASSISTANT`, via `insert(-1, ...)` |

Observations are `Role.TOOL` on the native path and `Role.USER` on both fallback
paths. That single inconsistency splits the function's behavior in half.

#### THEORY T-A - the NATIVE path. Silent no-op, every turn.

On the native function-calling path, nothing appended inside the loop is
`Role.USER`. The backward scan walks past every `Role.TOOL` observation and
every `Role.ASSISTANT` turn and lands on **Gray's original ask**, which is
typically short.

Worked arithmetic for a representative turn 3 (SYSTEM ~3,980 tokens, user ask
~200 chars, two 4,000-char tool observations, exemplars present):

- `total_chars` ~27,000, `estimated_tokens` ~6,750
- :121 `6750 <= 3000` is FALSE, so it proceeds
- scan lands on the ~200-char user ask
- `excess_chars` = (6750 - 3000) * 4 = ~15,000
- :129 `200 > 15,200` is FALSE
- :137 `break`, :138 return **unmodified**

**The function does nothing, on every turn, and says nothing about it.** The
per-turn context guard on the production native path is effectively absent.

**T-A therefore predicts:** context grows unbounded across turns until something
downstream truncates instead. What that downstream thing does, and whether the
SYSTEM message carrying `tool_descriptions` survives it, is **NOT ESTABLISHED**
- see section 3, quarantine item 1.

#### THEORY T-B - the FALLBACK paths. Double truncation, marker destroyed.

On the CodeAct (:483) and Action-Input (:502) paths, observations ARE
`Role.USER`, and they are the LAST message appended. The backward scan hits the
most recent observation immediately.

Those observations are already capped inline before being appended:

```
479: obs_text = tool_result.content
480: if len(obs_text) > 4000:
481:     obs_text = obs_text[:4000] + "\n\n[Output truncated]"
482: observation = f"Output:\n{obs_text}"
483: messages.append(Message(role=Role.USER, content=observation))
```

The same 4000-char inline cap appears at :451-452 (native) and :498-500
(Action-Input). Three hardcoded copies of the same constant.

So a capped observation is roughly 4,030 chars. The :129 guard passes whenever
`excess_chars` is under about 3,800 chars - that is, whenever the conversation
is over the 3000-token budget by less than ~950 tokens. **In that band the
function fires and cuts the tail off the tool observation the model is about to
reason over.**

**And because the `[Output truncated]` marker was appended at the END of
obs_text at :481, a tail cut at :130 REMOVES THE MARKER.** The replacement
marker at :134 says `[Input truncated to fit context window]` - which describes
the user's input, not a tool result.

**T-B therefore predicts:** on fallback-path turns in that band, the model
receives a tool observation that ends mid-sentence, with the honest marker
deleted and a misleading one attached, and no log anywhere. A model reasoning
over a mangled observation that it has not been told is mangled is a very good
fit for narrating an outcome instead of dispatching the next call.

**T-B is provable from source and arithmetic. It does not need a probe to be
believed. It needs a probe only to be MEASURED - specifically, how often real
runs land in the band.**

### 2.3 WHY THE COMMENT AT :397-398 IS THE TELL

```
397: # Truncate before every generate call -- tool results may have
398: # expanded the context beyond what the model supports.
399: messages = self._truncate_if_needed(messages)
```

The stated intent is to contain growth from tool results. On the native path the
function is **structurally incapable** of touching a `Role.TOOL` message - the
scan at :125 matches `Role.USER` and nothing else. On the fallback paths it can
touch them, but only by amputating them, which is not containment either.

**The function's stated purpose and its implemented behavior have never matched
on any path.** That is the shape of a defect that survives review: the comment
reassures every reader who does not check the role census.

### 2.4 The few-shot exemplars are a DORMANT context tax - CORRECTED, SEE SECTION 12

**THIS SECTION WAS WRITTEN WRONG AND IS CORRECTED IN SECTION 12. Read section 12
before using anything here.** The original text is preserved below because the
correction is the useful part.

> ORIGINAL, WRONG AS TO EFFECT: `:376-380` inserts exemplar pairs via
> `messages.insert(-1, ...)`. They land BEFORE the final message, they are
> counted in `total_chars` at :119 every single turn, and on the native path they
> sit further back than the user ask so the backward scan never reaches them.
> **They inflate the overflow they can never absorb.** Volume is unmeasured -
> `load_few_shot_exemplars("native_openhands")` was not read this window.

**MEASURED CORRECTION:** the exemplar source file does not exist on this
machine. The loader returns `[]`, the insert loop at :377-380 never executes,
and exemplar contribution is **ZERO chars, ZERO tokens**. The MECHANISM
described above is real - uncapped, doubled per exemplar, counted every turn -
but it is **DORMANT, not active.** It inflates nothing today. Full evidence and
consequences in section 12.

---

## 3. NEGATIVE RESULTS, CORRECTIONS, AND QUARANTINE

Per the 08/24 pinned rule: what a thing turned out NOT to be is knowledge, and a
window that changed nothing still produced knowledge.

### 3.1 REFUTED: the agent layer cannot evict the SYSTEM message

`_truncate_if_needed` only ever rewrites a `Role.USER` message (:125, :131-132).
It cannot delete a message, cannot reorder, and cannot touch `Role.SYSTEM`. The
`tool_descriptions` text at :324-330 is **not evictable by the agent's own
truncation code**, at any budget, ever.

**Do not re-raise agent-side SYSTEM eviction.** If SYSTEM is lost, it is lost
below this layer.

### 3.2 REFUTED: W36's framing of the hinge as either/or

W36 section 2.2 posed "API parameter, or prompt text?" and section 10 built two
mutually exclusive next-action branches on it. Both are true simultaneously
(section 2.1). The question was well-aimed; the answer space was too small.

### 3.3 QUARANTINE - the 550B's Q4 answer is INFERENCE, NOT EVIDENCE

The 550B was asked where truncation actually happens once `_truncate_if_needed`
no-ops, and whether SYSTEM survives. It answered that Ollama truncates
oldest-first and that SYSTEM is "most likely to be dropped" - while explicitly
stating in the same answer that Ollama server behavior is "external, not in this
codebase."

**That is inference delivered in the same register as its cited answers. Treat
it as a hypothesis with zero measurements behind it.** It is the T-A mechanism
we most want to be true, which is exactly why it needs an instrument. W36's G4
gate exists because of this failure mode.

It also leans on the ~3,980-token overhead figure, which W36 next-action 6
already flags as untrustworthy while `ollama.py:126` masks the reported token
count behind `prompt_tokens = max(reported, estimated)`.

**Unmasking :126 is now a prerequisite for testing T-A, not a cleanup item.**

### 3.4 Q3 IS UNANSWERED - the 550B answered from the SUPERSEDED bundle

The reply's Q3 asserts `core/compression.py` does not exist and cites the
bundle's own NOT-FOUND report. That is the **first** bundle
(`CLOUDBUNDLE-adhoc-20260906-104107.md`, 4 of 6). The corrected bundle
(`CLOUDBUNDLE-adhoc-20260906-104229.md`, 5 of 5) contains the real file at
`src/openjarvis/sessions/compression.py` and asks about it by that path.

**The compressor question is still open and the corrected bundle has not been
sent.** Q1, Q2 and Q5 were answered against four correct whole files and their
cited claims are consistent with this window's own direct reads.

### 3.5 MY ERROR: two bundle paths were guessed, not resolved

I built the first bundle using `src/openjarvis/core/compression.py` and
`src/openjarvis/agents/types.py`, both inferred from leaf filenames in a grep
rather than resolved. Real locations:

- `compression.py` is at `src/openjarvis/sessions/compression.py` - **sessions,
  not core.** A session-scoped compressor is architecturally unlikely to be
  wired into an agent turn loop, which strengthens rather than answers Q3.
- `src/openjarvis/agents/types.py` **does not exist.** The `Role` enum
  (`class Role(str, Enum)` at :15, `TOOL = "tool"` at :21) is in
  `src/openjarvis/core/types.py`, which was already in the bundle. The file was
  never missing; I asked for it twice under two paths, one of them wrong.

Caught only because `bundle_for_cloud.py` REPORTS missing files instead of
silently skipping them. **That design choice is the reason this window did not
ship a bundle with a hole in it.** Fourth instance of the silent-versus-loud
failure theme in four windows.

### 3.6 A PowerShell error worth pinning

`Select-String` has no `-Recurse` parameter. Recursive source greps must be:

```
Get-ChildItem .\src\openjarvis\ -Filter *.py -Recurse | Select-String -Pattern '...'
```

Note `-Filter` takes a single pattern; use `-Include` with multiple patterns,
and `-Include` requires `-Recurse` or a trailing `\*` on the path.

---

## 4. EXECUTION PATHS REGISTER

Standing structure per the 08/20 pin. This window adds the first FULL
characterization of the native_openhands turn loop as an execution path, and
splits it by dispatch branch because the branches behave differently.

### PATH 2 - `NativeOpenHandsAgent` turn loop (THREE DISPATCH BRANCHES)

- **Entry point:** agent `run()` / `ask()`, reached from the orchestrator path
  and from the managed-agent SSE stream. Both feed the same loop.
- **Call chain:** prompt build `native_openhands.py:324-330` -> `_build_messages`
  :374 -> few-shot insert :376-380 -> `_truncate_if_needed` :382 -> loop
  `for _turn in range(self._max_turns)` :394 -> `_truncate_if_needed` :399 ->
  `gen_kwargs["tools"]` :403 -> `_generate` :406 -> branch on
  `result.get("tool_calls", [])` :425.
- **Tool contract transport:** DUAL. Schemas via the `tools` API parameter
  (:390, :403). Descriptions as TEXT inside SYSTEM (:324-330).
- **Executor:** `self._executor`, `.execute(tc)` at :448 (native), :476
  (CodeAct), :495 (Action-Input). Construction not read this window - carried
  from W10's finding that executor construction is where the gate is decided.
- **Confirmation gate:** NOT characterized on this path this window. W10
  established the gate is a property of executor construction, so this path's
  gate status follows from whichever executor instance is injected. **OPEN.**
- **Event bus traffic:** `_oj_run_end` :361/:508, `_emit_turn_end`
  :357/:362/:410/:509, `_oj_raw_gen` :426 (Patch 4 RAWGEN), `_oj_set_turn` :396,
  RUNSTART at :598.
- **Human present:** depends on caller, not on this path.

#### BRANCH 2a - native function calling (`raw_tool_calls` non-empty, :427)

- Assistant turn appended `Role.ASSISTANT` with `tool_calls` :440-446
- Observation appended **`Role.TOOL`** :453-460, inline-capped 4000 :451-452
- `continue` :461
- **Truncation behavior: T-A, silent no-op every turn.**

#### BRANCH 2b - CodeAct (`_extract_code` hit, :466)

- Assistant turn appended `Role.ASSISTANT` :468
- Synthetic `code_interpreter` ToolCall :471-475
- Observation appended **`Role.USER`**, prefixed `Output:\n` :479-483
- `continue` :484
- **Truncation behavior: T-B, observation tail-cut in band.**

#### BRANCH 2c - Action-Input text fallback (`_extract_tool_call` hit, :488)

- Assistant turn appended `Role.ASSISTANT` :490
- Observation appended **`Role.USER`**, prefixed `Result: ` :498-502
- `continue` :503
- **Truncation behavior: T-B, observation tail-cut in band.**
- **Carried hazard:** Format 1 of `_extract_tool_call` is case-insensitive and
  unanchored, so prose containing "action:" can produce a false-positive tool
  name. This branch is therefore reachable by accident.

#### BRANCH 2d - final answer (no code, no tool call, :505)

- `_strip_think_tags` :506, `_strip_tool_call_text` :507, `_oj_run_end` "final"
  :508, returns `AgentResult` :510.
- **This is the branch Defect 1 exits through when it narrates instead of
  dispatching.**

#### PATH 2-URL - url_expanded early exit (:336-372)

- Skips the tool loop entirely. Hand-written 5-line SYSTEM, no tools, single
  `_generate` at :351, `_truncate_if_needed` at :349, `_oj_run_end` "urldirect".
- Worth registering because a run that takes this path has NO tool contract at
  all and will never emit a tool call. **Check this branch before attributing a
  no-tool-call run to Defect 1.**

---

## 5. SDP CONTENT FROM THIS WINDOW

Gray called this out explicitly: there is a lot of new architecture content
here. This section is written to be lifted into the SDP with minimal editing.

### 5.1 ARCHITECTURE - the dual tool-contract transport

The SDP needs a diagram and a paragraph on the fact that tool information leaves
the agent by **two independent transports with different survival properties**:

| Transport | Carries | Location | Truncatable? |
|---|---|---|---|
| `tools` API parameter | 12 JSON schemas | outside `messages` | NO - never |
| SYSTEM message text | `build_tool_descriptions` prose | inside `messages[0]` | YES - below the agent layer |

Per the 08/22 pin, the artifact must record ports, protocols and encoding at each
gate. For this gate: HTTP POST to the Ollama host, `/api/chat`, JSON body, the
`tools` key top-level and the descriptions embedded in `messages[0].content`.
Deliver as a downloadable standalone file for the wiki, not inline only.

**The decision this documents:** these two transports can disagree. A model can
hold a complete, valid schema set while holding no instructions about it. Any
future context-budget work must treat them as separate assets.

### 5.2 ARCHITECTURE - the truncation chain, all four stages

The SDP should document context reduction as a CHAIN with four independent
stages, because no single stage owns it:

1. **Inline observation cap, 4000 chars.** Three hardcoded copies,
   :451-452, :480-481, :499-500. Appends a `[Output truncated]` marker.
2. **`_truncate_if_needed`, 3000 tokens.** :113-138, called at :349, :382, :399.
   Behavior varies by dispatch branch. Can destroy stage 1's marker.
3. **`sessions/compression.py`, `TOOL_OUTPUT_MAX`.** Exists, handles `Role.TOOL`.
   **Reachability from this agent is UNPROVEN.** Owner and scope unknown.
4. **Engine / Ollama server, `num_ctx` 16384.** Behavior UNMEASURED. Whether it
   drops whole messages front-first, and whether SYSTEM is among them, is the
   open question that decides T-A.

**The architectural defect is that stage 2 does not know about stages 1, 3 or 4,
and its budget constant (3000) is unrelated to stage 4's (`num_ctx` 16384).**
Stage 2's budget is smaller than the SYSTEM prompt alone.

### 5.3 THE GUARD, IN PLAIN LANGUAGE (per the 09/02 pin)

Written so an eight-year-old could follow it. This belongs alongside the
technical detail, not instead of it.

> Imagine you are packing a lunchbox, and the rule is that everything has to fit.
>
> The lunchbox is the model's context window. The sandwich is the SYSTEM
> instructions - that is the big one, and it goes in first. Then there are
> snacks: the question you asked, and every answer the tools handed back.
>
> `_truncate_if_needed` is supposed to be the helper who checks the lunchbox
> before you close it. Here is what the helper actually does.
>
> First, the helper weighs EVERYTHING in the box, sandwich included. Then the
> helper compares that weight against a limit written on a sticky note. The
> sticky note says 3000. **The sandwich by itself weighs about 3,980.** So the
> box is always over the limit, even when it is empty of snacks.
>
> Now the helper goes to take something out. But the helper is only allowed to
> touch ONE kind of item: the thing you asked for. Not the sandwich. Not the
> tool answers. The helper starts at the top of the box and digs down until it
> finds your question, ignoring everything else on the way.
>
> **On the native path**, your question is a tiny snack, and the box is 15,000
> over. The helper looks at your tiny snack, decides that taking it out would not
> help enough, puts it back, and closes the lid without saying a word. Nobody is
> told the box is overweight. The box goes out the door too full.
>
> **On the fallback paths**, the tool answers get labelled as if they were your
> question. So the helper digs down, finds a big tool answer sitting right on
> top, and tears the end off it to make weight. The tool answer had a little tag
> on the end saying "there was more, it got cut" - and tearing the end off
> **removes that tag too.** Then the helper writes a new tag that says "your
> question was cut," which is not what happened at all.
>
> So the model gets a tool answer that stops in the middle of a sentence, with a
> tag on it describing the wrong thing, and no warning anywhere.

### 5.4 EVIDENCE STANDARD - what this window's method rules out

Continuing the standing practice of naming what a result RULES OUT:

- The role census RULES OUT agent-side SYSTEM eviction. It is a structural
  argument from source, not a measurement, and it is complete: there is no
  branch in :113-138 that removes or reorders a message.
- The dual-transport read RULES OUT "the model lost its tool schemas" as an
  explanation of Defect 1 on any path where `openai_tools` is non-empty.
- The 550B's Q4 RULES OUT NOTHING. It is inference. Recorded as a hypothesis.

**New method note for the SDP:** this window's most useful instrument was
`bundle_for_cloud.py` reporting missing files loudly. Two wrong paths were
caught for free. Build every tool to report what it did not find.

### 5.5 Defect 6 confirmation gate - GREAT DETAIL still owed

Per the 08/20 pin this remains the section needing the most depth: registry,
payload, transport, threading model. Unchanged this window, but PATH 2's gate
status is now an explicit OPEN item (section 4) and feeds it.

---

## 6. STANDING FACTS AND RULES

- Working directory is `PS C:\Users\Admin\OpenJarvis>` on the Windows box.
- Anything for the Ubuntu ollama host is `172.16.33.200` and must be labelled.
- Push to BOTH remotes - `origin` (GitHub) and `gitlab` (lab instance).
- `.\start-openjarvis.ps1` needs the `.\` prefix - a stale copy sits in
  `C:\Windows\System32`, which is on PATH.
- Backend log: `C:\Users\Admin\AppData\Local\OpenJarvis\logs\backend.log`
- Every download lands in `C:\Users\Admin\Downloads\`. Verify by MARKER CONTENT
  before running, never by filename.
- `Select-String` has NO `-Recurse`. Use `Get-ChildItem -Recurse | Select-String`.
- Every command must be valid on PowerShell 5.1. `Format-Hex -Count` is 6+.
- Probes must mirror PRODUCTION sampling (`temperature 0.7`, unseeded) unless the
  experiment is specifically about sampling.
- Any fallback-to-default path must log that it fell back.
- Read the matrix, not the verdict.
- Verify against the mailbox, never against the transcript.
- Connector-level `find_messages` returns a PLAIN LIST. Assert `isinstance(r, list)`.
- Size key on connector rows is `bytes`.
- Re-census before sizing any destructive test.
- Trash counts against the Yahoo quota until emptied.
- `ollama.py` lines 46 and 122-123 contain mojibake. Any patch to that file must
  read and write bytes or with explicit encoding, or it corrupts further.
- Design tests to be NON-INTERACTIVE. No test whose success depends on reaction
  speed.
- A spec inherited across windows can be invalidated by the fix the intervening
  window shipped. Re-read carried specs against current state before building.

---

## 7. ROLLBACK POINTS

**No code was modified this window. No new rollback point was created.**

- `ollama.py` - chain unchanged, still three deep. See W34 section 7.1.
  Committed at `c37d8b1`, so `git` is a rollback path.
- `config.toml` - unchanged from W35:
  ```
  C:\Users\Admin\.openjarvis\config.toml.bak_bomstrip_20260905   (722 B, WITH BOM - DO NOT RESTORE, it breaks startup)
  C:\Users\Admin\.openjarvis\config.toml.bak_numctx_20260905     (702 B, pre-num_ctx - the REAL rollback)
  ```
- Cheap num_ctx rollback remains the CONFIG KEY, not the patch: set
  `[engine] num_ctx` to 8192 or delete the line, then restart.
- `[[openjarvis-rollback-points]]` is at its size cap and needs condensing.

---

## 8. UNCOMMITTED WORK

`411cd59` is HEAD on both remotes - VERIFIED this window.

Untracked in the repo root, both written this window by `bundle_for_cloud.py`:

- `CLOUDBUNDLE-adhoc-20260906-104107.md` - **SUPERSEDED, 4 of 6 files.** Safe to
  delete. Do not send it; its Q3 answer is void.
- `CLOUDBUNDLE-adhoc-20260906-104229.md` - **CURRENT, 5 of 5, 85,672 bytes,
  ~21.4k tokens. NOT YET SENT.**

Neither is caught by `.gitignore:23` (`*.txt`), so both will keep appearing in
`git status --short` until cleared. The repo root carries a large untracked
working set - roughly 200 entries of probes, patches and handoffs. Not a defect,
but it makes `git status` unreadable and is worth a decision eventually.

---

## 9. THE 550B CLOUD MODEL - CARRIED FORWARD

Standing rule: when a question needs whole files rather than targeted reads,
bundle the suspected files into one markdown file for the 550B cloud model
(openrouter nemotron-3-ultra-550b) instead of spending window cycles on
piecemeal reads. 08/18 caveat holds - the free tier truncated one run and echoed
another; split into feeds of 2-3 questions.

**Interface, confirmed this window.** From `PS C:\Users\Admin\OpenJarvis>`:

```
python bundle_for_cloud.py --files <repo-relative/forward/slash/paths> --brief "..."
```

Output lands in the REPO ROOT as `CLOUDBUNDLE-<set>-<timestamp>.md`. It prints
the full path, byte size, approximate token count, and a found/total count.
**Resolve every path with `Get-ChildItem -Recurse` before passing it. Do not
infer a path from a grep's leaf filename.**

### FEED 0 - SEND FIRST. Already built, not yet sent.

`CLOUDBUNDLE-adhoc-20260906-104229.md` in the repo root. Five questions on the
truncation chain. **Q1, Q2 and Q5 have already been answered against equivalent
content and this window's direct reads agree with them - so if the reply comes
back short or echoed, the questions that actually still need answers are Q3 and
Q4.** Consider splitting to just those two.

### FEED 0-B - NEW, the highest-value unanswered question

What does the Ollama server do when the assembled prompt exceeds `num_ctx`
16384? Does it drop whole messages front-first, and does `messages[0]` (SYSTEM,
carrying `tool_descriptions`) go with them? **This decides T-A.** Note that this
is likely NOT answerable from the OpenJarvis source at all - it may need the
Ollama source or a live instrument. Ask the 550B which, before building.

### FEED 2 - STILL UNSENT AND STILL CHEAP

When `raw_tool_calls` is empty, is `_extract_tool_call` actually reached on the
live path, and would Format 4 dispatch a `<function=...>` block found in
content? If Format 4 absorbs it, a whole branch closes for free. **Raised in
priority by this window:** :488 is the gateway to BRANCH 2c, which is a T-B
path, so this question now also decides how often T-B is reachable.

### FEED 1

Should the num_ctx resolver move out of `ollama.py` into `_make_engine` /
`_HOST_MAP` in `_discovery.py`, and what is the cleanest shape that also threads
temperature the same way without changing behavior for existing callers?

### FEED 3

`config.toml` has at least two independent readers with different encoding
tolerance and opposite failure behavior (`core\config.py:1740` aborts,
`_oj_num_ctx_from_config` silently defaults). What is the minimal change that
gives one owner of config parsing, tolerant of BOM and encoding variation,
without a large refactor and without changing startup's fail-loud behavior?

Standing bundle set for context questions:

- `src\openjarvis\engine\ollama.py` (whole - carries the resolver)
- `src\openjarvis\agents\_stubs.py` (`_build_messages` :124-162, `_generate` :164-199)
- `src\openjarvis\agents\native_openhands.py` (whole - now the primary suspect)
- `src\openjarvis\sessions\compression.py` (NOTE: sessions, not core)
- `src\openjarvis\core\types.py` (the `Role` enum, :15 and :21)
- `src\openjarvis\research_loop.py` (the 16384 workaround)
- `C:\Users\Admin\.openjarvis\config.toml`
- `src\openjarvis\engine\_discovery.py`
- `src\openjarvis\core\config.py`

---

## 10. ORDERED NEXT ACTIONS

**W36's next-action 3 is obsolete. Start here.**

1. **Send FEED 0** (`CLOUDBUNDLE-adhoc-20260906-104229.md`, already in the repo
   root). Q3 and Q4 are what is actually owed. Costs one paste.

2. **Unmask `ollama.py:126`** - `prompt_tokens = max(reported, estimated)`
   discards the field that shows truncation. **This is now a PREREQUISITE for
   testing T-A, not cleanup.** Without the reported count there is no way to see
   whether the server truncated. Its own isolated patch, verified alone, per the
   08/17 rule.

3. **Then decide between T-A and T-B by cost, not by preference:**
   - **T-B is cheaper and already half-proven.** It needs an arithmetic
     demonstration plus a log line, not a 40-generation probe. Build a test that
     drives a CodeAct or Action-Input turn with a large observation and asserts
     whether :129 fires and whether `[Output truncated]` survives.
   - **T-A needs :126 unmasked first**, then an instrument that compares
     reported prompt tokens against assembled message tokens across a growing
     multi-turn native run, and checks whether the SYSTEM text is still present
     in the model's behavior after the crossover.

4. **Whichever comes first, the instrument must use the REAL system prompt and
   ALL 12 tool schemas.** W36 proved the toy task is deterministic (`evc=49` on
   all 40 generations) and cannot reach the defect. Keep the paired design and
   the four validity gates - G4 earned its place.

5. **Read `load_few_shot_exemplars("native_openhands")`** and measure the
   exemplar token volume (section 2.4). It is an unmeasured constant inside
   every context budget calculation on this path.

6. **Decide the 3000 constant's fate.** It is hardcoded at :116, referenced
   nowhere else, unconfigurable, and smaller than the SYSTEM prompt alone. Any
   change is a behavior change on three call sites and gets its own verification
   round. Do not fold it into another patch.

7. **Characterize PATH 2's confirmation gate** - which executor instance is
   injected into `NativeOpenHandsAgent` and how it is constructed. Feeds the SDP
   Defect 6 section directly (W10: the gate is decided at executor construction).

8. **Make `load_config()` BOM-tolerant** as its own isolated patch. Until then a
   machine-regenerated BOM'd `config.toml` takes the backend down on next start.

9. **Correct the Graystone Lab model inventory** - `qwen3-coder:30b` is
   `qwen3moe`, 30.5B, not a dense 32B. The "NO MoE model is present" note is
   wrong.

10. **Fix `.gitignore:23`** as its own change - a negation for
    `tests/*run*.txt`, verified in isolation. Until then, `-f` every run log.

11. Ask Gray for the true Yahoo Inbox count from the web UI. Two seconds on his
    side, unanswered since W32. `usage_report` said 12,807 / 859 MB; an August
    web-UI reading said 286K. They cannot both be true.

12. Chase `[security] mode = "warn"` - unexplained config change governing a guard.

13. Defect 6 / 6e - the confirm gate client listener, still unbuilt.

14. Condense `[[openjarvis-rollback-points]]`, at its size cap.

15. The `/v1/sessions` patch - fully spec'd, still untouched.

16. `memdb_audit.log` under the 30 MB scheme.

---

## 11. PARKED - DO NOT CHASE MID-TASK

- **NEW: the three 4000-char inline observation caps** (:451-452, :480-481,
  :499-500) are the same constant written three times. Consolidation is a
  behavior-neutral cleanup with a real regression risk. Not now.
- **NEW: the url_expanded early exit (:336-372) has no tool contract at all.**
  A run down that branch can never emit a tool call. Rule it out before
  attributing any no-tool-call run to Defect 1.
- **NEW: `[Input truncated to fit context window]` at :134 is factually wrong on
  the fallback paths** - it is appended to a TOOL OBSERVATION, not user input.
  Fixing the string is trivial; it is parked only because it must not be folded
  into the T-B patch that changes behavior.
- **NEW: the repo root has ~200 untracked working files.** A decision is owed on
  whether they get a directory, a `.gitignore` rule, or a commit.
- `/api/ps` mid-run is a safe, zero-cost production observability probe. It
  answered the VRAM question in one read against a live inference. Reusable.
- The backend listener runs on the SYSTEM Python
  (`AppData\Local\Programs\Python\Python312`), not the venv interpreter, while a
  venv python runs alongside holding no port. Which interpreter loads which
  site-packages is not understood.
- `[security] mode = "warn"` appeared in config.toml with no window on record
  setting it.
- `conv=-` on RUNSTART - the agent still receives no conversation identity.
- Format 1 of `_extract_tool_call` is case-insensitive and unanchored, so prose
  containing "action:" can produce a false-positive tool name. **Now known to be
  the gateway to BRANCH 2c, a T-B path.**
- `to_openai_function()` passes `parameters` through raw from `ToolSpec`, whose
  default is `{}`. Audit across the 12 tools.
- The confirm flow asks TWICE. UX defect, not Defect 1.
- Tool panel args render with cp437 mojibake in the desktop app.
- The 0 ms `account: yahoo` tool call preceding the real `account: yahoo_main` call.
- `git log -p --follow src\openjarvis\engine\ollama.py` to establish whether
  temperature 0.7 was deliberate or arrived with the file.
- Two benign skill-parser warnings on `research-paper-writing`. Cosmetic.

---

## 12. AMENDMENT - SYSTEM PROMPT ASSEMBLY MEASURED. TWO ITEMS CLOSED, ONE SECTION CORRECTED, ONE CLOUD-MODEL CONCLUSION REFUTED.

Appended later the same window, 09/06. Everything in this section is measured
from disk or read from source. Nothing here is estimated.

### 12.1 What was done

Located the three SYSTEM-prompt-assembly functions:

```
src/openjarvis/agents/prompt_loader.py|30|def load_system_prompt_override(agent_name: str) -> str | None:
src/openjarvis/agents/prompt_loader.py|53|def load_few_shot_exemplars(
src/openjarvis/tools/_stubs.py|480|def build_tool_descriptions(
```

Bundled `prompt_loader.py`, `tools\_stubs.py` and `native_openhands.py` whole to
the 550B (`CLOUDBUNDLE-adhoc-20260906-123255.md`, 3 of 3, ~15k tokens) with five
questions on assembly, volume and observability. Then checked the two disk paths
the loader constructs, because that half is a filesystem question no cloud model
can answer from source.

### 12.2 THE MEASUREMENT - BOTH OVERRIDE FILES ARE ABSENT

```
DIR: C:\Users\Admin\.openjarvis\agents\native_openhands
DIRECTORY DOES NOT EXIST
---
ABSENT: C:\Users\Admin\.openjarvis\agents\native_openhands\system_prompt.md
ABSENT: C:\Users\Admin\.openjarvis\agents\native_openhands\few_shot.json
```

The parent directory does not exist. Neither file exists.

**Consequence 1 - the live SYSTEM template is CONFIRMED.**
`load_system_prompt_override("native_openhands")` returns `None`
(`prompt_loader.py:38-39`), so `:326`'s `or` falls through to
`OPENHANDS_SYSTEM_PROMPT`. **The hardcoded constant at `native_openhands.py:25-53`
IS the live SYSTEM prompt.** Three windows of reasoning against it were correct.
This was an assumption; it is now a measurement.

**Consequence 2 - EXEMPLAR CONTRIBUTION IS ZERO.**
`load_few_shot_exemplars` returns `[]` (`prompt_loader.py:63-64`), the `for` loop
at `:377-380` never executes, and no exemplar messages are ever inserted.
**Zero chars, zero tokens, on every run on this machine.**

### 12.3 CORRECTION TO SECTION 2.4

Section 2.4 claimed the exemplars "inflate the overflow they can never absorb."
**That is wrong as to effect.** They inflate nothing, because there are none.

The mechanism it describes is real and worth keeping: `load_few_shot_exemplars`
has **NO cap** - no max-items, no max-chars (`prompt_loader.py:66, :76`) - each
exemplar becomes TWO messages, and they are counted in `total_chars` at `:119`
every turn while sitting further back than the user ask so the native-path scan
never reaches them. **The hazard is armed and dormant.** Dropping a
`few_shot.json` into that directory would activate it silently, with no cap and
no log.

Record it as a HAZARD, not as a current contributor to any budget.

### 12.4 THE 550B's Q4 CONCLUSION IS REFUTED

The 550B concluded that the assembled prompt totals ~18,849 chars / ~4,712
tokens before user input, **exceeds the 3000-token budget by 57%**, and that
"the guard will fire on the very first call at :382."

**That conclusion rested entirely on 9,600 chars of exemplars it assumed into
existence** ("assume 3 exemplars, 600 chars input + 1,000 chars output each").
Its own brief instructed it not to estimate where it could count. It estimated.

With exemplars measured at zero, its remaining figure for the SYSTEM message is
~9,249 chars / ~2,312 tokens - **UNDER the 3000 budget.** So at `:382`, before
any turn, `_truncate_if_needed` returns at `:121-122` without reaching the
backward scan at all.

**The guard does not fire early. It fires late, once tool observations
accumulate - which is precisely the T-A / T-B split derived in section 2.2 from
direct reads.** Our arithmetic survives. The cloud model's conclusion does not.

**METHOD NOTE, and it is the important one:** the 550B's Q1, Q2, Q3 and Q5 were
well-sourced and cited. Its Q4 was a confident wrong conclusion built by
compounding four estimates. **The failure was not in any single number - it was
in stacking estimates and then reporting the stack as a finding.** Same shape as
its Q4 on the previous bundle (section 3.3). Treat any cloud-model answer that
concludes rather than cites as a hypothesis, every time, regardless of how well
the neighbouring answers are sourced.

### 12.5 NEW FINDINGS, WELL-SOURCED, ACCEPTED

These came from the 550B with citations and are consistent with our own reads.

- **The override fallback is SILENT and UNDISTINGUISHABLE at the call site.**
  Both "file absent" (`prompt_loader.py:38-39`) and "read failed"
  (`:46-50`, catching bare `Exception`) return `None`. `:326`'s `or` swallows
  both identically. A corrupt or unreadable override is indistinguishable from
  no override at all. **FOURTH instance of the silent-versus-loud failure theme**
  (W35 BOM, W36 `.gitignore`, W37 bundle paths, now this).
- **`load_few_shot_exemplars` has NO cap of any kind** (`:66, :76`). Whatever is
  in the file goes in, doubled, every turn.
- **THE ASSEMBLED PROMPT SIZE IS INVISIBLE AT RUNTIME.** RUNSTART's `chars=%d`
  at `:605` logs **user input length only**. Nothing anywhere logs the SYSTEM
  size, the tool-description size, or the exemplar total. `_truncate_if_needed`
  logs nothing at all. **This is why this question has taken three windows and
  is still partly open: the system cannot tell us its own prompt size.**

### 12.6 A DISCREPANCY THAT IS NOW EXPLICIT

The ~3,980-token SYSTEM overhead figure has been carried since W36. With
exemplars measured at zero and the 550B's own estimate of the assembled SYSTEM
message at ~2,312 tokens, **those two numbers do not reconcile.** One is wrong.

Both are estimates, so this cannot be settled by more estimating. It needs the
reported prompt-token count from the engine - which is exactly what
`ollama.py:126` masks behind `prompt_tokens = max(reported, estimated)`.

**This raises next-action 2 from prerequisite to blocking.** Until `:126` is
unmasked there is no trustworthy prompt-size number anywhere in the system, and
every budget argument on this path rests on arithmetic nobody can check.

### 12.7 STATUS CHANGES TO SECTION 10

- **Next-action 5 (read `load_few_shot_exemplars`) is CLOSED.** Answer: zero
  contribution, uncapped mechanism, dormant hazard. Do not re-open; re-check
  only if `~\.openjarvis\agents\native_openhands\` ever appears on disk.
- **Next-action 2 (unmask `ollama.py:126`) is now BLOCKING**, per 12.6. It
  should open the next window, alone, verified in isolation per the 08/17 rule.
- **NEW next-action:** make the override fallback loud. A one-line log
  distinguishing "no override present" from "override failed to read" at
  `prompt_loader.py:46-50`. Its own isolated patch; do not fold it into anything.
- **NEW next-action:** log assembled prompt size at RUNSTART - `sys_chars`,
  `tools_chars`, `exemplar_chars` alongside the existing `chars=%d`. This is the
  instrument that makes every future context question answerable in one log
  line instead of one window. **Cheap, high leverage, and it is the thing whose
  absence cost this window and the two before it.**

### 12.8 SDP ADDITIONS FROM THIS AMENDMENT

- **Add to 5.2 (truncation chain):** stage 0, prompt assembly, is UNOBSERVABLE.
  The chain's input size is not measured anywhere in the running system. Any
  budget documented in the SDP is therefore derived, not observed, and must be
  labelled as such until `:126` is unmasked and RUNSTART is instrumented.
- **Add to 5.1 (dual transport):** the SYSTEM-side transport has a silent
  override mechanism with an undistinguishable failure mode. The prose half of
  the tool contract can be swapped or corrupted from disk with no runtime signal.
- **Add to 5.4 (evidence standard):** this amendment is the cleanest example on
  record of the standing method working. A cited answer and a concluded answer
  arrived in the same reply from the same model; one command against the
  filesystem separated them. **Name in the SDP: cloud models answer source
  questions, never state-of-this-machine questions. Route accordingly.**
- **Dormant-hazard pattern, new to the SDP:** the codebase contains at least one
  uncapped ingestion path that is inert only because a file happens not to
  exist. Worth an audit for others of the same shape.

---

## 13. SECOND AMENDMENT - NEXT-ACTION 2 IS REFUTED. THE T-A INSTRUMENT ALREADY EXISTS AND IS ALREADY PERSISTED. THE 8192 CLAMP IS REAL AND HISTORICAL. `prompt_tokens` IS NOT TRUSTWORTHY.

Appended later the same window, 09/06, after section 12. Still no code modified,
no backend restart. Two read-only probe scripts were written to the repo root;
both are new untracked files, see 13.8.

### 13.1 NEXT-ACTION 2 IS REFUTED. THERE IS NOTHING TO UNMASK.

W36 next-action 6, carried into W37 as next-action 2 and escalated to BLOCKING
in section 12.6, said: "Unmask `ollama.py:126` - `prompt_tokens =
max(reported, estimated)` discards the field that shows truncation."

**It discards nothing.** Read at `engine\ollama.py:118-142`:

```
118: data = resp.json()
119: # prompt_eval_count = tokens actually evaluated (KV-cache-aware).
120: # estimate_prompt_tokens = full prompt size (for cost comparison).
121: # We report both so downstream can use the right one:
124: reported_prompt = data.get("prompt_eval_count", 0)
125: estimated_prompt = estimate_prompt_tokens(messages)
126: prompt_tokens = max(reported_prompt, estimated_prompt)
127: prompt_tokens_evaluated = (
128:     reported_prompt if reported_prompt > 0 else prompt_tokens
129: )
135: "prompt_tokens": prompt_tokens,
136: "prompt_tokens_evaluated": prompt_tokens_evaluated,
```

`:126` is not a mask. It is one half of a **deliberate, documented two-field
design**: `prompt_tokens` is full assembled size, `prompt_tokens_evaluated` is
the engine's reported `prompt_eval_count`. **Both are already in the usage
dict.** The same pattern repeats on the two streaming paths at `:219-229` and
`:355-365`, and in `_openai_compat.py:95`.

**Do not patch `:126`. The carried assumption was wrong for two windows.**

The mojibake at `:122-123` is confirmed to be the arrow glyphs inside those
comment lines. Cosmetic, comments only, no logic affected.

### 13.2 THE T-A INSTRUMENT EXISTS, IS FULLY PLUMBED, AND WRITES TO A DATABASE

`prompt_tokens_evaluated` is not a dead field. Traced end to end:

```
core/types.py:135                  field on the record type
engine/ollama.py:136,228,364       emitted on all three generate paths
engine/_openai_compat.py:95        emitted on the compat path
telemetry/instrumented_engine.py:133,211   captured from usage
telemetry/store.py:25,83,130,167   REAL COLUMN, written every record
telemetry/aggregator.py:132,139,195        SUM() aggregated
server/savings.py:92-113           consumed
server/routes.py:660-661           consumed
```

`InstrumentedEngine` wraps the engine on the server path at `cli\serve.py:211`,
so backend traffic is recorded. **The measurement T-A needs has been collecting
itself in production this whole time.** No patch, no probe build, no restart was
ever required to obtain it.

**Database:** `C:\Users\Admin\.openjarvis\telemetry.db`, 958,464 bytes, last
written 09/05 09:50:00 - live and current. **6,992 rows.**

### 13.3 WHAT THE 6,992 ROWS SHOW

Probe `probe_telemetry_truncation.py`, whole-table:

```
AGENT       ROWS  PTE_ZERO  PT_GT_PTE   MAX_PT  MAX_PTE
(blank)     6992       338        396   168726    16226
```

Probe `probe_telemetry_ceiling.py`, banded:

```
PTE CEILING BANDS (pte > 0)
  A 8000-8192 (8k clamp)       n=137    lo=8001    hi=8192
  B 15900-16384 (16k clamp)    n=1      lo=16226   hi=16226
  D below bands                n=6516   lo=32      hi=7999
```

**FINDING 1 - THE 8192 CLAMP IS REAL.** 137 rows sit in 8000-8192 with `hi`
EXACTLY 8192. A prompt cannot be evaluated above the context window, and KV-cache
reuse cannot produce an exact ceiling AT the window size. **Ollama does clamp at
`num_ctx`, and it is recorded in production history.** The mechanism T-A
depends on is confirmed to exist.

**FINDING 2 - THE CLAMP EVIDENCE IS ALL HISTORICAL.** Every clamped row predates
W34's move to 16384. Post-change there is exactly ONE row near 16k - 16226, which
is UNDER 16384 and therefore a large prompt that FIT, not a clamp. **Band B is a
single row and is NOT a cluster.** If the 16k window were being hit routinely we
would see a band-B cluster the shape of band A. We do not.

### 13.4 REFUTED IN FLIGHT - `pt_gt_pte` IS NOT A TRUNCATION COUNT

I was building toward reading the 396 `pt_gt_pte` rows as truncations. **That
reading is wrong and the data refuted it before it reached this file.**

`prompt_tokens_evaluated` is documented at `:119` as KV-cache-aware. On any
multi-turn conversation with cache hits, evaluated is legitimately below full
size **with nothing dropped**. So `pt > pte` is the expected steady state, not a
defect signal. **The exact-8192 ceiling is the evidence. The raw gap count is
not.** Any future query must band on the ceiling, never count the gap.

### 13.5 FINDING 3 - `prompt_tokens` IS NOT TRUSTWORTHY AS ASSEMBLED SIZE

Top rows by gap:

```
08-07 09:42:51  qwen3-coder:30b   pt=167152  pte=4234  ct=255  gap=162918
08-07 09:37:28  qwen3-coder:30b   pt=168726  pte=5918  ct=53   gap=162808
08-07 09:34:04  qwen3-coder:30b   pt=166086  pte=8192  ct=390  gap=157894
07-10 17:48:44  qwen2.5-coder:32b pt=30741   pte=8192  ct=53   gap=22549
```

**These are NOT truncations.** A 167k-token prompt against an 8k window would
clamp AT 8192 - and the 09:34 row does exactly that. But the 09:42 and 09:37
rows evaluated 4,234 and 5,918, nowhere near any window boundary. **A prompt
cannot be clamped to a value below the window.**

So on those runs either `estimate_prompt_tokens(messages)` returned a wildly
wrong figure, or the two fields are measuring different objects on that path.
**The largest gaps in the entire database are an estimator artifact.**

**CONSEQUENCE, AND IT REACHES BACKWARD:** `prompt_tokens` derives from
`estimate_prompt_tokens` via the `max()` at `:126` whenever the estimate exceeds
the reported count. Section 12.6 flagged that the ~3,980-token overhead figure
and the ~2,312 estimate do not reconcile. **This is very likely why.** Do not
quote any assembled-size figure that traces back to `estimate_prompt_tokens`
until that function is read and its behavior on tool-carrying messages is
established. **That function has never been read in any window.**

### 13.6 FINDING 4 - THE `agent` COLUMN IS BLANK ON ALL 6,992 ROWS

`telemetry\store.py:23` defines `agent TEXT NOT NULL DEFAULT ''`. Every row in
the database carries the default. **Nothing populates it.**

**This is why the telemetry cannot close T-A.** The 137 clamped rows cannot be
attributed to `native_openhands` rather than to a research loop, a CLI ask, or
any other caller. A real defect in its own right, and cheap to fix - the column
exists, the writer just never sets it.

### 13.7 FINDING 5 - `research_router.py:92` WRITES THE WRONG KEY

```
server/research_router.py:92: prompt_tokens_evaluated=int(usage.get("prompt_tokens", 0))
```

It reads `prompt_tokens` and stores it as `prompt_tokens_evaluated`, assigning
full assembled size to the evaluated field. **That path's telemetry is silently
wrong**, and it inflates `prompt_tokens_evaluated` toward `prompt_tokens` on
every research run - which would mask exactly the gap we are looking for.
Unrelated to Defect 1, real, and it contaminates the table we just queried.

### 13.8 STATUS OF T-A AFTER THIS AMENDMENT

**T-A is NEITHER CONFIRMED NOR REFUTED.** State it plainly:

- The mechanism is REAL - Ollama clamps at `num_ctx`, 137 rows prove it.
- The evidence is HISTORICAL - all clamping predates the 16384 change.
- Post-16384 there is ONE near-window row and it FIT.
- Attribution is IMPOSSIBLE with the `agent` column blank.
- The estimator feeding `prompt_tokens` is not trustworthy (13.5).

**We found that the mechanism is real. We did not find it firing on our path.**

**T-B is unaffected by any of this** and remains provable from source. It is
now clearly the cheaper of the two theories to close.

### 13.9 NEW UNTRACKED FILES

Both in the repo root, both read-only against the database, both ASCII:

- `probe_telemetry_truncation.py` - whole-table counts grouped by agent
- `probe_telemetry_ceiling.py` - ceiling bands plus top-gap rows

**Primary evidence, re-runnable, and NOT regenerable from memory.** They are
`.py` so `.gitignore:23` (`*.txt`) will not swallow them, but commit them
deliberately with their output captured, per the W36 lesson about run logs.

### 13.10 REVISED NEXT ACTIONS - SUPERSEDES SECTION 10 ITEMS 2 AND 5

1. **DELETE next-action 2 entirely.** `ollama.py:126` needs no patch (13.1).

2. **READ `estimate_prompt_tokens`.** Never read in any window. It feeds
   `prompt_tokens` on every path via the `:126` `max()`, and 13.5 shows it
   producing 167k figures that cannot be right. **Every assembled-size number
   this project has quoted for three windows depends on it.** Highest-value
   read on the list.

3. **POPULATE the `agent` column** (13.6). Without it no telemetry query can
   ever be attributed to a dispatch path. Small, isolated, and it makes the
   existing 6,992-row instrument useful going forward.

4. **FIX `research_router.py:92`** (13.7). One-line wrong-key bug contaminating
   the telemetry table.

5. **CLOSE T-B FIRST.** It is provable from source, needs no telemetry, no
   restart, and no estimator we distrust. Drive a CodeAct or Action-Input turn
   with a large observation; assert whether `:129` fires and whether the
   `[Output truncated]` marker survives.

6. **T-A stays OPEN pending items 2 and 3.** Do not build a T-A instrument until
   the estimator is understood and the agent column is populated - a probe built
   on an untrusted estimator would produce another confident wrong number.

### 13.11 SDP ADDITIONS FROM THIS AMENDMENT

- **New architecture chapter: the telemetry spine.** `InstrumentedEngine` ->
  `TelemetryStore` -> `telemetry.db` -> `TelemetryAggregator` -> the savings and
  routes consumers. Ports, protocols, encoding per the 08/22 pin: local SQLite
  file, `sqlite3.connect(check_same_thread=False)`, schema at `store.py:17-40`
  with a migration list at `:130`. Deliver as a downloadable artifact.
- **Two-field token accounting is a DESIGN DECISION, not a defect** (13.1).
  Document `prompt_tokens` versus `prompt_tokens_evaluated` and which consumer
  should use which. W36 recorded it as a defect for two windows; the SDP should
  record both the decision and the misreading, since the misreading is what
  drove two windows of next-actions.
- **Add to 5.2 (truncation chain), stage 4:** the Ollama-server clamp is
  CONFIRMED REAL with 137 production measurements at exactly 8192. Stage 4 is no
  longer hypothetical - only its current relevance at 16384 is open.
- **Evidence standard, new template:** an exact ceiling AT a configured limit is
  proof of clamping; a gap between two token fields is NOT, because one field is
  cache-aware. **Band on the boundary, never count the gap** (13.4).
- **Instrument-before-building lesson, and it is the window's best one:** three
  windows were spent designing probes to measure something the system was
  already recording to a database on every call. **Before building an
  instrument, search the schema.** Add this to the SDP method chapter beside the
  G4-gate lesson.

---

## 14. THIRD AMENDMENT - THE AGENT PATH IS VERIFIED END TO END. PATH 2's GATE IS LIVE. TWELVE TOOLS CONFIRMED FROM CONFIG. AND A NEW SDP CHAPTER: DEPLOYMENT DIVERGENCE FROM UPSTREAM.

Appended later the same window, 09/06, after section 13. Still no code modified
and no backend restart. All reads.

### 14.0 STANDING CONTEXT - RECORD THIS ONCE SO IT STOPS NEEDING REPETITION

**Gray stated this three times across this window. It is not a finding, it is
the frame every finding in this project sits inside, and it was never written
down before now.**

OpenJarvis was cloned from the author's GitHub as an operational project.
**The author's agent-activation steps were NEVER run.** Qwen 30B was observed to
handle tools internally, `native_openhands` was adopted on that basis, and it
has been the agent ever since.

**Every agent behavior in OpenJarvis today was built by Gray.** The email
handling is his code. MCP was added by him. Memory was added by him. The tool
registrations that let Jarvis read and trash email are his. The `[DEBUG]` prints
at `serve.py:268/:280/:281` are his instrumentation, not upstream's.

**Consequence for every future window:** do not reason about this deployment as
if it were a stock install of the upstream project. When something upstream
would populate is empty, the first hypothesis is "that activation step was never
run," not "this is a defect." See 14.5.

Gray also has a 26 TB drive available for offloading, and a standing requirement
that all communications be captured. Not chased this window - noted because a
capture store, if it exists, is a second evidence source alongside
`telemetry.db`, and section 13's lesson applies to it: search what already
exists before building anything to collect it.

### 14.1 OPEN ITEM #3 IS VERIFIED - THE AGENT RECEIVES THE INSTRUMENTED ENGINE

Section 13.2 said `InstrumentedEngine` wraps the engine on the server path and
called the agent's use of it "provisionally cleared." **It is now fully traced.**

```
cli\serve.py:211  engine = InstrumentedEngine(engine, bus, energy_monitor=energy_mon)
cli\serve.py:241  agent_cls = AgentRegistry.get(agent_key)
cli\serve.py:319  agent = agent_cls(engine, model_name, **agent_kwargs)
```

`:211` **rebinds the name** - from that line on, `engine` IS the wrapper. `:319`
passes that same name to the agent constructor. **The agent runs on the
instrumented engine, so the 6,992 rows in `telemetry.db` include the
`native_openhands` runs.** Section 13's telemetry findings apply to our path.

**Construction sites found, corrected:** `server\api_routes.py:77` is NOT a
construction site - it is a listing endpoint enumerating registered agents
(`AgentRegistry.keys()` -> class name -> `accepts_tools`). It is almost
certainly what populates the agent dropdown in the desktop UI. Remove it from
any list of places an agent is built. Real construction sites are
`cli\serve.py:241`, `system\orchestrator.py:132`, `agents\executor.py:88/:250`,
`cli\chat_cmd.py:86`, `cli\ask.py:336`, `sdk.py:463`.

**The agent is never constructed by name.** No `NativeOpenHandsAgent(...)` call
exists anywhere. It is built through `AgentRegistry` (registered at
`native_openhands.py:56`), so the agent never chooses its own engine - the
construction site does. That is upstream's design and it is why the engine
question had to be answered at the call site.

### 14.2 HAZARD - INSTRUMENTATION FAILURE IS SILENT, AND IT DISABLES THE SPINE

```
211: engine = InstrumentedEngine(engine, bus, energy_monitor=energy_mon)
212: except Exception as exc:
213:     logger.debug("Engine instrumentation failed: %s", exc)
```

If `InstrumentedEngine` construction throws, `engine` remains the RAW unwrapped
object, the server starts normally, and the only trace is a **debug-level** line
most configurations never emit. Same shape at `:208-209` for the energy monitor.

**FIFTH instance of the silent-versus-loud failure theme in this window alone**
(W35 BOM, W36 `.gitignore`, W37 bundle paths, the prompt-override fallback at
12.5, now this).

**Direct consequence for section 13:** if instrumentation ever failed on a
start, every run from that session recorded NOTHING to `telemetry.db`, and there
is no way to detect that from the data. The 6,992 rows are a floor, not a
census. Any future telemetry conclusion must state this caveat.

### 14.3 PATH 2's CONFIRMATION GATE IS LIVE - SECTION 4's "OPEN" IS CLOSED

`cli\serve.py:288-317`, tagged `openjarvis-confirm-live-v1`:

```
296: _confirm_flag = _os.getenv("OPENJARVIS_CONFIRM_INTERACTIVE", "1")
299: if _confirm_flag.strip().lower() not in ("0","false","no","off"):
308:     def _server_confirm_callback(_prompt: str) -> bool:
309:         _cid = _confirm_stubs.CURRENT_CONFIRM_ID.get()
310:         if not _cid:
311:             return False
312:         return _cr.wait(_cid) == _cr.APPROVED
314:     agent_kwargs["interactive"] = True
315:     agent_kwargs["confirm_callback"] = _server_confirm_callback
```

**The gate is ON BY DEFAULT on the chat path** - the env var defaults to `"1"`
and must be explicitly set to a falsy value to disable it. The callback is a
REAL blocking wait on `confirm_registry`, **not** the
`lambda _prompt: True` auto-approver W10 found at the agent_manager sites
(`agent_manager_routes.py:1202-1206, 1562-1563, 1639-1640`).

**This is the opt-in-per-run design the W10/W13 constraint demanded, actually
implemented.** The comment at `:289-292` states the reason explicitly:
unattended entry points must never inherit a blocking gate.

Record for the execution-path register: **PATH 2 (chat, via `serve.py`) has a
LIVE gate with the 120 s TTL behind it.** The auto-approved paths remain the
managed-agent sites. That contrast - same tool, same process, different gate
status by construction site - is W10's finding, now with both sides confirmed.

### 14.4 TWELVE TOOLS - VERIFIED FROM CONFIG, WITH ONE CAVEAT

`C:\Users\Admin\.openjarvis\config.toml`:

```
13: [agent]
16: tools = "code_interpreter,file_read,file_write,shell_exec,think,calculator,
        retrieval,mailbox_list_accounts,mailbox_usage_report,mailbox_find_messages,
        mailbox_move_to_trash,mailbox_empty_folder"
17: max_turns = 15
26: [server]
29: agent = "native_openhands"
```

**Counted: exactly twelve.** The carried 12-tool figure SURVIVES verification -
the first carried number today to do so.

`config.agent.tools` is set, so the `else` at `serve.py:265` is never reached and
`_DEFAULT_TOOLS = {"think","calculator","web_search"}` **never applies.** That is
by Gray's design, not an accident - see 14.5.

`config.toml:29` confirms `agent = "native_openhands"` server-side, matching the
desktop UI selection. **The path analyzed all window is the path that runs.**

**CAVEAT, AND IT IS NOT CLOSED: twelve is the number REQUESTED, not the number
LOADED.** The loop at `serve.py:270-279` only appends tools present in
`ToolRegistry.keys()` that pass an `issubclass(BaseTool)` check. Any of the
twelve that failed to register is dropped **silently**. The mailbox tools are
Gray's additions, so they are the ones most exposed to a registration failure.

**Twelve requested: VERIFIED. Twelve loaded: STILL ASSUMED.**

**Also on this list and worth stating plainly:** `shell_exec`, `file_write`,
`file_read`, `code_interpreter` and `mailbox_move_to_trash` are all destructive
or high-privilege, and they are live on the chat path. The gate at 14.3 is doing
real work, not theoretical work.

### 14.5 THE `[DEBUG]` INSTRUMENTATION HAS NEVER BEEN READABLE

`serve.py:268`, `:280`, `:281` print `allowed=`, `registry_keys=` and
`tools_loaded=` unconditionally with `flush=True`. These are Gray's, added
specifically to answer the question 14.4's caveat leaves open.

**Measured: ZERO `[DEBUG]` lines in 715,164 bytes of `backend.log`**, while the
log is demonstrably live (uvicorn access lines one minute before the query).

**Cause: the log captures the `logging` module only. Raw `print()` goes to a
console that nothing reads**, because the backend runs detached.

**This is section 12.5's finding arrived at from the opposite direction.** There:
the system does not log prompt size. Here: when instrumentation WAS added, the
transport dropped it. Three `print()` calls have executed on every start since
they were written and have never produced a readable byte.

**STANDING LESSON, and it belongs in the SDP method chapter:
INSTRUMENTATION YOU CANNOT READ IS INSTRUMENTATION YOU DO NOT HAVE.** Verify the
output path of any instrument at the moment you add it, not when you need it.
This is a sibling of section 13's "search the schema before building the
instrument."

**Fix is one word** - `print(...)` becomes `logger.info(...)` at all three lines.
It is a source patch requiring a restart to verify, so it is a next-window item,
isolated, per the 08/17 rule.

### 14.6 NEW SDP CHAPTER - DEPLOYMENT DIVERGENCE FROM UPSTREAM

**Agreed with Gray this window. This is a new SDP chapter and it may be the most
important one for the stated goal of a standardized Jarvis installation across
platforms.**

The situation: this deployment deliberately diverges from the upstream author's
activation model (14.0). Every divergence was a deliberate choice. **None of them
is written down as one.** A future window reading `config.toml:16` cold sees
twelve tools and no reason why - and the reason is the load-bearing part.

**The argument for the chapter:** a standardized Jarvis installation across
platforms IS a specification. A divergence list, once written down, IS that
specification. Someone rebuilding Graystone's Jarvis on another box needs this
list, not the upstream README.

**Known divergences to date - START HERE, THIS IS NOT EXHAUSTIVE:**

1. **Agent activation never run** per upstream instructions (14.0).
2. **Explicit 12-tool list** in `config.agent.tools`, bypassing
   `_DEFAULT_TOOLS` (14.4).
3. **Custom mailbox tools** - `mailbox_list_accounts`, `mailbox_usage_report`,
   `mailbox_find_messages`, `mailbox_move_to_trash`, `mailbox_empty_folder`.
   Gray's code.
4. **MCP added.**
5. **Memory added.**
6. **`[DEBUG]` tool-loading instrumentation** at `serve.py:268/:280/:281`
   (14.5).
7. **`openjarvis-confirm-live-v1`** - the live confirmation gate at
   `serve.py:288-317` (14.3).
8. **`num_ctx` threading** through the ollama engine, W34/W35, commit `c37d8b1`.
9. **`openjarvis-retry400-v1`** at `ollama.py:104/:107`.
10. **Patch 4 RAWGEN diagnostics**, tagged temporary in `c37d8b1`.

**Per-divergence the chapter should record:** what upstream does, what we do
instead, why, what it depends on, and how to reproduce it on a fresh box.

**A second use for this chapter, immediately:** it is the correct first
hypothesis whenever something upstream would populate turns up empty. The blank
`agent` column in `telemetry.db` (13.6) is a live candidate - it may not be a
defect at all, but a field upstream's activation path populates and ours never
wires. **Re-examine 13.6 under this lens before treating it as a bug to fix.**

### 14.7 ASSUMPTION AUDIT - STATE OF PLAY

Gray asked directly what remains assumption rather than ground proof. Recorded
so the next window inherits the distinction rather than the confidence.

**VERIFIED THIS WINDOW:** commit state; dual tool-contract transport; the role
census; `_truncate_if_needed` cannot touch SYSTEM; override and exemplar files
absent; `prompt_tokens_evaluated` plumbed and persisted; 137 rows at exactly
8192; blank `agent` column; agent receives the instrumented engine (14.1); gate
live on PATH 2 (14.3); twelve tools requested (14.4); `[DEBUG]` output never
captured (14.5).

**STILL ASSUMPTION:**

1. **T-A and T-B themselves.** Both derived from reading code. No production
   turn has been OBSERVED doing either. T-B is provable from source; it is not
   yet proven.
2. **The ~3,980-token SYSTEM overhead.** Source unknown, traces through an
   estimator now distrusted (13.5). Weakest number on the books, and it appears
   in both T-A and T-B arithmetic.
3. **Twelve tools LOADED** (14.4 caveat). Only twelve REQUESTED is verified.
4. **That the 137 clamped rows are Ollama clamping** rather than something else.
   Strong inference from an exact ceiling at the configured limit; with `agent`
   blank and the estimator distrusted, still inference.
5. **`build_tool_descriptions` volume.** The 550B estimated ~8,062 chars for 12
   tools. Never counted.
6. **W36's "truncation drops WHOLE MESSAGES."** Inherited from v3's
   8192-landing-at-6818 observation. Plausible, never directly confirmed.

**THE PATTERN, AND IT IS THE WINDOW'S SUMMARY JUDGEMENT:
EVERYTHING ABOUT STRUCTURE IS VERIFIED. EVERYTHING ABOUT MAGNITUDE IS ASSUMED.**
We know exactly what the code does. We do not trust a single number describing
how much.

### 14.8 REVISED NEXT ACTIONS - SUPERSEDES 13.10

1. **CLOSE T-B.** Unchanged and still first. Provable from source, no telemetry,
   no restart, no estimator dependency.

2. **READ `estimate_prompt_tokens`.** Still the highest-value read. Closes
   assumptions 2 and 5 together and explains 13.5's 167k figures.

3. **Fix the three `print()` calls to `logger.info()`** at
   `serve.py:268/:280/:281` (14.5). Isolated patch, one restart, and it closes
   assumption 3 permanently - twelve loaded versus twelve requested becomes a
   log line on every start instead of an open question.

4. **Re-examine the blank `agent` column under the divergence lens** (14.6)
   before writing any patch for it. It may be an unrun activation step.

5. **Write the SDP deployment-divergence chapter** (14.6). Gray agreed to it
   this window. Ten known divergences listed; the list is not exhaustive and
   should be built out while the reasoning is still recoverable.

6. **Fix `research_router.py:92`** wrong-key bug (13.7).

7. **T-A stays OPEN** pending 2 and 4, plus the 14.2 caveat that the 6,992 rows
   are a floor rather than a census.

Items 8 onward: carry section 10 items 8-16 unchanged.

---

## 15. FOURTH AMENDMENT - THE AUTHOR'S DOCUMENTATION WAS READ FOR THE FIRST TIME. WE MAY BE TROUBLESHOOTING OUR OWN WORK. UPSTREAM'S ROADMAP CANNOT SERVE AS A PROGRESS MEASURE.

Final section of W37, 09/06. No code modified this window at any point. Two
documentation bundles were built and sent to the 550B; both returned.

### 15.0 THE CRITICISM THAT OPENED THIS - RECORD IT, IT IS THE MOST USEFUL THING IN THE WINDOW

**Gray, verbatim in substance:** "you naturally go back to independent
troubleshooting and building... we should be using all the resources supplied
for this build that the author provided... from my view, we are troubleshooting
our own work."

**He was right, and the pattern is now three-for-three in a single window:**

1. Section 13 - three windows of probe design for a measurement `telemetry.db`
   had been recording on every call since July.
2. Section 14.5 - instrumentation added that writes to a console nobody reads.
3. **This section - 80 files of the author's own documentation sitting in
   `docs\`, never referenced in any window, while we reverse-engineered the same
   subjects from source.**

**All three are the same failure: build or derive before checking what already
exists.** The first two were the system's. This one is mine.

**Gray also stated he had asked previously that the existence of the author's
installation files be carried forward, and it was not.** That is now pinned. It
should not have needed asking twice.

### 15.1 WHAT EXISTS THAT WE NEVER READ

```
docs\                       80 files
docs\development\roadmap.md            12,120 bytes
docs\architecture\agents.md            22,888 bytes
docs\architecture\overview.md          15,462 bytes
docs\architecture\memory.md            12,162 bytes
docs\architecture\learning.md          23,369 bytes
docs\architecture\security.md           8,348 bytes
docs\getting-started\configuration.md  35,541 bytes
docs\getting-started\installation.md    9,918 bytes
docs\getting-started\install.md         3,767 bytes
docs\telemetry.md                       6,560 bytes
docs\memory_db_schema.md                1,158 bytes
docs\assets\OpenJarvis_Architecture.png  240,689 bytes
scripts\install\        install.sh (11,829), pull-model.sh, install-rust.sh, +4
scripts\                oauth_all.py (12,288), quickstart, index_docs.py
deploy\                 docker (7 files), systemd, launchd
README.md               8,822 bytes
```

**`docs\assets\OpenJarvis_Architecture.png` is the author's own architecture
diagram.** The SDP has been building architecture artifacts from scratch.

### 15.2 THE PROGRESS MEASURE - UPSTREAM CANNOT SUPPLY IT

Gray's question: how do we measure progress against the initial requirements,
approaching one year and under 50 percent.

**ANSWER FROM THE DOCUMENTATION: upstream's roadmap CANNOT serve as the
denominator.** Cited findings:

- The roadmap uses three maturity tags - **Ready**, **Design Needed**,
  **Research-Stage** (`roadmap.md:29-36`). **NOTHING is marked Done or
  Complete anywhere in it.**
- It is explicitly a "where you can help" contributor document, not a
  completion tracker.
- The only "Currently supported" list (`roadmap.md:62-67`) contains THREE items,
  all channels: SendBlue iMessage/SMS, Slack Socket Mode, Desktop Interact tab.
- The 550B's Q5 independently confirms the gap: **no quantitative success
  criteria, no acceptance criteria per preset, no completion gates, no outcome
  metrics, no test matrix, no milestone definitions.** The documentation
  describes architecture and aspiration, not measurable outcomes.

**CONSEQUENCE: the progress denominator must be GRAY'S OWN INITIAL
REQUIREMENTS.** That document is the one that matters and it has not been
located. **Finding it, or reconstructing it, is now the first step of any
progress measure.** Upstream's capability list (15.3) is useful as a
CAPABILITY INVENTORY - what exists to be used - but not as a scorecard.

### 15.3 ALL SEVEN EXECUTIVE-ASSISTANT DUTIES ARE CLAIMED AS SHIPPED

The 550B was asked which executive-assistant duties the author claims. **All
seven come back covered**, with citations:

| Duty | Author's claimed provision |
|---|---|
| Email | `morning-digest` presets + `jarvis connect gdrive` (Gmail) |
| Calendar | same GDrive OAuth flow (Calendar, Tasks) |
| File management | `FileReadTool`, `code-assistant` preset, `jarvis memory index` |
| Scheduling | `scheduled-monitor` preset, `OperativeAgent`, `TaskScheduler` (cron/interval/once, SQLite persistence) |
| Web tasks | `WebSearchTool`, `deep_research` agent |
| Document work | `deep_research` with citations, chunking/embedding, `RetrievalTool` |
| **Recall of past actions** | **Memory primitive (5 backends), context injection, `MonitorOperativeAgent` - "long-horizon monitoring with memory, compression, and retrieval"** |

**THE RECALL ROW IS THE ONE THAT MATTERS.** Gray stated persistent memory was
set up but recall of past actions and a lessons-learned loop were never
finished. **`monitor_operative` is registered, appears in his own agent
dropdown, and has never been used.** It is upstream's answer to exactly that
requirement.

Also never evaluated: `jarvis init --preset` ships **seven starter configs**
(`morning-digest-mac`, `morning-digest-linux`, `morning-digest-minimal`,
`deep-research`, `code-assistant`, `scheduled-monitor`, `chat-simple`). Gray
hand-wrote `config.toml`.

### 15.4 THE HARD FINDINGS FROM BUNDLE 2 - CITED, NOT CONCLUDED

**A. `native_openhands` IS ABSENT FROM THE CONFIG REFERENCE.**
`configuration.md:201` lists valid `[agent] default_agent` values as: `simple`,
`orchestrator`, `react`, `operative`, `monitor_operative`. **`native_openhands`
is not among them.** It is documented in `agents.md:257-285` and `README.md:123`
but absent from the configuration reference table.

**We have built a year of work on the least-documented agent in the project.**
This alone may explain why so much of its behavior had to be derived from source.

**B. `max_turns` DEFAULT FOR `native_openhands` IS 3, NOT 10.**
Per the 550B's Q4 reading of `agents.md`. Gray's `config.toml:17` sets 15.
Five times the documented default for that agent. Not necessarily wrong -
but it is a divergence nobody recorded.

**C. NO INSTALL PATH CREATES THE PROMPT-OVERRIDE FILES.** Confirmed against
section 12.2's measurement. `~\.openjarvis\agents\<name>\system_prompt.md` and
`few_shot.json` are opt-in advanced overrides, never generated by
`jarvis init`, the one-line installer, or any preset. **Section 12.2's finding
that both are absent is EXPECTED BEHAVIOR for a standard install, not an
anomaly.** Correct the reading, keep the measurement.

**D. THE AUTHOR DOCUMENTS NO GUIDANCE FOR THE DEFECT 1 FAILURE MODE.** Q4
returned: no retry logic for malformed tool calls, no parse-failure handling, no
context-window-error guidance. `NativeOpenHandsAgent`'s documented behavior when
neither a code block nor an `Action:` is found is "returns the content as the
final answer" - **which is precisely the Defect 1 signature, described in the
author's own documentation as normal operation.**

**E. TWO PROMPT-OVERRIDE MECHANISMS THAT DO NOT MEET.** `config.py:922` defines
`system_prompt_path` and `configuration.md:205-206` documents it - but the
consumers are `operators\loader.py` and `recipes\loader.py`, **not**
`native_openhands`'s prompt assembly, which uses `load_system_prompt_override`'s
directory convention instead. **Setting the documented config key would not
affect the chat path.** Anyone attempting the documented route needs to know
this first.

### 15.5 THE OPEN QUESTION THAT ENDS THE WINDOW - DOCUMENTED VERSUS IMPLEMENTED

**`configuration.md:556-557` documents `[security] enforce_tool_confirmation`.**
Verified present in code: `core\config.py:1198` -
`enforce_tool_confirmation: bool = True`, written into generated configs at
`config.py:2028`.

**Gray's `config.toml` `[security]` block is three lines:**

```
[security]
profile = "personal"
mode = "warn"
```

No `enforce_tool_confirmation` key - so it takes the dataclass default of
`True`. Not disabled; never explicitly set. **And `mode = "warn"` - the
unexplained setting parked for weeks - sits in the same block.**

**THE QUESTION, AND IT IS NOT YET ANSWERED: is
`enforce_tool_confirmation` WIRED TO ANYTHING?** The grep found it in
`config.py` only - a definition and a config writer, **no consumer anywhere in
`src\openjarvis\`.**

**Why this decides the reading of the whole window:**

- **If it has no consumer:** the documented gate is a config field with no
  implementation behind it. Defect 6, 6c, 6d, 6e and
  `openjarvis-confirm-live-v1` were **not redundant - they were necessary.** We
  built what was documented but absent.
- **If it has a consumer:** fifteen-plus windows went into rebuilding a
  documented flag. That is the harder answer and it must be faced squarely.

**DO NOT let the 550B's Q5 closing line - "the developer likely rebuilt the
entire stack" - stand as a finding.** That is the model CONCLUDING, not citing.
It does not know what Yahoo IMAP requires that GDrive OAuth cannot do, and "a
documented flag exists" is not "that flag works." **This entire window is a
demonstration that documented intent and implemented behavior diverge in this
codebase.** Same failure shape as its Q4 in sections 3.3 and 12.4 - third
instance. **The cited parts of both replies are solid; every concluding sentence
is a hypothesis.**

### 15.6 REVISED NEXT ACTIONS - SUPERSEDES 14.8

**The ordering has changed. Documentation-first now precedes defect work.**

1. **ANSWER 15.5.** One grep for consumers of `enforce_tool_confirmation`
   outside `config.py`, plus a read of `docs\architecture\security.md`
   (8,348 bytes, never read). Decides whether fifteen windows of gate work
   were necessary or duplicative. **Cheapest high-stakes question on the list.**

2. **READ `docs\architecture\agents.md` DIRECTLY** (22,888 bytes). Not via the
   550B - directly. It is the author's account of the agent the whole project
   runs on, and it has never been read in any window.

3. **READ `docs\architecture\memory.md` and `docs\memory_db_schema.md`**, then
   evaluate `monitor_operative` against Gray's persistent-recall requirement
   (15.3). **This is the highest-value item for the PROGRAM GOAL**, as opposed
   to the defect backlog.

4. **LOCATE GRAY'S ORIGINAL INITIAL REQUIREMENTS** (15.2). Without that document
   there is no progress denominator. Upstream cannot supply one.

5. **CLOSE T-B.** Still provable from source, still cheap. Carried from 14.8.

6. **READ `estimate_prompt_tokens`.** Carried from 14.8 item 2.

7. **Fix the three `print()` calls to `logger.info()`** at
   `serve.py:268/:280/:281`. Carried from 14.8 item 3.

8. **Build the divergence chapter** (14.6), now with upstream's documented
   baseline available to diverge FROM. Add: `native_openhands` absent from the
   config reference (15.4A), `max_turns` 15 versus documented 3 (15.4B), the two
   non-meeting prompt-override mechanisms (15.4E).

9. Carry section 10 items 8-16 and 14.8 items 4, 6, 7 unchanged.

### 15.7 SDP ADDITIONS

- **The capability inventory in 15.3 is SDP content.** It is upstream's own
  statement of what the system provides, and it is the closest thing to a
  requirements baseline that exists outside Gray's head.
- **The divergence chapter (14.6) now has its other half.** Every divergence can
  be stated as "author documents X at `<file>:<section>`; Graystone does Y
  because Z." Ten divergences listed; three more added at 15.4.
- **New method rule, and it belongs at the top of the method chapter:
  READ THE PROJECT'S OWN DOCUMENTATION BEFORE DERIVING ANYTHING FROM SOURCE.**
  Three instances in one window of building what already existed (15.0).
- **`docs\assets\OpenJarvis_Architecture.png` exists.** Reconcile it against the
  SDP's hand-built architecture artifacts before producing more of them.
- **Record the 550B's failure mode as a standing caution:** cited answers and
  concluded answers arrive in the same reply, in the same register. Three
  instances now (3.3, 12.4, 15.5). **Trust the citations; treat every conclusion
  as a hypothesis.** Also: keep bundles scoped to files bearing on ONE question -
  accuracy degrades on large one-shot uploads, observed by Gray and consistent
  with all three failures.

### 15.8 WINDOW CLOSE

41 interactions. **No code was modified at any point.** `411cd59` remains HEAD
on both remotes, verified at the start.

**Three carried assumptions died:** the `ollama.py:126` mask (never was one),
the exemplar context tax (dormant, not active), and the estimator's
trustworthiness. **One survived verification:** twelve tools, counted from
config. **One of my own sections was wrong and was corrected in place** (2.4).

**The window's summary judgement stands from 14.7: EVERYTHING ABOUT STRUCTURE IS
VERIFIED, EVERYTHING ABOUT MAGNITUDE IS ASSUMED** - and to it add:
**EVERYTHING WE BUILT, WE BUILT WITHOUT READING WHAT THE AUTHOR ALREADY WROTE.**

New untracked files in the repo root from this window:
`probe_telemetry_truncation.py`, `probe_telemetry_ceiling.py`,
`CLOUDBUNDLE-adhoc-20260906-104107.md` (superseded),
`CLOUDBUNDLE-adhoc-20260906-104229.md` (unsent),
`CLOUDBUNDLE-adhoc-20260906-123255.md`,
`CLOUDBUNDLE-adhoc-20260906-140132.md`,
`CLOUDBUNDLE-adhoc-20260906-140458.md`, and this handoff.
