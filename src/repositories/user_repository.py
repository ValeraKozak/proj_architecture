from src.models.entities import User
from src.repositories.base import Repository


class UserRepository(Repository[User]):
    def __init__(self, db):
        super().__init__(db, User)

    def get_by_email(self, email: str) -> User | None:
        return self.db.query(User).filter(User.email == email).one_or_none()

