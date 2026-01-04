"""
LLM service for intelligent content transformation.

Provides OpenAI-powered content summarization, slide generation, and enhancement.
"""

import os
import json
from typing import Optional
from loguru import logger
from openai import OpenAI


class LLMService:
    """
    LLM service for intelligent content processing.

    Uses OpenAI GPT models for content summarization, slide generation,
    and executive presentation enhancement.
    """

    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-4o-mini"):
        """
        Initialize LLM service.

        Args:
            api_key: OpenAI API key. If not provided, uses OPENAI_API_KEY env var.
            model: Model to use (default: gpt-4o-mini for cost efficiency)
        """
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.model = model
        self.client = None

        if self.api_key:
            self.client = OpenAI(api_key=self.api_key)
            logger.info(f"LLM service initialized with model: {model}")
        else:
            logger.warning("No OpenAI API key provided - LLM features disabled")

    def is_available(self) -> bool:
        """Check if LLM service is available."""
        return self.client is not None

    def generate_executive_summary(self, content: str, max_points: int = 5) -> str:
        """
        Generate executive summary from content.

        Args:
            content: Raw content to summarize
            max_points: Maximum number of key points

        Returns:
            Executive summary as markdown bullet points
        """
        if not self.is_available():
            return ""

        prompt = f"""Analyze the following content and create an executive summary suitable for senior leadership.

Requirements:
- Maximum {max_points} key points
- Focus on strategic insights, outcomes, and business impact
- Use clear, concise language
- Format as bullet points
- Each point should be 1-2 sentences max

Content:
{content[:8000]}

Respond with ONLY the bullet points, no introduction or conclusion."""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an executive communication specialist who creates clear, impactful summaries for senior leadership."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=500
            )
            summary = response.choices[0].message.content.strip()
            logger.debug(f"Generated executive summary: {len(summary)} chars")
            return summary
        except Exception as e:
            logger.error(f"Failed to generate executive summary: {e}")
            return ""

    def generate_slide_structure(self, content: str, max_slides: int = 10) -> list[dict]:
        """
        Generate optimized slide structure from content.

        Args:
            content: Markdown content to convert
            max_slides: Maximum number of content slides

        Returns:
            List of slide dictionaries with title, bullets, and speaker_notes
        """
        if not self.is_available():
            return []

        prompt = f"""Convert the following content into a corporate presentation structure.

Requirements:
- Maximum {max_slides} slides (excluding title slide)
- Each slide should have:
  - A clear, action-oriented title (5-8 words)
  - 3-5 bullet points (concise, 10 words max each)
  - Speaker notes (2-3 sentences for context)
- Focus on key messages that matter to senior leadership
- Use professional business language
- Structure for logical flow

Content:
{content[:8000]}

Respond in JSON format:
[
  {{
    "title": "Slide Title",
    "bullets": ["Point 1", "Point 2", "Point 3"],
    "speaker_notes": "Context for the presenter..."
  }}
]"""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a presentation design expert who creates compelling executive presentations. Always respond with valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.4,
                max_tokens=2000,
                response_format={"type": "json_object"}
            )
            result = response.choices[0].message.content.strip()
            logger.debug(f"Slide structure raw response: {result[:200]}...")

            data = json.loads(result)

            # Handle various response formats
            if isinstance(data, list):
                slides = data
            elif isinstance(data, dict):
                # Try common keys
                slides = data.get("slides", data.get("presentation", data.get("content", [])))
                if not slides and len(data) == 1:
                    # Single key with array value
                    slides = list(data.values())[0]
            else:
                slides = []

            # Validate slide structure
            valid_slides = []
            for slide in slides:
                if isinstance(slide, dict) and slide.get("title"):
                    valid_slides.append({
                        "title": slide.get("title", ""),
                        "bullets": slide.get("bullets", slide.get("content", slide.get("points", []))),
                        "speaker_notes": slide.get("speaker_notes", slide.get("notes", ""))
                    })

            logger.debug(f"Generated slide structure: {len(valid_slides)} slides")
            return valid_slides
        except Exception as e:
            logger.error(f"Failed to generate slide structure: {e}")
            return []

    def enhance_bullet_points(self, bullets: list[str]) -> list[str]:
        """
        Enhance bullet points for executive presentation.

        Args:
            bullets: List of raw bullet points

        Returns:
            Enhanced bullet points
        """
        if not self.is_available() or not bullets:
            return bullets

        prompt = f"""Enhance these bullet points for an executive presentation.

Requirements:
- Start each with an action verb or key metric
- Keep each under 12 words
- Make them impactful and clear
- Maintain the original meaning

Bullet points:
{chr(10).join(f'- {b}' for b in bullets)}

Respond with ONLY the enhanced bullet points, one per line, starting with "-"."""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an executive communication specialist."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=300
            )
            result = response.choices[0].message.content.strip()
            enhanced = [line.lstrip("- ").strip() for line in result.split("\n") if line.strip().startswith("-")]
            return enhanced if enhanced else bullets
        except Exception as e:
            logger.error(f"Failed to enhance bullets: {e}")
            return bullets

    def generate_speaker_notes(self, slide_title: str, slide_content: list[str]) -> str:
        """
        Generate speaker notes for a slide.

        Args:
            slide_title: Title of the slide
            slide_content: Bullet points on the slide

        Returns:
            Speaker notes text
        """
        if not self.is_available():
            return ""

        prompt = f"""Generate speaker notes for this presentation slide.

Slide Title: {slide_title}
Content:
{chr(10).join(f'- {c}' for c in slide_content)}

Requirements:
- 2-3 sentences providing context
- Include key talking points
- Professional tone

Respond with ONLY the speaker notes text."""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a presentation coach."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.4,
                max_tokens=200
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            logger.error(f"Failed to generate speaker notes: {e}")
            return ""

    def suggest_chart_data(self, content: str) -> list[dict]:
        """
        Suggest charts/visualizations based on content.

        Args:
            content: Content to analyze

        Returns:
            List of chart suggestions with type, title, and data
        """
        if not self.is_available():
            return []

        prompt = f"""Analyze this content and suggest data visualizations.

Content:
{content[:4000]}

For each visualization opportunity, provide:
- chart_type: "bar", "pie", "line", or "comparison"
- title: Chart title
- data: List of {{label, value}} pairs (use realistic numbers if not explicit)

Return JSON array. If no visualizations make sense, return empty array [].

Example format:
[{{"chart_type": "bar", "title": "Revenue by Quarter", "data": [{{"label": "Q1", "value": 100}}]}}]"""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a data visualization expert."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=1000,
                response_format={"type": "json_object"}
            )
            result = response.choices[0].message.content.strip()
            data = json.loads(result)
            if isinstance(data, dict) and "charts" in data:
                return data["charts"]
            elif isinstance(data, list):
                return data
            return []
        except Exception as e:
            logger.error(f"Failed to suggest chart data: {e}")
            return []


# Singleton instance with lazy initialization
_llm_service: Optional[LLMService] = None


def get_llm_service(api_key: Optional[str] = None) -> LLMService:
    """
    Get or create LLM service instance.

    Args:
        api_key: Optional API key to initialize with

    Returns:
        LLMService instance
    """
    global _llm_service
    if _llm_service is None:
        _llm_service = LLMService(api_key=api_key)
    return _llm_service
