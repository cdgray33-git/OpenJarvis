# HANDOFF 2026-09-03 K / W33 - THE CEILING PROBE RAN. BOTH ITS VERDICTS WERE WRONG. THE REAL FINDING IS A STOCHASTIC DECODER.

Predecessor: HANDOFF-2026-09-03-J-W32-CEILING-HYPOTHESIS.md
All evidence in this window is dated 09/03 and was produced live in-window.

---

## 0. READ THIS FIRST - WHAT THIS WINDOW ACTUALLY DID

Two probes were run and one was built. Every headline verdict either probe
printed about itself was WRONG, and in both cases the error was caught by
reading the matrix rather than the READING block underneath it.

**The single most important carry-forward: a probe's self-verdict is a
convenience, not evidence. Read the columns.** Both scripts in this window
printed a confident conclusion that the numbers directly above it contradicted.

Window cost: one deliverable built (`probe_ctx_ceiling_v2.py`), two probe runs,
four cheap greps. Handoff requested at exchange 8. The v3 rate experiment was
SPECIFIED BUT DELIBERATELY NOT BUILT, per the one-deliverable rule.

---

## 1. WHAT WAS RUN

### 1.1 `probe_ctx_ceiling_v1.py` - built in W32, EXECUTED HERE for the first time
Staged from Downloads and verified by marker content, not by filename.
Output teed to `tests\ctx_ceiling_run_20260903.txt`.

HOST `http://172.16.33.200:11434`, MODEL `qwen3-coder:30b`, confirmed on the
HOST line before the run was trusted.

Shape: FOUR messages always - system, one oversized user message carrying all
the filler, an assistant stub, then the ask (lines 140-150). Sweeps payload
SIZE at a fixed message count.

```
 num_ctx   size    payloadB   prompt_eval   ntc
    8192    1000       7583         1335     1
    8192    4000      26195         3949     1
    8192    7000      45567         6613     1
    8192    9000      57952          420     1
    8192   12000      77089          420     1
    8192   16000     102298          420     1
   32768    1000       7363         1284     1
   32768    4000      26524         3990     1
   32768    7000      45352         6572     1
   32768    9000      57840         8360     0
   32768   12000      76794        10868     0
   32768   16000     101998        14469     0
```
Failing cells carried `<function=mailbox_find_messages> <parameter=...` in
CONTENT (truncated by the instrument at about 110 chars).

### 1.2 `probe_ctx_ceiling_v2.py` - built and run in this window
Marker `openjarvis-ctx-ceiling-v2`, in `tests\`, output teed to
`tests\ctx_ceiling_v2_run_20260903.txt`. Stdlib only, no `requests` dependency.

Shape: holds the token budget CONSTANT at 12000 and sweeps the number of
messages it is split across - the only shape in which a leading SYSTEM message
can be evicted. Host and model hardcoded from v1's verified output rather than
re-derived from config.

```
 num_ctx  pairs  nmsgs   payloadB  prompt_eval   ntc  verdict
    8192    ctl      4       8181         1876     1  TOOLCALL
   32768    ctl      4       8181         1878     1  TOOLCALL
    8192      1      4     109368          407     1  TOOLCALL
    8192      4     10     109189         6115     1  TOOLCALL
    8192     16     34     109653         7384     1  TOOLCALL
    8192     32     66     111255         8181     0  PROSE
   32768      1      4     109372        23647     1  TOOLCALL
   32768      4     10     109197        23224     1  TOOLCALL
   32768     16     34     109653        22700     1  TOOLCALL
   32768     32     66     112372        24108     1  TOOLCALL
