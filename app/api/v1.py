from __future__ import annotations

import base64
import logging
from datetime import datetime, timezone, timedelta
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel, EmailStr, Field
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from engine.interface import PatternRequest, generate_pattern, export_pattern
from engine.measurements.models import MeasurementProfile as EngineMeasurementProfile
from engine.export.models import ExportOptions

from ..db.session import get_session
from ..db.models import (
    User,
    Project,
    MeasurementProfile,
    DraftingSchool,
    BlockConfig,
    RuleGraphConfigModel,
    SizeProfileConfigModel,
    EaseProfileConfigModel,
    TransformPipelineConfigModel,
    Pattern,
    PatternResult,
    Subscription,
    Organization,
    OrganizationMember,
    ApiToken,
)
from ..services.pattern_service import PatternService
from ..auth.models import Token
from ..auth.security import verify_password, hash_password, create_access_token
from ..auth.deps import get_current_user
from ..settings import settings


router = APIRouter()
logger = logging.getLogger(__name__)


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
    size_profile_id: Optional[str] = None
    ease_profile_id: Optional[str] = None
    transform_pipeline_ids: List[str] = []
    debug: bool = False


class UserCreateRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=72)


class UserProfileResponse(BaseModel):
    id: int
    email: EmailStr


class ProjectCreateRequest(BaseModel):
    name: str = Field(..., max_length=255)


class ProjectResponse(BaseModel):
    id: int
    name: str
    status: str


class MeasurementProfileCreateRequest(BaseModel):
    name: str
    category: str = Field("womenswear", max_length=64)
    unit: str = Field("mm", max_length=16)
    values: Dict[str, float]


class MeasurementProfileResponse(BaseModel):
    id: int
    name: str
    category: str
    unit: str
    values: Dict[str, float]


class DraftingSchoolResponse(BaseModel):
    id: int
    name: str
    version: str
    config: Dict[str, Any]
    is_active: bool


class BlockConfigResponse(BaseModel):
    id: int
    name: str
    version: str
    config: Dict[str, Any]


class EaseProfileResponse(BaseModel):
    id: int
    name: str
    version: str
    config: Dict[str, Any]


class SizeProfileResponse(BaseModel):
    id: int
    name: str
    version: str
    config: Dict[str, Any]


class TransformPipelineResponse(BaseModel):
    id: int
    name: str
    version: str
    config: Dict[str, Any]


class RuleGraphResponse(BaseModel):
    id: int
    name: str
    version: str
    config: Dict[str, Any]


class PatternResultResponse(BaseModel):
    id: int
    pattern_id: int
    geometry: Optional[Dict[str, Any]] = None
    exports: Dict[str, Any]


class OrganizationCreateRequest(BaseModel):
    name: str = Field(..., max_length=255)


class OrganizationResponse(BaseModel):
    id: int
    name: str
    owner_id: int
    created_at: str


class OrganizationMemberResponse(BaseModel):
    id: int
    organization_id: int
    user_id: int
    user_email: str
    role: str


class OrganizationInviteRequest(BaseModel):
    email: EmailStr
    role: str = Field("member", max_length=64)


@router.post("/auth/login", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),  # noqa: B008
    session: AsyncSession = Depends(get_session),  # noqa: B008
) -> Token:
    result = await session.execute(
        User.__table__.select().where(User.email == form_data.username)
    )
    row = result.first()
    if not row:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user = User(**row._mapping)
    if not verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(
        subject=user.email,
        is_admin=user.is_admin,
        secret_key=settings.jwt_secret_key,
    )
    return Token(access_token=access_token)


@router.post(
    "/auth/register",
    response_model=UserProfileResponse,
    status_code=status.HTTP_201_CREATED,
)
async def register_user(
    payload: UserCreateRequest,
    session: AsyncSession = Depends(get_session),  # noqa: B008
) -> UserProfileResponse:
    existing = await session.execute(select(User).where(User.email == payload.email))
    if existing.scalars().first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists",
        )
    user = User(
        email=payload.email,
        password_hash=hash_password(payload.password),
        is_admin=False,
    )
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return UserProfileResponse(id=user.id, email=user.email)


