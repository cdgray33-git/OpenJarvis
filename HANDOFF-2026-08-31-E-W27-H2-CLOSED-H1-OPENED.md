# HANDOFF 2026-08-31 E / WINDOW 27
# H2 IS CLOSED - REPRODUCED, FIXED, VERIFIED IN ISOLATION, PUSHED TO BOTH REMOTES.
# Plus: my FIRST probe was non-discriminating and is pinned as a negative result,
# the protected-sender blocklist is NOT covered by anything run here, and H1 is
# read to `imap_mail.py:626` with `applied` still ASSUMED, never READ.

Predecessor: HANDOFF-2026-08-31-D-W26-BACKLOG-CLOSED-ARCH-ARTIFACT-BUILT.md
Host: Windows box. Shell: PowerShell 5.1. Working dir: `PS C:\Users\Admin\OpenJarvis>`.
Backend: 127.0.0.1:8010, ollama, qwen3-coder:30b, agent native_openhands.
Window shape: one read-first patch, one commit (`801869c`), pushed to both
remotes. Backend never started. No runtime debugging. Two read-only IMAP probes,
zero writes to the mailbox.

---

## 0. ONE PARAGRAPH FOR THE NEXT WINDOW

Backlog item 1 is DONE. `folder=folder` was added to the sender lookup at
`mailbox_tools.py:546`, committed as `801869c`, and both remotes are verified at
that hash. **The false negative was reproduced live before the fix and shown
closed after it, in one run, with the keyword as the only variable.** Working
tree is blank and the backup has been removed - git history is the rollback point
now. H1 was opened read-only and NOT touched: `mailbox_tools.py:689` is confirmed
as `success=bool(result.get("applied"))`, and `move_to_trash` is read down to
line 626, which is where `copied_count` is set. **`applied`, `failed_uids` and
`store_failed` all live past 626 and are still unread - the `applied = deleted > 0`
claim carried since W25 remains ASSUMED.** One read finishes it and it is item 1.
Nothing is half-applied; this is a clean seam.

---

## 1. WHAT LANDED

| Hash | Content | Counts | Verified by |
|---|---|---|---|
| `801869c` | `mailbox_tools.py` - scope sender lookup to the target folder | 1 ins, 1 del | `git commit` summary line |

Pushed `6c172d1..801869c` to `origin` AND `gitlab`. Plain fast-forward, identical
object counts (6 objects, 1.32 KiB) to both. No `--mirror`, no `--force`. Both
remotes verified sitting on `801869c` by `git --no-pager log --oneline -1
--decorate` **in the same exchange as the push**, per the W26 practice.

Counts taken from the `1 file changed, 1 insertion(+), 1 deletion(-)` summary
line. The `--stat` graph column was not used. Five windows of misreads on record;
the rule held this time.

### 1.1 The change, in full

`src\openjarvis\tools\mailbox_tools.py:546`, marker `openjarvis-h2-folder-scope-v1`:

    -  _hits = conn.find_messages(from_addr=_from_addr, limit=5000)
    +  _hits = conn.find_messages(folder=folder, from_addr=_from_addr, limit=5000)

One line. Nothing else in the file was touched.

---

## 2. H2 - THE EVIDENCE CHAIN, END TO END

### 2.1 The mechanism, confirmed by reading before any edit

Four reads, all this window, all marked READ:

- `mailbox_tools.py:519` - `folder = str(params.get("folder", "") or "")`. The
  variable exists in scope at 546.
- `mailbox_tools.py:539-544` - `if not folder: return ... "folder is required
  when using from_addr"`. **`folder` cannot be empty at line 546.** This matters:
  if it could be, `folder=folder` would pass `""` and `folders = [folder] if
  folder else ...` would silently fall back to the full scan. The guard makes the
  fix unconditional.
- `imap_mail.py:497` - `folders = [folder] if folder else self._target_folders(imap, for_usage=True)`.
- `imap_mail.py:527-528` - `if len(hits) >= limit: return hits`, **inside the
  per-folder `for name in folders:` loop.** This is the whole defect.

