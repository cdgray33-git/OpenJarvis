# HANDOFF 2026-08-31 B / WINDOW 24
# THREE SMALL DIFFS READ, COMMITTED AND PUSHED - HYPOTHESES NOW FOUR FOR FOUR WRONG
# Plus: a duplicated bind verdict, an event-loop pin measured at 253 s, three new hazards

Predecessor: HANDOFF-2026-08-31-A-W23-FOUR-COMMITS-PUSHED-HEAD-REPAIRED.md
Host: Windows box. Shell: PowerShell 5.1. Working dir: `PS C:\Users\Admin\OpenJarvis>`.
Backend: 127.0.0.1:8010, ollama, qwen3-coder:30b, agent native_openhands.
Window shape: provenance and commit window, same as W23. Nothing was patched. Nothing was
debugged. Three commits made, all pure provenance - no code behavior was changed by this
window's own actions. The window ended on the 15-exchange flag, not on a stuck problem.

---

## 0. ONE PARAGRAPH FOR THE NEXT WINDOW

The three small unread diffs are CLOSED - `auth_middleware.py`, `routes.py`, `ttsPlayer.ts`
are read verbatim, committed individually, and pushed to both remotes at `746ce84`. All
three W22 hypotheses about them were WRONG, which makes the running tally four for four.
`auth_middleware.py` is the W19 bind assertion, not v3 redaction, and it revealed a
DUPLICATED loopback verdict where the copy every consumer reads is not the copy this diff
adds. `routes.py` is an event-loop offload measured at 253 s of blocking, not the 6c
confirm route, and it turns out to be a PRECONDITION for the Defect 6 gate on the
non-streaming chat branches. `ttsPlayer.ts` is a first-unit chunker bound plus `[PUMPDBG]`
timing, not the 08/05 rewrite. TWO diffs remain unread and both are the mailbox pair.
`mailbox_tools.py` touches destructive paths and was deliberately NOT started at the tail
of this window.

---

## 1. WHAT LANDED - THREE COMMITS

In order, all on `main`:

| Hash | Content | Counts | Verified by |
|---|---|---|---|
| `7ddece9` | `auth_middleware.py` - `record_bind` + `bind_is_loopback` (W19 bind assertion) | 31 ins, 0 del | `status --short` BLANK |
| `aad8ccd` | `routes.py` - `openjarvis-offload-sync-handlers-v1`, both non-streaming branches to `asyncio.to_thread` | 16 ins, 4 del | `status --short` BLANK |
| `746ce84` | `ttsPlayer.ts` - first-unit word-boundary cut + `[PUMPDBG]` timing | 26 ins, 0 del | `status --short` BLANK |

Pushed: `531b270..746ce84` to `origin` AND `gitlab`. Both plain fast-forward, identical
object counts (18 objects, 4.28 KiB). No `--mirror`, no `--force`. Both remotes verified at
`746ce84` in the same exchange the commits were made, so nothing from this window ever sat
on one machine only. That was W22's lesson and it was applied deliberately.

Each commit carries its hazards in the commit message body, not only here. The commit
message is the provenance record that survives independent of the handoff files.

---

## 2. NEGATIVE RESULTS AND CORRECTIONS - PIN THESE

### 2.1 Hypotheses are now FOUR FOR FOUR wrong

| Diff | W22 hypothesis | Actual |
|---|---|---|
| `ollama.py +58` | Patch 4 RAWGEN | Patch 5 retry400 (W23) |
| `native_openhands.py +167` | Defect 1 parser formats | THREE changes; parser is 26 of 167 (W23) |
| `auth_middleware.py +31` | v3 redaction | W19 bind assertion (W24) |
| `routes.py +20` | 6c confirm route | event-loop offload (W24) |

`ttsPlayer.ts` was the only near miss - hypothesized "TTS rewrite", actually a chunker
change plus instrumentation. The rewrite itself was already committed 08/05. Call it
half-right at best; the diff is not what the hypothesis named.

**The standing conclusion is now stronger than W23 stated it.** Do not carry a hypothesis
about an unread diff forward as if it were a finding. The `--stat` line is compatible with
many contents. Only the verbatim diff discriminates. Four consecutive refutations is not
bad luck, it is the method working.

