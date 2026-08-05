"""Speech router ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â STT and TTS endpoints for OpenJarvis."""

from __future__ import annotations

import logging

from fastapi import APIRouter, HTTPException, Request, UploadFile, File
from fastapi.responses import Response
from pydantic import BaseModel
from fastapi.responses import StreamingResponse

logger = logging.getLogger(__name__)

speech_router = APIRouter(prefix="/v1/speech", tags=["speech"])


class SynthesizeRequest(BaseModel):
    text: str
    voice_id: str = "am_adam"
    speed: float = 0.85
    output_format: str = "wav"


@speech_router.post("/transcribe")
async def transcribe(request: Request, file: UploadFile = File(...)):
    """Transcribe uploaded audio to text using faster-whisper."""
    backend = getattr(request.app.state, "speech_backend", None)
    if backend is None:
        raise HTTPException(status_code=503, detail="Speech backend not available")

    audio_bytes = await file.read()
    filename = file.filename or "audio.wav"

    # TEMP DIAGNOSTIC: dump every uploaded clip so we can inspect it
    try:
        import os as _os, time as _time
        _dbg = _os.path.join(_os.environ.get("LOCALAPPDATA", "."), "OpenJarvis", "audio_debug")
        _os.makedirs(_dbg, exist_ok=True)
        _p = _os.path.join(_dbg, "mic_%d_%s" % (int(_time.time()), filename))
        with open(_p, "wb") as _fh:
            _fh.write(audio_bytes)
        logger.warning("MIC CAPTURE: %d bytes -> %s", len(audio_bytes), _p)
    except Exception as _e:
        logger.warning("mic capture dump failed: %s", _e)

    # TEMP DIAGNOSTIC: dump every uploaded clip so we can inspect it
    try:
        import os as _os, time as _time
        _dbg = _os.path.join(_os.environ.get("LOCALAPPDATA", "."), "OpenJarvis", "audio_debug")
        _os.makedirs(_dbg, exist_ok=True)
        _p = _os.path.join(_dbg, "mic_%d_%s" % (int(_time.time()), filename))
        with open(_p, "wb") as _fh:
            _fh.write(audio_bytes)
        logger.warning("MIC CAPTURE: %d bytes -> %s", len(audio_bytes), _p)
    except Exception as _e:
        logger.warning("mic capture dump failed: %s", _e)
    fmt = filename.rsplit(".", 1)[-1].lower() if "." in filename else "wav"

    try:
        result = backend.transcribe(audio_bytes, format=fmt)
        return {"text": result.text, "language": result.language}
    except Exception as exc:
        logger.error("Transcription failed: %s", exc)
        raise HTTPException(status_code=500, detail=str(exc))


# --- Remote TTS Backend (Kokoro on R630 / Tesla P4) ---
KOKORO_SERVER = "http://172.16.33.201:8880"

@speech_router.post("/synthesize")
async def synthesize(request: Request, body: SynthesizeRequest):
    """Forward Kokoro audio to the client as it arrives."""
    import httpx, time

    t0 = time.time()
    char_count = len(body.text)
    logger.warning("TTS START: %d chars, voice=%s", char_count, body.voice_id)

    async def _pump():
        first = True
        total = 0
        try:
            timeout = httpx.Timeout(60.0, connect=5.0)
            async with httpx.AsyncClient(timeout=timeout) as client:
                async with client.stream(
                    "POST",
                    KOKORO_SERVER + "/synthesize",
                    json={
                        "text": body.text,
                        "voice": body.voice_id,
                        "speed": body.speed,
                    },
                ) as resp:
                    resp.raise_for_status()
                    async for chunk in resp.aiter_bytes():
                        if not chunk:
                            continue
                        if first:
                            logger.warning(
                                "TTS TTFB: %.3fs (%d chars)",
                                time.time() - t0,
                                char_count,
                            )
                            first = False
                        total += len(chunk)
                        yield chunk
            logger.warning(
                "TTS DONE: %.3fs, %d bytes, %d chars",
                time.time() - t0,
                total,
                char_count,
            )
        except Exception as exc:
            logger.error("Synthesis failed: %s", exc)
            raise

    return StreamingResponse(
        _pump(),
        media_type="audio/wav",
        headers={"Cache-Control": "no-store", "X-Accel-Buffering": "no"},
    )

