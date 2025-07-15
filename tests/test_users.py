import pytest
from httpx import AsyncClient


test_user = {
    "username": "testuser",
    "password": "testpass123"
}


@pytest.mark.asyncio
async def test_register_user(async_client: AsyncClient):
    response = await async_client.post("/register", json=test_user)
    assert response.status_code in (200, 400)


@pytest.mark.asyncio
async def test_login_user(async_client: AsyncClient):
    response = await async_client.post("/token", data={
        "username": test_user["username"],
        "password": test_user["password"]
    })
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    return data["access_token"]


@pytest.mark.asyncio
async def test_get_current_user(async_client: AsyncClient):
    login_response = await async_client.post("/token", data={
        "username": test_user["username"],
        "password": test_user["password"]
    })
    token = login_response.json()["access_token"]

    response = await async_client.get(
        "/users/me/",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert response.json()["username"] == test_user["username"]
