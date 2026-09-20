# AGENTX — Security Architecture & Data Protection Policy

This document outlines the security controls, authentication standards, prompt injection defenses, privacy guidelines, and access controls implemented in **AGENTX**.

---

## 1. Authentication & Authorization Controls (Phase 2 Implemented)

- **Password Protection**: Passlib with **Argon2id** and **bcrypt** password hashing with salt and cost factor controls. Plaintext passwords are never stored or logged.
- **JWT Architecture**:
  - Access Token: HMAC-SHA256 (`HS256`), 15-minute expiration window.
  - Refresh Token: `HS256`, 7-day expiration window.
- **Token Verification**: FastAPI `OAuth2PasswordBearer` dependency (`app/api/deps.py`) validating `sub` user UUID and `type` token claim.
- **User-to-User Data Isolation**:
  - Domain resources verify `resource.user_id == current_user.id` using `verify_resource_owner` guard.
  - Cross-tenant data access attempts return `403 Forbidden`.

---

## 2. File Security & Upload Guardrails (Phase 3 Implemented)

- **Strict Extension Filtering**: Only `.pdf` and `.docx` extensions permitted.
- **MIME Type Validation**: `application/pdf` and `application/vnd.openxmlformats-officedocument.wordprocessingml.document`.
- **Magic Bytes Header Verification**: `%PDF-` for PDF, `PK\x03\x04` for DOCX. Defeats extension spoofing.
- **Filename Sanitization**: Strip path traversal components (`../`, `..\`) and special characters (`sanitize_filename`).
- **UUID File Masking**: Files stored under `resumes/{uuid}.pdf` to prevent arbitrary file execution.
- **File Size Limit**: Strict 10MB (`MAX_FILE_SIZE_BYTES`) limit.
- **SHA-256 Checksum Hashing**: Computes exact file checksums for auditing.

---

## 3. Multi-Agent Sandboxing & Tool Permissions (Phase 8 Implemented)

- **Controlled Tool Registry**: Agents interact strictly through permission-controlled function interfaces (`SandboxedAgentTools`).
- **Zero Unrestricted Access**: Agents cannot execute arbitrary database writes, shell commands, or network requests outside the registry.
- **Prompt Injection Defense Across Agent Boundaries**:
  - Resume, Job Description, and User Goal text are strictly treated as DATA. Wrapped in XML container tags (`<RESUME_DATA>`, `<JOB_DESCRIPTION_DATA>`, `<USER_ANSWER_DATA>`).
  - Malicious instructions inside input text cannot override Manager Agent orchestration plans or tool parameters.

---

## 4. Production Security Headers & PII Redaction Policy (Phase 9 Implemented)

- **HTTP Security Headers Middleware**:
  - `X-Content-Type-Options: nosniff` (Prevents MIME sniffing attacks).
  - `X-Frame-Options: DENY` (Protects against clickjacking attacks).
  - `X-XSS-Protection: 1; mode=block` (Enforces browser XSS filtering).
  - `Strict-Transport-Security: max-age=31536000; includeSubDomains` (Enforces HTTPS).
  - `Content-Security-Policy: default-src 'self'` (Restricts content sources).
- **PII Logging Sanitization Filter**:
  - `PIIRedactionFilter` redacts sensitive fields (`password`, `access_token`, `refresh_token`, `secret_key`, `Bearer <token>`) from all application log output.
  - Zero raw resume documents, passwords, or credentials logged to stdout or log files.
- **Correlation ID Tracking**: `CorrelationIdMiddleware` injects `X-Request-ID` to trace security events across distributed requests.
- **Global Unhandled Exception Sanitization**: Intercepts internal exceptions, logging correlation IDs while returning sanitized JSON responses without Python stack trace leakage.

---

## 5. Anti-Fabrication & Candidate Integrity Policy (Phase 7 & 8 Implemented)

- **Strict Anti-Fabrication Boundary**: Recommendations and interview suggestions must **NEVER** invent fake work experience, hallucinate metrics, or suggest false credentials.
- **Clear Information Distinctions**:
  - **Known Information**: Verified from candidate uploaded resume.
  - **Inferred Information**: Derived from job market tech stack benchmarks.
  - **Recommendations**: Suggested truthful resume formatting improvements and learning milestones.

---

## 6. Environment Secret Management

- Secrets (JWT `SECRET_KEY`, Database passwords, API Keys) managed exclusively via `.env` environment variables loaded via Pydantic `BaseSettings`.
- Zero hardcoded secrets in codebase.
