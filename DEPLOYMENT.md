# AGENTX — Production Deployment Guide

This document provides complete instructions for building, configuring, deploying, and operating **AGENTX** in a production environment.

---

## 1. Prerequisites

- **Docker**: Version 24.0+
- **Docker Compose**: Version 2.20+
- **PostgreSQL**: Version 16.0+ (or containerized via Compose)
- **Node.js**: Version 20.0+ (for frontend local development)
- **Python**: Version 3.11+ (for backend local development)

---

## 2. Docker Compose Quickstart

1. **Clone repository & prepare environment**:
   ```bash
   cp .env.example .env
   ```
2. **Launch multi-container stack**:
   ```bash
   docker-compose up -d --build
   ```
3. **Verify running containers**:
   ```bash
   docker-compose ps
   ```
   - `agentx_db`: PostgreSQL 16 (Port 5432)
   - `agentx_backend`: FastAPI API Server (Port 8000)
   - `agentx_frontend`: Next.js Standalone SaaS Dashboard (Port 3000)

4. **Verify health check**:
   ```bash
   curl http://localhost:8000/api/v1/health
   ```

---

## 3. Database Migrations (Alembic)

To apply database migrations inside the container:
```bash
docker-compose exec backend alembic upgrade head
```

---

## 4. Environment Variables Reference

| Variable | Description | Default / Example |
| :--- | :--- | :--- |
| `PROJECT_NAME` | Name of project | `AGENTX` |
| `ENVIRONMENT` | Environment mode (`development`, `production`) | `production` |
| `DATABASE_URL` | Async PostgreSQL connection string | `postgresql+asyncpg://...` |
| `SECRET_KEY` | JWT signing secret key | `64-char hex string` |
| `LLM_PROVIDER` | Active LLM provider (`mock`, `gemini`, `openai`) | `mock` |
| `GEMINI_API_KEY` | Google Gemini API Key | `AIzaSy...` |

---

## 5. Security & SSL Setup (Nginx Reverse Proxy Example)

Place an Nginx reverse proxy in front of the services:

```nginx
server {
    listen 443 ssl http2;
    server_name agentx.example.com;

    ssl_certificate /etc/letsencrypt/live/agentx.example.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/agentx.example.com/privkey.pem;

    location / {
        proxy_pass http://localhost:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /api/ {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Request-ID $request_id;
    }
}
```
