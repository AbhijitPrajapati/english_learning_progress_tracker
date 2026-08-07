import logging

from fastapi import Request
from fastapi.responses import JSONResponse

from app.application.exceptions import ApplicationError
from app.application.use_cases.auth.exceptions import (
    EmailAlreadyRegistered,
    InvalidCredentials,
    UserNotFound,
)

logger = logging.getLogger(__name__)


async def base_exception(request: Request, exc: Exception) -> JSONResponse:
    """Consistent response for unexpected server errors."""
    logger.exception(
        "Unexpected backend error",
        extra={"path": request.url.path, "detail": str(exc)},
    )
    return JSONResponse(status_code=500, content={"detail": "Internal server error"})


async def application_error(request: Request, exc: ApplicationError) -> JSONResponse:
    logger.info(
        "Backend application error",
        extra={"path": request.url.path, "detail": str(exc)},
    )
    return JSONResponse(
        status_code=503, content={"detail": "Something went wrong. Please try again."}
    )


async def invalid_credentials(
    request: Request, exc: InvalidCredentials
) -> JSONResponse:
    logger.info(
        "Invalid credentials",
        extra={"path": request.url.path, "detail": str(exc)},
    )
    return JSONResponse(
        status_code=401, content={"detail": "Email or password is incorrect."}
    )


async def email_already_registered(
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


async def user_not_found(request: Request, exc: UserNotFound) -> JSONResponse:
    logger.info(
        "User not found",
        extra={"path": request.url.path, "detail": str(exc)},
    )
    return JSONResponse(
        status_code=404,
        content={"detail": "An account with this email does not exist."},
    )
