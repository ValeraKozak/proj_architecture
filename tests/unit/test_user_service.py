import pytest

from src.adapters.persistence.mongodb.repositories import MongoUnitOfWork, MongoUserRepository
from src.application.common.errors import NotFoundError
from src.application.services.users import UserApplicationService
from src.models.entities import Role, User


def build_service(db_session):
    return UserApplicationService(
        users=MongoUserRepository(db_session),
        uow=MongoUnitOfWork(db_session),
    )


@pytest.fixture
def user_context(db_session):
    admin = User(
        email="admin@test.com",
        full_name="Admin User",
        password_hash="hashed",
        role=Role.ADMIN,
    )
    user = User(
        email="user@test.com",
        full_name="Simple User",
        password_hash="hashed",
        role=Role.USER,
    )
    db_session.add_all([admin, user])
    db_session.commit()
    db_session.refresh(admin)
    db_session.refresh(user)
    return {"admin": admin, "user": user}


def test_update_self_profile(db_session, user_context):
    updated = build_service(db_session).update_self(
        user_context["user"],
        full_name="Updated User Name",
    )
    assert updated.full_name == "Updated User Name"


def test_admin_can_update_user_role_and_block_flag(db_session, user_context):
    updated = build_service(db_session).update_by_admin(
        user_context["user"].id,
        role=Role.MODERATOR,
        is_blocked=True,
    )
    assert updated.role == Role.MODERATOR
    assert updated.is_blocked is True


def test_delete_user_without_relations(db_session, user_context):
    service = build_service(db_session)
    service.delete(user_context["user"].id)
    with pytest.raises(NotFoundError):
        service.get_by_id(user_context["user"].id)
