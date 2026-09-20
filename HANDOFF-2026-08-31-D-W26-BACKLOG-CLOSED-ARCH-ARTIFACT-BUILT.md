# HANDOFF 2026-08-31 D / WINDOW 26
# UNREAD-DIFF BACKLOG CLOSED. ARCHITECTURE ARTIFACT BUILT AFTER FIVE WINDOWS OWED.
# Plus: the SDP's confirmation-gate claim is REFUTED at the source, and H2 is
# a confident false negative on the delete path, not merely under-coverage.

Predecessor: HANDOFF-2026-08-31-C-W25-IMAP-MAIL-COMMITTED-ONE-DIFF-LEFT.md
Host: Windows box. Shell: PowerShell 5.1. Working dir: `PS C:\Users\Admin\OpenJarvis>`.
Backend: 127.0.0.1:8010, ollama, qwen3-coder:30b, agent native_openhands.
Window shape: provenance close-out plus one build. ONE commit (`6c172d1`), pure
provenance - no code behavior changed by this window's actions. One standalone
artifact produced. Nothing patched. Nothing debugged at runtime.

---

## 0. ONE PARAGRAPH FOR THE NEXT WINDOW

`mailbox_tools.py` is read verbatim, committed at `6c172d1` and pushed to both
remotes. **The unread-diff backlog is CLOSED** - `git status --short
--untracked-files=no` is blank, verified not asserted. Four windows of provenance
reconstruction are done. The architecture artifact owed for five windows is BUILT
and is in the repo root. Two findings dominate: **the SDP's
`requires_confirmation=True` claim for `mailbox_move_to_trash` is REFUTED at the
source and the omission is deliberate**, and **H2 is a confident false negative,
not under-coverage** - the search can return before the target folder is ever
opened, and the tool then reports "no messages matched" for a folder it never
looked at. H2's fix is ONE KEYWORD and is item 1. It was NOT started, on purpose,
with four exchanges left.

---

## 1. WHAT LANDED

| Hash | Content | Counts | Verified by |
|---|---|---|---|
| `6c172d1` | `mailbox_tools.py` - sender selection, windowed-count contract, account validation | 266 ins, 24 del | `status --short -uno` BLANK |

Pushed `611329e..6c172d1` to `origin` AND `gitlab`. Plain fast-forward, identical
object counts (6 objects, 5.54 KiB). No `--mirror`, no `--force`. Both remotes
verified at `6c172d1` in the same exchange as the push.

Also produced, in the repo root, UNTRACKED:
`OPENJARVIS-ARCH-GATES-2026-08-31-v1.md`, 14,897 bytes.

### 1.1 What `6c172d1` actually does - FIVE changes, not one

1. `_resolve_account` (`openjarvis-account-resolve-v1`) - unknown account ids no
   longer pass through unvalidated; the account email is accepted as an alias.
2. `mailbox_usage_report` - description rewritten to steer sender-discovery
   questions to it (`openjarvis-sender-discovery-v1`).
3. `mailbox_find_messages` (`openjarvis-find-summary-v1`,
   `openjarvis-find-window-v1`) - new `detail` enum defaulting to `summary`;
   `limit` default 200 -> 5000; aggregation into `by_address` / `by_folder`;
   `truncated` flag; a `note` stating counts are windowed at ~10,000 per folder
   and are a FLOOR, never a mailbox total.
4. `mailbox_move_to_trash` (`openjarvis-filter-move-v1`,
   `openjarvis-protected-senders-v1`, `openjarvis-uid-typeguard-v1`) - `from_addr`
   selects server-side so no uid list crosses the model; protected-sender
   blocklist; uids must be a JSON array of numeric strings; `timeout_seconds`
   300 -> **1800** (`openjarvis-tool-timeout-v1`).
5. `uids` removed from `required`; `folder` alone is required.

---

## 2. NEGATIVE RESULTS AND CORRECTIONS - PIN THESE

### 2.1 THE SDP IS WRONG ABOUT THE CONFIRMATION GATE - biggest finding of the window

W25 listed `requires_confirmation=True` as UNVERIFIED, taken from SDP revB:504
and revC:597, both prose. Read at the source this window:

    Select-String -Path src\openjarvis\tools\mailbox_tools.py -Pattern 'requires_confirmation'

Two hits, neither a spec assignment. Both are in a **header safety note that
explains why the flag is deliberately NOT set.** Quoted from the file:

    if tool.spec.requires_confirmation:
        if not self._interactive or self._confirm_callback is None:
            return ToolResult(..., success=False)

