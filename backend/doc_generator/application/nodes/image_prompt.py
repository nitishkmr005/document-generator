"""
Image prompt preparation node for unified workflow.

Builds an image prompt from summarized content (mind map) and optional user focus.
"""

from collections import deque

from loguru import logger

from ..unified_state import UnifiedWorkflowState
from ...infrastructure.logging_utils import (
    log_node_start,
    log_node_end,
    log_metric,
    log_progress,
    resolve_step_number,
    resolve_total_steps,
)
from .mindmap_nodes import generate_mindmap_tree


MAX_IMAGE_PROMPT_CHARS = 3600
MAX_MINDMAP_OUTLINE_NODES = 30
MAX_MINDMAP_OUTLINE_DEPTH = 3


def build_image_prompt_node(state: UnifiedWorkflowState) -> UnifiedWorkflowState:
    """
    Build an image prompt from summarized sources.

    If sources exist, generate a mind map (summarize mode) and derive a structured prompt.
    If no sources exist, use the user-provided prompt directly.
    """
    log_node_start(
        "build_image_prompt",
        step_number=resolve_step_number(state, "build_image_prompt", 6),
        total_steps=resolve_total_steps(state, 7),
    )

    request_data = state.get("request_data", {})
    user_prompt = (request_data.get("prompt") or "").strip()
    content = (state.get("summary_content") or state.get("raw_content") or "").strip()

    if not content:
        if not user_prompt:
            state["errors"] = state.get("errors", []) + [
                "No prompt or sources provided for image generation"
            ]
            log_node_end(
                "build_image_prompt", success=False, details="Missing prompt"
            )
            return state

        _set_image_prompt(state, user_prompt, source="user_prompt")
        log_metric("Prompt Source", "user prompt")
        log_metric("Prompt Length", f"{len(user_prompt)} chars")
        log_node_end("build_image_prompt", success=True, details="Prompt ready")
        return state

    provider = request_data.get("provider", "gemini")
    model = request_data.get("model", "gemini-2.5-flash")
    api_key = state.get("api_key", "")
    source_count = state.get("metadata", {}).get("source_count", 1)

    log_metric("Provider", provider)
    log_metric("Model", model)
    log_metric("Content Length", f"{len(content)} chars")
    log_progress("Generating mind map for image prompt")

    try:
        tree = generate_mindmap_tree(
            content=content,
            mode="summarize",
            provider=provider,
            model=model,
            api_key=api_key,
            source_count=source_count,
        )
    except Exception as exc:
        logger.error(f"Mind map generation failed: {exc}")
        tree = None

    if not tree:
        prompt = _build_image_prompt_from_summary(content, user_prompt)
        _set_image_prompt(state, prompt, source="summary_fallback")
        log_metric("Prompt Source", "summary fallback")
        log_metric("Prompt Length", f"{len(prompt)} chars")
        log_node_end("build_image_prompt", success=True, details="Prompt ready")
        return state

    prompt = _build_image_prompt_from_tree(tree, user_prompt)
    _set_image_prompt(state, prompt, source="mindmap")

    log_metric("Prompt Source", "mindmap")
    log_metric("Prompt Length", f"{len(prompt)} chars")
    log_node_end("build_image_prompt", success=True, details="Prompt ready")
    return state


def _set_image_prompt(state: UnifiedWorkflowState, prompt: str, source: str) -> None:
    state["image_prompt"] = prompt
    request_data = state.get("request_data", {})
    request_data["prompt"] = prompt
    state["request_data"] = request_data
    metadata = state.get("metadata", {})
    metadata["image_prompt_source"] = source
    state["metadata"] = metadata


def _build_image_prompt_from_tree(tree: dict, user_prompt: str) -> str:
    outline = _build_mindmap_outline(tree.get("nodes", {}))
    parts: list[str] = []

    parts.append("Create an image that strictly reflects the source content.")
    if user_prompt:
        parts.append(f"User focus: {user_prompt}")
    if tree.get("title"):
        parts.append(f"Title: {tree['title']}")
    if tree.get("summary"):
        parts.append(f"Summary: {tree['summary']}")
    nodes = tree.get("nodes", {}) or {}
    if nodes.get("label"):
        parts.append(f"Central topic: {nodes['label']}")
    if outline:
        parts.append(f"Key points:\n{chr(10).join(outline)}")
    parts.append("Use only these points. Do not add extra concepts or labels.")

    return _clamp_text("\n".join(parts), MAX_IMAGE_PROMPT_CHARS)


def _build_image_prompt_from_summary(summary: str, user_prompt: str) -> str:
    parts: list[str] = []
    parts.append("Create an image that strictly reflects the source content.")
    if user_prompt:
        parts.append(f"User focus: {user_prompt}")
    parts.append(f"Summary: {summary}")
    parts.append("Use only this summary. Do not add extra concepts or labels.")
    return _clamp_text("\n".join(parts), MAX_IMAGE_PROMPT_CHARS)


def _build_mindmap_outline(
    root: dict,
    max_nodes: int = MAX_MINDMAP_OUTLINE_NODES,
    max_depth: int = MAX_MINDMAP_OUTLINE_DEPTH,
) -> list[str]:
    lines: list[str] = []
    queue: deque[tuple[dict, int]] = deque()

    children = root.get("children") or []
    if children:
        for child in children:
            if isinstance(child, dict):
                queue.append((child, 1))
    else:
        if root:
            queue.append((root, 1))

    while queue and len(lines) < max_nodes:
        node, depth = queue.popleft()
        label = node.get("label")
        if not label:
            continue
        prefix = "  " * max(0, depth - 1)
        lines.append(f"{prefix}- {label}")

        if depth < max_depth:
            for child in node.get("children") or []:
                if isinstance(child, dict):
                    queue.append((child, depth + 1))

    return lines


def _clamp_text(text: str, max_chars: int) -> str:
    if len(text) <= max_chars:
        return text
    return text[:max_chars].rstrip()
