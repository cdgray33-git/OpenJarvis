# HANDOFF 2026-09-05 M / W35 - num_ctx 16384 IS VERIFIED LIVE IN PRODUCTION. THE BACKEND IS RESTARTED AND RUNNING. A CONFIG BOM REGRESSION BLOCKED THE RESTART AND WAS ROOT-CAUSED AND FIXED.

Predecessor: HANDOFF-2026-09-05-L-W34-NUMCTX-CONFIG-THREADED.md
All evidence in this window is dated 09/05 and was produced live in-window.

---

## 0. READ THIS FIRST - WHERE THE SYSTEM ACTUALLY SITS

The backend has been restarted. The running process now holds the W34 patched
`ollama.py` and is generating at **num_ctx 16384, confirmed from the Ollama host
itself**. W34's open design question (how to verify the value is live in a
different process) is CLOSED, and closed without writing any new code.

One regression was found on the way: the backend would not start at all. Cause
was W34's own config write, not the num_ctx patch. Diagnosed and fixed in this
window.

Nothing has been committed yet. Nine-plus files remain untracked or modified.
The commit and the dual push are the next act.

Window cost: no new code, no patch script, one three-byte data fix, roughly a
dozen read-only verifications. The v3 rate experiment specified in W33 section 4
is STILL UNBUILT.

---

## 1. WHAT WAS DONE, IN ORDER

### 1.1 Pre-restart process hygiene

Two python processes were live, both started 09/02 07:52:49:

```
15476  C:\Users\Admin\OpenJarvis\.venv\Scripts\python.exe
19632  C:\Users\Admin\AppData\Local\Programs\Python\Python312\python.exe
```

Identical start timestamps to the second, so this was the normal launcher/child
pair from one start, NOT the stale orphan pair seen on 08/17 and 08/18. Nothing
needed cleaning up beyond the ordinary stop.

Listener ownership was captured before stopping anything:

```
127.0.0.1  8010  OwningProcess 19632
```

**Observation carried forward, not chased:** the process holding the listener is
the SYSTEM Python (`...\Programs\Python\Python312\python.exe`), not the venv
interpreter. The venv process held no port. This has implications for which
site-packages the running backend actually loads, and therefore for whether a
patched source file is picked up on restart. It did not bite us today - the
patch demonstrably took effect - but the mechanism is not understood. See
section 13.

Both stopped with `Stop-Process -Id 19632,15476 -Force`. Confirmed gone: process
list empty, port 8010 free. That confirmation matters - a half-dead listener is
what confused the 08/17 and 08/18 port diagnostics.

### 1.2 The restart FAILED - and the cause was ours

`.\start-openjarvis.ps1` got as far as "Starting server on port 8010" and then
threw:

```
File "C:\Users\Admin\OpenJarvis\src\openjarvis\core\config.py", line 1740, in load_config
  data = tomllib.load(fh)
tomllib.TOMLDecodeError: Invalid statement (at line 1, column 1)
```

Line 1, column 1 on a file that had parsed fine for weeks. Full detail in
section 2.

### 1.3 Restart succeeded after the fix

```
Engine: ollama
Model:  qwen3-coder:30b
Agent:  native_openhands
URL:    http://127.0.0.1:8010
WARNING openjarvis.cli.serve: BIND_ASSERT host=127.0.0.1 port=8010 loopback=True
```

Tool registry loaded including the mailbox tool set. Scheduler active, memory
active, `wired memory_backend into 1 agent tool(s)`. Speech backend
faster-whisper. Two benign skill-parser warnings on `research-paper-writing`
(unmapped `title` and `dependencies` frontmatter fields, values preserved).

### 1.4 Verification of the live value - see section 3

---

## 2. THE BOM REGRESSION - THE BACKEND COULD NOT START

### 2.1 Diagnosis

Read-only, one command, PowerShell 5.1 valid:

```
len 722
first8 239,187,191,91,101,110,103,105
```

`239,187,191` is `EF BB BF`, the UTF-8 BOM. Then `[engi`. Confirmed.

