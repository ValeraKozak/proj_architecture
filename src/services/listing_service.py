from src.adapters.persistence.mongodb.repositories import (
    MongoCategoryRepository,
    MongoListingRepository,
    MongoUnitOfWork,
    MongoUserRepository,
)
from src.application.common.errors import ApplicationError
from src.application.services.listings import ListingApplicationService
from src.db.database import DatabaseSession
from src.dto.schemas import DeleteResponseDTO, ListingCreateDTO, ListingUpdateDTO
from src.models.entities import Listing, User
from src.services._legacy import translate_application_error


class ListingService:
    def __init__(self, db: DatabaseSession) -> None:
        self.service = ListingApplicationService(
            listings=MongoListingRepository(db),
            categories=MongoCategoryRepository(db),
            users=MongoUserRepository(db),
            uow=MongoUnitOfWork(db),
        )

    def create(self, payload: ListingCreateDTO, owner: User) -> Listing:
        try:
            return self.service.create(
                title=payload.title,
                description=payload.description,
                price=payload.price,
                category_id=payload.category_id,
                image_urls=[str(url) for url in payload.image_urls],
                owner=owner,
            )
        except ApplicationError as exc:
            raise translate_application_error(exc) from exc

    def update(self, listing_id: int, payload: ListingUpdateDTO, owner: User) -> Listing:
        image_urls = None
        if payload.image_urls is not None:
            image_urls = [str(url) for url in payload.image_urls]
        try:
            return self.service.update(
                listing_id,
                title=payload.title,
                description=payload.description,
                price=payload.price,
                category_id=payload.category_id,
                image_urls=image_urls,
                owner=owner,
            )
        except ApplicationError as exc:
            raise translate_application_error(exc) from exc

    def get_public(
        self,
        *,
        query: str | None = None,
        category_id: int | None = None,
        min_price: float | None = None,
        max_price: float | None = None,
        sort_by: str = "created_at",
        sort_order: str = "desc",
    ) -> list[Listing]:
        return self.service.get_public(
            query=query,
            category_id=category_id,
            min_price=min_price,
            max_price=max_price,
            sort_by=sort_by,
            sort_order=sort_order,
        )

    def get_by_id(self, listing_id: int, current_user: User | None = None) -> Listing:
        try:
            return self.service.get_by_id(listing_id, current_user)
        except ApplicationError as exc:
            raise translate_application_error(exc) from exc

    def get_owned(self, owner: User) -> list[Listing]:
        return self.service.get_owned(owner)

    def get_for_moderation(self) -> list[Listing]:
        return self.service.get_for_moderation()

    def delete(self, listing_id: int, owner: User) -> DeleteResponseDTO:
        try:
            return DeleteResponseDTO(**self.service.delete(listing_id, owner))
        except ApplicationError as exc:
            raise translate_application_error(exc) from exc
