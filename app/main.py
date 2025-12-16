from __future__ import annotations

from fastapi import Depends, FastAPI
from sqlalchemy.ext.asyncio import AsyncSession

from .api.v1 import router as api_v1_router
from .db.session import get_session


app = FastAPI(title="Garment Pattern Backend", version="0.1.0")


@app.get("/health")
async def health() -> dict:
    return {"status": "ok"}


@app.get("/ready")
async def ready(session: AsyncSession = Depends(get_session)) -> dict:  # noqa: B008
    # Touch the session to ensure DB connectivity.
    await session.execute("SELECT 1")
    return {"status": "ready"}


app.include_router(api_v1_router, prefix="/v1")



