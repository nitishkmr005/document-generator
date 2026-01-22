"""
Source extraction node for unified workflow.
"""

from pathlib import Path

from loguru import logger

from ...infrastructure.logging_utils import (
    log_node_start,
    log_node_end,
    log_metric,
    resolve_step_number,
    resolve_total_steps,
)
from ...utils.image_understanding import extract_image_content, is_image_file
from ..unified_state import UnifiedWorkflowState
from ...utils.source_utils import (
    should_skip_source_processing,
    skip_source_reason,
    set_skip_source_processing,
    detect_format,
)


def extract_sources_node(state: UnifiedWorkflowState) -> UnifiedWorkflowState:
    """
    Extract content from resolved sources.
    """
    if should_skip_source_processing(state):
        reason = skip_source_reason(state)
        if reason == "not_required":
            return state
        log_node_start(
            "extract_sources",
            step_number=resolve_step_number(state, "extract_sources", 3),
            total_steps=resolve_total_steps(state, 9),
        )
        log_node_end(
            "extract_sources",
            success=True,
            details=f"Skipped: {reason.replace('_', ' ')}",
        )
        return state

    request_data = state.get("request_data", {})
    api_key = state.get("api_key", "")
    provider = request_data.get("provider", "gemini")
    model = request_data.get("model", "gemini-2.5-flash")

    log_node_start(
        "extract_sources",
        step_number=resolve_step_number(state, "extract_sources", 3),
        total_steps=resolve_total_steps(state, 9),
    )

    try:
        from ..parsers import WebParser, get_parser

        content_blocks: list[dict] = []
        source_count = 0

        provider_name = provider.lower()
        if provider_name == "google":
            provider_name = "gemini"

        for source in state.get("resolved_sources", []):
            source_type = source.get("type", "")

            if source_type == "file":
                file_path_str = source.get("file_path", "")
                if not file_path_str:
                    continue
                file_path = Path(file_path_str)

                if is_image_file(file_path):
                    content, metadata = extract_image_content(
                        file_path,
                        provider_name,
                        model,
                        api_key,
                    )
                else:
                    parser = get_parser(detect_format(file_path))
                    content, metadata = parser.parse(file_path)

                if content:
                    title = metadata.get("title") or file_path.name
                    content_blocks.append(
                        {
                            "title": title,
                            "source": str(file_path),
                            "content": content,
                        }
                    )
                    source_count += 1
                    logger.debug(f"Parsed file: {file_path}")

            elif source_type == "url":
                url = source.get("url", "")
                if not url:
                    continue

                parser_type = source.get("parser")
                parser = WebParser(parser=parser_type)
                content, metadata = parser.parse(url)
                if content:
                    title = metadata.get("title") or url
                    content_blocks.append(
                        {
                            "title": title,
                            "source": url,
                            "content": content,
                        }
                    )
                    source_count += 1
                    logger.debug(f"Parsed URL: {url}")

            elif source_type == "text":
                content = source.get("content", "")
                if content.strip():
                    content_blocks.append(
                        {
                            "title": "Copied Text",
                            "source": "text",
                            "content": content.strip(),
                        }
                    )
                    source_count += 1
                    logger.debug("Added text content")

        if not content_blocks:
            state["errors"] = state.get("errors", []) + ["No valid sources provided"]
            set_skip_source_processing(state, "no_valid_sources")
            log_node_end("extract_sources", success=False, details="No valid sources")
            return state

        state["content_blocks"] = content_blocks
        metadata = state.get("metadata", {})
        metadata["source_count"] = source_count
        state["metadata"] = metadata

        log_metric("Parsed Sources", source_count)
        log_node_end(
            "extract_sources", success=True, details=f"{source_count} sources"
        )

    except Exception as exc:
        logger.error(f"Content extraction failed: {exc}")
        state["errors"] = state.get("errors", []) + [
            f"Content extraction failed: {str(exc)}"
        ]
        set_skip_source_processing(state, "extraction_failed")
        log_node_end("extract_sources", success=False, details=str(exc))

    return state
