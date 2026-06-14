import { useState, useMemo } from 'react';
import ReactMarkdown from 'react-markdown';
import rehypeHighlight from 'rehype-highlight';
import rehypeKatex from 'rehype-katex';
import remarkGfm from 'remark-gfm';
import remarkMath from 'remark-math';
import 'katex/dist/katex.min.css';
import { Copy, Check } from 'lucide-react';
import { AudioPlayer } from './AudioPlayer';
import { ToolCallCard } from './ToolCallCard';
import { XRayFooter } from './XRayFooter';
import type { ChatMessage } from '../../types';

function stripThinkTags(text: string): string {
  let cleaned = text.replace(/<think>[\s\S]*?<\/think>\s*/gi, '');
  cleaned = cleaned.replace(/^[\s\S]*?<\/think>\s*/i, '');
  return cleaned.trim();
}

interface Props {
  message: ChatMessage;
}

interface ParsedOptions {
  preamble: string;
  options: { number: string; text: string }[];
}

/**
 * Detects numbered lists in assistant responses and extracts them as options.
 * Returns null if the message doesn't look like a question with numbered choices.
 *
 * Matches patterns like:
 *   1. Option text
 *   1) Option text
 *   **1.** Option text  (bold markdown)
 */
function parseNumberedOptions(text: string): ParsedOptions | null {
  const lines = text.split('\n');

  // Find the first numbered item
  const numberedLineRegex = /^\s*\*{0,2}(\d+)[.)]\*{0,2}\s+(.+)/;
  let firstIndex = -1;
  for (let i = 0; i < lines.length; i++) {
    if (numberedLineRegex.test(lines[i])) {
      firstIndex = i;
      break;
    }
  }

  if (firstIndex === -1) return null;

  // Collect consecutive numbered items
  const options: { number: string; text: string }[] = [];
  let lastIndex = firstIndex;

  for (let i = firstIndex; i < lines.length; i++) {
    const match = lines[i].match(numberedLineRegex);
    if (match) {
      options.push({ number: match[1], text: match[2].replace(/\*+/g, '').trim() });
      lastIndex = i;
    } else if (lines[i].trim() === '') {
      // Allow blank lines within the list
      continue;
    } else if (/^\s+[*\-]/.test(lines[i])) {
      // Sub-bullet under a numbered item -- skip
      continue;
    } else {
      // Non-numbered non-blank non-sub-bullet -- stop
      break;
    }
  }

  // Only render as buttons if there are 2–8 options
  if (options.length < 2 || options.length > 8) return null;

  const preamble = lines.slice(0, firstIndex).join('\n').trim();

  // Check for trailing content after the list — if there's significant text after,
  // it's probably not a "pick one" prompt, just render normally
  const trailing = lines.slice(lastIndex + 1).join('\n').trim();
  if (trailing.length > 500) return null;

  return { preamble, options };
}

function getTextContent(node: any): string {
  if (typeof node === 'string' || typeof node === 'number') {
    return String(node);
  }
  if (Array.isArray(node)) {
    return node.map(getTextContent).join('');
  }
  if (node?.props?.children) {
    return getTextContent(node.props.children);
  }
  return '';
}

function CodeBlockPre({ children, ...props }: any) {
  const [copied, setCopied] = useState(false);
  const codeElement = Array.isArray(children) ? children[0] : children;
  const className = codeElement?.props?.className || '';
  const match = /language-([\w-]+)/.exec(className);
  const lang = match ? match[1] : '';
  const code = getTextContent(codeElement?.props?.children).replace(/\n$/, '');

  const handleCopy = () => {
    navigator.clipboard.writeText(code);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div
      className="code-block-wrapper relative my-3"
      style={{ borderRadius: 'var(--radius-md)', overflow: 'hidden' }}
    >
      <div
        className="flex items-center justify-between px-4 py-1.5 text-xs"
        style={{ background: 'var(--color-bg-tertiary)', color: 'var(--color-text-tertiary)' }}
      >
        <span className="font-mono">{lang || 'code'}</span>
        <button
          onClick={handleCopy}
          className="flex items-center gap-1 px-2 py-0.5 rounded transition-colors cursor-pointer"
          style={{ color: 'var(--color-text-tertiary)' }}
          onMouseEnter={(e) => (e.currentTarget.style.color = 'var(--color-text-secondary)')}
          onMouseLeave={(e) => (e.currentTarget.style.color = 'var(--color-text-tertiary)')}
        >
          {copied ? <Check size={12} /> : <Copy size={12} />}
          {copied ? 'Copied' : 'Copy'}
        </button>
      </div>
      <pre {...props} style={{ margin: 0, borderRadius: 0 }}>
        {children}
      </pre>
    </div>
  );
}

function CopyMessageButton({ content }: { content: string }) {
  const [copied, setCopied] = useState(false);

  const handleCopy = () => {
    navigator.clipboard.writeText(content);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <button
      onClick={handleCopy}
      className="p-1 rounded opacity-0 group-hover:opacity-100 transition-opacity cursor-pointer"
      style={{ color: 'var(--color-text-tertiary)' }}
      title="Copy message"
    >
      {copied ? <Check size={14} /> : <Copy size={14} />}
    </button>
  );
}