### 2.2 The equivalence claim, closed at the source

W26 asserted selection semantics are identical. That claim had one unverified
link: the filters compare `_h["folder"]` to the caller's string, but `folder` on
each hit is set from `row["folder"]`, which comes out of `_fetch_summaries` - not
from `name` directly. If that function normalized the name (case, quoting), the
fix would be a WIDENING on a delete path, not a restriction.

Read and closed:

- `imap_mail.py:336` - `imap.select(_quote_folder(folder), readonly=True)`. The
  quoting happens **at the select call only**. The parameter itself is untouched.
- `imap_mail.py:377` - `"folder": folder`. The parameter **echoed verbatim** into
  every summary row. No normalization anywhere.
- `mailbox_tools.py:558` and `:584` - both filters use `!= folder` exact string
  equality.

Therefore: before the change, `row["folder"]` was a server-supplied name from
`_target_folders`, and the filter only ever kept rows whose server name already
equaled the caller's string. After the change, `folders = [folder]` and
`row["folder"]` IS the caller's string, so the filter matches trivially. **The
surviving set is the same either way.** Scan restriction, not a behavior change.
Established by reading, then confirmed empirically in 2.3.

### 2.3 PROBE 1 - NON-DISCRIMINATING. PIN THIS AS A NEGATIVE RESULT.

Target `bestie` (last of 53 folders in `_target_folders` order), sender
`angela.winder89@gmail.com`, `limit=5000`.

    OLD  total: 86   in target: 86   secs: 113.7
    NEW  total: 86   in target: 86   secs: 3.0

**This proved nothing about H2.** Only 86 hits existed against a cap of 5000, so
`if len(hits) >= limit` never fired and the early return never executed. The
mechanism under test was never exercised. I designed a test that could not fail.

That is the W26 rule - *read the mechanism before naming the severity* - turned on
my own test design, and it is worth pinning in that form: **a test built from the
call site rather than the cap semantics will pass regardless of whether the defect
exists.** The discriminating variable was never the folder's position in the
order; it was whether the cap fills before that folder opens.

What Probe 1 did legitimately establish, and both are keepers:

1. **Equivalence, empirically.** 86 rows identical either way, corroborating 2.2.
2. **The scan restriction is real and large.** 113.7 s to 3.0 s, a ~38x cut,
   across a 53-folder account. Every sender-scoped move gets that back.

### 2.4 PROBE 2 - DISCRIMINATING. H2 REPRODUCED AND CLOSED.

Same account. Discovery walked folders for a sender present in both an early
folder and the target, then used `limit=5` so the cap fills immediately. The
`return`-inside-loop semantics are limit-relative, so a small limit exercises the
identical code path that 5000 would.

    SENDER: cdgray33@yahoo.com | EARLY FOLDER: Draft count 49 | TARGET: bestie
    OLD  total: 5  in target: 0  folders touched: ['Archive', 'Divorce Recordings', 'Draft']
    NEW  total: 5  in target: 5

OLD filled its cap inside Archive / Divorce Recordings / Draft and returned.
**`bestie` was never opened.** At the tool layer that becomes `"no messages
matched"` with `success=False` for a folder the code never looked at - a
confident false negative on a delete path, exactly as W26 described it from
reading alone.

Same sender, same limit, same run, same process. The keyword was the only
variable. **This is the isolation requirement satisfied.**

Both probes were read-only, non-interactive, ran to completion without any
reaction from Gray, and called `find_messages` only. **No writes to the mailbox
at any point.**

### 2.5 COVERAGE GAP - do not mistake Probe 2 for more than it is

The sender the discovery step landed on was `cdgray33@yahoo.com`, which is on the
`openjarvis-protected-senders-v1` blocklist (it is in the `_defaults` list at
`mailbox_tools.py:566-570`).

Nothing was at risk - the probe calls `conn.find_messages` directly and never
enters `MailboxMoveToTrashTool.execute`, so it never reaches the blocklist filter
at 580-589 and never reaches `move_to_trash`. But it means:

