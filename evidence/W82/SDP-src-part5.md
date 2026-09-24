# SDP SOURCE EXTRACT W82 part 5 (deduplicated by section hash)
### [ARCHIVE-W56-2026-09-13.md] 4. THE FIVE SITES, AND WHY THEY ARE NOT THE SAME
Four in `src\openjarvis\server\agent_manager_routes.py`, originally at 721,
1249, 1606, 1683:
- `dr-sse-stream` - `DeepResearchAgent` inside `generate_deep_research()`.
  Runs in a background thread; no confirm channel reaches the SSE client.
  `human_present=False`.
- `managed-agent-tool` - the `ToolExecutor` constructed per tool call inside
  the managed-agent tool loop. This is the site W54's toolkit bind protects.
  The original inline comment justified it: the user selected the tool in the
  wizard, so selection is the consent. That justification is now IN THE LOG,
  not only in a comment. `human_present=False`.
- `imessage-daemon` - `DeepResearchAgent` handed to `run_daemon`. Unattended.
  `human_present=False`.
- `sendblue-bridge` - `DeepResearchAgent` handed to `ChannelBridge`.
  Unattended. `human_present=False`.
Fifth, in `src\openjarvis\cli\ask.py`, `_run_agent`, formerly line 356:
- `cli-ask` - **`human_present=True`.** This is the finding the grep line could
  not have produced. `jarvis ask` is an interactive terminal command; a human
  is physically present. The auto-approve is there because nothing is wired to
  prompt stdin, NOT because the path is unattended. That is a GAP, recorded as
  a gap. The other four are a POSTURE. Collapsing them into one category would
  have destroyed the distinction.
All four route sites are INERT TODAY, and only by accident: W55 established
that none of the four tools returned by `_build_deep_research_tools()`
declares `requires_confirmation`, and the gate at `_stubs.py:337` fires only
on `True`. The `managed-agent-tool` site is NOT inert in the same way - it
constructs a `ToolExecutor` over an arbitrary registry tool, and `shell_exec`
and `apply_patch` do declare `requires_confirmation=True`.
---
### [ARCHIVE-W56-2026-09-13.md] 5. serve.py - THE REAL GATE THAT WAS SILENT
`serve.py` was uploaded whole on the assumption it held a sixth lambda. It did
not. `_server_confirm_callback` at :310 blocks on `_cr.wait(_cid)` and returns
the human's actual decision. It is the live chat gate, the one 6d wired.
A patch written from the grep line alone would have replaced a working gate
with an auto-approve. THE WHOLE-FILE UPLOAD PREVENTED THAT.
Its actual defect is the same class as the lambda: it returned `False` for
three unrelated reasons and wrote nothing distinguishing them.
- no `confirm_id` in context - a wiring fault, fails closed
- registry returned DENIED - the human refused
- registry returned TIMEOUT - nobody answered
`_outcome_reason` reconstructs these downstream by string-matching the
ToolResult content, which is inference from a message, not a record from the
decision point. Now the decision point itself logs, under
`site=chat-agent-live`, `human_present=True`:
- `decision=DENY_NO_CONFIRM_ID` before the early return
- `decision=WAIT` before blocking, carrying the confirm_id
- `decision=<registry outcome upper-cased>` after the wait returns
It still returns `_outcome == _cr.APPROVED`. Criterion 6 of the CLI harness
exists specifically to fail if a future window turns this into `return True`.
---
### [ARCHIVE-W56-2026-09-13.md] 6. EVIDENCE, HARNESSES, COMMITS
Three harnesses, all non-interactive, all exiting nonzero on any FAIL. All
three currently in the REPO ROOT and belong in `tools/` at flood triage.
`test_confirm_policy.py` - 7/7. Object-level. Importable, exported, returns
True, repr names the site, POLICY line lands in dispatch.log, line carries
`human_present` and `reason`, and - criterion 7 - a real `ToolExecutor` built
with a `requires_confirmation=True` stub tool accepts the policy in the
callback slot, the tool actually runs, and POLICY precedes `reason=OK`.
`test_confirm_policy_sites.py` - 7/7. AST over `agent_manager_routes.py`. Zero
bare lambdas, all four `confirm_callback` keywords are `ConfirmPolicy(...)`,
four distinct nonempty site tokens, every site has all three fields, all four
reasons over 30 chars (blocks placeholder text), module imports live, and the
bound `ConfirmPolicy` IS `tools._stubs.ConfirmPolicy` (blocks a shadow class).
`test_confirm_policy_cli.py` - 7/7. Tree-wide sweep plus `ask.py` and
`serve.py`. Criterion 1 tokenizes before judging - see section 7.
`classify_stub_hits.py` - one-shot adjudicator, kept as evidence of how the
false positive was ruled out rather than assumed away.
Commit 1, CONFIRMED on `origin` and `gitlab`:
`6bec081 W56: ban the bare lambda - named ConfirmPolicy at all four auto-approve sites`
Files: `_stubs.py`, `agent_manager_routes.py`, `test_confirm_policy.py`,
`test_confirm_policy_sites.py`. 4 files, 283 insertions, 5 deletions.
Commit 2, ISSUED, LANDING UNCONFIRMED. Files: `ask.py`, `serve.py`,
`test_confirm_policy_cli.py`, `classify_stub_hits.py`. Message subject:
`W56: name the fifth auto-approve (cli-ask) and the three branches of the real gate`
If it did not land, re-add those four paths and commit; body should record the
cli-ask human_present distinction, the serve.py three branches, and the
negative result in section 7.
---
### [ARCHIVE-W56-2026-09-13.md] 7. NEGATIVE RESULTS
**THERE IS NO SIXTH AUTO-APPROVE SITE.** Established, not assumed.
The first tree-wide sweep FAILED, reporting `src\openjarvis\tools\_stubs.py`.
That could have been a real site. It was adjudicated with the tokenizer rather
than by reading: `classify_stub_hits.py` walked the file with
`tokenize.generate_tokens`, collected every line covered by a COMMENT or
STRING token, and classified each regex hit against that set.
Result: exactly one hit, line 180, classified COMMENT_OR_DOCSTRING. It is the
line in the `ConfirmPolicy` header comment that quotes the banned pattern in
order to document it. VERDICT CLEAN.
So the sweep was matching its own documentation. The finding is about the
instrument, not the code: **a regex cannot tell prose from code, and an
instrument that cannot make that distinction will manufacture findings.** The
harness was corrected to tokenize first, and only then re-run - it now passes
7/7 with an empty hit list that means something.
Secondary negative result: **`serve.py:310` is not, and never was, a bare
lambda.** The grep line `def _server_confirm_callback(_prompt: str) -> bool:`
proved only that a callback exists there. See section 5.
---
### [ARCHIVE-W56-2026-09-13.md] 8. HAZARDS EARNED THIS WINDOW
- **`ask.py` is LF while the tree is generally CRLF.** A CRLF-normalized
  multi-line anchor silently fails to match. Detect per file:
  `$nl = if ($t.Contains("`r`n")) { "`r`n" } else { "`n" }` and build the
  anchor with `[string]::Join($nl, $lines)`.
