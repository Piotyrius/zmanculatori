from __future__ import annotations

from typing import Dict, Any, Optional

from ..geometry.patterns import PatternGeometry
from ..measurements.models import MeasurementProfile
from ..rules.executor import execute_rule_graph
from ..rules.models import RuleGraphConfig
from ..schools.models import DraftingSchoolConfig
from ..formulas.models import Formula, FormulaContext, FormulaType
from ..formulas.evaluator import evaluate_formula
from ..validators.pattern_validator import validate_measurements


def build_block_pattern(
    *,
    measurement_profile: MeasurementProfile,
    drafting_school_id: str,
    drafting_school_version: str,
    block_id: str,
    block_version: str,
    rule_graph_id: str,
    rule_graph_version: str,
    drafting_school_config: Optional[DraftingSchoolConfig] = None,
    rule_graph_config: Optional[RuleGraphConfig] = None,
    metadata: Dict[str, Any] | None = None,
) -> PatternGeometry:
    """
    Build a base block (stitching-line geometry) for the given configuration.

    Enhanced to:
    - Validate measurement requirements against school
    - Apply school-specific proportional logic
    - Combine measurement_profile and config parameters into a formula context.
    """
    # Validate measurement requirements if school config is provided
    if drafting_school_config:
        missing = measurement_profile.validate_required(
            drafting_school_config.measurement_requirements.required
        )
        if missing:
            raise ValueError(
                f"Missing required measurements for {drafting_school_config.name}: {missing}"
            )
    
    # Perform measurement sanity checks
    category = metadata.get("category", "womenswear") if metadata else "womenswear"
    measurement_validation = validate_measurements(measurement_profile.values, category)
    if not measurement_validation.is_valid:
        error_msg = "; ".join(measurement_validation.errors)
        raise ValueError(f"Measurement validation failed: {error_msg}")
    # Warnings are logged but don't block generation
    if measurement_validation.warnings:
        import logging
        logger = logging.getLogger(__name__)
        for warning in measurement_validation.warnings:
            logger.warning(f"Measurement warning: {warning}")
    
    # Build formula context with measurements
    context_vars = dict(measurement_profile.values)
    
    # Apply school-specific proportional logic if available
    if drafting_school_config and drafting_school_config.proportional_logic:
        formula_context = FormulaContext(variables=context_vars)
        for output_name, expression in drafting_school_config.proportional_logic.items():
            formula = Formula(
                expression=expression,
                formula_type=FormulaType.PROPORTIONAL,
            )
            try:
                calculated_value = evaluate_formula(formula, formula_context)
                context_vars[output_name] = calculated_value
            except Exception as e:
                # Log warning but continue - some formulas may depend on values not yet calculated
                pass
    
    # Use provided rule graph config or create empty one (for backward compatibility)
    if rule_graph_config:
        graph = rule_graph_config
    else:
        # Fallback: create empty graph (should not happen in production)
        graph = RuleGraphConfig(id=rule_graph_id, version=rule_graph_version, nodes=[])

    geometry = execute_rule_graph(
        graph=graph,
        context_variables=context_vars,
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







