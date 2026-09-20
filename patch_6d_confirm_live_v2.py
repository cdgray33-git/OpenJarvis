"""
6d - make the Defect 6 confirmation gate LIVE on PATH 1 (the chat path).

v2. v1 aborted correctly: serve.py is CRLF-majority (574 CRLF / 22 bare
LF), so splitting on "\\n" leaves a trailing "\\r" as line content and the
anchor strings did not carry it. v2 compares anchors with "\\r" stripped
and writes inserted lines WITH "\\r" so they match surrounding style.

Target: src\\openjarvis\\cli\\serve.py
Marker: openjarvis-confirm-live-v1

Adds `interactive` and `confirm_callback` to `agent_kwargs` immediately
before `agent = agent_cls(engine, model_name, **agent_kwargs)`.
No signature changes anywhere. Opt-in per server run via
OPENJARVIS_CONFIRM_INTERACTIVE (default ON for this path; set 0 to disable).

Safety: marker check, byte-exact anchor check (\\r-normalized), ast.parse
before writing, CRLF accounting, bare-LF count must be unchanged.
"""

import ast
import hashlib
import os
import re
import sys

TARGET = os.path.join("src", "openjarvis", "cli", "serve.py")
MARKER = "openjarvis-confirm-live-v1"

EXPECTED_ANCHOR = [
    '                if getattr(agent_cls, "accepts_tools", False):',
    '                    agent_kwargs["max_turns"] = config.agent.max_turns',
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

BARE_LF = re.compile(r"(?<!\r)\n")


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
    pre_bare = len(BARE_LF.findall(raw))
    print("PRE  size    :", pre_size)
    print("PRE  sha256  :", sha256(TARGET))
    print("PRE  CRLF    :", pre_crlf, " BARE-LF:", pre_bare)

    if MARKER in raw:
        print("ABORT: marker already present. Patch already applied.")
        return 1

    lines = raw.split("\n")
    if "\n".join(lines) != raw:
        print("ABORT: split/join round-trip is not byte-identical.")
        return 1
    print("ROUND-TRIP   : byte-identical OK")

    # Anchor is lines 285-288 (1-based) -> indices 284-287.
    start = 284
    actual = lines[start:start + 4]
    stripped = [ln[:-1] if ln.endswith("\r") else ln for ln in actual]
    if stripped != EXPECTED_ANCHOR:
        print("ABORT: anchor mismatch at lines 285-288.")
        for i, (got, want) in enumerate(zip(stripped, EXPECTED_ANCHOR)):
            if got != want:
                print("  BAD line %d" % (285 + i))
                print("     got  [%s]" % got)
                print("     want [%s]" % want)
            else:
                print("  OK  line %d" % (285 + i))
        return 1

    crlf_style = [ln.endswith("\r") for ln in actual]
    print("ANCHOR       : byte-exact at 285-288 OK")
    print("ANCHOR CRLF  :", crlf_style)

    insert_lines = INSERT.split("\n")
    if insert_lines and insert_lines[-1] == "":
        insert_lines = insert_lines[:-1]
    # Blank separator line after the block.
    insert_lines = insert_lines + [""]
    # Match surrounding CRLF style.
    insert_lines = [ln + "\r" for ln in insert_lines]

    new_lines = lines[:287] + insert_lines + lines[287:]
    new_raw = "\n".join(new_lines)

    try:
        ast.parse(new_raw.replace("\r\n", "\n"))
    except SyntaxError as exc:
        print("ABORT: ast.parse failed on the patched content:", exc)
        return 1
    print("AST PARSE    : OK")

    post_crlf = new_raw.count("\r\n")
    post_bare = len(BARE_LF.findall(new_raw))
    want_crlf = pre_crlf + len(insert_lines)
    if post_crlf != want_crlf:
        print("ABORT: CRLF %d, expected %d" % (post_crlf, want_crlf))
        return 1
    if post_bare != pre_bare:
        print("ABORT: bare-LF changed %d -> %d" % (pre_bare, post_bare))
        return 1
    print("CRLF CHECK   : %d (+%d inserted) OK" % (post_crlf, len(insert_lines)))
    print("BARE-LF CHECK: unchanged (%d) OK" % post_bare)

    with open(TARGET, "w", encoding="utf-8", newline="") as fh:
        fh.write(new_raw)

    post_size = os.path.getsize(TARGET)
    print("")
    print("WRITTEN.")
    print("POST size    :", post_size, "(delta +%d)" % (post_size - pre_size))
    print("POST sha256  :", sha256(TARGET))
    print("INSERTED     : lines 288-%d" % (287 + len(insert_lines)))
    print("")
    print("Verify next. Do NOT stack another change on this.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
