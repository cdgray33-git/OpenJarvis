# HANDOFF 2026-09-02 H / WINDOW 30
# THE `:765` SIBLING IS CLOSED - AND IT WAS NOT H1.
# `empty_folder` discarded the EXPUNGE return and reported success anyway.
# That is a FALSE POSITIVE - the opposite failure direction from H1.
# Patched `a99c739`, verified by an instrument that FAILED FIRST, pushed both
# remotes. Item 1 from W29 is DONE.
# Plus: the W29 handoff's `:689`/`:765` line numbers were STALE. Corrected here.

Predecessor: HANDOFF-2026-09-02-G-W29-H1-CONTRACT-SHIPPED-VERIFIED.md
Host: Windows box. Shell: PowerShell 5.1. Working dir: `PS C:\Users\Admin\OpenJarvis>`.
Backend: 127.0.0.1:8010, ollama, qwen3-coder:30b, agent native_openhands.
Window shape: reconcile, five reads, one 550B bundle, one new harness (ran
FAILING before the patch), one patch (clean on the first attempt), two commits,
both remotes.
Backend NEVER STARTED - not needed. Zero writes to the mailbox. Zero network
calls to Yahoo. The harness is stdlib-only and socket-free.

---

## 0. ONE PARAGRAPH FOR THE NEXT WINDOW

W29's item 1 is closed and it turned out to be a DIFFERENT defect class than
expected. `ImapMailConnector.empty_folder` called `imap.expunge()` and threw the
return value away, then set `applied = True` unconditionally. STORE was checked;
EXPUNGE was not. The result: server refuses the expunge, mail stays in the
folder wearing a `\Deleted` flag, and the tool reports `success=True`. A FALSE
POSITIVE - no duplication, no data loss, but a confident lie in exactly the
direction Gray will notice, because the entire point of the operation is
reclaiming space. Fixed at the connector (`a99c739`, 13 insertions, 1 deletion)
by capturing the return, setting `expunge_failed` and a plain-language error.
Verified by `tests\probe_h1_emptyfolder_v1.py` (`5a8ade0`, 208 insertions),
which was **run against unpatched code first and correctly reported 3/4 FAIL**,
then 4/4 PASS after. Both remotes at `5a8ade0`. **The one thing a new window
must NOT assume closed: the unchunked STORE at `imap_mail.py:709`, which is the
same payload shape Yahoo already rejected once on the move path.**

---

## 1. WHAT LANDED

    0b17b35  (W29 HEAD, start of this window)
    a99c739  imap_mail: check the EXPUNGE return in empty_folder
             (openjarvis-h1-emptyfolder-expunge-v1)   13 insertions(+), 1 deletion(-)
    5a8ade0  tests: add empty_folder expunge harness
             (openjarvis-h1-emptyfolder-v1)           208 insertions(+)

Counts from the `N insertions(+), M deletions(-)` line, per the standing rule.

New and TRACKED: `tests\probe_h1_emptyfolder_v1.py`.
Deleted from the repo root, deliberately: `patch_h1_emptyfolder_expunge_v1.py`.
Spent. The change is in git.

### 1.0 Start-of-window reconcile - PASSED

    0b17b35 (HEAD -> main, origin/main, origin/HEAD, gitlab/main, gitlab/HEAD)

Newest handoff on disk was the W29 `-G-` file. Handoff and repository agreed.
**Fifth consecutive window where this check was cheap and confirming.**

---

## 2. THE STALE LINE NUMBERS - A METHODOLOGY FINDING

**The W29 handoff cited the sibling defect at `mailbox_tools.py:765`. That was
wrong by the time it was written.** Sections 3.2, 8.1 and the execution-paths
register all carried `:689` / `:765`. Those numbers were produced by the v1
patch scan, which ran BEFORE `7b3a47e` inserted 46 lines into the same file.
They were never re-derived after the patch landed.

Actual addresses, confirmed this window:

- `MailboxMoveToTrashTool` return: `:731-735` (was `:689`)
- `MailboxEmptyFolderTool` return: `:810` (was `:765`)

