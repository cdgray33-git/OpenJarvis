"""patch_confirm_emit.py - Defect 6 / 6c STEP 3

Marker: openjarvis-confirm-emit-v1
Target: C:\\Users\\Admin\\OpenJarvis\\src\\openjarvis\\tools\\_stubs.py

Two anchored edits:
  1) module level - add CURRENT_CONFIRM_ID ContextVar directly after CURRENT_TURN_ID
  2) the confirmation gate - register in confirm_registry, emit
     EventType.TOOL_CONFIRM_REQUEST guarded by `if self._bus:` with seven
     fields and agent_id INSIDE data, build the prompt from _args_digest
     (not the raw params dict), and on a False callback return re-read the
     registry to distinguish DENIED from TIMEOUT.

Dry run by default. Pass --apply to write.
"""

import ast
import datetime
import hashlib
import os
import re
import sys

TARGET = r"C:\Users\Admin\OpenJarvis\src\openjarvis\tools\_stubs.py"
MARKER = "openjarvis-confirm-emit-v1"

# Positive controls - text that MUST already be in the file and MUST survive.
CONTROLS = [
    "openjarvis-dispatch-log-v1",
    "openjarvis-tool-timeout-v1",
    "ATTEMPT turn=%s tool=%s args=%s thread=%s",
    "def _args_digest(",
    "self._agent_id",
    "EventType.TOOL_CALL_START",
]

# Encoding control - this line carries a non-ASCII em dash. If our write
# mangles the encoding, this exact string stops matching.
ENCODING_CONTROL = "# ToolSpec \u2014 metadata describing a tool's interface"

ANCHOR2 = (
    "            prompt = f\"Allow execution of tool '{tool_call.name}' with args {params}?\"\n"
    "            if not self._confirm_callback(prompt):\n"
    "                return ToolResult(\n"
    "                    tool_name=tool_call.name,\n"
    "                    content=f\"Tool '{tool_call.name}' execution denied by user.\",\n"
    "                    success=False,\n"
    "                )\n"
)

REPLACE2 = (
    "            # " + MARKER + " - Defect 6 / 6c step 3\n"
    "            from openjarvis.core import confirm_registry as _cr\n"
    "\n"
    "            _digest = _args_digest(tool_call.arguments)\n"
    "            prompt = (\n"
    "                f\"Allow execution of tool '{tool_call.name}' \"\n"
    "                f\"with args {_digest}?\"\n"
    "            )\n"
    "            _cid = _cr.register(\n"
    "                tool=tool_call.name,\n"
    "                agent_id=self._agent_id,\n"
    "                turn_id=CURRENT_TURN_ID.get(),\n"
    "            )\n"
    "            _entry = _cr.get(_cid) or {}\n"
    "            if self._bus:\n"
    "                self._bus.publish(\n"
    "                    EventType.TOOL_CONFIRM_REQUEST,\n"
    "                    {\n"
    "                        \"confirm_id\": _cid,\n"
    "                        \"agent_id\": self._agent_id,\n"
    "                        \"turn_id\": CURRENT_TURN_ID.get(),\n"
    "                        \"tool\": tool_call.name,\n"
    "                        \"args_digest\": _digest,\n"
    "                        \"prompt\": prompt,\n"
    "                        \"expires_at\": _entry.get(\"expires_at\"),\n"
    "                    },\n"
    "                )\n"
    "            _token = CURRENT_CONFIRM_ID.set(_cid)\n"
    "            try:\n"
    "                _approved = self._confirm_callback(prompt)\n"
    "            finally:\n"
    "                CURRENT_CONFIRM_ID.reset(_token)\n"
    "            if not _approved:\n"
    "                _final = (_cr.get(_cid) or {}).get(\"decision\")\n"
    "                if _final == _cr.DENIED:\n"
    "                    _content = (\n"
    "                        f\"Tool '{tool_call.name}' execution denied by user.\"\n"
    "                    )\n"
    "                elif _final == _cr.APPROVED:\n"
    "                    _content = (\n"
    "                        f\"Tool '{tool_call.name}' was approved but the \"\n"
    "                        \"confirmation callback returned False. The tool did \"\n"
    "                        \"NOT run. Report this as an internal error, not as a \"\n"
    "                        \"refusal.\"\n"
    "                    )\n"
    "                else:\n"
    "                    _content = (\n"
    "                        f\"Tool '{tool_call.name}' was NOT executed because no \"\n"
    "                        \"confirmation answer arrived before the request \"\n"
    "                        \"expired. This is a TIMEOUT, not a refusal - the user \"\n"
    "                        \"did not deny it. Ask the user again rather than \"\n"
    "                        \"reporting that permission was refused.\"\n"
    "                    )\n"
    "                return ToolResult(\n"
    "                    tool_name=tool_call.name,\n"
    "                    content=_content,\n"
    "                    success=False,\n"
    "                )\n"
)

