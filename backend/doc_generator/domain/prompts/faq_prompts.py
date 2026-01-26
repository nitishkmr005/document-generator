"""
Prompts for FAQ generation.

Extracts Q&A pairs with tags from source content.
"""

FAQ_EXTRACTION_PROMPT = """You are an expert at creating FAQ documents from source content.

Analyze the following content and extract relevant frequently asked questions with answers.

**Instructions:**
1. Identify key topics and concepts in the content
2. Generate questions that users would naturally ask about these topics
3. Write clear, helpful answers based on the source content
4. Assign 1-3 relevant topic tags to each question
5. Generate exactly {faq_count} FAQ items
6. Answer format: {answer_format}
7. Detail level: {detail_level}
8. FAQ mode: {mode}
9. Audience persona: {audience}
10. Answers can use markdown formatting (bold, lists, code blocks)

Guidance:
- If answer format is "bulleted", use concise bullet points.
- If answer format is "concise", use short paragraphs.
- Detail level: short = 1-2 sentences, medium = 2-4 sentences, deep = 4-8 sentences with specifics.
- Mode should influence the types of questions asked.
- Audience persona should influence tone and terminology.

**Content to analyze:**
{content}

**Output JSON format:**
{{
  "title": "FAQ title based on content topic",
  "description": "Brief description of what these FAQs cover",
  "items": [
    {{
      "id": "faq-1",
      "question": "What is X?",
      "answer": "X is... **Key points:**\\n- Point 1\\n- Point 2",
      "tags": ["topic1", "topic2"]
    }}
  ]
}}

Return ONLY valid JSON, no other text."""


def build_faq_extraction_prompt(
    content: str,
    faq_count: int,
    answer_format: str,
    detail_level: str,
    mode: str,
    audience: str,
) -> str:
    """Build the FAQ extraction prompt with content.

    Args:
        content: Source content to extract FAQs from
        faq_count: Number of FAQ items to generate
        answer_format: Answer format (concise or bulleted)
        detail_level: Answer depth (short, medium, deep)
        mode: FAQ mode (balanced, onboarding, how_to_use, troubleshooting, technical_deep_dive)
        audience: Audience persona (general_reader, developer, business, compliance, support)

    Returns:
        Formatted prompt string
    """
    return FAQ_EXTRACTION_PROMPT.format(
        content=content,
        faq_count=faq_count,
        answer_format=answer_format,
        detail_level=detail_level,
        mode=mode,
        audience=audience,
    )
