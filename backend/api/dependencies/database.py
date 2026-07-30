from collections.abc import AsyncGenerator

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from application.analytics.accessor import MistakeAnalyticsAccessor
from application.common.unit_of_work import UnitOfWork
from backend.infrastructure.database.unit_of_work import SqlAlchemyUnitOfWork
from infrastructure.composition import InfrastructureComposition
from infrastructure.database.analytics_accessor import (
    SQLAlchemyMistakeAnalyticsAccessor,
)

from .composition import get_composition


async def get_session(
    composition: InfrastructureComposition = Depends(get_composition),
) -> AsyncGenerator[AsyncSession]:
    async with composition.session_factory() as session:
        yield session


async def get_uow(
    session: AsyncSession = Depends(get_session),
) -> AsyncGenerator[UnitOfWork]:
    async with SqlAlchemyUnitOfWork(session) as uow:
        yield uow


async def get_mistake_analytics_accessor(
    session: AsyncSession = Depends(get_session),
) -> MistakeAnalyticsAccessor:
    return SQLAlchemyMistakeAnalyticsAccessor(session)
