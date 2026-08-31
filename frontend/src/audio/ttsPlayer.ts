/*
 * ttsPlayer.ts - OpenJarvis TTS playback engine.
 * MARKER: openjarvis-tts-player-v1
 *
 * One persistent AudioContext for the whole session. Two reasons:
 *
 *   1. The Windows audio output endpoint sleeps when idle and swallows the head
 *      of the first sound sent to it after a period of silence. That is the
 *      missing-first-word defect. It reproduces outside the browser, in an
 *      ordinary media player, and disappears when the same file is replayed
 *      immediately. Holding a live AudioContext plus a silent keepalive source
 *      keeps the endpoint awake, so no chunk is ever a cold start.
 *
 *   2. Scheduling decoded AudioBuffers on one context timeline removes the
 *      per-chunk object URL, the revoke race that produced ERR_FILE_NOT_FOUND,
 *      and the inter-chunk gap that new Audio(url) + onended chaining cannot
 *      avoid.
 *
 * Synthesis runs faster than realtime: measured 13.376 s of audio returned from
 * a 7.68 s request. So once the first unit is playing, the queue never starves
 * and only the FIRST unit's latency is user-visible. That is the entire reason
 * FIRST_UNIT_MAX_CHARS is much smaller than UNIT_MAX_CHARS - the first unit is
 * deliberately a short clause so audio begins early, and everything after it is
 * packed normally to keep request count down.
 *
 * This module owns playback and nothing else. It has no React dependency and no
 * knowledge of messages or streaming state. The caller feeds it text.
 */

import { synthesizeSpeech } from '../lib/api';

/* Short first unit: time-to-first-audio is dominated by this one request. */
const FIRST_UNIT_MAX_CHARS = 90;

/* Kokoro's practical ceiling; matches the existing splitIntoTTSChunks cap. */
const UNIT_MAX_CHARS = 350;

/* Never schedule into the past. Small lead absorbs decode and event jitter. */
const SCHEDULE_LEAD_SECONDS = 0.08;

/*
 * Keepalive amplitude. Zero relies on the AudioContext holding the output
 * stream open, which is normally sufficient. If a machine is ever found whose
 * driver still idles through digital silence, raise this to something tiny like
 * 0.0001 - inaudible, but non-zero output. One line, one place.
 */
const KEEPALIVE_GAIN = 0.0;

let ctx: AudioContext | null = null;
let masterGain: GainNode | null = null;
let keepalive: AudioBufferSourceNode | null = null;

let pending: string[] = [];
let pumping = false;
let nextStartTime = 0;
let firstUnitQueued = false;

/* Bumped by stopAll() so in-flight synthesis from a cancelled turn is dropped. */
let generation = 0;

const active: Set<AudioBufferSourceNode> = new Set();

/* ------------------------------------------------------------------ */
/* Context lifecycle                                                    */
/* ------------------------------------------------------------------ */

function ensureContext(): AudioContext | null {
  if (ctx) {
    if (ctx.state === 'suspended') {
      void ctx.resume();
    }
    return ctx;
  }

  const Ctor =
    window.AudioContext ||
    (window as unknown as { webkitAudioContext?: typeof AudioContext })
      .webkitAudioContext;
  if (!Ctor) return null;

  try {
    ctx = new Ctor();
  } catch (err) {
    console.warn('[tts] AudioContext unavailable:', err);
    ctx = null;
    return null;
  }

  masterGain = ctx.createGain();
  masterGain.gain.value = 1;
  masterGain.connect(ctx.destination);

  startKeepalive(ctx);
  nextStartTime = ctx.currentTime;
  return ctx;
}

function startKeepalive(context: AudioContext): void {
  if (keepalive) return;
  try {
    const buf = context.createBuffer(1, context.sampleRate, context.sampleRate);
    const src = context.createBufferSource();
    src.buffer = buf;
    src.loop = true;
    const gain = context.createGain();
    gain.gain.value = KEEPALIVE_GAIN;
    src.connect(gain);
    gain.connect(context.destination);
    src.start();
    keepalive = src;
  } catch (err) {
    console.warn('[tts] keepalive failed to start:', err);
    keepalive = null;
  }
}

/*
 * An AudioContext created before any user gesture starts suspended. Prime it on
 * the first interaction so the device is already awake when the first reply
 * arrives. Self-installing, so the caller does not have to remember.
 */
function installGesturePrime(): void {
  if (typeof window === 'undefined') return;
  const handler = () => {
    ensureContext();
  };
  window.addEventListener('pointerdown', handler, { once: true, capture: true });
  window.addEventListener('keydown', handler, { once: true, capture: true });
}

installGesturePrime();

/* ------------------------------------------------------------------ */
/* Text splitting                                                       */
/* ------------------------------------------------------------------ */

/*
 * Break text into clause-sized pieces. Splitting at commas, semicolons and
 * colons as well as sentence ends is what lets the first unit be short: a
 * 205-character sentence packed whole would put the old 7.7 s request back on
 * the critical path.
 */
function breakText(text: string): string[] {
  const out: string[] = [];
  const sentences = text.split(/(?<=[.!?])\s+/);
  for (const sentence of sentences) {
    const trimmed = sentence.trim();
    if (!trimmed) continue;
    const parts = trimmed.split(/(?<=[,;:])\s+/);
    for (const part of parts) {
      const piece = part.trim();
      if (piece) out.push(piece);
    }
  }
  return out;
}

