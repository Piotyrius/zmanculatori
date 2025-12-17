"""
Config loading service for converting database JSONB configs to engine objects.

This service loads drafting schools, rule graphs, and blocks from the database
and converts them to the engine's internal representation.
"""
from __future__ import annotations

import logging
from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from engine.rules.models import RuleGraphConfig, RuleNode, RuleType
from engine.schools.models import (
    DraftingSchoolConfig,
    DraftingSchoolCategory,
    DraftingConventions,
    EasePhilosophy,
    MeasurementRequirements,
)
from engine.formulas.models import Formula, FormulaType

from ..db.models import DraftingSchool, RuleGraphConfigModel, BlockConfig

logger = logging.getLogger(__name__)


class ConfigLoader:
    """Service for loading and converting configs from database to engine objects."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def load_drafting_school(
        self, school_id: str, school_version: str
    ) -> Optional[DraftingSchoolConfig]:
        """Load drafting school from database and convert to DraftingSchoolConfig."""
        # Load by name and version first, then check config_jsonb id
        result = await self.session.execute(
            select(DraftingSchool).where(
                DraftingSchool.version == school_version,
            )
        )
        schools = result.scalars().all()
        
        # Find school with matching id in config_jsonb
        school = None
        for s in schools:
            config_id = s.config_jsonb.get("id") if s.config_jsonb else None
            if config_id == school_id:
                school = s
                break
        
        if not school:
            logger.warning(f"Drafting school {school_id} v{school_version} not found")
            return None

        config_json = school.config_jsonb
        if not config_json:
            logger.warning(f"Drafting school {school_id} has no config")
            return None

        # Convert category string to enum
        category_str = config_json.get("category", "educational_hybrid")
        try:
            category = DraftingSchoolCategory(category_str)
        except ValueError:
            logger.warning(f"Unknown category {category_str}, defaulting to educational_hybrid")
            category = DraftingSchoolCategory.EDUCATIONAL_HYBRID

        # Convert measurement requirements
        meas_req_json = config_json.get("measurement_requirements", {})
        measurement_requirements = MeasurementRequirements(
            required=meas_req_json.get("required", []),
            optional=meas_req_json.get("optional", []),
        )

        # Convert ease philosophy
        ease_phil_json = config_json.get("ease_philosophy", {})
        ease_philosophy = EasePhilosophy(values=ease_phil_json.get("values", {}))

        # Convert drafting conventions
        conv_json = config_json.get("drafting_conventions", {})
        drafting_conventions = DraftingConventions(conventions=conv_json.get("conventions", {}))

        return DraftingSchoolConfig(
            id=config_json.get("id", school_id),
            name=config_json.get("name", school.name),
            version=config_json.get("version", school_version),
            category=category,
            description=config_json.get("description"),
            measurement_requirements=measurement_requirements,
            proportional_logic=config_json.get("proportional_logic", {}),
            base_block_definitions=config_json.get("base_block_definitions", {}),
            ease_philosophy=ease_philosophy,
            drafting_conventions=drafting_conventions,
            metadata=config_json.get("metadata", {}),
        )

    async def load_rule_graph(
        self, rule_graph_id: str, rule_graph_version: str
    ) -> Optional[RuleGraphConfig]:
        """Load rule graph from database and convert to RuleGraphConfig."""
        # Load by version first, then check config_jsonb id
        result = await self.session.execute(
            select(RuleGraphConfigModel).where(
                RuleGraphConfigModel.version == rule_graph_version,
            )
        )
        rule_graphs = result.scalars().all()
        
        # Find rule graph with matching id in config_jsonb
        rule_graph_model = None
        for rg in rule_graphs:
            config_id = rg.config_jsonb.get("id") if rg.config_jsonb else None
            if config_id == rule_graph_id:
                rule_graph_model = rg
                break
        
        if not rule_graph_model:
            logger.warning(f"Rule graph {rule_graph_id} v{rule_graph_version} not found")
            return None

        config_json = rule_graph_model.config_jsonb
        if not config_json:
            logger.warning(f"Rule graph {rule_graph_id} has no config")
            return None

        # Convert nodes from JSON to RuleNode objects
        nodes_json = config_json.get("nodes", [])
        nodes = []
        for node_json in nodes_json:
            node = self._convert_node_json_to_rule_node(node_json)
            if node:
                nodes.append(node)

        return RuleGraphConfig(
            id=config_json.get("id", rule_graph_id),
            version=config_json.get("version", rule_graph_version),
            nodes=nodes,
        )

    def _convert_node_json_to_rule_node(self, node_json: dict) -> Optional[RuleNode]:
        """Convert a node JSON dict to a RuleNode object."""
        node_id = node_json.get("id")
        if not node_id:
            logger.warning("Node missing 'id' field")
            return None

        # Convert type string to RuleType enum
        type_str = node_json.get("type", "")
        try:
            node_type = RuleType(type_str)
        except ValueError:
            logger.warning(f"Unknown node type {type_str}, skipping node {node_id}")
            return None

        # Convert formula if present
        formula = None
        formula_json = node_json.get("formula")
        if formula_json:
            formula = self._convert_formula_json_to_formula(formula_json)

        return RuleNode(
            id=node_id,
            type=node_type,
            inputs=node_json.get("inputs", []),
            outputs=node_json.get("outputs", []),
            params=node_json.get("params", {}),
            formula=formula,
        )

    def _convert_formula_json_to_formula(self, formula_json: dict) -> Formula:
        """Convert formula JSON dict to Formula object."""
        from engine.formulas.models import FormulaType

        formula_type_str = formula_json.get("formula_type", "proportional")
        try:
            formula_type = FormulaType(formula_type_str)
        except ValueError:
            formula_type = FormulaType.PROPORTIONAL

        return Formula(
            expression=formula_json.get("expression", ""),
            formula_type=formula_type,
            version=formula_json.get("version", "1.0"),
            metadata=formula_json.get("metadata", {}),
            condition=formula_json.get("condition"),
            threshold=formula_json.get("threshold"),
            output_name=formula_json.get("output_name"),
        )

