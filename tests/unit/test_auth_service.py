import pytest
from fastapi import HTTPException

from src.dto.schemas import UserCreateDTO, UserLoginDTO
from src.services.auth_service import AuthService


def test_register_creates_user(db_session):
    service = AuthService(db_session)
    user = service.register(
        UserCreateDTO(email="new@example.com", full_name="New User", password="password123")
    )
    assert user.id is not None
    assert user.email == "new@example.com"


def test_register_rejects_duplicate_email(db_session):
    service = AuthService(db_session)
    service.register(
        UserCreateDTO(email="dup@example.com", full_name="First User", password="password123")
    )
    with pytest.raises(HTTPException):
        service.register(
            UserCreateDTO(email="dup@example.com", full_name="Second User", password="password123")
        )


@pytest.mark.parametrize(
    ("email", "password", "should_pass"),
    [
        ("login1@example.com", "password123", True),
        ("login2@example.com", "wrong-password", False),
        ("missing@example.com", "password123", False),
        ("LOGIN1@example.com", "password123", False),
        ("login1@example.com", "PASSWORD123", False),
        ("missing2@example.com", "bad", False),
        ("login1@example.com", "", False),
        ("", "password123", False),
        ("login1@example.com", "password124", False),
        ("login2@example.com", "password123", False),
    ],
)
def test_login_matrix(db_session, email, password, should_pass):
    service = AuthService(db_session)
    service.register(
        UserCreateDTO(email="login1@example.com", full_name="Login User", password="password123")
    )
    if should_pass:
        token = service.login(UserLoginDTO(email=email, password=password))
        assert token.access_token
    else:
        with pytest.raises(HTTPException):
            service.login(UserLoginDTO(email=email or "empty@example.com", password=password))


def test_login_rejects_blocked_user(db_session):
    service = AuthService(db_session)
    user = service.register(
        UserCreateDTO(email="blocked@example.com", full_name="Blocked User", password="password123")
    )
    user.is_blocked = True
    db_session.commit()
    with pytest.raises(HTTPException):
        service.login(UserLoginDTO(email="blocked@example.com", password="password123"))
