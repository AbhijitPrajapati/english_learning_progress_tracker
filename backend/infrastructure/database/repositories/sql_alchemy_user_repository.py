from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from application.common.repositories.user_repository import NewUser, UserRepository
from domain.user import User
from domain.value_objects import Email, UserId
from infrastructure.database.models import User as ORMUser


class SQLAlchemyUserRepository(UserRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, user: NewUser) -> User:
        orm_user = ORMUser(email=user.email, password_hash=user.password_hash)
        self.session.add(orm_user)
        await self.session.flush()
        return User(
            id=orm_user.id,
            email=orm_user.email,
            password_hash=orm_user.password_hash,
            created_at=orm_user.created_at,
        )

    async def get(self, user_id: UserId) -> User | None:
        orm_user = await self.session.get(ORMUser, user_id)
        if orm_user is None:
            return None
        return User(
            id=orm_user.id,
            email=orm_user.email,
            password_hash=orm_user.password_hash,
            created_at=orm_user.created_at,
        )

    async def get_by_email(self, email: Email) -> User | None:
        stmt = select(User).where(User.email == email)  # type: ignore
        result = await self.session.execute(stmt)
        orm_user = result.first()
        if orm_user is None:
            return None
        return User(
            id=orm_user.id,
            email=orm_user.email,
            password_hash=orm_user.password_hash,
            created_at=orm_user.created_at,
        )

    async def delete(self, user_id: UserId) -> None:
        orm_user = await self.session.get(ORMUser, user_id)
        await self.session.delete(orm_user)
        await self.session.flush()
