import logging

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from src.dto.schemas import CategoryCreateDTO, CategoryUpdateDTO
from src.models.entities import Category
from src.repositories.category_repository import CategoryRepository

logger = logging.getLogger(__name__)


class CategoryService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.categories = CategoryRepository(db)

    def create(self, payload: CategoryCreateDTO) -> Category:
        if self.categories.get_by_name(payload.name):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Category already exists",
            )
        category = Category(name=payload.name.strip(), description=payload.description.strip())
        self.categories.add(category)
        self.db.commit()
        return category

    def list_all(self) -> list[Category]:
        return self.categories.list_all()

    def get_by_id(self, category_id: int) -> Category:
        category = self.categories.get(category_id)
        if category is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
        return category

    def update(self, category_id: int, payload: CategoryUpdateDTO) -> Category:
        category = self.get_by_id(category_id)
        existing = self.categories.get_by_name(payload.name.strip())
        if existing is not None and existing.id != category_id:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Category already exists",
            )
        category.name = payload.name.strip()
        category.description = payload.description.strip()
        self.db.commit()
        self.db.refresh(category)
        logger.info("Category updated category_id=%s", category.id)
        return category

    def delete(self, category_id: int) -> None:
        category = self.get_by_id(category_id)
        if self.categories.has_related_listings(category_id):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Cannot delete category with listings",
            )
        self.categories.delete(category)
        self.db.commit()
        logger.info("Category deleted category_id=%s", category_id)
