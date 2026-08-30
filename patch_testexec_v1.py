#!/usr/bin/env python3
"""
patch_testexec_v1.py - add POST /v1/tools/test-execute to tools_router.

Marker: openjarvis-test-exec-v1
Target: src\\openjarvis\\server\\agent_manager_routes.py  (CRLF, double-encoded
        comment rules, pre-existing - this patch never touches a rule comment)

Run from the repo root:
    python .\\patch_testexec_v1.py            (dry run + replica self-test)
    python .\\patch_testexec_v1.py --apply    (writes, after the same checks)

Prints the interpreter it resolved to (W19-R2).
Dry-runs every anchor against a CRLF replica before touching the real file
(W19-R4).  Idempotent: refuses to apply twice on the marker.
"""

import hashlib
import os
import py_compile
import shutil
import sys
import time

MARKER = "openjarvis-test-exec-v1"
REL = os.path.join("src", "openjarvis", "server", "agent_manager_routes.py")
EXPECT_SHA = "94EC6F3F3351EB8F7FAFA09200FF5B393A1D92D4314430F50B273DF59AD00E1C"
EXPECT_LEN = 91395

ANCHOR = [
    '                "decision": entry.get("decision", ""),',
    "            },",
    "        )",
]

BLOCK = '''
    # openjarvis-test-exec-v1
    #
    # Deterministic trigger for the interactive confirmation gate.
    # Uses the LIVE chat agent's executor - constructs nothing - so what is
    # measured is the instance 6d wired, on serve.py's bus, with the real
    # confirm callback and the real agent_id.
    #
    # It is structurally incapable of running a tool that does not declare
    # requires_confirmation=True, so it is a trigger, not a bypass: every
    # accepted call parks on the gate and waits for POST /v1/tools/confirm.
    #
    # Disabled unless OPENJARVIS_TEST_EXEC is set AND the bind is loopback.
    # Both refusals are 403 with a distinct body so a probe can tell
    # "present but disabled" from "never mounted" (404).

    @tools_router.post("/test-execute")
    async def test_execute_tool(request: Request):
        import asyncio as _asyncio
        import json as _json
        import logging as _logging
        import os as _os
        import uuid as _uuid

        from fastapi.responses import JSONResponse

        from openjarvis.core.types import ToolCall as _ToolCall

        _log = _logging.getLogger(__name__)

        _flag = str(_os.environ.get("OPENJARVIS_TEST_EXEC", "")).strip().lower()
        if _flag in ("", "0", "false", "no", "off"):
            return JSONResponse(
                status_code=403,
                content={
                    "error": "test-execute disabled",
                    "reason": "OPENJARVIS_TEST_EXEC not set",
                    "marker": "openjarvis-test-exec-v1",
                },
            )

        if not bool(getattr(request.app.state, "bind_is_loopback", False)):
            return JSONResponse(
                status_code=403,
                content={
                    "error": "test-execute disabled",
                    "reason": "bind is not loopback",
                    "marker": "openjarvis-test-exec-v1",
                },
            )

        _agent = getattr(request.app.state, "agent", None)
        _executor = getattr(_agent, "_executor", None) if _agent is not None else None
        if _executor is None:
            return JSONResponse(
                status_code=409,
                content={
                    "error": "no live agent executor",
                    "agent": repr(_agent)[:120],
                },
            )

        try:
            _body = await request.json()
        except Exception:
            _body = {}
        if not isinstance(_body, dict):
            _body = {}

        _tool_name = str(_body.get("tool") or "").strip()
        _args = _body.get("arguments")
        if not isinstance(_args, dict):
            _args = {}

        if not _tool_name:
            return JSONResponse(
                status_code=400,
                content={"error": "tool is required"},
            )

        _specs = list(_executor.available_tools())
        _spec = None
        for _s in _specs:
            if getattr(_s, "name", "") == _tool_name:
                _spec = _s
                break

        if _spec is None:
            return JSONResponse(
                status_code=404,
                content={
                    "error": "tool not on the live agent",
                    "tool": _tool_name,
                    "available": [getattr(x, "name", "") for x in _specs],
                },
            )

        if not bool(getattr(_spec, "requires_confirmation", False)):
            return JSONResponse(
                status_code=422,
                content={
                    "error": "tool does not require confirmation - refused",
                    "tool": _tool_name,
                },
            )

        _run_id = _uuid.uuid4().hex[:8]
        _turn_id = "test-" + _run_id
        _call = _ToolCall(
            id="testexec-" + _run_id,
            name=_tool_name,
            arguments=_json.dumps(_args),
        )

        def _run() -> None:
            from openjarvis.tools import _stubs as _ts

            _token = _ts.CURRENT_TURN_ID.set(_turn_id)
            try:
                _executor.execute(_call)
            except Exception:
                _log.warning("test-execute run failed", exc_info=True)
            finally:
                try:
                    _ts.CURRENT_TURN_ID.reset(_token)
                except Exception:
                    pass

        _tasks = getattr(request.app.state, "_testexec_tasks", None)
        if _tasks is None:
            _tasks = set()
            request.app.state._testexec_tasks = _tasks
        _task = _asyncio.create_task(_asyncio.to_thread(_run))
        _tasks.add(_task)
        _task.add_done_callback(_tasks.discard)

        return JSONResponse(
            status_code=202,
            content={
                "accepted": True,
                "run_id": _run_id,
                "turn_id": _turn_id,
                "tool": _tool_name,
                "marker": "openjarvis-test-exec-v1",
            },
        )
'''


