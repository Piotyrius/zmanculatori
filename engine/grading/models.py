from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional


class GradingMethod(str, Enum):
    """Methods of grading."""
    PROPORTIONAL = "proportional"  # Grade based on proportional ratios
    LINEAR = "linear"  # Linear grade increments
    CUSTOM = "custom"  # Custom grading table


@dataclass(slots=True)
class SizeRange:
    """Size range definition for grading."""
    id: str
    name: str
    sizes: List[str] = field(default_factory=list)  # e.g., ["XS", "S", "M", "L", "XL"]
    base_size: str = "M"  # Base size for grading
    metadata: Dict[str, any] = field(default_factory=dict)


@dataclass(slots=True)
class GradeRule:
    """
    Grade rule for a specific measurement.
    
    Grading must not alter the base pattern logic.
    """
    measurement_name: str
    method: GradingMethod
    
    # For PROPORTIONAL: ratio (e.g., 0.1 = 10% increase per size)
    # For LINEAR: increment (e.g., 2.0 = 2mm increase per size)
    value: float
    
    # Optional: size-specific overrides
    size_overrides: Dict[str, float] = field(default_factory=dict)
    
    # Metadata
    metadata: Dict[str, any] = field(default_factory=dict)


@dataclass(slots=True)
class GradingTable:
    """
    School-specific grading table.
    
    Contains grade rules for all measurements in a size range.
    """
    id: str
    name: str
    version: str
    size_range: SizeRange
    
    # Grade rules by measurement name
    grade_rules: Dict[str, GradeRule] = field(default_factory=dict)
    
    # Link to drafting school if school-specific
    drafting_school_id: Optional[str] = None
    drafting_school_version: Optional[str] = None
    
    # Metadata
    metadata: Dict[str, any] = field(default_factory=dict)
    
    def get_grade_rule(self, measurement_name: str) -> Optional[GradeRule]:
        """Get grade rule for a measurement."""
        return self.grade_rules.get(measurement_name)
    
    def calculate_graded_value(
        self,
        measurement_name: str,
        base_value: float,
        size_offset: int  # Number of sizes from base (positive = larger, negative = smaller)
    ) -> float:
        """Calculate graded value for a measurement at a given size offset."""
        rule = self.get_grade_rule(measurement_name)
        if not rule:
            return base_value
        
        # Check for size-specific override
        if rule.size_overrides:
            size_name = self.size_range.sizes[
                self.size_range.sizes.index(self.size_range.base_size) + size_offset
            ]
            if size_name in rule.size_overrides:
                return base_value + rule.size_overrides[size_name]
        
        # Apply grading method
        if rule.method == GradingMethod.PROPORTIONAL:
            return base_value * (1.0 + rule.value * size_offset)
        elif rule.method == GradingMethod.LINEAR:
            return base_value + (rule.value * size_offset)
        else:
            return base_value



