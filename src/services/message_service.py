from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from src.dto.schemas import MessageCreateDTO
from src.models.entities import Listing, ListingStatus, Message, User
from src.repositories.message_repository import MessageRepository


class MessageService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.messages = MessageRepository(db)

    def send(self, payload: MessageCreateDTO, sender: User) -> Message:
        if sender.is_blocked:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Blocked users cannot send messages"
            )
        if sender.id == payload.recipient_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Cannot send message to yourself"
            )
        listing = self.db.get(Listing, payload.listing_id)
        if listing is None or listing.status != ListingStatus.APPROVED:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Messages are allowed only for approved listings",
            )
        recipient = self.db.get(User, payload.recipient_id)
        if recipient is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Recipient not found")
        message = Message(
            listing_id=payload.listing_id,
            sender_id=sender.id,
            recipient_id=payload.recipient_id,
            body=payload.body.strip(),
        )
        self.messages.add(message)
        self.db.commit()
        return message

    def list_user_messages(self, user_id: int) -> list[Message]:
        return self.messages.list_for_user(user_id)

