import enum
from dataclasses import dataclass, field
from datetime import UTC, datetime


class Role(enum.StrEnum):
    USER = "user"
    MODERATOR = "moderator"
    ADMIN = "admin"


class ListingStatus(enum.StrEnum):
    DRAFT = "draft"
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    ARCHIVED = "archived"


def utc_now() -> datetime:
    return datetime.now(UTC)


@dataclass
class User:
    id: int | None = None
    email: str = ""
    full_name: str = ""
    password_hash: str = ""
    role: Role = Role.USER
    is_blocked: bool = False
    created_at: datetime = field(default_factory=utc_now)


@dataclass
class Category:
    id: int | None = None
    name: str = ""
    description: str = ""


@dataclass
class ListingImage:
    id: int | None = None
    listing_id: int | None = None
    url: str = ""
    position: int = 0


@dataclass
class Listing:
    id: int | None = None
    title: str = ""
    description: str = ""
    price: float = 0.0
    status: ListingStatus = ListingStatus.DRAFT
    rejection_reason: str | None = None
    owner_id: int | None = None
    category_id: int | None = None
    created_at: datetime = field(default_factory=utc_now)
    updated_at: datetime = field(default_factory=utc_now)
    images: list[ListingImage] = field(default_factory=list)

    @property
    def image_urls(self) -> list[str]:
        return [image.url for image in sorted(self.images, key=lambda image: image.position)]


@dataclass
class Message:
    id: int | None = None
    listing_id: int | None = None
    sender_id: int | None = None
    recipient_id: int | None = None
    body: str = ""
    created_at: datetime = field(default_factory=utc_now)
