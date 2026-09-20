import uuid
import time
from typing import Dict, Any, Tuple, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.models.job_description import JobDescription
from app.domain.schemas.agent_trace import AgentStepTrace
from app.domain.schemas.job_description import ParsedJobDescription
from app.agents.tools.registry import SandboxedAgentTools


class JobDescriptionAgent:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def execute(
        self, user_id: uuid.UUID, job_id: Optional[uuid.UUID] = None, raw_jd_text: Optional[str] = None
    ) -> Tuple[Dict[str, Any], uuid.UUID, AgentStepTrace]:
        start_time = time.time()
        trace = AgentStepTrace(
            agent_name="JobDescriptionAgent",
            status="running",
            input_payload={"job_id": str(job_id) if job_id else None, "has_raw_text": bool(raw_jd_text)},
            tool_calls=["tool_parse_job"],
        )

        try:
            if job_id:
                result_jd = await self.db.execute(select(JobDescription).where(JobDescription.id == job_id))
                job_record = result_jd.scalar_one_or_none()
                if not job_record:
                    raise ValueError(f"Job ID {job_id} not found.")
                target_job_id = job_record.id
                parsed_jd_data = job_record.required_skills
            else:
                text = raw_jd_text or "Senior Backend Software Engineer with Python, FastAPI, Docker, Kubernetes."
                res = await SandboxedAgentTools.tool_parse_job(self.db, user_id, "Target Software Engineer Position", text)
                target_job_id = uuid.UUID(res["job_id"])
                parsed_jd_data = res["parsed_jd"]

            duration_ms = int((time.time() - start_time) * 1000)
            trace.status = "completed"
            trace.output_payload = parsed_jd_data
            trace.execution_time_ms = duration_ms

            return parsed_jd_data, target_job_id, trace

        except Exception as e:
            duration_ms = int((time.time() - start_time) * 1000)
            trace.status = "failed"
            trace.error_message = str(e)
            trace.execution_time_ms = duration_ms
            raise e
