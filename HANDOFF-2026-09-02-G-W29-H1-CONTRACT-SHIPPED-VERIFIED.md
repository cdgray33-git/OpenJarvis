# HANDOFF 2026-09-02 G / WINDOW 29
# H1 IS CLOSED AT THE TOOL LAYER. The four-state result contract is WRITTEN,
# VERIFIED BY OBSERVATION, COMMITTED, AND PUSHED TO BOTH REMOTES.
# Next actions 1, 2 and 3 from W28 are all DONE.
# Plus: a NEW SIBLING DEFECT found by the patch guard - `mailbox_empty_folder`
# at `mailbox_tools.py:765` carries the byte-identical `bool(applied)`
# conflation. Deliberately NOT touched. It is now item 1 on the board.

Predecessor: HANDOFF-2026-08-31-F-W28-H1-READ-CLOSED-STORE-MODE-FOUND.md
Host: Windows box. Shell: PowerShell 5.1. Working dir: `PS C:\Users\Admin\OpenJarvis>`.
Backend: 127.0.0.1:8010, ollama, qwen3-coder:30b, agent native_openhands.
Window shape: reconcile, four reads, one patch (two attempts, first failed safe),
one new harness built and run, two commits, both remotes.
Backend NEVER STARTED - not needed. Zero writes to the mailbox. Zero network
calls to Yahoo. PC had been rebooted since W28; irrelevant to on-disk git state
and to both harnesses, which are stdlib-only and socket-free.

---

## 0. ONE PARAGRAPH FOR THE NEXT WINDOW

