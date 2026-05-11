from src.adapters.persistence.mongodb.repositories import MongoUnitOfWork, MongoUserRepository
from src.application.common.errors import ApplicationError
from src.application.services.auth import AuthApplicationService
from src.core.security import PasswordManagerAdapter, TokenServiceAdapter
from src.db.database import DatabaseSession
from src.dto.schemas import TokenDTO, UserCreateDTO, UserLoginDTO
from src.models.entities import User
from src.services._legacy import translate_application_error


class AuthService:
    def __init__(self, db: DatabaseSession) -> None:
        self.service = AuthApplicationService(
            users=MongoUserRepository(db),
            uow=MongoUnitOfWork(db),
            password_manager=PasswordManagerAdapter(),
            token_service=TokenServiceAdapter(),
        )

    def register(self, payload: UserCreateDTO) -> User:
        try:
            return self.service.register(
                email=payload.email,
                full_name=payload.full_name,
                password=payload.password,
            )
        except ApplicationError as exc:
            raise translate_application_error(exc) from exc

    def login(self, payload: UserLoginDTO) -> TokenDTO:
        try:
            return TokenDTO(
                access_token=self.service.login(email=payload.email, password=payload.password)
            )
        except ApplicationError as exc:
            raise translate_application_error(exc) from exc
