"""Confirm registry - correlation store for interactive tool confirmation.

Defect 6 / Patch 6c.  Marker: openjarvis-confirm-registry-v1

Lives in ``core`` rather than ``server`` so that ``tools/_stubs.py`` and
the route layer can both import it without a circular import.

Threading model, runtime-proven 2026-08-19: on the SSE chat path the whole
synchronous tool chain runs on an ``asyncio.to_thread`` worker (observed
thread name ``asyncio_0``), while the inbound approval POST is served on
the event loop thread.  The waiter therefore blocks a WORKER thread and
the resolver runs on the LOOP thread, so this module uses
``threading.Event`` and never ``asyncio.Event``.  ``Event.set()`` from the
loop thread is non-blocking, so the POST handler returns immediately.

Expired entries are reaped inside ``register`` rather than by a background
task - no new task, no new failure mode.

Decisions are WRITE-ONCE.  ``resolve`` never flips a recorded decision and
returns False instead, which is what lets the route answer 409 with the
decision it already has.  A timeout is NOT a refusal: the caller must be
able to tell ``timeout`` from ``denied``, so both are distinct return
values here and must stay distinct in the ToolResult built by the gate.
"""

from __future__ import annotations

import os
import threading
import time
import uuid
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

APPROVED = "approved"
DENIED = "denied"
TIMEOUT = "timeout"

# Decisions a caller may hand to resolve().  TIMEOUT is set internally only.
RESOLVABLE = (APPROVED, DENIED)
_VALID_DECISIONS = (APPROVED, DENIED, TIMEOUT)

_DEFAULT_TTL = 120.0
TTL_ENV_VAR = "OPENJARVIS_CONFIRM_TTL"

_LOCK = threading.Lock()
_PENDING: Dict[str, "_Pending"] = {}


def default_ttl() -> float:
    """TTL in seconds.  Env var first - config.toml is machine-regenerated
    and can silently revert, so it is deliberately not consulted here."""
    raw = os.environ.get(TTL_ENV_VAR)
    if not raw:
        return _DEFAULT_TTL
    try:
        value = float(raw)
    except (TypeError, ValueError):
        return _DEFAULT_TTL
    return value if value > 0 else _DEFAULT_TTL


@dataclass
class _Pending:
    confirm_id: str
    tool: str
    agent_id: str
    turn_id: str
    created_at: float
    expires_at: float
    event: threading.Event = field(default_factory=threading.Event)
    decision: Optional[str] = None


def _snapshot(pending: "_Pending") -> Dict[str, Any]:
    return {
        "confirm_id": pending.confirm_id,
        "tool": pending.tool,
        "agent_id": pending.agent_id,
        "turn_id": pending.turn_id,
        "created_at": pending.created_at,
        "expires_at": pending.expires_at,
        "decision": pending.decision,
        "state": "resolved" if pending.decision is not None else "pending",
    }


def _reap_locked(now: float) -> List[str]:
    """Drop expired entries.  Caller must hold _LOCK."""
    dead = [cid for cid, p in _PENDING.items() if p.expires_at <= now]
    for cid in dead:
        pending = _PENDING.pop(cid)
        if pending.decision is None:
            pending.decision = TIMEOUT
        pending.event.set()
    return dead


def register(
    tool: str,
    agent_id: str = "",
    turn_id: str = "",
    ttl: Optional[float] = None,
) -> str:
    """Create a pending confirmation and return its correlation id."""
    ttl_value = default_ttl() if ttl is None else float(ttl)
    now = time.time()
    confirm_id = uuid.uuid4().hex
    with _LOCK:
        _reap_locked(now)
        _PENDING[confirm_id] = _Pending(
            confirm_id=confirm_id,
            tool=tool,
            agent_id=agent_id,
            turn_id=turn_id,
            created_at=now,
            expires_at=now + ttl_value,
        )
    return confirm_id


def wait(confirm_id: str, timeout: Optional[float] = None) -> str:
    """Block until resolved or expired.  Returns approved|denied|timeout.

    An unknown id returns ``timeout`` - the gate must fail closed, and a
    prompt lost to the lossy ws put_nowait is indistinguishable from a
    user who never looked.  Both land here.
    """
    with _LOCK:
        pending = _PENDING.get(confirm_id)
        if pending is None:
            return TIMEOUT
        if pending.decision is not None:
            return pending.decision
        budget = pending.expires_at - time.time()

    if timeout is not None:
        budget = min(budget, float(timeout))
    if budget > 0:
        pending.event.wait(budget)

    with _LOCK:
        current = _PENDING.get(confirm_id)
        if current is not None:
            if current.decision is None:
                current.decision = TIMEOUT
                current.event.set()
            return current.decision
    # Reaped while we waited; the reaper stamped the decision on our copy.
    return pending.decision or TIMEOUT


def resolve(confirm_id: str, decision: str) -> bool:
    """Record a human decision.  False if unknown, expired, or already set."""
    if decision not in RESOLVABLE:
        raise ValueError(
            "decision must be one of %s, got %r" % (list(RESOLVABLE), decision)
        )
    with _LOCK:
        pending = _PENDING.get(confirm_id)
        if pending is None or pending.decision is not None:
            return False
        if pending.expires_at <= time.time():
            pending.decision = TIMEOUT
            pending.event.set()
            return False
        pending.decision = decision
        pending.event.set()
        return True


def get(confirm_id: str) -> Optional[Dict[str, Any]]:
    """Read-only view for the route layer.  None means 404."""
    with _LOCK:
        pending = _PENDING.get(confirm_id)
        return _snapshot(pending) if pending is not None else None


def reap() -> List[str]:
    """Public wrapper - returns the ids dropped."""
    with _LOCK:
        return _reap_locked(time.time())


def pending_count() -> int:
    with _LOCK:
        return len(_PENDING)


def clear() -> None:
    """Test hook.  Wakes every waiter as a timeout before dropping them."""
    with _LOCK:
        for pending in _PENDING.values():
            if pending.decision is None:
                pending.decision = TIMEOUT
            pending.event.set()
        _PENDING.clear()