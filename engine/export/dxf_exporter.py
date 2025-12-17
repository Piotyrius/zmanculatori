from __future__ import annotations

import math
from typing import Dict

try:
    import ezdxf
    from ezdxf import units
except ImportError:
    ezdxf = None

from ..geometry.patterns import PatternGeometry, PatternPiece
from ..geometry.primitives import LineSegment, Arc, Spline, Point2D
from .models import ExportOptions, ExportBundle


def export_dxf(geometry: PatternGeometry, options: ExportOptions) -> ExportBundle:
    """
    Production-quality DXF exporter using ezdxf.
    
    Creates DXF with proper layers for cutting lines, grain lines, notches, and labels.
    """
    if ezdxf is None:
        raise ImportError("ezdxf is required for DXF export. Install with: pip install ezdxf")
    
    # Create DXF document
    doc = ezdxf.new("R2010")  # Use AutoCAD 2010 format for compatibility
    msp = doc.modelspace()
    
    # Set units
    if geometry.units == "mm":
        doc.units = units.MM
    elif geometry.units == "inches" or geometry.units == "in":
        doc.units = units.IN
    else:
        doc.units = units.MM  # Default to mm
    
    # Create layers
    cutting_layer = doc.layers.add("CUTTING_LINES", color=7)  # White/black
    grain_layer = doc.layers.add("GRAIN_LINES", color=1)  # Red
    notch_layer = doc.layers.add("NOTCHES", color=2)  # Yellow
    label_layer = doc.layers.add("LABELS", color=3)  # Green
    construction_layer = doc.layers.add("CONSTRUCTION", color=8)  # Gray
    
    # Export each pattern piece
    for piece in geometry.pieces:
        # Export cutting lines (lines, arcs, splines)
        for line in piece.lines:
            if not line.is_guide:
                msp.add_line(
                    (line.start.x, line.start.y),
                    (line.end.x, line.end.y),
                    dxfattribs={"layer": cutting_layer.dxf.name}
                )
        
        for arc in piece.arcs:
            # Convert arc to DXF arc
            start_angle_rad = math.radians(arc.start_angle)
            end_angle_rad = math.radians(arc.end_angle)
            msp.add_arc(
                center=(arc.center.x, arc.center.y),
                radius=arc.radius,
                start_angle=math.degrees(start_angle_rad),
                end_angle=math.degrees(end_angle_rad),
                dxfattribs={"layer": cutting_layer.dxf.name}
            )
        
        for spline in piece.splines:
            # Convert spline to DXF spline
            if len(spline.control_points) >= 2:
                points = [(cp.x, cp.y) for cp in spline.control_points]
                # Use fit points for spline
                msp.add_spline(
                    control_points=points,
                    dxfattribs={"layer": cutting_layer.dxf.name}
                )
        
        # Export grain line
        if piece.grain_line:
            msp.add_line(
                (piece.grain_line.start.x, piece.grain_line.start.y),
                (piece.grain_line.end.x, piece.grain_line.end.y),
                dxfattribs={"layer": grain_layer.dxf.name, "linetype": "DASHED"}
            )
            # Add arrow at end of grain line
            _add_arrow_to_line(msp, piece.grain_line, grain_layer.dxf.name)
        
        # Export notches
        if 'notches' in piece.metadata:
            for notch in piece.metadata['notches']:
                if isinstance(notch, dict) and 'location' in notch:
                    location = notch['location']
                    if isinstance(location, Point2D):
                        _add_notch_marker(msp, location, notch_layer.dxf.name)
        
        # Export piece label
        if piece.points:
            center_x = sum(p.x for p in piece.points) / len(piece.points)
            center_y = sum(p.y for p in piece.points) / len(piece.points)
        elif piece.lines:
            first_line = piece.lines[0]
            center_x = (first_line.start.x + first_line.end.x) / 2
            center_y = (first_line.start.y + first_line.end.y) / 2
        else:
            center_x, center_y = 0, 0
        
        label_text = piece.name
        if 'cut_count' in piece.metadata:
            label_text += f" (Cut: {piece.metadata['cut_count']})"
        if 'orientation' in piece.metadata:
            label_text += f" [{piece.metadata['orientation']}]"
        
        msp.add_text(
            label_text,
            dxfattribs={
                "layer": label_layer.dxf.name,
                "height": 5.0,
            }
        ).set_placement((center_x, center_y))
    
    # Save to bytes
    from io import BytesIO
    buffer = BytesIO()
    doc.save(buffer)
    dxf_bytes = buffer.getvalue()
    
    return ExportBundle(
        content=dxf_bytes,
        mime_type="application/dxf",
        metadata={
            "units": geometry.units,
            "format": "dxf",
            "version": "R2010",
        },
    )


def _add_arrow_to_line(msp, line: LineSegment, layer: str) -> None:
    """Add arrow marker at end of line."""
    dx = line.end.x - line.start.x
    dy = line.end.y - line.start.y
    length = math.sqrt(dx * dx + dy * dy)
    if length > 0:
        unit_x = dx / length
        unit_y = dy / length
        arrow_size = 5.0
        arrow_angle = math.radians(30)
        
        # Arrow point 1
        arrow_x1 = line.end.x - arrow_size * (unit_x * math.cos(arrow_angle) - unit_y * math.sin(arrow_angle))
        arrow_y1 = line.end.y - arrow_size * (unit_y * math.cos(arrow_angle) + unit_x * math.sin(arrow_angle))
        
        # Arrow point 2
        arrow_x2 = line.end.x - arrow_size * (unit_x * math.cos(arrow_angle) + unit_y * math.sin(arrow_angle))
        arrow_y2 = line.end.y - arrow_size * (unit_y * math.cos(arrow_angle) - unit_x * math.sin(arrow_angle))
        
        # Draw arrow lines
        msp.add_line(
            (line.end.x, line.end.y),
            (arrow_x1, arrow_y1),
            dxfattribs={"layer": layer}
        )
        msp.add_line(
            (line.end.x, line.end.y),
            (arrow_x2, arrow_y2),
            dxfattribs={"layer": layer}
        )


def _add_notch_marker(msp, location: Point2D, layer: str) -> None:
    """Add notch marker at location."""
    notch_size = 3.0
    # Draw small triangle
    points = [
        (location.x, location.y - notch_size),
        (location.x - notch_size, location.y),
        (location.x + notch_size, location.y),
        (location.x, location.y - notch_size),  # Close triangle
    ]
    msp.add_lwpolyline(
        points,
        close=True,
        dxfattribs={"layer": layer}
    )

