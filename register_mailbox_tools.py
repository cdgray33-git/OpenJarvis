#!/usr/bin/env python3
"""Register mailbox_tools in openjarvis/tools/__init__.py.

marker: openjarvis-register-mailbox-tools-v1

The tools package imports every built-in tool module at import time so the
``@ToolRegistry.register()`` decorators fire. ``mailbox_tools`` is not in
that list, so its five tools never reach ``MCPServer._auto_discover_tools``
and the agent cannot see them. This adds one try/except block matching the
25 already in the file.

Dry run by default. Stdlib only.

    python register_mailbox_tools.py
    python register_mailbox_tools.py --apply
"""

from __future__ import annotations

import argparse
import ast
import hashlib
import os
import shutil
import sys
import time

MARKER = "openjarvis-register-mailbox-tools-v1"
REL_TARGET = os.path.join("src", "openjarvis", "tools", "__init__.py")

ANCHOR = '__all__ = ["BaseTool", "ToolExecutor", "ToolSpec"]'

BLOCK_LINES = [
    "try:",
    "    import openjarvis.tools.mailbox_tools  # noqa: F401",
    "except ImportError:",
    "    pass",
    "",
]

IDEMPOTENCY_TOKEN = "openjarvis.tools.mailbox_tools"


def sha256_of(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest().upper()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply", action="store_true", help="Write the change")
    parser.add_argument("--path", default=".", help="Repo root (default: cwd)")
    args = parser.parse_args()

    root = os.path.abspath(args.path)
    target = os.path.join(root, REL_TARGET)

    print("marker : %s" % MARKER)
    print("target : %s" % target)

    if not os.path.isfile(target):
        print("ERROR  : target not found", file=sys.stderr)
        return 2

    with open(target, "rb") as fh:
        original = fh.read()

    print(
        "before : %d bytes / SHA256 %s" % (len(original), sha256_of(original))
    )

    text = original.decode("utf-8")

    if IDEMPOTENCY_TOKEN in text:
        print("\nalready registered. Nothing to do.")
        return 0

    # Preserve the file's existing line terminator.
    newline = "\r\n" if b"\r\n" in original else "\n"

    count = text.count(ANCHOR)
    if count != 1:
        print(
            "\nERROR  : anchor matched %d times, expected exactly 1" % count,
            file=sys.stderr,
        )
        print("anchor : %s" % ANCHOR, file=sys.stderr)
        return 3
    print("\nanchor check:")
    print("  ok   __all__ line matched, exactly once")

    block = newline.join(BLOCK_LINES) + newline
    patched = text.replace(ANCHOR, block + ANCHOR, 1)

    try:
        ast.parse(patched)
    except SyntaxError as exc:
        print("\nERROR  : patched source does not parse: %s" % exc, file=sys.stderr)
        return 4
    print("compile: OK (patched source parses)")

    encoded = patched.encode("utf-8")
    predicted = sha256_of(encoded)
    print("\n  inserting before __all__:")
    for line in BLOCK_LINES[:-1]:
        print("    %s" % line)

    print(
        "\nafter  : %d bytes / SHA256 %s (predicted)" % (len(encoded), predicted)
    )
    print(
        "delta  : %+d bytes / %+d lines"
        % (len(encoded) - len(original), len(BLOCK_LINES))
    )

    if not args.apply:
        print("\nDRY RUN. No changes written. Re-run with --apply to write.")
        return 0

    stamp = time.strftime("%Y%m%d_%H%M%S")
    backup = "%s.bak_%s" % (target, stamp)
    shutil.copy2(target, backup)
    print("\nbackup : %s" % backup)

    with open(target, "wb") as fh:
        fh.write(encoded)

    with open(target, "rb") as fh:
        on_disk = fh.read()
    actual = sha256_of(on_disk)
    print("written: %d bytes / SHA256 %s" % (len(on_disk), actual))

    if actual != predicted:
        print("VERIFY : MISMATCH. Restore from the backup above.", file=sys.stderr)
        return 5

    print("VERIFY : on-disk hash matches prediction. PATCH APPLIED.")
    print("")
    print("NEXT   : confirm the agent can see the tools:")
    print("  uv run python -c \"from openjarvis.mcp.server import MCPServer;\\")
    print("    print([t.spec.name for t in MCPServer().get_tools()\\")
    print("    if t.spec.name.startswith('mailbox_')])\"")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
