# AGENTX — Engineering & Development Guidelines

This document details coding standards, directory conventions, clean architecture rules, git workflows, and quality assurance practices for **AGENTX**.

---

## 1. Code Style & Quality Standards

### Python (Backend)
- **Code Formatter**: Black (line length 88).
- **Import Sorting**: isort with profile `black`.
- **Linter**: Ruff / Flake8.
- **Type Checking**: mypy (strict type hints required for all function signatures and returns).
- **Docstrings**: Google docstring style for public classes and functions.

### TypeScript / Next.js (Frontend)
- **Formatter & Linter**: ESLint + Prettier.
- **Type Safety**: No explicit `any` types allowed. Use strict interfaces in `src/types/`.
- **Component Design**: Functional React components with hooks. Prefer server components unless client interactivity (`'use client'`) is explicitly required.

---

## 2. Clean Architecture Rules

1. **Domain Isolation**: Code in `app/domain` must not import from `app/api`, `app/services`, or `app/db`.
2. **Interface Abstraction**: Services must depend on abstract base classes (interfaces) for external infrastructure components (e.g., storage, LLM providers).
3. **Pydantic Schemas**: Use Pydantic models for validation at the API boundary (`app/domain/schemas`) and internal domain entities (`app/domain/entities`).

---

## 3. Git Commit Conventions & Branch Strategy

Follow Conventional Commits specification:

- `feat(phase1): add master architecture documentation suite`
- `fix(auth): resolve JWT expiration timestamp validation bug`
- `docs(readme): update system quickstart instructions`
- `refactor(db): optimize user model indexes`
- `test(health): add health endpoint contract test`

### Branch Strategy:
- `main`: Production-ready release branch.
- `development`: Active integration branch.
- `feature/phase-X-...`: Dedicated feature branches per phase.

---

## 4. Testing Standards

- **Unit Tests**: Test individual domain services, helper utilities, and parsing rules in isolation using mocks for external dependencies.
- **Integration Tests**: Test API endpoints with an in-memory or test database instance using `httpx.AsyncClient`.
- **Test Coverage**: Maintain >= 80% code coverage across core domain and application service layers.
