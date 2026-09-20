from abc import ABC, abstractmethod
from app.services.document_processing.schemas import NormalizedDocument


class BaseDocumentExtractor(ABC):
    @abstractmethod
    def extract(self, file_bytes: bytes, filename: str) -> NormalizedDocument:
        """Extracts text and normalized structural entities from raw file bytes."""
        pass
