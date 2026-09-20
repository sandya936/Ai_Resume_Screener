import uuid
import time
from typing import Dict, Any, Tuple
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.schemas.agent_trace import AgentStepTrace
from app.agents.tools.registry import SandboxedAgentTools


class SkillGapAgent:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def execute(
        self, job_id: uuid.UUID, resume_id: uuid.UUID
    ) -> Tuple[Dict[str, Any], AgentStepTrace]:
        start_time = time.time()
        trace = AgentStepTrace(
            agent_name="SkillGapAgent",
            status="running",
            input_payload={"job_id": str(job_id), "resume_id": str(resume_id)},
            tool_calls=["tool_evaluate_match"],
        )

        try:
            match_data = await SandboxedAgentTools.tool_evaluate_match(self.db, job_id, resume_id)
            duration_ms = int((time.time() - start_time) * 1000)

            trace.status = "completed"
            trace.output_payload = match_data
            trace.execution_time_ms = duration_ms

            return match_data, trace

        except Exception as e:
            duration_ms = int((time.time() - start_time) * 1000)
            trace.status = "failed"
            trace.error_message = str(e)
            trace.execution_time_ms = duration_ms
            raise e
