import pytest
from httpx import AsyncClient
from app.agents.orchestrator import ManagerOrchestratorAgent


@pytest.mark.asyncio
async def test_sandboxed_tools_execution():
    # Verify that agent tools execute cleanly in isolated environment
    pass


@pytest.mark.asyncio
async def test_agents_api_endpoints(async_client: AsyncClient):
    # 1. Register User
    reg = await async_client.post(
        "/api/v1/auth/register",
        json={"email": "agent_user@example.com", "password": "Password123!", "full_name": "Agent User"},
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
        b"BT /F1 12 Tf 100 700 Td (Agent Candidate agent_user@example.com Python FastAPI PostgreSQL Docker Git) Tj ET\n"
        b"endstream\nendobj\n"
        b"5 0 obj\n<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>\nendobj\n"
        b"xref\n0 6\n"
        b"0000000000 65535 f \n0000000009 00000 n \n0000000058 00000 n \n0000000115 00000 n \n"
        b"0000000244 00000 n \n0000000413 00000 n \n"
        b"trailer\n<< /Size 6 /Root 1 0 R >>\n"
        b"startxref\n491\n%%EOF\n"
    )
    files = {"file": ("agent_resume.pdf", pdf_bytes, "application/pdf")}
    upload_res = await async_client.post("/api/v1/resumes/upload", headers=headers, files=files)
    resume_id = upload_res.json()["data"]["resume"]["id"]

    # 3. Call POST /agents/orchestrate
    orch_payload = {
        "resume_id": resume_id,
        "raw_jd_text": "Seeking a Senior Python Backend Engineer with 4+ years in Python, FastAPI, Docker, and Kubernetes.",
        "user_goal": "Analyze my resume against this job, identify gaps, build a roadmap, and prep me for interview.",
    }
    orch_res = await async_client.post("/api/v1/agents/orchestrate", headers=headers, json=orch_payload)
    assert orch_res.status_code == 200
    res_data = orch_res.json()
    assert res_data["success"] is True

    data = res_data["data"]
    session_id = data["session_id"]
    final_plan = data["final_action_plan"]
    trace = data["execution_trace"]

    assert final_plan["candidate_name"] is not None
    assert len(trace["steps"]) == 6  # Manager + 5 Sub-Agents
    assert trace["status"] == "completed"

    # 4. Call GET /agents/trace/{session_id}
    trace_res = await async_client.get(f"/api/v1/agents/trace/{session_id}", headers=headers)
    assert trace_res.status_code == 200
    assert trace_res.json()["data"]["session_id"] == session_id
