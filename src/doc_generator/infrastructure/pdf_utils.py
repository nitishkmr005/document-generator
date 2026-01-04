"""
PDF generation utilities migrated from data/build_transformer_pdf.py.

This module contains reusable functions for PDF generation using ReportLab,
including markdown parsing, styling, and flowable creation.
"""

from __future__ import annotations

from pathlib import Path
import hashlib
import html
import re
import subprocess
import tempfile
from typing import Iterator

from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.utils import ImageReader
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.platypus import (
    Paragraph,
    Spacer,
    Preformatted,
    Table,
    TableStyle,
    Image,
)
from cairosvg import svg2png
from loguru import logger

# Color palette (migrated from build_transformer_pdf.py lines 33-43)
PALETTE = {
    "ink": colors.HexColor("#1C1C1C"),
    "muted": colors.HexColor("#4A4A4A"),
    "paper": colors.HexColor("#F6F1E7"),
    "panel": colors.HexColor("#FFFDF8"),
    "accent": colors.HexColor("#D76B38"),
    "teal": colors.HexColor("#1E5D5A"),
    "line": colors.HexColor("#E2D7C9"),
    "code": colors.HexColor("#F2EEE7"),
    "table": colors.HexColor("#F8F4ED"),
}


def strip_frontmatter(text: str) -> str:
    """
    Remove YAML frontmatter from markdown text.

    Args:
        text: Markdown text potentially containing frontmatter

    Returns:
        Text with frontmatter removed
    """
    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) == 3:
            return parts[2].lstrip()
    return text


def inline_md(text: str) -> str:
    """
    Convert inline markdown formatting to HTML for ReportLab.

    Supports:
    - `code` → <font face='Courier'>code</font>
    - **bold** → <b>bold</b>
    - *italic* → <i>italic</i>

    Args:
        text: Text with inline markdown formatting

    Returns:
        Text with HTML formatting for ReportLab
    """
    safe = html.escape(text)
    safe = re.sub(r"`([^`]+)`", r"<font face='Courier'>\1</font>", safe)
    safe = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", safe)
    safe = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<i>\1</i>", safe)
    return safe


def parse_table(table_lines: list[str]) -> list[list[str]]:
    """
    Parse markdown table into 2D list.

    Args:
        table_lines: Lines of markdown table

    Returns:
        2D list of table cells (skips separator rows)
    """
    rows = []
    for line in table_lines:
        parts = [cell.strip() for cell in line.strip().strip("|").split("|")]
        # Skip separator rows (e.g., |---|---|)
        if all(re.match(r"^:?-{2,}:?$", cell) for cell in parts):
            continue
        rows.append(parts)
    return rows


def parse_markdown_lines(text: str) -> Iterator[tuple[str, any]]:
    """
    Parse markdown text into structured elements.

    Yields tuples of (element_type, content):
    - ("h1", "Heading text")
    - ("h2", "Subheading")
    - ("para", "Paragraph text")
    - ("code", "code content")
    - ("mermaid", "mermaid diagram code")
    - ("table", [[row1], [row2]])
    - ("bullets", ["item1", "item2"])
    - ("image", ("alt text", "url"))
    - ("quote", "quoted text")
    - ("spacer", "")

    Args:
        text: Markdown text to parse

    Yields:
        Tuples of (element_type, content)
    """
    lines = text.splitlines()
    in_code = False
    code_lang = ""
    code_lines = []
    table_lines = []
    bullets = []

    def flush_table():
        nonlocal table_lines
        if table_lines:
            yield ("table", parse_table(table_lines))
            table_lines = []

    def flush_bullets():
        nonlocal bullets
        if bullets:
            yield ("bullets", bullets)
            bullets = []

    for line in lines:
        # Code blocks
        if line.strip().startswith("```"):
            if in_code:
                content = "\n".join(code_lines)
                kind = "mermaid" if code_lang == "mermaid" else "code"
                yield (kind, content)
                code_lines = []
                code_lang = ""
                in_code = False
            else:
                in_code = True
                code_lang = line.strip().lstrip("```").strip().lower()
            continue

        if in_code:
            code_lines.append(line)
            continue

        # Tables
        if line.strip().startswith("|") and "|" in line:
            table_lines.append(line)
            continue

        if table_lines:
            yield from flush_table()

        # Bullet lists
        list_match = re.match(r"^[-*]\s+(.*)$", line)
        if list_match:
            bullets.append(list_match.group(1))
            continue

        if bullets:
            yield from flush_bullets()

        # Empty lines
        if not line.strip():
            yield ("spacer", "")
            continue

        # Headings
        heading_match = re.match(r"^(#{1,6})\s+(.*)$", line)
        if heading_match:
            level = len(heading_match.group(1))
            yield (f"h{level}", heading_match.group(2))
            continue

        # Images
        image_match = re.match(r"^!\[(.*?)\]\((.*?)\)", line)
        if image_match:
            alt = image_match.group(1) or "Figure"
            url = image_match.group(2)
            yield ("image", (alt, url))
            continue

        # Quotes
        quote_match = re.match(r"^>\s?(.*)$", line)
        if quote_match:
            yield ("quote", quote_match.group(1))
            continue

        # Regular paragraph
        yield ("para", line)

    # Flush remaining content
    if code_lines:
        kind = "mermaid" if code_lang == "mermaid" else "code"
        yield (kind, "\n".join(code_lines))
    if table_lines:
        yield from flush_table()
    if bullets:
        yield from flush_bullets()


