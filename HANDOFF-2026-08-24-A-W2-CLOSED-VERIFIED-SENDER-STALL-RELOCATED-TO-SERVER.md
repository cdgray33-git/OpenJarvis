# HANDOFF - 2026-08-24 SIXTH WINDOW
# W2 APPLIED AND VERIFIED. THE SENDER STALL IS NOT IN THE PROBE - IT IS SERVER-SIDE.
# NEW HAZARD: A PATCH REPORTED SUCCESS AND DID NOT LAND. NOTHING LEFT RUNNING.

Supersedes `HANDOFF-2026-08-23-E-W1-ROOT-CAUSED-AND-CLOSED-W2-CHARACTERIZED-READY-TO-PATCH.md`
for state. Everything in that file stands EXCEPT the W2 entry and the probe-v3 attribution of the
sender stall, both corrected below. Its sections 5, 7, 8, 9, 10, 11 are CARRIED FORWARD; only
deltas are restated here.

**Actions this window: one source patch applied and verified (W2), one filesystem integrity
investigation, one read-only inventory of `ws_probe.py`, one new standalone instrument built and
run. Backend restarted twice by Gray via `.\start-openjarvis.ps1`.**

---

## 0. STANDING RULES FOR THE NEXT WINDOW

Rules 1-10 from the prior handoff carry forward UNCHANGED. One addition, earned this window:

11. **HASH THE TARGET AFTER EVERY PATCH, AND HASH IT AGAIN AFTER ANY RESTART.** A patch script
    reporting "written" is NOT evidence the change is on disk. See section 3. This costs one
    command and it caught a silent no-op today.

---

## 1. W2 - APPLIED, VERIFIED, CLOSED

Guard added to the SPA catch-all in `src\openjarvis\server\app.py`. Two edits, one logical change:

- line 9: `from fastapi import FastAPI` -> `from fastapi import FastAPI, HTTPException`
- inside `spa_catch_all`, before the existing `if full_path:`:

```python
            # W2: never mask the API surface with the SPA index. Unmatched
            # /v1/* and /api/* paths must 404, not return 200 text/html.
            if full_path.startswith(("v1/", "api/")):
                raise HTTPException(status_code=404, detail="Not Found")
```

`full_path` does arrive WITHOUT a leading slash - the prior handoff's open question is now
answered by the passing verification.

**VERIFIED after a real restart, all four criteria:**

```
/v1/no_such_route_zzz  404  (non-200)      was 200 text/html 849 bytes
/v1/agents/events      404  (non-200)      was 200 text/html 849 bytes
/v1/sessions           200  application/json  69 bytes   unchanged
WS STATE: Open                                            unchanged
```

`/v1/agents/events` returning 404 to a plain GET is CORRECT: a GET without upgrade headers cannot
match a websocket route. The WS handshake itself is unaffected, proven by `WS STATE: Open` in the
same command.

File after patch: 13776 bytes, hash `8B2A7A0DB2CF7C5D1F40A597551DEC6204FF3ED66072F6DDF3F6BC8EB5D15BCC`.
Hash re-checked after the restart and unchanged.

**W2 STATUS: CLOSED.** Blast radius validated empty in the prior window and confirmed empty in
practice - `/v1/sessions` byte-identical before and after.

---

## 2. NEW ACTIVE ROLLBACK POINT

```
Copy-Item 'src\openjarvis\server\app.py.bak-20260824-081250' 'src\openjarvis\server\app.py' -Force
```

(`app.py.bak-20260824-074322` is byte-identical to it; either restores the pre-W2 file. Restart
required after either.)

Prior rollback points from section 5 of the last handoff remain active and untouched:

```
Copy-Item 'src\openjarvis\server\routes.py.bak-20260823-081543' 'src\openjarvis\server\routes.py' -Force
Copy-Item 'ws_probe.py.bak-20260823-091118' 'ws_probe.py' -Force
Copy-Item 'ws_probe.py.bak-20260823-092152' 'ws_probe.py' -Force
Copy-Item 'ws_probe.py.bak-20260823-095318' 'ws_probe.py' -Force
```

---

## 3. NEW HAZARD, HIGH - A PATCH REPORTED SUCCESS AND DID NOT LAND

**This is the most important finding of the window and it is UNEXPLAINED.**

The W2 patch script ran at 07:43:22. It reported: both anchors matched exactly once, temp file
compiled OK, backup created, `written: src\openjarvis\server\app.py`. The backup file WAS created
in that directory. **The target file was not changed.** Confirmed afterwards by three independent
signals:

- target and its own backup had IDENTICAL SHA256 (`4A9C60C0...`), 13486 bytes
- target mtime still 6/7/2026, not 08/24
- `git status --short` did NOT list `src/openjarvis/server/app.py` as modified

