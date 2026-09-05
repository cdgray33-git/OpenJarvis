#!/usr/bin/env python3
"""
patch_num_ctx_config.py
marker: openjarvis-num-ctx-config-v1

Threads a CONFIGURED num_ctx default into src/openjarvis/engine/ollama.py,
replacing the hardcoded 8192 literal at all three payload sites.

BEHAVIOR AFTER APPLY, before any config change:
    identical to today. The resolver returns 8192 when nothing is set.

RESOLUTION ORDER once applied:
    1. env OPENJARVIS_NUM_CTX
    2. [engine] num_ctx in <OPENJARVIS_HOME or ~/.openjarvis>/config.toml
    3. 8192

Callers that pass num_ctx explicitly are UNAFFECTED - kwargs.get() still
returns their value first. research_loop.py's 16384 keeps working.

SAFETY
  - reads and writes BYTES, so pre-existing mojibake (ollama.py:46, 122-123)
    passes through untouched and the line terminator is preserved
  - requires the target literal to appear EXACTLY 3 times
  - refuses to run twice (marker check)
  - ast.parse of the candidate before any write
  - predicts post-patch size and aborts if the on-disk size disagrees
  - dry run by default; --apply to write

USAGE (PowerShell, Windows box, from PS C:\\Users\\Admin\\OpenJarvis>)
    python .\\patch_num_ctx_config.py
    python .\\patch_num_ctx_config.py --apply
"""

import ast
import datetime
import os
import shutil
import sys

MARKER = "openjarvis-num-ctx-config-v1"
TARGET = os.path.join("src", "openjarvis", "engine", "ollama.py")

OLD = 'kwargs.get("num_ctx", 8192)'
NEW = 'kwargs.get("num_ctx", _oj_default_num_ctx())'
EXPECTED_HITS = 3

HELPER = '''
# --- openjarvis-num-ctx-config-v1 -------------------------------------------
# Resolves the DEFAULT num_ctx for this engine from configuration instead of a
# hardcoded literal. Callers that pass num_ctx explicitly are unaffected.
#
# Resolution order:
#   1. env OPENJARVIS_NUM_CTX
#   2. [engine] num_ctx in config.toml
#   3. 8192  (unchanged legacy behavior)
#
# Resolved once per process and cached. Every failure path falls back to 8192.

_OJ_NUM_CTX_CACHE = None


def _oj_config_path():
    import os as _os
    home = _os.environ.get("OPENJARVIS_HOME", "").strip()
    if not home:
        home = _os.path.join(_os.path.expanduser("~"), ".openjarvis")
    return _os.path.join(home, "config.toml")


def _oj_num_ctx_from_config():
    import re as _re
    try:
        with open(_oj_config_path(), "rb") as _fh:
            raw = _fh.read()
    except Exception:
        return None
    text = raw.decode("utf-8", "replace")
    try:
        import tomllib as _tomllib
        data = _tomllib.loads(text)
        val = data.get("engine", {}).get("num_ctx")
        if val is not None:
            return int(val)
        return None
    except Exception:
        pass
    try:
        for chunk in _re.split(r"(?m)^\\s*\\[", text):
            if chunk.startswith("engine]"):
                m = _re.search(r"(?m)^\\s*num_ctx\\s*=\\s*(\\d+)", chunk)
                if m:
                    return int(m.group(1))
    except Exception:
        pass
    return None


def _oj_default_num_ctx():
    global _OJ_NUM_CTX_CACHE
    if _OJ_NUM_CTX_CACHE is not None:
        return _OJ_NUM_CTX_CACHE
    value = 8192
    try:
        import os as _os
        env = _os.environ.get("OPENJARVIS_NUM_CTX", "").strip()
        if env:
            value = int(env)
        else:
            cfg = _oj_num_ctx_from_config()
            if cfg:
                value = int(cfg)
    except Exception:
        value = 8192
    if value < 512:
        value = 8192
    _OJ_NUM_CTX_CACHE = value
    return _OJ_NUM_CTX_CACHE
# --- end openjarvis-num-ctx-config-v1 ---------------------------------------
'''


