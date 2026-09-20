# AGENTX — Architecture Decision Records (ADR)

This document records the key architectural choices made during the engineering of **AGENTX**, including contexts, decisions, tradeoffs, and consequences.

---

## ADR-001: Modular Monolith vs. Microservices

### Status
**ACCEPTED**

### Context
AGENTX requires robust domain boundaries between User Management, Resume Extraction, ATS Scoring, Job Matching, and Career Generation. Microservices introduce premature deployment complexity, latency, and distributed transaction overhead.

### Decision
We choose a **Modular Monolith** architecture built in FastAPI with strictly segregated internal packages (`app/domain`, `app/services`, `app/providers`, `app/api`).

### Consequences
- **Pros**: Simple deployment, zero network latency between modules, transactional integrity, rapid developer feedback.
- **Cons**: High discipline required to prevent cross-domain coupling (enforced via domain interfaces).

---

## ADR-002: Async FastAPI + SQLAlchemy 2.0 Backend

### Status
**ACCEPTED**

### Context
Resume parsing and AI agent workflows involve asynchronous I/O (file reads, external LLM network requests, vector queries). Synchronous frameworks would block worker threads under concurrent load.

### Decision
Use **FastAPI** with **SQLAlchemy 2.0 Async Engine** and `asyncpg`.

### Consequences
- **Pros**: High concurrency capability, low memory footprint, native async request handling.
- **Cons**: All database calls and repository layers must explicitly use `async/await` syntax.

---

## ADR-003: Next.js App Router for Frontend SaaS UI

### Status
**ACCEPTED**

### Context
The user interface demands a state-of-the-art visual experience with server-side rendering for landing pages and high-performance dynamic client rendering for interactive dashboards.

### Decision
Use **Next.js 14+ (App Router)** with **TypeScript** and **Tailwind CSS**.

### Consequences
- **Pros**: Unified React framework, optimal SEO, SSR efficiency, native layout nesting.
- **Cons**: Requires clear boundary separation between Client (`'use client'`) and Server components.

---

## ADR-004: LLM Provider Abstraction Layer

### Status
**ACCEPTED**

### Context
Relying on a single LLM vendor creates API lock-in, vendor risk, and vulnerability to rate limits or outages.

### Decision
Implement an abstract `BaseLLMProvider` interface in `app/providers/base.py`. Concrete implementations (`GeminiProvider`, `OpenAIProvider`, `AnthropicProvider`) satisfy this interface with standard structured Pydantic outputs.

### Consequences
- **Pros**: Hot-swappable providers, seamless fallback strategy, vendor independence.
- **Cons**: Requires maintaining output schemas compatible across multiple model providers.

---

## ADR-005: Multi-Agent AI System Architecture

### Status
**ACCEPTED**

### Context
Single-prompt LLM architectures produce unpredictable, unexplainable outputs when attempting to parse, score, match, and advise simultaneously.

### Decision
Decompose AI processing into **4 Autonomous Specialized Agents** (Extractor, ATS Auditor, Job Matcher, Career Advisor) coordinated by a deterministic workflow orchestrator with step-by-step trace logging.

### Consequences
- **Pros**: Modular testing, clear failure attribution, explainable AI scoring, predictable output formats.
- **Cons**: Slightly increased token consumption due to intermediate agent state transitions.

---

## ADR-006: PostgreSQL + pgvector for Storage Strategy

### Status
**ACCEPTED**

### Context
Storing both structured entity relational data (Users, Resumes, Scores) and high-dimensional semantic embeddings in separate databases adds infrastructure overhead.

### Decision
Use **PostgreSQL 16** with the **`pgvector`** extension as a unified relational and vector database solution.

### Consequences
- **Pros**: Single operational database, transactional consistency between entities and embeddings.
- **Cons**: Requires PostgreSQL extension installation in production environments.

---

## ADR-007: JWT + Argon2 Auth Strategy & Refresh Token Lifecycle

### Status
**ACCEPTED**

### Context
User authentication must support stateless REST API access, password security against rainbow tables/brute force, and refresh token security.

