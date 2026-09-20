"""patch_cid_redact_v3.py

W19 PATCH - repoint the confirm_id redaction from socket auth to the loopback
bind, per Gray's 2026-08-29 ruling (W17 s4 consequence 2, never implemented -
rule W18-R6).

WHAT IT CHANGES

  src\\openjarvis\\cli\\serve.py
    Publishes the ALREADY-COMPUTED _is_loop (line ~613) onto app.state.
    No second computation of the predicate. That is deliberate: two independent
    derivations of the same security predicate is the defect class this
    codebase already has (W18 s6.B hazard note).

  src\\openjarvis\\server\\ws_bridge.py
    1. At accept, reads app.state.bind_is_loopback and stamps the socket as
       _ws_bind_loopback, beside the existing _ws_authed stamp.
    2. Adds bind_loopback=%s to the ws-accept line so the posture is
       recoverable from the log on every connection.
    3. Line 61 now keys the redaction on _ws_bind_loopback, not _ws_authed.

  FAIL-CLOSED: getattr default is False. If app.state has no bind_is_loopback
  (a non-serve.py entry point, or a mount order change), confirm_id is
  STRIPPED, not delivered, and ws-accept records bind_loopback=False so the
  cause is visible rather than silent.

IDEMPOTENT. Refuses to run twice on the marker openjarvis-ws-cid-redact-v3.
Backs up both files before touching either, and writes neither unless BOTH
edits resolve to exactly one match.

RUN FROM: repo root.
"""

from __future__ import annotations

import shutil
import sys
from pathlib import Path

MARKER = "openjarvis-ws-cid-redact-v3"

SERVE = Path("src/openjarvis/cli/serve.py")
BRIDGE = Path("src/openjarvis/server/ws_bridge.py")
SERVE_BAK = Path("src/openjarvis/cli/serve.py.bak-cidv3")
BRIDGE_BAK = Path("src/openjarvis/server/ws_bridge.py.bak-cidv3")


def read(p: Path) -> tuple[str, str]:
    """Return (text, line_ending) without normalizing the file's endings."""
    raw = p.read_bytes().decode("utf-8")
    eol = "\r\n" if "\r\n" in raw else "\n"
    return raw, eol


def block(lines: list[str], eol: str) -> str:
    return eol.join(lines)


# ---------------- anchors, as line lists so EOL style is matched ----------------

SERVE_OLD = [
    "    try:",
    "        _is_loop = _ipa.ip_address(bind_host).is_loopback",
    "    except ValueError:",
    '        _is_loop = bind_host in ("localhost", "")',
]

SERVE_NEW = SERVE_OLD + [
    "",
    f"    # {MARKER}",
    "    # The confirm-channel redaction in server/ws_bridge.py keys on this",
    "    # value. Published, never re-derived there. See W18 s6.B.",
    "    app.state.bind_is_loopback = _is_loop",
]

BRIDGE_STAMP_OLD = [
    "        websocket._ws_peer = _peer  # type: ignore[attr-defined]",
]

BRIDGE_STAMP_NEW = BRIDGE_STAMP_OLD + [
    f"        # {MARKER}",
    "        # Redaction posture comes from the server bind, not from a token.",
    "        # Absent attribute means fail closed: strip confirm_id.",
    '        _app_state = getattr(getattr(websocket, "app", None), "state", None)',
    '        _bind_loop = bool(getattr(_app_state, "bind_is_loopback", False))',
    "        websocket._ws_bind_loopback = _bind_loop  # type: ignore[attr-defined]",
]

BRIDGE_LOG_OLD = [
    "        logger.warning(",
    '            "ws-accept: peer=%s authed=%s agent_filter=%s ua=%r",',
    "            _peer,",
    "            _authed,",
    "            agent_id,",
    '            websocket.headers.get("user-agent"),',
    "        )",
]