@speech_router.get("/health")
async def speech_health(request: Request):
    """Check speech backend health."""
    backend = getattr(request.app.state, "speech_backend", None)
    stt_ok = backend is not None and backend.health()

    tts_ok = True  # Remote Kokoro service on R630 (P4)

    return {
        "available": stt_ok and tts_ok,
        "stt": "ok" if stt_ok else "unavailable",
        "tts": "ok" if tts_ok else "unavailable",
        "stt_backend": "faster-whisper",
        "tts_backend": "kokoro",
        "voice": "am_adam",
    }

  # Silero VAD + Whisper Streaming WS
import asyncio, json, logging, numpy as np, threading, time
from fastapi import WebSocket, WebSocketDisconnect
from faster_whisper.vad import VadOptions, get_speech_timestamps
from faster_whisper import WhisperModel

log = logging.getLogger("speech.stream")

# â”€â”€ Global models (loaded once) â”€â”€
_WHISPER_MODEL: WhisperModel | None = None
_VAD_OPTS = VadOptions(threshold=0.5, min_speech_duration_ms=250, min_silence_duration_ms=800)
_SAMPLE_RATE = 16000
_FRAME_SAMPLES = 512
_VAD_EVERY_N_FRAMES = 5
_VAD_WINDOW_SECONDS = 2.5
_VAD_WINDOW_SAMPLES = int(_SAMPLE_RATE * _VAD_WINDOW_SECONDS)
_MAX_UTTERANCE_SECONDS = 30.0
_OVERLAP_SECONDS = 1.0
_SILENCE_TICKS_REQUIRED = 2

def _get_whisper() -> WhisperModel:
    global _WHISPER_MODEL
    if _WHISPER_MODEL is None:
        from openjarvis.config import get_config
        cfg = get_config().speech
        _WHISPER_MODEL = WhisperModel(
            cfg.model, device=cfg.device, compute_type=cfg.compute_type, cpu_threads=4
        )
        log.info("Whisper model loaded: %s/%s/%s", cfg.model, cfg.device, cfg.compute_type)
    return _WHISPER_MODEL

@speech_router.websocket("/v1/speech/stream")
async def speech_stream_ws(ws: WebSocket):
    await ws.accept()
    log.info("WS /v1/speech/stream connected")

# Silero VAD + Whisper Streaming WS
import asyncio, json, logging, numpy as np, threading, time
from fastapi import WebSocket, WebSocketDisconnect
from faster_whisper.vad import VadOptions, get_speech_timestamps
from faster_whisper import WhisperModel

log = logging.getLogger("speech.stream")

# Global models (loaded once)
_WHISPER_MODEL: WhisperModel | None = None
_VAD_OPTS = VadOptions(threshold=0.5, min_speech_duration_ms=250, min_silence_duration_ms=800, speech_pad_ms=400)
_SAMPLE_RATE = 16000
_FRAME_SAMPLES = 512
_VAD_EVERY_N_FRAMES = 5
_VAD_WINDOW_SECONDS = 2.5
_VAD_WINDOW_SAMPLES = int(_SAMPLE_RATE * _VAD_WINDOW_SECONDS)
_MAX_UTTERANCE_SECONDS = 30.0
_OVERLAP_SECONDS = 1.0
_SILENCE_TICKS_REQUIRED = 2

def _get_whisper() -> WhisperModel:
    global _WHISPER_MODEL
    if _WHISPER_MODEL is None:
        from openjarvis.core.config import load_config
        cfg = load_config().speech
        _WHISPER_MODEL = WhisperModel(
            cfg.model, device=cfg.device, compute_type=cfg.compute_type, cpu_threads=4
        )
        log.info("Whisper model loaded: %s/%s/%s", cfg.model, cfg.device, cfg.compute_type)
    return _WHISPER_MODEL

@speech_router.websocket("/stream")
async def speech_stream_ws(ws: WebSocket):
    await ws.accept()
    log.info("WS /v1/speech/stream connected")

# Silero VAD + Whisper Streaming WS
import asyncio, json, logging, numpy as np, threading, time
from fastapi import WebSocket, WebSocketDisconnect
from faster_whisper.vad import VadOptions, get_speech_timestamps
from faster_whisper import WhisperModel

log = logging.getLogger("speech.stream")

