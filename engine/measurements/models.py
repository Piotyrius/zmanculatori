from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Set


class MeasurementCategory(str, Enum):
    """Measurement categories as defined in the domain specification."""
    # Core Girth Measurements
    CORE_GIRTH = "core_girth"
    # Vertical Measurements
    VERTICAL = "vertical"
    # Width and Depth Measurements
    WIDTH_DEPTH = "width_depth"
    # Sleeve Measurements
    SLEEVE = "sleeve"
    # Leg Measurements
    LEG = "leg"
    # Optional / Advanced
    OPTIONAL = "optional"


# Measurement definitions by category
MEASUREMENT_CATEGORIES: Dict[str, MeasurementCategory] = {
    # Core Girth Measurements (A)
    "bust": MeasurementCategory.CORE_GIRTH,
    "chest": MeasurementCategory.CORE_GIRTH,
    "waist": MeasurementCategory.CORE_GIRTH,
    "hip": MeasurementCategory.CORE_GIRTH,
    "high_hip": MeasurementCategory.CORE_GIRTH,
    "underbust": MeasurementCategory.CORE_GIRTH,
    "neck_circumference": MeasurementCategory.CORE_GIRTH,
    # Vertical Measurements (B)
    "body_height": MeasurementCategory.VERTICAL,
    "back_length": MeasurementCategory.VERTICAL,
    "front_length": MeasurementCategory.VERTICAL,
    "waist_to_hip": MeasurementCategory.VERTICAL,
    "shoulder_to_waist": MeasurementCategory.VERTICAL,
    "rise": MeasurementCategory.VERTICAL,
    "crotch_depth": MeasurementCategory.VERTICAL,
    # Width and Depth Measurements (C)
    "shoulder_width": MeasurementCategory.WIDTH_DEPTH,
    "back_width": MeasurementCategory.WIDTH_DEPTH,
    "front_width": MeasurementCategory.WIDTH_DEPTH,
    "armhole_depth": MeasurementCategory.WIDTH_DEPTH,
    "chest_depth": MeasurementCategory.WIDTH_DEPTH,
    # Sleeve Measurements (D)
    "arm_length": MeasurementCategory.SLEEVE,
    "upper_arm_circumference": MeasurementCategory.SLEEVE,
    "elbow_circumference": MeasurementCategory.SLEEVE,
    "wrist_circumference": MeasurementCategory.SLEEVE,
    "armhole_circumference": MeasurementCategory.SLEEVE,
    # Leg Measurements (E)
    "inseam": MeasurementCategory.LEG,
    "outseam": MeasurementCategory.LEG,
    "thigh": MeasurementCategory.LEG,
    "knee": MeasurementCategory.LEG,
    "calf": MeasurementCategory.LEG,
    "ankle": MeasurementCategory.LEG,
    # Optional / Advanced (F)
    "bust_point_distance": MeasurementCategory.OPTIONAL,
    "bust_point_height": MeasurementCategory.OPTIONAL,
    "shoulder_slope": MeasurementCategory.OPTIONAL,
    "neck_depth": MeasurementCategory.OPTIONAL,
}


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
    Extended with category support and validation.
    """

    values: Dict[str, float] = field(default_factory=dict)
    unit: str = "mm"
    source_profile_id: Optional[str] = None  # e.g. anthropometric profile

    def get(self, name: str) -> float:
        try:
            return self.values[name]
        except KeyError as exc:
            raise KeyError(f"Missing required measurement: {name}") from exc

    def get_category(self, name: str) -> Optional[MeasurementCategory]:
        """Get the category for a measurement name."""
        return MEASUREMENT_CATEGORIES.get(name)

    def get_measurements_by_category(self, category: MeasurementCategory) -> Dict[str, float]:
        """Get all measurements in a specific category."""
        return {
            name: value
            for name, value in self.values.items()
            if self.get_category(name) == category
        }

    def validate_required(self, required: List[str]) -> List[str]:
        """
        Validate that all required measurements are present.
        Returns list of missing measurement names.
        """
        missing = []
        for name in required:
            if name not in self.values:
                missing.append(name)
        return missing

    def has_category(self, category: MeasurementCategory) -> bool:
        """Check if profile has any measurements in the given category."""
        return any(
            self.get_category(name) == category
            for name in self.values.keys()
        )






