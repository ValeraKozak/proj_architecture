import pytest
from fastapi import HTTPException

from src.dto.schemas import CategoryCreateDTO
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

