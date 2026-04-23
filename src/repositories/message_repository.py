from src.models.entities import Message
from src.repositories.base import Repository


class MessageRepository(Repository[Message]):
    def __init__(self, db):
        super().__init__(db, Message)

    def list_for_user(self, user_id: int) -> list[Message]:
        return list(
            self.db.query(Message)
            .filter((Message.sender_id == user_id) | (Message.recipient_id == user_id))
            .all()
        )