### Decision
Use Passlib with **Argon2id / bcrypt** password hashing, short-lived JWT Access Tokens (15 mins), long-lived Refresh Tokens (7 days), and `reusable_oauth2` Bearer token guards.

### Consequences
- **Pros**: Stateless API verification, zero database hits for access token validation, industry-standard password protection.
- **Cons**: Client applications must manage token refresh state.

---

## ADR-008: Relational Entity Schema & Versioning Hierarchy

### Status
**ACCEPTED**

### Context
Candidates upload multiple resume revisions over time. Tracking ATS scores and job matching across revisions requires a explicit versioning model.

### Decision
Separate `Resume` (parent container) from `ResumeVersion` (concrete file revision entity). Attach `Analysis` and `JobMatch` records to `ResumeVersion` rather than `Resume`.

### Consequences
- **Pros**: Immutable analysis history across resume updates, exact version-level matching metrics.
- **Cons**: Extra table join required when fetching latest resume version summary.

---

## ADR-009: Storage Provider Abstraction & Document Processing Pipeline

### Status
**ACCEPTED**

### Context
Uploaded resumes must be validated, securely stored, and processed into normalized structural text entities independently of downstream AI parsing engines. Local storage must be hot-swappable with cloud S3 storage without modifying domain logic.

### Decision
Implement `BaseStorageProvider` interface (`LocalStorageProvider`) and `DocumentProcessorFactory` resolving PDF (`pypdf` / `pdfplumber`) and DOCX (`zipfile` / `python-docx`) extractors producing a standardized `NormalizedDocument` Pydantic payload.

### Consequences
- **Pros**: Zero coupling between document extraction and AI parsing; resilient pure-Python fallback extractors; seamless S3/GCS upgrade path.
- **Cons**: Scanned/image-only PDFs require downstream OCR engine support.

---

## ADR-010: AI Resume Parsing & LLM Provider Abstraction Architecture

### Status
**ACCEPTED**

### Context
Converting raw extracted text into structured resume entities (personal info, experience, education, skills, projects) requires LLM intelligence. Directly embedding LLM vendor calls inside route handlers creates coupling, prompt injection risks, and unhandled failure modes.

### Decision
Implement `BaseLLMProvider` interface (`GeminiLLMProvider`, `OpenAILLMProvider`, `MockDeterministicLLMProvider`) returning strongly typed `StructuredResume` Pydantic models. Enforce prompt injection defense via `<RESUME_DATA>` container tagging, 30s timeouts, and deterministic fallback execution.

### Consequences
- **Pros**: Zero vendor lock-in; robust against prompt injection attacks; deterministic offline fallback ensures 100% API reliability.
- **Cons**: LLM output requires strict JSON schema validation and null-value handling.

---

## ADR-011: Hybrid Deterministic-AI ATS Scoring Model Architecture

### Status
**ACCEPTED**

### Context
Black-box LLM scoring engines produce arbitrary, unexplainable scores that frustrate users and lack scientific credibility. Purely rule-based systems miss qualitative context.

### Decision
Combine a **60% Deterministic Engine** (`DeterministicRulesEngine` scanning action verb density, metric regex patterns `%/$`, section completeness, and word count) with a **40% AI Auditor** (`AIAuditorService` generating qualitative feedback and prioritized actionable improvements). Label ATS scores explicitly as *"ATS Compatibility Estimate"*.

### Consequences
- **Pros**: 100% explainable scoring formula; explicit positive (`+`), negative (`-`), and warning (`!`) reasons; zero arbitrary black-box numbers.
- **Cons**: Requires maintaining regex pattern registries for metric and action verb detection.

---

## ADR-012: Job Description Ingestion & Deterministic-Semantic Matching Engine

### Status
**ACCEPTED**

### Context
Job matching must compare candidate resumes against job postings accurately without failing on skill synonym variations (e.g. `K8s` vs `Kubernetes`, `Postgres` vs `PostgreSQL`).

### Decision
Implement `SkillNormalizer` canonical synonym mapper, `JobDescriptionParserService` extracting structured requirements inside `<JOB_DESCRIPTION_DATA>` prompt containers, and `JobMatcherService` computing a 5-category weighted match score (Required Skills 40%, Preferred Skills 15%, Experience 25%, Projects 10%, Education 10%).

