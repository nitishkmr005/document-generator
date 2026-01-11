"""
Direct markdown file parser.

Parses markdown files with frontmatter support (Hugo-style).
"""

from pathlib import Path
from typing import Tuple

from loguru import logger

from ...domain.exceptions import ParseError
from ...infrastructure.parsers.file_system import read_text_file, validate_file_exists
from ...utils.markdown_utils import extract_frontmatter, strip_frontmatter


class MarkdownParser:
    """
    Parser for markdown files.

    Extracts YAML frontmatter and preserves markdown structure.
    """

    def parse(self, input_path: str | Path) -> Tuple[str, dict]:
        """
        Parse markdown file.

        Args:
            input_path: Path to markdown file

        Returns:
            Tuple of (markdown_content, metadata)

        Raises:
            ParseError: If parsing fails
        """
        path = Path(input_path)

        try:
            validate_file_exists(path)
        except Exception as e:
            raise ParseError(f"Failed to access markdown file: {e}")

        logger.info(f"Parsing markdown file: {path.name}")

        try:
            content = read_text_file(path)

            # Extract frontmatter using shared utility
            metadata = extract_frontmatter(content)
            metadata["source_file"] = str(path)
            metadata["parser"] = "markdown"

            # Use filename as fallback title
            if "title" not in metadata:
                metadata["title"] = path.stem

            logger.debug(f"Extracted frontmatter: {metadata}")

            # Remove frontmatter from content using shared utility
            content = strip_frontmatter(content)

            logger.info(
                f"Markdown parsing completed: {len(content)} chars, "
                f"title='{metadata.get('title', 'N/A')}'"
            )

            return content, metadata

        except Exception as e:
            logger.error(f"Markdown parsing failed for {path}: {e}")
            raise ParseError(f"Failed to parse markdown: {e}")