@router.get("/auth/me", response_model=UserProfileResponse)
async def get_me(
    current_user: User = Depends(get_current_user),  # noqa: B008
) -> UserProfileResponse:
    return UserProfileResponse(id=current_user.id, email=current_user.email)


@router.post(
    "/projects",
    response_model=ProjectResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_project(
    payload: ProjectCreateRequest,
    current_user: User = Depends(get_current_user),  # noqa: B008
    session: AsyncSession = Depends(get_session),  # noqa: B008
) -> ProjectResponse:
    project = Project(
        owner_user_id=current_user.id,
        name=payload.name,
        status="active",
    )
    session.add(project)
    await session.commit()
    await session.refresh(project)
    return ProjectResponse(id=project.id, name=project.name, status=project.status)


@router.get("/projects", response_model=List[ProjectResponse])
async def list_projects(
    current_user: User = Depends(get_current_user),  # noqa: B008
    session: AsyncSession = Depends(get_session),  # noqa: B008
) -> List[ProjectResponse]:
    result = await session.execute(
        select(Project).where(Project.owner_user_id == current_user.id)
    )
    projects = result.scalars().all()
    return [
        ProjectResponse(id=p.id, name=p.name, status=p.status) for p in projects
    ]


@router.patch("/projects/{project_id}", response_model=ProjectResponse)
async def update_project(
    project_id: int,
    payload: ProjectCreateRequest,
    current_user: User = Depends(get_current_user),  # noqa: B008
    session: AsyncSession = Depends(get_session),  # noqa: B008
) -> ProjectResponse:
    result = await session.execute(
        select(Project).where(
            Project.id == project_id,
            Project.owner_user_id == current_user.id,
        )
    )
    project = result.scalars().first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Project not found"
        )
    project.name = payload.name
    await session.commit()
    await session.refresh(project)
    return ProjectResponse(id=project.id, name=project.name, status=project.status)


@router.delete("/projects/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_project(
    project_id: int,
    current_user: User = Depends(get_current_user),  # noqa: B008
    session: AsyncSession = Depends(get_session),  # noqa: B008
) -> None:
    result = await session.execute(
        select(Project).where(
            Project.id == project_id,
            Project.owner_user_id == current_user.id,
        )
    )
    project = result.scalars().first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Project not found"
        )
    await session.delete(project)
    await session.commit()


