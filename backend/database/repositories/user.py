from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from database.models.user import User as ORMUser


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    # async def create(self, email: str, password_hash: str) -> User:
    #     orm_user = ORMUser(email=email, password_hash=password_hash)
    #     self.session.add(orm_user)
    #     await self.session.flush()
    #     return User.model_validate(orm_user)

    # async def get(self, user_id: UUID) -> User | None:
    #     orm_user = await self.session.get(ORMUser, user_id)
    #     if orm_user is None:
    #         return None
    #     return User.model_validate(orm_user)
