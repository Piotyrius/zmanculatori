from __future__ import annotations

import asyncio
import logging

from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from sqladmin import Admin
from prometheus_fastapi_instrumentator import Instrumentator

from .api.v1 import router as api_v1_router
from .db.session import get_session, engine
from .db.models import Base
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
logger = logging.getLogger(__name__)

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


@app.on_event("startup")
async def on_startup() -> None:
    """
    Development convenience: ensure all SQLAlchemy models have tables.

    In production you'd typically run migrations instead of this.
    Includes simple retry logic so Postgres inside Docker has time to start.
    """
    max_attempts = 10
    delay_seconds = 2

    for attempt in range(1, max_attempts + 1):
        try:
            async with engine.begin() as conn:
                await conn.run_sync(Base.metadata.create_all)
            logger.info("Database tables created/verified.")
            break
        except Exception as exc:  # noqa: BLE001
            logger.warning(
                "DB init attempt %s/%s failed: %s",
                attempt,
                max_attempts,
                exc,
            )
            if attempt == max_attempts:
                logger.error("Giving up on DB init; API may fail if DB is unavailable.")
                break
            await asyncio.sleep(delay_seconds)

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



