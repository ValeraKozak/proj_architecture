import mongomock

from src.db.database import DatabaseSession, initialize_database
from src.models.entities import Category, Listing, ListingStatus, User


def test_mongodb_bootstrap_supports_related_documents():
    database = mongomock.MongoClient()["mongo_bootstrap"]
    initialize_database(database)
    session = DatabaseSession(database)

    user = User(email="mongo@example.com", full_name="Mongo User", password_hash="hashed")
    category = Category(name="Mongo Tech", description="Mongo tech goods")
    session.add_all([user, category])
    session.commit()

    listing = Listing(
        title="Mongo Listing",
        description="Listing stored in MongoDB with enough text for validation.",
        price=150.0,
        status=ListingStatus.APPROVED,
        owner_id=user.id,
        category_id=category.id,
    )
    session.add(listing)
    session.commit()

    assert database["users"].count_documents({}) == 1
    assert database["categories"].count_documents({}) == 1
    assert database["listings"].count_documents({}) == 1


def test_mongodb_bootstrap_uses_numeric_counters():
    database = mongomock.MongoClient()["mongo_counters"]
    initialize_database(database)
    session = DatabaseSession(database)

    first = User(email="first@example.com", full_name="First User", password_hash="hashed")
    second = User(email="second@example.com", full_name="Second User", password_hash="hashed")
    session.add_all([first, second])
    session.commit()

    assert first.id == 1
    assert second.id == 2
