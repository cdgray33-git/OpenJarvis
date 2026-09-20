"""
patch_ws_cid_redact.py - marker openjarvis-ws-cid-redact-v1

Single behavior change to src/openjarvis/server/ws_bridge.py:
  TOOL_CONFIRM_REQUEST frames delivered to an UNAUTHENTICATED websocket
  subscriber have confirm_id stripped. Authenticated subscribers (query
  param token == env OPENJARVIS_WS_TOKEN) get the full frame.

  Fail-closed: if OPENJARVIS_WS_TOKEN is unset or empty, no socket can
  authenticate, so no socket receives a live confirm_id.

Plus one additive log line at WS accept (peer, user-agent, authed) which
is the instrument used to verify the above.

Run from repo root:  python .\patch_ws_cid_redact.py
Creates a timestamped .bak next to the target before writing.
"""

import datetime
import pathlib
import shutil
import sys

TARGET = pathlib.Path("src/openjarvis/server/ws_bridge.py")

# ---------------------------------------------------------------- anchors

OLD_IMPORTS = """import asyncio
import logging
"""

NEW_IMPORTS = """import asyncio
import logging
import os
"""

OLD_FORWARD = """        for ws, (queue, loop) in list(clients.items()):
            agent_filter = getattr(ws, "_agent_filter", None)
            event_agent = (event.data or {}).get("agent_id")
            if agent_filter and event_agent != agent_filter:
                continue
            try:
                loop.call_soon_threadsafe(queue.put_nowait, payload)
"""

NEW_FORWARD = '''        # openjarvis-ws-cid-redact-v1
        _is_confirm_request = event.event_type is EventType.TOOL_CONFIRM_REQUEST
        for ws, (queue, loop) in list(clients.items()):
            agent_filter = getattr(ws, "_agent_filter", None)
            event_agent = (event.data or {}).get("agent_id")
            if agent_filter and event_agent != agent_filter:
                continue
            client_payload = payload
            if _is_confirm_request and not getattr(ws, "_ws_authed", False):
                _data = dict(payload["data"])
                _had_cid = _data.pop("confirm_id", None) is not None
                client_payload = dict(payload, data=_data)
                if _had_cid:
                    logger.warning(
                        "ws-cid-redact: stripped confirm_id from "
                        "TOOL_CONFIRM_REQUEST for unauthenticated subscriber %s",
                        getattr(ws, "_ws_peer", "unknown"),
                    )
            try:
                loop.call_soon_threadsafe(queue.put_nowait, client_payload)
'''

OLD_ACCEPT = """        agent_id = websocket.query_params.get("agent_id")
        websocket._agent_filter = agent_id  # type: ignore[attr-defined]
"""

NEW_ACCEPT = '''        agent_id = websocket.query_params.get("agent_id")
        websocket._agent_filter = agent_id  # type: ignore[attr-defined]
        # openjarvis-ws-cid-redact-v1
        _expected = os.environ.get("OPENJARVIS_WS_TOKEN") or ""
        _offered = websocket.query_params.get("token") or ""
        _authed = bool(_expected) and _offered == _expected
        _client = getattr(websocket, "client", None)
        _peer = f"{getattr(_client, 'host', '?')}:{getattr(_client, 'port', '?')}"
        websocket._ws_authed = _authed  # type: ignore[attr-defined]
        websocket._ws_peer = _peer  # type: ignore[attr-defined]
        logger.warning(
            "ws-accept: peer=%s authed=%s agent_filter=%s ua=%r",
            _peer,
            _authed,
            agent_id,
            websocket.headers.get("user-agent"),
        )
'''

EDITS = [
    ("import os", OLD_IMPORTS, NEW_IMPORTS),
    ("forward loop redaction", OLD_FORWARD, NEW_FORWARD),
    ("accept-time auth + log", OLD_ACCEPT, NEW_ACCEPT),
]

# ---------------------------------------------------------------- apply


def main() -> int:
    if not TARGET.exists():
        print(f"FAIL  target not found: {TARGET.resolve()}")
        print("      run this from the repo root (PS C:\\Users\\Admin\\OpenJarvis>)")
        return 2

    text = TARGET.read_text(encoding="utf-8")

    if "openjarvis-ws-cid-redact-v1" in text:
        print("FAIL  marker openjarvis-ws-cid-redact-v1 already present.")
        print("      file appears already patched; no changes written.")
        return 3

    # verify every anchor matches exactly once BEFORE writing anything
    for name, old, _new in EDITS:
        n = text.count(old)
        if n != 1:
            print(f"FAIL  anchor '{name}' matched {n} times, expected exactly 1.")
            print("      no changes written.")
            return 4
    print("OK    all 3 anchors matched exactly once")

    stamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    backup = TARGET.with_name(f"{TARGET.name}.bak_cidredact_{stamp}")
    shutil.copy2(TARGET, backup)
    print(f"OK    backup written: {backup}")

    for name, old, new in EDITS:
        text = text.replace(old, new, 1)
        print(f"OK    applied: {name}")

    TARGET.write_text(text, encoding="utf-8")
    print(f"OK    wrote {TARGET}")

    # post-write self-check
    after = TARGET.read_text(encoding="utf-8")
    checks = {
        "marker present": after.count("openjarvis-ws-cid-redact-v1") == 2,
        "import os": "\nimport os\n" in after,
        "redact branch": "_ws_authed" in after,
        "per-client payload": "client_payload" in after,
        "accept log": "ws-accept: peer=%s" in after,
    }
    for k, v in checks.items():
        print(f"{'OK   ' if v else 'FAIL '} post-check: {k}")

    import py_compile

    try:
        py_compile.compile(str(TARGET), doraise=True)
        print("OK    py_compile clean")
    except Exception as exc:  # noqa: BLE001
        print(f"FAIL  py_compile: {exc}")
        print(f"      RESTORE:  Copy-Item '{backup}' '{TARGET}' -Force")
        return 5

    print()
    print("RESTORE COMMAND (PowerShell, repo root):")
    print(f"  Copy-Item '{backup}' '{TARGET}' -Force")
    return 0


if __name__ == "__main__":
    sys.exit(main())
