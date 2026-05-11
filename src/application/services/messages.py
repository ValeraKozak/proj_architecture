import logging

from src.application.common.errors import ForbiddenError, NotFoundError, ValidationError
from src.application.ports.repositories import (
    ListingRepositoryPort,
    MessageRepositoryPort,
    UnitOfWorkPort,
    UserRepositoryPort,
)
from src.domain.entities import ListingStatus, Message, User

logger = logging.getLogger(__name__)


class MessageApplicationService:
    def __init__(
        self,
        messages: MessageRepositoryPort,
        listings: ListingRepositoryPort,
        users: UserRepositoryPort,
        uow: UnitOfWorkPort,
    ) -> None:
        self.messages = messages
        self.listings = listings
        self.users = users
        self.uow = uow

    def send(self, *, listing_id: int, recipient_id: int, body: str, sender: User) -> Message:
        if sender.is_blocked:
            raise ForbiddenError("Blocked users cannot send messages")
        if sender.id == recipient_id:
            raise ValidationError("Cannot send message to yourself")
        listing = self.listings.get(listing_id)
        if listing is None or listing.status != ListingStatus.APPROVED:
            raise ValidationError("Messages are allowed only for approved listings")
        recipient = self.users.get(recipient_id)
        if recipient is None:
            raise NotFoundError("Recipient not found")
        message = Message(
            listing_id=listing_id,
            sender_id=sender.id,
            recipient_id=recipient_id,
            body=body.strip(),
        )
        self.messages.add(message)
        self.uow.commit()
        self._enrich_message(message)
        logger.info(
            "Message sent message_id=%s listing_id=%s sender_id=%s recipient_id=%s",
            message.id,
            message.listing_id,
            sender.id,
            recipient.id,
        )
        return message

    def list_user_messages(self, user_id: int) -> list[Message]:
        return self._enrich_messages(self.messages.list_for_user(user_id))

    def get_user_message(self, message_id: int, user_id: int) -> Message:
        message = self.messages.get_for_user(message_id, user_id)
        if message is None:
            raise NotFoundError("Message not found")
        return self._enrich_message(message)

    def delete_user_message(self, message_id: int, user_id: int) -> None:
        message = self.get_user_message(message_id, user_id)
        self.messages.delete(message)
        self.uow.commit()
        logger.info("Message deleted message_id=%s user_id=%s", message_id, user_id)

    def _enrich_message(self, message: Message) -> Message:
        if message.sender_id is not None:
            sender = self.users.get(message.sender_id)
            message.sender_name = sender.full_name if sender is not None else None
        if message.recipient_id is not None:
            recipient = self.users.get(message.recipient_id)
            message.recipient_name = recipient.full_name if recipient is not None else None
        return message

    def _enrich_messages(self, messages: list[Message]) -> list[Message]:
        return [self._enrich_message(message) for message in messages]
