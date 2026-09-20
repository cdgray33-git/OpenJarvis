import pathlib

path = pathlib.Path(r"C:\Windows\System32\OpenJarvis\src\openjarvis\server\speech_router.py")
content = path.read_text(encoding="utf-8")

old = """@speech_router.post("/synthesize")
async def synthesize(request: Request, body: SynthesizeRequest):
    \"\"\"Synthesize text to audio using Kokoro TTS.\"\"\"
    import asyncio
    try:
        tts = get_tts()
        result = await asyncio.to_thread("""

new = """@speech_router.post("/synthesize")
async def synthesize(request: Request, body: SynthesizeRequest):
    \"\"\"Synthesize text to audio using Kokoro TTS.\"\"\"
    import asyncio
    import time
    t0 = time.time()
    char_count = len(body.text)
    logger.info(f"TTS START: {char_count} chars, voice={body.voice_id}")
    try:
        tts = get_tts()
        result = await asyncio.to_thread("""

old2 = """        return Response(
            content=result.audio,
            media_type="audio/wav",
            headers={"X-Duration": str(result.duration_seconds)},
        )"""

new2 = """        elapsed = time.time() - t0
        logger.info(f"TTS DONE: {elapsed:.2f}s for {char_count} chars ({char_count/elapsed:.0f} chars/sec)")
        return Response(
            content=result.audio,
            media_type="audio/wav",
            headers={"X-Duration": str(result.duration_seconds)},
        )"""

if old not in content:
    print("ERROR: synthesize block not found")
    exit(1)

if old2 not in content:
    print("ERROR: response block not found")
    exit(1)

content = content.replace(old, new, 1)
content = content.replace(old2, new2, 1)
path.write_text(content, encoding="utf-8", newline="\n")
print("OK: timing instrumentation added")