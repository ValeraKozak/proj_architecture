from fastapi import HTTPException, status

from src.core.security import create_access_token, hash_password, verify_password
from src.db.database import DatabaseSession
from src.dto.schemas import TokenDTO, UserCreateDTO, UserLoginDTO
from src.models.entities import User
from src.repositories.user_repository import UserRepository


class AuthService:
    def __init__(self, db: DatabaseSession) -> None:
        self.db = db
        self.users = UserRepository(db)

    def register(self, payload: UserCreateDTO) -> User:
        if self.users.get_by_email(payload.email):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already exists")
        user = User(
            email=payload.email,
            full_name=payload.full_name.strip(),
            password_hash=hash_password(payload.password),
        )
        self.users.add(user)
        self.db.commit()
        return user

    def login(self, payload: UserLoginDTO) -> TokenDTO:
        user = self.users.get_by_email(payload.email)
        if user is None or not verify_password(payload.password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials",
            )
        if user.is_blocked:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User is blocked")
        return TokenDTO(access_token=create_access_token(user.email))
