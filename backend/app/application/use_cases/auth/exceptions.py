from app.application.exceptions import ApplicationError


class InvalidCredentials(ApplicationError):
    pass


class UserNotFound(ApplicationError):
    pass


class EmailAlreadyRegistered(ApplicationError):
    pass
