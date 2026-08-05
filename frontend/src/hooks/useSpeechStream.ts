// frontend/src/hooks/useSpeechStream.ts
// WebSocket speech streaming hook: connects to /v1/speech/stream, pipes AudioWorklet frames,
// handles transcripts, barge-in, connection state.

import { useRef, useCallback, useEffect, useState } from 'react';

export type TranscriptCallback = (text: string, ttfb: number, total: number) => void;
export type StatusCallback = (status: 'connecting' | 'open' | 'closed' | 'error') => void;

interface UseSpeechStreamOptions {
  onTranscript?: TranscriptCallback;
  onStatusChange?: StatusCallback;
  onError?: (err: Error) => void;
}

export function useSpeechStream(options: UseSpeechStreamOptions = {}) {
  const wsRef = useRef<WebSocket | null>(null);
  const audioContextRef = useRef<AudioContext | null>(null);
  const workletNodeRef = useRef<AudioWorkletNode | null>(null);
  const mediaStreamRef = useRef<MediaStream | null>(null);
  const [isStreaming, setIsStreaming] = useState(false);

  const { onTranscript, onStatusChange, onError } = options;

  const setStatus = useCallback((status: 'connecting' | 'open' | 'closed' | 'error') => {
    onStatusChange?.(status);
  }, [onStatusChange]);

  const connect = useCallback(async () => {
    if (wsRef.current?.readyState === WebSocket.OPEN) return;

    setStatus('connecting');

    try {
      // 1. Get microphone access
      const stream = await navigator.mediaDevices.getUserMedia({
        audio: {
          channelCount: 1,
          echoCancellation: true,
          noiseSuppression: true,
          autoGainControl: true,
        },
      });
      mediaStreamRef.current = stream;

      // 2. Create AudioContext (resume if suspended)
      const audioCtx = new (window.AudioContext || (window as any).webkitAudioContext)();
      if (audioCtx.state === 'suspended') await audioCtx.resume();
      audioContextRef.current = audioCtx;

      // 3. Load AudioWorklet module
      await audioCtx.audioWorklet.addModule('/src/audio/worklet/PCMProcessor.js');

      // 4. Create worklet node
      const workletNode = new AudioWorkletNode(audioCtx, 'pcm-processor');
      workletNodeRef.current = workletNode;

      // 5. Connect mic -> worklet -> destination (silent output)
      const source = audioCtx.createMediaStreamSource(stream);
      source.connect(workletNode).connect(audioCtx.destination);

      // 6. Handle frames from worklet
      workletNode.port.onmessage = (e: MessageEvent<ArrayBuffer>) => {
        const frame = e.data;
        if (wsRef.current?.readyState === WebSocket.OPEN) {
          wsRef.current.send(frame);
        }
      };

      // 7. Open WebSocket
      const wsUrl = `${window.location.protocol === 'https:' ? 'wss:' : 'ws:'}//${window.location.host}/v1/speech/stream`;
      const ws = new WebSocket(wsUrl);
      ws.binaryType = 'arraybuffer';
      wsRef.current = ws;

      ws.onopen = () => {
        setStatus('open');
        setIsStreaming(true);
      };

      ws.onmessage = (event: MessageEvent<string>) => {
        try {
          const msg = JSON.parse(event.data);
          if (msg.type === 'transcript' && typeof msg.text === 'string') {
            onTranscript?.(msg.text, msg.ttfb ?? 0, msg.total ?? 0);
          } else if (msg.type === 'barge_in_ack') {
            // Server acknowledged barge-in; could trigger UI feedback
            console.debug('[useSpeechStream] barge-in acknowledged');
          }
        } catch (err) {
          console.warn('[useSpeechStream] failed to parse WS message:', err);
        }
      };

      ws.onerror = (err) => {
        console.error('[useSpeechStream] WS error:', err);
        onError?.(new Error('WebSocket error'));
        setStatus('error');
      };

      ws.onclose = () => {
        setStatus('closed');
        setIsStreaming(false);
      };
    } catch (err) {
      console.error('[useSpeechStream] connect failed:', err);
      onError?.(err as Error);
      setStatus('error');
      disconnect(); // FIXED: was cleanup()
    }
  }, [onTranscript, onError, setStatus]);

  const disconnect = useCallback(() => {
    // Signal worklet to flush partial frame
    workletNodeRef.current?.port.postMessage('flush');

    // Close WebSocket
    wsRef.current?.close();
    wsRef.current = null;

    // Stop media stream tracks
    mediaStreamRef.current?.getTracks().forEach((t) => t.stop());
    mediaStreamRef.current = null;

    // Disconnect audio graph
    workletNodeRef.current?.disconnect();
    workletNodeRef.current = null;

    audioContextRef.current?.close();
    audioContextRef.current = null;

    setIsStreaming(false);
    setStatus('closed');
  }, [setStatus]);

  const bargeIn = useCallback(() => {
    if (wsRef.current?.readyState === WebSocket.OPEN) {
      wsRef.current.send(JSON.stringify({ type: 'barge_in' }));
    }
  }, []);

  // Cleanup on unmount
  useEffect(() => {
    return () => {
      disconnect();
    };
  }, [disconnect]);

  return {
    isStreaming,
    connect,
    disconnect,
    bargeIn,
  };
}