from typing import Literal

from fastapi import APIRouter, Depends, Query

from src.adapters.http.dependencies import get_listing_service
from src.adapters.http.security import get_current_user, get_optional_current_user, require_role
from src.application.services import ListingApplicationService
from src.dto.schemas import DeleteResponseDTO, ListingCreateDTO, ListingReadDTO, ListingUpdateDTO
from src.models.entities import Role, User

router = APIRouter(prefix="/listings", tags=["listings"])


@router.post("", response_model=ListingReadDTO, status_code=201)
def create_listing(
    payload: ListingCreateDTO,
    service: ListingApplicationService = Depends(get_listing_service),
    current_user: User = Depends(get_current_user),
) -> ListingReadDTO:
    return service.create(
        title=payload.title,
        description=payload.description,
        price=payload.price,
        category_id=payload.category_id,
        image_urls=[str(url) for url in payload.image_urls],
        owner=current_user,
    )


@router.put("/{listing_id}", response_model=ListingReadDTO)
def update_listing(
    listing_id: int,
    payload: ListingUpdateDTO,
    service: ListingApplicationService = Depends(get_listing_service),
    current_user: User = Depends(get_current_user),
) -> ListingReadDTO:
    image_urls = None
    if payload.image_urls is not None:
        image_urls = [str(url) for url in payload.image_urls]
    return service.update(
        listing_id,
        title=payload.title,
        description=payload.description,
        price=payload.price,
        category_id=payload.category_id,
        image_urls=image_urls,
        owner=current_user,
    )


@router.get("", response_model=list[ListingReadDTO])
def public_listings(
    service: ListingApplicationService = Depends(get_listing_service),
    query: str | None = Query(default=None, min_length=1, max_length=100),
    category_id: int | None = Query(default=None, gt=0),
    min_price: float | None = Query(default=None, gt=0),
    max_price: float | None = Query(default=None, gt=0),
    sort_by: Literal["created_at", "price"] = Query(default="created_at"),
    sort_order: Literal["asc", "desc"] = Query(default="desc"),
) -> list[ListingReadDTO]:
    return service.get_public(
        query=query,
        category_id=category_id,
        min_price=min_price,
        max_price=max_price,
        sort_by=sort_by,
        sort_order=sort_order,
    )


@router.get("/me/owned", response_model=list[ListingReadDTO])
def my_listings(
    service: ListingApplicationService = Depends(get_listing_service),
    current_user: User = Depends(get_current_user),
) -> list[ListingReadDTO]:
    return service.get_owned(current_user)


@router.get("/moderation/pending", response_model=list[ListingReadDTO])
def moderation_queue(
    service: ListingApplicationService = Depends(get_listing_service),
    _: User = Depends(require_role(Role.ADMIN, Role.MODERATOR)),
) -> list[ListingReadDTO]:
    return service.get_for_moderation()


@router.get("/{listing_id}", response_model=ListingReadDTO)
def get_listing(
    listing_id: int,
    service: ListingApplicationService = Depends(get_listing_service),
    current_user: User | None = Depends(get_optional_current_user),
) -> ListingReadDTO:
    return service.get_by_id(listing_id, current_user)


@router.delete("/{listing_id}", response_model=DeleteResponseDTO)
def delete_listing(
    listing_id: int,
    service: ListingApplicationService = Depends(get_listing_service),
    current_user: User = Depends(get_current_user),
) -> DeleteResponseDTO:
    service.delete(listing_id, current_user)
    return DeleteResponseDTO(message="Listing deleted")
