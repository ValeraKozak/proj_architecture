from fastapi import Depends

from src.adapters.http.security_services import PasswordManagerAdapter, TokenServiceAdapter
from src.adapters.persistence.mongodb.database import DatabaseSession, get_db
from src.adapters.persistence.mongodb.repositories import (
    MongoCategoryRepository,
    MongoListingRepository,
    MongoMessageRepository,
    MongoUnitOfWork,
    MongoUserRepository,
)
from src.adapters.storage.local_files import LocalFileStorageAdapter
from src.application.services import (
    AuthApplicationService,
    CategoryApplicationService,
    ListingApplicationService,
    MessageApplicationService,
    ModerationApplicationService,
    UploadApplicationService,
    UserApplicationService,
)
from src.core.config import get_settings


def get_auth_service(db: DatabaseSession = Depends(get_db)) -> AuthApplicationService:
    return AuthApplicationService(
        users=MongoUserRepository(db),
        uow=MongoUnitOfWork(db),
        password_manager=PasswordManagerAdapter(),
        token_service=TokenServiceAdapter(),
    )


def get_category_service(db: DatabaseSession = Depends(get_db)) -> CategoryApplicationService:
    return CategoryApplicationService(
        categories=MongoCategoryRepository(db),
        uow=MongoUnitOfWork(db),
    )


def get_listing_service(db: DatabaseSession = Depends(get_db)) -> ListingApplicationService:
    return ListingApplicationService(
        listings=MongoListingRepository(db),
        categories=MongoCategoryRepository(db),
        users=MongoUserRepository(db),
        uow=MongoUnitOfWork(db),
    )


def get_message_service(db: DatabaseSession = Depends(get_db)) -> MessageApplicationService:
    return MessageApplicationService(
        messages=MongoMessageRepository(db),
        listings=MongoListingRepository(db),
        users=MongoUserRepository(db),
        uow=MongoUnitOfWork(db),
    )


def get_moderation_service(db: DatabaseSession = Depends(get_db)) -> ModerationApplicationService:
    return ModerationApplicationService(
        listings=MongoListingRepository(db),
        uow=MongoUnitOfWork(db),
    )


def get_user_service(db: DatabaseSession = Depends(get_db)) -> UserApplicationService:
    return UserApplicationService(
        users=MongoUserRepository(db),
        uow=MongoUnitOfWork(db),
    )


def get_upload_service() -> UploadApplicationService:
    settings = get_settings()
    return UploadApplicationService(
        storage=LocalFileStorageAdapter(settings.upload_dir),
        uploads_url_prefix=settings.uploads_url_prefix,
    )