BRIDGE_LOG_NEW = [
    "        logger.warning(",
    '            "ws-accept: peer=%s authed=%s bind_loopback=%s agent_filter=%s ua=%r",',
    "            _peer,",
    "            _authed,",
    "            _bind_loop,",
    "            agent_id,",
    '            websocket.headers.get("user-agent"),',
    "        )",
]

BRIDGE_GATE_OLD = [
    "            client_payload = payload",
    '            if _is_confirm_event and not getattr(ws, "_ws_authed", False):',
    '                _data = dict(payload["data"])',
    '                _had_cid = _data.pop("confirm_id", None) is not None',
    "                client_payload = dict(payload, data=_data)",
    "                if _had_cid:",
    "                    logger.warning(",
    '                        "ws-cid-redact: stripped confirm_id from %s "',
    '                        "for unauthenticated subscriber %s",',
    "                        event.event_type.value,",
    '                        getattr(ws, "_ws_peer", "unknown"),',
    "                    )",
]

BRIDGE_GATE_NEW = [
    "            client_payload = payload",
    f"            # {MARKER}",
    '            if _is_confirm_event and not getattr(ws, "_ws_bind_loopback", False):',
    '                _data = dict(payload["data"])',
    '                _had_cid = _data.pop("confirm_id", None) is not None',
    "                client_payload = dict(payload, data=_data)",
    "                if _had_cid:",
    "                    logger.warning(",
    '                        "ws-cid-redact: stripped confirm_id from %s for "',
    '                        "subscriber %s - server bind is not loopback, or the "',
    '                        "bind posture was never published to app.state",',
    "                        event.event_type.value,",
    '                        getattr(ws, "_ws_peer", "unknown"),',
    "                    )",
]


def apply(text: str, old: list[str], new: list[str], eol: str, label: str) -> str:
    o = block(old, eol)
    n = block(new, eol)
    count = text.count(o)
    if count != 1:
        print(f"FAIL: anchor '{label}' matched {count} times, expected exactly 1.")
        print("      No file was written. The source has drifted from the read.")
        sys.exit(3)
    print(f"  ok  {label}")
    return text.replace(o, n, 1)


def main() -> int:
    for p in (SERVE, BRIDGE):
        if not p.exists():
            print(f"FAIL: NOT FOUND: {p}")
            print("Are you at the repo root?")
            return 2

    serve_txt, serve_eol = read(SERVE)
    bridge_txt, bridge_eol = read(BRIDGE)

    if MARKER in serve_txt or MARKER in bridge_txt:
        print(f"ALREADY APPLIED: marker '{MARKER}' is present. Nothing done.")
        return 0

    _n = lambda e: "CRLF" if e == "\r\n" else "LF"
    print("line endings: serve=%s bridge=%s" % (_n(serve_eol), _n(bridge_eol)))
    print("matching anchors:")

    serve_new = apply(serve_txt, SERVE_OLD, SERVE_NEW, serve_eol, "serve.py app.state publish")
    b = apply(bridge_txt, BRIDGE_STAMP_OLD, BRIDGE_STAMP_NEW, bridge_eol, "ws_bridge.py accept stamp")
    b = apply(b, BRIDGE_LOG_OLD, BRIDGE_LOG_NEW, bridge_eol, "ws_bridge.py ws-accept log")
    b = apply(b, BRIDGE_GATE_OLD, BRIDGE_GATE_NEW, bridge_eol, "ws_bridge.py redaction gate")

    shutil.copy2(SERVE, SERVE_BAK)
    shutil.copy2(BRIDGE, BRIDGE_BAK)
    print(f"backups: {SERVE_BAK}")
    print(f"         {BRIDGE_BAK}")

    SERVE.write_bytes(serve_new.encode("utf-8"))
    BRIDGE.write_bytes(b.encode("utf-8"))

    print("\nAPPLIED. Both files written. 4 edits, 2 files.")
    print("The change is INERT until the backend process is restarted.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
