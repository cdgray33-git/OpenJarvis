import { useRef, useEffect, useState, useCallback } from 'react';
import { useNavigate } from 'react-router';
import { MessageBubble } from './MessageBubble';
import { InputArea } from './InputArea';
import { StreamingDots } from './StreamingDots';
import { useAppStore } from '../../lib/store';
import { ThinkingCircle } from '../ThinkingCircle';
import { Sparkles, PanelRightOpen, PanelRightClose, Database, MessageSquare, X, Volume2, VolumeX } from 'lucide-react';
import { listConnectors } from '../../lib/connectors-api';
import { synthesizeSpeech } from '../../lib/api';

function getGreeting(): string {
  const hour = new Date().getHours();
  if (hour < 12) return 'Good morning';
  if (hour < 18) return 'Good afternoon';
  return 'Good evening';
}

const MUTE_KEY = 'openjarvis_tts_muted';

export function ChatArea() {
  const messages = useAppStore((s) => s.messages);
  const streamState = useAppStore((s) => s.streamState);
  const systemPanelOpen = useAppStore((s) => s.systemPanelOpen);
  const toggleSystemPanel = useAppStore((s) => s.toggleSystemPanel);
  const navigate = useNavigate();
  const listRef = useRef<HTMLDivElement>(null);
  const shouldAutoScroll = useRef(true);
  const audioRef = useRef<HTMLAudioElement | null>(null);
  const lastSpokenIdRef = useRef<string | null>(null);

  const [hasConnectedSources, setHasConnectedSources] = useState<boolean | null>(null);
  const [bannerDismissed, setBannerDismissed] = useState(false);
  const [muted, setMuted] = useState<boolean>(() => {
    try { return localStorage.getItem(MUTE_KEY) === 'true'; } catch { return false; }
  });

  useEffect(() => {
    listConnectors()
      .then((list) => setHasConnectedSources(list.some((c) => c.connected)))
      .catch(() => setHasConnectedSources(null));
  }, []);

  useEffect(() => {
    if (shouldAutoScroll.current && listRef.current) {
      listRef.current.scrollTop = listRef.current.scrollHeight;
    }
  }, [messages, streamState.content]);

  const handleScroll = () => {
    if (!listRef.current) return;
    const { scrollTop, scrollHeight, clientHeight } = listRef.current;
    shouldAutoScroll.current = scrollHeight - scrollTop - clientHeight < 100;
  };

  const toggleMute = useCallback(() => {
    setMuted((prev) => {
      const next = !prev;
      try { localStorage.setItem(MUTE_KEY, String(next)); } catch {}
      if (next && audioRef.current) {
        audioRef.current.pause();
        audioRef.current = null;
      }
      return next;
    });
  }, []);

  // Auto-speak the last assistant message when streaming finishes
  useEffect(() => {
    if (streamState.isStreaming || muted) return;
    const lastMsg = messages[messages.length - 1];
    if (!lastMsg || lastMsg.role !== 'assistant') return;
    if (lastMsg.id === lastSpokenIdRef.current) return;
    if (!lastMsg.content || lastMsg.content.trim().length === 0) return;

    lastSpokenIdRef.current = lastMsg.id;

    // Stop any currently playing audio
    if (audioRef.current) {
      audioRef.current.pause();
      audioRef.current = null;
    }

    // Strip markdown for cleaner TTS
    const plainText = lastMsg.content
      .replace(/```[\s\S]*?```/g, 'code block.')
      .replace(/`[^`]+`/g, '')
      .replace(/[#*_~>]/g, '')
      .replace(/\[([^\]]+)\]\([^)]+\)/g, '$1')
      .trim();

    if (!plainText) return;

    synthesizeSpeech(plainText)
      .then((blob) => {
        const url = URL.createObjectURL(blob);
        const audio = new Audio(url);
        audioRef.current = audio;
        audio.play().catch(() => {});
        audio.onended = () => URL.revokeObjectURL(url);
      })
      .catch(() => {});
  }, [streamState.isStreaming, messages, muted]);

  const isEmpty = messages.length === 0 && !streamState.isStreaming;
  const PanelIcon = systemPanelOpen ? PanelRightClose : PanelRightOpen;

  return (
    <div className="flex flex-col h-full">
      <div className="flex items-center justify-end px-3 py-1.5 shrink-0 gap-1">
        {/* Mute toggle */}
        <button
          onClick={toggleMute}
          className="p-1.5 rounded-md transition-colors cursor-pointer"
          style={{ color: muted ? 'var(--color-text-tertiary)' : 'var(--color-accent)' }}
          title={muted ? 'Unmute Jarvis voice' : 'Mute Jarvis voice'}
        >
          {muted ? <VolumeX size={16} /> : <Volume2 size={16} />}
        </button>
        <button
          onClick={toggleSystemPanel}
          className="p-1.5 rounded-md transition-colors cursor-pointer"
          style={{ color: 'var(--color-text-tertiary)' }}
          title={`${systemPanelOpen ? 'Hide' : 'Show'} system panel (${navigator.platform.includes('Mac') ? '?' : 'Ctrl'}+I)`}
        >
          <PanelIcon size={16} />
        </button>
      </div>

      {hasConnectedSources === false && !bannerDismissed && (
        <div
          className="mx-4 mb-2 flex items-center gap-3 px-4 py-3 rounded-lg text-sm shrink-0"
          style={{
            background: 'var(--color-accent-subtle)',
            border: '1px solid var(--color-border)',
          }}
        >
          <Database size={16} style={{ color: 'var(--color-accent)', flexShrink: 0 }} />
          <span style={{ color: 'var(--color-text-secondary)', flex: 1 }}>
            Connect your data sources (Gmail, iMessage, Slack, etc.) to get personalized answers.
          </span>
          <button
            onClick={() => navigate('/data-sources')}
            className="px-3 py-1 rounded text-xs font-medium cursor-pointer"
            style={{ background: 'var(--color-accent)', color: 'var(--color-on-accent)', border: 'none' }}
          >
            Connect
          </button>
          <button
            onClick={() => setBannerDismissed(true)}
            className="p-1 rounded cursor-pointer"
            style={{ color: 'var(--color-text-tertiary)', background: 'transparent', border: 'none' }}
          >
            <X size={14} />
          </button>
        </div>
      )}

      <div
        ref={listRef}
        onScroll={handleScroll}
        className="flex-1 overflow-y-auto"
        style={{ paddingBottom: '0.5rem' }}
      >
        {isEmpty ? (
          <div className="flex flex-col items-center justify-center h-full px-4">
            <div
              className="w-12 h-12 rounded-2xl flex items-center justify-center mb-4"
              style={{ background: 'var(--color-accent-subtle)', color: 'var(--color-accent)' }}
            >
              <Sparkles size={24} />
            </div>
            <h2 className="text-xl font-semibold mb-2" style={{ color: 'var(--color-text)' }}>
              {getGreeting()}
            </h2>
            <p className="text-sm text-center max-w-sm mb-6" style={{ color: 'var(--color-text-secondary)' }}>
              Ask anything. Your AI runs locally — private, fast, and always available.
            </p>

            <div className="flex gap-3">
              <button
                onClick={() => navigate('/data-sources')}
                className="flex items-center gap-2 px-4 py-2.5 rounded-lg text-xs cursor-pointer transition-colors"
                style={{
                  background: 'var(--color-bg-secondary)',
                  border: '1px solid var(--color-border)',
                  color: 'var(--color-text-secondary)',
                }}
                onMouseEnter={(e) => (e.currentTarget.style.borderColor = 'var(--color-accent)')}
                onMouseLeave={(e) => (e.currentTarget.style.borderColor = 'var(--color-border)')}
              >
                <Database size={14} style={{ color: 'var(--color-accent)' }} />
                Connect Data Sources
              </button>
              <button
                onClick={() => { navigate('/data-sources'); setTimeout(() => window.dispatchEvent(new CustomEvent('switch-tab', { detail: 'messaging' })), 100); }}
                className="flex items-center gap-2 px-4 py-2.5 rounded-lg text-xs cursor-pointer transition-colors"
                style={{
                  background: 'var(--color-bg-secondary)',
                  border: '1px solid var(--color-border)',
                  color: 'var(--color-text-secondary)',
                }}
                onMouseEnter={(e) => (e.currentTarget.style.borderColor = 'var(--color-accent)')}
                onMouseLeave={(e) => (e.currentTarget.style.borderColor = 'var(--color-border)')}
              >
                <MessageSquare size={14} style={{ color: 'var(--color-accent)' }} />
                Set Up Messaging Channels
              </button>
            </div>
          </div>
        ) : (
          <div className="max-w-[var(--chat-max-width)] mx-auto px-4 py-4 pb-2">
            {messages.map((msg) => (
              <MessageBubble key={msg.id} message={msg} />
            ))}
            {streamState.isStreaming && streamState.content === '' && (
              <div className="flex justify-start mb-4">
                <StreamingDots phase={streamState.phase} />
              </div>
            )}
          </div>
        )}
      </div>

      {/* ThinkingCircle component */}
      <div style={{ position: 'fixed', top: 120, right: 20, zIndex: 999998 }}>
        <ThinkingCircle
          isLoading={streamState.isStreaming}
          phase={streamState.isStreaming ? "processing..." : undefined}
          variant="cyan"
        />
      </div>

      <div style={{ paddingBottom: '0.75rem' }}>
        <InputArea />
      </div>
    </div>
  );
}
