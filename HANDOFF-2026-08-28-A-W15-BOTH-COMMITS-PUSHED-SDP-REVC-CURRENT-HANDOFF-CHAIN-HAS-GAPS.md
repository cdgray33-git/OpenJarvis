# HANDOFF 2026-08-28 A - W15

## BOTH W14 NEXT-ACTIONS CLOSED. v2 COMMITTED AND PUSHED. SDP AT REVISION C. THE HANDOFF CHAIN ITSELF HAS GAPS.

Predecessor: `HANDOFF-2026-08-26-C-W14-OPEN-ITEM-1-CLOSED-REDACTION-COMPLETE-UNCOMMITTED.md`
W14 remains the authority on the v2 patch content and its verification evidence.
This file closes W14 next-actions 1 and 2, and opens a new problem class that is
not about the code at all.

Window opened 08/28 morning, closed at exchange 21. No source file was modified
this window. Two commits, one generated artifact, one inventory finding.

---

## 0. STANDING INSTRUCTIONS CARRIED FORWARD

Pinned. The next window inherits these without renegotiation.

- TOKEN CONSERVATION MODE on working sessions. Short replies, one command at a
  time, minimal restating.
- ALWAYS STATE SHELL AND HOST. Default is PowerShell on the Windows box from
  `PS C:\Users\Admin\OpenJarvis>`. Anything for the Ubuntu ollama host
  (172.16.33.200) must be labeled or wrapped as an ssh command.
- WORKING DIRECTORY IS FIXED at the repo root. Every command must run correctly
  from there. Path, shell or host differences are stated IN THE REQUEST, before
  it is run, never after it fails.
- NO non-ASCII symbols in replies.
- ALWAYS VERIFY. Never stack a second change on an unverified first one.
- FINISH THE THING BEFORE STARTING THE NEXT. No dangling processes.
- DESIGN TESTS TO BE NON-INTERACTIVE.
- SDP IS THE SECONDARY THOUGHT AT ALL TIMES. Every window feeds it.
- EXECUTION PATH REGISTER accumulates across windows. Never re-derived.
- PIN THE DETAIL OF EVERY WINDOW, INCLUDING THE NEGATIVE RESULTS.
- 15-exchange flag is a FLAG, NOT A STOP.
- ARCHITECTURE ARTIFACTS need ports, protocols and encoding at each gate, and
  are delivered as downloadable standalone files for the wiki.
- W12-R1: a command goes in a fenced code block ONLY if it is the command to run
  right now. Reference and restore commands go inline in prose, unformatted.
- W13-R1: an instrument that has never produced a positive reading cannot have
  its silence read as a finding.
- W13-R2: look for the existing harness before writing a new one.
- W13-R3: state the execution context for a script, not just its path.
- W14-R1: one command per message means ONE DESTINATION per message. Never mix a
  PowerShell command and a chat-app message to type in the same reply.
- W14-R2: write control expectations against the POST state.
- W14-R3: a wildcard that matches nothing is silent in PowerShell. Every delivery
  command assigns to a variable and prints a loud NOT DOWNLOADED message on the
  empty case.

NEW RULES ADDED THIS WINDOW:

- **W15-R1. ALWAYS PUSH TO BOTH REMOTES, UNPROMPTED.** Gray keeps GitHub and his
  own GitLab instance in sync deliberately. Every commit goes to both in the same
  session, without being asked and without a reminder. `origin` is GitHub,
  `gitlab` is the lab instance at 172.16.33.126 - that naming is a trap worth
  restating in every window.
- **W15-R2. A DOCUMENT DESCRIBED AS LIVING IS NOT STALE BETWEEN UPDATES.** The
  SDP artifact is a logbook that records ground truth as it is established, not a
  spec that has drifted from an implementation. Being behind the latest window is
  its normal state, not a defect. What IS a defect is an assertion inside it that
  has since been disproven, because a reader cannot tell which parts are current.
  Raise the second, do not raise the first.
- **W15-R3. VERIFY THE INSTRUMENT, NOT ONLY THE RESULT.** The revC patch was
  dry-run in Claude's container against the same source file BEFORE being sent to
  the Windows box, and both runs produced identical source and output SHA256s.
  That is what makes the box-side dry run a confirmation rather than a first
  attempt. Do this wherever the artifact can be uploaded.

