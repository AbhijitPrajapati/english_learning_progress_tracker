import logging

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.exceptions import InfrastructureError
from app.application.ports.repositories import NewUser, UpdateUser, UserRepository
from app.domain.user import Email, User, UserId
from app.infrastructure.database.models import User as ORMUser

logger = logging.getLogger(__name__)


class SQLAlchemyUserRepository(UserRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, user: NewUser) -> User:
        try:
            orm_user = ORMUser(email=user.email, password_hash=user.password_hash)
            self.session.add(orm_user)
            await self.session.flush()
            return User(
                id=orm_user.id,
                email=orm_user.email,
                password_hash=orm_user.password_hash,
                created_at=orm_user.created_at,
            )
        except SQLAlchemyError as e:
            logger.exception("Create user failed")
            raise InfrastructureError() from e

    async def get(self, user_id: UserId) -> User | None:
        try:
            orm_user = await self.session.get(ORMUser, user_id)
            if orm_user is None:
                return None
            return User(
                id=orm_user.id,
                email=orm_user.email,
                password_hash=orm_user.password_hash,
                created_at=orm_user.created_at,
            )
        except SQLAlchemyError as e:
            logger.exception("Get user by ID failed")
            raise InfrastructureError() from e

    async def get_by_email(self, email: Email) -> User | None:
        try:
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
        except SQLAlchemyError as e:
            logger.exception("Get user by email failed")
            raise InfrastructureError() from e

    async def delete(self, user_id: UserId) -> bool:
        try:
            orm_user = await self.session.get(ORMUser, user_id)
            if orm_user is None:
                return False
            await self.session.delete(orm_user)
            await self.session.flush()
            return True
        except SQLAlchemyError as e:
            logger.exception("Delete user failed")
            raise InfrastructureError() from e

    async def update(self, user_id: UserId, update_user: UpdateUser) -> User | None:
        try:
            orm_user = await self.session.get(ORMUser, user_id)
            if orm_user is None:
                return None
            orm_user.email = update_user.email
            await self.session.commit()
            return User(
                id=orm_user.id,
                email=orm_user.email,
                password_hash=orm_user.password_hash,
                created_at=orm_user.created_at,
            )
        except SQLAlchemyError as e:
            logger.exception("Update user failed")
            raise InfrastructureError() from e
