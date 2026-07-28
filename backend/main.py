import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from .config import BackendConfig
from .database import SessionManager
from .routers import sessions_router
from .transcription import WhisperAdapter

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger(__name__)


config = BackendConfig()  # type: ignore


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.transcriber = WhisperAdapter(config.whisper)
    app.state.session_manager = SessionManager(config.postgres)
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(sessions_router)


@app.exception_handler(Exception)
def base_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Consistent response for unexpected server errors."""
    logger.exception(
        "Unexpected backend error",
        extra={"path": request.url.path, "detail": str(exc)},
    )
    return JSONResponse(status_code=500, content={"detail": "Internal server error"})
