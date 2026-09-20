from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, EmailStr, ConfigDict


class PersonalInfo(BaseModel):
    full_name: Optional[str] = Field(None, description="Full candidate name")
    email: Optional[str] = Field(None, description="Email address")
    phone: Optional[str] = Field(None, description="Phone number")
    location: Optional[str] = Field(None, description="City, State, Country")
    linkedin_url: Optional[str] = Field(None, description="LinkedIn profile URL")
    github_url: Optional[str] = Field(None, description="GitHub profile URL")
    portfolio_url: Optional[str] = Field(None, description="Personal website or portfolio URL")
    summary: Optional[str] = Field(None, description="Professional summary or objective statement")


class EducationEntry(BaseModel):
    institution: str = Field(..., description="University or school name")
    degree: Optional[str] = Field(None, description="Degree earned (e.g. B.S., M.S.)")
    field_of_study: Optional[str] = Field(None, description="Major or field of study")
    start_date: Optional[str] = Field(None, description="Start date")
    end_date: Optional[str] = Field(None, description="End date or expected graduation")
    gpa: Optional[str] = Field(None, description="GPA score if specified")
    honors: List[str] = Field(default_factory=list, description="Honors or academic distinctions")


class WorkExperienceEntry(BaseModel):
    company: str = Field(..., description="Company or organization name")
    title: str = Field(..., description="Job title or role")
    location: Optional[str] = Field(None, description="Job location")
    start_date: Optional[str] = Field(None, description="Start date")
    end_date: Optional[str] = Field(None, description="End date")
    is_current: bool = Field(default=False, description="Whether this is the candidate's current position")
    description: Optional[str] = Field(None, description="Role summary description")
    accomplishments: List[str] = Field(default_factory=list, description="Bullet points of achievements/responsibilities")
    technologies: List[str] = Field(default_factory=list, description="Technologies/tools used in this position")


class SkillCategory(BaseModel):
    technical_skills: List[str] = Field(default_factory=list, description="Programming languages, frameworks, hard skills")
    soft_skills: List[str] = Field(default_factory=list, description="Communication, leadership, teamwork skills")
    languages: List[str] = Field(default_factory=list, description="Spoken languages")
    tools_and_frameworks: List[str] = Field(default_factory=list, description="Tools, cloud platforms, databases")


class ProjectEntry(BaseModel):
    title: str = Field(..., description="Project title")
    description: Optional[str] = Field(None, description="Project summary description")
    role: Optional[str] = Field(None, description="Candidate's role in the project")
    technologies: List[str] = Field(default_factory=list, description="Technologies used")
    url: Optional[str] = Field(None, description="Project demo or repository URL")
    start_date: Optional[str] = Field(None, description="Start date")
    end_date: Optional[str] = Field(None, description="End date")


class CertificationEntry(BaseModel):
    name: str = Field(..., description="Certification name")
    issuing_organization: Optional[str] = Field(None, description="Issuing body (e.g. AWS, Microsoft)")
    issue_date: Optional[str] = Field(None, description="Issue date")
    expiration_date: Optional[str] = Field(None, description="Expiration date")
    credential_id: Optional[str] = Field(None, description="Credential ID or number")
    url: Optional[str] = Field(None, description="Verification URL")


class AchievementEntry(BaseModel):
    title: str = Field(..., description="Achievement or award title")
    description: Optional[str] = Field(None, description="Description of achievement")
    date: Optional[str] = Field(None, description="Date awarded")


class PublicationEntry(BaseModel):
    title: str = Field(..., description="Publication title")
    publisher: Optional[str] = Field(None, description="Journal, conference, or publisher name")
    date: Optional[str] = Field(None, description="Publication date")
    url: Optional[str] = Field(None, description="Link to publication")


class LinkEntry(BaseModel):
    platform: str = Field(..., description="Platform name (e.g. Twitter, Medium, LeetCode)")
    url: str = Field(..., description="URL link")


class StructuredResume(BaseModel):
    personal_info: PersonalInfo = Field(default_factory=PersonalInfo)
    summary: Optional[str] = Field(None, description="Professional summary")
    education: List[EducationEntry] = Field(default_factory=list)
    work_experience: List[WorkExperienceEntry] = Field(default_factory=list)
    skills: SkillCategory = Field(default_factory=SkillCategory)
    projects: List[ProjectEntry] = Field(default_factory=list)
    certifications: List[CertificationEntry] = Field(default_factory=list)
    achievements: List[AchievementEntry] = Field(default_factory=list)
    publications: List[PublicationEntry] = Field(default_factory=list)
    links: List[LinkEntry] = Field(default_factory=list)

    model_config = ConfigDict(extra="allow", from_attributes=True)
