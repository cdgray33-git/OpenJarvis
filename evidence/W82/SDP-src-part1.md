# SDP SOURCE EXTRACT W82 part 1 (deduplicated by section hash)
### [ARCHIVE-W42-2026-09-09.md] 1. WHAT WAS DONE - NARRATIVE
**Exchange 1 - the two decisions.** W41 closed blocked on section 5 and had asked twice
without an answer. W42 opened by loading the handoff and putting both decisions to Gray as a
single tap-to-answer prompt rather than prose. Both landed in one exchange.
- **5.1 fix shape: ENV OVERRIDE inside the author's `setup_logging`.** Gray took the
  recommended option. This preserves ONE configuration authority over the `openjarvis` tree
  and satisfies the standing USE THE AUTHOR'S RESOURCES FIRST order.
- **5.2 budget: 40 MB TOTAL across all files.** With `backupCount=3` that is 4 files, so
  `maxBytes = 10 * 1024 * 1024`.
**Exchange 2 - one anchor read.** A single command pulled all three edit sites: `log_config.py`
in full (86 lines), `serve.py` L50-80, and `start-openjarvis.ps1` L20-40. Built per the READ
WIDE rule. It was sufficient; no follow-up read was needed to write the patch.
**Exchange 3 - the patch, dry run.** `patch-loglevel-v2.ps1`, hash-anchored, dry run by
default. FAILED on a Claude-authored off-by-one in the launcher anchors (hazard 5.1). Gray
offered to send file content; that was not needed - the numbering was visible in the prior
read.
**Exchange 4 - anchor correction in place.** A one-line PowerShell string-replace fixed the
three launcher line numbers inside the patch script without re-downloading it. All anchors
then passed.
**Exchange 5 - apply.** Clean. Backups made, canary intact, BOM preserved, `py_compile` OK.
**Exchange 6 - restart and verify.** Gray restarted and exercised the server. The verification
instrument was non-interactive and ran to completion per his standing rule. RESULT POSITIVE
on the primary criterion. See section 3.
**Exchange 7 - the 550B handoff attempt.** Gray called for the `:552` question to go to the
550B rather than burn window tokens. The bundle command and the model prompt were written.
**The 550B never answered.** See section 6.
---
### [ARCHIVE-W42-2026-09-09.md] 2. THE PATCH AS APPLIED
Script: `C:\Users\Admin\OpenJarvis\patch-loglevel-v2.ps1` (in repo root, currently UNTRACKED).
Applied 2026-09-09 12:30:56. Dry run by default, `-Apply` to write.
**Execution policy hazard, carried forward:** the box refuses unsigned scripts. `.\script.ps1`
throws `PSSecurityException / UnauthorizedAccess`. The working invocation is a bypassed child
process:
```powershell
powershell -ExecutionPolicy Bypass -File 'C:\Users\Admin\OpenJarvis\patch-loglevel-v2.ps1'
```
**Use that form for every future patch script.** This is not a per-script problem, it is the
machine's policy.
### [ARCHIVE-W42-2026-09-09.md] 2.1 Edit 1 - `src\openjarvis\cli\log_config.py` L5
Added `import os` after `import logging`.
### [ARCHIVE-W42-2026-09-09.md] 2.2 Edit 2 - `src\openjarvis\cli\log_config.py` L50-55, the level ladder
Was:
```python
    if quiet:
        level = logging.ERROR
    elif verbose:
        level = logging.DEBUG
    else:
        level = logging.WARNING
```
Now:
```python
    _env_level = logging.getLevelName(
        os.environ.get("OPENJARVIS_LOG_LEVEL", "WARNING").strip().upper()
    )
    if not isinstance(_env_level, int):
        _env_level = logging.WARNING
    if quiet:
        level = logging.ERROR
    elif verbose:
        level = logging.DEBUG
    else:
        level = _env_level
```
**DIVERGENCE FROM W41 SECTION 5.1, STATED AND ACCEPTED.** W41 specified the env check
"ahead of the quiet/verbose ladder." As written it is in the `else` branch instead, so
explicit `--quiet` and `--verbose` flags still win over the environment. On the serve path
neither flag is passed, so runtime behavior is identical to what 5.1 specified. The default
with the variable unset is unchanged at WARNING. `logging.getLevelName` on an unknown string
returns a string rather than an int, which the `isinstance` check catches, so a typo in the
variable degrades to WARNING rather than throwing.
### [ARCHIVE-W42-2026-09-09.md] 2.3 Edit 3 - `src\openjarvis\cli\serve.py` L61, rotation budget
`maxBytes=4 * 1024 * 1024` became `maxBytes=10 * 1024 * 1024`. With `backupCount=3` that is
`backend.log` plus three rotations at 10 MB each = 40 MB TOTAL, per decision 5.2.
### [ARCHIVE-W42-2026-09-09.md] 2.4 Edit 4 - `src\openjarvis\cli\serve.py` L63-65, the formatter swap
Was a plain `logging.Formatter`. Now:
```python
    from openjarvis.cli.log_config import SanitizingFormatter
    file_handler.setFormatter(
        SanitizingFormatter("%(asctime)s %(levelname)s %(name)s: %(message)s")
    )
```
Local import rather than a top-of-file import, deliberately: it keeps the whole change inside
the hash-anchored block and avoids touching an import section that was not read. No circular
import risk - `log_config` imports only from `openjarvis.security`. `py_compile` passed and
the server started, so the import resolves.
This is the W41 6.4 security fix. **It is applied but NOT proven - see 4.2.**
### [ARCHIVE-W42-2026-09-09.md] 2.5 Edit 5 - `start-openjarvis.ps1`, before the launch line
```powershell
# Route the openjarvis logger tree at INFO (see log_config.setup_logging)
$env:OPENJARVIS_LOG_LEVEL = "INFO"
```
The launcher is now 33 lines. The env var is process-scoped to the launched server.
**Consequence worth knowing: starting the server by any means OTHER than
`start-openjarvis.ps1` will run at WARNING and the tree goes dark again.** That is the dial
working as designed, but it is a trap for a future window that starts the server by hand.
### [ARCHIVE-W42-2026-09-09.md] 2.6 Patch harness properties, confirmed working
Worth reusing verbatim. The harness did all of the following and all of it held:
- exact-string anchor assertion on every line it touches, aborting before any write on
  mismatch, printing expected vs actual;
- per-file BOM detection and restoration (`serve.py` is BOM=True, `log_config.py` and the
  launcher are BOM=False);
- per-file newline detection so line endings are not normalized;
- `:552` canary SHA-256 captured before the write and re-checked after, with the line index
  shifted to account for inserted lines;
