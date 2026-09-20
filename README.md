# AGENTX — Production-Ready AI Resume Intelligence & Autonomous Career Platform

> **Version**: 1.0 (Production-Oriented Complete)  
> **Architecture**: Modular Monolith Async FastAPI Backend + Next.js 14 App Router SaaS Frontend  
> **AI Architecture**: 6-Agent Autonomous System & Sandboxed Tool Registry  
> **Test Harness**: 44/44 Passing Automated Pytest Suite  

---

## Executive Overview

**AGENTX** is a production-oriented AI Resume Intelligence SaaS platform designed to transform static resumes into actionable, explainable career development plans. Built on a high-performance **Modular Monolith** architecture in FastAPI (Async Python 3.11) and Next.js 14+ (App Router), AGENTX replaces arbitrary black-box LLM scoring with an explainable **60% Deterministic + 40% AI Auditor Engine**, a **Skill Normalizer** (`K8s` -> `kubernetes`), a **5-Category Open Mathematical Matching Formula**, and an observable **6-Agent Autonomous System**.

---

## Key Features

1. **Secure Document Processing**: PDF & DOCX extraction with magic bytes header verification (`%PDF-`, `PK\x03\x04`), 10MB size guardrails, path traversal sanitization, and isolated storage.
2. **AI Resume Parsing & Provider Abstraction**: LLM Provider Abstraction (`BaseLLMProvider`) supporting Google Gemini, OpenAI, and a deterministic mock fallback engine with 30s timeout guards and `<RESUME_DATA>` prompt injection defenses.
3. **Explainable ATS Scoring**: Transparent scoring engine evaluating action verb density (100+ action verb registry), quantitative metric presence (`%/$`), section completeness, and formatting risks.
4. **Job Description Ingestion & Skill Normalizer**: `SkillNormalizer` canonical synonym mapping (`K8s` -> `kubernetes`, `Postgres` -> `postgresql`, `JS` -> `javascript`) eliminating false-negative skill gap flags.
5. **5-Category Explainable Job Matching**:
   ```
   Overall Match Score = (Required_Skills_Match * 0.40) + 
                         (Preferred_Skills_Match * 0.15) + 
                         (Experience_Match * 0.25) + 
                         (Project_Relevance * 0.10) + 
                         (Education_Match * 0.10)
   ```
6. **Career Intelligence & 30-Day Learning Roadmap**: Prioritized skill gap engine (`Critical`, `Medium`, `Low`) and personalized 30-day learning curriculum with an enforced **Anti-Fabrication Policy**.
7. **Interview Intelligence & STAR Practice Studio**: 5-Category tailored question bank (Technical, Project, Behavioral, HR, JD-Specific) and practice answer evaluation scoring STAR framework elements.
8. **Autonomous Multi-Agent System**: 6 specialized agents (`ManagerOrchestratorAgent`, `ResumeAgent`, `JobDescriptionAgent`, `SkillGapAgent`, `RecommendationAgent`, `InterviewAgent`) executing sandboxed tools (`SandboxedAgentTools`) with an observable trace graph.
9. **Production Security & Observability**: Security Headers Middleware (CSP, HSTS, X-Frame-Options), Correlation Request ID tracking (`X-Request-ID`), PII Log Redaction Filter (`PIIRedactionFilter`), and global unhandled exception sanitization.

---

## Multi-Agent Architecture

```
User Goal Request
    ↓
ManagerOrchestratorAgent (Decomposes goal into plan)
    ├─> 1. ResumeAgent (Tool: tool_fetch_resume)
    ├─> 2. JobDescriptionAgent (Tool: tool_parse_job)
    ├─> 3. SkillGapAgent (Tool: tool_evaluate_match)
    ├─> 4. RecommendationAgent (Tool: tool_generate_roadmap)
    └─> 5. InterviewAgent (Tool: tool_generate_interview_questions)
    ↓
Validation & State Aggregation
    ↓
FinalCareerActionPlan + AgentExecutionSession Trace Graph
```

---

## Quickstart Guide

### Prerequisites
- Docker & Docker Compose
- Python 3.11+
- Node.js 20+

### Option A: Docker Compose Deployment (Recommended)
```bash
# 1. Clone repository & copy environment template
cp .env.example .env

# 2. Launch multi-container stack (PostgreSQL, Backend, Frontend)
docker-compose up -d --build

# 3. Check health status
curl http://localhost:8000/api/v1/health
```
Access the application:
- **Frontend Dashboard**: `http://localhost:3000`
- **Backend API Docs**: `http://localhost:8000/api/v1/docs`

---

## Test Verification Suite

Run full Pytest backend test suite:
```bash
cd backend
python -m pytest -v
```

**Results**: **44 passed in 2.70s (100% PASSING)**.

---

## Master Documentation System

1. [`PROJECT_STATE.md`](file:///c:/Users/sandy/OneDrive/Desktop/resume_screener/PROJECT_STATE.md) — Master project state v1.0 complete
2. [`ARCHITECTURE.md`](file:///c:/Users/sandy/OneDrive/Desktop/resume_screener/ARCHITECTURE.md) — Modular monolith & multi-agent system blueprints
3. [`DECISIONS.md`](file:///c:/Users/sandy/OneDrive/Desktop/resume_screener/DECISIONS.md) — 16 Architecture Decision Records (ADR 001 - 016)
4. [`DATABASE_SCHEMA.md`](file:///c:/Users/sandy/OneDrive/Desktop/resume_screener/DATABASE_SCHEMA.md) — Relational entity schemas & ER diagrams
5. [`API_CONTRACT.md`](file:///c:/Users/sandy/OneDrive/Desktop/resume_screener/API_CONTRACT.md) — OpenAPI 3.0 REST endpoints specification
6. [`SECURITY.md`](file:///c:/Users/sandy/OneDrive/Desktop/resume_screener/SECURITY.md) — Security headers, PII logging, prompt injection controls
7. [`KNOWN_ISSUES.md`](file:///c:/Users/sandy/OneDrive/Desktop/resume_screener/KNOWN_ISSUES.md) — Risk matrix & technical debt log
8. [`CHANGELOG.md`](file:///c:/Users/sandy/OneDrive/Desktop/resume_screener/CHANGELOG.md) — Version release notes v0.1.0 to v1.0.0
9. [`DEPLOYMENT.md`](file:///c:/Users/sandy/OneDrive/Desktop/resume_screener/DEPLOYMENT.md) — Production setup & Docker deployment manual
10. [`DEMO_GUIDE.md`](file:///c:/Users/sandy/OneDrive/Desktop/resume_screener/DEMO_GUIDE.md) — Live presentation script & tech-fest demo guide
11. [`FINAL_PROJECT_REPORT.md`](file:///c:/Users/sandy/OneDrive/Desktop/resume_screener/FINAL_PROJECT_REPORT.md) — 20-Section academic project report
12. [`TECH_FEST_PRESENTATION.md`](file:///c:/Users/sandy/OneDrive/Desktop/resume_screener/TECH_FEST_PRESENTATION.md) — 12-Slide Tech-Fest presentation deck
13. [`FINAL_REVIEW.md`](file:///c:/Users/sandy/OneDrive/Desktop/resume_screener/FINAL_REVIEW.md) — Final audit, viva notes & project review
