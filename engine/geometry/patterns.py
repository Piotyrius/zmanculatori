from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional

from .primitives import Arc, ConstructionGuide, LineSegment, Point2D, Spline


@dataclass(slots=True)
class PatternPiece:
    id: str
    name: str
    grain_line: Optional[LineSegment] = None
    seam_allowance_profile_id: Optional[str] = None
    points: List[Point2D] = field(default_factory=list)
    lines: List[LineSegment] = field(default_factory=list)
    arcs: List[Arc] = field(default_factory=list)
    splines: List[Spline] = field(default_factory=list)
    guides: List[ConstructionGuide] = field(default_factory=list)
    metadata: Dict[str, object] = field(default_factory=dict)


@dataclass(slots=True)
class PatternValidationResult:
    is_valid: bool
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)


@dataclass(slots=True)
class PatternGeometry:
    pieces: List[PatternPiece] = field(default_factory=list)
    units: str = "mm"
    coordinate_system: Dict[str, object] = field(
        default_factory=lambda: {
            "origin": [0.0, 0.0],
            "x_axis": [1.0, 0.0],
            "y_axis": [0.0, 1.0],
        }
    )
    validation: Optional[PatternValidationResult] = None
    metadata: Dict[str, object] = field(default_factory=dict)





