# HANDOFF 2026-09-05 L / W34 - num_ctx IS NOW CONFIGURABLE AND SET TO 16384. THE BACKEND HAS NOT BEEN RESTARTED, SO NOTHING IS LIVE YET.

Predecessor: HANDOFF-2026-09-03-K-W33-SAMPLING-CONFOUND.md
All evidence in this window is dated 09/05 and was produced live in-window.

---

## 0. READ THIS FIRST - WHERE THE SYSTEM ACTUALLY SITS

One patch was built, applied and verified in isolation. One defect was found in
that patch, diagnosed to root cause, and fixed. Three verification legs all
pass. **The backend has NOT been restarted. The running process still holds the
old code and is still generating at num_ctx 8192.**

Nothing about Jarvis's behavior has changed yet. The next window's first
substantive act is the restart, and that is where behavior can shift.

Window cost: one deliverable (`patch_num_ctx_config.py`), one follow-up
one-liner fix, roughly a dozen read-only verifications. No probe was run. The
v3 rate experiment specified in W33 section 4 is STILL UNBUILT.

---

## 1. WHAT WAS DONE, IN ORDER

### 1.1 Two questions answered before any code was touched

**Gray asked why we cannot fix the temperature at the MCP server.** The premise
had a wrinkle worth recording. Ollama is not choosing the temperature - we are.
`src\openjarvis\engine\ollama.py` is our own client module, and it puts an
explicit `"options": {"temperature": ...}` in every request body (:73-75,
:191-193, :270-272). The Ollama server on 172.16.33.200 receives 0.7 and obeys
it. It is doing exactly what it was told.

**Consequence, and it is a trap worth keeping:** a Modelfile with
`PARAMETER temperature 0` would be SILENTLY OVERRIDDEN by the explicit
`options.temperature` in the request. A server-side change would appear to be
applied and would do nothing. Do not reach for that lever while `ollama.py`
still sends a value.

**Gray then asked whether the original design was a static temperature.** It is
subtler than static, and the distinction shapes the fix:

- `temperature: float = 0.7` sits in the FUNCTION SIGNATURE at :54, :183, :243.
  It was designed to be caller-settable. No caller on the agent path sets it.
- `num_ctx` never had a signature entry at all. It existed only as
  `kwargs.get("num_ctx", 8192)` inside the payload dict at :76, :194, :273. It
  was bolted into the body, never given a front door.

So: one parameter meant to be set that nobody sets, and one that was never
designed to be set. Neither reachable from `config.toml`. The agent path
inherited a general-purpose chat default by silence.

**NOT ESTABLISHED, and worth being honest about:** this describes the code as it
sits, not the author's intent. `git log -p --follow src\openjarvis\engine\ollama.py`
would show whether 0.7 was chosen deliberately or arrived with the file. Not run
- it is a side investigation and the rule says finish the current thing first.

### 1.2 Gray's direction: eliminate the truncation

Taken as the target. One qualifier was stated and stands unrefuted:
**truncation is proven real but is NOT proven to be Defect 1's cause.** W33
established that SYSTEM survived every truncation tested, up to 66 messages and
111KB at 8192; what gets squeezed out is the middle of the conversation. So
raising num_ctx will stop the context loss. Whether it stops the fabricated
moves is exactly the open question.

That is not an argument for delay. It is the reason the patch was applied ALONE,
with temperature deliberately untouched - two variables changed at once is
precisely the confound that wrecked the v1-versus-v2 comparison in W33.

---

## 2. THE PATCH - `patch_num_ctx_config.py`

Marker `openjarvis-num-ctx-config-v1`. Staged from Downloads to the repo root
and verified by MARKER CONTENT, not filename.

### 2.1 Design

Replaces the `8192` literal at all three sites with a resolver. Resolution
order:

1. env `OPENJARVIS_NUM_CTX`
2. `[engine] num_ctx` in `<OPENJARVIS_HOME or ~/.openjarvis>/config.toml`
3. `8192` - unchanged legacy behavior

Cached once per process. Every failure path falls back to 8192. Values under 512
are rejected back to 8192.