Delta 45 lines, consistent with 46 insertions and 1 deletion.

**The check that caught it:** a `Select-String` for the literal
`bool(result.get("applied"))` returned exactly ONE hit, at `:810`. That single
command simultaneously proved (a) the W29 patch really removed the conflation
from the move path, and (b) the sibling's true address. Reading a window's own
patched file by inherited line number is how a correct finding turns into a
wrong instruction.

**NEW STANDING RULE (section 9): a line number recorded BEFORE a patch to the
same file is stale on arrival. Re-derive addresses by content search after any
patch that changes line counts, and record the search pattern, not the number.**

---

## 3. THE READS - `empty_folder`, RIGHT THROUGH

`imap_mail.py:671-718`, read whole. Registered so the next window does not
re-read it.

- `:677-683` - `plan` initialized with `"applied": False`.
- `:684-687` - `_connect()`; on None, `plan["error"] = self._last_error`, return.
- `:689` - `rows = self._fetch_summaries(imap, folder)`.
- `:690-693` - `message_count`, `bytes`, `human`.
- `:694-696` - no rows: `note = "folder already empty"`, return. `applied` stays False.
- `:697-703` - dry run: note with count and size, return. `applied` stays False.
- `:705-708` - `select(readonly=False)`; `typ != "OK"` sets an error and returns.
- `:709` - **`uid_set = ",".join(r["uid"] for r in rows)`. UNCHUNKED.** Every uid
  in one command line. See section 8 item 2.
- `:710-713` - `uid("STORE", uid_set, "+FLAGS", "(\\Deleted)")`. **Return IS
  checked.**
- `:714` - **`imap.expunge()`. Return WAS DISCARDED. This was the defect.**
- `:715` - `plan["applied"] = True`, unconditional.
- `:717-718` - `finally: self._close(imap)`.

### 3.1 The read that decided the severity - `_close`

`_close` calls **`imap.logout()`**, not `imap.close()`. This matters and was the
deciding fact. IMAP CLOSE implicitly expunges the selected mailbox; LOGOUT does
not. **Nothing rescues a failed expunge on the way out.** Had `_close` used
`close()`, the defect would have been largely cosmetic. It does not, so the
false positive is real. **Read the mechanism before naming the severity** paid
off here in the opposite direction from usual - it confirmed rather than
downgraded.

### 3.2 `_fetch_summaries` - read for the harness, `:325-369`

Needed to build a fake socket that does not lie. Verbs and shapes:

- `:336` `select(quoted, readonly=True)`, checked.
- `:341` `uid("SEARCH", None, "ALL")` -> `data[0]` is space-separated uid bytes.
- `:352` batch size 200.
- `:356-360` `uid("FETCH", uid_set, "(RFC822.SIZE BODY.PEEK[HEADER.FIELDS ...])")`.
- `:363-369` walks `resp` expecting **tuples of length >= 2**, `item[0]` bytes
  carrying `UID n` and `RFC822.SIZE n`, `item[1]` the header bytes. Anything
  else is skipped silently.

**Hazard this created for the harness, and it is the one that nearly mattered:**
a fake returning flat bytes instead of tuples yields ZERO rows, which hits the
`:694` already-empty return, which makes every scenario "pass" for entirely the
wrong reason. The harness prints `message_count` per row specifically to make
that visible. It read 3 on scenarios A/B/C, so the fake is genuinely satisfying
the real parser.

---

## 4. THE 550B RUN - FIRST USE IN THREE WINDOWS

Bundle: `mailbox_tools.py` + `imap_mail.py` whole. Brief: find every place a
multi-state result is collapsed to a single boolean; report CURRENT line numbers
counted from the bundle; **explicitly instructed not to trust any line number
from prior notes**; contrast expunge-based deletion against COPY-then-STORE.

### 4.1 Calibration - it independently landed `:734` and `:810`

Both numbers matched what we had verified by hand this window, and it did NOT
inherit the stale `:689`/`:765`. That is a real confidence signal, and the
"count from the bundle" instruction is what produced it. **Keep that clause in
every future brief.**

### 4.2 What it returned, graded