### 2.2 The remaining two line counts are themselves suspect

`mailbox_tools.py +290` and `imap_mail.py +100` are inherited from the W22 handoff. W23
section 2.1 established that two W22 counts were wrong because the `--stat` graph column
was read as an insertion count. These two numbers came from the same pass and have never
been re-derived. **Treat +290 and +100 as unverified.** Take real counts from the
`N insertions(+), M deletions(-)` summary line when the files are opened.

### 2.3 Authoring defect in this window's own output - my error, pinned

At exchange 9 I quoted a JavaScript source line inside a plain fenced block in the same
message as a runnable command. Gray pasted it into PowerShell, which rejected it at parse
time with a `ParserError`. No harm - nothing executed, nothing changed - but it cost an
exchange and it violated the spirit of the standing rule that Gray pastes exactly what he
is given.

**Rule adopted for all future windows: ONE runnable block per message, and quoted source
goes inline or in a block explicitly labeled as source, never in a bare fence that reads
like a command.** This belongs in the SDP verification-methodology chapter alongside the
graph-column error - both are failures of the instrument's presentation, not of its logic.

---

## 3. THE `auth_middleware.py` FINDING - A DUPLICATED BIND VERDICT

`7ddece9` appends three things after `check_bind_safety`:

- `_BIND_IS_LOOPBACK: bool | None` module global
- `bind_is_loopback() -> bool | None` reader, documented as None-means-not-run, which
  callers must treat as unsafe
- `record_bind(host, port, *, api_key) -> bool` which computes the verdict via
  `ipaddress.ip_address(host).is_loopback` with a `ValueError` fallback to
  `host in ("localhost", "")`, stores it, and logs a `BIND-ASSERT` line

Verified live by grep: `record_bind` IS called, at `cli/serve.py:539`. So the W19 claim
that a loopback bind is asserted at startup is TRUE and the SDP threat-model line stands.

### 3.1 HAZARD - the verdict is computed twice and the wrong copy is dead

Grep exposed a split that the diff alone does not show:

- `serve.py:539` calls `record_bind(...)` **and discards the return value**. So
  `_BIND_IS_LOOPBACK` is write-only.
- `serve.py:613-615` **independently recomputes** the identical verdict into a local
  `_is_loop`, using byte-identical logic (`ip_address(...).is_loopback`, same
  `("localhost", "")` fallback).
- `serve.py:620` sets `app.state.bind_is_loopback = _is_loop` - from the DUPLICATE, not
  from `record_bind`.
- Every real consumer reads the `app.state` copy: `agent_manager_routes.py:2167`,
  `ws_bridge.py:101`, and `patch_testexec_v1.py:77`.
- `bind_is_loopback()` the function has **ZERO callers**.

Net: the module-level global, its reader, and its None-means-unsafe contract are entirely
dead code. Consumers use `getattr(..., False)`, which fails closed - that part is correct
and should not be "fixed". Same family as the speech triplication in the pending cloud
bundle: one fact, two definitions, and a fix applied to one copy fixes nothing.

### 3.2 HAZARD - empty host is classified as LOOPBACK, in both copies

`host in ("localhost", "")` treats an empty bind host as safe. An empty bind host is
INADDR_ANY - every interface. That is the exact inversion this instrument exists to detect.
Present in `record_bind` AND in the `serve.py:613-615` duplicate, so it must be fixed in
both or in neither. Recorded, not patched.

### 3.3 Minor - the docstring names the wrong function

`bind_is_loopback`'s docstring credits `check_bind_safety` with recording the verdict.
`record_bind` does it. Suggests the code was split during authoring. It matters because it
points a reader of the None-means-unsafe contract at the wrong place to look.

---

## 4. THE `routes.py` FINDING - AN EVENT-LOOP PIN, AND A GATE PRECONDITION

`aad8ccd`, marker `openjarvis-offload-sync-handlers-v1`. Both non-streaming branches of
`chat_completions` were calling synchronous defs directly from a coroutine:

- `_handle_agent` - **measured**: 253 s of event-loop blocking with 23 consecutive
  `/health` timeouts during a single turn.
- `_handle_direct` - shape-confirmed by the author, not measured.

