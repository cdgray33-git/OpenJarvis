#!/usr/bin/env python3
"""
W61 PATCHER - protected senders v2 (mailbox_tools.py), Option B.

v1 read Path.cwd()/protected_senders.json: the list bound to wherever the
launcher was started. A MISSING file, a non-list, or an empty list fell
back to the defaults with NO log. A list of only blank entries ([" "])
filtered to [] and REPLACED the defaults with nothing - fail OPEN.

v2 (this patch):
  * fixed path DEFAULT_CONFIG_DIR / "protected_senders.json" - the same
    per-user dir that already holds the connector credentials
  * every fallback logged (backend.log AND dispatch.log with turn id)
  * never returns an empty list - falls back to the defaults instead
  * tolerates a UTF-8 BOM (PS5 trap) but logs it
  * defaults are lifted VERBATIM from the v1 block on disk

Then a ONE-TIME COPY: if the new file does not exist and the repo-root
file does and parses, its bytes (BOM stripped) are copied to the new
path. An existing new file is never touched.

Fails loud: anchors wrong, already patched, or no compile -> NOTHING
written, exit 1. Run with the repo .venv python.
"""

import ast
import datetime
import json
import os
import re
import shutil
import sys

REPO = r'C:\Users\Admin\OpenJarvis'
MT = os.path.join(REPO, 'src', 'openjarvis', 'tools', 'mailbox_tools.py')
ROOT_LIST = os.path.join(REPO, 'protected_senders.json')
STAMP = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
TAG = 'bak_w61protected_' + STAMP
BOM = b'\xef\xbb\xbf'
MARKER = 'openjarvis-protected-senders-v2'

V1_RE = re.compile(
    r'(?P<indent>[ \t]*)# openjarvis-protected-senders-v1\n'
    r'.*?'
    r"logger\.exception\('protected_senders\.json unreadable; using "
    r"built-in list'\)\n",
    re.DOTALL,
)
DEFAULTS_RE = re.compile(r'_defaults = (\[.*?\])', re.DOTALL)
PREFIX_ANCHOR = '_PREFIX = "imap_mail_"\n'

NEW_SITE = (
    '{i}# {m} (W61) - fixed path, loud fallbacks, never empty.\n'
    '{i}# See _load_protected_senders at module level.\n'
    '{i}_prot = _load_protected_senders()\n'
)

LOADER = '''

# --- openjarvis-protected-senders-v2 (W61) -----------------------------------
# The protected list lives in the per-user config dir, next to the connector
# credentials - NOT in the process working directory. v1 read
# cwd/protected_senders.json, so the list bound to wherever the launcher was
# started, and a missing file fell back to the defaults silently. v2: one
# fixed path, every fallback logged, and a list that filters down to nothing
# falls back to the defaults instead of to NO protection (v1 failed open on
# a list of blank strings).
PROTECTED_SENDERS_PATH = DEFAULT_CONFIG_DIR / "protected_senders.json"
_PROTECTED_DEFAULTS = %(defaults)s


def _protected_log(level, fmt, *args):
    """Write one PROTECTED line to backend.log and to dispatch.log."""
    logger.log(level, fmt, *args)
    try:
        from openjarvis.tools._stubs import CURRENT_TURN_ID, _get_dispatch_logger

        _get_dispatch_logger().log(
            level, "turn=%%s " + fmt, CURRENT_TURN_ID.get(), *args
        )
    except Exception:
        pass


def _load_protected_senders() -> List[str]:
    """Return lowercase sender substrings to protect. NEVER returns []."""
    path = PROTECTED_SENDERS_PATH
    defaults = [str(p).strip().lower() for p in _PROTECTED_DEFAULTS]
    if not path.is_file():
        _protected_log(
            logging.WARNING,
            "PROTECTED source=defaults reason=missing path=%%s count=%%d",
            path, len(defaults),
        )
        return defaults
    try:
        raw = path.read_bytes()
    except Exception:
        logger.exception("protected senders file unreadable: %%s", path)
        _protected_log(
            logging.ERROR,
            "PROTECTED source=defaults reason=unreadable path=%%s count=%%d",
            path, len(defaults),
        )
        return defaults
    if raw.startswith(b"\\xef\\xbb\\xbf"):
        _protected_log(
            logging.WARNING,
            "PROTECTED bom_stripped path=%%s (write this file as ASCII)",
            path,
        )
    try:
        data = json.loads(raw.decode("utf-8-sig"))
    except Exception:
        logger.exception("protected senders file is not valid JSON: %%s", path)
        _protected_log(
            logging.ERROR,
            "PROTECTED source=defaults reason=unparseable path=%%s count=%%d",
            path, len(defaults),
        )
        return defaults
    if not isinstance(data, list):
        _protected_log(
            logging.WARNING,
            "PROTECTED source=defaults reason=not_a_list type=%%s path=%%s"
            " count=%%d",
            type(data).__name__, path, len(defaults),
        )
        return defaults
    entries = [
        x.strip().lower() for x in data if isinstance(x, str) and x.strip()
    ]
    if not entries:
        _protected_log(
            logging.WARNING,
            "PROTECTED source=defaults reason=no_usable_entries raw_len=%%d"
            " path=%%s count=%%d",
            len(data), path, len(defaults),
        )
        return defaults
    if len(entries) != len(data):
        _protected_log(
            logging.WARNING,
            "PROTECTED dropped=%%d non-string or blank entries path=%%s",
            len(data) - len(entries), path,
        )
    _protected_log(
        logging.INFO,
        "PROTECTED source=file path=%%s count=%%d",
        path, len(entries),
    )
    return entries
'''


