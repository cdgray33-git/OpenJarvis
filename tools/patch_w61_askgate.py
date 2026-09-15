#!/usr/bin/env python3
"""
W61 PATCHER - ask.py, site cli-ask.

Replaces the W56 ConfirmPolicy at `_run_agent` (attribution only, ALWAYS
approves) with TerminalConfirmGate: a real gate that asks the person at
the terminal. Deny is the default. A stdin that is not a TTY denies
without reading. Every branch logs POLICY site=cli-ask to dispatch.log
and writes the decision into confirm_registry, because the executor
reports an unrecorded False as a TIMEOUT ("the user did not deny it, ask
again") - an unrecorded denial would invite a re-request loop.

Anchors: the W56 block (marker comment through the ConfirmPolicy call
closing paren) must match exactly once and contain site="cli-ask" and
human_present=True. `def _run_agent(` must appear exactly once; the class
is inserted above it. Preserves BOM and line endings as found.

Fails loud: already patched, anchor count wrong, not UTF-8, or patched
text does not compile -> NOTHING written, exit 1.
"""

import datetime
import os
import re
import shutil
import sys

REPO = r'C:\Users\Admin\OpenJarvis'
ASK = os.path.join(REPO, 'src', 'openjarvis', 'cli', 'ask.py')
STAMP = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
TAG = 'bak_w61askgate_' + STAMP
BOM = b'\xef\xbb\xbf'
MARKER = 'openjarvis-cli-confirm-gate-v1'

OLD_BLOCK_RE = re.compile(
    r'(?P<indent>[ \t]*)# openjarvis-confirm-policy-v1 \(W56\)\n'
    r'.*?'
    r'(?P=indent)agent_kwargs\["confirm_callback"\] = ConfirmPolicy\(\n'
    r'.*?'
    r'\n(?P=indent)\)\n',
    re.DOTALL,
)

NEW_SITE = (
    '{i}# {m} (W61)\n'
    '{i}# Was the W56 ConfirmPolicy (attribution only, always approved).\n'
    '{i}# Now a real terminal gate: deny by default, non-TTY denies.\n'
    '{i}agent_kwargs["confirm_callback"] = TerminalConfirmGate()\n'
)

CLASS_SRC = '''# --- openjarvis-cli-confirm-gate-v1 (W61) ------------------------------------
# A REAL gate for the interactive CLI path. Replaces the W56 ConfirmPolicy at
# site cli-ask, which only attributed a self-approval. A human is at this
# terminal, so ask them. Deny is the default. A stdin that is not a TTY
# denies WITHOUT reading. Every branch logs POLICY site=cli-ask to
# dispatch.log AND writes the decision into confirm_registry: the executor
# treats a False with no recorded decision as a TIMEOUT and tells the model
# the user did not deny it, which would turn a refusal into a re-request.


class TerminalConfirmGate:
    """Ask the person at the terminal. Only "y" or "yes" approves."""

    SITE = "cli-ask"
    _YES = ("y", "yes")
    _NO = ("n", "no")

    def __init__(self, stdin=None, stderr=None) -> None:
        # Injected streams exist for the harness; None means sys.* at call time.
        self._stdin = stdin
        self._stderr = stderr

    def __repr__(self) -> str:
        return "<TerminalConfirmGate site=%s default=DENY>" % self.SITE

    def _log(self, decision, human_present, answer, registry, reason, prompt):
        from openjarvis.tools import _stubs as _st

        _st._get_dispatch_logger().info(
            "POLICY site=%s decision=%s human_present=%s turn=%s"
            " confirm_id=%s answer=%s registry=%s reason=%s prompt=%s",
            self.SITE,
            decision,
            human_present,
            _st.CURRENT_TURN_ID.get(),
            _st.CURRENT_CONFIRM_ID.get() or "-",
            answer,
            registry,
            reason,
            _st._args_digest(prompt, limit=200),
        )

    def __call__(self, prompt: str) -> bool:
        from openjarvis.core import confirm_registry as _cr
        from openjarvis.tools import _stubs as _st

        stdin = self._stdin if self._stdin is not None else sys.stdin
        stderr = self._stderr if self._stderr is not None else sys.stderr
        cid = _st.CURRENT_CONFIRM_ID.get()

        def _record(decision):
            if not cid:
                return "no-id"
            try:
                return "recorded" if _cr.resolve(cid, decision) else "rejected"
            except Exception as exc:
                return "error-" + type(exc).__name__

        try:
            tty = bool(stdin is not None and stdin.isatty())
        except Exception:
            tty = False

        if not cid:
            self._log(
                "DENY_NO_CONFIRM_ID", tty, "-", "no-id",
                "gate reached with no confirm_id in context; failing closed",
                prompt,
            )
            return False

        if not tty:
            reg = _record(_cr.DENIED)
            self._log(
                "DENY_NO_TTY", False, "-", reg,
                "stdin is not a terminal; nobody can answer; denied without"
                " asking",
                prompt,
            )
            return False

        enc = getattr(stderr, "encoding", None) or "ascii"
        text = (
            "\\n[CONFIRM] " + str(prompt) + "\\n"
            "  Type y to allow. Anything else denies. [y/N]: "
        )
        try:
            text = text.encode(enc, "replace").decode(enc, "replace")
            stderr.write(text)
            stderr.flush()
        except Exception as exc:
            reg = _record(_cr.DENIED)
            self._log(
                "DENY_PROMPT_UNSHOWABLE", True, "-", reg,
                "could not display the prompt: " + type(exc).__name__,
                prompt,
            )
            return False

        self._log(
            "WAIT", True, "-", "pending",
            "blocking on a y/N answer from the terminal",
            prompt,
        )
        try:
            raw = stdin.readline()
        except KeyboardInterrupt:
            reg = _record(_cr.DENIED)
            self._log(
                "DENY_INTERRUPT", True, "^C", reg,
                "operator interrupted at the prompt",
                prompt,
            )
            raise
        except Exception as exc:
            reg = _record(_cr.DENIED)
            self._log(
                "DENY_STDIN_ERROR", True, "-", reg,
                "stdin read failed: " + type(exc).__name__,
                prompt,
            )
            return False

        if raw == "":
            reg = _record(_cr.DENIED)
            self._log(
                "DENY_EOF", True, "<eof>", reg,
                "end of input at the prompt",
                prompt,
            )
            return False

        answer = raw.strip().lower()
        shown = ascii(answer[:20])
        if answer in self._YES:
            reg = _record(_cr.APPROVED)
            if reg == "recorded":
                self._log(
                    "APPROVE", True, shown, reg,
                    "operator typed yes",
                    prompt,
                )
                return True
            self._log(
                "LATE_ANSWER_REJECTED", True, shown, reg,
                "operator said yes but the registry refused it (expired or"
                " already decided); NOT approved",
                prompt,
            )
            return False
        if answer == "":
            decision, why = "DENY_DEFAULT", "empty answer; default is deny"
        elif answer in self._NO:
            decision, why = "DENY", "operator typed no"
        else:
            decision, why = (
                "DENY_UNRECOGNIZED", "answer was not y/yes; treated as deny"
            )
        reg = _record(_cr.DENIED)
        self._log(decision, True, shown, reg, why, prompt)
        return False


'''


