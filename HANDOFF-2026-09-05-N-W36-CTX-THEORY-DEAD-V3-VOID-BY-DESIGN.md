# HANDOFF 2026-09-05 N / W36 - THE COMMIT SHIPPED TO BOTH REMOTES. probe_ctx_ceiling_v3 WAS BUILT, RUN, AND VOIDED BY ITS OWN GATE - AND THAT VOID IS THE MOST USEFUL RESULT OF THE WINDOW. THE TRUNCATION THEORY OF DEFECT 1 IS DEAD, STRUCTURALLY AND EMPIRICALLY.

Predecessor: HANDOFF-2026-09-05-M-W35-NUMCTX-VERIFIED-LIVE.md
All evidence in this window is dated 09/05 and was produced live in-window.

---

## 0. READ THIS FIRST - WHERE THE SYSTEM ACTUALLY SITS

W35's next-action 1 is CLOSED. Commit `c37d8b1` (9 files) is on GitHub and on
GitLab, both from parent `fce0b78`.

W35's next-action 2 is BUILT AND RUN. `tests\probe_ctx_ceiling_v3.py` executed
40 generations at production sampling and **voided itself on gate G4: zero
failures in arm A.** The rate question it was built to answer is unanswered.

That is not a wasted window. The void, plus a structural fact found while
reading the result, **kills the truncation/eviction theory of Defect 1.** The
search moves to the live agent path.

**The backend has NOT been restarted this window and no source file was
modified.** `ollama.py` is as committed. Config is as W35 left it (BOM stripped,
`num_ctx = 16384`).

**ONE COMMAND WAS ISSUED BUT ITS OUTPUT WAS NEVER SEEN** - see section 8. Verify
it before building on it.

---

## 1. WHAT WAS DONE, IN ORDER

### 1.1 The commit - and a silent exclusion caught before it shipped

W35 section 12 listed nine files. Before staging, the two run logs were checked
rather than assumed. Both existed on disk, and:

```
.gitignore:23:*.txt     "tests\ctx_ceiling_run_20260903.txt"
.gitignore:23:*.txt     "tests\ctx_ceiling_v2_run_20260903.txt"
```

**A blanket `*.txt` rule was silently excluding both.** They are primary,
non-regenerable SDD evidence. Without the check the commit would have shipped
seven files, reported success, and lost them - with no error anywhere.

Same failure shape as W35's BOM: a SILENT exclusion, not a loud one. Staged with
`git add -f`. `.gitignore` itself was deliberately NOT edited - a negation rule
is its own change and gets its own verification round.

Staged set verified as exactly 9 (8 `A`, 1 `M`) before committing.

### 1.2 Commit and dual push - VERIFIED

```
[main c37d8b1] 9 files changed, 1379 insertions(+), 3 deletions(-)
fce0b78..c37d8b1  main -> main   https://github.com/cdgray33-git/OpenJarvis.git
fce0b78..c37d8b1  main -> main   http://172.16.33.126/root/openjarvis-desktop.git
```

Both remotes at the same SHA from the same parent. Commit message tags the
Patch 4 / Patch 5 diagnostics as temporary, per W35's decision.

### 1.3 v3 was specified against a STALE spec - caught before building

W33 section 4 says "production sampling exactly: temperature 0.7, no seed,
**num_ctx 8192**, num_predict 1024. Do not improve these."

**That line was true on 09/03 and false on 09/05.** Production is 16384 as of
W34/W35. W33's two prompt sizes (7000 / 8200) were also chosen as below/above
saturation *relative to 8192*.

Building to the letter would have measured the retired regime and left the arm
we actually ship in unmeasured. Gray chose the alternative design.

**Standing lesson: a spec inherited across windows can be invalidated by the
very fix the intervening window shipped. Re-read a carried-forward spec against
current state before building it.**

### 1.4 v3 built as a paired experiment

- ARM A `num_ctx 8192` - prompt does not fit, truncates
- ARM B `num_ctx 16384` - prompt fits
- **PAIRED:** repeat *i* in both arms is a BYTE-IDENTICAL prompt. Only the
  window varies. Filler still varies between repeats so nothing is cache-served.
- N=20 per arm, temperature 0.7, no seed, num_predict 1024
- Four validity gates that VOID the run rather than report something soft
- Both W33 instrument defects fixed (empty -> UNINFORMATIVE and excluded;
  FULL content to the log, never a prefix)

**Known confound, not designed out and stated in the file:** arms run as blocks,
not interleaved, because changing `num_ctx` forces a full 20 GB reload. Time
order is confounded with arm. Interleaving would cost 40 reloads.

