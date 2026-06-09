import React from 'react';

interface Props {
  isLoading: boolean;
  phase?: string;
  variant?: 'cyan' | 'purple' | 'green' | 'red';
}

const COLORS = {
  cyan:   { glow: 'rgb(0, 231, 255)',   border: '#22d3ee' },
  purple: { glow: 'rgb(168, 85, 247)',  border: '#a855f7' },
  green:  { glow: 'rgb(52, 211, 153)',  border: '#34d399' },
  red:    { glow: 'rgb(239, 68, 68)',   border: '#ef4444' },
};

export function ThinkingCircle({ isLoading, phase, variant = 'cyan' }: Props) {
  if (!isLoading) return null;
  const c = COLORS[variant];
  return (
    <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 12, padding: '16px 0' }}>
      <div style={{ position: 'relative', width: 120, height: 120 }}>
        {/* Core */}
        <div style={{
          position: 'absolute', top: '50%', left: '50%',
          transform: 'translate(-50%, -50%)',
          width: 20, height: 20, borderRadius: '50%',
          background: `radial-gradient(circle, white, ${c.border})`,
          boxShadow: `0 0 15px ${c.glow}, 0 0 30px ${c.glow}`,
          animation: 'jarvis-pulse 2s ease-in-out infinite',
        }} />
        {/* Inner dashed ring */}
        <div style={{
          position: 'absolute', top: '50%', left: '50%',
          transform: 'translate(-50%, -50%)',
          width: 70, height: 70, borderRadius: '50%',
          border: `2px dashed ${c.border}`,
          opacity: 0.7,
          filter: `drop-shadow(0 0 4px ${c.glow})`,
          animation: 'jarvis-spin-cw 3s linear infinite',
        }} />
        {/* Outer ring */}
        <div style={{
          position: 'absolute', top: '50%', left: '50%',
          transform: 'translate(-50%, -50%)',
          width: 100, height: 100, borderRadius: '50%',
          border: `2px solid transparent`,
          borderTop: `3px solid ${c.border}`,
          borderBottom: `3px solid ${c.border}`,
          filter: `drop-shadow(0 0 6px ${c.glow})`,
          animation: 'jarvis-spin-ccw 4s linear infinite',
        }} />
        {/* Scanner */}
        <div style={{
          position: 'absolute', top: '50%', left: '50%',
          transform: 'translate(-50%, -50%)',
          width: 110, height: 110, borderRadius: '50%',
          border: `1px solid ${c.border}22`,
          borderLeft: `2px solid ${c.border}`,
          animation: 'jarvis-spin-cw 1.5s linear infinite',
        }} />
      </div>
      {phase && (
        <span style={{
          fontSize: 11, fontFamily: 'monospace',
          letterSpacing: '0.1em', color: c.border,
          animation: 'pulse 2s ease-in-out infinite',
        }}>{phase}</span>
      )}
    </div>
  );
}
