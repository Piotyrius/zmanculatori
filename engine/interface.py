from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from .measurements.models import MeasurementProfile
from .geometry.patterns import PatternGeometry
from .export.models import ExportOptions, ExportBundle
from .blocks.builder import build_block_pattern
from .transforms.pipeline import apply_transform_pipeline
from .validators.pattern_validator import validate_pattern_geometry


@dataclass(slots=True)
class PatternRequest:
    """
    High-level, engine-facing request for pattern generation.

    All IDs refer to immutable, versioned configuration objects that must
    be resolved before invoking the engine in a real application.
    The engine itself remains agnostic of persistence and subscription logic.
    """

    measurement_profile: MeasurementProfile

    garment_type: str
    fit: str
    category: str

    drafting_school_id: str
    drafting_school_version: str
    block_id: str
    block_version: str
    rule_graph_id: str
    rule_graph_version: str

    size_profile_id: Optional[str] = None
    ease_profile_id: Optional[str] = None
    transform_pipeline_ids: List[str] = field(default_factory=list)

    debug: bool = False
    engine_api_version: str = "1.0"

    # Arbitrary metadata for callers; ignored by core logic
    metadata: Dict[str, Any] = field(default_factory=dict)


def generate_pattern(request: PatternRequest) -> PatternGeometry:
    """
    Generate a pattern geometry for the given request.

    The caller is responsible for resolving configuration IDs into concrete
    DraftingSchoolConfig, BlockDefinition, RuleGraphConfig, TransformPipelines,
    etc. For now, this function operates on IDs only and assumes that the
    block builder and transform pipeline resolve them through pure callables.
    """
    # Build base block (stitching line geometry)
    geometry = build_block_pattern(
        measurement_profile=request.measurement_profile,
        drafting_school_id=request.drafting_school_id,
        drafting_school_version=request.drafting_school_version,
        block_id=request.block_id,
        block_version=request.block_version,
        rule_graph_id=request.rule_graph_id,
        rule_graph_version=request.rule_graph_version,
        metadata={
            "garment_type": request.garment_type,
            "fit": request.fit,
            "category": request.category,
            "engine_api_version": request.engine_api_version,
        },
    )

    # Apply transforms (ease, darts, style, grading, seam allowance, etc.)
    if request.transform_pipeline_ids:
        geometry = apply_transform_pipeline(
            geometry=geometry,
            transform_pipeline_ids=request.transform_pipeline_ids,
            debug=request.debug,
        )

    # Validate final geometry and attach validation metadata
    validation_result = validate_pattern_geometry(geometry)
    geometry.validation = validation_result  # type: ignore[attr-defined]

    return geometry


def export_pattern(geometry: PatternGeometry, options: ExportOptions) -> ExportBundle:
    """
    Export the given pattern geometry according to the provided options.
    """
    from .export.svg_exporter import export_svg
    from .export.dxf_exporter import export_dxf
    from .export.pdf_exporter import export_pdf

    format_lower = options.format.lower()
    if format_lower == "svg":
        return export_svg(geometry, options)
    elif format_lower == "dxf":
        return export_dxf(geometry, options)
    elif format_lower == "pdf":
        return export_pdf(geometry, options)
    else:
        raise ValueError(f"Unsupported export format: {options.format}")


__all__ = [
    "PatternRequest",
    "PatternGeometry",
    "ExportOptions",
    "ExportBundle",
    "generate_pattern",
    "export_pattern",
]




