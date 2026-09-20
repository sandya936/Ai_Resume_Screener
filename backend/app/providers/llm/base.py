from abc import ABC, abstractmethod
from app.domain.schemas.structured_resume import StructuredResume


class BaseLLMProvider(ABC):
    @abstractmethod
    async def parse_resume_text(self, raw_text: str) -> StructuredResume:
        """Parses raw resume text into a strongly typed StructuredResume model."""
        pass
