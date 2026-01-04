"""
Generators for different output formats.

Provides factory function to get appropriate generator for output format.
"""

from .pdf_generator import PDFGenerator
from .pptx_generator import PPTXGenerator

from ...domain.content_types import OutputFormat
from ...domain.exceptions import UnsupportedFormatError


def get_generator(output_format: str):
    """
    Get appropriate generator for output format.

    Args:
        output_format: Output format (pdf, pptx)

    Returns:
        Generator instance

    Raises:
        UnsupportedFormatError: If format is not supported
    """
    format_lower = output_format.lower()

    if format_lower in ["pdf", OutputFormat.PDF]:
        return PDFGenerator()

    if format_lower in ["pptx", "ppt", OutputFormat.PPTX]:
        return PPTXGenerator()

    raise UnsupportedFormatError(f"Unsupported output format: {output_format}")


__all__ = ["PDFGenerator", "PPTXGenerator", "get_generator"]
