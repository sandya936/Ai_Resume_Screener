# AGENTX — Known Issues & Technical Debt Register

This document tracks known limitations, architectural boundaries, risk mitigation strategies, and planned technical debt items for **AGENTX**.

---

## Risk Matrix & Mitigation Strategies

| Risk / Issue ID | Component | Description | Impact | Mitigation Strategy |
| :--- | :--- | :--- | :---: | :--- |
| **RISK-001** | LLM Extraction | External LLM API rate limits or downtime. | High | Provider Abstraction with automatic fallback to `MockDeterministicLLMProvider`. |
| **RISK-002** | File Extraction | Unstandardized PDF structures (column layouts, graphics) leading to text garbling. | Medium | Dual-engine extraction strategy (`pypdf` + `pdfplumber` fallback; pure-Python `zipfile` DOCX fallback). |
| **RISK-003** | Scanned PDFs | Image-only scanned PDFs contain zero extractable text strings. | Medium | Extractor sets `ocr_fallback_required = True`. |
| **RISK-004** | Prompt Injection | Malicious resumes, job postings, or practice answers attempting LLM system prompt override. | High | Enclosed text in XML container tags (`<RESUME_DATA>`, `<JOB_DESCRIPTION_DATA>`, `<USER_ANSWER_DATA>`). |
| **RISK-005** | ATS Estimate | Proprietary ATS vendors (Workday, Taleo, iCIMS) use closed parsing rules. | Low | Explicitly labeled as "ATS Compatibility Estimate" with disclaimer wording in UI. |
| **RISK-006** | Skill Synonyms | Non-standard or rare skill acronyms in job postings. | Low | Skill Normalizer dictionary translates common tech stack terms (`K8s` -> `kubernetes`). |
| **RISK-007** | Agent Latency | Multi-agent workflow involves 6 agent execution steps. | Low | Asynchronous tool execution & step-by-step trace graph streaming. |
| **RISK-008** | PII Redaction | Unstructured log statements might contain unflagged sensitive strings. | Low | `PIIRedactionFilter` enforces regex redaction on all log records. |

---

## Technical Debt & Optimization Log

1. **Phase 1 Baseline**: Architecture blueprints and scaffold initialized.
2. **Phase 2 DB Engine**: Production database runs PostgreSQL 16 (`asyncpg`); unit test suite utilizes in-memory SQLite (`aiosqlite`).
3. **Phase 3 Extractor Resilience**: Extractors feature pure-Python fallbacks (`pypdf`, `zipfile`+`ElementTree`) to operate reliably in DLL-restricted environments.
4. **Phase 4 LLM Resilience**: LLM providers feature 30-second timeout handling and fallback to deterministic mock parser.
5. **Phase 5 Hybrid Engine**: ATS scoring combines 60% deterministic rule analysis with 40% AI reasoning recommendations.
6. **Phase 6 Skill Normalization**: Skill Normalizer resolves tech stack synonyms to eliminate false negative skill gap flags.
7. **Phase 7 Anti-Fabrication**: Career recommendations explicitly prohibit fabricating fake experience or false metrics.
8. **Phase 8 Multi-Agent System**: 6 specialized agents coordinated by Manager Orchestrator with observable execution trace engine.
9. **Phase 9 Production Engineering**: HTTP Security Headers, Correlation Request ID tracking, PII Log Redaction Filter, Global Exception Sanitization, and 44 passing Pytest suite cases.
