# AGENTX — AI Resume Intelligence & Autonomous Career Platform
## Comprehensive Project Documentation

> **Project Author & Architecture**: Sandya Kaki & FastAPI Architecture  
> **Version**: 1.0 (Production Live)  
> **Frontend Live URL**: [https://frontend-pi-lime-21.vercel.app](https://frontend-pi-lime-21.vercel.app)  
> **Backend Live URL**: [https://ai-resume-screener-26ke.onrender.com](https://ai-resume-screener-26ke.onrender.com)  
> **GitHub Repository**: [https://github.com/sandya936/Ai_Resume_Screener](https://github.com/sandya936/Ai_Resume_Screener)  
> **Test Harness**: 44/44 Passing Automated Pytest Suite (100% Pass Rate)  

---

## 1. Executive Summary & Planning

### 1.1 Project Mission
**AGENTX** is a production-oriented AI Resume Intelligence & Autonomous Career Development SaaS platform. It transforms static resume documents (PDF / DOCX) into explainable, actionable, and quantifiable career growth assets. Unlike legacy arbitrary black-box ATS screeners, AGENTX uses a **60% Deterministic + 40% AI Auditor Engine**, canonical skill normalization, open mathematical job matching formulas, and an observable **6-Agent Autonomous Multi-Agent Swarm System**.

### 1.2 Development Planning & Methodology
The project was executed following strict software engineering principles:
- **Phase 1: Foundation & Core Domain Engine**: Schema definition, Pydantic domain models, document extraction engine (PDF/DOCX with magic byte validation), and database persistence layer.
- **Phase 2: ATS Scoring & Skill Normalization**: Action verb registry (100+ items), canonical keyword normalizer (`K8s` -> `kubernetes`), and 5-category explainable scoring mathematical formula.
- **Phase 3: Multi-Agent Orchestration Engine**: Built a 6-Agent autonomous system with sandboxed tool registries, execution trace logs, and state reconciliation.
- **Phase 4: Dual-Theme Frontend & Production UI**: Built a Next.js 14 App Router UI featuring dynamic state management, instant demo guest login, 40-question STAR interview studio, and a dual-theme switcher.
- **Phase 5: Automated Testing & Cloud Deployment**: 44 automated pytest unit/integration tests, zero-config SQLite/PostgreSQL layer, Render cloud backend deployment, and Vercel frontend cloud deployment.

---

## 2. Technical Stack

| Layer | Technology | Details / Purpose |
| :--- | :--- | :--- |
| **Backend Core** | FastAPI (Python 3.11+) | Asynchronous ASGI Web Framework for high concurrency |
| **Frontend Core** | Next.js 14 (App Router) | React Framework with TypeScript, Server/Client components |
| **Styling & CSS** | Vanilla CSS3 & Tailwind Utility Tokens | Dynamic CSS variables, glassmorphism, responsive grid/flex |
| **Database & ORM** | SQLAlchemy 2.0 (AsyncIO) + SQLite / PostgreSQL | Async database access with Alembic schema migration support |
| **AI LLM Providers** | Google Gemini 2.0 / OpenAI GPT-4 / Mock Engine | LLM Provider Abstraction (`BaseLLMProvider`) with fallback safety |
| **Document Processing** | `pdfplumber`, `python-docx`, `hashlib` | Magic-byte header validation (`%PDF-`, `PK\x03\x04`), SHA-256 integrity |
| **Security & Middleware** | Custom Security Middleware | PII Redaction Filter, HSTS, CSP, Correlation `X-Request-ID` |
| **Testing Harness** | Pytest 9.0+ (`pytest-asyncio`, `httpx`) | 44 automated tests covering domain, API, security, & agents |
| **Hosting & Cloud** | Vercel (Frontend) + Render (Backend) | Automatic GitHub CI/CD continuous deployment |

---

## 3. System Architecture & Multi-Agent Design

### 3.1 Monolith System Architecture
```
┌─────────────────────────────────────────────────────────────────────────┐
│                        Next.js 14 App Router UI                         │
│       (Dual Theme: Warm Crimson Parchment vs Dark Cyber Slate)         │
└────────────────────┬────────────────────────────────────────────────────┘
                     │ HTTP / REST API (JSON)
                     ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                    FastAPI Async Backend API Layer                      │
│   ├── Security Headers Middleware & Correlation ID (X-Request-ID)       │
│   ├── Rate Limiting (SlowAPI) & PII Log Redaction Filter                │
│   └── JWT / Argon2 Password Auth & Protected Routes                     │
└────────┬───────────────────┬───────────────────┬────────────────────────┘
         │                   │                   │
         ▼                   ▼                   ▼
┌─────────────────┐ ┌──────────────────┐ ┌────────────────────────┐
│ Document Engine │ │ ATS & Matcher    │ │ 6-Agent Autonomous     │
│ - PDF/DOCX      │ │ - Skill Normalizer│ │   Swarm System         │
│ - Magic Bytes   │ │ - 5-Category Math│ │ - Sandboxed Tools      │
└────────┬────────┘ └────────┬─────────┘ └──────────┬─────────────┘
         │                   │                      │
         └───────────────────┼──────────────────────┘
                             ▼
┌─────────────────────────────────────────────────────────────────────────┐
│               Async Data Layer (SQLAlchemy 2.0 ORM)                     │
│                  - SQLite / PostgreSQL Async Engine                     │
└─────────────────────────────────────────────────────────────────────────┘
```

### 3.2 Autonomous 6-Agent Swarm System
The multi-agent system uses a manager-worker topology with sandboxed tool execution:

```
                      ┌───────────────────────────────┐
                      │    ManagerOrchestratorAgent   │
                      │  (Plan Decomposition & State) │
                      └───────────────┬───────────────┘
                                      │
         ┌────────────────────────────┼────────────────────────────┐
         │                            │                            │
         ▼                            ▼                            ▼
┌─────────────────┐          ┌─────────────────┐          ┌─────────────────┐
│   ResumeAgent   │          │ JobDescription  │          │  SkillGapAgent  │
│                 │          │      Agent      │          │                 │
│ Tool:           │          │ Tool:           │          │ Tool:           │
│ tool_fetch_     │          │ tool_parse_     │          │ tool_evaluate_  │
│ resume          │          │ job             │          │ match           │
└─────────────────┘          └─────────────────┘          └─────────────────┘
         │                            │                            │
         └────────────────────────────┼────────────────────────────┘
                                      │
         ┌────────────────────────────┴────────────────────────────┐
         │                                                         │
         ▼                                                         ▼
┌─────────────────┐                                       ┌─────────────────┐
│ Recommendation  │                                       │ InterviewAgent  │
│      Agent      │                                       │                 │
│ Tool:           │                                       │ Tool:           │
│ tool_generate_  │                                       │ tool_generate_  │
│ roadmap         │                                       │ interview_      │
│                 │                                       │ questions       │
└─────────────────┘          └─────────────────┘          └─────────────────┘
```

---

## 4. UI Design & Aesthetics Architecture

### 4.1 Visual Design Philosophy
The AGENTX interface is designed to evoke executive-level polish, clarity, and delight:
- **Zero Browser Fallbacks**: Modern Google Fonts (`Outfit`, `Inter`), rich CSS variables, and seamless layout transitions.
- **Glassmorphism & Micro-Animations**: Card hover elevations (`translateY(-2px)`), gold border glows, smooth state transitions.
- **Responsive Layout Grid**: Full desktop, tablet, and mobile support.

### 4.2 Dual-Theme System (`agentx_theme`)
Users can switch between two curated visual themes at any time via the top navigation toggle bar:

1. **Warm Crimson Parchment Theme** (`theme-parchment`):
   - Background: Sandstone Parchment (`#F4EFEB`, `#EFE8E1`)
   - Accent Primary: Rich Crimson (`#8B0000`, `#9E1B1B`)
   - Accent Secondary: Warm Gold & Sandstone
   - Typography: Dark Espresso (`#2C221E`, `#4A3B32`)

2. **Dark Cyber Slate Theme** (`theme-dark`):
   - Background: Deep Obsidian / Cyber Slate (`#0B0F17`, `#111827`)
   - Accent Primary: Electric Emerald (`#10B981`, `#059669`)
   - Accent Secondary: Cyber Gold & Neon Cyan
   - Typography: Crisp White & Slate Grey (`#F9FAFB`, `#9CA3AF`)

---

## 5. Core Implementation Features

### 5.1 Secure Document Parsing & Validation
- **Magic Byte Check**: Validates `%PDF-` for PDFs and `PK\x03\x04` for DOCX files to prevent malicious file extension spoofing.
- **File Integrity**: SHA-256 checksum generation for duplicate detection.
- **Path Traversal Protection**: File basenames are sanitized using regex uuid generation before writing to isolated storage.

### 5.2 Canonical Skill Normalizer (`SkillNormalizer`)
Maps over 150+ tech acronyms and variants into standard canonical forms:
- `K8s`, `k8s` -> `kubernetes`
- `Postgres`, `postgresql` -> `postgresql`
- `JS`, `JavaScript` -> `javascript`
- `AWS`, `Amazon Web Services` -> `aws`

### 5.3 5-Category Mathematical Job Matching Engine
Evaluates candidate fit using a weighted mathematical formula:
Overall Match Score = (Required Skills Match * 0.40) + (Preferred Skills Match * 0.15) + (Experience Match * 0.25) + (Project Relevance * 0.10) + (Education Match * 0.10)

### 5.4 40-Question STAR Interview Practice Studio
- Generates 40 custom interview questions across 5 distinct categories:
  - Technical Deep Dives (10 questions)
  - Behavioral STAR Scenarios (10 questions)
  - Project Experience Dives (8 questions)
  - HR & Fit Questions (6 questions)
  - Job Description Specific (6 questions)
- Features real-time answer input, STAR framework evaluation, and instant performance feedback.

### 5.5 PII Redaction & Security Hardening
- **PII Redaction Filter**: Automatically strips email addresses, phone numbers, and SSNs from production logger outputs.
- **Security Headers**: Injects `X-Content-Type-Options: nosniff`, `X-Frame-Options: DENY`, `Strict-Transport-Security`, and `Content-Security-Policy`.
- **Correlation ID**: Attaches unique `X-Request-ID` to every HTTP request for full execution observability.

---

## 6. Verification & Automated Test Suite

The project includes an automated Pytest test suite covering all services, APIs, and edge cases:

```bash
cd backend
python -m pytest -v
```

### Test Results Breakdown:
- `test_ats_analysis.py`: 3/3 passed
- `test_auth.py`: 7/7 passed
- `test_career_intelligence.py`: 3/3 passed
- `test_health.py`: 1/1 passed
- `test_job_matching.py`: 3/3 passed
- `test_models.py`: 2/2 passed
- `test_multi_agent_system.py`: 2/2 passed
- `test_resilience_and_edge_cases.py`: 3/3 passed
- `test_resume_parsing.py`: 5/5 passed
- `test_resume_processing.py`: 9/9 passed
- `test_security_and_hardening.py`: 4/4 passed
- `test_user_profile.py`: 2/2 passed
- **Total**: **44 / 44 PASSED (100%)**

---

## 7. Deployment Architecture

### Backend Deployment (Render Cloud)
- **Runtime**: Python 3.11 ASGI Uvicorn Web Service
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `python -m uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- **Live Endpoint**: `https://ai-resume-screener-26ke.onrender.com`

### Frontend Deployment (Vercel Cloud)
- **Framework**: Next.js 14 App Router
- **Root Directory**: `frontend`
- **Build Command**: `npm run build`
- **Environment Variable**: `NEXT_PUBLIC_API_BASE_URL=https://ai-resume-screener-26ke.onrender.com`
- **Live Endpoint**: `https://frontend-pi-lime-21.vercel.app`

---

## 8. Attribution & Copyright
**© 2026 AGENTX AI Platform. All rights reserved.**  
*Powered by Sandya Kaki & FastAPI Architecture.*