- **A file Claude authored earlier in the same window is not known
  byte-exactly.** Two patch attempts against `test_confirm_policy_cli.py`
  aborted on anchor mismatch. Reissuing the file whole succeeded immediately.
- **PowerShell 5 has no heredoc.** `python - <<'PY'` produces "The '<'
  operator is reserved for future use". Write the .py, then run it.
- **Duplicate import lines make bad anchors.**
  `from openjarvis.connectors.store import KnowledgeStore` appears twice in
  `agent_manager_routes.py` - once at module top, once inside
  `_build_deep_research_tools()`. The `logger = logging.getLogger(...)` line
  is unique and was used instead.
- **Uniform indentation plus an AST parse is sufficient** when replacing at
  four sites of differing depth. Python accepted it; `ast.parse` confirmed it.
---
### [ARCHIVE-W56-2026-09-13.md] 9. SDD / SDP FEED
**serve.py is the API and startup path and MUST be a chapter.** Gray called
this explicitly on upload. It is the single place where the engine stack
(`get_engine` -> `setup_security` -> optional `MultiEngine` ->
`InstrumentedEngine`), the chat agent and its toolkit, the confirmation gate,
the channel bridge, the speech backend, the agent manager, the scheduler, the
memory backend, credentials, bind-safety and the uvicorn server are all
assembled. Ports, protocols and encoding at each gate per the 08/22 rule:
backend binds 8010; logs to `%LOCALAPPDATA%\OpenJarvis\logs\backend.log` via
`_configure_file_logging` with `SanitizingFormatter` and
`_TelemetryNoiseFilter`; `app.state.bind_is_loopback` is PUBLISHED HERE and
the WS confirm-channel redaction keys on it; `BIND_ASSERT` is logged at
WARNING on every start.
**Confirmation architecture chapter gains a third component.** It is now:
(1) the gate at `_stubs.py:337` that fires on `requires_confirmation`;
(2) the registry plus `POST /v1/tools/confirm` round trip;
(3) the CALLBACK POLICY LAYER - what is plugged into the callback slot at each
construction site, and what it records. Component 3 is new and is what makes
components 1 and 2 auditable after the fact. Document the five
`ConfirmPolicy` sites and `_server_confirm_callback` as one table:
site, human_present, posture, live-or-inert, and why.
**Design principle for the SDP, stated plainly:** a guard has three separable
properties - does it exist, does it fire, and can you tell afterwards what it
did. W53/W54/W55 addressed the first two. W56 addressed the third. All three
are required; none substitutes for another.
**Open SDP question, unanswered:** the four DR-site policies are inert only
because no DR tool declares `requires_confirmation`. Whether that is the
intended design or an oversight has never been ruled on. Document it as an
open question, not as a decision.
---
### [ARCHIVE-W56-2026-09-13.md] 10. EXECUTION PATHS DELTA
Append to the W52 register. Per-path field added this window:
**WHAT IS IN THE CONFIRM CALLBACK SLOT, AND WHAT IT WRITES.**
- Managed-agent SSE stream, `_stream_managed_agent()` - non-DR branch. Slot:
  `ConfirmPolicy(site="managed-agent-tool", human_present=False)`. Writes
  POLICY on every gated dispatch. Executor is constructed PER TOOL CALL inside
  the loop, over a single tool instance, after the W54 toolkit bind refusal.
- Managed-agent SSE stream - `deep_research` branch, `generate_deep_research()`.
  Slot: `ConfirmPolicy(site="dr-sse-stream", human_present=False)`. RETURNS
  BEFORE the non-DR tool loop. Executor is the agent's own, wrapped by
  `_tracked_execute` for progress events.
- iMessage daemon, spawned from `bind_channel` on `channel_type == "imessage"`.
  Slot: `ConfirmPolicy(site="imessage-daemon", human_present=False)`.
- SendBlue bridge, spawned from `bind_channel` on `channel_type == "sendblue"`.
  Slot: `ConfirmPolicy(site="sendblue-bridge", human_present=False)`.
- CLI `jarvis ask -a <agent>`, `ask.py::_run_agent`. Slot:
  `ConfirmPolicy(site="cli-ask", human_present=True)`. Human at the terminal,
  no stdin prompt wired. Entry point is Click, not HTTP. No event bus
  subscriber for confirm frames on this path.
- Live chat agent, constructed in `serve.py`. Slot:
  `_server_confirm_callback`, a REAL gate, `site=chat-agent-live`,
  `human_present=True`. Opt-out via `OPENJARVIS_CONFIRM_INTERACTIVE=0`.
  This is the executor `test-execute` drives.
---
### [ARCHIVE-W56-2026-09-13.md] 11. DIAGNOSTIC TOOLING REGISTER DELTA
Append to the W52 register. Output path verified at build time for each, per
the 09/06 rule.
- `ConfirmPolicy.__call__` - POLICY line. Sink: dispatch.log via
  `_get_dispatch_logger()`. VERIFIED READABLE at build time by
  `test_confirm_policy.py` criteria 5, 6 and 7, which read the file back by
  byte offset. Not a probe; permanent production instrumentation.
