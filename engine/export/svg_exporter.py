from __future__ import annotations

from typing import Dict

import svgwrite

from ..geometry.patterns import PatternGeometry, PatternPiece
from ..geometry.primitives import LineSegment, Arc, Spline, Point2D
from .models import ExportOptions, ExportBundle
import math


def export_svg(geometry: PatternGeometry, options: ExportOptions) -> ExportBundle:
    """
    Professional SVG exporter for MVP.

    Renders all pattern elements: lines, arcs, splines, grain lines, labels, and notches.
    """
    scale = options.scale or 1.0
    
    # Compute bounding box including all primitives
    all_x = []
    all_y = []
    for piece in geometry.pieces:
        for line in piece.lines:
            all_x.extend([line.start.x, line.end.x])
            all_y.extend([line.start.y, line.end.y])
        for arc in piece.arcs:
            # Approximate arc bounding box
            all_x.append(arc.center.x - arc.radius)
            all_x.append(arc.center.x + arc.radius)
            all_y.append(arc.center.y - arc.radius)
            all_y.append(arc.center.y + arc.radius)
        for spline in piece.splines:
            for cp in spline.control_points:
                all_x.append(cp.x)
                all_y.append(cp.y)
        if piece.grain_line:
            all_x.extend([piece.grain_line.start.x, piece.grain_line.end.x])
            all_y.extend([piece.grain_line.start.y, piece.grain_line.end.y])

    if not all_x or not all_y:
        size = (100, 100)
        viewbox = "0 0 100 100"
        min_x, min_y = 0, 0
    else:
        min_x, max_x = min(all_x), max(all_x)
        min_y, max_y = min(all_y), max(all_y)
        # Add padding
        padding = 20
        width = (max_x - min_x + 2 * padding) * scale
        height = (max_y - min_y + 2 * padding) * scale
        size = (width, height)
        viewbox = f"{min_x - padding} {min_y - padding} {max_x - min_x + 2 * padding} {max_y - min_y + 2 * padding}"

    dwg = svgwrite.Drawing(size=size, viewBox=viewbox)

    # Render each pattern piece
    for piece in geometry.pieces:
        # Create a group for each piece
        piece_group = dwg.g(id=f"piece-{piece.id}")
        
        # Render cutting lines (lines, arcs, splines)
        for line in piece.lines:
            if not line.is_guide:
                _draw_line(dwg, piece_group, line, scale)
        
        for arc in piece.arcs:
            _draw_arc(dwg, piece_group, arc, scale)
        
        for spline in piece.splines:
            _draw_spline(dwg, piece_group, spline, scale)
        
        # Render grain line (dashed with arrow)
        if piece.grain_line:
            _draw_grain_line(dwg, piece_group, piece.grain_line, scale)
        
        # Render notches
        if 'notches' in piece.metadata:
            for notch in piece.metadata['notches']:
                if isinstance(notch, dict) and 'location' in notch:
                    location = notch['location']
                    if isinstance(location, Point2D):
                        _draw_notch(dwg, piece_group, location, scale)
        
        # Render piece label
        _draw_piece_label(dwg, piece_group, piece, scale, min_x, min_y)
        
        dwg.add(piece_group)

    svg_bytes = dwg.tostring().encode("utf-8")
    metadata: Dict[str, object] = {
        "units": geometry.units,
        "coordinate_system": geometry.coordinate_system,
        "debug": options.debug,
    }
    return ExportBundle(content=svg_bytes, mime_type="image/svg+xml", metadata=metadata)


def _draw_line(dwg: svgwrite.Drawing, group: svgwrite.container.Group, line: LineSegment, scale: float) -> None:
    """Draw a line segment."""
    group.add(
        dwg.line(
            start=(line.start.x, line.start.y),
            end=(line.end.x, line.end.y),
            stroke="black" if not line.is_guide else "lightgray",
            stroke_width=1,
        )
    )


def _draw_arc(dwg: svgwrite.Drawing, group: svgwrite.container.Group, arc: Arc, scale: float) -> None:
    """Draw an arc as SVG path."""
    # Convert arc to SVG arc path
    start_x = arc.center.x + arc.radius * math.cos(math.radians(arc.start_angle))
    start_y = arc.center.y + arc.radius * math.sin(math.radians(arc.start_angle))
    end_x = arc.center.x + arc.radius * math.cos(math.radians(arc.end_angle))
    end_y = arc.center.y + arc.radius * math.sin(math.radians(arc.end_angle))
    
    # Determine if arc is large (sweep > 180 degrees)
    sweep_angle = arc.end_angle - arc.start_angle
    if sweep_angle < 0:
        sweep_angle += 360
    large_arc = 1 if sweep_angle > 180 else 0
    
    path_data = f"M {start_x} {start_y} A {arc.radius} {arc.radius} 0 {large_arc} 1 {end_x} {end_y}"
    group.add(
        dwg.path(
            d=path_data,
            stroke="black",
            stroke_width=1,
            fill="none",
        )
    )


