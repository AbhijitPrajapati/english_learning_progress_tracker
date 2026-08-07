class ApplicationError(Exception):
    """Base for expected application failures"""


class InfrastructureError(ApplicationError):
    """Base error port for infrastructure failures"""