- `_server_confirm_callback` branch logging - same sink, same logger.
  Verified statically; NOT yet observed live, because the backend has not been
  restarted since W55. First restart should show `site=chat-agent-live` lines.
- `test_confirm_policy.py`, `test_confirm_policy_sites.py`,
  `test_confirm_policy_cli.py` - stdout plus exit code. Repo root.
- `classify_stub_hits.py` - stdout. Repo root. Reusable pattern: classify a
  regex hit as code or prose before acting on it.
---
### [ARCHIVE-W56-2026-09-13.md] 12. 550B CLOUD MODEL
Not used this window. No question arose that needed whole files beyond what
Gray uploaded directly, and the direct-upload path outperformed it on cost for
this shape of work. The pattern stands for questions spanning more files than
fit in a window: bundle with the question EMBEDDED AT THE TOP of the bundle
file, and ship a script that POSTs it to openrouter nemotron-3-ultra-550b
directly - Gray does not relay prompts by hand.
### [ARCHIVE-W57-2026-09-14.md] 1.1 WINDOW SUBJECT AND OUTCOME
Subject as opened: gate the two destructive mailbox tools
(`mailbox_move_to_trash`, `mailbox_empty_folder`), which the W56 brief listed
as action 3 and described as "now cheap."
Outcome: **the flags were NOT set, deliberately, on Gray's ruling.** No source
was changed. What the window produced instead is a measured account of what
actually stands between the model and a destructive mailbox action, which
turned out not to be what either of us believed at the start.
This is a window that changed nothing and produced knowledge. Per the 08/24
rule it is pinned in full.
### [ARCHIVE-W57-2026-09-14.md] 1.2 THE TWO MECHANISMS, AND WHY CONFLATING THEM COST TWO EXCHANGES
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
### [ARCHIVE-W57-2026-09-14.md] 1.3 THE INSTRUMENT AND WHAT IT MEASURED
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
### [ARCHIVE-W57-2026-09-14.md] 1.4 GRAY'S RULING - HOLD THE FLAGS
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
### [ARCHIVE-W57-2026-09-14.md] 1.5 NEGATIVE RESULTS AND DEAD THEORIES
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
### [ARCHIVE-W57-2026-09-14.md] 1.6 HAZARDS EARNED THIS WINDOW
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
### [ARCHIVE-W57-2026-09-14.md] 1.7 SDD / SDP FEED
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
### [ARCHIVE-W57-2026-09-14.md] 1.8 550B CLOUD MODEL
Not used this window. No question required whole-file bundling - Gray uploaded
`mailbox_tools.py`, `imap_mail.py`, `App.tsx`, `ChatArea.tsx`,
`useAgentEvents.ts` and `ConfirmPrompt.tsx` directly and each answered its
question on its own. Carried forward for the next window that needs it.
### [ARCHIVE-W57-2026-09-14.md] 1.9 COMMITS
- `66a11a2` confirmed present on `origin` and `gitlab`, `src/` clean. This was
  W56's commit 2, whose landing was unknown at W56 close. **W56 action 1 is
  closed.**
- **W57 produced no commits.** Two untracked scripts added to the repo root:
  `validate_gates_w57.py`, `build_archive_w57.py`. Both belong in `tools/`.
### [ARCHIVE-W57-2026-09-14.md] 1.10 DELTA - DIAGNOSTIC TOOLING REGISTER
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
### [ARCHIVE-W57-2026-09-14.md] 1.11 DELTA - EXECUTION PATH REGISTER
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
### [ARCHIVE-W57-2026-09-14.md] 2. DIAGNOSTIC TOOLING REGISTER
BASE CARRIED VERBATIM from ARCHIVE-W52-2026-09-12.md. Do not rewrite; append
dated one-line DELTAS only. Deltas from later windows follow.
Standing rules, both earned 09/06: **search the schema before building an instrument**, and
**instrumentation you cannot read is instrumentation you do not have.**
### [ARCHIVE-W57-2026-09-14.md] 6. DELTA - DIAGNOSTIC TOOLING REGISTER
CARRIED VERBATIM from ARCHIVE-W55-2026-09-13.md.
Append to the register in `ARCHIVE-W52-2026-09-12.md`. Both instruments are
COMMITTED, both write to STDOUT, both exit 0 on pass and 1 on fail, both are
fully non-interactive, and both were verified readable at the moment they were
added.
- **`test_toolkit_refusal.py`** (repo root, commit `1263279`). Stub-engine
  harness for the managed-agent toolkit bind. THE ONLY WAY THIS GUARD CAN BE
  REGRESSION-TESTED, because it is unreachable via a real model. Five criteria.
  Run: `python .\test_toolkit_refusal.py`. Touches no running backend; imports
  the module in a separate process. Creates and removes
  `w55_breach_marker.txt`.
- **`test_knowledge_sql_authorizer.py`** (repo root, commit `2fb87cf`). Ten
  criteria against `KnowledgeSQLTool` on a throwaway in-memory database.
  Never opens the real `knowledge.db`. Run:
  `python .\test_knowledge_sql_authorizer.py`.
Standing lesson reaffirmed: both were built with their output path verified at
build time, not at need.
---
### [ARCHIVE-W57-2026-09-14.md] 11. DIAGNOSTIC TOOLING REGISTER DELTA
CARRIED VERBATIM from ARCHIVE-W56-2026-09-13.md.
Append to the W52 register. Output path verified at build time for each, per
the 09/06 rule.
- `ConfirmPolicy.__call__` - POLICY line. Sink: dispatch.log via
  `_get_dispatch_logger()`. VERIFIED READABLE at build time by
  `test_confirm_policy.py` criteria 5, 6 and 7, which read the file back by
  byte offset. Not a probe; permanent production instrumentation.
- `_server_confirm_callback` branch logging - same sink, same logger.
  Verified statically; NOT yet observed live, because the backend has not been
  restarted since W55. First restart should show `site=chat-agent-live` lines.