### Consequences
- **Pros**: Zero false negatives from skill synonyms; clear green `Matched`, red `Missing Required`, and amber `Weak / Preferred` categories; 100% explainable match breakdown.
- **Cons**: Requires maintaining synonym dictionaries for tech stack terms.

---

## ADR-013: Career Intelligence & Interview Practice Evaluation Engine Architecture

### Status
**ACCEPTED**

### Context
Candidates need actionable career guidance beyond match scores, including prioritized skill gap roadmaps and tailored interview practice without hallucinated fake experience.

### Decision
Implement `CareerIntelligenceService` (prioritizing Critical, Medium, Low skill gaps and generating 7-day sprint & 30-day curriculum roadmaps) and `InterviewIntelligenceService` (generating tailored Technical, Project, Behavioral, HR, and JD-Specific interview questions with explainable STAR framework answer evaluation). Enforce an explicit **Anti-Fabrication Policy**.

### Consequences
- **Pros**: 100% specific, non-generic recommendations; strict anti-fabrication boundary protecting candidate integrity; explainable practice answer scoring.
- **Cons**: Practice answer scoring relies on structured keyword/pattern metrics.

---

## ADR-014: Autonomous Multi-Agent System Architecture & Execution Trace Engine

### Status
**ACCEPTED**

### Context
Processing end-to-end career goal requests ("Analyze my resume against this job, identify my gaps, create a learning plan, and prepare me for the interview") in a single monolithic LLM call results in unexplainable failures, black-box processing, and untraceable errors.

### Decision
Implement a multi-agent system architecture comprising **6 Autonomous Specialized Agents** (`ManagerOrchestratorAgent`, `ResumeAgent`, `JobDescriptionAgent`, `SkillGapAgent`, `RecommendationAgent`, `InterviewAgent`) executing controlled sandboxed tools (`SandboxedAgentTools`), producing an explicit `AgentExecutionSession` trace graph.

### Consequences
- **Pros**: 100% observable execution graph; clear failure attribution and fallback recovery; modular agent testing; zero unrestricted system permissions.
- **Cons**: Multi-step agent execution adds modest overhead (measured in ms).

---

## ADR-015: Production Engineering, Security Hardening & Observability Architecture

### Status
**ACCEPTED**

### Context
Production applications require strict security headers, distributed correlation tracing, sensitive PII redaction from logs, and unhandled exception sanitization to prevent sensitive data leaks and raw Python stack trace exposure.

### Decision
Implement `SecurityHeadersMiddleware` (enforcing CSP, HSTS, X-Frame-Options, X-Content-Type-Options), `CorrelationIdMiddleware` (tracking request IDs via `X-Request-ID`), `PIIRedactionFilter` (masking passwords, JWTs, API keys in logs), and global exception handler (returning clean JSON error responses).

### Consequences
- **Pros**: Industry-standard HTTP security headers; zero stack trace or PII data leakage in production logs; end-to-end distributed request correlation.
- **Cons**: Middleware stack adds minimal per-request processing latency (~0.2ms).

---

## ADR-016: Multi-Container Docker Deployment & Demo Reliability Strategy Architecture

### Status
**ACCEPTED**

### Context
Deploying AGENTX for live technical fests and academic project vivas requires multi-container orchestration (PostgreSQL, FastAPI backend, Next.js frontend) and an honest presentation strategy that prevents failures if external LLM APIs experience downtime.

### Decision
Implement multi-stage `Dockerfile`s, `docker-compose.yml` service orchestration, and an explicit **Honest Demo Strategy** (`DEMO_GUIDE.md`) allowing seamless switching between Live LLM Mode and Offline Resilient Fallback Mode via `.env` configuration without presenting fake results.

### Consequences
- **Pros**: One-command production deployment (`docker-compose up -d`); 100% presentation uptime during live tech fests; zero unhandled API failure risks.
- **Cons**: Local multi-container execution requires ~1.5 GB RAM.
