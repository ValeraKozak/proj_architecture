from typing import Generic, TypeVar

from src.db.database import DatabaseSession

ModelType = TypeVar("ModelType")


class Repository(Generic[ModelType]):
    def __init__(self, db: DatabaseSession, model: type[ModelType]) -> None:
        self.db = db
        self.model = model

    def add(self, entity: ModelType) -> ModelType:
        return self.db.add(entity)

    def get(self, entity_id: int) -> ModelType | None:
        return self.db.get(self.model, entity_id)

    def list_all(self) -> list[ModelType]:
        return self.db.find_many(self.model)

    def delete(self, entity: ModelType) -> None:
        self.db.delete(entity)