- timestamped `.bak` for each file;
- `py_compile` on both Python modules;
- rollback commands printed at the end.
---
### [ARCHIVE-W42-2026-09-09.md] 3. RUNTIME VERIFICATION - THE POSITIVE RESULT
Restart at 12:33. Verification instrument, non-interactive, second PowerShell window:
```powershell
$l="$env:LOCALAPPDATA\OpenJarvis\logs\backend.log"; "SIZE: {0} KB" -f ([math]::Round((Get-Item $l).Length/1KB,1)); "--- DEBUG LINES (expect 4) ---"; (Select-String -Path $l -Pattern '\[DEBUG\]').Count; "--- openjarvis.* INFO or DEBUG (expect >0) ---"; (Select-String -Path $l -Pattern 'openjarvis\.(server|cli)').Count; "--- LAST 25 openjarvis LINES ---"; Select-String -Path $l -Pattern 'openjarvis\.' | Select-Object -Last 25 | ForEach-Object { $_.Line }
```
### [ARCHIVE-W42-2026-09-09.md] 3.2 The substantive finding inside the DEBUG output
This is the payload the four windows of logging work were for, and it is worth reading
carefully:
- `registry_keys` holds **41 tools**.
- `tools_loaded` holds **12 tool classes**.
- `allowed` holds **12 tool names**, matching `tools_loaded`.
The three mailbox mutation tools relevant to Defect 1 and Defect 6 - `mailbox_move_to_trash`,
`mailbox_empty_folder`, `mailbox_find_messages` - **are present in all three sets on the
serve path at startup.** So on this path they are registered, loaded, and allowed. Any Defect
1 theory that depends on the tool being absent from the registry at startup is not supported
by this evidence. **That does not close anything** - Defect 1's failures were never localized
to startup registration, and W41's engine-layer localization stands. But the register is now
observable, which it was not before.
The gap between 41 registered and 12 loaded is unexplained and was NOT investigated. It may
be entirely by design (config-gated tools). **Do not chase it mid-task; record it.**
### [ARCHIVE-W42-2026-09-09.md] 4.2 The canary is much bigger than W41 recorded
W41 6.3 estimated the damaged literal at "roughly TEN KILOBYTES." The measured length is
**49,789 characters.** That is a factor of five larger. It does not change the conclusion -
it is still a compounding cp1252/UTF-8 re-encoding artifact, still stable, still a canary -
but any SDD text quoting 10 KB should be corrected to 49,789 characters, measured 09/09.
**Practical consequence: never print that line raw into a chat window.** Any command that
reads around it must truncate. The form that works:
```powershell
$s='C:\Users\Admin\OpenJarvis\src\openjarvis\cli\serve.py'; $a=Get-Content $s; 530..576 | ForEach-Object { $t=$a[$_-1]; if($t.Length -gt 200){$t=$t.Substring(0,200)+" ...[TRUNCATED "+$a[$_-1].Length+" chars]"}; "L{0}: {1}" -f $_,$t }
```
### [ARCHIVE-W42-2026-09-09.md] 5.1 Claude-authored off-by-one on the launcher anchors - FOURTH command defect in three windows
The anchor read printed `# Start server` at L29; the patch asserted it at L30. The patch
aborted correctly and wrote nothing, which is the harness working as intended. But this is
the fourth Claude-authored command defect in three windows (W40 4.4, W41 6.1, and this).
**Standing correction from here: when a patch script asserts line numbers, derive them
mechanically from the read output rather than by counting in prose.** The read output already
carries `L29:` prefixes. Transcribing them by eye is the failure mode.
The recovery was cheap and is worth reusing - patch the patch in place rather than
regenerating and re-downloading it:
```powershell
$p='...\patch-x.ps1'; $t=[IO.File]::ReadAllText($p); $t=$t.Replace('old','new'); [IO.File]::WriteAllText($p,$t)
```
### [ARCHIVE-W42-2026-09-09.md] 5.2 Unsigned scripts are blocked by execution policy
See 2. `powershell -ExecutionPolicy Bypass -File '<absolute path>'` is the required form.
A `.\script.ps1` invocation will always fail on this box. Carry this in every handoff.
### [ARCHIVE-W42-2026-09-09.md] 5.3 The env var is a single point of darkness
Covered in 2.5. Anything that starts the server without `start-openjarvis.ps1` loses INFO.
A future window should consider whether the default in `log_config.py` should become INFO
outright, but **that is a decision for Gray, not a drive-by change.**
---
### [ARCHIVE-W42-2026-09-09.md] 7. NEGATIVE RESULTS - WHAT THIS WAS NOT
Recorded so no future window re-tests them.
- **The level gate was NOT the reason `serve.py:552` is invisible.** The gate is open and
  proven open by four other lines in the same file and the same logger. `:552` is guarded by
  something in the code path. New question, different shape.
- **Gate 3 and gate 4 were NOT in play for the server surface.** `openjarvis.server.*` and
  `openjarvis.cli.serve` propagate normally to root. Confirmed by observation, not inference.
- **The `SanitizingFormatter` local import is NOT a circular import.** The server started and
  `py_compile` passed.
- **The patch harness did NOT damage encoding.** `:552` hash identical before and after;
  `serve.py` BOM preserved. W40's harness design is validated for reuse.
- **The mailbox mutation tools are NOT missing from the startup registry.** All three appear
  in `registry_keys`, `tools_loaded`, and `allowed`.
- **The cloud outage is NOT established as caused by this window's changes.** See 6. It is
  an open question with the change record arguing against Gray's hypothesis.
---
### [ARCHIVE-W42-2026-09-09.md] 8. NEXT ACTIONS, IN ORDER
1. **COMMIT AND PUSH TO BOTH REMOTES.** Three windows overdue. There is now verified,
   working, uncommitted code sitting on disk and that is the largest unmanaged risk in the
   project right now. Stage explicit paths, never `git add -A`. `origin` is GitHub, `gitlab`
   is the lab instance. Files: `src\openjarvis\cli\log_config.py`,
   `src\openjarvis\cli\serve.py`, `start-openjarvis.ps1`, `patch-loglevel-v2.ps1`, and the
   W40 leftovers (`patch-debugreadable-v1b.ps1`).
2. **Run the cloud discriminating test** (section 6). One command. It either restores the
   550B tactic or tells us where the fault actually is.
3. **Resolve `serve.py:554`** (section 4.1) - via the 550B bundle if 2 restores it, otherwise
   via one wide truncating read in-window.
4. **Resolve `openjarvis.retry400`** - the gate-4 suspicion from W41 4.2, still untouched.
   `engine\ollama.py` L380-500. May invalidate a prior Defect 1 conclusion.
5. **Confirm rotation** when `backend.log` first crosses 10 MB (section 4.3).
6. **Return to Defect 1 / Defect 6 with the newly visible server surface.** This is the
   actual point of the last four windows: `routes.py`, `stream_bridge.py` and
   `agent_manager_routes.py` now emit into `backend.log`.
7. **Deferred, do not start mid-task:** the `:554` ASCII replacement; the 41-vs-12 tool
   registry gap (3.2); the three separate-entry-point `basicConfig` sites; whether the
   `log_config.py` default should become INFO.
---
### [ARCHIVE-W42-2026-09-09.md] 9. STANDING RULES CHECK
- **ALWAYS VERIFY, never stack on unverified** - HELD, and it paid. One patch, verified at
  runtime before anything else was proposed. The unmet criterion (`:552`) was reported as
  unmet rather than glossed.
- **FINISH THE THING BEFORE STARTING THE NEXT** - HELD. The `retry400` gate-4 read was
  explicitly deferred at the start of the window rather than bundled into the patch.
- **Shell and host on every command** - HELD.
- **No non-ASCII symbols** - HELD.
- **Working directory `PS C:\Users\Admin\OpenJarvis>`** - HELD. Download location was stated
  before the move command, and the move-and-run was given as one line.
- **READ WIDE, NOT IN NARROW SLICES** - HELD. One read covered all three edit sites.
- **Design tests to be non-interactive** - HELD. The verification instrument ran to
  completion in a second window with no reaction-time dependency.
- **TOKEN CONSERVATION MODE** - attempted, see section 10.
- **15-exchange flag** - not reached; window ran 7 exchanges.
- **USE THE AUTHOR'S RESOURCES FIRST** - HELD and decisive. The fix lives inside the author's
  `setup_logging` and uses the author's `SanitizingFormatter`. No third configuration
  authority was created.
- **PUSH TO BOTH REMOTES** - **STILL NOT DONE. NOW THREE WINDOWS OVERDUE.** Promoted to next
  action 1.
