from __future__ import annotations

from typing import Iterable, List

from ..geometry.patterns import PatternGeometry
from .models import TransformStep, TransformType


def apply_transform_pipeline(
    *, geometry: PatternGeometry, transform_pipeline_ids: Iterable[str], debug: bool = False
) -> PatternGeometry:
    """
    Apply one or more transform pipelines to the given geometry.

    For the engine-core scaffolding, this function currently returns the
    geometry unchanged. In a full implementation, the caller would resolve
    each pipeline ID to a list of TransformStep objects and apply them.
    """
    # TODO: integrate with concrete TransformPipeline configs.
    return geometry