419 lines, AST-verified, **zero non-ASCII bytes** (per the `ollama.py` mojibake
rule). Verified in place by MARKER CONTENT at four distinct lines, not filename.

---

## 2. THE RESULT - VOID BY GATE G4

```
 arm  num_ctx   runs   unin  fails  pev_med  breakdown
   A     8192     20      0      0     6818  TOOLCALL=20
   B    16384     20      0      0    14822  TOOLCALL=20

G1 passed - both controls emitted a tool call.
G2 passed - arm A peval 6818, arm B peval 14822. Arms differ.
G3 passed - uninformative counts within tolerance (A=0, B=0).
G4 FAILED - arm A produced ZERO failures in 20 informative runs.
```

**G4 is the gate that protects us from the answer we wanted.** Gray came into
this window believing context was fixed. Arm B was clean - but it was clean from
a clean baseline, so it proves nothing. The instrument said so and refused to
report a rate. Build the next one the same way.

### 2.1 What the run DID establish

**Arm A discarded more than half the prompt and the tool contract survived
anyway.** Byte-identical prompts evaluated to 6,818 tokens at `num_ctx 8192`
versus 14,822 at 16384 - roughly 8,000 tokens dropped - and every one of the 20
truncated generations still emitted a correct native tool call.

Truncation is real and measurable. **It does not remove the tool contract.**
This confirms v2's OUTCOME A at N=20 instead of a single cell.

Note also that truncation drops WHOLE MESSAGES: 8192 landed at 6,818, well under
the limit, not at it.

### 2.2 THE STRUCTURAL FINDING - WHY IT COULD NEVER HAVE FAILED

**The probe passes tools in the `tools` PARAMETER, outside the `messages`
array.** Message truncation cannot touch them, at any window size, ever.

Front-eviction of the tool contract was **not testable in this probe shape.**
v1, v2 and v3 all share it. The theory was never being tested by any of them.

**THE HINGE, AND THE NEXT ACTION:** this only kills the theory for PRODUCTION if
production does the same thing. If `native_openhands` instead embeds the 12 tool
descriptions as TEXT inside the SYSTEM message, that text IS truncatable and the
exposure is real - and no probe we have written has ever modeled it.

Read `native_openhands.py:324-374` (prompt build) and answer: are tool schemas
passed as an API parameter, or rendered into prompt text?

### 2.3 The probe task is too easy - the other reason to distrust it

`evc=49` on **all 40 generations**, at temperature 0.7 unseeded. Identical
output length every time. Sampling variance is effectively nil, which means the
task is deterministic: one tool, one unambiguous ask, a hand-written 5-line
SYSTEM.

Production carries 12 tools and roughly 3,980 tokens of overhead. **Defect 1
lives in that gap.** The next instrument must use the REAL system prompt and ALL
12 tool schemas, or it will keep passing.

---

## 3. NEGATIVE RESULTS AND CORRECTIONS

Per the 08/24 pinned rule, what a thing turned out NOT to be is knowledge.

- **THE 7-MINUTE STALL WAS NOT A STALL, AND MY VRAM-SPILL HYPOTHESIS WAS WRONG.**
  Mid-run, arm B appeared frozen at rep 6 for 7+ minutes. I hypothesized KV cache
  spilling to host memory - W35 measured only ~3.7 GB headroom, and a
  14.8k-token cache is far larger than the trivial prompt W35 tested with.
  **REFUTED by two independent facts:** `/api/ps` mid-run reported
  `size_vram` 20,280,883,328 = `size` exactly, fully resident, no spill; and the
  probe's own timer recorded rep 6 at 37.8s, in line with its neighbors.
  **There was no slowdown to explain.** Do not re-raise VRAM spill without new
  evidence.
- **CAUSE OF THE APPARENT FREEZE: the PowerShell console, not the process.**
  Gray selected text in the window to screenshot it. QuickEdit mode blocks the
  writing process at its next `print` until Esc/Enter. The HTTP call had already
  returned; the process sat blocked on stdout. **This directly threatens the
  non-interactive test rule - an unattended long run can be frozen indefinitely
  by a stray click.** See section 6.
- **TRUNCATION DOES NOT EVICT THE TOOL CONTRACT** - 20/20 at 8192 with ~8,000
  tokens discarded. Empirically confirmed and structurally explained (2.2).
- **num_ctx 16384 DID NOT CHANGE THE OUTCOME** on this shape - 20/20 both arms.
  The patch remains correct on its own merits (the ~3,980-token overhead figure
  justifies it) but **it does not close Defect 1.**
