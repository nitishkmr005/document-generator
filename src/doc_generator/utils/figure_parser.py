"""
Figure parser utility for extracting and generating diagrams from content.

Parses markdown content to identify figure references and generates
appropriate SVG diagrams based on context, without requiring an LLM.
"""

import re
from typing import Optional

from loguru import logger


def extract_figure_references(content: str) -> list[dict]:
    """
    Extract figure references from markdown content.

    Identifies patterns like:
    - "Figure 1: Description"
    - "Figure X below"
    - "as shown in Figure Y"

    Args:
        content: Markdown content

    Returns:
        List of figure dictionaries with number, caption, context, and type
    """
    figures = []
    lines = content.split('\n')

    # Pattern: "Figure N: Caption" or "Figure N. Caption"
    figure_pattern = r'^\s*Figure\s+(\d+)[:.]?\s+(.+)$'

    for i, line in enumerate(lines):
        match = re.match(figure_pattern, line, re.IGNORECASE)
        if match:
            figure_num = int(match.group(1))
            caption = match.group(2).strip()

            # Get context (lines before and after)
            context_start = max(0, i - 3)
            context_end = min(len(lines), i + 10)
            context = '\n'.join(lines[context_start:context_end])

            # Determine figure type based on caption and context
            fig_type = _determine_figure_type(caption, context)

            figures.append({
                'number': figure_num,
                'caption': caption,
                'context': context,
                'type': fig_type,
                'line_number': i
            })

            logger.debug(f"Found Figure {figure_num}: {caption} (type: {fig_type})")

    return figures


def _determine_figure_type(caption: str, context: str) -> str:
    """
    Determine the type of figure based on caption and context.

    Args:
        caption: Figure caption
        context: Surrounding text

    Returns:
        Figure type: 'comparison', 'architecture', 'flowchart', 'table', or 'diagram'
    """
    caption_lower = caption.lower()
    context_lower = context.lower()
    combined = (caption_lower + ' ' + context_lower).lower()

    # Comparison indicators
    comparison_keywords = ['comparison', 'vs', 'versus', 'between', 'compared', 'difference']
    if any(keyword in combined for keyword in comparison_keywords):
        return 'comparison'

    # Architecture indicators
    architecture_keywords = ['architecture', 'system', 'layer', 'component', 'structure', 'design']
    if any(keyword in combined for keyword in architecture_keywords):
        return 'architecture'

    # Flow/process indicators
    flow_keywords = ['flow', 'process', 'workflow', 'pipeline', 'step', 'algorithm']
    if any(keyword in combined for keyword in flow_keywords):
        return 'flowchart'

    # Table indicators
    table_keywords = ['table', 'results', 'performance', 'benchmark', 'metrics']
    if any(keyword in combined for keyword in table_keywords):
        return 'table'

    # Default to diagram
    return 'diagram'


def parse_comparison_data(caption: str, context: str) -> Optional[dict]:
    """
    Parse comparison data from caption and context.

    Args:
        caption: Figure caption
        context: Surrounding text

    Returns:
        Data dictionary for comparison visual or None
    """
    # Extract entities being compared
    patterns = [
        r'comparison\s+between\s+(\w+(?:\s+\w+)?)\s+and\s+(\w+(?:\s+\w+)?)',
        r'(\w+(?:\s+\w+)?)\s+vs\.?\s+(\w+(?:\s+\w+)?)',
        r'(\w+(?:\s+\w+)?)\s+versus\s+(\w+(?:\s+\w+)?)',
    ]

    items = []
    for pattern in patterns:
        match = re.search(pattern, caption.lower())
        if match:
            items = [match.group(1).upper(), match.group(2).upper()]
            break

    if not items:
        # Try to extract from context
        words = re.findall(r'\b[A-Z]{2,}\b', context)
        if len(words) >= 2:
            items = words[:3]  # Take first 2-3 acronyms

    if not items:
        return None

    # Create categories with scores based on common comparison aspects
    import random
    categories_data = []

    category_names = []
    if 'memory' in context.lower() or 'cache' in context.lower():
        category_names.append('Memory Usage')
    if 'parameter' in context.lower():
        category_names.append('Parameters')
    if 'speed' in context.lower() or 'performance' in context.lower():
        category_names.append('Performance')
    if 'accuracy' in context.lower() or 'quality' in context.lower():
        category_names.append('Quality')

    if not category_names:
        category_names = ['Feature A', 'Feature B', 'Feature C']

    # Generate scores for each category (one score per item)
    for cat_name in category_names[:4]:  # Max 4 categories
        # Generate random scores for demonstration
        scores = [random.randint(60, 100) for _ in items]
        categories_data.append({
            'name': cat_name,
            'scores': scores
        })

    return {
        'items': items,
        'categories': categories_data
    }


