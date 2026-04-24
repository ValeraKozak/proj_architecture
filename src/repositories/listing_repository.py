from sqlalchemy import or_
from sqlalchemy.orm import selectinload

from src.models.entities import Category, Listing, ListingStatus
from src.repositories.base import Repository


class ListingRepository(Repository[Listing]):
    def __init__(self, db):
        super().__init__(db, Listing)

    def list_visible(
        self,
        *,
        query: str | None = None,
        category_id: int | None = None,
        min_price: float | None = None,
        max_price: float | None = None,
        sort_by: str = "created_at",
        sort_order: str = "desc",
    ) -> list[Listing]:
        listing_query = (
            self.db.query(Listing)
            .options(selectinload(Listing.images))
            .join(Category)
            .filter(Listing.status == ListingStatus.APPROVED)
        )
        if query:
            pattern = f"%{query.strip()}%"
            listing_query = listing_query.filter(
                or_(
                    Listing.title.ilike(pattern),
                    Listing.description.ilike(pattern),
                    Category.name.ilike(pattern),
                )
            )
        if category_id is not None:
            listing_query = listing_query.filter(Listing.category_id == category_id)
        if min_price is not None:
            listing_query = listing_query.filter(Listing.price >= min_price)
        if max_price is not None:
            listing_query = listing_query.filter(Listing.price <= max_price)

        sort_column = Listing.price if sort_by == "price" else Listing.created_at
        sort_expression = sort_column.asc() if sort_order == "asc" else sort_column.desc()
        return list(listing_query.order_by(sort_expression, Listing.id.desc()).all())

    def list_for_moderation(self) -> list[Listing]:
        return list(
            self.db.query(Listing)
            .options(selectinload(Listing.images))
            .filter(Listing.status == ListingStatus.PENDING)
            .all()
        )

    def list_owned(self, owner_id: int) -> list[Listing]:
        return list(
            self.db.query(Listing)
            .options(selectinload(Listing.images))
            .filter(Listing.owner_id == owner_id)
            .order_by(Listing.created_at.desc(), Listing.id.desc())
            .all()
        )
