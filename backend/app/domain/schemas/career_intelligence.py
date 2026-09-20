from typing import List, Optional
from pydantic import BaseModel, Field, ConfigDict


class SkillGapItem(BaseModel):
    skill_name: str = Field(..., description="Name of missing or weak skill")
    priority: str = Field(..., description="Priority: 'critical', 'medium', or 'low'")
    jd_importance: str = Field(..., description="High, Medium, or Low JD requirement")
    learning_effort: str = Field(..., description="Estimated learning effort (e.g. 1 week, 3 weeks)")
    reason: str = Field(..., description="Explanation of why this skill is a gap")


class SpecificRecommendation(BaseModel):
    target_area: str = Field(..., description="Target area: 'resume', 'project', 'learning', or 'job_prep'")
    action_title: str = Field(..., description="Concise action title")
    detailed_guidance: str = Field(..., description="Specific, non-generic actionable instructions")


class RoadmapMilestone(BaseModel):
    timeframe: str = Field(..., description="'7_day', 'week_1', 'week_2', 'week_3', or 'week_4'")
    title: str = Field(..., description="Milestone title")
    focus_skills: List[str] = Field(default_factory=list, description="Skills targeted in this phase")
    action_items: List[str] = Field(default_factory=list, description="Concrete study or project action items")
    estimated_hours: int = Field(..., description="Estimated study hours required")


class LearningRoadmap(BaseModel):
    seven_day_plan: List[RoadmapMilestone] = Field(default_factory=list, description="7-day immediate sprint milestones")
    thirty_day_plan: List[RoadmapMilestone] = Field(default_factory=list, description="4-week structured curriculum milestones")


class CareerInsightsResult(BaseModel):
    skill_gaps: List[SkillGapItem] = Field(default_factory=list, description="Categorized skill gaps")
    specific_recommendations: List[SpecificRecommendation] = Field(default_factory=list, description="Actionable recommendations")
    learning_roadmap: LearningRoadmap = Field(..., description="7-day and 30-day learning roadmap")
    known_info_summary: str = Field(..., description="Summary of verified candidate credentials")
    disclaimer: str = Field(..., description="Anti-fabrication and recommendation boundary policy")

    model_config = ConfigDict(from_attributes=True)
