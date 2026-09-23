import pathlib, shutil, sys, time, py_compile
ts = time.strftime("%Y%m%d_%H%M%S")
root = pathlib.Path.cwd()
MARK = "openjarvis-engine-disable-v1"
cfg = root / "src/openjarvis/core/config.py"
dsc = root / "src/openjarvis/engine/_discovery.py"
def rd(p):
    with open(p, "r", encoding="utf-8", newline="") as fh: return fh.read()
def wr(p, s):
    with open(p, "w", encoding="utf-8", newline="") as fh: fh.write(s)
t_cfg, t_dsc = rd(cfg), rd(dsc)
nl_c = "\r\n" if "\r\n" in t_cfg else "\n"
nl_d = "\r\n" if "\r\n" in t_dsc else "\n"
print("NEWLINE cfg", repr(nl_c), "dsc", repr(nl_d))
if MARK in t_cfg or MARK in t_dsc:
    print("ABORT: marker already present"); sys.exit(2)
a1 = '    """Inference engine settings with nested per-engine configs."""' + nl_c + nl_c + '    default: str = "ollama"' + nl_c
r1 = a1 + "    # " + MARK + " (Graystone D-16): comma-separated engine keys that are" + nl_c + "    # never constructed or probed. The author ships no engine off-switch." + nl_c + '    disabled: str = ""' + nl_c
a2 = "logger = logging.getLogger(__name__)" + nl_d
r2 = a2 + nl_d + nl_d + "class EngineDisabled(RuntimeError):" + nl_d + '    """Raised by _make_engine for keys listed in [engine] disabled (' + MARK + ')."""' + nl_d
a3 = '    """Instantiate a registered engine with the appropriate config host."""' + nl_d
r3 = a3 + "    # " + MARK + " (Graystone D-16): single choke point for every enumerator" + nl_d + '    _off = {k.strip() for k in (getattr(config.engine, "disabled", "") or "").split(",") if k.strip()}' + nl_d + "    if key in _off:" + nl_d + '        raise EngineDisabled(f"engine {key!r} disabled by [engine] disabled")' + nl_d
for name, txt, a in (("cfg a1", t_cfg, a1), ("dsc a2", t_dsc, a2), ("dsc a3", t_dsc, a3)):
    n = txt.count(a); print(f"ANCHOR {name} count={n}")
    if n != 1: print("ABORT: anchor not unique"); sys.exit(3)
for p in (cfg, dsc):
    b = p.with_name(p.name + f".bak_w79disable_{ts}"); shutil.copy2(p, b); print("BACKUP", b)
wr(cfg, t_cfg.replace(a1, r1, 1))
wr(dsc, t_dsc.replace(a2, r2, 1).replace(a3, r3, 1))
for p in (cfg, dsc):
    py_compile.compile(str(p), doraise=True); print("COMPILE OK", p.name)
print("PATCH APPLIED", MARK)