"""
Image generation and editing nodes for unified workflow.

Handles:
- Raster image generation
- SVG generation
- Image editing (basic, style transfer, region-based)
"""

import base64
from typing import Any, Optional

from loguru import logger

from ..unified_state import UnifiedWorkflowState


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

    if not api_key:
        state["errors"] = state.get("errors", []) + [
            "Gemini API key required for image generation"
        ]
        return state

    # Extract image configuration
    prompt = request_data.get("prompt", "")
    style_id = request_data.get("style")
    style_category = request_data.get("style_category")
    output_format = request_data.get("output_format", "raster")
    free_text_mode = request_data.get("free_text_mode", False)

    if not prompt:
        state["errors"] = state.get("errors", []) + [
            "No prompt provided for image generation"
        ]
        return state

    logger.info(f"Generating image: format={output_format}, style={style_id}")

    try:
        from ...infrastructure.image.image_service import (
            ImageService,
            get_image_service,
        )
        from ...domain.image_styles import get_style_by_id

        # Get style if specified
        style = None
        if style_id and not free_text_mode:
            style = get_style_by_id(style_id)

        # Create image service
        service = ImageService(api_key=api_key)

        if not service.is_available():
            state["errors"] = state.get("errors", []) + ["Image service not available"]
            return state

        # Generate based on format
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
        else:
            state["errors"] = state.get("errors", []) + [
                "Image generation returned no data"
            ]

    except Exception as e:
        logger.error(f"Image generation failed: {e}")
        state["errors"] = state.get("errors", []) + [
            f"Image generation failed: {str(e)}"
        ]

    return state


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

    if not api_key:
        state["errors"] = state.get("errors", []) + [
            "Gemini API key required for image editing"
        ]
        return state

    # Extract edit configuration
    source_image = request_data.get("image", "")
    prompt = request_data.get("prompt", "")
    edit_mode = request_data.get("edit_mode", "basic")
    style_id = request_data.get("style")
    region = request_data.get("region")

    if not source_image:
        state["errors"] = state.get("errors", []) + [
            "No source image provided for editing"
        ]
        return state

    if not prompt:
        state["errors"] = state.get("errors", []) + ["No edit instructions provided"]
        return state

    logger.info(f"Editing image: mode={edit_mode}")

    try:
        from ...infrastructure.image.image_service import ImageService
        from ...domain.image_styles import get_style_by_id

        # Get style for style transfer
        style = None
        if style_id and edit_mode == "style_transfer":
            style = get_style_by_id(style_id)

        # Convert region if provided
        region_dict = None
        if region and edit_mode == "region":
            region_dict = {
                "x": region.get("x", 0),
                "y": region.get("y", 0),
                "width": region.get("width", 100),
                "height": region.get("height", 100),
            }

        # Create image service
        service = ImageService(api_key=api_key)

        if not service.is_available():
            state["errors"] = state.get("errors", []) + ["Image service not available"]
            return state

        # Edit image
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
        else:
            state["errors"] = state.get("errors", []) + [
                "Image editing returned no data"
            ]

    except Exception as e:
        logger.error(f"Image editing failed: {e}")
        state["errors"] = state.get("errors", []) + [f"Image editing failed: {str(e)}"]

    return state