Both now go through `await asyncio.to_thread(...)`. The in-code comment names
`stream_bridge.py:155` as the same idiom already in use, which is precisely why the
STREAMING path never exhibited this and only the non-streaming path did.

### 4.1 Verified before commit - the positional conversion is safe

The `_handle_direct` call was silently converted from keyword (`bus=bus,
complexity_info=complexity_info`) to positional (`bus, complexity_info`). This was NOT
required - `asyncio.to_thread` forwards `**kwargs` fine - and if the signature had a
keyword-only marker or an intervening parameter it would be a live `TypeError` on every
non-streaming direct-engine turn.

Checked at `routes.py:186-191`: `(engine, model, req, bus=None, complexity_info=None)`. No
`*`, no intervening parameter, order matches exactly. **Safe.** Recorded because a
gratuitous change inside a fix is a review hazard even when it happens to be correct.

### 4.2 THIS IS A DEFECT 6 PRECONDITION - carry into the SDP

The gate blocks a worker thread for up to the 120 s TTL, and the standing threading-model
constraint is that callers must be on `asyncio.to_thread`. Before `aad8ccd`, the
non-streaming chat path was NOT. A confirmation gate raised on `routes.py` dispatch branch
1b or 1d would therefore have blocked the ENTIRE EVENT LOOP for the full TTL, not merely a
worker thread - and the confirm response itself arrives over HTTP `POST /v1/tools/confirm`,
which needs that same loop to be alive to be received. That is a deadlock shape, not just
a latency problem.

`aad8ccd` is therefore not only a performance fix. It is a precondition for the
confirmation gate ever working on the non-streaming chat branches. Nobody framed it that
way when it was written; it was written as a latency fix. State it correctly in the SDP.

---

## 5. THE `ttsPlayer.ts` FINDING - TWO CHANGES

`746ce84`. Not the 08/05 rewrite.

**(1) Behavior change in `splitIntoUnits`.** An oversized FIRST piece is now cut at the last
space within `cap` and the remainder carried into `current`, instead of being emitted
whole. Bounds time-to-first-audio. Guarded by `if (cap < max)`, which is true only while
the first unit is being built - on every later enqueue `firstMax === max`, so the branch
cannot fire after the first. Falls through to the old whole-piece push when the head
contains no space at all.

**(2) `[PUMPDBG]` instrumentation** through the pump loop: `take`, `fetched`, `buffered`,
`ctx`, `decoded`, `scheduled`, with per-stage millisecond deltas, byte size and buffer
duration. Feeds the criterion 4 first-audio work.

### 5.1 Theory raised and killed - no ReferenceError in the pump

The `scheduled` log line at `:277` sits OUTSIDE the try/catch and references `ctx` and
`nextStartTime` while every other line in that function uses the local `context` from
`ensureContext()`. If those were not module-level, the line would throw on the first
scheduled chunk, escape through `finally { pumping = false }`, and kill the pump loop -
instrumentation silently breaking playback.

Grep settles it: `ctx` is module-level at `:49`, `nextStartTime` at `:55`. `ensureContext()`
assigns and returns that same `ctx` (`:82`, `:95`), and `schedule()` reads it via
`const context = ctx` at `:217`. So both `[PUMPDBG]` context lines report ONE object, and
the instrumentation is consistent. Theory dead, killed by reading directly.

---

## 6. WHAT REMAINS UNREAD - TWO DIFFS, BOTH MAILBOX

```
src/openjarvis/connectors/imap_mail.py    src/openjarvis/tools/mailbox_tools.py
```

W22 hypothesis, to be treated as UNRELIABLE given four consecutive refutations: Yahoo
chunk/retry plus redaction. Line counts also unverified per section 2.2.

Procedure that has now worked five times. Repeat it exactly:

1. `git --no-pager diff --stat -- <one file>` then `git --no-pager diff -- <same file>`
2. Read verbatim. Take counts from the summary line.
3. **Grep the identifiers the diff introduces**, before composing the commit. This is what
   turned `auth_middleware.py` from a 31-line append into a duplicated-verdict finding and
   what killed the `ttsPlayer` ReferenceError theory. The diff alone would have shown
   neither. This step is now part of the procedure, not optional.