---

## 1. WHAT WAS DONE

Two W14 next-actions, in order, each verified before the next was started. No
source file was touched. Both remotes are current.

### 1.1 Next-action 1 - the v2 change committed and pushed

PRE-COMMIT VERIFICATION: `ws_bridge.py` read off disk at 4,514 B with SHA256
`BD8904CD9564D7FA07AF4566CF2B41ACD10774A4C02D46A633CE2B68FB2AD3F6`, matching
W14's recorded post-patch state exactly. The file committed is the file verified.

`git status --short` showed 13 modified files and roughly 150 untracked. Staged
by explicit path, three files only.

| Property | Value |
|---|---|
| Commit | `4c365c1` on `main`, parent `6c132d6` |
| Scope | 3 files, 890 insertions, 5 deletions |
| Modified | `src/openjarvis/server/ws_bridge.py` |
| Added | `patch_ws_cid_redact_v2c.py`, `SDP-WS-EVENT-CHANNEL-2026-08-26-revB.md` |
| Excluded | The `.bak` file and 12 other dirty files in the tree |
| Push | `6c132d6..4c365c1` fast-forward on origin AND gitlab |

ROLLBACK: git revert 4c365c1 - or Copy-Item 'src\openjarvis\server\ws_bridge.py.bak_cidredactv2_20260826_083355' 'src\openjarvis\server\ws_bridge.py' -Force followed by a RESTART.

**THE `.bak` HAZARD WAS ALREADY HANDLED.** W14 open item 1 warned that
`ws_bridge.py.bak_cidredactv2_20260826_083355` sits in the tree and must not be
committed. It did NOT appear in `git status --short` at all, so something already
excludes it. The warning was sound; the risk was already mitigated. Staging by
explicit path meant it could not have landed regardless.

**EOL NORMALIZATION, PIN THIS.** The commit emitted `warning: in the working copy
of 'src/openjarvis/server/ws_bridge.py', CRLF will be replaced by LF the next time
Git touches it`. The working copy is CRLF; the committed blob is LF. That is
autocrlf, not corruption. Any EOL measurement taken from a fresh clone will
differ from one taken on this working copy, and the difference is EXPECTED. This
bears directly on the unresolved `_stubs.py` EOL contradiction (open item 9) -
re-measure, do not inherit, and do not read a mismatch there as damage.

### 1.2 Next-action 2 - SDP revision C

Read revB at source first. Amended IN PLACE, not rewritten, by
`patch_sdp_revc.py` (repo root, marker `openjarvis-sdp-ws-event-channel-revC`).
Fifteen anchored replacements, each asserted to match exactly 1, plus eight
post-state assertions that fail the run if an obsolete claim survives.

| Property | Value |
|---|---|
| Source | revB, 32,391 B, SHA256 `8763E410A0DD1344B32183FC3CB2A1130F12789E29B437B525B01FC38BAFBF2A` |
| Output | revC, 41,966 B (delta +9,575), SHA256 `EDC70B593BFDE73BFDD93DD8759A935697824E107A8C3D1B89029CD4609747E2` |
| EOL | pure LF preserved, 0 CRLF, 0 non-ASCII |
| Controls | 15 anchors all matched exactly 1; 8 post-state assertions all OK |
| Round trip | predicted 41,966 / actual 41,966, byte-identical |
| Independent check | hash and five section markers read back off disk after write |

The script writes revC alongside revB and does not modify revB. revB is retained
in the tree so the revision chain stays readable, and it is committed at
`4c365c1` regardless.

WHAT REVISION C CHANGED:

- Header: revision C, marker `openjarvis-ws-cid-redact-v2`, commit of record
  `4c365c1`, predecessor `6c132d6`, plus the note that the v1 marker is NOT
  unique in `ws_bridge.py`.
- 3.2: the "STILL CARRIES `confirm_id` UNREDACTED" claim REMOVED and replaced
  with the redacted behavior and a pointer to 6.5.