The 722 bytes account for cleanly against W34's recorded 702 B: 702 + 3 BOM +
17 for the inserted `num_ctx = 16384` line with CRLF. **No unexplained drift.**
Given W34 section 6.2 flagged an unexplained `[security] mode = "warn"` arriving
from nowhere, checking that the size fully accounts for was worth the seconds it
took.

### 2.2 ROOT CAUSE - ONE READER WAS FIXED, THE OTHER WAS NEVER CONSIDERED

W34 hit this same BOM in `_oj_num_ctx_from_config` and fixed it by making that
resolver BOM-tolerant, deliberately leaving the BOM in the file. The stated
reasoning was that `config.toml` is machine-regenerated and could come back
BOM'd at any time, so tolerance belongs in the reader.

**That reasoning is sound. It was applied to exactly one reader.**

`core\config.py:1740` `load_config()` is the other reader - the primary one, the
one the whole backend depends on - and it calls plain `tomllib.load(fh)` with no
BOM handling. It was never examined.

The defect was latent from the moment of W34's write (bomfix backup timestamped
09:17) and could not surface until something called `load_config()`. Nothing did
until the restart. **A latent-until-restart defect is its own hazard class: the
window that introduces it sees three green verification legs and closes clean.**

### 2.3 The fix applied

Stripped the three BOM bytes from `config.toml`, byte-level, with its own
backup. Deliberately a DATA fix, not a code fix - a code change to
`load_config()` would have been a second unverified change stacked on the
unverified num_ctx patch, which the standing rule forbids.

```
backup : C:\Users\Admin\.openjarvis\config.toml.bak_bomstrip_20260905
len    : 719  (predicted 719)
first8 : 91,101,110,103,105,110,101,93   = "[engine]"  (predicted)
```

Both predictions stated before the command ran and both matched.

### 2.4 STILL OWED - the durable fix

`load_config()` still cannot read a BOM'd config. `config.toml` is
machine-regenerated and can come back BOM'd, which would take the whole backend
down on next restart with a stack trace that looks nothing like an encoding
problem. Make `load_config()` BOM-tolerant as its own deliberate patch, verified
in isolation. Listed in section 12.

---

## 3. THE VERIFICATION - METHOD DECIDED, EXECUTED, PASSED

### 3.1 The problem W34 left open

W34 could prove the resolver returns 16384 in a test process. It could not prove
the BACKEND process sends it. The in-process check tests a different process;
the probes post directly to Ollama and bypass our code entirely; and
`ollama.py:126` masks `prompt_eval_count` behind a `max()`, so production
telemetry cannot show it. Three candidate methods were listed, none chosen.

### 3.2 First candidate tested and KILLED

`/v1/info` does not expose context length. It returns model, agent, engine only.
Dead end, recorded as a negative result.

### 3.3 The method that worked - FAR SIDE OF THE WIRE

**Ask the Ollama host what it actually loaded.** Ollama honors the `num_ctx` in
the request body and loads the model with that context. `GET /api/ps` on
172.16.33.200:11434 reports `context_length` for each resident model.

Why this is the right instrument, and worth reusing:

- it observes what our code SENT, not what our code says it would send. It is
  independent of our own logging, our own telemetry, and our own masked fields
- it needed no patch, no log line, and no new instrument on an already-unverified
  change
- it runs to completion on its own with no timing window to react to, which is
  the required test shape
- it is callable over plain HTTP from the Windows box. No ssh, no credentials

### 3.4 Execution and result

Baseline first: `/api/ps` returned an EMPTY models list. Nothing resident. This
was a lucky and clean starting condition - no stale 8192 load to muddy the read,
so the next load would be ours.

Then one trivial generation through `POST /v1/chat/completions` on the backend
(the route was read off `/openapi.json` rather than recalled from memory).
Returned `content: "ok"`, `finish_reason: stop`.

Then `/api/ps` again:

```
name             qwen3-coder:30b
family           qwen3moe
parameter_size   30.5B
quantization     Q4_K_M
size             20280883328
size_vram        20280883328
context_length   16384
expires_at       2026-09-06T13:50:00Z
```

**`context_length: 16384`. VERIFIED. The patch is live in production.**

---

## 4. NEGATIVE RESULTS AND CORRECTIONS

