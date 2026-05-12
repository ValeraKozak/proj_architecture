from dataclasses import dataclass, field
from datetime import datetime

from src.domain.entities import ListingStatus


@dataclass
class ListingDetails:
    id: int | None
    title: str
    description: str
    price: float
    status: ListingStatus
    rejection_reason: str | None
    owner_id: int | None
    owner_name: str | None
    category_id: int | None
    created_at: datetime | None
    image_urls: list[str] = field(default_factory=list)


@dataclass
class MessageDetails:
    id: int | None
    listing_id: int | None
    sender_id: int | None
    sender_name: str | None
    recipient_id: int | None
    recipient_name: str | None
    body: str
    created_at: datetime | None
