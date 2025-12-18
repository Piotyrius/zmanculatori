from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional


@dataclass(slots=True)
class Point2D:
    x: float
    y: float
    label: Optional[str] = None


@dataclass(slots=True)
class LineSegment:
    start: Point2D
    end: Point2D
    is_guide: bool = False


@dataclass(slots=True)
class Arc:
    center: Point2D
    radius: float
    start_angle: float
    end_angle: float


@dataclass(slots=True)
class Spline:
    control_points: List[Point2D]


@dataclass(slots=True)
class ConstructionGuide:
    """
    Tagged construction-only geometry that may be optionally exported
    in debug views but not intended for cutting lines.
    """

    primitive: LineSegment | Arc | Spline










