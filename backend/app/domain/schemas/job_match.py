from typing import List
from pydantic import BaseModel, Field, ConfigDict
from app.domain.schemas.ats_analysis import ScoringReason


class JobMatchResult(BaseModel):
    overall_match_score: int = Field(..., ge=0, le=100, description="Weighted overall job-resume match score")
    required_skills_match_score: int = Field(..., ge=0, le=100, description="Match percentage for mandatory required skills")
    preferred_skills_match_score: int = Field(..., ge=0, le=100, description="Match percentage for preferred skills")
    experience_match_score: int = Field(..., ge=0, le=100, description="Experience depth match score")
    education_match_score: int = Field(..., ge=0, le=100, description="Education requirement match score")
    project_relevance_score: int = Field(..., ge=0, le=100, description="Project relevance match score")
    
    matched_skills: List[str] = Field(default_factory=list, description="Skills present in both candidate resume and job posting (+)")
    missing_skills: List[str] = Field(default_factory=list, description="Mandatory skills required by JD but missing in resume (-)")
    weak_skills: List[str] = Field(default_factory=list, description="Preferred or partially matched skills (!)")
    keyword_gaps: List[str] = Field(default_factory=list, description="Important JD keywords absent in resume")
    
    reasons: List[ScoringReason] = Field(default_factory=list, description="Explicit explainable match reasons")
    actionable_gap_recommendations: List[str] = Field(default_factory=list, description="Recommendations to bridge candidate skill gaps")
    matching_formula_explanation: str = Field(..., description="Explanation of how match scores were computed")

    model_config = ConfigDict(from_attributes=True)
