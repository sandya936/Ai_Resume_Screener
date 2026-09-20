import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_get_and_update_user_profile(async_client: AsyncClient):
    reg_resp = await async_client.post(
        "/api/v1/auth/register",
        json={
            "email": "profile_user@example.com",
            "password": "Password123!",
            "full_name": "Initial Name",
        },
    )
    access_token = reg_resp.json()["data"]["tokens"]["access_token"]
    headers = {"Authorization": f"Bearer {access_token}"}

    # Get profile
    get_resp = await async_client.get("/api/v1/users/profile", headers=headers)
    assert get_resp.status_code == 200
    assert get_resp.json()["data"]["full_name"] == "Initial Name"

    # Update profile
    update_resp = await async_client.put(
        "/api/v1/users/profile",
        headers=headers,
        json={
            "full_name": "Updated Name",
            "location": "San Francisco, CA",
            "target_role": "Lead Architect",
            "bio": "Passionate full stack developer",
        },
    )
    assert update_resp.status_code == 200
    updated_data = update_resp.json()["data"]
    assert updated_data["full_name"] == "Updated Name"
    assert updated_data["location"] == "San Francisco, CA"
    assert updated_data["target_role"] == "Lead Architect"


@pytest.mark.asyncio
async def test_user_isolation(async_client: AsyncClient):
    # User A
    user_a_reg = await async_client.post(
        "/api/v1/auth/register",
        json={
            "email": "user_a@example.com",
            "password": "Password123!",
            "full_name": "User A",
        },
    )
    token_a = user_a_reg.json()["data"]["tokens"]["access_token"]

    # User B
    user_b_reg = await async_client.post(
        "/api/v1/auth/register",
        json={
            "email": "user_b@example.com",
            "password": "Password123!",
            "full_name": "User B",
        },
    )
    token_b = user_b_reg.json()["data"]["tokens"]["access_token"]

    # User A profile request with User A's token
    res_a = await async_client.get(
        "/api/v1/users/profile",
        headers={"Authorization": f"Bearer {token_a}"},
    )
    assert res_a.json()["data"]["full_name"] == "User A"

    # User B profile request with User B's token
    res_b = await async_client.get(
        "/api/v1/users/profile",
        headers={"Authorization": f"Bearer {token_b}"},
    )
    assert res_b.json()["data"]["full_name"] == "User B"
