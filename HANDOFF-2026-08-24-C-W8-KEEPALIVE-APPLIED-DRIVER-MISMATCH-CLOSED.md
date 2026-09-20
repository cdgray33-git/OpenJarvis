# HANDOFF - 2026-08-24 EIGHTH WINDOW
# KEEP-ALIVE APPLIED AND VERIFIED. AN 18-DAY-OLD DRIVER MISMATCH FOUND AND CLOSED.
# THE HOST LAYER WAS NEVER IN THE RECORD AND IT WAS HOLDING TWO DEFECTS.

Supersedes `HANDOFF-2026-08-24-B-W7-COLD-START-CLOSED-V3-CLEARED-SECOND-CONFIRM-CYCLE-PROVEN.md`
for state. Everything in that file stands EXCEPT the keep-alive item, which is now done. Its
sections 5, 7, 8, 9, 10, 11, 12 are CARRIED FORWARD; only deltas are restated here.

**Actions this window: ZERO source patches. One host reboot, one host config change, both
verified in isolation. Eight read-only reads. Nothing left running.**

This window never touched the OpenJarvis repo. Every change was on `ollama-mcp` (172.16.33.200).

---

## 0. STANDING RULES FOR THE NEXT WINDOW

Rules 1-12 carry forward UNCHANGED. Two additions, both earned this window:

13. **THE HOST LAYER IS PART OF THE SYSTEM AND IT WAS NEVER IN THE RECORD.** Every prior handoff
    describes the repo. This window found two live defects that no amount of source reading could
    have surfaced: a driver/library mismatch 18 days old, and a crash-looping systemd unit on the
    wrong host. **The execution path register and the SDD must cover hosts, units, drivers and
    GPUs, not just call chains.**

14. **BEFORE ASSERTING BLAST RADIUS, READ IT.** Claude asserted that a reboot of .200 could not
    affect speech, from the record, one command before the reading that showed `kokoro-tts` running
    on .200. The assertion was wrong in its premise and right by luck. **State host facts from a
    reading taken this window, never from the carried record.**

---

## 1. ITEM 1 IS CLOSED - KEEP-ALIVE APPLIED AND VERIFIED

**The 30-minute eviction was CONFIGURED, not a default.** `/etc/systemd/system/ollama.service.d/override.conf`
already carried `OLLAMA_KEEP_ALIVE=30m`. No handoff ever recorded that this override existed. Three
windows treated the cold start as an unset default.

Change applied:

```
OLLAMA_KEEP_ALIVE=30m  ->  OLLAMA_KEEP_ALIVE=24h
```

Verified in effect, not just on disk: `/api/ps` now returns `expires_at 2026-08-25T14:24:26Z`,
24 hours out. File-level confirmation alone was not accepted as proof.

**Layer decision, and the reasoning belongs in the SDD:** the setting went on the HOST SERVICE, not
as a per-request `keep_alive` field. Reason - the execution path register is still incomplete (W7
item 5 is literally an unknown path), so a per-request field would only cover call sites we have
enumerated and any unlisted path would silently inherit the old default. The host setting covers
every consumer. **The recorded cost: OpenJarvis INHERITS its residency guarantee rather than
declaring it.** If OpenJarvis later needs to differ, add the per-request field then, as an override
above a known floor.

**A finite 24h was chosen over `-1` deliberately.** Finite still lets the host reclaim 19.5 GB and
self-heals across restarts; `-1` pins the allocation permanently and turns a tuning value into a
standing claim on the GPU. Revisit only if that host is confirmed to serve nothing else.

---

## 2. THE DRIVER MISMATCH - FOUND, 18 DAYS OLD IN THE RECORD, NOW CLOSED

Attempting to size the `OLLAMA_MAX_LOADED_MODELS=2` headroom hit:

```
Failed to initialize NVML: Driver/library version mismatch
NVML library version: 580.173
NVRM kernel module:   580.159.03
/var/run/reboot-required  PRESENT
ollama uptime: 23 days (since Aug 1)
```