Filesystem was then proven healthy at that exact path: no reparse point, `Archive` attribute only,
clean directory chain, and a scratch file written into
`src\openjarvis\server\` persisted with a correct mtime.

A backend restart happened at 07:46:10, between the reported write and the check.

**Re-running the identical script at 08:12:50 landed correctly** - 13776 bytes, new hash, and it
survived a subsequent restart. Same script, same inputs, opposite outcome.

**What is ruled out:** the script's logic (it worked unchanged on the second run), the filesystem,
directory permissions, a git checkout, a reparse point or symlink, and startup reverting `src`
(the second patch survived two restarts).

**What is NOT ruled out and needs a decision next window:** whether the first invocation wrote to
a redirected location (Windows virtualization/redirection), whether some editor or sync process
held and rewrote the file, or whether the first run silently failed after its success print. The
first backup exists and is byte-identical to the original, which is consistent with the backup
step succeeding and the final write step not taking effect.

**Operational consequence, effective immediately:** no prior "patch applied" claim in ANY previous
handoff is evidence unless a hash or a behavior test confirmed it. **Rule 11 exists because of
this.** This belongs in the SDP under the operator-surface / evidence-quality heading.

---

## 4. THE SENDER STALL IS SERVER-SIDE, NOT PROBE v3

The prior handoff carried: "v3's sender thread can stall hundreds of seconds before the POST
leaves." **The attribution to v3 is now contradicted by measurement.**

New instrument built this window: `post_timing_probe.py`, in the repo root. Raw socket, no urllib,
no threads, no asyncio, no websockets - **shares nothing with `ws_probe.py`**, which is the whole
point. It timestamps socket create, TCP connect, request-bytes-sent, first response byte, headers
complete, body complete, so a stall lands in a named gap instead of one opaque number.

Two consecutive runs, PATH 1a, trivial prompt, `qwen3-coder:30b`:

```
RUN 1   socket 0.002s   connect 0.001s   send 0.000s   send->first byte  22.676s   body 0.001s
RUN 2   socket 0.000s   connect 0.000s   send 0.001s   send->first byte   0.565s   body 0.001s
```

Both returned `HTTP/1.1 200 OK`, `finish_reason stop`, content `ping`, 946 bytes.

**Three conclusions:**

1. **The request leaves the client in ~23 ms.** There is no client-side sender stall on this path.
   v3's own machinery cannot be the cause of a wait that reproduces without any of it.
2. **The wait is entirely `send -> first byte`** - the server accepted the request and did not
   begin the response. That is server-side by definition.
3. **40x variance between two identical back-to-back requests.** First slow, second fast, is a
   cold-start signature - model load into VRAM on the ollama host, or a lazily constructed
   component cached after first use.

**NOT YET CLAIMED:** that this cold-start effect explains v3's much larger stall. The magnitudes
differ by an order of magnitude. It may be the same mechanism at a different scale, or two
separate things. **Do not merge them in the record until measured.**

**Instrument note:** `post_timing_probe.py` is non-interactive, runs to completion, leaves nothing
running, and is now the standing sender-timing instrument. `--agent <id>` selects PATH 1b,
`--repeat N` for cold-vs-warm.

---

## 5. NEXT ACTION - IN ORDER, START HERE

1. **CONFIRM OR KILL THE COLD-START HYPOTHESIS.** Query the ollama host for resident models and
   TTL. Ubuntu host 172.16.33.200, from PowerShell as an ssh command or via the HTTP API.
   If `qwen3-coder:30b` was absent at run 1 and resident with a TTL now, cold start is confirmed
   and **the fix is a keep-alive setting, not a code change.** Then re-run
   `post_timing_probe.py --repeat 2` after the TTL expires to reproduce deliberately.
2. **THEN re-measure the v3 stall against this baseline.** With warm-vs-cold understood, run v3
   and see whether its stall survives a warm model. **If it does, there is a second mechanism and
   it is v3's - and only then is patching the probe justified.** This ordering matters: the prior
   plan was to patch v3 first, and that would have been a patch to the wrong artifact.
3. **Answer the second-confirm-cycle question** (prior handoff section 5). Still the highest-value
   open question in the project, now deferred THREE windows. **It has been blocked on instrument
   trust; item 2 is what unblocks it.** Take it as soon as v3 is either cleared or fixed.
4. **Re-run step 3** - bogus agent id, gate-provoking prompt. Whether a ToolExecutor is
   constructed at all on the unresolvable-id sub-case is still UNKNOWN.
5. **Decide the System32 housekeeping** (prior handoff section 7). Two stale
   `start-openjarvis.ps1` copies remain on PATH. The stub option is still the strongest.
6. **Optional, low:** the clean W1 proof - remove websockets, `.\start-openjarvis.ps1`, re-test.
7. **Only then** the 6e UI work. Mount site `ChatArea.tsx`, design call option (b), new hook,
   `AgentsPage` untouched.

**Open design question, carried forward unchanged and still unsettled:** if the browser only
reaches a tool-capable path when an agent is selected, then either the gate is irrelevant to
default chat, or default chat should be tool-capable and currently is not. **Product decision, not
a bug fix. Do not let it be settled implicitly.**

---

## 6. WHAT CHANGED IN THE SYSTEM

- **`src\openjarvis\server\app.py` MODIFIED** - W2 guard, verified. 13776 bytes.
- **NEW FILE in repo root:** `post_timing_probe.py` (instrument, not application code).
- **NEW FILE in repo root:** `patch_w2_catchall_guard_v2.py` (the applied patch script).
- `patch_w2_catchall_guard.py` (v1) deleted - it used `Path.read_text(newline=)`, which requires
  Python 3.13 and raised TypeError on this venv. Never modified anything.
- **`ws_probe.py` UNCHANGED**, still v3, marker `openjarvis-ws-probe-agent-v3`.
- Backend restarted twice by Gray via `.\start-openjarvis.ps1`.

---

## 7. STATE AT WINDOW CLOSE

- Backend UP on port 8010, started via the real load path, W2 guard live, WS verified Open.
- **No probe running. No auto-approver alive. Nothing left to come back to.**
- 6c SATISFIED. 6d LIVE-PROVEN, CLOSED. 6e transport CLOSED on 1a and 1d, PROVEN on 1b for the
  first confirm cycle. 6e backend emit APPLIED, timeout branch verified;
  approved/denied/reaped still UNPROVEN. 6e browser half OPEN, blocked only by the 1d
  default-path question.
- W1 CLOSED. W2 CLOSED AND VERIFIED. W3 WITHDRAWN. W4 OPEN.
- **NEW HIGH hazard: silent patch no-op, section 3.**
- Repo root cleanup list, plus this window's additions: `post_timing_probe.py`,
  `patch_w2_catchall_guard_v2.py`, `app.py.bak-20260824-074322`, `app.py.bak-20260824-081250`.

---

## 8. EXECUTION PATHS REGISTER

Paths 1a, 1b, 1d and 2-5 carry forward UNCHANGED. Two deltas:

- **THE UNMATCHED-PATH ROW IS NOW OBSOLETE AND MUST BE REWRITTEN, NOT DELETED.** It read: any
  `/v1/*` path that no route matches returns SPA `index.html`, 200, `text/html`, 849 bytes.
  **As of this window unmatched `/v1/*` and `/api/*` return 404.** The historical statement stays
  in the record because every measurement taken before 2026-08-24 08:12 was taken under the old
  behavior. **Re-date any prior finding that rested on a 200 from an unmatched path.**
- **NEW ROW - PATH 1a FIRST-REQUEST LATENCY.** Measured cold 22.676 s, warm 0.565 s, same request
  bytes, `send -> first byte`. **Cause not yet established.** The register should carry the
  cold/warm distinction on every path once measured, because a single latency number for a path
  is meaningless without stating which of the two it is.

---

## 9. SDP FEED

Prior windows' SDP feed carries forward IN FULL. Additions:

- **THE SILENT PATCH NO-OP IS A NEW SDP ENTRY AND IT BELONGS UNDER OPERATOR-SURFACE DEFECTS**, the
  category proposed last window with W1 as its case study. **W1 and this are the same family: every
  artifact individually correct, the composed outcome false, and no error at any layer.** Two
  worked examples now, which is enough to justify the section.
- **EVIDENCE QUALITY, STATED AS A RULE:** a tool's self-report of success is not evidence of
  effect. The patch script printed a truthful account of what it attempted and a false account of
  what resulted. **The SDP should require an independent post-condition check - hash, behavior, or
  both - for every change claim in the document.** Today: the hash caught it, the print did not.
- **INSTRUMENT INDEPENDENCE IS NOW A DEMONSTRATED METHOD, NOT A PRINCIPLE.** The .NET WS client
  cleared the WS transport last window; the raw-socket sender cleared the client this window.
  **Both worked because they shared nothing with the thing under test.** State this as the SDP's
  standing rule for diagnostic design and cite both instances.
- **HEALTH CHECKS ON `/v1/*` ARE NOW MEANINGFUL, WHERE THEY WERE NOT.** The prior entry - a fetch
  of `/v1/agents/events` returns 200 in both healthy and broken states - **is fixed as of this
  window.** An unmatched path now 404s, so a fetch-based check can finally distinguish "route
  exists" from "route does not." **Rewrite the entry to record both the defect and its closure;
  the before-state is what makes the SDP entry instructive.**
- **THE GATE STILL WRITES NOTHING TO THE LOG.** Carried forward unchanged. Unauditable after the
  fact.
- **ROUTING INPUTS ARE UNVALIDATED.** Carried forward. **The heading proposed last window - THE
  SERVER RETURNS 200 FOR THINGS THAT DID NOT HAPPEN - now has one of its two mechanisms fixed.**
  The unmatched-path mechanism is closed; the bogus-`agent`-yields-200 mechanism is NOT. Keep the
  heading, note that it is half-resolved.

---

## 10. SDD SECTION

Gray is building a detailed System Design Document covering all OpenJarvis work to date. This
window feeds it:

- **THE DEPLOYMENT AND RUNTIME ENVIRONMENT CHAPTER GAINS A SECOND FINDING.** The listener on 8010
  is a system-Python child process (`C:\Users\Admin\AppData\Local\Programs\Python\Python312\
  python.exe`) spawned by the correct venv parent, both running
  `-m openjarvis.cli serve --port 8010`. **The venv start path is correct and the process actually
  serving is not the venv interpreter.** That system Python cannot even import
  `openjarvis.server.app` - it fails on `python-multipart`. **Not investigated this window
  (rule 6). It is the W1 mechanism one layer deeper: correct invocation, wrong program.** The
  chapter must document the process tree, not just the launch command.
- **PORTS, PROTOCOLS, ENCODING AT EACH GATE, with the PRECONDITION field.** Unchanged for
  `/v1/agents/events` except the failure-mode line: **unmatched paths now return 404, not a
  200 SPA index.** Update that row and keep the old value with its date.
- **COMPONENT-LEVEL GUARANTEES DO NOT SURVIVE COMPOSITION - now FIVE worked examples.** The four
  from last window plus: **a patch script that verified its anchors, compiled its output, created
  its backup, and reported success, on a healthy filesystem, leaving the file unchanged.** Every
  step verified; the composition still produced nothing.
- **DIAGNOSIS QUALITY subsection gains a second entry.** Last window: a confident W1 diagnosis that
  was wrong. This window: a confident attribution of the sender stall to probe v3, carried across
  two handoffs, **contradicted by the first measurement that used an independent instrument.**
  Cost of the wrong attribution: a queued patch to the probe that would have changed nothing.
  **The pattern in both cases is attributing a symptom to the nearest suspicious artifact without
  asking what else could produce it.**
- **PERFORMANCE CHAPTER needs a cold/warm axis.** 1d streams token-by-token, 2-8 ms to first
  chunk. 1b: 0.017 s gated, 0.006-0.008 s short runs. 1a: **22.676 s cold, 0.565 s warm.**
  **Every prior latency figure in the project was recorded without stating whether the model was
  resident. They are not comparable to each other until that is known.** Flag this explicitly.
- **REQUEST DISPATCH section**, schema first then predicates then paths, unchanged as the plan.
- **Safety inversions, still four, unchanged this window.**
- **Evidence provenance:** this window's findings rest on read-only shell commands, file hashes,
  and a raw-socket client. **None are exposed to probe v3.** Firmest tier.

**Standing instruction:** every handoff from here carries an SDD section, and every window feeds
it.

---

## 11. METHOD LESSONS

1. **A TOOL'S SUCCESS MESSAGE IS A CLAIM, NOT A RESULT.** The patch script said "written." The
   hash said otherwise. **Post-condition checks are not ceremony; today one of them was the only
   thing standing between us and a window spent debugging a patch that was never applied.**
2. **WHEN TWO CANDIDATE FIXES ARE OPPOSITES, MEASURE BEFORE CHOOSING.** The sender stall had two
   possible homes - probe or server - with opposite fixes. **Building a 150-line independent
   instrument was cheaper than patching the wrong one and believing the result.**
3. **AN INSTRUMENT THAT SHARES MACHINERY WITH THE SUSPECT CANNOT CLEAR IT.** Patching v3 to
   diagnose v3's own unreliability was the queued plan. It could not have produced a trustworthy
   answer at any level of effort.
4. **TWO IDENTICAL REQUESTS ARE A MEASUREMENT, NOT A REPETITION.** The 40x spread between run 1
   and run 2 carried more information than either number alone. **`--repeat 2` should be the
   default posture for any latency claim from here.**
5. **FIXING ONE DEFECT INVALIDATES MEASUREMENTS TAKEN UNDER IT.** The W2 fix changed what
   `pick_heartbeat_endpoint` selects, because a 404 now falls through where a 200 SPA index once
   satisfied it. **Any probe run recorded before 08:12 today was taken on a different machine in
   this respect.**
6. **STOPPING IS A DECISION, AND IT WAS MADE DELIBERATELY HERE.** The cold-start hypothesis is
   one command from confirmation, and that command belongs at the head of the next window with a
   full verify cycle behind it - not at the tail of this one.
