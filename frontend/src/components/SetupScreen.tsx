import { useState, useEffect, useCallback } from 'react';
import { Loader2, CheckCircle2, XCircle, Server } from 'lucide-react';
import { getSetupStatus, type SetupStatus } from '../lib/api';

const STEPS = [
  { key: 'server_ready', label: 'API Server', icon: Server, detail: 'Starting server...' },
] as const;

type StepKey = (typeof STEPS)[number]['key'];

function StepRow({
  icon: Icon,
  label,
  done,
  active,
  detail,
}: {
  icon: typeof Server;
  label: string;
  done: boolean;
  active: boolean;
  detail: string;
}) {
  return (
    <div className="flex items-center gap-3 py-3">
      <div className="flex-shrink-0">
        {done ? (
          <CheckCircle2 size={20} style={{ color: 'var(--color-success)' }} />
        ) : active ? (
          <Loader2 size={20} className="animate-spin" style={{ color: 'var(--color-accent)' }} />
        ) : (
          <div
            className="w-5 h-5 rounded-full border-2"
            style={{ borderColor: 'var(--color-border)' }}
          />
        )}
      </div>
      <div className="flex-1">
        <div className="flex items-center gap-2">
          <Icon size={16} style={{ color: 'var(--color-text-secondary)' }} />
          <span className="text-sm font-medium" style={{ color: 'var(--color-text)' }}>
            {label}
          </span>
        </div>
        {active && (
          <div className="text-xs mt-0.5" style={{ color: 'var(--color-text-tertiary)' }}>
            {detail}
          </div>
        )}
      </div>
    </div>
  );
}

export function SetupScreen({ onReady }: { onReady: () => void }) {
  const [status, setStatus] = useState<SetupStatus | null>(null);

  const poll = useCallback(async () => {
    const s = await getSetupStatus();
    if (s) setStatus(s);
    if (s?.phase === 'ready') {
      setTimeout(() => onReady(), 600);
    }
  }, [onReady]);

  useEffect(() => {
    poll();
    const interval = setInterval(poll, 800);
    return () => clearInterval(interval);
  }, [poll]);

  const activeStep: StepKey | null =
    status && !status.server_ready ? 'server_ready' : null;

  return (
    <div
      className="fixed inset-0 flex items-center justify-center"
      style={{ background: 'var(--color-bg)' }}
    >
      <div className="w-full max-w-md px-6">
        <div className="text-center mb-10">
          <div
            className="w-16 h-16 rounded-2xl flex items-center justify-center mx-auto mb-4"
            style={{
              background: 'var(--color-accent-subtle)',
              color: 'var(--color-accent)',
            }}
          >
            <Server size={32} />
          </div>
          <h1 className="text-xl font-semibold mb-2" style={{ color: 'var(--color-text)' }}>
            OpenJarvis
          </h1>
          <p className="text-sm" style={{ color: 'var(--color-text-secondary)' }}>
            Connecting to backend...
          </p>
        </div>

        {STEPS.map((step) => (
          <StepRow
            key={step.key}
            icon={step.icon}
            label={step.label}
            done={status?.[step.key] ?? false}
            active={activeStep === step.key}
            detail={
              activeStep === step.key && status?.detail ? status.detail : step.detail
            }
          />
        ))}

        {status?.error && (
          <div
            className="flex items-start gap-3 px-4 py-3 rounded-xl text-sm mt-4"
            style={{
              background: 'color-mix(in srgb, var(--color-error) 10%, transparent)',
              border: '1px solid color-mix(in srgb, var(--color-error) 20%, transparent)',
              color: 'var(--color-error)',
            }}
          >
            <XCircle size={16} className="flex-shrink-0 mt-0.5" />
            <span style={{ wordBreak: 'break-word', overflowWrap: 'anywhere' }}>
              {status.error}
            </span>
          </div>
        )}

        {!status?.error && (
          <div
            className="h-1 rounded-full overflow-hidden mt-6"
            style={{ background: 'var(--color-bg-tertiary)' }}
          >
            <div
              className="h-full rounded-full transition-all duration-500"
              style={{
                background: 'var(--color-accent)',
                width: `${(status?.server_ready ? 1 : 0) * 100}%`,
              }}
            />
          </div>
        )}
      </div>
    </div>
  );
}
