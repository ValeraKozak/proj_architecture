import os

os.environ.setdefault("APP_DATABASE_URL", "mongomock://localhost/bulletin_board_test")

import mongomock
import pytest
from fastapi.testclient import TestClient

from src.adapters.http.security_services import create_access_token
from src.adapters.persistence.mongodb.database import (
    DatabaseSession,
    get_db,
    initialize_database,
    reset_database,
)
from src.domain.entities import Category, Listing, ListingStatus, Role, User
from src.main import app


@pytest.fixture
def db_session():
    client = mongomock.MongoClient()
    database = client["bulletin_board_test"]
    initialize_database(database)
    session = DatabaseSession(database)
    reset_database(session)
    initialize_database(database)
    try:
        yield session
    finally:
        reset_database(session)
        session.close()


@pytest.fixture
def client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as api_client:
        yield api_client
    app.dependency_overrides.clear()


@pytest.fixture
def seeded_users(db_session):
    owner = User(
        email="owner@example.com",
        full_name="Owner User",
        password_hash="hashed",
        role=Role.USER,
    )
    moderator = User(
        email="moderator@example.com",
        full_name="Moderator User",
        password_hash="hashed",
        role=Role.MODERATOR,
    )
    buyer = User(
        email="buyer@example.com",
        full_name="Buyer User",
        password_hash="hashed",
        role=Role.USER,
    )
    admin = User(
        email="admin@example.com",
        full_name="Admin User",
        password_hash="hashed",
        role=Role.ADMIN,
    )
    db_session.add_all([owner, moderator, buyer, admin])
    db_session.commit()
    return {"owner": owner, "moderator": moderator, "buyer": buyer, "admin": admin}


@pytest.fixture
def seeded_category(db_session):
    category = Category(name="Electronics", description="Phones and laptops")
    db_session.add(category)
    db_session.commit()
    return category


@pytest.fixture
def approved_listing(db_session, seeded_users, seeded_category):
    listing = Listing(
        title="Gaming laptop",
        description="Powerful laptop with RTX graphics and long description.",
        price=1250.0,
        status=ListingStatus.APPROVED,
        owner_id=seeded_users["owner"].id,
        category_id=seeded_category.id,
    )
    db_session.add(listing)
    db_session.commit()
    return listing


def auth_header(email: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {create_access_token(email)}"}