- `test_confirm_policy.py`, `test_confirm_policy_sites.py`,
  `test_confirm_policy_cli.py` - stdout plus exit code. Repo root.
- `classify_stub_hits.py` - stdout. Repo root. Reusable pattern: classify a
  regex hit as code or prose before acting on it.
---
### [ARCHIVE-W57-2026-09-14.md] 3. LOGGING TOPOLOGY, CURRENT STATE
BASE CARRIED VERBATIM from ARCHIVE-W52-2026-09-12.md. Do not rewrite; append
dated one-line DELTAS only. Deltas from later windows follow.
Pinned 09/08 after three windows were lost to instruments that could not be read.
### [ARCHIVE-W57-2026-09-14.md] 4. EXECUTION PATH REGISTER
BASE CARRIED VERBATIM from ARCHIVE-W52-2026-09-12.md. Do not rewrite; append
dated one-line DELTAS only. Deltas from later windows follow.
Per path: entry point, call chain with file:line, which `ToolExecutor` serves it and how that
executor is constructed, whether the confirmation gate is live / auto-approved / absent, event
bus traffic, and whether a human is present.
### [ARCHIVE-W57-2026-09-14.md] 7. DELTA - EXECUTION PATH REGISTER
CARRIED VERBATIM from ARCHIVE-W55-2026-09-13.md.
Append to the register in `ARCHIVE-W52-2026-09-12.md`.
**Managed-agent SSE stream, non-DR branch** - one field changes:
- Tool availability: unchanged in shape. **The bind added in W54 is now
  VERIFIED, not merely applied.** The executed set equals
  `stream_kwargs["tools"]` and a name outside it is refused with a
  `PermissionError` before `ToolRegistry.get()`, surfacing to the model as a
  normal failed tool result and to the UI as `tool_call_end` with
  `success=false`. Evidence: section 2.3.
- Confirmation gate on this path: STILL AUTO-APPROVED
  (`confirm_callback=lambda _prompt: True`). W54 narrowed WHICH tools reach the
  executor; it did not change whether the gate runs. Unchanged by W55.
**DeepResearch path** - new field recorded:
- Toolkit is exactly four tools: knowledge_search, knowledge_sql, scan_chunks,
  think. **NONE declares `requires_confirmation`.** The
  `confirm_callback=lambda _prompt: True` at the DR construction sites is
  therefore INERT - never consulted. It becomes live the instant a confirming
  tool is added to `_build_deep_research_tools()`. Human present: yes, but not
  consulted, and there is currently nothing to consult about.
- `knowledge_sql` on this path can now read `knowledge_chunks` and nothing
  else. Prior to `2fb87cf` it could read every table in `knowledge.db`.
---
### [ARCHIVE-W57-2026-09-14.md] 10. EXECUTION PATHS DELTA
CARRIED VERBATIM from ARCHIVE-W56-2026-09-13.md.
Append to the W52 register. Per-path field added this window:
**WHAT IS IN THE CONFIRM CALLBACK SLOT, AND WHAT IT WRITES.**
- Managed-agent SSE stream, `_stream_managed_agent()` - non-DR branch. Slot:
  `ConfirmPolicy(site="managed-agent-tool", human_present=False)`. Writes
  POLICY on every gated dispatch. Executor is constructed PER TOOL CALL inside
  the loop, over a single tool instance, after the W54 toolkit bind refusal.
- Managed-agent SSE stream - `deep_research` branch, `generate_deep_research()`.
  Slot: `ConfirmPolicy(site="dr-sse-stream", human_present=False)`. RETURNS
  BEFORE the non-DR tool loop. Executor is the agent's own, wrapped by
  `_tracked_execute` for progress events.
- iMessage daemon, spawned from `bind_channel` on `channel_type == "imessage"`.
  Slot: `ConfirmPolicy(site="imessage-daemon", human_present=False)`.
- SendBlue bridge, spawned from `bind_channel` on `channel_type == "sendblue"`.
  Slot: `ConfirmPolicy(site="sendblue-bridge", human_present=False)`.
- CLI `jarvis ask -a <agent>`, `ask.py::_run_agent`. Slot:
  `ConfirmPolicy(site="cli-ask", human_present=True)`. Human at the terminal,
  no stdin prompt wired. Entry point is Click, not HTTP. No event bus
  subscriber for confirm frames on this path.
- Live chat agent, constructed in `serve.py`. Slot:
  `_server_confirm_callback`, a REAL gate, `site=chat-agent-live`,
  `human_present=True`. Opt-out via `OPENJARVIS_CONFIRM_INTERACTIVE=0`.
  This is the executor `test-execute` drives.
