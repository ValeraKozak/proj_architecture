import logging

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from src.dto.schemas import UserAdminUpdateDTO, UserUpdateDTO
from src.models.entities import Role, User
from src.repositories.user_repository import UserRepository

logger = logging.getLogger(__name__)


class UserService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.users = UserRepository(db)

    def list_all(self) -> list[User]:
        return self.users.list_all()

    def get_by_id(self, user_id: int) -> User:
        user = self.users.get(user_id)
        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return user

    def update_self(self, current_user: User, payload: UserUpdateDTO) -> User:
        current_user.full_name = payload.full_name.strip()
        self.db.commit()
        self.db.refresh(current_user)
        logger.info("User profile updated user_id=%s", current_user.id)
        return current_user

    def update_by_admin(self, user_id: int, payload: UserAdminUpdateDTO) -> User:
        user = self.get_by_id(user_id)
        data = payload.model_dump(exclude_none=True)
        if "role" in data and data["role"] == Role.ADMIN and user.role != Role.ADMIN:
            logger.info("User promoted to admin user_id=%s", user.id)
        for field, value in data.items():
            setattr(user, field, value.strip() if isinstance(value, str) else value)
        self.db.commit()
        self.db.refresh(user)
        return user

    def delete(self, user_id: int) -> None:
        user = self.get_by_id(user_id)
        if user.listings or user.sent_messages or user.received_messages:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Cannot delete user with related listings or messages",
            )
        self.users.delete(user)
        self.db.commit()
        logger.info("User deleted user_id=%s", user_id)
