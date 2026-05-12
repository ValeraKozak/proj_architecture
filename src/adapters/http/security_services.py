import hashlib
import hmac
import secrets
from datetime import UTC, datetime, timedelta

from jose import jwt

from src.application.ports.security import PasswordManagerPort, TokenServicePort
from src.core.config import get_settings


def hash_password(password: str) -> str:
    salt = secrets.token_hex(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode(), salt.encode(), 100_000).hex()
    return f"{salt}${digest}"


def verify_password(plain_password: str, hashed_password: str) -> bool:
    salt, stored_digest = hashed_password.split("$", maxsplit=1)
    candidate = hashlib.pbkdf2_hmac("sha256", plain_password.encode(), salt.encode(), 100_000).hex()
    return hmac.compare_digest(candidate, stored_digest)


def create_access_token(subject: str) -> str:
    settings = get_settings()
    expires_at = datetime.now(UTC) + timedelta(minutes=settings.access_token_expire_minutes)
    payload = {"sub": subject, "exp": expires_at}
    return jwt.encode(payload, settings.secret_key, algorithm=settings.algorithm)


class PasswordManagerAdapter(PasswordManagerPort):
    def hash_password(self, password: str) -> str:
        return hash_password(password)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return verify_password(plain_password, hashed_password)


class TokenServiceAdapter(TokenServicePort):
    def create_access_token(self, subject: str) -> str:
        return create_access_token(subject)
