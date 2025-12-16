from __future__ import annotations

from typing import Dict

import svgwrite

from ..geometry.patterns import PatternGeometry
from ..geometry.primitives import LineSegment
from .models import ExportOptions, ExportBundle


def export_svg(geometry: PatternGeometry, options: ExportOptions) -> ExportBundle:
    """
    Minimal SVG exporter for MVP.

    This renders line segments from all pattern pieces. Further primitives
    (splines, arcs, guides, labels) can be added incrementally.
    """
    # Simple layout: compute bounding box and derive canvas size.
    all_x = []
    all_y = []
    for piece in geometry.pieces:
        for line in piece.lines:
            all_x.extend([line.start.x, line.end.x])
            all_y.extend([line.start.y, line.end.y])

    if not all_x or not all_y:
        size = (100, 100)
    else:
        min_x, max_x = min(all_x), max(all_x)
        min_y, max_y = min(all_y), max(all_y)
        width = (max_x - min_x) * options.scale or 100.0
        height = (max_y - min_y) * options.scale or 100.0
        size = (width, height)

    dwg = svgwrite.Drawing(size=size)

    for piece in geometry.pieces:
        for line in piece.lines:
            _draw_line(dwg, line, options)

    svg_bytes = dwg.tostring().encode("utf-8")
    metadata: Dict[str, object] = {
        "units": geometry.units,
        "coordinate_system": geometry.coordinate_system,
        "debug": options.debug,
    }
    return ExportBundle(content=svg_bytes, mime_type="image/svg+xml", metadata=metadata)


def _draw_line(dwg: svgwrite.Drawing, line: LineSegment, options: ExportOptions) -> None:
    dwg.add(
        dwg.line(
            start=(line.start.x * options.scale, line.start.y * options.scale),
            end=(line.end.x * options.scale, line.end.y * options.scale),
            stroke="black" if not line.is_guide else "lightgray",
            stroke_width=1,
        )
    )





