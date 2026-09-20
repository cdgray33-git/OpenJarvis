import sys, json
d = {"executable": sys.executable, "prefix": sys.prefix}
try:
    import openjarvis_rust
    d["rust"] = "OK"
    d["rust_file"] = getattr(openjarvis_rust, "__file__", "<builtin>")
    d["rust_attrs"] = sorted([a for a in dir(openjarvis_rust) if not a.startswith("_")])[:25]
except Exception as e:
    d["rust"] = "FAIL"
    d["rust_err"] = repr(e)
try:
    from openjarvis.tools.storage import SQLiteMemory
    d["sqlitememory_import"] = "OK"
except Exception as e:
    d["sqlitememory_import"] = repr(e)
try:
    import openjarvis.traces.store
    d["traces_store_import"] = "OK"
except Exception as e:
    d["traces_store_import"] = repr(e)
print(json.dumps(d))