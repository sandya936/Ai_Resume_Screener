import re
import uuid
from typing import Optional, List, Set, Dict, Any
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.models.job_description import JobDescription
from app.db.models.job_match import JobMatch
from app.db.models.parsed_resume import ParsedResume
from app.db.models.resume_version import ResumeVersion
from app.domain.schemas.structured_resume import (
    StructuredResume,
    PersonalInfo,
    SkillCategory,
    EducationEntry,
    WorkExperienceEntry,
    ProjectEntry,
    CertificationEntry,
)
from app.domain.schemas.job_description import ParsedJobDescription
from app.domain.schemas.job_match import JobMatchResult
from app.domain.schemas.ats_analysis import ScoringReason
from app.services.job_matching.jd_parser import SkillNormalizer, JobDescriptionParserService, KNOWN_TECH_KEYWORDS


class JobMatcherService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def match_job_and_resume(
        self, job_id: uuid.UUID, resume_id: uuid.UUID
    ) -> JobMatchResult:
        # 1. Fetch Job Description record
        result_jd = await self.db.execute(
            select(JobDescription).where(JobDescription.id == job_id)
        )
        jd_record = result_jd.scalar_one_or_none()

        if not jd_record:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={
                    "success": False,
                    "data": None,
                    "error": {
                        "code": "JOB_NOT_FOUND",
                        "message": "Job Description not found",
                        "details": [],
                    },
                },
            )

        # Parse JD structure
        if jd_record.required_skills and isinstance(jd_record.required_skills, dict) and "required_skills" in jd_record.required_skills:
            parsed_jd = ParsedJobDescription(**jd_record.required_skills)
        else:
            parsed_jd = JobDescriptionParserService.parse_text(
                jd_record.title, jd_record.company_name or "", jd_record.raw_text
            )

        # 2. Fetch Parsed Resume record
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

        # 3. Comprehensive Candidate Resume Skill Extraction across all sections & raw text
        raw_candidate_skills = (
            structured_resume.skills.technical_skills
            + structured_resume.skills.tools_and_frameworks
            + structured_resume.skills.soft_skills
        )
        if parsed_record.raw_text:
            for kw in KNOWN_TECH_KEYWORDS:
                if re.search(r"\b" + re.escape(kw) + r"\b", parsed_record.raw_text, re.IGNORECASE):
                    raw_candidate_skills.append(kw)

        for exp in structured_resume.work_experience:
            if exp.technologies:
                raw_candidate_skills.extend(exp.technologies)
        for proj in structured_resume.projects:
            if proj.technologies:
                raw_candidate_skills.extend(proj.technologies)

        candidate_skills_norm: Set[str] = set(
            SkillNormalizer.normalize_list(raw_candidate_skills)
        )

        # Normalize JD Skills
        jd_required_norm: Set[str] = set(
            SkillNormalizer.normalize_list(parsed_jd.required_skills)
        )
        jd_preferred_norm: Set[str] = set(
            SkillNormalizer.normalize_list(parsed_jd.preferred_skills)
        )

        # 4. Perform Matching Intersections
        matched_required = jd_required_norm.intersection(candidate_skills_norm)
        missing_required = jd_required_norm - candidate_skills_norm
        matched_preferred = jd_preferred_norm.intersection(candidate_skills_norm)
        weak_preferred = jd_preferred_norm - candidate_skills_norm

        matched_skills_list = list(matched_required.union(matched_preferred))
        missing_skills_list = list(missing_required)
        weak_skills_list = list(weak_preferred)

        # Calculate Scores
        req_score = int((len(matched_required) / max(1, len(jd_required_norm))) * 100)
        pref_score = int((len(matched_preferred) / max(1, len(jd_preferred_norm))) * 100) if jd_preferred_norm else 100

        # Dynamic Experience Match Score
        has_work = len(structured_resume.work_experience) > 0
        if has_work:
            work_text = " ".join([exp.description + " " + " ".join(exp.accomplishments) for exp in structured_resume.work_experience]).lower()
            work_matched = [sk for sk in jd_required_norm if sk in work_text or re.search(r"\b" + re.escape(sk) + r"\b", work_text)]
            exp_relevance_ratio = len(work_matched) / max(1, len(jd_required_norm))
            exp_score = int(75 + (exp_relevance_ratio * 25))
        else:
            exp_score = 40

        # Dynamic Project Relevance Score
        has_proj = len(structured_resume.projects) > 0
        if has_proj:
            proj_text = " ".join([p.title + " " + p.description + " " + " ".join(p.technologies) for p in structured_resume.projects]).lower()
            proj_matched = [sk for sk in jd_required_norm if sk in proj_text or re.search(r"\b" + re.escape(sk) + r"\b", proj_text)]
            proj_relevance_ratio = len(proj_matched) / max(1, len(jd_required_norm))
            proj_score = int(70 + (proj_relevance_ratio * 30))
        else:
            proj_score = 50

        # Education Match Score
        has_edu = len(structured_resume.education) > 0
        edu_score = 90 if has_edu else 50

        # Overall Formula Calculation (Weighted Real-world ATS Match Formula)
        overall_match_score = int(
            (req_score * 0.45)
            + (pref_score * 0.15)
            + (exp_score * 0.20)
            + (proj_score * 0.10)
            + (edu_score * 0.10)
        )
        overall_match_score = max(0, min(100, overall_match_score))

        # 5. Formulate Reasons & Recommendations
        reasons: List[ScoringReason] = []
        if matched_required:
            reasons.append(
                ScoringReason(
                    type="positive",
                    message=f"Matched core required skills: {', '.join(list(matched_required)[:4]).title()}.",
                    category="Required Skills",
                )
            )
        if missing_required:
            reasons.append(
                ScoringReason(
                    type="negative",
                    message=f"Missing mandatory required skills: {', '.join(list(missing_required)[:4]).title()}.",
                    category="Required Skills",
                )
            )

        recommendations: List[str] = []
        for sk in missing_skills_list[:3]:
            recommendations.append(
                f"Acquire or explicitly list proficiency in '{sk.title()}' to fulfill key JD requirements."
            )
        if not recommendations:
            recommendations.append("Candidate technical stack aligns closely with position requirements.")

        formula_explanation = (
            "Overall Match Score (0-100) is calculated using a weighted formula: Required Skills Match (40%), "
            "Preferred Skills Match (15%), Work Experience (25%), Project Relevance (10%), and Education (10%). "
            "Skill synonyms are normalized into canonical keys before evaluation."
        )

        match_result = JobMatchResult(
            overall_match_score=overall_match_score,
            required_skills_match_score=req_score,
            preferred_skills_match_score=pref_score,
            experience_match_score=exp_score,
            education_match_score=edu_score,
            project_relevance_score=proj_score,
            matched_skills=matched_skills_list,
            missing_skills=missing_skills_list,
            weak_skills=weak_skills_list,
            keyword_gaps=missing_skills_list,
            reasons=reasons,
            actionable_gap_recommendations=recommendations,
            matching_formula_explanation=formula_explanation,
        )

        # 6. Store in job_matches table
        result_ver = await self.db.execute(
            select(ResumeVersion)
            .where(ResumeVersion.resume_id == resume_id)
            .order_by(ResumeVersion.created_at.desc())
        )
        latest_ver = result_ver.scalars().first()

        if latest_ver:
            result_existing_match = await self.db.execute(
                select(JobMatch).where(
                    JobMatch.resume_version_id == latest_ver.id,
                    JobMatch.job_description_id == job_id,
                )
            )
            existing_match = result_existing_match.scalar_one_or_none()

            if existing_match:
                existing_match.match_score = overall_match_score
                existing_match.matching_skills = matched_skills_list
                existing_match.missing_skills = missing_skills_list
            else:
                new_match = JobMatch(
                    resume_version_id=latest_ver.id,
                    job_description_id=job_id,
                    match_score=overall_match_score,
                    matching_skills=matched_skills_list,
                    missing_skills=missing_skills_list,
                )
                self.db.add(new_match)

        await self.db.commit()
        return match_result
