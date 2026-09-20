import uuid
import time
from typing import Dict, Any, Tuple
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.schemas.agent_trace import AgentStepTrace
from app.agents.tools.registry import SandboxedAgentTools


class ResumeAgent:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def execute(self, resume_id: uuid.UUID) -> Tuple[Dict[str, Any], AgentStepTrace]:
        start_time = time.time()
        trace = AgentStepTrace(
            agent_name="ResumeAgent",
            status="running",
            input_payload={"resume_id": str(resume_id)},
            tool_calls=["tool_fetch_resume"],
        )

        try:
            structured_profile = await SandboxedAgentTools.tool_fetch_resume(self.db, resume_id)
            duration_ms = int((time.time() - start_time) * 1000)

            trace.status = "completed"
            trace.output_payload = structured_profile
            trace.execution_time_ms = duration_ms

            return structured_profile, trace

        except Exception as e:
            duration_ms = int((time.time() - start_time) * 1000)
            trace.status = "failed"
            trace.error_message = str(e)
            trace.execution_time_ms = duration_ms
            raise e
