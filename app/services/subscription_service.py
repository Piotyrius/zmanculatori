from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from ..db.models import Pattern, Subscription


@dataclass(slots=True)
class Capabilities:
    max_patterns_per_month: int
    max_concurrent_jobs: int
    allowed_export_formats: list[str]
    priority_queue: str


class SubscriptionService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_capabilities_for_user(self, user_id: int) -> Capabilities:
        result = await self.session.execute(
            select(Subscription).where(Subscription.user_id == user_id)
        )
        sub = result.scalars().first()
        if not sub:
            # sensible defaults for free tier
            return Capabilities(
                max_patterns_per_month=50,
                max_concurrent_jobs=2,
                allowed_export_formats=["svg"],
                priority_queue="low",
            )
        caps = sub.capabilities_jsonb or {}
        return Capabilities(
            max_patterns_per_month=int(caps.get("max_patterns_per_month", 200)),
            max_concurrent_jobs=int(caps.get("max_concurrent_jobs", 5)),
            allowed_export_formats=list(caps.get("allowed_export_formats", ["svg"])),
            priority_queue=str(caps.get("priority_queue", "standard")),
        )

    async def check_pattern_limits(self, user_id: int) -> None:
        # Placeholder: simple concurrent job count check.
        result = await self.session.execute(
            select(func.count(Pattern.id)).where(Pattern.status.in_(("pending", "running")))
        )
        running = int(result.scalar_one())
        caps = await self.get_capabilities_for_user(user_id)
        if running >= caps.max_concurrent_jobs:
            raise PermissionError("Concurrent pattern limit exceeded.")










