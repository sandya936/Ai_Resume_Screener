import uuid
from datetime import datetime, timezone
from typing import TYPE_CHECKING, Optional, Dict, List, Any
from sqlalchemy import String, Text, Integer, DateTime, ForeignKey, JSON
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base

if TYPE_CHECKING:
    from app.db.models.resume import Resume


class ParsedResume(Base):
    __tablename__ = "parsed_resumes"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    resume_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("resumes.id", ondelete="CASCADE"), unique=True, nullable=False
    )
    raw_text: Mapped[str] = mapped_column(Text, nullable=False)
    contact_info: Mapped[Dict[str, Any]] = mapped_column(
        JSON().with_variant(JSONB, "postgresql"), default=dict, nullable=False
    )
    summary: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    work_experience: Mapped[List[Any]] = mapped_column(
        JSON().with_variant(JSONB, "postgresql"), default=list, nullable=False
    )
    education: Mapped[List[Any]] = mapped_column(
        JSON().with_variant(JSONB, "postgresql"), default=list, nullable=False
    )
    skills: Mapped[Dict[str, Any]] = mapped_column(
        JSON().with_variant(JSONB, "postgresql"), default=dict, nullable=False
    )
    projects: Mapped[List[Any]] = mapped_column(
        JSON().with_variant(JSONB, "postgresql"), default=list, nullable=False
    )
    certifications: Mapped[List[Any]] = mapped_column(
        JSON().with_variant(JSONB, "postgresql"), default=list, nullable=False
    )
    ats_score: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    ats_feedback: Mapped[Optional[Dict[str, Any]]] = mapped_column(
        JSON().with_variant(JSONB, "postgresql"), nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False
    )

    resume: Mapped["Resume"] = relationship("Resume")
