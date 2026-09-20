from typing import List, Optional
from pydantic import BaseModel, Field, ConfigDict


class CategoryScore(BaseModel):
    category_name: str = Field(..., description="Name of category (e.g. ATS Compatibility, Content Quality)")
    score: int = Field(..., ge=0, le=100, description="Score from 0 to 100")
    weight: float = Field(..., ge=0.0, le=1.0, description="Weight factor in overall calculation")
    description: str = Field(..., description="Brief summary of category performance")


class ScoringReason(BaseModel):
    type: str = Field(..., description="Reason type: 'positive' (+), 'negative' (-), or 'warning' (!)")
    message: str = Field(..., description="Explanation message")
    category: str = Field(..., description="Associated category name")


class ATSAnalysisResult(BaseModel):
    overall_score: int = Field(..., ge=0, le=100, description="Weighted overall resume quality score")
    ats_compatibility_score: int = Field(..., ge=0, le=100, description="ATS Compatibility Estimate score")
    category_scores: List[CategoryScore] = Field(default_factory=list, description="Breakdown by category")
    reasons: List[ScoringReason] = Field(default_factory=list, description="Explicit reasons for scores")
    strengths: List[str] = Field(default_factory=list, description="Key resume strengths (+)")
    weaknesses: List[str] = Field(default_factory=list, description="Key resume weaknesses (-)")
    warnings: List[str] = Field(default_factory=list, description="Formatting or structural risk warnings (!)")
    actionable_improvements: List[str] = Field(default_factory=list, description="Prioritized recommendations for candidate")
    scoring_formula_explanation: str = Field(..., description="Explanation of how scores were computed")

    model_config = ConfigDict(from_attributes=True)
