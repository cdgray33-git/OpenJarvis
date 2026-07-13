"""Speech router ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â STT and TTS endpoints for OpenJarvis."""

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
                    KOKORO_SERVER + "/synthesize-stream",
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
