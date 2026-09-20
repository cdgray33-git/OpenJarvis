"""
patch_w2_catchall_guard_v2.py

W2 FIX: guard the SPA catch-all so unmatched /v1/* and /api/* paths return 404
instead of 200 text/html index.html.

Two edits, one logical change:
  1. line 9  - add HTTPException to the fastapi import
  2. line 349-351 - add the prefix guard at the top of spa_catch_all

Process: back up, verify each anchor matches EXACTLY ONCE, write a temp file,
py_compile the temp, and only then write over the real file.
Aborts without touching anything if any anchor count is not 1 or compile fails.

Run from repo root: C:\\Users\\Admin\\OpenJarvis
"""

import datetime
import pathlib
import py_compile
import shutil
import sys
import tempfile

TARGET = pathlib.Path("src/openjarvis/server/app.py")

IMPORT_OLD = "from fastapi import FastAPI"
IMPORT_NEW = "from fastapi import FastAPI, HTTPException"

GUARD_OLD_LINES = [
    '        async def spa_catch_all(full_path: str):',
    '            """Serve static files directly, fall back to index.html for SPA routes."""',
    '            if full_path:',
]

GUARD_NEW_LINES = [
    '        async def spa_catch_all(full_path: str):',
    '            """Serve static files directly, fall back to index.html for SPA routes."""',
    '            # W2: never mask the API surface with the SPA index. Unmatched',
    '            # /v1/* and /api/* paths must 404, not return 200 text/html.',
    '            if full_path.startswith(("v1/", "api/")):',
    '                raise HTTPException(status_code=404, detail="Not Found")',
    '            if full_path:',
]


def fail(msg):
    print("ABORT: " + msg)
    print("NO FILE WAS MODIFIED.")
    sys.exit(1)


def main():
    if not TARGET.is_file():
        fail("target not found: %s (run from repo root)" % TARGET)

    with open(str(TARGET), "r", encoding="utf-8", newline="") as fh:
        raw = fh.read()
    nl = "\r\n" if "\r\n" in raw else "\n"

    guard_old = nl.join(GUARD_OLD_LINES)
    guard_new = nl.join(GUARD_NEW_LINES)

    n_import = raw.count(IMPORT_OLD)
    n_guard = raw.count(guard_old)

    print("newline style : %s" % ("CRLF" if nl == "\r\n" else "LF"))
    print("import anchor : %d match(es)" % n_import)
    print("guard anchor  : %d match(es)" % n_guard)

    if raw.count(IMPORT_NEW) > 0:
        fail("HTTPException already present in the fastapi import - patch may already be applied")
    if n_import != 1:
        fail("import anchor must match exactly once, got %d" % n_import)
    if n_guard != 1:
        fail("guard anchor must match exactly once, got %d" % n_guard)

    patched = raw.replace(IMPORT_OLD, IMPORT_NEW, 1).replace(guard_old, guard_new, 1)

    if patched == raw:
        fail("replacement produced no change")

    tmp_dir = tempfile.mkdtemp(prefix="w2guard_")
    tmp_file = pathlib.Path(tmp_dir) / "app_patched.py"
    with open(str(tmp_file), "w", encoding="utf-8", newline="") as fh:
        fh.write(patched)

    try:
        py_compile.compile(str(tmp_file), doraise=True)
    except py_compile.PyCompileError as exc:
        fail("temp file failed to compile: %s" % exc)

    print("temp compile  : OK (%s)" % tmp_file)

    stamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    backup = TARGET.with_name(TARGET.name + ".bak-" + stamp)
    shutil.copy2(str(TARGET), str(backup))
    print("backup        : %s" % backup)

    with open(str(TARGET), "w", encoding="utf-8", newline="") as fh:
        fh.write(patched)
    print("written       : %s" % TARGET)

    print("")
    print("ROLLBACK COMMAND:")
    print("Copy-Item '%s' '%s' -Force" % (backup.as_posix().replace("/", "\\"),
                                          TARGET.as_posix().replace("/", "\\")))
    print("")
    print("RESTART REQUIRED before verification.")


if __name__ == "__main__":
    main()
