from fastapi import HTTPException

from src.application.common.errors import ApplicationError


def translate_application_error(exc: ApplicationError) -> HTTPException:
    return HTTPException(status_code=exc.status_code, detail=exc.detail)
