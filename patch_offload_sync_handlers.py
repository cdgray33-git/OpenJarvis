#!/usr/bin/env python3
"""
patch_offload_sync_handlers.py

DEFECT
  src/openjarvis/server/routes.py, chat_completions (async def, :47) calls two
  synchronous handlers without awaiting them:

    :162   return _handle_agent(agent, model, request_body, complexity_info)
    :165   return _handle_direct(engine, model, request_body, bus=..., ...)

  Both are plain `def`. Calling them from a coroutine runs them to completion
  ON THE EVENT LOOP THREAD, so the entire server is unresponsive for the whole
  duration of the request - not just this route. Health checks, the UI, other
  clients, and WebSocket frame delivery all stop.

EVIDENCE
  _handle_agent  : MEASURED. ws_probe.py run 2026-08-23 07:36:50 recorded 23
                   consecutive HTTP /health timeouts spanning t+3.2 to t+256,
                   beginning at the chat POST and ending when it returned. WS
                   pong went from 0.001 s to a 120 s timeout over the same
                   span. 18 event frames were delivered in a single 7 ms burst
                   on release. Loop healthy before, healthy after.
  _handle_direct : SHAPE-CONFIRMED, not measured. :189 instrumented_generate
                   and :199 engine.generate are synchronous calls in a plain
                   def, same call pattern. Blocks for one inference rather
                   than a full tool loop.

FIX
  Wrap both in asyncio.to_thread. This is the idiom already used by this
  codebase for exactly this purpose at server/stream_bridge.py:155, which is
  why the STREAMING agent path does not exhibit the defect. We are applying
  the house pattern two frames up the stack, not inventing one.

NOT IN SCOPE
  - The two 120 s confirm cycles observed in one turn. Real, carried, and
    unaffected by this patch: it stops them freezing the server, it does not
    shorten them.
  - The dead `bus` lookup at :164, unreachable because :161 returns first.
  - confirm_registry's docstring claim that the loop stays free, which this
    run disproved for the non-streaming path.

Idempotent. Safe to re-run. Exits nonzero and changes nothing on any failure.
"""

import ast
import datetime
import py_compile
import shutil
import sys
import tempfile
from pathlib import Path

TARGET = Path("src/openjarvis/server/routes.py")
MARKER = "openjarvis-offload-sync-handlers-v1"

OLD_AGENT = """    if agent is not None:
        return _handle_agent(agent, model, request_body, complexity_info)
"""

NEW_AGENT = """    if agent is not None:
        # openjarvis-offload-sync-handlers-v1
        # _handle_agent is a synchronous def. Calling it directly from this
        # coroutine pinned the event loop for the entire turn - measured at
        # 253 s with 23 consecutive /health timeouts. Same idiom as
        # stream_bridge.py:155, which is why the streaming path is unaffected.
        return await asyncio.to_thread(
            _handle_agent, agent, model, request_body, complexity_info
        )
"""

OLD_DIRECT = """    bus = getattr(request.app.state, "bus", None)
    return _handle_direct(
        engine,
        model,
        request_body,
        bus=bus,
        complexity_info=complexity_info,
    )
"""

NEW_DIRECT = """    bus = getattr(request.app.state, "bus", None)
    # openjarvis-offload-sync-handlers-v1
    # Same defect shape as the _handle_agent branch above: synchronous def,
    # called without await from a coroutine. Shape-confirmed, not measured.
    return await asyncio.to_thread(
        _handle_direct,
        engine,
        model,
        request_body,
        bus,
        complexity_info,
    )
"""


def fail(msg):
    print("ABORT: %s" % msg)
    print("Nothing was changed.")
    sys.exit(1)


