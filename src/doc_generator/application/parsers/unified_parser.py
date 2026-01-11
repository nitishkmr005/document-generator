"""
Unified parser using Docling for multiple document formats.

Handles PDF, DOCX, PPTX, XLSX, and images with advanced OCR support.
"""

from pathlib import Path
from typing import Tuple

from loguru import logger

from ...domain.exceptions import ParseError
from ...infrastructure.parsers.docling import convert_document_to_markdown, is_docling_available


class UnifiedParser:
    """
    Parser for PDF, DOCX, PPTX, images using Docling.

    Uses IBM Research's Docling library for advanced document parsing
    with OCR, table extraction, and layout analysis.
    """

    def __init__(self):
        if not is_docling_available():
            logger.warning(
                "Docling not available - unified parser will have limited functionality"
            )

    def parse(self, input_path: str | Path) -> Tuple[str, dict]:
        """
        Parse document using Docling.

        Args:
            input_path: Path to input file

        Returns:
            Tuple of (markdown_content, metadata)

        Raises:
            ParseError: If parsing fails
        """
        path = Path(input_path)

        if not path.exists():
            raise ParseError(f"File not found: {path}")

        logger.info(f"Parsing with UnifiedParser (Docling): {path.name}")

        try:
            content, metadata = convert_document_to_markdown(path)

            logger.info(
                f"UnifiedParser completed: {len(content)} chars, "
                f"{metadata.get('pages', 'N/A')} pages"
            )

            return content, metadata

        except Exception as e:
            logger.error(f"UnifiedParser failed for {path}: {e}")
            raise ParseError(f"Failed to parse document: {e}")
