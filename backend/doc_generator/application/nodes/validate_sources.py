"""
Source validation node for unified workflow.
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
from ..unified_state import UnifiedWorkflowState, is_document_type, requires_content_extraction
from ...utils.source_utils import set_skip_source_processing


def validate_sources_node(state: UnifiedWorkflowState) -> UnifiedWorkflowState:
    """
    Validate sources for unified workflow.

    Ensures sources exist and handles checkpoint reuse decisions.
    """
    output_type = state.get("output_type", "")

    if not requires_content_extraction(output_type):
        set_skip_source_processing(state, "not_required")
        return state

    if state.get("metadata", {}).get("reused_content") and state.get("raw_content"):
        if is_document_type(output_type):
            input_path = state.get("input_path", "")
            if input_path and Path(input_path).exists():
                log_node_start(
                    "validate_sources",
                    step_number=resolve_step_number(state, "validate_sources", 1),
                    total_steps=resolve_total_steps(state, 9),
                )
                logger.info("Reusing extracted content from checkpoint")
                set_skip_source_processing(state, "reused_content")
                log_node_end(
                    "validate_sources", success=True, details="Reused checkpoint"
                )
                return state
        else:
            log_node_start(
                "validate_sources",
                step_number=resolve_step_number(state, "validate_sources", 1),
                total_steps=resolve_total_steps(state, 9),
            )
            logger.info("Reusing extracted content from checkpoint")
            set_skip_source_processing(state, "reused_content")
            log_node_end("validate_sources", success=True, details="Reused checkpoint")
            return state

    log_node_start(
        "validate_sources",
        step_number=resolve_step_number(state, "validate_sources", 1),
        total_steps=resolve_total_steps(state, 9),
    )

    request_data = state.get("request_data", {})
    sources = request_data.get("sources", [])
    direct_prompt = (request_data.get("prompt") or "").strip()

    if not sources:
        if output_type == "image_generate" and direct_prompt:
            set_skip_source_processing(state, "direct_prompt")
            log_node_end("validate_sources", success=True, details="Direct prompt")
            return state
        state["errors"] = state.get("errors", []) + ["No sources provided"]
        set_skip_source_processing(state, "no_sources")
        log_node_end("validate_sources", success=False, details="No sources")
        return state

    log_metric("Sources", len(sources))
    log_node_end("validate_sources", success=True, details=f"{len(sources)} sources")
    return state
