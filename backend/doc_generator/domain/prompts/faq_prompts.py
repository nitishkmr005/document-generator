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
5. The number of FAQs should match content depth (typically 5-20 items)
6. Answers can use markdown formatting (bold, lists, code blocks)

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


def build_faq_extraction_prompt(content: str) -> str:
    """Build the FAQ extraction prompt with content.

    Args:
        content: Source content to extract FAQs from

    Returns:
        Formatted prompt string
    """
    return FAQ_EXTRACTION_PROMPT.format(content=content)