def parse_list(b):
    """Return (entries, bom) for a candidate list file, or (None, bom)."""
    bom = b.startswith(BOM)
    try:
        data = json.loads(b.decode('utf-8-sig'))
    except Exception:
        return None, bom
    if not isinstance(data, list):
        return None, bom
    ent = [x for x in data if isinstance(x, str) and x.strip()]
    return (ent if ent else None), bom


def migrate():
    print('')
    print('--- ONE-TIME COPY')
    sys.path.insert(0, os.path.join(REPO, 'src'))
    try:
        from openjarvis.core.config import DEFAULT_CONFIG_DIR
    except Exception as exc:
        print('SKIPPED: could not import DEFAULT_CONFIG_DIR (%s: %s). '
              'Copy the file by hand.' % (type(exc).__name__, exc))
        return
    dest = os.path.join(str(DEFAULT_CONFIG_DIR), 'protected_senders.json')
    print('NEW PATH  : %s' % dest)
    if os.path.isfile(dest):
        with open(dest, 'rb') as fh:
            ent, bom = parse_list(fh.read())
        print('EXISTS    : left untouched. entries=%s bom=%s'
              % (len(ent) if ent else 'UNUSABLE', bom))
        return
    if not os.path.isfile(ROOT_LIST):
        print('NO SOURCE : %s missing. Loader will log reason=missing and '
              'use defaults.' % ROOT_LIST)
        return
    with open(ROOT_LIST, 'rb') as fh:
        src = fh.read()
    ent, bom = parse_list(src)
    if ent is None:
        print('NOT COPIED: %s is not a usable list. Fix it first.' % ROOT_LIST)
        return
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    with open(dest, 'wb') as fh:
        fh.write(src[3:] if bom else src)
    with open(dest, 'rb') as fh:
        head = list(fh.read(3))
    print('COPIED    : %s -> %s  entries=%d  first3=%s  bom_stripped=%s'
          % (ROOT_LIST, dest, len(ent), head, bom))


def main():
    if not os.path.isfile(MT):
        print('MISSING: %s' % MT)
        return 1
    with open(MT, 'rb') as fh:
        raw = fh.read()
    has_bom = raw.startswith(BOM)
    body = raw[3:] if has_bom else raw
    try:
        text = body.decode('utf-8')
    except UnicodeDecodeError as exc:
        print('ABORT: not valid UTF-8 (%s). Nothing written.' % exc)
        return 1
    crlf = '\r\n' in text
    text = text.replace('\r\n', '\n')

    if MARKER in text:
        print('ABORT: %s already present. Nothing written.' % MARKER)
        migrate()
        return 1
    for need in ('from typing import Any, Dict, List, Optional',
                 'import json\n', 'import logging\n',
                 'from openjarvis.core.config import DEFAULT_CONFIG_DIR'):
        if need not in text:
            print('ABORT: expected import %r not found. Nothing written.'
                  % need.strip())
            return 1

    hits = list(V1_RE.finditer(text))
    if len(hits) != 1:
        print('ABORT: v1 block matched %d times (expected 1). Nothing '
              'written.' % len(hits))
        return 1
    m = hits[0]
    old = m.group(0)
    if '_Path.cwd()' not in old or old.count('\n') > 25:
        print('ABORT: v1 block lacks _Path.cwd() or spans %d lines. '
              'Nothing written.' % old.count('\n'))
        return 1
    dm = DEFAULTS_RE.search(old)
    try:
        defaults = ast.literal_eval(dm.group(1)) if dm else None
    except (ValueError, SyntaxError):
        defaults = None
    if not isinstance(defaults, list) or not defaults \
            or not all(isinstance(x, str) and x.strip() for x in defaults):
        print('ABORT: could not lift the v1 defaults list. Nothing written.')
        return 1

    text2 = (text[:m.start()]
             + NEW_SITE.format(i=m.group('indent'), m=MARKER)
             + text[m.end():])
    if text2.count(PREFIX_ANCHOR) != 1:
        print('ABORT: %r found %d times (expected 1). Nothing written.'
              % (PREFIX_ANCHOR.strip(), text2.count(PREFIX_ANCHOR)))
        return 1
    pos = text2.index(PREFIX_ANCHOR) + len(PREFIX_ANCHOR)
    loader = LOADER % {'defaults': json.dumps(defaults)}
    text3 = text2[:pos] + loader + text2[pos:]

    out = text3.replace('\n', '\r\n') if crlf else text3
    outbytes = (BOM if has_bom else b'') + out.encode('utf-8')
    try:
        compile(outbytes, MT, 'exec')
    except SyntaxError as exc:
        print('ABORT: patched file does not compile: %s. Nothing written.'
              % exc)
        return 1

    bak = MT + '.' + TAG
    shutil.copy2(MT, bak)
    with open(MT, 'wb') as fh:
        fh.write(outbytes)

    cwd_left = len(re.findall(r'\.cwd\(\)', text3))
    print('=' * 68)
    print('W61 PROTECTED SENDERS v2 PATCH - %s' % STAMP)
    print('=' * 68)
    print('FILE       : %s' % MT)
    print('BACKUP     : %s' % bak)
    print('BOM / CRLF : %s / %s (preserved)' % (has_bom, crlf))
    print('LINES      : %d -> %d' % (text.count('\n'), text3.count('\n')))
    print('V1 BLOCK   : %d lines replaced' % old.count('\n'))
    print('DEFAULTS   : %d lifted verbatim' % len(defaults))
    print('.cwd() LEFT: %d (expected 0)' % cwd_left)
    print('COMPILE    : OK')
    print('=' * 68)
    migrate()
    print('')
    print('NOT a verification. Run the W61 protected harness, then restart')
    print('the backend - the running process still has v1 loaded.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
