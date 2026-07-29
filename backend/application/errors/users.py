from .base import ApplicationError


class UserNotFound(ApplicationError):
    pass


class EmailAlreadyRegistered(ApplicationError):
    pass
