# HANDOFF 2026-09-02 I / WINDOW 31
# THE PROTECTED-SENDER GUARD WORKS. FOURTH-WINDOW DEBT PAID.
# And the `uids` path bypasses it completely - confirmed THREE independent ways.
# Plus: `protected_senders.json` REPLACES the built-in list, does not extend it,
# and its absence is SILENT. No such file exists anywhere in the tree today.
# ZERO changes to production code. One tracked harness, `fce0b78`, both remotes.

Predecessor: HANDOFF-2026-09-02-H-W30-EMPTYFOLDER-EXPUNGE-CLOSED.md
Host: Windows box. Shell: PowerShell 5.1. Working dir: `PS C:\Users\Admin\OpenJarvis>`.
Backend: 127.0.0.1:8010, ollama, qwen3-coder:30b, agent native_openhands.
Window shape: reconcile, four reads, two content searches, one 550B bundle,
one new harness, three harness runs, one commit, both remotes.
Backend NEVER STARTED - not needed. Zero writes to the mailbox. Zero network
calls to Yahoo. The harness is stdlib-only and socket-free.
**No file under `src\` was modified this window.**

---

## 0. ONE PARAGRAPH FOR THE NEXT WINDOW

W30's item 3 - the protected-sender guard, owed for four windows - is CLOSED and
the guard is SOUND on the path it covers. `tests\probe_h3_protected_v1.py`
(`fce0b78`, 235 insertions) drives the real `MailboxMoveToTrashTool.execute`
against a fake connector and grades on **what the connector was asked to do**,
not on what the tool reported. Five scenarios, 5/5. The load-bearing one is B:
four hits, two protected, and `move_to_trash` received exactly `['22','24']`.
The filter chain `:599 _sel = _keep` -> `:624 params["uids"] = _sel` is now
OBSERVED end to end. **Three findings the next window must carry: (1) the `uids`
parameter path reaches the destructive call with NO protected-sender check,
confirmed by branch read, by 550B trace, and by live execution; (2)
`protected_senders.json` REPLACES the built-in ten-entry list rather than
extending it, so a short override file silently strips protection from every
default; (3) that file does not exist anywhere in the tree, and its absence
produces no log line - `:574 is_file()` simply falls through.** The single
thing NOT to assume closed: whether the `uids` bypass is a design decision or a
defect. This window deliberately did not decide it.

---

## 1. WHAT LANDED

    5a8ade0  (W30 HEAD, start of this window)
    fce0b78  tests: exercise the protected-sender guard, move path
             (openjarvis-h3-protected-v1)             235 insertions(+)

Count from the `N insertions(+)` line, per the standing rule.

New and TRACKED: `tests\probe_h3_protected_v1.py`.
**Nothing under `src\` was touched. No `.bak` was created because no production
file was patched. Rollback for this window is `git revert fce0b78`, which only
removes a test.**

### 1.0 Start-of-window reconcile - PASSED

    5a8ade0 (HEAD -> main, origin/main, origin/HEAD, gitlab/main, gitlab/HEAD)

Newest handoff on disk was the W30 `-H-` file. Handoff and repository agreed.
**Sixth consecutive window where this check was cheap and confirming.** It has
never once caught a divergence. Keep it anyway - it is two seconds and it is the
only thing standing between an inherited assumption and a wrong instruction.

---

## 2. THE READS - THE GUARD, RIGHT THROUGH

`mailbox_tools.py`, `MailboxMoveToTrashTool`. Registered so the next window does
not re-read it. **Per the W30 rule, the SEARCH PATTERNS are recorded alongside
the numbers; the numbers are true as of `fce0b78` and stale the moment anyone
patches this file.**

Pattern that locates the whole guard:
`Select-String -Pattern "protected|Path\.cwd|protected_senders"`

- `:513` `execute(self, **params)`. Entry.
- `:515` `connector_for(account)`; `:516-517` None -> `_no_account_result`.
- `:524` `_from_addr` read from params. `:526` `_blocked_report = {}`.
- `:527` **`if _from_addr:` - THIS IS THE BRANCH THAT OWNS THE ENTIRE GUARD.**
- `:528-538` rejects `uids` **only when `from_addr` is ALSO present.**
- `:539-544` `folder` required when using `from_addr`.
- `:546` `conn.find_messages(folder=, from_addr=, limit=5000)`.
- `:554-562` builds `_sel` from hits. **DEAD - overwritten at `:599`.**
- `:563` marker `openjarvis-protected-senders-v1`.
- `:566-570` `_defaults`, ten entries, written lowercase.
- `:571` `_prot = _defaults`.
- `:573` **`_pf = _Path.cwd() / 'protected_senders.json'`.**
- `:574-577` if the file exists and parses to a non-empty list, `_prot` is
  **REPLACED**, entries lowercased.
- `:578-579` `except` logs only on UNREADABLE. **Absence logs NOTHING.**
- `:580-598` second loop; substring match `_p in _a`; matches go to
  `_blocked_report`, non-matches to `_keep`.
- `:599` `_sel = _keep`.
- `:602-612` all blocked and nothing kept -> `success=False`, error names the
  condition, `protected_blocked` carried.
- `:613-623` nothing matched at all -> `success=False`, `searched` count.
- `:624` **`params["uids"] = _sel`.** The filtered list is installed.
- `:625` `_resolved = len(_sel)`.
- `:627-663` `openjarvis-uid-typeguard-v1`; type check, digit check, non-empty.
- `:666-668` `_confirmed(params)` false -> dry-run plan.
- `:669` **`conn.move_to_trash(folder, uids, dry_run=False)`. Destructive.**
- `:678-684` projection, **gated on `_resolved`** - see 2.2.
- `:686-735` `openjarvis-h1-result-contract-v1`, the W29 four-state contract.
- `:734` `success=(_outcome == "complete")`.

### 2.1 The guard is TOOL-LAYER ONLY

`Select-String` for the same pattern across BOTH `mailbox_tools.py` and
`imap_mail.py` returned **zero hits in the connector.** The connector has no
concept of a protected sender. Anything that calls `ImapMailConnector`
directly - and W25 established that direct `connector_for()` calls are a real
pattern - is unguarded by construction. **READ, exhaustive.**

### 2.2 Two presence asymmetries, W30 5.4 family, both NEW

`:678` gates on `_resolved`, which is non-zero **only** on the `from_addr` path.

- `selected_by`, `from_addr`, `resolved_uid_count` are **ABSENT** on the `uids`
  path. Not empty, not None - absent.
- `:682` fires only when `_blocked_report` is truthy, so `protected_blocked` is
  **ABSENT** when nothing was blocked.

**Any consumer must use `.get()`.** That is now the third key in this family
after `store_failed` (W28 2.4) and `expunge_failed` (W30 5.4). **This is no
longer an occasional quirk - it is the house style of this file, and the SDP
should state it as a contract-wide rule rather than three separate footnotes.**

### 2.3 Dead code at `:554-562`

The first loop builds `_sel`; `:599` overwrites it unconditionally. Only the
second loop is load-bearing. Harmless today. Worth removing only because a
future reader will assume the first loop matters. Not touched - FINISH THE
THING.

---

## 3. THE BYPASS - CONFIRMED THREE INDEPENDENT WAYS

**`MailboxMoveToTrashTool.execute(folder=..., uids=[...], dry_run=False,
confirm="CONFIRM DELETE")` reaches `conn.move_to_trash` at `:669` without ever
entering the guard.**

| Method | Evidence |
|---|---|
| Branch read | Guard body is entirely inside `:527 if _from_addr:`. `:528` rejects `uids` only when `from_addr` is ALSO given. **READ** |
| Exhaustive search | Only `protected` sites in the file are `:563-682`, all inside that branch. Zero in `imap_mail.py`. **READ** |
| Live execution | Scenario D: `find_messages` NEVER CALLED; `move_to_trash` received `['41','42']`, both protected senders. **OBSERVED** |
| 550B trace | Independently identified Combination A as reaching `:669` unguarded. **CORROBORATING, not deciding** |

### 3.1 It is coherent, which is why it must be DECIDED and not just fixed

`:521-523` states the design intent: the model passes a sender substring and the
tool resolves it to uids **so that no uid list ever crosses the model.**
Under that intent, `from_addr` is the model-facing path and `uids` is for
callers that already hold uids from a prior `find_messages`. The guard being on
the model-facing path is then deliberate, not an oversight.

**But nothing enforces that split.** `uids` is a public parameter on the same
tool with the same confirm token, and the model can populate it - W23 already
recorded the model fabricating uid lists, which is why `openjarvis-uid-typeguard-v1`
exists at all. **The typeguard proves the model DOES reach this parameter.**

**BOARD ITEM, NOT DECIDED THIS WINDOW.** Three options, in ascending cost:
1. Document it as intended and state the premise in the SDP.
2. Run the guard on the `uids` path too - requires a header fetch per uid to
   learn `from_addr`, so it costs a round trip and changes the tool's cost model.
3. Refuse `uids` from model-originated calls entirely, keeping it for internal
   callers - needs a caller-identity concept that does not currently exist.

Scenario D pins the CURRENT behaviour, so whichever is chosen, **closing the
bypass will announce itself as a D FAIL rather than passing silently.**

---

## 4. THE OVERRIDE FILE - A NEW HAZARD, NOT PREVIOUSLY RECORDED

### 4.1 It REPLACES, it does not extend

`:576-577`: if the JSON parses to a non-empty list, `_prot` becomes that list
**entirely.** The ten built-in defaults are discarded.

Scenario E proved this by execution. Override file contained one address. Result:
`notify@r.groupon.com` - a BUILT-IN protected sender - was **moved**, while the
override-only address was blocked. **OBSERVED.**

**Consequence: anyone who writes a short `protected_senders.json` believing they
are adding a sender silently removes protection from all ten defaults,
including `cdgray33@yahoo.com`.** That is Gray's own address and the most
consequential entry in the list.

### 4.2 Its absence is SILENT

`:574 if _pf.is_file():` - false means fall through with `_prot = _defaults` and
**no log line.** The `except` at `:578` catches unreadable, not absent. There is
no way to tell from the logs whether an override was loaded, not found, or never
intended. **READ.**

### 4.3 The file does not exist

`Get-ChildItem -Path . -Filter protected_senders.json -Recurse` over the whole
tree returned **nothing.** **The built-in ten entries are what is in force
today, and always have been.** **READ + OBSERVED.**

Combined with `Path.cwd()`, this means the override is CWD-relative, so even
once written it loads only when the backend is started from the directory
holding it. W25 already recorded that the backend is started manually from the
repo root via `.\start-openjarvis.ps1`, so repo root is the effective location -
but nothing documents or enforces that.

### 4.4 Matching semantics - noted, deliberately not adjudicated

Substring, case-insensitive on one side only: JSON entries are lowercased at
`:577`, `_defaults` are not and merely happen to be written lowercase. `_a` is
lowercased at `:589`, so a mixed-case entry in `_defaults` would silently never
match. Entries `'account@'` and `'ratings@'` match very broadly.

**Over-blocking is the fail-safe direction**, so this is a note, not a defect.
It becomes material once consolidation runs volume through the guard, because
broad matches will block messages the operator expected to move and the
`protected_blocked` report is the only signal.

---

## 5. THE 550B RUN

Bundle: `mailbox_tools.py` alone, whole. 39405 bytes, ~9851 tokens.
`CLOUDBUNDLE-adhoc-20260902-092154.md`, repo root, untracked.

Brief: enumerate every parameter path reaching a destructive operation, state
for each whether it passes `openjarvis-protected-senders-v1`, name explicitly
any path that does not, list every early return and its trigger, **report
CURRENT line numbers counted from this bundle and do not trust prior notes**,
and **do not assess severity - only locate and enumerate.**

### 5.1 Grading

| Finding | Verdict |
|---|---|
| Combination A (`uids`) bypasses the guard | **CORRECT - corroborates, see 3** |
| Combination B (`from_addr`) passes the guard | **CORRECT - but rested on `:624`, which it asserted and I then READ** |
| Combination C (`empty_folder` has no check) | **DISCOUNTED - already W30 5.5, and it is a design consequence, not a finding** |
| Early-return tables, both tools | **CORRECT, complete, matched the read** |
| Line numbers | **CORRECT - no stale `:689`/`:765` inheritance** |

### 5.2 What it missed

**It never accounted for `:682`.** Its model of the guard ended at `:599`, so it
had nothing to say about what happens to `_blocked_report` on a PARTIAL block -
which is exactly the layered-projection family from W30 7.3. Consistent with
W30 4.4: it reasons about the block in front of it and does not follow a value
past the branch that produced it.

### 5.3 The severity instruction worked

Adding **"do not assess severity, only locate and enumerate"** produced a
cleaner artifact than W30's run. It stayed inside its competence and did not
need to be argued down. **Keep that clause alongside the line-number clause in
every future brief.** Two clauses now, both earned:

- "report CURRENT line numbers counted from this bundle, do not trust any line
  number from prior notes"
- "do not assess severity, only locate and enumerate"

---

## 6. THE HARNESS

`tests\probe_h3_protected_v1.py`, marker `openjarvis-h3-protected-v1`, stdlib
only, run from the repo root, non-interactive, socket-free.

**REAL:** the whole `MailboxMoveToTrashTool.execute` body, the real guard, the
real uid typeguard, the real `_confirmed`, the real W29 result contract.
**FAKE:** only the object returned by `connector_for()`, swapped by
monkeypatching `MT.connector_for` and restored in a `finally`.

**It grades on what the connector was ASKED to do** - `conn.moved_uids` - not on
what the tool reported. That is the W28 rule applied as the primary assertion
rather than as a diagnostic print.

| # | Scenario | Result |
|---|---|---|
| A | `from_addr`, ALL hits protected | `move_to_trash` NEVER CALLED. `success=False`, error names the condition. |
| B | `from_addr`, MIXED 2 of 4 protected | **`move_to_trash(uids=['22','24'])`.** The two protected uids never reached the connector. |
| C | `from_addr`, NONE protected | Both uids passed. `protected_blocked` **ABSENT**, not empty. |
| D | `uids` direct, protected senders | **BYPASS. `find_messages` never called, both uids moved.** |
| E | override file present | Built-in list **REPLACED**. Groupon moved, override address blocked. |

Scenario E writes `protected_senders.json` to CWD, **refuses to run if the file
already exists**, and removes it in a `finally` with a loud warning if removal
fails. Exchange-6 evidence says it does not exist, and the post-run tree is
clean.

### 6.1 The harness prints its own bypass list

Per W27 2.5 and W29. Printed on every run so it cannot drift from the code:
no real IMAP server; `find_messages` is a stub so server-side search correctness
is untested; `from_addr` values come from the stub, not parsed headers;
`empty_folder` is not covered; substring breadth is exercised but not graded;
**and scenario D asserts the CURRENT bypass, so a D FAIL means the bypass was
closed, not that the harness broke.**

---

## 7. NEGATIVE RESULTS - PINNED PER THE W30 RULE

**A window that changed no production code still produced knowledge. This
section is the point of the window.**

### 7.1 The guard is NOT broken. Run 1 read 1/5 and that was MY fault.

First run: four FAILs, **every one with the identical single mismatch
`success=False want=True`.** `moved_uids` matched in all five. Presence matched
in all five.

Cause: my fake `move_to_trash` returned `applied`/`moved`/`folder`/`uids` and
omitted `copied_count` and `deleted_count`. `:692-693` defaulted both to 0,
`:700` set `_outcome = "no_op"`, `:734` correctly returned `success=False`.

**The W29 contract was working exactly as designed. The fake was speaking the
pre-W29 dialect.** The failing run was an unplanned confirmation that `:734`
refuses to report success when the connector payload lacks the counts.

**METHODOLOGY ENTRY 20: a fake must satisfy the real CONSUMER of its return
value, not the caller's signature.** Mine satisfied `move_to_trash`'s parameter
list perfectly and failed its result contract. This is the W30 3.2 hazard one
layer up - and it failed LOUDLY rather than passing for the wrong reason, which
is the good direction and worth noting as such.

### 7.2 Run 2 was byte-identical, and that was NOT a code problem

Second run produced output identical to the first, including scenario A's PASS.
The corrected file had never reached disk: the browser saved the re-delivered
download as `probe_h3_protected_v1 (1).py`, and `Copy-Item` had copied the
original again.

Caught by `Select-String -Pattern "copied_count"` against the copy in `.\tests\`
returning **0**. One command distinguished "my fix is wrong" from "my fix is not
there", and those demand completely different responses.

**METHODOLOGY ENTRY 21: a file delivered for download a second time under the
same name is RENAMED by the browser. Copy by explicit source filename, and
verify the copy by content search - not by timestamp, not by assumption.**
**Corollary: byte-identical output across two runs is evidence the code did not
change, NOT evidence the behaviour is stable.**

### 7.3 `empty_folder` having no protected-sender check is NOT a defect

The 550B reported it. Already recorded W30 5.5. It is a **design consequence**:
the operation is folder-scoped and takes no sender selector, so there is nothing
for a per-sender guard to filter. **State it in the SDP as a decision with its
reasoning.** Do not open it as a board item; that would be the third window it
has been re-raised.

### 7.4 MY PROCESS FAILURE - a heredoc in a runnable block

I issued a patch command using a PowerShell here-string (`@"..."@`) inside
`python -`. **This directly violates the standing rule "no heredocs, no `<<`, no
`$(...)`".** The `@"` was not at end-of-line, PowerShell did not form a
here-string, `python -` got no stdin, and Gray was dropped into an interactive
REPL he could not exit with `exit()` because the input had left Python inside an
unterminated block. Escape: Ctrl+C, then Ctrl+Z Enter.

