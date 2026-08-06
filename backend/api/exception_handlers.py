import logging

from fastapi import Request
from fastapi.responses import JSONResponse

logger = logging.getLogger(__name__)


def base_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Consistent response for unexpected server errors."""
    logger.exception(
        "Unexpected backend error",
        extra={"path": request.url.path, "detail": str(exc)},
    )
    return JSONResponse(status_code=500, content={"detail": "Internal server error"})
