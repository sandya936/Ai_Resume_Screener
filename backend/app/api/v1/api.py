from fastapi import APIRouter
from app.api.v1.endpoints import auth, users, resumes, parsing, analysis, jobs, career, interview, agents

api_v1_router = APIRouter()

api_v1_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_v1_router.include_router(users.router, prefix="/users", tags=["Users"])
api_v1_router.include_router(resumes.router, prefix="/resumes", tags=["Resumes"])
api_v1_router.include_router(parsing.router, prefix="/resumes", tags=["Resume Parsing"])
api_v1_router.include_router(analysis.router, prefix="/analysis", tags=["Resume Intelligence & ATS"])
api_v1_router.include_router(jobs.router, prefix="/jobs", tags=["Job Descriptions & Matching"])
api_v1_router.include_router(career.router, prefix="/career", tags=["Career Intelligence & Guidance"])
api_v1_router.include_router(interview.router, prefix="/interview", tags=["Interview Intelligence & Practice"])
api_v1_router.include_router(agents.router, prefix="/agents", tags=["Multi-Agent Autonomous System"])
