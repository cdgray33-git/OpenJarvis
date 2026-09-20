import re
path = r'C:\Windows\System32\OpenJarvis\pyproject.toml'
text = open(path, 'r', encoding='utf-8-sig').read()
text = text.replace('"pynvml>=13.0.1"', '"nvidia-ml-py>=12.0"')
text = re.sub(r'speech = \["faster-whisper>=1\.0"\]', 'speech = ["faster-whisper>=1.2.1", "kokoro-onnx>=0.5.0", "ctranslate2>=4.8.0", "onnxruntime>=1.14", "av>=17.1.0", "sounddevice>=0.4.6"]', text)
text = text.replace('requires-python = ">=3.10"', 'requires-python = ">=3.11"')
open(path, 'w', encoding='utf-8', newline='\n').write(text)
print('Done')
