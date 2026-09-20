# HANDOFF 2026-08-31 C / WINDOW 25
# imap_mail.py READ, COMMITTED AND PUSHED - ONE DIFF LEFT IN THE ENTIRE BACKLOG
# Plus: the 300s timeout figure is STALE, three hazards on the destructive path,
# and a stale-handoff failure that cost three exchanges

Predecessor: HANDOFF-2026-08-31-B-W24-THREE-DIFFS-CLEARED-FOUR-FOR-FOUR-REFUTED.md
Host: Windows box. Shell: PowerShell 5.1. Working dir: `PS C:\Users\Admin\OpenJarvis>`.
Backend: 127.0.0.1:8010, ollama, qwen3-coder:30b, agent native_openhands.
Window shape: provenance and commit window, third in a row. Nothing was patched.
Nothing was debugged. ONE commit made, pure provenance - no code behavior was changed
by this window's own actions. The window ended by DECIDING to stop diff work with four
exchanges left rather than starting `mailbox_tools.py` at the tail.

---

## 0. ONE PARAGRAPH FOR THE NEXT WINDOW

`imap_mail.py` is read verbatim, committed at `611329e` and pushed to both remotes.
It is the Yahoo chunk/retry work - chunk 10, pause 1.0s, 4 retries with exponential
backoff, then per-UID degradation. **The unread-diff backlog is now ONE file:
`mailbox_tools.py`.** Give it the front of a window. Three hazards were recorded on
the destructive move path and NOT patched; hazard 2 (partial failure reports success)
is decided in `mailbox_tools.py` itself, because grep proved it is the only caller.
The "300s tool timeout" in the memory record is STALE for this tool - the real bound
is 1800s. This window also opened on the WRONG handoff, which cost three exchanges and
produced a rediscovery of W24's own finding; section 2.1 has the correction.

---

## 1. WHAT LANDED - ONE COMMIT

| Hash | Content | Counts | Verified by |
|---|---|---|---|
| `611329e` | `imap_mail.py` - chunked/paced/retried `move_to_trash`, plus `_imap_text()` | 88 ins, 12 del | `status --short` BLANK |

Pushed: `746ce84..611329e` to `origin` AND `gitlab`. Plain fast-forward, identical
object counts (6 objects, 2.80 KiB). No `--mirror`, no `--force`. Both remotes verified
at `611329e` by `log --oneline -1 origin/main` and the same against `gitlab/main`, in
the same exchange as the push.

The three hazards below are in the commit message body, not only in this file. The
commit message is the provenance record that survives independent of the handoffs -
which matters more than usual given section 2.1.

---

## 2. NEGATIVE RESULTS AND CORRECTIONS - PIN THESE

### 2.1 THIS WINDOW OPENED ON A STALE HANDOFF - my error, and the most useful finding here

Gray uploaded W23. W24 already existed, in the repo root, unread by me. I spent three
exchanges re-deriving `auth_middleware.py` and announced a "third hypothesis dead" that
was simply W24's `7ddece9` rediscovered. No new information, three exchanges gone.

What caught it: `git status --short` listing the repo root, where
`HANDOFF-2026-08-31-B-W24-...md` was sitting in plain view. **Git corrected the handoff,
for the second time in two windows.**

**Rule adopted: at the START of every window, run `git --no-pager log --oneline -5` and
list the handoff files, and reconcile the uploaded handoff against what HEAD actually
says BEFORE acting on any of its claims.** A handoff describes the tree at the moment it
was written. It is a claim about the past, not a description of the present. This is the
same lesson as "a hypothesis about a diff is not evidence about that diff", one level up:
now it applies to the handoff chain itself.

### 2.2 The count was wrong a THIRD time

W22 recorded `imap_mail.py +100`. Actual, from the summary line: **88 insertions, 12
deletions.** Same cause as W23 section 2.1 - the `--stat` graph column read as an
insertion count. Three instances now.

**`mailbox_tools.py +290` is from the same pass and is therefore also wrong.** Do not
plan around 290. Take the real count from the `N insertions(+), M deletions(-)` line
when the file is opened.

