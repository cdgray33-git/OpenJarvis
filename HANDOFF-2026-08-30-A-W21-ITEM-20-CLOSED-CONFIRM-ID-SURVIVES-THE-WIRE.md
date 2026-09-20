# HANDOFF 2026-08-30 A / WINDOW 21
# OPEN ITEM 20 CLOSED - CONFIRM_ID SURVIVES THE WIRE - W20 COMMITTED AND PUSHED TO BOTH REMOTES

Predecessor: HANDOFF-2026-08-29-E-W20-TEST-EXECUTE-ROUTE-SHIPPED-CONFIRM-FRAME-ON-THE-WIRE.md
Host: Windows box. Shell: PowerShell 5.1. Working dir: `PS C:\Users\Admin\OpenJarvis>`.
Backend: 127.0.0.1:8010, ollama, qwen3-coder:30b, agent native_openhands.
Window shape: short, clean. No trace was cut. A mailbox interruption mid-window is
documented in section 6 because it produced rulings that outlive it.

---

## 0. ONE PARAGRAPH FOR THE NEXT WINDOW

Open item 20 is CLOSED. `confirm_id` is PRESENT on the `tool_confirm_request` frame
delivered to a bare, unauthenticated WebSocket client on loopback. The v3 redaction does
not strip it, and a UI can therefore answer a confirmation. The blocker was never the
server - it was a one-token key mismatch in the probe, found on the first read, fixed in
isolation, and verified by re-running W20 section 5 unchanged. W20's route plus this
window's probe fix are committed as `dde85c3` and pushed to BOTH remotes. The next window
inherits no unverified change and no dangling process. Its first job is the git hygiene
problem in section 7, which is now the largest untracked risk in the repo.

---

## 1. WHAT WAS DECIDED (rulings, do not revisit)

- **RULING: commit the W20 route ALONE, not the working tree.** `git status` showed 14
  modified tracked files. Only `agent_manager_routes.py` belongs to W20. A blanket
  `git add -A` would have swept thirteen files of unknown provenance from earlier windows
  into a commit whose message describes none of them. The commit was scoped to three
  paths by name.
- **RULING: the diff stat is the discriminator before committing a file.** W20 recorded
  the route as exactly 146 inserted lines. `git diff --stat` returned
  `146 insertions(+)`, 0 deletions, which proves the file carries the route and nothing
  else. This is the cheap check that makes a scoped commit safe, and it should be applied
  to every one of the remaining 13 files before any of them is committed.
- **RULING: `probe_ws_bare_subscribe.py` was NOT added to this commit.** It is untracked
  and lives in a repo root that already holds roughly 150 loose scripts. Adding probes one
  at a time makes that worse. Flagged as section 7 work, not solved opportunistically.

---

## 2. THE DEFECT, FOUND ON ONE READ

W20 section 4.1 recorded a contradiction: the probe printed a `tool_confirm_request`
frame at #3 and then printed `NO CONFIRM EVENTS` in its summary. W20 correctly refused to
call item 20 measured and correctly localized the fault to the probe rather than the
server.

Read of `probe_ws_bare_subscribe.py` lines 100-190 (the whole file is 190 lines) found it
immediately, in two places:

| Line | Code as written | Wire reality |
|---|---|---|
| 131 | `if etype.startswith("tool.confirm"):` | type is `tool_confirm_request` |
| 169 | `... str(f.get("type","")).startswith("tool.confirm")` | same |

**DOT versus UNDERSCORE.** Both sites tested a dotted prefix. Neither could ever match.
Line 131's failure is why the live frame line never had `confirm_id=` appended; line
169's failure is why `confirms` was an empty list, which fell through to the `else` at
181 and printed the false "NO CONFIRM EVENTS - EXPECTED, NOT A FAILURE".

**Nothing was wrong with the server, the bus, the bridge, or the redaction.** A single
character of separator in a diagnostic instrument produced four windows' worth of
uncertainty about a security property.

---

## 3. THE FIX AND ITS VERIFICATION

### 3.1 Patch

`patch_probe_confirmkey_v1.py`, marker `openjarvis-probe-confirmkey-v1`. Normalizes
underscores to dots before the prefix test at both sites:
`etype.replace("_", ".").startswith("tool.confirm")`. Nothing else in the probe was
touched - not the stale static text at line 184, not the unsuppressable trigger at 106.
FINISH THE THING applies to patches too.

| | Pre | Post |
|---|---|---|
| Bytes | 7729 | 7818 |
| SHA256 | 9098DC0D...4129D66F | 236155B2...E6D07061 |

