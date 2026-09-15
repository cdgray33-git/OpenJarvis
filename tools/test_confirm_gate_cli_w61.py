#!/usr/bin/env python3
"""W61 harness - openjarvis-cli-confirm-gate-v1 (ask.py TerminalConfirmGate).

Supersedes test_confirm_policy_cli.py (W56): its checks 2-4 assert the
ConfirmPolicy this patch removes and will now FAIL by design.

Runs to completion with NO operator input: every answer is scripted
through fake stdin/stderr objects.

dispatch.log is redirected to a temp dir BEFORE any openjarvis import, so
harness POLICY lines never land in the real log. The harness then reads
that temp log back - the instrument proves where its output lands.

Run from the repo root. Exits nonzero on any FAIL.
"""
import ast
import inspect
import io
import os
import re
import sys
import tempfile
import time
import tokenize

TMP = tempfile.mkdtemp(prefix="w61gate_")
os.environ["LOCALAPPDATA"] = TMP
os.environ.pop("OPENJARVIS_CONFIRM_TTL", None)
sys.path.insert(0, os.path.join(os.getcwd(), "src"))
ASK = os.path.join("src", "openjarvis", "cli", "ask.py")
SRV = os.path.join("src", "openjarvis", "cli", "serve.py")
LOG = os.path.join(TMP, "OpenJarvis", "logs", "dispatch.log")

results = []


def check(n, ok, detail=""):
    results.append((n, bool(ok)))
    print(("PASS " if ok else "FAIL ") + n + ("  " + detail if detail else ""))


# ---------------------------------------------------------------- static --
pat = re.compile(r"confirm_callback\s*[=:]\s*.{0,20}lambda[^\n]*True")


def noncode_lines(fp):
    out = set()
    try:
        with io.open(fp, encoding="utf-8") as fh:
            for tok in tokenize.generate_tokens(fh.readline):
                if tok.type in (tokenize.COMMENT, tokenize.STRING):
                    for ln in range(tok.start[0], tok.end[0] + 1):
                        out.add(ln)
    except Exception:
        return None
    return out


hits = []
for root, dirs, files in os.walk("src"):
    for f in files:
        if not f.endswith(".py"):
            continue
        fp = os.path.join(root, f)
        try:
            body = open(fp, encoding="utf-8", errors="replace").read()
        except OSError:
            continue
        found = [body[:m.start()].count("\n") + 1 for m in pat.finditer(body)]
        if not found:
            continue
        skip = noncode_lines(fp)
        if skip is None:
            hits.append(fp + ":UNPARSEABLE")
            continue
        real = [ln for ln in found if ln not in skip]
        if real:
            hits.append("%s:%s" % (fp, real))
check("01 zero auto-approve lambdas in CODE tree-wide", not hits, str(hits))

atext = open(ASK, encoding="utf-8-sig").read()
atree = ast.parse(atext)


def call_name(node):
    f = node.func
    return getattr(f, "id", None) or getattr(f, "attr", None)


cp_calls = [n for n in ast.walk(atree)
            if isinstance(n, ast.Call) and call_name(n) == "ConfirmPolicy"]
check("02 ask.py constructs ZERO ConfirmPolicy", not cp_calls,
      "found %d" % len(cp_calls))

gate_assigns = []
for n in ast.walk(atree):
    if not isinstance(n, ast.Assign) or len(n.targets) != 1:
        continue
    t = n.targets[0]
    if not isinstance(t, ast.Subscript):
        continue
    key = t.slice.value if isinstance(t.slice, ast.Constant) else None
    if key == "confirm_callback" and isinstance(n.value, ast.Call) \
            and call_name(n.value) == "TerminalConfirmGate":
        gate_assigns.append(n)
check("03 ask.py sets confirm_callback = TerminalConfirmGate() once",
      len(gate_assigns) == 1, "found %d" % len(gate_assigns))

top_classes = [n.name for n in atree.body if isinstance(n, ast.ClassDef)]
check("04 TerminalConfirmGate is module-level and marked",
      "TerminalConfirmGate" in top_classes
      and "openjarvis-cli-confirm-gate-v1" in atext)

stext = open(SRV, encoding="utf-8-sig").read()
ast.parse(stext)
need = ["decision=DENY_NO_CONFIRM_ID", "decision=WAIT", "site=chat-agent-live"]
missing = [x for x in need if x not in stext]
check("05 serve.py gate logs all three branches", not missing, str(missing))

seg = stext[stext.find("def _server_confirm_callback"):]
cut = seg.find('agent_kwargs["interactive"]')
seg = seg[:cut] if cut > 0 else seg
check("06 serve.py gate still returns the registry outcome",
      "_outcome == _cr.APPROVED" in seg and "return True" not in seg)

