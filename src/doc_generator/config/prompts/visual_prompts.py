"""
Prompts for visual/SVG generation.

These prompts are used by ClaudeSVGGenerator and LLMContentGenerator
to create diagram data and SVG visualizations.
"""

# Visual data generation prompt
VISUAL_DATA_PROMPT = """Generate structured data for a {visual_type} diagram.

**Title**: {title}
**Description**: {description}
**Context**: {context}

Generate JSON data in this format:
{format_example}

Requirements:
- Keep text labels SHORT (max 20 characters) to prevent overlap
- Include 4-8 elements for clarity
- Make connections logical based on the description
- Use clear, concise names

Respond with ONLY valid JSON, no explanations:"""


# Data format examples for different visual types
VISUAL_DATA_FORMATS = {
    "architecture": """{
  "components": [{"id": "1", "name": "Component Name", "layer": "frontend|backend|database|external"}],
  "connections": [{"from": "1", "to": "2", "label": "connection type"}]
}""",
    "flowchart": """{
  "nodes": [{"id": "1", "type": "start|end|process|decision", "text": "Node text"}],
  "edges": [{"from": "1", "to": "2", "label": "optional label"}]
}""",
    "comparison": """{
  "items": ["Option A", "Option B"],
  "categories": [{"name": "Category", "scores": [8, 6]}]
}""",
    "comparison_visual": """{
  "items": ["Option A", "Option B"],
  "categories": [{"name": "Category", "scores": [8, 6]}]
}""",
    "concept_map": """{
  "concepts": [{"id": "1", "text": "Concept", "level": 0}],
  "relationships": [{"from": "1", "to": "2", "label": "relates to"}]
}""",
    "mind_map": """{
  "central": "Main Topic",
  "branches": [{"text": "Branch 1", "children": ["Sub 1.1", "Sub 1.2"]}]
}"""
}


# SVG generation prompts by type
SVG_ARCHITECTURE_PROMPT = """Generate a professional SVG architecture diagram with the following specifications:

Title: {title}

Components:
{components}

Connections:
{connections}

Requirements:
1. Create a clean, professional architecture diagram in SVG format
2. Use a modern color palette (teal #1E5D5A for backend, blue #2E86AB for frontend, magenta #A23B72 for database, orange #D76B38 for external services)
3. Components should be rounded rectangles with drop shadows
4. Connections should be arrows with labels if provided
5. Layout components in logical layers (frontend → backend → database)
6. Use clear, readable fonts (14-16px for component names)
7. Add subtle gradients and professional styling
8. SVG viewBox should be approximately 1000x600
9. Include proper spacing between components (80-100px)
10. Make it visually similar to professional architecture diagrams

{validation_feedback}

Return ONLY the SVG code, no explanations or markdown code blocks."""


SVG_FLOWCHART_PROMPT = """Generate a professional SVG flowchart with the following specifications:

Title: {title}

Nodes:
{nodes}

Edges (Connections):
{edges}

Requirements:
1. Create a top-to-bottom flowchart
2. Start/End nodes: rounded rectangles with teal color (#1E5D5A)
3. Process nodes: rectangles with blue color (#2E86AB)
4. Decision nodes: diamond shapes with orange color (#D76B38)
5. Use arrows to connect nodes with labels if provided
6. Layout nodes vertically with proper spacing (100px vertical gaps)
7. Center-align nodes horizontally when possible
8. Add subtle drop shadows for depth
9. Use clear, readable fonts (13px for node text, 11px for edge labels)
10. SVG viewBox should fit content (approximately 800x1000)

{validation_feedback}

Return ONLY the SVG code, no explanations or markdown code blocks."""


SVG_COMPARISON_PROMPT = """Generate a professional SVG comparison visual with the following specifications:

Title: {title}

Items to Compare: {items}

Categories with Scores:
{categories}

Requirements:
1. Create a modern comparison table/matrix
2. Header row with items across the top
3. Category names in the left column
4. Use colored bars to show scores (teal #1E5D5A, orange #D76B38, blue #2E86AB)
5. Add rounded corners to the table
6. Alternate row colors for readability (#F8F9FA and white)
7. Clear, professional typography (14px for headers, 12px for content)
8. Add subtle borders and shadows
9. SVG viewBox should fit the content (approximately 900x500)
10. Make it clean and professional like a modern dashboard

{validation_feedback}

Return ONLY the SVG code, no explanations or markdown code blocks."""


SVG_CONCEPT_MAP_PROMPT = """Generate a professional SVG concept map with the following specifications:

Title: {title}

Concepts:
{concepts}

Relationships:
{relationships}

Requirements:
1. Create a hierarchical concept map
2. Concepts should be ellipses with varying colors by level
3. Level 0: teal (#1E5D5A), Level 1: blue (#2E86AB), Level 2: orange (#D76B38)
4. Connect concepts with dotted lines and arrows
5. Add relationship labels in italics along the connecting lines
6. Layout concepts in levels (top-level at top, children below)
7. Use clear, readable fonts (12px for concept text, 10px for relationships)
8. Add subtle drop shadows
9. SVG viewBox should fit content (approximately 900x700)
10. Make it visually clean and hierarchical

{validation_feedback}

Return ONLY the SVG code, no explanations or markdown code blocks."""


SVG_MIND_MAP_PROMPT = """Generate a professional SVG mind map with the following specifications:

Title: {title}

Central Topic: {central}

Branches:
{branches}

Requirements:
1. Create a radial mind map with the central topic in the center
2. Branches radiate outward in a circular pattern
3. Use varying colors for different branches (use palette: #1E5D5A, #D76B38, #2E86AB, #A23B72, #F18F01)
4. Central node should be larger and prominent (ellipse with gradient)
5. Branch nodes should be rounded ellipses
6. Connect nodes with smooth curves, not straight lines
7. Use clear, readable fonts (16px for central, 12px for branches, 10px for children)
8. Add subtle drop shadows for depth
9. SVG viewBox should be approximately 1000x700
10. Make it visually appealing and professional

{validation_feedback}

Return ONLY the SVG code, no explanations or markdown code blocks."""