CTXVAR = (
    "# " + MARKER + " - lets a Callable[[str], bool] confirm callback learn\n"
    "# which confirm_id it is being asked about, without widening its signature.\n"
    "CURRENT_CONFIRM_ID = contextvars.ContextVar(\"openjarvis_confirm_id\", default=\"\")\n"
)


def fail(msg):
    print("ABORT: " + msg)
    sys.exit(1)


def main():
    apply = "--apply" in sys.argv

    if not os.path.isfile(TARGET):
        fail("target not found: " + TARGET)

    with open(TARGET, "r", encoding="utf-8", newline="") as fh:
        original = fh.read()

    pre_bytes = original.encode("utf-8")
    print("target      : " + TARGET)
    print("pre size    : %d B" % len(pre_bytes))
    print("pre sha256  : " + hashlib.sha256(pre_bytes).hexdigest().upper())

    crlf = original.count("\r\n")
    lf = original.count("\n") - crlf
    print("EOL         : %d CRLF / %d bare LF" % (crlf, lf))
    if crlf and not lf:
        eol = "\r\n"
    elif lf and not crlf:
        eol = "\n"
    elif lf > crlf:
        # MIXED, LF-dominant. Splitting on "\n" leaves each stray "\r" attached
        # to the end of that line's content, so joining on "\n" restores it.
        # Proven below rather than assumed.
        eol = "\n"
        print("EOL         : MIXED, LF-dominant - stray CR bytes ride as content")
    else:
        fail("MIXED line endings, CRLF-dominant - not handled, refusing to write")

    if eol.join(original.split(eol)) != original:
        fail("split/join round-trip is NOT byte-identical - refusing to write")
    print("round-trip  : byte-identical OK")

    def E(text):
        return text.replace("\n", eol) if eol != "\n" else text

    # --- idempotence -------------------------------------------------------
    if MARKER in original:
        fail("marker already present - patch has already been applied")

    # --- positive controls, pre-write --------------------------------------
    for ctl in CONTROLS:
        n = original.count(ctl)
        print("control     : %-45s %d" % (ctl[:45], n))
        if n < 1:
            fail("positive control missing before write: " + ctl)
    if ENCODING_CONTROL not in original:
        fail("encoding control line not found - refusing to write")
    print("encoding    : control line OK")

    # --- anchor 1: the CURRENT_TURN_ID declaration -------------------------
    lines = original.split(eol)
    hits = [i for i, ln in enumerate(lines) if ln.startswith("CURRENT_TURN_ID")]
    print("anchor 1    : CURRENT_TURN_ID declaration, %d match(es)" % len(hits))
    if len(hits) != 1:
        for i, ln in enumerate(lines):
            if "CURRENT_TURN_ID" in ln:
                print("   line %d: %s" % (i + 1, ln))
        fail("anchor 1 must match exactly 1")
    if any(ln.startswith("CURRENT_CONFIRM_ID") for ln in lines):
        fail("CURRENT_CONFIRM_ID already declared")
    print("   line %d: %s" % (hits[0] + 1, lines[hits[0]]))

    # The declaration may span several lines. Walk forward until the
    # parentheses balance so the insert lands AFTER the whole statement.
    end = hits[0]
    depth = 0
    while end < len(lines):
        depth += lines[end].count("(") - lines[end].count(")")
        if depth <= 0:
            break
        end += 1
    if end != hits[0]:
        for j in range(hits[0] + 1, end + 1):
            print("   line %d: %s" % (j + 1, lines[j]))
    print("   statement ends line %d" % (end + 1))

    ctx_lines = CTXVAR.rstrip("\n").split("\n")
    lines = lines[: end + 1] + [""] + ctx_lines + lines[end + 1:]
    candidate = eol.join(lines)

    # --- anchor 2: the gate block ------------------------------------------
    a2 = E(ANCHOR2)
    n2 = candidate.count(a2)
    print("anchor 2    : gate prompt/callback/denied block, %d match(es)" % n2)
    if n2 != 1:
        m = re.search(r"^.*requires_confirmation:.*$", candidate, re.M)
        if m:
            start = candidate.count(eol, 0, m.start())
            for i in range(start, min(start + 22, len(candidate.split(eol)))):
                print("   line %d: %s" % (i + 1, candidate.split(eol)[i]))
        fail("anchor 2 must match exactly 1 - gate text differs from the handoff")

    candidate = candidate.replace(a2, E(REPLACE2))

    # --- compile the candidate BEFORE writing ------------------------------
    try:
        ast.parse(candidate)
    except SyntaxError as exc:
        fail("candidate does not parse: %s" % exc)
    print("ast.parse   : OK")

    post_bytes = candidate.encode("utf-8")
    predicted = len(post_bytes)
    print("predicted   : %d B (delta %+d)" % (predicted, predicted - len(pre_bytes)))

    if not apply:
        print("")
        print("DRY RUN ONLY - nothing written. Re-run with --apply.")
        return

    # --- backup ------------------------------------------------------------
    stamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    bak = TARGET + ".bak_confirmemit_" + stamp
    with open(bak, "wb") as fh:
        fh.write(pre_bytes)
    print("backup      : " + bak)

    with open(TARGET, "w", encoding="utf-8", newline="") as fh:
        fh.write(candidate)

    # --- verify the write, do not merely report it -------------------------
    actual = os.path.getsize(TARGET)
    print("on disk     : %d B" % actual)
    if actual != predicted:
        print("SIZE MISMATCH - predicted %d, got %d" % (predicted, actual))
        print("RESTORE: Copy-Item '%s' '%s' -Force" % (bak, TARGET))
        sys.exit(1)

    with open(TARGET, "r", encoding="utf-8", newline="") as fh:
        after = fh.read()

    checks = [
        ("marker x2", after.count(MARKER) == 2),
        ("CURRENT_CONFIRM_ID declared", "CURRENT_CONFIRM_ID = contextvars" in after),
        ("registry import", "from openjarvis.core import confirm_registry as _cr" in after),
        ("emit guarded by self._bus", "            if self._bus:" + eol + "                self._bus.publish(" + eol + "                    EventType.TOOL_CONFIRM_REQUEST," in after),
        ("agent_id inside data", '"agent_id": self._agent_id,' in after),
        ("prompt from digest", "_digest = _args_digest(tool_call.arguments)" in after),
        ("raw params prompt gone", "with args {params}?" not in after),
        ("timeout branch", "This is a TIMEOUT, not a refusal" in after),
        ("encoding control", ENCODING_CONTROL in after),
        ("CRLF lines preserved (%d)" % crlf, after.count("\r\n") == crlf),
    ]
    for ctl in CONTROLS:
        checks.append(("control " + ctl[:32], ctl in after))

    bad = False
    for name, ok in checks:
        print("verify      : %-40s %s" % (name, "OK" if ok else "FAIL"))
        if not ok:
            bad = True

    try:
        import py_compile
        py_compile.compile(TARGET, doraise=True)
        print("py_compile  : OK")
    except Exception as exc:
        print("py_compile  : FAIL %s" % exc)
        bad = True

    print("post sha256 : " + hashlib.sha256(after.encode("utf-8")).hexdigest().upper())

    if bad:
        print("")
        print("ONE OR MORE CHECKS FAILED.")
        print("RESTORE: Copy-Item '%s' '%s' -Force" % (bak, TARGET))
        sys.exit(1)

    print("")
    print("APPLIED CLEAN.")
    print("ROLLBACK: Copy-Item '%s' '%s' -Force" % (bak, TARGET))


if __name__ == "__main__":
    main()
