from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from src.dto.schemas import ModerationDecisionDTO
from src.models.entities import Listing, ListingStatus


class ModerationService:
    def __init__(self, db: Session) -> None:
        self.db = db

    def review(self, listing_id: int, payload: ModerationDecisionDTO) -> Listing:
        listing = self.db.get(Listing, listing_id)
        if listing is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Listing not found")
        if listing.status != ListingStatus.PENDING:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Only pending listings can be moderated",
            )
        if payload.approved:
            listing.status = ListingStatus.APPROVED
            listing.rejection_reason = None
        else:
            if not payload.rejection_reason:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Rejection reason is required",
                )
            listing.status = ListingStatus.REJECTED
            listing.rejection_reason = payload.rejection_reason.strip()
        self.db.commit()
        self.db.refresh(listing)
        return listing