- 3.3: scoped to BOTH confirm event types; warning documented as
  frame-type-parameterized; the four-edits-not-one-line scope correction pinned.
- 5: three new timing rows - TTL 120.013 s third measurement, 1.6 s reap-to-
  re-request, 245.8 s total user-visible failure.
- NEW 6.5: the v2 verification pair, the post-reboot process-age precondition,
  and the honest limit about the lost in-run positive control.
- 7.2: OVERTURNED. The `ua=` field works; the limitation is PowerShell 5.1
  `ClientWebSocket` only. Removal recommendation withdrawn.
- 8: item 1 CLOSED, item 4 CLOSED, item 5 CORRECTED on evidence, new item 8 for
  the `reaped` flag.
- 9: posture C raised from HALF to FULLY implemented for this transport, with an
  explicit scope limit and a statement that correct is not the same as usable.
- NEW 10.1: commit `4c365c1`, the EOL note, and the two patch-discipline items.

| Property | Value |
|---|---|
| Commit | `38e907d` on `main`, parent `4c365c1` |
| Scope | 2 files, 1,249 insertions |
| Added | `SDP-WS-EVENT-CHANNEL-2026-08-26-revC.md`, `patch_sdp_revc.py` |
| Push | `4c365c1..38e907d` fast-forward on origin AND gitlab |

BOTH PUSHES CONFIRMED BY `git ls-remote --heads`: origin and gitlab returned the
identical hash `38e907dd082745c7bba1e172d2bc43fd0d6b9684`. Remote agreement was
verified, not assumed from a successful push.

---

## 2. THE HANDOFF CHAIN HAS GAPS - NEW PROBLEM CLASS

Not a code finding. It concerns the SDD source material itself, which makes it
an SDP-relevant risk rather than a housekeeping note.

Inventory taken across the repo root and `%USERPROFILE%\Downloads`.

### 2.1 Four windows have no handoff anywhere

W1, W2, W7, W8, W9, W10, W11, W12, W13 and W14 all have files.
**W3, W4, W5 and W6 have NO file in either location.** Either those windows were
never written up, or the files are gone. Which of the two is unestablished.

### 2.2 W10 exists as two different documents

Same window letter, different titles, different sizes, neither present in both
locations.

| Location | Title | Size |
|---|---|---|
| Repo root | `...W10-GATE-BYPASS-MECHANISM-FOUND-AT-EXECUTOR-CONSTRUCTION.md` | 42,211 B |
| Downloads | `...W10-GATE-FIRED-ON-ALL-SIX-ANOMALY-RETRACTED-CONFIRM-CLIENT-UNIDENTIFIED.md` | 29,566 B |

Their headers state different conclusions. The Downloads one retracts the
no-block anomaly and leaves the answering client unidentified. The repo one says
the no-block is explained, the gate is deterministic and the executor is not, and
traces the mechanism to executor construction.

READ TOGETHER THAT IS A PROGRESSION, NOT A CONTRADICTION - the repo version is
almost certainly the later, fuller write-up of the same window, and the size
supports it. BUT THAT IS INFERENCE FROM HEADERS, NOT ESTABLISHED. Given how much
later work rests on the executor-construction finding, W10 should not stay
ambiguous. Resolve it by reading both in full, not by reasoning about titles.

### 2.3 A same-name size difference that turned out to be nothing

`HANDOFF-2026-08-23-C-AGENT-FIELD-CONFIRMED-PROBE-V3-SPEC.md` is 19,635 B in the
repo and 19,368 B in Downloads. The 19,368 figure is also the exact size of
`HANDOFF-2026-08-20-6d-APPLIED-VERIFIED.md`, which raised a wrong-content-under-
the-right-name theory. HEADERS READ: identical first five lines. Same document;
the difference is line endings. **THEORY DEAD, recorded because it was checked.**

### 2.4 Single-copy files - RESOLVED THIS WINDOW

W13 existed only in the repo root; W14 only in Downloads. Both were copied so
each now exists in both locations. Verified by size after: W13 at 26,285 B in
both, W14 at 36,719 B in both.