4. Match against the memory record for that defect, THEN compose the commit.
5. One file at a time. Do not batch. Expect the hypothesis to be wrong.

`mailbox_tools.py` is the largest remaining item and touches DESTRUCTIVE mailbox paths -
`move_to_trash` and the connector call chain. It was deliberately not started at the tail
of W24. **Give it a window with room at the front, not a tail end.** Read it against
`/areas/openjarvis-mailbox-yahoo.md` and `/areas/openjarvis-tool-invocation-defect.md`
before composing anything.

---

## 7. EXECUTION PATHS REGISTER

Standing structure. Carried forward and extended, not re-derived.

### PATHS ALREADY REGISTERED (unchanged this window)

- PATH 1: orchestrator `ask()` via `system\orchestrator.py`
- PATH 2: managed-agent SSE via `_stream_managed_agent()` in `server\agent_manager_routes.py`
  (four auto-approve sites, open item 6 - still the largest outstanding gate item)
- PATH 3: test-execute trigger via `POST /v1/tools/test-execute` - gate LIVE, `confirm_id`
  verified on the wire (W21)
- Frontend submit paths F-A typed, F-B voice, F-C option relay (DEAD - no handler for
  `jarvis-submit-text`)

### TOOL-CALL EXTRACTION ORDER (from W23, unchanged - carried for the SDD)

| Order | Format | Risk |
|---|---|---|
| native | `result["tool_calls"]` from engine, counted as `ntc` in RAWGEN | none - healthy path |
| 1 | action-style, CASE-INSENSITIVE and UNANCHORED | false positive on prose containing `action:` |
| 2 | (still unread) | unknown |
| 4 | OpenHands XML `<function=...>` | shadowed by Format 1 |
| 3 | bare JSON `{"name":..., "arguments":...}` | qwen2.5-coder emits this |

Precedence is an accident of insertion order, not a decision. Audit still owed.

### EXTENDED THIS WINDOW - concurrency posture of the chat dispatch branches

The `routes.py` chat dispatch branches 1a/1b/1c/1d gain a recorded concurrency property:

- **Streaming branches** were already correct - `stream_bridge.py:155` uses the
  `to_thread` idiom.
- **Non-streaming branches (1b/1d)** ran their handlers ON THE EVENT LOOP until `aad8ccd`.
  Agent branch measured at 253 s of blocking. Now offloaded.
- Consequence for the gate: any path that can raise the Defect 6 confirmation gate MUST
  reach it from a worker thread, because the gate blocks for up to the 120 s TTL and the
  resolving `POST /v1/tools/confirm` needs the loop free to be received. Record
  "is this path on a worker thread?" as a standing per-path property in the register,
  alongside "is the gate live/auto-approved/absent?".

### BIND POSTURE - a cross-path property, new

Every path that checks `app.state.bind_is_loopback` (`agent_manager_routes.py:2167`,
`ws_bridge.py:101`, `patch_testexec_v1.py:77`) depends on `serve.py:620`, which is fed by
the DUPLICATE computation at `:613-615`, not by `record_bind`. Record this as a shared
dependency of PATH 2 and the WS transport rather than as a property of any one path.

---

## 8. SDP / SDD FEED

**Architecture - repository integrity.** W23's remediation holds and is extended: three more
commits, all pushed to both remotes in the same window they were made. The underlying
property is still unchanged - no CI, no clean-clone import check, no automated provenance.
But the manual method has now been exercised across two windows and eight diffs, and it
works. State in the SDP that provenance was reconstructed by verbatim diff-reading plus
identifier grep, that the grep step is what produced the two most valuable findings, and
that the method is sound but does not scale.

**Duplicated definitions are a recurring architectural defect, not a one-off.** Three
instances now on record: the speech triplication (pending cloud bundle), the two-bus
EventBus split (resolved), and the bind verdict (section 3.1). Add a named SDP subsection
for it. Common shape: one fact, two computations, consumers reading whichever copy is
wired to `app.state`, and the other copy silently dead. The detection method that works is
grepping the identifier, never reading the definition site.

