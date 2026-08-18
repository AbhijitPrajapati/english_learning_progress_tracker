import logging

from fastapi import Request

logger = logging.getLogger(__name__)


def log_exception(msg: str, exc: Exception, request: Request, error=False) -> None:
    if error:
        logger.error(msg, extra={"path": request.url.path}, exc_info=exc)
    else:
        logger.info(msg, extra={"path": request.url.path, "detail": str(exc)})
