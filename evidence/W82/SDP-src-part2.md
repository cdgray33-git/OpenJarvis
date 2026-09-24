# SDP SOURCE EXTRACT W82 part 2 (deduplicated by section hash)
### [ARCHIVE-W44-2026-09-10.md] 9.2 For the SDP guard chapter - in plain language, as required
**The eight-year-old version.** *The program keeps a list of tools that need passwords - a
weather tool, a search tool, and so on. When it starts up, it counts how many passwords each
tool has, and writes a note in its diary saying "search tool: 1 of 2 passwords". But it only
writes that note if at least one tool actually has a password. If none of them do, there is
nothing to say, so it says nothing. For weeks we thought the diary was broken. The diary was
fine. There was just nothing to write.*
*And the note never contains a password itself - only how many there are. Like writing "I have
3 keys on my keyring" instead of drawing pictures of the keys.*
**The technical version.** `serve.py:553` is a truthiness guard on a list accumulated at
`:546-552`. The list gains an entry per tool only where `get_credential_status()` returns at
least one truthy value. On an install with no configured tool credentials the list is empty and
`:554` is unreachable. The absence of the log line is a correct signal about credential state,
not an observability defect.
**Why this belongs in the guard chapter specifically:** it is the cleanest example in the
codebase of **a guard whose silence is informative.** The distinction the SDP must draw for
every guard it documents is: does this guard's silence mean "condition not met" or "something
broke"? Here it is the former, and six windows were spent partly because that distinction was
never written down. **Every guard documented in the SDP gets an explicit "what does silence
mean here" line.**
### [ARCHIVE-W44-2026-09-10.md] 9.3 For the SDP methodology chapter
Two entries, both from section 4:
- **Proof by elimination against a known-good sibling.** The argument that `:554`'s three
  upstream `sys.exit(1)` gates all passed rests entirely on other `logger.info` calls in the
  same module arriving in `backend.log`. **A working sibling on the same path is a load-bearing
  piece of evidence** and is cheaper than any probe. Worth naming as a technique.
- **External model output is evidence, not instruction.** Section 4.1. The failure mode is
  specific and repeatable: a model given one file reasons correctly within that file and then
  proposes an action that violates environment rules it was never told. The SDP should record
  that cloud analysis is used for **reading**, and that every command it emits is re-derived
  locally against the hard-facts list.
### [ARCHIVE-W44-2026-09-10.md] 9.4 Defect 6 confirmation gate - the standing GREAT DETAIL requirement
Unchanged and unfed this window. The registry, payload, transport and threading model still
need full treatment. **Action 4 is the window that produces it**, now that
`agent_manager_routes.py` and `stream_bridge.py` emit.
---
### [ARCHIVE-W44-2026-09-10.md] 11. PROGRAM GOAL AND THE PROGRESS PROBLEM
**The goal:** a functional executive assistant that performs the duties at a computer that a
human would. Approaching one year. Not yet 50 percent of the initial requirements.
**What W44 moved:** observability and understanding, not capability. `:554` is explained; a
reusable cloud-analysis instrument now exists. **A user cannot do anything today that they
could not do on 09/09.**
**This is the fifth consecutive window with that shape**, and the honest reading is that the
logging work was necessary - Defect 1 and Defect 6 could not be seen without it - but that
"necessary groundwork" has been the answer for six windows running.
**Action 5 exists to break this**, and has now been deferred across many windows despite being
the cheapest item on every list: no code reads, no patches, no restarts. It needs the initial
requirements list, a pass marking each item done / partial / not started, and a number.
**The recommendation to Gray, stated plainly:** run action 5 **before** action 4, not after.
Action 4 is Defect 1 and Defect 6, which is real capability work and probably several windows
of it. Going into that without a measure means the next several windows also cannot say what
they moved. Action 5 is one window, and it is the instrument that makes every window after it
able to answer the question.
**This is a recommendation about ordering, not a change to the list.** The list is Gray's.
### [ARCHIVE-W45-2026-09-10.md] SECTION INDEX
```
 1  WINDOW SUMMARY                      authored this window
 2  PRIMARY TRACE                       authored this window
 3  SECONDARY EVIDENCE                  authored this window
 4  NEGATIVE RESULTS AND REFUTED TESTS  authored this window
 5  HAZARDS FOUND                       authored this window
 6  DIAGNOSTIC TOOLING REGISTER         CARRIED + delta
 7  LOGGING TOPOLOGY                    CARRIED + delta
 8  EXECUTION PATH REGISTER             CARRIED + delta
 9  SDD / SDP FEED                      authored this window
10  550B BUNDLE PATTERN                 CARRIED + delta
11  PROGRAM GOAL                        CARRIED + delta
12  RULES OF ENGAGEMENT                 CARRIED + delta
```
---
### [ARCHIVE-W45-2026-09-10.md] 1. WINDOW SUMMARY
W45 was a pure read window. **No file was modified, no patch was applied, no server was
started or restarted.** Git remains clean at `b4cbd81`. Four of the five carried actions were
worked; three closed permanently and the fourth was re-diagnosed. Every closure was a NEGATIVE
result - the suspected fault did not exist in any of the three cases.
The handoff cost rule was applied for the first time. The scaffold was built in exchange 1 by
sed-extracting sections 6, 7, 8, 10, 11 and 12 verbatim from the W44 archive; only new material
was authored, and it was authored INCREMENTALLY as each action closed rather than retyped at
the end. Carried registers received `CHANGED THIS WINDOW` delta blocks and were never rewritten.
What closed:
- **Action 1** - the `serve.py:554` silence. The `:553` guard is confirmed as the cause by
  direct measurement: all 24 tools in `TOOL_CREDENTIALS` have zero credentials set, so
  `_cred_parts` is empty and the guard is False. `:554` is correct code. The carried
  "UNPROVEN formatter" item closes with it - the line could not have leaked a secret because
  there was no secret to render.
- **Action 2** - `openjarvis.retry400`. Refuted as a gate-4 problem. The tree is a correctly
  built private logger writing `engine.log`, which holds exactly two probe lines from 8/18 and
  nothing since. The instrument is healthy and its code path has not executed in 23 days.
- **Action 3** - rotation. Already proven and nobody had looked. Three rolls sit on disk from
  8/18, 8/24 and 9/3. The "wait for 10 MB" instruction was retired.
- **Action 4** - re-diagnosed, not closed. The six windows of logging work SUCCEEDED. The tree
  is open at INFO, the sink is correct, the formatter is correct, redaction is applied, and
  `routes.py` and `stream_bridge.py` do reach `backend.log`. They are silent because they
  contain six log statements between them across 1,161 lines, four of which are failure-only
  or DEBUG-gated. **There is no suppressor. There are no call sites.** Action 4 is therefore a
  PATCH task, not a read task, and was deliberately not started at exchange 12.
- **Action 5** - untouched, deferred again.
What this window is worth to the program: it ended a search. Several windows have been looking
for something that was swallowing records. Nothing is. That question is now closed and the next
window can spend its whole budget building instrumentation instead of hunting a suppressor.
### [ARCHIVE-W45-2026-09-10.md] 2.2 Action 2 CLOSED - `openjarvis.retry400` is healthy and has never fired
Wide read of `engine\ollama.py` (538 lines, SHA-256
`EAEC3A42CB25A31F44B2B8EB2EAF05B3F4E5EAB4E2B5D423F2AA40827B5AA7FD`), lines 340-538, plus a
bounded call-site search.
- `_oj_r400_logger()` at `:414-435` builds a PRIVATE tree: logger `openjarvis.retry400`,
  `RotatingFileHandler` to `%LOCALAPPDATA%\OpenJarvis\logs\engine.log`, `maxBytes=2 MiB`,
  `backupCount=2`, `setLevel(INFO)`, **`propagate = False`** at `:433`, guarded by an
  `_oj_ready` idempotence flag at `:417`. Falls back to `NullHandler` at `:431` on any failure.
