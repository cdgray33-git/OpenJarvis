#!/usr/bin/env python3
"""
W61 PATCHER - serve.py mojibake, two sites.

SITE A  channel-wiring comment:
        '# Wire channel messages <mojibake> agent / engine (...)'
SITE B  LIVE log call, runs on EVERY backend start:
        'logger.info("Credentials loaded <mojibake> %s", ...)'
        writes a multi-kilobyte mangled string to backend.log.

Method (W60 template, hardened): anchor on the ASCII text BEFORE and
AFTER the mangled span and replace the WHOLE span with an ASCII string.
Encoding depth is irrelevant. The span must contain only non-ASCII and
whitespace; if it holds any other ASCII the script aborts, because that
would mean the anchors are wrong.

Locates serve.py itself: exactly one serve.py under the repo that holds
both 'def serve(' and 'openjarvis-confirm-live-v1'. Skips _bak, .git,
.venv, venv, node_modules. Prints its choice.

Fails loud: anchors not found exactly once, span not clean, or patched
bytes fail to compile -> NOTHING written, exit 1.
"""

import datetime
import os
import shutil
import sys

REPO = r'C:\Users\Admin\OpenJarvis'
SKIP_DIRS = {'_bak', '.git', '.venv', 'venv', 'node_modules', '__pycache__'}
STAMP = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
TAG = 'bak_w61serve_' + STAMP
BOM = b'\xef\xbb\xbf'

# (label, prefix, suffix, ascii replacement for the span between them)
SITES = [
    ('A comment', '# Wire channel messages',
     'agent / engine (per-chat session isolation)', ' -> '),
    ('B log call', 'logger.info("Credentials loaded',
     '%s", ", ".join(_cred_parts))', ' - '),
]


def find_serve():
    hits = []
    for dirpath, dirnames, filenames in os.walk(REPO):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        if 'serve.py' not in filenames:
            continue
        p = os.path.join(dirpath, 'serve.py')
        try:
            with open(p, 'rb') as fh:
                b = fh.read()
        except OSError:
            continue
        if b'def serve(' in b and b'openjarvis-confirm-live-v1' in b:
            hits.append(p)
    return hits


def is_ascii(ch):
    return ord(ch) < 0x80


def main():
    hits = find_serve()
    print('SERVE.PY CANDIDATES: %d' % len(hits))
    for h in hits:
        print('  %s' % h)
    if len(hits) != 1:
        print('ABORT: expected exactly 1 candidate. Nothing written.')
        return 1
    path = hits[0]

    with open(path, 'rb') as fh:
        raw = fh.read()
    has_bom = raw.startswith(BOM)
    body = raw[3:] if has_bom else raw
    before_nonascii = sum(1 for x in body if x > 0x7F)

    text = body.decode('utf-8', errors='surrogateescape')
    lines = text.split('\n')
    report = []

    for label, prefix, suffix, repl in SITES:
        idx = [i for i, ln in enumerate(lines)
               if prefix in ln and suffix in ln]
        if len(idx) != 1:
            print('ABORT: site %s matched %d lines (expected 1). '
                  'Nothing written.' % (label, len(idx)))
            return 1
        i = idx[0]
        ln = lines[i]
        start = ln.index(prefix) + len(prefix)
        end = ln.index(suffix, start)
        span = ln[start:end]
        if not any(not is_ascii(c) for c in span):
            print('ABORT: site %s span has no non-ASCII - already clean? '
                  'Nothing written.' % label)
            return 1
        stray = [c for c in span if is_ascii(c) and not c.isspace()]
        if stray:
            print('ABORT: site %s span holds %d stray ASCII chars (%r...). '
                  'Anchors wrong. Nothing written.'
                  % (label, len(stray), ''.join(stray[:20])))
            return 1
        new = ln[:start] + repl + ln[end:]
        lines[i] = new
        report.append((label, i + 1, len(ln), len(new), new.strip()))

    newbody = '\n'.join(lines).encode('utf-8', errors='surrogateescape')

    try:
        compile(newbody, path, 'exec')
    except (SyntaxError, ValueError) as exc:
        print('ABORT: patched file does not compile: %s. Nothing written.'
              % exc)
        return 1

    bak = path + '.' + TAG
    shutil.copy2(path, bak)
    with open(path, 'wb') as fh:
        fh.write((BOM if has_bom else b'') + newbody)

    after_nonascii = sum(1 for x in newbody if x > 0x7F)
    residual = []
    for n, ln in enumerate(newbody.split(b'\n'), 1):
        c = sum(1 for x in ln if x > 0x7F)
        if c:
            residual.append((n, c))

    print('=' * 68)
    print('W61 SERVE.PY PATCH - %s' % STAMP)
    print('=' * 68)
    print('FILE      : %s' % path)
    print('BACKUP    : %s' % bak)
    print('BOM       : %s (preserved as found)' % ('YES' if has_bom else 'no'))
    print('NON-ASCII : %d bytes -> %d bytes' % (before_nonascii,
                                              after_nonascii))
    print('BYTES     : %d -> %d' % (len(raw), len(newbody) + (3 if has_bom else 0)))
    print('COMPILE   : OK')
    for label, lineno, oldlen, newlen, txt in report:
        print('')
        print('SITE %s  line %d  chars %d -> %d' % (label, lineno,
                                                    oldlen, newlen))
        print('  %s' % txt)
    print('')
    print('RESIDUAL NON-ASCII LINES (expected none): %d' % len(residual))
    for n, c in residual:
        print('  line %d: %d bytes' % (n, c))
    print('=' * 68)
    print('NOT a verification. Restart via start-openjarvis.ps1 and read')
    print('the "Credentials loaded" line in backend.log.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
