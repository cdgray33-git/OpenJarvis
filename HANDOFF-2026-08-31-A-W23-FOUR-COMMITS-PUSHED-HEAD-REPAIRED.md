# HANDOFF 2026-08-31 A / WINDOW 23
# HEAD REPAIRED AND PUSHED - SIX COMMITS, TWO HYPOTHESES REFUTED
# Plus: Format 4 XML parser found live and uncommitted; two new hazards pinned

Predecessor: HANDOFF-2026-08-30-B-W22-HEAD-IS-BROKEN-EVENTS-ENUM-UNCOMMITTED.md
Host: Windows box. Shell: PowerShell 5.1. Working dir: `PS C:\Users\Admin\OpenJarvis>`.
Backend: 127.0.0.1:8010, ollama, qwen3-coder:30b, agent native_openhands.
Window shape: commit and provenance window. Nothing was patched. Nothing was debugged.
Six commits made. No code behavior was changed by this window's own actions.
The window ended on the 15-exchange flag, not on a stuck problem.

---

## 0. ONE PARAGRAPH FOR THE NEXT WINDOW

W22's headline finding is CLOSED. `events.py` is committed, and `HEAD` now defines the two
`EventType` members that `ws_bridge.py` and `_stubs.py` were already committed against, so
the confirmation path no longer raises `AttributeError` on a fresh clone. The four planned
commits (A/B/C/D) all landed and were pushed to BOTH remotes. Two of the seven unread
diffs were then read in full, and BOTH handoff hypotheses about them were WRONG:
`ollama.py +58` is Patch 5 retry400, not Patch 4 RAWGEN; `native_openhands.py +167` is
THREE separate changes, one of which is a live undocumented behavior change (Format 4 XML
tool-call parsing). Five diffs remain unread. Two new hazards were recorded and
deliberately not chased.

---

## 1. WHAT LANDED - SIX COMMITS

In order, all on `main`:

| Hash | Content | Verified by |
|---|---|---|
| `7442a47` | `events.py` - TOOL_CONFIRM_REQUEST / TOOL_CONFIRM_RESOLVED enum members | `git show HEAD:...` returned both members; had returned nothing before |
| `f53a60d` | `app.py` - SPA catch-all raises 404 for `v1/` and `api/` | `show --stat HEAD`, one file |
| `efc28e4` | `api.ts` + `ChatArea.tsx` - TTS first chunk 90 chars, `[TTSDBG]` lines KEPT | `show --stat HEAD`, two files |
| `cc84aae` | `config.toml` + `fix_interface.ps1` - memory block, System32 path repair | `show --stat HEAD`, two files |
| `6d47d8b` | `ollama.py` - Patch 5 retry400 trap | `log --oneline`, `status --short` BLANK |
| `531b270` | `native_openhands.py` - Format 4 + agent-log + RAWGEN | `log --oneline`, `status --short` BLANK |

Pushed: `dde85c3..cc84aae` to `origin` AND `gitlab`, both plain fast-forward, identical
object counts (28 objects, 4.03 KiB). No `--mirror`, no `--force` - deliberate, given the
08/05 accident. `6d47d8b` and `531b270` were pushed at the end of the window.

### 1.1 The verification pattern that worked

`git status --short -- <file>` returning BLANK means tracked and clean. That is the same
one-line test that exposed the W22 inversion in the first place, and it was used as the
close-out check on every commit here. Cheap, unambiguous, and it asks HEAD a question
rather than the working tree.

---

## 2. NEGATIVE RESULTS AND CORRECTIONS - PIN THESE

### 2.1 The handoff's line counts were wrong, twice

W22 section 2 recorded `app.py` as +6/-1 and `api.ts` as +6/-2. Actual: `app.py` is
+5/-1, `api.ts` is +5/-1. The error came from reading the `6 +++++-` graph column in
`--stat` output as an insertion count. **The graph column is a scaled bar, not a number.**
Content was correct in both cases; only the arithmetic was wrong. Authoring correction for
all future handoffs: take counts from the `N insertions(+), M deletions(-)` summary line.

### 2.2 `ollama.py +58` is NOT Patch 4 RAWGEN - REFUTED

W22 section 2.1 hypothesized RAWGEN. The diff is unambiguously **Patch 5, marker
`openjarvis-retry400-v1`**: two call sites at `ollama.py:102-105` bracketing the silent
`payload.pop("tools", None)` retry, plus three helpers appended after `__all__`. RAWGEN
(marker `openjarvis-raw-gen-v1`) is in `native_openhands.py`. The two patches were applied
on the same day (08/18) to different files, which is how they got conflated.

### 2.3 `native_openhands.py +167` is not one thing - REFUTED

Hypothesized as "Defect 1 parser formats". It is THREE changes (section 3). The parser
hypothesis covers 26 of the 167 lines.

### 2.4 Method note

Both refutations came from reading the diff verbatim, not from the `--stat` line and not
from the handoff's own claim. The `--stat` line would have supported either hypothesis.
Same family as the 08/18 standing note: every theory that died died because something was
read directly.

---

