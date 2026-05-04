from src.models.entities import Listing, Message, User
from src.repositories.base import Repository


class UserRepository(Repository[User]):
    def __init__(self, db):
        super().__init__(db, User)

    def get_by_email(self, email: str) -> User | None:
        return self.db.find_one(User, {"email": email})

    def has_related_content(self, user_id: int) -> bool:
        return (
            self.db.count(Listing, {"owner_id": user_id}) > 0
            or self.db.count(Message, {"sender_id": user_id}) > 0
            or self.db.count(Message, {"recipient_id": user_id}) > 0
        )