`ToolExecutor.execute` treats the flag as a **hard requirement, not a prompt**.
The server-side agent path builds its executor without `interactive=True` and
without a confirm callback, so a flagged tool **fails every call** rather than
prompting. That is the `_confirm_callback = None` defect, documented in-file
before it had a number.

**The interlock is the tool contract instead:** `dry_run` defaults True and
returns a plan with exact counts; applying requires BOTH `dry_run=False` AND
`confirm` set to the exact string `CONFIRM DELETE`.

**Two revisions of the SDP assert the opposite of the source.** Correct them.

**Standing caveat, do not lose it:** that reasoning predates the 6c confirm
registry and route. The premise that no executor can supply a callback MAY HAVE
EXPIRED. Not retested. Retesting it decides whether this path rejoins the real
gate or keeps its bespoke interlock permanently. Do not let it become folklore in
either direction.

### 2.2 H2 is a FALSE NEGATIVE on a delete path, not under-coverage

I asserted "under-coverage" twice before reading the mechanism. Reading it made
the finding worse, and the correction matters more than the original claim.

- `imap_mail.py:477-486` - `find_messages` is keyword-only and **accepts
  `folder`**.
- `imap_mail.py:~496` - `folders = [folder] if folder else self._target_folders(...)`.
- `imap_mail.py:527` - `if len(hits) >= limit: return hits` sits **INSIDE the
  per-folder loop** and returns immediately.
- `mailbox_tools.py:546` - the move path calls
  `conn.find_messages(from_addr=_from_addr, limit=5000)` with **no `folder=`**.

Consequence: folders iterate in `_target_folders` order. A scan that fills 5000
hits in earlier folders **returns before the target folder is ever opened.** The
tool then reports `"no messages matched"` with `success=False` for a folder it
never looked at. The cap is also spent on rows that are then discarded by the
Python-side folder filter.

Passing `folder=folder` restricts `folders` to one name. The Python-side filter
in `mailbox_tools` already compares folder names exactly, so selection semantics
are **IDENTICAL** - this is a scan restriction, not a behavior change. That
equivalence was established by reading, and it is what makes this a fix rather
than a patch to a delete path.

### 2.3 The count was wrong a FOURTH time

W22 recorded `mailbox_tools.py +290`. Actual: **266 insertions, 24 deletions.**
Same cause every time - the `--stat` graph column read as an insertion count.
Four instances. The pattern is now certain, not suspected. The rule stands: take
the count from the `N insertions(+), M deletions(-)` summary line, never the graph.

### 2.4 Handoff reconciliation worked, first time it was cheap

W25's new rule was applied at exchange 1. HEAD was `611329e`, matching the
handoff; Handoff C was the newest file in the root. Cost one exchange and
confirmed rather than corrected. W25 spent three exchanges learning this. The
rule is earning its place - keep it at the top of section 9.

### 2.5 The PowerShell commit idiom worked first try

Section 7.1 of W25, used verbatim for a long multi-line message. No parse error,
no continuation prompt, message file written to `%TEMP%` and removed. The
dialect rule from W25 section 2.5 held under its first real test.

---

## 3. THE ARCHITECTURE ARTIFACT - BUILT, FIVE-WINDOW DEBT CLEARED

`OPENJARVIS-ARCH-GATES-2026-08-31-v1.md`, repo root, untracked, 14,897 bytes.
Cut at `6c172d1`. Scope chosen by Gray: **all registered paths, full detail on
the mailbox and confirmation gates.**

Structure: hosts and ports; a 13-row gate inventory (G1-G13) with transport,
encoding and human-present per gate; the registered execution paths; threading
model; full confirmation-gate detail; full destructive-mailbox-path detail with
wire behavior and timings; the open hazard table; and an explicit
"what this does not cover" section.

**The design decision worth carrying forward: every row carries an EVIDENCE
column - READ, OBSERVED, or ASSUMED.** ASSUMED rows are protocol defaults never
verified here (ollama 11434, Yahoo IMAP 993, the TLS assumption). This project
has been burned repeatedly by confident prose, section 2.1 being the latest;
marking the gaps rather than filling them silently is the mitigation. **Do not
strip that column when the artifact goes into the wiki.**

### 3.1 Incidental finding - plaintext HTTP to the GitLab remote

`http://172.16.33.126/root/openjarvis-desktop.git`. Port 80, no TLS. Every push
carries repository contents over the lab network unencrypted. Found while
building the ports table. Not a code defect and not on any backlog. Recorded as a
lab-infrastructure item; belongs with the Zero Trust work, not with OpenJarvis.

---

## 4. WHAT REMAINS UNREAD

**Nothing.** `git status --short --untracked-files=no` is BLANK.