@router.post(
    "/measurement-profiles",
    response_model=MeasurementProfileResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_measurement_profile(
    payload: MeasurementProfileCreateRequest,
    current_user: User = Depends(get_current_user),  # noqa: B008
    session: AsyncSession = Depends(get_session),  # noqa: B008
) -> MeasurementProfileResponse:
    profile = MeasurementProfile(
        owner_user_id=current_user.id,
        name=payload.name,
        category=payload.category,
        unit=payload.unit,
        values_jsonb=payload.values,
    )
    session.add(profile)
    await session.commit()
    await session.refresh(profile)
    return MeasurementProfileResponse(
        id=profile.id,
        name=profile.name,
        category=profile.category,
        unit=profile.unit,
        values=profile.values_jsonb,
    )


@router.get(
    "/measurement-profiles",
    response_model=List[MeasurementProfileResponse],
)
async def list_measurement_profiles(
    current_user: User = Depends(get_current_user),  # noqa: B008
    session: AsyncSession = Depends(get_session),  # noqa: B008
) -> List[MeasurementProfileResponse]:
    result = await session.execute(
        select(MeasurementProfile).where(
            MeasurementProfile.owner_user_id == current_user.id
        )
    )
    profiles = result.scalars().all()
    return [
        MeasurementProfileResponse(
            id=p.id,
            name=p.name,
            category=p.category,
            unit=p.unit,
            values=p.values_jsonb,
        )
        for p in profiles
    ]


async def _get_user_tier(
    user: User, session: AsyncSession
) -> str:
    """Get user's subscription tier. Stub to 'pro' for MVP."""
    # Check for active subscription
    now = datetime.now(timezone.utc)
    result = await session.execute(
        select(Subscription).where(
            Subscription.user_id == user.id,
            Subscription.valid_until > now,
        )
    )
    subscription = result.scalars().first()
    if subscription:
        return subscription.tier
    # Default to 'pro' for MVP
    return "pro"


@router.post("/patterns/generate", status_code=status.HTTP_202_ACCEPTED)
async def generate_pattern_endpoint(
    payload: PatternGenerationRequestModel,
    current_user: User = Depends(get_current_user),  # noqa: B008
    session: AsyncSession = Depends(get_session),  # noqa: B008
) -> Dict[str, Any]:
    """
    MVP synchronous generation endpoint.

    For now this executes the engine inline and persists Pattern/PatternResult.
    """
    # Ensure project belongs to user
    project_result = await session.execute(
        select(Project).where(
            Project.id == payload.project_id,
            Project.owner_user_id == current_user.id,
        )
    )
    project = project_result.scalars().first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Project not found"
        )

    # Check subscription tier (stub to 'pro' for MVP)
    tier = await _get_user_tier(current_user, session)
    # For MVP, allow all features for 'pro' tier
    # In future, validate transform_pipeline_ids and custom profiles based on tier

    measurement_profile = EngineMeasurementProfile(
        values=payload.measurements.values,
        unit=payload.measurements.unit,
    )

    request = PatternRequest(
        measurement_profile=measurement_profile,
        garment_type=payload.garment_type,
        fit=payload.fit,
        category=payload.category,
        drafting_school_id=payload.drafting_school_id,
        drafting_school_version=payload.drafting_school_version,
        block_id=payload.block_id,
        block_version=payload.block_version,
        rule_graph_id=payload.rule_graph_id,
        rule_graph_version=payload.rule_graph_version,
        size_profile_id=payload.size_profile_id,
        ease_profile_id=payload.ease_profile_id,
        transform_pipeline_ids=payload.transform_pipeline_ids,
        debug=payload.debug,
    )

    # In a full system canonical_request_hash would be a deterministic hash of the request.
    canonical_hash = "mvp-sync"
    config_version_bundle: Dict[str, Any] = {
        "drafting_school_id": payload.drafting_school_id,
        "drafting_school_version": payload.drafting_school_version,
        "block_id": payload.block_id,
        "block_version": payload.block_version,
        "rule_graph_id": payload.rule_graph_id,
        "rule_graph_version": payload.rule_graph_version,
        "size_profile_id": payload.size_profile_id,
        "ease_profile_id": payload.ease_profile_id,
        "transform_pipeline_ids": payload.transform_pipeline_ids,
    }

    service = PatternService(session)
    pattern = await service.create_pattern_request(
        project_id=project.id,
        request=request,
        canonical_request_hash=canonical_hash,
        config_version_bundle=config_version_bundle,
    )

    geometry = generate_pattern(request)
    
    # Generate exports in all formats
    exports_json: Dict[str, Any] = {}
    
    # SVG
    svg_options = ExportOptions(format="svg")
    svg_bundle = export_pattern(geometry, svg_options)
    exports_json["svg"] = {
        "mime_type": svg_bundle.mime_type,
        "content": svg_bundle.content.decode("utf-8", errors="ignore"),
        "metadata": svg_bundle.metadata,
    }
    
    # DXF
    try:
        dxf_options = ExportOptions(format="dxf")
        dxf_bundle = export_pattern(geometry, dxf_options)
        exports_json["dxf"] = {
            "mime_type": dxf_bundle.mime_type,
            "content": dxf_bundle.content.decode("utf-8", errors="ignore"),
            "metadata": dxf_bundle.metadata,
        }
    except Exception as e:
        # Log but don't fail if DXF export fails
        logger.warning(f"DXF export failed: {e}")
    
    # PDF
    try:
        pdf_options = ExportOptions(format="pdf", dpi=300)
        pdf_bundle = export_pattern(geometry, pdf_options)
        exports_json["pdf"] = {
            "mime_type": pdf_bundle.mime_type,
            "content": base64.b64encode(pdf_bundle.content).decode("utf-8"),  # Base64 encode binary PDF
            "metadata": pdf_bundle.metadata,
        }
    except Exception as e:
        # Log but don't fail if PDF export fails
        logger.warning(f"PDF export failed: {e}")

    result = await service.store_pattern_result(
        pattern=pattern,
        geometry_json={"validation": getattr(geometry, "validation", None)},
        exports_json=exports_json,
    )

    await session.commit()

    return {
        "pattern_id": pattern.id,
        "status": pattern.status,
        "result_id": result.id,
    }


