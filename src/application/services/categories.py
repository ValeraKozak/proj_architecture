import logging

from src.application.common.errors import ConflictError, NotFoundError
from src.application.ports.repositories import CategoryRepositoryPort, UnitOfWorkPort
from src.domain.entities import Category

logger = logging.getLogger(__name__)


class CategoryApplicationService:
    def __init__(self, categories: CategoryRepositoryPort, uow: UnitOfWorkPort) -> None:
        self.categories = categories
        self.uow = uow

    def create(self, *, name: str, description: str) -> Category:
        if self.categories.get_by_name(name):
            raise ConflictError("Category already exists")
        category = Category(name=name.strip(), description=description.strip())
        self.categories.add(category)
        self.uow.commit()
        return category

    def list_all(self) -> list[Category]:
        return self.categories.list_all()

    def get_by_id(self, category_id: int) -> Category:
        category = self.categories.get(category_id)
        if category is None:
            raise NotFoundError("Category not found")
        return category

    def update(self, category_id: int, *, name: str, description: str) -> Category:
        category = self.get_by_id(category_id)
        existing = self.categories.get_by_name(name.strip())
        if existing is not None and existing.id != category_id:
            raise ConflictError("Category already exists")
        category.name = name.strip()
        category.description = description.strip()
        self.uow.commit()
        self.uow.refresh(category)
        logger.info("Category updated category_id=%s", category.id)
        return category

    def delete(self, category_id: int) -> None:
        category = self.get_by_id(category_id)
        if self.categories.has_related_listings(category_id):
            raise ConflictError("Cannot delete category with listings")
        self.categories.delete(category)
        self.uow.commit()
        logger.info("Category deleted category_id=%s", category_id)
