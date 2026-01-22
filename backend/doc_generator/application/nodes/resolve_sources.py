"""
Source resolution node for unified workflow.
"""

from loguru import logger

from ...infrastructure.logging_utils import (
    log_node_start,
    log_node_end,
    log_metric,
    resolve_step_number,
    resolve_total_steps,
)
from ..unified_state import UnifiedWorkflowState
from ...utils.source_utils import (
    coerce_source_dict,
    should_skip_source_processing,
    skip_source_reason,
    set_skip_source_processing,
    resolve_upload_path,
)


def resolve_sources_node(state: UnifiedWorkflowState) -> UnifiedWorkflowState:
    """
    Resolve source references (file IDs → paths, URL/text normalization).
    """
    if should_skip_source_processing(state):
        reason = skip_source_reason(state)
        if reason == "not_required":
            return state
        log_node_start(
            "resolve_sources",
            step_number=resolve_step_number(state, "resolve_sources", 2),
            total_steps=resolve_total_steps(state, 9),
        )
        log_node_end(
            "resolve_sources",
            success=True,
            details=f"Skipped: {reason.replace('_', ' ')}",
        )
        return state

    log_node_start(
        "resolve_sources",
        step_number=resolve_step_number(state, "resolve_sources", 2),
        total_steps=resolve_total_steps(state, 9),
    )

    request_data = state.get("request_data", {})
    sources = request_data.get("sources", [])

    try:
        from ...infrastructure.api.services.storage import StorageService

        storage = StorageService()
        resolved_sources: list[dict] = []
        file_id: str | None = None

        for source in sources:
            source_data = coerce_source_dict(source)
            source_type = source_data.get("type", "")

            if source_type == "file":
                current_file_id = source_data.get("file_id", "")
                if not current_file_id:
                    continue

                if not file_id:
                    file_id = current_file_id

                file_path = resolve_upload_path(storage, current_file_id)
                if not file_path:
                    continue

                if file_path.suffix.lower() in {".xlsx", ".xls"}:
                    state["errors"] = state.get("errors", []) + [
                        "Excel files are not supported."
                    ]
                    set_skip_source_processing(state, "unsupported_format")
                    log_node_end(
                        "resolve_sources",
                        success=False,
                        details="Excel not supported",
                    )
                    return state

                resolved_sources.append(
                    {
                        "type": "file",
                        "file_path": str(file_path),
                        "file_id": current_file_id,
                    }
                )

            elif source_type == "url":
                url = source_data.get("url", "")
                if not url:
                    continue
                resolved_sources.append(
                    {
                        "type": "url",
                        "url": url,
                        "parser": source_data.get("parser"),
                    }
                )

            elif source_type == "text":
                content = source_data.get("content", "")
                if content.strip():
                    resolved_sources.append(
                        {
                            "type": "text",
                            "content": content.strip(),
                        }
                    )

        state["resolved_sources"] = resolved_sources
        if file_id:
            state["resolved_file_id"] = file_id

        log_metric("Resolved Sources", len(resolved_sources))
        log_node_end(
            "resolve_sources",
            success=True,
            details=f"{len(resolved_sources)} sources",
        )

    except Exception as exc:
        logger.error(f"Source resolution failed: {exc}")
        state["errors"] = state.get("errors", []) + [
            f"Source resolution failed: {str(exc)}"
        ]
        set_skip_source_processing(state, "resolution_failed")
        log_node_end("resolve_sources", success=False, details=str(exc))

    return state
