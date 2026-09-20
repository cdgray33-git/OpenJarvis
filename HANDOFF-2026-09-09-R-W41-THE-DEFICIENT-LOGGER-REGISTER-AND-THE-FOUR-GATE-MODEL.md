# HANDOFF 2026-09-09 (R / W41)
## THE DEFICIENT LOGGER REGISTER, AND THE GATE MODEL IS FOUR NOT TWO

Window opened 09/09 off the W40 handoff, under an explicit budget constraint from Gray
(67 percent usage at open, investigation only, lowest cost path). Executed W40 next-action
5.1 (the BLOCKER read), then closed the logging topology register on both sides -
operational and deficient. **NO CODE WAS WRITTEN, NO FILE WAS MODIFIED, NO RESTART WAS
PERFORMED.** This was a pure investigation window and it ended by Gray's call to hand off
clean rather than start the patch shallow.

**STATE AT CLOSE: W40's patch is still on disk and still gated. The level fix is now fully
designed and unblocked, but TWO DECISIONS FROM GRAY ARE OUTSTANDING and the patch must not
be written until they land. See section 5.**

---

## 1. WHAT WAS DONE - NARRATIVE

Four reads, in sequence, each one closing a question the previous one opened.

**Read 1 - locate `cli.py` (W40 blocker 5.1).** `Get-ChildItem -Recurse -Filter cli.py`
returned exactly one hit: `src\openjarvis\evals\cli.py`. Not `cli\cli.py`. The W40 grep had
printed filenames without paths and the true location was a different package entirely.

**Read 2 - `evals\cli.py` L160-200.** `_setup_logging(verbose)` at `:166` is a
`logging.basicConfig(level=DEBUG if verbose else INFO, ...)` call. Two consequences, both
decisive:
- `basicConfig` configures the ROOT logger and is a NO-OP when root already has handlers.
  It never touches the `openjarvis` logger.
- It is on the `evals` entry point, which the serve path never imports.

So this is NOT a second gate on our defect, and it is NOT a reusable INFO route. **W40
blocker 5.1 is CLOSED.** The two-author-logging-setups worry from W40 section 5.1 was
unfounded, and that is recorded as a negative result below.

**Read 3 - `cli\log_config.py` in full, plus `cli\serve.py` L40-L130.** This confirmed the
W40 root cause line by line and added one finding W40 did not have. `setup_logging` offers
ERROR, DEBUG, or WARNING and NOTHING ELSE - there is no INFO route to the `openjarvis` tree
anywhere in the author's code. That makes the gap real rather than suspected, which is what
Gray's use-the-author's-code-first order needed established before a fix shape could be
chosen. Also confirmed: no `propagate = False` anywhere in `log_config.py`, so once the
level gate opens, records DO reach root's file handler. Nothing else is in the way.

**Read 4 - the propagation and configuration grep across `src`.** First attempt was
DEFECTIVE (see hazard 6.1). Corrected, it produced the operational register in section 3
and exposed that the register was structurally incomplete - it could only see modules that
call `setLevel`, `propagate`, `basicConfig`, or `getLogger("openjarvis`. Modules using a
plain `getLogger(__name__)` matched nothing.

**Read 5 - the `getLogger(__name__)` enumeration.** Sorted-unique file list, roughly 225
modules. That is the true size of the silenced surface. Section 4 holds the register.

---

## 2. THE GATE MODEL IS FOUR, NOT TWO - SUPERSEDES W40 SECTION 2.1

W40 recorded two independent gates between an instrument and `backend.log`. The 09/09 grep
exposed two more. **Any future instrument must be verified against ALL FOUR at the moment
it is added.**

| Gate | Condition | How it fails silently |
|---|---|---|
| 1 | The call must go through the `logging` module, not `print()` | `print()` goes to the detached console. Zero readable bytes. Earned 09/06. |
| 2 | The EMITTING logger's effective level must permit the record | Rejected before any handler is consulted. An explicitly set level on a parent means that subtree NEVER inherits from root. Earned 09/08. |
| 3 | `propagate = False` on the logger or any ancestor | Record stops before it reaches root's handler. Earned 09/09. |
| 4 | A logger with `propagate = False` AND no handler of its own | Record is discarded with no error and no destination at all. Earned 09/09. |

