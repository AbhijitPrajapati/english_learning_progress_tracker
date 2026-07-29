from fastapi import APIRouter, Depends, HTTPException

from api.dependencies.application import (
    AuthenticateUser,
    RegisterUser,
    get_authenticate_user,
    get_register_user,
)
from api.dependencies.auth import TokenService, get_token_service
from api.schemas.auth import (
    LoginRequest,
    LoginResponse,
    RegisterRequest,
    RegisterResponse,
)

router = APIRouter(prefix="/auth")


@router.post("/login", response_model=LoginResponse)
async def login(
    request: LoginRequest,
    authenticate_user: AuthenticateUser = Depends(get_authenticate_user),
    token_service: TokenService = Depends(get_token_service),
) -> LoginResponse:
    user = await authenticate_user.execute(request.email, password=request.password)
    if user is None:
        raise HTTPException(status_code=000, detail="Authentication failed")
    token = token_service.issue(user.id)
    return LoginResponse(access_token=token, user_id=user.id.value)


@router.post("/register", response_model=RegisterResponse)
async def register(
    request: RegisterRequest, register_user: RegisterUser = Depends(get_register_user)
) -> RegisterResponse:
    try:
        user = await register_user.execute(request.email, request.password)
    except Exception:  # noqa: BLE001
        raise HTTPException(status_code=000, detail="user exists already")
    return RegisterResponse(
        id=user.id.value, email=user.email, created_at=user.created_at
    )
