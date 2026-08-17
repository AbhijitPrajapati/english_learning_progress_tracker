from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.exceptions import register_exception_handlers
from app.api.routers.account import router as account_router
from app.api.routers.analytics import router as analytics_router
from app.api.routers.auth import router as auth_router
from app.api.routers.speeches import router as speeches_router
from app.infrastructure.composition import (
    InfrastructureComposition,
    InfrastructureSettings,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Construct application infrastrucutre on app startup"""
    infrastructure_settings = InfrastructureSettings()  # type: ignore
    app.state.composition = InfrastructureComposition(infrastructure_settings)
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(auth_router)
app.include_router(speeches_router)
app.include_router(analytics_router)
app.include_router(account_router)

register_exception_handlers(app)
