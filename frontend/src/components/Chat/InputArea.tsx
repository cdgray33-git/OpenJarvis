// frontend/src/components/Chat/InputArea.tsx
// Updated to use useSpeechStream hook for WebSocket streaming STT

import React, { useState, useCallback, useRef, useEffect } from "react";
import { useSpeechStream, TranscriptCallback } from "@/hooks/useSpeechStream";
import { useAppStore } from "@/lib/store";
import { uploadChatFiles, getBase } from "@/lib/api";
import { Mic, MicOff, Send, X, Loader2, Paperclip, ChevronUp, ChevronDown } from "lucide-react";

interface InputAreaProps {
  onSendMessage: (text: string, attachments?: { name: string; size: number; type: string }[]) => void;
  disabled?: boolean;
  placeholder?: string;
}

const CHAT_ACCEPTED_EXTENSIONS = '.txt,.md,.pdf,.docx,.csv,.zip,.png,.jpg,.jpeg,.gif,.webp,.bmp,.tiff,.mp4,.webm,.mov,.mkv,.avi';

interface AttachedFile {
  name: string;
  size: number;
  type: string;
  preview?: string;
  file?: File;
}

export function InputArea({ onSendMessage, disabled = false, placeholder = "Type a message..." }: InputAreaProps) {
  const [text, setText] = useState("");
  const [isStreaming, setIsStreaming] = useState(false);
  const [transcriptPreview, setTranscriptPreview] = useState("");
  const [status, setStatus] = useState<"idle" | "connecting" | "streaming" | "open" | "closed" | "error">("idle");
  const [attachedFiles, setAttachedFiles] = useState<AttachedFile[]>([]);
  const [showAttachments, setShowAttachments] = useState(false);
  const [isDragOver, setIsDragOver] = useState(false);
  const textareaRef = useRef<HTMLTextAreaElement>(null);
  const previewRef = useRef<HTMLDivElement>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);
  const attachmentsRef = useRef<HTMLDivElement>(null);
  const [agents, setAgents] = useState<{ key: string; class: string; accepts_tools: boolean }[]>([]);
  const [selectedAgent, setSelectedAgent] = useState<string>('');
  const setSelectedAgentId = useAppStore((s) => s.setSelectedAgentId);

  const { addMessage } = useAppStore();

  const handleTranscript: TranscriptCallback = useCallback((text, ttfb, total) => {
    if (text.trim()) {
      setTranscriptPreview(text);
      previewRef.current?.scrollIntoView({ behavior: "smooth", block: "nearest" });
    }
  }, []);

  const handleStatusChange = useCallback((s: "connecting" | "open" | "streaming" | "closed" | "error") => {
    setStatus(s);
    setIsStreaming(s === "open" || s === "streaming");
    if (s === "closed" || s === "error") {
      if (transcriptPreview.trim()) {
        onSendMessage(transcriptPreview.trim());
        setTranscriptPreview("");
      }
    }
  }, [onSendMessage, transcriptPreview]);

  const handleError = useCallback((err: Error) => {
    console.error("[InputArea] Speech stream error:", err);
    setStatus("error");
    setTimeout(() => setStatus("idle"), 3000);
  }, []);

  const { connect, disconnect, bargeIn } = useSpeechStream({
    onTranscript: handleTranscript,
    onStatusChange: handleStatusChange,
    onError: handleError,
  });

  const handleMicClick = useCallback(() => {
    if (isStreaming || status === "connecting") {
      disconnect();
    } else {
      connect();
    }
  }, [isStreaming, status, connect, disconnect]);

  const handleFiles = useCallback(async (files: FileList) => {
    const newFiles: AttachedFile[] = []
    for (const file of Array.from(files)) {
      if (file.size > 50 * 1024 * 1024) {
        alert(`File ${file.name} is too large (max 50MB)`)
        continue
      }
      let preview: string | undefined
      if (file.type.startsWith('image/')) {
        preview = await new Promise((resolve) => {
          const reader = new FileReader()
          reader.onload = () => resolve(reader.result as string)
          reader.readAsDataURL(file)
        })
      }
      newFiles.push({
        name: file.name,
        size: file.size,
        type: file.type,
        preview,
        file,
      })
    }
    setAttachedFiles((prev) => [...prev, ...newFiles])
    setShowAttachments(true)
  }, [])

  const removeFile = useCallback((index: number) => {
    setAttachedFiles((prev) => prev.filter((_, i) => i !== index))
  }, [])

  const handleDragOver = useCallback((e: React.DragEvent) => {
    e.preventDefault()
    e.stopPropagation()
    setIsDragOver(true)
  }, [])

  const handleDragLeave = useCallback((e: React.DragEvent) => {
    e.preventDefault()
    e.stopPropagation()
    setIsDragOver(false)
  }, [])

  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault()
    e.stopPropagation()
    setIsDragOver(false)
    if (e.dataTransfer.files.length > 0) {
      handleFiles(e.dataTransfer.files)
    }
  }, [handleFiles])

  const handleFileInputChange = useCallback((e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      handleFiles(e.target.files)
      e.target.value = ''
    }
  }, [handleFiles])

  const sendWithAttachments = useCallback(async () => {
    const msg = text.trim() || transcriptPreview.trim()
    if (!msg && attachedFiles.length === 0) return
    
    if (attachedFiles.length > 0) {
      const filesToUpload = attachedFiles.map(f => f.file).filter((f): f is File => !!f)
      if (filesToUpload.length > 0) {
        try {
          await uploadChatFiles(filesToUpload)
        } catch (e) {
          console.error('File upload error:', e)
        }
      }
    }
    
    const attachmentMeta = attachedFiles.map((f) => ({ name: f.name, size: f.size, type: f.type }))
    onSendMessage(msg, attachmentMeta.length > 0 ? attachmentMeta : undefined)
    setText('')
    setTranscriptPreview('')
    setAttachedFiles([])
    setShowAttachments(false)
    if (isStreaming) {
      bargeIn()
      disconnect()
    }
  }, [text, transcriptPreview, attachedFiles, onSendMessage, isStreaming, bargeIn, disconnect])

  const handleSendClick = sendWithAttachments

  const handleKeyDown = useCallback((e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSendClick();
    }
  }, [handleSendClick]);

  const handleTextChange = useCallback((e: React.ChangeEvent<HTMLTextAreaElement>) => {
    setText(e.target.value);
    if (isStreaming && e.target.value.trim()) {
      bargeIn();
      disconnect();
    }
  }, [isStreaming, bargeIn, disconnect]);

  useEffect(() => {
    textareaRef.current?.focus();
  }, []);

  useEffect(() => {
    const handleClickOutside = (e: MouseEvent) => {
      if (attachmentsRef.current && !attachmentsRef.current.contains(e.target as Node)) {
        setShowAttachments(false)
      }
    }
    document.addEventListener('mousedown', handleClickOutside)
    return () => document.removeEventListener('mousedown', handleClickOutside)
  }, [])

  useEffect(() => {
    fetch(getBase() + '/v1/agents')
      .then((r) => (r.ok ? r.json() : { registered: [] }))
      .then((d) => setAgents(d.registered || []))
      .catch(() => {});
  }, [])

  const micIcon = isStreaming ? (
    <MicOff className="w-5 h-5 text-red-500" />
  ) : (
    <Mic className="w-5 h-5 text-gray-600 hover:text-blue-600" />
  );

  const formatSize = (bytes: number) => {
    if (bytes < 1024) return `${bytes} B`
    if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`
    return `${(bytes / (1024 * 1024)).toFixed(1)} MB`
  }

  const getFileIcon = (type: string, preview?: string) => {
    if (preview) return <img src={preview} alt="" className="w-5 h-5 rounded object-cover" />
    if (type.startsWith('image/')) return <span className="text-xs text-gray-500">🖼</span>
    if (type.startsWith('video/')) return <span className="text-xs text-gray-500">🎬</span>
    if (type === 'application/zip' || type === 'application/x-zip-compressed') return <span className="text-xs text-gray-500">📦</span>
    if (type === 'application/pdf') return <span className="text-xs text-gray-500">📄</span>
    return <span className="text-xs text-gray-500">📎</span>
  }

  return (
    <div className="flex flex-col gap-2 p-4 border-t border-gray-200 bg-white">
      {(isStreaming || transcriptPreview) && (
        <div
          ref={previewRef}
          className={`px-3 py-2 rounded-lg border transition-all ${
            isStreaming
              ? "bg-blue-50 border-blue-200 text-blue-900"
              : "bg-green-50 border-green-200 text-green-900"
          }`}
        >
          <div className="flex items-center gap-2 text-sm">
            <Loader2 className={`w-4 h-4 animate-spin ${isStreaming ? "text-blue-500" : "hidden"}`} />
            <span className="font-medium">{isStreaming ? "Listening..." : "Ready to send"}</span>
            {isStreaming && (
              <span className="text-xs text-blue-600">(click mic to stop)</span>
            )}
          </div>
          {transcriptPreview && (
            <p className="mt-1 text-sm whitespace-pre-wrap">{transcriptPreview}</p>
          )}
        </div>
      )}

      {attachedFiles.length > 0 && showAttachments && (
        <div
          ref={attachmentsRef}
          className="absolute bottom-full left-0 right-0 mb-2 p-2 rounded-lg border bg-white shadow-lg z-10 max-h-60 overflow-y-auto"
          style={{ borderColor: 'var(--color-border)' }}
        >
          <div className="flex items-center justify-between mb-2 pb-2 border-b text-sm font-medium">
            <span>Attachments ({attachedFiles.length})</span>
            <button
              onClick={() => setShowAttachments(false)}
              className="p-1 text-gray-400 hover:text-gray-600"
              aria-label="Close attachments"
            >
              <X className="w-4 h-4" />
            </button>
          </div>
          {attachedFiles.map((file, idx) => (
            <div key={idx} className="flex items-center gap-2 px-2 py-1.5 rounded hover:bg-gray-50">
              {getFileIcon(file.type, file.preview)}
              <div className="flex-1 min-w-0">
                <p className="text-sm truncate">{file.name}</p>
                <p className="text-xs text-gray-400">{formatSize(file.size)}</p>
              </div>
              <button
                onClick={() => removeFile(idx)}
                className="p-1 text-gray-400 hover:text-red-500"
                aria-label={`Remove ${file.name}`}
              >
                <X className="w-4 h-4" />
              </button>
            </div>
          ))}
          <button
            onClick={() => fileInputRef.current?.click()}
            className="w-full mt-2 px-2 py-1.5 text-xs text-center text-blue-600 hover:bg-blue-50 rounded"
          >
            + Add more files
          </button>
        </div>
      )}

      <div className="flex items-end gap-2 relative">
        <textarea
          ref={textareaRef}
          value={text}
          onChange={handleTextChange}
          onKeyDown={handleKeyDown}
          placeholder={placeholder}
          disabled={disabled || isStreaming}
          rows={1}
          className={`
            flex-1 px-4 py-2.5 rounded-lg border resize-none
            focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent
            transition-colors
            ${disabled || isStreaming ? "bg-gray-50 text-gray-500 cursor-not-allowed" : "bg-white"}
            ${isStreaming ? "border-blue-200" : "border-gray-300"}
            pr-12
          `}
          style={{ minHeight: "44px" }}
        />

        <div className="relative" ref={attachmentsRef}>
          <button
            onClick={() => {
              if (attachedFiles.length > 0) {
                setShowAttachments(!showAttachments)
              } else {
                fileInputRef.current?.click()
              }
            }}
            onDragOver={handleDragOver}
            onDragLeave={handleDragLeave}
            onDrop={handleDrop}
            disabled={disabled}
            className={`
              p-2.5 rounded-lg transition-colors flex-shrink-0
              ${attachedFiles.length > 0
                ? "bg-blue-50 text-blue-600 hover:bg-blue-100"
                : "bg-gray-100 text-gray-600 hover:bg-gray-200"}
              ${disabled ? "opacity-50 cursor-not-allowed" : ""}
              ${isDragOver ? "bg-blue-100 border-blue-400" : ""}
            `}
            title={attachedFiles.length > 0 ? `${attachedFiles.length} file(s) attached - click to manage` : "Attach files"}
            aria-label={attachedFiles.length > 0 ? `${attachedFiles.length} file(s) attached` : "Attach files"}
          >
            <Paperclip className="w-5 h-5" />
            {attachedFiles.length > 0 && (
              <span className="absolute -top-1 -right-1 w-5 h-5 text-xs font-medium bg-red-500 text-white rounded-full flex items-center justify-center">
                {attachedFiles.length > 9 ? '9+' : attachedFiles.length}
              </span>
            )}
            {showAttachments && <ChevronUp className="w-4 h-4 ml-1" />}
            {!showAttachments && attachedFiles.length === 0 && <ChevronDown className="w-4 h-4 ml-1 opacity-50" />}
          </button>
          
          <input
            ref={fileInputRef}
            type="file"
            multiple
            accept={CHAT_ACCEPTED_EXTENSIONS}
            onChange={handleFileInputChange}
            className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
            aria-hidden="true"
          />
        </div>

        <select
          value={selectedAgent}
          onChange={(e) => { setSelectedAgent(e.target.value); setSelectedAgentId(e.target.value || null); }}
          disabled={disabled}
          className='h-[44px] px-2 rounded-lg border border-gray-300 bg-white text-xs text-gray-700 flex-shrink-0 max-w-[150px]'
          title='Agent'
          aria-label='Select agent'
        >
          <option value=''>No agent (chat)</option>
          {agents.map((a) => (
            <option key={a.key} value={a.key}>{a.key}</option>
          ))}
        </select>

        <button
          onClick={handleMicClick}
          disabled={disabled || status === "connecting"}
          className={`
            p-2.5 rounded-lg transition-colors flex-shrink-0
            ${isStreaming
              ? "bg-red-50 text-red-600 hover:bg-red-100"
              : "bg-gray-100 text-gray-600 hover:bg-gray-200"}
            ${disabled || status === "connecting" ? "opacity-50 cursor-not-allowed" : ""}
          `}
          title={isStreaming ? "Stop listening" : "Start voice input"}
          aria-label={isStreaming ? "Stop voice input" : "Start voice input"}
        >
          {status === "connecting" ? (
            <Loader2 className="w-5 h-5 animate-spin" />
          ) : (
            micIcon
          )}
        </button>

        <button
          onClick={handleSendClick}
          disabled={disabled || (!text.trim() && !transcriptPreview.trim() && attachedFiles.length === 0)}
          className={`
            p-2.5 rounded-lg transition-colors flex-shrink-0
            ${text.trim() || transcriptPreview.trim() || attachedFiles.length > 0
              ? "bg-blue-600 text-white hover:bg-blue-700"
              : "bg-gray-100 text-gray-400 cursor-not-allowed"}
          `}
          title="Send message"
          aria-label="Send message"
        >
          <Send className="w-5 h-5" />
        </button>

        {(text.trim() || attachedFiles.length > 0) && (
          <button
            onClick={() => { setText(""); setAttachedFiles([]); setShowAttachments(false); }}
            className="p-2.5 rounded-lg bg-gray-100 text-gray-600 hover:bg-gray-200 transition-colors"
            title="Clear input"
            aria-label="Clear input"
          >
            <X className="w-5 h-5" />
          </button>
        )}
      </div>

      {status === "error" && (
        <div className="text-xs text-red-600 flex items-center gap-1">
          <span>Speech recognition error — click mic to retry</span>
        </div>
      )}
    </div>
  );
}
