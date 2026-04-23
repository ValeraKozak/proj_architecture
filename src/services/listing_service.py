import logging

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from src.dto.schemas import DeleteResponseDTO, ListingCreateDTO, ListingUpdateDTO
from src.models.entities import Category, Listing, ListingStatus, Role, User
from src.repositories.listing_repository import ListingRepository

logger = logging.getLogger(__name__)


class ListingService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.listings = ListingRepository(db)

    def create(self, payload: ListingCreateDTO, owner: User) -> Listing:
        if owner.is_blocked:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Blocked users cannot post",
            )
        category = self.db.get(Category, payload.category_id)
        if category is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
        listing = Listing(
            title=payload.title.strip(),
            description=payload.description.strip(),
            price=payload.price,
            category_id=payload.category_id,
            owner_id=owner.id,
            status=ListingStatus.PENDING,
        )
        self.listings.add(listing)
        self.db.commit()
        logger.info("Listing created listing_id=%s owner_id=%s", listing.id, owner.id)
        return listing

    def update(self, listing_id: int, payload: ListingUpdateDTO, owner: User) -> Listing:
        listing = self._get_owned_listing(listing_id, owner.id)
        if payload.category_id is not None and self.db.get(Category, payload.category_id) is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
        for field, value in payload.model_dump(exclude_none=True).items():
            setattr(listing, field, value.strip() if isinstance(value, str) else value)
        listing.status = ListingStatus.PENDING
        listing.rejection_reason = None
        self.db.commit()
        self.db.refresh(listing)
        logger.info("Listing updated listing_id=%s owner_id=%s", listing.id, owner.id)
        return listing

    def get_public(self) -> list[Listing]:
        return self.listings.list_visible()

    def get_by_id(self, listing_id: int, current_user: User | None = None) -> Listing:
        listing = self.listings.get(listing_id)
        if listing is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Listing not found")
        if listing.status == ListingStatus.APPROVED:
            return listing
        if current_user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Listing not found")
        if current_user.id == listing.owner_id or current_user.role in {Role.ADMIN, Role.MODERATOR}:
            return listing
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Listing not found")

    def get_owned(self, owner: User) -> list[Listing]:
        return self.listings.list_owned(owner.id)

    def get_for_moderation(self) -> list[Listing]:
        return self.listings.list_for_moderation()

    def delete(self, listing_id: int, owner: User) -> DeleteResponseDTO:
        listing = self._get_owned_listing(listing_id, owner.id)
        self.listings.delete(listing)
        self.db.commit()
        logger.info("Listing deleted listing_id=%s owner_id=%s", listing.id, owner.id)
        return DeleteResponseDTO(message="Listing deleted")

    def _get_owned_listing(self, listing_id: int, owner_id: int) -> Listing:
        listing = self.listings.get(listing_id)
        if listing is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Listing not found")
        if listing.owner_id != owner_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not your listing")
        return listing
