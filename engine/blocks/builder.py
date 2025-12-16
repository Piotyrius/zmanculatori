from __future__ import annotations

from typing import Dict, Any

from ..geometry.patterns import PatternGeometry
from ..measurements.models import MeasurementProfile
from ..rules.executor import execute_rule_graph
from ..rules.models import RuleGraphConfig


def build_block_pattern(
    *,
    measurement_profile: MeasurementProfile,
    drafting_school_id: str,
    drafting_school_version: str,
    block_id: str,
    block_version: str,
    rule_graph_id: str,
    rule_graph_version: str,
    metadata: Dict[str, Any] | None = None,
) -> PatternGeometry:
    """
    Build a base block (stitching-line geometry) for the given configuration.

    In a full implementation, this would:
    - Resolve drafting_school_id/version and block_id/version to configs.
    - Resolve rule_graph_id/version to RuleGraphConfig.
    - Combine measurement_profile and config parameters into a formula context.

    For now, we require the caller to supply a resolved RuleGraphConfig via
    dependency injection at a higher level. Here we only structure the logic.
    """
    # Placeholder: the actual graph should be injected by higher-level services.
    # For engine-core scaffolding, we construct an empty graph.
    graph = RuleGraphConfig(id=rule_graph_id, version=rule_graph_version, nodes=[])

    geometry = execute_rule_graph(
        graph=graph,
        context_variables=dict(measurement_profile.values),
        geometry=None,
    )

    if metadata:
        geometry.metadata.update(metadata)
    geometry.metadata.update(
        {
            "drafting_school_id": drafting_school_id,
            "drafting_school_version": drafting_school_version,
            "block_id": block_id,
            "block_version": block_version,
            "rule_graph_id": rule_graph_id,
            "rule_graph_version": rule_graph_version,
        }
    )
    geometry.units = measurement_profile.unit
    return geometry