CLAUDE'S ERROR DURING THAT COPY, recorded per the negative-results rule:
`Get-ChildItem -Filter '*W13*','*W14*'` throws - `-Filter` takes a single string,
not an array. Use `-Path .\* -Include 'a','b'` for multiple patterns. The two
`Copy-Item` calls ran before the failure, so only the verification half broke and
it was re-run separately.

### 2.5 The handoffs are untracked, by decision

Every handoff in the repo root shows as `??` in `git status`. Raised as a
single-machine risk. **GRAY'S DECISION: not tracking them.** They are saved and
retrievable from the chat history. Recorded here so a future window does not
re-litigate it.

ONE THING THE NEXT WINDOW SHOULD KNOW rather than re-raise: chat history is a
retention policy, not a backup under Gray's control. He is aware. Do not bring it
up again.

---

## 3. EXECUTION PATHS REGISTER

Carried unchanged from W14. Nothing this window touched an execution path.

- Orchestrator `ask()` via `system\orchestrator.py`.
- Managed-agent SSE via `_stream_managed_agent()` in
  `server\agent_manager_routes.py`.
- `routes.py` chat dispatch branches 1a/1b/1c/1d.
- The confirm-gate flow as verified, W14 Appendix B.1, stages 1 through 11b.

Gate/transport facts unchanged: bind `127.0.0.1:8010`, route `/v1/agents/events`,
WebSocket over HTTP/1.1 upgrade, UTF-8 JSON via `send_json`, accept
unconditional, auth via query-string `token` against env `OPENJARVIS_WS_TOKEN`,
field redaction on BOTH confirm event types.

---

## 4. SDP / SDD FEED FROM THIS WINDOW

**`SDP-WS-EVENT-CHANNEL-2026-08-26-revC.md` is CURRENT as of `38e907d`.** It
contains no known false statement. That is a first for this artifact - revB
asserted two things that were disproven while it sat.

What a future revision D would need, none of it urgent:

- Section 10.2 for `38e907d` itself, once anything downstream depends on it.
- Open item 8 (`reaped` flag) resolved against `confirm_registry._snapshot()`.
- Open item 5 rewritten again once the token source is actually located.

NEW MATERIAL FOR THE METHODOLOGY CHAPTER:

- **The living-document distinction (W15-R2).** An artifact that records ground
  truth as it is established has a different staleness contract than a spec.
  Behind is normal; internally contradicted is the defect. Claude got this wrong
  in this window and was corrected. Worth stating explicitly in the SDD so the
  distinction is not re-derived.
- **Cross-machine determinism as instrument verification (W15-R3).** The revC
  patch produced identical source and output SHA256s in Claude's container and on
  the Windows box. That turns the box-side dry run from a first attempt into a
  confirmation, and it is available for free whenever the input can be uploaded.
- **Post-state assertions as a second control layer.** The revC script asserts
  not only that 15 anchors matched, but that four obsolete strings are ABSENT
  from the output - "STILL CARRIES", "HALF IMPLEMENTED", "For TOOL_CONFIRM_REQUEST
  only:". Anchor counts prove the edits fired. Absence assertions prove the old
  claim is gone. They are different failures and both are worth catching.
- **SDD source-material integrity is now a tracked risk** (section 2). The
  register the SDD is built from has four missing windows and one ambiguous one.

---

## 5. OPEN ITEMS, ORDERED

Renumbered from W14. Items 1 and 2 of W14 are closed.

1. **TOKEN PERSISTENCE - the source is unlocated.** Carried from W14 section 3,
   unchanged this window. The token survived a genuine reboot and nobody can say
   why. Not in env at any scope, not in `start-openjarvis.ps1`, not in `.env`,
   not in any repo-root `.ps1`. Remaining candidates: the launching shell, and
   the desktop app's spawn chain. GATES ITEM 2. No secret goes into `.env` while
   that file is in its current state.
2. **6e. NO USER CAN ANSWER A GATE.** Unchanged and still the only thing between
   this feature and being usable. Mount `useAgentEvents`
   (`frontend\src\lib\useAgentEvents.ts`, points at `/v1/agents/events` at line
   19) with NO `agent_id` param, plus the token from item 1. Every gate measured
   in W14 reaped at 120 s and the user saw an apology.
