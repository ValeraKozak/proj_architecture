from fastapi import APIRouter, Depends

from src.adapters.http.dependencies import get_moderation_service
from src.adapters.http.security import require_role
from src.application.services import ModerationApplicationService
from src.dto.schemas import ListingReadDTO, ModerationDecisionDTO
from src.models.entities import Role, User

router = APIRouter(prefix="/moderation", tags=["moderation"])


@router.post("/listings/{listing_id}", response_model=ListingReadDTO)
def review_listing(
    listing_id: int,
    payload: ModerationDecisionDTO,
    service: ModerationApplicationService = Depends(get_moderation_service),
    _: User = Depends(require_role(Role.ADMIN, Role.MODERATOR)),
) -> ListingReadDTO:
    return service.review(
        listing_id,
        approved=payload.approved,
        rejection_reason=payload.rejection_reason,
    )
