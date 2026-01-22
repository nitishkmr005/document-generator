"""Image generation node for unified workflow."""

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


def generate_image_node(state: UnifiedWorkflowState) -> UnifiedWorkflowState:
    """
    Generate an image from a text prompt.

    Supports raster (PNG) and SVG output formats.

    Args:
        state: Current workflow state with image configuration

    Returns:
        Updated state with image_data
    """
    request_data = state.get("request_data", {})
    api_key = state.get("gemini_api_key") or state.get("api_key", "")

    log_node_start(
        "image_generate",
        step_number=resolve_step_number(state, "image_generate", 7),
        total_steps=resolve_total_steps(state, 7),
    )

    if not api_key:
        state["errors"] = state.get("errors", []) + [
            "Gemini API key required for image generation"
        ]
        log_node_end("image_generate", success=False, details="Missing API key")
        return state

    prompt = request_data.get("prompt", "")
    style_id = request_data.get("style")
    output_format = request_data.get("output_format", "raster")
    free_text_mode = request_data.get("free_text_mode", False)

    if not prompt:
        state["errors"] = state.get("errors", []) + [
            "No prompt provided for image generation"
        ]
        log_node_end("image_generate", success=False, details="Missing prompt")
        return state

    logger.info(f"Generating image: format={output_format}, style={style_id}")
    log_metric("Output Format", output_format)
    log_metric("Style", style_id or "free_text")

    try:
        from ...infrastructure.image.image_service import ImageService
        from ...domain.image_styles import get_style_by_id

        style = None
        if style_id and not free_text_mode:
            style = get_style_by_id(style_id)

        if output_format == "svg" and style and not style.supports_svg:
            state["errors"] = state.get("errors", []) + [
                f"Style '{style.name}' does not support SVG output"
            ]
            log_node_end("image_generate", success=False, details="SVG not supported")
            return state

        service = ImageService(api_key=api_key)

        if not service.is_available():
            state["errors"] = state.get("errors", []) + ["Image service not available"]
            log_node_end("image_generate", success=False, details="Service unavailable")
            return state

        if output_format == "svg":
            image_data, prompt_used = service.generate_svg(
                prompt=prompt,
                style=style,
                free_text_mode=free_text_mode,
            )
            result_format = "svg"
        else:
            image_data, prompt_used = service.generate_raster_image(
                prompt=prompt,
                style=style,
                free_text_mode=free_text_mode,
            )
            result_format = "png"

        if image_data:
            state["image_data"] = image_data
            state["image_output_format"] = result_format
            state["image_prompt_used"] = prompt_used
            state["completed"] = True
            logger.info(f"Image generated successfully: format={result_format}")
            log_node_end("image_generate", success=True, details="Image ready")
        else:
            state["errors"] = state.get("errors", []) + [
                "Image generation returned no data"
            ]
            log_node_end("image_generate", success=False, details="No image data")

    except Exception as e:
        logger.error(f"Image generation failed: {e}")
        state["errors"] = state.get("errors", []) + [
            f"Image generation failed: {str(e)}"
        ]
        log_node_end("image_generate", success=False, details=str(e))

    return state