Six sites. Grading, not accepting:

| # | Site | Verdict |
|---|---|---|
| 1 | `mailbox_tools:246` usage report | DISCOUNTED - read-only, no retry hazard |
| 2 | `mailbox_tools:410` find_messages | DISCOUNTED - read-only; the "empty vs unreachable" ambiguity is real but low |
| 3 | `mailbox_tools:734` move_to_trash | CORRECT - and already fixed W29 |
| 4 | `imap_mail:647` `plan["applied"] = deleted > 0` | **KEEP - live, see 4.3** |
| 5 | `imap_mail:715` unconditional `applied = True` | **CORRECT - this window's defect, CONFIRMED BY READ** |
| 6 | `mailbox_tools:810` inherits site 5 | CORRECT |

### 4.3 Site 4 is still live and was NOT fixed by W29

`imap_mail.py:647` sets `plan["applied"] = deleted > 0` at the connector. The
W29 contract stopped the TOOL from reading it, but **`applied` is still in the
payload the model sees**. The conflation persists one layer below where it was
fixed. Not touched this window. Board item.

### 4.4 What the 550B could NOT see, and it was the deciding fact

**It never checked `_close`.** Its entire site-5 argument assumed nothing else
expunges. Correct here - but by luck, not by method. It reasons about the code
in front of it and does not chase a helper that decides the conclusion. **Use it
to LOCATE and to SWEEP. Do not let it name a severity.** That stays a read.

### 4.5 A hazard it surfaced without flagging

It noted the STORE is unchunked without connecting it to anything. That is the
same payload shape that forced the chunk/retry patch on the move path. On a
large Trash, `empty_folder` may fail at `:710` for a reason already solved
elsewhere in the same file. **It reports honestly (STORE is checked), so this is
a reliability item, not a safety one.** Board item 2.

---

## 5. THE PATCH AND THE VERIFICATION

### 5.1 The instrument was built and RUN BEFORE the patch

`tests\probe_h1_emptyfolder_v1.py`, marker `openjarvis-h1-emptyfolder-v1`,
stdlib only, run from the repo root.

**REAL:** the whole tool body, the whole `empty_folder`, the whole
`_fetch_summaries`, the real `_close`.
**FAKE:** only the object returned by `_connect`.

Expectations were written to the POST-FIX contract, so against unpatched code:

    OVERALL: FAIL   (3/4)
    B expunge NOT OK    applied=True  success=True  want=False   FAIL

**That failing run is the evidence the test is real.** A test written after the
fix and passing on the first run proves nothing about its ability to detect the
defect. This satisfies W27 2.3 by demonstration rather than by argument, and it
is the strongest form of that rule seen so far.

### 5.2 The patch - `a99c739`

Anchor was the three-line `expunge / applied = True / return plan` block, NOT
the bare `imap.expunge()` - which appears twice, the other in `move_to_trash`.
The uniqueness guard reported `anchor occurrences: 1` and
`expunge call sites before: 2 after: 2`, so the untouched sibling call is
documented by the patch run itself.

New body at `:714-728`: capture `_xtyp`, on non-OK set `expunge_failed = True`
plus an error naming the count and folder in plain language and return with
`applied` still at its `:682` False. On OK, `expunge_failed = False` then
`applied = True`.

**Line endings: `imap_mail.py` is LF (901 bare LF, 0 CRLF).** `mailbox_tools.py`
is the CRLF file that throws the git warning. **Two different line endings in
the same package.** Feeds the `.gitattributes` item.

### 5.3 Verified in isolation, then re-run

`py_compile` OK, `:714-728` read back off disk, and only then the harness
re-run - unchanged file, same command.

    OVERALL: PASS   (4/4)
    B  applied=False  success=False  expunge_failed=True
       error names the folder, the count, and says do not report success

### 5.4 The presence asymmetry - PIN THIS

`expunge_failed` is **absent** on scenarios C and D, not False. Same shape as
`store_failed` in W28 2.4. **Any consumer must use `.get()`, never
`result["expunge_failed"]`.** The W29 contract already learned this lesson once;
it now applies to a second key.

