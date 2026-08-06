import logging

from fastapi import Request
from fastapi.responses import JSONResponse

from app.application.exceptions import ApplicationError
from app.application.use_cases.auth.exceptions import (
    EmailAlreadyRegistered,
    InvalidCredentials,
)

logger = logging.getLogger(__name__)


def base_exception(request: Request, exc: Exception) -> JSONResponse:
    """Consistent response for unexpected server errors."""
    logger.exception(
        "Unexpected backend error",
        extra={"path": request.url.path, "detail": str(exc)},
    )
    return JSONResponse(status_code=500, content={"detail": "Internal server error"})


def application_error(request: Request, exc: ApplicationError) -> JSONResponse:
    logger.exception(
        "Backend application error",
        extra={"path": request.url.path, "detail": str(exc)},
    )
    return JSONResponse(
        status_code=503, content={"detail": "Something went wrong. Please try again."}
    )


def invalid_credentials(request: Request, exc: InvalidCredentials) -> JSONResponse:
    logger.info(
        "Invalid credentials",
        extra={"path": request.url.path, "detail": str(exc)},
    )
    return JSONResponse(
        status_code=401, content={"detail": "Email or password is incorrect."}
    )


def email_already_registered(
    request: Request, exc: EmailAlreadyRegistered
) -> JSONResponse:
    logger.info(
        "Email already registered",
        extra={"path": request.url.path, "detail": str(exc)},
    )
    return JSONResponse(
        status_code=409,
        content={"detail": "An account with this email already exists."},
    )