---
### [ARCHIVE-W57-2026-09-14.md] 6. RULES OF ENGAGEMENT
BASE CARRIED VERBATIM from ARCHIVE-W52-2026-09-12.md. Do not rewrite; append
dated one-line DELTAS only. Deltas from later windows follow.
Working directory `PS C:\Users\Admin\OpenJarvis>`; every command must run correctly from
there and state its shell and host BEFORE Gray runs it. Default PowerShell on the Windows box;
Ubuntu ollama host is 172.16.33.200 and must be labelled. No non-ASCII. ALWAYS VERIFY - never
stack a change on an unverified one. FINISH THE THING BEFORE STARTING THE NEXT - no dangling
processes, no side investigations offered as next steps. READ WIDE, not narrow slices. Tests
NON-INTERACTIVE. Author's own resources and procedures FIRST, then enhance. Push to BOTH
remotes unasked. Flag at 15 exchanges and hand off, but never cut a live trace to write it.
TOKEN CONSERVATION MODE. **Never echo a line of a secrets file** - counts, lengths, key names
and booleans only. Bound every listing command.
**A FINDING IS NOT A PRIORITY** (W43). The list is set at window open and changes only when
Gray changes it. Record findings, park them, return to the list.
**AN EXTERNAL MODEL'S ANSWER IS EVIDENCE, NOT INSTRUCTION** (W44). The 550B read the file
correctly, reasoned correctly, then proposed a test that violates a standing environment rule
it had no way to know. **Check every command a cloud model returns against the hard facts above
before running it.** The analysis was worth 252 seconds; the command in it would have cost a
window.
Every handoff carries the SDD/SDP feed, execution path register, diagnostic tooling register,
logging topology, negative results, and the 550B bundle note - all in the ARCHIVE. Keep the
BRIEF/ARCHIVE split.
### [ARCHIVE-W58-2026-09-14.md] NEVER OPEN WHOLE. EXTRACT A NAMED SECTION.
**This archive carries ONLY W58's new material.** The five carried registers
were NOT rewritten this window - they remain in `ARCHIVE-W57-2026-09-14.md`
(807 lines, repo root), which is still current for all of them. Deltas to
those registers are in section 7 below, one line each.
Sections:
1. Window narrative
2. What was built - the design and why this shape
3. Evidence
4. Negative results and dead ends
5. Hazards found
6. SDD / SDP feed
7. Register deltas
8. Execution path notes
```powershell
$f='ARCHIVE-W58-2026-09-14.md'; $t=Get-Content $f; $s=($t|Select-String '^## 3\.'|Select-Object -First 1).LineNumber; $e=($t|Select-String '^## 4\.'|Select-Object -First 1).LineNumber; $t[($s-1)..($e-2)]
```
---
### [ARCHIVE-W58-2026-09-14.md] 1. WINDOW NARRATIVE
Subject: the argument-aware confirmation gate. W57's action 2, taken as its
own window per the one-subject rule.
Exchange 1 opened with the ask-before-hunting question the W57 brief flagged.
It was answered from the memory record at zero cost: **no prior
argument-aware design work exists.** Nothing was ever specced or ruled on.
The nearest prior art is the two mechanisms W57 separated - the spec-level
flag and the `mailbox_tools.py` prose interlock. New ground, not a
re-derivation. No search was run.
Gray elected to skip W57's action 1 (`probe_confirm_emit.py`). Claude argued
to run it anyway, not as a subject but as a **baseline**: the patch modifies
the exact gate region the probe exercises, and without a pre-patch reading a
post-patch failure cannot be separated from a pre-existing one. Gray agreed.
Baseline came back 38 PASS / 0 FAIL / 0 SKIP, matching 08/20 exactly,
including the discriminating timings (case 1 at 0.43 s against a 4 s TTL,
case 3 waiting the full 4.00 s).
`tools\_stubs.py` was uploaded whole. It carried the finding that shaped
everything after: `params` - the parsed argument dict - is built at the top of
`_execute_inner`, and the boundary guard, the RBAC check and the taint scrub
all run on it BEFORE the gate. Dispatch below the gate is
`pool.submit(tool.execute, **params)` on **the same object**. So a predicate
reading `params` at the gate is gating exactly what executes. W53 is satisfied
by construction rather than by care.
A tree-wide enumeration of `requires_confirmation` consumers then turned up
the one thing that would have been missed: `agent_manager_routes.py:2315`, the
08/29 test-only route, **which was actually built** and guards on the flag
being True. That made the flag flip a four-path change, not a one-path change.
`mailbox_tools.py` was uploaded whole. It closed the design in one read:
**the predicate already existed.** `_confirmed(params)` returns True only when
`dry_run` is false AND `confirm == "CONFIRM DELETE"` - precisely the condition
under which the tool applies. It handles the string/bool coercion. The
argument-aware gate was therefore not a new mechanism to invent but an
existing one to route.
Claude raised the scope-in-the-prompt problem (section 5) and asked for a
ruling. Gray: "I need it to function. We can make improvements later." Ruling
taken; the emit payload was left untouched at 38/38.
Patch script produced, dry run clean on all eight anchors, applied, verified.
New probe produced, 50 PASS / 0 FAIL. Baseline probe re-run, still 38 / 0 / 0.
Handoff at Gray's call at 93 percent usage.
---
### [ARCHIVE-W58-2026-09-14.md] 2. WHAT WAS BUILT - THE DESIGN AND WHY THIS SHAPE
Three ideas, eight anchored edits, two files.
**(a) `BaseTool.needs_confirmation(params) -> bool`, default True.**
A concrete method on the ABC, not abstract. Default True is the whole safety
argument: a tool that does not override it behaves exactly as it did before
the hook existed. `shell_exec`, `git_commit` and `agent_kill` are bit-for-bit
unchanged, and that is asserted by the regression block of the probe rather
than assumed.
**(b) The gate reads BOTH.**
`requires_confirmation` stays the ELIGIBILITY switch; the predicate is the
PER-CALL refinement. Both must be true.
**THE REJECTED ALTERNATIVE, recorded so it is not revisited:** replacing the
spec flag with a predicate, leaving the mailbox flags False and gating them
from elsewhere. That was rejected because the flag is read by consumers
OUTSIDE the executor - `validate_gates_w57.py` reads it by `ast`, and the
test-execute route at 2315 guards on it. A tool gated by a hidden predicate
while its spec still says False would make **the spec lie about the tool** -
W47 turned against us. Keeping the flag truthful is what lets the existing
validator and the existing test route keep working unchanged.
**(c) The two destructive tools override with `_confirmed(params)`.**
The same function the tools already use to decide whether to apply. The human
gate and the tool's own interlock now test the identical condition, which is
the strongest available form of "what is consented to is what executes."
**Plus two things that were not strictly required and were done anyway:**
- **`GATEPRED` logging.** When the predicate narrows a gate-eligible call down
  to no-gate, the executor writes `decision=NARROWED_NO_GATE` with the args
  digest to `dispatch.log`. Without it, an ungated destructive call would look
  byte-identical to a call that was never eligible - exactly the W56 failure.
  A raising predicate writes `decision=FAIL_CLOSED`. Readability was verified
  at the moment the instrument was added, per the 09/06 rule, by having the
  probe itself read the file back and assert the lines landed.
- **The SAFETY NOTE docstring was rewritten** (edits G and H). It said the
  flag "is NOT set, and why". After the patch the flag IS set. Leaving it
  would have planted a register that disagrees with the code in the one place
  a future window is most likely to read. The historical reasoning is kept
  above a dated W58 status block.
