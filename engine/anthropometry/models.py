from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Optional


@dataclass(slots=True)
class AnthropometricProfile:
    """
    Describes a body profile category (e.g. adult, child, petite, plus),
    with typical base measurements and optional metadata.
    """

    id: str
    name: str
    category: str
    base_measurements_mm: Dict[str, float] = field(default_factory=dict)
    metadata: Dict[str, str] = field(default_factory=dict)


@dataclass(slots=True)
class SizeProfile:
    """
    Named size profile (e.g. 36, S, M, L) referencing an anthropometric profile.
    """

    id: str
    name: str
    anthropometric_profile_id: str
    base_measurements_mm: Dict[str, float] = field(default_factory=dict)
    metadata: Dict[str, str] = field(default_factory=dict)






