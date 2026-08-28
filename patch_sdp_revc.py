#!/usr/bin/env python3
# openjarvis-sdp-ws-event-channel-revC
# Produces SDP-WS-EVENT-CHANNEL-2026-08-26-revC.md from revB by anchored
# in-place amendment. Dry run by default; --apply writes the output file.
#
# Run from the repo root:  python .\patch_sdp_revc.py            (dry run)
#                          python .\patch_sdp_revc.py --apply
#
# Every replacement asserts an exact match count. Any miss aborts before write.

import hashlib
import sys

SRC = "SDP-WS-EVENT-CHANNEL-2026-08-26-revB.md"
DST = "SDP-WS-EVENT-CHANNEL-2026-08-26-revC.md"

EXPECT_SRC_BYTES = 32391
EXPECT_SRC_SHA = None  # set after first run if a pin is wanted

EDITS = []


def edit(name, old, new, count=1):
    EDITS.append((name, old, new, count))


# ---------------------------------------------------------------- E1 header
edit(
    "E1 header block -> revision C",
    """Artifact date: 2026-08-26. Source window: W12 continuation (W13).
REVISION B, same day, post-W13: sections 3.2, 3.3, 5, 6, 7, 8, 9 and 10 amended
after the redaction was proven BOTH WAYS, the implementation was read at source,
and the feature set was committed. Revision A of this file predated all of that.
Marker of the change described here: `openjarvis-ws-cid-redact-v1`.
Commit of record: `6c132d6` on `main`, pushed to both remotes.

STATUS CHANGE IN THIS REVISION: the D-SEC-1 redaction is no longer merely
APPLIED. It is VERIFIED behaviorally in both directions and CONFIRMED at source.
Section 8 open item 2 of revision A is closed by section 6.
""",
    """Artifact date: 2026-08-26. Source window: W12 continuation (W13, W14).
REVISION C, 2026-08-28, post-W14: sections 3.2, 3.3, 5, 6, 7, 8, 9 and 10
amended after the redaction was WIDENED to cover both confirm frame types,
verified both ways a second time, and committed. Revision B described a
half-implemented posture; that is no longer the state.
Marker of the change described here: `openjarvis-ws-cid-redact-v2` on the
forward-loop block. The accept-site block deliberately remains at v1 because it
did not change - the v1 marker is NOT unique in that file and any control
asserting that it greps back exactly once would be wrong.
Commit of record: `4c365c1` on `main`, pushed to both remotes.
Predecessor commit: `6c132d6` (the v1 redaction and the confirm registry).

STATUS CHANGE IN THIS REVISION: posture C is FULLY implemented for this
transport. Both `TOOL_CONFIRM_REQUEST` and `TOOL_CONFIRM_RESOLVED` are redacted
for unauthenticated subscribers, proven in both directions on a post-reboot
build. Revision B open item 1 is CLOSED. Revision B open item 4 is CLOSED and
its finding OVERTURNED. Revision B open item 5 is CORRECTED on evidence, not
closed.
""",
)

# ---------------------------------------------------------------- E2 3.2
edit(
    "E2 section 3.2 - resolved frame no longer unredacted",
    """THIS FRAME STILL CARRIES `confirm_id` UNREDACTED. See section 8, open item 1.
""",
    """THIS FRAME IS NOW REDACTED for unauthenticated subscribers, as of the
`openjarvis-ws-cid-redact-v2` change (commit `4c365c1`). An authenticated
subscriber receives `confirm_id`; an unauthenticated one receives every other
field intact and no `confirm_id`. Section 6.5 records the proof in both
directions. Revision B's "still carries it unredacted" framing is obsolete and
should not be quoted from older copies of this artifact.
""",
)

# ---------------------------------------------------------------- E3 3.3 head
edit(
    "E3 section 3.3 heading and scope line",
    """### 3.3 Redaction rule (the `openjarvis-ws-cid-redact-v1` behavior)

For `TOOL_CONFIRM_REQUEST` only:
""",
    """### 3.3 Redaction rule (the `openjarvis-ws-cid-redact-v2` behavior)

For BOTH `TOOL_CONFIRM_REQUEST` and `TOOL_CONFIRM_RESOLVED`:
""",
)

