# HANDOFF 2026-08-31 F / WINDOW 28
# H1's DEFINING FACT IS NOW READ, NOT ASSUMED. `applied = deleted > 0` CONFIRMED
# AT `imap_mail.py:647`.
# Plus: a SECOND failure mode was found and REPRODUCED - COPY succeeds, STORE
# fails, messages sit duplicated in Trash, and the tool reports success=False.
# No file was edited. No commit. Nothing is half-applied.

Predecessor: HANDOFF-2026-08-31-E-W27-H2-CLOSED-H1-OPENED.md
Host: Windows box. Shell: PowerShell 5.1. Working dir: `PS C:\Users\Admin\OpenJarvis>`.
Backend: 127.0.0.1:8010, ollama, qwen3-coder:30b, agent native_openhands.
Window shape: reconcile, four reads, one synthetic harness built and run.
Backend never started. Zero writes to the mailbox. Zero network calls. No commit.

---

## 0. ONE PARAGRAPH FOR THE NEXT WINDOW

H1 next-action item 1 is DONE. `move_to_trash` was read to its end - it terminates
at `imap_mail.py:653` with the `finally` at 654-655 - and `applied = deleted > 0`
is now READ at `:647`. The W25 claim was correct, but the read plus a harness
exposed that it is correct for the wrong reason and hides a second defect. A
non-interactive stubbed-IMAP harness (`probe_h1_store_v1.py`, repo root,
UNTRACKED) exercised the real body of `move_to_trash` across four scenarios and
reproduced both failure modes in one run. **H1-B (partial COPY, reports
success=True) is confirmed. H1-C is NEW: COPY succeeds, every STORE fails,
`applied` is False, the tool reports success=False - and the messages are already
sitting in Trash. A retry duplicates them again.** The result contract at
`mailbox_tools.py:689` is now decidable on reproduced evidence; it was not started,
deliberately, at exchange 10. Nothing edited, nothing to roll back, clean seam.

---

## 1. WHAT LANDED

Nothing was committed. HEAD is unchanged at `801869c`.

One new untracked file in the repo root: `probe_h1_store_v1.py`, marker
`openjarvis-h1-store-probe-v1`. Its disposition is an open decision - see item 3
in section 8.

### 1.0 Start-of-window reconcile - PASSED

Per the standing rule. `git --no-pager log --oneline -1 --decorate` returned:

    801869c (HEAD -> main, origin/main, origin/HEAD, gitlab/main, gitlab/HEAD)
    mailbox_tools: scope sender lookup to the target folder (openjarvis-h2-folder-scope-v1)

Both remotes on HEAD. Newest handoff on disk was the W27 `-E-` file. Handoff and
repository agreed; nothing had drifted. Third consecutive window where this check
was cheap and confirming.

Note the branch is `main`, not `master`. Earlier handoffs hedged on this. READ now.

---

## 2. H1 - THE READ THAT CLOSES THE ASSUMPTION

### 2.1 `move_to_trash` ends at 653

READ `imap_mail.py:626-695`. The function body runs 537-653; `finally:
self._close(imap)` is 654-655; `_imap_text` starts at 657. **There is no further
code belonging to `move_to_trash`.** The three-window search for where `applied`
is assigned is over.

### 2.2 The tail, in full - all READ

- `:626-627` - `plan["copied_count"] = len(copied)`, `plan["failed_uids"] = failed`.
  **`failed_uids` is set UNCONDITIONALLY**, so it is present even when empty.
- `:628-629` - `copy_errors` only when `errors` is non-empty, truncated to 10.
- `:631-633` - if `copied` is empty: `plan["error"] = "COPY to %r failed for all
  uids"`, return. `applied` stays False from the 568 seed.
- `:635-643` - the STORE loop. Iterates **`copied` only**, in `chunk_size` slices.
  `imap.uid("STORE", ",".join(sub), "+FLAGS", "(\\Deleted)")`. On `typ == "OK"`,
  `deleted += len(sub)`. Otherwise `plan.setdefault("store_failed", []).extend(sub)`.
  **`store_failed` is set only on failure** - absent from the dict in the happy path.
