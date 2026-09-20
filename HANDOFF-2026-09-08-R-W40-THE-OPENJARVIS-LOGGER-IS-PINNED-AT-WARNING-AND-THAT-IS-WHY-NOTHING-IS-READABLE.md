# HANDOFF 2026-09-08 (R / W40)
## THE `openjarvis` LOGGER IS PINNED AT WARNING AND THAT IS WHY NOTHING IS READABLE

Window opened 09/08 morning off the W39 handoff. Next-action 1 (the four unreadable
`[DEBUG]` prints) was executed, applied, verified on disk, restarted - and STILL produced
zero readable bytes. Chasing that produced the actual root cause, which is a second
independent gate nobody had mapped. Gray converted that into a standing requirement:
map and record every logger tree and every source that configures logging.

**STATE AT CLOSE: one patch applied and verified on disk. Its runtime effect is
BLOCKED by the root cause below. A second patch is DESIGNED but NOT WRITTEN, pending
one unresolved read.**

---

## 1. WHAT WAS DONE

### 1.1 Patch applied: `print()` to `logger.info()` in `cli\serve.py`

Marker `openjarvis-debug-readable-v1`. Four lines only: `:268` `allowed`, `:280`
`registry_keys`, `:281` `tools_loaded`, `:513` `wired memory_backend`.

- Pre-patch: 253,764 B / SHA256 `1B06ACCB2183B54E421E68F11F1C8F74F88265AA4E66BD60304271522C4FCC12` / 654 lines / CRLF 653 / bare LF 0
- Post-patch: 253,868 B (delta +104) / SHA256 `A21D17DFA856027F63106C5848009F66D3FB234918C7BBB6EA551C7252B21C42`
- Line count, CRLF count, bare LF count all UNCHANGED. `:552` byte-identical. 18 `console.print` sites intact. `py_compile` clean under `.\.venv\Scripts\python.exe`.
- Delta reconciles exactly: per line `print(`to`logger.info(` = +6, dropping `, flush=True` = -12, trailing marker comment = +32; net +26 x 4 lines = 104.

Applied by `patch-debugreadable-v1b.ps1`, still in the repo root. Dry run then `-Apply`,
22 checks PASS.

**ROLLBACK (registered in `openjarvis-rollback-points-2`):**
```
Copy-Item 'C:\Users\Admin\OpenJarvis\src\openjarvis\cli\serve.py.bak_debugreadable_20260908-093533' 'C:\Users\Admin\OpenJarvis\src\openjarvis\cli\serve.py' -Force
```

### 1.2 Restart performed, result NEGATIVE

`backend.log` baseline 2,240,040 B at 09:36:50. After restart: 2,249,709 B, +9,669 B,
96 new lines. **Zero `[DEBUG]` lines.** The patch is correct and on disk; it is gated
elsewhere.

---

## 2. ROOT CAUSE - FOUND AND CONFIRMED IN SOURCE

`src\openjarvis\cli\log_config.py`:

```
L45:  logger = logging.getLogger("openjarvis")     <-- the PARENT of every openjarvis.* logger
L48:  logger.handlers.clear()
L50:  if quiet:    level = logging.ERROR
L52:  elif verbose: level = logging.DEBUG
L54:  else:         level = logging.WARNING        <-- the default
L57:  logger.setLevel(level)
L60:  console_handler = logging.StreamHandler()    <-- DETACHED CONSOLE, invisible
L64:  logger.addHandler(console_handler)
L67:  if verbose or log_file is not None:          <-- file handler ONLY in these cases
```

`src\openjarvis\cli\__init__.py`:
```
L52:  @click.option("--verbose", is_flag=True, default=False, ...)
L53:  @click.option("--quiet",   is_flag=True, default=False, ...)
L55:  def cli(ctx, verbose, quiet):                <-- top-level click GROUP
L62:      setup_logging(verbose=verbose, quiet=quiet)
L86:  cli.add_command(serve, "serve")
```

`start-openjarvis.ps1:31`:
```
& "C:\Users\Admin\OpenJarvis\.venv\Scripts\python.exe" -m openjarvis.cli serve --port 8010
```

**The chain:** the launch goes through `openjarvis.cli`, which is the click group. The
group body runs BEFORE the `serve` subcommand. Neither `--verbose` nor `--quiet` is
passed, so `level = logging.WARNING` and the `openjarvis` logger is EXPLICITLY set to
WARNING. Only then does `serve()` run and call `_configure_file_logging()` at
`serve.py:109`.

