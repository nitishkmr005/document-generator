"""
Protocol interfaces for parsers and generators.

Defines abstract interfaces that implementations must follow.
"""

from typing import Protocol, Tuple
from pathlib import Path


class ContentParser(Protocol):
    """
    Protocol for content parsers.

    All parsers must implement the parse() method to extract content
    and metadata from input sources.
    """

    def parse(self, input_path: str | Path) -> Tuple[str, dict]:
        """
        Parse input and extract content.

        Args:
            input_path: Path to input file or URL

        Returns:
            Tuple of (content_text, metadata_dict)

        Raises:
            ParseError: If parsing fails
        """
        ...


class OutputGenerator(Protocol):
    """
    Protocol for output generators.

    All generators must implement the generate() method to create
    output documents from structured content.
    """

    def generate(self, content: dict, metadata: dict, output_dir: Path) -> Path:
        """
        Generate output document from structured content.

        Args:
            content: Structured content dictionary
            metadata: Document metadata
            output_dir: Output directory for generated file

        Returns:
            Path to generated document

        Raises:
            GenerationError: If generation fails
        """
        ...