**`openjarvis-protected-senders-v1` HAS NEVER BEEN EXERCISED BY ANY TEST.** Not
this window, not previously on record. It is READ but not OBSERVED. A future
window must not read "we tested with a protected sender and it was fine" out of
this handoff. It was not tested. It was bypassed.

---

## 3. H1 - OPENED, READ-ONLY, NOT TOUCHED

The highest-severity open item on the destructive path. Read this window; no edit
proposed, because the defining fact is still unread.

### 3.1 The tool layer - CONFIRMED, and narrower than the backlog stated

`mailbox_tools.py`, READ 650-690:

- `:658-663` - guard: `folder` and a non-empty `uids` required.
- `:665-668` - `if not _confirmed(params): plan = conn.move_to_trash(folder, uids,
  dry_run=True)` then `_needs_confirmation_result`. This is the bespoke interlock,
  not the Defect 6 gate. Consistent with W26 section 2.1.
- `:669` - `result = conn.move_to_trash(folder, uids, dry_run=False)`. Live call.
- `:678-684` - if `_resolved`, the dict is copied and **provenance fields are
  ADDED**: `selected_by`, `protected_blocked`, `from_addr`, `resolved_uid_count`.
  Nothing is reconciled. Nothing is removed.
- **`:689` - `success=bool(result.get("applied"))`.**

`result` is passed whole to `_dump`, so if the connector emits `failed_uids` or
`store_failed` they DO reach the model inside `content`. But `success` is already
`True`, and `success` is what the agent reasons over. The model then accurately
reports an inaccurate result - the W26 formulation holds exactly.

### 3.2 The connector - READ to line 626, and it reframes the problem

`imap_mail.py`, `move_to_trash` at `:537`, READ 537-626:

- Signature `:537-546`: `chunk_size=10, pause_s=1.0, max_retries=4`, returns `Dict[str, Any]`.
- `:560-569` - a **single mutable `plan` dict**, with `"applied": False` seeded at 568.
- **Six exit points return that same dict.** `:572` no uids, `:575` dry run,
  `:579` no connection, `:584` cannot select folder for writing, plus the tail
  past 626. Every early return carries `applied: False`.
- `:587-589` - `copied = []`, `failed = []`, `errors = []`. **The data exists.**
- `:591-592` - if `folder == trash`, `copied = list(uids)` with no COPY at all.
- `:597-608` - chunked UID COPY, `max_retries` with exponential backoff, IMAP
  error text accumulated into `errors`.
- `:615-622` - **the degrade path.** On a persistently failing chunk it retries
  each uid individually; successes go to `copied`, failures to `failed` with their
  error text. This is the `611329e` work.
- `:626` - `plan["copied_count"] = len(copied)`.

**Consequence for H1, and this is the correction:** the contract is not uniformly
broken. Because `applied` is seeded `False` and every early return preserves it,
`success=bool(result.get("applied"))` is CORRECT for the no-uids, dry-run,
no-connection and unselectable-folder cases. The defect is narrower and lives
entirely in the partial-success case.

**And the connector already separates COPY success from failure at the uid level.**
`copied` and `failed` are both populated. So H1 is not "the data is missing" - the
data is there and the tool layer discards it.

### 3.3 What is STILL UNREAD, and must not be asserted

`applied`, `failed_uids` and `store_failed` are all assigned **past line 626**.
Never read. The claim `applied = deleted > 0`, carried since W25, is **ASSUMED,
not READ.** Do not repeat it as fact. Two SDP revisions already carried an
unmarked assumption as fact (W26 2.1) and that is the most expensive mistake this
project keeps making.

The sharpened question for the next window: **which of `copied`, `failed` and the
STORE/EXPUNGE outcome feed `applied`, and why does the tool layer surface none of
the other two in `success`?**

Next read, first thing, PowerShell 5.1 from the repo root:

    $g = 'src\openjarvis\connectors\imap_mail.py'
    Get-Content $g | Select-Object -Skip 625 -First 70 | ForEach-Object -Begin {$i=626} -Process { '{0,4}: {1}' -f $i, $_; $i++ }

---

## 4. NEW BACKLOG ITEM - YAHOO FOLDER CONSOLIDATION, 53 TO 18-19

