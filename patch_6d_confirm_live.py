"""
6d - make the Defect 6 confirmation gate LIVE on PATH 1 (the chat path).

Target: src\\openjarvis\\cli\\serve.py
Marker: openjarvis-confirm-live-v1

What it does: adds `interactive` and `confirm_callback` to `agent_kwargs`
immediately before `agent = agent_cls(engine, model_name, **agent_kwargs)`.
No signature changes anywhere. Opt-in per server run via the env var
OPENJARVIS_CONFIRM_INTERACTIVE (default ON for this path - a human is
always at the chat UI; set it to 0 to disable without editing code).

Safety:
  - refuses to run twice (marker check)
  - refuses to run if the anchor lines are not byte-exact
  - ast.parse before writing
  - CRLF count must be unchanged after writing (this file is MIXED:
    574 CRLF / 22 bare LF - stray \\r rides as line content)
Read-only until every check passes.
"""

import ast
import hashlib
import os
import sys

TARGET = os.path.join("src", "openjarvis", "cli", "serve.py")
MARKER = "openjarvis-confirm-live-v1"

EXPECTED_ANCHOR = [
    '                if getattr(agent_cls, "accepts_tools", False):',
    "                    agent_kwargs[\"max_turns\"] = config.agent.max_turns",
    "",
    "                agent = agent_cls(engine, model_name, **agent_kwargs)",
]

INSERT = '''                # openjarvis-confirm-live-v1
                # Defect 6 / 6d: make the confirmation gate live on the chat
                # path. The agent forwards these straight to its ToolExecutor
                # (agents\\_stubs.py:325-332). Opt-in per server run so that
                # unattended entry points never inherit a blocking gate.
                if getattr(agent_cls, "accepts_tools", False):
                    import os as _os

                    _confirm_flag = _os.getenv(
                        "OPENJARVIS_CONFIRM_INTERACTIVE", "1"
                    )
                    if _confirm_flag.strip().lower() not in (
                        "0",
                        "false",
                        "no",
                        "off",
                    ):
                        from openjarvis.core import confirm_registry as _cr
                        from openjarvis.tools import _stubs as _confirm_stubs

                        def _server_confirm_callback(_prompt: str) -> bool:
                            _cid = _confirm_stubs.CURRENT_CONFIRM_ID.get()
                            if not _cid:
                                return False
                            return _cr.wait(_cid) == _cr.APPROVED

                        agent_kwargs["interactive"] = True
                        agent_kwargs["confirm_callback"] = (
                            _server_confirm_callback
                        )
'''


def sha256(path):
    with open(path, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest().upper()


def main():
    print("SCRIPT :", os.path.abspath(__file__))
    print("TARGET :", os.path.abspath(TARGET))

    if not os.path.exists(TARGET):
        print("ABORT: target not found. Run from the repo root.")
        return 1

    with open(TARGET, "r", encoding="utf-8", newline="") as fh:
        raw = fh.read()

    pre_size = len(raw.encode("utf-8"))
    pre_crlf = raw.count("\r\n")
    print("PRE  size   :", pre_size)
    print("PRE  sha256 :", sha256(TARGET))
    print("PRE  CRLF   :", pre_crlf)

    if MARKER in raw:
        print("ABORT: marker already present. Patch already applied.")
        return 1

    lines = raw.split("\n")
    if "\n".join(lines) != raw:
        print("ABORT: split/join round-trip is not byte-identical.")
        return 1
    print("ROUND-TRIP  : byte-identical OK")

    # Anchor is lines 285-288 (1-based) -> indices 284-287.
    start = 284
    actual = lines[start:start + 4]
    if actual != EXPECTED_ANCHOR:
        print("ABORT: anchor mismatch at lines 285-288.")
        for i, (got, want) in enumerate(zip(actual, EXPECTED_ANCHOR)):
            flag = "OK " if got == want else "BAD"
            print("  %s %d" % (flag, 285 + i))
            if got != want:
                print("     got  [%s]" % got)
                print("     want [%s]" % want)
        return 1
    print("ANCHOR      : byte-exact at 285-288 OK")

    insert_lines = INSERT.split("\n")
    if insert_lines and insert_lines[-1] == "":
        insert_lines = insert_lines[:-1]

    # Insert before line 288 (index 287), i.e. before the agent construction.
    new_lines = lines[:287] + insert_lines + [""] + lines[287:]
    new_raw = "\n".join(new_lines)

    try:
        ast.parse(new_raw.replace("\r\n", "\n"))
    except SyntaxError as exc:
        print("ABORT: ast.parse failed on the patched content:", exc)
        return 1
    print("AST PARSE   : OK")

    post_crlf = new_raw.count("\r\n")
    if post_crlf != pre_crlf:
        print("ABORT: CRLF count changed %d -> %d" % (pre_crlf, post_crlf))
        return 1
    print("CRLF CHECK  : unchanged (%d)" % post_crlf)

    with open(TARGET, "w", encoding="utf-8", newline="") as fh:
        fh.write(new_raw)

    post_size = os.path.getsize(TARGET)
    print("")
    print("WRITTEN.")
    print("POST size   :", post_size, "(delta +%d)" % (post_size - pre_size))
    print("POST sha256 :", sha256(TARGET))
    print("INSERTED    : lines 288-%d" % (287 + len(insert_lines) + 1))
    print("")
    print("Verify next. Do NOT stack another change on this.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