@router.get("/configs/drafting-schools", response_model=List[DraftingSchoolResponse])
async def list_drafting_schools(
    active_only: bool = True,
    current_user: User = Depends(get_current_user),  # noqa: B008
    session: AsyncSession = Depends(get_session),  # noqa: B008
) -> List[DraftingSchoolResponse]:
    """List available drafting schools."""
    query = select(DraftingSchool)
    if active_only:
        query = query.where(DraftingSchool.is_active == True)  # noqa: E712
    result = await session.execute(query)
    schools = result.scalars().all()
    return [
        DraftingSchoolResponse(
            id=s.id,
            name=s.name,
            version=s.version,
            config=s.config_jsonb,
            is_active=s.is_active,
        )
        for s in schools
    ]


@router.get("/configs/blocks", response_model=List[BlockConfigResponse])
async def list_blocks(
    current_user: User = Depends(get_current_user),  # noqa: B008
    session: AsyncSession = Depends(get_session),  # noqa: B008
) -> List[BlockConfigResponse]:
    """List available block configurations."""
    result = await session.execute(select(BlockConfig))
    blocks = result.scalars().all()
    return [
        BlockConfigResponse(
            id=b.id,
            name=b.name,
            version=b.version,
            config=b.config_jsonb,
        )
        for b in blocks
    ]


@router.get("/configs/ease-profiles", response_model=List[EaseProfileResponse])
async def list_ease_profiles(
    current_user: User = Depends(get_current_user),  # noqa: B008
    session: AsyncSession = Depends(get_session),  # noqa: B008
) -> List[EaseProfileResponse]:
    """List available ease profiles."""
    result = await session.execute(select(EaseProfileConfigModel))
    profiles = result.scalars().all()
    return [
        EaseProfileResponse(
            id=p.id,
            name=p.name,
            version=p.version,
            config=p.config_jsonb,
        )
        for p in profiles
    ]


@router.get("/configs/size-profiles", response_model=List[SizeProfileResponse])
async def list_size_profiles(
    current_user: User = Depends(get_current_user),  # noqa: B008
    session: AsyncSession = Depends(get_session),  # noqa: B008
) -> List[SizeProfileResponse]:
    """List available size profiles."""
    result = await session.execute(select(SizeProfileConfigModel))
    profiles = result.scalars().all()
    return [
        SizeProfileResponse(
            id=p.id,
            name=p.name,
            version=p.version,
            config=p.config_jsonb,
        )
        for p in profiles
    ]


@router.get(
    "/configs/transform-pipelines", response_model=List[TransformPipelineResponse]
)
async def list_transform_pipelines(
    current_user: User = Depends(get_current_user),  # noqa: B008
    session: AsyncSession = Depends(get_session),  # noqa: B008
) -> List[TransformPipelineResponse]:
    """List available transform pipelines."""
    result = await session.execute(select(TransformPipelineConfigModel))
    pipelines = result.scalars().all()
    return [
        TransformPipelineResponse(
            id=p.id,
            name=p.name,
            version=p.version,
            config=p.config_jsonb,
        )
        for p in pipelines
    ]


@router.get("/configs/rule-graphs", response_model=List[RuleGraphResponse])
async def list_rule_graphs(
    current_user: User = Depends(get_current_user),  # noqa: B008
    session: AsyncSession = Depends(get_session),  # noqa: B008
) -> List[RuleGraphResponse]:
    """List available rule graph configurations."""
    result = await session.execute(select(RuleGraphConfigModel))
    graphs = result.scalars().all()
    return [
        RuleGraphResponse(
            id=g.id,
            name=g.name,
            version=g.version,
            config=g.config_jsonb,
        )
        for g in graphs
    ]