Userspace had been upgraded under a live kernel module. Ollama still worked only because it took
its CUDA context before the upgrade. **A restart to apply the keep-alive change would very likely
have brought ollama back CPU-only** - a far worse regression than the 17 s being fixed, on the host
the whole inference path depends on. Verify-first caught this; the keep-alive change was held.

**THIS WAS ALREADY IN THE RECORD AND WAS LOST.** The 08/06 TTS investigation recorded it verbatim
as "a separate real issue, do not lose - `ollama-mcp` genuinely has the driver/library mismatch and
needs a reboot or module reload." It was filed against the TTS problem, was not the TTS cause, and
was never carried into a handoff. **It survived 18 days because it was recorded in the wrong place.**

**CORRECTION TO THAT 08/06 NOTE:** it also claimed "local model inference is on CPU right now."
**That is refuted.** `/api/ps` before the reboot showed `size_vram` equal to `size`, 19.5 GB fully
resident. Ollama was on the GPU throughout. Do not carry the CPU claim forward.

**RESOLUTION:** `sudo reboot`, verified in isolation before anything else touched the host:

```
NVRM module   580.173.02   (matches userspace)
nvidia-smi    initializes clean
ollama        active
reboot flag   cleared
GPU           Tesla P40, 23040 MiB, 0 MiB used
```

**CAUSE, and it will recur:** `unattended-upgrades.service` is running on this host. It will replace
the driver under a live context again. That is a lab policy decision, not a bug - see section 9.

---

## 3. HOST TOPOLOGY - ESTABLISHED BY READING, NOT BY RECORD

The `ollama-mcp` / `ollama-mcp2` confusion has cost this project two retractions historically. It is
now settled by `machine-id`, which is decisive:

| | 172.16.33.200 | 172.16.33.201 |
|---|---|---|
| hostname | `ollama-mcp` | `ollama-mcp2` |
| machine-id | `6daf1277af154042b070a6db925f7c56` | `e79b1231530845bdabe2aeb8e5c41552` |
| interface | `enp6s18` | `ens18` |
| GPU | **Tesla P40, 23040 MiB** | **Tesla P4, 7680 MiB** |
| ollama | `ollama.service`, active | runs outside systemd (08/07 finding) |
| kokoro-tts | present, CRASH-LOOPING (section 4) | active, SERVING |
| docker | none | `docker0`, `br-99322ea6ce16` |

**TWO DISTINCT MACHINES. TWO DIFFERENT GPUs.** The record's identification was correct.

**SSH ACCOUNT IS `administrator` ON BOTH.** This was never in a handoff and cost a failed command
this window. .200 accepts key auth; .201 prompted for a password.

**HEADROOM, now answerable:** P40 has 23,040 MiB, the model holds ~19.5 GB. `OLLAMA_MAX_LOADED_MODELS=2`
therefore has roughly 3.5 GB of room - enough for a small second model, **nowhere near a second 30B.**
Not a fault, but it is a documented constraint and a 24h keep-alive makes a collision more likely,
not less.

**OPEN, one read:** `size_vram` read 19,488,159,872 before the reboot and 19,072,923,776 after, on
the new driver. `size` was not captured in the same call afterward, so whether it is still FULLY
resident is UNCONFIRMED. One `/api/ps` read settles it. Do not assume.

---

## 4. `kokoro-tts.service` IS CRASH-LOOPING ON THE WRONG HOST - OPEN

```
host 172.16.33.200 (ollama-mcp)
ExecStart: venv/bin/uvicorn kokoro_server:app --host 0.0.0.0 --port 8880 --workers 1
start_time 14:03:42   stop_time 14:03:47   code=exited   status=3
```

**Five seconds to exit 3, then `Restart=` brings it straight back.** `systemctl list-units` showed it
"running" at 13:54 - that was a snapshot of one respawn cycle, not a healthy service. It has never
served traffic: nothing points at `.200:8880`.