The backlog that ran from W22 through W26 is closed. The procedure went six for
six: `diff --stat` for the real counts, full `diff` read verbatim, grep every
identifier, expect the hypothesis to be wrong, then commit. It was wrong or
partly wrong six times out of six.

Remaining unread SOURCE (never a diff, so never on that backlog): Format 2 of
`_extract_tool_call`, and PATH 2's four auto-approve sites.

---

## 5. EXECUTION PATHS REGISTER

Standing structure. Carried forward and extended, not re-derived.

### PATHS ALREADY REGISTERED (unchanged this window)

- PATH 1: orchestrator `ask()` via `system\orchestrator.py`
- PATH 2: managed-agent SSE via `_stream_managed_agent()` in
  `server\agent_manager_routes.py` (four auto-approve sites, open item 6 - still
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

### EXTENDED THIS WINDOW - the destructive mailbox path, corrected

| Property | Value | Evidence |
|---|---|---|
| Registration | `mailbox_tools.py:453` | READ |
| Spec | `mailbox_tools.py:463-509`, `timeout_seconds=1800.0` | READ |
| **Confirmation gate** | **ABSENT AND DELIBERATE.** Interlock is `dry_run=False` + `confirm="CONFIRM DELETE"` | **READ (2.1)** |
| Sender resolution | `mailbox_tools.py:546`, `conn.find_messages(from_addr=..., limit=5000)`, **no folder=** | READ |
| Connector search | `imap_mail.py:477-486`, keyword-only, accepts `folder` | READ |
| Cap semantics | `imap_mail.py:527`, `return` INSIDE the per-folder loop | READ |
| Callers into connector | `mailbox_tools.py:667` dry run, `:669` live - ONLY callers | READ (grep) |
| Connector method | `imap_mail.py:537` `move_to_trash` | READ |
| Protocol | UID COPY, UID STORE +FLAGS \Deleted, EXPUNGE | READ |
| Encoding | IMAP wire bytes; `_imap_text()` UTF-8 decode, errors=replace | READ |
| Threading | synchronous, on an `asyncio.to_thread` worker, never the event loop | READ |
| Blocking floor | ~29 s per 290 uids clean | derived |
| Blocking ceiling | ~12 min per 290 uids fully degraded | derived |
| Timeout headroom | 1800 s vs ~12 min - fits | READ |

---

## 6. SDP / SDD FEED

**Correction required, highest priority in this section.** SDP revB:504 and
revC:597 both assert `requires_confirmation=True` for `mailbox_move_to_trash`.
Both are WRONG (section 2.1). Replace with: the flag is deliberately unset; the
reason is recorded in the `mailbox_tools.py` header; the interlock is
`dry_run=False` plus the exact `CONFIRM DELETE` token; and the stated premise
predates 6c and is untested. **Do not simply flip the boolean - carry the
reasoning, or the next reader will "fix" it back and break every call.**

**Defect 6 confirmation gate - GREAT DETAIL per Gray's standing instruction.**
Unchanged from W25 except as follows. Registry: write-once, 409 on re-decision,
TIMEOUT internal only. Payload: seven fields; `turn_id` from `CURRENT_TURN_ID`
set by `openjarvis-agent-log-v1` - **a diagnostic marker load-bearing on a
safety-critical payload, still a design smell and now named as needing its own
owner.** Transport: EventBus -> ws_bridge -> bare WS client; delivery proven W20,
payload integrity W21. Redaction CLOSED. TTL 120 s governs the WAIT FOR A HUMAN,
not the execution that follows - state that separation explicitly. New this
window: **the mailbox path does not use this gate at all**, which changes the
gate's coverage claim in the SDP. PATH 3 is the only end-to-end proof.

**Defect 1 - two independent mechanisms, keep them separate.** (a) The model
claims actions it never invoked: parser and prompt problem. (b) **H1 - the tool
truthfully reports `applied: True` for a partial move**, and the model accurately
reports an inaccurate result. No confabulation occurs. Different fixes. H1 is a
result-contract problem and, after reading the file it was assigned to, is
**still open** - `mailbox_tools.py` passes `applied` straight up and reconciles
neither `failed_uids` nor `store_failed`.

**Architecture - repository integrity.** No CI, no clean-clone import check, no
automated provenance. W23-W26 reconstructed provenance by hand, one file per
window. State plainly that this does not scale and that the mitigation is CI plus
commit-message provenance, not better handoffs. Commit bodies now carry the
hazard records, which is the one durable part.

**Verification methodology chapter - two new entries (running total eight):**
7. **Read the mechanism before naming the severity.** H2 was called
   "under-coverage" twice from the call site alone. Reading the cap semantics
   changed it to a confident false negative on a delete path (section 2.2).
8. **Mark evidence quality on every architectural claim.** READ / OBSERVED /
   ASSUMED. Section 2.1 exists because two SDP revisions carried an unmarked
   assumption as fact (section 3).

**Architecture artifact: DELIVERED.** Five-window debt cleared. Section 5 of W25
was lifted into it as intended. Next version should add the speech gates and
characterize PATH 2's auto-approve sites.

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
resolve to, and every case where those two disagree. **Carried across FIVE windows.**

**Staleness.** Built 08/30. Since then `app.py` moved in `f53a60d` (W23),
`routes.py` in `aad8ccd` (W24), `imap_mail.py` in `611329e` (W25) and
`mailbox_tools.py` in `6c172d1` (W26). **Rebuild before submitting. Do not submit
the existing file.**

**Widening still recommended:** duplicated definitions are a four-instance
pattern (speech triplication, the `auth_middleware.py` / `serve.py` bind verdict).
Consider a general duplicated-definition sweep rather than a speech-only brief.

### 7.1 PowerShell idiom for a multi-line commit message - PROVEN W26

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

The closing `'@` must be at column zero. Never use a bash heredoc.

---

## 8. NEXT ACTIONS, ORDERED

1. **H2 - the one-keyword fix.** At `mailbox_tools.py:546`, add `folder=folder`
   to the `conn.find_messages(...)` call. Selection semantics are identical
   (section 2.2, established by reading), so this is a scan restriction, not a
   behavior change on the delete path. Verify IN ISOLATION - dry run against a
   folder that sorts late in `_target_folders` is the discriminating test, and it
   must be non-interactive. Commit, push both remotes. Smallest real safety
   improvement available.
2. **H1 - the result contract.** `applied = deleted > 0` reports success for a
   partial move. Decide what `mailbox_tools.py` does with `applied`,
   `failed_uids` and `store_failed`. This is the Defect 1 result-contract
   question and it is the highest-severity open item on the destructive path.
3. **Retest the 4.1 premise** - does the confirm callback now reach the mailbox
   path after 6c? Decides whether `requires_confirmation` can be set at all
   (section 2.1). Until this is answered the SDP correction must carry the
   caveat, not a verdict.
4. **Rebuild and feed `CLOUDBUNDLE-speech`** to the 550B. Rebuild mandatory -
   four files have moved. Consider widening to a duplicated-definition sweep.
5. **Parser ordering audit** (W23 section 3.1). All four formats in one pass,
   precedence decided deliberately. Format 1's unanchored case-insensitive match
   shadowing Format 4 XML is the live risk. Format 2 is still unread.
6. **Open item 6** - four managed-agent auto-approve sites on PATH 2. Largest
   outstanding confirmation-gate item, untouched for several windows.
7. **Repo root layout decision** - `scripts/`, `handoffs/`, `.gitignore`,
   `.gitattributes` for CRLF. Roughly 160 untracked files, now including the
   architecture artifact. `mailbox_tools.py` throws a CRLF warning on every git
   command, noise that hides real warnings. Delete the stray
   `"patch_testexec_v1 .py"` WITH THE SPACE - `patch_testexec_v1.py` (no space)
   is live and reads `app.state.bind_is_loopback`, so check which is which first.
8. **Build and feed the second prompt bundle** - `InputArea.tsx`,
   `useSpeechStream.ts`, `MessageBubble.tsx`. Tests transcript accumulation,
   identifies the `jarvis-option-select` dispatcher.
9. **One retry of the 120B** on a bundle, to separate attachment failure from
   size limit.
10. **Lab item, not OpenJarvis:** the GitLab remote is plaintext HTTP (3.1).

---

## 9. STANDING RULES IN FORCE

- **START OF WINDOW: reconcile the handoff against HEAD before acting on it.**
  `git --no-pager log --oneline -5` plus a look for newer handoff files.
  (W25 2.1; worked first time and cheaply in W26 2.4.)
- ALWAYS VERIFY. Never stack a second change on an unverified first one.
- FINISH THE THING BEFORE STARTING THE NEXT. No dangling processes. **W26
  declined to start H2 with four exchanges left rather than leave a half-verified
  patch on a delete path.**
- Take counts from the `N insertions(+), M deletions(-)` line, NEVER the `--stat`
  graph column. Four misreads on record.
- **Read the mechanism before naming the severity.** (New, W26 2.2.)
- **Mark evidence quality: READ / OBSERVED / ASSUMED.** (New, W26 section 3.)
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
  untracked.