- **The two ctx_ceiling run logs were NOT already tracked.** They were being
  silently swallowed by `.gitignore:23`.

---

## 4. SDP / SDD FEED FROM THIS WINDOW

### 4.1 Architectural item - WHERE DOES THE TOOL CONTRACT LIVE?

The SDP needs a definitive statement, per execution path, of whether tool
definitions travel as an API parameter or as prompt text. These have completely
different truncation exposure and the difference is invisible in logs. Record it
per path in the register.

### 4.2 Method note - AN INSTRUMENT MUST BE ABLE TO SAY NO

v3's value came entirely from a gate that refused to report. Design gates that
void the run BEFORE seeing the data, and state them in the file. If the
instrument cannot fail in a way that contradicts the hypothesis, it is
decoration.

Corollary found the hard way: **check what your probe structurally CANNOT test.**
v1, v2 and v3 all passed tools outside `messages`, so none of them could ever
have reproduced front-eviction. Three windows of probes shared one blind spot.

### 4.3 Plain language - the eight-year-old test

> We thought Jarvis was forgetting his tools because his notebook got too full
> and the first page fell out. So we filled the notebook past bursting, twice,
> twenty times each way, and watched.
>
> He never once forgot his tools. And then we noticed why: **his tools were
> never written in the notebook at all.** They were on a card he holds in his
> other hand. It does not matter how full the notebook gets - the card is still
> in his hand.
>
> So we were looking in the wrong place, and we can stop looking there. But
> there is one thing left to check. We tested a pretend Jarvis who holds a card.
> We have not checked whether the REAL Jarvis holds a card, or whether somebody
> wrote his tools onto the first page of the notebook after all.

### 4.4 Still owed, unchanged

- Defect 6 confirmation gate: registry, payload, transport, threading model, in
  GREAT DETAIL, plain-language alongside technical. Not touched this window.
- The connector-direct path (W32 section 7.3) needs its own SDP entry.
- Prompt assembly and truncation diagram, `num_ctx` marked at each gate, ports /
  protocols / encoding, delivered as a downloadable standalone file for the wiki.
  **Now also needs to mark WHERE TOOL DEFINITIONS ENTER on each path.**

---

## 5. EXECUTION PATHS REGISTER

Standing structure per path: entry point, call chain with file:line, which
ToolExecutor instance serves it and how it is constructed, whether the
confirmation gate is live / auto-approved / absent, event bus traffic, human
presence.

### 5.1 PROBE PATH - direct to Ollama, BYPASSES ALL OPENJARVIS CODE

Recorded because three windows of conclusions rest on it and its limits are now
known.

- **Entry point:** `POST http://172.16.33.200:11434/api/chat` from
  `tests\probe_ctx_ceiling_v*.py` on the Windows box.
- **Call chain:** `urllib.request` -> Ollama HTTP. No OpenJarvis module loaded.
- **Tool contract:** top-level `tools` parameter, OUTSIDE `messages`.
  **Structurally immune to message truncation.**
- **ToolExecutor:** none. No dispatch, no execution - emission is observed, never
  execution.
- **Confirmation gate:** absent.
- **Event bus:** none.
- **Human present:** launches it, then unattended.
- **LIMIT, PINNED:** this path cannot reproduce any defect that depends on our
  prompt assembly, our tool rendering, our parser, or our dispatch. A clean
  result here says the MODEL behaves. It says nothing about production.

### 5.2 Previously identified, unchanged

- Startup / config load (W35 section 8.1)
- `POST /v1/chat/completions` non-streaming (W35 section 8.2)
- Orchestrator `ask()` via `system\orchestrator.py`
- Managed-agent SSE via `_stream_managed_agent()` in `server\agent_manager_routes.py`
- routes.py chat dispatch branches 1a/1b/1c/1d

---

## 6. STANDING RULES - THREE ADDED THIS WINDOW

- **NEW: check what your probe structurally CANNOT test, before trusting a clean
  result.** Ask which mechanism the instrument is physically incapable of
  exercising. v1/v2/v3 could never have shown front-eviction.
- **NEW: a spec carried across windows can be invalidated by the fix the
  intervening window shipped.** Re-read it against current state before building.
  W33's "production sampling = num_ctx 8192" was stale within 48 hours.
- **NEW: QUICKEDIT WILL FREEZE AN UNATTENDED RUN.** Clicking or selecting text in
  a PowerShell window blocks the writing process at its next `print` until
  Esc/Enter. **Redirect long runs to a file instead of watching them:**
  `python .\tests\probe_x.py *> tests\run.log`. This is now part of the
  non-interactive test rule, not a footnote.
