from uuid import UUID

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.ports.repositories import EmailConflictError, UserRepository
from app.domain.user import EmailAddress, User
from app.infrastructure.database.models import User as ORMUser


def to_domain(orm_user: ORMUser) -> User:
    return User(
        id=orm_user.id,
        email=EmailAddress(orm_user.email),
        password_hash=orm_user.password_hash,
        created_at=orm_user.created_at,
    )


class SQLAlchemyUserRepository(UserRepository):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, email: EmailAddress, password_hash: str) -> User:
        orm_user = ORMUser(email=email.value, password_hash=password_hash)
        self.session.add(orm_user)
        try:
            await self.session.flush()
        except IntegrityError as error:
            raise EmailConflictError() from error
        return to_domain(orm_user)

    async def get(self, user_id: UUID) -> User | None:
        orm_user = await self.session.get(ORMUser, user_id)
        return None if orm_user is None else to_domain(orm_user)

    async def get_by_email(self, email: EmailAddress) -> User | None:
        result = await self.session.execute(
            select(ORMUser).where(ORMUser.email == email.value)
        )
        orm_user = result.scalar_one_or_none()
        return None if orm_user is None else to_domain(orm_user)

    async def delete(self, user_id: UUID) -> bool:
        orm_user = await self.session.get(ORMUser, user_id)
        if orm_user is None:
            return False
        await self.session.delete(orm_user)
        await self.session.flush()
        return True

    async def update_password(self, user_id: UUID, password_hash: str) -> User | None:
        orm_user = await self.session.get(ORMUser, user_id)
        if orm_user is None:
            return None
        orm_user.password_hash = password_hash
        await self.session.flush()
        return to_domain(orm_user)
