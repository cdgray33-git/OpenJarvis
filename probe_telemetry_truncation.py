import sqlite3, os
db = os.path.expanduser(r"~\.openjarvis\telemetry.db")
c = sqlite3.connect(db); c.row_factory = sqlite3.Row
print("DB:", db)
print("ROWS:", c.execute("SELECT COUNT(*) AS n FROM telemetry").fetchone()["n"])
print()
q = """
SELECT agent,
       COUNT(*) AS n,
       SUM(CASE WHEN prompt_tokens_evaluated = 0 THEN 1 ELSE 0 END) AS pte_zero,
       SUM(CASE WHEN prompt_tokens > prompt_tokens_evaluated
                 AND prompt_tokens_evaluated > 0 THEN 1 ELSE 0 END) AS pt_gt_pte,
       MAX(prompt_tokens) AS max_pt,
       MAX(prompt_tokens_evaluated) AS max_pte
FROM telemetry GROUP BY agent ORDER BY n DESC
"""
print("%-28s %7s %9s %10s %8s %8s" % ("AGENT","ROWS","PTE_ZERO","PT_GT_PTE","MAX_PT","MAX_PTE"))
for r in c.execute(q):
    print("%-28s %7d %9d %10d %8d %8d" % (
        r["agent"] or "(blank)", r["n"], r["pte_zero"],
        r["pt_gt_pte"], r["max_pt"], r["max_pte"]))
