"""
SVG chart generator for data visualizations.

Creates professional SVG charts for presentations.
"""

from pathlib import Path
from typing import Optional
from loguru import logger

# Corporate color palette
CHART_COLORS = [
    "#1E5D5A",  # Teal (primary)
    "#D76B38",  # Orange (accent)
    "#2E86AB",  # Blue
    "#A23B72",  # Magenta
    "#F18F01",  # Amber
    "#C73E1D",  # Red
    "#3A7CA5",  # Steel blue
    "#5C946E",  # Green
]

BACKGROUND_COLOR = "#FFFFFF"
TEXT_COLOR = "#1C1C1C"
MUTED_COLOR = "#666666"
GRID_COLOR = "#E0E0E0"


class SVGGenerator:
    """
    Generate professional SVG charts for presentations.
    """

    def __init__(self, width: int = 800, height: int = 500):
        """
        Initialize SVG generator.

        Args:
            width: Chart width in pixels
            height: Chart height in pixels
        """
        self.width = width
        self.height = height
        self.padding = 60
        self.font_family = "Arial, Helvetica, sans-serif"

    def generate_bar_chart(
        self,
        data: list[dict],
        title: str,
        output_path: Optional[Path] = None
    ) -> str:
        """
        Generate horizontal bar chart.

        Args:
            data: List of {label, value} dictionaries
            title: Chart title
            output_path: Optional path to save SVG

        Returns:
            SVG string
        """
        if not data:
            return ""

        chart_width = self.width - 2 * self.padding - 100  # Extra space for labels
        chart_height = self.height - 2 * self.padding - 40  # Space for title

        max_value = max(d.get("value", 0) for d in data)
        if max_value == 0:
            max_value = 1

        bar_height = min(40, (chart_height - 20) / len(data) - 10)
        spacing = (chart_height - bar_height * len(data)) / (len(data) + 1)

        svg_parts = [
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {self.width} {self.height}" width="{self.width}" height="{self.height}">',
            f'<rect width="{self.width}" height="{self.height}" fill="{BACKGROUND_COLOR}"/>',
            # Title
            f'<text x="{self.width/2}" y="35" text-anchor="middle" font-family="{self.font_family}" font-size="24" font-weight="bold" fill="{TEXT_COLOR}">{self._escape(title)}</text>',
        ]

        # Draw bars
        y_start = self.padding + 40
        x_start = self.padding + 100  # Space for labels

        for i, item in enumerate(data):
            label = item.get("label", f"Item {i+1}")
            value = item.get("value", 0)
            bar_width = (value / max_value) * chart_width
            y = y_start + spacing + i * (bar_height + spacing)
            color = CHART_COLORS[i % len(CHART_COLORS)]

            # Label
            svg_parts.append(
                f'<text x="{x_start - 10}" y="{y + bar_height/2 + 5}" text-anchor="end" font-family="{self.font_family}" font-size="14" fill="{TEXT_COLOR}">{self._escape(str(label))}</text>'
            )

            # Bar with rounded corners
            svg_parts.append(
                f'<rect x="{x_start}" y="{y}" width="{bar_width}" height="{bar_height}" fill="{color}" rx="4" ry="4"/>'
            )

            # Value label
            svg_parts.append(
                f'<text x="{x_start + bar_width + 10}" y="{y + bar_height/2 + 5}" font-family="{self.font_family}" font-size="14" font-weight="bold" fill="{TEXT_COLOR}">{value}</text>'
            )

        svg_parts.append('</svg>')
        svg = '\n'.join(svg_parts)

        if output_path:
            self._save_svg(svg, output_path)

        return svg

    def generate_pie_chart(
        self,
        data: list[dict],
        title: str,
        output_path: Optional[Path] = None
    ) -> str:
        """
        Generate pie chart.

        Args:
            data: List of {label, value} dictionaries
            title: Chart title
            output_path: Optional path to save SVG

        Returns:
            SVG string
        """
        if not data:
            return ""

        total = sum(d.get("value", 0) for d in data)
        if total == 0:
            total = 1

        cx = self.width / 2 - 80
        cy = self.height / 2 + 20
        radius = min(self.width, self.height) / 3

        svg_parts = [
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {self.width} {self.height}" width="{self.width}" height="{self.height}">',
            f'<rect width="{self.width}" height="{self.height}" fill="{BACKGROUND_COLOR}"/>',
            # Title
            f'<text x="{self.width/2}" y="35" text-anchor="middle" font-family="{self.font_family}" font-size="24" font-weight="bold" fill="{TEXT_COLOR}">{self._escape(title)}</text>',
        ]

        # Draw pie slices
        start_angle = -90  # Start from top
        for i, item in enumerate(data):
            value = item.get("value", 0)
            percentage = value / total
            angle = percentage * 360
            end_angle = start_angle + angle

            # Calculate path
            path = self._pie_slice_path(cx, cy, radius, start_angle, end_angle)
            color = CHART_COLORS[i % len(CHART_COLORS)]

            svg_parts.append(f'<path d="{path}" fill="{color}" stroke="{BACKGROUND_COLOR}" stroke-width="2"/>')

            start_angle = end_angle

        # Legend
        legend_x = self.width - 160
        legend_y = 80

        for i, item in enumerate(data):
            label = item.get("label", f"Item {i+1}")
            value = item.get("value", 0)
            percentage = (value / total) * 100
            color = CHART_COLORS[i % len(CHART_COLORS)]
            y = legend_y + i * 28

            # Color box
            svg_parts.append(
                f'<rect x="{legend_x}" y="{y}" width="16" height="16" fill="{color}" rx="2"/>'
            )
            # Label
            svg_parts.append(
                f'<text x="{legend_x + 24}" y="{y + 13}" font-family="{self.font_family}" font-size="13" fill="{TEXT_COLOR}">{self._escape(str(label))} ({percentage:.0f}%)</text>'
            )

        svg_parts.append('</svg>')
        svg = '\n'.join(svg_parts)

        if output_path:
            self._save_svg(svg, output_path)

        return svg

    def generate_comparison_chart(
        self,
        data: list[dict],
        title: str,
        output_path: Optional[Path] = None
    ) -> str:
        """
        Generate comparison/column chart.

        Args:
            data: List of {label, value} dictionaries
            title: Chart title
            output_path: Optional path to save SVG

        Returns:
            SVG string
        """
        if not data:
            return ""

        chart_width = self.width - 2 * self.padding
        chart_height = self.height - 2 * self.padding - 60

        max_value = max(d.get("value", 0) for d in data)
        if max_value == 0:
            max_value = 1

        bar_width = min(60, (chart_width - 40) / len(data) - 20)
        spacing = (chart_width - bar_width * len(data)) / (len(data) + 1)

        x_start = self.padding
        y_bottom = self.height - self.padding - 30

        svg_parts = [
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {self.width} {self.height}" width="{self.width}" height="{self.height}">',
            f'<rect width="{self.width}" height="{self.height}" fill="{BACKGROUND_COLOR}"/>',
            # Title
            f'<text x="{self.width/2}" y="35" text-anchor="middle" font-family="{self.font_family}" font-size="24" font-weight="bold" fill="{TEXT_COLOR}">{self._escape(title)}</text>',
            # Baseline
            f'<line x1="{x_start}" y1="{y_bottom}" x2="{x_start + chart_width}" y2="{y_bottom}" stroke="{GRID_COLOR}" stroke-width="2"/>',
        ]

        # Grid lines
        for i in range(5):
            y = y_bottom - (i / 4) * chart_height
            value = (i / 4) * max_value
            svg_parts.append(
                f'<line x1="{x_start}" y1="{y}" x2="{x_start + chart_width}" y2="{y}" stroke="{GRID_COLOR}" stroke-width="1" stroke-dasharray="4"/>'
            )
            svg_parts.append(
                f'<text x="{x_start - 10}" y="{y + 5}" text-anchor="end" font-family="{self.font_family}" font-size="12" fill="{MUTED_COLOR}">{value:.0f}</text>'
            )

        # Draw columns
        for i, item in enumerate(data):
            label = item.get("label", f"Item {i+1}")
            value = item.get("value", 0)
            bar_height = (value / max_value) * chart_height
            x = x_start + spacing + i * (bar_width + spacing)
            y = y_bottom - bar_height
            color = CHART_COLORS[i % len(CHART_COLORS)]

            # Column
            svg_parts.append(
                f'<rect x="{x}" y="{y}" width="{bar_width}" height="{bar_height}" fill="{color}" rx="4" ry="4"/>'
            )

            # Value on top
            svg_parts.append(
                f'<text x="{x + bar_width/2}" y="{y - 8}" text-anchor="middle" font-family="{self.font_family}" font-size="14" font-weight="bold" fill="{TEXT_COLOR}">{value}</text>'
            )

            # Label below
            svg_parts.append(
                f'<text x="{x + bar_width/2}" y="{y_bottom + 20}" text-anchor="middle" font-family="{self.font_family}" font-size="12" fill="{TEXT_COLOR}">{self._escape(str(label))}</text>'
            )

        svg_parts.append('</svg>')
        svg = '\n'.join(svg_parts)

        if output_path:
            self._save_svg(svg, output_path)

        return svg

    def generate_line_chart(
        self,
        data: list[dict],
        title: str,
        output_path: Optional[Path] = None
    ) -> str:
        """
        Generate line chart.

        Args:
            data: List of {label, value} dictionaries
            title: Chart title
            output_path: Optional path to save SVG

        Returns:
            SVG string
        """
        if not data or len(data) < 2:
            return ""

        chart_width = self.width - 2 * self.padding - 40
        chart_height = self.height - 2 * self.padding - 60

        max_value = max(d.get("value", 0) for d in data)
        min_value = min(d.get("value", 0) for d in data)
        if max_value == min_value:
            max_value = min_value + 1

        x_start = self.padding + 40
        y_bottom = self.height - self.padding - 30

        svg_parts = [
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {self.width} {self.height}" width="{self.width}" height="{self.height}">',
            f'<rect width="{self.width}" height="{self.height}" fill="{BACKGROUND_COLOR}"/>',
            # Title
            f'<text x="{self.width/2}" y="35" text-anchor="middle" font-family="{self.font_family}" font-size="24" font-weight="bold" fill="{TEXT_COLOR}">{self._escape(title)}</text>',
            # Axes
            f'<line x1="{x_start}" y1="{y_bottom}" x2="{x_start + chart_width}" y2="{y_bottom}" stroke="{TEXT_COLOR}" stroke-width="2"/>',
            f'<line x1="{x_start}" y1="{y_bottom}" x2="{x_start}" y2="{y_bottom - chart_height}" stroke="{TEXT_COLOR}" stroke-width="2"/>',
        ]

        # Calculate points
        points = []
        x_step = chart_width / (len(data) - 1)

        for i, item in enumerate(data):
            value = item.get("value", 0)
            x = x_start + i * x_step
            y = y_bottom - ((value - min_value) / (max_value - min_value)) * chart_height
            points.append((x, y))

        # Draw area under line
        area_path = f"M {points[0][0]} {y_bottom}"
        for x, y in points:
            area_path += f" L {x} {y}"
        area_path += f" L {points[-1][0]} {y_bottom} Z"
        svg_parts.append(f'<path d="{area_path}" fill="{CHART_COLORS[0]}" fill-opacity="0.2"/>')

        # Draw line
        line_path = f"M {points[0][0]} {points[0][1]}"
        for x, y in points[1:]:
            line_path += f" L {x} {y}"
        svg_parts.append(f'<path d="{line_path}" stroke="{CHART_COLORS[0]}" stroke-width="3" fill="none"/>')

        # Draw points and labels
        for i, (x, y) in enumerate(points):
            label = data[i].get("label", f"{i+1}")
            value = data[i].get("value", 0)

            # Point
            svg_parts.append(f'<circle cx="{x}" cy="{y}" r="6" fill="{CHART_COLORS[0]}" stroke="{BACKGROUND_COLOR}" stroke-width="2"/>')

            # X-axis label
            svg_parts.append(
                f'<text x="{x}" y="{y_bottom + 18}" text-anchor="middle" font-family="{self.font_family}" font-size="11" fill="{TEXT_COLOR}">{self._escape(str(label))}</text>'
            )

        # Y-axis labels
        for i in range(5):
            y = y_bottom - (i / 4) * chart_height
            value = min_value + (i / 4) * (max_value - min_value)
            svg_parts.append(
                f'<text x="{x_start - 8}" y="{y + 4}" text-anchor="end" font-family="{self.font_family}" font-size="11" fill="{MUTED_COLOR}">{value:.0f}</text>'
            )

        svg_parts.append('</svg>')
        svg = '\n'.join(svg_parts)

        if output_path:
            self._save_svg(svg, output_path)

        return svg

    def _pie_slice_path(self, cx: float, cy: float, r: float, start_angle: float, end_angle: float) -> str:
        """Calculate SVG path for pie slice."""
        import math

        start_rad = math.radians(start_angle)
        end_rad = math.radians(end_angle)

        x1 = cx + r * math.cos(start_rad)
        y1 = cy + r * math.sin(start_rad)
        x2 = cx + r * math.cos(end_rad)
        y2 = cy + r * math.sin(end_rad)

        large_arc = 1 if (end_angle - start_angle) > 180 else 0

        return f"M {cx} {cy} L {x1} {y1} A {r} {r} 0 {large_arc} 1 {x2} {y2} Z"

    def generate_architecture_diagram(
        self,
        components: dict,
        title: str,
        description: str = "",
        output_path: Optional[Path] = None
    ) -> str:
        """
        Generate an architecture diagram showing components and connections.

        Args:
            components: Dict with 'boxes' and 'connections' lists
            title: Diagram title
            description: Optional caption
            output_path: Optional path to save SVG

        Returns:
            SVG string
        """
        boxes = components.get("boxes", [])
        connections = components.get("connections", [])

        if not boxes:
            return ""

        # Larger canvas for architecture diagrams
        width = 900
        height = 600

        svg_parts = [
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}">',
            f'<rect width="{width}" height="{height}" fill="{BACKGROUND_COLOR}"/>',
            # Title
            f'<text x="{width/2}" y="35" text-anchor="middle" font-family="{self.font_family}" font-size="22" font-weight="bold" fill="{TEXT_COLOR}">{self._escape(title)}</text>',
        ]

        # Add description if provided
        if description:
            svg_parts.append(
                f'<text x="{width/2}" y="55" text-anchor="middle" font-family="{self.font_family}" font-size="12" fill="{MUTED_COLOR}">{self._escape(description)}</text>'
            )

        # Calculate box positions in a grid-like layout
        box_positions = {}
        num_boxes = len(boxes)
        cols = min(3, num_boxes)
        rows = (num_boxes + cols - 1) // cols

        box_width = 180
        box_height = 80
        h_spacing = (width - cols * box_width) / (cols + 1)
        v_spacing = (height - 80 - rows * box_height) / (rows + 1)

        start_y = 80

        for i, box in enumerate(boxes):
            row = i // cols
            col = i % cols

            x = h_spacing + col * (box_width + h_spacing)
            y = start_y + v_spacing + row * (box_height + v_spacing)

            box_id = box.get("id", f"box_{i}")
            box_positions[box_id] = {
                "x": x,
                "y": y,
                "cx": x + box_width / 2,
                "cy": y + box_height / 2,
                "width": box_width,
                "height": box_height
            }

            label = box.get("label", f"Component {i+1}")
            desc = box.get("description", "")
            color = CHART_COLORS[i % len(CHART_COLORS)]

            # Box with shadow effect
            svg_parts.append(
                f'<rect x="{x+3}" y="{y+3}" width="{box_width}" height="{box_height}" fill="#E0E0E0" rx="8" ry="8"/>'
            )
            svg_parts.append(
                f'<rect x="{x}" y="{y}" width="{box_width}" height="{box_height}" fill="{color}" rx="8" ry="8"/>'
            )

            # Label
            svg_parts.append(
                f'<text x="{x + box_width/2}" y="{y + 30}" text-anchor="middle" font-family="{self.font_family}" font-size="14" font-weight="bold" fill="white">{self._escape(label)}</text>'
            )

            # Description
            if desc:
                wrapped_desc = desc[:25] + "..." if len(desc) > 25 else desc
                svg_parts.append(
                    f'<text x="{x + box_width/2}" y="{y + 50}" text-anchor="middle" font-family="{self.font_family}" font-size="11" fill="rgba(255,255,255,0.9)">{self._escape(wrapped_desc)}</text>'
                )

        # Draw connections with arrows
        for conn in connections:
            from_id = conn.get("from", "")
            to_id = conn.get("to", "")
            conn_label = conn.get("label", "")

            if from_id in box_positions and to_id in box_positions:
                from_pos = box_positions[from_id]
                to_pos = box_positions[to_id]

                # Calculate connection points
                x1, y1 = from_pos["cx"], from_pos["cy"]
                x2, y2 = to_pos["cx"], to_pos["cy"]

                # Adjust to box edges
                if abs(x2 - x1) > abs(y2 - y1):
                    # Horizontal connection
                    if x2 > x1:
                        x1 = from_pos["x"] + from_pos["width"]
                        x2 = to_pos["x"]
                    else:
                        x1 = from_pos["x"]
                        x2 = to_pos["x"] + to_pos["width"]
                    y1 = y2 = (from_pos["cy"] + to_pos["cy"]) / 2
                else:
                    # Vertical connection
                    if y2 > y1:
                        y1 = from_pos["y"] + from_pos["height"]
                        y2 = to_pos["y"]
                    else:
                        y1 = from_pos["y"]
                        y2 = to_pos["y"] + to_pos["height"]
                    x1 = x2 = (from_pos["cx"] + to_pos["cx"]) / 2

                # Arrow line
                svg_parts.append(
                    f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{TEXT_COLOR}" stroke-width="2" marker-end="url(#arrowhead)"/>'
                )

                # Connection label
                if conn_label:
                    mid_x = (x1 + x2) / 2
                    mid_y = (y1 + y2) / 2 - 8
                    svg_parts.append(
                        f'<text x="{mid_x}" y="{mid_y}" text-anchor="middle" font-family="{self.font_family}" font-size="10" fill="{MUTED_COLOR}">{self._escape(conn_label)}</text>'
                    )

        # Add arrowhead marker definition
        svg_parts.insert(2, '''<defs>
            <marker id="arrowhead" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
                <polygon points="0 0, 10 3.5, 0 7" fill="#1C1C1C"/>
            </marker>
        </defs>''')

        svg_parts.append('</svg>')
        svg = '\n'.join(svg_parts)

        if output_path:
            self._save_svg(svg, output_path)

        return svg

    def generate_comparison_diagram(
        self,
        components: dict,
        title: str,
        description: str = "",
        output_path: Optional[Path] = None
    ) -> str:
        """
        Generate a comparison diagram showing side-by-side concepts.

        Args:
            components: Dict with 'items' list containing name, features, pros, cons
            title: Diagram title
            description: Optional caption
            output_path: Optional path to save SVG

        Returns:
            SVG string
        """
        items = components.get("items", [])

        if not items:
            return ""

        num_items = min(len(items), 4)
        items = items[:num_items]

        # Calculate dimensions
        width = 900
        item_width = (width - 60) / num_items - 20
        height = 550

        svg_parts = [
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}">',
            f'<rect width="{width}" height="{height}" fill="{BACKGROUND_COLOR}"/>',
            # Title
            f'<text x="{width/2}" y="35" text-anchor="middle" font-family="{self.font_family}" font-size="22" font-weight="bold" fill="{TEXT_COLOR}">{self._escape(title)}</text>',
        ]

        if description:
            svg_parts.append(
                f'<text x="{width/2}" y="55" text-anchor="middle" font-family="{self.font_family}" font-size="12" fill="{MUTED_COLOR}">{self._escape(description)}</text>'
            )

        start_y = 75
        content_height = height - start_y - 20

        for i, item in enumerate(items):
            x = 30 + i * (item_width + 20)
            name = item.get("name", f"Item {i+1}")
            features = item.get("features", [])
            pros = item.get("pros", [])
            cons = item.get("cons", [])
            color = CHART_COLORS[i % len(CHART_COLORS)]

            # Item container
            svg_parts.append(
                f'<rect x="{x}" y="{start_y}" width="{item_width}" height="{content_height}" fill="#F8F9FA" stroke="{color}" stroke-width="3" rx="10" ry="10"/>'
            )

            # Header bar
            svg_parts.append(
                f'<rect x="{x}" y="{start_y}" width="{item_width}" height="45" fill="{color}" rx="10" ry="10"/>'
            )
            svg_parts.append(
                f'<rect x="{x}" y="{start_y + 35}" width="{item_width}" height="15" fill="{color}"/>'
            )

            # Item name
            svg_parts.append(
                f'<text x="{x + item_width/2}" y="{start_y + 28}" text-anchor="middle" font-family="{self.font_family}" font-size="14" font-weight="bold" fill="white">{self._escape(name)}</text>'
            )

            y_offset = start_y + 65

            # Features
            if features:
                svg_parts.append(
                    f'<text x="{x + 12}" y="{y_offset}" font-family="{self.font_family}" font-size="11" font-weight="bold" fill="{TEXT_COLOR}">Features:</text>'
                )
                y_offset += 18
                for feature in features[:5]:
                    wrapped = feature[:30] + "..." if len(feature) > 30 else feature
                    svg_parts.append(
                        f'<text x="{x + 18}" y="{y_offset}" font-family="{self.font_family}" font-size="10" fill="{TEXT_COLOR}">• {self._escape(wrapped)}</text>'
                    )
                    y_offset += 16

            # Pros
            if pros:
                y_offset += 10
                svg_parts.append(
                    f'<text x="{x + 12}" y="{y_offset}" font-family="{self.font_family}" font-size="11" font-weight="bold" fill="#2E7D32">Pros:</text>'
                )
                y_offset += 18
                for pro in pros[:3]:
                    wrapped = pro[:30] + "..." if len(pro) > 30 else pro
                    svg_parts.append(
                        f'<text x="{x + 18}" y="{y_offset}" font-family="{self.font_family}" font-size="10" fill="#2E7D32">+ {self._escape(wrapped)}</text>'
                    )
                    y_offset += 16

            # Cons
            if cons:
                y_offset += 10
                svg_parts.append(
                    f'<text x="{x + 12}" y="{y_offset}" font-family="{self.font_family}" font-size="11" font-weight="bold" fill="#C62828">Cons:</text>'
                )
                y_offset += 18
                for con in cons[:3]:
                    wrapped = con[:30] + "..." if len(con) > 30 else con
                    svg_parts.append(
                        f'<text x="{x + 18}" y="{y_offset}" font-family="{self.font_family}" font-size="10" fill="#C62828">− {self._escape(wrapped)}</text>'
                    )
                    y_offset += 16

        svg_parts.append('</svg>')
        svg = '\n'.join(svg_parts)

        if output_path:
            self._save_svg(svg, output_path)

        return svg

    def generate_flow_diagram(
        self,
        components: dict,
        title: str,
        description: str = "",
        output_path: Optional[Path] = None
    ) -> str:
        """
        Generate a flow diagram showing process steps.

        Args:
            components: Dict with 'steps' and 'arrows' lists
            title: Diagram title
            description: Optional caption
            output_path: Optional path to save SVG

        Returns:
            SVG string
        """
        steps = components.get("steps", [])
        arrows = components.get("arrows", [])

        if not steps:
            return ""

        width = 900
        height = 500
        num_steps = len(steps)

        # Calculate step positions - horizontal layout
        step_width = 140
        step_height = 90
        total_width = num_steps * step_width + (num_steps - 1) * 40
        start_x = (width - total_width) / 2

        svg_parts = [
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}">',
            f'<rect width="{width}" height="{height}" fill="{BACKGROUND_COLOR}"/>',
            # Arrowhead definition
            '''<defs>
                <marker id="flowarrow" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
                    <polygon points="0 0, 10 3.5, 0 7" fill="#1C1C1C"/>
                </marker>
            </defs>''',
            # Title
            f'<text x="{width/2}" y="40" text-anchor="middle" font-family="{self.font_family}" font-size="22" font-weight="bold" fill="{TEXT_COLOR}">{self._escape(title)}</text>',
        ]

        if description:
            svg_parts.append(
                f'<text x="{width/2}" y="60" text-anchor="middle" font-family="{self.font_family}" font-size="12" fill="{MUTED_COLOR}">{self._escape(description)}</text>'
            )

        step_positions = {}
        center_y = height / 2

        for i, step in enumerate(steps):
            x = start_x + i * (step_width + 40)
            y = center_y - step_height / 2

            step_id = step.get("id", f"step_{i}")
            step_positions[step_id] = {
                "x": x,
                "y": y,
                "cx": x + step_width / 2,
                "cy": y + step_height / 2,
                "right": x + step_width,
                "left": x
            }

            label = step.get("label", f"Step {i+1}")
            desc = step.get("description", "")
            color = CHART_COLORS[i % len(CHART_COLORS)]

            # Step number circle
            svg_parts.append(
                f'<circle cx="{x + step_width/2}" cy="{y - 15}" r="18" fill="{color}"/>'
            )
            svg_parts.append(
                f'<text x="{x + step_width/2}" y="{y - 10}" text-anchor="middle" font-family="{self.font_family}" font-size="14" font-weight="bold" fill="white">{i+1}</text>'
            )

            # Step box with rounded corners
            svg_parts.append(
                f'<rect x="{x+2}" y="{y+2}" width="{step_width}" height="{step_height}" fill="#E0E0E0" rx="12" ry="12"/>'
            )
            svg_parts.append(
                f'<rect x="{x}" y="{y}" width="{step_width}" height="{step_height}" fill="white" stroke="{color}" stroke-width="3" rx="12" ry="12"/>'
            )

            # Step label
            svg_parts.append(
                f'<text x="{x + step_width/2}" y="{y + 35}" text-anchor="middle" font-family="{self.font_family}" font-size="13" font-weight="bold" fill="{TEXT_COLOR}">{self._escape(label[:20])}</text>'
            )

            # Step description
            if desc:
                wrapped = desc[:35] + "..." if len(desc) > 35 else desc
                svg_parts.append(
                    f'<text x="{x + step_width/2}" y="{y + 55}" text-anchor="middle" font-family="{self.font_family}" font-size="10" fill="{MUTED_COLOR}">{self._escape(wrapped)}</text>'
                )

        # Draw arrows between steps
        for arrow in arrows:
            from_id = arrow.get("from", "")
            to_id = arrow.get("to", "")
            arrow_label = arrow.get("label", "")

            if from_id in step_positions and to_id in step_positions:
                from_pos = step_positions[from_id]
                to_pos = step_positions[to_id]

                x1 = from_pos["right"]
                x2 = to_pos["left"]
                y1 = y2 = (from_pos["cy"] + to_pos["cy"]) / 2

                # Arrow line
                svg_parts.append(
                    f'<line x1="{x1 + 5}" y1="{y1}" x2="{x2 - 5}" y2="{y2}" stroke="{TEXT_COLOR}" stroke-width="2" marker-end="url(#flowarrow)"/>'
                )

                # Arrow label
                if arrow_label:
                    mid_x = (x1 + x2) / 2
                    svg_parts.append(
                        f'<text x="{mid_x}" y="{y1 - 10}" text-anchor="middle" font-family="{self.font_family}" font-size="9" fill="{MUTED_COLOR}">{self._escape(arrow_label)}</text>'
                    )

        # If no explicit arrows, draw sequential arrows
        if not arrows and num_steps > 1:
            step_ids = [step.get("id", f"step_{i}") for i, step in enumerate(steps)]
            for i in range(len(step_ids) - 1):
                from_pos = step_positions[step_ids[i]]
                to_pos = step_positions[step_ids[i + 1]]

                x1 = from_pos["right"]
                x2 = to_pos["left"]
                y1 = y2 = from_pos["cy"]

                svg_parts.append(
                    f'<line x1="{x1 + 5}" y1="{y1}" x2="{x2 - 5}" y2="{y2}" stroke="{TEXT_COLOR}" stroke-width="2" marker-end="url(#flowarrow)"/>'
                )

        svg_parts.append('</svg>')
        svg = '\n'.join(svg_parts)

        if output_path:
            self._save_svg(svg, output_path)

        return svg

    def _escape(self, text: str) -> str:
        """Escape text for SVG."""
        return (text
                .replace("&", "&amp;")
                .replace("<", "&lt;")
                .replace(">", "&gt;")
                .replace('"', "&quot;"))

    def _save_svg(self, svg: str, path: Path) -> None:
        """Save SVG to file."""
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(svg, encoding="utf-8")
        logger.debug(f"Saved SVG chart: {path}")


