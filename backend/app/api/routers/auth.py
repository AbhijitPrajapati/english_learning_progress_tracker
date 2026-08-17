from fastapi import APIRouter, Depends

from app.api.dependencies.application import (
    AuthenticateUser,
    IssueToken,
    RegisterUser,
    get_authenticate_user,
    get_issue_token,
    get_register_user,
)
from app.application.use_cases.auth.models import (
    RegisterUserResponse,
    TokenResponse,
    UserCredentials,
)

router = APIRouter(prefix="/auth")


@router.post("/login", response_model=TokenResponse)
async def login(
    request: UserCredentials,
    authenticate_user: AuthenticateUser = Depends(get_authenticate_user),
    issue_token: IssueToken = Depends(get_issue_token),
) -> TokenResponse:
    user_id = await authenticate_user.execute(request)
    return await issue_token.execute(user_id)


@router.post("/register", response_model=RegisterUserResponse)
async def register(
    request: UserCredentials, register_user: RegisterUser = Depends(get_register_user)
) -> RegisterUserResponse:
    return await register_user.execute(request)

