"""Speech router Ã¢â‚¬â€ STT and TTS endpoints for OpenJarvis."""

from __future__ import annotations

import logging

from fastapi import APIRouter, HTTPException, Request, UploadFile, File
from fastapi.responses import Response
from pydantic import BaseModel

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
    fmt = filename.rsplit(".", 1)[-1].lower() if "." in filename else "wav"

    try:
        result = backend.transcribe(audio_bytes, format=fmt)
        return {"text": result.text, "language": result.language}
    except Exception as exc:
        logger.error("Transcription failed: %s", exc)
        raise HTTPException(status_code=500, detail=str(exc))


# --- Remote TTS Backend (Kokoro on R730xd) ---
KOKORO_SERVER = "http://172.16.33.201:8880"

@speech_router.post("/synthesize")
async def synthesize(request: Request, body: SynthesizeRequest):
    import httpx, time
    t0 = time.time()
    char_count = len(body.text)
    logger.warning("TTS START: %d chars, voice=%s", char_count, body.voice_id)
    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            resp = await client.post(
                KOKORO_SERVER + "/synthesize-stream",
                json={"text": body.text, "voice": body.voice_id, "speed": body.speed},
            )
            resp.raise_for_status()
        elapsed = time.time() - t0
        logger.warning("TTS DONE: %.2fs for %d chars", elapsed, char_count)
        return Response(content=resp.content, media_type="audio/wav")
    except Exception as exc:
        logger.error("Synthesis failed: %s", exc)
        raise HTTPException(status_code=500, detail=str(exc))

@speech_router.get("/health")
async def speech_health(request: Request):
    """Check speech backend health."""
    backend = getattr(request.app.state, "speech_backend", None)
    stt_ok = backend is not None and backend.health()

    tts_ok = True  # Remote Kokoro service on R730xd

    return {
        "available": stt_ok and tts_ok,
        "stt": "ok" if stt_ok else "unavailable",
        "tts": "ok" if tts_ok else "unavailable",
        "stt_backend": "faster-whisper",
        "tts_backend": "kokoro",
        "voice": "am_adam",
    }