- Emitters `_oj_log_retry400` at `:438` and `_oj_log_retry400_result` at `:460`. Both are
  called - `:104` and `:107`, inside the 400-retry branch. Both wrapped in bare `except: pass`.
- `engine.log` on disk: 179 bytes, TWO lines, both timestamped `2026-08-18 16:07:57`, body
  `probe body: unsupported tools payload` - the synthetic probe that installed the instrument.
CONCLUSION. The gate-4 suspicion carried since W41 is REFUTED. The tree is correctly built,
writable, and readable. It has produced no production records in 23 days because the 400-retry
branch has not executed. This corroborates the 09/02 death of the RETRY400 tools-drop theory
from a second, independent direction.
### [ARCHIVE-W45-2026-09-10.md] 2.3 Action 3 CLOSED - rotation is already proven
`%LOCALAPPDATA%\OpenJarvis\logs` listing: `backend.log` 3,168,396 bytes (9/10 08:12), `.1`
4,194,243 (9/3), `.2` 4,194,303 (8/24), `.3` 4,194,228 (8/18), `.4` 10,485,724 (7/18), `.5`
10,485,731 (7/16). Three distinct rolls in the 4 MiB era plus two in the 10 MiB era. Rotation
works and needs no further confirmation. The carried instruction to wait for a 10 MB crossing
is retired.
Also present in that directory and previously unregistered: `agent.log` 201,629 (9/9),
`dispatch.log` 35,218 (9/3), `memdb_audit.log` 2,276 (7/12), `bindassert_probe.txt` 183 (8/29).
### [ARCHIVE-W45-2026-09-10.md] 2.4 The `backend.log` authority, and the cap round trip
`log_config.py` read WHOLE (93 lines). It is NOT the `backend.log` authority. It configures the
`openjarvis` logger only, and its file handler (`:81-85`, `maxBytes=5 MiB`, `backupCount=3`)
attaches ONLY when `verbose` or an explicit `log_file` is passed, defaulting to
`~/.openjarvis/cli.log` - a different file that nothing in this investigation touches.
`serve.py:48-76` `_configure_file_logging()` IS the authority. Root logger, `handlers.clear()`
at `:72`, `maxBytes=10 MiB`, `backupCount=3`, `encoding=utf-8` at `:61`, `SanitizingFormatter`
imported from `log_config` and applied at `:63-66`, `_TelemetryNoiseFilter` added at `:69`,
`root.setLevel(INFO)` at `:74`. Docstring at `:49-55` records WHY: console writes block the
single-threaded asyncio loop under Windows QuickEdit selection.
CAP HISTORY, from the `.bak` set: 10 MiB / `backupCount=5` on 7/14 and 8/17; 4 MiB /
`backupCount=3` in every backup from `bak-bindassert` through `bak_loglevel_20260909-123056`;
10 MiB / `backupCount=3` now. The change back to 10 MiB was made INSIDE the 9/9 logging patch -
current file `LastWriteTime` 12:30:57 is one second after the `.bak_loglevel` snapshot at
12:30:56, and it is committed at `b4cbd81`.
VERIFIED CLEAN: current `serve.py` SHA-256 matches the W44 carried hash
`64A897F94BD9770DDFC0F707D58BA5D16A7D1BF1C3C42B53E3C04FFA7BC71808` exactly, and
`git diff --stat` on the file is empty. No drift since W44 close.
### [ARCHIVE-W45-2026-09-10.md] 2.5 ACTION 4 - the logging work landed, the instrumentation does not exist
`backend.log` grouped over 2026-09-07 05:02:18 to 2026-09-10 08:33:42, last 20,000 lines,
19,918 parsed. Levels: 19,787 INFO, 129 WARNING, 2 ERROR.
Logger distribution:
```
19744  uvicorn.access
  120  dotenv.main
   20  uvicorn.error
   11  openjarvis.cli.serve
    7  openjarvis.server
    6  openjarvis.skills.parser
    6  httpx
    2  openjarvis.agents.scheduler
    2  openjarvis.server.auth_middleware
```
`uvicorn.access` is 99.1 percent of the file. `openjarvis.server` is SEVEN lines in three days.
WHY, from the source - the three modules are wired CORRECTLY and are nearly silent by
construction:
- `server\routes.py`, 793 lines, FOUR log call sites total, all on logger
  `openjarvis.server` used inline (no module-level logger object): `:102` debug, `:136` debug,
  `:153` info, `:411` error. Root is at INFO, so `:102` and `:136` are gated out. The entire
  chat dispatch path emits ONE informational line.
- `server\stream_bridge.py`, 368 lines, TWO call sites, both on `openjarvis.server`:
  `:193-194` error, `:288-289` warning. BOTH ARE FAILURE-ONLY. A healthy stream emits nothing.
- `server\agent_manager_routes.py`, 2,448 lines, logger is the EXPLICIT name
  `openjarvis.server.agent_manager` at `:21` - a DIFFERENT logger, which appears zero times in
  three days. 6 info sites (`:559`, `:975`, `:1656`, `:1698`, `:1778`, `:1798`, `:1805`), the
  rest warning/error. `_stream_managed_agent` is at `:619`, called from `:1842`. A SECOND
  logger exists in the same file at `:2154` via `__name__`, i.e. two trees in one module.
CONCLUSION. The six windows of logging work SUCCEEDED at what they were doing: tree open at
INFO, correct sink, correct formatter, redaction applied. They did NOT fail. But they routed a
pipe that almost nothing is pouring into. Defect 1 (tool invocation) and Defect 6 (confirmation
gate) have NO log lines on their actual code paths. Observability was necessary and is not
sufficient - the next step is instrumenting the tool-call sites and the gate, which is a PATCH
cycle, not a read cycle.
SECOND-ORDER FINDING. `_TelemetryNoiseFilter` (`serve.py:28-45`) is EXONERATED as a suppressor
- `:39` returns True for any record whose name is not `uvicorn.access`, so it cannot drop
openjarvis records. But its own docstring says the telemetry endpoints were 98 percent of
volume; they are gone and `uvicorn.access` is STILL 99.1 percent. Access logging alone
exhausts the rotation budget. Any real instrumentation added to the tool paths will be
competing with it for the 10 MiB window.
### [ARCHIVE-W45-2026-09-10.md] 3. SECONDARY EVIDENCE - FINDINGS RECORDED AND PARKED
Per A FINDING IS NOT A PRIORITY, none of these were chased and none were added to the list.
- **ZERO CONNECTOR CREDENTIALS ARE PROVISIONED.** All 24 tools in `TOOL_CREDENTIALS` report
  `set=0`, including `email` (EMAIL_USERNAME, EMAIL_PASSWORD) and `web_search`
  (TAVILY_API_KEY). The working Yahoo mailbox path therefore obtains credentials somewhere
  OTHER than `TOOL_CREDENTIALS`. This is a program-goal observation - an executive assistant
  with no provisioned connectors - and it is worth its own window.
- **FOUR `basicConfig` CALLERS EXIST AND ARE UNINVESTIGATED:** `channels\slack_daemon.py:198`,
  `evals\cli.py:168`, `mining\_miner_loop_main.py:224`, `mining\_mps_miner_loop_main.py:304`.
  `basicConfig` touches the root logger. If any of these runs in the server process it would
  contend with `root_logger.handlers.clear()` at `serve.py:72`. Unknown whether any does.
- **THREE LOG FILES HAVE NO REGISTERED PRODUCER:** `agent.log` (201 KB, 9/9), `dispatch.log`
  (35 KB, 9/3), `memdb_audit.log` (2 KB, 7/12). `agent.log` is probably
  `agents\native_openhands.py:544` (`openjarvis.agent`) but that was not confirmed. These are
  EXISTING instruments - search them before building anything new.
