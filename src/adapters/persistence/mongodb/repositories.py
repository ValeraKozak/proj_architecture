from __future__ import annotations

from re import escape

from pymongo import ASCENDING, DESCENDING

from src.adapters.persistence.mongodb.database import DatabaseSession
from src.application.ports.repositories import (
    CategoryRepositoryPort,
    ListingRepositoryPort,
    MessageRepositoryPort,
    UnitOfWorkPort,
    UserRepositoryPort,
)
from src.domain.entities import Category, Listing, ListingStatus, Message, User


class MongoUnitOfWork(UnitOfWorkPort):
    def __init__(self, session: DatabaseSession) -> None:
        self.session = session

    def commit(self) -> None:
        self.session.commit()

    def refresh(self, entity: object) -> None:
        self.session.refresh(entity)


class MongoUserRepository(UserRepositoryPort):
    def __init__(self, session: DatabaseSession) -> None:
        self.session = session

    def add(self, entity: User) -> User:
        return self.session.add(entity)

    def get(self, entity_id: int) -> User | None:
        return self.session.get(User, entity_id)

    def list_all(self) -> list[User]:
        return self.session.find_many(User)

    def delete(self, entity: User) -> None:
        self.session.delete(entity)

    def get_by_email(self, email: str) -> User | None:
        return self.session.find_one(User, {"email": email})

    def has_related_content(self, user_id: int) -> bool:
        return (
            self.session.count(Listing, {"owner_id": user_id}) > 0
            or self.session.count(Message, {"sender_id": user_id}) > 0
            or self.session.count(Message, {"recipient_id": user_id}) > 0
        )


class MongoCategoryRepository(CategoryRepositoryPort):
    def __init__(self, session: DatabaseSession) -> None:
        self.session = session

    def add(self, entity: Category) -> Category:
        return self.session.add(entity)

    def get(self, entity_id: int) -> Category | None:
        return self.session.get(Category, entity_id)

    def list_all(self) -> list[Category]:
        return self.session.find_many(Category)

    def delete(self, entity: Category) -> None:
        self.session.delete(entity)

    def get_by_name(self, name: str) -> Category | None:
        return self.session.find_one(Category, {"name": name})

    def has_related_listings(self, category_id: int) -> bool:
        return self.session.count(Listing, {"category_id": category_id}) > 0


class MongoListingRepository(ListingRepositoryPort):
    def __init__(self, session: DatabaseSession) -> None:
        self.session = session

    def add(self, entity: Listing) -> Listing:
        return self.session.add(entity)

    def get(self, entity_id: int) -> Listing | None:
        return self.session.get(Listing, entity_id)

    def delete(self, entity: Listing) -> None:
        self.session.delete(entity)

    def list_visible(
        self,
        *,
        query: str | None = None,
        category_id: int | None = None,
        min_price: float | None = None,
        max_price: float | None = None,
        sort_by: str = "created_at",
        sort_order: str = "desc",
    ) -> list[Listing]:
        mongo_query: dict[str, object] = {"status": ListingStatus.APPROVED.value}
        if category_id is not None:
            mongo_query["category_id"] = category_id
        if min_price is not None or max_price is not None:
            price_filter: dict[str, float] = {}
            if min_price is not None:
                price_filter["$gte"] = min_price
            if max_price is not None:
                price_filter["$lte"] = max_price
            mongo_query["price"] = price_filter
        if query:
            normalized_query = query.strip()
            category_ids = [
                category.id
                for category in self.session.find_many(
                    Category,
                    {"name": {"$regex": escape(normalized_query), "$options": "i"}},
                )
                if category.id is not None
            ]
            mongo_query["$or"] = [
                {"title": {"$regex": escape(normalized_query), "$options": "i"}},
                {"description": {"$regex": escape(normalized_query), "$options": "i"}},
                {"category_id": {"$in": category_ids or [-1]}},
            ]

        sort_direction = ASCENDING if sort_order == "asc" else DESCENDING
        sort_field = "price" if sort_by == "price" else "created_at"
        return self.session.find_many(
            Listing,
            mongo_query,
            sort=[(sort_field, sort_direction), ("id", DESCENDING)],
        )

    def list_for_moderation(self) -> list[Listing]:
        return self.session.find_many(
            Listing,
            {"status": ListingStatus.PENDING.value},
            sort=[("created_at", DESCENDING), ("id", DESCENDING)],
        )

    def list_owned(self, owner_id: int) -> list[Listing]:
        return self.session.find_many(
            Listing,
            {"owner_id": owner_id},
            sort=[("created_at", DESCENDING), ("id", DESCENDING)],
        )


class MongoMessageRepository(MessageRepositoryPort):
    def __init__(self, session: DatabaseSession) -> None:
        self.session = session

    def add(self, entity: Message) -> Message:
        return self.session.add(entity)

    def delete(self, entity: Message) -> None:
        self.session.delete(entity)

    def list_for_user(self, user_id: int) -> list[Message]:
        return self.session.find_many(
            Message,
            {"$or": [{"sender_id": user_id}, {"recipient_id": user_id}]},
            sort=[("created_at", DESCENDING), ("id", DESCENDING)],
        )

    def get_for_user(self, message_id: int, user_id: int) -> Message | None:
        return self.session.find_one(
            Message,
            {
                "id": message_id,
                "$or": [{"sender_id": user_id}, {"recipient_id": user_id}],
            },
        )
