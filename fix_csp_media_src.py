# MARKER: openjarvis-fix-csp-media-src-v1
"""Line-anchored patch: grant media-src/img-src/font-src in the server CSP.

PROBLEM
    src/openjarvis/server/middleware.py emits:
        Content-Security-Policy: default-src 'self' 'unsafe-inline' 'unsafe-eval'
    No media-src directive, so it falls back to default-src, and 'self' does
    not cover the blob: scheme. Every URL.createObjectURL() audio blob is
    rejected at assignment. Observed in the browser console 2026-08-03 as
    "Loading media from 'blob:http://127.0.0.1:8010/...' violates ...".
    Same fallback blocks a data: woff2 font and a data: svg background.

    frontend/src-tauri/tauri.conf.json:29 already grants
    "img-src 'self' data: blob:; media-src blob: data:" -- which is why the
    Tauri desktop app plays audio and the browser does not. This patch brings
    the server policy in line for the shared surfaces only.

WHAT IT CHANGES
    Two sites, both of which must move together or the test constant diverges
    from live behaviour:
      * line 52 -- the string inside SecurityHeadersMiddleware.dispatch (LIVE)
      * line 67 -- the "Content-Security-Policy" entry of SECURITY_HEADERS
                   (test-only mirror; app.py never imports it)

    Resulting policy (identical at both sites):
        default-src 'self' 'unsafe-inline' 'unsafe-eval';
        img-src 'self' data: blob:;
        font-src 'self' data:;
        media-src 'self' blob: data:

    default-src is left EXACTLY as-is. Nothing is tightened. Only the three
    directives proven blocked in the console are added.

OPTIONAL --allow-mic
    Also rewrites Permissions-Policy microphone=() to microphone=(self) at
    lines 49 and 66. Off by default. Needed only for browser-surface STT
    testing; the Tauri webview is unaffected either way.

USAGE
    python fix_csp_media_src.py                  # dry run, default
    python fix_csp_media_src.py --apply
    python fix_csp_media_src.py --apply --allow-mic
    python fix_csp_media_src.py --path C:\\Users\\Admin\\Openjarvis

Stdlib only. Read-only unless --apply is passed.
"""

import argparse
import hashlib
import os
import shutil
import sys
import time

MARKER = "openjarvis-fix-csp-media-src-v1"
REL_TARGET = os.path.join("src", "openjarvis", "server", "middleware.py")

# ---------------------------------------------------------------- anchors --
# (1-based line number, exact expected content without line terminator)

CSP_OLD = "default-src 'self' 'unsafe-inline' 'unsafe-eval'"

CSP_PARTS = [
    "default-src 'self' 'unsafe-inline' 'unsafe-eval'; ",
    "img-src 'self' data: blob:; ",
    "font-src 'self' data:; ",
    "media-src 'self' blob: data:",
]
CSP_NEW = "".join(CSP_PARTS)

# live site: inside dispatch(), 16-space indent, parenthesised assignment
LIVE_LINE = 52
LIVE_EXPECT = '                "%s"' % CSP_OLD
LIVE_REPLACE = ['                "%s"' % p for p in CSP_PARTS]

# test-constant site: dict entry, 4-space indent
DICT_LINE = 67
DICT_EXPECT = '    "Content-Security-Policy": "%s",' % CSP_OLD
DICT_REPLACE = (
    ['    "Content-Security-Policy": (']
    + ['        "%s"' % p for p in CSP_PARTS]
    + ["    ),"]
)

# optional microphone sites
MIC_OLD = "camera=(), microphone=(), geolocation=()"
MIC_NEW = "camera=(), microphone=(self), geolocation=()"
MIC_LIVE_LINE = 49
MIC_LIVE_EXPECT = '                "%s"' % MIC_OLD
MIC_LIVE_REPLACE = ['                "%s"' % MIC_NEW]
MIC_DICT_LINE = 66
MIC_DICT_EXPECT = '    "Permissions-Policy": "%s",' % MIC_OLD
MIC_DICT_REPLACE = ['    "Permissions-Policy": "%s",' % MIC_NEW]


