import pytest
from fastapi import HTTPException

from src.dto.schemas import UserAdminUpdateDTO, UserUpdateDTO
from src.models.entities import Role, User
from src.services.user_service import UserService


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
    updated = UserService(db_session).update_self(
        user_context["user"],
        UserUpdateDTO(full_name="Updated User Name"),
    )
    assert updated.full_name == "Updated User Name"


def test_admin_can_update_user_role_and_block_flag(db_session, user_context):
    updated = UserService(db_session).update_by_admin(
        user_context["user"].id,
        UserAdminUpdateDTO(role=Role.MODERATOR, is_blocked=True),
    )
    assert updated.role == Role.MODERATOR
    assert updated.is_blocked is True


def test_delete_user_without_relations(db_session, user_context):
    service = UserService(db_session)
    service.delete(user_context["user"].id)
    with pytest.raises(HTTPException):
        service.get_by_id(user_context["user"].id)
