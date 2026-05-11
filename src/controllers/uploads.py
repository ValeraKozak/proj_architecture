from fastapi import APIRouter, Depends, File, UploadFile

from src.adapters.http.dependencies import get_upload_service
from src.adapters.http.security import get_current_user
from src.application.services import UploadApplicationService
from src.dto.schemas import UploadImageBatchDTO, UploadImageReadDTO
from src.models.entities import User

router = APIRouter(prefix="/uploads", tags=["uploads"])


@router.post("/images", response_model=UploadImageBatchDTO, status_code=201)
async def upload_images(
    files: list[UploadFile] = File(...),
    service: UploadApplicationService = Depends(get_upload_service),
    current_user: User = Depends(get_current_user),
) -> UploadImageBatchDTO:
    materialized_files: list[tuple[str | None, str | None, bytes]] = []
    for file in files:
        materialized_files.append((file.filename, file.content_type, await file.read()))
    urls = service.upload_images(files=materialized_files, current_user=current_user)
    return UploadImageBatchDTO(files=[UploadImageReadDTO(url=url) for url in urls])
