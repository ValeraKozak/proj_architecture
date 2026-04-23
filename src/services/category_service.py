from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from src.dto.schemas import CategoryCreateDTO
from src.models.entities import Category
from src.repositories.category_repository import CategoryRepository


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
