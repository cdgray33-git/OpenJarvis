"""openjarvis-bind-assert-v1

Change C. Emits a runtime BIND_ASSERT log line naming the actual bind address,
the resolved loopback verdict, and the bound engine, at startup, to backend.log.

Anchors on content, never on line numbers. Idempotent: refuses to apply twice.
Writes serve.py.bak-bindassert before touching anything.
"""

from __future__ import annotations

import shutil
import sys
from pathlib import Path

TARGET = Path("src/openjarvis/cli/serve.py")
BACKUP = Path("src/openjarvis/cli/serve.py.bak-bindassert")
MARKER = "openjarvis-bind-assert-v1"

ANCHOR = """    if not _is_loop and "*" in config.server.cors_origins:"""

INSERT = '''    # openjarvis-bind-assert-v1
    # Runtime bind assertion. The confirm-channel redaction posture is
    # conditional on this bind, so the bind must be recoverable from the log.
    logger.info(
        "BIND_ASSERT host=%s port=%s loopback=%s engine=%s model=%s agent=%s",
        bind_host,
        bind_port,
        _is_loop,
        engine_name,
        model_name,
        agent_key or "none",
    )
    if not _is_loop:
        logger.warning(
            "BIND_ASSERT NON_LOOPBACK host=%s - confirm channel is exposed "
            "beyond this host. Socket auth is deliberately absent (ruling "
            "2026-08-29). Do not run this bind with untrusted network reach.",
            bind_host,
        )

'''


def main() -> int:
    if not TARGET.exists():
        print(f"FAIL: {TARGET} not found. Run from the repo root.")
        return 1

    src = TARGET.read_text(encoding="utf-8")

    if MARKER in src:
        print(f"ALREADY APPLIED: marker {MARKER} present. No change made.")
        return 0

    count = src.count(ANCHOR)
    if count != 1:
        print(f"FAIL: anchor matched {count} times, expected exactly 1.")
        print("Anchor was:")
        print(ANCHOR)
        return 1

    patched = src.replace(ANCHOR, INSERT + ANCHOR, 1)

    shutil.copy2(TARGET, BACKUP)
    TARGET.write_text(patched, encoding="utf-8")

    print(f"BACKUP WRITTEN: {BACKUP}")
    print(f"PATCH APPLIED: {TARGET}")
    print(f"lines before={len(src.splitlines())} after={len(patched.splitlines())}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