---
### [ARCHIVE-W58-2026-09-14.md] 3. EVIDENCE
**Baseline before touching anything** - `probe_confirm_emit.py`, 38 PASS /
0 FAIL / 0 SKIP. Case 1 approved in 0.43 s against a 4 s TTL; case 3 waited
the full 4.00 s. The timings are the load-bearing part, not the passes.
**Dry run** - all eight anchors `count=1`. Both files CRLF-major and the
script adapted. `_stubs.py` 25,476 -> 27,242 B predicted, +37 lines, **crlf
delta +37 equal to the line delta** (no mixed-EOL damage), nonascii +0.
`mailbox_tools.py` 34,439 -> 36,146 B, +37 lines, crlf +37, nonascii +0.
`ast.parse` OK on the PROPOSED text before any write was possible.
**Apply** - on-disk 27,242 and 36,146, both MATCH predicted. Marker count 2
and 5. `ast.parse` OK on what actually landed, re-read from disk. Six controls
survived: confirm-emit marker, `ConfirmPolicy`, the dispatch ATTEMPT format,
`CONFIRM_TOKEN`, `_confirmed`, the protected-senders block.
**`probe_argaware_gate.py` - 50 PASS / 0 FAIL.** No backend, no restart, no
network, no mail touched. Safety design: every executor case passes
`account="__nonexistent_probe_account__"` so the tool returns its no-account
result before any IMAP connection, and the one case that reaches the gate is
resolved **DENIED**, so the tool body never runs. Per the 08/29 first-run-
denies ruling, applied to the probe as well.
- Predicate table, 16 cases across both tools, all correct: no args, explicit
  dry run, apply-without-token, apply-with-wrong-token, correct token, string
  `"false"` coerced, string `"0"` coerced, and token-but-still-dry-run.
- Case 1 dry run: **0 confirm events, 0.00 s**, reached the tool body.
- Case 2 `dry_run` omitted: 0 events, 0.00 s.
- Case 3 apply without the token: 0 events, 0.00 s.
- Case 4 real apply: exactly 1 event, all seven payload fields intact,
  turn_id carried, **blocked 0.33 s against a 6 s TTL** - the upper bound is
  what discriminates "released by resolve" from "timed out and looked right."
  Result content says denied by user, success False.
- Case 5 `empty_folder` real apply: 1 event, 0.32 s, denied.
- Regression: flag True with NO override still gates, 1 event, 0.33 s.
- Fail closed: a predicate that raises still gates, dispatch did not crash.
- Instrument readability: 3 `NARROWED_NO_GATE` lines, 1 `FAIL_CLOSED` line,
  18 hits on the probe turn id, all read back out of `dispatch.log`.
**Regression control after the patch** - `probe_confirm_emit.py` re-run:
still 38 / 0 / 0. The default-True path is unchanged.
---
### [ARCHIVE-W58-2026-09-14.md] 4. NEGATIVE RESULTS AND DEAD ENDS
- **NO PRIOR ARGUMENT-AWARE DESIGN WORK EXISTS.** Established from the record,
  not by searching the tree. A future window must not go hunting for one.
- **"Make the gate argument-aware" did NOT mean giving the gate access to
  arguments.** The gate already had them - `_args_digest(tool_call.arguments)`
  is computed a few lines below it by the confirm-emit patch, and `params` is
  in scope. What was missing was a per-tool predicate to consume them. The
  change is far smaller than the name suggests.
- **The predicate did not need to be written.** `_confirmed` already existed
  and is exactly right. Two windows of design work were avoided by reading the
  file before designing. Same family as the 09/06 search-the-schema lesson.
- **The obvious design - replace the flag - is wrong.** See section 2. It
  breaks `validate_gates_w57.py` and the test-execute route and makes the spec
  lie. Do not revive it.
- **W57's "hold the flags" ruling was not overturned.** His stated objection
  was cost (two clicks, two 120 s TTLs per deletion), not principle. The
  narrowing removes the cost, so the ruling is satisfied. A future window must
  not read the flip as having gone against him.
---
### [ARCHIVE-W58-2026-09-14.md] 5. HAZARDS FOUND
- **THE GATE FIRES BEFORE `from_addr` IS RESOLVED INTO UIDS AND BEFORE THE
  PROTECTED-SENDERS FILTER RUNS.** On a `from_addr` call, Approve consents to
  a sender substring, not a count. The dry-run plan shown beforehand carries
  the count; the gate prompt does not. **W53 risk that survives this window.**
- **`_args_digest` CAPS AT 400 CHARS.** A long uid list reaches the prompt as
  `...TRUNC` - approving a scope that cannot be seen. Same family as above.
  Both are the improvement Gray deferred, and both need the emit payload
  touched, which is currently proven at 38/38.
- **`cli\ask.py:356` IS STILL A BARE `lambda prompt: True`** with no
  `ConfirmPolicy` wrapper. After the flag flip it is a path that will silently
  auto-approve a real mailbox deletion with no POLICY line. Not chased.
- **The four `ConfirmPolicy` sites** (`agent_manager_routes.py` 721 / 1206 /
  1563 / 1640) now auto-approve the mailbox tools too - but WITH attribution.
  Same execution, now recorded. Strictly better than before, not a regression.
- **`_stubs.py` IS CRLF-MAJOR (663 of 664) AND HAS ZERO NON-ASCII BYTES.**
  Both carried notes on this file were stale - it was recorded as LF-with-two-
  stray-CRLF and as carrying an em-dash needing an encoding control. Neither
  is true now. A non-ASCII BYTE COUNT is the durable control; it works without
  knowing which glyph to look for.
- **The gate moved from `_stubs.py:265` to `:390`** when the outcome wrapper
  was added. Anchor on text.
