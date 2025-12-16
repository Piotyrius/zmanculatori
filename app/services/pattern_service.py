from __future__ import annotations

from typing import Any, Dict, Optional

from sqlalchemy.ext.asyncio import AsyncSession

from engine import PatternRequest, generate_pattern, export_pattern
from engine.export.models import ExportOptions
from engine.measurements.models import MeasurementProfile

from ..db.models import Pattern, PatternResult


class PatternService:
    """
    Orchestrates pattern generation and export around the pure engine.

    This service is intentionally thin for now; subscription checks and
    async dispatch will be layered on top via Celery tasks.
    """

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create_pattern_request(
        self,
        project_id: int,
        request: PatternRequest,
        canonical_request_hash: str,
        config_version_bundle: Dict[str, Any],
    ) -> Pattern:
        pattern = Pattern(
            project_id=project_id,
            block_type=request.garment_type,
            engine_api_version=request.engine_api_version,
            config_version_bundle_jsonb=config_version_bundle,
            canonical_request_hash=canonical_request_hash,
            status="pending",
        )
        self.session.add(pattern)
        await self.session.flush()
        return pattern

    async def store_pattern_result(
        self,
        pattern: Pattern,
        geometry_json: Dict[str, Any],
        exports_json: Dict[str, Any],
    ) -> PatternResult:
        pattern.status = "completed"
        result = PatternResult(
            pattern_id=pattern.id,
            geometry_jsonb=geometry_json,
            exports_jsonb=exports_json,
        )
        self.session.add(result)
        await self.session.flush()
        return result


