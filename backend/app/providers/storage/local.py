import os
import uuid
import aiofiles
from pathlib import Path
from typing import Optional
from app.core.config import settings
from app.providers.storage.base import BaseStorageProvider


class LocalStorageProvider(BaseStorageProvider):
    def __init__(self, base_dir: Optional[str] = None):
        self.base_dir = Path(base_dir or settings.UPLOAD_STORAGE_PATH) / "resumes"
        self.base_dir.mkdir(parents=True, exist_ok=True)

    async def save_file(self, file_bytes: bytes, filename: str, content_type: str) -> str:
        # Generate safe UUID filename preserving extension
        ext = Path(filename).suffix.lower()
        unique_name = f"{uuid.uuid4().hex}{ext}"
        relative_path = os.path.join("resumes", unique_name)
        full_path = self.base_dir / unique_name

        async with aiofiles.open(full_path, "wb") as f:
            await f.write(file_bytes)

        return relative_path

    async def get_file(self, storage_path: str) -> Optional[bytes]:
        full_path = Path(settings.UPLOAD_STORAGE_PATH) / storage_path
        if not full_path.exists():
            return None
        async with aiofiles.open(full_path, "rb") as f:
            return await f.read()

    async def delete_file(self, storage_path: str) -> bool:
        full_path = Path(settings.UPLOAD_STORAGE_PATH) / storage_path
        if full_path.exists():
            try:
                os.remove(full_path)
                return True
            except OSError:
                return False
        return False
