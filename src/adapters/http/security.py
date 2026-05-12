from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt

from src.adapters.http.dependencies import get_user_service
from src.application.common.errors import ForbiddenError, UnauthorizedError
from src.application.services import UserApplicationService
from src.core.config import get_settings
from src.domain.entities import Role, User

security = HTTPBearer()
optional_security = HTTPBearer(auto_error=False)


def decode_token_subject(token: str) -> str:
    settings = get_settings()
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        subject = payload.get("sub")
    except JWTError as exc:
        raise UnauthorizedError("Invalid authentication token") from exc
    if not subject or not isinstance(subject, str):
        raise UnauthorizedError("Invalid authentication token")
    return subject


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    service: UserApplicationService = Depends(get_user_service),
) -> User:
    email = decode_token_subject(credentials.credentials)
    user = service.get_by_email(email)
    if user is None:
        raise UnauthorizedError("User not found")
    return user


def get_optional_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(optional_security),
    service: UserApplicationService = Depends(get_user_service),
) -> User | None:
    if credentials is None:
        return None
    email = decode_token_subject(credentials.credentials)
    return service.get_by_email(email)


def require_role(*roles: Role):
    def dependency(current_user: User = Depends(get_current_user)) -> User:
        if current_user.role not in roles:
            raise ForbiddenError("You do not have permission to perform this action")
        return current_user

    return dependency
