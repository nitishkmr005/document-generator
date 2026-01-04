"""
Output generation node for LangGraph workflow.

Generates PDF or PPTX from structured content.
"""

from pathlib import Path
from loguru import logger

from ...domain.models import WorkflowState
from ..generators import get_generator
from ...domain.exceptions import GenerationError


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

        # Get output directory
        output_dir = Path("src/output")

        # Generate output file
        output_path = generator.generate(
            content=state["structured_content"],
            metadata=state["metadata"],
            output_dir=output_dir
        )

        state["output_path"] = str(output_path)

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