def main():
    if not os.path.isfile(ASK):
        print('MISSING: %s' % ASK)
        return 1
    with open(ASK, 'rb') as fh:
        raw = fh.read()
    has_bom = raw.startswith(BOM)
    body = raw[3:] if has_bom else raw
    try:
        text = body.decode('utf-8')
    except UnicodeDecodeError as exc:
        print('ABORT: ask.py is not valid UTF-8 (%s). Nothing written.' % exc)
        return 1
    crlf = '\r\n' in text
    text = text.replace('\r\n', '\n')

    if MARKER in text:
        print('ABORT: %s already present. Nothing written.' % MARKER)
        return 1
    if not re.search(r'^import sys$', text, re.MULTILINE):
        print('ABORT: module-level "import sys" not found. Nothing written.')
        return 1

    hits = list(OLD_BLOCK_RE.finditer(text))
    if len(hits) != 1:
        print('ABORT: W56 cli-ask block matched %d times (expected 1). '
              'Nothing written.' % len(hits))
        return 1
    m = hits[0]
    old = m.group(0)
    if 'site="cli-ask"' not in old or 'human_present=True' not in old:
        print('ABORT: matched block lacks site="cli-ask" or '
              'human_present=True. Nothing written.')
        return 1
    if old.count('\n') > 25:
        print('ABORT: matched block spans %d lines (max 25) - anchor ran '
              'wide. Nothing written.' % old.count('\n'))
        return 1
    new_site = NEW_SITE.format(i=m.group('indent'), m=MARKER)
    text2 = text[:m.start()] + new_site + text[m.end():]

    anchor = '\ndef _run_agent(\n'
    if text2.count(anchor) != 1:
        print('ABORT: "def _run_agent(" found %d times (expected 1). '
              'Nothing written.' % text2.count(anchor))
        return 1
    pos = text2.index(anchor) + 1
    text3 = text2[:pos] + CLASS_SRC + text2[pos:]

    out = text3.replace('\n', '\r\n') if crlf else text3
    outbytes = (BOM if has_bom else b'') + out.encode('utf-8')
    try:
        compile(outbytes, ASK, 'exec')
    except SyntaxError as exc:
        print('ABORT: patched ask.py does not compile: %s. Nothing written.'
              % exc)
        return 1

    bak = ASK + '.' + TAG
    shutil.copy2(ASK, bak)
    with open(ASK, 'wb') as fh:
        fh.write(outbytes)

    lines = text3.split('\n')
    cls_line = next(i + 1 for i, ln in enumerate(lines)
                    if ln.startswith('class TerminalConfirmGate'))
    site_line = next(i + 1 for i, ln in enumerate(lines)
                     if 'TerminalConfirmGate()' in ln)
    calls_left = len(re.findall(r'ConfirmPolicy\(', text3))

    print('=' * 68)
    print('W61 ASK.PY GATE PATCH - %s' % STAMP)
    print('=' * 68)
    print('FILE        : %s' % ASK)
    print('BACKUP      : %s' % bak)
    print('BOM / CRLF  : %s / %s (preserved)' % (has_bom, crlf))
    print('LINES       : %d -> %d' % (text.count('\n'), text3.count('\n')))
    print('W56 BLOCK   : %d lines removed' % old.count('\n'))
    print('CLASS       : TerminalConfirmGate at line %d' % cls_line)
    print('SITE        : line %d  %s' % (site_line, lines[site_line - 1].strip()))
    print('ConfirmPolicy( calls left in ask.py: %d (expected 0)' % calls_left)
    print('COMPILE     : OK')
    print('=' * 68)
    print('NOT a verification. Run the W61 harness.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
