import hashlib, os
from pathlib import Path
home = Path.home() / ".openjarvis"; cfg = home / "config.toml"
h = lambda p: hashlib.sha256(p.read_bytes()).hexdigest().upper()[:16]
names = ["SOUL.md", "MEMORY.md", "USER.md", "skills"]
before = {n: (home / n).exists() for n in names}; hb = h(cfg)
print("BEFORE config.toml sha=%s  exists=%s" % (hb, before))
from openjarvis.cli._bootstrap import _seed_memory_files
_seed_memory_files()
ha = h(cfg)
for n in names:
    p = home / n
    if p.is_dir(): print("AFTER  %-9s DIR  created_now=%s" % (n, not before[n]))
    elif p.exists(): print("AFTER  %-9s %4d bytes created_now=%s first=%r" % (n, p.stat().st_size, not before[n], p.read_text().splitlines()[0] if p.read_text() else ""))
    else: print("AFTER  %-9s ABSENT" % n)
print("config.toml sha after=%s  UNCHANGED=%s" % (ha, ha == hb))
print("P1 PASS=%s" % (ha == hb and all((home / n).exists() for n in names)))
