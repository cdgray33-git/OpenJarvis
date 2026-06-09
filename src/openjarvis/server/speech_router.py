"""Speech router — STT and TTS endpoints for OpenJarvis."""

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


@speech_router.post("/synthesize")
async def synthesize(request: Request, body: SynthesizeRequest):
    """Synthesize text to audio using Kokoro TTS."""
    from openjarvis.speech.kokoro_tts import KokoroTTSBackend

    try:
        tts = KokoroTTSBackend()
        result = tts.synthesize(
            body.text,
            voice_id=body.voice_id,
            speed=body.speed,
            output_format=body.output_format,
        )
        return Response(
            content=result.audio,
            media_type="audio/wav",
            headers={"X-Duration": str(result.duration_seconds)},
        )
    except Exception as exc:
        logger.error("Synthesis failed: %s", exc)
        raise HTTPException(status_code=500, detail=str(exc))


@speech_router.get("/health")
async def speech_health(request: Request):
    """Check speech backend health."""
    backend = getattr(request.app.state, "speech_backend", None)
    stt_ok = backend is not None and backend.health()

    from openjarvis.speech.kokoro_tts import KokoroTTSBackend
    tts = KokoroTTSBackend()
    tts_ok = tts.health()

    return {
        "available": stt_ok and tts_ok,
        "stt": "ok" if stt_ok else "unavailable",
        "tts": "ok" if tts_ok else "unavailable",
        "stt_backend": "faster-whisper",
        "tts_backend": "kokoro",
        "voice": "am_adam",
    }