**Callers that pass `num_ctx` explicitly are untouched** - `kwargs.get()` still
returns their value first, so `research_loop.py`'s 16384 keeps working exactly
as it did.

**Deliberate property: the patch is INERT on apply.** With no env and no config
key, the resolver returns 8192 and behavior is byte-identical to before. That
buys two clean verification steps instead of one - prove the wiring, then prove
the value - so a later misbehavior can be attributed to one or the other.

### 2.2 KNOWN ARCHITECTURAL SHORTCUT - FOR THE SDP

The resolver reads `config.toml` DIRECTLY from the engine module. The clean fix
threads the value through `_make_engine` in `engine\_discovery.py`, the way
`_HOST_MAP` already does for the host. That remains FEED 1's question for the
550B model.

The contained version was chosen deliberately because it touches ONE file and
can be verified in isolation, which is the standing rule. **Record it in the SDP
as a known shortcut with a named better alternative, not as the intended
architecture.**

### 2.3 Safety handling in the script

- reads and writes BYTES, so the pre-existing mojibake at `ollama.py:46` and
  `122-123` passes through untouched and the LF terminator is preserved without
  a `newline=""` assumption
- requires the target literal EXACTLY 3 times, aborts otherwise
- refuses to run twice (marker check)
- `ast.parse` of the candidate before any write
- predicts post-patch size, compares to on-disk size after write, aborts and
  prints the restore command on mismatch
- dry run by default

### 2.4 Apply record

```
pre size    : 17785 bytes
eol         : LF
anchor hits : 3 (expected 3)
   site at line  76: "num_ctx": kwargs.get("num_ctx", 8192),
   site at line 194: "num_ctx": kwargs.get("num_ctx", 8192),
   site at line 273: "num_ctx": kwargs.get("num_ctx", 8192),
ast.parse   : OK
post size   : 19929 bytes (delta +2144)
backup      : src\openjarvis\engine\ollama.py.bak_numctx_20260905_083106
on disk     : 19929 bytes
  PASS  marker present
  PASS  3 call sites rewritten
  PASS  no hardcoded literal remains
  PASS  resolver defined
```

**17,785 B is exactly the Patch 5 RETRY400 post-patch state on record.** The
tree had not drifted - nothing else had touched `ollama.py` since 08/18. Line
numbers 76 / 194 / 273 match the 09/02 record exactly. This is a clean
continuity check and is worth doing on every future patch to this file.

---

## 3. THE VERIFICATION LEGS - ALL THREE PASS

Each run read-only, no backend, no Ollama contact.

**LEG 1 - patch is inert with nothing configured**
```
cfgpath C:\Users\Admin\.openjarvis\config.toml
fromcfg None
resolved 8192
```

**LEG 2 - env override**
```
OPENJARVIS_NUM_CTX=16384  ->  resolved 16384
```
Set inside the one python process only; nothing persisted.

**LEG 3 - config file** (after the BOM fix in section 4)
```
fromcfg 16384
resolved 16384
```

Env was tested BEFORE config deliberately, to separate "does the resolver work"
from "does the config parsing work". That ordering is what made the BOM defect
diagnosable in one step instead of two.

---

## 4. THE DEFECT FOUND IN MY OWN PATCH - BOM

### 4.1 What happened

After inserting `num_ctx = 16384` under `[engine]`, leg 3 returned
`fromcfg None` / `resolved 8192`. The config leg failed.

Diagnosed in one read-only command:
```
first8 b'\xef\xbb\xbf[engi'
bomchar '\ufeff'
strip_parse {'num_ctx': 16384, 'default': 'ollama'}
```

`Set-Content -Encoding UTF8` in PowerShell 5.1 writes a UTF-8 BOM. The BOM
defeated `tomllib`, and it ALSO defeated the regex fallback, because that
fallback anchors on `^\s*\[` and a BOM is not whitespace. Both parse paths
failed and `except Exception` returned None silently.

### 4.2 CLAUDE'S ERROR, STATED PLAINLY

**I told Gray the resolver tolerates a leading BOM. It does not.** That claim
was made in the same message that set up the write which produced the BOM. Worse,
my own `except Exception` swallowed the evidence, so the failure surfaced as a
silent default rather than an error.