**Residual risk, and how it was closed:** the pasted lines went into the REPL,
and they included a write to `.\tests\probe_h3_protected_v1.py`. Whether it
executed was never determined. It was closed by **overwriting that exact file
wholesale** with a known-good copy - the script touched no other path, and
`copied_count` going 0 -> 2 confirmed the final state. The final 5/5 ran against
a file of verified provenance.

**The rule exists because of exactly this. Deliver a FILE for download instead
of an in-place patch command whenever the content contains quotes.** That is
what should have happened, and it is what happened on the retry.

---

## 8. EXECUTION PATHS REGISTER

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
- Frontend submit F-A typed, F-B voice, F-C option relay (DEAD)
- `_extract_tool_call` order: native, Format 1 (case-insensitive, UNANCHORED),
  Format 2 (unread), Format 4 (XML, shadowed by 1), Format 3 (bare JSON)
- `mailbox_empty_folder` tool + connector - full row set in W30 section 6

### EXTENDED THIS WINDOW - `mailbox_move_to_trash`, BOTH PARAMETER PATHS

**This tool has TWO distinct execution paths and they have different safety
properties. Register them separately.**

| Property | PATH M-A (`uids`) | PATH M-B (`from_addr`) | Evidence |
|---|---|---|---|
| Entry | `:513 execute(**params)` | `:513 execute(**params)` | READ |
| Connector acquisition | `:515 connector_for(account)` | same | READ |
| Guard branch entered | **NO - `:527` false** | YES | **READ + OBSERVED (new)** |
| `find_messages` called | **NO** | `:546`, limit 5000 | **OBSERVED (new)** |
| Protected-sender check | **NONE** | `:563-599` | **READ + OBSERVED (new)** |
| uid origin | **caller-supplied, unvalidated as to sender** | tool-resolved from server search | **READ (new)** |
| uid typeguard | `:627-663`, applies to BOTH | same | READ |
| Confirm interlock | `:666 _confirmed(params)`; `dry_run=False` + exact `CONFIRM DELETE` | same | READ |
| Gate callback | **none in path** - no Defect 6 gate | **none in path** | OBSERVED |
| Destructive call | `:669` | `:669` | READ |
| `selected_by` in payload | **ABSENT** (`:678` gated on `_resolved`) | `"from_addr"` | **OBSERVED (new)** |
| `protected_blocked` | **ABSENT always** | present only when non-empty | **OBSERVED (new)** |
| Result contract | `:686-735`, four-state, identical | same | READ + OBSERVED |
| Human present | not required | not required | OBSERVED |

