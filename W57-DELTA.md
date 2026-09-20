## 1. W57 WINDOW DELTA - AUTHORED, NOT CARRIED

Everything below section 1 was copied VERBATIM from a prior archive by
`build_archive_w57.py` and must not be rewritten - append dated one-line
DELTAS only.

### 1.1 WINDOW SUBJECT AND OUTCOME

Subject as opened: gate the two destructive mailbox tools
(`mailbox_move_to_trash`, `mailbox_empty_folder`), which the W56 brief listed
as action 3 and described as "now cheap."

Outcome: **the flags were NOT set, deliberately, on Gray's ruling.** No source
was changed. What the window produced instead is a measured account of what
actually stands between the model and a destructive mailbox action, which
turned out not to be what either of us believed at the start.

This is a window that changed nothing and produced knowledge. Per the 08/24
rule it is pinned in full.

### 1.2 THE TWO MECHANISMS, AND WHY CONFLATING THEM COST TWO EXCHANGES

There are two separate things in this tree that both get called
"confirmation." They share no code.

**Mechanism A, the real gate.** A ToolSpec declares
`requires_confirmation=True`. `ToolExecutor.execute` stops at the gate in
`tools\_stubs.py`, registers a confirm id, emits `tool_confirm_request` on the
bus, and blocks in `_server_confirm_callback` on `_cr.wait(cid)` against a
120 s TTL. The WS bridge carries the frame to the browser.
`ConfirmPrompt.tsx` renders a floating panel with **Approve and Deny buttons
and a seconds-remaining countdown**. The answer POSTs to
`/v1/tools/confirm`. This is structurally enforced: the tool body does not run
until the registry resolves.

**Mechanism B, the prose interlock.** Inside `mailbox_tools.py`, `_confirmed()`
returns True only when `dry_run` is falsy AND `confirm` equals the exact string
`CONFIRM DELETE`. Otherwise the tool returns a dry-run plan whose
`instruction` field tells the model to show the plan to the user and ask for
approval. The human approval happens in PROSE, in the chat window. **The
caller that then satisfies the interlock is the MODEL.**

Gray reported that a confirm prompt appears when he moves email and that he
must type "confirm" before the agent acts, and that this is present because he
insisted email be confirmed by a human. Claude initially took that as evidence
Mechanism A was live for mailbox tools. It is not. `ConfirmPrompt.tsx` has no
text input anywhere in it - it is two buttons and a countdown. Typing a word
is Mechanism B.

Gray then supplied the fact that settled it: he HAS seen Approve and Deny, and
clicked Approve about three times, on the test commands Claude provided,
before the move to non-interactive testing. Those tests used `shell_exec`.

So: Mechanism A is real and human-verified on `shell_exec`. Mechanism B is
what guards his mail.

### 1.3 THE INSTRUMENT AND WHAT IT MEASURED

Gray's correction, which is now a rule of engagement: "validate and not ask
questions without testing the current state." Two exchanges had gone into
asking him what he remembered. He was right to stop it.

`validate_gates_w57.py` (repo root, 15,337 B, read-only, non-interactive).
Result **10 PASS / 3 FAIL / 0 SKIP**. All three FAILs are findings, not faults.

SECTION A - spec truth on disk, parsed with `ast` rather than regex, because a
regex cannot tell a declaration from a comment mentioning one:

- `mailbox_tools.py` holds 5 ToolSpec calls. `mailbox_list_accounts` (177),
  `mailbox_usage_report` (206), `mailbox_find_messages` (272),
  **`mailbox_move_to_trash` (474)**, **`mailbox_empty_folder` (759)**.
  **NONE declares `requires_confirmation`.** The field defaults False, so an
  absent flag is an open tool.
- `shell_exec.py:35` declares `requires_confirmation=True`. The control holds,
  so Section A itself is sound.
- `imap_mail.py` `mcp_tools()` holds 4 declarative specs. `mailbox_move_to_trash`
  at 872 and `mailbox_empty_folder` at 893 **DO declare
  `requires_confirmation=True`.** Those specs are display-only - the connector's
  own docstring says they are enumerated for display and are NOT what the agent
  executes. **The intent to gate these tools exists in the tree and landed on
  the layer that cannot enforce it.** A register that disagrees with the code
  is the finding (W47).

SECTION B - the interlock as a pure function, importing the real `_confirmed`,
6 of 6 PASS:

| case | applies |
|---|---|
| no params at all | False |
| `dry_run=True` with the token | False |
| `dry_run=False`, no token | False |
| `dry_run=False`, wrong-case token | False |
| `dry_run="false"` (string) plus token | True |
| `dry_run=False` plus exact token | True |

**The load-bearing case is the last one.** A single call carrying both fields
applies immediately. There is no state, no requirement that a dry run happened
first, and no human in the path. Whichever caller sets those two fields
performs the deletion.

SECTION D - the live confirm route, 3 of 3 PASS. `GET /v1/tools` 200 (18,129
bytes). Unknown id 404. Bad decision 400. The 400 is load-bearing: nothing but
our own handler returns it, and the `confirm_registry` import sits above body
validation, so a failed import would give 500 instead.

