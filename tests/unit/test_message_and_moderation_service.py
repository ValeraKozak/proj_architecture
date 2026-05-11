import pytest

from src.adapters.persistence.mongodb.repositories import (
    MongoListingRepository,
    MongoMessageRepository,
    MongoUnitOfWork,
    MongoUserRepository,
)
from src.application.common.errors import NotFoundError, ValidationError
from src.application.services.messages import MessageApplicationService
from src.application.services.moderation import ModerationApplicationService
from src.models.entities import Category, Listing, ListingStatus, Role, User


def build_message_service(db_session):
    return MessageApplicationService(
        messages=MongoMessageRepository(db_session),
        listings=MongoListingRepository(db_session),
        users=MongoUserRepository(db_session),
        uow=MongoUnitOfWork(db_session),
    )


def build_moderation_service(db_session):
    return ModerationApplicationService(
        listings=MongoListingRepository(db_session),
        uow=MongoUnitOfWork(db_session),
    )


@pytest.fixture
def message_context(db_session):
    category = Category(name="Tech", description="Tech items")
    owner = User(email="owner@msg.com", full_name="Owner", password_hash="hashed")
    buyer = User(email="buyer@msg.com", full_name="Buyer", password_hash="hashed")
    moderator = User(
        email="mod@msg.com", full_name="Moderator", password_hash="hashed", role=Role.MODERATOR
    )
    db_session.add_all([category, owner, buyer, moderator])
    db_session.commit()
    listing = Listing(
        title="Console",
        description="Approved gaming console with accessories and detailed description.",
        price=300,
        status=ListingStatus.APPROVED,
        owner_id=owner.id,
        category_id=category.id,
    )
    pending_listing = Listing(
        title="Phone",
        description="Pending phone offer with detailed description for moderation.",
        price=200,
        status=ListingStatus.PENDING,
        owner_id=owner.id,
        category_id=category.id,
    )
    db_session.add_all([listing, pending_listing])
    db_session.commit()
    db_session.refresh(listing)
    db_session.refresh(pending_listing)
    return {
        "owner": owner,
        "buyer": buyer,
        "moderator": moderator,
        "listing": listing,
        "pending_listing": pending_listing,
    }


@pytest.mark.parametrize(
    "body",
    [
        "Is this item still available?",
        "Can you lower the price?",
        "Do you ship nationwide?",
        "Can I inspect it tomorrow?",
        "What is the condition of the battery?",
        "Do you have the receipt?",
        "Can we meet in the city center?",
        "Any scratches or defects?",
        "Would you accept cash?",
        "Please send more photos.",
    ],
)
def test_send_message_success_cases(db_session, message_context, body):
    message = build_message_service(db_session).send(
        listing_id=message_context["listing"].id,
        recipient_id=message_context["owner"].id,
        body=body,
        sender=message_context["buyer"],
    )
    assert message.body == body


def test_send_message_rejects_self_message(db_session, message_context):
    with pytest.raises(ValidationError):
        build_message_service(db_session).send(
            listing_id=message_context["listing"].id,
            recipient_id=message_context["buyer"].id,
            body="Hello",
            sender=message_context["buyer"],
        )


def test_send_message_rejects_unapproved_listing(db_session, message_context):
    with pytest.raises(ValidationError):
        build_message_service(db_session).send(
            listing_id=message_context["pending_listing"].id,
            recipient_id=message_context["owner"].id,
            body="Hello",
            sender=message_context["buyer"],
        )


def test_get_and_delete_user_message(db_session, message_context):
    service = build_message_service(db_session)
    message = service.send(
        listing_id=message_context["listing"].id,
        recipient_id=message_context["owner"].id,
        body="Checking message retrieval flow.",
        sender=message_context["buyer"],
    )
    fetched = service.get_user_message(message.id, message_context["buyer"].id)
    assert fetched.id == message.id
    service.delete_user_message(message.id, message_context["buyer"].id)
    with pytest.raises(NotFoundError):
        service.get_user_message(message.id, message_context["buyer"].id)


@pytest.mark.parametrize(
    ("approved", "reason", "expected_status"),
    [
        (True, None, ListingStatus.APPROVED),
        (False, "Spam content", ListingStatus.REJECTED),
        (False, "Wrong category", ListingStatus.REJECTED),
        (False, "Missing price details", ListingStatus.REJECTED),
        (False, "Suspicious description", ListingStatus.REJECTED),
        (False, "Duplicate post", ListingStatus.REJECTED),
        (False, "Forbidden item", ListingStatus.REJECTED),
        (False, "Low quality content", ListingStatus.REJECTED),
        (False, "Contact data in title", ListingStatus.REJECTED),
        (False, "Incomplete item details", ListingStatus.REJECTED),
    ],
)
def test_moderation_review_paths(db_session, message_context, approved, reason, expected_status):
    pending = message_context["pending_listing"]
    if pending.status != ListingStatus.PENDING:
        pending.status = ListingStatus.PENDING
        db_session.commit()
    result = build_moderation_service(db_session).review(
        pending.id,
        approved=approved,
        rejection_reason=reason,
    )
    assert result.status == expected_status


def test_moderation_requires_reason_for_rejection(db_session, message_context):
    with pytest.raises(ValidationError):
        build_moderation_service(db_session).review(
            message_context["pending_listing"].id,
            approved=False,
            rejection_reason=None,
        )