err = ""
try:
    import importlib
    askmod = importlib.import_module("openjarvis.cli.ask")
    importlib.import_module("openjarvis.cli.serve")
    TerminalConfirmGate = askmod.TerminalConfirmGate
    from openjarvis.core import confirm_registry as _cr
    from openjarvis.tools import _stubs as _st
    ok7 = True
except Exception as e:
    ok7, err = False, "%s: %s" % (type(e).__name__, e)
check("07 ask.py, serve.py, registry, stubs import", ok7, err)
if not ok7:
    print("\nRESULT %d/%d PASS (behavioral checks skipped)"
          % (sum(1 for _, ok in results if ok), len(results)))
    sys.exit(1)


# ------------------------------------------------------------ behavioral --
class FakeIn:
    def __init__(self, data="", tty=True, exc=None):
        self.data, self.tty, self.exc, self.reads = data, tty, exc, 0

    def isatty(self):
        return self.tty

    def readline(self):
        self.reads += 1
        if self.exc is not None:
            raise self.exc
        return self.data


class FakeErr:
    encoding = "cp1252"

    def __init__(self):
        self.parts = []

    def write(self, s):
        self.parts.append(s)

    def flush(self):
        pass

    def text(self):
        return "".join(self.parts)


def run_case(label, stdin, set_cid=True, ttl=None, sleep=0.0, prompt=None):
    cid = _cr.register(tool="w61_gate_probe", agent_id="w61h",
                       turn_id="w61h-" + label, ttl=ttl)
    if sleep:
        time.sleep(sleep)
    errs = FakeErr()
    gate = TerminalConfirmGate(stdin=stdin, stderr=errs)
    if prompt is None:
        prompt = ("Allow execution of tool 'w61_gate_probe' with args "
                  '{"case": "%s"}?' % label)
    t1 = _st.CURRENT_TURN_ID.set("w61h-" + label)
    t2 = _st.CURRENT_CONFIRM_ID.set(cid if set_cid else "")
    raised = None
    rv = None
    try:
        rv = gate(prompt)
    except BaseException as e:  # noqa: BLE001 - KeyboardInterrupt case
        raised = e
    finally:
        _st.CURRENT_CONFIRM_ID.reset(t2)
        _st.CURRENT_TURN_ID.reset(t1)
    snap = _cr.get(cid) or {}
    return rv, snap.get("decision"), errs.text(), raised


A, D, T = _cr.APPROVED, _cr.DENIED, _cr.TIMEOUT
# label, stdin, kwargs, expected return, expected registry, log token
CASES = [
    ("yes_short", FakeIn("y\n"), {}, True, A, "APPROVE"),
    ("yes_long", FakeIn("  YES \r\n"), {}, True, A, "APPROVE"),
    ("no", FakeIn("n\n"), {}, False, D, "DENY"),
    ("empty", FakeIn("\n"), {}, False, D, "DENY_DEFAULT"),
    ("eof", FakeIn(""), {}, False, D, "DENY_EOF"),
    ("other", FakeIn("sure\n"), {}, False, D, "DENY_UNRECOGNIZED"),
    ("notty", FakeIn("y\n", tty=False), {}, False, D, "DENY_NO_TTY"),
    ("nocid", FakeIn("y\n"), {"set_cid": False}, False, None,
     "DENY_NO_CONFIRM_ID"),
    ("expired", FakeIn("y\n"), {"ttl": 0.05, "sleep": 0.2}, False, T,
     "LATE_ANSWER_REJECTED"),
    ("stdinerr", FakeIn(exc=OSError("boom")), {}, False, D,
     "DENY_STDIN_ERROR"),
    ("unicode", FakeIn("y\n"),
     {"prompt": "Allow tool 'x' with args {\"s\": \"a \u2192 b\"}?"},
     True, A, "APPROVE"),
]

n = 8
for label, stdin, kw, exp_rv, exp_reg, token in CASES:
    rv, reg, shown, raised = run_case(label, stdin, **kw)
    ok = raised is None and rv is exp_rv and reg == exp_reg
    detail = "rv=%r registry=%r raised=%r" % (rv, reg, raised)
    if label == "notty":
        ok = ok and stdin.reads == 0 and shown == ""
        detail += " reads=%d prompt_shown=%s" % (stdin.reads, bool(shown))
    elif label != "nocid":
        ok = ok and "[CONFIRM]" in shown and "[y/N]" in shown
    if label == "unicode":
        ok = ok and "?" in shown and "\u2192" not in shown
    check("%02d case %-9s -> %s" % (n, label, token), ok, detail)
    n += 1

