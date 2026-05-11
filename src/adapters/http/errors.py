from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse

from src.application.common.errors import (
    ApplicationError,
    ConflictError,
    ForbiddenError,
    NotFoundError,
    UnauthorizedError,
    ValidationError,
)


def to_http_exception(exc: ApplicationError) -> HTTPException:
    status_code = 500
    if isinstance(exc, ValidationError):
        status_code = 400
    elif isinstance(exc, UnauthorizedError):
        status_code = 401
    elif isinstance(exc, ForbiddenError):
        status_code = 403
    elif isinstance(exc, NotFoundError):
        status_code = 404
    elif isinstance(exc, ConflictError):
        status_code = 409
    return HTTPException(status_code=status_code, detail=str(exc))


async def handle_application_error(_: Request, exc: ApplicationError) -> JSONResponse:
    http_exc = to_http_exception(exc)
    return JSONResponse(status_code=http_exc.status_code, content={"detail": http_exc.detail})