- `:645` - `imap.expunge()`. **Return value never checked.**
- `:646-647` - `plan["deleted_count"] = deleted`, **`plan["applied"] = deleted > 0`**.
- `:648-652` - if `failed`, a `note` naming how many uids were left in place.
- `:653` - return.

### 2.3 What `applied` actually means - and it is weaker than the claim implied

`applied = deleted > 0` is READ and correct. But `deleted` is **chunk-granular,
not uid-granular**: `deleted += len(sub)` credits the whole slice when the chunk's
STORE returns OK. And `expunge()` is fired blind at 645.

Therefore `applied: True` means precisely: **at least one STORE chunk returned OK.**
It does NOT mean the COPY set was complete, it does NOT mean every uid was flagged,
and it does NOT mean the expunge succeeded. Three separate gaps behind one boolean.

This is the correction that matters for the SDP. The carried claim was not wrong,
it was *underspecified*, and an H1 fix written against "applied = deleted > 0" as a
sufficient description would have reproduced the same conflation one layer up.

### 2.4 Asymmetry that any contract must handle

| Key | When present | Set at |
|---|---|---|
| `failed_uids` | ALWAYS, empty list when clean | `:627` unconditional |
| `store_failed` | ONLY when a STORE chunk fails | `:642` via `setdefault` |
| `copy_errors` | only when `errors` non-empty | `:629` |
| `note` | only when `failed` non-empty | `:649` |
| `deleted_count` | only past the 633 early return | `:646` |

A consumer that does `result.get("store_failed", [])` is fine; one that assumes
symmetry with `failed_uids` and does `result["store_failed"]` raises on the happy
path. OBSERVED across all four scenarios.

---

## 3. THE HARNESS - DESIGN, AND WHY THIS SHAPE

`probe_h1_store_v1.py`, repo root, untracked, stdlib only.

**Why synthetic and not live.** To reach the STORE loop at 635 the code must first
complete the COPY at 597-608, which writes real messages into Trash on the Yahoo
account before the mechanism under test even begins. And a STORE failure cannot be
induced on demand against a real server. A live probe would therefore have been
destructive AND non-discriminating. This is the W27 2.3 lesson applied at design
time rather than discovered afterwards.

**What is real:** the entire body of `move_to_trash`, 560-653, unmodified.
**What is faked:** only the object returned by `self._connect()`.

Enablers, all established by reading first:

- `__init__` (`:168-197`) has a default for **every** parameter, so
  `ImapMailConnector(provider="yahoo", account_id="harness")` constructs with no
  credentials and touches only the `PROVIDERS` table. No config file, no network.
- `_connect` is patched **on the instance**, not on the class or the module.
- `pause_s=0.0` is passed as a **real parameter**. `time.sleep` was NOT patched.
  Untouched, the retry ladder at 601-608 sleeps 1+2+4+8 s per failing chunk.
- `_close` (`:273-278`) is a staticmethod that swallows everything, so the fake
  needs only `logout()`.

Stub surface, complete: `select(quoted, readonly=False)`, `uid("COPY", uid_set,
qtrash)`, `uid("STORE", uid_set, "+FLAGS", "(\\Deleted)")`, `expunge()`, `logout()`.

**The harness reports what the fake server was ASKED to do alongside the plan
dict.** That is the whole point - the divergence in scenario C is only visible by
comparing the two, and a harness that printed the plan dict alone would have
reported "applied: False" and looked like a clean no-op.

12 uids at `chunk_size=10` gives two chunks, so chunking and the 623-624
inter-chunk path both execute. Non-interactive, runs to completion, no reaction
from Gray required.

---

## 4. THE FOUR SCENARIOS - OBSERVED

    A  COPY ok, STORE ok       applied=True   copied=12 deleted=12 failed=[]
    B  COPY partial, STORE ok  applied=True   copied=11 deleted=11 failed=['7']
    C  COPY ok, STORE all NO   applied=False  copied=12 deleted=0  store_failed=all 12
    D  COPY all fail           applied=False  copied=0  early return at 633