Per the 08/24 pinned rule, what a thing turned out NOT to be is knowledge.

- **`/v1/info` does NOT expose context length.** Killed as a verification
  method. Do not re-try it.
- **The two python processes were NOT a stale pair.** Identical start timestamps
  established that in one read. The 08/17 and 08/18 orphan pattern did not
  recur this time.
- **`config.toml` had NOT drifted unexplainedly.** 722 B accounts for exactly as
  702 + BOM + the inserted line. The `[security] mode = "warn"` mystery from
  W34 6.2 did NOT grow a sibling this window.
- **The restart failure was NOT the num_ctx patch.** It was the config write
  that accompanied it. The patch itself was never implicated.
- **CORRECTION TO THE 07/31 LAB INVENTORY - `qwen3-coder:30b` IS A MoE.** The
  Graystone Lab inventory records "NO MoE model is present" and states that
  every 19 GB entry is a dense 32B, which is the worst-case shape for the P40's
  weak compute. The host reports `family: qwen3moe`, `parameter_size: 30.5B` for
  the live production model. That pinned note is wrong for this model and the
  P40 compute picture is materially better than recorded. Correct the inventory.

---

## 5. KV CACHE COST - ANSWERED (W34 item 3)

W34 warned that 16384 doubles the KV cache on a resident 30B across the P40s and
to watch for slowdowns or eviction.

Measured: `size_vram` 20,280,883,328 bytes = 20.28 GB, fully resident, on a 24 GB
P40. **It fits at 16384.** Nothing evicting, nothing spilling to host memory.
Headroom is roughly 3.7 GB, which is thin but real.

`expires_at` sits about 24 hours out, so keep_alive is long and the model will
stay resident between sessions rather than cold-loading each time.

The cheap rollback remains the CONFIG KEY, not the patch: set `[engine] num_ctx`
to 8192 or delete the line, then restart.

---

## 6. A NUMBER WORTH PINNING - PROMPT OVERHEAD

The trivial one-line request "Reply with the single word: ok" reported:

```
prompt_tokens      3980
completion_tokens  2
```

**Roughly 3,980 tokens of prompt overhead before the user's message is even
counted** - system prompt plus tool schemas. Against the old 8192 that is
half the window gone before the conversation starts, which puts W33's truncation
findings in a much sharper light. Against 16384 it is under a quarter.

**Caveat, and it matters:** `ollama.py:126` computes
`prompt_tokens = max(reported_prompt, estimated_prompt)`, so this figure may be
our estimate rather than Ollama's count. Treat 3,980 as an order-of-magnitude
reading, not a measurement, until :126 is unmasked. It is one more reason to
unmask it.

---

## 7. ROLLBACK POINTS - UPDATED

### 7.1 `ollama.py` - chain unchanged, still three deep

Unchanged this window. See W34 section 7.1. No code was modified in W35.

### 7.2 `config.toml` - NEW THIS WINDOW

```
C:\Users\Admin\.openjarvis\config.toml.bak_bomstrip_20260905   (722 B, WITH BOM)
C:\Users\Admin\.openjarvis\config.toml.bak_numctx_20260905     (702 B, pre-num_ctx)
```

Restore the bomstrip backup (PowerShell, Windows box, any path):

```powershell
Copy-Item "$env:USERPROFILE\.openjarvis\config.toml.bak_bomstrip_20260905" "$env:USERPROFILE\.openjarvis\config.toml" -Force
```

**Note the trap:** restoring `bak_bomstrip_20260905` restores the BOM and the
backend will refuse to start again. That backup exists to prove what the bad
state was, not as a state to return to. The pre-num_ctx backup is the real
rollback.

Restart the backend after any of these.

---

## 8. EXECUTION PATHS REGISTER

Standing structure per path: entry point, call chain with file:line, which
ToolExecutor instance serves it and how it is constructed, whether the
confirmation gate is live / auto-approved / absent, event bus traffic, human
presence.

### 8.1 NEW PATH ESTABLISHED THIS WINDOW - STARTUP / CONFIG LOAD

Not an inference path, but it gates every other path and it took the system down
today, so it belongs in the register.