@router.get("/projects/{project_id}/patterns", response_model=List[Dict[str, Any]])
async def list_project_patterns(
    project_id: int,
    current_user: User = Depends(get_current_user),  # noqa: B008
    session: AsyncSession = Depends(get_session),  # noqa: B008
) -> List[Dict[str, Any]]:
    """List all patterns for a project (version history)."""
    # Verify project belongs to user
    project_result = await session.execute(
        select(Project).where(
            Project.id == project_id,
            Project.owner_user_id == current_user.id,
        )
    )
    project = project_result.scalars().first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Project not found"
        )

    # Get patterns with results
    patterns_result = await session.execute(
        select(Pattern)
        .where(Pattern.project_id == project_id)
        .order_by(Pattern.created_at.desc())
    )
    patterns = patterns_result.scalars().all()
    
    # Get results for each pattern
    result_list = []
    for pattern in patterns:
        result_query = await session.execute(
            select(PatternResult).where(PatternResult.pattern_id == pattern.id)
        )
        result = result_query.scalars().first()
        result_list.append({
            "id": pattern.id,
            "project_id": pattern.project_id,
            "status": pattern.status,
            "version_index": pattern.version_index,
            "tag": pattern.tag,
            "config": pattern.config_version_bundle_jsonb,
            "created_at": pattern.created_at.isoformat() if pattern.created_at else None,
            "has_result": result is not None,
        })
    
    return result_list


@router.get("/patterns/{pattern_id}/diff/{other_pattern_id}", response_model=Dict[str, Any])
async def compare_pattern_versions(
    pattern_id: int,
    other_pattern_id: int,
    current_user: User = Depends(get_current_user),  # noqa: B008
    session: AsyncSession = Depends(get_session),  # noqa: B008
) -> Dict[str, Any]:
    """Compare two pattern versions and return differences in their config bundles."""
    # Verify both patterns belong to user's projects
    patterns_result = await session.execute(
        select(Pattern)
        .join(Project)
        .where(
            Pattern.id.in_([pattern_id, other_pattern_id]),
            Project.owner_user_id == current_user.id,
        )
    )
    patterns = {p.id: p for p in patterns_result.scalars().all()}
    
    if pattern_id not in patterns or other_pattern_id not in patterns:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="One or both patterns not found"
        )
    
    pattern1 = patterns[pattern_id]
    pattern2 = patterns[other_pattern_id]
    
    # Compare config bundles
    config1 = pattern1.config_version_bundle_jsonb
    config2 = pattern2.config_version_bundle_jsonb
    
    def deep_diff(d1: Dict[str, Any], d2: Dict[str, Any], path: str = "") -> List[Dict[str, Any]]:
        """Recursively find differences between two dictionaries."""
        diffs = []
        all_keys = set(d1.keys()) | set(d2.keys())
        
        for key in all_keys:
            current_path = f"{path}.{key}" if path else key
            val1 = d1.get(key)
            val2 = d2.get(key)
            
            if key not in d1:
                diffs.append({
                    "path": current_path,
                    "type": "added",
                    "old_value": None,
                    "new_value": val2,
                })
            elif key not in d2:
                diffs.append({
                    "path": current_path,
                    "type": "removed",
                    "old_value": val1,
                    "new_value": None,
                })
            elif isinstance(val1, dict) and isinstance(val2, dict):
                diffs.extend(deep_diff(val1, val2, current_path))
            elif val1 != val2:
                diffs.append({
                    "path": current_path,
                    "type": "changed",
                    "old_value": val1,
                    "new_value": val2,
                })
        
        return diffs
    
    differences = deep_diff(config1, config2)
    
    return {
        "pattern1_id": pattern_id,
        "pattern1_version": pattern1.version_index,
        "pattern2_id": other_pattern_id,
        "pattern2_version": pattern2.version_index,
        "differences": differences,
        "summary": {
            "total_changes": len(differences),
            "added": len([d for d in differences if d["type"] == "added"]),
            "removed": len([d for d in differences if d["type"] == "removed"]),
            "changed": len([d for d in differences if d["type"] == "changed"]),
        },
    }