# ---------------------------------------------------------------- E4 3.3 warn
edit(
    "E4 section 3.3 warning now names the frame type",
    """- A redaction emits a `logger.warning` naming the peer.
""",
    """- A redaction emits a `logger.warning` naming BOTH the frame type and the
  peer. The frame type is passed as a parameter rather than hardcoded, so the
  log discriminates which frame was redacted for which subscriber. Before v2 the
  string hardcoded `TOOL_CONFIRM_REQUEST`; widening the predicate without this
  would have written a false statement into the audit log on every resolved-frame
  redaction, in the same class as the fail-quiet hazards section 7.4 tracks.
""",
)

# ---------------------------------------------------------------- E5 3.3 tail
edit(
    "E5 section 3.3 verification paragraph -> both frame types",
    """VERIFIED BOTH WAYS 08/26. The rule above is no longer a description of intent.
Section 6.2 records an unauthenticated run in which the request frame arrived
twice without `confirm_id`, and an authenticated run in which it arrived with
one, and section 6.3 records the forward loop read at source. Behavior,
implementation and this document agree.
""",
    """VERIFIED BOTH WAYS, BOTH FRAME TYPES. The rule above is not a description of
intent. Section 6.2 records the request-frame pair; section 6.5 records the
resolved-frame pair on the v2 build, unauthenticated and authenticated, against
the same server. Section 6.3 records the forward loop read at source. Behavior,
implementation and this document agree.

SCOPE CORRECTION WORTH PINNING: revision B scoped this change as one line at
`ws_bridge.py:51`. It is four edits. The predicate at 51 is consumed at 58, and
the warning text at 64-65 hardcoded the frame type. A scope estimate carried in
a handoff is an estimate; re-derive it from source before patching.
""",
)

# ---------------------------------------------------------------- E6 timings
edit(
    "E6 section 5 - three new timing rows",
    """| `tool_confirm_resolved` to `tool_call_start` | 4 ms, resolved frame FIRST | Disclosure window opens before execution - see section 3.2 |
""",
    """| `tool_confirm_resolved` to `tool_call_start` | 4 ms, resolved frame FIRST | Disclosure window opens before execution - see section 3.2 |
| Unanswered confirmation, third measurement | 120.013 s (emit 09:16:12.2346845, reap 09:18:12.24768) | Third independent run consistent with 120.004 and 120.027 - the TTL is stable, not coincidental |
| Reap to re-request | 1.6 s (t1 reaped 09:18:12.247, t2 issued 09:18:13.833) | One user request consumes TWO 120 s worker slots on the shared pool, not one |
| Total user-visible time, unanswered gate | 245.8 s, ending in an apology | The cost of open item 2a stated in wall-clock time rather than as a design note |
""",
)