**The single most important row is "Protected-sender check". The same tool, the
same confirm token, two different safety guarantees, distinguished only by which
optional parameter the caller populated.**

---

## 9. SDD / SDP - WHAT THIS WINDOW OWES THE DOCUMENT

### 9.1 The guard chapter can now be written from OBSERVATION

Every claim below is backed by a harness run, not by reading:

- The guard filters at the correct boundary - protected uids never reach the
  connector, they are not filtered downstream or merely reported.
- All-blocked produces a distinct, honest failure that names the reason.
- Partial-block succeeds on the remainder and reports what was withheld.
- Clean cases carry no `protected_blocked` key at all.

### 9.2 The presence-asymmetry contract - promote to a RULE

Three keys now (`store_failed`, `expunge_failed`, `protected_blocked`) plus the
whole `:678-684` group. **The SDP should state once, as a contract-wide rule:
optional result keys are ABSENT rather than falsy, and every consumer -
including the model prompt - must treat absence as the default case.** Stop
footnoting it per-key.

### 9.3 GRAY'S STANDING INSTRUCTION, 09/02 - PLAIN-LANGUAGE GUARD CHAPTER

Extend, do not replace. W29's four entries and W30's "emptying the bin" stand
unchanged. **New this window:**

**The do-not-touch list, in plain language.** Jarvis keeps a short list of
people whose mail must never be thrown away - things like account notices,
order confirmations, and Gray's own address. When you ask Jarvis to clear out
mail from a sender, it looks at every message it found, sets aside anything from
somebody on that list, and only throws away the rest. If EVERYTHING it found was
on the list, it throws away nothing at all and tells you why. It always tells
you who it set aside and how many.