### 5.5 What this test BYPASSED - per the W27 2.5 rule

The harness prints this itself on every run, so it cannot drift.

- **A server that answers EXPUNGE OK and expunges nothing.** The residual. This
  is option B (re-verify by re-listing after expunge) and it is NOT closed.
- **The unchunked STORE at `:709`.** No payload-size limit is simulated.
- **No real IMAP server.** Proves what the code does with given replies.
- **Protected senders** - `empty_folder` does not consult them at all, which is
  itself worth noting: the most destructive tool in the file has NO protected-
  sender check. It deletes a whole folder, so per-sender protection does not
  apply, but that should be a stated design decision in the SDP rather than an
  observed absence.
- **`mailbox_move_to_trash`** - covered by the other harness, untouched.

---

## 6. EXECUTION PATHS REGISTER

Standing structure. Carried forward and extended, not re-derived.

### PATHS ALREADY REGISTERED (unchanged this window)

- PATH 1: orchestrator `ask()` via `system\orchestrator.py`
- PATH 2: managed-agent SSE via `_stream_managed_agent()` in
  `server\agent_manager_routes.py` (four auto-approve sites, still the largest
  outstanding gate item)
- PATH 3: `POST /v1/tools/test-execute` - gate LIVE, `confirm_id` verified on
  the wire (W21). Still the only path proven end to end.
- `routes.py` chat dispatch 1a/1b/1c/1d - non-streaming branches offloaded to
  `asyncio.to_thread` as of `aad8ccd`
- Frontend submit F-A typed, F-B voice, F-C option relay (DEAD - no handler for
  `jarvis-submit-text`)
- `_extract_tool_call` order: native, Format 1 (case-insensitive, UNANCHORED),
  Format 2 (unread), Format 4 (XML, shadowed by 1), Format 3 (bare JSON).
  Precedence is an accident of insertion order.

### EXTENDED THIS WINDOW - `mailbox_empty_folder`, tool and connector

| Property | Value | Evidence |
|---|---|---|
| Tool entry point | `mailbox_tools.py:780` `execute(self, **params)` | **READ (new)** |
| Connector acquisition | `:782` `connector_for(account)` | **READ (new)** |
| Confirm interlock | `:795` `_confirmed(params)`; dry-run plan returned via `_needs_confirmation_result` | **READ + OBSERVED (new)** |
| Gate callback | none in path; accepts `confirm=CONFIRM_TOKEN` directly | **OBSERVED (new)** |
| Protected senders | **NOT consulted at all on this path** | **READ (new)** |
| Connector body | `imap_mail.py:671-718` | **READ (new)** |
| STORE payload | `:709` uid_set unchunked, all uids one command | **READ - HAZARD, UNPATCHED** |
| STORE return | `:710-713` checked, sets error | READ + OBSERVED |
| EXPUNGE return | `:714` **now checked**, sets `expunge_failed` + error | **READ + OBSERVED (WAS the defect)** |
| Teardown | `:717-718` `finally` -> `_close` -> **`logout()`, NOT `close()`** | **READ (new) - decided the severity** |
| A clean | `applied=True`, `success=True`, `expunge_failed=False` | **OBSERVED** |
| B expunge NO | `applied=False`, `success=False`, `expunge_failed=True` | **OBSERVED - WAS True/True** |
| C store NO | `applied=False`, `success=False`, `expunge_failed` **absent** | **OBSERVED** |
| D empty | `applied=False`, `success=False`, early return at `:694` | **OBSERVED** |
| `imap_mail:647` `applied = deleted > 0` | still in the move payload | **READ - DEFECT, UNPATCHED** |
| Harness | `tests\probe_h1_emptyfolder_v1.py`, 4/4 PASS | OBSERVED |

---

## 7. SDP / SDD FEED

### 7.1 Record `empty_folder` as its OWN defect class, not H1 repeating

**The SDP must not fold this into H1.** The failure directions are opposite and
the distinction is the whole lesson:

