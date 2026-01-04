"""
PPTX generator using python-pptx.

Generates PowerPoint presentations from structured markdown content.
Supports LLM-enhanced slide generation for executive presentations.
"""

from pathlib import Path
from loguru import logger

from ...infrastructure.pptx_utils import (
    create_presentation,
    add_title_slide,
    add_content_slide,
    add_section_header_slide,
    add_image_slide,
    add_executive_summary_slide,
    add_chart_slide,
    save_presentation,
)
from ...infrastructure.pdf_utils import parse_markdown_lines
from ...infrastructure.svg_generator import generate_chart
from ...domain.exceptions import GenerationError


class PPTXGenerator:
    """
    PPTX generator using python-pptx.

    Converts structured markdown content to PowerPoint presentation.
    """

    def __init__(self):
        """Initialize PPTX generator."""
        pass

    def generate(self, content: dict, metadata: dict, output_dir: Path) -> Path:
        """
        Generate PPTX from structured content.

        Uses LLM-enhanced content when available for executive-quality presentations.

        Args:
            content: Structured content dictionary with 'title', 'markdown',
                     and optional 'slides', 'executive_summary', 'charts' keys
            metadata: Document metadata
            output_dir: Output directory

        Returns:
            Path to generated PPTX

        Raises:
            GenerationError: If PPTX generation fails
        """
        try:
            # Ensure output directory exists
            output_dir.mkdir(parents=True, exist_ok=True)

            # Create output path
            title = metadata.get("title", "presentation")
            safe_title = title.replace(" ", "_").replace("/", "_")
            output_path = output_dir / f"{safe_title}.pptx"

            logger.info(f"Generating PPTX: {output_path.name}")

            # Get markdown content
            markdown_content = content.get("markdown", content.get("raw_content", ""))

            if not markdown_content:
                raise GenerationError("No content provided for PPTX generation")

            # Check for LLM enhancements
            has_llm_enhancements = any(
                key in content for key in ["slides", "executive_summary", "charts"]
            )

            if has_llm_enhancements:
                logger.info("Using LLM-enhanced slide generation")

            # Create presentation with full structured content
            self._create_presentation(
                output_path,
                title,
                markdown_content,
                metadata,
                structured_content=content if has_llm_enhancements else None
            )

            logger.info(f"PPTX generated successfully: {output_path}")

            return output_path

        except Exception as e:
            logger.error(f"PPTX generation failed: {e}")
            raise GenerationError(f"Failed to generate PPTX: {e}")

    def _create_presentation(
        self,
        output_path: Path,
        title: str,
        markdown_content: str,
        metadata: dict,
        structured_content: dict = None
    ) -> None:
        """
        Create PowerPoint presentation.

        Uses LLM-generated slide structure when available for executive-quality output.

        Args:
            output_path: Path to output PPTX
            title: Presentation title
            markdown_content: Markdown content to convert
            metadata: Document metadata
            structured_content: Optional structured content with LLM enhancements
        """
        # Create presentation
        prs = create_presentation()

        # Add title slide
        subtitle = metadata.get("subtitle", metadata.get("author", ""))
        add_title_slide(prs, title, subtitle)

        # Check for LLM-enhanced content
        if structured_content:
            # Add executive summary if available
            executive_summary = structured_content.get("executive_summary", "")
            if executive_summary:
                summary_points = [
                    line.strip() for line in executive_summary.split("\n")
                    if line.strip() and (line.strip().startswith("-") or line.strip().startswith("•"))
                ]
                if summary_points:
                    add_executive_summary_slide(prs, "Executive Summary", summary_points)
                    logger.debug("Added executive summary slide")

            # Use LLM-generated slide structure if available
            slides = structured_content.get("slides", [])
            if slides:
                self._add_llm_slides(prs, slides)
            else:
                # Fallback to markdown-based generation
                self._add_slides_from_markdown(prs, markdown_content)

            # Add chart slides if suggested
            charts = structured_content.get("charts", [])
            self._add_chart_slides(prs, charts, output_path.parent)
        else:
            # No LLM enhancement - use markdown-based generation
            self._add_slides_from_markdown(prs, markdown_content)

        # Save presentation
        save_presentation(prs, output_path)

        logger.debug(f"Created presentation with {len(prs.slides)} slides")

    def _add_llm_slides(self, prs, slides: list[dict]) -> None:
        """
        Add slides from LLM-generated structure.

        Args:
            prs: Presentation object
            slides: List of slide dictionaries with title, bullets, speaker_notes
        """
        for slide_data in slides:
            title = slide_data.get("title", "")
            bullets = slide_data.get("bullets", [])
            speaker_notes = slide_data.get("speaker_notes", "")

            if title and bullets:
                add_content_slide(
                    prs,
                    title,
                    bullets,
                    is_bullets=True,
                    speaker_notes=speaker_notes
                )

        logger.debug(f"Added {len(slides)} LLM-generated slides")

    def _add_chart_slides(self, prs, charts: list[dict], output_dir: Path) -> None:
        """
        Generate and add chart slides.

        Args:
            prs: Presentation object
            charts: List of chart suggestions from LLM
            output_dir: Directory for temporary chart files
        """
        for i, chart in enumerate(charts[:3]):  # Max 3 charts
            chart_type = chart.get("chart_type", "bar")
            title = chart.get("title", f"Chart {i+1}")
            data = chart.get("data", [])

            if not data:
                continue

            # Generate SVG
            svg_path = output_dir / f"chart_{i}.svg"
            try:
                generate_chart(chart_type, data, title, svg_path)
                add_chart_slide(prs, title, svg_path)
                logger.debug(f"Added chart slide: {title}")
            except Exception as e:
                logger.warning(f"Failed to generate chart: {e}")

    def _add_slides_from_markdown(self, prs, markdown_content: str) -> None:
        """
        Parse markdown and add slides to presentation.

        Creates slides based on markdown structure:
        - H1: Section header slides
        - H2: Content slide titles
        - Bullets: Bullet points on content slides
        - Images: Image slides

        Args:
            prs: Presentation object
            markdown_content: Markdown content to parse
        """
        current_slide_title = None
        current_slide_content = []
        is_bullets = True

        for kind, content_item in parse_markdown_lines(markdown_content):
            # H1 becomes section header
            if kind == "h1":
                # Flush current slide if any
                if current_slide_title and current_slide_content:
                    add_content_slide(prs, current_slide_title, current_slide_content, is_bullets)
                    current_slide_content = []

                # Add section header
                add_section_header_slide(prs, content_item)
                current_slide_title = None

            # H2 becomes slide title
            elif kind == "h2":
                # Flush current slide if any
                if current_slide_title and current_slide_content:
                    add_content_slide(prs, current_slide_title, current_slide_content, is_bullets)

                # Start new slide
                current_slide_title = content_item
                current_slide_content = []
                is_bullets = True

            # H3 becomes content item (if no H2 title yet, becomes title)
            elif kind == "h3":
                if current_slide_title:
                    current_slide_content.append(f"• {content_item}")
                else:
                    current_slide_title = content_item
                    current_slide_content = []

            # Bullets
            elif kind == "bullets":
                is_bullets = True
                current_slide_content.extend(content_item)

            # Paragraphs
            elif kind == "para":
                if content_item.strip():
                    is_bullets = False
                    current_slide_content.append(content_item)

            # Images
            elif kind == "image":
                # Flush current slide if any
                if current_slide_title and current_slide_content:
                    add_content_slide(prs, current_slide_title, current_slide_content, is_bullets)
                    current_slide_content = []
                    current_slide_title = None

                alt, url = content_item
                image_path = self._resolve_image_path(url)
                if image_path:
                    add_image_slide(prs, alt, image_path, alt)
                else:
                    # Add as text slide if image not found
                    if not current_slide_title:
                        current_slide_title = "Image"
                    current_slide_content.append(f"Image: {alt}")

            # Code blocks, quotes - add as text content
            elif kind in ["code", "quote"]:
                is_bullets = False
                # Truncate long code blocks for slides
                if len(content_item) > 200:
                    content_item = content_item[:200] + "..."
                current_slide_content.append(content_item)

            # Tables - add summary
            elif kind == "table":
                if content_item:
                    current_slide_content.append(f"Table with {len(content_item)} rows")

            # Mermaid diagrams - add placeholder
            elif kind == "mermaid":
                current_slide_content.append("Diagram (see source)")

            # Limit content per slide (max 7 items)
            if len(current_slide_content) >= 7:
                if current_slide_title:
                    add_content_slide(prs, current_slide_title, current_slide_content, is_bullets)
                    current_slide_title = None
                    current_slide_content = []

        # Flush final slide
        if current_slide_title and current_slide_content:
            add_content_slide(prs, current_slide_title, current_slide_content, is_bullets)

    def _resolve_image_path(self, url: str) -> Path | None:
        """
        Resolve image URL to local path.

        Args:
            url: Image URL or path

        Returns:
            Path to local image or None
        """
        # If it's a URL, we can't resolve it locally
        if url.startswith("http://") or url.startswith("https://"):
            logger.warning(f"Remote image URLs not supported in PPTX: {url}")
            return None

        # Try to resolve as local path
        cleaned = url.lstrip("/")

        # Check several possible locations
        candidates = [
            Path(url),  # Absolute path
            Path(cleaned),  # Relative path
            Path("static") / cleaned,  # Hugo static dir
            Path("src/output") / cleaned,  # Output dir
        ]

        for candidate in candidates:
            if candidate.exists() and candidate.is_file():
                return candidate

        logger.warning(f"Image not found: {url}")
        return None
