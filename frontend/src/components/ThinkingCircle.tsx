import { useEffect, useRef } from 'react';
type ThinkingState = 'idle' | 'thinking' | 'speaking';
interface ThinkingCircleProps {
  state: ThinkingState;
  size?: number;
}
export function ThinkingCircle({ state, size = 90 }: ThinkingCircleProps) {
  const rotRef = useRef<SVGGElement>(null);
  const rot2Ref = useRef<SVGGElement>(null);
  const angleRef = useRef(0);
  const angle2Ref = useRef(0);
  const rafRef = useRef<number>(0);
  useEffect(() => {
    const speed = state === 'thinking' ? 2.2 : state === 'speaking' ? 3.5 : 0.3;
    const speed2 = -speed * 0.6;
    const animate = () => {
      angleRef.current = (angleRef.current + speed) % 360;
      angle2Ref.current = (angle2Ref.current + speed2 + 360) % 360;
      if (rotRef.current) rotRef.current.setAttribute('transform', `rotate(${angleRef.current} ${size/2} ${size/2})`);
      if (rot2Ref.current) rot2Ref.current.setAttribute('transform', `rotate(${angle2Ref.current} ${size/2} ${size/2})`);
      rafRef.current = requestAnimationFrame(animate);
    };
    rafRef.current = requestAnimationFrame(animate);
    return () => cancelAnimationFrame(rafRef.current);
  }, [state, size]);
  const cx = size / 2;
  const cy = size / 2;
  const accent = state === 'idle' ? 'rgba(100,160,255,0.35)' : state === 'thinking' ? 'rgba(0,220,255,0.9)' : 'rgba(0,255,200,1)';
  const glow = state === 'idle' ? 'none' : `drop-shadow(0 0 6px ${accent})`;
  const r1 = size * 0.42;
  const r2 = size * 0.32;
  const r3 = size * 0.20;
  return (
    <div style={{ width: size, height: size, pointerEvents: 'none', filter: glow }}>
      <svg width={size} height={size} viewBox={`0 0 ${size} ${size}`}>
        <circle cx={cx} cy={cy} r={r1} fill="none" stroke={accent} strokeWidth="1.5" opacity={0.5} strokeDasharray="4 6" />
        <g ref={rotRef}>
          <circle cx={cx} cy={cy} r={r2} fill="none" stroke={accent} strokeWidth="2" opacity={0.8} strokeDasharray={`${r2 * 0.8} ${r2 * 0.4}`} />
          {[0, 72, 144, 216, 288].map((a, i) => {
            const rad = (a * Math.PI) / 180;
            return <circle key={i} cx={cx + r2 * Math.cos(rad)} cy={cy + r2 * Math.sin(rad)} r={size * 0.04} fill={accent} opacity={0.9} />;
          })}
        </g>
        <g ref={rot2Ref}>
          <circle cx={cx} cy={cy} r={r3} fill="none" stroke={accent} strokeWidth="1.5" opacity={0.7} strokeDasharray={`${r3 * 1.2} ${r3 * 0.5}`} />
        </g>
        <circle cx={cx} cy={cy} r={size * 0.09} fill={accent} opacity={state === 'idle' ? 0.3 : 0.9} />
        <circle cx={cx} cy={cy} r={size * 0.05} fill="white" opacity={state === 'idle' ? 0.2 : 0.95} />
        {[0, 90, 180, 270].map((a, i) => {
          const rad = (a * Math.PI) / 180;
          const x1 = cx + (r1 - 4) * Math.cos(rad);
          const y1 = cy + (r1 - 4) * Math.sin(rad);
          const x2 = cx + (r1 + 4) * Math.cos(rad);
          const y2 = cy + (r1 + 4) * Math.sin(rad);
          return <line key={i} x1={x1} y1={y1} x2={x2} y2={y2} stroke={accent} strokeWidth="2" opacity={0.8} />;
        })}
      </svg>
    </div>
  );
}
