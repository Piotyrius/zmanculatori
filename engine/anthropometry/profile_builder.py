from __future__ import annotations

from typing import Dict

from ..measurements.models import MeasurementProfile
from .models import AnthropometricProfile, SizeProfile


def build_measurement_profile_from_size(
    anthropometric_profile: AnthropometricProfile,
    size_profile: SizeProfile,
    overrides: MeasurementProfile | None = None,
) -> MeasurementProfile:
    """
    Combine an anthropometric profile, a size profile, and optional overrides
    into a concrete MeasurementProfile in canonical units (mm).
    """
    values: Dict[str, float] = {}
    values.update(anthropometric_profile.base_measurements_mm)
    values.update(size_profile.base_measurements_mm)

    if overrides:
        values.update(overrides.values)

    return MeasurementProfile(values=values, unit="mm", source_profile_id=size_profile.id)