@router.post("/patterns/{pattern_id}/restore", response_model=Dict[str, Any])
async def restore_pattern_version(
    pattern_id: int,
    current_user: User = Depends(get_current_user),  # noqa: B008
    session: AsyncSession = Depends(get_session),  # noqa: B008
) -> Dict[str, Any]:
    """Restore a previous pattern version by cloning its configuration."""
    # Verify pattern belongs to user's project
    pattern_result = await session.execute(
        select(Pattern)
        .join(Project)
        .where(
            Pattern.id == pattern_id,
            Project.owner_user_id == current_user.id,
        )
    )
    old_pattern = pattern_result.scalars().first()
    if not old_pattern:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Pattern not found"
        )

    # Get the next version index
    from sqlalchemy import func
    max_version_result = await session.execute(
        select(func.max(Pattern.version_index))
        .where(Pattern.project_id == old_pattern.project_id)
    )
    max_version = max_version_result.scalar_one_or_none()
    next_version = (max_version or 0) + 1

    # Create new pattern with same config
    new_pattern = Pattern(
        project_id=old_pattern.project_id,
        block_type=old_pattern.block_type,
        engine_api_version=old_pattern.engine_api_version,
        config_version_bundle_jsonb=old_pattern.config_version_bundle_jsonb,
        canonical_request_hash=old_pattern.canonical_request_hash,
        status="pending",
        version_index=next_version,
        tag=f"Restored from v{old_pattern.version_index or '?'}",
    )
    session.add(new_pattern)
    await session.flush()

    return {
        "pattern_id": new_pattern.id,
        "project_id": new_pattern.project_id,
        "version_index": new_pattern.version_index,
        "status": new_pattern.status,
    }


@router.get("/patterns/{pattern_id}/result", response_model=PatternResultResponse)
async def get_pattern_result(
    pattern_id: int,
    current_user: User = Depends(get_current_user),  # noqa: B008
    session: AsyncSession = Depends(get_session),  # noqa: B008
) -> PatternResultResponse:
    """Fetch pattern result including geometry and exports."""
    # Verify pattern belongs to user's project
    pattern_result = await session.execute(
        select(Pattern)
        .join(Project)
        .where(
            Pattern.id == pattern_id,
            Project.owner_user_id == current_user.id,
        )
    )
    pattern = pattern_result.scalars().first()
    if not pattern:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Pattern not found"
        )

    # Get the result
    result_query = await session.execute(
        select(PatternResult).where(PatternResult.pattern_id == pattern_id)
    )
    result = result_query.scalars().first()
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Pattern result not found"
        )

    return PatternResultResponse(
        id=result.id,
        pattern_id=result.pattern_id,
        geometry=result.geometry_jsonb,
        exports=result.exports_jsonb,
    )


@router.post("/patterns/{pattern_id}/export")
async def export_pattern_file(
    pattern_id: int,
    format: str = "svg",
    current_user: User = Depends(get_current_user),  # noqa: B008
    session: AsyncSession = Depends(get_session),  # noqa: B008
) -> Dict[str, Any]:
    """Export pattern in the specified format (SVG/DXF/PDF)."""
    from fastapi.responses import Response
    
    # Verify pattern belongs to user's project
    pattern_result = await session.execute(
        select(Pattern)
        .join(Project)
        .where(
            Pattern.id == pattern_id,
            Project.owner_user_id == current_user.id,
        )
    )
    pattern = pattern_result.scalars().first()
    if not pattern:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Pattern not found"
        )

    # Get the result
    result_query = await session.execute(
        select(PatternResult).where(PatternResult.pattern_id == pattern_id)
    )
    result = result_query.scalars().first()
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Pattern result not found"
        )

    # Check if export already exists
    format_key = format.lower()
    exports = result.exports_jsonb or {}
    
    if format_key in exports:
        export_data = exports[format_key]
        if isinstance(export_data, dict) and "content" in export_data:
            content = export_data["content"]
            if isinstance(content, str):
                # Check if it's base64 encoded (PDF) or plain text (SVG/DXF)
                if format_key == "pdf":
                    try:
                        content_bytes = base64.b64decode(content)
                    except Exception:
                        content_bytes = content.encode("utf-8")
                else:
                    content_bytes = content.encode("utf-8")
            else:
                content_bytes = content
            
            mime_type = export_data.get("mime_type", "application/octet-stream")
            return Response(
                content=content_bytes,
                media_type=mime_type,
                headers={
                    "Content-Disposition": f'attachment; filename="pattern_{pattern_id}.{format_key}"',
                },
            )

    # Export not found, return error
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Export format '{format}' not available for this pattern",
    )


