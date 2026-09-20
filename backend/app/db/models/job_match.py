import uuid
from datetime import datetime, timezone
from typing import TYPE_CHECKING, List, Any
from sqlalchemy import Integer, DateTime, ForeignKey, JSON
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base

if TYPE_CHECKING:
    from app.db.models.resume_version import ResumeVersion
    from app.db.models.job_description import JobDescription


class JobMatch(Base):
    __tablename__ = "job_matches"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    resume_version_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("resume_versions.id", ondelete="CASCADE"), index=True, nullable=False
    )
    job_description_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("job_descriptions.id", ondelete="CASCADE"), index=True, nullable=False
    )
    match_score: Mapped[int] = mapped_column(Integer, nullable=False)
    matching_skills: Mapped[List[Any]] = mapped_column(
        JSON().with_variant(JSONB, "postgresql"), default=list, nullable=False
    )
    missing_skills: Mapped[List[Any]] = mapped_column(
        JSON().with_variant(JSONB, "postgresql"), default=list, nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False
    )

    resume_version: Mapped["ResumeVersion"] = relationship("ResumeVersion", back_populates="job_matches")
    job_description: Mapped["JobDescription"] = relationship("JobDescription", back_populates="job_matches")
