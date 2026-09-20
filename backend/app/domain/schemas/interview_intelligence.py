from typing import List, Optional
from pydantic import BaseModel, Field, ConfigDict


class InterviewQuestion(BaseModel):
    id: str = Field(..., description="Unique question identifier")
    category: str = Field(..., description="Category label")
    question_type: str = Field(default="resume_based", description="'resume_based' or 'hr_based'")
    question_text: str = Field(..., description="The interview question text")
    context_reason: str = Field(..., description="Why this question is relevant to candidate resume or JD gaps")
    star_talking_points: List[str] = Field(default_factory=list, description="Recommended STAR framework talking points")


class AnswerEvaluationRequest(BaseModel):
    question_id: str = Field(..., description="ID of question being answered")
    question_text: str = Field(..., description="Interview question text")
    user_answer: str = Field(..., min_length=10, description="User's practice answer text")


class AnswerEvaluationResponse(BaseModel):
    score: int = Field(..., ge=0, le=100, description="Practice answer quality score (0-100)")
    strengths: List[str] = Field(default_factory=list, description="Effective elements in candidate answer")
    missing_elements: List[str] = Field(default_factory=list, description="Missing technical details or STAR elements")
    improved_sample_answer: str = Field(..., description="High-impact exemplar answer tailored to candidate profile")
    explainable_feedback: str = Field(..., description="Detailed feedback explaining score and next steps")

    model_config = ConfigDict(from_attributes=True)