Gate 4 is the dangerous one. It looks exactly like working instrumentation in source and
produces nothing at runtime, with no exception to catch.

---

## 3. OPERATIONAL LOGGING REGISTER - WHAT WORKS TODAY

### 3.1 The three self-configured subtrees

Each sets its own level to INFO on its own authority, so it clears gate 2 without consulting
the WARNING parent. Each also sets `propagate = False`, so it bypasses root entirely and
writes only to its own sink. **This is why `dispatch.log` and `agent.log` verified positive
while everything else went dark. They were never subject to the defect. That is luck, not
design.**

| Logger | Declared / configured at | Sink | Status |
|---|---|---|---|
| `openjarvis.dispatch` | `tools\_stubs.py:111`, `:127` setLevel INFO, `:128` propagate False | `dispatch.log` | VERIFIED POSITIVE (W-earlier) |
| `openjarvis.agent` | `agents\native_openhands.py:544`, `:560` setLevel INFO, `:561` propagate False | `agent.log` | VERIFIED POSITIVE (W-earlier) |
| `openjarvis.retry400` | `engine\ollama.py:416`, `:432` setLevel INFO, `:433` propagate False | UNCONFIRMED | **SUSPECTED GATE 4 - see 4.2** |

### 3.2 Everything outside the `openjarvis` tree

`uvicorn.access`, `uvicorn.error`, `httpx` inherit ROOT at INFO (`serve.py:72`) and land in
`backend.log`. All 85 INFO lines in the W40 restart window were these. This works because
`serve.py:651` passes `log_config=None` to `uvicorn.Config`, so uvicorn inherits root rather
than installing its own dictConfig. **Do not "fix" that None - it is load-bearing.**

### 3.3 WARNING and above, everywhere in the tree

BIND_ASSERT from `openjarvis.cli.serve` and the two `openjarvis.skills.parser` lines arrive
for exactly this reason. WARNING clears gate 2 even with the parent pinned.

### 3.4 The noise filter

`_TelemetryNoiseFilter` (`serve.py:28-45`, attached `:67`, marker `openjarvis-log-budget-v1`)
is live and dropping `uvicorn.access` records for `/v1/telemetry/energy` and
`/v1/telemetry/stats`. Working as designed.

---

## 4. DEFICIENT LOGGER REGISTER - WHAT IS DARK, AND WHY

### 4.1 The register

| Logger / concern | Declared at | Gate blocking it | Sink it should reach | Fix that unblocks it |
|---|---|---|---|---|
| `openjarvis.server` | `server\routes.py:102` DEBUG, `:136` DEBUG, `:153` INFO | 2 | `backend.log` via root | Level fix |
| `openjarvis.server` | `server\stream_bridge.py:193`, `:288` | 2 | `backend.log` via root | Level fix |
| `openjarvis.server.agent_manager` | `server\agent_manager_routes.py:21` | 2 | `backend.log` via root | Level fix |
| `openjarvis.cli.serve` - the 4 patched DEBUG lines | `serve.py:268`, `:280`, `:281`, `:513` | 2 | `backend.log` via root | Level fix |
| `openjarvis.cli.serve` - credentials line | `serve.py:552` | 2 | `backend.log` via root | Level fix PLUS formatter swap |
| ~225 modules using `getLogger(__name__)` with no `setLevel` | see 4.3 | 2 | `backend.log` via root | Level fix |
| `openjarvis.retry400` | `engine\ollama.py:432-433` | **4 SUSPECTED** | unknown | Read required first - see 4.2 |
| `cli.log` sink | `log_config.py:67` | Never constructed on the serve path | `~\.openjarvis\cli.log` | Not needed if the level fix lands |
| Detached console sink | `log_config.py:60-64` StreamHandler, plus surviving `print()` calls | 1 | nothing readable | OUT OF SCOPE - abandon this sink |
| `backend.log` credential redaction | `serve.py:64` plain `logging.Formatter` | n/a - correctness, not visibility | `backend.log` | `SanitizingFormatter` swap |
| `channels\slack_daemon.py:198` | `basicConfig` | Separate process entry point | unknown | OUT OF SCOPE this thread |
| `mining\_miner_loop_main.py:224` | `basicConfig` | Separate process entry point | unknown | OUT OF SCOPE this thread |
| `mining\_mps_miner_loop_main.py:304` | `basicConfig` | Separate process entry point | unknown | OUT OF SCOPE this thread |