---
### [ARCHIVE-W58-2026-09-14.md] 6. SDD / SDP FEED
**The guard, in plain language (the 09/02 requirement).** There are two locks
on the mailbox door. The first lock is a password the ASSISTANT has to type -
it must say `dry_run=false` and the exact words `CONFIRM DELETE`. The
assistant can type that itself, so that lock keeps it from deleting by
accident, but it does not ask a person anything. The second lock is a button
that appears on Gray's screen, and only a person can press it. Until this
window the mailbox door had only the first lock. Now it has both - and the
second lock is smart enough to stay out of the way when the assistant is only
LOOKING at the mail. It appears only when something is about to actually move.
**Architecture decision to record:** eligibility and per-call refinement are
deliberately separate. The spec flag is declarative, greppable and readable by
`ast` from outside the process - which is what lets an external validator and
a test route reason about the gate without running it. The predicate is
imperative and argument-aware. Collapsing them into one mechanism would have
cost the external readability.
**Evidence standard applied, worth carrying:** every timing assertion in the
new probe carries an UPPER bound as well as a lower one. `elapsed > 0.25`
proves it blocked; `elapsed < 3.0` against a 6 s TTL proves it was released by
`resolve()` rather than by expiry. A check is worth only what it can
discriminate.
**Open SDP item:** the confirmation prompt does not name the scope of what it
is approving. Section 5.
---
### [ARCHIVE-W58-2026-09-14.md] 7. REGISTER DELTAS
Append these to the W57 archive's registers; do not rewrite those sections.
- **DIAGNOSTIC TOOLING +2:** `patch_argaware_gate.py` (repo root, applies the
  eight edits, dry-run prints byte/line/CRLF/non-ASCII counts and anchor
  counts, `ast.parse`s before writing, verifies on-disk size and six controls
  after). `probe_argaware_gate.py` (repo root, 50 assertions, in-process, no
  backend, no network, cannot touch a mailbox).
- **DIAGNOSTIC TOOLING +1 instrument:** `GATEPRED` lines in `dispatch.log` -
  `decision=NARROWED_NO_GATE` and `decision=FAIL_CLOSED`, both verified
  readable at build time.
- **LOGGING TOPOLOGY:** no new logger. `GATEPRED` rides the EXISTING
  `openjarvis.dispatch` logger via `_get_dispatch_logger()`, landing in
  `%LOCALAPPDATA%\OpenJarvis\logs\dispatch.log`. Nothing new to map.
- **EXECUTION PATHS:** no new path. The gate site inside
  `ToolExecutor._execute_inner` is shared by every path already in the
  register; the flag flip changes WHICH TOOLS reach it on four of them.
