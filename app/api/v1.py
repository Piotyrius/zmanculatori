from __future__ import annotations

from typing import Any, Dict, List

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel, EmailStr, Field
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from engine.interface import PatternRequest, generate_pattern, export_pattern
from engine.measurements.models import MeasurementProfile as EngineMeasurementProfile
from engine.export.models import ExportOptions

from ..db.session import get_session
from ..db.models import User, Project, MeasurementProfile
from ..services.pattern_service import PatternService
from ..auth.models import Token
from ..auth.security import verify_password, hash_password, create_access_token
from ..auth.deps import get_current_user
from ..settings import settings


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


class UserCreateRequest(BaseModel):
    email: EmailStr
    password: str


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
    }

    service = PatternService(session)
    pattern = await service.create_pattern_request(
        project_id=project.id,
        request=request,
        canonical_request_hash=canonical_hash,
        config_version_bundle=config_version_bundle,
    )

    geometry = generate_pattern(request)
    export_options = ExportOptions(format="svg")
    export_bundle = export_pattern(geometry, export_options)

    result = await service.store_pattern_result(
        pattern=pattern,
        geometry_json={"validation": getattr(geometry, "validation", None)},
        exports_json={
            "svg": {
                "mime_type": export_bundle.mime_type,
                "content": export_bundle.content.decode("utf-8", errors="ignore"),
                "metadata": export_bundle.metadata,
            }
        },
    )

    await session.commit()

    return {
        "pattern_id": pattern.id,
        "status": pattern.status,
        "result_id": result.id,
    }