@router.post(
    "/organizations",
    response_model=OrganizationResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_organization(
    payload: OrganizationCreateRequest,
    current_user: User = Depends(get_current_user),  # noqa: B008
    session: AsyncSession = Depends(get_session),  # noqa: B008
) -> OrganizationResponse:
    """Create a new organization."""
    org = Organization(
        name=payload.name,
        owner_id=current_user.id,
    )
    session.add(org)
    await session.flush()
    
    # Add creator as admin member
    member = OrganizationMember(
        organization_id=org.id,
        user_id=current_user.id,
        role="admin",
    )
    session.add(member)
    await session.commit()
    await session.refresh(org)
    
    return OrganizationResponse(
        id=org.id,
        name=org.name,
        owner_id=org.owner_id,
        created_at=org.created_at.isoformat() if org.created_at else "",
    )


@router.get("/organizations", response_model=List[OrganizationResponse])
async def list_organizations(
    current_user: User = Depends(get_current_user),  # noqa: B008
    session: AsyncSession = Depends(get_session),  # noqa: B008
) -> List[OrganizationResponse]:
    """List organizations the user belongs to."""
    result = await session.execute(
        select(Organization)
        .join(OrganizationMember)
        .where(OrganizationMember.user_id == current_user.id)
    )
    orgs = result.scalars().all()
    return [
        OrganizationResponse(
            id=o.id,
            name=o.name,
            owner_id=o.owner_id,
            created_at=o.created_at.isoformat() if o.created_at else "",
        )
        for o in orgs
    ]


@router.get(
    "/organizations/{org_id}/members",
    response_model=List[OrganizationMemberResponse],
)
async def list_organization_members(
    org_id: int,
    current_user: User = Depends(get_current_user),  # noqa: B008
    session: AsyncSession = Depends(get_session),  # noqa: B008
) -> List[OrganizationMemberResponse]:
    """List members of an organization."""
    # Verify user is a member
    member_check = await session.execute(
        select(OrganizationMember).where(
            OrganizationMember.organization_id == org_id,
            OrganizationMember.user_id == current_user.id,
        )
    )
    if not member_check.scalars().first():
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not a member of this organization",
        )

    # Get all members
    result = await session.execute(
        select(OrganizationMember, User)
        .join(User, OrganizationMember.user_id == User.id)
        .where(OrganizationMember.organization_id == org_id)
    )
    members = result.all()
    return [
        OrganizationMemberResponse(
            id=m.id,
            organization_id=m.organization_id,
            user_id=m.user_id,
            user_email=u.email,
            role=m.role,
        )
        for m, u in members
    ]


@router.post(
    "/organizations/{org_id}/invite",
    status_code=status.HTTP_201_CREATED,
)
async def invite_to_organization(
    org_id: int,
    payload: OrganizationInviteRequest,
    current_user: User = Depends(get_current_user),  # noqa: B008
    session: AsyncSession = Depends(get_session),  # noqa: B008
) -> Dict[str, Any]:
    """Invite a user to an organization."""
    # Verify user is admin of org
    member_check = await session.execute(
        select(OrganizationMember).where(
            OrganizationMember.organization_id == org_id,
            OrganizationMember.user_id == current_user.id,
            OrganizationMember.role == "admin",
        )
    )
    if not member_check.scalars().first():
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can invite members",
        )

    # Find user by email
    user_result = await session.execute(
        select(User).where(User.email == payload.email)
    )
    user = user_result.scalars().first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    # Check if already a member
    existing = await session.execute(
        select(OrganizationMember).where(
            OrganizationMember.organization_id == org_id,
            OrganizationMember.user_id == user.id,
        )
    )
    if existing.scalars().first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User is already a member",
        )

    # Add member
    member = OrganizationMember(
        organization_id=org_id,
        user_id=user.id,
        role=payload.role,
    )
    session.add(member)
    await session.commit()
    await session.refresh(member)

    return {
        "id": member.id,
        "organization_id": member.organization_id,
        "user_id": member.user_id,
        "role": member.role,
    }


