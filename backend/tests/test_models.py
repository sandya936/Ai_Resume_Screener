import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.core.security import get_password_hash
from app.db.models.user import User
from app.db.models.user_profile import UserProfile
from app.db.models.resume import Resume
from app.db.models.resume_version import ResumeVersion
from app.db.models.analysis import Analysis
from app.db.models.job_description import JobDescription
from app.db.models.job_match import JobMatch
from app.db.models.audit_log import AuditLog


@pytest.mark.asyncio
async def test_user_and_profile_relationship(db_session: AsyncSession):
    user = User(
        email="test_models@example.com",
        hashed_password=get_password_hash("Secret123!"),
        role="user",
    )
    db_session.add(user)
    await db_session.flush()

    profile = UserProfile(
        user_id=user.id,
        full_name="Model Test User",
        target_role="Senior Full Stack Engineer",
    )
    db_session.add(profile)
    await db_session.commit()

    result = await db_session.execute(
        select(User).options(selectinload(User.profile)).where(User.id == user.id)
    )
    fetched_user = result.scalar_one()

    assert fetched_user.email == "test_models@example.com"
    assert fetched_user.profile is not None
    assert fetched_user.profile.full_name == "Model Test User"
    assert fetched_user.profile.target_role == "Senior Full Stack Engineer"


@pytest.mark.asyncio
async def test_resume_version_analysis_and_job_match_hierarchy(db_session: AsyncSession):
    # 1. Create User
    user = User(
        email="hierarchy@example.com",
        hashed_password=get_password_hash("Secret123!"),
    )
    db_session.add(user)
    await db_session.flush()

    # 2. Create Resume & Version
    resume = Resume(user_id=user.id, title="Software Architect Resume", is_primary=True)
    db_session.add(resume)
    await db_session.flush()

    version = ResumeVersion(
        resume_id=resume.id,
        version_number=1,
        filename="architect_resume.pdf",
        file_path="/uploads/architect_resume.pdf",
        file_size_bytes=204850,
        mime_type="application/pdf",
        sha256_checksum="abc123sha256checksumhash",
    )
    db_session.add(version)
    await db_session.flush()

    # 3. Create Analysis
    analysis = Analysis(
        resume_version_id=version.id,
        analysis_type="ats_score",
        status="completed",
        score=92,
        payload={"readability": "excellent", "keyword_density": 0.85},
    )
    db_session.add(analysis)

    # 4. Create Job Description & Job Match
    job_desc = JobDescription(
        user_id=user.id,
        title="Lead AI Engineer",
        company_name="TechCorp Inc",
        raw_text="Looking for an experienced Lead AI Engineer with Python & Next.js skills.",
        required_skills=["Python", "FastAPI", "Next.js", "PostgreSQL"],
    )
    db_session.add(job_desc)
    await db_session.flush()

    job_match = JobMatch(
        resume_version_id=version.id,
        job_description_id=job_desc.id,
        match_score=88,
        matching_skills=["Python", "FastAPI"],
        missing_skills=["Next.js"],
    )
    db_session.add(job_match)

    # 5. Create Audit Log
    audit_log = AuditLog(
        user_id=user.id,
        action="MATCH_ANALYSIS_CREATED",
        resource_type="job_match",
        resource_id=str(job_match.id),
        details={"match_score": 88},
    )
    db_session.add(audit_log)

    await db_session.commit()

    # 6. Verify cascading and relationships
    result = await db_session.execute(
        select(Resume)
        .options(
            selectinload(Resume.versions).selectinload(ResumeVersion.analyses),
            selectinload(Resume.versions).selectinload(ResumeVersion.job_matches),
        )
        .where(Resume.id == resume.id)
    )
    fetched_resume = result.scalar_one()

    assert fetched_resume.title == "Software Architect Resume"
    assert len(fetched_resume.versions) == 1
    assert fetched_resume.versions[0].filename == "architect_resume.pdf"
    assert len(fetched_resume.versions[0].analyses) == 1
    assert fetched_resume.versions[0].analyses[0].score == 92
    assert len(fetched_resume.versions[0].job_matches) == 1
    assert fetched_resume.versions[0].job_matches[0].match_score == 88