**Why this drops everything:** a `logger.info()` call is rejected at the EMITTING
logger's effective level check, before any handler is consulted. Because `openjarvis`
has an explicitly set level, that subtree never inherits from root - so
`serve.py:72 root_logger.setLevel(logging.INFO)` is irrelevant to it.

**Evidence this explains, completely:**
- `WARNING openjarvis.cli.serve: BIND_ASSERT` arrives. WARNING clears the bar.
- `WARNING openjarvis.skills.parser` (x2) arrives. Same reason.
- All 85 INFO lines in the restart window came from `uvicorn.access`, `uvicorn.error`, `httpx` - OUTSIDE the `openjarvis` tree, so untouched.
- `serve.py:552` is a plain `logger.info` on the credentials path, unrelated to our patch, and it is ALSO missing. This is the observation that killed every theory specific to our four lines.

**Ordering is favourable:** `setup_logging` runs first, `_configure_file_logging` runs
second. A level fix placed in `_configure_file_logging` runs LAST and overrides cleanly.

### 2.1 The lesson that generalizes

The 09/06 finding (`print()` goes to a detached console) was correct but INCOMPLETE.
There are TWO independent gates between an instrument and `backend.log`:

1. the call must go through the `logging` module, not `print()`
2. the emitting logger's effective level must permit the record

Converting `print()` to `logger.info` cleared gate 1 and left gate 2 shut. **Any future
instrument must be verified against BOTH gates at the moment it is added.**

---

## 3. NEGATIVE RESULTS - WHAT THIS WAS NOT, AND HOW THAT WAS ESTABLISHED

Recording these so no future window re-tests them.

- **NOT the root logger level.** `serve.py:72` sets root to INFO. Read directly.
- **NOT the file handler level.** The `RotatingFileHandler` built at `serve.py:60-65` has no `setLevel` call. Read directly.
- **NOT a stale/duplicate module.** `python -c "import openjarvis"` returned `PKG=C:\Users\Admin\OpenJarvis\src\openjarvis\__init__.py`. The repo copy is the imported copy, not a `site-packages` shadow.
- **NOT the patch failing to reach disk.** Re-read at absolute path after the restart showed all four lines carrying `logger.info(` and the marker.
- **NOT a branch that did not execute.** `serve.py:552` proves the whole `openjarvis` tree is affected, not one code path.
- **NOT invalid UTF-8 in the file.** Strict decode passed; zero replacement characters. `:552` mojibake is valid UTF-8 that merely renders badly.

---

## 4. NEW FILE-LEVEL AND METHOD HAZARDS EARNED THIS WINDOW

### 4.1 `cli\serve.py` CARRIES A UTF-8 BOM
`File.ReadAllText` STRIPS the BOM on read regardless of the encoding object passed. Any
read-modify-write that does not re-emit it silently drops three bytes. Caught by a
byte-identical round-trip test BEFORE patching: read with `UTF8Encoding($false)`, write
with `UTF8Encoding($true)`.

Corollary: `UTF8Encoding.GetBytes()` does NOT emit the preamble - only `File.WriteAllText`
does. Any in-memory size or BOM prediction must add `GetPreamble()` explicitly.

### 4.2 .NET's working directory is NOT PowerShell's location
`[System.IO.File]::ReadAllText('src\...')` resolved against `C:\WINDOWS\system32` and
threw. Worse, the failure left the previous `$L` in scope, so the next loop printed
PRE-PATCH content and looked like the patch had vanished. **Always absolute paths in
.NET calls. A throw does not clear the variable it was going to assign.**

### 4.3 `if`/`else` cannot be pasted across separate lines
PowerShell closes the `if` at the newline and rejects the orphan `else`. Keep
`} else {` on one line, or avoid the construct in pasted blocks.

### 4.4 Two Claude script defects, both caught by the dry run
- Expected per-line hashes held in an `[ordered]` hashtable keyed by integers. An `OrderedDictionary` indexed by an integer does POSITIONAL lookup, not key lookup - every expected hash came back `$null` and all four checks FAILED against a provably intact file. Use an array of objects.
- The BOM assertion ran against `GetBytes()` output, which never contains the preamble, so it reported FAIL on a write that would have been correct.

**Both times the first instinct was to suspect the target file, and both times the file
was fine and the instrument was wrong. A check that fails must be diagnosed before the
plan is changed.**