**The part that matters and is easy to miss.** There are two ways to ask Jarvis
to throw mail away. If you say "get rid of the mail from this sender", Jarvis
does the checking described above. But if you hand Jarvis a specific list of
messages and say "throw away exactly these", **it does not check the list at
all.** It assumes you already looked. That is like the difference between
telling somebody "clear out the junk drawer, but leave anything important" and
handing them a stack of papers and saying "shred these". In the second case they
shred what you handed them. **Right now nothing stops the wrong stack from being
handed over.**

**The second thing that is easy to miss.** The do-not-touch list can be replaced
by writing your own list in a file. But writing your own list **throws the
built-in one away** - it does not add to it. So if you write a file with one
name in it because you wanted to protect one more person, you have just removed
protection from the ten who were already protected. Nobody is told this
happened. Right now no such file exists, so the built-in list is what is
protecting you.

**The short version for the chapter opener: a guard that only runs on one of the
two doors is not a guard, it is a habit. And a list you can replace by accident
is worse than a list you cannot change at all.**

### 9.4 Carried correction, STILL OWED, unchanged

SDP revB:504 and revC:597 assert `requires_confirmation=True` for
`mailbox_move_to_trash`. Both WRONG (W26 2.1). Replace with: the flag is
deliberately unset, the reason is in the `mailbox_tools.py` header, the
interlock is `dry_run=False` plus the exact `CONFIRM DELETE` token, and the
stated premise predates 6c and is untested. Carry the reasoning, do not flip the
boolean. **Applies to BOTH destructive tools** (W30 7.5). **Confirmed again this
window by execution: `_confirmed(params)` at `:666` with no gate callback
anywhere in either path.**

