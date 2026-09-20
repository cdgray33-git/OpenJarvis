# HANDOFF 2026-09-03 J / W32 - MAILBOX EMERGENCY CLEARED, RETRY400 THEORY DEAD, num_ctx CEILING IS THE NEW LEAD

Predecessor: HANDOFF-2026-09-02-I-W31-PROTECTED-SENDERS-PROVEN.md
Evidence in this window is dated 09/02 (logs and probe runs); handoff written 09/03.

---

## 0. READ THIS FIRST - WINDOW DISCIPLINE

This window burned a large share of Gray's session budget: four scripts delivered
(bulk census, folder census, inbox cleanup, ceiling probe) plus several large log
reads. Gray flagged it directly. The mailbox emergency justified three of those;
the fourth should have been handed off rather than built in the same window.

**Rule reinforced for the next window: ONE deliverable per window when the budget
is live. Hand the second one off.**

---

## 1. WHAT WAS URGENT AND IS NOW CLOSED

Gray's Yahoo mailbox was out of space. This blocked his actual use of the system,
not just testing. It was routed AWAY from the agent (Defect 1 makes the agent
untrustworthy for destructive work) to the direct connector path.

### 1.1 Bulk (Spam) folder census - NOT the problem
`tests\probe_bulk_census_v1.py`, marker `openjarvis-bulk-census-v1`, read-only.

- 677 messages, 29.8 MB, **400 distinct senders**
- Largest single sender was 26 messages
- **Conclusion: Bulk was under 4 percent of the problem.** Long tail, no
  concentration, not worth a destructive script. Gray cleared it manually in the
  web UI.

NEGATIVE RESULT WORTH KEEPING: the agent's earlier "spam list" had claimed Bulk
was the target. It was not. Sizing a cleanup from a model's assertion instead of
a census would have wasted the whole effort.

### 1.2 Inbox census - the real problem
`tests\probe_folder_census_v1.py`, marker `openjarvis-folder-census-v1`,
read-only, takes the folder as an argument. Reusable - use this one, do not
write another census script.

- ROWS RETURNED **exactly 10000** - at the Yahoo IMAP window ceiling
- 749.7 MB, 878 distinct senders, 711 distinct domains
- Window spans **2026-05-23 to 2026-09-02, 102 days**, roughly 98 messages/day inbound
- Concentration: top 40 senders = 34.6 percent of messages, 34.0 percent of bytes
- Row keys confirmed: `['bytes', 'date', 'folder', 'from_addr', 'human', 'subject', 'uid']`.
  **Size key is `bytes`.** Record this - two probes guessed at it before it was known.

### 1.3 The cleanup run - EXECUTED, VERIFIED, SUCCESSFUL
`tests\probe_inbox_cleanup_v1.py`, marker `openjarvis-inbox-cleanup-v1`.
Dry run first, then `--apply`.

- 14 approved senders, exact-match on lowercased full address (NOT substring)
- **1,477 messages moved to Trash, 146.4 MB, ZERO failures, 944.3 s**
- Gray then emptied Trash manually. Space reclaimed. Emergency over.

Script carries its own guard because the real protected-sender guard is TOOL-LAYER
ONLY and connector-direct calls bypass it. Hardcoded exclusions: github,
capitalone, wellsfargo, chase, bank, irs.gov, usps, paypal, monster, visa.com.
Guard aborts the run on collision before opening a connection.

