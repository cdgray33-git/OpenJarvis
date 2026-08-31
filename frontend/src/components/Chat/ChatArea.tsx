import { useRef, useEffect, useState, useCallback } from 'react';
import { useNavigate } from 'react-router';
import { MessageBubble } from './MessageBubble';
import { InputArea } from './InputArea';
import { StreamingDots } from './StreamingDots';
import { useAppStore, generateId } from '../../lib/store';
import { ThinkingCircle } from '../ThinkingCircle';
import { Sparkles, PanelRightOpen, PanelRightClose, Database, MessageSquare, X, Volume2, VolumeX, Paperclip } from 'lucide-react';
import { listConnectors } from '../../lib/connectors-api';
import { fetchSavings } from '../../lib/api';
import { enqueue, stopAll } from '../../audio/ttsPlayer';
import { streamChat } from '../../lib/sse';
import type { ChatMessage, ToolCallInfo, TokenUsage, MessageTelemetry } from '../../types';

function formatBytes(b: number): string {
  if (b < 1024) return b + ' B';
  if (b < 1048576) return (b / 1024).toFixed(1) + ' KB';
  return (b / 1048576).toFixed(1) + ' MB';
}

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
  const lastSpokenIdRef = useRef<string | null>(null);
  const hasMountedRef = useRef(false);
  const spokenCharsRef = useRef<number>(0);
  const sendAbortRef = useRef<AbortController | null>(null);
  const sendTimerRef = useRef<ReturnType<typeof setInterval> | null>(null);

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
      if (next) stopAll();
      return next;
    });
  }, []);

  // -------------------------------------------------------------------------
  // TTS driver. ONE owner for the whole reply.
  //
  // The previous code had two effects competing over shared refs. The
  // mid-stream effect claimed lastSpokenIdRef as soon as it spoke its first
  // sentence; the post-stream effect then returned early because that id was
  // already claimed. Whatever was still unspoken when streaming ended fell
  // between them. All playback state now lives in ttsPlayer, so this effect
  // decides only WHAT text to hand over and WHEN.
  //
  // While streaming, hand over text up to the last completed sentence. Once
  // streaming ends, hand over everything remaining regardless of punctuation.
  // That final flush is what guarantees the last sentence is spoken, and it
  // works whether the store lands the final text and resetStream() in one
  // render or in two.
  // -------------------------------------------------------------------------
  useEffect(() => {
    const lastMsg = messages[messages.length - 1];

    // On mount, adopt whatever is already on screen as already spoken, so a
    // restored conversation is never read aloud. This is what hasMountedRef
    // was always for: it was declared and read but never assigned anywhere,
    // so the guard below it never opened and mid-stream TTS never ran once.
    if (!hasMountedRef.current) {
      hasMountedRef.current = true;
      if (lastMsg && lastMsg.role === 'assistant' && lastMsg.id) {
        lastSpokenIdRef.current = lastMsg.id;
        spokenCharsRef.current = (lastMsg.content || '').length;
      }
      return;
    }

    if (!lastMsg || lastMsg.role !== 'assistant' || !lastMsg.id) return;

    // A new reply cancels anything still queued from the previous one.
    if (lastMsg.id !== lastSpokenIdRef.current) {
      lastSpokenIdRef.current = lastMsg.id;
      spokenCharsRef.current = 0;
      stopAll();
    }

    const fullText = lastMsg.content || '';
    let take = fullText.length;
    console.log('[TTSDBG] run', Date.now(), 'stream=' + streamState.isStreaming, 'len=' + fullText.length, 'spoken=' + spokenCharsRef.current);

    if (streamState.isStreaming) {
      const unspoken = fullText.slice(spokenCharsRef.current);
      const match = unspoken.match(/^[\s\S]*[.!?](?=\s)/);
      if (!match) return;
      take = spokenCharsRef.current + match[0].length;
    }

    if (take <= spokenCharsRef.current) return;

    const segment = fullText.slice(spokenCharsRef.current, take);
    spokenCharsRef.current = take;

    // Consumed even while muted, so unmuting mid-reply does not replay text
    // that already went past on screen.
    if (muted) return;

    const plainText = segment
      .replace(/```[\s\S]*?```/g, 'code block.')
      .replace(/`[^`]+`/g, '')
      .replace(/[#*_~>]/g, '')
      .replace(/\[([^\]]+)\]\([^)]+\)/g, '$1')
      .trim();

    if (plainText) { console.log('[TTSDBG] enqueue', Date.now(), 'stream=' + streamState.isStreaming, 'seg=' + plainText.length, 'spoken=' + spokenCharsRef.current); enqueue(plainText); }
  }, [streamState.isStreaming, streamState.content, messages, muted]);

  // Relay numbered-option button clicks into InputArea's submit flow
  useEffect(() => {
    const handler = (e: Event) => {
      const text = (e as CustomEvent<string>).detail;
      if (!text) return;
      window.dispatchEvent(new CustomEvent('jarvis-submit-text', { detail: text }));
    };
    window.addEventListener('jarvis-option-select', handler);
    return () => window.removeEventListener('jarvis-option-select', handler);
  }, []);

  const handleSendMessage = useCallback(async (text: string, attachments?: { name: string; size: number; type: string }[]) => {
    const content = text.trim();
    if (!content && (!attachments || attachments.length === 0)) return;

    const s0 = useAppStore.getState();
    if (s0.streamState.isStreaming) return;

    let convId = s0.activeId;
    if (!convId) convId = s0.createConversation(s0.selectedModel);

    const userMsg: ChatMessage = {
      id: generateId(),
      role: 'user',
      content,
      timestamp: Date.now(),
      attachments: attachments && attachments.length > 0 ? attachments : undefined,
    };
    s0.addMessage(convId, userMsg);

    const apiMessages = useAppStore.getState().messages.map((m) => ({ role: m.role, content: m.content }));

    const assistantMsg: ChatMessage = {
      id: generateId(),
      role: 'assistant',
      content: '',
      timestamp: Date.now(),
    };
    s0.addMessage(convId, assistantMsg);

    const startTime = Date.now();
    sendTimerRef.current = setInterval(() => {
      useAppStore.getState().setStreamState({ elapsedMs: Date.now() - startTime });
    }, 100);

    const controller = new AbortController();
    sendAbortRef.current = controller;

    let acc = '';
    let usage: TokenUsage | undefined;
    let complexity: { score: number; tier: string; suggested_max_tokens: number } | undefined;
    const toolCalls: ToolCallInfo[] = [];
    let lastFlush = 0;
    let ttftMs: number | undefined;

    const st = useAppStore.getState();
    st.setStreamState({ isStreaming: true, phase: 'Generating...', elapsedMs: 0, activeToolCalls: [], content: '' });
    st.addLogEntry({ timestamp: Date.now(), level: 'info', category: 'chat', message: 'Request: ' + content.slice(0, 80) });

    try {
      for await (const sseEvent of streamChat(
        {
          model: st.selectedModel,
          messages: apiMessages,
          stream: true,
          temperature: st.settings.temperature,
          max_tokens: st.settings.maxTokens,
          agent: st.selectedAgentId || '',
        },
        controller.signal,
      )) {
        const eventName = sseEvent.event;
        if (eventName === 'agent_turn_start') {
          useAppStore.getState().setStreamState({ phase: 'Agent thinking...' });
        } else if (eventName === 'inference_start') {
          useAppStore.getState().setStreamState({ phase: 'Generating...' });
        } else if (eventName === 'tool_call_start') {
          try {
            const data = JSON.parse(sseEvent.data);
            toolCalls.push({ id: generateId(), tool: data.tool, arguments: data.arguments || '', status: 'running' });
            useAppStore.getState().setStreamState({ phase: 'Calling ' + data.tool + '...', activeToolCalls: [...toolCalls] });
            useAppStore.getState().updateLastAssistant(convId, acc, [...toolCalls]);
          } catch (e) { void e; }
        } else if (eventName === 'tool_call_end') {
          try {
            const data = JSON.parse(sseEvent.data);
            const tc = toolCalls.find((t) => t.tool === data.tool && t.status === 'running');
            if (tc) {
              tc.status = data.success ? 'success' : 'error';
              tc.latency = data.latency;
              tc.result = data.result;
            }
            useAppStore.getState().setStreamState({ phase: 'Generating...', activeToolCalls: [...toolCalls] });
            useAppStore.getState().updateLastAssistant(convId, acc, [...toolCalls]);
          } catch (e) { void e; }
        } else {
          try {
            const data = JSON.parse(sseEvent.data);
            const delta = data.choices?.[0]?.delta;
            if (data.usage) usage = data.usage;
            if (data.complexity) complexity = data.complexity;
            if (delta?.content) {
              if (!ttftMs) ttftMs = Date.now() - startTime;
              acc += delta.content;
              useAppStore.getState().setStreamState({ content: acc, phase: '' });
              const now = Date.now();
              if (now - lastFlush >= 80) {
                useAppStore.getState().updateLastAssistant(convId, acc, toolCalls.length > 0 ? [...toolCalls] : undefined, undefined, undefined, undefined, false);
                lastFlush = now;
              }
            }
            if (data.choices?.[0]?.finish_reason === 'stop') break;
          } catch (e) { void e; }
        }
      }
    } catch (err) {
      const anyErr = err as { name?: string; message?: string };
      if (anyErr?.name === 'AbortError') {
        if (!acc) acc = '(Generation stopped)';
      } else {
        const errMsg = anyErr?.message || String(err);
        acc = acc || ('Error: ' + errMsg);
        useAppStore.getState().addLogEntry({ timestamp: Date.now(), level: 'error', category: 'chat', message: 'Stream error: ' + errMsg });
      }
    } finally {
      if (!acc) acc = 'No response was generated. Please try again.';
      const totalMs = Date.now() - startTime;
      const telemetry: MessageTelemetry = {
        engine: 'mcp',
        model_id: st.selectedModel,
        total_ms: totalMs,
        ttft_ms: ttftMs,
        tokens_per_sec: usage?.completion_tokens ? usage.completion_tokens / (totalMs / 1000) : undefined,
        complexity_score: complexity?.score,
        complexity_tier: complexity?.tier,
        suggested_max_tokens: complexity?.suggested_max_tokens,
      };
      useAppStore.getState().updateLastAssistant(convId, acc, toolCalls.length > 0 ? toolCalls : undefined, usage, telemetry);
      if (sendTimerRef.current) { clearInterval(sendTimerRef.current); sendTimerRef.current = null; }
      useAppStore.getState().resetStream();
      useAppStore.getState().addLogEntry({ timestamp: Date.now(), level: 'info', category: 'chat', message: 'Response: ' + acc.length + ' chars' });
      sendAbortRef.current = null;
      fetchSavings().then((d) => useAppStore.getState().setSavings(d)).catch(() => {});
    }
  }, []);

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
          title={`${systemPanelOpen ? 'Hide' : 'Show'} system panel (${navigator.platform.includes('Mac') ? '⌘' : 'Ctrl'}+I)`}
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
              <div key={msg.id}>
                <MessageBubble message={msg} />
                {msg.attachments && msg.attachments.length > 0 && (
                  <div className='flex flex-wrap gap-2 justify-end mb-4 px-1'>
                    {msg.attachments.map((att, ai) => (
                      <div
                        key={ai}
                        className='flex items-center gap-2 px-3 py-1.5 rounded-lg text-xs'
                        style={{ background: 'var(--color-accent-subtle)', border: '1px solid var(--color-border)', color: 'var(--color-text-secondary)' }}
                      >
                        <Paperclip size={12} />
                        <span className='truncate max-w-[180px]'>{att.name}</span>
                        <span style={{ color: 'var(--color-text-tertiary)' }}>{formatBytes(att.size)}</span>
                      </div>
                    ))}
                  </div>
                )}
              </div>
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
        <InputArea onSendMessage={handleSendMessage} />
      </div>
    </div>
  );
}
