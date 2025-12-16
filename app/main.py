from __future__ import annotations

from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from sqladmin import Admin
from prometheus_fastapi_instrumentator import Instrumentator

from .api.v1 import router as api_v1_router
from .db.session import get_session, engine
from .admin.views import (
    UserAdmin,
    OrganizationAdmin,
    OrganizationMemberAdmin,
    SubscriptionAdmin,
    ProjectAdmin,
    PatternAdmin,
    PatternResultAdmin,
    DraftingSchoolAdmin,
    BlockConfigAdmin,
    RuleGraphConfigAdmin,
    TransformPipelineConfigAdmin,
    SizeProfileConfigAdmin,
    EaseProfileConfigAdmin,
    SeamAllowanceProfileConfigAdmin,
    ConfigAuditLogAdmin,
)
from .logging_config import configure_logging


configure_logging()

app = FastAPI(
    title="Garment Pattern Backend",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

# CORS configuration for local frontend (Next.js on http://localhost:3000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

admin = Admin(app, engine.sync_engine)
admin.add_view(UserAdmin)
admin.add_view(OrganizationAdmin)
admin.add_view(OrganizationMemberAdmin)
admin.add_view(SubscriptionAdmin)
admin.add_view(ProjectAdmin)
admin.add_view(PatternAdmin)
admin.add_view(PatternResultAdmin)
admin.add_view(DraftingSchoolAdmin)
admin.add_view(BlockConfigAdmin)
admin.add_view(RuleGraphConfigAdmin)
admin.add_view(TransformPipelineConfigAdmin)
admin.add_view(SizeProfileConfigAdmin)
admin.add_view(EaseProfileConfigAdmin)
admin.add_view(SeamAllowanceProfileConfigAdmin)
admin.add_view(ConfigAuditLogAdmin)


@app.get("/health")
async def health() -> dict:
    return {"status": "ok"}


@app.get("/ready")
async def ready(session: AsyncSession = Depends(get_session)) -> dict:  # noqa: B008
    # Touch the session to ensure DB connectivity.
    await session.execute("SELECT 1")
    return {"status": "ready"}


app.include_router(api_v1_router, prefix="/v1")


Instrumentator().instrument(app).expose(app)