- **`backend.log.4` AND `.5` ARE ORPHANED** at 10 MiB each, outside the current
  `backupCount=3` window. 20 MB that will never rotate away.
- **`server\serve.py` IS A 0-LINE FILE** shadowing the name of the real `cli\serve.py`.
### [ARCHIVE-W45-2026-09-10.md] 4.1 What `:554` turned out NOT to be
- NOT a broken log line. NOT a level-gating problem. NOT a sink problem. NOT a formatter
  problem. It is a guarded line whose guard is False.
- NOT a secrets leak, confirmed twice over. W44 established from the source that it logs
  counts (`"web_search: 1/2 keys"`); this window establishes that with zero credentials set
  the line cannot render at all. The `SanitizingFormatter` remains correct to have applied and
  is now unambiguously belt-and-braces rather than a fix.
- The W44 example string `web_search: 1/2 keys` was ILLUSTRATIVE, drawn from the code shape.
  Real state is `web_search 0/1`. Do not treat that example as observed output.
### [ARCHIVE-W45-2026-09-10.md] 4.2 What `openjarvis.retry400` turned out NOT to be
NOT gate-4 gated. NOT misconfigured. NOT unwritable. NOT propagating into the root tree. It is
a correctly built private tree sitting on a code path that has not executed since the probe
that installed it. An empty instrument is not a broken instrument - established by reading the
tree AND the file it writes, not by inference from either alone.
### [ARCHIVE-W45-2026-09-10.md] 4.3 What `backend.log` rotation turned out NOT to be
NOT unconfirmed. Three rolls were already on disk when the carried item said to wait for one.
The item survived several windows because nobody listed the log directory.
### [ARCHIVE-W45-2026-09-10.md] 4.4 A claim I made this window and retracted
Mid-window I asserted from byte counts alone that the cap had been REDUCED to 4 MiB and that
`backend.log` would never reach 10 MB. Reading `serve.py:61` showed the current constant is
10 MiB and the 4 MiB era had ENDED. The byte evidence was real; the direction inferred from it
was backwards. Pinned as a methodology result: artifact sizes date a config, they do not
report the current one.
### [ARCHIVE-W45-2026-09-10.md] 4.5 What the `backend.log` silence turned out NOT to be
NOT a level gate. NOT a sink error. NOT the `SanitizingFormatter`. NOT `_TelemetryNoiseFilter`.
NOT a propagation break. NOT a naming mismatch in `routes.py` or `stream_bridge.py` - both use
`openjarvis.server` and both reach the file. The silence is ABSENCE OF CALL SITES. Six log
statements across 1,161 lines of the two hot modules, four of which are failure-only or
DEBUG-gated. This is the single most useful negative result of the window: it ends the search
for a suppressor, which is what the last several windows were implicitly looking for.
### [ARCHIVE-W45-2026-09-10.md] 5. HAZARDS FOUND
- **`agent_manager_routes.py` USES A DIFFERENT LOGGER NAME.** `openjarvis.server.agent_manager`
  at `:21`, not `openjarvis.server` and not `__name__`. A grep for one name will miss it. It
  also defines a SECOND logger at `:2154` via `__name__`. Two trees, one module.
- **`routes.py` HAS NO MODULE-LEVEL LOGGER OBJECT.** All four sites call
  `logging.getLogger("openjarvis.server")` inline. A search for `logger =` finds nothing there.
- **`server\serve.py` IS 0 LINES.** An empty file shadowing the name of the real
  `cli\serve.py`. Do not read it expecting content and do not confuse the two paths.
- **ACCESS LOGGING WILL DROWN NEW INSTRUMENTATION.** At 99.1 percent of volume, anything added
  to the tool paths rotates out fast. Consider a dedicated sink or an access-log suppression
  before adding volume to root.
- **THE `serve.py` ROLLBACK COMMAND HAS AN UNLABELLED SIDE EFFECT.** Restoring
  `serve.py.bak_loglevel_20260909-123056` reverts `maxBytes` from 10 MiB to 4 MiB along with
  whatever it is meant to undo, because the cap change was made inside the 9/9 patch. The
  worktree is clean at `b4cbd81`, so `git checkout -- src/openjarvis/cli/serve.py` is the
  cleaner restore path for this file. Label the `.bak` as PRE-9/9-PATCH state.
- **`.4` AND `.5` ARE ORPHANS.** `backend.log.4` and `.5` (10 MiB, July) are outside the
  current `backupCount=3` window and will never be rotated away. 20 MB parked on disk forever
  unless deleted by hand.
- **TWO LOG FILES ARE EASILY CONFUSED.** `log_config.py` writes `cli.log` under
  `~/.openjarvis/`; `serve.py` writes `backend.log` under `%LOCALAPPDATA%\OpenJarvis\logs`.
  Reading the wrong module to answer a `backend.log` question has already cost time.
- **`Select-String` HAS NO `-Recurse`.** Pipe `Get-ChildItem -Recurse` into it. Cost one
  exchange this window.
---
### [ARCHIVE-W45-2026-09-10.md] 6.6 CHANGED THIS WINDOW
<!-- ONE LINE PER CHANGE. New instrument, output path verified at build time, or none. -->
- ADDED `probe_cred_parts.py` (repo root, untracked): static credential-state reader. Output
  path is STDOUT of `uv run python`, verified readable at build time - it does not touch the
  logging tree, so no sink question arises. Reusable for any future credential question.
  Prints key NAMES and booleans only, never values.
- REGISTERED `openjarvis.retry400` as READABLE and EMPTY: writes
  `%LOCALAPPDATA%\OpenJarvis\logs\engine.log`, 179 bytes, 2 probe lines from 8/18, no
  production records. Do not rebuild it and do not treat its silence as a defect.
- REGISTERED, PRODUCER UNKNOWN: `agent.log` (201 KB, 9/9), `dispatch.log` (35 KB, 9/3),
  `memdb_audit.log` (2 KB, 7/12), `bindassert_probe.txt` (183 B, 8/29). These are existing
  instruments nobody has claimed - SEARCH HERE BEFORE BUILDING ANYTHING NEW.
### [ARCHIVE-W45-2026-09-10.md] 7.6 CHANGED THIS WINDOW
- **AUTHORITY CORRECTED.** `backend.log` is configured by `serve.py:48-76`
  `_configure_file_logging()`, on the ROOT logger, NOT by `cli\log_config.py`.
- **`log_config.py` READ WHOLE (93 lines) and reclassified.** It configures the `openjarvis`
  logger and writes `~/.openjarvis/cli.log`, attaching a file handler ONLY when `verbose=True`
  or an explicit `log_file` is passed (`:74`). Level from `OPENJARVIS_LOG_LEVEL` at `:51-62`,
  default WARNING. Console handler always attached at `:67-71`.
- **REDACTION QUESTION ANSWERED.** The root `backend.log` handler DOES carry
  `SanitizingFormatter` (`serve.py:63-66`). Both files that apply it are now known.
- **ROOT CAP IS 10 MiB / backupCount=3** (`serve.py:61`), restored from a 4 MiB era inside the
  9/9 patch. Cap history in Archive 2.4.
- **FOURTH PRIVATE TREE FOUND.** `agents\native_openhands.py:552` - `RotatingFileHandler`,
  2.5 MiB, `backupCount=4`, `NullHandler` fallback at `:559`. Sink not yet identified.