### 2.3 Hypothesis tally - five tested, first partial hit

| Diff | W22 hypothesis | Actual |
|---|---|---|
| `ollama.py +58` | Patch 4 RAWGEN | Patch 5 retry400 (W23) |
| `native_openhands.py +167` | Defect 1 parser formats | THREE changes (W23) |
| `auth_middleware.py +31` | v3 redaction | W19 bind assertion (W24) |
| `routes.py +20` | 6c confirm route | event-loop offload (W24) |
| `imap_mail.py +100` | Yahoo chunk/retry PLUS redaction | chunk/retry YES, redaction NO (W25) |

First hypothesis not wholly refuted. It was still wrong on its second clause - redaction
is not in this file at all. The standing rule does not weaken: read the diff.

### 2.4 The 300s tool timeout figure is STALE for the destructive path

The memory record carries "300s timeout" as the bound on the tool-invocation false
negative. For `mailbox_move_to_trash` that is **wrong and has been for some time**.

- `_stubs.py:41` - `ToolSpec.timeout_seconds` default is **30.0**, not 300.
- `_stubs.py:367` - `timeout = tool.spec.timeout_seconds or self._default_timeout`.
- `mailbox_tools.py:509` - the registered spec sets **`timeout_seconds=1800.0`**, marker
  `openjarvis-tool-timeout-v1`. Thirty minutes. Someone raised this deliberately.
- The 300.0 values live at `imap_mail.py:837/858/899` - **different tools**.

I briefly concluded the bound was 30s and that the patch could never complete a large
move. That was wrong; I checked before committing rather than after. Worst case for a
fully-degraded 290-uid run is roughly 12 minutes, which fits inside 1800s with room.

**Correct the memory record.** Quoting "300s" at this tool will mislead the next window.

### 2.5 Authoring defect - I broke W24's own new rule, in my first commit attempt

W24 section 2.3 adopted "ONE runnable block per message, source labeled as source"
after a JS line was pasted into PowerShell. I then handed Gray a **bash heredoc**
(`git commit -F - <<'MSG'`) in PowerShell 5.1. Parse error, console left at a `>>`
continuation prompt, nothing executed, tree untouched. Cost one exchange.

**The rule was insufficient because it addressed presentation, not dialect.** Widened:
**every runnable block must be valid in the target shell, and PowerShell 5.1 is the
target unless explicitly labeled otherwise. Heredocs, `<<`, and `$(...)` command
substitution are bash and must never appear in a block for Gray.** The working
PowerShell idiom for a multi-line commit message is recorded in section 7.

---

## 3. THE `imap_mail.py` FINDING - WHAT `611329e` ACTUALLY DOES

`move_to_trash` gains three keyword args: `chunk_size=10`, `pause_s=1.0`,
`max_retries=4`. Docstring records that Yahoo rate-limits bulk UID COPY and reports it
inconsistently - `[LIMIT]` on large sets, `[SERVERBUG]` on small ones, both transient.

The COPY loop, replacing a single all-uids COPY:

1. `uids` coerced to `str` up front.
2. If source folder IS trash, skip COPY entirely, treat all as copied.
3. Otherwise chunk into 10s. Per chunk: up to 4 COPY attempts, `time.sleep(delay)`
   between them, `delay *= 2` (so 1s, 2s, 4s, 8s).
4. If the chunk still fails, **degrade to one UID at a time** so a single poisoned
   message cannot strand the other nine. 1s pause between singles.
5. 1s pause between chunks.
6. `\Deleted` is set only on UIDs whose COPY returned OK, in chunks, 1s apart.
7. `imap.expunge()`, then `applied = deleted > 0`.

New reporting keys on the plan dict: `copied_count`, `failed_uids`, `copy_errors`
(first 10), `deleted_count`, `store_failed`, and a `note` when copies failed.

New helper `_imap_text(data)` - static, flattens an imaplib response payload to a
readable string, bytes decoded UTF-8 with `replace`, bare `except` returning `repr`.

### 3.1 HAZARD - COPY-then-STORE is no longer atomic

