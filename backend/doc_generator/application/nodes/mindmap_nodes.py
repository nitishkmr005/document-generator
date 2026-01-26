"""
Mind map generation nodes for unified workflow.

Handles:
- Content analysis and concept extraction
- Mind map tree structure generation
"""

import json
import os

from loguru import logger

from ..unified_state import UnifiedWorkflowState


def generate_mindmap_node(state: UnifiedWorkflowState) -> UnifiedWorkflowState:
    """
    Generate mind map from extracted content.

    Uses LLM to analyze content and create a hierarchical mind map structure.

    Args:
        state: Current workflow state with raw_content

    Returns:
        Updated state with mindmap_tree
    """
    request_data = state.get("request_data", {})
    raw_content = state.get("summary_content") or state.get("raw_content", "")
    api_key = state.get("api_key", "")

    if not raw_content:
        state["errors"] = state.get("errors", []) + ["No content for mind map"]
        return state

    # Extract mindmap configuration
    mode = request_data.get("mode", "summarize")
    provider = request_data.get("provider", "gemini")
    model = request_data.get("model", "gemini-2.5-flash")

    logger.info(f"Generating mind map: mode={mode}")

    try:
        source_count = state.get("metadata", {}).get("source_count", 1)
        tree = generate_mindmap_tree(
            content=raw_content,
            mode=mode,
            provider=provider,
            model=model,
            api_key=api_key,
            source_count=source_count,
        )
        if not tree:
            state["errors"] = state.get("errors", []) + [
                "Failed to build mind map"
            ]
            return state

        state["mindmap_tree"] = tree
        state["mindmap_mode"] = mode
        state["completed"] = True

        logger.info(f"Generated mind map with root: {tree.get('title', 'Untitled')}")

    except Exception as e:
        logger.error(f"Mind map generation failed: {e}")
        state["errors"] = state.get("errors", []) + [
            f"Mind map generation failed: {str(e)}"
        ]

    return state


def generate_mindmap_tree(
    content: str,
    mode: str,
    provider: str,
    model: str,
    api_key: str,
    source_count: int,
) -> dict | None:
    """Generate a mind map tree from content."""
    if not content:
        return None

    from ...infrastructure.llm import LLMService

    provider_name = provider if provider != "google" else "gemini"

    key_mapping = {
        "gemini": "GOOGLE_API_KEY",
        "openai": "OPENAI_API_KEY",
        "anthropic": "ANTHROPIC_API_KEY",
    }
    env_var = key_mapping.get(provider_name)
    if env_var and api_key:
        os.environ[env_var] = api_key

    llm_service = LLMService(provider=provider_name, model=model)

    prompt = _build_mindmap_prompt(content, mode, source_count)
    response = llm_service.generate(prompt)
    if not response:
        return None

    mindmap_json = _extract_json(response)
    if not mindmap_json:
        return None

    return _build_tree_structure(mindmap_json, mode, source_count)


def _build_mindmap_prompt(content: str, mode: str, source_count: int) -> str:
    """Build LLM prompt for mind map generation."""
    if mode == "summarize":
        return f"""Analyze the following content and create a mind map structure.

CONTENT:
{content}

Create a mind map that captures the key concepts and their relationships.
The mind map should have a central topic with 3-7 main branches, each with relevant sub-branches.

OUTPUT FORMAT (JSON):
{{
  "title": "Main Topic",
  "summary": "Brief summary of the content",
  "central_node": {{
    "label": "Central Topic",
    "children": [
      {{
        "label": "Main Branch 1",
        "children": [
          {{"label": "Sub-topic 1.1"}},
          {{"label": "Sub-topic 1.2"}}
        ]
      }},
      {{
        "label": "Main Branch 2",
        "children": [
          {{"label": "Sub-topic 2.1"}}
        ]
      }}
    ]
  }}
}}

Based on {source_count} source document(s), create a comprehensive mind map."""

    elif mode == "detailed":
        return f"""Analyze the following content and create a detailed mind map structure.

CONTENT:
{content}

Create a comprehensive mind map with:
- Clear central topic
- 5-10 main branches covering all major themes
- 2-4 sub-branches per main branch
- Include specific details, facts, and concepts

OUTPUT FORMAT (JSON):
{{
  "title": "Main Topic",
  "summary": "Comprehensive summary",
  "central_node": {{
    "label": "Central Topic",
    "children": [...]
  }}
}}

Based on {source_count} source document(s), be thorough and detailed."""

    else:  # hierarchical
        return f"""Analyze the following content and create a hierarchical mind map.

CONTENT:
{content}

Create a structured hierarchical mind map that shows:
- Clear parent-child relationships
- Logical groupings of concepts
- Multiple levels of depth where appropriate

OUTPUT FORMAT (JSON):
{{
  "title": "Main Topic",
  "summary": "Brief summary",
  "central_node": {{
    "label": "Central Topic",
    "children": [...]
  }}
}}

Based on {source_count} source document(s), focus on clear hierarchy."""


def _build_tree_structure(data: dict, mode: str, source_count: int) -> dict:
    """Build the mind map tree structure from parsed JSON."""
    title = data.get("title", "Mind Map")
    summary = data.get("summary", "")
    central_node = data.get("central_node") or data.get("root") or data.get("nodes")

    if not central_node:
        # Try to find node structure in the response
        if "label" in data:
            central_node = data
        else:
            central_node = {"label": title, "children": []}

    # Recursively parse nodes
    nodes = _parse_mindmap_item(central_node)

    return {
        "title": title,
        "summary": summary,
        "mode": mode,
        "source_count": source_count,
        "nodes": nodes,
    }


def _parse_mindmap_item(node_data: dict) -> dict:
    """Recursively parse node data into the expected format."""
    if not node_data:
        return {"label": "Unknown", "children": []}

    label = node_data.get("label", node_data.get("name", node_data.get("text", "Node")))
    children = node_data.get("children", [])

    parsed_children = [
        _parse_mindmap_item(child) for child in children if isinstance(child, dict)
    ]

    result = {"label": label}
    if parsed_children:
        result["children"] = parsed_children

    return result


def _extract_json(text: str) -> dict | None:
    """Extract JSON object from text."""
    if not text:
        return None

    def _parse_candidate(candidate: str) -> dict | None:
        try:
            parsed = json.loads(candidate)
            return parsed if isinstance(parsed, dict) else None
        except json.JSONDecodeError:
            return None

    direct = _parse_candidate(text)
    if direct is not None:
        return direct

    cleaned = text.strip()
    if cleaned.startswith("```json"):
        cleaned = cleaned[7:]
    elif cleaned.startswith("```"):
        cleaned = cleaned[3:]
    if cleaned.endswith("```"):
        cleaned = cleaned[:-3]
    cleaned = cleaned.strip()

    cleaned_parsed = _parse_candidate(cleaned)
    if cleaned_parsed is not None:
        return cleaned_parsed

    start_idx = cleaned.find("{")
    if start_idx == -1:
        return None

    brace_count = 0
    in_string = False
    escape_next = False

    for i in range(start_idx, len(cleaned)):
        ch = cleaned[i]
        if escape_next:
            escape_next = False
            continue
        if ch == "\\":
            escape_next = True
            continue
        if ch == '"' and not escape_next:
            in_string = not in_string
            continue
        if in_string:
            continue
        if ch == "{":
            brace_count += 1
        elif ch == "}":
            brace_count -= 1
            if brace_count == 0:
                return _parse_candidate(cleaned[start_idx : i + 1])

    return None
