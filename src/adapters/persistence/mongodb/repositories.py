from src.application.ports.repositories import (
    CategoryRepositoryPort,
    ListingRepositoryPort,
    MessageRepositoryPort,
    UnitOfWorkPort,
    UserRepositoryPort,
)
from src.db.database import DatabaseSession
from src.repositories.category_repository import CategoryRepository
from src.repositories.listing_repository import ListingRepository
from src.repositories.message_repository import MessageRepository
from src.repositories.user_repository import UserRepository


class MongoUnitOfWork(UnitOfWorkPort):
    def __init__(self, session: DatabaseSession) -> None:
        self.session = session

    def commit(self) -> None:
        self.session.commit()

    def refresh(self, entity: object) -> None:
        self.session.refresh(entity)


class MongoUserRepository(UserRepositoryPort):
    def __init__(self, session: DatabaseSession) -> None:
        self.repository = UserRepository(session)

    def add(self, entity):
        return self.repository.add(entity)

    def get(self, entity_id: int):
        return self.repository.get(entity_id)

    def list_all(self):
        return self.repository.list_all()

    def delete(self, entity) -> None:
        self.repository.delete(entity)

    def get_by_email(self, email: str):
        return self.repository.get_by_email(email)

    def has_related_content(self, user_id: int) -> bool:
        return self.repository.has_related_content(user_id)


class MongoCategoryRepository(CategoryRepositoryPort):
    def __init__(self, session: DatabaseSession) -> None:
        self.repository = CategoryRepository(session)

    def add(self, entity):
        return self.repository.add(entity)

    def get(self, entity_id: int):
        return self.repository.get(entity_id)

    def list_all(self):
        return self.repository.list_all()

    def delete(self, entity) -> None:
        self.repository.delete(entity)

    def get_by_name(self, name: str):
        return self.repository.get_by_name(name)

    def has_related_listings(self, category_id: int) -> bool:
        return self.repository.has_related_listings(category_id)


class MongoListingRepository(ListingRepositoryPort):
    def __init__(self, session: DatabaseSession) -> None:
        self.repository = ListingRepository(session)

    def add(self, entity):
        return self.repository.add(entity)

    def get(self, entity_id: int):
        return self.repository.get(entity_id)

    def delete(self, entity) -> None:
        self.repository.delete(entity)

    def list_visible(self, **kwargs):
        return self.repository.list_visible(**kwargs)

    def list_for_moderation(self):
        return self.repository.list_for_moderation()

    def list_owned(self, owner_id: int):
        return self.repository.list_owned(owner_id)


class MongoMessageRepository(MessageRepositoryPort):
    def __init__(self, session: DatabaseSession) -> None:
        self.repository = MessageRepository(session)

    def add(self, entity):
        return self.repository.add(entity)

    def delete(self, entity) -> None:
        self.repository.delete(entity)

    def list_for_user(self, user_id: int):
        return self.repository.list_for_user(user_id)

    def get_for_user(self, message_id: int, user_id: int):
        return self.repository.get_for_user(message_id, user_id)
