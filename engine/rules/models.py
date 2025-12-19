from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional

from ..formulas.models import Formula


class RuleType(str, Enum):
    COMPUTE_VALUE = "COMPUTE_VALUE"
    CONSTRUCT_POINT = "CONSTRUCT_POINT"
    CONSTRUCT_LINE = "CONSTRUCT_LINE"
    CONSTRUCT_ARC = "CONSTRUCT_ARC"
    CONSTRUCT_SPLINE = "CONSTRUCT_SPLINE"
    CONSTRUCT_GRAIN_LINE = "CONSTRUCT_GRAIN_LINE"
    CONSTRUCT_DART = "CONSTRUCT_DART"
    CONSTRUCT_NOTCH = "CONSTRUCT_NOTCH"
    CONSTRUCT_PIECE_BOUNDARY = "CONSTRUCT_PIECE_BOUNDARY"
    SET_PIECE_METADATA = "SET_PIECE_METADATA"
    APPLY_TRANSFORM = "APPLY_TRANSFORM"


@dataclass(slots=True)
class RuleNode:
    id: str
    type: RuleType
    inputs: List[str] = field(default_factory=list)
    outputs: List[str] = field(default_factory=list)
    params: Dict[str, object] = field(default_factory=dict)
    formula: Optional[Formula] = None


@dataclass(slots=True)
class RuleGraphConfig:
    id: str
    version: str
    nodes: List[RuleNode]







