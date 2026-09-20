# AGENTX — System Architecture Blueprint

This document details the high-level architecture, module boundaries, data flows, clean architecture principles, and multi-agent AI topology for **AGENTX**.

---

## 1. Architectural Style & Design Principles

AGENTX is designed as a **Modular Monolith** applying **Clean Architecture** (Hexagonal Architecture / Ports and Adapters) principles.

```
+-----------------------------------------------------------------------+
|                             PRESENTATION                              |
|           Next.js 14 Dashboard / React / Tailwind CSS / Web           |
+-----------------------------------------------------------------------+
                                   │  (HTTPS / JSON REST API)
                                   ▼
+-----------------------------------------------------------------------+
|                              API LAYER                                |
|        FastAPI Controllers / OpenAPI / Middleware / Auth Guards       |
+-----------------------------------------------------------------------+
                                   │
                                   ▼
+-----------------------------------------------------------------------+
|                          APPLICATION LAYER                            |
|     Use Cases / Business Workflows / Multi-Agent Orchestrator         |
+-----------------------------------------------------------------------+
                                   │
                                   ▼
+-----------------------------------------------------------------------+
|                            DOMAIN LAYER                               |
|   Core Entities / Value Objects / Domain Services / Validation Rules  |
+-----------------------------------------------------------------------+
                                   │
                                   ▼
+-----------------------------------------------------------------------+
|                        INFRASTRUCTURE LAYER                           |
|  SQLAlchemy Repositories / LLM Providers / Storage / Vector Engine   |
+-----------------------------------------------------------------------+
                                   │
                                   ▼
+-----------------------------------------------------------------------+
|                         EXTERNAL RESOURCES                            |
|    PostgreSQL DB / Disk Storage / OpenAI / Gemini / Anthropic APIs    |
+-----------------------------------------------------------------------+
```

### Key Architectural Guidelines:
1. **Dependency Rule**: Dependencies point inward. The Domain layer has zero dependencies on external frameworks or databases.
2. **Provider Abstraction**: All LLMs, file storage, and external APIs are accessed via interfaces defined in the domain layer.
3. **API-First Design**: REST contracts are strictly typed using Pydantic schemas.
4. **Explainable AI**: AI outputs are parsed into strict JSON schemas with confidence scores and execution trace logging.

---

## 2. Multi-Agent AI Workflow Topology

```
                  ┌──────────────────────────────┐
                  │    Raw Document (PDF/DOCX)   │
                  └──────────────┬───────────────┘
                                 │
                                 ▼
                  ┌──────────────────────────────┐
                  │      Extraction Agent        │
                  │  (Multi-format Text & LLM)   │
                  └──────────────┬───────────────┘
                                 │
                                 ▼
                  ┌──────────────────────────────┐
                  │     Structured Resume Entity │
                  └──────────────┬───────────────┘
                                 │
                 ┌───────────────┴───────────────┐
                 │                               │
                 ▼                               ▼
  ┌─────────────────────────────┐ ┌─────────────────────────────┐
  │      ATS Scoring Agent      │ │     Job Matching Agent      │
  │  (Quality Audit & ATS Fit)  │ │ (Vector Match & Skill Gaps) │
  └──────────────┬──────────────┘ └──────────────┬──────────────┘
                 │                               │
                 └───────────────┬───────────────┘
                                 │
                                 ▼
                  ┌──────────────────────────────┐
                  │     Career Advisor Agent     │
                  │ (Roadmaps & Interview Quiz)  │
                  └──────────────┬───────────────┘
                                 │
                                 ▼
                  ┌──────────────────────────────┐
                  │  Career Intelligence Output  │
                  └──────────────────────────────┘
```

### Agent Roles:
- **Extractor Agent**: Extracts clean text, normalizes dates, separates contact details, education, work experience, projects, skills, and certifications into a unified Pydantic model.
- **ATS Quality Agent**: Evaluates resume formatting, readability, section metrics, action verb density, impact metrics (quantified achievements), and calculates an ATS compatibility score (0-100).
- **Job Matcher Agent**: Ingests job description, extracts required vs. optional skills, performs semantic similarity matching, and generates a structured skill gap matrix.
- **Career Advisor Agent**: Takes ATS analysis and skill gaps to build a target-oriented learning roadmap and role-specific interview preparation package.

---

## 3. Storage & Infrastructure Layering

- **Relational Storage**: PostgreSQL 16 managed via SQLAlchemy 2.0 Async Engine with Alembic schema migrations.
- **Vector Search Engine**: PostgreSQL with `pgvector` extension for storing and querying 1536-dimensional embeddings of skills, experience snippets, and job postings.
- **File Repository**: Local file system abstraction (swappable with AWS S3 / Cloud Storage) with SHA-256 deduplication and AES-256 path masking.
- **Security Middleware**: CORS, Rate Limiting (SlowAPI), JWT Bearer Auth middleware, Security Headers (HSTS, CSP, X-Frame-Options).
