from uuid import UUID

from fastapi import Depends
from fastapi.security import APIKeyCookie

from app.api.authentication import SESSION_COOKIE_NAME
from app.api.dependencies.application import ContainerDependency
from app.application.use_cases.auth.exceptions import InvalidToken

session_cookie = APIKeyCookie(name=SESSION_COOKIE_NAME, auto_error=False)


async def get_current_user(
    container: ContainerDependency,
    token: str | None = Depends(session_cookie),
) -> UUID:
    if token is None:
        raise InvalidToken()
    return await container.get_user_id_from_token.execute(token)
