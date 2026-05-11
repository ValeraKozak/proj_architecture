from typing import Protocol


class FileStoragePort(Protocol):
    def save_image(self, filename: str, content: bytes) -> str: ...
