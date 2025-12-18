from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional


class DraftingSchoolCategory(str, Enum):
    """Categories of drafting schools as defined in the domain specification."""
    METRIC_PATTERN_CUTTING = "metric_pattern_cutting"
    ANGLO_AMERICAN = "anglo_american"
    FLAT_PATTERN_INDUSTRIAL = "flat_pattern_industrial"
    TAILORING_BASED = "tailoring_based"
    EDUCATIONAL_HYBRID = "educational_hybrid"


@dataclass(slots=True)
class MeasurementRequirements:
    """Measurement requirements for a drafting school."""
    required: List[str] = field(default_factory=list)
    optional: List[str] = field(default_factory=list)


@dataclass(slots=True)
class EasePhilosophy:
    """Default ease values for a drafting school."""
    values: Dict[str, Dict[str, float]] = field(default_factory=dict)
    # Structure: {measurement_name: {ease_type: value}}
    # ease_type can be: "wearing", "design", "functional", "production"


@dataclass(slots=True)
class DraftingConventions:
    """School-specific drafting conventions and rules."""
    conventions: Dict[str, any] = field(default_factory=dict)
    # Examples: {"shoulder_slope_method": "proportional", "dart_distribution": "equal"}


@dataclass(slots=True)
class DraftingSchoolConfig:
    """
    Configuration for a drafting school system.
    
    Each school consists of:
    - measurement requirements
    - proportional logic
    - base block definitions
    - ease philosophy
    - drafting conventions
    """
    id: str
    name: str
    version: str
    category: DraftingSchoolCategory
    description: Optional[str] = None
    
    # Measurement requirements for this school
    measurement_requirements: MeasurementRequirements = field(
        default_factory=MeasurementRequirements
    )
    
    # Proportional logic formulas (measurement_name -> formula_expression)
    proportional_logic: Dict[str, str] = field(default_factory=dict)
    
    # Base block definitions (block_type -> block_id)
    base_block_definitions: Dict[str, str] = field(default_factory=dict)
    
    # Default ease philosophy
    ease_philosophy: EasePhilosophy = field(default_factory=EasePhilosophy)
    
    # School-specific drafting conventions
    drafting_conventions: DraftingConventions = field(
        default_factory=DraftingConventions
    )
    
    # Metadata for extensibility
    metadata: Dict[str, any] = field(default_factory=dict)


