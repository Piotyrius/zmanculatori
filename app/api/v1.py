from __future__ import annotations

from typing import Any, Dict

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession

from engine.measurements.models import MeasurementProfile

from ..db.session import get_session
from ..services.pattern_service import PatternService


router = APIRouter()


class MeasurementInputModel(BaseModel):
    values: Dict[str, float]
    unit: str = "mm"


class PatternGenerationRequestModel(BaseModel):
    project_id: int
    garment_type: str
    fit: str
    category: str
    measurements: MeasurementInputModel
    drafting_school_id: str
    drafting_school_version: str
    block_id: str
    block_version: str
    rule_graph_id: str
    rule_graph_version: str
    debug: bool = False


@router.post("/patterns/generate", status_code=status.HTTP_202_ACCEPTED)
async def generate_pattern_endpoint(
    payload: PatternGenerationRequestModel,
    session: AsyncSession = Depends(get_session),  # noqa: B008
) -> Dict[str, Any]:
    """
    MVP synchronous generation endpoint.

    In the full system this will enqueue a Celery task and return a job ID.
    """
    service = PatternService(session)

    profile = MeasurementProfile(
        values=payload.measurements.values,
        unit=payload.measurements.unit,
    )

    canonical_hash = "todo-hash"  # placeholder until async/caching todo
    config_version_bundle: Dict[str, Any] = {
        "drafting_school_id": payload.drafting_school_id,
        "drafting_school_version": payload.drafting_school_version,
        "block_id": payload.block_id,
        "block_version": payload.block_version,
        "rule_graph_id": payload.rule_graph_id,
        "rule_graph_version": payload.rule_graph_version,
    }

    # For MVP we do not actually invoke the engine here (no configs loaded yet).
    pattern = await service.create_pattern_request(
        project_id=payload.project_id,
        request=None,  # type: ignore[arg-type]
        canonical_request_hash=canonical_hash,
        config_version_bundle=config_version_bundle,
    )
    await session.commit()

    return {"pattern_id": pattern.id, "status": pattern.status}