def strip_cr(lines):
    return [ln[:-1] if ln.endswith("\r") else ln for ln in lines]


def find_anchor(lines):
    """Return the index of the LAST anchor line. Requires exactly one match."""
    bare = strip_cr(lines)
    hits = []
    first = ANCHOR[0]
    for i, ln in enumerate(bare):
        if ln != first:
            continue
        if bare[i:i + len(ANCHOR)] == ANCHOR:
            hits.append(i)
    if len(hits) != 1:
        return None, len(hits)
    return hits[0] + len(ANCHOR) - 1, 1


def build_lines(text):
    return text.split("\n")


def insert_block(text):
    lines = build_lines(text)
    idx, n = find_anchor(lines)
    if idx is None:
        return None, n, 0
    crlf_style = lines[idx].endswith("\r")
    new_lines = BLOCK.split("\n")
    if new_lines and new_lines[-1] == "":
        new_lines = new_lines[:-1]
    if crlf_style:
        new_lines = [ln + "\r" for ln in new_lines]
    out = lines[:idx + 1] + new_lines + lines[idx + 1:]
    return "\n".join(out), 1, len(new_lines)


def counts(text):
    crlf = text.count("\r\n")
    lf = text.count("\n")
    return crlf, lf - crlf


def selftest():
    print("--- REPLICA SELF-TEST (CRLF) ---")
    replica_src = [
        "    @tools_router.post(\"/confirm\")",
        "    async def confirm_tool(request: Request):",
        "        pass",
        "        return JSONResponse(",
        "            status_code=409,",
        "            content={",
        "                \"error\": \"already resolved\",",
        "                \"decision\": entry.get(\"decision\", \"\"),",
        "            },",
        "        )",
        "",
        "    sendblue_router = APIRouter(prefix=\"/v1/channels/sendblue\")",
        "",
    ]
    replica = "\r\n".join(replica_src)
    pre_crlf, pre_lf = counts(replica)
    print("replica CRLF %d BARELF %d" % (pre_crlf, pre_lf))

    out, n, inserted = insert_block(replica)
    if out is None:
        print("FAIL anchor matched %d times on replica" % n)
        return False
    post_crlf, post_lf = counts(out)
    print("anchor hits 1 OK / inserted %d lines" % inserted)
    print("post CRLF %d BARELF %d" % (post_crlf, post_lf))
    ok = True
    if post_crlf != pre_crlf + inserted:
        print("FAIL CRLF delta %d expected %d" % (post_crlf - pre_crlf, inserted))
        ok = False
    if post_lf != pre_lf:
        print("FAIL bare LF changed %d -> %d" % (pre_lf, post_lf))
        ok = False
    if MARKER not in out:
        print("FAIL marker absent from replica output")
        ok = False
    if "sendblue_router" not in out:
        print("FAIL control lost - sendblue_router")
        ok = False
    if out.index(MARKER) > out.index("sendblue_router"):
        print("FAIL block landed AFTER the sendblue router")
        ok = False
    out2, n2, ins2 = insert_block(out)
    if out2 is not None and MARKER in out and ins2 > 0:
        if out2.count(MARKER) > out.count(MARKER):
            print("NOTE idempotence is enforced by the marker guard, not the anchor")
    print("replica self-test %s" % ("OK" if ok else "FAILED"))
    return ok


