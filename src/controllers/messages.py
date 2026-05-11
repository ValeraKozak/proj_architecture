from fastapi import APIRouter, Depends

from src.adapters.http.dependencies import get_message_service
from src.adapters.http.security import get_current_user
from src.application.services import MessageApplicationService
from src.dto.schemas import DeleteResponseDTO, MessageCreateDTO, MessageReadDTO
from src.models.entities import User

router = APIRouter(prefix="/messages", tags=["messages"])


@router.post("", response_model=MessageReadDTO, status_code=201)
def send_message(
    payload: MessageCreateDTO,
    service: MessageApplicationService = Depends(get_message_service),
    current_user: User = Depends(get_current_user),
) -> MessageReadDTO:
    return service.send(
        listing_id=payload.listing_id,
        recipient_id=payload.recipient_id,
        body=payload.body,
        sender=current_user,
    )


@router.get("/me", response_model=list[MessageReadDTO])
def my_messages(
    service: MessageApplicationService = Depends(get_message_service),
    current_user: User = Depends(get_current_user),
) -> list[MessageReadDTO]:
    return service.list_user_messages(current_user.id)


@router.get("/{message_id}", response_model=MessageReadDTO)
def get_message(
    message_id: int,
    service: MessageApplicationService = Depends(get_message_service),
    current_user: User = Depends(get_current_user),
) -> MessageReadDTO:
    return service.get_user_message(message_id, current_user.id)


@router.delete("/{message_id}", response_model=DeleteResponseDTO)
def delete_message(
    message_id: int,
    service: MessageApplicationService = Depends(get_message_service),
    current_user: User = Depends(get_current_user),
) -> DeleteResponseDTO:
    service.delete_user_message(message_id, current_user.id)
    return DeleteResponseDTO(message="Message deleted")
