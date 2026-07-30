from backend.application.exception_base import ApplicationError


class InvalidCredentials(ApplicationError):
    pass


class UserNotFound(ApplicationError):
    pass


class EmailAlreadyRegistered(ApplicationError):
    pass
