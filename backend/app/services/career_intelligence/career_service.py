import uuid
from typing import Optional, List
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.models.parsed_resume import ParsedResume
from app.domain.schemas.structured_resume import (
    StructuredResume,
    PersonalInfo,
    SkillCategory,
    EducationEntry,
    WorkExperienceEntry,
    ProjectEntry,
    CertificationEntry,
)
from app.domain.schemas.career_intelligence import (
    CareerInsightsResult,
    SkillGapItem,
    SpecificRecommendation,
    RoadmapMilestone,
    LearningRoadmap,
)


class CareerIntelligenceService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def generate_career_insights(
        self, resume_id: uuid.UUID, target_job_title: Optional[str] = None
    ) -> CareerInsightsResult:
        # 1. Fetch ParsedResume record
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

        structured_resume = StructuredResume(
            personal_info=PersonalInfo(**parsed_record.contact_info),
            summary=parsed_record.summary,
            work_experience=[WorkExperienceEntry(**w) for w in parsed_record.work_experience],
            education=[EducationEntry(**e) for e in parsed_record.education],
            skills=SkillCategory(**parsed_record.skills),
            projects=[ProjectEntry(**p) for p in parsed_record.projects],
            certifications=[CertificationEntry(**c) for c in parsed_record.certifications],
        )

        candidate_skills = set(
            s.lower()
            for s in structured_resume.skills.technical_skills
            + structured_resume.skills.tools_and_frameworks
        )

        # 2. Dynamic Skill Gap Engine
        # Query latest JobDescription for the user if available
        target_role_str = (target_job_title or "").strip()
        job_required_skills: List[str] = []

        from app.db.models.job_description import JobDescription
        result_jd = await self.db.execute(
            select(JobDescription)
            .where(JobDescription.user_id == parsed_record.resume.user_id)
            .order_by(JobDescription.created_at.desc())
        )
        latest_jd = result_jd.scalars().first()

        if latest_jd and latest_jd.required_skills:
            parsed_skills = latest_jd.required_skills.get("required_skills", [])
            job_required_skills = [s.lower() for s in parsed_skills]
            if not target_role_str:
                target_role_str = latest_jd.title

        if not job_required_skills:
            if any(k in target_role_str.lower() for k in ["analyst", "data", "tableau", "power bi", "excel"]):
                job_required_skills = ["sql", "python", "pandas", "tableau", "power bi", "excel", "data visualization"]
            elif any(k in target_role_str.lower() for k in ["frontend", "react", "ui"]):
                job_required_skills = ["javascript", "typescript", "react", "next.js", "css", "html"]
            else:
                job_required_skills = ["python", "fastapi", "postgresql", "docker", "git", "rest api"]

        # Identify missing skills dynamically
        missing_skills = [sk for sk in job_required_skills if sk not in candidate_skills]

        skill_gaps: List[SkillGapItem] = []
        for sk in missing_skills[:4]:
            skill_title = sk.title()
            if sk in ["power bi", "tableau", "data visualization"]:
                skill_title = f"{sk.title()} & Interactive Dashboarding"
                effort = "1-2 weeks"
                reason = f"Essential for presenting data findings to technical and business stakeholders as a {target_role_str or 'Data Analyst'}."
            elif sk in ["pandas", "numpy"]:
                skill_title = f"{sk.title()} Data Manipulation & Transformation"
                effort = "1 week"
                reason = "Core requirement for structured dataset cleaning and analysis."
            elif sk in ["sql", "postgresql", "vlookup", "excel"]:
                skill_title = f"{sk.title()} Data Querying & Analytical Formulas"
                effort = "1 week"
                reason = "Primary tool for extracting business metrics and raw database records."
            else:
                skill_title = f"{sk.title()} Proficiency"
                effort = "1-2 weeks"
                reason = f"Required skill explicitly requested for {target_role_str or 'target role'}."

            skill_gaps.append(
                SkillGapItem(
                    skill_name=skill_title,
                    priority="critical" if len(skill_gaps) < 2 else "medium",
                    jd_importance="High" if len(skill_gaps) < 2 else "Medium",
                    learning_effort=effort,
                    reason=reason,
                )
            )

        if not skill_gaps:
            skill_gaps.append(
                SkillGapItem(
                    skill_name="Advanced Domain Intelligence & Executive Reporting",
                    priority="low",
                    jd_importance="Low",
                    learning_effort="2 weeks",
                    reason=f"Candidate possesses all core technical skills for {target_role_str or 'target role'}.",
                )
            )

        # 3. Specific Recommendation Engine
        recommendations: List[SpecificRecommendation] = []
        has_metrics = False
        for exp in structured_resume.work_experience:
            for acc in exp.accomplishments:
                if any(c in acc for c in ["%", "$", "x", "ms"]):
                    has_metrics = True
                    break

        if not has_metrics and len(structured_resume.work_experience) > 0:
            first_company = structured_resume.work_experience[0].company
            recommendations.append(
                SpecificRecommendation(
                    target_area="resume",
                    action_title="Quantify Project & Experience Outcomes",
                    detailed_guidance=(
                        f"Add measurable impact to your {first_company} work experience bullet points, "
                        "such as query latency reduction %, dataset size processed, active dashboard users, or metric accuracy improvements."
                    ),
                )
            )
        else:
            recommendations.append(
                SpecificRecommendation(
                    target_area="resume",
                    action_title="Highlight Action-Oriented Key Accomplishments",
                    detailed_guidance="Lead each bullet point with strong impact verbs (e.g. Visualized, Analyzed, Optimized, Engineered).",
                )
            )

        recommendations.append(
            SpecificRecommendation(
                target_area="project",
                action_title=f"Build a {target_role_str or 'Target Role'} Portfolio Case Study",
                detailed_guidance=(
                    f"Construct a hands-on portfolio case study demonstrating end-to-end data processing, "
                    f"interactive dashboarding, and actionable business insights tailored for {target_role_str or 'target role'}."
                ),
            )
        )

        # 4. Dynamic Learning Roadmap Engine (30-Day)
        gap_1 = skill_gaps[0].skill_name if len(skill_gaps) > 0 else "Core Skill Mastery"
        gap_2 = skill_gaps[1].skill_name if len(skill_gaps) > 1 else "Tooling & Integration"

        thirty_day_plan = [
            RoadmapMilestone(
                timeframe="week_1",
                title=f"Week 1: Core Fundamentals & {gap_1}",
                focus_skills=[gap_1.split()[0]],
                action_items=[
                    f"Master foundational concepts and hands-on exercises in {gap_1}.",
                    "Build initial script/dashboard verifying core functionality.",
                ],
                estimated_hours=10,
            ),
            RoadmapMilestone(
                timeframe="week_2",
                title=f"Week 2: Advanced Tooling & {gap_2}",
                focus_skills=[gap_2.split()[0]],
                action_items=[
                    f"Implement practical workflows using {gap_2}.",
                    "Integrate automated data pipelines or UI dashboards.",
                ],
                estimated_hours=12,
            ),
            RoadmapMilestone(
                timeframe="week_3",
                title=f"Week 3: {target_role_str or 'Target Role'} Case Study Development",
                focus_skills=["Case Study", "Domain Project"],
                action_items=[
                    "Design end-to-end portfolio project featuring clean code & documentation.",
                    "Publish repository with interactive demo preview or clear results breakdown.",
                ],
                estimated_hours=14,
            ),
            RoadmapMilestone(
                timeframe="week_4",
                title="Week 4: Portfolio Verification & Interview Preparation",
                focus_skills=["STAR Method", "Interview Prep"],
                action_items=[
                    "Prepare STAR interview responses linking project accomplishments to target position.",
                    "Conduct practice mock interview evaluations.",
                ],
                estimated_hours=10,
            ),
        ]

        seven_day_plan = [
            RoadmapMilestone(
                timeframe="7_day",
                title=f"Immediate Skill Assessment in {gap_1.split()[0]}",
                focus_skills=[gap_1.split()[0]],
                action_items=[f"Complete hands-on tutorial for {gap_1.split()[0]}."],
                estimated_hours=6,
            )
        ]

        known_info = (
            f"Candidate: {structured_resume.personal_info.full_name or 'N/A'} | "
            f"Target Position: {target_role_str or 'N/A'} | "
            f"Technical Skills: {', '.join(structured_resume.skills.technical_skills[:5])}"
        )

        disclaimer = (
            "Anti-Fabrication Policy: All recommendations are derived from verified candidate resume content "
            "and target job description requirements. AGENTX will never suggest inventing fake experience, false metrics, "
            "or unearned credentials."
        )

        return CareerInsightsResult(
            skill_gaps=skill_gaps,
            specific_recommendations=recommendations,
            learning_roadmap=LearningRoadmap(
                seven_day_plan=seven_day_plan, thirty_day_plan=thirty_day_plan
            ),
            known_info_summary=known_info,
            disclaimer=disclaimer,
        )