- **PRIVATE TREES, FULL SET AS OF W45:** root (`serve.py`, backend.log), `openjarvis`
  (`log_config.py`, cli.log, verbose-only), `openjarvis.retry400` (`ollama.py:414`,
  engine.log, propagate=False), `tools\_stubs.py:119` (2 MiB, backupCount=4, sink TBD),
  `agents\native_openhands.py:552` (2.5 MiB, backupCount=4, sink TBD).
- **FOUR `basicConfig` CALLERS REGISTERED, NONE INVESTIGATED:**
  `channels\slack_daemon.py:198`, `evals\cli.py:168`, `mining\_miner_loop_main.py:224`,
  `mining\_mps_miner_loop_main.py:304`. Any of these running in-process would fight
  `root_logger.handlers.clear()` at `serve.py:72`. OPEN QUESTION, not chased this window.
- **SINK DIRECTORY INVENTORY** (`%LOCALAPPDATA%\OpenJarvis\logs`): backend.log + .1-.5,
  agent.log, dispatch.log, engine.log, memdb_audit.log, bindassert_probe.txt. `agent.log`,
  `dispatch.log` and `memdb_audit.log` have no registered producer yet.
### [ARCHIVE-W45-2026-09-10.md] 8.3 CHANGED THIS WINDOW
- NO new path added. Two carried paths gained an OBSERVABILITY property: the `routes.py` chat
  dispatch path has FOUR log sites total (`:102` debug, `:136` debug, `:153` info, `:411`
  error) on logger `openjarvis.server`, called INLINE with no module-level logger object; the
  managed-agent SSE path (`_stream_managed_agent`, `agent_manager_routes.py:619`, called from
  `:1842`) logs to the SEPARATE logger `openjarvis.server.agent_manager` (`:21`), which has
  produced zero records in three days.
- `stream_bridge.py` emits on `openjarvis.server` at `:193-194` (error) and `:288-289`
  (warning) ONLY - failure-only, nothing on a healthy stream.
- Confirmation-gate state on both paths: UNCHANGED and still UNLOGGED. No instrument exists on
  the gate itself.
### [ARCHIVE-W45-2026-09-10.md] 9.1 For the SDD architecture chapter - the logging subsystem
Five distinct logger trees are now documented with their sinks, caps and encodings:
| Tree | Configured at | Sink | Cap | Backups | Encoding | Formatter |
|---|---|---|---|---|---|---|
| root | `cli\serve.py:60-74` | `%LOCALAPPDATA%\OpenJarvis\logs\backend.log` | 10 MiB | 3 | utf-8 | SanitizingFormatter |
| `openjarvis` | `cli\log_config.py:81-91` | `~/.openjarvis/cli.log` (verbose only) | 5 MiB | 3 | default | SanitizingFormatter |
| `openjarvis.retry400` | `engine\ollama.py:414-435` | `...\logs\engine.log` | 2 MiB | 2 | utf-8 | plain, propagate=False |
| `openjarvis.agent` | `agents\native_openhands.py:544-559` | sink TBD | 2.5 MiB | 4 | utf-8 | plain |
| (tools) | `tools\_stubs.py:119-126` | sink TBD | 2 MiB | 4 | utf-8 | plain |
Transport is the local filesystem in all five cases; no port or network protocol is involved,
which is itself the architectural point - logging has no remote gate. The one architectural
hazard to record is that `serve.py:72` calls `root_logger.handlers.clear()`, making startup
ORDER significant: any handler attached before `_configure_file_logging()` runs is discarded.
### [ARCHIVE-W45-2026-09-10.md] 9.2 For the SDP guard chapter - in plain language, as required
**What a guard is.** Imagine a light switch with a piece of tape over it that says "only flip
this if there is a bulb in the socket." The switch is the log line. The tape is the guard. If
there is no bulb, you never flip the switch, and the room stays dark. Someone walking in and
seeing a dark room might think the switch is broken. It is not broken. It was told not to
work, and it obeyed.
**Our guard.** At line 553 of `serve.py` the program asks a question: "do I have any passwords
or keys saved for my tools?" If the answer is yes, it writes a line saying HOW MANY it has -
never what they are, just the count, like saying "I have 2 keys on my keyring" instead of
showing you the keys. If the answer is no, it writes nothing at all.
**What we found.** We counted. The answer is zero. Not one of the 24 tools has a single key
saved. So the program was right to stay quiet, every single time. For weeks we thought the
quiet meant something was wrong with our ability to see inside the program. The quiet meant
there was nothing to say.
**The lesson for the design package.** Before you decide an instrument is broken, check
whether it was ever supposed to speak. Ask what would have to be TRUE for it to produce
output, then go and measure whether that thing is true. Measuring took one command. Guessing
took five windows.
### [ARCHIVE-W45-2026-09-10.md] 9.3 For the SDP methodology chapter
- **ARTIFACT SIZES DATE A CONFIGURATION, THEY DO NOT REPORT THE CURRENT ONE.** This window I
  inferred from 4 MiB rotated files that the cap HAD BEEN REDUCED, and asserted it. Reading
  the source showed the 4 MiB era had ENDED. The evidence was sound; the direction of
  inference was backwards. Read the constant, then use the artifacts to date it.
- **AN EMPTY INSTRUMENT IS NOT A BROKEN INSTRUMENT.** Distinguishing the two requires reading
  the tree AND the file it writes. Either alone is ambiguous.
- **ABSENCE OF CALL SITES IS A DISTINCT FAILURE MODE FROM SUPPRESSION**, and the two look
  identical from the log file. Count the call sites in the source before hunting a suppressor.