- **Entry point:** `.\start-openjarvis.ps1` from `C:\Users\Admin\OpenJarvis`,
  manual, admin session. Not a service, no autostart.
- **Call chain, read directly off the 09/05 traceback:**
  - `src\openjarvis\cli\__main__.py:6` -> `main()`
  - `src\openjarvis\cli\__init__.py:143` -> `cli()`
  - click dispatch -> `src\openjarvis\cli\serve.py:124` -> `load_config()`
  - `src\openjarvis\core\config.py:1740` -> `tomllib.load(fh)`
- **Failure mode:** hard abort, no fallback, no default config. An unparseable
  `config.toml` takes the entire backend down. Contrast with
  `_oj_num_ctx_from_config`, which swallows the same failure and returns a
  default silently. **Two readers of the same file with opposite failure
  philosophies. Neither is obviously right, but the inconsistency is itself a
  finding for the SDD.**
- **ToolExecutor:** not constructed on this path.
- **Confirmation gate:** not applicable.
- **Human present:** yes, always - manual start.

### 8.2 PATH EXERCISED THIS WINDOW - `POST /v1/chat/completions`, non-streaming

- **Entry point:** `POST http://127.0.0.1:8010/v1/chat/completions`, `stream=false`
- **Established today:** it reaches our `ollama.py` payload builder and the
  `num_ctx` resolver, proven by the host loading at 16384 after this call and
  only this call. It returns `usage` with prompt/completion tokens and a
  `complexity` block (`score`, `tier`, `suggested_max_tokens`).
- **NOT established this window:** the routes.py dispatch branch (1a/1b/1c/1d)
  this request took, the ToolExecutor instance and its construction, the
  confirmation gate state, and event bus traffic. The trivial prompt invoked no
  tool, so none of that was exercised. **Do not assume it matches the
  orchestrator path.** Left open deliberately rather than guessed at.
- **Human present:** yes, direct curl-equivalent.

### 8.3 Previously identified, unchanged

- Orchestrator `ask()` path via `system\orchestrator.py`
- Managed-agent SSE stream via `_stream_managed_agent()` in
  `server\agent_manager_routes.py`
- The routes.py chat dispatch branches 1a/1b/1c/1d

---

## 9. SDP / SDD FEED FROM THIS WINDOW

### 9.1 The architectural finding - CONFIG IS READ BY TWO READERS WITH NO SHARED CONTRACT

This is the headline SDP item from W35. `config.toml` is parsed in at least two
places, independently, with different encoding tolerance and opposite failure
behavior. One aborts the process; one silently substitutes a default. Neither
knows about the other. A change that satisfies one can break the other, and did.

The SDP should record: the file, its readers, what each tolerates, what each
does on failure, and the fact that no single component owns parsing it.

### 9.2 PLAIN LANGUAGE - what went wrong today, for the eight-year-old test

> Jarvis keeps its settings in a little notebook. This morning we wrote a new
> setting into the notebook, and the pen we used left an invisible smudge at the
> very top of the first page before the writing started.
>
> There are two people who read that notebook. Yesterday we taught the first
> reader to ignore the smudge, and he was fine. But we forgot there was a second
> reader. The second reader is the one who has to read the notebook before Jarvis
> can wake up at all. He saw the smudge, did not know what it was, and refused to
> read any further - so Jarvis never woke up.
>
> Two things are worth learning from that. The first is that when you fix a
> problem for one reader, you have to go and count how many readers there are.
> The second is that the second reader was actually the BETTER one, even though
> he is the one who stopped everything. He said loudly "I cannot read this."
> The first reader, when he could not read it, quietly used the old setting and
> said nothing at all - and that is far more dangerous, because everything looks
> like it is working.

### 9.3 METHOD NOTE - verify from the far side of the wire

When you need to prove that YOUR code sent something, ask the thing that
RECEIVED it. Do not add logging to the sender to prove what the sender does -
that is a new unverified change in the path you are trying to verify, and it
only tells you what the sender believes.

Today's instance: `/api/ps` on the Ollama host reported `context_length: 16384`.
That is independent of our telemetry, immune to our masked `prompt_eval_count`,
and needed zero new code. **Generalize it: before building an instrument, check
whether the far end already reports the thing.**