COPY ok + STORE fail leaves the message **in Trash AND in the source folder**. A
duplicate. It is recorded in `store_failed` and never reconciled. The old code was
all-or-nothing: either both succeeded or the whole operation reported failure.

### 3.2 HAZARD - partial failure reports success. THIS IS THE ONE THAT MATTERS

`plan["applied"] = deleted > 0`. **Three UIDs out of 290 returns `applied: True`.**
The `note` field explaining what was left in place fires only for COPY failures, never
for STORE failures.

Why this is worse than an ordinary bug: **Defect 1 is Jarvis claiming completed
destructive mailbox actions that did not happen.** This hands the model a result that
reads as success when it mostly was not. The model is not confabulating in that case -
it is reporting what the tool told it.

Grep established `move_to_trash` has **exactly one caller**: `mailbox_tools.py:667`
(dry run) and `:669` (live). So the contract is decided in the one file still unread.
Read section 3.2 of this handoff before deciding what `mailbox_tools.py` should do with
`applied`, `failed_uids` and `store_failed`.

### 3.3 HAZARD - `time.sleep` blocks a pool worker, downgraded from a suspected deadlock

A degraded 290-uid run holds a worker for roughly 12 minutes. Investigated because W24
established that a gate raised from the event loop deadlocks.

**Not an event-loop deadlock.** The synchronous tool chain runs on a worker thread:
`routes.py:168` and `:176` (that is W24's `aad8ccd`), `stream_bridge.py:155`,
`agent_manager_routes.py:2258`, and `confirm_registry.py:9` documents the model
explicitly. This is the known pool-starvation constraint made worse **in degree**, not
a new class of failure. Recorded, not patched.

---

## 4. WHAT REMAINS UNREAD - ONE DIFF

```
src/openjarvis/tools/mailbox_tools.py
```

That is the whole backlog. `git status --short` shows it as the only modified tracked
file besides the one just committed.

- Count is UNVERIFIED (section 2.2). Not 290.
- It threw the **CRLF warning** on every `--stat` this window - `.gitattributes` question,
  next actions item 7.
- It touches **destructive mailbox paths** and it is the sole caller of the function
  just committed.
- It is where hazard 3.2 gets decided.
- Read it against the mailbox and tool-invocation memory records BEFORE composing the
  commit, per the standing procedure.

Procedure, unchanged and working five for five:
`git --no-pager diff --stat -- <one file>`, then `git --no-pager diff -- <same file>`,
read verbatim, **grep every identifier it introduces or calls**, then compose the commit.
One file at a time. Expect the hypothesis to be wrong.

---

## 5. EXECUTION PATHS REGISTER

Standing structure. Carried forward and extended, not re-derived.

### PATHS ALREADY REGISTERED (unchanged this window)

- PATH 1: orchestrator `ask()` via `system\orchestrator.py`
- PATH 2: managed-agent SSE via `_stream_managed_agent()` in `server\agent_manager_routes.py`
  (four auto-approve sites, open item 6 - still the largest outstanding gate item)
- PATH 3: test-execute trigger via `POST /v1/tools/test-execute` - gate LIVE, `confirm_id`
  verified on the wire (W21)
- `routes.py` chat dispatch branches 1a/1b/1c/1d - non-streaming branches offloaded to
  `asyncio.to_thread` as of `aad8ccd` (W24)
- Frontend submit paths F-A typed, F-B voice, F-C option relay (DEAD - no handler for
  `jarvis-submit-text`)
- Tool-call extraction order inside `_extract_tool_call`: native, then Format 1
  (case-insensitive, UNANCHORED), Format 2 (unread), Format 4 (XML, shadowed by 1),
  Format 3 (bare JSON). Precedence is an accident of insertion order. (W23)

### EXTENDED THIS WINDOW - the destructive mailbox path, with timings

`mailbox_move_to_trash` end to end, as it now stands at `611329e`:

| Property | Value |
|---|---|
| Registration | `mailbox_tools.py:453`, `@ToolRegistry.register("mailbox_move_to_trash")` |
| Spec | `mailbox_tools.py:463-509`, `timeout_seconds=1800.0` marker `openjarvis-tool-timeout-v1` |
| Confirmation gate | `requires_confirmation=True` per SDP revB:504 / revC:597 - VERIFY at the spec, not from the SDP |
| Caller into connector | `mailbox_tools.py:667` dry run, `:669` live - the ONLY callers |
| Connector method | `imap_mail.py:537` `move_to_trash` |
| Protocol | IMAP over the connector's session; UID COPY, UID STORE +FLAGS \Deleted, EXPUNGE |
| Threading | synchronous; runs on an `asyncio.to_thread` worker, never the event loop |
| Blocking floor | ~1s per chunk of 10, so ~29s for 290 uids on a fully clean run |
| Blocking ceiling | ~12 min for 290 uids fully degraded (15s backoff + 10 singles per chunk) |
| Timeout headroom | 1800s bound vs ~12 min worst case - fits |

**The timing rows are new and belong in the SDD.** Before `611329e` this call had no
deliberate pacing and its duration was a function of the server alone. It now has a
floor proportional to message count, which is a property the confirmation gate's 120s
TTL and the pool-starvation constraint both have to be reasoned against.

---

## 6. SDP / SDD FEED

**Architecture - repository integrity.** Unchanged in substance: no CI, no clean-clone
import check, no provenance record linking hunks to windows. W25 adds a second-order
version of the same problem: **the handoff chain itself has no integrity check.** This
window acted on a superseded handoff for three exchanges because nothing reconciles the
uploaded document against HEAD. Provenance reconstructed manually by diff-reading is
now at W23/W24/W25 - three consecutive windows, one file each at the end. State plainly
in the SDP that this does not scale and that the mitigation is CI plus commit-message
provenance, not better handoffs.

**Defect 1 - a NEW mechanism, distinct from confabulation.** The SDP records Defect 1 as
the model claiming destructive actions it did not invoke. Section 3.2 documents a second,
independent route to the same symptom: **the tool truthfully reports `applied: True` for
a partial move.** The model is then accurate about an inaccurate result. These need
separating in the SDP - they have different fixes. Confabulation is a parser and prompt
problem; this is a result-contract problem in `mailbox_tools.py`.

**Defect 6 confirmation gate - GREAT DETAIL per Gray's standing instruction.** W25 adds:
- **timing, new**: the gated tool's own runtime now has a deliberate floor and a ~12 min
  degraded ceiling (section 5). The gate's 120s TTL governs the WAIT FOR A HUMAN, not the
  execution that follows. Confirm the SDP states that separation explicitly, because a
  reader who conflates them will conclude the gate times out mid-move. It does not.
- **timeout bound corrected**: 1800s at `mailbox_tools.py:509`, NOT the 300s on record
  and NOT the 30.0 `ToolSpec` default (section 2.4).
- **threading model**: unchanged from W24 and now confirmed by grep for this path
  specifically - `to_thread` at `routes.py:168/176`, `stream_bridge.py:155`,
  `agent_manager_routes.py:2258`. Correctness requirement, not a performance guideline.
- **registry**: write-once, 409 on re-decision, TIMEOUT internal only. Unchanged.
- **payload**: seven fields; `turn_id` from `CURRENT_TURN_ID` set by
  `openjarvis-agent-log-v1` - diagnostic marker load-bearing on the gate payload. Still
  a design smell worth naming.
- **transport**: EventBus -> ws_bridge -> bare WS client. Delivery proven W20, payload
  integrity W21. Redaction CLOSED, do not re-open.
- **source integrity**: RESOLVED, both remotes at `611329e`.
- **UNVERIFIED**: `requires_confirmation=True` for this tool is taken from SDP revB:504
  and revC:597, both prose. It has NOT been read at the spec in this window. Read
  `mailbox_tools.py:463-509` directly when that file is opened and either confirm it or
  correct the SDP.

**Threat model.** Unchanged from W24, including the refinement that both copies of the
bind verdict classify an empty host as loopback and that the copy consumers read is the
`serve.py:613-615` duplicate. Known accepted risk.

**Verification methodology chapter - two new entries (running total six):**
5. Reconcile the handoff against HEAD before acting on it. A handoff is a claim about
   the past. Git is the present. Two windows running, git corrected the handoff
   (section 2.1).
6. A runnable block must be valid in the TARGET SHELL. W24's "one block per message" was
   about presentation and did not prevent a bash heredoc being handed to PowerShell 5.1
   (section 2.5). Dialect is part of the instrument.

**Architecture artifacts still owed:** ports, protocols and encoding at each gate, as a
downloadable standalone file for Gray's wiki. **NOT produced this window. Now owed across
FIVE windows.** This window flagged the fork explicitly at exchange 5 and Gray was given
the choice; diff work was taken deliberately, on the reasoning that `mailbox_tools.py`
is gate-relevant and building the artifact against an unread diff would mean building it
twice. **That reasoning expires the moment `mailbox_tools.py` is committed.** Section 5
of this handoff now contains real protocol and timing rows for one gate - that is the
seed of the artifact and should be lifted directly into it.

---

## 7. 550B CLOUD MODEL

Carried forward per the 08/29 pin. **Untouched this window.**

`bundle_for_cloud.py` in the repo root, marker `openjarvis-cloudbundle-v1`. Read-only,
stdlib only, does not import openjarvis. Use it whenever a question needs whole files
rather than targeted reads.

- `--set speech` and `--set prompt` defined, briefs already written.
- `--files <paths> --brief "<question>"` for ad hoc.
- Model: `openrouter/nvidia/nemotron-3-ultra-550b-a55b:free`. Proven on a ~16.7k token
  bundle, 438 s.
- The 120B (`nemotron-3-super-120b-a12b:free`) did NOT read the bundle. One retry still
  owed to separate "did not attach" from "will not consume that size".

**STILL PENDING, NOT SUBMITTED: `CLOUDBUNDLE-speech-20260830-115352.md`** (approx 20,766
tokens), covering `speech_router.py`, `app.py`, `api_routes.py`. Brief asks for every
duplicated definition with CURRENT line numbers, a diff of the copies against each other,
which copy FastAPI routes to versus which one Python globals resolve to, and every case
where those two disagree. **Carried across FOUR windows now.**

**Staleness, updated again.** Built 08/30. Since then `app.py` moved in `f53a60d` (W23)
and `routes.py` in `aad8ccd` (W24). `imap_mail.py` moved in `611329e` (W25) but is not in
this bundle. **Rebuild before submitting. Do not submit the existing file.**

**Widening still recommended:** duplicated definitions are now a four-instance pattern
(speech triplication, the `auth_middleware.py`/`serve.py` bind verdict from W24). Consider
a general duplicated-definition sweep rather than a speech-only brief.

### 7.1 PowerShell idiom for a multi-line commit message - USE THIS, per section 2.5

Source, NOT a command to paste as-is. Adapt the text and run from the repo root. Writes
the message to `%TEMP%`, not the repo root, so it does not add to the untracked pile.

    $msg = @'
    subject line here

    body here
    '@
    $f = Join-Path $env:TEMP 'ojmsg.txt'
    $msg | Set-Content -Path $f -Encoding ascii
    git add <path>
    git commit -F $f
    Remove-Item $f

The closing `'@` must be at column zero. Never use a bash heredoc.

---

## 8. NEXT ACTIONS, ORDERED

1. **`mailbox_tools.py`** - THE LAST UNREAD DIFF. Front of the window, not the tail.
   Destructive paths. Full procedure including grep. Read section 3.2 of this handoff
   first and decide the `applied` / `failed_uids` / `store_failed` contract as part of
   the same piece of work - that is the Defect 1 result-contract question, and it is
   already open, so it is not a side investigation. Verify `requires_confirmation=True`
   at the spec while the file is open (section 6). Commit, then push both remotes.
   **This closes the unread-diff backlog entirely.**
2. **Architecture artifact** - ports, protocols, encoding at each gate, standalone
   downloadable file for the wiki. Owed FIVE windows. The stated reason for deferring it
   expires when item 1 lands. Seed it from section 5 of this handoff.
3. **Rebuild and feed `CLOUDBUNDLE-speech`** to the 550B. Rebuild mandatory - `app.py`
   has moved twice. Consider widening to a duplicated-definition sweep (section 7).
4. **Parser ordering audit** (W23 section 3.1). All four formats in one pass, precedence
   decided deliberately. Format 1's unanchored case-insensitive match shadowing Format 4
   XML is the specific live risk.
5. **Correct the memory record** on the tool timeout - 1800s for
   `mailbox_move_to_trash`, not 300s (section 2.4).
6. **Build and feed the second prompt bundle** - `InputArea.tsx`, `useSpeechStream.ts`,
   `MessageBubble.tsx`. Tests transcript accumulation, identifies the
   `jarvis-option-select` dispatcher.
7. **Repo root layout decision** - `scripts/`, `handoffs/`, `.gitignore`,
   `.gitattributes` for CRLF. The root now holds roughly 160 untracked files: every
   probe, patch, dump and handoff ever written. `mailbox_tools.py` throws a CRLF warning
   on every git command, which is noise that hides real warnings. Delete the stray
   `"patch_testexec_v1 .py"` WITH THE SPACE - note `patch_testexec_v1.py` (no space) is
   live and reads `app.state.bind_is_loopback`, so check which is which before deleting.
8. **One retry of the 120B** on a bundle, to separate attachment failure from size limit.
9. **Open item 6** - four managed-agent auto-approve sites on PATH 2. Largest outstanding
   confirmation-gate item, untouched for several windows.

---

## 9. STANDING RULES IN FORCE

- **START OF WINDOW: reconcile the handoff against HEAD before acting on it.**
  `git --no-pager log --oneline -5` plus a look for newer handoff files. (New, W25
  section 2.1.)
- ALWAYS VERIFY. Never stack a second change on an unverified first one.
- FINISH THE THING BEFORE STARTING THE NEXT. No dangling processes.
- State shell and host on every command. Default PowerShell on the Windows box; anything
  for the Ubuntu ollama host (172.16.33.200) must be labeled or PowerShell-wrapped ssh.
- Commands must run from `PS C:\Users\Admin\OpenJarvis>` as pasted. If a command needs a
  different path, say so IN THE REQUEST, before it runs. When a file is delivered for
  download, state where it lands and give the command that accounts for that location, in
  the same message.
- ONE runnable block per message. Quoted source goes inline or in a block labeled as
  source, never in a bare fence. (W24 section 2.3.)
- **Every runnable block must be valid in PowerShell 5.1 unless explicitly labeled for
  another shell. No heredocs, no `<<`, no `$(...)` substitution.** (New, W25 section 2.5.)
- No non-ASCII symbols in replies.
- Tests must be non-interactive - no test whose success depends on Gray reacting inside a
  time window.
- Pin the detail of every window including negative results.
- Push to both remotes, always. `origin` is GitHub, `gitlab` is
  `http://172.16.33.126/root/openjarvis-desktop.git`.
- Token conservation on working sessions.
- Flag at 15 exchanges, then hand off. A flag, not a stop - never cut a live trace.
- Every handoff carries the SDD/SDP section, the EXECUTION PATHS register, and the 550B
  cloud-model section.

## 10. USEFUL PATHS

- Backend log: `C:\Users\Admin\AppData\Local\OpenJarvis\logs\backend.log`
- Agent log: `%LOCALAPPDATA%\OpenJarvis\logs\agent.log` (2.5MB x4) - RUNSTART/TURN/RUNEND/RAWGEN
- Engine log: `%LOCALAPPDATA%\OpenJarvis\logs\engine.log` (2MB x2) - RETRY400, still at
  179 B, no line has ever fired
- Start: `.\start-openjarvis.ps1` from the repo root. The `.\` is MANDATORY - a stale copy
  in `C:\Windows\System32` is on PATH and shadows it.
- `BIND-ASSERT` line in the backend log, emitted by `record_bind` at startup -
  `host=`, `port=`, `loopback=`, `api_key_set=`. (W24.)
