from typing import Protocol

from domain.user import CreateUser, User
from domain.value_objects import UserId


class UserRepository(Protocol):
    async def create(self, user: CreateUser) -> User: ...
    async def get(self, user_id: UserId) -> User | None: ...
    async def delete(self, user_id: UserId) -> None: ...
