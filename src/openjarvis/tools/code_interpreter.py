"""Code interpreter tool — safe Python code execution in subprocess."""

from __future__ import annotations

import subprocess
from pathlib import Path
import sys
from typing import Any

from openjarvis.core.registry import ToolRegistry
from openjarvis.core.types import ToolResult
from openjarvis.tools._stubs import BaseTool, ToolSpec

# Dangerous patterns to block
_BLOCKED_PATTERNS = [
    "os.system",
    "os.popen",
    "subprocess.",
    "shutil.rmtree",
    "os.remove",
    "os.unlink",
    "os.rmdir",
    "__import__",
    "eval(",
    "exec(",
    "compile(",
    "open(",
]


@ToolRegistry.register("code_interpreter")
class CodeInterpreterTool(BaseTool):
    """Execute Python code in an isolated subprocess."""

    tool_id = "code_interpreter"

    def __init__(self, timeout: int = 30, max_output: int = 10000):
        self._timeout = timeout
        self._max_output = max_output

    @property
    def spec(self) -> ToolSpec:
        return ToolSpec(
            name="code_interpreter",
            description=(
                "Execute Python code and return the output."
                " Code runs in an isolated subprocess."
            ),
            parameters={
                "type": "object",
                "properties": {
                    "code": {
                        "type": "string",
                        "description": "Python code to execute.",
                    },
                },
                "required": ["code"],
            },
            category="code",
        )

    def execute(self, **params: Any) -> ToolResult:
        code = params.get("code", "")
        if not code:
            return ToolResult(
                tool_name="code_interpreter",
                content="No code provided.",
                success=False,
            )

        code = _oj_strip_fence(code)  # openjarvis-w83-codefence-v1
        _oj_before = _oj_snapshot()  # openjarvis-w87-codefiles-v1
        # Security check
        for pattern in _BLOCKED_PATTERNS:
            if pattern in code:
                return ToolResult(
                    tool_name="code_interpreter",
                    content=f"Blocked: code contains prohibited pattern '{pattern}'",
                    success=False,
                )

        try:
            result = subprocess.run(
                [sys.executable, "-c", code],
                capture_output=True,
                text=True,
                timeout=self._timeout,
                cwd=_oj_workdir(),  # openjarvis-w83-codecwd-v1
            )
            output = result.stdout
            if result.stderr:
                output += ("\n" if output else "") + result.stderr
            if len(output) > self._max_output:
                output = output[: self._max_output] + "\n... (output truncated)"
            # openjarvis-w87-codefiles-v1 (W87 G-10): report files the run created or changed, FIRST in content
            _oj_files = _oj_changed(_oj_before)
            _oj_content = output or "(no output)"
            if _oj_files:
                _oj_content = (
                    "Files created or changed in the workspace:\n"
                    + "\n".join("%s (%d bytes)" % (f["path"], f["size_bytes"]) for f in _oj_files)
                    + "\n\nOutput:\n" + _oj_content
                )
            return ToolResult(
                tool_name="code_interpreter",
                content=_oj_content,
                success=result.returncode == 0,
                metadata={"returncode": result.returncode, "files": _oj_files},
            )
        except subprocess.TimeoutExpired:
            return ToolResult(
                tool_name="code_interpreter",
                content=f"Execution timed out after {self._timeout} seconds.",
                success=False,
            )
        except Exception as exc:
            return ToolResult(
                tool_name="code_interpreter",
                content=f"Execution error: {exc}",
                success=False,
            )


# openjarvis-w83-codecwd-v1 (W83 G-2): author runs the subprocess with no cwd, so relative saves (a .docx, a .pptx) land
# wherever the server started - usually the repo root. Use the same folder file_write is confined to.
def _oj_workdir():
    try:
        from openjarvis.core.config import load_config, resolve_file_write_dirs
        d = resolve_file_write_dirs(load_config())[0]
    except Exception:
        d = str(Path.home() / ".openjarvis" / "workspace")
    Path(d).mkdir(parents=True, exist_ok=True)
    return d

# openjarvis-w83-codefence-v1 (W83 G-9): models often wrap the code argument in a markdown fence (```python ... ```);
# the author tool ran it verbatim, so line 1 was a SyntaxError. Strip one leading fence line and a trailing fence.
def _oj_strip_fence(code):
    s = code.strip()
    if not s.startswith("```"):
        return code
    i = s.find("\n")
    s = s[i + 1:] if i != -1 else ""
    s = s.rstrip()
    if s.endswith("```"):
        s = s[:-3].rstrip()
    return s

# openjarvis-w87-codefiles-v1 (W87 G-10): the author returns stdout only, so a script that saves a document and prints
# nothing gives the model "(no output)" and no proof the file exists (S3 R2: valid .docx made, model then tried shell_exec to
# check, hit the confirmation gate, and told the user it failed). Snapshot the workspace top level before the run and
# report what changed after it. Files written OUTSIDE the workspace by absolute path are not seen here (G-1, POAM-50).
def _oj_snapshot():
    try:
        d = Path(_oj_workdir())
        return {p.name: (p.stat().st_mtime_ns, p.stat().st_size) for p in d.iterdir() if p.is_file()}
    except Exception:
        return None

def _oj_changed(before):
    if before is None:
        return []
    try:
        d = Path(_oj_workdir())
        out = []
        for p in sorted(d.iterdir()):
            if not p.is_file():
                continue
            st = p.stat()
            if before.get(p.name) != (st.st_mtime_ns, st.st_size):
                out.append({"path": str(p.resolve()), "size_bytes": st.st_size})
        return out
    except Exception:
        return []

__all__ = ["CodeInterpreterTool"]
