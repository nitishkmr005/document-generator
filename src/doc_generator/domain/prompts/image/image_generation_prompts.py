"""
Prompt templates for image generation and evaluation.
"""

from ..content_types import ImageType


def build_gemini_image_prompt(image_type: ImageType, prompt: str, size_hint: str) -> str:
    """
    Build Gemini image generation prompt with size hints.
    """
    if image_type == ImageType.INFOGRAPHIC:
        return f"""Create a vibrant, educational infographic that explains: {prompt}

Style requirements:
- Clean, modern infographic design
- Use clear icons only when they represent actual concepts
- Include clear labels and annotations
- Use a professional color palette (blues, teals, oranges)
- Make it suitable for inclusion in a professional document
- No text-heavy design - focus on visual explanation
- High contrast for readability when printed
- Use ONLY the concepts in the prompt; do not add new information
- Avoid metaphorical objects (pipes, ropes, factories) unless explicitly mentioned
- For workflows/architectures, use flat rounded rectangles + arrows in a clean grid
{size_hint}"""

    if image_type == ImageType.DECORATIVE:
        return f"""Create a professional, thematic header image for: {prompt}

Style requirements:
- Abstract or semi-abstract design
- Professional and modern aesthetic
- Subtle and elegant - not distracting
- Use muted, professional colors
- Suitable as a section header in a document
- Wide aspect ratio (16:9 or similar)
- No text in the image
- Use ONLY the concepts in the prompt; do not add new information
{size_hint}"""

    if image_type == ImageType.MERMAID:
        return f"""Create a professional, clean flowchart/diagram image that represents: {prompt}

Style requirements:
- Clean, modern diagram design with clear flow
- Use boxes, arrows, and connections to show relationships
- Professional color scheme (blues, grays, with accent colors)
- Include clear labels for each step/component
- Make it suitable for inclusion in a corporate document
- High contrast for readability when printed
- No watermarks or decorative elements
- Focus on clarity and visual hierarchy
- Use ONLY the concepts in the prompt; do not add new information
{size_hint}"""

    return prompt


def build_alignment_prompt(section_title: str, content: str) -> str:
    """
    Prompt to validate image alignment with content.
    """
    return (
        "Check if this image aligns with the section content below. "
        "Confirm the image title text matches the section title. "
        "Return JSON only with keys: "
        "{\"aligned\": true|false, "
        "\"notes\": \"short reason\", "
        "\"visual_feedbacks\": [\"short visual issue/strength\"], "
        "\"labels_or_text_feedback\": [\"label/text issue/strength\"]}.\n\n"
        f"Section Title: {section_title}\n\n"
        f"Section Content:\n{content[:2000]}"
    )


def build_prompt_improvement_prompt(
    section_title: str,
    content: str,
    original_prompt: str,
    alignment_notes: str,
) -> str:
    """
    Prompt to improve image prompt based on alignment feedback.
    """
    return (
        "Improve the image generation prompt to better align with the section content. "
        "Use ONLY concepts present in the content. Return ONLY the revised prompt text.\n\n"
        f"Section Title: {section_title}\n\n"
        f"Section Content:\n{content[:2000]}\n\n"
        f"Original Prompt:\n{original_prompt}\n\n"
        f"Alignment Notes:\n{alignment_notes}\n"
    )


def build_image_description_prompt(section_title: str, content: str) -> str:
    """
    Prompt to describe an image based on section content.
    """
    return (
        "Write a concise blog-style description of this image. "
        "Use only what is visible and what is supported by the section content. "
        "Keep it to 2-4 sentences.\n\n"
        f"Section Title: {section_title}\n\n"
        f"Section Content:\n{content[:2000]}"
    )


def build_prompt_generator_prompt(
    section_title: str,
    content_preview: str,
    style_hint: str,
    required_labels_str: str,
    visual_title: str,
    visual_desc: str,
) -> str:
    """
    Prompt to generate a content-specific image prompt.
    """
    style_requirements = (
        "Use a clean block-diagram style: flat rounded rectangles, thin arrows, "
        "muted teal/orange/gray palette, light background with subtle dotted grid. "
        "Minimal icons only when needed, no photos, no textures."
    )
    if style_hint in ("architecture_diagram", "process_flow"):
        style_requirements += " Prefer left-to-right flow with labeled steps."

    prompt = "Create an image prompt for a diagram.\n\n"
    prompt += f"Title: {visual_title}\n"
    if visual_desc:
        prompt += f"Description: {visual_desc}\n"
    prompt += f"Style: {style_hint.replace('_', ' ')}\n"
    prompt += f"Required labels (verbatim): {required_labels_str}\n"
    prompt += f"Style guide: {style_requirements}\n\n"
    prompt += "Constraints:\n"
    prompt += "- Use ONLY concepts present in the content below.\n"
    prompt += "- Do NOT add new stages, tools, or labels.\n"
    prompt += "- Avoid metaphorical objects (pipes, ropes, factories).\n"
    prompt += f"- The image title text must exactly match: {section_title}.\n"
    prompt += "- Return ONLY the final image prompt text.\n\n"
    prompt += f"Content:\n{content_preview}\n"
    return prompt
