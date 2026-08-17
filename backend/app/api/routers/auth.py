from uuid import UUID

from fastapi import APIRouter, Depends, Request, Response, status

from app.api.authentication import (
    clear_session_cookie,
    is_secure_request,
    set_session_cookie,
)
from app.api.dependencies.application import ContainerDependency
from app.api.dependencies.current_user import get_current_user
from app.api.mappers import to_login_response, to_register_response
from app.api.responses import error_responses
from app.api.schemas.auth import (
    LoginRequest,
    LoginResponse,
    RegisterRequest,
    RegisterResponse,
)
from app.domain.user import EmailAddress, NewPassword

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post(
    "/login",
    response_model=LoginResponse,
    operation_id="login",
    responses=error_responses(401, 422, 500),
)
async def login(
    request: LoginRequest,
    http_request: Request,
    response: Response,
    container: ContainerDependency,
) -> LoginResponse:
    session = await container.login.execute(
        EmailAddress(str(request.email)), request.password
    )
    set_session_cookie(
        response,
        session.session_token,
        secure=is_secure_request(http_request),
    )
    return to_login_response(session)


@router.post(
    "/register",
    response_model=RegisterResponse,
    status_code=status.HTTP_201_CREATED,
    operation_id="register",
    responses=error_responses(409, 422, 500),
)
async def register(
    request: RegisterRequest,
    container: ContainerDependency,
) -> RegisterResponse:
    user = await container.register_user.execute(
        EmailAddress(str(request.email)), NewPassword(request.password)
    )
    return to_register_response(user)


@router.get(
    "/session",
    response_model=LoginResponse,
    operation_id="getSession",
    responses=error_responses(401, 500),
)
async def get_session(user_id: UUID = Depends(get_current_user)) -> LoginResponse:
    return LoginResponse(user_id=user_id)


@router.post(
    "/logout",
    status_code=status.HTTP_204_NO_CONTENT,
    operation_id="logout",
    responses=error_responses(500),
)
async def logout(http_request: Request, response: Response) -> None:
    clear_session_cookie(response, secure=is_secure_request(http_request))