def _draw_spline(dwg: svgwrite.Drawing, group: svgwrite.container.Group, spline: Spline, scale: float) -> None:
    """Draw a spline as SVG path with Bezier curves."""
    if len(spline.control_points) < 2:
        return
    
    # For cubic Bezier, need 4 points per segment
    # For quadratic Bezier, need 3 points per segment
    # For simplicity, use quadratic Bezier with control points
    path_parts = [f"M {spline.control_points[0].x} {spline.control_points[0].y}"]
    
    if len(spline.control_points) == 2:
        # Simple line
        path_parts.append(f"L {spline.control_points[1].x} {spline.control_points[1].y}")
    elif len(spline.control_points) == 3:
        # Quadratic Bezier
        path_parts.append(
            f"Q {spline.control_points[1].x} {spline.control_points[1].y} "
            f"{spline.control_points[2].x} {spline.control_points[2].y}"
        )
    else:
        # Multiple quadratic Bezier segments
        for i in range(1, len(spline.control_points) - 1):
            if i == 1:
                path_parts.append(
                    f"Q {spline.control_points[i].x} {spline.control_points[i].y} "
                    f"{spline.control_points[i + 1].x} {spline.control_points[i + 1].y}"
                )
            else:
                # Use previous point as control for smooth curve
                path_parts.append(
                    f"T {spline.control_points[i + 1].x} {spline.control_points[i + 1].y}"
                )
    
    group.add(
        dwg.path(
            d=" ".join(path_parts),
            stroke="black",
            stroke_width=1,
            fill="none",
        )
    )


def _draw_grain_line(dwg: svgwrite.Drawing, group: svgwrite.container.Group, grain_line: LineSegment, scale: float) -> None:
    """Draw grain line with dashed style and arrow."""
    # Draw dashed line
    group.add(
        dwg.line(
            start=(grain_line.start.x, grain_line.start.y),
            end=(grain_line.end.x, grain_line.end.y),
            stroke="blue",
            stroke_width=0.5,
            stroke_dasharray="5,5",
        )
    )
    
    # Draw arrow at end
    dx = grain_line.end.x - grain_line.start.x
    dy = grain_line.end.y - grain_line.start.y
    length = math.sqrt(dx * dx + dy * dy)
    if length > 0:
        # Arrow direction
        unit_x = dx / length
        unit_y = dy / length
        
        # Arrow size
        arrow_size = 5
        arrow_angle = math.radians(30)
        
        # Arrow points
        arrow_x1 = grain_line.end.x - arrow_size * (unit_x * math.cos(arrow_angle) - unit_y * math.sin(arrow_angle))
        arrow_y1 = grain_line.end.y - arrow_size * (unit_y * math.cos(arrow_angle) + unit_x * math.sin(arrow_angle))
        arrow_x2 = grain_line.end.x - arrow_size * (unit_x * math.cos(arrow_angle) + unit_y * math.sin(arrow_angle))
        arrow_y2 = grain_line.end.y - arrow_size * (unit_y * math.cos(arrow_angle) - unit_x * math.sin(arrow_angle))
        
        # Draw arrow
        arrow_path = f"M {grain_line.end.x} {grain_line.end.y} L {arrow_x1} {arrow_y1} M {grain_line.end.x} {grain_line.end.y} L {arrow_x2} {arrow_y2}"
        group.add(
            dwg.path(
                d=arrow_path,
                stroke="blue",
                stroke_width=0.5,
                fill="none",
            )
        )


def _draw_notch(dwg: svgwrite.Drawing, group: svgwrite.container.Group, location: Point2D, scale: float) -> None:
    """Draw a notch marker."""
    notch_size = 3
    # Draw small triangle notch
    notch_path = (
        f"M {location.x} {location.y - notch_size} "
        f"L {location.x - notch_size} {location.y} "
        f"L {location.x + notch_size} {location.y} Z"
    )
    group.add(
        dwg.path(
            d=notch_path,
            stroke="black",
            stroke_width=0.5,
            fill="black",
        )
    )


def _draw_piece_label(dwg: svgwrite.Drawing, group: svgwrite.container.Group, piece: PatternPiece, scale: float, min_x: float, min_y: float) -> None:
    """Draw piece label and metadata."""
    # Find center of piece for label placement
    if piece.points:
        center_x = sum(p.x for p in piece.points) / len(piece.points)
        center_y = sum(p.y for p in piece.points) / len(piece.points)
    elif piece.lines:
        # Use first line's midpoint
        first_line = piece.lines[0]
        center_x = (first_line.start.x + first_line.end.x) / 2
        center_y = (first_line.start.y + first_line.end.y) / 2
    else:
        center_x = min_x + 50
        center_y = min_y + 50
    
    # Build label text
    label_parts = [piece.name]
    if 'cut_count' in piece.metadata:
        label_parts.append(f"Cut: {piece.metadata['cut_count']}")
    if 'orientation' in piece.metadata:
        label_parts.append(f"({piece.metadata['orientation']})")
    
    label_text = "\n".join(label_parts)
    
    # Draw label background
    group.add(
        dwg.rect(
            insert=(center_x - 30, center_y - 15),
            size=(60, 30),
            fill="white",
            stroke="black",
            stroke_width=0.5,
            opacity=0.8,
        )
    )
    
    # Draw label text
    group.add(
        dwg.text(
            label_text,
            insert=(center_x, center_y),
            text_anchor="middle",
            dominant_baseline="middle",
            font_size="10px",
            font_family="Arial, sans-serif",
            fill="black",
        )
    )







