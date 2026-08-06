class TokenServiceError(Exception):
    pass


class InvalidToken(TokenServiceError):
    pass
