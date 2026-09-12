import { useCallback, useEffect, useRef, useState } from 'react';
import { ShieldAlert } from 'lucide-react';
import { useAgentEvents, type AgentEvent } from '../../lib/useAgentEvents';
import { confirmTool } from '../../lib/api';

// openjarvis-confirm-ui-v1 - Defect 6 / 6e browser half
//
// Mounts the UNFILTERED agent-event socket (subscribeAll = true, no agent_id
// query param) because confirmation events carry the executor's CLASS identity
// in data.agent_id, which can never match a managed-agent INSTANCE id. The
// server-side filter short-circuits on a falsy _agent_filter at
// ws_bridge.py:56-59.
//
// Frame shapes read live from tools/_stubs.py on 2026-09-12:
//   tool_confirm_request.data  = confirm_id, agent_id, turn_id, tool,
//                                args_digest, prompt, expires_at
//   tool_confirm_resolved.data = confirm_id, agent_id, turn_id, tool,
//                                decision, state, created_at, expires_at,
//                                reaped
//
// The request frame is published BEFORE the executor blocks on the callback
// (_stubs.py:362-374, callback at :377), so the full expiry window is
// available to answer in. The resolved frame fires on EVERY outcome including
// TIMEOUT (:382-384), so dismiss-on-resolved covers expiry with no local timer.

const CONFIRM_EVENTS = ['tool_confirm_request', 'tool_confirm_resolved'] as const;

interface PendingConfirm {
  confirmId: string;
  tool: string;
  prompt: string;
  argsDigest: string;
  turnId: string;
  expiresAtMs: number | null;
}

function asString(v: unknown): string {
  return typeof v === 'string' ? v : '';
}

// expires_at comes straight off the registry entry. Its unit is UNVERIFIED as
// of W51 - treat anything below 1e12 as epoch SECONDS and scale it. If the
// countdown ever reads wrong, this is the line to check first.
function normalizeExpiry(v: unknown): number | null {
  if (typeof v !== 'number' || !isFinite(v) || v <= 0) return null;
  return v < 1e12 ? v * 1000 : v;
}

