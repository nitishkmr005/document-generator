"""
Content type enumerations for document generator.

Defines supported input and output formats.
"""

from enum import Enum


class ContentFormat(str, Enum):
    """Supported input content formats."""

    PDF = "pdf"
    MARKDOWN = "md"
    TEXT = "txt"
    URL = "url"
    DOCX = "docx"
    PPTX = "pptx"
    HTML = "html"


class OutputFormat(str, Enum):
    """Supported output formats."""

    PDF = "pdf"
    PPTX = "pptx"
