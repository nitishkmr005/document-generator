"""Image editing node for unified workflow."""

from __future__ import annotations

from loguru import logger

from ..unified_state import UnifiedWorkflowState
from ...infrastructure.logging_utils import (
    log_node_start,
    log_node_end,
    log_metric,
    resolve_step_number,
    resolve_total_steps,
)


def edit_image_node(state: UnifiedWorkflowState) -> UnifiedWorkflowState:
    """
    Edit an existing image.

    Supports basic editing, style transfer, and region-based inpainting.

    Args:
        state: Current workflow state with source image and edit instructions

    Returns:
        Updated state with edited image_data
    """
    request_data = state.get("request_data", {})
    api_key = state.get("gemini_api_key") or state.get("api_key", "")

    log_node_start(
        "image_edit",
        step_number=resolve_step_number(state, "image_edit", 1),
        total_steps=resolve_total_steps(state, 1),
    )

    if not api_key:
        state["errors"] = state.get("errors", []) + [
            "Gemini API key required for image editing"
        ]
        log_node_end("image_edit", success=False, details="Missing API key")
        return state

    source_image = request_data.get("image", "")
    prompt = request_data.get("prompt", "")
    edit_mode = request_data.get("edit_mode", "basic")
    style_id = request_data.get("style")
    region = request_data.get("region")

    if not source_image:
        state["errors"] = state.get("errors", []) + [
            "No source image provided for editing"
        ]
        log_node_end("image_edit", success=False, details="Missing source image")
        return state

    if not prompt:
        state["errors"] = state.get("errors", []) + ["No edit instructions provided"]
        log_node_end("image_edit", success=False, details="Missing prompt")
        return state

    logger.info(f"Editing image: mode={edit_mode}")
    log_metric("Edit Mode", edit_mode)

    try:
        from ...infrastructure.image.image_service import ImageService
        from ...domain.image_styles import get_style_by_id

        style = None
        if style_id and edit_mode == "style_transfer":
            style = get_style_by_id(style_id)

        region_dict = None
        if region and edit_mode == "region":
            region_dict = {
                "x": region.get("x", 0),
                "y": region.get("y", 0),
                "width": region.get("width", 100),
                "height": region.get("height", 100),
            }

        service = ImageService(api_key=api_key)

        if not service.is_available():
            state["errors"] = state.get("errors", []) + ["Image service not available"]
            log_node_end("image_edit", success=False, details="Service unavailable")
            return state

        edited_image = service.edit_image(
            image_base64=source_image,
            prompt=prompt,
            style=style,
            region=region_dict,
        )

        if edited_image:
            state["image_data"] = edited_image
            state["image_output_format"] = "png"
            state["image_source"] = source_image
            state["image_edit_mode"] = edit_mode
            state["completed"] = True
            logger.info("Image edited successfully")
            log_node_end("image_edit", success=True, details="Image ready")
        else:
            state["errors"] = state.get("errors", []) + [
                "Image editing returned no data"
            ]
            log_node_end("image_edit", success=False, details="No image data")

    except Exception as e:
        logger.error(f"Image editing failed: {e}")
        state["errors"] = state.get("errors", []) + [
            f"Image editing failed: {str(e)}"
        ]
        log_node_end("image_edit", success=False, details=str(e))

    return state