Raised by Gray this window. **Not started, deliberately** - it would have left the
H2 patch unverified on a delete path.

`_target_folders` returned 53 folders, in this order (recorded because the
consolidation needs the real list, and because folder ORDER is what makes H2 bite):

    2006 Goals, 2025 Job Search, 8015 Dorado Terrace, AI Tool Kit, AT&-T,
    All State, American Airlines, Apple, Archive, BAE, Bulk, Calendar_Events,
    Cancellations, Cancun, Car Transmission, Certifications, Cisco,
    Divorce Recordings, Draft, Drafts, EBay, Facebook, Family, Finance,
    Health_Medical, Honda, Inbox, Inbox/Receipts, Jacobs, Junk, Newsletters,
    Nordstrom, Online Purchases, Personal, Photos_Media, Priority, Private,
    Productivity, Promotions, Receipts_Confirmations, School, Sent, Shopping,
    Social, Social_Media, Spam, Tickets, Tower Federal Credit Union, Trash,
    Verizon, Veteran Stuff, Work, bestie

Note `AT&-T` - that is IMAP modified-UTF7 leaking through as a literal folder
name, and any mapping table has to handle it rather than assume clean ASCII.
Note also the near-duplicate pairs already visible: `Draft` / `Drafts`,
`Social` / `Social_Media`, `Receipts_Confirmations` / `Inbox/Receipts`,
`Junk` / `Spam` / `Bulk`.

**This is gated on H1 and it is a hard dependency, not a preference.** A
consolidation is a bulk move across nearly every folder in that list. With H1
open, a fold that moves 40 of 60 messages reports `applied: True` and the agent
tells Gray it is done. Partial folds would be silently accepted, repeatedly, at
volume. H2 would have been the other repeat offender - a sender-scoped scan
returning before reaching the target folder - which is now closed.

Scope when it starts: Gray's established 18-19 categories are the target set; the
mapping table from 53 source folders to those categories is the deliverable
BEFORE any move runs; and the move plan must be dry-run per source folder with
counts, not one bulk operation.

---

## 5. EXECUTION PATHS REGISTER

Standing structure. Carried forward and extended, not re-derived.

### PATHS ALREADY REGISTERED (unchanged this window)

- PATH 1: orchestrator `ask()` via `system\orchestrator.py`
- PATH 2: managed-agent SSE via `_stream_managed_agent()` in
  `server\agent_manager_routes.py` (four auto-approve sites, open item - still
  the largest outstanding gate item)
- PATH 3: test-execute via `POST /v1/tools/test-execute` - gate LIVE, `confirm_id`
  verified on the wire (W21). **The only path where the gate is proven end to end.**
- `routes.py` chat dispatch 1a/1b/1c/1d - non-streaming branches offloaded to
  `asyncio.to_thread` as of `aad8ccd`
- Frontend submit F-A typed, F-B voice, F-C option relay (DEAD - no handler for
  `jarvis-submit-text`)
- `_extract_tool_call` order: native, Format 1 (case-insensitive, UNANCHORED),
  Format 2 (unread), Format 4 (XML, shadowed by 1), Format 3 (bare JSON).
  Precedence is an accident of insertion order.

### EXTENDED THIS WINDOW - destructive mailbox path, sender-resolution stage

