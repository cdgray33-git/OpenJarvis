import pathlib

path = pathlib.Path(r"C:\Windows\System32\OpenJarvis\src\openjarvis\server\speech_router.py")
content = path.read_text(encoding="utf-8")

content = content.replace(
    'logger.info(f"TTS START: {char_count} chars, voice={body.voice_id}")',
    'logger.warning(f"TTS START: {char_count} chars, voice={body.voice_id}")'
)
content = content.replace(
    'logger.info(f"TTS DONE: {elapsed:.2f}s for {char_count} chars ({char_count/elapsed:.0f} chars/sec)")',
    'logger.warning(f"TTS DONE: {elapsed:.2f}s for {char_count} chars ({char_count/elapsed:.0f} chars/sec)")'
)

path.write_text(content, encoding="utf-8", newline="\n")
print("OK: log level bumped to WARNING")