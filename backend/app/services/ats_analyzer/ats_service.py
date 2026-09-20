import uuid
from typing import Optional
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.models.resume import Resume
from app.db.models.resume_version import ResumeVersion
from app.db.models.parsed_resume import ParsedResume
from app.db.models.analysis import Analysis
from app.domain.schemas.structured_resume import (
    StructuredResume,
    PersonalInfo,
    SkillCategory,
    EducationEntry,
    WorkExperienceEntry,
    ProjectEntry,
    CertificationEntry,
)
from app.domain.schemas.ats_analysis import (
    ATSAnalysisResult,
    CategoryScore,
    ScoringReason,
)
from app.services.ats_analyzer.deterministic_rules import DeterministicRulesEngine
from app.services.ats_analyzer.ai_auditor import AIAuditorService


class ATSAnalyzerService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def analyze_resume(self, resume_id: uuid.UUID) -> ATSAnalysisResult:
        # 1. Fetch resume and parsed resume entity
        result_parsed = await self.db.execute(
            select(ParsedResume).where(ParsedResume.resume_id == resume_id)
        )
        parsed_record = result_parsed.scalar_one_or_none()

        if not parsed_record:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={
                    "success": False,
                    "data": None,
                    "error": {
                        "code": "PARSED_RESUME_NOT_FOUND",
                        "message": "Resume has not been parsed yet. Run POST /resumes/{id}/parse first.",
                        "details": [],
                    },
                },
            )

        # Reconstruct StructuredResume Pydantic model
        structured_resume = StructuredResume(
            personal_info=PersonalInfo(**parsed_record.contact_info),
            summary=parsed_record.summary,
            work_experience=[WorkExperienceEntry(**w) for w in parsed_record.work_experience],
            education=[EducationEntry(**e) for e in parsed_record.education],
            skills=SkillCategory(**parsed_record.skills),
            projects=[ProjectEntry(**p) for p in parsed_record.projects],
            certifications=[CertificationEntry(**c) for c in parsed_record.certifications],
        )

        raw_text = parsed_record.raw_text

        # 2. Run Deterministic Engine
        det_res = DeterministicRulesEngine.evaluate(structured_resume, raw_text)

        # 3. Category Scores Setup
        cat_scores = [
            CategoryScore(
                category_name="ATS Compatibility",
                score=det_res["ats_compatibility_score"],
                weight=0.25,
                description="Estimates structural compatibility with standard Applicant Tracking Systems.",
            ),
            CategoryScore(
                category_name="Content Quality",
                score=det_res["content_quality_score"],
                weight=0.20,
                description="Evaluates action verb usage, clarity, and readability.",
            ),
            CategoryScore(
                category_name="Skills",
                score=det_res["skills_score"],
                weight=0.15,
                description="Evaluates diversity and categorization of technical and soft skills.",
            ),
            CategoryScore(
                category_name="Experience",
                score=det_res["experience_score"],
                weight=0.15,
                description="Evaluates quantified metrics, bullet achievements, and career depth.",
            ),
            CategoryScore(
                category_name="Projects",
                score=det_res["projects_score"],
                weight=0.10,
                description="Evaluates project descriptions, technologies, and URLs.",
            ),
            CategoryScore(
                category_name="Education",
                score=det_res["education_score"],
                weight=0.05,
                description="Evaluates degree, institution, and major completeness.",
            ),
            CategoryScore(
                category_name="Completeness",
                score=det_res["completeness_score"],
                weight=0.10,
                description="Evaluates presence of standard required resume sections.",
            ),
        ]

        # Calculate Weighted Overall Score
        overall_score = int(sum(c.score * c.weight for c in cat_scores))
        overall_score = max(0, min(100, overall_score))

        # 4. Generate Actionable Improvements
        actionable_improvements = AIAuditorService.generate_recommendations(
            structured_resume, det_res
        )

        formula_explanation = (
            "Overall Score (0-100) is calculated as a weighted average across 7 categories: "
            "ATS Compatibility (25%), Content Quality (20%), Skills (15%), Experience (15%), "
            "Projects (10%), Education (5%), and Completeness (10%). Scores are derived using "
            "deterministic rule verification combined with qualitative reasoning."
        )

        analysis_result = ATSAnalysisResult(
            overall_score=overall_score,
            ats_compatibility_score=det_res["ats_compatibility_score"],
            category_scores=cat_scores,
            reasons=det_res["reasons"],
            strengths=det_res["strengths"],
            weaknesses=det_res["weaknesses"],
            warnings=det_res["warnings"],
            actionable_improvements=actionable_improvements,
            scoring_formula_explanation=formula_explanation,
        )

        # 5. Persist ATS Score in parsed_resumes and Analysis record
        parsed_record.ats_score = det_res["ats_compatibility_score"]
        parsed_record.ats_feedback = analysis_result.model_dump()

        # Find latest resume version
        result_ver = await self.db.execute(
            select(ResumeVersion)
            .where(ResumeVersion.resume_id == resume_id)
            .order_by(ResumeVersion.created_at.desc())
        )
        latest_ver = result_ver.scalars().first()

        if latest_ver:
            analysis_record = Analysis(
                resume_version_id=latest_ver.id,
                analysis_type="ats_score",
                status="completed",
                score=overall_score,
                payload=analysis_result.model_dump(),
            )
            self.db.add(analysis_record)

        await self.db.commit()
        return analysis_result
