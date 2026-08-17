from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.exceptions import register_exception_handlers
from app.api.router import api_router
from app.container import ApplicationContainer
from app.settings import InfrastructureSettings


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None]:
    """Construct application infrastructure on app startup."""
    infrastructure_settings = InfrastructureSettings()  # type: ignore
    container = ApplicationContainer(infrastructure_settings)
    app.state.container = container
    try:
        yield
    finally:
        await container.close()


app = FastAPI(
    title="English Learning Progress Tracker API",
    version="1.0.0",
    lifespan=lifespan,
)
app.include_router(api_router)

register_exception_handlers(app)
