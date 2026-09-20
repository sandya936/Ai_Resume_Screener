import uuid
from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.api.deps import get_db, get_current_active_user, verify_resource_owner
from app.db.models.user import User
from app.db.models.job_description import JobDescription
from app.db.models.resume import Resume
from app.domain.schemas.job_description import (
    JobDescriptionCreate,
    JobDescriptionResponse,
    ParsedJobDescription,
)
from app.domain.schemas.job_match import JobMatchResult
from app.services.job_matching import JobDescriptionParserService, JobMatcherService

router = APIRouter()


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_job_description(
    payload: JobDescriptionCreate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
) -> Any:
    # 1. Parse Job Description
    parsed_jd = JobDescriptionParserService.parse_text(
        payload.title, payload.company_name or "", payload.raw_text
    )

    # 2. Save in Database
    job_record = JobDescription(
        user_id=current_user.id,
        title=payload.title,
        company_name=payload.company_name,
        raw_text=payload.raw_text,
        required_skills=parsed_jd.model_dump(),
    )
    db.add(job_record)
    await db.commit()
    await db.refresh(job_record)

    return {
        "success": True,
        "data": {
            "job": JobDescriptionResponse(
                id=job_record.id,
                user_id=job_record.user_id,
                title=job_record.title,
                company_name=job_record.company_name,
                raw_text=job_record.raw_text,
                parsed_jd=parsed_jd,
                created_at=job_record.created_at,
            ).model_dump()
        },
        "error": None,
    }


@router.get("/{job_id}")
async def get_job_description(
    job_id: uuid.UUID,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
) -> Any:
    result = await db.execute(select(JobDescription).where(JobDescription.id == job_id))
    job = result.scalar_one_or_none()

    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "success": False,
                "data": None,
                "error": {
                    "code": "JOB_NOT_FOUND",
                    "message": "Job Description not found",
                    "details": [],
                },
            },
        )
    verify_resource_owner(job.user_id, current_user.id)

    parsed_jd = ParsedJobDescription(**job.required_skills) if job.required_skills else None

    return {
        "success": True,
        "data": {
            "job": JobDescriptionResponse(
                id=job.id,
                user_id=job.user_id,
                title=job.title,
                company_name=job.company_name,
                raw_text=job.raw_text,
                parsed_jd=parsed_jd,
                created_at=job.created_at,
            ).model_dump()
        },
        "error": None,
    }


@router.post("/{job_id}/match/{resume_id}")
async def match_job_and_resume(
    job_id: uuid.UUID,
    resume_id: uuid.UUID,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
) -> Any:
    # 1. Verify Job Ownership
    result_jd = await db.execute(select(JobDescription).where(JobDescription.id == job_id))
    job = result_jd.scalar_one_or_none()
    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "success": False,
                "data": None,
                "error": {"code": "JOB_NOT_FOUND", "message": "Job Description not found", "details": []},
            },
        )
    verify_resource_owner(job.user_id, current_user.id)

    # 2. Verify Resume Ownership
    result_res = await db.execute(select(Resume).where(Resume.id == resume_id))
    resume = result_res.scalar_one_or_none()
    if not resume:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "success": False,
                "data": None,
                "error": {"code": "RESUME_NOT_FOUND", "message": "Resume not found", "details": []},
            },
        )
    verify_resource_owner(resume.user_id, current_user.id)

    # 3. Trigger JobMatcherService
    matcher = JobMatcherService(db)
    match_result = await matcher.match_job_and_resume(job_id, resume_id)

    return {
        "success": True,
        "data": {
            "job_id": str(job_id),
            "resume_id": str(resume_id),
            "match_result": match_result.model_dump(),
        },
        "error": None,
    }


@router.get("/{job_id}/match/{resume_id}")
async def get_job_match_result(
    job_id: uuid.UUID,
    resume_id: uuid.UUID,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
) -> Any:
    # 1. Verify Job Ownership
    result_jd = await db.execute(select(JobDescription).where(JobDescription.id == job_id))
    job = result_jd.scalar_one_or_none()
    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "success": False,
                "data": None,
                "error": {"code": "JOB_NOT_FOUND", "message": "Job Description not found", "details": []},
            },
        )
    verify_resource_owner(job.user_id, current_user.id)

    # 2. Trigger JobMatcherService to return stored/fresh match result
    matcher = JobMatcherService(db)
    match_result = await matcher.match_job_and_resume(job_id, resume_id)

    return {
        "success": True,
        "data": {
            "job_id": str(job_id),
            "resume_id": str(resume_id),
            "match_result": match_result.model_dump(),
        },
        "error": None,
    }
