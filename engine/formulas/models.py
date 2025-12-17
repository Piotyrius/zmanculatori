from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict


@dataclass(slots=True)
class Formula:
    expression: str


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


class FormulaError(ValueError):
    def __init__(self, message: str) -> None:
        super().__init__(message)





