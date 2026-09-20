# patch_confirm_registry.ps1
# Defect 6 / Patch 6c step 1 - create src\openjarvis\core\confirm_registry.py
# Run from the OpenJarvis repo root:
#   powershell -ExecutionPolicy Bypass -File .\patch_confirm_registry.ps1
# Writes the module itself. Nothing to paste. Read-only to every other file.

$ErrorActionPreference = 'Stop'

$root = $PSScriptRoot
if ([string]::IsNullOrWhiteSpace($root)) { $root = (Get-Location).Path }
$coreDir = Join-Path $root 'src\openjarvis\core'
$target  = Join-Path $coreDir 'confirm_registry.py'

Write-Host "=== PATCH 6c STEP 1 - confirm_registry ===" -ForegroundColor Cyan
Write-Host "root   : $root"
Write-Host "target : $target"
Write-Host ""

if (-not (Test-Path $coreDir)) {
  Write-Host "ABORT: $coreDir not found. Put this script in the repo root." -ForegroundColor Red
} else {

$moduleText = @'
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
'@

$testText = @'
import sys
import threading
import time

import openjarvis.core.confirm_registry as cr

FAILS = []


def check(name, got, want):
    ok = got == want
    print("%-28s %-9s got=%r want=%r" % (name, "PASS" if ok else "FAIL", got, want))
    if not ok:
        FAILS.append(name)


def resolve_soon(cid, decision, delay=0.05):
    def _go():
        time.sleep(delay)
        cr.resolve(cid, decision)
    t = threading.Thread(target=_go, daemon=True)
    t.start()
    return t


cr.clear()

# 1 approve
cid = cr.register("shell_exec", agent_id="native_openhands", turn_id="t1", ttl=5)
resolve_soon(cid, cr.APPROVED)
check("approve", cr.wait(cid), "approved")

# 2 deny
cid = cr.register("git_commit", agent_id="native_openhands", turn_id="t2", ttl=5)
resolve_soon(cid, cr.DENIED)
check("deny", cr.wait(cid), "denied")

# 3 timeout - a timeout is NOT a refusal
cid = cr.register("agent_kill", agent_id="native_openhands", turn_id="t3", ttl=5)
t0 = time.time()
check("timeout", cr.wait(cid, timeout=0.2), "timeout")
check("timeout bounded", 0.15 < time.time() - t0 < 1.0, True)

# 4 write-once
cid = cr.register("shell_exec", turn_id="t4", ttl=5)
check("first resolve", cr.resolve(cid, cr.APPROVED), True)
check("second resolve", cr.resolve(cid, cr.DENIED), False)
check("decision not flipped", cr.get(cid)["decision"], "approved")
check("state resolved", cr.get(cid)["state"], "resolved")

# 5 unknown id
check("resolve unknown", cr.resolve("deadbeef", cr.APPROVED), False)
check("wait unknown", cr.wait("deadbeef"), "timeout")
check("get unknown", cr.get("deadbeef"), None)

# 6 ttl expiry reaps and stamps timeout
cid = cr.register("shell_exec", turn_id="t6", ttl=0.1)
time.sleep(0.2)
check("expired wait", cr.wait(cid), "timeout")
check("expired resolve", cr.resolve(cid, cr.APPROVED), False)

# 7 payload fields the emit needs
cid = cr.register("shell_exec", agent_id="native_openhands", turn_id="a8172e4c-t1", ttl=5)
snap = cr.get(cid)
check("agent_id carried", snap["agent_id"], "native_openhands")
check("turn_id carried", snap["turn_id"], "a8172e4c-t1")
check("state pending", snap["state"], "pending")

# 8 bad decision rejected
try:
    cr.resolve(cid, "maybe")
    check("bad decision", "no raise", "ValueError")
except ValueError:
    check("bad decision", "ValueError", "ValueError")

# 9 reap housekeeping
cr.clear()
check("clear empties", cr.pending_count(), 0)

# 10 default ttl
check("default ttl", cr.default_ttl(), 120.0)

print("")
if FAILS:
    print("SELFTEST FAILED: " + ", ".join(FAILS))
    sys.exit(1)
print("SELFTEST PASSED - all cases green")
sys.exit(0)
'@

  # ---- backup only if something is already there -------------------------
  $stamp = Get-Date -Format 'yyyyMMdd_HHmmss'
  $backup = $null
  if (Test-Path $target) {
    $backup = "$target.bak_defect6_confirmreg_$stamp"
    Copy-Item $target $backup -Force
    Write-Host "PRE-EXISTING FILE BACKED UP: $backup" -ForegroundColor Yellow
  } else {
    Write-Host "New file - no backup needed." -ForegroundColor Gray
  }

  # ---- write -------------------------------------------------------------
  [System.IO.File]::WriteAllText($target, $moduleText, (New-Object System.Text.UTF8Encoding($false)))
  Write-Host "WROTE $([System.IO.File]::ReadAllText($target).Length) chars" -ForegroundColor Green
  Write-Host ""

  # ---- verify the write --------------------------------------------------
  Write-Host "--- marker check ---"
  $body = [System.IO.File]::ReadAllText($target)
  $markers = @(
    'openjarvis-confirm-registry-v1',
    'def register(',
    'def wait(',
    'def resolve(',
    'threading.Event',
    'RESOLVABLE = (APPROVED, DENIED)'
  )
  $allOk = $true
  foreach ($m in $markers) {
    $hit = $body.Contains($m)
    if (-not $hit) { $allOk = $false }
    Write-Host ("  {0,-34} {1}" -f $m, $(if ($hit) { 'OK' } else { 'MISSING' }))
  }
  $negative = $body.Contains('asyncio.Event')
  Write-Host ("  {0,-34} {1}" -f 'asyncio.Event absent', $(if ($negative) { 'FAIL - present' } else { 'OK' }))
  if ($negative) { $allOk = $false }

  # encoding control: this module is pure ASCII, so bytes must equal chars
  $byteLen = ([System.IO.File]::ReadAllBytes($target)).Length
  $charLen = $body.Length
  Write-Host ("  {0,-34} bytes={1} chars={2} {3}" -f 'ascii/encoding control', $byteLen, $charLen, $(if ($byteLen -eq $charLen) { 'OK' } else { 'FAIL' }))
  if ($byteLen -ne $charLen) { $allOk = $false }
  Write-Host ""

  # ---- pick an interpreter ----------------------------------------------
  $py = Join-Path $root '.venv\Scripts\python.exe'
  if (-not (Test-Path $py)) { $py = 'python' }
  Write-Host "python : $py"
  Write-Host ""

  # ---- py_compile --------------------------------------------------------
  Write-Host "--- py_compile ---"
  & $py -m py_compile $target
  if ($LASTEXITCODE -eq 0) { Write-Host "  py_compile OK" -ForegroundColor Green }
  else { Write-Host "  py_compile FAILED" -ForegroundColor Red; $allOk = $false }
  Write-Host ""

  # ---- self-test in isolation -------------------------------------------
  Write-Host "--- self-test (registry in isolation, no backend involved) ---"
  $testFile = Join-Path $env:TEMP "confirmreg_selftest_$stamp.py"
  [System.IO.File]::WriteAllText($testFile, $testText, (New-Object System.Text.UTF8Encoding($false)))
  $env:PYTHONPATH = (Join-Path $root 'src')
  Push-Location $root
  & $py $testFile
  $testExit = $LASTEXITCODE
  Pop-Location
  Remove-Item $testFile -Force -ErrorAction SilentlyContinue
  if ($testExit -ne 0) { $allOk = $false }
  Write-Host ""

  # ---- verdict -----------------------------------------------------------
  if ($allOk) {
    Write-Host "=== 6c STEP 1 VERIFIED ===" -ForegroundColor Green
    Write-Host "Registry is correct in isolation. No live restart needed -"
    Write-Host "nothing imports it yet. Next step is the emit."
  } else {
    Write-Host "=== 6c STEP 1 FAILED - DO NOT BUILD ON THIS ===" -ForegroundColor Red
  }
  Write-Host ""
  Write-Host "--- ROLLBACK ---" -ForegroundColor Yellow
  if ($backup) {
    Write-Host "Copy-Item '$backup' '$target' -Force"
  } else {
    Write-Host "Remove-Item '$target' -Force"
    Write-Host "Remove-Item (Join-Path '$coreDir' '__pycache__\confirm_registry*.pyc') -Force -ErrorAction SilentlyContinue"
  }
}
