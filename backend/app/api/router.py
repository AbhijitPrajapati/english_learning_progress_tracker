from fastapi import APIRouter

from app.api.routers.account import router as account_router
from app.api.routers.analytics import router as analytics_router
from app.api.routers.auth import router as auth_router
from app.api.routers.speeches import router as speeches_router

api_router = APIRouter(prefix="/api/v1")
api_router.include_router(auth_router)
api_router.include_router(speeches_router)
api_router.include_router(analytics_router)
api_router.include_router(account_router)
