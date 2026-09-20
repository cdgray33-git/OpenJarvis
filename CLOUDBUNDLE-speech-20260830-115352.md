# OPENJARVIS CODE REVIEW BUNDLE

- marker: `openjarvis-cloudbundle-v1`
- set: `speech` - speech_router.py duplicate definitions
- generated: 2026-08-30T11:53:52
- repo root: `C:\Users\Admin\OpenJarvis`
- files in bundle: 3

You are reviewing complete source files. Every file is included in full, with authoritative 1-based line numbers in the left gutter. Nothing has been elided.

---

# THE QUESTION

BACKGROUND

This is OpenJarvis, a self-hosted assistant. The speech surface is
FastAPI. An observation recorded on 2026-08-05, NOT re-verified since,
claimed that `speech_router.py` contains THREE definitions each of
`_get_whisper`, `speech_stream_ws`, and `_transcribe_and_send`, plus a
duplicated tts_ok / tts_backend health block. The route decorators were
said to differ between copies: one registered
`@speech_router.websocket("/v1/speech/stream")` and two registered
`@speech_router.websocket("/stream")`, on a router that already carries
a `/v1/speech` prefix.

The consequence, if true, is that Python module globals resolve to the
LAST definition while FastAPI route matching takes the FIRST
registration. The running STT path would then be a mix of copies, and
any prior debugging that read one copy while the process executed
another would have produced misleading results. Several months of
isolated patches may trace back to this.

TREAT THE LINE NUMBERS ABOVE AS STALE. The file has been edited since.
Derive everything from the source in this bundle.

WHAT I NEED FROM YOU

1. Enumerate EVERY duplicated top-level definition in speech_router.py:
   function name, and the exact current line number of each occurrence.
   Include decorators, module-level constants, and any repeated block,
   not only the three names above.

2. For each duplicated function, compare the copies against each other.
   Are they byte-identical, or do they diverge? If they diverge, state
   exactly what differs. This decides whether removal is safe or whether
   behaviour would change.

3. For each duplicated ROUTE, state the fully-resolved path including the
   router prefix, and state which registration FastAPI will match first.
   Flag any path that ends up registered twice, and any path that is
   registered under two different fully-resolved URLs.

4. State, for each duplicated symbol, which definition Python module
   globals actually resolve to at import time, and therefore which copy
   executes when the symbol is called internally rather than routed to.

5. Identify any case where 3 and 4 disagree - where the routed copy and
   the internally-called copy are different objects. That is the defect
   shape I most need named.

6. Search app.py and api_routes.py for anything that registers a speech
   path or a `/v1/speech/health` route a second time, and say which
   registration wins.

7. Recommend which copy of each duplicate to KEEP, with your reasoning,
   and give me the EXACT line ranges to delete.

OUTPUT RULES

- Cite every claim as `path:line`.
- When you propose a deletion or an edit, QUOTE THE ANCHOR LINES
  VERBATIM, including leading whitespace. I patch by exact-string anchor
  and a paraphrased anchor is useless to me.
- If the 08/05 claim of triplication is WRONG, say so plainly and show
  what is actually there. A negative result is a useful result here.
- Do not write a patch script. Give me findings and anchors.

---

# SOURCE

---

## FILE: `src/openjarvis/server/speech_router.py`

- bytes: 22109
- lines: 550
- sha256: `547ACD2C3806318E9EBC9C488470FFD31E71F679EBC7D0AC1968AB9C0C433341`
- line terminator: CRLF

Line numbers below are 1-based and authoritative. Cite them.

