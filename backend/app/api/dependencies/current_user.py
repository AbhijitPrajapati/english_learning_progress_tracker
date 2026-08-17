from uuid import UUID

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from .application import GetUserIdFromToken, get_user_id_from_token

bearer_scheme = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    get_user_from_token: GetUserIdFromToken = Depends(get_user_id_from_token),
) -> UUID:
    return await get_user_from_token.execute(credentials.credentials)