**It is a stale duplicate of the real service on .201.** Almost certainly the residue of an attempted
TTS migration to .200 - see section 5.

**Consequences:** continuous restart churn on the host that serves every model call, log noise, and
if it ever DID come up it would take VRAM from the P40 that the 30B model needs. **Not chased this
window (rule 6). It gets disabled as its own isolated change** - see section 9.

**IT DOES NOT AFFECT SPEECH.** `src\openjarvis\server\speech_router.py:68` sets
`KOKORO_SERVER = "http://172.16.33.201:8880"` and every script in `tools\` agrees. REQUIREMENT ONE
runs off .201 and was never at risk.

---

## 5. `patch_tts.py` IS A TRAP IN THE REPO ROOT - DO NOT RUN IT

```
patch_tts.py:15:  'KOKORO_SERVER = "http://172.16.33.200:8880"\n\n'
```

**It rewrites the TTS target to the WRONG HOST** - to .200, where the service crash-loops. The disk
currently says .201, so it is NOT applied.

Per rule 12, a patch script in the repo root is an unconfirmed claim about the disk. This one is
confirmed unapplied and must STAY unapplied. **It goes on the cleanup list with its reason attached,
not just its name** - a bare filename on a list is exactly how it would get run by a future window
looking for something to apply.

---

## 6. ROLLBACK POINTS

All prior repo rollback points remain active and untouched, including
`app.py.bak-20260824-081250`.

**NEW, and it is the project's FIRST host-side rollback point:**

```
host:  172.16.33.200 (ollama-mcp)
file:  /etc/systemd/system/ollama.service.d/override.conf.bak-20260824
restore:
  ssh -t administrator@172.16.33.200 'sudo cp /etc/systemd/system/ollama.service.d/override.conf.bak-20260824 /etc/systemd/system/ollama.service.d/override.conf && sudo systemctl daemon-reload && sudo systemctl restart ollama'