### 9.5 Defect 6 confirmation gate - GREAT DETAIL per Gray's standing instruction

Unchanged from W26-W30. Registry: write-once, 409 on re-decision, TIMEOUT
internal only. Payload: seven fields; `turn_id` from `CURRENT_TURN_ID` set by
`openjarvis-agent-log-v1` - a diagnostic marker load-bearing on a
safety-critical payload, still a design smell needing its own owner. Transport:
EventBus -> ws_bridge -> bare WS client; delivery proven W20, payload integrity
W21. Redaction CLOSED. TTL 120 s governs the WAIT FOR A HUMAN, not the execution
that follows. **Neither mailbox tool uses this gate, now OBSERVED rather than
read - the harness drove both paths to the destructive call with no gate
interaction. PATH 3 remains the only end-to-end proof.** Plain-language
companion **STILL NOT WRITTEN - now THREE windows owed.**

### 9.6 Defect 1 - keep the two mechanisms separate

(a) The model claims actions it never invoked: parser and prompt problem, still
open. (b) The tool mis-reports and the model accurately relays it - closed for
the destructive mailbox path as a whole, pending the `imap_mail:647` residue.
**Nothing this window changed either. The guard is a separate axis from Defect 1
and should not be filed under it.**

### 9.7 Verification methodology chapter - two new entries (running total 21)