- **550B for whole-file work** - attempted and BLOCKED by the outage (section 6).
---
### [ARCHIVE-W42-2026-09-09.md] 10.2 What worked this window
Seven exchanges took the project from "patch blocked on two decisions" to "applied and
runtime-verified," including a failed anchor and its recovery. The things that made that
possible:
- decisions gathered in ONE prompt rather than a discussion;
- ONE wide read serving all three edit sites;
- the patch delivered as a downloadable file, not pasted into chat;
- the anchor failure repaired in place rather than by regenerating the script;
- verification as a single non-interactive command producing counts, not dumps.
### [ARCHIVE-W42-2026-09-09.md] 10.3 The structural answer, for Gray's decision
**Claude Code** is Anthropic's agentic coding tool that runs in the terminal on the machine
itself. <cite index="8-1">It maintains awareness of the whole project structure, can directly edit files,
run commands, and create commits, and supports MCP for external data sources.</cite> <cite index="8-1">Prerequisites are
Node.js 18 or newer and a Claude.ai or Anthropic Console account.</cite>
Relevance to this specific project: the paste-the-output loop is the dominant cost driver
here, and it exists only because the assistant cannot see the filesystem. In Claude Code the
model reads `serve.py` itself, runs the verification command itself, and reads the result -
none of which enters a chat transcript that gets re-sent every turn. **Whether the plan cost
works out better for Gray is a separate question that should be checked at
https://support.claude.com rather than assumed.** Docs: https://docs.claude.com/en/docs/claude-code/overview
This is offered as information, not a recommendation to switch mid-thread.
---
### [ARCHIVE-W42-2026-09-09.md] 11. EXECUTION PATHS - CARRIED, WITH ONE UPDATE
The startup path traced in W40 and confirmed in W41 is unchanged, with the launcher addition:
`start-openjarvis.ps1` sets `OPENJARVIS_LOG_LEVEL=INFO` (NEW, line 31-32), then runs
`python -m openjarvis.cli serve --port 8010`, entering the click group at
`cli\__init__.py:55` which calls `setup_logging` at `:62` (**this is now where the env var is
consumed**), then dispatches to `serve()` registered at `:86`, which calls
`_configure_file_logging()` at `serve.py:109` and finally `uvicorn.Config(...)` at
`serve.py:653` (shifted by 2). Human present: yes, manual start from the admin session.
**NEW observable data on this path, from 3.2:** at startup the tool registry holds 41 keys,
12 tool classes load, and 12 are allowed. This is now visible on every start.
The two paths in the standing register - the orchestrator `ask()` path via
`system\orchestrator.py`, and the managed-agent SSE stream via `_stream_managed_agent()` in
`server\agent_manager_routes.py` - are UNCHANGED, but **`agent_manager_routes.py` logs are
now readable in `backend.log` for the first time**, which is the tool that path work has been
missing.
---
### [ARCHIVE-W42-2026-09-09.md] 12. ROLLBACK POINTS
New, from 2026-09-09 12:30:56. Register these in `openjarvis-rollback-points-2`:
```
Copy-Item 'C:\Users\Admin\OpenJarvis\src\openjarvis\cli\log_config.py.bak_loglevel_20260909-123056' 'C:\Users\Admin\OpenJarvis\src\openjarvis\cli\log_config.py' -Force
Copy-Item 'C:\Users\Admin\OpenJarvis\src\openjarvis\cli\serve.py.bak_loglevel_20260909-123056' 'C:\Users\Admin\OpenJarvis\src\openjarvis\cli\serve.py' -Force
Copy-Item 'C:\Users\Admin\OpenJarvis\start-openjarvis.ps1.bak_loglevel_20260909-123056' 'C:\Users\Admin\OpenJarvis\start-openjarvis.ps1' -Force
```
W40's stands and is already registered:
```
Copy-Item 'C:\Users\Admin\OpenJarvis\src\openjarvis\cli\serve.py.bak_debugreadable_20260908-093533' 'C:\Users\Admin\OpenJarvis\src\openjarvis\cli\serve.py' -Force
```
---
### [ARCHIVE-W42-2026-09-09.md] 13. DIAGNOSTIC TOOLING REGISTER - ADDITIONS
Per the 09/06 standing order, register every instrument so no future window rebuilds it.
| Instrument | Location | Output lands | Readable |
|---|---|---|---|
| `OPENJARVIS_LOG_LEVEL` env dial | `log_config.py:50-55`, set in `start-openjarvis.ps1:31` | controls the whole `openjarvis` tree level | YES - verified 09/09 |
| `patch-loglevel-v2.ps1` | repo root, UNTRACKED | console; dry run default | YES |
| `:552`/`:554` canary hash | inside `patch-loglevel-v2.ps1` | console at patch time | YES |
| Level-fix verification command | section 3, not saved to a file | console | YES |
| Cloud discriminating test | section 6, not saved to a file | console | untested |
| The 4 `[DEBUG]` lines | `serve.py:268/:280/:281/:513` | `backend.log` | **YES - as of 09/09. Previously the standing example of unreadable instrumentation. That lesson is now RESOLVED, and it took four windows.** |
| `serve.py:554` credentials line | `serve.py:554` | `backend.log` | **UNKNOWN - never fires on startup** |
| `openjarvis.retry400` | `engine\ollama.py:432-433` | unknown | **UNKNOWN - gate 4 suspected, still unread** |
---
### [ARCHIVE-W42-2026-09-09.md] 14. SDD / SDP FEED FROM THIS WINDOW
**Architecture.** The observability subsystem's three-regime structure documented in W41 is
unchanged, but regime 1 (the CLI click group's `setup_logging`) now has an EXTERNAL INPUT:
the `OPENJARVIS_LOG_LEVEL` environment variable. The SDD observability chapter needs the
configuration precedence recorded explicitly: `--quiet` beats `--verbose` beats
`OPENJARVIS_LOG_LEVEL` beats the WARNING default; and regime 3 (the three self-configuring
subtrees) still overrides all of it for its own subtrees by setting its own level and
`propagate = False`.
**Decision and evidence.** The decision to place the env check inside the author's function
rather than add a third configuration authority is now backed by a RUNTIME result, not only
by reading: six previously-dark loggers across three modules became readable from one
six-line change, with no new configuration site. That is the strongest available argument for
the single-authority principle and belongs in the SDD as a worked example.
**Hazards for the SDP.** The four-gate model (unchanged, now runtime-confirmed); the
execution policy block on unsigned scripts; the env var as a single point of darkness for
non-launcher starts; the 49,789-character encoding canary at `:554`; the unproven redaction;
and the cloud outage as an open fault.
**Ports, protocols, encoding at each gate** (per the 08/22 standing requirement): unchanged
this window. Server binds 127.0.0.1:8010, loopback confirmed by two independent BIND assertions
(`openjarvis.cli.serve` at WARNING and `openjarvis.server.auth_middleware` at INFO, the latter
newly visible and also reporting `api_key_set=True`). `backend.log` is UTF-8 with rotation at
10 MB x 4. `serve.py` on disk is UTF-8 WITH BOM; `log_config.py` and `start-openjarvis.ps1`
are UTF-8 WITHOUT BOM. **Any future patch harness must preserve those three states
individually - they are not uniform across the repo.**
**PLAIN LANGUAGE (the eight-year-old explanation), for the SDP:**
Last time we said the log file is a mailbox, and there are four ways a letter can fail to
arrive. The big one was rule number two: the post office had a sign saying "only URGENT
letters get delivered," and all our letters were marked ORDINARY, so they were thrown away.
Today we changed the sign. Now it says "ORDINARY letters are fine too."
And the letters arrived. Four letters we had been writing for two weeks and never seen, plus
two more from parts of the program we did not even know were trying to write to us. They were
all there, on time, perfectly readable. Nothing else was broken and nothing else needed
fixing. The map we drew last time was right.
One thing surprised us. There was a fifth letter we expected - the one about passwords - and
it never showed up. That is not because the post office threw it away. It is because the
person who writes that letter never sat down to write it at all that day. Something in the
program decides when he writes, and we do not know yet what that something is. So we still do
not know whether the special ink we installed - the ink that blacks out passwords so they
cannot be read - actually works, because he has not written anything for us to check.
The lesson: when you fix a thing, check every single thing you said you would check. Five out
of six is not six. The one that did not arrive is the one that teaches you something new.
---
### [ARCHIVE-W42-2026-09-09.md] 15. THE 550B CLOUD MODEL (STANDING, 08/29)
**BLOCKED THIS WINDOW.** See section 6. The tactic remains standing and correct; the
transport is broken. Restore it before treating it as unavailable long-term.
The bundle command written for the `:554` question, ready to run once cloud access is back
(PowerShell, Windows box, from `PS C:\Users\Admin\OpenJarvis>`). It truncates any line over
300 characters so the 49 KB literal cannot blow the context:
```powershell
$s='C:\Users\Admin\OpenJarvis\src\openjarvis\cli\serve.py'; $o='C:\Users\Admin\OpenJarvis\bundle-serve-552.md'; $a=Get-Content $s; $b=New-Object System.Text.StringBuilder; [void]$b.AppendLine("# BUNDLE: serve.py for the :554 question"); [void]$b.AppendLine("Line 554 is a single ~50KB damaged string literal and is TRUNCATED below. Do not comment on its contents."); [void]$b.AppendLine(""); [void]$b.AppendLine('```python'); for($i=1;$i -le $a.Count;$i++){ $t=$a[$i-1]; if($t.Length -gt 300){$t=$t.Substring(0,300)+" ...[TRUNCATED, original length "+$a[$i-1].Length+"]"}; [void]$b.AppendLine(("{0}: {1}" -f $i,$t)) }; [void]$b.AppendLine('```'); [IO.File]::WriteAllText($o,$b.ToString(),(New-Object System.Text.UTF8Encoding($false))); "WROTE {0}  ({1} KB)" -f $o,[math]::Round((Get-Item $o).Length/1KB,1)
```
The five-part prompt to send with it is in section 4.1.
**Suggested bundle set for other pending questions:** `engine\ollama.py` whole file for the
`retry400` gate-4 question; `cloud_router.py` plus whatever constructs the OpenRouter request
if section 6's test points at our code.
---
### [ARCHIVE-W43-2026-09-09.md] SECTION INDEX
| # | Section |
|---|---|
| 1 | What was done - narrative |
| 2 | The commit and push - CLOSED AND VERIFIED |
| 3 | The cloud thread - what was established |
| 4 | The discriminating test - the result that flipped the conclusion |
| 5 | Cloud loose ends - RECORDED AND PARKED, not a priority |
| 6 | New hazards and Claude-authored defects this window |
| 7 | Negative results - what this was NOT |
| 8 | Execution paths - carried, with one addition |
| 9 | The 550B cloud model - UNBLOCKED |
| 10 | Program goal and progress |
| 11 | Diagnostic tooling register - additions |
| 12 | SDD / SDP feed from this window |
| 13 | Rollback points |
---
### [ARCHIVE-W43-2026-09-09.md] 2. THE COMMIT AND PUSH - CLOSED AND VERIFIED
**Commit `b4cbd81`**, message "Logging: route openjarvis tree at INFO into backend.log",
5 files changed, 493 insertions, 7 deletions.
Staged explicitly, never `git add -A`:
- `src/openjarvis/cli/log_config.py` (9 lines changed)
- `src/openjarvis/cli/serve.py` (14 lines changed)
- `start-openjarvis.ps1` (2 lines added)
- `patch-loglevel-v2.ps1` (190 lines, new)
- `patch-debugreadable-v1b.ps1` (285 lines, new)
**Pushed to both remotes.** `origin` (GitHub, `cdgray33-git/OpenJarvis`) took
`411cd59..b4cbd81` as a fast-forward. `gitlab` (`172.16.33.126/root/openjarvis-desktop`)
confirmed at `b4cbd81` via `git ls-remote`. Plain `git push` only - no flags, and never
`--mirror` on the lab remote given the 08/05 incident.
### [ARCHIVE-W43-2026-09-09.md] 3.1 The key store, found
**`C:\Users\Admin\.openjarvis\cloud-keys.env`.** Declared at `cloud_router.py:25` as
`_CLOUD_ENV_FILE = Path.home() / ".openjarvis" / "cloud-keys.env"`, and read by `_load_keys()`
**on every request** so that live updates through the UI are picked up without a restart. The
process environment can override it, but does not have to supply it.
Gray entered the key through the app's Cloud Models tab. This is why it appears in neither
`.env`, nor the process environment, nor `config.toml` - all three of which were probed and all
three of which were the wrong place.
**Verified present, no content read:** 1 matching line, 73 characters, `sk-or-` prefix.
The Cloud Models tab also shows `ANTHROPIC_API_KEY` and `GEMINI_API_KEY` fields (empty) and an
OpenRouter field marked **"Connected"**. Note for future windows: **"Connected" means a key is
stored, not that it was validated against the API.** It is not a health signal.
### [ARCHIVE-W43-2026-09-09.md] 3.2 The `gpt-oss-120b:free` 404, fully explained
The live OpenRouter catalog (430 models) contains:
```
openai/gpt-oss-safeguard-20b
openai/gpt-oss-120b
openai/gpt-oss-120b:batch
openai/gpt-oss-20b
openai/gpt-oss-20b:batch
```
**There is no `:free` variant.** The OpenJarvis Cloud Models tab nonetheless offers
`openrouter/openai/gpt-oss-120b:free`. That is a stale hardcoded catalog entry for a slug the
provider retired. A 404 on `/chat/completions` with a valid key is the classic response to an
unknown model id, and this is exactly that.
**Origin is provider-side; the fix is ours.** Where the Cloud Models list is defined was NOT
located this window - that is action 2 in the brief.
By contrast, the catalog DOES contain `nvidia/nemotron-3-ultra-550b-a55b:free`, plus nine other
nemotron variants. The 550B slug was never retired.
### [ARCHIVE-W43-2026-09-09.md] 6.1 Three more unreadable instruments, in `cloud_router.py`
```python
print(f"[DEBUG] OpenRouter model string: {actual_model!r}", flush=True, file=sys.stderr)
print(f"[RETRY] 429 received, waiting {_delay}s", flush=True, file=sys.stderr)
print(f"[RETRY] 429 on attempt {_attempt}, retrying...", flush=True, file=sys.stderr)
```
**Exactly the 09/06 lesson, in a new location.** `print()` goes to the detached console;
`backend.log` captures only the `logging` module. These three have run on every cloud call and
produced zero readable bytes. Had they been readable, the model string actually sent and the
retry behavior would both have been visible from the start, and this window's investigation
would have been perhaps two exchanges instead of twelve.
The 09/06 standing order said to verify an instrument's output path at the moment it is added.
**It should be extended: audit existing `print()` instruments in any file a window opens, and
register them.** Converting these three to `logger` calls is action 3 in the brief.
### [ARCHIVE-W43-2026-09-09.md] 6.2 Claude-authored defects - FIVE in four windows
Three this window, following W40 4.4, W41 6.1 and W42 5.1:
**(a) Conclusion outran evidence.** Claude ran the W42 discriminating test, saw
`MODELS ENDPOINT OK. count=430`, and stated "key is valid, endpoint is valid." **OpenRouter's
`/models` endpoint is public and answers without authentication.** The 430-model list proved
the slugs existed and proved nothing whatever about the key. The 401 two exchanges later
exposed this. Gray was told the correction directly.
**(b) An unbounded listing command.** `Get-ChildItem -Recurse` over `~\.openjarvis` with no
`-First` would have dumped a large result into a token-constrained window. Gray refused to
paste it, correctly. **Standing correction: bound every listing command.**
**(c) A guessed path.** `cloud_router.py` was addressed at `src\openjarvis\engine\` when it
lives at `src\openjarvis\server\`. `Select-String` had returned bare filenames without
directories and Claude filled in the folder by assumption rather than asking. Gray supplied the
real path from Explorer.
**The common thread in (a) and (c) is asserting something not read.** Same family as W42's
off-by-one on line numbers, where anchors were transcribed by eye rather than derived
mechanically.
### [ARCHIVE-W43-2026-09-09.md] 6.3 The W42 discriminating test was built on a false premise
Its first statement was
`$k=(Get-Content '...\.env' | Select-String '^OPENROUTER_API_KEY=')`. **There has never been an
`OPENROUTER_API_KEY` line in `.env`.** The recorded key inventory for that file - GitLab,
Wiki.js, NetBox, Portainer, MySQL, Mailgun, peppers - contains no OpenRouter entry, and a direct
count returned `LINES=0`. The test sent `Bearer ` with an empty value and got an instant 401.
**Lesson for handoff authorship: a command written into an archive for a future window to run
carries an embedded assumption, and the assumption ages.** The W42 archive asserted a key
location it had not verified. Any command shipped in a handoff should state the premise it
depends on so the next window can check it in one step rather than debugging the test.
---
### [ARCHIVE-W43-2026-09-09.md] 7. NEGATIVE RESULTS - WHAT THIS WAS NOT
Per the 08/24 standing order, what was ruled out and how.
- **NOT the W42 logging changes.** Three independent grounds: `cloud_router.py` has mtime
  6/11/2026 and has not been touched in three months; the key resolution path
  (`cloud-keys.env` read at request time) intersects nothing W42 modified; and W42's five
  changes were a log level, two ranges in `_configure_file_logging`, and one launcher env var.
- **NOT provider-side, for nemotron.** Refuted by the 5.1 s successful call in section 4.
- **NOT free-tier queue saturation.** Same evidence. 5.1 s is not a saturated queue.
- **NOT a missing, malformed, or rotated key.** Present, 73 chars, `sk-or-` prefix, and it
  produced a successful completion.
- **NOT the `openrouter/` prefix.** `removeprefix` handles it correctly, read directly at
  `cloud_router.py` in `_stream_openai`.
- **NOT `.env`.** The OpenRouter key was never stored there. The malformed-`.env` thread on
  record in `openjarvis-config-secrets` is unrelated to this fault.
- **NOT a `config.toml` setting.** A key-name search of the live config returned zero matches
  for router, cloud, api_key, or openrouter.
- **NOT a CRLF normalization rewrite of `serve.py`.** Checked before pushing; 14 lines changed.
- **The 180.7 s failure is NOT a provider timeout** - it is our own `timeout=180` client.
---
### [ARCHIVE-W43-2026-09-09.md] 8. EXECUTION PATHS - CARRIED, WITH ONE ADDITION
The startup path from W40/W41/W42 is unchanged: `start-openjarvis.ps1` sets
`OPENJARVIS_LOG_LEVEL=INFO`, runs `python -m openjarvis.cli serve --port 8010`, entering the
click group at `cli\__init__.py:55` which calls `setup_logging` at `:62`, dispatching to
`serve()` at `:86`, which calls `_configure_file_logging()` at `serve.py:109` and
`uvicorn.Config(...)` at `serve.py:653`. Human present: yes.
The orchestrator `ask()` path and the managed-agent SSE stream via `_stream_managed_agent()`
are unchanged.
**NEW PATH, PARTIALLY MAPPED - the cloud request path.**
- Entry point: not yet identified (a chat request selecting a cloud model).
- `server\cloud_router.py`, module docstring states it **bypasses the engine system entirely**
  and uses `httpx` directly so no cloud SDK packages are required.
- `get_provider()` at `:69` routes by model-name prefix. OpenAI, Anthropic, Google and MiniMax
  are matched by prefix tuples; four HuggingFace orgs (`mlx-community/`, `bartowski/`,
  `unsloth/`, `lmstudio-community/`) are explicitly forced local; **any remaining model name
  containing a `/` falls through to `openrouter`.** That fallthrough is broad and worth noting
  in the SDD - it is a catch-all, not a whitelist.
- `_load_keys()` at `:39` reads `cloud-keys.env` from disk on every call, then lets six named
  process env vars override.
- `_stream_openai()` builds the payload, strips the `openrouter/` prefix, sets headers
  including `HTTP-Referer: https://openjarvis.local` and `X-Title: OpenJarvis`, and streams
  with `httpx.AsyncClient(timeout=180)` and `_retry_delays = [5, 10, 20]` on 429 only.
- Confirmation gate: **absent on this path** as far as read. Not verified beyond line 200.
- Event bus traffic: none observed in the first 200 lines.
- **A SECOND cloud path is known to exist but is unidentified - see section 5.**
---
### [ARCHIVE-W43-2026-09-09.md] 9. THE 550B CLOUD MODEL (STANDING, 08/29) - UNBLOCKED
**The blocker is lifted.** `nvidia/nemotron-3-ultra-550b-a55b:free` answered a direct call in
5.1 s. The tactic is available again for the `:554` question and for any other whole-file
question.
Two ways to use it. Direct API calls from PowerShell work now and bypass OpenJarvis entirely -
that is the reliable route until the second-path fault is fixed. Through the OpenJarvis UI it
may still fail, since the fault is on our side.
The bundle command for the `:554` question, unchanged, truncating any line over 300 characters
so the 49 KB literal cannot blow the context. PowerShell, Windows box, from
`PS C:\Users\Admin\OpenJarvis>`:
```powershell
$s='C:\Users\Admin\OpenJarvis\src\openjarvis\cli\serve.py'; $o='C:\Users\Admin\OpenJarvis\bundle-serve-552.md'; $a=Get-Content $s; $b=New-Object System.Text.StringBuilder; [void]$b.AppendLine("# BUNDLE: serve.py for the :554 question"); [void]$b.AppendLine("Line 554 is a single ~50KB damaged string literal and is TRUNCATED below. Do not comment on its contents."); [void]$b.AppendLine(""); [void]$b.AppendLine('```python'); for($i=1;$i -le $a.Count;$i++){ $t=$a[$i-1]; if($t.Length -gt 300){$t=$t.Substring(0,300)+" ...[TRUNCATED, original length "+$a[$i-1].Length+"]"}; [void]$b.AppendLine(("{0}: {1}" -f $i,$t)) }; [void]$b.AppendLine('```'); [IO.File]::WriteAllText($o,$b.ToString(),(New-Object System.Text.UTF8Encoding($false))); "WROTE {0}  ({1} KB)" -f $o,[math]::Round((Get-Item $o).Length/1KB,1)
```
The five-part `:554` prompt to send with it is in the W42 archive section 4.1.
**Suggested bundle set for the new question:** `server\cloud.py` whole file plus
`server\cloud_router.py` whole file, for the second-cloud-path question in section 5. Also
`engine\ollama.py` whole file for the `retry400` gate-4 question.
---
### [ARCHIVE-W43-2026-09-09.md] 11. DIAGNOSTIC TOOLING REGISTER - ADDITIONS
Per the 09/06 standing order.
| Instrument | Location | Output lands | Readable |
|---|---|---|---|
| `OPENJARVIS_LOG_LEVEL` env dial | `log_config.py:50-55`, set in `start-openjarvis.ps1:31` | whole `openjarvis` tree level | YES - verified 09/09 |
| The 4 `[DEBUG]` lines | `serve.py:268/:280/:281/:513` | `backend.log` | YES - as of 09/09 |
| `serve.py:554` credentials line | `serve.py:554` | `backend.log` | UNKNOWN - never fires on startup |
| `openjarvis.retry400` | `engine\ollama.py:432-433` | unknown | UNKNOWN - gate 4 suspected, unread |
| **OpenRouter models-catalog probe** | **not saved to a file; W43 section 3.2** | **console** | **YES - and note `/models` is a PUBLIC endpoint, it does NOT test the key** |
| **OpenRouter completion probe** | **not saved to a file; W43 section 4** | **console** | **YES - this is the real end-to-end key + slug test. Prefer it over the catalog probe.** |
| **`cloud-keys.env` shape probe** | **not saved to a file; W43 section 3.1** | **console** | **YES - prints count, length, prefix boolean only. Complies with the 08/01 no-echo rule.** |
| **`[DEBUG] OpenRouter model string`** | **`cloud_router.py`, in `_stream_openai`** | **detached console via `print(file=sys.stderr)`** | **NO - unreadable, see 6.1** |
| **`[RETRY] 429 received`** | **`cloud_router.py`, in `_stream_openai`** | **detached console via `print(file=sys.stderr)`** | **NO - unreadable, see 6.1** |
| **`[RETRY] 429 on attempt`** | **`cloud_router.py`, in `_stream_openai`** | **detached console via `print(file=sys.stderr)`** | **NO - unreadable, see 6.1** |
---
### [ARCHIVE-W43-2026-09-09.md] 12. SDD / SDP FEED FROM THIS WINDOW
**Architecture - new subsystem to document: cloud request routing.** The SDD needs a chapter
covering `server\cloud_router.py` as a distinct subsystem that, by its own docstring, bypasses
the engine entirely. Record: the provider-detection rules in `get_provider()` including the
four force-local HuggingFace orgs and the broad `"/" in model` catch-all to OpenRouter; the
request-time key load from `cloud-keys.env` with process-env override; the three message
conversion functions (`_to_openai_msgs`, `_to_anthropic_msgs`, `_to_google_contents`) and the
Gemini system-role workaround that injects a synthetic "Understood." assistant turn; the
`timeout=180` and `[5, 10, 20]` retry ladder; and the fact that a second cloud path exists and
is unmapped.
**Ports, protocols and encoding at this gate** (per the 08/22 requirement): outbound HTTPS 443
to `openrouter.ai`, path `/api/v1/chat/completions`, POST, JSON body, UTF-8, SSE response
consumed line-wise with a `data: ` prefix and a `[DONE]` sentinel. Auth is a bearer token in the
`Authorization` header. Two identifying headers are sent, `HTTP-Referer: https://openjarvis.local`
and `X-Title: OpenJarvis`.
**Decision and evidence, for the SDP:** the decision to read credentials from disk on every
request rather than at process start is deliberate and documented in the module docstring - it
makes UI-entered keys live without a restart. The evidence that it works is this window's
`LINES=1 / LEN=73 / STARTS_SK_OR=True` probe combined with the successful completion.
**Guard mechanisms in plain language** (per the 09/02 requirement): there is no confirmation
gate on the cloud path as read. When OpenJarvis wants to ask a cloud model something, it opens
the key file, finds the right key, addresses the letter, and sends it - nobody is asked first.
That is fine for asking a question, because asking a remote model to write text cannot delete a
file or send an email. The gates that matter are the ones on the tools the model's answer might
trigger afterwards, and those live elsewhere (Defect 6). **The SDD should state this explicitly
so a reader does not assume the cloud path is ungoverned by oversight - it is governed
downstream, not at the request.**
**Hazard for the SDP hazards register:** the `"/" in model` catch-all means any unrecognized
model name containing a slash is sent to OpenRouter with the user's key. A typo'd or
malformed local model name could produce an unintended outbound cloud call. Not observed, but
it follows from the code as read.
**Correction to prior SDD text:** any passage attributing the cloud outage to the W42 logging
changes, or to provider-side unavailability of the 550B, is wrong and should be rewritten per
sections 4 and 7.
---
### [ARCHIVE-W44-2026-09-10.md] SECTION INDEX
| # | Section | Read it when |
|---|---------|--------------|
| 1 | Window summary | You want the one-paragraph shape of W44 |
| 2 | The 550B call - what was sent and what came back | You are about to make another cloud call |
| 3 | The `:554` answer, in full | You are closing action 1 |
| 4 | NEGATIVE RESULTS AND REFUTED TESTS | Before running anything W44 or the 550B suggested |
| 5 | Hazards found | Before touching `serve.py` or the cloud path |
| 6 | Diagnostic tooling register | Before building any new instrument |
| 7 | Logging topology, current state | Before adding a log line or chasing a missing one |
| 8 | Execution path register | SDD architecture chapter |
| 9 | SDD / SDP feed from this window | You are writing the design package |
| 10 | The 550B bundle pattern, current form | You need whole-file analysis |
| 11 | Program goal and the progress problem | Action 5 |
---
### [ARCHIVE-W44-2026-09-10.md] 2. THE 550B CALL - WHAT WAS SENT AND WHAT CAME BACK
**Instrument:** `ask-550b-554.ps1`, repo root. Single script, no arguments.
**Sequence it runs:** canary hash check on line 554 (match printed as a boolean, literal never
printed) -> bundle build with the question embedded at the top and every line over 300
characters truncated with its original length noted -> key read from
`C:\Users\Admin\.openjarvis\cloud-keys.env`, printed as length and `sk-or-` boolean only ->
POST to `https://openrouter.ai/api/v1/chat/completions` with a 900 s timeout -> answer written
to `ANSWER-554-<stamp>.md` in the repo root and echoed to console.
**Measured, 2026-09-09 15:04:25:**
```
CANARY:  len=49789  match=True
FILE:    lines=655
BUNDLE:  bundle-serve-554-20260909-150425.md  (33.1 KB)
KEY:     found=True  len=73  prefix_ok=True
SEND:    model=nvidia/nemotron-3-ultra-550b-a55b:free  payload=35 KB
ELAPSED: 251.9s
FINISH:  length
CHARS:   2902
```
### [ARCHIVE-W44-2026-09-10.md] 2.1 Calibration facts for the next cloud call
- **252 s for a 35 KB payload**, against 5.1 s for the ten-token smoke test in W43. The W43
  figure is not a latency baseline for real work. **Budget four to five minutes**, and note
  this is comfortably inside the script's 900 s timeout but far outside the 180 s client
  timeout that the OpenJarvis path imposes. That gap is a second, independent reason to use
  the direct script rather than the UI.
- **`FINISH: length` means the answer was TRUNCATED at `max_tokens=6000`.** The answer stops
  partway through the fenced code block in question 5. Nemotron is a reasoning model and spends
  budget before it emits. **Raise `max_tokens` to 12000 for the next call, or ask fewer
  questions per call.** The truncation cost the closing brace of a command that was going to be
  discarded anyway, so nothing of value was lost this time. It will not always be so cheap.
- **Five questions is at or past the practical limit** for one call at that payload size.
---
### [ARCHIVE-W44-2026-09-10.md] 3.1 Enclosing scope
`serve()` at `:96`, signature
`def serve(host, port, engine_key, model_name, agent_name) -> None:`, running to EOF at `:655`.
Module-level Click command, decorator at `:79`. Not a method of any class. **The whole of
`serve.py` from `:96` down is one function.**
### [ARCHIVE-W44-2026-09-10.md] 3.2 The guard chain from `serve()` entry to `:554`
Four gates stand between entry at `:103` and line 554:
| Line | Gate | Failure behaviour |
|------|------|-------------------|
| `:115-124` | `try` / `except ImportError` on `uvicorn` and `fastapi` | `sys.exit(1)` |
| `:151-157` | `if resolved is None` after `get_engine(config, engine_key)` | `sys.exit(1)` at `:157` |
| `:224-232` | model resolution | `sys.exit(1)` at `:232` |
| `:553` | **`if _cred_parts:`** | falls through, no log, no error |
Everything else between those points - telemetry, cloud engine, instrumentation, agent,
channel, speech, agent manager, scheduler, memory, API key fallback, bind safety - is
`try`/`except` or `if` that logs and continues. None of it early-exits.
**Complete condition for `:554` to execute:** server dependencies import, AND an engine
resolves, AND a model resolves, AND at least one tool in `TOOL_CREDENTIALS` has one or more
credentials configured.
### [ARCHIVE-W44-2026-09-10.md] 3.3 Reachability - the reasoning that matters
The first three gates are **provably passed**, and this is the elegant part of the argument:
the server starts, and other `logger.info` calls in this same module reach `backend.log` after
the W43 level fix. A process that reached those lines cannot have taken any of the three
`sys.exit(1)` branches. **By elimination, only `:553` remains.**
`_cred_parts` is built at `:546-552`: iterate `sorted(TOOL_CREDENTIALS)` at `:547`, call
`get_credential_status(_tool_name)` at `:548`, count truthy values at `:549`, append
`f"{_tool_name}: {_set}/{_total} keys"` at `:551` **only when `_set > 0`**.
So on an install where no tool credential is configured, `_cred_parts` is `[]`, `:553` is
falsy, and `:554` never runs. **This is not a defect. It is the line working as written.**
### [ARCHIVE-W44-2026-09-10.md] 3.4 What `:554` logs - and why this closes the formatter item
`logger.info("Credentials loaded " + ", ".join(_cred_parts))`. `TOOL_CREDENTIALS` and
`get_credential_status` are imported at `:544` from `openjarvis.core.credentials`.
**Each element is a COUNT, not a value** - `"web_search: 1/2 keys"`. No key material, no
tokens, no secrets.
**Consequence for the carried "SanitizingFormatter applied but UNPROVEN" item:** the formatter
was applied on 09/09 specifically because raising the tree to INFO was thought to turn `:554`
into an unredacted secrets sink. That premise is wrong. `:554` never carried secrets.
**The formatter still stays.** It is correct defence for every other line in the tree, and
`backend.log` genuinely had no redaction before. But it is no longer blocking anything, and the
word "UNPROVEN" against it should stop implying risk. Downgrade, do not remove.
### [ARCHIVE-W44-2026-09-10.md] 3.5 The probe that closes this
Static read of credential state. No server start, no restart, no port collision, and it prints
key NAMES and booleans only, never values. PowerShell, Windows box, from
`C:\Users\Admin\OpenJarvis`:
```powershell
@'
try:
    from openjarvis.core.credentials import TOOL_CREDENTIALS, get_credential_status
except Exception as e:
    print("IMPORT FAILED: %r" % (e,)); raise SystemExit(1)
parts = []
for t in sorted(TOOL_CREDENTIALS):
    st = get_credential_status(t)
    if isinstance(st, dict):
        total = len(st); s = sum(1 for v in st.values() if v)
        print("TOOL %-24s set=%d total=%d keys=%s" % (t, s, total, sorted(st.keys())))
        if s > 0: parts.append("%s: %d/%d keys" % (t, s, total))
    else:
        print("TOOL %-24s -> unexpected return type %s" % (t, type(st).__name__))
print("")
print("CRED_PARTS_COUNT=%d" % len(parts))
print("GUARD_AT_553_PASSES=%s" % bool(parts))
'@ | Set-Content -Path 'C:\Users\Admin\OpenJarvis\probe_cred_parts.py' -Encoding ascii; uv run python 'C:\Users\Admin\OpenJarvis\probe_cred_parts.py'
```
**Reading the result:**
- `GUARD_AT_553_PASSES=False` - guard confirmed as the cause. Action 1 closes. `:554` is
  working correctly and there is nothing to fix.
- `GUARD_AT_553_PASSES=True` - **the guard is NOT the cause and the 550B's analysis is wrong
  somewhere.** Do not patch anything. Re-open with a wide read of `serve.py:540-560` and check
  whether `:546-552` sits behind an outer block the model did not report.
- `IMPORT FAILED` - the module path at `:544` is not what was reported. Wide-read
  `serve.py:535-560` before anything else.
The probe is defensive about `get_credential_status`'s return type because that type was never
directly read - only inferred from the model's description of `:549`.
---
### [ARCHIVE-W44-2026-09-10.md] 4. NEGATIVE RESULTS AND REFUTED TESTS
**This section exists because a window that changes nothing still produces knowledge.**
### [ARCHIVE-W44-2026-09-10.md] 4.2 What `:554` turned out NOT to be
- **NOT a level problem.** Settled in W43 and confirmed here - four sibling `logger.info` calls
  in the same module reach `backend.log`.
- **NOT a handler, formatter, sink or import problem.** Same evidence.
- **NOT a defect at all**, pending 3.5. It is a correctly guarded line on a path that is simply
  not taken on this install.
- **NOT a secrets exposure.** Section 3.4. The premise behind part of the 09/09 patch was
  mistaken, though the patch itself remains correct.
### [ARCHIVE-W44-2026-09-10.md] 5. HAZARDS FOUND
- **CONSOLE MOJIBAKE ON MODEL OUTPUT.** The 550B's em-dashes rendered as garbled bytes in the
  PowerShell transcript. The `ANSWER-554-*.md` file on disk is clean UTF-8. **Read the file,
  not the scrollback.** This is the same class as Gray's standing no-non-ASCII rule and is a
  display-layer problem, not a data problem.
- **`FINISH: length` is silent truncation.** The answer ends mid-code-block with no error and
  no marker in the text itself. **Always check `FINISH` before trusting a cloud answer is
  complete.** The script prints it; do not skip past it.
- **The canary held.** `len=49789`, `match=True`. Read-only access to `serve.py` did not
  disturb it, as expected. Recorded because the value of a canary is the unbroken run of
  matches, not the one time it fails.
- **`ask-550b-554.ps1` is untracked and matches no `.gitignore` rule.** `.gitignore:28` is
  `/patch-*.ps1`, hyphen form, and this is `ask-`, so a plain `git add` will pick it up. It is
  a reusable instrument and should be committed. The `bundle-*` and `ANSWER-*` files are
  regenerable output and should not be.
---
### [ARCHIVE-W44-2026-09-10.md] 6. DIAGNOSTIC TOOLING REGISTER
Standing rules, both earned 09/06: **search the schema before building an instrument**, and
**instrumentation you cannot read is instrumentation you do not have.**
### [ARCHIVE-W44-2026-09-10.md] 6.1 NEW THIS WINDOW
| Instrument | Location | Output lands | Readable |
|---|---|---|---|
| **`ask-550b-554.ps1`** | repo root, untracked | `ANSWER-554-<stamp>.md` and `bundle-serve-554-<stamp>.md`, both repo root; progress to console | **YES - verified at build time. Canary boolean, key length and prefix boolean only; no secret values, no raw literal.** |
Despite the name it is **not specific to `:554`**. To reuse it for another file, change `$src`
and replace the `$question` here-string. It is the general form of the 09/09 embedded-prompt
pattern. Consider renaming to `ask-550b.ps1` with parameters when it is next touched.
### [ARCHIVE-W44-2026-09-10.md] 6.2 PROPOSED, NOT YET RUN
`probe_cred_parts.py` - section 3.5. Static credential-state read. Once run, it belongs in this
register as readable-console-only, untracked, and is worth keeping alongside the other probes.
### [ARCHIVE-W44-2026-09-10.md] 6.3 CARRIED - READABLE
- `telemetry.db` at `C:\Users\Admin\.openjarvis\telemetry.db`. Live since July. Schema at
  `telemetry\store.py:17-40`. Carries `prompt_tokens`, `prompt_tokens_evaluated`, latency,
  ttft, cost, energy, GPU columns.
- `backend.log` at `C:\Users\Admin\AppData\Local\OpenJarvis\logs\backend.log`. `logging` module
  only - never raw `print()`. 10 MB x 3 since 09/09.
- `bundle_for_cloud.py`, repo root. The earlier general bundler. Reports missing files rather
  than skipping them silently. **Superseded in practice by 6.1 for single-file questions**,
  because it does not embed the prompt or send the request.
- `probe_telemetry_truncation.py`, `probe_telemetry_ceiling.py`, repo root, 09/06. Read-only
  against `telemetry.db`. Untracked, primary evidence, not regenerable from memory.
- `/api/ps` on the ollama host, 172.16.33.200. Zero-cost live-inference observability.
- Patch 4 RAWGEN (`_oj_raw_gen`) and RUNSTART at `native_openhands.py:598`, tagged temporary in
  `c37d8b1`.
### [ARCHIVE-W44-2026-09-10.md] 6.4 CARRIED - NOT READABLE
- `cli\serve.py:268/:280/:281` and `:513` - four unconditional `print(..., flush=True)` calls to
  a detached console. Zero readable bytes, ever. `:513` reports the memory-backend wiring count
  and is the most valuable of the four. **Converting them to `logger.info` is now a
  genuinely cheap win**, because the level gate that would have swallowed them is open as of
  09/09. This has been carried for four windows and is smaller than it looks.
### [ARCHIVE-W44-2026-09-10.md] 6.5 BLIND SPOTS, UNCHANGED
- Assembled prompt size is invisible at runtime. RUNSTART's `chars=` at `:605` is user input
  length only.
- The `agent` column in `telemetry` is blank on all rows, so no row attributes to a dispatch
  path.
- Engine instrumentation failure is SILENT - `serve.py:212-213` catches and logs at DEBUG,
  leaving the engine unwrapped. Telemetry row counts are a floor, not a census.
- `server\research_router.py:92` writes `prompt_tokens` into `prompt_tokens_evaluated`.
- `estimate_prompt_tokens` via the `max()` at `ollama.py:126` has produced impossible
  167k-token figures. Never read. Do not quote any number tracing back to it.
---
### [ARCHIVE-W44-2026-09-10.md] 7. LOGGING TOPOLOGY, CURRENT STATE
Pinned 09/08 after three windows were lost to instruments that could not be read.
### [ARCHIVE-W44-2026-09-10.md] 7.1 The four gates
A record must clear **all four** to reach `backend.log`:
1. It must use `logging`, not `print()`.
2. The emitting logger's effective level must permit it.
3. No `propagate=False` on the logger or any ancestor.
4. If `propagate=False`, the logger needs its own handler or the record is discarded silently.
### [ARCHIVE-W44-2026-09-10.md] 7.2 Current level state - the gate is OPEN
The 09/09 fix landed as one write via `patch-loglevel-v2.ps1`: an `OPENJARVIS_LOG_LEVEL`
override inside the author's own `log_config.py:setup_logging` consulted in the `else` branch
so `--verbose` and `--quiet` still win; `serve.py:61` maxBytes 4 MB to 10 MB; `serve.py:63-65`
plain `logging.Formatter` to `SanitizingFormatter`; and `start-openjarvis.ps1` exporting
`OPENJARVIS_LOG_LEVEL=INFO`. Canary unchanged, BOM preserved, `py_compile` clean.
Runtime-verified: all four `[DEBUG]` lines at `cli.serve` arrive as INFO, plus
`openjarvis.server.auth_middleware` BIND-ASSERT and `openjarvis.agents.scheduler` - surfaces
dark in every prior window.
**W44 adds:** `:554`'s continued silence is now explained by gate 0 - the code never runs -
rather than by any of the four. **The tree is not hiding it.**
### [ARCHIVE-W44-2026-09-10.md] 7.4 Configuration authorities
- `cli\log_config.py:23 setup_logging`, called from `cli\__init__.py:62` on **every** `jarvis`
  invocation. `:57` logger level, `:61` console handler, `:79` file handler at DEBUG. This is
  the author's code and the correct place for level policy.
- `cli\serve.py:70-72` - clears ROOT handlers, adds the file handler, sets ROOT to INFO.
- Three subtrees set their own level and `propagate=False`: `openjarvis.dispatch`
  (`tools\_stubs.py:111,127,128`), `openjarvis.agent` (`native_openhands.py:544,560,561`),
  **`openjarvis.retry400` (`engine\ollama.py:416,432,433`, SINK STILL UNCONFIRMED - this is
  action 2)**.
- `evals\cli.py:166` - separate entry point, root only, not on the serve path. Not a gate.
- `cli\serve.py:653` - `uvicorn.Config(..., log_level="info", log_config=None)`. `log_config=None`
  means uvicorn inherits root, which is why uvicorn INFO reaches `backend.log`.
### [ARCHIVE-W44-2026-09-10.md] 7.5 Still deficient
Every INFO/DEBUG in the tree using bare `getLogger(__name__)` was dark before 09/09 and is now
open: `server\routes.py:102,136` DEBUG and `:153` INFO (chat dispatch),
`server\stream_bridge.py:193,288` (SSE), `server\agent_manager_routes.py:21` (managed agent).
**These three files are why the level fix was worth six windows - they are the Defect 1 and
Defect 6 surfaces, and they are now visible. Action 4 is where that pays off.**
---
### [ARCHIVE-W44-2026-09-10.md] 8. EXECUTION PATH REGISTER
Per path: entry point, call chain with file:line, which `ToolExecutor` serves it and how that
executor is constructed, whether the confirmation gate is live / auto-approved / absent, event
bus traffic, and whether a human is present.
### [ARCHIVE-W44-2026-09-10.md] 8.1 Added this window - the startup path
**`jarvis serve` startup.** Entry: Click command `serve()` at `cli\serve.py:96`, decorator
`:79`, running to EOF `:655`. **The entire startup sequence is one function body.**
Ordered structure now known: dependency import `:115-124` (hard exit) -> engine resolution
`:151-157` (hard exit) -> model resolution `:224-232` (hard exit) -> a long run of
`try`/`except` blocks that log and continue, covering telemetry, cloud engine, instrumentation,
agent, channel, speech, agent manager, scheduler and memory -> credential summary `:546-554` ->
bind safety -> `uvicorn.Config` at `:653`.
**Property worth recording for the SDD:** after the three hard exits, **startup is
fail-soft throughout.** Any subsystem can fail and the server still comes up, having logged at
DEBUG or continued silently. `serve.py:212-213` is the named example - engine instrumentation
fails, is caught, logs at DEBUG, and the server runs with an unwrapped engine. **The operator
gets a running server that is quietly missing a subsystem.** This is a design characteristic,
not a bug, and it belongs in the design package explicitly because it determines how much any
"the server started" signal is actually worth.
No `ToolExecutor` on this path. No confirmation gate. No event bus traffic. Human present at
invocation only.
### [ARCHIVE-W44-2026-09-10.md] 8.2 Carried
- **`routes.py` chat dispatch, branches 1a/1b/1c/1d** - see `[[openjarvis-execution-paths]]`.
  Concurrency and tool-availability properties recorded there.
- **Orchestrator `ask()`** via `system\orchestrator.py`.
- **Managed-agent SSE stream** via `_stream_managed_agent()` in
  `server\agent_manager_routes.py`.
All three now emit into `backend.log` after the 09/09 level fix. **None has had its executor
construction, gate state, or bus traffic traced under the new visibility.** That is action 4.
---
### [ARCHIVE-W44-2026-09-10.md] 9.1 For the SDD architecture chapter
**Startup is a single fail-soft function.** Section 8.1. Three hard gates, then everything
degrades quietly. Document the ordered sequence and mark which subsystems can be absent from a
running server.
**Credential reporting is count-based by design.** `:546-554` reports `n/m keys` per tool and
never the values. This is a deliberate, correct pattern and should be cited in the SDP as the
house style for logging anything credential-adjacent.

