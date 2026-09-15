#!/usr/bin/env python3
"""
W60 PATCHER - two findings, two files.

FINDING 1  ToolCallCard.tsx renders tool latency with a ms/s branch that
           assumes MILLISECONDS. The SSE field is SECONDS. Verified W60
           against dispatch.log on three calls:
               39.268 s -> chip "39ms"
               31.994 s -> chip "32ms"
               84.732 s (80.135 s excluding the 4.597 s gate wait)
                        -> chip "80ms"

FINDING 2  Mojibake in ToolCallCard.tsx (2 lines) and CommandPalette.tsx
           (21 lines). TWO DIFFERENT manglings are present - a cp1252
           chain and a cp437/cp850 chain - so this script does NOT match
           on mojibake glyphs at all. It anchors on the ASCII text of the
           target line and replaces EVERY non-ASCII run on that line with
           a specified ASCII string. Encoding depth is therefore
           irrelevant. (W59: measure the bytes, never guess the glyph.)

Leaves alone: the ChatArea.tsx BOM, the App.tsx comment em dash, and the
api.ts comment em dashes - none are user-visible.

Fails loud: if any anchor or the latency block is not found, NOTHING is
written and the script exits 1.
"""

import datetime
import os
import re
import shutil
import sys

ROOT = r'C:\Users\Admin\OpenJarvis\frontend\src'
STAMP = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
TAG = 'bak_w60chip_' + STAMP

TOOLCALLCARD = os.path.join(ROOT, 'components', 'Chat', 'ToolCallCard.tsx')
COMMANDPALETTE = os.path.join(ROOT, 'components', 'CommandPalette.tsx')

NONASCII = re.compile(r'[^\x00-\x7F]+')

# (anchor substring in the line, ASCII replacement for every non-ASCII run)
# First matching anchor wins, so specific anchors precede generic ones.
LINE_RULES = {
    TOOLCALLCARD: [
        ('const trimmed = valStr.length > 40', '...'),
        ('return entries.length === 1', '...'),
    ],
    COMMANDPALETTE: [
        ('Refreshing model list', '...'),
        ('Cloud Models tab', '--'),
        ('Navigate', 'Up/Down'),
        ('No models available', '-'),
        ('desc:', '-'),
    ],
}

# Finding 1. Whitespace-tolerant so reindentation does not break it.
LATENCY_RE = re.compile(
    r'\{toolCall\.latency\s*<\s*1000\s*\n'
    r'(\s*)\?\s*`\$\{Math\.round\(toolCall\.latency\)\}ms`\s*\n'
    r'\s*:\s*`\$\{\(toolCall\.latency\s*/\s*1000\)\.toFixed\(1\)\}s`\}'
)

LATENCY_NEW = (
    '{/* SSE sends latency in SECONDS, not ms. Verified W60 against '
    'dispatch.log. */}\n'
    '            {toolCall.latency < 1\n'
    '              ? `${Math.round(toolCall.latency * 1000)}ms`\n'
    '              : `${toolCall.latency.toFixed(1)}s`}'
)


def nonascii_bytes(path):
    with open(path, 'rb') as fh:
        return sum(1 for b in fh.read() if b > 0x7F)


def main():
    for path in (TOOLCALLCARD, COMMANDPALETTE):
        if not os.path.isfile(path):
            print('MISSING: %s' % path)
            return 1

    results = []

    for path, rules in LINE_RULES.items():
        before_bytes = nonascii_bytes(path)
        with open(path, 'r', encoding='utf-8', errors='surrogateescape',
                  newline='') as fh:
            text = fh.read()

        lines = text.split('\n')
        changed = []

        for i, line in enumerate(lines):
            if not NONASCII.search(line):
                continue
            for anchor, repl in rules:
                if anchor in line:
                    newline = NONASCII.sub(repl, line)
                    if newline != line:
                        lines[i] = newline
                        changed.append((i + 1, newline.strip()))
                    break

        newtext = '\n'.join(lines)

        latency_hits = 0
        if path == TOOLCALLCARD:
            newtext, latency_hits = LATENCY_RE.subn(LATENCY_NEW, newtext)
            if latency_hits != 1:
                print('ABORT: latency block matched %d times in %s '
                      '(expected 1). Nothing written.'
                      % (latency_hits, os.path.basename(path)))
                return 1

        if newtext == text:
            print('ABORT: no change produced for %s. Nothing written.'
                  % os.path.basename(path))
            return 1

        bak = path + '.' + TAG
        shutil.copy2(path, bak)
        with open(path, 'w', encoding='utf-8', errors='surrogateescape',
                  newline='') as fh:
            fh.write(newtext)

        results.append((path, bak, before_bytes, nonascii_bytes(path),
                        changed, latency_hits))

    print('=' * 68)
    print('W60 CHIP PATCH - %s' % STAMP)
    print('=' * 68)
    for path, bak, before_b, after_b, changed, lat in results:
        print('')
        print('FILE      : %s' % path)
        print('BACKUP    : %s' % bak)
        print('NON-ASCII : %d bytes -> %d bytes' % (before_b, after_b))
        print('LINES FIXED (%d):' % len(changed))
        for lineno, txt in changed:
            shown = txt if len(txt) <= 96 else txt[:96] + ' [...]'
            print('  %5d  %s' % (lineno, shown))
        if lat:
            print('LATENCY   : unit branch rewritten, seconds-aware')
    print('')
    print('=' * 68)
    print('RESIDUAL NON-ASCII (expected 0 in both files):')
    for path, _, _, after_b, _, _ in results:
        print('  %-24s %d' % (os.path.basename(path), after_b))
    print('=' * 68)
    print('')
    print('NOT a verification. Rebuild and look at a tool chip.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
