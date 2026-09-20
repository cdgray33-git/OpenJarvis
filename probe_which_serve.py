import importlib.util
spec = importlib.util.find_spec("openjarvis.cli.serve")
p = spec.origin
print("LOADED FROM:", p)
src = open(p, encoding="utf-8").read()
print("MARKER PRESENT:", "openjarvis-bind-assert-v1" in src)
print("LINES:", len(src.splitlines()))
