import os

os.environ.setdefault("APP_DATABASE_URL", "sqlite+pysqlite:///:memory:")

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from src.core.security import create_access_token
from src.db.database import Base, get_db
from src.main import app
from src.models.entities import Category, Listing, ListingStatus, Role, User

TEST_DB_URL = "sqlite+pysqlite:///:memory:"
engine = create_engine(
    TEST_DB_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(autouse=True)
def reset_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def db_session():
    session = TestingSessionLocal()
    try:
        yield session
    finally:
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
    db_session.refresh(owner)
    db_session.refresh(moderator)
    db_session.refresh(buyer)
    db_session.refresh(admin)
    return {"owner": owner, "moderator": moderator, "buyer": buyer, "admin": admin}


@pytest.fixture
def seeded_category(db_session):
    category = Category(name="Electronics", description="Phones and laptops")
    db_session.add(category)
    db_session.commit()
    db_session.refresh(category)
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
    db_session.refresh(listing)
    return listing


def auth_header(email: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {create_access_token(email)}"}
