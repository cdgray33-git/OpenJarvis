import sqlite3, os, datetime
db = os.path.expanduser(r"~\.openjarvis\telemetry.db")
c = sqlite3.connect(db); c.row_factory = sqlite3.Row
print("PTE CEILING BANDS (all rows, pte>0)")
q = """
SELECT CASE
  WHEN prompt_tokens_evaluated BETWEEN 8000 AND 8192 THEN 'A 8000-8192 (8k clamp)'
  WHEN prompt_tokens_evaluated BETWEEN 15900 AND 16384 THEN 'B 15900-16384 (16k clamp)'
  WHEN prompt_tokens_evaluated > 16384 THEN 'C above 16384'
  ELSE 'D below bands' END AS band,
  COUNT(*) AS n, MIN(prompt_tokens_evaluated) AS lo, MAX(prompt_tokens_evaluated) AS hi
FROM telemetry WHERE prompt_tokens_evaluated > 0 GROUP BY band ORDER BY band
"""
for r in c.execute(q):
    print("  %-28s n=%-6d lo=%-7d hi=%d" % (r["band"], r["n"], r["lo"], r["hi"]))
print()
print("TOP 12 BY GAP (pt - pte), pte>0")
q2 = """
SELECT timestamp, model_id, prompt_tokens AS pt, prompt_tokens_evaluated AS pte,
       completion_tokens AS ct, prompt_tokens - prompt_tokens_evaluated AS gap
FROM telemetry WHERE prompt_tokens_evaluated > 0
ORDER BY gap DESC LIMIT 12
"""
for r in c.execute(q2):
    ts = datetime.datetime.fromtimestamp(r["timestamp"]).strftime("%m-%d %H:%M:%S")
    print("  %s  %-26s pt=%-8d pte=%-7d ct=%-6d gap=%d" % (
        ts, (r["model_id"] or "")[:26], r["pt"], r["pte"], r["ct"], r["gap"]))