- **BOUNDED SEARCHES SILENTLY TRUNCATE.** A `Select-Object -First 60` cut the logger listing
  before it reached `server\`, and a `-First 70` cut it before `routes.py`. Both cost an
  exchange. When a search is meant to be exhaustive, scope it narrowly enough to be complete
  rather than capping a wide one.
### [ARCHIVE-W45-2026-09-10.md] 9.4 Defect 6 confirmation gate - the standing GREAT DETAIL requirement
No new evidence this window. Carried forward unchanged: registry, payload, transport and
threading model still require full documentation. W45 adds ONE relevant fact - the gate has no
log line on it. Whatever instrumentation is built for Defect 6 next window becomes the primary
evidence source for this chapter, so it should be designed to produce the SDP material, not
only to answer the immediate debugging question.
### [ARCHIVE-W45-2026-09-10.md] 10.1 CHANGED THIS WINDOW
- NOT USED this window. Every question was answerable by targeted wide reads on the Windows
  box; no bundle was built and no cloud call was made. `ask-550b-554.ps1` remains in the repo
  root, untracked and uncommitted, and is still worth committing.
- The W44 rule stands and was reinforced: AN EXTERNAL MODEL'S ANSWER IS EVIDENCE, NOT
  INSTRUCTION. The 550B's W44 analysis of `:554` was CONFIRMED CORRECT this window by direct
  measurement - it read the guard right. Only its proposed test was unsafe. Both halves of
  that judgement are now proven.
### [ARCHIVE-W45-2026-09-10.md] 12. RULES OF ENGAGEMENT
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
### [ARCHIVE-W46-2026-09-10.md] 1. WINDOW SHAPE
W46 was a short window opened on a partially spent budget, on W45's next action 1 exactly as
written: instrument the tool-call sites and the Defect 6 gate, one patch, verified in isolation.
**The list did not change. One action was worked. One patch was applied and statically
verified. No server was started. Nothing was promoted from a finding to a priority.**
The window inverted its own premise twice. It opened intending to BUILD an instrument, found
the instrument already existed, then found that the thing actually missing was different from
what either W45 or the code's own authors appeared to think.
### [ARCHIVE-W46-2026-09-10.md] 2.1 The tool-path instrument already existed and is the right one
Per the standing 09/06 rule - SEARCH FOR THE EXISTING INSTRUMENT BEFORE BUILDING ONE - the
first command of the window listed `dispatch.log` rather than writing code.
`%LOCALAPPDATA%\OpenJarvis\logs\dispatch.log`, 35,218 bytes, last write 2026-09-03 14:13:36.
It carries **paired ATTEMPT / OUTCOME records on every tool dispatch**, on the dedicated
`openjarvis.dispatch` sink with `propagate=False`, which means it is structurally immune to the
`uvicorn.access` volume problem that Brief W45 warned would drown anything added to root.
Observed format:
```
2026-09-02 12:15:00,485 INFO ATTEMPT turn=963c973f-t4 tool=mailbox_find_messages args={...} thread=asyncio_0
2026-09-02 12:15:04,324 INFO OUTCOME turn=963c973f-t4 tool=mailbox_find_messages success=True latency=3.837 timed_out=False
```
Fields already present: turn id with per-turn sequence suffix (`-t1`, `-t2`...), tool name, full
argument digest with truncation already built in (`...TRUNC`), thread name, success, latency,
and `timed_out`. Argument capture is real - the 9/2 records show live `mailbox_find_messages`
and `mailbox_usage_report` calls against `yahoo_main` with folder and sender parameters intact.
**This is the direct instrument for Defect 1.** Defect 1 is "Jarvis claims a completed
destructive action without invoking a tool". An absent ATTEMPT line is proof of non-invocation
from the log alone, with no inference required.
### [ARCHIVE-W46-2026-09-10.md] 2.2 `dispatch.log` producer - the register contradicted itself, and 7.3 was right
W45 Archive 6.6 registered `dispatch.log` as PRODUCER UNKNOWN. W45 Archive 7.3 named the
producer as `openjarvis.dispatch`, built lazily in `tools\_stubs.py`. **7.3 is correct.**
Confirmed at `_stubs.py:111`, `lg = logging.getLogger("openjarvis.dispatch")`, called through
`_get_dispatch_logger()` at `:176` and `:435`. Correct 6.6 on sight; do not re-investigate.
Its silence since 9/3 is **not** a defect and not a gate problem: no server has been started
since. An untouched log on an unstarted server is the expected observation.
### [ARCHIVE-W46-2026-09-10.md] 2.3 The Defect 6 confirmation gate is ALREADY BUILT - W45's Archive 8.3 is STALE
This is the largest correction of the window. Archive 8.3 (W45) states "Confirmation-gate state
on both paths: UNCHANGED and still UNLOGGED. No instrument exists on the gate itself."
Read directly at `_stubs.py:268-357`, the gate is substantially implemented and carries the
6c step 3 marker `openjarvis-confirm-emit-v1` in the source at `:280`:
| Line | What is there |
|---|---|
| `:269` | `if tool.spec.requires_confirmation:` - the gate test |
| `:270` | `if not self._interactive or self._confirm_callback is None:` - the Defect 6 condition, returns a failure ToolResult at `:271` |
| `:281` | imports `openjarvis.core.confirm_registry` |
| `:283-287` | builds args digest and the human-readable prompt |
| `:288-292` | `_cr.register(tool=, agent_id=, turn_id=)` - registry entry created |
| `:294-306` | publishes `EventType.TOOL_CONFIRM_REQUEST` with confirm_id, agent_id, turn_id, tool, args_digest, prompt, expires_at |
| `:307-311` | sets `CURRENT_CONFIRM_ID` contextvar, calls `self._confirm_callback(prompt)`, resets in `finally` |
| `:313-316` | re-reads the registry; falls back to APPROVED/TIMEOUT if no decision recorded |
| `:317-331` | publishes `TOOL_CONFIRM_RESOLVED` with decision, state, created_at, expires_at, and a `reaped` boolean |
| `:332-357` | **three-way outcome split**: DENIED, APPROVED-but-callback-returned-False (explicitly told to report as internal error, not refusal), and TIMEOUT (explicitly told to re-ask rather than report refusal) |
The `reaped` flag and the approved-but-False branch are careful work. The model-facing wording
at `:341-352` is deliberately written to stop the assistant misreporting a timeout as a user
refusal - a Defect 1 adjacent concern already anticipated in the source.
**What the gate does NOT have is a log line.** Every state above goes to the event bus only.
That distinction - instrumented on the bus, silent on disk - is why 8.3 read as "no instrument".
### [ARCHIVE-W46-2026-09-10.md] 2.4 THE ACTUAL DEFECT: seven early returns between ATTEMPT and OUTCOME
`ToolExecutor.execute` logs ATTEMPT at `:176` and OUTCOME at `:435`. Between them the wide read
of `:160-450` found **seven return paths that exit without an OUTCOME line**:
| Line | Early return | Reason it fires |
|---|---|---|
| `:184` | unknown tool | name not in `self._tools` |
| `:194` | invalid arguments JSON | `json.JSONDecodeError` |
| `:207` | security block | `boundary_guard.check_outbound` raised |
| `:230` | capability denied | RBAC `capability_policy.check` False |
| `:257` | taint violation | sink policy `check_taint` |
| `:271` | **gate: no callback** | **the Defect 6 condition itself** |
| `:353` | gate: denied / timeout / internal | `_approved` False |
**Consequence:** an ATTEMPT with no matching OUTCOME was ambiguous across eight causes (those
seven plus an unhandled exception). The log could not answer the question it was built for.
**This is not theoretical - an orphan is already in the file.** `turn=214f0358-t3
tool=mailbox_find_spam`, ATTEMPT at 2026-09-02 12:22:08,696, **no OUTCOME line ever**. The next
ATTEMPT (`-t4`) arrives 18 seconds later, so the process survived. Retroactively unknowable.
### [ARCHIVE-W46-2026-09-10.md] 2.5 THE PATCH - `openjarvis-dispatch-outcome-v1`, APPLIED AND STATICALLY VERIFIED
Applied to `src\openjarvis\tools\_stubs.py` at 2026-09-10 13:14:56 by
`patch-dispatch-outcome-v3.ps1`. 75 insertions, 12 deletions, one file.
**Design.** Not seven scattered edits. `execute` becomes a thin wrapper that logs ATTEMPT,
calls the original body renamed `_execute_inner`, and logs exactly one OUTCOME on every path
including `BaseException` (logged then re-raised). **A future eighth early return is covered
automatically** - the wrapper cannot miss a path it does not know about.
**Reason codes.** A module-level `_outcome_reason(result)` classifies the returned ToolResult by
content prefix, read-only, never mutating it. The OUTCOME line gains `reason=`:
```
OK  TIMEOUT_TOOL  UNKNOWN_TOOL  BAD_ARGS  BOUNDARY_BLOCK  CAPABILITY_DENIED
TAINT_VIOLATION  GATE_NO_CALLBACK  GATE_DENIED  GATE_TIMEOUT  GATE_INTERNAL_ERROR
TOOL_ERROR  EXCEPTION  FAIL_OTHER
```
**The gate becomes observable for free.** `GATE_NO_CALLBACK` is the on-disk signature of
Defect 6. `GATE_DENIED` / `GATE_TIMEOUT` / `GATE_INTERNAL_ERROR` preserve on disk the three-way
distinction the source already draws in `:332-357`, which previously existed only on the bus.
**Verification, non-interactive, no server:** `py_compile` clean; then the classifier exercised
against all twelve outcome strings taken from the actual return sites. **FAILURES: 0.** The
script self-restores its backup on any failure - a path proven by the v1 run, which failed its
own check and restored cleanly.
**NOT YET RUNTIME VERIFIED. No server was started this window. That is next action 1.**
### [ARCHIVE-W46-2026-09-10.md] 3. SECONDARY EVIDENCE - FINDINGS RECORDED AND PARKED
- **The orphaned `mailbox_find_spam` ATTEMPT (2.4)** stays unexplained. Not chased.
- **W45's parked items are unchanged and were not touched:** zero connector credentials across
  all 24 tools; four `basicConfig` callers uninvestigated; `agent.log` and `memdb_audit.log`
  still have no confirmed producer.
- **`_stubs.py` is CRLF and git warns it will be normalized to LF on next touch.** Any future
  whole-file hash comparison on this file must account for that, exactly as the `:554` hash
  work had to.
### [ARCHIVE-W46-2026-09-10.md] 4.1 What the tool path turned out NOT to be
**NOT dark.** W45 concluded the Defect 1 and Defect 6 surfaces had no call sites, which was
true of `backend.log` and led to next action "instrument the tool-call sites". The tool path
was in fact instrumented the whole time, on a different sink, with a better format than
anything that would have been built. **The W45 conclusion was correct about the file it
examined and wrong about the system.** Reading a log for absence proves the absence in THAT
sink only.
### [ARCHIVE-W46-2026-09-10.md] 4.2 What the Defect 6 gate turned out NOT to be
NOT unimplemented. NOT un-instrumented. NOT missing a registry, a payload, or a bus emit - all
three exist and are detailed in 2.3. It is missing ONE thing: persistence of its decisions to
disk. The W45 archive entry claiming no instrument exists on the gate is retired.
### [ARCHIVE-W46-2026-09-10.md] 4.3 What `dispatch.log`'s silence turned out NOT to be
NOT a suppressor, NOT a level gate, NOT a sink fault, NOT an unregistered producer. The server
has not run since 9/3. **Second time in two windows that an empty instrument was nearly
mistaken for a broken one** - W45 hit this with `openjarvis.retry400`. The rule earned there
held here and saved the window.
### [ARCHIVE-W46-2026-09-10.md] 4.4 Two failures that were mine, not the system's
Two patch scripts failed before v3 landed, both on PowerShell-to-Python quoting, both costing
an exchange in a session where the budget was explicitly tight.
- **v1**: multi-line Python passed to `python -c` via a here-string. PowerShell splits it across
  arguments; Python saw an unclosed paren. **The abort-and-restore path worked correctly** and
  returned the file untouched, which is the useful half of the result.
- **v2**: single quotes escaped as `\'`. That is Python/C escaping. **PowerShell escapes a
  single quote by doubling it (`''`)**, and inside a literal here-string needs no escaping at
  all. This failed at PARSE time, so no backup was taken and no edit was attempted.
