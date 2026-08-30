"""
patch_probe_confirmkey_v1.py

Fixes the confirm-frame discriminator in probe_ws_bare_subscribe.py.

Defect: the probe tests etype.startswith("tool.confirm") (DOT) in two places,
but the event type on the wire is "tool_confirm_request" (UNDERSCORES). Result:
a received confirm frame is reported as no confirm events, and confirm_id is
never inspected. See HANDOFF-2026-08-29-E section 4.1.

Change: normalize underscores to dots before the prefix test, in both places.
Nothing else is touched.

Run from PS C:\\Users\\Admin\\OpenJarvis>
"""
import hashlib
import os
import py_compile
import shutil
import sys
import time

TARGET = "probe_ws_bare_subscribe.py"
MARKER = "openjarvis-probe-confirmkey-v1"

OLD_1 = '            if etype.startswith("tool.confirm"):'
NEW_1 = '            if etype.replace("_", ".").startswith("tool.confirm"):'

OLD_2 = '    confirms = [f for f in frames if str(f.get("type", "")).startswith("tool.confirm")]'
NEW_2 = ('    confirms = [f for f in frames\n'
         '                if str(f.get("type", "")).replace("_", ".").startswith("tool.confirm")]')


def sha(b):
    return hashlib.sha256(b).hexdigest().upper()


def main():
    print(f"python: {sys.executable}")
    print(f"cwd:    {os.getcwd()}")

    if not os.path.exists(TARGET):
        print(f"ABORT: {TARGET} not found in cwd. Run from the repo root.")
        return 1

    with open(TARGET, "rb") as fh:
        pre = fh.read()

    print(f"PRE  bytes={len(pre)}  sha256={sha(pre)}")
    print(f"PRE  CRLF={pre.count(b'\\r\\n')}  bareLF={pre.count(b'\\n') - pre.count(b'\\r\\n')}")

    text = pre.decode("utf-8")

    if MARKER in text:
        print("ALREADY PATCHED (marker present). No change made.")
        return 0

    n1 = text.count(OLD_1)
    n2 = text.count(OLD_2)
    print(f"anchor 1 (live line 131) hits: {n1}   expected 1")
    print(f"anchor 2 (collector 169) hits: {n2}   expected 1")
    if n1 != 1 or n2 != 1:
        print("ABORT: anchor count not exactly 1. File is not the expected pre-image.")
        return 1

    out = text.replace(OLD_1, NEW_1).replace(OLD_2, NEW_2)
    out = out.rstrip("\r\n") + f"\r\n\r\n# {MARKER}\r\n"

    # ---- assertions before writing ----
    checks = [
        ('new anchor 1 present', out.count(NEW_1) == 1),
        ('new anchor 2 present', 'replace("_", ".").startswith("tool.confirm")' in out),
        ('old dot-only test gone', 'etype.startswith("tool.confirm")' not in out),
        ('marker present', out.count(MARKER) == 1),
        ('control: trigger_traffic untouched', out.count("trigger_traffic") == text.count("trigger_traffic")),
        ('control: ABSENT - REDACTED survives', "ABSENT - REDACTED" in out),
    ]
    ok = True
    for name, res in checks:
        print(f"  check: {name:<38} {'OK' if res else 'FAIL'}")
        ok = ok and res
    if not ok:
        print("ABORT: pre-write checks failed. Nothing written.")
        return 1

    bak = f"{TARGET}.bak_confirmkey_{time.strftime('%Y%m%d_%H%M%S')}"
    shutil.copy2(TARGET, bak)
    print(f"BACKUP: {bak}")

    with open(TARGET, "wb") as fh:
        fh.write(out.encode("utf-8"))

    with open(TARGET, "rb") as fh:
        post = fh.read()
    print(f"POST bytes={len(post)}  sha256={sha(post)}")
    print(f"POST CRLF={post.count(b'\\r\\n')}  bareLF={post.count(b'\\n') - post.count(b'\\r\\n')}")

    try:
        py_compile.compile(TARGET, doraise=True)
        print("py_compile: OK")
    except Exception as exc:
        print(f"py_compile FAILED: {exc}")
        print(f'RESTORE: copy "{os.path.abspath(bak)}" "{os.path.abspath(TARGET)}"')
        return 1

    print("PATCH APPLIED.")
    print(f'RESTORE COMMAND: copy "{os.path.abspath(bak)}" "{os.path.abspath(TARGET)}"')
    return 0


if __name__ == "__main__":
    sys.exit(main())
