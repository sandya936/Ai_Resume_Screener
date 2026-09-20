import uuid
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, ConfigDict


class JobDescriptionCreate(BaseModel):
    title: str = Field(..., min_length=2, max_length=255, description="Job posting title")
    company_name: Optional[str] = Field(None, max_length=255, description="Company name")
    raw_text: str = Field(..., min_length=20, description="Full job description text")


class ParsedJobDescription(BaseModel):
    title: str = Field(..., description="Job title")
    company_name: Optional[str] = Field(None, description="Company name")
    required_skills: List[str] = Field(default_factory=list, description="Must-have required technical and soft skills")
    preferred_skills: List[str] = Field(default_factory=list, description="Nice-to-have preferred skills")
    technologies: List[str] = Field(default_factory=list, description="Tools, frameworks, and technologies")
    responsibilities: List[str] = Field(default_factory=list, description="Core responsibilities and duties")
    experience_requirements: Optional[str] = Field(None, description="Years or depth of experience required")
    education_requirements: Optional[str] = Field(None, description="Degree or academic requirements")
    domain_knowledge: List[str] = Field(default_factory=list, description="Domain specific knowledge (e.g., FinTech, SaaS)")
    keywords: List[str] = Field(default_factory=list, description="Key search phrases and terms")

    model_config = ConfigDict(from_attributes=True)


class JobDescriptionResponse(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    title: str
    company_name: Optional[str]
    raw_text: str
    parsed_jd: Optional[ParsedJobDescription] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
