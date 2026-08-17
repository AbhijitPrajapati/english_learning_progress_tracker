from uuid import UUID

from pydantic import EmailStr
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.ports.repositories import UserRepository
from app.domain.user import User
from app.infrastructure.database.models import User as ORMUser


class SQLAlchemyUserRepository(UserRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, email: EmailStr, password_hash: str) -> User:
        orm_user = ORMUser(email=email, password_hash=password_hash)
        self.session.add(orm_user)
        await self.session.flush()
        return User(
            id=orm_user.id,
            email=orm_user.email,
            password_hash=orm_user.password_hash,
            created_at=orm_user.created_at,
        )

    async def get(self, user_id: UUID) -> User | None:
        orm_user = await self.session.get(ORMUser, user_id)
        if orm_user is None:
            return None
        return User(
            id=orm_user.id,
            email=orm_user.email,
            password_hash=orm_user.password_hash,
            created_at=orm_user.created_at,
        )

    async def get_by_email(self, email: EmailStr) -> User | None:
        stmt = select(ORMUser).where(ORMUser.email == email)  # type: ignore
        result = await self.session.execute(stmt)
        orm_user = result.scalar_one_or_none()
        if orm_user is None:
            return None
        return User(
            id=orm_user.id,
            email=orm_user.email,
            password_hash=orm_user.password_hash,
            created_at=orm_user.created_at,
        )

    async def delete(self, user_id: UUID) -> None:
        orm_user = await self.session.get(ORMUser, user_id)
        await self.session.delete(orm_user)
        await self.session.flush()

    async def update(self, user_id: UUID, password_hash: str) -> User | None:
        orm_user = await self.session.get(ORMUser, user_id)
        if orm_user is None:
            return None
        orm_user.password_hash = password_hash
        await self.session.commit()
        return User(
            id=orm_user.id,
            email=orm_user.email,
            password_hash=orm_user.password_hash,
            created_at=orm_user.created_at,
        )
