class ApplicationError(Exception):
    """Base for expected application failures"""


class InvalidAudio(ApplicationError):
    """The submitted sample cannot be processed as supported audio."""
