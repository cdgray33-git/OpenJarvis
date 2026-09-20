import importlib, os
m = importlib.import_module("openjarvis.agents.native_openhands")
p = os.path.join(os.environ["LOCALAPPDATA"], "OpenJarvis", "logs", "agent.log")
before = os.path.getsize(p) if os.path.exists(p) else 0
print("agent.log before:", before)
print("helper present:", hasattr(m, "_oj_raw_gen"))
m._oj_raw_gen("probe-raw-1", "probe-raw-1-t1", "AAA<think>x</think>BBB", "AAABBB", 0)
for h in m._oj_get_agent_logger().handlers:
    h.flush()
after = os.path.getsize(p) if os.path.exists(p) else 0
print("agent.log after:", after, "| delta:", after - before)
with open(p, "r", encoding="utf-8", errors="replace") as f:
    tail = [ln for ln in f.read().splitlines() if "probe-raw-1" in ln]
print("PROBE LINES:", len(tail))
for ln in tail:
    print(ln)
