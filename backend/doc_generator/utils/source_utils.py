"""
Shared helpers for unified source preparation nodes.
"""

import uuid
from pathlib import Path

from loguru import logger

from ..domain.content_types import ContentFormat
from ..infrastructure.settings import get_settings
from ..application.unified_state import UnifiedWorkflowState


def coerce_source_dict(source: object) -> dict:
    """Normalize source models (dict or Pydantic) into a plain dict."""
    if isinstance(source, dict):
        return source
    if hasattr(source, "model_dump"):
        try:
            return source.model_dump()  # type: ignore[no-any-return]
        except Exception:
            return {}
    if hasattr(source, "dict"):
        try:
            return source.dict()  # type: ignore[no-any-return]
        except Exception:
            return {}
    return {}


def should_skip_source_processing(state: UnifiedWorkflowState) -> bool:
    metadata = state.get("metadata", {})
    return bool(metadata.get("skip_source_processing"))


def skip_source_reason(state: UnifiedWorkflowState) -> str:
    metadata = state.get("metadata", {})
    return metadata.get("skip_source_reason", "")


def set_skip_source_processing(state: UnifiedWorkflowState, reason: str) -> None:
    metadata = state.get("metadata", {})
    metadata["skip_source_processing"] = True
    metadata["skip_source_reason"] = reason
    state["metadata"] = metadata


def detect_format(file_path: Path) -> str:
    """Detect content format from file extension."""
    suffix = file_path.suffix.lower()
    format_map = {
        ".pdf": ContentFormat.PDF.value,
        ".md": ContentFormat.MARKDOWN.value,
        ".markdown": ContentFormat.MARKDOWN.value,
        ".txt": ContentFormat.TEXT.value,
        ".docx": ContentFormat.DOCX.value,
        ".pptx": ContentFormat.PPTX.value,
        ".html": ContentFormat.HTML.value,
    }
    return format_map.get(suffix, ContentFormat.TEXT.value)


def merge_markdown_sources(parsed_blocks: list[dict]) -> str:
    """Merge parsed markdown sources into a single document."""
    sections = []
    for block in parsed_blocks:
        title = block.get("title", "Source")
        source = block.get("source", "")
        content = block.get("content", "")
        header = f"## Source: {title}"
        if source and source != "text":
            header += f"\n\nSource: {source}"
        sections.append(f"{header}\n\n{content}")
    return "\n\n---\n\n".join(sections)


def resolve_upload_path(storage, file_id: str) -> Path | None:
    """Resolve file_id to a stored file path."""
    try:
        return storage.get_upload_path(file_id)
    except FileNotFoundError:
        pattern = f"{file_id}*"
        matches = list(storage.upload_dir.glob(pattern))
        if matches:
            return matches[0]
        logger.warning(f"File not found: {file_id}")
        return None


def write_temp_markdown(content: str) -> Path:
    """Write merged markdown to a temp file and return its path."""
    settings = get_settings()
    temp_dir = settings.generator.temp_dir
    temp_dir.mkdir(parents=True, exist_ok=True)
    temp_path = temp_dir / f"temp_input_{uuid.uuid4().hex}.md"
    temp_path.write_text(content, encoding="utf-8")
    logger.info(f"Created temp input file: {temp_path}")
    return temp_path
