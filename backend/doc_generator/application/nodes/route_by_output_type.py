"""
Routing helper for unified workflow.
"""

from ..unified_state import UnifiedWorkflowState, get_output_branch


def route_by_output_type(state: UnifiedWorkflowState) -> str:
    """
    Router function to determine which workflow branch to execute.

    Args:
        state: Current workflow state

    Returns:
        Branch name for conditional edge routing
    """
    return get_output_branch(state)