def make_banner(text: str, styles: dict) -> Table:
    """
    Create a colored banner for section headings.

    Args:
        text: Section heading text
        styles: ReportLab styles dictionary

    Returns:
        Table flowable with banner styling
    """
    banner = Table(
        [[Paragraph(inline_md(text), styles["SectionBanner"])]],
        colWidths=[6.9 * inch]
    )
    banner.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), PALETTE["accent"]),
        ("TEXTCOLOR", (0, 0), (-1, -1), colors.white),
        ("LEFTPADDING", (0, 0), (-1, -1), 10),
        ("RIGHTPADDING", (0, 0), (-1, -1), 10),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    return banner


def rasterize_svg(svg_path: Path, image_cache: Path) -> Path:
    """
    Convert SVG to PNG for embedding in PDF.

    Args:
        svg_path: Path to SVG file
        image_cache: Directory for cached images

    Returns:
        Path to generated PNG file
    """
    image_cache.mkdir(parents=True, exist_ok=True)
    output_path = image_cache / (svg_path.stem + ".png")

    if not output_path.exists():
        svg2png(url=str(svg_path), write_to=str(output_path), output_width=1600)
        logger.info(f"Rasterized SVG: {svg_path.name} → {output_path.name}")

    return output_path


def make_image_flowable(
    alt: str,
    image_path: Path,
    styles: dict,
    max_width: float = 6.9 * inch,
    max_height: float = 4.4 * inch
) -> list:
    """
    Create image flowable with caption.

    Args:
        alt: Alt text / caption
        image_path: Path to image file
        styles: ReportLab styles dictionary
        max_width: Maximum image width
        max_height: Maximum image height

    Returns:
        List of flowables (Image + caption + spacer)
    """
    if not image_path.exists():
        logger.warning(f"Image not found: {image_path}")
        return [Paragraph(f"Image placeholder: {inline_md(alt)}", styles["ImageCaption"])]

    img = ImageReader(str(image_path))
    width_px, height_px = img.getSize()
    scale = min(max_width / width_px, max_height / height_px)
    render_w = width_px * scale
    render_h = height_px * scale

    flow = [Image(str(image_path), width=render_w, height=render_h)]
    flow.append(Paragraph(inline_md(alt), styles["ImageCaption"]))
    flow.append(Spacer(1, 6))

    return flow


def make_code_block(code: str, styles: dict) -> Table:
    """
    Create formatted code block.

    Args:
        code: Code content
        styles: ReportLab styles dictionary

    Returns:
        Table flowable with code block styling
    """
    block = Preformatted(code, styles["CodeBlock"])
    table = Table([[block]], colWidths=[6.9 * inch])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), PALETTE["code"]),
        ("BOX", (0, 0), (-1, -1), 0.8, PALETTE["line"]),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    return table


def render_mermaid(
    mermaid_text: str,
    image_cache: Path,
    mmdc_path: Path | None = None
) -> Path | None:
    """
    Render mermaid diagram to PNG.

    Args:
        mermaid_text: Mermaid diagram code
        image_cache: Directory for cached images
        mmdc_path: Path to mermaid CLI (optional)

    Returns:
        Path to generated PNG or None if rendering failed
    """
    if mmdc_path is None:
        mmdc_path = Path("node_modules/.bin/mmdc")

    if not mmdc_path.exists():
        logger.warning("Mermaid CLI not found, skipping diagram rendering")
        return None

    image_cache.mkdir(parents=True, exist_ok=True)
    digest = hashlib.sha256(mermaid_text.encode("utf-8")).hexdigest()[:12]
    out_path = image_cache / f"mermaid-{digest}.png"

    if out_path.exists():
        return out_path

    with tempfile.NamedTemporaryFile(suffix=".mmd", delete=False) as temp_file:
        temp_file.write(mermaid_text.encode("utf-8"))
        temp_path = Path(temp_file.name)

    try:
        subprocess.run(
            [
                str(mmdc_path), "-i", str(temp_path), "-o", str(out_path),
                "-b", "transparent", "-w", "1600"
            ],
            check=True,
            capture_output=True,
            text=True,
        )
        logger.info(f"Rendered mermaid diagram: {out_path.name}")
    except subprocess.CalledProcessError as e:
        logger.error(f"Mermaid rendering failed: {e.stderr}")
        return None
    finally:
        temp_path.unlink(missing_ok=True)

    return out_path if out_path.exists() else None


