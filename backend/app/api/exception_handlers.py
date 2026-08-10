import logging

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.application.use_cases.auth.exceptions import (
    EmailAlreadyRegistered,
    InvalidCredentials,
    InvalidToken,
)

logger = logging.getLogger(__name__)


def register_exception_handlers(app: FastAPI) -> None:

    def log_exception(msg: str, exc: Exception, request: Request) -> None:
        logger.info(msg, extra={"path": request.url.path, "detail": str(exc)})

    @app.exception_handler(Exception)
    async def base_exception(request: Request, exc: Exception) -> JSONResponse:
        logger.error(
            "Unexpected server error", extra={"path": request.url.path}, exc_info=exc
        )
        return JSONResponse(
            status_code=500,
            content={"detail": "Something went wrong. Please try again."},
        )

    @app.exception_handler(InvalidCredentials)
    async def invalid_credentials(
        request: Request, exc: InvalidCredentials
    ) -> JSONResponse:
        log_exception("Invalid credentials", exc, request)
        return JSONResponse(
            status_code=401, content={"detail": "Email or password is incorrect."}
        )

    @app.exception_handler(EmailAlreadyRegistered)
    async def email_already_registered(
        request: Request, exc: EmailAlreadyRegistered
    ) -> JSONResponse:
        log_exception("Email already registered", exc, request)
        return JSONResponse(
            status_code=409,
            content={"detail": "An account with this email already exists."},
        )

    @app.exception_handler(InvalidToken)
    async def invalid_token(request: Request, exc: InvalidToken) -> JSONResponse:
        log_exception("Invalid token", exc, request)
        return JSONResponse(
            status_code=401,
            content={"detail": "Authentication token is invalid."},
        )