Both anchors matched exactly once. Controls held: `trigger_traffic` occurrence count
unchanged, the `ABSENT - REDACTED` string survived, old dot-only test gone, marker
present once. py_compile OK.

### 3.2 Route liveness re-checked before measuring

`POST /v1/tools/test-execute {"tool":"mailbox_list_accounts"}` returned **422** with
`{"error":"tool does not require confirmation - refused"}`. This one call re-settled all
three W20 propositions in the current process: route mounted (not 404), env flag live
(not 403), guard still refusing non-confirming tools (422). No restart was needed.

### 3.3 THE MEASUREMENT - ITEM 20 CLOSED

W20 section 5's two-window procedure, run verbatim.

Window B: `POST /v1/tools/test-execute` with `shell_exec` returned **202**,
`run_id=94a6a2bb`, `turn_id=test-94a6a2bb`.

Window A:

```
[ws] #3   tool_confirm_request   agent_id=native_openhands  confirm_id=PRESENT
...
CONFIRM EVENTS: 1
  tool_confirm_request  confirm_id=PRESENT
```

**Both instruments now agree.** The live line and the summary collector report the same
thing, which is itself the proof that the 4.1 contradiction is resolved rather than
merely silenced.

**FINDING: the v3 redaction does NOT strip `confirm_id` on the wire.** The gate's request
frame reaches a bare, unauthenticated WS client with the answerable id intact. A UI can
answer a confirmation. Open item 20 is CLOSED.

**SECURITY COROLLARY, new and worth carrying:** the client that received `confirm_id` was
unauthed (`authed=False`). So anything that can open a WebSocket to the backend on
loopback can read a confirmation id and therefore answer a confirmation gate. Bind is
loopback so the blast radius is local to the box, but this is now a known property rather
than an assumption, and it belongs in the SDP threat section.

---

## 4. NEGATIVE RESULTS - WHAT THINGS TURNED OUT NOT TO BE

Pinned per the 08/24 rule.

### 4.1 The redaction was NOT the problem, and never had been

Four windows of suspicion pointed at `ws_bridge.py:61` and `OPENJARVIS_WS_TOKEN`. The
probe's own error message reinforced it, telling the reader that an ABSENT id means the
bridge redacted it because `_ws_authed` is False. That message is correct as written but
was never reached. **The instrument's explanatory text advertised a cause for a condition
the instrument could not detect.** Record this next to W20 section 4.1 in the
verification-methodology chapter: a probe that explains a failure it cannot measure is
worse than a silent one, because the explanation reads as analysis.

### 4.2 CLAUDE ERROR - my own patch script's line-ending counters are garbage

`patch_probe_confirmkey_v1.py` printed `PRE CRLF=0 bareLF=5` for a file that is plainly
not five lines long. The escapes in the count expressions were double-escaped, so it
counted occurrences of literal backslash-r text rather than line endings. **The byte
counts and SHAs in section 3.1 are sound; the CRLF and bareLF columns in that output mean
nothing.** Caught on read, not by the script. Any future patch script copying this
template must fix those two expressions or drop them - a wrong number in a verification
banner is exactly the class of thing this project keeps getting burned by.

### 4.3 GRAY WAS RIGHT - there was nothing to wait on

I told Gray to wait for Window A to print frame #3 and then its summary. He pushed back:
nothing to wait on. He was correct. The probe's summary prints when its LISTEN_SECONDS
window expires, and the first run's window had already closed before the trigger fired.
**I asked him to watch a timer I had not established the length of.** The re-run worked
because the trigger landed inside the window, not because anything changed.

### 4.4 The discriminator we specified was never actually displayed

W20's success criterion was a frame carrying `turn_id=test-<run_id>` matching Window B's
response body. **The probe does not print `turn_id`.** Frame #3 was matched to run
`94a6a2bb` by inference: only a confirming tool parks on the gate, and the probe's own
trigger returned 2 completion tokens with no tool call. That inference is strong but it is
not the displayed discriminator that was specified. If the next window adds the
`--no-trigger` flag, add `turn_id` to the printed line at the same time and the inference
becomes an observation.

### 4.5 Interpreter drift, still unchased

The patch script printed `sys.executable` as system Python 3.12, not a venv. W20 section
4.7 flagged the same drift on the probe. Still not chased, still a candidate false
negative in some later run.

---

## 5. VERIFIED FACTS SUMMARY

| Fact | Evidence |
|---|---|
| Probe confirm key was `tool.confirm`, wire is `tool_confirm_request` | direct read, lines 131 and 169 |
| Fix applied, single anchor hit each site | 7729 -> 7818 bytes, SHA recorded |
| Route live and enabled in current process | 422 with the refusal body |
| Gate reached with no model in the path | 202, `turn_id=test-94a6a2bb` |
| `confirm_id` PRESENT on an unauthed WS client | frame #3 and summary agree |
| W20 route diff is exactly the route | `146 insertions(+)`, 0 deletions |
| Commit on both remotes | `4dd6448..dde85c3` on GitHub and GitLab |