### 9.4 Unchanged and still owed

- Defect 6 confirmation gate: registry, payload, transport, threading model, in
  GREAT DETAIL, with the plain-language explanation alongside the technical one.
  Not touched this window.
- The connector-direct path (W32 section 7.3) needs its own SDP entry.
- Prompt assembly and truncation diagram, with declared `num_ctx` marked at each
  gate, ports/protocols/encoding at each gate, delivered as a downloadable
  standalone file for the wiki. **The declared value is now confirmed at 16384,
  so this diagram can finally be drawn with a real number on it.**

---

## 10. THE 550B CLOUD MODEL - CARRIED FORWARD

Standing rule: when a question needs whole files rather than targeted reads,
bundle the suspected files into one markdown file for the 550B cloud model
(openrouter nemotron-3-ultra-550b) instead of spending window cycles on
piecemeal reads. 08/18 caveat holds - the free tier truncated one run and echoed
another; split into feeds of 2-3 questions.

Bundle, with one addition:

- `src\openjarvis\engine\ollama.py` (whole - carries the resolver)
- `src\openjarvis\agents\_stubs.py` (`_build_messages` :124-162, `_generate` :164-199)
- `src\openjarvis\agents\native_openhands.py` (prompt build :324-374, `_extract_tool_call` :161-250 incl. Format 4 at :216-240)
- `src\openjarvis\research_loop.py` (the 16384 workaround)
- `C:\Users\Admin\.openjarvis\config.toml`
- `src\openjarvis\engine\_discovery.py`
- **ADD: `src\openjarvis\core\config.py`** - for FEED 3 below

**FEED 2 IS STILL THE HIGHEST-VALUE CHEAP QUESTION, SEND IT FIRST:** when
`raw_tool_calls` is empty, is `_extract_tool_call` actually reached on the live
path, and would Format 4 dispatch a `<function=...>` block found in content? If
Format 4 absorbs it, a whole branch closes for free.

**FEED 1, unchanged from W34's revision:** should the num_ctx resolver move out
of `ollama.py` into `_make_engine` / `_HOST_MAP` in `_discovery.py`, and what is
the cleanest shape that also threads temperature the same way without changing
behavior for callers that already pass either?

**FEED 3, NEW:** `config.toml` has at least two independent readers with
different encoding tolerance and opposite failure behavior
(`core\config.py:1740` aborts, `_oj_num_ctx_from_config` silently defaults).
What is the minimal change that gives one owner of config parsing, tolerant of
BOM and encoding variation, without a large refactor and without changing
startup's fail-loud behavior?

---

## 11. STANDING RULES - TWO ADDED THIS WINDOW

- **NEW: when you fix a parser, count the readers.** A tolerance fix applied to
  one reader of a shared file is not a fix. Enumerate every consumer before
  declaring it handled.
- **NEW: a defect that can only surface on restart is its own hazard class.**
  W34 closed with three green legs and a latent process-killing bug. Any change
  touching config, environment, or startup must be validated by an actual
  restart in the same window, not by in-process checks alone.
- Any fallback-to-default path must log that it fell back. A silent default is
  indistinguishable from a success.
- Every command must be valid on PowerShell 5.1. `Format-Hex -Count` is 6+.
- Probes must mirror PRODUCTION sampling (`temperature 0.7`, unseeded) unless
  the experiment is specifically about sampling.
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

## 12. UNCOMMITTED WORK - THE COMMIT IS THE NEXT ACT

