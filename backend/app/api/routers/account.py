from fastapi import APIRouter, Depends, status

from app.api.dependencies.application import (
    DeleteUser,
    get_delete_user,
)
from app.api.dependencies.current_user import get_current_user
from app.domain.user import User

router = APIRouter(prefix="/account")

@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
async def delete(delete_user: DeleteUser = Depends(get_delete_user), current_user: User = Depends(get_current_user)) -> None:
    await delete_user.execute(current_user.id)