from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.application.exceptions import InvalidAudio
from app.application.use_cases.account.exceptions import InvalidCurrentPassword
from app.application.use_cases.auth.exceptions import (
    EmailAlreadyRegistered,
    InvalidCredentials,
    InvalidToken,
)
from app.application.use_cases.speeches.exceptions import (
    AnalysisQuotaReached,
    SpeechNotFound,
)

from .model import ErrorBody, ErrorCode
from .util import log_exception


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(Exception)
    async def base_exception(request: Request, exc: Exception) -> JSONResponse:
        log_exception("Unexpected server error", exc, request, error=True)
        return JSONResponse(
            status_code=500,
            content=ErrorBody(
                detail="Something went wrong. Please try again.",
                code=ErrorCode.UNEXPECTED,
            ).model_dump(mode="json"),
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
            ).model_dump(mode="json"),
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
            ).model_dump(mode="json"),
        )

    @app.exception_handler(InvalidToken)
    async def invalid_token(request: Request, exc: InvalidToken) -> JSONResponse:
        log_exception("Invalid token", exc, request)
        return JSONResponse(
            status_code=401,
            content=ErrorBody(
                detail="Authentication token is invalid.",
                code=ErrorCode.INVALID_TOKEN,
            ).model_dump(mode="json"),
        )

    @app.exception_handler(SpeechNotFound)
    async def speech_not_found(request: Request, exc: SpeechNotFound) -> JSONResponse:
        log_exception("Speech not found", exc, request)
        return JSONResponse(
            status_code=404,
            content=ErrorBody(
                detail="Speech not found.",
                code=ErrorCode.SPEECH_NOT_FOUND,
            ).model_dump(mode="json"),
        )

    @app.exception_handler(InvalidCurrentPassword)
    async def invalid_current_password(
        request: Request, exc: InvalidCurrentPassword
    ) -> JSONResponse:
        log_exception("Invalid current password", exc, request)
        return JSONResponse(
            status_code=400,
            content=ErrorBody(
                detail="Current password is incorrect.",
                code=ErrorCode.INVALID_CURRENT_PASSWORD,
            ).model_dump(mode="json"),
        )

    @app.exception_handler(InvalidAudio)
    async def invalid_audio(request: Request, exc: InvalidAudio) -> JSONResponse:
        log_exception("Invalid audio upload", exc, request)
        return JSONResponse(
            status_code=400,
            content=ErrorBody(
                detail=str(exc) or "Audio upload is invalid.",
                code=ErrorCode.INVALID_AUDIO,
            ).model_dump(mode="json"),
        )

    @app.exception_handler(RequestValidationError)
    async def validation_error(
        request: Request, exc: RequestValidationError
    ) -> JSONResponse:
        log_exception("Request validation failed", exc, request)
        return JSONResponse(
            status_code=422,
            content=ErrorBody(
                detail="Request validation failed.",
                code=ErrorCode.VALIDATION_ERROR,
            ).model_dump(mode="json"),
        )

    @app.exception_handler(AnalysisQuotaReached)
    async def analysis_quota_reached(
        request: Request, exc: RequestValidationError
    ) -> JSONResponse:
        log_exception("Analysis quota reached", exc, request)
        return JSONResponse(
            status_code=429,
            content=ErrorBody(
                detail="Analysis quota reached.",
                code=ErrorCode.QUOTA_REACHED,
            ).model_dump(mode="json"),
        )
