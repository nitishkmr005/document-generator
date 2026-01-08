"""
Content merger utility for combining multiple parsed documents into a single output.

This module provides functions to merge content from multiple files in a folder
into a cohesive document suitable for PDF or PPTX generation.
"""

from datetime import datetime
from pathlib import Path
from typing import Optional

from loguru import logger

from ..infrastructure.llm_service import LLMService
from ..infrastructure.settings import get_settings
from .content_cleaner import clean_content_for_output


def merge_folder_content(
    parsed_contents: list[dict],
    folder_name: str,
    llm_service: Optional[LLMService] = None
) -> dict:
    """
    Merge content from multiple parsed files into a single document.

    Args:
        parsed_contents: List of parsed content dicts with keys:
            - filename: Original filename
            - raw_content: Raw parsed content
            - structured_content: Structured content
            - metadata: File metadata
        folder_name: Name of the folder (used as topic/title)
        llm_service: Optional LLM service for generating summary

    Returns:
        Dict with:
            - temp_file: Path to temporary merged markdown file
            - metadata: Combined metadata
            - num_files: Number of files merged
    """
    logger.info(f"Merging {len(parsed_contents)} files into single document")

    # Build merged document
    sections = []

    # Add title based on folder name
    title = folder_name.replace("-", " ").replace("_", " ").title()
    sections.append(f"# {title}\n")

    # Add metadata section
    sections.append(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    sections.append(f"**Source Files:** {len(parsed_contents)}\n")
    sections.append("\n---\n\n")

    # Add table of contents if multiple files
    if len(parsed_contents) > 1:
        sections.append("## Table of Contents\n\n")
        for idx, content in enumerate(parsed_contents, 1):
            filename = content["filename"]
            # Remove extension and format as title
            section_title = Path(filename).stem.replace("-", " ").replace("_", " ").title()
            sections.append(f"{idx}. [{section_title}](#{section_title.lower().replace(' ', '-')})\n")
        sections.append("\n---\n\n")

    # Generate executive summary using LLM if available
    if llm_service:
        try:
            logger.info("Generating executive summary using LLM...")
            # Combine all content for summary (use raw_content which is markdown)
            all_text = "\n\n".join([
                content.get("raw_content", "")
                for content in parsed_contents
                if content.get("raw_content")
            ])

            if all_text:
                summary = llm_service.generate_executive_summary(all_text)
                if summary:
                    sections.append("## Executive Summary\n\n")
                    sections.append(summary)
                    sections.append("\n\n---\n\n")
                    logger.success("Executive summary generated")
        except Exception as e:
            logger.warning(f"Failed to generate executive summary: {e}")

    # Add content from each file
    for idx, content in enumerate(parsed_contents, 1):
        filename = content["filename"]

        # Get content - prefer raw_content as it's markdown
        content_text = content.get("raw_content", "")
        if not content_text:
            # Fallback to structured_content if it's a string
            structured = content.get("structured_content", "")
            if isinstance(structured, str):
                content_text = structured
            else:
                # Skip if no usable content
                logger.warning(f"No usable content for {filename}")
                continue

        # Clean the content before adding to merged document
        logger.debug(f"Cleaning content from {filename}")
        content_text = clean_content_for_output(content_text)

        # Create section header based on filename
        section_title = Path(filename).stem.replace("-", " ").replace("_", " ").title()

        # Add section separator for clarity
        if idx > 1:
            sections.append("\n---\n\n")

        # Add section header
        sections.append(f"## {section_title}\n\n")

        # Add source file reference
        sections.append(f"*Source: {filename}*\n\n")

        # Add the actual content
        # If content already has markdown headers, adjust their level
        adjusted_content = _adjust_header_levels(content_text)
        sections.append(adjusted_content)
        sections.append("\n\n")

    # Combine all sections
    merged_content = "".join(sections)

    # Write to temporary file using settings
    settings = get_settings()
    temp_dir = settings.generator.temp_dir
    temp_dir.mkdir(parents=True, exist_ok=True)

    temp_file = temp_dir / f"{folder_name}_merged.md"
    temp_file.write_text(merged_content, encoding="utf-8")

    logger.success(f"Merged content written to: {temp_file}")

    # Combine metadata from all files
    combined_metadata = {
        "title": title,
        "topic": folder_name,
        "num_source_files": len(parsed_contents),
        "source_files": [content["filename"] for content in parsed_contents],
        "generated_date": datetime.now().isoformat(),
        "author": "Document Generator",
    }

    # Merge individual file metadata
    all_tags = set()
    all_authors = set()
    for content in parsed_contents:
        metadata = content.get("metadata", {})
        if "tags" in metadata:
            if isinstance(metadata["tags"], list):
                all_tags.update(metadata["tags"])
            else:
                all_tags.add(str(metadata["tags"]))
        if "author" in metadata and metadata["author"]:
            all_authors.add(metadata["author"])

    if all_tags:
        combined_metadata["tags"] = sorted(list(all_tags))
    if all_authors:
        combined_metadata["authors"] = sorted(list(all_authors))

    return {
        "temp_file": str(temp_file),
        "metadata": combined_metadata,
        "num_files": len(parsed_contents)
    }


def _adjust_header_levels(content: str) -> str:
    """
    Adjust markdown header levels to fit within the merged document structure.

    Since the merged document uses # for title and ## for sections,
    we shift all headers in individual content down by 2 levels.

    Args:
        content: Markdown content

    Returns:
        Content with adjusted header levels
    """
    lines = content.split("\n")
    adjusted_lines = []

    for line in lines:
        # Check if line is a markdown header
        if line.strip().startswith("#"):
            # Count the number of # symbols
            header_match = line.lstrip()
            hash_count = 0
            for char in header_match:
                if char == "#":
                    hash_count += 1
                else:
                    break

            # Shift header down by 2 levels (but max at h6)
            new_level = min(hash_count + 2, 6)
            header_text = header_match[hash_count:].lstrip()
            adjusted_line = "#" * new_level + " " + header_text
            adjusted_lines.append(adjusted_line)
        else:
            adjusted_lines.append(line)

    return "\n".join(adjusted_lines)