```

**The rollback register must now span hosts, not just the repo.** Restoring this one returns
keep-alive to 30m; it does NOT undo the reboot, which is not reversible and does not need to be.

---

## 7. RETRACTIONS THIS WINDOW - BOTH MINE

1. **"A reboot here does not touch REQUIREMENT ONE."** Asserted from the carried record, one command
   before the reading that showed `kokoro-tts` running on .200. The conclusion held, but only
   because the unit turned out to be a broken duplicate. **The premise was unread.** Corrected
   before Gray acted on it.
2. **Two malformed commands.** A `USER@` placeholder that failed auth, and a `Select-String` sweep
   that let a binary `.db` consume all 40 result slots while `Format-Table` truncated the matched
   text away. Both cost a round trip.

**This is the fourth instance of the DIAGNOSIS QUALITY pattern** now tracked in the SDD: attributing
or asserting before reading the evidence that was one command away. The countermeasure stands - when
the discriminating read is available, take it before speaking.

---

## 8. STATE AT WINDOW CLOSE

- **`ollama-mcp` (.200) rebooted, driver healthy, ollama active, keep-alive 24h verified live.**
- Model `qwen3-coder:30b` resident, `expires_at 2026-08-25T14:24:26Z`.
- OpenJarvis backend: **NOT touched this window.** Its state is as W7 left it - up on 8010, W2 guard
  live, gate live. **Not re-verified since the .200 reboot** - see section 9 item 1.
- No probe running, no listener alive, nothing left to come back to.
- 6c SATISFIED. 6d LIVE-PROVEN CLOSED. 6e transport CLOSED on 1a, 1b (multi-cycle), 1d.
  `TOOL_CONFIRM_RESOLVED` LIVE. **6e browser half OPEN.**
- W1 CLOSED. W2 CLOSED AND VERIFIED. W3 WITHDRAWN. W4 OPEN.
- Cold start CLOSED. Probe v3 CLEARED. Second confirm cycle CLOSED. **Keep-alive CLOSED. Driver
  mismatch CLOSED.**

---

## 9. NEXT ACTION - IN ORDER, START HERE

1. **RE-VERIFY OPENJARVIS END TO END AFTER THE HOST REBOOT.** The model host went down and came back
   under a new driver. Nothing in the app was changed, but the app has not made a real request since.
   One chat turn through the UI, confirm a response and confirm the gate still fires. **Do this
   before any new work** - it is the isolation check on the reboot from the application side.
2. **CONFIRM FULL VRAM RESIDENCY.** One `/api/ps` read capturing BOTH `size` and `size_vram`.
   Section 3 open item. Trivial, and it closes a real unknown.
3. **READ `patch_confirm_resolved.py` AND HASH ITS TARGET.** Carried unchanged from W7 item 2.
   Establish what shipped on 08/22 and capture one full untruncated `tool_confirm_resolved` frame so
   the 6e UI is written against a known field set.
4. **THE 6e UI WORK - HEAD OF THE QUEUE ONCE 3 IS DONE.** Mount site `ChatArea.tsx`, design option
   (b), new hook, `AgentsPage` untouched. Subscribe to `tool_confirm_request` AND
   `tool_confirm_resolved`.
5. **DISABLE THE STALE `kokoro-tts` UNIT ON .200.** Section 4. `sudo systemctl disable --now
   kokoro-tts` on .200 ONLY. **Verify the hostname in the same command** - this unit name exists on
   both boxes and running it against .201 takes speech down.
6. **DECIDE THE `unattended-upgrades` POLICY ON THE MODEL HOSTS.** Section 2. It caused an 18-day
   silent degradation and will do it again. Options: hold the nvidia packages, or accept it and add
   a residency/driver check to startup. **Architecture decision, belongs in the SDD.**
7. **Fix the 0 ms latency display** before the 6e UI ships. Carried from W7 section 5.
8. **Re-run W7 step 3** - bogus agent id, gate-provoking prompt. Still UNKNOWN.
9. **System32 housekeeping** - two stale `start-openjarvis.ps1` copies on PATH. Stub option still
   strongest. Unchanged.

**Open design question, carried forward unchanged and still unsettled:** if the browser only reaches
a tool-capable path when an agent is selected, then either the gate is irrelevant to default chat,
or default chat should be tool-capable and currently is not. **Product decision. Do not let it be
settled implicitly.**

**ALSO STILL OPEN, carried and not chased:** `mailbox_move_to_trash` and `mailbox_empty_folder` carry
NO `requires_confirmation` at the spec level. **The destructive mailbox tools remain ungated and no
amount of confirm-gate wiring reaches them.** Oldest live safety item in the project. It has now
survived several windows as a carried note and **it deserves a decision, not another carry.**

---

## 10. EXECUTION PATHS REGISTER

Paths 1a, 1b, 1d and 2-5 carry forward UNCHANGED. Deltas:

- **EVERY PATH ROW NOW NEEDS A HOST AND DRIVER COLUMN.** This window found two defects invisible from
  the source tree. A path's behaviour depends on which host serves it, that host's GPU, its unit
  config and its driver state. **The register is incomplete without them.**
- **PATH 1a GAINS A HOST ROW.** Served by `ollama-mcp` 172.16.33.200:11434, HTTP/JSON, Tesla P40
  23040 MiB, driver 580.173.02, `ollama.service` under systemd, `OLLAMA_KEEP_ALIVE=24h`,
  `OLLAMA_MAX_LOADED_MODELS=2`.
- **THE SPEECH PATH GAINS A HOST ROW.** Served by `ollama-mcp2` 172.16.33.201:8880, HTTP/JSON, Tesla
  P4 7680 MiB, `kokoro-tts.service` under systemd. Client anchor
  `src\openjarvis\server\speech_router.py:68`.
- **PATH 1a COLD/WARM ROW - RE-BASELINE REQUIRED.** W7's 16.692 s was measured on the OLD DRIVER,
  pre-reboot. This window measured 13.855 s but by a DIFFERENT INSTRUMENT (direct HTTP round trip
  including full generation) on a DIFFERENT PATH. **The two are not comparable and must not be
  differenced.** The cold row needs one re-measure on PATH 1a with the raw-socket instrument.
- **THE COLD/WARM AXIS REMAINS MANDATORY ON EVERY PATH ROW**, and now carries a driver-version
  qualifier too.

---

## 11. SDP FEED

Prior windows' SDP feed carries forward IN FULL. Additions:

- **THE SYSTEM HAS A HOST LAYER AND THE SDP DID NOT MODEL IT.** Two live defects this window, neither
  reachable from the source tree: a driver mismatch and a crash-looping unit on the wrong host.
  **Add a deployment-state section covering hosts, units, drivers, GPUs and their config, at the same
  rigour as the call chains.**
- **THE RECORD DRIFTS IN A THIRD DIRECTION: RIGHT FACT, WRONG FILE.** Rule 11 covers claimed-not-applied;
  rule 12 covers applied-not-claimed. **This window found correctly-recorded-but-unrouted** - the
  driver mismatch was written down accurately on 08/06 inside a TTS investigation it did not belong
  to, and was never seen again. **A finding filed under the wrong problem is functionally lost.**
  The countermeasure is routing, not diligence: a finding that is not the current problem must be
  promoted to the handoff in its own right, at the moment it is found.
- **CONFIGURED VALUES MASQUERADE AS DEFAULTS.** `OLLAMA_KEEP_ALIVE=30m` was a deliberate choice by
  someone, invisible to three windows of planning that assumed an unset default. **Enumerate the
  config before theorizing about behaviour.**
- **A UNIT REPORTING `running` MAY BE CRASH-LOOPING.** `systemctl list-units` showed `kokoro-tts`
  active on .200; it exits 3 every five seconds and is respawned. **`is-active` is not health.**
  Read `ExecStart` with `start_time`/`stop_time`/`status` before concluding a service works. Same
  evidence-quality family as "a tool's self-report of success is not evidence of effect."
- **THE FIRST HOST-SIDE ROLLBACK POINT EXISTS.** The rollback register spanned only the repo until
  now. **It must span hosts**, and host changes divide into reversible (config) and irreversible
  (reboot) - the register should distinguish them.
- **AUTOMATED UPDATES ARE AN UNMANAGED CHANGE SOURCE ON A CRITICAL HOST.** `unattended-upgrades`
  replaced a GPU driver under a live CUDA context and degraded the host silently for 18 days.
  **Every "nothing changed" claim in this project is conditional on that service not having acted.**
- **BLAST RADIUS IS A READING, NOT AN INFERENCE.** Before any destructive host action, enumerate what
  runs there in the same session. See section 7 retraction 1.
- **A `0ms` LATENCY DISPLAY ON A GATED TOOL IS AN OPERATOR-SURFACE HAZARD.** Carried unchanged.
- **ROUTING INPUTS ARE UNVALIDATED.** Carried unchanged, still half-resolved.

---

## 12. SDD SECTION

Gray is building a detailed System Design Document covering all OpenJarvis work to date. This window
feeds it:

- **DEPLOYMENT AND RUNTIME ENVIRONMENT - THE HOST TABLE IS NOW REAL DATA, section 3.** Two machines,
  distinct machine-ids, two different GPUs (P40 23040 MiB on the model host, P4 7680 MiB on the
  speech host), different interface names, different ollama management (systemd on .200, outside
  systemd on .201). **This table belongs in the SDD verbatim** - the `ollama-mcp` / `ollama-mcp2`
  ambiguity has caused retractions three times and a table with machine-ids ends it.
- **PORTS, PROTOCOLS, ENCODING AT EACH GATE - two rows confirmed this window.** `.200:11434` HTTP/JSON
  for model inference (`/api/generate`, `/api/ps`, `keep_alive:0` forces eviction, `models: []` is the
  cold post-condition); `.201:8880` HTTP/JSON for speech (`/synthesize`, `/synthesize-stream`,
  `/health`). **Add a HOST and DRIVER column to this artifact**, and remember it must be delivered as
  a downloadable standalone file for the wiki.
- **KEEP-ALIVE OWNERSHIP - DECIDED, WITH REASONING, section 1.** Host service config over per-request
  field, because the execution path register is incomplete and unlisted paths would silently inherit
  the old default. **Recorded cost: OpenJarvis inherits its residency guarantee rather than declaring
  it.** Record the reasoning, not just the value - and record the finite-vs-`-1` choice too.
- **PERFORMANCE CHAPTER - THE 1a COLD BASELINE IS NOW INVALID AND MUST BE RE-TAKEN.** W7's 16.692 s
  was measured on the old driver. **Every latency figure in the project now needs a driver-version
  qualifier alongside the residency qualifier.** The chapter needs two columns, not one.
- **CONFIRMATION GATE CHAPTER - GREAT DETAIL, per the standing instruction.** Unchanged this window;
  W7's characterization stands in full including the two-gates-in-one-turn case.
- **DIAGNOSIS QUALITY subsection gains a FOURTH entry, and it is mine.** I asserted that a .200 reboot
  could not affect REQUIREMENT ONE, from the carried record, one command before the reading that
  showed `kokoro-tts` running on .200. **Four instances is no longer a pattern, it is a property of
  how I work under a carried record.** The countermeasure is now specific: **a host fact stated in a
  handoff is a hypothesis until re-read in the current session.**
- **OPERATIONS CHAPTER, NEW - CHANGE SOURCES OUTSIDE THE PROJECT.** `unattended-upgrades` on the model
  hosts. The SDD should name every actor that can change this system without a handoff entry.
- **COMPONENT-LEVEL GUARANTEES DO NOT SURVIVE COMPOSITION - still five worked examples**, none added.
- **Safety inversions - still four**, plus the standing spec-level gap on the destructive mailbox
  tools, which is an absence rather than an inversion and should be its own entry.
- **Evidence provenance:** direct HTTP reads, ssh reads of systemd unit state, `machine-id`
  comparison, `nvidia-smi` post-reboot, and a repo-wide source grep. **No OpenJarvis source was
  modified**, so nothing here is contingent on a patch landing. Firmest tier.

**Standing instruction:** every handoff from here carries an SDD section, and every window feeds it.

---

## 13. METHOD LESSONS

1. **VERIFY-FIRST PAID FOR ITSELF IN CASH THIS WINDOW.** The keep-alive change required a restart.
   Reading the host before restarting found a driver mismatch that would very likely have brought
   ollama back CPU-only. **The cheapest open win in the project was sitting on top of a live hazard**,
   and the only reason it did not fire is that the config was not changed first.
2. **ISOLATE THE RISKY STEP EVEN WHEN COMBINING IS FREE.** The reboot restarted ollama anyway, so
   writing the override first would have saved a restart. It was not done. The reboot was verified
   alone, then the config applied and verified alone. **Two changes in one reboot means two suspects
   if it comes back wrong**, with a 19.5 GB model that will not load.
3. **A RIGHT FACT IN THE WRONG FILE IS A LOST FACT.** 18 days. See section 11.
4. **`machine-id` SETTLES HOST IDENTITY. NOTHING ELSE DOES.** Hostnames, IPs and interface names have
   all misled this project. Two commands, one decisive answer.
5. **BINARY FILES IN THE REPO ROOT WILL EAT A GREP.** `memory_vacuumed_test.db` consumed all 40
   result slots. Scope by extension and print the matched text, or the sweep proves nothing.
6. **A CONFIG WINDOW IS A LEGITIMATE WINDOW.** Zero source patches, two host changes, two questions
   closed and two new defects found. Nothing left half-wired because nothing was started that could be.