SECTION E - 12 confirm harnesses already in the repo root, listed in the
tooling register delta below.

### 1.4 GRAY'S RULING - HOLD THE FLAGS

Claude proposed setting `requires_confirmation=True` on both mailbox tools this
window, then caught a problem in its own proposal before Gray acted on it:

**`requires_confirmation` is a SPEC-level boolean. The gate cannot see the
call's arguments.** So the flag gates the dry-run call as well as the applying
call. One deletion would cost two Approve clicks against two 120 s TTLs, and
the first click guards an operation that changes nothing.

Gray's ruling: **HOLD.** His reasoning, recorded in his words: the two clicks
currently work and do not hurt anything; it is not fully fleshed out as a
service; basically in development. The argument-aware gate comes first.

This is the correct call and supersedes the W56 brief's framing of action 3 as
"now cheap."

### 1.5 NEGATIVE RESULTS AND DEAD THEORIES

**DEAD - "navigating away from chat causes the 120 s timeouts."** Claude
asserted this as though it were a finding. It is unsupported. Every 120 s block
on record (08/21, 08/22 at 120.004 s) happened when NO browser listener existed
at all; `ConfirmPrompt.tsx` dates its own frame-shape reads to 2026-09-12, well
after. Gray pushed back correctly - he pastes only what he is given and is not
the cause. **What is true:** ChatArea sits under the `/` index route, so a route
change unmounts it and closes the socket. That is a structural property of the
code and has NEVER been observed to fire. Do not carry the causal claim.

**DEAD - "the listener move is 190 lines."** The carried note was wrong about
scope. `useAgentEvents.ts` already carries the `subscribeAll` opt-in (marker
`openjarvis-agent-events-subscribeall-v1`) and `ConfirmPrompt.tsx:97` already
calls it correctly as `useAgentEvents(undefined, onEvent, CONFIRM_EVENTS,
true)`. Only the `<ConfirmPrompt />` JSX element needs to move. The hook and
the subscription stay where they are.

**NOT A DUPLICATE-SOCKET RISK.** `AgentsPage.tsx:1736` and `:3338` both call
`useAgentEvents` with a real `agentId`, so both are filtered managed-agent
listeners. They cannot receive chat-path confirm frames, which carry the
executor CLASS identity `native_openhands`.

**NOT STALE - the `mailbox_tools.py` SAFETY NOTE, partially.** Its W49 status
block says the flag stays off because no consumer of `POST /v1/tools/confirm`
has been proven to resolve the id. That specific claim IS now stale - one was
proven 08/22 and again 08/24, and Gray has clicked Approve since. But the
docstring's underlying caution was sound for a different reason it did not
know: the spec-level flag would gate the dry run too. **Do not delete that
note; correct it when the argument-aware gate lands.**

### 1.6 HAZARDS EARNED THIS WINDOW

**A DELTA SECTION AND A BASE SECTION MATCH THE SAME KEYWORDS.** The first
version of `build_archive_w57.py` resolved carried registers by "newest match
wins." On the real archives that selected W56's 19-line DIAGNOSTIC TOOLING
REGISTER DELTA over W52's 133-line base, and W56's 28-line EXECUTION PATHS
DELTA over W52's 182-line base - **discarding roughly 300 lines of register
while reporting success.** Correct shape is base plus every subsequent delta,
appended in order. Caught ONLY because the dry run printed line counts and 19
was visibly wrong where 133 was expected.

**A DRY RUN THAT PRINTS NO COUNTS IS NOT A DRY RUN.** A summary reading
"carried 5 sections" would have passed. The counts are what discriminate.

**THE BROWSER SAVES A SECOND DOWNLOAD AS `name (1).py`.** Fired again this
window - the selector printed `build_archive_w57 (1).py`. The newest-file
selector that PRINTS its choice is what made the corrected script run instead
of the stale one. Keep it on every delivery.

**CLAUDE DESCRIBED A SCRIPT WITHOUT PRODUCING IT.** The first
`validate_gates_w57.py` command was issued against a file that had never been
created; the selector bound null and the command failed. Produce the artifact,
then issue the command that runs it, in the same message.

**MOJIBAKE IN USER-VISIBLE STRINGS, NOT JUST COMMENTS.** `ChatArea.tsx` has
garbled characters in the system-panel `title` attribute (the Ctrl/Cmd hint)
and in the empty-state line about running locally. Both render on screen. The
known mojibake list previously implied comments only.

**TWO `[DEBUG]`-CLASS CONSOLE LINES STILL LIVE IN `ChatArea.tsx`** - the
`[TTSDBG]` `console.log` calls in the TTS driver effect. Diagnostic register
item, not removed this window.

### 1.7 SDD / SDP FEED

**SDP - THE GUARD IN PLAIN LANGUAGE.** The eight-year-old version, which the
SDP owes per the 09/02 requirement:

