"""openjarvis-toolkit-refusal-test-v2 (W55)

Deterministic, non-interactive test of the W54 toolkit-bind refusal path.

WHY THIS SHAPE:
  _allowed_tool_names is built from stream_kwargs["tools"] - the exact spec
  set handed to the model. A well-behaved model is therefore structurally
  incapable of emitting a refused name, so the refusal path CANNOT be
  triggered by prompting a real agent. It can only be triggered by a
  tool_call whose name is outside the spec set.

  This harness supplies exactly that, with a stub engine, and exercises the
  REAL _stream_managed_agent: the real bind construction, the real guard, the
  real logger, the real exception handler, the real SSE frames. Nothing about
  the guard is re-implemented here.

V2 CHANGE - why v1 criterion 5 was wrong:
  v1 searched the whole SSE body for a sentinel string. tool_call_start
  echoes the tool ARGUMENTS verbatim before the guard is ever reached, so
  the sentinel matched the echo, not execution. A string in the transcript
  is not evidence a tool ran. v2 asserts on a FILESYSTEM ARTIFACT instead:
  the refused command's only job is to create a marker file. Execution
  leaves the file behind or execution did not happen.

PASS CRITERIA (all five must hold):
  1. bind line logged with exactly ['think']
  2. TOOLKIT REFUSAL warning logged, tool=shell_exec
  3. SSE tool_call_end for shell_exec carries success=false
  4. the tool result text names the refusal
  5. the marker file does not exist - shell_exec never ran

Run from repo root:  python test_toolkit_refusal.py
Exit code 0 = PASS, 1 = FAIL.
"""

import asyncio
import json
import logging
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "src"))

MARKER = os.path.join(os.getcwd(), "w55_breach_marker.txt")
CAPTURED = []


class _Capture(logging.Handler):
    def emit(self, record):
        try:
            CAPTURED.append((record.levelname, record.getMessage()))
        except Exception:
            pass


class FakeChunk:
    def __init__(self, content=None, tool_calls=None, finish_reason=None):
        self.content = content
        self.tool_calls = tool_calls
        self.finish_reason = finish_reason


class FakeEngine:
    """Turn 1: emit a tool_call for a tool NOT in the toolkit.
    Turn 2: emit plain content so the loop terminates."""

    def __init__(self, refused_tool, command):
        self.refused_tool = refused_tool
        self.command = command
        self.turn = 0
        self._model = "stub-model"

    async def stream_full(self, messages, **kwargs):
        self.turn += 1
        if self.turn == 1:
            yield FakeChunk(
                tool_calls=[
                    {
                        "index": 0,
                        "id": "call_w55_refusal",
                        "function": {
                            "name": self.refused_tool,
                            "arguments": json.dumps({"command": self.command}),
                        },
                    }
                ]
            )
            yield FakeChunk(finish_reason="tool_calls")
        else:
            yield FakeChunk(content="done")
            yield FakeChunk(finish_reason="stop")


class FakeManager:
    def __init__(self):
        self.stored = []

    def list_messages(self, agent_id, limit=50):
        return []

    def mark_message_delivered(self, message_id):
        return None

    def add_learning_log(self, agent_id, kind, text, meta=None):
        return None

    def store_agent_response(self, agent_id, content, tool_calls=None):
        self.stored.append((content, tool_calls))


async def main():
    if os.path.exists(MARKER):
        os.remove(MARKER)

    logger = logging.getLogger("openjarvis.server.agent_manager")
    logger.setLevel(logging.INFO)
    logger.addHandler(_Capture())

    from openjarvis.server.agent_manager_routes import _stream_managed_agent

    manager = FakeManager()
    command = 'cmd /c echo breached > "%s"' % MARKER
    engine = FakeEngine("shell_exec", command)

    agent_record = {
        "id": "W55TESTHARNESS",
        "agent_type": "monitor_operative",
        "config": {
            "model": "stub-model",
            "tools": ["think"],
            "max_turns": 3,
            "system_prompt": "test harness",
        },
    }

    response = await _stream_managed_agent(
        manager=manager,
        agent_record=agent_record,
        user_content="harness",
        message_id="msg-w55",
        engine=engine,
        bus=None,
        app_state=None,
    )

    frames = []
    async for raw in response.body_iterator:
        frames.append(raw if isinstance(raw, str) else raw.decode("utf-8", "replace"))
    body = "".join(frames)

    bind_ok = any(
        lvl == "INFO" and "toolkit bound (1 tools)" in msg and "'think'" in msg
        for lvl, msg in CAPTURED
    )
    refusal_ok = any(
        lvl == "WARNING" and "TOOLKIT REFUSAL" in msg and "tool=shell_exec" in msg
        for lvl, msg in CAPTURED
    )

    end_ok = False
    result_ok = False
    for block in body.split("\n\n"):
        if "event: tool_call_end" not in block:
            continue
        for line in block.split("\n"):
            if not line.startswith("data: "):
                continue
            try:
                payload = json.loads(line[6:])
            except Exception:
                continue
            if payload.get("tool") != "shell_exec":
                continue
            end_ok = payload.get("success") is False
            result_ok = "not in this agent's toolkit" in (payload.get("result") or "")

    marker_present = os.path.exists(MARKER)
    if marker_present:
        try:
            os.remove(MARKER)
        except Exception:
            pass

    print("")
    print("=== openjarvis-toolkit-refusal-test-v2 ===")
    print("1 bind line, exactly ['think']      : %s" % ("PASS" if bind_ok else "FAIL"))
    print("2 TOOLKIT REFUSAL, tool=shell_exec  : %s" % ("PASS" if refusal_ok else "FAIL"))
    print("3 tool_call_end success=false       : %s" % ("PASS" if end_ok else "FAIL"))
    print("4 result names the refusal          : %s" % ("PASS" if result_ok else "FAIL"))
    print("5 no marker file, shell_exec never ran : %s"
          % ("PASS" if not marker_present else "FAIL"))
    print("")
    print("marker path checked: %s" % MARKER)
    print("")
    print("--- captured log lines ---")
    for lvl, msg in CAPTURED:
        print("%-7s %s" % (lvl, msg))
    print("")

    ok = bind_ok and refusal_ok and end_ok and result_ok and not marker_present
    print("OVERALL: %s" % ("PASS" if ok else "FAIL"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
