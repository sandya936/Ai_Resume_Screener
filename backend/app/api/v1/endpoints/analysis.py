import uuid
from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.api.deps import get_db, get_current_active_user, verify_resource_owner
from app.db.models.user import User
from app.db.models.resume import Resume
from app.db.models.parsed_resume import ParsedResume
from app.domain.schemas.ats_analysis import ATSAnalysisResult
from app.services.ats_analyzer import ATSAnalyzerService

router = APIRouter()


@router.post("/ats/{resume_id}")
async def analyze_resume_ats(
    resume_id: uuid.UUID,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
) -> Any:
    # 1. Fetch resume & verify user ownership
    result = await db.execute(select(Resume).where(Resume.id == resume_id))
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

    # 2. Run ATS Analysis Service
    analyzer = ATSAnalyzerService(db)
    analysis_result = await analyzer.analyze_resume(resume_id)

    return {
        "success": True,
        "data": {
            "resume_id": str(resume.id),
            "ats_analysis": analysis_result.model_dump(),
        },
        "error": None,
    }


@router.get("/ats/{resume_id}")
async def get_resume_ats_analysis(
    resume_id: uuid.UUID,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
) -> Any:
    # 1. Fetch resume & verify user ownership
    result = await db.execute(select(Resume).where(Resume.id == resume_id))
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

    # 2. Fetch ParsedResume feedback payload
    result_parsed = await db.execute(
        select(ParsedResume).where(ParsedResume.resume_id == resume_id)
    )
    parsed_record = result_parsed.scalar_one_or_none()

    if not parsed_record or not parsed_record.ats_feedback:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "success": False,
                "data": None,
                "error": {
                    "code": "ANALYSIS_NOT_FOUND",
                    "message": "ATS analysis report not found. Call POST /analysis/ats/{id} first.",
                    "details": [],
                },
            },
        )

    analysis_result = ATSAnalysisResult(**parsed_record.ats_feedback)

    return {
        "success": True,
        "data": {
            "resume_id": str(resume.id),
            "ats_analysis": analysis_result.model_dump(),
        },
        "error": None,
    }
