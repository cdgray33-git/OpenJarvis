import pathlib

path = pathlib.Path(r"C:\Windows\System32\OpenJarvis\\src\\openjarvis\\server\\speech_router.py")
content = path.read_text(encoding="utf-8")

old_synthesize_endpoint = """@speech_router.post("/synthesize")
async def synthesize(request: Request, body: SynthesizeRequest):
    \"\"\"Synthesize text to audio using Kokoro TTS.\"\"\"
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
        raise HTTPException(status_code=500, detail=str(exc))"""

new_synthesize_endpoint = """# --- Singleton TTS Backend ---
_tts_backend = None

def get_tts():
    global _tts_backend
    if _tts_backend is None:
        from openjarvis.speech.kokoro_tts import KokoroTTSBackend
        _tts_backend = KokoroTTSBackend()
    return _tts_backend


@speech_router.post("/synthesize")
async def synthesize(request: Request, body: SynthesizeRequest):
    \"\"\"Synthesize text to audio using Kokoro TTS.\"\"\"
    import asyncio
    try:
        tts = get_tts()
        result = await asyncio.to_thread(
            tts.synthesize,
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
        raise HTTPException(status_code=500, detail=str(exc))"""

old_health = """@speech_router.get("/health")
async def speech_health(request: Request):
    \"\"\"Check speech backend health.\"\"\"
    backend = getattr(request.app.state, "speech_backend", None)
    stt_ok = backend is not None and backend.health()

    from openjarvis.speech.kokoro_tts import KokoroTTSBackend
    tts = KokoroTTSBackend()
    tts_ok = tts.health()"""

new_health = """@speech_router.get("/health")
async def speech_health(request: Request):
    \"\"\"Check speech backend health.\"\"\"
    backend = getattr(request.app.state, "speech_backend", None)
    stt_ok = backend is not None and backend.health()

    tts = get_tts()
    tts_ok = tts.health()"""

if old_synthesize_endpoint not in content:
    print("ERROR: synthesize block not found")
    exit(1)

if old_health not in content:
    print("ERROR: health block not found")
    exit(1)

content = content.replace(old_synthesize_endpoint, new_synthesize_endpoint, 1)
content = content.replace(old_health, new_health, 1)

path.write_text(content, encoding="utf-8", newline="\n")
print("OK: speech_router.py patched successfully")