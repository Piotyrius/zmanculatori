from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Dict


class TransformType(str, Enum):
    EASE = "EASE"
    DART = "DART"
    STYLE = "STYLE"
    SEAM_ALLOWANCE = "SEAM_ALLOWANCE"
    GRADING = "GRADING"


@dataclass(slots=True)
class TransformStep:
    id: str
    type: TransformType
    params: Dict[str, object]





