#!/usr/bin/env python
"""
patch_agent_log.py  --  OpenJarvis Patch 3 of 3
Marker: openjarvis-agent-log-v1

Adds a turn-boundary instrument to src/openjarvis/agents/native_openhands.py.

Writes %LOCALAPPDATA%\\OpenJarvis\\logs\\agent.log  (2.5 MB x 4, own rotating
handler, propagate=False) beside the existing dispatch.log, and SETS the
contextvar openjarvis.tools._stubs.CURRENT_TURN_ID at the start of every turn
so dispatch.log lines carry a real turn id instead of "-".

Records per run: run id, agent class, model, conversation id, tool count,
max_turns, input size.  Per turn: turn id and turn number.  Per exit: which of
the three exits was taken, turn count, number of dispatched tool results, and
the head of the final generation.

Anchors are matched on STRIPPED LINE TEXT, never on line numbers, and each
anchor must match exactly once or the patch aborts.  Indentation is taken from
the matched line itself.

Usage (PowerShell, repo root):
    python .\\patch_agent_log.py            # dry run, writes nothing
    python .\\patch_agent_log.py --apply    # takes .bak_ copy, then writes
"""

import ast
import datetime
import os
import shutil
import sys

MARKER = "openjarvis-agent-log-v1"
TARGET = os.path.join("src", "openjarvis", "agents", "native_openhands.py")

# ---------------------------------------------------------------- helper block

HELPER_BLOCK = '''
# --- openjarvis-agent-log-v1 -------------------------------------------------
# Turn-boundary record in its own rotating file, so an agent turn that
# dispatched NOTHING is distinguishable from one that was never instrumented.
# Also sets tools._stubs.CURRENT_TURN_ID (a ContextVar) so dispatch.log lines
# carry a real turn id.  Every call site is exception-swallowing on purpose:
# instrumentation must never be able to break a run.
_oj_agent_logger = None


def _oj_get_agent_logger():
    global _oj_agent_logger
    if _oj_agent_logger is not None:
        return _oj_agent_logger
    import logging as _lgm
    import logging.handlers as _lgh
    import os as _os

    lg = _lgm.getLogger("openjarvis.agent")
    if not lg.handlers:
        log_dir = _os.path.join(
            _os.environ.get("LOCALAPPDATA", _os.path.expanduser("~")),
            "OpenJarvis", "logs",
        )
        try:
            _os.makedirs(log_dir, exist_ok=True)
            h = _lgh.RotatingFileHandler(
                _os.path.join(log_dir, "agent.log"),
                maxBytes=2621440, backupCount=4, encoding="utf-8",
            )
            h.setFormatter(_lgm.Formatter("%(asctime)s %(levelname)s %(message)s"))
            lg.addHandler(h)
        except Exception:
            lg.addHandler(_lgm.NullHandler())
    lg.setLevel(_lgm.INFO)
    lg.propagate = False
    _oj_agent_logger = lg
    return lg


def _oj_conv_id(context):
    for attr in ("conversation_id", "session_id", "thread_id", "id"):
        v = getattr(context, attr, None)
        if v:
            return str(v)
    meta = getattr(context, "metadata", None)
    if isinstance(meta, dict):
        for k in ("conversation_id", "session_id", "thread_id"):
            if meta.get(k):
                return str(meta[k])
    return "-"


def _oj_model_name(agent):
    for attr in ("_model", "model", "_model_name"):
        v = getattr(agent, attr, None)
        if isinstance(v, str) and v:
            return v
    llm = getattr(agent, "_llm", None) or getattr(agent, "llm", None)
    for attr in ("model", "model_name", "_model"):
        v = getattr(llm, attr, None)
        if isinstance(v, str) and v:
            return v
    return "-"


def _oj_run_start(agent, context, input_text):
    import uuid as _uuid

    run_id = _uuid.uuid4().hex[:8]
    try:
        _oj_get_agent_logger().info(
            "RUNSTART run=%s agent=%s model=%s conv=%s tools=%d maxturns=%s chars=%d",
            run_id,
            type(agent).__name__,
            _oj_model_name(agent),
            _oj_conv_id(context),
            len(getattr(agent, "_tools", []) or []),
            getattr(agent, "_max_turns", "-"),
            len(input_text or ""),
        )
    except Exception:
        pass
    return run_id


def _oj_set_turn(run_id, turns):
    turn_id = "%s-t%d" % (run_id, turns)
    try:
        from openjarvis.tools._stubs import CURRENT_TURN_ID as _cti

        _cti.set(turn_id)
    except Exception:
        pass
    try:
        _oj_get_agent_logger().info(
            "TURN run=%s turn=%s n=%d", run_id, turn_id, turns
        )
    except Exception:
        pass
    return turn_id


def _oj_run_end(run_id, kind, turns, tool_results, content):
    try:
        head = (content or "")[:160].replace("\\n", " ").replace("\\r", " ")
        _oj_get_agent_logger().info(
            "RUNEND run=%s exit=%s turns=%s dispatched=%d chars=%d head=%s",
            run_id, kind, turns,
            len(tool_results or []),
            len(content or ""),
            head,
        )
    except Exception:
        pass


# --- end openjarvis-agent-log-v1 ---------------------------------------------

'''

