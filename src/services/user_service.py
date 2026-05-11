from src.adapters.persistence.mongodb.repositories import MongoUnitOfWork, MongoUserRepository
from src.application.common.errors import ApplicationError
from src.application.services.users import UserApplicationService
from src.db.database import DatabaseSession
from src.dto.schemas import UserAdminUpdateDTO, UserUpdateDTO
from src.models.entities import User
from src.services._legacy import translate_application_error


class UserService:
    def __init__(self, db: DatabaseSession) -> None:
        self.service = UserApplicationService(
            users=MongoUserRepository(db),
            uow=MongoUnitOfWork(db),
        )

    def list_all(self) -> list[User]:
        return self.service.list_all()

    def get_by_id(self, user_id: int) -> User:
        try:
            return self.service.get_by_id(user_id)
        except ApplicationError as exc:
            raise translate_application_error(exc) from exc

    def update_self(self, current_user: User, payload: UserUpdateDTO) -> User:
        try:
            return self.service.update_self(current_user, full_name=payload.full_name)
        except ApplicationError as exc:
            raise translate_application_error(exc) from exc

    def update_by_admin(self, user_id: int, payload: UserAdminUpdateDTO) -> User:
        try:
            return self.service.update_by_admin(
                user_id,
                full_name=payload.full_name,
                role=payload.role,
                is_blocked=payload.is_blocked,
            )
        except ApplicationError as exc:
            raise translate_application_error(exc) from exc

    def delete(self, user_id: int) -> None:
        try:
            self.service.delete(user_id)
        except ApplicationError as exc:
            raise translate_application_error(exc) from exc