| | H1-C (move_to_trash) | W30 (empty_folder) |
|---|---|---|
| Reported | failure | **success** |
| Reality | mail moved, in two places | **mail still there, flagged only** |
| Class | FALSE NEGATIVE | **FALSE POSITIVE** |
| Damage | retry duplicates | **operator stops looking; quota never reclaimed** |
| Fix cost | free - projection only | **cheap - one return value, producer-side** |

**The generalizable statement for the chapter:** W29 taught that a lossy result
may be lossy at the projection rather than the producer, and the projection is
cheaper to fix. W30 is the other half - **here the producer never collected the
fact at all, because it issued a command and did not look at the answer.** Both
are "the result is thinner than reality", but the remedy differs, and the way to
tell them apart is to ask whether the discarded fact was ever in the dict.

### 7.2 A NEW recognized hazard class: the unchecked command

`imap.expunge()` at `:714` was the only IMAP command in the destructive path
whose return was ignored. `select` was checked. `STORE` was checked. `expunge`
was not. **The SDP should name "issued but unchecked" as its own hazard, distinct
from duplicated definitions and duplicated result projections.** The sweep is
mechanical and cheap: find every IMAP verb whose `(typ, data)` return is
discarded. That is a good future 550B brief.

### 7.3 Duplicated result projections - the count is now SIX, not five

W29 recorded five instances of the duplicated-definition family. The 550B sweep
found `imap_mail:647` still projecting `applied = deleted > 0` at the connector
under the fixed tool. **The pattern is not just duplicated across functions, it
is LAYERED - fixing the top layer leaves the bottom one shipping the same
collapsed flag in the payload.** Widen the SDP's sweep accordingly.

### 7.4 GRAY'S STANDING INSTRUCTION, 09/02 - PLAIN-LANGUAGE GUARD CHAPTER

Extend, do not replace. W29's four entries (confirm token, protected senders,
uid guard, four-state report) stand unchanged. **New this window:**

**Emptying the bin, in plain language.** When Jarvis empties a folder it does
two things: first it puts a sticker on every message that says "throw this
away", then it tells the mail server "now actually throw away everything with a
sticker". The second part is the one that frees up space.

Jarvis used to only check that the STICKERS went on. It never checked whether
the server actually threw anything away. So if the server said "no" to the
second part, Jarvis would still come back and say "all done, folder emptied" -
while every single message was still sitting right there, wearing a sticker
nobody acted on. Your mailbox would be just as full as before, and you would
have stopped worrying about it, because you were told it was handled.

That is a different kind of mistake from the one we fixed last time. Last time
Jarvis said "it failed" when it had partly worked. This time Jarvis said "it
worked" when nothing had happened. **Being told a job is done when it is not is
worse than being told it failed, because when you are told it failed you go and
look.**

Now Jarvis checks the answer to the second part too. If the server refuses, it
says so plainly: the folder is NOT empty, the messages are still there with
stickers on them, and no space was freed.

**The short version for the chapter opener: if you tell somebody to do
something, you have to listen to their answer. Jarvis was giving the order and
walking away.**

### 7.5 Carried correction, STILL OWED, unchanged

SDP revB:504 and revC:597 assert `requires_confirmation=True` for
`mailbox_move_to_trash`. Both WRONG (W26 2.1). Replace with: the flag is
deliberately unset, the reason is in the `mailbox_tools.py` header, the
interlock is `dry_run=False` plus the exact `CONFIRM DELETE` token, and the
stated premise predates 6c and is untested. Carry the reasoning, do not flip the
boolean. **Confirmed again this window: `mailbox_empty_folder` behaves the same
way - `:795` `_confirmed(params)` with no gate callback anywhere in the path.
The same correction applies to BOTH destructive tools.**

### 7.6 Defect 6 confirmation gate - GREAT DETAIL per Gray's standing instruction

Unchanged from W26/W27/W28/W29. Registry: write-once, 409 on re-decision,
TIMEOUT internal only. Payload: seven fields; `turn_id` from `CURRENT_TURN_ID`
set by `openjarvis-agent-log-v1` - a diagnostic marker load-bearing on a
safety-critical payload, still a design smell needing its own owner. Transport:
EventBus -> ws_bridge -> bare WS client; delivery proven W20, payload integrity
W21. Redaction CLOSED. TTL 120 s governs the WAIT FOR A HUMAN, not the execution
that follows. **Neither mailbox tool uses this gate. PATH 3 remains the only
end-to-end proof.** Per 7.4 this section still owes its plain-language
companion. **Not yet written - now two windows owed.**

