from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, Optional


class FormulaType(str, Enum):
    """Types of formulas as defined in the domain specification."""
    PROPORTIONAL = "proportional"  # Based on body measurement ratios
    FIXED_ALLOWANCE = "fixed_allowance"  # Measurement + constant
    CONDITIONAL = "conditional"  # Depend on thresholds
    DERIVED = "derived"  # Calculated values not directly measured
    SCHOOL_SPECIFIC = "school_specific"  # Same block, different logic by school


@dataclass(slots=True)
class Formula:
    """
    A formula expression with type and metadata.
    """
    expression: str
    formula_type: FormulaType = FormulaType.PROPORTIONAL
    version: str = "1.0"
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    # For conditional formulas
    condition: Optional[str] = None  # Expression that must be true for formula to apply
    threshold: Optional[float] = None  # Threshold value for conditional evaluation
    
    # For derived measurements
    output_name: Optional[str] = None  # Name of the derived measurement


@dataclass(slots=True)
class FormulaContext:
    """
    Evaluation context for formulas.

    Typically includes:
    - measurement values
    - intermediate rule results
    - configuration parameters (ratios, ease, constants)
    """

    variables: Dict[str, float]
    
    def get(self, name: str, default: Optional[float] = None) -> float:
        """Get a variable value with optional default."""
        if default is not None:
            return self.variables.get(name, default)
        return self.variables[name]


class FormulaError(ValueError):
    def __init__(self, message: str) -> None:
        super().__init__(message)