### 4.1 The state table - four truths, two booleans

| | copied | deleted | Ground truth | `success` today |
|---|---|---|---|---|
| A | all | all | done | True |
| B | some | some | partly done, remainder still in source | **True** |
| C | all | 0 | **duplicated into Trash, nothing removed** | **False** |
| D | 0 | 0 | nothing happened, mailbox clean | False |

**B and C are both lies. C is the dangerous one.**

### 4.2 H1-B - CONFIRMED, as W26 described it from reading

`failed_uids=['7']` and the note "1 uid(s) could not be copied and were left in
place" are both in the dict and both reach the model inside `content`. But
`success=True`, and `success` is what the agent reasons over. The model accurately
reports an inaccurate result. Exactly the W26 formulation, now OBSERVED.

### 4.3 H1-C - NEW THIS WINDOW, AND NOT PREVIOUSLY ON THE BOARD

    *** DIVERGENCE: 12 message(s) copied into trash while the tool reports success=False

`copied` is non-empty so the 631 early return does not fire. Every STORE returns
NO. `deleted` stays 0, `applied` is False, `mailbox_tools.py:689` yields
`success=False`, and the agent reports that nothing happened.

**The messages are already in Trash.** The source folder still has them. The user
is told the operation failed. **The natural response to that report is to retry,
which copies them a second time.** A false negative with a live, accumulating side
effect.

Severity argument: H1-B silently under-delivers, which is bad. H1-C actively
invites the user to duplicate mail, at volume, on a path the folder-consolidation
work (W27 section 4) is about to drive across 53 folders. **H1-C should be treated
as the higher severity of the two.**

### 4.4 Three things the harness produced that reading did not

1. **`deleted_count` is chunk-granular** (2.3). Visible only by comparing the
   STORE calls issued against `deleted_count`.
2. **`expunge()` runs even when every STORE failed.** Scenario C called expunge on
   a folder with nothing flagged. Harmless in itself, but **expunge having been
   called is not evidence that anything was removed** - do not use it as one.
3. **`_close` runs on the early returns.** `logout: True` in all four scenarios
   including D, which returns at 633 from inside the `try`. Correct behavior, now
   OBSERVED rather than assumed.

### 4.5 What this test BYPASSED - per the W27 2.5 rule

State it explicitly so no future window inherits false coverage:

- **`mailbox_tools.py` was NOT executed.** The harness calls the connector
  directly. `MailboxMoveToTrashTool.execute`, the `CONFIRM DELETE` interlock, the
  provenance fields at 678-684, and `success=bool(...)` at 689 were all bypassed.
  The `success` column in 4.1 is computed by the harness from `applied`, not
  observed from the tool layer.
- **`openjarvis-protected-senders-v1` STILL never exercised.** Second consecutive
  window it was bypassed rather than covered. Unchanged from W27 2.5.
- **No real IMAP server was involved.** Server-side behaviors - partial STORE
  within an OK chunk, expunge failures, Yahoo quirks - are outside what this can
  show. The harness proves what the CODE does with given server responses, not
  which responses a real server gives.
- **`folder == trash` (`:591-592`) was not exercised.** That branch sets
  `copied = list(uids)` with no COPY at all. Untested.
- **The COPY retry ladder ran with `pause_s=0.0`.** Timing behavior under real
  latency is not covered.

---

## 5. EXECUTION PATHS REGISTER

Standing structure. Carried forward and extended, not re-derived.

### PATHS ALREADY REGISTERED (unchanged this window)

- PATH 1: orchestrator `ask()` via `system\orchestrator.py`
- PATH 2: managed-agent SSE via `_stream_managed_agent()` in
  `server\agent_manager_routes.py` (four auto-approve sites, open item - still the
  largest outstanding gate item)
- PATH 3: test-execute via `POST /v1/tools/test-execute` - gate LIVE, `confirm_id`
  verified on the wire (W21). The only path proven end to end.
