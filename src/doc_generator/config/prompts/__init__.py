"""
Prompt templates for LLM-powered document generation.

Centralizes all prompts used across the application for:
- Content transformation (blog generation)
- Visual/SVG generation
- Summaries and titles
"""

from .content_prompts import (
    CONTENT_SYSTEM_PROMPT,
    CONTENT_GENERATION_PROMPT,
    CONTENT_CHUNK_PROMPT,
    TITLE_GENERATION_PROMPT,
    TYPE_INSTRUCTIONS,
)

from .visual_prompts import (
    VISUAL_DATA_PROMPT,
    VISUAL_DATA_FORMATS,
    SVG_ARCHITECTURE_PROMPT,
    SVG_FLOWCHART_PROMPT,
    SVG_COMPARISON_PROMPT,
    SVG_CONCEPT_MAP_PROMPT,
    SVG_MIND_MAP_PROMPT,
)

from .summary_prompts import (
    SUMMARY_PROMPT,
    EXECUTIVE_SUMMARY_PROMPT,
    SLIDE_STRUCTURE_PROMPT,
)

__all__ = [
    # Content prompts
    "CONTENT_SYSTEM_PROMPT",
    "CONTENT_GENERATION_PROMPT",
    "CONTENT_CHUNK_PROMPT",
    "TITLE_GENERATION_PROMPT",
    "TYPE_INSTRUCTIONS",
    # Visual prompts
    "VISUAL_DATA_PROMPT",
    "VISUAL_DATA_FORMATS",
    "SVG_ARCHITECTURE_PROMPT",
    "SVG_FLOWCHART_PROMPT",
    "SVG_COMPARISON_PROMPT",
    "SVG_CONCEPT_MAP_PROMPT",
    "SVG_MIND_MAP_PROMPT",
    # Summary prompts
    "SUMMARY_PROMPT",
    "EXECUTIVE_SUMMARY_PROMPT",
    "SLIDE_STRUCTURE_PROMPT",
]