---

## 6. MAILBOX INTERRUPTION (out of band, but it produced durable rulings)

Gray hit his Yahoo quota mid-window and could neither send nor receive. Handled inline;
the OpenJarvis thread was parked cleanly and resumed.

- Fresh whole-mailbox census via the existing read-only `probe_usage_report.py`. Requires
  `$env:PYTHONIOENCODING="utf-8"` on this box.
- **NEW RULINGS, 24 senders cleared for Trash:** fashionnova, navyexchg/NEX,
  bananarepublicfactory, zalesoutlet, bestbuy, purple, sears, etsy, angi, dunhamssports,
  thetourguy, amf bowling, pulsetv, burger king, containerstore, skool, cvs extracare,
  untilgone, menswearhouse, womenshealthfirstly, wordstrivia, sperry, shoemall,
  retailmenot. Gray ruled the block in at once, explicitly including skool, CVS and NEX
  after those three were flagged as needing a call.
- **STILL UNRULED and held out:** whyy.org, github notifications, capitalone, USPS
  informed delivery.
- Standing exclusions re-confirmed: both stackcommerce addresses, self-sent
  cdgray33@yahoo.com, groupon notify/orders/verify/otp.
- Two scripts delivered to repo root: `move_promo_20260830.py` (33 senders, report-then-
  apply, double-gated) and `move_bestbuy_express.py` (direct move, two senders). **Gray
  ultimately drove the move through Jarvis instead**, which is the point of the whole
  project - the scripts were the fallback and stayed the fallback.
- **DESIGN NOTE worth keeping for any future mailbox script: use a folder ALLOWLIST, not
  a protected-folder blacklist.** The allowlist (Inbox, Archive, Promotions, Newsletters,
  Social, Social_Media) cannot reach a protected folder even if the protected list is
  wrong or incomplete. Same for searching by FULL address rather than substring token -
  it structurally removes the `noreply@r.groupon.com` versus `notify@r.groupon.com`
  collision class.

---

## 7. GIT STATE - THE NEXT WINDOW'S FIRST JOB

