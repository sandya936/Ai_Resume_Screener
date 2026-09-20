import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_register_user_success(async_client: AsyncClient):
    response = await async_client.post(
        "/api/v1/auth/register",
        json={
            "email": "alice@example.com",
            "password": "SecurePassword123!",
            "full_name": "Alice Smith",
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["success"] is True
    assert data["data"]["user"]["email"] == "alice@example.com"
    assert data["data"]["user"]["profile"]["full_name"] == "Alice Smith"
    assert "access_token" in data["data"]["tokens"]
    assert "refresh_token" in data["data"]["tokens"]


@pytest.mark.asyncio
async def test_register_duplicate_email(async_client: AsyncClient):
    # First registration
    await async_client.post(
        "/api/v1/auth/register",
        json={
            "email": "duplicate@example.com",
            "password": "SecurePassword123!",
            "full_name": "Original User",
        },
    )
    # Duplicate registration
    response = await async_client.post(
        "/api/v1/auth/register",
        json={
            "email": "duplicate@example.com",
            "password": "AnotherPassword123!",
            "full_name": "Imposter User",
        },
    )
    assert response.status_code == 400
    data = response.json()
    assert data["success"] is False
    assert data["error"]["code"] == "DUPLICATE_EMAIL"


@pytest.mark.asyncio
async def test_login_success(async_client: AsyncClient):
    # Register first
    await async_client.post(
        "/api/v1/auth/register",
        json={
            "email": "bob@example.com",
            "password": "MySecretPassword123!",
            "full_name": "Bob Builder",
        },
    )
    # Login
    response = await async_client.post(
        "/api/v1/auth/login",
        json={
            "email": "bob@example.com",
            "password": "MySecretPassword123!",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["data"]["user"]["email"] == "bob@example.com"
    assert "access_token" in data["data"]["tokens"]


@pytest.mark.asyncio
async def test_login_invalid_password(async_client: AsyncClient):
    await async_client.post(
        "/api/v1/auth/register",
        json={
            "email": "charlie@example.com",
            "password": "CorrectPassword123!",
            "full_name": "Charlie Brown",
        },
    )
    response = await async_client.post(
        "/api/v1/auth/login",
        json={
            "email": "charlie@example.com",
            "password": "WrongPassword123!",
        },
    )
    assert response.status_code == 401
    data = response.json()
    assert data["success"] is False
    assert data["error"]["code"] == "INVALID_CREDENTIALS"


@pytest.mark.asyncio
async def test_read_current_user_authenticated_and_unauthenticated(async_client: AsyncClient):
    # 1. Unauthenticated call
    unauth_resp = await async_client.get("/api/v1/auth/me")
    assert unauth_resp.status_code == 401

    # 2. Register & get token
    reg_resp = await async_client.post(
        "/api/v1/auth/register",
        json={
            "email": "diana@example.com",
            "password": "DianaPassword123!",
            "full_name": "Diana Prince",
        },
    )
    access_token = reg_resp.json()["data"]["tokens"]["access_token"]

    # 3. Authenticated call
    auth_resp = await async_client.get(
        "/api/v1/auth/me",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert auth_resp.status_code == 200
    data = auth_resp.json()
    assert data["success"] is True
    assert data["data"]["email"] == "diana@example.com"


@pytest.mark.asyncio
async def test_refresh_token_flow(async_client: AsyncClient):
    reg_resp = await async_client.post(
        "/api/v1/auth/register",
        json={
            "email": "eve@example.com",
            "password": "EvePassword123!",
            "full_name": "Eve Adams",
        },
    )
    refresh_token = reg_resp.json()["data"]["tokens"]["refresh_token"]

    ref_resp = await async_client.post(
        "/api/v1/auth/refresh",
        json={"refresh_token": refresh_token},
    )
    assert ref_resp.status_code == 200
    data = ref_resp.json()
    assert data["success"] is True
    assert "access_token" in data["data"]
    assert "refresh_token" in data["data"]


@pytest.mark.asyncio
async def test_logout(async_client: AsyncClient):
    reg_resp = await async_client.post(
        "/api/v1/auth/register",
        json={
            "email": "frank@example.com",
            "password": "FrankPassword123!",
            "full_name": "Frank Castle",
        },
    )
    access_token = reg_resp.json()["data"]["tokens"]["access_token"]

    logout_resp = await async_client.post(
        "/api/v1/auth/logout",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert logout_resp.status_code == 200
    assert logout_resp.json()["success"] is True