20. **A fake must satisfy the real CONSUMER of its return value, not the
    caller's signature.** A stub matching the parameter list perfectly can still
    fail the contract that reads its output. When a harness fails uniformly with
    one mismatch class across every scenario that reached the collaborator,
    suspect the stub's return shape before suspecting the code.
21. **A re-delivered download is RENAMED by the browser.** Copy by explicit
    source filename and verify by content search. **Byte-identical output across
    two runs is evidence the code did not change, not evidence of stability.**

### 9.8 Architecture artifact

`OPENJARVIS-ARCH-GATES-2026-08-31-v1.md`, repo root, untracked, cut at
`6c172d1`, now **SIX commits stale** (`801869c`, `7b3a47e`, `0b17b35`,
`a99c739`, `5a8ade0`, `fce0b78`). Next version must add everything W30 listed
**plus the M-A / M-B path split from section 8, which is an architecture fact,
not a detail.** Ports/protocols/encoding per the 08/22 rule. Downloadable
standalone file for the wiki.

---

## 10. NEXT ACTIONS, ORDERED

1. **DECIDE the `uids` bypass** (section 3.1). Newly ranked first because it is
   now fully characterised, it is on the most destructive tool, and item 2 below
   is gated on knowing whether the guard applies to bulk operations. Three
   options are laid out with costs. **This is a decision, not an investigation -
   it needs Gray, not a window.**
2. **Folder consolidation, 53 to 18-19** (W27 section 4). Gray confirmed this is
   the direction. **Item 3 is no longer blocking it - the guard is proven.**
   Remaining gate is decision 1, since consolidation drives `from_addr`
   selection at volume and the answer determines whether bulk moves are guarded.
   Mapping table first, dry run per source folder, no bulk operation. Watch
   `AT&-T` (modified-UTF7 leaking), and the near-duplicate pairs `Draft`/`Drafts`,
   `Social`/`Social_Media`, `Receipts_Confirmations`/`Inbox/Receipts`,
   `Junk`/`Spam`/`Bulk`. **NO CONFIRMED DELETE FOLDER TOOL EXISTS** - establish
   whether one does before planning the removal phase.
3. **`protected_senders.json` - write one, or document the built-ins as
   canonical.** New this window. The REPLACE semantics plus the silent absence
   plus `Path.cwd()` make this a trap for whoever touches it first. Minimum:
   a comment at `:566` stating the file replaces rather than extends. Better: a
   log line on both branches of `:574` so the loaded list is knowable from the
   logs.