# Global models (loaded once)
_WHISPER_MODEL: WhisperModel | None = None
_VAD_OPTS = VadOptions(threshold=0.5, min_speech_duration_ms=250, min_silence_duration_ms=800, speech_pad_ms=400)
_SAMPLE_RATE = 16000
_FRAME_SAMPLES = 512
_VAD_EVERY_N_FRAMES = 5
_VAD_WINDOW_SECONDS = 2.5
_VAD_WINDOW_SAMPLES = int(_SAMPLE_RATE * _VAD_WINDOW_SECONDS)
_MAX_UTTERANCE_SECONDS = 30.0
_OVERLAP_SECONDS = 1.0
_SILENCE_TICKS_REQUIRED = 2

def _get_whisper() -> WhisperModel:
    global _WHISPER_MODEL
    if _WHISPER_MODEL is None:
        from openjarvis.core.config import load_config
        cfg = load_config().speech
        _WHISPER_MODEL = WhisperModel(
            cfg.model, device=cfg.device, compute_type=cfg.compute_type, cpu_threads=4
        )
        log.info("Whisper model loaded: %s/%s/%s", cfg.model, cfg.device, cfg.compute_type)
    return _WHISPER_MODEL

@speech_router.websocket("/stream")
async def speech_stream_ws(ws: WebSocket):
    await ws.accept()
    log.info("WS /v1/speech/stream connected")
    
    vad_window = np.zeros(_VAD_WINDOW_SAMPLES, dtype=np.float32)
    utterance = np.zeros(0, dtype=np.float32)
    frame_count = 0
    silence_ticks = 0
    transcribe_lock = asyncio.Lock()
    
    try:
        while True:
            msg = await ws.receive()
            if msg["type"] == "websocket.disconnect":
                break
            
            if "bytes" in msg and msg["bytes"]:
                pcm16 = np.frombuffer(msg["bytes"], dtype=np.int16)
                if pcm16.size != _FRAME_SAMPLES:
                    log.warning("Frame size %d != %d, skipping", pcm16.size, _FRAME_SAMPLES)
                    continue
                f32 = (pcm16.astype(np.float32) / 32768.0)
                
                vad_window = np.roll(vad_window, -_FRAME_SAMPLES)
                vad_window[-_FRAME_SAMPLES:] = f32
                utterance = np.concatenate([utterance, f32])
                
                if len(utterance) >= _SAMPLE_RATE * _MAX_UTTERANCE_SECONDS:
                    log.info("Force-cut at %.1fs", _MAX_UTTERANCE_SECONDS)
                    keep = int(_SAMPLE_RATE * _OVERLAP_SECONDS)
                    to_transcribe = utterance[:-keep]
                    utterance = utterance[-keep:]
                    asyncio.create_task(_transcribe_and_send(ws, to_transcribe, transcribe_lock))
                    silence_ticks = 0
                    continue
                
                frame_count += 1
                if frame_count % _VAD_EVERY_N_FRAMES != 0:
                    continue
                
                try:
                    segments = get_speech_timestamps(vad_window, _VAD_OPTS, sampling_rate=_SAMPLE_RATE)
                except Exception as e:
                    log.error("VAD error: %s", e)
                    continue
                
                if segments:
                    silence_ticks = 0
                else:
                    silence_ticks += 1
                    if silence_ticks >= _SILENCE_TICKS_REQUIRED and len(utterance) > _SAMPLE_RATE * 0.5:
                        log.info("Endpoint detected after %.2fs silence", silence_ticks * _VAD_EVERY_N_FRAMES * 0.032)
                        to_transcribe = utterance.copy()
                        utterance = np.zeros(0, dtype=np.float32)
                        silence_ticks = 0
                        asyncio.create_task(_transcribe_and_send(ws, to_transcribe, transcribe_lock))
            
            elif "text" in msg and msg["text"]:
                try:
                    ctrl = json.loads(msg["text"])
                    if ctrl.get("type") == "barge_in":
                        log.info("Barge-in received")
                        utterance = np.zeros(0, dtype=np.float32)
                        silence_ticks = 0
                        await ws.send_text(json.dumps({"type": "barge_in_ack"}))
                except json.JSONDecodeError:
                    pass
    
    except WebSocketDisconnect:
        log.info("WS disconnected")
    except Exception as e:
        log.exception("WS error: %s", e)
    finally:
        log.info("WS cleanup")

