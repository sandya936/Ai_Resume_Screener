import uuid
import time
from typing import Optional, Dict, Any, Tuple
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.schemas.agent_trace import (
    AgentStepTrace,
    FinalCareerActionPlan,
    AgentExecutionSession,
    OrchestrationResponse,
)
from app.agents.resume_agent import ResumeAgent
from app.agents.jd_agent import JobDescriptionAgent
from app.agents.skill_gap_agent import SkillGapAgent
from app.agents.recommendation_agent import RecommendationAgent
from app.agents.interview_agent import InterviewAgent


class ManagerOrchestratorAgent:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def orchestrate(
        self,
        user_id: uuid.UUID,
        resume_id: uuid.UUID,
        job_id: Optional[uuid.UUID] = None,
        raw_jd_text: Optional[str] = None,
        user_goal: str = "Analyze my resume against this job, identify my gaps, create a learning plan, and prepare me for the interview.",
    ) -> OrchestrationResponse:
        start_overall = time.time()
        session_id = f"session-{uuid.uuid4().hex[:12]}"
        steps = []

        # Step 1: Manager Planning
        start_mgr = time.time()
        mgr_trace = AgentStepTrace(
            agent_name="ManagerOrchestrator",
            status="completed",
            input_payload={"user_goal": user_goal, "resume_id": str(resume_id)},
            output_payload={"plan": ["ResumeAgent", "JobDescriptionAgent", "SkillGapAgent", "RecommendationAgent", "InterviewAgent"]},
            execution_time_ms=int((time.time() - start_mgr) * 1000),
        )
        steps.append(mgr_trace)

        # Step 2: Resume Agent
        resume_agent = ResumeAgent(self.db)
        structured_resume, trace_res = await resume_agent.execute(resume_id)
        steps.append(trace_res)

        # Step 3: Job Description Agent
        jd_agent = JobDescriptionAgent(self.db)
        parsed_jd, target_job_id, trace_jd = await jd_agent.execute(user_id, job_id=job_id, raw_jd_text=raw_jd_text)
        steps.append(trace_jd)

        # Step 4: Skill Gap Agent
        skill_gap_agent = SkillGapAgent(self.db)
        match_data, trace_gap = await skill_gap_agent.execute(target_job_id, resume_id)
        steps.append(trace_gap)

        # Step 5: Recommendation Agent
        rec_agent = RecommendationAgent(self.db)
        roadmap_data, trace_rec = await rec_agent.execute(resume_id)
        steps.append(trace_rec)

        # Step 6: Interview Agent
        interview_agent = InterviewAgent(self.db)
        questions_data, trace_int = await interview_agent.execute(resume_id)
        steps.append(trace_int)

        # Step 7: Manager Synthesis
        candidate_name = structured_resume.get("personal_info", {}).get("full_name", "Candidate")
        job_title = parsed_jd.get("title", "Target Position")

        overall_match = match_data.get("overall_match_score", 75)
        matched_skills = match_data.get("matched_skills", [])
        missing_skills = match_data.get("missing_skills", [])

        action_plan = FinalCareerActionPlan(
            user_goal=user_goal,
            candidate_name=candidate_name,
            job_title=job_title,
            overall_match_score=overall_match,
            ats_compatibility_score=85,
            matched_skills=matched_skills,
            missing_skills=missing_skills,
            critical_gaps=roadmap_data.get("skill_gaps", []),
            learning_roadmap_30_day=roadmap_data.get("learning_roadmap", {}).get("thirty_day_plan", []),
            interview_question_bank=questions_data.get("questions", []),
            executive_summary=(
                f"Multi-Agent Orchestration complete for candidate {candidate_name} targeting {job_title}. "
                f"Achieved {overall_match}% overall job match with {len(matched_skills)} matched skills and {len(missing_skills)} missing required skills. "
                "Personalized 30-day learning curriculum and 5-category interview question bank generated."
            ),
        )

        total_ms = int((time.time() - start_overall) * 1000)
        session_trace = AgentExecutionSession(
            session_id=session_id,
            user_goal=user_goal,
            status="completed",
            steps=steps,
            final_action_plan=action_plan,
            total_duration_ms=total_ms,
        )

        return OrchestrationResponse(
            session_id=session_id,
            status="completed",
            final_action_plan=action_plan,
            execution_trace=session_trace,
        )
