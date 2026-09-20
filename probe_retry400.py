import importlib, os
m = importlib.import_module("openjarvis.engine.ollama")
class R:
    status_code = 400
    text = "probe body: unsupported tools payload"
m._oj_log_retry400(R(), {"messages": [{"role": "user", "content": "x"}], "tools": [1, 2]}, [1, 2] * 6)
m._oj_log_retry400_result(R())
p = os.path.join(os.environ["LOCALAPPDATA"], "OpenJarvis", "logs", "engine.log")
print("exists:", os.path.exists(p), "size:", os.path.getsize(p) if os.path.exists(p) else 0)
print(open(p, encoding="utf-8").read()[-400:])