### 7.7 Defect 1 - keep the two mechanisms separate

(a) The model claims actions it never invoked: parser and prompt problem, still
open. (b) The tool mis-reports and the model accurately relays it - **(b) is now
FIXED for `move_to_trash` AND for `empty_folder`.** No confabulation in either.
**(b) is closed for the destructive mailbox path as a whole**, pending the
`:647` connector-payload residue in 4.3.

### 7.8 Verification methodology chapter - three new entries (running total nineteen)

17. **Run the new instrument against the UNPATCHED code first and require it to
    FAIL.** The failing 3/4 run is the proof the test can detect the defect.
    This is stronger than reasoning about whether a test is capable of a
    negative - it demonstrates it. Cost: nothing, the harness had to be written
    anyway. **Make this the default order for every future defect.**
18. **A line number recorded before a patch to the same file is stale on
    arrival.** Re-derive by content search, and record the SEARCH PATTERN in the
    handoff instead of the number. A single `Select-String` for the defective
    expression proved the old fix landed and located the new site at once.
19. **A cloud sweep can locate but must not adjudicate.** The 550B was right
    about `:715` and reached that conclusion without ever checking `_close`,
    whose behavior decided whether the finding mattered. Use it for breadth,
    then read the deciding helper yourself.

### 7.9 Architecture artifact

`OPENJARVIS-ARCH-GATES-2026-08-31-v1.md`, repo root, untracked, cut at
`6c172d1`, now **FIVE commits stale** (`801869c`, `7b3a47e`, `0b17b35`,
`a99c739`, `5a8ade0`). Next version must add: the four-state result-contract
row, the H1-B/H1-C split, the `empty_folder` expunge check and its false-positive
class, the absence of any protected-sender check on the empty path, and
ports/protocols/encoding per the 08/22 rule. Downloadable standalone file for
the wiki.

---

## 8. NEXT ACTIONS, ORDERED

1. **Folder consolidation, 53 to 18-19** (W27 section 4). **Gray stated this
   window that this is the direction: all content moves into ~18 predefined
   folders, then the drained folders are removed.** Still gated on item 3
   (protected senders, never exercised) because consolidation drives `from_addr`
   selection. Mapping table first, dry run per source folder, no bulk operation.
   Watch `AT&-T` (modified-UTF7 leaking), and the near-duplicate pairs
   `Draft`/`Drafts`, `Social`/`Social_Media`,
   `Receipts_Confirmations`/`Inbox/Receipts`, `Junk`/`Spam`/`Bulk`.
   **NEW SUB-ITEM: there is no confirmed DELETE FOLDER tool.** Removing the
   drained folders is a different operation from emptying them. Establish
   whether one exists before planning the removal phase.
2. **The unchunked STORE at `imap_mail.py:709`.** Same payload shape Yahoo
   already rejected on the move path, which is why the chunk/retry ladder exists
   there. Reliability, not safety - STORE is checked, so it fails honestly.
   Becomes materially more likely once consolidation makes Trash large. The
   proven ladder is in the same file and can be reused.
3. **Exercise `openjarvis-protected-senders-v1`. FOURTH window owed.** Longest
   outstanding item on the destructive path. Non-interactive run through
   `MailboxMoveToTrashTool.execute` using **`from_addr`, not `uids`**, against a
   protected sender, asserting `protected_blocked` is populated and nothing is
   selected. `tests\probe_h1_toolprobe_v1.py` is the vehicle; a fake
   `find_messages` is the only new stub. **Also verify the
   `protected_senders.json` `Path.cwd()` load** - the override may silently not
   load depending on where the backend was started from.
4. **`imap_mail:647` `plan["applied"] = deleted > 0`** (4.3). The connector-level
   residue under the fixed tool. Still in the payload the model reads. Decide:
   remove it, or redefine it to agree with the tool's `outcome`.