- `.gitignore:23` is a blanket `*.txt`. **Every run log needs `git add -f`.**
- When you fix a parser, count the readers.
- A defect that can only surface on restart is its own hazard class. Validate
  config/environment/startup changes with an ACTUAL restart in the same window.
- Any fallback-to-default path must log that it fell back.
- Every command must be valid on PowerShell 5.1. `Format-Hex -Count` is 6+.
- Probes must mirror PRODUCTION sampling (`temperature 0.7`, unseeded) unless the
  experiment is specifically about sampling.
- Read the matrix, not the verdict.
- Verify against the mailbox, never against the transcript.
- Connector-level `find_messages` returns a PLAIN LIST. Assert `isinstance(r, list)`.
- Size key on connector rows is `bytes`.
- Re-census before sizing any destructive test.
- Trash counts against the Yahoo quota until emptied.
- Every download lands in `C:\Users\Admin\Downloads\`. Verify by MARKER CONTENT
  before running, never by filename.
- `.\start-openjarvis.ps1` needs the `.\` prefix - a stale copy sits in
  `C:\Windows\System32`, which is on PATH.
- Backend log: `C:\Users\Admin\AppData\Local\OpenJarvis\logs\backend.log`
- Push to BOTH remotes - `origin` (GitHub) and `gitlab` (lab instance).

---

## 7. ROLLBACK POINTS

**No code was modified this window.** No new rollback point was created.

- `ollama.py` - chain unchanged, still three deep. See W34 section 7.1.
  Now also committed at `c37d8b1`, so `git` is a rollback path.
- `config.toml` - unchanged from W35:
  ```
  C:\Users\Admin\.openjarvis\config.toml.bak_bomstrip_20260905   (722 B, WITH BOM - DO NOT RESTORE, it breaks startup)
  C:\Users\Admin\.openjarvis\config.toml.bak_numctx_20260905     (702 B, pre-num_ctx - the REAL rollback)
  ```
- Cheap num_ctx rollback remains the CONFIG KEY, not the patch: set
  `[engine] num_ctx` to 8192 or delete the line, then restart.

---

## 8. UNCOMMITTED WORK - AND ONE UNVERIFIED COMMAND

**`c37d8b1` is pushed to both remotes - VERIFIED.**

**UNVERIFIED, ISSUED AT WINDOW END, OUTPUT NEVER SEEN.** A second commit was
issued covering:

- `tests\probe_ctx_ceiling_v3.py`
- `tests\ctx_ceiling_v3_run_20260905-123036.txt` (staged with `-f`)

with a push to both remotes. **VERIFY THIS FIRST NEXT WINDOW before assuming
either file is committed.** From `PS C:\Users\Admin\OpenJarvis>`:

```
git log --oneline -3; git status --short; git ls-files tests\ | Select-String 'v3'
```

If it did not land, re-issue it. The run log is primary evidence and is NOT
regenerable - and `.gitignore:23` will swallow it again without `-f`.

---

## 9. THE 550B CLOUD MODEL - CARRIED FORWARD

Standing rule: when a question needs whole files rather than targeted reads,
bundle the suspected files into one markdown file for the 550B cloud model
(openrouter nemotron-3-ultra-550b) instead of spending window cycles on
piecemeal reads. 08/18 caveat holds - the free tier truncated one run and echoed
another; split into feeds of 2-3 questions.

Bundle:

- `src\openjarvis\engine\ollama.py` (whole - carries the resolver)
- `src\openjarvis\agents\_stubs.py` (`_build_messages` :124-162, `_generate` :164-199)
- `src\openjarvis\agents\native_openhands.py` (prompt build :324-374, `_extract_tool_call` :161-250 incl. Format 4 at :216-240)
- `src\openjarvis\research_loop.py` (the 16384 workaround)
- `C:\Users\Admin\.openjarvis\config.toml`
- `src\openjarvis\engine\_discovery.py`
- `src\openjarvis\core\config.py`

**FEED 0 - NEW, NOW THE HIGHEST-VALUE QUESTION, SEND IT FIRST:** in
`native_openhands.py`, are the 12 tool definitions passed to the engine as a
top-level `tools` API parameter, or rendered as TEXT into the system prompt? If
text, at what token position, and is that text reachable by truncation at
`num_ctx 16384` given ~3,980 tokens of overhead? **This single answer either
revives the eviction theory for production or kills it for good.**

**FEED 2, STILL UNSENT AND STILL CHEAP:** when `raw_tool_calls` is empty, is
`_extract_tool_call` actually reached on the live path, and would Format 4
dispatch a `<function=...>` block found in content? If Format 4 absorbs it, a
whole branch closes for free.

**FEED 1:** should the num_ctx resolver move out of `ollama.py` into
`_make_engine` / `_HOST_MAP` in `_discovery.py`, and what is the cleanest shape
that also threads temperature the same way without changing behavior for callers
that already pass either?

**FEED 3:** `config.toml` has at least two independent readers with different
encoding tolerance and opposite failure behavior (`core\config.py:1740` aborts,
`_oj_num_ctx_from_config` silently defaults). What is the minimal change that
gives one owner of config parsing, tolerant of BOM and encoding variation,
without a large refactor and without changing startup's fail-loud behavior?

---

## 10. ORDERED NEXT ACTIONS

1. **Verify the section 8 commit landed.** One command, first thing.

2. **READ `native_openhands.py:324-374` AND ANSWER SECTION 2.2's HINGE
   QUESTION** - are tool schemas an API parameter or prompt text? This is the
   cheapest high-value read on the list and it determines whether truncation is
   dead for production or very much alive. Send FEED 0 in parallel.

3. **Then, depending on 2:**
   - *Tools as API parameter* -> truncation is dead for production. Defect 1 is
     sampling, parsing, or dispatch. Go to the LIVE AGENT PATH with the real
     system prompt and all 12 tools.
   - *Tools as prompt text* -> eviction is live and untested. Build v4 with the
     REAL system prompt and ALL 12 schemas rendered the way production renders
     them. Keep the paired design and the four gates.

4. **Either way, the next instrument needs the real prompt.** v3's `evc=49` on
   all 40 runs proves the toy task is deterministic and cannot reach the defect.

5. **Make `load_config()` BOM-tolerant** as its own isolated patch. Until then a
   machine-regenerated BOM'd `config.toml` takes the backend down on next start.

6. **Unmask `ollama.py:126`** - `prompt_tokens = max(reported, estimated)`
   discards the field that shows truncation, and blocks trusting the 3,980-token
   overhead figure.

7. **Correct the Graystone Lab model inventory** - `qwen3-coder:30b` is
   `qwen3moe`, 30.5B, not a dense 32B. The "NO MoE model is present" note is
   wrong. Re-confirmed from `/api/ps` this window.

8. **Fix `.gitignore:23`** as its own change - a negation for `tests/*run*.txt`,
   verified in isolation. Until then, `-f` every run log.

9. Ask Gray for the true Yahoo Inbox count from the web UI. Two seconds on his
   side, unanswered since W32. `usage_report` said 12,807 / 859 MB; an August
   web-UI reading said 286K. They cannot both be true.

10. Chase `[security] mode = "warn"` - unexplained config change governing a guard.

11. Defect 6 / 6e - the confirm gate client listener, still unbuilt.

12. Condense `[[openjarvis-rollback-points]]`, at its size cap.

13. The `/v1/sessions` patch - fully spec'd, still untouched.

14. `memdb_audit.log` under the 30 MB scheme.

---

## 11. PARKED - DO NOT CHASE MID-TASK

- **NEW: `/api/ps` mid-run is a safe, zero-cost production observability probe.**
  It answered the VRAM question in one read against a live inference. Reusable.
- The backend listener runs on the SYSTEM Python
  (`AppData\Local\Programs\Python\Python312`), not the venv interpreter, while a
  venv python runs alongside holding no port. Which interpreter loads which
  site-packages is not understood.
- `[security] mode = "warn"` appeared in config.toml with no window on record
  setting it.
- `conv=-` on RUNSTART - the agent still receives no conversation identity.
- Format 1 of `_extract_tool_call` is case-insensitive and unanchored, so prose
  containing "action:" can produce a false-positive tool name.
- `to_openai_function()` passes `parameters` through raw from `ToolSpec`, whose
  default is `{}`. Audit across the 12 tools.
- The confirm flow asks TWICE. UX defect, not Defect 1.
- Tool panel args render with cp437 mojibake in the desktop app.
- The 0 ms `account: yahoo` tool call preceding the real `account: yahoo_main` call.
- `ollama.py` lines 46 and 122-123 contain mojibake. Any patch to that file must
  read and write bytes or with explicit encoding, or it corrupts further.
- `git log -p --follow src\openjarvis\engine\ollama.py` to establish whether
  temperature 0.7 was deliberate or arrived with the file.
- Two benign skill-parser warnings on `research-paper-writing`. Cosmetic.