Nothing committed since W32. Untracked in `tests\`:

- `probe_bulk_census_v1.py`
- `probe_folder_census_v1.py`
- `probe_inbox_cleanup_v1.py`
- `probe_ctx_ceiling_v1.py`
- `probe_ctx_ceiling_v2.py`
- `ctx_ceiling_run_20260903.txt`
- `ctx_ceiling_v2_run_20260903.txt`

Untracked in repo root:

- `patch_num_ctx_config.py`

Modified tracked:

- `src\openjarvis\engine\ollama.py`

The two run logs are primary evidence for the SDD and should be committed with
the probes, not regenerated.

**DECIDED THIS WINDOW:** the Patch 4 and Patch 5 temporary diagnostics in
`ollama.py` **go in with the commit as-is.** Removing them would be a code
change to a file we just verified live, requiring its own verification round
before the push - which is the stacking the standing rule forbids. They come out
later as a deliberate patch. Tag them in the commit message so the next reader
knows they are temporary.

---

## 13. ORDERED NEXT ACTIONS

1. **Commit the nine files and push to BOTH remotes.** `origin` is GitHub,
   `gitlab` is the lab instance at 172.16.33.126. Plain `git push`, never
   `--mirror` - see the 08/05 incident.

2. **Build and run `probe_ctx_ceiling_v3.py`** to W33 section 4's spec.
   Production sampling, two sizes, N=20, rate not verdict, both instrument
   defects fixed (empty content classifies UNINFORMATIVE and is excluded from
   the verdict; capture FULL content, not a prefix). **This is now the single
   most valuable thing on the list** - context is fixed and verified, so this
   experiment finally isolates whether the remaining Defect 1 behavior is
   sampling or was context all along.

3. **Then, and only depending on 2's rate result:** either the sampling-side fix
   (thread temperature the same way, a seed, constrained decoding, or a retry on
   `ntc=0`), or back to the live agent path. Do not pre-commit to one.

4. Send the 550B bundle, **FEED 2 first** - it can close a whole branch cheaply.

5. **Make `load_config()` BOM-tolerant** as its own isolated patch. Until then a
   machine-regenerated BOM'd `config.toml` will take the backend down on the
   next restart.

6. **Unmask `ollama.py:126`** - `prompt_tokens = max(reported, estimated)`
   discards the one field that shows truncation, and is why item 2 needed an
   external instrument at all. Now also blocks trusting the 3,980-token
   overhead figure.

7. **Correct the Graystone Lab model inventory** - `qwen3-coder:30b` is
   `qwen3moe`, 30.5B, not a dense 32B. The "NO MoE model is present" note is
   wrong.

8. Ask Gray for the true Yahoo Inbox message count from the web UI. Two seconds
   on his side, unanswered since W32. `usage_report` said 12,807 / 859 MB; an
   August web-UI reading said 286K. They cannot both be true.

9. Chase `[security] mode = "warn"` - unexplained config change governing a
   guard.

10. Defect 6 / 6e - the confirm gate client listener, still unbuilt.

11. Condense `[[openjarvis-rollback-points]]`, at its size cap.

12. The `/v1/sessions` patch - fully spec'd, still untouched.

13. `memdb_audit.log` under the 30 MB scheme.

---

## 14. PARKED - DO NOT CHASE MID-TASK

- **NEW: the backend listener runs on the SYSTEM Python
  (`AppData\Local\Programs\Python\Python312`), not the venv interpreter, while a
  venv python runs alongside holding no port.** Which interpreter loads which
  site-packages is not understood. The patch took effect today so it is not
  urgent, but it is a live ambiguity in how the process is actually launched.
- `[security] mode = "warn"` appeared in config.toml with no window on record
  setting it (also at 9 above because it governs a guard).
- `conv=-` on RUNSTART - the agent still receives no conversation identity.
- Format 1 of `_extract_tool_call` is case-insensitive and unanchored, so prose
  containing "action:" can produce a false-positive tool name.
- `to_openai_function()` passes `parameters` through raw from `ToolSpec`, whose
  default is `{}`. Audit across the 12 tools.
- The confirm flow asks TWICE. UX defect, not Defect 1.
- Tool panel args render with cp437 mojibake in the desktop app.
- The 0 ms `account: yahoo` tool call preceding the real `account: yahoo_main` call.
- `ollama.py` lines 46 and 122-123 contain mojibake. Any patch to that file must
  read and write bytes or with explicit encoding, or it corrupts further. The
  W34 patch script handled this correctly - reuse its approach.
- `git log -p --follow src\openjarvis\engine\ollama.py` to establish whether
  temperature 0.7 was a deliberate choice or arrived with the file.
- Two benign skill-parser warnings on `research-paper-writing` (unmapped `title`
  and `dependencies` frontmatter fields). Cosmetic, values preserved.