```python
  1 | """Speech router ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â STT and TTS endpoints for OpenJarvis."""
  2 | 
  3 | from __future__ import annotations
  4 | 
  5 | import logging
  6 | 
  7 | from fastapi import APIRouter, HTTPException, Request, UploadFile, File
  8 | from fastapi.responses import Response
  9 | from pydantic import BaseModel
 10 | from fastapi.responses import StreamingResponse
 11 | 
 12 | logger = logging.getLogger(__name__)
 13 | 
 14 | speech_router = APIRouter(prefix="/v1/speech", tags=["speech"])
 15 | 
 16 | 
 17 | class SynthesizeRequest(BaseModel):
 18 |     text: str
 19 |     voice_id: str = "am_adam"
 20 |     speed: float = 0.85
 21 |     output_format: str = "wav"
 22 | 
 23 | 
 24 | @speech_router.post("/transcribe")
 25 | async def transcribe(request: Request, file: UploadFile = File(...)):
 26 |     """Transcribe uploaded audio to text using faster-whisper."""
 27 |     backend = getattr(request.app.state, "speech_backend", None)
 28 |     if backend is None:
 29 |         raise HTTPException(status_code=503, detail="Speech backend not available")
 30 | 
 31 |     audio_bytes = await file.read()
 32 |     filename = file.filename or "audio.wav"
 33 | 
 34 |     # TEMP DIAGNOSTIC: dump every uploaded clip so we can inspect it
 35 |     try:
 36 |         import os as _os, time as _time
 37 |         _dbg = _os.path.join(_os.environ.get("LOCALAPPDATA", "."), "OpenJarvis", "audio_debug")
 38 |         _os.makedirs(_dbg, exist_ok=True)
 39 |         _p = _os.path.join(_dbg, "mic_%d_%s" % (int(_time.time()), filename))
 40 |         with open(_p, "wb") as _fh:
 41 |             _fh.write(audio_bytes)
 42 |         logger.warning("MIC CAPTURE: %d bytes -> %s", len(audio_bytes), _p)
 43 |     except Exception as _e:
 44 |         logger.warning("mic capture dump failed: %s", _e)
 45 | 
 46 |     # TEMP DIAGNOSTIC: dump every uploaded clip so we can inspect it
 47 |     try:
 48 |         import os as _os, time as _time
 49 |         _dbg = _os.path.join(_os.environ.get("LOCALAPPDATA", "."), "OpenJarvis", "audio_debug")
 50 |         _os.makedirs(_dbg, exist_ok=True)
 51 |         _p = _os.path.join(_dbg, "mic_%d_%s" % (int(_time.time()), filename))
 52 |         with open(_p, "wb") as _fh:
 53 |             _fh.write(audio_bytes)
 54 |         logger.warning("MIC CAPTURE: %d bytes -> %s", len(audio_bytes), _p)
 55 |     except Exception as _e:
 56 |         logger.warning("mic capture dump failed: %s", _e)
 57 |     fmt = filename.rsplit(".", 1)[-1].lower() if "." in filename else "wav"
 58 | 
 59 |     try:
 60 |         result = backend.transcribe(audio_bytes, format=fmt)
 61 |         return {"text": result.text, "language": result.language}
 62 |     except Exception as exc:
 63 |         logger.error("Transcription failed: %s", exc)
 64 |         raise HTTPException(status_code=500, detail=str(exc))
 65 | 
 66 | 
 67 | # --- Remote TTS Backend (Kokoro on R630 / Tesla P4) ---
 68 | KOKORO_SERVER = "http://172.16.33.201:8880"
 69 | 
 70 | @speech_router.post("/synthesize")
 71 | async def synthesize(request: Request, body: SynthesizeRequest):
 72 |     """Forward Kokoro audio to the client as it arrives."""
 73 |     import httpx, time
 74 | 
 75 |     t0 = time.time()
 76 |     char_count = len(body.text)
 77 |     logger.warning("TTS START: %d chars, voice=%s", char_count, body.voice_id)
 78 | 
 79 |     async def _pump():
 80 |         first = True
 81 |         total = 0
 82 |         try:
 83 |             timeout = httpx.Timeout(60.0, connect=5.0)
 84 |             async with httpx.AsyncClient(timeout=timeout) as client:
 85 |                 async with client.stream(
 86 |                     "POST",
 87 |                     KOKORO_SERVER + "/synthesize",
 88 |                     json={
 89 |                         "text": body.text,
 90 |                         "voice": body.voice_id,
 91 |                         "speed": body.speed,
 92 |                     },
 93 |                 ) as resp:
 94 |                     resp.raise_for_status()
 95 |                     async for chunk in resp.aiter_bytes():
 96 |                         if not chunk:
 97 |                             continue
 98 |                         if first:
 99 |                             logger.warning(
100 |                                 "TTS TTFB: %.3fs (%d chars)",
101 |                                 time.time() - t0,
102 |                                 char_count,
103 |                             )
104 |                             first = False
105 |                         total += len(chunk)
106 |                         yield chunk
107 |             logger.warning(
108 |                 "TTS DONE: %.3fs, %d bytes, %d chars",
109 |                 time.time() - t0,
110 |                 total,
111 |                 char_count,
112 |             )
113 |         except Exception as exc:
114 |             logger.error("Synthesis failed: %s", exc)
115 |             raise
116 | 
117 |     return StreamingResponse(
118 |         _pump(),
119 |         media_type="audio/wav",
120 |         headers={"Cache-Control": "no-store", "X-Accel-Buffering": "no"},
121 |     )
122 | 
123 | @speech_router.get("/health")
124 | async def speech_health(request: Request):
125 |     """Check speech backend health."""
126 |     backend = getattr(request.app.state, "speech_backend", None)
127 |     stt_ok = backend is not None and backend.health()
128 | 
129 |     tts_ok = True  # Remote Kokoro service on R630 (P4)
130 | 
131 |     return {
132 |         "available": stt_ok and tts_ok,
133 |         "stt": "ok" if stt_ok else "unavailable",
134 |         "tts": "ok" if tts_ok else "unavailable",
135 |         "stt_backend": "faster-whisper",
136 |         "tts_backend": "kokoro",
137 |         "voice": "am_adam",
138 |     }
139 | 
140 |   # Silero VAD + Whisper Streaming WS
141 | import asyncio, json, logging, numpy as np, threading, time
142 | from fastapi import WebSocket, WebSocketDisconnect
143 | from faster_whisper.vad import VadOptions, get_speech_timestamps
144 | from faster_whisper import WhisperModel
145 | 
146 | log = logging.getLogger("speech.stream")
147 | 
148 | # â”€â”€ Global models (loaded once) â”€â”€
149 | _WHISPER_MODEL: WhisperModel | None = None
150 | _VAD_OPTS = VadOptions(threshold=0.5, min_speech_duration_ms=250, min_silence_duration_ms=800)
151 | _SAMPLE_RATE = 16000
152 | _FRAME_SAMPLES = 512
153 | _VAD_EVERY_N_FRAMES = 5
154 | _VAD_WINDOW_SECONDS = 2.5
155 | _VAD_WINDOW_SAMPLES = int(_SAMPLE_RATE * _VAD_WINDOW_SECONDS)
156 | _MAX_UTTERANCE_SECONDS = 30.0
157 | _OVERLAP_SECONDS = 1.0
158 | _SILENCE_TICKS_REQUIRED = 2
159 | 
160 | def _get_whisper() -> WhisperModel:
161 |     global _WHISPER_MODEL
162 |     if _WHISPER_MODEL is None:
163 |         from openjarvis.config import get_config
164 |         cfg = get_config().speech
165 |         _WHISPER_MODEL = WhisperModel(
166 |             cfg.model, device=cfg.device, compute_type=cfg.compute_type, cpu_threads=4
167 |         )
168 |         log.info("Whisper model loaded: %s/%s/%s", cfg.model, cfg.device, cfg.compute_type)
169 |     return _WHISPER_MODEL
170 | 
171 | @speech_router.websocket("/v1/speech/stream")
172 | async def speech_stream_ws(ws: WebSocket):
173 |     await ws.accept()
174 |     log.info("WS /v1/speech/stream connected")
175 | 
176 | # Silero VAD + Whisper Streaming WS
177 | import asyncio, json, logging, numpy as np, threading, time
178 | from fastapi import WebSocket, WebSocketDisconnect
179 | from faster_whisper.vad import VadOptions, get_speech_timestamps
180 | from faster_whisper import WhisperModel
181 | 
182 | log = logging.getLogger("speech.stream")
183 | 
184 | # Global models (loaded once)
185 | _WHISPER_MODEL: WhisperModel | None = None
186 | _VAD_OPTS = VadOptions(threshold=0.5, min_speech_duration_ms=250, min_silence_duration_ms=800, speech_pad_ms=400)
187 | _SAMPLE_RATE = 16000
188 | _FRAME_SAMPLES = 512
189 | _VAD_EVERY_N_FRAMES = 5
190 | _VAD_WINDOW_SECONDS = 2.5
191 | _VAD_WINDOW_SAMPLES = int(_SAMPLE_RATE * _VAD_WINDOW_SECONDS)
192 | _MAX_UTTERANCE_SECONDS = 30.0
193 | _OVERLAP_SECONDS = 1.0
194 | _SILENCE_TICKS_REQUIRED = 2
195 | 
196 | def _get_whisper() -> WhisperModel:
197 |     global _WHISPER_MODEL
198 |     if _WHISPER_MODEL is None:
199 |         from openjarvis.core.config import load_config
200 |         cfg = load_config().speech
201 |         _WHISPER_MODEL = WhisperModel(
202 |             cfg.model, device=cfg.device, compute_type=cfg.compute_type, cpu_threads=4
203 |         )
204 |         log.info("Whisper model loaded: %s/%s/%s", cfg.model, cfg.device, cfg.compute_type)
205 |     return _WHISPER_MODEL
206 | 
207 | @speech_router.websocket("/stream")
208 | async def speech_stream_ws(ws: WebSocket):
209 |     await ws.accept()
210 |     log.info("WS /v1/speech/stream connected")
211 | 
212 | # Silero VAD + Whisper Streaming WS
213 | import asyncio, json, logging, numpy as np, threading, time
214 | from fastapi import WebSocket, WebSocketDisconnect
215 | from faster_whisper.vad import VadOptions, get_speech_timestamps
216 | from faster_whisper import WhisperModel
217 | 
218 | log = logging.getLogger("speech.stream")
219 | 
220 | # Global models (loaded once)
221 | _WHISPER_MODEL: WhisperModel | None = None
222 | _VAD_OPTS = VadOptions(threshold=0.5, min_speech_duration_ms=250, min_silence_duration_ms=800, speech_pad_ms=400)
223 | _SAMPLE_RATE = 16000
224 | _FRAME_SAMPLES = 512
225 | _VAD_EVERY_N_FRAMES = 5
226 | _VAD_WINDOW_SECONDS = 2.5
227 | _VAD_WINDOW_SAMPLES = int(_SAMPLE_RATE * _VAD_WINDOW_SECONDS)
228 | _MAX_UTTERANCE_SECONDS = 30.0
229 | _OVERLAP_SECONDS = 1.0
230 | _SILENCE_TICKS_REQUIRED = 2
231 | 
232 | def _get_whisper() -> WhisperModel:
233 |     global _WHISPER_MODEL
234 |     if _WHISPER_MODEL is None:
235 |         from openjarvis.core.config import load_config
236 |         cfg = load_config().speech
237 |         _WHISPER_MODEL = WhisperModel(
238 |             cfg.model, device=cfg.device, compute_type=cfg.compute_type, cpu_threads=4
239 |         )
240 |         log.info("Whisper model loaded: %s/%s/%s", cfg.model, cfg.device, cfg.compute_type)
241 |     return _WHISPER_MODEL
242 | 
243 | @speech_router.websocket("/stream")
244 | async def speech_stream_ws(ws: WebSocket):
245 |     await ws.accept()
246 |     log.info("WS /v1/speech/stream connected")
247 |     
248 |     vad_window = np.zeros(_VAD_WINDOW_SAMPLES, dtype=np.float32)
249 |     utterance = np.zeros(0, dtype=np.float32)
250 |     frame_count = 0
251 |     silence_ticks = 0
252 |     transcribe_lock = asyncio.Lock()
253 |     
254 |     try:
255 |         while True:
256 |             msg = await ws.receive()
257 |             if msg["type"] == "websocket.disconnect":
258 |                 break
259 |             
260 |             if "bytes" in msg and msg["bytes"]:
261 |                 pcm16 = np.frombuffer(msg["bytes"], dtype=np.int16)
262 |                 if pcm16.size != _FRAME_SAMPLES:
263 |                     log.warning("Frame size %d != %d, skipping", pcm16.size, _FRAME_SAMPLES)
264 |                     continue
265 |                 f32 = (pcm16.astype(np.float32) / 32768.0)
266 |                 
267 |                 vad_window = np.roll(vad_window, -_FRAME_SAMPLES)
268 |                 vad_window[-_FRAME_SAMPLES:] = f32
269 |                 utterance = np.concatenate([utterance, f32])
270 |                 
271 |                 if len(utterance) >= _SAMPLE_RATE * _MAX_UTTERANCE_SECONDS:
272 |                     log.info("Force-cut at %.1fs", _MAX_UTTERANCE_SECONDS)
273 |                     keep = int(_SAMPLE_RATE * _OVERLAP_SECONDS)
274 |                     to_transcribe = utterance[:-keep]
275 |                     utterance = utterance[-keep:]
276 |                     asyncio.create_task(_transcribe_and_send(ws, to_transcribe, transcribe_lock))
277 |                     silence_ticks = 0
278 |                     continue
279 |                 
280 |                 frame_count += 1
281 |                 if frame_count % _VAD_EVERY_N_FRAMES != 0:
282 |                     continue
283 |                 
284 |                 try:
285 |                     segments = get_speech_timestamps(vad_window, _VAD_OPTS, sampling_rate=_SAMPLE_RATE)
286 |                 except Exception as e:
287 |                     log.error("VAD error: %s", e)
288 |                     continue
289 |                 
290 |                 if segments:
291 |                     silence_ticks = 0
292 |                 else:
293 |                     silence_ticks += 1
294 |                     if silence_ticks >= _SILENCE_TICKS_REQUIRED and len(utterance) > _SAMPLE_RATE * 0.5:
295 |                         log.info("Endpoint detected after %.2fs silence", silence_ticks * _VAD_EVERY_N_FRAMES * 0.032)
296 |                         to_transcribe = utterance.copy()
297 |                         utterance = np.zeros(0, dtype=np.float32)
298 |                         silence_ticks = 0
299 |                         asyncio.create_task(_transcribe_and_send(ws, to_transcribe, transcribe_lock))
300 |             
301 |             elif "text" in msg and msg["text"]:
302 |                 try:
303 |                     ctrl = json.loads(msg["text"])
304 |                     if ctrl.get("type") == "barge_in":
305 |                         log.info("Barge-in received")
306 |                         utterance = np.zeros(0, dtype=np.float32)
307 |                         silence_ticks = 0
308 |                         await ws.send_text(json.dumps({"type": "barge_in_ack"}))
309 |                 except json.JSONDecodeError:
310 |                     pass
311 |     
312 |     except WebSocketDisconnect:
313 |         log.info("WS disconnected")
314 |     except Exception as e:
315 |         log.exception("WS error: %s", e)
316 |     finally:
317 |         log.info("WS cleanup")
318 | 
319 | async def _transcribe_and_send(ws: WebSocket, audio: np.ndarray, lock: asyncio.Lock):
320 |     if audio.size == 0:
321 |         return
322 |     async with lock:
323 |         model = _get_whisper()
324 |         t0 = time.perf_counter()
325 |         try:
326 |             segments, info = await asyncio.to_thread(
327 |                 model.transcribe, audio, language="en", beam_size=1, vad_filter=False
328 |             )
329 |             text = " ".join(s.text for s in segments).strip()
330 |             total = time.perf_counter() - t0
331 |             if text:
332 |                 await ws.send_text(json.dumps({
333 |                     "type": "transcript",
334 |                     "text": text,
335 |                     "ttfb": round(total, 3),
336 |                     "total": round(total, 3)
337 |                 }))
338 |                 log.info("Transcript: %.3fs | %s", total, text[:80])
339 |         except Exception as e:
340 |             log.exception("Transcribe error: %s", e)
341 | 
342 |     
343 |     vad_window = np.zeros(_VAD_WINDOW_SAMPLES, dtype=np.float32)
344 |     utterance = np.zeros(0, dtype=np.float32)
345 |     frame_count = 0
346 |     silence_ticks = 0
347 |     transcribe_lock = asyncio.Lock()
348 |     
349 |     try:
350 |         while True:
351 |             msg = await ws.receive()
352 |             if msg["type"] == "websocket.disconnect":
353 |                 break
354 |             
355 |             if "bytes" in msg and msg["bytes"]:
356 |                 pcm16 = np.frombuffer(msg["bytes"], dtype=np.int16)
357 |                 if pcm16.size != _FRAME_SAMPLES:
358 |                     log.warning("Frame size %d != %d, skipping", pcm16.size, _FRAME_SAMPLES)
359 |                     continue
360 |                 f32 = (pcm16.astype(np.float32) / 32768.0)
361 |                 
362 |                 vad_window = np.roll(vad_window, -_FRAME_SAMPLES)
363 |                 vad_window[-_FRAME_SAMPLES:] = f32
364 |                 utterance = np.concatenate([utterance, f32])
365 |                 
366 |                 if len(utterance) >= _SAMPLE_RATE * _MAX_UTTERANCE_SECONDS:
367 |                     log.info("Force-cut at %.1fs", _MAX_UTTERANCE_SECONDS)
368 |                     keep = int(_SAMPLE_RATE * _OVERLAP_SECONDS)
369 |                     to_transcribe = utterance[:-keep]
370 |                     utterance = utterance[-keep:]
371 |                     asyncio.create_task(_transcribe_and_send(ws, to_transcribe, transcribe_lock))
372 |                     silence_ticks = 0
373 |                     continue
374 |                 
375 |                 frame_count += 1
376 |                 if frame_count % _VAD_EVERY_N_FRAMES != 0:
377 |                     continue
378 |                 
379 |                 try:
380 |                     segments = get_speech_timestamps(vad_window, _VAD_OPTS, sampling_rate=_SAMPLE_RATE)
381 |                 except Exception as e:
382 |                     log.error("VAD error: %s", e)
383 |                     continue
384 |                 
385 |                 if segments:
386 |                     silence_ticks = 0
387 |                 else:
388 |                     silence_ticks += 1
389 |                     if silence_ticks >= _SILENCE_TICKS_REQUIRED and len(utterance) > _SAMPLE_RATE * 0.5:
390 |                         log.info("Endpoint detected after %.2fs silence", silence_ticks * _VAD_EVERY_N_FRAMES * 0.032)
391 |                         to_transcribe = utterance.copy()
392 |                         utterance = np.zeros(0, dtype=np.float32)
393 |                         silence_ticks = 0
394 |                         asyncio.create_task(_transcribe_and_send(ws, to_transcribe, transcribe_lock))
395 |             
396 |             elif "text" in msg and msg["text"]:
397 |                 try:
398 |                     ctrl = json.loads(msg["text"])
399 |                     if ctrl.get("type") == "barge_in":
400 |                         log.info("Barge-in received")
401 |                         utterance = np.zeros(0, dtype=np.float32)
402 |                         silence_ticks = 0
403 |                         await ws.send_text(json.dumps({"type": "barge_in_ack"}))
404 |                 except json.JSONDecodeError:
405 |                     pass
406 |     
407 |     except WebSocketDisconnect:
408 |         log.info("WS disconnected")
409 |     except Exception as e:
410 |         log.exception("WS error: %s", e)
411 |     finally:
412 |         log.info("WS cleanup")
413 | 
414 | async def _transcribe_and_send(ws: WebSocket, audio: np.ndarray, lock: asyncio.Lock):
415 |     if audio.size == 0:
416 |         return
417 |     async with lock:
418 |         model = _get_whisper()
419 |         t0 = time.perf_counter()
420 |         try:
421 |             segments, info = await asyncio.to_thread(
422 |                 model.transcribe, audio, language="en", beam_size=1, vad_filter=False
423 |             )
424 |             text = " ".join(s.text for s in segments).strip()
425 |             total = time.perf_counter() - t0
426 |             if text:
427 |                 await ws.send_text(json.dumps({
428 |                     "type": "transcript",
429 |                     "text": text,
430 |                     "ttfb": round(total, 3),
431 |                     "total": round(total, 3)
432 |                 }))
433 |                 log.info("Transcript: %.3fs | %s", total, text[:80])
434 |         except Exception as e:
435 |             log.exception("Transcribe error: %s", e)
436 | 
437 |     
438 |     vad_window = np.zeros(_VAD_WINDOW_SAMPLES, dtype=np.float32)
439 |     utterance = np.zeros(0, dtype=np.float32)
440 |     frame_count = 0
441 |     silence_ticks = 0
442 |     barge_in = threading.Event()
443 |     barge_in.clear()
444 |     
445 |     try:
446 |         while True:
447 |             msg = await ws.receive()
448 |             if msg["type"] == "websocket.disconnect":
449 |                 break
450 |             
451 |             # â”€â”€ Binary PCM16 frame â”€â”€
452 |             if "bytes" in msg and msg["bytes"]:
453 |                 pcm16 = np.frombuffer(msg["bytes"], dtype=np.int16)
454 |                 if pcm16.size != _FRAME_SAMPLES:
455 |                     log.warning("Frame size %d != %d, skipping", pcm16.size, _FRAME_SAMPLES)
456 |                     continue
457 |                 f32 = (pcm16.astype(np.float32) / 32768.0)
458 |                 
459 |                 # Rolling VAD window
460 |                 vad_window = np.roll(vad_window, -_FRAME_SAMPLES)
461 |                 vad_window[-_FRAME_SAMPLES:] = f32
462 |                 
463 |                 # Accumulate utterance
464 |                 utterance = np.concatenate([utterance, f32])
465 |                 
466 |                 # Force-cut at 30s with overlap
467 |                 if len(utterance) >= _SAMPLE_RATE * _MAX_UTTERANCE_SECONDS:
468 |                     log.info("Force-cut at %.1fs", _MAX_UTTERANCE_SECONDS)
469 |                     keep = int(_SAMPLE_RATE * _OVERLAP_SECONDS)
470 |                     to_transcribe = utterance[:-keep]
471 |                     utterance = utterance[-keep:]
472 |                     asyncio.create_task(_transcribe_and_send(ws, to_transcribe))
473 |                     silence_ticks = 0
474 |                     continue
475 |                 
476 |                 frame_count += 1
477 |                 if frame_count % _VAD_EVERY_N_FRAMES != 0:
478 |                     continue
479 |                 
480 |                 # â”€â”€ VAD on fixed window â”€â”€
481 |                 try:
482 |                     segments = get_speech_timestamps(vad_window, _VAD_OPTS)
483 |                 except Exception as e:
484 |                     log.error("VAD error: %s", e)
485 |                     continue
486 |                 
487 |                 if segments:
488 |                     silence_ticks = 0
489 |                 else:
490 |                     silence_ticks += 1
491 |                     if silence_ticks >= _SILENCE_TICKS_REQUIRED and len(utterance) > _SAMPLE_RATE * 0.5:
492 |                         log.info("Endpoint detected after %.2fs silence", silence_ticks * _VAD_EVERY_N_FRAMES * 0.032)
493 |                         to_transcribe = utterance.copy()
494 |                         utterance = np.zeros(0, dtype=np.float32)
495 |                         silence_ticks = 0
496 |                         asyncio.create_task(_transcribe_and_send(ws, to_transcribe))
497 |             
498 |             # â”€â”€ JSON control messages â”€â”€
499 |             elif "text" in msg and msg["text"]:
500 |                 try:
501 |                     ctrl = json.loads(msg["text"])
502 |                     if ctrl.get("type") == "barge_in":
503 |                         log.info("Barge-in received")
504 |                         utterance = np.zeros(0, dtype=np.float32)
505 |                         silence_ticks = 0
506 |                         await ws.send_text(json.dumps({"type": "barge_in_ack"}))
507 |                 except json.JSONDecodeError:
508 |                     pass
509 |     
510 |     except WebSocketDisconnect:
511 |         log.info("WS disconnected")
512 |     except Exception as e:
513 |         log.exception("WS error: %s", e)
514 |     finally:
515 |         log.info("WS cleanup")
516 | 
517 | async def _transcribe_and_send(ws: WebSocket, audio: np.ndarray):
518 |     if audio.size == 0:
519 |         return
520 |     model = _get_whisper()
521 |     t0 = time.perf_counter()
522 |     try:
523 |         segments, info = await asyncio.to_thread(
524 |             model.transcribe, audio, language="en", beam_size=1, vad_filter=False
525 |         )
526 |         text = " ".join(s.text for s in segments).strip()
527 |         ttfb = time.perf_counter() - t0
528 |         total = ttfb
529 |         if text:
530 |             await ws.send_text(json.dumps({
531 |                 "type": "transcript",
532 |                 "text": text,
533 |                 "ttfb": round(ttfb, 3),
534 |                 "total": round(total, 3)
535 |             }))
536 |             log.info("Transcript: %.3fs | %s", total, text[:80])
537 |     except Exception as e:
538 |         log.exception("Transcribe error: %s", e)
539 | 
540 | 
541 |     tts_ok = True  # Remote Kokoro service on R630 (P4)
542 | 
543 |     return {
544 |         "available": stt_ok and tts_ok,
545 |         "stt": "ok" if stt_ok else "unavailable",
546 |         "tts": "ok" if tts_ok else "unavailable",
547 |         "stt_backend": "faster-whisper",
548 |         "tts_backend": "kokoro",
549 |         "voice": "am_adam",
550 |     }
```

