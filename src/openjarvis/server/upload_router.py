"""Upload / Paste router for ingesting documents into the memory backend."""

from __future__ import annotations

import base64
import io
import logging
import uuid
import zipfile
from typing import List, Optional

from fastapi import APIRouter, File, Form, HTTPException, Request, UploadFile
from pydantic import BaseModel

from openjarvis.core.config import DEFAULT_CONFIG_DIR

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/v1/connectors/upload", tags=["upload"])

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

_ALLOWED_EXTENSIONS = {
    ".txt", ".md", ".csv", ".pdf", ".docx",
    ".zip",
    ".png", ".jpg", ".jpeg", ".gif", ".webp", ".bmp", ".tiff",
    ".mp4", ".webm", ".mov", ".mkv", ".avi",
}


def _chunk_text(text: str, max_chars: int = 1000) -> List[str]:
    """Split *text* into ~max_chars pieces at paragraph boundaries."""
    paragraphs = text.split("\n\n")
    chunks: List[str] = []
    current = ""
    for para in paragraphs:
        para = para.strip()
        if not para:
            continue
        if current and len(current) + len(para) + 2 > max_chars:
            chunks.append(current.strip())
            current = para
        else:
            current = f"{current}\n\n{para}" if current else para
    if current.strip():
        chunks.append(current.strip())
    # Guard against very large paragraphs that exceed max_chars
    final: List[str] = []
    for chunk in chunks:
        while len(chunk) > max_chars:
            # Find last space within limit
            split_at = chunk.rfind(" ", 0, max_chars)
            if split_at == -1:
                split_at = max_chars
            final.append(chunk[:split_at].strip())
            chunk = chunk[split_at:].strip()
        if chunk:
            final.append(chunk)
    return final


def _extract_text_from_zip(data: bytes) -> list[tuple[str, bytes, str]]:
    """Extract files from a zip archive. Returns list of (filename, content, extension)."""
    results = []
    with zipfile.ZipFile(io.BytesIO(data), 'r') as zf:
        # Zip bomb protection
        total_uncompressed = sum(info.file_size for info in zf.infolist())
        if total_uncompressed > 100 * 1024 * 1024:  # 100 MB limit
            raise HTTPException(status_code=400, detail='Zip archive too large (uncompressed > 100MB)')
        if len(zf.infolist()) > 500:  # max 500 files
            raise HTTPException(status_code=400, detail='Too many files in archive (max 500)')
        
        for info in zf.infolist():
            # Path traversal protection
            if info.is_dir():
                continue
            name = info.filename
            if name.startswith('/') or '..' in name:
                continue
            ext = ''
            if '.' in name:
                ext = '.' + name.rsplit('.', 1)[-1].lower()
            try:
                file_data = zf.read(info)
                results.append((name, file_data, ext))
            except Exception as e:
                logger.warning('Failed to extract %s from zip: %s', name, e)
    return results


def _process_image(data: bytes, filename: str, ext: str) -> dict:
    """Process image file - return metadata for vision models."""
    b64 = base64.b64encode(data).decode('ascii')
    mime = {
        '.png': 'image/png', '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg',
        '.gif': 'image/gif', '.webp': 'image/webp', '.bmp': 'image/bmp',
        '.tiff': 'image/tiff'
    }.get(ext, 'application/octet-stream')
    return {
        'type': 'image',
        'filename': filename,
        'mime_type': mime,
        'base64': b64,
        'size': len(data),
    }


def _process_video(data: bytes, filename: str, ext: str) -> dict:
    """Process video file - store metadata for now."""
    mime = {
        '.mp4': 'video/mp4', '.webm': 'video/webm', '.mov': 'video/quicktime',
        '.mkv': 'video/x-matroska', '.avi': 'video/x-msvideo'
    }.get(ext, 'application/octet-stream')
    return {
        'type': 'video',
        'filename': filename,
        'mime_type': mime,
        'size': len(data),
        'note': 'Video stored as metadata; transcription not yet implemented',
    }


def _extract_text_from_pdf(data: bytes) -> str:
    """Extract text from a PDF using pdfplumber or PyPDF2."""
    # Try pdfplumber first
    try:
        import pdfplumber  # type: ignore[import-untyped]

        with pdfplumber.open(io.BytesIO(data)) as pdf:
            pages = [p.extract_text() or "" for p in pdf.pages]
        return "\n\n".join(pages)
    except ImportError:
        pass

    # Fall back to PyPDF2
    try:
        from PyPDF2 import PdfReader  # type: ignore[import-untyped]

        reader = PdfReader(io.BytesIO(data))
        pages = [p.extract_text() or "" for p in reader.pages]
        return "\n\n".join(pages)
    except ImportError:
        raise HTTPException(
            status_code=500,
            detail=(
                "PDF parsing requires pdfplumber or PyPDF2. "
                "Install one with: pip install pdfplumber"
            ),
        )


def _extract_text_from_docx(data: bytes) -> str:
    """Extract text from a .docx file using python-docx."""
    try:
        from docx import Document  # type: ignore[import-untyped]

        doc = Document(io.BytesIO(data))
        return "\n\n".join(p.text for p in doc.paragraphs if p.text.strip())
    except ImportError:
        raise HTTPException(
            status_code=500,
            detail=(
                "DOCX parsing requires python-docx. "
                "Install with: pip install python-docx"
            ),
        )


def _get_memory_backend(request: Request):
    """Retrieve the shared memory backend instance from app.state."""
    backend = getattr(request.app.state, "memory_backend", None)
    if backend is None:
        raise HTTPException(
            status_code=503,
            detail="Memory backend not configured. Enable 'agent.context_from_memory' in config.",
        )
    return backend