| Property | Value | Evidence |
|---|---|---|
| Registration | `mailbox_tools.py:453` | READ (W26) |
| Spec | `mailbox_tools.py:463-509`, `timeout_seconds=1800.0`, `required: ["folder"]` | READ |
| Confirmation gate | **ABSENT AND DELIBERATE.** Interlock is `dry_run=False` + `confirm="CONFIRM DELETE"` | READ (W26 2.1) |
| Folder binding | `mailbox_tools.py:519`, guarded non-empty at `:539-544` | READ |
| Sender resolution | `mailbox_tools.py:546`, **now `folder=folder`** as of `801869c` | READ |
| Connector search | `imap_mail.py:477-486`, keyword-only, accepts `folder` | READ |
| Folder list construction | `imap_mail.py:497`, `[folder]` when supplied | READ |
| Cap semantics | `imap_mail.py:527`, `return` INSIDE the per-folder loop | READ + OBSERVED (2.4) |
| Folder name fidelity | `imap_mail.py:377` echoes the parameter verbatim; quoting only at `:336` select | READ |
| Python-side filters | `mailbox_tools.py:558`, `:584`, exact string equality | READ |
| Protected senders | `mailbox_tools.py:566-589`, file override `protected_senders.json` in cwd | READ, **never exercised (2.5)** |
| Callers into connector | `mailbox_tools.py:667` dry run, `:669` live - ONLY callers | READ (grep, W26) |
| Connector move | `imap_mail.py:537`, chunked COPY, retry, per-uid degrade | READ |
| Result contract | `mailbox_tools.py:689` `success=bool(result.get("applied"))` | READ |
| `applied` definition | past `imap_mail.py:626` | **UNREAD - ASSUMED** |
| Protocol | UID COPY, UID STORE +FLAGS \Deleted, EXPUNGE | READ |
| Encoding | IMAP wire bytes; `_imap_text()` UTF-8 decode, errors=replace | READ |
| Threading | synchronous, on an `asyncio.to_thread` worker, never the event loop | READ |
| Scan cost, 53 folders | 113.7 s unscoped vs 3.0 s scoped, same 86 rows | OBSERVED (2.3) |

---

## 6. SDP / SDD FEED

**Carried correction, still owed.** SDP revB:504 and revC:597 assert
`requires_confirmation=True` for `mailbox_move_to_trash`. Both WRONG (W26 2.1).
Replace with: the flag is deliberately unset, the reason is in the
`mailbox_tools.py` header, the interlock is `dry_run=False` plus the exact
`CONFIRM DELETE` token, and the stated premise predates 6c and is untested. **Do
not simply flip the boolean - carry the reasoning.**

**New for the SDP this window - the sender-resolution stage is now a documented
gate.** It has its own failure mode independent of the confirmation interlock: a
scan that returns before opening the target folder produces `success=False` and
`"no messages matched"` for a folder never examined. That is a *safety-relevant
false negative* - it does not delete the wrong thing, it silently declines to act
and reports it as an empty result. The SDP's destructive-path chapter should
state both directions of failure, not only "could it delete too much".

**Evidence-quality marking is now load-bearing, and this window proves it twice.**
The `applied = deleted > 0` claim survived from W25 to W27 unread, and would have
been written into an H1 fix as fact. Section 3.3 stops it. Keep the
READ / OBSERVED / ASSUMED column in every artifact row.

**Defect 6 confirmation gate - GREAT DETAIL per Gray's standing instruction.**
Unchanged from W26. Registry: write-once, 409 on re-decision, TIMEOUT internal
only. Payload: seven fields; `turn_id` from `CURRENT_TURN_ID` set by
`openjarvis-agent-log-v1` - a diagnostic marker load-bearing on a safety-critical
payload, still a design smell needing its own owner. Transport: EventBus ->
ws_bridge -> bare WS client; delivery proven W20, payload integrity W21.
Redaction CLOSED. TTL 120 s governs the WAIT FOR A HUMAN, not the execution that
follows. The mailbox path does not use this gate at all; PATH 3 remains the only
end-to-end proof.

**Defect 1 - two independent mechanisms, keep them separate.** (a) The model
claims actions it never invoked: parser and prompt problem. (b) **H1 - the tool
truthfully reports `applied: True` for a partial move**, and the model accurately
reports an inaccurate result. No confabulation. H1 is narrower than previously
stated (section 3.2): the early-return cases are correct; only partial success is
mis-reported.

**Verification methodology chapter - two new entries (running total ten):**
9. **A test built from the call site rather than the cap semantics cannot fail.**
   Probe 1 exercised nothing because 86 hits never reached a 5000 cap (2.3). Derive
   the test from the mechanism, then check the test can actually produce a negative.
10. **Distinguish "bypassed" from "covered".** Probe 2 ran against a
    protected-listed sender and touched the blocklist not at all. Recording that
    explicitly is what stops a future window inheriting false coverage (2.5).

