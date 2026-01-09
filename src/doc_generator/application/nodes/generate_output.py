"""
Output generation node for LangGraph workflow.

Generates PDF or PPTX from structured content.
"""

from pathlib import Path

from loguru import logger

from ...domain.exceptions import GenerationError
from ...domain.models import WorkflowState
from ...infrastructure.settings import get_settings
from ..generators import get_generator


def generate_output_node(state: WorkflowState) -> WorkflowState:
    """
    Generate PDF or PPTX from structured content.

    Args:
        state: Current workflow state

    Returns:
        Updated state with output_path
    """
    try:
        # Get appropriate generator
        generator = get_generator(state["output_format"])

        # Check if custom output_path is provided
        custom_output_path = state.get("output_path", "")

        if custom_output_path:
            # Use custom output path if provided
            custom_path = Path(custom_output_path)
            output_dir = custom_path.parent
            # Generate with custom path by passing output_dir and using metadata to set filename
            state["metadata"]["custom_filename"] = custom_path.stem
            output_path = generator.generate(
                content=state["structured_content"],
                metadata=state["metadata"],
                output_dir=output_dir
            )
        else:
            # Get default output directory from settings
            settings = get_settings()

            # Create topic-specific output directory
            # Get folder name from metadata or derive from input path
            folder_name = state["metadata"].get("custom_filename")
            if not folder_name:
                input_path = state.get("input_path", "")
                if input_path:
                    input_p = Path(input_path)
                    # Use parent folder name if input is a file, or folder name if input is a folder
                    folder_name = input_p.parent.name if input_p.is_file() else input_p.name
                else:
                    folder_name = "output"

            topic_output_dir = settings.generator.output_dir / folder_name
            topic_output_dir.mkdir(parents=True, exist_ok=True)

            # Generate output file in topic subfolder
            output_path = generator.generate(
                content=state["structured_content"],
                metadata=state["metadata"],
                output_dir=topic_output_dir
            )

        state["output_path"] = str(output_path)

        # Cache structured content for future use
        metadata = state.get("metadata", {})
        if metadata.get("cache_content", False):
            from ...utils.content_cache import save_structured_content
            input_path = state.get("input_path", "")
            if input_path:
                save_structured_content(state["structured_content"], input_path)

        logger.info(f"Generated output: {output_path}")

    except GenerationError as e:
        error_msg = f"Generation failed: {str(e)}"
        state["errors"].append(error_msg)
        logger.error(error_msg)

    except Exception as e:
        error_msg = f"Unexpected generation error: {str(e)}"
        state["errors"].append(error_msg)
        logger.error(error_msg)

    return state