**Defect 6 confirmation gate - GREAT DETAIL per Gray's standing instruction.** W24 adds:
- **threading model, corrected and sharpened**: the constraint is not merely "callers should
  use `asyncio.to_thread`" - it is that a gate raised from the event loop deadlocks,
  because the resolving HTTP POST cannot be received while the loop is blocked. The
  non-streaming chat branches violated this until `aad8ccd` (section 4.2). Streaming
  never did. This changes the constraint from a performance guideline to a correctness
  requirement and it should be written up that way.
- **registry**: write-once contract, 409 on re-decision, TIMEOUT settable only internally.
  Unchanged.
- **payload**: seven fields; `turn_id` from `CURRENT_TURN_ID`, set by
  `openjarvis-agent-log-v1` - a diagnostic marker load-bearing on the gate payload.
  Unchanged, still a design smell worth naming.
- **transport**: EventBus -> ws_bridge -> bare WS client. Delivery proven W20, payload
  integrity proven W21. Redaction question CLOSED, do not re-open.
- **source integrity**: RESOLVED as of `7442a47`, both remotes.

**Threat model.** Unchanged in substance: an unauthenticated loopback WS subscriber can read
`confirm_id` and answer a gate. `OPENJARVIS_WS_TOKEN` unset so `_ws_authed` is always
False. Deliberate deferral (W17 auth ruling), scope local box only. **Refinement from W24:**
the loopback assertion backing "scope local box only" is real and does run
(`serve.py:539`), but the verdict the consumers actually read comes from the duplicate at
`:613-615`, and BOTH copies classify an empty bind host as loopback. The mitigation is
therefore sound for an explicit `127.0.0.1` bind and unsound for an empty one. Known
accepted risk, now stated precisely.

**Verification methodology chapter - two new entries (running total four):**
3. Grep the identifiers a diff introduces before writing it up. The diff shows what a
   change says; the grep shows whether anything listens. Two of this window's three
   findings came from the grep, not the diff.
4. Presentation of an instrument is part of the instrument. A source line pasted as a
   command cost an exchange (section 2.3). One runnable block per message; label source
   as source.

**Architecture artifacts still owed:** ports, protocols and encoding at each gate, as a
downloadable standalone file for Gray's wiki. **Not produced this window either. Now owed
across FOUR windows.** It has been outranked by diff-clearing every time. Next window
either builds it first or the SDP records that it was consciously deprioritized again -
silent carry-forward is how it got to four.

---

## 9. 550B CLOUD MODEL

Carried forward per the 08/29 pin.

`bundle_for_cloud.py` in the repo root, marker `openjarvis-cloudbundle-v1`. Read-only,
stdlib only, does not import openjarvis. Use it whenever a question needs whole files
rather than targeted reads.

- `--set speech` and `--set prompt` defined, briefs already written.
- `--files <paths> --brief "<question>"` for ad hoc.
- Model: `openrouter/nvidia/nemotron-3-ultra-550b-a55b:free`. Proven on a ~16.7k token
  bundle, 438 s.
- The 120B (`nemotron-3-super-120b-a12b:free`) did NOT read the bundle. One retry still
  owed to separate "did not attach" from "will not consume that size".

**STILL PENDING, NOT SUBMITTED: `CLOUDBUNDLE-speech-20260830-115352.md`** (approx 20,766
tokens), covering `speech_router.py`, `app.py`, `api_routes.py`. Brief asks for every
duplicated definition with CURRENT line numbers, a diff of the copies against each other,
which copy FastAPI routes to versus which one Python globals resolve to, and every case
where those two disagree. **Carried across THREE windows now.**

**Staleness warning, updated.** The bundle was built 08/30. Since then `app.py` moved in
`f53a60d` (W23, the 404 guard, 5 lines) and `routes.py` moved in `aad8ccd` (W24, 16/4) -
`routes.py` is not in this bundle, but if the brief's answer touches request dispatch the
answer will be against a stale tree. **Rebuild before submitting.** Do not submit the
existing file.

**Directly relevant to the brief:** section 3.1 of this handoff is a fourth duplicated
definition, found manually, in `auth_middleware.py` / `serve.py`. Consider widening the
speech brief into a general duplicated-definition sweep, or building a second bundle for
it - the 550B is being asked exactly the right question and the answer class is broader
than speech.

