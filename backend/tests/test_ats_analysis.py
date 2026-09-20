import pytest
from httpx import AsyncClient
from app.domain.schemas.structured_resume import (
    StructuredResume,
    PersonalInfo,
    WorkExperienceEntry,
    SkillCategory,
    EducationEntry,
    ProjectEntry,
)
from app.services.ats_analyzer.deterministic_rules import DeterministicRulesEngine


def test_deterministic_action_verbs_and_metrics():
    resume = StructuredResume(
        personal_info=PersonalInfo(
            full_name="Bob Smith",
            email="bob@example.com",
            phone="555-999-0000",
        ),
        summary="Engineered scalable cloud applications with microservice architecture and high concurrency resilience.",
        work_experience=[
            WorkExperienceEntry(
                company="TechCorp Inc",
                title="Senior Software Architect",
                accomplishments=[
                    "Architected microservices reducing API latency by 45%.",
                    "Spearheaded database migration saving $150k annually across cloud infrastructure.",
                    "Optimized throughput for 10M daily requests across distributed Kubernetes clusters.",
                    "Automated CI/CD deployment pipelines using GitHub Actions and Docker.",
                    "Led a cross-functional engineering team of 12 backend developers.",
                ],
            )
        ],
        skills=SkillCategory(technical_skills=["Python", "FastAPI", "Docker", "PostgreSQL", "AWS", "Git"]),
        education=[EducationEntry(institution="Massachusetts Institute of Technology", degree="B.S. CS")],
        projects=[
            ProjectEntry(
                title="Cloud Scaling Engine",
                description="Engineered high throughput event bus processing 50k messages per second.",
                technologies=["Python", "Kafka"],
            )
        ],
    )

    raw_text = (
        "Bob Smith | bob@example.com | 555-999-0000 | San Francisco, CA | linkedin.com/in/bobsmith\n"
        "Professional Summary: Senior Software Architect with 8 years of experience building resilient cloud applications.\n"
        "Work Experience:\n"
        "Senior Software Architect - TechCorp Inc (2020 - Present)\n"
        "- Architected microservices reducing API latency by 45%.\n"
        "- Spearheaded database migration saving $150k annually across cloud infrastructure.\n"
        "- Optimized throughput for 10M daily requests across distributed Kubernetes clusters.\n"
        "- Automated CI/CD deployment pipelines using GitHub Actions and Docker.\n"
        "- Led a cross-functional engineering team of 12 backend developers.\n"
        "Education:\n"
        "Bachelor of Science in Computer Science - Massachusetts Institute of Technology (2014 - 2018)\n"
        "Skills:\n"
        "Technical Skills: Python, FastAPI, Docker, PostgreSQL, AWS, Git, Kubernetes, Linux, REST API\n"
    )

    res = DeterministicRulesEngine.evaluate(resume, raw_text)

    assert res["ats_compatibility_score"] >= 80
    assert res["content_quality_score"] >= 80
    assert res["experience_score"] >= 80
    assert len(res["strengths"]) >= 2
    assert any("action verbs" in s.lower() for s in res["strengths"])


def test_missing_metrics_and_action_verbs():
    resume = StructuredResume(
        personal_info=PersonalInfo(
            full_name="Candidate",
            email="cand@example.com",
            phone="1234567890",
        ),
        summary="Basic summary",
        work_experience=[
            WorkExperienceEntry(
                company="Company A",
                title="Developer",
                accomplishments=["Worked on bug fixes and maintenance."],
            )
        ],
        skills=SkillCategory(technical_skills=["HTML"]),
    )

    raw_text = "Candidate cand@example.com 1234567890 Worked on bug fixes and maintenance."

    res = DeterministicRulesEngine.evaluate(resume, raw_text)

    assert res["content_quality_score"] < 60
    assert res["experience_score"] < 60
    assert any("quantifiable metrics" in w.lower() for w in res["weaknesses"])


@pytest.mark.asyncio
async def test_ats_analysis_api_endpoints(async_client: AsyncClient):
    # 1. Register User
    reg = await async_client.post(
        "/api/v1/auth/register",
        json={"email": "ats_user@example.com", "password": "Password123!", "full_name": "ATS Candidate"},
    )
    token = reg.json()["data"]["tokens"]["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 2. Upload Resume PDF
    pdf_bytes = (
        b"%PDF-1.4\n"
        b"1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n"
        b"2 0 obj\n<< /Type /Pages /Kids [3 0 R] /Count 1 >>\nendobj\n"
        b"3 0 obj\n<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Contents 4 0 R /Resources << /Font << /F1 5 0 R >> >> >>\nendobj\n"
        b"4 0 obj\n<< /Length 120 >>\nstream\n"
        b"BT /F1 12 Tf 100 700 Td (ATS Candidate ats_user@example.com Architected Python FastAPI microservices reducing latency by 40%.) Tj ET\n"
        b"endstream\nendobj\n"
        b"5 0 obj\n<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>\nendobj\n"
        b"xref\n0 6\n"
        b"0000000000 65535 f \n0000000009 00000 n \n0000000058 00000 n \n0000000115 00000 n \n"
        b"0000000244 00000 n \n0000000413 00000 n \n"
        b"trailer\n<< /Size 6 /Root 1 0 R >>\n"
        b"startxref\n491\n%%EOF\n"
    )
    files = {"file": ("ats_resume.pdf", pdf_bytes, "application/pdf")}
    upload_res = await async_client.post("/api/v1/resumes/upload", headers=headers, files=files)
    resume_id = upload_res.json()["data"]["resume"]["id"]

    # 3. Call POST /resumes/{id}/parse first to parse document
    await async_client.post(f"/api/v1/resumes/{resume_id}/parse?provider=mock", headers=headers)

    # 4. Call POST /analysis/ats/{id}
    analysis_res = await async_client.post(f"/api/v1/analysis/ats/{resume_id}", headers=headers)
    assert analysis_res.status_code == 200
    res_data = analysis_res.json()
    assert res_data["success"] is True
    ats = res_data["data"]["ats_analysis"]
    assert "overall_score" in ats
    assert "ats_compatibility_score" in ats
    assert len(ats["category_scores"]) == 7
    assert len(ats["actionable_improvements"]) >= 1

    # 5. Call GET /analysis/ats/{id}
    get_res = await async_client.get(f"/api/v1/analysis/ats/{resume_id}", headers=headers)
    assert get_res.status_code == 200
    assert get_res.json()["data"]["ats_analysis"]["overall_score"] == ats["overall_score"]
