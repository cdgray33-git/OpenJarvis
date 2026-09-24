"""Document ingestion — file reading, type detection, directory walking."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional, Tuple

from openjarvis.tools.storage.chunking import Chunk, ChunkConfig, chunk_text

import logging

logger = logging.getLogger(__name__)

# Directories to skip when walking a tree
_SKIP_DIRS = frozenset(
    {
        "__pycache__",
        # openjarvis-w83-skipdirs-v1 (owner O-a, W83): build output trees - likely route to the 21 GB corpus
        "target",
        "dist",
        "build",
        ".git",
        ".hg",
        ".svn",
        "node_modules",
        ".venv",
        "venv",
        ".tox",
        ".mypy_cache",
        ".ruff_cache",
        ".pytest_cache",
        "__pypackages__",
        ".eggs",
        "*.egg-info",
    }
)

# Extension -> file-type mapping
_CODE_EXTS = frozenset(
    {
        ".py",
        ".js",
        ".ts",
        ".tsx",
        ".jsx",
        ".rs",
        ".go",
        ".java",
        ".c",
        ".cpp",
        ".h",
        ".hpp",
        ".rb",
        ".sh",
        ".bash",
        ".zsh",
        ".lua",
        ".swift",
        ".kt",
        ".scala",
        ".cs",
        ".r",
        ".sql",
        ".yaml",
        ".yml",
        ".toml",
        ".json",
        ".xml",
        ".html",
        ".css",
    }
)


@dataclass(slots=True)
class DocumentMeta:
    """Metadata about an ingested document."""

    path: str
    file_type: str
    size_bytes: int
    line_count: int


def detect_file_type(path: Path) -> str:
    """Map a file extension to one of: text, markdown, pdf, code."""
    suffix = path.suffix.lower()
    if suffix in {".md", ".markdown", ".mdx"}:
        return "markdown"
    if suffix == ".pdf":
        return "pdf"
    if suffix in _CODE_EXTS:
        return "code"
    return "text"


def read_document(path: Path) -> Tuple[str, DocumentMeta]:
    """Read a file and return ``(text, metadata)``.

    Raises
    ------
    ImportError
        If the file is a PDF and ``pdfplumber`` is not installed.
    FileNotFoundError
        If *path* does not exist.
    """
    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")

    ftype = detect_file_type(path)

    if ftype == "pdf":
        try:
            import pdfplumber  # noqa: F401
        except ImportError:
            raise ImportError(
                "PDF support requires pdfplumber. "
                "Install it with: uv sync --extra memory-pdf"
            ) from None

        text = _read_pdf(path)
    else:
        text = _read_text(path)

    line_count = text.count("\n") + 1 if text else 0
    meta = DocumentMeta(
        path=str(path),
        file_type=ftype,
        size_bytes=path.stat().st_size,
        line_count=line_count,
    )
    return text, meta


# openjarvis-w83-decode-v2 (D-29): ONE decoder for both ingest paths (this file and server/upload_router.py).
# Author defect: utf-8 then latin-1. latin-1 never fails, so UTF-16 text was stored as char+NUL and binaries were
# accepted as text. BOM first, then utf-8, then latin-1; refuse any NUL or >5% control chars (returns None).
def decode_text_bytes(data: bytes, name: str = "") -> Optional[str]:
    enc = None
    try:
        if data[:3] == b"\xef\xbb\xbf":
            text, enc = data[3:].decode("utf-8", errors="replace"), "utf-8-sig"
        elif data[:2] in (b"\xff\xfe", b"\xfe\xff"):
            text, enc = data.decode("utf-16"), "utf-16"
    except UnicodeDecodeError:
        enc = None
    if enc is None:
        try:
            text, enc = data.decode("utf-8"), "utf-8"
        except UnicodeDecodeError:
            text, enc = data.decode("latin-1"), "latin-1"
    nul = text.count("\x00")
    ctl = sum(1 for ch in text if ord(ch) < 32 and ch not in "\t\n\r\f\v")
    if text and (nul > 0 or ctl * 20 > len(text)):
        logger.warning("DECODE refused %s: nul=%d ctl=%d of %d chars after %s decode - not stored", name, nul, ctl, len(text), enc)
        return None
    logger.info("DECODE %s as %s chars=%d", name, enc, len(text))
    return text


def _read_text(path: Path) -> str:
    """Read a text file through decode_text_bytes; refused content raises OSError (walker skips it)."""
    text = decode_text_bytes(path.read_bytes(), str(path))
    if text is None:
        raise OSError("refused undecodable file: %s" % path)
    return text


def _read_pdf(path: Path) -> str:
    """Extract text from a PDF via pdfplumber."""
    import pdfplumber

    pages: List[str] = []
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                pages.append(text)
    return "\n\n".join(pages)


def _should_skip_dir(name: str) -> bool:
    """Return True if directory *name* should be skipped."""
    if name.startswith("."):
        return True
    if name in _SKIP_DIRS:
        return True
    if name.endswith(".egg-info"):
        return True
    return False


def ingest_path(
    path: Path,
    *,
    config: Optional[ChunkConfig] = None,
) -> List[Chunk]:
    """Ingest a file or directory into chunks.

    If *path* is a file, reads and chunks it.
    If *path* is a directory, recursively walks it (skipping hidden and
    common non-content directories) and chunks each file.
    """
    if not path.exists():
        raise FileNotFoundError(f"Path not found: {path}")

    if path.is_file():
        text, _meta = read_document(path)
        return chunk_text(text, source=str(path), config=config)

    # Directory: recursive walk
    all_chunks: List[Chunk] = []
    for child in sorted(path.rglob("*")):
        # Skip directories themselves — rglob yields files too
        if child.is_dir():
            continue

        # Check if any parent directory should be skipped
        rel = child.relative_to(path)
        skip = False
        for part in rel.parts[:-1]:
            if _should_skip_dir(part):
                skip = True
                break
        if skip:
            continue

        # Skip hidden files
        if child.name.startswith("."):
            continue

        # Skip sensitive files (secrets, credentials, keys)
        from openjarvis.security.file_policy import is_sensitive_file

        if is_sensitive_file(child):
            continue

        # Skip binary-looking files
        if child.suffix.lower() in {
            ".png",
            ".jpg",
            ".jpeg",
            ".gif",
            ".bmp",
            ".ico",
            ".mp3",
            ".mp4",
            ".wav",
            ".avi",
            ".mov",
            ".zip",
            ".tar",
            ".gz",
            ".bz2",
            ".7z",
            ".exe",
            ".dll",
            ".so",
            ".dylib",
            ".o",
            ".pyc",
            ".pyo",
            ".class",
            ".wasm",
        }:
            continue

        try:
            text, _meta = read_document(child)
            chunks = chunk_text(text, source=str(child), config=config)
            all_chunks.extend(chunks)
        except (ImportError, OSError):
            # Skip files we can't read (e.g. PDF without pdfplumber)
            continue

    return all_chunks


__all__ = ["DocumentMeta", "detect_file_type", "ingest_path", "read_document"]
