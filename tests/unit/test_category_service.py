import pytest
from fastapi import HTTPException

from src.dto.schemas import CategoryCreateDTO, CategoryUpdateDTO
from src.models.entities import Listing, User
from src.services.category_service import CategoryService


def test_create_category(db_session):
    category = CategoryService(db_session).create(
        CategoryCreateDTO(name="Vehicles", description="Cars, bikes, scooters")
    )
    assert category.id is not None


@pytest.mark.parametrize(
    "name",
    [
        "Vehicles",
        "Real Estate",
        "Jobs",
        "Services",
        "Pets",
        "Fashion",
        "Home",
        "Garden",
        "Sports",
        "Books",
    ],
)
def test_create_multiple_unique_categories(db_session, name):
    category = CategoryService(db_session).create(
        CategoryCreateDTO(name=name, description=f"{name} description")
    )
    assert category.name == name


def test_duplicate_category_rejected(db_session):
    service = CategoryService(db_session)
    service.create(CategoryCreateDTO(name="Electronics", description="Devices and gadgets"))
    with pytest.raises(HTTPException):
        service.create(CategoryCreateDTO(name="Electronics", description="Duplicate name"))


def test_get_category_by_id(db_session):
    category = CategoryService(db_session).create(
        CategoryCreateDTO(name="Garden", description="Outdoor and gardening supplies")
    )
    fetched = CategoryService(db_session).get_by_id(category.id)
    assert fetched.id == category.id


def test_update_category(db_session):
    service = CategoryService(db_session)
    category = service.create(CategoryCreateDTO(name="Home", description="Home accessories"))
    updated = service.update(
        category.id,
        CategoryUpdateDTO(name="Home Decor", description="Decor and furniture"),
    )
    assert updated.name == "Home Decor"


def test_delete_category_without_listings(db_session):
    service = CategoryService(db_session)
    category = service.create(CategoryCreateDTO(name="Travel", description="Travel items"))
    service.delete(category.id)
    with pytest.raises(HTTPException):
        service.get_by_id(category.id)


def test_delete_category_with_listings_rejected(db_session):
    service = CategoryService(db_session)
    category = service.create(CategoryCreateDTO(name="Office", description="Office items"))
    owner = User(email="office@test.com", full_name="Office Owner", password_hash="hashed")
    db_session.add(owner)
    db_session.commit()
    db_session.add(
        Listing(
            title="Desk",
            description="Wooden office desk with enough details for validation.",
            price=80,
            owner_id=owner.id,
            category_id=category.id,
        )
    )
    db_session.commit()
    with pytest.raises(HTTPException):
        service.delete(category.id)
