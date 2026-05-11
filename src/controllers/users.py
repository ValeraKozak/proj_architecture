from fastapi import APIRouter, Depends, status

from src.adapters.http.dependencies import get_user_service
from src.adapters.http.security import get_current_user, require_role
from src.application.services import UserApplicationService
from src.dto.schemas import DeleteResponseDTO, UserAdminUpdateDTO, UserReadDTO, UserUpdateDTO
from src.models.entities import Role, User

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me", response_model=UserReadDTO)
def get_me(current_user: User = Depends(get_current_user)) -> UserReadDTO:
    return current_user


@router.patch("/me", response_model=UserReadDTO)
def update_me(
    payload: UserUpdateDTO,
    service: UserApplicationService = Depends(get_user_service),
    current_user: User = Depends(get_current_user),
) -> UserReadDTO:
    return service.update_self(current_user, full_name=payload.full_name)


@router.get("", response_model=list[UserReadDTO])
def list_users(
    service: UserApplicationService = Depends(get_user_service),
    _: User = Depends(require_role(Role.ADMIN)),
) -> list[UserReadDTO]:
    return service.list_all()


@router.get("/{user_id}", response_model=UserReadDTO)
def get_user(
    user_id: int,
    service: UserApplicationService = Depends(get_user_service),
    _: User = Depends(require_role(Role.ADMIN)),
) -> UserReadDTO:
    return service.get_by_id(user_id)


@router.patch("/{user_id}", response_model=UserReadDTO)
def update_user(
    user_id: int,
    payload: UserAdminUpdateDTO,
    service: UserApplicationService = Depends(get_user_service),
    _: User = Depends(require_role(Role.ADMIN)),
) -> UserReadDTO:
    return service.update_by_admin(
        user_id,
        full_name=payload.full_name,
        role=payload.role,
        is_blocked=payload.is_blocked,
    )


@router.delete("/{user_id}", response_model=DeleteResponseDTO, status_code=status.HTTP_200_OK)
def delete_user(
    user_id: int,
    service: UserApplicationService = Depends(get_user_service),
    _: User = Depends(require_role(Role.ADMIN)),
) -> DeleteResponseDTO:
    service.delete(user_id)
    return DeleteResponseDTO(message="User deleted")
