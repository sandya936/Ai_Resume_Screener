import pytest
from httpx import AsyncClient
from app.core.logging import PIIRedactionFilter
import logging


@pytest.mark.asyncio
async def test_security_headers_present(async_client: AsyncClient):
    response = await async_client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.headers.get("X-Content-Type-Options") == "nosniff"
    assert response.headers.get("X-Frame-Options") == "DENY"
    assert response.headers.get("X-XSS-Protection") == "1; mode=block"
    assert "Strict-Transport-Security" in response.headers
    assert "Content-Security-Policy" in response.headers


@pytest.mark.asyncio
async def test_request_id_correlation(async_client: AsyncClient):
    response = await async_client.get("/api/v1/health", headers={"X-Request-ID": "custom-req-12345"})
    assert response.status_code == 200
    assert response.headers.get("X-Request-ID") == "custom-req-12345"


def test_pii_logging_sanitization():
    filter_obj = PIIRedactionFilter()

    rec1 = logging.LogRecord("test", logging.INFO, "path", 10, 'User login {"password": "SuperSecretPassword123!"}', (), None)
    filter_obj.filter(rec1)
    assert "SuperSecretPassword123!" not in rec1.msg
    assert "[REDACTED_PASSWORD]" in rec1.msg

    rec2 = logging.LogRecord("test", logging.INFO, "path", 10, 'Auth header: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9', (), None)
    filter_obj.filter(rec2)
    assert "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9" not in rec2.msg
    assert "[REDACTED_BEARER_TOKEN]" in rec2.msg


@pytest.mark.asyncio
async def test_unauthorized_token_rejection(async_client: AsyncClient):
    res = await async_client.get("/api/v1/users/profile", headers={"Authorization": "Bearer invalid_token_xxx"})
    assert res.status_code in [401, 403]
