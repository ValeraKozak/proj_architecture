from src.adapters.persistence.mongodb.repositories import MongoCategoryRepository, MongoUnitOfWork
from src.application.common.errors import ApplicationError
from src.application.services.categories import CategoryApplicationService
from src.db.database import DatabaseSession
from src.dto.schemas import CategoryCreateDTO, CategoryUpdateDTO
from src.models.entities import Category
from src.services._legacy import translate_application_error


class CategoryService:
    def __init__(self, db: DatabaseSession) -> None:
        self.service = CategoryApplicationService(
            categories=MongoCategoryRepository(db),
            uow=MongoUnitOfWork(db),
        )

    def create(self, payload: CategoryCreateDTO) -> Category:
        try:
            return self.service.create(name=payload.name, description=payload.description)
        except ApplicationError as exc:
            raise translate_application_error(exc) from exc

    def list_all(self) -> list[Category]:
        return self.service.list_all()

    def get_by_id(self, category_id: int) -> Category:
        try:
            return self.service.get_by_id(category_id)
        except ApplicationError as exc:
            raise translate_application_error(exc) from exc

    def update(self, category_id: int, payload: CategoryUpdateDTO) -> Category:
        try:
            return self.service.update(
                category_id,
                name=payload.name,
                description=payload.description,
            )
        except ApplicationError as exc:
            raise translate_application_error(exc) from exc

    def delete(self, category_id: int) -> None:
        try:
            self.service.delete(category_id)
        except ApplicationError as exc:
            raise translate_application_error(exc) from exc
