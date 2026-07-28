import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from .config import BackendConfig
from .database import PostgresAdapter
from .transcription import WhisperAdapter

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan for managing dependencies
    """
    config = BackendConfig()  # type: ignore
    app.state.whisper = WhisperAdapter(config.whisper)
    app.state.database = PostgresAdapter(config.postgres)
    yield


app = FastAPI(lifespan=lifespan)


@app.exception_handler(Exception)
def base_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """
    Base handler for unexpected backend errors
    """
    logger.exception(
        "Unexpected backend error", extra={"path": request.url.path, "detail": str(exc)}
    )
    return JSONResponse(status_code=500, content={"detail": "Internal server error"})
