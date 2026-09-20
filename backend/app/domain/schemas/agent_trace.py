import uuid
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field, ConfigDict


class AgentStepTrace(BaseModel):
    agent_name: str = Field(..., description="Name of execution agent")
    status: str = Field(..., description="'pending', 'running', 'completed', or 'failed'")
    input_payload: Dict[str, Any] = Field(default_factory=dict, description="Input parameters passed to agent")
    output_payload: Optional[Dict[str, Any]] = Field(None, description="Output payload produced by agent")
    tool_calls: List[str] = Field(default_factory=list, description="List of sandboxed tool functions executed")
    execution_time_ms: int = Field(default=0, description="Duration in milliseconds")
    error_message: Optional[str] = Field(None, description="Error message if step failed")


class FinalCareerActionPlan(BaseModel):
    user_goal: str = Field(..., description="Target user goal")
    candidate_name: Optional[str] = Field(None, description="Candidate name")
    job_title: Optional[str] = Field(None, description="Target job title")
    overall_match_score: Optional[int] = Field(None, description="Overall Job Match Score")
    ats_compatibility_score: Optional[int] = Field(None, description="ATS Compatibility Estimate Score")
    matched_skills: List[str] = Field(default_factory=list)
    missing_skills: List[str] = Field(default_factory=list)
    critical_gaps: List[Dict[str, Any]] = Field(default_factory=list)
    learning_roadmap_30_day: List[Dict[str, Any]] = Field(default_factory=list)
    interview_question_bank: List[Dict[str, Any]] = Field(default_factory=list)
    executive_summary: str = Field(..., description="Action plan summary synthesized by Manager Agent")

    model_config = ConfigDict(from_attributes=True)


class AgentExecutionSession(BaseModel):
    session_id: str = Field(..., description="Unique execution session ID")
    user_goal: str = Field(..., description="Target user goal")
    status: str = Field(..., description="'completed', 'partially_completed', or 'failed'")
    steps: List[AgentStepTrace] = Field(default_factory=list, description="Step-by-step trace graph")
    final_action_plan: Optional[FinalCareerActionPlan] = Field(None)
    total_duration_ms: int = Field(default=0, description="Total multi-agent workflow duration in ms")

    model_config = ConfigDict(from_attributes=True)


class OrchestrationRequest(BaseModel):
    resume_id: uuid.UUID = Field(..., description="Candidate resume ID")
    job_id: Optional[uuid.UUID] = Field(None, description="Optional target Job Description ID")
    raw_jd_text: Optional[str] = Field(None, description="Optional pasted Job Description text")
    user_goal: str = Field(
        "Analyze my resume against this job, identify my gaps, create a learning plan, and prepare me for the interview.",
        description="Target user goal",
    )


class OrchestrationResponse(BaseModel):
    session_id: str
    status: str
    final_action_plan: FinalCareerActionPlan
    execution_trace: AgentExecutionSession

    model_config = ConfigDict(from_attributes=True)
