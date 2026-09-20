import uuid
from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.api.deps import get_db, get_current_active_user, verify_resource_owner
from app.db.models.user import User
from app.db.models.resume import Resume
from app.domain.schemas.interview_intelligence import (
    InterviewQuestion,
    AnswerEvaluationRequest,
    AnswerEvaluationResponse,
)
from app.services.career_intelligence import InterviewIntelligenceService

router = APIRouter()


@router.post("/questions/{resume_id}")
async def generate_interview_questions(
    resume_id: uuid.UUID,
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

    # 2. Generate questions
    interview_service = InterviewIntelligenceService(db)
    questions = await interview_service.generate_question_bank(resume_id)

    return {
        "success": True,
        "data": {
            "resume_id": str(resume.id),
            "questions": [q.model_dump() for q in questions],
        },
        "error": None,
    }


@router.post("/evaluate")
async def evaluate_interview_answer(
    payload: AnswerEvaluationRequest,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    evaluation = InterviewIntelligenceService.evaluate_answer(payload)
    return {
        "success": True,
        "data": {
            "evaluation": evaluation.model_dump(),
        },
        "error": None,
    }
