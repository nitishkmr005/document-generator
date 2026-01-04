"""
Content transformation node for LangGraph workflow.

Transforms raw content into structured format for generators.
"""

from loguru import logger

from ...domain.models import WorkflowState


def transform_content_node(state: WorkflowState) -> WorkflowState:
    """
    Transform raw content into structured format for generators.

    Structures content for both PDF and PPTX generation by:
    - Storing raw markdown content
    - Extracting title and metadata
    - Preparing structured dictionary

    Args:
        state: Current workflow state

    Returns:
        Updated state with structured_content
    """
    try:
        content = state.get("raw_content", "")
        metadata = state.get("metadata", {})

        # For this simple implementation, we pass markdown through
        # Generators will parse it themselves using pdf_utils.parse_markdown_lines
        structured = {
            "markdown": content,
            "title": metadata.get("title", "Document"),
        }

        state["structured_content"] = structured

        logger.info(f"Transformed content: title='{structured['title']}', {len(content)} chars")

    except Exception as e:
        error_msg = f"Transformation failed: {str(e)}"
        state["errors"].append(error_msg)
        logger.error(error_msg)

    return state
