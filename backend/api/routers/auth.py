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
from application.errors.auth import InvalidCredentials
from application.errors.users import EmailAlreadyRegistered, UserNotFound
from domain.value_objects import Email

router = APIRouter(prefix="/auth")


@router.post("/login", response_model=LoginResponse)
async def login(
    request: LoginRequest,
    authenticate_user: AuthenticateUser = Depends(get_authenticate_user),
    token_service: TokenService = Depends(get_token_service),
) -> LoginResponse:
    try:
        user = await authenticate_user.execute(
            Email(value=request.email), password=request.password
        )
    except UserNotFound:
        raise HTTPException(status_code=404, detail="User not found")
    except InvalidCredentials:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = token_service.issue(user.id)
    return LoginResponse(access_token=token, user_id=user.id.value)


@router.post("/register", response_model=RegisterResponse)
async def register(
    request: RegisterRequest, register_user: RegisterUser = Depends(get_register_user)
) -> RegisterResponse:
    try:
        user = await register_user.execute(Email(value=request.email), request.password)
    except EmailAlreadyRegistered:
        raise HTTPException(status_code=409, detail="Email already registered")
    return RegisterResponse(
        id=user.id.value, email=user.email.value, created_at=user.created_at
    )