# ---------------------------------------------------------------- E7 6.5 new
edit(
    "E7 new section 6.5 before section 7",
    """---

## 7. NEGATIVE RESULTS - PIN THESE
""",
    """### 6.5 Part three - the v2 widening, both frame types, post-reboot

Ran 2026-08-26 after the predicate was widened to cover `TOOL_CONFIRM_RESOLVED`.
Same instruments as 6.2, same server, opposite expected result on one frame.

PRECONDITION, and it nearly invalidated the run: the box REBOOTED at 08:47:25,
between the patch write (08:33:55) and the verification. Before any behavioral
claim was made, both python process creation times were read at 08:52:53 -
19 minutes AFTER the patch and 5 minutes after boot. The running server therefore
serves post-patch code. Command lines were deliberately NOT printed; they can
carry secrets and creation time answers the question alone. THIS CHECK IS NOW A
PREREQUISITE for any behavioral claim following a patch, not an optional step.

| | Unauthenticated (peer 56454) | Authenticated (peer 58294) |
|---|---|---|
| `tool_confirm_request` carries `confirm_id` | NO, on both t1 and t2 | YES, `0e5e7140...` |
| `tool_confirm_resolved` carries `confirm_id` | NO - the v2 change, proven | YES, the same cid |
| `ws-cid-redact` lines naming this peer | 3, both frame types named | none |

The unauthenticated resolved frame printed UNTRUNCATED in the capture with
`agent_id`, `turn_id`, `tool`, `decision:"timeout"`, `state:"resolved"`,
`created_at`, `expires_at` and `reaped:false` - and no `confirm_id`. In the 6.2
run that same frame type, on that same script, carried its cid in the clear.
Same harness, same regex, same server, opposite result.

The authenticated half is not a formality. Over-redaction was the plausible
regression from widening a predicate, and it is the only thing that
distinguishes a working redaction from a broken one.

HONEST LIMIT, stated because it is a real weakening of the evidence: this run
has NO in-run positive control. The 6.2 run got one for free precisely BECAUSE
the resolved frame was unredacted - the regex firing on it proved the instrument
live. The v2 change removes that. The regex is proven by the earlier run against
the same build, not by this one. Acceptable only because the before-picture is
the same script on the same server. Any future window wanting an in-run control
must use a third frame type that legitimately carries an id-like field.

METHODOLOGICAL CONSEQUENCE, and it generalizes past this transport: THE
STRONGEST AVAILABLE VERIFICATION MAY DESTROY THE CONTROL THAT MADE THE PREVIOUS
ONE STRONG. A hardening change can reduce future observability. That cost should
be named at design time, not discovered afterward.

---

## 7. NEGATIVE RESULTS - PIN THESE
""",
)

# ---------------------------------------------------------------- E8 7.2
edit(
    "E8 section 7.2 heading -> overturned",
    """### 7.2 The `ua=` attribution field is currently dead
""",
    """### 7.2 The `ua=` attribution field is dead ONLY FROM POWERSHELL - OVERTURNED
""",
)

edit(
    "E9 section 7.2 consequence -> corrected",
    """CONSEQUENCE: the `ua=` field cannot presently identify a subscriber from a
PowerShell test client. The prospective-identification use recorded for this
field is NOT satisfied. Attribution in runs A and B rests on timestamp
correlation alone, which is adequate here only because nothing else subscribes.
""",
    """OVERTURNED 2026-08-26. The limitation is specific to the .NET Framework
`ClientWebSocket` under PowerShell 5.1. It is NOT a property of the field and
NOT a server-side defect. A client that sets the header was already sitting in
the repo root: `probe_confirm_frames.py` produced
`ua='Python/3.12 websockets/17.0.1'` on the authenticated accept for peer 58294.

CONSEQUENCE, corrected: KEEP THE FIELD. Revision B recommended removing it as a
permanently-null column; that recommendation is withdrawn. Subscriber
attribution no longer rests on timestamp correlation alone - use a Python client
for any test where attribution matters, and expect `ua=None` from a PowerShell
one.

NOTED, NOT A CONTRADICTION: that string reports `websockets/17.0.1` while the
venv holds 15.0.1. Different interpreters - the probe ran on system Python 3.12,
the server on the venv. Worth confirming once if any future test depends on
client library behavior rather than protocol behavior.

LESSON FOR THIS PACKAGE: a capability was recorded as ABSENT when what was
actually established was that ONE CLIENT could not exercise it. Before a field,
route or feature is written down as dead, name the instrument that failed to
reach it and ask whether a different instrument would.
""",
)

