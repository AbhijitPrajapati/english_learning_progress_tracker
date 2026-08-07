from fastapi import FastAPI

from app.application.exceptions import ApplicationError
from app.application.use_cases.auth.exceptions import (
    EmailAlreadyRegistered,
    InvalidCredentials,
    UserNotFound,
)

from .handlers import (
    application_error,
    base_exception,
    email_already_registered,
    invalid_credentials,
    user_not_found,
)


def register_exception_handlers(app: FastAPI):
    app.add_exception_handler(Exception, base_exception)
    app.add_exception_handler(ApplicationError, application_error)  # type: ignore
    app.add_exception_handler(EmailAlreadyRegistered, email_already_registered)  # type: ignore
    app.add_exception_handler(InvalidCredentials, invalid_credentials)  # type: ignore
    app.add_exception_handler(UserNotFound, user_not_found)  # type: ignore