4. **The unchunked STORE at `imap_mail.py:709`.** Same payload shape Yahoo
   already rejected on the move path. Reliability, not safety - STORE is
   checked, so it fails honestly. Becomes materially more likely once
   consolidation makes Trash large. The proven ladder is in the same file.
5. **`imap_mail:647` `plan["applied"] = deleted > 0`.** Connector-level residue
   under the fixed tool, still in the payload the model reads. Remove or
   redefine to agree with the tool's `outcome`.
6. **Option B for `empty_folder`: re-verify by re-listing** after expunge,
   report `remaining_count`, derive outcome from observed truth. The W30 harness
   already has the scenario slot.
7. **`deleted_count` chunk-granularity** (W28 2.3). A chunk STORE returning OK
   credits all its uids, so `deleted_count` can overstate - turning a genuine
   `partial` into a false `complete`.
8. **`folder == trash` branch** (`imap_mail.py:591-592`), sets `copied =
   list(uids)` with no COPY at all. Never exercised, four windows.
9. **Retest the W26 2.1 premise** - does the confirm callback now reach the
   mailbox path after 6c? Decides whether `requires_confirmation` can be set at
   all, for both destructive tools.
10. **550B sweep: every IMAP verb whose return is discarded** (W30 7.2).
    Mechanical, cheap, and the class that produced the W30 defect. Bundle
    `imap_mail.py` whole. **Use both brief clauses from 5.3.**
11. **Write the plain-language companion for the Defect 6 gate chapter** (9.5).
    THREE windows owed now.
12. **Refresh the architecture artifact** - six commits stale (9.8).
13. **Parser ordering audit** (W23 3.1). Format 1's unanchored case-insensitive
    match shadowing Format 4 XML is the live risk. Format 2 still unread.
14. **PATH 2's four managed-agent auto-approve sites.** Largest outstanding
    confirmation-gate item, untouched for several windows.
15. **Repo root layout.** `tests\` now holds FOUR tracked harnesses. Still owed:
    `scripts\`, `handoffs\`, `.gitignore`, `.gitattributes` (`imap_mail.py` is
    LF, `mailbox_tools.py` is CRLF, same package). Roughly 157 untracked files.
    **Now also: `CLOUDBUNDLE-adhoc-*.md` files accumulate in the repo root and
    should be gitignored or moved.** Delete the stray `"patch_testexec_v1 .py"`
    WITH THE SPACE; `patch_testexec_v1.py` (no space) is live.
16. **The pending speech bundle** (section 11) - NINE windows carried.
17. **One retry of the 120B** on a bundle, to separate attachment failure from
    size limit.
18. **Lab item, not OpenJarvis:** the GitLab remote is plaintext HTTP, port 80,
    no TLS. Belongs with the Zero Trust work.

---

## 11. 550B CLOUD MODEL

Carried forward per the 08/29 pin. **USED THIS WINDOW.** Bundle:
`mailbox_tools.py` whole, brief asking for every parameter path to a destructive
operation and whether each passes the guard. Verdict in section 5: excellent at
enumeration and early-return tables, correctly calibrated on line numbers, and
**noticeably better behaved when explicitly told not to assess severity.**

`bundle_for_cloud.py` in the repo root, marker `openjarvis-cloudbundle-v1`.
Read-only, stdlib only, does not import openjarvis. Prints the bundle path,
byte count, and approximate token count; writes nothing else.

- `--set speech` and `--set prompt` defined, briefs already written.
- `--files <paths> --brief "<question>"` for ad hoc.
- Model: `openrouter/nvidia/nemotron-3-ultra-550b-a55b:free`.
- **BOTH clauses in every brief:** "report CURRENT line numbers counted from this
  bundle, do not trust prior notes" AND "do not assess severity, only locate and
  enumerate."
- Delivery: `Get-Content <bundle> -Raw | Set-Clipboard` then paste. The brief is
  embedded in the bundle, so no separate prompt is needed.
- The 120B did NOT read the bundle. One retry still owed.

**STILL PENDING, NOT SUBMITTED: the speech bundle** covering
`speech_router.py`, `app.py`, `api_routes.py`. Brief asks for every duplicated
definition with current line numbers, a diff of the copies, which copy FastAPI
routes to versus which one Python globals resolve to, and every disagreement.
**Carried across NINE windows. Rebuild before submitting - the existing file is
from 08/30 and is stale.**

---

## 12. STANDING RULES IN FORCE

- **START OF WINDOW: reconcile the handoff against HEAD before acting on it.**
  `git --no-pager log --oneline -1 --decorate` plus a look for newer handoff
  files. (W25 2.1; confirming W26-W31.) Branch is `main`.
- ALWAYS VERIFY. Never stack a second change on an unverified first one.
- **Build the instrument BEFORE the patch and require it to FAIL first.** (W30.)
- FINISH THE THING BEFORE STARTING THE NEXT. No dangling processes. **W31 found
  the dead loop at `:554-562` and the matching-semantics asymmetry mid-read and
  deliberately did not chase either.**
- Any patch script must assert its anchor is unique and refuse to write
  otherwise. (W29.)
- **A line number recorded before a patch to the same file is stale. Re-derive
  by content search; record the pattern, not the number.** (W30.)
- Take counts from the `N insertions(+), M deletions(-)` line, NEVER the
  `--stat` graph column. Four misreads on record.
- **Read the mechanism before naming the severity.** (W26 2.2.)
- **Mark evidence quality: READ / OBSERVED / ASSUMED.** (W28 2.3.)
- A test derived from the call site rather than the mechanism cannot fail.
  (W27 2.3.)
- **Record what a test BYPASSED** (W27 2.5) and **have the instrument print that
  list itself** (W29).
- **Print what the collaborator was asked to do, not only what the function
  returned** (W28) - **and where possible ASSERT on it, not just print it**
  (W31, section 6).
- **A fake must satisfy the real CONSUMER of its return value.** (New, W31.)
- **A re-delivered download is renamed. Copy by explicit source filename and
  verify by content search.** (New, W31.)
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
  **VIOLATED IN W31 - see 7.4. Deliver a FILE for download instead of an
  in-place patch command whenever the content contains quotes.**
- No non-ASCII symbols in replies.
- Tests must be non-interactive.
- Pin the detail of every window including negative results.
- Push to both remotes, always. `origin` is GitHub, `gitlab` is
  `http://172.16.33.126/root/openjarvis-desktop.git`.