async def _transcribe_and_send(ws: WebSocket, audio: np.ndarray, lock: asyncio.Lock):
    if audio.size == 0:
        return
    async with lock:
        model = _get_whisper()
        t0 = time.perf_counter()
        try:
            segments, info = await asyncio.to_thread(
                model.transcribe, audio, language="en", beam_size=1, vad_filter=False
            )
            text = " ".join(s.text for s in segments).strip()
            total = time.perf_counter() - t0
            if text:
                await ws.send_text(json.dumps({
                    "type": "transcript",
                    "text": text,
                    "ttfb": round(total, 3),
                    "total": round(total, 3)
                }))
                log.info("Transcript: %.3fs | %s", total, text[:80])
        except Exception as e:
            log.exception("Transcribe error: %s", e)

    
    vad_window = np.zeros(_VAD_WINDOW_SAMPLES, dtype=np.float32)
    utterance = np.zeros(0, dtype=np.float32)
    frame_count = 0
    silence_ticks = 0
    transcribe_lock = asyncio.Lock()
    
    try:
        while True:
            msg = await ws.receive()
            if msg["type"] == "websocket.disconnect":
                break
            
            if "bytes" in msg and msg["bytes"]:
                pcm16 = np.frombuffer(msg["bytes"], dtype=np.int16)
                if pcm16.size != _FRAME_SAMPLES:
                    log.warning("Frame size %d != %d, skipping", pcm16.size, _FRAME_SAMPLES)
                    continue
                f32 = (pcm16.astype(np.float32) / 32768.0)
                
                vad_window = np.roll(vad_window, -_FRAME_SAMPLES)
                vad_window[-_FRAME_SAMPLES:] = f32
                utterance = np.concatenate([utterance, f32])
                
                if len(utterance) >= _SAMPLE_RATE * _MAX_UTTERANCE_SECONDS:
                    log.info("Force-cut at %.1fs", _MAX_UTTERANCE_SECONDS)
                    keep = int(_SAMPLE_RATE * _OVERLAP_SECONDS)
                    to_transcribe = utterance[:-keep]
                    utterance = utterance[-keep:]
                    asyncio.create_task(_transcribe_and_send(ws, to_transcribe, transcribe_lock))
                    silence_ticks = 0
                    continue
                
                frame_count += 1
                if frame_count % _VAD_EVERY_N_FRAMES != 0:
                    continue
                
                try:
                    segments = get_speech_timestamps(vad_window, _VAD_OPTS, sampling_rate=_SAMPLE_RATE)
                except Exception as e:
                    log.error("VAD error: %s", e)
                    continue
                
                if segments:
                    silence_ticks = 0
                else:
                    silence_ticks += 1
                    if silence_ticks >= _SILENCE_TICKS_REQUIRED and len(utterance) > _SAMPLE_RATE * 0.5:
                        log.info("Endpoint detected after %.2fs silence", silence_ticks * _VAD_EVERY_N_FRAMES * 0.032)
                        to_transcribe = utterance.copy()
                        utterance = np.zeros(0, dtype=np.float32)
                        silence_ticks = 0
                        asyncio.create_task(_transcribe_and_send(ws, to_transcribe, transcribe_lock))
            
            elif "text" in msg and msg["text"]:
                try:
                    ctrl = json.loads(msg["text"])
                    if ctrl.get("type") == "barge_in":
                        log.info("Barge-in received")
                        utterance = np.zeros(0, dtype=np.float32)
                        silence_ticks = 0
                        await ws.send_text(json.dumps({"type": "barge_in_ack"}))
                except json.JSONDecodeError:
                    pass
    
    except WebSocketDisconnect:
        log.info("WS disconnected")
    except Exception as e:
        log.exception("WS error: %s", e)
    finally:
        log.info("WS cleanup")

