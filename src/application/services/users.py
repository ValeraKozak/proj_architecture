import logging

from src.application.common.errors import ConflictError, NotFoundError
from src.application.ports.repositories import UnitOfWorkPort, UserRepositoryPort
from src.domain.entities import Role, User

logger = logging.getLogger(__name__)


class UserApplicationService:
    def __init__(self, users: UserRepositoryPort, uow: UnitOfWorkPort) -> None:
        self.users = users
        self.uow = uow

    def list_all(self) -> list[User]:
        return self.users.list_all()

    def get_by_id(self, user_id: int) -> User:
        user = self.users.get(user_id)
        if user is None:
            raise NotFoundError("User not found")
        return user

    def update_self(self, current_user: User, *, full_name: str) -> User:
        current_user.full_name = full_name.strip()
        self.uow.commit()
        self.uow.refresh(current_user)
        logger.info("User profile updated user_id=%s", current_user.id)
        return current_user

    def update_by_admin(
        self,
        user_id: int,
        *,
        full_name: str | None = None,
        role: Role | None = None,
        is_blocked: bool | None = None,
    ) -> User:
        user = self.get_by_id(user_id)
        if role == Role.ADMIN and user.role != Role.ADMIN:
            logger.info("User promoted to admin user_id=%s", user.id)
        if full_name is not None:
            user.full_name = full_name.strip()
        if role is not None:
            user.role = role
        if is_blocked is not None:
            user.is_blocked = is_blocked
        self.uow.commit()
        self.uow.refresh(user)
        return user

    def delete(self, user_id: int) -> None:
        user = self.get_by_id(user_id)
        if self.users.has_related_content(user_id):
            raise ConflictError("Cannot delete user with related listings or messages")
        self.users.delete(user)
        self.uow.commit()
        logger.info("User deleted user_id=%s", user_id)
