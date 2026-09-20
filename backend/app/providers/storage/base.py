from abc import ABC, abstractmethod
from typing import Optional


class BaseStorageProvider(ABC):
    @abstractmethod
    async def save_file(self, file_bytes: bytes, filename: str, content_type: str) -> str:
        """Saves file bytes and returns storage path / reference."""
        pass

    @abstractmethod
    async def get_file(self, storage_path: str) -> Optional[bytes]:
        """Retrieves raw file bytes from storage."""
        pass

    @abstractmethod
    async def delete_file(self, storage_path: str) -> bool:
        """Deletes file from storage."""
        pass