**Architecture artifact.** `OPENJARVIS-ARCH-GATES-2026-08-31-v1.md` still in the
repo root, untracked, cut at `6c172d1`. **Now one commit stale** - the
sender-resolution row changed at `801869c`. Next version: refresh that row, add
the speech gates, characterize PATH 2's auto-approve sites.

---

## 7. 550B CLOUD MODEL

Carried forward per the 08/29 pin. **Untouched this window.**

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
resolve to, and every case where those two disagree. **Carried across SIX windows.**

**Staleness.** Built 08/30. Since then `app.py` moved in `f53a60d` (W23),
`routes.py` in `aad8ccd` (W24), `imap_mail.py` in `611329e` (W25) and
`mailbox_tools.py` in `6c172d1` (W26) and again in `801869c` (W27). **Rebuild
before submitting. Do not submit the existing file.**

**Widening still recommended:** duplicated definitions are a four-instance pattern
(speech triplication, the `auth_middleware.py` / `serve.py` bind verdict).
Consider a general duplicated-definition sweep rather than a speech-only brief.

**Candidate bundle for H1, if the next read does not settle it:** `imap_mail.py`
plus `mailbox_tools.py` with the brief "trace every assignment to `applied`,
`failed_uids` and `store_failed`, and state for each exit point of `move_to_trash`
what the three values are". Both files are large enough that targeted reads have
now cost three windows.

### 7.1 PowerShell idiom for a multi-line commit message - PROVEN W26, RE-PROVEN W27

Source, NOT a command to paste as-is. Adapt the text and run from the repo root.
Writes to `%TEMP%`, not the repo root, so it does not add to the untracked pile.

    $msg = @'
    subject line here

    body here
    '@
    $f = Join-Path $env:TEMP 'ojmsg.txt'
    $msg | Set-Content -Path $f -Encoding ascii
    git add <path>
    git commit -F $f
    Remove-Item $f

The closing `'@` must be at column zero. Never use a bash heredoc. Used again this
window for a 25-line message with indented output blocks - no parse error, no
continuation prompt.

### 7.2 In-place single-line patch idiom - PROVEN W27

    $f = '<path>'
    Copy-Item $f "$f.bak-<tag>" -Force
    (Get-Content $f -Raw) -replace '<escaped old>', '<new>' | Set-Content $f -Encoding ascii -NoNewline
    git --no-pager diff

`-NoNewline` is deliberate: it preserves the file's existing line endings instead
of rewriting them, so a one-line change stays a one-line diff on a CRLF file
rather than becoming a whole-file diff. Verified - the diff came back as exactly
one `-`/`+` pair on a file that throws the CRLF warning on every git command.

---

## 8. NEXT ACTIONS, ORDERED

1. **H1 - finish the read.** `imap_mail.py` from 626 to the end of
   `move_to_trash`. Establish what assigns `applied`, `failed_uids` and
   `store_failed`. Command in section 3.3. Until this is read, do not propose a
   contract and do not repeat `applied = deleted > 0`.
2. **H1 - decide the result contract.** What `mailbox_tools.py:689` should report
   when `copied` is non-empty and `failed` is non-empty. The connector already
   has the data (3.2); the tool layer discards it. Highest-severity open item on
   the destructive path, and a hard prerequisite for item 4.
3. **Exercise `openjarvis-protected-senders-v1`.** Never tested (2.5). Needs a
   non-interactive dry-run through `MailboxMoveToTrashTool.execute` - not a direct
   connector call - against a protected sender, asserting the block report is
   populated and nothing is selected.
4. **Yahoo folder consolidation, 53 to 18-19** (section 4). Gated on items 1-2.
   Mapping table first, dry run per source folder, no bulk operation.
5. **Retest the W26 2.1 premise** - does the confirm callback now reach the
   mailbox path after 6c? Decides whether `requires_confirmation` can be set at
   all. Until answered, the SDP correction carries the caveat, not a verdict.