**This is the same failure class the investigation keeps finding in this
codebase** - the silent tools-drop retry, the silent truncation, the masked
`prompt_eval_count` at :126. A component that swallows its own failure and
returns a plausible default cannot be distinguished from one that worked. I
wrote a fresh instance of the exact defect class we are hunting.

### 4.3 The fix

Appended `.lstrip(chr(65279))` to the decode line in
`_oj_num_ctx_from_config`. Guarded one-liner: asserted the anchor appears
exactly once, `ast.parse`d before write, own backup, byte-level so mojibake and
LF survive.

```
hits 1
bak  src\openjarvis\engine\ollama.py.bak_bomfix_20260905_091745
size 19948
```

**Fixing the parser rather than rewriting the config without a BOM was
deliberate.** `config.toml` is machine-regenerated (recorded in the rollback
register) and could come back BOM'd at any time. Tolerance belongs in the
reader.

### 4.4 Three smaller Claude errors this window, pinned so they are not repeated

1. **Predicted 19,947 bytes, actual 19,948.** Miscounted `.lstrip(chr(65279))`
   as 18 characters; it is 19. The file is correct - the prediction was wrong.
   Harmless here only because the script's own size check was not in play on a
   hand-written one-liner.
2. **Used `Format-Hex -Count`, which is PowerShell 6+.** Gray runs 5.1. The
   command errored. Every command must be valid on 5.1.
3. **Predicted the 4th line of config.toml would be `[intelligence]`** when I
   had just read that line 2 was `default = "ollama"`. Misstated a file already
   in front of me. Order does not matter in TOML so nothing broke, but stating a
   prediction from memory when the read is on screen is the exact habit the
   08/18 standing note warns about.

---

## 5. NEGATIVE RESULTS - WHAT THIS WINDOW ESTABLISHED THINGS ARE NOT

Per the 08/24 pinned rule, a thing proven NOT to be the case is knowledge and
gets pinned.

- **`config.toml` is NOT UTF-16 and is NOT corrupt.** A `Select-String` that
  returned nothing raised the possibility; the raw dump rendered as clean text.
  It is plain UTF-8, with a BOM as of this window's write.
- **The empty `Select-String` output was SCROLLBACK, not a file problem.** Long
  commands pushed the head of the output off screen twice. Diagnosis method that
  worked: ask for a deliberately short output (`-TotalCount 12`) rather than
  re-running the same wide command.
- **The tree had NOT drifted since 08/18.** 17,785 B matched the RETRY400 record
  exactly and all three anchor line numbers matched the 09/02 record.
- **`OPENJARVIS_HOME` is still empty**, so the resolver's `~/.openjarvis`
  fallback is the live path. Confirmed by the resolver printing
  `C:\Users\Admin\.openjarvis\config.toml`.

---

## 6. CONFIG STATE - TWO OBSERVATIONS WORTH CARRYING

`C:\Users\Admin\.openjarvis\config.toml`, backed up to
`config.toml.bak_numctx_20260905` (702 B, verified matching).

**6.1 The file has grown and changed since the last full read.** 580 B on 07/31,
686 B after the mailbox tool additions, **702 B now**. It is machine-regenerated
and the rollback register already warns it can silently revert. Re-read it,
never assume it.

**6.2 NEW, UNEXPLAINED, PARKED: `[security]` now carries `mode = "warn"`.**
That key was not in the 07/31 capture and no window on record set it. It is a
live security-profile setting that arrived from somewhere. Not chased - it
appeared mid-task and the rule is finish the current thing. **Do not let this
one sit indefinitely; it governs a guard.**

**6.3 Resolved without action:** `default_model` now reads `qwen3-coder:30b`,
matching the live model. The 08/01 model mismatch (config said
`qwen2.5-coder:32b`, `/v1/info` said `qwen3-coder:30b`) has closed itself in the
file at some point. Mechanism unknown, which is mildly interesting given 6.2.

Current `[engine]` section:
```
[engine]
num_ctx = 16384
default = "ollama"
```

---