```

---

## 2. WHAT IS PROVEN, AND WHAT IS RETIRED

### 2.1 PROVEN - TRUNCATION AT 8192 IS REAL
v1 pinned `prompt_eval_count` at **420, 420, 420** across payloads of 58KB,
77KB and 102KB, with latency collapsing from 10.6s to about 1.7s. v2
independently pinned at **407** on the same shape. Three payloads differing by
44KB cannot produce an identical evaluated count by cache scatter. This is the
PINNING discriminator W32 specified, and it fired.

Mechanism, now understood: Ollama discarded the single oversized user message
whole and kept SYSTEM plus the assistant stub plus the ask, which is about 410
to 420 tokens. **The tool contract survived because it was never in the message
that got cut.**

### 2.2 PROVEN - THE TOOL CONTRACT SURVIVES MESSAGE-COUNT PRESSURE
v2 at 8192 held `ntc=1` through 34 messages and 7384 evaluated tokens.
Front-eviction of the SYSTEM message did NOT occur at any count tested up to
the point of window saturation.

### 2.3 RETIRED - "qwen3-coder switches to `<function=` format above 8000 tokens"
This was v1's finding and it looked strong. It does not survive.

**v1 ran at `temperature 0.7` with NO seed** (`probe_ctx_ceiling_v1.py:158`).
Its three 32768 failures are three unrepeated draws from a stochastic decoder,
not a demonstrated boundary. v2 at `temperature 0` emitted clean native tool
calls at 22700, 23224, 23647 and 24108 evaluated tokens - far past where v1
failed. **Do not carry the format-switch boundary into the SDD.**

Worth keeping from it anyway: when the model DOES emit that form, it is calling
the tool in the wrong channel, not refusing. `_extract_tool_call` Format 4
(native_openhands.py:216-240) already parses that exact syntax and its code
comment names qwen3-coder specifically. So `ntc=0` in a probe does NOT imply
`dispatched=0` in production. The probes measure the engine only.

### 2.4 RETIRED - v2's OWN "OUTCOME A, front-eviction is dead"
Also wrong, and the defect is in code written this window.

The decisive cell, `8192 pairs=32`, returned `ntc=0` with **completely empty
content**. `classify()` falls through to `PROSE` on empty content, and the
verdict block read the absence of a `NOTOOLS` cell as proof the system message
survived. **An empty generation is uninformative, not exculpatory.** That cell
established nothing either way.

### 2.5 THE ONE NUMBER WORTH KEEPING FROM THAT CELL
At 8192, tool emission held at `prompt_eval` **7384** and died at **8181**
against a declared window of **8192**. Failure is at SATURATION of the window,
not at a message count. Payload was about 109KB in all four 8192 sweep cells,
so bytes were controlled; only how much survived truncation varied.

### 2.6 THE CONFOUND THAT INVALIDATES CROSS-PROBE COMPARISON
v1 and v2 differ in **TWO** variables - sampling temperature AND message shape.
Neither can attribute its own result against the other. Any v3 changes one
variable at a time.

---

## 3. **THE ACTUAL NEW FINDING - PRODUCTION DECODES STOCHASTICALLY**

Read directly from source this window:

```
ollama.py:54   temperature: float = 0.7,     (generate)
ollama.py:183  temperature: float = 0.7,
ollama.py:243  temperature: float = 0.7,     (streaming)
ollama.py:73-75 / 191-193 / 270-272   "options": {temperature, num_predict}
```
`config.toml` has `[engine]` at :1 and `[agent]` at :12 and **no temperature key
anywhere**, exactly as it has no num_ctx key. **Production runs temperature 0.7,
unseeded, at all three sites.**

Consequences, and this reframes the whole investigation:

1. **v1 accidentally matched production sampling. v2 did not.** v2's clean sweep
   is the unrepresentative run, not the corrective one. This is the opposite of
   how it was read in-window at first.
2. **A stochastic decoder explains the reproduction history directly.** Defect 1
   failed two deliberate reproduction attempts in August while firing
   spontaneously. A probabilistic failure has no on-demand trigger - only a
   RATE. Every experiment run against it so far has been one coin flip per cell.
3. **Every single-sample probe result in the record is weaker than it looked**,
   including healthy ones. A cell that emitted a tool call once is not proof the
   configuration is safe.

**This does not clear truncation.** Production runs at 8192 and conversation
history only grows. Once a conversation crosses saturation it stays across it,
which matches the 09/02 hard boundary exactly: healthy through 12:24:52, then
every run after it failing identically and never recovering. Truncation
plausibly sets the failure RATE and sampling decides which turns fall over.
Both mechanisms are live; neither is proven causal.

---

## 4. NEXT ACTION - `probe_ctx_ceiling_v3.py`, SPECIFIED, NOT BUILT

A RATE experiment, not another sweep. Deliberately handed off rather than built
in this window.

SPEC:
- Production sampling exactly: `temperature 0.7`, no seed, `num_ctx 8192`,
  `num_predict 1024`. Do not "improve" these.
- Two prompt sizes only: one BELOW saturation (target `prompt_eval` near 7000)
  and one ABOVE (target near 8200). v2's pairs=16 and pairs=32 cells hit those
  marks and can be reused as-is.
- **N=20 repeats per size.** The output is a failure RATE per size, with a
  binomial confidence interval, not a verdict.
- Distinct filler per repeat so nothing is cache-served.
- Classify EVERY generation by content: TOOLCALL / WRONGCHANNEL (`<function=`
  present) / NOTOOLS (claims no access) / EMPTY / PROSE.

TWO INSTRUMENT DEFECTS TO FIX IN IT, both found the hard way this window:
1. **Empty content must classify as UNINFORMATIVE**, never PROSE, and must be
   excluded from any verdict rather than counted as a non-failure.
2. **Capture full content, not a 110-char or 400-char prefix.** v1 could not
   distinguish "tools gone" from "tools present, wrong channel" because it cut
   the string before the discriminator.

READ SHAPE:
- Rate materially higher above saturation than below -> truncation drives the
  rate. The fix is config-shaped: thread `num_ctx` to the agent path.
- Similar non-zero rate at both sizes -> the defect is sampling, not context.
  A different fix entirely - constrained decoding, a seed, or a retry on `ntc=0`.
- Zero failures in 40 generations -> the probe shape does not reach the defect
  and the search moves back to the live agent path.

---

## 5. ROLLBACK POINTS - NO NEW ONES THIS WINDOW

No source file was patched in W33. Everything built was a standalone probe in
`tests\`. Existing rollbacks unchanged:
- Patch 4 (RAWGEN): `Copy-Item 'src\openjarvis\agents\native_openhands.py.bak_rawgen_20260818_145629' 'src\openjarvis\agents\native_openhands.py' -Force` then RESTART backend
- Patch 5 (RETRY400): `Copy-Item 'src\openjarvis\engine\ollama.py.bak_retry400_20260818_160710' 'src\openjarvis\engine\ollama.py' -Force` then RESTART backend

Both remain temporary diagnostics and come out once Defect 1 is fixed.

---

## 6. EXECUTION PATHS REGISTER

No new path mapped this window. Carried forward unchanged:

**Path 1 - orchestrator `ask()`** via `system\orchestrator.py`.
**Path 2 - managed-agent SSE stream** via `_stream_managed_agent()` in
`server\agent_manager_routes.py`.
**Paths 1a/1b/1c/1d** - the `routes.py` chat dispatch branches.
**Path 3 - CONNECTOR-DIRECT** (W32): no ToolExecutor, no confirmation gate, no
protected-sender guard, no event bus traffic, human present by construction.
Still the proven route for destructive mailbox work and still the layer beneath
every guard in the system.

NEW DETAIL FOR PATHS 1 AND 2, from this window's source read: every generation
on both paths goes through `ollama.py` at `temperature 0.7` unseeded with
`num_ctx 8192`, none of which is configurable from `config.toml`. Record this in
the register as a property of the engine leg shared by all agent paths.

---

## 7. SYSTEM DESIGN PACKAGE (SDP / SDD) - WHAT THIS WINDOW OWES IT

### 7.1 CORRECTION REQUIRED - W32 section 7.1 IS WRONG AS WRITTEN
W32 gave a plain-language story for the truncation hazard: "the pages at the TOP
fall out of their hands first, and those were the pages with the tools on them."

**Measurement contradicts it.** The tool descriptions sit in the SYSTEM message
and the SYSTEM message SURVIVED every truncation observed - at 8192, across
payloads up to 111KB and message counts up to 66. What was discarded was the
middle of the conversation. Do not ship the W32 wording.

CORRECTED PLAIN-LANGUAGE VERSION (per the 09/02 pinned rule):

> Imagine you hand someone a folder for a job. The first page lists the tools
> they are allowed to use. Behind it are all the notes from everything you have
> discussed so far, and the last page is what you want done right now.
>
> The folder has a limit. When you keep adding notes, the folder does not throw
> away the first page and it does not throw away the last page - it squeezes out
> the notes in the MIDDLE.
>
> So the person still knows what tools they have, and still knows what you asked
> for. What they lose is the memory of how you got here. They start answering
> without the context, and the longer you talk, the more of the middle is gone.
>
> And there is a second thing. This person does not decide the same way every
> time - there is a bit of a dice roll in how they answer. Most of the time they
> pick up the tool. Sometimes they just describe the job instead. When the folder
> is full and the dice roll goes badly on the same turn, you get an answer that
> sounds finished and nothing actually happened.

That second paragraph is the new hazard class and it belongs in the guard
chapter: **a component whose failure is probabilistic rather than deterministic
cannot be cleared by a passing test.** Same family as the silent tools-drop
retry and the silent truncation - it degrades without an error surface - but
worse to verify, because a single successful run proves nothing.

### 7.2 METHOD LESSON, the important one from this window
Two probes printed confident self-verdicts. **Both were wrong, and in both cases
the raw matrix directly above the verdict contained the contradiction.** v1
concluded "hypothesis wounded" while its own prompt_eval column showed the
pinning that confirmed truncation. v2 concluded "front-eviction is dead" on the
strength of a cell that returned empty output.

For the SDD: any automated instrument that emits a conclusion must also emit the
evidence the conclusion was drawn from, positioned so the reader sees the
evidence first. And **an instrument's verdict logic is code, and code written in
the same window as the experiment has not been reviewed by anything.**

### 7.3 Configuration hazard for the config chapter
`ollama.py` hardcodes defaults for BOTH `num_ctx` (8192) and `temperature`
(0.7) at three sites each, and `config.toml` can override NEITHER. Two
behavior-critical parameters are unreachable from configuration. Document them
together - the same fix threads both.

### 7.4 Unchanged and still owed
- Defect 6 confirmation gate: registry, payload, transport, threading model, in
  GREAT DETAIL. Not touched this window.
- The connector-direct path (W32 section 7.3) needs its own SDP entry.
- Prompt assembly and truncation diagram, with declared `num_ctx` marked at each
  gate, as a downloadable standalone file for the wiki.

---

## 8. THE 550B CLOUD MODEL - CARRIED FORWARD

Standing rule: when a question needs whole files rather than targeted reads,
bundle the suspected files into one markdown file for the 550B cloud model
(openrouter nemotron-3-ultra-550b) instead of spending window cycles on
piecemeal reads. Note the 08/18 caveat - the free tier truncated one run and
echoed another; split into feeds of 2-3 questions.

**Bundle is still worth sending, and the question has CHANGED:**
- `src\openjarvis\engine\ollama.py` (whole - three num_ctx sites, three
  temperature sites, the mask at :126)
- `src\openjarvis\agents\_stubs.py` (`_build_messages` :124-162, `_generate`
  :164-199)
- `src\openjarvis\agents\native_openhands.py` (prompt build :324-374, and
  `_extract_tool_call` :161-250 including Format 4 at :216-240)
- `src\openjarvis\research_loop.py` (the 16384 workaround)
- `C:\Users\Admin\.openjarvis\config.toml`

Questions, split into two feeds:
- FEED 1: cleanest way to thread configured `num_ctx` AND `temperature` from
  config.toml to all three ollama.py sites without changing behavior for callers
  that already pass them.
- FEED 2: when `raw_tool_calls` is empty, is `_extract_tool_call` actually
  reached on the live path, and would Format 4 dispatch a `<function=...>` block
  found in content? This decides whether the wrong-channel emission is a real
  production failure or one the parser already absorbs.

---

## 9. STANDING RULES - ONE ADDED THIS WINDOW

- **NEW: probes must mirror PRODUCTION sampling** (`temperature 0.7`, unseeded,
  `num_ctx 8192`) unless the experiment is specifically about sampling. A probe
  at temperature 0 is measuring a system Gray does not run.
- **NEW: read the matrix, not the verdict.** Applies to every instrument in
  `tests\`, including ones written earlier in the same session.
- Verify against the mailbox, never against the transcript.
- Connector-level `find_messages` returns a PLAIN LIST. Assert
  `isinstance(r, list)`.
- Size key on connector rows is `bytes`.
- Re-census before sizing any destructive test.
- Trash counts against the Yahoo quota until emptied.
- Every download lands in `C:\Users\Admin\Downloads\`. Verify by MARKER CONTENT
  before running, never by filename.
- Push to BOTH remotes - `origin` (GitHub) and `gitlab` (lab instance).

---

## 10. UNCOMMITTED WORK

Nothing has been committed since W32. Currently untracked in `tests\`:
- `probe_bulk_census_v1.py`
- `probe_folder_census_v1.py`
- `probe_inbox_cleanup_v1.py`
- `probe_ctx_ceiling_v1.py`
- `probe_ctx_ceiling_v2.py`
- `ctx_ceiling_run_20260903.txt`
- `ctx_ceiling_v2_run_20260903.txt`

Seven files. The two run logs are primary evidence for the SDD and should be
committed with the probes, not regenerated.

---

## 11. ORDERED NEXT ACTIONS

1. **Build and run `probe_ctx_ceiling_v3.py`** to section 4's spec. Production
   sampling, two sizes, N=20, rate not verdict, both instrument defects fixed.
2. Depending on the rate result: either thread configured `num_ctx` and
   `temperature` to the agent path (verify in isolation, stack nothing on it),
   or move to the sampling-side fix.
3. Send the 550B bundle, FEED 2 first - if Format 4 already absorbs the
   wrong-channel emission in production, that closes a whole branch cheaply.
4. Commit the seven `tests\` files to BOTH remotes.
5. Ask Gray for the true Yahoo Inbox message count from the web UI. Two seconds
   on his side, still unanswered from W32. `usage_report` said 12,807 / 859 MB;
   an August web-UI reading said 286K. They cannot both be true.
6. Defect 6 / 6e - the confirm gate client listener, still unbuilt.
7. Condense `[[openjarvis-rollback-points]]`, at its size cap.
8. The `/v1/sessions` patch - fully spec'd, still untouched.
9. `memdb_audit.log` under the 30 MB scheme.

---

## 12. PARKED - DO NOT CHASE MID-TASK

- Two backend python processes have appeared repeatedly (08/17, 08/18). A stale
  listener confuses port-based diagnostics.
- `conv=-` on RUNSTART - the agent still receives no conversation identity.
- Format 1 of `_extract_tool_call` is case-insensitive and unanchored, so prose
  containing "action:" can produce a false-positive tool name.
- `to_openai_function()` passes `parameters` through raw from `ToolSpec`, whose
  default is `{}`. Audit across the 12 tools.
- The confirm flow asks TWICE. UX defect, not Defect 1.
- Tool panel args render with cp437 mojibake in the desktop app.
- The 0 ms `account: yahoo` tool call preceding the real `account: yahoo_main`
  call.
- `ollama.py` lines 46 and 122-123 already contain mojibake. Any patch to that
  file must read and write with explicit encoding or it corrupts further.
- The masked field at `ollama.py:126` - `prompt_tokens = max(reported_prompt,
  estimated_prompt)` still discards the one field that shows truncation. Both
  probes read `prompt_eval_count` straight from Ollama and bypassed the mask
  entirely, so this is not blocking, but production telemetry is still lying
  about input size.