# ---------------------------------------------------------------- E10 item 1
edit(
    "E10 section 8 item 1 -> CLOSED",
    """1. **`TOOL_CONFIRM_RESOLVED` still carries `confirm_id` unredacted.** ESCALATED
   in this revision, not merely carried. Replay is blocked (409 in 16 ms against
   a real out-of-band resolver), but the resolved frame is broadcast 4 ms BEFORE
   `tool_call_start`, so this is an unauthenticated intelligence feed on every
   gated operation rather than a spent key of no consequence. See section 3.2.
   Fix is small and already scoped: widen `ws_bridge.py:51` to cover both confirm
   event types. The `_had_cid` guard at line 60 already handles a frame with no
   cid, so the branch is safe on either. Own change, own verification pass -
   re-run the unauthenticated exploit and confirm the `CONFIRM_ID:` banner NEVER
   prints, not even at +120 s. Run 1 in section 6.2 is the before-picture.
""",
    """1. **CLOSED by section 6.5.** `TOOL_CONFIRM_RESOLVED` is redacted for
   unauthenticated subscribers as of `openjarvis-ws-cid-redact-v2`, commit
   `4c365c1`. Verified in both directions on a confirmed post-patch build. The
   fix was four edits, not the one line revision B scoped. Retained as a numbered
   item so references to "open item 1" from earlier documents resolve correctly.
""",
)

# ---------------------------------------------------------------- E11 item 4
edit(
    "E11 section 8 item 4 -> CLOSED",
    """4. **`ua=` attribution** needs a client that can actually set the header, or the
   field should be removed rather than left as a permanently-null column.
""",
    """4. **CLOSED and OVERTURNED.** The `ua=` field works. See section 7.2. The
   removal recommendation is withdrawn; use a Python client where attribution
   matters. Retained as a numbered item for reference resolution.
""",
)

# ---------------------------------------------------------------- E12 item 5
edit(
    "E12 section 8 item 5 -> corrected on evidence",
    """5. **Token persistence.** The token in use is session-scoped, set in the shell
   that launched the server. It does not survive a reboot or a new window, so
   any fresh start comes up fail-closed.""",
    """5. **Token persistence - CORRECTED, NOT CLOSED.** Revision B stated that the
   token is session-scoped and does not survive a reboot, so any fresh start
   comes up fail-closed. THAT IS FALSE AS STATED. A genuine reboot occurred at
   08:47:25 on 08/26 and the token survived it: `authed=True` at 09:00:21.
   Discriminated rather than assumed - a deliberately WRONG token returned
   `authed=False` at 09:06:58, which is the load-bearing control, because without
   it "it authenticates" cannot be separated from "the auth check is broken."
   The source was then hunted and NOT found: `OPENJARVIS_WS_TOKEN` is unset at
   Process, User and Machine scope; absent from `start-openjarvis.ps1`; absent
   from `.env`; absent from every repo-root `.ps1`. Remaining candidates are the
   launching shell and the desktop app's spawn chain. THE TRUE STATEMENT IS
   NARROWER AND STILL A REAL GAP: the token has no durable, discoverable home,
   so whether a fresh start comes up authenticated depends on how it was
   launched, and nobody can currently explain why it worked. Open item 2a cannot
   depend on an unlocated secret.""",
)

# ---------------------------------------------------------------- E13 item 8
edit(
    "E13 section 8 - new item 8, reaped flag",
    """   fourth builds an ad-hoc per-tool executor and calls `execute()` directly,
   bypassing the agent, on the managed-agent SSE stream. Its rationale is stated
   as deliberate - wizard-added tools treated as pre-approved. That argument must
   be explicitly accepted or overturned, not left implicit.
""",
    """   fourth builds an ad-hoc per-tool executor and calls `execute()` directly,
   bypassing the agent, on the managed-agent SSE stream. Its rationale is stated
   as deliberate - wizard-added tools treated as pre-approved. That argument must
   be explicitly accepted or overturned, not left implicit.
8. **`"reaped": false` on a timeout resolution.** The resolved frame carries a
   `reaped` field that the section 3.2 frame contract does not list, and it reads
   `false` on a resolution whose `decision` is `timeout`. Observed on both the
   unauthenticated (09:18:12.250) and authenticated (09:25:45.263) runs. Either
   the field name is misleading or the flag is set at a later stage than the
   emit. Read `confirm_registry._snapshot()` before the frame contract in this
   document is treated as complete.
""",
)

