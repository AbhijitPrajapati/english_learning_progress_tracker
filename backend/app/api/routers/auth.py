from fastapi import APIRouter, Depends

from app.api.dependencies.application import (
    AuthenticateUser,
    IssueToken,
    RegisterUser,
    get_authenticate_user,
    get_issue_token,
    get_register_user,
)
from app.api.schemas.auth import (
    LoginRequest,
    LoginResponse,
    RegisterRequest,
    RegisterResponse,
)
from app.domain.user import Email

router = APIRouter(prefix="/auth")


@router.post("/login", response_model=LoginResponse)
async def login(
    request: LoginRequest,
    authenticate_user: AuthenticateUser = Depends(get_authenticate_user),
    issue_token: IssueToken = Depends(get_issue_token),
) -> LoginResponse:
    user = await authenticate_user.execute(
        Email(value=request.email), password=request.password
    )
    token = await issue_token.execute(user.id)
    return LoginResponse(access_token=token, user_id=user.id.value)


@router.post("/register", response_model=RegisterResponse)
async def register(
    request: RegisterRequest, register_user: RegisterUser = Depends(get_register_user)
) -> RegisterResponse:
    user = await register_user.execute(Email(value=request.email), request.password)
    return RegisterResponse(
        id=user.id.value, email=user.email.value, created_at=user.created_at
    )

