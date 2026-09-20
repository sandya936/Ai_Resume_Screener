import uuid
from typing import Optional
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.db.models.resume_version import ResumeVersion
from app.db.models.parsed_resume import ParsedResume
from app.domain.schemas.structured_resume import StructuredResume
from app.providers.llm.factory import LLMProviderFactory


class ResumeParserService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def parse_version(
        self, version_id: uuid.UUID, provider_name: Optional[str] = None
    ) -> StructuredResume:
        # 1. Fetch version and existing document extraction analysis
        result = await self.db.execute(
            select(ResumeVersion)
            .options(selectinload(ResumeVersion.analyses), selectinload(ResumeVersion.resume))
            .where(ResumeVersion.id == version_id)
        )
        version = result.scalar_one_or_none()

        if not version:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={
                    "success": False,
                    "data": None,
                    "error": {
                        "code": "VERSION_NOT_FOUND",
                        "message": "Resume version not found",
                        "details": [],
                    },
                },
            )

        # Retrieve extracted raw text
        extraction_analysis = next(
            (a for a in version.analyses if a.analysis_type == "document_extraction"), None
        )
        raw_text = ""
        if extraction_analysis and extraction_analysis.payload:
            raw_text = extraction_analysis.payload.get("raw_text", "")

        if not raw_text.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "success": False,
                    "data": None,
                    "error": {
                        "code": "EMPTY_EXTRACTED_TEXT",
                        "message": "Resume version contains no extracted text to parse.",
                        "details": [],
                    },
                },
            )

        # 2. Invoke LLM provider
        provider = LLMProviderFactory.get_provider(provider_name)
        structured_resume: StructuredResume = await provider.parse_resume_text(raw_text)

        # 3. Store or update ParsedResume in Database
        result_parsed = await self.db.execute(
            select(ParsedResume).where(ParsedResume.resume_id == version.resume_id)
        )
        parsed_record = result_parsed.scalar_one_or_none()

        contact_dict = structured_resume.personal_info.model_dump()
        work_exp_list = [w.model_dump() for w in structured_resume.work_experience]
        edu_list = [e.model_dump() for e in structured_resume.education]
        skills_dict = structured_resume.skills.model_dump()
        projects_list = [p.model_dump() for p in structured_resume.projects]
        certs_list = [c.model_dump() for c in structured_resume.certifications]

        if parsed_record:
            parsed_record.raw_text = raw_text
            parsed_record.contact_info = contact_dict
            parsed_record.summary = structured_resume.summary or ""
            parsed_record.work_experience = work_exp_list
            parsed_record.education = edu_list
            parsed_record.skills = skills_dict
            parsed_record.projects = projects_list
            parsed_record.certifications = certs_list
        else:
            parsed_record = ParsedResume(
                resume_id=version.resume_id,
                raw_text=raw_text,
                contact_info=contact_dict,
                summary=structured_resume.summary or "",
                work_experience=work_exp_list,
                education=edu_list,
                skills=skills_dict,
                projects=projects_list,
                certifications=certs_list,
                ats_score=None,
                ats_feedback=None,
            )
            self.db.add(parsed_record)

        await self.db.commit()
        return structured_resume