- `routes.py` chat dispatch 1a/1b/1c/1d - non-streaming branches offloaded to
  `asyncio.to_thread` as of `aad8ccd`
- Frontend submit F-A typed, F-B voice, F-C option relay (DEAD - no handler for
  `jarvis-submit-text`)
- `_extract_tool_call` order: native, Format 1 (case-insensitive, UNANCHORED),
  Format 2 (unread), Format 4 (XML, shadowed by 1), Format 3 (bare JSON).
  Precedence is an accident of insertion order.

### EXTENDED THIS WINDOW - destructive mailbox path, execution stage

Sender-resolution stage rows from W27 are unchanged and still valid. New and
revised rows:

| Property | Value | Evidence |
|---|---|---|
| Function extent | `imap_mail.py:537-653`, `finally` 654-655 | **READ (was open)** |
| `applied` definition | `:647` `plan["applied"] = deleted > 0` | **READ (was ASSUMED)** |
| `deleted` granularity | chunk-level; `deleted += len(sub)` on chunk OK | READ + OBSERVED |
| STORE loop domain | iterates `copied` only, never `uids` | READ |
| `expunge` | `:645`, unconditional, **return ignored** | READ + OBSERVED |
| `failed_uids` presence | `:627` UNCONDITIONAL, empty list when clean | READ + OBSERVED |
| `store_failed` presence | `:642` `setdefault`, ABSENT when clean | READ + OBSERVED |
| Early return, no COPY | `:631-633`, `applied` False, clean mailbox | OBSERVED (D) |
| Partial COPY | `applied` **True**, `failed_uids` populated | OBSERVED (B) |
| STORE total failure | `applied` **False**, messages ALREADY in trash | **OBSERVED (C) - NEW** |
| Teardown on early return | `_close` runs; `logout` observed in all 4 | OBSERVED |
| `folder == trash` branch | `:591-592`, no COPY issued | READ, **never exercised** |
| Result contract | `mailbox_tools.py:689` `success=bool(applied)` | READ, **not executed this window** |
| Protected senders | `mailbox_tools.py:566-589` | READ, **never exercised, 2 windows** |
| Test harness | `probe_h1_store_v1.py`, stubbed IMAP, 4 scenarios | OBSERVED |

---

## 6. SDP / SDD FEED

**H1 must now be recorded as TWO defects, not one.** Every prior artifact treats
H1 as the partial-move over-report. That is H1-B. H1-C is a distinct failure with
the opposite sign and a live side effect, and it shares only the root cause.

Root cause, stated once for the SDP: **a four-state outcome is projected onto a
one-bit result.** The connector computes and preserves everything needed to tell
the four states apart - `copied_count`, `deleted_count`, `failed_uids`,
`store_failed` - and `mailbox_tools.py:689` discards all of it in favor of
`bool(applied)`. The fix is at the tool layer; the connector needs no change for
correctness of reporting. (`deleted` being chunk-granular is a separate, smaller
accuracy issue inside the connector.)

**Correct the carried claim, do not just mark it READ.** `applied = deleted > 0`
is confirmed at `:647`, but the SDP must state what it means: at least one STORE
chunk returned OK. Not "the move succeeded". Three gaps hide behind it - COPY
completeness, per-uid STORE truth within an OK chunk, and expunge outcome. An
artifact that records only "applied = deleted > 0, READ" carries the same
underspecification that cost this project three windows.

**Destructive-path chapter now needs three directions of failure, not two.** W27
added the false negative (declines to act, reports empty). Add: **acts partially
and reports success** (H1-B), and **acts destructively-then-incompletely and
reports failure** (H1-C). "Could it delete too much" remains the least of them.

**Carried correction, STILL OWED, unchanged.** SDP revB:504 and revC:597 assert
`requires_confirmation=True` for `mailbox_move_to_trash`. Both WRONG (W26 2.1).
Replace with: the flag is deliberately unset, the reason is in the
`mailbox_tools.py` header, the interlock is `dry_run=False` plus the exact
`CONFIRM DELETE` token, and the stated premise predates 6c and is untested. Do not
simply flip the boolean - carry the reasoning.