`ERROR` at `server\routes.py:411` is NOT in this table - it clears gate 2 and arrives today.
Only DEBUG and INFO in that file are lost.

### 4.2 `openjarvis.retry400` - THE ONE UNRESOLVED ITEM

`engine\ollama.py:416` declares it, `:432` sets INFO, `:433` sets `propagate = False`. If no
handler is attached to that logger nearby, gate 4 applies and those records reach nothing at
all, silently. **I did not read that block. Do not assume either way.**

This matters beyond tidiness: RETRY400 is instrumentation built for the Defect 1
investigation (see `openjarvis-defect1-engine`, where the RETRY400 tools-drop theory died
09/02). If it has been writing to nowhere, that is a third instance of INSTRUMENTATION YOU
CANNOT READ IS INSTRUMENTATION YOU DO NOT HAVE, and it would need re-examining before any
conclusion drawn from its silence is trusted.

One wide read settles it. PowerShell, Windows box, from `PS C:\Users\Admin\OpenJarvis>`:

```powershell
$h='C:\Users\Admin\OpenJarvis\src\openjarvis\engine\ollama.py'; Get-Content $h | Select-Object -Skip 379 -First 121 | ForEach-Object -Begin {$i=380} -Process {"{0}: {1}" -f $i,$_; $i++}
```

### 4.3 The size of the silenced surface

The `getLogger(__name__)` enumeration returned roughly 225 unique modules. Two caveats that
matter for prioritisation:

