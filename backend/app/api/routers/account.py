from uuid import UUID

from fastapi import APIRouter, Depends, Request, Response, status

from app.api.authentication import clear_session_cookie, is_secure_request
from app.api.dependencies.application import ContainerDependency
from app.api.dependencies.current_user import get_current_user
from app.api.responses import error_responses
from app.api.schemas.auth import ChangePasswordRequest
from app.domain.user import NewPassword

router = APIRouter(prefix="/account", tags=["account"])


@router.patch(
    "/password",
    status_code=status.HTTP_204_NO_CONTENT,
    operation_id="changePassword",
    responses=error_responses(400, 401, 422, 500),
)
async def change_password(
    request: ChangePasswordRequest,
    container: ContainerDependency,
    user_id: UUID = Depends(get_current_user),
) -> None:
    await container.change_password.execute(
        user_id,
        request.current_password,
        NewPassword(request.new_password),
    )


@router.delete(
    "",
    status_code=status.HTTP_204_NO_CONTENT,
    operation_id="deleteAccount",
    responses=error_responses(401, 500),
)
async def delete_account(
    http_request: Request,
    response: Response,
    container: ContainerDependency,
    user_id: UUID = Depends(get_current_user),
) -> None:
    await container.delete_user.execute(user_id)
    clear_session_cookie(response, secure=is_secure_request(http_request))