# ---------------------------------------------------------------- edit plan
# (anchor_stripped, position, [lines to insert, unindented], description)

EDITS = [
    (
        "self._emit_turn_start(input)",
        "after",
        ["_oj_run_id = _oj_run_start(self, context, input)"],
        "run start record",
    ),
    (
        "self._emit_turn_end(turns=1)",
        "before",
        ['_oj_run_end(_oj_run_id, "urldirect", 1, [], content)'],
        "exit 1 of 3 - URL-expansion early return",
    ),
    (
        "turns += 1",
        "after",
        ["_oj_turn_id = _oj_set_turn(_oj_run_id, turns)"],
        "turn boundary - sets CURRENT_TURN_ID",
    ),
    (
        "self._emit_turn_end(turns=turns)",
        "before",
        ['_oj_run_end(_oj_run_id, "final", turns, all_tool_results, content)'],
        "exit 2 of 3 - final answer (the Defect 1 exit)",
    ),
    (
        "result = self._max_turns_result(all_tool_results, turns, content=final)",
        "before",
        ['_oj_run_end(_oj_run_id, "maxturns", turns, all_tool_results, final)'],
        "exit 3 of 3 - max turns exhausted",
    ),
]

HELPER_ANCHOR = '__all__ = ["NativeOpenHandsAgent"]'


def fail(msg):
    print("ABORT: " + msg)
    sys.exit(1)


def find_unique(lines, needle):
    hits = [i for i, ln in enumerate(lines) if ln.strip() == needle]
    if len(hits) == 0:
        fail("anchor not found: " + needle)
    if len(hits) > 1:
        fail(
            "anchor matched %d times (must be 1): %s -> lines %s"
            % (len(hits), needle, [h + 1 for h in hits])
        )
    return hits[0]


def main():
    apply = "--apply" in sys.argv

    if not os.path.isfile(TARGET):
        fail("target not found: " + TARGET + " (run from the repo root)")

    # newline="" preserves the file's existing line endings instead of letting
    # text mode rewrite every line. v1 of this script did NOT do this and turned
    # a 20,990 B LF file into a 25,645 B CRLF file on apply.
    with open(TARGET, "r", encoding="utf-8", newline="") as f:
        original = f.read()

    eol = "\r\n" if "\r\n" in original else "\n"
    print("line endings detected: %s" % ("CRLF" if eol == "\r\n" else "LF"))

    if MARKER in original:
        fail("marker " + MARKER + " already present - patch is already applied")

    lines = original.split(eol)
    print("target : %s" % TARGET)
    print("size   : %d bytes, %d lines" % (len(original.encode("utf-8")), len(lines)))
    print("")

    # Resolve every anchor against the ORIGINAL file first, so the report shows
    # true pre-patch line numbers and one bad anchor aborts before any edit.
    plan = []
    for needle, pos, payload, desc in EDITS:
        idx = find_unique(lines, needle)
        indent = lines[idx][: len(lines[idx]) - len(lines[idx].lstrip())]
        plan.append((idx, pos, payload, indent, desc, needle))
        print("  line %4d  %-6s  %s" % (idx + 1, pos, desc))
        print("             anchor: %s" % needle)

    helper_idx = find_unique(lines, HELPER_ANCHOR)
    print("  line %4d  before  helper block (%d lines)"
          % (helper_idx + 1, len(HELPER_BLOCK.split("\n"))))
    print("")

    # Apply from the bottom up so earlier indices stay valid.
    out = list(lines)
    ops = sorted(plan, key=lambda p: p[0], reverse=True)

    out[helper_idx:helper_idx] = HELPER_BLOCK.split("\n")

    for idx, pos, payload, indent, desc, needle in ops:
        if idx > helper_idx:
            fail("unexpected: edit anchor below the helper anchor")
        at = idx + 1 if pos == "after" else idx
        out[at:at] = [indent + p for p in payload]

    patched = eol.join(out)

    try:
        ast.parse(patched)
    except SyntaxError as e:
        fail("ast.parse FAILED on the patched text: %s (line %s)" % (e.msg, e.lineno))
    print("ast.parse: OK")

    delta = len(patched.encode("utf-8")) - len(original.encode("utf-8"))
    print("new size : %d bytes (%+d)" % (len(patched.encode("utf-8")), delta))
    print("")

    if not apply:
        print("DRY RUN - nothing written. Re-run with --apply to write.")
        return

    stamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    bak = TARGET + ".bak_agentlog_" + stamp
    shutil.copy2(TARGET, bak)
    print("backup   : " + bak)

    with open(TARGET, "w", encoding="utf-8", newline="") as f:
        f.write(patched)

    on_disk = os.path.getsize(TARGET)
    expected = len(patched.encode("utf-8"))
    if on_disk != expected:
        print("APPLIED  : " + TARGET)
        fail(
            "SIZE MISMATCH - on disk %d, expected %d. Restore the backup:\n"
            "  Copy-Item '%s' '%s' -Force" % (on_disk, expected, bak, TARGET)
        )
    print("APPLIED  : %s (%d bytes on disk, matches prediction)" % (TARGET, on_disk))
    print("")
    print("ROLLBACK : Copy-Item '%s' '%s' -Force" % (bak, TARGET))


if __name__ == "__main__":
    main()
