from typing import Protocol

from domain.value_objects import UserId


class TokenService(Protocol):
    def issue(self, user_id: UserId) -> str: ...
    def verify(self, token: str) -> UserId: ...
