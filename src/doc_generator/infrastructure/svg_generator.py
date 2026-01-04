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
