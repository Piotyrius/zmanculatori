from __future__ import annotations

from typing import Final


CANONICAL_UNIT: Final[str] = "mm"

_UNIT_FACTORS_TO_MM = {
    "mm": 1.0,
    "millimeter": 1.0,
    "millimeters": 1.0,
    "cm": 10.0,
    "centimeter": 10.0,
    "centimeters": 10.0,
    "in": 25.4,
    "inch": 25.4,
    "inches": 25.4,
}


def to_mm(value: float, unit: str) -> float:
    try:
        factor = _UNIT_FACTORS_TO_MM[unit.lower()]
    except KeyError as exc:
        raise ValueError(f"Unsupported measurement unit: {unit}") from exc
    return value * factor


def normalize_unit(unit: str) -> str:
    if unit.lower() not in _UNIT_FACTORS_TO_MM:
        raise ValueError(f"Unsupported measurement unit: {unit}")
    return CANONICAL_UNIT






