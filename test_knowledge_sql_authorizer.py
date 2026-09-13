"""openjarvis-knowledge-sql-authorizer-test-v1 (W55)

Deterministic, non-interactive test of openjarvis-knowledge-sql-authorizer-v1.

Builds a THROWAWAY in-memory SQLite database containing knowledge_chunks plus
a decoy table, hands it to the real KnowledgeSQLTool, and exercises the real
execute() path. Your actual knowledge.db is never opened.

PASS CRITERIA:
  1. a legitimate aggregate query still works
  2. sqlite_master is denied (schema enumeration closed)
  3. an unrelated table is denied (scope actually enforced)
  4. a write is refused
  5. LIKE '%update%' is ALLOWED - the old blacklist false positive is gone
  6. a CTE (WITH ...) is allowed - old startswith('SELECT') refused these
  7. authorizer CLEARED after a SUCCESSFUL call (shared conn not restricted)
  8. authorizer CLEARED after a DENIED call (the finally path)

Criteria 7 and 8 are checked by running a raw query against the DECOY table
on the same connection after the tool returns. If the authorizer leaked, that
raw query fails - which is exactly how a leak would break every other
consumer of the shared knowledge store.

Run from repo root:  python test_knowledge_sql_authorizer.py
Exit code 0 = PASS, 1 = FAIL.
"""

import os
import sqlite3
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "src"))

RESULTS = []


def check(label, ok, detail=""):
    RESULTS.append((label, bool(ok), detail))


class FakeStore:
    """Minimal stand-in exposing the one attribute the tool touches."""

    def __init__(self, conn):
        self._conn = conn


def build_db():
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    conn.execute(
        "CREATE TABLE knowledge_chunks ("
        "id INTEGER PRIMARY KEY, content TEXT, source TEXT, author TEXT)"
    )
    conn.execute("CREATE TABLE decoy_secrets (id INTEGER PRIMARY KEY, secret TEXT)")
    conn.execute("INSERT INTO decoy_secrets (secret) VALUES ('TOPSECRET')")
    for i in range(60):
        conn.execute(
            "INSERT INTO knowledge_chunks (content, source, author) VALUES (?,?,?)",
            ("x" * 600 + " update " + str(i), "imessage", "author%d" % (i % 3)),
        )
    conn.commit()
    return conn


def authorizer_is_clear(conn):
    """True if the shared connection is unrestricted."""
    try:
        conn.execute("SELECT secret FROM decoy_secrets").fetchone()
        return True
    except sqlite3.DatabaseError:
        return False


def main():
    conn = build_db()

    from openjarvis.tools.knowledge_sql import KnowledgeSQLTool

    tool = KnowledgeSQLTool(store=FakeStore(conn))

    r = tool.execute(query="SELECT author, COUNT(*) AS n FROM knowledge_chunks GROUP BY author")
    check("1 legitimate aggregate query works", r.success, (r.content or "")[:70])

    check("7 authorizer cleared after SUCCESS", authorizer_is_clear(conn))

    r = tool.execute(query="SELECT name FROM sqlite_master")
    check("2 sqlite_master denied", not r.success, (r.content or "")[:70])

    check("8 authorizer cleared after DENIAL", authorizer_is_clear(conn))

    r = tool.execute(query="SELECT secret FROM decoy_secrets")
    leaked = "TOPSECRET" in (r.content or "")
    check("3 unrelated table denied", (not r.success) and (not leaked),
          (r.content or "")[:70])

    r = tool.execute(query="UPDATE knowledge_chunks SET content='x'")
    check("4 write refused", not r.success, (r.content or "")[:70])

    r = tool.execute(
        query="SELECT id FROM knowledge_chunks WHERE content LIKE '%update%' LIMIT 3"
    )
    check("5 LIKE '%update%' now ALLOWED", r.success, (r.content or "")[:70])

    r = tool.execute(
        query="WITH t AS (SELECT author FROM knowledge_chunks) "
              "SELECT author, COUNT(*) AS n FROM t GROUP BY author"
    )
    check("6 CTE allowed", r.success, (r.content or "")[:70])

    r = tool.execute(query="SELECT content FROM knowledge_chunks")
    meta = r.metadata or {}
    check("9 byte cap fires on wide output",
          r.success and bool(meta.get("truncated")),
          "rows_fetched=%s rendered=%s truncated=%s"
          % (meta.get("rows_fetched"), meta.get("num_rows"), meta.get("truncated")))

    check("10 authorizer cleared at end", authorizer_is_clear(conn))

    print("")
    print("=== openjarvis-knowledge-sql-authorizer-test-v1 ===")
    failed = 0
    for label, ok, detail in RESULTS:
        if not ok:
            failed += 1
        print("%-40s : %s" % (label, "PASS" if ok else "FAIL"))
        if detail:
            print("%-40s   %s" % ("", detail.replace("\n", " / ")))
    print("")
    print("OVERALL: %s" % ("PASS" if failed == 0 else "FAIL (%d)" % failed))
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