---

## FILE: `src/openjarvis/server/app.py`

- bytes: 13776
- lines: 369
- sha256: `8B2A7A0DB2CF7C5D1F40A597551DEC6204FF3ED66072F6DDF3F6BC8EB5D15BCC`
- line terminator: LF

Line numbers below are 1-based and authoritative. Cite them.

```python
  1 | """FastAPI application factory for the OpenJarvis API server."""
  2 | 
  3 | from __future__ import annotations
  4 | 
  5 | import logging
  6 | import pathlib
  7 | import time
  8 | 
  9 | from fastapi import FastAPI, HTTPException
 10 | from fastapi.responses import FileResponse
 11 | from fastapi.staticfiles import StaticFiles
 12 | 
 13 | from openjarvis.server.analytics_routes import router as analytics_router
 14 | from openjarvis.server.api_routes import include_all_routes
 15 | from openjarvis.server.comparison import comparison_router
 16 | from openjarvis.server.connectors_router import create_connectors_router
 17 | from openjarvis.server.dashboard import dashboard_router
 18 | from openjarvis.server.digest_routes import create_digest_router
 19 | from openjarvis.server.research_router import router as research_router
 20 | from openjarvis.server.routes import router
 21 | from openjarvis.server.upload_router import router as upload_router
 22 | from openjarvis.server.speech_router import speech_router
 23 | 
 24 | logger = logging.getLogger(__name__)
 25 | 
 26 | 
 27 | def _restore_sendblue_bindings(app: FastAPI) -> None:
 28 |     """Restore SendBlue channel bindings from the database on startup.
 29 | 
 30 |     If a SendBlue binding was created via the Messaging tab and the server
 31 |     restarts, this ensures the ChannelBridge + DeepResearchAgent are wired
 32 |     up so incoming webhooks continue to work.
 33 |     """
 34 |     try:
 35 |         mgr = getattr(app.state, "agent_manager", None)
 36 |         if mgr is None:
 37 |             return
 38 | 
 39 |         # Check all agents for sendblue bindings
 40 |         for agent in mgr.list_agents():
 41 |             agent_id = agent.get("id", agent.get("agent_id", ""))
 42 |             bindings = mgr.list_channel_bindings(agent_id)
 43 |             for b in bindings:
 44 |                 if b.get("channel_type") != "sendblue":
 45 |                     continue
 46 |                 config = b.get("config", {})
 47 |                 api_key_id = config.get("api_key_id", "")
 48 |                 api_secret_key = config.get("api_secret_key", "")
 49 |                 from_number = config.get("from_number", "")
 50 |                 if not api_key_id or not api_secret_key:
 51 |                     continue
 52 | 
 53 |                 from openjarvis.channels.sendblue import SendBlueChannel
 54 | 
 55 |                 sb = SendBlueChannel(
 56 |                     api_key_id=api_key_id,
 57 |                     api_secret_key=api_secret_key,
 58 |                     from_number=from_number,
 59 |                 )
 60 |                 sb.connect()
 61 |                 app.state.sendblue_channel = sb
 62 | 
 63 |                 # Create ChannelBridge if none exists
 64 |                 bridge = getattr(app.state, "channel_bridge", None)
 65 |                 if bridge and hasattr(bridge, "_channels"):
 66 |                     bridge._channels["sendblue"] = sb
 67 |                 else:
 68 |                     from openjarvis.server.channel_bridge import ChannelBridge
 69 |                     from openjarvis.server.session_store import SessionStore
 70 | 
 71 |                     session_store = SessionStore()
 72 |                     engine = getattr(app.state, "engine", None)
 73 |                     dr_agent = None
 74 |                     if engine:
 75 |                         from openjarvis.server.agent_manager_routes import (
 76 |                             _build_deep_research_tools,
 77 |                         )
 78 | 
 79 |                         tools = _build_deep_research_tools(engine=engine, model="")
 80 |                         if tools:
 81 |                             from openjarvis.agents.deep_research import (
 82 |                                 DeepResearchAgent,
 83 |                             )
 84 | 
 85 |                             model_name = getattr(app.state, "model", "") or getattr(
 86 |                                 engine, "_model", ""
 87 |                             )
 88 |                             dr_agent = DeepResearchAgent(
 89 |                                 engine=engine,
 90 |                                 model=model_name,
 91 |                                 tools=tools,
 92 |                             )
 93 | 
 94 |                     bus = getattr(app.state, "bus", None)
 95 |                     if bus is None:
 96 |                         from openjarvis.core.events import EventBus
 97 | 
 98 |                         bus = EventBus()
 99 | 
100 |                     app.state.channel_bridge = ChannelBridge(
101 |                         channels={"sendblue": sb},
102 |                         session_store=session_store,
103 |                         bus=bus,
104 |                         agent_manager=mgr,
105 |                         deep_research_agent=dr_agent,
106 |                     )
107 | 
108 |                 logger.info(
109 |                     "Restored SendBlue channel binding: %s",
110 |                     from_number,
111 |                 )
112 |                 return  # Only need one SendBlue binding
113 |     except Exception as exc:
114 |         logger.debug("SendBlue binding restore skipped: %s", exc)
115 | 
116 | 
117 | # No-cache headers applied to static file responses
118 | _NO_CACHE_HEADERS = {
119 |     "Cache-Control": "no-cache, no-store, must-revalidate",
120 |     "Pragma": "no-cache",
121 |     "Expires": "0",
122 | }
123 | 
124 | 
125 | class _NoCacheStaticFiles(StaticFiles):
126 |     """StaticFiles subclass that adds no-cache headers to every response."""
127 | 
128 |     async def __call__(self, scope, receive, send):
129 |         async def _send_with_headers(message):
130 |             if message["type"] == "http.response.start":
131 |                 extra = [(k.encode(), v.encode()) for k, v in _NO_CACHE_HEADERS.items()]
132 |                 # Remove etag and last-modified
133 |                 existing = [
134 |                     (k, v)
135 |                     for k, v in message.get("headers", [])
136 |                     if k.lower() not in (b"etag", b"last-modified")
137 |                 ]
138 |                 message = {**message, "headers": existing + extra}
139 |             await send(message)
140 | 
141 |         await super().__call__(scope, receive, _send_with_headers)
142 | 
143 | 
144 | def create_app(
145 |     engine,
146 |     model: str,
147 |     *,
148 |     agent=None,
149 |     bus=None,
150 |     engine_name: str = "",
151 |     agent_name: str = "",
152 |     channel_bridge=None,
153 |     config=None,
154 |     memory_backend=None,
155 |     speech_backend=None,
156 |     agent_manager=None,
157 |     agent_scheduler=None,
158 |     api_key: str = "",
159 |     webhook_config: dict | None = None,
160 |     cors_origins: list[str] | None = None,
161 | ) -> FastAPI:
162 |     """Create and configure the FastAPI application.
163 | 
164 |     Parameters
165 |     ----------
166 |     engine:
167 |         The inference engine to use for completions.
168 |     model:
169 |         Default model name.
170 |     agent:
171 |         Optional agent instance for agent-mode completions.
172 |     bus:
173 |         Optional event bus for telemetry.
174 |     channel_bridge:
175 |         Optional channel bridge for multi-platform messaging.
176 |     config:
177 |         Optional JarvisConfig for other settings.
178 |     """
179 |     app = FastAPI(
180 |         title="OpenJarvis API",
181 |         description="OpenAI-compatible API server for OpenJarvis",
182 |         version="0.1.0",
183 |     )
184 | 
185 |     from fastapi.middleware.cors import CORSMiddleware
186 | 
187 |     _origins = (
188 |         cors_origins
189 |         if cors_origins is not None
190 |         else [
191 |             "http://localhost:5173",
192 |             "http://127.0.0.1:5173",
193 |             # Tauri 2 production webview origins:
194 |             #   macOS / Linux / iOS  -> tauri://localhost
195 |             #   Windows / Android    -> http://tauri.localhost (default),
196 |             #                           https://tauri.localhost when
197 |             #                           windows.useHttpsScheme is enabled
198 |             "tauri://localhost",
199 |             "http://tauri.localhost",
200 |             "https://tauri.localhost",
201 |         ]
202 |     )
203 |     app.add_middleware(
204 |         CORSMiddleware,
205 |         allow_origins=_origins,
206 |         allow_credentials=True,
207 |         allow_methods=["*"],
208 |         allow_headers=["*"],
209 |     )
210 | 
211 |     # Store dependencies in app state
212 |     app.state.engine = engine
213 |     app.state.model = model
214 |     app.state.agent = agent
215 |     app.state.bus = bus
216 |     app.state.engine_name = engine_name
217 |     app.state.agent_name = agent_name or (
218 |         getattr(agent, "agent_id", None) if agent else None
219 |     )
220 |     app.state.channel_bridge = channel_bridge
221 |     app.state.config = config
222 |     app.state.memory_backend = memory_backend
223 |     app.state.speech_backend = speech_backend
224 |     app.state.agent_manager = agent_manager
225 |     app.state.agent_scheduler = agent_scheduler
226 |     app.state.session_start = time.time()
227 | 
228 |     # Wire up trace store if traces are enabled
229 |     app.state.trace_store = None
230 |     try:
231 |         from openjarvis.core.config import load_config
232 |         from openjarvis.traces.store import TraceStore
233 | 
234 |         cfg = config if config is not None else load_config()
235 |         if cfg.traces.enabled:
236 |             _trace_store = TraceStore(db_path=cfg.traces.db_path)
237 |             app.state.trace_store = _trace_store
238 |             _bus = getattr(app.state, "bus", None)
239 |             if _bus is not None:
240 |                 _trace_store.subscribe_to_bus(_bus)
241 |     except Exception:
242 |         pass  # traces are optional; don't block server startup
243 | 
244 |     # Wire up external analytics if enabled (PostHog) — never block startup.
245 |     # Note: we do NOT fire app_opened here. The frontend owns that event
246 |     # because "server started" (this code path) is not the same as "user
247 |     # opened the app" — the server can run headless via cron, daemons,
248 |     # or test suites.
249 |     app.state.analytics_client = None
250 |     app.state.analytics_bridge = None
251 |     try:
252 |         from openjarvis.analytics import (
253 |             AnalyticsClient,
254 |             EventBridge,
255 |             is_analytics_enabled,
256 |         )
257 |         from openjarvis.core.config import load_config
258 | 
259 |         _cfg = config if config is not None else load_config()
260 |         if is_analytics_enabled(_cfg.analytics):
261 |             _client = AnalyticsClient(_cfg.analytics)
262 |             app.state.analytics_client = _client
263 |             _bus_ref = getattr(app.state, "bus", None)
264 |             if _bus_ref is not None:
265 |                 _bridge = EventBridge(_bus_ref, _client)
266 |                 _bridge.start()
267 |                 app.state.analytics_bridge = _bridge
268 | 
269 |             @app.on_event("shutdown")
270 |             async def _shutdown_analytics() -> None:
271 |                 bridge = getattr(app.state, "analytics_bridge", None)
272 |                 if bridge is not None:
273 |                     try:
274 |                         bridge.stop()
275 |                     except Exception:
276 |                         pass
277 |                 client = getattr(app.state, "analytics_client", None)
278 |                 if client is not None:
279 |                     try:
280 |                         client.shutdown()
281 |                     except Exception:
282 |                         pass
283 |     except Exception as _exc:
284 |         logger.debug("Analytics init skipped: %s", _exc)
285 | 
286 |     app.include_router(router)
287 |     app.include_router(dashboard_router)
288 |     app.include_router(comparison_router)
289 |     app.include_router(create_connectors_router())
290 |     app.include_router(create_digest_router())
291 |     app.include_router(upload_router)
292 |     app.include_router(speech_router)
293 |     app.include_router(research_router)
294 |     app.include_router(analytics_router)
295 |     include_all_routes(app)
296 | 
297 |     # Restore SendBlue channel bindings from database on startup
298 |     _restore_sendblue_bindings(app)
299 | 
300 |     # Add security headers middleware
301 |     try:
302 |         from openjarvis.server.middleware import create_security_middleware
303 | 
304 |         middleware_cls = create_security_middleware()
305 |         if middleware_cls is not None:
306 |             app.add_middleware(middleware_cls)
307 |     except Exception as exc:
308 |         logger.debug("Security middleware init skipped: %s", exc)
309 | 
310 |     # API key authentication middleware - disabled for Graystone Lab local network
311 |     if False:
312 |         try:
313 |             from openjarvis.server.auth_middleware import AuthMiddleware
314 | 
315 |             app.add_middleware(AuthMiddleware, api_key=api_key)
316 |         except Exception as exc:
317 |             logger.debug("Auth middleware init skipped: %s", exc)
318 | 
319 |     # Mount webhook routes (always — SendBlue may be configured dynamically)
320 |     if webhook_config:
321 |         try:
322 |             from openjarvis.server.webhook_routes import (
323 |                 create_webhook_router,
324 |             )
325 | 
326 |             webhook_router = create_webhook_router(
327 |                 bridge=channel_bridge,
328 |                 twilio_auth_token=webhook_config.get("twilio_auth_token", ""),
329 |                 bluebubbles_password=webhook_config.get("bluebubbles_password", ""),
330 |                 whatsapp_verify_token=webhook_config.get("whatsapp_verify_token", ""),
331 |                 whatsapp_app_secret=webhook_config.get("whatsapp_app_secret", ""),
332 |             )
333 |             app.include_router(webhook_router)
334 |         except Exception as exc:
335 |             logger.debug("Webhook routes init skipped: %s", exc)
336 | 
337 |     # Serve static frontend assets if the static/ directory exists
338 |     static_dir = pathlib.Path(__file__).parent / "static"
339 |     if static_dir.is_dir():
340 |         assets_dir = static_dir / "assets"
341 |         if assets_dir.is_dir():
342 |             app.mount(
343 |                 "/assets",
344 |                 _NoCacheStaticFiles(directory=assets_dir),
345 |                 name="static-assets",
346 |             )
347 | 
348 |         @app.get("/{full_path:path}")
349 |         async def spa_catch_all(full_path: str):
350 |             """Serve static files directly, fall back to index.html for SPA routes."""
351 |             # W2: never mask the API surface with the SPA index. Unmatched
352 |             # /v1/* and /api/* paths must 404, not return 200 text/html.
353 |             if full_path.startswith(("v1/", "api/")):
354 |                 raise HTTPException(status_code=404, detail="Not Found")
355 |             if full_path:
356 |                 candidate = (static_dir / full_path).resolve()
357 |                 # Path traversal prevention
358 |                 resolved_root = static_dir.resolve()
359 |                 if candidate.is_relative_to(resolved_root) and candidate.is_file():
360 |                     return FileResponse(candidate, headers=_NO_CACHE_HEADERS)
361 |             return FileResponse(
362 |                 static_dir / "index.html",
363 |                 headers=_NO_CACHE_HEADERS,
364 |             )
365 | 
366 |     return app
367 | 
368 | 
369 | __all__ = ["create_app"]
```

