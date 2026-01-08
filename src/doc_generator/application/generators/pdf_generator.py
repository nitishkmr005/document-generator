"""
PDF generator using ReportLab.

Generates PDF documents from structured markdown content.
"""

from pathlib import Path

from loguru import logger
from reportlab.lib.pagesizes import letter
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer

from ...domain.exceptions import GenerationError
from ...infrastructure.pdf_utils import (
    create_custom_styles,
    inline_md,
    make_banner,
    make_code_block,
    make_image_flowable,
    make_mermaid_flowable,
    make_quote,
    make_table,
    parse_markdown_lines,
    rasterize_svg,
)
from ...infrastructure.settings import get_settings
from ...utils.image_utils import resolve_image_path


class PDFGenerator:
    """
    PDF generator using ReportLab.

    Converts structured markdown content to PDF with custom styling.
    """

    def __init__(self, image_cache: Path | None = None):
        """
        Initialize PDF generator.

        Args:
            image_cache: Directory for cached images (optional)
        """
        settings = get_settings()
        self.image_cache = image_cache or Path(settings.pdf.image_cache_dir)
        self.styles = create_custom_styles()

    def generate(self, content: dict, metadata: dict, output_dir: Path) -> Path:
        """
        Generate PDF from structured content.

        Args:
            content: Structured content dictionary with 'title', 'markdown',
                     and optional 'visualizations' keys
            metadata: Document metadata
            output_dir: Output directory

        Returns:
            Path to generated PDF

        Raises:
            GenerationError: If PDF generation fails
        """
        try:
            # Ensure output directory exists
            output_dir.mkdir(parents=True, exist_ok=True)
            self.image_cache.mkdir(parents=True, exist_ok=True)

            # Create output path
            # Get title for document content
            title = metadata.get("title", "document")

            # Check for custom filename for output file
            if "custom_filename" in metadata:
                filename = metadata["custom_filename"]
            else:
                filename = title.replace(" ", "_").replace("/", "_")

            output_path = output_dir / f"{filename}.pdf"

            logger.info(f"Generating PDF: {output_path.name}")

            # Get markdown content
            markdown_content = content.get("markdown", content.get("raw_content", ""))

            if not markdown_content:
                raise GenerationError("No content provided for PDF generation")

            # Get visualizations if available
            visualizations = content.get("visualizations", [])

            # Create PDF
            self._create_pdf(output_path, title, markdown_content, metadata, visualizations)

            logger.info(f"PDF generated successfully: {output_path}")

            return output_path

        except Exception as e:
            logger.error(f"PDF generation failed: {e}")
            raise GenerationError(f"Failed to generate PDF: {e}")

    def _create_pdf(
        self,
        output_path: Path,
        title: str,
        markdown_content: str,
        metadata: dict,
        visualizations: list[dict] = None
    ) -> None:
        """
        Create PDF document.

        Args:
            output_path: Path to output PDF
            title: Document title
            markdown_content: Markdown content to convert
            metadata: Document metadata
            visualizations: Optional list of visualization dictionaries
        """
        visualizations = visualizations or []

        # Create document
        doc = SimpleDocTemplate(
            str(output_path),
            pagesize=letter,
            rightMargin=54,
            leftMargin=54,
            topMargin=54,
            bottomMargin=54,
            title=title,
            author=metadata.get("author", ""),
        )

        story = []

        # Add title page
        story.append(Paragraph(inline_md(title), self.styles["TitleCover"]))

        subtitle = metadata.get("subtitle", metadata.get("url", ""))
        if subtitle:
            story.append(Paragraph(inline_md(subtitle), self.styles["SubtitleCover"]))

        story.append(Spacer(1, 12))

        # Parse and add markdown content
        for kind, content_item in parse_markdown_lines(markdown_content):
            if kind == "spacer":
                story.append(Spacer(1, 6))

            elif kind == "h1":
                story.append(Paragraph(inline_md(content_item), self.styles["Heading2Custom"]))

            elif kind == "h2":
                story.append(Spacer(1, 8))
                story.append(make_banner(content_item, self.styles))
                story.append(Spacer(1, 6))

            elif kind == "h3":
                story.append(Paragraph(inline_md(content_item), self.styles["Heading3Custom"]))

            elif kind.startswith("h"):
                story.append(Paragraph(inline_md(content_item), self.styles["Heading3Custom"]))

            elif kind == "image":
                alt, url = content_item
                # Resolve image path (if local file)
                image_path = self._resolve_image_path(url)
                if image_path:
                    story.extend(make_image_flowable(alt, image_path, self.styles))
                else:
                    story.append(Paragraph(f"Image: {inline_md(alt)}", self.styles["ImageCaption"]))

            elif kind == "quote":
                story.append(make_quote(content_item, self.styles))
                story.append(Spacer(1, 6))

            elif kind == "bullets":
                for item in content_item:
                    story.append(
                        Paragraph(inline_md(item), self.styles["BulletCustom"], bulletText="-")
                    )

            elif kind == "mermaid":
                story.extend(make_mermaid_flowable(content_item, self.styles, self.image_cache))

            elif kind == "code":
                story.append(make_code_block(content_item, self.styles))

            elif kind == "table":
                story.append(make_table(content_item, self.styles))
                story.append(Spacer(1, 6))

            else:  # para
                if content_item.strip():
                    story.append(Paragraph(inline_md(content_item), self.styles["BodyCustom"]))

        # Add visualizations section if available
        if visualizations:
            story.append(Spacer(1, 20))
            story.append(make_banner("Visualizations", self.styles))
            story.append(Spacer(1, 12))

            for visual in visualizations:
                vis_title = visual.get("title", "Visualization")
                svg_path = visual.get("path", "")

                if svg_path:
                    svg_path = Path(svg_path)
                    if svg_path.exists():
                        # Rasterize SVG to PNG for PDF embedding
                        png_path = rasterize_svg(svg_path, self.image_cache)
                        if png_path:
                            story.extend(make_image_flowable(vis_title, png_path, self.styles))
                            story.append(Spacer(1, 8))
                            vis_type = visual.get("type", "diagram")
                            logger.debug(f"Added {vis_type} visualization to PDF: {vis_title}")

        # Build PDF
        element_count = len(story)
        doc.build(story)

        logger.debug(f"PDF document built with {element_count} elements")

    def _resolve_image_path(self, url: str) -> Path | None:
        """
        Resolve image URL to local path.

        Args:
            url: Image URL or path

        Returns:
            Path to local image or None
        """
        return resolve_image_path(
            url,
            image_cache=self.image_cache,
            rasterize_func=rasterize_svg
        )