**COMMITTED AND PUSHED THIS WINDOW:** `dde85c3`, 3 files, 637 insertions.
`src/openjarvis/server/agent_manager_routes.py`, `patch_testexec_v1.py`,
`patch_probe_confirmkey_v1.py`. Pushed to `origin` (GitHub) and `gitlab`
(http://172.16.33.126/root/openjarvis-desktop.git), both from `4dd6448..dde85c3`.
Remotes are in sync.

**STILL UNCOMMITTED - 13 modified tracked files with mixed provenance:**

```
configs/openjarvis/config.toml          frontend/fix_interface.ps1
frontend/src/audio/ttsPlayer.ts         frontend/src/components/Chat/ChatArea.tsx
frontend/src/lib/api.ts                 src/openjarvis/agents/native_openhands.py
src/openjarvis/connectors/imap_mail.py  src/openjarvis/core/events.py
src/openjarvis/engine/ollama.py         src/openjarvis/server/app.py
src/openjarvis/server/auth_middleware.py src/openjarvis/server/routes.py
src/openjarvis/tools/mailbox_tools.py
```

Several of these carry verified, valuable work from earlier windows - the WS bridge fix,
the v3 redaction, the mailbox patches, the loop patch. **They are one `git checkout` away
from being lost and nothing in the repo records which window produced which hunk.**
Recommended method, one file at a time: `git diff --stat <file>`, compare against the
handoff that claims it, commit alone with a message naming that handoff. Do not batch.

**REPO ROOT POLLUTION:** roughly 150 untracked loose scripts (patch_*, probe_*, check_*,
dump*, fix_*), 19 untracked HANDOFF markdown files, and a stray
`"patch_testexec_v1 .py"` with a space in the filename sitting beside the real one.
A `scripts/` and `handoffs/` layout plus a `.gitignore` decision is owed. Not urgent, but
the space-in-filename duplicate is an active hazard for anchor-based patching.

---

## 8. EXECUTION PATHS REGISTER

Standing structure. Carried forward and extended, not re-derived.

### PATH 3: test-execute trigger - UPDATED

All W20 fields stand unchanged. Two amendments from this window:

| Field | Update |
|---|---|
| Confirmation gate | LIVE, re-confirmed in a second independent run (`94a6a2bb`) |
| Event bus traffic | `TOOL_CONFIRM_REQUEST` reaches a bare WS client **carrying `confirm_id`**. Delivery AND payload integrity now both proven. Redaction question CLOSED. |

Previously registered: PATH 1 orchestrator `ask()` via `system\orchestrator.py`; PATH 2
managed-agent SSE via `_stream_managed_agent()` in `server\agent_manager_routes.py`
(carries the four auto-approve sites, item 6); plus the routes.py chat dispatch branches
1a/1b/1c/1d.

---

## 9. SDP / SDD FEED

**Architecture.** The three-entry-path table for the confirmation gate is now not only
fillable but complete on the transport question. For the test-execute path: gate LIVE,
`confirm_id` delivered intact to an unauthed loopback subscriber.

**Defect 6 confirmation gate - Gray flagged this for GREAT DETAIL.** W21 upgrades the
transport row from W20:
- registry: write-once contract, 409 on re-decision, TIMEOUT settable only internally
- payload: seven fields, `turn_id` from the `CURRENT_TURN_ID` ContextVar,
  **`confirm_id` VERIFIED PRESENT on the wire**
- transport: EventBus -> ws_bridge -> bare WS client. Delivery proven W20, payload
  integrity proven W21. **The redaction question is closed; do not re-open it.**
- threading model: gate blocks a worker thread up to the 120 s TTL; callers must use
  `asyncio.to_thread`; pool-starvation constraint follows

**Threat model, new section owed.** An unauthenticated loopback WS subscriber can read
`confirm_id` and can therefore answer a confirmation gate. `OPENJARVIS_WS_TOKEN` is
unset, so `_ws_authed` is always False. This is a deliberate deferral (W17 auth ruling),
not an oversight, but the SDP must state it as a known accepted risk with its scope
(local box only, loopback bind asserted at startup per W19) rather than leave it implicit.

**Hazards found.** A diagnostic instrument that explains a failure it cannot detect
(section 4.1). Verification banners that print wrong numbers (section 4.2). Specifying a
discriminator the instrument does not display (section 4.4). All three belong in the
verification-methodology chapter alongside W20's positive-control case study.

---

## 10. 550B CLOUD MODEL

Carried forward per the 08/29 pin. When a question needs whole files rather than targeted
reads, bundle the suspected files into a single markdown file for Gray's 550B cloud model
(openrouter nemotron-3-ultra-550b) rather than spending window cycles on piecemeal reads.

**Not needed this window** - the probe defect was one read of a 190-line file. W20 had
pre-identified this as the bundle candidate if the fix was not obvious on sight; it was
obvious on sight, so the bundle was correctly not built. Recording that the escalation
path was considered and declined, per the negative-results rule.

**Strong candidate for the git hygiene work in section 7:** 13 diffs across frontend and
backend, needing provenance matched against 19 handoff documents. That is a whole-file
comparison problem across many files, which is exactly the shape the 550B pattern exists
for.

---

## 11. NEXT ACTIONS, ORDERED

1. **Git hygiene, section 7.** Take the 13 modified tracked files one at a time:
   `git diff --stat <file>`, match to the handoff claiming it, commit alone, push both.
   Consider bundling the diffs for the 550B model to do the provenance matching.
2. **Repo root layout decision.** `scripts/` and `handoffs/` plus a `.gitignore`. Delete
   the stray `"patch_testexec_v1 .py"` (with the space) - it is an anchor-patching hazard.
3. Cheap probe improvements, do not let them displace 1 and 2: add `--no-trigger` so the
   measurement collapses to one window; **print `turn_id` on the frame line** (section
   4.4); fix the stale static text at line 184 that still claims there is no direct
   tool-execution route; fix the PID capture using `Get-NetTCPConnection -LocalPort 8010`.
4. Open item 6 (the four managed-agent auto-approve sites on PATH 2) is now the largest
   remaining item on the confirmation gate.

---

## 12. STANDING RULES IN FORCE

- ALWAYS VERIFY. Never stack a second change on an unverified first one.
- FINISH THE THING BEFORE STARTING THE NEXT. No dangling processes.
- State shell and host on every command. Default PowerShell on the Windows box; anything
  for the Ubuntu ollama host (172.16.33.200) must be labeled or PowerShell-wrapped ssh.
- Commands must run from `PS C:\Users\Admin\OpenJarvis>` as pasted. If a command needs a
  different path, say so IN THE REQUEST, before it runs.
- No non-ASCII symbols in replies.
- Tests must be non-interactive wherever possible.
- Pin the detail of every window including negative results.
- Push to both remotes, always.
- Token conservation on working sessions.
- Flag at 15 exchanges, then hand off. A flag, not a stop - never cut a live trace.
