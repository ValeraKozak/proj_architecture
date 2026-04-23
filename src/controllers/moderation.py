from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.core.security import require_role
from src.db.database import get_db
from src.dto.schemas import ListingReadDTO, ModerationDecisionDTO
from src.models.entities import Role, User
from src.services.moderation_service import ModerationService

router = APIRouter(prefix="/moderation", tags=["moderation"])


@router.post("/listings/{listing_id}", response_model=ListingReadDTO)
def review_listing(
    listing_id: int,
    payload: ModerationDecisionDTO,
    db: Session = Depends(get_db),
    _: User = Depends(require_role(Role.ADMIN, Role.MODERATOR)),
) -> ListingReadDTO:
    return ModerationService(db).review(listing_id, payload)