class ApiTokenCreateRequest(BaseModel):
    name: str = Field(..., max_length=255)
    scopes: List[str] = Field(default_factory=list)
    expires_in_days: Optional[int] = Field(None, ge=1, le=365)


class ApiTokenResponse(BaseModel):
    id: int
    name: str
    scopes: List[str]
    created_at: str
    last_used_at: Optional[str]
    expires_at: Optional[str]
    is_active: bool
    token: Optional[str] = None  # Only returned on creation


@router.post(
    "/api-tokens",
    response_model=ApiTokenResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_api_token(
    payload: ApiTokenCreateRequest,
    current_user: User = Depends(get_current_user),  # noqa: B008
    session: AsyncSession = Depends(get_session),  # noqa: B008
) -> ApiTokenResponse:
    """Create a new API token for programmatic access."""
    import secrets
    import hashlib
    
    # Generate a secure token
    raw_token = secrets.token_urlsafe(32)
    token_hash = hashlib.sha256(raw_token.encode()).hexdigest()
    
    # Calculate expiration
    expires_at = None
    if payload.expires_in_days:
        expires_at = datetime.now(timezone.utc) + timedelta(days=payload.expires_in_days)
    
    api_token = ApiToken(
        user_id=current_user.id,
        name=payload.name,
        token_hash=token_hash,
        scopes_jsonb={"scopes": payload.scopes},
        expires_at=expires_at,
        is_active=True,
    )
    session.add(api_token)
    await session.commit()
    await session.refresh(api_token)
    
    return ApiTokenResponse(
        id=api_token.id,
        name=api_token.name,
        scopes=api_token.scopes_jsonb.get("scopes", []),
        created_at=api_token.created_at.isoformat() if api_token.created_at else "",
        last_used_at=api_token.last_used_at.isoformat() if api_token.last_used_at else None,
        expires_at=api_token.expires_at.isoformat() if api_token.expires_at else None,
        is_active=api_token.is_active,
        token=raw_token,  # Only returned once on creation
    )


@router.get("/api-tokens", response_model=List[ApiTokenResponse])
async def list_api_tokens(
    current_user: User = Depends(get_current_user),  # noqa: B008
    session: AsyncSession = Depends(get_session),  # noqa: B008
) -> List[ApiTokenResponse]:
    """List all API tokens for the current user."""
    result = await session.execute(
        select(ApiToken).where(ApiToken.user_id == current_user.id)
    )
    tokens = result.scalars().all()
    return [
        ApiTokenResponse(
            id=t.id,
            name=t.name,
            scopes=t.scopes_jsonb.get("scopes", []),
            created_at=t.created_at.isoformat() if t.created_at else "",
            last_used_at=t.last_used_at.isoformat() if t.last_used_at else None,
            expires_at=t.expires_at.isoformat() if t.expires_at else None,
            is_active=t.is_active,
        )
        for t in tokens
    ]


@router.delete("/api-tokens/{token_id}", status_code=status.HTTP_204_NO_CONTENT)
async def revoke_api_token(
    token_id: int,
    current_user: User = Depends(get_current_user),  # noqa: B008
    session: AsyncSession = Depends(get_session),  # noqa: B008
) -> None:
    """Revoke (delete) an API token."""
    result = await session.execute(
        select(ApiToken).where(
            ApiToken.id == token_id,
            ApiToken.user_id == current_user.id,
        )
    )
    token = result.scalars().first()
    if not token:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="API token not found"
        )
    
    await session.delete(token)
    await session.commit()



