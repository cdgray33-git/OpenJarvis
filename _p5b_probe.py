import sys, json, os
d = {}
d["cwd"] = os.getcwd()
d["path0"] = sys.path[0] if sys.path else ""
d["executable"] = sys.executable
try:
    import openjarvis_rust
    d["rust"] = "OK"
    d["rust_file"] = getattr(openjarvis_rust, "__file__", "<builtin>")
except Exception as e:
    d["rust"] = "FAIL"
    d["rust_err"] = repr(e)
try:
    import openjarvis
    d["oj_file"] = getattr(openjarvis, "__file__", "<none>")
except Exception as e:
    d["oj_err"] = repr(e)
print(json.dumps(d))