def sha256_of(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for block in iter(lambda: fh.read(65536), b""):
            h.update(block)
    return h.hexdigest().upper()


def split_keepends(raw):
    """Return (lines_without_terminators, terminators) preserving exactness."""
    text = raw.decode("utf-8")
    pieces = text.splitlines(True)
    bodies, ends = [], []
    for p in pieces:
        if p.endswith("\r\n"):
            bodies.append(p[:-2])
            ends.append("\r\n")
        elif p.endswith("\n"):
            bodies.append(p[:-1])
            ends.append("\n")
        elif p.endswith("\r"):
            bodies.append(p[:-1])
            ends.append("\r")
        else:
            bodies.append(p)
            ends.append("")
    return bodies, ends


def check_anchor(bodies, lineno, expect, label):
    idx = lineno - 1
    if idx < 0 or idx >= len(bodies):
        print("  FAIL %-14s line %d out of range (file has %d lines)"
              % (label, lineno, len(bodies)))
        return False
    actual = bodies[idx]
    if actual == expect:
        print("  ok   %-14s line %d matched byte-exact" % (label, lineno))
        return True
    print("  FAIL %-14s line %d MISMATCH" % (label, lineno))
    print("       expected: %r" % expect)
    print("       actual  : %r" % actual)
    return False


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--path", default=".", help="repo root (default: cwd)")
    ap.add_argument("--apply", action="store_true", help="write changes")
    ap.add_argument("--allow-mic", action="store_true",
                    help="also set Permissions-Policy microphone=(self)")
    args = ap.parse_args()

    target = os.path.join(os.path.abspath(args.path), REL_TARGET)
    print("marker : %s" % MARKER)
    print("target : %s" % target)

    if not os.path.isfile(target):
        print("ERROR  : file not found")
        return 2

    raw = open(target, "rb").read()
    before_hash = sha256_of(target)
    bodies, ends = split_keepends(raw)
    print("before : %d bytes / %d lines / SHA256 %s"
          % (len(raw), len(bodies), before_hash))

    # ------------------------------------------------------ idempotency --
    if "media-src" in raw.decode("utf-8"):
        print("")
        print("NO-OP  : 'media-src' already present in this file.")
        print("         Nothing to do. Exiting without changes.")
        return 0

    # ---------------------------------------------------------- anchors --
    print("")
    print("anchor checks:")
    edits = []
    ok = True
    ok &= check_anchor(bodies, LIVE_LINE, LIVE_EXPECT, "csp-live")
    edits.append((LIVE_LINE, LIVE_REPLACE))
    ok &= check_anchor(bodies, DICT_LINE, DICT_EXPECT, "csp-const")
    edits.append((DICT_LINE, DICT_REPLACE))

    if args.allow_mic:
        ok &= check_anchor(bodies, MIC_LIVE_LINE, MIC_LIVE_EXPECT, "mic-live")
        edits.append((MIC_LIVE_LINE, MIC_LIVE_REPLACE))
        ok &= check_anchor(bodies, MIC_DICT_LINE, MIC_DICT_EXPECT, "mic-const")
        edits.append((MIC_DICT_LINE, MIC_DICT_REPLACE))

    if not ok:
        print("")
        print("ABORT  : one or more anchors did not match. File NOT touched.")
        print("         The file has drifted from what this patch expects.")
        return 3

    # -------------------------------------------------- build new content --
    # descending line order so earlier edits do not shift later indices
    new_bodies = list(bodies)
    new_ends = list(ends)
    for lineno, replacement in sorted(edits, key=lambda e: -e[0]):
        idx = lineno - 1
        term = new_ends[idx] or "\n"
        new_bodies[idx:idx + 1] = replacement
        new_ends[idx:idx + 1] = [term] * len(replacement)

    new_text = "".join(b + e for b, e in zip(new_bodies, new_ends))
    new_raw = new_text.encode("utf-8")

    print("")
    print("resulting policy string:")
    print("  %s" % CSP_NEW)
    if args.allow_mic:
        print("resulting permissions-policy:")
        print("  %s" % MIC_NEW)

    # --------------------------------------------------- compile in memory --
    try:
        compile(new_text, target, "exec")
        print("")
        print("compile: OK (patched source parses)")
    except SyntaxError as exc:
        print("")
        print("ABORT  : patched source does NOT compile: %s" % exc)
        return 4

    predicted = hashlib.sha256(new_raw).hexdigest().upper()
    print("after  : %d bytes / %d lines / SHA256 %s (predicted)"
          % (len(new_raw), len(new_bodies), predicted))
    print("delta  : %+d bytes / %+d lines"
          % (len(new_raw) - len(raw), len(new_bodies) - len(bodies)))

    if not args.apply:
        print("")
        print("DRY RUN. No changes written. Re-run with --apply to write.")
        return 0

    # ------------------------------------------------------------- write --
    stamp = time.strftime("%Y%m%d_%H%M%S")
    backup = "%s.bak_%s" % (target, stamp)
    shutil.copy2(target, backup)
    print("")
    print("backup : %s" % backup)

    with open(target, "wb") as fh:
        fh.write(new_raw)

    actual_hash = sha256_of(target)
    actual_size = os.path.getsize(target)
    print("written: %d bytes / SHA256 %s" % (actual_size, actual_hash))
    if actual_hash == predicted:
        print("VERIFY : on-disk hash matches prediction. PATCH APPLIED.")
    else:
        print("VERIFY : MISMATCH between predicted and on-disk hash.")
        print("         Restore with:")
        print('         Copy-Item "%s" "%s" -Force' % (backup, target))
        return 5

    print("")
    print("NEXT   : restart the backend (.\\start-openjarvis.ps1), confirm")
    print("         [LIVE] against the PID from netstat, then re-check:")
    print("         (Invoke-WebRequest 'http://127.0.0.1:8010/'"
          " -UseBasicParsing).Headers['content-security-policy']")
    return 0


if __name__ == "__main__":
    sys.exit(main())
