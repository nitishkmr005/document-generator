"""
PowerPoint generation utilities using python-pptx.

Provides helper functions for creating PPTX presentations programmatically.
"""

from pathlib import Path
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
from loguru import logger


# Color theme (matching PDF palette)
THEME_COLORS = {
    "ink": RGBColor(28, 28, 28),
    "muted": RGBColor(74, 74, 74),
    "accent": RGBColor(215, 107, 56),
    "teal": RGBColor(30, 93, 90),
    "background": RGBColor(255, 255, 255),
}


def create_presentation() -> Presentation:
    """
    Create a new PowerPoint presentation with 16:9 layout.

    Returns:
        Presentation object
    """
    prs = Presentation()
    prs.slide_width = Inches(10)
    prs.slide_height = Inches(5.625)  # 16:9 aspect ratio

    logger.debug("Created new PowerPoint presentation (16:9)")
    return prs


def add_title_slide(prs: Presentation, title: str, subtitle: str = "") -> None:
    """
    Add title slide to presentation.

    Args:
        prs: Presentation object
        title: Title text
        subtitle: Subtitle text (optional)
    """
    slide_layout = prs.slide_layouts[0]  # Title slide layout
    slide = prs.slides.add_slide(slide_layout)

    title_shape = slide.shapes.title
    subtitle_shape = slide.placeholders[1]

    title_shape.text = title
    title_shape.text_frame.paragraphs[0].font.size = Pt(44)
    title_shape.text_frame.paragraphs[0].font.color.rgb = THEME_COLORS["ink"]
    title_shape.text_frame.paragraphs[0].font.bold = True

    if subtitle:
        subtitle_shape.text = subtitle
        subtitle_shape.text_frame.paragraphs[0].font.size = Pt(20)
        subtitle_shape.text_frame.paragraphs[0].font.color.rgb = THEME_COLORS["muted"]

    logger.debug(f"Added title slide: {title}")


def add_content_slide(
    prs: Presentation,
    title: str,
    content: list[str],
    is_bullets: bool = True
) -> None:
    """
    Add content slide with title and bullet points or paragraphs.

    Args:
        prs: Presentation object
        title: Slide title
        content: List of content items
        is_bullets: Whether to format as bullets (default True)
    """
    slide_layout = prs.slide_layouts[1]  # Title and content layout
    slide = prs.slides.add_slide(slide_layout)

    title_shape = slide.shapes.title
    title_shape.text = title
    title_shape.text_frame.paragraphs[0].font.size = Pt(32)
    title_shape.text_frame.paragraphs[0].font.color.rgb = THEME_COLORS["ink"]

    # Add content
    content_shape = slide.placeholders[1]
    text_frame = content_shape.text_frame
    text_frame.clear()

    for i, item in enumerate(content):
        if i == 0:
            p = text_frame.paragraphs[0]
        else:
            p = text_frame.add_paragraph()

        p.text = item
        p.font.size = Pt(18)
        p.font.color.rgb = THEME_COLORS["muted"]

        if is_bullets:
            p.level = 0

    logger.debug(f"Added content slide: {title} ({len(content)} items)")


def add_section_header_slide(prs: Presentation, section_title: str) -> None:
    """
    Add section header slide (like banner in PDF).

    Args:
        prs: Presentation object
        section_title: Section heading text
    """
    slide_layout = prs.slide_layouts[2]  # Section header layout
    slide = prs.slides.add_slide(slide_layout)

    title_shape = slide.shapes.title
    title_shape.text = section_title
    title_shape.text_frame.paragraphs[0].font.size = Pt(40)
    title_shape.text_frame.paragraphs[0].font.color.rgb = RGBColor(255, 255, 255)
    title_shape.text_frame.paragraphs[0].font.bold = True
    title_shape.text_frame.paragraphs[0].alignment = PP_ALIGN.CENTER

    # Set background color
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = THEME_COLORS["accent"]

    logger.debug(f"Added section header: {section_title}")


def add_image_slide(
    prs: Presentation,
    title: str,
    image_path: Path,
    caption: str = ""
) -> None:
    """
    Add slide with image and optional caption.

    Args:
        prs: Presentation object
        title: Slide title
        image_path: Path to image file
        caption: Image caption (optional)
    """
    slide_layout = prs.slide_layouts[6]  # Blank layout
    slide = prs.slides.add_slide(slide_layout)

    # Add title
    left = Inches(0.5)
    top = Inches(0.3)
    width = Inches(9)
    height = Inches(0.8)

    title_box = slide.shapes.add_textbox(left, top, width, height)
    text_frame = title_box.text_frame
    p = text_frame.paragraphs[0]
    p.text = title
    p.font.size = Pt(28)
    p.font.color.rgb = THEME_COLORS["ink"]
    p.font.bold = True

    # Add image (centered)
    if image_path.exists():
        left = Inches(1.5)
        top = Inches(1.5)
        max_width = Inches(7)
        max_height = Inches(3.5)

        slide.shapes.add_picture(
            str(image_path),
            left, top,
            width=max_width
        )

    # Add caption if provided
    if caption:
        left = Inches(0.5)
        top = Inches(5)
        width = Inches(9)
        height = Inches(0.5)

        caption_box = slide.shapes.add_textbox(left, top, width, height)
        text_frame = caption_box.text_frame
        p = text_frame.paragraphs[0]
        p.text = caption
        p.font.size = Pt(14)
        p.font.color.rgb = THEME_COLORS["muted"]
        p.font.italic = True
        p.alignment = PP_ALIGN.CENTER

    logger.debug(f"Added image slide: {title}")


def save_presentation(prs: Presentation, output_path: Path) -> None:
    """
    Save presentation to file.

    Args:
        prs: Presentation object
        output_path: Path to output file

    Raises:
        IOError: If save fails
    """
    try:
        # Ensure parent directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)

        prs.save(str(output_path))
        logger.info(f"Saved presentation: {output_path}")

    except Exception as e:
        logger.error(f"Failed to save presentation: {e}")
        raise IOError(f"Failed to save presentation: {e}")
