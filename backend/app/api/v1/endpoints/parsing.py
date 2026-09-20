import uuid
from typing import Any, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.api.deps import get_db, get_current_active_user, verify_resource_owner
from app.db.models.user import User
from app.db.models.resume import Resume
from app.db.models.parsed_resume import ParsedResume
from app.domain.schemas.structured_resume import (
    StructuredResume,
    PersonalInfo,
    SkillCategory,
    EducationEntry,
    WorkExperienceEntry,
    ProjectEntry,
    CertificationEntry,
)
from app.services.resume_parser import ResumeParserService

router = APIRouter()


@router.post("/{resume_id}/parse")
async def parse_resume(
    resume_id: uuid.UUID,
    version_id: Optional[uuid.UUID] = Query(None),
    provider: Optional[str] = Query(None),
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
) -> Any:
    # 1. Fetch resume and verify ownership
    result = await db.execute(
        select(Resume).options(selectinload(Resume.versions)).where(Resume.id == resume_id)
    )
    resume = result.scalar_one_or_none()

    if not resume:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "success": False,
                "data": None,
                "error": {
                    "code": "RESUME_NOT_FOUND",
                    "message": "Resume not found",
                    "details": [],
                },
            },
        )
    verify_resource_owner(resume.user_id, current_user.id)

    if not resume.versions:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "success": False,
                "data": None,
                "error": {
                    "code": "NO_RESUME_VERSIONS",
                    "message": "Resume has no uploaded version revisions to parse",
                    "details": [],
                },
            },
        )

    # Resolve target version (latest if not specified)
    target_version_id = version_id or resume.versions[-1].id

    # 2. Trigger ResumeParserService
    parser_service = ResumeParserService(db)
    structured_resume = await parser_service.parse_version(target_version_id, provider_name=provider)

    return {
        "success": True,
        "data": {
            "resume_id": str(resume.id),
            "version_id": str(target_version_id),
            "structured_profile": structured_resume.model_dump(),
        },
        "error": None,
    }


@router.get("/{resume_id}/parsed")
async def get_parsed_resume(
    resume_id: uuid.UUID,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
) -> Any:
    # 1. Fetch resume and verify ownership
    result_res = await db.execute(select(Resume).where(Resume.id == resume_id))
    resume = result_res.scalar_one_or_none()

    if not resume:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "success": False,
                "data": None,
                "error": {
                    "code": "RESUME_NOT_FOUND",
                    "message": "Resume not found",
                    "details": [],
                },
            },
        )
    verify_resource_owner(resume.user_id, current_user.id)

    # 2. Fetch ParsedResume record
    result_parsed = await db.execute(
        select(ParsedResume).where(ParsedResume.resume_id == resume_id)
    )
    parsed_record = result_parsed.scalar_one_or_none()

    if not parsed_record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "success": False,
                "data": None,
                "error": {
                    "code": "PARSED_RESUME_NOT_FOUND",
                    "message": "Resume has not been parsed yet. Call POST /resumes/{id}/parse first.",
                    "details": [],
                },
            },
        )

    # Reconstruct StructuredResume Pydantic entity
    structured_profile = StructuredResume(
        personal_info=PersonalInfo(**parsed_record.contact_info),
        summary=parsed_record.summary,
        work_experience=[WorkExperienceEntry(**w) for w in parsed_record.work_experience],
        education=[EducationEntry(**e) for e in parsed_record.education],
        skills=SkillCategory(**parsed_record.skills),
        projects=[ProjectEntry(**p) for p in parsed_record.projects],
        certifications=[CertificationEntry(**c) for c in parsed_record.certifications],
    )

    return {
        "success": True,
        "data": {
            "resume_id": str(resume.id),
            "structured_profile": structured_profile.model_dump(),
        },
        "error": None,
    }