export function ConfirmPrompt() {
  const [queue, setQueue] = useState<PendingConfirm[]>([]);
  const [busy, setBusy] = useState(false);
  const [notice, setNotice] = useState<string | null>(null);
  const [now, setNow] = useState<number>(() => Date.now());
  const seenRef = useRef<Set<string>>(new Set());

  const onEvent = useCallback((event: AgentEvent) => {
    const data = (event.data || {}) as Record<string, unknown>;
    const confirmId = asString(data.confirm_id);

    if (!confirmId) {
      // A confirm frame with no confirm_id means the server stripped it:
      // ws_bridge.py:62-73 redacts unless app.state.bind_is_loopback is true.
      // Nothing actionable can be rendered from a redacted frame.
      console.warn('[confirm-ui] confirm frame arrived with no confirm_id (redacted?)', event.type);
      return;
    }

    if (event.type === 'tool_confirm_request') {
      if (seenRef.current.has(confirmId)) return;
      seenRef.current.add(confirmId);
      setQueue((prev) => {
        if (prev.some((p) => p.confirmId === confirmId)) return prev;
        return [
          ...prev,
          {
            confirmId,
            tool: asString(data.tool) || 'unknown tool',
            prompt: asString(data.prompt),
            argsDigest: asString(data.args_digest),
            turnId: asString(data.turn_id),
            expiresAtMs: normalizeExpiry(data.expires_at),
          },
        ];
      });
      return;
    }

    // tool_confirm_resolved - the authoritative dismissal for any outcome,
    // including a TIMEOUT we never answered and a decision made elsewhere.
    setQueue((prev) => prev.filter((p) => p.confirmId !== confirmId));
    const decision = asString(data.decision);
    if (decision === 'timeout') {
      setNotice('The confirmation request expired before it was answered.');
    }
  }, []);

  useAgentEvents(undefined, onEvent, CONFIRM_EVENTS, true);

  const active = queue[0];

  // Countdown ticks only while something is pending.
  useEffect(() => {
    if (!active) return;
    setNow(Date.now());
    const t = setInterval(() => setNow(Date.now()), 1000);
    return () => clearInterval(t);
  }, [active]);

  // Clear a stale notice once a new request lands.
  useEffect(() => {
    if (active) setNotice(null);
  }, [active]);

  const answer = useCallback(
    async (decision: 'approve' | 'deny') => {
      if (!active || busy) return;
      const confirmId = active.confirmId;
      setBusy(true);
      setNotice(null);
      try {
        const res = await confirmTool(confirmId, decision);
        if (res.ok) {
          // The resolved frame will also clear this; clearing locally keeps the
          // button from sitting dead if the socket is mid-reconnect.
          setQueue((prev) => prev.filter((p) => p.confirmId !== confirmId));
        } else if (res.status === 404) {
          setQueue((prev) => prev.filter((p) => p.confirmId !== confirmId));
          setNotice('That request already expired. The tool did not run.');
        } else if (res.status === 409) {
          const held = asString((res.body as Record<string, unknown>).decision);
          setQueue((prev) => prev.filter((p) => p.confirmId !== confirmId));
          setNotice('Already answered' + (held ? ' (' + held + ')' : '') + '.');
        } else {
          const err = asString((res.body as Record<string, unknown>).error);
          setNotice('Could not send the answer: ' + (err || 'HTTP ' + res.status));
        }
      } catch (e) {
        setNotice('Could not reach the server: ' + String(e));
      } finally {
        setBusy(false);
      }
    },
    [active, busy],
  );

  if (!active && !notice) return null;

  const secondsLeft =
    active && active.expiresAtMs
      ? Math.max(0, Math.round((active.expiresAtMs - now) / 1000))
      : null;

  return (
    <div
      style={{
        position: 'fixed',
        bottom: 96,
        left: '50%',
        transform: 'translateX(-50%)',
        zIndex: 999999,
        width: 'min(560px, calc(100vw - 32px))',
      }}
    >
      <div
        className="rounded-lg px-4 py-3 text-sm"
        style={{
          background: 'var(--color-bg-secondary)',
          border: '1px solid var(--color-accent)',
          boxShadow: '0 8px 24px rgba(0,0,0,0.35)',
        }}
      >
        {active ? (
          <>
            <div className="flex items-center gap-2 mb-2">
              <ShieldAlert size={16} style={{ color: 'var(--color-accent)', flexShrink: 0 }} />
              <span className="font-medium" style={{ color: 'var(--color-text)' }}>
                Confirmation required
              </span>
              {secondsLeft !== null && (
                <span className="text-xs ml-auto" style={{ color: 'var(--color-text-tertiary)' }}>
                  {secondsLeft}s left
                </span>
              )}
            </div>

            <p className="mb-2" style={{ color: 'var(--color-text-secondary)' }}>
              {active.prompt || 'Allow execution of tool ' + active.tool + '?'}
            </p>

            <div className="text-xs mb-3" style={{ color: 'var(--color-text-tertiary)' }}>
              <div>tool: {active.tool}</div>
              {active.argsDigest && <div className="break-all">args: {active.argsDigest}</div>}
              {active.turnId && <div>turn: {active.turnId}</div>}
            </div>

            <div className="flex items-center gap-2">
              <button
                onClick={() => answer('approve')}
                disabled={busy}
                className="px-3 py-1.5 rounded text-xs font-medium cursor-pointer"
                style={{
                  background: 'var(--color-accent)',
                  color: 'var(--color-on-accent)',
                  border: 'none',
                  opacity: busy ? 0.6 : 1,
                }}
              >
                Approve
              </button>
              <button
                onClick={() => answer('deny')}
                disabled={busy}
                className="px-3 py-1.5 rounded text-xs font-medium cursor-pointer"
                style={{
                  background: 'transparent',
                  color: 'var(--color-text-secondary)',
                  border: '1px solid var(--color-border)',
                  opacity: busy ? 0.6 : 1,
                }}
              >
                Deny
              </button>
              {queue.length > 1 && (
                <span className="text-xs ml-auto" style={{ color: 'var(--color-text-tertiary)' }}>
                  +{queue.length - 1} waiting
                </span>
              )}
            </div>
          </>
        ) : (
          <div className="flex items-center gap-2">
            <span style={{ color: 'var(--color-text-secondary)' }}>{notice}</span>
            <button
              onClick={() => setNotice(null)}
              className="ml-auto px-2 py-1 rounded text-xs cursor-pointer"
              style={{
                background: 'transparent',
                color: 'var(--color-text-tertiary)',
                border: '1px solid var(--color-border)',
              }}
            >
              Dismiss
            </button>
          </div>
        )}

        {active && notice && (
          <div className="text-xs mt-2" style={{ color: 'var(--color-text-tertiary)' }}>
            {notice}
          </div>
        )}
      </div>
    </div>
  );
}
