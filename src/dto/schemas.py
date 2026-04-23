from datetime import datetime

from pydantic import BaseModel, EmailStr, Field, field_validator

from src.models.entities import ListingStatus, Role


class UserCreateDTO(BaseModel):
    email: EmailStr
    full_name: str = Field(min_length=2, max_length=255)
    password: str = Field(min_length=8, max_length=128)


class UserLoginDTO(BaseModel):
    email: EmailStr
    password: str


class UserReadDTO(BaseModel):
    id: int
    email: EmailStr
    full_name: str
    role: Role
    is_blocked: bool

    model_config = {"from_attributes": True}


class TokenDTO(BaseModel):
    access_token: str
    token_type: str = "bearer"


class CategoryCreateDTO(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    description: str = Field(min_length=5, max_length=255)


class CategoryReadDTO(CategoryCreateDTO):
    id: int

    model_config = {"from_attributes": True}


class ListingCreateDTO(BaseModel):
    title: str = Field(min_length=5, max_length=150)
    description: str = Field(min_length=20, max_length=5000)
    price: float = Field(gt=0)
    category_id: int

    @field_validator("title")
    @classmethod
    def strip_title(cls, value: str) -> str:
        return value.strip()


class ListingUpdateDTO(BaseModel):
    title: str | None = Field(default=None, min_length=5, max_length=150)
    description: str | None = Field(default=None, min_length=20, max_length=5000)
    price: float | None = Field(default=None, gt=0)
    category_id: int | None = None


class ListingReadDTO(BaseModel):
    id: int
    title: str
    description: str
    price: float
    status: ListingStatus
    rejection_reason: str | None
    owner_id: int
    category_id: int
    created_at: datetime | None = None

    model_config = {"from_attributes": True}


class ModerationDecisionDTO(BaseModel):
    approved: bool
    rejection_reason: str | None = Field(default=None, max_length=255)


class MessageCreateDTO(BaseModel):
    listing_id: int
    recipient_id: int
    body: str = Field(min_length=1, max_length=1000)


class MessageReadDTO(BaseModel):
    id: int
    listing_id: int
    sender_id: int
    recipient_id: int
    body: str
    created_at: datetime | None = None

    model_config = {"from_attributes": True}

