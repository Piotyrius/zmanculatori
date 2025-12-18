from __future__ import annotations

from typing import Iterable

import numpy as np

from .primitives import LineSegment, Point2D


def line_length(line: LineSegment) -> float:
    dx = line.end.x - line.start.x
    dy = line.end.y - line.start.y
    return float(np.hypot(dx, dy))


def translate_point(point: Point2D, dx: float, dy: float) -> Point2D:
    return Point2D(x=point.x + dx, y=point.y + dy, label=point.label)


def translate_points(points: Iterable[Point2D], dx: float, dy: float) -> list[Point2D]:
    return [translate_point(p, dx, dy) for p in points]








