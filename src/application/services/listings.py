import logging

from src.application.common.errors import ForbiddenError, NotFoundError, ValidationError
from src.application.ports.repositories import (
    CategoryRepositoryPort,
    ListingRepositoryPort,
    UnitOfWorkPort,
    UserRepositoryPort,
)
from src.domain.entities import Listing, ListingImage, ListingStatus, Role, User

logger = logging.getLogger(__name__)


class ListingApplicationService:
    def __init__(
        self,
        listings: ListingRepositoryPort,
        categories: CategoryRepositoryPort,
        users: UserRepositoryPort,
        uow: UnitOfWorkPort,
    ) -> None:
        self.listings = listings
        self.categories = categories
        self.users = users
        self.uow = uow

    def create(
        self,
        *,
        title: str,
        description: str,
        price: float,
        category_id: int,
        image_urls: list[str],
        owner: User,
    ) -> Listing:
        if owner.is_blocked:
            raise ForbiddenError("Blocked users cannot post")
        if self.categories.get(category_id) is None:
            raise NotFoundError("Category not found")
        listing = Listing(
            title=title.strip(),
            description=description.strip(),
            price=price,
            category_id=category_id,
            owner_id=owner.id,
            status=ListingStatus.PENDING,
        )
        self._set_images(listing, image_urls)
        self.listings.add(listing)
        self.uow.commit()
        self.uow.refresh(listing)
        self._enrich_listing(listing)
        logger.info("Listing created listing_id=%s owner_id=%s", listing.id, owner.id)
        return listing

    def update(
        self,
        listing_id: int,
        *,
        title: str | None,
        description: str | None,
        price: float | None,
        category_id: int | None,
        image_urls: list[str] | None,
        owner: User,
    ) -> Listing:
        listing = self._get_owned_listing(listing_id, owner.id)
        if category_id is not None and self.categories.get(category_id) is None:
            raise NotFoundError("Category not found")
        if title is not None:
            listing.title = title.strip()
        if description is not None:
            listing.description = description.strip()
        if price is not None:
            listing.price = price
        if category_id is not None:
            listing.category_id = category_id
        if image_urls is not None:
            self._set_images(listing, image_urls)
        listing.status = ListingStatus.PENDING
        listing.rejection_reason = None
        self.uow.commit()
        self.uow.refresh(listing)
        self._enrich_listing(listing)
        logger.info("Listing updated listing_id=%s owner_id=%s", listing.id, owner.id)
        return listing

    def get_public(
        self,
        *,
        query: str | None = None,
        category_id: int | None = None,
        min_price: float | None = None,
        max_price: float | None = None,
        sort_by: str = "created_at",
        sort_order: str = "desc",
    ) -> list[Listing]:
        if min_price is not None and max_price is not None and min_price > max_price:
            raise ValidationError("min_price cannot be greater than max_price")
        listings = self.listings.list_visible(
            query=query,
            category_id=category_id,
            min_price=min_price,
            max_price=max_price,
            sort_by=sort_by,
            sort_order=sort_order,
        )
        return self._enrich_listings(listings)

    def get_by_id(self, listing_id: int, current_user: User | None = None) -> Listing:
        listing = self.listings.get(listing_id)
        if listing is None:
            raise NotFoundError("Listing not found")
        if listing.status == ListingStatus.APPROVED:
            self._enrich_listing(listing)
            return listing
        if current_user is None:
            raise NotFoundError("Listing not found")
        if current_user.id == listing.owner_id or current_user.role in {Role.ADMIN, Role.MODERATOR}:
            self._enrich_listing(listing)
            return listing
        raise NotFoundError("Listing not found")

    def get_owned(self, owner: User) -> list[Listing]:
        return self._enrich_listings(self.listings.list_owned(owner.id))

    def get_for_moderation(self) -> list[Listing]:
        return self._enrich_listings(self.listings.list_for_moderation())

    def delete(self, listing_id: int, owner: User) -> None:
        listing = self._get_owned_listing(listing_id, owner.id)
        self.listings.delete(listing)
        self.uow.commit()
        logger.info("Listing deleted listing_id=%s owner_id=%s", listing.id, owner.id)

    def _get_owned_listing(self, listing_id: int, owner_id: int | None) -> Listing:
        listing = self.listings.get(listing_id)
        if listing is None:
            raise NotFoundError("Listing not found")
        if listing.owner_id != owner_id:
            raise ForbiddenError("Not your listing")
        return listing

    @staticmethod
    def _set_images(listing: Listing, image_urls: list[str]) -> None:
        listing.images = [
            ListingImage(url=image_url, position=index)
            for index, image_url in enumerate(image_urls)
        ]

    def _enrich_listing(self, listing: Listing) -> Listing:
        if listing.owner_id is not None:
            owner = self.users.get(listing.owner_id)
            listing.owner_name = owner.full_name if owner is not None else None
        return listing

    def _enrich_listings(self, listings: list[Listing]) -> list[Listing]:
        return [self._enrich_listing(listing) for listing in listings]
