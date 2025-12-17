"""
Seed data service for loading domain content.

Provides idempotent loading with version management.
"""
from __future__ import annotations

import logging
from typing import Dict, List, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import (
    DraftingSchool,
    BlockConfig,
    RuleGraphConfigModel,
    EaseProfileConfigModel,
    TransformPipelineConfigModel,
    MeasurementCategory,
    EducationalContent,
)
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from data.seeds import (
    drafting_schools,
    blocks,
    rule_graphs,
    ease_profiles,
    transforms,
    education,
    measurements,
)

logger = logging.getLogger(__name__)


class SeedService:
    """Service for loading seed data into the database."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def load_all(self) -> Dict[str, int]:
        """Load all seed data. Returns counts of loaded items."""
        counts = {}
        counts["measurement_categories"] = await self.load_measurement_categories()
        counts["drafting_schools"] = await self.load_drafting_schools()
        counts["blocks"] = await self.load_blocks()
        counts["rule_graphs"] = await self.load_rule_graphs()
        counts["ease_profiles"] = await self.load_ease_profiles()
        counts["transform_pipelines"] = await self.load_transform_pipelines()
        counts["educational_content"] = await self.load_educational_content()
        return counts

    async def load_measurement_categories(self) -> int:
        """Load measurement categories. Idempotent."""
        categories = measurements.get_measurement_categories()
        count = 0
        for cat_data in categories:
            # Check if exists
            result = await self.session.execute(
                select(MeasurementCategory).where(
                    MeasurementCategory.name == cat_data["name"]
                )
            )
            existing = result.scalars().first()
            if not existing:
                category = MeasurementCategory(**cat_data)
                self.session.add(category)
                count += 1
        await self.session.commit()
        logger.info(f"Loaded {count} measurement categories")
        return count

    async def load_drafting_schools(self) -> int:
        """Load drafting schools. Idempotent by name+version."""
        schools = drafting_schools.get_drafting_schools()
        count = 0
        for school_data in schools:
            # Check if exists
            result = await self.session.execute(
                select(DraftingSchool).where(
                    DraftingSchool.name == school_data["name"],
                    DraftingSchool.version == school_data["version"],
                )
            )
            existing = result.scalars().first()
            if not existing:
                school = DraftingSchool(**school_data)
                self.session.add(school)
                count += 1
        await self.session.commit()
        logger.info(f"Loaded {count} drafting schools")
        return count

    async def load_blocks(self) -> int:
        """Load blocks. Idempotent by name+version."""
        blocks_data = blocks.get_blocks()
        count = 0
        for block_data in blocks_data:
            # Check if exists
            result = await self.session.execute(
                select(BlockConfig).where(
                    BlockConfig.name == block_data["name"],
                    BlockConfig.version == block_data["version"],
                )
            )
            existing = result.scalars().first()
            if not existing:
                block = BlockConfig(**block_data)
                self.session.add(block)
                count += 1
        await self.session.commit()
        logger.info(f"Loaded {count} blocks")
        return count

    async def load_rule_graphs(self) -> int:
        """Load rule graphs. Idempotent by name+version."""
        graphs = rule_graphs.get_rule_graphs()
        count = 0
        for graph_data in graphs:
            # Check if exists
            result = await self.session.execute(
                select(RuleGraphConfigModel).where(
                    RuleGraphConfigModel.name == graph_data["name"],
                    RuleGraphConfigModel.version == graph_data["version"],
                )
            )
            existing = result.scalars().first()
            if not existing:
                graph = RuleGraphConfigModel(**graph_data)
                self.session.add(graph)
                count += 1
        await self.session.commit()
        logger.info(f"Loaded {count} rule graphs")
        return count

    async def load_ease_profiles(self) -> int:
        """Load ease profiles. Idempotent by name+version."""
        profiles = ease_profiles.get_ease_profiles()
        count = 0
        for profile_data in profiles:
            # Check if exists
            result = await self.session.execute(
                select(EaseProfileConfigModel).where(
                    EaseProfileConfigModel.name == profile_data["name"],
                    EaseProfileConfigModel.version == profile_data["version"],
                )
            )
            existing = result.scalars().first()
            if not existing:
                profile = EaseProfileConfigModel(**profile_data)
                self.session.add(profile)
                count += 1
        await self.session.commit()
        logger.info(f"Loaded {count} ease profiles")
        return count

    async def load_transform_pipelines(self) -> int:
        """Load transform pipelines. Idempotent by name+version."""
        pipelines = transforms.get_transform_pipelines()
        count = 0
        for pipeline_data in pipelines:
            # Check if exists
            result = await self.session.execute(
                select(TransformPipelineConfigModel).where(
                    TransformPipelineConfigModel.name == pipeline_data["name"],
                    TransformPipelineConfigModel.version == pipeline_data["version"],
                )
            )
            existing = result.scalars().first()
            if not existing:
                pipeline = TransformPipelineConfigModel(**pipeline_data)
                self.session.add(pipeline)
                count += 1
        await self.session.commit()
        logger.info(f"Loaded {count} transform pipelines")
        return count

    async def load_educational_content(self) -> int:
        """Load educational content. Idempotent by title+content_type."""
        content_list = education.get_educational_content()
        count = 0
        
        # First, load drafting schools to get IDs for linking
        schools_result = await self.session.execute(select(DraftingSchool))
        schools_map = {s.config_jsonb.get("id"): s.id for s in schools_result.scalars().all()}
        
        for content_data in content_list:
            # Check if exists
            result = await self.session.execute(
                select(EducationalContent).where(
                    EducationalContent.title == content_data["title"],
                    EducationalContent.content_type == content_data["content_type"],
                )
            )
            existing = result.scalars().first()
            if not existing:
                # Link drafting school if specified in config
                if content_data.get("drafting_school_id") is None:
                    # Try to find by name in config
                    config_id = content_data.get("metadata_jsonb", {}).get("drafting_school_id")
                    if config_id and config_id in schools_map:
                        content_data["drafting_school_id"] = schools_map[config_id]
                
                content = EducationalContent(**content_data)
                self.session.add(content)
                count += 1
        await self.session.commit()
        logger.info(f"Loaded {count} educational content items")
        return count