/*
 * Greedy pack, with a smaller cap until the first unit has been emitted.
 * A piece longer than the cap is emitted whole rather than cut mid-word.
 */
function splitIntoUnits(text: string, firstMax: number, max: number): string[] {
  const units: string[] = [];
  let cap = firstMax;
  let current = '';

  const flush = () => {
    const trimmed = current.trim();
    if (trimmed) {
      units.push(trimmed);
      cap = max;
    }
    current = '';
  };

  for (const piece of breakText(text)) {
    if (piece.length > cap) {
      flush();
      /*
       * First unit only: bound time-to-first-audio by cutting an oversized
       * piece at a word boundary instead of emitting it whole. `cap < max`
       * is true only while the first unit is still being built -- on every
       * later enqueue firstMax === max, so this branch cannot fire.
       */
      if (cap < max) {
        const head = piece.slice(0, cap);
        const cut = head.lastIndexOf(' ');
        if (cut > 0) {
          units.push(piece.slice(0, cut).trim());
          cap = max;
          current = piece.slice(cut + 1);
          continue;
        }
      }
      units.push(piece);
      cap = max;
      continue;
    }
    const candidate = current ? current + ' ' + piece : piece;
    if (candidate.length > cap) {
      flush();
      current = piece;
    } else {
      current = candidate;
    }
  }
  flush();

  return units;
}

/* ------------------------------------------------------------------ */
/* Synthesis pump and scheduling                                        */
/* ------------------------------------------------------------------ */

function schedule(buffer: AudioBuffer): void {
  const context = ctx;
  if (!context || !masterGain) return;

  const src = context.createBufferSource();
  src.buffer = buffer;
  src.connect(masterGain);

  const earliest = context.currentTime + SCHEDULE_LEAD_SECONDS;
  if (nextStartTime < earliest) nextStartTime = earliest;

  src.start(nextStartTime);
  nextStartTime += buffer.duration;

  active.add(src);
  src.onended = () => {
    active.delete(src);
  };
}

async function pump(): Promise<void> {
  if (pumping) return;
  pumping = true;
  const myGeneration = generation;

  try {
    while (pending.length > 0) {
      if (myGeneration !== generation) return;

      const unit = pending.shift() as string;
      let buffer: AudioBuffer;
      const t0 = Date.now();
      console.log('[PUMPDBG] take', t0, 'chars=' + unit.length, 'pending=' + pending.length);

      try {
        const blob = await synthesizeSpeech(unit);
        const t1 = Date.now();
        console.log('[PUMPDBG] fetched', t1, '+' + (t1 - t0) + 'ms', 'bytes=' + blob.size);
        if (myGeneration !== generation) return;

        const bytes = await blob.arrayBuffer();
        const t2 = Date.now();
        console.log('[PUMPDBG] buffered', t2, '+' + (t2 - t1) + 'ms');
        const context = ensureContext();
        if (!context) return;
        console.log('[PUMPDBG] ctx', Date.now(), 'state=' + context.state, 'currentTime=' + context.currentTime.toFixed(3));

        buffer = await context.decodeAudioData(bytes.slice(0));
        const t3 = Date.now();
        console.log('[PUMPDBG] decoded', t3, '+' + (t3 - t2) + 'ms', 'dur=' + buffer.duration.toFixed(2) + 's');
      } catch (err) {
        /*
         * Loud on purpose. The old play().catch() discarded a failed chunk with
         * no signal at all, which is why chunk loss went unnoticed for weeks.
         */
        console.warn('[tts] unit failed, continuing:', err);
        continue;
      }

      if (myGeneration !== generation) return;
      schedule(buffer);
      console.log('[PUMPDBG] scheduled', Date.now(), 'state=' + (ctx ? ctx.state : 'null'), 'now=' + (ctx ? ctx.currentTime.toFixed(3) : '-'), 'next=' + nextStartTime.toFixed(3));
    }
  } finally {
    pumping = false;
  }
}

/* ------------------------------------------------------------------ */
/* Public API                                                           */
/* ------------------------------------------------------------------ */

/* Create or resume the context. Safe to call repeatedly. */
export function primeAudio(): void {
  ensureContext();
}

/*
 * Mark the start of a new reply, so the next unit uses the short first-unit cap
 * again. Does not stop audio already scheduled.
 */
export function beginTurn(): void {
  firstUnitQueued = false;
}

/* Queue text for synthesis and playback. Returns immediately. */
export function enqueue(text: string): void {
  const clean = text.trim();
  if (!clean) return;
  if (!ensureContext()) return;

  const firstMax = firstUnitQueued ? UNIT_MAX_CHARS : FIRST_UNIT_MAX_CHARS;
  const units = splitIntoUnits(clean, firstMax, UNIT_MAX_CHARS);
  if (units.length === 0) return;

  firstUnitQueued = true;
  for (const unit of units) pending.push(unit);
  void pump();
}

/*
 * Cancel everything: pending units, in-flight synthesis, and scheduled audio.
 * The context and its keepalive stay up, which is the whole point.
 */
export function stopAll(): void {
  generation += 1;
  pending = [];
  firstUnitQueued = false;

  active.forEach((src) => {
    try {
      src.stop();
    } catch {
      /* already ended */
    }
  });
  active.clear();

  if (ctx) nextStartTime = ctx.currentTime;
}

/* True while anything is queued, synthesizing, or sounding. */
export function isSpeaking(): boolean {
  return pending.length > 0 || pumping || active.size > 0;
}
