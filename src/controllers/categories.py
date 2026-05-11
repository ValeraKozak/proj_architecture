from fastapi import APIRouter, Depends

from src.adapters.http.dependencies import get_category_service
from src.adapters.http.security import require_role
from src.application.services import CategoryApplicationService
from src.dto.schemas import CategoryCreateDTO, CategoryReadDTO, CategoryUpdateDTO, DeleteResponseDTO
from src.models.entities import Role, User

router = APIRouter(prefix="/categories", tags=["categories"])


@router.post("", response_model=CategoryReadDTO, status_code=201)
def create_category(
    payload: CategoryCreateDTO,
    service: CategoryApplicationService = Depends(get_category_service),
    _: User = Depends(require_role(Role.ADMIN, Role.MODERATOR)),
) -> CategoryReadDTO:
    return service.create(name=payload.name, description=payload.description)


@router.get("", response_model=list[CategoryReadDTO])
def list_categories(
    service: CategoryApplicationService = Depends(get_category_service),
) -> list[CategoryReadDTO]:
    return service.list_all()


@router.get("/{category_id}", response_model=CategoryReadDTO)
def get_category(
    category_id: int,
    service: CategoryApplicationService = Depends(get_category_service),
) -> CategoryReadDTO:
    return service.get_by_id(category_id)


@router.put("/{category_id}", response_model=CategoryReadDTO)
def update_category(
    category_id: int,
    payload: CategoryUpdateDTO,
    service: CategoryApplicationService = Depends(get_category_service),
    _: User = Depends(require_role(Role.ADMIN, Role.MODERATOR)),
) -> CategoryReadDTO:
    return service.update(category_id, name=payload.name, description=payload.description)


@router.delete("/{category_id}", response_model=DeleteResponseDTO)
def delete_category(
    category_id: int,
    service: CategoryApplicationService = Depends(get_category_service),
    _: User = Depends(require_role(Role.ADMIN)),
) -> DeleteResponseDTO:
    service.delete(category_id)
    return DeleteResponseDTO(message="Category deleted")
