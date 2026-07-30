import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from backend.api.routers.analytics import router as analytics_router
from backend.api.routers.auth import router as auth_router
from backend.api.routers.speeches import router as samples_router

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(auth_router)
app.include_router(samples_router)
app.include_router(analytics_router)


@app.exception_handler(Exception)
def base_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Consistent response for unexpected server errors."""
    logger.exception(
        "Unexpected backend error",
        extra={"path": request.url.path, "detail": str(exc)},
    )
    return JSONResponse(status_code=500, content={"detail": "Internal server error"})