W28's highest-severity open item is closed. `mailbox_tools.py` now computes a
four-state `outcome` - `complete` / `partial` / `copied_not_removed` / `no_op` -
from fields the connector already produced, instead of projecting them onto
`bool(applied)`. H1-B no longer reports success. H1-C now carries
`retry_unsafe: True` plus a plain-language warning naming both locations the
mail is sitting in, which is the specific thing that used to invite the
duplicating retry. Verified by a NEW tool-layer harness
(`tests\probe_h1_toolprobe_v1.py`) that drives the real
`MailboxMoveToTrashTool.execute` against a real `ImapMailConnector` with only
the IMAP socket faked - so `success` is OBSERVED, not computed. 4/4 scenarios
PASS. Committed `7b3a47e`, harnesses committed `0b17b35`, both pushed to
`origin` and `gitlab`. A `tests\` directory now exists, which partially settles
item 12. **The one thing a new window must NOT assume closed: the identical
defect at `:765` in `mailbox_empty_folder` is still live.**

---

## 1. WHAT LANDED

Two commits, both on both remotes.

    801869c  (W28 HEAD, start of this window)
    7b3a47e  mailbox_tools: four-state result contract for move_to_trash
             (openjarvis-h1-result-contract-v1)   46 insertions(+), 1 deletion(-)
    0b17b35  tests: add H1 destructive-path harnesses, connector and tool layer
             (openjarvis-h1-store-probe-v1, openjarvis-h1-toolprobe-v1)
             2 files changed, 332 insertions(+)

Counts taken from the `N insertions(+), M deletions(-)` line, per the standing
rule. Not from the `--stat` graph column.

New in the repo and TRACKED:

- `tests\probe_h1_store_v1.py` - the W28 connector-layer harness, moved out of
  the repo root. Was untracked; now committed. Item 3 from W28 is decided.
- `tests\probe_h1_toolprobe_v1.py` - NEW this window, tool layer.

Deleted from the repo root, deliberately: `patch_h1_result_contract_v1.py` and
`patch_h1_result_contract_v2.py`. Spent. The change is in git; rollback does not
depend on them.

### 1.0 Start-of-window reconcile - PASSED

    801869c (HEAD -> main, origin/main, origin/HEAD, gitlab/main, gitlab/HEAD)
    mailbox_tools: scope sender lookup to the target folder (openjarvis-h2-folder-scope-v1)

Newest handoff on disk was the W28 `-F-` file. Handoff and repository agreed.
**Fourth consecutive window where this check was cheap and confirming.** Gray had
rebooted the PC two days prior; the reconcile is exactly what makes that a
non-event rather than a question.

---

## 2. THE READS THAT MADE THE PATCH POSSIBLE

All READ this window, none previously on record.

### 2.1 `MailboxMoveToTrashTool.execute` - the seam

- `:513` - `def execute(self, **params: Any) -> ToolResult:`. Keyword-only, no
  positional contract to honor.
- `:514-515` - `account = str(params.get("account", "") or "")`, then
  **`conn = connector_for(account)`**. This is the patchable seam for any
  tool-layer harness: patch `connector_for` in the `mailbox_tools` namespace.
- `:516-517` - `conn is None` returns `_no_account_result`.
- `:519` - `folder` from params.

### 2.2 The uid typeguard - `openjarvis-uid-typeguard-v1`, `:627-656`

This matters to the contract and was not previously registered.

- `:628-641` - rejects a `str`/`bytes` `uids`, or anything not list/tuple, with a
  message telling the model not to construct uids itself.
- `:642` - **`uids = [str(u).strip() for u in uids]`**. Normalization happens
  BEFORE the connector call.
- `:643-656` - rejects any non-numeric uid, reporting `invalid_sample` (first 5)
  and `invalid_count`.

**Consequence for the contract:** `len(uids)` at the return site is the
post-typeguard, post-normalization count. It is the correct denominator for
`requested_count`, and it is correct on the `from_addr` path too, because
`:624` writes the resolved selection back into `params["uids"]` before the
typeguard runs.

### 2.3 The sender-resolution and protected-senders block, `:524-625`

READ, not exercised. Registered here so the next window does not re-read it:

- `:527-538` - passing BOTH `from_addr` and `uids` is rejected.
- `:539-544` - `from_addr` without `folder` is rejected.
- `:546` - `conn.find_messages(folder=..., from_addr=..., limit=5000)`, carrying
  the `openjarvis-h2-folder-scope-v1` marker from W27.
- `:558` - a second, redundant folder filter on the hits.
- `:563-578` - `openjarvis-protected-senders-v1`. Ten hardcoded defaults
  including `cdgray33@yahoo.com` and several Groupon transactional addresses;
  overridable by `protected_senders.json` in **`Path.cwd()`** - note, the CURRENT
  WORKING DIRECTORY, not the package directory. That is a real hazard: the
  override silently does not load if the backend is started from anywhere other
  than the repo root. **UNVERIFIED, flagged, not chased this window.**
- `:602-612` - if every match is protected, returns `success=False` with a
  `protected_blocked` report.
- `:624-625` - `params["uids"] = _sel`, `_resolved = len(_sel)`.

---

## 3. THE PATCH - AND THE GUARD THAT EARNED ITS KEEP

### 3.1 v1 FAILED SAFE. This is the most important event of the window.

The v1 patch script anchored on the exact five-line return block:

        return ToolResult(
            tool_name=self.tool_id,
            content=_dump(result),
            success=bool(result.get("applied")),
        )

It refused to run:

    line endings: CRLF
    anchor occurrences: 2
    FAIL: anchor must appear exactly once. Nothing written.

**Nothing was written. No `.bak` was created. No half-applied state.** A
`str.replace` without the uniqueness assertion would have silently patched the
first occurrence and left the operator believing the job was done - and the
first occurrence is the right one, so the patch would have LOOKED correct while
concealing that a second site exists.

### 3.2 The new finding the guard exposed - `mailbox_empty_folder:765`

    689             success=bool(result.get("applied")),     MailboxMoveToTrashTool
    765             success=bool(result.get("applied")),     MailboxEmptyFolderTool

`MailboxEmptyFolderTool` is registered at `:693` and permanently deletes every
message in a folder. Its docstring at `:695` says so, and its description at
`:704-712` calls it IRREVERSIBLE AND DESTRUCTIVE, gated on `dry_run=false` plus
the same `CONFIRM DELETE` token.

**It carries the identical one-bit conflation.** Whether it has the same four
states is UNKNOWN - it is expunge-based, not COPY-then-STORE, so the failure
geometry is probably different and possibly smaller. **Do not assume it is H1
again. Read the mechanism before naming the severity** (W26 2.2). But it is the
most destructive tool in the file and it reports through a boolean that has now
been proven inadequate one function above it.

**NOT TOUCHED THIS WINDOW, ON PURPOSE.** FINISH THE THING BEFORE STARTING THE
NEXT. It is item 1 in section 8.

### 3.3 v2 - the widened anchor

v2 anchored on the `_resolved` provenance block at `:678-684` plus the return.
That block sets `selected_by`, `protected_blocked`, `from_addr` and
`resolved_uid_count`, and exists ONLY in `MailboxMoveToTrashTool`. Anchor
occurrences: 1. Applied.

The script also printed the sibling count before and after - 2 before, 1 after -
so the untouched site is documented by the patch run itself rather than by
memory.

### 3.4 What the contract actually computes, at `:686-712`

Nothing new is collected. Every input was already in the plan dict:

    _requested    = len(uids)                     # post-typeguard
    _copied       = result.get("copied_count") or 0
    _deleted      = result.get("deleted_count") or 0
    _failed       = result.get("failed_uids") or []
    _store_failed = result.get("store_failed") or []

    if   _copied == 0                                        -> "no_op"
    elif _deleted == 0                                       -> "copied_not_removed"
    elif _failed or _store_failed or _deleted != _requested   -> "partial"
    else                                                      -> "complete"

    success = (_outcome == "complete")

The `or 0` idiom is load-bearing and not cosmetic - see 4.2. `result.get` is
used throughout rather than `result[...]`, which respects the presence asymmetry
recorded in W28 2.4 (`store_failed` is absent on the happy path).

On `copied_not_removed` the result also gets `retry_unsafe: True` and a
`warning` naming the count and the source folder in plain language. On `partial`
it gets `retry_unsafe: False` and a warning naming the shortfall. Both warnings
are written for the MODEL to relay to a human, not for a log.

### 3.5 Verified in isolation before anything stacked on it

`python -m py_compile` returned COMPILE OK, and `:686-700` was read back from
disk showing the marker and the new body. Only then was the harness built.

---

## 4. THE TOOL-LAYER HARNESS - AND WHAT IT OBSERVED

`tests\probe_h1_toolprobe_v1.py`, marker `openjarvis-h1-toolprobe-v1`, stdlib
only. Run from the repo root: `python .\tests\probe_h1_toolprobe_v1.py`.
**Verified to still pass after the move into `tests\`** - it does
`sys.path.insert(0, cwd()\src)`, so the repo root remains the required CWD.

**What is REAL:** the entire tool body `mailbox_tools.py:513-712` including the
typeguard and the confirm interlock, AND the entire connector body
`imap_mail.py:537-653`. **What is FAKE:** only the object returned by
`ImapMailConnector._connect`.

This closes W28 4.5's stated gap. The `success` column is no longer computed by
the harness from `applied` - it is read off the returned `ToolResult`.

### 4.1 The verdict table - OBSERVED

| | COPY | STORE | outcome | success | retry_unsafe |
|---|---|---|---|---|---|
| A | ok | ok | `complete` | **True** | absent |
| B | partial (uid 7) | ok | `partial` | **False** | False |
| C | ok | all NO | `copied_not_removed` | **False** | **True** |
| D | all fail | - | `no_op` | **False** | absent |

    OVERALL: PASS   (4/4, expected outcome AND expected success per row)

B: `requested/copied/deleted = 12/11/11`, `failed_uids=['7']`, warning names the
shortfall. C: `12/12/0`, `store_failed` lists all twelve, warning names both
locations and says do not retry.

The harness can produce a negative - it asserts a per-row expectation and prints
PASS/FAIL, and it exits 2 loudly if the connector import path does not resolve.
Checked against the W27 2.3 rule before it was run.

### 4.2 Three things this run produced that the connector-layer probe did not

1. **Scenario D returns `deleted_count: None`, not 0.** The `:633` early return
   fires before `:646` ever sets the key. `result.get("deleted_count") or 0` is
   therefore not defensive padding - **remove the `or 0` and `no_op` raises a
   TypeError on the comparison.** Now OBSERVED, was never visible from the
   connector probe because that probe read the raw plan dict and did no
   arithmetic on it.
2. **Scenario D never calls `expunge`.** `expunge=False` observed, against
   `expunge=True` in C. Confirms by observation that `:633` returns before
   `:645`, and sharpens W28 4.4 item 2: expunge fires on total STORE failure but
   NOT on total COPY failure.
3. **The COPY retry ladder is visible in the call counts.** A: 2 COPY calls.
   B: **15**. D: **20**. Two chunks, and each failing chunk is retried up the
   1/2/4/8 ladder. This is the first time the ladder's real call volume has been
   OBSERVED rather than inferred from reading `:601-608`.

### 4.3 What this test BYPASSED - per the W27 2.5 rule

Stated so no future window inherits false coverage. The harness prints this
banner itself on every run, so it cannot drift from the file.

- **`time.sleep` was PATCHED** in `openjarvis.connectors.imap_mail`. The tool
  calls `move_to_trash(folder, uids, dry_run=False)` **positionally**, so
  `pause_s` cannot be threaded through from the tool layer. This is a departure
  from W28 methodology entry 13 (prefer a real parameter over a patched global)
  forced by the call site. **Retry ladder TIMING is not covered.** With real
  sleeps, scenario D would take roughly 30 s.
- **`openjarvis-protected-senders-v1` STILL not exercised. THIRD consecutive
  window.** The harness passes `uids`, not `from_addr`, so `:527-625` is skipped
  entirely. This is now the longest-standing bypassed item on the destructive
  path.
- **No real IMAP server.** Proves what the code does with given responses, not
  which responses Yahoo gives. Partial STORE inside an OK chunk, expunge
  failures and Yahoo quirks remain outside.
- **`folder == trash` (`imap_mail.py:591-592`) not exercised.** Still untested,
  two windows running.
- **`mailbox_empty_folder` not covered at all.** Its `:765` conflation is
  untested by anything.
- The `protected_senders.json` `Path.cwd()` load (2.3) is untested.

---

## 5. EXECUTION PATHS REGISTER

Standing structure. Carried forward and extended, not re-derived.

### PATHS ALREADY REGISTERED (unchanged this window)

- PATH 1: orchestrator `ask()` via `system\orchestrator.py`
- PATH 2: managed-agent SSE via `_stream_managed_agent()` in
  `server\agent_manager_routes.py` (four auto-approve sites, open item - still
  the largest outstanding gate item)
- PATH 3: test-execute via `POST /v1/tools/test-execute` - gate LIVE,
  `confirm_id` verified on the wire (W21). The only path proven end to end.
- `routes.py` chat dispatch 1a/1b/1c/1d - non-streaming branches offloaded to
  `asyncio.to_thread` as of `aad8ccd`
- Frontend submit F-A typed, F-B voice, F-C option relay (DEAD - no handler for
  `jarvis-submit-text`)
- `_extract_tool_call` order: native, Format 1 (case-insensitive, UNANCHORED),
  Format 2 (unread), Format 4 (XML, shadowed by 1), Format 3 (bare JSON).
  Precedence is an accident of insertion order.

### EXTENDED THIS WINDOW - destructive mailbox path, tool stage

W27 sender-resolution rows and W28 connector rows are unchanged and still valid.
New and revised:

| Property | Value | Evidence |
|---|---|---|
| Tool entry point | `mailbox_tools.py:513` `execute(self, **params)` | **READ (new)** |
| Connector acquisition | `:515` `conn = connector_for(account)` | **READ (new)** |
| uid typeguard | `:627-656`, normalizes then rejects non-numeric | **READ (new)** |
| `requested_count` source | `len(uids)` post-typeguard, post-`from_addr` writeback | READ + OBSERVED |
| Result contract | `:686-712`, four-state `outcome`, `success = outcome == "complete"` | **READ + OBSERVED (WAS the open item)** |
| A complete | `success=True` | **OBSERVED (tool layer)** |
| B partial | `success=False`, warning, `retry_unsafe=False` | **OBSERVED (tool layer) - was True** |
| C copied_not_removed | `success=False`, warning, **`retry_unsafe=True`** | **OBSERVED (tool layer) - NEW SURFACE** |
| D no_op | `success=False`, `deleted_count` **absent/None** | **OBSERVED (tool layer)** |
| `expunge` on total COPY failure | NOT called (`:633` returns first) | **OBSERVED (new)** |
| COPY retry ladder volume | 2 calls clean, 15 on one failing chunk, 20 on two | **OBSERVED (new)** |
| `mailbox_empty_folder` result | `:765` `success=bool(result.get("applied"))` | **READ - DEFECT, UNPATCHED** |
| `protected_senders.json` load | `Path.cwd()`, CWD-dependent | READ, **UNVERIFIED** |
| Protected senders | `:563-625` | READ, **never exercised, 3 windows** |
| Tool-layer harness | `tests\probe_h1_toolprobe_v1.py`, 4/4 PASS | OBSERVED |

---

## 6. SDP / SDD FEED

### 6.1 H1 is CLOSED at the tool layer - record it as fixed, with the shape

The SDP's destructive-path chapter can now move H1-B and H1-C from "open defect"
to "fixed, `7b3a47e`, verified by `tests\probe_h1_toolprobe_v1.py`". Record the
root-cause statement from W28 verbatim - **a four-state outcome was projected
onto a one-bit result** - and add the fix shape: **the fix was entirely at the
tool layer and added no new data collection.** Everything needed to tell the
four states apart was already in the connector's plan dict. That is the
generalizable lesson: when a result looks lossy, check whether the loss is at
the producer or the projection, because the projection is far cheaper to fix.

### 6.2 A NEW standing hazard for the SDP: duplicated result projections

`bool(result.get("applied"))` appearing at both `:689` and `:765` is the FIFTH
instance of the duplicated-definition pattern (speech triplication, the
`auth_middleware.py` / `serve.py` bind verdict, and now this). **The SDP should
name duplicated-definition as a recognized project-wide hazard class, not an
incidental finding.** It has now bitten in three subsystems. The
duplicated-definition sweep proposed in W28 section 7 should be widened to
include duplicated RESULT PROJECTIONS, not just duplicated function definitions.

### 6.3 GRAY'S NEW STANDING INSTRUCTION, 09/02 - PLAIN-LANGUAGE GUARD CHAPTER

**The SDP must explain the guard and confirmation mechanisms in language an
eight-year-old could follow, alongside the full technical detail. Not instead of
it - alongside it.** Every window from here contributes the plain-language
version of any guard it touches. Seeded below; extend, do not replace.

**The confirm token, in plain language.** Jarvis is allowed to throw away your
mail, but only if you say a magic phrase first. The phrase is `CONFIRM DELETE`,
spelled exactly. If Jarvis does not say the magic phrase, the tool does not
throw anything away - it just tells you what it WOULD have thrown away, and
waits. That is the dry run. It is like a friend holding up a bag of your stuff
and asking "this one?" before anything goes in the bin.

**The protected senders list, in plain language.** There is a short list of
people whose mail is never allowed in the bin, no matter who asks. Your own
address is on it. If Jarvis tries to bin mail from someone on that list, the
tool takes them back out and tells you it did. If EVERYTHING it wanted to bin
was on the list, it bins nothing at all and says so.

**The uid guard, in plain language.** Every message has a ticket number. Jarvis
is not allowed to make up ticket numbers - it has to use numbers it got from
actually looking in the mailbox. If it hands over anything that is not a proper
number, the tool refuses the whole job rather than guess. This stops it binning
the wrong mail because it invented a number that happened to belong to
something else.

**The new four-state report, in plain language - THIS is the W29 addition.**
Moving mail to the bin is really two steps: first make a copy in the bin, then
remove the original. Either step can go wrong on its own, which means there are
four different endings, not two:

1. **Everything worked.** Copies made, originals removed. Jarvis says "done".
2. **Some worked.** A few messages would not copy, so they are still sitting in
   the old place. Jarvis used to say "done" here. That was a lie of omission -
   you would think the job was finished when part of it was not. It now says
   "not finished" and tells you exactly how many were left behind.
3. **The copies were made but the originals were never removed.** This is the
   bad one. Your mail is now in TWO places at once. Jarvis used to say "it
   failed" - which sounds like nothing happened, so the natural thing to do is
   try again, and trying again makes a THIRD copy. It now says "it failed, AND
   twelve messages are already in your bin, AND do not try this again" in
   words the assistant has to repeat to you.
4. **Nothing happened at all.** Nothing copied, nothing removed, mailbox
   untouched. Jarvis says "it failed", and that one is honest.

The short version for the chapter opener: **a report that says "it failed" must
also say whether anything was left behind, because "failed" and "nothing
happened" are not the same thing, and treating them as the same is what makes a
person retry a job that is already half-done.**

### 6.4 Carried correction, STILL OWED, unchanged

SDP revB:504 and revC:597 assert `requires_confirmation=True` for
`mailbox_move_to_trash`. Both WRONG (W26 2.1). Replace with: the flag is
deliberately unset, the reason is in the `mailbox_tools.py` header, the
interlock is `dry_run=False` plus the exact `CONFIRM DELETE` token, and the
stated premise predates 6c and is untested. Do not simply flip the boolean -
carry the reasoning. **Confirmed again this window from the harness: the tool
accepts `confirm="CONFIRM DELETE"` directly with no gate callback in the path.**

### 6.5 Defect 6 confirmation gate - GREAT DETAIL per Gray's standing instruction

Unchanged from W26/W27/W28. Registry: write-once, 409 on re-decision, TIMEOUT
internal only. Payload: seven fields; `turn_id` from `CURRENT_TURN_ID` set by
`openjarvis-agent-log-v1` - a diagnostic marker load-bearing on a
safety-critical payload, still a design smell needing its own owner. Transport:
EventBus -> ws_bridge -> bare WS client; delivery proven W20, payload integrity
W21. Redaction CLOSED. TTL 120 s governs the WAIT FOR A HUMAN, not the execution
that follows. The mailbox path does not use this gate at all; PATH 3 remains the
only end-to-end proof. **Per 6.3, this section now also owes a plain-language
companion explanation. Not yet written.**

### 6.6 Defect 1 - keep the two mechanisms separate

(a) The model claims actions it never invoked: parser and prompt problem, still
open. (b) The tool mis-reports and the model accurately relays it - **(b) is now
FIXED for `move_to_trash` and OPEN for `empty_folder`.** No confabulation in
either.

### 6.7 Verification methodology chapter - three new entries (running total sixteen)

14. **Make the patch script assert that its anchor is unique, and refuse to
    write otherwise.** v1 matched twice and stopped. A blind `replace(old, new,
    1)` would have patched the correct site and hidden the existence of the
    second one. **The guard did not just prevent an error - it produced a
    finding.** This is the strongest argument yet for the pattern.
15. **Have the instrument print its own bypass list at runtime.** The tool
    harness prints what it does NOT cover every time it runs, so the coverage
    claim lives in the executable and cannot drift from the handoff the way a
    written-down claim does.
16. **A test that exercises two real layers with one faked boundary beats two
    tests that each fake the other layer.** Faking only `_connect` kept
    `mailbox_tools.py:513-712` and `imap_mail.py:537-653` simultaneously real,
    which is what made `deleted_count: None` visible - it only surfaces when the
    tool layer does arithmetic on the connector's actual output.

### 6.8 Architecture artifact

`OPENJARVIS-ARCH-GATES-2026-08-31-v1.md`, repo root, untracked, cut at
`6c172d1`, now **THREE commits stale** (`801869c`, `7b3a47e`, `0b17b35`). Next
version must add: the four-state result-contract row, the H1-B/H1-C split, the
`:765` sibling defect, and the ports/protocols/encoding at each gate per the
08/22 standing requirement. Deliver as a downloadable standalone file for the
wiki.

---

## 7. 550B CLOUD MODEL

Carried forward per the 08/29 pin. **Untouched this window** - every question
was answerable with four targeted reads. Second consecutive window it was not
needed, which is itself worth noting: targeted reads have been sufficient since
the H1 mechanism was located.

`bundle_for_cloud.py` in the repo root, marker `openjarvis-cloudbundle-v1`.
Read-only, stdlib only, does not import openjarvis. Use it whenever a question
needs whole files rather than targeted reads.

- `--set speech` and `--set prompt` defined, briefs already written.
- `--files <paths> --brief "<question>"` for ad hoc.
- Model: `openrouter/nvidia/nemotron-3-ultra-550b-a55b:free`. Proven on a ~16.7k
  token bundle, 438 s.
- The 120B (`nemotron-3-super-120b-a12b:free`) did NOT read the bundle. One
  retry still owed, to separate "did not attach" from "will not consume that
  size".

**STILL PENDING, NOT SUBMITTED: `CLOUDBUNDLE-speech-20260830-115352.md`**
(approx 20,766 tokens), covering `speech_router.py`, `app.py`, `api_routes.py`.
Brief asks for every duplicated definition with CURRENT line numbers, a diff of
the copies against each other, which copy FastAPI routes to versus which one
Python globals resolve to, and every case where those two disagree. **Carried
across EIGHT windows.**

**Staleness.** Built 08/30. Five files have moved since, and `mailbox_tools.py`
moved twice more this window. **Rebuild before submitting. Do not submit the
existing file.**

**Widening now strongly recommended, and the brief should change.** Per 6.2 this
is a five-instance pattern and now includes duplicated RESULT PROJECTIONS, not
only duplicated definitions. A good bundle for the 550B: `mailbox_tools.py`
whole, plus `imap_mail.py` whole, with the brief "find every place a
multi-state operation result is collapsed into a single boolean, and for each
one list the distinguishable states that are being discarded." That is a
question targeted reads are BAD at - it requires seeing every return site in
both files at once - which makes it the right kind of question to spend the
bundle on.

---

## 8. NEXT ACTIONS, ORDERED

1. **`mailbox_empty_folder:765` - read the mechanism, then decide the contract.**
   NEW, found by the v1 patch guard (3.2). Byte-identical `bool(applied)` on the
   most destructive tool in the file. **Read `execute` and the connector's
   `empty_folder` before naming a severity or assuming H1 repeats** - it is
   expunge-based, not COPY-then-STORE, so its state space is probably different.
   The verification vehicle already exists: extend
   `tests\probe_h1_toolprobe_v1.py` with an empty-folder scenario set.
2. **Exercise `openjarvis-protected-senders-v1`. THIRD window owed.** Longest
   outstanding item on the destructive path. Needs a non-interactive run through
   `MailboxMoveToTrashTool.execute` using **`from_addr`, not `uids`**, against a
   protected sender, asserting `protected_blocked` is populated and nothing is
   selected. The tool harness is the vehicle and the fake `find_messages` is the
   only new stub needed. **Also verify the `protected_senders.json`
   `Path.cwd()` load (2.3)** - the override may silently not load depending on
   where the backend was started from.
3. **Yahoo folder consolidation, 53 to 18-19** (W27 section 4). The W28 gate on
   items 1-2 is now **partially lifted**: H1-C is surfaced, so a failed fold
   reports `retry_unsafe` instead of inviting a duplicating retry. Still gated on
   item 2, because consolidation drives `from_addr` selection and protected
   senders has never been exercised. Mapping table first, dry run per source
   folder, no bulk operation. Watch `AT&-T` (modified-UTF7 leaking through) and
   the near-duplicate pairs `Draft`/`Drafts`, `Social`/`Social_Media`,
   `Receipts_Confirmations`/`Inbox/Receipts`, `Junk`/`Spam`/`Bulk`.
4. **`deleted_count` chunk-granularity** (W28 2.3). Connector-side, real,
   smaller. A chunk STORE returning OK credits all its uids, so `deleted_count`
   can overstate. Note this now interacts with the contract: an overstated
   `deleted` could turn a genuine `partial` into a false `complete` when
   `_deleted == _requested` is reached by over-crediting. **That raises its
   priority above where W28 had it.** Decide: leave documented, or make
   uid-accurate.
5. **`folder == trash` branch** (`imap_mail.py:591-592`), sets
   `copied = list(uids)` with no COPY at all. Never exercised, two windows. One
   scenario in the existing harness covers it.
6. **Retest the W26 2.1 premise** - does the confirm callback now reach the
   mailbox path after 6c? Decides whether `requires_confirmation` can be set at
   all. Until answered the SDP correction carries the caveat, not a verdict.
7. **Rebuild and feed a bundle to the 550B**, with the WIDENED brief in section
   7 - every collapsed multi-state result across `mailbox_tools.py` and
   `imap_mail.py`. Rebuild mandatory.
8. **Refresh the architecture artifact** - three commits stale, plus the
   contract row, the H1-B/H1-C split, the `:765` defect, and ports/protocols/
   encoding per the 08/22 rule. Downloadable file for the wiki.
9. **Write the plain-language companion for the Defect 6 gate chapter** (6.3,
   6.5). Gray's 09/02 instruction. The move-to-trash guards are seeded in 6.3;
   the confirmation gate itself is not yet done.
10. **Parser ordering audit** (W23 3.1). All four formats in one pass,
    precedence decided deliberately. Format 1's unanchored case-insensitive
    match shadowing Format 4 XML is the live risk. Format 2 still unread.
11. **PATH 2's four managed-agent auto-approve sites.** Largest outstanding
    confirmation-gate item, untouched for several windows.
12. **Repo root layout - PARTIALLY DONE.** `tests\` now exists and is tracked.
    Still owed: `scripts\`, `handoffs\`, `.gitignore`, `.gitattributes` for CRLF.
    Roughly 158 untracked files remain. `mailbox_tools.py` still throws a CRLF
    warning on every git command - it fired again on `7b3a47e` - noise that
    hides real warnings. Delete the stray `"patch_testexec_v1 .py"` WITH THE
    SPACE; `patch_testexec_v1.py` (no space) is live and reads
    `app.state.bind_is_loopback`, so check which is which first.
13. **Second prompt bundle** - `InputArea.tsx`, `useSpeechStream.ts`,
    `MessageBubble.tsx`. Tests transcript accumulation, identifies the
    `jarvis-option-select` dispatcher.
14. **One retry of the 120B** on a bundle, to separate attachment failure from
    size limit.
15. **Lab item, not OpenJarvis:** the GitLab remote is plaintext HTTP, port 80,
    no TLS. Belongs with the Zero Trust work.

---

## 9. STANDING RULES IN FORCE

- **START OF WINDOW: reconcile the handoff against HEAD before acting on it.**
  `git --no-pager log --oneline -1 --decorate` plus a look for newer handoff
  files. (W25 2.1; cheap and confirming in W26, W27, W28 and again in W29.)
  Branch is `main`.
- ALWAYS VERIFY. Never stack a second change on an unverified first one.
- FINISH THE THING BEFORE STARTING THE NEXT. No dangling processes. **W29 found
  the `:765` sibling defect mid-patch and deliberately did not chase it.**
- **Any patch script must assert its anchor is unique and refuse to write
  otherwise.** (New, W29. It caught a real second site.)
- Take counts from the `N insertions(+), M deletions(-)` line, NEVER the
  `--stat` graph column. Four misreads on record.
- **Read the mechanism before naming the severity.** (W26 2.2.)
- **Mark evidence quality: READ / OBSERVED / ASSUMED.** And when an assumption
  is promoted to READ, state what it MEANS, not just that it was confirmed.
  (W28 2.3.)
- **A test derived from the call site rather than the mechanism cannot fail.**
  Check that a proposed test is capable of producing a negative. (W27 2.3.)
- **Record what a test BYPASSED, not only what it covered** (W27 2.5) - and
  **have the instrument print that list itself** (new, W29).
- **Print what the collaborator was asked to do, not only what the function
  returned.** (W28.)
- State shell and host on every command. Default PowerShell 5.1 on the Windows
  box; anything for the Ubuntu ollama host (172.16.33.200) must be labeled or
  PowerShell-wrapped ssh.
- Commands must run from `PS C:\Users\Admin\OpenJarvis>` as pasted. If a command
  needs a different path, say so IN THE REQUEST, before it runs. When a file is
  delivered for download, state where it lands and give the command that
  accounts for that location, in the same message.
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
- Flag at 15 exchanges, then hand off. A flag, not a stop - never cut a live
  trace. **W29 flagged at 15 and finished the verification before writing this.**
- Every handoff carries the SDD/SDP section, the EXECUTION PATHS register, and
  the 550B cloud-model section.
- **The SDP guard chapters need a plain-language explanation an eight-year-old
  could follow, alongside the technical detail.** (New, Gray 09/02.)

---

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
  untracked, THREE commits stale.
- **H1 harnesses, both TRACKED as of `0b17b35`, both run FROM THE REPO ROOT:**
  - `python .\tests\probe_h1_store_v1.py` - connector layer, 4 scenarios
  - `python .\tests\probe_h1_toolprobe_v1.py` - tool layer, 4 scenarios,
    asserts PASS/FAIL per row, prints its own bypass list
  - Neither touches the network or the mailbox. Both require CWD = repo root.
- Connector module path, RESOLVED and confirmed by the harness:
  `openjarvis.connectors.imap_mail`
- `CONFIRM_TOKEN` is exactly the string `CONFIRM DELETE`, importable from
  `openjarvis.tools.mailbox_tools`.
- **Rollback for this window:** `git revert 7b3a47e` for the contract, or the
  file-level backup at
  `src\openjarvis\tools\mailbox_tools.py.h1contract.bak` (untracked, still on
  disk):
  `Copy-Item .\src\openjarvis\tools\mailbox_tools.py.h1contract.bak .\src\openjarvis\tools\mailbox_tools.py -Force`
