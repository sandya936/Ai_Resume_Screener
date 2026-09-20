# AGENTX — Database Schema Design

This document details the PostgreSQL relational data model, table structures, column definitions, data types, indexes, and constraints implemented in **AGENTX**.

---

## Entity-Relationship Diagram

```
 [users] (1) ───< (1) [user_profiles]
    │
    ├───< (N) [resumes] (1) ───< (N) [resume_versions]
    │          │                          │
    │          └──── (1) ──> [parsed_resumes]
    │                                     │
    ├───< (N) [job_descriptions]          ├────< (N) [analyses] (ATS, Career & Agent Traces)
    │               │                     │
    │               └─────── (1) ─────────┼────< (N) [job_matches]
    │                                     │
    └───< (N) [audit_logs]                │
```

---

## Table Specifications

### 1. `users`
System user credentials, roles, and status flags.

```sql
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    role VARCHAR(50) NOT NULL DEFAULT 'user',
    is_active BOOLEAN NOT NULL DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL
);

CREATE INDEX idx_users_email ON users(email);
```

### 2. `user_profiles`
User profile information (1-to-1 relationship with `users`).

```sql
CREATE TABLE user_profiles (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID UNIQUE NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    full_name VARCHAR(255) NOT NULL,
    phone VARCHAR(50),
    bio TEXT,
    avatar_url VARCHAR(512),
    location VARCHAR(255),
    target_role VARCHAR(255),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL
);
```

### 3. `resumes`
Parent container for uploaded resume documents.

```sql
CREATE TABLE resumes (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(255) NOT NULL,
    is_primary BOOLEAN NOT NULL DEFAULT false,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL
);

CREATE INDEX idx_resumes_user_id ON resumes(user_id);
```

### 4. `resume_versions`
Specific file version revisions of a resume.

```sql
CREATE TABLE resume_versions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    resume_id UUID NOT NULL REFERENCES resumes(id) ON DELETE CASCADE,
    version_number INTEGER NOT NULL DEFAULT 1,
    filename VARCHAR(255) NOT NULL,
    file_path VARCHAR(512) NOT NULL,
    file_size_bytes INTEGER NOT NULL,
    mime_type VARCHAR(100) NOT NULL,
    sha256_checksum VARCHAR(64) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL
);

CREATE INDEX idx_resume_versions_resume_id ON resume_versions(resume_id);
CREATE INDEX idx_resume_versions_checksum ON resume_versions(sha256_checksum);
```

### 5. `parsed_resumes`
Structured candidate profile extracted by AI parser & updated with ATS score.

```sql
CREATE TABLE parsed_resumes (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    resume_id UUID UNIQUE NOT NULL REFERENCES resumes(id) ON DELETE CASCADE,
    raw_text TEXT NOT NULL,
    contact_info JSONB NOT NULL DEFAULT '{}',
    summary TEXT,
    work_experience JSONB NOT NULL DEFAULT '[]',
    education JSONB NOT NULL DEFAULT '[]',
    skills JSONB NOT NULL DEFAULT '{}',
    projects JSONB NOT NULL DEFAULT '[]',
    certifications JSONB NOT NULL DEFAULT '[]',
    ats_score INTEGER,
    ats_feedback JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL
);

CREATE INDEX idx_parsed_resumes_resume_id ON parsed_resumes(resume_id);
```

### 6. `analyses` (Phase 8 Updated)
Document extraction payloads, ATS score, quality audit results, career guidance, and multi-agent execution session traces.

```sql
CREATE TABLE analyses (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    resume_version_id UUID NOT NULL REFERENCES resume_versions(id) ON DELETE CASCADE,
    analysis_type VARCHAR(100) NOT NULL, -- 'document_extraction', 'ats_score', 'career_insights', 'agent_orchestration_trace'
    status VARCHAR(50) NOT NULL DEFAULT 'pending',
    score INTEGER,
    payload JSONB NOT NULL DEFAULT '{}', -- Stores AgentExecutionSession JSON payload
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL
);

CREATE INDEX idx_analyses_version_id ON analyses(resume_version_id);
```

### 7. `job_descriptions`
Target job postings.

```sql
CREATE TABLE job_descriptions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(255) NOT NULL,
    company_name VARCHAR(255),
    raw_text TEXT NOT NULL,
    required_skills JSONB NOT NULL DEFAULT '[]',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL
);

CREATE INDEX idx_job_descriptions_user_id ON job_descriptions(user_id);
```

### 8. `job_matches`
Semantic and keyword matching evaluations.

```sql
CREATE TABLE job_matches (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    resume_version_id UUID NOT NULL REFERENCES resume_versions(id) ON DELETE CASCADE,
    job_description_id UUID NOT NULL REFERENCES job_descriptions(id) ON DELETE CASCADE,
    match_score INTEGER NOT NULL,
    matching_skills JSONB NOT NULL DEFAULT '[]',
    missing_skills JSONB NOT NULL DEFAULT '[]',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL
);

CREATE INDEX idx_job_matches_version_job ON job_matches(resume_version_id, job_description_id);
```

### 9. `audit_logs`
Security actions and system audit trail.

```sql
CREATE TABLE audit_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    action VARCHAR(100) NOT NULL,
    resource_type VARCHAR(100) NOT NULL,
    resource_id VARCHAR(255),
    ip_address VARCHAR(45),
    details JSONB NOT NULL DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL
);

CREATE INDEX idx_audit_logs_user_action ON audit_logs(user_id, action);
```