async def _transcribe_and_send(ws: WebSocket, audio: np.ndarray, lock: asyncio.Lock):
    if audio.size == 0:
        return
    async with lock:
        model = _get_whisper()
        t0 = time.perf_counter()
        try:
            segments, info = await asyncio.to_thread(
                model.transcribe, audio, language="en", beam_size=1, vad_filter=False
            )
            text = " ".join(s.text for s in segments).strip()
            total = time.perf_counter() - t0
            if text:
                await ws.send_text(json.dumps({
                    "type": "transcript",
                    "text": text,
                    "ttfb": round(total, 3),
                    "total": round(total, 3)
                }))
                log.info("Transcript: %.3fs | %s", total, text[:80])
        except Exception as e:
            log.exception("Transcribe error: %s", e)

    
    vad_window = np.zeros(_VAD_WINDOW_SAMPLES, dtype=np.float32)
    utterance = np.zeros(0, dtype=np.float32)
    frame_count = 0
    silence_ticks = 0
    barge_in = threading.Event()
    barge_in.clear()
    
    try:
        while True:
            msg = await ws.receive()
            if msg["type"] == "websocket.disconnect":
                break
            
            # â”€â”€ Binary PCM16 frame â”€â”€
            if "bytes" in msg and msg["bytes"]:
                pcm16 = np.frombuffer(msg["bytes"], dtype=np.int16)
                if pcm16.size != _FRAME_SAMPLES:
                    log.warning("Frame size %d != %d, skipping", pcm16.size, _FRAME_SAMPLES)
                    continue
                f32 = (pcm16.astype(np.float32) / 32768.0)
                
                # Rolling VAD window
                vad_window = np.roll(vad_window, -_FRAME_SAMPLES)
                vad_window[-_FRAME_SAMPLES:] = f32
                
                # Accumulate utterance
                utterance = np.concatenate([utterance, f32])
                
                # Force-cut at 30s with overlap
                if len(utterance) >= _SAMPLE_RATE * _MAX_UTTERANCE_SECONDS:
                    log.info("Force-cut at %.1fs", _MAX_UTTERANCE_SECONDS)
                    keep = int(_SAMPLE_RATE * _OVERLAP_SECONDS)
                    to_transcribe = utterance[:-keep]
                    utterance = utterance[-keep:]
                    asyncio.create_task(_transcribe_and_send(ws, to_transcribe))
                    silence_ticks = 0
                    continue
                
                frame_count += 1
                if frame_count % _VAD_EVERY_N_FRAMES != 0:
                    continue
                
                # â”€â”€ VAD on fixed window â”€â”€
                try:
                    segments = get_speech_timestamps(vad_window, _VAD_OPTS)
                except Exception as e:
                    log.error("VAD error: %s", e)
                    continue
                
                if segments:
                    silence_ticks = 0
                else:
                    silence_ticks += 1
                    if silence_ticks >= _SILENCE_TICKS_REQUIRED and len(utterance) > _SAMPLE_RATE * 0.5:
                        log.info("Endpoint detected after %.2fs silence", silence_ticks * _VAD_EVERY_N_FRAMES * 0.032)
                        to_transcribe = utterance.copy()
                        utterance = np.zeros(0, dtype=np.float32)
                        silence_ticks = 0
                        asyncio.create_task(_transcribe_and_send(ws, to_transcribe))
            
            # â”€â”€ JSON control messages â”€â”€
            elif "text" in msg and msg["text"]:
                try:
                    ctrl = json.loads(msg["text"])
                    if ctrl.get("type") == "barge_in":
                        log.info("Barge-in received")
                        utterance = np.zeros(0, dtype=np.float32)
                        silence_ticks = 0
                        await ws.send_text(json.dumps({"type": "barge_in_ack"}))
                except json.JSONDecodeError:
                    pass
    
    except WebSocketDisconnect:
        log.info("WS disconnected")
    except Exception as e:
        log.exception("WS error: %s", e)
    finally:
        log.info("WS cleanup")

async def _transcribe_and_send(ws: WebSocket, audio: np.ndarray):
    if audio.size == 0:
        return
    model = _get_whisper()
    t0 = time.perf_counter()
    try:
        segments, info = await asyncio.to_thread(
            model.transcribe, audio, language="en", beam_size=1, vad_filter=False
        )
        text = " ".join(s.text for s in segments).strip()
        ttfb = time.perf_counter() - t0
        total = ttfb
        if text:
            await ws.send_text(json.dumps({
                "type": "transcript",
                "text": text,
                "ttfb": round(ttfb, 3),
                "total": round(total, 3)
            }))
            log.info("Transcript: %.3fs | %s", total, text[:80])
    except Exception as e:
        log.exception("Transcribe error: %s", e)


    tts_ok = True  # Remote Kokoro service on R630 (P4)

    return {
        "available": stt_ok and tts_ok,
        "stt": "ok" if stt_ok else "unavailable",
        "tts": "ok" if tts_ok else "unavailable",
        "stt_backend": "faster-whisper",
        "tts_backend": "kokoro",
        "voice": "am_adam",
    }
