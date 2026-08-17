from typing import Any, Literal

from app.api.exceptions.model import ErrorBody

type ErrorStatus = Literal[400, 401, 404, 409, 422, 500]
type AdditionalResponses = dict[int | str, dict[str, Any]]


def error_responses(*statuses: ErrorStatus) -> AdditionalResponses:
    descriptions: dict[ErrorStatus, str] = {
        400: "Invalid request",
        401: "Authentication required or invalid",
        404: "Resource not found",
        409: "Resource conflict",
        422: "Request validation failed",
        500: "Unexpected server error",
    }
    return {
        status: {"model": ErrorBody, "description": descriptions[status]}
        for status in statuses
    }