Neither failure ever left `_stubs.py` in a partial state. **The rule: any Python longer than one
line goes into a file via a literal `@'...'@` here-string, then is run as a file. Never `-c`,
never string concatenation with escapes.**
### [ARCHIVE-W46-2026-09-10.md] 5. HAZARDS FOUND
- **`_stubs.py` IS CRLF AND GIT WILL NORMALIZE IT TO LF.** Warning emitted on the diff this
  window. Whole-file hashes of this file are not stable across a git touch.
- **`python -c` CANNOT CARRY MULTI-LINE SOURCE THROUGH POWERSHELL.** See 4.4.
- **POWERSHELL SINGLE-QUOTE ESCAPING IS `''`, NOT `\'`.** See 4.4.
- **TWO DEAD PATCH SCRIPTS ARE IN THE REPO ROOT**: `patch-dispatch-outcome-v1.ps1` and
  `-v2.ps1`. Both are superseded and neither should be run. Gitignored by `.gitignore:28`
  (`/patch-*.ps1`), so they will not be committed, but they are on disk. Delete them.
- **THE ARCHIVE CAN CONTRADICT ITSELF ACROSS SECTIONS.** 6.6 and 7.3 disagreed about
  `dispatch.log`'s producer for a full window. When two carried sections disagree, resolve it
  from source in one command rather than trusting the more recent entry - the more recent entry
  was the wrong one here.
### [ARCHIVE-W46-2026-09-10.md] 6.7 CHANGED THIS WINDOW (W46)
- **`dispatch.log` PRODUCER CONFIRMED, 6.6 CORRECTED.** `openjarvis.dispatch`, obtained at
  `tools\_stubs.py:111` via `_get_dispatch_logger()`. It is NOT an unclaimed instrument. It is
  the primary tool-dispatch instrument and the direct evidence source for Defect 1.
- **REGISTERED AS READABLE AND LIVE:** `dispatch.log`, 35,218 bytes at window close, last
  production write 2026-09-03 14:13:36. Paired ATTEMPT/OUTCOME per dispatch, dedicated sink,
  `propagate=False`, argument capture with built-in truncation. Immune to the `uvicorn.access`
  volume problem by construction. **DO NOT BUILD A TOOL-PATH INSTRUMENT. EXTEND THIS ONE.**
- **EXTENDED THIS WINDOW:** `openjarvis-dispatch-outcome-v1` in `_stubs.py` - OUTCOME is now
  unconditional on all eight exit paths and carries `reason=<CODE>`. Output path verified at
  build time: same logger, same sink, same formatter as the existing ATTEMPT line, so no new
  sink question arises. Statically verified, NOT yet runtime verified.
- **ADDED, GITIGNORED:** `patch-dispatch-outcome-v3.ps1` (repo root). Anchor-based splicer with
  match-count assertions, BOM and newline preservation, `py_compile` plus classifier
  verification, and self-restore on any failure. The general form worth reusing for future
  `_stubs.py` patches. `-v1.ps1` and `-v2.ps1` are DEAD - delete them.
### [ARCHIVE-W46-2026-09-10.md] 7.7 CHANGED THIS WINDOW (W46)
- **NO LOGGING CONFIGURATION WAS TOUCHED.** No level, sink, formatter, handler or propagation
  change. The 09/09 level work stands unmodified.
- **THE `openjarvis.dispatch` TREE IS PROMOTED FROM SINK-TBD TO FULLY CHARACTERIZED.** Built in
  `tools\_stubs.py` (logger at `:111`, handler at `:119`, 2 MiB, backupCount=4,
  `propagate=False`), sink CONFIRMED as `%LOCALAPPDATA%\OpenJarvis\logs\dispatch.log`. The W45
  table row reading "(tools) ... sink TBD" is now answered.
- **CONSEQUENCE FOR THE SDD TABLE IN 9.1 (W45):** four of the five trees now have confirmed
  sinks. Only `openjarvis.agent` (`native_openhands.py:544-559`, 2.5 MiB, backupCount=4)
  remains sink-TBD, and `agent.log` at 201 KB is the obvious candidate - unconfirmed, not
  chased.
- **`propagate=False` ON THE DISPATCH TREE IS A FEATURE HERE, NOT A HAZARD.** It is precisely
  what keeps tool-dispatch records out of the `uvicorn.access`-dominated 10 MiB root window.
  Any future instrumentation of a hot path should follow this pattern rather than adding to root.
### [ARCHIVE-W46-2026-09-10.md] 8.4 CHANGED THIS WINDOW (W46)
- **NO NEW PATH ADDED.** The dispatch chain inside `ToolExecutor.execute` is now fully ordered
  and documented in section 9.1 - it is a property shared by ALL paths that own a
  `ToolExecutor`, not a path of its own.
- **GATE STATE CORRECTED FOR THE REGISTER.** The gate is IMPLEMENTED (`_stubs.py:268-357`,
  marker `openjarvis-confirm-emit-v1`), publishes `TOOL_CONFIRM_REQUEST` and
  `TOOL_CONFIRM_RESOLVED`, and registers with `core.confirm_registry`. The W45 entry
  "gate ... still UNLOGGED, no instrument exists on the gate itself" was HALF right: no DISK
  record existed, but bus instrumentation and a registry did. As of this window the gate's
  four outcomes write distinct reason codes to `dispatch.log`.