---

## 5. NEXT ACTIONS, IN ORDER

### 5.1 BLOCKER - one read, must happen first

`cli.py` is NOT at `src\openjarvis\cli\cli.py` (confirmed: file not found). The 09/08
grep reported `cli.py:166: def _setup_logging(verbose)` with calls at `:1267` and `:1398`,
but `Select-String` printed filenames without paths, so its true location is UNKNOWN.

There are therefore TWO author logging setups and we have only read one. Locate and read
it before designing the fix:

```powershell
Get-ChildItem -Recurse -Filter cli.py -Path C:\Users\Admin\OpenJarvis\src | Select-Object FullName
```
then read its `L150-L200`.

It may already expose an INFO path, in which case the author's mechanism is more complete
than `log_config.py` alone suggests and the fix shape changes.

### 5.2 THE DECISION GRAY MADE, AND WHAT IS STILL OPEN

Gray's direction, verbatim in substance:
- **Raise the log budget from 4 MB to 40 MB.**
- **The `[DEBUG]` lines were troubleshooting scaffolding that was never removed** - they can be demoted to a less chatty level rather than kept at full volume.
- **USE THE AUTHOR'S EMBEDDED CODE FIRST.** Only write new code for genuine gaps in the author's code, or for new capability being added.
- **He wants a HYBRID, and wants to see the code before a true answer is given.**

The three shapes that were on the table:

- **A - raise `openjarvis` to INFO inside `_configure_file_logging`.** One line after `serve.py:72`. Scoped to the serve path, overrides cleanly because it runs last, fixes the whole class including `:552`.
- **B - pass `verbose=True` from the serve path.** Uses the author's own mechanism. **PROBLEM:** `verbose` maps to DEBUG, not INFO, AND triggers the `cli.log` file handler at `log_config.py:67`. Much louder than wanted.
- **C - change the four lines to `logger.warning`.** Smallest change, unblocks today, leaves `:552` and every other INFO invisible. Treats the symptom.

**The observed gap in the author's code: `setup_logging` offers ERROR, DEBUG, or WARNING.
There is NO INFO option.** If `cli.py`'s `_setup_logging` does not supply one either, then
the missing INFO level IS the gap, and the correct hybrid under Gray's standing order is
to use the author's function and supply the level he did not expose - NOT to build a
parallel mechanism beside it.

**Do not finalize the fix shape until 5.1 is read.**

### 5.3 The patch, once the shape is settled