3. **W10 is two documents that disagree.** Section 2.2. Establish which is
   authoritative before anything else cites the executor-construction finding.
4. **W3 through W6 have no handoff anywhere.** Section 2.1. Establish whether
   they were written and lost, or never written.
5. **Destructive mailbox tools are ungated at the spec level.** Only
   `agent_tools.py:289`, `git_tool.py:283`, `shell_exec.py:71` declare
   `requires_confirmation=True`. Coverage gap, not a mechanism gap. Needs a Gray
   decision.
6. **Four auto-approve sites live** in `server\agent_manager_routes.py`
   (720-721, 1202-1206, 1562-1563, 1639-1640). Accept or overturn explicitly.
   Needs a Gray decision.
7. **Silent frame drop on queue overflow** still has no instrument.
8. **`"reaped": false` on timeout resolutions** unexplained. Read
   `confirm_registry._snapshot()`.
9. **Four `[DEBUG]` prints in `cli\serve.py`** at 268, 280, 281, 513, shipped in
   `6c132d6` and still present.
10. **`_stubs.py` EOL baseline contradiction** unresolved. Re-measure, do not
    inherit - and see the autocrlf note in section 1.1 before reading any
    mismatch as damage.
11. **08/05 GitLab history damage below the tip** still unassessed. The tip is
    confirmed an ancestor of local main; older history is not.
12. **65-package venv mutation on start** still unchased.

CLOSED THIS WINDOW: W14 open item 1 (v2 uncommitted) and W14 next-action 2 (SDP
stale). Also closed: the single-copy exposure on W13 and W14.

---

## 6. NEXT ACTIONS, ORDERED

1. **Locate the WS token source** (open item 1). Start with the desktop app's
   spawn chain - it is the more likely of the two remaining candidates and can be
   read without touching anything. Then decide its durable home.
2. **Build 6e.** Only after 1.
3. **Resolve the W10 ambiguity** (open item 3). Read both files in full. Cheap,
   read-only, and it protects everything downstream that cites W10.
4. Then open items 5 and 6 - both need a Gray decision, not just code.

Do not skip ahead to 2. Nothing has changed since W14 on this point: everything
measured says the gate is correct, and nothing says it is usable.

---

## APPENDIX A. DISCREPANCY REGISTER

Every point this window where the WRITTEN RECORD disagreed with DIRECT
OBSERVATION, or where Claude was wrong. Recorded whether or not it changed the
outcome.

### D1. "The `.bak` file must not be committed" - RISK ALREADY MITIGATED
- CLAIMED BY: W14 open item 1, as an active hazard.
- FOUND: `ws_bridge.py.bak_cidredactv2_20260826_083355` does not appear in
  `git status --short` at all. Something already excludes it.
- ESTABLISHED BY: full `git status --short` read before staging.
- DISPOSITION: the warning was sound and cost nothing. Staging by explicit path
  made it moot regardless. Not a defect in the W14 record - a hazard that had
  already been handled by other means.

### D2. "The SDP artifact is dangerously stale" - CLAUDE'S FRAMING ERROR
- CLAIMED BY: Claude, this window, with urgency.
- CORRECTED BY: Gray. The SDP is a LIVING DOCUMENT created to capture exactly
  this - ground truth gets documented and updated as it is discovered. Being
  behind the newest window is its designed state, not a failure.
- WHAT SURVIVES THE CORRECTION, narrower and still true: revB asserted two things
  that had been disproven (3.2 on the resolved frame, 7.2 on the `ua=` field),
  and a reader mid-cycle cannot tell which parts are current. That is an argument
  for doing the update, not an alarm about it.
- DISPOSITION: rule W15-R2. Raise internal contradiction, not lateness.

### D3. "Same name, different size means wrong content" - THEORY DEAD
- CLAIMED BY: Claude, on the 08-23-C pair, reinforced by the coincidence that
  19,368 B is also the exact size of `HANDOFF-2026-08-20-6d-APPLIED-VERIFIED.md`.
