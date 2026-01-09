"""
Configuration module for document generator.

Contains settings and prompts used across the application.

Usage:
    from doc_generator.config import settings, get_settings
    from doc_generator.config.prompts import CONTENT_SYSTEM_PROMPT
"""

# Settings re-export
from .settings import (
    Settings,
    get_settings,
    settings,
)

# Prompt re-exports
from .prompts import (
    CONTENT_SYSTEM_PROMPT,
    CONTENT_GENERATION_PROMPT,
    CONTENT_CHUNK_PROMPT,
    TITLE_GENERATION_PROMPT,
    VISUAL_DATA_PROMPT,
    SVG_ARCHITECTURE_PROMPT,
    SVG_FLOWCHART_PROMPT,
    SVG_COMPARISON_PROMPT,
    SVG_CONCEPT_MAP_PROMPT,
    SVG_MIND_MAP_PROMPT,
    SUMMARY_PROMPT,
)

__all__ = [
    # Settings
    "Settings",
    "get_settings",
    "settings",
    # Prompts
    "CONTENT_SYSTEM_PROMPT",
    "CONTENT_GENERATION_PROMPT",
    "CONTENT_CHUNK_PROMPT",
    "TITLE_GENERATION_PROMPT",
    "VISUAL_DATA_PROMPT",
    "SVG_ARCHITECTURE_PROMPT",
    "SVG_FLOWCHART_PROMPT",
    "SVG_COMPARISON_PROMPT",
    "SVG_CONCEPT_MAP_PROMPT",
    "SVG_MIND_MAP_PROMPT",
    "SUMMARY_PROMPT",
]
