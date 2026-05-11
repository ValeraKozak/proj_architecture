from src.adapters.persistence.mongodb.repositories import MongoListingRepository, MongoUnitOfWork
from src.application.common.errors import ApplicationError
from src.application.services.moderation import ModerationApplicationService
from src.db.database import DatabaseSession
from src.dto.schemas import ModerationDecisionDTO
from src.models.entities import Listing
from src.services._legacy import translate_application_error


class ModerationService:
    def __init__(self, db: DatabaseSession) -> None:
        self.service = ModerationApplicationService(
            listings=MongoListingRepository(db),
            uow=MongoUnitOfWork(db),
        )

    def review(self, listing_id: int, payload: ModerationDecisionDTO) -> Listing:
        try:
            return self.service.review(
                listing_id,
                approved=payload.approved,
                rejection_reason=payload.rejection_reason,
            )
        except ApplicationError as exc:
            raise translate_application_error(exc) from exc
