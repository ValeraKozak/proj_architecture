from typing import Protocol


class PasswordManagerPort(Protocol):
    def hash_password(self, password: str) -> str: ...

    def verify_password(self, plain_password: str, hashed_password: str) -> bool: ...


class TokenServicePort(Protocol):
    def create_access_token(self, subject: str) -> str: ...