**Defect 6 confirmation gate - GREAT DETAIL per Gray's standing instruction.**
Unchanged from W26/W27. Registry: write-once, 409 on re-decision, TIMEOUT internal
only. Payload: seven fields; `turn_id` from `CURRENT_TURN_ID` set by
`openjarvis-agent-log-v1` - a diagnostic marker load-bearing on a safety-critical
payload, still a design smell needing its own owner. Transport: EventBus ->
ws_bridge -> bare WS client; delivery proven W20, payload integrity W21. Redaction
CLOSED. TTL 120 s governs the WAIT FOR A HUMAN, not the execution that follows. The
mailbox path does not use this gate at all; PATH 3 remains the only end-to-end proof.

**Defect 1 - keep the two mechanisms separate.** (a) The model claims actions it
never invoked: parser and prompt problem. (b) The tool mis-reports and the model
accurately relays it - now split into H1-B and H1-C. No confabulation in either.

**Verification methodology chapter - three new entries (running total thirteen):**

11. **When the mechanism cannot be reached without a destructive side effect,
    stub the boundary rather than accept the side effect.** Reaching the STORE
    loop live requires writing real messages into Trash first. Patching
    `_connect` on the instance kept 560-653 real while making the test free.
12. **Print what the collaborator was ASKED to do, not only what the function
    returned.** Scenario C's divergence is invisible in the plan dict alone - it
    reads as a clean `applied: False`. The harness caught it only because it also
    reported the COPY calls the fake received.
13. **Prefer a real parameter over a patched global.** `pause_s=0.0` beat patching
    `time.sleep`: fewer moving parts, and the code under test stayed byte-identical.

**Architecture artifact.** `OPENJARVIS-ARCH-GATES-2026-08-31-v1.md`, repo root,
untracked, cut at `6c172d1`, still one commit stale (`801869c` changed the
sender-resolution row). Next version must also add the H1-B / H1-C split and the
result-contract row.

---

## 7. 550B CLOUD MODEL

Carried forward per the 08/29 pin. **Untouched this window** - every question was
answerable with targeted reads, and the H1 read that had cost three windows closed
in one.

`bundle_for_cloud.py` in the repo root, marker `openjarvis-cloudbundle-v1`.
Read-only, stdlib only, does not import openjarvis. Use it whenever a question
needs whole files rather than targeted reads.

- `--set speech` and `--set prompt` defined, briefs already written.
- `--files <paths> --brief "<question>"` for ad hoc.
- Model: `openrouter/nvidia/nemotron-3-ultra-550b-a55b:free`. Proven on a ~16.7k
  token bundle, 438 s.
- The 120B (`nemotron-3-super-120b-a12b:free`) did NOT read the bundle. One retry
  still owed, to separate "did not attach" from "will not consume that size".

**STILL PENDING, NOT SUBMITTED: `CLOUDBUNDLE-speech-20260830-115352.md`** (approx
20,766 tokens), covering `speech_router.py`, `app.py`, `api_routes.py`. Brief asks
for every duplicated definition with CURRENT line numbers, a diff of the copies
against each other, which copy FastAPI routes to versus which one Python globals
resolve to, and every case where those two disagree. **Carried across SEVEN windows.**

**Staleness.** Built 08/30. `app.py` moved in `f53a60d` (W23), `routes.py` in
`aad8ccd` (W24), `imap_mail.py` in `611329e` (W25), `mailbox_tools.py` in `6c172d1`
(W26) and `801869c` (W27). **Rebuild before submitting. Do not submit the existing file.**

**Widening still recommended:** duplicated definitions are a four-instance pattern
(speech triplication, the `auth_middleware.py` / `serve.py` bind verdict). Consider
a general duplicated-definition sweep rather than a speech-only brief.