def make_mermaid_flowable(
    mermaid_text: str,
    styles: dict,
    image_cache: Path,
    mmdc_path: Path | None = None
) -> list:
    """
    Create mermaid diagram flowable.

    Args:
        mermaid_text: Mermaid diagram code
        styles: ReportLab styles dictionary
        image_cache: Directory for cached images
        mmdc_path: Path to mermaid CLI (optional)

    Returns:
        List of flowables (Image + spacer or placeholder)
    """
    rendered = render_mermaid(mermaid_text, image_cache, mmdc_path)

    if not rendered:
        return [
            Paragraph("Mermaid diagram (rendering not available)", styles["ImageCaption"]),
            Spacer(1, 6)
        ]

    img = ImageReader(str(rendered))
    width_px, height_px = img.getSize()
    max_width = 6.9 * inch
    max_height = 4.4 * inch
    scale = min(max_width / width_px, max_height / height_px)
    render_w = width_px * scale
    render_h = height_px * scale

    flow = [Image(str(rendered), width=render_w, height=render_h)]
    flow.append(Spacer(1, 6))

    return flow


def make_quote(text: str, styles: dict) -> Table:
    """
    Create styled quote block.

    Args:
        text: Quote text
        styles: ReportLab styles dictionary

    Returns:
        Table flowable with quote styling
    """
    box = Table(
        [[Paragraph(inline_md(text), styles["Quote"])]],
        colWidths=[6.9 * inch]
    )
    box.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#F4FBF8")),
        ("BOX", (0, 0), (-1, -1), 1, PALETTE["line"]),
        ("LEFTPADDING", (0, 0), (-1, -1), 10),
        ("RIGHTPADDING", (0, 0), (-1, -1), 10),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
    ]))
    return box


def make_table(table_data: list[list[str]], styles: dict) -> Table:
    """
    Create formatted table from markdown table data.

    Args:
        table_data: 2D list of table cells
        styles: ReportLab styles dictionary

    Returns:
        Table flowable with styling
    """
    if not table_data:
        return Table([[]])

    wrapped = [
        [Paragraph(inline_md(cell), styles["TableCell"]) for cell in row]
        for row in table_data
    ]
    table = Table(wrapped, hAlign="LEFT")
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), PALETTE["teal"]),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.5, PALETTE["line"]),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))

    return table


def create_custom_styles() -> dict:
    """
    Create custom ReportLab styles for PDF generation.

    Returns:
        Dictionary of custom ParagraphStyle objects
    """
    styles = getSampleStyleSheet()

    # Title styles
    styles.add(ParagraphStyle(
        name="TitleCover",
        parent=styles["Title"],
        fontName="Times-Roman",
        fontSize=28,
        leading=32,
        textColor=PALETTE["ink"],
        spaceAfter=6,
    ))

    styles.add(ParagraphStyle(
        name="SubtitleCover",
        parent=styles["BodyText"],
        fontName="Helvetica",
        fontSize=12,
        leading=16,
        textColor=PALETTE["muted"],
    ))

    # Section banner
    styles.add(ParagraphStyle(
        name="SectionBanner",
        parent=styles["BodyText"],
        fontName="Helvetica-Bold",
        fontSize=12,
        leading=14,
    ))

    # Heading styles
    styles.add(ParagraphStyle(
        name="Heading2Custom",
        parent=styles["Heading2"],
        fontName="Times-Roman",
        fontSize=16,
        leading=20,
        textColor=PALETTE["ink"],
        spaceAfter=6,
    ))

    styles.add(ParagraphStyle(
        name="Heading3Custom",
        parent=styles["Heading3"],
        fontName="Times-Roman",
        fontSize=13,
        leading=17,
        textColor=PALETTE["ink"],
        spaceAfter=4,
    ))

    # Body text
    styles.add(ParagraphStyle(
        name="BodyCustom",
        parent=styles["BodyText"],
        fontName="Helvetica",
        fontSize=10.5,
        leading=14,
        textColor=PALETTE["muted"],
        spaceAfter=6,
    ))

    # Bullets
    styles.add(ParagraphStyle(
        name="BulletCustom",
        parent=styles["BodyText"],
        fontName="Helvetica",
        fontSize=10.5,
        leading=14,
        leftIndent=12,
        bulletIndent=0,
        spaceAfter=4,
        textColor=PALETTE["muted"],
    ))

    # Code block
    styles.add(ParagraphStyle(
        name="CodeBlock",
        parent=styles["BodyText"],
        fontName="Courier",
        fontSize=8.5,
        leading=11,
        leftIndent=6,
        rightIndent=6,
        spaceAfter=6,
        textColor=PALETTE["ink"],
    ))

    # Image caption
    styles.add(ParagraphStyle(
        name="ImageCaption",
        parent=styles["BodyText"],
        fontName="Helvetica-Oblique",
        fontSize=9.5,
        leading=12,
        textColor=PALETTE["muted"],
        alignment=1,  # Center
    ))

    # Quote
    styles.add(ParagraphStyle(
        name="Quote",
        parent=styles["BodyText"],
        fontName="Helvetica-Oblique",
        fontSize=10.5,
        leading=14,
        textColor=PALETTE["ink"],
    ))

    # Table cell
    styles.add(ParagraphStyle(
        name="TableCell",
        parent=styles["BodyText"],
        fontName="Helvetica",
        fontSize=9.5,
        leading=12,
        textColor=PALETTE["ink"],
    ))

    return styles
