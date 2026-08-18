from fastapi import Request, Response

SESSION_COOKIE_NAME = "session"


def is_secure_request(request: Request) -> bool:
    forwarded_protocol = request.headers.get("x-forwarded-proto")
    return forwarded_protocol == "https" or request.url.scheme == "https"


def set_session_cookie(response: Response, token: str, *, secure: bool) -> None:
    response.set_cookie(
        key=SESSION_COOKIE_NAME,
        value=token,
        httponly=True,
        secure=secure,
        samesite="lax",
        path="/",
    )


def clear_session_cookie(response: Response, *, secure: bool) -> None:
    response.delete_cookie(
        key=SESSION_COOKIE_NAME,
        httponly=True,
        secure=secure,
        samesite="lax",
        path="/",
    )
