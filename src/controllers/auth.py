from fastapi import APIRouter, Depends

from src.adapters.http.dependencies import get_auth_service
from src.application.services import AuthApplicationService
from src.dto.schemas import TokenDTO, UserCreateDTO, UserLoginDTO, UserReadDTO

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserReadDTO, status_code=201)
def register(
    payload: UserCreateDTO,
    service: AuthApplicationService = Depends(get_auth_service),
) -> UserReadDTO:
    return service.register(
        email=payload.email,
        full_name=payload.full_name,
        password=payload.password,
    )


@router.post("/login", response_model=TokenDTO)
def login(
    payload: UserLoginDTO,
    service: AuthApplicationService = Depends(get_auth_service),
) -> TokenDTO:
    return TokenDTO(access_token=service.login(email=payload.email, password=payload.password))
