import uuid
from typing import Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.services.resume_parser import ResumeParserService
from app.services.job_matching import JobDescriptionParserService, JobMatcherService
from app.services.ats_analyzer import ATSAnalyzerService
from app.services.career_intelligence import CareerIntelligenceService, InterviewIntelligenceService
from app.domain.schemas.job_description import JobDescriptionCreate
from app.db.models.job_description import JobDescription
from app.db.models.resume import Resume
from app.db.models.resume_version import ResumeVersion


class SandboxedAgentTools:
    @staticmethod
    async def tool_fetch_resume(db: AsyncSession, resume_id: uuid.UUID) -> Dict[str, Any]:
        """Tool: Retrieves candidate resume and ensures structured profile is parsed."""
        result_res = await db.execute(
            select(Resume).options(selectinload(Resume.versions)).where(Resume.id == resume_id)
        )
        resume = result_res.scalar_one_or_none()

        if not resume:
            raise ValueError(f"Resume ID {resume_id} not found.")

        parser_service = ResumeParserService(db)
        latest_version_id = resume.versions[-1].id if resume.versions else None
        if not latest_version_id:
            raise ValueError("Resume has no version revisions.")

        structured = await parser_service.parse_version(latest_version_id, provider_name="mock")
        return structured.model_dump()

    @staticmethod
    async def tool_parse_job(
        db: AsyncSession, user_id: uuid.UUID, title: str, raw_text: str
    ) -> Dict[str, Any]:
        """Tool: Parses and saves a Job Description posting."""
        parsed_jd = JobDescriptionParserService.parse_text(title, "Target Company", raw_text)

        job_record = JobDescription(
            user_id=user_id,
            title=title,
            company_name="Target Company",
            raw_text=raw_text,
            required_skills=parsed_jd.model_dump(),
        )
        db.add(job_record)
        await db.commit()
        await db.refresh(job_record)

        return {"job_id": str(job_record.id), "parsed_jd": parsed_jd.model_dump()}

    @staticmethod
    async def tool_evaluate_match(
        db: AsyncSession, job_id: uuid.UUID, resume_id: uuid.UUID
    ) -> Dict[str, Any]:
        """Tool: Computes explainable job-resume match score."""
        matcher = JobMatcherService(db)
        match_result = await matcher.match_job_and_resume(job_id, resume_id)
        return match_result.model_dump()

    @staticmethod
    async def tool_evaluate_ats_score(db: AsyncSession, resume_id: uuid.UUID) -> Dict[str, Any]:
        """Tool: Computes ATS Compatibility Estimate score."""
        analyzer = ATSAnalyzerService(db)
        ats_result = await analyzer.analyze_resume(resume_id)
        return ats_result.model_dump()

    @staticmethod
    async def tool_generate_roadmap(db: AsyncSession, resume_id: uuid.UUID) -> Dict[str, Any]:
        """Tool: Generates skill gap analysis and 30-day learning curriculum."""
        career_service = CareerIntelligenceService(db)
        insights = await career_service.generate_career_insights(resume_id)
        return insights.model_dump()

    @staticmethod
    async def tool_generate_interview_questions(
        db: AsyncSession, resume_id: uuid.UUID
    ) -> Dict[str, Any]:
        """Tool: Generates 5-category interview question bank with STAR points."""
        interview_service = InterviewIntelligenceService(db)
        questions = await interview_service.generate_question_bank(resume_id)
        return {"questions": [q.model_dump() for q in questions]}
