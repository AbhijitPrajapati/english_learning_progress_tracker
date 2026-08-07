from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.domain.user import User

from .application import GetUserFromToken, get_user_from_token

bearer_scheme = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    get_user_from_token: GetUserFromToken = Depends(get_user_from_token),
) -> User:
    return await get_user_from_token.execute(credentials.credentials)
