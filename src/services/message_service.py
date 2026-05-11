from src.adapters.persistence.mongodb.repositories import (
    MongoListingRepository,
    MongoMessageRepository,
    MongoUnitOfWork,
    MongoUserRepository,
)
from src.application.common.errors import ApplicationError
from src.application.services.messages import MessageApplicationService
from src.db.database import DatabaseSession
from src.dto.schemas import DeleteResponseDTO, MessageCreateDTO
from src.models.entities import Message, User
from src.services._legacy import translate_application_error


class MessageService:
    def __init__(self, db: DatabaseSession) -> None:
        self.service = MessageApplicationService(
            messages=MongoMessageRepository(db),
            listings=MongoListingRepository(db),
            users=MongoUserRepository(db),
            uow=MongoUnitOfWork(db),
        )

    def send(self, payload: MessageCreateDTO, sender: User) -> Message:
        try:
            return self.service.send(
                listing_id=payload.listing_id,
                recipient_id=payload.recipient_id,
                body=payload.body,
                sender=sender,
            )
        except ApplicationError as exc:
            raise translate_application_error(exc) from exc

    def list_user_messages(self, user_id: int) -> list[Message]:
        return self.service.list_user_messages(user_id)

    def get_user_message(self, message_id: int, user_id: int) -> Message:
        try:
            return self.service.get_user_message(message_id, user_id)
        except ApplicationError as exc:
            raise translate_application_error(exc) from exc

    def delete_user_message(self, message_id: int, user_id: int) -> DeleteResponseDTO:
        try:
            return DeleteResponseDTO(**self.service.delete_user_message(message_id, user_id))
        except ApplicationError as exc:
            raise translate_application_error(exc) from exc