function NumberedOptionButtons({ parsed }: { parsed: ParsedOptions }) {
  const [selected, setSelected] = useState<string | null>(null);

  const handleSelect = (option: { number: string; text: string }) => {
    if (selected) return; // already chosen
    setSelected(option.number);
    window.dispatchEvent(
      new CustomEvent('jarvis-option-select', { detail: option.text })
    );
  };

  return (
    <div>
      {/* Preamble text rendered as markdown */}
      {parsed.preamble && (
        <div className="prose max-w-none mb-3">
          <ReactMarkdown
            remarkPlugins={[remarkGfm, remarkMath]}
            rehypePlugins={[[rehypeHighlight, { detect: true }], rehypeKatex]}
            components={{ pre: CodeBlockPre }}
          >
            {parsed.preamble}
          </ReactMarkdown>
        </div>
      )}

      {/* Option buttons */}
      <div
        style={{
          display: 'flex',
          flexDirection: 'column',
          gap: '0.5rem',
          marginTop: parsed.preamble ? '0' : '0.25rem',
        }}
      >
        {parsed.options.map((opt) => {
          const isSelected = selected === opt.number;
          const isDimmed = selected !== null && !isSelected;

          return (
            <button
              key={opt.number}
              onClick={() => handleSelect(opt)}
              disabled={selected !== null}
              style={{
                display: 'flex',
                alignItems: 'center',
                gap: '0.75rem',
                padding: '0.6rem 1rem',
                borderRadius: 'var(--radius-lg)',
                border: isSelected
                  ? '1.5px solid var(--color-accent)'
                  : '1.5px solid var(--color-border)',
                background: isSelected
                  ? 'var(--color-accent-subtle)'
                  : 'var(--color-bg-secondary)',
                color: isDimmed
                  ? 'var(--color-text-tertiary)'
                  : 'var(--color-text)',
                cursor: selected ? 'default' : 'pointer',
                opacity: isDimmed ? 0.45 : 1,
                textAlign: 'left',
                fontSize: '0.875rem',
                transition: 'all 0.15s ease',
                width: '100%',
              }}
              onMouseEnter={(e) => {
                if (!selected) {
                  e.currentTarget.style.borderColor = 'var(--color-accent)';
                  e.currentTarget.style.background = 'var(--color-accent-subtle)';
                }
              }}
              onMouseLeave={(e) => {
                if (!selected) {
                  e.currentTarget.style.borderColor = 'var(--color-border)';
                  e.currentTarget.style.background = 'var(--color-bg-secondary)';
                }
              }}
            >
              {/* Number badge */}
              <span
                style={{
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  minWidth: '1.5rem',
                  height: '1.5rem',
                  borderRadius: '50%',
                  background: isSelected ? 'var(--color-accent)' : 'var(--color-bg-tertiary)',
                  color: isSelected ? 'var(--color-on-accent)' : 'var(--color-text-secondary)',
                  fontSize: '0.75rem',
                  fontWeight: 600,
                  flexShrink: 0,
                  transition: 'all 0.15s ease',
                }}
              >
                {opt.number}
              </span>
              <span>{opt.text}</span>
            </button>
          );
        })}
      </div>
    </div>
  );
}

export function MessageBubble({ message }: Props) {
  const isUser = message.role === 'user';

  if (isUser) {
    return (
      <div className="flex justify-end mb-4">
        <div
          className="max-w-[85%] px-4 py-2.5 text-sm leading-relaxed"
          style={{
            background: 'var(--color-user-bubble)',
            color: 'var(--color-user-bubble-text)',
            borderRadius: 'var(--radius-xl) var(--radius-xl) var(--radius-sm) var(--radius-xl)',
            whiteSpace: 'pre-wrap',
            wordBreak: 'break-word',
          }}
        >
          {message.content}
        </div>
      </div>
    );
  }

  const cleanContent = useMemo(() => stripThinkTags(message.content), [message.content]);
  const parsedOptions = useMemo(() => parseNumberedOptions(cleanContent), [cleanContent]);

  return (
    <div className="group mb-6">
      {/* Tool calls */}
      {message.toolCalls && message.toolCalls.length > 0 && (
        <div className="mb-3 flex flex-col gap-2">
          {message.toolCalls.map((tc) => (
            <ToolCallCard key={tc.id} toolCall={tc} />
          ))}
        </div>
      )}

      {/* Audio player (e.g. morning digest) */}
      {message.audio?.url && <AudioPlayer src={message.audio.url} />}

      {/* Assistant message — numbered options OR regular markdown */}
      {cleanContent && (
        parsedOptions ? (
          <NumberedOptionButtons parsed={parsedOptions} />
        ) : (
          <div className="prose max-w-none">
            <ReactMarkdown
              remarkPlugins={[remarkGfm, remarkMath]}
              rehypePlugins={[[rehypeHighlight, { detect: true }], rehypeKatex]}
              components={{
                pre: CodeBlockPre,
              }}
            >
              {cleanContent}
            </ReactMarkdown>
          </div>
        )
      )}

      {/* Footer: copy + x-ray */}
      <div className="flex items-center gap-2 mt-1.5">
        <CopyMessageButton content={cleanContent} />
      </div>
      <XRayFooter usage={message.usage} telemetry={message.telemetry} />
    </div>
  );
}
