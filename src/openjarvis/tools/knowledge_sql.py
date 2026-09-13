"""KnowledgeSQLTool - read-only SQL queries against the KnowledgeStore.

Allows agents to run SELECT queries for aggregation, counting, ranking,
and filtering operations that BM25 search cannot handle.

openjarvis-knowledge-sql-authorizer-v2 (W55)
============================================

WHAT CHANGED AND WHY

The previous guard was two text checks: the query had to start with SELECT,
and the UPPERCASED query text could not contain any of DROP/DELETE/INSERT/
UPDATE/ALTER/CREATE/ATTACH as a substring. Both operate on the query STRING,
before SQLite has parsed anything. That shape has two faults.

  FALSE POSITIVES. The blacklist matched inside string literals, so a
  perfectly legal read like
      SELECT * FROM knowledge_chunks WHERE content LIKE '%update%'
  was refused because the word UPDATE appeared in the user's search term.

  FALSE NEGATIVES, and this is the one that mattered. Nothing checked WHICH
  TABLE was read. The tool's own description advertises knowledge_chunks,
  but the enforcement covered no table at all:
      SELECT * FROM sqlite_master
  enumerated the schema, and every other table in knowledge.db was readable
  from there. Write was blocked; SCOPE WAS NOT.

THE FIX USES SQLITE'S OWN MECHANISM, NOT A BETTER BLACKLIST.

sqlite3.Connection.set_authorizer installs a callback that SQLite invokes
during statement preparation, once per operation, with the RESOLVED table and
column names. It sits at the parse layer, so it cannot be fooled by a string
literal, a CTE, an alias, a view, or creative whitespace. Anything not
explicitly permitted is denied by the engine before a single row is touched.

Because the authorizer is the real enforcement now, the text blacklist is
GONE rather than kept "for defence in depth" - keeping it would only preserve
its false positives while adding nothing the authorizer does not already do.
The SELECT/WITH prefix check is kept solely to return a friendly message for
the common mistake; it is not load-bearing.

THREADING HAZARD - READ BEFORE EDITING

set_authorizer is per-CONNECTION and GLOBAL to it, and self._store._conn is
SHARED with every other consumer of the knowledge store. An authorizer left
installed would silently restrict all of them. It is therefore installed
under a module-level lock and cleared in a finally block. Do not move either.

FAILURE MODE OF THE DENIAL

An authorizer denial surfaces as sqlite3.DatabaseError, NOT
sqlite3.OperationalError. The old code caught only OperationalError, so a
denial would have escaped this tool as an unhandled exception. The catch is
widened accordingly.

V2 CORRECTION - DO NOT RE-ADD THE FRIENDLY DENIAL MESSAGE

v1 special-cased the denial to rewrite it into a friendlier sentence, keyed on
the substring "not authorized". SQLite does not say that. The real text,
confirmed by the W55 harness, is:

    access to decoy_secrets.secret is prohibited
    access to sqlite_master.name is prohibited

so the branch never fired and was dead code inside a guard - the exact kind of
thing that reads as working when someone audits this file later. It is removed
rather than repaired: SQLite's own message NAMES THE TABLE AND COLUMN THAT WAS
REFUSED, which is strictly more useful than the sentence it was replacing.
"""

from __future__ import annotations

import sqlite3
import threading
from typing import Any, Optional

from openjarvis.connectors.store import KnowledgeStore
from openjarvis.core.registry import ToolRegistry
from openjarvis.core.types import ToolResult
from openjarvis.tools._stubs import BaseTool, ToolSpec

_MAX_ROWS = 50

# fetchmany() caps ROWS, not BYTES. A single SELECT content query returns 50
# full chunk bodies, which is a context-blowout on its own. Cap the rendered
# output too.
_MAX_BYTES = 16000

# The only table this tool may read. Enforced by the authorizer, not by text.
_ALLOWED_TABLE = "knowledge_chunks"

_SCHEMA_DESCRIPTION = (
    "Table: knowledge_chunks\n"
    "Columns: id, content, source, doc_type, doc_id, title, author, "
    "participants, timestamp, thread_id, url, metadata, chunk_index"
)

# set_authorizer is global to the connection and the connection is shared.
# Serialize install / execute / clear so two concurrent callers cannot leave
# one another's authorizer in place.
_AUTHORIZER_LOCK = threading.Lock()

# Action codes. SQLITE_FUNCTION and SQLITE_RECURSIVE are not present on every
# Python build, so resolve them defensively rather than importing by name.
_SQLITE_SELECT = sqlite3.SQLITE_SELECT
_SQLITE_READ = sqlite3.SQLITE_READ
_SQLITE_FUNCTION = getattr(sqlite3, "SQLITE_FUNCTION", 31)
_SQLITE_RECURSIVE = getattr(sqlite3, "SQLITE_RECURSIVE", 33)