> There are two different locks on the mailbox. The first lock is a real one:
> the program stops, a box appears on your screen with an Approve button and a
> countdown, and nothing happens until you press it. The second lock is not a
> lock at all - it is a note taped to the door that says "please ask permission
> first." The assistant reads the note and usually does ask. But the assistant
> is also the one holding the door handle. If it ever decides not to ask, there
> is nothing in the way. Right now the mail is behind the note, not the lock.

**SDP - EVIDENCE STANDARD.** Every check in `validate_gates_w57.py` prints what
a PASS rules out, and Section C is ABSENT with its absence printed in the
script's own output rather than passing silently. An instrument that hides its
own gaps is worse than one that has none.

**SDD - ARCHITECTURE.** The confirm chain has four layers and the mailbox
tools sit outside it at layer 1:
1. ToolSpec declares `requires_confirmation` (mailbox: NO; shell_exec: YES)
2. `ToolExecutor` gate in `tools\_stubs.py` fires only on that flag
3. Bus emit -> `ws_bridge` -> browser `ConfirmPrompt`
4. `POST /v1/tools/confirm` -> `confirm_registry.resolve` -> callback unblocks

Layers 2, 3 and 4 are proven working. Layer 1 is the whole gap.

**SDD - THE DESIGN DEFECT TO RECORD.** `requires_confirmation` being
spec-level rather than call-level is an architectural limitation, not an
oversight in the mailbox tools. Any tool with a safe mode and a destructive
mode cannot be gated correctly under it. The argument-aware gate is the fix and
belongs in the SDD as a decision with this evidence behind it.

### 1.8 550B CLOUD MODEL

Not used this window. No question required whole-file bundling - Gray uploaded
`mailbox_tools.py`, `imap_mail.py`, `App.tsx`, `ChatArea.tsx`,
`useAgentEvents.ts` and `ConfirmPrompt.tsx` directly and each answered its
question on its own. Carried forward for the next window that needs it.

### 1.9 COMMITS

- `66a11a2` confirmed present on `origin` and `gitlab`, `src/` clean. This was
  W56's commit 2, whose landing was unknown at W56 close. **W56 action 1 is
  closed.**
- **W57 produced no commits.** Two untracked scripts added to the repo root:
  `validate_gates_w57.py`, `build_archive_w57.py`. Both belong in `tools/`.

### 1.10 DELTA - DIAGNOSTIC TOOLING REGISTER

Appended to the register carried in section 2. New instruments this window:

- **`validate_gates_w57.py`** - repo root, 15,337 B, read-only,
  non-interactive, exit 1 on any FAIL. Proves spec truth (`ast`), the prose
  interlock (6 cases), and the live confirm route (200/404/400). Output: stdout
  only, no file, no log. Deliberately does NOT fire the gate end to end and
  says so in its own summary.
- **`build_archive_w57.py`** - repo root, 9,708 B. Assembles the ARCHIVE
  scaffold by extraction. **Prints a manifest only, never section bodies** -
  that is what makes carrying registers free. `--dry-run` writes nothing.
  Refuses to overwrite an existing output file.

Harnesses confirmed PRESENT in the repo root (Section E, do not rebuild):
`patch_6d_confirm_live.py` 5409, `patch_6d_confirm_live_v2.py` 6137,
`patch_confirm_emit.py` 12062, `patch_confirm_resolved.py` 4348,
`patch_probe_confirmkey_v1.py` 3784, `probe_6d_confirm_live.py` 6845,
**`probe_confirm_emit.py` 13843**, `probe_confirm_frames.py` 7154,
`probe_confirm_trace_w50_v2.py` 10736, `test_confirm_policy.py` 3187,
`test_confirm_policy_cli.py` 3927, `test_confirm_policy_sites.py` 3120.

`probe_confirm_emit.py` is the one to run first next window.

### 1.11 DELTA - EXECUTION PATH REGISTER

Appended to the register carried in section 4. No new execution path was
discovered this window. One property recorded against the existing chat path:

- **Chat path, confirm leg, browser half.** Entry `ConfirmPrompt.tsx:97`,
  `useAgentEvents(undefined, onEvent, CONFIRM_EVENTS, true)` - unfiltered,
  no `agent_id` query param, so the server filter at `ws_bridge.py:56-59`
  short-circuits. Frames handled: `tool_confirm_request` (enqueue, deduped on
  `confirm_id` via a `seenRef` Set) and `tool_confirm_resolved` (dismiss, any
  outcome including TIMEOUT, so no local expiry timer is needed). Answer leg is
  `confirmTool(confirmId, decision)` -> `POST /v1/tools/confirm`, with 404 and
  409 both handled and 409 reading back the recorded decision. Human IS
  present. **Mount point is `ChatArea`, under the `/` index route - so the
  socket closes on any route change.** Never observed to fire.
- **`expires_at` unit remains UNVERIFIED**, per the W51 comment still in
  `ConfirmPrompt.tsx`. `normalizeExpiry` treats anything below 1e12 as epoch
  seconds and scales it. If a countdown ever reads wrong, that is the first
  line to check.