- Roughly 65 are under `evals\` and roughly 33 under `learning\`. Those are eval-time and
  offline-training paths, not the serve path. **The serve-relevant silenced surface is
  therefore on the order of 127 modules**, which is still the overwhelming majority of the
  running system.
- The counts above are derived from the sorted-unique list in the W41 transcript. If an
  exact figure is needed for the SDD, re-derive rather than quoting these.

Re-derive with, from `PS C:\Users\Admin\OpenJarvis>`:

```powershell
(Get-ChildItem -Path 'C:\Users\Admin\OpenJarvis\src' -Recurse -Filter *.py | Select-String -Pattern 'getLogger\(__name__\)' | ForEach-Object { $_.Path } | Sort-Object -Unique).Count
```

### 4.4 What the level fix actually buys

Raising `openjarvis` to INFO restores every category in 4.1 EXCEPT `cli.log`, the console
sink, and anything hitting gates 3 or 4. Concretely that is the entire `routes.py` /
`stream_bridge.py` / `agent_manager_routes.py` server surface - **the exact paths needed for
the Defect 1 and Defect 6 work.** This is the unlock, not a cleanup.

---

## 5. THE TWO OPEN DECISIONS - PATCH IS BLOCKED ON THESE

Asked twice in W41, not yet answered. **Do not write the patch without them.**

### 5.1 Fix shape

The observed gap is real and confirmed: `setup_logging` offers ERROR, DEBUG, WARNING and no
INFO. Under Gray's standing USE THE AUTHOR'S CODE FIRST order, the correct hybrid is to
supply the level he did not expose, inside his own function.

- **RECOMMENDED - env override inside `log_config.py:setup_logging`.** An
  `OPENJARVIS_LOG_LEVEL` check ahead of the quiet/verbose ladder, default unchanged at
  WARNING. `start-openjarvis.ps1` sets it to INFO. Keeps ONE authority over the `openjarvis`
  tree, and gives Gray a dial without another code edit later.
- **FALLBACK - shape A, one `setLevel` line in `_configure_file_logging` after
  `serve.py:72`.** Works, runs last, overrides cleanly, scoped to the serve path. **Cost:
  creates a THIRD place that configures logging, which is the precise architectural fault
  W40 documented.**
- **DEAD - shape B (`verbose=True` from the serve path).** Maps to DEBUG not INFO, and
  triggers the `cli.log` file handler at `log_config.py:67`. Much louder than wanted. Killed
  in W41 on the `log_config.py` read.
- **DEAD - shape C (demote the four lines to `logger.warning`).** Leaves `:552` and every
  other INFO in the tree invisible. Treats the symptom. Killed by the `:552` observation in
  W40.

### 5.2 The 40 MB budget

`serve.py:61` is `maxBytes=4 * 1024 * 1024, backupCount=3`. Gray's direction is 40 MB.
**Is that 40 MB PER FILE (160 MB total with 3 backups) or 40 MB TOTAL (about 13 MB per file,
or 40 MB with backupCount reduced)?** Not yet answered.

---

## 6. NEW HAZARDS EARNED THIS WINDOW

### 6.1 `Select-String` has NO `-Recurse` parameter
The W41 propagation grep was written as
`Select-String -Path '...\src\*.py' -Recurse -Pattern ...` and threw
`NamedParameterNotFound`. `-Path` does not recurse and there is no `-Recurse` on this cmdlet.
Correct form is `Get-ChildItem -Recurse -Filter *.py | Select-String -Pattern ...`.
**This is a Claude-authored command defect, the third in two windows. Same family as W40
hazard 4.4: the instrument was wrong, not the target.**

### 6.2 Narrow reads are a standing defect - Gray's correction, verbatim in substance
Gray, 09/09: *"small queries has bitten us many times and we have up to 3 versions of the
same functions because of it. 40 lines should be 150 or 200."* Reading the minimum slice is
how duplicate implementations of the same function got written without anyone noticing.
**Standing rule from here: pull the whole file or a generous surrounding range, and prefer
ONE WIDE read over several targeted ones.** The W41 reads after this correction were built
that way and each one closed more than it was aimed at.

### 6.3 `serve.py:552` IS A LIVE ENCODING CANARY - upgraded from W40's assessment

W40 recorded `:552` as "valid UTF-8 that merely renders badly." **That understates it.** The
line read in full in W41 is a single string literal of roughly TEN KILOBYTES of compounding,
self-similar, nested encoding damage - the same escalating sequence repeated hundreds of
times. That pattern is the signature of a UTF-8 string read as cp1252 and re-encoded as
UTF-8, REPEATEDLY, across many read-modify-write cycles. Each cycle roughly doubles it. The
original was almost certainly a single check mark or arrow character.

Three consequences:

1. **It is a canary and it is now stable.** W40's harness
   (`UTF8Encoding($false)` read, `UTF8Encoding($true)` write) is correct. If `:552` ever
   GROWS again, a patch harness has broken encoding. **Hash `:552` before and after every
   write to this file, forever.**
2. **It is evidence of the file's history.** Multiple prior write cycles used the wrong
   encoding. The damage is still sitting in the file.
3. **It must NOT ride along in the level patch.** Replacing the blob with plain ASCII is its
   own patch, AFTER the level fix is verified. It is cosmetic plus ten kilobytes; the level
   fix is the blocker. Under FINISH THE THING BEFORE STARTING THE NEXT, it waits.

### 6.4 `backend.log` HAS NO CREDENTIAL REDACTION

The author wrote `SanitizingFormatter` (`log_config.py:15-20`, wrapping `CredentialStripper`)
and applied it to the console handler at `:62` and the `cli.log` handler at `:80`.
`serve.py:64` uses a PLAIN `logging.Formatter`. **`backend.log` is unredacted today.**

This is not academic. The line we are trying to make visible, `:552`, is on the credentials
path. Raising the tree to INFO turns that line ON, into an unredacted sink, which we are
simultaneously enlarging to 40 MB. Against the 08/01 credential exposure that already forced
a rotation (see `openjarvis-config-secrets`), **the formatter swap must land in the SAME
write as the level fix.** Do not separate them.

---

## 7. NEGATIVE RESULTS - WHAT THIS WAS NOT

Recorded so no future window re-tests them. W40's list still stands in full; these are new.

- **NOT a second author logging setup on the serve path.** `cli.py` is `evals\cli.py`, a
  different package, never imported by `openjarvis.cli serve`. W40's 5.1 worry is dead.
- **NOT a usable INFO route hiding in `evals\cli.py`.** It is `basicConfig`, which targets
  root and is a no-op when root has handlers. Cannot reach the `openjarvis` tree.
- **NOT a propagation problem in `log_config.py`.** Read in full; no `propagate = False`
  anywhere in it. Once gate 2 opens, records reach root's handler.
- **NOT limited to a few modules.** The `getLogger(__name__)` enumeration proves the
  silenced surface is roughly 225 modules, about 127 of them on serve-relevant paths.
- **NOT a uvicorn dictConfig problem.** `log_config=None` at `serve.py:651` means uvicorn
  inherits root, which is why uvicorn lines arrive at INFO today.

---

## 8. NEXT ACTIONS, IN ORDER

1. **GET THE TWO DECISIONS FROM GRAY** (section 5). Blocking. Do not write code first.
2. **Read `engine\ollama.py` L380-L500** (section 4.2) to resolve the `retry400` gate-4
   suspicion. One wide read. Cheap, and it may invalidate a prior Defect 1 conclusion.
3. **Write the single patch** - `serve.py:61` size, `serve.py:64` formatter swap, and the
   level fix in whatever shape 5.1 dictates. ONE file write covering all three, built on
   `patch-debugreadable-v1b.ps1` (do not rebuild it, adapt it): dry run by default,
   hash-anchored on full lines, BOM-preserving via `UTF8Encoding($true)`, `:552` hash
   asserted before and after, no-drift check on all other lines, `py_compile`, timestamped
   `.bak`, rollback command printed. Register the rollback in
   `openjarvis-rollback-points-2`.
4. **Restart and VERIFY.** All four `[DEBUG]` lines AND `serve.py:552` must appear in
   `backend.log`, and `:552` must appear REDACTED. **Nothing is closed until that is seen.**
   Applied and verified on disk is not the same as readable - that is the W40 lesson and it
   has not been earned back yet.
5. **Only then**: commit and push to BOTH remotes (see section 12 - there is already
   uncommitted work sitting there from W40).
6. **Deferred, do not start mid-task**: the `:552` ASCII replacement (6.3); the full handler
   topology map for W40 5.5; the three separate-entry-point `basicConfig` sites.

---

## 9. LOGGING TOPOLOGY REGISTER (STANDING, 09/08) - UPDATED

Gray, 09/08: *"we will identify and record every logger tree and every source that we
configure to send logs. Those need to be pinned for every future chat window to reference. I
see that we do not have enough tooling in place to understand our own system and we both
failed to record our findings in the beginning so we stop going around in circles. This will
be a requirement moving forward."*

Pinned as `openjarvis-logging-topology`. **Every handoff from here carries this section.
Every window feeds it.** W41 contribution: the operational register (section 3), the
deficient register (section 4), and the four-gate model (section 2), which together close
the register on both sides for the first time.

### 9.1 Configuration sources - full list as of 09/09

| Location | What it does |
|---|---|
| `cli\log_config.py:45,57` | `getLogger("openjarvis")`, sets ERROR/DEBUG/**WARNING** - THE ROOT CAUSE. No INFO option exists. |
| `cli\log_config.py:48` | clears handlers on the `openjarvis` logger |
| `cli\log_config.py:61` | console handler at same level, to detached console |
| `cli\log_config.py:79` | file handler at DEBUG - only if `verbose` or explicit `log_file` |
| `cli\__init__.py:57,62` | imports and calls `setup_logging` in the click group - runs on EVERY invocation, BEFORE the subcommand |
| `cli\serve.py:70` | `root_logger.handlers.clear()` |
| `cli\serve.py:72` | `root_logger.setLevel(logging.INFO)` |
| `cli\serve.py:651` | `uvicorn.Config(..., log_level="info", log_config=None)` - uvicorn inherits root. Load-bearing. |
| `evals\cli.py:166,168` | `_setup_logging` -> `basicConfig`. ROOT only, no-op if root has handlers. **NOT on the serve path.** RESOLVED 09/09. |
| `agents\native_openhands.py:544,560,561` | `openjarvis.agent`, INFO, propagate False |
| `engine\ollama.py:416,432,433` | `openjarvis.retry400`, INFO, propagate False. **Handler UNCONFIRMED.** |
| `tools\_stubs.py:111,127,128` | `openjarvis.dispatch`, INFO, propagate False |
| `channels\slack_daemon.py:198` | `basicConfig`. Separate entry point. Unmapped. |
| `mining\_miner_loop_main.py:224` | `basicConfig`. Separate entry point. Unmapped. |
| `mining\_mps_miner_loop_main.py:304` | `basicConfig`. Separate entry point. Unmapped. |

### 9.2 Sinks

| Sink | Path | Config |
|---|---|---|
| `backend.log` | `C:\Users\Admin\AppData\Local\OpenJarvis\logs\backend.log` | Rotating, 4 MB x 3 (**going to 40 MB, size question open**), formatter `%(asctime)s %(levelname)s %(name)s: %(message)s`, utf-8, on ROOT via `serve.py:71`. Carries `_TelemetryNoiseFilter` (`serve.py:67`, marker `openjarvis-log-budget-v1`). **NO CREDENTIAL REDACTION - see 6.4.** |
| `dispatch.log` | `%LOCALAPPDATA%\OpenJarvis\logs\` | logger `openjarvis.dispatch`, 2 MB x 4, propagate False. OPERATIONAL. |
| `agent.log` | `%LOCALAPPDATA%\OpenJarvis\logs\` | own logger, 2.5 MB x 4, propagate False. OPERATIONAL. |
| `cli.log` | `~\.openjarvis\cli.log` | 5 MB x 3, DEBUG - **only created when `verbose` is set. Not present on the serve path.** |
| detached console | n/a | `print()` and `log_config.py:64`'s StreamHandler. **Zero readable bytes. Abandon.** |
| `telemetry.db` | see diagnostic tooling register | per-call measurements since July |
| `retry400` destination | UNKNOWN | **Possibly nothing at all. Gate 4 suspected. See 4.2.** |

### 9.3 Standing method notes
- A logger reaching `backend.log` at WARNING but not INFO is a LEVEL problem on that logger
  or its ancestors - check the EMITTING logger's effective level, not root.
- An explicitly set level on a parent logger means that subtree NEVER inherits from root.
- `propagate = False` is a second, independent reason a line can be invisible (gate 3).
- `propagate = False` with NO handler attached means the record goes nowhere and raises
  nothing (gate 4). This is the failure mode that looks like working code.
- `basicConfig` targets ROOT and silently does nothing if root already has handlers. It is
  never a way to configure the `openjarvis` tree.

---

## 10. DIAGNOSTIC TOOLING REGISTER (STANDING, 09/06)

Carried forward. See memory `openjarvis-diagnostic-tooling`.

- `dispatch.log` ATTEMPT/OUTCOME at the `ToolExecutor.execute` boundary - built, verified
  positive. Confirmed 09/09 to be gate-immune (self-configured subtree).
- `agent.log` RUNSTART/TURN/RUNEND at the agent turn boundary - built, verified, correlates
  with dispatch via turn id. Same gate immunity.
- RAWGEN instrument (Patch 4) in `native_openhands.py` - built, verified.
- **RETRY400 instrument in `engine\ollama.py` - STATUS DOWNGRADED TO UNVERIFIED 09/09.**
  Gate 4 suspected. Its destination is unconfirmed. Do not trust conclusions drawn from its
  silence until 4.2 is read.
- `telemetry.db` - **already recording on every call since July.** SEARCH THE SCHEMA BEFORE
  BUILDING ANY NEW INSTRUMENT.
- BIND-ASSERT recorder in `auth_middleware.py` - appended, module imports clean, recorded as
  NOT yet wired into serve.py. **BUT** BIND_ASSERT lines ARE appearing in `backend.log` at
  WARNING from `openjarvis.cli.serve`. One of the two records is stale. Still unreconciled
  as of 09/09.
- `patch-debugreadable-v1b.ps1` in the repo root - reusable, hash-anchored, BOM-preserving
  patch harness for `serve.py`. **Do not rebuild this; adapt it.**

**Both standing lessons still apply, and the second now has three proofs:** SEARCH THE
SCHEMA BEFORE BUILDING AN INSTRUMENT, and INSTRUMENTATION YOU CANNOT READ IS INSTRUMENTATION
YOU DO NOT HAVE.

---

## 11. EXECUTION PATH REGISTER

No new execution paths traced this window. Existing register unchanged - see memory
`openjarvis-execution-paths` for the `routes.py` chat dispatch branches (1a/1b/1c/1d), the
orchestrator `ask()` path, and the managed-agent SSE stream.

**W41 addition, relevant to every path in the register:** the observability status of the
three main paths is now known and it is uniformly bad.

| Path | Logger | Status today |
|---|---|---|
| `routes.py` chat dispatch (1a-1d) | `openjarvis.server` | DARK below WARNING. DEBUG at `:102`/`:136`, INFO at `:153` all dropped. |
| Managed-agent SSE stream | `openjarvis.server.agent_manager` | DARK below WARNING. |
| SSE / stream bridge | `openjarvis.server` | DARK below WARNING. |
| Tool execution boundary | `openjarvis.dispatch` | VISIBLE in `dispatch.log`. |
| Agent turn boundary | `openjarvis.agent` | VISIBLE in `agent.log`. |

The STARTUP path traced in W40 is unchanged and confirmed: `start-openjarvis.ps1:31` runs
`python -m openjarvis.cli serve --port 8010`, entering the click group at
`cli\__init__.py:55` (running `setup_logging` at `:62`), then dispatching to `serve()`
registered at `:86`, which calls `_configure_file_logging()` at `serve.py:109` and finally
`uvicorn.Config(...)` at `serve.py:651`. Human present: yes, manual start from the admin
session. No autostart, not a service.

---

## 12. STANDING RULES CHECK

- **ALWAYS VERIFY, never stack on unverified** - held. Nothing was written this window, so
  nothing was stacked. The W40 patch remains unverified at runtime and that is stated
  plainly rather than papered over.
- **FINISH BEFORE STARTING THE NEXT** - held. The `:552` encoding finding was recorded and
  explicitly deferred rather than chased.
- **Shell and host on every command** - held. All commands labelled PowerShell / Windows box
  / from `PS C:\Users\Admin\OpenJarvis>`.
- **No non-ASCII symbols** - held.
- **Working directory `PS C:\Users\Admin\OpenJarvis>`** - held; all reads used absolute
  paths.
- **READ WIDE, NOT IN NARROW SLICES** - corrected mid-window by Gray, then held. New standing
  rule, recorded at 6.2.
- **Design tests to be non-interactive** - n/a this window, no tests run.
- **15-exchange flag** - not reached. Window closed at 8 exchanges by Gray's call to hand off
  fresh.
- **PUSH TO BOTH REMOTES (`origin` = GitHub, `gitlab` = lab instance)** - **STILL NOT DONE.
  CARRIED FORWARD FROM W40 AS OUTSTANDING.** The `serve.py` change and
  `patch-debugreadable-v1b.ps1` remain uncommitted. Stage explicit paths, never
  `git add -A`. The naming is a trap worth restating: `origin` is GitHub, `gitlab` is the lab
  instance.
- **USE THE AUTHOR'S RESOURCES FIRST** - held, and it drove the outcome. The author's
  `setup_logging` and `SanitizingFormatter` are both central to the recommended fix rather
  than being replaced by new code.

---

## 13. ROLLBACK POINTS

No new rollback points created this window - nothing was written. W40's stands and is
registered in `openjarvis-rollback-points-2`:

```
Copy-Item 'C:\Users\Admin\OpenJarvis\src\openjarvis\cli\serve.py.bak_debugreadable_20260908-093533' 'C:\Users\Admin\OpenJarvis\src\openjarvis\cli\serve.py' -Force
```

---

## 14. SDD / SDP FEED FROM THIS WINDOW

**Architecture.** The observability subsystem has THREE distinct configuration regimes
running simultaneously, and no component knows about the others:
1. the CLI click group (`setup_logging`) which owns the `openjarvis` tree and pins it to
   WARNING;
2. the serve command (`_configure_file_logging`) which owns ROOT and the `backend.log`
   handler;
3. three self-configuring subtrees (`dispatch`, `agent`, `retry400`) which opt out of both
   by setting their own level and `propagate = False`.

Regime 3 is why any instrumentation works at all today. **This belongs in the SDD
observability chapter with the full call order and the four-gate model.**

**Decision and evidence.** The decision to fill the author's missing INFO level inside his
own function, rather than add a third configuration authority, rests on two pieces of
evidence gathered in W41: `setup_logging` demonstrably exposes no INFO route (full file
read), and `evals\cli.py` demonstrably does not supply one either (full function read). Both
reads are recorded above with line numbers.

**Hazards for the SDP.** The four-gate model; the UTF-8 BOM in `serve.py`; the .NET
working-directory trap; the `:552` compounding encoding damage as a canary; and the
unredacted `backend.log`. The last one is a security finding, not an observability one, and
should be filed as such.

**PLAIN LANGUAGE (the eight-year-old explanation), for the SDP:**

Imagine the log file is a mailbox, and every part of the program is a person who might post
a letter into it.

There are FOUR ways a letter can fail to arrive, and we have now found all four.

One: the person never actually posts the letter - they just say it out loud in an empty
room. That is `print()`. Nobody hears it.

Two: there is a rule at the post office that says "only send letters marked URGENT." Our
letters were marked ORDINARY, so the post office threw them away before they ever reached
the mailbox. That is the level gate, and it is our main problem.

Three: some people have decided not to use the post office at all. They carry their letters
somewhere else themselves. That is `propagate = False`. Three parts of our program do this,
and funnily enough they are the only three whose letters we have been able to read.

Four - and this is the sneaky one: a person decides not to use the post office, but ALSO
does not carry the letter anywhere. They write it, seal it, and drop it in the bin. Nobody
ever knows. There is no error, no complaint, no missing-mail notice. We think one part of
our program may be doing exactly this, and we need to go look.

The lesson: when you build something to tell you what is happening, check THAT DAY that you
can actually read what it writes. Otherwise you have built a person who writes letters into
a bin.

---

## 15. THE 550B CLOUD MODEL (STANDING, 08/29)

If the next window needs whole files rather than targeted reads, bundle the suspects into
ONE markdown file for Gray to feed to his 550B cloud model (openrouter
nemotron-3-ultra-550b) rather than spending window cycles on piecemeal reads.

**Carried note:** W41 did NOT need this. The four wide reads answered everything except 4.2.
The READ WIDE rule from 6.2 reduced the need for the bundle rather than increasing it - worth
remembering, they are complementary tactics, not competing ones.

**If a bundle IS needed next window, the suggested set is:** `engine\ollama.py` (whole file,
for the retry400 handler question), and `server\routes.py` plus `server\stream_bridge.py` if
the level fix lands and the newly visible output needs interpreting against source.

---

## 16. PROGRAM GOAL AND PROGRESS

Goal: a FUNCTIONAL EXECUTIVE ASSISTANT that performs the duties at a computer a human would.
Approaching one year; not yet 50 percent of initial requirements. Gray needs a way to MEASURE
progress against those requirements. See memory `openjarvis-program-goals`.

**What this window moved toward that goal:** nothing user-facing, and no code changed. What
it produced is the COMPLETE map of why the system cannot be observed - both the working side
and the broken side - which has now blocked four separate windows. The deficient register in
section 4 is the artifact that stops the circling: any future window can look up a logger and
know immediately whether it is expected to produce output and which gate is holding it.

That is infrastructure for velocity, not a feature. It should be counted as such rather than
as progress against the requirement list.

**Honest note, carried and now overdue:** the requirements-measurement problem itself has been
deferred across SEVERAL windows. It is not a debugging task and will not surface naturally
during one. **It needs its own window, and it should be scheduled deliberately rather than
waiting for a gap.**