One file, one write, both changes together:
- `serve.py:61` `maxBytes=4 * 1024 * 1024` to `40 * 1024 * 1024` (Gray's 40 MB budget; `backupCount=3` presumably unchanged - CONFIRM with Gray whether 40 MB is the per-file size or the total ceiling, since 40 x 3 backups is 160 MB)
- the level fix, in whatever shape 5.1 dictates

Build it in the same shape as `patch-debugreadable-v1b.ps1`: dry run by default,
hash-anchored on full lines, BOM-preserving via `UTF8Encoding($true)`, `:552` hash
asserted before and after, no-drift check on all other lines, `py_compile`, timestamped
`.bak`, rollback command printed.

### 5.4 Then, and only then, verify

Restart and confirm all four `[DEBUG]` lines AND `serve.py:552` appear in `backend.log`.
**Nothing is closed until that is seen.** Applied and verified on disk is not the same as
readable - that is the whole lesson of this window.

### 5.5 Deferred, do not start mid-task

`log_config.py:48` clears handlers on the `openjarvis` logger and `:64` attaches a
`StreamHandler` to the detached console. `serve.py:70` separately clears handlers on the
ROOT logger. Two functions clearing handlers on different loggers at different times. The
ordering is now known (group first, serve second) but the full handler topology is not
mapped. Feed `openjarvis-logging-topology` when it is.

---

## 6. LOGGING TOPOLOGY REGISTER (NEW STANDING REQUIREMENT)

Gray, 09/08: *"we will identify and record every logger tree and every source that we
configure to send logs. Those need to be pinned for every future chat window to
reference. I see that we do not have enough tooling in place to understand our own system
and we both failed to record our findings in the beginning so we stop going around in
circles. This will be a requirement moving forward."*

Pinned to memory as `openjarvis-logging-topology`. **Every handoff from here carries this
section. Every window feeds it.**

### 6.1 Configuration sources (grep `setLevel|.level =|disable(` across `src`, 09/08)

| Location | What it does |
|---|---|
| `cli\log_config.py:45,57` | `getLogger("openjarvis")`, sets ERROR/DEBUG/**WARNING** - THE ROOT CAUSE |
| `cli\log_config.py:48` | clears handlers on the `openjarvis` logger |
| `cli\log_config.py:61` | console handler at same level, to detached console |
| `cli\log_config.py:79` | file handler at DEBUG - only if `verbose` or explicit `log_file` |
| `cli\__init__.py:57,62` | imports and calls `setup_logging` in the click group - runs on EVERY invocation |
| `cli\serve.py:70` | `root_logger.handlers.clear()` - discards anything attached earlier |
| `cli\serve.py:72` | `root_logger.setLevel(logging.INFO)` |
| `cli\serve.py:651` | `uvicorn.Config(..., log_level="info", log_config=None)` - no dictConfig, so uvicorn inherits root |
| `cli\cli.py:166` | a SECOND `_setup_logging(verbose)`, called `:1267` and `:1398` - **LOCATION UNKNOWN, NOT YET READ** |
| `agents\native_openhands.py:560` | `lg.setLevel(INFO)` |
| `engines\ollama.py:432` | `lg.setLevel(INFO)` |
| `tools\_stubs.py:127` | `lg.setLevel(INFO)` |

### 6.2 Sinks

| Sink | Path | Config |
|---|---|---|
| `backend.log` | `C:\Users\Admin\AppData\Local\OpenJarvis\logs\backend.log` | Rotating, 4 MB x 3 (**going to 40 MB**), formatter `%(asctime)s %(levelname)s %(name)s: %(message)s`, utf-8, on ROOT via `serve.py:71`. Carries `_TelemetryNoiseFilter` (`serve.py:67`, marker `openjarvis-log-budget-v1`) dropping `uvicorn.access` records containing `/v1/telemetry/energy` or `/v1/telemetry/stats` |
| `dispatch.log` | `%LOCALAPPDATA%\OpenJarvis\logs\` | logger `openjarvis.dispatch`, 2 MB x 4, `propagate=False` |
| `agent.log` | `%LOCALAPPDATA%\OpenJarvis\logs\` | own logger, 2.5 MB x 4, `propagate=False` |
| `cli.log` | `~\.openjarvis\cli.log` | 5 MB x 3, DEBUG - **only created when `verbose` is set**. Not present on the normal serve path |
| detached console | n/a | `print()` and `log_config.py:64`'s StreamHandler. **Zero readable bytes.** |
| `telemetry.db` | see diagnostic tooling register | per-call measurements since July |

### 6.3 Standing method notes
- A logger reaching `backend.log` at WARNING but not INFO is a LEVEL problem on that logger or its ancestors - check the EMITTING logger's effective level, not root.
- `propagate = False` on a subtree is a second, independent reason a line can be invisible.
- An explicitly set level on a parent logger means that subtree NEVER inherits from root.

---

## 7. DIAGNOSTIC TOOLING REGISTER (STANDING, 09/06)

Carried forward. See memory `openjarvis-diagnostic-tooling`.

- `dispatch.log` ATTEMPT/OUTCOME at the `ToolExecutor.execute` boundary - built, verified positive
- `agent.log` RUNSTART/TURN/RUNEND at the agent turn boundary - built, verified, correlates with dispatch via turn id
- RAWGEN instrument (Patch 4) in `native_openhands.py` - built, verified
- `telemetry.db` - **already recording on every call since July.** Search the schema BEFORE building any new instrument.
- BIND-ASSERT recorder in `auth_middleware.py` - appended, module imports clean, **NOT yet wired into serve.py**. Note: BIND_ASSERT lines ARE appearing in `backend.log`, at WARNING, from `openjarvis.cli.serve` - so some bind assertion is live on the serve path. Reconcile this against the "not yet wired" note; one of the two records is stale.
- **NEW 09/08:** `patch-debugreadable-v1b.ps1` in the repo root - a reusable, hash-anchored, BOM-preserving patch harness for `serve.py`. Do not rebuild this; adapt it.

**Both standing lessons still apply: SEARCH THE SCHEMA BEFORE BUILDING AN INSTRUMENT, and
INSTRUMENTATION YOU CANNOT READ IS INSTRUMENTATION YOU DO NOT HAVE.** This window is the
second proof of the latter.

---

## 8. EXECUTION PATH REGISTER

No new execution paths traced this window. Existing register unchanged - see memory
`openjarvis-execution-paths` for the `routes.py` chat dispatch branches (1a/1b/1c/1d),
the orchestrator `ask()` path, and the managed-agent SSE stream.

**One addition relevant to the register:** the STARTUP path is now traced end to end.
`start-openjarvis.ps1:31` runs `python -m openjarvis.cli serve --port 8010`, which enters
the click group at `cli\__init__.py:55` (running `setup_logging` at `:62`), then dispatches
to `serve()` registered at `:86`, which calls `_configure_file_logging()` at
`serve.py:109` and finally `uvicorn.Config(...)` at `serve.py:651`. Human present: yes,
manual start from the admin session. No autostart, not a service.

---

## 9. SDD / SDP FEED FROM THIS WINDOW

**Architecture:** the logging subsystem has TWO configuration authorities that run in
sequence on every start - the CLI click group (`setup_logging`, sets the `openjarvis`
tree) and the serve command (`_configure_file_logging`, sets root and owns the file
handler). Neither knows about the other. This is a genuine architectural finding and
belongs in the SDD observability chapter with the full call order.

**Decision and evidence:** the decision to raise the `openjarvis` logger level rather
than demote the instruments rests on the `serve.py:552` observation - the defect affects
every INFO in the tree, not the four patched lines, so a per-line fix would leave the
class of problem intact.

**Hazards for the SDP:** the UTF-8 BOM in `serve.py`; the .NET working-directory trap;
the two-gate model for instrument visibility. All three cost real cycles this window.

**PLAIN LANGUAGE (the eight-year-old explanation), for the SDP:**
Think of the log file as a mailbox, and every part of the program as a person who might
post a letter. There is a rule at the post office that says "only send letters marked
URGENT or worse." Our four notes were marked ORDINARY, so the post office threw them away
before they ever reached the mailbox. We spent the morning checking the mailbox, checking
the address, and checking whether the letters were written at all - when the problem was
a rule at the post office that nobody had written down. Now we have written it down.

---

## 10. THE 550B CLOUD MODEL (STANDING, 08/29)

If the next window needs whole files rather than targeted reads - and section 5.1 may
well need `cli.py` in full, since it is a large file with `_setup_logging` at `:166` and
callers at `:1267` and `:1398` - bundle the suspects into ONE markdown file for Gray to
feed to his 550B cloud model (openrouter nemotron-3-ultra-550b) rather than spending
window cycles on piecemeal reads.

**Suggested bundle for the logging question:** `cli\cli.py`, `cli\log_config.py`,
`cli\__init__.py`, and `cli\serve.py` lines 40-120.

---

## 11. PROGRAM GOAL AND PROGRESS

Goal: a FUNCTIONAL EXECUTIVE ASSISTANT that performs the duties at a computer a human
would. Approaching one year; not yet 50% of initial requirements. Gray needs a way to
MEASURE progress against those requirements. See memory `openjarvis-program-goals`.

**What this window moved toward that goal:** nothing user-facing. What it produced is
the ability to SEE the system - which has now blocked three separate windows and will
block every future diagnostic until it is fixed. The logging topology register exists so
this class of circling stops. That is infrastructure for velocity, not a feature, and it
should be counted as such rather than as progress against the requirement list.

**Honest note for the next window:** the requirements-measurement problem itself has now
been deferred across several windows. It is not a debugging task and will not surface
naturally during one. It needs its own window.

---

## 12. STANDING RULES CHECK

- ALWAYS VERIFY, never stack on unverified - held. The patch was dry-run, applied, disk-verified, restart-tested, and the negative result was chased rather than papered over.
- FINISH BEFORE STARTING THE NEXT - held. No second patch was proposed while the first was unverified. Section 5.5 is explicitly deferred.
- Shell and host on every command - held.
- No non-ASCII symbols - held.
- Working directory `PS C:\Users\Admin\OpenJarvis>` - held; the one relative-path failure is recorded as hazard 4.2.
- Push to BOTH remotes (`origin` = GitHub, `gitlab` = lab instance) - **NOT DONE THIS WINDOW.** The `serve.py` change and `patch-debugreadable-v1b.ps1` are uncommitted. Stage explicit paths, never `git add -A`.
- 15-exchange flag - reached and flagged; the live trace was not cut, per the 08/24 rule.