- **THE PER-PATH QUESTION IS NOW EMPIRICALLY ANSWERABLE.** Which `ToolExecutor` serves a path
  and how it was constructed - specifically whether `confirm_callback` is None and whether
  `interactive` is False - no longer needs to be traced by reading constructors. Any path that
  hits a confirmation-requiring tool with a dead gate now writes `reason=GATE_NO_CALLBACK`
  with its `turn=` id. **Running one confirmation-requiring tool on each path fills in the
  register's gate column directly.** That is the cheapest route to the column that has been
  blank since the register was created.
- **THREADING MODEL RECORDED FOR EVERY PATH:** one-worker `ThreadPoolExecutor` per call at
  `:370`, `future.result(timeout=)` at `:372`, and **timeout abandons rather than cancels**
  (`:380-392`). Applies to every execution path that dispatches a tool.
### [ARCHIVE-W46-2026-09-10.md] 9.1 For the SDD architecture chapter - the tool dispatch path
`ToolExecutor.execute` (`tools\_stubs.py`) is now documented end to end as an ordered gate
chain. Every stage can terminate the dispatch, and after this window **every termination is
recorded on disk with a distinct reason code.** Order is significant and is as follows:
| Order | Stage | Line | Terminates with |
|---|---|---|---|
| 1 | tool lookup | `:182-188` | `UNKNOWN_TOOL` |
| 2 | argument parse | `:191-198` | `BAD_ARGS` |
| 3 | boundary guard (external tools only) | `:201-211` | `BOUNDARY_BLOCK` |
| 4 | RBAC capability check | `:214-238` | `CAPABILITY_DENIED` + bus `CAPABILITY_DENIED` |
| 5 | taint / sink policy | `:240-266` | `TAINT_VIOLATION` + bus `TAINT_VIOLATION` |
| 6 | **confirmation gate** | `:268-357` | `GATE_*` + bus `TOOL_CONFIRM_REQUEST` / `RESOLVED` |
| 7 | execution with timeout | `:366-398` | `OK`, `TIMEOUT_TOOL`, `TOOL_ERROR` |
Architecturally notable, for the design package:
- **The security stages run BEFORE the confirmation gate.** A capability-denied or taint-blocked
  call never reaches a human. The gate is the last stage, not the first.
- **Execution is on a one-worker `ThreadPoolExecutor` per call** (`:370-372`), with
  `future.result(timeout=...)`. **A timeout abandons the future; it does not cancel the work.**
  The source says so plainly at `:383-388` and sets `outcome_verified = False` at `:392`. This
  is the threading model the Defect 6 SDP chapter requires, and it is a real property: after a
  timeout the tool may still be running and may still complete.
- **Transport at each gate is in-process only.** Registry is a Python module (`core
  .confirm_registry`), payload is a dict on the event bus, correlation is the `CURRENT_CONFIRM_ID`
  and `CURRENT_TURN_ID` contextvars. No port, no wire protocol, no serialization boundary except
  `_json_safe_metadata` at `:443`, which strips non-JSON-serializable values (currently
  `TaintSet`) before they reach bus subscribers and the trace store.
### [ARCHIVE-W46-2026-09-10.md] 9.2 For the SDP guard chapter - in plain language, as required
**What the gate is.** Think of a door with a guard standing at it. Some rooms you can walk into
on your own. Some rooms have a sign that says "ask first". When the assistant wants to go into
an "ask first" room, the guard stops it and asks you.
**What can happen at that door.** Four things, and telling them apart is the whole point.
You can say **yes**, and it goes in. You can say **no**, and it does not. You can say nothing
at all until the guard gives up waiting - and that is **not the same as saying no**, because you
never actually answered. Or **there might be no guard on duty at all**, in which case the
assistant is turned away even though nobody ever decided anything.
**Why it matters that these look alike.** If the assistant treats "you never answered" as "you
said no", it will come back and tell you that you refused something you never even saw. The
program already knows this - the message it writes for a timeout says, in effect, *ask the
person again, they did not deny it*. That care was already in the code.
**What we fixed today.** The guard was writing all of this down on a whiteboard that gets wiped
when the room empties, and nothing in the permanent notebook. So the next morning you could not
tell whether the door had been opened, refused, timed out, or left unguarded. We did not change
the guard. We gave it a pen and the notebook, so each of those four now writes a different,
permanent line.
**The lesson for the design package.** Distinguishing "no" from "no answer" from "no guard" is
not a nicety. Each demands a different response from the assistant, and if they collapse into a
single failure the assistant will confidently tell the user something untrue about their own
decision.
### [ARCHIVE-W46-2026-09-10.md] 9.3 For the SDP methodology chapter
- **AN ABSENCE PROVEN IN ONE SINK IS NOT AN ABSENCE IN THE SYSTEM.** W45 proved there were no
  call sites in `backend.log` and concluded the tool path was uninstrumented. A dedicated sink
  with better records existed. Before concluding a thing is unrecorded, enumerate the sinks.
- **A CARRIED REGISTER CAN GO STALE AND STILL LOOK AUTHORITATIVE.** Archive 8.3 asserted the gate
  had no instrument; the gate had a registry, two bus events and a three-way decision split.
  Carried sections describe the system as of when they were written, not as of now.
- **WHEN TWO CARRIED SECTIONS DISAGREE, RESOLVE FROM SOURCE, NOT BY RECENCY.** 6.6 versus 7.3 on
  `dispatch.log`; the newer entry was the wrong one, and one `Select-String` settled it.
- **PREFER ONE STRUCTURAL EDIT OVER N SCATTERED ONES.** Seven early returns could each have
  gained a log line. A wrapper covers all seven, cannot miss the eighth, and is one thing to
  verify and one thing to roll back.
- **A VERIFIER THAT FAILS IS EVIDENCE THE ABORT PATH WORKS.** The v1 failure was self-inflicted
  and still produced a real result: backup, detect, restore, clean tree.
### [ARCHIVE-W46-2026-09-10.md] 9.4 Defect 6 confirmation gate - the standing GREAT DETAIL requirement
**Substantially advanced this window.** Registry, payload and transport are now documented in
9.1 and 2.3 from source, and the threading model is documented in 9.1. Remaining for the
chapter: what `core\confirm_registry.py` actually stores and how entries are reaped (states
APPROVED / DENIED / TIMEOUT and `expires_at` are known only by their use at the call site, not
from reading the registry itself), and who supplies `confirm_callback` on each execution path.
That second question is the same one as execution-path executor construction in section 8, and
the `GATE_NO_CALLBACK` reason code now answers it empirically per path once the server runs.
### [ARCHIVE-W46-2026-09-10.md] 11.2 CHANGED THIS WINDOW (W46)
- **W46 IS THE SEVENTH CONSECUTIVE OBSERVABILITY WINDOW - BUT IT CLOSED THE BUILD.** W45 ended
  the observability INVESTIGATION; W46 shipped the patch that investigation called for. The
  instrument required to see Defect 1 and Defect 6 now exists and is verified short of runtime.
- **CAPABILITY MOVED: none.** A user cannot do anything today they could not do on 09/09.
- **BUT THE NEXT WINDOW CAN MOVE CAPABILITY FOR THE FIRST TIME IN SEVEN.** Defect 1 is
  "claims a completed destructive action without invoking a tool" - a correctness defect in the
  assistant's core promise. With paired ATTEMPT/OUTCOME and reason codes on disk it is
  diagnosable rather than arguable. That is the return on seven windows.
- **ACTION 5 (requirements measurement) REMAINS UNRUN - EIGHTH DEFERRAL.** The argument to run
  it before the Defect 1 work is unchanged and unweakened. It remains the cheapest item on the
  list: no code reads, no patches, no restarts, one window, and it is the only thing that will
  let the windows after it state what they moved.