## 7. ROLLBACK POINTS

### 7.1 `ollama.py` - THE CHAIN IS NOW THREE DEEP

Each restores to the state BELOW it, not to stock. **Restart the backend after
any of them.**

```
Copy-Item 'src\openjarvis\engine\ollama.py.bak_bomfix_20260905_091745' 'src\openjarvis\engine\ollama.py' -Force
```
-> returns to the num_ctx patch WITHOUT the BOM fix (19,929 B). Config leg will
silently fail; env leg still works.

```
Copy-Item 'src\openjarvis\engine\ollama.py.bak_numctx_20260905_083106' 'src\openjarvis\engine\ollama.py' -Force
```
-> returns to the RETRY400 state (17,785 B). num_ctx hardcoded 8192 again.

```
Copy-Item 'src\openjarvis\engine\ollama.py.bak_retry400_20260818_160710' 'src\openjarvis\engine\ollama.py' -Force
```
-> returns to STOCK.

### 7.2 config.toml

```
Copy-Item "$env:USERPROFILE\.openjarvis\config.toml.bak_numctx_20260905" "$env:USERPROFILE\.openjarvis\config.toml" -Force
```
-> removes `num_ctx = 16384`. 702 B, verified matching at copy time.

**The cheapest rollback for a num_ctx problem is the CONFIG KEY ALONE, not the
patch.** Set it back to 8192, or delete the line. The patch is inert without a
value.

### 7.3 Unchanged, carried forward

- Patch 4 (RAWGEN): `Copy-Item 'src\openjarvis\agents\native_openhands.py.bak_rawgen_20260818_145629' 'src\openjarvis\agents\native_openhands.py' -Force` then RESTART
- Patch 5 (RETRY400) is now the MIDDLE of the ollama.py chain above, not a
  standalone revert. Reverting to `.bak_retry400_20260818_160710` removes the
  num_ctx work AND returns to stock in one move.

Both remain temporary diagnostics and come out once Defect 1 is fixed.

---

## 8. EXECUTION PATHS REGISTER

No new path mapped this window. Carried forward unchanged:

**Path 1 - orchestrator `ask()`** via `system\orchestrator.py`.
**Path 2 - managed-agent SSE stream** via `_stream_managed_agent()` in
`server\agent_manager_routes.py`.
**Paths 1a/1b/1c/1d** - the `routes.py` chat dispatch branches.
**Path 3 - CONNECTOR-DIRECT** (W32): no ToolExecutor, no confirmation gate, no
protected-sender guard, no event bus traffic, human present by construction.

**AMENDED PROPERTY OF THE SHARED ENGINE LEG.** W33 recorded that every
generation on Paths 1 and 2 runs at `temperature 0.7` unseeded with
`num_ctx 8192`, none of it configurable. As of this window:

- `num_ctx` IS now configurable, is set to 16384 in `config.toml`, and is
  **pending a backend restart to take effect**
- `temperature` is STILL 0.7, still unseeded, still unreachable from config

Record it as a half-closed hazard, not a closed one.

---

## 9. SYSTEM DESIGN PACKAGE (SDP / SDD) - WHAT THIS WINDOW OWES IT

### 9.1 CONFIG CHAPTER - the two-parameter hazard is now half-fixed

W33 section 7.3 said `ollama.py` hardcodes both `num_ctx` and `temperature` at
three sites each with no config override, and that the same fix threads both.
**Half of that is now done and the other half is deliberately not.** Document
the asymmetry and the reason: changing both at once would have made the next
experiment unattributable.

### 9.2 NEW HAZARD CLASS - the silently-swallowed config parse

Section 4 of this handoff belongs in the guard chapter verbatim. A config reader
whose failure path returns a plausible default is indistinguishable from one
that succeeded. This joins the established family:

- silent tools-drop retry (`ollama.py:102-105`)
- silent server-side truncation
- the masked `prompt_eval_count` at `ollama.py:126`
- and now a silent config-parse failure, **written this window, by me**

The unifying property: each degrades WITHOUT AN ERROR SURFACE. The design rule
that falls out of it - **any fallback-to-default path must log that it fell
back.** None of the four does.

