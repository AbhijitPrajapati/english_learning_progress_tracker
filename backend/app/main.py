from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.exception_handlers import register_exception_handlers
from app.api.routers.analytics import router as analytics_router
from app.api.routers.auth import router as auth_router
from app.api.routers.speeches import router as samples_router
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
app.include_router(samples_router)
app.include_router(analytics_router)

register_exception_handlers(app)