5. **Option B for `empty_folder`: re-verify by re-listing.** The residual from
   5.5 - a server answering EXPUNGE OK while expunging nothing. Re-run
   `_fetch_summaries` after expunge, report `remaining_count`, derive the outcome
   from observed truth. The harness already has the scenario slot.
6. **`deleted_count` chunk-granularity** (W28 2.3). A chunk STORE returning OK
   credits all its uids, so `deleted_count` can overstate - which can turn a
   genuine `partial` into a false `complete`. Decide: document or make
   uid-accurate.
7. **`folder == trash` branch** (`imap_mail.py:591-592`), sets
   `copied = list(uids)` with no COPY at all. Never exercised, three windows.
8. **Retest the W26 2.1 premise** - does the confirm callback now reach the
   mailbox path after 6c? Decides whether `requires_confirmation` can be set at
   all, **for both destructive tools** (7.5).
9. **550B sweep: every IMAP verb whose return is discarded** (7.2). Mechanical,
   cheap, and the one that just bit us. Bundle `imap_mail.py` whole.
10. **Write the plain-language companion for the Defect 6 gate chapter** (7.6).
    TWO windows owed now.
11. **Refresh the architecture artifact** - five commits stale (7.9).
12. **Parser ordering audit** (W23 3.1). Format 1's unanchored case-insensitive
    match shadowing Format 4 XML is the live risk. Format 2 still unread.
13. **PATH 2's four managed-agent auto-approve sites.** Largest outstanding
    confirmation-gate item, untouched for several windows.
14. **Repo root layout.** `tests\` exists and holds three tracked harnesses.
    Still owed: `scripts\`, `handoffs\`, `.gitignore`, `.gitattributes`.
    **`.gitattributes` is now better motivated: `imap_mail.py` is LF,
    `mailbox_tools.py` is CRLF, same package** (5.2). Roughly 157 untracked
    files remain. Delete the stray `"patch_testexec_v1 .py"` WITH THE SPACE;
    `patch_testexec_v1.py` (no space) is live and reads
    `app.state.bind_is_loopback` - check which is which first.
15. **The pending speech bundle** (section 9) - EIGHT windows carried.
16. **One retry of the 120B** on a bundle, to separate attachment failure from
    size limit.
17. **Lab item, not OpenJarvis:** the GitLab remote is plaintext HTTP, port 80,
    no TLS. Belongs with the Zero Trust work.

---

## 9. 550B CLOUD MODEL

Carried forward per the 08/29 pin. **USED THIS WINDOW**, first time in three.
Bundle: `mailbox_tools.py` + `imap_mail.py` whole, brief asking for every
collapsed multi-state result. Verdict in section 4: excellent at locating,
correctly calibrated on line numbers when told to count from the bundle, and
unreliable on severity because it does not chase deciding helpers.

`bundle_for_cloud.py` in the repo root, marker `openjarvis-cloudbundle-v1`.
Read-only, stdlib only, does not import openjarvis.

- `--set speech` and `--set prompt` defined, briefs already written.
- `--files <paths> --brief "<question>"` for ad hoc.
- Model: `openrouter/nvidia/nemotron-3-ultra-550b-a55b:free`.
- **Keep the clause "report CURRENT line numbers counted from this bundle, do
  not trust prior notes" in every brief.** It demonstrably worked.
- The 120B did NOT read the bundle. One retry still owed.

**STILL PENDING, NOT SUBMITTED: the speech bundle** covering
`speech_router.py`, `app.py`, `api_routes.py`. Brief asks for every duplicated
definition with current line numbers, a diff of the copies, which copy FastAPI
routes to versus which one Python globals resolve to, and every disagreement.
**Carried across NINE windows. Rebuild before submitting - the existing file is
from 08/30 and is stale.**

---

## 10. STANDING RULES IN FORCE

- **START OF WINDOW: reconcile the handoff against HEAD before acting on it.**
  `git --no-pager log --oneline -1 --decorate` plus a look for newer handoff
  files. (W25 2.1; confirming in W26-W30.) Branch is `main`.
- ALWAYS VERIFY. Never stack a second change on an unverified first one.
- **Build the instrument BEFORE the patch and require it to FAIL first.**
  (New, W30. See 7.8 entry 17.)
- FINISH THE THING BEFORE STARTING THE NEXT. No dangling processes. **W30 found
  the unchunked STORE mid-read and deliberately did not chase it.**
- Any patch script must assert its anchor is unique and refuse to write
  otherwise. (W29. Caught a real second site then; kept the move-path expunge
  call safe this window.)
- **A line number recorded before a patch to the same file is stale. Re-derive
  by content search; record the pattern, not the number.** (New, W30.)
- Take counts from the `N insertions(+), M deletions(-)` line, NEVER the
  `--stat` graph column. Four misreads on record.
- **Read the mechanism before naming the severity.** (W26 2.2.)
- **Mark evidence quality: READ / OBSERVED / ASSUMED.** When an assumption is
  promoted to READ, state what it MEANS. (W28 2.3.)
- A test derived from the call site rather than the mechanism cannot fail.
  (W27 2.3.)
- **Record what a test BYPASSED** (W27 2.5) and **have the instrument print that
  list itself** (W29).
- **Print what the collaborator was asked to do, not only what the function
  returned.** (W28. The IMAP verb log is why the expunge-reached fact is
  OBSERVED.)
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
- Tests must be non-interactive.
- Pin the detail of every window including negative results.
- Push to both remotes, always. `origin` is GitHub, `gitlab` is
  `http://172.16.33.126/root/openjarvis-desktop.git`.
