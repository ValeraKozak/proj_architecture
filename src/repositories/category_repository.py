from src.models.entities import Category, Listing
from src.repositories.base import Repository


class CategoryRepository(Repository[Category]):
    def __init__(self, db):
        super().__init__(db, Category)

    def get_by_name(self, name: str) -> Category | None:
        return self.db.find_one(Category, {"name": name})

    def has_related_listings(self, category_id: int) -> bool:
        return self.db.count(Listing, {"category_id": category_id}) > 0