def main():
    apply = "--apply" in sys.argv
    print("INTERPRETER %s" % sys.executable)
    print("CWD %s" % os.getcwd())
    print("MODE %s" % ("APPLY" if apply else "DRY RUN"))

    if not selftest():
        print("ABORT replica self-test failed")
        return 1

    path = os.path.join(os.getcwd(), REL)
    if not os.path.isfile(path):
        print("ABORT target not found: %s" % path)
        return 1

    with open(path, "rb") as fh:
        raw = fh.read()
    sha = hashlib.sha256(raw).hexdigest().upper()
    text = raw.decode("utf-8")
    pre_crlf, pre_lf = counts(text)

    print("--- TARGET ---")
    print("PATH %s" % path)
    print("LEN %d (expected %d)" % (len(raw), EXPECT_LEN))
    print("SHA %s" % sha)
    print("CRLF %d BARELF %d" % (pre_crlf, pre_lf))

    if MARKER in text:
        print("ALREADY APPLIED - marker present. Nothing to do.")
        return 0
    if sha != EXPECT_SHA:
        print("ABORT SHA does not match the file this patch was written against.")
        return 1

    out, n, inserted = insert_block(text)
    if out is None:
        print("ABORT anchor matched %d times, expected exactly 1" % n)
        return 1
    post_crlf, post_lf = counts(out)
    print("--- DRY RESULT ---")
    print("anchor hits 1 OK")
    print("inserted %d lines" % inserted)
    print("predicted LEN %d (delta +%d)" % (len(out.encode("utf-8")),
                                            len(out.encode("utf-8")) - len(raw)))
    print("predicted CRLF %d (delta +%d)" % (post_crlf, post_crlf - pre_crlf))
    print("predicted BARELF %d (was %d)" % (post_lf, pre_lf))

    if post_crlf != pre_crlf + inserted:
        print("ABORT CRLF delta wrong")
        return 1
    if post_lf != pre_lf:
        print("ABORT bare LF count changed")
        return 1

    enc_probe = "SendBlue auto-setup helpers"
    if text.count(enc_probe) != out.count(enc_probe):
        print("ABORT encoding control changed")
        return 1
    print("ENCODING CONTROL ok (%d occurrence)" % out.count(enc_probe))

    if not apply:
        print("DRY RUN COMPLETE - nothing written. Re-run with --apply")
        return 0

    stamp = time.strftime("%Y%m%d_%H%M%S")
    bak = path + ".bak_testexec_" + stamp
    shutil.copy2(path, bak)
    print("BACKUP %s" % bak)

    with open(path, "wb") as fh:
        fh.write(out.encode("utf-8"))

    with open(path, "rb") as fh:
        raw2 = fh.read()
    text2 = raw2.decode("utf-8")
    c2, l2 = counts(text2)
    print("--- POST WRITE ---")
    print("LEN %d" % len(raw2))
    print("SHA %s" % hashlib.sha256(raw2).hexdigest().upper())
    print("CRLF %d BARELF %d" % (c2, l2))
    print("MARKER %d" % text2.count(MARKER))
    print("ROUTE %d" % text2.count('@tools_router.post("/test-execute")'))
    print("CONTROL confirm route %d" % text2.count('@tools_router.post("/confirm")'))
    print("CONTROL sendblue %d" % text2.count("sendblue_router = APIRouter"))

    try:
        py_compile.compile(path, doraise=True)
        print("PY_COMPILE OK")
    except Exception as exc:
        print("PY_COMPILE FAILED: %s" % exc)
        print("RESTORE: copy \"%s\" \"%s\"" % (bak, path))
        return 1

    print("APPLIED. Backend restart required before the route exists.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
