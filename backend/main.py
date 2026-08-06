from contextlib import asynccontextmanager

from fastapi import FastAPI

from backend.api.exception_handlers import base_exception
from backend.api.routers.analytics import router as analytics_router
from backend.api.routers.auth import router as auth_router
from backend.api.routers.speeches import router as samples_router
from backend.infrastructure.composition import (
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

app.add_exception_handler(Exception, base_exception)
