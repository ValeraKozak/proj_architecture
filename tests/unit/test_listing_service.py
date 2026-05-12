import pytest

from src.adapters.persistence.mongodb.repositories import (
    MongoCategoryRepository,
    MongoListingRepository,
    MongoUnitOfWork,
    MongoUserRepository,
)
from src.application.common.errors import ForbiddenError, NotFoundError
from src.application.services.listings import ListingApplicationService
from src.domain.entities import Category, ListingStatus, User


def build_service(db_session):
    return ListingApplicationService(
        listings=MongoListingRepository(db_session),
        categories=MongoCategoryRepository(db_session),
        users=MongoUserRepository(db_session),
        uow=MongoUnitOfWork(db_session),
    )


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
    listing = build_service(db_session).create(
        title="iPhone 14 Pro",
        description="Used phone in great condition with charger and long enough text.",
        price=900,
        category_id=category.id,
        image_urls=["https://images.example.com/iphone-front.jpg"],
        owner=owner,
    )
    assert listing.status == ListingStatus.PENDING
    assert listing.image_urls == ["https://images.example.com/iphone-front.jpg"]


@pytest.mark.parametrize("price", [1, 5, 10, 49.99, 100, 250, 999.99, 1500, 2500, 5000])
def test_create_listing_accepts_positive_prices(db_session, owner_and_category, price):
    owner, category = owner_and_category
    listing = build_service(db_session).create(
        title=f"Valid title {price}",
        description="Long enough description for a valid listing submission text.",
        price=price,
        category_id=category.id,
        image_urls=[],
        owner=owner,
    )
    assert listing.price == price


def test_create_listing_rejects_missing_category(db_session, owner_and_category):
    owner, _ = owner_and_category
    with pytest.raises(NotFoundError):
        build_service(db_session).create(
            title="Missing category",
            description="Long enough description to pass dto validation.",
            price=10,
            category_id=999,
            image_urls=[],
            owner=owner,
        )


def test_create_listing_rejects_blocked_owner(db_session, owner_and_category):
    owner, category = owner_and_category
    owner.is_blocked = True
    db_session.commit()
    with pytest.raises(ForbiddenError):
        build_service(db_session).create(
            title="Blocked owner",
            description="Long enough description to pass dto validation.",
            price=100,
            category_id=category.id,
            image_urls=[],
            owner=owner,
        )


@pytest.mark.parametrize(
    ("title", "price"),
    [(f"Updated title {index}", 19 + index) for index in range(1, 11)],
)
def test_update_listing_resets_status(db_session, owner_and_category, title, price):
    owner, category = owner_and_category
    service = build_service(db_session)
    listing = service.create(
        title="Original title",
        description="Original long enough description for listing submission.",
        price=19,
        category_id=category.id,
        image_urls=[],
        owner=owner,
    )
    listing.status = ListingStatus.REJECTED
    listing.rejection_reason = "Fix details"
    db_session.commit()
    updated = service.update(
        listing.id,
        title=title,
        description=None,
        price=price,
        category_id=None,
        image_urls=["https://images.example.com/updated-listing.jpg"],
        owner=owner,
    )
    assert updated.status == ListingStatus.PENDING
    assert updated.rejection_reason is None
    assert updated.image_urls == ["https://images.example.com/updated-listing.jpg"]


def test_get_owned_listings_returns_owner_items(db_session, owner_and_category):
    owner, category = owner_and_category
    service = build_service(db_session)
    service.create(
        title="Owner listing",
        description="Detailed description for owner listing in owned list test.",
        price=50,
        category_id=category.id,
        image_urls=[],
        owner=owner,
    )
    listings = service.get_owned(owner)
    assert len(listings) == 1


def test_get_public_listings_supports_search_and_filters(db_session, owner_and_category):
    owner, category = owner_and_category
    furniture = Category(name="Furniture", description="Home and office furniture")
    db_session.add(furniture)
    db_session.commit()
    db_session.refresh(furniture)

    service = build_service(db_session)
    matching = service.create(
        title="Gaming Chair Pro",
        description="Comfortable ergonomic chair with headrest and adjustable armrests.",
        price=220,
        category_id=furniture.id,
        image_urls=[],
        owner=owner,
    )
    matching.status = ListingStatus.APPROVED
    ignored = service.create(
        title="Desk Lamp",
        description="Bright lamp with long enough text for the validation rules.",
        price=45,
        category_id=category.id,
        image_urls=[],
        owner=owner,
    )
    ignored.status = ListingStatus.APPROVED
    db_session.commit()

    listings = service.get_public(query="chair", min_price=100, sort_by="price", sort_order="asc")
    assert [listing.id for listing in listings] == [matching.id]
    assert ignored.id not in [listing.id for listing in listings]


def test_get_listing_by_id_visible_for_owner(db_session, owner_and_category):
    owner, category = owner_and_category
    service = build_service(db_session)
    listing = service.create(
        title="Hidden listing",
        description="Pending listing with enough details for owner access.",
        price=75,
        category_id=category.id,
        image_urls=[],
        owner=owner,
    )
    fetched = service.get_by_id(listing.id, owner)
    assert fetched.id == listing.id


def test_delete_listing_archives_listing(db_session, owner_and_category):
    owner, category = owner_and_category
    service = build_service(db_session)
    listing = service.create(
        title="Archive me",
        description="Listing description long enough for archive deletion scenario.",
        price=42,
        category_id=category.id,
        image_urls=[],
        owner=owner,
    )
    service.delete(listing.id, owner)
    with pytest.raises(NotFoundError):
        service.get_by_id(listing.id, owner)
