import pathlib

path = pathlib.Path(r"C:\Windows\System32\OpenJarvis\frontend\src\lib\api.ts")
content = path.read_text(encoding="utf-8")

old = """export async function synthesizeSpeech(text: string, voiceId = 'am_adam', speed = 0.85): Promise<Blob> {
  const res = await apiFetch(\\/v1/speech/synthesize\, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ text, voice_id: voiceId, speed, output_format: 'wav' }),
  });
  if (!res.ok) throw new Error(\Synthesis failed: \\);
  return res.blob();
}"""

new = """export async function synthesizeSpeech(text: string, voiceId = 'am_adam', speed = 0.85): Promise<Blob> {
  const res = await apiFetch(\\/v1/speech/synthesize\, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ text, voice_id: voiceId, speed, output_format: 'wav' }),
  });
  if (!res.ok) throw new Error(\Synthesis failed: \\);
  return res.blob();
}

// ---------------------------------------------------------------------------
// TTS chunking — Kokoro has a hard ~510-phoneme ceiling per call. Long
// responses must be split into sentence-sized chunks so each call stays
// well under that limit (roughly 350 chars is a safe margin for most
// English text) and so the frontend can start playing audio before the
// entire response has been synthesized.
// ---------------------------------------------------------------------------

const TTS_MAX_CHUNK_CHARS = 350;

export function splitIntoTTSChunks(text: string): string[] {
  const sentences = text.match(/[^.!?]+[.!?]+(?:\\s+|$)|[^.!?]+$/g) || [text];
  const chunks: string[] = [];
  let current = '';
  for (const raw of sentences) {
    const sentence = raw.trim();
    if (!sentence) continue;
    if (sentence.length > TTS_MAX_CHUNK_CHARS) {
      // Single sentence itself too long — hard-split on word boundaries.
      if (current) { chunks.push(current); current = ''; }
      const words = sentence.split(/\\s+/);
      let piece = '';
      for (const w of words) {
        if ((piece + ' ' + w).trim().length > TTS_MAX_CHUNK_CHARS) {
          if (piece) chunks.push(piece.trim());
          piece = w;
        } else {
          piece = (piece + ' ' + w).trim();
        }
      }
      if (piece) chunks.push(piece);
      continue;
    }
    if ((current + ' ' + sentence).trim().length > TTS_MAX_CHUNK_CHARS) {
      if (current) chunks.push(current.trim());
      current = sentence;
    } else {
      current = (current + ' ' + sentence).trim();
    }
  }
  if (current) chunks.push(current.trim());
  return chunks.filter((c) => c.length > 0);
}

/**
 * Synthesize each chunk in order, invoking onChunk(blob, index) as soon as
 * each one is ready. Synthesis of chunk N+1 begins immediately after chunk
 * N's request is sent (not awaited serially) so the pipeline stays full,
 * but onChunk fires in strict order so playback never gets out of sequence.
 */
export async function synthesizeSpeechChunks(
  text: string,
  onChunk: (blob: Blob, index: number, total: number) => void,
  voiceId = 'am_adam',
  speed = 0.85,
): Promise<void> {
  const chunks = splitIntoTTSChunks(text);
  const total = chunks.length;
  let nextToDeliver = 0;
  const results: (Blob | null)[] = new Array(total).fill(null);

  const deliverReady = () => {
    while (nextToDeliver < total && results[nextToDeliver] !== null) {
      onChunk(results[nextToDeliver] as Blob, nextToDeliver, total);
      nextToDeliver += 1;
    }
  };

  await Promise.all(
    chunks.map(async (chunk, i) => {
      try {
        const blob = await synthesizeSpeech(chunk, voiceId, speed);
        results[i] = blob;
      } catch {
        results[i] = new Blob([], { type: 'audio/wav' });
      }
      deliverReady();
    }),
  );
}"""

if old not in content:
    print("ERROR: synthesizeSpeech block not found — file may have changed")
    raise SystemExit(1)

content = content.replace(old, new, 1)
path.write_text(content, encoding="utf-8", newline="\n")
print("OK: api.ts chunking helpers added")
