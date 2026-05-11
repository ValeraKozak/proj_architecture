import logging

from src.application.common.errors import ConflictError, NotFoundError, ValidationError
from src.application.ports.repositories import ListingRepositoryPort, UnitOfWorkPort
from src.domain.entities import Listing, ListingStatus

logger = logging.getLogger(__name__)


class ModerationApplicationService:
    def __init__(self, listings: ListingRepositoryPort, uow: UnitOfWorkPort) -> None:
        self.listings = listings
        self.uow = uow

    def review(
        self,
        listing_id: int,
        *,
        approved: bool,
        rejection_reason: str | None,
    ) -> Listing:
        listing = self.listings.get(listing_id)
        if listing is None:
            raise NotFoundError("Listing not found")
        if listing.status != ListingStatus.PENDING:
            raise ConflictError("Only pending listings can be moderated")
        if approved:
            listing.status = ListingStatus.APPROVED
            listing.rejection_reason = None
        else:
            if not rejection_reason:
                raise ValidationError("Rejection reason is required")
            listing.status = ListingStatus.REJECTED
            listing.rejection_reason = rejection_reason.strip()
        self.uow.commit()
        self.uow.refresh(listing)
        logger.info("Listing moderated listing_id=%s status=%s", listing.id, listing.status)
        return listing
