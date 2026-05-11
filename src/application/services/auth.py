from src.application.common.errors import ApplicationError
from src.application.ports.repositories import UnitOfWorkPort, UserRepositoryPort
from src.application.ports.security import PasswordManagerPort, TokenServicePort
from src.domain.entities import User


class AuthApplicationService:
    def __init__(
        self,
        users: UserRepositoryPort,
        uow: UnitOfWorkPort,
        password_manager: PasswordManagerPort,
        token_service: TokenServicePort,
    ) -> None:
        self.users = users
        self.uow = uow
        self.password_manager = password_manager
        self.token_service = token_service

    def register(self, *, email: str, full_name: str, password: str) -> User:
        if self.users.get_by_email(email):
            raise ApplicationError(409, "Email already exists")
        user = User(
            email=email,
            full_name=full_name.strip(),
            password_hash=self.password_manager.hash_password(password),
        )
        self.users.add(user)
        self.uow.commit()
        return user

    def login(self, *, email: str, password: str) -> str:
        user = self.users.get_by_email(email)
        if user is None or not self.password_manager.verify_password(password, user.password_hash):
            raise ApplicationError(401, "Invalid credentials")
        if user.is_blocked:
            raise ApplicationError(403, "User is blocked")
        return self.token_service.create_access_token(user.email)
