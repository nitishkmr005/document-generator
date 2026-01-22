"""
Source merge node for unified workflow.
"""

from ...infrastructure.logging_utils import (
    log_node_start,
    log_node_end,
    log_metric,
    resolve_step_number,
    resolve_total_steps,
)
from ..unified_state import UnifiedWorkflowState, is_document_type
from ...utils.source_utils import (
    should_skip_source_processing,
    skip_source_reason,
    merge_markdown_sources,
    write_temp_markdown,
)


def merge_sources_node(state: UnifiedWorkflowState) -> UnifiedWorkflowState:
    """
    Merge extracted content blocks into a single raw content payload.
    """
    if should_skip_source_processing(state):
        reason = skip_source_reason(state)
        if reason == "not_required":
            return state
        log_node_start(
            "merge_sources",
            step_number=resolve_step_number(state, "merge_sources", 4),
            total_steps=resolve_total_steps(state, 9),
        )
        log_node_end(
            "merge_sources",
            success=True,
            details=f"Skipped: {reason.replace('_', ' ')}",
        )
        return state

    output_type = state.get("output_type", "")
    content_blocks = state.get("content_blocks", [])

    log_node_start(
        "merge_sources",
        step_number=resolve_step_number(state, "merge_sources", 4),
        total_steps=resolve_total_steps(state, 9),
    )

    if not content_blocks:
        log_node_end("merge_sources", success=False, details="No content to merge")
        return state

    if is_document_type(output_type):
        merged_content = merge_markdown_sources(content_blocks)
    else:
        merged_content = "\n\n---\n\n".join(
            block.get("content", "").strip()
            for block in content_blocks
            if block.get("content", "").strip()
        )

    state["raw_content"] = merged_content
    if is_document_type(output_type):
        temp_path = write_temp_markdown(merged_content)
        state["input_path"] = str(temp_path)

    resolved_file_id = state.pop("resolved_file_id", None)
    if resolved_file_id:
        metadata = state.get("metadata", {})
        metadata["file_id"] = resolved_file_id
        state["metadata"] = metadata

    state.pop("content_blocks", None)
    state.pop("resolved_sources", None)

    log_metric("Content Length", f"{len(merged_content)} chars")
    log_node_end(
        "merge_sources",
        success=True,
        details=f"{len(merged_content)} chars",
    )

    return state
