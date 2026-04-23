from src.models.entities import Category
from src.repositories.base import Repository


class CategoryRepository(Repository[Category]):
    def __init__(self, db):
        super().__init__(db, Category)

    def get_by_name(self, name: str) -> Category | None:
        return self.db.query(Category).filter(Category.name == name).one_or_none()

