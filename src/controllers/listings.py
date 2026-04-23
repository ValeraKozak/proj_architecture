from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.core.security import get_current_user, require_role
from src.db.database import get_db
from src.dto.schemas import ListingCreateDTO, ListingReadDTO, ListingUpdateDTO
from src.models.entities import Role, User
from src.services.listing_service import ListingService

router = APIRouter(prefix="/listings", tags=["listings"])


@router.post("", response_model=ListingReadDTO, status_code=201)
def create_listing(
    payload: ListingCreateDTO,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ListingReadDTO:
    return ListingService(db).create(payload, current_user)


@router.put("/{listing_id}", response_model=ListingReadDTO)
def update_listing(
    listing_id: int,
    payload: ListingUpdateDTO,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ListingReadDTO:
    return ListingService(db).update(listing_id, payload, current_user)


@router.get("", response_model=list[ListingReadDTO])
def public_listings(db: Session = Depends(get_db)) -> list[ListingReadDTO]:
    return ListingService(db).get_public()


@router.get("/moderation/pending", response_model=list[ListingReadDTO])
def moderation_queue(
    db: Session = Depends(get_db),
    _: User = Depends(require_role(Role.ADMIN, Role.MODERATOR)),
) -> list[ListingReadDTO]:
    return ListingService(db).get_for_moderation()

