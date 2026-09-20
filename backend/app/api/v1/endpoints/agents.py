import uuid
from typing import Any, Dict
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.api.deps import get_db, get_current_active_user, verify_resource_owner
from app.db.models.user import User
from app.db.models.resume import Resume
from app.domain.schemas.agent_trace import (
    OrchestrationRequest,
    OrchestrationResponse,
    AgentExecutionSession,
)
from app.agents.orchestrator import ManagerOrchestratorAgent

router = APIRouter()

# In-memory session trace store for high-speed observable trace retrieval
TRACE_STORE: Dict[str, AgentExecutionSession] = {}


@router.post("/orchestrate")
async def orchestrate_multi_agent_workflow(
    payload: OrchestrationRequest,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
) -> Any:
    # 1. Verify Resume Ownership
    result_res = await db.execute(select(Resume).where(Resume.id == payload.resume_id))
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

    # 2. Execute ManagerOrchestratorAgent
    orchestrator = ManagerOrchestratorAgent(db)
    response = await orchestrator.orchestrate(
        user_id=current_user.id,
        resume_id=payload.resume_id,
        job_id=payload.job_id,
        raw_jd_text=payload.raw_jd_text,
        user_goal=payload.user_goal,
    )

    # Store trace for retrieval
    TRACE_STORE[response.session_id] = response.execution_trace

    return {
        "success": True,
        "data": response.model_dump(),
        "error": None,
    }


@router.get("/trace/{session_id}")
async def get_agent_execution_trace(
    session_id: str,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    if session_id not in TRACE_STORE:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "success": False,
                "data": None,
                "error": {
                    "code": "TRACE_NOT_FOUND",
                    "message": f"Execution session '{session_id}' not found.",
                    "details": [],
                },
            },
        )

    session_trace = TRACE_STORE[session_id]
    return {
        "success": True,
        "data": {
            "session_id": session_id,
            "execution_trace": session_trace.model_dump(),
        },
        "error": None,
    }
