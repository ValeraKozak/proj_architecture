from src.models.entities import Listing, ListingStatus
from src.repositories.base import Repository


class ListingRepository(Repository[Listing]):
    def __init__(self, db):
        super().__init__(db, Listing)

    def list_visible(self) -> list[Listing]:
        return list(self.db.query(Listing).filter(Listing.status == ListingStatus.APPROVED).all())

    def list_for_moderation(self) -> list[Listing]:
        return list(self.db.query(Listing).filter(Listing.status == ListingStatus.PENDING).all())

    def list_owned(self, owner_id: int) -> list[Listing]:
        return list(self.db.query(Listing).filter(Listing.owner_id == owner_id).all())