## 3. THE FORMAT 4 FINDING - A LIVE BEHAVIOR CHANGE THAT WAS UNCOMMITTED

Inside `531b270`, at `_extract_tool_call` around line 213:

```
<function=NAME><parameter=KEY>value</parameter></function>
```

A regex pair with `re.DOTALL`, tolerant of `\s*=\s*` malformed spacing and of missing
closing tags via `(?:</function>|\Z)`. Parameter values are `int()`-coerced with a
`ValueError` fallback to string. Emitted by qwen3-coder as CONTENT when native `tool_calls`
do not fire. Without this parser that syntax leaked into the chat as visible backend
prose instead of executing.

**This is a real behavior change and it was sitting unstaged.** Unlike the instrumentation,
losing it would have changed what the product does. It is now committed.

### 3.1 HAZARD - parser ordering, live and untested

Format 4 was inserted AHEAD of Format 3 but BEHIND Formats 1 and 2. Format 1 is already on
record (08/18) as case-insensitive and unanchored, so prose containing `action:` produces a
false-positive tool name and WINS over a legitimate Format 4 XML call. That interaction is
now live and has never been tested. Recorded, not patched - patching it needs the full
format inventory read in one pass, which is a task of its own.

### 3.2 The instrumentation is not purely optional

`openjarvis-agent-log-v1` sets `tools._stubs.CURRENT_TURN_ID`, the ContextVar that supplies
`turn_id` in the Defect 6 confirm payload. **Removing the agent-log instrumentation as
"temporary diagnostic" would strip a field the confirmation gate emits.** The commit
message records this. Do not treat all three markers as equally removable.

### 3.3 Minor gap, recorded

`_oj_run_end` has no call on the exception path at the early-return around :358. A run that
raises writes RUNSTART with no RUNEND. Affects log analysis only, not behavior.

---

## 4. WHAT REMAINS UNREAD - FIVE DIFFS

```
frontend/src/audio/ttsPlayer.ts          src/openjarvis/connectors/imap_mail.py
src/openjarvis/server/auth_middleware.py src/openjarvis/server/routes.py
src/openjarvis/tools/mailbox_tools.py
```

Hypotheses from W22, now to be treated as UNRELIABLE given two refutations out of two
tested: `mailbox_tools.py +290` and `imap_mail.py +100` = Yahoo chunk/retry plus redaction;
`auth_middleware.py +31` and `routes.py +20` = v3 redaction and the 6c confirm route;
`ttsPlayer.ts +26` = TTS rewrite.

Procedure that worked and should be repeated: `git --no-pager diff --stat -- <one file>`
then `git --no-pager diff -- <same file>`, read verbatim, match against the memory record
for that defect, THEN compose the commit. One file at a time. Do not batch. Expect the
hypothesis to be wrong.

`mailbox_tools.py +290` is the largest remaining and touches destructive mailbox paths -
give it a window with room, not a tail end.

---

## 5. EXECUTION PATHS REGISTER

Standing structure. Carried forward and extended, not re-derived.

### PATHS ALREADY REGISTERED (unchanged this window)

- PATH 1: orchestrator `ask()` via `system\orchestrator.py`
- PATH 2: managed-agent SSE via `_stream_managed_agent()` in `server\agent_manager_routes.py`
  (four auto-approve sites, open item 6 - still the largest outstanding gate item)
- PATH 3: test-execute trigger via `POST /v1/tools/test-execute` - gate LIVE, `confirm_id`
  verified on the wire (W21)
- `routes.py` chat dispatch branches 1a/1b/1c/1d
- Frontend submit paths F-A typed, F-B voice, F-C option relay (DEAD - no handler for
  `jarvis-submit-text`)

### EXTENDED THIS WINDOW - tool-call extraction is a path property

The agent turn loop has FOUR ways to produce a tool call, and they are tried in order
inside `_extract_tool_call` (`native_openhands.py` ~:150-240):

| Order | Format | Risk |
|---|---|---|
| native | `result["tool_calls"]` from the engine, counted as `ntc` in RAWGEN | none - this is the healthy path |
| 1 | action-style, CASE-INSENSITIVE and UNANCHORED | false positive on prose containing `action:` |
| 2 | (unread this window) | unknown |
| 4 | OpenHands XML `<function=...>` - NEW, section 3 | shadowed by Format 1 |
| 3 | bare JSON `{"name":..., "arguments":...}` | qwen2.5-coder emits this |

Register this ordering in the SDD. Any path that reaches the agent loop inherits all four,
and the precedence between them is currently an accident of insertion order rather than a
decision.

---

## 6. SDP / SDD FEED

**Architecture - repository integrity, follow-up to W22.** The W22 finding is now
remediated for the confirmation path, but the underlying property is unchanged: OpenJarvis
has no CI, no clean-clone import check, and no provenance record linking hunks to windows.
This window demonstrated the cost concretely - six commits' worth of work, including one
live behavior change, existed only on one machine. State in the SDP that provenance was
reconstructed manually by diff-reading in W22/W23, and that this is not repeatable at scale.