- Token conservation on working sessions.
- Flag at 15 exchanges, then hand off. A flag, not a stop. **W31 flagged at 15
  and finished the verification, commit and push before writing this.**
- Every handoff carries the SDD/SDP section, the EXECUTION PATHS register, and
  the 550B cloud-model section.
- **The SDP guard chapters need a plain-language explanation an eight-year-old
  could follow, alongside the technical detail.** (Gray 09/02.)

---

## 13. USEFUL PATHS

- Backend log: `C:\Users\Admin\AppData\Local\OpenJarvis\logs\backend.log`
- Agent log: `%LOCALAPPDATA%\OpenJarvis\logs\agent.log` (2.5MB x4) -
  RUNSTART/TURN/RUNEND/RAWGEN
- Engine log: `%LOCALAPPDATA%\OpenJarvis\logs\engine.log` (2MB x2) - RETRY400,
  no line has ever fired
- Start: `.\start-openjarvis.ps1` from the repo root. The `.\` is MANDATORY - a
  stale copy in `C:\Windows\System32` is on PATH and shadows it.
- `BIND-ASSERT` line in the backend log, emitted by `record_bind` at startup.
- Architecture artifact: `OPENJARVIS-ARCH-GATES-2026-08-31-v1.md`, repo root,
  untracked, SIX commits stale.
- **Harnesses, all TRACKED, all run FROM THE REPO ROOT:**
  - `python .\tests\probe_h1_store_v1.py` - connector layer, move path
  - `python .\tests\probe_h1_toolprobe_v1.py` - tool layer, move path, 4/4
  - `python .\tests\probe_h1_emptyfolder_v1.py` - tool + connector, empty path,
    4/4, prints its own bypass list
  - `python .\tests\probe_h3_protected_v1.py` - **protected-sender guard, both
    parameter paths, 5/5, prints its own bypass list. Scenario D asserts the
    CURRENT bypass and will FAIL when the bypass is closed - that is intended.**
  - None touch the network or the mailbox. All require CWD = repo root.
- Connector module path: `openjarvis.connectors.imap_mail`
- `CONFIRM_TOKEN` is exactly the string `CONFIRM DELETE`, importable from
  `openjarvis.tools.mailbox_tools`.
- **Protected senders: ten built-in defaults at `mailbox_tools.py:566-570`.
  `protected_senders.json` DOES NOT EXIST anywhere in the tree. If created, it
  must sit in the backend's CWD (effectively the repo root) and it REPLACES the
  built-ins.**
- **Rollback for this window:** `git revert fce0b78`. Removes only a test file;
  no production code was changed, so there is no `.bak` for W31.
- W30 rollback still available: `git revert a99c739`, or
  `src\openjarvis\connectors\imap_mail.py.emptyfolder.bak`
- W29 rollback still available: `git revert 7b3a47e`, or
  `src\openjarvis\tools\mailbox_tools.py.h1contract.bak`