### 9.3 PLAIN-LANGUAGE EXPLANATION, per the 09/02 pinned rule

For `num_ctx`:

> Imagine the person doing your job can only hold so many pages in their hands
> at once. That limit was set to a small number and there was no way to change
> it - not a setting anywhere, just a number written inside the machine. When
> you gave them more pages than they could hold, they did not tell you. They
> quietly let the middle pages fall on the floor and answered from what was
> left.
>
> We have now put a dial on it, and turned the dial up to twice what it was. The
> dial did not exist yesterday.

For the BOM defect:

> When we wrote the new setting down, the program that wrote it added three
> invisible characters at the very start of the file. You cannot see them. The
> part that reads the file looked at the first thing on the page, did not
> recognize it, gave up, and - instead of saying "I could not read this" -
> quietly used the old number and carried on as if nothing had happened.
>
> That is the dangerous part. Not that it failed. That it failed and said
> nothing, and everything downstream looked normal.

### 9.4 METHOD NOTE for the SDD

The env-before-config test ordering is worth writing down as a pattern. Testing
the resolver through the env lever first isolated "the resolver works" from "the
file parses". When the config leg then failed, the cause was already narrowed to
one leg and took a single command to root-cause. **Test the simpler injection
path first, always.**

### 9.5 Unchanged and still owed

- Defect 6 confirmation gate: registry, payload, transport, threading model, in
  GREAT DETAIL. Not touched this window.
- The connector-direct path (W32 section 7.3) needs its own SDP entry.
- Prompt assembly and truncation diagram, with declared `num_ctx` marked at each
  gate, as a downloadable standalone file for the wiki. **This one is now more
  valuable, since the declared value at the gate has changed.**

---

## 10. THE 550B CLOUD MODEL - CARRIED FORWARD, FEED 1 IS PARTLY ANSWERED

Standing rule: when a question needs whole files rather than targeted reads,
bundle the suspected files into one markdown file for the 550B cloud model
(openrouter nemotron-3-ultra-550b) instead of spending window cycles on
piecemeal reads. 08/18 caveat holds - the free tier truncated one run and echoed
another; split into feeds of 2-3 questions.

Bundle unchanged:
- `src\openjarvis\engine\ollama.py` (whole - now carries the resolver)
- `src\openjarvis\agents\_stubs.py` (`_build_messages` :124-162, `_generate` :164-199)
- `src\openjarvis\agents\native_openhands.py` (prompt build :324-374, `_extract_tool_call` :161-250 incl. Format 4 at :216-240)
- `src\openjarvis\research_loop.py` (the 16384 workaround)
- `C:\Users\Admin\.openjarvis\config.toml`
- ADD: `src\openjarvis\engine\_discovery.py` (for the FEED 1 revision below)

**FEED 1 IS REVISED.** The question is no longer "how do we thread num_ctx" - a
working answer is applied. The question is now: *should the resolver move out of
`ollama.py` and into `_make_engine` / `_HOST_MAP` in `_discovery.py`, and what
is the cleanest shape that also threads temperature the same way without
changing behavior for callers that already pass either?*

**FEED 2 UNCHANGED and still the highest-value cheap question:** when
`raw_tool_calls` is empty, is `_extract_tool_call` actually reached on the live
path, and would Format 4 dispatch a `<function=...>` block found in content?
This decides whether the wrong-channel emission is a real production failure or
one the parser already absorbs. **If Format 4 absorbs it, a whole branch closes
for free.**

---

## 11. STANDING RULES - TWO ADDED THIS WINDOW

- **NEW: any fallback-to-default path must log that it fell back.** A silent
  default is indistinguishable from a success. Applies to config reading, retry
  logic, and every `except Exception` in this codebase.
- **NEW: every command must be valid on PowerShell 5.1.** `Format-Hex -Count` is
  6+ and failed. Check before pasting.
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
- Push to BOTH remotes - `origin` (GitHub) and `gitlab` (lab instance).

---

## 12. UNCOMMITTED WORK

