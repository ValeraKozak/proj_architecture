import secrets

from src.application.common.errors import ForbiddenError, ValidationError
from src.application.ports.storage import FileStoragePort
from src.domain.entities import User

ALLOWED_CONTENT_TYPES: dict[str, str] = {
    "image/jpeg": ".jpg",
    "image/png": ".png",
    "image/webp": ".webp",
    "image/gif": ".gif",
}
MAX_FILES_PER_REQUEST = 6
MAX_FILE_SIZE_BYTES = 5 * 1024 * 1024


class UploadApplicationService:
    def __init__(self, storage: FileStoragePort, uploads_url_prefix: str) -> None:
        self.storage = storage
        self.uploads_url_prefix = uploads_url_prefix.rstrip("/")

    def upload_images(
        self,
        *,
        files: list[tuple[str | None, str | None, bytes]],
        current_user: User,
    ) -> list[str]:
        if current_user.is_blocked:
            raise ForbiddenError("Blocked users cannot upload images")
        if not files:
            raise ValidationError("No files provided")
        if len(files) > MAX_FILES_PER_REQUEST:
            raise ValidationError(f"You can upload at most {MAX_FILES_PER_REQUEST} images at once")

        uploaded_urls: list[str] = []
        for original_name, content_type, content in files:
            extension = ALLOWED_CONTENT_TYPES.get(content_type or "")
            if extension is None:
                raise ValidationError(f"Unsupported image type: {content_type or 'unknown'}")
            if not content:
                raise ValidationError(f"File {original_name or 'image'} is empty")
            if len(content) > MAX_FILE_SIZE_BYTES:
                raise ValidationError(f"File {original_name or 'image'} is larger than 5 MB")

            filename = f"{secrets.token_hex(16)}{extension}"
            stored_name = self.storage.save_image(filename, content)
            uploaded_urls.append(f"{self.uploads_url_prefix}/{stored_name}")

        return uploaded_urls
