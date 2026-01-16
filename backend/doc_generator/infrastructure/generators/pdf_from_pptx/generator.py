"""
PDF from PPTX generator.

Generates PowerPoint presentations and converts them to PDF format.
Supports:
1. LibreOffice headless conversion (primary, high quality)
2. Fallback rendering using slide images
"""

import shutil
import subprocess
import tempfile
from pathlib import Path

from loguru import logger

from ..pptx.generator import PPTXGenerator


class PDFFromPPTXGenerator:
    """PDF from PPTX generator.

    Creates PowerPoint presentations using PPTXGenerator, then converts to PDF.
    """

    def __init__(self, image_cache: Path | None = None):
        """
        Initialize PDF from PPTX generator.

        Args:
            image_cache: Directory for cached images (optional)
        """
        self.pptx_generator = PPTXGenerator()
        self._libreoffice_available = self._check_libreoffice()

    def _check_libreoffice(self) -> bool:
        """Check if LibreOffice is available for conversion."""
        # Check for libreoffice or soffice command
        for cmd in [
            "libreoffice",
            "soffice",
            "/Applications/LibreOffice.app/Contents/MacOS/soffice",
        ]:
            if shutil.which(cmd):
                logger.debug(f"Found LibreOffice: {cmd}")
                return True

        # On macOS, check for the app bundle
        mac_paths = [
            "/Applications/LibreOffice.app/Contents/MacOS/soffice",
            "/opt/homebrew/bin/soffice",
        ]
        for path in mac_paths:
            if Path(path).exists():
                logger.debug(f"Found LibreOffice: {path}")
                return True

        logger.warning(
            "LibreOffice not found. Install LibreOffice for high-quality PPTX to PDF conversion. "
            "Falling back to basic PDF generation."
        )
        return False

    def generate(self, content: dict, metadata: dict, output_dir: Path) -> str:
        """
        Generate PDF from PPTX.

        First generates PPTX using PPTXGenerator, then converts to PDF.

        Args:
            content: Structured content dictionary with 'title' and 'markdown'
            metadata: Document metadata
            output_dir: Output directory

        Returns:
            Path to generated PDF file
        """
        logger.info("=== Starting PDF from PPTX Generation ===")

        # Step 1: Generate PPTX
        logger.info("Step 1: Generating PPTX...")
        pptx_path = self.pptx_generator.generate(content, metadata, output_dir)
        pptx_file = Path(pptx_path)

        if not pptx_file.exists():
            raise FileNotFoundError(f"PPTX generation failed: {pptx_path}")

        logger.info(f"PPTX generated: {pptx_file.name}")

        # Step 2: Convert PPTX to PDF
        logger.info("Step 2: Converting PPTX to PDF...")

        # PDF output path (same name, different extension)
        pdf_path = pptx_file.with_suffix(".pdf")

        if self._libreoffice_available:
            success = self._convert_with_libreoffice(pptx_file, output_dir)
            if success and pdf_path.exists():
                logger.success(f"PDF created via LibreOffice: {pdf_path.name}")
                # Keep the PPTX as well (user might want both)
                return str(pdf_path)
            else:
                logger.warning("LibreOffice conversion failed, using fallback")

        # Fallback: Generate a PDF with slide-based layout directly
        pdf_path = self._generate_fallback_pdf(content, metadata, output_dir, pptx_file)
        logger.success(f"PDF created via fallback method: {pdf_path}")

        return str(pdf_path)

    def _convert_with_libreoffice(self, pptx_path: Path, output_dir: Path) -> bool:
        """
        Convert PPTX to PDF using LibreOffice headless mode.

        Args:
            pptx_path: Path to PPTX file
            output_dir: Directory for output PDF

        Returns:
            True if conversion succeeded, False otherwise
        """
        # Find LibreOffice executable
        lo_cmd = None
        for cmd in [
            "libreoffice",
            "soffice",
            "/Applications/LibreOffice.app/Contents/MacOS/soffice",
        ]:
            if shutil.which(cmd):
                lo_cmd = cmd
                break
            if Path(cmd).exists():
                lo_cmd = cmd
                break

        if not lo_cmd:
            return False

        try:
            # Use a temporary directory for the conversion to avoid conflicts
            with tempfile.TemporaryDirectory() as temp_dir:
                # Run LibreOffice in headless mode
                cmd = [
                    lo_cmd,
                    "--headless",
                    "--convert-to",
                    "pdf",
                    "--outdir",
                    temp_dir,
                    str(pptx_path),
                ]

                logger.debug(f"Running: {' '.join(cmd)}")

                result = subprocess.run(
                    cmd,
                    capture_output=True,
                    text=True,
                    timeout=120,  # 2 minute timeout
                )

                if result.returncode != 0:
                    logger.error(f"LibreOffice conversion failed: {result.stderr}")
                    return False

                # Move the generated PDF to output directory
                temp_pdf = Path(temp_dir) / pptx_path.with_suffix(".pdf").name
                if temp_pdf.exists():
                    target_pdf = output_dir / temp_pdf.name
                    shutil.move(str(temp_pdf), str(target_pdf))
                    logger.info(f"PDF moved to: {target_pdf}")
                    return True
                else:
                    logger.error(f"PDF not found in temp dir: {temp_dir}")
                    return False

        except subprocess.TimeoutExpired:
            logger.error("LibreOffice conversion timed out")
            return False
        except Exception as e:
            logger.error(f"LibreOffice conversion error: {e}")
            return False

    def _generate_fallback_pdf(
        self, content: dict, metadata: dict, output_dir: Path, pptx_path: Path
    ) -> str:
        """
        Generate a PDF from structured content using slide-based layout.

        This is a fallback when LibreOffice is not available.
        Creates a presentation-style PDF directly from the content with
        proper markdown rendering and slide-like visual styling.

        Args:
            content: Structured content dictionary
            metadata: Document metadata
            output_dir: Output directory
            pptx_path: Path to the generated PPTX (for reference)

        Returns:
            Path to generated PDF
        """
        import re
        import html
        from datetime import datetime
        from reportlab.lib.pagesizes import landscape, A4
        from reportlab.lib.units import inch
        from reportlab.lib import colors
        from reportlab.platypus import (
            SimpleDocTemplate,
            Paragraph,
            Spacer,
            PageBreak,
            Table,
            TableStyle,
            KeepTogether,
        )
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.enums import TA_CENTER, TA_LEFT

        # Helper function to convert markdown to ReportLab HTML
        def inline_md(text: str) -> str:
            """Convert inline markdown formatting to HTML for ReportLab."""
            if not text:
                return ""

            # Handle markdown links [text](url) -> clickable links
            link_pattern = r"\[([^\]]+)\]\(([^\)]+)\)"
            links = []

            def replace_link(match):
                text_part = match.group(1)
                url = match.group(2)
                links.append((text_part, url))
                return f"__LINK_{len(links)-1}__"

            text = re.sub(link_pattern, replace_link, text)

            # Handle code blocks
            parts = re.split(r"(`[^`]+`)", text)
            rendered = []
            for part in parts:
                if part.startswith("`") and part.endswith("`") and len(part) >= 2:
                    code = html.escape(part[1:-1])
                    rendered.append(
                        f"<font face='Courier' color='#6366f1'>{code}</font>"
                    )
                    continue
                safe = html.escape(part)
                # Bold **text**
                safe = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", safe)
                # Italic *text*
                safe = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<i>\1</i>", safe)
                rendered.append(safe)

            result = "".join(rendered)

            # Restore links
            for i, (link_text, url) in enumerate(links):
                placeholder = f"__LINK_{i}__"
                link_html = f'<link href="{html.escape(url)}" color="blue"><u>{html.escape(link_text)}</u></link>'
                result = result.replace(placeholder, link_html)

            return result

        # Create PDF path
        pdf_filename = pptx_path.stem + ".pdf"
        pdf_path = output_dir / pdf_filename

        # Slide dimensions (landscape A4)
        page_width, page_height = landscape(A4)

        # Create document with landscape orientation (like slides)
        doc = SimpleDocTemplate(
            str(pdf_path),
            pagesize=landscape(A4),
            rightMargin=0.75 * inch,
            leftMargin=0.75 * inch,
            topMargin=0.5 * inch,
            bottomMargin=0.5 * inch,
        )

        # Color palette
        ACCENT_COLOR = colors.HexColor("#6366f1")  # Indigo
        DARK_TEXT = colors.HexColor("#1e293b")  # Slate-800
        LIGHT_BG = colors.HexColor("#f8fafc")  # Slate-50
        MUTED_TEXT = colors.HexColor("#64748b")  # Slate-500

        # Create styles
        styles = getSampleStyleSheet()

        # Main title style (for cover slide)
        main_title_style = ParagraphStyle(
            "MainTitle",
            parent=styles["Title"],
            fontSize=48,
            leading=56,
            alignment=TA_CENTER,
            spaceAfter=20,
            textColor=DARK_TEXT,
            fontName="Helvetica-Bold",
        )

        # Subtitle style
        subtitle_style = ParagraphStyle(
            "Subtitle",
            parent=styles["Normal"],
            fontSize=20,
            leading=26,
            alignment=TA_CENTER,
            textColor=MUTED_TEXT,
            fontName="Helvetica",
        )

        # Slide title style
        slide_title_style = ParagraphStyle(
            "SlideTitle",
            parent=styles["Heading1"],
            fontSize=32,
            leading=40,
            alignment=TA_CENTER,
            spaceAfter=16,
            textColor=DARK_TEXT,
            fontName="Helvetica-Bold",
        )

        # Body text style
        body_style = ParagraphStyle(
            "SlideBody",
            parent=styles["Normal"],
            fontSize=18,
            leading=28,
            leftIndent=40,
            spaceBefore=6,
            spaceAfter=6,
            textColor=DARK_TEXT,
            fontName="Helvetica",
        )

        # Bullet style
        bullet_style = ParagraphStyle(
            "SlideBullet",
            parent=styles["Normal"],
            fontSize=18,
            leading=28,
            leftIndent=60,
            bulletIndent=40,
            spaceBefore=6,
            spaceAfter=6,
            textColor=DARK_TEXT,
            fontName="Helvetica",
        )

        # Build story (content)
        story = []

        # Get content details
        title = content.get("title", metadata.get("title", "Presentation"))
        markdown_content = content.get("markdown", "")
        slides_data = content.get("slides", [])

        # === Cover Slide ===
        # Top accent bar
        accent_bar = Table([[""]], colWidths=[page_width - 1.5 * inch], rowHeights=[8])
        accent_bar.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, -1), ACCENT_COLOR),
                    ("TOPPADDING", (0, 0), (-1, -1), 0),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
                ]
            )
        )
        story.append(accent_bar)
        story.append(Spacer(1, 2 * inch))
        story.append(Paragraph(inline_md(title), main_title_style))
        story.append(Spacer(1, 0.5 * inch))

        # Decorative line under title
        divider = Table([[""]], colWidths=[3 * inch], rowHeights=[4])
        divider.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, -1), ACCENT_COLOR),
                    ("TOPPADDING", (0, 0), (-1, -1), 0),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
                    ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ]
            )
        )
        # Wrap in a table to center it
        centered_divider = Table([[divider]], colWidths=[page_width - 1.5 * inch])
        centered_divider.setStyle(
            TableStyle(
                [
                    ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ]
            )
        )
        story.append(centered_divider)
        story.append(Spacer(1, 0.5 * inch))

        # Metadata
        author = metadata.get("author", "")
        if author:
            story.append(Paragraph(f"By {inline_md(author)}", subtitle_style))
            story.append(Spacer(1, 0.2 * inch))

        date_str = datetime.now().strftime("%B %d, %Y")
        story.append(Paragraph(date_str, subtitle_style))
        story.append(PageBreak())

        # === Content Slides ===
        def create_slide_frame(slide_title: str, content_elements: list) -> list:
            """Create a slide with visual framing."""
            elements = []

            # Top accent bar
            elements.append(accent_bar)
            elements.append(Spacer(1, 0.3 * inch))

            # Slide title with background bar
            title_table = Table(
                [[Paragraph(inline_md(slide_title), slide_title_style)]],
                colWidths=[page_width - 1.5 * inch],
            )
            title_table.setStyle(
                TableStyle(
                    [
                        ("BACKGROUND", (0, 0), (-1, -1), LIGHT_BG),
                        ("TOPPADDING", (0, 0), (-1, -1), 12),
                        ("BOTTOMPADDING", (0, 0), (-1, -1), 12),
                        ("LEFTPADDING", (0, 0), (-1, -1), 12),
                        ("RIGHTPADDING", (0, 0), (-1, -1), 12),
                        ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#e2e8f0")),
                    ]
                )
            )
            elements.append(title_table)
            elements.append(Spacer(1, 0.3 * inch))

            # Content
            for elem in content_elements:
                elements.append(elem)

            elements.append(PageBreak())
            return elements

        if slides_data:
            # Use LLM-generated slides structure
            for slide in slides_data:
                slide_title = slide.get("title", "")
                bullets = slide.get("bullets", [])

                content_elements = []
                for bullet in bullets:
                    content_elements.append(
                        Paragraph(f"• {inline_md(bullet)}", bullet_style)
                    )

                story.extend(create_slide_frame(slide_title, content_elements))
        else:
            # Parse markdown content for slides
            self._add_slides_from_markdown_v2(
                story,
                markdown_content,
                slide_title_style,
                body_style,
                bullet_style,
                inline_md,
                accent_bar,
                LIGHT_BG,
                page_width,
            )

        # Build PDF
        try:
            doc.build(story)
            logger.info(f"Fallback PDF generated with slide styling: {pdf_path}")
            return str(pdf_path)
        except Exception as e:
            logger.error(f"Failed to generate fallback PDF: {e}")
            raise

    def _add_slides_from_markdown_v2(
        self,
        story: list,
        markdown_content: str,
        title_style,
        body_style,
        bullet_style,
        inline_md,
        accent_bar,
        light_bg,
        page_width,
    ) -> None:
        """
        Parse markdown and add slides to the PDF story with proper formatting.

        Args:
            story: ReportLab story list to append to
            markdown_content: Markdown content to parse
            title_style: Style for slide titles
            body_style: Style for body paragraphs
            bullet_style: Style for bullet points
            inline_md: Function to convert markdown to HTML
            accent_bar: Accent bar table element
            light_bg: Background color for titles
            page_width: Page width for table sizing
        """
        import re
        from reportlab.platypus import Spacer, Paragraph, PageBreak, Table, TableStyle
        from reportlab.lib.units import inch
        from reportlab.lib import colors

        # Track seen section titles to prevent duplicates
        seen_titles = set()

        def normalize_title(t: str) -> str:
            """Normalize title for duplicate detection."""
            cleaned = re.sub(r"^\d+[\.:\)\s]+\s*", "", t.strip())
            return re.sub(r"\s+", " ", cleaned).strip().lower()

        # Split content by H2 headings (slide boundaries)
        sections = re.split(r"^##\s+", markdown_content, flags=re.MULTILINE)

        for section in sections[1:]:  # Skip empty first element
            lines = section.strip().split("\n")
            if not lines:
                continue

            # First line is the slide title
            slide_title = lines[0].strip()

            # Skip duplicate sections
            normalized = normalize_title(slide_title)
            if normalized in seen_titles:
                continue
            seen_titles.add(normalized)

            # Create slide frame
            story.append(accent_bar)
            story.append(Spacer(1, 0.3 * inch))

            # Slide title with background
            title_table = Table(
                [[Paragraph(inline_md(slide_title), title_style)]],
                colWidths=[page_width - 1.5 * inch],
            )
            title_table.setStyle(
                TableStyle(
                    [
                        ("BACKGROUND", (0, 0), (-1, -1), light_bg),
                        ("TOPPADDING", (0, 0), (-1, -1), 12),
                        ("BOTTOMPADDING", (0, 0), (-1, -1), 12),
                        ("LEFTPADDING", (0, 0), (-1, -1), 12),
                        ("RIGHTPADDING", (0, 0), (-1, -1), 12),
                        ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#e2e8f0")),
                    ]
                )
            )
            story.append(title_table)
            story.append(Spacer(1, 0.3 * inch))

            # Process remaining lines
            current_paragraph = []

            for line in lines[1:]:
                line = line.strip()
                if not line:
                    # Flush current paragraph
                    if current_paragraph:
                        text = " ".join(current_paragraph)
                        story.append(Paragraph(inline_md(text), body_style))
                        current_paragraph = []
                    continue

                # Skip H3 and lower headings (they become sub-bullets or bold text)
                if line.startswith("### "):
                    # Sub-heading becomes bold paragraph
                    if current_paragraph:
                        text = " ".join(current_paragraph)
                        story.append(Paragraph(inline_md(text), body_style))
                        current_paragraph = []
                    sub_title = line[4:].strip()
                    story.append(Spacer(1, 0.1 * inch))
                    story.append(
                        Paragraph(f"<b>{inline_md(sub_title)}</b>", body_style)
                    )
                    continue

                # Handle bullet points
                if (
                    line.startswith("- ")
                    or line.startswith("* ")
                    or line.startswith("• ")
                ):
                    # Flush current paragraph
                    if current_paragraph:
                        text = " ".join(current_paragraph)
                        story.append(Paragraph(inline_md(text), body_style))
                        current_paragraph = []

                    bullet_text = line[2:] if not line.startswith("• ") else line[2:]
                    story.append(Paragraph(f"• {inline_md(bullet_text)}", bullet_style))
                elif line.startswith("#"):
                    # Skip other headings within a slide
                    continue
                else:
                    # Regular paragraph text - accumulate
                    current_paragraph.append(line)

            # Flush any remaining paragraph
            if current_paragraph:
                text = " ".join(current_paragraph)
                story.append(Paragraph(inline_md(text), body_style))

            story.append(PageBreak())

    def _add_slides_from_markdown(
        self, story: list, markdown_content: str, title_style, bullet_style
    ) -> None:
        """
        Legacy method - redirects to v2 implementation.
        Kept for backwards compatibility.
        """
        # This method is now superseded by _add_slides_from_markdown_v2
        # but kept in case old code calls it
        import re
        import html
        from reportlab.platypus import Spacer, Paragraph, PageBreak
        from reportlab.lib.units import inch

        def inline_md(text: str) -> str:
            if not text:
                return ""
            parts = re.split(r"(`[^`]+`)", text)
            rendered = []
            for part in parts:
                if part.startswith("`") and part.endswith("`") and len(part) >= 2:
                    code = html.escape(part[1:-1])
                    rendered.append(f"<font face='Courier'>{code}</font>")
                    continue
                safe = html.escape(part)
                safe = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", safe)
                safe = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<i>\1</i>", safe)
                rendered.append(safe)
            return "".join(rendered)

        # Split content by H2 headings
        sections = re.split(r"^##\s+", markdown_content, flags=re.MULTILINE)

        for section in sections[1:]:
            lines = section.strip().split("\n")
            if not lines:
                continue

            slide_title = lines[0].strip()
            story.append(Spacer(1, 0.3 * inch))
            story.append(Paragraph(inline_md(slide_title), title_style))
            story.append(Spacer(1, 0.3 * inch))

            for line in lines[1:]:
                line = line.strip()
                if not line:
                    continue

                if line.startswith("- ") or line.startswith("* "):
                    bullet_text = line[2:]
                    story.append(Paragraph(f"• {inline_md(bullet_text)}", bullet_style))
                elif line.startswith("• "):
                    bullet_text = line[2:]
                    story.append(Paragraph(f"• {inline_md(bullet_text)}", bullet_style))
                elif not line.startswith("#"):
                    story.append(Paragraph(f"• {inline_md(line)}", bullet_style))

            story.append(PageBreak())
