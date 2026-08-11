from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.application.use_cases.auth.exceptions import (
    EmailAlreadyRegistered,
    InvalidCredentials,
    InvalidToken,
)

from .model import ErrorBody, ErrorCode
from .util import log_exception


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(Exception)
    async def base_exception(request: Request, exc: Exception) -> JSONResponse:
        log_exception("Unexpected server error", exc, request)
        return JSONResponse(
            status_code=500,
            content=ErrorBody(
                detail="Something went wrong. Please try again.",
                code=ErrorCode.UNEXPECTED,
            ).model_dump(),
        )

    @app.exception_handler(InvalidCredentials)
    async def invalid_credentials(
        request: Request, exc: InvalidCredentials
    ) -> JSONResponse:
        log_exception("Invalid credentials", exc, request)
        return JSONResponse(
            status_code=401,
            content=ErrorBody(
                detail="Email or password is incorrect.",
                code=ErrorCode.INVALID_CREDENTIALS,
            ).model_dump(),
        )

    @app.exception_handler(EmailAlreadyRegistered)
    async def email_already_registered(
        request: Request, exc: EmailAlreadyRegistered
    ) -> JSONResponse:
        log_exception("Email already registered", exc, request)
        return JSONResponse(
            status_code=409,
            content=ErrorBody(
                detail="An account with this email already exists.",
                code=ErrorCode.ALREADY_REGISTERED,
            ).model_dump(),
        )

    @app.exception_handler(InvalidToken)
    async def invalid_token(request: Request, exc: InvalidToken) -> JSONResponse:
        log_exception("Invalid token", exc, request)
        return JSONResponse(
            status_code=401,
            content=ErrorBody(
                detail="Authentication token is invalid.",
                code=ErrorCode.INVALID_TOKEN,
            ).model_dump(),
        )