def generate_chart(
    chart_type: str,
    data: list[dict],
    title: str,
    output_path: Optional[Path] = None,
    width: int = 800,
    height: int = 500
) -> str:
    """
    Generate chart based on type.

    Args:
        chart_type: "bar", "pie", "line", or "comparison"
        data: List of {label, value} dictionaries
        title: Chart title
        output_path: Optional path to save SVG
        width: Chart width
        height: Chart height

    Returns:
        SVG string
    """
    generator = SVGGenerator(width=width, height=height)

    chart_methods = {
        "bar": generator.generate_bar_chart,
        "pie": generator.generate_pie_chart,
        "line": generator.generate_line_chart,
        "comparison": generator.generate_comparison_chart,
    }

    method = chart_methods.get(chart_type, generator.generate_bar_chart)
    return method(data, title, output_path)


def generate_concept_diagram(
    diagram_type: str,
    components: dict,
    title: str,
    description: str = "",
    output_path: Optional[Path] = None
) -> str:
    """
    Generate concept diagram based on type.

    Args:
        diagram_type: "architecture", "comparison", or "flow"
        components: Diagram components (structure depends on type)
        title: Diagram title
        description: Optional caption
        output_path: Optional path to save SVG

    Returns:
        SVG string
    """
    generator = SVGGenerator()

    diagram_methods = {
        "architecture": generator.generate_architecture_diagram,
        "comparison": generator.generate_comparison_diagram,
        "flow": generator.generate_flow_diagram,
    }

    method = diagram_methods.get(diagram_type)
    if method:
        return method(components, title, description, output_path)

    logger.warning(f"Unknown diagram type: {diagram_type}, using architecture")
    return generator.generate_architecture_diagram(components, title, description, output_path)
