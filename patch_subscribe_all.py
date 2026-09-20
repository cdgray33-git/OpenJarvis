"""openjarvis-agent-events-subscribeall-v1

Barriers 1 and 2 of 6e, in one edit.

Barrier 1: the guard at `if (!agentId) return;` aborts the effect before
connect() runs, so no client can ever subscribe without an agentId.

Barrier 2: buildWsUrl ALREADY returns a bare /v1/agents/events URL with no
agent_id query parameter when agentId is falsy. That branch is dead code today
because of the barrier 1 guard. A bare URL leaves _agent_filter falsy on the
server, which short-circuits the filter at ws_bridge.py:56-59 and lets
TOOL_CONFIRM_REQUEST frames through.

This patch adds a fourth optional parameter, subscribeAll. The guard becomes a
test of both, so the existing three-argument call sites in AgentsPage.tsx keep
byte-identical behavior and the dead branch becomes reachable on opt-in.

A sentinel value in the agentId slot was rejected: it would flow into
encodeURIComponent and into the dependency array, overloading one variable with
two meanings.

Anchors on content, never on line numbers. Idempotent. Writes a .bak first.
"""

from __future__ import annotations

import shutil
import sys
from pathlib import Path

TARGET = Path("frontend/src/lib/useAgentEvents.ts")
BACKUP = Path("frontend/src/lib/useAgentEvents.ts.bak-subscribeall")
MARKER = "openjarvis-agent-events-subscribeall-v1"

# --- edit 1: signature ---------------------------------------------------
SIG_OLD = """export function useAgentEvents(
  agentId: string | undefined,
  onEvent: (event: AgentEvent) => void,
  eventTypes?: readonly string[],
): void {"""

SIG_NEW = """export function useAgentEvents(
  agentId: string | undefined,
  onEvent: (event: AgentEvent) => void,
  eventTypes?: readonly string[],
  // openjarvis-agent-events-subscribeall-v1
  // Opt in to the unfiltered stream. When true, the socket connects with NO
  // agent_id query parameter, leaving _agent_filter falsy on the server so the
  // filter at ws_bridge.py:56-59 short-circuits. Required for the chat path,
  // where confirmation events carry a CLASS identity (native_openhands) that
  // can never match a managed-agent INSTANCE id.
  subscribeAll = false,
): void {"""

# --- edit 2: the guard ---------------------------------------------------
GUARD_OLD = """    if (!agentId) return;"""

GUARD_NEW = """    if (!agentId && !subscribeAll) return;"""

# --- edit 3: dependency array -------------------------------------------
DEPS_OLD = """  }, [agentId]);"""

DEPS_NEW = """  }, [agentId, subscribeAll]);"""

# --- edit 4: url construction -------------------------------------------
# buildWsUrl already handles the falsy case correctly. The call site passes
# agentId directly, which is exactly right: on an opt-in subscription agentId
# is undefined, so the bare-URL branch is taken. No change needed there.

EDITS = [
    ("signature", SIG_OLD, SIG_NEW),
    ("guard", GUARD_OLD, GUARD_NEW),
    ("deps", DEPS_OLD, DEPS_NEW),
]


def main() -> int:
    if not TARGET.exists():
        print(f"FAIL: {TARGET} not found. Run from the repo root.")
        return 1

    src = TARGET.read_text(encoding="utf-8")

    if MARKER in src:
        print(f"ALREADY APPLIED: marker {MARKER} present. No change made.")
        return 0

    # Verify every anchor matches exactly once BEFORE writing anything.
    for name, old, _new in EDITS:
        n = src.count(old)
        if n != 1:
            print(f"FAIL: anchor '{name}' matched {n} times, expected exactly 1.")
            print("NO CHANGE MADE. Anchor was:")
            print(old)
            return 1

    patched = src
    for name, old, new in EDITS:
        patched = patched.replace(old, new, 1)
        print(f"  applied: {name}")

    shutil.copy2(TARGET, BACKUP)
    TARGET.write_text(patched, encoding="utf-8")

    print(f"BACKUP WRITTEN: {BACKUP}")
    print(f"PATCH APPLIED: {TARGET}")
    print(f"lines before={len(src.splitlines())} after={len(patched.splitlines())}")
    print("EXPECTED DELTA: +7 lines")
    return 0


if __name__ == "__main__":
    sys.exit(main())
