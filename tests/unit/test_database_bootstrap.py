import mongomock

from src.db.database import DatabaseSession, initialize_database, reset_database
from src.models.entities import Category, User


def test_initialize_database_creates_expected_collections():
    database = mongomock.MongoClient()["bootstrap_test"]

    initialize_database(database)

    assert {"users", "categories", "listings", "listing_images", "messages"}.issubset(
        set(database.list_collection_names())
    )


def test_reset_database_clears_collections_but_keeps_runtime_usable():
    database = mongomock.MongoClient()["reset_test"]
    initialize_database(database)
    session = DatabaseSession(database)
    session.add(User(email="reset@example.com", full_name="Reset User", password_hash="hashed"))
    session.add(Category(name="Reset", description="Reset description"))
    session.commit()

    reset_database(session)
    initialize_database(database)

    assert database["users"].count_documents({}) == 0
    assert database["categories"].count_documents({}) == 0
