# SDP SOURCE EXTRACT W82 part 6 (deduplicated by section hash)
### [ARCHIVE-W59-2026-09-14.md] 5. HAZARDS FOUND
**THE .NET RESOLVER TRAP, HIT FOR THE FIFTH TIME.** `[IO.File]::ReadAllBytes`
given a relative path resolved it against `C:\WINDOWS\system32`. Gray called
for it to be pinned permanently and it now is.
The second half is the dangerous half and is new to the record: **when the
.NET call failed mid-block, `$b` retained a value from earlier in the
session** - a `Get-ChildItem` result for `BRIEF-W57-2026-09-14.md` - and the
rest of the block ran against it, printing `NON-ASCII BYTE COUNT: 0` for a
file that has 17. A failed command in the middle of a block does not stop the
block, and PowerShell variables are session-scoped. **The output was
confident, well-formatted, and completely wrong.** Reissue the whole block
after any mid-block failure; never re-run the failed line alone.
**`_bak\` POISONS REPO-WIDE FILE SEARCHES.** Three stale `ChatArea.tsx`
copies from 20260718 sit in `_bak\patch_*\`. The first patcher found four
ChatArea files and aborted, correctly. Frontend work must be scoped to
`C:\Users\Admin\OpenJarvis\frontend`.
**`cli\ask.py:356` REMAINS AN UNGUARDED CONSENT PATH.** A bare `lambda: True`
with no ConfirmPolicy, meaning a real deletion on that path is approved
silently and leaves no attributable trace. Carried unchased from W58 into
W60. This is the only known path where the W58 flag flip does not produce
either a human gate or a POLICY line. It is a consent hole.
**THE GATE PROMPT STILL DOES NOT NAME ITS SCOPE.** It fires before
`from_addr` is resolved and before the protected-senders filter runs, so on a
sender-based call the human is consenting to a substring, not to a count.
`_args_digest` caps at 400 chars, so a long uid list arrives truncated. Not a
correctness defect - the gate gates the right calls - but it is the gap
between "a human approved" and "a human approved knowingly", and section 3
just made the model's count report the only thing closing it.
---
### [ARCHIVE-W59-2026-09-14.md] 6. SDD / SDP FEED
**For the SDP guard chapter, in plain language.** Before this window there
were two different ways the program asked permission to throw mail away. One
was the assistant typing a question into the chat and waiting for you to type
a magic phrase back. The other was a real button that appears on screen and
actually holds the deletion still until somebody presses it. Having both was
confusing, because the typed phrase only proved you agreed with a
DESCRIPTION of the plan, while the button proves you agreed with the exact
thing that is about to run. We kept the button and removed the typed phrase.
The assistant still TELLS you how many messages it found - that part matters,
because the button by itself does not show you a count - but it no longer
asks you to approve twice in two different ways.
**For the SDD architecture chapter.** Consent for destructive mailbox actions
now has exactly one enforcement point: `BaseTool.needs_confirmation(params)`
in `tools\_stubs.py`, evaluated with `tool.spec.requires_confirmation`. The
model-side interlock (`dry_run=False` plus the exact `CONFIRM DELETE` token)
remains in force but is explicitly NOT a consent mechanism - it is a
contract guard the model satisfies itself, and W57 established that
distinction. Documentation must not describe the token as user approval.
**Evidence quality note for the SDD.** Both of this window's substantive
conclusions came from instruments that already existed: `dispatch.log` for
the gate behavior, and a byte dump for the encoding. Neither required new
tooling. This is the 09/06 search-the-schema rule paying out twice in one
window, and it belongs in the SDD as an argument for the tooling register
itself.
---
### [ARCHIVE-W59-2026-09-14.md] 7. REGISTER DELTAS
Append to the W57 registers; do not rewrite them.
**DIAGNOSTIC TOOLING REGISTER - delta:**
- `tools\patch_confirmprompt_move.py` - v1, ABORTED on a guessed glyph form.
  Kept as the worked example of why byte-anchoring beats form-guessing.
- `tools\patch_confirmprompt_move2.py` - v2, byte-anchored, PATCH OK. Locates
  its own targets, refuses on any anchor miss, reports CRLF/LF and non-ASCII
  deltas. Output: stdout only.
- `tools\patch_prose_ask.py` - byte-anchored, CRLF-aware, PATCH OK. One
  mis-specified verify line, documented in section 3.
- Ad-hoc byte-dump block (not a file): prints every non-ASCII byte of a file
  with surrounding context. Cheap, decisive, worth keeping as a pattern.
- `dispatch.log` confirmed again as the instrument of record for gate
  behavior. ATTEMPT / GATEPRED / OUTCOME with `reason=` is sufficient to
  reconstruct a consent sequence without reading any source.
**EXECUTION PATH REGISTER - delta:**
- Chat path: gate LIVE and observed firing per-sender, with `reason=OK` on
  approval and `reason=GATE_TIMEOUT` at 120 s on no answer. Human present:
  required, and its absence is now a known log signature.
- `cli\ask.py:356`: bare `lambda: True`, no ConfirmPolicy, human ABSENT, no
  trace emitted. Unguarded. See section 5.
**LOGGING TOPOLOGY - delta:** no change. `dispatch.log` in
`%LOCALAPPDATA%\OpenJarvis\logs\` remains readable and was read directly.
**PROGRAM GOAL - delta:** consent for destructive mailbox actions is now
single-mechanism and human-gated on the chat path. Still zero connector
credentials across all 24 tools.
---
### [ARCHIVE-W59-2026-09-14.md] 8. COMMITS AND ARTIFACTS
| commit | content |
|--------|---------|
| `bed1072` | argument-aware gate - `_stubs.py`, `mailbox_tools.py` (W58 source) |
| `2490f94` | ConfirmPrompt to `App.tsx`; two mojibake strings cleared |
| `3f4a978` | model-side prose confirmation ask removed |
All three on `origin` (GitHub) and `gitlab` (172.16.33.126).
Exe: `frontend\src-tauri\target\release\openjarvis-desktop.exe`, 19,027,968 B,
built 13:36:37, 2m 10s compile. Build exited 1 on the signing-key error,
which is normal and occurs after bundling.
Backups: `.bak_confirmapp_20260914_133200` (App.tsx, ChatArea.tsx),
`.bak_proseask_20260914_135119` (mailbox_tools.py),
`.bak_argaware_20260914_083411` (W58, both source files).
Scripts moved into `tools\` this window: `patch_argaware_gate.py`,
`probe_argaware_gate.py`, `validate_gates_w57.py`, `build_archive_w57.py`.
Repo root is clear of loose scripts.
### [ARCHIVE-W60-2026-09-15.md] NEVER OPENED WHOLE. EXTRACT A NAMED SECTION.
Carries ONLY W60's new material and deltas. ARCHIVE-W57 remains the single
source for the five carried registers.
```powershell
$f='ARCHIVE-W60-2026-09-15.md'; $t=Get-Content $f; $s=($t|Select-String '^## 3\.'|Select-Object -First 1).LineNumber; $e=($t|Select-String '^## 4\.'|Select-Object -First 1).LineNumber; $t[($s-1)..($e-2)]
```
### [ARCHIVE-W60-2026-09-15.md] SECTION INDEX
1. Window narrative
2. Evidence
3. Negative results and dead theories
4. Hazards found
5. SDD / SDP feed
6. Execution paths delta
7. Diagnostic tooling register delta
8. Action 3 - the three options, in full
9. Process failures this window
---
### [ARCHIVE-W60-2026-09-15.md] 1. WINDOW NARRATIVE
W60 opened on one unverified thing from W59: the `ConfirmPrompt` move to
`App.tsx` was committed and built but had never been seen firing.
The first log read showed `dispatch.log` ending at 10:27 the previous day -
a clean empty baseline, since the file appends across restarts. Whatever
appeared next was unambiguously the new build.
The first live attempt LOOKED like a total failure. The gate did not render,
the model asked in prose for a typed "CONFIRM DELETE", and the tool-call
chips showed 39ms, 32ms and 80ms for calls that should take 30 seconds
against Yahoo IMAP. Claude opened a theory that the tools had not run at all
(W55) and that the running exe was stale.
Both halves of that were wrong. The exe was the 13:36 build started at 13:42,
the backend started 13:52 after the prose-ask patch. And the log showed the
same three calls at 39.268 s, 31.994 s and 84.732 s. The chip was printing
SECONDS with an `ms` suffix. The tools had run; 85 messages had moved.
That reversal produced the window's main fix. Three data points pinned the
unit contract exactly, including a subtraction that landed on the nose: the
84.732 s call rendered as "80ms" because the SSE value EXCLUDES the 4.597 s
gate wait, and 80.135 rounds to 80.
The second live attempt was the real verification. The gate rendered, Gray
approved, `dispatch.log` recorded WAIT then APPROVED 4.6 s apart, the move
completed at reason=OK, and the messages were in Trash by eye.
The window then went after the gate prompt's scope (action 3), read three
files whole, and established that resolution is downstream of the prompt.
While reading `mailbox_tools.py` for that, it found the protected-senders
file resolved from `Path.cwd()` - and then that the file had never existed
at all.
### [ARCHIVE-W60-2026-09-15.md] 2. EVIDENCE
**Latency unit, three points, all from `dispatch.log` against the chat UI:**
| dispatch `latency=` | gate wait | expected chip | chip showed |
|---|---|---|---|
| 39.268 (find_messages) | none | 39 | 39ms |
| 31.994 (move dry_run) | none | 32 | 32ms |
| 84.732 (move apply) | 4.597 | 80.135 -> 80 | 80ms |
Post-fix, live: chips read `133.7s`, `41.1s`, and `25ms` for a genuinely
sub-second call.
**Gate fire 1 - turn `335d69e4-t1`, 2026-09-14:**
```
14:10:39.014 ATTEMPT  mailbox_move_to_trash from_addr=capitalone@notification.capitalone.com dry_run=false confirm="CONFIRM DELETE"
14:10:39.014 POLICY   site=chat-agent-live decision=WAIT     confirm_id=c208a8be...
14:10:43.611 POLICY   site=chat-agent-live decision=APPROVED confirm_id=c208a8be... reason=registry returned this outcome
14:12:03.745 OUTCOME  success=True latency=84.732 reason=OK
```
Human-confirmed: 85 messages present in Trash.
**Gate fire 2 - turn `d8f45b0b-t4`:** screenshot of the `ConfirmPrompt`
dialog, 104 s remaining on the TTL, `from_addr: "fashionnova"`, Approve and
Deny both rendered. Approved; move reported complete.
**`GATEPRED decision=NARROWED_NO_GATE`** observed at 14:07:20 on the
`dry_run: true` call. W58's argument-aware gate behaving exactly as designed.
**Mojibake, measured not guessed:** `ToolCallCard.tsx` 30 non-ASCII bytes to
0; `CommandPalette.tsx` 216 to 0, across 32 lines.
**`protected_senders.json`:** `Test-Path` False at the repo root; a recursive
search of `C:\Users\Admin` returned NOTHING. Seeded 2026-09-15 with the ten
defaults, first three bytes `91,13,10` (no BOM).
### [ARCHIVE-W60-2026-09-15.md] 3. NEGATIVE RESULTS AND DEAD THEORIES
**DEAD: "the running exe is stale."** Claude's single-cause theory for four
symptoms at once. Killed by direct measurement - exe LastWriteTime 13:36:37,
process StartTime 13:42:02, backend python StartTime 13:52:28, all AFTER
every W59 commit. Cost: one command. Worth it.
**DEAD: "the 85 messages were never moved" (W55 invocation).** Rested
entirely on the `ms` suffix. The log showed 39/32/85 SECONDS. **A wrong unit
label manufactured a defect that was not there.** This is the inverse of the
W55 failure mode and belongs beside it.
**DEAD: "the prose ask survives because `3f4a978` did not take effect."**
The backend restarted at 13:52, AFTER the 13:51 patch. The 14:07 turn that
showed the ask was running patched code; a later turn on the same code showed
no ask. The ask is MODEL-NONDETERMINISTIC. `3f4a978` lowered its probability
and did not remove the behaviour. Criterion 2 of action 1 cannot be closed by
a single clean turn.
**DEAD: "`_args_digest` lives in `serve.py`."** Claude asserted a file
location without verifying it. It is in `tools\_stubs.py`, alongside
`ToolExecutor.execute` and the prompt builder. Cost: one wasted file request.
**DEAD: "the protected-senders list is loading from the wrong directory."**
The cwd hazard is real, but the file did not exist anywhere on the drive, so
nothing was ever mis-resolved. The failure was simpler and worse: silent
fall-back to defaults, with `_pf.is_file()` returning False by design.
**NOT A DEFECT: the `ChatArea.tsx` BOM, the `App.tsx` em dash, the `api.ts`
comment mojibake.** All three confirmed non-user-visible and deliberately
left alone.
### [ARCHIVE-W60-2026-09-15.md] 4. HAZARDS FOUND
**H1 - `serve.py` MOJIBAKE, LIVE, UNPATCHED.** A multi-kilobyte mangled
string inside the `logger.info("Credentials loaded ...")` call. That line
executes on EVERY backend start and writes to `backend.log`. A second
instance sits in the channel-wiring comment. Many generations of
re-encoding, well past the two chains cleared in the frontend. NOT FIXED -
see section 9.
**H2 - PROTECTED SENDERS BIND TO LAUNCH DIRECTORY.** `_Path.cwd() /
'protected_senders.json'` in `mailbox_tools.py`. `start-openjarvis.ps1`
never sets a location; it invokes `.venv\Scripts\python.exe` directly. The
list therefore depends on where the script was launched from. Same family as
the .NET resolver trap pinned 09/14.
**H3 - AN UNREADABLE PROTECTED-SENDERS FILE IS INDISTINGUISHABLE FROM A
MISSING ONE.** The `except Exception` around the read logs and falls back to
the ten defaults. A BOM, a syntax error, or a permissions failure all
produce a silently reduced protection list. The move proceeds.
**H4 - THE GATE PROMPT NAMES A SUBSTRING, NOT A SCOPE.** Unchanged from W59,
now with live evidence. `from_addr: "fashionnova"` matches every sender
containing that string. `_args_digest` truncates at 400 chars.
**H5 - THE RUNNING EXE LOCKS THE BUILD OUTPUT.** `npm run tauri build` fails
on a file lock, not a code error, if the app is running. Stop it first.
### [ARCHIVE-W60-2026-09-15.md] 5. SDD / SDP FEED
**Confirmation gate, plain-language (09/02 requirement).** When Jarvis is
about to throw mail away for real, it stops and asks a person first. The ask
is a box on the screen with two buttons. If nobody presses a button within
two minutes, Jarvis gives up and does nothing - it does NOT take silence as
a yes. W60 watched this happen twice and checked the mailbox afterward both
times.
The important limitation, in the same plain language: the box tells you WHICH
tool wants to run and shows you the raw instructions it was given, but it
does NOT tell you HOW MANY messages will be thrown away. It cannot, yet -
Jarvis has not counted them at the moment it asks. It counts them after you
say yes. So pressing Approve means "yes, delete mail from whoever matches
this pattern", not "yes, delete these 85 messages".
**Architecture note for the SDD.** The gate is composed of four parts in
three files: the eligibility flag (`ToolSpec.requires_confirmation`), the
per-call predicate (`BaseTool.needs_confirmation(params)`, overridden with
`_confirmed`), the prompt construction and registry emit
(`ToolExecutor._execute_inner` in `tools\_stubs.py`), and the blocking wait
(`_server_confirm_callback` at `serve.py:310`). Only the third has access to
both the tool object and the resolved params - this is where any scope
improvement must live.
**Ports/protocols/encoding at each gate (08/22 requirement).** Backend HTTP
on 8010. Approve/Deny travels as `POST /v1/tools/confirm`, JSON, UTF-8. The
prompt reaches the browser over the WebSocket bridge as a
`TOOL_CONFIRM_REQUEST` event carrying `confirm_id`, `args_digest`, `prompt`
and `expires_at`. TTL 120 s enforced in `confirm_registry`.
### [ARCHIVE-W60-2026-09-15.md] 6. EXECUTION PATHS DELTA
No new paths identified. One correction to the register: the chat-agent-live
path's prompt is BUILT in `tools\_stubs.py:_execute_inner`, not in
`serve.py`. `serve.py:310` supplies only the blocking wait and the POLICY
log lines. The register's five-path count is unchanged; `cli\ask.py:356`
remains the unguarded fifth.
### [ARCHIVE-W60-2026-09-15.md] 7. DIAGNOSTIC TOOLING REGISTER DELTA
**NEW: `tools\patch_w60_chip.py`.** Byte-agnostic mojibake patcher. Anchors
on the ASCII text of a target line and replaces every non-ASCII run on that
line with a specified ASCII string, so the encoding depth of the corruption
does not matter. Writes `.bak_w60chip_<stamp>` backups, aborts and writes
NOTHING if any anchor or the latency block fails to match exactly once,
reports before/after non-ASCII byte counts per file. Output goes to stdout
only - it is a one-shot, not an instrument.
Reusable for H1. Extend `LINE_RULES` with `serve.py` anchors.
### [ARCHIVE-W60-2026-09-15.md] 8. ACTION 3 - THE THREE OPTIONS, IN FULL
The gate prompt does not name what Approve consents to. Three shapes, all
costed. None chosen; Gray picks in W61.
**OPTION A - use a count that already exists. NOT AVAILABLE.**
Ruled out on the code, not on opinion. `needs_confirmation(params)` reads
only `dry_run` and `confirm`. `find_messages` and the protected-senders
filter both run inside `execute()`, AFTER approval. A count in today's
prompt would be a number nothing computed - worse than the substring,
because it would look authoritative.
**OPTION B - resolve before prompting.**
Add a hook symmetric with W58's `needs_confirmation`, e.g.
`BaseTool.confirmation_detail(params) -> str`, called in `_execute_inner`
with both `tool` and `params` in hand. For the mailbox tools it would run
the `from_addr` lookup and the protected-senders filter, returning "85
messages from 1 sender, 3 protected senders excluded". TRUE consent to a
quantity. Cost: roughly 30 s of dead air before the dialog paints, on a
120 s TTL, and the lookup runs twice per approved move.
**OPTION C - state what the prompt already knows. CHEAP.**
No lookup, no latency. Change the prompt text to say that `from_addr` is a
SENDER SUBSTRING rather than an address, name the folder, state that
`dry_run` is false, and note that protected senders are filtered after
approval. Would have rendered "sender substring 'fashionnova' in Inbox,
apply (not a dry run)" instead of a raw JSON blob. Fixes the specific
observed defect - a substring being mistaken for an address - without
claiming a count.
C then B is the likely order given "function first, improve later", but that
is Claude's read, not Gray's ruling.
### [ARCHIVE-W60-2026-09-15.md] 9. PROCESS FAILURES THIS WINDOW
Recorded because the 08/24 rule says a window's negative knowledge is part of
its output, and these cost real budget.
**THE HANDOFF SCAFFOLD WAS NOT BUILT IN THE FIRST EXCHANGE.** The 09/10 rule
is explicit and Claude ignored it, flagged at 15 exchanges, then continued to
24 before writing anything. The BRIEF and ARCHIVE were authored from scratch
at the end - exactly the cost the rule exists to avoid.
**H1 WAS CARRIED, NOT PATCHED.** The 09/12 rule says we fix what we find in
the window. `serve.py` mojibake was found around exchange 20 with no budget
left to patch, rebuild and verify. It is action 1 in W60's list for a reason.
**AN UNVERIFIED FILE LOCATION WAS STATED AS FACT.** `_args_digest` was
claimed to be in `serve.py`. It is in `_stubs.py`. One wasted file request.
**A COUNT WAS QUOTED FROM A TRUNCATED GREP.** "21 mojibake lines" in
`CommandPalette.tsx`; the real number was 32. The patcher found them all
because it anchored on `desc:` rather than on the count, but the number
should not have been stated.
**TWO EXCHANGES WENT TO A MISREAD INSTRUCTION.** Gray asked a question about
how the action list related to a proposal; Claude treated it as a correction
and invented a menu of choices. VALIDATE, DO NOT INTERROGATE cuts both ways -
answer the question asked.
### [ARCHIVE-W61-2026-09-15.md] NEVER READ WHOLE. EXTRACT A NAMED SECTION.
Section index:
1. Window narrative
2. Evidence
3. Negative results (what it was NOT, and how established)
4. Hazards
5. SDD / SDP feed (guard mechanisms: technical detail AND plain language)
6. Register DELTAS (one line each; base registers live in ARCHIVE-W57)
7. 550B bundle carry-forward (openrouter nemotron-3-ultra-550b; bundle
   embeds its own prompt and posts itself via API)
8. SDD reference (pinned)
### [ARCHIVE-W61-2026-09-15.md] 2. Evidence
- `git add` of `tools/patch_w60_chip.py` was refused: "paths are ignored by
  one of your .gitignore files: tools". Commit 39a17a5 shows "3 files
  changed" - the patcher is NOT in the commit despite the message
  "retain chip patcher". VERIFIED: `.gitignore:18:/tools/` matches it;
  patcher exists on disk; 2 files under tools\ ARE tracked (force-added or
  tracked before the rule), so the ignore is not total.
### [ARCHIVE-W61-2026-09-15.md] 3. Negative results
- 08:47:31 restart (BIND_ASSERT backend.log line 38883, 127.0.0.1:8010):
  NO "Credentials loaded" line anywhere in current backend.log. The code
  only logs it when at least one tool has a key set (`if _cred_parts:`).
  The W60 brief claim "writes on EVERY start" is contradicted by this
  measurement. CLOSED 08:50: cred_lines=0 in all six logs
  (backend.log through backend.log.5, back to 2026-07-16). INFO sink is
  live: same-logger "[DEBUG] allowed=" landed at line 38875, 8 lines
  above BIND. So the line has NEVER fired on this box; the W60 "every
  start" claim was never true. The patch is correct but dormant; its
  verification is compile OK plus 0 non-ASCII bytes, not a runtime read.
- Gray's only credentials are his email keys, and they do not register
  in TOOL_CREDENTIALS (count stayed 0). Observation only - NOT a
  requirement, not chased.
- ACTION 2 AS WRITTEN IS STALE. Brief (carried W58->W60) said
  `cli\ask.py:356` is a "bare lambda: True, no ConfirmPolicy, silently
  approves". Measured 09-15: ZERO `lambda: True` anywhere under
  src\openjarvis. `_run_agent` in ask.py already passes
  `ConfirmPolicy(site="cli-ask", human_present=True, reason="...gap, not a
  chosen posture")` - W56 work. ConfirmPolicy defined
  `tools\_stubs.py:208`. So the site is ATTRIBUTED, not silent. What
  remains true: ConfirmPolicy never denies, so a human at the terminal is
  never asked and a destructive call still self-approves. Three windows
  carried a description the code no longer matched (W47 rule).
- NO SCRIPTED CALLER of `jarvis ask` exists (git grep, tracked +
  untracked, 09-15): no .ps1/.bat/.sh/scheduler hits. Hits are upstream
  docs, tests, CLI registration, and handoff/bundle text. So a
  deny-by-default stdin gate on cli-ask breaks nothing in Graystone use.
  Upstream `docs/user-guide/scheduler.md:194` shows `jarvis ask --agent`
  under cron; anyone following it would be DENIED (logged, not silent).
- 09:2x LIVE RUN of patch_w61_askgate.py ABORTED: marker
  openjarvis-cli-confirm-gate-v1 ALREADY PRESENT in ask.py on disk, but
  the ask.py uploaded this window has no such marker. Upload and disk
  disagree. RESOLVED: the block had run TWICE; the paste was the second
  run. Proof: backup `ask.py.bak_w61askgate_20260915_092228` and ask.py
  LastWriteTime 09:22:28 share the same second. Live harness 23/23 PASS
  on the real tree (.venv python). Class at L323, site at L522.
- LESSON (W61): a claim carried in a brief is not a measurement. W60
  wrote "on EVERY start" without reading the log; W61 spent two
  exchanges disproving it.
### [ARCHIVE-W61-2026-09-15.md] 4. Hazards
- `protected_senders.json` was committed at 39a17a5 and is on BOTH
  remotes. The W61 close untracks it; git HISTORY still holds it. It
  carries sender addresses, not credentials. Not scrubbed.
- Logging register disagreement, observed not chased: serve.py configures
  backend.log at 10 MB x 3 backups, but on disk backend.log.1-.3 are
  ~4 MiB each and backend.log.4/.5 (10 MB, July) exist beyond
  backupCount=3. Something else rotated this file at 4 MiB. W47 rule:
  the disagreement is the finding - for the logging topology register.
- A `.bak_*` made by shutil.copy2 shows the SOURCE file's old mtime
  (ask.py backup reads 09/13 08:52 - the W56 edit), not when the backup
  was made. The timestamp in the backup NAME is the creation time.
- `_execute_inner`: callback returns False and registry has no decision
  -> classified TIMEOUT, model told "user did not deny it, ask again".
  Any gate that denies locally without writing the registry manufactures
  a false TIMEOUT. Binding on the W61 CLI gate.
- A three-glyph garble (Gamma, C-cedilla, o-umlaut) in PowerShell console output of git grep is the CONSOLE rendering
  a valid UTF-8 em dash as cp437. Not file mojibake. ask.py line 1 holds a
  correct UTF-8 em dash. Do not "fix".
- serve.py mojibake at two sites (channel-wiring comment; LIVE
  `logger.info("Credentials loaded ...")`). Patcher `tools\patch_w61_serve.py`
  replaces the whole span between ASCII anchors; tested offline on a
  7-deep cp1252 chain (1908 -> 0 non-ASCII bytes, rerun aborts clean,
  `_bak\serve.py` skipped).
- LIVE RUN 08:41:21: `src\openjarvis\cli\serve.py` 255973 -> 27458 bytes;
  228518 -> 0 non-ASCII. Site A line 381 was 53005 chars, site B line 588
  was 49790 chars. The file was ~89 percent mojibake by bytes. Compiles.
  Backup `serve.py.bak_w61serve_20260915_084121`. [runtime check pending]
- The force-add commit block was NOT run: HEAD still 39a17a5, tools\ still
  2 tracked files. Folded into the serve.py commit.
- A commit message can claim content the commit does not hold. `git add`
  on an ignored path prints a hint and continues; the commit still succeeds.
### [ARCHIVE-W61-2026-09-15.md] 5. SDD / SDP feed
- CLI GATE DESIGN (W61, Action 2). Technical: replace
  `ConfirmPolicy(site="cli-ask")` in `ask.py::_run_agent` with a terminal
  gate. Reads one line from stdin; only "y"/"yes" approves; empty, EOF,
  anything else denies; stdin not a TTY denies without asking. Every
  branch writes `POLICY site=cli-ask decision=...` to dispatch.log. The
  gate must WRITE its decision into confirm_registry, because
  `ToolExecutor._execute_inner` treats an unresolved False as TIMEOUT and
  tells the model "the user did not deny it. Ask the user again" - a
  CLI denial left unrecorded would be reported as a timeout and invite a
  re-request loop.
- CLI GATE, PLAIN LANGUAGE: when Jarvis, running in the terminal, wants
  to do something that can't be undone (like moving mail to the trash),
  it stops and asks the person at the keyboard "Allow this? y/N". Only a
  clear "y" lets it go ahead. If nobody answers, or the answer is
  anything else, or there is no keyboard at all (a script is running it),
  the answer is NO. Whatever happens, it writes a note in the log saying
  what was asked and what the answer was, so later we can tell a real
  "yes" from a machine pretending.
- MAILBOX SERVICE - ARCHITECTURE (SDP, architecture-focused; every
  action and channel that touches the service). Items marked NOT READ
  were not measured in W61 and must not be treated as fact.
  ENTRY CHANNELS
  * Chat UI (Tauri exe, React) -> backend FastAPI, HTTP on
    127.0.0.1:8010, loopback only (BIND_ASSERT in backend.log). Chat
    stream is SSE (latency field in SECONDS). Confirm prompt reaches
    the UI as a WS frame (ConfirmPrompt, W57); the answer returns as
    JSON POST /v1/tools/confirm - the route normalizes approve/deny to
    approved/denied. Payloads JSON, UTF-8.
  * CLI `jarvis ask -a <agent>` -> in-process agent; confirmation over
    the terminal: prompt on stderr (encoded to the console code page with
    replacement), answer on stdin, TTY only. `TerminalConfirmGate`.
  * Managed-agent / scheduler / SDK paths: see the W57 execution-path
    register. Four ConfirmPolicy auto-approve sites in
    agent_manager_routes (attributed, never deny). sdk.py path
    unregistered (NOT READ).
  TOOL LAYER (`src\openjarvis\tools\mailbox_tools.py`, 5 tools, results
  are JSON strings)
  * Read: mailbox_list_accounts; mailbox_usage_report (cap mail.read,
    600 s); mailbox_find_messages (mail.read, 600 s, summary default,
    counts windowed to the newest ~10,000 per folder on the server).
  * Write: mailbox_move_to_trash (mail.write, 1800 s) and
    mailbox_empty_folder (mail.write, 600 s). Both: dry_run defaults
    TRUE; apply needs dry_run=false AND confirm="CONFIRM DELETE"
    (model-side interlock); spec requires_confirmation=True AND
    needs_confirmation(params)=_confirmed(params) (human gate fires on
    apply only).
  GATE (`tools\_stubs.py` ToolExecutor._execute_inner)
  * Order: unknown tool -> JSON args -> boundary guard (non-local tools)
    -> RBAC capability -> taint -> GATEPRED -> confirm gate -> execute in
    a 1-worker thread pool with the spec timeout.
  * Confirm gate: `core\confirm_registry.py`, in-process, threading.Event,
    TTL 120 s (env OPENJARVIS_CONFIRM_TTL), decisions approved / denied /
    timeout, WRITE-ONCE. Bus events TOOL_CONFIRM_REQUEST and
    TOOL_CONFIRM_RESOLVED. A False callback with no recorded decision is
    reported to the model as TIMEOUT.
  GUARD - PROTECTED SENDERS (v2, W61)
  * File `DEFAULT_CONFIG_DIR\protected_senders.json` =
    `C:\Users\Admin\.openjarvis\protected_senders.json`. JSON array of
    strings, UTF-8; a BOM is tolerated and logged. Lowercased substring
    match against each message's from_addr. The file REPLACES the 10
    built-in defaults; any unusable file falls back to the defaults,
    never to an empty list. Applied ONLY on the from_addr selection
    path - a direct uids call is NOT checked (open gap).
  SECRETS - PINNED BY GRAY 09/15
  * mailbox_tools.py already keeps connector credentials in the same
    per-user dir: `C:\Users\Admin\.openjarvis\connectors\
    imap_mail_<account>.json` = {"email","password","provider"}, read
    by `load_tokens()`; `connector_for()` also reads an optional "host".
    Written by `setup_mailbox_account.py`. Module docstring says nothing
    logs or returns a password (claim NOT independently verified W61).
    Option B puts the guard list beside them so no account data lives in
    the repo.
  UPSTREAM
  * `ImapMailConnector(provider, account_id, credentials_path,
    imap_host)` -> the mail provider (Yahoo) over IMAP. PORT, TLS MODE
    AND AUTH MECHANISM: NOT READ (imap_mail.py) - required before this
    section is complete.
  VISIBILITY
  * backend.log - root logger, `%LOCALAPPDATA%\OpenJarvis\logs`, UTF-8,
    SanitizingFormatter; PROTECTED lines and the blocked-sender report.
  * dispatch.log - logger openjarvis.dispatch, same dir, 2 MB x 4, UTF-8,
    no propagation; ATTEMPT / OUTCOME / GATEPRED / POLICY / PROTECTED
    lines, each with turn id.
- MAILBOX GUARD, PLAIN LANGUAGE: Jarvis keeps a short list of senders
  whose mail it must never throw away, like your own address and your
  order receipts. The list is a small file kept in your private settings
  folder, next to the file that holds your email password, and not in
  the project code. Before Jarvis moves mail from a sender to the trash,
  it checks each message against that list and leaves the protected ones
  alone. If the list is missing or broken, Jarvis uses a built-in backup
  list instead and writes a note saying so - it never ends up with no
  list at all. One hole is still open: if Jarvis is handed exact message
  numbers instead of a sender name, it does not check the list yet.
### [ARCHIVE-W61-2026-09-15.md] 6. Register DELTAS
- Diagnostic tooling: `tools\` is gitignored by `.gitignore:18 /tools/`.
  Only force-added files are versioned (2 before W61). Every new instrument
  in tools\ needs `git add -f` or it silently stays local.
- Logging topology: [TBD]
- Execution paths: UNVERIFIED - `sdk.py:469/525/573` imports
  `_build_tools` and `_get_memory_backend` from cli.ask but NOT
  `_run_agent`. If the SDK constructs its own agent, its confirm_callback
  wiring is unregistered. Not read; not chased.
- Diagnostic tooling: `test_confirm_policy_cli.py` at repo root (W56) is
  SUPERSEDED by `tools\test_confirm_gate_cli_w61.py` - its checks 2-4
  assert the removed ConfirmPolicy and now fail by design. The W61
  harness (23 checks) redirects LOCALAPPDATA to a temp dir before import,
  so its POLICY lines never touch the real dispatch.log, and reads the
  temp log back. Non-interactive: scripted fake stdin/stderr.
- Diagnostic tooling: `tools\patch_w61_askgate.py` - ask.py gate patcher.
  Offline: 23/23 PASS on a stand-in tree; 3/7 on the unpatched file
  (negative control); CRLF preserved; rerun aborts.
- Program goal: [TBD]
- Diagnostic tooling: `tools\patch_w61_protected.py` (v2 loader + one-time
  copy) and `tools\test_protected_senders_w61.py` (19 checks, temp
  dispatch.log, fake connector, reads the real list only). Supersedes
  scenario E of `tests\probe_h3_protected_v1.py` (assumes CWD - NOT READ,
  not edited).
- Rules of engagement: a claim carried in a brief is not a measurement
  (W61). New instruments in tools\ need `git add -f` (W61).
- ACTION 3 STARTED 09-15: one mailbox_tools.py (src\openjarvis\tools);
  L617 `_Path.cwd() / 'protected_senders.json'`; L623
  `logger.exception('...unreadable; using built-in list')` - so the
  "unreadable is silent" claim in the W60 brief may also be stale; the
  MISSING-file case is the one with no log. `register_mailbox_tools.py`
  at repo root not yet checked (grep was scoped to src).
- ACTION 3 MEASURED (whole-repo grep + mailbox_tools.py read whole):
  * ONLY reader is mailbox_tools.py `MailboxMoveToTrashTool.execute`.
    Other hits: `patch_protected_senders.py` (root, the original
    inserter - history) and `tests/probe_h3_protected_v1.py` scenario E,
    which drops the file in CWD and WILL GO STALE when the path moves.
  * W60 CLAIM "unreadable file is silently swallowed" IS WRONG: L623
    `logger.exception` writes ERROR + traceback to backend.log.
  * The SILENT cases are: file missing; valid JSON that is not a list;
    an empty list. All three fall back to the 10 defaults with no log.
  * FAIL-OPEN FOUND: a list whose entries are all blank (e.g. [" "])
    passes the `isinstance(list) and _ld` test, filters to [], and
    replaces the defaults with NOTHING - every sender becomes movable,
    silently.
  * GAP FOUND: the protected filter lives inside `if _from_addr:`. A
    call that passes `uids` directly is never checked against the list.
    Not patched with the path fix - needs imap_mail.py to map uid ->
    sender. Queued behind this patch's verification.
- ACTION 3 CLOSED 09:49 (Option B, Gray-approved windows ago so keys are
  not exposed): `patch_w61_protected.py` applied to mailbox_tools.py
  (CRLF preserved, 880 -> 961 lines, 17-line v1 block replaced, 10
  defaults lifted verbatim, 0 `.cwd()` left, compiles). One-time copy:
  repo-root list -> `C:\Users\Admin\.openjarvis\protected_senders.json`,
  10 entries, first bytes `[` CR LF (no BOM). Harness
  `tools\test_protected_senders_w61.py` 19/19 PASS LIVE, incl. check 15
  (real file loads source=file) and check 17 (all-blank list now falls
  back to defaults; cdgray33@yahoo.com held back). Backend RESTART
  required - the running process still had v1 loaded at close.
  Backup `mailbox_tools.py.bak_w61protected_20260915_094907`.
- OFFLINE NEGATIVE RESULT: the first offline run showed "not a usable
  list" for a BOM fixture. Cause was the TEST: /bin/sh printf wrote the
  literal text \xef\xbb\xbf. Fixed the fixture; code unchanged.
### [ARCHIVE-W61-2026-09-15.md] 8. SDD reference
- PINNED 09/15 (Gray): the SDP is ARCHITECTURE-FOCUSED and details every
  action and channel that interacts with a service. The program is being
  worked as a LIST OF ACTIVITIES, each of which REPAIRS a service or
  DEPLOYS a new one - and that list includes the visibility tooling
  being installed everywhere. Organize SDP entries per service, per
  activity. Mailbox service entry: section 5.
- PINNED: Gray's SDD covers all OpenJarvis work. Every window feeds it;
  this archive's sections 3-6 are W61's input. Section 5 holds the
  CLI-gate design in technical and plain-language form (09/02 rule).
### [ARCHIVE-W62-2026-09-15.md] INDEX
  s1  CARRIED BRIEF-W61 (W62 scaffold, exchange 1)
  s2  READ THIS FILE ONLY. DO NOT READ AN ARCHIVE UNLESS A SECTION IS NAMED BELOW.
  s3  STATE AT CLOSE
  s4  NEXT ACTIONS, IN ORDER
  s5  HARD FACTS A NEW WINDOW WILL GET WRONG
  s6  ROLLBACK POINTS (W56-W60 points remain valid)
  s7  RULES OF ENGAGEMENT
  s8  W62 FINDINGS (added 2026-09-15; W62 ORDER below supersedes NEXT ACTIONS above)
  s9  W62 ORDER (proposed)
  s10  W62 FINDINGS, EXCHANGE 3-4 (output from ALREADY-RUNNING v1 backend)
  s11  W62 ORDER (exchange 4)
  s12  W62 MEASUREMENTS, EXCHANGE 5
  s13  W62 MEASUREMENTS, EXCHANGE 6
  s14  W62 MEASUREMENTS, EXCHANGE 7
  s15  W62 MEASUREMENTS, EXCHANGE 8
  s16  W62 MEASUREMENTS, EXCHANGE 9
  s17  W62 FINDINGS, EXCHANGE 11 (ttsPlayer.ts read whole; audio endpoints probed)
  s18  W62 MEASUREMENTS, EXCHANGE 10 (applied at ex12; the ex10 block never ran)
  s19  W62 MEASUREMENTS, EXCHANGE 12
  s20  W62 EXCHANGE 13-14 (ex13 block stopped; ex14 handoff)
  s21  W62 NEGATIVE RESULTS (what it was NOT, and how that was established)
  s22  W62 SDD/SDP FEED
  s23  W62 EXECUTION PATHS DELTA
  s24  W62 TOOLING REGISTER DELTA (all in tools\, all need git add -f)
  s25  W62 LOGGING TOPOLOGY DELTA
  s26  W62 550B CARRY
  s27  W62 PROGRAM GOAL
  s28  W62 HANDOFF MEASUREMENT
### [ARCHIVE-W62-2026-09-15.md] READ THIS FILE ONLY. DO NOT READ AN ARCHIVE UNLESS A SECTION IS NAMED BELOW.
Registers: ARCHIVE-W57 (root). W61 material + register DELTAS: ARCHIVE-W61
s6; SDD/SDP feed incl. plain-language CLI gate: s5. Never open whole.
### [ARCHIVE-W62-2026-09-15.md] STATE AT CLOSE
- **W61 CLOSE COMMIT CARRIES ACTION 3 + THIS HANDOFF** (`git log -1`).
- **ACTION 1 CLOSED (`fb67e95`).** serve.py mojibake gone. Its credentials
  log line is DORMANT (never fired since 07-16); verified by compile only.
- **ACTION 2 CLOSED (`e1b21b5`).** "Bare lambda" claim was STALE. ask.py now
  has `TerminalConfirmGate`: y/N, deny default, non-TTY denies, decision
  written to the registry. Harness 23/23 LIVE.
- **ACTION 3 CLOSED (Option B).** Protected list now at
  `C:\Users\Admin\.openjarvis\protected_senders.json`, beside the IMAP
  credentials (PINNED - SDP s5). Every fallback logged; never empty (v1
  failed OPEN on blank lists). Harness 19/19 LIVE. Root copy untracked.
  **BACKEND RESTART PENDING** - it still ran v1 at close.
### [ARCHIVE-W62-2026-09-15.md] NEXT ACTIONS, IN ORDER
1. **RESTART** via `.\start-openjarvis.ps1`; on the first real move, confirm
   `PROTECTED source=file` in dispatch.log (it logs only on a move call).
2. **UIDS PATH SKIPS THE PROTECTED LIST.** Needs `imap_mail.py` whole
   (uid -> sender; also gives IMAP port/TLS/auth the SDP is missing).
3. **GATE PROMPT SCOPE.** Three options documented in W60.
4. **`sdk.py` path** - imports `_build_tools` from cli.ask but not
   `_run_agent`; its confirm wiring is unregistered. Read before ruling.
5. **UNTRACKED FLOOD - OWN WINDOW.** 6. **Requirements measurement.**
### [ARCHIVE-W62-2026-09-15.md] HARD FACTS A NEW WINDOW WILL GET WRONG
- **`tools\` IS GITIGNORED (`.gitignore:18 /tools/`).** A plain `git add`
  prints a hint and the commit still succeeds WITHOUT the file. Use `-f`.
- **THE CLI GATE MUST WRITE THE REGISTRY.** `_execute_inner` turns a False
  with no recorded decision into TIMEOUT and tells the model "the user did
  not deny it, ask again". Any local deny must `_cr.resolve(cid, DENIED)`.
- **`test_confirm_policy_cli.py` (root, W56) IS SUPERSEDED** - its checks
  2-4 fail by design. Use `tools\test_confirm_gate_cli_w61.py` with
  `.venv\Scripts\python.exe`, run from the repo root.
- **A `copy2` BACKUP SHOWS THE SOURCE'S OLD MTIME.** The name stamp is the
  creation time. A patcher that says "already present" may be a 2nd run.
- **PROSE ASK IS MODEL-NONDETERMINISTIC.** **GATE PROMPT IS BUILT IN
  `_stubs.py`**; resolution is downstream; `from_addr` is a substring.
- **THE REPO-ROOT `protected_senders.json` IS NO LONGER READ.** Edit the one
  in `C:\Users\Admin\.openjarvis\`. Write it ASCII (a BOM is logged).
- **`ConfirmPolicy` NEVER DENIES.** `_server_confirm_callback` and
  `TerminalConfirmGate` ARE gates. Registry takes `approved`/`denied`.
- **`dry_run` DEFAULTS TRUE** (NARROWED_NO_GATE is correct). **BUILD EXITS
  1 ON SUCCESS; THE RUNNING EXE LOCKS THE OUTPUT.**
- **BACKEND PORT 8010.** Logs `%LOCALAPPDATA%\OpenJarvis\logs\`. Handoffs
  in repo root, else Downloads. Start ONLY via `.\start-openjarvis.ps1`.
- **A 3-GLYPH GARBLE IN CONSOLE GIT OUTPUT IS DISPLAY, NOT FILE MOJIBAKE.**
### [ARCHIVE-W62-2026-09-15.md] ROLLBACK POINTS (W56-W60 points remain valid)
```powershell
git revert HEAD      # W61 close: protected v2 (+ handoff); list copy stays
git revert e1b21b5   # CLI terminal gate
git revert fb67e95   # serve.py mojibake
Copy-Item 'C:\Users\Admin\OpenJarvis\src\openjarvis\cli\ask.py.bak_w61askgate_20260915_092228' 'C:\Users\Admin\OpenJarvis\src\openjarvis\cli\ask.py' -Force
Copy-Item 'C:\Users\Admin\OpenJarvis\src\openjarvis\cli\serve.py.bak_w61serve_20260915_084121' 'C:\Users\Admin\OpenJarvis\src\openjarvis\cli\serve.py' -Force
```
### [ARCHIVE-W62-2026-09-15.md] RULES OF ENGAGEMENT
Full text is ARCHIVE-W57 section 6. Standing: **GRAY UPLOADS WHOLE FILES,
REGARDLESS OF SIZE; CLAUDE DOES NOT ISSUE READS.** ONE RUNNABLE BLOCK PER
MESSAGE. **PRODUCE THE ARTIFACT BEFORE ISSUING THE COMMAND THAT RUNS IT.**
**DELIVER WITH A NEWEST-FILE SELECTOR THAT PRINTS ITS CHOICE.** A DRY RUN
THAT PRINTS NO COUNTS IS NOT A DRY RUN. VALIDATE, DO NOT INTERROGATE. WE FIX
WHAT WE FIND IN THIS WINDOW. REISSUE WHOLE, DO NOT PATCH THE PATCHER. DO NOT
RULE FROM AN ARCHIVE SECTION. PRODUCTION BUILD ONLY - NEVER `tauri dev`.
**BUILD THE HANDOFF SCAFFOLD IN THE FIRST EXCHANGE, NOT THE LAST.**
Working directory `PS C:\Users\Admin\OpenJarvis>`; state shell and host
BEFORE he runs anything; Ubuntu ollama host is 172.16.33.200. No non-ASCII.
ALWAYS VERIFY. FINISH THE THING BEFORE STARTING THE NEXT. Tests
NON-INTERACTIVE. Author's resources FIRST. Push to BOTH remotes unasked.
Flag at 15 exchanges, never cut a live trace. TOKEN CONSERVATION MODE. DO NOT
RE-DERIVE PRIOR-WINDOW WORK WITHOUT ASKING. **.NET STATIC METHODS RESOLVE
RELATIVE PATHS AGAINST `C:\WINDOWS\system32` - ALWAYS PASS ABSOLUTE.**
**PINNED: SDP IS ARCHITECTURE-FOCUSED - EVERY ACTION AND CHANNEL PER
SERVICE; WORK IS A LIST OF REPAIR/DEPLOY ACTIVITIES INCL. VISIBILITY
TOOLING** (W61, ARCHIVE s8). **A CLAIM IN A BRIEF IS NOT A MEASUREMENT.** **NEW
INSTRUMENTS IN `tools\` NEED `git add -f`** (W61).
**A REGISTER THAT DISAGREES WITH THE CODE IS THE FINDING** (W47). **CONSENT
IS ONLY CONSENT IF THE THING CONSENTED TO IS THE THING THAT EXECUTES** (W53).
**A STRING IN THE TRANSCRIPT IS NOT EVIDENCE A TOOL RAN** (W55). **AN
AUTO-APPROVE THAT LEAVES NO TRACE IS INDISTINGUISHABLE FROM CONSENT** (W56).
**AN INTERLOCK THE MODEL SATISFIES IS NOT A HUMAN GATE** (W57). **THE
PREDICATE YOU NEED IS OFTEN ALREADY WRITTEN SOMEWHERE THAT ISN'T THE GATE**
(W58). **AN EMPTY CHAIR LOOKS EXACTLY LIKE A BROKEN GATE IN THE LOG** (W59).
**A UNIT LABEL IS PART OF THE EVIDENCE; A WRONG ONE MANUFACTURES A DEFECT
THAT ISN'T THERE** (W60). **A SAFETY LIST THAT WAS NEVER CREATED FAILS
EXACTLY LIKE ONE THAT LOADS** (W60).
**Program goal:** a functional executive assistant doing the duties at a
computer a human would. W61 closed the LAST unasked-consent path known on
a human-attended entry: the terminal now asks before a destructive tool
runs, and a refusal is reported as a refusal. Requirements measurement
is still unbuilt.
### [ARCHIVE-W62-2026-09-15.md] W62 FINDINGS (added 2026-09-15; W62 ORDER below supersedes NEXT ACTIONS above)
- **F-W62-1 APPROVAL UX REGRESSION.** "Move 20 senders to trash" raises 20
  pop-ups, each with its own 120 s timeout. Before the gate work, ONE approval
  covered the interaction. Wanted: one approval per user request. Constraint
  (W53/W57/W56): that approval shows the exact manifest (senders, count),
  covers ONLY those calls, anything off-manifest still asks, every pass is
  logged. Likely same item as old action 3 (W60 options) - ASK before reading.
- **F-W62-2 TTS SILENT.** Reply text prints, no voice. NOT MEASURED. Suspects
  only: pending restart, 6c gate/WS emit work, tts-service on ollama-mcp2.
- **F-W62-3 USAGE COST.** An ask sent to the long W61 window after the 5-hour
  reset billed ~30 percent of the fresh session before cancel. RULE: after a
  reset NEVER continue the old window; open new with the BRIEF only.
- **W61 LAST OUTPUT** never arrived; W62 could not see it. Treat BRIEF-W61 as
  complete unless Gray pastes the missing tail.
### [ARCHIVE-W62-2026-09-15.md] W62 ORDER (proposed)
1. RESTART + confirm `PROTECTED source=file` (unchanged).
2. F-W62-2 TTS silent - measure AFTER restart.
3. F-W62-1 approval batching (absorbs old 3).
4. Old 2 (uids path), 4 (sdk.py), 5 (untracked flood), 6 (requirements).
### [ARCHIVE-W62-2026-09-15.md] W62 MEASUREMENTS, EXCHANGE 5
- HKCU\Console QuickEdit=1. Backend console owner pid=21032 is classic conhost (not OpenConsole), window open since 09/12.
- Backend pid=18592 started 09/15/2026 13:04:21. Live console mode: pid=21032 getmode=True mode=0x1E7 QUICKEDIT_LIVE=True EXTENDED=True
- HEAD files changed after backend start: 0 (0 = running backend loaded W61 v2 code; restart may be moot).
- TOOLING REGISTER DELTA: tools\probe_console_mode_w62.ps1 - hidden child attaches read-only to a console pid, reads CONIN mode; output tools\probe_console_mode_w62.out.txt (verified readable at build). Needs git add -f.
### [ARCHIVE-W62-2026-09-15.md] W62 MEASUREMENTS, EXCHANGE 8
- 726 s gap re-measured with a shared read: 72 lines inside (of 40990 read). First in gap: 2026-09-15 13:16:37,541 WARNING openjarvis.server.speech_router: TTS START: 6 chars, voice=am_adam
- LOGGING TOPOLOGY DELTA: backend.log is held open by the live backend. [IO.File]::ReadLines/ReadAllLines FAIL on it; Select-String and FileStream with FileShare 'ReadWrite, Delete' succeed. Use the latter in instruments.
- HARD FACT: a failed .NET read left a counter at its initial 0 and the block reported it as a result. Start counters at -1; gate every write on the read succeeding.
- COMMIT attempted ex8: start-openjarvis.ps1 W62-QUICKEDIT + 3 tools\ instruments + this BRIEF; push origin (GitHub) + gitlab (lab). Verify with git log -1.
### [ARCHIVE-W62-2026-09-15.md] W62 MEASUREMENTS, EXCHANGE 9
- Gap by logger: openjarvis.server.speech_router=1; uvicorn.access=71
- Gap by minute: 13:16=1 13:28=71
- Non-access lines in gap: 1
- VERDICT: CONFIRMED: only TTS START is console-bound in gap; SUPERSEDED ex10: server served NOTHING for 12 min (event loop blocked on the console write), then released a 71-request backlog. 726 s = paused log write, not synthesis. Covered by cd2d1db.
- LOGGING TOPOLOGY DELTA: console shows openjarvis WARNING+ only; uvicorn.access INFO is file-only. A paused console blocks only threads writing to the console, and if the blocked write is on the asyncio event loop the WHOLE server stops; the file shows silence then a burst (ex10).
### [ARCHIVE-W62-2026-09-15.md] W62 MEASUREMENTS, EXCHANGE 10 (applied at ex12; the ex10 block never ran)
- Gap by minute: 13:16=1 (TTS START) 13:28=71 (uvicorn.access); 13:17-13:27 = 0.
- F-W62-2a CLOSED (cause): a QuickEdit-paused console write on the event loop froze the WHOLE server for 726 s. Any gate approval then would have hung. Fix cd2d1db. OPEN: see the green "QuickEdit off" line at the next normal restart.
- HAZARD (SDP, no patch this window): console-bound log writes on the asyncio loop can stall the server. Candidate: queue-based log handler.
- LESSON: a verdict string must not assert what the same block has not measured.
### [ARCHIVE-W62-2026-09-15.md] W62 EXCHANGE 13-14 (ex13 block stopped; ex14 handoff)
- Frontend files (git ls-files): frontend/src/audio/ttsPlayer.ts, frontend/src/components/Chat/ChatArea.tsx, frontend/src/components/Desktop/lib/api.ts, frontend/src/hooks/useSpeech.ts, frontend/src/hooks/useSpeechStream.ts, frontend/src/lib/api.ts.
- TWO api.ts files. ttsPlayer imports '../lib/api' = frontend/src/lib/api.ts. Which copy Gray uploaded in ex13 is not established; its 2 garbled dashes match lib/api.ts (garbled-seq=2, proper em dash=0).
- ex13 stopped at "PORT 9222 ALREADY IN USE" BEFORE closing the app. App not relaunched; nothing to undo. probe_webview_cdp_w62.ps1 written, parse errors 0, NEVER RUN.
- ex13 static findings (api.ts whole): F-W62-2d confirmed (synthesizeSpeech has no timeout). Legacy synthesizeSpeechChunks/splitIntoTTSChunks still exported (second TTS path; ChatArea use unread). Recording code not in api.ts. Noted only: bind/unbindAgentChannel use bare fetch (no auth header); submitSavings posts to external Supabase.
- ex12 ruling (positive-controlled): OpenJarvis WebView2 host pid 30200 had audio-service pid 26788 but NO audio session on any endpoint; control pid 28460 was seen state=1. F-W62-2b is FRONTEND.
### [ARCHIVE-W62-2026-09-15.md] W62 NEGATIVE RESULTS (what it was NOT, and how that was established)
- NOT slow synthesis: TTS DONE came 10 ms after TTFB (726.030 -> 726.040 s).
- NOT a TTS-only stall: per-minute count 13:17-13:27 = 0 lines; 71 requests served at 13:28.
- NOT "server kept serving" (ex9 verdict text); the per-minute data in the same output contradicted it.
- NOT "0 lines in gap" as ex7 printed: ReadLines failed on the locked log and the counter kept its initial 0. Shared read found 72.
- NOT a pending restart: backend started 13:04:21, after every W61 HEAD file (latest 09:53).
- NOT device, mute, routing or consent: all endpoints unmuted, mic consent Allow at HKCU/HKLM/desktop apps, probe proven sighted by a silent-WAV control.
- NOT a blind probe: the control session was seen.
### [ARCHIVE-W62-2026-09-15.md] W62 SDD/SDP FEED
- Backend host chain: explorer -> powershell pid 21032 (classic conhost, open since 09/12) -> python 5668 -> python 18592 listening 127.0.0.1:8010 (HTTP). Console input mode was 0x1E7 (QuickEdit on), now 0x1A7.
- Logging channels: openjarvis loggers WARNING+ -> console AND backend.log; uvicorn.access INFO -> backend.log only. A console write made on the asyncio event loop is a single stall point for every HTTP route: TTS, UI polls, POST /v1/tools/confirm.
- Plain language (the guard): the server writes a note on its screen before some jobs. If you click in that window, Windows holds the pen still until you let go. The server waits for the pen, and while it waits it cannot answer anyone - not the voice, not the approve button - so an approval can run out its 120 seconds with nobody able to press it. We told Windows not to hold the pen when you click.
- Speech output channel: WebView2 -> POST /v1/speech/synthesize (HTTP, loopback 8010, JSON in: text, voice_id am_adam, speed 0.85, output_format wav; WAV out) -> ttsPlayer decodeAudioData -> one AudioContext + silent keepalive -> Windows default render endpoint via a WASAPI shared session owned by the WebView2 audio-service process. That session never appeared.
- Speech input channel: WebView2 microphone capture (files useSpeech.ts / useSpeechStream.ts, unread) -> POST /v1/speech/transcribe (HTTP multipart, recording.webm) -> faster-whisper. Since 08/17 Windows records capture opening and closing in the same second.
- Hazards: event-loop console stall (candidate hardening: queue-based log handler); no synthesize timeout; stranded pump after stopAll; two api.ts; unidentified 9222 listener; a WebView2 debug port lets local processes drive approvals.
- Repair/deploy activity list W62: A1 QuickEdit off live + start script DONE (cd2d1db). A2 console, audio and CDP instruments BUILT (8728267 + close). A3 playback fix PENDING. A4 mic fix PENDING. A5 synth timeout + pump restart PENDING. A6 api.ts mojibake PENDING. A7 stop-query PENDING. A8 approval batching PENDING.
### [ARCHIVE-W62-2026-09-15.md] W62 EXECUTION PATHS DELTA
- NEW PATH "speech synthesize": entry POST /v1/speech/synthesize (server/speech_router.py). Not a tool path: no ToolExecutor, no confirmation gate (non-destructive). Human present. Event bus traffic not measured. Shares the event-loop console-stall hazard with every route.
- NEW PATH "speech transcribe": entry POST /v1/speech/transcribe. Same properties; frontend caller unread.
- GATE NOTE: /v1/tools/confirm is served on the same event loop, so a console stall can expire an approval with the human present.
### [ARCHIVE-W62-2026-09-15.md] W62 TOOLING REGISTER DELTA (all in tools\, all need git add -f)
- probe_console_mode_w62.ps1: hidden, attaches read-only to a console pid, reads CONIN mode. Out probe_console_mode_w62.out.txt. VERIFIED.
- set_console_quickedit_w62.ps1 -Action read|off|on -TargetPid N. Out set_console_quickedit_w62.out.txt. VERIFIED.
- test_quickedit_snippet_w62.ps1: runs the start-script snippet in a fresh hidden console. Out test_quickedit_snippet_w62.out.txt. VERIFIED (PASS=True).
- probe_audio_w62.ps1: default endpoints, endpoint vol/mute, every session with pid chain/state/vol/mute, mic consent and app last-use. Out probe_audio_w62.out.txt. VERIFIED and positive-controlled.
- audio_control_w62.ps1: hidden silent WAV, 20 s. Positive control for the audio probe.
- probe_webview_cdp_w62.ps1 -Out F [-Port 9222]: replays WebView2 console+Log history (tts/audio/mic filter), evaluates page audio/mic state. OUTPUT PATH NOT VERIFIED - never run.
- Already in code: ttsPlayer [PUMPDBG] and [tts] lines -> WebView2 console; unreadable in production without CDP.
### [ARCHIVE-W62-2026-09-15.md] W62 LOGGING TOPOLOGY DELTA
- backend.log is held open by the live backend: [IO.File]::ReadLines/ReadAllLines FAIL; Select-String and FileStream with FileShare 'ReadWrite, Delete' succeed.
- Console receives openjarvis WARNING+; uvicorn.access INFO is file-only. A paused console blocks only threads writing to it; on the event loop that is the whole server, and the file shows silence then a burst.
- Frontend console (WebView2) is a separate sink with no file; reachable only via CDP.
### [ARCHIVE-W62-2026-09-15.md] W62 HANDOFF MEASUREMENT
- Port 9222 listener at handoff: addr=127.0.0.1 pid=28496 name=msedgewebview2.exe started=09/15/2026 00:36:27 parent=openjarvis-desktop.exe/30200 cmd="C:\Program Files (x86)\Microsoft\EdgeWebView\Application\152.0.4191.66\msedgewebview2.exe" --embedded-browser-webview=1 --webview-exe-name=openjarvis-desktop.exe --webview-exe-version=0.1.0 --user-data-dir="C:\Users\Adm...
### [ARCHIVE-W63-2026-09-17.md] READ THIS FILE ONLY. DO NOT READ AN ARCHIVE UNLESS A SECTION IS NAMED BELOW.
Registers: ARCHIVE-W57 (root) + ARCHIVE-W61 s6 deltas + ARCHIVE-W62 deltas
(root; INDEX and extract command at top). Never open whole.
### [ARCHIVE-W63-2026-09-17.md] NEXT ACTIONS, IN ORDER
1. **RULE ON THE 9222 LISTENER** above. A WebView2 debug port lets any local
   process drive the page, approvals included.
2. **PLAYBACK + MIC.** Gray uploads WHOLE at window open: `ChatArea.tsx`,
   `hooks\useSpeech.ts`, `hooks\useSpeechStream.ts`,
   `components\Desktop\lib\api.ts`. Then run the CDP probe on a free port.
3. **F-W62-2c STRANDED PUMP** (stopAll mid-fetch leaves `pumping` true; the
   next turn never plays) and **F-W62-2d NO SYNTH TIMEOUT**
   (`lib\api.ts synthesizeSpeech`). Patch together with item 2.
4. **api.ts MOJIBAKE:** 2 garbled dash sequences in `frontend\src\lib\api.ts`
   comments.
5. **F-W62-5 STOP-QUERY** control, believed unwired. Unmeasured.
6. **F-W62-1 APPROVAL BATCHING** (absorbs old gate scope; W60 options - ASK
   before reading W60). One approval per request, showing the exact manifest;
   off-manifest still asks; every pass logged.
7. Old: uids path skips protected list (`imap_mail.py` whole); `sdk.py`
   confirm wiring; untracked flood (OWN WINDOW); requirements measurement.
### [ARCHIVE-W63-2026-09-17.md] HARD FACTS A NEW WINDOW WILL GET WRONG
- **TWO api.ts FILES:** `frontend\src\lib\api.ts` (ttsPlayer imports this)
  and `frontend\src\components\Desktop\lib\api.ts`. Duplicate-code hazard.
- **`backend.log` IS HELD OPEN.** `[IO.File]::ReadLines` FAILS on it. Use
  `Select-String` or a FileStream with FileShare 'ReadWrite, Delete'. Start
  counters at -1 so a failed read cannot print a result.
- **A VERDICT STRING MUST NOT ASSERT WHAT THE BLOCK DID NOT MEASURE** (ex9).
- **CONSOLE SHOWS openjarvis WARNING+ ONLY;** uvicorn.access is file-only.
- **QuickEdit off kills mouse drag-select** in the backend console. The Pause
  key and Ctrl+S can still suspend output.
- **Audio probe `pid=0` = Windows system sounds;** its "System Idle Process"
  chain is a display artifact. Defaults: Elgato Wave:3 headphones (vol 0.44)
  and Elgato Wave:3 mic. Mic consent Allow everywhere.
- **`WEBVIEW2_ADDITIONAL_BROWSER_ARGUMENTS`** is set per process only; never
  set it user-wide.
- W61 carried: `tools\` gitignored (`git add -f`); the CLI gate must write the
  registry; protected list lives in `C:\Users\Admin\.openjarvis\`; ConfirmPolicy
  never denies; dry_run defaults true; build exits 1 on success and the
  running exe locks output; backend 8010; logs `%LOCALAPPDATA%\OpenJarvis\logs\`;
  start only via `.\start-openjarvis.ps1`.
- **USAGE:** after a 5-hour reset NEVER continue the old window (an ask there
  billed ~30 percent of a fresh session in W61).
### [ARCHIVE-W63-2026-09-17.md] RULES OF ENGAGEMENT
Full text ARCHIVE-W57 section 6; W61 additions in ARCHIVE-W62 carried brief.
GRAY UPLOADS WHOLE FILES; CLAUDE DOES NOT ISSUE READS. ONE RUNNABLE BLOCK PER
MESSAGE. State shell and host first; run from `PS C:\Users\Admin\OpenJarvis>`;
Ubuntu ollama host 172.16.33.200. No non-ASCII. .NET static methods need
ABSOLUTE paths. ALWAYS VERIFY. FINISH THE THING. PATCH WHAT WE FIND.
VALIDATE, DO NOT INTERROGATE. Tests NON-INTERACTIVE. Author's resources
FIRST. PRODUCTION BUILD ONLY. Push to BOTH remotes (`origin` = GitHub,
`gitlab` = lab). New `tools\` files need `git add -f`. Flag at 15 exchanges;
never cut a live trace. TOKEN CONSERVATION. DO NOT RE-DERIVE PRIOR WORK
WITHOUT ASKING. BUILD THE HANDOFF SCAFFOLD IN EXCHANGE 1 (extract, do not
retype). 550B PATTERN: bundle whole files with the prompt embedded plus a
script that posts to openrouter nemotron-3-ultra-550b. SDP, execution paths,
tooling register, logging topology: ARCHIVE-W62 delta sections; every window
feeds them, negative results included.
W62 lessons: **A LOCKED FILE RETURNS A DEFAULT, NOT A RESULT. A POSITIVE
CONTROL TURNS "NOTHING SEEN" INTO EVIDENCE. A CLICK IN A CONSOLE CAN STOP A
SERVER.**
**Program goal:** a functional executive assistant doing a human's computer
duties. W62 removed a way the whole server could silently freeze (approvals
included) and localized lost voice to the desktop app. Voice (Requirement
One) is still down; requirements measurement is still unbuilt.

