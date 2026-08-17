from uuid import UUID

from fastapi import APIRouter, Depends, status

from app.api.dependencies.application import (
    DeleteUser,
    get_delete_user,
)
from app.api.dependencies.current_user import get_current_user

router = APIRouter(prefix="/account")

@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
async def delete(delete_user: DeleteUser = Depends(get_delete_user), user_id: UUID = Depends(get_current_user)) -> None:
    await delete_user.execute(user_id)