- FOUND: identical first five lines in both copies. Same document.
- ESTABLISHED BY: `Get-Content -TotalCount 5` on both.
- DISPOSITION: dead. The size delta is line endings. A size coincidence is not
  evidence of content substitution, and the check that settled it cost one
  command.

### D4. `Get-ChildItem -Filter` with an array - CLAUDE'S ERROR
- WHAT: `-Filter '*W13*','*W14*'` throws `Cannot convert 'System.Object[]' to the
  type 'System.String'`. `-Filter` accepts one string only.
- IMPACT: the verification half of a combined copy-and-verify command failed. The
  two `Copy-Item` calls had already run, so no work was lost, but the copy sat
  unverified until a second command was issued.
- DISPOSITION: use `-Path .\* -Include 'a','b'` for multiple patterns. Note the
  shape of the failure - a command that does real work and then fails on its own
  verification leaves the work in an unconfirmed state. Put the verification in
  its own command when the work is not idempotent.

### D5. W10 duplication - UNRESOLVED, RAISED
- See section 2.2. Two documents, same window, different stated conclusions,
  neither in both locations.
- DISPOSITION: open item 3. Do not settle it by reasoning about titles.

### D6. Four windows missing from the record - UNRESOLVED, RAISED
- See section 2.1. W3, W4, W5, W6 have no file in either location.
- DISPOSITION: open item 4.

---

## APPENDIX B. THE REVISION C PATCH - REPRODUCTION

`patch_sdp_revc.py` is committed at `38e907d` and is deterministic. Re-running it
against an unmodified revB will produce revC byte-for-byte.

From `PS C:\Users\Admin\OpenJarvis>`:
python .\patch_sdp_revc.py            (dry run, writes nothing)
python .\patch_sdp_revc.py --apply    (writes revC alongside revB)

PRECONDITIONS THE SCRIPT ENFORCES ITSELF, each an abort rather than a warning:
- source is exactly 32,391 B, or ABORT
- source is pure LF, or ABORT - it refuses to rewrite EOLs silently
- all 15 anchors match exactly 1, or ABORT
- all 8 post-state assertions pass, or ABORT
- output is pure LF, or ABORT
- after write, the file is read back and compared to what was generated

EXPECTED OUTPUT: source SHA256
`8763E410A0DD1344B32183FC3CB2A1130F12789E29B437B525B01FC38BAFBF2A`, output
SHA256 `EDC70B593BFDE73BFDD93DD8759A935697824E107A8C3D1B89029CD4609747E2`,
41,966 B. These were produced identically in Claude's container and on the
Windows box, which is what makes the box-side dry run a confirmation rather than
a first attempt.

INDEPENDENT VERIFICATION AFTER APPLY, not trusting the script's own report:
$f='SDP-WS-EVENT-CHANNEL-2026-08-26-revC.md'; "{0} B" -f (Get-Item $f).Length; (Get-FileHash $f -Algorithm SHA256).Hash

Five section markers should be present: `REVISION C` at line 7, the posture
statement at 18, `### 6.5 Part three` at 387, `POSTURE C IS FULLY IMPLEMENTED` at
657, `### 10.1 The v2 commit` at 731.

---

## APPENDIX C. GIT STATE AT WINDOW CLOSE

| Property | Value |
|---|---|
| HEAD | `38e907d` on `main` |
| origin (GitHub) | `38e907dd082745c7bba1e172d2bc43fd0d6b9684` |
| gitlab (172.16.33.126) | `38e907dd082745c7bba1e172d2bc43fd0d6b9684` |
| Divergence | none - verified by `git ls-remote --heads`, not inferred from push output |
| Commits this window | `4c365c1` (v2 redaction), `38e907d` (SDP revision C) |

Both pushes were plain `git push <remote> main:main`. No force, no mirror, no
prune, no upstream set. Given the 08/05 mirror-push incident on this exact GitLab
remote, that shape is deliberate and should stay deliberate.

STILL DIRTY IN THE TREE, untouched and intentionally so: 12 modified files
(TTS, mailbox, engine, frontend, config) and roughly 150 untracked probe and
patch scripts. None of it belongs to this work. Do not clean it up as a side
task - see the FINISH THE THING rule.