# ---------------------------------------------------------------- E14 sec 9
edit(
    "E14 section 9 residual -> fully implemented",
    """RESIDUAL, stated so the posture is not overclaimed: posture C is satisfied for
`TOOL_CONFIRM_REQUEST` only. Until open item 1 is closed, the cid still reaches
unauthenticated subscribers on the resolved frame, 4 ms ahead of execution. The
posture is HALF IMPLEMENTED and should be described that way in the security
chapter until the second half lands.
""",
    """POSTURE C IS FULLY IMPLEMENTED FOR THIS TRANSPORT as of commit `4c365c1`.
Revision B recorded it as HALF IMPLEMENTED because the resolved frame still
carried the cid. Both confirm frame types are now redacted for unauthenticated
subscribers, verified in both directions (section 6.5). No `confirm_id` reaches
an unauthenticated socket on this channel by any frame.

SCOPE OF THAT CLAIM, stated so it is not read wider than it is: it covers
`/v1/agents/events` and nothing else. It says nothing about whether a local
process can obtain the token by other means, nothing about the three other
execution paths in the register, and nothing about tools that never reach a gate
at all - open item 6 remains a coverage gap that no amount of transport
hardening touches.

THE FEATURE IS CORRECT AND STILL NOT USABLE. Every gate measured in section 6.5
reaped at 120 s and the user saw an apology. Correctness and usability are
different states and this document should not be read as claiming the second.
See open item 2a.
""",
)

# ---------------------------------------------------------------- E15 sec 10
edit(
    "E15 section 10 - v2 commit appended",
    """BACKUP HYGIENE: both `ws_bridge.py.bak_cidredact_*` files hashed identically to
each other and differently from the live file, confirming genuine pre-patch
content and that the committed file is the patched one. Deleted by explicit path,
never by wildcard, with a count of 0 confirmed after.
""",
    """BACKUP HYGIENE: both `ws_bridge.py.bak_cidredact_*` files hashed identically to
each other and differently from the live file, confirming genuine pre-patch
content and that the committed file is the patched one. Deleted by explicit path,
never by wildcard, with a count of 0 confirmed after.

### 10.1 The v2 commit - `4c365c1`, 2026-08-28

| Property | Value |
|---|---|
| Commit | `4c365c1` on `main`, parent `6c132d6` |
| Scope | 3 files, 890 insertions, 5 deletions |
| Changed | `server/ws_bridge.py` 4,414 B -> 4,514 B, SHA256 `BD8904CD9564D7FA07AF4566CF2B41ACD10774A4C02D46A633CE2B68FB2AD3F6` |
| Added | `patch_ws_cid_redact_v2c.py`, `SDP-WS-EVENT-CHANNEL-2026-08-26-revB.md` |
| Staging method | Explicit paths only, never `-A`; staged count verified at exactly 3 before committing |
| Excluded | `ws_bridge.py.bak_cidredactv2_20260826_083355` and 12 other dirty files in the tree |
| Remotes | `6c132d6..4c365c1` fast-forward on BOTH; `git ls-remote --heads` returned the identical hash from each |
| Rollback | `git revert 4c365c1`, or restore the backup and restart |

EOL NOTE, so a future window does not read it as damage: the commit emitted
`warning: in the working copy of 'src/openjarvis/server/ws_bridge.py', CRLF will
be replaced by LF the next time Git touches it`. The working copy is CRLF and the
committed blob is LF. That is autocrlf normalization, not corruption. Any EOL
measurement taken from a fresh clone will differ from one taken on this working
copy, and the difference is expected. This bears directly on the unresolved
`_stubs.py` EOL contradiction in section 7.6 - re-measure, do not inherit.

PATCH DISCIPLINE, two items from the v2 work worth carrying into the methodology
chapter:

- A MARKER IS NOT AUTOMATICALLY A UNIQUE ANCHOR. `# openjarvis-ws-cid-redact-v1`
  appears TWICE in `ws_bridge.py` at identical indent - forward-loop block and
  accept-site block. The v2 patch located the forward-loop instance positionally
  with an assertion, and deliberately left the accept-site marker at v1 because
  that block did not change.
- WRITE CONTROL EXPECTATIONS AGAINST THE POST STATE. Two dry runs aborted on
  control-authoring errors, not patch errors: a non-unique anchor, and a needle
  whose expected count was computed against the pre-patch file while the control
  ran against the patched text. Both were caught before anything was written.
  The dry-run-before-apply discipline is what made two authoring errors cost
  nothing.
""",
)