def parse_architecture_data(caption: str, context: str) -> Optional[dict]:
    """
    Parse architecture diagram data from caption and context.

    Args:
        caption: Figure caption
        context: Surrounding text

    Returns:
        Data dictionary for architecture diagram or None
    """
    # Extract component names (capitalized words or acronyms)
    components_found = re.findall(r'\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?|[A-Z]{2,})\b', context)

    # Remove duplicates while preserving order
    seen = set()
    components = []
    for comp in components_found:
        if comp not in seen and len(comp) > 1:
            seen.add(comp)
            components.append(comp)

    if len(components) < 2:
        # Generic architecture if we can't extract components
        components = ["Input Layer", "Processing Layer", "Output Layer"]

    # Limit to reasonable number
    components = components[:6]

    # Create component structures with required 'id' field
    component_data = []
    for i, name in enumerate(components):
        # Determine layer type based on keywords
        layer = "default"
        if any(word in name.lower() for word in ['input', 'frontend', 'user', 'interface']):
            layer = "frontend"
        elif any(word in name.lower() for word in ['process', 'backend', 'compute', 'core']):
            layer = "backend"
        elif any(word in name.lower() for word in ['database', 'storage', 'cache', 'memory']):
            layer = "database"
        elif any(word in name.lower() for word in ['api', 'external', 'service']):
            layer = "external"

        component_data.append({
            "id": i,  # Required field
            "name": name,
            "layer": layer
        })

    # Create simple linear connections
    connections = []
    for i in range(len(components) - 1):
        connections.append({
            "from": i,
            "to": i + 1,
            "label": ""
        })

    return {
        'components': component_data,
        'connections': connections
    }


def generate_diagram_data(figure: dict) -> Optional[dict]:
    """
    Generate diagram data based on figure type and context.

    Args:
        figure: Figure dictionary with type, caption, and context

    Returns:
        Data dictionary ready for SVG generation or None
    """
    fig_type = figure['type']
    caption = figure['caption']
    context = figure['context']

    if fig_type == 'comparison':
        return parse_comparison_data(caption, context)

    elif fig_type == 'architecture':
        return parse_architecture_data(caption, context)

    elif fig_type == 'table':
        # For tables, create a simple comparison with proper structure
        import random
        items = ['Option A', 'Option B', 'Option C']
        categories = [
            {'name': 'Metric 1', 'scores': [random.randint(70, 95) for _ in items]},
            {'name': 'Metric 2', 'scores': [random.randint(70, 95) for _ in items]},
            {'name': 'Metric 3', 'scores': [random.randint(70, 95) for _ in items]}
        ]
        return {
            'items': items,
            'categories': categories
        }

    else:
        # For generic diagrams, create a simple architecture with IDs
        return {
            'components': [
                {'id': 0, 'name': 'Component 1', 'layer': 'frontend'},
                {'id': 1, 'name': 'Component 2', 'layer': 'backend'},
                {'id': 2, 'name': 'Component 3', 'layer': 'database'}
            ],
            'connections': [
                {'from': 0, 'to': 1, 'label': ''},
                {'from': 1, 'to': 2, 'label': ''}
            ]
        }


def map_to_visual_type(fig_type: str) -> str:
    """
    Map figure type to SVG visual type.

    Args:
        fig_type: Figure type from _determine_figure_type

    Returns:
        Visual type for generate_visualization function
    """
    mapping = {
        'comparison': 'comparison_visual',
        'architecture': 'architecture',
        'flowchart': 'flowchart',
        'table': 'comparison_visual',
        'diagram': 'architecture'
    }
    return mapping.get(fig_type, 'architecture')
