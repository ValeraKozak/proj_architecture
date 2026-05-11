from pathlib import Path

from src.application.ports.storage import FileStoragePort


class LocalFileStorageAdapter(FileStoragePort):
    def __init__(self, upload_dir: str) -> None:
        self.upload_dir = Path(upload_dir)
        self.upload_dir.mkdir(parents=True, exist_ok=True)

    def save_image(self, filename: str, content: bytes) -> str:
        destination = self.upload_dir / filename
        destination.write_bytes(content)
        return filename