def main():
    apply = "--apply" in sys.argv

    with open(SRC, "rb") as f:
        raw = f.read()

    print("SOURCE: %s" % SRC)
    print("  bytes    : %d (expected %d)" % (len(raw), EXPECT_SRC_BYTES))
    print("  sha256   : %s" % hashlib.sha256(raw).hexdigest().upper())
    print("  CRLF     : %d   bare LF: %d" % (raw.count(b"\r\n"), raw.count(b"\n") - raw.count(b"\r\n")))
    print("  non-ascii: %d" % sum(1 for b in raw if b > 127))

    if len(raw) != EXPECT_SRC_BYTES:
        print("\nABORT: source size does not match the expected revB byte count.")
        return 2
    if raw.count(b"\r\n") != 0:
        print("\nABORT: source is not pure LF. Refusing to rewrite EOLs silently.")
        return 2

    text = raw.decode("ascii")

    print("\nCONTROLS (%d edits):" % len(EDITS))
    ok = True
    for name, old, new, count in EDITS:
        found = text.count(old)
        status = "OK " if found == count else "FAIL"
        if found != count:
            ok = False
        print("  [%s] %-52s expected %d, found %d" % (status, name[:52], count, found))

    if not ok:
        print("\nABORT: at least one anchor did not match its expected count.")
        print("Nothing written. Fix the anchor, do not loosen the assertion.")
        return 2

    out = text
    for name, old, new, count in EDITS:
        out = out.replace(old, new, count)

    ob = out.encode("ascii")

    print("\nRESULT:")
    print("  bytes    : %d -> %d (delta %+d)" % (len(raw), len(ob), len(ob) - len(raw)))
    print("  sha256   : %s" % hashlib.sha256(ob).hexdigest().upper())
    print("  CRLF     : %d   bare LF: %d" % (ob.count(b"\r\n"), ob.count(b"\n") - ob.count(b"\r\n")))
    print("  non-ascii: %d" % sum(1 for b in ob if b > 127))

    # post-state assertions
    checks = [
        ("REVISION C header present", "REVISION C, 2026-08-28, post-W14" in out, True),
        ("v2 marker named", "openjarvis-ws-cid-redact-v2" in out, True),
        ("commit of record 4c365c1", out.count("4c365c1") >= 4, True),
        ("section 6.5 created", "### 6.5 Part three" in out, True),
        ("section 10.1 created", "### 10.1 The v2 commit" in out, True),
        ("old 'STILL CARRIES' claim gone", "STILL CARRIES `confirm_id` UNREDACTED" not in out, True),
        ("old HALF IMPLEMENTED claim gone", "posture is HALF IMPLEMENTED" not in out, True),
        ("3.3 no longer says REQUEST only", "For `TOOL_CONFIRM_REQUEST` only:" not in out, True),
    ]
    print("\nPOST-STATE ASSERTIONS:")
    for label, result, want in checks:
        if result != want:
            ok = False
        print("  [%s] %s" % ("OK " if result == want else "FAIL", label))

    if not ok:
        print("\nABORT: post-state assertion failed. Nothing written.")
        return 2

    if ob.count(b"\r\n") != 0:
        print("\nABORT: output is not pure LF. Nothing written.")
        return 2

    if not apply:
        print("\nDRY RUN CLEAN. Nothing written. Re-run with --apply to write %s" % DST)
        return 0

    with open(DST, "wb") as f:
        f.write(ob)

    with open(DST, "rb") as f:
        back = f.read()

    print("\nWRITTEN: %s" % DST)
    print("  predicted %d bytes, actual %d bytes" % (len(ob), len(back)))
    print("  round trip byte-identical: %s" % (back == ob))
    if back != ob:
        print("  ABORT-AFTER-WRITE: file on disk does not match what was generated.")
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