**The H1 candidate bundle from W27 is now WITHDRAWN.** It proposed bundling
`imap_mail.py` plus `mailbox_tools.py` to trace `applied`. Both are now READ; the
bundle would be spend for nothing. Do not carry it forward.

---

## 8. NEXT ACTIONS, ORDERED

1. **H1 - decide the result contract at `mailbox_tools.py:689`.** Now decidable on
   reproduced evidence (4.1). Four states, currently two booleans. Required: B must
   not report unqualified success; **C must surface that messages were copied and
   not removed**, because the natural retry duplicates them. Highest-severity open
   item on the destructive path and a hard prerequisite for item 5. Design
   consideration: the four states are distinguishable from `copied_count`,
   `deleted_count`, `failed_uids` and `store_failed`, all already in the dict - see
   the presence asymmetry in 2.4 before writing the accessor.
2. **Extend the harness to the tool layer.** It currently stops at the connector
   (4.5). Once the contract is written, the same four scenarios must run through
   `MailboxMoveToTrashTool.execute` so `success` is OBSERVED, not computed by the
   harness. This is the verification for item 1 and should be built with it.
3. **Decide the disposition of `probe_h1_store_v1.py`.** Untracked in the repo
   root, adding to the roughly 160-file pile. It is the only executable regression
   test for the destructive path that exists. Commit it (and where - `scripts/`,
   `tests/`?) or delete it deliberately. Do not leave it drifting.
4. **Exercise `openjarvis-protected-senders-v1`.** Bypassed two windows running.
   Needs a non-interactive dry-run through `MailboxMoveToTrashTool.execute` -
   not a direct connector call - against a protected sender, asserting the block
   report is populated and nothing is selected. Item 2's harness is the natural
   vehicle.
5. **Yahoo folder consolidation, 53 to 18-19** (W27 section 4). Gated on items 1-2,
   and the gate is now firmer: H1-C means a failed consolidation fold can duplicate
   mail into Trash while reporting failure. Mapping table first, dry run per source
   folder, no bulk operation. Watch `AT&-T` (modified-UTF7 leaking through) and the
   near-duplicate pairs `Draft`/`Drafts`, `Social`/`Social_Media`,
   `Receipts_Confirmations`/`Inbox/Receipts`, `Junk`/`Spam`/`Bulk`.
6. **`deleted_count` chunk-granularity** (2.3). Smaller, connector-side, real. A
   chunk STORE returning OK credits all its uids. Decide whether to leave it
   documented or make it uid-accurate.
7. **Retest the W26 2.1 premise** - does the confirm callback now reach the mailbox
   path after 6c? Decides whether `requires_confirmation` can be set at all. Until
   answered, the SDP correction carries the caveat, not a verdict.
8. **Rebuild and feed `CLOUDBUNDLE-speech`** to the 550B. Rebuild mandatory - five
   files have moved. Consider widening to a duplicated-definition sweep.
9. **Parser ordering audit** (W23 3.1). All four formats in one pass, precedence
   decided deliberately. Format 1's unanchored case-insensitive match shadowing
   Format 4 XML is the live risk. Format 2 still unread.
10. **PATH 2's four managed-agent auto-approve sites.** Largest outstanding
    confirmation-gate item, untouched for several windows.
11. **Refresh the architecture artifact** - one commit stale, plus the H1-B/H1-C
    split and the result-contract row (section 6).
12. **Repo root layout decision** - `scripts/`, `handoffs/`, `.gitignore`,
    `.gitattributes` for CRLF. Roughly 160 untracked files, now 161. `mailbox_tools.py`
    throws a CRLF warning on every git command, noise that hides real warnings.
    Delete the stray `"patch_testexec_v1 .py"` WITH THE SPACE - `patch_testexec_v1.py`
    (no space) is live and reads `app.state.bind_is_loopback`, so check which is which first.
13. **Second prompt bundle** - `InputArea.tsx`, `useSpeechStream.ts`,
    `MessageBubble.tsx`. Tests transcript accumulation, identifies the
    `jarvis-option-select` dispatcher.
