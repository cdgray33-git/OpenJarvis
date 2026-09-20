"""
patch_confirm_resolved.py
6e backend half: add the TOOL_CONFIRM_RESOLVED emit at the confirmation gate.

Marker: openjarvis-confirm-resolved-v1
Target: src/openjarvis/tools/_stubs.py
Insert: after CURRENT_CONFIRM_ID.reset(_token), before the `if not _approved:` branch,
        so approved / denied / timeout all share one emit site.

Run from the repo root:  PS C:\\Users\\Admin\\OpenJarvis>
    python .\\patch_confirm_resolved.py

Idempotent. Aborts if already applied. Writes a timestamped .bak first.
"""

import datetime
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent
TARGET = ROOT / "src" / "openjarvis" / "tools" / "_stubs.py"
MARKER = "openjarvis-confirm-resolved-v1"

ANCHOR = (
    "                CURRENT_CONFIRM_ID.reset(_token)\n"
    "            if not _approved:\n"
)

INSERT = (
    "                CURRENT_CONFIRM_ID.reset(_token)\n"
    "            # " + MARKER + "\n"
    "            _resolved = _cr.get(_cid) or {}\n"
    "            _decision = _resolved.get(\"decision\") or (\n"
    "                _cr.APPROVED if _approved else _cr.TIMEOUT\n"
    "            )\n"
    "            if self._bus:\n"
    "                self._bus.publish(\n"
    "                    EventType.TOOL_CONFIRM_RESOLVED,\n"
    "                    {\n"
    "                        \"confirm_id\": _cid,\n"
    "                        \"agent_id\": self._agent_id,\n"
    "                        \"turn_id\": CURRENT_TURN_ID.get(),\n"
    "                        \"tool\": tool_call.name,\n"
    "                        \"decision\": _decision,\n"
    "                        \"state\": _resolved.get(\"state\"),\n"
    "                        \"created_at\": _resolved.get(\"created_at\"),\n"
    "                        \"expires_at\": _resolved.get(\"expires_at\"),\n"
    "                        \"reaped\": not _resolved,\n"
    "                    },\n"
    "                )\n"
    "            if not _approved:\n"
)


def fail(msg):
    print("ABORT: " + msg)
    sys.exit(1)


def main():
    if not TARGET.exists():
        fail("target not found: " + str(TARGET))

    # Guard 1: the event type must actually be defined in the enum.
    src_dir = ROOT / "src" / "openjarvis"
    defined = False
    where = ""
    for p in src_dir.rglob("*.py"):
        try:
            txt = p.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        if re.search(r"^\s*TOOL_CONFIRM_RESOLVED\s*=", txt, re.M):
            defined = True
            where = str(p.relative_to(ROOT))
            break
    if not defined:
        fail(
            "EventType.TOOL_CONFIRM_RESOLVED is not defined anywhere in "
            "src/openjarvis. Do not patch a publish for an event type that "
            "does not exist."
        )
    print("OK  EventType.TOOL_CONFIRM_RESOLVED defined in: " + where)

    text = TARGET.read_text(encoding="utf-8")

    # Guard 2: idempotence.
    if MARKER in text:
        print("ALREADY APPLIED: marker " + MARKER + " present. No change made.")
        return

    count = text.count(ANCHOR)
    if count != 1:
        fail(
            "anchor matched " + str(count) + " times, expected exactly 1. "
            "The gate region has changed since it was read. Do not patch blind."
        )

    stamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    bak = TARGET.with_suffix(TARGET.suffix + ".bak-" + stamp)
    bak.write_text(text, encoding="utf-8")
    print("OK  rollback point written: " + str(bak.relative_to(ROOT)))

    patched = text.replace(ANCHOR, INSERT, 1)
    TARGET.write_text(patched, encoding="utf-8")
    print("OK  patched: " + str(TARGET.relative_to(ROOT)))

    # Compile check.
    import py_compile

    try:
        py_compile.compile(str(TARGET), doraise=True)
    except py_compile.PyCompileError as exc:
        print("COMPILE FAILED - restoring from backup")
        TARGET.write_text(text, encoding="utf-8")
        fail("syntax error after patch, file restored: " + str(exc))
    print("OK  compiles clean")

    print("")
    print("ROLLBACK COMMAND (PowerShell, repo root):")
    print(
        "  Copy-Item '"
        + str(bak.relative_to(ROOT))
        + "' '"
        + str(TARGET.relative_to(ROOT))
        + "' -Force"
    )


if __name__ == "__main__":
    main()
