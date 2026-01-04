"""
Direct markdown file parser.

Parses markdown files with frontmatter support (Hugo-style).
"""

from pathlib import Path
from typing import Tuple
import re
from loguru import logger

from ...infrastructure.file_system import read_text_file, validate_file_exists
from ...domain.exceptions import ParseError


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

            # Extract frontmatter
            metadata = self._extract_frontmatter(content)
            metadata["source_file"] = str(path)
            metadata["parser"] = "markdown"

            # Remove frontmatter from content
            content = self._strip_frontmatter(content)

            logger.info(
                f"Markdown parsing completed: {len(content)} chars, "
                f"title='{metadata.get('title', 'N/A')}'"
            )

            return content, metadata

        except Exception as e:
            logger.error(f"Markdown parsing failed for {path}: {e}")
            raise ParseError(f"Failed to parse markdown: {e}")

    def _extract_frontmatter(self, text: str) -> dict:
        """
        Extract YAML frontmatter from markdown.

        Args:
            text: Markdown text

        Returns:
            Dictionary of metadata from frontmatter
        """
        metadata = {}

        # Check for frontmatter
        frontmatter_match = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)

        if frontmatter_match:
            fm_text = frontmatter_match.group(1)

            # Simple YAML parsing (title, author, date)
            title_match = re.search(r"title:\s*(.+)", fm_text)
            if title_match:
                metadata["title"] = title_match.group(1).strip('"\'')

            author_match = re.search(r"author:\s*(.+)", fm_text)
            if author_match:
                metadata["author"] = author_match.group(1).strip('"\'')

            date_match = re.search(r"date:\s*(.+)", fm_text)
            if date_match:
                metadata["date"] = date_match.group(1).strip('"\'')

            logger.debug(f"Extracted frontmatter: {metadata}")

        # Use filename as fallback title
        if "title" not in metadata:
            metadata["title"] = Path(text).stem if hasattr(text, "stem") else "Document"

        return metadata

    def _strip_frontmatter(self, text: str) -> str:
        """
        Remove YAML frontmatter from markdown.

        Args:
            text: Markdown text

        Returns:
            Text with frontmatter removed
        """
        if text.startswith("---"):
            parts = text.split("---", 2)
            if len(parts) == 3:
                return parts[2].lstrip()

        return text
