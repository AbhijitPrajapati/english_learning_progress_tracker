from collections.abc import AsyncGenerator

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from backend.application.ports.unit_of_work import UnitOfWork
from backend.infrastructure.composition import InfrastructureComposition
from backend.infrastructure.database.unit_of_work import SqlAlchemyUnitOfWork

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
