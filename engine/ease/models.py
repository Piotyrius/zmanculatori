from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, Optional


class EaseCategory(str, Enum):
    """Categories of ease as defined in the domain specification."""
    WEARING = "wearing"  # Basic comfort ease
    DESIGN = "design"  # Style-specific ease
    FUNCTIONAL = "functional"  # Movement and function ease
    PRODUCTION = "production"  # Manufacturing tolerance ease


class FitProfile(str, Enum):
    """Fit profiles as defined in the domain specification."""
    CLOSE = "close"
    REGULAR = "regular"
    LOOSE = "loose"
    OVERSIZED = "oversized"
    CUSTOM = "custom"


@dataclass(slots=True)
class EaseProfile:
    """
    Ease profile defining ease values for different measurements.
    
    Ease must be applied parametrically, not destructively.
    """
    id: str
    name: str
    version: str
    fit_profile: FitProfile
    
    # Ease values by measurement name and category
    # Structure: {measurement_name: {ease_category: value}}
    ease_values: Dict[str, Dict[EaseCategory, float]] = field(default_factory=dict)
    
    # Link to drafting school if school-specific
    drafting_school_id: Optional[str] = None
    drafting_school_version: Optional[str] = None
    
    # Metadata
    metadata: Dict[str, any] = field(default_factory=dict)
    
    def get_ease(
        self,
        measurement_name: str,
        category: EaseCategory,
        default: float = 0.0
    ) -> float:
        """Get ease value for a measurement and category."""
        return (
            self.ease_values
            .get(measurement_name, {})
            .get(category, default)
        )
    
    def get_total_ease(self, measurement_name: str) -> float:
        """Get total ease (sum of all categories) for a measurement."""
        measurement_ease = self.ease_values.get(measurement_name, {})
        return sum(measurement_ease.values())