def _authorizer(action: int, arg1: Any, arg2: Any, dbname: Any, source: Any) -> int:
    """Permit read-only access to _ALLOWED_TABLE and nothing else.

    SQLite calls this once per operation during statement preparation.

      SQLITE_SELECT     - a SELECT is being prepared. arg1/arg2 are None.
      SQLITE_READ       - arg1 is the table, arg2 the column being read.
      SQLITE_FUNCTION   - arg2 is the function name (COUNT, LOWER, ...).
      SQLITE_RECURSIVE  - a recursive CTE. Read-only.

    Every other action code (INSERT, UPDATE, DELETE, DROP, ATTACH, PRAGMA,
    CREATE, TRANSACTION, ...) falls through to SQLITE_DENY. This is a
    whitelist: a SQLite version that adds a new write action gets denied by
    default rather than slipping through, which is the whole reason for
    preferring this over a blacklist.
    """
    if action == _SQLITE_SELECT:
        return sqlite3.SQLITE_OK
    if action == _SQLITE_FUNCTION:
        return sqlite3.SQLITE_OK
    if action == _SQLITE_RECURSIVE:
        return sqlite3.SQLITE_OK
    if action == _SQLITE_READ:
        # arg1 is the resolved table name. sqlite_master, sqlite_temp_master,
        # and every unrelated table land here and are denied.
        return sqlite3.SQLITE_OK if arg1 == _ALLOWED_TABLE else sqlite3.SQLITE_DENY
    return sqlite3.SQLITE_DENY


@ToolRegistry.register("knowledge_sql")
class KnowledgeSQLTool(BaseTool):
    """Run read-only SQL against the knowledge store for aggregation queries."""

    tool_id = "knowledge_sql"

    def __init__(self, store: Optional[KnowledgeStore] = None) -> None:
        self._store = store

    @property
    def spec(self) -> ToolSpec:
        return ToolSpec(
            name="knowledge_sql",
            description=(
                "Run a read-only SQL SELECT query against the knowledge_chunks table. "
                "Use for counting, ranking, aggregation, and filtering. "
                f"{_SCHEMA_DESCRIPTION}"
            ),
            parameters={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": (
                            "SQL SELECT query against knowledge_chunks. "
                            "Read-only; no other table is accessible. "
                            "Example: SELECT author, COUNT(*) as n "
                            "FROM knowledge_chunks "
                            "WHERE source='imessage' GROUP BY author "
                            "ORDER BY n DESC LIMIT 10"
                        ),
                    },
                },
                "required": ["query"],
            },
            category="knowledge",
        )

    def execute(self, **params: Any) -> ToolResult:
        if self._store is None:
            return ToolResult(
                tool_name="knowledge_sql",
                content="No knowledge store configured.",
                success=False,
            )

        query: str = params.get("query", "").strip()
        if not query:
            return ToolResult(
                tool_name="knowledge_sql",
                content="No query provided.",
                success=False,
            )

        # Friendly message for the common mistake. NOT the security boundary -
        # the authorizer below is. Kept permissive enough to allow CTEs, which
        # are read-only and which the old startswith("SELECT") check refused.
        normalized = query.lstrip().upper()
        if not (normalized.startswith("SELECT") or normalized.startswith("WITH")):
            return ToolResult(
                tool_name="knowledge_sql",
                content="Only SELECT queries are allowed (read-only).",
                success=False,
            )

        conn = self._store._conn

        with _AUTHORIZER_LOCK:
            try:
                conn.set_authorizer(_authorizer)
                rows = conn.execute(query).fetchmany(_MAX_ROWS)
            except sqlite3.DatabaseError as exc:
                # Covers OperationalError (bad SQL) and the authorizer's
                # denial, which is a DatabaseError and would have escaped the
                # old narrow catch. SQLite's own text names the refused table
                # and column - see the V2 note in the module docstring for why
                # it is passed through unrewritten.
                return ToolResult(
                    tool_name="knowledge_sql",
                    content=f"SQL error: {exc}",
                    success=False,
                )
            finally:
                # MUST run. The connection is shared; a leaked authorizer
                # would restrict every other consumer of knowledge.db.
                try:
                    conn.set_authorizer(None)
                except Exception:
                    pass

        if not rows:
            return ToolResult(
                tool_name="knowledge_sql",
                content="Query returned no results.",
                success=True,
                metadata={"num_rows": 0},
            )

        columns = rows[0].keys()
        lines = [" | ".join(columns)]
        lines.append(" | ".join("---" for _ in columns))

        used = sum(len(line) + 1 for line in lines)
        rendered = 0
        truncated = False
        for row in rows:
            line = " | ".join(str(row[c]) for c in columns)
            if used + len(line) + 1 > _MAX_BYTES:
                truncated = True
                break
            lines.append(line)
            used += len(line) + 1
            rendered += 1

        if truncated:
            lines.append(
                f"... output truncated at {_MAX_BYTES} characters "
                f"({rendered} of {len(rows)} rows shown). "
                "Select fewer columns or add a tighter WHERE clause."
            )

        return ToolResult(
            tool_name="knowledge_sql",
            content="\n".join(lines),
            success=True,
            metadata={
                "num_rows": rendered,
                "rows_fetched": len(rows),
                "truncated": truncated,
            },
        )


__all__ = ["KnowledgeSQLTool"]
