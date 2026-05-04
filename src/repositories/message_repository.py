from pymongo import DESCENDING

from src.models.entities import Message
from src.repositories.base import Repository


class MessageRepository(Repository[Message]):
    def __init__(self, db):
        super().__init__(db, Message)

    def list_for_user(self, user_id: int) -> list[Message]:
        return self.db.find_many(
            Message,
            {"$or": [{"sender_id": user_id}, {"recipient_id": user_id}]},
            sort=[("created_at", DESCENDING), ("id", DESCENDING)],
        )

    def get_for_user(self, message_id: int, user_id: int) -> Message | None:
        return self.db.find_one(
            Message,
            {
                "id": message_id,
                "$or": [{"sender_id": user_id}, {"recipient_id": user_id}],
            },
        )
