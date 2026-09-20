import sys, json
d = {"executable": sys.executable, "prefix": sys.prefix, "base_prefix": sys.base_prefix}
try:
    import openjarvis_rust
    d["rust"] = "OK"
    d["rust_file"] = getattr(openjarvis_rust, "__file__", "<builtin>")
    d["rust_attrs"] = sorted([a for a in dir(openjarvis_rust) if not a.startswith("_")])[:20]
except Exception as e:
    d["rust"] = "FAIL"
    d["rust_err"] = repr(e)
print(json.dumps(d))