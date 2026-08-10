from app.application.exceptions import ApplicationError


class InvalidCredentials(ApplicationError):
    pass


class EmailAlreadyRegistered(ApplicationError):
    pass


class InvalidToken(ApplicationError):
    pass
