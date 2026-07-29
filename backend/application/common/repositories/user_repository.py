from typing import Protocol

from pydantic import EmailStr

from domain.user import User
from domain.value_objects import UserId

from .models import NewUser


class UserRepository(Protocol):
    async def create(self, user: NewUser) -> User: ...
    async def get(self, user_id: UserId) -> User | None: ...
    async def get_by_email(self, email: EmailStr) -> User | None: ...
    async def delete(self, user_id: UserId) -> None: ...