- **PROGRAM GOAL:** first code movement in three windows. See section 8.
---
### [ARCHIVE-W58-2026-09-14.md] 8. EXECUTION PATH NOTES - WHICH PATHS THE FLIP LANDS ON
1. **Chat path** (`routes.py` -> `app.state.agent` -> agent's own executor).
   Gate goes live on both mailbox tools. Intended. UNPROVEN LIVE - the backend
   has not been restarted.
2. **Test-execute route**, `agent_manager_routes.py:2315`. Guards on
   `requires_confirmation` being True, so the two tools are now eligible
   there. This is a GAIN: it is the deterministic, loopback-guarded,
   model-free way to exercise the gate against the real destructive tools
   without asking qwen3-coder to cooperate. Best candidate for the live proof
   if the chat-path test is inconclusive.
3. **Four `ConfirmPolicy` sites.** Auto-approve with attribution.
4. **`cli\ask.py:356`.** Bare auto-approve, no attribution. Section 5.
**Toward the program goal.** The destructive mailbox tools now have a human
gate that fires on destruction and stays silent on inspection, and the
protection Gray believed he had - model compliance with an instruction string
- is now backed by a button only a person can press. Proven in isolation at
50/0. **Not yet proven live.** That is action 1 of W59, and until it runs the
honest statement is that the gate exists on disk, not that it protects him.
### [ARCHIVE-W59-2026-09-14.md] (preamble)
# ARCHIVE W59 - 2026-09-14
NEW MATERIAL AND DELTAS ONLY. The five carried registers - diagnostic
tooling, logging topology, execution paths, program goal, rules of
engagement - remain in `ARCHIVE-W57-2026-09-14.md` and were NOT rewritten.
Extract a named section from W57; append the W59 deltas in section 7 below.
NEVER OPEN THIS FILE WHOLE. Extract a named section.
### [ARCHIVE-W59-2026-09-14.md] SECTION INDEX
1. Window summary
2. The double-confirmation investigation (NEGATIVE RESULT)
3. The prose ask - source, fix, and the overshoot that was avoided
4. The mojibake and BOM analysis
5. Hazards found
6. SDD / SDP feed
7. Register deltas
8. Commits and artifacts
---
### [ARCHIVE-W59-2026-09-14.md] 1. WINDOW SUMMARY
W59 opened on the W58 brief with one instruction: measure the
double-confirmation defect before patching it. That measurement closed the
defect as a non-defect within one exchange, and the window then executed the
rest of the W58 action list to completion.
Everything on that list is now done and pushed. Three commits, all on both
remotes. The exe was rebuilt and relaunched; the backend was restarted.
Two things were fixed that the W58 brief had listed as separate deferred
items - the ConfirmPrompt move (an eighth carry) and the mojibake audit -
and they were done in one patch and one build because both lived in
`ChatArea.tsx`. That is the only reason they were combined.
The window's real product is not the code. It is the closure of a
misdiagnosis: a log pattern that looked exactly like a broken gate turned out
to be a correctly-firing gate in front of an empty chair.
---
### [ARCHIVE-W59-2026-09-14.md] What was suspected
The W58 brief recorded the symptom: after Gray clicked Approve, the model
asked him again in prose to confirm with "CONFIRM DELETE", and a banner
reading `The confirmation request expired before it was answered.` appeared.
The brief named a leading candidate - the `instruction` string returned by
`_needs_confirmation_result` telling the model to ask the user - and named
the discriminator: two ATTEMPT lines with DIFFERENT args digests would mean
two separate tool calls with the prose ask between them.
The brief also named a second candidate: a per-sender loop, with the gate
firing once per sender, correctly, and reading as a repeat.
### [ARCHIVE-W59-2026-09-14.md] What was measured
`dispatch.log`, 58 `move_to_trash` lines, 28 ATTEMPT. The relevant turn is
`48be7cd6`, and it is at **10:20-10:27, not the 13:02 the brief recorded**.
It was identified by its sender set matching the screenshot.
Three ATTEMPT lines, every one carrying `"confirm": "CONFIRM DELETE"` on its
first and only try:
| line | sender | result | latency |
|------|--------|--------|---------|
| t1 | notifications@github.com | `reason=OK` | 139.558 s |
| t2 | capitalone@notification.capitalone.com | `GATE_TIMEOUT` | 120.005 s |
| t3 | capitalone@notification.capitalone.com | `GATE_TIMEOUT` | 120.017 s |
t3 is the agent's known re-request after a timeout, with byte-identical args.
### [ARCHIVE-W59-2026-09-14.md] The finding
**The second candidate was correct and the first was wrong.** The gate fired
once per sender. That is the designed behavior: capitalone is a different
deletion than github and deserves its own consent.
The instruction-text theory required a no-token ATTEMPT followed by a
token-bearing one. No such pair exists anywhere in the log. The model
supplied the token itself on every call, because it had already run its dry
runs ninety minutes earlier in a separate turn (`3f4b2aff`, 08:53, five
senders, all `dry_run: true`).
### [ARCHIVE-W59-2026-09-14.md] Why the gates went unanswered
Gray stated it directly: he had to leave after the first approval. t2 and t3
are not a rendering failure, not a bus failure, and not a registry failure.
They are a correctly-fired gate in front of nobody. The two timeouts account
for 240 s of the turn's 402.5 s.
**This is the W59 lesson: AN EMPTY CHAIR LOOKS EXACTLY LIKE A BROKEN GATE IN
THE LOG.** `GATE_TIMEOUT` is indistinguishable, from the log alone, between
"the prompt never reached the human" and "the human was not there". Any
future investigation of a gate timeout must establish human presence FIRST,
because it is free to establish and it eliminates the entire class.
### [ARCHIVE-W59-2026-09-14.md] It is real, it is just not what it was thought to be
The screenshot confirms the model wrote, in chat: a request to confirm with
"CONFIRM DELETE", followed by a statement that it would then proceed with the
remaining senders. So the model IS asking in prose, redundantly, alongside a
gate that asks with buttons. It simply was not generating a second tool call.
### [ARCHIVE-W59-2026-09-14.md] Source, found by reading the whole file
Three strings in `mailbox_tools.py`, all written before the gate existed:
1. `_needs_confirmation_result` -> `instruction`: "Nothing was changed. Show
   this plan to the user and ask them to approve it. Only if they explicitly
   approve, call this tool again with dry_run=false and confirm set to the
   exact string above."
2. `MailboxMoveToTrashTool.spec.description`: "Never pass those without the
   user's explicit approval of a dry-run plan you have already shown them."
3. `MailboxEmptyFolderTool.spec.description`: the same sentence.
The dry runs at 08:53 returned string 1. The model carried that instruction
forward into the 10:20 turn.
### [ARCHIVE-W59-2026-09-14.md] The overshoot that was avoided
The obvious fix is to delete the ask. That would have been a regression.
The gate prompt renders an args digest, not counts, and the digest caps at
400 chars. If the model stopped narrating the dry-run plan, the ONLY thing
the human would ever see before approving is a truncated argument blob. The
count - the single most decision-relevant fact about a bulk mailbox move -
would vanish from the interaction entirely.
So the fix separates the two jobs the old text conflated: REPORTING the plan
(which the model must keep doing, with counts) and REQUESTING approval (which
now belongs solely to the gate). The rewritten strings instruct the model to
report the counts, then re-call with the token, and explicitly not to ask for
a typed phrase or wait for a chat reply.
This is a direct application of W53: consent is only consent if the thing
consented to is the thing that executes. A typed phrase in chat is consent to
a described plan; a button click on the gate is consent to the actual
arguments about to run. Keeping both meant two consents of unequal quality.
Now there is one, and it is the good one.
### [ARCHIVE-W59-2026-09-14.md] Verification
Byte-level patcher, CRLF-aware, exactly-once anchors. 36,146 -> 36,782 B,
871 -> 880 CRLF, non-ASCII 0 before and after. Marker
`openjarvis-prose-ask-v1` present 3 times, `explicit approval` absent.
`ast.parse` OK - the meaningful control, since the anchors splice into
multi-line string concatenations inside spec bodies where a bad join is a
syntax error rather than a behavior change.
### [ARCHIVE-W59-2026-09-14.md] A BAD CONTROL, RECORDED
One verify line in the patcher counted `ask "` followed by a newline and
reported 1 where it expected 0. That match is in the module docstring,
discussing the model-satisfied interlock - unrelated text. The control was
mis-specified, not the patch. It is recorded here rather than quietly
dropped, because a control that reports a false positive is as much a defect
in the instrument as one that reports a false negative. The valid controls
were marker count and `explicit approval` count.
---
### [ARCHIVE-W59-2026-09-14.md] The measurement that mattered
A byte-level dump of `ChatArea.tsx` printed every non-ASCII byte with 35
characters of context on each side. 17 bytes total. This is the instrument
that settled everything else in this section, and it took one command.
### [ARCHIVE-W59-2026-09-14.md] The BOM finding
`ChatArea.tsx` carries a UTF-8 BOM (`EF BB BF`) at offset 0. That accounts
for 3 of its 17 non-ASCII bytes and is not mojibake.
`App.tsx` also reports 3 non-ASCII bytes but has NO BOM. Its 3 bytes are an
em dash inside the commented-out desktop auto-update block - a code comment,
never rendered. The patcher's output labeled both as "expect 3 BOM", which
was right by number and wrong by reason for `App.tsx`. Corrected here.
Neither should be touched. The practical consequence: **a non-ASCII byte
count of zero is not the right success control for these files.** The control
is the delta - 17 to 3 - not the absolute.
---

