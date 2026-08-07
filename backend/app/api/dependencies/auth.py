from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.application.exceptions import InfrastructureError
from app.application.ports.services import TokenService
from app.application.ports.unit_of_work import UnitOfWork
from app.domain.user import User

from .database import get_uow
from .infrastructure import get_token_service

bearer_scheme = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    token_service: TokenService = Depends(get_token_service),
    uow: UnitOfWork = Depends(get_uow),
) -> User:
    try:
        user_id = token_service.verify(credentials.credentials)
    except InfrastructureError:
        raise HTTPException(
            status_code=401,
            detail="Invalid authentication token",
        )
    user = await uow.users.get(user_id)
    if user is None:
        raise HTTPException(
            status_code=404,
            detail="Authentication required",
        )
    return user
