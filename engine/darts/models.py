from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional


class DartType(str, Enum):
    """Types of darts as defined in the domain specification."""
    WAIST = "waist"
    BUST = "bust"
    SHOULDER = "shoulder"
    FRENCH = "french"


class DartOperation(str, Enum):
    """Dart operations as defined in the domain specification."""
    ROTATE = "rotate"  # Rotate dart to different location
    SPLIT = "split"  # Split dart into multiple darts
    ELIMINATE = "eliminate"  # Remove dart (e.g., through design ease)


@dataclass(slots=True)
class DartTransform:
    """
    A dart transformation operation.
    
    Shaping operations must be reversible and rule-based.
    """
    id: str
    dart_type: DartType
    operation: DartOperation
    
    # Operation parameters
    # For ROTATE: target_location (point name or coordinates)
    # For SPLIT: split_count (number of darts), split_positions (list of positions)
    # For ELIMINATE: elimination_method (e.g., "ease", "gather", "pleat")
    params: Dict[str, any] = field(default_factory=dict)
    
    # Reversibility metadata
    is_reversible: bool = True
    reverse_params: Optional[Dict[str, any]] = None
    
    # Metadata
    metadata: Dict[str, any] = field(default_factory=dict)