# ---------------------------------------------------------------------------
# Schemas
# ---------------------------------------------------------------------------


class PasteRequest(BaseModel):
    title: str = ""
    content: str


class IngestResponse(BaseModel):
    chunks_added: int
    source: str = "upload"


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------


@router.post("/ingest", response_model=IngestResponse)
async def ingest_paste(request: Request, body: PasteRequest) -> IngestResponse:
    """Ingest pasted text into the shared memory backend."""
    text = body.content.strip()
    if not text:
        raise HTTPException(status_code=400, detail="Content is empty")

    memory_backend = _get_memory_backend(request)
    doc_id = str(uuid.uuid4())
    chunks = _chunk_text(text)

    for idx, chunk in enumerate(chunks):
        memory_backend.store(
            chunk,
            source="upload",
            metadata={
                "doc_type": "paste",
                "doc_id": doc_id,
                "title": body.title or "Pasted text",
                "chunk_index": idx,
            },
        )

    logger.info("Ingested %d chunks from pasted text (doc_id=%s)", len(chunks), doc_id)
    return IngestResponse(chunks_added=len(chunks))


@router.post("/ingest/files", response_model=IngestResponse)
async def ingest_files(
    request: Request,
    files: List[UploadFile] = File(...),
    title: Optional[str] = Form(None),
) -> IngestResponse:
    """Ingest uploaded files into the shared memory backend."""
    memory_backend = _get_memory_backend(request)
    total_chunks = 0

    for upload in files:
        filename = upload.filename or "untitled"
        ext = ""
        if "." in filename:
            ext = "." + filename.rsplit(".", 1)[-1].lower()

        if ext not in _ALLOWED_EXTENSIONS:
            allowed = ", ".join(sorted(_ALLOWED_EXTENSIONS))
            raise HTTPException(
                status_code=400,
                detail=(f"Unsupported file type: {ext}. Allowed: {allowed}"),
            )

        data = await upload.read()

        # Handle zip archives - extract and process each member
        if ext == ".zip":
            members = _extract_text_from_zip(data)
            for member_name, member_data, member_ext in members:
                if member_ext not in _ALLOWED_EXTENSIONS:
                    logger.info("Skipping unsupported file in zip: %s (%s)", member_name, member_ext)
                    continue
                # Recursively process each member (but not nested zips to avoid loops)
                if member_ext == ".zip":
                    continue
                await _process_single_file(memory_backend, member_name, member_data, member_ext, title)
                total_chunks += 1  # approximate
            continue

        # Process single file
        await _process_single_file(memory_backend, filename, data, ext, title)
        total_chunks += 1  # approximate count

    return IngestResponse(chunks_added=total_chunks)


async def _process_single_file(memory_backend, filename: str, data: bytes, ext: str, title: Optional[str]):
    """Process a single file based on its extension."""
    doc_id = str(uuid.uuid4())
    doc_title = title or filename

    if ext in (".txt", ".md", ".csv"):
        try:
            text = data.decode("utf-8")
        except UnicodeDecodeError:
            text = data.decode("latin-1")
        text = text.strip()
        if not text:
            return
        chunks = _chunk_text(text)
        for idx, chunk in enumerate(chunks):
            memory_backend.store(
                chunk,
                source="upload",
                metadata={
                    "doc_type": ext.lstrip("."),
                    "doc_id": doc_id,
                    "title": doc_title,
                    "chunk_index": idx,
                },
            )
        logger.info("Ingested %d chunks from text file %s (doc_id=%s)", len(chunks), filename, doc_id)

    elif ext == ".pdf":
        text = _extract_text_from_pdf(data)
        text = text.strip()
        if text:
            chunks = _chunk_text(text)
            for idx, chunk in enumerate(chunks):
                memory_backend.store(
                    chunk,
                    source="upload",
                    metadata={
                        "doc_type": "pdf",
                        "doc_id": doc_id,
                        "title": doc_title,
                        "chunk_index": idx,
                    },
                )
            logger.info("Ingested %d chunks from PDF %s (doc_id=%s)", len(chunks), filename, doc_id)

    elif ext == ".docx":
        text = _extract_text_from_docx(data)
        text = text.strip()
        if text:
            chunks = _chunk_text(text)
            for idx, chunk in enumerate(chunks):
                memory_backend.store(
                    chunk,
                    source="upload",
                    metadata={
                        "doc_type": "docx",
                        "doc_id": doc_id,
                        "title": doc_title,
                        "chunk_index": idx,
                    },
                )
            logger.info("Ingested %d chunks from DOCX %s (doc_id=%s)", len(chunks), filename, doc_id)

    elif ext in (".png", ".jpg", ".jpeg", ".gif", ".webp", ".bmp", ".tiff"):
        # Store image as base64 for vision models
        img_meta = _process_image(data, filename, ext)
        memory_backend.store(
            f"[Image: {filename}]",
            source="upload",
            metadata={
                "doc_type": "image",
                "doc_id": doc_id,
                "title": doc_title,
                "image_meta": img_meta,
            },
        )
        logger.info("Stored image %s (doc_id=%s, %d bytes)", filename, doc_id, len(data))

    elif ext in (".mp4", ".webm", ".mov", ".mkv", ".avi"):
        # Store video metadata for now
        vid_meta = _process_video(data, filename, ext)
        memory_backend.store(
            f"[Video: {filename}]",
            source="upload",
            metadata={
                "doc_type": "video",
                "doc_id": doc_id,
                "title": doc_title,
                "video_meta": vid_meta,
            },
        )
        logger.info("Stored video metadata %s (doc_id=%s, %d bytes)", filename, doc_id, len(data))