def main():
    if not TARGET.exists():
        fail("%s not found. Run from the repo root, C:\\Users\\Admin\\OpenJarvis" % TARGET)

    src = TARGET.read_text(encoding="utf-8")

    # ---- guard: already applied
    if MARKER in src:
        print("Marker %s already present." % MARKER)
        print("Patch is already applied. Nothing to do.")
        return 0

    # ---- guard: asyncio must be importable in this module
    tree = ast.parse(src)
    has_asyncio = False
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name == "asyncio":
                    has_asyncio = True
        elif isinstance(node, ast.ImportFrom):
            if node.module == "asyncio":
                has_asyncio = True

    # ---- guard: both target blocks must be present verbatim
    if OLD_AGENT not in src:
        fail("the _handle_agent call site does not match the expected text. "
             "The file has changed since it was read. Re-read routes.py:160-171 "
             "before patching.")
    if src.count(OLD_AGENT) != 1:
        fail("the _handle_agent call site matched %d times, expected 1."
             % src.count(OLD_AGENT))
    if OLD_DIRECT not in src:
        fail("the _handle_direct call site does not match the expected text. "
             "Re-read routes.py:160-171 before patching.")
    if src.count(OLD_DIRECT) != 1:
        fail("the _handle_direct call site matched %d times, expected 1."
             % src.count(OLD_DIRECT))

    # ---- guard: _handle_direct positional order must match how we now call it
    # We switch from keyword args to positional, so the signature order matters.
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name == "_handle_direct":
            names = [a.arg for a in node.args.args]
            expected = ["engine", "model", "req", "bus", "complexity_info"]
            if names != expected:
                fail("_handle_direct signature is %s, expected %s. The "
                     "positional call in this patch would bind the wrong "
                     "arguments." % (names, expected))
            break
    else:
        fail("could not find _handle_direct definition to verify its signature.")

    new_src = src.replace(OLD_AGENT, NEW_AGENT).replace(OLD_DIRECT, NEW_DIRECT)

    if not has_asyncio:
        # Insert `import asyncio` next to the existing stdlib imports.
        # `from __future__` imports must remain the first statements in the
        # file, so anchor the insertion after them rather than at the first
        # line that happens to start with import/from.
        new_tree = ast.parse(new_src)
        future_end = 0
        first_import = None
        for node in new_tree.body:
            if isinstance(node, ast.ImportFrom) and node.module == "__future__":
                future_end = max(future_end, node.end_lineno or node.lineno)
            elif isinstance(node, (ast.Import, ast.ImportFrom)):
                if first_import is None:
                    first_import = node.lineno

        lines = new_src.split("\n")
        if future_end:
            insert_at = future_end          # 0-based index == just after it
        elif first_import is not None:
            insert_at = first_import - 1
        else:
            fail("asyncio is not imported and no import block was found to "
                 "add it to. Add `import asyncio` by hand and re-run.")
        lines.insert(insert_at, "import asyncio")
        new_src = "\n".join(lines)
        print("NOTE: asyncio was not imported. Added `import asyncio` at line %d."
              % (insert_at + 1))
    else:
        print("asyncio already imported. No import added.")

    # ---- backup
    stamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    backup = TARGET.with_name(TARGET.name + ".bak-" + stamp)
    shutil.copy2(TARGET, backup)
    print("Backup written: %s" % backup)

    # ---- compile-check in a temp file BEFORE touching the real one
    with tempfile.NamedTemporaryFile("w", suffix=".py", delete=False,
                                     encoding="utf-8") as tmp:
        tmp.write(new_src)
        tmp_path = Path(tmp.name)
    try:
        py_compile.compile(str(tmp_path), doraise=True)
    except py_compile.PyCompileError as exc:
        tmp_path.unlink(missing_ok=True)
        backup.unlink(missing_ok=True)
        fail("patched source does not compile: %s" % exc)
    finally:
        tmp_path.unlink(missing_ok=True)

    # ---- write, then compile the real file and self-restore on failure
    TARGET.write_text(new_src, encoding="utf-8")
    try:
        py_compile.compile(str(TARGET), doraise=True)
    except py_compile.PyCompileError as exc:
        shutil.copy2(backup, TARGET)
        fail("post-write compile failed, file RESTORED from backup: %s" % exc)

    print()
    print("PATCH APPLIED - %s" % MARKER)
    print("  routes.py  _handle_agent  -> asyncio.to_thread   (measured defect)")
    print("  routes.py  _handle_direct -> asyncio.to_thread   (shape-confirmed)")
    print()
    print("ROLLBACK:")
    print("  Copy-Item '%s' '%s' -Force" % (backup, TARGET))
    print()
    print("RESTART REQUIRED before this takes effect.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
