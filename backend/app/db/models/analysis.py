import uuid
from datetime import datetime, timezone
from typing import TYPE_CHECKING, Optional, Dict, Any
from sqlalchemy import String, Integer, DateTime, ForeignKey, JSON
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base

if TYPE_CHECKING:
    from app.db.models.resume_version import ResumeVersion


class Analysis(Base):
    __tablename__ = "analyses"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    resume_version_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("resume_versions.id", ondelete="CASCADE"), index=True, nullable=False
    )
    analysis_type: Mapped[str] = mapped_column(String(100), nullable=False) # e.g. 'ats_score', 'structure_audit'
    status: Mapped[str] = mapped_column(String(50), default="pending", nullable=False)
    score: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    payload: Mapped[Dict[str, Any]] = mapped_column(
        JSON().with_variant(JSONB, "postgresql"), default=dict, nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False
    )

    resume_version: Mapped["ResumeVersion"] = relationship("ResumeVersion", back_populates="analyses")
