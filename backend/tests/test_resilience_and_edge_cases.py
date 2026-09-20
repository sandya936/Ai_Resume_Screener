import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_empty_document_upload_rejected(async_client: AsyncClient):
    reg = await async_client.post(
        "/api/v1/auth/register",
        json={"email": "empty_doc@example.com", "password": "Password123!", "full_name": "Empty User"},
    )
    token = reg.json()["data"]["tokens"]["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    files = {"file": ("empty.pdf", b"", "application/pdf")}
    res = await async_client.post("/api/v1/resumes/upload", headers=headers, files=files)
    assert res.status_code == 400
    assert res.json()["error"]["code"] in ["EMPTY_FILE", "INVALID_FILE_HEADER"]


@pytest.mark.asyncio
async def test_corrupted_document_upload_rejected(async_client: AsyncClient):
    reg = await async_client.post(
        "/api/v1/auth/register",
        json={"email": "corrupt_doc@example.com", "password": "Password123!", "full_name": "Corrupt User"},
    )
    token = reg.json()["data"]["tokens"]["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    files = {"file": ("corrupt.pdf", b"NOT_A_VALID_PDF_HEADER_CONTENT_STRING_XYZ", "application/pdf")}
    res = await async_client.post("/api/v1/resumes/upload", headers=headers, files=files)
    assert res.status_code == 400
    assert res.json()["error"]["code"] in ["CORRUPTED_FILE", "INVALID_FILE_HEADER"]


@pytest.mark.asyncio
async def test_unsupported_file_extension_rejected(async_client: AsyncClient):
    reg = await async_client.post(
        "/api/v1/auth/register",
        json={"email": "exe_user@example.com", "password": "Password123!", "full_name": "Exe User"},
    )
    token = reg.json()["data"]["tokens"]["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    files = {"file": ("malicious.exe", b"MZ_EXECUTABLE_BINARY_DATA", "application/x-msdownload")}
    res = await async_client.post("/api/v1/resumes/upload", headers=headers, files=files)
    assert res.status_code == 400
    assert res.json()["error"]["code"] in ["UNSUPPORTED_EXTENSION", "UNSUPPORTED_FILE_TYPE"]
