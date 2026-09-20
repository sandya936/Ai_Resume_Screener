import uuid
from typing import Any, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.api.deps import get_db, get_current_active_user, verify_resource_owner
from app.db.models.user import User
from app.db.models.resume import Resume
from app.domain.schemas.career_intelligence import CareerInsightsResult
from app.services.career_intelligence import CareerIntelligenceService

router = APIRouter()


@router.post("/insights/{resume_id}")
async def generate_career_insights(
    resume_id: uuid.UUID,
    target_role: Optional[str] = Query(None),
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
) -> Any:
    # 1. Verify Resume Ownership
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

    # 2. Trigger CareerIntelligenceService
    career_service = CareerIntelligenceService(db)
    insights = await career_service.generate_career_insights(resume_id, target_job_title=target_role)

    return {
        "success": True,
        "data": {
            "resume_id": str(resume.id),
            "career_insights": insights.model_dump(),
        },
        "error": None,
    }