Still nothing committed since W32. Untracked in `tests\`:
- `probe_bulk_census_v1.py`
- `probe_folder_census_v1.py`
- `probe_inbox_cleanup_v1.py`
- `probe_ctx_ceiling_v1.py`
- `probe_ctx_ceiling_v2.py`
- `ctx_ceiling_run_20260903.txt`
- `ctx_ceiling_v2_run_20260903.txt`

Untracked in repo root, NEW this window:
- `patch_num_ctx_config.py`

Modified tracked, NEW this window:
- `src\openjarvis\engine\ollama.py`

The two run logs are primary evidence for the SDD and should be committed with
the probes, not regenerated. **Note `ollama.py` still carries the Patch 4 and
Patch 5 temporary diagnostics** - decide before committing whether they go in
with it or come out first.

---

## 13. ORDERED NEXT ACTIONS

1. **RESTART THE BACKEND.** This is the first substantive act and everything
   below depends on it. Kill any stale python pairs first (they have appeared
   repeatedly - 08/17, 08/18) so a stale listener does not confuse the check.

2. **VERIFY 16384 IS LIVE IN THE RUNNING PROCESS - AND THIS NEEDS A METHOD
   DECIDED.** This is an OPEN DESIGN QUESTION, not a solved step. The in-process
   check in section 3 proves the resolver, but the backend is a DIFFERENT
   PROCESS. The probes post directly to Ollama and bypass our code entirely, so
   they cannot verify it either. And `ollama.py:126` masks `prompt_eval_count`
   behind a `max()`, so production telemetry cannot show it.
   Candidate shapes, none yet chosen: read the value back off a live
   `/v1/info`-style endpoint if one exposes it; a deliberate long-context
   conversation that previously died and now survives; or a minimal log line at
   the payload build. **Do not stack a new instrument patch on the unverified
   one without deciding this deliberately.**

3. **WATCH FOR THE KV CACHE COST.** 16384 doubles the KV cache on a resident 30B
   model across the P40s (24GB, Pascal). If generations slow markedly or Ollama
   starts evicting the model, that is the cost surfacing. The cheap rollback is
   the CONFIG KEY, not the patch - set it to 8192 or delete the line.

4. **Build and run `probe_ctx_ceiling_v3.py`** to W33 section 4's spec.
   Production sampling, two sizes, N=20, rate not verdict, both instrument
   defects fixed (empty content classifies UNINFORMATIVE and is excluded from
   the verdict; capture FULL content, not a prefix). This is the experiment that
   decides whether the remaining defect is sampling or context.

5. **Then, and only depending on 4's rate result:** either the sampling-side fix
   (thread temperature the same way, a seed, constrained decoding, or a retry on
   `ntc=0`), or back to the live agent path. Do not pre-commit to one.

6. Send the 550B bundle, **FEED 2 first** - it can close a whole branch cheaply.

7. Commit the nine files to BOTH remotes.

8. Ask Gray for the true Yahoo Inbox message count from the web UI. Two seconds
   on his side, unanswered since W32. `usage_report` said 12,807 / 859 MB; an
   August web-UI reading said 286K. They cannot both be true.

9. Chase `[security] mode = "warn"` (section 6.2) - unexplained config change
   governing a guard.

10. Defect 6 / 6e - the confirm gate client listener, still unbuilt.

11. Condense `[[openjarvis-rollback-points]]`, at its size cap.

12. The `/v1/sessions` patch - fully spec'd, still untouched.

13. `memdb_audit.log` under the 30 MB scheme.

---

## 14. PARKED - DO NOT CHASE MID-TASK

- `[security] mode = "warn"` appeared in config.toml with no window on record
  setting it (also listed at 9 above because it governs a guard).
- Two backend python processes have appeared repeatedly (08/17, 08/18). A stale
  listener confuses port-based diagnostics.
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
- The masked field at `ollama.py:126` - `prompt_tokens = max(reported_prompt,
  estimated_prompt)` still discards the one field that shows truncation.
  **Now more painful than before**, because it is also the field that would
  verify item 2 above.
- `git log -p --follow src\openjarvis\engine\ollama.py` to establish whether
  temperature 0.7 was a deliberate choice or arrived with the file.