def fail(msg):
    print("ABORT: " + msg)
    sys.exit(1)


def main():
    apply_it = "--apply" in sys.argv

    if not os.path.isfile(TARGET):
        fail("target not found: " + TARGET
             + "  (run this from the repo root, C:\\Users\\Admin\\OpenJarvis)")

    with open(TARGET, "rb") as fh:
        original = fh.read()

    pre_size = len(original)
    print("target      : " + TARGET)
    print("pre size    : %d bytes" % pre_size)

    try:
        text = original.decode("utf-8")
    except UnicodeDecodeError as exc:
        fail("file is not valid UTF-8, refusing to touch it: %s" % exc)

    crlf = text.count("\r\n")
    lf = text.count("\n") - crlf
    if crlf and lf:
        fail("MIXED line endings (%d CRLF, %d LF) - refusing" % (crlf, lf))
    eol = "\r\n" if crlf else "\n"
    print("eol         : " + ("CRLF" if crlf else "LF"))

    if MARKER in text:
        fail("marker already present - this patch has already been applied")

    hits = text.count(OLD)
    print("anchor hits : %d (expected %d)" % (hits, EXPECTED_HITS))
    if hits != EXPECTED_HITS:
        fail("expected exactly %d occurrences of %s, found %d"
             % (EXPECTED_HITS, OLD, hits))

    # show the three sites
    line_no = 0
    for line in text.split("\n"):
        line_no += 1
        if OLD in line:
            print("   site at line %d: %s" % (line_no, line.strip()))

    candidate = text.replace(OLD, NEW)

    helper = HELPER
    if eol == "\r\n":
        helper = helper.replace("\n", "\r\n")
    if not candidate.endswith(eol):
        candidate = candidate + eol
    candidate = candidate + helper

    try:
        ast.parse(candidate)
    except SyntaxError as exc:
        fail("candidate does not parse: %s" % exc)
    print("ast.parse   : OK")

    new_bytes = candidate.encode("utf-8")
    predicted = len(new_bytes)
    print("post size   : %d bytes (delta %+d)" % (predicted, predicted - pre_size))

    if not apply_it:
        print("")
        print("DRY RUN - nothing written. Re-run with --apply to write.")
        return

    stamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    bak = TARGET + ".bak_numctx_" + stamp
    shutil.copy2(TARGET, bak)
    print("backup      : " + bak)

    with open(TARGET, "wb") as fh:
        fh.write(new_bytes)

    actual = os.path.getsize(TARGET)
    print("on disk     : %d bytes" % actual)
    if actual != predicted:
        print("SIZE MISMATCH - predicted %d, got %d" % (predicted, actual))
        print("RESTORE NOW:")
        print("  Copy-Item '%s' '%s' -Force" % (bak, TARGET))
        sys.exit(1)

    with open(TARGET, "rb") as fh:
        verify = fh.read().decode("utf-8")
    checks = [
        (MARKER in verify, "marker present"),
        (verify.count(NEW) == EXPECTED_HITS, "%d call sites rewritten" % EXPECTED_HITS),
        (verify.count(OLD) == 0, "no hardcoded literal remains"),
        ("def _oj_default_num_ctx" in verify, "resolver defined"),
    ]
    ok = True
    for passed, label in checks:
        print("  %s  %s" % ("PASS" if passed else "FAIL", label))
        if not passed:
            ok = False
    if not ok:
        print("RESTORE NOW:")
        print("  Copy-Item '%s' '%s' -Force" % (bak, TARGET))
        sys.exit(1)

    print("")
    print("APPLIED CLEAN. Behavior is UNCHANGED until a value is set.")
    print("ROLLBACK:")
    print("  Copy-Item '%s' '%s' -Force" % (bak, TARGET))
    print("  then RESTART the backend")


if __name__ == "__main__":
    main()
