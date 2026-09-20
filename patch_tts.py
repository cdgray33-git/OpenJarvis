path = r'C:\Windows\System32\openjarvis\src\openjarvis\server\speech_router.py'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

old_marker = '# --- Singleton TTS Backend ---'
end_marker = '@speech_router.get("/health")'

if old_marker not in content:
    print('MATCH FAILED')
else:
    start = content.index(old_marker)
    end = content.index(end_marker)
    new_block = (
        '# --- Remote TTS Backend (Kokoro on R730xd) ---\n'
        'KOKORO_SERVER = "http://172.16.33.200:8880"\n\n'
        '@speech_router.post("/synthesize")\n'
        'async def synthesize(request: Request, body: SynthesizeRequest):\n'
        '    import httpx, time\n'
        '    t0 = time.time()\n'
        '    char_count = len(body.text)\n'
        '    logger.warning("TTS START: %d chars, voice=%s", char_count, body.voice_id)\n'
        '    try:\n'
        '        async with httpx.AsyncClient(timeout=60.0) as client:\n'
        '            resp = await client.post(\n'
        '                KOKORO_SERVER + "/synthesize",\n'
        '                json={"text": body.text, "voice": body.voice_id, "speed": body.speed},\n'
        '            )\n'
        '            resp.raise_for_status()\n'
        '        elapsed = time.time() - t0\n'
        '        logger.warning("TTS DONE: %.2fs for %d chars", elapsed, char_count)\n'
        '        return Response(content=resp.content, media_type="audio/wav")\n'
        '    except Exception as exc:\n'
        '        logger.error("Synthesis failed: %s", exc)\n'
        '        raise HTTPException(status_code=500, detail=str(exc))\n\n'
    )
    content = content[:start] + new_block + content[end:]
    with open(path, 'w', encoding='utf-8', newline='\n') as f:
        f.write(content)
    print('SUCCESS')