---

## 10. NEXT ACTIONS, ORDERED

1. **`imap_mail.py`** - smaller of the two remaining. Full procedure, section 6, including
   the grep step. Commit on verification.
2. **`mailbox_tools.py`** - LARGEST REMAINING, destructive mailbox paths. Own window, front
   not tail. Read against the mailbox and tool-invocation memory records first. This closes
   the unread-diff backlog entirely.
3. **Push both remotes** once 1 and 2 land. `origin` GitHub, `gitlab` lab instance.
4. **Rebuild and feed `CLOUDBUNDLE-speech`** to the 550B. Rebuild is mandatory, not
   optional - `app.py` has moved twice since the bundle was built. Consider widening to a
   duplicated-definition sweep per section 9.
5. **Architecture artifact** (ports, protocols, encoding at each gate) as a standalone
   downloadable file. Owed four windows. Do this before more diff work or record the
   deprioritization explicitly.
6. **Parser ordering audit** (W23 section 3.1). All four formats in one pass, precedence
   decided deliberately. Format 1's unanchored case-insensitive match shadowing Format 4
   XML is the specific live risk.
7. **Build and feed the second prompt bundle** - `InputArea.tsx`, `useSpeechStream.ts`,
   `MessageBubble.tsx`. Tests transcript accumulation, identifies the
   `jarvis-option-select` dispatcher.
8. **Repo root layout decision**: `scripts/`, `handoffs/`, `.gitignore`, `.gitattributes`
   for the CRLF question - every git command in this window emitted a CRLF warning, which
   is noise that hides real warnings. Delete the stray `"patch_testexec_v1 .py"` with the
   space. Note `patch_testexec_v1.py` (no space) is live and reads
   `app.state.bind_is_loopback`, so check which is which before deleting.
9. **One retry of the 120B** on a bundle, to separate attachment failure from size limit.
10. **Open item 6** - four managed-agent auto-approve sites on PATH 2. Largest outstanding
    confirmation-gate item, untouched for several windows.

---

## 11. STANDING RULES IN FORCE

- ALWAYS VERIFY. Never stack a second change on an unverified first one.
- FINISH THE THING BEFORE STARTING THE NEXT. No dangling processes.
- State shell and host on every command. Default PowerShell on the Windows box; anything
  for the Ubuntu ollama host (172.16.33.200) must be labeled or PowerShell-wrapped ssh.
- Commands must run from `PS C:\Users\Admin\OpenJarvis>` as pasted. If a command needs a
  different path, say so IN THE REQUEST, before it runs. When a file is delivered for
  download, state where it lands and give the command that accounts for that location, in
  the same message.
- **ONE runnable block per message. Quoted source goes inline or in a block labeled as
  source, never in a bare fence.** (New, W24 section 2.3.)
- No non-ASCII symbols in replies.
- Tests must be non-interactive - no test whose success depends on Gray reacting inside a
  time window.
- Pin the detail of every window including negative results.
- Push to both remotes, always. `origin` is GitHub, `gitlab` is
  `http://172.16.33.126/root/openjarvis-desktop.git`.
- Token conservation on working sessions.
- Flag at 15 exchanges, then hand off. A flag, not a stop - never cut a live trace.
- Every handoff carries the SDD/SDP section, the EXECUTION PATHS register, and the 550B
  cloud-model section.

## 12. USEFUL PATHS

- Backend log: `C:\Users\Admin\AppData\Local\OpenJarvis\logs\backend.log`
- Agent log: `%LOCALAPPDATA%\OpenJarvis\logs\agent.log` (2.5MB x4) - RUNSTART/TURN/RUNEND/RAWGEN
- Engine log: `%LOCALAPPDATA%\OpenJarvis\logs\engine.log` (2MB x2) - RETRY400, still at
  179 B, no line has ever fired
- Start: `.\start-openjarvis.ps1` from the repo root. The `.\` is MANDATORY - a stale copy
  in `C:\Windows\System32` is on PATH and shadows it.
- New this window: `BIND-ASSERT` line in the backend log, emitted by `record_bind` at
  startup - `host=`, `port=`, `loopback=`, `api_key_set=`.
