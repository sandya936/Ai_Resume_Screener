# AGENTX — Technology Stack Specifications

This document defines the selected technology stack, version constraints, and technical rationale for **AGENTX**.

---

## 1. Backend Core Technology Stack

| Technology | Selected Tool | Version | Purpose / Rationale |
| :--- | :--- | :--- | :--- |
| **Language** | Python | `^3.11` | Industry standard for AI/ML integration, rapid development, typing support. |
| **Web Framework** | FastAPI | `^0.110.0` | High performance, native async support, automatic OpenAPI doc generation. |
| **Data Validation** | Pydantic | `^2.6.0` | High-speed data validation, strict schema enforcement for LLM responses. |
| **ORM** | SQLAlchemy | `^2.0.25` | Modern async ORM, robust transaction management, migration ecosystem. |
| **Database Driver** | asyncpg | `^0.29.0` | Ultra-fast asynchronous PostgreSQL driver for Python. |
| **DB Migrations** | Alembic | `^1.13.0` | Declarative, version-controlled database schema migrations. |
| **Security & Auth** | PyJWT / Passlib / Argon2 | `^2.8.0` | Enterprise-grade JWT token issuance and password hashing. |
| **Document Extract**| pdfplumber / python-docx | `^0.10.3` | Accurate textual and structural extraction from PDF and DOCX files. |
| **Testing** | Pytest / HTTPX | `^8.0.0` | Async unit, integration, and API testing framework. |

---

## 2. Frontend Core Technology Stack

| Technology | Selected Tool | Version | Purpose / Rationale |
| :--- | :--- | :--- | :--- |
| **Framework** | Next.js (App Router) | `^14.1.0` | Server-Side Rendering (SSR), React 18 Server Components, optimized SEO & routing. |
| **Language** | TypeScript | `^5.3.0` | End-to-end type safety shared with API schemas. |
| **Styling** | Tailwind CSS | `^3.4.0` | Utility-first, dynamic responsive styling with custom dark theme support. |
| **Icons** | Lucide React | `^0.330.0` | Modern, lightweight icon library. |
| **State & HTTP** | Axios / TanStack Query | `^5.18.0` | Declarative data fetching, caching, and server state management. |

---

## 3. Database & AI Infrastructure

- **Database**: PostgreSQL 16
- **Vector Storage**: `pgvector` extension (for embedding similarity matching)
- **AI Provider Integration**: Abstract Provider Interface with concrete connectors:
  - Google Gemini API (`google-generativeai` / `google-genai`)
  - OpenAI API (`openai`)
  - Anthropic Claude API (`anthropic`)
- **Containerization**: Docker Compose (multi-stage builds for frontend, backend, and PostgreSQL).