- **THE CREDENTIAL GAP IS STILL THE LARGEST UNADDRESSED PROGRAM-GOAL FACT.** Zero connector
  credentials across 24 tools. Nothing this window changed that, and nothing on the list
  addresses it.
### [ARCHIVE-W46-2026-09-10.md] 12.2 CHANGED THIS WINDOW (W46)
- **SEARCH THE SINKS BEFORE BUILDING AN INSTRUMENT** (W46). Extends the 09/06 rule. An absence
  proven in one log file is an absence in that file only. `dispatch.log` had the right records
  in a better format than anything that would have been built, and one listing command found it.
- **A CARRIED REGISTER DESCRIBES THE SYSTEM AS OF WHEN IT WAS WRITTEN** (W46). Archive 8.3 said
  the gate had no instrument; the gate had a registry, two bus events and a three-way decision
  split. When a carried claim is load-bearing for the window's plan, verify it from source
  before acting on it.
- **WHEN TWO CARRIED SECTIONS DISAGREE, RESOLVE FROM SOURCE, NOT BY RECENCY** (W46). The newer
  entry was the wrong one.
- **ANY PYTHON LONGER THAN ONE LINE GOES TO A FILE VIA A LITERAL `@'...'@` HERE-STRING, THEN
  RUNS AS A FILE** (W46). Never `python -c` through PowerShell; never escaped-quote string
  concatenation. Two exchanges lost. PowerShell escapes a single quote by DOUBLING it.
- **ONE STRUCTURAL EDIT BEATS N SCATTERED ONES** (W46). One wrapper covered seven early returns
  and covers the eighth nobody has written yet. One thing to verify, one thing to roll back.
### [ARCHIVE-W47-2026-09-10.md] 1. WINDOW SHAPE
ONE SUBJECT: W46 Brief next-action 1, runtime-verify `openjarvis-dispatch-outcome-v1`. Nothing
else was worked. Nothing was promoted. The scaffold was built in exchange one per the 09/10
handoff-cost rule and this archive is assembled onto it by extraction.
Result in one line: **the patch is half-verified and MUST NOT BE COMMITTED.** `reason=OK` is
proven faithful on the success path. `reason=GATE_TIMEOUT` is proven UNFAITHFUL against the
source on the gate path. The window ends on an open, well-characterised contradiction rather
than a green check, and that is the correct outcome.
Exchange count ran to 27. The 15-flag was raised at 14 and again at 16; per standing rule a
live trace was not cut to write the handoff.
### [ARCHIVE-W47-2026-09-10.md] 2.1 The success path - VERIFIED
Baseline before any call: `dispatch.log` 35218 bytes, 228 lines, last write 2026-09-03
14:13:36. Every pre-existing OUTCOME line lacks a `reason=` field, which is what makes the
new field self-proving: its presence identifies the patched code as the code that ran.
Call: `POST /v1/chat/completions`, model `qwen3-coder:30b`, prompt instructing a calculator
tool call. HTTP 200.
```
2026-09-10 13:54:20,835 INFO ATTEMPT turn=87dbc294-t1 tool=calculator args={"expression": "8347 * 291"} thread=asyncio_0
2026-09-10 13:54:20,841 INFO OUTCOME turn=87dbc294-t1 tool=calculator success=True latency=0.006 timed_out=False reason=OK
```
228 -> 230 lines. Exactly one pair. `reason=OK` present. **The wrapper is live and the success
path is faithful.** This result stands and is not disturbed by anything in 2.3.
### [ARCHIVE-W47-2026-09-10.md] 2.3 The gate path - THE CONTRADICTION
Call: `test-execute` on `shell_exec`, args `{"command":"echo openjarvis-gate-probe"}`. Chosen
because it is the ONLY live tool declaring `requires_confirmation`, and because it parks before
executing so nothing runs unless approved. Response was immediate 200 `{accepted:true,
run_id:4027ae9a, turn_id:test-4027ae9a}`.
```
2026-09-10 14:08:49,626 INFO ATTEMPT turn=test-4027ae9a tool=shell_exec args={"command": "echo openjarvis-gate-probe"} thread=asyncio_0
   [ 120 seconds, no OUTCOME - orphan ATTEMPT observed deliberately ]
2026-09-10 14:10:49,632 INFO OUTCOME turn=test-4027ae9a tool=shell_exec success=False latency=120.007 timed_out=False reason=GATE_TIMEOUT
```
Two things were established and one was broken:
1. **The orphan-ATTEMPT ambiguity is closed.** An ATTEMPT with no OUTCOME now means a live wait,
   reproduced deliberately with a known cause. The 9/2 orphan
   (`214f0358-t3 mailbox_find_spam`, 12:22:08) is explainable by this shape.
2. **`timed_out=False` alongside `reason=GATE_TIMEOUT` correctly distinguishes a GATE timeout
   from a TOOL timeout** - the distinction `confirm_registry.py:21-23` insists must stay
   distinct. The instrument preserves it on disk.
3. **But the reason is wrong.** The full source argument is in 8.5. Summary: the executor that
   served this call is built with `interactive=False` and `confirm_callback=None`, so
   `_stubs.py:338` should have returned immediately with the no-callback result. It blocked
   120.007 s instead - matching `_DEFAULT_TTL = 120.0` exactly. The instrument reported a
   terminal path the code says cannot have been taken.
### [ARCHIVE-W47-2026-09-10.md] 2.4 Why this was caught
It was caught because Gray refused to commit on two separately-verified halves and demanded the
full designed path - dispatch, human decision, execution, one coded outcome - end to end. Chasing
that requirement is what forced the read of the callback wiring, which is where the
contradiction surfaced. A commit on the half-results would have shipped an unfaithful `reason=`
field as ground truth into every window after this one.
### [ARCHIVE-W47-2026-09-10.md] 3. SECONDARY EVIDENCE - FINDINGS RECORDED AND PARKED
- **`OPENJARVIS_API_KEY` EXISTS AND IS UNVERSIONED.** 12 characters, set at Windows **User**
  level, inherited by every shell including the server's. SHA-256 fingerprint prefix
  `B1F66AA40A99` (recorded for identity without the secret). It is in NO repo file: not `.env`
  (which holds GITLAB_TOKEN, WIKI_JS_API_TOKEN, Netbox_Token, API_TOKEN_PEPPERS,
  API_TOKEN_PEPPER_1, Portainer_API_Token and a Gmail OAUTH block, none of them this), not
  `config.toml` (no `[server.auth]` section at all), and not `start-openjarvis.ps1` (which sets
  only PYTHONUTF8, PYTHONIOENCODING, HOME and OPENJARVIS_LOG_LEVEL). `cli\serve.py:524` reads
  the env var, then falls back to `config.toml [server][auth][api_key]` at `:534`. **The auth
  layer's sole credential has no reproducible source.** Config-reproducibility finding, SDP
  security-chapter finding.
- **`config.toml` SAYS `host = "0.0.0.0"` BUT THE SERVER BINDS 127.0.0.1.** `check_bind_safety`
  at `cli\serve.py:540` is what forces it; `auth_middleware.py:71` states a non-loopback bind
  REQUIRES the key. The effective bind disagrees with the declared config. Not investigated.
- **`OPENJARVIS_TEST_EXEC=1` IS NOW PERMANENTLY SET AT USER LEVEL ON THIS BOX.** Set during this
  window to enable the probe. It enables `test-execute` on every future start. **Decide whether
  it belongs scoped to a session inside `start-openjarvis.ps1` instead.** Left as-is
  deliberately so the next window can re-run the probe without a restart.
- Carried from W46, untouched: the 9/2 orphan ATTEMPT (now explainable, see 2.3); zero connector
  credentials across 24 tools; four `basicConfig` callers; `agent.log` / `memdb_audit.log`
  producers.