intr = FakeIn(exc=KeyboardInterrupt())
rv, reg, shown, raised = run_case("interrupt", intr)
check("%02d case interrupt -> re-raised, registry denied" % n,
      isinstance(raised, KeyboardInterrupt) and reg == D,
      "raised=%r registry=%r" % (type(raised).__name__, reg))
n += 1

# ------------------------------------------------------ log landing check --
try:
    logtext = open(LOG, encoding="utf-8").read()
except OSError as e:
    logtext = ""
    print("  (could not read %s: %s)" % (LOG, e))
want = [(c[0], c[5]) for c in CASES] + [("interrupt", "DENY_INTERRUPT")]
absent = []
for label, token in want:
    rx = re.compile(r"POLICY site=cli-ask decision=%s .*turn=w61h-%s "
                    % (re.escape(token), re.escape(label)))
    if not rx.search(logtext):
        absent.append("%s/%s" % (label, token))
waits = len(re.findall(r"POLICY site=cli-ask decision=WAIT ", logtext))
check("%02d every case logged POLICY site=cli-ask to the temp dispatch.log"
      % n, not absent and waits >= 8,
      "missing=%s WAIT_lines=%d log=%s" % (absent, waits, LOG))
n += 1

# ----------------------------------------------- end-to-end via executor --
from openjarvis.core.types import ToolCall, ToolResult  # noqa: E402
from openjarvis.tools._stubs import (  # noqa: E402
    BaseTool, ToolExecutor, ToolSpec, _outcome_reason,
)


def make_call(name, args):
    kw = {"name": name, "arguments": args}
    try:
        for p in inspect.signature(ToolCall).parameters.values():
            if p.name in kw:
                continue
            if p.default is inspect.Parameter.empty and p.kind in (
                    p.POSITIONAL_OR_KEYWORD, p.KEYWORD_ONLY):
                kw[p.name] = "w61h-" + p.name
    except (TypeError, ValueError):
        pass
    return ToolCall(**kw)


class Probe(BaseTool):
    tool_id = "w61_gate_probe"

    def __init__(self):
        self.ran = 0

    @property
    def spec(self):
        return ToolSpec(name="w61_gate_probe", description="W61 probe",
                        requires_confirmation=True, timeout_seconds=5.0)

    def execute(self, **params):
        self.ran += 1
        return ToolResult(tool_name="w61_gate_probe", content="ran",
                          success=True)


def e2e(label, answer):
    probe = Probe()
    ex = ToolExecutor(
        [probe], interactive=True,
        confirm_callback=TerminalConfirmGate(stdin=FakeIn(answer),
                                             stderr=FakeErr()),
    )
    tok = _st.CURRENT_TURN_ID.set("w61h-" + label)
    try:
        res = ex.execute(make_call("w61_gate_probe", '{"x": 1}'))
    finally:
        _st.CURRENT_TURN_ID.reset(tok)
    return probe.ran, res


try:
    ran, res = e2e("e2e-deny", "n\n")
    reason = _outcome_reason(res)
    check("%02d executor: typed n -> tool NOT run, reason=GATE_DENIED" % n,
          ran == 0 and not res.success and reason == "GATE_DENIED",
          "ran=%d success=%s reason=%s" % (ran, res.success, reason))
except Exception as e:
    check("%02d executor: typed n" % n, False,
          "%s: %s" % (type(e).__name__, e))
n += 1

try:
    ran, res = e2e("e2e-approve", "y\n")
    reason = _outcome_reason(res)
    check("%02d executor: typed y -> tool ran once, reason=OK" % n,
          ran == 1 and res.success and reason == "OK",
          "ran=%d success=%s reason=%s" % (ran, res.success, reason))
except Exception as e:
    check("%02d executor: typed y" % n, False,
          "%s: %s" % (type(e).__name__, e))
n += 1

try:
    ran, res = e2e("e2e-eof", "")
    reason = _outcome_reason(res)
    check("%02d executor: no answer -> NOT run, reported as DENIED not "
          "TIMEOUT" % n,
          ran == 0 and reason == "GATE_DENIED",
          "ran=%d reason=%s" % (ran, reason))
except Exception as e:
    check("%02d executor: no answer" % n, False,
          "%s: %s" % (type(e).__name__, e))
n += 1

bad = [name for name, ok in results if not ok]
print("")
print("TEMP LOG: %s" % LOG)
print("RESULT %d/%d PASS" % (len(results) - len(bad), len(results)))
sys.exit(1 if bad else 0)
