import pytest
from fastapi import HTTPException

from src.dto.schemas import ListingCreateDTO, ListingUpdateDTO
from src.models.entities import Category, ListingStatus, User
from src.services.listing_service import ListingService


@pytest.fixture
def owner_and_category(db_session):
    owner = User(email="owner@test.com", full_name="Owner", password_hash="hashed")
    category = Category(name="Electronics", description="Devices")
    db_session.add_all([owner, category])
    db_session.commit()
    db_session.refresh(owner)
    db_session.refresh(category)
    return owner, category


def test_create_listing_sets_pending_status(db_session, owner_and_category):
    owner, category = owner_and_category
    listing = ListingService(db_session).create(
        ListingCreateDTO(
            title="iPhone 14 Pro",
            description="Used phone in great condition with charger and long enough text.",
            price=900,
            category_id=category.id,
        ),
        owner,
    )
    assert listing.status == ListingStatus.PENDING


@pytest.mark.parametrize("price", [1, 5, 10, 49.99, 100, 250, 999.99, 1500, 2500, 5000])
def test_create_listing_accepts_positive_prices(db_session, owner_and_category, price):
    owner, category = owner_and_category
    listing = ListingService(db_session).create(
        ListingCreateDTO(
            title=f"Valid title {price}",
            description="Long enough description for a valid listing submission text.",
            price=price,
            category_id=category.id,
        ),
        owner,
    )
    assert listing.price == price


def test_create_listing_rejects_missing_category(db_session, owner_and_category):
    owner, _ = owner_and_category
    with pytest.raises(HTTPException):
        ListingService(db_session).create(
            ListingCreateDTO(
                title="Missing category",
                description="Long enough description to pass dto validation.",
                price=10,
                category_id=999,
            ),
            owner,
        )


def test_create_listing_rejects_blocked_owner(db_session, owner_and_category):
    owner, category = owner_and_category
    owner.is_blocked = True
    db_session.commit()
    with pytest.raises(HTTPException):
        ListingService(db_session).create(
            ListingCreateDTO(
                title="Blocked owner",
                description="Long enough description to pass dto validation.",
                price=100,
                category_id=category.id,
            ),
            owner,
        )


@pytest.mark.parametrize(
    ("title", "price"),
    [
        ("Updated title 1", 20),
        ("Updated title 2", 21),
        ("Updated title 3", 22),
        ("Updated title 4", 23),
        ("Updated title 5", 24),
        ("Updated title 6", 25),
        ("Updated title 7", 26),
        ("Updated title 8", 27),
        ("Updated title 9", 28),
        ("Updated title 10", 29),
    ],
)
def test_update_listing_resets_status(db_session, owner_and_category, title, price):
    owner, category = owner_and_category
    service = ListingService(db_session)
    listing = service.create(
        ListingCreateDTO(
            title="Original title",
            description="Original long enough description for listing submission.",
            price=19,
            category_id=category.id,
        ),
        owner,
    )
    listing.status = ListingStatus.REJECTED
    listing.rejection_reason = "Fix details"
    db_session.commit()
    updated = service.update(
        listing.id,
        ListingUpdateDTO(title=title, price=price),
        owner,
    )
    assert updated.status == ListingStatus.PENDING
    assert updated.rejection_reason is None


def test_get_owned_listings_returns_owner_items(db_session, owner_and_category):
    owner, category = owner_and_category
    service = ListingService(db_session)
    service.create(
        ListingCreateDTO(
            title="Owner listing",
            description="Detailed description for owner listing in owned list test.",
            price=50,
            category_id=category.id,
        ),
        owner,
    )
    listings = service.get_owned(owner)
    assert len(listings) == 1


def test_get_listing_by_id_visible_for_owner(db_session, owner_and_category):
    owner, category = owner_and_category
    service = ListingService(db_session)
    listing = service.create(
        ListingCreateDTO(
            title="Hidden listing",
            description="Pending listing with enough details for owner access.",
            price=75,
            category_id=category.id,
        ),
        owner,
    )
    fetched = service.get_by_id(listing.id, owner)
    assert fetched.id == listing.id


def test_delete_listing_archives_listing(db_session, owner_and_category):
    owner, category = owner_and_category
    service = ListingService(db_session)
    listing = service.create(
        ListingCreateDTO(
            title="Archive me",
            description="Listing description long enough for archive deletion scenario.",
            price=42,
            category_id=category.id,
        ),
        owner,
    )
    result = service.delete(listing.id, owner)
    assert result.message == "Listing deleted"
    with pytest.raises(HTTPException):
        service.get_by_id(listing.id, owner)
