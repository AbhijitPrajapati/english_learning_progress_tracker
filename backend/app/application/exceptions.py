class ApplicationError(Exception):
    """Base for expected application failures"""


class InfrastructureError(Exception):
    """Base error port for infrastructure failures"""
