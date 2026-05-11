import pytest

from src.adapters.http.security import PasswordManagerAdapter, TokenServiceAdapter
from src.adapters.persistence.mongodb.repositories import MongoUnitOfWork, MongoUserRepository
from src.application.common.errors import ConflictError, ForbiddenError, UnauthorizedError
from src.application.services.auth import AuthApplicationService


def build_service(db_session):
    return AuthApplicationService(
        users=MongoUserRepository(db_session),
        uow=MongoUnitOfWork(db_session),
        password_manager=PasswordManagerAdapter(),
        token_service=TokenServiceAdapter(),
    )


def test_register_creates_user(db_session):
    service = build_service(db_session)
    user = service.register(email="new@example.com", full_name="New User", password="password123")
    assert user.id is not None
    assert user.email == "new@example.com"


def test_register_rejects_duplicate_email(db_session):
    service = build_service(db_session)
    service.register(email="dup@example.com", full_name="First User", password="password123")
    with pytest.raises(ConflictError):
        service.register(email="dup@example.com", full_name="Second User", password="password123")


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
    service = build_service(db_session)
    service.register(email="login1@example.com", full_name="Login User", password="password123")
    if should_pass:
        token = service.login(email=email, password=password)
        assert token
    else:
        with pytest.raises(UnauthorizedError):
            service.login(email=email or "empty@example.com", password=password)


def test_login_rejects_blocked_user(db_session):
    service = build_service(db_session)
    user = service.register(
        email="blocked@example.com",
        full_name="Blocked User",
        password="password123",
    )
    user.is_blocked = True
    db_session.commit()
    with pytest.raises(ForbiddenError):
        service.login(email="blocked@example.com", password="password123")
