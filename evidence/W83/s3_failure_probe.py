import os, re
from pathlib import Path
DL = Path(os.environ["LOCALAPPDATA"]) / "OpenJarvis" / "logs" / "dispatch.log"
lines = [l for l in DL.read_text(errors="replace").splitlines() if l[:19] >= "2026-09-24 20:05:34" and "ATTEMPT" in l and ("tool=file_write" in l or "tool=code_interpreter" in l)]
print("ATTEMPTS since S3 start: %d" % len(lines))
from openjarvis.tools.code_interpreter import _BLOCKED_PATTERNS
for l in lines:
    tool = re.search(r"tool=(\S+)", l).group(1); args = l[l.find("args=") + 5:]
    if tool == "file_write":
        m = re.search(r'"path":\s*"([^"]*)"', args); print("  FILE_WRITE path=%r content_chars~%d" % (m.group(1) if m else "?", len(args)))
    else:
        hits = [p for p in _BLOCKED_PATTERNS if p in args.replace("\\n", "\n")]
        print("  CODE_INTERPRETER blocklist_hits=%s code_head=%r" % (hits, args[:220]))
from openjarvis.core.config import load_config, resolve_file_write_dirs
from openjarvis.tools.file_write import FileWriteTool
dirs = resolve_file_write_dirs(load_config()); fw = FileWriteTool(allowed_dirs=dirs)
print("ALLOWED_DIRS", dirs)
for pth in ("w83_s3_replay.txt", str(Path(dirs[0]) / "w83_s3_replay.txt")):
    r = fw.execute(path=pth, content="replay")
    print("REPLAY file_write path=%r success=%s msg=%r" % (pth, r.success, str(r.content)[:160]))
    q = Path(dirs[0]) / "w83_s3_replay.txt"
    if q.exists(): q.unlink()
