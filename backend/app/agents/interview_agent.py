import uuid
import time
from typing import Dict, Any, Tuple
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.schemas.agent_trace import AgentStepTrace
from app.agents.tools.registry import SandboxedAgentTools


class InterviewAgent:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def execute(self, resume_id: uuid.UUID) -> Tuple[Dict[str, Any], AgentStepTrace]:
        start_time = time.time()
        trace = AgentStepTrace(
            agent_name="InterviewAgent",
            status="running",
            input_payload={"resume_id": str(resume_id)},
            tool_calls=["tool_generate_interview_questions"],
        )

        try:
            questions_data = await SandboxedAgentTools.tool_generate_interview_questions(self.db, resume_id)
            duration_ms = int((time.time() - start_time) * 1000)

            trace.status = "completed"
            trace.output_payload = questions_data
            trace.execution_time_ms = duration_ms

            return questions_data, trace

        except Exception as e:
            duration_ms = int((time.time() - start_time) * 1000)
            trace.status = "failed"
            trace.error_message = str(e)
            trace.execution_time_ms = duration_ms
            raise e
