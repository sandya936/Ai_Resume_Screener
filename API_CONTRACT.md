# AGENTX — API Contract & Specifications

This document defines the OpenAPI 3.0 compatible RESTful endpoints, request/response schemas, error handling conventions, and status codes implemented in **AGENTX**.

---

## Standard Response Structure

All endpoints return responses in a standardized JSON wrapper format:

```json
{
  "success": true,
  "data": { ... },
  "error": null,
  "timestamp": "2026-08-31T19:56:00Z"
}
```

Standard Error Format:
```json
{
  "success": false,
  "data": null,
  "error": {
    "code": "TRACE_NOT_FOUND",
    "message": "Execution session 'session-123' not found.",
    "details": []
  },
  "timestamp": "2026-08-31T19:56:00Z"
}
```

---

## Implemented Endpoint Matrix (Phases 1 - 8)

### 1. System & Health

| Method | Endpoint | Description | Auth Required | Status Code |
| :--- | :--- | :--- | :---: | :---: |
| `GET` | `/api/v1/health` | System health & status check | No | 200 OK |

### 2. Authentication & User Management (Phase 2)

| Method | Endpoint | Description | Auth Required | Status Code |
| :--- | :--- | :--- | :---: | :---: |
| `POST` | `/api/v1/auth/register` | Register user & profile with email/password | No | 201 Created |
| `POST` | `/api/v1/auth/login` | Authenticate user & issue Access + Refresh JWTs | No | 200 OK |
| `POST` | `/api/v1/auth/refresh` | Issue new access token via refresh token | No | 200 OK |
| `POST` | `/api/v1/auth/logout` | Revoke current user session | Yes | 200 OK |
| `GET` | `/api/v1/auth/me` | Fetch authenticated user details & profile | Yes | 200 OK |
| `GET` | `/api/v1/users/profile` | Retrieve user profile details | Yes | 200 OK |
| `PUT` | `/api/v1/users/profile` | Update user profile details | Yes | 200 OK |

### 3. Resume Upload & Document Processing (Phase 3)

| Method | Endpoint | Description | Auth Required | Status Code |
| :--- | :--- | :--- | :---: | :---: |
| `POST` | `/api/v1/resumes/upload` | Upload PDF/DOCX resume file, validate, store & extract | Yes | 201 Created |
| `GET` | `/api/v1/resumes` | List current user's uploaded resumes | Yes | 200 OK |
| `GET` | `/api/v1/resumes/{resume_id}` | Fetch resume container metadata & versions | Yes | 200 OK |
| `GET` | `/api/v1/resumes/versions/{version_id}` | Fetch specific resume version details | Yes | 200 OK |
| `GET` | `/api/v1/resumes/versions/{version_id}/extracted-text` | Retrieve raw extracted text & normalized structure | Yes | 200 OK |
| `DELETE` | `/api/v1/resumes/{resume_id}` | Delete resume, versions, and underlying disk files | Yes | 200 OK |

### 4. AI Resume Parsing & Structured Profile (Phase 4)

| Method | Endpoint | Description | Auth Required | Status Code |
| :--- | :--- | :--- | :---: | :---: |
| `POST` | `/api/v1/resumes/{resume_id}/parse` | Trigger AI LLM parser to extract structured profile | Yes | 200 OK |
| `GET` | `/api/v1/resumes/{resume_id}/parsed` | Retrieve candidate's stored structured resume profile | Yes | 200 OK |

### 5. Resume Intelligence & ATS Compatibility Engine (Phase 5)

| Method | Endpoint | Description | Auth Required | Status Code |
| :--- | :--- | :--- | :---: | :---: |
| `POST` | `/api/v1/analysis/ats/{resume_id}` | Trigger explainable ATS and resume quality analysis | Yes | 200 OK |
| `GET` | `/api/v1/analysis/ats/{resume_id}` | Retrieve stored explainable ATS analysis report | Yes | 200 OK |

### 6. Job Description Analysis & Resume Matching (Phase 6)

| Method | Endpoint | Description | Auth Required | Status Code |
| :--- | :--- | :--- | :---: | :---: |
| `POST` | `/api/v1/jobs` | Create/upload a Job Description posting | Yes | 201 Created |
| `GET` | `/api/v1/jobs/{job_id}` | Retrieve Job Description details and parsed structure | Yes | 200 OK |
| `POST` | `/api/v1/jobs/{job_id}/match/{resume_id}` | Execute explainable job-resume semantic match evaluation | Yes | 200 OK |
| `GET` | `/api/v1/jobs/{job_id}/match/{resume_id}` | Retrieve stored job-resume match result | Yes | 200 OK |

### 7. Career Recommendation & Interview Intelligence (Phase 7)

| Method | Endpoint | Description | Auth Required | Status Code |
| :--- | :--- | :--- | :---: | :---: |
| `POST` | `/api/v1/career/insights/{resume_id}` | Generate prioritized skill gaps & 30-day learning roadmap | Yes | 200 OK |
| `POST` | `/api/v1/interview/questions/{resume_id}` | Generate tailored question bank (Technical, Project, Behavioral, HR, JD) | Yes | 200 OK |
| `POST` | `/api/v1/interview/evaluate` | Evaluate candidate practice answer with explainable STAR feedback | Yes | 200 OK |

### 8. Autonomous Multi-Agent AI System (Phase 8 Implemented)

| Method | Endpoint | Description | Auth Required | Status Code |
| :--- | :--- | :--- | :---: | :---: |
| `POST` | `/api/v1/agents/orchestrate` | Execute multi-agent goal orchestration workflow | Yes | 200 OK |
| `GET` | `/api/v1/agents/trace/{session_id}` | Retrieve observable multi-agent execution trace graph | Yes | 200 OK |
