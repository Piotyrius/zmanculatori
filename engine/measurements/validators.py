from __future__ import annotations

from typing import Dict, Iterable, List, Tuple

from .models import RawMeasurementInput, MeasurementProfile
from .units import to_mm, normalize_unit


class MeasurementValidationError(ValueError):
    def __init__(self, errors: List[str]) -> None:
        super().__init__("Invalid measurements")
        self.errors = errors


def validate_and_normalize_measurements(
    raw: RawMeasurementInput,
    required_names: Iterable[str],
    min_max_bounds: Dict[str, Tuple[float, float]] | None = None,
) -> MeasurementProfile:
    """
    Convert raw input into a canonical MeasurementProfile in millimeters,
    enforcing required fields and basic bounds.
    """
    errors: List[str] = []
    values_mm: Dict[str, float] = {}

    for name in required_names:
        if name not in raw.values:
            errors.append(f"Missing required measurement: {name}")

    for name, value in raw.values.items():
        if value <= 0:
            errors.append(f"Measurement {name} must be positive, got {value}")
            continue

        value_mm = to_mm(value, raw.unit)
        if min_max_bounds and name in min_max_bounds:
            min_v, max_v = min_max_bounds[name]
            if not (min_v <= value_mm <= max_v):
                errors.append(
                    f"Measurement {name}={value_mm}mm out of bounds [{min_v}, {max_v}]mm"
                )
                continue
        values_mm[name] = value_mm

    if errors:
        raise MeasurementValidationError(errors)

    return MeasurementProfile(values=values_mm, unit=normalize_unit(raw.unit))