**Caveat to record honestly:** committing `events.py` proves the identifiers exist at HEAD.
It does NOT prove a fresh clone imports cleanly. A real clean-clone import check needs deps
installed and is an unbuilt instrument. Do not overstate the fix.

**Defect 6 confirmation gate - GREAT DETAIL per Gray's standing instruction.** W23 adds:
- registry: write-once contract, 409 on re-decision, TIMEOUT settable only internally
- payload: seven fields; `turn_id` comes from `CURRENT_TURN_ID`, which is set by
  `openjarvis-agent-log-v1` in `native_openhands.py` - **a diagnostic marker is
  load-bearing on the gate payload** (section 3.2). This is new and it is a design smell
  worth naming in the SDP.
- transport: EventBus -> ws_bridge -> bare WS client. Delivery proven W20, payload
  integrity proven W21. Redaction question CLOSED, do not re-open.
- threading model: gate blocks a worker thread up to the 120 s TTL; callers must use
  `asyncio.to_thread`; pool-starvation constraint follows.
- source integrity: RESOLVED as of `7442a47`, pushed to both remotes.

**Threat model.** Unchanged: an unauthenticated loopback WS subscriber can read `confirm_id`
and can therefore answer a confirmation gate. `OPENJARVIS_WS_TOKEN` is unset so `_ws_authed`
is always False. Deliberate deferral (W17 auth ruling), scope local box only, loopback bind
asserted at startup per W19. Known accepted risk.

**Verification methodology chapter - two new entries:**
1. The `--stat` graph column is a scaled bar, not a count. Two handoff errors came from
   reading it as a number (section 2.1). Take counts from the summary line.
2. A stated hypothesis about a diff is not evidence about that diff. Two for two wrong this
   window. The `--stat` line is compatible with many contents; only the verbatim diff
   discriminates.

**Architecture artifacts still owed:** ports, protocols and encoding at each gate, as a
downloadable standalone file for Gray's wiki. Not produced this window. This is now
carried across three windows without being built.

---

## 7. 550B CLOUD MODEL

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
where those two disagree. Built and sitting in the repo root. Feeding it is a next action
and has now been carried across two windows.

**Note for the next bundle:** `app.py` changed this window (`f53a60d`, the 404 guard). If
the pending bundle was built before that commit, its `app.py` copy is stale by five lines.
Rebuild before submitting, or state the staleness in the brief.

---

## 8. NEXT ACTIONS, ORDERED

1. **Read the remaining five diffs**, one file at a time, per the procedure in section 4.
   Start with the small ones (`auth_middleware.py +31`, `routes.py +20`, `ttsPlayer.ts +26`)
   to clear the count, then give `mailbox_tools.py +290` and `imap_mail.py +100` their own
   room. Commit each as it is verified. Push both remotes at the end.
2. **Rebuild and feed `CLOUDBUNDLE-speech`** to the 550B - triplication question, section 7.
   Rebuild first because `app.py` moved.
3. **Build and feed the second prompt bundle** - `InputArea.tsx`, `useSpeechStream.ts`,
   `MessageBubble.tsx`. Tests transcript accumulation and identifies the
   `jarvis-option-select` dispatcher.
4. **Parser ordering audit** (section 3.1). Read all four formats in one pass and decide
   precedence deliberately. Format 1's unanchored case-insensitive match is the specific
   risk.
5. Repo root layout decision: `scripts/`, `handoffs/`, `.gitignore`, `.gitattributes` for
   the CRLF question. Delete the stray `"patch_testexec_v1 .py"` with the space.
6. One retry of the 120B on a bundle, to separate attachment failure from size limit.
7. Open item 6 - the four managed-agent auto-approve sites on PATH 2. Largest outstanding
   confirmation-gate item, untouched for several windows.
8. Architecture artifact (ports, protocols, encoding at each gate) as a standalone
   downloadable file. Owed for three windows now.

---

## 9. STANDING RULES IN FORCE

- ALWAYS VERIFY. Never stack a second change on an unverified first one.
- FINISH THE THING BEFORE STARTING THE NEXT. No dangling processes.
- State shell and host on every command. Default PowerShell on the Windows box; anything
  for the Ubuntu ollama host (172.16.33.200) must be labeled or PowerShell-wrapped ssh.
- Commands must run from `PS C:\Users\Admin\OpenJarvis>` as pasted. If a command needs a
  different path, say so IN THE REQUEST, before it runs. When a file is delivered for
  download, state where it lands and give the command that accounts for that location, in
  the same message.
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

## 10. USEFUL PATHS

- Backend log: `C:\Users\Admin\AppData\Local\OpenJarvis\logs\backend.log`
- Agent log: `%LOCALAPPDATA%\OpenJarvis\logs\agent.log` (2.5MB x4) - RUNSTART/TURN/RUNEND/RAWGEN
- Engine log: `%LOCALAPPDATA%\OpenJarvis\logs\engine.log` (2MB x2) - RETRY400, still at
  179 B, no line has ever fired
- Start: `.\start-openjarvis.ps1` from the repo root. The `.\` is MANDATORY - a stale copy
  in `C:\Windows\System32` is on PATH and shadows it.