- Token conservation on working sessions.
- Flag at 15 exchanges, then hand off. A flag, not a stop. **W30 flagged at 15
  and finished the commit and push before writing this.**
- Every handoff carries the SDD/SDP section, the EXECUTION PATHS register, and
  the 550B cloud-model section.
- **The SDP guard chapters need a plain-language explanation an eight-year-old
  could follow, alongside the technical detail.** (Gray 09/02.)

---

## 11. USEFUL PATHS

- Backend log: `C:\Users\Admin\AppData\Local\OpenJarvis\logs\backend.log`
- Agent log: `%LOCALAPPDATA%\OpenJarvis\logs\agent.log` (2.5MB x4) -
  RUNSTART/TURN/RUNEND/RAWGEN
- Engine log: `%LOCALAPPDATA%\OpenJarvis\logs\engine.log` (2MB x2) - RETRY400,
  no line has ever fired
- Start: `.\start-openjarvis.ps1` from the repo root. The `.\` is MANDATORY - a
  stale copy in `C:\Windows\System32` is on PATH and shadows it.
- `BIND-ASSERT` line in the backend log, emitted by `record_bind` at startup.
- Architecture artifact: `OPENJARVIS-ARCH-GATES-2026-08-31-v1.md`, repo root,
  untracked, FIVE commits stale.
- **Harnesses, all TRACKED, all run FROM THE REPO ROOT:**
  - `python .\tests\probe_h1_store_v1.py` - connector layer, move path
  - `python .\tests\probe_h1_toolprobe_v1.py` - tool layer, move path, 4/4
  - `python .\tests\probe_h1_emptyfolder_v1.py` - tool + connector, empty path,
    4/4, prints its own bypass list
  - None touch the network or the mailbox. All require CWD = repo root.
- Connector module path: `openjarvis.connectors.imap_mail`
- `CONFIRM_TOKEN` is exactly the string `CONFIRM DELETE`, importable from
  `openjarvis.tools.mailbox_tools`.
- **Rollback for this window:** `git revert a99c739`, or the file-level backup
  at `src\openjarvis\connectors\imap_mail.py.emptyfolder.bak` (untracked, still
  on disk):
  `Copy-Item .\src\openjarvis\connectors\imap_mail.py.emptyfolder.bak .\src\openjarvis\connectors\imap_mail.py -Force`
- W29 rollback still available: `git revert 7b3a47e`, or
  `src\openjarvis\tools\mailbox_tools.py.h1contract.bak`