---

## FILE: `src/openjarvis/server/api_routes.py`

- bytes: 32776
- lines: 965
- sha256: `91EC41E64DFE73FAC8BA1233A2B0683CD57A55691A6D63C7E51C6A98055DB6D9`
- line terminator: CRLF

Line numbers below are 1-based and authoritative. Cite them.

```python
  1 | """Extended API routes for agents, workflows, memory, traces, etc."""
  2 | 
  3 | from __future__ import annotations
  4 | 
  5 | import inspect
  6 | import json
  7 | import logging
  8 | from typing import Any, Dict, List, Optional
  9 | 
 10 | from fastapi import APIRouter, HTTPException, Request, WebSocket, WebSocketDisconnect
 11 | from pydantic import BaseModel
 12 | from openjarvis.core.types import Message, Role
 13 | from openjarvis.tools.storage.context import inject_context, ContextConfig
 14 | from openjarvis.connectors.store import KnowledgeStore
 15 | 
 16 | logger = logging.getLogger(__name__)
 17 | 
 18 | # ---- Request/Response models ----
 19 | 
 20 | 
 21 | class AgentCreateRequest(BaseModel):
 22 |     agent_type: str
 23 |     tools: Optional[List[str]] = None
 24 |     agent_id: Optional[str] = None
 25 | 
 26 | 
 27 | class AgentMessageRequest(BaseModel):
 28 |     message: str
 29 | 
 30 | 
 31 | class MemoryStoreRequest(BaseModel):
 32 |     content: str
 33 |     metadata: Optional[Dict[str, Any]] = None
 34 | 
 35 | 
 36 | class MemorySearchRequest(BaseModel):
 37 |     query: str
 38 |     top_k: int = 5
 39 | 
 40 | 
 41 | class MemoryIndexRequest(BaseModel):
 42 |     path: str
 43 | 
 44 | 
 45 | class BudgetLimitsRequest(BaseModel):
 46 |     max_tokens_per_day: Optional[int] = None
 47 |     max_requests_per_hour: Optional[int] = None
 48 | 
 49 | 
 50 | class FeedbackScoreRequest(BaseModel):
 51 |     trace_id: str
 52 |     score: float
 53 |     source: str = "api"
 54 | 
 55 | 
 56 | class OptimizeRunRequest(BaseModel):
 57 |     benchmark: str
 58 |     max_trials: int = 20
 59 |     optimizer_model: str = "claude-sonnet-4-6"
 60 |     max_samples: int = 50
 61 | 
 62 | 
 63 | # ---- Agent routes ----
 64 | 
 65 | agents_router = APIRouter(prefix="/v1/agents", tags=["agents"])
 66 | 
 67 | 
 68 | @agents_router.get("")
 69 | async def list_agents(request: Request):
 70 |     """List available agent types and running agents."""
 71 |     registered = []
 72 |     try:
 73 |         import openjarvis.agents  # noqa: F401 â€” side-effect registration
 74 |         from openjarvis.core.registry import AgentRegistry
 75 | 
 76 |         for key in sorted(AgentRegistry.keys()):
 77 |             cls = AgentRegistry.get(key)
 78 |             registered.append(
 79 |                 {
 80 |                     "key": key,
 81 |                     "class": cls.__name__,
 82 |                     "accepts_tools": getattr(cls, "accepts_tools", False),
 83 |                 }
 84 |             )
 85 |     except Exception as exc:
 86 |         logger.warning("Failed to list registered agents: %s", exc)
 87 | 
 88 |     running = []
 89 |     try:
 90 |         from openjarvis.tools.agent_tools import _SPAWNED_AGENTS
 91 | 
 92 |         running = [{"id": k, **v} for k, v in _SPAWNED_AGENTS.items()]
 93 |     except ImportError:
 94 |         pass
 95 | 
 96 |     return {"registered": registered, "running": running}
 97 | 
 98 | 
 99 | @agents_router.post("")
100 | async def create_agent(req: AgentCreateRequest, request: Request):
101 |     """Spawn a new agent."""
102 |     try:
103 |         from openjarvis.tools.agent_tools import AgentSpawnTool
104 | 
105 |         tool = AgentSpawnTool()
106 |         params = {"agent_type": req.agent_type}
107 |         if req.tools:
108 |             params["tools"] = ",".join(req.tools)
109 |         if req.agent_id:
110 |             params["agent_id"] = req.agent_id
111 |         result = tool.execute(**params)
112 |         if not result.success:
113 |             raise HTTPException(status_code=400, detail=result.content)
114 |         return {
115 |             "status": "created",
116 |             "content": result.content,
117 |             "metadata": result.metadata,
118 |         }
119 |     except ImportError:
120 |         raise HTTPException(status_code=501, detail="Agent tools not available")
121 | 
122 | 
123 | @agents_router.delete("/{agent_id}")
124 | async def kill_agent(agent_id: str, request: Request):
125 |     """Kill a running agent."""
126 |     try:
127 |         from openjarvis.tools.agent_tools import AgentKillTool
128 | 
129 |         tool = AgentKillTool()
130 |         result = tool.execute(agent_id=agent_id)
131 |         if not result.success:
132 |             raise HTTPException(status_code=404, detail=result.content)
133 |         return {"status": "stopped", "agent_id": agent_id}
134 |     except ImportError:
135 |         raise HTTPException(status_code=501, detail="Agent tools not available")
136 | 
137 | 
138 | @agents_router.post("/{agent_id}/message")
139 | async def message_agent(agent_id: str, req: AgentMessageRequest, request: Request):
140 |     """Send a message to a running agent."""
141 |     try:
142 |         from openjarvis.tools.agent_tools import AgentSendTool
143 | 
144 |         tool = AgentSendTool()
145 |         result = tool.execute(agent_id=agent_id, message=req.message)
146 |         if not result.success:
147 |             raise HTTPException(status_code=404, detail=result.content)
148 |         return {"status": "sent", "content": result.content}
149 |     except ImportError:
150 |         raise HTTPException(status_code=501, detail="Agent tools not available")
151 | 
152 | 
153 | # ---- Memory routes ----
154 | 
155 | memory_router = APIRouter(prefix="/v1/memory", tags=["memory"])
156 | 
157 | 
158 | def _get_memory_backend(request: Request):
159 |     """Return the app-level memory backend, falling back to a fresh SQLiteMemory."""
160 |     backend = getattr(request.app.state, "memory_backend", None)
161 |     if backend is None:
162 |         try:
163 |             from openjarvis.tools.storage.sqlite import SQLiteMemory
164 | 
165 |             backend = SQLiteMemory()
166 |         except Exception:
167 |             return None
168 |     return backend
169 | 
170 | 
171 | @memory_router.post("/store")
172 | async def memory_store(req: MemoryStoreRequest, request: Request):
173 |     """Store content in memory."""
174 |     backend = _get_memory_backend(request)
175 |     if backend is None:
176 |         return {"status": "stored", "note": "no backend available"}
177 |     try:
178 |         backend.store(req.content, metadata=req.metadata or {})
179 |         return {"status": "stored"}
180 |     except Exception as exc:
181 |         raise HTTPException(status_code=500, detail=str(exc))
182 | 
183 | 
184 | @memory_router.post("/search")
185 | async def memory_search(req: MemorySearchRequest, request: Request):
186 |     """Search memory for relevant content."""
187 |     backend = _get_memory_backend(request)
188 |     if backend is None:
189 |         return {"results": []}
190 |     try:
191 |         results = backend.retrieve(req.query, top_k=req.top_k)
192 |         items = [
193 |             {
194 |                 "content": r.content,
195 |                 "score": getattr(r, "score", 0.0),
196 |                 "metadata": getattr(r, "metadata", {}),
197 |             }
198 |             for r in results
199 |         ]
200 |         return {"results": items}
201 |     except Exception as exc:
202 |         raise HTTPException(status_code=500, detail=str(exc))
203 | 
204 | 
205 | @memory_router.get("/stats")
206 | async def memory_stats(request: Request):
207 |     """Get memory backend statistics."""
208 |     backend = _get_memory_backend(request)
209 |     if backend is None:
210 |         return {"entries": 0, "backend": "none", "status": "not_configured"}
211 |     try:
212 |         count = backend.count() if hasattr(backend, "count") else 0
213 |         return {
214 |             "entries": count,
215 |             "total_documents": count,
216 |             "total_chunks": count,
217 |             "backend": getattr(backend, "backend_id", "unknown"),
218 |         }
219 |     except Exception as exc:
220 |         raise HTTPException(status_code=500, detail=str(exc))
221 | 
222 | 
223 | @memory_router.get("/config")
224 | async def memory_config(request: Request):
225 |     """Return current memory configuration."""
226 |     try:
227 |         config = getattr(request.app.state, "config", None)
228 |         if config is None:
229 |             from openjarvis.core.config import load_config
230 | 
231 |             config = load_config()
232 |         backend = getattr(request.app.state, "memory_backend", None)
233 |         return {
234 |             "backend_type": (
235 |                 backend.backend_id
236 |                 if backend is not None
237 |                 else config.memory.default_backend
238 |             ),
239 |             "context_top_k": config.memory.context_top_k,
240 |             "context_min_score": config.memory.context_min_score,
241 |             "context_max_tokens": config.memory.context_max_tokens,
242 |             "context_from_memory": config.agent.context_from_memory,
243 |         }
244 |     except Exception as exc:
245 |         raise HTTPException(status_code=500, detail=str(exc))
246 | 
247 | 
248 | @memory_router.post("/index")
249 | async def memory_index(req: MemoryIndexRequest, request: Request):
250 |     """Index files from a path into memory."""
251 |     try:
252 |         from pathlib import Path
253 | 
254 |         from openjarvis.tools.storage.ingest import ingest_path
255 | 
256 |         target = Path(req.path).expanduser().resolve()
257 |         if not target.exists():
258 |             raise HTTPException(status_code=404, detail=f"Path not found: {req.path}")
259 | 
260 |         backend = _get_memory_backend(request)
261 |         if backend is None:
262 |             raise HTTPException(status_code=503, detail="No memory backend available")
263 | 
264 |         chunks = ingest_path(target)
265 |         stored = 0
266 |         for chunk in chunks:
267 |             metadata = {"source": getattr(chunk, "source", str(target))}
268 |             if hasattr(chunk, "metadata") and chunk.metadata:
269 |                 metadata.update(chunk.metadata)
270 |             backend.store(chunk.content, metadata=metadata)
271 |             stored += 1
272 | 
273 |         return {"status": "indexed", "chunks_indexed": stored}
274 |     except HTTPException:
275 |         raise
276 |     except Exception as exc:
277 |         raise HTTPException(status_code=500, detail=str(exc))
278 | 
279 | 
280 | # ---- Traces routes ----
281 | 
282 | traces_router = APIRouter(prefix="/v1/traces", tags=["traces"])
283 | 
284 | 
285 | def _serialise_trace(trace) -> dict:
286 |     """Convert a Trace dataclass to a frontend-friendly dict."""
287 |     import datetime
288 |     from dataclasses import asdict
289 | 
290 |     d = asdict(trace)
291 |     d["id"] = d.pop("trace_id", "")
292 |     started = d.pop("started_at", 0.0)
293 |     d["created_at"] = (
294 |         datetime.datetime.fromtimestamp(started, tz=datetime.timezone.utc).isoformat()
295 |         if started
296 |         else None
297 |     )
298 |     dur = d.pop("total_latency_seconds", 0.0)
299 |     d["duration_ms"] = round(dur * 1000)
300 |     for step in d.get("steps", []):
301 |         st = step.get("step_type")
302 |         if hasattr(st, "value"):
303 |             step["step_type"] = st.value
304 |     return d
305 | 
306 | 
307 | @traces_router.get("")
308 | async def list_traces(request: Request, limit: int = 20):
309 |     """List recent traces."""
310 |     try:
311 |         store = getattr(request.app.state, "trace_store", None)
312 |         if store is None:
313 |             return {"traces": []}
314 |         traces = store.list_traces(limit=limit)
315 |         items = [_serialise_trace(t) for t in traces]
316 |         return {"traces": items}
317 |     except Exception as exc:
318 |         return {"traces": [], "error": str(exc)}
319 | 
320 | 
321 | @traces_router.get("/{trace_id}")
322 | async def get_trace(trace_id: str, request: Request):
323 |     """Get a specific trace by ID."""
324 |     try:
325 |         store = getattr(request.app.state, "trace_store", None)
326 |         if store is None:
327 |             raise HTTPException(status_code=404, detail="Trace not found")
328 |         trace = store.get(trace_id)
329 |         if trace is None:
330 |             raise HTTPException(status_code=404, detail="Trace not found")
331 |         return _serialise_trace(trace)
332 |     except HTTPException:
333 |         raise
334 |     except Exception as exc:
335 |         raise HTTPException(status_code=500, detail=str(exc))
336 | 
337 | 
338 | # ---- Telemetry routes ----
339 | 
340 | telemetry_router = APIRouter(prefix="/v1/telemetry", tags=["telemetry"])
341 | 
342 | 
343 | @telemetry_router.get("/stats")
344 | async def telemetry_stats(request: Request):
345 |     """Get aggregated telemetry statistics."""
346 |     try:
347 |         from dataclasses import asdict
348 | 
349 |         from openjarvis.core.config import DEFAULT_CONFIG_DIR
350 |         from openjarvis.telemetry.aggregator import TelemetryAggregator
351 | 
352 |         db_path = DEFAULT_CONFIG_DIR / "telemetry.db"
353 |         if not db_path.exists():
354 |             return {"total_requests": 0, "total_tokens": 0}
355 | 
356 |         session_start = getattr(request.app.state, "session_start", None)
357 |         agg = TelemetryAggregator(db_path)
358 |         try:
359 |             stats = agg.summary(since=session_start)
360 |             d = asdict(stats)
361 |             d.pop("per_model", None)
362 |             d.pop("per_engine", None)
363 |             d["total_requests"] = d.pop("total_calls", 0)
364 |             return d
365 |         finally:
366 |             agg.close()
367 |     except Exception as exc:
368 |         return {"error": str(exc)}
369 | 
370 | 
371 | @telemetry_router.get("/energy")
372 | async def telemetry_energy(request: Request):
373 |     """Get energy monitoring data."""
374 |     try:
375 |         from openjarvis.core.config import DEFAULT_CONFIG_DIR
376 |         from openjarvis.telemetry.aggregator import TelemetryAggregator
377 | 
378 |         db_path = DEFAULT_CONFIG_DIR / "telemetry.db"
379 |         if not db_path.exists():
380 |             return {
381 |                 "total_energy_j": 0,
382 |                 "energy_per_token_j": 0,
383 |                 "avg_power_w": 0,
384 |                 "cpu_temp_c": None,
385 |                 "gpu_temp_c": None,
386 |             }
387 | 
388 |         session_start = getattr(request.app.state, "session_start", None)
389 |         agg = TelemetryAggregator(db_path)
390 |         try:
391 |             stats = agg.summary(since=session_start)
392 |             total_energy = stats.total_energy_joules
393 |             total_tokens = stats.total_tokens
394 |             total_latency = stats.total_latency
395 |             return {
396 |                 "total_energy_j": total_energy,
397 |                 "energy_per_token_j": (
398 |                     total_energy / total_tokens if total_tokens > 0 else 0
399 |                 ),
400 |                 "avg_power_w": (
401 |                     total_energy / total_latency if total_latency > 0 else 0
402 |                 ),
403 |                 "cpu_temp_c": None,
404 |                 "gpu_temp_c": None,
405 |             }
406 |         finally:
407 |             agg.close()
408 |     except Exception as exc:
409 |         return {"error": str(exc)}
410 | 
411 | 
412 | # ---- Skills routes ----
413 | 
414 | skills_router = APIRouter(prefix="/v1/skills", tags=["skills"])
415 | 
416 | 
417 | @skills_router.get("")
418 | async def list_skills(request: Request):
419 |     """List installed skills."""
420 |     try:
421 |         from openjarvis.core.registry import SkillRegistry
422 | 
423 |         skills = []
424 |         for key in sorted(SkillRegistry.keys()):
425 |             skills.append({"name": key})
426 |         return {"skills": skills}
427 |     except Exception as exc:
428 |         logger.warning("Failed to list skills: %s", exc)
429 |         return {"skills": []}
430 | 
431 | 
432 | @skills_router.post("")
433 | async def install_skill(request: Request):
434 |     """Install a skill (placeholder)."""
435 |     return {
436 |         "status": "not_implemented",
437 |         "message": "Use TOML files in ~/.openjarvis/skills/",
438 |     }
439 | 
440 | 
441 | @skills_router.delete("/{skill_name}")
442 | async def remove_skill(skill_name: str, request: Request):
443 |     """Remove a skill (placeholder)."""
444 |     return {
445 |         "status": "not_implemented",
446 |         "message": "Skill removal not yet supported via API",
447 |     }
448 | 
449 | 
450 | # ---- Sessions routes ----
451 | 
452 | sessions_router = APIRouter(prefix="/v1/sessions", tags=["sessions"])
453 | 
454 | 
455 | @sessions_router.get("")
456 | async def list_sessions(request: Request, limit: int = 20):
457 |     """List active sessions."""
458 |     try:
459 |         from openjarvis.sessions.store import SessionStore
460 | 
461 |         store = SessionStore()
462 |         sessions = store.recent(limit=limit)
463 |         items = [s.to_dict() if hasattr(s, "to_dict") else str(s) for s in sessions]
464 |         return {"sessions": items}
465 |     except Exception as exc:
466 |         return {"sessions": [], "error": str(exc)}
467 | 
468 | 
469 | @sessions_router.get("/{session_id}")
470 | async def get_session(session_id: str, request: Request):
471 |     """Get a specific session."""
472 |     try:
473 |         from openjarvis.sessions.store import SessionStore
474 | 
475 |         store = SessionStore()
476 |         session = store.get(session_id)
477 |         if session is None:
478 |             raise HTTPException(status_code=404, detail="Session not found")
479 |         return session.to_dict() if hasattr(session, "to_dict") else {"id": session_id}
480 |     except HTTPException:
481 |         raise
482 |     except Exception as exc:
483 |         raise HTTPException(status_code=500, detail=str(exc))
484 | 
485 | 
486 | # ---- Budget routes ----
487 | 
488 | budget_router = APIRouter(prefix="/v1/budget", tags=["budget"])
489 | 
490 | _budget_limits: Dict[str, Any] = {
491 |     "max_tokens_per_day": None,
492 |     "max_requests_per_hour": None,
493 | }
494 | _budget_usage: Dict[str, int] = {
495 |     "tokens_today": 0,
496 |     "requests_this_hour": 0,
497 | }
498 | 
499 | 
500 | @budget_router.get("")
501 | async def get_budget(request: Request):
502 |     """Get current budget usage and limits."""
503 |     return {"limits": _budget_limits, "usage": _budget_usage}
504 | 
505 | 
506 | @budget_router.put("/limits")
507 | async def set_budget_limits(req: BudgetLimitsRequest, request: Request):
508 |     """Update budget limits."""
509 |     if req.max_tokens_per_day is not None:
510 |         _budget_limits["max_tokens_per_day"] = req.max_tokens_per_day
511 |     if req.max_requests_per_hour is not None:
512 |         _budget_limits["max_requests_per_hour"] = req.max_requests_per_hour
513 |     return {"status": "updated", "limits": _budget_limits}
514 | 
515 | 
516 | # ---- Prometheus metrics ----
517 | 
518 | metrics_router = APIRouter(tags=["metrics"])
519 | 
520 | 
521 | @metrics_router.get("/metrics")
522 | async def prometheus_metrics(request: Request):
523 |     """Prometheus-compatible metrics endpoint."""
524 |     try:
525 |         from openjarvis.core.config import DEFAULT_CONFIG_DIR
526 |         from openjarvis.telemetry.aggregator import TelemetryAggregator
527 | 
528 |         db_path = DEFAULT_CONFIG_DIR / "telemetry.db"
529 |         if not db_path.exists():
530 |             from starlette.responses import PlainTextResponse
531 | 
532 |             return PlainTextResponse("# no telemetry data\n", media_type="text/plain")
533 | 
534 |         agg = TelemetryAggregator(db_path)
535 |         stats = agg.summary()
536 | 
537 |         lines = [
538 |             "# HELP openjarvis_requests_total Total requests processed",
539 |             "# TYPE openjarvis_requests_total counter",
540 |             f"openjarvis_requests_total {stats.get('total_requests', 0)}",
541 |             "# HELP openjarvis_tokens_total Total tokens generated",
542 |             "# TYPE openjarvis_tokens_total counter",
543 |             f"openjarvis_tokens_total {stats.get('total_tokens', 0)}",
544 |             "# HELP openjarvis_latency_avg_ms Average latency in milliseconds",
545 |             "# TYPE openjarvis_latency_avg_ms gauge",
546 |             f"openjarvis_latency_avg_ms {stats.get('avg_latency_ms', 0)}",
547 |         ]
548 |         from starlette.responses import PlainTextResponse
549 | 
550 |         return PlainTextResponse("\n".join(lines) + "\n", media_type="text/plain")
551 |     except Exception as exc:
552 |         logger.warning("Failed to collect Prometheus metrics: %s", exc)
553 |         from starlette.responses import PlainTextResponse
554 | 
555 |         return PlainTextResponse("# No metrics available\n", media_type="text/plain")
556 | 
557 | 
558 | # ---- WebSocket streaming routes ----
559 | 
560 | websocket_router = APIRouter(tags=["websocket"])
561 | 
562 | 
563 | @websocket_router.websocket("/v1/chat/stream")
564 | async def websocket_chat_stream(websocket: WebSocket):
565 |     """Stream chat responses over a WebSocket connection.
566 | 
567 |     Accepts JSON messages of the form::
568 | 
569 |         {"message": "...", "model": "...", "agent": "..."}
570 | 
571 |     Sends back JSON chunks::
572 | 
573 |         {"type": "chunk", "content": "..."}   -- per-token streaming
574 |         {"type": "done",  "content": "..."}   -- final assembled response
575 |         {"type": "error", "detail": "..."}    -- on failure
576 |     """
577 |     await websocket.accept()
578 |     try:
579 |         while True:
580 |             raw = await websocket.receive_text()
581 |             try:
582 |                 data = json.loads(raw)
583 |             except (json.JSONDecodeError, ValueError):
584 |                 await websocket.send_json(
585 |                     {"type": "error", "detail": "Invalid JSON"},
586 |                 )
587 |                 continue
588 | 
589 |             message = data.get("message")
590 |             if not message:
591 |                 await websocket.send_json(
592 |                     {"type": "error", "detail": "Missing 'message' field"},
593 |                 )
594 |                 continue
595 | 
596 |             model = data.get("model") or getattr(
597 |                 websocket.app.state,
598 |                 "model",
599 |                 "default",
600 |             )
601 |             engine = getattr(websocket.app.state, "engine", None)
602 |             if engine is None:
603 |                 await websocket.send_json(
604 |                     {"type": "error", "detail": "No engine configured"},
605 |                 )
606 |                 continue
607 | 
608 |             user_message_obj = Message(role=Role.USER, content=message)
609 |             messages = [user_message_obj]
610 | 
611 |             # === RETRIEVAL SETUP & INJECTION ===
612 |             knowledge_store = KnowledgeStore()
613 |             context_config = ContextConfig(
614 |                 enabled=True,
615 |                 top_k=5,
616 |                 min_score=0.0,
617 |                 max_context_tokens=2048,
618 |             )
619 |             messages = inject_context(message, messages, knowledge_store, config=context_config)
620 | 
621 |             try:
622 |                 # Prefer streaming if the engine supports it
623 |                 stream_fn = getattr(engine, "stream", None)
624 |                 if stream_fn is not None and (
625 |                     inspect.isasyncgenfunction(stream_fn) or callable(stream_fn)
626 |                 ):
627 |                     full_content = ""
628 |                     try:
629 |                         gen = stream_fn(messages, model=model)
630 |                         # Handle both async and sync generators
631 |                         if inspect.isasyncgen(gen):
632 |                             async for token in gen:
633 |                                 full_content += token
634 |                                 await websocket.send_json(
635 |                                     {"type": "chunk", "content": token},
636 |                                 )
637 |                         else:
638 |                             # Sync generator â€” iterate in a thread to avoid
639 |                             # blocking the event loop
640 |                             for token in gen:
641 |                                 full_content += token
642 |                                 await websocket.send_json(
643 |                                     {"type": "chunk", "content": token},
644 |                                 )
645 |                     except TypeError:
646 |                         # stream() didn't return an iterable; fall back to
647 |                         # generate()
648 |                         result = engine.generate(messages, model=model)
649 |                         content = (
650 |                             result.get("content", "")
651 |                             if isinstance(
652 |                                 result,
653 |                                 dict,
654 |                             )
655 |                             else str(result)
656 |                         )
657 |                         full_content = content
658 |                         await websocket.send_json(
659 |                             {"type": "chunk", "content": content},
660 |                         )
661 |                     await websocket.send_json(
662 |                         {"type": "done", "content": full_content},
663 |                     )
664 |                 else:
665 |                     # No stream method â€” single-shot generate
666 |                     result = engine.generate(messages, model=model)
667 |                     content = (
668 |                         result.get("content", "")
669 |                         if isinstance(
670 |                             result,
671 |                             dict,
672 |                         )
673 |                         else str(result)
674 |                     )
675 |                     await websocket.send_json(
676 |                         {"type": "chunk", "content": content},
677 |                     )
678 |                     await websocket.send_json(
679 |                         {"type": "done", "content": content},
680 |                     )
681 |             except WebSocketDisconnect:
682 |                 raise
683 |             except Exception as exc:
684 |                 await websocket.send_json(
685 |                     {"type": "error", "detail": str(exc)},
686 |                 )
687 |     except WebSocketDisconnect:
688 |         pass  # Client disconnected â€” nothing to clean up
689 | 
690 | 
691 | # ---- Learning routes ----
692 | 
693 | learning_router = APIRouter(prefix="/v1/learning", tags=["learning"])
694 | 
695 | 
696 | @learning_router.get("/stats")
697 | async def learning_stats(request: Request):
698 |     """Return learning system statistics across all sub-policies."""
699 |     result: Dict[str, Any] = {}
700 | 
701 |     # Skill discovery
702 |     try:
703 |         from openjarvis.learning.agents.skill_discovery import SkillDiscovery
704 | 
705 |         discovery = SkillDiscovery()
706 |         result["skill_discovery"] = {
707 |             "available": True,
708 |             "discovered_count": len(discovery.discovered_skills),
709 |         }
710 |     except Exception as exc:
711 |         logger.warning("Failed to load skill discovery stats: %s", exc)
712 |         result["skill_discovery"] = {"available": False}
713 | 
714 |     return result
715 | 
716 | 
717 | @learning_router.get("/policy")
718 | async def learning_policy(request: Request):
719 |     """Return current routing policy configuration."""
720 |     result: Dict[str, Any] = {}
721 | 
722 |     # Load config and extract learning section
723 |     try:
724 |         from openjarvis.core.config import load_config
725 | 
726 |         config = load_config()
727 |         lc = config.learning
728 |         result["enabled"] = lc.enabled
729 |         result["update_interval"] = lc.update_interval
730 |         result["auto_update"] = lc.auto_update
731 |         result["routing"] = {
732 |             "policy": lc.routing.policy,
733 |             "min_samples": lc.routing.min_samples,
734 |         }
735 |         result["intelligence"] = {
736 |             "policy": lc.intelligence.policy,
737 |         }
738 |         result["agent"] = {
739 |             "policy": lc.agent.policy,
740 |         }
741 |         result["metrics"] = {
742 |             "accuracy_weight": lc.metrics.accuracy_weight,
743 |             "latency_weight": lc.metrics.latency_weight,
744 |             "cost_weight": lc.metrics.cost_weight,
745 |             "efficiency_weight": lc.metrics.efficiency_weight,
746 |         }
747 |     except Exception as exc:
748 |         logger.warning("Failed to load learning config: %s", exc)
749 |         result["enabled"] = False
750 |         result["routing"] = {"policy": "heuristic", "min_samples": 5}
751 |         result["intelligence"] = {"policy": "none"}
752 |         result["agent"] = {"policy": "none"}
753 |         result["metrics"] = {}
754 | 
755 |     return result
756 | 
757 | 
758 | # ---- Speech routes ----
759 | 
760 | speech_router = APIRouter(prefix="/v1/speech", tags=["speech"])
761 | 
762 | 
763 | @speech_router.post("/transcribe")
764 | async def transcribe_speech(request: Request):
765 |     """Transcribe uploaded audio to text."""
766 |     backend = getattr(request.app.state, "speech_backend", None)
767 |     if backend is None:
768 |         raise HTTPException(status_code=501, detail="Speech backend not configured")
769 | 
770 |     form = await request.form()
771 |     audio_file = form.get("file")
772 |     if audio_file is None:
773 |         raise HTTPException(status_code=400, detail="Missing 'file' field")
774 | 
775 |     audio_bytes = await audio_file.read()
776 |     language = form.get("language")
777 | 
778 |     # Detect format from filename
779 |     filename = getattr(audio_file, "filename", "audio.wav")
780 |     ext = filename.rsplit(".", 1)[-1] if "." in filename else "wav"
781 | 
782 |     result = backend.transcribe(audio_bytes, format=ext, language=language or None)
783 |     return {
784 |         "text": result.text,
785 |         "language": result.language,
786 |         "confidence": result.confidence,
787 |         "duration_seconds": result.duration_seconds,
788 |     }
789 | 
790 | 
791 | @speech_router.get("/health")
792 | async def speech_health(request: Request):
793 |     """Check if a speech backend is available."""
794 |     backend = getattr(request.app.state, "speech_backend", None)
795 |     if backend is None:
796 |         return {"available": False, "reason": "No speech backend configured"}
797 |     return {
798 |         "available": backend.health(),
799 |         "backend": backend.backend_id,
800 |     }
801 | 
802 | 
803 | # ---- Feedback routes ----
804 | 
805 | feedback_router = APIRouter(prefix="/v1/feedback", tags=["feedback"])
806 | 
807 | 
808 | @feedback_router.post("")
809 | async def submit_feedback(req: FeedbackScoreRequest, request: Request):
810 |     """Submit feedback for a trace."""
811 |     try:
812 |         from openjarvis.core.config import DEFAULT_CONFIG_DIR
813 |         from openjarvis.traces.store import TraceStore
814 | 
815 |         db_path = DEFAULT_CONFIG_DIR / "traces.db"
816 |         if not db_path.exists():
817 |             raise HTTPException(status_code=404, detail="No trace database")
818 | 
819 |         store = TraceStore(db_path)
820 |         updated = store.update_feedback(req.trace_id, req.score)
821 |         store.close()
822 | 
823 |         if not updated:
824 |             raise HTTPException(
825 |                 status_code=404, detail=f"Trace '{req.trace_id}' not found"
826 |             )
827 |         return {"status": "recorded", "trace_id": req.trace_id}
828 |     except HTTPException:
829 |         raise
830 |     except Exception as exc:
831 |         raise HTTPException(status_code=500, detail=str(exc))
832 | 
833 | 
834 | @feedback_router.get("/stats")
835 | async def feedback_stats(request: Request):
836 |     """Get feedback statistics."""
837 |     return {"total": 0, "mean_score": 0.0}
838 | 
839 | 
840 | # ---- Optimize routes ----
841 | 
842 | optimize_router = APIRouter(prefix="/v1/optimize", tags=["optimize"])
843 | 
844 | 
845 | @optimize_router.get("/runs")
846 | async def list_optimize_runs(request: Request):
847 |     """List optimization runs."""
848 |     try:
849 |         from openjarvis.core.config import DEFAULT_CONFIG_DIR
850 |         from openjarvis.learning.optimize.store import OptimizationStore
851 | 
852 |         db_path = DEFAULT_CONFIG_DIR / "optimize.db"
853 |         if not db_path.exists():
854 |             return {"runs": []}
855 | 
856 |         store = OptimizationStore(db_path)
857 |         runs = store.list_runs()
858 |         store.close()
859 |         return {"runs": runs}
860 |     except Exception as exc:
861 |         logger.warning("Failed to list optimization runs: %s", exc)
862 |         return {"runs": []}
863 | 
864 | 
865 | @optimize_router.get("/runs/{run_id}")
866 | async def get_optimize_run(run_id: str, request: Request):
867 |     """Get optimization run details."""
868 |     try:
869 |         from openjarvis.core.config import DEFAULT_CONFIG_DIR
870 |         from openjarvis.learning.optimize.store import OptimizationStore
871 | 
872 |         db_path = DEFAULT_CONFIG_DIR / "optimize.db"
873 |         if not db_path.exists():
874 |             return {"run_id": run_id, "status": "not_found"}
875 | 
876 |         store = OptimizationStore(db_path)
877 |         run = store.get_run(run_id)
878 |         store.close()
879 | 
880 |         if run is None:
881 |             return {"run_id": run_id, "status": "not_found"}
882 | 
883 |         return {
884 |             "run_id": run.run_id,
885 |             "status": run.status,
886 |             "benchmark": run.benchmark,
887 |             "trials": len(run.trials),
888 |             "best_trial_id": (run.best_trial.trial_id if run.best_trial else None),
889 |         }
890 |     except Exception as exc:
891 |         logger.warning("Failed to get optimization run %s: %s", run_id, exc)
892 |         return {"run_id": run_id, "status": "not_found"}
893 | 
894 | 
895 | @optimize_router.post("/runs")
896 | async def start_optimize_run(req: OptimizeRunRequest, request: Request):
897 |     """Start a new optimization run."""
898 |     return {"status": "started", "run_id": "placeholder"}
899 | 
900 | 
901 | def include_all_routes(app) -> None:
902 |     """Include all extended API routers in a FastAPI app."""
903 |     app.include_router(agents_router)
904 |     app.include_router(memory_router)
905 |     app.include_router(traces_router)
906 |     app.include_router(telemetry_router)
907 |     app.include_router(skills_router)
908 |     app.include_router(sessions_router)
909 |     app.include_router(budget_router)
910 |     app.include_router(metrics_router)
911 |     app.include_router(websocket_router)
912 |     app.include_router(learning_router)
913 |     app.include_router(speech_router)
914 |     app.include_router(feedback_router)
915 |     app.include_router(optimize_router)
916 | 
917 |     # Agent Manager routes (if available)
918 |     try:
919 |         if hasattr(app.state, "agent_manager") and app.state.agent_manager:
920 |             from openjarvis.server.agent_manager_routes import (  # noqa: PLC0415
921 |                 create_agent_manager_router,
922 |             )
923 | 
924 |             (
925 |                 agents_r,
926 |                 templates_r,
927 |                 global_r,
928 |                 tools_r,
929 |                 sendblue_r,
930 |             ) = create_agent_manager_router(app.state.agent_manager)
931 |             app.include_router(agents_r)
932 |             app.include_router(templates_r)
933 |             app.include_router(global_r)
934 |             app.include_router(tools_r)
935 |             app.include_router(sendblue_r)
936 |     except ImportError:
937 |         pass
938 | 
939 |     # WebSocket bridge for real-time agent events
940 |     try:
941 |         from openjarvis.core.events import get_event_bus
942 |         from openjarvis.server.ws_bridge import create_ws_router
943 | 
944 |         ws_router = create_ws_router(getattr(app.state, "bus", None) or get_event_bus())  # openjarvis-ws-bus-v1
945 |         app.include_router(ws_router)
946 |     except Exception:
947 |         logger.debug("WebSocket bridge not available", exc_info=True)
948 | 
949 | 
950 | __all__ = [
951 |     "include_all_routes",
952 |     "agents_router",
953 |     "memory_router",
954 |     "traces_router",
955 |     "telemetry_router",
956 |     "skills_router",
957 |     "sessions_router",
958 |     "budget_router",
959 |     "metrics_router",
960 |     "websocket_router",
961 |     "learning_router",
962 |     "speech_router",
963 |     "feedback_router",
964 |     "optimize_router",
965 | ]
```

---

# MANIFEST

| file | found | bytes | lines | sha256 |
|---|---|---|---|---|
| `src/openjarvis/server/speech_router.py` | yes | 22109 | 550 | `547ACD2C3806318E...` |
| `src/openjarvis/server/app.py` | yes | 13776 | 369 | `8B2A7A0DB2CF7C5D...` |
| `src/openjarvis/server/api_routes.py` | yes | 32776 | 965 | `91EC41E64DFE73FA...` |

These hashes pin the exact bytes you reviewed. If a later patch is built against different bytes, the mismatch is detectable.