**Senders deliberately EXCLUDED and why** (the agent had wrongly listed several as
spam): `notifications@github.com` (Gray's own repo traffic, 188 msgs),
`capitalone@...` and `alerts@notify.wellsfargo.com` (financial),
`uspsinformeddelivery@...` (deliveries), `monster@notifications.monster.com`
(job search - Gray keeps a `2025 Job Search` folder). A model that cannot invoke
tools is unreliable as a JUDGE, not only as an ACTOR. Its target list was rebuilt
from the census, not inherited.

### 1.4 CONNECTOR SIGNATURE - PROVEN BY INTROSPECTION, RECORD IT
```
move_to_trash(folder: str, uids: Sequence[str], *,
              dry_run: bool = True, chunk_size: int = 10,
              pause_s: float = 1.0, max_retries: int = 4) -> Dict[str, Any]
```
- `dry_run` defaults to **True** and is **keyword-only**. Destructive action
  requires an explicit `dry_run=False`. Good design - do not change it.
- The connector does its OWN chunking at 10 with a 1.0 s pause and 4 retries.
  Outer batching just feeds it. 1,477 messages took 944 s because of this, and
  it produced zero failures. The retry-hardened path works.

---

## 2. **NEW ARCHITECTURAL FINDING - THE YAHOO WINDOW SLIDES**

This was an open question since 08/14 and the cleanup run answered it for free.

Measured across the 1,477-message move:
- rows BEFORE 10000, rows AFTER **10000** (delta 0 - held at the ceiling)
- oldest BEFORE `2026-05-23T13:48:56Z`, oldest AFTER **`2026-05-11T20:55:25Z`**
- **The window moved BACK 12 days as messages left it.**

**Yahoo refills the 10,000-message IMAP pane with older mail when messages are
removed.** The ceiling is a WINDOW, not a fixed set. Consequences:

1. Repeated cleanup passes reach progressively further back through the mailbox.
   The whole mailbox IS reachable over enough passes.
2. The local-archive architecture ([[openjarvis-mail-archive]]) is now OPTIONAL
   rather than required for reach. Still valuable for backup and offline NLP.
3. The 209 "target messages still in Inbox" after the run are **NOT failures** -
   they are newly-visible older messages from the same senders pulled in by the
   refill. Expect this on every pass. Do not read it as a defect.
4. The 1477-vs-1476 drift between dry run and apply is live inbound mail arriving
   between the two runs. Normal.

UNRESOLVED, cheap for Gray to settle: `usage_report` said 12,807 messages / 859 MB;
an August web-UI reading said 286K. Those cannot both be true and they change how
many passes finish the job. **Ask Gray to read the message count in the Yahoo web
UI.** Two seconds on his side.

---

## 3. DEFECT 1 - THE STATE OF THE INVESTIGATION

### 3.1 SPONTANEOUS RECURRENCE CAPTURED (09/02, the cleanest on record)

Gray asked Jarvis to move Spam to Trash. It claimed eleven per-sender moves.
Nothing moved.

agent.log sequence:
```
12:15  963c973f  turns=5  dispatched=4   healthy
12:17  72dca478  turns=5  dispatched=4   healthy
12:19  214f0358  turns=6  dispatched=5   healthy, last real dispatch 12:24:52
12:28  d5acf5db  turns=1  dispatched=0  ntc=0  chars=320
12:29  3bfba8a9  turns=1  dispatched=0  ntc=0  chars=3216   <- THE FABRICATION
12:54  6115f6ef  turns=1  dispatched=0  ntc=0  chars=2858   <- self-correction spiral
```
`dispatch.log` corroborates independently: last write 12:24:52, nothing after.
Two instruments, same boundary.

THREE THINGS THIS SETTLED:
1. The eleven "moves" were **ONE generation of 3,216 chars with ntc=0**. Never
   eleven attempts. The transcript's apparent sequence is a single fabricated block.
2. **NOT intermittent within the conversation - a HARD BOUNDARY.** Every run from
   12:28 onward failed identically. Tool emission never recovered.
3. The 12:28 and 12:54 runs saying "I don't have a direct way to delete in bulk"
   and "I don't have the proper system access" are **NOT confabulation**. That is
   a model accurately describing a prompt that no longer contains tool descriptions.

### 3.2 **RETRY400 / SILENT TOOLS-DROP THEORY IS DEAD FOR THIS EVENT**

`engine.log` still **179 B / 08/18 16:07:57** after a genuine spontaneous failure.
Only the two 08/18 probe lines. Patch 5 is live, armed, and silent.

The silent tools-drop retry at `ollama.py:102-105` **did not fire**. This was the
leading theory since 08/18. **Do not carry it as the front-runner.** Patch 5 stays
in - it has zero false positives and costs nothing - but it is now a ruled-out
branch for this failure mode.

### 3.3 **NEW LEADING HYPOTHESIS: THE UNCONFIGURED num_ctx=8192 CEILING**

`ollama.py` declares `"num_ctx": kwargs.get("num_ctx", 8192)` at THREE sites:
`:76` (generate), `:194`, `:273` (streaming).

Repo-wide grep of `src` for `num_ctx`, WITH a positive control (`max_tokens` = 490
hits, so the search reaches callers):
```
research_loop.py:341,364,374,487,653   num_ctx: int = 16384  (its own, threaded through)
ollama.py:76, 194, 273                 kwargs.get("num_ctx", 8192)
```
**Exactly one caller passes num_ctx, and it is not the agent path.** Everything
else - including `NativeOpenHandsAgent` - runs at **8192**. `config.toml` has no
num_ctx key anywhere.

`research_loop.py` setting its own 16384 is CORROBORATING evidence: another
subsystem already hit this wall and worked around it locally without fixing the
default.

Healthy multi-turn mailbox runs on record hit **17,077 input tokens** - more than
double the declared window.

MECHANISM: Ollama truncates server-side and returns 200. The SYSTEM message
carrying `{tool_descriptions}` sits at the FRONT of the prompt and goes first.

FITS EVERY OBSERVATION AT ONCE: no 400; empty `tool_calls` on a 200;
`changed=False`; fresh conversations always healthy; conversation history as the
leading correlate; a hard boundary rather than flicker; and a model that honestly
reports having no tools once past the line.

**IT ALSO EXPLAINS GRAY'S SECOND COMPLAINT.** He reported Jarvis "not acting the
way it had the other day" in its responses, separately from the fabrication. If
the prompt truncates from the front, the model loses the tool descriptions AND the
system prompt that shapes its behavior. **One mechanism, two symptoms, both keyed
to conversation length.** Treat degraded response quality and fabricated tool
results as the same bug until proven otherwise.

### 3.4 THE MASKED FIELD - `ollama.py:126`

```python
reported_prompt  = data.get("prompt_eval_count", 0)   # :124 - Ollama's own count
estimated_prompt = estimate_prompt_tokens(messages)   # :125 - our guess
prompt_tokens    = max(reported_prompt, estimated_prompt)   # :126 - THE MASK
```

**The one field that would show truncation has been captured all along and then
discarded by taking the max with our own estimate.** The 17,077 figure on record
is very likely the ESTIMATE, not what Ollama actually evaluated. We have never
seen the raw `prompt_eval_count` on a failing turn.

CONFOUND, must be stated in any conclusion: the comment at `:119-123` says
`prompt_eval_count` is KV-cache-aware, so a low value alone does not prove
truncation. **The discriminator is PINNING** - a value that flattens at a ceiling
as the payload grows is truncation; cache reuse gives scattered lows.

### 3.5 HAZARD FOR ANY PATCH TO ollama.py

Lines 46 and 122-123 already contain **mojibake** (em-dash and arrow characters
corrupted). The file carries pre-existing encoding damage. Any patch script must
read and write with explicit encoding or it will corrupt further. Patch 5's
`newline=""` handling preserved EOL but this is a separate axis.

---

## 4. NEXT ACTION - BUILT, NOT YET RUN

`probe_ctx_ceiling_v1.py` is **written and delivered to Gray's Downloads but was
never executed.** It is the immediate next step and it needs no patch, no backend
restart, and touches no mailbox.

WHAT IT DOES: posts payloads directly to Ollama shaped exactly as `ollama.py:69-89`
builds them, sweeping prompt size `[1000, 4000, 7000, 9000, 12000, 16000]` against
`num_ctx` `[8192, 32768]`. Records ntc, `prompt_eval_count`, payload bytes per cell.
Distinct filler per cell to suppress cache reuse. Smallest cell is a built-in
positive control - if it emits no tool call, the probe is wrong and the script
says so rather than allowing a false conclusion.

READ SHAPE:
- ntc dies at 8192 but holds at 32768 at the same size -> **CONFIRMED**
- ntc holds at both -> hypothesis wounded, move the search on
- ntc zero everywhere including the smallest -> fix the probe, not the theory

**If this confirms, Defect 1 becomes reproducible on demand for the first time.**
Two deliberate reproduction attempts failed in August; the defect has only ever
occurred spontaneously.

RUN IT (PowerShell 5.1, Windows box, from `PS C:\Users\Admin\OpenJarvis>`):
```powershell
Copy-Item "$env:USERPROFILE\Downloads\probe_ctx_ceiling_v1.py" ".\tests\" -Force; Select-String -Path ".\tests\probe_ctx_ceiling_v1.py" -Pattern "openjarvis-ctx-ceiling-v1" | Select-Object -First 1 | ForEach-Object { "MARKER OK: " + $_.Line.Trim() }; python .\tests\probe_ctx_ceiling_v1.py
```
Twelve generations on a 30B model - allow time. Check the HOST line first; if it
does not read `172.16.33.200` the config key was guessed wrong and the printed
value must be seen before trusting the run.

IF CONFIRMED, the fix is small and config-shaped: `num_ctx` is already read from
kwargs at all three sites, so it needs a config key threaded to the agent path -
not a code rewrite. **Verify in isolation before stacking anything on it.**

IF WOUNDED, the next instrument is a GENREQ/GENRESP pair logging `ntools`,
`payloadbytes`, `nmsgs`, `num_ctx`, `reported_prompt`, `estimated_prompt` and
`ntc` on EVERY request into the existing `engine.log`. Patch 5's blind spot is
that it only speaks on a 400, and this failure produced none.

---

## 5. ROLLBACK POINTS - NO NEW ONES THIS WINDOW

No source file was patched in W32. All four deliverables are standalone probes in
`tests\`. Existing rollbacks unchanged:
- Patch 4 (RAWGEN): `Copy-Item 'src\openjarvis\agents\native_openhands.py.bak_rawgen_20260818_145629' 'src\openjarvis\agents\native_openhands.py' -Force` then RESTART backend
- Patch 5 (RETRY400): `Copy-Item 'src\openjarvis\engine\ollama.py.bak_retry400_20260818_160710' 'src\openjarvis\engine\ollama.py' -Force` then RESTART backend

Both are temporary diagnostics and come out once Defect 1 is fixed.

---

## 6. EXECUTION PATHS REGISTER

No new path was mapped this window. Carried forward unchanged:

**Path 1 - orchestrator `ask()`** via `system\orchestrator.py`.
**Path 2 - managed-agent SSE stream** via `_stream_managed_agent()` in
`server\agent_manager_routes.py`.
**Paths 1a/1b/1c/1d** - the `routes.py` chat dispatch branches.

**NEW THIS WINDOW - Path 3, the CONNECTOR-DIRECT path** (not an agent path, but it
must be in the register because it is now the proven route for destructive work):
- Entry point: a standalone script under `tests\`, run from the CLI by Gray
- Call chain: `openjarvis.tools.mailbox_tools.connector_for(account)` ->
  connector instance -> `find_messages(folder=, limit=)` /
  `move_to_trash(folder, uids, *, dry_run=True, chunk_size=10, pause_s=1.0, max_retries=4)`
- ToolExecutor: **NONE.** No executor is constructed on this path.
- Confirmation gate: **ABSENT.** `--apply` in the calling script is the only gate.
- Protected-sender guard: **ABSENT** - it is tool-layer only (W31 2.1).
- Event bus traffic: **NONE.** Nothing appears in `dispatch.log` or `agent.log`.
- Human present: YES, by construction.

**This is the architectural hazard to document.** The connector layer has no
guard, no gate, and no audit trail. Every safety mechanism in OpenJarvis lives
above it. Any script written at this level must carry its own guard, as
`probe_inbox_cleanup_v1.py` does. Do not treat that as optional.

---

## 7. SYSTEM DESIGN PACKAGE (SDP / SDD) - WHAT THIS WINDOW OWES IT

Standing pinned rule: SDP is the secondary thought at all times. This window feeds
the following.

### 7.1 New hazard class for the guard chapter
A **declared context window that silently discards the front of the prompt**,
taking the tool contract and the system prompt with it. Same class as the silent
tools-drop retry: a mechanism that degrades capability without any error surface.

PLAIN-LANGUAGE VERSION (per the 09/02 pinned rule - an eight-year-old must follow it):

> Imagine you give someone a very long list of instructions, and at the top of the
> list you write down the tools they are allowed to use. Then you keep adding more
> and more to the bottom of the list. But the person can only hold a certain number
> of pages at once. When the list gets too long, the pages at the TOP fall out of
> their hands first - and those were the pages with the tools on them.
>
> Now the person still has the bottom of the list, so they know what you asked for.
> But they cannot see the tools anymore. So they do the best they can from memory,
> and they tell you they did the job - because from what they can still see, that
> is the answer that makes sense.
>
> They were not lying to you. They could not see the tools. We told the system it
> could hold 8,192 pages, and then we handed it 17,000.

### 7.2 Architecture artifact owed
The SDD needs a diagram of the prompt assembly and truncation path, with the
declared `num_ctx` marked at each gate, per Gray's standing requirement that
architecture artifacts show ports, protocols, and encoding at each gate and be
delivered as a downloadable standalone file for his wiki.

### 7.3 The connector-direct path (section 6 above) needs its own SDP entry
It is the layer beneath every guard in the system, and it is now the proven route
for destructive mailbox work. The SDP must state plainly that the confirmation
gate, the protected-sender guard, and the audit trail all live ABOVE this layer
and none of them apply to it.

### 7.4 Defect 6 confirmation gate
Unchanged from W31 - still owes GREAT DETAIL in the SDP on registry, payload,
transport, and threading model. Not touched this window.

### 7.5 Method lesson worth recording
The email cleanup succeeded because every step was measured before it was acted
on: census before target list, dry run before apply, re-census before believing
the result. The re-census is what produced the sliding-window discovery, which was
not what it was built to find. **Verification produces knowledge, not just
confidence.**

---

## 8. THE 550B CLOUD MODEL - CARRIED FORWARD

Standing rule: when a question needs whole files rather than targeted reads,
bundle the suspected files into a single markdown file for Gray's 550B cloud model
(openrouter nemotron-3-ultra-550b) rather than spending window cycles on
piecemeal reads.

**Candidate bundle if the ceiling probe confirms and the fix is not obvious:**
- `src\openjarvis\engine\ollama.py` (whole - all three num_ctx sites, the mask at :126)
- `src\openjarvis\agents\_stubs.py` (`_build_messages` at :124-162, `_generate` at :164-199)
- `src\openjarvis\agents\native_openhands.py` (prompt build at :324-374)
- `src\openjarvis\research_loop.py` (the 16384 workaround - how it threads num_ctx through)
- `C:\Users\Admin\.openjarvis\config.toml`

Question to ask it: what is the cleanest way to thread a configured `num_ctx` from
config.toml to all three ollama.py sites without changing behavior for callers
that already pass it.

---

## 9. STANDING RULES REAFFIRMED THIS WINDOW

- **Verify against the mailbox, never against the transcript.** Held again: the
  cleanup was verified by re-census, not by the script's own report.
- **Connector-level `find_messages` returns a PLAIN LIST**, not a dict. The
  `match_count` dict shape belongs to the tool layer. Assert `isinstance(r, list)`.
- **Size key on connector rows is `bytes`.** Now confirmed, stop guessing.
- **Re-census before sizing any destructive test.** Sender counts go stale from
  window roll AND from Gray's manual cleanup.
- **Trash counts against the Yahoo quota.** Moving to Trash frees nothing until
  Trash is emptied. Always a separate, deliberate step.
- **Every download lands in `C:\Users\Admin\Downloads\`** and gets renamed on
  re-delivery. Verify by marker content before running, never by filename.
- **Push to BOTH remotes** - `origin` (GitHub) and `gitlab` (lab instance).
  Nothing was committed this window; the four probes in `tests\` are uncommitted.

---

## 10. ORDERED NEXT ACTIONS

1. **Run `probe_ctx_ceiling_v1.py`.** Highest value, lowest cost, no patch needed.
2. If confirmed: thread a configured `num_ctx` to the agent path. Verify in
   isolation. Do not stack anything on it.
3. If wounded: build the GENREQ/GENRESP instrument into `engine.log`.
4. Ask Gray for the true Yahoo Inbox message count from the web UI.
5. Commit the four `tests\` probes to both remotes.
6. Defect 6 / 6e - the confirm gate client listener, still unbuilt.
7. Condense `[[openjarvis-rollback-points]]`, at its size cap.
8. The `/v1/sessions` patch - fully spec'd, still untouched.
9. `memdb_audit.log` under the 30 MB scheme.

---

## 11. PARKED - DO NOT CHASE MID-TASK

- Two backend python processes have appeared repeatedly (08/17, 08/18). A stale
  listener confuses port-based diagnostics.
- `conv=-` on RUNSTART - the agent still receives no conversation identity. Keeps
  `/v1/sessions` on the critical path.
- Format 1 of `_extract_tool_call` is case-insensitive and unanchored, so prose
  containing "action:" can produce a false-positive tool name.
- `to_openai_function()` passes `parameters` through raw from `ToolSpec`, whose
  default is `{}` - a tool that never sets it emits a bare `{}` with no
  `"type":"object"`. Audit across the 12 tools.
- The confirm flow asks TWICE (model prompts, then dry-runs and prompts again).
  UX defect, not Defect 1.
- Tool panel args render with cp437 mojibake in the desktop app.
- The 0 ms `account: yahoo` tool call preceding the real `account: yahoo_main`
  call - looks like an account-name miss returning instantly.