6. **Rebuild and feed `CLOUDBUNDLE-speech`** to the 550B. Rebuild mandatory -
   five files have moved. Consider widening to a duplicated-definition sweep.
7. **Parser ordering audit** (W23 3.1). All four formats in one pass, precedence
   decided deliberately. Format 1's unanchored case-insensitive match shadowing
   Format 4 XML is the live risk. Format 2 still unread.
8. **PATH 2's four managed-agent auto-approve sites.** Largest outstanding
   confirmation-gate item, untouched for several windows.
9. **Refresh the architecture artifact** - one commit stale, sender-resolution row
   changed at `801869c`.
10. **Repo root layout decision** - `scripts/`, `handoffs/`, `.gitignore`,
    `.gitattributes` for CRLF. Roughly 160 untracked files. `mailbox_tools.py`
    throws a CRLF warning on every git command, noise that hides real warnings.
    Delete the stray `"patch_testexec_v1 .py"` WITH THE SPACE - `patch_testexec_v1.py`
    (no space) is live and reads `app.state.bind_is_loopback`, so check which is
    which first.
11. **Second prompt bundle** - `InputArea.tsx`, `useSpeechStream.ts`,
    `MessageBubble.tsx`. Tests transcript accumulation, identifies the
    `jarvis-option-select` dispatcher.
12. **One retry of the 120B** on a bundle, to separate attachment failure from
    size limit.
13. **Lab item, not OpenJarvis:** the GitLab remote is plaintext HTTP, port 80,
    no TLS. Belongs with the Zero Trust work.

---

## 9. STANDING RULES IN FORCE

- **START OF WINDOW: reconcile the handoff against HEAD before acting on it.**
  `git --no-pager log --oneline -5` plus a look for newer handoff files.
  (W25 2.1; cheap and confirming in W26 and again in W27 - one exchange, HEAD
  matched, newest handoff matched.)
- ALWAYS VERIFY. Never stack a second change on an unverified first one.
- FINISH THE THING BEFORE STARTING THE NEXT. No dangling processes. **W27 parked
  the folder-consolidation request mid-window rather than start it on top of an
  unverified delete-path patch.**
- Take counts from the `N insertions(+), M deletions(-)` line, NEVER the `--stat`
  graph column. Four misreads on record.
- **Read the mechanism before naming the severity.** (W26 2.2.)
- **Mark evidence quality: READ / OBSERVED / ASSUMED.** (W26 section 3.)
- **A test derived from the call site rather than the mechanism cannot fail.**
  Check that a proposed test is capable of producing a negative. (New, W27 2.3.)
- **Record what a test BYPASSED, not only what it covered.** (New, W27 2.5.)
- State shell and host on every command. Default PowerShell 5.1 on the Windows
  box; anything for the Ubuntu ollama host (172.16.33.200) must be labeled or
  PowerShell-wrapped ssh.
- Commands must run from `PS C:\Users\Admin\OpenJarvis>` as pasted. If a command
  needs a different path, say so IN THE REQUEST, before it runs. When a file is
  delivered for download, state where it lands and give the command that accounts
  for that location, in the same message.
- ONE runnable block per message. Quoted source inline or labeled as source.
- **Every runnable block must be valid in PowerShell 5.1 unless explicitly
  labeled for another shell. No heredocs, no `<<`, no `$(...)` substitution.**
- No non-ASCII symbols in replies.
- Tests must be non-interactive - no test whose success depends on Gray reacting
  inside a time window.
- Pin the detail of every window including negative results.
- Push to both remotes, always. `origin` is GitHub, `gitlab` is
  `http://172.16.33.126/root/openjarvis-desktop.git`.
- Token conservation on working sessions.
- Flag at 15 exchanges, then hand off. A flag, not a stop - never cut a live trace.
- Every handoff carries the SDD/SDP section, the EXECUTION PATHS register, and
  the 550B cloud-model section.

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
- Rollback for `801869c`: `git revert 801869c`, or
  `git checkout 6c172d1 -- src\openjarvis\tools\mailbox_tools.py`. The
  `.bak-w27-h2` file was removed after both remotes verified.
