"""
Prompts for summary and slide structure generation.

These prompts are used by LLMService for executive summaries,
slide structure generation, and visualization suggestions.
"""

# General summary prompt
SUMMARY_PROMPT = """Summarize the following content into {max_points} key points.

Each point should:
- Be concise (1-2 sentences)
- Capture a distinct key concept or insight
- Be actionable or informative

Content:
{content}

Return ONLY the bullet points, one per line, starting with "- "."""


# Executive summary prompt
EXECUTIVE_SUMMARY_PROMPT = """Create an executive summary of the following document.

The summary should:
1. Be 3-5 paragraphs
2. Start with a high-level overview (1 paragraph)
3. Cover the main topics and key insights (2-3 paragraphs)  
4. End with conclusions or implications (1 paragraph)
5. Be suitable for a busy executive who needs to quickly understand the content
6. Use professional, clear language

Document content:
{content}

Write the executive summary now:"""


# Slide structure prompt
SLIDE_STRUCTURE_PROMPT = """Create a presentation outline from the following content.

Requirements:
- Maximum {max_slides} slides
- Each slide should have:
  - A clear, concise title (5-8 words)
  - 3-5 bullet points (10-15 words each)
  - Optional: notes for the presenter

Content:
{content}

Return the structure as JSON in this format:
{{
  "title": "Presentation Title",
  "slides": [
    {{
      "title": "Slide Title",
      "bullets": ["Point 1", "Point 2", "Point 3"],
      "notes": "Optional presenter notes"
    }}
  ]
}}"""


# Visualization suggestion prompt
VISUALIZATION_SUGGESTION_PROMPT = """Analyze this content and suggest up to {max_visuals} visualizations that would help explain the concepts.

For each suggestion, provide:
1. Type: architecture, flowchart, comparison, mind_map, or concept_map
2. Title: A short, descriptive title
3. Data: Structured data for the visualization

Content:
{content}

Return as JSON array:
[
  {{
    "type": "architecture|flowchart|comparison|mind_map|concept_map",
    "title": "Visualization Title",
    "data": {{ ... type-specific data ... }}
  }}
]

Type-specific data formats:
- architecture: {{"components": [...], "connections": [...]}}
- flowchart: {{"nodes": [...], "edges": [...]}}
- comparison: {{"items": [...], "categories": [...]}}
- mind_map: {{"central": "...", "branches": [...]}}
- concept_map: {{"concepts": [...], "relationships": [...]}}"""


# Chart data suggestion prompt
CHART_DATA_PROMPT = """Based on this content, extract or estimate data suitable for a chart.

Content:
{content}

Provide chart data in this JSON format:
{{
  "chart_type": "bar|line|pie|scatter",
  "title": "Chart Title",
  "x_label": "X Axis Label",
  "y_label": "Y Axis Label", 
  "data": [
    {{"label": "Item 1", "value": 10}},
    {{"label": "Item 2", "value": 20}}
  ]
}}

If no suitable data can be extracted, return:
{{"chart_type": "none", "reason": "explanation"}}"""