14. **One retry of the 120B** on a bundle, to separate attachment failure from size limit.
15. **Lab item, not OpenJarvis:** the GitLab remote is plaintext HTTP, port 80, no
    TLS. Belongs with the Zero Trust work.

---

## 9. STANDING RULES IN FORCE

- **START OF WINDOW: reconcile the handoff against HEAD before acting on it.**
  `git --no-pager log --oneline -1 --decorate` plus a look for newer handoff files.
  (W25 2.1; cheap and confirming in W26, W27 and again in W28.) Branch is `main`.
- ALWAYS VERIFY. Never stack a second change on an unverified first one.
- FINISH THE THING BEFORE STARTING THE NEXT. No dangling processes. **W28 stopped
  at the contract decision rather than start an edit at exchange 10.**
- Take counts from the `N insertions(+), M deletions(-)` line, NEVER the `--stat`
  graph column. Four misreads on record.
- **Read the mechanism before naming the severity.** (W26 2.2.)
- **Mark evidence quality: READ / OBSERVED / ASSUMED.** (W26 section 3.) **And when
  an assumption is promoted to READ, state what it MEANS, not just that it was
  confirmed.** (New, W28 2.3.)
- **A test derived from the call site rather than the mechanism cannot fail.**
  Check that a proposed test is capable of producing a negative. (W27 2.3.)
- **Record what a test BYPASSED, not only what it covered.** (W27 2.5.)
- **Print what the collaborator was asked to do, not only what the function
  returned.** (New, W28.)
- State shell and host on every command. Default PowerShell 5.1 on the Windows box;
  anything for the Ubuntu ollama host (172.16.33.200) must be labeled or
  PowerShell-wrapped ssh.
- Commands must run from `PS C:\Users\Admin\OpenJarvis>` as pasted. If a command
  needs a different path, say so IN THE REQUEST, before it runs. When a file is
  delivered for download, state where it lands and give the command that accounts
  for that location, in the same message.
- ONE runnable block per message. Quoted source inline or labeled as source.
- **Every runnable block must be valid in PowerShell 5.1 unless explicitly labeled
  for another shell. No heredocs, no `<<`, no `$(...)` substitution.**
- No non-ASCII symbols in replies.
- Tests must be non-interactive - no test whose success depends on Gray reacting
  inside a time window.
- Pin the detail of every window including negative results.
- Push to both remotes, always. `origin` is GitHub, `gitlab` is
  `http://172.16.33.126/root/openjarvis-desktop.git`.
- Token conservation on working sessions.
- Flag at 15 exchanges, then hand off. A flag, not a stop - never cut a live trace.
- Every handoff carries the SDD/SDP section, the EXECUTION PATHS register, and the
  550B cloud-model section.

## 10. USEFUL PATHS

- Backend log: `C:\Users\Admin\AppData\Local\OpenJarvis\logs\backend.log`
- Agent log: `%LOCALAPPDATA%\OpenJarvis\logs\agent.log` (2.5MB x4) -
  RUNSTART/TURN/RUNEND/RAWGEN
- Engine log: `%LOCALAPPDATA%\OpenJarvis\logs\engine.log` (2MB x2) - RETRY400,
  still at 179 B, no line has ever fired
- Start: `.\start-openjarvis.ps1` from the repo root. The `.\` is MANDATORY - a
  stale copy in `C:\Windows\System32` is on PATH and shadows it.
- `BIND-ASSERT` line in the backend log, emitted by `record_bind` at startup.
- Architecture artifact: `OPENJARVIS-ARCH-GATES-2026-08-31-v1.md`, repo root,
  untracked, one commit stale.
- H1 harness: `probe_h1_store_v1.py`, repo root, untracked. Run with
  `python .\probe_h1_store_v1.py`. No network, no mailbox writes.
- **No rollback point needed for W28 - nothing was edited.** Last rollback of
  record: `git revert 801869c`, or
  `git checkout 6c172d1 -- src\openjarvis\tools\mailbox_tools.py`.
