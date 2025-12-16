from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Optional


@dataclass(slots=True)
class RawMeasurementInput:
    """
    Raw measurements as provided by a client.

    Values may be in different units; they must be normalized into a
    MeasurementProfile before use by the drafting engine.
    """

    values: Dict[str, float]
    unit: str = "mm"  # e.g. "mm", "cm", "inch"


@dataclass(slots=True)
class MeasurementProfile:
    """
    Normalized, validated measurements in canonical units (millimeters).
    """

    values: Dict[str, float] = field(default_factory=dict)
    unit: str = "mm"
    source_profile_id: Optional[str] = None  # e.g. anthropometric profile

    def get(self, name: str) -> float:
        try:
            return self.values[name]
        except KeyError as exc:
            raise KeyError(f"Missing required measurement: {name}") from exc


