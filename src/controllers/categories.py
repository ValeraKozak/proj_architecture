from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.core.security import require_role
from src.db.database import get_db
from src.dto.schemas import CategoryCreateDTO, CategoryReadDTO
from src.models.entities import Role, User
from src.services.category_service import CategoryService

router = APIRouter(prefix="/categories", tags=["categories"])


@router.post("", response_model=CategoryReadDTO, status_code=201)
def create_category(
    payload: CategoryCreateDTO,
    db: Session = Depends(get_db),
    _: User = Depends(require_role(Role.ADMIN, Role.MODERATOR)),
) -> CategoryReadDTO:
    return CategoryService(db).create(payload)


@router.get("", response_model=list[CategoryReadDTO])
def list_categories(db: Session = Depends(get_db)) -> list[CategoryReadDTO]:
    return CategoryService(db).list_all()

