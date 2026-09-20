# AGENTX — Master Engineering Roadmap

This document defines the 10-phase sequential execution plan for building **AGENTX** — a production-ready AI Resume Intelligence & Career Platform.

---

## Phase Overview Matrix

| Phase | Module / Focus | Status | Key Deliverable |
| :---: | :--- | :---: | :--- |
| **Phase 1** | **Foundation & Architecture** | **COMPLETED** | System blueprints, 11 master docs, project scaffolding |
| **Phase 2** | Core Data Models & Infrastructure | Pending | Database models, Alembic migrations, DB session management |
| **Phase 3** | Auth & User Management System | Pending | JWT auth, RBAC, registration/login, user profile API |
| **Phase 4** | Resume Ingestion & Storage Pipeline | Pending | PDF/DOCX upload, secure storage, file validation, SHA256 checksums |
| **Phase 5** | Resume Parsing & Extraction Engine | Pending | Multi-format text extraction, Pydantic structured resume schemas, LLM parser |
| **Phase 6** | Resume Quality & ATS Analysis Engine | Pending | Quantitative scoring, ATS parser simulation, section audit engine |
| **Phase 7** | Job Matching & Skill Gap Engine | Pending | Job description ingestion, vector/keyword matching, skill gap matrix |
| **Phase 8** | Career Roadmap & Interview Generator | Pending | AI personalized skill roadmap, contextual interview question generator |
| **Phase 9** | Multi-Agent AI Orchestrator (AgentX Brain) | Pending | Multi-agent state graph (Extractor, Scorer, Matcher, Advisor), execution tracer |
| **Phase 10** | SaaS Dashboard UI, E2E Integration & Polish | Pending | Next.js dynamic dashboard, analytics visualizer, E2E testing, docker build |

---

## Detailed Phase Breakdown

### Phase 1 — Foundation & Architecture (COMPLETED)
- Inspect workspace and design clean architecture.
- Document 11 master state files (`PROJECT_STATE.md`, `ROADMAP.md`, `ARCHITECTURE.md`, `TECH_STACK.md`, `DECISIONS.md`, `DATABASE_SCHEMA.md`, `API_CONTRACT.md`, `SECURITY.md`, `DEVELOPMENT_GUIDELINES.md`, `KNOWN_ISSUES.md`, `CHANGELOG.md`).
- Scaffold initial FastAPI backend and Next.js frontend directory structure.

### Phase 2 — Core Data Models & Infrastructure Setup
- Implement SQLAlchemy 2.0 async models: `User`, `Resume`, `ParsedData`, `JobDescription`, `MatchAnalysis`, `CareerRoadmap`, `InterviewQuestion`, `AuditLog`.
- Configure Alembic migrations workflow.
- Set up DB repository pattern and async unit tests.

### Phase 3 — Auth & User Management System
- User registration, password hashing (Argon2 / bcrypt), JWT authentication (Access & Refresh tokens).
- Role-Based Access Control (`User`, `Recruiter`, `Admin`).
- Auth API endpoints & Next.js Auth context integration.

### Phase 4 — Resume Ingestion & Storage Pipeline
- File upload router with MIME validation, file size limits (10MB), and malware/sanitization check.
- Local secure disk storage / S3-compatible abstraction with encrypted file paths and SHA256 deduplication.
- Storage repository and metadata database tracking.

### Phase 5 — Resume Parsing & Information Extraction Engine
- Multi-format text extractor (pdfplumber, PyPDF2, python-docx).
- Pydantic domain models for Structured Resume (Contact, Education, Work Experience, Skills, Certifications, Projects).
- LLM extraction pipeline with provider fallback and strict JSON schema enforcement.

### Phase 6 — Resume Quality & ATS Compatibility Analysis Engine
- Quantitative ATS compatibility scoring algorithm (0 - 100 scale).
- Section presence, formatting, keyword density, and impact metric audit engine.
- Actionable improvement recommendations generator with explainable reasoning.

### Phase 7 — Job Description Processing & Resume-Job Matching Engine
- Job Description ingestion & structured keyword/requirement extractor.
- Hybrid matching algorithm (Keyword overlap + Semantic vector embedding similarity).
- Detailed skill gap breakdown matrix (Missing Hard Skills, Soft Skills, Experience delta).

### Phase 8 — AI Skill Gap, Career Roadmap & Interview Question Generator
- Step-by-step career progression roadmap generator based on target roles.
- Customized technical & behavioral interview question generator with sample answer key and scoring rubrics.

### Phase 9 — Multi-Agent Orchestration Engine (AgentX Brain)
- Autonomous Multi-Agent workflow orchestrator:
  - **Extractor Agent**: Parses raw resume document into structured entity format.
  - **ATS Quality Agent**: Evaluates structural integrity, readability, and ATS metrics.
  - **Job Matcher Agent**: Performs semantic comparison against target Job Descriptions.
  - **Career Advisor Agent**: Synthesizes analysis to generate roadmaps and interview questions.
- Step-by-step agent trace logger & execution status stream.

### Phase 10 — SaaS Dashboard UI, E2E Integration & Production Hardening
- Production Next.js SaaS user interface: Upload workspace, Resume view, ATS score card, Job matcher modal, Career roadmap timeline, Interview quiz module.
- End-to-end integration tests & performance optimizations.
- Docker production images build, security hardening check, and final project documentation update.
